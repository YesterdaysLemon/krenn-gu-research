#!/usr/bin/env python3
"""Run a research command with ownership, logging, and resource bounds.

This is an execution-safety tool, not a scientific verifier.  It launches the
command without a shell, records durable local metadata, rejects duplicate
run identifiers, enforces a wall-clock timeout, and terminates the owned
process tree on timeout or interruption.

On Windows the child tree is assigned to a Job Object with
KILL_ON_JOB_CLOSE and an aggregate job-memory limit.  On POSIX the child gets
its own process group and an RLIMIT_AS limit where the platform provides it.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import datetime as dt
import errno
import json
import os
import pathlib
import re
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from typing import BinaryIO, Iterator, Sequence


EXIT_DUPLICATE = 73
EXIT_LAUNCH_FAILED = 127
EXIT_TIMEOUT = 124
EXIT_INTERRUPTED = 130
EXIT_CONTAINMENT_FAILED = 125
LONG_RUN_SECONDS = 60.0
RUN_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")
PYTHON_EXE_RE = re.compile(
    r"(?:python|pythonw|python\d+(?:\.\d+)?|pypy\d*)(?:\.exe)?\Z",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RunConfig:
    """Validated runner inputs."""

    run_id: str
    timeout_seconds: float
    memory_mb: int
    run_root: pathlib.Path
    cwd: pathlib.Path
    command: tuple[str, ...]


class DuplicateRunError(RuntimeError):
    """Raised when another runner holds the same run-id lock."""


def utc_now() -> str:
    """Return a stable UTC timestamp for run metadata."""

    return dt.datetime.now(dt.timezone.utc).isoformat()


def _write_json(path: pathlib.Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _lock_byte(handle: BinaryIO) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        return

    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _unlock_byte(handle: BinaryIO) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return

    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextlib.contextmanager
def run_lock(path: pathlib.Path, owner: dict[str, object]) -> Iterator[None]:
    """Hold a crash-releasing, cross-process lock for one run identifier."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        if path.stat().st_size == 0:
            handle.write(b"\0")
            handle.flush()
        try:
            _lock_byte(handle)
        except OSError as exc:
            if exc.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                raise DuplicateRunError(
                    f"run id is already active: {owner['run_id']}"
                ) from exc
            raise
        try:
            handle.seek(1)
            handle.truncate()
            handle.write(json.dumps(owner, sort_keys=True).encode("utf-8"))
            handle.flush()
            yield
        finally:
            _unlock_byte(handle)


class _WindowsJob:
    """Minimal Windows Job Object wrapper for owned child-tree cleanup."""

    JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9

    def __init__(self, memory_bytes: int) -> None:
        from ctypes import wintypes

        class IoCounters(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong),
            ]

        class BasicLimitInformation(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class ExtendedLimitInformation(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BasicLimitInformation),
                ("IoInfo", IoCounters),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        kernel32.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        kernel32.SetInformationJobObject.restype = wintypes.BOOL
        kernel32.AssignProcessToJobObject.argtypes = [
            wintypes.HANDLE,
            wintypes.HANDLE,
        ]
        kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
        kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        kernel32.TerminateJobObject.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL

        handle = kernel32.CreateJobObjectW(None, None)
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())

        limits = ExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = (
            self.JOB_OBJECT_LIMIT_JOB_MEMORY | self.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        limits.JobMemoryLimit = memory_bytes
        if not kernel32.SetInformationJobObject(
            handle,
            self.JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            error = ctypes.WinError(ctypes.get_last_error())
            kernel32.CloseHandle(handle)
            raise error

        self._kernel32 = kernel32
        self._handle = handle

    def assign(self, process: subprocess.Popen[str]) -> None:
        from ctypes import wintypes

        process_handle = wintypes.HANDLE(process._handle)  # noqa: SLF001
        if not self._kernel32.AssignProcessToJobObject(self._handle, process_handle):
            raise ctypes.WinError(ctypes.get_last_error())

    def terminate(self, exit_code: int) -> None:
        if self._handle and not self._kernel32.TerminateJobObject(
            self._handle, exit_code
        ):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self) -> None:
        if self._handle:
            self._kernel32.CloseHandle(self._handle)
            self._handle = None


def _posix_memory_limit(memory_bytes: int):
    def set_limit() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))

    return set_limit


def _command_uses_ephemeral_python(command: Sequence[str]) -> bool:
    executable = pathlib.Path(command[0]).name
    if not PYTHON_EXE_RE.fullmatch(executable):
        return False
    arguments = list(command[1:])
    index = 0
    options_with_separate_values = {"-W", "-X", "--check-hash-based-pycs"}
    while index < len(arguments):
        argument = arguments[index]
        if argument in {"-", "-c"}:
            return True
        if argument == "-m":
            return False
        if not argument.startswith("-"):
            return False
        if argument in options_with_separate_values:
            index += 1
        index += 1
    return True


