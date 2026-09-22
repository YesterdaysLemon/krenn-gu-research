#!/usr/bin/env python3
"""Replay the protected one-paired-minority formula with formal monomials.

The mathematical identity is all-order and is proved by the associated
counting argument.  This verifier exhausts every applicable ``n=8``
word/majority pair and performs a deterministic exact sample at ``n=12``.
It is finite corroboration, not an exhaustive all-order proof.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from random import Random


Symbol = tuple[int, int, int, int]
Monomial = tuple[Symbol, ...]
Polynomial = Counter[Monomial]


def protected_partner(color: int, vertex: int) -> int:
    """Return the partner of ``vertex`` in its component's ``M_color``."""

    return vertex ^ (color + 1)


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield every ordinary perfect matching of ``vertices``."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def edge_symbol(u: int, v: int, color_u: int, color_v: int) -> Monomial | None:
    """Return the formal factor for one physical scalar edge.

    Protected unit entries contribute the empty monomial.  Every allowed
    crossing scalar entry receives its own symbol.
    """

    if u > v:
        u, v, color_u, color_v = v, u, color_v, color_u
    if u // 4 == v // 4:
        protected_color = (u ^ v) - 1
        return () if color_u == color_v == protected_color else None
    if color_u == color_v:
        return None
    return ((u, v, color_u, color_v),)


def multiply_terms(*parts: Monomial | None) -> Monomial | None:
    """Multiply formal squarefree physical-entry monomials."""

    factors: list[Symbol] = []
    for part in parts:
        if part is None:
            return None
        factors.extend(part)
    return tuple(sorted(factors))


def permanent_terms(
    rows: tuple[int, ...], columns: tuple[int, ...], word: tuple[int, ...]
) -> Polynomial:
    """Return the complete formal permanent expansion for a rectangular view."""

    if not rows:
        return Counter({(): 1})
    result: Polynomial = Counter()
    first = rows[0]
    for index, column in enumerate(columns):
        factor = edge_symbol(first, column, word[first], word[column])
        if factor is None:
            continue
        remainder = columns[:index] + columns[index + 1 :]
        for term, multiplicity in permanent_terms(rows[1:], remainder, word).items():
            product_term = multiply_terms(factor, term)
            assert product_term is not None
            result[product_term] += multiplicity
    return result


def physical_terms(word: tuple[int, ...]) -> Polynomial:
    """Enumerate every literal protected-scaffold perfect-matching monomial."""

    result: Polynomial = Counter()
    for matching in perfect_matchings(tuple(range(len(word)))):
        term: Monomial | None = ()
        for u, v in matching:
            term = multiply_terms(term, edge_symbol(u, v, word[u], word[v]))
            if term is None:
                break
        if term is not None:
            result[term] += 1
    return result


def collision_count(word: tuple[int, ...], majority: int) -> int:
    """Count protected ``M_majority`` pairs with two minority endpoints."""

    return sum(
        word[u] != majority and word[protected_partner(majority, u)] != majority
        for u in range(len(word))
        if u < protected_partner(majority, u)
    )


def one_pair_formula_terms(word: tuple[int, ...], majority: int) -> Polynomial:
    """Expand the exact common-minor formula for ``q_majority(word)=1``."""

    minority = tuple(v for v, color in enumerate(word) if color != majority)
    complete_pairs = [
        (u, protected_partner(majority, u))
        for u in range(len(word))
        if u < protected_partner(majority, u)
        and word[u] != majority
        and word[protected_partner(majority, u)] != majority
    ]
    if len(complete_pairs) != 1:
        raise ValueError("one-pair formula requires collision count one")
    x, y = complete_pairs[0]
    independent = tuple(v for v in minority if v not in (x, y))
    partner_columns = tuple(protected_partner(majority, v) for v in independent)
    resources = tuple(
        (u, protected_partner(majority, u))
        for u in range(len(word))
        if u < protected_partner(majority, u)
        and word[u] == word[protected_partner(majority, u)] == majority
    )

    result: Polynomial = Counter()
    for left_index, r in enumerate(minority):
        for s in minority[left_index + 1 :]:
            rows = tuple(v for v in minority if v not in (r, s))
            cofactor = permanent_terms(rows, partner_columns, word)

            direct = edge_symbol(r, s, word[r], word[s])
            if direct is not None:
                for term, multiplicity in cofactor.items():
                    product_term = multiply_terms(term, direct)
                    assert product_term is not None
                    result[product_term] += multiplicity

            for u, v in resources:
                for first, second in ((u, v), (v, u)):
                    closure = multiply_terms(
                        edge_symbol(r, first, word[r], majority),
                        edge_symbol(s, second, word[s], majority),
                    )
                    if closure is None:
                        continue
                    for term, multiplicity in cofactor.items():
                        product_term = multiply_terms(term, closure)
                        assert product_term is not None
                        result[product_term] += multiplicity
    return result


def one_pair_word_majorities(components: int):
    """Yield all word/majority pairs with collision count one."""

    vertex_count = 4 * components
    for word in product(range(3), repeat=vertex_count):
        for majority in range(3):
            if collision_count(word, majority) == 1:
                yield word, majority


def replay() -> dict[str, int | str]:
    """Run the exhaustive ``n=8`` and deterministic sampled ``n=12`` checks."""

    exhaustive = 0
    for word, majority in one_pair_word_majorities(2):
        assert physical_terms(word) == one_pair_formula_terms(word, majority)
        exhaustive += 1
    assert exhaustive == 6000

    generator = Random(20260922)
    sampled = 0
    while sampled < 60:
        word = tuple(generator.randrange(3) for _ in range(12))
        for majority in range(3):
            if collision_count(word, majority) != 1:
                continue
            assert physical_terms(word) == one_pair_formula_terms(word, majority)
            sampled += 1
            if sampled == 60:
                break
    assert sampled == 60

    return {
        "n8_word_majorities_exhausted": exhaustive,
        "n12_word_majorities_sampled": sampled,
        "status": "EXACT_PROTECTED_ONE_PAIR_FORMULA_PASS",
    }


def main() -> None:
    receipt = replay()
    for key, value in receipt.items():
        print(key, value)


if __name__ == "__main__":
    main()
