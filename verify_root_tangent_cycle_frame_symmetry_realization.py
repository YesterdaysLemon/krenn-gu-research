"""Verify simultaneous root-tangent quotient frames on a symmetric cycle."""

from __future__ import annotations

import json

import sympy as sp


def generic_frame_identity() -> dict[str, object]:
    x0, x1, x2 = sp.symbols("x0 x1 x2", nonzero=True)
    d0, d1, d2 = sp.symbols("d0 d1 d2", nonzero=True)
    t_prev, t_next = sp.symbols("t_prev t_next")
    root = sp.Matrix((x0, x1, x2))
    quotient = sp.Matrix(((d1, -d0, 0), (d2, 0, -d0)))
    diagonal = sp.Matrix((d0, d1, d2))
    derivative = sp.diag(d0 / x0, d1 / x1, d2 / x2)
    target = quotient * derivative
    edge_classes = sp.Matrix(((1, 1), (t_prev, t_next)))
    coefficient_covectors = sp.simplify(edge_classes.inv() * target)
    assert quotient * diagonal == sp.zeros(2, 1)
    assert target * root == sp.zeros(2, 1)
    assert sp.simplify(edge_classes * coefficient_covectors - target) == sp.zeros(2, 3)
    assert sp.simplify(coefficient_covectors * root) == sp.zeros(2, 1)
    assert sp.factor(edge_classes.det()) == t_next - t_prev
    witness_minor = sp.factor(coefficient_covectors[:, :2].det())
    assert witness_minor != 0
    return {
        "edge_class_determinant": str(sp.factor(edge_classes.det())),
        "coefficient_annihilator": [
            str(sp.factor(v)) for v in coefficient_covectors * root
        ],
        "coefficient_rank_witness": str(witness_minor),
        "target_rank": target.rank(),
    }


def exact_cycle(length: int) -> dict[str, object]:
    weights = sp.Matrix((2, 3, 5))
    quotient = sp.Matrix(((weights[1], -weights[0], 0), (weights[2], 0, -weights[0])))
    roots = [sp.Matrix((i + 2, i + 3, i + 5)) for i in range(length)]
    edge_classes = [sp.Matrix((1, i)) for i in range(length)]
    local_covectors: list[tuple[sp.Matrix, sp.Matrix]] = []
    targets: list[sp.Matrix] = []
    for i, root in enumerate(roots):
        derivative = sp.diag(*(weights[c] / root[c] for c in range(3)))
        target = quotient * derivative
        basis = edge_classes[i - 1].row_join(edge_classes[i])
        coefficient_covectors = basis.inv() * target
        assert coefficient_covectors * root == sp.zeros(2, 1)
        assert basis * coefficient_covectors == target
        assert coefficient_covectors.rank() == 2
        local_covectors.append(
            (coefficient_covectors[0, :].T, coefficient_covectors[1, :].T)
        )
        targets.append(target)

    edge_blocks: list[sp.Matrix] = []
    for i in range(length):
        j = (i + 1) % length
        left = local_covectors[i][1]
        right = local_covectors[j][0]
        u_left = sp.Matrix((1 / roots[i][0], 0, 0))
        u_right = sp.Matrix((1 / roots[j][0], 0, 0))
        block = left * u_right.T + u_left * right.T
        assert block * roots[j] == left
        assert block.T * roots[i] == right
        assert (roots[i].T * block * roots[j])[0] == 0
        edge_blocks.append(block)

    for i in range(length):
        reconstructed = (
            edge_classes[i - 1] * local_covectors[i][0].T
            + edge_classes[i] * local_covectors[i][1].T
        )
        assert reconstructed == targets[i]
        previous_block = edge_blocks[i - 1]
        next_block = edge_blocks[i]
        assert previous_block.T * roots[i - 1] == local_covectors[i][0]
        assert next_block * roots[(i + 1) % length] == local_covectors[i][1]

    return {
        "roots": length,
        "edges": length,
        "shared_classes": length,
        "all_local_frame_ranks": [target.rank() for target in targets],
        "all_base_edge_evaluations_zero": True,
    }


def main() -> None:
    result = {
        "status": "VERIFIED",
        "field": "Q and symbolic characteristic zero",
        "generic_frame": generic_frame_identity(),
        "exact_cycles": [exact_cycle(length) for length in range(3, 10)],
        "shared_cofactor_class_at_both_edge_endpoints": True,
        "reverse_edge_block_is_transpose": True,
        "complementary_hafnian_realizability_proved": False,
        "second_order_compatibility_proved": False,
        "finite_field_used": False,
        "global_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
