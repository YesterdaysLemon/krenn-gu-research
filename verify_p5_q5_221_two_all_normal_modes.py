#!/usr/bin/env python3
"""Verify the monotone two-all-normal-modes obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symmetric_tensor(factors):
    order = len(factors)
    dimension = len(factors[0])
    tensor = {}
    for indices in itertools.product(range(dimension), repeat=order):
        value = sum(
            sp.prod(
                factors[mode][indices[permutation[mode]]]
                for mode in range(order)
            )
            for permutation in itertools.permutations(range(order))
        )
        if value:
            tensor[indices] = sp.expand(value)
    return tensor


def contract_first(tensor, covector):
    output = {}
    for indices, coefficient in tensor.items():
        value = coefficient * covector[indices[0]]
        if value:
            remaining = indices[1:]
            output[remaining] = sp.expand(
                output.get(remaining, 0) + value
            )
    return {
        indices: coefficient
        for indices, coefficient in output.items()
        if coefficient
    }


def proportional_tensors(first, second):
    keys = set(first) | set(second)
    ratios = []
    for key in keys:
        left = first.get(key, 0)
        right = second.get(key, 0)
        if not left and not right:
            continue
        if not left or not right:
            return False
        ratios.append(sp.factor(left / right))
    return bool(ratios) and len(set(ratios)) == 1


def component_count(edges):
    parent = list(range(4))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        root_left = find(left)
        root_right = find(right)
        parent[root_left] = root_right
    return len({find(vertex) for vertex in range(4)})


def main() -> None:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = tuple(left + right for left, right in zip(e[0], e[1]))
    h0 = tuple(left - right for left, right in zip(e[0], e[1]))
    u1 = tuple(left + right for left, right in zip(e[2], e[3]))
    h1 = tuple(left - right for left, right in zip(e[2], e[3]))
    h2 = e[4]
    t0 = symmetric_tensor((u0, e[2], e[3], h2))
    t1 = symmetric_tensor((e[0], e[1], u1, h2))
    t2 = symmetric_tensor((e[0], e[1], e[2], e[3]))

    residual_0 = contract_first(contract_first(t0, h2), h1)
    residual_1 = contract_first(contract_first(t1, h2), h0)
    residual_2 = contract_first(contract_first(t2, h1), h0)
    expected_0 = symmetric_tensor((u0, h1))
    expected_1 = symmetric_tensor((h0, u1))
    expected_2 = symmetric_tensor((h0, h1))
    assert proportional_tensors(residual_0, expected_0)
    assert proportional_tensors(residual_1, expected_1)
    assert proportional_tensors(residual_2, expected_2)

    # Vertices are a,b,c,d.  Each rank-one equation chooses an endpoint
    # at which its source edge becomes dependent.
    edges = ((0, 3), (1, 2), (1, 3))
    colouring_profiles = []
    for colours in itertools.product((0, 1), repeat=3):
        endpoint_edges = tuple(
            tuple(edge for edge, colour in zip(edges, colours) if colour == side)
            for side in (0, 1)
        )
        component_counts = tuple(
            component_count(side_edges) for side_edges in endpoint_edges
        )
        assert min(component_counts) <= 2
        colouring_profiles.append(component_counts)

    output = {
        "verified": True,
        "field": "C",
        "cover_orbit": 5,
        "bilinear_residuals": [
            "Sym(u0,h1)",
            "Sym(h0,u1)",
            "Sym(h0,h1)",
        ],
        "dependency_edges": ["a-d", "b-c", "b-d"],
        "abstract_endpoint_colourings_checked": len(colouring_profiles),
        "maximum_forced_endpoint_span": 2,
        "required_endpoint_rank": 3,
        "monotone_cover_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_two_all_normal_modes_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
