#!/usr/bin/env python3
"""Independent modular audit of the r=0 ninth-component H31 theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

THEOREM = (
    HERE
    / "P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = (
    HERE
    / "verify_p5_h31_embedded_p3_component_r_zero_boundary.py"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inv(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def permanent(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    """Subset-DP permanent, independently of the symbolic verifier."""
    size = len(rows)
    dp = [0] * (1 << size)
    dp[0] = 1
    for row_index in range(size):
        updated = [0] * (1 << size)
        for mask, value in enumerate(dp):
            if value == 0 or mask.bit_count() != row_index:
                continue
            for column in range(size):
                if mask & (1 << column):
                    continue
                updated[mask | (1 << column)] += (
                    value * rows[row_index][column]
                )
        dp = [value % prime for value in updated]
    return dp[-1] % prime


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = inv(work[pivot_row][column], prime)
        work[pivot_row] = [
            entry * scale % prime for entry in work[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column] % prime
            if factor:
                work[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def nullspace_mod(matrix: list[list[int]], prime: int) -> list[list[int]]:
    work = [[entry % prime for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = inv(work[pivot_row][column], prime)
        work[pivot_row] = [
            entry * scale % prime for entry in work[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = tuple(column for column in range(columns) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column] % prime
        basis.append(vector)
    return basis


def dot(left: list[int], right: list[int], prime: int) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True)) % prime


def marked_three_rows(
    aa: int, bb: int, cc: int, prime: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    alpha = (
        (-1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
    )
    beta = (
        (-1 - aa, aa, 1),
        (1 + bb, 1, bb),
        (-1, cc, 1 + cc),
    )
    return tuple(
        tuple(entry % prime for entry in row) for row in alpha
    ), tuple(tuple(entry % prime for entry in row) for row in beta)


def insertion_table(
    cap_s: int, cap_u: int, aa: int, bb: int, cc: int, prime: int
) -> tuple[list[list[int]], list[int], list[int]]:
    alpha, beta = marked_three_rows(aa, bb, cc, prime)
    mode_zero = (1 % prime, cap_s % prime, cap_u % prime, 0)
    table: list[list[int]] = []
    for word in WORDS3:
        row_coefficients = []
        for variable in range(6):
            extension = [0] * 6
            extension[variable] = 1
            rows = []
            for mode in range(3):
                if word[mode]:
                    rows.append(beta[mode] + (extension[3 + mode],))
                else:
                    rows.append(alpha[mode] + (extension[mode],))
            row_coefficients.append(
                permanent((mode_zero, *tuple(rows)), prime)
            )
        table.append(row_coefficients)
    mixed = [
        table[index]
        for index, word in enumerate(WORDS3)
        if word not in ((0, 0, 0), (1, 1, 1))
    ]
    return mixed, table[0], table[-1]


def coefficients4(
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> dict[tuple[int, ...], int]:
    return {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            ),
            prime,
        )
        for word in WORDS4
    }


def one_marked(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    dimension = len(alpha[0])
    result = []
    for word in WORDS3:
        selected: list[tuple[int, ...] | None] = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if word[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(dimension):
            basis = tuple(
                int(index == coordinate) for index in range(dimension)
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
        result.append(coefficient_row)
    return result


def phi(
    cap_s: int,
    cap_u: int,
    aa: int,
    bb: int,
    cc: int,
    prime: int,
) -> int:
    return (
        cap_s
        * (
            cap_u
            * (
                (cap_s - cap_u) * (aa + 1) * (bb + 1)
                - aa * (bb + 1)
                + 1
            )
            + bb * (cap_s + 1)
        )
        + cc
        * (
            cap_s * bb * (cap_s + cap_u + 1)
            + cap_u * aa * (1 - cap_s - cap_u)
        )
    ) % prime


def solve_phi(
    cap_s: int, cap_u: int, aa: int, bb: int, prime: int
) -> int:
    value0 = phi(cap_s, cap_u, aa, bb, 0, prime)
    value1 = (phi(cap_s, cap_u, aa, bb, 1, prime) - value0) % prime
    assert value1
    return -value0 * inv(value1, prime) % prime


def audit_sample(
    name: str,
    parameters: tuple[int, int, int, int, int],
    prime: int,
    *,
    expect_binary: bool = True,
) -> dict[str, object]:
    cap_s, cap_u, aa, bb, cc = (
        parameter % prime for parameter in parameters
    )
    mixed, alpha_row, beta_row = insertion_table(
        cap_s, cap_u, aa, bb, cc, prime
    )
    kernel_basis = nullspace_mod(mixed, prime)
    genuine = next(
        (
            vector
            for vector in kernel_basis
            if dot(alpha_row, vector, prime)
        ),
        None,
    )
    if not expect_binary:
        assert genuine is None
        return {
            "binary_direction": False,
            "mixed_rank": rank_mod(mixed, prime),
        }
    assert genuine is not None, (name, parameters, kernel_basis)
    alpha_diagonal = dot(alpha_row, genuine, prime)
    beta_beta_beta = dot(beta_row, genuine, prime)
    assert alpha_diagonal

    last_alpha, last_beta = marked_three_rows(aa, bb, cc, prime)
    x0 = beta_beta_beta * inv(2, prime) % prime
    alpha5 = (
        (0, 1, cap_s, cap_u, x0),
        *tuple(
            (0, *last_alpha[mode], genuine[mode] % prime)
            for mode in range(3)
        ),
    )
    beta5 = (
        (1, 0, 0, 0, 1),
        *tuple(
            (0, *last_beta[mode], genuine[3 + mode] % prime)
            for mode in range(3)
        ),
    )
    neighboring_alpha = tuple(
        tuple(row[coordinate] for coordinate in (1, 2, 3, 4))
        for row in alpha5
    )
    neighboring_beta = tuple(
        tuple(row[coordinate] for coordinate in (1, 2, 3, 4))
        for row in beta5
    )
    neighboring = coefficients4(
        neighboring_alpha, neighboring_beta, prime
    )
    assert neighboring[(0, 0, 0, 0)] == alpha_diagonal
    assert neighboring[(1, 1, 1, 1)] == (-2) % prime
    assert all(
        value == 0
        for word, value in neighboring.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )

    pure_alpha = tuple(tuple(row[:4]) for row in alpha5)
    pure_beta = tuple(tuple(row[:4]) for row in beta5)
    pure = coefficients4(pure_alpha, pure_beta, prime)
    assert pure[(1, 1, 1, 1)] == (-2) % prime
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    excluding_modes = []
    for mode in (1, 2, 3):
        neighboring_map = one_marked(
            mode, neighboring_alpha, neighboring_beta, prime
        )
        pure_map = one_marked(mode, pure_alpha, pure_beta, prime)
        if rank_mod(neighboring_map, prime) == 4 and any(
            row[0] % prime for row in pure_map
        ):
            excluding_modes.append(mode)
    assert excluding_modes, (name, parameters, genuine)
    return {
        "binary_direction": True,
        "alpha_diagonal": alpha_diagonal,
        "mixed_nullity": len(kernel_basis),
        "excluding_modes": excluding_modes,
    }


def main() -> None:
    audits: dict[str, object] = {}
    for prime in (101, 103):
        half = inv(2, prime)
        signed_samples = (
            ("S0_a0", (0, 2, 0, 2, 3)),
            ("S0_c0", (0, 2, 2, 3, 0)),
            ("U0_b0", (2, 0, 2, 0, 3)),
            ("U0_cm1", (2, 0, 2, 3, -1)),
            ("I1", (2, 1, -2, -half, 3)),
            ("I2", (2, 1, 3, -half, 0)),
            ("I3", (2, 1, -2, 3, -1)),
            ("J1", (2, -1, -2, 0, 3)),
            ("J2", (2, -1, -2, 3, -2)),
            ("J3", (2, -1, 3, -1, -2)),
            ("K1", (2, -3, 0, -3 * half, 3)),
            ("K2", (2, -3, 3, -3 * half, 2)),
            ("K3", (2, -3, -1, 3, 2)),
            ("P1", (0, 1, 0, 2, 0)),
            ("P2", (0, 1, 0, 0, 2)),
            ("P3", (0, 1, 2, -1, 0)),
            ("Q1", (-1, 0, 2, 0, -1)),
            ("Q2", (-1, 0, 0, 0, 2)),
            ("Q3", (-1, 0, -1, 2, -1)),
            ("R1", (0, 0, 0, 0, 2)),
            ("R2", (0, 0, 2, 0, 0)),
            ("R3", (0, 0, 0, 2, -1)),
        )
        prime_result: dict[str, object] = {}
        for name, parameters in signed_samples:
            prime_result[name] = audit_sample(name, parameters, prime)

        residual_starts = (
            ("residual_b_generic", (2, 3, 4, 5)),
            ("residual_a_generic", (2, 3, 2, -1)),
            ("residual_last_cover", (2, 3, -1, -1)),
        )
        for name, (cap_s, cap_u, aa, bb) in residual_starts:
            value0 = phi(cap_s, cap_u, aa, bb, 0, prime)
            value1 = (
                phi(cap_s, cap_u, aa, bb, 1, prime) - value0
            ) % prime
            if value1:
                cc = solve_phi(cap_s, cap_u, aa, bb, prime)
            else:
                assert value0 == 0
                cc = 3
            parameters = (cap_s, cap_u, aa, bb, cc)
            assert phi(*parameters, prime) == 0
            d1 = (cap_s - cap_u - 1) % prime
            d2 = (cap_s + cap_u - 1) % prime
            d3 = (cap_s + cap_u + 1) % prime
            assert cap_s * cap_u * d1 * d2 * d3 % prime
            prime_result[name] = audit_sample(name, parameters, prime)

        prime_result["empty_0m1"] = audit_sample(
            "empty_0m1", (0, -1, -1, 2, -1), prime, expect_binary=False
        )
        prime_result["empty_10"] = audit_sample(
            "empty_10", (1, 0, 2, -1, 0), prime, expect_binary=False
        )
        audits[str(prime)] = prime_result

    output = {
        "verified": True,
        "method": (
            "independent subset-DP permanents, modular nullspaces, "
            "binary slices, and one-marked ranks"
        ),
        "finite_field_audit_is_theorem": False,
        "primes": audits,
        "r_zero_A_nonzero_H31_fibre_empty": True,
        "whole_affine_B_nonzero_ninth_component_H31_fibre_empty": True,
        "global_problem_resolved": False,
        "dependencies": {
            THEOREM.name: sha256(THEOREM),
            PRIMARY.name: sha256(PRIMARY),
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
