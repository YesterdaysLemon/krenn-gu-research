#!/usr/bin/env python3
"""Exact perfect-pairing certificates for the 52 non-four gate covers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p6_common_port_111_rank_five_catalecticant import (
    SPLIT_MINORS,
    canonical_factor,
    minimal_hitting_sets,
)
from verify_p6_common_port_111_unique_four_gate_obstruction import (
    catalecticant_basis,
    symbolic_catalecticant,
)

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md"
UNIQUE_FOUR_COVER = (0, 3, 5, 9)

# Unless a cover occurs here, every gate receives coefficient +1.  For the
# three exceptional covers, the listed gate alone receives coefficient -1.
SIGN_FLIPS = {
    (2, 3, 6, 7, 10, 12, 15): 6,
    (1, 4, 8, 9, 11, 12, 15): 1,
    (1, 2, 4, 6, 8, 10, 13, 15): 2,
}

# Determinants of the certified linear combinations of the canonical gate
# matrices.  This table is deliberately explicit: replay checks discovery did
# not silently choose a new witness.
EXPECTED_DETERMINANTS = {
    (0, 1, 4, 5, 9): 3,
    (0, 3, 5, 7, 10): 13,
    (0, 1, 4, 5, 7, 10): -54,
    (2, 3, 5, 7, 12): 3,
    (1, 2, 4, 5, 7, 12): -102,
    (1, 2, 5, 7, 8, 12): -30,
    (1, 5, 8, 9, 12): 1,
    (2, 3, 5, 8, 9, 12): 16,
    (1, 5, 7, 8, 10, 12): -102,
    (2, 3, 5, 8, 9, 13): 8,
    (1, 2, 4, 5, 8, 9, 13): 2,
    (2, 3, 5, 7, 8, 10, 13): 30,
    (1, 2, 4, 5, 7, 8, 10, 13): 32,
    (0, 3, 6, 9, 11, 14): 4,
    (0, 1, 4, 6, 9, 11, 14): 9,
    (0, 3, 6, 7, 10, 11, 14): 79,
    (0, 1, 4, 6, 7, 10, 11, 14): -8,
    (2, 3, 6, 7, 11, 12, 14): -45,
    (1, 2, 4, 6, 7, 11, 12, 14): -80,
    (1, 2, 6, 7, 8, 11, 12, 14): 40,
    (1, 6, 8, 9, 11, 12, 14): 115,
    (2, 3, 6, 8, 9, 11, 12, 14): -68,
    (1, 6, 7, 8, 10, 11, 12, 14): 48,
    (2, 3, 6, 8, 9, 11, 13, 14): -32,
    (1, 2, 4, 6, 8, 9, 11, 13, 14): 60,
    (2, 3, 6, 7, 8, 10, 11, 13, 14): 156,
    (1, 2, 4, 6, 7, 8, 10, 11, 13, 14): 108,
    (0, 3, 6, 10, 15): 1,
    (0, 1, 4, 6, 10, 15): -5,
    (0, 4, 9, 11, 15): 3,
    (0, 3, 6, 9, 11, 15): 16,
    (0, 4, 6, 10, 11, 15): 36,
    (0, 4, 7, 10, 11, 15): 9,
    (2, 3, 6, 7, 10, 12, 15): 72,
    (1, 2, 4, 6, 7, 10, 12, 15): -95,
    (1, 6, 8, 10, 12, 15): 1,
    (2, 3, 6, 8, 10, 12, 15): -25,
    (2, 4, 7, 11, 12, 15): -3,
    (2, 3, 6, 7, 11, 12, 15): -107,
    (1, 2, 6, 7, 8, 11, 12, 15): -72,
    (1, 4, 8, 9, 11, 12, 15): -8,
    (2, 4, 8, 9, 11, 12, 15): 33,
    (1, 6, 8, 9, 11, 12, 15): -25,
    (2, 3, 6, 8, 9, 11, 12, 15): -192,
    (2, 4, 6, 8, 10, 11, 12, 15): 84,
    (1, 4, 7, 8, 10, 11, 12, 15): -77,
    (2, 3, 6, 8, 10, 13, 15): -1,
    (1, 2, 4, 6, 8, 10, 13, 15): 16,
    (2, 4, 8, 9, 11, 13, 15): 5,
    (2, 3, 6, 8, 9, 11, 13, 15): -24,
    (2, 4, 6, 8, 10, 11, 13, 15): 24,
    (2, 4, 7, 8, 10, 11, 13, 15): 96,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rebuild_gates_and_covers() -> tuple[list[sp.Matrix], list[tuple[int, ...]]]:
    symbolic, b_variables, c_variables = symbolic_catalecticant(catalecticant_basis())
    variables = b_variables + c_variables
    factors: list[sp.Poly] = []
    hyperedges: list[tuple[int, ...]] = []

    for rows, columns in SPLIT_MINORS:
        determinant = sp.expand(symbolic.extract(rows, columns).det())
        _constant, raw_factors = sp.factor_list(determinant, *variables)
        assert len(raw_factors) == 3
        factor_ids = []
        for factor, exponent in raw_factors:
            assert exponent == 1
            normalized = canonical_factor(factor, variables)
            if normalized not in factors:
                factors.append(normalized)
            factor_ids.append(factors.index(normalized))
        hyperedges.append(tuple(sorted(factor_ids)))

    assert len(factors) == 16
    assert len(set(hyperedges)) == 22
    gates = [
        sp.Matrix(
            5,
            5,
            lambda row, column, current=factor: current.coeff_monomial(
                b_variables[row] * c_variables[column]
            ),
        )
        for factor in factors
    ]
    assert all(gate == gate.T and gate.rank() == 2 for gate in gates)

    cover_masks = minimal_hitting_sets(sorted(set(hyperedges)), len(factors))
    covers = [
        tuple(index for index in range(len(factors)) if mask & (1 << index))
        for mask in cover_masks
    ]
    return gates, covers


def witness_coefficients(cover: tuple[int, ...]) -> list[int]:
    flipped_gate = SIGN_FLIPS.get(cover)
    return [-1 if gate == flipped_gate else 1 for gate in cover]


def main() -> None:
    gates, covers = rebuild_gates_and_covers()
    assert len(covers) == 53
    assert [cover for cover in covers if len(cover) == 4] == [UNIQUE_FOUR_COVER]

    nonfour_covers = [cover for cover in covers if cover != UNIQUE_FOUR_COVER]
    assert len(nonfour_covers) == 52
    assert set(nonfour_covers) == set(EXPECTED_DETERMINANTS)
    assert set(SIGN_FLIPS) <= set(nonfour_covers)

    certificates = []
    plain_sum_singular = []
    for cover in nonfour_covers:
        plain_sum = sum((gates[gate] for gate in cover), sp.zeros(5, 5))
        if plain_sum.det() == 0:
            plain_sum_singular.append(cover)

        coefficients = witness_coefficients(cover)
        witness = sum(
            (
                coefficient * gates[gate]
                for gate, coefficient in zip(cover, coefficients, strict=True)
            ),
            sp.zeros(5, 5),
        )
        determinant = sp.factor(witness.det())
        assert determinant == EXPECTED_DETERMINANTS[cover]
        assert determinant != 0
        assert witness.rank() == 5
        certificates.append(
            {
                "cover": list(cover),
                "coefficients": coefficients,
                "determinant": int(determinant),
            }
        )

    assert plain_sum_singular == list(SIGN_FLIPS)

    # If a perfect pairing vanishes on B x C with dim C=3, then B lies in the
    # two-dimensional annihilator of its three-dimensional image.  It cannot
    # itself have dimension three.
    ambient_dimension = 5
    plane_dimension = 3
    annihilator_dimension = ambient_dimension - plane_dimension
    assert annihilator_dimension == 2 < plane_dimension

    output = {
        "status": "verified",
        "field": "Q (the theorem is over C)",
        "minimal_cover_count": len(covers),
        "unique_four_cover": list(UNIQUE_FOUR_COVER),
        "nonfour_cover_count": len(nonfour_covers),
        "plain_sum_certificate_count": len(nonfour_covers) - len(SIGN_FLIPS),
        "one_sign_flip_certificate_count": len(SIGN_FLIPS),
        "perfect_pairing_certificates": certificates,
        "all_nonfour_covers_excluded": True,
        "all_covers_excluded_when_combined_with_unique_four_theorem": True,
        "displayed_rank_five_shared_factor_extension_excluded": True,
        "all_rank_five_configurations_classified": False,
        "p6_to_delta3_decided": False,
        "global_conjecture_resolved": False,
        "coefficient_search_used_in_replay": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
    }
    output_path = ROOT / "tmp" / "p6_common_port_111_all_gate_covers_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
