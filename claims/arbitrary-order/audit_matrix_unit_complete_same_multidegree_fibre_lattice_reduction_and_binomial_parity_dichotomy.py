"""No-import audit of complete-block fibre-lattice descent."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Exponent = tuple[int, ...]


# Decimal data copied from the theorem's fixed U7D regression table.  This
# audit intentionally imports no repository module and shares no enumerator
# with the primary verifier.
TABLE: dict[Edge, tuple[int, int, int]] = {
    (0, 1): (0, 0, 1),
    (0, 2): (0, 0, 1),
    (0, 3): (0, 0, 1),
    (0, 4): (0, 0, 1),
    (0, 5): (1, 2, 1),
    (0, 6): (1, 1, 1),
    (0, 7): (2, 2, 1),
    (1, 2): (0, 1, -1),
    (1, 3): (0, 0, 1),
    (1, 4): (1, 0, -1),
    (1, 5): (1, 1, 1),
    (1, 6): (2, 2, 1),
    (1, 7): (0, 0, 1),
    (2, 3): (1, 1, 1),
    (2, 4): (0, 1, -1),
    (2, 5): (2, 2, 1),
    (2, 6): (0, 0, 1),
    (2, 7): (2, 0, 1),
    (3, 4): (2, 2, 1),
    (3, 5): (0, 1, 1),
    (3, 6): (1, 0, 1),
    (3, 7): (1, 1, 1),
    (4, 5): (0, 0, 1),
    (4, 6): (1, 1, 1),
    (4, 7): (1, 1, 1),
    (5, 6): (0, 1, 1),
    (5, 7): (1, 1, 1),
    (6, 7): (1, 1, 1),
}

EDGES = tuple(combinations(range(8), 2))
POSITIONS = {edge: index for index, edge in enumerate(EDGES)}


def balanced_words() -> tuple[Word, ...]:
    records = []
    for positions in combinations(range(8), 4):
        word = [1] * 8
        for position in positions:
            word[position] = 0
        records.append(tuple(word))
    return tuple(records)


def target_fibre(word: Word) -> tuple[Matching, ...]:
    """Enumerate one fibre by target-constrained least-vertex recursion."""
    output: list[Matching] = []

    def recurse(remaining: tuple[int, ...], prefix: Matching) -> None:
        if not remaining:
            output.append(prefix)
            return
        left = remaining[0]
        for index in range(1, len(remaining)):
            right = remaining[index]
            edge = (left, right)
            left_label, right_label, _ = TABLE[edge]
            if left_label != word[left] or right_label != word[right]:
                continue
            residue = remaining[1:index] + remaining[index + 1 :]
            recurse(residue, prefix + (edge,))

    recurse(tuple(range(8)), ())
    return tuple(output)


def incidence(matching: Matching) -> Exponent:
    vector = [0] * len(EDGES)
    for edge in matching:
        vector[POSITIONS[edge]] = 1
    return tuple(vector)


def subtract(left: Exponent, right: Exponent) -> Exponent:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def add(*vectors: Exponent) -> Exponent:
    return tuple(sum(values) for values in zip(*vectors, strict=True))


def evaluate(exponent: Exponent, values: tuple[Fraction, ...]) -> Fraction:
    result = Fraction(1)
    for value, power in zip(values, exponent, strict=True):
        result *= value**power
    return result


def matching_weight(matching: Matching) -> int:
    result = 1
    for edge in matching:
        result *= TABLE[edge][2]
    return result


def diagonal_matching(matching: Matching) -> bool:
    return all(TABLE[edge][0] == TABLE[edge][1] for edge in matching)


def audit_word_first_normalization() -> tuple[dict[str, object], dict[Word, tuple[Matching, ...]]]:
    """Rebuild all 70 fibres and audit C=lambda_ref f independently."""
    fibres = {word: target_fibre(word) for word in balanced_words()}
    histogram = Counter(len(fibre) for fibre in fibres.values())
    assert histogram == Counter({0: 57, 1: 10, 2: 3})

    assignments = (
        tuple(Fraction(2 * index + 3, index + 2) for index in range(len(EDGES))),
        tuple(
            Fraction((-1 if index % 4 == 0 else 1) * (index + 5), index + 3)
            for index in range(len(EDGES))
        ),
    )
    checked = 0
    normalized_terms = 0
    for fibre in fibres.values():
        if not fibre:
            continue
        reference = incidence(fibre[-1])
        normalized = tuple(subtract(incidence(matching), reference) for matching in fibre)
        assert normalized[-1] == (0,) * len(EDGES)
        normalized_terms += len(normalized)
        for values in assignments:
            original = sum((evaluate(incidence(matching), values) for matching in fibre), Fraction(0))
            reduced = evaluate(reference, values) * sum(
                (evaluate(exponent, values) for exponent in normalized), Fraction(0)
            )
            assert original == reduced
            checked += 1

    second_singleton = (1, 0, 1, 1, 0, 0, 1, 0)
    assert target_fibre(second_singleton) == (((0, 6), (1, 7), (2, 3), (4, 5)),)
    return (
        {
            "word_first_recursions": len(fibres),
            "histogram": dict(sorted(histogram.items())),
            "normalized_terms": normalized_terms,
            "exact_factorizations_checked": checked,
            "independent_singleton": second_singleton,
            "singleton_normalized_polynomial": "1",
        },
        fibres,
    )


def matrix_rank(rows: tuple[tuple[int, ...], ...]) -> int:
    """Compute rational row rank by an audit-local Fraction elimination."""
    if not rows:
        return 0
    matrix = [list(map(Fraction, row)) for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Compute an exact determinant by Fraction elimination."""
    if not matrix:
        return 1
    work = [list(map(Fraction, row)) for row in matrix]
    value = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        scale = work[column][column]
        value *= scale
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            multiple = work[row][column] / scale
            for index in range(column, len(work)):
                work[row][index] -= multiple * work[column][index]
    assert value.denominator == 1
    return value.numerator


