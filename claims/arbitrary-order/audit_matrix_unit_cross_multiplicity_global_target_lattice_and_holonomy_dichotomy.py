"""Independent no-import audit of the global cross-multiplicity lattice."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Vector = tuple[int, ...]
Polynomial = tuple[Fraction, ...]

# Decimal endpoint-label codes in lexicographic physical-edge order.  This is
# an independent encoding of the U7D label support and carries no amplitudes.
LABEL_CODES = (
    0,
    0,
    0,
    0,
    12,
    11,
    22,
    1,
    0,
    10,
    11,
    22,
    0,
    11,
    1,
    22,
    0,
    20,
    22,
    1,
    10,
    11,
    0,
    11,
    11,
    1,
    11,
    11,
)

EDGES = tuple(combinations(range(8), 2))
EDGE_BIT = {edge: 1 << index for index, edge in enumerate(EDGES)}
LABELS = {edge: divmod(code, 10) for edge, code in zip(EDGES, LABEL_CODES, strict=True)}


def pack_word(word: tuple[int, ...]) -> int:
    """Pack a ternary word with vertex zero least significant."""
    return sum(colour * 3**vertex for vertex, colour in enumerate(word))


def unpack_word(code: int) -> tuple[int, ...]:
    """Unpack one eight-vertex ternary word."""
    result = []
    for _ in range(8):
        code, colour = divmod(code, 3)
        result.append(colour)
    return tuple(result)


def enumerate_fibres() -> dict[int, tuple[int, ...]]:
    """Traverse perfect matchings by least-vertex deletion."""
    fibres: dict[int, list[int]] = defaultdict(list)

    def visit(vertices: int, word: list[int], matching: int) -> None:
        if not vertices:
            fibres[pack_word(tuple(word))].append(matching)
            return
        left_bit = vertices & -vertices
        left = left_bit.bit_length() - 1
        remainder = vertices ^ left_bit
        partners = remainder
        while partners:
            right_bit = partners & -partners
            right = right_bit.bit_length() - 1
            partners ^= right_bit
            edge = (left, right)
            left_colour, right_colour = LABELS[edge]
            next_word = word[:]
            next_word[left] = left_colour
            next_word[right] = right_colour
            visit(
                remainder ^ right_bit,
                next_word,
                matching | EDGE_BIT[edge],
            )

    visit((1 << 8) - 1, [-1] * 8, 0)
    return {word: tuple(records) for word, records in fibres.items()}


def bit_vector(bits: int) -> Vector:
    """Expand a matching bitset in the physical edge basis."""
    return tuple(1 if bits & (1 << index) else 0 for index in range(len(EDGES)))


def difference(left: int, right: int) -> Vector:
    """Return the signed incidence difference left minus right."""
    return tuple(
        a - b for a, b in zip(bit_vector(left), bit_vector(right), strict=True)
    )


def endpoint_character(vector: Vector) -> Vector:
    """Apply the independently encoded endpoint-colour character map."""
    result = [0] * 24
    for edge, coefficient in zip(EDGES, vector, strict=True):
        if not coefficient:
            continue
        left, right = edge
        left_colour, right_colour = LABELS[edge]
        result[3 * left + left_colour] += coefficient
        result[3 * right + right_colour] += coefficient
    return tuple(result)


def rational_rank(rows: list[Vector]) -> int:
    """Compute exact row rank by independent Fraction elimination."""
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def audit_endpoint_kernel_and_separation() -> dict[str, object]:
    """Reconstruct both multidegrees and their direct-sum lattice test."""
    fibres = enumerate_fibres()
    assert sum(map(len, fibres.values())) == 105
    assert len(fibres) == 101

    rows_by_word: dict[int, list[Vector]] = {}
    for word, records in fibres.items():
        if len(records) > 1:
            rows_by_word[word] = [difference(record, records[0]) for record in records[1:]]

    cycle_words = (
        (0, 0, 0, 0, 1, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 0, 1),
    )
    neighbour = (0, 2, 0, 0, 1, 1, 2, 1)
    cycle_codes = {pack_word(word) for word in cycle_words}
    neighbour_code = pack_word(neighbour)
    assert set(rows_by_word) == cycle_codes | {neighbour_code}

    cycle_rows = [rows_by_word[pack_word(word)][0] for word in cycle_words]
    neighbour_rows = rows_by_word[neighbour_code]
    all_rows = cycle_rows + neighbour_rows
    assert all(not any(endpoint_character(row)) for row in all_rows)
    assert tuple(neighbour.count(colour) for colour in range(3)) == (3, 3, 2)
    assert {
        tuple(unpack_word(code).count(colour) for colour in range(3))
        for code in cycle_codes
    } == {(4, 4, 0)}

    cycle_rank = rational_rank(cycle_rows)
    neighbour_rank = rational_rank(neighbour_rows)
    combined_rank = rational_rank(all_rows)
    intersection_rank = cycle_rank + neighbour_rank - combined_rank
    assert (cycle_rank, neighbour_rank, combined_rank, intersection_rank) == (3, 1, 4, 0)

    cycle_support = {
        index for row in cycle_rows for index, coefficient in enumerate(row) if coefficient
    }
    neighbour_support = {
        index
        for row in neighbour_rows
        for index, coefficient in enumerate(row)
        if coefficient
    }
    shared_edges = {EDGES[index] for index in cycle_support & neighbour_support}
    assert shared_edges == {(0, 2), (2, 4), (3, 5), (5, 7)}

    pure_rows = []
    for colour in range(3):
        records = fibres[pack_word((colour,) * 8)]
        assert len(records) == 1
        pure_rows.append(bit_vector(records[0]))
    assert rational_rank(all_rows + pure_rows) == 7

    return {
        "fibres": len(fibres),
        "cross_degree_rows": len(all_rows),
        "cycle_rank": cycle_rank,
        "neighbour_rank": neighbour_rank,
        "intersection_rank": intersection_rank,
        "shared_edges": tuple(sorted(shared_edges)),
        "rank_after_pure_anchors": 7,
    }


def evaluate_character(
    polynomial: dict[tuple[int, ...], Fraction], values: tuple[Fraction, ...]
) -> Fraction:
    """Evaluate a small Laurent polynomial at a nonzero rational character."""
    result = Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for power, value in zip(exponent, values, strict=True):
            term *= value**power
        result += term
    return result


def add_scaled(
    target: dict[tuple[int, ...], Fraction],
    source: dict[tuple[int, ...], Fraction],
    scale: Fraction,
) -> None:
    """Add a scaled sparse polynomial in place."""
    for exponent, coefficient in source.items():
        target[exponent] = target.get(exponent, Fraction(0)) + scale * coefficient
        if not target[exponent]:
            del target[exponent]


def audit_holonomy_and_unit_alternatives() -> dict[str, object]:
    """Use separate character and explicit-unit derivations."""
    zero = (0, 0, 0, 0)
    x_exp = (1, 0, 0, 0)
    y_exp = (0, 1, 0, 0)
    z_exp = (0, 0, 1, 0)
    w_exp = (0, 0, 0, 1)
    one_plus_x = {zero: Fraction(1), x_exp: Fraction(1)}
    one_plus_y = {zero: Fraction(1), y_exp: Fraction(1)}
    one_plus_z = {zero: Fraction(1), z_exp: Fraction(1)}
    x_minus_y = {x_exp: Fraction(1), y_exp: Fraction(-1)}
    one_plus_w = {zero: Fraction(1), w_exp: Fraction(1)}

    proper_character = (Fraction(-1),) * 4
    for polynomial in (
        one_plus_x,
        one_plus_y,
        one_plus_z,
        x_minus_y,
        one_plus_w,
    ):
        assert evaluate_character(polynomial, proper_character) == 0
    assert proper_character[0] * proper_character[1] * proper_character[2] == -1

    # The residual 1+x+y makes the same core a unit, with a literal ideal
    # certificate (1+x)+(1+y)-(1+x+y)=1.
    one_plus_x_plus_y = {
        zero: Fraction(1),
        x_exp: Fraction(1),
        y_exp: Fraction(1),
    }
    certificate: dict[tuple[int, ...], Fraction] = {}
    add_scaled(certificate, one_plus_x, Fraction(1))
    add_scaled(certificate, one_plus_y, Fraction(1))
    add_scaled(certificate, one_plus_x_plus_y, Fraction(-1))
    assert certificate == {zero: Fraction(1)}

    # Curated H-polynomials vanish at H=-1 exactly when divisible by H+1.
    samples: tuple[Polynomial, ...] = (
        (Fraction(1), Fraction(1)),
        (Fraction(-1), Fraction(0), Fraction(1)),
        (Fraction(2), Fraction(3), Fraction(1)),
    )
    assert all(
        sum(coefficient * Fraction(-1) ** degree for degree, coefficient in enumerate(poly))
        == 0
        for poly in samples
    )

    return {
        "proper_character": "x=y=z=w=-1",
        "proper_holonomy": -1,
        "unit_certificate": "(1+x)+(1+y)-(1+x+y)=1",
        "H_plus_one_divisibility_samples": len(samples),
    }


def trim(polynomial: Polynomial) -> Polynomial:
    """Remove high zero coefficients."""
    result = list(polynomial)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def polynomial_divmod(dividend: Polynomial, divisor: Polynomial) -> tuple[Polynomial, Polynomial]:
    """Exact univariate division over the rationals."""
    remainder = list(trim(dividend))
    divisor = trim(divisor)
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and any(remainder):
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + degree] -= coefficient * value
        remainder = list(trim(tuple(remainder)))
    return trim(tuple(quotient)), trim(tuple(remainder))


def monic_gcd(left: Polynomial, right: Polynomial) -> Polynomial:
    """Independent Euclidean gcd over Q."""
    left, right = trim(left), trim(right)
    while any(right):
        _, remainder = polynomial_divmod(left, right)
        left, right = right, remainder
    scale = left[-1]
    return trim(tuple(coefficient / scale for coefficient in left))


def audit_rank_one_residuals() -> dict[str, str]:
    """Audit proper and unit quotient sheets without symbolic algebra."""
    t_minus_one = (Fraction(-1), Fraction(1))
    t_plus_one = (Fraction(1), Fraction(1))
    t_squared_minus_one = (Fraction(-1), Fraction(0), Fraction(1))
    proper = monic_gcd(t_squared_minus_one, t_minus_one)
    unit = monic_gcd(t_minus_one, t_plus_one)
    assert proper == t_minus_one
    assert unit == (Fraction(1),)
    return {"proper_gcd": "t-1", "unit_gcd": "1"}


def main() -> None:
    """Run the independent exact audit."""
    lattice = audit_endpoint_kernel_and_separation()
    holonomy = audit_holonomy_and_unit_alternatives()
    rank_one = audit_rank_one_residuals()
    print("cross-multiplicity global target-lattice no-import audit: PASS")
    print(f"  independent endpoint-character lattice: {lattice}")
    print(f"  explicit holonomy/unit alternatives: {holonomy}")
    print(f"  independent rank-one gcds: {rank_one}")


if __name__ == "__main__":
    main()
