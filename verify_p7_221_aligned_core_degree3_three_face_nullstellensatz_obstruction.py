"""Verify the three-face degree-three obstruction for the aligned core word.

The exact six-parameter degree-five family is substituted first.  All 35
degree-three faces are constructed, but a three-face unit-ideal certificate
proves inconsistency without a Groebner basis or any parameter search.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

import verify_p7_221_aligned_core_degree5_affine_completion as aligned


def permanent_evaluator(matrix: sp.Matrix):
    @cache
    def permanent(rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Expr:
        if not rows:
            return sp.Integer(1)
        first = rows[0]
        return sp.expand(
            sum(
                matrix[first, column]
                * permanent(rows[1:], columns[:position] + columns[position + 1 :])
                for position, column in enumerate(columns)
            )
        )

    return permanent


def four_core_hafnian(vertices: tuple[int, int, int, int], edges) -> sp.Expr:
    first, second, third, fourth = vertices

    def edge(left: int, right: int) -> sp.Expr:
        return edges[min(left, right), max(left, right)]

    return sp.expand(
        edge(first, second) * edge(third, fourth)
        + edge(first, third) * edge(second, fourth)
        + edge(first, fourth) * edge(second, third)
    )


def degree_three_response(face: str, incidence, edges, permanent) -> sp.Expr:
    columns = tuple(aligned.P.index(terminal) for terminal in face)
    total = sp.Integer(0)
    for used_rows in combinations(range(7), 3):
        remaining = tuple(index for index in range(7) if index not in used_rows)
        total += permanent(used_rows, columns) * four_core_hafnian(remaining, edges)
    return sp.expand(total)


def main() -> None:
    incidence = aligned.incidence_matrix()
    raw_edges, variables = aligned.core_edges()
    degree_five_family = aligned.degree_five_parametrization(variables)
    edges = {
        pair: sp.expand(sp.sympify(value).subs(degree_five_family))
        for pair, value in raw_edges.items()
    }
    free_parameters = (
        variables[2, 4],
        variables[2, 5],
        variables[2, 6],
        variables[3, 4],
        variables[3, 5],
        variables[3, 6],
    )
    permanent = permanent_evaluator(incidence)
    faces = tuple("".join(face) for face in combinations(aligned.P, 3))
    assert len(faces) == 35
    responses = {
        face: degree_three_response(face, incidence, edges, permanent) for face in faces
    }
    response_polynomials = {
        face: sp.Poly(response, free_parameters, extension=aligned.RHO)
        for face, response in responses.items()
    }
    assert all(polynomial.total_degree() <= 2 for polynomial in response_polynomials.values())
    assert sum(not polynomial.is_zero for polynomial in response_polynomials.values()) == 24

    # Monic normalization only divides by a nonzero field scalar, so it does
    # not change the zero set over Q(rho) or any field extension.
    normalized = {
        face: response_polynomials[face].monic().as_expr() for face in ("124", "125", "12a")
    }
    p = variables[3, 4]
    q = variables[3, 5]
    rho = aligned.RHO
    alpha = 5 + 2 * rho / 21
    capital_c = 230 + 104 * rho / 7
    delta = 6 + rho / 21
    kappa = sp.simplify(delta * alpha / capital_c)

    assert sp.simplify(normalized["124"] - (q - delta)) == 0
    assert normalized["125"] == p
    assert sp.simplify(normalized["12a"] - q * (p - kappa)) == 0

    certificate = sp.expand(
        q * normalized["125"] - normalized["12a"] - kappa * normalized["124"]
    )
    assert sp.simplify(certificate - delta * kappa) == 0
    unit_certificate = sp.simplify(capital_c * certificate / (delta**2 * alpha))
    assert unit_certificate == 1

    # Each denominator and the certificate constant is nonzero in Q(rho).
    assert sp.simplify((6 + rho / 21) * (6 - rho / 21) - sp.Rational(755, 21)) == 0
    assert sp.simplify((5 + 2 * rho / 21) * (5 - 2 * rho / 21) - sp.Rational(521, 21)) == 0
    assert 805**2 - 21 * 52**2 == 591241

    deletion_faces = {
        face: "".join(terminal for terminal in aligned.P if terminal not in face)
        for face in normalized
    }
    assert deletion_faces == {"124": "35ab", "125": "34ab", "12a": "345b"}

    print("aligned-core degree-three obstruction: VERIFIED")
    print("degree3_faces_constructed=35 nonzero=24 quadratic_or_lower=35")
    print("three_face_subsystem=124,125,12a")
    print("normalized=(q-delta),p,q*(p-delta*alpha/C)")
    print("Nullstellensatz_unit_certificate=1")
    print("solutions_over_Qsqrt21=NONE solutions_over_algebraic_closure=NONE")
    print("parameter_search=0 groebner_basis=not_needed")
    print("scope=single_alignment_single_mixed_word")


if __name__ == "__main__":
    main()
