"""Independent no-import audit for the GLS29 normal-channel theorem."""

from fractions import Fraction
from functools import cache
from itertools import combinations, product


def vector(values):
    return tuple(Fraction(value) for value in values)


def coordinate(index, dimension):
    return tuple(Fraction(int(index == slot)) for slot in range(dimension))


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(value, item):
    return tuple(value * entry for entry in item)


def rank(columns):
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


def kronecker(left, right):
    return tuple(a * b for a in left for b in right)


def audit_normal_quotient():
    basis3 = [coordinate(index, 3) for index in range(3)]
    basis9 = [coordinate(index, 9) for index in range(9)]
    q = add(basis9[1], basis9[3])
    p = sum(q)

    def project(item):
        return add(scale(p, item), scale(-sum(item), q))

    tangent_coordinates = sorted(
        {(i, j) for i in range(2) for j in range(3)}
        | {(i, j) for i in range(3) for j in range(2)}
    )
    tangent = [kronecker(basis3[i], basis3[j]) for i, j in tangent_coordinates]
    tangent_bar = [project(item) for item in tangent]
    transverse = [add(basis9[index], scale(-1, basis9[8])) for index in range(8)]
    assert p == 2
    assert rank(tangent) == 8
    assert rank(tangent_bar) == 7
    assert rank(transverse) == 8
    assert all(item[8] == 0 for item in tangent_bar)
    assert any(item[8] != 0 for item in transverse)
    return {
        "p": p,
        "tangent_rank": rank(tangent),
        "projected_tangent_rank": rank(tangent_bar),
        "transverse_rank": rank(transverse),
    }


@cache
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


def coefficient(word, edge):
    total = Fraction(0)
    for matching in matchings(tuple(range(len(word)))):
        term = Fraction(1)
        for left, right in matching:
            term *= edge(left, right, word[left], word[right])
        total += term
    return total


def audit_matching_laplace_identity():
    def edge(left, right, colour_left, colour_right):
        if left > right:
            return edge(right, left, colour_right, colour_left)
        if (left, right) == (0, 1):
            return Fraction(0)
        if left < 2:
            return Fraction((left + 2) * (right + 1) - colour_left + 2 * colour_right)
        return Fraction(1 + 3 * left - right + 2 * colour_left - colour_right)

    checked = 0
    for root_word in product(range(3), repeat=2):
        for port_word in product(range(3), repeat=4):
            direct = coefficient((*root_word, *port_word), edge)
            laplace = Fraction(0)
            for u, v in combinations(range(2, 6), 2):
                remainder = tuple(index for index in range(2, 6) if index not in (u, v))
                cu, cv = port_word[u - 2], port_word[v - 2]
                cross = edge(0, u, root_word[0], cu) * edge(
                    1, v, root_word[1], cv
                ) + edge(0, v, root_word[0], cv) * edge(1, u, root_word[1], cu)
                response = edge(
                    remainder[0],
                    remainder[1],
                    port_word[remainder[0] - 2],
                    port_word[remainder[1] - 2],
                )
                laplace += cross * response
            assert direct == laplace
            checked += 1
    return {
        "coefficients": checked,
        "six_vertex_matchings": len(matchings(tuple(range(6)))),
    }


def audit_support_classification():
    edges = tuple(combinations(range(6), 2))
    checked = 0
    for size in range(1, 7):
        for family in combinations(edges, size):
            if not all(set(a) & set(b) for a, b in combinations(family, 2)):
                continue
            common = set(family[0]).intersection(*(set(item) for item in family[1:]))
            vertices = set().union(*(set(item) for item in family))
            assert common or len(vertices) == 3
            checked += 1

    colours = frozenset(range(3))
    possible = [
        frozenset(items) for size in range(3) for items in combinations(range(3), size)
    ]
    patterns = []
    for item in product(possible, repeat=3):
        if all(item[i] | item[j] == colours for i, j in combinations(range(3), 2)):
            assert all(len(entry) == 2 for entry in item)
            assert {next(iter(colours - entry)) for entry in item} == colours
            patterns.append(item)
    assert len(patterns) == 6
    return {
        "intersecting_families": checked,
        "triangle_coordinate_patterns": len(patterns),
    }


def pair_channel(x, y, left, right):
    return tuple(
        x[left][i] * y[right][j] + y[left][i] * x[right][j]
        for i in range(3)
        for j in range(3)
    )


