"""Verify the P7 2+2+1 jet-orthogonal fixed-window splice."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

from verify_p7_fixed_complement_laplace_fan_cover_and_lower_frame_separation import (
    RANK_TWO_PAIRS,
    ROOTS,
    UNMARKED,
    canonical_matrices,
    laplace_term,
    permanent_dp,
)
from verify_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model import (
    build_ledger,
    build_model,
    graph_tensor_for_subset,
)

AXIS_LABELS = (0, 0, 1, 1, 2)


def assembled_blocker_rows() -> dict[str, sp.Matrix]:
    h0, h1, h2 = canonical_matrices()
    raw: dict[str, list[list[sp.Expr]]] = {
        "t": [[h0[i, 0], h1[i, 0], h2[i, 0]] for i in ROOTS],
        "u01": [[h0[i, 1], h1[i, 3], 0] for i in ROOTS],
        "v01": [[h0[i, 2], h1[i, 4], 0] for i in ROOTS],
        "u02": [[h0[i, 3], 0, h2[i, 1]] for i in ROOTS],
        "v02": [[h0[i, 4], 0, h2[i, 2]] for i in ROOTS],
        "u12": [[0, h1[i, 1], h2[i, 3]] for i in ROOTS],
        "v12": [[0, h1[i, 2], h2[i, 4]] for i in ROOTS],
    }
    return {name: sp.Matrix(rows) for name, rows in raw.items()}


def check_jet_orthogonal_interface() -> None:
    frozen = sp.ones(3, 1)
    identity = sp.eye(3)
    blocker_rows = assembled_blocker_rows()
    for root, axis in enumerate(AXIS_LABELS):
        alpha = sp.zeros(3, 1)
        alpha[axis] = 1
        projection = identity - frozen * alpha.T
        assert (alpha.T * frozen)[0] == 1
        assert projection * frozen == sp.zeros(3, 1)
        assert alpha.T * projection == sp.zeros(1, 3)
        assert projection * projection == projection

        tangent_basis = [sp.eye(3)[:, coordinate] for coordinate in range(3) if coordinate != axis]
        for tangent in tangent_basis:
            assert projection * tangent == tangent
            assert (alpha.T * tangent)[0] == 0

        # E_(i,b)=alpha_i tensor r_(i,b): frozen evaluation recovers r,
        # while every tangent evaluation is zero.
        for rows in blocker_rows.values():
            blocker_covector = rows[root, :]
            edge_matrix = alpha * blocker_covector
            assert frozen.T * edge_matrix == blocker_covector
            for tangent in tangent_basis:
                assert tangent.T * edge_matrix == sp.zeros(1, 3)


def coefficient_rank(left: sp.Expr, right: sp.Expr, variables: tuple[sp.Symbol, ...]) -> int:
    left_poly = sp.Poly(left, *variables)
    right_poly = sp.Poly(right, *variables)
    monomials = sorted(set(left_poly.monoms()) | set(right_poly.monoms()))
    matrix = sp.Matrix(
        [
            [left_poly.coeff_monomial(monomial) for monomial in monomials],
            [right_poly.coeff_monomial(monomial) for monomial in monomials],
        ]
    )
    return matrix.rank()


def check_common_mixed_jet_sector() -> tuple[dict[tuple[int, int], sp.Expr], dict[tuple[int, int], sp.Expr]]:
    local, p, q, root_blocks, residual_blocks, blocks = build_model()
    ledger = build_ledger()

    # The local coordinate restrictions have exactly the same axis pattern
    # as the frozen pure sector.
    for root, axis in enumerate(AXIS_LABELS):
        assert local[root][axis] == 0
        assert all(local[root][colour] != 0 for colour in range(3) if colour != axis)

    variables = tuple(
        sorted(
            set().union(
                *(expression.free_symbols for expression in root_blocks.values()),
                *(expression.free_symbols for expression in residual_blocks.values()),
            ),
            key=str,
        )
    )
    for pair in combinations(ROOTS, 2):
        assert coefficient_rank(root_blocks[pair], residual_blocks[pair], variables) == 2
        assert residual_blocks[pair] == sp.expand(
            p[pair[0]] * q[pair[1]] + q[pair[0]] * p[pair[1]]
        )

    checked = 0
    for size in range(1, 6):
        for root_subset in combinations(ROOTS, size):
            graph_value = graph_tensor_for_subset(root_subset, blocks, ledger)
            target = sp.Matrix(
                [
                    sp.prod(local[root][colour] for root in root_subset)
                    for colour in range(3)
                ]
            )
            assert all(sp.expand(entry) == 0 for entry in graph_value - target)
            checked += 1
    assert checked == 31
    assert len(ledger) == 62
    return root_blocks, residual_blocks


def check_fixed_window_separation_and_selector_readiness(
    root_blocks: dict[tuple[int, int], sp.Expr],
    residual_blocks: dict[tuple[int, int], sp.Expr],
) -> None:
    variables = tuple(
        sorted(
            set().union(
                *(expression.free_symbols for expression in root_blocks.values()),
                *(expression.free_symbols for expression in residual_blocks.values()),
            ),
            key=str,
        )
    )
    assert {
        pair
        for pair in combinations(ROOTS, 2)
        if 3 - len({AXIS_LABELS[root] for root in pair}) == 2
    } == RANK_TWO_PAIRS

    colour_tagged_windows = 0
    for matrix in canonical_matrices():
        assert permanent_dp(matrix) == -1
        for retained in combinations(UNMARKED, 2):
            terms = {
                pair: laplace_term(matrix, pair, retained)
                for pair in combinations(ROOTS, 2)
            }
            assert sum(terms.values(), sp.Integer(0)) == -1
            assert all(terms[pair] == 0 for pair in RANK_TWO_PAIRS)
            active_pairs = [pair for pair, value in terms.items() if value != 0]
            assert active_pairs
            assert all(pair not in RANK_TWO_PAIRS for pair in active_pairs)
            assert all(
                coefficient_rank(root_blocks[pair], residual_blocks[pair], variables) == 2
                for pair in active_pairs
            )
            colour_tagged_windows += 1
    assert colour_tagged_windows == 18


def check_displayed_companion_minors() -> None:
    _, _, _, root_blocks, residual_blocks, _ = build_model()
    all_variables = tuple(
        sorted(
            set().union(
                *(expression.free_symbols for expression in root_blocks.values()),
                *(expression.free_symbols for expression in residual_blocks.values()),
            ),
            key=str,
        )
    )
    names = {str(symbol): symbol for symbol in all_variables}
    certificates = {
        (0, 1): (("y1", "y2"), ("x1", "x2"), 1),
        (0, 2): (("y1", "y3"), ("x1", "y3"), 1),
        (0, 3): (("y1", "y4"), ("u4", "x1"), 1),
        (0, 4): (("x1", "x5"), ("u5", "y1"), 1),
        (1, 2): (("y2", "y3"), ("u3", "x2"), 1),
        (1, 3): (("y2", "y4"), ("x2", "y4"), 1),
        (1, 4): (("x5", "y2"), ("x2", "x5"), -1),
        (2, 3): (("y3", "y4"), ("u3", "u4"), 1),
        (2, 4): (("u5", "y3"), ("u3", "u5"), -1),
        (3, 4): (("x5", "y4"), ("u4", "u5"), -1),
    }
    for pair, (left_names, right_names, expected) in certificates.items():
        left_monomial = sp.prod(names[name] for name in left_names)
        right_monomial = sp.prod(names[name] for name in right_names)
        matrix = sp.Matrix(
            [
                [
                    sp.Poly(expression, *all_variables).coeff_monomial(monomial)
                    for monomial in (left_monomial, right_monomial)
                ]
                for expression in (root_blocks[pair], residual_blocks[pair])
            ]
        )
        assert matrix.det() == expected


def main() -> None:
    check_jet_orthogonal_interface()
    root_blocks, residual_blocks = check_common_mixed_jet_sector()
    check_fixed_window_separation_and_selector_readiness(root_blocks, residual_blocks)
    check_displayed_companion_minors()
    print("PASS: exact jet-orthogonal frozen/tangent splice")
    print("PASS: all 31 common mixed lower-root equations")
    print("PASS: all 18 fixed windows retain zero rho>=2 shore incidence")
    print("PASS: distinguished companion forms independent at every root pair")
    print("SCOPE: common tensor hafnian ledger and marked-star fan remain UNRESOLVED")


if __name__ == "__main__":
    main()
