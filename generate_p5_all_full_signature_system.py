"""Regenerate exact all-full P5 signature systems independently."""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction
from pathlib import Path

from sympy import Matrix

import verify_p5_pair_signature_catalogue_coverage as PAIR_CATALOGUE


MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PAIRS = tuple(itertools.combinations(SOURCES, 2))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))
ALL_COLOURINGS = tuple(itertools.product(COLOURS, repeat=5))
Expression = tuple[Fraction, tuple[int, ...]]
_CATALOGUE: tuple[tuple, ...] | None = None


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
        tuple(a + b for a, b in zip(left[1], right[1])),
    )


def power(expression: Expression, exponent: int) -> Expression:
    return (
        expression[0] ** exponent,
        tuple(value * exponent for value in expression[1]),
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


def incidence_relations(
    signatures: tuple[tuple, ...],
    variables: tuple[tuple[int, int, int], ...],
) -> tuple[list[list[int]], list[Fraction]]:
    positions = {
        variable: index for index, variable in enumerate(variables)
    }
    rows = []
    constants = []
    for mode, signature in enumerate(signatures):
        _supports, incidences = signature
        for pair_index, (first, second) in enumerate(PAIRS):
            for coordinate in COLOURS:
                if not (incidences[pair_index] & (1 << coordinate)):
                    continue
                other = [
                    colour
                    for colour in COLOURS
                    if colour != coordinate
                ]
                first_term = (
                    (mode, first, other[0]),
                    (mode, second, other[1]),
                )
                second_term = (
                    (mode, first, other[1]),
                    (mode, second, other[0]),
                )
                active = (
                    all(variable in positions for variable in first_term),
                    all(variable in positions for variable in second_term),
                )
                if active == (False, False):
                    continue
                if active[0] != active[1]:
                    raise AssertionError("singleton incidence minor")
                row = [0] * len(variables)
                for variable in first_term:
                    row[positions[variable]] += 1
                for variable in second_term:
                    row[positions[variable]] -= 1
                rows.append(row)
                constants.append(Fraction(1))
    return rows, constants


def active_permutations(
    supports: tuple[tuple[int, ...], ...],
    colours: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in PERMUTATIONS
        if all(
            supports[mode][permutation[mode]]
            & (1 << colours[mode])
            for mode in MODES
        )
    )


def catalogue() -> tuple[tuple, ...]:
    global _CATALOGUE
    if _CATALOGUE is None:
        _CATALOGUE = PAIR_CATALOGUE.finite_field_local_signatures()
    return _CATALOGUE


def generate(signature_indices: tuple[int, ...]) -> tuple[str, dict]:
    if len(signature_indices) != 5:
        raise ValueError("five signature indices are required")
    local_catalogue = catalogue()
    signatures = tuple(
        local_catalogue[index] for index in signature_indices
    )
    supports = tuple(signature[0] for signature in signatures)
    if any(
        sorted(row).count(7) != 2
        or any(mask not in (1, 2, 4, 7) for mask in row)
        for row in supports
    ):
        raise ValueError("system is outside the all-full boundary")
    edges = tuple(
        (mode, source, colour)
        for mode in MODES
        for source in SOURCES
        for colour in COLOURS
        if supports[mode][source] & (1 << colour)
    )
    if len(edges) != 45:
        raise AssertionError("all-full system must have 45 entries")
    for colours in ALL_COLOURINGS:
        if (
            len(set(colours)) > 1
            and len(active_permutations(supports, colours)) == 2
        ):
            raise AssertionError(
                "unexpected two-term permanent coefficient"
            )

    nodes = tuple(("r", source) for source in SOURCES) + tuple(
        ("c", mode, colour)
        for mode in MODES
        for colour in COLOURS
    )
    union_find = UnionFind(nodes)
    tree_edges = set()
    for mode, source, colour in edges:
        if union_find.union(
            ("r", source), ("c", mode, colour)
        ):
            tree_edges.add((mode, source, colour))
    free_edges = tuple(edge for edge in edges if edge not in tree_edges)
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    if len(tree_edges) != 19 or len(free_edges) != 26:
        raise AssertionError("gauge graph dimensions changed")

    raw_rows, raw_constants = incidence_relations(
        signatures, edges
    )
    edge_position = {
        edge: index for index, edge in enumerate(edges)
    }
    relation_rows = []
    relation_constants = []
    for raw_row, constant in zip(
        raw_rows, raw_constants, strict=True
    ):
        projected = [0] * len(free_edges)
        for edge in free_edges:
            projected[free_position[edge]] = raw_row[
                edge_position[edge]
            ]
        if any(projected):
            relation_rows.append(projected)
            relation_constants.append(constant)
        elif constant != 1:
            raise AssertionError("gauge projection contradiction")
    relation_matrix = Matrix(relation_rows)
    independent_rows = list(relation_matrix.T.rref()[1])
    basis = relation_matrix[independent_rows, :]
    pivot_columns = list(basis.rref()[1])
    pivot_matrix = basis[:, pivot_columns]
    pivot_determinant = int(pivot_matrix.det())
    inverse = pivot_matrix.inv()
    if (
        len(independent_rows) != 5
        or abs(pivot_determinant) != 1
        or any(value.q != 1 for value in inverse)
    ):
        raise AssertionError("expected rank-five unimodular relations")
    nonpivot_columns = [
        index
        for index in range(len(free_edges))
        if index not in pivot_columns
    ]
    basis_constants = [
        relation_constants[index] for index in independent_rows
    ]
    final_names = [
        f"u{index}" for index in range(len(nonpivot_columns))
    ]
    free_expressions: list[Expression | None] = [None] * len(free_edges)
    for final_index, free_index in enumerate(nonpivot_columns):
        exponent = [0] * len(nonpivot_columns)
        exponent[final_index] = 1
        free_expressions[free_index] = (
            Fraction(1),
            tuple(exponent),
        )
    exponent_matrix = -inverse * basis[:, nonpivot_columns]
    for pivot_row, free_index in enumerate(pivot_columns):
        coefficient = Fraction(1)
        for relation_constant, raw_power in zip(
            basis_constants, inverse.row(pivot_row), strict=True
        ):
            coefficient *= relation_constant ** int(raw_power)
        exponents = tuple(
            int(value) for value in exponent_matrix.row(pivot_row)
        )
        free_expressions[free_index] = (coefficient, exponents)
    if any(expression is None for expression in free_expressions):
        raise AssertionError("incomplete Laurent parameterization")
    expressions = tuple(
        expression
        for expression in free_expressions
        if expression is not None
    )
    for row, expected in zip(
        relation_rows, relation_constants, strict=True
    ):
        value: Expression = (
            Fraction(1),
            (0,) * len(nonpivot_columns),
        )
        for expression, exponent in zip(
            expressions, row, strict=True
        ):
            if exponent:
                value = multiply(value, power(expression, exponent))
        if any(value[1]) or value[0] != expected:
            raise AssertionError("relation replay failed")

    one: Expression = (
        Fraction(1),
        (0,) * len(nonpivot_columns),
    )

    def entry(
        mode: int, source: int, colour: int
    ) -> Expression | None:
        edge = (mode, source, colour)
        if edge in tree_edges:
            return one
        if edge in free_position:
            return expressions[free_position[edge]]
        return None

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
    saturation_factors = final_names + pure_polynomials
    saturation = "*".join(saturation_factors)
    variables = final_names + ["z"]
    equations = mixed + [f"z*({saturation})-1"]
    program = "\n".join(
        [
            f"// signature source: {signature_indices}",
            f"// supports: {supports}",
            "// coefficient stratum: support plus pair incidences",
            f"// nonzero entries: {len(edges)}",
            f"// gauge-free variables: {len(free_edges)}",
            "// binomial relation rank: 5",
            "// binomial handling: unimodular elimination",
            f"// selected pivot determinant: {pivot_determinant}",
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
        "signature_indices": signature_indices,
        "supports": supports,
        "nonzero_entries": len(edges),
        "gauge_free_variables": len(free_edges),
        "relation_rank": 5,
        "pivot_determinant": pivot_determinant,
        "laurent_parameters": len(final_names),
        "mixed_equations": len(mixed),
        "pure_coefficients": 3,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indices", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    indices = tuple(map(int, args.indices.split(",")))
    program, metadata = generate(indices)
    args.output.write_text(program, encoding="utf-8", newline="\n")
    print(metadata)


if __name__ == "__main__":
    main()
