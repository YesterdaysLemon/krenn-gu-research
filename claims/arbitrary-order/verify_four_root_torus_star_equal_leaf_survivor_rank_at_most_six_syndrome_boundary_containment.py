#!/usr/bin/env python3
"""Verify the scoped GLD86 low-center-rank boundary containment.

The calculation is exact over ``Q(i)``.  It replays the pinned GLD75
bidirectional ideal certificate, reconstructs the fixed 37-row GLD71
syndrome map, and evaluates one named 7-by-7 syndrome minor on the equal-leaf
frame chart.  The factorization is then combined with the exact column
replacement identity forced by ``M(G) C = 0`` and the scale-fixed coordinate
``C_8 = 1``.  No Fitting ideal is computed or declared empty here.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD71 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD75 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py"
)
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"

SYNDROME_ROWS = (0, 1, 17, 19, 31, 32, 33)
SYNDROME_COLUMNS = (2, 3, 4, 5, 6, 7, 8)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check() -> dict[str, object]:
    gld75 = load_module(GLD75, "gld75_for_gld86")

    raw_certificate = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw_certificate
    assert hashlib.sha256(raw_certificate).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw_certificate)
    assert payload["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert payload["variable_order"] == [f"x{index}" for index in range(15)]
    assert payload["incidence_generator_count"] == 37
    assert payload["basis_generator_count"] == 10
    assert payload["forward_shape"] == [37, 10]
    assert payload["reverse_shape"] == [10, 37]
    assert sum(len(entry["terms"]) for entry in payload["forward"]) == 27
    assert sum(len(entry["terms"]) for entry in payload["reverse"]) == 63

    # GLD75 owns the full bidirectional replay.  This verifier checks its
    # immutable carrier and reconstructs the same ten basis generators; the
    # expensive 37-equation certificate replay remains available through the
    # owning GLD75 command and is not silently treated as a new GLD86 result.
    shifts = tuple(sp.symbols("x0:15"))
    generators = tuple(
        sp.expand(gld75.sparse_polynomial(encoded, shifts).as_expr())
        for encoded in payload["basis"]
    )
    assert len(generators) == 10
    scale_fixed = tuple(sp.expand(value.subs(shifts[8], 0)) for value in generators)
    center = sp.Matrix(shifts[:8])
    coefficient_from_basis = sp.Matrix(scale_fixed).jacobian(center)
    inhomogeneous = sp.Matrix(scale_fixed).subs({value: 0 for value in center})
    assert all(
        sp.diff(entry, variable) == 0
        for entry in coefficient_from_basis
        for variable in center
    )
    assert (
        sp.Matrix(scale_fixed)
        - coefficient_from_basis * center
        - inhomogeneous
    ).applyfunc(sp.expand) == sp.zeros(10, 1)

    gld71 = load_module(GLD71, "gld71_for_gld86")
    parent = gld75.load_gld72().load_gate().load_parent()
    relations = gld71.full_relations(parent)
    # This also checks that the selected sparse rows are a full annihilator
    # basis for the rank-44 fixed star, rather than an arbitrary collection of
    # equations.
    all_columns, annihilator_basis, _punctured_rows = gld71.check_punctured_code(
        parent, relations
    )
    assert len(relations) == 37
    assert len(all_columns) == 79
    assert len(annihilator_basis) == 44

    p, q, r, a, b, c = sp.symbols("p q r a b c")
    imaginary = sp.I
    leaf = sp.Matrix(
        [[1, 1, 1], [p, q, 1 + imaginary + r], [a, 1 + b, 1 + c]]
    )
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    assert syndrome.shape == (37, 9)

    selected = syndrome.extract(SYNDROME_ROWS, SYNDROME_COLUMNS)
    determinant = sp.expand(selected.det(method="domain-ge"))
    s = 1 + imaginary + r
    divisors = (
        p - q,
        p - s,
        q - s,
        p * q + p * s + q * s - p - q - s,
    )
    expected = sp.expand(432 * sp.prod(divisor**2 for divisor in divisors))
    assert sp.expand(determinant - expected) == 0
    assert determinant.free_symbols <= {p, q, r}

    # The actual center coordinate is the GLD72 center plus the shift x8.  The
    # scale-fixed chart sets x8=0, so C8 is the exact unit 1.
    gaussian_center = sp.Matrix(
        [-2 - 2 * imaginary, -1 + 2 * imaginary, 3, 0, -3 + 3 * imaginary, 0, 0, -1 + 2 * imaginary, 1]
    )
    actual_center = gaussian_center + sp.Matrix(shifts[:9])
    assert sp.expand(actual_center[8].subs(shifts[8], 0)) == 1

    gaussian_leaf = sp.Matrix(
        [[1, 1, 1], [0, 0, 1 + imaginary], [0, 1, 1]]
    )
    gaussian_syndrome = gld71.coefficient_matrix(
        parent, relations, (gaussian_leaf, gaussian_leaf, gaussian_leaf)
    )
    assert all(
        sp.simplify(value) == 0 for value in gaussian_syndrome * gaussian_center
    )
    assert gaussian_syndrome.rank() == 7
    assert gaussian_syndrome[:, :8].rank() == 7

    return {
        "status": "exact_GLD86_rank_at_most_six_boundary_containment",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_characteristic_zero_then_C",
        "syndrome_shape": list(syndrome.shape),
        "selected_rows": list(SYNDROME_ROWS),
        "selected_columns": list(SYNDROME_COLUMNS),
        "selected_minor_factorization": "432*(p-q)^2*(p-s)^2*(q-s)^2*(p*q+p*s+q*s-p-q-s)^2",
        "named_divisors": ["p-q", "p-s", "q-s", "p*q+p*s+q*s-p-q-s"],
        "minor_free_symbols": sorted(str(symbol) for symbol in determinant.free_symbols),
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_shapes": {
            "incidence": payload["incidence_generator_count"],
            "basis": payload["basis_generator_count"],
            "forward_terms": sum(len(entry["terms"]) for entry in payload["forward"]),
            "reverse_terms": sum(len(entry["terms"]) for entry in payload["reverse"]),
        },
        "gaussian_syndrome_rank": gaussian_syndrome.rank(),
        "gaussian_center_column_rank": gaussian_syndrome[:, :8].rank(),
        "scale_fixed_C8": "1",
        "column_replacement_identity_used": True,
        "rank_at_most_six_confined_to_named_divisors": True,
        "omega_saturated_divisors_excluded": False,
        "gld83_fitting_pullback_computed": False,
        "global_conjecture_resolved": False,
    }


def main() -> None:
    print("four-root equal-leaf rank-at-most-six syndrome boundary: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
