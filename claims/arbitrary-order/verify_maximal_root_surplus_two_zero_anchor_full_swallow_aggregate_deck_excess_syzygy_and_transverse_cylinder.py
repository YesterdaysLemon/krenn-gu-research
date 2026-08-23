"""Focused exact checks for the GLS40 aggregate-deck/cylinder theorem."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def basis_vector(index: int, size: int = 3) -> sp.Matrix:
    return sp.eye(size)[:, index]


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def pair_columns(
    x_left: sp.Matrix,
    y_left: sp.Matrix,
    x_right: sp.Matrix,
    y_right: sp.Matrix,
) -> sp.Matrix:
    columns = []
    for left_index in range(x_left.cols):
        for right_index in range(x_right.cols):
            columns.append(
                tensor(x_left[:, left_index], y_right[:, right_index])
                + tensor(x_right[:, right_index], y_left[:, left_index])
            )
    return sp.Matrix.hstack(*columns)


def aggregate_rank_checks() -> dict[str, tuple[int, ...]]:
    ell = sp.eye(5)[:3, :]
    h_pure = sp.Matrix([[1, 1, 1, 0, 0]])
    h_mixed = sp.Matrix([[0, 0, 0, 1, 0]])

    outside_pure = sp.Matrix.vstack(ell, -h_pure)
    outside_mixed = sp.Matrix.vstack(ell, -h_mixed)
    assert outside_pure.rank() == 3
    assert outside_mixed.rank() == 4

    beta = sp.Matrix([1, -2, 3])
    diagonal = sp.eye(3)
    inside_rank_two = diagonal - beta * sp.Matrix([[1, 0, 0]])
    inside_rank_three = sp.Matrix.hstack(diagonal, sp.zeros(3, 2)) - beta * h_mixed
    assert inside_rank_two.rank() == 2
    assert inside_rank_three.rank() == 3
    return {
        "q_outside_delta": (outside_pure.rank(), outside_mixed.rank()),
        "q_inside_delta": (inside_rank_two.rank(), inside_rank_three.rank()),
    }


def canonical_rank_strata_checks() -> dict[str, tuple[int, ...]]:
    e = [basis_vector(index, 9) for index in range(9)]
    diagonal = [e[index] for index in (0, 4, 8)]
    q_outside = e[1] + e[3]
    q_inside = e[0]
    off_extensions = [e[index] for index in (2, 5, 6, 7, 1, 3)]
    epsilon = sp.ones(1, 9)

    outside_excess = []
    outside_cylinders = []
    inside_excess = []
    inside_cylinders = []
    for rank_b in range(4, 10):
        outside_basis = diagonal + [q_outside] + off_extensions[: rank_b - 4]
        outside_b = sp.Matrix.hstack(*outside_basis)
        assert outside_b.rank() == rank_b
        p_outside = 2 * sp.eye(9) - q_outside * epsilon
        outside_c = p_outside * outside_b
        assert outside_c.rank() == rank_b - 1
        assert (p_outside * sp.Matrix.hstack(*diagonal)).rank() == 3
        outside_excess.append(rank_b - 4)
        outside_cylinders.append(9 * outside_c.rank())

        inside_basis = diagonal + off_extensions[: rank_b - 3]
        inside_b = sp.Matrix.hstack(*inside_basis)
        assert inside_b.rank() == rank_b
        p_inside = sp.eye(9) - q_inside * epsilon
        inside_c = p_inside * inside_b
        assert inside_c.rank() == rank_b - 1
        assert (p_inside * sp.Matrix.hstack(*diagonal)).rank() == 2
        inside_excess.append(rank_b - 3)
        inside_cylinders.append(9 * inside_c.rank())

    assert tuple(outside_cylinders) == (27, 36, 45, 54, 63, 72)
    assert tuple(inside_cylinders) == (27, 36, 45, 54, 63, 72)
    return {
        "q_outside_excess": tuple(outside_excess),
        "q_inside_excess": tuple(inside_excess),
        "cylinder_dimensions": tuple(outside_cylinders),
    }


def rank_six_interface_control() -> dict[str, int]:
    e = [basis_vector(index) for index in range(3)]
    residual = {
        "q0": (e[0], e[0]),
        "q1": (e[1], e[1]),
    }
    port_colours = {"u0": 0, "u1": 1, "u2": 2, "u3": 2}
    labels: dict[str, tuple[sp.Matrix, sp.Matrix]] = {}
    for label, (x_vector, y_vector) in residual.items():
        labels[label] = (x_vector, y_vector)
    for label, colour in port_colours.items():
        coordinate_map = e[colour] * e[colour].T
        labels[label] = (coordinate_map, coordinate_map)

    order = tuple(labels)
    sigma_blocks = []
    for left, right in combinations(order, 2):
        if (left, right) == ("q0", "q1"):
            continue
        x_left, y_left = labels[left]
        x_right, y_right = labels[right]
        sigma_blocks.append(pair_columns(x_left, y_left, x_right, y_right))
    sigma = sp.Matrix.hstack(*sigma_blocks)

    q = tensor(e[0], e[1]) + tensor(e[1], e[0])
    diagonal = [tensor(vector, vector) for vector in e]
    full_swallow = sigma.row_join(sp.Matrix.hstack(q, *diagonal))
    assert sigma.rank() == 6
    assert full_swallow.rank() == 6
    assert sp.Matrix.hstack(*diagonal, q).rank() == 4

    target_columns = []
    aggregate_columns = []
    word_checks = 0
    for word in product(range(3), repeat=4):
        h_value = int(word == (0, 1, 0, 0))
        aggregate = sp.zeros(9, 1)

        if word[2:] == (0, 0):
            aggregate -= pair_columns(
                labels["u0"][0],
                labels["u0"][1],
                labels["u1"][0],
                labels["u1"][1],
            )[:, 3 * word[0] + word[1]]
        if word[1:] == (0, 0, 0):
            one_residual = pair_columns(
                labels["q0"][0],
                labels["q0"][1],
                labels["u0"][0],
                labels["u0"][1],
            )
            aggregate += sp.Rational(1, 2) * one_residual[:, word[0]]
        if (word[0], word[2], word[3]) == (1, 1, 1):
            one_residual = pair_columns(
                labels["q1"][0],
                labels["q1"][1],
                labels["u1"][0],
                labels["u1"][1],
            )
            aggregate += sp.Rational(1, 2) * one_residual[:, word[1]]
        if word[:2] == (2, 2):
            pair = pair_columns(
                labels["u2"][0],
                labels["u2"][1],
                labels["u3"][0],
                labels["u3"][1],
            )
            aggregate += sp.Rational(1, 2) * pair[:, 3 * word[2] + word[3]]

        target = sp.zeros(9, 1)
        if len(set(word)) == 1:
            target = diagonal[word[0]]
        assert q * h_value + aggregate == target
        aggregate_columns.append(aggregate)
        target_columns.append(target)
        word_checks += 1

    aggregate_map = sp.Matrix.hstack(*aggregate_columns)
    target_map = sp.Matrix.hstack(*target_columns)
    assert word_checks == 81
    assert aggregate_map.rank() == 4
    assert target_map.rank() == 3

    epsilon = sp.ones(1, 9)
    p_value = int((epsilon * q)[0])
    projector = p_value * sp.eye(9) - q * epsilon
    assert p_value == 2
    assert projector.rank() == 8
    assert (projector * sigma).rank() == 5
    return {
        "sigma_rank": sigma.rank(),
        "swallow_rank": full_swallow.rank(),
        "aggregate_rank": aggregate_map.rank(),
        "excess_dimension": sigma.rank() - 4,
        "port_words": word_checks,
        "transverse_rank": (projector * sigma).rank(),
    }


def rank_five_mixed_boundary() -> dict[str, int]:
    x_u = sp.Matrix([[0, 0, 0], [1, 1, 0], [-1, 0, 1]])
    y_u = sp.Matrix([[-1, 0, 1], [0, 0, 0], [0, 0, 0]])
    x_v = sp.Matrix([[1, 1, 0], [0, 0, 0], [0, -1, 1]])
    y_v = sp.Matrix([[0, 0, -1], [0, 1, 0], [0, 0, 1]])
    pair = pair_columns(x_u, y_u, x_v, y_v)
    e9 = [basis_vector(index, 9) for index in range(9)]
    diagonal = sp.Matrix.hstack(e9[0], e9[4], e9[8])
    assert pair.rank() == 5
    assert pair.row_join(diagonal).rank() == 5
    assert pair[:, 0] == -e9[0]
    assert pair[:, 4] == e9[4]
    assert pair[:, 8] == e9[8]

    annihilator = sp.Matrix.vstack(
        e9[1].T,
        e9[2].T,
        (e9[3] + e9[5]).T,
        (e9[6] + e9[7]).T,
    )
    assert annihilator * pair == sp.zeros(4, 9)
    assert annihilator.rank() == 4

    variables = sp.symbols("x0 x1 x2 y0 y1 y2")
    x_z = sp.Matrix(variables[:3])
    y_z = sp.Matrix(variables[3:])
    equations = []
    for x_other, y_other in ((x_u, y_u), (x_v, y_v)):
        for column in range(3):
            matrix = tensor(x_z, y_other[:, column]) + tensor(
                x_other[:, column], y_z
            )
            equations.extend(annihilator * matrix)
    compatibility = sp.Matrix(
        [[sp.expand(equation).coeff(variable) for variable in variables] for equation in equations]
    )
    assert compatibility.shape == (24, 6)
    assert compatibility.rank() == 6
    independent_rows = compatibility.T.rref()[1]
    determinant = compatibility[list(independent_rows), :].det()
    assert abs(determinant) == 1

    raw_flattening = sp.Matrix([[1], [2], [3]]) * sp.Matrix([[1, -1, 2]])
    ghz_flattening = sp.eye(3)
    assert raw_flattening.rank() == 1
    assert ghz_flattening.rank() == 3
    return {
        "pair_rank": pair.rank(),
        "annihilator_rank": annihilator.rank(),
        "third_label_equations": compatibility.rows,
        "third_label_rank": compatibility.rank(),
        "independent_determinant": int(determinant),
        "raw_deck_flattening_rank": raw_flattening.rank(),
        "ghz_flattening_rank": ghz_flattening.rank(),
    }


def main() -> None:
    aggregate = aggregate_rank_checks()
    strata = canonical_rank_strata_checks()
    rank_six = rank_six_interface_control()
    rank_five = rank_five_mixed_boundary()
    print("GLS40 aggregate-deck/excess/cylinder primary checks: PASS")
    print("  aggregate rank formulas:", aggregate)
    print("  canonical rank strata:", strata)
    print("  rank-six full-equation interface:", rank_six)
    print("  rank-five mixed/pure boundary:", rank_five)


if __name__ == "__main__":
    main()
