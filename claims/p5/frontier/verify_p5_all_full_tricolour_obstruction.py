#!/usr/bin/env python3
"""Verify the proper all-full P5 tricolour obstruction package."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = HERE
BOUNDARY = (
    REPO_ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "all_full_tricolour_boundary"
)

CASES = (
    {
        "name": "c10_orbit_126",
        "shape": "C10",
        "supports": (
            (7, 7, 4, 2, 1),
            (1, 7, 7, 4, 2),
            (2, 1, 7, 7, 4),
            (4, 2, 1, 7, 7),
            (7, 4, 2, 1, 7),
        ),
    },
    {
        "name": "c10_orbit_122",
        "shape": "C10",
        "supports": (
            (7, 7, 4, 2, 1),
            (4, 7, 7, 1, 2),
            (2, 1, 7, 7, 4),
            (1, 4, 2, 7, 7),
            (7, 2, 1, 4, 7),
        ),
    },
    {
        "name": "c4c6_orbit_56",
        "shape": "C4+C6",
        "supports": (
            (7, 7, 4, 2, 1),
            (7, 7, 2, 1, 4),
            (4, 1, 7, 7, 2),
            (2, 4, 1, 7, 7),
            (1, 2, 7, 4, 7),
        ),
    },
)

EXPECTED_SHA256 = {
    "c10_orbit_126.sing": (
        "46a6a69b76d76ff748c494ecfd13bc0a43bca0d554d56670bf57a5c037cc2eb6"
    ),
    "c10_orbit_126.ms": (
        "8a4e946a42c5804ac42ed8f69500bfc1c67e6960e0c50a9f99f0915ee5ac9bd6"
    ),
    "c10_orbit_126.msolve.out": (
        "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
    ),
    "c10_orbit_126.slimgb.out": (
        "da464856ccf5abe4ac99bf0afdf13f6250eabb46f44547a0f2d3320bfd22abb6"
    ),
    "c10_orbit_122.sing": (
        "243a62a855cfc3319ee38aa329d64b8875a19dcc6b1eb1ead42100ccc692df1e"
    ),
    "c10_orbit_122.ms": (
        "3ffcc6847be06b1649a25ea42cc653ddf42eeeaff778854217976a04eb14c38c"
    ),
    "c10_orbit_122.msolve.out": (
        "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
    ),
    "c10_orbit_122.slimgb.out": (
        "da464856ccf5abe4ac99bf0afdf13f6250eabb46f44547a0f2d3320bfd22abb6"
    ),
    "c4c6_orbit_56.sing": (
        "ebaeb60e1c078083e181c3da9503fb9db15d5f69d5636113d3481a331df426f4"
    ),
    "c4c6_orbit_56.ms": (
        "7ef9b8c74c8d23bd287f84f37f1fbc0df29236b3deaf42e67d3659ee5b4990bb"
    ),
    "c4c6_orbit_56.msolve.out": (
        "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
    ),
    "c4c6_orbit_56.slimgb.out": (
        "da464856ccf5abe4ac99bf0afdf13f6250eabb46f44547a0f2d3320bfd22abb6"
    ),
}

RING_RE = re.compile(
    r"^ring r=0,\((?P<variables>[A-Za-z0-9_,]+)\),dp;$",
    re.MULTILINE,
)
IDEAL_RE = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)


class UnionFind:
    def __init__(self, items: tuple[tuple, ...]) -> None:
        self.parent = {item: item for item in items}

    def find(self, item: tuple) -> tuple:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left: tuple, right: tuple) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        self.parent[right] = left
        return True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polynomial_string(
    terms: dict[tuple[int, ...], Fraction],
    variable_names: list[str],
) -> str:
    retained = {
        exponent: coefficient
        for exponent, coefficient in terms.items()
        if coefficient
    }
    if not retained:
        return "0"
    minima = [
        min(exponent[index] for exponent in retained)
        for index in range(len(variable_names))
    ]
    pieces = []
    for exponent, coefficient in sorted(retained.items()):
        shifted = [
            value - minimum
            for value, minimum in zip(exponent, minima)
        ]
        factors = []
        for variable, value in zip(variable_names, shifted):
            if value == 1:
                factors.append(variable)
            elif value:
                factors.append(f"{variable}^{value}")
        monomial = "*".join(factors) if factors else "1"
        if coefficient == 1:
            pieces.append(monomial)
        elif coefficient == -1:
            pieces.append(f"-({monomial})")
        else:
            pieces.append(
                f"({coefficient.numerator}/{coefficient.denominator})"
                f"*({monomial})"
            )
    return "+".join(pieces)


def reconstruct_equations(
    supports: tuple[tuple[int, ...], ...],
) -> tuple[list[str], list[str], str]:
    edges = tuple(
        (mode, source, colour)
        for mode in range(5)
        for source in range(5)
        for colour in range(3)
        if supports[mode][source] & (1 << colour)
    )
    nodes = tuple(("r", source) for source in range(5)) + tuple(
        ("c", mode, colour)
        for mode in range(5)
        for colour in range(3)
    )
    union_find = UnionFind(nodes)
    tree_edges = set()
    for mode, source, colour in edges:
        if union_find.union(
            ("r", source), ("c", mode, colour)
        ):
            tree_edges.add((mode, source, colour))
    free_edges = tuple(edge for edge in edges if edge not in tree_edges)
    if len(edges) != 45 or len(tree_edges) != 19 or len(free_edges) != 26:
        raise AssertionError("unexpected gauge graph dimensions")
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    names = [f"u{index}" for index in range(len(free_edges))]

    def coefficient(colouring: tuple[int, ...]) -> str:
        terms: dict[tuple[int, ...], Fraction] = defaultdict(Fraction)
        for permutation in itertools.permutations(range(5)):
            exponent = [0] * len(free_edges)
            for mode, source in enumerate(permutation):
                edge = (mode, source, colouring[mode])
                if edge not in tree_edges and edge not in free_position:
                    break
                if edge in free_position:
                    exponent[free_position[edge]] += 1
            else:
                terms[tuple(exponent)] += 1
        return polynomial_string(terms, names)

    mixed = []
    pure = []
    for colouring in itertools.product(range(3), repeat=5):
        if len(set(colouring)) == 1:
            pure.append(coefficient(colouring))
        elif len(set(colouring)) == 3:
            mixed.append(coefficient(colouring))
    if len(mixed) != 150 or len(pure) != 3:
        raise AssertionError("unexpected colour coefficient counts")
    if any(polynomial == "0" for polynomial in mixed + pure):
        raise AssertionError("representative contains a forced-zero target")
    saturation_factors = names + [f"({polynomial})" for polynomial in pure]
    saturation = f"z*({'*'.join(saturation_factors)})-1"
    return names, mixed, saturation


def expected_msolve(source_text: str) -> str:
    ring_match = RING_RE.search(source_text)
    ideal_match = IDEAL_RE.search(source_text)
    if ring_match is None or ideal_match is None:
        raise AssertionError("unrecognized packaged Singular source")
    variables = ring_match.group("variables").split(",")
    equations = ideal_match.group("equations").split(",\n")
    return (
        ",".join(variables)
        + "\n0\n"
        + ",\n".join(equations)
        + "\n"
    )


def verify_hash(path: Path) -> str:
    digest = sha256(path)
    expected = EXPECTED_SHA256.get(path.name)
    if expected is None:
        raise AssertionError(f"missing expected hash for {path.name}")
    if digest != expected:
        raise AssertionError(f"hash mismatch for {path.name}")
    return digest


def main() -> None:
    verified_cases = []
    for case in CASES:
        name = case["name"]
        source = BOUNDARY / f"{name}.sing"
        msolve_input = BOUNDARY / f"{name}.ms"
        msolve_output = BOUNDARY / f"{name}.msolve.out"
        slimgb_output = BOUNDARY / f"{name}.slimgb.out"
        for path in (source, msolve_input, msolve_output, slimgb_output):
            verify_hash(path)

        source_text = source.read_text(encoding="utf-8")
        support_marker = f"// supports: {case['supports']}"
        if support_marker not in source_text:
            raise AssertionError(f"{name} support marker differs")
        ring_match = RING_RE.search(source_text)
        ideal_match = IDEAL_RE.search(source_text)
        if ring_match is None or ideal_match is None:
            raise AssertionError(f"{name} source format differs")
        variables = ring_match.group("variables").split(",")
        equations = ideal_match.group("equations").split(",\n")
        if variables != [f"u{index}" for index in range(26)] + ["z"]:
            raise AssertionError(f"{name} ring variables differ")
        names, mixed, saturation = reconstruct_equations(case["supports"])
        if names != variables[:-1] or equations != mixed + [saturation]:
            raise AssertionError(
                f"{name} does not encode exactly the 150 tricolour "
                "coefficients and the nonzero saturation"
            )
        if msolve_input.read_text(encoding="utf-8") != expected_msolve(
            source_text
        ):
            raise AssertionError(f"{name} msolve conversion differs")
        if msolve_output.read_text(encoding="utf-8").strip() != "[-1]:":
            raise AssertionError(f"{name} msolve result is not unit ideal")
        if slimgb_output.read_text(encoding="utf-8").strip() != "UNIT_IDEAL":
            raise AssertionError(f"{name} Singular result is not unit ideal")
        verified_cases.append(
            {
                "name": name,
                "shape": case["shape"],
                "nonzero_entries": 45,
                "gauge_variables": 26,
                "tricolour_equations": 150,
                "two_colour_equations_used": 0,
                "msolve_result": "[-1]:",
            }
        )

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "the three proper-colour all-full exact-three-coordinate "
                    "P5 support orbits"
                ),
                "cases": verified_cases,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
