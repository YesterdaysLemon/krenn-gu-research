"""Independent no-import audit of the face-quotient sharp lift."""

from fractions import Fraction
from itertools import combinations

TERMINALS = tuple("12345ab")
MODES = tuple(range(7))
COLOURS = tuple(range(3))
FACES = {
    "01": frozenset("1234a"),
    "02": frozenset("1235b"),
    "12": frozenset("1345b"),
}
PAIR_COLOURS = {"01": (0, 1), "02": (0, 2), "12": (1, 2)}
ZERO3 = (Fraction(0),) * 3
E = tuple(
    tuple(Fraction(row == column) for row in COLOURS) for column in COLOURS
)


def quadratic_norm(value):
    rational, radical = value
    return rational * rational - 21 * radical * radical


def incidence_axes():
    axes = {(mode, terminal): frozenset() for mode in MODES for terminal in TERMINALS}
    axes[0, "5"] = frozenset((2,))
    axes[1, "4"] = frozenset((1,))
    axes[2, "2"] = frozenset((0,))
    for mode in range(3, 7):
        axes[mode, "1"] = frozenset((1,))
        axes[mode, "3"] = frozenset((2,))
    return axes


def span_axes(incidence, mode, terminals):
    result = frozenset()
    for terminal in terminals:
        result |= incidence[mode, terminal]
    return result


def quotient_vector(incidence, mode, terminals, colour):
    if colour in span_axes(incidence, mode, terminals):
        return ZERO3
    return E[colour]


def tensor(left, right):
    return tuple(value * other for value in left for other in right)


def rank(columns):
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns)]
    column_count = len(columns)
    result = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(result, len(rows)) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        pivot_value = rows[result][column]
        rows[result] = [value / pivot_value for value in rows[result]]
        for row in range(len(rows)):
            if row == result or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[row], rows[result])
            ]
        result += 1
    return result


def project_tensor(incidence, left, right, terminals, value):
    killed_left = span_axes(incidence, left, terminals)
    killed_right = span_axes(incidence, right, terminals)
    return tuple(
        Fraction(0) if row in killed_left or column in killed_right else entry
        for row in COLOURS
        for column, entry in enumerate(value[3 * row : 3 * row + 3])
    )


def edge_tensor(left, right):
    pair = frozenset((left, right))
    if pair == frozenset((0, 1)):
        colour = 0
    elif pair == frozenset((0, 2)):
        colour = 1
    elif pair == frozenset((1, 2)):
        colour = 2
    elif 2 in pair:
        return (Fraction(0),) * 9
    else:
        colour = 0
    return tensor(E[colour], E[colour])


def face_line(incidence, left, right, label):
    first, second = PAIR_COLOURS[label]
    return (
        tensor(
            quotient_vector(incidence, left, FACES[label], first),
            quotient_vector(incidence, right, FACES[label], first),
        ),
        tensor(
            quotient_vector(incidence, left, FACES[label], second),
            quotient_vector(incidence, right, FACES[label], second),
        ),
    )


def main():
    assert quadratic_norm((Fraction(1), Fraction(43, 21))) == Fraction(-1828, 21)
    assert quadratic_norm((Fraction(0), Fraction(1))) == -21
    assert quadratic_norm((Fraction(2, 7), Fraction(2, 7))) == Fraction(-80, 49)

    incidence = incidence_axes()
    terminal_set = frozenset(TERMINALS)
    overlap_checks = 0
    for mode in MODES:
        for first_label, second_label in combinations(FACES, 2):
            first = FACES[first_label]
            second = FACES[second_label]
            first_span = span_axes(incidence, mode, first)
            second_span = span_axes(incidence, mode, second)
            assert first_span & second_span == span_axes(
                incidence, mode, first & second
            )
            assert first_span | second_span == span_axes(
                incidence, mode, first | second
            )
            overlap_checks += 1
    assert overlap_checks == 21
    triple_overlap = frozenset.intersection(*FACES.values())
    assert triple_overlap == frozenset("13")
    for mode in MODES:
        triple_span = span_axes(incidence, mode, triple_overlap)
        face_spans = [span_axes(incidence, mode, face) for face in FACES.values()]
        assert face_spans[0] & face_spans[1] & face_spans[2] == triple_span

    expected_binary_ranks = {
        "01": (2, 1, 1, 1, 1, 1, 1),
        "02": (1, 2, 1, 1, 1, 1, 1),
        "12": (1, 1, 2, 0, 0, 0, 0),
    }
    for label, colours in PAIR_COLOURS.items():
        actual = tuple(
            rank(
                tuple(
                    quotient_vector(incidence, mode, FACES[label], colour)
                    for colour in colours
                )
            )
            for mode in MODES
        )
        assert actual == expected_binary_ranks[label]
    assert tuple(
        3 - len(span_axes(incidence, mode, terminal_set)) for mode in MODES
    ) == (2, 2, 2, 1, 1, 1, 1)

    active_union_line_checks = 0
    for left, right in combinations(MODES, 2):
        edge = edge_tensor(left, right)
        lines = {}
        projected_edges = {}
        for label, face in FACES.items():
            line = face_line(incidence, left, right, label)
            assert rank(line) <= 1
            projected_edge = project_tensor(
                incidence, left, right, face, edge
            )
            if rank(line) == 1:
                assert rank((projected_edge,)) == 1
                assert rank(line + (projected_edge,)) == 1
            lines[label] = line
            projected_edges[label] = projected_edge

        for first_label, second_label in combinations(FACES, 2):
            union = FACES[first_label] | FACES[second_label]
            union_edge = project_tensor(incidence, left, right, union, edge)
            assert project_tensor(
                incidence,
                left,
                right,
                union,
                projected_edges[first_label],
            ) == union_edge
            assert project_tensor(
                incidence,
                left,
                right,
                union,
                projected_edges[second_label],
            ) == union_edge
            if rank(lines[first_label]) == rank(lines[second_label]) == 1:
                first_image = tuple(
                    project_tensor(incidence, left, right, union, column)
                    for column in lines[first_label]
                )
                second_image = tuple(
                    project_tensor(incidence, left, right, union, column)
                    for column in lines[second_label]
                )
                assert rank(first_image) == rank(second_image) == 1
                assert rank(first_image + second_image) == 1
                active_union_line_checks += 1
    assert active_union_line_checks == 17

    print("AUDIT PASS: exact coefficient norms are nonzero")
    print("AUDIT PASS: 21 pairwise and 7 triple-overlap defects vanish")
    print("AUDIT PASS: all facewise and global quotient ranks are sharp")
    print("AUDIT PASS: common edge tensors pass 17 active union-line tests")
    print("SCOPE: no residual-permanent or full-response claim")
    print("searches=0")


if __name__ == "__main__":
    main()
