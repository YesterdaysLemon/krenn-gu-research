#!/usr/bin/env python3
"""Independent finite-field audit of the complete marked-basis theorem."""

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
THEOREM = ROOT / "P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md"
PRIMARY = ROOT / "verify_p5_h31_marked_basis_fibre_classification.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent3(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    return (
        rows[0][0] * rows[1][1] * rows[2][2]
        + rows[0][0] * rows[1][2] * rows[2][1]
        + rows[0][1] * rows[1][0] * rows[2][2]
        + rows[0][1] * rows[1][2] * rows[2][0]
        + rows[0][2] * rows[1][0] * rows[2][1]
        + rows[0][2] * rows[1][1] * rows[2][0]
    ) % prime


def permanent4(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    states = [0] * 16
    states[0] = 1
    for row in rows:
        updated = [0] * 16
        for mask, value in enumerate(states):
            if not value:
                continue
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    updated[mask | (1 << column)] += value * entry
        states = [value % prime for value in updated]
    return states[15]


def rref_mod(
    matrix: list[list[int]],
    prime: int,
) -> tuple[list[list[int]], tuple[int, ...]]:
    if not matrix:
        return [], ()
    work = [[entry % prime for entry in row] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [
            entry * inverse % prime for entry in work[pivot_row]
        ]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (left - scale * right) % prime
                    for left, right in zip(
                        work[row],
                        work[pivot_row],
                        strict=True,
                    )
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, tuple(pivot_columns)


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    return len(rref_mod(matrix, prime)[1])


def kernel_mod(matrix: list[list[int]], prime: int) -> list[list[int]]:
    reduced, pivots = rref_mod(matrix, prime)
    columns = len(matrix[0])
    free = tuple(column for column in range(columns) if column not in pivots)
    basis: list[list[int]] = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % prime
        basis.append(vector)
    return basis


def dot(left: list[int], right: list[int], prime: int) -> int:
    return sum(
        a * b for a, b in zip(left, right, strict=True)
    ) % prime


def family_rows(
    L: int,
    Q: int,
    C: int,
    shifts: tuple[int, ...],
    prime: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    D = (C + L) % prime
    A = (1 + L * Q) % prime
    alpha = (
        (1, Q, 0, -A),
        (L, 1, -L, -L),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    canonical = (
        (0, 1, D, C),
        (0, 0, 1, 1),
        (0, 1, 0, L),
        (1, 0, 1, 0),
    )
    beta = tuple(
        tuple(
            (
                canonical[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            % prime
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    alpha = tuple(
        tuple(entry % prime for entry in row)
        for row in alpha
    )
    return alpha, beta


def coefficient_rows(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[list[list[int]], list[int], list[int]]:
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    rows: list[list[int]] = []
    for bits in range(16):
        selected = tuple(
            beta[mode] if bits & (1 << mode) else alpha[mode]
            for mode in range(4)
        )
        row = [0] * 8
        for mode in range(4):
            remaining = tuple(
                tuple(selected[other][coordinate] for coordinate in common)
                for other in range(4)
                if other != mode
            )
            value = permanent3(remaining, prime)
            target = 4 + mode if bits & (1 << mode) else mode
            row[target] = value
        rows.append(row)
    return rows[1:15], rows[0], rows[15]


def binary_extension_data(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[list[list[int]], list[int], list[int], list[list[int]]]:
    mixed, diagonal_a, diagonal_b = coefficient_rows(
        distinguished,
        alpha,
        beta,
        prime,
    )
    kernel = kernel_mod(mixed, prime)
    return mixed, diagonal_a, diagonal_b, kernel


def has_binary_extension(
    diagonal_a: list[int],
    diagonal_b: list[int],
    kernel: list[list[int]],
    prime: int,
) -> bool:
    # Over F_5 and F_7, a finite-dimensional vector space is not the
    # union of two proper hyperplanes.
    return (
        any(dot(diagonal_a, vector, prime) for vector in kernel)
        and any(dot(diagonal_b, vector, prime) for vector in kernel)
    )


def projective_vectors(
    dimension: int,
    prime: int,
) -> list[tuple[int, ...]]:
    vectors: list[tuple[int, ...]] = []
    for first in range(dimension):
        for tail in itertools.product(
            range(prime),
            repeat=dimension - first - 1,
        ):
            vectors.append((0,) * first + (1,) + tail)
    return vectors


def linear_combination(
    coefficients: tuple[int, ...],
    basis: list[list[int]],
    prime: int,
) -> tuple[int, ...]:
    return tuple(
        sum(
            coefficient * basis[index][coordinate]
            for index, coefficient in enumerate(coefficients)
        )
        % prime
        for coordinate in range(8)
    )


def extended_rows(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    extension: tuple[int, ...],
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (extension[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode in range(4)
    )
    return alpha_p, beta_p


def marked_matrix(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    other_modes = tuple(other for other in range(4) if other != mode)
    result: list[list[int]] = []
    for bits in range(8):
        selected = {
            other: (
                beta[other]
                if bits & (1 << index)
                else alpha[other]
            )
            for index, other in enumerate(other_modes)
        }
        coefficient_row = []
        for coordinate in range(4):
            remaining_columns = tuple(
                column for column in range(4) if column != coordinate
            )
            permanent_rows = tuple(
                tuple(
                    selected[other][column]
                    for column in remaining_columns
                )
                for other in other_modes
            )
            coefficient_row.append(permanent3(permanent_rows, prime))
        result.append(coefficient_row)
    return result


def pure_coefficients(
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[int, ...]:
    return tuple(
        permanent4(
            tuple(
                beta[mode]
                if bits & (1 << mode)
                else alpha[mode]
                for mode in range(4)
            ),
            prime,
        )
        for bits in range(16)
    )


def projection_generators(
    distinguished: int,
    c: int,
    q: int,
    shift: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    s0, s1, s2, s3 = shift
    if distinguished == 0:
        generators = (
            s3,
            s2 * c + q * c - s1 + q + 1,
            s1 * c - s2 * c + s1,
            s0 * c - s2 * c + q * c + q + c + 2,
            s2 * q + s2,
            s1 * q + s1,
            s0 * q + s0 - s1 + 1,
            s1 * s2 - s2,
            s0 * s2 - s2,
            s1 * s1 - s1,
            s0 * s1 - s1,
            (q + 1) * ((c + 1) * q + 1),
        )
    elif distinguished == 1:
        generators = (
            q * c + s0 + q - c,
            (2 * c + 1) * s3,
            (2 * c + 1) * s2,
            (2 * c + 1) * s1 + 5 * c * s2
            + 2 * s2 + s3 - c - 1,
            (2 * c + 1) * s0 - 2 * c * c - 3 * c - 1,
            s3 * q - 6 * c * s1 - 9 * c * s2
            + 2 * s0 - 3 * s1 - 4 * s2 + c + 1,
            s2 * q - 2 * s3 * q + 4 * c * s1
            + 4 * c * s2 - 2 * s0 + 2 * s1
            + 3 * s2 - 2 * s3,
            3 * s1 * q + 3 * s2 * q - 6 * c * s1
            - 3 * c * s2 - 10 * c * s3 + 6 * s0
            + 3 * s1 + s3 - 3 * c - 6,
            s0 * q + 2 * c * s1 + 2 * c * s2 + c * s3
            + s0 + s1 + s2 + s3 - 2 * c - 1,
            s3 * s3 - s3,
            s2 * s3 - s3,
            s1 * s3,
            2 * s0 * s3 - 2 * s0 + s2 - 2 * s3
            + 2 * c + 2,
            s2 * s2 + 2 * c * s2 + 2 * s2 - 2 * s3,
            s1 * s2 - s2 + s3,
            2 * s0 * s2 - 2 * s0 + s2 - 2 * s3
            + 2 * c + 2,
            4 * s0 * s1 - 2 * s1 - 3 * s2 + 4 * s3
            - 2 * c - 2,
            4 * s0 * s0 - 4 * c * c - s2 + s3
            - 8 * c - 4,
        )
    elif distinguished == 2:
        generators = (
            s3,
            s1,
            s2 * q + s2 - 1,
            s0 * s2 * c + s0 * q * c + s0 * q - s0 * c
            - s2 * c + c + 1,
            (s0 * q + 1) * ((c + 1) * q + 1),
        )
    else:
        generators = (
            s1,
            s2 * c - s3 * c - s3,
            s3 * q,
            s2 * q,
            s0 * q - s3 + 1,
            s3 * s3 - s3,
            s2 * s3 - s2,
            s0 * s3 + s3,
            s0 * s2 + s2,
        )
    return tuple(generator % prime for generator in generators)


def predicted_l1(
    distinguished: int,
    c: int,
    q: int,
    prime: int,
) -> set[tuple[int, ...]]:
    one = 1 % prime
    D = (c + one) % prime
    A = (one + q) % prime
    B = (one + D * q) % prime
    result: set[tuple[int, ...]] = set()
    if distinguished == 0:
        if A == 0 and c:
            result.add((
                1,
                1,
                D * pow(c, -1, prime) % prime,
                0,
            ))
        if B == 0 and c:
            result.add((
                -D * pow(c, -1, prime) % prime,
                0,
                0,
                0,
            ))
    elif distinguished == 1:
        R = (one + 2 * c) % prime
        if B == 0 and R:
            result.add((
                D,
                D * pow(R, -1, prime) % prime,
                0,
                0,
            ))
        if R == 0:
            if q == -2 % prime:
                result.add((pow(2, -1, prime), 0, 1, 1))
            if q == -1 % prime:
                result.add((0, 1, -1 % prime, 0))
            if q == 0:
                result.add((-pow(2, -1, prime) % prime, 0, 1, 1))
    elif distinguished == 2:
        if q and A and B:
            result.add((
                -pow(q, -1, prime) % prime,
                0,
                pow(A, -1, prime),
                0,
            ))
        if A and B == 0:
            inverse_a = pow(A, -1, prime)
            result.update(
                (T, 0, inverse_a, 0)
                for T in range(prime)
            )
    else:
        if q:
            result.add((-pow(q, -1, prime) % prime, 0, 0, 0))
        elif c:
            result.add((
                -1 % prime,
                0,
                D * pow(c, -1, prime) % prime,
                1,
            ))
    return result


def predicted_l0(
    distinguished: int,
    q: int,
    prime: int,
) -> set[tuple[int, ...]]:
    if distinguished == 0:
        return (
            {(T, 0, 0, 0) for T in range(prime)}
            if q
            else set()
        )
    if distinguished == 1:
        return set()
    if distinguished == 2:
        return {(T, 0, 0, 0) for T in range(prime)}
    if q:
        return (
            {(T, 0, 0, 0) for T in range(prime)}
            | {(0, 0, 0, S) for S in range(prime)}
        )
    return {(0, 0, 0, 1)}


def audit_marking(
    distinguished: int,
    L: int,
    Q: int,
    C: int,
    shift: tuple[int, ...],
    prime: int,
) -> tuple[int, int]:
    alpha, beta = family_rows(L, Q, C, shift, prime)
    pure = pure_coefficients(alpha, beta, prime)
    D = (C + L) % prime
    assert pure[15] == 2 * D % prime
    assert all(not coefficient for coefficient in pure[:15])

    _, diagonal_a, diagonal_b, kernel = binary_extension_data(
        distinguished,
        alpha,
        beta,
        prime,
    )
    assert has_binary_extension(
        diagonal_a,
        diagonal_b,
        kernel,
        prime,
    )
    pure_transverse = tuple(
        any(
            row[distinguished]
            for row in marked_matrix(mode, alpha, beta, prime)
        )
        for mode in range(4)
    )
    projective_checked = 0
    admissible_checked = 0
    for coefficients in projective_vectors(len(kernel), prime):
        extension = linear_combination(coefficients, kernel, prime)
        projective_checked += 1
        if not (
            dot(diagonal_a, list(extension), prime)
            and dot(diagonal_b, list(extension), prime)
        ):
            continue
        admissible_checked += 1
        alpha_p, beta_p = extended_rows(
            distinguished,
            alpha,
            beta,
            extension,
        )
        assert any(
            pure_transverse[mode]
            and rank_mod(
                marked_matrix(mode, alpha_p, beta_p, prime),
                prime,
            )
            == 4
            for mode in range(4)
        )
    assert admissible_checked
    return projective_checked, admissible_checked


def main() -> None:
    projection_counts: dict[str, dict[str, int]] = {}
    fibre_counts: dict[str, dict[str, int]] = {}
    total_projective_extensions = 0
    total_admissible_extensions = 0
    total_markings = 0
    l0_closure_artifacts = 0

    for prime in (5, 7):
        projection_by_q = {str(q): 0 for q in range(4)}
        # Exhaust the exact normalized L=1 elimination varieties.
        for c in range(prime):
            if c == -1 % prime:
                continue
            for q in range(prime):
                predicted = {
                    distinguished: predicted_l1(
                        distinguished,
                        c,
                        q,
                        prime,
                    )
                    for distinguished in range(4)
                }
                for shift in itertools.product(range(prime), repeat=4):
                    for distinguished in range(4):
                        on_projection = not any(
                            projection_generators(
                                distinguished,
                                c,
                                q,
                                shift,
                                prime,
                            )
                        )
                        expected = shift in predicted[distinguished]
                        assert on_projection == expected, (
                            prime,
                            distinguished,
                            c,
                            q,
                            shift,
                            on_projection,
                            expected,
                        )
                        if on_projection:
                            projection_by_q[str(distinguished)] += 1

        field_markings: set[
            tuple[int, int, int, int, tuple[int, ...]]
        ] = set()
        for c in range(prime):
            if c == -1 % prime:
                continue
            for q in range(prime):
                for distinguished in range(4):
                    for shift in predicted_l1(
                        distinguished,
                        c,
                        q,
                        prime,
                    ):
                        field_markings.add(
                            (distinguished, 1, q, c, shift)
                        )

        # L=0,C=1.  Audit the constructible correction to the four
        # projection closures directly from the mixed kernels.
        for q in range(prime):
            for distinguished in range(4):
                predicted = predicted_l0(
                    distinguished,
                    q,
                    prime,
                )
                closure = (
                    {(T, 0, 0, 0) for T in range(prime)}
                    if distinguished in (0, 2)
                    else (
                        set()
                        if distinguished == 1
                        else (
                            {(T, 0, 0, 0) for T in range(prime)}
                            | {(0, 0, 0, S) for S in range(prime)}
                        )
                    )
                )
                for shift in closure:
                    alpha, beta = family_rows(
                        0,
                        q,
                        1,
                        shift,
                        prime,
                    )
                    _, da, db, kernel = binary_extension_data(
                        distinguished,
                        alpha,
                        beta,
                        prime,
                    )
                    actual = has_binary_extension(da, db, kernel, prime)
                    assert actual == (shift in predicted)
                    if not actual:
                        l0_closure_artifacts += 1
                for shift in predicted:
                    field_markings.add(
                        (distinguished, 0, q, 1, shift)
                    )

        projective_field = 0
        admissible_field = 0
        for distinguished, L, Q, C, shift in sorted(field_markings):
            projective, admissible = audit_marking(
                distinguished,
                L,
                Q,
                C,
                shift,
                prime,
            )
            projective_field += projective
            admissible_field += admissible
        total_markings += len(field_markings)
        total_projective_extensions += projective_field
        total_admissible_extensions += admissible_field
        projection_counts[f"F_{prime}"] = projection_by_q
        fibre_counts[f"F_{prime}"] = {
            "surviving_markings": len(field_markings),
            "projective_kernel_directions": projective_field,
            "admissible_binary_extensions": admissible_field,
        }

    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "finite_fields": ["F_5", "F_7"],
        "normalized_L1_projection_point_counts": projection_counts,
        "fibre_counts": fibre_counts,
        "surviving_markings_checked": total_markings,
        "projective_kernel_directions_checked": (
            total_projective_extensions
        ),
        "admissible_binary_extensions_checked": (
            total_admissible_extensions
        ),
        "L0_projection_closure_artifacts_rejected": (
            l0_closure_artifacts
        ),
        "all_admissible_extensions_ternarily_excluded": True,
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "method": (
            "exhaustive normalized elimination-variety evaluation, "
            "independent permanent expansion, modular kernels, and "
            "all projective extensions on surviving fibres"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_marked_basis_fibre_classification_audit.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
