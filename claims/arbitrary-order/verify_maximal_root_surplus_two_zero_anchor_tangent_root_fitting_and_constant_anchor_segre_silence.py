"""Focused exact checks for the GLS34 tangent-root and anchor boundary."""

from __future__ import annotations

import runpy
from functools import cache
from itertools import product
from pathlib import Path

import sympy as sp

GLS30 = runpy.run_path(
    str(
        Path(__file__).with_name(
            "verify_maximal_root_surplus_two_zero_anchor_normal_product_"
            "divisor_kernel_profile_and_same_graph_sharpness.py"
        )
    )
)


def add_polynomials(
    left: dict[tuple[int, ...], sp.Expr],
    right: dict[tuple[int, ...], sp.Expr],
    scale: sp.Expr | None = None,
) -> dict[tuple[int, ...], sp.Expr]:
    if scale is None:
        scale = sp.Integer(1)
    output = dict(left)
    for exponent, coefficient in right.items():
        output[exponent] = sp.expand(
            output.get(exponent, sp.Integer(0)) + scale * coefficient
        )
        if output[exponent] == 0:
            del output[exponent]
    return output


def multiply_polynomials(
    left: dict[tuple[int, ...], sp.Expr],
    right: dict[tuple[int, ...], sp.Expr],
) -> dict[tuple[int, ...], sp.Expr]:
    output: dict[tuple[int, ...], sp.Expr] = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_exponent[index] + right_exponent[index] for index in range(6)
            )
            output[exponent] = sp.expand(
                output.get(exponent, sp.Integer(0))
                + left_coefficient * right_coefficient
            )
    return {
        exponent: coefficient
        for exponent, coefficient in output.items()
        if coefficient != 0
    }


def linear_polynomial(
    component: int, residual: int, matrix: sp.Matrix
) -> dict[tuple[int, ...], sp.Expr]:
    output = {}
    offset = 3 * residual
    for colour in range(3):
        coefficient = matrix[component, colour]
        if coefficient:
            exponent = [0] * 6
            exponent[offset + colour] = 1
            output[tuple(exponent)] = coefficient
    return output


def residual_monomial(
    first_colour: int, second_colour: int
) -> dict[tuple[int, ...], sp.Expr]:
    exponent = [0] * 6
    exponent[first_colour] = 1
    exponent[3 + second_colour] = 1
    return {tuple(exponent): sp.Integer(1)}


def homogeneous_exponents(degree: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (first, second, degree - first - second)
        for first in range(degree + 1)
        for second in range(degree + 1 - first)
    )


def coefficient_matrix(
    columns: list[dict[tuple[int, ...], sp.Expr]],
    exponent_order: list[tuple[int, ...]],
) -> sp.Matrix:
    row_index = {exponent: index for index, exponent in enumerate(exponent_order)}
    vectors = []
    for polynomial in columns:
        vector = sp.zeros(len(exponent_order), 1)
        for exponent, coefficient in polynomial.items():
            vector[row_index[exponent]] = coefficient
        vectors.append(vector)
    return sp.Matrix.hstack(*vectors)


def shore_data() -> tuple[
    tuple[tuple[dict[tuple[int, ...], sp.Expr], ...], ...],
    tuple[tuple[dict[tuple[int, ...], sp.Expr], ...], ...],
]:
    matrices = (
        (
            sp.Matrix(((1, 1, -1), (2, -1, 1), (-2, -1, 0))),
            sp.Matrix(((-1, -1, 1), (2, 1, 2), (-1, 0, -1))),
        ),
        (
            sp.Matrix(((-2, 2, -2), (0, -2, -1), (-1, -2, 1))),
            sp.Matrix(((2, 1, 0), (-1, 1, 1), (2, 1, -1))),
        ),
    )
    normals = []
    root_syzygies = []
    for shore in range(2):
        xi0 = tuple(
            linear_polynomial(component, 0, matrices[shore][0])
            for component in range(3)
        )
        xi1 = tuple(
            linear_polynomial(component, 1, matrices[shore][1])
            for component in range(3)
        )
        normal = (
            add_polynomials(
                multiply_polynomials(xi0[1], xi1[2]),
                multiply_polynomials(xi0[2], xi1[1]),
                -1,
            ),
            add_polynomials(
                multiply_polynomials(xi0[2], xi1[0]),
                multiply_polynomials(xi0[0], xi1[2]),
                -1,
            ),
            add_polynomials(
                multiply_polynomials(xi0[0], xi1[1]),
                multiply_polynomials(xi0[1], xi1[0]),
                -1,
            ),
        )
        root_syzygy = tuple(
            add_polynomials(
                multiply_polynomials(xi1[0], xi0[component]),
                multiply_polynomials(xi0[0], xi1[component]),
                -1,
            )
            for component in range(3)
        )
        assert root_syzygy[0] == {}
        assert root_syzygy[1] == {
            exponent: -coefficient for exponent, coefficient in normal[2].items()
        }
        assert root_syzygy[2] == normal[1]
        normals.append(normal)
        root_syzygies.append(root_syzygy)
    return tuple(normals), tuple(root_syzygies)


