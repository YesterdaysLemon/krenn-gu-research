#!/usr/bin/env python3
"""Exact proof-B replay for the ordinary component-19 p=0 boundary."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_P0_ORDINARY_OPEN_PROOF_B.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


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
    return sp.factor(value.get(15, 0))


def symmetric_product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def product_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(symmetric_product(lrow, rrow) for lrow in left for rrow in right)
    )


q, phi = sp.symbols("q phi", nonzero=True)
h0, h1, h2, h3, lam, t = sp.symbols("h0 h1 h2 h3 lam t")
C0, C1, C2, C3 = sp.symbols("C0 C1 C2 C3")
D0, D1, D2, D3 = sp.symbols("D0 D1 D2 D3")
X, Y, Z = sp.symbols("X Y Z")
extension_variables = (C0, C1, C2, C3, D0, D1, D2, D3)
h = (h0, h1, h2, h3)
C_rows = (C0, C1, C2, C3)
D_rows = (D0, D1, D2, D3)
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)

# Regular replacement for the singular generic pure basis at p=0.
planes = (
    (Abar, add(Bbar, scale(q, B))),
    (B, A),
    (Bbar, A),
    (Abar, add(B, scale(phi, Bbar))),
)


def contract(row, extension, direction, infinity=False):
    if direction == "01":
        first = row[0] if infinity else lam * row[0] + row[1]
        return (sp.expand(first), row[2], row[3], extension)
    if direction == "23":
        third = row[2] if infinity else lam * row[2] + row[3]
        return (row[0], row[1], sp.expand(third), extension)
    raise ValueError(direction)


def contracted_planes(direction, infinity=False):
    result = []
    for mode, (alpha, beta) in enumerate(planes):
        marked_beta = add(beta, scale(h[mode], alpha))
        result.append(
            (
                contract(alpha, C_rows[mode], direction, infinity),
                contract(marked_beta, D_rows[mode], direction, infinity),
            )
        )
    return tuple(result)


def tensor(direction, infinity=False):
    direction_planes = contracted_planes(direction, infinity)
    return {
        word: permanent(tuple(direction_planes[i][word[i]] for i in range(4)))
        for word in WORDS
    }


def coefficient_vector(expression):
    expanded = sp.expand(expression)
    vector = tuple(expanded.coeff(variable) for variable in extension_variables)
    assert sp.expand(
        expanded
        - sum(
            value * variable
            for value, variable in zip(vector, extension_variables, strict=True)
        )
    ) == 0
    return vector


def one_marked_matrix(direction_planes, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    basis = tuple(
        tuple(sp.Integer(index == coordinate) for index in range(4))
        for coordinate in range(4)
    )
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        fixed = tuple(
            direction_planes[mode][bit]
            for mode, bit in zip(other_modes, word, strict=True)
        )
        rows.append([permanent((*fixed, basis_row)) for basis_row in basis])
    return sp.Matrix(rows)


raw_tensor = {
    word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
    for word in WORDS
}
raw_support = {word: value for word, value in raw_tensor.items() if value != 0}
assert raw_support.keys() == {(1, 1, 1, 1)}
assert_equal(raw_support[(1, 1, 1, 1)], 4 * (q - phi))

pair_witnesses = {
    (0, 1): (3, (1, 2, 5), (0, 2, 3), 4 * q),
    (0, 2): (3, (1, 2, 5), (0, 2, 3), 4 * q),
    (0, 3): (
        4,
        (0, 1, 2, 5),
        (0, 1, 2, 3),
        -8 * (q - phi) * (phi * q - 1),
    ),
    (1, 2): (3, (0, 1, 2), (1, 2, 3), -4),
    (1, 3): (3, (1, 2, 5), (0, 1, 3), 4 * phi),
    (2, 3): (3, (1, 2, 5), (0, 1, 3), 4 * phi),
}
for pair, (rank, rows, columns, expected) in pair_witnesses.items():
    pair_matrix = product_matrix(planes[pair[0]], planes[pair[1]])
    assert_equal(pair_matrix.extract(rows, columns).det(), expected)
    if rank == 3:
        for larger_rows in itertools.combinations(range(6), 4):
            assert pair_matrix.extract(larger_rows, range(4)).det() == 0

special_03 = product_matrix(planes[0], planes[3]).subs(q, 1 / phi)
assert_equal(
    special_03.extract((0, 1, 5), (0, 1, 3)).det(),
    4 * (phi - 1) * (phi + 1) ** 2 / phi,
)
for larger_rows in itertools.combinations(range(6), 4):
    assert special_03.extract(larger_rows, range(4)).det() == 0

finite = {direction: tensor(direction) for direction in ("01", "23")}
infinite = {direction: tensor(direction, True) for direction in ("01", "23")}

# D01 can never be binary; D23 is the only possible binary side.
assert finite["01"][(0, 0, 0, 0)] == 0
assert infinite["01"][(0, 0, 0, 0)] == 0

L = C1 * (lam - 1) + C2 * (lam + 1)
assert_equal(finite["23"][(0, 0, 0, 0)], -2 * L)
assert_equal(finite["23"][(0, 0, 0, 1)], -2 * h3 * L)
assert_equal(finite["23"][(1, 0, 0, 0)], -2 * h0 * L)
assert_equal(
    finite["01"][(0, 0, 0, 1)],
    -2 * (lam - 1) * (phi * C1 - C2),
)
assert_equal(
    finite["01"][(1, 0, 0, 0)],
    2 * (lam - 1) * (-C1 + q * C2),
)

# Off phi*q=1, the complete finite branch is lambda=1,h=(0,0,t,0).
branch = {lam: 1, h0: 0, h1: 0, h2: t, h3: 0}
forward_matrix = sp.Matrix(
    [
        coefficient_vector(finite["01"][word])
        for word in WORDS
        if word != (1, 1, 1, 1)
    ]
    + [
        coefficient_vector(finite["23"][word])
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
)
branch_matrix = forward_matrix.subs(branch)
r = q - phi
v_x = sp.Matrix((0, -1 / r, phi / r, 0, 1, 0, 0, 0))
v_y = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
v_z = sp.Matrix((0, -q / r, 1 / r, 0, 0, 0, 0, 1))
for vector in (v_x, v_y, v_z):
    assert all(sp.factor(value) == 0 for value in branch_matrix * vector)
kernel_minor = sp.factor(
    branch_matrix.extract((3, 10, 11, 13, 16), (0, 1, 2, 3, 6)).det()
)
assert_equal(kernel_minor, -1024 * q * r**2)

extension = X * v_x + Y * v_y + Z * v_z
extension_substitution = dict(zip(extension_variables, extension, strict=True))
B01 = sp.factor(
    finite["01"][(1, 1, 1, 1)].subs(branch).subs(extension_substitution)
)
A23 = sp.factor(
    finite["23"][(0, 0, 0, 0)].subs(branch).subs(extension_substitution)
)
B23 = sp.factor(
    finite["23"][(1, 1, 1, 1)].subs(branch).subs(extension_substitution)
)
F = phi * X + Z
H = X + q * Z
G = r * Y - t * F
assert_equal(B01, 4 * G)
assert_equal(A23, -4 * F / r)
assert_equal(B23, 4 * H)

branch_planes = tuple(
    tuple(
        tuple(
            sp.factor(
                sp.sympify(entry)
                .subs(branch)
                .subs(extension_substitution)
            )
            for entry in row
        )
        for row in plane
    )
    for plane in contracted_planes("01")
)
mode0_matrix = one_marked_matrix(branch_planes, 0)
mode3_matrix = one_marked_matrix(branch_planes, 3)
minor0 = sp.factor(mode0_matrix.extract((1, 3, 5, 7), range(4)).det())
minor3 = sp.factor(mode3_matrix.extract((4, 5, 6, 7), range(4)).det())
expected_minor0 = 64 * Z * (phi**2 - 1) * (2 * phi * X + (phi * q + 1) * Z) * G / r**2
expected_minor3 = -64 * X * (q**2 - 1) * ((phi * q + 1) * X + 2 * q * Z) * G / r**2
assert_equal(minor0, expected_minor0)
assert_equal(minor3, expected_minor3)

# Each mode has only this one four-minor generator, up to sign.
for matrix, generator in ((mode0_matrix, minor0), (mode3_matrix, minor3)):
    values = {
        sp.factor(matrix.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(8), 4)
    }
    assert values <= {sp.Integer(0), generator, -generator}

simultaneous_linear_determinant = sp.factor(
    sp.Matrix(((2 * phi, phi * q + 1), (phi * q + 1, 2 * q))).det()
)
assert_equal(simultaneous_linear_determinant, -(phi * q - 1) ** 2)

# At infinity, off phi*q=1, the D23 binary open is impossible.
infinity_L = C1 + C2
assert_equal(infinite["23"][(0, 0, 0, 0)], -2 * infinity_L)
assert_equal(infinite["23"][(0, 0, 0, 1)], -2 * h3 * infinity_L)
assert_equal(infinite["23"][(1, 0, 0, 0)], -2 * h0 * infinity_L)
assert_equal(infinite["01"][(0, 0, 0, 1)], -2 * (phi * C1 - C2))
assert_equal(infinite["01"][(1, 0, 0, 0)], 2 * (-C1 + q * C2))

component_text = COMPONENT.read_text(encoding="utf-8")
assert "T_0111=4p" in component_text
assert "T_1111=4(q-phi)" in component_text

payload = {
    "status": "pass",
    "role": "proof_b",
    "date_utc": datetime.now(UTC)
    .replace(microsecond=0)
    .isoformat()
    .replace("+00:00", "Z"),
    "git_commit": git_commit(),
    "claim_label": "VERIFIED",
    "discovery_claim_label": "DERIVED",
    "scope": "ordinary component-19 p=0 boundary on q*phi*(q-phi)!=0",
    "inputs": {COMPONENT.name: sha256(COMPONENT)},
    "method": (
        "regular replacement basis, subset-algebra permanents, fixed pair "
        "and kernel minors, direct finite/infinity compatibility, complete "
        "kernel vectors, and complete one-marked four-minor generators"
    ),
    "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "ordinary_tensor": {"support": {"1111": "4*(q-phi)"}},
    "nonzero_all_pair_open": "q*phi*(q-phi)!=0",
    "pair_profiles": {
        "phi*q!=1": [3, 3, 4, 3, 3, 3],
        "phi*q=1": [3, 3, 3, 3, 3, 3],
    },
    "generic_compatibility": {
        "parameter_open": "phi*q!=1",
        "finite_branch": "lambda=1,h=(0,0,t,0)",
        "infinity_branch": "empty",
        "kernel_rank": 5,
        "kernel": [[str(value) for value in vector] for vector in (v_x, v_y, v_z)],
        "kernel_minor": str(kernel_minor),
        "genuine_locus": "F*G*H!=0",
        "F_G_H": [str(F), str(G), str(H)],
    },
    "obstruction_open": {
        "exact_union": "genuine and (M0!=0 or M3!=0)",
        "M0": str(minor0),
        "M3": str(minor3),
        "complete_parameter_open": (
            "q*phi*(q-phi)*(q^2-1)*(phi^2-1)*"
            "((q*phi)^2-1)!=0"
        ),
    },
    "claim": "weighted H22 fibre empty on the obstruction open",
    "unknown": [
        "q=+/-1",
        "phi=+/-1",
        "q*phi=1 compatibility divisor and all intersections",
        "q*phi=-1 with X*Z=0 on the rank-safe genuine locus",
        "other simultaneous M0=M3=0 extension subloci",
        "q=phi zero tensor and its projectivized transverse directions (deferred)",
    ],
    "candidate_artifacts_read": False,
    "limitations": (
        "this is an obstruction-open theorem, not closure across the listed "
        "rank-safe loci; q=0 is not all-pair-open and phi=0 is outside the "
        "component torus; no arbitrary-order reduction or global conclusion"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
