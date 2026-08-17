"""Independent standard-library audit of the common projective theorem.

This script imports neither SymPy nor the primary verifier.  It uses sparse
polynomial dictionaries for the homogeneous identity, elementary exact line
constraints for the common-space classification, and direct complementary
matching enumeration with ``Fraction`` coefficients for the two controls.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product

Q = Fraction
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Q]
Matrix = tuple[tuple[Q, Q, Q], tuple[Q, Q, Q], tuple[Q, Q, Q]]
Edge = tuple[int, int]
Word = tuple[int, int, int, int]

PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES: tuple[Edge, ...] = tuple(combinations(PORTS, 2))
MATCHINGS: tuple[tuple[Edge, Edge], ...] = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
VARIABLE_COUNT = 2 + 2 * len(EDGES)


def monomial(variable: int) -> Polynomial:
    powers = [0] * VARIABLE_COUNT
    powers[variable] = 1
    return {tuple(powers): Q(1)}


def add(*polynomials: Polynomial) -> Polynomial:
    answer: defaultdict[Monomial, Q] = defaultdict(Q)
    for polynomial in polynomials:
        for powers, coefficient in polynomial.items():
            answer[powers] += coefficient
    return {
        powers: coefficient for powers, coefficient in answer.items() if coefficient
    }


def scale(coefficient: Q | int, polynomial: Polynomial) -> Polynomial:
    value = Q(coefficient)
    return {
        powers: value * entry for powers, entry in polynomial.items() if value * entry
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: defaultdict[Monomial, Q] = defaultdict(Q)
    for left_powers, left_value in left.items():
        for right_powers, right_value in right.items():
            powers = tuple(
                first + second
                for first, second in zip(left_powers, right_powers, strict=True)
            )
            answer[powers] += left_value * right_value
    return {
        powers: coefficient for powers, coefficient in answer.items() if coefficient
    }


def audit_homogeneous_identity() -> None:
    alpha = monomial(0)
    beta = monomial(1)
    direct = {edge: monomial(2 + number) for number, edge in enumerate(EDGES)}
    channel = {
        edge: monomial(2 + len(EDGES) + number) for number, edge in enumerate(EDGES)
    }
    selected = {
        edge: add(multiply(alpha, direct[edge]), multiply(beta, channel[edge]))
        for edge in EDGES
    }
    compound_direct = add(*(multiply(direct[e], direct[f]) for e, f in MATCHINGS))
    compound_channel = add(*(multiply(channel[e], channel[f]) for e, f in MATCHINGS))
    compound_selected = add(*(multiply(selected[e], selected[f]) for e, f in MATCHINGS))
    cross = add(
        *(
            add(
                multiply(direct[e], channel[f]),
                multiply(channel[e], direct[f]),
            )
            for e, f in MATCHINGS
        )
    )
    selected_four = add(multiply(alpha, compound_direct), multiply(beta, cross))
    difference = add(
        multiply(alpha, selected_four),
        scale(-1, compound_selected),
        multiply(multiply(beta, beta), compound_channel),
    )
    assert difference == {}


def constraint_rank(rows: list[tuple[Q, Q]]) -> int:
    nonzero = [row for row in rows if row != (0, 0)]
    if not nonzero:
        return 0
    first = nonzero[0]
    if all(first[0] * row[1] == first[1] * row[0] for row in nonzero[1:]):
        return 1
    return 2


def intersection_dimension(spaces: tuple[str, ...]) -> int:
    constraints = {
        "zero": ((Q(1), Q(0)), (Q(0), Q(1))),
        "line_11": ((Q(1), Q(-1)),),
        "line_12": ((Q(2), Q(-1)),),
        "plane": (),
    }
    rows = [row for name in spaces for row in constraints[name]]
    return 2 - constraint_rank(rows)


def audit_common_spaces() -> None:
    names = ("zero", "line_11", "line_12", "plane")
    counts = {0: 0, 1: 0, 2: 0}
    for spaces in product(names, repeat=7):
        observed = intersection_dimension(spaces)
        if "zero" in spaces or {"line_11", "line_12"} <= set(spaces):
            expected = 0
        elif any(name.startswith("line_") for name in spaces):
            expected = 1
        else:
            expected = 2
        assert observed == expected
        counts[observed] += 1
    assert sum(counts.values()) == 4**7
    assert counts[2] == 1
    assert counts[1] == 2 * (2**7 - 1)


def zero_matrix() -> Matrix:
    return tuple(tuple(Q(0) for _ in COLORS) for _ in COLORS)  # type: ignore[return-value]


def diagonal_matrix(values: tuple[Q | int, Q | int, Q | int]) -> Matrix:
    return tuple(
        tuple(Q(values[row]) if row == column else Q(0) for column in COLORS)
        for row in COLORS
    )  # type: ignore[return-value]


def outer(left: tuple[int, int, int], right: tuple[int, int, int]) -> Matrix:
    return tuple(
        tuple(Q(left[row] * right[column]) for column in COLORS) for row in COLORS
    )  # type: ignore[return-value]


def add_matrix(left: Matrix, right: Matrix, right_scale: Q | int = 1) -> Matrix:
    scalar = Q(right_scale)
    return tuple(
        tuple(left[row][column] + scalar * right[row][column] for column in COLORS)
        for row in COLORS
    )  # type: ignore[return-value]


def corrected_blocks(
    first: tuple[tuple[int, int, int], ...],
    second: tuple[tuple[int, int, int], ...],
) -> dict[Edge, Matrix]:
    answer: dict[Edge, Matrix] = {}
    for edge in EDGES:
        left, right = edge
        answer[edge] = add_matrix(
            outer(first[left], second[right]), outer(second[left], first[right])
        )
    return answer


def compound(blocks: dict[Edge, Matrix]) -> dict[Word, Q]:
    answer: defaultdict[Word, Q] = defaultdict(Q)
    for first, second in MATCHINGS:
        for first_left, first_right, second_left, second_right in product(
            COLORS, repeat=4
        ):
            value = (
                blocks[first][first_left][first_right]
                * blocks[second][second_left][second_right]
            )
            if not value:
                continue
            word = [0, 0, 0, 0]
            word[first[0]], word[first[1]] = first_left, first_right
            word[second[0]], word[second[1]] = second_left, second_right
            answer[tuple(word)] += value  # type: ignore[index]
    return {word: value for word, value in answer.items() if value}


def cross(left: dict[Edge, Matrix], right: dict[Edge, Matrix]) -> dict[Word, Q]:
    answer: defaultdict[Word, Q] = defaultdict(Q)
    for first, second in MATCHINGS:
        for first_left, first_right, second_left, second_right in product(
            COLORS, repeat=4
        ):
            value = (
                left[first][first_left][first_right]
                * right[second][second_left][second_right]
                + right[first][first_left][first_right]
                * left[second][second_left][second_right]
            )
            if not value:
                continue
            word = [0, 0, 0, 0]
            word[first[0]], word[first[1]] = first_left, first_right
            word[second[0]], word[second[1]] = second_left, second_right
            answer[tuple(word)] += value  # type: ignore[index]
    return {word: value for word, value in answer.items() if value}


def add_tensors(*tensors: dict[Word, Q]) -> dict[Word, Q]:
    answer: defaultdict[Word, Q] = defaultdict(Q)
    for tensor in tensors:
        for word, value in tensor.items():
            answer[word] += value
    return {word: value for word, value in answer.items() if value}


def active_colors(pairs: dict[Edge, Matrix], port: int) -> set[int]:
    answer: set[int] = set()
    for color in COLORS:
        for partner in PORTS:
            if partner == port:
                continue
            edge = tuple(sorted((port, partner)))
            complement = tuple(value for value in PORTS if value not in edge)
            other = tuple(sorted(complement))
            if any(
                pairs[edge][color][color] * pairs[other][delta][delta]
                for delta in COLORS
                if delta != color
            ):
                answer.add(color)
    return answer


def audit_unequal_slopes() -> None:
    channel = {edge: diagonal_matrix((2, 0, 0)) for edge in EDGES}
    one_edges = {(0, 1), (1, 2), (2, 3)}
    two_edges = {(0, 2), (1, 3)}
    selected_pairs = {
        edge: diagonal_matrix((2, int(edge in one_edges), int(edge in two_edges)))
        for edge in EDGES
    }
    direct = {
        edge: add_matrix(selected_pairs[edge], channel[edge], -2) for edge in EDGES
    }
    assert all(
        add_matrix(direct[edge], channel[edge], 2) == selected_pairs[edge]
        for edge in EDGES
    )
    response = add_tensors(compound(direct), cross(direct, channel))
    assert tuple(response.get((color,) * 4, Q(0)) for color in COLORS) == (
        Q(-12),
        Q(1),
        Q(1),
    )
    assert all(len(set(word)) == 1 for word in response)
    assert active_colors(selected_pairs, 0) == {0, 1, 2}
    assert (Q(1), Q(2)) != (Q(1), Q(1))
    assert Q(1) * Q(1) - Q(2) * Q(1) != 0


def audit_common_camouflage() -> None:
    first = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0))
    second = ((0, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0))
    channel = corrected_blocks(first, second)
    selected_pairs = {
        (0, 1): diagonal_matrix((0, 0, 1)),
        (2, 3): diagonal_matrix((0, 0, 1)),
        (0, 2): diagonal_matrix((1, 1, 0)),
        (1, 3): diagonal_matrix((2, 2, 0)),
        (0, 3): diagonal_matrix((1, Q(2, 3), 0)),
        (1, 2): diagonal_matrix((3, 2, 0)),
    }
    direct = {
        edge: add_matrix(selected_pairs[edge], channel[edge], -1) for edge in EDGES
    }
    response = add_tensors(compound(direct), cross(direct, channel))
    assert tuple(response.get((color,) * 4, Q(0)) for color in COLORS) == (
        Q(3),
        Q(4, 3),
        Q(1),
    )
    assert all(len(set(word)) == 1 for word in response)
    assert all(active_colors(selected_pairs, port) == {0, 1} for port in PORTS)


def main() -> None:
    audit_homogeneous_identity()
    audit_common_spaces()
    audit_unequal_slopes()
    audit_common_camouflage()
    print("common projective joint-response independent audit: PASS")


if __name__ == "__main__":
    main()
