#!/usr/bin/env python3
"""Exact proof-B replay for the component-19 q=0, phi=+/-1 endpoints."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_PROOF_B.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
Q0_REPORT = ROOT / "P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_PROOF_B.md"
Q0_REPLAY = ROOT / "derive_p5_h22_component19_q0_special_divisor_proof_b.py"
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
h0, h1, h2, h3, lam, t = sp.symbols("h0 h1 h2 h3 lam t")
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
alpha0 = add(scale(-phi, Abar), scale(-phi * p, B), scale(-p, Bbar))
beta0 = add(Abar, scale(p, B))
planes = (
    (alpha0, beta0),
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
        expanded - sum(value * variable for value, variable in zip(vector, extension_variables))
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
assert {word: value for word, value in raw_tensor.items() if value != 0} == {
    (1, 1, 1, 1): 4 * p
}

pair_witnesses = {
    (0, 1): (3, (1, 2, 3), (0, 1, 3), -4 * p**2 * phi),
    (0, 2): (4, (1, 2, 3, 5), (0, 1, 2, 3), 8 * p**3),
    (0, 3): (4, (0, 1, 2, 5), (0, 1, 2, 3), -8 * p**2 * phi),
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

finite = {direction: tensor(direction) for direction in ("01", "23")}
infinite = {direction: tensor(direction, True) for direction in ("01", "23")}
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

Cc, Dd, Ee = sp.symbols("C D E")
endpoint_results = {}
for epsilon in (1, -1):
    branch = {
        phi: epsilon,
        lam: 1,
        h0: epsilon,
        h1: 0,
        h2: t,
        h3: 0,
    }
    branch_matrix = forward_matrix.subs(branch)
    v_c = sp.Matrix((0, -1 / p, epsilon / p, 0, 1, 0, 0, 0))
    v_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    v_e = sp.Matrix((epsilon * p, 0, -epsilon, 0, 0, 0, 0, 1))
    for vector in (v_c, v_d, v_e):
        assert branch_matrix * vector == sp.zeros(29, 1)
    kernel_minor = sp.factor(
        branch_matrix.extract(
            (2, 3, 11, 13, 16), (0, 1, 2, 3, 6)
        ).det()
    )
    assert_equal(kernel_minor, 1024 * p**3)

    extension = Cc * v_c + Dd * v_d + Ee * v_e
    extension_substitution = dict(
        zip(extension_variables, extension, strict=True)
    )
    B01 = sp.factor(
        finite["01"][(1, 1, 1, 1)].subs(branch).subs(extension_substitution)
    )
    A23 = sp.factor(
        finite["23"][(0, 0, 0, 0)].subs(branch).subs(extension_substitution)
    )
    B23 = sp.factor(
        finite["23"][(1, 1, 1, 1)].subs(branch).subs(extension_substitution)
    )
    F = Cc - p * Ee
    G = p * Dd - epsilon * t * F
    assert_equal(B01, 4 * G)
    assert_equal(A23, 4 * F / p)
    assert_equal(B23, 4 * Cc)

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
    marked_matrix = one_marked_matrix(branch_planes, 3)
    obstruction_minor = sp.factor(
        marked_matrix.extract((2, 3, 4, 7), range(4)).det()
    )
    assert_equal(obstruction_minor, -64 * epsilon * Cc * p * G**2)

    # The forward branch is unique and the infinity chart is empty.
    L = C1 * (lam - 1) + C2 * (lam + 1)
    assert_equal(finite["23"][(0, 0, 0, 0)], 2 * phi * L)
    assert_equal(finite["23"][(0, 0, 0, 1)], 2 * h3 * phi * L)
    assert_equal(finite["23"][(1, 0, 0, 0)], 2 * (h0 * phi - 1) * L)
    forced = {phi: epsilon, h3: 0, h0: epsilon}
    assert_equal(
        finite["01"][(1, 0, 0, 0)].subs(forced),
        2 * epsilon * C1 * p * (lam - 1),
    )
    assert_equal(
        finite["01"][(0, 0, 0, 0)].subs(forced),
        2 * p * (C1 - epsilon * C2) * (lam - 1),
    )
    assert_equal(
        finite["23"][(0, 1, 0, 0)].subs(forced).subs(lam, 1),
        4 * epsilon * C2 * h1,
    )
    infinity_L = C1 + C2
    assert_equal(infinite["23"][(0, 0, 0, 0)].subs(phi, epsilon), 2 * epsilon * infinity_L)
    assert_equal(
        infinite["01"][(1, 0, 0, 0)].subs(forced),
        2 * epsilon * C1 * p,
    )
    assert_equal(
        infinite["01"][(0, 0, 0, 0)].subs(forced),
        2 * p * (C1 - epsilon * C2),
    )

    # Reverse orientation: normalize the D01 all-alpha open by K=1.
    reverse = {phi: epsilon, h0: epsilon, h3: -1 / p, C1: 0, C2: -epsilon}
    A01 = finite["01"][(0, 0, 0, 0)].subs(reverse)
    reverse_A23 = finite["23"][(0, 0, 0, 0)].subs(reverse)
    assert_equal(A01, 2 * p * (lam - 1))
    assert_equal(reverse_A23, -2 * (lam + 1))
    reverse_at_minus_one = {**reverse, lam: -1, D1: 0, D2: 0, h1: 0}
    assert_equal(finite["01"][(1, 1, 1, 1)].subs(reverse_at_minus_one), 0)
    assert_equal(infinite["23"][(0, 0, 0, 0)].subs(reverse), -2)

    endpoint_results[str(epsilon)] = {
        "pair_profile": [3, 4, 4, 3, 3, 3],
        "finite_branch": f"lambda=1,h=({epsilon},0,t,0)",
        "kernel": [
            [str(value) for value in vector] for vector in (v_c, v_d, v_e)
        ],
        "kernel_rank": 5,
        "kernel_minor": str(kernel_minor),
        "diagonals": {"B01": str(B01), "A23": str(A23), "B23": str(B23)},
        "genuine_locus": str(sp.factor(Cc * F * G)),
        "obstruction_minor_rows_2347": str(obstruction_minor),
        "infinity_branch": "empty",
        "reverse_orientation": "empty",
    }

component_text = COMPONENT.read_text(encoding="utf-8")
q0_text = Q0_REPORT.read_text(encoding="utf-8")
assert "T_0111=4p" in component_text
assert "The `phi=+/-1` boundary" in q0_text

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
    "scope": "component 19 weighted H22 on q=0, phi=+1 and phi=-1, p!=0",
    "inputs": {
        path.name: sha256(path) for path in (COMPONENT, Q0_REPORT, Q0_REPLAY)
    },
    "method": (
        "fresh endpoint squarefree permanents, direct finite/infinity "
        "contractions, structural orientation case split, complete kernel "
        "vectors plus fixed rank minors, and a fixed one-marked minor"
    ),
    "command": f"uv run --with sympy python {SCRIPT.name}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "endpoints": endpoint_results,
    "candidate_artifacts_read": False,
    "limitations": (
        "p=0 is the zero-tensor/lower boundary and is excluded; no other "
        "projective component boundaries, arbitrary-order reduction, "
        "component exhaustiveness, prize graph, or global conclusion"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
