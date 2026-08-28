"""Primary exact checks for the cross-product partial-uncontraction theorem.

The arbitrary-root tensor identity is proved in the owning document.  This
script checks the finite matching-survival ledger, the complete six-label
zero-set census, the four injective shore-orientation obstructions, and the
sharp GLS58 scalar control that is rejected by the new one-open equations.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

LABELS = tuple(range(6))
COLOURS = tuple(range(3))


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def audit_partial_uncontraction_survival() -> dict[str, int]:
    """A companion pair survives iff both of its labels remain open."""

    pairs = tuple(combinations(LABELS, 2))
    checked = 0
    for size in range(7):
        for open_labels in combinations(LABELS, size):
            open_set = frozenset(open_labels)
            survivors = tuple(pair for pair in pairs if frozenset(pair) <= open_set)
            assert len(survivors) == size * (size - 1) // 2
            if size <= 1:
                assert not survivors
            if size == 2:
                assert survivors == (tuple(open_labels),)
            checked += 1

    return {
        "partial_uncontraction_open_sets": checked,
        "one_open_source_terms": 0,
        "two_open_source_terms": 1,
    }


def audit_six_label_double_cover() -> dict[str, int]:
    """Non-axis injective labels have at most one zero cross coordinate."""

    # -1 means that no cross-product coordinate vanishes identically.
    admissible: list[tuple[int, ...]] = []
    for assignment in product((-1, 0, 1, 2), repeat=6):
        counts = tuple(assignment.count(colour) for colour in COLOURS)
        if all(count >= 2 for count in counts):
            admissible.append(assignment)
            assert counts == (2, 2, 2)
            assert -1 not in assignment

            for colour in COLOURS:
                zero_pair = tuple(
                    label for label, value in enumerate(assignment) if value == colour
                )
                assert len(zero_pair) == 2
                for target_colour in COLOURS:
                    zeros_outside = tuple(
                        label
                        for label, value in enumerate(assignment)
                        if value == target_colour and label not in zero_pair
                    )
                    if target_colour == colour:
                        assert not zeros_outside
                    else:
                        assert len(zeros_outside) == 2

    # Number of labelled 2+2+2 partitions: 6!/(2!2!2!).
    assert len(admissible) == 90
    return {
        "nonaxis_zero_set_assignments": 4**6,
        "double_cover_partitions": len(admissible),
    }


def shore_vector(
    prefix: str, colour: int, orientation: str
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return generic p,q vectors for the two GLS58 Lemma-9 orientations."""

    others = tuple(index for index in COLOURS if index != colour)
    if orientation == "X":
        alpha = sp.Symbol(f"{prefix}_alpha")
        p = sp.zeros(3, 1)
        p[colour] = alpha
        q = sp.Matrix(sp.symbols(f"{prefix}_q0:{3}"))
        # The written proof uses that both off-colour q coordinates span.
        assert all(q[index] != 0 for index in others)
        return p, q
    if orientation == "Y":
        beta = sp.Symbol(f"{prefix}_beta")
        p = sp.Matrix(sp.symbols(f"{prefix}_p0:{3}"))
        q = sp.zeros(3, 1)
        q[colour] = beta
        assert all(p[index] != 0 for index in others)
        return p, q
    raise ValueError(orientation)


def audit_pair_orientation_obstruction() -> dict[str, int]:
    """No two same-colour non-axis injective patterns have a pure companion."""

    checked = 0
    for colour in COLOURS:
        for left_orientation, right_orientation in product(("X", "Y"), repeat=2):
            p_s, q_s = shore_vector("s", colour, left_orientation)
            p_u, q_u = shore_vector("u", colour, right_orientation)
            companion = outer(p_s, q_u) + outer(q_s, p_u)
            off_pure = tuple(
                sp.expand(companion[row, column])
                for row in COLOURS
                for column in COLOURS
                if (row, column) != (colour, colour)
            )
            assert any(value != 0 for value in off_pure)
            checked += 1

    return {"injective_orientation_cases": checked}


