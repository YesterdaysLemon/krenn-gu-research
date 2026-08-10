"""Independent exact audit of the balanced two-open gauge boundary.

This no-import audit uses labelled bitmask matchings and formal commutative
monomial ledgers.  It is bounded convention evidence, not a proof of the
arbitrary-order theorem and not evidence for a Krenn--Gu witness.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Iterator
from functools import lru_cache
from itertools import permutations
from math import factorial


Vertex = tuple[str, int]
Pair = tuple[Vertex, Vertex]
Matching = tuple[Pair, ...]
Monomial = tuple[str, ...]
Polynomial = Counter[Monomial]
Term = tuple[int, Monomial]


def ordered_pair(left: Vertex, right: Vertex) -> Pair:
    return (left, right) if left < right else (right, left)


def labelled_matchings(
    vertices: tuple[Vertex, ...],
    allowed: Callable[[Vertex, Vertex], bool] | None = None,
) -> Iterator[Matching]:
    """Generate matchings by a cached integer-mask recurrence."""

    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[Matching, ...]:
        if mask == 0:
            return ((),)
        first_bit = mask & -mask
        first_index = first_bit.bit_length() - 1
        first = vertices[first_index]
        rest = mask ^ first_bit
        results: list[Matching] = []
        candidates = rest
        while candidates:
            partner_bit = candidates & -candidates
            partner_index = partner_bit.bit_length() - 1
            partner = vertices[partner_index]
            candidates ^= partner_bit
            if allowed is not None and not allowed(first, partner):
                continue
            for tail in solve(rest ^ partner_bit):
                results.append((ordered_pair(first, partner),) + tail)
        return tuple(results)

    yield from solve((1 << len(vertices)) - 1)


def partner_map(matching: Matching) -> dict[Vertex, Vertex]:
    result: dict[Vertex, Vertex] = {}
    for left, right in matching:
        result[left] = right
        result[right] = left
    return result


def matching_key(matching: Matching) -> frozenset[Pair]:
    return frozenset(ordered_pair(left, right) for left, right in matching)


def matching_product(edge_terms: Iterable[list[Term]]) -> Polynomial:
    result: Polynomial = Counter({(): 1})
    for terms in edge_terms:
        next_result: Polynomial = Counter()
        for old_monomial, old_coefficient in result.items():
            for coefficient, monomial in terms:
                next_result[tuple(sorted(old_monomial + monomial))] += (
                    old_coefficient * coefficient
                )
        result = Counter(
            {
                monomial: coefficient
                for monomial, coefficient in next_result.items()
                if coefficient
            }
        )
        if not result:
            break
    return result


def add_polynomial(target: Polynomial, source: Polynomial) -> None:
    target.update(source)
    for monomial in tuple(target):
        if target[monomial] == 0:
            del target[monomial]


def scaled(polynomial: Polynomial, divisor: int) -> Polynomial:
    assert divisor > 0
    assert all(coefficient % divisor == 0 for coefficient in polynomial.values())
    return Counter(
        {
            monomial: coefficient // divisor
            for monomial, coefficient in polynomial.items()
            if coefficient
        }
    )


def sector_name_and_label(
    matching: Matching, roots: tuple[Vertex, ...]
) -> tuple[str, tuple[int, ...]]:
    i_root, j_root = roots[:2]
    partners = partner_map(matching)
    i_partner = partners[i_root]
    j_partner = partners[j_root]
    if i_partner[0] == "B" and j_partner[0] == "B":
        return "both_outside", ()
    if i_partner == j_root:
        return "open_pair", ()
    if i_partner[0] == "R" and j_partner[0] == "B":
        return "i_pinned", (i_partner[1],)
    if j_partner[0] == "R" and i_partner[0] == "B":
        return "j_pinned", (j_partner[1],)
    assert i_partner[0] == j_partner[0] == "R"
    assert i_partner != j_partner
    return "both_pinned", (i_partner[1], j_partner[1])


def audit_five_sector_partition(r: int, q: int) -> None:
    roots = tuple(("R", index) for index in range(r))
    outside = tuple(("B", index) for index in range(r + 2 * q))
    vertices = roots + outside

    def allowed(left: Vertex, right: Vertex) -> bool:
        if left[0] != "R" or right[0] != "R":
            return True
        return left[1] < 2 or right[1] < 2

    buckets: dict[tuple[str, tuple[int, ...]], set[frozenset[Pair]]] = defaultdict(set)
    every_matching: set[frozenset[Pair]] = set()
    outside_edge_count = {
        "both_outside": q,
        "open_pair": q + 1,
        "i_pinned": q + 1,
        "j_pinned": q + 1,
        "both_pinned": q + 2,
    }

    for matching in labelled_matchings(vertices, allowed):
        key = matching_key(matching)
        assert key not in every_matching
        every_matching.add(key)
        sector, label = sector_name_and_label(matching, roots)
        buckets[(sector, label)].add(key)
        actual_outside_edges = sum(
            left[0] == right[0] == "B" for left, right in matching
        )
        assert actual_outside_edges == outside_edge_count[sector]

        partners = partner_map(matching)
        if sector == "both_pinned":
            s_index, t_index = label
            assert partners[roots[0]] == roots[s_index]
            assert partners[roots[1]] == roots[t_index]
            assert s_index != t_index

    assert every_matching == set().union(*buckets.values())
    m = r + 2 * q
    per_label = {
        "both_outside": factorial(m) // (2**q * factorial(q)),
        "open_pair": factorial(m) // (2 ** (q + 1) * factorial(q + 1)),
        "i_pinned": factorial(m) // (2 ** (q + 1) * factorial(q + 1)),
        "j_pinned": factorial(m) // (2 ** (q + 1) * factorial(q + 1)),
        "both_pinned": factorial(m) // (2 ** (q + 2) * factorial(q + 2)),
    }
    assert len(buckets[("both_outside", ())]) == per_label["both_outside"]
    assert len(buckets[("open_pair", ())]) == per_label["open_pair"]
    pinned = range(2, r)
    for s_index in pinned:
        assert len(buckets[("i_pinned", (s_index,))]) == per_label["i_pinned"]
        assert len(buckets[("j_pinned", (s_index,))]) == per_label["j_pinned"]
    for s_index in pinned:
        for t_index in pinned:
            if s_index == t_index:
                assert ("both_pinned", (s_index, t_index)) not in buckets
                continue
            assert (
                len(buckets[("both_pinned", (s_index, t_index))])
                == per_label["both_pinned"]
            )


def outside_hafnian_ledger(order: int) -> Polynomial:
    vertices = tuple(("B", index) for index in range(order))
    result: Polynomial = Counter()
    for matching in labelled_matchings(vertices):
        terms: list[list[Term]] = []
        for (_, left), (_, right) in matching:
            terms.append(
                [
                    (1, (f"A@{left}", f"B@{right}")),
                    (1, (f"B@{left}", f"A@{right}")),
                ]
            )
        add_polynomial(result, matching_product(terms))
    return result


def permanent_ledger(rows: tuple[str, ...], outside_order: int) -> Polynomial:
    assert len(rows) == outside_order
    result: Polynomial = Counter()
    for assignment in permutations(range(outside_order)):
        monomial = tuple(
            sorted(f"{row}@{vertex}" for row, vertex in zip(rows, assignment, strict=True))
        )
        result[monomial] += 1
    return result


def audit_two_row_factorials() -> None:
    for half_order in range(4):
        order = 2 * half_order
        hafnian = outside_hafnian_ledger(order)
        permanent = permanent_ledger(
            ("A",) * half_order + ("B",) * half_order, order
        )
        assert hafnian == scaled(permanent, factorial(half_order))
        expected_coefficient = factorial(half_order)
        assert set(hafnian.values()) == {expected_coefficient}


def variation_edge_terms(left: Vertex, right: Vertex, q: int) -> list[Term]:
    if left[0] == right[0] == "B":
        u, v = left[1], right[1]
        return [
            (1, (f"A@{u}", f"B@{v}")),
            (1, (f"B@{u}", f"A@{v}")),
        ]
    if left[0] == "B":
        left, right = right, left
    if right[0] == "B":
        root, vertex = left[1], right[1]
        if root == 0:
            return [(1, (f"A@{vertex}",))]
        if root == 1:
            return [
                (1, (f"D@{vertex}",)),
                (1, ("ETA", f"B@{vertex}")),
            ]
        return [(1, (f"H{root}@{vertex}",))]

    root_left, root_right = left[1], right[1]
    if {root_left, root_right} == {0, 1}:
        return [(-(q + 1), ("ETA",))]
    if 1 in {root_left, root_right}:
        pinned = root_right if root_left == 1 else root_left
        assert pinned >= 2
        return [(1, (f"L{pinned}",))]
    return []


def expected_variation(r: int, q: int) -> Polynomial:
    outside_order = r + 2 * q
    persistent = tuple(f"H{index}" for index in range(2, r))
    defect_rows = persistent + ("A",) * (q + 1) + ("B",) * q + ("D",)
    assert len(defect_rows) == outside_order
    result = scaled(permanent_ledger(defect_rows, outside_order), factorial(q))

    for pinned in range(2, r):
        companion_rows = (
            tuple(row for row in persistent if row != f"H{pinned}")
            + ("A",) * (q + 2)
            + ("B",) * (q + 1)
        )
        assert len(companion_rows) == outside_order
        companion = scaled(
            permanent_ledger(companion_rows, outside_order), factorial(q + 1)
        )
        labelled: Polynomial = Counter()
        for monomial, coefficient in companion.items():
            labelled[tuple(sorted(monomial + (f"L{pinned}",)))] += coefficient
        add_polynomial(result, labelled)
    return result


def audit_full_variation(r: int, q: int) -> None:
    roots = tuple(("R", index) for index in range(r))
    outside = tuple(("B", index) for index in range(r + 2 * q))
    direct: Polynomial = Counter()
    companion_labels: set[int] = set()
    eta_terms_before_cancellation = 0

    for matching in labelled_matchings(roots + outside):
        terms = [variation_edge_terms(left, right, q) for left, right in matching]
        if any(not edge_expansion for edge_expansion in terms):
            continue
        contribution = matching_product(terms)
        for monomial, coefficient in contribution.items():
            if "ETA" in monomial:
                eta_terms_before_cancellation += abs(coefficient)
            for atom in monomial:
                if atom.startswith("L"):
                    companion_labels.add(int(atom[1:]))
        add_polynomial(direct, contribution)

    assert eta_terms_before_cancellation > 0
    assert all("ETA" not in monomial for monomial in direct)
    assert companion_labels == set(range(2, r))
    assert direct == expected_variation(r, q)


def star_branch_matchings(r: int, branch: str) -> tuple[Matching, ...]:
    roots = tuple(("R", index) for index in range(r))
    outside = tuple(("B", index) for index in range(r))
    i_root, j_root = roots[:2]
    u_zero = outside[0]
    if branch == "plus":
        fixed = (ordered_pair(i_root, u_zero),)
        remaining = tuple(vertex for vertex in roots + outside if vertex not in {i_root, u_zero})
    else:
        assert branch == "minus"
        fixed = (ordered_pair(i_root, j_root),)
        remaining = tuple(vertex for vertex in roots + outside if vertex not in {i_root, j_root})

    def allowed(left: Vertex, right: Vertex) -> bool:
        if left[0] == right[0] == "B":
            return 0 in {left[1], right[1]}
        return True

    return tuple(fixed + tail for tail in labelled_matchings(remaining, allowed))


def star_involution(matching: Matching, r: int) -> Matching:
    edges = set(matching_key(matching))
    i_root, j_root = ("R", 0), ("R", 1)
    u_zero = ("B", 0)
    plus_edge = ordered_pair(i_root, u_zero)
    minus_edge = ordered_pair(i_root, j_root)
    if plus_edge in edges:
        j_edge = next(edge for edge in edges if j_root in edge)
        v_vertex = j_edge[0] if j_edge[1] == j_root else j_edge[1]
        assert v_vertex[0] == "B" and v_vertex != u_zero
        edges.remove(plus_edge)
        edges.remove(j_edge)
        edges.add(minus_edge)
        edges.add(ordered_pair(u_zero, v_vertex))
    else:
        assert minus_edge in edges
        outside_edge = next(
            edge for edge in edges if edge[0][0] == edge[1][0] == "B"
        )
        assert u_zero in outside_edge
        v_vertex = outside_edge[0] if outside_edge[1] == u_zero else outside_edge[1]
        edges.remove(minus_edge)
        edges.remove(outside_edge)
        edges.add(plus_edge)
        edges.add(ordered_pair(j_root, v_vertex))
    assert len(edges) == r
    return tuple(sorted(edges))


def star_monomial(matching: Matching) -> tuple[int, Monomial]:
    coefficient = 1
    atoms: list[str] = ["K", "ETA", "A@0"]
    for left, right in matching:
        vertices = {left, right}
        if ("R", 0) in vertices:
            if ("R", 1) in vertices:
                coefficient = -1
            continue
        if left[0] == right[0] == "B":
            v_index = right[1] if left[1] == 0 else left[1]
            atoms.append(f"B@{v_index}")
            continue
        if ("R", 1) in vertices:
            vertex = right if left == ("R", 1) else left
            atoms.append(f"B@{vertex[1]}")
            continue
        root = left if left[0] == "R" else right
        vertex = right if left[0] == "R" else left
        atoms.append(f"X{root[1]}@{vertex[1]}")
    return coefficient, tuple(sorted(atoms))


def audit_star_involution(r: int) -> None:
    plus = star_branch_matchings(r, "plus")
    minus = star_branch_matchings(r, "minus")

    def contributes(matching: Matching, branch: str) -> bool:
        edges = matching_key(matching)
        root_edges = sum(left[0] == right[0] == "R" for left, right in edges)
        outside_edges = sum(left[0] == right[0] == "B" for left, right in edges)
        if branch == "plus":
            return root_edges == outside_edges == 0
        return root_edges == outside_edges == 1

    plus_live = {matching_key(matching) for matching in plus if contributes(matching, "plus")}
    minus_live = {
        matching_key(matching) for matching in minus if contributes(matching, "minus")
    }
    expected_pairs = factorial(r - 1)
    assert len(plus_live) == len(minus_live) == expected_pairs

    for key in plus_live | minus_live:
        matching = tuple(sorted(key))
        partner = star_involution(matching, r)
        partner_key = matching_key(partner)
        if key in plus_live:
            assert partner_key in minus_live
        else:
            assert partner_key in plus_live
        assert matching_key(star_involution(partner, r)) == key
        assert partner_key != key
        coefficient, monomial = star_monomial(matching)
        partner_coefficient, partner_monomial = star_monomial(partner)
        assert monomial == partner_monomial
        assert coefficient == -partner_coefficient


def main() -> None:
    for r, q in ((4, 0), (4, 1), (5, 1), (4, 2)):
        audit_five_sector_partition(r, q)
    audit_two_row_factorials()
    for r, q in ((4, 0), (4, 1), (5, 1), (4, 2)):
        audit_full_variation(r, q)
    for r in range(2, 7):
        audit_star_involution(r)

    print("independent balanced two-open gauge audit: PASS")
    print("five_sector_cases: r,q=(4,0),(4,1),(5,1),(4,2)")
    print("two_row_factorials: q=0,1,2,3")
    print("star_involution_orders: r=2,3,4,5,6")
    print("scope: bounded exact convention and multiplicity audit")
    print("imports_primary_verifier: false")
    print("is_krenn_gu_witness: false")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
