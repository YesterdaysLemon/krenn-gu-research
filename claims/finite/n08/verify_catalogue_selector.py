"""Audit a selector compilation and its optional UNSAT proof artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from eight_vertex_skeleton_batch import (
    canonical_degree_three_role_skeletons,
    canonical_minimum_five_skeletons,
    canonical_normalized_killer_skeletons,
    canonical_role_skeletons,
    ordered_role_skeletons,
)
from eight_vertex_sparse_exact import local_allowed_edges


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dimacs_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError(f"{path} is not DIMACS CNF")
    return int(variables), int(clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--cadical-log", type=Path)
    parser.add_argument("--drat-log", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads(
        args.manifest.read_text(encoding="utf-8")
    )
    center_degree = int(manifest.get("center_degree", 4))
    target_edges = manifest.get("target_edges")
    if target_edges is not None:
        target_edges = int(target_edges)
    graph6 = Path(str(manifest["graph6"]))
    base_cnf = Path(str(manifest["base_cnf"]))
    selector_cnf = Path(str(manifest["output"]))
    if sha256(graph6) != manifest["graph6_sha256"]:
        raise AssertionError("graph6 hash mismatch")
    if sha256(base_cnf) != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash mismatch")
    if sha256(selector_cnf) != manifest["output_sha256"]:
        raise AssertionError("selector CNF hash mismatch")

    builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[center_degree]
    roles, catalogue = builder(
        graph6, target_edges=target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    for key, value in catalogue.items():
        if int(manifest[key]) != value:
            raise AssertionError(f"catalogue field changed: {key}")
    selected_role_indices = list(
        map(
            int,
            manifest.get(
                "selected_role_indices", range(len(ordered_roles))
            ),
        )
    )
    if (
        selected_role_indices != sorted(set(selected_role_indices))
        or any(
            index < 0 or index >= len(ordered_roles)
            for index in selected_role_indices
        )
    ):
        raise AssertionError("selected role indices are not canonical")
    selected_roles = [
        ordered_roles[index] for index in selected_role_indices
    ]
    fixed_assumptions = list(
        map(int, manifest.get("fixed_assumptions", []))
    )
    if fixed_assumptions != sorted(set(fixed_assumptions)) or any(
        -literal in fixed_assumptions for literal in fixed_assumptions
    ):
        raise AssertionError("fixed assumptions are not canonical")

    base_variables, base_clauses = dimacs_header(base_cnf)
    selector_variables, selector_clauses = dimacs_header(
        selector_cnf
    )
    allowed = local_allowed_edges(center_degree)
    selectors = [
        base_variables + 1 + index
        for index in range(len(selected_roles))
    ]
    implications = len(selected_roles) * len(allowed)
    if (
        int(manifest["selectors"]),
        int(manifest["selector_implications"]),
        int(manifest["variables"]),
        int(manifest["clauses"]),
    ) != (
        len(selectors),
        implications,
        base_variables + len(selectors),
        base_clauses + len(fixed_assumptions) + 1 + implications,
    ):
        raise AssertionError("selector dimensions are inconsistent")
    if (selector_variables, selector_clauses) != (
        int(manifest["variables"]),
        int(manifest["clauses"]),
    ):
        raise AssertionError("selector DIMACS header changed")

    first_block_variable = 1 + 9 * len(allowed)
    with base_cnf.open(
        "r", encoding="ascii"
    ) as base, selector_cnf.open("r", encoding="ascii") as combined:
        next(base)
        next(combined)
        for clause_index, line in enumerate(base, start=1):
            if combined.readline() != line:
                raise AssertionError(
                    "selector changed the base at clause "
                    f"{clause_index}"
                )
        for literal in fixed_assumptions:
            if combined.readline() != f"{literal} 0\n":
                raise AssertionError("fixed assumption unit changed")
        expected = " ".join(map(str, selectors)) + " 0\n"
        if combined.readline() != expected:
            raise AssertionError("selector disjunction changed")
        for selector, skeleton in zip(
            selectors, selected_roles, strict=True
        ):
            present = set(skeleton)
            for edge_index, edge in enumerate(allowed):
                block = first_block_variable + edge_index
                literal = block if edge in present else -block
                expected = f"-{selector} {literal} 0\n"
                if combined.readline() != expected:
                    raise AssertionError(
                        "selector implication changed"
                    )
        if combined.readline():
            raise AssertionError("selector CNF has an unexpected tail")

    proof_payload: dict[str, object] = {}
    if args.proof is not None:
        proof_payload = {
            "proof_bytes": args.proof.stat().st_size,
            "proof_sha256": sha256(args.proof),
        }
    if args.cadical_log is not None:
        log = args.cadical_log.read_text(encoding="utf-8")
        if "s UNSATISFIABLE" not in log:
            raise AssertionError("CaDiCaL UNSAT terminal is missing")
        proof_payload["cadical_log_sha256"] = sha256(
            args.cadical_log
        )
    if args.drat_log is not None:
        log = args.drat_log.read_text(encoding="utf-8")
        if "s VERIFIED" not in log:
            raise AssertionError("DRAT verification terminal is missing")
        proof_payload["drat_log_sha256"] = sha256(args.drat_log)

    payload = {
        "verified": True,
        "center_degree": center_degree,
        "target_edges": target_edges,
        **catalogue,
        "selectors": len(selectors),
        "full_canonical_roles": len(ordered_roles),
        "selected_role_indices": selected_role_indices,
        "fixed_assumptions": fixed_assumptions,
        "selector_implications": implications,
        "variables": selector_variables,
        "clauses": selector_clauses,
        "graph6_sha256": manifest["graph6_sha256"],
        "base_cnf_sha256": manifest["base_cnf_sha256"],
        "selector_cnf_sha256": manifest["output_sha256"],
        **proof_payload,
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
