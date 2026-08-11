"""Independent no-import audit of the GHZ moment-balanced gauge boundary."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

Edge = tuple[int, int]
Pair = tuple[int, int]
CodeTable = dict[Edge, tuple[int, Pair]]

ZERO: Pair = (0, 0)
ONE: Pair = (1, 0)
NEGATIVE_ONE: Pair = (-1, 0)


def pair_sum(left: Pair, right: Pair) -> Pair:
    """Add coefficient pairs in Z[w]/(w^2+w+1)."""
    return left[0] + right[0], left[1] + right[1]


def pair_product(left: Pair, right: Pair) -> Pair:
    """Multiply coefficient pairs by direct polynomial reduction."""
    constant = left[0] * right[0] - left[1] * right[1]
    linear = left[0] * right[1] + left[1] * right[0] - left[1] * right[1]
    return constant, linear


def squared_modulus(value: Pair) -> int:
    """Evaluate the Eisenstein norm without complex floating point."""
    return value[0] ** 2 - value[0] * value[1] + value[1] ** 2


def decode(code: int) -> tuple[int, int]:
    """Decode the two endpoint labels stored as a decimal digit pair."""
    return divmod(code, 10)


def audit_table() -> CodeTable:
    """Build the phase table independently of the primary verifier."""
    labels = {
        (0, 1): 0,
        (0, 2): 20,
        (0, 3): 0,
        (0, 4): 1,
        (0, 5): 11,
        (0, 6): 22,
        (0, 7): 10,
        (1, 2): 0,
        (1, 3): 22,
        (1, 4): 11,
        (1, 5): 12,
        (1, 6): 2,
        (1, 7): 21,
        (2, 3): 20,
        (2, 4): 0,
        (2, 5): 22,
        (2, 6): 11,
        (2, 7): 12,
        (3, 4): 10,
        (3, 5): 0,
        (3, 6): 21,
        (3, 7): 11,
        (4, 5): 0,
        (4, 6): 20,
        (4, 7): 22,
        (5, 6): 10,
        (5, 7): 0,
        (6, 7): 0,
    }
    phases = {edge: ONE for edge in labels}
    phases[(0, 1)] = (0, -1)
    phases[(1, 2)] = (1, 1)
    phases[(0, 4)] = NEGATIVE_ONE
    phases[(0, 7)] = NEGATIVE_ONE
    return {edge: (labels[edge], phases[edge]) for edge in labels}


def compatible_recursion(table: CodeTable, word: tuple[int, ...]):
    """Compute one fibre through a least-set-bit hafnian recursion."""
    full_mask = (1 << len(word)) - 1

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[Pair, Pair, int, int]:
        if mask == 0:
            return ONE, ZERO, 1, 0
        first_bit = mask & -mask
        left = first_bit.bit_length() - 1
        residue = mask ^ first_bit
        diagonal_sum = ZERO
        offdiagonal_sum = ZERO
        diagonal_count = 0
        offdiagonal_count = 0
        choices = residue
        while choices:
            partner_bit = choices & -choices
            right = partner_bit.bit_length() - 1
            choices ^= partner_bit
            code, phase = table[(left, right)]
            left_label, right_label = decode(code)
            if (left_label, right_label) != (word[left], word[right]):
                continue
            d_sum, o_sum, d_count, o_count = recurse(residue ^ partner_bit)
            if left_label == right_label:
                diagonal_sum = pair_sum(diagonal_sum, pair_product(phase, d_sum))
                offdiagonal_sum = pair_sum(
                    offdiagonal_sum,
                    pair_product(phase, o_sum),
                )
                diagonal_count += d_count
                offdiagonal_count += o_count
            else:
                combined = pair_sum(d_sum, o_sum)
                offdiagonal_sum = pair_sum(
                    offdiagonal_sum,
                    pair_product(phase, combined),
                )
                offdiagonal_count += d_count + o_count
        return diagonal_sum, offdiagonal_sum, diagonal_count, offdiagonal_count

    return recurse(full_mask)


def moment_census(table: CodeTable) -> tuple[tuple[int, int, int], ...]:
    """Accumulate the actual squared phase magnitudes at labelled endpoints."""
    loads = [[0, 0, 0] for _ in range(8)]
    for (left, right), (code, phase) in table.items():
        left_label, right_label = decode(code)
        magnitude = squared_modulus(phase)
        loads[left][left_label] += magnitude
        loads[right][right_label] += magnitude
    return tuple(tuple(row) for row in loads)


def alternate_restricted_incidence(table: CodeTable) -> list[list[int]]:
    """Use vertex zero, rather than seven, as the colour-sum anchor."""
    basis = [(vertex, colour) for colour in range(3) for vertex in range(1, 8)]
    rows = []
    for (left, right), (code, _) in table.items():
        left_label, right_label = decode(code)
        row = []
        for vertex, colour in basis:
            value = int((left, left_label) == (vertex, colour))
            value += int((right, right_label) == (vertex, colour))
            value -= int((left, left_label) == (0, colour))
            value -= int((right, right_label) == (0, colour))
            row.append(value)
        rows.append(row)
    return rows


def modular_rank(matrix: list[list[int]], prime: int) -> int:
    """Compute rank over a prime field using only integer modular arithmetic."""
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [(entry * inverse) % prime for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def transpose_product(matrix: list[list[int]]) -> list[list[int]]:
    """Form R^T R through an implementation separate from the primary."""
    width = len(matrix[0])
    return [
        [sum(row[left] * row[right] for row in matrix) for right in range(width)]
        for left in range(width)
    ]


def audit_moment_geometry(table: CodeTable) -> dict[str, object]:
    """Audit balance, quotient rank, and a genuine edgewise stabilizer."""
    assert all(squared_modulus(phase) == 1 for _, phase in table.values())
    census = moment_census(table)
    assert census == ((3, 2, 2),) * 8

    incidence = alternate_restricted_incidence(table)
    assert [sum(row[column] for row in incidence) for column in range(21)] == [
        0
    ] * 21
    prime = 101
    assert modular_rank(incidence, prime) == 20
    assert modular_rank(transpose_product(incidence), prime) == 20

    stabilizer_rows = (
        (1, 1, -1),
        (-1, 1, 1),
        (1, -1, 1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, -1),
        (1, 1, 1),
        (-1, -1, 1),
    )
    assert tuple(sum(row[colour] for row in stabilizer_rows) for colour in range(3)) == (
        0,
        0,
        0,
    )
    for (left, right), (code, _) in table.items():
        left_label, right_label = decode(code)
        assert (
            stabilizer_rows[left][left_label]
            + stabilizer_rows[right][right_label]
            == 0
        )
    return {
        "actual_squared_magnitude_loads": census[0],
        "modular_rank_lower_bound": 20,
        "explicit_kernel_upper_bound": 20,
        "edgewise_stabilizer_dimension": 1,
    }


def audit_nonrigidity(table: CodeTable) -> tuple[tuple[int, ...], ...]:
    """Recompute all three S_c sets directly from decimal label codes."""
    sets = []
    for colour in range(3):
        active = set()
        for (left, right), (code, _) in table.items():
            left_label, right_label = decode(code)
            if left_label != colour and right_label == colour:
                active.add(left)
            if right_label != colour and left_label == colour:
                active.add(right)
        sets.append(tuple(sorted(active)))
    result = tuple(sets)
    assert result == (
        (0, 2, 3, 4, 5, 6),
        (0, 1, 3, 4, 5, 6, 7),
        (1, 2, 3, 6, 7),
    )
    return result


def audit_selected_fibres(table: CodeTable) -> dict[str, object]:
    """Audit pure targets, active cancellations, bridges, and nonwitness word."""
    pure = []
    for colour in range(3):
        diagonal, offdiagonal, diagonal_count, offdiagonal_count = (
            compatible_recursion(table, (colour,) * 8)
        )
        assert pair_sum(diagonal, offdiagonal) == ONE
        assert offdiagonal == ZERO
        assert offdiagonal_count == 0
        pure.append((diagonal, diagonal_count))
    assert pure == [(ONE, 2), (ONE, 1), (ONE, 1)]

    chi_0 = (0, 1, 2, 0, 1, 2, 0, 0)
    chi_1 = (1, 2, 0, 2, 0, 1, 0, 0)
    active = {}
    for word in (chi_0, chi_1):
        diagonal, offdiagonal, diagonal_count, offdiagonal_count = (
            compatible_recursion(table, word)
        )
        assert (diagonal, offdiagonal) == (ONE, NEGATIVE_ONE)
        assert (diagonal_count, offdiagonal_count) == (1, 1)
        assert pair_sum(diagonal, offdiagonal) == ZERO
        active[word] = (diagonal, offdiagonal)

    bridges = {
        (0, 4): (0, 1),
        (1, 5): (1, 2),
        (2, 3): (2, 0),
        (2, 4): (0, 0),
        (0, 5): (1, 1),
        (1, 3): (2, 2),
    }
    for edge, labels in bridges.items():
        assert decode(table[edge][0]) == labels

    exposed = (0, 0, 0, 0, 0, 0, 2, 0)
    diagonal, offdiagonal, diagonal_count, offdiagonal_count = compatible_recursion(
        table,
        exposed,
    )
    assert (diagonal, offdiagonal) == (ZERO, ONE)
    assert (diagonal_count, offdiagonal_count) == (0, 1)
    return {
        "pure_values_and_counts": pure,
        "active_fibres": active,
        "exposed_word": exposed,
        "perfect_matchings": 1 * 3 * 5 * 7,
    }


def main() -> None:
    table = audit_table()
    assert set(table) == set(combinations(range(8), 2))
    geometry = audit_moment_geometry(table)
    flags = audit_nonrigidity(table)
    fibres = audit_selected_fibres(table)
    print("matrix-unit GHZ moment-balanced gauge independent audit: PASS")
    print(f"  alternate moment/rank audit: {geometry}")
    print(f"  proper nonrigidity sets: {flags}")
    print(f"  bitmask phase-fibre audit: {fibres}")


if __name__ == "__main__":
    main()
