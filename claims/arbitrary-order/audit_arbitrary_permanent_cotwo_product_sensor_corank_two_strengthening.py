"""Independent no-import audit of the co-two corank-two strengthening."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement

Eisenstein = tuple[Fraction, Fraction]
EVector = tuple[Eisenstein, ...]

ZERO: Eisenstein = (Fraction(0), Fraction(0))
ONE: Eisenstein = (Fraction(1), Fraction(0))


def add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    """Add in Q(omega), where omega^2+omega+1=0."""
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    """Subtract in Q(omega)."""
    return left[0] - right[0], left[1] - right[1]


def multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    """Multiply in Q(omega) using omega^2=-omega-1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def inverse(value: Eisenstein) -> Eisenstein:
    """Invert a nonzero Eisenstein rational exactly."""
    a, b = value
    norm = a * a - a * b + b * b
    assert norm
    return (a - b) / norm, -b / norm


def divide(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    """Divide exactly in Q(omega)."""
    return multiply(left, inverse(right))


def projective(vector: EVector) -> EVector:
    """Normalize a nonzero Q(omega) vector by its first nonzero entry."""
    pivot = next(entry for entry in vector if entry != ZERO)
    return tuple(divide(entry, pivot) for entry in vector)


def edge_list(vertex_count: int) -> list[tuple[int, int]]:
    """List the square-free quadratic coordinates."""
    return list(combinations(range(vertex_count), 2))


def square_free_product(left: EVector, right: EVector) -> EVector:
    """Multiply degree-one forms in the square-free algebra."""
    return tuple(
        add(
            multiply(left[first], right[second]),
            multiply(left[second], right[first]),
        )
        for first, second in edge_list(len(left))
    )


def rank(vectors: list[EVector]) -> int:
    """Row-rank vectors over Q(omega) by a custom exact elimination."""
    if not vectors:
        return 0
    work = [list(vector) for vector in vectors]
    row_count = len(work)
    column_count = len(work[0])
    current = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(current, row_count) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[current], work[pivot] = work[pivot], work[current]
        pivot_inverse = inverse(work[current][column])
        work[current] = [
            multiply(entry, pivot_inverse) for entry in work[current]
        ]
        for row in range(row_count):
            if row == current or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                subtract(entry, multiply(factor, basis))
                for entry, basis in zip(work[row], work[current], strict=True)
            ]
        current += 1
        if current == row_count:
            break
    return current


def support_graph_audit() -> dict[int, Counter[tuple[int, int]]]:
    """Derive all graph sizes from support sets, independently of weights."""
    ledger: dict[int, Counter[tuple[int, int]]] = {}
    for vertex_count in range(2, 9):
        supports = [
            frozenset(support)
            for size in (1, 2)
            for support in combinations(range(vertex_count), size)
        ]
        counts: Counter[tuple[int, int]] = Counter()
        for left_index, left in enumerate(supports):
            for right in supports[left_index:]:
                if left == right and len(left) == 1:
                    continue
                if left == right:
                    graph = {tuple(sorted(left))}
                else:
                    graph = {
                        edge
                        for edge in edge_list(vertex_count)
                        if (edge[0] in left and edge[1] in right)
                        or (edge[1] in left and edge[0] in right)
                    }
                incident = {vertex for edge in graph for vertex in edge}
                assert incident == left | right
                counts[(len(incident), len(graph))] += 1

                if len(incident) == 4:
                    assert len(graph) == 4
                    colour: dict[int, int] = {}
                    start = next(iter(incident))
                    colour[start] = 0
                    frontier = [start]
                    while frontier:
                        vertex = frontier.pop()
                        for edge in graph:
                            if vertex not in edge:
                                continue
                            neighbour = edge[1] if edge[0] == vertex else edge[0]
                            wanted = 1 - colour[vertex]
                            if neighbour in colour:
                                assert colour[neighbour] == wanted
                            else:
                                colour[neighbour] = wanted
                                frontier.append(neighbour)
                    assert len(colour) == 4
                    shores = {
                        frozenset(v for v, value in colour.items() if value == bit)
                        for bit in (0, 1)
                    }
                    assert shores == {frozenset(left), frozenset(right)}
        ledger[vertex_count] = counts
    return ledger


def support_two_forms(vertex_count: int) -> list[EVector]:
    """Use the six Eisenstein units as projective two-support ratios."""
    units: tuple[Eisenstein, ...] = (
        (Fraction(1), Fraction(0)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(-1)),
        (Fraction(-1), Fraction(-1)),
        (Fraction(1), Fraction(1)),
    )
    forms: list[EVector] = []
    for first in range(vertex_count):
        form = [ZERO for _ in range(vertex_count)]
        form[first] = ONE
        forms.append(tuple(form))
    for first, second in combinations(range(vertex_count), 2):
        for unit in units:
            form = [ZERO for _ in range(vertex_count)]
            form[first] = ONE
            form[second] = unit
            forms.append(tuple(form))
    return forms


def quadratic_vertices(quadratic: EVector, vertex_count: int) -> set[int]:
    """Find vertices incident to a nonzero quadratic coefficient."""
    result: set[int] = set()
    for coefficient, edge in zip(
        quadratic, edge_list(vertex_count), strict=True
    ):
        if coefficient != ZERO:
            result.update(edge)
    return result


def eisenstein_factor_audit() -> dict[int, dict[str, object]]:
    """Stress-test factor-line spans on a cancellation-rich exact grid."""
    ledger: dict[int, dict[str, object]] = {}
    for vertex_count in range(2, 7):
        forms = support_two_forms(vertex_count)
        factor_lines: dict[EVector, set[EVector]] = defaultdict(set)
        for left, right in combinations_with_replacement(forms, 2):
            product = square_free_product(left, right)
            if all(entry == ZERO for entry in product):
                continue
            quadratic = projective(product)
            factor_lines[quadratic].update((projective(left), projective(right)))

        histogram: Counter[tuple[int, int]] = Counter()
        triangle_dependences = 0
        for quadratic, factors in factor_lines.items():
            factor_rank = rank(list(factors))
            vertices = len(quadratic_vertices(quadratic, vertex_count))
            histogram[(vertices, factor_rank)] += 1
            if vertices <= 2 or vertices == 4:
                assert factor_rank <= 2
            if factor_rank >= 3:
                assert vertices == 3
                squares = [square_free_product(factor, factor) for factor in factors]
                assert rank(squares) == rank([*squares, quadratic])
                triangle_dependences += 1

        if vertex_count >= 4:
            assert any(vertices == 4 for vertices, _ in histogram)
            assert max(
                factor_rank
                for (vertices, factor_rank), count in histogram.items()
                if vertices == 4 and count
            ) == 2
        ledger[vertex_count] = {
            "projective_forms": len(forms),
            "projective_products": len(factor_lines),
            "histogram": dict(sorted(histogram.items())),
            "triangle_square_dependences": triangle_dependences,
        }
    return ledger


def main() -> None:
    graphs = support_graph_audit()
    factors = eisenstein_factor_audit()
    print("arbitrary permanent co-two corank-two independent audit: PASS")
    print(f"  support graph ledgers through 8 vertices: {graphs}")
    print(f"  exact Q(omega) factor-line ledgers: {factors}")


if __name__ == "__main__":
    main()
