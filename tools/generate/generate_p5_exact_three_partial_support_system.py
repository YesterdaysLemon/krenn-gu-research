"""Regenerate one exact-three-partial P5 support system independently."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

import generate_p5_one_partial_support_system as BASE


def generate(
    supports: tuple[tuple[int, ...], ...],
    signature_indices: tuple[int, ...],
) -> tuple[str, dict]:
    return BASE.generate(
        supports,
        signature_indices,
        expected_partial_cells=3,
    )


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
