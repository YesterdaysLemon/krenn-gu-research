"""Primary exact checks for complete-block fibre-lattice descent."""

from __future__ import annotations

import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository src directory")

from krenn_gu.integer_signed_lattice import IntegerSignedLattice  # noqa: E402

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


def balanced_words() -> tuple[Word, ...]:
    """Return the complete eight-letter multidegree-(4,4,0) block."""
    records = []
    for zero_positions in combinations(range(8), 4):
        word = [1] * 8
        for position in zero_positions:
            word[position] = 0
        records.append(tuple(word))
    return tuple(records)


def support_fibres() -> dict[Word, tuple[Matching, ...]]:
    """Group every physical perfect matching by its endpoint-label word."""
    table = complete_table()
    fibres: dict[Word, list[Matching]] = {}
    for matching in perfect_matchings(tuple(range(8))):
        word, _, _ = matching_record(matching, table, 8)
        fibres.setdefault(word, []).append(matching)
    return {word: tuple(records) for word, records in fibres.items()}


EDGES = tuple(combinations(range(8), 2))
EDGE_POSITION = {edge: index for index, edge in enumerate(EDGES)}


def incidence(matching: Matching) -> Exponent:
    """Encode one square-free matching monomial in Z^E."""
    vector = [0] * len(EDGES)
    for edge in matching:
        vector[EDGE_POSITION[edge]] += 1
    return tuple(vector)


def subtract(left: Exponent, right: Exponent) -> Exponent:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def add(*vectors: Exponent) -> Exponent:
    return tuple(sum(entries) for entries in zip(*vectors, strict=True))


def laurent_value(exponent: Exponent, values: dict[Edge, Fraction]) -> Fraction:
    """Evaluate an integral Laurent monomial exactly."""
    result = Fraction(1)
    for edge, power in zip(EDGES, exponent, strict=True):
        result *= values[edge] ** power
    return result


def exact_assignments() -> tuple[dict[Edge, Fraction], ...]:
    """Give two nonzero rational physical-amplitude assignments."""
    first = {
        edge: Fraction(index + 2, 1)
        for index, edge in enumerate(EDGES)
    }
    second = {
        edge: Fraction((-1 if index % 3 == 0 else 1) * (index + 3), index + 2)
        for index, edge in enumerate(EDGES)
    }
    return first, second


def assert_complete_block_normalization() -> dict[str, object]:
    """Check every original fibre against its normalized Laurent polynomial."""
    fibres = support_fibres()
    words = balanced_words()
    histogram: Counter[int] = Counter()
    relation_rows: list[Exponent] = []
    normalized_terms = 0
    checked_equalities = 0

    for word in words:
        fibre = fibres.get(word, ())
        histogram[len(fibre)] += 1
        if not fibre:
            continue
        reference = incidence(fibre[0])
        normalized = tuple(subtract(incidence(matching), reference) for matching in fibre)
        assert normalized[0] == (0,) * len(EDGES)
        relation_rows.extend(normalized[1:])
        normalized_terms += len(normalized)

        for values in exact_assignments():
            original = sum(
                (laurent_value(incidence(matching), values) for matching in fibre),
                Fraction(0),
            )
            reduced = laurent_value(reference, values) * sum(
                (laurent_value(exponent, values) for exponent in normalized),
                Fraction(0),
            )
            assert original == reduced
            checked_equalities += 1

    assert histogram == Counter({0: 57, 1: 10, 2: 3})
    assert len(relation_rows) == 3
    assert normalized_terms == 16

    singleton_word = (0, 0, 0, 1, 1, 0, 1, 1)
    singleton = fibres[singleton_word]
    assert len(singleton) == 1
    singleton_normalized = (
        subtract(incidence(singleton[0]), incidence(singleton[0])),
    )
    assert singleton_normalized == ((0,) * len(EDGES),)

    return {
        "words": len(words),
        "histogram": dict(sorted(histogram.items())),
        "normalized_terms": normalized_terms,
        "within_fibre_rows": len(relation_rows),
        "exact_factorizations_checked": checked_equalities,
        "singleton_normalized_polynomial": "1",
    }


