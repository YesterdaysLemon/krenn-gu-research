#!/usr/bin/env python3
"""Independent audit of the remaining fixed-kernel obstructions."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md"
PERMUTATIONS = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rref(rows, columns: int, prime: int):
    matrix = [
        [value % prime for value in row]
        for row in rows
        if any(value % prime for value in row)
    ]
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            inverse * value % prime for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(
                    matrix[row],
                    matrix[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def rank(rows, columns: int, prime: int) -> int:
    return len(rref(rows, columns, prime))


def projective_lines(prime: int):
    result = []
    for vector in itertools.product(range(prime), repeat=3):
        if not any(vector):
            continue
        pivot = next(index for index, value in enumerate(vector) if value)
        inverse = pow(vector[pivot], -1, prime)
        normalized = tuple(value * inverse % prime for value in vector)
        if normalized not in result:
            result.append(normalized)
    return tuple(result)


def plane_basis(normal, prime: int):
    vectors = tuple(
        vector
        for vector in itertools.product(range(prime), repeat=3)
        if any(vector)
        and sum(
            left * right
            for left, right in zip(vector, normal, strict=True)
        )
        % prime
        == 0
    )
    first = vectors[0]
    second = next(
        vector
        for vector in vectors[1:]
        if rank((first, vector), 3, prime) == 2
    )
    return (first, second)


def permanent_three(first, second, third, prime: int) -> int:
    return sum(
        first[permutation[0]]
        * second[permutation[1]]
        * third[permutation[2]]
        for permutation in PERMUTATIONS
    ) % prime


def restricted_tensor(normals, prime: int):
    planes = tuple(plane_basis(normal, prime) for normal in normals)
    return tuple(
        permanent_three(
            planes[0][first],
            planes[1][second],
            planes[2][third],
            prime,
        )
        for first, second, third in itertools.product((0, 1), repeat=3)
    )


def flattening_ranks(values, prime: int):
    first = [
        list(values[index * 4 : (index + 1) * 4])
        for index in range(2)
    ]
    second = [
        [
            values[first_index * 4 + second_index * 2 + third_index]
            for first_index in range(2)
            for third_index in range(2)
        ]
        for second_index in range(2)
    ]
    third = [
        [
            values[first_index * 4 + second_index * 2 + third_index]
            for first_index in range(2)
            for second_index in range(2)
        ]
        for third_index in range(2)
    ]
    return tuple(
        rank(matrix, 4, prime) for matrix in (first, second, third)
    )


def is_nonzero_decomposable(normals, prime: int) -> bool:
    values = restricted_tensor(normals, prime)
    return any(values) and flattening_ranks(values, prime) == (1, 1, 1)


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def main() -> None:
    sign_audits = {}
    for prime in (3, 5):
        lines = projective_lines(prime)
        valid = tuple(
            normals
            for normals in itertools.product(lines, repeat=3)
            if is_nonzero_decomposable(normals, prime)
        )
        all_equal_coordinate = tuple(
            normals
            for normals in valid
            if all(normal[1] == normal[2] for normal in normals)
        )
        cover10_slice = tuple(
            normals
            for normals in valid
            if normals[0][0] == 0
            and normals[1][1] == normals[1][2]
            and normals[2][1] == normals[2][2]
        )
        assert not all_equal_coordinate
        assert len(cover10_slice) == 1
        sign_audits[str(prime)] = {
            "projective_lines": len(lines),
            "valid_ordered_plane_triples": len(valid),
            "all_equal_coordinate_triples": len(all_equal_coordinate),
            "cover10_constrained_triples": len(cover10_slice),
            "cover10_constrained_normals": [
                list(normal) for normal in cover10_slice[0]
            ],
        }

    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    variables = (x0, x1, x2, x3, x4)
    u0 = (1, 1, 0, 0, 0)
    h1 = (0, 0, 1, -1, 0)
    q01 = (x0 + x1) * (x2 - x3) * x4
    q01_h1 = derivative(q01, variables, h1)
    assert sp.expand(q01_h1 - 2 * (x0 + x1) * x4) == 0

    # Independent derivative-rank audit.
    da, db, dc = sp.symbols("da db dc")
    derivative_matrix = sp.Matrix(
        ((0, dc, db), (dc, 0, da), (db, da, 0))
    )
    minors = tuple(
        sp.factor(
            derivative_matrix.extract(indices, indices).det()
        )
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert minors == (-dc**2, -db**2, -da**2)

    # Independent kernel-intersection determinant for the Q02/Q21
    # overlap in cover #7.
    h0 = sp.Matrix((1, -1, 0, 0, 0))
    h1_vector = sp.Matrix(h1)
    u0_vector = sp.Matrix(u0)
    u1 = sp.Matrix((0, 0, 1, 1, 0))
    h2 = sp.Matrix((0, 0, 0, 0, 1))
    ka, kb, kc = sp.symbols("ka kb kc")
    lifted_row = kb * u0_vector - ka * u1 + kc * h2
    overlap_matrix = sp.Matrix.hstack(
        h0,
        h1_vector,
        lifted_row,
        u1,
        h2,
    )
    overlap_determinant = sp.factor(overlap_matrix.det())
    assert overlap_determinant == -4 * kb

    output = {
        "audited": True,
        "field": "C",
        "method": (
            "independent apolar differentiation and finite-field "
            "projective sign-chart audit"
        ),
        "finite_field_sign_audits": sign_audits,
        "Q01_by_h1": str(q01_h1),
        "derivative_principal_minors": [str(value) for value in minors],
        "cover7_overlap_determinant": str(overlap_determinant),
        "ambient_row_spaces_enumerated": 0,
        "local_maps_enumerated": 0,
        "monotone_cover_orbits": [7, 10],
        "monotone_covers_excluded": True,
        "remaining_monotone_cover_orbits": [8, 12, 13],
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_remaining_fixed_kernel_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
