"""Focused exact verifier for the pair/four-port interference boundary."""

from fractions import Fraction
from itertools import combinations, product

import sympy as sp

PORTS = tuple(range(4))
COLORS = tuple(range(3))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def ordered_pair(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def verify_symbolic_interference() -> None:
    h = sp.symbols("h")
    b = {e: sp.symbols(f"B{e[0]}{e[1]}") for e in combinations(PORTS, 2)}
    k = {e: sp.symbols(f"K{e[0]}{e[1]}") for e in combinations(PORTS, 2)}
    d = {e: h * b[e] + k[e] for e in b}

    c_b = sum(b[e] * b[f] for e, f in MATCHINGS)
    c_k = sum(k[e] * k[f] for e, f in MATCHINGS)
    c_d = sum(d[e] * d[f] for e, f in MATCHINGS)
    t = h * c_b + sum(k[e] * b[f] + b[e] * k[f] for e, f in MATCHINGS)
    assert sp.expand(h * t - c_d + c_k) == 0


def verify_common_row_expansion() -> None:
    a = sp.symbols("a0:4")
    b = sp.symbols("b0:4")
    k = {(i, j): a[i] * b[j] + b[i] * a[j] for i, j in combinations(PORTS, 2)}
    compound = sp.expand(sum(k[e] * k[f] for e, f in MATCHINGS))
    assignment = 2 * sum(
        sp.prod(a[u] if u in subset else b[u] for u in PORTS)
        for subset in map(set, combinations(PORTS, 2))
    )
    assert sp.expand(compound - assignment) == 0

    # In the port-0 flattening, every assignment row is in span{a_0,b_0}.
    poly = sp.Poly(compound, a[0], b[0])
    assert all(sum(monomial) == 1 for monomial, _ in poly.terms())


def diagonal_compound_entry(
    diagonal: dict[tuple[tuple[int, int], int], sp.Symbol],
    word: tuple[int, int, int, int],
) -> sp.Expr:
    total = sp.Integer(0)
    for e, f in MATCHINGS:
        i, j = e
        k, ell = f
        if word[i] == word[j] and word[k] == word[ell]:
            total += diagonal[e, word[i]] * diagonal[f, word[k]]
    return sp.expand(total)


def verify_all_selected_grids() -> None:
    diagonal = {
        (e, c): sp.symbols(f"d{e[0]}{e[1]}_{c}")
        for e in combinations(PORTS, 2)
        for c in COLORS
    }
    fixed_port = 0
    choices = {
        c: tuple(
            (v, delta)
            for v in PORTS
            if v != fixed_port
            for delta in COLORS
            if delta != c
        )
        for c in COLORS
    }
    checked = 0
    for selected in product(*(choices[c] for c in COLORS)):
        betas: dict[int, tuple[int, int, int]] = {}
        expected: dict[int, sp.Expr] = {}
        for c, (v, delta) in zip(COLORS, selected, strict=True):
            other_ports = tuple(u for u in PORTS if u != fixed_port)
            beta = tuple(c if u == v else delta for u in other_ports)
            betas[c] = beta
            e = ordered_pair(fixed_port, v)
            remaining = tuple(u for u in PORTS if u not in e)
            f = ordered_pair(*remaining)
            expected[c] = diagonal[e, c] * diagonal[f, delta]
        assert len(set(betas.values())) == 3

        other_ports = tuple(u for u in PORTS if u != fixed_port)
        for row in COLORS:
            for column in COLORS:
                word_list = [0] * 4
                word_list[fixed_port] = row
                for u, value in zip(other_ports, betas[column], strict=True):
                    word_list[u] = value
                word = tuple(word_list)
                assert len(set(word)) > 1
                actual = diagonal_compound_entry(diagonal, word)
                target = expected[column] if row == column else 0
                assert sp.expand(actual - target) == 0
        checked += 1
    assert checked == 216


def frame_data() -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    a = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0)]
    b = [(0, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0)]
    return a, b


def k_entry(
    a: list[tuple[int, int, int]],
    b: list[tuple[int, int, int]],
    i: int,
    j: int,
    ci: int,
    cj: int,
) -> Fraction:
    return Fraction(a[i][ci] * b[j][cj] + b[i][ci] * a[j][cj])


def target_diagonals() -> dict[tuple[int, int], tuple[Fraction, Fraction, Fraction]]:
    return {
        (0, 1): (Fraction(0), Fraction(0), Fraction(1)),
        (2, 3): (Fraction(0), Fraction(0), Fraction(1)),
        (0, 2): (Fraction(1), Fraction(1), Fraction(0)),
        (1, 3): (Fraction(2), Fraction(2), Fraction(0)),
        (0, 3): (Fraction(1), Fraction(2, 3), Fraction(0)),
        (1, 2): (Fraction(3), Fraction(2), Fraction(0)),
    }


