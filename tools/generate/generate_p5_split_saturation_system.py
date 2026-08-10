#!/usr/bin/env python3
"""Convert a direct P5 saturation program to split inverse variables."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.p5_split_saturation import convert_text  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--algorithm",
        choices=("slimgb", "std"),
        default="slimgb",
    )
    args = parser.parse_args()
    converted = convert_text(
        args.input.read_text(encoding="utf-8"),
        args.algorithm,
    )
    args.output.write_text(
        converted,
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
