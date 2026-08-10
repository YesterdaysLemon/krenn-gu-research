#!/usr/bin/env python3
"""Verify one short rare-slice affine core in the q5_311 branch."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_311_RARE_AFFINE_CORE.md"
MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))

CLOSURE = (
    (1, 1, 1, 2, 4),
    (7, 7, 7, 1, 2),
    (7, 7, 4, 7, 1),
    (2, 2, 7, 7, 7),
    (4, 4, 2, 4, 7),
)
SOURCE_SUPPORT = (
    (1, 1, 1, 2, 4),
    (5, 5, 5, 1, 2),
    (7, 7, 4, 5, 1),
    (2, 2, 3, 7, 7),
    (4, 4, 2, 4, 5),
)
GAUGE_TREE = (
    (2, 0, 0),
    (2, 1, 1),
    (2, 2, 2),
    (4, 1, 2),
    (1, 0, 0),
    (3, 2, 0),
    (3, 0, 1),
    (0, 2, 0),
    (4, 2, 1),
    (1, 1, 0),
    (0, 3, 1),
    (3, 4, 0),
    (1, 2, 0),
    (3, 3, 0),
    (1, 1, 2),
    (0, 4, 2),
    (4, 4, 0),
    (3, 3, 2),
    (1, 4, 1),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_chart() -> None:
    if CLOSURE[0] != (1, 1, 1, 2, 4):
        raise AssertionError("chart is not in normalized q5_311 form")
    if any(
        actual & ~allowed
        for actual_row, closure_row in zip(
            SOURCE_SUPPORT,
            CLOSURE,
            strict=True,
        )
        for actual, allowed in zip(
            actual_row,
            closure_row,
            strict=True,
        )
    ):
        raise AssertionError("source support escaped the closure")
    if len(set(GAUGE_TREE)) != 19:
        raise AssertionError("gauge tree edge count changed")

    nodes = [
        *(("r", source) for source in SOURCES),
        *(
            ("c", mode, colour)
            for mode in MODES
            for colour in COLOURS
        ),
    ]
    parent = {node: node for node in nodes}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for mode, source, colour in GAUGE_TREE:
        if not SOURCE_SUPPORT[mode][source] & (1 << colour):
            raise AssertionError("gauge edge is absent from source support")
        left = find(("r", source))
        right = find(("c", mode, colour))
        if left == right:
            raise AssertionError("gauge edges contain a cycle")
        parent[left] = right
    if len({find(node) for node in nodes}) != 1:
        raise AssertionError("19 gauge edges do not span 20 nodes")


def main() -> None:
    validate_chart()
    tree = set(GAUGE_TREE)
    edges = tuple(
        (mode, source, colour)
        for mode in MODES
        for source in SOURCES
        for colour in COLOURS
        if CLOSURE[mode][source] & (1 << colour)
    )
    free_edges = tuple(edge for edge in edges if edge not in tree)
    if len(edges) != 45 or len(free_edges) != 26:
        raise AssertionError("chart variable count changed")
    variables = sp.symbols(f"u0:{len(free_edges)}")
    free_variable = dict(zip(free_edges, variables, strict=True))

    expected_named_edges = {
        16: (3, 1, 1),
        17: (3, 2, 1),
        18: (3, 2, 2),
        20: (3, 4, 1),
        24: (4, 4, 1),
        25: (4, 4, 2),
    }
    if any(
        free_edges[index] != edge
        for index, edge in expected_named_edges.items()
    ):
        raise AssertionError("named affine-core variables changed")

    def entry(mode: int, source: int, colour: int):
        edge = (mode, source, colour)
        if edge in tree:
            return sp.Integer(1)
        return free_variable.get(edge, sp.Integer(0))

    def coefficient(word: tuple[int, ...]):
        return sp.expand(
            sum(
                sp.prod(
                    entry(mode, source, word[mode])
                    for mode, source in enumerate(permutation)
                )
                for permutation in PERMUTATIONS
            )
        )

    words = {
        "F10000": (1, 0, 0, 0, 0),
        "F10010": (1, 0, 0, 1, 0),
        "F10100": (1, 0, 1, 0, 0),
        "F11100": (1, 1, 1, 0, 0),
        "F11110": (1, 1, 1, 1, 0),
        "F12200": (1, 2, 2, 0, 0),
        "F12202": (1, 2, 2, 0, 2),
        "F12220": (1, 2, 2, 2, 0),
        "F22202": (2, 2, 2, 0, 2),
        "P1": (1, 1, 1, 1, 1),
        "P2": (2, 2, 2, 2, 2),
    }
    coefficients = {
        name: coefficient(word) for name, word in words.items()
    }
    if any(
        len(set(word)) == 1
        for name, word in words.items()
        if name.startswith("F")
    ):
        raise AssertionError("an affine-core equation is not mixed")

    u = variables
    identity_one = sp.expand(
        (1 + u[17]) * coefficients["F10000"]
        - coefficients["F10010"]
        + u[16] * coefficients["F10100"]
        + u[20] * coefficients["F11100"]
        + u[24] * coefficients["F11110"]
        - coefficients["P1"]
    )
    identity_two = sp.expand(
        -u[25] * coefficients["F12200"]
        + (1 - u[18]) * coefficients["F12202"]
        + u[25] * coefficients["F12220"]
        + u[18] * coefficients["F22202"]
        - coefficients["P2"]
    )
    if identity_one != 0 or identity_two != 0:
        raise AssertionError("rare affine identities failed")

    identity_payload = {
        name: str(coefficients[name])
        for name in sorted(coefficients)
    }
    identity_hash = hashlib.sha256(
        json.dumps(
            identity_payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    output = {
        "verified": True,
        "scope": "one exact normalized q5_311 gauge chart",
        "closure_entries": len(edges),
        "gauge_tree_edges": len(GAUGE_TREE),
        "free_variables": len(free_edges),
        "first_identity_distinct_mixed_coefficients": 5,
        "first_identity_macaulay_rows": 6,
        "second_identity_distinct_mixed_coefficients": 4,
        "second_identity_macaulay_rows": 5,
        "identity_coefficients": "all plus or minus one",
        "pure_coefficients_forced_zero": [1, 2],
        "coefficient_expansion_sha256": identity_hash,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_311_rare_affine_core.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
