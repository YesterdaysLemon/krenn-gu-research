#!/usr/bin/env python3
"""Independent audit of the two-residual coordinate-monomial no-go."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
NOTE = HERE / "TWO_RESIDUAL_COORDINATE_MONOMIAL_SLICE_UNIVERSALITY_NOGO.md"


def edge_label(left: int, right: int, roots: int, sector: str):
    """Classify an edge using integer vertices, independently of the primary."""
    blockers = roots + 2
    q0 = roots + blockers
    q1 = q0 + 1

    if left > right:
        left, right = right, left
    left_is_root = left < roots
    left_is_blocker = roots <= left < roots + blockers
    right_is_blocker = roots <= right < roots + blockers

    if left_is_root and right_is_blocker:
        return ("H", left, right - roots)
    if sector == "cofactor" and left_is_blocker and right_is_blocker:
        return ("W", left - roots, right - roots)
    if left == q0 and right == q1:
        return ("h",)
    if sector == "ports":
        if left_is_blocker and right == q0:
            return ("a", left - roots)
        if left_is_blocker and right == q1:
            return ("b", left - roots)
    return None


def anchored_matchings(pool: tuple[int, ...], roots: int, sector: str):
    """Pair the largest remaining vertex first (not the primary recurrence)."""
    if not pool:
        yield ()
        return
    anchor = pool[-1]
    for index, partner in enumerate(pool[:-1]):
        label = edge_label(partner, anchor, roots, sector)
        if label is None:
            continue
        smaller_pool = pool[:index] + pool[index + 1 : -1]
        for tail in anchored_matchings(smaller_pool, roots, sector):
            yield ((partner, anchor, label),) + tail


def signature(matching, roots: int, sector: str):
    root_ports = [None] * roots
    exceptional = []
    for _left, _right, label in matching:
        if label[0] == "H":
            root_ports[label[1]] = label[2]
        elif label[0] == "W":
            exceptional = sorted(label[1:])
        elif label[0] == "a":
            exceptional.append((0, label[1]))
        elif label[0] == "b":
            exceptional.append((1, label[1]))
    assert all(port is not None for port in root_ports)
    if sector == "cofactor":
        assert len(exceptional) == 2
        return tuple(root_ports), tuple(exceptional)
    assert sorted(kind for kind, _port in exceptional) == [0, 1]
    residual_ports = tuple(
        next(port for kind, port in exceptional if kind == residual)
        for residual in (0, 1)
    )
    return tuple(root_ports), residual_ports


def audit_matching_classes(roots: int):
    blockers = roots + 2
    vertices = tuple(range(2 * roots + 4))

    observed_cofactor = Counter(
        signature(matching, roots, "cofactor")
        for matching in anchored_matchings(vertices, roots, "cofactor")
    )
    expected_cofactor = {
        (assignment, omitted)
        for assignment in itertools.permutations(range(blockers), roots)
        for omitted in (tuple(sorted(set(range(blockers)) - set(assignment))),)
    }
    assert set(observed_cofactor) == expected_cofactor
    assert set(observed_cofactor.values()) == {1}

    observed_ports = Counter(
        signature(matching, roots, "ports")
        for matching in anchored_matchings(vertices, roots, "ports")
    )
    expected_ports = {
        (permutation[:roots], permutation[roots:])
        for permutation in itertools.permutations(range(blockers))
    }
    assert set(observed_ports) == expected_ports
    assert set(observed_ports.values()) == {1}

    cofactor_count = math.factorial(blockers) // 2
    port_count = math.factorial(blockers)
    assert len(observed_cofactor) == cofactor_count
    assert len(observed_ports) == port_count
    return {
        "roots": roots,
        "blockers": blockers,
        "cofactor_matchings": cofactor_count,
        "port_matchings": port_count,
        "multiplicity_one": True,
    }


def audit_kernel_and_scaling():
    g0 = sp.Matrix([[1, 0, -1]])
    g1 = sp.Matrix([[0, 1, -1]])
    stacked = sp.Matrix.vstack(g0, g1)
    v = sp.Matrix([1, 1, 1])
    assert stacked * v == sp.zeros(2, 1)
    assert stacked.rank() == 2

    coordinate_determinants = []
    for colour in range(3):
        coordinate = sp.zeros(1, 3)
        coordinate[0, colour] = 1
        determinant = sp.det(sp.Matrix.vstack(stacked, coordinate))
        assert determinant != 0
        coordinate_determinants.append(int(determinant))

    s, t = sp.symbols("s t")
    beta_on_kernel = sp.expand((s * v)[0] * (t * v)[0])
    assert beta_on_kernel == s * t

    d0, d1, d2 = sp.symbols("d0 d1 d2", nonzero=True)
    roots = (sp.Matrix([d0, d1, d2]),) + (v,) * 4
    diagonal = tuple(
        sp.prod(root[colour] for root in roots) * v[colour] ** 2 for colour in range(3)
    )
    assert diagonal == (d0, d1, d2)
    return {
        "kernel_rank": stacked.rank(),
        "kernel_generator": tuple(map(int, v)),
        "coordinate_augmentation_determinants": coordinate_determinants,
        "residual_edge_on_kernel": str(beta_on_kernel),
        "diagonal_coefficients": tuple(map(str, diagonal)),
    }


def audit_arbitrary_r_ledger():
    rows = []
    for roots in range(2, 9):
        blockers = roots + 2
        cofactor = math.comb(blockers, 2) * math.factorial(roots)
        assert cofactor == math.factorial(blockers) // 2
        rows.append(
            {
                "roots": roots,
                "blockers": blockers,
                "cofactor_assignments": cofactor,
                "two_port_assignments": math.factorial(blockers),
            }
        )
    return rows


def main():
    note = NOTE.read_text(encoding="utf-8")
    required = (
        "slice-universal for the unresolved",
        "no-go theorem for a proof route",
        "not a Krenn--Gu counterexample",
        "global Krenn--Gu conjecture remain **UNKNOWN** or **UNRESOLVED**",
    )
    assert all(phrase in note for phrase in required)

    report = {
        "status": "AUDIT_PASS",
        "method": "independent largest-vertex matching recurrence",
        "matching_classes": [audit_matching_classes(r) for r in range(2, 6)],
        "kernel_and_scaling": audit_kernel_and_scaling(),
        "arbitrary_r_ledger": audit_arbitrary_r_ledger(),
        "local_slice_nogo_only": True,
        "global_counterexample": False,
        "finite_field_used": False,
        "imports_project_code": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
