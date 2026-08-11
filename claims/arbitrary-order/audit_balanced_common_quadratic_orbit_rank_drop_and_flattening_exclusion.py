"""Independent no-import audit of the common-quadratic exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product


def matchings(vertices: tuple[int, ...]):
    """Generate labelled matchings by removing the least remaining vertex."""
    if len(vertices) == 0:
        yield ()
        return
    anchor = vertices[0]
    tail = vertices[1:]
    for place, mate in enumerate(tail):
        unused = tail[:place] + tail[place + 1 :]
        for continuation in matchings(unused):
            yield ((anchor, mate),) + continuation


def rational_rank(rows: list[list[int]]) -> int:
    """Compute exact row rank by a separately written Fraction elimination."""
    if not rows:
        return 0
    work = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * basis
                for value, basis in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def coordinate_coefficient(word: tuple[int, ...]) -> int:
    """Evaluate the identity-form tensor by direct matching enumeration."""
    total = 0
    for matching in matchings(tuple(range(len(word)))):
        if all(word[left] == word[right] for left, right in matching):
            total += 1
    return total


def certificate_words(m: int) -> tuple[tuple[int, ...], ...]:
    """Choose three pure and three two-odd right words."""
    pure_words = tuple((colour,) * (2 * m - 2) for colour in range(3))
    pair_words = []
    for first, second in combinations(range(3), 2):
        third = next(
            colour
            for colour in range(3)
            if colour not in {first, second}
        )
        pair_words.append(
            (first, second) + (third,) * max(0, 2 * m - 4)
        )
    return pure_words + tuple(pair_words)


def audit_flattening_certificate() -> dict[int, tuple[int, int]]:
    """Use only direct matchings to audit the Wick/GHZ rank mismatch."""
    ledger: dict[int, tuple[int, int]] = {}
    left_words = tuple(product(range(3), repeat=2))
    for m in range(2, 6):
        right_words = certificate_words(m)
        wick_rows = [
            [coordinate_coefficient(left + right) for right in right_words]
            for left in left_words
        ]
        ghz_rows = [
            [int(len(set(left + right)) == 1) for right in right_words]
            for left in left_words
        ]
        wick_rank = rational_rank(wick_rows)
        ghz_rank = rational_rank(ghz_rows)
        assert wick_rank == 6
        assert ghz_rank == 3
        for row_index, left in enumerate(left_words):
            reverse_index = left_words.index(tuple(reversed(left)))
            assert wick_rows[row_index] == wick_rows[reverse_index]
        ledger[m] = (wick_rank, ghz_rank)
    return ledger


def direct_companion_tensor(
    m: int,
    subset: tuple[int, ...],
    contraction_vectors: tuple[tuple[int, int, int], ...],
) -> dict[tuple[int, ...], int]:
    """Enumerate one uniform-form companion without using its closed formula."""
    roots = tuple(range(m))
    entries: dict[tuple[int, ...], int] = {}
    for crossing_roots in combinations(roots, len(subset)):
        crossing_set = set(crossing_roots)
        for target_order in permutations(subset):
            assignment = tuple(zip(crossing_roots, target_order, strict=True))
            residual_roots = tuple(
                root for root in roots if root not in crossing_set
            )
            for root_matching in matchings(residual_roots):
                edge_slots = len(assignment) + len(root_matching)
                for edge_colours in product(range(3), repeat=edge_slots):
                    word = [-1] * m
                    weight = 1
                    for position, (root, target) in enumerate(assignment):
                        colour = edge_colours[position]
                        word[root] = colour
                        weight *= contraction_vectors[target][colour]
                    offset = len(assignment)
                    for position, (left, right) in enumerate(root_matching):
                        colour = edge_colours[offset + position]
                        word[left] = colour
                        word[right] = colour
                    key = tuple(word)
                    entries[key] = entries.get(key, 0) + weight
    return entries


def diagonal_polynomial(
    tensor: dict[tuple[int, ...], int],
) -> dict[tuple[int, int, int], int]:
    """Collapse a root tensor to sparse repeated-root monomial coordinates."""
    polynomial: dict[tuple[int, int, int], int] = {}
    for word, coefficient in tensor.items():
        exponent = tuple(word.count(colour) for colour in range(3))
        polynomial[exponent] = polynomial.get(exponent, 0) + coefficient
    return {key: value for key, value in polynomial.items() if value != 0}


def audit_sensor_ranks() -> dict[int, tuple[int, int, int]]:
    """Build companion tensors directly and audit the all-cut rank bound."""
    ledger: dict[int, tuple[int, int, int]] = {}
    for m in range(3, 6):
        contraction_vectors = tuple(
            (1, value, value * value) for value in range(1, m + 1)
        )
        subsets = tuple(
            subset
            for size in range(m + 1)
            if size % 2 == m % 2
            for subset in combinations(range(m), size)
        )
        polynomials = [
            diagonal_polynomial(
                direct_companion_tensor(m, subset, contraction_vectors)
            )
            for subset in subsets
        ]
        monomials = tuple(
            (first, second, m - first - second)
            for first in range(m + 1)
            for second in range(m - first + 1)
        )
        rows = [
            [polynomial.get(monomial, 0) for polynomial in polynomials]
            for monomial in monomials
        ]
        rank = rational_rank(rows)
        columns = len(subsets)
        bound = m * (m - 1) // 2 + 1
        assert columns == 2 ** (m - 1)
        assert rank == min(columns, bound)
        if m >= 4:
            assert rank < columns
        ledger[m] = (columns, rank, bound)
    return ledger


def audit_local_rank() -> dict[int, int]:
    """Directly audit one-slot ranks for diagonal forms of each rank."""
    rest_words = tuple(product(range(3), repeat=3))
    ledger: dict[int, int] = {}
    for form_rank in range(4):
        rows = []
        for first_colour in range(3):
            row = []
            for rest in rest_words:
                word = (first_colour,) + rest
                total = 0
                for matching in matchings((0, 1, 2, 3)):
                    valid = True
                    for left, right in matching:
                        if not (
                            word[left] == word[right]
                            and word[left] < form_rank
                        ):
                            valid = False
                            break
                    if valid:
                        total += 1
                row.append(total)
            rows.append(row)
        rank = rational_rank(rows)
        assert rank == form_rank
        ledger[form_rank] = rank
    return ledger


def main() -> None:
    flattenings = audit_flattening_certificate()
    sensors = audit_sensor_ranks()
    local = audit_local_rank()
    print("balanced common-quadratic independent audit: PASS")
    print(f"  direct (Wick, GHZ) flattening ranks: {flattenings}")
    print(f"  direct (columns, rank, bound) sensor ranks: {sensors}")
    print(f"  direct degenerate local ranks: {local}")


if __name__ == "__main__":
    main()
