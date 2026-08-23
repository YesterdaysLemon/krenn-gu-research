"""No-import Fraction audit for GLS30, independent of its SymPy verifier."""

from fractions import Fraction
from functools import cache
from itertools import combinations, product

COLOURS = tuple(range(3))
PORTS = tuple(range(4))
PAIRS = tuple(combinations(PORTS, 2))


def vector(*entries):
    return tuple(Fraction(entry) for entry in entries)


def unit(index):
    return tuple(Fraction(int(index == slot)) for slot in COLOURS)


def matrix_unit(row, column, value=1):
    return tuple(
        tuple(Fraction(value if (i, j) == (row, column) else 0) for j in COLOURS)
        for i in COLOURS
    )


def matrix_add(*matrices):
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices) for j in COLOURS)
        for i in COLOURS
    )


def matrix_scale(value, matrix):
    value = Fraction(value)
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def tensor_pair(left, right):
    return tuple(tuple(a * b for b in right) for a in left)


def dot(left, right):
    return sum(a * b for a, b in zip(left, right, strict=True))


def matvec(matrix, right):
    return tuple(dot(row, right) for row in matrix)


def bilinear(left, matrix, right):
    return dot(left, matvec(matrix, right))


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLOURS) for i in COLOURS)


def matrix_rank(columns):
    if not columns:
        return 0
    rows = [[column[row] for column in columns] for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
        selected = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]), None
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                entry - multiplier * base
                for entry, base in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def cross(left, right):
    return vector(
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def channel(x, y, pair):
    left, right = pair
    return matrix_add(tensor_pair(x[left], y[right]), tensor_pair(y[left], x[right]))


def complement(pair):
    return tuple(port for port in PORTS if port not in pair)


def audit_kernel_isolation():
    # This uses a four-port Fraction contraction, not the primary's five-port
    # dense-array route.
    x = (
        vector(1, 2, 0),
        vector(0, 1, 2),
        vector(2, 0, 1),
        vector(1, -1, 1),
    )
    y = (
        vector(0, 1, 1),
        vector(1, 0, 1),
        vector(1, 2, 0),
        vector(0, 1, 2),
    )
    kernels = tuple(cross(x[u], y[u]) for u in PORTS)
    responses = {
        pair: tuple(
            tuple(Fraction(1 + sum(pair) + 2 * i - j) for j in COLOURS) for i in COLOURS
        )
        for pair in PAIRS
    }
    for kept in PAIRS:
        cut = complement(kept)
        observed = [[Fraction(0) for _ in COLOURS] for _ in COLOURS]
        for kept_word in product(COLOURS, repeat=2):
            for cut_word in product(COLOURS, repeat=2):
                word = [0, 0, 0, 0]
                for port, colour in zip(kept, kept_word, strict=True):
                    word[port] = colour
                for port, colour in zip(cut, cut_word, strict=True):
                    word[port] = colour
                weight = kernels[cut[0]][cut_word[0]] * kernels[cut[1]][cut_word[1]]
                value = Fraction(0)
                for supplier in PAIRS:
                    response_pair = complement(supplier)
                    value += (
                        channel(x, y, supplier)[word[supplier[0]]][word[supplier[1]]]
                        * responses[response_pair][word[response_pair[0]]][
                            word[response_pair[1]]
                        ]
                    )
                observed[kept_word[0]][kept_word[1]] += weight * value
        scalar = bilinear(kernels[cut[0]], responses[cut], kernels[cut[1]])
        expected = matrix_scale(scalar, channel(x, y, kept))
        assert tuple(map(tuple, observed)) == expected
    return {"isolated_pairs": 6, "arithmetic": "Fraction"}


def assemble_four_tensor(suppliers, responses):
    output = {}
    for word in product(COLOURS, repeat=4):
        value = Fraction(0)
        for pair in PAIRS:
            other = complement(pair)
            value += (
                suppliers[pair][word[pair[0]]][word[pair[1]]]
                * responses[other][word[other[0]]][word[other[1]]]
            )
        if value:
            output[word] = value
    return output


def audit_controls():
    e0, e1 = unit(0), unit(1)
    one_x = (e0,) * 4
    one_y = one_x
    one_scalars = (1, 1, 1, 1, 1, Fraction(-9, 2))
    one_responses = {
        pair: matrix_scale(value, tensor_pair(e0, e0))
        for pair, value in zip(PAIRS, one_scalars, strict=True)
    }
    one_suppliers = {pair: channel(one_x, one_y, pair) for pair in PAIRS}
    assert assemble_four_tensor(one_suppliers, one_responses) == {(0, 0, 0, 0): 1}

    two_x = (e0, e0, e1, e1)
    two_y = two_x
    two_responses = {
        (0, 1): tensor_pair(e1, e1),
        (2, 3): matrix_scale(Fraction(1, 2), tensor_pair(e0, e0)),
    }
    for pair, value in zip(
        ((0, 2), (0, 3), (1, 2), (1, 3)), (1, 1, 1, -3), strict=True
    ):
        two_responses[pair] = matrix_scale(value, tensor_pair(e0, e1))
    two_suppliers = {pair: channel(two_x, two_y, pair) for pair in PAIRS}
    assert assemble_four_tensor(two_suppliers, two_responses) == {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 2,
    }
    for suppliers, responses in (
        (one_suppliers, one_responses),
        (two_suppliers, two_responses),
    ):
        assert all(
            any(entry for row in item for entry in row) for item in suppliers.values()
        )
        assert all(
            any(entry for row in item for entry in row) for item in responses.values()
        )
        assert all(
            any(entry for row in suppliers[complement(pair)] for entry in row)
            for pair in PAIRS
        )
    return {"controls": 2, "tensor_coefficients": 162, "full_normal_images": 12}


@cache
def recursive_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[-1]
    output = []
    for position, second in enumerate(vertices[:-1]):
        remainder = vertices[:position] + vertices[position + 1 : -1]
        for tail in recursive_matchings(remainder):
            output.append((*tail, (second, first)))
    return tuple(output)


def edge_value(matrices, left, right, colour_left, colour_right):
    if left < right:
        matrix = matrices.get((left, right))
        if matrix is None:
            return Fraction(0)
        return matrix[colour_left][colour_right]
    return edge_value(matrices, right, left, colour_right, colour_left)


def coefficient(matrices, word, vertices=None):
    if vertices is None:
        vertices = tuple(range(len(word)))
    total = Fraction(0)
    for matching in recursive_matchings(vertices):
        term = Fraction(1)
        for left, right in matching:
            term *= edge_value(matrices, left, right, word[left], word[right])
        total += term
    return total


def put(matrices, left, right, matrix):
    if left < right:
        matrices[(left, right)] = matrix
    else:
        matrices[(right, left)] = transpose(matrix)


def response_deck_graph(active_count):
    matrices = {}
    e0, e1 = unit(0), unit(1)
    if active_count == 1:
        n0, n1 = vector(1, 1, 0), vector(1, 0, 1)
        shore0 = (vector(0, 0, 1), vector(1, -1, 1))
        shore1 = (vector(0, 1, 0), vector(1, 1, -1))
        x = (e0,) * 4
        responses = {
            pair: matrix_scale(value, tensor_pair(e0, e0))
            for pair, value in zip(PAIRS, (1, 1, 1, 1, 1, Fraction(-9, 2)), strict=True)
        }
        expected = {(0, 0, 0, 0): Fraction(1)}
        expected_p = Fraction(2)
    else:
        n0, n1 = vector(1, 1, 0), vector(1, 2, 1)
        shore0 = (vector(0, 0, 1), vector(1, -1, 1))
        shore1 = (vector(0, 1, -2), vector(1, 1, -3))
        x = (e0, e0, e1, e1)
        responses = {
            (0, 1): tensor_pair(e1, e1),
            (2, 3): matrix_scale(Fraction(1, 2), tensor_pair(e0, e0)),
        }
        for pair, value in zip(
            ((0, 2), (0, 3), (1, 2), (1, 3)), (1, 1, 1, -3), strict=True
        ):
            responses[pair] = matrix_scale(value, tensor_pair(e0, e1))
        expected = {(0, 0, 0, 0): Fraction(1), (1, 1, 1, 1): Fraction(2)}
        expected_p = Fraction(-2)

    put(matrices, 0, 2, tensor_pair(shore0[0], e0))
    put(matrices, 0, 3, tensor_pair(shore0[1], e0))
    put(matrices, 1, 2, tensor_pair(shore1[0], e0))
    put(matrices, 1, 3, tensor_pair(shore1[1], e0))
    for port in PORTS:
        put(matrices, 0, 4 + port, tensor_pair(e0, x[port]))
        put(matrices, 1, 4 + port, tensor_pair(e0, x[port]))
    put(matrices, 2, 3, matrix_unit(0, 0))
    for pair, response in responses.items():
        put(matrices, 4 + pair[0], 4 + pair[1], response)
    q = matrix_add(
        tensor_pair(shore0[0], shore1[1]),
        tensor_pair(shore0[1], shore1[0]),
    )
    assert sum(entry for row in q for entry in row) == expected_p
    return matrices, n0, n1, responses, expected, expected_p


def audit_response_deck_integrability():
    results = {}
    ones = vector(1, 1, 1)
    for active_count in (1, 2):
        matrices, n0, n1, responses, expected, p = response_deck_graph(active_count)
        normal = {}
        for port_word in product(COLOURS, repeat=4):
            total = Fraction(0)
            for root_word in product(COLOURS, repeat=4):
                word = (*root_word, *port_word)
                weight = (
                    n0[root_word[0]]
                    * n1[root_word[1]]
                    * ones[root_word[2]]
                    * ones[root_word[3]]
                )
                total += weight * coefficient(matrices, word)
            if total:
                normal[port_word] = total
        assert normal == expected

        response_coefficients = 0
        for pair in PAIRS:
            vertices = (2, 3, 4 + pair[0], 4 + pair[1])
            for port_word in product(COLOURS, repeat=2):
                total = Fraction(0)
                for qword in product(COLOURS, repeat=2):
                    word = [0] * 8
                    word[2], word[3] = qword
                    word[4 + pair[0]], word[4 + pair[1]] = port_word
                    total += coefficient(matrices, tuple(word), vertices)
                assert total == responses[pair][port_word[0]][port_word[1]]
                response_coefficients += 1
        results[active_count] = {
            "p": p,
            "normal_coefficients": 81,
            "response_coefficients": response_coefficients,
        }
    return results


def maximum_root_graph():
    matrices = {}
    put(
        matrices,
        0,
        2,
        matrix_add(matrix_unit(0, 0), matrix_scale(-1, matrix_unit(1, 0))),
    )
    put(matrices, 1, 2, matrices[(0, 2)])
    put(matrices, 0, 3, matrix_unit(1, 1))
    put(matrices, 0, 4, matrix_unit(2, 2))
    put(matrices, 1, 3, matrix_unit(2, 2))
    put(matrices, 1, 4, matrix_unit(1, 1))
    put(matrices, 0, 5, matrix_unit(0, 0))
    put(matrices, 1, 5, matrix_unit(0, 0))
    for port in (6, 7):
        put(matrices, 0, port, matrix_unit(1, 0))
        put(matrices, 1, port, matrix_unit(2, 1))
    put(matrices, 3, 4, matrix_unit(0, 0))
    put(matrices, 2, 5, matrix_unit(0, 1))
    put(matrices, 2, 6, matrix_unit(1, 1))
    put(matrices, 2, 7, matrix_unit(2, 2))
    put(matrices, 5, 6, matrix_unit(2, 2))
    put(matrices, 5, 7, matrix_unit(1, 1))
    put(matrices, 6, 7, matrix_unit(0, 0, Fraction(1, 2)))
    return matrices


def audit_maximum_root_control():
    matrices = maximum_root_graph()
    ones = vector(1, 1, 1)
    roots = (0, 1, 2)
    outside = (3, 4, 5, 6, 7)
    assert all(
        bilinear(ones, matrices.get(pair, matrix_unit(0, 0, 0)), ones) == 0
        for pair in combinations(roots, 2)
    )

    monomial_edges = {
        pair
        for pair, matrix in matrices.items()
        if sum(bool(entry) for row in matrix for entry in row) == 1
    }
    maximum_independent_size = 0
    for mask in range(1 << 8):
        selected = tuple(vertex for vertex in range(8) if mask & (1 << vertex))
        if all(pair not in monomial_edges for pair in combinations(selected, 2)):
            maximum_independent_size = max(maximum_independent_size, len(selected))
    assert maximum_independent_size == 3

    incidence_ranks = []
    for vertex in outside:
        columns = []
        for colour in COLOURS:
            columns.append(
                tuple(
                    sum(
                        edge_value(matrices, root, vertex, root_colour, colour)
                        for root_colour in COLOURS
                    )
                    for root in roots
                )
            )
        incidence_ranks.append(matrix_rank(columns))
    assert tuple(incidence_ranks) == (2, 2, 2, 2, 3)

    pure = tuple(coefficient(matrices, (colour,) * 8) for colour in COLOURS)
    assert pure == (1, 1, 1)
    failures = (
        coefficient(matrices, (0, 1, 0, 0, 0, 0, 0, 0)),
        coefficient(matrices, (1, 0, 0, 0, 0, 0, 0, 0)),
    )
    assert failures == (Fraction(-1, 2), Fraction(-1, 2))

    promoted = (2, 5, 6, 7)
    response_coefficients = 0
    for pair in combinations(promoted, 2):
        assert any(
            edge_value(matrices, *pair, left_colour, right_colour)
            for left_colour, right_colour in product(COLOURS, repeat=2)
        )
        for word in product(COLOURS, repeat=2):
            total = Fraction(0)
            for qword in product(COLOURS, repeat=2):
                full_word = [0] * 8
                full_word[3], full_word[4] = qword
                full_word[pair[0]], full_word[pair[1]] = word
                total += coefficient(matrices, tuple(full_word), (3, 4, *pair))
            assert total == edge_value(matrices, *pair, *word)
            response_coefficients += 1

    normal = {}
    for port_word in product(COLOURS, repeat=4):
        total = Fraction(0)
        for qword in product(COLOURS, repeat=2):
            word = (0, 0, port_word[0], qword[0], qword[1], *port_word[1:])
            total += coefficient(matrices, word)
        if total:
            normal[port_word] = total
    assert normal == {(0, 0, 0, 0): 1}
    return {
        "maximum_root_size": maximum_independent_size,
        "incidence_ranks": tuple(incidence_ranks),
        "pure": pure,
        "mixed_failures": failures,
        "response_coefficients": response_coefficients,
        "normal_coefficients": 81,
    }


def audit_projected_kernel_logic():
    # Exhaust coordinate supports of nonzero line generators in K^2.  If one
    # factor is the plane, Hadamard dimension is exactly the other's support.
    generators = (vector(1, 0), vector(0, 1), vector(1, 1), vector(1, -1))
    support_checks = 0
    for generator in generators:
        support = sum(value != 0 for value in generator)
        plane_products = (
            vector(generator[0], 0),
            vector(0, generator[1]),
        )
        assert matrix_rank(plane_products) == support
        support_checks += 1
    assert matrix_rank((vector(1, 0), vector(0, 1))) == 2
    return {"line_supports": support_checks, "zero_star_branch_retained": True}


def main():
    print("GLS30 independent no-import audit: PASS")
    print("  independent kernel isolation:", audit_kernel_isolation())
    print("  sparse control assembly:", audit_controls())
    print("  projected-kernel support logic:", audit_projected_kernel_logic())
    print("  independent response-deck replay:", audit_response_deck_integrability())
    print("  recursive physical graph audit:", audit_maximum_root_control())
    print("  no imports from the primary verifier, SymPy, or repository helpers")


if __name__ == "__main__":
    main()
