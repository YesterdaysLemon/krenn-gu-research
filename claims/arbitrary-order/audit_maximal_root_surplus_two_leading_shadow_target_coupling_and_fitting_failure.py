"""Independent no-project-import audit of the GLS18 leading-shadow theorem."""

from itertools import product

PRIME = 5


def inverse(value):
    return pow(value % PRIME, PRIME - 2, PRIME)


def matrix_rank(rows):
    work = [[entry % PRIME for entry in row] for row in rows]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = inverse(work[pivot_row][column])
        work[pivot_row] = [(scale * entry) % PRIME for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def columns_to_rows(columns, dimension):
    return [[column[row] for column in columns] for row in range(dimension)]


def two_by_two_minors(rows):
    if len(rows) != 2:
        raise ValueError("bounded audit expects two rows")
    return [
        (rows[0][left] * rows[1][right] - rows[0][right] * rows[1][left]) % PRIME
        for left in range(len(rows[0]))
        for right in range(left + 1, len(rows[0]))
    ]


def minor_values(rows, size):
    if size == 1:
        return [entry % PRIME for row in rows for entry in row]
    if size == 2:
        return two_by_two_minors(rows)
    raise ValueError("bounded audit only uses sizes one and two")


def audit_complete_target_words():
    """Compare all five labelled output words, including mixed words."""

    alpha = (1, 2, 4)
    checked = 0
    admitted = 0
    for b in product(range(PRIME), repeat=2):
        for response in product(range(PRIME), repeat=5):
            # The three pure coefficients are forced by the three independent
            # pure target words.  There are no left-side mixed target words.
            pure_columns = [
                tuple(
                    (b[row] * response[col] * inverse(alpha[col])) % PRIME
                    for row in range(2)
                )
                for col in range(3)
            ]
            mixed_rhs = [
                tuple((b[row] * response[col]) % PRIME for row in range(2))
                for col in range(3, 5)
            ]
            equation_holds = all(not any(column) for column in mixed_rhs)
            if equation_holds:
                pure_rank = matrix_rank(columns_to_rows(pure_columns, 2))
                assert pure_rank <= 1
                assert (pure_rank == 1) == (any(b) and any(response))
                if any(b):
                    assert not any(response[3:])
                admitted += 1
            checked += 1
    return checked, admitted


def audit_pointwise_rank_rise():
    checks = 0
    rises = 0
    for nuisance in product(range(PRIME), repeat=2):
        nuisance_rows = [[nuisance[0]], [nuisance[1]]]
        for desired in product(range(PRIME), repeat=2):
            augmented = [
                [nuisance[0], desired[0]],
                [nuisance[1], desired[1]],
            ]
            rise = matrix_rank(augmented) > matrix_rank(nuisance_rows)
            detector = False
            for size in (1, 2):
                if not any(minor_values(nuisance_rows, size)) and any(
                    minor_values(augmented, size)
                ):
                    detector = True
            assert rise == detector
            rises += int(rise)
            checks += 1
    return checks, rises


def affine_value(coefficients, point):
    return (coefficients[0] + coefficients[1] * point) % PRIME


def audit_gated_vanishing_sets():
    """Independently compare useful loci with gated minor containments."""

    checks = 0
    empty_loci = 0
    gates = ((1, 0),) + tuple((-root % PRIME, 1) for root in range(PRIME))
    # Two affine nuisance entries, one constant desired column, and all
    # principal gates 1 and z-root.  This is a point-set audit, not a radical
    # algorithm and not an import of the primary verifier.
    for coefficients in product(range(PRIME), repeat=4):
        first = coefficients[:2]
        second = coefficients[2:]
        for desired in product(range(PRIME), repeat=2):
            for gate in gates:
                useful_points = []
                containment_holds = True
                for point in range(PRIME):
                    nuisance_rows = [
                        [affine_value(first, point)],
                        [affine_value(second, point)],
                    ]
                    augmented = [
                        nuisance_rows[0] + [desired[0]],
                        nuisance_rows[1] + [desired[1]],
                    ]
                    gate_value = affine_value(gate, point)
                    if gate_value and matrix_rank(augmented) > matrix_rank(
                        nuisance_rows
                    ):
                        useful_points.append(point)
                    for size in (1, 2):
                        nuisance_vanishes = not any(minor_values(nuisance_rows, size))
                        augmented_vanishes = not any(minor_values(augmented, size))
                        if nuisance_vanishes and gate_value and not augmented_vanishes:
                            containment_holds = False
                assert (not useful_points) == containment_holds
                empty_loci += int(not useful_points)
                checks += 1
    return checks, empty_loci


def audit_four_root_spaces():
    root_basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    assert matrix_rank(columns_to_rows(root_basis, 3)) == 3
    full_masks = 0
    for mask in range(8):
        nuisance = [root_basis[index] for index in range(3) if mask & (1 << index)]
        all_absorbed = all(
            matrix_rank(columns_to_rows(nuisance + [vector], 3))
            == matrix_rank(columns_to_rows(nuisance, 3))
            for vector in root_basis
        )
        assert all_absorbed == (mask == 7)
        full_masks += int(all_absorbed)

    pair_diagonal = tuple(
        tuple(int(position == 3 * colour + colour) for position in range(9))
        for colour in range(3)
    )
    pair_rank = matrix_rank(columns_to_rows(pair_diagonal, 9))
    assert pair_rank == 3
    assert pair_rank < 9
    return full_masks, pair_rank


def main():
    target_words = audit_complete_target_words()
    pointwise = audit_pointwise_rank_rise()
    gated = audit_gated_vanishing_sets()
    four_root = audit_four_root_spaces()
    print("INDEPENDENT LEADING-SHADOW TARGET/FITTING AUDIT PASS")
    print("  complete five-word equations / admitted equations:", target_words)
    print("  pointwise rank tables / rises:", pointwise)
    print("  gated affine point sets / empty loci:", gated)
    print("  r=4 full first-shadow masks / pair diagonal rank:", four_root)
    print("  scope: exact failure profile only; no survival or node closure")


if __name__ == "__main__":
    main()
