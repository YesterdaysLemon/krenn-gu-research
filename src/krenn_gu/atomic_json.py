"""Portable atomic JSON output for repository operator tools."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path


def atomic_write(path: Path, payload: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for attempt in range(50):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if os.name != "nt" or attempt == 49:
                raise
            time.sleep(0.1)


__all__ = ["atomic_write"]
