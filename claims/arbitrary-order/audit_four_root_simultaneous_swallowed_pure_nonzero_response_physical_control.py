"""Independent no-import audit of the simultaneous swallowed-pure control."""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


ROOT_TABLE = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)
OUTSIDE = {
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
B = tuple(range(6))


def edge(left: int, right: int):
    if left > right:
        left, right = right, left
    if right < 4:
        return None
    if left < 4:
        return ROOT_TABLE[left][right - 4]
    return OUTSIDE[(left - 4, right - 4)]


@lru_cache(maxsize=None)
def recurrence(vertices: tuple[int, ...]) -> Counter[tuple[tuple[int, int], ...]]:
    if not vertices:
        return Counter({(): 1})
    first = vertices[0]
    answer = Counter()
    for position in range(1, len(vertices)):
        second = vertices[position]
        colour = edge(first, second)
        if colour is None:
            continue
        remaining = vertices[1:position] + vertices[position + 1 :]
        for assignment, coefficient in recurrence(remaining).items():
            tagged = tuple(sorted(assignment + ((first, colour), (second, colour))))
            answer[tagged] += coefficient
    return answer


def counter(vertices: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    return Counter(
        {
            tuple(dict(assignment)[vertex] for vertex in vertices): coefficient
            for assignment, coefficient in recurrence(vertices).items()
        }
    )


def audit_state() -> None:
    full = counter(tuple(range(10)))
    assert len(full) == 119 and sum(full.values()) == 124
    assert tuple(full[(colour,) * 10] for colour in range(3)) == (1, 1, 1)
    assert full[tuple(map(int, "1200100020"))] == 1
    assert all(
        full[tuple(other if position == changed else colour for position in range(10))]
        == 0
        for colour in range(3)
        for changed in range(10)
        for other in range(3)
        if other != colour
    )


def tagged_companion(outside_set: tuple[int, ...]):
    vertices = tuple(range(4)) + tuple(4 + index for index in outside_set)

    def allowed(left: int, right: int):
        return (left < 4) != (right < 4)

    def walk(remaining: tuple[int, ...], assignment: dict[int, int]):
        if not remaining:
            yield assignment
            return
        first = remaining[0]
        for position in range(1, len(remaining)):
            second = remaining[position]
            if not allowed(first, second):
                continue
            root = first if first < 4 else second
            outside = second - 4 if first < 4 else first - 4
            colour = ROOT_TABLE[root][outside]
            if colour is None:
                continue
            rest = remaining[1:position] + remaining[position + 1 :]
            yield from walk(rest, assignment | {root: colour, outside + 4: colour})

    return tuple(walk(vertices, {}))


def nu(target, outside_set, sigma, beta):
    complement = tuple(index for index in U if index not in target)
    answer = Counter()
    for assignment in tagged_companion(tuple(outside_set)):
        outside_word = {
            index - 4: colour for index, colour in assignment.items() if index >= 4
        }
        if any(outside_word[index] != colour for index, colour in sigma.items()):
            continue
        root_word = tuple(assignment[root] for root in range(4))
        tail = tuple(
            outside_word[index] if index in outside_set else beta[index]
            for index in complement
        )
        answer[root_word + tail] += 1
    return +answer


def identity_ledger():
    def t(sign, outside, sigma, beta=None):
        return sign, tuple(outside), dict(sigma), dict(beta or {})

    return {
        ((0, 1), 0): [t(1, (0, 1, 2, 5), {0: 0, 1: 0}, {3: 0})],
        ((0, 1), 1): [t(1, (0, 1, 2, 3), {0: 1, 1: 1})],
        ((0, 1), 2): [t(1, (0, 1, 2, 3), {0: 2, 1: 2})],
        ((0, 2), 0): [t(1, (0, 1, 2, 5), {0: 0, 2: 0}, {3: 0})],
        ((0, 2), 1): [t(1, (0, 1, 2, 3), {0: 1, 2: 1})],
        ((0, 2), 2): [
            t(1, (0, 1, 2, 3), {0: 2, 2: 2}),
            t(-1, (0, 1, 2, 4), {0: 0, 2: 2}, {3: 0}),
        ],
        ((0, 3), 0): [
            t(-1, (0, 2, 3, 5), {0: 2, 3: 0}, {1: 0}),
            t(1, (0, 2, 4, 5), {0: 0}, {1: 0}),
        ],
        ((0, 3), 1): [t(1, (0, 1, 3, 4), {0: 1, 3: 1}, {2: 1})],
        ((0, 3), 2): [t(1, (0, 1, 3, 5), {0: 2, 3: 2}, {2: 2})],
        ((1, 2), 0): [t(1, (0, 1, 2, 5), {1: 0, 2: 0}, {3: 0})],
        ((1, 2), 1): [t(1, (0, 1, 2, 3), {1: 1, 2: 1})],
        ((1, 2), 2): [t(1, (0, 1, 2, 3), {1: 2, 2: 2})],
        ((1, 3), 0): [t(1, (1, 2, 3, 5), {1: 0, 3: 0}, {0: 0})],
        ((1, 3), 1): [
            t(1, (0, 1, 3, 4), {1: 1, 3: 1}, {2: 1}),
            t(-1, (0, 1, 3, 5), {1: 0, 3: 1}, {2: 1}),
        ],
        ((1, 3), 2): [t(1, (0, 1, 2, 3), {1: 2, 3: 2})],
        ((2, 3), 0): [t(1, (1, 2, 3, 5), {2: 0, 3: 0}, {0: 0})],
        ((2, 3), 1): [t(1, (0, 1, 2, 3), {2: 1, 3: 1})],
        ((2, 3), 2): [t(1, (0, 1, 2, 3), {2: 2, 3: 2})],
        (U, 0): [t(1, (0, 1, 2, 5), {0: 0, 1: 0, 2: 0})],
        (U, 1): [t(1, (0, 1, 2, 3), {0: 1, 1: 1, 2: 1, 3: 1})],
        (U, 2): [t(1, (0, 1, 2, 3), {0: 2, 1: 2, 2: 2, 3: 2})],
    }


def audit_identities() -> None:
    ledger = identity_ledger()
    passed = 0
    for (target, colour), expression in ledger.items():
        result = Counter()
        for sign, outside_set, sigma, beta in expression:
            for word, coefficient in nu(target, outside_set, sigma, beta).items():
                result[word] += sign * coefficient
        result = Counter({word: value for word, value in result.items() if value})
        length = 4 + len(set(U) - set(target))
        assert result == Counter({(colour,) * length: 1})
        passed += 1
    assert passed == 21


def sparse_rank(columns: list[Counter[tuple[int, ...]]]) -> int:
    def index(word):
        value = 0
        for digit in word:
            value = 3 * value + digit
        return value

    basis: dict[int, dict[int, Fraction]] = {}
    for column in columns:
        vector = {index(word): Fraction(value) for word, value in column.items()}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = vector[pivot]
                basis[pivot] = {row: value / scale for row, value in vector.items()}
                break
            factor = vector[pivot]
            for row, value in basis[pivot].items():
                vector[row] = vector.get(row, Fraction(0)) - factor * value
                if not vector[row]:
                    del vector[row]
    return len(basis)


def audit_ranks() -> None:
    expected = {
        (0, 1): (203, 175),
        (0, 2): (203, 174),
        (0, 3): (200, 165),
        (1, 2): (175, 157),
        (1, 3): (194, 166),
        (2, 3): (194, 169),
        U: (115, 61),
    }
    for target, wanted in expected.items():
        complement = tuple(index for index in U if index not in target)
        unique = {}
        raw_count = 0
        for outside_set in combinations(B, 4):
            sigma_indices = tuple(index for index in outside_set if index in target)
            beta_indices = tuple(
                index for index in complement if index not in outside_set
            )
            for sigma_values in product(range(3), repeat=len(sigma_indices)):
                sigma = dict(zip(sigma_indices, sigma_values, strict=True))
                for beta_values in product(range(3), repeat=len(beta_indices)):
                    beta = dict(zip(beta_indices, beta_values, strict=True))
                    column = nu(target, outside_set, sigma, beta)
                    if column:
                        raw_count += 1
                        unique[tuple(sorted(column.items()))] = column
        columns = list(unique.values())
        assert (raw_count, sparse_rank(columns)) == wanted
        for colour in range(3):
            pure = Counter({(colour,) * (4 + len(complement)): 1})
            assert sparse_rank(columns + [pure]) == wanted[1]


def main() -> None:
    audit_state()
    audit_identities()
    audit_ranks()
    print("four-root simultaneous swallowed-pure independent audit: PASS")


if __name__ == "__main__":
    main()
