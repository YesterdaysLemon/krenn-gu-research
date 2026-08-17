"""Primary exact verifier for the simultaneous swallowed-pure control."""

from collections import Counter
from itertools import combinations, permutations, product

import sympy as sp
from sympy.polys.matrices import DomainMatrix


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
U = (0, 1, 2, 3)
Q = (4, 5)
B = U + Q


def edge_colour(left: int, right: int) -> int | None:
    if left > right:
        left, right = right, left
    if right < 4:
        return None
    if left < 4:
        return ROOT_TABLE[left][right - 4]
    return OUTSIDE_COLOURS[(left - 4, right - 4)]


def matching_assignments(vertices: tuple[int, ...]) -> list[dict[int, int]]:
    if not vertices:
        return [{}]
    first = vertices[0]
    assignments = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        colour = edge_colour(first, second)
        if colour is None:
            continue
        remaining = vertices[1:index] + vertices[index + 1 :]
        for assignment in matching_assignments(remaining):
            assignments.append(assignment | {first: colour, second: colour})
    return assignments


def word_counter(vertices: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    return Counter(
        tuple(assignment[vertex] for vertex in vertices)
        for assignment in matching_assignments(vertices)
    )


def check_state_and_responses() -> None:
    full_vertices = tuple(range(10))
    full = word_counter(full_vertices)
    assert len(full) == 119
    assert sum(full.values()) == 124
    for colour in range(3):
        assert full[(colour,) * 10] == 1
        for vertex in range(10):
            for other in set(range(3)) - {colour}:
                word = [colour] * 10
                word[vertex] = other
                assert full[tuple(word)] == 0
    mixed = tuple(int(digit) for digit in "1200100020")
    assert full[mixed] == 1
    for vertex in range(10):
        minor = sp.Matrix(
            [
                [
                    full[
                        tuple(
                            row_colour if index == vertex else column_colour
                            for index in range(10)
                        )
                    ]
                    for column_colour in range(3)
                ]
                for row_colour in range(3)
            ]
        )
        assert minor == sp.eye(3)

    expected = {
        (0, 1): {"00": 1, "02": 1, "20": 1},
        (0, 2): {"01": 1, "22": 2},
        (0, 3): {"00": 1, "01": 1, "20": 1},
        (1, 2): {"01": 1, "11": 1, "22": 1},
        (1, 3): {"01": 1, "11": 1, "20": 1},
        (2, 3): {"00": 1, "10": 1, "21": 1},
        U: {
            "0000": 1,
            "0010": 2,
            "0021": 1,
            "0110": 1,
            "0111": 2,
            "0200": 1,
            "0220": 1,
            "2000": 1,
            "2021": 1,
            "2110": 1,
            "2121": 2,
            "2220": 1,
        },
    }
    for target, wanted in expected.items():
        vertices = tuple(4 + index for index in Q + target)
        counter = word_counter(vertices)
        contracted = Counter()
        for word, coefficient in counter.items():
            open_word = word[2:]
            contracted["".join(map(str, open_word))] += coefficient
        assert dict(contracted) == wanted
        assert sum(contracted.values()) == (15 if target == U else 3)


def companion_terms(outside_set: tuple[int, ...]):
    for assigned in permutations(outside_set):
        root_colours = []
        outside_colours = {}
        for root, outside in enumerate(assigned):
            colour = ROOT_TABLE[root][outside]
            if colour is None:
                break
            root_colours.append(colour)
            outside_colours[outside] = colour
        else:
            yield tuple(root_colours), outside_colours


def nuisance_slice(
    target: tuple[int, ...],
    outside_set: tuple[int, ...],
    sigma: dict[int, int],
    beta: dict[int, int],
) -> Counter[tuple[int, ...]]:
    complement = tuple(index for index in U if index not in target)
    answer = Counter()
    for root_word, outside_word in companion_terms(outside_set):
        if any(outside_word[index] != colour for index, colour in sigma.items()):
            continue
        complement_word = tuple(
            outside_word[index] if index in outside_set else beta[index]
            for index in complement
        )
        answer[root_word + complement_word] += 1
    return +answer


def certificates():
    def term(sign, outside, sigma, beta=None):
        return (sign, tuple(outside), dict(sigma), dict(beta or {}))

    return {
        ((0, 1), 0): [term(1, (0, 1, 2, 5), {0: 0, 1: 0}, {3: 0})],
        ((0, 1), 1): [term(1, (0, 1, 2, 3), {0: 1, 1: 1})],
        ((0, 1), 2): [term(1, (0, 1, 2, 3), {0: 2, 1: 2})],
        ((0, 2), 0): [term(1, (0, 1, 2, 5), {0: 0, 2: 0}, {3: 0})],
        ((0, 2), 1): [term(1, (0, 1, 2, 3), {0: 1, 2: 1})],
        ((0, 2), 2): [
            term(1, (0, 1, 2, 3), {0: 2, 2: 2}),
            term(-1, (0, 1, 2, 4), {0: 0, 2: 2}, {3: 0}),
        ],
        ((0, 3), 0): [
            term(-1, (0, 2, 3, 5), {0: 2, 3: 0}, {1: 0}),
            term(1, (0, 2, 4, 5), {0: 0}, {1: 0}),
        ],
        ((0, 3), 1): [term(1, (0, 1, 3, 4), {0: 1, 3: 1}, {2: 1})],
        ((0, 3), 2): [term(1, (0, 1, 3, 5), {0: 2, 3: 2}, {2: 2})],
        ((1, 2), 0): [term(1, (0, 1, 2, 5), {1: 0, 2: 0}, {3: 0})],
        ((1, 2), 1): [term(1, (0, 1, 2, 3), {1: 1, 2: 1})],
        ((1, 2), 2): [term(1, (0, 1, 2, 3), {1: 2, 2: 2})],
        ((1, 3), 0): [term(1, (1, 2, 3, 5), {1: 0, 3: 0}, {0: 0})],
        ((1, 3), 1): [
            term(1, (0, 1, 3, 4), {1: 1, 3: 1}, {2: 1}),
            term(-1, (0, 1, 3, 5), {1: 0, 3: 1}, {2: 1}),
        ],
        ((1, 3), 2): [term(1, (0, 1, 2, 3), {1: 2, 3: 2})],
        ((2, 3), 0): [term(1, (1, 2, 3, 5), {2: 0, 3: 0}, {0: 0})],
        ((2, 3), 1): [term(1, (0, 1, 2, 3), {2: 1, 3: 1})],
        ((2, 3), 2): [term(1, (0, 1, 2, 3), {2: 2, 3: 2})],
        (U, 0): [term(1, (0, 1, 2, 5), {0: 0, 1: 0, 2: 0})],
        (U, 1): [term(1, (0, 1, 2, 3), {0: 1, 1: 1, 2: 1, 3: 1})],
        (U, 2): [term(1, (0, 1, 2, 3), {0: 2, 1: 2, 2: 2, 3: 2})],
    }


def check_certificates() -> None:
    ledger = certificates()
    assert len(ledger) == 21
    for (target, colour), expression in ledger.items():
        result = Counter()
        for sign, outside, sigma, beta in expression:
            result.update(
                {
                    word: sign * coefficient
                    for word, coefficient in nuisance_slice(
                        target, outside, sigma, beta
                    ).items()
                }
            )
        result = Counter({word: value for word, value in result.items() if value})
        complement = tuple(index for index in U if index not in target)
        assert result == Counter({(colour,) * (4 + len(complement)): 1})


def word_index(word: tuple[int, ...]) -> int:
    value = 0
    for digit in word:
        value = 3 * value + digit
    return value


def nuisance_columns(target: tuple[int, ...]):
    complement = tuple(index for index in U if index not in target)
    unique = {}
    raw_count = 0
    for outside in combinations(B, 4):
        sigma_indices = tuple(index for index in outside if index in target)
        beta_indices = tuple(index for index in complement if index not in outside)
        for sigma_values in product(range(3), repeat=len(sigma_indices)):
            sigma = dict(zip(sigma_indices, sigma_values, strict=True))
            for beta_values in product(range(3), repeat=len(beta_indices)):
                beta = dict(zip(beta_indices, beta_values, strict=True))
                column = nuisance_slice(target, outside, sigma, beta)
                if column:
                    raw_count += 1
                    key = tuple(sorted(column.items()))
                    unique[key] = column
    return raw_count, list(unique.values())


def check_nuisance_ranks() -> None:
    expected = {
        (0, 1): (203, 175),
        (0, 2): (203, 174),
        (0, 3): (200, 165),
        (1, 2): (175, 157),
        (1, 3): (194, 166),
        (2, 3): (194, 169),
        U: (115, 61),
    }
    for target, (column_count, wanted_rank) in expected.items():
        complement = tuple(index for index in U if index not in target)
        row_count = 3 ** (4 + len(complement))
        raw_count, columns = nuisance_columns(target)
        assert raw_count == column_count
        entries = {}
        for column_index, column in enumerate(columns):
            for word, coefficient in column.items():
                entries[(word_index(word), column_index)] = coefficient
        matrix = sp.MutableSparseMatrix(row_count, len(columns), entries)
        assert DomainMatrix.from_Matrix(matrix).rank() == wanted_rank


def check_structure() -> None:
    for outside in range(6):
        column = [ROOT_TABLE[root][outside] for root in range(4)]
        assert set(column) == {0, 1, 2, None}
    assert len(OUTSIDE_COLOURS) == 15
    assert all(colour in (0, 1, 2) for colour in OUTSIDE_COLOURS.values())


def main() -> None:
    check_structure()
    check_state_and_responses()
    check_certificates()
    check_nuisance_ranks()
    print("four-root simultaneous swallowed-pure primary replay: PASS")


if __name__ == "__main__":
    main()
