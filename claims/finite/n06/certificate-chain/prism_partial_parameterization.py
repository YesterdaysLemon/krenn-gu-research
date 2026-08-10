"""Hybrid torus parameterization for deficient prism core orbits."""

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

from collections import Counter

from krenn_gu.prism_orbit_screen import Polynomial, clean_polynomial


def partial_parameter_names(rank_one_blocks: set[int]) -> list[str]:
    names: list[str] = []
    for block in range(6):
        if block in rank_one_blocks:
            names.extend(f"u{3 * block + row}" for row in range(3))
            names.extend(f"v{3 * block + column}" for column in range(3))
        else:
            names.extend(f"x{9 * block + entry}" for entry in range(9))
    return names


def partially_parameterize_polynomial(
    polynomial: Polynomial, rank_one_blocks: set[int]
) -> Polynomial:
    result: Polynomial = Counter()
    for monomial, coefficient in polynomial.items():
        factors: list[str] = []
        for variable in monomial:
            entry_index = int(variable[1:])
            block = entry_index // 9
            within_block = entry_index % 9
            if block not in rank_one_blocks:
                factors.append(variable)
                continue
            row = within_block // 3
            column = within_block % 3
            factors.extend((f"u{3 * block + row}", f"v{3 * block + column}"))
        result[tuple(sorted(factors))] += coefficient
    return clean_polynomial(result)
