"""Exact replay for the m=3 full-joint-rank monomial-root-edge localization."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp


def tidx(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def monomial_block(left: int, right: int) -> dict[tuple[int, int], sp.Rational]:
    return {(left, right): sp.Rational(1)}


def derivative_matrix(
    b12: dict[tuple[int, int], sp.Rational],
    b13: dict[tuple[int, int], sp.Rational],
    b23: dict[tuple[int, int], sp.Rational],
) -> sp.Matrix:
    """Columns are the images of the nine standard domain vectors."""
    out = sp.zeros(27, 9)
    for h in range(3):
        for (b, c), value in b23.items():
            out[tidx(h, b, c), h] += value
        for (a, c), value in b13.items():
            out[tidx(a, h, c), 3 + h] += value
        for (a, b), value in b12.items():
            out[tidx(a, b, h), 6 + h] += value
    return out


def check_derivative_ranks() -> None:
    zero: dict[tuple[int, int], sp.Rational] = {}
    assert derivative_matrix(zero, zero, monomial_block(1, 2)).rank() == 3

    # Exhaust every pair of coordinate-monomial root blocks.
    slots = ("12", "13", "23")
    for first, second in combinations(slots, 2):
        for pos_first, pos_second in product(product(range(3), repeat=2), repeat=2):
            blocks = {slot: {} for slot in slots}
            blocks[first] = monomial_block(*pos_first)
            blocks[second] = monomial_block(*pos_second)
            rank = derivative_matrix(blocks["12"], blocks["13"], blocks["23"]).rank()
            assert rank in (5, 6)

    # The shared third factor gives the sharp one-dimensional intersection.
    aligned = derivative_matrix(
        {}, monomial_block(0, 2), monomial_block(1, 2)
    )
    assert aligned.rank() == 5
    transverse = derivative_matrix(
        {}, monomial_block(0, 1), monomial_block(1, 2)
    )
    assert transverse.rank() == 6
    print("shared-derivative root-block ranks: PASS (3 / 5 / 6)")


def check_two_term_torus_zeros() -> None:
    positions = list(product(range(3), repeat=2))
    checked = 0
    for first, second in combinations(positions, 2):
        s = [sp.Rational(1)] * 3
        t = [sp.Rational(1)] * 3
        variables_first = {("s", first[0]), ("t", first[1])}
        variables_second = {("s", second[0]), ("t", second[1])}
        kind, index = next(iter(variables_first - variables_second))
        if kind == "s":
            s[index] = sp.Rational(-3, 2)
        else:
            t[index] = sp.Rational(-3, 2)
        value = 2 * s[first[0]] * t[first[1]] + 3 * s[second[0]] * t[second[1]]
        assert value == 0
        assert all(entry != 0 for entry in (*s, *t))
        checked += 1
    assert checked == 36
    print("two-monomial bilinear torus zeros: PASS (36/36)")


def check_sparse_target_quotient() -> None:
    for p, q in product(range(3), repeat=2):
        exceptional = {(a, p, q) for a in range(3)}
        fixed_diagonal = {
            (c, c, c)
            for c in range(3)
            if (c, c, c) not in exceptional
        }
        expected = 2 if p == q else 3
        assert len(fixed_diagonal) == expected
        assert len(exceptional) == 3
    print("GHZ modulo one root coordinate line: PASS (9/9)")


def check_exceptional_line_pair_globalization() -> None:
    values = [sp.Rational(((17 * index + 11) % 13) - 6) for index in range(81)]
    h = sp.MutableDenseNDimArray(values, (3, 3, 3, 3))
    checked = 0
    for a, p, q, x, y, r in product(range(3), repeat=6):
        colours = (x, y, r)
        direct = sum(
            h[0, sigma[0], a, colours[sigma[0]]]
            * h[1, sigma[1], p, colours[sigma[1]]]
            * h[2, sigma[2], q, colours[sigma[2]]]
            for sigma in permutations(range(3))
        )
        grouped = (
            h[0, 0, a, x]
            * (h[1, 1, p, y] * h[2, 2, q, r] + h[1, 2, p, r] * h[2, 1, q, y])
            + h[0, 1, a, y]
            * (h[1, 0, p, x] * h[2, 2, q, r] + h[1, 2, p, r] * h[2, 0, q, x])
            + h[0, 2, a, r]
            * (h[1, 0, p, x] * h[2, 1, q, y] + h[1, 1, p, y] * h[2, 0, q, x])
        )
        assert direct == grouped
        checked += 1
    assert checked == 729
    print("exceptional-line global pair decomposition: PASS (729/729)")


def permanent3(matrix: tuple[tuple[int, ...], ...]) -> int:
    return sum(
        matrix[0][sigma[0]] * matrix[1][sigma[1]] * matrix[2][sigma[2]]
        for sigma in permutations(range(3))
    )


def check_monomial_rank_floor() -> None:
    matrices: list[tuple[tuple[int, ...], ...]] = []
    for entries in product(range(4), repeat=9):
        matrix = tuple(tuple(entries[3 * i + j] for j in range(3)) for i in range(3))
        if any(sum(row) != 3 for row in matrix):
            continue
        if any(sum(matrix[i][j] for i in range(3)) != 3 for j in range(3)):
            continue
        matrices.append(matrix)
    values = [permanent3(matrix) for matrix in matrices]
    assert len(matrices) == 55
    assert min(values) == 6
    assert values.count(6) == 1
    print("monomial joint-cross permanental rank floor: PASS (min 6 over 55 counts)")


def main() -> None:
    check_derivative_ranks()
    check_two_term_torus_zeros()
    check_exceptional_line_pair_globalization()
    check_sparse_target_quotient()
    check_monomial_rank_floor()
    print("balanced m=3 full-joint-rank monomial-root-edge localization: PASS")


if __name__ == "__main__":
    main()
