"""Focused tests for the bounded research-process runner."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "research" / "run_bounded.py"
SPEC = importlib.util.spec_from_file_location("run_bounded", RUNNER)
assert SPEC is not None and SPEC.loader is not None
RUN_BOUNDED = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUN_BOUNDED
SPEC.loader.exec_module(RUN_BOUNDED)


class BoundedResearchRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.run_root = pathlib.Path(self.temporary.name) / "runs"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(
        self,
        run_id: str,
        timeout: float,
        command: list[str],
        memory_mb: int = 256,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--run-id",
                run_id,
                "--timeout-seconds",
                str(timeout),
                "--memory-mb",
                str(memory_mb),
                "--run-root",
                str(self.run_root),
                "--cwd",
                str(ROOT),
                "--",
                *command,
            ],
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )

    def metadata(self, run_id: str) -> dict[str, object]:
        files = list((self.run_root / run_id).glob("*/run.json"))
        self.assertEqual(len(files), 1)
        return json.loads(files[0].read_text(encoding="utf-8"))

    def test_success_records_output_and_metadata(self) -> None:
        result = self.invoke(
            "success",
            5,
            [sys.executable, "-c", "print('bounded hello')"],
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("bounded hello", result.stdout)
        metadata = self.metadata("success")
        self.assertEqual(metadata["status"], "succeeded")
        self.assertEqual(metadata["runner_exit_code"], 0)
        log = pathlib.Path(str(metadata["log"])).read_text(encoding="utf-8")
        self.assertEqual(log, "bounded hello\n")

    def test_limited_console_encoding_does_not_truncate_utf8_log(self) -> None:
        stream = io.StringIO("before\nrelation \u27fa value\nafter\n")
        log = io.StringIO()
        state = RUN_BOUNDED._OutputPumpState()
        console_bytes = io.BytesIO()
        console = io.TextIOWrapper(
            console_bytes,
            encoding="cp1252",
            errors="strict",
        )

        try:
            with mock.patch.object(RUN_BOUNDED.sys, "stdout", console):
                RUN_BOUNDED._pump_output(stream, log, state)
            console.flush()
            echoed = console_bytes.getvalue().decode("cp1252")
        finally:
            console.detach()

        self.assertIsNone(state.failure)
        self.assertEqual(log.getvalue(), "before\nrelation \u27fa value\nafter\n")
        self.assertIn(r"relation \u27fa value", echoed)
        self.assertEqual(echoed.splitlines()[-1], "after")

    def test_output_pump_failure_cannot_report_success(self) -> None:
        class FailingConsole:
            encoding = "utf-8"
            errors = "strict"

            def write(self, _text: str) -> None:
                raise OSError("console unavailable")

            def flush(self) -> None:
                pass

        config = RUN_BOUNDED.RunConfig(
            run_id="output-failure",
            timeout_seconds=5,
            memory_mb=256,
            run_root=self.run_root,
            cwd=ROOT,
            command=(
                sys.executable,
                "-c",
                "print('first line'); print('child completed')",
            ),
        )

        with mock.patch.object(RUN_BOUNDED.sys, "stdout", FailingConsole()):
            result = RUN_BOUNDED.run(config)

        self.assertEqual(result, RUN_BOUNDED.EXIT_OUTPUT_FAILED)
        metadata = self.metadata("output-failure")
        self.assertEqual(metadata["status"], "output_failed")
        self.assertEqual(metadata["child_exit_code"], 0)
        self.assertEqual(metadata["runner_exit_code"], result)
        self.assertIn("console unavailable", metadata["output_error"])
        log = pathlib.Path(str(metadata["log"])).read_text(encoding="utf-8")
        self.assertEqual(log, "first line\nchild completed\n")

    def test_timeout_returns_124_and_records_terminal_state(self) -> None:
        result = self.invoke(
            "timeout",
            0.25,
            [sys.executable, "-c", "import time; time.sleep(30)"],
        )

        self.assertEqual(result.returncode, RUN_BOUNDED.EXIT_TIMEOUT)
        metadata = self.metadata("timeout")
        self.assertEqual(metadata["status"], "timed_out")
        self.assertEqual(metadata["runner_exit_code"], RUN_BOUNDED.EXIT_TIMEOUT)

    def test_duplicate_run_id_is_rejected(self) -> None:
        self.run_root.mkdir(parents=True)
        owner = {"run_id": "duplicate", "runner_pid": os.getpid()}
        lock_path = self.run_root / "duplicate.lock"
        with RUN_BOUNDED.run_lock(lock_path, owner):
            result = self.invoke(
                "duplicate",
                5,
                [sys.executable, "-c", "print('must not run')"],
            )

        self.assertEqual(result.returncode, RUN_BOUNDED.EXIT_DUPLICATE)
        self.assertIn("already active", result.stderr)
        self.assertFalse((self.run_root / "duplicate").exists())

    def test_long_ephemeral_python_is_rejected_before_launch(self) -> None:
        result = self.invoke(
            "anonymous",
            61,
            [sys.executable, "-c", "print('must not run')"],
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("must use a durable script or module", result.stderr)
        self.assertFalse(self.run_root.exists())

    def test_long_ephemeral_python_after_options_is_rejected(self) -> None:
        config = RUN_BOUNDED.RunConfig(
            run_id="anonymous-options",
            timeout_seconds=61,
            memory_mb=256,
            run_root=self.run_root,
            cwd=ROOT,
            command=(sys.executable, "-X", "dev", "-u", "-c", "print('x')"),
        )

        with self.assertRaisesRegex(ValueError, "durable script or module"):
            RUN_BOUNDED.validate_config(config)

    def test_timeout_reaps_owned_tree(self) -> None:
        result = self.invoke(
            "reap-tree",
            0.25,
            [
                sys.executable,
                "-c",
                (
                    "import os,subprocess,sys,time; "
                    "p=subprocess.Popen([sys.executable,'-c',"
                    "'import time; time.sleep(30)']); "
                    "print(os.getpid(),p.pid,flush=True); time.sleep(30)"
                ),
            ],
        )

        self.assertEqual(result.returncode, RUN_BOUNDED.EXIT_TIMEOUT)
        pids = [int(value) for value in result.stdout.strip().splitlines()[0].split()]
        for pid in pids:
            self.assert_process_exits(pid)

    def assert_process_exits(self, pid: int) -> None:
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except OSError:
                return
            time.sleep(0.05)
        self.fail(f"owned process still exists: {pid}")

    @unittest.skipUnless(os.name == "nt", "KILL_ON_JOB_CLOSE is Windows-specific")
    def test_abrupt_runner_exit_reaps_owned_tree(self) -> None:
        command = (
            "import os,subprocess,sys,time; "
            "p=subprocess.Popen([sys.executable,'-c',"
            "'import time; time.sleep(30)']); "
            "print(os.getpid(),p.pid,flush=True); time.sleep(30)"
        )
        runner = subprocess.Popen(
            [
                sys.executable,
                str(RUNNER),
                "--run-id",
                "owner-exit",
                "--timeout-seconds",
                "30",
                "--memory-mb",
                "256",
                "--run-root",
                str(self.run_root),
                "--cwd",
                str(ROOT),
                "--",
                sys.executable,
                "-c",
                command,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            assert runner.stdout is not None
            pids = [int(value) for value in runner.stdout.readline().split()]
            self.assertEqual(len(pids), 2)
            runner.kill()
            runner.wait(timeout=5)
            for pid in pids:
                self.assert_process_exits(pid)
        finally:
            if runner.poll() is None:
                runner.kill()
                runner.wait(timeout=5)
            if runner.stdout is not None:
                runner.stdout.close()
            if runner.stderr is not None:
                runner.stderr.close()


if __name__ == "__main__":
    unittest.main()
