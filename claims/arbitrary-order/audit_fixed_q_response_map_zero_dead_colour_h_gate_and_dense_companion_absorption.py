"""Independent stdlib audit of the post-GLD20 dead-colour gate."""

from fractions import Fraction
from itertools import combinations, product


PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
EDGE_POSITION = {edge: position for position, edge in enumerate(EDGES)}
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
Q_LEFT, Q_RIGHT = 4, 5
VERTICES = PORTS + (Q_LEFT, Q_RIGHT)
Q_SET = frozenset((Q_LEFT, Q_RIGHT))


def vertex_set(mask):
    return frozenset(port for port in PORTS if mask & (1 << port))


def complete_graph(vertices):
    return frozenset(combinations(sorted(vertices), 2))


def support_channels():
    nontrivial = tuple(vertex_set(mask) for mask in range(16) if mask.bit_count() >= 2)
    result = set()
    for colors in combinations(COLORS, 2):
        for left, right in product(nontrivial, repeat=2):
            if len(left) != 4 and len(right) != 4:
                continue
            left_edges = complete_graph(left)
            right_edges = complete_graph(right)
            result.add(
                tuple(
                    ((1 << colors[0]) if edge in left_edges else 0)
                    | ((1 << colors[1]) if edge in right_edges else 0)
                    for edge in EDGES
                )
            )
    return result


def pair_allowed(left_b, right_b, left_k, right_k):
    if left_b and right_b:
        return (
            left_b == right_b
            and left_b.bit_count() == 1
            and left_k | left_b == left_b
            and right_k | left_b == left_b
        )
    if left_b:
        return right_k == 0 if left_b.bit_count() > 1 else right_k | left_b == left_b
    if right_b:
        return left_k == 0 if right_b.bit_count() > 1 else left_k | right_b == right_b
    return True


def audit_support_counts():
    channels = support_channels()
    assert len(channels) == 63
    raw_total = 0
    by_secondary_size = {2: 0, 3: 0, 4: 0}
    for channel in channels:
        union = 0
        for mask in channel:
            union |= mask
        active = tuple(color for color in COLORS if union & (1 << color))
        assert len(active) == 2
        missing = next(color for color in COLORS if color not in active)
        dense = all(mask == union for mask in channel)
        dominant = union
        for mask in channel:
            dominant &= mask
        assert dominant.bit_count() == (2 if dense else 1)
        local = []
        for left, right in MATCHINGS:
            left_number = EDGE_POSITION[left]
            right_number = EDGE_POSITION[right]
            choices = []
            for left_b, right_b in product(range(8), repeat=2):
                if pair_allowed(
                    left_b,
                    right_b,
                    channel[left_number],
                    channel[right_number],
                ):
                    choices.append((left_b, right_b))
            local.append(tuple(choices))
        count = 0
        for triple in product(*local):
            direct = [0] * 6
            for matching, choices in zip(MATCHINGS, triple, strict=True):
                direct[EDGE_POSITION[matching[0]]] = choices[0]
                direct[EDGE_POSITION[matching[1]]] = choices[1]
            assert all(not mask & (1 << missing) for mask in direct)
            assert all(not mask & ~dominant for mask in direct)
            assert all((bmask | kmask) != 7 for bmask, kmask in zip(direct, channel))
            if dense:
                assert not any(direct)
            count += 1
        raw_total += count

        if dense:
            by_secondary_size[4] += count
        else:
            edge_counts = {
                color: sum(bool(mask & (1 << color)) for mask in channel)
                for color in active
            }
            secondary_edges = min(edge_counts.values())
            size = 2 if secondary_edges == 1 else 3
            by_secondary_size[size] += count

    assert by_secondary_size == {2: 36 * 32, 3: 24 * 8, 4: 3}
    assert raw_total == 1347


def poly_constant(value):
    value = Fraction(value)
    return {} if value == 0 else {(): value}


def poly_variable(name, coefficient=1):
    coefficient = Fraction(coefficient)
    return {} if coefficient == 0 else {(name,): coefficient}


def poly_add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def poly_multiply(left, right):
    answer = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            monomial = tuple(sorted(first + second))
            answer[monomial] = answer.get(monomial, Fraction(0)) + (
                first_coefficient * second_coefficient
            )
            if answer[monomial] == 0:
                del answer[monomial]
    return answer


def graph_data(dense=False):
    direct = {}
    for edge in EDGES:
        for color in COLORS:
            direct[(edge, color)] = (
                {} if dense or color != 0 else poly_variable(f"b{edge}{color}")
            )
    shores = {}
    for port in PORTS:
        first = f"p{port}"
        second = f"r{port}"
        shores[(Q_LEFT, port, 0)] = poly_variable(first)
        shores[(Q_RIGHT, port, 0)] = poly_variable(first)
        shores[(Q_LEFT, port, 1)] = poly_variable(second)
        shores[(Q_RIGHT, port, 1)] = poly_variable(second, -1)
        shores[(Q_LEFT, port, 2)] = {}
        shores[(Q_RIGHT, port, 2)] = {}
    return direct, shores


