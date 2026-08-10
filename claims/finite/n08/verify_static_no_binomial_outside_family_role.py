"""Independently audit a static no-binomial CNF outside a finite family."""

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
import itertools
import json
from pathlib import Path

from enumerate_double_c4_singleton_family import selected_entries
from enumerate_five_regular_double_c4_singleton_family import (
    enumerate_patterns,
)
from krenn_gu.search_witness import EquationSystem

Edge = tuple[int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int, bytes]:
    with path.open("rb") as handle:
        line = handle.readline()
    fields = line.split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise AssertionError(f"{path} is not a DIMACS CNF")
    return int(fields[2]), int(fields[3]), line


def labelled_family_supports(
    family: dict[str, object],
    system: EquationSystem,
) -> set[frozenset[int]]:
    supports: set[frozenset[int]] = set()
    subtotal = 0
    for row in family["types"]:
        skeleton = frozenset(
            tuple(map(int, edge)) for edge in row["skeleton_edges"]
        )
        edges = sorted(skeleton)
        factors, unlabelled = enumerate_patterns(system, skeleton)
        if len(factors) != int(row["double_c4_factors"]):
            raise AssertionError("double-C4 factor count changed")
        if len(unlabelled) != int(
            row["colour_unlabelled_factorizations"]
        ):
            raise AssertionError("one-factorization count changed")
        labelled: set[tuple[int, ...]] = set()
        for pattern in unlabelled:
            for permutation in itertools.permutations(range(system.d)):
                labelled.add(
                    tuple(
                        system.d
                        if label == system.d
                        else permutation[label]
                        for label in pattern
                    )
                )
        if len(labelled) != int(row["labelled_supports"]):
            raise AssertionError("labelled family count changed")
        subtotal += len(labelled)
        supports.update(
            frozenset(selected_entries(system, edges, pattern))
            for pattern in labelled
        )
    if subtotal != int(family["labelled_supports"]):
        raise AssertionError("aggregate labelled count changed")
    if len(supports) != subtotal:
        raise AssertionError("family types produced duplicate supports")
    return supports


def expected_tail(
    system: EquationSystem,
    skeleton: set[Edge],
    supports: set[frozenset[int]],
) -> bytes:
    graph_first = system.variable_count + 1
    rows = [
        (
            f"{graph_first + edge_index} 0\n"
            if edge in skeleton
            else f"-{graph_first + edge_index} 0\n"
        ).encode("ascii")
        for edge_index, edge in enumerate(system.edges)
    ]
    for selected in sorted(supports, key=lambda value: sorted(value)):
        clause = [
            -(flat + 1) if flat in selected else flat + 1
            for flat in range(system.variable_count)
        ]
        rows.append(
            (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        )
    return b"".join(rows)


def compare_prefix_and_tail(
    base_cnf: Path,
    output_cnf: Path,
    expected: bytes,
) -> None:
    with base_cnf.open("rb") as base, output_cnf.open("rb") as output:
        base.readline()
        output.readline()
        while True:
            base_chunk = base.read(8 * 1024 * 1024)
            if not base_chunk:
                break
            if output.read(len(base_chunk)) != base_chunk:
                raise AssertionError("output changed a base-CNF body byte")
        if output.read() != expected:
            raise AssertionError("output extension differs from reconstruction")


def complement_cycle_lengths(skeleton: set[Edge]) -> tuple[int, ...]:
    complete = set(itertools.combinations(range(8), 2))
    complement = complete - skeleton
    if any(
        sum(vertex in edge for edge in complement) != 2
        for vertex in range(8)
    ):
        raise AssertionError("pinned skeleton complement is not 2-regular")
    unseen = set(range(8))
    lengths: list[int] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component: set[int] = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(
                other
                for edge in complement
                if vertex in edge
                for other in edge
                if other != vertex and other not in component
            )
        unseen -= component
        lengths.append(len(component))
    return tuple(sorted(lengths))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    base_manifest_path = Path(manifest["base_manifest"])
    family_manifest_path = Path(manifest["family_manifest"])
    base_cnf = Path(manifest["base_cnf"])
    output_cnf = Path(manifest["output_cnf"])
    base_manifest = json.loads(
        base_manifest_path.read_text(encoding="utf-8")
    )
    family = json.loads(
        family_manifest_path.read_text(encoding="utf-8")
    )

    if sha256(base_manifest_path) != manifest["base_manifest_sha256"]:
        raise AssertionError("base manifest hash changed")
    if sha256(family_manifest_path) != manifest["family_manifest_sha256"]:
        raise AssertionError("family manifest hash changed")
    observed_base_hash = sha256(base_cnf)
    if observed_base_hash != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash changed")
    if observed_base_hash != base_manifest["output_cnf_sha256"]:
        raise AssertionError("base manifest does not bind the base CNF")
    observed_output_hash = sha256(output_cnf)
    if observed_output_hash != manifest["output_cnf_sha256"]:
        raise AssertionError("output CNF hash changed")

    variables, old_clauses, _ = header(base_cnf)
    new_variables, new_clauses, _ = header(output_cnf)
    if variables != new_variables:
        raise AssertionError("extension changed the variable count")
    if (variables, old_clauses) != (
        int(manifest["variables"]),
        int(manifest["old_clauses"]),
    ):
        raise AssertionError("base header differs from manifest")

    system = EquationSystem(8, 3)
    if system.variable_count != 252:
        raise AssertionError("unexpected support-variable layout")
    skeleton = {
        tuple(map(int, edge)) for edge in manifest["skeleton_edges"]
    }
    expected_cycle_type = {
        "c8": (8,),
        "c5_c3": (3, 5),
        "c4_c4": (4, 4),
    }[manifest["skeleton_type"]]
    if complement_cycle_lengths(skeleton) != expected_cycle_type:
        raise AssertionError("pinned skeleton has the wrong isomorphism type")
    family_row = next(
        row
        for row in family["types"]
        if row["skeleton_type"] == manifest["skeleton_type"]
    )
    if skeleton != {
        tuple(map(int, edge)) for edge in family_row["skeleton_edges"]
    }:
        raise AssertionError("pinned skeleton differs from family catalogue")

    supports = labelled_family_supports(family, system)
    tail = expected_tail(system, skeleton, supports)
    expected_extension_clauses = len(system.edges) + len(supports)
    if expected_extension_clauses != (
        int(manifest["role_unit_clauses"])
        + int(manifest["support_blocking_clauses"])
    ):
        raise AssertionError("extension clause count changed")
    if new_clauses != old_clauses + expected_extension_clauses:
        raise AssertionError("output header has the wrong clause count")
    compare_prefix_and_tail(base_cnf, output_cnf, tail)

    payload = {
        "verified": True,
        "scope": manifest["scope"],
        "necessary_conditions_only": bool(
            manifest["necessary_conditions_only"]
        ),
        "stronger_than_prize_hypothesis": bool(
            manifest["stronger_than_prize_hypothesis"]
        ),
        "skeleton_type": manifest["skeleton_type"],
        "complement_cycle_lengths": list(expected_cycle_type),
        "variables": new_variables,
        "clauses": new_clauses,
        "role_unit_clauses": len(system.edges),
        "blocked_supports": len(supports),
        "blocked_support_sizes": sorted({len(row) for row in supports}),
        "base_cnf_sha256": observed_base_hash,
        "output_cnf_sha256": observed_output_hash,
        "output_cnf_prefix_and_tail_reconstructed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
