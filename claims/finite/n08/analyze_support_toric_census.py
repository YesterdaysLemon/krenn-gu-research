"""Build exact toric-degeneration/balanced certificates for SAT supports."""

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
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from eight_vertex_skeleton_laurent_batch import (
    local_positive_to_flat,
)
from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from krenn_gu.search_witness import EquationSystem
from support_toric_degeneration import (
    entry_endpoints,
    primitive_integer_vector,
    supported_exponents,
    verify_balanced_certificate,
    verify_degeneration_certificate,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def incidence_matrix(
    system: EquationSystem,
    selected: list[int],
) -> np.ndarray:
    matrix = np.zeros((len(selected), system.n * system.d))
    for row, flat_index in enumerate(selected):
        first, second = entry_endpoints(system, flat_index)
        matrix[row, first[0] * system.d + first[1]] += 1
        matrix[row, second[0] * system.d + second[1]] += 1
    return matrix


def colour_sum_matrix(system: EquationSystem) -> np.ndarray:
    matrix = np.zeros((system.d, system.n * system.d))
    for colour in range(system.d):
        for vertex in range(system.n):
            matrix[colour, vertex * system.d + colour] = 1
    return matrix


def discover_certificate(
    system: EquationSystem,
    selected: list[int],
) -> dict[str, object]:
    incidence = incidence_matrix(system, selected)
    colour_sums = colour_sum_matrix(system)
    coordinate_count = system.n * system.d

    # Feasibility normalization: all supported exponents are nonnegative,
    # and their sum is at least one.
    inequalities = np.vstack(
        [-incidence, -incidence.sum(axis=0)[None, :]]
    )
    bounds = np.r_[np.zeros(len(selected)), -1.0]
    degeneration = linprog(
        np.zeros(coordinate_count),
        A_ub=inequalities,
        b_ub=bounds,
        A_eq=colour_sums,
        b_eq=np.zeros(system.d),
        bounds=[(None, None)] * coordinate_count,
        method="highs",
    )
    if degeneration.success:
        potential_vector = primitive_integer_vector(degeneration.x)
        potentials = [
            potential_vector[
                vertex * system.d : (vertex + 1) * system.d
            ]
            for vertex in range(system.n)
        ]
        exponents = supported_exponents(
            system, selected, potentials
        )
        certificate: dict[str, object] = {
            "mode": "support_degeneration",
            "potentials": potentials,
            "deleted_entries": sorted(
                flat_index
                for flat_index, exponent in exponents.items()
                if exponent > 0
            ),
        }
        verify_degeneration_certificate(
            system, selected, certificate
        )
        return certificate

    # Exact alternative: positive lifted-edge weights with colour-constant
    # weighted degrees.  The lower bound one removes homogeneous scaling.
    edge_count = len(selected)
    equalities = np.c_[incidence.T, -colour_sums.T]
    balanced = linprog(
        np.r_[np.ones(edge_count), np.zeros(system.d)],
        A_eq=equalities,
        b_eq=np.zeros(coordinate_count),
        bounds=[
            *([(1.0, None)] * edge_count),
            *([(None, None)] * system.d),
        ],
        method="highs",
    )
    if not balanced.success:
        raise RuntimeError(
            "neither side of the toric alternative was discovered: "
            f"{degeneration.message}; {balanced.message}"
        )
    integers = primitive_integer_vector(balanced.x)
    weights = integers[:edge_count]
    degrees = integers[edge_count:]
    if min(weights) <= 0:
        # Primitive normalization could only flip a homogeneous solution
        # if the numerical solver returned the opposite sign.
        weights = [-value for value in weights]
        degrees = [-value for value in degrees]
    # A required monochromatic perfect matching is supported in each
    # colour.  Adding its incidence vector raises only that colour's common
    # degree, so all colour degrees can be made equal without losing strict
    # positivity.  This exhibits a strictly positive fractional perfect
    # matching on the full lifted support graph.
    common_degree = max(degrees)
    positions = {
        flat_index: index
        for index, flat_index in enumerate(selected)
    }
    for colour, degree in enumerate(degrees):
        increment = common_degree - degree
        if not increment:
            continue
        for matching in system.matchings:
            diagonal_entries = [
                system.edge_index[edge] * system.d**2
                + colour * system.d
                + colour
                for edge in matching
            ]
            if all(entry in positions for entry in diagonal_entries):
                for entry in diagonal_entries:
                    weights[positions[entry]] += increment
                break
        else:
            raise AssertionError(
                f"no supported monochromatic matching in colour {colour}"
            )
    degrees = [common_degree] * system.d
    certificate = {
        "mode": "balanced_support",
        "entry_weights": weights,
        "colour_degrees": degrees,
        "uniform_lifted_degree": common_degree,
    }
    verify_balanced_certificate(system, selected, certificate)
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "tmp/eight_vertex_signed_lattice_combined_census.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_support_toric_census.json"
        ),
    )
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    system = EquationSystem(8, 3)
    rows: list[dict[str, object]] = []
    modes: Counter[str] = Counter()
    deleted_histogram: Counter[int] = Counter()
    seen_hashes: set[str] = set()

    for raw in source["models"]:
        log = Path(raw["log"])
        log_hash = sha256(log)
        if log_hash != raw["log_sha256"]:
            raise AssertionError(f"source log hash changed: {log}")
        if log_hash in seen_hashes:
            raise AssertionError(f"duplicate source log: {log}")
        seen_hashes.add(log_hash)
        selected = sorted(
            local_positive_to_flat(
                system,
                sorted(positive_model_literals(log)),
                center_degree=1,
            )
        )
        if len(selected) != int(raw["selected_entries"]):
            raise AssertionError(f"selected-entry count changed: {log}")
        certificate = discover_certificate(system, selected)
        mode = str(certificate["mode"])
        modes[mode] += 1
        if mode == "support_degeneration":
            deleted_histogram[
                len(certificate["deleted_entries"])  # type: ignore[arg-type]
            ] += 1
        rows.append(
            {
                "log": str(log),
                "log_sha256": log_hash,
                "selected_entries": len(selected),
                "certificate": certificate,
            }
        )

    payload = {
        "verified": True,
        "scope": (
            "finite exact support-toric census of completed dense n=8 "
            "SAT models"
        ),
        "claim_scope": (
            "certifies each listed support; the general reduction is "
            "the Gordan-Stiemke alternative, not a prize proof"
        ),
        "source_manifest": str(args.input),
        "source_manifest_sha256": sha256(args.input),
        "support_models": len(rows),
        "degenerable_supports": modes["support_degeneration"],
        "balanced_supports": modes["balanced_support"],
        "deleted_entry_histogram": {
            str(key): value
            for key, value in sorted(deleted_histogram.items())
        },
        "models": rows,
    }
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key != "models"
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
