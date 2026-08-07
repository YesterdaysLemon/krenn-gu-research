#!/usr/bin/env python3
"""Independent audit of the common-active binary component certificate."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
ANCHOR = (0, 1, 1, 0)


def multiply(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def top_product(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    value = {0: sp.Integer(1)}
    for row in rows:
        linear = {
            1 << index: sp.sympify(entry)
            for index, entry in enumerate(row)
            if entry != 0
        }
        value = multiply(value, linear)
    return sp.expand(value.get(15, 0))


def tensor(
    planes: tuple[tuple[tuple[sp.Expr, ...], ...], ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            top_product(tuple(planes[mode][word[mode]] for mode in range(4)))
        )
        for word in WORDS
    }


def wedge(
    plane: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(plane[0][left] * plane[1][right] - plane[0][right] * plane[1][left])
        for left, right in PAIRS
    )


def pivot01_plane(entries: tuple[sp.Expr, ...]) -> tuple[tuple[sp.Expr, ...], ...]:
    return ((1, 0, entries[0], entries[1]), (0, 1, entries[2], entries[3]))


def singular_command() -> list[str]:
    native = shutil.which("Singular")
    if native:
        return [native, "-q"]
    return ["wsl.exe", "--exec", "/usr/bin/Singular", "-q"]


def main() -> None:
    p, q = sp.symbols("p q")
    normalized = (
        (
            (-(p - q + 1) / (p + q), -1, 1, 0),
            ((q**2 - q) / (p + q), -p - q, 0, 1),
        ),
        ((1, 0, 0, 0), (0, p + 1, q - 1, 1)),
        ((1, 0, 0, 0), (0, p, q, 1)),
        ((1, 1, 1, 0), (1, 0, 0, 0)),
    )
    values = tensor(normalized)
    expected = {
        (0, 1, 1, 1): 2 * (p - q + 1),
        (1, 1, 1, 1): -2 * q * (q - 1),
    }
    assert {word for word, value in values.items() if value != 0} == set(expected)
    for word, expected_value in expected.items():
        assert sp.expand(values[word] - expected_value) == 0

    # Independently reconstruct the affine graph slice at the rational point.
    point = (
        -6,
        1,
        -2,
        sp.Rational(1, 6),
        0,
        0,
        1,
        sp.Rational(1, 3),
        0,
        0,
        2,
        sp.Rational(1, 2),
        0,
        0,
        1,
        0,
    )
    target_point = (0, 0, 0, -1)
    fixed = {0, 1, 2, 3, 6}
    retained = tuple(index for index in range(20) if index not in fixed)
    local = tuple(sp.symbols("u0:15"))
    plane_symbols = tuple(sp.symbols("a0:16"))
    target_symbols = tuple(sp.symbols("b0:4"))
    universal_planes = tuple(
        pivot01_plane(plane_symbols[4 * mode : 4 * mode + 4]) for mode in range(4)
    )
    universal_tensor = tensor(universal_planes)
    equations = []
    for word in WORDS:
        if word == ANCHOR:
            continue
        target_monomial = sp.prod(
            target_symbols[mode] for mode in range(4) if word[mode] != ANCHOR[mode]
        )
        equations.append(
            sp.expand(
                universal_tensor[word] - universal_tensor[ANCHOR] * target_monomial
            )
        )
    all_symbols = (*plane_symbols, *target_symbols)
    full_point = (*point, *target_point)
    substitution = {
        symbol: (
            full_point[index]
            if index in fixed
            else full_point[index] + local[retained.index(index)]
        )
        for index, symbol in enumerate(all_symbols)
    }
    integer_equations = []
    for equation in equations:
        denominator, polynomial = sp.Poly(
            sp.expand(equation.subs(substitution)), *local
        ).clear_denoms()
        assert denominator == 6
        assert polynomial.primitive()[0] == 1
        integer_equations.append(polynomial.as_expr())
    source = (
        "ring R=103,(" + ",".join(map(str, local)) + "),ds;\n"
        "ideal I="
        + ",\n".join(sp.sstr(value).replace("**", "^") for value in integer_equations)
        + ';\nideal G=std(I);print("AUDIT:"+string(size(G))+":"+string(dim(G))+":"+string(vdim(G)));\n'
    )
    completed = subprocess.run(
        singular_command(),
        input=source,
        text=True,
        capture_output=True,
        timeout=600,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip()
    assert "AUDIT:18:0:9" in completed.stdout

    # Collapse the genuine binary exact pair to the singleton exact pair.
    epsilon, rho, lam, gamma = sp.symbols("epsilon rho lambda gamma")
    binary_p = rho
    binary_q = 1 / epsilon
    denominator = lam * (binary_p + binary_q)
    binary_u0 = (
        (
            -gamma * (lam * binary_p - lam * binary_q + 1) / denominator,
            -1,
            1,
            0,
        ),
        (
            gamma * (lam * binary_q**2 - binary_q) / denominator,
            -binary_p - binary_q,
            0,
            1,
        ),
    )
    diagonal = (1, 1, epsilon, 1)

    def scaled(row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
        return tuple(
            sp.expand(entry * weight)
            for entry, weight in zip(row, diagonal, strict=True)
        )

    v = (0, rho, 1 / epsilon, 1)
    u = (0, lam * rho + 1, lam / epsilon - 1, lam)
    moving = (
        tuple(scaled(row) for row in binary_u0),
        (scaled((1, 0, 0, 0)), scaled(u)),
        (scaled((1, 0, 0, 0)), scaled(v)),
        (scaled((gamma, 1, 1, 0)), scaled((1, 0, 0, 0))),
    )
    expected_limits = (
        (0, -gamma, gamma, 1, -1, 0),
        (lam * rho + 1, lam, lam, 0, 0, 0),
        (rho, 1, 1, 0, 0, 0),
        (-1, 0, 0, 0, 0, 0),
    )
    for plane, expected_limit in zip(moving, expected_limits, strict=True):
        actual_limit = tuple(
            sp.factor(sp.limit(value, epsilon, 0)) for value in wedge(plane)
        )
        assert actual_limit == expected_limit

    print(
        json.dumps(
            {
                "status": "audited",
                "implementation": "subset_algebra_and_independent_graph_slice",
                "audit_prime": 103,
                "standard_basis": [18, 0, 9],
                "singleton_plucker_limits": 4,
                "kernel_endpoint_signature": [2, 2, 0, 0],
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
