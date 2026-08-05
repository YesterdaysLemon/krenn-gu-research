#!/usr/bin/env python3
"""Independent original-coordinate audit of the tenth component H22 theorem."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
SINGULAR = ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def subset_permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    table: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        nxt: dict[int, sp.Expr] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = sp.expand(nxt.get(target, 0) + coefficient * entry)
        table = nxt
    return sp.expand(table[15])


def original_rows(s: int, t: int):
    alpha = (
        (1, 1, 1, 1),
        (1 - s, 1 + s, 0, 2),
        (1 - t, 1 + t, 2, 0),
        (0, 0, 1, -1),
    )
    beta = (
        (0, 0, 1, 1),
        (-s, s, 1, 1),
        (-t, t, 1, 1),
        (s + t - 1 - s * t, s + t + 1 + s * t, -s - t, -s - t),
    )
    return alpha, beta


def weighted_row(row, extension: sp.Expr, rho: sp.Symbol):
    return (row[0], row[1], rho * row[2] + row[3], extension)


def coordinates_at_point(
    s: int,
    t: int,
    rho: sp.Symbol,
    extensions: tuple[sp.Symbol, ...],
):
    alpha, beta = original_rows(s, t)
    alpha_extended = tuple(
        weighted_row(alpha[mode], extensions[mode], rho) for mode in range(4)
    )
    beta_extended = tuple(
        weighted_row(beta[mode], extensions[4 + mode], rho) for mode in range(4)
    )
    return {
        word: subset_permanent(
            tuple(
                beta_extended[mode] if word[mode] else alpha_extended[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }


def toric_generators(coordinates):
    empty = coordinates[(0, 0, 0, 0)]
    singleton = {
        mode: coordinates[tuple(int(index == mode) for index in range(4))]
        for mode in range(4)
    }
    generators = [sp.expand(empty - 1)]
    for size in (2, 3):
        for subset in itertools.combinations(range(4), size):
            word = tuple(int(mode in subset) for mode in range(4))
            generators.append(
                sp.expand(
                    coordinates[word] * empty ** (size - 1)
                    - sp.prod(singleton[mode] for mode in subset)
                )
            )
    return tuple(generators)


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def check_point(point: tuple[int, int]) -> dict[str, object]:
    rho = sp.Symbol("rho")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    coordinates = coordinates_at_point(*point, rho, extensions)
    generators = toric_generators(coordinates)
    program = "\n".join(
        (
            "ring R=(0,rho),(x0,x1,x2,x3,y0,y1,y2,y3),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(singular(generator) for generator in generators) + ";",
            "I=std(I);",
            '"AUDIT:"+string(reduce(1,I)==0)+":"+string(size(I));',
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
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    result = [line.strip() for line in completed.stdout.splitlines() if line.startswith("AUDIT:")]
    assert result == ["AUDIT:1:1"], completed.stdout
    return {
        "component_point": list(point),
        "coefficient_field": "C(rho)",
        "normalization_plus_toric_generators": len(generators),
        "reduced_basis": ["1"],
    }


def main() -> None:
    points = ((2, 3), (3, 5))
    results = [check_point(point) for point in points]
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent original-(s,t) rows and subset-DP permanents",
                "weighted_direction": "23",
                "points": results,
                "all_markings_encoded_by_fixed_vertex_join": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
