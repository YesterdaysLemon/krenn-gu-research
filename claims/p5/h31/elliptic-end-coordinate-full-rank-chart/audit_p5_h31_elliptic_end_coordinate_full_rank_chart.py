#!/usr/bin/env python3
"""Independent DP-permanent audit of the end-coordinate rank chart."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md"
PRIMARY = ROOT / "verify_p5_h31_elliptic_end_coordinate_full_rank_chart.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PIVOT_ROWS = (0, 1, 2, 3, 4, 9)
PIVOT_COLUMNS = (0, 1, 2, 3, 4, 6)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                next_states[next_mask] = (
                    next_states.get(next_mask, sp.Integer(0))
                    + coefficient * entry
                )
        states = next_states
    return sp.expand(states[15])


def extension_system(distinguished, alpha, beta):
    extension = sp.symbols("a0:4") + sp.symbols("b0:4")
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_extended = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extension[mode],)
        for mode, row in enumerate(alpha)
    )
    beta_extended = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent_dp(tuple(
            beta_extended[mode] if word[mode] else alpha_extended[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], variable) for variable in extension]
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    diagonal_a = sp.Matrix([[
        sp.diff(coefficients[(0, 0, 0, 0)], variable)
        for variable in extension
    ]])
    diagonal_b = sp.Matrix([[
        sp.diff(coefficients[(1, 1, 1, 1)], variable)
        for variable in extension
    ]])
    return mixed, diagonal_a, diagonal_b


def reduce_elliptic(expression, Y, relation) -> sp.Expr:
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
        mixed, diagonal_a, diagonal_b = extension_system(
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
        kernel = sp.Matrix(
            kernel_zero[:4]
            + tuple(
                kernel_zero[4 + mode] + t[mode] * kernel_zero[mode]
                for mode in range(4)
            )
        )
        assert all(
            reduce_elliptic(entry, Y, relation) == 0
            for entry in mixed * kernel
        )
        assert reduce_elliptic(
            (diagonal_a * kernel)[0],
            Y,
            relation,
        ) == 0
        assert reduce_elliptic(
            (diagonal_b * kernel)[0],
            Y,
            relation,
        ) == sign * 4 * r * x * (x - 1 - r) * (x - 1 + r)

        quotient = mixed[:, [0, 2, 3, 4, 5, 6, 7]]
        signed_Y = r**2 * x + sign * Y
        pivot = reduce_elliptic(
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
        bordered = reduce_elliptic(
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
        cases[str(distinguished)] = {
            "pivot": str(pivot),
            "bordered": str(bordered),
        }

    completed = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=120,
    )
    if completed.returncode != 0:
        raise AssertionError(
            ("primary verifier failed", completed.stdout, completed.stderr)
        )
    primary_output = json.loads(completed.stdout)
    assert primary_output["verified"] is True
    assert primary_output["chart_complement_closed"] is False

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        "distinguished_coordinates": [0, 3],
        "universal_kernel_verified": True,
        "quotient_full_rank_chart_verified": True,
        "primary_replay_verified": True,
        "chart_complement_closed": False,
        "cases": cases,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_end_coordinate_full_rank_chart_audited.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
