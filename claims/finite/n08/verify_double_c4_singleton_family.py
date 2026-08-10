"""Independently verify the certified double-C4 singleton family.

The producer enumerates a finite macro-family on a fixed 20-edge skeleton.
This verifier deliberately reconstructs that family by a different route:

* choose every 8-edge spanning subgraph and retain precisely the two-C4
  2-factors;
* recursively enumerate perfect matchings of each cubic complement;
* enumerate its one-factorizations;
* quotient the resulting supports by all skeleton automorphisms and all
  global colour permutations;
* check the emitted model/support/activity data; and
* bind every orbit to a separately verified factor-lattice/DRAT audit.

The resulting claim concerns this macro-family only.  It does not assert
that every support satisfying the original Krenn-Gu hypotheses has this
form.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from search_witness import EquationSystem

Edge = tuple[int, int]
Matching = frozenset[Edge]
Pattern = tuple[int, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_path(raw: str, expected_hash: str) -> Path:
    path = Path(raw)
    if not path.is_file():
        raise AssertionError(f"missing artifact: {path}")
    actual = sha256(path)
    if actual != expected_hash:
        raise AssertionError(
            f"hash mismatch for {path}: {actual} != {expected_hash}"
        )
    return path


def component_sizes(edges: frozenset[Edge], n: int) -> list[int]:
    adjacency = [set() for _ in range(n)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    unseen = set(range(n))
    sizes: list[int] = []
    while unseen:
        root = min(unseen)
        stack = [root]
        unseen.remove(root)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return sorted(sizes)


def double_c4_factors(
    skeleton: frozenset[Edge],
    n: int,
) -> list[frozenset[Edge]]:
    """Find the factors by edge subsets, not by enumerating 4-cycles."""
    output: list[frozenset[Edge]] = []
    for candidate_tuple in itertools.combinations(sorted(skeleton), n):
        candidate = frozenset(candidate_tuple)
        degrees = Counter(
            vertex for edge in candidate for vertex in edge
        )
        if all(degrees[vertex] == 2 for vertex in range(n)):
            if component_sizes(candidate, n) == [4, 4]:
                output.append(candidate)
    return sorted(output, key=lambda value: sorted(value))


def perfect_matchings(edges: frozenset[Edge], n: int) -> list[Matching]:
    adjacency = [set() for _ in range(n)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)

    def visit(unmatched: frozenset[int]) -> list[Matching]:
        if not unmatched:
            return [frozenset()]
        first = min(unmatched)
        output: list[Matching] = []
        for second in sorted(adjacency[first] & unmatched):
            remainder = unmatched - {first, second}
            edge = (min(first, second), max(first, second))
            for tail in visit(remainder):
                output.append(tail | {edge})
        return output

    return sorted(
        set(visit(frozenset(range(n)))),
        key=lambda matching: sorted(matching),
    )


def one_factorizations(
    complement: frozenset[Edge],
    n: int,
) -> list[tuple[Matching, Matching, Matching]]:
    matchings = perfect_matchings(complement, n)
    output: set[tuple[Matching, Matching, Matching]] = set()
    for triple in itertools.combinations(matchings, 3):
        if frozenset().union(*triple) == complement:
            output.add(tuple(sorted(triple, key=lambda value: sorted(value))))
    return sorted(
        output,
        key=lambda triple: [
            sorted(matching) for matching in triple
        ],
    )


def skeleton_automorphisms(
    skeleton: frozenset[Edge],
    n: int,
) -> list[tuple[int, ...]]:
    output: list[tuple[int, ...]] = []
    for permutation in itertools.permutations(range(n)):
        image = frozenset(
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in skeleton
        )
        if image == skeleton:
            output.append(tuple(permutation))
    return output


def transform(
    pattern: Pattern,
    edges: list[Edge],
    positions: dict[Edge, int],
    vertex_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> Pattern:
    result = [-1] * len(pattern)
    for edge, label in zip(edges, pattern, strict=True):
        image = tuple(
            sorted(
                (
                    vertex_permutation[edge[0]],
                    vertex_permutation[edge[1]],
                )
            )
        )
        result[positions[image]] = (
            3 if label == 3 else colour_permutation[label]
        )
    if any(label < 0 for label in result):
        raise AssertionError("automorphism failed to map a skeleton edge")
    return tuple(result)


def canonical(
    pattern: Pattern,
    edges: list[Edge],
    automorphisms: list[tuple[int, ...]],
) -> Pattern:
    positions = {edge: index for index, edge in enumerate(edges)}
    return min(
        transform(
            pattern,
            edges,
            positions,
            automorphism,
            colour_permutation,
        )
        for automorphism in automorphisms
        for colour_permutation in itertools.permutations(range(3))
    )


def selected_entries(pattern: Pattern, edges: list[Edge]) -> set[int]:
    complete_edges = list(itertools.combinations(range(8), 2))
    positions = {edge: index for index, edge in enumerate(complete_edges)}
    selected: set[int] = set()
    for edge, label in zip(edges, pattern, strict=True):
        base = 9 * positions[edge]
        if label == 3:
            selected.update(range(base, base + 9))
        else:
            selected.add(base + 4 * label)
    return selected


def parse_model(path: Path, variable_count: int) -> set[int]:
    tokens = path.read_text(encoding="ascii").split()
    literals: list[int] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in {"s", "SATISFIABLE", "v"}:
            index += 1
            continue
        literal = int(token)
        if literal:
            literals.append(literal)
        index += 1
    if sorted(abs(literal) for literal in literals) != list(
        range(1, variable_count + 1)
    ):
        raise AssertionError(f"{path} is not a total entry assignment")
    return {literal - 1 for literal in literals if literal > 0}


def activity_summary(
    system: EquationSystem,
    selected: set[int],
) -> tuple[dict[str, int], list[int]]:
    mask = np.zeros(system.variable_count, dtype=bool)
    mask[list(selected)] = True
    activity = np.all(mask[system.variable_ids], axis=2)
    counts = np.sum(activity, axis=0)
    forbidden = Counter(
        int(counts[equation])
        for equation, target in enumerate(system.target)
        if not bool(target)
    )
    required = [
        int(counts[equation])
        for equation, target in enumerate(system.target)
        if bool(target)
    ]
    return (
        {str(key): value for key, value in sorted(forbidden.items())},
        required,
    )


def check_factor_audit(
    audit_path: Path,
    orbit: dict[str, object],
) -> dict[str, object]:
    orbit_identifier = orbit.get(
        "orbit_index",
        orbit.get("global_orbit_index"),
    )
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("verified") is not True:
        raise AssertionError(f"unverified factor audit: {audit_path}")
    if audit.get("selected_entries") != 84:
        raise AssertionError(f"unexpected selected-entry count: {audit_path}")

    artifact_pairs = (
        ("manifest", "manifest_sha256"),
        ("source_model", "source_model_sha256"),
        ("final_cnf", "final_cnf_sha256"),
        ("drat", "drat_sha256"),
        ("cadical_log", "cadical_log_sha256"),
        ("drat_trim_log", "drat_trim_log_sha256"),
    )
    artifacts = {
        name: checked_path(str(audit[name]), str(audit[hash_name]))
        for name, hash_name in artifact_pairs
    }
    if audit["source_model_sha256"] != orbit["model_sha256"]:
        raise AssertionError(
            f"audit/model mismatch for orbit {orbit_identifier}"
        )

    manifest = json.loads(
        artifacts["manifest"].read_text(encoding="utf-8")
    )
    required_manifest_values = {
        "status": "UNSAT",
        "necessary_conditions_only": False,
        "include_direct_binomials": not bool(
            orbit.get("binomial_free", True)
        ),
        "model_sha256": orbit["model_sha256"],
        "selected_entries": 84,
        "selected_flat_indices": orbit["selected_flat_indices"],
        "final_cnf_sha256": audit["final_cnf_sha256"],
        "factor_relation_count": audit["factor_relations"],
        "factor_clause_count": audit["factor_clauses"],
    }
    for key, expected in required_manifest_values.items():
        if manifest.get(key) != expected:
            raise AssertionError(
                f"{audit_path}: manifest field {key!r} disagrees"
            )
    if len(manifest.get("branches", [])) != audit["learned_clauses"]:
        raise AssertionError(
            f"{audit_path}: manifest branch count disagrees"
        )
    if sha256(artifacts["source_model"]) != manifest["model_sha256"]:
        raise AssertionError("factor manifest source-model hash mismatch")
    if sha256(artifacts["final_cnf"]) != manifest["final_cnf_sha256"]:
        raise AssertionError("factor manifest final-CNF hash mismatch")

    cadical_text = artifacts["cadical_log"].read_text(
        encoding="utf-8",
        errors="replace",
    )
    drat_text = artifacts["drat_trim_log"].read_text(
        encoding="utf-8",
        errors="replace",
    )
    if "s UNSATISFIABLE" not in cadical_text:
        raise AssertionError(f"missing CaDiCaL UNSAT marker: {audit_path}")
    if "s VERIFIED" not in drat_text:
        raise AssertionError(f"missing DRAT verification marker: {audit_path}")

    return {
        "orbit_index": orbit_identifier,
        "audit": str(audit_path),
        "audit_sha256": sha256(audit_path),
        "factor_relations": audit["factor_relations"],
        "factor_clauses": audit["factor_clauses"],
        "lattice_branches": audit["learned_clauses"],
        "final_cnf_sha256": audit["final_cnf_sha256"],
        "drat_sha256": audit["drat_sha256"],
        "drat_trim_log_sha256": audit["drat_trim_log_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family-manifest", type=Path, required=True)
    parser.add_argument(
        "--factor-audit",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    family = json.loads(
        args.family_manifest.read_text(encoding="utf-8")
    )
    if family.get("verified") is not True:
        raise AssertionError("family producer did not mark its output verified")
    source_path = checked_path(
        str(family["source_manifest"]),
        str(family["source_manifest_sha256"]),
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    role_index = int(family["role_index"])
    source_edges = sorted(
        tuple(map(int, edge))
        for edge in source["rows"][role_index]["skeleton_edges"]
    )
    manifest_edges = sorted(
        tuple(map(int, edge)) for edge in family["skeleton_edges"]
    )
    if source_edges != manifest_edges:
        raise AssertionError("source and family skeletons disagree")
    if source.get("target_edges") != 20 or len(manifest_edges) != 20:
        raise AssertionError("family is not attached to an exact-20 skeleton")

    n = 8
    skeleton = frozenset(manifest_edges)
    degrees = Counter(vertex for edge in skeleton for vertex in edge)
    if any(degrees[vertex] != 5 for vertex in range(n)):
        raise AssertionError("the fixed skeleton is not 5-regular")

    factors = double_c4_factors(skeleton, n)
    patterns: set[Pattern] = set()
    edges = sorted(skeleton)
    for factor in factors:
        complement = skeleton - factor
        complement_degrees = Counter(
            vertex for edge in complement for vertex in edge
        )
        if any(complement_degrees[vertex] != 3 for vertex in range(n)):
            raise AssertionError("factor complement is not cubic")
        for factorization in one_factorizations(complement, n):
            labels = {edge: 3 for edge in factor}
            for colour, matching in enumerate(factorization):
                for edge in matching:
                    labels[edge] = colour
            patterns.add(tuple(labels[edge] for edge in edges))

    automorphisms = skeleton_automorphisms(skeleton, n)
    orbits: dict[Pattern, list[Pattern]] = defaultdict(list)
    for pattern in patterns:
        orbits[canonical(pattern, edges, automorphisms)].append(pattern)
    reconstructed = sorted(orbits.items())

    expected_counts = {
        "double_c4_factors": len(factors),
        "skeleton_automorphisms": len(automorphisms),
        "colour_unlabelled_factorizations": len(patterns),
        "labelled_supports": 6 * len(patterns),
        "support_orbits": len(reconstructed),
    }
    for key, expected in expected_counts.items():
        if family.get(key) != expected:
            raise AssertionError(
                f"family count {key!r}: {family.get(key)} != {expected}"
            )
    if expected_counts != {
        "double_c4_factors": 34,
        "skeleton_automorphisms": 128,
        "colour_unlabelled_factorizations": 108,
        "labelled_supports": 648,
        "support_orbits": 10,
    }:
        raise AssertionError(f"unexpected reconstructed counts: {expected_counts}")

    system = EquationSystem(8, 3)
    if system.variable_count != 252:
        raise AssertionError("unexpected n=8,d=3 variable count")
    rows = family["orbits"]
    if len(rows) != len(reconstructed):
        raise AssertionError("family orbit-row count mismatch")
    for orbit_index, ((pattern, members), row) in enumerate(
        zip(reconstructed, rows, strict=True)
    ):
        if row["orbit_index"] != orbit_index:
            raise AssertionError("nonconsecutive family orbit indices")
        if tuple(row["canonical_edge_labels"]) != pattern:
            raise AssertionError(f"canonical pattern mismatch at orbit {orbit_index}")
        if row["orbit_size"] != len(members):
            raise AssertionError(f"orbit-size mismatch at orbit {orbit_index}")
        selected = selected_entries(pattern, edges)
        if len(selected) != 84:
            raise AssertionError(f"orbit {orbit_index} is not an 84-entry support")
        if row["selected_entries"] != 84:
            raise AssertionError(f"manifest count mismatch at orbit {orbit_index}")
        if row["selected_flat_indices"] != sorted(selected):
            raise AssertionError(f"selected support mismatch at orbit {orbit_index}")
        model_path = checked_path(str(row["model"]), str(row["model_sha256"]))
        if parse_model(model_path, system.variable_count) != selected:
            raise AssertionError(f"model mismatch at orbit {orbit_index}")
        forbidden, required = activity_summary(system, selected)
        if forbidden != row["forbidden_activity_histogram"]:
            raise AssertionError(f"activity histogram mismatch at orbit {orbit_index}")
        if required != row["required_activity_counts"]:
            raise AssertionError(f"required activity mismatch at orbit {orbit_index}")
        if "1" in forbidden or "2" in forbidden:
            raise AssertionError(f"orbit {orbit_index} is not binomial-free")

    audit_by_model_hash: dict[str, Path] = {}
    for audit_path in args.factor_audit:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        model_hash = str(audit["source_model_sha256"])
        if model_hash in audit_by_model_hash:
            raise AssertionError(f"duplicate audit for model {model_hash}")
        audit_by_model_hash[model_hash] = audit_path
    expected_model_hashes = {str(row["model_sha256"]) for row in rows}
    if set(audit_by_model_hash) != expected_model_hashes:
        missing = expected_model_hashes - set(audit_by_model_hash)
        extra = set(audit_by_model_hash) - expected_model_hashes
        raise AssertionError(f"audit coverage mismatch: missing={missing}, extra={extra}")

    audit_rows = [
        check_factor_audit(
            audit_by_model_hash[str(row["model_sha256"])],
            row,
        )
        for row in rows
    ]
    payload = {
        "verified": True,
        "scope": (
            "all 648 labelled double-C4/full-block plus three-matching "
            "singleton supports (108 up to global colour permutation) "
            "on the fixed exact-20-edge 5-regular skeleton"
        ),
        "claim_scope": (
            "proves this finite macro-family impossible only; does not "
            "prove every support has this form and is not the global "
            "Krenn-Gu conjecture"
        ),
        "family_manifest": str(args.family_manifest),
        "family_manifest_sha256": sha256(args.family_manifest),
        "source_manifest": str(source_path),
        "source_manifest_sha256": sha256(source_path),
        **expected_counts,
        "selected_entries_per_support": 84,
        "binomial_free_labelled_supports": 6 * len(patterns),
        "certified_impossible_labelled_supports": 6 * len(patterns),
        "orbit_audits": audit_rows,
        "total_factor_relations": sum(
            int(row["factor_relations"]) for row in audit_rows
        ),
        "total_factor_clauses": sum(
            int(row["factor_clauses"]) for row in audit_rows
        ),
        "total_lattice_branches": sum(
            int(row["lattice_branches"]) for row in audit_rows
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
