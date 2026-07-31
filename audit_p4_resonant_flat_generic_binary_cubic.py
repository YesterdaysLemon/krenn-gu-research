#!/usr/bin/env python3
"""Independent linear-system and compound audit of the flat chart."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def main() -> None:
    L, T, U = sp.symbols("L T U")

    # Solve the synchronization equations directly in coefficient form.
    # Unknown order is (a,b,c,d,e,f,g,h).
    sync = sp.Matrix(
        (
            (-1, 0, 0, 0, 0, 1, 0, 0),
            (-1, 0, 0, 0, 1, 0, 1, 0),
            (-L, 0, 0, 0, 1, 0, 0, 1),
            (1, -1, -1, 0, 0, 0, 0, 0),
            (1, -L, 0, -1, 0, 0, 0, 0),
            (0, 0, -L, -1, 0, 0, 1, 1),
        )
    )
    pencil_basis = sp.Matrix(
        (
            (1, 0),
            (0, 1),
            (1, -1),
            (1, -L),
            (0, L),
            (1, 0),
            (1, -L),
            (L, -L),
        )
    )
    assert sync.rank() == 6
    assert sync * pencil_basis == sp.zeros(6, 2)
    assert pencil_basis.rank() == 2

    C = 2 * sp.Matrix(
        (
            (
                -(L * T * U + T * U - T - U),
                -(L * T * U - 1),
                -(L * T + L * U - L - 1),
                L * (L * T * U - L * T - L * U - T - U + 3),
            ),
            (
                L * T * U - L * T - L * U - T - U + 3,
                -(L * T + L * U - L - 1),
                -L * (L * T * U - 1),
                -L**2 * (L * T * U + T * U - T - U),
            ),
            (
                -(L * T * U - T - U),
                1,
                L,
                -L**2 * (T * U - T - U),
            ),
            (
                -(T * U - T - U),
                1,
                1,
                -L * (L * T * U - T - U),
            ),
        )
    )

    F = sp.Poly(
        L**2 * T**2 * U**2
        - L * T**2
        - 4 * L * T * U
        + 2 * L * T
        - L * U**2
        + 2 * L * U
        + 2 * T
        + 2 * U
        - 3,
        L,
        T,
        U,
    )

    # This 2-minor makes the compressed span exactly two off L=1.
    kj_minor = sp.Poly(C.extract((2, 3), (1, 2)).det(), L, T, U)
    assert kj_minor == sp.Poly(-4 * (L - 1), L, T, U)

    row_triples = tuple(itertools.combinations(range(4), 3))
    column_triples = tuple(itertools.combinations(range(4), 3))
    remainders = []
    quotients = []
    for rows in row_triples:
        for columns in column_triples:
            minor = sp.Poly(C.extract(rows, columns).det(), L, T, U)
            quotient, remainder = sp.div(minor, F)
            quotients.append(quotient)
            remainders.append(remainder)
    assert all(remainder.is_zero for remainder in remainders)

    # The compression minor has nonzero quotient 8(L-1).
    compression_index = row_triples.index((1, 2, 3)) * 4
    compression_quotient = quotients[compression_index]
    assert compression_quotient == sp.Poly(8 * (L - 1), L, T, U)

    # There are nonzero quotient cofactors on both ends of the matrix,
    # so the common factor is not an artefact of a zero row or column.
    assert quotients[0] == sp.Poly(
        -8 * (L * T - 1) * (L * U - 1), L, T, U
    )
    assert quotients[12] == sp.Poly(8 * (L - 1), L, T, U)

    # Audit the omitted projective sheet directly, without taking a
    # limit of the affine matrix.
    C_inf = 2 * sp.Matrix(
        (
            (
                -(L * U + U - 1),
                -L * U,
                -L,
                L * (L * U - L - 1),
            ),
            (
                L * U - L - 1,
                -L,
                -L**2 * U,
                -L**2 * (L * U + U - 1),
            ),
            (-(L * U - 1), 0, 0, -L**2 * (U - 1)),
            (-(U - 1), 0, 0, -L * (L * U - 1)),
        )
    )
    inf_compression = [
        sp.factor(C_inf.extract(rows, (0, 1, 2)).det())
        for rows in row_triples
    ]
    G = sp.Poly(L * U**2 - 1, L, U)
    assert sp.expand(
        inf_compression[0] + 8 * L**2 * (L * U - 1) * G.as_expr()
    ) == 0
    assert sp.expand(
        inf_compression[1] + 8 * L**2 * (U - 1) * G.as_expr()
    ) == 0
    inf_remainders = []
    for rows in row_triples:
        for columns in column_triples:
            minor = sp.Poly(C_inf.extract(rows, columns).det(), L, U)
            _, remainder = sp.div(minor, G)
            inf_remainders.append(remainder)
    assert all(remainder.is_zero for remainder in inf_remainders)
    surviving_two_minor = sp.factor(C_inf.extract((0, 2), (0, 1)).det())
    assert sp.expand(surviving_two_minor + 4 * L * U * (L * U - 1)) == 0

    C_double_inf = 2 * sp.Matrix(
        (
            (-L - 1, -L, 0, L**2),
            (L, 0, -L**2, -L**3 - L**2),
            (-L, 0, 0, -L**2),
            (-1, 0, 0, -L**2),
        )
    )
    double_minor = sp.factor(
        C_double_inf.extract((0, 1, 2), (0, 1, 2)).det()
    )
    assert sp.expand(double_minor + 8 * L**4) == 0

    result = {
        "synchronization_matrix_rank": sync.rank(),
        "pencil_basis_rank": pencil_basis.rank(),
        "independent_KJ_minor": str(kj_minor.as_expr()),
        "compound_entries_divisible_by_F": len(remainders),
        "compression_quotient": str(compression_quotient.as_expr()),
        "infinite_sheet_compound_entries": len(inf_remainders),
        "double_infinite_minor": str(double_minor),
        "proof_boundary": "only zero or repeated projective columns remain",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
