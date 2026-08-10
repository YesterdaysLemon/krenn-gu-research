"""Measure elementary transport/rectangle coverage of six-vertex Laurent cubes.

The older six-vertex proof manifests store support literals by polynomial
variable name.  This audit reconstructs their original edge-entry indices and
asks whether each exact Laurent no-good already contains one of the newer
combinatorial contradictions:

* one-vertex cancellation transport; or
* a two-monomial four-corner rectangle.

Absence of either certificate is not a criticism of the Laurent certificate:
it only says that the newer elementary detector does not subsume that cube.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from cancellation_transport import (
    cube_cancellation_transport_certificates,
    cube_two_monomial_rectangle_certificates,
    decided_cube_activity,
)
from killer_union_stratum import normalized_union_stratum, union_orbit_equations
from odd_binomial_cycle import cube_odd_binomial_triangle_certificates
from prism_laurent_reduction import primitive_binomial_reduction
from prism_orbit_screen import clean_polynomial
from search_killer_patterns import active_mask_for_pattern
from search_witness import EquationSystem
from signed_binomial_lattice import (
    signed_binomial_lattice_certificates,
    verify_signed_binomial_lattice_certificate,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_entry_statuses(
    system: EquationSystem,
    pattern: list[list[int]],
    normalized: bool,
) -> tuple[dict[str, int], set[int], set[int]]:
    """Return name-to-flat, fixed-nonzero, and structural-zero entries."""
    _names, _equations, variable_names = union_orbit_equations(
        system,
        pattern,
        normalize_mutual=normalized,
    )
    name_to_flat = {name: int(flat) for flat, name in variable_names.items()}
    if normalized:
        fixed, active = normalized_union_stratum(system, pattern)
        fixed_nonzero = {
            int(index) for index in np.flatnonzero(np.abs(fixed) > 0)
        }
    else:
        active = active_mask_for_pattern(system, pattern)
        fixed_nonzero = set()
    possible = {
        int(index) for index in np.flatnonzero(active)
    } | fixed_nonzero
    structural_zero = set(range(system.variable_count)) - possible
    return name_to_flat, fixed_nonzero, structural_zero


def analyze(manifest: Path) -> dict[str, Any]:
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    system = EquationSystem(6, 3)
    all_equations = list(range(len(system.colourings)))
    rows: list[dict[str, Any]] = []
    aggregate = Counter()

    default_normalized = bool(payload.get("normalized", False))
    for row in payload["rows"]:
        pattern = [
            [int(neighbour) for neighbour in neighbours]
            for neighbours in row["pattern"]
        ]
        normalized = bool(row.get("normalized", default_normalized))
        name_to_flat, fixed_nonzero, structural_zero = row_entry_statuses(
            system,
            pattern,
            normalized,
        )
        names, equations, _variable_names = union_orbit_equations(
            system,
            pattern,
            normalize_mutual=normalized,
        )
        row_counts = Counter()
        certificate_rows: list[dict[str, Any]] = []
        for certificate_index, certificate in enumerate(row["certificates"]):
            positive = fixed_nonzero | {
                name_to_flat[str(name)]
                for name in certificate["positive_cube"]
            }
            zero = structural_zero | {
                name_to_flat[str(name)]
                for name in certificate["negative_cube"]
            }
            retained, _colourings, _activities = decided_cube_activity(
                system,
                all_equations,
                positive,
                zero,
            )
            lattice = signed_binomial_lattice_certificates(
                system,
                retained,
                _activities,
                maximum_certificates=1,
            )
            if lattice:
                verify_signed_binomial_lattice_certificate(
                    system,
                    {
                        equation: activity
                        for equation, activity in zip(
                            retained,
                            _activities,
                            strict=True,
                        )
                    },
                    lattice[0],
                )
            transport = cube_cancellation_transport_certificates(
                system,
                all_equations,
                positive,
                zero,
            )
            rectangles = cube_two_monomial_rectangle_certificates(
                system,
                all_equations,
                positive,
                zero,
            )
            triangles = cube_odd_binomial_triangle_certificates(
                system,
                all_equations,
                positive,
                zero,
            )
            modes = Counter(
                str(item["certificate_mode"]) for item in rectangles
            )
            positive_names = {
                str(name) for name in certificate["positive_cube"]
            }
            negative_names = {
                str(name) for name in certificate["negative_cube"]
            }
            source_indices = [
                *[int(index) for index in certificate["basis_equations"]],
                int(certificate["unit_equation"]),
            ]
            restricted = []
            for source_index in source_indices:
                polynomial = clean_polynomial(
                    Counter(
                        {
                            monomial: coefficient
                            for monomial, coefficient in equations[
                                source_index
                            ].items()
                            if not any(
                                variable in negative_names
                                for variable in monomial
                            )
                        }
                    )
                )
                for monomial in polynomial:
                    if not set(monomial) <= positive_names:
                        raise AssertionError(
                            "Laurent cube leaves an unclassified variable"
                        )
                if polynomial:
                    restricted.append(polynomial)
            active_names = [
                name for name in names if name in positive_names
            ]
            _reduced_names, _reduced, metadata = (
                primitive_binomial_reduction(
                    restricted,
                    active_names,
                )
            )
            unit_indices = [
                int(index)
                for index in metadata["unit_equation_indices"]
            ]
            if not unit_indices:
                raise AssertionError(
                    "stored Laurent certificate has no replayed unit"
                )
            required_basis_sizes = [
                len(
                    metadata["unit_basis_equation_indices"].get(
                        str(index),
                        [],
                    )
                )
                for index in unit_indices
            ]
            chosen_unit_position = min(
                range(len(unit_indices)),
                key=lambda position: (
                    required_basis_sizes[position],
                    len(restricted[unit_indices[position]]),
                    unit_indices[position],
                ),
            )
            circuit_size = (
                1 + required_basis_sizes[chosen_unit_position]
            )
            unit_input_terms = len(
                restricted[unit_indices[chosen_unit_position]]
            )
            elementary = bool(transport or rectangles or triangles)
            row_counts["laurent_cubes"] += 1
            row_counts["decided_equations"] += len(retained)
            row_counts["transport_cubes"] += bool(transport)
            row_counts["rectangle_cubes"] += bool(rectangles)
            row_counts["odd_triangle_cubes"] += bool(triangles)
            row_counts["elementary_cubes"] += elementary
            row_counts["transport_certificates"] += len(transport)
            row_counts["rectangle_certificates"] += len(rectangles)
            row_counts["odd_triangle_certificates"] += len(triangles)
            row_counts["signed_lattice_cubes"] += bool(lattice)
            row_counts["toric_circuit_equations"] += circuit_size
            row_counts["toric_unit_input_terms"] += unit_input_terms
            for mode, count in modes.items():
                row_counts[f"rectangle_mode_{mode}"] += count
            certificate_rows.append(
                {
                    "certificate_index": certificate_index,
                    "positive_entries": len(positive),
                    "zero_entries": len(zero),
                    "decided_equations": len(retained),
                    "transport_certificates": len(transport),
                    "rectangle_certificates": len(rectangles),
                    "rectangle_modes": dict(sorted(modes.items())),
                    "odd_triangle_certificates": len(triangles),
                    "signed_lattice_certificate": (
                        None
                        if not lattice
                        else {
                            "mode": lattice[0]["certificate_mode"],
                            "basis_relations": len(
                                lattice[0]["basis_relations"]
                            ),
                        }
                    ),
                    "toric_circuit_equations": circuit_size,
                    "toric_unit_equations": len(unit_indices),
                    "toric_unit_input_terms": unit_input_terms,
                }
            )
        aggregate.update(row_counts)
        aggregate["exact_fallback_certificates"] += len(
            row.get("exact_certificates", [])
        )
        rows.append(
            {
                "orbit": int(row["orbit"]),
                "normalized": normalized,
                "status": str(row["status"]),
                "counts": dict(sorted(row_counts.items())),
                "certificates": certificate_rows,
                "exact_fallback_certificates": len(
                    row.get("exact_certificates", [])
                ),
            }
        )

    return {
        "verified": True,
        "claim_scope": (
            "finite detector-coverage audit; no new global theorem is claimed"
        ),
        "source_manifest": str(manifest),
        "source_sha256": sha256(manifest),
        "system": {"vertices": 6, "colours": 3},
        "counts": dict(sorted(aggregate.items())),
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.manifest)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["counts"], sort_keys=True))
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
