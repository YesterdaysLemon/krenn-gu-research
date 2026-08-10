"""Run the all-even factor-fork analyzer over a deterministic support batch."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("output_prefix")
    parser.add_argument("--first-index", type=int, default=0)
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    total = len(exploration["survivors"])
    stop = total if args.limit is None else min(total, args.limit)
    statuses: dict[str, int] = {}
    started = time.perf_counter()
    completed = 0
    for index in range(args.first_index, stop, args.stride):
        output = Path(f"{args.output_prefix}{index}_factor_fork.json")
        command = [
            sys.executable,
            str(HERE / "analyze_fourteen_vertex_even_cycle_factor_fork.py"),
            str(args.exploration),
            "--survivor-index",
            str(index),
            "--output",
            str(output),
        ]
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(output.read_text(encoding="utf-8"))
        status = str(payload["status"])
        statuses[status] = statuses.get(status, 0) + 1
        completed += 1
        if completed % 5 == 0:
            print(
                f"completed={completed} index={index} "
                f"statuses={statuses}",
                flush=True,
            )

    summary = {
        "status": "batch_complete",
        "exploration": str(args.exploration),
        "first_index": args.first_index,
        "stride": args.stride,
        "stop": stop,
        "completed": completed,
        "statuses": statuses,
        "elapsed_seconds": time.perf_counter() - started,
    }
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
