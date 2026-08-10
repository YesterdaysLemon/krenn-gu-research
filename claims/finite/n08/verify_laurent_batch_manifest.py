"""Independently audit Laurent support conflicts learned by a batch run.

The batch learner records a cube of entries forced nonzero/zero and the
amplitude equations used for each contradiction.  This verifier checks that
the cube really specializes every used equation to the advertised torus,
reruns the exact integer Laurent reduction, reconstructs every symmetry
clause, and checks that the learned CNF is exactly the base CNF plus those
clauses.
"""

from __future__ import annotations

import argparse
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

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.cancellation_transport import (
    cube_cancellation_transport_certificates,
    cube_two_monomial_rectangle_certificates,
)
from krenn_gu.eight_vertex_degree4_cegar import (
    full_equations,
    symmetry_clauses,
)
from krenn_gu.eight_vertex_sparse_exact import local_allowed_edges
from krenn_gu.odd_binomial_cycle import (
    cube_odd_binomial_triangle_certificates,
)
from krenn_gu.prism_laurent_reduction import primitive_binomial_reduction
from krenn_gu.search_witness import EquationSystem
from krenn_gu.signed_binomial_lattice import (
    cube_verify_signed_binomial_lattice_certificate,
)

Polynomial = Counter[tuple[str, ...]]


def dimacs_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError(f"{path} is not DIMACS CNF")
    return int(variables), int(clauses)


def structural_zero_indices(
    system: EquationSystem,
    center_degree: int = 4,
) -> set[int]:
    allowed = set(local_allowed_edges(center_degree))
    return {
        9 * system.edge_index[edge] + 3 * row + column
        for edge in system.edges
        if edge not in allowed
        for row in range(3)
        for column in range(3)
    }


def restrict_used_equations(
    equations: list[Polynomial],
    names: dict[int, str],
    name_to_flat: dict[str, int],
    structural_zero: set[int],
    positive: set[int],
    negative: set[int],
    used: list[int],
) -> list[Polynomial]:
    restricted: list[Polynomial] = []
    for equation_index in used:
        output: Polynomial = Counter()
        for monomial, coefficient in equations[equation_index].items():
            factors = [name_to_flat[variable] for variable in monomial]
            if any(
                factor in structural_zero or factor in negative
                for factor in factors
            ):
                continue
            unspecified = [
                factor for factor in factors if factor not in positive
            ]
            if unspecified:
                raise AssertionError(
                    "learned cube leaves a surviving monomial unspecified: "
                    f"equation={equation_index}, factors={unspecified}"
                )
            output[monomial] += coefficient
        output = Counter(
            {
                monomial: coefficient
                for monomial, coefficient in output.items()
                if coefficient
            }
        )
        if not output:
            raise AssertionError(
                f"used equation {equation_index} restricts to zero"
            )
        restricted.append(output)
    return restricted


