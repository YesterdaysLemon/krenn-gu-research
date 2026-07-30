#!/usr/bin/env python3
"""Independent finite-field audit of the generic 1+3 H31 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h31_one_three_component_generic_obstruction.py"
MODULI = (5, 7)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MARKED_WORDS = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent3(rows, modulus: int) -> int:
    return sum(
        rows[0][permutation[0]]
        * rows[1][permutation[1]]
        * rows[2][permutation[2]]
        for permutation in PERMUTATIONS3
    ) % modulus


def matrix_rank_mod(matrix: list[list[int]], modulus: int) -> int:
    if not matrix:
        return 0
    work = [[entry % modulus for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, modulus)
        work[rank] = [
            entry * inverse % modulus for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def nullspace_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    work = [[entry % modulus for entry in row] for row in matrix]
    row = 0
    pivots = []
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], -1, modulus)
        work[row] = [entry * inverse % modulus for entry in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            scale = work[other][column]
            if scale:
                work[other] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(
                        work[other], work[row], strict=True
                    )
                ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    free = [
        column for column in range(len(work[0])) if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [0] * len(work[0])
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[pivot_row][free_column] % modulus
        basis.append(vector)
    return basis


def projective_vectors(dimension: int, modulus: int):
    for pivot in range(dimension):
        for tail in itertools.product(
            range(modulus), repeat=dimension - pivot - 1
        ):
            yield (0,) * pivot + (1,) + tail


def raw_branch_planes(
    branch: str, S: int, D: int, G: int, modulus: int
):
    T = {
        "L1": -D + G + S,
        "L2": D + G - S,
        "L3": -D - G - S,
    }[branch]
    P = G - T
    Q = D - S
    planes = (
        [[2, P + Q, Q - P, 0], [0, 0, 1, 1]],
        [[0, 1, -1, 0], [1, 0, S, D]],
        [[1, 0, G, T], [0, 1, 0, -1]],
        [[0, 1, 1, 0], [0, 1, 0, 1]],
    )
    return tuple(
        [[entry % modulus for entry in row] for row in plane]
        for plane in planes
    )


def linear_combination(left, right, a, b, modulus: int):
    return [
        (a * left[index] + b * right[index]) % modulus
        for index in range(4)
    ]


def canonical_basis_mod(
    branch: str, S: int, D: int, G: int, modulus: int
):
    planes = raw_branch_planes(branch, S, D, G, modulus)
    row = lambda mode, index: planes[mode][index]
    if branch == "L1":
        alpha = (
            linear_combination(
                row(0, 0), row(0, 1), G + S, -2 * D * G, modulus
            ),
            row(1, 0),
            row(2, 1),
            linear_combination(row(3, 0), row(3, 1), 1, -1, modulus),
        )
    elif branch == "L2":
        alpha = (
            linear_combination(
                row(0, 0),
                row(0, 1),
                D + G,
                -2 * D * (D + G - S),
                modulus,
            ),
            row(1, 0),
            row(2, 1),
            linear_combination(row(3, 0), row(3, 1), 1, -1, modulus),
        )
    else:
        alpha = (
            row(0, 1),
            row(1, 0),
            row(2, 1),
            linear_combination(
                row(3, 0),
                row(3, 1),
                G * (D + G + S),
                D * S,
                modulus,
            ),
        )
    beta = (row(0, 0), row(1, 1), row(2, 0), row(3, 0))
    return alpha, beta


def shifted_basis_mod(alpha, beta, shifts, modulus: int):
    return tuple(
        [
            (
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            % modulus
            for coordinate in range(4)
        ]
        for mode in range(4)
    )


def extension_row_mod(
    word, distinguished: int, alpha, beta, modulus: int
) -> list[int]:
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    selected = [
        beta[mode] if word[mode] else alpha[mode] for mode in range(4)
    ]
    row = [0] * 8
    for mode in range(4):
        other_rows = [
            [selected[other][coordinate] for coordinate in common]
            for other in range(4)
            if other != mode
        ]
        column = mode + (4 if word[mode] else 0)
        row[column] = permanent3(other_rows, modulus)
    return row


def binary_matrices_mod(
    distinguished: int, alpha, beta, modulus: int
):
    rows = {
        word: extension_row_mod(
            word, distinguished, alpha, beta, modulus
        )
        for word in WORDS
    }
    mixed = [
        rows[word]
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    return mixed, rows[(0, 0, 0, 0)], rows[(1, 1, 1, 1)]


def dot(left, right, modulus: int) -> int:
    return sum(
        a * b for a, b in zip(left, right, strict=True)
    ) % modulus


def combine_basis(basis, coefficients, modulus: int) -> list[int]:
    return [
        sum(
            coefficients[index] * basis[index][coordinate]
            for index in range(len(basis))
        )
        % modulus
        for coordinate in range(len(basis[0]))
    ]


def extended_rows(
    distinguished: int, alpha, beta, extension, modulus: int
):
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_extended = tuple(
        [alpha[mode][coordinate] for coordinate in common]
        + [extension[mode] % modulus]
        for mode in range(4)
    )
    beta_extended = tuple(
        [beta[mode][coordinate] for coordinate in common]
        + [extension[4 + mode] % modulus]
        for mode in range(4)
    )
    return alpha_extended, beta_extended


def one_marked_map_mod(mode: int, alpha, beta, modulus: int):
    rows = []
    for bits in MARKED_WORDS:
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
        for candidate_column in range(4):
            remaining_columns = tuple(
                column
                for column in range(4)
                if column != candidate_column
            )
            other_rows = [
                [
                    selected[other][column]
                    for column in remaining_columns
                ]
                for other in range(4)
                if other != mode
            ]
            coefficient_row.append(permanent3(other_rows, modulus))
        rows.append(coefficient_row)
    return rows


def audit_branch(
    branch: str,
    parameters: tuple[int, int, int],
    modulus: int,
) -> dict:
    S, D, G = parameters
    alpha, canonical_beta = canonical_basis_mod(
        branch, S, D, G, modulus
    )
    assert all(matrix_rank_mod([alpha[m], canonical_beta[m]], modulus) == 2
               for m in range(4))

    survivor_markings = {q: 0 for q in range(4)}
    genuine_directions = {q: 0 for q in range(4)}
    injective_directions = {q: 0 for q in range(4)}
    transverse_checks = {q: 0 for q in range(4)}

    for shifts in itertools.product(range(modulus), repeat=4):
        beta = shifted_basis_mod(
            alpha, canonical_beta, shifts, modulus
        )
        for distinguished in range(4):
            mixed, diagonal_a, diagonal_b = binary_matrices_mod(
                distinguished, alpha, beta, modulus
            )
            kernel = nullspace_mod(mixed, modulus)
            marking_genuine = 0
            for projective in projective_vectors(len(kernel), modulus):
                extension = combine_basis(kernel, projective, modulus)
                if (
                    dot(diagonal_a, extension, modulus) == 0
                    or dot(diagonal_b, extension, modulus) == 0
                ):
                    continue
                marking_genuine += 1
                genuine_directions[distinguished] += 1
                neighbour_alpha, neighbour_beta = extended_rows(
                    distinguished,
                    alpha,
                    beta,
                    extension,
                    modulus,
                )
                marked = one_marked_map_mod(
                    0, neighbour_alpha, neighbour_beta, modulus
                )
                assert matrix_rank_mod(marked, modulus) == 4
                injective_directions[distinguished] += 1

                pure_marked = one_marked_map_mod(
                    0, alpha, beta, modulus
                )
                assert any(
                    pure_marked[row][distinguished] != 0
                    for row in range(8)
                )
                transverse_checks[distinguished] += 1
            if marking_genuine:
                survivor_markings[distinguished] += 1
                assert len(kernel) == 2
                assert marking_genuine == modulus - 1

    if branch == "L1":
        assert survivor_markings == {0: 0, 1: 0, 2: 1, 3: 1}, (
            modulus,
            branch,
            survivor_markings,
            genuine_directions,
        )
        assert genuine_directions == {
            0: 0,
            1: 0,
            2: modulus - 1,
            3: modulus - 1,
        }
    elif branch == "L2":
        assert survivor_markings == {
            0: 0,
            1: 0,
            2: modulus,
            3: modulus,
        }, (modulus, branch, survivor_markings, genuine_directions)
        assert genuine_directions == {
            0: 0,
            1: 0,
            2: modulus * (modulus - 1),
            3: modulus * (modulus - 1),
        }
    else:
        assert survivor_markings == {0: 0, 1: 0, 2: 0, 3: 0}, (
            modulus,
            branch,
            survivor_markings,
            genuine_directions,
        )
        assert genuine_directions == {0: 0, 1: 0, 2: 0, 3: 0}
    assert injective_directions == genuine_directions
    assert transverse_checks == genuine_directions

    return {
        "parameters_S_D_G": list(parameters),
        "markings_checked": 4 * modulus**4,
        "survivor_markings_by_distinguished_coordinate": {
            str(key): value for key, value in survivor_markings.items()
        },
        "genuine_projective_extension_directions": sum(
            genuine_directions.values()
        ),
        "injective_marked_map_directions": sum(
            injective_directions.values()
        ),
        "transverse_pure_checks": sum(transverse_checks.values()),
    }


def audit_modulus(modulus: int) -> dict:
    branch_parameters = {
        "L1": (1, 2, 2),
        "L2": (1, 2, 1),
        "L3": (1, 2, 2),
    }
    audits = {
        branch: audit_branch(branch, parameters, modulus)
        for branch, parameters in branch_parameters.items()
    }
    return {
        "modulus": modulus,
        "branches": audits,
        "total_markings_checked": sum(
            audit["markings_checked"] for audit in audits.values()
        ),
        "total_genuine_projective_extension_directions": sum(
            audit["genuine_projective_extension_directions"]
            for audit in audits.values()
        ),
        "all_genuine_directions_injective_and_transverse": True,
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "DP trilinear permanent, exhaustive marked bases, "
            "projective kernel directions, and modular marked-map ranks"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "total_markings_checked": sum(
            audit["total_markings_checked"] for audit in audits
        ),
        "total_genuine_projective_extension_directions": sum(
            audit["total_genuine_projective_extension_directions"]
            for audit in audits
        ),
        "generic_marked_fibre_pattern_replayed": True,
        "all_extension_obstruction_replayed": True,
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
        / "p5_h31_one_three_component_generic_obstruction_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
