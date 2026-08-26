#!/usr/bin/env python3
"""Explore the exact leaf-S3 representation behind GLD74.

This is a bounded parent-proposition experiment.  It reconstructs the fixed
GLD70 nuisance map in canonical coordinates, proves equivariance of its raw
79-coordinate presentation under permutation of the three equal leaf ports,
and decomposes the raw space, nuisance image, raw kernel, and GLD74 mixed
quotient into rational S3 isotypic pieces.

The script does not claim a response exclusion away from the GLD72 point.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import chain, combinations, permutations, product
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


def load_gld75():
    spec = importlib.util.spec_from_file_location("gld75_local_germ", GLD75)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_gld74():
    spec = importlib.util.spec_from_file_location("gld74_full_fibre", GLD74)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def raw_descriptors():
    descriptors = [("q",)]
    descriptors.extend(
        ("residual", residual, mode, colour)
        for residual in range(2)
        for mode in range(4)
        for colour in range(3)
    )
    descriptors.extend(
        ("pair", modes, colours)
        for modes in combinations(range(4), 2)
        for colours in product(range(3), repeat=2)
    )
    assert len(descriptors) == 79
    return tuple(descriptors)


def permute_raw_descriptor(descriptor, mode_permutation):
    if descriptor[0] == "q":
        return descriptor
    if descriptor[0] == "residual":
        _tag, residual, mode, colour = descriptor
        return ("residual", residual, mode_permutation[mode], colour)
    _tag, modes, colours = descriptor
    transported = sorted(
        zip(
            (mode_permutation[modes[0]], mode_permutation[modes[1]]),
            colours,
            strict=True,
        )
    )
    return (
        "pair",
        tuple(mode for mode, _colour in transported),
        tuple(colour for _mode, colour in transported),
    )


def permutation_matrix(descriptors, mode_permutation):
    index = {descriptor: position for position, descriptor in enumerate(descriptors)}
    matrix = sp.zeros(len(descriptors), len(descriptors))
    for source, descriptor in enumerate(descriptors):
        target_descriptor = permute_raw_descriptor(descriptor, mode_permutation)
        matrix[index[target_descriptor], source] = 1
    assert matrix.T * matrix == sp.eye(len(descriptors))
    # ``permute_tensor_modes`` evaluates the source tensor at inverse-permuted
    # output indices, so coefficient coordinates carry the contragredient
    # permutation in this column convention.
    return matrix.T


def representation_coordinates(basis: sp.Matrix, transported: sp.Matrix) -> sp.Matrix:
    pivots = basis.T.rref()[1]
    assert len(pivots) == basis.cols
    square = basis[list(pivots), :]
    coordinates = square.inv() * transported[list(pivots), :]
    assert basis * coordinates == transported
    return coordinates


def character_decomposition(identity: int, transposition: int, three_cycle: int):
    trivial = (identity + 3 * transposition + 2 * three_cycle) // 6
    sign = (identity - 3 * transposition + 2 * three_cycle) // 6
    standard = (2 * identity - 2 * three_cycle) // 6
    assert trivial + sign + 2 * standard == identity
    return {
        "character": [identity, transposition, three_cycle],
        "multiplicities_trivial_sign_standard": [trivial, sign, standard],
        "isotypic_dimensions_trivial_sign_standard": [trivial, sign, 2 * standard],
    }


def full_q0_response_maps(gld73, eta, ports, words):
    """Build the complete 81-coordinate q0 root-response maps.

    The mixed restriction is useful for the GLD74 quotient, but GLD76's
    universal module is formed before that restriction.  Keep this
    reconstruction local so the covariance assertion below covers the same
    full response maps used by the universal-module verifier.
    """

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


def check():
    gld75 = load_gld75()
    gld74 = load_gld74()
    survivor = gld75.load_gld72()
    gate = survivor.load_gate()
    parent = gate.load_parent()
    xi, eta, ports = parent.canonical_torus_star(1)
    layers = parent.full_q_layer_columns(xi, eta, ports)
    columns = list(chain.from_iterable(layers))
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    assert nuisance.shape == (81, 79) and nuisance.rank() == 44

    descriptors = raw_descriptors()
    kernel = sp.Matrix.hstack(*nuisance.nullspace())
    image_pivots = nuisance.rref()[1]
    image_basis = nuisance[:, list(image_pivots)]
    assert kernel.shape == (79, 35) and image_basis.shape == (81, 44)
    gld73 = gld74.load_gld73()
    mixed_rows = tuple(
        row for row, word in enumerate(parent.LOCAL_INDICES) if len(set(word)) != 1
    )
    response_maps = gld74.q0_response_context(gld73, eta, ports)
    complete_response_maps = full_q0_response_maps(
        gld73, eta, ports, parent.LOCAL_INDICES
    )
    constant = sp.Matrix.hstack(
        *(sp.Matrix(column) for column in [columns[0], *columns[13:25]])
    )
    assert constant.shape == (81, 13) and constant.rank() == 13
    constant_mixed = sp.Matrix(
        [[column[row] for column in [columns[0], *columns[13:25]]] for row in mixed_rows]
    )
    assert constant_mixed.shape == (78, 13) and constant_mixed.rank() == 13

    class_data = {}
    raw_characters = {}
    kernel_characters = {}
    image_characters = {}
    for leaf_sigma in permutations((1, 2, 3)):
        mode_permutation = (0, *leaf_sigma)
        raw_action = permutation_matrix(descriptors, mode_permutation)
        tensor_action = sp.Matrix.hstack(
            *(
                gld75.permute_tensor_modes(
                    parent, sp.eye(81)[:, column], mode_permutation
                )
                for column in range(81)
            )
        )
        assert nuisance * raw_action == tensor_action * nuisance

        mixed_action = tensor_action[list(mixed_rows), list(mixed_rows)]
        assert all(
            complete_response * raw_action == tensor_action * complete_response
            for complete_response in complete_response_maps
        )
        assert constant.row_join(tensor_action * constant).rank() == 13
        assert all(
            response_map * raw_action == mixed_action * response_map
            for response_map in response_maps
        )
        assert constant_mixed.row_join(mixed_action * constant_mixed).rank() == 13

        kernel_action = representation_coordinates(kernel, raw_action * kernel)
        image_action = representation_coordinates(
            image_basis, tensor_action * image_basis
        )
        assert sp.trace(raw_action) == sp.trace(kernel_action) + sp.trace(image_action)

        fixed_leaf_modes = sum(
            int(mode_permutation[mode] == mode) for mode in (1, 2, 3)
        )
        if fixed_leaf_modes == 3:
            conjugacy_class = "identity"
        elif fixed_leaf_modes == 1:
            conjugacy_class = "transposition"
        else:
            conjugacy_class = "three_cycle"
        values = (
            int(sp.trace(raw_action)),
            int(sp.trace(image_action)),
            int(sp.trace(kernel_action)),
        )
        if conjugacy_class in class_data:
            assert class_data[conjugacy_class] == values
        class_data[conjugacy_class] = values
        raw_characters[conjugacy_class] = values[0]
        image_characters[conjugacy_class] = values[1]
        kernel_characters[conjugacy_class] = values[2]

    order = ("identity", "transposition", "three_cycle")
    raw_decomposition = character_decomposition(*(raw_characters[key] for key in order))
    image_decomposition = character_decomposition(
        *(image_characters[key] for key in order)
    )
    kernel_decomposition = character_decomposition(
        *(kernel_characters[key] for key in order)
    )

    # In the mixed 78-coordinate space, a transposition fixes 24 words and a
    # three-cycle fixes 6.  The constant q0 response subspace is Q plus the
    # twelve eta-residual columns; its characters are 13, 7, 4.
    mixed_character = (78, 24, 6)
    constant_character = (13, 7, 4)
    quotient_character = tuple(
        mixed - constant
        for mixed, constant in zip(mixed_character, constant_character, strict=True)
    )
    quotient_decomposition = character_decomposition(*quotient_character)

    centre, leaf = survivor.candidate_frames()
    tensor = survivor.tensor_from_frames(parent, centre, leaf)
    particular = image_basis.gauss_jordan_solve(tensor)[0]
    raw_particular = sp.zeros(79, 1)
    for pivot, value in zip(image_pivots, particular, strict=True):
        raw_particular[pivot] = value
    averaged = sp.zeros(79, 1)
    for leaf_sigma in permutations((1, 2, 3)):
        averaged += permutation_matrix(descriptors, (0, *leaf_sigma)) * raw_particular
    averaged /= 6
    assert nuisance * averaged == tensor
    assert all(
        permutation_matrix(descriptors, (0, *leaf_sigma)) * averaged == averaged
        for leaf_sigma in permutations((1, 2, 3))
    )

    return {
        "status": "exact_representation_reduction_not_response_exclusion",
        "global_conjecture": "UNRESOLVED",
        "nuisance_shape_rank": [81, 79, nuisance.rank()],
        "raw_space": raw_decomposition,
        "nuisance_image": image_decomposition,
        "raw_kernel": kernel_decomposition,
        "mixed_space_character": list(mixed_character),
        "constant_response_character": list(constant_character),
        "gld74_quotient": quotient_decomposition,
        "complete_q0_response_covariance_verified": True,
        "complete_q0_response_shape": [81, 79],
        "complete_q0_fixed_block_covariance_verified": True,
        "s3_invariant_raw_preimage_exists": True,
        "s3_invariant_raw_fibre_dimension": kernel_decomposition[
            "multiplicities_trivial_sign_standard"
        ][0],
        "whole_survivor_locus_response_excluded": False,
    }


def main():
    result = check()
    print("four-root survivor response S3 representation: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
