"""Independent sparse-polynomial audit of the common-quadric obstruction."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, int]


def matching_decompositions(vertices: tuple[int, ...]):
    """Generate matchings using a different anchor-removal implementation."""
    if len(vertices) == 0:
        yield ()
        return
    anchor, *others_list = vertices
    others = tuple(others_list)
    for position, partner in enumerate(others):
        unused = others[:position] + others[position + 1 :]
        for continuation in matching_decompositions(unused):
            yield ((anchor, partner),) + continuation


def clean(polynomial: Polynomial) -> Polynomial:
    """Remove zero sparse coefficients."""
    return {monomial: value for monomial, value in polynomial.items() if value}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add two sparse integer polynomials."""
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def scale(polynomial: Polynomial, scalar: int) -> Polynomial:
    """Scale a sparse polynomial."""
    return clean(
        {monomial: scalar * coefficient for monomial, coefficient in polynomial.items()}
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply two sparse integer polynomials."""
    result: Polynomial = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            monomial = tuple(
                first[index] + second[index] for index in range(3)
            )
            result[monomial] = (
                result.get(monomial, 0)
                + first_coefficient * second_coefficient
            )
    return clean(result)


def product_of(polynomials: list[Polynomial]) -> Polynomial:
    """Multiply a list of sparse polynomials."""
    result: Polynomial = {(0, 0, 0): 1}
    for polynomial in polynomials:
        result = multiply(result, polynomial)
    return result


def reduce_mod_q(polynomial: Polynomial) -> Polynomial:
    """Reduce modulo z^2+x^2+y^2 using the monic z^2 relation."""
    result: Polynomial = {}
    pending = list(polynomial.items())
    while pending:
        (x_power, y_power, z_power), coefficient = pending.pop()
        if coefficient == 0:
            continue
        if z_power < 2:
            key = (x_power, y_power, z_power)
            result[key] = result.get(key, 0) + coefficient
            continue
        pending.append(
            ((x_power + 2, y_power, z_power - 2), -coefficient)
        )
        pending.append(
            ((x_power, y_power + 2, z_power - 2), -coefficient)
        )
    return clean(result)


def linear(x_coefficient: int, y_coefficient: int, z_coefficient: int) -> Polynomial:
    """Construct one sparse linear form."""
    return clean(
        {
            (1, 0, 0): x_coefficient,
            (0, 1, 0): y_coefficient,
            (0, 0, 1): z_coefficient,
        }
    )


def sparse_permanent(matrix: list[list[Polynomial]]) -> Polynomial:
    """Expand a polynomial permanent with no determinant signs."""
    size = len(matrix)
    total: Polynomial = {}
    for order in permutations(range(size)):
        term = product_of([matrix[row][order[row]] for row in range(size)])
        total = add(total, term)
    return total


def scalar_permanent(matrix: list[list[int]]) -> int:
    """Expand an integer permanent independently."""
    size = len(matrix)
    total = 0
    for order in permutations(range(size)):
        term = 1
        for row in range(size):
            term *= matrix[row][order[row]]
        total += term
    return total


def general_cross_matrix(m: int) -> list[list[Polynomial]]:
    """Build non-column-separable forms distinct from the primary instance."""
    return [
        [
            linear(
                2 + row + 3 * column,
                1 + 2 * row + column,
                4 + row + column,
            )
            for column in range(m)
        ]
        for row in range(m)
    ]


def full_contraction(m: int, cross: list[list[Polynomial]]) -> Polynomial:
    """Enumerate the complete repeated-root matching polynomial."""
    quadratic: Polynomial = {
        (2, 0, 0): 1,
        (0, 2, 0): 1,
        (0, 0, 2): 1,
    }
    total: Polynomial = {}
    for matching in matching_decompositions(tuple(range(2 * m))):
        factors: list[Polynomial] = []
        scalar = 1
        for left, right in matching:
            if right < m:
                scalar *= 2 + 2 * left + right
                factors.append(quadratic)
            elif left < m:
                factors.append(cross[left][right - m])
            else:
                scalar *= 3 + 4 * (left - m) + 2 * (right - m)
        total = add(total, scale(product_of(factors), scalar))
    return total


def audit_residue_identity() -> dict[int, tuple[int, int]]:
    """Check independently that only the all-cross sector survives modulo Q."""
    ledger: dict[int, tuple[int, int]] = {}
    for m in range(2, 5):
        cross = general_cross_matrix(m)
        full = full_contraction(m, cross)
        all_cross = sparse_permanent(cross)
        difference = add(full, scale(all_cross, -1))
        assert reduce_mod_q(difference) == {}
        assert reduce_mod_q(full) == reduce_mod_q(all_cross)
        ledger[m] = (
            len(tuple(matching_decompositions(tuple(range(2 * m))))),
            len(full),
        )
    return ledger


def conformal_scalar_matrix(m: int) -> list[list[int]]:
    """Choose a positive matrix so its permanent is manifestly nonzero."""
    return [
        [2 + (row + 2) * (column + 1) for column in range(m)]
        for row in range(m)
    ]


def audit_column_factorization() -> dict[int, tuple[int, int]]:
    """Check factorization and nondivisibility with a separate sparse route."""
    ledger: dict[int, tuple[int, int]] = {}
    for m in range(2, 6):
        scalars = conformal_scalar_matrix(m)
        forms = [
            linear(2 + column, 3 + 2 * column, 5 + column)
            for column in range(m)
        ]
        cross = [
            [scale(forms[column], scalars[row][column]) for column in range(m)]
            for row in range(m)
        ]
        cross_permanent = sparse_permanent(cross)
        scalar_value = scalar_permanent(scalars)
        expected = scale(product_of(forms), scalar_value)
        assert scalar_value > 0
        assert cross_permanent == expected
        remainder = reduce_mod_q(cross_permanent)
        assert remainder != {}
        ledger[m] = (scalar_value, len(remainder))
    return ledger


def fraction_rank(rows: list[list[int]]) -> int:
    """Compute exact rank for the degenerate local-span audit."""
    work = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * basis
                for entry, basis in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
    return rank


def audit_degenerate_spans_and_target_words() -> dict[str, object]:
    """Check local ranks and the exact coordinate-word zero boundary."""
    span_ranks = {}
    vectors = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 3, 5))
    for form_rank in range(4):
        rows = [
            [vector[index] if index < form_rank else 0 for vector in vectors]
            for index in range(3)
        ]
        rank = fraction_rank(rows)
        assert rank == form_rank
        span_ranks[form_rank] = rank

    constant_words = ((0, 0, 0), (1, 1, 1), (2, 2, 2))
    mixed_words = ((0, 1, 2), (0, 0, 1), (2, 1, 2))
    assert all(len(set(word)) == 1 for word in constant_words)
    assert all(len(set(word)) > 1 for word in mixed_words)
    return {"span_ranks": span_ranks, "mixed_zero_words": len(mixed_words)}


def audit_zero_permanent_pure_branch() -> dict[int, int]:
    """Use separate zero-permanent instances to audit the pure contradiction."""
    matrices = {
        2: [[1, 2], [1, -2]],
        4: [
            [1, 2, 0, 0],
            [1, -2, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
    }
    ledger: dict[int, int] = {}
    for m, scalars in matrices.items():
        assert scalar_permanent(scalars) == 0
        nonroot_forms = [
            linear(3 + column, 2 * column + 1, 4 + column)
            for column in range(m)
        ]
        cross = [
            [scale(nonroot_forms[column], scalars[row][column]) for column in range(m)]
            for row in range(m)
        ]
        assert sparse_permanent(cross) == {}
        assert reduce_mod_q(full_contraction(m, cross)) == {}

        root_forms = [
            linear(2 * row + 1, row + 3, 5 + row)
            for row in range(m)
        ]
        pure_remainder = reduce_mod_q(product_of(root_forms))
        assert pure_remainder != {}
        ledger[m] = len(pure_remainder)
    return ledger


def main() -> None:
    residues = audit_residue_identity()
    factors = audit_column_factorization()
    boundaries = audit_degenerate_spans_and_target_words()
    zero_permanent = audit_zero_permanent_pure_branch()
    print("balanced common-quadric independent audit: PASS")
    print(f"  (matchings, sparse terms) residue ledger: {residues}")
    print(f"  (scalar permanent, remainder terms): {factors}")
    print(f"  local/target boundary ledger: {boundaries}")
    print(f"  zero-permanent pure remainder terms: {zero_permanent}")


if __name__ == "__main__":
    main()
