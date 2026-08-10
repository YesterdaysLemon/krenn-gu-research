"""Independent no-import audit for the characteristic-two route boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


def pairing_terms(vertices: frozenset[int]):
    if not vertices:
        yield ()
        return
    first = min(vertices)
    for partner in sorted(vertices - {first}):
        remainder = vertices - {first, partner}
        for tail in pairing_terms(remainder):
            yield ((first, partner), *tail)


def audit_delta2_example() -> None:
    entries = {
        (0, 1, 0, 0): Fraction(1),
        (2, 3, 0, 0): Fraction(1, 2),
        (0, 2, 0, 0): Fraction(1),
        (1, 3, 0, 0): Fraction(1, 2),
        (0, 3, 1, 1): Fraction(1),
        (1, 2, 1, 1): Fraction(1),
    }
    for word in product((0, 1), repeat=4):
        total = Fraction(0)
        for pairing in pairing_terms(frozenset(range(4))):
            value = Fraction(1)
            for i, j in pairing:
                value *= entries.get((i, j, word[i], word[j]), Fraction(0))
            total += value
        assert total == (1 if word.count(word[0]) == 4 else 0)


def gf4_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    a, b = left
    c, d = right
    # (a+b*x)(c+d*x), x^2=x+1, coefficients modulo two.
    return ((a * c + b * d) % 2, (a * d + b * c + b * d) % 2)


def audit_residue_extension_example() -> None:
    zero, one = (0, 0), (1, 0)
    alpha, alpha2 = (0, 1), (1, 1)
    edge_weight = {
        (0, 1): alpha,
        (2, 3): one,
        (4, 5): one,
        (0, 2): alpha2,
        (1, 3): one,
    }
    total = zero
    nonzero_terms = []
    for pairing in pairing_terms(frozenset(range(6))):
        value = one
        for item in pairing:
            value = gf4_multiply(value, edge_weight.get(item, zero))
        total = ((total[0] + value[0]) % 2, (total[1] + value[1]) % 2)
        if value != zero:
            nonzero_terms.append((pairing, value))
    assert total == one
    assert [value for _, value in nonzero_terms] == [alpha, alpha2]
    assert all(
        any(edge_weight.get(item, zero) != one for item in pairing)
        for pairing, _ in nonzero_terms
    )


def matrix_rank_mod_p(matrix: tuple[tuple[int, ...], ...], prime: int) -> int:
    rows = [list(row) for row in matrix]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column] % prime), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column] % prime, -1, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for r in range(len(rows)):
            if r == rank:
                continue
            factor = rows[r][column] % prime
            if factor:
                rows[r] = [
                    (rows[r][c] - factor * rows[rank][c]) % prime
                    for c in range(columns)
                ]
        rank += 1
    return rank


def h_on_basis(matrix: tuple[tuple[int, ...], ...], i: int, j: int, k: int, l: int, p: int) -> int:
    return (
        matrix[i][j] * matrix[k][l]
        + matrix[i][k] * matrix[j][l]
        + matrix[i][l] * matrix[j][k]
    ) % p


def symmetric_matrices(size: int, prime: int):
    positions = tuple(combinations(range(size), 2)) + tuple((i, i) for i in range(size))
    for values in product(range(prime), repeat=len(positions)):
        rows = [[0] * size for _ in range(size)]
        for (i, j), value in zip(positions, values, strict=True):
            rows[i][j] = rows[j][i] = value
        yield tuple(tuple(row) for row in rows)


def audit_small_field_classification() -> None:
    # These are bounded sanity tables for the arbitrary-field proof.
    for prime, size in ((2, 4), (3, 3), (5, 2)):
        for matrix in symmetric_matrices(size, prime):
            vanishes = all(
                h_on_basis(matrix, i, j, k, l, prime) == 0
                for i, j, k, l in product(range(size), repeat=4)
            )
            rank = matrix_rank_mod_p(matrix, prime)
            if prime == 2:
                alternating = all(matrix[i][i] == 0 for i in range(size))
                expected = alternating and rank <= 2
            elif prime == 3:
                expected = rank <= 1
            else:
                expected = rank == 0
            assert vanishes == expected


def audit_matching_gauge_invariance() -> None:
    # Exponent bookkeeping: every perfect matching uses each vertex once.
    for order in (4, 6, 8):
        for pairing in pairing_terms(frozenset(range(order))):
            incidence = [0] * order
            for i, j in pairing:
                incidence[i] += 1
                incidence[j] += 1
            assert incidence == [1] * order


def main() -> None:
    audit_delta2_example()
    audit_residue_extension_example()
    audit_small_field_classification()
    audit_matching_gauge_invariance()
    print("independent characteristic-two lift-obstruction audit: PASS")
    print("small field tables: F2 dim4, F3 dim3, F5 dim2")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
