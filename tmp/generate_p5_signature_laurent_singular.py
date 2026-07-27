"""Generate a binomial-parameterized exact Singular test for one P_5 stratum."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import pathlib
from fractions import Fraction

from sympy import Matrix


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE = ROOT / "tmp" / "probe_p5_tricolour_support_sat.py"
SPEC = importlib.util.spec_from_file_location("p5_probe", PROBE)
P5 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(P5)

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
            piece = monomial
        elif coefficient == -1:
            piece = f"-({monomial})"
        else:
            piece = f"({coefficient.numerator}/{coefficient.denominator})*({monomial})"
        pieces.append(piece)
    return "+".join(pieces)


def main() -> None:
    parser = argparse.ArgumentParser()
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--indices")
    source_group.add_argument("--descriptor", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--metadata", type=pathlib.Path)
    parser.add_argument(
        "--order", choices=("dp", "lp", "Dp", "ds"), default="dp"
    )
    parser.add_argument(
        "--algorithm",
        choices=("std", "slimgb"),
        default="std",
    )
    parser.add_argument(
        "--support-only",
        action="store_true",
        help=(
            "ignore pair-incidence binomials and test the larger exact-support "
            "coefficient stratum"
        ),
    )
    parser.add_argument(
        "--implicit-binomial-ideal",
        action="store_true",
        help=(
            "keep pair-incidence binomials as saturated ideal equations "
            "instead of eliminating them, for differential testing"
        ),
    )
    args = parser.parse_args()
    if args.indices is not None:
        indices: tuple[int, ...] | None = tuple(
            map(int, args.indices.split(","))
        )
        if len(indices) != 5:
            raise ValueError("five signature indices are required")
        catalogue = P5.finite_field_local_signatures()
        signatures = tuple(catalogue[index] for index in indices)
        signature_label = str(indices)
    else:
        indices = None
        descriptor = json.loads(
            args.descriptor.read_text(encoding="utf-8")
        )
        raw_supports = descriptor["supports"]
        raw_incidences = descriptor["pair_incidences"]
        if len(raw_supports) != 5 or len(raw_incidences) != 5:
            raise ValueError("descriptor requires five local maps")
        signatures = tuple(
            (
                tuple(map(int, raw_supports[mode])),
                tuple(map(int, raw_incidences[mode])),
            )
            for mode in P5.MODES
        )
        signature_label = f"abstract descriptor {args.descriptor.name}"
    supports = tuple(signature[0] for signature in signatures)
    edges = tuple(
        (mode, source, colour)
        for mode in P5.MODES
        for source in P5.SOURCES
        for colour in P5.COLOURS
        if supports[mode][source] & (1 << colour)
    )

    nodes = tuple(("r", source) for source in P5.SOURCES) + tuple(
        ("c", mode, colour)
        for mode in P5.MODES
        for colour in P5.COLOURS
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

    relation_rows = []
    relation_constants = []
    if not args.support_only:
        frontier = P5.binomial_closure_result(
            supports, signatures, return_frontier=True
        )
        if frontier is None or not frontier.get("frontier"):
            raise RuntimeError(
                f"signature tuple is already contradictory: {frontier}"
            )
        original_variables = tuple(frontier["variables"])
        original_position = {
            variable: index
            for index, variable in enumerate(original_variables)
        }
        for raw_row, raw_constant in zip(
            frontier["rows"], frontier["constants"]
        ):
            projected = [0] * len(free_edges)
            for edge in free_edges:
                projected[free_position[edge]] = int(
                    raw_row[original_position[edge]]
                )
            if any(projected):
                relation_rows.append(projected)
                relation_constants.append(Fraction(raw_constant))
            elif Fraction(raw_constant) != 1:
                raise RuntimeError("gauge projection exposed a contradiction")

    relation_rank = 0
    pivot_determinant: int | None = None
    use_implicit_relations = False
    relation_polynomials: list[str] = []
    if relation_rows:
        relation_matrix = Matrix(relation_rows)
        independent_rows = list(relation_matrix.T.rref()[1])
        basis = relation_matrix[independent_rows, :]
        relation_rank = len(independent_rows)
        pivot_columns = list(basis.rref()[1])
        pivot_matrix = basis[:, pivot_columns]
        pivot_determinant = int(pivot_matrix.det())
        inverse = pivot_matrix.inv()
        use_implicit_relations = (
            args.implicit_binomial_ideal
            or abs(pivot_determinant) != 1
            or any(value.q != 1 for value in inverse)
        )
        if use_implicit_relations:
            pivot_columns = []
            nonpivot_columns = list(range(len(free_edges)))
        else:
            nonpivot_columns = [
                index
                for index in range(len(free_edges))
                if index not in pivot_columns
            ]
        basis_constants = [
            relation_constants[index] for index in independent_rows
        ]
    else:
        basis = Matrix.zeros(0, len(free_edges))
        pivot_columns = []
        inverse = Matrix.zeros(0, 0)
        nonpivot_columns = list(range(len(free_edges)))
        basis_constants = []

    final_names = [f"u{index}" for index in range(len(nonpivot_columns))]
    free_expressions: list[Expression | None] = [None] * len(free_edges)
    for final_index, free_index in enumerate(nonpivot_columns):
        exponent = [0] * len(nonpivot_columns)
        exponent[final_index] = 1
        free_expressions[free_index] = (Fraction(1), tuple(exponent))
    if pivot_columns and not use_implicit_relations:
        free_block = basis[:, nonpivot_columns]
        exponent_matrix = -inverse * free_block
        for pivot_row, free_index in enumerate(pivot_columns):
            coefficient = Fraction(1)
            for relation_constant, raw_power in zip(
                basis_constants, inverse.row(pivot_row)
            ):
                coefficient *= relation_constant ** int(raw_power)
            exponents = tuple(
                int(value) for value in exponent_matrix.row(pivot_row)
            )
            free_expressions[free_index] = (coefficient, exponents)
    assert all(expression is not None for expression in free_expressions)
    expressions = tuple(expression for expression in free_expressions if expression)

    if use_implicit_relations:
        # On the coefficient torus, x^row = expected is equivalent to the
        # polynomial x^(row_+) - expected*x^(row_-) = 0.  Keeping these
        # binomials in the saturated ideal avoids choosing roots when the
        # relation lattice has a non-unimodular pivot minor.
        for row, expected in zip(relation_rows, relation_constants):
            positive = tuple(max(exponent, 0) for exponent in row)
            negative = tuple(max(-exponent, 0) for exponent in row)
            relation_polynomials.append(
                polynomial_string(
                    {
                        positive: Fraction(1),
                        negative: -expected,
                    },
                    final_names,
                )
            )
        relation_polynomials = list(dict.fromkeys(relation_polynomials))
        if any(polynomial == "0" for polynomial in relation_polynomials):
            raise RuntimeError("implicit relation unexpectedly vanished")
    else:
        # Replay every original relation under the parameterization.
        for row, expected in zip(relation_rows, relation_constants):
            value: Expression = (
                Fraction(1),
                (0,) * len(nonpivot_columns),
            )
            for expression, exponent in zip(expressions, row):
                if exponent:
                    value = multiply(value, power(expression, exponent))
            assert all(exponent == 0 for exponent in value[1])
            assert value[0] == expected

    one: Expression = (Fraction(1), (0,) * len(nonpivot_columns))

    def entry(mode: int, source: int, colour: int) -> Expression | None:
        edge = (mode, source, colour)
        if edge not in free_position and edge not in tree_edges:
            return None
        if edge in tree_edges:
            return one
        return expressions[free_position[edge]]

    def monomial(
        selected: list[tuple[int, int, int]]
    ) -> Expression | None:
        value = one
        for mode, source, colour in selected:
            factor = entry(mode, source, colour)
            if factor is None:
                return None
            value = multiply(value, factor)
        return value

    mixed_polynomials = []
    mixed_records = []
    pure_polynomials = []
    pure_records = []
    for colours in P5.ALL_COLOURINGS:
        terms: dict[tuple[int, ...], Fraction] = {}
        for permutation in P5.PERMUTATIONS:
            value = monomial(
                [
                    (mode, permutation[mode], colours[mode])
                    for mode in P5.MODES
                ]
            )
            if value is None:
                continue
            terms[value[1]] = terms.get(value[1], Fraction(0)) + value[0]
        text = polynomial_string(terms, final_names)
        if len(set(colours)) == 1:
            pure_polynomials.append(f"({text})")
            pure_records.append(
                {"colours": colours, "polynomial": text}
            )
        elif text != "0":
            mixed_polynomials.append(text)
            mixed_records.append(
                {"colours": colours, "polynomial": text}
            )

    saturation_factors = final_names + pure_polynomials
    saturation = "*".join(saturation_factors) if saturation_factors else "1"
    ring_variables = final_names + ["z"]
    equations = relation_polynomials + list(dict.fromkeys(mixed_polynomials))
    equations.append(f"z*({saturation})-1")
    binomial_handling = (
        "implicit saturated ideal"
        if use_implicit_relations
        else "unimodular elimination"
    )
    program = "\n".join(
        [
            f"// signature source: {signature_label}",
            f"// supports: {supports}",
            (
                "// coefficient stratum: exact support only"
                if args.support_only
                else "// coefficient stratum: support plus pair incidences"
            ),
            f"// nonzero entries: {len(edges)}",
            f"// gauge-free variables: {len(free_edges)}",
            f"// binomial relation rank: {relation_rank}",
            f"// binomial handling: {binomial_handling}",
            f"// selected pivot determinant: {pivot_determinant}",
            f"// explicit binomial equations: {len(relation_polynomials)}",
            f"// Laurent parameters: {len(final_names)}",
            f"// distinct mixed equations: {len(set(mixed_polynomials))}",
            f"ring r=0,({','.join(ring_variables)}),{args.order};",
            "option(redSB);",
            "ideal I=" + ",\n".join(equations) + ";",
            f"ideal G={args.algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    args.output.parent.mkdir(exist_ok=True)
    args.output.write_text(program, encoding="utf-8")
    if args.metadata is not None:
        args.metadata.parent.mkdir(exist_ok=True)
        args.metadata.write_text(
            json.dumps(
                {
                    "signature_source": signature_label,
                    "supports": supports,
                    "support_only": args.support_only,
                    "binomial_handling": binomial_handling,
                    "pivot_determinant": pivot_determinant,
                    "relation_polynomials": relation_polynomials,
                    "variables": final_names,
                    "pure": pure_records,
                    "mixed": mixed_records,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print(
        {
            "output": str(args.output),
            "signature_indices": indices,
            "nonzero_entries": len(edges),
            "gauge_free_variables": len(free_edges),
            "relation_rank": relation_rank,
            "binomial_handling": binomial_handling,
            "pivot_determinant": pivot_determinant,
            "relation_equations": len(relation_polynomials),
            "laurent_parameters": len(final_names),
            "mixed_equations": len(set(mixed_polynomials)),
            "support_only": args.support_only,
            "order": args.order,
        }
    )


if __name__ == "__main__":
    main()
