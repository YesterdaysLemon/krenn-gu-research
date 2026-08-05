#!/usr/bin/env python3
"""Independent modular audit of the triangle-component H31 obstruction.

Imports nothing from the primary verifier.  At two generic
finite-field component points it exhausts every marked basis in all
four distinguished frames, recovers exactly the marking loci of the
theorem, checks the ubiquitous reconstruction kernel, and replays the
certificate minors on every genuine projective extension direction.
Finite-field evidence corroborates the characteristic-zero theorem;
it is not itself the proof.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = tuple(
    bits for bits in BITS4 if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMS4 = tuple(itertools.permutations(range(4)))
SAMPLES = ((11, 2, 3), (13, 2, 3))

CERTIFICATE_MINORS = {
    0: (1, ((0, 2, 3, 7), (0, 3, 6, 7))),
    2: (3, ((0, 2, 3, 7), (0, 2, 6, 7), (0, 2, 4, 7))),
    3: (1, ((0, 1, 4, 7),)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family_rows(pp, qq, modulus):
    alpha = (
        (pp * qq + 1, 1, pp, pp * qq + 1),
        (pp, 1, 0, 0),
        (1, 0, -1, 0),
        (0, 0, 1, 1),
    )
    beta = (
        (qq + 1, 0, 1, qq),
        (0, 0, 1, -1),
        (-pp, 1, 0, 0),
        (1, 0, 1, 0),
    )
    reduce_row = lambda row: tuple(value % modulus for value in row)
    return tuple(map(reduce_row, alpha)), tuple(map(reduce_row, beta))


def permanent4(rows, modulus):
    return sum(
        rows[0][pi[0]] * rows[1][pi[1]] * rows[2][pi[2]] * rows[3][pi[3]]
        for pi in PERMS4
    ) % modulus


def perm3(r0, r1, r2, modulus):
    return (
        r0[0] * (r1[1] * r2[2] + r1[2] * r2[1])
        + r0[1] * (r1[0] * r2[2] + r1[2] * r2[0])
        + r0[2] * (r1[0] * r2[1] + r1[1] * r2[0])
    ) % modulus


def rref_nullspace(matrix, modulus):
    work = [[entry % modulus for entry in row] for row in matrix]
    rows, columns = len(work), len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
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
            if row != pivot_row and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(work[row], work[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
    free = tuple(
        column for column in range(columns) if column not in pivots
    )
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column] % modulus
        basis.append(tuple(vector))
    return len(pivots), tuple(basis)


def determinant_mod(matrix, modulus):
    work = [[entry % modulus for entry in row] for row in matrix]
    size = len(work)
    result = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        value = work[column][column]
        result = result * value % modulus
        inverse = pow(value, -1, modulus)
        for row in range(column + 1, size):
            scale = work[row][column] * inverse % modulus
            for offset in range(column, size):
                work[row][offset] = (
                    work[row][offset] - scale * work[column][offset]
                ) % modulus
    return result % modulus


def one_marked_rows(mode, alpha_ext, beta_ext, modulus):
    rows = []
    for bits in BITS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta_ext[other] if bits[bit_index] else alpha_ext[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(i == coordinate) for i in range(4))
            coefficient_row.append(
                permanent4(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    ),
                    modulus,
                )
            )
        rows.append(coefficient_row)
    return rows


def expected_locus(distinguished, pp, qq, modulus):
    if distinguished == 0:
        return {
            (t0, 0, 0, 0) for t0 in range(modulus)
        }
    if distinguished == 1:
        return set()
    if distinguished == 2:
        return (
            {(t0, 0, 0, 0) for t0 in range(modulus)}
            | {(0, 0, t2, 0) for t2 in range(modulus)}
        )
    if distinguished == 3:
        denom1 = (pp * qq + pp + 1) % modulus
        denom2 = (pp * qq + 1) % modulus
        if denom1 == 0 or denom2 == 0:
            return None
        t0 = -(qq + 1) * pow(denom1, -1, modulus) % modulus
        t3 = -denom1 * pow(denom2, -1, modulus) % modulus
        return {(t0, 0, 0, t3)}
    raise ValueError(distinguished)


def audit_sample(modulus, pp, qq):
    alpha, beta0 = family_rows(pp, qq, modulus)
    pure = {
        bits: permanent4(
            tuple(
                beta0[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            ),
            modulus,
        )
        for bits in BITS4
    }
    assert pure[(1, 1, 1, 1)] == (-2) % modulus
    assert all(
        value == 0 for bits, value in pure.items() if bits != (1, 1, 1, 1)
    )

    report = {}
    for distinguished in range(4):
        common = tuple(
            coordinate
            for coordinate in range(4)
            if coordinate != distinguished
        )
        alpha_common = tuple(
            tuple(alpha[mode][coordinate] for coordinate in common)
            for mode in range(4)
        )
        beta0_common = tuple(
            tuple(beta0[mode][coordinate] for coordinate in common)
            for mode in range(4)
        )
        survivors = set()
        genuine_total = 0
        minors_checked = 0
        for shifts in itertools.product(range(modulus), repeat=4):
            beta_common = tuple(
                tuple(
                    (b + shifts[mode] * a) % modulus
                    for b, a in zip(
                        beta0_common[mode], alpha_common[mode]
                    )
                )
                for mode in range(4)
            )
            mixed_rows = []
            for word in MIXED:
                selected = tuple(
                    beta_common[mode] if word[mode]
                    else alpha_common[mode]
                    for mode in range(4)
                )
                row = [0] * 8
                for mode in range(4):
                    others = tuple(
                        selected[other]
                        for other in range(4)
                        if other != mode
                    )
                    slot = mode + (4 if word[mode] else 0)
                    row[slot] = perm3(*others, modulus)
                mixed_rows.append(row)
            first = [0] * 8
            second = [0] * 8
            for mode in range(4):
                others_alpha = tuple(
                    alpha_common[other]
                    for other in range(4)
                    if other != mode
                )
                others_beta = tuple(
                    beta_common[other]
                    for other in range(4)
                    if other != mode
                )
                first[mode] = perm3(*others_alpha, modulus)
                second[4 + mode] = perm3(*others_beta, modulus)

            # ubiquitous reconstruction direction
            reconstruction = tuple(
                alpha[mode][distinguished] for mode in range(4)
            ) + tuple(
                (
                    beta0[mode][distinguished]
                    + shifts[mode] * alpha[mode][distinguished]
                )
                % modulus
                for mode in range(4)
            )
            dot = lambda row, vec: sum(
                left * right for left, right in zip(row, vec)
            ) % modulus
            assert all(
                dot(row, reconstruction) == 0 for row in mixed_rows
            )
            assert dot(first, reconstruction) == 0
            assert dot(second, reconstruction) == (-2) % modulus

            rank, kernel = rref_nullspace(mixed_rows, modulus)
            assert rank <= 7
            if not kernel:
                continue
            genuine = []
            dimension = len(kernel)
            for pivot in range(dimension):
                for tail in itertools.product(
                    range(modulus), repeat=dimension - pivot - 1
                ):
                    coefficients = (0,) * pivot + (1,) + tail
                    vector = tuple(
                        sum(
                            coefficients[index] * kernel[index][coord]
                            for index in range(dimension)
                        )
                        % modulus
                        for coord in range(8)
                    )
                    if dot(first, vector) and dot(second, vector):
                        genuine.append(vector)
            if not genuine:
                continue
            survivors.add(shifts)
            mode, row_sets = CERTIFICATE_MINORS[distinguished]
            for vector in genuine:
                genuine_total += 1
                alpha_ext = tuple(
                    alpha_common[m] + (vector[m],) for m in range(4)
                )
                beta_ext = tuple(
                    beta_common[m] + (vector[4 + m],) for m in range(4)
                )
                marked = one_marked_rows(
                    mode, alpha_ext, beta_ext, modulus
                )
                values = [
                    determinant_mod(
                        [marked[row] for row in rows], modulus
                    )
                    for rows in row_sets
                ]
                assert any(value != 0 for value in values), (
                    distinguished,
                    shifts,
                    vector,
                )
                minors_checked += 1
        expected = expected_locus(distinguished, pp, qq, modulus)
        assert expected is not None, "marking point undefined"
        assert survivors == expected, (
            distinguished,
            sorted(survivors - expected)[:5],
            sorted(expected - survivors)[:5],
        )
        report[str(distinguished)] = {
            "survivor_markings": len(survivors),
            "genuine_directions": genuine_total,
            "certificate_minor_checks": minors_checked,
            "locus_matches_theorem": True,
        }
    return report


def main() -> None:
    reports = {}
    for modulus, pp, qq in SAMPLES:
        reports[f"F_{modulus}(p={pp},q={qq})"] = audit_sample(
            modulus, pp, qq
        )
    output = {
        "audited": True,
        "finite_field_corroboration_only": True,
        "samples": reports,
        "reconstruction_kernel_checked_at_every_marking": True,
        "survivor_loci_match_theorem": True,
        "certificate_minors_cover_every_genuine_direction": True,
        "theorem": THEOREM.name,
        "theorem_sha256": (
            sha256(THEOREM) if THEOREM.exists() else None
        ),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / (
        "p5_h31_all_rank_one_triangle_component_generic_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
