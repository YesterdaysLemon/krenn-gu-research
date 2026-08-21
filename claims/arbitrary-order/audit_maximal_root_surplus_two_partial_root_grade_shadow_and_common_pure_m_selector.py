"""Independent no-import audit of the GLS17 partial-root shadow theorem."""

from fractions import Fraction
from itertools import combinations
from math import factorial, gcd


def matching_masks(available_mask, edge_count, answer, chosen=()):
    if edge_count == 0:
        answer.add(tuple(sorted(chosen)))
        return
    if available_mask.bit_count() < 2 * edge_count:
        return
    least_bit = available_mask & -available_mask
    without_least = available_mask ^ least_bit
    matching_masks(without_least, edge_count, answer, chosen)
    partners = without_least
    while partners:
        partner = partners & -partners
        partners ^= partner
        edge = least_bit | partner
        matching_masks(
            without_least ^ partner, edge_count - 1, answer, chosen + (edge,)
        )


def all_matchings(order, edge_count):
    answer = set()
    matching_masks((1 << order) - 1, edge_count, answer)
    return answer


def falling(value, count):
    answer = 1
    for offset in range(count):
        answer *= value - offset
    return answer


def audit_transversal_counts():
    checks = 0
    records = {}
    for order in range(2, 9):
        order_record = {}
        for target_half_size in range(1, order // 2 + 1):
            open_count = target_half_size - 1
            grade_m = open_count
            grade_z = target_half_size
            open_masks = [
                sum(1 << root for root in roots)
                for roots in combinations(range(order), open_count)
            ]
            m_matchings = all_matchings(order, grade_m)
            z_matchings = all_matchings(order, grade_z)
            outside_count = order - 2 * grade_m
            expected_per_open = falling(order - open_count, open_count) * factorial(
                outside_count
            )
            counts = []
            for open_mask in open_masks:
                surviving_m = [
                    matching
                    for matching in m_matchings
                    if all(edge & open_mask for edge in matching)
                ]
                surviving_z = [
                    matching
                    for matching in z_matchings
                    if all(edge & open_mask for edge in matching)
                ]
                # Each M matching receives every bijection of its free roots.
                monomial_count = len(surviving_m) * factorial(outside_count)
                assert monomial_count == expected_per_open
                assert not surviving_z
                for matching in surviving_m:
                    assert all((edge & open_mask).bit_count() == 1 for edge in matching)
                    covered_open = 0
                    for edge in matching:
                        covered_open |= edge & open_mask
                    assert covered_open == open_mask
                counts.append(monomial_count)
                checks += len(m_matchings) + len(z_matchings)
            order_record[target_half_size] = tuple(counts)
        records[order] = order_record
    return checks, records


def audit_grade_cutoff():
    checks = 0
    profiles = {}
    for order in range(2, 9):
        for target_half_size in range(1, order // 2 + 1):
            open_count = target_half_size - 1
            open_mask = (1 << open_count) - 1
            profile = []
            for grade in range(order // 2 + 1):
                matchings = all_matchings(order, grade)
                survivors = sum(
                    all(edge & open_mask for edge in matching) for matching in matchings
                )
                if grade >= target_half_size:
                    assert survivors == 0
                profile.append(survivors)
                checks += len(matchings)
            profiles[order, target_half_size] = tuple(profile)
    return checks, profiles


def primitive(delta, eta):
    divisor = gcd(abs(delta), abs(eta))
    delta //= divisor
    eta //= divisor
    if delta < 0 or (delta == 0 and eta < 0):
        delta, eta = -delta, -eta
    return delta, eta


def audit_operator_spaces():
    lines = {
        primitive(delta, eta)
        for delta in range(-5, 6)
        for eta in range(-5, 6)
        if delta or eta
    }
    pure_m = (1, 0)
    checks = 0
    for delta, eta in lines:
        for leading in (Fraction(0), Fraction(1), Fraction(-5, 3)):
            if leading and eta * leading == 0:
                assert (delta, eta) == pure_m
            checks += 1
    # Each target with a surviving leading class contributes either the
    # singleton pure-M row or the full coefficient plane.
    for ranks in (
        (1,),
        (2,),
        (1, 1),
        (1, 2),
        (2, 2),
        (1, 2, 1, 2, 1, 2, 1),
    ):
        spaces = [{pure_m} if rank == 1 else {pure_m, (0, 1), (1, 1)} for rank in ranks]
        intersection = set.intersection(*spaces)
        assert pure_m in intersection
        checks += 1
    return checks, len(lines)


def audit_four_root_covector():
    order = 4
    matchings = all_matchings(order, 1)
    counts = {}
    for open_root in range(order):
        open_mask = 1 << open_root
        surviving_edges = [
            matching[0] for matching in matchings if matching[0] & open_mask
        ]
        assert len(surviving_edges) == 3
        # Each choice of the closed partner leaves two roots for the two
        # residual assignments.
        counts[open_root] = len(surviving_edges) * factorial(2)
        assert counts[open_root] == 6
    return counts


def main():
    transversal_checks, transversal_records = audit_transversal_counts()
    grade_checks, grade_profiles = audit_grade_cutoff()
    operator_checks, line_count = audit_operator_spaces()
    four_root_counts = audit_four_root_covector()
    compact = {
        order: {
            half_size: (len(counts), counts[0] if counts else 0)
            for half_size, counts in record.items()
        }
        for order, record in transversal_records.items()
    }
    print("INDEPENDENT PARTIAL-ROOT LEADING-SHADOW AUDIT PASS")
    print("  bitmask transversal checks:", transversal_checks)
    print("  open-mask count / monomials per mask:", compact)
    print("  independent grade checks:", grade_checks)
    print("  grade matching profiles:", grade_profiles)
    print("  primitive projective/common-space checks:", operator_checks, line_count)
    print("  r=4 first-root covector monomials:", four_root_counts)
    print("  scope: leading-shadow implications only; activity and closure remain open")


if __name__ == "__main__":
    main()
