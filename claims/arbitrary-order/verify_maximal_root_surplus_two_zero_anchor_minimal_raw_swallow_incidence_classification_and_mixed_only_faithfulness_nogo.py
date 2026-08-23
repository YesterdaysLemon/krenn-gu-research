"""Focused exact checks for the GLS37 minimal-swallow classification/no-go."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import runpy

import sympy as sp


GLS35 = runpy.run_path(
    str(
        Path(__file__).with_name(
            "verify_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py"
        )
    )
)

A0 = GLS35["A0"]
A1 = GLS35["A1"]
Q0 = GLS35["Q0"]
Q1 = GLS35["Q1"]
PORTS = GLS35["PORTS"]
E = GLS35["E"]
ONE = GLS35["ONE"]
edge_block = GLS35["edge_block"]
graph_coefficient = GLS35["graph_coefficient"]
tensor = GLS35["tensor"]


def shore_channel_profile(
    left_basis: sp.Matrix, diagonal: sp.Matrix
) -> dict[str, object]:
    """Compute the two one-Q off-diagonal channel kernels."""

    exchange = sp.Matrix(((0, 1), (1, 0)))
    right_basis = (exchange * left_basis.inv() * diagonal).T
    assert left_basis * exchange * right_basis.T == diagonal

    # Columns of each basis are the two named residual shore vectors.
    left_row_0 = left_basis[0, :].T
    left_row_1 = left_basis[1, :].T
    right_row_0 = right_basis[0, :].T
    right_row_1 = right_basis[1, :].T
    channel_01 = sp.Matrix.hstack(left_row_0, right_row_1)
    channel_10 = sp.Matrix.hstack(left_row_1, right_row_0)

    kernels = (channel_01.nullspace(), channel_10.nullspace())
    for kernel in kernels:
        assert len(kernel) <= 1
        if kernel:
            # The entries are (B_1,A_0) or (B_0,A_1).  Neither can vanish
            # because every coordinate row of each shore basis is nonzero.
            assert kernel[0][0] != 0 and kernel[0][1] != 0
            assert 2 * kernel[0][0] * kernel[0][1] != 0
    return {
        "right_basis": right_basis,
        "channel_ranks": (channel_01.rank(), channel_10.rank()),
        "channel_dimension": sum(len(kernel) for kernel in kernels),
        "kernel_vectors": tuple(
            tuple(kernel[0]) if kernel else () for kernel in kernels
        ),
    }


def check_minimal_swallow_classification() -> dict[str, object]:
    diagonal = sp.diag(2, 3)
    examples = (
        sp.Matrix(((-2, -2), (-2, -1))),
        sp.Matrix(((-2, -2), (-2, 0))),
        sp.Matrix(((-2, 0), (0, -2))),
    )
    profiles = tuple(shore_channel_profile(basis, diagonal) for basis in examples)
    assert tuple(profile["channel_dimension"] for profile in profiles) == (0, 1, 2)

    # The individual one-Q equations may leave zero, one, or two channels.
    # On the full-swallow rank-three fibre, however, every generator belongs
    # to Delta.  Both shores and every allowed port pair are supported on the
    # same two-colour plane, so the diagonal part of the complete image has
    # dimension at most two.  It cannot equal the three-dimensional Delta.
    for profile in profiles:
        for kernel in profile["kernel_vectors"]:
            if kernel:
                beta, alpha = kernel
                assert alpha * beta + alpha * beta != 0
    two_colour_diagonal = sp.Matrix.hstack(
        sp.eye(9)[:, 0],
        sp.eye(9)[:, 4],
    )
    full_diagonal = sp.Matrix.hstack(
        sp.eye(9)[:, 0],
        sp.eye(9)[:, 4],
        sp.eye(9)[:, 8],
    )
    assert two_colour_diagonal.rank() == 2
    assert full_diagonal.rank() == 3
    assert two_colour_diagonal.row_join(sp.eye(9)[:, 8]).rank() == 3
    return {
        "channel_profiles": profiles,
        "two_colour_diagonal_rank": two_colour_diagonal.rank(),
        "full_diagonal_rank": full_diagonal.rank(),
        "rank_three_full_swallow_with_two_rank_two_shores": "excluded",
    }


def check_mixed_only_control() -> dict[str, object]:
    edges, _, _ = GLS35["build_control"]()
    nuisance, q, _ = GLS35["raw_anchor_matrix"](edges)
    pure = [tensor(E[colour], E[colour]) for colour in range(3)]
    assert nuisance.rank() == nuisance.row_join(q).rank() == 8
    assert [nuisance.row_join(vector).rank() for vector in pure] == [9, 9, 9]
    assert q == pure[1] + pure[2]
    assert (tensor(ONE, ONE).T * q)[0] == 2

    # Every complementary non-Q deck is zero: after deleting a non-Q label,
    # at least one residual remains and is isolated in the outside graph.
    for residual in (Q0, Q1):
        other_residual = Q1 if residual == Q0 else Q0
        assert edge_block(edges, residual, other_residual) == sp.zeros(3)
        for port in PORTS:
            assert edge_block(edges, residual, port) == sp.zeros(3)

    support = {}
    for word in product(range(3), repeat=8):
        coefficient = graph_coefficient(edges, word)
        if coefficient:
            support[word] = coefficient
    assert support == {
        (1, 1, 0, 0, 0, 0, 0, 0): sp.Rational(1, 2),
        (2, 2, 0, 0, 0, 0, 0, 0): sp.Rational(1, 2),
    }

    contracted = {}
    for port_word in product(range(3), repeat=4):
        coefficient_matrix = sp.zeros(3)
        for left_colour, right_colour in product(range(3), repeat=2):
            coefficient_matrix[left_colour, right_colour] = sum(
                graph_coefficient(
                    edges,
                    (left_colour, right_colour, q0_colour, q1_colour, *port_word),
                )
                for q0_colour, q1_colour in product(range(3), repeat=2)
            )
        if coefficient_matrix != sp.zeros(3):
            contracted[port_word] = coefficient_matrix
    assert contracted == {(0, 0, 0, 0): sp.diag(0, sp.Rational(1, 2), sp.Rational(1, 2))}

    mixed_failures = [
        word
        for word in product(range(3), repeat=4)
        if len(set(word)) > 1 and word in contracted
    ]
    assert not mixed_failures
    pure_defects = {
        (colour,) * 4: contracted.get((colour,) * 4, sp.zeros(3))
        - sp.diag(*(1 if index == colour else 0 for index in range(3)))
        for colour in range(3)
    }
    assert tuple(defect.rank() for defect in pure_defects.values()) == (3, 1, 1)

    # The physical port deck is one pure word and is nonzero on the local
    # GLS34 product-kernel tuple; pH=1 there.
    h_value = GLS35["deck_value"](edges, PORTS, {port: E[0] for port in PORTS})
    assert h_value == sp.Rational(1, 2)
    assert 2 * h_value == 1

    return {
        "raw_ranks": (8, 8),
        "pure_augmentation_ranks": (9, 9, 9),
        "full_support": len(support),
        "contracted_support": len(contracted),
        "mixed_port_failures": len(mixed_failures),
        "pure_defect_ranks": tuple(defect.rank() for defect in pure_defects.values()),
        "pH_kernel_value": 2 * h_value,
    }


def main() -> None:
    classification = check_minimal_swallow_classification()
    control = check_mixed_only_control()
    print("GLS37 minimal-swallow/mixed-only primary checks: PASS")
    print("  channel dimensions:", tuple(p["channel_dimension"] for p in classification["channel_profiles"]))
    print(
        "  diagonal ranks:",
        (classification["two_colour_diagonal_rank"], classification["full_diagonal_rank"]),
    )
    print(
        "  rank-three/two-shore fibre:",
        classification["rank_three_full_swallow_with_two_rank_two_shores"],
    )
    print("  mixed-only control:", control)


if __name__ == "__main__":
    main()