def audit_pure_axis_exclusion() -> dict[str, int]:
    """Classify every nonempty pure-axis zero pattern used in Theorem 7."""

    total = 0
    one_open_failures = 0
    axis_set_quotient_failures = 0
    singleton_quotient_failures = 0

    for axis_count in range(1, 7):
        nonaxis_count = 6 - axis_count
        for assignment in product((-1, 0, 1, 2), repeat=nonaxis_count):
            total += 1
            extra_zeros = {
                colour: tuple(
                    label for label, value in enumerate(assignment) if value == colour
                )
                for colour in COLOURS
            }
            if not all(extra_zeros.values()):
                if axis_count == 1:
                    one_open_failures += 1
                else:
                    axis_set_quotient_failures += 1
                continue

            # Three disjoint nonempty sets require at least three nonaxis
            # labels.  With three through five labels, one set is a singleton.
            assert axis_count <= 3
            singleton_colours = tuple(
                colour for colour in COLOURS if len(extra_zeros[colour]) == 1
            )
            assert singleton_colours
            colour = singleton_colours[0]
            (partner,) = extra_zeros[colour]
            assert all(
                partner not in extra_zeros[other]
                for other in COLOURS
                if other != colour
            )
            singleton_quotient_failures += 1

    assert total == sum(4 ** (6 - axis_count) for axis_count in range(1, 7))
    assert total == 1365
    assert one_open_failures == 634
    assert axis_set_quotient_failures == 275
    assert singleton_quotient_failures == 456
    assert (
        one_open_failures + axis_set_quotient_failures + singleton_quotient_failures
        == total
    )

    # Check the constructive dual-functional proof that every nonempty
    # three-colour diagonal survives at least two active-line quotients.
    diagonal_cases = 0
    for axis_count in range(2, 7):
        active = [sp.Matrix(sp.symbols(f"a{slot}_0:3")) for slot in range(axis_count)]
        for size in range(1, 4):
            for support in combinations(COLOURS, size):
                desired = support[0]
                unwanted = support[1:]
                functionals: list[sp.Matrix] = []
                for slot, active_row in enumerate(active):
                    if slot < len(unwanted):
                        killed = unwanted[slot]
                        remaining = next(
                            colour
                            for colour in COLOURS
                            if colour not in (desired, killed)
                        )
                    else:
                        remaining = next(
                            colour for colour in COLOURS if colour != desired
                        )
                    functional = sp.zeros(3, 1)
                    functional[desired] = active_row[remaining]
                    functional[remaining] = -active_row[desired]
                    assert (functional.T * active_row)[0] == 0
                    assert functional[desired] != 0
                    functionals.append(functional)

                readings = {
                    colour: sp.prod(functional[colour] for functional in functionals)
                    for colour in support
                }
                assert readings[desired] != 0
                assert all(readings[colour] == 0 for colour in unwanted)
                diagonal_cases += 1

    assert diagonal_cases == 35
    return {
        "pure_axis_assignments": total,
        "pure_axis_one_open_failures": one_open_failures,
        "pure_axis_axis_set_quotient_failures": axis_set_quotient_failures,
        "pure_axis_singleton_quotient_failures": singleton_quotient_failures,
        "active_quotient_diagonal_cases": diagonal_cases,
    }


def audit_gls58_scalar_sharpness() -> dict[str, int]:
    """Replay the GLS58 termwise-zero control and detect its one-open failure."""

    z_0 = sp.Matrix(sp.symbols("z00 z01 z02"))
    z_1 = sp.Matrix(sp.symbols("z10 z11 z12"))
    permutation = sp.Matrix(((0, 0, 1), (1, 0, 0), (0, 1, 0)))
    additions = (
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.zeros(3),
        sp.diag(0, 0, 1),
        sp.zeros(3),
        sp.zeros(3),
    )
    y_cells = ((2, 2), (0, 1), (0, 0), (0, 2), (1, 1), (0, 1))

    crosses: list[sp.Matrix] = []
    zero_sets: list[set[int]] = [set() for _ in COLOURS]
    for label, (addition, (row, column)) in enumerate(
        zip(additions, y_cells, strict=True)
    ):
        x_matrix = permutation + addition
        y_matrix = sp.zeros(3)
        y_matrix[row, column] = 1
        assert x_matrix.det() == 1
        cross = (x_matrix.T * z_0).cross(y_matrix.T * z_1)
        assert any(sp.expand(entry) != 0 for entry in cross)
        crosses.append(cross)
        for colour in COLOURS:
            if sp.expand(cross[colour]) == 0:
                zero_sets[colour].add(label)

    assert zero_sets == [{2}, {1, 4, 5}, {0, 3}]
    scalar_products = tuple(
        sp.expand(sp.prod(cross[colour] for cross in crosses)) for colour in COLOURS
    )
    assert scalar_products == (0, 0, 0)

    failed_one_open = 0
    for colour, zero_set in enumerate(zero_sets):
        if len(zero_set) != 1:
            continue
        (open_label,) = tuple(zero_set)
        product_without_open = sp.expand(
            sp.prod(crosses[label][colour] for label in LABELS if label != open_label)
        )
        assert product_without_open != 0
        failed_one_open += 1

    assert failed_one_open == 1

    return {
        "gls58_scalar_zero_products": len(scalar_products),
        "gls58_control_failed_one_open_equations": failed_one_open,
    }


def main() -> None:
    summary: dict[str, int] = {}
    summary.update(audit_partial_uncontraction_survival())
    summary.update(audit_six_label_double_cover())
    summary.update(audit_pair_orientation_obstruction())
    summary.update(audit_pure_axis_exclusion())
    summary.update(audit_gls58_scalar_sharpness())

    for key in sorted(summary):
        print(f"{key}: {summary[key]}")
    print("PASS: GLS61 cross-product partial-uncontraction checks")


if __name__ == "__main__":
    main()