def assert_active_cycle_lattice() -> dict[str, object]:
    """Reconstruct the U7D binomial rows and their exact holonomy sign."""
    table = complete_table()
    fibres = support_fibres()
    cycle_words, _, _, _ = transition_data()
    rows: list[Exponent] = []
    specialized_holonomy = Fraction(1)

    for word in cycle_words:
        fibre = fibres[word]
        assert len(fibre) == 2
        records = [matching_record(matching, table, 8) for matching in fibre]
        diagonal = next(matching for matching, (_, _, flag) in zip(fibre, records, strict=True) if flag)
        cross = next(matching for matching, (_, _, flag) in zip(fibre, records, strict=True) if not flag)
        diagonal_weight = matching_record(diagonal, table, 8)[1]
        cross_weight = matching_record(cross, table, 8)[1]
        assert diagonal_weight == 1 and cross_weight == -1
        rows.append(subtract(incidence(diagonal), incidence(cross)))
        specialized_holonomy *= diagonal_weight / cross_weight

    lattice = IntegerSignedLattice(rows)
    assert lattice.rank == 3
    assert not lattice.has_inconsistent_kernel
    holonomy_exponent = add(*rows)
    assert lattice.transported_sign(holonomy_exponent) == -1
    assert specialized_holonomy == -1

    # The three rows are part of the complete block's within-fibre lattice,
    # but the complete U7D block is already the unit ideal by its singleton.
    return {
        "cycle_length": len(rows),
        "relation_rank": lattice.rank,
        "kernel_dimension": len(lattice.kernel_basis),
        "parity_consistent": True,
        "transported_holonomy_sign": lattice.transported_sign(holonomy_exponent),
        "specialized_holonomy": specialized_holonomy,
        "binomial_subsystem_elimination": "(H+1)",
        "complete_block_elimination": "(1) via singleton",
    }


def combine(coefficients: tuple[int, ...], rows: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(
        sum(coefficient * row[column] for coefficient, row in zip(coefficients, rows, strict=True))
        for column in range(len(rows[0]))
    )


def assert_signed_parity_dichotomy() -> dict[str, int]:
    """Check saturated and nonsaturated consistent/inconsistent systems."""
    cases = (
        {
            "rows": ((1, 0), (0, 1), (1, 1)),
            "inconsistent": True,
            "witness": (1, 1, -1),
        },
        {
            "rows": ((2,), (4,)),
            "inconsistent": True,
            "witness": (2, -1),
        },
        {
            "rows": ((2, 0), (2, 0), (0, 2)),
            "inconsistent": False,
            "witness": (1, -1, 0),
        },
        {
            "rows": ((2,), (-2,)),
            "inconsistent": False,
            "witness": (1, 1),
        },
    )
    consistent = 0
    inconsistent = 0
    nonsaturated = 0

    for case in cases:
        rows = case["rows"]
        witness = case["witness"]
        lattice = IntegerSignedLattice(rows)
        assert combine(witness, rows) == (0,) * len(rows[0])
        assert lattice.has_inconsistent_kernel is case["inconsistent"]
        assert (sum(witness) % 2 == 1) is case["inconsistent"]
        if case["inconsistent"]:
            inconsistent += 1
        else:
            consistent += 1
            first_row = rows[0]
            assert lattice.transported_sign(first_row) == -1
        if any(abs(entry) > 1 for row in rows for entry in row):
            nonsaturated += 1

    return {
        "systems": len(cases),
        "consistent": consistent,
        "odd_dependency_unit_cases": inconsistent,
        "nonsaturated_cases": nonsaturated,
    }


def assert_nonsaturated_coset_basis() -> dict[str, int]:
    """Audit the free coset decomposition for 2Z plus 3Z in a box."""
    seen = 0
    residues: Counter[tuple[int, int]] = Counter()
    for exponent in product(range(-5, 6), repeat=2):
        representative = (exponent[0] % 2, exponent[1] % 3)
        lattice_part = (
            exponent[0] - representative[0],
            exponent[1] - representative[1],
        )
        assert lattice_part[0] % 2 == 0
        assert lattice_part[1] % 3 == 0
        assert tuple(a + b for a, b in zip(lattice_part, representative, strict=True)) == exponent
        residues[representative] += 1
        seen += 1
    assert set(residues) == set(product(range(2), range(3)))
    return {"exponents_decomposed": seen, "coset_representatives": len(residues)}


def main() -> None:
    block = assert_complete_block_normalization()
    cycle = assert_active_cycle_lattice()
    parity = assert_signed_parity_dichotomy()
    cosets = assert_nonsaturated_coset_basis()
    print("complete same-multidegree fibre-lattice primary checks: PASS")
    print(f"  complete-block normalization: {block}")
    print(f"  active-cycle signed lattice: {cycle}")
    print(f"  binomial parity dichotomy: {parity}")
    print(f"  nonsaturated coset basis: {cosets}")


if __name__ == "__main__":
    main()
