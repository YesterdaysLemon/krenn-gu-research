"""Primary exact checks for the global cross-multiplicity target lattice."""

from __future__ import annotations

import sys
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness import (  # noqa: E402
    complete_table,
    matching_record,
    perfect_matchings,
    transition_data,
)

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Exponent = tuple[int, ...]

EDGES = tuple(combinations(range(8), 2))
EDGE_POSITION = {edge: index for index, edge in enumerate(EDGES)}


def incidence(matching: Matching) -> Exponent:
    """Encode a matching monomial in the physical edge lattice."""
    result = [0] * len(EDGES)
    for edge in matching:
        result[EDGE_POSITION[edge]] += 1
    return tuple(result)


def subtract(left: Exponent, right: Exponent) -> Exponent:
    """Subtract two integral exponent vectors."""
    return tuple(a - b for a, b in zip(left, right, strict=True))


def support_fibres() -> dict[Word, tuple[Matching, ...]]:
    """Enumerate the complete U7D matching fibres by endpoint word."""
    table = complete_table()
    fibres: dict[Word, list[Matching]] = defaultdict(list)
    for matching in perfect_matchings(tuple(range(8))):
        word, _, _ = matching_record(matching, table, 8)
        fibres[word].append(matching)
    return {word: tuple(records) for word, records in fibres.items()}


def endpoint_character(exponent: Exponent) -> tuple[int, ...]:
    """Apply the 24-coordinate endpoint-colour character map."""
    table = complete_table()
    result = [0] * 24
    for edge, coefficient in zip(EDGES, exponent, strict=True):
        if not coefficient:
            continue
        left, right = edge
        left_colour, right_colour, _ = table[edge]
        result[3 * left + left_colour] += coefficient
        result[3 * right + right_colour] += coefficient
    return tuple(result)


def rank(rows: list[Exponent]) -> int:
    """Return the exact rational row rank."""
    return int(sp.Matrix(rows).rank()) if rows else 0


def laurent_value(exponent: Exponent, values: tuple[Fraction, ...]) -> Fraction:
    """Evaluate one Laurent monomial exactly."""
    answer = Fraction(1)
    for power, value in zip(exponent, values, strict=True):
        answer *= value**power
    return answer


def assert_cross_multiplicity_fixture() -> dict[str, object]:
    """Audit the real U7D cross-degree lattice and its exact separation."""
    fibres = support_fibres()
    assert sum(map(len, fibres.values())) == 105
    assert len(fibres) == 101

    rows_by_word: dict[Word, list[Exponent]] = {}
    values = tuple(Fraction(index + 2, index + 1) for index in range(len(EDGES)))
    factorizations = 0
    for word, records in fibres.items():
        if len(records) < 2:
            continue
        reference = incidence(records[0])
        rows = [subtract(incidence(record), reference) for record in records[1:]]
        rows_by_word[word] = rows
        assert all(not any(endpoint_character(row)) for row in rows)

        original = sum(
            (laurent_value(incidence(record), values) for record in records),
            Fraction(0),
        )
        normalized = Fraction(1) + sum(
            (laurent_value(row, values) for row in rows),
            Fraction(0),
        )
        assert original == laurent_value(reference, values) * normalized
        factorizations += 1

    cycle_words = set(transition_data()[0])
    cycle_rows = [row for word, rows in rows_by_word.items() if word in cycle_words for row in rows]
    neighbour_rows = [
        row for word, rows in rows_by_word.items() if word not in cycle_words for row in rows
    ]
    neighbour_words = [word for word in rows_by_word if word not in cycle_words]

    assert len(rows_by_word) == 4
    assert len(cycle_rows) == 3
    assert len(neighbour_rows) == 1
    assert neighbour_words == [(0, 2, 0, 0, 1, 1, 2, 1)]
    assert tuple(neighbour_words[0].count(colour) for colour in range(3)) == (3, 3, 2)
    assert {
        tuple(word.count(colour) for colour in range(3)) for word in cycle_words
    } == {(4, 4, 0)}

    cycle_rank = rank(cycle_rows)
    neighbour_rank = rank(neighbour_rows)
    combined_rank = rank(cycle_rows + neighbour_rows)
    intersection_rank = cycle_rank + neighbour_rank - combined_rank
    assert (cycle_rank, neighbour_rank, combined_rank, intersection_rank) == (3, 1, 4, 0)

    cycle_coordinates = {
        index for row in cycle_rows for index, coefficient in enumerate(row) if coefficient
    }
    neighbour_coordinates = {
        index
        for row in neighbour_rows
        for index, coefficient in enumerate(row)
        if coefficient
    }
    shared_edges = {EDGES[index] for index in cycle_coordinates & neighbour_coordinates}
    assert shared_edges == {(0, 2), (2, 4), (3, 5), (5, 7)}

    # The three pure residuals are monomial-minus-one anchors in this table.
    pure_rows: list[Exponent] = []
    for colour in range(3):
        records = fibres[(colour,) * 8]
        assert len(records) == 1
        _, weight, diagonal = matching_record(records[0], complete_table(), 8)
        assert weight == 1 and diagonal
        pure_rows.append(incidence(records[0]))
    assert rank(cycle_rows + neighbour_rows + pure_rows) == 7

    return {
        "matching_fibres": len(fibres),
        "multi_term_fibres": len(rows_by_word),
        "mixed_multidegrees": ((4, 4, 0), (3, 3, 2)),
        "endpoint_kernel_rows": len(cycle_rows) + len(neighbour_rows),
        "cycle_lattice_rank": cycle_rank,
        "neighbour_lattice_rank": neighbour_rank,
        "intersection_rank": intersection_rank,
        "shared_physical_edges": tuple(sorted(shared_edges)),
        "mixed_plus_pure_anchor_rank": 7,
        "exact_reference_factorizations": factorizations,
    }


