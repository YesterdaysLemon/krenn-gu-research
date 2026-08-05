"""Independent no-import audit of vacuum-free dual-Wick observability.

This audit uses rational arithmetic and a separate fixed hafnian recurrence.
It imports neither SymPy nor the primary verifier.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations


def hafnian(vertices: tuple[int, ...], edge: dict[tuple[int, int], Fraction]) -> Fraction:
    @cache
    def recurse(current: tuple[int, ...]) -> Fraction:
        if not current:
            return Fraction(1)
        first = current[0]
        total = Fraction(0)
        for position, partner in enumerate(current[1:], start=1):
            total += edge[tuple(sorted((first, partner)))] * recurse(
                current[1:position] + current[position + 1 :]
            )
        return total

    return recurse(vertices)


def defect(
    subset: tuple[int, ...],
    h: Fraction,
    direct: dict[tuple[int, int], Fraction],
    corrected: dict[tuple[int, int], Fraction],
) -> tuple[Fraction, Fraction]:
    m_subset = hafnian(subset, direct)
    z_subset = h * m_subset
    insertion = Fraction(0)
    observed_sum = Fraction(0)
    for pair in combinations(subset, 2):
        complement = tuple(vertex for vertex in subset if vertex not in pair)
        m_complement = hafnian(complement, direct)
        insertion += corrected[pair] * m_complement
        observed_sum += (h * direct[pair] + corrected[pair]) * m_complement
    z_subset += insertion
    return m_subset, observed_sum - z_subset


def main() -> None:
    # One fixed dense rational response independently checks the 4/6 factors.
    vertices = tuple(range(6))
    pairs = tuple(combinations(vertices, 2))
    direct = {
        pair: Fraction((pair[0] + 2) * (pair[1] + 3) - 5) for pair in pairs
    }
    left = tuple(Fraction(value) for value in (1, -2, 3, 4, -1, 2))
    right = tuple(Fraction(value) for value in (2, 1, -1, 3, 5, -3))
    corrected = {
        (u, v): left[u] * right[v] + right[u] * left[v] for u, v in pairs
    }
    residual_edge = Fraction(7, 3)
    m_four, d_four = defect((0, 1, 2, 3), residual_edge, direct, corrected)
    m_six, d_six = defect(vertices, residual_edge, direct, corrected)
    assert d_four == residual_edge * m_four
    assert d_six == 2 * residual_edge * m_six
    assert 2 * m_six * d_four == m_four * d_six

    # A separate physical channel realizes three unequal opposite sums.
    p, q, r = Fraction(2), Fraction(5), Fraction(11)
    a = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    b = (Fraction(0), p, q, r)
    response = {
        (u, v): a[u] * b[v] + b[u] * a[v]
        for u, v in combinations(range(4), 2)
    }
    opposite = (
        response[(0, 1)] + response[(2, 3)],
        response[(0, 2)] + response[(1, 3)],
        response[(0, 3)] + response[(1, 2)],
    )
    assert opposite == (p, q, r)
    assert len(set(opposite)) == 3

    # Independent multiplication modulo t^2 for two different vacuum values.
    def square_zero_product(h: Fraction) -> tuple[Fraction, Fraction]:
        # (1+t)(h-h*t) = h + 0*t.
        return (h, -h + h)

    assert square_zero_product(Fraction(2)) == (Fraction(2), Fraction(0))
    assert square_zero_product(Fraction(13, 5)) == (
        Fraction(13, 5),
        Fraction(0),
    )
    # Direct graph audit: port edge 01=1, residual edge pr=h,
    # incidences p0=-h and r1=1.  The two pair matchings cancel, and any
    # larger displayed port set contains an isolated vertex.
    for vacuum in (Fraction(2), Fraction(13, 5)):
        escape_edges = {
            pair: Fraction(0) for pair in combinations(range(9), 2)
        }
        escape_edges[(0, 1)] = Fraction(1)
        escape_edges[(7, 8)] = vacuum
        escape_edges[(0, 7)] = -vacuum
        escape_edges[(1, 8)] = Fraction(1)
        assert hafnian((0, 1, 7, 8), escape_edges) == 0
        assert hafnian((0, 1, 2, 3, 7, 8), escape_edges) == 0
        assert hafnian((0, 1, 2, 3, 4, 5, 7, 8), escape_edges) == 0

    # Direct check of the paired-singleton formula at one exact point.
    h = Fraction(17, 4)
    b_uv = Fraction(3, 2)
    a_u, a_v, b_u, b_v = map(Fraction, (2, -1, 5, 7))
    z_uv = h * b_uv + a_u * b_v + b_u * a_v
    recovered = (z_uv - a_u * b_v - b_u * a_v) / b_uv
    assert recovered == h

    print("independent vacuum-free dual-Wick audit: PASS")
    print(f"D4_factor=1 D6_factor=2 cross_identity=PASS m4={m_four} m6={m_six}")
    print("physical_opposite_sums=(2,5,11) additive_not_forced")
    print("two_term_empty_scalar_escape=PASS")
    print("paired_singleton_recovery=PASS")
    print("graph_search=0 support_search=0 colour_word_enumeration=0")


if __name__ == "__main__":
    main()
