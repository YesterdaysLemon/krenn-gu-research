"""Independent no-import audit of pair descent and permanental response."""


def permutations(values):
    if not values:
        return [()]
    answer = []
    for index, value in enumerate(values):
        remainder = values[:index] + values[index + 1 :]
        for tail in permutations(remainder):
            answer.append((value,) + tail)
    return answer


def permanent(matrix):
    if not matrix:
        return 1
    return sum(
        product(matrix[row][permutation[row]] for row in range(len(matrix)))
        for permutation in permutations(tuple(range(len(matrix))))
    )


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def minor(matrix, deleted_row, deleted_column):
    return [
        [value for column, value in enumerate(row) if column != deleted_column]
        for row_index, row in enumerate(matrix)
        if row_index != deleted_row
    ]


def vertices(matching):
    answer = set()
    for left, right in matching:
        assert left not in answer and right not in answer
        answer.add(left)
        answer.add(right)
    return answer


def main():
    # Separate 3x3 integer exterior: compare the cofactor contraction with
    # direct choices of the two crossing edges and the residual matching.
    w = [[2, 3, 5], [7, 11, 13], [17, 19, 23]]
    y = [[29, 31, 37], [41, 43, 47]]
    z = [[53, 59], [61, 67], [71, 73]]

    c_per = [
        [permanent(minor(w, r, q)) for r in range(3)]
        for q in range(3)
    ]
    response = [[0, 0], [0, 0]]
    direct = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for q in range(3):
                for r in range(3):
                    response[i][j] += y[i][q] * c_per[q][r] * z[r][j]

                    remaining_rows = [row for row in range(3) if row != r]
                    remaining_columns = [column for column in range(3) if column != q]
                    for assignment in permutations(tuple(remaining_columns)):
                        residual_weight = product(
                            w[row][assignment[index]]
                            for index, row in enumerate(remaining_rows)
                        )
                        direct[i][j] += y[i][q] * z[r][j] * residual_weight
    assert response == direct
    assert all(value > 0 for row in response for value in row)

    # Audit the alternating path and its exact terminal change independently.
    large = {
        ("a0", "q0"),
        ("a1", "q1"),
        ("r0", "p0"),
        ("r1", "p1"),
    }
    alternating_path = {
        ("a0", "q0"),
        ("r0", "q0"),
        ("r0", "p0"),
    }
    reduced = large.symmetric_difference(alternating_path)
    assert vertices(large) == {"a0", "a1", "p0", "p1", "r0", "r1", "q0", "q1"}
    assert vertices(reduced) == {"a1", "p1", "r0", "r1", "q0", "q1"}
    assert len(reduced) == 3

    # Both feasible terminal sets are balanced between mode and source shores.
    large_terminals = {"a0", "a1", "p0", "p1"}
    reduced_terminals = {"a1", "p1"}
    for terminals in (large_terminals, reduced_terminals):
        assert sum(name.startswith("a") for name in terminals) == sum(
            name.startswith("p") for name in terminals
        )

    # Independent Boolean transitive closure.  The cut {a1,v1,p1} prevents
    # a1 from reaching p0, whereas a0 reaches both exits.
    vertices_directed = ("a0", "a1", "v0", "v1", "p0", "p1")
    arcs = {
        ("a0", "v0"),
        ("a1", "v1"),
        ("v0", "v1"),
        ("v0", "p0"),
        ("v1", "p1"),
    }
    closure = set(arcs)
    closure.update((vertex, vertex) for vertex in vertices_directed)
    changed = True
    while changed:
        changed = False
        for left, middle in tuple(closure):
            for middle_again, right in tuple(closure):
                if middle == middle_again and (left, right) not in closure:
                    closure.add((left, right))
                    changed = True
    assert ("a0", "p0") in closure
    assert ("a0", "p1") in closure
    assert ("a1", "p1") in closure
    assert ("a1", "p0") not in closure

    print("independent no-import boundary delta-matroid audit: PASS")
    print("one 3x3 cofactor identity and one path toggle; no family census")


if __name__ == "__main__":
    main()
