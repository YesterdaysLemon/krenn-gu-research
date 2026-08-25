"""Verify the GLD72 Gaussian GHZ survivor in the fixed torus-star space."""

from __future__ import annotations

import importlib.util
import json
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / ("verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py")
)


def load_gate():
    spec = importlib.util.spec_from_file_location("gld71_gate", GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate_frames() -> tuple[sp.Matrix, sp.Matrix]:
    imaginary = sp.I
    centre = sp.Matrix(
        [
            [-2 - 2 * imaginary, -1 + 2 * imaginary, 3],
            [0, -3 + 3 * imaginary, 0],
            [0, -1 + 2 * imaginary, 1],
        ]
    )
    leaf = sp.Matrix(
        [
            [1, 1, 1],
            [0, 0, 1 + imaginary],
            [0, 1, 1],
        ]
    )
    return centre, leaf


def tensor_from_frames(parent, centre: sp.Matrix, leaf: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(
                sum(
                    centre[root, component]
                    * leaf[i, component]
                    * leaf[j, component]
                    * leaf[k, component]
                    for component in range(3)
                )
            )
            for root, i, j, k in parent.LOCAL_INDICES
        ]
    )


def flattening_rank(parent, tensor: sp.Matrix, left_modes: tuple[int, ...]) -> int:
    right_modes = tuple(mode for mode in range(4) if mode not in left_modes)
    rows = []
    for left_indices in product(range(3), repeat=len(left_modes)):
        row = []
        for right_indices in product(range(3), repeat=len(right_modes)):
            word = [0] * 4
            for mode, index in zip(left_modes, left_indices, strict=True):
                word[mode] = index
            for mode, index in zip(right_modes, right_indices, strict=True):
                word[mode] = index
            row.append(tensor[parent.LOCAL_INDEX[tuple(word)]])
        rows.append(row)
    return sp.Matrix(rows).rank()


def check_candidate() -> dict[str, object]:
    gate = load_gate()
    parent = gate.load_parent()
    relations = gate.full_relations(parent)
    centre, leaf = candidate_frames()
    tensor = tensor_from_frames(parent, centre, leaf)

    q_columns, residual_columns, pair_columns = parent.full_q_layer_columns(
        *parent.canonical_torus_star(1)
    )
    all_columns = q_columns + residual_columns + pair_columns
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in all_columns))
    pivot_basis = nuisance[:, list(parent.STAR_PIVOT_COLUMNS)]
    coefficients = pivot_basis.gauss_jordan_solve(tensor)[0]
    replay = pivot_basis * coefficients
    assert all(sp.simplify(value) == 0 for value in replay - tensor)
    assert nuisance.rank() == pivot_basis.rank() == 44
    assert nuisance.row_join(tensor).rank() == 44

    syndrome = gate.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    centre_vector = sp.Matrix(list(centre))
    assert syndrome.rank() == 7
    assert len(syndrome.nullspace()) == 2
    assert all(sp.simplify(value) == 0 for value in syndrome * centre_vector)

    centre_determinant = sp.factor(centre.det())
    leaf_determinant = sp.factor(leaf.det())
    assert centre_determinant == 12
    assert leaf_determinant == -1 - sp.I

    local_ranks = tuple(flattening_rank(parent, tensor, (mode,)) for mode in range(4))
    balanced_ranks = tuple(
        flattening_rank(parent, tensor, modes) for modes in ((0, 1), (0, 2), (0, 3))
    )
    assert local_ranks == (3, 3, 3, 3)
    assert balanced_ranks == (3, 3, 3)

    epsilon_direct = sp.factor(parent.epsilon(list(tensor)))
    epsilon_from_frames = sp.factor(6 * centre_determinant * leaf_determinant**3)
    expected_epsilon = 144 - 144 * sp.I
    assert sp.simplify(epsilon_direct - epsilon_from_frames) == 0
    assert sp.simplify(epsilon_direct - expected_epsilon) == 0

    support_size = sum(value != 0 for value in tensor)
    assert support_size == 61
    nonzero_coefficients = sum(value != 0 for value in coefficients)

    return {
        "status": "exact_fixed_star_route_refutation_not_global_resolution",
        "global_conjecture": "UNRESOLVED",
        "nuisance_rank": 44,
        "augmented_rank": 44,
        "syndrome_rank": 7,
        "syndrome_nullity": 2,
        "det_centre": str(centre_determinant),
        "det_leaf_frame": str(leaf_determinant),
        "local_ranks": local_ranks,
        "balanced_ranks": balanced_ranks,
        "epsilon": str(expected_epsilon),
        "tensor_support_size": support_size,
        "pivot_witness_nonzero_coefficients": nonzero_coefficients,
        "fixed_star_determinant_safe_statement": False,
        "graph_source_integrability_proved": False,
    }


def main() -> None:
    result = check_candidate()
    print("four-root torus-star Gaussian GHZ survivor: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
