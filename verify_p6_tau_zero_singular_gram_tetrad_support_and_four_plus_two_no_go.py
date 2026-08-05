"""Exact checks for the P6 tau-zero singular-Gram 4+2 no-go."""

from functools import cache
from itertools import combinations

import sympy as sp

CORE = (0, 1, 2, 3)
PORTS = (4, 5)
FACE = CORE + PORTS
FACE_COLUMNS = (
    (14, -24, 20, 15, -29, 9),
    (10, -33, 36, 30, -58, 18),
    (2, 38, -45, -30, 73, -23),
)


def coloured_matching(
    colours: dict[int, int],
    x_matrix: sp.Matrix,
    y_matrix: sp.Matrix,
    z_matrix: sp.Matrix,
    beta_c: sp.Expr,
    beta_d: sp.Expr,
) -> sp.Expr:
    port_index = {4: 0, 5: 1}

    def block_value(left: int, right: int) -> sp.Expr:
        if left > right:
            left, right = right, left
        left_colour = colours[left]
        right_colour = colours[right]
        same_colour = left_colour == right_colour

        if left in CORE and right in CORE:
            if same_colour:
                return sp.Integer(1)
            if left_colour == 1:
                return z_matrix[left, right]
            return z_matrix[right, left]

        if left in PORTS and right in PORTS:
            if not same_colour:
                return sp.Integer(0)
            return beta_c if left_colour == 0 else beta_d

        core_vertex = left
        port = right
        core_colour = left_colour
        port_colour = right_colour
        if same_colour:
            return sp.Integer(0)
        if core_colour == 0 and port_colour == 1:
            return x_matrix[core_vertex, port_index[port]]
        return y_matrix[core_vertex, port_index[port]]

    @cache
    def rec(remaining: tuple[int, ...]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        first = remaining[0]
        total = sp.Integer(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += block_value(first, partner) * rec(rest)
        return sp.expand(total)

    return rec(FACE)


def row_pair(
    matrix: sp.Matrix, first: int, second: int, left: int, right: int
) -> sp.Expr:
    return sp.expand(
        matrix[first, left] * matrix[second, right]
        + matrix[first, right] * matrix[second, left]
    )


def matching_identity_checks() -> None:
    x_matrix = sp.Matrix(4, 2, sp.symbols("x0:8"))
    y_matrix = sp.Matrix(4, 2, sp.symbols("y0:8"))
    z_symbols = sp.symbols("z0:12")
    z_matrix = sp.zeros(4)
    for symbol, (left, right) in zip(
        z_symbols,
        (
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 2),
            (1, 3),
            (2, 0),
            (2, 1),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 2),
        ),
        strict=True,
    ):
        z_matrix[left, right] = symbol
    beta_c, beta_d = sp.symbols("bc bd")

    window_minority = {vertex: (1 if vertex in CORE else 0) for vertex in FACE}
    coefficient = coloured_matching(
        window_minority,
        x_matrix,
        y_matrix,
        z_matrix,
        beta_c,
        beta_d,
    )
    expected = 3 * beta_c + sum(
        row_pair(y_matrix, left, right, 0, 1)
        for left, right in combinations(CORE, 2)
    )
    assert sp.expand(coefficient - expected) == 0

    core_pair_minority = {vertex: 0 for vertex in FACE}
    core_pair_minority[0] = 1
    core_pair_minority[1] = 1
    coefficient = coloured_matching(
        core_pair_minority,
        x_matrix,
        y_matrix,
        z_matrix,
        beta_c,
        beta_d,
    )
    p_01 = row_pair(y_matrix, 0, 1, 0, 1)
    r_01 = z_matrix[0, 2] * z_matrix[1, 3] + z_matrix[0, 3] * z_matrix[1, 2]
    assert sp.expand(coefficient - (beta_c * (1 + r_01) + p_01)) == 0

    mixed_location = {vertex: 0 for vertex in FACE}
    mixed_location[0] = 1
    mixed_location[4] = 1
    coefficient = coloured_matching(
        mixed_location,
        x_matrix,
        y_matrix,
        z_matrix,
        beta_c,
        beta_d,
    )
    d_matrix = sp.ones(4) - sp.eye(4)
    expected = y_matrix[0, 1] * (d_matrix * x_matrix)[0, 0]
    assert sp.expand(coefficient - expected) == 0
    print("three symbolic 4+2 matching identities, including circulation: PASS")