def fitting_certificate() -> dict[str, object]:
    normals, root_syzygies = shore_data()
    exponent22 = [
        first + second
        for first in homogeneous_exponents(2)
        for second in homogeneous_exponents(2)
    ]
    kappas = []
    for shore in range(2):
        columns = [
            multiply_polynomials(
                normals[shore][component], residual_monomial(first, second)
            )
            for component in (1, 2)
            for first, second in product(range(3), repeat=2)
        ]
        kappas.append(coefficient_matrix(columns, exponent22))

    exponent33 = [
        first + second
        for first in homogeneous_exponents(3)
        for second in homogeneous_exponents(3)
    ]
    mu_columns = [
        multiply_polynomials(
            multiply_polynomials(normals[0][left], normals[1][right]),
            residual_monomial(first, second),
        )
        for left, right in product((1, 2), repeat=2)
        for first, second in product(range(3), repeat=2)
    ]
    mu = coefficient_matrix(mu_columns, exponent33)

    observation_keys = []
    for profile, degree in (("00", 1), ("10", 2), ("01", 2), ("11", 3)):
        observation_keys.extend(
            (profile, first + second)
            for first in homogeneous_exponents(degree)
            for second in homogeneous_exponents(degree)
        )
    observation_row = {key: index for index, key in enumerate(observation_keys)}
    observation_columns = []
    tensor_indices = tuple(product(range(3), repeat=4))
    for left, right, first, second in tensor_indices:
        residual = residual_monomial(first, second)
        profiles: dict[str, dict[tuple[int, ...], sp.Expr]] = {"11": {}}
        if left == 0 and right == 0:
            profiles["00"] = residual
        if right == 0:
            profiles["10"] = multiply_polynomials(normals[0][left], residual)
        if left == 0:
            profiles["01"] = multiply_polynomials(normals[1][right], residual)
        profiles["11"] = multiply_polynomials(
            multiply_polynomials(normals[0][left], normals[1][right]), residual
        )
        column = sp.zeros(len(observation_keys), 1)
        for profile, polynomial in profiles.items():
            for exponent, coefficient in polynomial.items():
                column[observation_row[(profile, exponent)]] = coefficient
        observation_columns.append(column)
    observation = sp.Matrix.hstack(*observation_columns)

    tensor_index = {entry: index for index, entry in enumerate(tensor_indices)}
    blind_columns = []
    for shore in range(2):
        for other_component in range(3):
            column = sp.zeros(81, 1)
            for root_component, polynomial in enumerate(root_syzygies[shore]):
                for exponent, coefficient in polynomial.items():
                    first = next(index for index in range(3) if exponent[index])
                    second = next(index for index in range(3) if exponent[3 + index])
                    tensor_entry = (
                        (root_component, other_component, first, second)
                        if shore == 0
                        else (other_component, root_component, first, second)
                    )
                    column[tensor_index[tensor_entry]] += coefficient
            blind_columns.append(column)
    blind = sp.Matrix.hstack(*blind_columns)

    kappa_rows = (
        (0, 1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 18, 19, 21, 22, 23, 24),
        (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 13, 18, 19, 20, 21, 22, 25),
    )
    kappa_columns = tuple(range(17))
    kappa_determinants = tuple(
        matrix.extract(rows, kappa_columns).det()
        for matrix, rows in zip(kappas, kappa_rows, strict=True)
    )
    assert kappa_determinants == (576, -33554432)

    mu_rows = (
        0,
        1,
        2,
        4,
        5,
        6,
        7,
        8,
        10,
        11,
        12,
        14,
        15,
        16,
        17,
        18,
        20,
        21,
        24,
        25,
        40,
        41,
        42,
        44,
        45,
        46,
        47,
        48,
        50,
        51,
        54,
        55,
    )
    mu_columns = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
    )
    mu_determinant = mu.extract(mu_rows, mu_columns).det()
    assert mu_determinant == 2**55 * 3**7

    blind_rows = (9, 27, 36, 37, 45, 63)
    blind_determinant = blind.extract(blind_rows, range(6)).det()
    assert blind_determinant == -896

    observation_rows = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        12,
        13,
        14,
        15,
        16,
        18,
        19,
        20,
        21,
        27,
        28,
        30,
        31,
        32,
        33,
        45,
        46,
        47,
        48,
        49,
        51,
        52,
        53,
        54,
        55,
        58,
        63,
        64,
        65,
        66,
        67,
        70,
        81,
        82,
        83,
        85,
        86,
        87,
        88,
        89,
        91,
        92,
        93,
        95,
        96,
        97,
        98,
        99,
        101,
        102,
        105,
        106,
        121,
        122,
        123,
        125,
        126,
        127,
        128,
        129,
        131,
        132,
        135,
        136,
    )
    observation_columns_for_minor = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
    )
    observation_determinant = observation.extract(
        observation_rows, observation_columns_for_minor
    ).det()
    assert observation_determinant == 2**86 * 3**9

    ranks = (
        kappas[0].rank(),
        kappas[1].rank(),
        mu.rank(),
        blind.rank(),
        observation.rank(),
    )
    assert ranks == (17, 17, 32, 6, 75)
    assert observation * blind == sp.zeros(181, 6)
    return {
        "matrix_shapes": (
            kappas[0].shape,
            kappas[1].shape,
            mu.shape,
            blind.shape,
            observation.shape,
        ),
        "ranks": ranks,
        "nonzero_minors": (
            *kappa_determinants,
            mu_determinant,
            blind_determinant,
            observation_determinant,
        ),
        "observation_times_blind_zero": True,
    }


