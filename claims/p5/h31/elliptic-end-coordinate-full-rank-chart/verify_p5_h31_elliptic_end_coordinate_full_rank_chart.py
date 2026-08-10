#!/usr/bin/env python3
"""Verify the end-coordinate full-rank quotient chart."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.p5_marked_basis import mixed_matrix


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md"
MIDDLE = REPO_ROOT / 'claims/p5/h31/elliptic-middle-coordinate-rank-drop/P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md'
PIVOT_ROWS = (0, 1, 2, 3, 4, 9)
PIVOT_COLUMNS = (0, 1, 2, 3, 4, 6)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remainder_mod_elliptic(expression, Y, relation) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, Y),
        sp.Poly(relation, Y),
    ).as_expr()
    return sp.factor(remainder / denominator)


def main() -> None:
    r, x, Y = sp.symbols("r x Y")
    t = sp.symbols("t0:4")
    _t0, _t1, t2, t3 = t
    D = x + r**2 - 1
    f = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    relation = Y**2 - f
    assert sp.factor(r**4 * x**2 - f) == (
        x * (r - 1) * (r + 1) * (x - 1) * D
    )

    alpha = (
        (
            Y + r**2 * x,
            -r * x - r**2 * x,
            -r * x + r**2 * x,
            -Y + r**2 * x,
        ),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (r, -1, -1, r),
    )
    beta_zero = (
        (1, -1, 1, 1),
        (D, r * x + D, r * x - D, D),
        (x * (1 - x) + Y, r * x, r * x, x * (1 - x) - Y),
        (0, 1, 1, 0),
    )
    beta = tuple(
        tuple(
            beta_zero[mode][coordinate]
            + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    cases = {}
    for distinguished, sign in ((0, -1), (3, 1)):
        mixed, diagonal_a, diagonal_b = mixed_matrix(
            distinguished,
            alpha,
            beta,
        )
        kernel_zero = (
            (
                Y + r**2 * x,
                1,
                0,
                r,
                1,
                D,
                Y - x**2 + x,
                0,
            )
            if distinguished == 0
            else (
                Y - r**2 * x,
                1,
                0,
                -r,
                -1,
                -D,
                Y + x**2 - x,
                0,
            )
        )
        marked_kernel = sp.Matrix(
            kernel_zero[:4]
            + tuple(
                kernel_zero[4 + mode] + t[mode] * kernel_zero[mode]
                for mode in range(4)
            )
        )
        assert all(
            remainder_mod_elliptic(entry, Y, relation) == 0
            for entry in mixed * marked_kernel
        )
        assert remainder_mod_elliptic(
            (diagonal_a * marked_kernel)[0],
            Y,
            relation,
        ) == 0
        expected_diagonal_b = (
            sign * 4 * r * x * (x - 1 - r) * (x - 1 + r)
        )
        assert remainder_mod_elliptic(
            (diagonal_b * marked_kernel)[0],
            Y,
            relation,
        ) == expected_diagonal_b

        quotient = mixed[:, [0, 2, 3, 4, 5, 6, 7]]
        signed_Y = r**2 * x + sign * Y
        pivot = remainder_mod_elliptic(
            quotient.extract(PIVOT_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            ),
            Y,
            relation,
        )
        expected_pivot = (
            64
            * r**8
            * x**5
            * signed_Y
            * (r - 1)
            * (r + 1)
            * (x - t2)
            * (t3 - 1)
            * (x - 1)
        )
        assert sp.factor(pivot - expected_pivot) == 0

        bordered = remainder_mod_elliptic(
            quotient.extract(
                PIVOT_ROWS + (11,),
                PIVOT_COLUMNS + (5,),
            ).det(method="domain-ge"),
            Y,
            relation,
        )
        expected_bordered = (
            128
            * r**7
            * x**4
            * signed_Y
            * (r - 1)
            * (r + 1)
            * (x - t2)
            * (t3 - 1)
            * (x - 1)
            * D
        )
        assert sp.factor(bordered - expected_bordered) == 0
        assert remainder_mod_elliptic(
            (r**2 * x - Y) * (r**2 * x + Y)
            - x * (r - 1) * (r + 1) * (x - 1) * D,
            Y,
            relation,
        ) == 0

        cases[str(distinguished)] = {
            "universal_kernel": [str(entry) for entry in marked_kernel],
            "diagonal_b": str(expected_diagonal_b),
            "pivot": str(pivot),
            "bordered_full_rank_minor": str(bordered),
        }

    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinates": [0, 3],
        "universal_mixed_kernel_verified": True,
        "quotient_rank_on_chart": 7,
        "binary_survivor_on_chart": False,
        "chart_complement_closed": False,
        "cases": cases,
        "dependencies": {MIDDLE.name: sha256(MIDDLE)},
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_end_coordinate_full_rank_chart_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
