#!/usr/bin/env python3
"""Exact verifier for the rank-five common-port 1+1+1 checkpoint."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md"
PAIRS = tuple(itertools.combinations(range(5), 2))
TRIPLES = tuple(itertools.combinations(range(5), 3))

VECTORS = {
    "x01": (0, -1, -1, 0, 0),
    "x02": (1, 0, 0, 0, -2),
    "x10": (0, 0, 0, -1, 1),
    "x12": (-1, 0, 1, 0, 0),
    "x20": (-1, 1, 0, 0, 0),
    "x21": (1, 0, 0, 2, 0),
}

BAD_NAMES = (
    ("x10", "x21"),
    ("x12", "x20"),
    ("x12", "x21"),
    ("x01", "x20"),
    ("x02", "x20"),
    ("x02", "x21"),
    ("x01", "x10"),
    ("x01", "x12"),
    ("x02", "x10"),
)

GOOD_NAMES = (
    ("x10", "x20"),
    ("x01", "x21"),
    ("x02", "x12"),
)

K_BASIS_INDICES = (0, 1, 2, 4, 6)

SPLIT_MINORS = (
    ((0, 1, 2), (0, 1, 2)),
    ((0, 1, 2), (0, 2, 3)),
    ((0, 1, 2), (0, 3, 4)),
    ((0, 1, 3), (0, 1, 2)),
    ((0, 1, 3), (0, 1, 4)),
    ((0, 1, 3), (0, 3, 4)),
    ((0, 1, 4), (0, 1, 2)),
    ((0, 1, 4), (0, 3, 4)),
    ((0, 2, 3), (0, 1, 4)),
    ((0, 2, 3), (0, 2, 3)),
    ((0, 2, 3), (0, 3, 4)),
    ((0, 2, 4), (0, 2, 3)),
    ((0, 2, 4), (0, 3, 4)),
    ((0, 3, 4), (0, 1, 4)),
    ((0, 3, 4), (0, 3, 4)),
    ((1, 2, 3), (0, 1, 2)),
    ((1, 2, 3), (0, 1, 4)),
    ((1, 2, 3), (0, 2, 3)),
    ((1, 2, 4), (0, 1, 2)),
    ((1, 2, 4), (0, 2, 3)),
    ((1, 3, 4), (0, 1, 2)),
    ((1, 3, 4), (0, 1, 4)),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def product_two(left: tuple[int, ...], right: tuple[int, ...]) -> list[int]:
    return [
        left[first] * right[second] + left[second] * right[first]
        for first, second in PAIRS
    ]


def product_three(
    first: tuple[int, ...],
    second: tuple[int, ...],
    third: tuple[int, ...],
) -> list[int]:
    return [
        sum(
            first[order[0]] * second[order[1]] * third[order[2]]
            for order in itertools.permutations(triple)
        )
        for triple in TRIPLES
    ]


def pairing_matrix(quadratics: list[list[int]]) -> sp.Matrix:
    return sp.Matrix(
        [
            [
                quadratic[
                    PAIRS.index(
                        tuple(index for index in range(5) if index not in triple)
                    )
                ]
                for triple in TRIPLES
            ]
            for quadratic in quadratics
        ]
    )


def canonical_factor(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    polynomial = sp.Poly(expression, *variables, domain=sp.QQ)
    return sp.Poly(
        sp.expand(polynomial.as_expr() / polynomial.LC()),
        *variables,
        domain=sp.QQ,
    )


def factor_matrix(
    polynomial: sp.Poly,
    b_variables: tuple[sp.Symbol, ...],
    c_variables: tuple[sp.Symbol, ...],
) -> list[list[str]]:
    return [
        [
            str(polynomial.coeff_monomial(b_variables[i] * c_variables[j]))
            for j in range(5)
        ]
        for i in range(5)
    ]


def minimal_hitting_sets(edges: list[tuple[int, ...]], vertices: int) -> list[int]:
    minimal: list[int] = []
    for mask in range(1, 1 << vertices):
        if not all(any(mask & (1 << vertex) for vertex in edge) for edge in edges):
            continue
        if any((old & mask) == old for old in minimal):
            continue
        minimal.append(mask)
    return minimal


def main() -> None:
    exceptional_pairs = (
        (VECTORS["x01"], VECTORS["x02"]),
        (VECTORS["x10"], VECTORS["x12"]),
        (VECTORS["x20"], VECTORS["x21"]),
    )
    assert [sp.Matrix([left, right]).rank() for left, right in exceptional_pairs] == [
        2,
        2,
        2,
    ]

    relation_weights = (1, 1, 2, 1, 1, 1)
    ordered_vectors = tuple(VECTORS[name] for name in VECTORS)
    assert [
        sum(
            weight * vector[column]
            for weight, vector in zip(relation_weights, ordered_vectors)
        )
        for column in range(5)
    ] == [0] * 5
    assert sp.Matrix(ordered_vectors).rank() == 5

    bad = [product_two(VECTORS[left], VECTORS[right]) for left, right in BAD_NAMES]
    good = [product_two(VECTORS[left], VECTORS[right]) for left, right in GOOD_NAMES]
    bad_rank = sp.Matrix(bad).rank()
    total_rank = sp.Matrix(bad + good).rank()
    assert bad_rank == 5
    assert total_rank == 8

    k_basis = [bad[index] for index in K_BASIS_INDICES]
    assert sp.Matrix(k_basis).rank() == 5
    assert sp.Matrix(k_basis + bad).rank() == 5

    h_basis = pairing_matrix(bad).nullspace()
    l_basis = pairing_matrix(bad + good).nullspace()
    assert len(h_basis) == 5
    assert len(l_basis) == 2

    ell_factors = (
        (
            (0, 0, 1, 0, -2),
            (1, 0, 0, -2, 0),
            (0, 1, 0, -2, 0),
        ),
        (
            (1, 0, 1, 0, 0),
            (0, 1, 0, 0, -2),
            (0, 0, 0, 1, 1),
        ),
    )
    ell_vectors = [product_three(*factors) for factors in ell_factors]
    total_pairing = pairing_matrix(bad + good)
    assert total_pairing * sp.Matrix.hstack(*map(sp.Matrix, ell_vectors)) == sp.zeros(
        12, 2
    )
    assert sp.Matrix(ell_vectors).rank() == 2
    assert sp.Matrix.hstack(*l_basis, *map(sp.Matrix, ell_vectors)).rank() == 2

    h_matrix = sp.Matrix.hstack(*h_basis)
    good_on_h = pairing_matrix(good) * h_matrix
    assert good_on_h.rank() == 3
    diagonal_duals: list[sp.Matrix] = []
    for colour in range(3):
        target = sp.eye(3).col(colour)
        solution, parameters = good_on_h.gauss_jordan_solve(target)
        if parameters.rows:
            solution = solution.subs({parameter: 0 for parameter in parameters})
        cubic = h_matrix * solution
        diagonal_duals.append(cubic)
    assert pairing_matrix(good) * sp.Matrix.hstack(*diagonal_duals) == sp.eye(3)
    assert pairing_matrix(bad) * sp.Matrix.hstack(*diagonal_duals) == sp.zeros(9, 3)

    b_variables = sp.symbols("b0:5")
    c_variables = sp.symbols("c0:5")
    variables = b_variables + c_variables
    catalecticant = sp.zeros(5, 5)
    for row, quadratic in enumerate(k_basis):
        for source_coordinate in range(5):
            entry = 0
            for b_index in range(5):
                for c_index in range(5):
                    if len({source_coordinate, b_index, c_index}) < 3:
                        continue
                    triple = tuple(sorted((source_coordinate, b_index, c_index)))
                    complement = tuple(
                        index for index in range(5) if index not in triple
                    )
                    entry += (
                        b_variables[b_index]
                        * c_variables[c_index]
                        * quadratic[PAIRS.index(complement)]
                    )
            catalecticant[row, source_coordinate] = sp.expand(entry)

    factors: list[sp.Poly] = []
    factorizations = []
    edges: list[tuple[int, ...]] = []
    for rows, columns in SPLIT_MINORS:
        determinant = sp.expand(catalecticant.extract(rows, columns).det())
        _coefficient, raw_factors = sp.factor_list(determinant, *variables)
        assert len(raw_factors) == 3
        assert all(
            exponent == 1 and sp.Poly(factor, *variables).total_degree() == 2
            for factor, exponent in raw_factors
        )
        factor_ids = []
        for factor, _ in raw_factors:
            normalized = canonical_factor(factor, variables)
            if normalized not in factors:
                factors.append(normalized)
            factor_ids.append(factors.index(normalized))
        product = sp.prod(factors[index].as_expr() for index in factor_ids)
        constant = sp.cancel(determinant / product)
        assert constant.is_Rational
        assert sp.expand(determinant - constant * product) == 0
        edge = tuple(sorted(factor_ids))
        edges.append(edge)
        factorizations.append(
            {
                "rows": list(rows),
                "columns": list(columns),
                "constant": str(constant),
                "factor_ids": list(edge),
            }
        )

    assert len(factors) == 16
    assert len(set(edges)) == 22
    minimal_covers = minimal_hitting_sets(sorted(set(edges)), len(factors))
    cover_distribution = {
        size: sum(mask.bit_count() == size for mask in minimal_covers)
        for size in range(1, 17)
        if any(mask.bit_count() == size for mask in minimal_covers)
    }
    assert cover_distribution == {
        4: 1,
        5: 6,
        6: 13,
        7: 14,
        8: 16,
        9: 2,
        10: 1,
    }

    simple_expressions = (
        b_variables[3] * c_variables[4] + b_variables[4] * c_variables[3],
        b_variables[1] * c_variables[4] + b_variables[4] * c_variables[1],
        b_variables[1] * c_variables[2] + b_variables[2] * c_variables[1],
        b_variables[2] * c_variables[3] + b_variables[3] * c_variables[2],
    )
    simple_ids = {
        factors.index(canonical_factor(expression, variables))
        for expression in simple_expressions
    }
    four_covers = [mask for mask in minimal_covers if mask.bit_count() == 4]
    assert len(four_covers) == 1
    assert {index for index in range(16) if four_covers[0] & (1 << index)} == simple_ids

    output = {
        "verified": True,
        "field": "Q (the theorem is over C)",
        "exceptional_plane_ranks": [2, 2, 2],
        "balanced_relation_weights": list(relation_weights),
        "forbidden_span_rank": bad_rank,
        "total_quadratic_span_rank": total_rank,
        "marked_quotient_rank": total_rank - bad_rank,
        "H_dimension": len(h_basis),
        "L_dimension": len(l_basis),
        "L_decomposable_generators": ell_vectors,
        "marked_pairing_on_diagonal_duals": [
            [str(value) for value in row]
            for row in (
                pairing_matrix(good) * sp.Matrix.hstack(*diagonal_duals)
            ).tolist()
        ],
        "k_basis_bad_indices": list(K_BASIS_INDICES),
        "k_basis_rows": k_basis,
        "catalecticant_entry_degrees": [1, 1],
        "split_minor_count": len(factorizations),
        "bilinear_gate_count": len(factors),
        "bilinear_gate_expressions": [str(factor.as_expr()) for factor in factors],
        "bilinear_gate_matrices": [
            factor_matrix(factor, b_variables, c_variables) for factor in factors
        ],
        "split_minor_factorizations": factorizations,
        "minimal_cover_count": len(minimal_covers),
        "minimal_cover_size_distribution": {
            str(size): count for size, count in cover_distribution.items()
        },
        "minimal_covers": [
            [index for index in range(16) if mask & (1 << index)]
            for mask in minimal_covers
        ],
        "unique_four_gate_cover": sorted(simple_ids),
        "shared_full_mode_factorization_constructed": False,
        "rank_five_configuration_excluded": False,
        "p6_to_delta3_decided": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
    }
    output_path = (
        ROOT / "tmp" / "p6_common_port_111_rank_five_catalecticant_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
