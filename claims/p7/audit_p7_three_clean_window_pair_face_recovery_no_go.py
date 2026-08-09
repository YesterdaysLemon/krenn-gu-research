"""Independent no-import audit of the three-window pair-face no-go."""

from fractions import Fraction
from itertools import combinations, permutations

PORTS = tuple(range(6))
TARGET = frozenset(range(4))
EDGES = tuple(combinations(PORTS, 2))
TARGET_COLUMNS = tuple(i for i, edge in enumerate(EDGES) if set(edge) <= TARGET)
NUISANCE_COLUMNS = tuple(i for i in range(15) if i not in TARGET_COLUMNS)

REPRESENTATIVES = (
    ("1256", "3456"),
    ("1256", "1456"),
    ("3456", "3456"),
    ("1345", "2356"),
    ("1245", "2456"),
    ("1236", "2345"),
    ("1235", "1345"),
    ("1245", "1246"),
    ("2346", "2346"),
)

WITNESSES = (
    (0, 1, -1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, -2, 1, 0, -1, 1, -2, -1, 0, 1, 0, 0, -1, 0, 1),
    (0, 1, -1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, 1, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0),
    (-1, 0, 1, 0, 0, 1, 0, 1, -1, -1, 0, 0, -1, 1, 0),
    (1, -1, 0, 0, 0, 0, -1, 1, -1, 1, -1, 1, 0, 0, 0),
    (-1, 2, -1, -1, 0, -1, 2, 2, 0, -1, -1, 0, 2, 0, 0),
    (0, -1, 1, -1, -1, 1, -1, 1, 1, 0, 0, 0, 0, 0, 0),
    (-1, 1, 0, 0, 0, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0),
)


def parse(label):
    return frozenset(int(value) - 1 for value in label)


def matrix(windows):
    return [
        [Fraction(int(vertex in edge and set(edge) <= current)) for edge in EDGES]
        for current in windows
        for vertex in sorted(current)
    ]


def rank(rows):
    work = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def matvec(rows, vector):
    return [sum(entry * value for entry, value in zip(row, vector)) for row in rows]


def canonical(pair):
    return tuple(sorted(pair, key=lambda value: tuple(sorted(value))))


def images(pair):
    result = set()
    for inside in permutations(range(4)):
        for outside in ((4, 5), (5, 4)):
            relabel = dict(zip(PORTS, inside + outside))
            current = tuple(
                frozenset(relabel[value] for value in item) for item in pair
            )
            result.add(canonical(current))
            result.add(canonical((current[1], current[0])))
    return result


def main():
    pairs = tuple(canonical((parse(left), parse(right))) for left, right in REPRESENTATIVES)
    covered = set()
    for pair in pairs:
        covered.update(images(pair))
    others = tuple(
        frozenset(values)
        for values in combinations(PORTS, 4)
        if frozenset(values) != TARGET
    )
    assert covered == {canonical((left, right)) for left in others for right in others}

    recoveries = []
    for pair, witness in zip(pairs, WITNESSES):
        rows = matrix((TARGET,) + pair)
        assert matvec(rows, witness) == [0] * len(rows)
        assert any(witness[index] for index in TARGET_COLUMNS)
        total_rank = rank(rows)
        nuisance_rank = rank(
            [[row[column] for column in NUISANCE_COLUMNS] for row in rows]
        )
        recoveries.append(total_rank - nuisance_rank)
    assert max(recoveries) == 5
    assert set(recoveries) == {4, 5}

    print("AUDIT PASS: nine stabilizer orbits cover every window pair")
    print("AUDIT PASS: all integer witnesses are invisible and target-nonzero")
    print("AUDIT PASS: maximum recovery dimension is five and is attained")
    print("searches=0")


if __name__ == "__main__":
    main()
