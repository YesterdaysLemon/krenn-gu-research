"""Independent no-import audit of the diagonal-incidence Schubert theorem."""

from fractions import Fraction


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if work[row][column]:
                pivot = row
                break
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row != pivot_row and work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    value - multiplier * pivot_value
                    for value, pivot_value in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def columns_to_rows(columns, dimension):
    return [[column[row] for column in columns] for row in range(dimension)]


def basis_vector(dimension, index):
    return tuple(1 if row == index else 0 for row in range(dimension))


def delete_rows(matrix, killed):
    return [row for index, row in enumerate(matrix) if index not in killed]


def main():
    n, k, d, q = 8, 4, 3, 4
    delta_columns = [basis_vector(n, index) for index in (0, 1, 2)]
    models = (
        ((3, 4, 5, 6), 0, 3, 7),
        ((0, 3, 4, 5), 1, 2, 6),
        ((0, 1, 3, 4), 2, 1, 5),
    )

    for image_indices, intersection_dimension, obstruction_rank, augmented_rank in models:
        gamma_columns = [basis_vector(n, index) for index in image_indices]
        gamma = columns_to_rows(gamma_columns, n)
        augmented = columns_to_rows(gamma_columns + delta_columns, n)
        assert rank(gamma) == k
        assert rank(augmented) == augmented_rank

        # Quotient by the coordinate image W and restrict Delta.
        obstruction = delete_rows(columns_to_rows(delta_columns, n), image_indices)
        assert rank(obstruction) == obstruction_rank
        assert d - obstruction_rank == intersection_dimension

        # Annihilator rows are coordinate covectors outside W.  Their
        # restrictions to Delta have the same rank.
        left_indices = [index for index in range(n) if index not in image_indices]
        left_restriction = [
            [1 if left_index == delta_index else 0 for delta_index in (0, 1, 2)]
            for left_index in left_indices
        ]
        assert len(left_restriction) == q
        assert rank(left_restriction) == obstruction_rank

        # Quotient by Delta gives the cofactor-relation matrix.
        cofactor_relations = delete_rows(gamma, (0, 1, 2))
        assert k - rank(cofactor_relations) == intersection_dimension

    # Dimension derivation from the incidence resolution, independently of
    # the primary verifier's matrix representation.
    n_big, k_big, d_big = 243, 219, 3
    q_big = n_big - k_big
    ambient = k_big * (n_big - k_big)
    resolved = (d_big - 1) + (k_big - 1) * (n_big - k_big)
    assert (ambient, resolved, ambient - resolved) == (5256, 5234, 22)

    stratum_codimensions = {}
    for intersection_dimension in (1, 2, 3):
        maximum_rank = d_big - intersection_dimension
        codimension = (d_big - maximum_rank) * (q_big - maximum_rank)
        stratum_codimensions[intersection_dimension] = codimension
    assert stratum_codimensions == {1: 22, 2: 46, 3: 72}

    # Normal spaces: variable diagonal target removes d-1 quotient
    # directions, whereas a fixed target removes none.
    variable_target_conditions = q_big - (d_big - 1)
    fixed_target_conditions = q_big
    assert (variable_target_conditions, fixed_target_conditions) == (22, 24)

    # Every nonzero cofactor coordinate can span the simple-incidence kernel.
    pi_delta_rows = (3, 4, 5, 6, 7)
    for chosen in range(k):
        other_columns = [column for column in range(k) if column != chosen]
        gamma_columns = []
        for column in range(k):
            if column == chosen:
                gamma_columns.append(basis_vector(n, 0))
            else:
                position = other_columns.index(column)
                gamma_columns.append(basis_vector(n, 3 + position))
        gamma = columns_to_rows(gamma_columns, n)
        relation_matrix = [gamma[row] for row in pi_delta_rows]
        assert rank(gamma) == k
        assert rank(relation_matrix) == k - 1
        assert all(relation_matrix[row][chosen] == 0 for row in range(len(relation_matrix)))

    print("AUDIT PASS: quotient and annihilator obstruction ranks agree")
    print("AUDIT PASS: incidence strata have codimensions 22, 46, 72")
    print("AUDIT PASS: tangent normal counts are 22 variable and 24 fixed")
    print("AUDIT PASS: generic cofactor relation matrix has corank one")
    print("AUDIT PASS: no coordinate cofactor relation is universal")
    print("searches=0")
    print("SCOPE: graph-companion incidence and physical cofactor realization UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