def audit_exchange_identity():
    x = (
        vector((1, 2, -1)),
        vector((0, 1, 3)),
        vector((2, -2, 1)),
        vector((1, 0, 2)),
    )
    y = (
        vector((2, 0, 1)),
        vector((-1, 2, 1)),
        vector((0, 3, -2)),
        vector((2, 1, 0)),
    )
    k01 = pair_channel(x, y, 0, 1)
    k23 = pair_channel(x, y, 2, 3)
    k03 = pair_channel(x, y, 0, 3)
    k12 = pair_channel(x, y, 1, 2)
    delta02 = tuple(
        x[0][i] * y[2][j] - y[0][i] * x[2][j] for i in range(3) for j in range(3)
    )
    delta13 = tuple(
        x[1][i] * y[3][j] - y[1][i] * x[3][j] for i in range(3) for j in range(3)
    )
    for word in product(range(3), repeat=4):
        left = (
            k01[3 * word[0] + word[1]] * k23[3 * word[2] + word[3]]
            - k03[3 * word[0] + word[3]] * k12[3 * word[1] + word[2]]
        )
        right = -delta02[3 * word[0] + word[2]] * delta13[3 * word[1] + word[3]]
        assert left == right
    return {"rational_coefficients": 81}


def audit_four_port_kernel_cases():
    x = (
        vector((1, 0, 2)),
        vector((0, 1, 1)),
        vector((2, 1, 0)),
        vector((1, -1, 0)),
    )
    y = (
        vector((0, 1, 1)),
        vector((1, 0, 2)),
        vector((0, 2, 1)),
        vector((1, 1, 2)),
    )

    def cross(left, right):
        return vector(
            (
                left[1] * right[2] - left[2] * right[1],
                left[2] * right[0] - left[0] * right[2],
                left[0] * right[1] - left[1] * right[0],
            )
        )

    kernels = tuple(cross(x[index], y[index]) for index in range(4))
    assert all(any(item) for item in kernels)
    responses = {
        pair: tuple(
            Fraction(1 + 2 * sum(pair) + row - 2 * column)
            for row in range(3)
            for column in range(3)
        )
        for pair in combinations(range(4), 2)
    }

    def bilinear(matrix_values, left, right):
        return sum(
            left[row] * matrix_values[3 * row + column] * right[column]
            for row, column in product(range(3), repeat=2)
        )

    for kept in combinations(range(4), 2):
        cut = tuple(index for index in range(4) if index not in kept)
        expected_scalar = bilinear(responses[cut], kernels[cut[0]], kernels[cut[1]])
        expected = scale(expected_scalar, pair_channel(x, y, *kept))
        observed = [Fraction(0) for _ in range(9)]
        for supplier in combinations(range(4), 2):
            complement = tuple(index for index in range(4) if index not in supplier)
            supplier_tensor = pair_channel(x, y, *supplier)
            for kept_word in product(range(3), repeat=2):
                value = Fraction(0)
                for cut_word in product(range(3), repeat=2):
                    word = [0] * 4
                    for port, colour in zip(kept, kept_word, strict=True):
                        word[port] = colour
                    for port, colour in zip(cut, cut_word, strict=True):
                        word[port] = colour
                    value += (
                        kernels[cut[0]][cut_word[0]]
                        * kernels[cut[1]][cut_word[1]]
                        * supplier_tensor[3 * word[supplier[0]] + word[supplier[1]]]
                        * responses[complement][
                            3 * word[complement[0]] + word[complement[1]]
                        ]
                    )
                observed[3 * kept_word[0] + kept_word[1]] += value
        assert tuple(observed) == expected

    nonempty = tuple(
        frozenset(items)
        for size in range(1, 4)
        for items in combinations(range(3), size)
    )
    support_cases = 0
    activity_compatible = 0
    for supports in product(nonempty, repeat=4):
        if not all(
            len(supports[i] & supports[j]) in (0, 2)
            for i, j in combinations(range(4), 2)
        ):
            continue
        two_supports = [item for item in set(supports) if len(item) == 2]
        assert any(supports.count(item) >= 3 for item in two_supports)
        support_cases += 1
        if all(sum(colour in item for item in supports) <= 2 for colour in range(3)):
            activity_compatible += 1
    assert activity_compatible == 0
    return {
        "independent_kernel_contractions": 6,
        "support_cases": support_cases,
        "activity_compatible": activity_compatible,
    }


