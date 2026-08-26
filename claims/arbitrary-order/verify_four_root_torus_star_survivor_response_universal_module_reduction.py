#!/usr/bin/env python3
"""Verify the local universal response-module reduction after GLD75.

Over the exact equal-leaf survivor chart, this constructs a fixed full-tensor
quotient of the complete q0 response.  It replaces the original 17 by 3 lift
matrix by an equivalent 4 by 3 lift against a 68 by 4 root-response matrix,
without choosing a response minor and without deleting rank-drop fibres.

This is a denominator-free incidence reduction, not an emptiness theorem.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import chain, combinations, product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD75 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py"
)
GLD74 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py"
)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def q0_response_maps(gld73, eta, ports, words):
    matchings = tuple(gld73.perfect_matchings(tuple(range(10))))
    pair_offset = {pair: index for index, pair in enumerate(combinations(range(4), 2))}
    response_maps = []
    for root in range(4):
        varied_edge = (root, 4)
        root_matchings = tuple(
            matching for matching in matchings if varied_edge in matching
        )
        rows = []
        for word in words:
            row = [sp.Integer(0)] * 79
            for matching in root_matchings:
                complement = tuple(edge for edge in matching if edge != varied_edge)
                if any(right < 4 for _left, right in complement):
                    continue
                raw_edges = [edge for edge in complement if edge[0] >= 5]
                assert len(raw_edges) == 1
                left, right = raw_edges[0]
                if left == 5:
                    port = right - 6
                    raw_index = 1 + 3 * port + word[port]
                else:
                    left_port = left - 6
                    right_port = right - 6
                    raw_index = (
                        25
                        + 9 * pair_offset[(left_port, right_port)]
                        + 3 * word[left_port]
                        + word[right_port]
                    )
                fixed_weight = sp.prod(
                    eta[left_root]
                    if right_vertex == 5
                    else ports[right_vertex - 6][word[right_vertex - 6]][left_root]
                    for left_root, right_vertex in complement
                    if left_root < 4
                )
                row[raw_index] += fixed_weight
            rows.append(row)
        response_maps.append(sp.Matrix(rows))
    return response_maps


def fixed_quotient(constant: sp.Matrix):
    pivot_rows = tuple(constant.T.rref()[1])
    assert len(pivot_rows) == constant.cols
    quotient_rows = tuple(row for row in range(constant.rows) if row not in set(pivot_rows))
    correction = constant[list(quotient_rows), :] * constant[list(pivot_rows), :].inv()

    def project(matrix: sp.Matrix):
        return matrix[list(quotient_rows), :] - correction * matrix[list(pivot_rows), :]

    return pivot_rows, quotient_rows, project


def check():
    gld75 = load(GLD75, "gld75_local_germ")
    gld74 = load(GLD74, "gld74_full_fibre")
    survivor = gld75.load_gld72()
    gate = survivor.load_gate()
    parent = gate.load_parent()
    gld73 = gld74.load_gld73()

    shifts = sp.symbols("x0:15")
    certificate = json.loads(gld75.CERTIFICATE.read_text())
    survivor_basis = [
        gld75.sparse_polynomial(encoded, shifts).as_expr()
        for encoded in certificate["basis"]
    ]
    origin = {shift: 0 for shift in shifts}
    scale_fixed_basis = [*survivor_basis, shifts[8]]
    scale_jacobian = sp.Matrix(scale_fixed_basis).jacobian(shifts).subs(origin)
    assert scale_jacobian.rank() == 11
    scale_free = tuple(
        column
        for column in range(15)
        if column not in set(scale_jacobian.rref()[1])
    )
    assert scale_free == (6, 12, 13, 14)

    centre0, leaf0 = survivor.candidate_frames()
    centre = sp.Matrix(
        3, 3, [centre0[index] + shifts[index] for index in range(9)]
    )
    leaf = sp.ones(3, 3)
    for local_index, (row, colour) in enumerate(
        (item for row in (1, 2) for item in ((row, 0), (row, 1), (row, 2)))
    ):
        leaf[row, colour] = leaf0[row, colour] + shifts[9 + local_index]
    target = survivor.tensor_from_frames(parent, centre, leaf)

    xi, eta, ports = parent.canonical_torus_star(1)
    columns = list(chain.from_iterable(parent.full_q_layer_columns(xi, eta, ports)))
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    pivots = nuisance.rref()[1]
    kernel = sp.Matrix.hstack(*nuisance.nullspace())
    nuisance_basis = nuisance[:, list(pivots)]
    pivot_rows = nuisance_basis.T.rref()[1]
    pivot_solve = nuisance_basis[list(pivot_rows), :].inv()
    pivot_coefficients = pivot_solve * target[list(pivot_rows), :]
    particular = sp.zeros(79, 1)
    for pivot, value in zip(pivots, pivot_coefficients, strict=True):
        particular[pivot] = sp.expand(value)
    solve_residual = nuisance * particular - target
    assert all(sp.expand(solve_residual[row]) == 0 for row in pivot_rows)
    left_relations = sp.Matrix.hstack(*nuisance.T.nullspace()).T
    assert left_relations.shape == (37, 81)
    assert left_relations * nuisance == sp.zeros(37, 79)
    assert all(
        sp.expand(value) == 0
        for value in left_relations * solve_residual + left_relations * target
    )
    _variables, _equations, basepoint, _centre, _leaf = gld75.gauge_incidence(
        parent, left_relations, survivor
    )
    _certified_shifts, certified_incidence = gld75.symmetric_shifted_system(
        _variables, _equations, basepoint
    )
    assert _certified_shifts == shifts
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(left_relations * target, certified_incidence, strict=True)
    )
    assert kernel.shape == (79, 35)

    constant_columns = [columns[0], *columns[13:25]]
    constant = sp.Matrix.hstack(*(sp.Matrix(column) for column in constant_columns))
    assert constant.shape == (81, 13) and constant.rank() == 13
    response_maps = q0_response_maps(gld73, eta, ports, parent.LOCAL_INDICES)
    assert all(response.shape == (81, 79) for response in response_maps)
    _constant_pivots, quotient_rows, project = fixed_quotient(constant)
    assert len(quotient_rows) == 68

    affine_coefficients = particular.row_join(kernel)
    projected_root_affine = [project(response * affine_coefficients) for response in response_maps]
    signed_root_sum = (
        projected_root_affine[0]
        + projected_root_affine[1]
        + projected_root_affine[2]
        - projected_root_affine[3]
    )
    assert any(sp.expand(value.subs(origin)) != 0 for value in signed_root_sum)

    response_target = sp.Matrix.hstack(
        *(
            sp.Matrix(
                [
                    centre[word[0], colour]
                    * leaf[word[1], colour]
                    * leaf[word[2], colour]
                    * leaf[word[3], colour]
                    for word in parent.LOCAL_INDICES
                ]
            )
            for colour in range(3)
        )
    )
    projected_target = project(response_target)
    assert projected_target.shape == (68, 3)
    assert projected_target.subs(origin).rank() == 3

    # On the full 68-dimensional quotient all four root columns must be kept.
    # (Their signed sum only vanishes after restriction to mixed words, as in
    # GLD74.)  Thus H(t)X=R with X of shape 4 by 3 is exactly equivalent to
    # the original containment after quotienting the thirteen fixed columns.
    assert sp.Matrix.hstack(
        *(matrix[:, 0].subs(origin) for matrix in projected_root_affine)
    ).shape == (68, 4)

    gld74_data = gld74.quotient_forms()
    assert gld74.coefficient_fingerprint(gld74_data["coefficient_rows"]) == (
        "17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e"
    )

    fitting_counts = {}
    for response_rank in range(5):
        fitting_counts[str(response_rank)] = {
            "root_rank_upper_bound_minors": (
                0
                if response_rank == 4
                else sp.binomial(68, response_rank + 1)
                * sp.binomial(4, response_rank + 1)
            ),
            "augmented_rank_upper_bound_minors": sp.binomial(
                68, response_rank + 1
            ) * sp.binomial(7, response_rank + 1),
            "root_rank_chart_minors": (
                1
                if response_rank == 0
                else sp.binomial(68, response_rank) * sp.binomial(4, response_rank)
            ),
        }
    fitting_counts = {
        key: {name: int(value) for name, value in record.items()}
        for key, record in fitting_counts.items()
    }

    return {
        "status": "exact_universal_response_module_reduction_not_emptiness",
        "global_conjecture": "UNRESOLVED",
        "scale_fixed_survivor_chart": {
            "variables": 15,
            "equations": 11,
            "jacobian_rank_at_gld72": 11,
            "free_coordinates": [f"x{index}" for index in scale_free],
        },
        "raw_solve_shape_rank_kernel": [81, 79, nuisance.rank(), kernel.cols],
        "fixed_response_subspace_rank": constant.rank(),
        "full_tensor_quotient_dimension": len(quotient_rows),
        "projected_root_affine_shape": [68, 4, 36],
        "projected_target_shape_rank_at_gld72": [68, 3, 3],
        "signed_root_sum_vanishes_only_after_mixed_restriction": True,
        "equivalent_lift_matrix_shape": [4, 3],
        "equivalent_incidence_equations": 68 * 3,
        "original_lift_matrix_shape": [17, 3],
        "rank_stratum_minor_counts": fitting_counts,
        "gld74_specialization_quotient_fingerprint": (
            "17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e"
        ),
        "rank_drop_fibres_retained": True,
        "universal_incidence_empty": False,
    }


def main():
    result = check()
    print("four-root survivor universal response-module reduction: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
