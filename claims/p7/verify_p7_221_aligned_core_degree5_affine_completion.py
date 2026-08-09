"""Verify the aligned-core 20x12 degree-five affine completion.

The alignment and mixed word are fixed in advance.  All twenty prescribed
degree-five faces are checked as one exact compound system; no alignment,
support, word, or graph search is performed.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

P = tuple("12345ab")
RHO = sp.sqrt(21)
COLOUR_TWO_POSITIONS = (0, 2, 3)
COLOUR_ZERO_POSITIONS = (1, 4, 5, 6)
CROSS_PAIRS = tuple(
    (left, right) for left in COLOUR_TWO_POSITIONS for right in COLOUR_ZERO_POSITIONS
)
FACES = tuple(
    "".join(face) for face in combinations(P, 5) if "".join(face) != "12345"
)


def incidence_matrix() -> sp.Matrix:
    alpha = 5 + 2 * RHO / 21
    beta = 1 + 16 * RHO / 21
    capital_c = 230 + 104 * RHO / 7
    matrix = sp.zeros(7)

    def put(row: int, terminal: str, value=1) -> None:
        matrix[row, P.index(terminal)] = value

    put(0, "5", sp.Rational(1, 7))  # z_* at f1
    put(1, "2")  # c0 f2
    put(2, "1")  # c2 z1 at ell
    put(2, "3")
    put(3, "2")  # c2 z2 at h3
    put(3, "4")
    put(4, "4")  # c0 h4
    put(4, "b", -alpha)
    put(5, "5")  # c0 h5
    put(5, "b", capital_c)
    put(6, "a")  # c0 ha
    put(6, "b", beta)
    return matrix


def core_edges():
    variables = {pair: sp.Symbol(f"x{pair[0]}{pair[1]}") for pair in CROSS_PAIRS}
    fixed = {
        (2, 3): sp.Integer(1),
        (4, 5): -6 - RHO / 21,
        (4, 6): RHO / 21,
        (5, 6): 1 + 22 * RHO / 21,
    }
    edges: dict[tuple[int, int], sp.Expr] = {}
    for left in range(7):
        for right in range(left + 1, 7):
            pair = (left, right)
            reversed_pair = (right, left)
            edges[pair] = variables.get(pair, variables.get(reversed_pair, fixed.get(pair, 0)))
    return edges, variables


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


def degree_five_response(face: str, edges, permanent) -> sp.Expr:
    columns = tuple(P.index(terminal) for terminal in face)
    total = sp.Integer(0)
    for left in range(7):
        for right in range(left + 1, 7):
            rows = tuple(index for index in range(7) if index not in (left, right))
            total += edges[left, right] * permanent(rows, columns)
    return sp.expand(total)


def degree_five_parametrization(variables):
    alpha = 5 + 2 * RHO / 21
    beta = 1 + 16 * RHO / 21
    capital_c = 230 + 104 * RHO / 7
    delta = 6 + RHO / 21
    x = variables
    return {
        x[0, 1]: capital_c * x[3, 4] / (7 * alpha) - x[3, 5] / 7,
        x[0, 4]: delta / 7 - capital_c * x[3, 4] / (7 * alpha),
        x[0, 5]: capital_c * (delta - x[3, 5]) / (7 * alpha),
        x[0, 6]: capital_c * x[3, 6] / (7 * alpha)
        + (beta * delta + 1 + RHO) / (7 * alpha),
        x[2, 1]: -1 - x[2, 4] + alpha * x[2, 5] / capital_c,
        x[3, 1]: x[3, 4] - alpha * x[3, 5] / capital_c,
    }


def hafnian_evaluator(edges):
    @cache
    def hafnian(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        return sp.expand(
            sum(
                edges[min(first, second), max(first, second)]
                * hafnian(vertices[1:position] + vertices[position + 1 :])
                for position, second in enumerate(vertices[1:], 1)
            )
        )

    return hafnian


def degree_one_response(terminal: str, incidence, edges) -> sp.Expr:
    hafnian = hafnian_evaluator(edges)
    column = P.index(terminal)
    return sp.expand(
        sum(
            incidence[row, column]
            * hafnian(tuple(index for index in range(7) if index != row))
            for row in range(7)
        )
    )


def main() -> None:
    assert sp.simplify(RHO**2 - 21) == 0
    assert len(FACES) == 20 and len(CROSS_PAIRS) == 12
    incidence = incidence_matrix()
    edges, variables = core_edges()
    permanent = permanent_evaluator(incidence)
    responses = {face: degree_five_response(face, edges, permanent) for face in FACES}

    ordered_variables = tuple(variables[pair] for pair in CROSS_PAIRS)
    coefficient_matrix = sp.Matrix(
        [[responses[face].coeff(variable) for variable in ordered_variables] for face in FACES]
    )
    constants = sp.Matrix(
        [responses[face].subs(dict.fromkeys(ordered_variables, 0)) for face in FACES]
    )
    assert coefficient_matrix.rank() == 6
    assert coefficient_matrix.row_join(-constants).rank() == 6

    parametrization = degree_five_parametrization(variables)
    for face in FACES:
        assert sp.simplify(responses[face].subs(parametrization)) == 0

    free_variables = (
        variables[2, 4],
        variables[2, 5],
        variables[2, 6],
        variables[3, 4],
        variables[3, 5],
        variables[3, 6],
    )
    assert all(variable not in parametrization for variable in free_variables)

    # The next smallest boundary is also consistent.  This is one exact point
    # on the degree-five family satisfying all seven degree-one equations;
    # x26 is set to zero only to display a single compact witness.
    degree_one_branch = {
        variables[3, 4]: 0,
        variables[3, 5]: 0,
        variables[3, 6]: 1,
        variables[2, 4]: sp.Rational(337, 506778)
        - sp.Rational(41206, 1773723) * RHO,
        variables[2, 5]: sp.Rational(23005, 521)
        + sp.Rational(11638, 10941) * RHO,
        variables[2, 6]: 0,
    }
    completed_branch = {
        **degree_one_branch,
        **{
            variable: sp.simplify(value.subs(degree_one_branch))
            for variable, value in parametrization.items()
        },
    }
    for face in FACES:
        assert sp.simplify(responses[face].subs(completed_branch)) == 0
    for terminal in P:
        assert sp.simplify(degree_one_response(terminal, incidence, edges).subs(completed_branch)) == 0

    print("aligned-core degree-five affine completion: VERIFIED")
    print("alignment=z*->f1; z1,z2->ell,h3; z3,z4->h5,ha; z5,z6->f2,h4")
    print("mixed_positions=(2,0,2,2,0,0,0)")
    print("degree5_system=20x12 rank=6 augmented_rank=6 solution_dimension=6")
    print("degree1_exact_extension=VERIFIED")
    print("degree3_conditions=NOT_TESTED")
    print("alignment_search=0 support_search=0 word_search=0")


if __name__ == "__main__":
    main()
