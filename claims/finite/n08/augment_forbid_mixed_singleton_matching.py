"""Append the negation of a mixed monochromatic-singleton perfect matching.

The complete-ambient n=8 support generator allocates one exact indicator
``s[e,c]`` for every edge and colour.  It is true exactly when the whole
``3 x 3`` block on ``e`` consists of one nonzero diagonal entry ``(c,c)``.

For every perfect matching and every nonconstant assignment of colours to
its four edges, this extension appends

    OR_e not s[e, colour[e]].

Thus a SAT model of the extension has no mixed perfect matching made
entirely of monochromatic singleton blocks.  An UNSAT decision proves that
the base relaxation forces such a matching.
"""

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
import hashlib
import itertools
import json
from pathlib import Path

from krenn_gu.search_witness import EquationSystem


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("input is not a DIMACS CNF")
    return int(variables), int(clauses)


def mixed_singleton_clauses(
    singleton_base: int,
) -> list[tuple[int, ...]]:
    system = EquationSystem(8, 3)

    def singleton(edge: tuple[int, int], colour: int) -> int:
        return (
            singleton_base
            + system.edge_index[edge] * system.d
            + colour
        )

    clauses: list[tuple[int, ...]] = []
    for matching in system.matchings:
        for colours in itertools.product(
            range(system.d),
            repeat=system.n // 2,
        ):
            if len(set(colours)) == 1:
                continue
            clauses.append(
                tuple(
                    -singleton(edge, colour)
                    for edge, colour in zip(
                        matching,
                        colours,
                        strict=True,
                    )
                )
            )
    if len(clauses) != 105 * (3**4 - 3):
        raise AssertionError("mixed singleton clause count changed")
    if len(set(clauses)) != len(clauses):
        raise AssertionError("mixed singleton clauses are not unique")
    return clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--singleton-base",
        type=int,
        default=821,
        help=(
            "first singleton indicator; 821 is the allocation after "
            "the complete K8 entry/block variables and max-20 counter"
        ),
    )
    args = parser.parse_args()

    old_variables, old_clause_count = header(args.base_cnf)
    clauses = mixed_singleton_clauses(args.singleton_base)
    largest_singleton = args.singleton_base + 28 * 3 - 1
    if largest_singleton > old_variables:
        raise ValueError("singleton allocation exceeds the CNF header")

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as source, (
        args.output_cnf.open("w", encoding="ascii", newline="\n")
    ) as target:
        next(source)
        target.write(
            f"p cnf {old_variables} "
            f"{old_clause_count + len(clauses)}\n"
        )
        for line in source:
            target.write(line)
        for clause in clauses:
            target.write(" ".join(map(str, clause)) + " 0\n")

    payload = {
        "scope": (
            "negation of a mixed monochromatic-singleton perfect "
            "matching in the complete-ambient n=8 support relaxation"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "variables": old_variables,
        "base_clauses": old_clause_count,
        "appended_clauses": len(clauses),
        "output_clauses": old_clause_count + len(clauses),
        "singleton_base": args.singleton_base,
        "singleton_variables": 28 * 3,
        "perfect_matchings": 105,
        "mixed_edge_colourings_per_matching": 3**4 - 3,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
