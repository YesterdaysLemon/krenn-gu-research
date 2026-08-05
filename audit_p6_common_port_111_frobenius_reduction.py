#!/usr/bin/env python3
"""Independent modular audit of the common-port 1+1+1 reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "tmp" / "p6_common_port_111_frobenius_verified.json"
PAIR_MASKS = tuple(
    (1 << left) | (1 << right)
    for left, right in itertools.combinations(range(5), 2)
)
TRIPLE_MASKS = tuple(
    sum(1 << index for index in triple)
    for triple in itertools.combinations(range(5), 3)
)
TOP_MASK = (1 << 5) - 1

VECTORS = {
    "x01": (0, 0, -1, -1, 0),
    "x02": (0, 1, 0, 0, -1),
    "x10": (-1, 0, 0, 1, 0),
    "x12": (0, 1, 0, 0, -1),
    "x20": (0, 1, 0, -1, 0),
    "x21": (-1, 0, -1, 0, 0),
}

BAD = (
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

GOOD = (
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


def linear_form(vector: tuple[int, ...], prime: int) -> dict[int, int]:
    return {
        1 << index: coefficient % prime
        for index, coefficient in enumerate(vector)
        if coefficient % prime
    }


def multiply(
    left: dict[int, int], right: dict[int, int], prime: int
) -> dict[int, int]:
    result: dict[int, int] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = (
                result.get(mask, 0) + left_value * right_value
            ) % prime
    return {mask: value for mask, value in result.items() if value}


def vectorize(form: dict[int, int], basis: tuple[int, ...]) -> list[int]:
    return [form.get(mask, 0) for mask in basis]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    rows = [[value % prime for value in row] for row in matrix]
    if not rows:
        return 0
    pivot_row = 0
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
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (left - scale * right) % prime
                for left, right in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def nullspace_mod(
    matrix: list[list[int]], columns: int, prime: int
) -> list[list[int]]:
    rows = [[value % prime for value in row] for row in matrix]
    pivot_row = 0
    pivots = []
    for column in range(columns):
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
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (left - scale * right) % prime
                for left, right in zip(rows[row], rows[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
    free_columns = [column for column in range(columns) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [0] * columns
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rows[row][free] % prime
        basis.append(vector)
    return basis


def top_pair(
    quadratic: dict[int, int], cubic_vector: list[int], prime: int
) -> int:
    cubic = {
        mask: value % prime
        for mask, value in zip(TRIPLE_MASKS, cubic_vector)
        if value % prime
    }
    return multiply(quadratic, cubic, prime).get(TOP_MASK, 0)


def main() -> None:
    field_results = {}
    for prime in (3, 5, 7):
        forms = {
            name: linear_form(vector, prime) for name, vector in VECTORS.items()
        }
        plane_ranks = [
            rank_mod(
                [
                    [value % prime for value in VECTORS[left]],
                    [value % prime for value in VECTORS[right]],
                ],
                prime,
            )
            for left, right in (("x01", "x02"), ("x10", "x12"), ("x20", "x21"))
        ]
        assert plane_ranks == [2, 2, 2]

        bad_forms = [multiply(forms[left], forms[right], prime) for left, right in BAD]
        good_forms = [
            multiply(forms[left], forms[right], prime) for left, right in GOOD
        ]
        bad_matrix = [vectorize(form, PAIR_MASKS) for form in bad_forms]
        total_matrix = bad_matrix + [
            vectorize(form, PAIR_MASKS) for form in good_forms
        ]
        bad_rank = rank_mod(bad_matrix, prime)
        total_rank = rank_mod(total_matrix, prime)
        assert bad_rank == 6
        assert total_rank == 9

        # Pairing rows on the cubic basis are obtained by complementary masks,
        # independently of the primary's tuple-index implementation.
        bad_pairing = [
            [form.get(TOP_MASK ^ mask, 0) for mask in TRIPLE_MASKS]
            for form in bad_forms
        ]
        total_pairing = [
            [form.get(TOP_MASK ^ mask, 0) for mask in TRIPLE_MASKS]
            for form in bad_forms + good_forms
        ]
        h_basis = nullspace_mod(bad_pairing, len(TRIPLE_MASKS), prime)
        l_basis = nullspace_mod(total_pairing, len(TRIPLE_MASKS), prime)
        assert len(h_basis) == 4
        assert len(l_basis) == 1
        good_on_h = [
            [top_pair(form, cubic, prime) for cubic in h_basis]
            for form in good_forms
        ]
        assert rank_mod(good_on_h, prime) == 3
        assert all(
            top_pair(form, cubic, prime) == 0
            for form in bad_forms + good_forms
            for cubic in l_basis
        )

        field_results[f"F_{prime}"] = {
            "exceptional_plane_ranks": plane_ranks,
            "forbidden_span_rank": bad_rank,
            "total_span_rank": total_rank,
            "H_dimension": len(h_basis),
            "L_dimension": len(l_basis),
            "marked_pairing_rank_on_H": rank_mod(good_on_h, prime),
        }

    primary_data = json.loads(PRIMARY.read_text(encoding="utf-8"))
    assert primary_data["verified"] is True
    assert primary_data["forbidden_span_rank"] == 6
    assert primary_data["total_quadratic_span_rank"] == 9
    assert primary_data["shared_full_mode_factorization_constructed"] is False
    assert primary_data["profile_excluded"] is False

    output = {
        "verified": True,
        "method": "squarefree subset dictionaries and modular row reduction",
        "finite_fields": field_results,
        "linear_frobenius_relaxation_consistent": True,
        "shared_full_mode_factorization_constructed": False,
        "profile_excluded": False,
        "primary_artifact": PRIMARY.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
    }
    output_path = ROOT / "tmp" / "p6_common_port_111_frobenius_audited.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
