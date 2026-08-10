#!/usr/bin/env python3
"""Verify the shifted marked-basis H31 branch over the known component."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.p5_marked_basis import (  # noqa: E402
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)

REPO_ROOT, HERE = bootstrap(__file__)
BITS4 = tuple(itertools.product((0, 1), repeat=4))
THEOREM = HERE / "P5_H31_MARKED_BASIS_OPEN_BRANCH.md"
FAMILY = REPO_ROOT / "claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    output_path = REPO_ROOT / "tmp" / "p5_h31_marked_basis_open_branch_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
