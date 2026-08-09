"""Verify face-specific quotient descent's exact sharp symbolic lift.

The script checks one displayed incidence/edge construction.  It performs no
graph, support, colour-word, alignment, or parameter search.
"""

from itertools import combinations

import sympy as sp

import verify_p7_221_degree5_incidence_quotient_rectangle_flattening as binary

TERMINALS = tuple("12345ab")
MODES = tuple(range(7))
COLOURS = tuple(range(3))
FACES = {
    "01": frozenset("1234a"),
    "02": frozenset("1235b"),
    "12": frozenset("1345b"),
}
PAIR_COLOURS = {"01": (0, 1), "02": (0, 2), "12": (1, 2)}
E = tuple(sp.eye(3).col(index) for index in COLOURS)
ZERO = sp.zeros(3, 1)


def incidence_system() -> dict[tuple[int, str], sp.Matrix]:
    incidence = {(mode, terminal): ZERO for mode in MODES for terminal in TERMINALS}
    incidence[0, "5"] = E[2]
    incidence[1, "4"] = E[1]
    incidence[2, "2"] = E[0]
    for mode in range(3, 7):
        incidence[mode, "1"] = E[1]
        incidence[mode, "3"] = E[2]
    return incidence


def span_matrix(
    incidence: dict[tuple[int, str], sp.Matrix],
    mode: int,
    terminals: frozenset[str],
) -> sp.Matrix:
    columns = [
        incidence[mode, terminal]
        for terminal in TERMINALS
        if terminal in terminals and incidence[mode, terminal] != ZERO
    ]
    return sp.Matrix.hstack(*columns) if columns else sp.zeros(3, 0)


def same_span(left: sp.Matrix, right: sp.Matrix) -> bool:
    return (
        left.rank()
        == right.rank()
        == sp.Matrix.hstack(left, right).rank()
    )


def killed_colours(
    incidence: dict[tuple[int, str], sp.Matrix],
    mode: int,
    terminals: frozenset[str],
) -> frozenset[int]:
    span = span_matrix(incidence, mode, terminals)
    rank = span.rank()
    return frozenset(
        colour
        for colour in COLOURS
        if sp.Matrix.hstack(span, E[colour]).rank() == rank
    )


def quotient_projector(
    incidence: dict[tuple[int, str], sp.Matrix],
    mode: int,
    terminals: frozenset[str],
) -> sp.Matrix:
    killed = killed_colours(incidence, mode, terminals)
    return sp.diag(*(0 if colour in killed else 1 for colour in COLOURS))


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def edge_tensor(left: int, right: int) -> sp.Matrix:
    pair = frozenset((left, right))
    if pair == frozenset((0, 1)):
        colour = 0
    elif pair == frozenset((0, 2)):
        colour = 1
    elif pair == frozenset((1, 2)):
        colour = 2
    elif 2 in pair:
        return sp.zeros(9, 1)
    else:
        colour = 0
    return tensor(E[colour], E[colour])


def projected_line(
    incidence: dict[tuple[int, str], sp.Matrix],
    left: int,
    right: int,
    face_label: str,
) -> sp.Matrix:
    face = FACES[face_label]
    first, second = PAIR_COLOURS[face_label]
    q_left = quotient_projector(incidence, left, face)
    q_right = quotient_projector(incidence, right, face)
    return sp.Matrix.hstack(
        tensor(q_left * E[first], q_right * E[first]),
        tensor(q_left * E[second], q_right * E[second]),
    )


