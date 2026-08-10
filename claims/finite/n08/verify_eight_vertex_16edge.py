"""Fail-closed audit of the n=8 degree-four, exact-16-edge exclusion.

This verifier checks both layers of the certificate:

* the first exact Laurent support conflict and its twelve symmetries;
* the complete selector disjunction over all canonical essential skeleton
  roles, including the independently checked DRAT proof of UNSAT.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu.eight_vertex_degree4_cegar import (
    full_equations,
    laurent_conflict,
    symmetry_clauses,
)
from eight_vertex_degree4_support import decode_graph6
from eight_vertex_skeleton_batch import (
    canonical_role_skeletons,
    matching_covered,
)
from krenn_gu.eight_vertex_sparse_exact import (
    local_allowed_edges,
    positive_model_literals,
    selected_flat_indices,
)
from krenn_gu.search_witness import EquationSystem

EXPECTED = {
    "survivor_model": (
        "tmp/eight_vertex_local_degree4_max16.model",
        "504d4b16d131d2795fb684236f84328f678be5cef36ce49cb2c34e0198cac2bd",
    ),
    "base_cnf": (
        "tmp/eight_vertex_local_degree4_full_local_max16.cnf",
        "115904d925c3cf25ab3919f810b62a0a159749cc3bf78e0042c51fdb8148e100",
    ),
    "cegar_manifest": (
        "tmp/eight_vertex_local_degree4_cegar1.json",
        "2fa64532a0de628f3b8bba6874a8f9d8a6f38d84207fe561df9314b67faba97b",
    ),
    "cegar_cnf": (
        "tmp/eight_vertex_local_degree4_cegar1_max16.cnf",
        "570694ce87893c68f5900bde185203b8f2d6216d82da94454936e880e81b6d59",
    ),
    "graph6": (
        "tmp/n8_mindeg3_e12_16.g6",
        "27cd1f0ce69e65fb3fee28633c75e2f7925566df7856a394c3a0ab6e096548fe",
    ),
    "selector_manifest": (
        "tmp/eight_vertex_16edge_catalogue_cegar1.json",
        "2c147933fc87a63201908aab4ebecd6df8bd2b75c7c84b3e35932f4311e19264",
    ),
    "selector_cnf": (
        "tmp/eight_vertex_16edge_catalogue_cegar1.cnf",
        "04f3864a50a7443009998cf9fea0bd0f780753cfa3de390e740a3892683d5cf3",
    ),
    "minisat_model": (
        "tmp/eight_vertex_16edge_catalogue_cegar1.minisat.model",
        "8e47e39240b5b347f444074f97e7ab4b4c11d3f534469b5cb23f4b6d2f7390df",
    ),
    "minisat_log": (
        "tmp/eight_vertex_16edge_catalogue_cegar1.minisat.log",
        "4a0a3edcf5dee69b4dd433feb6d8f58e90480967137460f6e88a29c0e64d5c48",
    ),
    "proof": (
        "tmp/eight_vertex_16edge_catalogue_cegar1_cadical195.drat",
        "dad69926d0ac6fa23abb2c7812096990dd1dcb0c98f14c2773b3c6724f35d7e1",
    ),
    "cadical_log": (
        "tmp/eight_vertex_16edge_catalogue_cegar1_cadical195.log",
        "6a22924f6d803915e7301844eeb444f8fba6bbaa36fa6e7043987967f2b4c848",
    ),
    # Filled only after the independent checker reaches ``s VERIFIED``.
    "drat_log": (
        "tmp/eight_vertex_16edge_catalogue_cegar1_drat_trim.log",
        "a2fba233866031217990c22916defa7f45e0dfe1b196a2314632e09fe2907d3b",
    ),
}

BASE_VARIABLES = 394_821
BASE_CLAUSES = 2_849_784
CEGAR_CLAUSES = 2_849_796
SELECTOR_VARIABLES = 405_062
SELECTOR_CLAUSES = 3_105_822
SELECTORS = 10_241
SELECTOR_IMPLICATIONS = 256_025
PROOF_BYTES = 243_459_151
EXPECTED_RESOLUTION_STEPS = "211119420 resolution steps"


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


def connected(edges: set[tuple[int, int]]) -> bool:
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for edge in edges:
            if vertex not in edge:
                continue
            other = edge[0] if edge[1] == vertex else edge[1]
            if other not in seen:
                seen.add(other)
                frontier.append(other)
    return len(seen) == 8


def audit_laurent_replay(paths: dict[str, Path]) -> dict[str, object]:
    manifest = json.loads(
        paths["cegar_manifest"].read_text(encoding="utf-8")
    )
    system = EquationSystem(8, 3)
    positive_model = positive_model_literals(paths["survivor_model"])
    selected = set(selected_flat_indices(system, positive_model))
    equations, names, name_to_flat = full_equations(system)
    positive, negative, metadata = laurent_conflict(
        system,
        equations,
        names,
        name_to_flat,
        selected,
    )
    clauses = symmetry_clauses(system, positive, negative)

    expected_fields = {
        **metadata,
        "positive_entries": sorted(positive),
        "negative_entries": sorted(negative),
        "cube_size": len(positive) + len(negative),
        "stabilizer_size": 12,
        "distinct_learned_clauses": len(clauses),
        "learned_clauses": [list(clause) for clause in clauses],
    }
    for key, expected in expected_fields.items():
        if manifest.get(key) != expected:
            raise AssertionError(f"Laurent replay mismatch in {key}")
    if len(selected) != 34:
        raise AssertionError("first survivor is no longer a 34-entry stratum")
    if (
        metadata["binomial_equations"],
        metadata["binomial_rank"],
        len(positive) + len(negative),
        len(clauses),
    ) != (59, 16, 48, 12):
        raise AssertionError("Laurent conflict dimensions changed")
    return {
        "selected_entries": len(selected),
        "restricted_equations": metadata["restricted_equations"],
        "binomial_equations": metadata["binomial_equations"],
        "binomial_rank": metadata["binomial_rank"],
        "cube_size": len(positive) + len(negative),
        "learned_symmetry_clauses": len(clauses),
    }


def audit_catalogue(
    path: Path,
) -> tuple[list[tuple[tuple[int, int], ...]], dict[str, object]]:
    rows = [
        row
        for row in path.read_text(encoding="ascii").splitlines()
        if row
    ]
    if len(rows) != 950 or len(set(rows)) != len(rows):
        raise AssertionError("graph6 row count or uniqueness changed")
    edge_counts: Counter[int] = Counter()
    exact_degree_four = 0
    exact_matching_covered = 0
    for row in rows:
        edges = set(decode_graph6(row))
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(8)
        ]
        if (
            not connected(edges)
            or min(degrees) < 3
            or not 12 <= len(edges) <= 16
        ):
            raise AssertionError("graph6 catalogue violates its scope")
        edge_counts[len(edges)] += 1
        if len(edges) == 16 and 4 in degrees:
            exact_degree_four += 1
            if matching_covered(edges):
                exact_matching_covered += 1
    if edge_counts != Counter({12: 5, 13: 35, 14: 136, 15: 309, 16: 465}):
        raise AssertionError("graph6 edge-count distribution changed")
    if (exact_degree_four, exact_matching_covered) != (440, 364):
        raise AssertionError("exact-16 graph filter counts changed")

    roles, catalogue = canonical_role_skeletons(path)
    ordered = sorted(roles)
    if catalogue != {
        "unlabeled_matching_covered_graphs": 364,
        "canonical_role_skeletons": SELECTORS,
    }:
        raise AssertionError("canonical role catalogue changed")
    allowed = set(local_allowed_edges())
    for skeleton in ordered:
        edges = set(skeleton)
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(8)
        ]
        if (
            len(edges) != 16
            or not edges <= allowed
            or set(
                other
                for edge in edges
                if 0 in edge
                for other in edge
                if other != 0
            )
            != {1, 2, 3, 4}
            or degrees[0] != 4
            or min(degrees) < 3
            or not connected(edges)
            or not matching_covered(edges)
        ):
            raise AssertionError("bad canonical skeleton role")
    return ordered, {
        "graph6_rows": len(rows),
        "edge_count_distribution": dict(sorted(edge_counts.items())),
        "exact_16_with_degree_four": exact_degree_four,
        "unlabeled_matching_covered_graphs": exact_matching_covered,
        "canonical_role_skeletons": len(ordered),
    }


def audit_selector_compilation(
    cegar_cnf: Path,
    selector_cnf: Path,
    roles: list[tuple[tuple[int, int], ...]],
) -> None:
    old_variables, old_clauses = dimacs_header(cegar_cnf)
    new_variables, new_clauses = dimacs_header(selector_cnf)
    if (old_variables, old_clauses) != (
        BASE_VARIABLES,
        CEGAR_CLAUSES,
    ):
        raise AssertionError("CEGAR CNF dimensions changed")
    if (new_variables, new_clauses) != (
        SELECTOR_VARIABLES,
        SELECTOR_CLAUSES,
    ):
        raise AssertionError("selector CNF dimensions changed")

    selectors = [
        old_variables + 1 + index for index in range(len(roles))
    ]
    allowed = local_allowed_edges()
    first_block_variable = 1 + 9 * len(allowed)
    with cegar_cnf.open(
        "r", encoding="ascii"
    ) as base, selector_cnf.open("r", encoding="ascii") as combined:
        next(base)
        next(combined)
        for index, base_line in enumerate(base, start=1):
            if combined.readline() != base_line:
                raise AssertionError(
                    f"selector CNF base prefix changed at clause {index}"
                )
        expected_selector_line = " ".join(map(str, selectors)) + " 0\n"
        if combined.readline() != expected_selector_line:
            raise AssertionError("selector disjunction changed")
        for selector, skeleton in zip(selectors, roles, strict=True):
            present = set(skeleton)
            for edge_index, edge in enumerate(allowed):
                block = first_block_variable + edge_index
                literal = block if edge in present else -block
                expected = f"-{selector} {literal} 0\n"
                if combined.readline() != expected:
                    raise AssertionError(
                        "selector-to-skeleton implication changed"
                    )
        if combined.readline():
            raise AssertionError("unexpected clauses after selector tail")


def main() -> None:
    base = Path(".").resolve()
    paths: dict[str, Path] = {}
    hashes: dict[str, str] = {}
    for label, (relative, expected_hash) in EXPECTED.items():
        path = base / relative
        observed = sha256(path)
        if observed != expected_hash:
            raise AssertionError(
                f"{label} hash mismatch: {observed} != {expected_hash}"
            )
        paths[label] = path
        hashes[label] = observed

    if dimacs_header(paths["base_cnf"]) != (
        BASE_VARIABLES,
        BASE_CLAUSES,
    ):
        raise AssertionError("base max-16 CNF dimensions changed")
    if paths["proof"].stat().st_size != PROOF_BYTES:
        raise AssertionError("proof size changed")

    laurent = audit_laurent_replay(paths)
    roles, catalogue = audit_catalogue(paths["graph6"])
    audit_selector_compilation(
        paths["cegar_cnf"], paths["selector_cnf"], roles
    )

    selector_manifest = json.loads(
        paths["selector_manifest"].read_text(encoding="utf-8")
    )
    if (
        selector_manifest.get("selectors"),
        selector_manifest.get("selector_implications"),
        selector_manifest.get("variables"),
        selector_manifest.get("clauses"),
    ) != (
        SELECTORS,
        SELECTOR_IMPLICATIONS,
        SELECTOR_VARIABLES,
        SELECTOR_CLAUSES,
    ):
        raise AssertionError("selector manifest dimensions changed")
    if paths["minisat_model"].read_text(
        encoding="ascii"
    ).strip() != "UNSAT":
        raise AssertionError("MiniSat result file is not UNSAT")
    if "UNSATISFIABLE" not in paths["minisat_log"].read_text(
        encoding="utf-8"
    ):
        raise AssertionError("MiniSat terminal line missing")
    if "s UNSATISFIABLE" not in paths["cadical_log"].read_text(
        encoding="utf-8"
    ):
        raise AssertionError("CaDiCaL terminal line missing")
    drat_log = paths["drat_log"].read_text(encoding="utf-8")
    if (
        "s VERIFIED" not in drat_log
        or EXPECTED_RESOLUTION_STEPS not in drat_log
    ):
        raise AssertionError("independent DRAT verification missing")

    result = {
        "verified": True,
        "claim": (
            "no n=8 three-colour complex witness with an essential "
            "degree-four vertex and exactly 16 skeleton edges"
        ),
        "laurent_replay": laurent,
        "catalogue": catalogue,
        "variables": SELECTOR_VARIABLES,
        "clauses": SELECTOR_CLAUSES,
        "proof_bytes": PROOF_BYTES,
        "resolution_steps": int(EXPECTED_RESOLUTION_STEPS.split()[0]),
        "hashes": hashes,
    }
    output = base / "tmp/eight_vertex_16edge_audit.json"
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}: verified=True")


if __name__ == "__main__":
    main()
