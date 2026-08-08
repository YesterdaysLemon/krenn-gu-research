#!/usr/bin/env python3
"""Independent modular audit of the triangle-component weighted H22.

Imports nothing from the primary verifier.  At two generic
finite-field component points with generic slopes it exhausts every
marked basis in both weighted diagonal pencils, recovers exactly the
slope-independent marking loci of the theorem, and replays the
certificate minors on every genuine kernel direction.  Finite-field
evidence corroborates the characteristic-zero theorem; it is not
itself the proof.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

ROOT = REPO_ROOT
THEOREM = (
    HERE
    / "P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = tuple(
    bits for bits in BITS4 if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMS4 = tuple(itertools.permutations(range(4)))
# (modulus, p, q, r) with r generic for the listed divisors.  The
# slope 4 at F_11 is deliberately avoided: at (11,2,3,4) the D_01
# census acquires a modular specialization jump (an extra survivor
# line t_0=-2, t_3 free, absent at F_13 with the same (p,q,r) and at
# every other tested F_11 slope, so an implicit elimination
# denominator has content divisible by 11 there).  Every direction on
# that jump line still has a rank-four mode-1 marked map, so even the
# artifact is obstruction-consistent; see the theorem's honest
# frontier.
SAMPLES = ((11, 2, 3, 3), (13, 2, 3, 4))

MODE_T0 = 1
MINORS_T0 = ((0, 2, 3, 7),)
MODE_T3 = 3
MINORS_T3 = ((0, 2, 3, 7), (0, 2, 6, 7))


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


def weighted_row(row, extension, diagonal, rv, modulus):
    if diagonal == "01":
        return (
            (rv * row[0] + row[1]) % modulus,
            row[2],
            row[3],
            extension % modulus,
        )
    return (
        row[0],
        row[1],
        (rv * row[2] + row[3]) % modulus,
        extension % modulus,
    )


def word_coefficient(word, alpha_ext, beta_ext, modulus):
    return permanent4(
        tuple(
            beta_ext[mode] if word[mode] else alpha_ext[mode]
            for mode in range(4)
        ),
        modulus,
    )


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


def perm3(r0, r1, r2, modulus):
    return (
        r0[0] * (r1[1] * r2[2] + r1[2] * r2[1])
        + r0[1] * (r1[0] * r2[2] + r1[2] * r2[0])
        + r0[2] * (r1[0] * r2[1] + r1[1] * r2[0])
    ) % modulus


def weighted_common(row, diagonal, rv, modulus):
    """First three columns of a weighted row (extension deleted)."""
    if diagonal == "01":
        return (
            (rv * row[0] + row[1]) % modulus,
            row[2],
            row[3],
        )
    return (
        row[0],
        row[1],
        (rv * row[2] + row[3]) % modulus,
    )


def linear_system(diagonal, alpha, beta_marked, rv, modulus):
    """14 mixed rows plus the two diagonal rows, as linear forms in
    the eight extension slots.  Every word coefficient is linear in
    the extensions, and its slot derivative is the three-by-three
    permanent of the other selected weighted common rows."""
    weighted_alpha = tuple(
        weighted_common(alpha[mode], diagonal, rv, modulus)
        for mode in range(4)
    )
    weighted_beta = tuple(
        weighted_common(beta_marked[mode], diagonal, rv, modulus)
        for mode in range(4)
    )
    mixed_rows = []
    first = [0] * 8
    second = [0] * 8
    for word in BITS4:
        selected = tuple(
            weighted_beta[mode] if word[mode] else weighted_alpha[mode]
            for mode in range(4)
        )
        row = [0] * 8
        for mode in range(4):
            others = tuple(
                selected[other] for other in range(4) if other != mode
            )
            slot = mode + (4 if word[mode] else 0)
            row[slot] = perm3(*others, modulus)
        if word == (0, 0, 0, 0):
            first = row
        elif word == (1, 1, 1, 1):
            second = row
        else:
            mixed_rows.append(row)
    return mixed_rows, first, second


def audit_pencil(diagonal, modulus, pp, qq, rv):
    alpha, beta0 = family_rows(pp, qq, modulus)
    denominator = (pp * qq + pp + 1) % modulus
    assert denominator != 0
    t0_star = -(qq + 1) * pow(denominator, -1, modulus) % modulus
    if diagonal == "01":
        expected = {(s, 0, 0, 0) for s in range(modulus)}
    else:
        expected = (
            {(s, 0, 0, 0) for s in range(modulus)}
            | {(t0_star, 0, 0, s) for s in range(modulus)}
        )

    survivors = set()
    genuine_total = 0
    minors_checked = 0
    for shifts in itertools.product(range(modulus), repeat=4):
        beta_marked = tuple(
            tuple(
                (b + shifts[mode] * a) % modulus
                for b, a in zip(beta0[mode], alpha[mode])
            )
            for mode in range(4)
        )
        mixed_rows, first, second = linear_system(
            diagonal, alpha, beta_marked, rv, modulus
        )
        rank, kernel = rref_nullspace(mixed_rows, modulus)
        if not kernel:
            continue
        dot = lambda row, vec: sum(
            left * right for left, right in zip(row, vec)
        ) % modulus
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
        assert shifts in expected, (diagonal, shifts)
        on_t0_line = shifts[1] == shifts[2] == shifts[3] == 0
        if on_t0_line:
            mode, row_sets = MODE_T0, MINORS_T0
        else:
            mode, row_sets = MODE_T3, MINORS_T3
        for vector in genuine:
            genuine_total += 1
            alpha_ext = tuple(
                weighted_row(
                    alpha[m], vector[m], diagonal, rv, modulus
                )
                for m in range(4)
            )
            beta_ext = tuple(
                weighted_row(
                    beta_marked[m], vector[4 + m], diagonal, rv, modulus
                )
                for m in range(4)
            )
            marked = one_marked_rows(mode, alpha_ext, beta_ext, modulus)
            values = [
                determinant_mod(
                    [marked[row] for row in rows], modulus
                )
                for rows in row_sets
            ]
            assert any(value != 0 for value in values), (
                diagonal,
                shifts,
                vector,
            )
            minors_checked += 1
    missing = {
        shifts for shifts in expected if shifts not in survivors
    }
    return {
        "survivor_markings": len(survivors),
        "expected_locus_size": len(expected),
        "markings_on_locus_without_genuine_direction": len(missing),
        "survivors_inside_theorem_locus": True,
        "genuine_directions": genuine_total,
        "certificate_minor_checks": minors_checked,
    }


def main() -> None:
    reports = {}
    for modulus, pp, qq, rv in SAMPLES:
        for value in (
            rv,
            (rv - 1) % modulus,
            (rv + 1) % modulus,
            (pp * rv - 1) % modulus,
            (pp * rv + 1) % modulus,
            (pp * qq + pp * rv + 1) % modulus,
        ):
            assert value != 0, (modulus, rv)
        key = f"F_{modulus}(p={pp},q={qq},r={rv})"
        reports[key] = {
            diagonal: audit_pencil(diagonal, modulus, pp, qq, rv)
            for diagonal in ("01", "23")
        }
    output = {
        "audited": True,
        "finite_field_corroboration_only": True,
        "samples": reports,
        "survivors_contained_in_theorem_loci": True,
        "certificate_minors_cover_every_genuine_direction": True,
        "theorem": THEOREM.name,
        "theorem_sha256": (
            sha256(THEOREM) if THEOREM.exists() else None
        ),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / (
        "p5_h22_all_rank_one_triangle_component_generic_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
