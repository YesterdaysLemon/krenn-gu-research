#!/usr/bin/env python3
"""Primary exact verifier for the common-port 1+1+1 reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md"
PAIRS = tuple(itertools.combinations(range(5), 2))
TRIPLES = tuple(itertools.combinations(range(5), 3))

VECTORS = {
    "x01": (0, 0, -1, -1, 0),
    "x02": (0, 1, 0, 0, -1),
    "x10": (-1, 0, 0, 1, 0),
    "x12": (0, 1, 0, 0, -1),
    "x20": (0, 1, 0, -1, 0),
    "x21": (-1, 0, -1, 0, 0),
}

BAD_NAMES = (
    ("x10", "x21"),
    ("x12", "x20"),
    ("x12", "x21"),
    ("x01", "x20"),
    ("x02", "x20"),
    ("x02", "x21"),
    ("x01", "x10"),
    ("x01", "x12"),
    ("x02", "x10"),
)

GOOD_NAMES = (
    ("x10", "x20"),
    ("x01", "x21"),
    ("x02", "x12"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def degree_two_product(
    left: tuple[int, ...], right: tuple[int, ...]
) -> list[int]:
    return [
        left[first] * right[second] + left[second] * right[first]
        for first, second in PAIRS
    ]


def frobenius_pair(
    quadratic: list[int] | list[Fraction],
    cubic: list[int] | list[Fraction],
) -> Fraction:
    result = Fraction(0)
    for pair_index, pair in enumerate(PAIRS):
        complement = tuple(index for index in range(5) if index not in pair)
        triple_index = TRIPLES.index(complement)
        result += Fraction(quadratic[pair_index]) * Fraction(
            cubic[triple_index]
        )
    return result


def pairing_matrix(quadratics: list[list[int]]) -> list[list[int]]:
    rows = []
    for quadratic in quadratics:
        row = []
        for triple in TRIPLES:
            complement = tuple(index for index in range(5) if index not in triple)
            row.append(quadratic[PAIRS.index(complement)])
        rows.append(row)
    return rows


def rref(
    matrix: list[list[int | Fraction]],
) -> tuple[list[list[Fraction]], list[int]]:
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return [], []
    pivot_row = 0
    pivots = []
    for column in range(len(rows[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                left - scale * right
                for left, right in zip(rows[row], rows[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows[:pivot_row], pivots


def rank(matrix: list[list[int | Fraction]]) -> int:
    return len(rref(matrix)[1])


def nullspace(
    matrix: list[list[int | Fraction]], columns: int
) -> list[list[Fraction]]:
    reduced, pivots = rref(matrix)
    free_columns = [column for column in range(columns) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(vector)
    return basis


def solve_surjective(
    matrix: list[list[Fraction]], target: list[int]
) -> list[Fraction]:
    augmented = [
        row[:] + [Fraction(value)] for row, value in zip(matrix, target)
    ]
    reduced, pivots = rref(augmented)
    variable_count = len(matrix[0])
    assert all(pivot < variable_count for pivot in pivots)
    solution = [Fraction(0) for _ in range(variable_count)]
    for row, pivot in enumerate(pivots):
        solution[pivot] = reduced[row][-1]
    assert [
        sum(entry * value for entry, value in zip(row, solution))
        for row in matrix
    ] == [Fraction(value) for value in target]
    return solution


def linear_combination(
    coefficients: list[Fraction], vectors: list[list[Fraction]]
) -> list[Fraction]:
    return [
        sum(
            coefficient * vector[index]
            for coefficient, vector in zip(coefficients, vectors)
        )
        for index in range(len(vectors[0]))
    ]


def main() -> None:
    exceptional_pairs = (
        (VECTORS["x01"], VECTORS["x02"]),
        (VECTORS["x10"], VECTORS["x12"]),
        (VECTORS["x20"], VECTORS["x21"]),
    )
    assert [rank([list(left), list(right)]) for left, right in exceptional_pairs] == [
        2,
        2,
        2,
    ]

    bad = [
        degree_two_product(VECTORS[left], VECTORS[right])
        for left, right in BAD_NAMES
    ]
    good = [
        degree_two_product(VECTORS[left], VECTORS[right])
        for left, right in GOOD_NAMES
    ]
    bad_rank = rank(bad)
    total_rank = rank(bad + good)
    assert bad_rank == 6
    assert total_rank == 9
    assert total_rank - bad_rank == 3

    # Reconstruct the three 2 x 2 exceptional coefficient tables directly
    # from the missing-column pattern.
    exceptional_columns = {
        0: {1: "x01", 2: "x02"},
        1: {0: "x10", 2: "x12"},
        2: {0: "x20", 1: "x21"},
    }
    coefficient_table = {}
    reconstructed_bad_names = []
    reconstructed_good_names = []
    for deleted_colour in range(3):
        active_modes = [mode for mode in range(3) if mode != deleted_colour]
        left_mode, right_mode = active_modes
        table = {}
        for left_colour, right_colour in itertools.product(
            exceptional_columns[left_mode], exceptional_columns[right_mode]
        ):
            names = (
                exceptional_columns[left_mode][left_colour],
                exceptional_columns[right_mode][right_colour],
            )
            is_good = left_colour == right_colour == deleted_colour
            table[f"{left_colour},{right_colour}"] = {
                "factors": list(names),
                "marked": is_good,
            }
            if is_good:
                reconstructed_good_names.append(names)
            else:
                reconstructed_bad_names.append(names)
        coefficient_table[str(deleted_colour)] = table
    assert set(map(frozenset, reconstructed_bad_names)) == set(
        map(frozenset, BAD_NAMES)
    )
    assert set(map(frozenset, reconstructed_good_names)) == set(
        map(frozenset, GOOD_NAMES)
    )

    h_basis = nullspace(pairing_matrix(bad), len(TRIPLES))
    l_basis = nullspace(pairing_matrix(bad + good), len(TRIPLES))
    assert len(h_basis) == 4
    assert len(l_basis) == 1
    assert all(
        frobenius_pair(quadratic, cubic) == 0
        for quadratic in bad
        for cubic in h_basis
    )
    assert all(
        frobenius_pair(quadratic, cubic) == 0
        for quadratic in bad + good
        for cubic in l_basis
    )

    good_on_h = [
        [frobenius_pair(quadratic, cubic) for cubic in h_basis]
        for quadratic in good
    ]
    assert rank(good_on_h) == 3
    diagonal_cubics = []
    for colour in range(3):
        target = [int(index == colour) for index in range(3)]
        coefficients = solve_surjective(good_on_h, target)
        cubic = linear_combination(coefficients, h_basis)
        diagonal_cubics.append(cubic)
    diagonal_pairing = [
        [frobenius_pair(quadratic, cubic) for cubic in diagonal_cubics]
        for quadratic in good
    ]
    assert diagonal_pairing == [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    assert all(
        frobenius_pair(quadratic, cubic) == 0
        for quadratic in bad
        for cubic in diagonal_cubics
    )

    # An abstract 27-entry cubic table satisfies every linear pairing
    # equation: use the three dual cubics on the diagonal and zero in every
    # mixed position.  No shared factorization is asserted.
    abstract_cubic_table = {}
    linear_pairing_checks = 0
    zero_cubic = [Fraction(0) for _ in TRIPLES]
    for word in itertools.product(range(3), repeat=3):
        cubic = diagonal_cubics[word[0]] if len(set(word)) == 1 else zero_cubic
        abstract_cubic_table["".join(map(str, word))] = (
            f"w_{word[0]}" if len(set(word)) == 1 else "0"
        )
        for bad_quadratic in bad:
            assert frobenius_pair(bad_quadratic, cubic) == 0
            linear_pairing_checks += 1
        for colour, good_quadratic in enumerate(good):
            expected = int(word == (colour, colour, colour))
            assert frobenius_pair(good_quadratic, cubic) == expected
            linear_pairing_checks += 1

    output = {
        "verified": True,
        "field": "C",
        "exceptional_plane_ranks": [2, 2, 2],
        "forbidden_quadrics": len(bad),
        "marked_quadrics": len(good),
        "forbidden_span_rank": bad_rank,
        "total_quadratic_span_rank": total_rank,
        "marked_quotient_rank": total_rank - bad_rank,
        "H_dimension": len(h_basis),
        "L_dimension": len(l_basis),
        "marked_pairing_on_dual_cubics": [
            [str(value) for value in row] for row in diagonal_pairing
        ],
        "exceptional_coefficient_tables": coefficient_table,
        "abstract_cubic_entries": abstract_cubic_table,
        "linear_pairing_checks": linear_pairing_checks,
        "shared_full_mode_factorization_constructed": False,
        "profile_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
    }
    output_path = ROOT / "tmp" / "p6_common_port_111_frobenius_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
