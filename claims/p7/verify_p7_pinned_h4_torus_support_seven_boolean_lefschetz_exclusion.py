"""Primary exact replay for the P7 support-seven Boolean-Lefschetz exclusion."""

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(7))
PAIRS = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))
FOURS = tuple(combinations(VERTICES, 4))


def inclusion(rows: tuple[tuple[int, ...], ...], cols: tuple[tuple[int, ...], ...]) -> sp.Matrix:
    """Return the fixed subset-inclusion matrix with the displayed bases."""
    return sp.Matrix(
        [[int(set(col).issubset(row)) for col in cols] for row in rows]
    )


def weighted_multiplication(
    rows: tuple[tuple[int, ...], ...],
    cols: tuple[tuple[int, ...], ...],
    weights: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    """Matrix for multiplication by sum_i weights[i] z_i in the square-free algebra."""
    entries: list[list[sp.Expr]] = []
    for row in rows:
        row_set = set(row)
        current: list[sp.Expr] = []
        for col in cols:
            col_set = set(col)
            if col_set.issubset(row_set) and len(row_set - col_set) == 1:
                current.append(weights[next(iter(row_set - col_set))])
            else:
                current.append(sp.Integer(0))
        entries.append(current)
    return sp.Matrix(entries)


def hafnian_with_complement(
    triple: tuple[int, int, int],
    star: tuple[sp.Symbol, ...],
    edges: dict[tuple[int, int], sp.Symbol],
) -> sp.Expr:
    """Four-hafnian on the complement vertex together with a support triple."""
    a, b, c = triple
    return star[a] * edges[tuple(sorted((b, c)))] + star[b] * edges[
        tuple(sorted((a, c)))
    ] + star[c] * edges[tuple(sorted((a, b)))]


def main() -> None:
    star = sp.symbols("u0:7", nonzero=True)
    reciprocal = sp.symbols("q0:7", nonzero=True)
    edge_symbols = sp.symbols("d0:21")
    edges = dict(zip(PAIRS, edge_symbols, strict=True))

    w23 = inclusion(TRIPLES, PAIRS)
    w34 = inclusion(FOURS, TRIPLES)
    m_star_23 = weighted_multiplication(TRIPLES, PAIRS, star)
    m_reciprocal_34 = weighted_multiplication(FOURS, TRIPLES, reciprocal)

    assert w23.shape == (35, 21)
    assert w34.shape == (35, 35)
    assert w23.rank() == 21
    assert w34.rank() == 35
    assert (w23.T * w23).det() == 15 * 8**6 * 3**14
    assert w34.det() == -(2**16) * 3**6

    vertices8 = tuple(range(8))
    fours8 = tuple(combinations(vertices8, 4))
    fives8 = tuple(combinations(vertices8, 5))
    w45_8 = inclusion(fives8, fours8)
    assert w45_8.shape == (56, 70)
    assert w45_8.rank() == 56
    assert len(fours8) - w45_8.rank() == 14

    # Direct multiplication factorization L_u=m_ell^(3) m_u^(2).
    direct_operator = w34 * m_star_23
    for row_index, four in enumerate(FOURS):
        four_set = set(four)
        direct_hafnian_row = sp.expand(
            sum(
                hafnian_with_complement(
                    tuple(sorted(four_set - {omitted})), star, edges
                )
                for omitted in four
            )
        )
        factorized_row = sp.expand(
            sum(
                direct_operator[row_index, col_index] * edge_symbols[col_index]
                for col_index in range(len(PAIRS))
            )
        )
        assert sp.expand(direct_hafnian_row - factorized_row) == 0

        for col_index, pair in enumerate(PAIRS):
            expected = (
                sum(star[k] for k in four_set - set(pair))
                if set(pair).issubset(four_set)
                else 0
            )
            assert sp.expand(direct_operator[row_index, col_index] - expected) == 0

    # Diagonal conjugacy: D_{k+1}(u) W = m_u D_k(u).
    pair_products = sp.diag(*(sp.prod(star[i] for i in pair) for pair in PAIRS))
    triple_products = sp.diag(
        *(sp.prod(star[i] for i in triple) for triple in TRIPLES)
    )
    assert triple_products * w23 == m_star_23 * pair_products

    four_products_q = sp.diag(
        *(sp.prod(reciprocal[i] for i in four) for four in FOURS)
    )
    triple_products_q = sp.diag(
        *(sp.prod(reciprocal[i] for i in triple) for triple in TRIPLES)
    )
    assert four_products_q * w34 == m_reciprocal_34 * triple_products_q

    # Reciprocal-incidence factorization, with q_i=1/u_i, after clearing
    # denominators by the row product and scaling D_ab to E_ab=D_ab/(u_a u_b).
    reciprocal_operator = m_reciprocal_34 * w23
    for row_index, four in enumerate(FOURS):
        four_set = set(four)
        for col_index, pair in enumerate(PAIRS):
            pair_set = set(pair)
            if not pair_set.issubset(four_set):
                assert reciprocal_operator[row_index, col_index] == 0
                continue
            complement = tuple(sorted(four_set - pair_set))
            assert sp.expand(
                reciprocal_operator[row_index, col_index]
                - reciprocal[complement[0]]
                - reciprocal[complement[1]]
            ) == 0

            substitution = {
                reciprocal[i]: sp.Integer(1) / star[i] for i in VERTICES
            }
            cleared = sp.prod(star[i] for i in four) * (
                reciprocal_operator[row_index, col_index]
                / sp.prod(star[i] for i in pair)
            )
            expected = star[complement[0]] + star[complement[1]]
            assert sp.cancel(cleared.subs(substitution) - expected) == 0

    print("PASS: universal single-complement hafnian row factorization")
    print("PASS: W_(2,3)(7) rank 21 and W_(3,4)(7) rank 35")
    print(f"det Gram(W23)={15 * 8**6 * 3**14}")
    print(f"det W34={-(2**16) * 3**6}")
    print("PASS: direct and reciprocal Boolean-Lefschetz factorizations")
    print("CONCLUSION: P7 full-edge-torus support-seven circuits are impossible")
    print("PASS: the support-eight primitive Boolean space has dimension 14")
    print("BOUNDARY: its edge-torus intersection and P7 target realizability remain UNKNOWN")


if __name__ == "__main__":
    main()
