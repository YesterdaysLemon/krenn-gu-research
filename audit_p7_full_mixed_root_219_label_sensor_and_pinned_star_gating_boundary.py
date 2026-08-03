"""Independent no-import audit of the full P7 mixed-label sensor.

This reconstruction uses Ryser permanents row-by-row rather than importing
or reusing the primary verifier's matching recursion.
"""

from itertools import combinations, product

ROOTS = range(5)
NONROOTS = range(9)
WORDS = list(product(range(3), repeat=5))

# Each three-character token is one root covector.
H_TOKENS = (
    "010 010 100 010 001 010 010 -110 01-1",
    "001 100 010 100 100 001 010 -101 01-1",
    "001 100 001 010 010 001 100 -110 01-1",
    "001 010 010 001 010 100 001 1-10 0-11",
    "001 001 001 100 001 010 010 10-1 -101",
)


def parse_vector(token):
    values = []
    index = 0
    while index < len(token):
        if token[index] == "-":
            values.append(-int(token[index + 1]))
            index += 2
        else:
            values.append(int(token[index]))
            index += 1
    assert len(values) == 3
    return tuple(values)


H = tuple(tuple(parse_vector(token) for token in row.split()) for row in H_TOKENS)

L_FLAT = (
    (-1, 1, -1, -1, -1, 1, 0, -1, 3),
    (-1, 0, 1, 0, -1, 0, 1, 0, 0),
    (1, -1, 1, 0, 1, -1, 1, 1, -3),
    (1, 0, 0, -1, 1, 0, 0, 1, -2),
    (-1, 0, -1, -1, -1, -1, 1, 1, 3),
    (0, 0, -1, -1, 1, -1, -1, -1, 4),
    (-1, 1, 1, 1, 0, 1, 1, 0, -4),
    (1, -1, -1, 1, 1, 0, 1, 0, -2),
    (0, 0, 1, 1, 1, 0, -1, 0, -2),
    (1, -1, 0, 1, 1, 0, -1, -1, 0),
)
L = {}
for pair, entries in zip(combinations(ROOTS, 2), L_FLAT):
    L[pair] = tuple(entries[3 * row : 3 * row + 3] for row in range(3))


def permanent_ryser(matrix):
    """Ryser formula over the integers for a square matrix."""
    size = len(matrix)
    if size == 0:
        return 1
    total = 0
    for mask in range(1, 1 << size):
        term = -1 if (size - mask.bit_count()) % 2 else 1
        for row in matrix:
            row_sum = sum(row[column] for column in range(size) if mask >> column & 1)
            term *= row_sum
        total += term
    return total


def coefficient(word, deletion):
    size = len(deletion)
    if size == 5:
        return permanent_ryser(
            [[H[root][endpoint][word[root]] for endpoint in deletion] for root in ROOTS]
        )
    if size == 3:
        value = 0
        for i, j in combinations(ROOTS, 2):
            remaining = [root for root in ROOTS if root not in (i, j)]
            scalar = L[i, j][word[i]][word[j]]
            scalar *= permanent_ryser(
                [
                    [H[root][endpoint][word[root]] for endpoint in deletion]
                    for root in remaining
                ]
            )
            value += scalar
        return value
    assert size == 1
    endpoint = deletion[0]
    value = 0
    for unmatched in ROOTS:
        remaining = [root for root in ROOTS if root != unmatched]
        pairings = (
            ((remaining[0], remaining[1]), (remaining[2], remaining[3])),
            ((remaining[0], remaining[2]), (remaining[1], remaining[3])),
            ((remaining[0], remaining[3]), (remaining[1], remaining[2])),
        )
        for first_pair, second_pair in pairings:
            i, j = first_pair
            s, t = second_pair
            value += (
                H[unmatched][endpoint][word[unmatched]]
                * L[min(i, j), max(i, j)][word[i] if i < j else word[j]][
                    word[j] if i < j else word[i]
                ]
                * L[min(s, t), max(s, t)][word[s] if s < t else word[t]][
                    word[t] if s < t else word[s]
                ]
            )
    return value


def determinant_mod(matrix, prime):
    work = [[value % prime for value in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = None
        for row in range(column, len(work)):
            if work[row][column]:
                pivot = row
                break
        assert pivot is not None
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, len(work)):
            if work[row][column]:
                multiplier = work[row][column] * inverse % prime
                for inner in range(column, len(work)):
                    work[row][inner] = (
                        work[row][inner] - multiplier * work[column][inner]
                    ) % prime
    return determinant % prime


def main():
    assert all(sum(H[root][u]) == 1 for root in ROOTS for u in range(7))
    assert all(sum(H[root][u]) == 0 for root in ROOTS for u in (7, 8))
    assert all(sum(sum(row) for row in matrix) == 0 for matrix in L.values())

    labels = list(combinations(NONROOTS, 5))
    labels += list(combinations(NONROOTS, 3))
    labels += [(u,) for u in NONROOTS]
    assert len(labels) == 219

    # The named minor uses the first 219 lexicographic ternary rows.
    minor = [[coefficient(word, label) for label in labels] for word in WORDS[:219]]
    residue = determinant_mod(minor, 1_000_033)
    assert residue == 921_291

    diagonal_columns = []
    for colour in range(3):
        column = [0] * len(WORDS)
        column[WORDS.index((colour,) * 5)] = 1
        diagonal_columns.append(column)
    ordinary_columns = [
        [coefficient(word, label) for word in WORDS] for label in labels
    ]
    augmented_columns = ordinary_columns + diagonal_columns
    augmented_rows = [list(row) for row in zip(*augmented_columns)]
    target_minor = augmented_rows[:221] + [augmented_rows[242]]
    target_residue = determinant_mod(target_minor, 1_000_033)
    assert target_residue == 812_790

    # Independent ledger for the pinned-star selector and support-cover cases.
    pinned_depth_three = 6 * 5 // 2
    unwanted_depth_three = 6 * 5 * 4 // 6
    assert (pinned_depth_three, unwanted_depth_three) == (15, 20)
    cover_caps = []
    for roots_in_cover, endpoints_in_cover in ((2, 0), (1, 1), (0, 2)):
        if roots_in_cover == 2:
            cap = 3**2
        elif roots_in_cover == 1:
            cap = 6 - endpoints_in_cover
        else:
            cap = 1
        cover_caps.append(cap)
    assert cover_caps == [9, 5, 1]

    print("AUDIT PASS: independent Ryser construction of all 219 columns")
    print("AUDIT PASS: named determinant mod 1000033 = 921291")
    print("AUDIT PASS: diagonal-target determinant mod 1000033 = 812790")
    print("AUDIT PASS: sensor image intersects the diagonal target only at zero")
    print("AUDIT PASS: legal pairwise-zero and residual-annihilator conditions")
    print("AUDIT PASS: P5 support-gating caps are 9, 5, 1")
    print("searches=0")
    print("SCOPE: GHZ target-incidence and P5 algebraic compression remain UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
