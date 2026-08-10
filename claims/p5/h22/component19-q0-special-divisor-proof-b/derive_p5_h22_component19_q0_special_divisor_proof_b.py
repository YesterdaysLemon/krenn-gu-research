#!/usr/bin/env python3
"""Bounded exact proof-B replay for component 19 on q=0."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_PROOF_B.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
GENERIC_THEOREM = ROOT / (
    "P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_"
    "GENERIC_OBSTRUCTION_VERIFICATION.md"
)
CONVENTION = ROOT / "claims/p5/h22/common-singleton/P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))
WORDS = tuple(itertools.product((0, 1), repeat=4))
p, phi = sp.symbols("p phi", nonzero=True)
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(4))


def scale(value, row):
    return tuple(sp.expand(value * entry) for entry in row)


alpha0 = add(scale(-phi, Abar), scale(-phi * p, B), scale(-p, Bbar))
beta0 = add(Abar, scale(p, B))
planes = (
    (alpha0, beta0),
    (B, A),
    (Bbar, A),
    (Abar, add(B, scale(phi, Bbar))),
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit():
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def assert_equal(actual, expected):
    assert sp.factor(actual - expected) == 0, (actual, expected)


def multiply(left, right):
    result = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return result


def permanent(rows):
    value = {0: sp.Integer(1)}
    for row in rows:
        value = multiply(
            value,
            {1 << i: entry for i, entry in enumerate(row) if entry != 0},
        )
    return sp.factor(value.get(15, 0))


tensor_values = {
    word: permanent(tuple(planes[i][word[i]] for i in range(4)))
    for word in WORDS
}
assert {
    word: value for word, value in tensor_values.items() if value != 0
} == {(1, 1, 1, 1): 4 * p}


def symmetric_product(left, right):
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def product_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(lrow, rrow) for lrow in left for rrow in right)
    )


pair_witnesses = {
    (0, 1): (3, (1, 2, 3), (0, 1, 3), -4 * p**2 * phi),
    (0, 2): (4, (1, 2, 3, 5), (0, 1, 2, 3), 8 * p**3),
    (0, 3): (4, (0, 1, 2, 5), (0, 1, 2, 3), -8 * p**2 * phi),
    (1, 2): (3, (0, 1, 2), (1, 2, 3), -4),
    (1, 3): (3, (1, 2, 5), (0, 1, 3), 4 * phi),
    (2, 3): (3, (1, 2, 5), (0, 1, 3), 4 * phi),
}
pair_profile = []
for pair, witness in pair_witnesses.items():
    rank, rows, columns, determinant = witness
    pair_matrix = product_matrix(planes[pair[0]], planes[pair[1]])
    assert_equal(pair_matrix.extract(rows, columns).det(), determinant)
    if rank == 3:
        for larger_rows in itertools.combinations(range(6), 4):
            assert pair_matrix.extract(larger_rows, range(4)).det() == 0
    pair_profile.append(rank)
assert pair_profile == [3, 4, 4, 3, 3, 3]


h0, h1, h2, h3, lam, t = sp.symbols("h0 h1 h2 h3 lam t")
h = (h0, h1, h2, h3)
C = sp.symbols("C0:4")
D = sp.symbols("D0:4")
extension_variables = (*C, *D)


def contract(row, extension, direction):
    if direction == "01":
        return (
            sp.expand(lam * row[0] + row[1]),
            row[2],
            row[3],
            extension,
        )
    if direction == "23":
        return (
            row[0],
            row[1],
            sp.expand(lam * row[2] + row[3]),
            extension,
        )
    raise ValueError(direction)


def contract_infinity(row, extension, direction):
    if direction == "01":
        return (row[0], row[2], row[3], extension)
    if direction == "23":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def contracted_planes(direction):
    result = []
    for i, (alpha, beta) in enumerate(planes):
        marked_beta = add(beta, scale(h[i], alpha))
        result.append(
            (
                contract(alpha, C[i], direction),
                contract(marked_beta, D[i], direction),
            )
        )
    return tuple(result)


def contracted_planes_infinity(direction):
    result = []
    for i, (alpha, beta) in enumerate(planes):
        marked_beta = add(beta, scale(h[i], alpha))
        result.append(
            (
                contract_infinity(alpha, C[i], direction),
                contract_infinity(marked_beta, D[i], direction),
            )
        )
    return tuple(result)


def coefficient_vector(expression):
    expression = sp.expand(expression)
    assert sp.expand(expression.subs(dict.fromkeys(extension_variables, 0))) == 0
    vector = tuple(sp.expand(expression.coeff(variable)) for variable in extension_variables)
    assert sp.expand(expression - sum(v * x for v, x in zip(vector, extension_variables))) == 0
    return vector


tensors = {}
for direction in ("01", "23"):
    direction_planes = contracted_planes(direction)
    tensors[direction] = {
        word: permanent(tuple(direction_planes[i][word[i]] for i in range(4)))
        for word in WORDS
    }

infinity_tensors = {}
for direction in ("01", "23"):
    direction_planes = contracted_planes_infinity(direction)
    infinity_tensors[direction] = {
        word: permanent(tuple(direction_planes[i][word[i]] for i in range(4)))
        for word in WORDS
    }

rows01 = [coefficient_vector(tensors["01"][word]) for word in WORDS if word != (1, 1, 1, 1)]
rows23 = [
    coefficient_vector(tensors["23"][word])
    for word in WORDS
    if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
]
matrix = sp.Matrix(rows01 + rows23)
branch = {lam: 1, h0: 1 / phi, h1: 0, h2: t, h3: 0}
branch_matrix = matrix.subs(branch)
CC, DD = sp.symbols("CC DD")
zC = sp.Matrix((0, -1 / p, phi / p, 0, 1, 0, 0, 0))
zD = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
assert branch_matrix * zC == sp.zeros(29, 1)
assert branch_matrix * zD == sp.zeros(29, 1)
branch_minor = sp.factor(
    branch_matrix.extract(
        (2, 3, 5, 11, 13, 16), (0, 1, 2, 3, 6, 7)
    ).det()
)
assert_equal(branch_minor, 4096 * p**4 * phi**2 * (phi**2 - 1))
extension = CC * zC + DD * zD


def evaluate(expression, *substitutions):
    value = expression
    for substitution in substitutions:
        value = value.subs(substitution)
    return sp.factor(value)


B01 = tensors["01"][(1, 1, 1, 1)]
A23 = tensors["23"][(0, 0, 0, 0)]
B23 = tensors["23"][(1, 1, 1, 1)]
extension_substitution = dict(zip(extension_variables, extension, strict=True))
branch_diagonals = {
    "B01": evaluate(B01, branch, extension_substitution),
    "A23": evaluate(A23, branch, extension_substitution),
    "B23": evaluate(B23, branch, extension_substitution),
}
assert_equal(branch_diagonals["B01"], 4 * (p * DD - phi * t * CC))
assert_equal(branch_diagonals["A23"], 4 * CC * phi**2 / p)
assert_equal(branch_diagonals["B23"], 4 * CC)


def one_marked_matrix(direction_planes, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    basis = tuple(
        tuple(sp.Integer(index == coordinate) for index in range(4))
        for coordinate in range(4)
    )
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        fixed_rows = tuple(
            direction_planes[mode][bit]
            for mode, bit in zip(other_modes, word, strict=True)
        )
        rows.append([permanent((*fixed_rows, basis_row)) for basis_row in basis])
    return sp.Matrix(rows)


branch_d01_planes = tuple(
    tuple(
        tuple(
            sp.factor(
                sp.sympify(entry)
                .subs(branch)
                .subs(dict(zip(extension_variables, extension)))
            )
            for entry in row
        )
        for row in plane
    )
    for plane in contracted_planes("01")
)
one_marked = one_marked_matrix(branch_d01_planes, 3)
one_marked_minor = sp.factor(
    one_marked.extract((1, 2, 5, 7), range(4)).det()
)
assert_equal(one_marked_minor, -64 * CC * p * (p * DD - phi * t * CC) ** 2)

# The displayed equations give a direct, non-Groebner proof of the shared branch.
L = C[1] * (lam - 1) + C[2] * (lam + 1)
assert_equal(A23, 2 * phi * L)
assert_equal(tensors["23"][(0, 0, 0, 1)], 2 * h3 * phi * L)
assert_equal(tensors["23"][(1, 0, 0, 0)], 2 * (h0 * phi - 1) * L)
forced = {h3: 0, h0: 1 / phi}
assert_equal(
    evaluate(tensors["01"][(1, 0, 0, 0)], forced),
    2 * C[1] * p * (lam - 1) / phi,
)
assert_equal(
    evaluate(tensors["01"][(0, 0, 0, 0)], forced),
    2 * p * (C[1] - phi * C[2]) * (lam - 1),
)
assert_equal(
    evaluate(tensors["23"][(0, 1, 0, 0)], forced, {lam: 1}),
    4 * phi * C[2] * h1,
)

# At infinity, A23-open forces h3=0 and h0=1/phi; two D01 equations
# then force C1=C2=0, contradicting A23-open.
infinity_A23 = infinity_tensors["23"][(0, 0, 0, 0)]
infinity_L = C[1] + C[2]
assert_equal(infinity_A23, 2 * phi * infinity_L)
assert_equal(
    infinity_tensors["23"][(0, 0, 0, 1)],
    2 * h3 * phi * infinity_L,
)
assert_equal(
    infinity_tensors["23"][(1, 0, 0, 0)],
    2 * (h0 * phi - 1) * infinity_L,
)
assert_equal(
    evaluate(infinity_tensors["01"][(0, 0, 0, 0)], forced),
    2 * p * (C[1] - phi * C[2]),
)
assert_equal(
    evaluate(infinity_tensors["01"][(1, 0, 0, 0)], forced),
    2 * p * C[1] / phi,
)

# D01 finite binary-open normalization: K=C1-phi*C2=1.
binary_substitution = {
    C[1]: 1 - phi * h0,
    C[2]: -h0,
    h3: (phi * (phi**2 - 1) * h0 - phi**2) / p,
}
binary_split = evaluate(tensors["01"][(1, 0, 0, 1)], binary_substitution)
assert_equal(
    binary_split,
    -2
    * (lam - 1)
    * (h0 * phi - 1)
    * (h0 * phi**2 - h0 - phi),
)
infinity_binary_split = evaluate(
    infinity_tensors["01"][(1, 0, 0, 1)], binary_substitution
)
assert_equal(
    infinity_binary_split,
    -2 * (h0 * phi - 1) * (h0 * phi**2 - h0 - phi),
)

# The excluded phi=+/-1 endpoints have an exact rank-five jump.
boundary_data = {}
for phi_value in (1, -1):
    boundary_matrix = branch_matrix.subs(phi, phi_value)
    boundary_vc = zC.subs(phi, phi_value)
    boundary_extra = sp.Matrix(
        (p * phi_value, 0, -phi_value, 0, 0, 0, 0, 1)
    )
    assert boundary_matrix * boundary_vc == sp.zeros(29, 1)
    assert boundary_matrix * zD == sp.zeros(29, 1)
    assert boundary_matrix * boundary_extra == sp.zeros(29, 1)
    boundary_minor = sp.factor(
        boundary_matrix.extract(
            (2, 3, 11, 13, 16), (0, 1, 2, 3, 6)
        ).det()
    )
    assert_equal(boundary_minor, 1024 * p**3)
    boundary_data[str(phi_value)] = {
        "rank": 5,
        "extra_kernel_vector": [str(value) for value in boundary_extra],
        "fixed_minor": str(boundary_minor),
    }

source_component = COMPONENT.read_text(encoding="utf-8")
source_theorem = GENERIC_THEOREM.read_text(encoding="utf-8")
source_convention = CONVENTION.read_text(encoding="utf-8")
assert "T_0111=4p" in source_component
assert "lambda=1" in source_theorem
assert "D_01^(lambda:mu)" in source_convention

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
    "scope": "component 19 weighted H22 on q=0 with p*phi*(phi^2-1)!=0",
    "inputs": {
        path.name: sha256(path)
        for path in (COMPONENT, GENERIC_THEOREM, CONVENTION)
    },
    "method": (
        "fresh subset-algebra permanents, fixed pair minors, direct finite/"
        "infinity contraction equations, structural case splits, and fixed "
        "extension/one-marked minors; no Groebner basis"
    ),
    "command": f"uv run --with sympy python {SCRIPT.name}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "pair_profile": pair_profile,
    "finite_shared_branch": {
        "marking": "lambda=1,h=(1/phi,0,t,0)",
        "kernel": [
            [str(value) for value in zC],
            [str(value) for value in zD],
        ],
        "rank_six_minor": str(branch_minor),
        "diagonals": {key: str(value) for key, value in branch_diagonals.items()},
        "genuine_open": "C*(p*D-phi*t*C)!=0",
    },
    "infinity_shared_branch": "empty",
    "one_marked_minor_rows_1257": str(one_marked_minor),
    "phi_endpoints": boundary_data,
    "limitations": (
        "the phi=+/-1 rank-jump endpoints are recorded but not closed; no "
        "other parameter/projective boundaries, arbitrary-order reduction, "
        "component exhaustiveness, prize graph, or global conclusion"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
