"""Regenerate one exact-two-partial P5 support system independently."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.p5_exact_two_support_system import generate  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--supports", required=True)
    parser.add_argument("--indices", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    supports = tuple(
        tuple(map(int, row))
        for row in ast.literal_eval(args.supports)
    )
    indices = tuple(map(int, args.indices.split(",")))
    program, metadata = generate(supports, indices)
    args.output.write_text(program, encoding="utf-8", newline="\n")
    print(metadata)


if __name__ == "__main__":
    main()
