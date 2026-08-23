"""Focused exact checks for GLS33 residual-Laurent polarization."""

import runpy
from functools import cache
from itertools import product
from pathlib import Path

import sympy as sp

GLS32 = runpy.run_path(
    str(
        Path(__file__).with_name(
            "verify_maximal_root_surplus_two_zero_anchor_first_polarized_simultaneous_absorption_sharpness.py"
        )
    )
)

A0, A1, Q0, Q1, K, U1, U2, U3 = range(8)
PORTS = (K, U1, U2, U3)
ONE = sp.ones(3, 1)
E = tuple(sp.eye(3)[:, index] for index in range(3))

build_control = GLS32["build_control"]
edge_block = GLS32["edge_block"]
raw_graph_coefficient = GLS32["graph_coefficient"]
perfect_matchings = GLS32["perfect_matchings"]
edges = build_control()


@cache
def graph_coefficient(word: tuple[int, ...]) -> sp.Expr:
    return raw_graph_coefficient(edges, word)


def residual_shores() -> dict[str, object]:
    z0 = sp.Matrix(sp.symbols("z00 z01 z02"))
    z1 = sp.Matrix(sp.symbols("z10 z11 z12"))
    xi00 = edge_block(edges, A0, Q0) * z0
    xi01 = edge_block(edges, A0, Q1) * z1
    xi10 = edge_block(edges, A1, Q0) * z0
    xi11 = edge_block(edges, A1, Q1) * z1
    assert xi00 == z0[1] * E[1]
    assert xi01 == z1[2] * E[2]
    assert xi10 == z0[2] * E[2]
    assert xi11 == z1[1] * E[1]

    normal0 = xi00.cross(xi01)
    normal1 = xi10.cross(xi11)
    assert normal0 == z0[1] * z1[2] * E[0]
    assert normal1 == -z0[2] * z1[1] * E[0]
    for xi in (xi00, xi01):
        assert (xi.T * normal0)[0] == 0
        assert (xi.T * E[0])[0] == 0
    for xi in (xi10, xi11):
        assert (xi.T * normal1)[0] == 0
        assert (xi.T * E[0])[0] == 0
    return {
        "xi": (xi00, xi01, xi10, xi11),
        "canonical_normals": (normal0, normal1),
        "constant_normal": E[0],
        "canonical_bidegree": (1, 1),
    }


def resolved_failures(
    left: sp.Matrix, right: sp.Matrix
) -> dict[tuple[int, int, int, int, int, int], sp.Expr]:
    failures = {}
    for q0, q1 in product(range(3), repeat=2):
        for ports in product(range(3), repeat=4):
            observed = sum(
                left[a0] * right[a1] * graph_coefficient((a0, a1, q0, q1, *ports))
                for a0, a1 in product(range(3), repeat=2)
            )
            expected = (
                left[q0] * right[q0] if q0 == q1 and ports == (q0, q0, q0, q0) else 0
            )
            difference = sp.factor(observed - expected)
            if difference:
                failures[(q0, q1, *ports)] = difference
    return failures


def residual_support(failures) -> dict[tuple[int, int], int]:
    support = {}
    for word in failures:
        support[word[:2]] = support.get(word[:2], 0) + 1
    return support


def residual_polynomial(failures, ports) -> sp.Expr:
    z0 = sp.symbols("z00 z01 z02")
    z1 = sp.symbols("z10 z11 z12")
    return sp.factor(
        sum(
            value * z0[word[0]] * z1[word[1]]
            for word, value in failures.items()
            if word[2:] == ports
        )
    )


def all_ones_contraction_failures(failures) -> dict[tuple[int, ...], sp.Expr]:
    contracted = {}
    for ports in product(range(3), repeat=4):
        value = sp.factor(
            sum(
                coefficient
                for word, coefficient in failures.items()
                if word[2:] == ports
            )
        )
        if value:
            contracted[ports] = value
    return contracted


