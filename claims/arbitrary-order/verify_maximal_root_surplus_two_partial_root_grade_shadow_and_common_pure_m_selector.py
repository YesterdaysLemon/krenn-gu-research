"""Focused exact checks for the GLS17 partial-root leading-shadow theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations


def partial_matchings(vertices: tuple[int, ...], edge_count: int):
    if edge_count == 0:
        yield ()
        return
    if len(vertices) < 2 * edge_count:
        return
    first = vertices[0]
    # The first vertex may remain outside-matched.
    yield from partial_matchings(vertices[1:], edge_count)
    for index, other in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in partial_matchings(remainder, edge_count - 1):
            yield ((first, other),) + tail


def companion_signatures(order: int, grade: int, outside: tuple[str, ...]):
    roots = tuple(range(order))
    signatures = set()
    for edges in partial_matchings(roots, grade):
        used = {vertex for edge in edges for vertex in edge}
        free = tuple(root for root in roots if root not in used)
        assert len(free) == len(outside)
        for image in permutations(outside):
            assignment = tuple(sorted(zip(free, image, strict=True)))
            signatures.add((tuple(sorted(edges)), assignment))
    return signatures


def survives(signature, open_roots: frozenset[int]) -> bool:
    edges, _assignment = signature
    return all(open_roots.intersection(edge) for edge in edges)


def leading_formula_signatures(
    order: int, open_roots: tuple[int, ...], outside: tuple[str, ...]
):
    open_set = frozenset(open_roots)
    closed = tuple(root for root in range(order) if root not in open_set)
    signatures = set()
    for partners in permutations(closed, len(open_roots)):
        edges = tuple(sorted(tuple(sorted(pair)) for pair in zip(open_roots, partners)))
        used = open_set | frozenset(partners)
        free = tuple(root for root in range(order) if root not in used)
        for image in permutations(outside):
            assignment = tuple(sorted(zip(free, image, strict=True)))
            signatures.add((edges, assignment))
    return signatures


def check_leading_formula():
    records = {}
    for order in range(2, 8):
        order_records = []
        for target_half_size in range(1, order // 2 + 1):
            grade_m = target_half_size - 1
            grade_z = target_half_size
            complement_size = order - 2 * target_half_size
            outside_m = ("q0", "q1") + tuple(f"c{i}" for i in range(complement_size))
            outside_z = tuple(f"c{i}" for i in range(complement_size))
            m_signatures = companion_signatures(order, grade_m, outside_m)
            z_signatures = companion_signatures(order, grade_z, outside_z)
            for open_roots in combinations(range(order), grade_m):
                open_set = frozenset(open_roots)
                surviving_m = {
                    signature
                    for signature in m_signatures
                    if survives(signature, open_set)
                }
                formula = leading_formula_signatures(
                    order, tuple(open_roots), outside_m
                )
                assert surviving_m == formula
                assert not any(
                    survives(signature, open_set) for signature in z_signatures
                )
                order_records.append(
                    (target_half_size, tuple(open_roots), len(surviving_m))
                )
        records[order] = order_records
    return records


def check_grade_cutoff():
    checks = 0
    profiles = {}
    for order in range(2, 8):
        for target_half_size in range(1, order // 2 + 1):
            open_count = target_half_size - 1
            open_set = frozenset(range(open_count))
            profile = []
            for grade in range(order // 2 + 1):
                outside_size = order - 2 * grade
                signatures = companion_signatures(
                    order, grade, tuple(f"d{i}" for i in range(outside_size))
                )
                survivor_count = sum(
                    survives(signature, open_set) for signature in signatures
                )
                if grade >= target_half_size:
                    assert survivor_count == 0
                profile.append(survivor_count)
                checks += len(signatures)
            profiles[order, target_half_size] = tuple(profile)
    return checks, profiles


def normalize(delta: int, eta: int):
    if delta:
        return Fraction(1), Fraction(eta, delta)
    return Fraction(0), Fraction(1)


def check_operator_implications():
    lines = {
        normalize(delta, eta)
        for delta in range(-3, 4)
        for eta in range(-3, 4)
        if delta or eta
    }
    pure_m = (Fraction(1), Fraction(0))
    cases = 0
    for rank in (0, 1, 2):
        for line in lines:
            for leading in (Fraction(0), Fraction(1), Fraction(-2)):
                if rank == 0:
                    allowed = leading == 0
                elif rank == 1:
                    allowed = line[1] * leading == 0
                else:
                    allowed = True
                if leading and allowed:
                    assert rank == 2 or line == pure_m
                cases += 1
    # A rank-two space and every surviving rank-one space contain pure M.
    for ranks in ((1, 1, 1), (1, 2, 1), (2, 2, 2)):
        spaces = [lines if rank == 2 else {pure_m} for rank in ranks]
        assert pure_m in set.intersection(*spaces)
    return cases, len(lines)


def check_four_root_formula():
    order = 4
    target_half_size = 2
    outside = ("q0", "q1")
    all_counts = {}
    for open_root in range(order):
        signatures = companion_signatures(order, target_half_size - 1, outside)
        surviving = {
            signature
            for signature in signatures
            if survives(signature, frozenset({open_root}))
        }
        formula = leading_formula_signatures(order, (open_root,), outside)
        assert surviving == formula
        assert len(surviving) == 6
        all_counts[open_root] = len(surviving)
    return all_counts


def main() -> None:
    leading_records = check_leading_formula()
    grade_checks, grade_profiles = check_grade_cutoff()
    operator_cases = check_operator_implications()
    four_root_counts = check_four_root_formula()
    compact_records = {
        order: sum(len(entry) > 0 for entry in records)
        for order, records in leading_records.items()
    }
    print("partial-root grade shadow and common pure-M checks: PASS")
    print("  root-order leading-shadow cases:", compact_records)
    print("  exact companion signatures checked:", grade_checks)
    print("  grade survivor profiles:", grade_profiles)
    print("  projective rank cases / lines:", operator_cases)
    print("  r=4 four-port leading monomials per open root:", four_root_counts)
    print("  scope: conditional leading survival; activity and node closure stay open")


if __name__ == "__main__":
    main()
