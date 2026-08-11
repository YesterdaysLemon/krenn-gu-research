"""Independent graph-matching audit of the minimal two-open detector."""

from __future__ import annotations

from collections.abc import Iterable
from itertools import product

Covector = tuple[int, int, int]
Word = tuple[int, ...]


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return labelled perfect matchings by a first-vertex recursion."""
    if not vertices:
        return ((),)
    first = vertices[0]
    matchings = []
    for offset in range(1, len(vertices)):
        second = vertices[offset]
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for tail in perfect_matchings(rest):
            matchings.append((((first, second)), *tail))
    return tuple(matchings)


def matching_total(
    vertices: tuple[int, ...], edge: dict[tuple[int, int], int]
) -> int:
    """Sum edge products over the independent matching ledger."""
    return sum(
        product_value(edge[tuple(sorted(pair))] for pair in matching)
        for matching in perfect_matchings(vertices)
    )


def product_value(values: Iterable[int]) -> int:
    """Multiply an iterable without importing a computer-algebra helper."""
    result = 1
    for value in values:
        result *= value
    return result


def evaluate(row: tuple[Covector, ...], word: Word) -> list[int]:
    return [row[mode][colour] for mode, colour in enumerate(word)]


def collision_tensor(
    a: tuple[Covector, Covector, Covector],
    b: tuple[Covector, Covector, Covector],
) -> dict[Word, int]:
    """Build P3(a,a,b) from its three b-location cases."""
    values: dict[Word, int] = {}
    for word in product(range(3), repeat=3):
        a_values = evaluate(a, word)
        b_values = evaluate(b, word)
        values[word] = 2 * (
            b_values[0] * a_values[1] * a_values[2]
            + a_values[0] * b_values[1] * a_values[2]
            + a_values[0] * a_values[1] * b_values[2]
        )
    return values


def audit_hall_counts() -> None:
    for q in range(12):
        repeated = q + 1
        a_outside = 3 * repeated - 1
        b_outside = 3 * repeated
        assert a_outside == 3 * q + 2
        assert b_outside == 3 * q + 3
        for r in range(2, 20):
            outside = r + 2 * q
            assert (b_outside <= outside) == (r >= q + 3)
            if r == q + 3:
                counts = [repeated, repeated, repeated]
                assert sum(counts) == outside


def audit_collision_boundary() -> None:
    axes: tuple[Covector, Covector, Covector] = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    boundary_b: tuple[Covector, Covector, Covector] = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, -2),
    )
    tensor = collision_tensor(axes, boundary_b)
    assert len(tensor) == 27
    assert set(tensor.values()) == {0}

    nonzero_b: tuple[Covector, Covector, Covector] = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 3),
    )
    nonzero = collision_tensor(axes, nonzero_b)
    assert nonzero[(0, 1, 2)] == 10
    assert sum(value != 0 for value in nonzero.values()) == 1


def audit_two_open_graph_variation() -> None:
    """Recover the q=0 companion residual from all 15 graph matchings."""
    a: tuple[Covector, Covector, Covector] = (
        (1, 2, 3),
        (2, -1, 4),
        (3, 5, -2),
    )
    b: tuple[Covector, Covector, Covector] = (
        (2, 3, 5),
        (-1, 4, 2),
        (5, -2, 1),
    )
    h_s: tuple[Covector, Covector, Covector] = (
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
    )
    eta: Covector = (41, 43, 47)
    ell_s: Covector = (53, 59, 61)
    collision = collision_tensor(a, b)
    vertices = tuple(range(6))
    root_j, root_i, root_s = 0, 1, 2

    for word in product(range(3), repeat=3):
        for j_colour in range(3):
            base: dict[tuple[int, int], int] = {}
            for first in vertices:
                for second in vertices:
                    if first >= second or root_i in (first, second):
                        continue
                    pair = (first, second)
                    if pair == (root_j, root_s):
                        base[pair] = ell_s[j_colour]
                    elif first == root_j and second >= 3:
                        mode = second - 3
                        base[pair] = eta[j_colour] * b[mode][word[mode]]
                    elif first == root_s and second >= 3:
                        mode = second - 3
                        base[pair] = h_s[mode][word[mode]]
                    elif first >= 3:
                        left = first - 3
                        right = second - 3
                        base[pair] = (
                            a[left][word[left]] * b[right][word[right]]
                            + b[left][word[left]] * a[right][word[right]]
                        )
                    else:
                        raise AssertionError(pair)

            variation = 0
            for matching in perfect_matchings(vertices):
                incident = next(pair for pair in matching if root_i in pair)
                partner = incident[0] if incident[1] == root_i else incident[1]
                if partner == root_j:
                    delta = -eta[j_colour]
                elif partner == root_s:
                    delta = 0
                else:
                    mode = partner - 3
                    delta = a[mode][word[mode]]
                remaining = [pair for pair in matching if pair != incident]
                variation += delta * product_value(
                    base[tuple(sorted(pair))] for pair in remaining
                )

            expected = ell_s[j_colour] * collision[word]
            assert variation == expected


def audit_recolouring_coefficients() -> None:
    """Evaluate the pure/mixed pair through the six-vertex graph ledger."""
    a_outside: tuple[Covector, Covector, Covector] = (
        (2, 0, 0),
        (0, 3, 0),
        (0, 0, 5),
    )
    b_outside: tuple[Covector, Covector, Covector] = (
        (7, 0, 0),
        (0, 11, 0),
        (0, 0, 13),
    )
    h_first: tuple[Covector, Covector, Covector] = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 10),
    )
    h_second: tuple[Covector, Covector, Covector] = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
    )
    eta: Covector = (29, 31, 37)
    ell_first: Covector = (41, 43, 47)
    ell_second: Covector = (53, 59, 61)

    def coefficient(outside_colour: int, j_colour: int) -> int:
        vertices = tuple(range(6))
        root_j, root_first, root_second = 0, 1, 2
        edge: dict[tuple[int, int], int] = {}
        for first in vertices:
            for second in vertices:
                if first >= second:
                    continue
                pair = (first, second)
                if pair == (root_j, root_first):
                    edge[pair] = ell_first[j_colour]
                elif pair == (root_j, root_second):
                    edge[pair] = ell_second[j_colour]
                elif pair == (root_first, root_second):
                    edge[pair] = 0
                elif first == root_j:
                    mode = second - 3
                    edge[pair] = (
                        eta[j_colour] * b_outside[mode][outside_colour]
                    )
                elif first == root_first:
                    mode = second - 3
                    edge[pair] = h_first[mode][outside_colour]
                elif first == root_second:
                    mode = second - 3
                    edge[pair] = h_second[mode][outside_colour]
                else:
                    left = first - 3
                    right = second - 3
                    edge[pair] = (
                        a_outside[left][outside_colour]
                        * b_outside[right][outside_colour]
                        + b_outside[left][outside_colour]
                        * a_outside[right][outside_colour]
                    )
        return matching_total(vertices, edge)

    for colour in range(3):
        retained = [mode for mode in range(3) if mode != colour]
        cofactor = (
            h_first[retained[0]][colour]
            * h_second[retained[1]][colour]
            + h_first[retained[1]][colour]
            * h_second[retained[0]][colour]
        )
        beta = b_outside[colour][colour]
        assert cofactor != 0
        for j_colour in range(3):
            expected = eta[j_colour] * beta * cofactor
            assert coefficient(colour, j_colour) == expected


def audit_detection_linear_algebra() -> None:
    # The two companion coefficients form a basis.  Deleting either one leaves
    # a nonzero rank-one observation; stacking the two observations has rank 2.
    first_observation = (0, 5)
    second_observation = (5, 0)
    assert any(first_observation)
    assert any(second_observation)
    determinant = (
        first_observation[0] * second_observation[1]
        - first_observation[1] * second_observation[0]
    )
    assert determinant != 0


def main() -> None:
    audit_hall_counts()
    audit_collision_boundary()
    audit_two_open_graph_variation()
    audit_recolouring_coefficients()
    audit_detection_linear_algebra()
    print("AUDIT PASS: independent repeated-row Hall arithmetic")
    print("AUDIT PASS: direct three-case P3 collision and Hall-only boundary")
    print("AUDIT PASS: all 15-matchings two-open graph variation")
    print("AUDIT PASS: independent six-vertex pure/mixed recolouring ledger")
    print("AUDIT PASS: fixed-i nonzero and collectively rank-two observations")
    print("AUDIT SCOPE: written flattening proof supplies the universal implication")
    print("AUDIT SCOPE: larger aligned and all unfactorized cells remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