def coefficient_profiles() -> dict[str, object]:
    profiles = {
        "00": resolved_failures(ONE, ONE),
        "10": resolved_failures(E[0], ONE),
        "01": resolved_failures(ONE, E[0]),
        "11": resolved_failures(E[0], E[0]),
    }
    counts = {name: len(failures) for name, failures in profiles.items()}
    assert counts == {"00": 200, "10": 76, "01": 76, "11": 0}
    supports = {name: residual_support(failures) for name, failures in profiles.items()}
    assert supports["10"] == {(0, 1): 38, (2, 0): 38}
    assert supports["01"] == {(0, 2): 38, (1, 0): 38}
    assert supports["11"] == {}

    z00, z01, z02, z10, z11, z12 = sp.symbols("z00 z01 z02 z10 z11 z12")
    sample_ports = (0, 0, 0, 1)
    sample10 = residual_polynomial(profiles["10"], sample_ports)
    sample01 = residual_polynomial(profiles["01"], sample_ports)
    assert sp.factor(sample10 - (z00 * z11 - z02 * z10) / 4) == 0
    assert sp.factor(sample01 - (z00 * z12 - z01 * z10) / 4) == 0

    contracted = {
        name: all_ones_contraction_failures(failures)
        for name, failures in profiles.items()
    }
    assert len(contracted["00"]) == 41
    assert not contracted["10"]
    assert not contracted["01"]
    assert not contracted["11"]
    return {
        "coefficient_counts": counts,
        "residual_supports": supports,
        "sample_defects": (sample10, sample01),
        "all_ones_failure_counts": {
            name: len(failures) for name, failures in contracted.items()
        },
    }


def kernel_supplier_annihilation() -> dict[str, object]:
    a = {port: (ONE.T * edge_block(edges, A0, port)).T for port in PORTS}
    b = {port: (ONE.T * edge_block(edges, A1, port)).T for port in PORTS}
    kernels = {K: E[1], U1: E[1], U2: E[1], U3: E[1]}
    assert all((a[port].T * kernels[port])[0] == 0 for port in PORTS)
    assert all((b[port].T * kernels[port])[0] == 0 for port in PORTS)

    killed_pairs = 0
    for left_index in range(len(PORTS)):
        for right_index in range(left_index + 1, len(PORTS)):
            left = PORTS[left_index]
            right = PORTS[right_index]
            supplier = a[left] * b[right].T + b[left] * a[right].T
            assert (kernels[left].T * supplier * kernels[right])[0] == 0
            killed_pairs += 1

    killed_one_q = 0
    for port in PORTS:
        for residual in (Q0, Q1):
            xi0 = edge_block(edges, A0, residual) * ONE
            xi1 = edge_block(edges, A1, residual) * ONE
            supplier = (xi0.T * ONE)[0] * b[port] + (xi1.T * ONE)[0] * a[port]
            assert (supplier.T * kernels[port])[0] == 0
            killed_one_q += 1

    h_uhat = sum(
        sp.prod(edge_block(edges, left, right)[1, 1] for left, right in matching)
        for matching in perfect_matchings(PORTS)
    )
    p = 2
    diagonal_target = 1
    assert h_uhat == 1
    assert p * h_uhat == 2
    assert diagonal_target == 1
    constant_kernel_defect = p * h_uhat - diagonal_target
    assert constant_kernel_defect == 1
    return {
        "local_kernel_dimensions_at_least": 1,
        "killed_pair_suppliers": killed_pairs,
        "killed_one_q_suppliers": killed_one_q,
        "constant_kernel_values": (p * h_uhat, diagonal_target),
        "constant_kernel_defect": constant_kernel_defect,
    }


def main() -> None:
    shores = residual_shores()
    profiles = coefficient_profiles()
    kernels = kernel_supplier_annihilation()
    print("GLS33 residual-Laurent/root-deck primary checks: PASS")
    print("  formal residual shores:", shores)
    print("  residual coefficient profiles:", profiles)
    print("  constant-deck kernel annihilation:", kernels)
    print(
        "  scope: polynomial identities/anchor quotient; strategic/global closure OPEN"
    )


if __name__ == "__main__":
    main()
