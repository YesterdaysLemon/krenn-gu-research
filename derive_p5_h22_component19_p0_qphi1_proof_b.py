#!/usr/bin/env python3
"""Exact proof-B replay for component 19 at p=0 and q*phi=1."""

from __future__ import annotations

import contextlib
import hashlib
import io
import itertools
import json
import runpy
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHI1_PROOF_B.md"
COMPONENT = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
BASE = ROOT / "derive_p5_h22_component19_p0_ordinary_open_proof_b.py"


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


# Reuse only the independently derived regular-chart algebra.  Its stdout is
# suppressed; no construction or compatibility-divisor artifact is imported.
with contextlib.redirect_stdout(io.StringIO()):
    base = runpy.run_path(str(BASE))

phi = base["phi"]
q = base["q"]
lam = base["lam"]
h0, h1, h2, h3 = base["h"]
C0, C1, C2, C3, D0, D1, D2, D3 = base["extension_variables"]
extension_variables = base["extension_variables"]
words = base["WORDS"]
planes = base["planes"]
finite = base["finite"]
infinite = base["infinite"]
product_matrix = base["product_matrix"]
contracted_planes = base["contracted_planes"]
one_marked_matrix = base["one_marked_matrix"]

c, u, v, t = sp.symbols("c u v t")
qphi1 = {q: 1 / phi}

# The ordinary tensor is nonzero away from the two zero endpoints.
raw_support = {
    word: sp.factor(value.subs(qphi1))
    for word, value in base["raw_tensor"].items()
    if sp.factor(value.subs(qphi1)) != 0
}
assert raw_support.keys() == {(1, 1, 1, 1)}
assert_equal(raw_support[(1, 1, 1, 1)], 4 * (1 / phi - phi))

# All six pair products have exact rank three on phi^2 != 1.
special_planes = tuple(
    tuple(
        tuple(sp.factor(sp.sympify(entry).subs(qphi1)) for entry in row)
        for row in plane
    )
    for plane in planes
)
pair_witnesses = {
    (0, 1): ((1, 2, 5), (0, 2, 3), 4 / phi),
    (0, 2): ((1, 2, 5), (0, 2, 3), 4 / phi),
    (0, 3): (
        (0, 1, 5),
        (0, 1, 3),
        4 * (phi - 1) * (phi + 1) ** 2 / phi,
    ),
    (1, 2): ((0, 1, 2), (1, 2, 3), -4),
    (1, 3): ((1, 2, 5), (0, 1, 3), 4 * phi),
    (2, 3): ((1, 2, 5), (0, 1, 3), 4 * phi),
}
for pair, (rows, columns, expected) in pair_witnesses.items():
    matrix = product_matrix(special_planes[pair[0]], special_planes[pair[1]])
    assert_equal(matrix.extract(rows, columns).det(), expected)
    for larger_rows in itertools.combinations(range(6), 4):
        assert sp.factor(matrix.extract(larger_rows, range(4)).det()) == 0


def mixed_matrix(data, substitutions) -> sp.Matrix:
    expressions = [
        data[direction][word].subs(substitutions)
        for direction in ("01", "23")
        for word in words
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    return sp.Matrix(
        [
            [sp.expand(expression).coeff(variable) for variable in extension_variables]
            for expression in expressions
        ]
    )


# D01 has zero all-alpha coefficient, so D23 must be binary.  Its all-alpha
# open forces h0=h3=0 at every finite or infinite shared orientation.
finite_l = C1 * (lam - 1) + C2 * (lam + 1)
assert_equal(finite["23"][(0, 0, 0, 0)].subs(qphi1), -2 * finite_l)
assert_equal(finite["23"][(0, 0, 0, 1)].subs(qphi1), -2 * h3 * finite_l)
assert_equal(finite["23"][(1, 0, 0, 0)].subs(qphi1), -2 * h0 * finite_l)
assert finite["01"][(0, 0, 0, 0)] == 0
assert infinite["01"][(0, 0, 0, 0)] == 0

# For lambda != 1, D01 forces C2=phi*C1.  Unless lambda=-1, the following
# opposite-sign equations contradict C1*(phi^2-1) != 0.
orientation_sub = {q: 1 / phi, h0: 0, h3: 0, C2: phi * C1}
assert_equal(
    finite["23"][(0, 0, 0, 0)].subs(orientation_sub),
    -2 * C1 * ((phi + 1) * lam + phi - 1),
)
assert_equal(
    finite["01"][(1, 0, 1, 1)].subs(orientation_sub),
    -2
    * (lam + 1)
    * (C1 * (phi**2 - 1) - phi * D0 - D3)
    / phi,
)
assert_equal(
    finite["01"][(1, 1, 0, 1)].subs(orientation_sub),
    -2 * (lam + 1) * (C1 * (phi**2 - 1) + phi * D0 + D3),
)

# The complete lambda=-1 mixed kernel is three dimensional but nongenuine.
minus_orientation = {q: 1 / phi, lam: -1, h0: 0, h1: 0, h2: 0, h3: 0}
minus_matrix = mixed_matrix(finite, minus_orientation)
minus_vectors = (
    sp.Matrix((0, 1, phi, 0, 0, 0, 0, 0)),
    sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0)),
    sp.Matrix((0, 0, 0, 0, 0, 0, 0, 1)),
)
for vector in minus_vectors:
    assert all(sp.factor(value) == 0 for value in minus_matrix * vector)