def d_entry(
    diagonal: dict[tuple[int, int], tuple[Fraction, Fraction, Fraction]],
    i: int,
    j: int,
    ci: int,
    cj: int,
) -> Fraction:
    if i > j:
        i, j, ci, cj = j, i, cj, ci
    return diagonal[i, j][ci] if ci == cj else Fraction(0)


def compound_word(
    entry,
    word: tuple[int, int, int, int],
) -> Fraction:
    return sum(
        entry(*e, word[e[0]], word[e[1]]) * entry(*f, word[f[0]], word[f[1]])
        for e, f in MATCHINGS
    )


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for offset in range(1, len(vertices)):
        second = vertices[offset]
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def verify_camouflage_control() -> None:
    a, b = frame_data()
    diagonal = target_diagonals()
    for u in PORTS:
        assert sp.Matrix([a[u], b[u]]).rank() == 2

    def kval(i: int, j: int, ci: int, cj: int) -> Fraction:
        return k_entry(a, b, i, j, ci, cj)

    def dval(i: int, j: int, ci: int, cj: int) -> Fraction:
        return d_entry(diagonal, i, j, ci, cj)

    def bval(i: int, j: int, ci: int, cj: int) -> Fraction:
        return dval(i, j, ci, cj) - kval(i, j, ci, cj)

    assert kval(0, 1, 0, 1) == 1
    assert kval(2, 3, 1, 0) == 1

    expected_pure = (Fraction(3), Fraction(4, 3), Fraction(1))
    response: dict[tuple[int, int, int, int], Fraction] = {}
    for word in product(COLORS, repeat=4):
        d_compound = compound_word(dval, word)
        k_compound = compound_word(kval, word)
        response[word] = d_compound - k_compound
        if len(set(word)) > 1:
            assert response[word] == 0
    assert tuple(response[(c, c, c, c)] for c in COLORS) == expected_pure

    # A separate six-vertex matching expansion realizes the same response.
    # Vertices 0,1 are residuals; vertices 2,...,5 are ports 0,...,3.
    def graph_edge(i: int, j: int, colors: tuple[int, ...]) -> Fraction:
        if i > j:
            return graph_edge(j, i, colors)
        if (i, j) == (0, 1):
            return Fraction(1)
        if i == 0 and j >= 2:
            return Fraction(a[j - 2][colors[j]])
        if i == 1 and j >= 2:
            return Fraction(b[j - 2][colors[j]])
        return bval(i - 2, j - 2, colors[i], colors[j])

    matchings = tuple(perfect_matchings(tuple(range(6))))
    assert len(matchings) == 15
    for word in product(COLORS, repeat=4):
        colors = (0, 0) + word
        total = sum(
            sp.prod(graph_edge(i, j, colors) for i, j in matching)
            for matching in matchings
        )
        assert total == response[word]

    # Every pair response is D, checked by its three matchings.
    for i, j in combinations(PORTS, 2):
        for ci, cj in product(COLORS, repeat=2):
            pair_response = bval(i, j, ci, cj) + kval(i, j, ci, cj)
            assert pair_response == dval(i, j, ci, cj)
            if ci != cj:
                assert pair_response == 0

    # K -> -K and B -> D+K preserve both target depths but not K.
    for word in product(COLORS, repeat=4):
        neg_k_compound = compound_word(lambda i, j, ci, cj: -kval(i, j, ci, cj), word)
        assert compound_word(dval, word) - neg_k_compound == response[word]


def verify_zero_h_deck_ambiguity() -> None:
    a = (1, 1, 0)
    b = (1, -1, 0)

    def kval(_i: int, _j: int, ci: int, cj: int) -> Fraction:
        return Fraction(a[ci] * b[cj] + b[ci] * a[cj])

    for ci, cj in product(COLORS, repeat=2):
        if ci != cj:
            assert kval(0, 1, ci, cj) == 0
    assert kval(0, 1, 0, 0) == 2
    assert kval(0, 1, 1, 1) == -2

    zero_blocks = {e: Fraction(0) for e in combinations(PORTS, 2)}
    signed_blocks = zero_blocks.copy()
    signed_blocks[(0, 1)] = Fraction(1)
    signed_blocks[(2, 3)] = Fraction(-1)

    def response_for_blocks(
        multipliers: dict[tuple[int, int], Fraction],
        word: tuple[int, int, int, int],
    ) -> Fraction:
        total = Fraction(0)
        for e, f in MATCHINGS:
            ke = kval(*e, word[e[0]], word[e[1]])
            kf = kval(*f, word[f[0]], word[f[1]])
            total += ke * multipliers[f] * kf + multipliers[e] * ke * kf
        return total

    for word in product(COLORS, repeat=4):
        assert response_for_blocks(zero_blocks, word) == 0
        assert response_for_blocks(signed_blocks, word) == 0


def main() -> None:
    verify_symbolic_interference()
    verify_common_row_expansion()
    verify_all_selected_grids()
    verify_camouflage_control()
    verify_zero_h_deck_ambiguity()
    print("two-residual pair/four-port interference verifier: PASS")


if __name__ == "__main__":
    main()
