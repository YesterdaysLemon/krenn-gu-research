"""Focused exact verifier for GLS36 incidence-image/lift sharpness."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import cache
from itertools import combinations, product

import sympy as sp


ROOT_TABLE = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)
OUTSIDE_COLOURS = {
    (0, 1): 0,
    (0, 2): 2,
    (0, 3): 0,
    (0, 4): 2,
    (0, 5): 0,
    (1, 2): 1,
    (1, 3): 1,
    (1, 4): 2,
    (1, 5): 0,
    (2, 3): 0,
    (2, 4): 1,
    (2, 5): 2,
    (3, 4): 1,
    (3, 5): 0,
    (4, 5): 0,
}

R0, R1, R2, R3 = range(4)
U0, U1, U2, U3, Q0, Q1 = range(4, 10)
A = (R1, R2)
Q = (Q0, Q1)
UHAT = (R0, R3, U0, U1, U2, U3)
BHAT = Q + UHAT
ORIGINAL_U = (U0, U1, U2, U3)
EYE = sp.eye(3)
E = tuple(EYE[:, colour] for colour in range(3))
ONE = sp.ones(3, 1)


def edge_block(left: int, right: int) -> sp.Matrix:
    """Return the exact coordinate-monomial edge block."""

    if left > right:
        return edge_block(right, left).T
    if right < 4:
        return sp.zeros(3)
    if left < 4:
        colour = ROOT_TABLE[left][right - 4]
    else:
        colour = OUTSIDE_COLOURS[(left - 4, right - 4)]
    if colour is None:
        return sp.zeros(3)
    return E[colour] * E[colour].T


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def raw_slice(pair: tuple[int, int], colours: tuple[int, ...]) -> sp.Matrix:
    """Return one GLS35 coefficient slice of g_D(z_Q)."""

    vectors: dict[int, sp.Matrix] = {}
    colour_iter = iter(colours)
    for vertex in pair:
        vectors[vertex] = ONE if vertex in Q else E[next(colour_iter)]
    left, right = pair
    return tensor(
        edge_block(A[0], left) * vectors[left],
        edge_block(A[1], right) * vectors[right],
    ) + tensor(
        edge_block(A[0], right) * vectors[right],
        edge_block(A[1], left) * vectors[left],
    )


def raw_anchor_matrix() -> tuple[sp.Matrix, sp.Matrix]:
    q = raw_slice(Q, ())
    columns: list[sp.Matrix] = []
    for pair in combinations(BHAT, 2):
        if pair == Q:
            continue
        open_count = sum(vertex in UHAT for vertex in pair)
        for colours in product(range(3), repeat=open_count):
            columns.append(raw_slice(pair, colours))
    assert len(columns) == 171
    return sp.Matrix.hstack(*columns), q


@cache
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def coordinate_entry(block: sp.Matrix) -> tuple[int, int] | None:
    entries = [
        (left, right)
        for left in range(3)
        for right in range(3)
        if block[left, right] != 0
    ]
    if not entries:
        return None
    assert len(entries) == 1
    return entries[0]


def word_counter(vertices: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    position = {vertex: index for index, vertex in enumerate(vertices)}
    answer: Counter[tuple[int, ...]] = Counter()
    for matching in perfect_matchings(vertices):
        word: list[int | None] = [None] * len(vertices)
        for left, right in matching:
            entry = coordinate_entry(edge_block(left, right))
            if entry is None:
                break
            left_colour, right_colour = entry
            word[position[left]] = left_colour
            word[position[right]] = right_colour
        else:
            assert all(colour is not None for colour in word)
            answer[tuple(word)] += 1  # type: ignore[arg-type]
    return answer


def ternary_index(word: tuple[int, ...]) -> int:
    value = 0
    for colour in word:
        value = 3 * value + colour
    return value


def flattening(full: Counter[tuple[int, ...]]) -> sp.Matrix:
    complement = tuple(vertex for vertex in range(10) if vertex not in A)
    columns: dict[tuple[int, ...], sp.Matrix] = defaultdict(lambda: sp.zeros(9, 1))
    for word, coefficient in full.items():
        a_word = tuple(word[vertex] for vertex in A)
        other_word = tuple(word[vertex] for vertex in complement)
        columns[other_word][ternary_index(a_word)] += coefficient
    return sp.Matrix.hstack(*(columns[word] for word in sorted(columns)))


def check_incidence_image() -> dict[str, object]:
    nuisance, q = raw_anchor_matrix()
    pure = [tensor(E[colour], E[colour]) for colour in range(3)]
    missing = tensor(E[1], E[2])

    assert q == tensor(E[2], E[1])
    assert (tensor(ONE, ONE).T * q)[0] == 1
    assert nuisance.rank() == nuisance.row_join(q).rank() == 8
    assert [nuisance.row_join(vector).rank() for vector in pure] == [8, 8, 8]
    assert nuisance.row_join(missing).rank() == 9

    # Eight literal single-slice basis certificates, including q and the pure rows.
    assert raw_slice((U2, Q1), (0,)) == pure[0]
    assert raw_slice((Q1, U1), (1,)) == tensor(E[0], E[1])
    assert raw_slice((Q1, U3), (2,)) == tensor(E[0], E[2])
    assert raw_slice((U2, U3), (0, 1)) == tensor(E[1], E[0])
    assert raw_slice((U1, U3), (1, 1)) == pure[1]
    assert raw_slice((Q0, U2), (0,)) == tensor(E[2], E[0])
    assert raw_slice((U0, U1), (2, 1)) == q
    assert raw_slice((U0, U3), (2, 2)) == pure[2]

    expected_support = set(range(9)) - {ternary_index((1, 2))}
    actual_support = {
        row
        for row in range(9)
        if any(nuisance[row, column] for column in range(nuisance.cols))
    }
    assert actual_support == expected_support
    return {
        "raw_shape": nuisance.shape,
        "raw_rank": nuisance.rank(),
        "missing_coordinate": "e12",
    }


def check_state_and_flattening() -> dict[str, object]:
    full = word_counter(tuple(range(10)))
    assert len(full) == 119
    assert sum(full.values()) == 124
    for colour in range(3):
        assert full[(colour,) * 10] == 1
        for vertex in range(10):
            for other in set(range(3)) - {colour}:
                word = [colour] * 10
                word[vertex] = other
                assert full[tuple(word)] == 0

    mixed = {word: value for word, value in full.items() if len(set(word)) > 1}
    assert len(mixed) == 116
    assert Counter(mixed.values()) == Counter({1: 111, 2: 5})
    assert sorted("".join(map(str, word)) for word, value in mixed.items() if value == 2) == [
        "0100000100",
        "0200000020",
        "0200200000",
        "0221201200",
        "2210012020",
    ]

    matrix = flattening(full)
    assert matrix.rank() == 8
    assert {
        row for row in range(9) if any(matrix[row, column] for column in range(matrix.cols))
    } == set(range(9)) - {ternary_index((1, 2))}

    residual_absent = word_counter(UHAT)
    assert len(residual_absent) == 9
    assert set(residual_absent.values()) == {1}
    assert sum(residual_absent.values()) == 9
    return {
        "full_support": len(full),
        "full_matching_count": sum(full.values()),
        "mixed_failures": len(mixed),
        "flattening_rank": matrix.rank(),
        "residual_absent_support": len(residual_absent),
    }


def check_source_gates_and_silence() -> dict[str, object]:
    # Every outside vertex has the three coordinate rows and one zero root row.
    for outside in range(6):
        assert set(ROOT_TABLE[root][outside] for root in range(4)) == {0, 1, 2, None}
    assert len(OUTSIDE_COLOURS) == 15

    response_totals = {}
    for target in combinations(ORIGINAL_U, 2):
        counter = word_counter(Q + target)
        response_totals[target] = sum(counter.values())
        assert response_totals[target] == 3
    four_port = word_counter(Q + ORIGINAL_U)
    response_totals[ORIGINAL_U] = sum(four_port.values())
    assert response_totals[ORIGINAL_U] == 15

    # Local constant-anchor kernels on Uhat.  The base-root ports have zero rows.
    local_row_support = {}
    for port in UHAT:
        rows = []
        for probe in A:
            evaluated = edge_block(probe, port).T * ONE
            rows.append(tuple(evaluated))
        local_row_support[port] = rows
    assert local_row_support[R0] == [(0, 0, 0), (0, 0, 0)]
    assert local_row_support[R3] == [(0, 0, 0), (0, 0, 0)]
    assert local_row_support[U0] == [(0, 0, 1), (0, 0, 0)]
    assert local_row_support[U1] == [(0, 0, 0), (0, 1, 0)]
    assert local_row_support[U2] == [(0, 0, 0), (1, 0, 0)]
    assert local_row_support[U3] == [(0, 1, 0), (0, 0, 1)]
    # Colours 2, 1, and 0 are killed respectively at u0, u1, and u2.

    return {
        "pair_response_totals": sorted(response_totals[target] for target in combinations(ORIGINAL_U, 2)),
        "four_port_response_total": response_totals[ORIGINAL_U],
        "diagonal_anchor": "silent",
    }


def main() -> None:
    incidence = check_incidence_image()
    state = check_state_and_flattening()
    source = check_source_gates_and_silence()
    print("GLS36 incidence-image/common-row/lift sharpness primary checks: PASS")
    print("  incidence:", incidence)
    print("  state:", state)
    print("  source/silence:", source)


if __name__ == "__main__":
    main()