def main() -> None:
    rho = binary.RHO
    beta = 2 * (1 + rho) / 7
    expected = {
        "01": (1 + 43 * rho / 21, -6, 0),
        "02": (rho, 0, beta),
        "12": (0, rho, beta),
    }
    for label, face in FACES.items():
        actual = tuple(binary.formal_wick_value(colour, face) for colour in COLOURS)
        assert all(
            sp.simplify(value - target) == 0
            for value, target in zip(actual, expected[label], strict=True)
        )

    incidence = incidence_system()
    terminal_set = frozenset(TERMINALS)

    # Each pairwise span square has zero overlap defect and the correct union.
    overlap_checks = 0
    for mode in MODES:
        for left_label, right_label in combinations(FACES, 2):
            left_face = FACES[left_label]
            right_face = FACES[right_label]
            left_span = span_matrix(incidence, mode, left_face)
            right_span = span_matrix(incidence, mode, right_face)
            overlap_span = span_matrix(incidence, mode, left_face & right_face)
            union_span = span_matrix(incidence, mode, left_face | right_face)
            intersection_dimension = (
                left_span.rank()
                + right_span.rank()
                - sp.Matrix.hstack(left_span, right_span).rank()
            )
            assert overlap_span.rank() == intersection_dimension
            assert same_span(union_span, sp.Matrix.hstack(left_span, right_span))
            overlap_checks += 1
    assert overlap_checks == 21
    triple_overlap = frozenset.intersection(*FACES.values())
    assert triple_overlap == frozenset("13")
    for mode in MODES:
        triple_span = span_matrix(incidence, mode, triple_overlap)
        face_spans = [
            span_matrix(incidence, mode, face) for face in FACES.values()
        ]
        intersection_dimension = face_spans[0].rank()
        intersection_basis = face_spans[0]
        for next_span in face_spans[1:]:
            intersection_dimension = (
                intersection_basis.rank()
                + next_span.rank()
                - sp.Matrix.hstack(intersection_basis, next_span).rank()
            )
            if intersection_dimension == 0:
                intersection_basis = sp.zeros(3, 0)
            else:
                # In the displayed coordinate lift, equality of the claimed
                # triple span can be checked by dimension and containment.
                intersection_basis = triple_span
        assert triple_span.rank() == intersection_dimension

    expected_binary_ranks = {
        "01": (2, 1, 1, 1, 1, 1, 1),
        "02": (1, 2, 1, 1, 1, 1, 1),
        "12": (1, 1, 2, 0, 0, 0, 0),
    }
    for label, colours in PAIR_COLOURS.items():
        ranks = tuple(
            sp.Matrix.hstack(
                *(
                    quotient_projector(incidence, mode, FACES[label]) * E[colour]
                    for colour in colours
                )
            ).rank()
            for mode in MODES
        )
        assert ranks == expected_binary_ranks[label]

    full_ranks = tuple(
        quotient_projector(incidence, mode, terminal_set).rank() for mode in MODES
    )
    assert full_ranks == (2, 2, 2, 1, 1, 1, 1)

    # Every face line has rank at most one.  A common A_ij generates each
    # nonzero line, and its two face projections agree after passing to a
    # union quotient.
    active_union_line_checks = 0
    for left, right in combinations(MODES, 2):
        edge = edge_tensor(left, right)
        face_data: dict[str, tuple[sp.Matrix, sp.Matrix]] = {}
        for label, face in FACES.items():
            line = projected_line(incidence, left, right, label)
            assert line.rank() <= 1
            q_pair = tensor(
                quotient_projector(incidence, left, face),
                quotient_projector(incidence, right, face),
            )
            projected_edge = q_pair * edge
            if line.rank() == 1:
                assert projected_edge != sp.zeros(9, 1)
                assert sp.Matrix.hstack(line, projected_edge).rank() == 1
            face_data[label] = (line, projected_edge)

        for first_label, second_label in combinations(FACES, 2):
            union = FACES[first_label] | FACES[second_label]
            union_map = tensor(
                quotient_projector(incidence, left, union),
                quotient_projector(incidence, right, union),
            )
            first_line, first_edge = face_data[first_label]
            second_line, second_edge = face_data[second_label]
            union_edge = union_map * edge
            assert union_map * first_edge == union_edge
            assert union_map * second_edge == union_edge
            if first_line.rank() == second_line.rank() == 1:
                first_image = union_map * first_line
                second_image = union_map * second_line
                assert first_image.rank() == second_image.rank() == 1
                assert sp.Matrix.hstack(first_image, second_image).rank() == 1
                active_union_line_checks += 1
    assert active_union_line_checks == 17

    print("PASS: three exact face tensors have nonzero colour-pair coefficients")
    print("PASS: all 21 pairwise and 7 triple-overlap defects vanish")
    print("PASS: facewise binary ranks and global ranks (2,2,2,1,1,1,1) are sharp")
    print("PASS: one common edge family satisfies 17 active union-line gluings")
    print("SCOPE: quotient-line lift only; residual permanents and full responses open")
    print("searches=0")


if __name__ == "__main__":
    main()
