#!/usr/bin/env python3
"""Replay the full target-local obstruction on the two q*phi=-1 axes."""

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
REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHIM1_AXIS_TARGET_LOCAL_PROOF_B.md"
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


def restrict(row, direction):
    if direction == "01":
        return (sp.expand(row[0] + row[1]), row[2], row[3], row[4])
    if direction == "23":
        return (row[0], row[1], sp.expand(row[2] + row[3]), row[4])
    raise ValueError(direction)


def restricted_tensor(full_planes, direction):
    return {
        word: permanent(tuple(restrict(full_planes[i][word[i]], direction) for i in range(4)))
        for word in WORDS4
    }


def full_one_marked_map(full_planes, direction, marked_mode):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    basis = tuple(
        tuple(sp.Integer(index == coordinate) for index in range(5))
        for coordinate in range(5)
    )
    rows = []
    for word in WORDS3:
        fixed = tuple(
            restrict(full_planes[mode][bit], direction)
            for mode, bit in zip(other_modes, word, strict=True)
        )
        rows.append(
            [permanent((*fixed, restrict(basis_row, direction))) for basis_row in basis]
        )
    return sp.Matrix(rows)


phi, t, X, Z = sp.symbols("phi t X Z", nonzero=True)
s = phi**2 + 1
A = (1, 1, 0, 0)
Abar = (1, -1, 0, 0)
B = (0, 0, 1, 1)
Bbar = (0, 0, 1, -1)

# Fresh regular p=0 basis after q=-1/phi.
planes = (
    (Abar, add(Bbar, scale(-1 / phi, B))),
    (B, A),
    (Bbar, A),
    (Abar, add(B, scale(phi, Bbar))),
)

raw_tensor = {
    word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
    for word in WORDS4
}
raw_support = {word: value for word, value in raw_tensor.items() if value != 0}
assert raw_support.keys() == {(1, 1, 1, 1)}
assert_equal(raw_support[(1, 1, 1, 1)], -4 * s / phi)


def extended_planes(C, D):
    h = (0, 0, t, 0)
    result = []
    for mode, (alpha, beta) in enumerate(planes):
        alpha5 = tuple(map(sp.sympify, alpha)) + (C[mode],)
        marked_beta = add(beta, scale(h[mode], alpha))
        beta5 = tuple(map(sp.sympify, marked_beta)) + (D[mode],)
        result.append((alpha5, beta5))
    return tuple(result)


axes = {
    "Z": {
        "coordinate": Z,
        "C": (0, -Z / s, -phi * Z / s, 0),
        "D": (0, 0, 0, Z),
        "diagonals": (-4 * t * Z, 4 * phi * Z / s, -4 * Z / phi),
        "stack_minor": 64 * Z**4 * phi / s**2,
        "stack_ranks": (5, 4, 4, 4),
    },
    "X": {
        "coordinate": X,
        "C": (0, phi * X / s, -phi**2 * X / s, 0),
        "D": (X, 0, 0, 0),
        "diagonals": (-4 * phi * t * X, 4 * phi**2 * X / s, 4 * X),
        "stack_minor": -64 * X**4 * phi**5 / s**2,
        "stack_ranks": (4, 4, 4, 5),
    },
}

axis_results = {}
for axis, data in axes.items():
    full_planes = extended_planes(data["C"], data["D"])
    tensors = {
        direction: restricted_tensor(full_planes, direction)
        for direction in ("01", "23")
    }

    # The shared extension is exactly binary/pure on both slices.
    for word in WORDS4:
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1)):
            assert sp.factor(tensors["01"][word]) == 0
            assert sp.factor(tensors["23"][word]) == 0
    assert tensors["01"][(0, 0, 0, 0)] == 0
    assert_equal(tensors["01"][(1, 1, 1, 1)], data["diagonals"][0])
    assert_equal(tensors["23"][(0, 0, 0, 0)], data["diagonals"][1])
    assert_equal(tensors["23"][(1, 1, 1, 1)], data["diagonals"][2])

    maps = {
        (direction, mode): full_one_marked_map(full_planes, direction, mode)
        for direction in ("01", "23")
        for mode in range(4)
    }

    # Every separate one-marked rank test is safe: all four-minors vanish.
    for matrix in maps.values():
        for row_indices in itertools.combinations(range(8), 4):
            for column_indices in itertools.combinations(range(5), 4):
                determinant = matrix.extract(row_indices, column_indices).det()
                assert sp.factor(determinant) == 0

    direction_ranks = {
        direction: tuple(maps[(direction, mode)].rank() for mode in range(4))
        for direction in ("01", "23")
    }
    assert direction_ranks == {"01": (3, 1, 1, 3), "23": (3, 3, 3, 3)}

    stacks = {
        mode: maps[("01", mode)].col_join(maps[("23", mode)])
        for mode in range(4)
    }
    stack_ranks = tuple(stacks[mode].rank() for mode in range(4))
    assert stack_ranks == data["stack_ranks"]
    witness = sp.factor(stacks[1].extract((7, 8, 9, 15), (0, 1, 2, 3)).det())
    assert_equal(witness, data["stack_minor"])

    axis_results[axis] = {
        "individual_ranks": direction_ranks,
        "stack_ranks_over_function_field": stack_ranks,
        "uniform_mode1_minor_rows_7_8_9_15_cols_0_1_2_3": str(witness),
        "diagonals_B01_A23_B23": [str(value) for value in data["diagonals"]],
    }

component_text = COMPONENT.read_text(encoding="utf-8")
assert "T_1111=4(q-phi)" in component_text
assert "phi!=0" in component_text

payload = {
    "status": "pass",
    "role": "proof_b",
    "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "git_commit": git_commit(),
    "claim_label": "DERIVED",
    "scope": (
        "ordinary p=0,q*phi=-1 axes X=Y=0,Z*t!=0 and "
        "Z=Y=0,X*t!=0"
    ),
    "inputs": {COMPONENT.name: sha256(COMPONENT)},
    "method": (
        "fresh regular p0 reconstruction, exact shared binary contractions, "
        "full-target one-marked maps, complete individual four-minor checks, "
        "and fixed stacked four-minors"
    ),
    "command": f"uv run --with sympy python {SCRIPT.name}",
    "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
    "ordinary_tensor": "T1111=-4*(phi^2+1)/phi",
    "ordinary_parameter_open": "phi*(phi^2+1)!=0",
    "target_local_condition": "rank(stack(N01_i,N23_i))<=3 for every mode i",
    "axes": axis_results,
    "claim": "both complete ordinary genuine axes have no shared ternary H22 lift",
    "construction_p0_artifacts_read": False,
    "unknown": [
        "phi^2=-1 zero-tensor fibre",
        "projectivized or transverse directions at the zero tensor",
        "valuative and closure fibres",
    ],
    "limitations": (
        "ordinary axes only; no zero-tensor, projectivized, valuative, closure, "
        "arbitrary-order, or global claim"
    ),
}
print(json.dumps(payload, indent=2, sort_keys=True))
