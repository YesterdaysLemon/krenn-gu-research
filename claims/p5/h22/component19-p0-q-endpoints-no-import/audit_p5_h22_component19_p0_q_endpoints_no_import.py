#!/usr/bin/env python3
"""No-import verifier for component 19 at p=0 and q=+/-1."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_P0_Q_ENDPOINTS_NO_IMPORT_VERIFICATION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


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


def regular_planes(epsilon):
    return (
        (Abar, add(Bbar, scale(epsilon, B))),
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


def contracted_planes(planes, direction, infinity=False):
    result = []
    for mode, (alpha, beta) in enumerate(planes):
        marked_beta = add(beta, scale(h[mode], alpha))
        result.append(
            (
                contract(alpha, C[mode], direction, infinity),
                contract(marked_beta, D[mode], direction, infinity),
            )
        )
    return tuple(result)


def tensor(planes, direction, infinity=False):
    direction_planes = contracted_planes(planes, direction, infinity)
    return {
        word: permanent(tuple(direction_planes[i][word[i]] for i in range(4)))
        for word in WORDS4
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


def restrict_full(row, direction):
    if direction == "01":
        return (sp.expand(row[0] + row[1]), row[2], row[3], row[4])
    if direction == "23":
        return (row[0], row[1], sp.expand(row[2] + row[3]), row[4])
    raise ValueError(direction)


def full_one_marked_map(full_planes, direction, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    basis = tuple(
        tuple(sp.Integer(index == coordinate) for index in range(5))
        for coordinate in range(5)
    )
    rows = []
    for word in WORDS3:
        fixed = tuple(
            restrict_full(full_planes[mode][bit], direction)
            for mode, bit in zip(other_modes, word, strict=True)
        )
        rows.append(
            [
                permanent((*fixed, restrict_full(basis_row, direction)))
                for basis_row in basis
            ]
        )
    return sp.Matrix(rows)


def four_minors(matrix):
    return {
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(8), 4)
        for columns in itertools.combinations(range(5), 4)
    }


phi, lam = sp.symbols("phi lambda", nonzero=True)
h0, h1, h2, h3, t = sp.symbols("h0 h1 h2 h3 t")
C0, C1, C2, C3 = sp.symbols("C0 C1 C2 C3")
D0, D1, D2, D3 = sp.symbols("D0 D1 D2 D3")
X, Y, Z = sp.symbols("X Y Z")
h = (h0, h1, h2, h3)
C = (C0, C1, C2, C3)
D = (D0, D1, D2, D3)
extension_variables = C + D
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)

endpoint_results = {}
for epsilon in (1, -1):
    planes = regular_planes(epsilon)

    raw_tensor = {
        word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS4
    }
    raw_support = {word: value for word, value in raw_tensor.items() if value != 0}
    assert raw_support.keys() == {(1, 1, 1, 1)}
    assert_equal(raw_support[(1, 1, 1, 1)], 4 * (epsilon - phi))

    finite = {direction: tensor(planes, direction) for direction in ("01", "23")}
    infinite = {
        direction: tensor(planes, direction, True) for direction in ("01", "23")
    }
    finite_l = C1 * (lam - 1) + C2 * (lam + 1)

    # Direct orientation equations.  The determinant epsilon*phi-1 is a unit
    # under phi*(phi^2-1) != 0, so finite lambda=1 is forced and infinity dies.
    assert_equal(finite["23"][(0, 0, 0, 0)], -2 * finite_l)
    assert_equal(finite["23"][(0, 0, 0, 1)], -2 * h3 * finite_l)
    assert_equal(finite["23"][(1, 0, 0, 0)], -2 * h0 * finite_l)
    assert_equal(
        finite["01"][(0, 0, 0, 1)],
        -2 * (lam - 1) * (phi * C1 - C2),
    )
    assert_equal(
        finite["01"][(1, 0, 0, 0)],
        2 * (lam - 1) * (-C1 + epsilon * C2),
    )
    assert_equal(
        sp.Matrix(((phi, -1), (-1, epsilon))).det(), epsilon * phi - 1
    )
    infinity_l = C1 + C2
    assert_equal(infinite["23"][(0, 0, 0, 0)], -2 * infinity_l)
    assert_equal(infinite["01"][(0, 0, 0, 1)], -2 * (phi * C1 - C2))
    assert_equal(
        infinite["01"][(1, 0, 0, 0)], 2 * (-C1 + epsilon * C2)
    )

    # Complete finite shared branch.
    branch = {lam: 1, h0: 0, h1: 0, h2: t, h3: 0}
    forward_matrix = sp.Matrix(
        [
            coefficient_vector(finite["01"][word])
            for word in WORDS4
            if word != (1, 1, 1, 1)
        ]
        + [
            coefficient_vector(finite["23"][word])
            for word in WORDS4
            if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
        ]
    ).subs(branch)
    r = epsilon - phi
    v_x = sp.Matrix((0, -1 / r, phi / r, 0, 1, 0, 0, 0))
    v_y = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    v_z = sp.Matrix((0, -epsilon / r, 1 / r, 0, 0, 0, 0, 1))
    for vector in (v_x, v_y, v_z):
        assert all(sp.factor(value) == 0 for value in forward_matrix * vector)
    kernel_minor = sp.factor(
        forward_matrix.extract((3, 10, 11, 13, 16), (0, 1, 2, 3, 6)).det()
    )
    assert_equal(kernel_minor, -1024 * epsilon * r**2)

    extension = X * v_x + Y * v_y + Z * v_z
    extension_sub = dict(zip(extension_variables, extension, strict=True))
    F = phi * X + Z
    G = r * Y - t * F
    H = X + epsilon * Z
    assert_equal(
        finite["01"][(1, 1, 1, 1)].subs(branch).subs(extension_sub), 4 * G
    )
    assert_equal(
        finite["23"][(0, 0, 0, 0)].subs(branch).subs(extension_sub), -4 * F / r
    )
    assert_equal(
        finite["23"][(1, 1, 1, 1)].subs(branch).subs(extension_sub), 4 * H
    )

    full_planes = []
    for mode, (alpha, beta) in enumerate(planes):
        alpha5 = tuple(map(sp.sympify, alpha)) + (extension[mode],)
        marked_beta = add(beta, scale(branch[h[mode]], alpha))
        beta5 = tuple(map(sp.sympify, marked_beta)) + (extension[4 + mode],)
        full_planes.append((alpha5, beta5))
    full_planes = tuple(full_planes)
    maps = {
        (direction, mode): full_one_marked_map(full_planes, direction, mode)
        for direction in ("01", "23")
        for mode in range(4)
    }

    # Complete individual-rank classification.
    L = 2 * phi * X + (epsilon * phi + 1) * Z
    generator_01 = sp.factor(64 * Z * (phi**2 - 1) * L * G / r**2)
    values_01 = four_minors(maps[("01", 0)])
    assert values_01 <= {sp.Integer(0), generator_01, -generator_01}
    assert generator_01 in values_01 or -generator_01 in values_01

    fixed_23 = sp.factor(
        maps[("23", 2)].extract((0, 2, 3, 7), (0, 1, 2, 4)).det()
    )
    assert_equal(fixed_23, 64 * Y**2 * H)
    values_23 = four_minors(maps[("23", 2)])
    assert all(sp.factor(value.subs(Y, 0)) == 0 for value in values_23)

    for key, matrix in maps.items():
        if key not in (("01", 0), ("23", 2)):
            assert four_minors(matrix) == {sp.Integer(0)}

    # The two complete individual-rank survivor families.
    family_a = {Y: 0, Z: 0}
    family_b = {Y: 0, X: -(epsilon * phi + 1) * Z / (2 * phi)}
    stack = maps[("01", 1)].col_join(maps[("23", 1)])
    stack_a = stack.subs(family_a)
    stack_b = stack.subs(family_b)
    witness_a = sp.factor(
        stack_a.extract((7, 8, 9, 15), (0, 1, 2, 3)).det()
    )
    witness_b = sp.factor(
        stack_b.extract((7, 8, 9, 15), (0, 1, 2, 3)).det()
    )
    assert_equal(witness_a, -64 * X**4 * phi**3 / (phi - epsilon) ** 2)
    assert_equal(witness_b, 4 * Z**4 * (phi - epsilon) ** 2 / phi)
    assert stack_a.rank() == 4
    assert stack_b.rank() == 4

    # Recheck that all individual four-minors vanish on each survivor.
    for matrix in maps.values():
        assert all(
            sp.factor(value.subs(family_a)) == 0 for value in four_minors(matrix)
        )
        assert all(
            sp.factor(value.subs(family_b)) == 0 for value in four_minors(matrix)
        )

    endpoint_results[str(epsilon)] = {
        "ordinary_tensor": str(raw_support[(1, 1, 1, 1)]),
        "orientation": "finite lambda=1 only; infinity empty",
        "kernel_rank": 5,
        "kernel_minor": str(kernel_minor),
        "kernel": [
            "C=(0,-H/(e-phi),F/(e-phi),0)",
            "D=(X,Y,0,Z)",
            "h=(0,0,t,0)",
        ],
        "genuine_locus": "F*G*H!=0",
        "individual_rank_safe_locus": "Y=0 and Z*L=0",
        "survivor_A": "Y=Z=0, X*t!=0",
        "survivor_B": "Y=0, X=-(e*phi+1)*Z/(2*phi), Z*t!=0",
        "stacked_mode1_minor_A": str(witness_a),
        "stacked_mode1_minor_B": str(witness_b),
    }

component_text = COMPONENT.read_text(encoding="utf-8")
assert "T_1111=4(q-phi)" in component_text
assert "phi!=0" in component_text

payload = {
    "status": "pass",
    "role": "verifier",
    "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "git_commit": git_commit(),
    "claim_label": "VERIFIED",
    "scope": "component 19 ordinary p=0,q=+/-1 over Q(phi), phi*(phi^2-1)!=0",
    "inputs": {COMPONENT.name: sha256(COMPONENT)},
    "method": (
        "fresh regular-basis permanents, direct finite/infinity compatibility, "
        "complete shared kernel, exhaustive individual four-minors, and fixed "
        "full-target stacked minors"
    ),
    "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "candidate_verdict": "VERIFIED",
    "candidate_claim": (
        "exactly two individual-rank survivor families remain for each sign, "
        "and both have fixed nonzero mode-one stacked minors"
    ),
    "endpoints": endpoint_results,
    "forbidden_exploration_script_read_or_imported": False,
    "forbidden_candidate_report_read_or_imported": False,
    "limitations": (
        "ordinary q endpoints only; no phi=0,+/-1, projectivized, valuative, "
        "closure, arbitrary-order, or global claim"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
