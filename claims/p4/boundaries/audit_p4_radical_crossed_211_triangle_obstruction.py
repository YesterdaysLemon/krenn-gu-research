#!/usr/bin/env python3
"""Independent exact audit of the radical-crossed triangle obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
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
THEOREM = HERE / "P4_RADICAL_CROSSED_211_TRIANGLE_OBSTRUCTION.md"
PRIMARY = HERE / "verify_p4_radical_crossed_211_triangle_obstruction.py"
SUPPORT_ONE = REPO_ROOT / "claims/p4/classifications/P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def product(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def sync_matrix(a: tuple[int, ...], b: tuple[int, ...]) -> sp.Matrix:
    x = sp.symbols("r0:4")
    z = sp.symbols("s0:4")
    equations = product(a, z) - product(x, b)
    return equations.jacobian((*x, *z))


def audit_distinct(
    name: str,
    a: tuple[int, ...],
    a_bar: tuple[int, ...],
    b: tuple[int, ...],
    b_bar: tuple[int, ...],
) -> dict[str, object]:
    matrix = sync_matrix(a, b)
    expected = sp.Matrix.hstack(
        sp.Matrix((*a, *b)),
        sp.Matrix((*b_bar, 0, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 0, *a_bar)),
    )
    assert matrix.rank() == 5
    assert expected.rank() == 3
    assert matrix * expected == sp.zeros(6, 3)
    assert len(matrix.nullspace()) == 3

    lam, mu, nu = sp.symbols("l m n")
    x1 = tuple(lam * a[i] + mu * b_bar[i] for i in range(4))
    x2 = tuple(lam * b[i] + nu * a_bar[i] for i in range(4))
    columns = sp.Matrix.hstack(
        product(a, b), product(a, x2), product(x1, b), product(x1, x2)
    )
    assert all(
        sp.factor(columns.extract(rows, columns3).det()) == 0
        for rows in itertools.combinations(range(6), 3)
        for columns3 in itertools.combinations(range(4), 3)
    )
    return {"orbit": name, "kernel_dimension": 3, "pair_rank_upper_bound": 2}


def main() -> None:
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    results = [
        audit_distinct(
            "adjacent",
            a,
            a_bar,
            (1, 0, 1, 0),
            (1, 0, -1, 0),
        ),
        audit_distinct(
            "disjoint",
            a,
            a_bar,
            (0, 0, 1, 1),
            (0, 0, 1, -1),
        ),
    ]

    # Equal support: coefficient pairs kill the complementary entries.
    g = sp.symbols("g", nonzero=True)
    matrix = sync_matrix(a, (1, g, 0, 0))
    x = sp.symbols("r0:4")
    z = sp.symbols("s0:4")
    equations = matrix * sp.Matrix((*x, *z))
    assert sp.factor(equations[1]) == -x[2] + z[2]
    assert sp.factor(equations[3]) == -g * x[2] + z[2]
    assert sp.factor(equations[2]) == -x[3] + z[3]
    assert sp.factor(equations[4]) == -g * x[3] + z[3]

    theorem = THEOREM.read_text(encoding="utf-8")
    support_one = SUPPORT_ONE.read_text(encoding="utf-8")
    for marker in (
        "complete solution",
        "dim(U_1U_2)<=2",
        "previously unnamed sixth Borel-flag orbit",
        "global conjecture remains **UNRESOLVED**",
    ):
        assert marker in theorem
    assert "entire support-one boundary" in support_one

    print(
        json.dumps(
            {
                "status": "verified",
                "role": "independent no-import audit",
                "claim_label": "VERIFIED",
                "scope": "AB radical-crossed triangle-(2,1,1) obstruction",
                "distinct_support_replays": results,
                "equal_support_equations_checked": True,
                "primary_imported": False,
                "inputs": {
                    path.name: sha256(path) for path in (THEOREM, PRIMARY, SUPPORT_ONE)
                },
                "finite_field_inference_used": False,
                "broad_search_used": False,
                "triangle_211_cell_exhausted": False,
                "global_Krenn_Gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
