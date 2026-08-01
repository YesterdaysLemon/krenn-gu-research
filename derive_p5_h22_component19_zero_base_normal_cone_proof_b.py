#!/usr/bin/env python3
"""Proof-B replay for the component-19 zero-base normal cone."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_ZERO_BASE_NORMAL_CONE_PROOF_B.md"
COMPONENT = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
DEPENDENCIES = (
    ROOT / "P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md",
    ROOT / "P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md",
    ROOT / "P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md",
    ROOT / "P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md",
)
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
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
    return sp.factor(value.get((1 << len(rows)) - 1, 0))


def symmetric_product(left, right):
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def product_matrix(left, right):
    return sp.Matrix.hstack(
        *(symmetric_product(lrow, rrow) for lrow in left for rrow in right)
    )


def contract(row, extension, direction, weight, infinity=False):
    if direction == "01":
        first = row[0] if infinity else weight * row[0] + row[1]
        return (sp.expand(first), row[2], row[3], extension)
    if direction == "23":
        third = row[2] if infinity else weight * row[2] + row[3]
        return (row[0], row[1], sp.expand(third), extension)
    raise ValueError(direction)


def contracted_tensor(planes, direction, weight, h, C, D, infinity=False):
    contracted = []
    for mode, (alpha, beta) in enumerate(planes):
        marked_beta = add(beta, scale(h[mode], alpha))
        contracted.append(
            (
                contract(alpha, C[mode], direction, weight, infinity),
                contract(marked_beta, D[mode], direction, weight, infinity),
            )
        )
    return {
        word: permanent(tuple(contracted[i][word[i]] for i in range(4)))
        for word in WORDS4
    }


def restrict_full(row, direction, weight):
    if direction == "01":
        return (sp.expand(weight * row[0] + row[1]), row[2], row[3], row[4])
    return (row[0], row[1], sp.expand(weight * row[2] + row[3]), row[4])


def full_one_marked_map(full_planes, direction, weight, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    basis = tuple(
        tuple(sp.Integer(index == coordinate) for index in range(5))
        for coordinate in range(5)
    )
    rows = []
    for word in WORDS3:
        fixed = tuple(
            restrict_full(full_planes[mode][bit], direction, weight)
            for mode, bit in zip(other_modes, word, strict=True)
        )
        rows.append(
            [
                permanent((*fixed, restrict_full(basis_row, direction, weight)))
                for basis_row in basis
            ]
        )
    return sp.Matrix(rows)


phi, p, q, tau, a, b = sp.symbols("phi p q tau a b", nonzero=True)
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)

# Exact source-family restriction and first normal coefficient.
source_planes = (
    (add(Abar, scale(p, B)), add(Bbar, scale(q, B))),
    (B, A),
    (Bbar, A),
    (Abar, add(B, scale(phi, Bbar))),
)
source_tensor = {
    word: permanent(tuple(source_planes[mode][word[mode]] for mode in range(4)))
    for word in WORDS4
}
source_support = {word: value for word, value in source_tensor.items() if value != 0}
assert source_support.keys() == {(0, 1, 1, 1), (1, 1, 1, 1)}
assert_equal(source_support[(0, 1, 1, 1)], 4 * p)
assert_equal(source_support[(1, 1, 1, 1)], 4 * (q - phi))
linear_arc = {p: a * tau, q: phi + b * tau}
assert_equal(source_tensor[(0, 1, 1, 1)].subs(linear_arc) / tau, 4 * a)
assert_equal(source_tensor[(1, 1, 1, 1)].subs(linear_arc) / tau, 4 * b)

# Frozen base pair witnesses; only edge 03 can drop below rank three.
base_planes = tuple(
    tuple(tuple(sp.sympify(entry).subs({p: 0, q: phi}) for entry in row) for row in plane)
    for plane in source_planes
)
pair_witnesses = {
    (0, 1): ((1, 2, 5), (0, 2, 3), 4 * phi),
    (0, 2): ((1, 2, 5), (0, 2, 3), 4 * phi),
    (0, 3): ((0, 1, 2), (0, 1, 2), -4 * (phi**2 - 1)),
    (1, 2): ((0, 1, 2), (1, 2, 3), -4),
    (1, 3): ((1, 2, 5), (0, 1, 3), 4 * phi),
    (2, 3): ((1, 2, 5), (0, 1, 3), 4 * phi),
}
for pair, (rows, columns, expected) in pair_witnesses.items():
    matrix = product_matrix(base_planes[pair[0]], base_planes[pair[1]])
    assert_equal(matrix.extract(rows, columns).det(), expected)

# Fresh finite/infinity endpoint calculation for phi=e and p*r!=0.
r, weight, t = sp.symbols("r lambda t", nonzero=True)
h_symbols = sp.symbols("h0:4")
C_symbols = sp.symbols("C0:4")
D_symbols = sp.symbols("D0:4")
extension_variables = C_symbols + D_symbols
endpoint_results = {}
for epsilon in (1, -1):
    endpoint_planes = (
        (
            add(scale(r, Abar), scale(-p, add(Bbar, scale(epsilon, B)))),
            add(Abar, scale(p, B)),
        ),
        (B, A),
        (Bbar, A),
        (Abar, add(B, scale(epsilon, Bbar))),
    )
    finite = {
        direction: contracted_tensor(
            endpoint_planes,
            direction,
            weight,
            h_symbols,
            C_symbols,
            D_symbols,
        )
        for direction in ("01", "23")
    }

    # Complete D23-binary branch.
    branch = {
        weight: 1,
        h_symbols[0]: -1 / r,
        h_symbols[1]: 0,
        h_symbols[2]: t,
        h_symbols[3]: 0,
    }
    unwanted = [
        finite["01"][word]
        for word in WORDS4
        if word != (1, 1, 1, 1)
    ] + [
        finite["23"][word]
        for word in WORDS4
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    branch_matrix = sp.Matrix(
        [
            [
                sp.expand(expression.subs(branch)).coeff(variable)
                for variable in extension_variables
            ]
            for expression in unwanted
        ]
    )
    v_x = sp.Matrix((0, -1 / p, epsilon / p, 0, 1, 0, 0, 0))
    v_y = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    v_z = sp.Matrix(
        (epsilon * p, -(r + epsilon) / r, 1 / r, 0, 0, 0, 0, 1)
    )
    for vector in (v_x, v_y, v_z):
        assert all(sp.factor(value) == 0 for value in branch_matrix * vector)
    kernel_minor = sp.factor(
        branch_matrix.extract((2, 3, 11, 13, 16), (0, 1, 2, 3, 6)).det()
    )
    # A row-order variant of the fixed nonzero rank-five witness is accepted.
    assert kernel_minor != 0
    assert branch_matrix.rank() == 5

    X, Y, Z = sp.symbols("X Y Z")
    extension = X * v_x + Y * v_y + Z * v_z
    extension_sub = dict(zip(extension_variables, extension, strict=True))
    F = epsilon * X * r + Z * p
    G = p * r * Y - t * F
    H = X * r + Z * p * r + epsilon * Z * p
    B01 = sp.factor(
        finite["01"][(1, 1, 1, 1)].subs(branch).subs(extension_sub)
    )
    A23 = sp.factor(
        finite["23"][(0, 0, 0, 0)].subs(branch).subs(extension_sub)
    )
    B23 = sp.factor(
        finite["23"][(1, 1, 1, 1)].subs(branch).subs(extension_sub)
    )
    assert_equal(B01, 4 * G / r)
    assert_equal(A23, -4 * F / p)
    assert_equal(B23, 4 * H / r)

    full_planes = []
    for mode, (alpha, beta) in enumerate(endpoint_planes):
        alpha5 = tuple(map(sp.sympify, alpha)) + (extension[mode],)
        marked_beta = add(beta, scale(branch[h_symbols[mode]], alpha))
        beta5 = tuple(map(sp.sympify, marked_beta)) + (extension[4 + mode],)
        full_planes.append((alpha5, beta5))
    marked_map = full_one_marked_map(tuple(full_planes), "23", 1, 3)
    marked_minor = sp.factor(
        marked_map.extract((0, 2, 3, 7), (0, 1, 2, 4)).det()
    )
    assert_equal(marked_minor, 64 * F**2 * H / r**2)

    # Reverse finite orientation: normalize K=C1-e*C2=1 and A23=0.
    reverse_weight = r / (r + 2) if epsilon == 1 else (r - 2) / r
    denominator = (epsilon + 1) * weight + 1 - epsilon
    reverse_sub = {
        weight: reverse_weight,
        C_symbols[1]: sp.factor(((weight + 1) / denominator).subs(weight, reverse_weight)),
        C_symbols[2]: sp.factor(((1 - weight) / denominator).subs(weight, reverse_weight)),
        h_symbols[0]: sp.factor((-(1 - weight) / denominator).subs(weight, reverse_weight)),
        h_symbols[3]: epsilon * r / p,
    }
    reverse_equations = []
    for direction in ("01", "23"):
        for word in WORDS4:
            if word in ((0, 0, 0, 0), (1, 1, 1, 1)):
                continue
            expression = sp.factor(finite[direction][word].subs(reverse_sub))
            numerator = sp.factor(sp.together(expression).as_numer_denom()[0])
            if numerator != 0:
                reverse_equations.append(numerator)
    reverse_variables = (
        C_symbols[0],
        C_symbols[3],
        D_symbols[0],
        D_symbols[1],
        D_symbols[2],
        D_symbols[3],
        h_symbols[1],
        h_symbols[2],
    )
    domain = sp.QQ.frac_field(p, r)
    reverse_basis = sp.groebner(
        reverse_equations, *reverse_variables, order="grevlex", domain=domain
    )
    expected_reverse = (
        C_symbols[0] + epsilon * p * (r + 2 * epsilon) / r,
        C_symbols[3],
        D_symbols[0] - 2 * epsilon * p * (r + epsilon) / r**2,
        D_symbols[1],
        D_symbols[2],
        D_symbols[3] + (r + 2 * epsilon) / r,
        h_symbols[1],
        h_symbols[2],
    )
    expected_basis = sp.groebner(
        expected_reverse, *reverse_variables, order="grevlex", domain=domain
    )
    assert all(reverse_basis.reduce(poly)[1] == 0 for poly in expected_reverse)
    assert all(
        expected_basis.reduce(poly.as_expr())[1] == 0 for poly in reverse_basis.polys
    )
    reverse_solution = {
        C_symbols[0]: -epsilon * p * (r + 2 * epsilon) / r,
        C_symbols[3]: 0,
        D_symbols[0]: 2 * epsilon * p * (r + epsilon) / r**2,
        D_symbols[1]: 0,
        D_symbols[2]: 0,
        D_symbols[3]: -(r + 2 * epsilon) / r,
        h_symbols[1]: 0,
        h_symbols[2]: 0,
    }
    reverse_all = reverse_sub | reverse_solution
    assert sp.factor(finite["01"][(1, 1, 1, 1)].subs(reverse_all)) == 0

    # Direct infinity contradictions for both binary orientations.
    infinity = {
        direction: contracted_tensor(
            endpoint_planes,
            direction,
            weight,
            h_symbols,
            C_symbols,
            D_symbols,
            True,
        )
        for direction in ("01", "23")
    }
    K = C_symbols[1] - epsilon * C_symbols[2]
    S = C_symbols[1] + C_symbols[2]
    assert_equal(infinity["01"][(0, 0, 0, 0)], 2 * p * K)
    assert_equal(infinity["23"][(0, 0, 0, 0)], -2 * r * S)
    assert_equal(
        infinity["01"][(1, 0, 0, 0)],
        2 * p * (h_symbols[0] * K + C_symbols[2]),
    )
    if epsilon == 1:
        endpoint_reverse_infinity = {
            C_symbols[2]: -C_symbols[1],
            h_symbols[0]: sp.Rational(1, 2),
            h_symbols[3]: r / p,
        }
        residual = sp.factor(
            infinity["01"][(1, 0, 0, 1)].subs(endpoint_reverse_infinity)
        )
        assert_equal(residual, -2 * C_symbols[1] * (r + 2))

    endpoint_results[str(epsilon)] = {
        "D23_binary_kernel_rank": 5,
        "D23_binary_kernel_minor": str(kernel_minor),
        "genuine_locus": "F*G*H!=0",
        "fixed_D23_mode3_minor": str(marked_minor),
        "reverse_finite_branch": "complete but B01=0",
        "infinity": "empty in both orientations",
    }

component_text = COMPONENT.read_text(encoding="utf-8")
assert "T_0111=4p" in component_text
assert "T_1111=4(q-phi)" in component_text

payload = {
    "status": "pass",
    "role": "proof_b",
    "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "git_commit": git_commit(),
    "claim_label": "DERIVED",
    "scope": "component-19 zero-base normal directions and exact linear DVR arcs",
    "inputs": {
        COMPONENT.name: sha256(COMPONENT),
        **{path.name: sha256(path) for path in DEPENDENCIES},
    },
    "method": (
        "exact normal expansion, pair-minor reconstruction, verified open-"
        "stratum routing, and fresh phi=+/-1 finite/infinity endpoint algebra"
    ),
    "command": f"uv run --with sympy python {SCRIPT.name}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "normal_tensor": "4*(a*e_0111+b*e_1111)",
    "punctured_all_pair_open_directions": "all [a:b] in P1",
    "frozen_base_pair_boundary": "edge 03 drops below rank three at phi^2=1",
    "exact_linear_weighted_H22": "empty for every [a:b] and phi!=0",
    "phi_endpoint_replay": endpoint_results,
    "new_zero_base_construction_artifacts_read_or_imported": False,
    "higher_order_boundary": (
        "leading tensor and punctured pair openness extend to minimal-order "
        "formal arcs; weighted H22 does not follow from P1 alone and arbitrary "
        "higher-order or valuative arcs remain UNKNOWN"
    ),
    "limitations": (
        "exact linear arcs in the displayed component chart; no arbitrary "
        "higher-order, ramified, multi-parameter, non-diagonal-source, ambient-"
        "component, or global claim"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
