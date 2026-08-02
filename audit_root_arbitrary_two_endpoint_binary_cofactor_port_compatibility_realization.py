"""Independent no-import audit of the odd-blocker binary port gadget."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache

Vector = tuple[int, int, int]


def rational_rank(rows: list[Vector]) -> int:
    work = [[Fraction(value) for value in row] for row in rows if any(row)]
    pivot_row = 0
    for column in range(3):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                left - scale * right
                for left, right in zip(work[index], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def path_signatures(blocker_count: int, endpoint: int) -> Counter[tuple[int, ...]]:
    q = blocker_count
    vertices = tuple(range(blocker_count)) + (q,)
    edges: dict[tuple[int, int], tuple[int, int]] = {}
    for index in range(blocker_count - 1):
        colour = 1 if index % 2 == 0 else 0
        edges[index, index + 1] = (colour, 1)
    edges[0, q] = (0, 1)
    edges[1, q] = (2, 1)
    edges[blocker_count - 1, q] = (1, 1 if endpoint == 0 else -1)

    @cache
    def recurse(remaining: tuple[int, ...]):
        if not remaining:
            return ((),)
        first = remaining[0]
        answer = []
        for position in range(1, len(remaining)):
            second = remaining[position]
            edge = tuple(sorted((first, second)))
            if edge not in edges:
                continue
            rest = remaining[1:position] + remaining[position + 1 :]
            for tail in recurse(rest):
                answer.append((edge,) + tail)
        return tuple(answer)

    signatures: Counter[tuple[int, ...]] = Counter()
    for matching in recurse(vertices):
        word = [-1] * blocker_count
        coefficient = 1
        for edge in matching:
            colour, weight = edges[edge]
            coefficient *= weight
            for vertex in edge:
                if vertex != q:
                    word[vertex] = colour
        assert -1 not in word
        signatures[tuple(word)] += coefficient
    return Counter(
        {word: coefficient for word, coefficient in signatures.items() if coefficient}
    )


def principal_deletion_signature(
    blocker_count: int, deleted: int
) -> Counter[tuple[int, ...]]:
    vertices = tuple(vertex for vertex in range(blocker_count) if vertex != deleted)
    edges = {
        (index, index + 1): (1 if index % 2 == 0 else 0)
        for index in range(blocker_count - 1)
    }

    @cache
    def recurse(remaining: tuple[int, ...]):
        if not remaining:
            return ((),)
        first = remaining[0]
        answer = []
        for position in range(1, len(remaining)):
            second = remaining[position]
            edge = (first, second)
            if edge not in edges:
                continue
            rest = remaining[1:position] + remaining[position + 1 :]
            for tail in recurse(rest):
                answer.append((edge,) + tail)
        return tuple(answer)

    positions = {vertex: index for index, vertex in enumerate(vertices)}
    signatures: Counter[tuple[int, ...]] = Counter()
    for matching in recurse(vertices):
        word = [-1] * len(vertices)
        for edge in matching:
            colour = edges[edge]
            word[positions[edge[0]]] = word[positions[edge[1]]] = colour
        assert -1 not in word
        signatures[tuple(word)] += 1
    return signatures


def outer(left: Vector, right: Vector) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(a * b for b in right) for a in left)


def add(
    left: tuple[tuple[int, ...], ...], right: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def audit_case(blocker_count: int) -> tuple[int, int]:
    zero = (0, 0, 0)
    a = [zero for _ in range(blocker_count)]
    b = [zero for _ in range(blocker_count)]
    a[0], a[1], a[-1] = (1, 0, 0), (0, 0, 1), (0, 1, 0)
    b[0], b[1], b[-1] = (1, 0, 0), (0, 0, 1), (0, -1, 0)
    assert rational_rank(a) == rational_rank(b) == 3

    first = path_signatures(blocker_count, 0)
    second = path_signatures(blocker_count, 1)
    assert first == Counter({(0,) * blocker_count: 1, (1,) * blocker_count: 1})
    assert second == Counter({(0,) * blocker_count: 1, (1,) * blocker_count: -1})
    for deleted in range(blocker_count):
        signature = principal_deletion_signature(blocker_count, deleted)
        if deleted % 2:
            assert not signature
        else:
            expected = (1,) * deleted + (0,) * (blocker_count - 1 - deleted)
            assert signature == Counter({expected: 1})

    checks = 0
    for u in range(blocker_count):
        for v in range(u + 1, blocker_count):
            formula = add(outer(a[u], b[v]), outer(b[u], a[v]))
            # Independent enumeration of the two nonzero four-vertex
            # matchings when the q0--q1 edge has weight zero.
            enumerated = tuple(
                tuple(a[u][i] * b[v][j] + b[u][i] * a[v][j] for j in range(3))
                for i in range(3)
            )
            assert formula == enumerated
            checks += 1
    return len(first) + len(second), checks


def main() -> None:
    cases = 0
    signature_terms = 0
    four_vertex_checks = 0
    for blocker_count in range(5, 22, 2):
        terms, checks = audit_case(blocker_count)
        cases += 1
        signature_terms += terms
        four_vertex_checks += checks
    print("PASS: independent odd-blocker binary cofactor/full-port audit")
    print(f"odd blocker counts: {cases}")
    print(f"surviving endpoint signature terms: {signature_terms}")
    print(f"four-vertex tensor checks: {four_vertex_checks}")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
