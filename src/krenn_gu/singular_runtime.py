"""Portable bounded Singular process execution shared by claim tooling."""

from __future__ import annotations

import os
import subprocess
import time


SINGULAR_COMMAND = (
    "wsl.exe",
    "--exec",
    "/usr/bin/Singular",
    "-q",
)


def singular_command_with_timeout(timeout: float) -> tuple[str, ...]:
    if timeout <= 0:
        raise ValueError("Singular timeout must be positive")
    if os.name != "nt":
        return SINGULAR_COMMAND
    return (
        "wsl.exe",
        "--exec",
        "/usr/bin/timeout",
        "--signal=KILL",
        f"{timeout:.6f}s",
        "/usr/bin/Singular",
        "-q",
    )


def run_singular(program: str, timeout: float) -> dict:
    started = time.monotonic()
    infrastructure_attempts = []
    for attempt in range(3):
        try:
            completed = subprocess.run(
                singular_command_with_timeout(timeout),
                input=program,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                timeout=timeout + 5,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "infrastructure_attempts": infrastructure_attempts,
            }
        output = completed.stdout + completed.stderr
        normalized_output = output.replace("\x00", "")
        infrastructure_attempts.append(
            {
                "returncode": completed.returncode,
                "wsl_service_unexpected": (
                    "WSL/Service/E_UNEXPECTED" in normalized_output
                ),
            }
        )
        if (
            os.name != "nt"
            or "WSL/Service/E_UNEXPECTED" not in normalized_output
            or attempt == 2
        ):
            break
        time.sleep(1.5 * (attempt + 1))
    status = (
        "UNIT_IDEAL"
        if "UNIT_IDEAL" in output
        else "SURVIVOR"
        if "SURVIVOR" in output
        else "ERROR"
    )
    return {
        "status": status,
        "returncode": completed.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "output_tail": output[-2000:],
        "infrastructure_attempts": infrastructure_attempts,
    }


__all__ = ["SINGULAR_COMMAND", "run_singular", "singular_command_with_timeout"]