def validate_config(config: RunConfig) -> None:
    """Validate boundaries before creating a child process."""

    if not RUN_ID_RE.fullmatch(config.run_id):
        raise ValueError(
            "run-id must be 1-80 characters using letters, digits, '.', '_', "
            "or '-', and must start with a letter or digit"
        )
    if config.timeout_seconds <= 0:
        raise ValueError("timeout-seconds must be positive")
    if config.memory_mb <= 0:
        raise ValueError("memory-mb must be positive")
    if not config.command:
        raise ValueError("a command is required after '--'")
    if not config.cwd.is_dir():
        raise ValueError(f"cwd is not a directory: {config.cwd}")
    if config.timeout_seconds > LONG_RUN_SECONDS and _command_uses_ephemeral_python(
        config.command
    ):
        raise ValueError(
            "Python runs longer than 60 seconds must use a durable script or "
            "module, not stdin or -c"
        )


def _pump_output(stream, log_handle) -> None:
    try:
        for line in iter(stream.readline, ""):
            log_handle.write(line)
            log_handle.flush()
            sys.stdout.write(line)
            sys.stdout.flush()
    finally:
        stream.close()


def _windows_containment_child(command: Sequence[str]) -> int:
    """Wait for Job assignment, then launch the real command inside the Job."""

    if sys.stdin.buffer.read(1) != b"G":
        print("run_bounded: containment gate closed before assignment", file=sys.stderr)
        return EXIT_CONTAINMENT_FAILED
    try:
        child = subprocess.Popen(list(command))
    except OSError as exc:
        print(f"run_bounded: launch failed: {exc}", file=sys.stderr)
        return EXIT_LAUNCH_FAILED
    return child.wait()


def _terminate_process_tree(
    process: subprocess.Popen[str],
    windows_job: _WindowsJob | None,
    exit_code: int,
) -> None:
    if process.poll() is not None:
        return
    if windows_job is not None:
        windows_job.terminate(exit_code)
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)


def run(config: RunConfig) -> int:
    """Execute one validated bounded run and return the runner exit code."""

    validate_config(config)
    started_at = utc_now()
    started_clock = time.monotonic()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_directory = config.run_root / config.run_id / f"{stamp}-{os.getpid()}"
    run_directory.mkdir(parents=True, exist_ok=False)
    metadata_path = run_directory / "run.json"
    log_path = run_directory / "run.log"
    metadata: dict[str, object] = {
        "schema_version": 1,
        "run_id": config.run_id,
        "runner_pid": os.getpid(),
        "command": list(config.command),
        "cwd": str(config.cwd.resolve()),
        "started_at": started_at,
        "timeout_seconds": config.timeout_seconds,
        "memory_mb": config.memory_mb,
        "status": "starting",
        "log": str(log_path.resolve()),
    }
    _write_json(metadata_path, metadata)

    memory_bytes = config.memory_mb * 1024 * 1024
    windows_job: _WindowsJob | None = None
    if os.name == "nt":
        try:
            windows_job = _WindowsJob(memory_bytes)
        except OSError as exc:
            metadata.update(
                status="containment_failed",
                error=f"{type(exc).__name__}: {exc}",
                finished_at=utc_now(),
                elapsed_seconds=round(time.monotonic() - started_clock, 3),
                runner_exit_code=EXIT_CONTAINMENT_FAILED,
            )
            _write_json(metadata_path, metadata)
            print(f"run_bounded: containment failed: {exc}", file=sys.stderr)
            return EXIT_CONTAINMENT_FAILED
    popen_kwargs: dict[str, object] = {
        "cwd": config.cwd,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "bufsize": 1,
    }
    launched_command = list(config.command)
    if os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        popen_kwargs["stdin"] = subprocess.PIPE
        launched_command = [
            sys.executable,
            str(pathlib.Path(__file__).resolve()),
            "--_windows-containment-child",
            *config.command,
        ]
    else:
        popen_kwargs["start_new_session"] = True
        popen_kwargs["preexec_fn"] = _posix_memory_limit(memory_bytes)

    process: subprocess.Popen[str] | None = None
    output_thread: threading.Thread | None = None
    runner_code = EXIT_LAUNCH_FAILED
    try:
        with log_path.open("w", encoding="utf-8", newline="") as log_handle:
            try:
                process = subprocess.Popen(launched_command, **popen_kwargs)
                if windows_job is not None:
                    windows_job.assign(process)
                    assert process.stdin is not None
                    process.stdin.write("G")
                    process.stdin.close()
            except OSError as exc:
                if process is not None and process.poll() is None:
                    process.kill()
                    process.wait()
                metadata.update(
                    status="launch_failed",
                    error=f"{type(exc).__name__}: {exc}",
                )
                print(f"run_bounded: launch failed: {exc}", file=sys.stderr)
                return EXIT_LAUNCH_FAILED

            assert process.stdout is not None
            metadata.update(status="running", child_pid=process.pid)
            _write_json(metadata_path, metadata)
            output_thread = threading.Thread(
                target=_pump_output,
                args=(process.stdout, log_handle),
                name=f"run-bounded-output-{process.pid}",
                daemon=True,
            )
            output_thread.start()

            try:
                child_code = process.wait(timeout=config.timeout_seconds)
                runner_code = child_code
                metadata.update(
                    status="succeeded" if child_code == 0 else "failed",
                    child_exit_code=child_code,
                )
            except subprocess.TimeoutExpired:
                _terminate_process_tree(process, windows_job, EXIT_TIMEOUT)
                process.wait()
                runner_code = EXIT_TIMEOUT
                metadata.update(status="timed_out", child_exit_code=process.returncode)
            except KeyboardInterrupt:
                _terminate_process_tree(process, windows_job, EXIT_INTERRUPTED)
                process.wait()
                runner_code = EXIT_INTERRUPTED
                metadata.update(
                    status="interrupted", child_exit_code=process.returncode
                )
            if output_thread is not None:
                output_thread.join(timeout=3)
    finally:
        if process is not None and process.poll() is None:
            with contextlib.suppress(OSError):
                _terminate_process_tree(process, windows_job, runner_code)
            with contextlib.suppress(subprocess.TimeoutExpired):
                process.wait(timeout=3)
        if output_thread is not None:
            output_thread.join(timeout=3)
        if windows_job is not None:
            windows_job.close()
        metadata.update(
            finished_at=utc_now(),
            elapsed_seconds=round(time.monotonic() - started_clock, 3),
            runner_exit_code=runner_code,
        )
        _write_json(metadata_path, metadata)

    return runner_code


