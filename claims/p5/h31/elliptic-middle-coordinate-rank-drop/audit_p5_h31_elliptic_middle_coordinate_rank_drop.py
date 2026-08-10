#!/usr/bin/env python3
"""Independent DP-permanent audit of the middle-coordinate rank-drop chart."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
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



ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md"
PRIMARY = ROOT / "verify_p5_h31_elliptic_middle_coordinate_rank_drop.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PIVOT_ROWS = (1, 2, 3, 8, 9, 11)
PIVOT_COLUMNS = (0, 2, 3, 4, 5, 6)
REMAINING_COLUMN = 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
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


def extension_system(distinguished: int, alpha, beta):
    extensions = sp.symbols("a0:4") + sp.symbols("b0:4")
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    extended_alpha = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extensions[mode],)
        for mode, row in enumerate(alpha)
    )
    extended_beta = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extensions[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent_dp(tuple(
            extended_beta[mode] if word[mode] else extended_alpha[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    mixed = sp.Matrix([
        [
            sp.diff(coefficients[word], variable)
            for variable in extensions
        ]
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    diagonal_a = sp.Matrix([[
        sp.diff(coefficients[(0, 0, 0, 0)], variable)
        for variable in extensions
    ]])
    diagonal_b = sp.Matrix([[
        sp.diff(coefficients[(1, 1, 1, 1)], variable)
        for variable in extensions
    ]])
    return mixed, diagonal_a, diagonal_b


def remainder_mod_elliptic(expression, Y, relation) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, Y),
        sp.Poly(relation, Y),
    ).as_expr()
    return sp.factor(remainder / denominator)


def border(matrix, row, Y, relation) -> sp.Expr:
    return remainder_mod_elliptic(
        matrix.extract(
            PIVOT_ROWS + (row,),
            PIVOT_COLUMNS + (REMAINING_COLUMN,),
        ).det(method="domain-ge"),
        Y,
        relation,
    )


def dependent_factor(expression, variable) -> sp.Expr:
    numerator = sp.factor(sp.fraction(sp.cancel(expression))[0])
    factors = [
        factor
        for factor, multiplicity in sp.factor_list(numerator)[1]
        if factor.has(variable)
        for _ in range(multiplicity)
    ]
    assert len(factors) == 1
    return factors[0]


def same_divisor(left, right) -> None:
    ratio = sp.factor(left / right)
    assert ratio != 0 and not ratio.free_symbols


def main() -> None:
    r, x, Y = sp.symbols("r x Y")
    t = sp.symbols("t0:4")
    t0, t1, t2, t3 = t
    D = x + r**2 - 1
    f = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    relation = Y**2 - f
    Q = -f / x
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

    audited_cases = {}
    for distinguished, sigma in ((1, -1), (2, 1)):
        mixed, diagonal_a, diagonal_b = extension_system(
            distinguished,
            alpha,
            beta,
        )
        kernel_zero = (
            (
                -r * x * (r + 1),
                0,
                1,
                -1,
                -1,
                (r + 1) * (r + x - 1),
                r * x,
                1,
            )
            if distinguished == 1
            else (
                r * x * (r - 1),
                0,
                -1,
                -1,
                1,
                (r - 1) * (-r + x - 1),
                r * x,
                1,
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
        assert remainder_mod_elliptic(
            (diagonal_b * marked_kernel)[0],
            Y,
            relation,
        ) == -4 * r * x * (x - 1 - r) * (x - 1 + r)

        quotient = mixed[:, [0, 1, 3, 4, 5, 6, 7]]
        pivot = remainder_mod_elliptic(
            quotient.extract(PIVOT_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            ),
            Y,
            relation,
        )
        expected_pivot = (
            -64
            * r**2
            * t0
            * x**2
            * (t3 - 1)
            * (r**2 * x - t2)
            * D
            * Q**2
        )
        assert sp.factor(pivot - expected_pivot) == 0

        branch_substitutions = {
            "I": {
                t3: 0,
                t2: -sigma * r * x,
                t0: -1 / (x * D),
            },
            "II": {
                t3: 0,
                t2: x * (1 - x),
                t0: -1 / (r * (r + sigma) * x),
            },
        }
        compatibility_output = {}
        for name, substitution in branch_substitutions.items():
            specialized = quotient.subs(substitution)
            factors = {
                row: dependent_factor(
                    border(specialized, row, Y, relation),
                    t1,
                )
                for row in (5, 6, 13)
            }

            def compatibility(left_row, right_row):
                left = factors[left_row]
                right = factors[right_row]
                return remainder_mod_elliptic(
                    sp.diff(left, t1) * right.subs(t1, 0)
                    - sp.diff(right, t1) * left.subs(t1, 0),
                    Y,
                    relation,
                )

            first = compatibility(6, 13)
            if name == "I":
                expected_first = (
                    sigma
                    * Y
                    * (r + sigma)
                    * (x - 1)
                    * (x - 1 + sigma * r) ** 2
                    * D
                    * Q
                )
                same_divisor(first, expected_first)
                assert sp.factor(
                    factors[13].subs(x, 1) - r**4 * (Y - t1)
                ) == 0
                compatibility_output[name] = [str(expected_first)]
            else:
                expected_first = (
                    sigma
                    * Y
                    * r
                    * (x - 1 + sigma * r)
                    * D
                    * Q
                )
                second = compatibility(5, 6)
                expected_second = (
                    2
                    * Y
                    * r**2
                    * (x - 1)
                    * (x + 1 - sigma * r)
                    * D**2
                    * Q
                )
                same_divisor(first, expected_first)
                same_divisor(second, expected_second)
                compatibility_output[name] = [
                    str(expected_first),
                    str(expected_second),
                ]
        audited_cases[str(distinguished)] = {
            "pivot": str(pivot),
            "compatibilities": compatibility_output,
        }

    # Run the primary as a separate process after the independent rebuild.
    completed = subprocess.run(
        [str(Path(__import__("sys").executable)), str(PRIMARY)],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=180,
    )
    if completed.returncode != 0:
        raise AssertionError(
            ("primary verifier failed", completed.stdout, completed.stderr)
        )
    primary_output = json.loads(completed.stdout)
    assert primary_output["verified"] is True
    assert primary_output["full_survivor_divisor_classified"] is False

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        "distinguished_coordinates": [1, 2],
        "universal_kernel_and_pivot_verified": True,
        "branch_compatibilities_verified": True,
        "primary_replay_verified": True,
        "full_survivor_divisor_classified": False,
        "cases": audited_cases,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_middle_coordinate_rank_drop_audited.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
