#!/usr/bin/env python3
"""Exact proof-B replay for component 19 on the divisor q=phi."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_Q_EQUALS_PHI_DIVISOR_PROOF_B.md"
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


p, phi = sp.symbols("p phi", nonzero=True)
h0, h1, h2, h3, lam = sp.symbols("h0 h1 h2 h3 lam")
C0, C1, C2, C3 = sp.symbols("C0 C1 C2 C3")
D0, D1, D2, D3 = sp.symbols("D0 D1 D2 D3")
extension_variables = (C0, C1, C2, C3, D0, D1, D2, D3)
h = (h0, h1, h2, h3)
C_rows = (C0, C1, C2, C3)
D_rows = (D0, D1, D2, D3)
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)

# This basis is regular on q=phi; it does not divide by q-phi.
planes = (
    (add(Bbar, scale(phi, B)), add(Abar, scale(p, B))),
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


raw_tensor = {
    word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
    for word in WORDS
}
assert {word: value for word, value in raw_tensor.items() if value != 0} == {
    (1, 1, 1, 1): 4 * p
}

pair_witnesses = {
    (0, 1): (4, (1, 2, 3, 5), (0, 1, 2, 3), -8 * p * phi),
    (0, 2): (4, (1, 2, 3, 5), (0, 1, 2, 3), 8 * p),
    (0, 3): (3, (1, 2, 5), (0, 2, 3), 4 * p**2),
    (1, 2): (3, (0, 1, 2), (1, 2, 3), -4),
    (1, 3): (3, (1, 2, 5), (0, 1, 3), 4 * phi),
    (2, 3): (3, (1, 2, 5), (0, 1, 3), 4 * phi),
}
pair_profile = []
for pair, (rank, rows, columns, expected) in pair_witnesses.items():
    pair_matrix = product_matrix(planes[pair[0]], planes[pair[1]])
    assert_equal(pair_matrix.extract(rows, columns).det(), expected)
    if rank == 3:
        for larger_rows in itertools.combinations(range(6), 4):
            assert pair_matrix.extract(larger_rows, range(4)).det() == 0
    pair_profile.append(rank)
assert pair_profile == [4, 4, 3, 3, 3, 3]

finite = {direction: tensor(direction) for direction in ("01", "23")}
infinite = {direction: tensor(direction, True) for direction in ("01", "23")}

# D23 can never be the binary direction on either weight chart.
assert finite["23"][(0, 0, 0, 0)] == 0
assert infinite["23"][(0, 0, 0, 0)] == 0

# Analyze the only possible orientation: D01 binary and D23 pure.
K = C1 - phi * C2
A01 = finite["01"][(0, 0, 0, 0)]
assert_equal(A01, -2 * K * (lam - 1))
assert_equal(finite["01"][(0, 0, 0, 1)], -2 * h3 * K * (lam - 1))
assert_equal(
    finite["01"][(1, 0, 0, 0)],
    2 * (lam - 1) * (-h0 * K + p * C2),
)
assert_equal(
    finite["01"][(1, 0, 0, 1)].subs(h3, 0),
    2 * (lam - 1) * (-phi * C1 + C2),
)

# On A01-open, scale K=1. These are the only possible finite data.
core_branch = {
    lam: (1 - phi) / (1 + phi),
    h0: p * phi / (1 - phi**2),
    h3: 0,
}
normalized_extension = {
    C0: 0,
    C1: 1 / (1 - phi**2),
    C2: phi / (1 - phi**2),
    C3: 0,
    D1: h1 / (1 - phi**2),
    D2: phi * h2 / (1 - phi**2),
    D3: 0,
}
normal_shared = {**core_branch, **normalized_extension}

weight_equation = finite["23"][(1, 0, 0, 0)]
assert_equal(
    weight_equation.subs({C1: 1 / (1 - phi**2), C2: phi / (1 - phi**2)}),
    -2 * ((1 + phi) * lam + phi - 1) / (1 - phi**2),
)
assert_equal(
    finite["01"][(0, 0, 1, 0)].subs(normal_shared),
    4 * h2 * phi / (phi + 1),
)
assert_equal(
    finite["01"][(0, 1, 0, 0)].subs(normal_shared),
    4 * h1 * phi / (phi + 1),
)

forced_branch = {**core_branch, h1: 0, h2: 0}
reverse_matrix = sp.Matrix(
    [
        coefficient_vector(finite["01"][word])
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    + [
        coefficient_vector(finite["23"][word])
        for word in WORDS
        if word != (1, 1, 1, 1)
    ]
)
forced_matrix = reverse_matrix.subs(forced_branch)
full_rank_rows = (1, 2, 3, 4, 7, 10, 12, 24)
full_rank_minor = sp.factor(
    forced_matrix.extract(full_rank_rows, range(8)).det()
)
assert_equal(full_rank_minor, -131072 * p**2 * phi**4 / (phi + 1) ** 8)

# A transparent incompatibility certificate after K=1 gives the same result.
equation_1011 = sp.factor(finite["01"][(1, 0, 1, 1)].subs(normal_shared))
equation_1101 = sp.factor(finite["01"][(1, 1, 0, 1)].subs(normal_shared))
assert_equal(
    equation_1011,
    -4 * (-D0 * phi**2 + D0 + p) / ((phi - 1) * (phi + 1) ** 2),
)
assert_equal(
    equation_1101,
    -4
    * phi
    * (D0 * phi**2 - D0 + p)
    / ((phi - 1) * (phi + 1) ** 2),
)

# Direct infinity equations: K-open implies C2=phi*C1, then D23 purity fails.
assert_equal(infinite["01"][(0, 0, 0, 0)], -2 * K)
assert_equal(infinite["01"][(0, 0, 0, 1)], -2 * h3 * K)
assert_equal(
    infinite["01"][(1, 0, 0, 0)], 2 * (-h0 * K + p * C2)
)
assert_equal(
    infinite["01"][(1, 0, 0, 1)].subs(h3, 0),
    2 * (-phi * C1 + C2),
)
assert_equal(infinite["23"][(1, 0, 0, 0)], -2 * (C1 + C2))

component_text = COMPONENT.read_text(encoding="utf-8")
assert "U_0=span(A_bar+pB, B_bar+qB)" in component_text
assert "(p,q-phi)!=(0,0)" in component_text

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
    "scope": "component 19 weighted H22 on q=phi with p*phi!=0",
    "inputs": {COMPONENT.name: sha256(COMPONENT)},
    "method": (
        "regular intrinsic basis, subset-algebra permanents, fixed pair "
        "minors, direct finite/infinity equations, normalized compatibility "
        "identities, and a fixed full-rank extension minor"
    ),
    "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "pure_support": {"1111": "4*p"},
    "all_pair_open": "p*phi!=0",
    "pair_profile": pair_profile,
    "D23_binary_orientation": "empty: all-alpha diagonal identically zero",
    "D01_binary_finite": {
        "phi=+/-1": "empty at the binary diagonal open",
        "phi^2!=1_candidate": (
            "lambda=(1-phi)/(1+phi), "
            "h=(p*phi/(1-phi^2),0,0,0)"
        ),
        "complete_extension_kernel": "zero",
        "fixed_rank_eight_minor": str(full_rank_minor),
        "incompatibility_equations": [str(equation_1011), str(equation_1101)],
    },
    "D01_binary_infinity": "empty",
    "weighted_H22_fibre": "empty",
    "candidate_artifacts_read": False,
    "limitations": (
        "p=0 is the zero-tensor boundary and phi=0 is outside the component "
        "torus; no other projective boundaries, arbitrary-order reduction, "
        "component exhaustiveness, prize graph, or global conclusion"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