minus_minor = sp.factor(
    minus_matrix.extract((0, 2, 4, 20, 27), (0, 1, 3, 5, 6)).det()
)
assert_equal(minus_minor, -1024 * phi**3)
minus_extension = c * minus_vectors[0] + u * minus_vectors[1] + v * minus_vectors[2]
minus_sub = dict(zip(extension_variables, minus_extension, strict=True))
assert finite["01"][(1, 1, 1, 1)].subs(minus_orientation).subs(minus_sub) == 0

# The complete finite genuine candidate kernel at lambda=1.
plus_orientation = {q: 1 / phi, lam: 1, h0: 0, h1: 0, h2: t, h3: 0}
plus_matrix = mixed_matrix(finite, plus_orientation)
plus_vectors = (
    sp.Matrix((0, 1, -phi, 0, 0, 0, 0, phi**2 - 1)),
    sp.Matrix((0, 0, 0, 0, 1, 0, 0, -phi)),
    sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0)),
)
for vector in plus_vectors:
    assert all(sp.factor(value) == 0 for value in plus_matrix * vector)
plus_minor = sp.factor(
    plus_matrix.extract((2, 9, 10, 12, 15), (0, 1, 2, 3, 6)).det()
)
assert_equal(
    plus_minor,
    -1024 * (phi - 1) ** 2 * (phi + 1) ** 2 / phi**3,
)
plus_extension = c * plus_vectors[0] + u * plus_vectors[1] + v * plus_vectors[2]
plus_sub = dict(zip(extension_variables, plus_extension, strict=True))
genuine_factor = phi * c * t + v
assert_equal(
    finite["01"][(1, 1, 1, 1)].subs(plus_orientation).subs(plus_sub),
    -4 * (phi**2 - 1) * genuine_factor / phi,
)
assert_equal(
    finite["23"][(0, 0, 0, 0)].subs(plus_orientation).subs(plus_sub),
    4 * phi * c,
)
assert_equal(
    finite["23"][(1, 1, 1, 1)].subs(plus_orientation).subs(plus_sub),
    4 * c * (phi**2 - 1) / phi,
)

# Two fixed one-marked minors obstruct every genuine plus-branch extension.
plus_planes = tuple(
    tuple(
        tuple(
            sp.factor(sp.sympify(entry).subs(plus_orientation).subs(plus_sub))
            for entry in row
        )
        for row in plane
    )
    for plane in contracted_planes("01")
)
mode0 = one_marked_matrix(plus_planes, 0)
mode3 = one_marked_matrix(plus_planes, 3)
minor0 = sp.factor(mode0.extract((1, 3, 5, 7), range(4)).det())
minor3 = sp.factor(mode3.extract((4, 5, 6, 7), range(4)).det())
assert_equal(
    minor0,
    128
    * c
    * phi
    * (phi**2 - 1)
    * genuine_factor
    * (phi * u - c * (phi**2 - 1)),
)
assert_equal(
    minor3,
    -128 * c * u * (phi**2 - 1) * genuine_factor / phi**2,
)

# At infinity, C2=phi*C1 and the same equations have no lambda+1 escape.
infinity_sub = {q: 1 / phi, h0: 0, h3: 0, C2: phi * C1}
assert_equal(
    infinite["23"][(0, 0, 0, 0)].subs(infinity_sub),
    -2 * C1 * (phi + 1),
)
assert_equal(
    infinite["01"][(1, 0, 1, 1)].subs(infinity_sub),
    -2 * (C1 * (phi**2 - 1) - phi * D0 - D3) / phi,
)
assert_equal(
    infinite["01"][(1, 1, 0, 1)].subs(infinity_sub),
    -2 * (C1 * (phi**2 - 1) + phi * D0 + D3),
)

component_text = COMPONENT.read_text(encoding="utf-8")
assert "T_1111=4(q-phi)" in component_text

payload = {
    "status": "pass",
    "role": "proof_b",
    "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "git_commit": git_commit(),
    "claim_label": "VERIFIED",
    "discovery_claim_label": "DERIVED",
    "scope": "ordinary component-19 p=0 divisor q*phi=1, phi^2!=1",
    "inputs": {COMPONENT.name: sha256(COMPONENT), BASE.name: sha256(BASE)},
    "method": (
        "regular p0 basis, exact pair minors, direct finite/infinity weighted "
        "contractions, complete extension kernels, and fixed one-marked minors"
    ),
    "command": f"uv run --with sympy python {SCRIPT.name}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "ordinary_tensor": "T1111=4*(1/phi-phi)",
    "pair_profile": [3, 3, 3, 3, 3, 3],
    "finite_orientations": {
        "lambda=1": "complete genuine-candidate kernel; universally rank-obstructed",
        "lambda=-1": "complete three-dimensional kernel; B01=0, nongenuine",
        "other": "incompatible with phi^2!=1 on the A23-open",
    },
    "infinity_orientation": "empty on the A23-open",
    "plus_kernel": [
        "C=(0,c,-phi*c,0)",
        "D=(u,v,0,c*(phi^2-1)-phi*u)",
        "h=(0,0,t,0)",
    ],
    "genuine_locus": "c*(phi*c*t+v)!=0",
    "fixed_minors": {"mode0": str(minor0), "mode3": str(minor3)},
    "claim": "ordinary weighted H22 fibre is empty",
    "unknown": [
        "phi=+/-1 zero endpoints",
        "transverse or projectivized directions at the zero endpoints",
        "valuative and closure fibres",
    ],
    "construction_compatibility_artifacts_read": False,
    "limitations": (
        "ordinary divisor only; no endpoint, valuative, closure, arbitrary-order, "
        "or global claim"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
