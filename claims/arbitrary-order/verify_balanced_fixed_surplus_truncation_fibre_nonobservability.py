"""Focused exact checks for balanced fixed-surplus truncation.

The arbitrary-order proofs are written in the owning theorem note.  This
script checks bounded matching bijections, parity boundaries, initial-word
coefficients, and multiplicity constants.  It is not an independent audit,
a graph-family search, or a proof of the global Krenn--Gu conjecture.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb, factorial

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


@lru_cache(None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Return all perfect matchings of a labelled complete graph."""
    if not vertices:
        return ((),)
    if len(vertices) % 2:
        return ()
    u = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append((edge(u, v),) + tail)
    return tuple(result)


def subsets_of_size(vertices: tuple[int, ...], size: int):
    yield from combinations(vertices, size)


def even_subsets(vertices: tuple[int, ...]):
    for size in range(0, len(vertices) + 1, 2):
        yield from subsets_of_size(vertices, size)


def mate_map(matching: Matching) -> dict[int, int]:
    mates: dict[int, int] = {}
    for u, v in matching:
        mates[u] = v
        mates[v] = u
    return mates


def odd_double_factorial(value: int) -> int:
    if value in (-1, 0):
        return 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def check_balanced_regrouping() -> None:
    """Compare the contracted balanced ledger with direct matchings."""
    cases = ((2, 0), (3, 1), (4, 1), (2, 2), (3, 2))
    for r, q in cases:
        roots = tuple(range(r))
        blockers = tuple(range(r, 2 * r + 2 * q))
        shore_q = blockers[:q]
        nonroots = blockers[q:]
        balanced_roots = tuple(sorted(roots + shore_q))
        vertices = tuple(sorted(roots + blockers))

        direct: Counter[Matching] = Counter()
        for matching in perfect_matchings(vertices):
            if any(u in roots and v in roots for u, v in matching):
                continue
            direct[tuple(sorted(matching))] += 1

        regrouped: Counter[Matching] = Counter()
        observed_depths: set[int] = set()
        for internal_tuple in even_subsets(nonroots):
            internal = set(internal_tuple)
            cross_shore = tuple(v for v in nonroots if v not in internal)
            companion_vertices = tuple(sorted(balanced_roots + cross_shore))
            for companion in perfect_matchings(companion_vertices):
                mates = mate_map(companion)
                if any(mates[v] not in balanced_roots for v in cross_shore):
                    continue
                if any(u in roots and v in roots for u, v in companion):
                    continue
                observed_depths.add(len(internal))
                assert len(internal) <= 2 * q
                for residue in perfect_matchings(tuple(sorted(internal))):
                    matching = tuple(sorted(companion + residue))
                    regrouped[matching] += 1

        assert direct == regrouped
        assert all(multiplicity == 1 for multiplicity in regrouped.values())
        assert all(depth <= 2 * q for depth in observed_depths)


