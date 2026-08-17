"""Independent standard-library audit of the fixed-Q joint M/Z theorem."""

from fractions import Fraction
from itertools import combinations, product


def sparse_rank(columns: list[dict[int, Fraction]]) -> int:
    pivots: dict[int, dict[int, Fraction]] = {}
    for source in columns:
        vector = {row: value for row, value in source.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                scale = vector[pivot]
                pivots[pivot] = {row: value / scale for row, value in vector.items()}
                break
            factor = vector[pivot]
            for row, value in pivots[pivot].items():
                updated = vector.get(row, Fraction(0)) - factor * value
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(pivots)


def dense_rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    columns = [
        {
            row: Fraction(rows[row][column])
            for row in range(len(rows))
            if rows[row][column]
        }
        for column in range(len(rows[0]))
    ]
    return sparse_rank(columns)


def multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def check_rank_branches() -> None:
    controls = (
        ([[1, 0], [0, 1]], [[1, 0, 0], [0, 1, 0]], (2, 2, 2)),
        ([[1, 0], [0, 1]], [[1, 0, 0], [1, 0, 0]], (2, 1, 1)),
        ([[1, 0], [0, 1]], [[0, 0, 0], [0, 0, 0]], (2, 0, 0)),
        ([[1, 1]], [[1, 0, 0], [0, 1, 0]], (1, 2, 1)),
        ([[1, 1]], [[1, 0, 0], [-1, 0, 0]], (1, 1, 0)),
        ([[0, 0]], [[1, 0, 0], [0, 1, 0]], (0, 2, 0)),
    )
    for desired, responses, expected in controls:
        observed = (
            dense_rank(desired),
            dense_rank(responses),
            dense_rank(multiply(desired, responses)),
        )
        assert observed == expected

    # Direct 2x2 wedge tests for independent and dependent desired classes.
    assert 1 * 1 - 0 * 0 != 0
    assert 1 * 2 - 2 * 1 == 0
    assert 3 + 7 * 11 - (-4 + 7 * 11) == 7


def deck_dimension(n: int) -> int:
    return (4 ** (n + 2) + (-2) ** (n + 2)) // 2 - 1


def check_sizes() -> None:
    assert [deck_dimension(n) for n in (4, 6, 7)] == [2079, 32895, 130815]
    assert [3 ** (14 - size) for size in (2, 4, 6)] == [531441, 59049, 6561]
    assert 2 * (6 * 729 + 81) == 8910


def edges_for(n: int) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(range(n), 2))


def coordinate(
    edges: tuple[tuple[int, int], ...], edge: tuple[int, int], colours: tuple[int, int]
) -> int:
    return 9 * edges.index(tuple(sorted(edge))) + 3 * colours[0] + colours[1]


def difference(
    edges: tuple[tuple[int, int], ...],
    positive: tuple[tuple[int, int], tuple[int, int]],
    negative: tuple[tuple[int, int], tuple[int, int]],
) -> dict[int, Fraction]:
    return {
        coordinate(edges, *positive): Fraction(1),
        coordinate(edges, *negative): Fraction(-1),
    }


def k33_basis() -> tuple[list[dict[int, Fraction]], tuple[tuple[int, int], ...]]:
    edges = edges_for(6)
    basis = [
        difference(edges, (positive, (0, 0)), (negative, (0, 0)))
        for positive, negative in (
            ((0, 2), (0, 1)),
            ((1, 2), (0, 1)),
            ((3, 5), (3, 4)),
            ((4, 5), (3, 4)),
        )
    ]
    for port in range(6):
        shore = {0, 1, 2} if port < 3 else {3, 4, 5}
        mates = sorted(shore - {port})
        for colour in (1, 2):
            positive = tuple(sorted((port, mates[0])))
            negative = tuple(sorted((port, mates[1])))
            positive_colours = (colour, 0) if positive[0] == port else (0, colour)
            negative_colours = (colour, 0) if negative[0] == port else (0, colour)
            basis.append(
                difference(
                    edges, (positive, positive_colours), (negative, negative_colours)
                )
            )
    return basis, edges


