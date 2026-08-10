"""Two-vertex polynomial divisibility obstruction for three-colour systems.

If a three-colour weight system exactly produces the GHZ tensor, then for
every vertex pair (p,q), its bilinear edge polynomial B_pq(x,y) divides the
polynomial

    F_pq(x,y) = sum_c x_c y_c product_(r != p,q)
                  ((W_pr^T x) cross (W_qr^T y))_c.

This module constructs both polynomials numerically and measures the
least-squares remainder after division.  A nonzero remainder is a rigorous
obstruction once the input weights themselves are exact.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np

from prism_boundary import prism_weights
from search_witness import EquationSystem, load_candidate

Exponent = tuple[int, int, int]
BiExponent = tuple[Exponent, Exponent]
Polynomial = dict[BiExponent, complex]


def monomials(total_degree: int) -> tuple[Exponent, ...]:
    return tuple(
        (a, b, total_degree - a - b)
        for a in range(total_degree + 1)
        for b in range(total_degree - a + 1)
    )


def add_exponents(left: Exponent, right: Exponent) -> Exponent:
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for (left_x, left_y), left_value in left.items():
        for (right_x, right_y), right_value in right.items():
            key = (
                add_exponents(left_x, right_x),
                add_exponents(left_y, right_y),
            )
            result[key] = result.get(key, 0j) + left_value * right_value
    return {key: value for key, value in result.items() if value != 0}


def oriented_block(
    system: EquationSystem, weights: np.ndarray, first: int, second: int
) -> np.ndarray:
    blocks = system.edge_array(weights)
    if first < second:
        return blocks[system.edge_index[(first, second)]]
    return blocks[system.edge_index[(second, first)]].T


def cross_component_polynomial(
    block_p: np.ndarray, block_q: np.ndarray, component: int
) -> Polynomial:
    # (l cross m)_0 = l_1 m_2 - l_2 m_1, cyclically.
    positive = ((1, 2), (2, 0), (0, 1))[component]
    negative = ((2, 1), (0, 2), (1, 0))[component]
    result: Polynomial = {}
    for sign, (left_colour, right_colour) in (
        (1, positive),
        (-1, negative),
    ):
        for x_colour in range(3):
            for y_colour in range(3):
                coefficient = (
                    sign
                    * block_p[x_colour, left_colour]
                    * block_q[y_colour, right_colour]
                )
                if coefficient == 0:
                    continue
                x_exp = tuple(int(index == x_colour) for index in range(3))
                y_exp = tuple(int(index == y_colour) for index in range(3))
                key = (x_exp, y_exp)  # type: ignore[arg-type]
                result[key] = result.get(key, 0j) + coefficient
    return {key: value for key, value in result.items() if value != 0}


def contraction_polynomial(
    system: EquationSystem, weights: np.ndarray, p: int, q: int
) -> Polynomial:
    if system.d != 3:
        raise ValueError("the cross-product obstruction is specific to d=3")
    remaining = [vertex for vertex in range(system.n) if vertex not in (p, q)]
    total: Polynomial = {}
    for colour in range(3):
        x_exp = tuple(int(index == colour) for index in range(3))
        y_exp = tuple(int(index == colour) for index in range(3))
        term: Polynomial = {(x_exp, y_exp): 1 + 0j}  # type: ignore[dict-item]
        for vertex in remaining:
            term = multiply(
                term,
                cross_component_polynomial(
                    oriented_block(system, weights, p, vertex),
                    oriented_block(system, weights, q, vertex),
                    colour,
                ),
            )
        for key, value in term.items():
            total[key] = total.get(key, 0j) + value
    return {key: value for key, value in total.items() if value != 0}


def divisibility_remainder(
    system: EquationSystem, weights: np.ndarray, p: int, q: int
) -> dict[str, float | int]:
    degree = system.n - 1
    target_basis = tuple(itertools.product(monomials(degree), repeat=2))
    quotient_basis = tuple(itertools.product(monomials(degree - 1), repeat=2))
    target_index = {exponents: index for index, exponents in enumerate(target_basis)}

    contraction = contraction_polynomial(system, weights, p, q)
    target_vector = np.zeros(len(target_basis), dtype=np.complex128)
    for exponents, coefficient in contraction.items():
        target_vector[target_index[exponents]] = coefficient

    edge_block = oriented_block(system, weights, p, q)
    multiplication = np.zeros(
        (len(target_basis), len(quotient_basis)), dtype=np.complex128
    )
    for quotient_index, (x_exp, y_exp) in enumerate(quotient_basis):
        for x_colour in range(3):
            for y_colour in range(3):
                coefficient = edge_block[x_colour, y_colour]
                if coefficient == 0:
                    continue
                x_unit = tuple(int(index == x_colour) for index in range(3))
                y_unit = tuple(int(index == y_colour) for index in range(3))
                target_exp = (
                    add_exponents(x_exp, x_unit),  # type: ignore[arg-type]
                    add_exponents(y_exp, y_unit),  # type: ignore[arg-type]
                )
                multiplication[target_index[target_exp], quotient_index] += coefficient

    if np.linalg.norm(multiplication) == 0:
        remainder_norm = float(np.linalg.norm(target_vector))
        quotient_rank = 0
    else:
        quotient, _, quotient_rank, _ = np.linalg.lstsq(
            multiplication, target_vector, rcond=None
        )
        remainder_norm = float(
            np.linalg.norm(target_vector - multiplication @ quotient)
        )
    target_norm = float(np.linalg.norm(target_vector))
    relative_remainder = remainder_norm / max(target_norm, np.finfo(float).tiny)
    return {
        "p": p,
        "q": q,
        "edge_rank": int(np.linalg.matrix_rank(edge_block, tol=1e-10)),
        "target_norm": target_norm,
        "remainder_norm": remainder_norm,
        "relative_remainder": relative_remainder,
        "multiplication_rank": int(quotient_rank),
    }


def all_pair_remainders(
    system: EquationSystem, weights: np.ndarray
) -> list[dict[str, float | int]]:
    return [
        divisibility_remainder(system, weights, p, q)
        for p, q in itertools.combinations(range(system.n), 2)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--candidate", type=Path)
    source.add_argument("--prism-x", type=float)
    args = parser.parse_args()

    if args.candidate is not None:
        payload = json.loads(args.candidate.read_text(encoding="utf-8"))
        system = EquationSystem(int(payload["n"]), int(payload["d"]))
        weights, _ = load_candidate(args.candidate, system)
    else:
        system, weights = prism_weights(complex(args.prism_x))

    results = all_pair_remainders(system, weights)
    print(json.dumps(results, indent=2))
    print(
        "maximum relative remainder=",
        max(float(result["relative_remainder"]) for result in results),
    )


if __name__ == "__main__":
    main()
