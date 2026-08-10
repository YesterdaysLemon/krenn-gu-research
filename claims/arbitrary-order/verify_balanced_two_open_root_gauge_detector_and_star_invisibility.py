"""Focused exact checks for the balanced two-open-root gauge theorem.

The arbitrary-order proofs are the written matching partition and the
sign-reversing star involution.  This script separately checks the five
two-open sectors, the repeated-row factorials, and one exact r=5 formal
star model.  It does not search graph families or prove existence of a GHZ
witness.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import factorial

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Monomial = tuple[str, ...]
Term = tuple[Matching, Edge]


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[Matching] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append((edge(first, second),) + tail)
    return tuple(answer)


def hafnian(vertices: tuple[int, ...], weight) -> int:
    if not vertices:
        return 1
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += weight(first, second) * hafnian(rest, weight)
    return total


def permanent(
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    weight,
) -> int:
    assert len(rows) == len(columns)
    if not rows:
        return 1
    first = rows[0]
    total = 0
    for position, column in enumerate(columns):
        remaining = columns[:position] + columns[position + 1 :]
        total += weight(first, column) * permanent(rows[1:], remaining, weight)
    return total


def odd_double_factorial(size: int) -> int:
    """Return (size-1)!! for an even nonnegative vertex count."""
    assert size >= 0 and size % 2 == 0
    answer = 1
    for value in range(1, size, 2):
        answer *= value
    return answer


def falling(size: int, count: int) -> int:
    if count < 0 or count > size:
        return 0
    answer = 1
    for value in range(count):
        answer *= size - value
    return answer


def check_five_sector_identity(r: int, q: int) -> dict[str, int]:
    roots = tuple(range(r))
    outside = tuple(range(r, 2 * r + 2 * q))
    i, j = 0, 1
    root_set = set(roots)
    outside_set = set(outside)

    def graph_weight(u: int, v: int) -> int:
        u, v = edge(u, v)
        if u in root_set and v in root_set:
            if u not in (i, j) and v not in (i, j):
                return 0
            return (u + 2) * (v + 5) + 3
        if u in root_set:
            return (u + 3) * (v - r + 4) + 5
        return (u - r + 2) * (v - r + 7) + 11

    def cross_weight(root: int, mode: int) -> int:
        return graph_weight(root, mode)

    def outside_weight(left: int, right: int) -> int:
        return graph_weight(left, right)

    def layer(active_roots: tuple[int, ...]) -> int:
        surplus = len(outside) - len(active_roots)
        assert surplus >= 0 and surplus % 2 == 0
        total = 0
        for selected in combinations(outside, surplus):
            selected_set = set(selected)
            columns = tuple(mode for mode in outside if mode not in selected_set)
            total += hafnian(selected, outside_weight) * permanent(
                active_roots,
                columns,
                cross_weight,
            )
        return total

    direct = hafnian(roots + outside, graph_weight)
    both_outside = layer(roots)
    together = graph_weight(i, j) * layer(tuple(s for s in roots if s not in (i, j)))

    i_fixed = 0
    j_fixed = 0
    other_roots = tuple(s for s in roots if s not in (i, j))
    for s in other_roots:
        i_fixed += graph_weight(i, s) * layer(
            tuple(root for root in roots if root not in (i, s))
        )
        j_fixed += graph_weight(j, s) * layer(
            tuple(root for root in roots if root not in (j, s))
        )

    both_fixed = 0
    for s in other_roots:
        for t in other_roots:
            if s == t:
                continue
            both_fixed += graph_weight(i, s) * graph_weight(j, t) * layer(
                tuple(root for root in roots if root not in (i, j, s, t))
            )

    sector_total = both_outside + together + i_fixed + j_fixed + both_fixed
    assert direct == sector_total

    counts: Counter[str] = Counter()
    for matching in perfect_matchings(roots + outside):
        if any(graph_weight(*pair) == 0 for pair in matching):
            continue
        partners: dict[int, int] = {}
        for left, right in matching:
            partners[left] = right
            partners[right] = left
        partner_i = partners[i]
        partner_j = partners[j]
        if partner_i in outside_set and partner_j in outside_set:
            counts["both_outside"] += 1
        elif partner_i == j:
            counts["together"] += 1
        elif partner_i in root_set and partner_j in outside_set:
            counts["i_fixed"] += 1
        elif partner_i in outside_set and partner_j in root_set:
            counts["j_fixed"] += 1
        else:
            assert partner_i in root_set and partner_j in root_set
            assert partner_i != partner_j
            counts["both_fixed"] += 1

    mode_count = len(outside)

    def unit_layer(active_count: int) -> int:
        if active_count < 0:
            return 0
        return falling(mode_count, active_count) * odd_double_factorial(
            mode_count - active_count
        )

    expected = {
        "both_outside": unit_layer(r),
        "together": unit_layer(r - 2),
        "i_fixed": (r - 2) * unit_layer(r - 2),
        "j_fixed": (r - 2) * unit_layer(r - 2),
        "both_fixed": (r - 2) * (r - 3) * unit_layer(r - 4),
    }
    assert dict(counts) == {name: value for name, value in expected.items() if value}
    return expected


def check_sector_bijections() -> None:
    summaries = {
        (r, q): check_five_sector_identity(r, q)
        for r, q in ((4, 0), (3, 1), (4, 1))
    }
    assert summaries[(4, 0)]["both_fixed"] > 0
    assert summaries[(3, 1)]["both_fixed"] == 0


def row_permanent(rows: tuple[tuple[int, ...], ...]) -> int:
    if not rows:
        return 1
    columns = tuple(range(len(rows)))
    return permanent(
        tuple(range(len(rows))),
        columns,
        lambda row, column: rows[row][column],
    )


def wick_hafnian(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    assert len(a) == len(b) and len(a) % 2 == 0
    modes = tuple(range(len(a)))
    return hafnian(
        modes,
        lambda left, right: a[left] * b[right] + b[left] * a[right],
    )


def check_wick_factorials() -> None:
    for q in range(5):
        size = 2 * q
        modes = tuple(range(size))
        a = tuple(2 * mode + 1 for mode in modes)
        b = tuple(mode * mode + 3 for mode in modes)

        direct = wick_hafnian(a, b)
        repeated_rows = tuple(a for _ in range(q)) + tuple(b for _ in range(q))
        labelled = row_permanent(repeated_rows)
        assert labelled == factorial(q) * direct

    # The companion sector uses q+1 repeated rows of each type.
    for q in range(4):
        size = 2 * (q + 1)
        modes = tuple(range(size))
        a = tuple(mode + 2 for mode in modes)
        b = tuple(3 * mode + 1 for mode in modes)

        direct = wick_hafnian(a, b)
        rows = tuple(a for _ in range(q + 1)) + tuple(b for _ in range(q + 1))
        assert row_permanent(rows) == factorial(q + 1) * direct


def multiply_monomials(*parts: Monomial) -> Monomial:
    return tuple(sorted(symbol for part in parts for symbol in part))


def check_star_involution() -> None:
    r = 5
    roots = tuple(range(r))
    outside = tuple(range(r, 2 * r))
    i, j = 0, 1
    u_0 = outside[0]
    root_set = set(roots)
    outside_set = set(outside)

    def base_term(pair: Edge) -> Monomial | None:
        left, right = pair
        if left in root_set and right in root_set:
            return (f"rr_{left}_{right}",)
        if left in root_set and right in outside_set:
            mode = right - r
            if left == j:
                return ("eta", f"b_{mode}")
            return (f"h_{left}_{mode}",)
        if left in outside_set and right in outside_set:
            if u_0 not in pair:
                return None
            other = right if left == u_0 else left
            return ("a_0", f"b_{other - r}")
        raise AssertionError("unexpected vertex classes")

    delta_terms: dict[Edge, tuple[int, Monomial]] = {
        edge(i, u_0): (1, ("kappa", "a_0")),
        edge(i, j): (-1, ("kappa", "eta")),
    }

    def term_data(term: Term) -> tuple[int, Monomial] | None:
        matching, delta_edge = term
        sign, delta_monomial = delta_terms[delta_edge]
        pieces = [delta_monomial]
        for pair in matching:
            if pair == delta_edge:
                continue
            current = base_term(pair)
            if current is None:
                return None
            pieces.append(current)
        return sign, multiply_monomials(*pieces)

    terms: set[Term] = set()
    coefficient: Counter[Monomial] = Counter()
    for matching in perfect_matchings(roots + outside):
        for delta_edge in delta_terms:
            if delta_edge not in matching:
                continue
            term = (tuple(sorted(matching)), delta_edge)
            data = term_data(term)
            if data is None:
                continue
            sign, monomial = data
            terms.add(term)
            coefficient[monomial] += sign

    assert not {monomial: value for monomial, value in coefficient.items() if value}
    assert len(terms) == 48

    def partner(term: Term) -> Term:
        matching, delta_edge = term
        pairs = set(matching)
        if delta_edge == edge(i, u_0):
            j_edge = next(pair for pair in pairs if j in pair)
            v = j_edge[1] if j_edge[0] == j else j_edge[0]
            assert v in outside_set and v != u_0
            pairs.remove(delta_edge)
            pairs.remove(j_edge)
            pairs.add(edge(i, j))
            pairs.add(edge(u_0, v))
            return tuple(sorted(pairs)), edge(i, j)

        assert delta_edge == edge(i, j)
        star_edge = next(
            pair
            for pair in pairs
            if pair != delta_edge
            and pair[0] in outside_set
            and pair[1] in outside_set
            and u_0 in pair
        )
        v = star_edge[1] if star_edge[0] == u_0 else star_edge[0]
        pairs.remove(delta_edge)
        pairs.remove(star_edge)
        pairs.add(edge(i, u_0))
        pairs.add(edge(j, v))
        return tuple(sorted(pairs)), edge(i, u_0)

    for term in terms:
        paired = partner(term)
        assert paired in terms
        assert partner(paired) == term
        data = term_data(term)
        paired_data = term_data(paired)
        assert data is not None and paired_data is not None
        sign, monomial = data
        paired_sign, paired_monomial = paired_data
        assert sign == -paired_sign
        assert monomial == paired_monomial

    # Two one-mode-supported a rows cannot be assigned injectively.
    a = (7, 0, 0, 0, 0)
    other_rows = tuple(
        tuple((row + 2) * (column + 3) + 1 for column in range(r))
        for row in range(r - 2)
    )
    assert row_permanent((a, a) + other_rows) == 0


def main() -> None:
    check_sector_bijections()
    check_wick_factorials()
    check_star_involution()
    print("balanced two-open-root gauge focused checks: PASS")
    print("five-sector matching partitions: r=3,4 and q=0,1")
    print("Wick repeated-row factorials: q=0,...,4")
    print("formal r=5 star involution terms: 48")
    print("tight_layer_or_GHZ_witness_constructed: false")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
