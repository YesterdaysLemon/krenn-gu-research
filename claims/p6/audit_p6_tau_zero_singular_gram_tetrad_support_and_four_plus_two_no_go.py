"""Independent sparse-polynomial audit of the P6 tau-zero 4+2 no-go."""

from fractions import Fraction
from functools import cache
from itertools import combinations

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Fraction]

CORE = (0, 1, 2, 3)
PORTS = (4, 5)
FACE = CORE + PORTS
FACE_COLUMNS = (
    (14, -24, 20, 15, -29, 9),
    (10, -33, 36, 30, -58, 18),
    (2, 38, -45, -30, 73, -23),
)


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: value for monomial, value in poly.items() if value}


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if not coefficient else {(): coefficient}


def variable(name: str) -> Polynomial:
    return {(name,): Fraction(1)}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = left.copy()
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + value
    return clean(result)


def scale(poly: Polynomial, value: int | Fraction) -> Polynomial:
    scalar = Fraction(value)
    return clean(
        {monomial: scalar * coefficient for monomial, coefficient in poly.items()}
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + left_value * right_value
            )
    return clean(result)


def add_many(polynomials: list[Polynomial]) -> Polynomial:
    result: Polynomial = {}
    for poly in polynomials:
        result = add(result, poly)
    return result


def matrix_variables(prefix: str, rows: int, columns: int) -> list[list[Polynomial]]:
    return [
        [variable(f"{prefix}{row}{column}") for column in range(columns)]
        for row in range(rows)
    ]


def coloured_matching(
    colours: dict[int, int],
    x_matrix: list[list[Polynomial]],
    y_matrix: list[list[Polynomial]],
    z_matrix: list[list[Polynomial]],
    beta_c: Polynomial,
    beta_d: Polynomial,
) -> Polynomial:
    port_index = {4: 0, 5: 1}

    def block_value(left: int, right: int) -> Polynomial:
        if left > right:
            left, right = right, left
        left_colour = colours[left]
        right_colour = colours[right]
        same_colour = left_colour == right_colour

        if left in CORE and right in CORE:
            if same_colour:
                return constant(1)
            if left_colour == 1:
                return z_matrix[left][right]
            return z_matrix[right][left]

        if left in PORTS and right in PORTS:
            if not same_colour:
                return {}
            return beta_c if left_colour == 0 else beta_d

        core_vertex = left
        port = right
        core_colour = left_colour
        port_colour = right_colour
        if same_colour:
            return {}
        if core_colour == 0 and port_colour == 1:
            return x_matrix[core_vertex][port_index[port]]
        return y_matrix[core_vertex][port_index[port]]

    @cache
    def rec(remaining: tuple[int, ...]) -> tuple[tuple[Monomial, Fraction], ...]:
        if not remaining:
            return tuple(constant(1).items())
        first = remaining[0]
        total: Polynomial = {}
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            rest_poly = dict(rec(rest))
            total = add(total, multiply(block_value(first, partner), rest_poly))
        return tuple(sorted(total.items()))

    return dict(rec(FACE))


def row_pair(
    matrix: list[list[Polynomial]],
    first: int,
    second: int,
    left: int,
    right: int,
) -> Polynomial:
    return add(
        multiply(matrix[first][left], matrix[second][right]),
        multiply(matrix[first][right], matrix[second][left]),
    )


def matching_identity_audit() -> None:
    x_matrix = matrix_variables("x", 4, 2)
    y_matrix = matrix_variables("y", 4, 2)
    z_matrix = [
        [
            {} if row == column else variable(f"z{row}{column}")
            for column in CORE
        ]
        for row in CORE
    ]
    beta_c = variable("bc")
    beta_d = variable("bd")

    window_minority = {vertex: (1 if vertex in CORE else 0) for vertex in FACE}
    coefficient = coloured_matching(
        window_minority,
        x_matrix,
        y_matrix,
        z_matrix,
        beta_c,
        beta_d,
    )
    expected = add(
        scale(beta_c, 3),
        add_many(
            [
                row_pair(y_matrix, left, right, 0, 1)
                for left, right in combinations(CORE, 2)
            ]
        ),
    )
    assert coefficient == expected

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
    circulation_pair = add(
        multiply(z_matrix[0][2], z_matrix[1][3]),
        multiply(z_matrix[0][3], z_matrix[1][2]),
    )
    expected = add(
        multiply(beta_c, add(constant(1), circulation_pair)),
        row_pair(y_matrix, 0, 1, 0, 1),
    )
    assert coefficient == expected

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
    expected = multiply(
        y_matrix[0][1],
        add_many([x_matrix[row][0] for row in (1, 2, 3)]),
    )
    assert coefficient == expected
    print("independent sparse matching identities: PASS")


