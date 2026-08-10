"""Write 252 DIMACS unit clauses from a complete entry-support model."""

from __future__ import annotations

import argparse
from pathlib import Path

from eight_vertex_sparse_exact import positive_model_literals
from search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    positive = positive_model_literals(args.model)
    literals = [
        variable if variable in positive else -variable
        for variable in range(1, system.variable_count + 1)
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(f"{literal} 0\n" for literal in literals),
        encoding="ascii",
    )
    print(f"unit_clauses={len(literals)}")


if __name__ == "__main__":
    main()