def euler_hafnian_check() -> None:
    a01, a02, a03, a12, a13, a23 = sp.symbols(
        "a01 a02 a03 a12 a13 a23"
    )
    edge_weights = {
        (0, 1): a01,
        (0, 2): a02,
        (0, 3): a03,
        (1, 2): a12,
        (1, 3): a13,
        (2, 3): a23,
    }
    core_hafnian = a01 * a23 + a02 * a13 + a03 * a12
    euler_sum = sp.Integer(0)
    for left, right in combinations(CORE, 2):
        complement = tuple(
            vertex for vertex in CORE if vertex not in (left, right)
        )
        euler_sum += (
            edge_weights[(left, right)]
            * edge_weights[tuple(sorted(complement))]
        )
    assert sp.expand(euler_sum - 2 * core_hafnian) == 0

    beta = sp.symbols("b")
    pair_symbols = {
        pair: -edge_weights[pair] * beta
        for pair in combinations(CORE, 2)
    }
    window_equation = beta * core_hafnian + sum(
        edge_weights[
            tuple(
                sorted(
                    vertex
                    for vertex in CORE
                    if vertex not in pair
                )
            )
        ]
        * pair_symbols[pair]
        for pair in combinations(CORE, 2)
    )
    assert sp.expand(window_equation + beta * core_hafnian) == 0
    print("four-core Euler-hafnian factor-two identity: PASS")


def tetrad_checks() -> None:
    expected_products = (
        (126, 696, 300),
        (180, 1914, 1080),
        (-46, 2774, 1350),
    )
    for column, target in zip(
        FACE_COLUMNS, expected_products, strict=True
    ):
        products = (
            column[0] * column[5],
            column[1] * column[4],
            column[2] * column[3],
        )
        assert products == target
        assert len(set(products)) > 1
        assert all(value != 0 for value in column)

    row = sp.symbols("r0:4")
    rank_one = tuple(
        -2 * row[left] * row[right]
        for left, right in combinations(range(4), 2)
    )
    products = (
        rank_one[0] * rank_one[5],
        rank_one[1] * rank_one[4],
        rank_one[2] * rank_one[3],
    )
    assert all(
        sp.expand(product - products[0]) == 0
        for product in products[1:]
    )
    print("exact face columns fail the rank-one tetrad identities: PASS")


def circulation_energy_check() -> None:
    spare, u, v, w, x = sp.symbols("s u v w x")
    z_matrix = sp.Matrix(
        [
            [0, -spare - w, u + spare + v + w, -u - v],
            [spare + v + w + x, 0, -u - spare - v - w - x, u],
            [-spare - v, spare, 0, v],
            [-w - x, w, x, 0],
        ]
    )
    assert all(sum(z_matrix[row, column] for column in CORE) == 0 for row in CORE)
    assert all(sum(z_matrix[row, column] for row in CORE) == 0 for column in CORE)

    energy = sp.Integer(0)
    for first, second in combinations(CORE, 2):
        complement = tuple(
            vertex
            for vertex in CORE
            if vertex not in (first, second)
        )
        left, right = complement
        energy += (
            z_matrix[first, left] * z_matrix[second, right]
            + z_matrix[first, right] * z_matrix[second, left]
        )
    expected = 2 * (
        u**2
        + u * v
        + 2 * u * w
        + u * x
        + v**2
        + v * w
        + 2 * v * x
        + w**2
        + w * x
        + x**2
    )
    assert sp.expand(energy - expected) == 0
    witness = {u: sp.sqrt(sp.Rational(-3, 2)), v: 0, w: 0, x: 0}
    assert sp.simplify(energy.subs(witness) + 3) == 0
    print("five-dimensional core-circulation energy boundary: PASS")


def section_family_checks() -> None:
    expected_covariants = ((76, -12), (119, -38), (-132, 54))
    for column, target in zip(
        FACE_COLUMNS, expected_covariants, strict=True
    ):
        first = column[0] + column[5]
        second = column[1] + column[4]
        third = column[2] + column[3]
        assert (first - second, first - third) == target
        assert target != (0, 0)
        assert len(set(column)) > 1
    print("nonzero covariants and nonconstant columns for tau-family closure: PASS")


def main() -> None:
    matching_identity_checks()
    euler_hafnian_check()
    tetrad_checks()
    circulation_energy_check()
    section_family_checks()
    print("P6 tau-zero singular-Gram/tetrad no-go primary verification: PASS")


if __name__ == "__main__":
    main()
