"""Write 252 DIMACS unit clauses from a complete entry-support model."""

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
from pathlib import Path

from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from krenn_gu.search_witness import EquationSystem


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
