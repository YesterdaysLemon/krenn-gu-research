"""Pin one skeleton role and block a certified family in a static CNF."""

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
import itertools
import json
import shutil
from pathlib import Path

from augment_no_binomial_amplitudes import header, sha256
from enumerate_double_c4_singleton_family import (
    skeleton_automorphisms,
    transform_pattern,
)
from krenn_gu.search_witness import EquationSystem


def expanded_supports(
    family: dict[str, object],
    system: EquationSystem,
) -> set[frozenset[int]]:
    output: set[frozenset[int]] = set()
    family_types = family.get("types", [family])
    expanded = 0
    for family_type in family_types:
        edges = sorted(
            tuple(map(int, edge))
            for edge in family_type["skeleton_edges"]
        )
        positions = {edge: index for index, edge in enumerate(edges)}
        automorphisms = skeleton_automorphisms(
            system.n,
            frozenset(edges),
        )
        patterns: set[tuple[int, ...]] = set()
        for orbit in family_type["orbits"]:
            canonical = tuple(
                map(int, orbit["canonical_edge_labels"])
            )
            for automorphism in automorphisms:
                for colour_permutation in itertools.permutations(
                    range(system.d)
                ):
                    patterns.add(
                        transform_pattern(
                            canonical,
                            edges,
                            positions,
                            automorphism,
                            colour_permutation,
                        )
                    )
        if len(patterns) != int(family_type["labelled_supports"]):
            raise AssertionError("family type did not expand exactly")
        expanded += len(patterns)
        for pattern in patterns:
            selected: set[int] = set()
            for edge, label in zip(edges, pattern, strict=True):
                base = system.d**2 * system.edge_index[edge]
                if label == system.d:
                    selected.update(range(base, base + system.d**2))
                else:
                    selected.add(base + (system.d + 1) * label)
            output.add(frozenset(selected))
    if expanded != int(family["labelled_supports"]):
        raise AssertionError("aggregate family expansion count changed")
    if len(output) != expanded:
        raise AssertionError("expanded family contains duplicate supports")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-manifest", type=Path, required=True)
    parser.add_argument("--family-manifest", type=Path, required=True)
    parser.add_argument(
        "--skeleton-type",
        choices=("c8", "c5_c3", "c4_c4"),
        default="c4_c4",
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()

    base_manifest = json.loads(
        args.base_manifest.read_text(encoding="utf-8")
    )
    base_cnf = Path(base_manifest["output_cnf"])
    if sha256(base_cnf) != base_manifest["output_cnf_sha256"]:
        raise AssertionError("static no-binomial CNF changed")
    variables, old_clauses = header(base_cnf)

    family = json.loads(
        args.family_manifest.read_text(encoding="utf-8")
    )
    family_types = family.get("types", [family])
    skeleton_row = next(
        row
        for row in family_types
        if row.get("skeleton_type", "c4_c4") == args.skeleton_type
    )
    skeleton = {
        tuple(map(int, edge)) for edge in skeleton_row["skeleton_edges"]
    }
    system = EquationSystem(8, 3)
    if system.variable_count != 252:
        raise AssertionError("unexpected entry-variable layout")
    graph_first_variable = system.variable_count + 1
    role_units = [
        (
            graph_first_variable + edge_index
            if edge in skeleton
            else -(graph_first_variable + edge_index)
        )
        for edge_index, edge in enumerate(system.edges)
    ]

    supports = expanded_supports(family, system)
    support_blockers = [
        tuple(
            (
                -(flat + 1)
                if flat in selected
                else flat + 1
            )
            for flat in range(system.variable_count)
        )
        for selected in sorted(supports, key=lambda value: sorted(value))
    ]
    extension_clauses = len(role_units) + len(support_blockers)
    new_clauses = old_clauses + extension_clauses

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with base_cnf.open("rb") as reader, args.output_cnf.open(
        "wb"
    ) as writer:
        reader.readline()
        writer.write(f"p cnf {variables} {new_clauses}\n".encode("ascii"))
        shutil.copyfileobj(reader, writer, length=8 * 1024 * 1024)
        for literal in role_units:
            writer.write(f"{literal} 0\n".encode("ascii"))
        for clause in support_blockers:
            writer.write(
                (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            )
    if header(args.output_cnf) != (variables, new_clauses):
        raise AssertionError("materialized CNF header changed")

    payload = {
        "scope": (
            "static exact-role no-binomial support CNF outside the "
            "certified double-C4/singleton family"
        ),
        "necessary_conditions_only": True,
        "stronger_than_prize_hypothesis": True,
        "base_manifest": str(args.base_manifest),
        "base_manifest_sha256": sha256(args.base_manifest),
        "base_cnf": str(base_cnf),
        "base_cnf_sha256": sha256(base_cnf),
        "family_manifest": str(args.family_manifest),
        "family_manifest_sha256": sha256(args.family_manifest),
        "skeleton_type": args.skeleton_type,
        "skeleton_edges": [list(edge) for edge in sorted(skeleton)],
        "variables": variables,
        "old_clauses": old_clauses,
        "role_unit_clauses": len(role_units),
        "support_blocking_clauses": len(support_blockers),
        "new_clauses": new_clauses,
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
    }
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
