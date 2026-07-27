"""Regenerate one exact-support P5 coefficient system independently."""

from __future__ import annotations

import argparse
import ast
import itertools
from fractions import Fraction
from pathlib import Path


MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))
ALL_COLOURINGS = tuple(itertools.product(COLOURS, repeat=5))
Expression = tuple[Fraction, tuple[int, ...]]


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


def multiply(left: Expression, right: Expression) -> Expression:
    return (
        left[0] * right[0],
        tuple(a + b for a, b in zip(left[1], right[1], strict=True)),
    )


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
            for value, minimum in zip(exponent, minima, strict=True)
        ]
        factors = []
        for variable, value in zip(
            variable_names, shifted, strict=True
        ):
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


def validate_supports(
    supports: tuple[tuple[int, ...], ...],
) -> None:
    if len(supports) != 5 or any(len(row) != 5 for row in supports):
        raise ValueError("supports must be a 5 by 5 array")
    if any(mask not in (1, 2, 3, 4, 5, 6, 7)
           for row in supports for mask in row):
        raise ValueError("invalid support mask")
    if any(
        sum(mask in (1, 2, 4) for mask in row) != 3
        for row in supports
    ):
        raise ValueError("each mode must have three coordinate rows")
    if any(
        sorted(
            supports[mode][source]
            for mode in MODES
            if supports[mode][source] in (1, 2, 4)
        )
        != [1, 2, 4]
        for source in SOURCES
    ):
        raise ValueError("source columns must contain 1, 2, and 4")
    noncoordinate = [
        mask
        for row in supports
        for mask in row
        if mask not in (1, 2, 4)
    ]
    if (
        len(noncoordinate) != 10
        or noncoordinate.count(7) != 9
        or sum(mask in (3, 5, 6) for mask in noncoordinate) != 1
    ):
        raise ValueError("not the exactly-one-partial boundary")


def generate(
    supports: tuple[tuple[int, ...], ...],
    signature_indices: tuple[int, ...],
) -> tuple[str, dict]:
    validate_supports(supports)
    if len(signature_indices) != 5:
        raise ValueError("five signature indices are required")
    edges = tuple(
        (mode, source, colour)
        for mode in MODES
        for source in SOURCES
        for colour in COLOURS
        if supports[mode][source] & (1 << colour)
    )
    if len(edges) != 44:
        raise AssertionError("one-partial system must have 44 entries")

    nodes = tuple(("r", source) for source in SOURCES) + tuple(
        ("c", mode, colour)
        for mode in MODES
        for colour in COLOURS
    )
    union_find = UnionFind(nodes)
    tree_edges = set()
    for edge in edges:
        mode, source, colour = edge
        if union_find.union(
            ("r", source), ("c", mode, colour)
        ):
            tree_edges.add(edge)
    free_edges = tuple(edge for edge in edges if edge not in tree_edges)
    if len(tree_edges) != 19 or len(free_edges) != 25:
        raise AssertionError("gauge graph dimensions changed")
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    final_names = [f"u{index}" for index in range(len(free_edges))]
    one: Expression = (
        Fraction(1),
        (0,) * len(free_edges),
    )

    def entry(
        mode: int, source: int, colour: int
    ) -> Expression | None:
        edge = (mode, source, colour)
        if edge in tree_edges:
            return one
        if edge not in free_position:
            return None
        exponent = [0] * len(free_edges)
        exponent[free_position[edge]] = 1
        return Fraction(1), tuple(exponent)

    mixed_polynomials = []
    pure_polynomials = []
    for colours in ALL_COLOURINGS:
        terms: dict[tuple[int, ...], Fraction] = {}
        for permutation in PERMUTATIONS:
            value = one
            for mode, source in enumerate(permutation):
                factor = entry(mode, source, colours[mode])
                if factor is None:
                    break
                value = multiply(value, factor)
            else:
                terms[value[1]] = (
                    terms.get(value[1], Fraction(0)) + value[0]
                )
        text = polynomial_string(terms, final_names)
        if len(set(colours)) == 1:
            pure_polynomials.append(f"({text})")
        elif text != "0":
            mixed_polynomials.append(text)
    mixed = list(dict.fromkeys(mixed_polynomials))
    if len(pure_polynomials) != 3:
        raise AssertionError("pure coefficient count changed")
    saturation = "*".join(final_names + pure_polynomials)
    equations = mixed + [f"z*({saturation})-1"]
    variables = final_names + ["z"]
    program = "\n".join(
        [
            f"// signature source: {signature_indices}",
            f"// supports: {supports}",
            "// coefficient stratum: exact support only",
            f"// nonzero entries: {len(edges)}",
            f"// gauge-free variables: {len(free_edges)}",
            "// binomial relation rank: 0",
            "// binomial handling: unimodular elimination",
            "// selected pivot determinant: None",
            "// explicit binomial equations: 0",
            f"// Laurent parameters: {len(final_names)}",
            f"// distinct mixed equations: {len(mixed)}",
            f"ring r=0,({','.join(variables)}),dp;",
            "option(redSB);",
            "ideal I=" + ",\n".join(equations) + ";",
            "ideal G=slimgb(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    return program, {
        "nonzero_entries": len(edges),
        "gauge_free_variables": len(free_edges),
        "laurent_parameters": len(final_names),
        "mixed_equations": len(mixed),
        "pure_coefficients": 3,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--supports", required=True)
    parser.add_argument("--indices", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    supports = tuple(
        tuple(map(int, row))
        for row in ast.literal_eval(args.supports)
    )
    indices = tuple(map(int, args.indices.split(",")))
    program, metadata = generate(supports, indices)
    args.output.write_text(program, encoding="utf-8", newline="\n")
    print(metadata)


if __name__ == "__main__":
    main()
