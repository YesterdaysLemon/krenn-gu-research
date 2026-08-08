#!/usr/bin/env python3
"""Independent modular audit of the eighth component's generic H31 fibre."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py"
)
SAMPLES = {
    11: (1, 2, 7, 3),
    13: (1, 3, 5, 10),
}
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MARKED_ROWS = (0, 1, 3, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows, modulus: int) -> int:
    states = [0] * 16
    states[0] = 1
    for row in rows:
        updated = [0] * 16
        for mask, value in enumerate(states):
            if not value:
                continue
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit == 0:
                    updated[mask | bit] = (
                        updated[mask | bit] + value * entry
                    ) % modulus
        states = updated
    return states[15]


def component_basis(modulus: int):
    a, b, f, phi = SAMPLES[modulus]
    j = (f + b * phi * phi) % modulus
    kappa = phi * (b * f + 1) % modulus
    eta = -(b * f + 1) % modulus
    alpha = (
        (0, 0, 1, -1),
        (-a * f + 1, -a * f - 1, f + phi, f - phi),
        (
            -a * j + eta,
            -a * j - eta,
            j + kappa,
            j - kappa,
        ),
        (1, -1, 0, 0),
    )
    beta = (
        (a + b, a - b, 0, 2),
        (1, 1, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    alpha = tuple(
        tuple(value % modulus for value in row) for row in alpha
    )
    beta = tuple(
        tuple(value % modulus for value in row) for row in beta
    )
    phi_value = (
        a * a * b * f * phi * phi
        + a * a * f * f
        - b * b * f * f
        + b * b * phi * phi
        - b * f
        - 1
    ) % modulus
    assert phi_value == 0
    return (a, b, f, phi), alpha, beta


def extension_coefficients(
    distinguished: int, alpha, beta, extension, modulus: int
):
    common = tuple(
        coordinate for coordinate in range(4)
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
    return {
        bits: permanent(
            tuple(
                beta_p[mode] if bits[mode] else alpha_p[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in BITS4
    }


def extension_matrices(distinguished: int, alpha, beta, modulus: int):
    columns = []
    for coordinate in range(8):
        extension = [0] * 8
        extension[coordinate] = 1
        columns.append(
            extension_coefficients(
                distinguished, alpha, beta, extension, modulus
            )
        )
    mixed_bits = tuple(
        bits
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    mixed = [
        [columns[column][bits] for column in range(8)]
        for bits in mixed_bits
    ]
    diagonals = tuple(
        [columns[column][bits] for column in range(8)]
        for bits in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, *diagonals


def rref_nullspace(matrix, modulus: int):
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots = []
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
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [
            value * inverse % modulus for value in work[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                (left - scale * right) % modulus
                for left, right in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
    free = tuple(column for column in range(columns) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column] % modulus
        basis.append(tuple(vector))
    return len(pivots), tuple(basis)


def projective_directions(dimension: int, modulus: int):
    for pivot in range(dimension):
        for tail in itertools.product(
            range(modulus), repeat=dimension - pivot - 1
        ):
            yield (0,) * pivot + (1,) + tail


def combine(direction, basis, modulus: int):
    return tuple(
        sum(
            direction[index] * basis[index][coordinate]
            for index in range(len(basis))
        )
        % modulus
        for coordinate in range(8)
    )


def dot(row, vector, modulus: int) -> int:
    return sum(
        left * right for left, right in zip(row, vector, strict=True)
    ) % modulus


def determinant_mod(matrix, modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % modulus
            for offset in range(column, len(work)):
                work[row][offset] = (
                    work[row][offset]
                    - scale * work[column][offset]
                ) % modulus
    return result % modulus


def one_marked_map(mode: int, alpha, beta, modulus: int):
    rows = []
    for bits in BITS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    ),
                    modulus,
                )
            )
        rows.append(coefficient_row)
    return rows


def marked_extension(
    distinguished: int,
    extension,
    alpha,
    beta,
    mode: int,
    modulus: int,
):
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row],)
        for row in range(4)
    )
    beta_p = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_p, beta_p, modulus)


def expected_markings(parameters, modulus: int):
    a, b, f, phi = parameters
    common = (
        a * a * b * f * f + 2 * b * b * f + b
    ) % modulus
    coefficient = (1 - a * a * f * f) % modulus
    inverse = pow(coefficient, -1, modulus)
    constant_two = (
        3 * a * a * f * f
        - 2 * b * b * f * f
        - 2 * b * f
        - 3
    ) % modulus
    constant_three = (
        -a * a * f * f
        + 2 * b * b * f * f
        + 2 * b * f
        + 1
    ) % modulus
    t02 = -(common * phi + constant_two) * inverse % modulus
    t03 = -(common * phi + constant_three) * inverse % modulus
    return {
        0: set(),
        1: set(),
        2: {(t02, 0, 0, 0)},
        3: {(t03, 0, 0, 0)},
    }


def obstruction_ratio(parameters, distinguished: int, modulus: int):
    a, b, f, _phi = parameters
    numerator = f * (b * f + 1) * (1 - a * a * f * f)
    denominator = a * a * f + b
    ratio = numerator * pow(denominator % modulus, -1, modulus)
    return ratio % modulus if distinguished == 2 else -ratio % modulus


def audit_modulus(modulus: int):
    parameters, alpha, canonical_beta = component_basis(modulus)
    pure = {
        bits: permanent(
            tuple(
                canonical_beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in BITS4
    }
    assert pure[(1, 1, 1, 1)] == 4 % modulus
    assert all(
        value == 0
        for bits, value in pure.items()
        if bits != (1, 1, 1, 1)
    )

    expected = expected_markings(parameters, modulus)
    observed = {distinguished: set() for distinguished in range(4)}
    extension_checks = 0
    for distinguished in range(4):
        for shifts in itertools.product(range(modulus), repeat=4):
            beta = tuple(
                tuple(
                    (
                        canonical_beta[mode][coordinate]
                        + shifts[mode] * alpha[mode][coordinate]
                    )
                    % modulus
                    for coordinate in range(4)
                )
                for mode in range(4)
            )
            mixed, diagonal_a, diagonal_b = extension_matrices(
                distinguished, alpha, beta, modulus
            )
            rank, kernel = rref_nullspace(mixed, modulus)
            first_restriction = tuple(
                dot(diagonal_a, vector, modulus) for vector in kernel
            )
            second_restriction = tuple(
                dot(diagonal_b, vector, modulus) for vector in kernel
            )
            # Over F_p with p > 2, two proper hyperplanes cannot cover
            # the whole kernel.  Thus both nonzero restricted forms
            # admit a common projective direction with nonzero values.
            if not any(first_restriction) or not any(second_restriction):
                continue
            genuine = []
            for direction in projective_directions(
                len(kernel), modulus
            ):
                extension = combine(direction, kernel, modulus)
                first = dot(diagonal_a, extension, modulus)
                second = dot(diagonal_b, extension, modulus)
                if first and second:
                    genuine.append((extension, first, second))
            assert genuine
            observed[distinguished].add(shifts)
            assert distinguished in (2, 3)
            assert rank == 6
            ratio = obstruction_ratio(
                parameters, distinguished, modulus
            )
            assert ratio
            for extension, first, second in genuine:
                marked = marked_extension(
                    distinguished,
                    extension,
                    alpha,
                    beta,
                    0,
                    modulus,
                )
                determinant = determinant_mod(
                    [
                        [marked[row][column] for column in range(4)]
                        for row in MARKED_ROWS
                    ],
                    modulus,
                )
                assert determinant == (
                    ratio * first * second * second
                ) % modulus
                assert determinant
                extension_checks += 1
    assert observed == expected, (observed, expected)
    return {
        "modulus": modulus,
        "sample_a_b_f_phi": list(parameters),
        "marked_bases_tested": 4 * modulus**4,
        "surviving_markings": sum(len(values) for values in observed.values()),
        "projected_markings": {
            str(key): [list(value) for value in sorted(values)]
            for key, values in observed.items()
        },
        "genuine_projective_extension_directions_checked": extension_checks,
    }


def main() -> None:
    audits = [
        audit_modulus(modulus) for modulus in sorted(SAMPLES)
    ]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "finite-field marked-basis census, subset-DP permanent, "
            "modular kernels, and all-projective-direction minor replay"
        ),
        "moduli": sorted(SAMPLES),
        "audits": audits,
        "generic_marked_fibre_excluded_modularly": True,
        "finite_field_results_are_corroboration_only": True,
        "known_pure_component_orbits_at_least": 8,
        "all_eight_known_components_generic_marked_fibres_excluded": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_disjoint_mixed_star_component_generic_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
