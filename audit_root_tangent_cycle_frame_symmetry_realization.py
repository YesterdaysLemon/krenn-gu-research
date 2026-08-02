"""No-import rational audit of the root-tangent cycle frame realization."""

from __future__ import annotations

import json
from fractions import Fraction

Vector = tuple[Fraction, ...]
Matrix = tuple[Vector, ...]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(dot(row, vector) for row in matrix)


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))
    )


def add_matrices(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(lrow, rrow, strict=True))
        for lrow, rrow in zip(left, right, strict=True)
    )


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(a * b for b in right) for a in left)


def scale_add(
    scale_left: Fraction, left: Vector, scale_right: Fraction, right: Vector
) -> Vector:
    return tuple(
        scale_left * a + scale_right * b for a, b in zip(left, right, strict=True)
    )


def local_data(
    root: Vector, t_prev: Fraction, t_next: Fraction
) -> tuple[Matrix, Vector, Vector]:
    d0, d1, d2 = Fraction(2), Fraction(3), Fraction(5)
    target = (
        (d0 * d1 / root[0], -d0 * d1 / root[1], Fraction(0)),
        (d0 * d2 / root[0], Fraction(0), -d0 * d2 / root[2]),
    )
    denominator = t_next - t_prev
    assert denominator != 0
    previous = scale_add(t_next / denominator, target[0], -1 / denominator, target[1])
    following = scale_add(-t_prev / denominator, target[0], 1 / denominator, target[1])
    assert dot(previous, root) == 0
    assert dot(following, root) == 0
    reconstructed = (
        scale_add(Fraction(1), previous, Fraction(1), following),
        scale_add(t_prev, previous, t_next, following),
    )
    assert reconstructed == target
    return target, previous, following


def audit_cycle(length: int) -> dict[str, object]:
    roots: list[Vector] = [
        tuple(Fraction(value) for value in (i + 2, i + 3, i + 5)) for i in range(length)
    ]
    parameters = [Fraction(i) for i in range(length)]
    local = [
        local_data(roots[i], parameters[i - 1], parameters[i]) for i in range(length)
    ]
    blocks: list[Matrix] = []
    for i in range(length):
        j = (i + 1) % length
        left = local[i][2]
        right = local[j][1]
        u_left = (1 / roots[i][0], Fraction(0), Fraction(0))
        u_right = (1 / roots[j][0], Fraction(0), Fraction(0))
        block = add_matrices(outer(left, u_right), outer(u_left, right))
        assert mat_vec(block, roots[j]) == left
        assert mat_vec(transpose(block), roots[i]) == right
        assert dot(roots[i], mat_vec(block, roots[j])) == 0
        blocks.append(block)

    for i in range(length):
        assert mat_vec(transpose(blocks[i - 1]), roots[i - 1]) == local[i][1]
        assert mat_vec(blocks[i], roots[(i + 1) % length]) == local[i][2]

    return {
        "roots": length,
        "cycle_edges": length,
        "local_quotient_rank": 2,
        "edge_endpoint_constraints": 2 * length,
        "base_pairwise_zero_constraints": length,
    }


def main() -> None:
    result = {
        "status": "AUDIT_PASS",
        "method": "independent Fraction cycle and bilinear-block construction",
        "imports_project_code": False,
        "cycles": [audit_cycle(length) for length in range(3, 13)],
        "transpose_symmetry_obstructs_first_jet_frames": False,
        "complementary_hafnian_realizability_proved": False,
        "second_order_compatibility_proved": False,
        "finite_field_used": False,
        "global_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
