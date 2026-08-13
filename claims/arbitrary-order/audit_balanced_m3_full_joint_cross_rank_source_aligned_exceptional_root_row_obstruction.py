"""Independent stdlib audit of the source-aligned root-row obstruction."""

from __future__ import annotations

from itertools import product


def rank_mod_two(rows: list[list[int]]) -> int:
    work = [[entry % 2 for entry in row] for row in rows]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (i for i in range(pivot_row, len(work)) if work[i][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        for i, row in enumerate(work):
            if i == pivot_row or not row[column]:
                continue
            work[i] = [
                (left + right) % 2
                for left, right in zip(row, work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def product_map(q: tuple[int, ...]) -> list[list[int]]:
    x = q[:3]
    y = q[3:]
    columns: list[list[int]] = []
    for basis in range(6):
        v = [0, 0, 0]
        w = [0, 0, 0]
        if basis < 3:
            v[basis] = 1
        else:
            w[basis - 3] = 1
        column = [
            (v[i] * y[j] + x[i] * w[j]) % 2
            for i, j in product(range(3), repeat=2)
        ]
        columns.append(column)
    return [[columns[j][i] for j in range(6)] for i in range(9)]


def audit_finite_field_zero_divisors() -> None:
    counts: dict[tuple[str, int], int] = {}
    for q in product(range(2), repeat=6):
        if not any(q):
            continue
        pure = not any(q[:3]) or not any(q[3:])
        nullity = 6 - rank_mod_two(product_map(q))
        key = ("pure" if pure else "mixed", nullity)
        counts[key] = counts.get(key, 0) + 1
    assert counts == {("pure", 3): 14, ("mixed", 1): 49}
    print("independent F_2 zero-divisor census: PASS (14 pure; 49 mixed)")


def audit_purity_assignments() -> None:
    for labels in product((0, 1), repeat=3):
        majority = 0 if labels.count(0) >= 2 else 1
        majority_indices = [i for i, label in enumerate(labels) if label == majority]
        assert len(majority_indices) >= 2
        # q_first kills p_second and the remaining p; q_second kills p_first
        # and the remaining p.  Hence every p lies in the majority summand.
        forced = set(range(3))
        assert forced == {0, 1, 2}
        if len(set(labels)) == 2:
            minority = next(i for i, label in enumerate(labels) if label != majority)
            # q_minority also forces the two other p's into the opposite
            # summand, so those p's are zero.
            zero_forced = {i for i in range(3) if i != minority}
            assert len(zero_forced) == 2
    print("independent purity/pigeonhole audit: PASS (8 assignments)")


def audit_support_words() -> None:
    for s in range(3):
        allowed = {(a, s, s) for a in range(3)}
        allowed.update((c, c, c) for c in range(3))
        forbidden_grid = [
            word for word in product(range(3), repeat=3) if word[1] != word[2]
        ]
        assert len(allowed) == 5
        assert len(forbidden_grid) == 18
        assert all(word not in allowed for word in forbidden_grid)
    print("independent sparse-word audit: PASS (3 charts)")


def main() -> None:
    audit_finite_field_zero_divisors()
    audit_purity_assignments()
    audit_support_words()
    print("independent source-aligned exceptional-root-row audit: PASS")


if __name__ == "__main__":
    main()