def check_parity_and_rank_counts() -> None:
    for r in range(2, 11):
        for q in range(11):
            m = r + q
            column_count = 2 ** (m - 1)
            surviving_count = sum(
                comb(m, 2 * j) for j in range(min(q, m // 2) + 1)
            )
            largest_even = 2 * (m // 2)
            has_forced_zero_column = largest_even > 2 * q
            assert has_forced_zero_column == (r >= q + 2)
            assert surviving_count <= column_count

            if r == q + 1:
                assert largest_even == 2 * q
                if q >= 1:
                    assert 3**q < column_count == 4**q

            if r >= 3 and q <= r:
                assert 3**q < column_count


def all_cross_cut_count(
    matching: Matching,
    roots: tuple[int, ...],
    blockers: tuple[int, ...],
    q: int,
) -> int:
    count = 0
    roots_set = set(roots)
    for shore_q_tuple in subsets_of_size(blockers, q):
        shore_q = set(shore_q_tuple)
        balanced_roots = roots_set | shore_q
        nonroots = set(blockers) - shore_q
        if all(
            (u in balanced_roots and v in nonroots)
            or (v in balanced_roots and u in nonroots)
            for u, v in matching
        ):
            count += 1
    return count


def check_top_cut_multiplicity() -> None:
    for r, q in ((2, 0), (3, 1), (2, 2), (3, 2)):
        roots = tuple(range(r))
        blockers = tuple(range(r, 2 * r + 2 * q))
        vertices = tuple(sorted(roots + blockers))
        for matching in perfect_matchings(vertices):
            if any(u in roots and v in roots for u, v in matching):
                continue
            assert all_cross_cut_count(matching, roots, blockers, q) == 2**q


def check_q0_initial_words() -> None:
    for r in range(2, 7):
        roots = tuple(range(r))
        nonroots = tuple(range(r, 2 * r))
        for internal_tuple in even_subsets(nonroots):
            internal = set(internal_tuple)
            cross_shore = tuple(v for v in nonroots if v not in internal)
            vertices = tuple(sorted(roots + cross_shore))
            selected = 0
            b_roots = {v - r for v in internal}
            for matching in perfect_matchings(vertices):
                mates = mate_map(matching)
                if any(mates[v] not in roots for v in cross_shore):
                    continue
                valid = True
                letters: dict[int, str] = {}
                lambda_degree = 0
                mu_degree = 0
                for u, v in matching:
                    if u in roots and v in roots:
                        letters[u] = "b"
                        letters[v] = "b"
                        mu_degree += 1
                    else:
                        root = u if u in roots else v
                        nonroot = v if u in roots else u
                        if nonroot != r + root:
                            valid = False
                            break
                        letters[root] = "a"
                        lambda_degree += 1
                if not valid:
                    continue
                if {root for root, letter in letters.items() if letter == "b"} != b_roots:
                    continue
                assert lambda_degree == r - len(internal)
                assert mu_degree == len(internal) // 2
                selected += 1
            assert selected == odd_double_factorial(len(internal) - 1)


def q1_selected_terms(
    matching: Matching,
    r: int,
    q_root: int,
    special_v: int,
) -> list[tuple[int, int, dict[int, str]]]:
    """Expand only terms visible in the selected binary tensor rows."""
    u_vertex = {r + 2 + index: index for index in range(r)}
    states: list[tuple[int, int, dict[int, str]]] = [(0, 0, {})]
    for left, right in matching:
        if left < r and right < r:
            edge_states = [(1, 0, {left: "b", right: "b"})]
        elif left < r and right == q_root:
            edge_states = [(1, 1, {left: "b", q_root: "b"})]
        elif left == q_root and right == special_v:
            edge_states = [(0, 0, {q_root: "a"})]
        elif left == q_root and right in u_vertex:
            edge_states = [
                (0, 0, {q_root: "a"}),
                (0, 0, {q_root: "b"}),
            ]
        else:
            old_root = left if left < r else right if right < r else None
            nonroot = right if left < r else left
            if old_root is None or nonroot not in u_vertex:
                return []
            if u_vertex[nonroot] != old_root:
                return []
            edge_states = [(1, 0, {old_root: "a"})]

        next_states: list[tuple[int, int, dict[int, str]]] = []
        for lambda_degree, mu_degree, letters in states:
            for edge_lambda, edge_mu, edge_letters in edge_states:
                if set(letters) & set(edge_letters):
                    continue
                next_states.append(
                    (
                        lambda_degree + edge_lambda,
                        mu_degree + edge_mu,
                        letters | edge_letters,
                    )
                )
        states = next_states
    return states


def check_q1_initial_words() -> None:
    for r in range(3, 6):
        roots = tuple(range(r))
        q_root = r
        special_v = r + 1
        u_vertices = tuple(r + 2 + index for index in range(r))
        nonroots = (special_v,) + u_vertices
        balanced_roots = roots + (q_root,)

        for internal_tuple in even_subsets(nonroots):
            internal = set(internal_tuple)
            cross_shore = tuple(v for v in nonroots if v not in internal)
            vertices = tuple(sorted(balanced_roots + cross_shore))
            desired = {
                root: ("b" if u_vertices[root] in internal else "a")
                for root in roots
            }
            desired[q_root] = "b" if special_v in internal else "a"

            degrees: Counter[tuple[int, int]] = Counter()
            for matching in perfect_matchings(vertices):
                mates = mate_map(matching)
                if any(mates[v] not in balanced_roots for v in cross_shore):
                    continue
                for lambda_degree, mu_degree, letters in q1_selected_terms(
                    matching, r, q_root, special_v
                ):
                    if letters == desired:
                        degrees[(lambda_degree, mu_degree)] += 1

            assert degrees
            maximal_lambda = max(lambda_degree for lambda_degree, _ in degrees)
            minimal_mu = min(
                mu_degree
                for lambda_degree, mu_degree in degrees
                if lambda_degree == maximal_lambda
            )
            if special_v not in internal:
                expected_lambda = r - len(internal) // 2
                expected_mu = 0
            else:
                expected_lambda = r - len(internal) // 2 + 1
                expected_mu = 1
            assert (maximal_lambda, minimal_mu) == (expected_lambda, expected_mu)
            assert degrees[(maximal_lambda, minimal_mu)] == odd_double_factorial(
                len(internal) - 1
            )


def check_wick_and_absorption_multiplicities() -> None:
    for q in range(1, 5):
        vertices = tuple(range(2 * q))
        shore_a = set(vertices[:q])
        crossing = 0
        for matching in perfect_matchings(vertices):
            if all((u in shore_a) != (v in shore_a) for u, v in matching):
                crossing += 1
        assert crossing == factorial(q)

    for q in range(4):
        for p in range(3):
            edge_count = q + p + 1
            vertices = tuple(range(2 * edge_count))
            hafnian_count = len(perfect_matchings(vertices))
            pointed_count = 0
            for u, v in combinations(vertices, 2):
                residue = tuple(w for w in vertices if w not in {u, v})
                pointed_count += len(perfect_matchings(residue))
            assert pointed_count == edge_count * hafnian_count


def check_hall_arithmetic() -> None:
    for r in range(2, 11):
        for q in range(1, 11):
            modes = r + 2 * q
            combined_quota_possible = 6 * q <= 2 * modes
            assert combined_quota_possible == (q <= r)

            existing_row_quota_possible = 3 * (q + 1) <= modes
            assert existing_row_quota_possible == (r >= q + 3)

            if q == r:
                assert modes == 3 * q


def main() -> None:
    check_balanced_regrouping()
    check_parity_and_rank_counts()
    check_top_cut_multiplicity()
    check_q0_initial_words()
    check_q1_initial_words()
    check_wick_and_absorption_multiplicities()
    check_hall_arithmetic()
    print("balanced fixed-surplus truncation and fibre checks: PASS")
    print("scope: bounded convention checks; arbitrary-order proof is written")
    print("independent_audit: false")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