def combine(coefficients: tuple[int, ...], rows: tuple[Exponent, ...]) -> Exponent:
    return tuple(
        sum(coefficient * row[column] for coefficient, row in zip(coefficients, rows, strict=True))
        for column in range(len(rows[0]))
    )


def certify_kernel(
    rows: tuple[Exponent, ...],
    kernel_columns: tuple[tuple[int, ...], ...],
    complement_columns: tuple[tuple[int, ...], ...],
) -> bool:
    """Certify a full integer kernel through a unimodular domain basis."""
    generator_count = len(rows)
    columns = kernel_columns + complement_columns
    assert len(columns) == generator_count
    assert all(len(column) == generator_count for column in columns)
    domain_basis = tuple(
        tuple(column[row] for column in columns)
        for row in range(generator_count)
    )
    assert abs(determinant(domain_basis)) == 1
    zero = (0,) * len(rows[0])
    assert all(combine(column, rows) == zero for column in kernel_columns)
    complement_images = tuple(combine(column, rows) for column in complement_columns)
    assert matrix_rank(complement_images) == len(complement_columns)
    return any(sum(column) % 2 for column in kernel_columns)


def audit_binomial_parity_certificates() -> dict[str, int]:
    """Use independent unimodular certificates for the exact parity split."""
    cases = (
        (
            ((1, 0), (0, 1), (1, 1)),
            ((1, 1, -1),),
            ((0, 1, 0), (0, 0, 1)),
            True,
        ),
        (
            ((2,), (4,)),
            ((2, -1),),
            ((1, 0),),
            True,
        ),
        (
            ((2, 0), (2, 0), (0, 2)),
            ((1, -1, 0),),
            ((0, 1, 0), (0, 0, 1)),
            False,
        ),
        (
            ((2,), (-2,)),
            ((1, 1),),
            ((0, 1),),
            False,
        ),
    )
    odd = 0
    consistent = 0
    for raw_rows, kernel, complement, expected_odd in cases:
        rows = tuple(tuple(row) for row in raw_rows)
        result = certify_kernel(rows, kernel, complement)
        assert result is expected_odd
        odd += result
        consistent += not result
    return {
        "unimodular_kernel_certificates": len(cases),
        "odd_dependency_unit_cases": odd,
        "parity_consistent_cases": consistent,
    }


def audit_cycle_character(fibres: dict[Word, tuple[Matching, ...]]) -> dict[str, object]:
    """Recover the three binomial rows and their endpoint-character kernel."""
    cycle_words = tuple(word for word, fibre in fibres.items() if len(fibre) == 2)
    assert len(cycle_words) == 3
    rows = []
    specialized = Fraction(1)
    for word in sorted(cycle_words):
        fibre = fibres[word]
        diagonal = next(matching for matching in fibre if diagonal_matching(matching))
        cross = next(matching for matching in fibre if not diagonal_matching(matching))
        rows.append(subtract(incidence(diagonal), incidence(cross)))
        specialized *= Fraction(matching_weight(diagonal), matching_weight(cross))
    relation_rows = tuple(rows)

    identity = tuple(
        tuple(1 if row == column else 0 for row in range(3))
        for column in range(3)
    )
    assert not certify_kernel(relation_rows, (), identity)
    holonomy = add(*relation_rows)

    endpoint_character: Counter[tuple[int, int]] = Counter()
    for edge, exponent in zip(EDGES, holonomy, strict=True):
        if not exponent:
            continue
        left, right = edge
        left_label, right_label, _ = TABLE[edge]
        endpoint_character[(left, left_label)] += exponent
        endpoint_character[(right, right_label)] += exponent
    assert not +endpoint_character
    assert specialized == -1
    return {
        "cycle_relation_rank": matrix_rank(relation_rows),
        "integer_kernel_dimension": 0,
        "endpoint_character_zero": True,
        "transported_sign": -1,
        "specialized_holonomy": specialized,
        "proper_binomial_elimination": "(H+1)",
    }


def audit_skew_nonsaturated_cosets() -> dict[str, int]:
    """Decompose a box modulo <(2,0),(1,3)> by a different route."""
    residues: Counter[tuple[int, int]] = Counter()
    checked = 0
    for exponent in product(range(-6, 7), repeat=2):
        q, second_residue = divmod(exponent[1], 3)
        adjusted_first = exponent[0] - q
        p, first_residue = divmod(adjusted_first, 2)
        lattice_part = (2 * p + q, 3 * q)
        representative = (first_residue, second_residue)
        assert tuple(a + b for a, b in zip(lattice_part, representative, strict=True)) == exponent
        residues[representative] += 1
        checked += 1
    assert set(residues) == set(product(range(2), range(3)))
    return {"exponents_decomposed": checked, "skew_cosets": len(residues)}


def main() -> None:
    block, fibres = audit_word_first_normalization()
    parity = audit_binomial_parity_certificates()
    cycle = audit_cycle_character(fibres)
    cosets = audit_skew_nonsaturated_cosets()
    print("independent complete same-multidegree fibre-lattice audit: PASS")
    print(f"  word-first normalized block: {block}")
    print(f"  unimodular parity certificates: {parity}")
    print(f"  independently reconstructed cycle: {cycle}")
    print(f"  skew nonsaturated coset basis: {cosets}")


if __name__ == "__main__":
    main()
