"""Exact q5_311 rare-slice Singular program construction."""

from __future__ import annotations

import itertools
from fractions import Fraction

from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_support_system as GENERATOR
from krenn_gu import p5_split_saturation as SPLIT

def build_program(
    record: dict,
    include_majority_pure: bool = False,
    basis_algorithm: str = "slimgb",
    inverse_first: bool = False,
) -> tuple[str, str, dict]:
    if basis_algorithm not in ("slimgb", "std"):
        raise ValueError("unsupported Singular basis algorithm")
    supports = HIGH.normalized_supports(
        record["closure_supports"]
    )
    tree = HIGH.normalized_tree(record["gauge_tree"])
    if supports[0] != HIGH.BRANCH_BACKBONES["q5_311"]:
        raise ValueError("record is not in normalized q5_311 form")
    HIGH.validate_forest(
        HIGH.normalized_supports(record["supports"]),
        supports,
        tree,
    )

    edges = tuple(
        (mode, source, colour)
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        for colour in SEMANTICS.COLOURS
        if supports[mode][source] & (1 << colour)
    )
    tree_set = set(tree)
    if len(tree_set) != len(tree) or any(
        edge not in edges for edge in tree
    ):
        raise ValueError("gauge forest is not contained in the chart")
    free_edges = tuple(edge for edge in edges if edge not in tree_set)
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    names = [f"u{index}" for index in range(len(free_edges))]
    one: GENERATOR.Expression = (
        Fraction(1),
        (0,) * len(free_edges),
    )

    def entry(
        mode: int,
        source: int,
        colour: int,
    ) -> GENERATOR.Expression | None:
        edge = (mode, source, colour)
        if edge in tree_set:
            return one
        position = free_position.get(edge)
        if position is None:
            return None
        exponent = [0] * len(free_edges)
        exponent[position] = 1
        return Fraction(1), tuple(exponent)

    def coefficient(colours: tuple[int, ...]) -> str:
        terms: dict[tuple[int, ...], Fraction] = {}
        for permutation in itertools.permutations(SEMANTICS.SOURCES):
            value = one
            for mode, source in enumerate(permutation):
                factor = entry(mode, source, colours[mode])
                if factor is None:
                    break
                value = GENERATOR.multiply(value, factor)
            else:
                terms[value[1]] = (
                    terms.get(value[1], Fraction(0)) + value[0]
                )
        return GENERATOR.polynomial_string(
            terms,
            names,
            set(),
        )

    mixed = []
    for colours in itertools.product(
        SEMANTICS.COLOURS,
        repeat=5,
    ):
        if colours[0] not in (1, 2) or len(set(colours)) == 1:
            continue
        polynomial = coefficient(colours)
        if polynomial != "0":
            mixed.append(polynomial)
    mixed = list(dict.fromkeys(mixed))
    pure_colours = (
        (0, 1, 2) if include_majority_pure else (1, 2)
    )
    pure = {
        colour: coefficient((colour,) * 5)
        for colour in pure_colours
    }
    if any(polynomial == "0" for polynomial in pure.values()):
        raise AssertionError("a required rare pure coefficient vanished")

    variables = names + ["z"]
    saturation = "*".join(
        f"({pure[colour]})" for colour in pure_colours
    )
    equations = mixed + [f"z*({saturation})-1"]
    program = "\n".join(
        [
            "// q5_311 simultaneous rare-colour P4 slices",
            f"// supports: {supports}",
            f"// gauge forest: {tree}",
            "// retained mode-zero colours: 1,2",
            f"// distinct rare mixed equations: {len(mixed)}",
            (
                "// saturated pure coefficients: "
                + ",".join(map(str, pure_colours))
            ),
            f"ring r=0,({','.join(variables)}),dp;",
            "option(redSB);",
            "ideal I=" + ",\n".join(equations) + ";",
            f"ideal G={basis_algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    safe_names = [
        f"v{index:02d}" for index in range(len(names))
    ]
    safe_name = dict(zip(names, safe_names, strict=True))

    def rename(expression: str) -> str:
        return SPLIT.IDENTIFIER_PATTERN.sub(
            lambda match: safe_name[match.group(0)],
            expression,
        )

    safe_mixed = [rename(polynomial) for polynomial in mixed]
    safe_pure = {
        colour: rename(polynomial)
        for colour, polynomial in pure.items()
    }
    inverse_names = [
        f"w{colour}" for colour in pure_colours
    ]
    split_variables = (
        inverse_names + safe_names
        if inverse_first
        else safe_names + inverse_names
    )
    split_program = "\n".join(
        [
            "// exact split saturation for q5_311 rare P4 slices",
            (
                "ring r=0,("
                + ",".join(split_variables)
                + "),dp;"
            ),
            "option(redSB);",
            "ideal I="
            + ",\n".join(
                [
                    *(
                        f"w{colour}*({safe_pure[colour]})-1"
                        for colour in pure_colours
                    ),
                    *safe_mixed,
                ]
            )
            + ";",
            f"ideal G={basis_algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    return program, split_program, {
        "closure_entries": len(edges),
        "gauge_forest_edges": len(tree),
        "variables": len(variables),
        "rare_mixed_equations": len(mixed),
        "saturated_pure_colours": pure_colours,
        "majority_mixed_equations": 0,
        "basis_algorithm": basis_algorithm,
        "split_inverse_variables_first": inverse_first,
    }


__all__ = ["build_program"]
