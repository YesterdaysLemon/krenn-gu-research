"""Verify the physical pair-companion transform and transport identities."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
from math import comb, factorial, gcd

import sympy as sp

Monomial = tuple[str, ...]
Polynomial = Counter[Monomial]


def monomial(*factors: str) -> Monomial:
    return tuple(sorted(factors))


def add_term(polynomial: Polynomial, *factors: str) -> None:
    polynomial[monomial(*factors)] += 1


def psi_root_array(order: int, complement: tuple[int, ...]) -> Polynomial:
    """Expand Psi_C(R) using a root-pair edge followed by a C-bijection."""

    roots = tuple(range(order))
    answer: Polynomial = Counter()
    for left, right in combinations(roots, 2):
        remaining = tuple(root for root in roots if root not in (left, right))
        for assigned_ports in permutations(complement):
            factors = [f"r{left}.{right}"]
            factors.extend(
                f"l{root}.{port}"
                for root, port in zip(remaining, assigned_ports, strict=True)
            )
            add_term(answer, *factors)
    return answer


def direct_g_c(order: int, complement: tuple[int, ...]) -> Polynomial:
    """Enumerate G_C directly by its unique root partial matching."""

    roots = tuple(range(order))
    answer: Polynomial = Counter()
    for matching_edge in combinations(roots, 2):
        free_roots = tuple(root for root in roots if root not in matching_edge)
        for assignment in permutations(complement):
            edge = f"r{matching_edge[0]}.{matching_edge[1]}"
            incidence = [
                f"l{root}.{port}"
                for root, port in zip(free_roots, assignment, strict=True)
            ]
            add_term(answer, edge, *incidence)
    return answer


def psi_residual_array(order: int, complement: tuple[int, ...]) -> Polynomial:
    """Expand Psi_C(K^Q), including both residual orientations."""

    roots = tuple(range(order))
    answer: Polynomial = Counter()
    for left, right in combinations(roots, 2):
        remaining = tuple(root for root in roots if root not in (left, right))
        for assigned_ports in permutations(complement):
            incidence = [
                f"l{root}.{port}"
                for root, port in zip(remaining, assigned_ports, strict=True)
            ]
            add_term(answer, f"x{left}", f"y{right}", *incidence)
            add_term(answer, f"y{left}", f"x{right}", *incidence)
    return answer


def direct_g_qc(order: int, complement: tuple[int, ...]) -> Polynomial:
    """Enumerate G_(Q union C) as all root-to-outside bijections."""

    outside = ("q0", "q1") + tuple(f"u{port}" for port in complement)
    answer: Polynomial = Counter()
    for assignment in permutations(outside):
        factors = []
        for root, vertex in enumerate(assignment):
            if vertex == "q0":
                factors.append(f"x{root}")
            elif vertex == "q1":
                factors.append(f"y{root}")
            else:
                factors.append(f"l{root}.{vertex[1:]}")
        add_term(answer, *factors)
    return answer


def check_matching_bijections() -> dict[int, int]:
    checked: dict[int, int] = {}
    for order in range(2, 8):
        targets = tuple(combinations(range(order), 2))
        expected_root_terms = comb(order, 2) * factorial(order - 2)
        expected_residual_terms = factorial(order)
        for target in targets:
            complement = tuple(port for port in range(order) if port not in target)
            root_transform = psi_root_array(order, complement)
            residual_transform = psi_residual_array(order, complement)
            assert root_transform == direct_g_c(order, complement)
            assert residual_transform == direct_g_qc(order, complement)
            assert sum(root_transform.values()) == expected_root_terms
            assert sum(residual_transform.values()) == expected_residual_terms
            assert set(root_transform.values()) == {1}
            assert set(residual_transform.values()) == {1}
        checked[order] = len(targets)
    return checked


def primitive_directions(bound: int = 3) -> tuple[tuple[int, int], ...]:
    directions = set()
    for delta in range(-bound, bound + 1):
        for eta in range(-bound, bound + 1):
            if delta == eta == 0:
                continue
            first, second = delta, eta
            common = gcd(abs(first), abs(second))
            first //= common
            second //= common
            if first < 0 or (first == 0 and second < 0):
                first, second = -first, -second
            directions.add((first, second))
    return tuple(sorted(directions))


def check_projective_kernel_and_transport() -> int:
    delta_s, eta_s, delta_t, eta_t, generator = sp.symbols(
        "delta_s eta_s delta_t eta_t generator"
    )
    desired = sp.Matrix([[delta_s, eta_s]])
    own_kernel = sp.Matrix([[-eta_s], [delta_s]])
    foreign_kernel = sp.Matrix([[-eta_t], [delta_t]])
    determinant = delta_t * eta_s - eta_t * delta_s
    assert sp.expand((desired * own_kernel)[0]) == 0
    assert sp.expand((desired * foreign_kernel)[0] - determinant) == 0
    transport = delta_t * eta_s * generator - eta_t * delta_s * generator
    assert sp.expand(transport - determinant * generator) == 0

    directions = primitive_directions()
    comparisons = 0
    for first in directions:
        row = sp.Matrix([[first[0], first[1]]])
        own = sp.Matrix([[-first[1]], [first[0]]])
        assert (row * own)[0] == 0
        for second in directions:
            foreign = sp.Matrix([[-second[1]], [second[0]]])
            value = int((row * foreign)[0])
            same = first == second
            assert (value == 0) == same
            comparisons += 1
    assert (1, 0) in directions
    assert (0, 1) in directions
    return comparisons


def check_target_coupling() -> None:
    delta_s, eta_s, delta_t, eta_t = sp.symbols("delta_s eta_s delta_t eta_t")
    diagonal, generator, alpha, pure = sp.symbols("diagonal generator alpha pure")
    determinant = delta_t * eta_s - eta_t * delta_s
    transport = determinant * generator
    difference = sp.expand(diagonal * transport - determinant * alpha * pure)
    target_relation = diagonal * generator - alpha * pure
    assert sp.expand(difference - determinant * target_relation) == 0


def main() -> None:
    matching_checks = check_matching_bijections()
    comparisons = check_projective_kernel_and_transport()
    check_target_coupling()
    print("physical pair-companion transforms: PASS")
    print(f"root orders and target counts: {matching_checks}")
    print(f"exact projective comparisons: {comparisons}")
    print("scope: identities only; synchronization and activity remain open")


if __name__ == "__main__":
    main()
