#!/usr/bin/env python3
"""Audit of a marked chart in a withdrawn mixed-triangle theorem."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import itertools
import json

import sympy as sp


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def multiplication_matrix(linear: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(linear, sp.eye(4).col(column)) for column in range(4))
    )


def main() -> None:
    # Crossed partition {0,2}|{1,3}.
    a = sp.Matrix((1, 0, 1, 0))
    a_bar = sp.Matrix((1, 0, -1, 0))
    b = sp.Matrix((0, 1, 0, 1))
    b_bar = sp.Matrix((0, 1, 0, -1))
    alpha_2, beta_2, alpha_3, beta_3 = sp.symbols(
        "alpha_2 beta_2 alpha_3 beta_3"
    )
    y2, x2 = a + beta_2 * b_bar, b + alpha_2 * a_bar
    y3, x3 = a + beta_3 * b_bar, b + alpha_3 * a_bar

    assert product(a, x2) == product(b, y2)
    assert product(a, x3) == product(b, y3)

    # Full-support leaf kernels have no linear annihilator.
    full_matrix = multiplication_matrix(y2)
    full_minor = sp.factor(full_matrix.extract((0, 1, 3, 5), range(4)).det())
    assert full_minor != 0
    assert full_minor.subs(beta_2, 0) == 0

    # At beta_2=0 the annihilator is exactly the crossed a_bar.
    two_support_matrix = full_matrix.subs(beta_2, 0)
    assert two_support_matrix.rank() == 3
    two_support_kernel = two_support_matrix.nullspace()
    assert len(two_support_kernel) == 1
    assert sp.Matrix.hstack(two_support_kernel[0], a_bar).rank() == 1

    # The other partner plane cannot contain that annihilator line.
    partner_matrix = sp.Matrix.hstack(y3, x3, a_bar)
    assert partner_matrix.rank() == 3
    all_containment_minors = [
        sp.factor(partner_matrix.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    ]
    assert any(not minor.free_symbols and minor != 0 for minor in all_containment_minors)

    result = {
        "crossed_partition": "{0,2}|{1,3}",
        "full_support_annihilator_minor": str(full_minor),
        "two_support_annihilator": [int(value) for value in a_bar],
        "partner_containment_constant_minor": True,
        "conclusion": "mixed (2,2,1) triangle impossible",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
