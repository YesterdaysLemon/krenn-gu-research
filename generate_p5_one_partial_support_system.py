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
    invertible_positions: set[int] | None = None,
) -> str:
    retained = {
        exponent: coefficient
        for exponent, coefficient in terms.items()
        if coefficient
    }
    if not retained:
        return "0"
    if invertible_positions is None:
        invertible_positions = set(range(len(variable_names)))
    minima = [
        (
            min(exponent[index] for exponent in retained)
            if index in invertible_positions
            else 0
        )
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
    expected_partial_cells: int = 1,
) -> None:
    if expected_partial_cells not in range(0, 11):
        raise ValueError(
            "expected partial-cell count must be between zero and ten"
        )
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
        or noncoordinate.count(7) != 10 - expected_partial_cells
        or sum(mask in (3, 5, 6) for mask in noncoordinate)
        != expected_partial_cells
    ):
        raise ValueError(
            "not the requested exact-partial-cell boundary"
        )


def generate(
    supports: tuple[tuple[int, ...], ...],
    signature_indices: tuple[int, ...],
    expected_partial_cells: int = 1,
    coordinate_backbone_closure: bool = False,
    pure_saturation_only: bool = False,
    gauge_tree_edges: tuple[tuple[int, int, int], ...] | None = None,
    allow_arbitrary_support: bool = False,
    monomial_order: str = "dp",
    algorithm: str = "slimgb",
) -> tuple[str, dict]:
    if monomial_order not in ("dp", "lp", "Dp"):
        raise ValueError("unsupported global monomial order")
    if algorithm not in ("slimgb", "std"):
        raise ValueError("unsupported Singular basis algorithm")
    if allow_arbitrary_support:
        if (
            len(supports) != 5
            or any(len(row) != 5 for row in supports)
            or any(
                mask not in (0, 1, 2, 3, 4, 5, 6, 7)
                for row in supports
                for mask in row
            )
        ):
            raise ValueError(
                "arbitrary supports must be a 5 by 5 array "
                "of three-bit masks"
            )
    else:
        validate_supports(supports, expected_partial_cells)
    if allow_arbitrary_support and coordinate_backbone_closure:
        raise ValueError(
            "coordinate-backbone closure requires the exact-three "
            "coordinate support model"
        )
    if coordinate_backbone_closure and expected_partial_cells != 0:
        raise ValueError(
            "coordinate-backbone closure requires all ten "
            "noncoordinate cells to have full support"
        )
    if coordinate_backbone_closure and pure_saturation_only:
        raise ValueError(
            "coordinate-backbone closure already selects its "
            "invertible parameter set"
        )
    if coordinate_backbone_closure and gauge_tree_edges is not None:
        raise ValueError(
            "coordinate-backbone closure does not use a full gauge tree"
        )
    if len(signature_indices) != 5:
        raise ValueError("five signature indices are required")
    edges = tuple(
        (mode, source, colour)
        for mode in MODES
        for source in SOURCES
        for colour in COLOURS
        if supports[mode][source] & (1 << colour)
    )
    expected_entries = (
        len(edges)
        if allow_arbitrary_support
        else 45 - expected_partial_cells
    )
    if len(edges) != expected_entries:
        raise AssertionError(
            f"system must have {expected_entries} entries"
        )

    nodes = tuple(("r", source) for source in SOURCES) + tuple(
        ("c", mode, colour)
        for mode in MODES
        for colour in COLOURS
    )
    union_find = UnionFind(nodes)
    tree_edges = set()
    if gauge_tree_edges is not None:
        tree_candidates = gauge_tree_edges
        if (
            (
                len(tree_candidates) != 19
                if not allow_arbitrary_support
                else not 0 <= len(tree_candidates) <= 19
            )
            or len(set(tree_candidates)) != len(tree_candidates)
            or any(edge not in edges for edge in tree_candidates)
        ):
            raise ValueError(
                "gauge forest must contain distinct support entries "
                "and at most 19 entries"
            )
    else:
        tree_candidates = edges
        if pure_saturation_only:
            # A pure-only certificate remains valid when every non-tree
            # coefficient vanishes.  Prefer the always-present coordinate
            # entries in the gauge tree so that the resulting certificate
            # covers as many lower-support descendants as possible.
            tree_candidates = tuple(
                edge
                for edge in edges
                if supports[edge[0]][edge[1]] in (1, 2, 4)
            ) + tuple(
                edge
                for edge in edges
                if supports[edge[0]][edge[1]] not in (1, 2, 4)
            )
    for edge in tree_candidates:
        mode, source, colour = edge
        if (
            coordinate_backbone_closure
            and supports[mode][source] not in (1, 2, 4)
        ):
            continue
        if union_find.union(
            ("r", source), ("c", mode, colour)
        ):
            tree_edges.add(edge)
        elif gauge_tree_edges is not None:
            raise ValueError("gauge tree contains a cycle")
    if (
        gauge_tree_edges is not None
        and len(tree_edges) != len(gauge_tree_edges)
    ):
        raise ValueError("gauge forest contains a cycle")
    free_edges = tuple(edge for edge in edges if edge not in tree_edges)
    expected_free_edges = (
        len(edges) - len(tree_edges)
        if allow_arbitrary_support
        else 26 - expected_partial_cells
    )
    if coordinate_backbone_closure:
        if any(
            supports[mode][source] not in (1, 2, 4)
            for mode, source, _colour in tree_edges
        ):
            raise AssertionError("closure gauge used an optional entry")
    elif (
        (
            not allow_arbitrary_support
            and len(tree_edges) != 19
        )
        or len(free_edges) != expected_free_edges
    ):
        raise AssertionError("gauge graph dimensions changed")
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    final_names = [f"u{index}" for index in range(len(free_edges))]
    invertible_positions = {
        index
        for index, (mode, source, _colour) in enumerate(free_edges)
        if supports[mode][source] in (1, 2, 4)
    }
    if pure_saturation_only:
        invertible_positions = set()
    elif not coordinate_backbone_closure:
        invertible_positions = set(range(len(free_edges)))
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
        text = polynomial_string(
            terms,
            final_names,
            invertible_positions,
        )
        if len(set(colours)) == 1:
            pure_polynomials.append(f"({text})")
        elif text != "0":
            mixed_polynomials.append(text)
    mixed = list(dict.fromkeys(mixed_polynomials))
    if len(pure_polynomials) != 3:
        raise AssertionError("pure coefficient count changed")
    saturated_names = [
        final_names[index]
        for index in sorted(invertible_positions)
    ]
    saturation = "*".join(saturated_names + pure_polynomials)
    equations = mixed + [f"z*({saturation})-1"]
    variables = final_names + ["z"]
    header = [
        f"// signature source: {signature_indices}",
        f"// supports: {supports}",
    ]
    if gauge_tree_edges is not None:
        gauge_label = (
            "tree" if len(gauge_tree_edges) == 19 else "forest"
        )
        header.append(
            f"// gauge {gauge_label}: {gauge_tree_edges}"
        )
    if allow_arbitrary_support:
        header.append("// support model: arbitrary nonempty masks")
    if pure_saturation_only or coordinate_backbone_closure:
        header.append(
            f"// saturated parameters: {len(saturated_names)}"
        )
    program = "\n".join(
        header
        + [
            (
                "// coefficient stratum: coordinate-backbone closure"
                if coordinate_backbone_closure
                else (
                    "// coefficient stratum: gauge chart, "
                    "pure saturation only"
                    if pure_saturation_only
                    else "// coefficient stratum: exact support only"
                )
            ),
            f"// nonzero entries: {len(edges)}",
            f"// gauge-free variables: {len(free_edges)}",
            "// binomial relation rank: 0",
            "// binomial handling: unimodular elimination",
            "// selected pivot determinant: None",
            "// explicit binomial equations: 0",
            f"// Laurent parameters: {len(final_names)}",
            f"// distinct mixed equations: {len(mixed)}",
            f"ring r=0,({','.join(variables)}),{monomial_order};",
            "option(redSB);",
            "ideal I=" + ",\n".join(equations) + ";",
            f"ideal G={algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    metadata = {
        "nonzero_entries": len(edges),
        "gauge_free_variables": len(free_edges),
        "laurent_parameters": len(final_names),
        "saturated_parameters": len(saturated_names),
        "mixed_equations": len(mixed),
        "pure_coefficients": 3,
    }
    if len(tree_edges) != 19:
        metadata["gauge_fixed_entries"] = len(tree_edges)
    return program, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--supports", required=True)
    parser.add_argument("--indices", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--partial-cells",
        type=int,
        choices=tuple(range(0, 11)),
        default=1,
    )
    parser.add_argument(
        "--coordinate-backbone-closure",
        action="store_true",
    )
    parser.add_argument(
        "--pure-saturation-only",
        action="store_true",
    )
    parser.add_argument(
        "--gauge-tree",
        help=(
            "optional Python literal containing the 19 "
            "(mode, source, colour) gauge-tree entries"
        ),
    )
    parser.add_argument(
        "--allow-arbitrary-support",
        action="store_true",
    )
    parser.add_argument(
        "--order",
        choices=("dp", "lp", "Dp"),
        default="dp",
    )
    parser.add_argument(
        "--algorithm",
        choices=("slimgb", "std"),
        default="slimgb",
    )
    args = parser.parse_args()
    supports = tuple(
        tuple(map(int, row))
        for row in ast.literal_eval(args.supports)
    )
    indices = tuple(map(int, args.indices.split(",")))
    gauge_tree = (
        tuple(
            tuple(map(int, edge))
            for edge in ast.literal_eval(args.gauge_tree)
        )
        if args.gauge_tree is not None
        else None
    )
    program, metadata = generate(
        supports,
        indices,
        expected_partial_cells=args.partial_cells,
        coordinate_backbone_closure=args.coordinate_backbone_closure,
        pure_saturation_only=args.pure_saturation_only,
        gauge_tree_edges=gauge_tree,
        allow_arbitrary_support=args.allow_arbitrary_support,
        monomial_order=args.order,
        algorithm=args.algorithm,
    )
    args.output.write_text(program, encoding="utf-8", newline="\n")
    print(metadata)


if __name__ == "__main__":
    main()
