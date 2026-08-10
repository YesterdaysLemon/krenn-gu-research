"""Materialize one CNF disjoining canonical fixed-edge skeleton roles.

The base support CNF is augmented with one selector per canonical role
skeleton.  At least one selector is true, and a true selector fixes all 25
block indicators to that skeleton.  This converts an independently
enumerated incremental batch into one proof-producing CNF.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import hashlib
import json
from pathlib import Path

from eight_vertex_skeleton_batch import (
    canonical_degree_three_role_skeletons,
    canonical_minimum_five_skeletons,
    canonical_normalized_killer_skeletons,
    canonical_role_skeletons,
    ordered_role_skeletons,
)
from krenn_gu.eight_vertex_sparse_exact import local_allowed_edges


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dimacs_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("base file is not DIMACS CNF")
    return int(variables), int(clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6",
        type=Path,
        default=Path("tmp/n8_mindeg3_e12_16.g6"),
    )
    parser.add_argument("--target-edges", type=int, default=16)
    parser.add_argument(
        "--all-edge-counts",
        action="store_true",
        help="include every edge count present in graph6",
    )
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=4,
    )
    parser.add_argument(
        "--expected-roles",
        type=int,
        help="optional fail-closed check on the canonical role count",
    )
    parser.add_argument(
        "--role-index",
        type=int,
        action="append",
        help=(
            "include only this zero-based role from the full canonical "
            "catalogue; repeat for a selected case union"
        ),
    )
    parser.add_argument(
        "--assumption",
        type=int,
        action="append",
        help="append this fixed DIMACS literal as a unit clause; repeatable",
    )
    parser.add_argument(
        "--base-cnf",
        type=Path,
        default=Path(
            "tmp/eight_vertex_local_degree4_cegar1_max16.cnf"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_16edge_catalogue_cegar1.cnf"
        ),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "tmp/eight_vertex_16edge_catalogue_cegar1.json"
        ),
    )
    args = parser.parse_args()

    target_edges = (
        None if args.all_edge_counts else args.target_edges
    )
    catalogue_builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[args.center_degree]
    roles, catalogue = catalogue_builder(
        args.graph6, target_edges=target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    if (
        args.expected_roles is not None
        and len(ordered_roles) != args.expected_roles
    ):
        raise AssertionError(
            "canonical role catalogue size changed: "
            f"{len(ordered_roles)} != {args.expected_roles}"
        )
    if target_edges is not None and any(
        len(skeleton) != target_edges for skeleton in ordered_roles
    ):
        raise AssertionError("catalogue contains the wrong edge count")
    indexed_roles = list(enumerate(ordered_roles))
    if args.role_index:
        selected_role_indices = sorted(set(args.role_index))
        if (
            selected_role_indices[0] < 0
            or selected_role_indices[-1] >= len(ordered_roles)
        ):
            raise ValueError("--role-index is outside the catalogue")
        indexed_roles = [
            (index, ordered_roles[index])
            for index in selected_role_indices
        ]
    else:
        selected_role_indices = list(range(len(ordered_roles)))
    selected_roles = [role for _, role in indexed_roles]
    old_variables, old_clauses = dimacs_header(args.base_cnf)
    fixed_assumptions = sorted(set(args.assumption or []))
    if any(-literal in fixed_assumptions for literal in fixed_assumptions):
        raise ValueError("fixed assumptions contain a contradiction")
    if any(
        not literal or abs(literal) > old_variables
        for literal in fixed_assumptions
    ):
        raise ValueError("fixed assumption references an unknown variable")
    selectors = [
        old_variables + 1 + index
        for index in range(len(selected_roles))
    ]
    allowed = local_allowed_edges(args.center_degree)
    first_block_variable = 1 + 9 * len(allowed)
    added_clauses = (
        1
        + len(selected_roles) * len(allowed)
        + len(fixed_assumptions)
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open(
        "r", encoding="ascii"
    ) as reader, args.output.open("w", encoding="ascii") as writer:
        next(reader)
        writer.write(
            f"p cnf {old_variables + len(selectors)} "
            f"{old_clauses + added_clauses}\n"
        )
        for line in reader:
            writer.write(line)
        for literal in fixed_assumptions:
            writer.write(f"{literal} 0\n")
        writer.write(" ".join(map(str, selectors)) + " 0\n")
        for selector, skeleton in zip(
            selectors, selected_roles, strict=True
        ):
            present = set(skeleton)
            for edge_index, edge in enumerate(allowed):
                block = first_block_variable + edge_index
                literal = block if edge in present else -block
                writer.write(f"-{selector} {literal} 0\n")

    payload = {
        "scope": (
            "all canonical connected matching-covered n=8 "
            + (
                f"{target_edges}-edge"
                if target_edges is not None
                else "all-edge-count"
            )
            + (
                " minimum-degree-five skeleton roles"
                if args.center_degree == 0
                else (
                    " normalized generic-killer skeleton roles"
                    if args.center_degree == 1
                    else (
                        f" skeleton roles with a degree-"
                        f"{args.center_degree} vertex"
                    )
                )
            )
        ),
        **catalogue,
        "target_edges": target_edges,
        "center_degree": args.center_degree,
        "graph6": str(args.graph6),
        "graph6_sha256": sha256(args.graph6),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "full_canonical_roles": len(ordered_roles),
        "selected_role_indices": selected_role_indices,
        "fixed_assumptions": fixed_assumptions,
        "selectors": len(selectors),
        "selector_implications": len(selected_roles) * len(allowed),
        "variables": old_variables + len(selectors),
        "clauses": old_clauses + added_clauses,
        "output": str(args.output),
        "output_sha256": sha256(args.output),
    }
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
