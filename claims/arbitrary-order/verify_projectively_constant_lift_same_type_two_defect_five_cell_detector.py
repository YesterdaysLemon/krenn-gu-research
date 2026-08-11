"""Primary exact checks for the same-type two-defect five-cell theorem."""

from __future__ import annotations

from itertools import combinations, permutations, product

COLOURS = (0, 1, 2)
ROOTS = (0, 1, 2, 3)
ROWS = ("b", "c", "x", "y", "z")
MODES = ("u", "v", "t0", "t1", "t2")
ALL_COLOURS = frozenset(COLOURS)

SupportChart = dict[str, dict[str, frozenset[int]]]


def support_permanent_count(chart: SupportChart, colour: int) -> int:
    """Count source assignments in the 0/1 support permanent."""
    return sum(
        all(colour in chart[mode][row] for mode, row in zip(MODES, order, strict=True))
        for order in permutations(ROWS)
    )


def incidence_degrees(labels: list[frozenset[int]]) -> tuple[int, int, int]:
    return tuple(sum(colour in label for label in labels) for colour in COLOURS)


def inactive_set_census() -> tuple[int, int]:
    pairs = tuple(frozenset(pair) for pair in combinations(ROOTS, 2))
    equal = 0
    diamonds = 0
    for inactive_u in pairs:
        for inactive_v in pairs:
            if not inactive_u.intersection(inactive_v):
                continue
            if inactive_u.union(inactive_v) == frozenset(ROOTS):
                continue
            if inactive_u == inactive_v:
                equal += 1
            else:
                diamonds += 1
                assert len(inactive_u.intersection(inactive_v)) == 1
                assert len(inactive_u.union(inactive_v)) == 3
    assert equal == 6
    assert diamonds == 24

    # Pair Hall capacity for the one-dimensional AA common kernel.
    assert 5 * 1 < 3 * 2
    # Triple Hall capacity for b plus two BB common-kernel rows.
    assert 2 * 1 + 3 * 2 < 3 * 3
    return equal, diamonds


def aa_chart(
    u_axes: tuple[int, int, int],
    v_axes: tuple[int, int, int],
    transverse_axes: tuple[int, int, int],
) -> SupportChart:
    a_u, x_u, z_u = u_axes
    a_v, y_v, z_v = v_axes
    chart: SupportChart = {
        "u": {
            "b": frozenset(),
            "c": frozenset({a_u}),
            "x": frozenset({x_u}),
            "y": frozenset({a_u}),
            "z": frozenset({z_u}),
        },
        "v": {
            "b": frozenset(),
            "c": frozenset({a_v}),
            "x": frozenset({a_v}),
            "y": frozenset({y_v}),
            "z": frozenset({z_v}),
        },
    }
    for index, axis in enumerate(transverse_axes):
        chart[f"t{index}"] = {
            "b": ALL_COLOURS,
            "c": frozenset({axis}),
            "x": frozenset({axis}),
            "y": frozenset({axis}),
            "z": ALL_COLOURS,
        }
    return chart


def check_aa_support_obstruction() -> tuple[int, int, int]:
    charts = 0
    equal_z_axis = 0
    distinct_z_axis = 0
    for u_axes in permutations(COLOURS):
        for v_axes in permutations(COLOURS):
            for transverse_axes in product(COLOURS, repeat=3):
                charts += 1
                chart = aa_chart(u_axes, v_axes, transverse_axes)
                pure_counts = tuple(
                    support_permanent_count(chart, colour) for colour in COLOURS
                )
                z_u = u_axes[2]
                z_v = v_axes[2]
                if z_u == z_v:
                    equal_z_axis += 1
                    assert pure_counts[z_u] == 0
                else:
                    distinct_z_axis += 1
                    if pure_counts[z_u]:
                        assert transverse_axes.count(z_u) >= 2
                    if pure_counts[z_v]:
                        assert transverse_axes.count(z_v) >= 2
                    assert not (pure_counts[z_u] and pure_counts[z_v])
                assert not all(pure_counts)
    assert charts == 972
    assert equal_z_axis == 324
    assert distinct_z_axis == 648
    return charts, equal_z_axis, distinct_z_axis


