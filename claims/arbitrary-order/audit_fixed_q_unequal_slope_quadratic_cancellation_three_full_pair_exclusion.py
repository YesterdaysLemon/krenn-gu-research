"""Independent standard-library audit of the unequal-slope detector.

This audit imports neither SymPy nor the primary verifier.  It uses a sparse
formal-polynomial implementation, direct complementary-matching tensor
enumeration, exact ``Fraction`` elimination, and independently built physical
controls.  The written arbitrary-field proof remains load-bearing.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product

Q = Fraction
Monomial = tuple[str, ...]
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


def constant(value: int | Q) -> Polynomial:
    coefficient = Q(value)
    return {(): coefficient} if coefficient else {}


def atom(name: str) -> Polynomial:
    return {(name,): Q(1)}


def add(*polynomials: Polynomial) -> Polynomial:
    answer: defaultdict[Monomial, Q] = defaultdict(Q)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return {
        monomial: coefficient for monomial, coefficient in answer.items() if coefficient
    }


def scale(coefficient: int | Q, polynomial: Polynomial) -> Polynomial:
    scalar = Q(coefficient)
    return {
        monomial: scalar * value
        for monomial, value in polynomial.items()
        if scalar * value
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: defaultdict[Monomial, Q] = defaultdict(Q)
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_value * right_value
            )
    return {
        monomial: coefficient for monomial, coefficient in answer.items() if coefficient
    }


def audit_general_identity() -> None:
    p, t = atom("p"), atom("t")
    direct = {edge: atom(f"B{edge}") for edge in EDGES}
    channel = {edge: atom(f"K{edge}") for edge in EDGES}
    selected = {edge: add(direct[edge], multiply(p, channel[edge])) for edge in EDGES}

    def compound(blocks):
        return add(*(multiply(blocks[e], blocks[f]) for e, f in MATCHINGS))

    def cross(left, right):
        return add(
            *(
                add(multiply(left[e], right[f]), multiply(right[e], left[f]))
                for e, f in MATCHINGS
            )
        )

    response = add(compound(direct), multiply(t, cross(direct, channel)))
    coefficient = add(multiply(p, p), scale(-2, multiply(p, t)))
    claimed = add(
        compound(selected),
        multiply(add(t, scale(-1, p)), cross(selected, channel)),
        multiply(coefficient, compound(channel)),
    )
    assert add(response, scale(-1, claimed)) == {}


def zero_polynomial_matrix() -> tuple[tuple[Polynomial, ...], ...]:
    return tuple(tuple({} for _ in COLORS) for _ in COLORS)


def formal_diagonal_blocks(prefix: str):
    answer = {}
    for edge in EDGES:
        rows = [[{} for _ in COLORS] for _ in COLORS]
        for color in COLORS:
            rows[color][color] = atom(f"{prefix}{edge}_{color}")
        answer[edge] = tuple(tuple(row) for row in rows)
    return answer


def formal_full_blocks(prefix: str):
    return {
        edge: tuple(
            tuple(atom(f"{prefix}{edge}_{row}{column}") for column in COLORS)
            for row in COLORS
        )
        for edge in EDGES
    }


def formal_compound_word(blocks, word: Word) -> Polynomial:
    return add(
        *(
            multiply(
                blocks[first][word[first[0]]][word[first[1]]],
                blocks[second][word[second[0]]][word[second[1]]],
            )
            for first, second in MATCHINGS
        )
    )


def formal_cross_word(left, right, word: Word) -> Polynomial:
    return add(
        *(
            add(
                multiply(
                    left[first][word[first[0]]][word[first[1]]],
                    right[second][word[second[0]]][word[second[1]]],
                ),
                multiply(
                    right[first][word[first[0]]][word[first[1]]],
                    left[second][word[second[0]]][word[second[1]]],
                ),
            )
            for first, second in MATCHINGS
        )
    )


def audit_eighteen_rows() -> None:
    diagonal = formal_diagonal_blocks("D")
    channel = formal_full_blocks("K")
    q = atom("q")
    first, second = (0, 1), (2, 3)
    words: set[Word] = set()

    for a, b in product(COLORS, repeat=2):
        if a == b:
            continue
        c = next(color for color in COLORS if color not in (a, b))
        first_word = (a, b, c, c)
        observed_first = add(
            formal_compound_word(diagonal, first_word),
            multiply(q, formal_cross_word(diagonal, channel, first_word)),
        )
        expected_first = multiply(
            q,
            multiply(channel[first][a][b], diagonal[second][c][c]),
        )
        assert observed_first == expected_first
        words.add(first_word)

        second_word = (c, c, a, b)
        observed_second = add(
            formal_compound_word(diagonal, second_word),
            multiply(q, formal_cross_word(diagonal, channel, second_word)),
        )
        expected_second = multiply(
            q,
            multiply(diagonal[first][c][c], channel[second][a][b]),
        )
        assert observed_second == expected_second
        words.add(second_word)

    for c, d in product(COLORS, repeat=2):
        if c == d:
            continue
        word = (c, c, d, d)
        observed = add(
            formal_compound_word(diagonal, word),
            multiply(q, formal_cross_word(diagonal, channel, word)),
        )
        expected = add(
            multiply(diagonal[first][c][c], diagonal[second][d][d]),
            multiply(
                q,
                add(
                    multiply(diagonal[first][c][c], channel[second][d][d]),
                    multiply(channel[first][c][c], diagonal[second][d][d]),
                ),
            ),
        )
        assert observed == expected
        words.add(word)

    assert len(words) == 18


def exact_rank(rows: list[list[Q]]) -> int:
    matrix = [list(row) for row in rows]
    rank = 0
    if not matrix:
        return rank
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
    return rank


def audit_ratio_system() -> None:
    rows: list[list[Q]] = []
    for first_color, second_color in product(COLORS, repeat=2):
        if first_color == second_color:
            continue
        row = [Q(0)] * 6
        row[first_color] = Q(1)
        row[3 + second_color] = Q(1)
        rows.append(row)
    assert exact_rank(rows) == 5
    assert exact_rank([row + [Q(1)] for row in rows]) == 5
    particular = (Q(0), Q(0), Q(0), Q(1), Q(1), Q(1))
    direction = (Q(1), Q(1), Q(1), Q(-1), Q(-1), Q(-1))
    assert all(sum(row[i] * particular[i] for i in range(6)) == 1 for row in rows)
    assert all(sum(row[i] * direction[i] for i in range(6)) == 0 for row in rows)


def diagonal_matrix(values: tuple[int | Q, int | Q, int | Q]) -> Matrix:
    return tuple(
        tuple(Q(values[row]) if row == column else Q(0) for column in COLORS)
        for row in COLORS
    )  # type: ignore[return-value]


def outer(left, right) -> Matrix:
    return tuple(
        tuple(Q(left[row] * right[column]) for column in COLORS) for row in COLORS
    )  # type: ignore[return-value]


def add_matrix(left: Matrix, right: Matrix, right_scale: int | Q = 1) -> Matrix:
    scalar = Q(right_scale)
    return tuple(
        tuple(left[row][column] + scalar * right[row][column] for column in COLORS)
        for row in COLORS
    )  # type: ignore[return-value]


def corrected_blocks(first, second) -> dict[Edge, Matrix]:
    return {
        edge: add_matrix(
            outer(first[edge[0]], second[edge[1]]),
            outer(second[edge[0]], first[edge[1]]),
        )
        for edge in EDGES
    }


def numeric_compound(blocks: dict[Edge, Matrix]) -> dict[Word, Q]:
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


def numeric_cross(left: dict[Edge, Matrix], right: dict[Edge, Matrix]) -> dict[Word, Q]:
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
            other = tuple(value for value in PORTS if value not in edge)
            complement = tuple(sorted(other))
            if any(
                pairs[edge][color][color] * pairs[complement][delta][delta]
                for delta in COLORS
                if delta != color
            ):
                answer.add(color)
    return answer


def assert_pure(tensor: dict[Word, Q], expected: tuple[int | Q, ...]) -> None:
    assert tuple(tensor.get((color,) * 4, Q(0)) for color in COLORS) == tuple(
        map(Q, expected)
    )
    assert all(len(set(word)) == 1 for word in tensor)


def audit_missing_three_full_control() -> None:
    channel = {edge: diagonal_matrix((2, 0, 0)) for edge in EDGES}
    first_support = {(0, 1), (1, 2), (2, 3)}
    second_support = {(0, 2), (1, 3)}
    selected = {
        edge: diagonal_matrix(
            (2, int(edge in first_support), int(edge in second_support))
        )
        for edge in EDGES
    }
    direct = {edge: add_matrix(selected[edge], channel[edge], -2) for edge in EDGES}
    response = add_tensors(numeric_compound(direct), numeric_cross(direct, channel))
    assert_pure(response, (-12, 1, 1))
    assert active_colors(selected, 0) == {0, 1, 2}
    assert all(
        any(selected[edge][color][color] == 0 for color in COLORS) for edge in EDGES
    )


def raw_rank_two_channel() -> dict[Edge, Matrix]:
    first = ((1, 1, 0),) * 4
    second = ((1, -1, 0),) * 4
    channel = corrected_blocks(first, second)
    assert all(block == diagonal_matrix((2, -2, 0)) for block in channel.values())
    return channel


def audit_all_nonzero_control() -> None:
    channel = raw_rank_two_channel()
    direct = {edge: diagonal_matrix((0, 0, 1)) for edge in EDGES}
    selected = {edge: add_matrix(direct[edge], channel[edge]) for edge in EDGES}
    assert all(block == diagonal_matrix((2, -2, 1)) for block in selected.values())
    assert_pure(numeric_compound(direct), (0, 0, 3))
    assert active_colors(selected, 0) == {0, 1, 2}


def audit_pure_normalized_control() -> None:
    channel = raw_rank_two_channel()
    supports = {
        0: {(0, 1), (2, 3)},
        1: {(0, 2), (1, 3)},
        2: {(0, 3), (1, 2)},
    }
    direct = {
        edge: diagonal_matrix(tuple(int(edge in supports[color]) for color in COLORS))
        for edge in EDGES
    }
    selected = {edge: add_matrix(direct[edge], channel[edge]) for edge in EDGES}
    assert_pure(numeric_compound(direct), (1, 1, 1))
    assert active_colors(selected, 0) == {0, 1, 2}
    assert selected[(0, 3)] == selected[(1, 2)] == diagonal_matrix((2, -2, 1))


def main() -> None:
    audit_general_identity()
    audit_eighteen_rows()
    audit_ratio_system()
    audit_missing_three_full_control()
    audit_all_nonzero_control()
    audit_pure_normalized_control()
    print("unequal-slope quadratic-cancellation independent audit: PASS")


if __name__ == "__main__":
    main()
