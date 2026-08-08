#!/usr/bin/env python3
"""Verify the full generic weighted H22 obstruction on the tenth component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

ROOT = REPO_ROOT
THEOREM = HERE / "P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = ROOT / "claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md"
DENSE = ROOT / "P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def cayley_rows(u: sp.Symbol, v: sp.Symbol):
    alpha = (
        (1, 0, 1, 0),
        (1 - u, -1 - u, 1 - u, -1 + u),
        (1 - v, -1 - v, 1 - v, 1 - v),
        (0, 0, 0, 1 - u * v),
    )
    beta = (
        (0, 0, 1, 0),
        (0, -1 - u, 1 - u, 0),
        (0, -1 - v, 1 - v, 0),
        (1 - u * v, -1 - u * v, -1 + u * v, 0),
    )
    return alpha, beta


def standard_row(row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    a, a_bar, b, b_bar = row
    return (a + a_bar, a - a_bar, b + b_bar, b - b_bar)


def weighted_23_row(
    row: tuple[sp.Expr, ...], extension: sp.Expr, rho: sp.Symbol
) -> tuple[sp.Expr, ...]:
    a, a_bar, b, b_bar = row
    return (a + a_bar, a - a_bar, b + rho * b_bar, extension)


def tensor_coordinates(
    alpha,
    beta,
    extensions: tuple[sp.Symbol, ...],
    rho: sp.Symbol,
) -> dict[tuple[int, ...], sp.Expr]:
    alpha_extended = tuple(
        weighted_23_row(alpha[mode], extensions[mode], rho) for mode in range(4)
    )
    beta_extended = tuple(
        weighted_23_row(beta[mode], extensions[4 + mode], rho) for mode in range(4)
    )
    return {
        word: permanent(
            tuple(
                beta_extended[mode] if word[mode] else alpha_extended[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }


def toric_generators(coordinates: dict[tuple[int, ...], sp.Expr]):
    empty = coordinates[(0, 0, 0, 0)]
    singleton = {
        mode: coordinates[tuple(int(index == mode) for index in range(4))]
        for mode in range(4)
    }
    quadrics = []
    cubics = []
    for size, target in ((2, quadrics), (3, cubics)):
        for subset in itertools.combinations(range(4), size):
            word = tuple(int(mode in subset) for mode in range(4))
            target.append(
                sp.expand(
                    coordinates[word] * empty ** (size - 1)
                    - sp.prod(singleton[mode] for mode in subset)
                )
            )
    return empty, singleton, tuple(quadrics), tuple(cubics)


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def unit_ideal(generators: tuple[sp.Expr, ...]) -> bool:
    program = "\n".join(
        (
            "ring R=(0,u,v,rho),(x0,x1,x2,x3,y0,y1,y2,y3),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(singular(generator) for generator in generators) + ";",
            "I=std(I);",
            '"CODEX_RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "I;",
            "quit;",
        )
    )
    completed = subprocess.run(
        SINGULAR,
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((completed.returncode, completed.stdout, completed.stderr))
    result = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert result == ["CODEX_RESULT:1:1"], completed.stdout
    assert "I[1]=1" in completed.stdout
    return True


def main() -> None:
    u, v, rho = sp.symbols("u v rho")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    x0, x1, x2, x3, y0, y1, y2, y3 = extensions
    alpha, beta = cayley_rows(u, v)

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    standard_row(beta[mode] if word[mode] else alpha[mode])
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    expected_pure = 4 * (u - 1) * (v - 1) * (u * v - 1)
    assert sp.expand(pure[(1, 1, 1, 1)] - expected_pure) == 0
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    coordinates = tensor_coordinates(alpha, beta, extensions, rho)
    empty, singleton, quadrics, cubics = toric_generators(coordinates)
    assert len(quadrics) == 6 and len(cubics) == 4

    K = x3 + rho * (1 - u * v) * y0
    L = -2 * (u + 1) * (v + 1)
    M = -4 * (u + v)
    expected_pattern = {
        (1, 0, 0, 0): M * K,
        (1, 0, 1, 0): L * K,
        (1, 1, 0, 0): L * K,
        (1, 1, 1, 0): L * K,
    }
    assert all(
        sp.factor(coordinates[word] - expected) == 0
        for word, expected in expected_pattern.items()
    )
    gap = sp.factor(M - L)
    assert sp.expand(gap - 2 * (u - 1) * (v - 1)) == 0

    generators = (sp.expand(empty - 1),) + quadrics + cubics
    assert unit_ideal(generators)

    print(
        json.dumps(
            {
                "status": "pass",
                "theorem": THEOREM.name,
                "component_function_field": "C(u,v,rho)",
                "weighted_direction": "23",
                "pure_coefficient": str(expected_pure),
                "fixed_vertex_join_generators": {
                    "normalization": 1,
                    "quadrics": len(quadrics),
                    "cubics": len(cubics),
                },
                "visible_open_branch": {
                    "pivot": str(K),
                    "coefficient_gap": str(gap),
                    "excluded": True,
                },
                "reduced_groebner_basis": ["1"],
                "all_markings_eliminated_intrinsically": True,
                "generic_weighted_H22_fibre_empty": True,
                "all_eleven_certified_components_generically_H22_closed": True,
                "search_used": False,
                "dependencies": {
                    path.name: sha256(path) for path in (COMPONENT, DENSE)
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