def bb_chart(
    beta_u: int,
    beta_v: int,
    missing_u: int,
    missing_v: int,
    transverse_missing: tuple[int, int, int],
) -> SupportChart:
    plane_u = ALL_COLOURS - {missing_u}
    plane_v = ALL_COLOURS - {missing_v}
    chart: SupportChart = {
        "u": {
            "b": frozenset({beta_u}),
            "c": frozenset({beta_u}),
            "x": plane_u,
            "y": frozenset({beta_u}),
            "z": ALL_COLOURS,
        },
        "v": {
            "b": frozenset({beta_v}),
            "c": frozenset({beta_v}),
            "x": frozenset({beta_v}),
            "y": plane_v,
            "z": ALL_COLOURS,
        },
    }
    for index, missing in enumerate(transverse_missing):
        plane = ALL_COLOURS - {missing}
        chart[f"t{index}"] = {
            "b": plane,
            "c": plane,
            "x": plane,
            "y": plane,
            "z": ALL_COLOURS,
        }
    return chart


def bb_triple_labels(
    beta_u: int,
    beta_v: int,
    missing_u: int,
    missing_v: int,
    transverse_missing: tuple[int, int, int],
) -> tuple[list[frozenset[int]], list[frozenset[int]]]:
    transverse = [ALL_COLOURS - {missing} for missing in transverse_missing]
    labels_bcx = [
        ALL_COLOURS - {missing_u},
        frozenset({beta_v}),
        *transverse,
    ]
    labels_bcy = [
        frozenset({beta_u}),
        ALL_COLOURS - {missing_v},
        *transverse,
    ]
    return labels_bcx, labels_bcy


def check_bb_incidence_obstruction() -> tuple[int, int, int, int]:
    charts = 0
    triple_quota_charts = 0
    exact_missing_ledgers = 0
    admissible = 0
    for beta_u in COLOURS:
        for beta_v in COLOURS:
            for missing_u in COLOURS:
                if missing_u == beta_u:
                    continue
                for missing_v in COLOURS:
                    if missing_v == beta_v:
                        continue
                    for transverse_missing in product(COLOURS, repeat=3):
                        charts += 1
                        chart = bb_chart(
                            beta_u,
                            beta_v,
                            missing_u,
                            missing_v,
                            transverse_missing,
                        )
                        pure_counts = tuple(
                            support_permanent_count(chart, colour)
                            for colour in COLOURS
                        )
                        if all(pure_counts):
                            assert len(set(transverse_missing)) == 3

                        labels_bcx, labels_bcy = bb_triple_labels(
                            beta_u,
                            beta_v,
                            missing_u,
                            missing_v,
                            transverse_missing,
                        )
                        if min(incidence_degrees(labels_bcx)) < 3:
                            continue
                        if min(incidence_degrees(labels_bcy)) < 3:
                            continue
                        triple_quota_charts += 1

                        if len(set(transverse_missing)) == 3:
                            exact_missing_ledgers += 1
                            assert missing_u == beta_v
                            assert missing_v == beta_u
                            assert beta_u != beta_v
                            assert pure_counts[beta_u] == 0

                        if all(pure_counts):
                            admissible += 1

    assert charts == 972
    assert triple_quota_charts == 54
    assert exact_missing_ledgers == 36
    assert admissible == 0
    return charts, triple_quota_charts, exact_missing_ledgers, admissible


def main() -> None:
    equal, diamonds = inactive_set_census()
    aa_charts, aa_equal, aa_distinct = check_aa_support_obstruction()
    bb_charts, bb_quota, bb_exact, bb_admissible = check_bb_incidence_obstruction()
    print(
        "PASS: same-type inactive-set census has "
        f"{equal} equal and {diamonds} diamond patterns"
    )
    print(
        f"PASS: {aa_charts} AA support charts "
        f"({aa_equal} equal-axis, {aa_distinct} distinct-axis) lose a pure term"
    )
    print(
        f"PASS: {bb_charts} BB charts give {bb_quota} triple-quota ledgers, "
        f"{bb_exact} exact missing-colour ledgers, and {bb_admissible} survivors"
    )
    print("SCOPE: AA/BB two-defect cells detected")
    print("SCOPE: three-or-more defects and global Krenn-Gu remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