def assert_holonomy_dichotomy() -> dict[str, object]:
    """Check proper and unit cross-block outcomes by exact small ideals."""
    x, y, z, w, holonomy = sp.symbols("x y z w H")
    core = [1 + x, 1 + y, 1 + z]

    proper = sp.groebner(
        [*core, x - y, 1 + w, holonomy - x * y * z],
        x,
        y,
        z,
        w,
        holonomy,
        order="lex",
    )
    assert proper.reduce(holonomy + 1)[1] == 0
    assert proper.reduce(sp.Integer(1))[1] == 1
    proper_character = {x: -1, y: -1, z: -1, w: -1, holonomy: -1}
    assert all(sp.expand(polynomial.subs(proper_character)) == 0 for polynomial in proper.polys)

    unit = sp.groebner(
        [*core, 1 + x + y, holonomy - x * y * z],
        x,
        y,
        z,
        holonomy,
        order="lex",
    )
    assert unit.polys == [sp.Poly(1, x, y, z, holonomy, domain="ZZ")]

    # Two residual systems on the same rank-one quotient: one survives and
    # one is a unit.  Their declared source multidegrees play no algebraic role
    # after exact support-difference normalization.
    t = sp.symbols("t")
    proper_gcd = sp.gcd(sp.Poly(t**2 - 1, t), sp.Poly(t - 1, t)).monic()
    unit_gcd = sp.gcd(sp.Poly(t - 1, t), sp.Poly(t + 1, t)).monic()
    assert proper_gcd.as_expr() == t - 1
    assert unit_gcd.as_expr() == 1

    return {
        "cycle_length": 3,
        "proper_cross_block_elimination": "(H+1)",
        "unit_cross_block_elimination": "(1)",
        "rank_one_proper_gcd": str(proper_gcd.as_expr()),
        "rank_one_unit_gcd": str(unit_gcd.as_expr()),
    }


def assert_free_coset_descent() -> dict[str, int]:
    """Check a nonsaturated free coset basis independently of a pivot choice."""
    residues: set[tuple[int, int]] = set()
    checked = 0
    for exponent in product(range(-6, 7), repeat=2):
        representative = (exponent[0] % 2, exponent[1] % 3)
        lattice_part = (
            exponent[0] - representative[0],
            exponent[1] - representative[1],
        )
        assert lattice_part[0] % 2 == 0
        assert lattice_part[1] % 3 == 0
        assert tuple(
            a + b for a, b in zip(lattice_part, representative, strict=True)
        ) == exponent
        residues.add(representative)
        checked += 1
    assert residues == set(product(range(2), range(3)))
    return {"ambient_exponents": checked, "coset_basis_size": len(residues)}


def main() -> None:
    """Run the primary exact checks."""
    fixture = assert_cross_multiplicity_fixture()
    holonomy = assert_holonomy_dichotomy()
    descent = assert_free_coset_descent()
    print("cross-multiplicity global target-lattice primary checks: PASS")
    print(f"  U7D endpoint-character fixture: {fixture}")
    print(f"  global holonomy dichotomy: {holonomy}")
    print(f"  nonsaturated free descent: {descent}")


if __name__ == "__main__":
    main()
