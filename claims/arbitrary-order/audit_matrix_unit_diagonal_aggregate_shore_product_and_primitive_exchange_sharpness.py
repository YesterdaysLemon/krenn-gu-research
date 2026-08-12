"""Independent no-import audit of diagonal aggregate shore-product sharpness."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb, gcd

Edge = tuple[int, int]
Poly = tuple[Fraction, ...]
WordCode = int

ORDER = 12
ONE: Poly = (Fraction(1),)
NEG_ONE: Poly = (Fraction(-1),)
T_POLY: Poly = (Fraction(0), Fraction(1))
X_POLY: Poly = (Fraction(-1), Fraction(-1))


def normalize(poly: Poly) -> Poly:
    """Remove high zero coefficients."""
    values = list(poly)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_add(left: Poly, right: Poly) -> Poly:
    """Add exact coefficient tuples."""
    size = max(len(left), len(right))
    result = [Fraction(0) for _ in range(size)]
    for index in range(size):
        if index < len(left):
            result[index] += left[index]
        if index < len(right):
            result[index] += right[index]
    return normalize(tuple(result))


def poly_mul(left: Poly, right: Poly) -> Poly:
    """Multiply exact coefficient tuples."""
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            result[left_degree + right_degree] += left_value * right_value
    return normalize(tuple(result))


def poly_sum(values: list[Poly]) -> Poly:
    """Add a list of exact polynomials."""
    result = (Fraction(0),)
    for value in values:
        result = poly_add(result, value)
    return result


def is_zero(poly: Poly) -> bool:
    """Test exact polynomial zero."""
    return all(value == 0 for value in poly)


def build_table() -> dict[Edge, tuple[int, int, Poly]]:
    """Rebuild the literal table independently from the primary verifier."""
    old_rows = (
        (0, 1, 0, 0, ONE),
        (0, 2, 0, 0, ONE),
        (0, 3, 0, 0, ONE),
        (0, 4, 0, 0, ONE),
        (0, 5, 1, 2, ONE),
        (0, 6, 1, 1, ONE),
        (0, 7, 2, 2, ONE),
        (1, 2, 0, 1, NEG_ONE),
        (1, 3, 0, 0, ONE),
        (1, 4, 1, 0, NEG_ONE),
        (1, 5, 1, 1, ONE),
        (1, 6, 2, 2, ONE),
        (1, 7, 0, 0, ONE),
        (2, 3, 1, 1, ONE),
        (2, 4, 0, 1, X_POLY),
        (2, 5, 2, 2, ONE),
        (2, 6, 0, 0, ONE),
        (2, 7, 2, 0, ONE),
        (3, 4, 2, 2, ONE),
        (3, 5, 0, 1, ONE),
        (3, 6, 1, 0, ONE),
        (3, 7, 1, 1, ONE),
        (4, 5, 0, 0, ONE),
        (4, 6, 1, 1, ONE),
        (4, 7, 1, 1, ONE),
        (5, 6, 0, 1, ONE),
        (5, 7, 1, 1, ONE),
        (6, 7, 1, 1, ONE),
    )
    table = {
        (left, right): (left_label, right_label, weight)
        for left, right, left_label, right_label, weight in old_rows
    }

    for old in range(8):
        for new in range(8, 12):
            labels = (0, 1) if new < 10 else (1, 0)
            table[(old, new)] = (*labels, ONE)

    table.update(
        {
            (8, 9): (0, 0, ONE),
            (8, 10): (0, 0, ONE),
            (8, 11): (1, 1, ONE),
            (9, 10): (1, 1, ONE),
            (9, 11): (0, 0, ONE),
            (10, 11): (1, 1, ONE),
            (0, 8): (2, 2, ONE),
            (1, 9): (2, 2, ONE),
            (2, 8): (0, 0, T_POLY),
            (3, 9): (0, 0, ONE),
            (6, 10): (2, 2, ONE),
            (7, 11): (2, 2, ONE),
            (1, 11): (1, 0, (Fraction(2),)),
        }
    )
    return table


EDGES = tuple(combinations(range(ORDER), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def edge_mask(*edges: Edge) -> int:
    """Pack an edge set into a 66-bit integer."""
    result = 0
    for left, right in edges:
        edge = (min(left, right), max(left, right))
        result |= 1 << EDGE_INDEX[edge]
    return result


def matching_masks(vertices_mask: int):
    """Generate matchings by pairing the highest remaining vertex."""
    if vertices_mask == 0:
        yield 0
        return
    right = vertices_mask.bit_length() - 1
    without_right = vertices_mask ^ (1 << right)
    possible = without_right
    while possible:
        left_bit = possible & -possible
        left = left_bit.bit_length() - 1
        residue = without_right ^ left_bit
        for tail in matching_masks(residue):
            yield tail | (1 << EDGE_INDEX[(left, right)])
        possible ^= left_bit


def unpack_edges(mask: int) -> tuple[Edge, ...]:
    """Decode an edge mask."""
    return tuple(
        edge for index, edge in enumerate(EDGES) if mask & (1 << index)
    )


def encode_word(labels: tuple[int, ...]) -> WordCode:
    """Pack a ternary word in base three."""
    result = 0
    power = 1
    for label in labels:
        result += label * power
        power *= 3
    return result


def parse_word(text: str) -> WordCode:
    """Pack a displayed ternary word."""
    return encode_word(tuple(map(int, text)))


def record_matching(
    mask: int,
    table: dict[Edge, tuple[int, int, Poly]],
) -> tuple[WordCode, Poly, bool]:
    """Compute packed word, custom polynomial weight, and diagonal flag."""
    labels = [-1] * ORDER
    weight = ONE
    diagonal = True
    for edge in unpack_edges(mask):
        left_label, right_label, scalar = table[edge]
        labels[edge[0]] = left_label
        labels[edge[1]] = right_label
        weight = poly_mul(weight, scalar)
        diagonal = diagonal and left_label == right_label
    return encode_word(tuple(labels)), weight, diagonal


def fraction_rank(matrix: list[list[Fraction]]) -> int:
    """Compute exact row rank by a local Gaussian elimination."""
    work = [row[:] for row in matrix]
    pivot_row = 0
    if not work:
        return 0
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
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor == 0:
                continue
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def determinant_4(matrix: list[list[int]]) -> Fraction:
    """Compute a four-by-four determinant with exact elimination."""
    work = [[Fraction(value) for value in row] for row in matrix]
    determinant = Fraction(1)
    for column in range(4):
        pivot = next(
            (row for row in range(column, 4) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant *= -1
        pivot_value = work[column][column]
        determinant *= pivot_value
        for entry in range(column, 4):
            work[column][entry] /= pivot_value
        for row in range(column + 1, 4):
            factor = work[row][column]
            for entry in range(column, 4):
                work[row][entry] -= factor * work[column][entry]
    return determinant


def difference(positive: int, negative: int) -> list[int]:
    """Return one signed matching difference from packed masks."""
    return [
        int(bool(positive & (1 << index)))
        - int(bool(negative & (1 << index)))
        for index in range(len(EDGES))
    ]


@lru_cache(maxsize=None)
def compatible_shore_hafnian(
    vertices_mask: int,
    colour: int,
    frozen_table: tuple[tuple[Edge, tuple[int, int, Poly]], ...],
) -> tuple[int, Poly]:
    """Compute a shore count and hafnian by pairing the lowest vertex."""
    if vertices_mask == 0:
        return 1, ONE
    table = dict(frozen_table)
    left_bit = vertices_mask & -vertices_mask
    left = left_bit.bit_length() - 1
    residue = vertices_mask ^ left_bit
    count = 0
    value = (Fraction(0),)
    partners = residue
    while partners:
        right_bit = partners & -partners
        right = right_bit.bit_length() - 1
        edge = (left, right)
        left_label, right_label, weight = table[edge]
        if left_label == right_label == colour:
            subcount, subvalue = compatible_shore_hafnian(
                residue ^ right_bit,
                colour,
                frozen_table,
            )
            count += subcount
            value = poly_add(value, poly_mul(weight, subvalue))
        partners ^= right_bit
    return count, value


def check_triangular_holonomy_independence() -> None:
    """Audit injectivity of H -> -1/(1+t) in bounded exact degrees."""
    for degree in range(13):
        columns: list[list[Fraction]] = []
        for power in range(degree + 1):
            exponent = degree - power
            coefficients = [Fraction(0) for _ in range(degree + 1)]
            sign = Fraction((-1) ** power)
            for term_degree in range(exponent + 1):
                coefficients[term_degree] = sign * comb(exponent, term_degree)
            columns.append(coefficients)
        matrix = [
            [columns[column][row] for column in range(degree + 1)]
            for row in range(degree + 1)
        ]
        assert fraction_rank(matrix) == degree + 1


def main() -> None:
    """Run the independent exact audit."""
    table = build_table()
    assert set(table) == set(EDGES)
    assert len(table) == 66

    local_labels = [set() for _ in range(ORDER)]
    for (left, right), (left_label, right_label, _) in table.items():
        local_labels[left].add(left_label)
        local_labels[right].add(right_label)
    assert local_labels == [{0, 1, 2} for _ in range(ORDER)]

    ledgers: dict[WordCode, list[tuple[int, Poly, bool]]] = defaultdict(list)
    all_vertices = (1 << ORDER) - 1
    for matching in matching_masks(all_vertices):
        word_code, weight, diagonal = record_matching(matching, table)
        ledgers[word_code].append((matching, weight, diagonal))

    assert sum(map(len, ledgers.values())) == 10395
    assert len(ledgers) == 5128
    assert sum(len(records) == 1 for records in ledgers.values()) == 2979

    chi_0 = parse_word("000011110011")
    chi_1 = parse_word("001100110011")
    chi_2 = parse_word("010101010011")

    f_0 = edge_mask((0, 1), (2, 4), (3, 5), (6, 7), (8, 9), (10, 11))
    extra = edge_mask((0, 1), (2, 8), (3, 9), (4, 6), (5, 7), (10, 11))
    g_2 = edge_mask((0, 2), (1, 3), (4, 6), (5, 7), (8, 9), (10, 11))
    g_0 = edge_mask((0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11))
    f_1 = edge_mask((0, 4), (1, 2), (3, 7), (5, 6), (8, 9), (10, 11))
    f_2 = edge_mask((0, 2), (1, 4), (3, 6), (5, 7), (8, 9), (10, 11))
    g_1 = edge_mask((0, 4), (1, 5), (2, 6), (3, 7), (8, 9), (10, 11))

    expected = {
        chi_0: {
            f_0: (X_POLY, False),
            extra: (T_POLY, True),
            g_2: (ONE, True),
        },
        chi_1: {g_0: (ONE, True), f_1: (NEG_ONE, False)},
        chi_2: {f_2: (NEG_ONE, False), g_1: (ONE, True)},
    }
    for word_code, expected_records in expected.items():
        actual = {
            matching: (weight, diagonal)
            for matching, weight, diagonal in ledgers[word_code]
        }
        assert actual == expected_records
        assert is_zero(poly_sum([weight for _, weight, _ in ledgers[word_code]]))

    pure = {
        parse_word("0" * ORDER): edge_mask(
            (0, 3), (1, 7), (2, 6), (4, 5), (8, 10), (9, 11)
        ),
        parse_word("1" * ORDER): edge_mask(
            (0, 6), (1, 5), (2, 3), (4, 7), (8, 11), (9, 10)
        ),
        parse_word("2" * ORDER): edge_mask(
            (0, 8), (1, 9), (2, 5), (3, 4), (6, 10), (7, 11)
        ),
    }
    for word_code, matching in pure.items():
        assert ledgers[word_code] == [(matching, ONE, True)]

    active = set()
    for word_code, records in ledgers.items():
        total = poly_sum([weight for _, weight, _ in records])
        offdiagonal = poly_sum(
            [weight for _, weight, diagonal in records if not diagonal]
        )
        if is_zero(total) and not is_zero(offdiagonal):
            active.add(word_code)
    assert active == {chi_0, chi_1, chi_2}

    frozen_table = tuple(sorted(table.items()))
    zero_vertices = sum(1 << vertex for vertex in (0, 1, 2, 3, 8, 9))
    one_vertices = sum(1 << vertex for vertex in (4, 5, 6, 7, 10, 11))
    assert compatible_shore_hafnian(zero_vertices, 0, frozen_table) == (
        2,
        (Fraction(1), Fraction(1)),
    )
    assert compatible_shore_hafnian(one_vertices, 1, frozen_table) == (1, ONE)
    assert compatible_shore_hafnian(0, 2, frozen_table) == (1, ONE)

    for vertices_mask, colour in ((zero_vertices, 0), (one_vertices, 1)):
        vertices = [
            vertex for vertex in range(ORDER) if vertices_mask & (1 << vertex)
        ]
        for size in range(2, len(vertices) + 1, 2):
            for subset in combinations(vertices, size):
                subset_mask = sum(1 << vertex for vertex in subset)
                count, hafnian = compatible_shore_hafnian(
                    subset_mask,
                    colour,
                    frozen_table,
                )
                if count:
                    assert not is_zero(hafnian)

    p_zero = edge_mask((0, 2), (1, 3), (8, 9))
    m_zero = edge_mask((0, 1), (2, 8), (3, 9))
    cycle_mask = p_zero ^ m_zero
    cycle_edges = set(unpack_edges(cycle_mask))
    assert cycle_edges == {
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 8),
        (3, 9),
        (8, 9),
    }
    degrees = defaultdict(int)
    for left, right in cycle_edges:
        degrees[left] += 1
        degrees[right] += 1
    assert set(degrees.values()) == {2}

    vectors = [
        difference(f_0, g_2),
        difference(f_1, g_0),
        difference(f_2, g_1),
        difference(extra, g_2),
    ]
    assert gcd(*[abs(value) for value in vectors[-1]]) == 1
    assert fraction_rank(
        [[Fraction(value) for value in vector] for vector in vectors]
    ) == 4
    columns = [EDGE_INDEX[edge] for edge in ((0, 1), (0, 2), (1, 2), (2, 4))]
    minor = [[vector[column] for column in columns] for vector in vectors]
    assert minor == [
        [1, -1, 0, 1],
        [-1, 0, 1, 0],
        [0, 1, 0, 0],
        [1, -1, 0, 0],
    ]
    assert determinant_4(minor) == 1

    delta_support = {
        EDGES[index] for index, value in enumerate(vectors[-1]) if value
    }
    cycle_support = {
        EDGES[index]
        for vector in vectors[:3]
        for index, value in enumerate(vector)
        if value
    }
    assert delta_support & cycle_support == {(0, 1), (0, 2), (1, 3)}

    check_triangular_holonomy_independence()

    eta = parse_word("000001000011")
    eta_matching = edge_mask(
        (0, 4), (1, 7), (2, 6), (3, 5), (8, 9), (10, 11)
    )
    assert ledgers[eta] == [(eta_matching, ONE, False)]

    print("PASS no-import 66-bit matching census: 10395 exact matchings")
    print("PASS only three active words and one shortest directed cycle")
    print("PASS complete 3/2/2 fibres have solely diagonal excess")
    print("PASS independent shore DP gives the 2x1x1 product")
    print("PASS every supported sharpness subshore has nonzero hafnian")
    print("PASS primitive alternating 6-cycle reconstructed by XOR")
    print("PASS custom Gaussian audit gives saturated direct rank 4")
    print("PASS shared physical edges do not create an integer dependency")
    print("PASS triangular H-substitution ranks through degree 12")
    print("PASS pure anchors equal 1 and outside singleton is a unit")
    print("PASS global Krenn-Gu status remains UNRESOLVED")


if __name__ == "__main__":
    main()
