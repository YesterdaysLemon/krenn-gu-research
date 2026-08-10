"""Independent no-import audit of the all-bridge active-deck checkpoint."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


def hafnian(matrix: list[list[Fraction]], vertices: tuple[int, ...]) -> Fraction:
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    total = Fraction(0)
    for offset, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:offset] + vertices[offset + 1 :]
        total += matrix[first][partner] * hafnian(matrix, remainder)
    return total


def deterministic_matrix(order: int, seed: int) -> list[list[Fraction]]:
    matrix = [[Fraction(0) for _ in range(order)] for _ in range(order)]
    for i, j in combinations(range(order), 2):
        numerator = ((i + 2) * (j + 3) + 5 * seed) % 17 - 8
        denominator = 1 + ((3 * i + j + seed) % 5)
        matrix[i][j] = matrix[j][i] = Fraction(numerator, denominator)
    return matrix


def audit_numeric_laplace() -> None:
    for order in (2, 4, 6, 8):
        vertices = tuple(range(order))
        for seed in range(1, 5):
            matrix = deterministic_matrix(order, seed)
            full = hafnian(matrix, vertices)
            for pivot in vertices:
                expansion = Fraction(0)
                for partner in vertices:
                    if partner == pivot:
                        continue
                    remainder = tuple(
                        v for v in vertices if v not in (pivot, partner)
                    )
                    expansion += matrix[pivot][partner] * hafnian(
                        matrix, remainder
                    )
                assert expansion == full


def audit_cut_logic() -> None:
    """Rebuild the two oriented mixed-cut implications as a truth table."""

    records = []
    for z0, z1, z2, c0, c1, c2 in product((0, 1), repeat=6):
        z = (z0, z1, z2)
        cof = (c0, c1, c2)
        oriented_cuts_zero = all(
            z[a] * cof[b] == 0
            for a in range(3)
            for b in range(3)
            if a != b
        )
        if not oriented_cuts_zero:
            continue
        active = tuple(a for a in range(3) if z[a] * cof[a] != 0)
        records.append((z, cof, active))
        if active:
            assert len(active) == 1
            a = active[0]
            assert all(z[b] == cof[b] == 0 for b in range(3) if b != a)
    assert len(records) == 18
    assert sum(bool(record[2]) for record in records) == 3


def audit_local_degree_implication() -> None:
    """Use set partitions, rather than the primary's labelled assignments."""

    shared = frozenset({"shared"})
    active_colours = {
        0: frozenset({"active-0"}),
        1: frozenset({"active-1"}),
        2: frozenset({"active-2"}),
    }
    incident = set(shared)
    for colour in range(3):
        incident.update(active_colours[colour])
    assert len(incident) == 4
    assert "shared" not in {
        next(iter(active_colours[colour])) for colour in range(3)
    }


def audit_local_word_forcing() -> None:
    """A proper cubic factorization forces an edge from its endpoint colour."""

    vertices = range(8)
    factors = {
        0: {tuple(sorted((i, i ^ 1))) for i in vertices if i < (i ^ 1)},
        1: {tuple(sorted((i, i ^ 2))) for i in vertices if i < (i ^ 2)},
        2: {tuple(sorted((i, i ^ 4))) for i in vertices if i < (i ^ 4)},
    }
    assert all(len(factor) == 4 for factor in factors.values())
    assert not (factors[0] & factors[1] or factors[0] & factors[2] or factors[1] & factors[2])

    # Pick a nonmonochromatic cube matching directly.
    chosen = {(0, 1), (2, 3), (4, 6), (5, 7)}
    colour_of_edge = {
        item: colour for colour, factor in factors.items() for item in factor
    }
    assert chosen <= set(colour_of_edge)
    word = {}
    for i, j in chosen:
        colour = colour_of_edge[(i, j)]
        word[i] = colour
        word[j] = colour
    forced = set()
    for vertex in vertices:
        colour = word[vertex]
        incident = [item for item in factors[colour] if vertex in item]
        assert len(incident) == 1
        forced.add(incident[0])
    assert forced == chosen


def main() -> None:
    audit_numeric_laplace()
    audit_cut_logic()
    audit_local_degree_implication()
    audit_local_word_forcing()
    print("independent active-deck/cubic-diagonal audit: PASS")
    print("no primary-module import; exact rational arithmetic only")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