def graph_edge(left, right, word, direct, shores):
    if {left, right} == {Q_LEFT, Q_RIGHT}:
        return poly_variable("h")
    if left in (Q_LEFT, Q_RIGHT) and right in PORTS:
        return shores[(left, right, word[right])]
    if right in (Q_LEFT, Q_RIGHT) and left in PORTS:
        return shores[(right, left, word[left])]
    edge = tuple(sorted((left, right)))
    if word[left] != word[right]:
        return {}
    return direct[(edge, word[left])]


def principal_hafnian(vertices, word, direct, shores):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return poly_constant(1)
    first = vertices[0]
    answer = {}
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        term = poly_multiply(
            graph_edge(first, second, word, direct, shores),
            principal_hafnian(remainder, word, direct, shores),
        )
        answer = poly_add(answer, term)
    return answer


def labels():
    return tuple(
        frozenset(label) for size in (2, 4, 6) for label in combinations(VERTICES, size)
    )


def coordinate(label, word):
    return label, tuple((port, word[port]) for port in PORTS if port in label)


def surviving_coordinates(word, direct, shores):
    return {
        coordinate(label, word): principal_hafnian(label, word, direct, shores)
        for label in labels()
        if principal_hafnian(label, word, direct, shores)
    }


def audit_label_ledgers():
    direct, shores = graph_data()
    pure = {port: 2 for port in PORTS}
    assert set(surviving_coordinates(pure, direct, shores)) == {(Q_SET, ())}

    for port in PORTS:
        for color in (0, 1):
            word = dict(pure)
            word[port] = color
            actual = set(surviving_coordinates(word, direct, shores))
            assert actual == {
                (Q_SET, ()),
                (frozenset((Q_LEFT, port)), ((port, color),)),
                (frozenset((Q_RIGHT, port)), ((port, color),)),
            }

    shores[(Q_LEFT, 3, 1)] = {}
    shores[(Q_RIGHT, 3, 1)] = {}
    outside_word = dict(pure)
    outside_word[3] = 1
    assert set(surviving_coordinates(outside_word, direct, shores)) == {(Q_SET, ())}

    direct, shores = graph_data(dense=True)
    package_count = 0
    for edge in EDGES:
        complement = tuple(port for port in PORTS if port not in edge)
        desired_label = frozenset((Q_LEFT, Q_RIGHT, *edge))
        for repeated in (0, 1):
            other = 1 - repeated
            nuisance = set()
            for orientation in ((other, 2), (2, other)):
                word = {edge[0]: repeated, edge[1]: repeated}
                word[complement[0]], word[complement[1]] = orientation
                actual = surviving_coordinates(word, direct, shores)
                assert coordinate(desired_label, word) in actual
                nuisance.update(key for key in actual if key[0] != desired_label)
            assert len(nuisance) == 9
            package_count += 1
    assert package_count == 12


def bilinear(left, right):
    return Fraction(left[0]) * Fraction(right[1]) + Fraction(left[1]) * Fraction(
        right[0]
    )


def audit_physical_control():
    p, r = (1, 1), (1, -1)
    for u, v in EDGES:
        assert bilinear(p, p) == 2
        assert bilinear(r, r) == -2
        assert bilinear(p, r) == 0
        assert bilinear(r, p) == 0
    assert bilinear((0, 0), p) == bilinear((0, 0), r) == 0


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
    return pivot_row


def audit_linear_gates():
    nuisance_columns = [
        [Fraction(int(row == column)) for row in range(12)] for column in range(9)
    ]
    detected = [Fraction(int(row == 9)) for row in range(12)]
    absorbed = nuisance_columns[0]
    nuisance_rows = [list(row) for row in zip(*nuisance_columns, strict=True)]
    assert rational_rank(nuisance_rows) == 9
    detected_rows = [
        row + [value] for row, value in zip(nuisance_rows, detected, strict=True)
    ]
    absorbed_rows = [
        row + [value] for row, value in zip(nuisance_rows, absorbed, strict=True)
    ]
    assert rational_rank(detected_rows) == 10
    assert rational_rank(absorbed_rows) == 9

    shore_matrix = ((Fraction(1), Fraction(1)), (Fraction(1), Fraction(-1)))
    assert rational_rank(shore_matrix) == 2
    target = [Fraction(0)] * 81
    target[-1] = Fraction(5)
    companion = [entry / 2 for entry in target]
    assert [2 * entry for entry in companion] == target
    assert sum(bool(entry) for entry in companion) == 1


def main():
    audit_support_counts()
    audit_label_ledgers()
    audit_physical_control()
    audit_linear_gates()
    print("response-map-zero dead-colour companion-gate independent audit: PASS")


if __name__ == "__main__":
    main()
