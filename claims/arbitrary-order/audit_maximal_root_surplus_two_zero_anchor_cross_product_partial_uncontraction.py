"""Independent no-import audit for GLS61.

This audit uses only finite set and support calculations.  It shares no
SymPy code and imports no project module.
"""

from __future__ import annotations

from itertools import combinations, product

LABELS = frozenset(range(6))
COLOURS = frozenset(range(3))


def matching_survival_audit() -> int:
    checked = 0
    pairs = tuple(frozenset(pair) for pair in combinations(LABELS, 2))
    for mask in range(1 << 6):
        open_set = frozenset(label for label in LABELS if mask & (1 << label))
        survivors = tuple(pair for pair in pairs if pair <= open_set)
        assert len(survivors) == len(open_set) * (len(open_set) - 1) // 2
        checked += 1
    return checked


def double_cover_audit() -> int:
    accepted = 0
    for assignment in product((None, 0, 1, 2), repeat=6):
        zero_sets = {
            colour: frozenset(
                label for label, value in enumerate(assignment) if value == colour
            )
            for colour in COLOURS
        }
        one_open = all(
            zero_sets[colour] - {open_label}
            for colour in COLOURS
            for open_label in LABELS
        )
        if not one_open:
            continue
        accepted += 1
        assert tuple(sorted(len(zero_sets[colour]) for colour in COLOURS)) == (
            2,
            2,
            2,
        )
        assert set().union(*zero_sets.values()) == LABELS
        assert sum(len(zero_sets[colour]) for colour in COLOURS) == 6
    assert accepted == 90
    return accepted


def companion_supports(
    colour: int, left_orientation: str, right_orientation: str
) -> tuple[frozenset[tuple[int, int]], frozenset[tuple[int, int]]]:
    all_support = COLOURS
    pure = frozenset({colour})

    if left_orientation == "X":
        p_left, q_left = pure, all_support
    else:
        p_left, q_left = all_support, pure

    if right_orientation == "X":
        p_right, q_right = pure, all_support
    else:
        p_right, q_right = all_support, pure

    first = {(row, column) for row in p_left for column in q_right}
    second = {(row, column) for row in q_left for column in p_right}
    return frozenset(first), frozenset(second)


def orientation_support_audit() -> int:
    checked = 0
    for colour in COLOURS:
        for left, right in product(("X", "Y"), repeat=2):
            first, second = companion_supports(colour, left, right)
            # A coordinate present in exactly one summand cannot cancel.
            unique_support = first ^ second
            assert unique_support - {(colour, colour)}
            checked += 1
    assert checked == 12
    return checked


def pure_axis_audit() -> dict[str, int]:
    counts = {"one_open": 0, "axis_set": 0, "singleton": 0}
    total = 0
    for axis_count in range(1, 7):
        for assignment in product((None, 0, 1, 2), repeat=6 - axis_count):
            total += 1
            extras = {
                colour: frozenset(
                    label for label, value in enumerate(assignment) if value == colour
                )
                for colour in COLOURS
            }
            if not all(extras.values()):
                counts["one_open" if axis_count == 1 else "axis_set"] += 1
                continue
            assert axis_count <= 3
            singleton_colours = tuple(
                colour for colour in COLOURS if len(extras[colour]) == 1
            )
            assert singleton_colours
            colour = singleton_colours[0]
            (partner,) = tuple(extras[colour])
            assert all(
                partner not in extras[other] for other in COLOURS if other != colour
            )
            counts["singleton"] += 1

    assert total == 1365
    assert counts == {"one_open": 634, "axis_set": 275, "singleton": 456}

    # A diagonal with at most three colours can assign each unwanted colour
    # to a separate quotient slot while retaining one desired colour.
    diagonal_cases = 0
    for axis_count in range(2, 7):
        slots = tuple(range(axis_count))
        for size in range(1, 4):
            for support in combinations(COLOURS, size):
                desired = support[0]
                unwanted = support[1:]
                assert len(unwanted) <= len(slots)
                assigned = dict(zip(unwanted, slots[: len(unwanted)], strict=True))
                assert desired not in assigned
                assert len(set(assigned.values())) == len(unwanted)
                diagonal_cases += 1
    assert diagonal_cases == 35

    return {
        "pure_axis_assignments": total,
        "pure_axis_one_open_failures": counts["one_open"],
        "pure_axis_axis_set_quotient_failures": counts["axis_set"],
        "pure_axis_singleton_quotient_failures": counts["singleton"],
        "active_quotient_diagonal_cases": diagonal_cases,
    }


def scalar_boundary_audit() -> int:
    # The GLS58 control has exactly one zero factor for each colour.  It
    # passes the fully contracted scalar equation but fails when that unique
    # label is left open.
    zero_sets = {0: {2}, 1: {1, 4, 5}, 2: {0, 3}}
    failures = 0
    for colour in COLOURS:
        assert zero_sets[colour]
        if len(zero_sets[colour]) == 1:
            (open_label,) = tuple(zero_sets[colour])
            assert not (zero_sets[colour] - {open_label})
            failures += 1
    assert failures == 1
    return failures


def main() -> None:
    summary = {
        "open_set_survival_ledgers": matching_survival_audit(),
        "double_cover_partitions": double_cover_audit(),
        "orientation_support_cases": orientation_support_audit(),
        "scalar_boundary_one_open_failures": scalar_boundary_audit(),
    }
    summary.update(pure_axis_audit())
    for key in sorted(summary):
        print(f"{key}: {summary[key]}")
    print("PASS: independent GLS61 finite/support audit")


if __name__ == "__main__":
    main()