def euler_hafnian_audit() -> None:
    edges = {
        pair: variable(f"a{pair[0]}{pair[1]}")
        for pair in combinations(CORE, 2)
    }
    core_hafnian = add_many(
        [
            multiply(edges[(0, 1)], edges[(2, 3)]),
            multiply(edges[(0, 2)], edges[(1, 3)]),
            multiply(edges[(0, 3)], edges[(1, 2)]),
        ]
    )
    euler_sum: Polynomial = {}
    for pair in combinations(CORE, 2):
        complement = tuple(
            vertex for vertex in CORE if vertex not in pair
        )
        euler_sum = add(
            euler_sum,
            multiply(edges[pair], edges[tuple(sorted(complement))]),
        )
    assert euler_sum == scale(core_hafnian, 2)

    beta = variable("b")
    substituted_pairs = {
        pair: scale(multiply(edges[pair], beta), -1)
        for pair in combinations(CORE, 2)
    }
    window_equation = multiply(beta, core_hafnian)
    for pair in combinations(CORE, 2):
        complement = tuple(
            vertex for vertex in CORE if vertex not in pair
        )
        window_equation = add(
            window_equation,
            multiply(
                edges[tuple(sorted(complement))],
                substituted_pairs[pair],
            ),
        )
    assert window_equation == scale(multiply(beta, core_hafnian), -1)
    print("independent Euler-hafnian factor-two identity: PASS")


def tetrad_audit() -> None:
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
        assert all(value for value in column)

    rows = [variable(f"r{index}") for index in range(4)]
    rank_one = [
        scale(multiply(rows[left], rows[right]), -2)
        for left, right in combinations(range(4), 2)
    ]
    products = (
        multiply(rank_one[0], rank_one[5]),
        multiply(rank_one[1], rank_one[4]),
        multiply(rank_one[2], rank_one[3]),
    )
    assert products[0] == products[1] == products[2]
    print("independent rank-one tetrad boundary: PASS")


def circulation_energy_audit() -> None:
    spare = variable("s")
    u = variable("u")
    v = variable("v")
    w = variable("w")
    x = variable("x")
    z_matrix = [
        [
            {},
            scale(add(spare, w), -1),
            add_many([u, spare, v, w]),
            scale(add(u, v), -1),
        ],
        [
            add_many([spare, v, w, x]),
            {},
            scale(add_many([u, spare, v, w, x]), -1),
            u,
        ],
        [scale(add(spare, v), -1), spare, {}, v],
        [scale(add(w, x), -1), w, x, {}],
    ]
    for row in CORE:
        assert add_many(z_matrix[row]) == {}
    for column in CORE:
        assert add_many([z_matrix[row][column] for row in CORE]) == {}

    energy: Polynomial = {}
    for first, second in combinations(CORE, 2):
        left, right = tuple(
            vertex
            for vertex in CORE
            if vertex not in (first, second)
        )
        energy = add(
            energy,
            add(
                multiply(z_matrix[first][left], z_matrix[second][right]),
                multiply(z_matrix[first][right], z_matrix[second][left]),
            ),
        )
    expected = scale(
        add_many(
            [
                multiply(u, u),
                multiply(u, v),
                scale(multiply(u, w), 2),
                multiply(u, x),
                multiply(v, v),
                multiply(v, w),
                scale(multiply(v, x), 2),
                multiply(w, w),
                multiply(w, x),
                multiply(x, x),
            ]
        ),
        2,
    )
    assert energy == expected
    assert "s" not in {name for monomial in energy for name in monomial}
    print("independent circulation-energy polynomial: PASS")


def section_family_audit() -> None:
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
    print("independent tau-family boundary data: PASS")


def main() -> None:
    matching_identity_audit()
    euler_hafnian_audit()
    tetrad_audit()
    circulation_energy_audit()
    section_family_audit()
    print("computer_algebra=0")
    print("P6 tau-zero singular-Gram/tetrad no-go independent audit: PASS")


if __name__ == "__main__":
    main()