def tensor_product(vectors: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.kronecker_product(*vectors)


def restriction_sum(
    factors: tuple[tuple[sp.Matrix, ...], ...], deltas: tuple[sp.Expr, ...]
) -> sp.Matrix:
    tensors = tuple(tensor_product(colour_factors) for colour_factors in factors)
    output = sp.zeros(tensors[0].rows, 1)
    for delta, tensor in zip(deltas, tensors, strict=True):
        output += delta * tensor
    return output


def segre_restriction_representatives() -> dict[str, object]:
    zero = sp.zeros(1, 1)
    one = sp.ones(1, 1)

    support_one_killed = (((zero, one),), (sp.Integer(1),))
    killed_value = restriction_sum(*support_one_killed)
    assert killed_value == sp.zeros(1, 1)

    support_one_surviving = (((one, sp.Matrix((2,))),), (sp.Integer(1),))
    surviving_value = restriction_sum(*support_one_surviving)
    assert surviving_value == sp.Matrix((2,))

    support_two_killed = (
        ((zero, one), (one, zero)),
        (sp.Integer(2), sp.Integer(-3)),
    )
    assert restriction_sum(*support_two_killed) == sp.zeros(1, 1)

    base = sp.Matrix((1, 2))
    support_two_proportional = (
        (
            (base, sp.Matrix((3,)), one),
            (2 * base, sp.Matrix((-3,)), sp.Matrix((3,))),
        ),
        (sp.Integer(6), sp.Integer(1)),
    )
    proportional_tensors = tuple(
        tensor_product(factors) for factors in support_two_proportional[0]
    )
    assert proportional_tensors[1] == -6 * proportional_tensors[0]
    assert 6 + 1 * (2 * -1 * 3) == 0
    assert restriction_sum(*support_two_proportional) == sp.zeros(2, 1)

    support_three_exceptional = (
        (
            (sp.Matrix((1,)), sp.Matrix((3,)), sp.Matrix((1, 0))),
            (sp.Matrix((2,)), sp.Matrix((-1,)), sp.Matrix((0, 1))),
            (
                sp.Matrix((-1,)),
                sp.Matrix((2,)),
                sp.Matrix((sp.Rational(3, 2), -1)),
            ),
        ),
        (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
    )
    exceptional_relation = (
        3 * support_three_exceptional[0][0][2]
        - 2 * support_three_exceptional[0][1][2]
        - 2 * support_three_exceptional[0][2][2]
    )
    assert exceptional_relation == sp.zeros(2, 1)
    assert all(
        factor != sp.zeros(factor.rows, 1)
        for colour_factors in support_three_exceptional[0]
        for factor in colour_factors
    )
    assert restriction_sum(*support_three_exceptional) == sp.zeros(2, 1)

    support_three_nonsilent = (
        (
            support_three_exceptional[0][0],
            support_three_exceptional[0][1],
            (
                sp.Matrix((-1,)),
                sp.Matrix((2,)),
                sp.Matrix((1, 1)),
            ),
        ),
        support_three_exceptional[1],
    )
    nonsilent_value = restriction_sum(*support_three_nonsilent)
    assert nonsilent_value == sp.Matrix((1, -4))
    evaluation_tuple = (sp.Matrix((1,)), sp.Matrix((1,)), sp.Matrix((1, 0)))
    evaluated = sum(
        delta
        * sp.prod(
            (factor.T * vector)[0]
            for factor, vector in zip(colour_factors, evaluation_tuple, strict=True)
        )
        for delta, colour_factors in zip(
            support_three_nonsilent[1], support_three_nonsilent[0], strict=True
        )
    )
    assert evaluated == 1
    return {
        "support_zero": {"automatic_silence": True},
        "support_one": {
            "killed": tuple(killed_value),
            "surviving": tuple(surviving_value),
        },
        "support_two": {
            "both_killed": True,
            "local_proportionalities": (2, -1, 3),
            "scalar_cancellation": 0,
        },
        "support_three": {
            "exceptional_relation": tuple(exceptional_relation),
            "silent": True,
            "nonsilent_restriction": tuple(nonsilent_value),
            "nonsilent_evaluation": evaluated,
        },
    }


def same_line(left: sp.Matrix, right: sp.Matrix) -> bool:
    return (
        left.rank() == right.rank() == 1 and sp.Matrix.hstack(left, right).rank() == 1
    )


def two_active_physical_control() -> dict[str, object]:
    x, y, responses = GLS30["two_active_control"]()
    edges, normal0, normal1, projector = GLS30["build_response_deck_graph"](
        x, y, responses, 2
    )
    assert projector == -2
    basis = tuple(sp.eye(3)[:, colour] for colour in range(3))
    one = sp.ones(3, 1)
    a = (basis[1], basis[2], basis[0], basis[2])
    b = (basis[2], basis[1], basis[2], basis[0])
    root0 = basis[2]
    tangent0 = sp.Matrix((sp.Rational(1, 2), sp.Rational(1, 2), -1))
    root1 = sp.Matrix((1, -1, 1))
    tangent1 = sp.Matrix((0, 1, -1))
    assert (one.T * root0)[0] == 1
    assert (normal0.T * root0)[0] == 0
    assert (one.T * tangent0)[0] == 0
    assert (normal0.T * tangent0)[0] == 1
    assert (one.T * root1)[0] == 1
    assert (normal1.T * root1)[0] == 0
    assert (one.T * tangent1)[0] == 0
    assert (normal1.T * tangent1)[0] == 1

    put_edge = GLS30["put_edge"]
    edge_block = GLS30["edge_block"]
    for port in range(4):
        put_edge(
            edges,
            0,
            4 + port,
            root0 * a[port].T + tangent0 * x[port].T,
        )
        put_edge(
            edges,
            1,
            4 + port,
            root1 * b[port].T + tangent1 * y[port].T,
        )
        assert edge_block(edges, 0, 4 + port).T * one == a[port]
        assert edge_block(edges, 0, 4 + port).T * normal0 == x[port]
        assert edge_block(edges, 1, 4 + port).T * one == b[port]
        assert edge_block(edges, 1, 4 + port).T * normal1 == y[port]

    def joint_kernel(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
        nullspace = sp.Matrix.hstack(left, right).T.nullspace()
        assert len(nullspace) == 1
        return nullspace[0]

    kernel00 = tuple(joint_kernel(a[port], b[port]) for port in range(4))
    kernel10 = tuple(joint_kernel(x[port], b[port]) for port in range(4))
    kernel01 = tuple(joint_kernel(a[port], y[port]) for port in range(4))
    expected00 = (basis[0], basis[0], basis[1], basis[1])
    expected10 = (basis[1], basis[2], basis[0], basis[2])
    expected01 = (basis[2], basis[1], basis[2], basis[0])
    for observed, expected in zip(kernel00, expected00, strict=True):
        assert same_line(observed, expected)
    for observed, expected in zip(kernel10, expected10, strict=True):
        assert same_line(observed, expected)
    for observed, expected in zip(kernel01, expected01, strict=True):
        assert same_line(observed, expected)

    for kernels in (kernel10, kernel01):
        for omitted in range(4):
            product_vector = sp.ones(3, 1)
            for port in range(4):
                if port != omitted:
                    product_vector = product_vector.multiply_elementwise(kernels[port])
            assert product_vector == sp.zeros(3, 1)
    for colour in range(3):
        assert sp.prod(kernel00[port][colour] for port in range(4)) == 0

    constant_deck_value = GLS30["contracted_coefficient"](
        {},
        {4 + port: kernel00[port] for port in range(4)},
        edges,
        tuple(range(4, 8)),
    )
    constant_deck_left = sp.expand(projector * constant_deck_value)
    assert constant_deck_value == -2
    assert constant_deck_left == 4

    suppliers = {pair: GLS30["channel_pair"](x, y, pair) for pair in GLS30["PAIRS"]}
    assert GLS30["tensor4_from_pair_terms"](suppliers, responses) == GLS30[
        "diagonal_tensor"
    ]((1, 2, 0))
    assert all(response != sp.zeros(3) for response in responses.values())

    response_checks = 0
    contracted_coefficient = GLS30["contracted_coefficient"]
    for pair in GLS30["PAIRS"]:
        vertices = (2, 3, 4 + pair[0], 4 + pair[1])
        for word in product(range(3), repeat=2):
            observed = contracted_coefficient(
                {vertices[2]: word[0], vertices[3]: word[1]},
                {2: one, 3: one},
                edges,
                vertices,
            )
            assert observed == responses[pair][word]
            response_checks += 1
    assert response_checks == 54

    profiles = {}
    for label, left, right in (
        ("00", one, one),
        ("10", normal0, one),
        ("01", one, normal1),
        ("11", normal0, normal1),
    ):
        failures = {}
        for word in product(range(3), repeat=4):
            observed = contracted_coefficient(
                {4 + port: word[port] for port in range(4)},
                {0: left, 1: right, 2: one, 3: one},
                edges,
                tuple(range(8)),
            )
            expected = left[word[0]] * right[word[0]] if word == (word[0],) * 4 else 0
            defect = sp.expand(observed - expected)
            if defect:
                failures[word] = defect
        profiles[label] = failures
    profile_counts = tuple(len(profiles[label]) for label in ("00", "10", "01", "11"))
    assert profile_counts == (15, 10, 11, 0)
    assert all(profiles[label][(0, 0, 0, 0)] == -1 for label in ("00", "10", "01"))

    singleton_defect_slices = 0
    for label, kernels in (("10", kernel10), ("01", kernel01)):
        for free_port in range(4):
            complement_ports = tuple(port for port in range(4) if port != free_port)
            for free_colour in range(3):
                contracted_defect = sp.Integer(0)
                for complement_word in product(range(3), repeat=3):
                    word = [0, 0, 0, 0]
                    word[free_port] = free_colour
                    for port, colour in zip(
                        complement_ports, complement_word, strict=True
                    ):
                        word[port] = colour
                    contracted_defect += profiles[label].get(
                        tuple(word), sp.Integer(0)
                    ) * sp.prod(kernels[port][word[port]] for port in complement_ports)
                assert sp.expand(contracted_defect) == 0
                singleton_defect_slices += 1
    assert singleton_defect_slices == 24

    raw_graph_coefficient = GLS30["graph_coefficient"]

    @cache
    def graph_coefficient(word: tuple[int, ...]) -> sp.Expr:
        return raw_graph_coefficient(word, edges)

    pure = tuple(graph_coefficient((colour,) * 8) for colour in range(3))
    assert pure == (0, 0, 0)
    ghz_failures = 0
    mixed_nonzero = 0
    for word in product(range(3), repeat=8):
        expected = sp.Integer(1) if word == (word[0],) * 8 else sp.Integer(0)
        observed = graph_coefficient(word)
        if observed != expected:
            ghz_failures += 1
        if word != (word[0],) * 8 and observed:
            mixed_nonzero += 1
    assert mixed_nonzero == 144
    assert ghz_failures == 147
    return {
        "p": projector,
        "kernel_axes": {
            "K00": (0, 0, 1, 1),
            "K10": (1, 2, 0, 2),
            "K01": (2, 1, 2, 0),
        },
        "normal_identity": (1, 2, 0),
        "constant_diagonal_restriction": 0,
        "constant_kernel_values": (constant_deck_left, 0),
        "constant_kernel_defect": constant_deck_left,
        "nonzero_physical_responses": 6,
        "response_coefficients": response_checks,
        "profile_failure_counts": profile_counts,
        "zero_singleton_defect_slices": singleton_defect_slices,
        "first_defects": (-1, -1, -1),
        "pure_coefficients": pure,
        "mixed_nonzero_coefficients": mixed_nonzero,
        "ghz_failures": ghz_failures,
    }


def main() -> None:
    fitting = fitting_certificate()
    segre = segre_restriction_representatives()
    control = two_active_physical_control()
    print("GLS34 tangent-root/constant-anchor primary checks: PASS")
    print("  exact tangent-root Fitting certificate:", fitting)
    print("  direct Segre-restriction representatives:", segre)
    print("  two-active diagonal-silent physical control:", control)
    print(
        "  scope: coefficient/diagonal-silence boundary; strategic/global closure OPEN"
    )


if __name__ == "__main__":
    main()
