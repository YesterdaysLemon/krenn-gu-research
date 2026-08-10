#!/usr/bin/env python3
"""Independent audit of component 21's extension-kernel H31 obstruction."""

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
PRIMARY = ROOT / "verify_p5_component21_extension_kernel_marked_h31_leading_obstruction.py"
THEOREM = ROOT / "P5_COMPONENT21_EXTENSION_KERNEL_MARKED_H31_LEADING_OBSTRUCTION.md"
PINNED = {
    ROOT / "P5_COMPONENT21_FINITE_BASE_EXTENSION_INFINITY_PARTIAL_CLOSURE.md": (
        "1c8f5c83aeae794782b684b1f35f3c25323470edae28c38a5c52d423b8a86502"
    ),
    ROOT / "verify_p5_component21_finite_base_extension_infinity_partial_closure.py": (
        "3c407f3b9612e1a51268f85c78778eb0ee23543438ee432838501f02f6a02229"
    ),
    ROOT / "audit_p5_component21_finite_base_extension_infinity_partial_closure.py": (
        "965afa260b29fc02e624a0362c78644dd8f8604594cdcbef78cbf7c29a8b4ca6"
    ),
}
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
SEVEN_ROWS = (0, 1, 2, 4, 5, 7, 8)
SEVEN_COLUMNS = tuple(range(7))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Subset-DP permanent, independent of the primary's permutation sum."""
    size = len(rows)
    state: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_state: dict[int, sp.Expr] = {}
        for mask, value in state.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_state[new_mask] = next_state.get(new_mask, 0) + (
                    value * row[column]
                )
        state = next_state
    return sp.expand(state[(1 << size) - 1])


def bases(
    p: sp.Expr, epsilon: int
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    return (
        add(cap_a, scale(p, cap_b)),
        add(scale(epsilon, cap_a), cap_c),
        cap_c,
        cap_d,
    ), (
        add(cap_c, scale(epsilon * p, cap_b)),
        cap_a,
        cap_b,
        add(cap_a, scale(epsilon, cap_c)),
    )


def marked(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        add(beta[mode], scale(shifts[mode], alpha[mode])) for mode in range(4)
    )


def extended_rows(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]
]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[mode][index] for index in retained) + (extension[mode],)
        for mode in range(4)
    )
    beta_rows = tuple(
        tuple(beta[mode][index] for index in retained) + (extension[4 + mode],)
        for mode in range(4)
    )
    return alpha_rows, beta_rows


