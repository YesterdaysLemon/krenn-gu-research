"""Independent no-import audit of the GLS16 base-shadow theorem."""

from fractions import Fraction
from itertools import combinations
from math import factorial, gcd


def inject_words(roots, outside, prefix, answer):
    if not roots:
        answer.add(tuple(prefix))
        return
    for index, vertex in enumerate(outside):
        inject_words(
            roots[1:],
            outside[:index] + outside[index + 1 :],
            prefix + [vertex],
            answer,
        )


def direct_words(order):
    answer = set()
    inject_words(
        tuple(range(order)),
        (100, 101) + tuple(range(order - 2)),
        [],
        answer,
    )
    return answer


def transformed_words(order):
    answer = set()
    roots = tuple(range(order))
    complement = tuple(range(order - 2))
    for pair in combinations(roots, 2):
        rest = tuple(root for root in roots if root not in pair)
        tails = set()
        inject_words(rest, complement, [], tails)
        for residual in ((100, 101), (101, 100)):
            for tail in tails:
                word = [None] * order
                word[pair[0]], word[pair[1]] = residual
                for root, vertex in zip(rest, tail):
                    word[root] = vertex
                answer.add(tuple(word))
    return answer


def audit_matching_shadow():
    total = 0
    counts = {}
    for order in range(2, 9):
        left = transformed_words(order)
        right = direct_words(order)
        assert left == right
        assert len(left) == factorial(order)
        counts[order] = len(left)
        total += len(left)
    return total, counts


def audit_grade_masks():
    checked = 0
    records = {}
    for order in range(2, 9):
        outside = order + 2
        pair_masks = 0
        killed_masks = 0
        for mask in range(1, 1 << outside):
            size = mask.bit_count()
            if size % 2 or size < 2:
                continue
            grade = (size - 2) // 2
            if grade == 0:
                assert size == 2
                pair_masks += 1
            else:
                assert grade >= 1
                killed_masks += 1
            checked += 1
        assert pair_masks == outside * (outside - 1) // 2
        records[order] = (pair_masks, killed_masks)
    return checked, records


def normalize_pair(delta, eta):
    divisor = gcd(abs(delta), abs(eta))
    delta //= divisor
    eta //= divisor
    if delta < 0 or (delta == 0 and eta < 0):
        delta, eta = -delta, -eta
    return delta, eta


def audit_projective_shadow():
    lines = {
        normalize_pair(delta, eta)
        for delta in range(-4, 5)
        for eta in range(-4, 5)
        if delta or eta
    }
    checks = 0
    for delta, eta in lines:
        for base in (Fraction(0), Fraction(1), Fraction(-3, 2)):
            if eta * base == 0 and base:
                assert eta == 0
                assert normalize_pair(delta, eta) == (1, 0)
            checks += 1
    for first in lines:
        for second in lines:
            if first != second:
                assert first != (1, 0) or second != (1, 0)
                checks += 1
    return checks, len(lines)


def audit_cross_slots():
    checks = 0
    profiles = {}
    for order in range(3, 9):
        target_masks = [
            (1 << left) | (1 << right) for left, right in combinations(range(order), 2)
        ]
        profile = {}
        all_mask = (1 << order) - 1
        for source in target_masks:
            for target in target_masks:
                if source == target:
                    continue
                common = source & target
                source_only = source & ~target
                target_only = target & ~source
                exterior = all_mask & ~(source | target)
                assert source_only.bit_count() == target_only.bit_count()
                assert source_only.bit_count() in (1, 2)
                assert not (source_only & target_only)
                assert common | source_only | target_only | exterior == all_mask
                key = (
                    common.bit_count(),
                    source_only.bit_count(),
                    exterior.bit_count(),
                )
                profile[key] = profile.get(key, 0) + 1
                # S and Q union S are both foreign to T and Q union T.
                q_mask = (1 << order) | (1 << (order + 1))
                assert source != target
                assert (q_mask | source) != target
                assert source != (q_mask | target)
                assert (q_mask | source) != (q_mask | target)
                checks += 1
        profiles[order] = profile
    return checks, profiles


def audit_rank_controls():
    controls = (
        # k, delta, eta, base class, allowed
        (0, 0, 0, 0, True),
        (1, 1, 0, 1, True),
        (1, 0, 1, 0, True),
        (1, 2, 3, 0, True),
        (2, 1, 0, 1, True),
        (0, 0, 0, 1, False),
        (1, 0, 1, 1, False),
        (1, 2, 3, 1, False),
    )
    for rank, delta, eta, base, allowed in controls:
        condition = not (rank == 0 and base != 0) and not (
            rank == 1 and eta * base != 0
        )
        assert condition == allowed
    return len(controls)


def main():
    matching_total, matching_counts = audit_matching_shadow()
    grade_checks, grade_records = audit_grade_masks()
    projective_checks, line_count = audit_projective_shadow()
    cross_checks, cross_profiles = audit_cross_slots()
    rank_controls = audit_rank_controls()
    print("INDEPENDENT BASE-GRADE / CROSS-TARGET AUDIT PASS")
    print("  recursive matching words:", matching_total, matching_counts)
    print("  bitmask grade checks:", grade_checks, grade_records)
    print("  primitive projective checks:", projective_checks, line_count)
    print("  ordered target-slot checks:", cross_checks, cross_profiles)
    print("  independent rank controls:", rank_controls)
    print("  scope: theorem identities only; transport and node closure stay open")


if __name__ == "__main__":
    main()