def audit_conflict(
    system: EquationSystem,
    equations: list[Polynomial],
    names: dict[int, str],
    name_to_flat: dict[str, int],
    structural_zero: set[int],
    conflict: dict[str, object],
    center_degree: int = 4,
) -> list[tuple[int, ...]]:
    positive = set(map(int, conflict["positive_entries"]))
    negative = set(map(int, conflict["negative_entries"]))
    if positive & negative:
        raise AssertionError("conflict cube has contradictory entry signs")
    if len(positive) + len(negative) != int(conflict["cube_size"]):
        raise AssertionError("conflict cube size is inconsistent")
    if (positive | negative) & structural_zero:
        raise AssertionError("conflict unnecessarily fixes structural zeros")
    if any(
        index < 0 or index >= system.variable_count
        for index in positive | negative
    ):
        raise AssertionError("conflict contains an invalid flat index")

    used = list(map(int, conflict["used_equation_indices"]))
    if used != sorted(set(used)):
        raise AssertionError("used equation indices are not canonical")
    expected_colourings = [
        [int(value) for value in system.colourings[index]]
        for index in used
    ]
    if conflict["used_colourings"] != expected_colourings:
        raise AssertionError("used colouring labels do not match equations")

    if conflict.get("certificate_kind") == "cancellation_transport":
        certificates = cube_cancellation_transport_certificates(
            system,
            used,
            positive,
            negative | structural_zero,
        )
        if conflict.get("transport_certificate") not in certificates:
            raise AssertionError(
                "recorded cancellation-transport certificate did not replay"
            )
    elif conflict.get("certificate_kind") == "two_monomial_rectangle":
        certificates = cube_two_monomial_rectangle_certificates(
            system,
            used,
            positive,
            negative | structural_zero,
        )
        if conflict.get("rectangle_certificate") not in certificates:
            raise AssertionError(
                "recorded two-monomial rectangle did not replay"
            )
    elif conflict.get("certificate_kind") == "odd_binomial_triangle":
        certificates = cube_odd_binomial_triangle_certificates(
            system,
            used,
            positive,
            negative | structural_zero,
        )
        if conflict.get("odd_triangle_certificate") not in certificates:
            raise AssertionError(
                "recorded odd-binomial triangle did not replay"
            )
    elif conflict.get("certificate_kind") == "signed_binomial_lattice":
        cube_verify_signed_binomial_lattice_certificate(
            system,
            used,
            positive,
            negative | structural_zero,
            conflict["signed_lattice_certificate"],
        )
    else:
        restricted = restrict_used_equations(
            equations,
            names,
            name_to_flat,
            structural_zero,
            positive,
            negative,
            used,
        )
        active_names = [names[index] for index in sorted(positive)]
        _, _, metadata = primitive_binomial_reduction(
            restricted, active_names
        )
        if not metadata["unit_equation_indices"] and not metadata[
            "linear_monomial_unit_relations"
        ]:
            raise AssertionError(
                "recorded support cube has no exact Laurent-unit contradiction"
            )
    return symmetry_clauses(
        system,
        positive,
        negative,
        center_degree=center_degree,
    )