def coefficient_matrix(
    alpha_rows: tuple[tuple[sp.Expr, ...], ...],
    beta_rows: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    coefficients = []
    for word in WORDS4:
        rows = tuple(
            beta_rows[mode] if word[mode] else alpha_rows[mode]
            for mode in range(4)
        )
        coefficients.append(permanent(rows))
    return sp.Matrix(
        [
            [sp.diff(coefficient, variable) for variable in extension]
            for coefficient in coefficients
        ]
    )


def one_marked_obstruction(
    alpha_rows: tuple[tuple[sp.Expr, ...], ...],
    beta_rows: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    output = []
    for word in WORDS3:
        chosen: list[tuple[sp.Expr, ...] | None] = []
        bit = 0
        for mode in range(4):
            if mode == 3:
                chosen.append(None)
            else:
                chosen.append(beta_rows[mode] if word[bit] else alpha_rows[mode])
                bit += 1
        row = []
        for coordinate in range(4):
            basis = tuple(sp.Integer(index == coordinate) for index in range(4))
            square_rows = tuple(
                basis if mode == 3 else chosen[mode] for mode in range(4)
            )
            assert all(item is not None for item in square_rows)
            row.append(permanent(square_rows))  # type: ignore[arg-type]
        output.append(tuple(row))
    return sp.Matrix(output)


def kernel_vector(
    p: sp.Symbol,
    epsilon: int,
    distinguished: int,
    shifts: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    sign = -1 if distinguished == 2 else 1
    alpha_part = (
        -sp.Rational(1, 2),
        -epsilon,
        sp.Integer(0),
        sp.Rational(sign, 2) / p,
    )
    beta_part = (
        sp.Rational(epsilon, 2),
        sp.Integer(0),
        -sp.Rational(1, 2) / p,
        sp.Integer(1),
    )
    return sp.Matrix(
        alpha_part
        + tuple(
            sp.expand(beta_part[mode] + shifts[mode] * alpha_part[mode])
            for mode in range(4)
        )
    )


def audit_case(
    p: sp.Symbol,
    epsilon: int,
    distinguished: int,
    shifts: tuple[sp.Symbol, ...],
    extension: tuple[sp.Symbol, ...],
) -> dict[str, object]:
    alpha, unmarked_beta = bases(p, epsilon)
    beta = marked(alpha, unmarked_beta, shifts)
    alpha_rows, beta_rows = extended_rows(
        distinguished, alpha, beta, extension
    )
    matrix = coefficient_matrix(alpha_rows, beta_rows, extension)
    kernel = kernel_vector(p, epsilon, distinguished, shifts)
    kernel_image = matrix * kernel
    assert all(sp.factor(value) == 0 for value in kernel_image)

    obstruction = one_marked_obstruction(alpha_rows, beta_rows)
    assert obstruction.shape == (8, 4)
    assert all(
        sp.Poly(entry, *extension).total_degree() <= 1 for entry in obstruction
    )
    evaluated = obstruction.subs(dict(zip(extension, kernel, strict=True)))
    assert sp.factor(evaluated[0, 2]) == 1
    kernel_scale = sp.Symbol("c", nonzero=True)
    scaled = obstruction.subs(
        dict(zip(extension, kernel_scale * kernel, strict=True))
    )
    assert sp.factor(scaled[0, 2]) == kernel_scale

    unmarked_alpha_rows, unmarked_beta_rows = extended_rows(
        distinguished, alpha, unmarked_beta, extension
    )
    unmarked_matrix = coefficient_matrix(
        unmarked_alpha_rows, unmarked_beta_rows, extension
    )
    minor = sp.factor(
        sp.polys.matrices.DomainMatrix.from_Matrix(
            unmarked_matrix[list(SEVEN_ROWS), list(SEVEN_COLUMNS)]
        )
        .det()
        .as_expr()
    )
    assert sp.cancel(minor / (256 * p**3)) in (1, -1)
    return {
        "epsilon": epsilon,
        "distinguished": distinguished,
        "kernel_rank": 1,
        "selected_obstruction_entry": str(evaluated[0, 2]),
        "scaled_obstruction_entry": str(scaled[0, 2]),
        "seven_minor": str(minor),
    }


def main() -> None:
    p = sp.Symbol("p", nonzero=True)
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    cases = [
        audit_case(p, epsilon, distinguished, shifts, extension)
        for epsilon in (1, -1)
        for distinguished in (2, 3)
    ]
    assert len(cases) == 4
    assert all(case["selected_obstruction_entry"] == "1" for case in cases)

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    assert "No finite-field computation is used as proof." in theorem_text
    assert "global Krenn--Gu conjecture remains **UNRESOLVED**" in theorem_text

    completed = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    primary_payload = json.loads(completed.stdout)
    assert primary_payload["status"] == "pass"
    assert primary_payload["finite_nonzero_sheet_marked_H31_extension_poles_closed"]
    assert not primary_payload["global_conjecture_resolved"]

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "independent_permanent": "subset dynamic programming",
                "repository_imports_used": False,
                "cases": cases,
                "selected_entry_identically_one": True,
                "primary_replay_status": primary_payload["status"],
                "finite_weight_H22_kernel_normals_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "dependency_hashes": dependency_hashes,
                "primary_sha256": sha256(PRIMARY),
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
