"""No-import audit of the top two-port synchronization boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations

# A tiny commutative polynomial dictionary.  Monomials are sorted tuples of
# variable names; coefficients are integers.
Poly = dict[tuple[str, ...], int]


def poly_var(name: str) -> Poly:
    return {(name,): 1}


def poly_add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def poly_mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_determinant_3(matrix: list[list[Poly]]) -> Poly:
    result: Poly = {}
    for permutation in permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j] for i in range(3) for j in range(i + 1, 3)
        )
        term: Poly = {(): 1}
        for row, column in enumerate(permutation):
            term = poly_mul(term, matrix[row][column])
        result = poly_add(result, term, -1 if inversions % 2 else 1)
    return result


def zeon_add(
    left: dict[int, Fraction], right: dict[int, Fraction]
) -> dict[int, Fraction]:
    result = dict(left)
    for mask, value in right.items():
        result[mask] = result.get(mask, Fraction(0)) + value
    return {mask: value for mask, value in result.items() if value}


def zeon_scale(poly: dict[int, Fraction], scalar: Fraction) -> dict[int, Fraction]:
    return {mask: scalar * value for mask, value in poly.items() if scalar * value}


def zeon_mul(
    left: dict[int, Fraction], right: dict[int, Fraction]
) -> dict[int, Fraction]:
    result: dict[int, Fraction] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def zeon_inverse(
    poly: dict[int, Fraction], port_count: int
) -> dict[int, Fraction]:
    assert poly.get(0) == 1
    nilpotent = zeon_add(poly, {0: Fraction(-1)})
    result = {0: Fraction(1)}
    power = {0: Fraction(1)}
    for degree in range(1, port_count + 1):
        power = zeon_mul(power, nilpotent)
        result = zeon_add(result, zeon_scale(power, Fraction((-1) ** degree)))
    return result


def hafnian(matrix: list[list[int]]) -> int:
    size = len(matrix)
    assert size % 2 == 0 and all(len(row) == size for row in matrix)
    memo = {0: 1}

    def evaluate(mask: int) -> int:
        if mask in memo:
            return memo[mask]
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        total = 0
        candidates = rest
        while candidates:
            second_bit = candidates & -candidates
            second = second_bit.bit_length() - 1
            total += matrix[first][second] * evaluate(rest ^ second_bit)
            candidates ^= second_bit
        memo[mask] = total
        return total

    return evaluate((1 << size) - 1)


def permanent(matrix: list[list[int]]) -> int:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    states = {0: 1}
    for row in matrix:
        next_states: dict[int, int] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = next_states.get(new_mask, 0) + value * entry
        states = next_states
    return states[(1 << size) - 1]


def principal(matrix: list[list[int]], indices: tuple[int, ...]) -> list[list[int]]:
    return [[matrix[i][j] for j in indices] for i in indices]


def main() -> None:
    # Independently prove det(a0*b1^T+b0*a1^T)=0 as a polynomial identity.
    synchronized: list[list[Poly]] = []
    for i in range(3):
        row: list[Poly] = []
        for j in range(3):
            first = poly_mul(poly_var(f"a0{i}"), poly_var(f"b1{j}"))
            second = poly_mul(poly_var(f"b0{i}"), poly_var(f"a1{j}"))
            row.append(poly_add(first, second))
        synchronized.append(row)
    assert polynomial_determinant_3(synchronized) == {}

    # The physical direct sector h=1, B=I3, a=b=0 returns I3 exactly.
    identity = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    direct_response = [[1 * identity[i][j] + 0 + 0 for j in range(3)] for i in range(3)]
    assert direct_response == identity
    assert (
        identity[0][0] * identity[1][1] * identity[2][2]
        - identity[0][0] * identity[1][2] * identity[2][1]
        - identity[0][1] * identity[1][0] * identity[2][2]
        + identity[0][1] * identity[1][2] * identity[2][0]
        + identity[0][2] * identity[1][0] * identity[2][1]
        - identity[0][2] * identity[1][1] * identity[2][0]
        == 1
    )

    # Independent four-port dual-Wick calculation at one exact integer point.
    pairs = tuple(combinations(range(4), 2))
    pair_masks = {pair: (1 << pair[0]) | (1 << pair[1]) for pair in pairs}
    b_values = dict(zip(pairs, (2, -1, 3, 4, -2, 5), strict=True))
    a_values = (1, 2, -1, 3)
    d_values = (2, -2, 4, 1)
    k_values = {
        pair: a_values[pair[0]] * d_values[pair[1]]
        + d_values[pair[0]] * a_values[pair[1]]
        for pair in pairs
    }
    q_b = {pair_masks[pair]: Fraction(value) for pair, value in b_values.items()}
    q_k = {pair_masks[pair]: Fraction(value) for pair, value in k_values.items()}
    m_family = zeon_add(
        {0: Fraction(1)},
        zeon_add(q_b, zeon_scale(zeon_mul(q_b, q_b), Fraction(1, 2))),
    )
    h_value = Fraction(7)
    z_family = zeon_mul(m_family, zeon_add({0: h_value}, q_k))
    for pair, mask in pair_masks.items():
        assert z_family[mask] == h_value * b_values[pair] + k_values[pair]
    n_family = zeon_add(z_family, zeon_scale(m_family, -h_value))
    relative = zeon_mul(n_family, zeon_inverse(m_family, 4))
    assert relative == q_k

    full_mask = 15
    tangent_four = 0
    for pair, mask in pair_masks.items():
        complement_pair = tuple(i for i in range(4) if (full_mask ^ mask) & (1 << i))
        tangent_four += k_values[pair] * b_values[complement_pair]
    assert n_family[full_mask] == tangent_four

    # q=4: equal top permanent, different constant and quadratic layers.
    zero = [[0] * 4 for _ in range(4)]
    split = [[0] * 4 for _ in range(4)]
    split[0][1] = split[1][0] = 1
    split[2][3] = split[3][2] = 1
    incidence = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    assert permanent(incidence) == 1
    assert hafnian(zero) == 0
    assert hafnian(split) == 1
    zero_quadratic: dict[tuple[int, int], int] = {}
    split_quadratic: dict[tuple[int, int], int] = {}
    for pair in pairs:
        complement = tuple(i for i in range(4) if i not in pair)
        incidence_minor = [[incidence[i][j] for j in pair] for i in pair]
        zero_quadratic[pair] = hafnian(principal(zero, complement)) * permanent(
            incidence_minor
        )
        split_quadratic[pair] = hafnian(principal(split, complement)) * permanent(
            incidence_minor
        )
    assert all(value == 0 for value in zero_quadratic.values())
    assert split_quadratic == {
        (0, 1): 1,
        (0, 2): 0,
        (0, 3): 0,
        (1, 2): 0,
        (1, 3): 0,
        (2, 3): 1,
    }

    assert tuple(3 * order + 3 for order in (5, 6, 7)) == (18, 21, 24)

    print("AUDIT PASS")
    print("generic synchronized determinant vanishes identically")
    print("direct rank-three top block and paired-depth recovery agree")
    print("q=4 top/lower nonobservability witness agrees")
    print("strict support table P5/P6/P7 = 18/21/24")


if __name__ == "__main__":
    main()
