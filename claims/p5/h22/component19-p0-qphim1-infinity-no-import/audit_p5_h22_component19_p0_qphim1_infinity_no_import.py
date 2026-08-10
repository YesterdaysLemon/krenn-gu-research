#!/usr/bin/env python3
"""No-import verifier for the p=0, q*phi=-1 infinity chart."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp

ROOT = HERE
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def assert_equal(actual: sp.Expr, expected: sp.Expr) -> None:
    assert sp.factor(actual - expected) == 0, (actual, expected)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(value, row):
    return tuple(sp.expand(value * entry) for entry in row)


def multiply(left, right):
    result = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return result


def permanent(rows) -> sp.Expr:
    value = {0: sp.Integer(1)}
    for row in rows:
        linear = {
            1 << index: sp.sympify(entry)
            for index, entry in enumerate(row)
            if entry != 0
        }
        value = multiply(value, linear)
    return sp.factor(value.get((1 << len(rows)) - 1, 0))


def restrict_infinity(row, extension, direction):
    if direction == "01":
        return (row[0], row[2], row[3], extension)
    if direction == "23":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def contracted_planes(direction):
    result = []
    for mode, (alpha, beta) in enumerate(planes):
        marked_beta = add(beta, scale(h[mode], alpha))
        result.append(
            (
                restrict_infinity(alpha, C[mode], direction),
                restrict_infinity(marked_beta, D[mode], direction),
            )
        )
    return tuple(result)


def tensor(direction):
    direction_planes = contracted_planes(direction)
    return {
        word: permanent(tuple(direction_planes[i][word[i]] for i in range(4)))
        for word in WORDS
    }


phi = sp.symbols("phi", nonzero=True)
h0, h1, h2, h3 = sp.symbols("h0 h1 h2 h3")
C0, C1, C2, C3 = sp.symbols("C0 C1 C2 C3")
D0, D1, D2, D3 = sp.symbols("D0 D1 D2 D3")
h = (h0, h1, h2, h3)
C = (C0, C1, C2, C3)
D = (D0, D1, D2, D3)
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)

# Fresh regular p=0 basis with q=-1/phi.
planes = (
    (Abar, add(Bbar, scale(-1 / phi, B))),
    (B, A),
    (Bbar, A),
    (Abar, add(B, scale(phi, Bbar))),
)

raw_tensor = {
    word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
    for word in WORDS
}
raw_support = {word: value for word, value in raw_tensor.items() if value != 0}
assert raw_support.keys() == {(1, 1, 1, 1)}
assert_equal(raw_support[(1, 1, 1, 1)], -4 * (phi**2 + 1) / phi)

infinity = {direction: tensor(direction) for direction in ("01", "23")}

# D01 cannot be binary; D23 must carry the two nonzero diagonal coefficients.
assert infinity["01"][(0, 0, 0, 0)] == 0
A23 = sp.factor(infinity["23"][(0, 0, 0, 0)])
assert_equal(A23, -2 * (C1 + C2))
assert_equal(infinity["23"][(0, 0, 0, 1)], h3 * A23)
assert_equal(infinity["23"][(1, 0, 0, 0)], h0 * A23)

# Two necessary D01 mixed equations already contradict the A23-open.
m1 = sp.factor(infinity["01"][(0, 0, 0, 1)])
m2 = sp.factor(infinity["01"][(1, 0, 0, 0)])
assert_equal(m1, -2 * (phi * C1 - C2))
assert_equal(m2, 2 * (-C1 - C2 / phi))
coefficient_determinant = sp.factor(
    sp.Matrix(((phi, -1), (-1, -1 / phi))).det()
)
assert_equal(coefficient_determinant, -2)

ideal_identity = sp.factor(
    (1 - phi) * m1 / (2 * phi) + (1 + phi) * m2 / 2
)
assert_equal(ideal_identity, A23)

# The certificate remains direct at both phi^2=1 ordinary endpoints.
assert_equal(A23.subs(phi, 1), m2.subs(phi, 1))
assert_equal(A23.subs(phi, -1), -m1.subs(phi, -1))
assert_equal(raw_support[(1, 1, 1, 1)].subs(phi, 1), -8)
assert_equal(raw_support[(1, 1, 1, 1)].subs(phi, -1), 8)

component_text = COMPONENT.read_text(encoding="utf-8")
assert "T_1111=4(q-phi)" in component_text
assert "phi!=0" in component_text

payload = {
    "status": "pass",
    "role": "verifier",
    "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "git_commit": git_commit(),
    "claim_label": "VERIFIED",
    "scope": (
        "component 19 ordinary p=0,q*phi=-1 shared weight-at-infinity "
        "chart on phi*(phi^2+1)!=0"
    ),
    "inputs": {COMPONENT.name: sha256(COMPONENT)},
    "method": (
        "fresh regular p0 basis, direct infinity contractions, saturated "
        "mixed-coefficient identity, and direct phi=+/-1 endpoint replay"
    ),
    "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "ordinary_tensor": "T1111=-4*(phi^2+1)/phi",
    "required_binary_diagonal": "A23=-2*(C1+C2)",
    "mixed_coefficients": [str(m1), str(m2)],
    "coefficient_determinant": str(coefficient_determinant),
    "incidence_certificate": (
        "A23=((1-phi)/(2*phi))*m1+((1+phi)/2)*m2"
    ),
    "genuine_shared_incidence": "empty",
    "target_local_compatibility": "vacuously empty after incidence obstruction",
    "phi_squared_1_included": True,
    "new_infinity_construction_artifacts_read_or_imported": False,
    "limitations": (
        "ordinary infinity chart only; no phi=0, phi^2=-1 zero tensor, "
        "finite weight, projectivized, valuative, closure, arbitrary-order, "
        "or global claim"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
