#!/usr/bin/env python3
"""Independent modular audit of the shifted marked-basis branch."""

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
THEOREM = ROOT / "P5_H31_MARKED_BASIS_OPEN_BRANCH.md"
PRIMARY = ROOT / "verify_p5_h31_marked_basis_open_branch.py"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
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


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [
            entry * inverse % prime for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (left - scale * right) % prime
                    for left, right in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
    return rank


def coefficients(
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> dict[tuple[int, ...], int]:
    return {
        bits: permanent(tuple(
            beta[mode] if bits[mode] else alpha[mode]
            for mode in range(4)
        ), prime)
        for bits in BITS4
    }


def extension_rows(
    distinguished: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    extension: tuple[int, ...],
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
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
    return alpha_p, beta_p


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
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(permanent(tuple(
                basis if other == mode else selected[other]
                for other in range(4)
            ), prime))
        rows.append(coefficient_row)
    return rows


def main() -> None:
    field_counts = {}
    checked = 0
    for prime in (5, 7):
        accepted = 0
        for L, Q, C in itertools.product(range(prime), repeat=3):
            D = (C + L) % prime
            A = (1 + L * Q) % prime
            B = (1 + D * Q) % prime
            if not (L and Q and D and A and B):
                continue
            accepted += 1
            inverse_q = pow(Q, -1, prime)
            inverse_a = pow(A, -1, prime)
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
            shifts = (-inverse_q, 0, L * inverse_a, 0)
            beta = tuple(
                tuple(
                    canonical[mode][coordinate]
                    + shifts[mode] * alpha[mode][coordinate]
                    for coordinate in range(4)
                )
                for mode in range(4)
            )

            for mode in range(4):
                for left, right in itertools.combinations(range(4), 2):
                    canonical_minor = (
                        alpha[mode][left] * canonical[mode][right]
                        - alpha[mode][right] * canonical[mode][left]
                    ) % prime
                    shifted_minor = (
                        alpha[mode][left] * beta[mode][right]
                        - alpha[mode][right] * beta[mode][left]
                    ) % prime
                    assert shifted_minor == canonical_minor

            pure = coefficients(alpha, beta, prime)
            assert pure[(1, 1, 1, 1)] == 2 * D % prime
            assert all(
                not value
                for bits, value in pure.items()
                if bits != (1, 1, 1, 1)
            )

            extension = (
                1, 0, 0, -1,
                B * inverse_q, 1, 0, 0,
            )
            alpha_p, beta_p = extension_rows(
                2, alpha, beta, extension
            )
            neighbour = coefficients(alpha_p, beta_p, prime)
            assert neighbour[(0, 0, 0, 0)] == -2 * A % prime
            assert neighbour[(1, 1, 1, 1)] == (
                2 * B * inverse_q
            ) % prime
            assert all(
                not value
                for bits, value in neighbour.items()
                if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
            )

            marked = one_marked_map(2, alpha_p, beta_p, prime)
            selected = [marked[index] for index in (0, 1, 3, 7)]
            assert rank_mod(selected, prime) == 4
            pure_marked = one_marked_map(2, alpha, beta, prime)
            assert pure_marked[0][2] == A
            checked += 1
        field_counts[f"F_{prime}"] = accepted

    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "finite_fields": ["F_5", "F_7"],
        "admissible_parameter_counts": field_counts,
        "parameter_tuples_checked": checked,
        "method": "dynamic-programming permanent and modular rank",
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / 'tmp/p5_h31_marked_basis_open_branch_audit.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
