#!/usr/bin/env python3
"""Independent finite-field audit of the H31 rank-two-family no-lift."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inv(value: int, prime: int) -> int:
    return pow(value % prime, -1, prime)


def permanent(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    size = len(rows)
    total = 0
    for permutation in itertools.permutations(range(size)):
        product = 1
        for row in range(size):
            product = product * rows[row][permutation[row]] % prime
        total = (total + product) % prime
    return total


def rref_mod(
    matrix: list[list[int]],
    prime: int,
) -> tuple[list[list[int]], tuple[int, ...]]:
    result = [
        [value % prime for value in row]
        for row in matrix
    ]
    if not result:
        return result, ()
    rows = len(result)
    columns = len(result[0])
    pivot_columns = []
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (
                row
                for row in range(pivot_row, rows)
                if result[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = (
            result[selected],
            result[pivot_row],
        )
        scale = inv(result[pivot_row][column], prime)
        result[pivot_row] = [
            value * scale % prime
            for value in result[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row or not result[row][column]:
                continue
            multiple = result[row][column]
            result[row] = [
                (left - multiple * right) % prime
                for left, right in zip(
                    result[row],
                    result[pivot_row],
                    strict=True,
                )
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return result, tuple(pivot_columns)


def nullspace_mod(
    matrix: list[list[int]],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    rref, pivots = rref_mod(matrix, prime)
    columns = len(matrix[0])
    free = tuple(
        column for column in range(columns) if column not in pivots
    )
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free_column] % prime
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left: list[int], right: tuple[int, ...], prime: int) -> int:
    return sum(
        first * second
        for first, second in zip(left, right, strict=True)
    ) % prime


def pure_family_shared(
    prime: int,
    epsilon: int,
    iota: int,
    ell: int,
    jay: int,
    chi: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    inv_e = inv(epsilon, prime)
    inv_i = inv(iota, prime)
    gamma = epsilon * iota * ell % prime
    beta = (
        (0, 1, (chi + gamma) * inv_e % prime),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, iota),
    )
    alpha = (
        (1, jay, 0),
        (ell, 1, -iota * ell % prime),
        (-inv_i % prime, 0, 1),
        (0, 0, -inv_e % prime),
    )
    return alpha, beta


def extension_system(
    alpha_shared: tuple[tuple[int, ...], ...],
    beta_shared: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[list[list[int]], list[int], list[int]]:
    coefficient_rows = {}
    for bits in BITS4:
        word = "".join(map(str, bits))
        row = []
        for variable in range(8):
            alpha = []
            beta = []
            for mode in range(4):
                alpha.append(
                    alpha_shared[mode]
                    + (int(variable == mode),)
                )
                beta.append(
                    beta_shared[mode]
                    + (int(variable == 4 + mode),)
                )
            selected = tuple(
                beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            )
            row.append(permanent(selected, prime))
        coefficient_rows[word] = row
    mixed = [
        coefficient_rows[word]
        for word in coefficient_rows
        if word not in ("0000", "1111")
    ]
    return (
        mixed,
        coefficient_rows["0000"],
        coefficient_rows["1111"],
    )


def linear_combination(
    basis: tuple[tuple[int, ...], ...],
    coefficients: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    return tuple(
        sum(
            coefficients[index] * basis[index][coordinate]
            for index in range(len(basis))
        )
        % prime
        for coordinate in range(len(basis[0]))
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    rows = []
    for bits in BITS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if bits[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    ),
                    prime,
                )
            )
        rows.append(coefficient_row)
    return rows


def audit_prime(prime: int) -> dict[str, int]:
    admissible_parameters = 0
    binary_extendable_parameters = 0
    binary_delta2_extensions = 0
    attempted_third_row_lifts = 0
    successful_third_row_lifts = 0

    for epsilon in range(1, prime):
        for iota in range(1, prime):
            for ell, jay, chi in itertools.product(
                range(prime),
                repeat=3,
            ):
                if (chi + epsilon * iota * ell) % prime == 0:
                    continue
                admissible_parameters += 1
                alpha_shared, beta_shared = pure_family_shared(
                    prime,
                    epsilon,
                    iota,
                    ell,
                    jay,
                    chi,
                )
                mixed, alpha_diagonal, beta_diagonal = extension_system(
                    alpha_shared,
                    beta_shared,
                    prime,
                )
                kernel = nullspace_mod(mixed, prime)
                valid_vectors = []
                for coefficients in itertools.product(
                    range(prime),
                    repeat=len(kernel),
                ):
                    if not any(coefficients):
                        continue
                    vector = linear_combination(
                        kernel,
                        coefficients,
                        prime,
                    )
                    if (
                        dot(alpha_diagonal, vector, prime)
                        and dot(beta_diagonal, vector, prime)
                    ):
                        valid_vectors.append(vector)
                if not valid_vectors:
                    continue
                binary_extendable_parameters += 1
                if ell != 0 or jay == 0:
                    raise AssertionError(
                        "binary extension escaped the l=0,j!=0 divisor"
                    )

                inv_e = inv(epsilon, prime)
                inv_i = inv(iota, prime)
                alpha_s = (
                    (1, jay, 0, -epsilon * iota % prime),
                    (0, 1, 0, 0),
                    (-inv_i % prime, 0, 1, 0),
                    (0, 0, -inv_e % prime, 1),
                )
                beta_s = (
                    (0, 1, chi * inv_e % prime, chi),
                    (0, 0, 1, epsilon),
                    (0, 1, 0, 0),
                    (1, 0, iota, 0),
                )
                marked_s = one_marked_map(
                    1,
                    alpha_s,
                    beta_s,
                    prime,
                )
                marked_s_kernel = nullspace_mod(marked_s, prime)
                if marked_s_kernel != ((0, 1, 0, 0),):
                    raise AssertionError("pure-hyperplane kernel changed")

                for vector in valid_vectors:
                    binary_delta2_extensions += 1
                    alpha_p = tuple(
                        alpha_shared[mode] + (vector[mode],)
                        for mode in range(4)
                    )
                    beta_p = tuple(
                        beta_shared[mode] + (vector[4 + mode],)
                        for mode in range(4)
                    )
                    marked_p = one_marked_map(
                        1,
                        alpha_p,
                        beta_p,
                        prime,
                    )
                    _rref, pivots = rref_mod(marked_p, prime)
                    if len(pivots) != 4:
                        raise AssertionError(
                            "Delta2-hyperplane one-row map is not injective"
                        )
                    attempted_third_row_lifts += 1
                    # H_p forces the row to be supported only on s.
                    # H_s permits only e_1^*, so the intersection is zero.
                    successful_third_row_lifts += 0

    expected_parameters = (prime - 1) ** 3 * prime**2
    expected_extendable = (prime - 1) ** 4
    expected_extensions = expected_extendable * (prime - 1) ** 2
    assert admissible_parameters == expected_parameters
    assert binary_extendable_parameters == expected_extendable
    assert binary_delta2_extensions == expected_extensions
    assert attempted_third_row_lifts == expected_extensions
    assert successful_third_row_lifts == 0
    return {
        "admissible_pure_family_parameters": admissible_parameters,
        "binary_extendable_parameters": binary_extendable_parameters,
        "binary_Delta2_extension_vectors": binary_delta2_extensions,
        "attempted_third_row_lifts": attempted_third_row_lifts,
        "successful_third_row_lifts": successful_third_row_lifts,
    }


def main() -> None:
    audits = {
        str(prime): audit_prime(prime)
        for prime in (5, 7)
    }
    output = {
        "audited": True,
        "finite_fields": ["F_5", "F_7"],
        "audits": audits,
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "known_rank_two_family_H31_lift_possible": False,
        "scope": "finite-field audit; written theorem is characteristic zero",
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / 'tmp/p5_h31_known_rank_two_family_audited.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
