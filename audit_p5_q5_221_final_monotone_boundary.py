#!/usr/bin/env python3
"""Independent audit of the final normalized q5_221 boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md"
PERMUTATIONS = tuple(itertools.permutations(range(3)))
REPRESENTATIVES = (
    (0b0011, 0b0011, 0b0111),
    (0b0011, 0b0011, 0b1101),
    (0b0011, 0b0101, 0b0111),
    (0b0011, 0b0101, 0b1011),
    (0b0011, 0b0101, 0b1110),
    (0b0011, 0b0111, 0b0011),
    (0b0011, 0b0111, 0b0101),
    (0b0011, 0b0111, 0b1001),
    (0b0011, 0b0111, 0b1100),
    (0b0011, 0b1100, 0b0111),
    (0b0011, 0b1101, 0b0011),
    (0b0011, 0b1101, 0b0101),
    (0b0011, 0b1101, 0b0110),
    (0b0011, 0b1101, 0b1100),
)
CLOSED = frozenset((0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11))
EXACT = frozenset((8, 12, 13))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relabel_bits(bits: int, permutation) -> int:
    image = 0
    for old_mode, new_mode in enumerate(permutation):
        if bits & (1 << old_mode):
            image |= 1 << new_mode
    return image


def canonical(pattern):
    orbit = set()
    for permutation in itertools.permutations(range(4)):
        image = tuple(relabel_bits(bits, permutation) for bits in pattern)
        orbit.add(image)
        orbit.add((image[1], image[0], image[2]))
    return min(orbit)


CANONICAL_TO_INDEX = {
    canonical(pattern): index
    for index, pattern in enumerate(REPRESENTATIVES)
}


def direct_extensions(pattern):
    result = set()
    for colour in (0, 1):
        for mode in range(4):
            if pattern[colour] & (1 << mode):
                continue
            extension = list(pattern)
            extension[colour] |= 1 << mode
            result.add(canonical(tuple(extension)))
    return result


def immediate_cover_indices(pattern):
    indices = set()
    for colour in (0, 1):
        if pattern[colour].bit_count() <= 2:
            continue
        for mode in range(4):
            if not pattern[colour] & (1 << mode):
                continue
            cover = list(pattern)
            cover[colour] &= ~(1 << mode)
            if sum(bits.bit_count() for bits in cover) != 7:
                continue
            representative = canonical(tuple(cover))
            indices.add(CANONICAL_TO_INDEX[representative])
    return frozenset(indices)


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
    result = set()
    for vector in itertools.product(range(prime), repeat=3):
        if not any(vector):
            continue
        pivot = next(index for index, value in enumerate(vector) if value)
        inverse = pow(vector[pivot], -1, prime)
        result.add(tuple(value * inverse % prime for value in vector))
    return tuple(sorted(result))


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


def restricted_tensor(normals, prime: int):
    planes = tuple(plane_basis(normal, prime) for normal in normals)
    return tuple(
        sum(
            planes[0][first][permutation[0]]
            * planes[1][second][permutation[1]]
            * planes[2][third][permutation[2]]
            for permutation in PERMUTATIONS
        )
        % prime
        for first, second, third in itertools.product((0, 1), repeat=3)
    )


def flattening_ranks(values, prime: int):
    matrices = (
        [
            list(values[index * 4 : (index + 1) * 4])
            for index in range(2)
        ],
        [
            [
                values[first * 4 + second * 2 + third]
                for first in range(2)
                for third in range(2)
            ]
            for second in range(2)
        ],
        [
            [
                values[first * 4 + second * 2 + third]
                for first in range(2)
                for second in range(2)
            ]
            for third in range(2)
        ],
    )
    return tuple(rank(matrix, 4, prime) for matrix in matrices)


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
    eight_extensions = set()
    for index in EXACT:
        eight_extensions.update(direct_extensions(REPRESENTATIVES[index]))

    exceptional = set()
    for pattern in eight_extensions:
        cover_indices = immediate_cover_indices(pattern)
        assert cover_indices
        if not cover_indices & CLOSED:
            assert cover_indices <= EXACT
            exceptional.add(pattern)

    expected_exceptional = {
        (0b0011, 0b1111, 0b1100),
        (0b0111, 0b1011, 0b1100),
    }
    assert exceptional == expected_exceptional

    ninth_extensions = set()
    for pattern in exceptional:
        ninth_extensions.update(direct_extensions(pattern))
    for pattern in ninth_extensions:
        # Removing either new incidence may give an exceptional
        # eight-pattern; enumerate every seven-subcover through a
        # direct finite check.
        found_closed = False
        for first_colour in (0, 1):
            for first_mode in range(4):
                if pattern[first_colour].bit_count() <= 2:
                    continue
                if not pattern[first_colour] & (1 << first_mode):
                    continue
                eight = list(pattern)
                eight[first_colour] &= ~(1 << first_mode)
                if sum(bits.bit_count() for bits in eight) != 8:
                    continue
                found_closed |= bool(
                    immediate_cover_indices(tuple(eight)) & CLOSED
                )
        assert found_closed

    sign_audit = {}
    for prime in (3, 5):
        lines = projective_lines(prime)
        valid = []
        for normals in itertools.product(lines, repeat=3):
            values = restricted_tensor(normals, prime)
            if any(values) and flattening_ranks(
                values, prime
            ) == (1, 1, 1):
                valid.append(normals)
        equality = tuple(
            normals
            for normals in valid
            if all(normal[1] == normal[2] for normal in normals)
        )
        assert not equality
        sign_audit[str(prime)] = {
            "projective_lines": len(lines),
            "valid_ordered_plane_triples": len(valid),
            "all_equal_coordinate_triples": len(equality),
        }

    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
    variables = (x0, x1, x2, x3)
    h0 = (1, -1, 0, 0)
    h1 = (0, 0, 1, -1)
    t2 = x0 * x1 * x2 * x3
    double_contraction = derivative(
        derivative(t2, variables, h0),
        variables,
        h1,
    )
    expected = (x1 - x0) * (x3 - x2)
    assert sp.expand(double_contraction - expected) == 0
    bilinear_hessian = sp.hessian(double_contraction, variables)
    assert bilinear_hessian.rank() == 2
    # The associated symmetric bilinear tensor has rank two; either
    # cross-block alone is the expected rank-one product.
    mixed_block = bilinear_hessian.extract((0, 1), (2, 3))
    assert mixed_block.rank() == 1
    tensor_bilinear_rank = 2

    output = {
        "audited": True,
        "field": "C",
        "method": (
            "independent cover-extension audit, finite-field sign "
            "slice, and apolar differentiation"
        ),
        "exact_cover_extensions": len(eight_extensions),
        "exceptional_eight_incidence_orbits": [
            [format(bits, "04b") for bits in pattern]
            for pattern in sorted(exceptional)
        ],
        "ninth_extensions_checked": len(ninth_extensions),
        "finite_field_sign_audit": sign_audit,
        "double_contraction": str(double_contraction),
        "double_contracted_tensor_rank": tensor_bilinear_rank,
        "ambient_row_spaces_enumerated": 0,
        "local_maps_enumerated": 0,
        "q5_221_excluded": True,
        "P5_to_Delta3_excluded": False,
        "remaining_branch_in_original_three_type_partition": "q4_211",
        "complete_high_coordinate_partition": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_final_monotone_boundary_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
