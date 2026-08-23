"""Independent standard-library audit for the GLS36 exact control."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


ROOT_ROWS = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)
OUTSIDE = (
    (0, 1, 0),
    (0, 2, 2),
    (0, 3, 0),
    (0, 4, 2),
    (0, 5, 0),
    (1, 2, 1),
    (1, 3, 1),
    (1, 4, 2),
    (1, 5, 0),
    (2, 3, 0),
    (2, 4, 1),
    (2, 5, 2),
    (3, 4, 1),
    (3, 5, 0),
    (4, 5, 0),
)
OUTSIDE_MAP = {(left, right): colour for left, right, colour in OUTSIDE}

R0, R1, R2, R3 = range(4)
U0, U1, U2, U3, Q0, Q1 = range(4, 10)
PROBES = (R1, R2)
RESIDUAL = (Q0, Q1)
PORTS = (R0, R3, U0, U1, U2, U3)
BASE = RESIDUAL + PORTS


def edge_colour(left: int, right: int) -> int | None:
    if left > right:
        left, right = right, left
    if right < 4:
        return None
    if left < 4:
        return ROOT_ROWS[left][right - 4]
    return OUTSIDE_MAP[(left - 4, right - 4)]


def incidence(probe: int, vertex: int, test_colour: int | None) -> int | None:
    colour = edge_colour(probe, vertex)
    if colour is None:
        return None
    if test_colour is None or test_colour == colour:
        return colour
    return None


def raw_column(pair: tuple[int, int], open_word: tuple[int, ...]) -> tuple[int, ...]:
    tests = {}
    open_iter = iter(open_word)
    for vertex in pair:
        tests[vertex] = None if vertex in RESIDUAL else next(open_iter)
    answer = [0] * 9
    left, right = pair
    for swap in (False, True):
        first, second = ((right, left) if swap else (left, right))
        c0 = incidence(PROBES[0], first, tests[first])
        c1 = incidence(PROBES[1], second, tests[second])
        if c0 is not None and c1 is not None:
            answer[3 * c0 + c1] += 1
    return tuple(answer)


def rank(columns: list[tuple[int, ...]]) -> int:
    if not columns:
        return 0
    matrix = [list(map(Fraction, row)) for row in zip(*columns, strict=True)]
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for column in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


@lru_cache(maxsize=None)
def deletion_deck(vertices: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    """Vertex-deletion matching recurrence returning the full word counter."""

    if not vertices:
        return Counter({(): 1})
    first = vertices[0]
    answer: Counter[tuple[int, ...]] = Counter()
    for index in range(1, len(vertices)):
        second = vertices[index]
        colour = edge_colour(first, second)
        if colour is None:
            continue
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail, coefficient in deletion_deck(remaining).items():
            reconstructed = [colour]
            tail_iter = iter(tail)
            for position in range(1, len(vertices)):
                reconstructed.append(colour if position == index else next(tail_iter))
            answer[tuple(reconstructed)] += coefficient
    return answer


def index(word: tuple[int, ...]) -> int:
    value = 0
    for colour in word:
        value = 3 * value + colour
    return value


def audit_raw_module() -> dict[str, object]:
    columns = []
    for pair in combinations(BASE, 2):
        if pair == RESIDUAL:
            continue
        degree = sum(vertex in PORTS for vertex in pair)
        columns.extend(raw_column(pair, word) for word in product(range(3), repeat=degree))
    assert len(columns) == 171
    q = raw_column(RESIDUAL, ())
    pure = [tuple(1 if position == 3 * colour + colour else 0 for position in range(9)) for colour in range(3)]
    e12 = tuple(1 if position == 5 else 0 for position in range(9))
    assert q == tuple(1 if position == 7 else 0 for position in range(9))
    assert rank(columns) == rank(columns + [q]) == 8
    assert all(rank(columns + [vector]) == 8 for vector in pure)
    assert rank(columns + [e12]) == 9
    assert raw_column((U0, U1), (2, 1)) == q
    assert raw_column((U2, Q1), (0,)) == pure[0]
    assert raw_column((U1, U3), (1, 1)) == pure[1]
    assert raw_column((U0, U3), (2, 2)) == pure[2]
    return {"columns": len(columns), "rank": rank(columns), "missing": "e12"}


def audit_state() -> dict[str, object]:
    full = deletion_deck(tuple(range(10)))
    assert len(full) == 119 and sum(full.values()) == 124
    assert all(full[(colour,) * 10] == 1 for colour in range(3))
    mixed = {word: value for word, value in full.items() if len(set(word)) != 1}
    assert len(mixed) == 116
    assert Counter(mixed.values()) == Counter({1: 111, 2: 5})

    complement = tuple(vertex for vertex in range(10) if vertex not in PROBES)
    flatten_columns: dict[tuple[int, ...], list[int]] = defaultdict(lambda: [0] * 9)
    for word, coefficient in full.items():
        probe_word = tuple(word[vertex] for vertex in PROBES)
        complement_word = tuple(word[vertex] for vertex in complement)
        flatten_columns[complement_word][index(probe_word)] += coefficient
    columns = [tuple(flatten_columns[word]) for word in sorted(flatten_columns)]
    assert rank(columns) == 8
    assert all(column[5] == 0 for column in columns)

    residual_absent = deletion_deck(PORTS)
    assert len(residual_absent) == 9
    assert set(residual_absent.values()) == {1}

    for outside in range(6):
        assert set(ROOT_ROWS[root][outside] for root in range(4)) == {0, 1, 2, None}
    for target in combinations((U0, U1, U2, U3), 2):
        assert sum(deletion_deck(RESIDUAL + target).values()) == 3
    assert sum(deletion_deck(RESIDUAL + (U0, U1, U2, U3)).values()) == 15

    return {
        "support": len(full),
        "mixed_failures": len(mixed),
        "flattening_rank": rank(columns),
        "H_support": len(residual_absent),
    }


def main() -> None:
    raw = audit_raw_module()
    state = audit_state()
    print("GLS36 independent no-import audit: PASS")
    print("  raw:", raw)
    print("  state:", state)


if __name__ == "__main__":
    main()