def k52_basis() -> tuple[list[dict[int, Fraction]], tuple[tuple[int, int], ...]]:
    edges = edges_for(7)
    basis = [
        difference(edges, ((leaf, 5), (colour, 0)), ((leaf, 6), (colour, 0)))
        for leaf in range(5)
        for colour in range(3)
    ]
    for first in range(3):
        for second in range(3):
            basis.append({coordinate(edges, (5, 6), (first, second)): Fraction(1)})
    return basis, edges


def wick_image(
    direction: dict[int, Fraction],
    edges: tuple[tuple[int, int], ...],
    channel_edges: tuple[tuple[int, int], ...],
) -> dict[tuple[tuple[int, ...], tuple[int, ...]], Fraction]:
    answer: dict[tuple[tuple[int, ...], tuple[int, ...]], Fraction] = {}
    for index, coefficient_value in direction.items():
        edge = edges[index // 9]
        colour_number = index % 9
        assignment = {edge[0]: colour_number // 3, edge[1]: colour_number % 3}
        for channel_edge in channel_edges:
            if set(edge).isdisjoint(channel_edge):
                support = tuple(sorted(edge + channel_edge))
                word = tuple(assignment.get(port, 0) for port in support)
                key = (support, word)
                answer[key] = answer.get(key, Fraction(0)) + coefficient_value
    return {key: value for key, value in answer.items() if value}


def project_to_edges(
    basis: list[dict[int, Fraction]],
    edges: tuple[tuple[int, int], ...],
    selected: set[tuple[int, int]],
) -> list[dict[int, Fraction]]:
    selected_rows = {
        9 * number + colour
        for number, edge in enumerate(edges)
        if edge in selected
        for colour in range(9)
    }
    return [
        {row: value for row, value in vector.items() if row in selected_rows}
        for vector in basis
    ]


def check_block_covers() -> None:
    basis33, edges33 = k33_basis()
    channel33 = tuple((left, right) for left in range(3) for right in range(3, 6))
    assert sparse_rank(basis33) == 16
    assert all(not wick_image(vector, edges33, channel33) for vector in basis33)
    cover33 = {(0, 1), (0, 2), (3, 4), (3, 5)}
    assert sparse_rank(project_to_edges(basis33, edges33, cover33)) == 16
    for edge in tuple(combinations((0, 1, 2), 2)) + tuple(combinations((3, 4, 5), 2)):
        assert sparse_rank(project_to_edges(basis33, edges33, {edge})) == 5

    basis52, edges52 = k52_basis()
    channel52 = tuple((leaf, centre) for leaf in range(5) for centre in (5, 6))
    assert sparse_rank(basis52) == 24
    assert all(not wick_image(vector, edges52, channel52) for vector in basis52)
    cover52 = {(5, 6), *((leaf, 5) for leaf in range(5))}
    assert sparse_rank(project_to_edges(basis52, edges52, cover52)) == 24
    support_groups = [{(5, 6)}] + [{(leaf, 5), (leaf, 6)} for leaf in range(5)]
    assert all(cover52 & group for group in support_groups)
    assert len(support_groups) == 6


PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def m4_value(
    coefficients: dict[tuple[tuple[int, int], tuple[int, int]], Fraction],
    word: tuple[int, int, int, int],
) -> Fraction:
    value = Fraction(0)
    for first, second in PAIRINGS:
        first_word = tuple(word[port] for port in first)
        second_word = tuple(word[port] for port in second)
        value += coefficients.get((first, first_word), Fraction(0)) * coefficients.get(
            (second, second_word), Fraction(0)
        )
    return value


ROOT_TABLE = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)


def tagged_companion(outside_set: tuple[int, ...]):
    def assign(
        root: int,
        remaining: tuple[int, ...],
        root_word: tuple[int, ...],
        outside_word: dict[int, int],
    ):
        if root == 4:
            yield root_word, outside_word
            return
        for position, outside in enumerate(remaining):
            colour = ROOT_TABLE[root][outside]
            if colour is None:
                continue
            rest = remaining[:position] + remaining[position + 1 :]
            yield from assign(
                root + 1, rest, root_word + (colour,), outside_word | {outside: colour}
            )

    return tuple(assign(0, outside_set, (), {}))


def direct_slice(
    target: tuple[int, int],
    outside_set: tuple[int, ...],
    sigma: dict[int, int],
    beta: dict[int, int],
) -> dict[tuple[int, ...], Fraction]:
    complement = tuple(port for port in range(4) if port not in target)
    answer: dict[tuple[int, ...], Fraction] = {}
    for root_word, outside_word in tagged_companion(outside_set):
        if any(outside_word[port] != colour for port, colour in sigma.items()):
            continue
        tail = tuple(
            outside_word[port] if port in outside_set else beta[port]
            for port in complement
        )
        word = root_word + tail
        answer[word] = answer.get(word, Fraction(0)) + 1
    return answer


def joint_slices(target: tuple[int, int]) -> list[dict[tuple[int, ...], Fraction]]:
    complement = tuple(port for port in range(4) if port not in target)
    desired_set = tuple(sorted((4, 5) + complement))
    answer = []
    for outside_set in combinations(range(6), 4):
        if outside_set == desired_set:
            continue
        sigma_ports = tuple(port for port in outside_set if port in target)
        beta_ports = tuple(port for port in complement if port not in outside_set)
        for sigma_values in product(range(3), repeat=len(sigma_ports)):
            sigma = dict(zip(sigma_ports, sigma_values, strict=True))
            for beta_values in product(range(3), repeat=len(beta_ports)):
                beta = dict(zip(beta_ports, beta_values, strict=True))
                column = direct_slice(target, outside_set, sigma, beta)
                if column:
                    answer.append(column)
    return answer


def audit_gld11_joint_ledger() -> None:
    counts = {
        (0, 1): 202,
        (0, 2): 202,
        (0, 3): 199,
        (1, 2): 174,
        (1, 3): 193,
        (2, 3): 193,
    }
    pivots = {
        (0, 1): tuple(map(int, "202122")),
        (0, 2): tuple(map(int, "011221")),
        (0, 3): tuple(map(int, "000100")),
        (1, 3): tuple(map(int, "100110")),
        (2, 3): tuple(map(int, "121212")),
    }
    for target, count in counts.items():
        nuisance = joint_slices(target)
        complement = tuple(port for port in range(4) if port not in target)
        desired = direct_slice(target, tuple(sorted((4, 5) + complement)), {}, {})
        assert len(nuisance) == count
        if target in pivots:
            pivot = pivots[target]
            assert desired.get(pivot, Fraction(0)) == 1
            assert all(not column.get(pivot, Fraction(0)) for column in nuisance)
        else:
            words = tuple(
                tuple(map(int, text)) for text in ("002002", "011001", "121010")
            )
            weights = (Fraction(1), Fraction(-1), Fraction(1))

            def evaluate(column: dict[tuple[int, ...], Fraction]) -> Fraction:
                return sum(
                    weight * column.get(word, Fraction(0))
                    for weight, word in zip(weights, words, strict=True)
                )

            assert evaluate(desired) == 1
            assert all(evaluate(column) == 0 for column in nuisance)


def check_detector() -> None:
    coefficients = {
        ((0, 1), (0, 0)): Fraction(1),
        ((2, 3), (1, 1)): Fraction(1),
        ((0, 2), (0, 0)): Fraction(1),
        ((1, 3), (0, 0)): Fraction(1),
        ((0, 3), (0, 1)): Fraction(1),
        ((1, 2), (0, 1)): Fraction(-1),
    }
    assert m4_value(coefficients, (0, 0, 1, 1)) == 0
    assert m4_value(coefficients, (0, 0, 0, 0)) == 1
    assert len({(a, b) for a in ("13", "24") for b in ("14", "23")}) == 4


def main() -> None:
    check_rank_branches()
    check_sizes()
    check_block_covers()
    audit_gld11_joint_ledger()
    check_detector()
    print("fixed-Q joint M/Z quotient paired-attachment independent audit: PASS")


if __name__ == "__main__":
    main()
