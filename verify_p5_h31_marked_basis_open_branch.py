#!/usr/bin/env python3
"""Verify the shifted marked-basis H31 branch over the known component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_MARKED_BASIS_OPEN_BRANCH.md"
FAMILY = ROOT / "P4_DECOMPOSABLE_RANK_TWO_FAMILY.md"
COMPONENT = ROOT / "P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.factor(sum(
        sp.prod(rows[row][permutation[row]] for row in range(4))
        for permutation in PERMUTATIONS
    ))


def extension_coefficients(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: sp.Matrix,
) -> dict[tuple[int, ...], sp.Expr]:
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
        bits: permanent(tuple(
            beta_p[mode] if bits[mode] else alpha_p[mode]
            for mode in range(4)
        ))
        for bits in BITS4
    }


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
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
            )))
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def marked_extension(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    mode: int,
) -> sp.Matrix:
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
    return one_marked_map(mode, alpha_p, beta_p)


def mixed_matrix(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    variables = sp.symbols("x0:4") + sp.symbols("y0:4")
    coefficients = extension_coefficients(
        distinguished,
        alpha,
        beta,
        sp.Matrix(variables),
    )
    mixed = sp.Matrix([
        [sp.diff(coefficients[bits], variable) for variable in variables]
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    diagonals = tuple(sp.Matrix([[
        sp.diff(coefficients[bits], variable) for variable in variables
    ]]) for bits in ((0, 0, 0, 0), (1, 1, 1, 1)))
    return mixed, *diagonals


def main() -> None:
    L, Q, C = sp.symbols("L Q C", nonzero=True)
    D = C + L
    A = 1 + L * Q
    B = 1 + D * Q

    alpha = (
        (1, Q, 0, -A),
        (L, 1, -L, -L),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )
    canonical_beta = (
        (0, 1, D, C),
        (0, 0, 1, 1),
        (0, 1, 0, L),
        (1, 0, 1, 0),
    )
    shifts = (-1 / Q, 0, L / A, 0)
    beta = tuple(
        tuple(
            canonical_beta[mode][coordinate]
            + shifts[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    canonical_plueckers = tuple(
        tuple(sp.factor(
            alpha[mode][left] * canonical_beta[mode][right]
            - alpha[mode][right] * canonical_beta[mode][left]
        ) for left, right in itertools.combinations(range(4), 2))
        for mode in range(4)
    )
    shifted_plueckers = tuple(
        tuple(sp.factor(
            alpha[mode][left] * beta[mode][right]
            - alpha[mode][right] * beta[mode][left]
        ) for left, right in itertools.combinations(range(4), 2))
        for mode in range(4)
    )
    assert shifted_plueckers == canonical_plueckers

    pure_coefficients = {
        bits: permanent(tuple(
            beta[mode] if bits[mode] else alpha[mode]
            for mode in range(4)
        ))
        for bits in BITS4
    }
    assert sp.factor(
        pure_coefficients[(1, 1, 1, 1)] - 2 * D
    ) == 0
    assert all(
        sp.factor(value) == 0
        for bits, value in pure_coefficients.items()
        if bits != (1, 1, 1, 1)
    )

    extension = sp.Matrix((1, 0, 0, -1, B / Q, 1, 0, 0))
    neighbouring = extension_coefficients(2, alpha, beta, extension)
    assert sp.factor(neighbouring[(0, 0, 0, 0)] + 2 * A) == 0
    assert sp.factor(neighbouring[(1, 1, 1, 1)] - 2 * B / Q) == 0
    assert all(
        sp.factor(value) == 0
        for bits, value in neighbouring.items()
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )

    marked = marked_extension(2, extension, alpha, beta, 2)
    determinant = sp.factor(marked[[0, 1, 3, 7], :].det())
    assert sp.factor(determinant - 8 * A**2 * B) == 0
    pure_marked = one_marked_map(2, alpha, beta)
    assert sp.factor(pure_marked[0, 2] - A) == 0

    specialized_alpha = tuple(
        tuple(
            sp.sympify(entry).subs({L: 1, Q: 1, C: 1})
            for entry in row
        )
        for row in alpha
    )
    specialized_canonical = tuple(
        tuple(sp.sympify(entry).subs({L: 1, Q: 1, C: 1}) for entry in row)
        for row in canonical_beta
    )
    specialized_beta = tuple(
        tuple(
            sp.sympify(entry).subs({L: 1, Q: 1, C: 1})
            for entry in row
        )
        for row in beta
    )
    canonical_mixed, canonical_a, canonical_b = mixed_matrix(
        2, specialized_alpha, specialized_canonical
    )
    shifted_mixed, shifted_a, shifted_b = mixed_matrix(
        2, specialized_alpha, specialized_beta
    )
    assert canonical_mixed.rank() == 7
    canonical_kernel = canonical_mixed.nullspace()
    assert len(canonical_kernel) == 1
    assert (
        (canonical_a * canonical_kernel[0])[0],
        (canonical_b * canonical_kernel[0])[0],
    ) == (0, 4)
    assert shifted_mixed.rank() == 6
    specialized_extension = extension.subs({L: 1, Q: 1, C: 1})
    assert shifted_mixed * specialized_extension == sp.zeros(14, 1)
    assert (
        (shifted_a * specialized_extension)[0],
        (shifted_b * specialized_extension)[0],
    ) == (-4, 6)

    output = {
        "verified": True,
        "field": "C",
        "method": "marked-basis fibre and exact permanent identities",
        "same_plane_tuple": True,
        "canonical_specialized_mixed_rank": 7,
        "shifted_specialized_mixed_rank": 6,
        "shifted_binary_diagonals": ["-2*(1+L*Q)", "2*(1+(C+L)*Q)/Q"],
        "marked_determinant": "8*(1+L*Q)^2*(1+(C+L)*Q)",
        "H31_lift_excluded_on_branch": True,
        "whole_marked_component_excluded": False,
        "dependencies": {
            FAMILY.name: sha256(FAMILY),
            COMPONENT.name: sha256(COMPONENT),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_h31_marked_basis_open_branch_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