def audit_same_graph_certificate():
    names = ("a0", "a1", "k", "q0", "q1", "u1", "u2", "u3")
    matrices = {}

    def zero_matrix():
        return tuple(tuple(Fraction(0) for _ in range(3)) for _ in range(3))

    def put(left, right, rows):
        i, j = names.index(left), names.index(right)
        value = tuple(tuple(Fraction(entry) for entry in row) for row in rows)
        if i < j:
            matrices[(i, j)] = value
        else:
            matrices[(j, i)] = tuple(zip(*value, strict=True))

    for left, right in combinations(names, 2):
        put(left, right, zero_matrix())
    e00 = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
    e10 = ((0, 0, 0), (1, 0, 0), (0, 0, 0))
    for root in ("a0", "a1"):
        put(root, "q0", e00)
        put(root, "q1", e10)
    data = {
        ("a0", "k"): ((-1, -1, -1), (1, 0, 1), (1, 1, -1)),
        ("a1", "k"): ((-1, 1, 1), (-1, -1, 0), (1, -1, 1)),
        ("a0", "u1"): ((1, 0, 0), (1, 1, 1), (1, -1, 1)),
        ("a0", "u2"): ((-1, 1, -1), (-1, -1, -1), (-1, 1, -1)),
        ("a0", "u3"): ((0, 0, 0), (1, -1, 1), (-1, 1, 0)),
        ("a1", "u1"): ((1, -1, 0), (-1, 0, 0), (-1, -1, 1)),
        ("a1", "u2"): ((-1, -1, -1), (-1, 0, 0), (1, 0, 0)),
        ("a1", "u3"): ((-1, 1, 1), (-1, 1, 0), (0, -1, 0)),
        ("k", "u1"): ((-1, -1, -1), (0, -1, 1), (1, 0, 0)),
        ("k", "u2"): ((1, -1, 1), (-1, 1, 1), (-1, 0, 1)),
        ("k", "u3"): ((0, 1, 1), (0, 1, 0), (1, 0, -1)),
    }
    for endpoints, rows in data.items():
        put(*endpoints, rows)
    put("k", "q0", ((0, 1, 0), (0, 0, 0), (0, 0, 0)))
    put("k", "q1", ((0, 0, 1), (0, 0, 0), (0, 0, 0)))
    put("q0", "q1", ((Fraction(-1, 2), 0, 0), (0, Fraction(1, 2), 0), (0, 0, 1)))
    e01 = ((0, 1, 0), (0, 0, 0), (0, 0, 0))
    for left, right in (("u1", "u2"), ("u1", "u3"), ("u2", "u3")):
        put(left, right, e01)

    def edge(left, right, colour_left, colour_right):
        if left < right:
            return matrices[(left, right)][colour_left][colour_right]
        return matrices[(right, left)][colour_right][colour_left]

    q = [Fraction(0) for _ in range(9)]
    for a0, a1, q0, q1 in product(range(3), repeat=4):
        q[3 * a0 + a1] += edge(0, 3, a0, q0) * edge(1, 4, a1, q1) + edge(
            0, 4, a0, q1
        ) * edge(1, 3, a1, q0)
    assert q == [Fraction(int(index in (1, 3))) for index in range(9)]
    p = sum(q)

    promoted = (2, 5, 6, 7)
    supplier_ranks = []
    for u, v in combinations(promoted, 2):
        columns = []
        for cu, cv in product(range(3), repeat=2):
            raw = []
            for a0, a1 in product(range(3), repeat=2):
                raw.append(
                    edge(0, u, a0, cu) * edge(1, v, a1, cv)
                    + edge(0, v, a0, cv) * edge(1, u, a1, cu)
                )
            epsilon = sum(raw)
            columns.append(
                tuple(p * raw[index] - q[index] * epsilon for index in range(9))
            )
        supplier_ranks.append(rank(columns))
    assert supplier_ranks == [8] * 6

    pure = tuple(coefficient((colour,) * 8, edge) for colour in range(3))
    failed = coefficient((0, 0, 0, 0, 0, 0, 1, 0), edge)
    assert pure == (Fraction(1), Fraction(1), Fraction(1))
    assert failed == Fraction(-3, 2)
    return {
        "p": p,
        "supplier_ranks": tuple(supplier_ranks),
        "pure": pure,
        "failed_hamming_one": failed,
    }


def main():
    print("zero-anchor normal-channel independent audit: PASS")
    print("  quotient from coordinate supports:", audit_normal_quotient())
    print("  recursive matching/Laplace identity:", audit_matching_laplace_identity())
    print("  support classification:", audit_support_classification())
    print("  four-port kernel cases:", audit_four_port_kernel_cases())
    print("  rational exchange identity:", audit_exchange_identity())
    print("  independently replayed graph certificate:", audit_same_graph_certificate())
    print("  no imports from primary verifier, SymPy, or repository helpers")


if __name__ == "__main__":
    main()