def audit_cnf(
    base: Path,
    learned: Path,
    clauses: list[tuple[int, ...]],
) -> None:
    base_variables, base_clauses = dimacs_header(base)
    learned_variables, learned_clauses = dimacs_header(learned)
    if learned_variables != base_variables:
        raise AssertionError("learned CNF changed the variable count")
    if learned_clauses != base_clauses + len(clauses):
        raise AssertionError("learned CNF clause count is inconsistent")

    with base.open(
        "r", encoding="ascii"
    ) as source, learned.open("r", encoding="ascii") as augmented:
        next(source)
        next(augmented)
        for clause_index, source_line in enumerate(source, start=1):
            if augmented.readline() != source_line:
                raise AssertionError(
                    "learned CNF changed its base prefix at clause "
                    f"{clause_index}"
                )
        for clause in clauses:
            expected = " ".join(map(str, clause)) + " 0\n"
            if augmented.readline() != expected:
                raise AssertionError("learned CNF clause tail changed")
        if augmented.readline():
            raise AssertionError("learned CNF has an unexpected tail")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path)
    parser.add_argument("--learned-cnf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    center_degree = int(manifest.get("center_degree", 4))
    system = EquationSystem(8, 3)
    equations, names, name_to_flat = full_equations(system)
    structural_zero = structural_zero_indices(
        system, center_degree
    )

    clause_union: set[tuple[int, ...]] = set()
    raw_conflicts = manifest.get("conflicts", [])
    if isinstance(raw_conflicts, int):
        # A transfer manifest intentionally stores only the source manifests
        # and the reconstructed clause union.  Replay every source rather
        # than trusting the transfer generator.
        conflict_count = 0
        sources = list(manifest.get("source_manifests", []))
        if not sources:
            raise AssertionError(
                "combined manifest has no source manifests"
            )
        for source in sources:
            source_path = Path(str(source["path"]))
            if source["sha256"] != hashlib.sha256(
                source_path.read_bytes()
            ).hexdigest():
                raise AssertionError(
                    f"source manifest hash mismatch: {source_path}"
                )
            source_manifest = json.loads(
                source_path.read_text(encoding="utf-8")
            )
            if (
                int(source_manifest.get("center_degree", 4))
                != center_degree
            ):
                raise AssertionError(
                    f"source center degree changed: {source_path}"
                )
            source_raw = source_manifest.get("conflicts", [])
            if isinstance(source_raw, int):
                raise AssertionError(
                    "nested combined Laurent manifests are unsupported"
                )
            source_conflicts = list(source_raw)
            if (
                not source_conflicts
                and "used_equation_indices" in source_manifest
            ):
                source_conflicts = [
                    {**source_manifest, "conflict_index": 0}
                ]
            source_clauses: set[tuple[int, ...]] = set()
            for expected_index, conflict in enumerate(
                source_conflicts
            ):
                if int(conflict["conflict_index"]) != expected_index:
                    raise AssertionError(
                        f"source conflicts are not contiguous: "
                        f"{source_path}"
                    )
                source_clauses.update(
                    audit_conflict(
                        system,
                        equations,
                        names,
                        name_to_flat,
                        structural_zero,
                        conflict,
                        center_degree=center_degree,
                    )
                )
            if (
                int(source["conflicts"]) != len(source_conflicts)
                or int(source["clauses"]) != len(source_clauses)
            ):
                raise AssertionError(
                    f"source transfer counts changed: {source_path}"
                )
            source_recorded = source_manifest.get(
                "learned_clauses"
            )
            if isinstance(source_recorded, list) and {
                tuple(map(int, clause))
                for clause in source_recorded
            } != source_clauses:
                raise AssertionError(
                    f"source clause union changed: {source_path}"
                )
            conflict_count += len(source_conflicts)
            clause_union.update(source_clauses)
        if int(raw_conflicts) != conflict_count:
            raise AssertionError(
                "combined manifest conflict count changed"
            )
    else:
        conflicts = list(raw_conflicts)
        if not conflicts and "used_equation_indices" in manifest:
            conflicts = [{**manifest, "conflict_index": 0}]
        for expected_index, conflict in enumerate(conflicts):
            if int(conflict["conflict_index"]) != expected_index:
                raise AssertionError(
                    "conflict indices are not contiguous"
                )
            clause_union.update(
                audit_conflict(
                    system,
                    equations,
                    names,
                    name_to_flat,
                    structural_zero,
                    conflict,
                    center_degree=center_degree,
                )
            )
        conflict_count = len(conflicts)
    ordered_clauses = sorted(clause_union)
    recorded = [
        tuple(map(int, clause))
        for clause in manifest.get("learned_clauses", [])
    ]
    if recorded != ordered_clauses:
        raise AssertionError(
            "manifest learned clauses do not equal the conflict images"
        )
    if int(
        manifest.get("laurent_conflicts", conflict_count)
    ) != conflict_count:
        raise AssertionError("manifest conflict count is inconsistent")

    base = args.base_cnf
    learned = args.learned_cnf
    if base is None and manifest.get("base_cnf"):
        base = Path(str(manifest["base_cnf"]))
    if learned is None and manifest.get("learned_cnf"):
        learned = Path(str(manifest["learned_cnf"]))
    if learned is None and manifest.get("output_cnf"):
        learned = Path(str(manifest["output_cnf"]))
    if (base is None) != (learned is None):
        raise AssertionError("provide both base and learned CNFs")
    if base is not None and learned is not None:
        audit_cnf(base, learned, ordered_clauses)

    payload = {
        "verified": True,
        "conflicts": conflict_count,
        "learned_clauses": len(ordered_clauses),
        "cnf_checked": base is not None,
        "center_degree": center_degree,
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