def parse_args(argv: Sequence[str] | None = None) -> RunConfig:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--timeout-seconds", required=True, type=float)
    parser.add_argument("--memory-mb", required=True, type=int)
    parser.add_argument(
        "--run-root",
        type=pathlib.Path,
        default=pathlib.Path(".research-runs"),
        help="local log/metadata root (default: .research-runs)",
    )
    parser.add_argument(
        "--cwd",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="child working directory (default: current directory)",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command and arguments, normally preceded by '--'",
    )
    args = parser.parse_args(argv)
    command = list(args.command)
    if command and command[0] == "--":
        command.pop(0)
    return RunConfig(
        run_id=args.run_id,
        timeout_seconds=args.timeout_seconds,
        memory_mb=args.memory_mb,
        run_root=args.run_root.resolve(),
        cwd=args.cwd.resolve(),
        command=tuple(command),
    )


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if raw_argv and raw_argv[0] == "--_windows-containment-child":
        if os.name != "nt":
            print(
                "run_bounded: Windows containment mode on non-Windows", file=sys.stderr
            )
            return EXIT_CONTAINMENT_FAILED
        return _windows_containment_child(raw_argv[1:])

    try:
        config = parse_args(raw_argv)
        validate_config(config)
    except ValueError as exc:
        print(f"run_bounded: {exc}", file=sys.stderr)
        return 2

    owner = {
        "run_id": config.run_id,
        "runner_pid": os.getpid(),
        "started_at": utc_now(),
        "cwd": str(config.cwd),
        "command": list(config.command),
    }
    lock_path = config.run_root / f"{config.run_id}.lock"
    previous_sigterm = None
    if hasattr(signal, "SIGTERM"):
        previous_sigterm = signal.getsignal(signal.SIGTERM)

        def interrupt_on_sigterm(_signum, _frame):
            raise KeyboardInterrupt

        signal.signal(signal.SIGTERM, interrupt_on_sigterm)
    try:
        with run_lock(lock_path, owner):
            return run(config)
    except DuplicateRunError as exc:
        print(f"run_bounded: {exc}", file=sys.stderr)
        return EXIT_DUPLICATE
    finally:
        if previous_sigterm is not None:
            signal.signal(signal.SIGTERM, previous_sigterm)


if __name__ == "__main__":
    raise SystemExit(main())
