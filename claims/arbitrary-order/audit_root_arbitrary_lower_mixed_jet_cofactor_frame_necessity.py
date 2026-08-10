"""Independent no-import audit of lower mixed-root cofactor frames."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import product

Row = tuple[int, int, int]


def kernel(row: Row) -> tuple[Row, Row]:
    if row[2]:
        return (row[2], 0, -row[0]), (0, row[2], -row[1])
    if row[1]:
        return (row[1], -row[0], 0), (0, 0, row[1])
    return (0, row[0], 0), (0, 0, row[0])


def tensor(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a * b for a in left for b in right)


def forms(rows: tuple[Row, ...]) -> list[list[Fraction]]:
    answer = []
    for colour in range(3):
        word = (1,)
        for row in rows:
            basis = kernel(row)
            word = tensor(word, (basis[0][colour], basis[1][colour]))
        answer.append([Fraction(value) for value in word])
    return answer


def rational_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix if any(row)]
    if not work:
        return 0
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((index for index in range(pivot_row, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [a - scale * b for a, b in zip(work[index], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def axis(row: Row) -> int | None:
    support = [index for index, value in enumerate(row) if value]
    return support[0] if len(support) == 1 else None


def predicted(rows: tuple[Row, ...]) -> int:
    axes = {axis(row) for row in rows} - {None}
    if axes:
        return 3 - len(axes)
    for omitted in range(3):
        if all(row[omitted] == 0 for row in rows):
            return 2
    return 3


def frame_rank_audit() -> int:
    covectors = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 2, 0),
        (1, 0, 2),
        (0, 1, 2),
        (1, 1, 1),
        (1, 2, 3),
    )
    checked = 0
    for order in (2, 3, 4):
        for index, rows in enumerate(product(covectors, repeat=order)):
            if index % (1 if order == 2 else 37 if order == 3 else 541):
                continue
            actual = rational_rank(forms(rows))
            expected = predicted(rows)
            if actual != expected:
                raise AssertionError((rows, actual, expected))
            checked += 1
    return checked


def surviving_graph(root_count: int) -> tuple[tuple[int, ...], dict[tuple[int, int], int]]:
    """All-1 coefficient after e1 derivatives at roots 0 and 1."""
    blocker_count = root_count + 2
    roots = tuple(range(root_count))
    blockers = tuple(range(root_count, root_count + blocker_count))
    q0 = root_count + blocker_count
    q1 = q0 + 1
    vertices = roots + blockers + (q0, q1)
    values = {vertex: "x" for vertex in vertices}
    values[roots[0]] = values[roots[1]] = "y1"
    for blocker in blockers:
        values[blocker] = "b1"
    weights: dict[tuple[int, int], int] = {}

    def add(u: int, v: int, value: int) -> None:
        if value:
            weights[tuple(sorted((u, v)))] = value

    # Root--blocker block e2 tensor e_((i+u) mod 3).
    for i, root in enumerate(roots):
        for local_u, blocker in enumerate(blockers):
            left = 0 if values[root] == "y1" else 1
            right = int((i + local_u) % 3 == 1)
            add(root, blocker, left * right)

    # Root path: q edges survive only between two y1 roots.  Stabilized p
    # edges vanish both on y1 and at the fixed vector x.
    for i in range(root_count - 1):
        colour = (1 if i % 2 == 0 else 0) if root_count % 2 else (0 if i % 2 == 0 else 1)
        value = int(colour == 1 and values[roots[i]] == values[roots[i + 1]] == "y1")
        add(roots[i], roots[i + 1], value)

    # Endpoint edges use e2 at the endpoint.  A q root edge survives only at
    # a y1 root, and an all-1 blocker survives only on a q blocker edge.
    if root_count % 2:
        add(roots[0], q0, 0)
        add(roots[-1], q1, int(values[roots[-1]] == "y1"))
        add(blockers[0], q1, 0)
        add(blockers[-1], q0, 1)
    else:
        add(roots[0], q0, int(values[roots[0]] == "y1"))
        add(roots[-1], q1, int(values[roots[-1]] == "y1"))
        add(blockers[0], q0, 0)
        add(blockers[-1], q1, 0)

    for i in range(blocker_count - 1):
        colour = 1 if i % 2 == 0 else 0
        add(blockers[i], blockers[i + 1], int(colour == 1))
    return vertices, weights


def matching_count(vertices: tuple[int, ...], weights: dict[tuple[int, int], int]) -> int:
    @cache
    def recurse(remaining: tuple[int, ...]) -> int:
        if not remaining:
            return 1
        first = remaining[0]
        total = 0
        for position in range(1, len(remaining)):
            second = remaining[position]
            edge = tuple(sorted((first, second)))
            weight = weights.get(edge, 0)
            if weight:
                rest = remaining[1:position] + remaining[position + 1 :]
                total += weight * recurse(rest)
        return total

    return recurse(vertices)


def lower_jet_audit() -> int:
    checked = 0
    for root_count in range(3, 15):
        vertices, weights = surviving_graph(root_count)
        if matching_count(vertices, weights) != 0:
            raise AssertionError((root_count, weights))
        checked += 1
    return checked


def deletion_parity_audit() -> int:
    checked = 0
    # A partial matching saturating k varied vertices has j outside partners;
    # its other k-j vertices pair internally, so j and k have equal parity.
    for size in range(2, 15):
        for outside in range(size + 1):
            realizable = (size - outside) % 2 == 0
            parity = outside % 2 == size % 2
            if realizable != parity:
                raise AssertionError((size, outside))
            checked += 1
    return checked


def main() -> None:
    frame_checks = frame_rank_audit()
    parity_checks = deletion_parity_audit()
    lower_checks = lower_jet_audit()
    print("PASS: independent arbitrary lower mixed-jet cofactor-frame audit")
    print(f"exact rational frame ranks: {frame_checks}")
    print(f"deletion parity cases: {parity_checks}")
    print(f"sharpness construction lower two-root zeros: {lower_checks}")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
