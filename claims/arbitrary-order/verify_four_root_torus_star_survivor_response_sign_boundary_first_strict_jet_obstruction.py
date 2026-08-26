#!/usr/bin/env python3
"""Verify the first strict-transform jet at all three GLD77 sign points.

This is an exact calculation over Q(i).  It keeps the four scale-fixed
GLD75 survivor tangent directions, the moving 35-dimensional raw fibre, the
moving thirteen-column response quotient, and both proportionality-slope
variables.  At each projective sign-plane boundary point it computes

    M u + S_survivor f + S_slope d + rho*r = 0,

where rho is the first homogeneous affine coordinate.  The result is only a
first-jet obstruction: rho=0 is compatible and higher-order lifts are not
excluded here.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import chain, combinations, permutations, product
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
GLD74 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py"
)
GLD75 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py"
)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


G74 = load(GLD74, "gld74_first_strict_jet")
G75 = load(GLD75, "gld75_first_strict_jet")
G72 = G75.load_gld72()
GATE = G72.load_gate()
PARENT = GATE.load_parent()
G73 = G74.load_gld73()


# Sparse t-coordinate representatives and their GLD74 proportionality charts.
BOUNDARY_POINTS = (
    (
        "v_minus",
        -1,
        1,
        {13: -1, 15: 1, 22: 1, 24: -1, 31: -1, 33: 1},
    ),
    (
        "v_plus",
        1,
        -1,
        {
            9: -sp.I,
            10: -1,
            11: sp.I,
            14: 1,
            18: sp.I,
            19: 1,
            20: -sp.I,
            23: -1,
            27: -sp.I,
            28: -1,
            29: sp.I,
            32: 1,
        },
    ),
    (
        "v_third",
        -1,
        -1,
        {
            9: 1,
            10: -1,
            11: -1,
            14: 1,
            18: -1,
            19: 1,
            20: 1,
            23: -1,
            27: 1,
            28: -1,
            29: -1,
            32: 1,
        },
    ),
)


def dual(value, derivative=0):
    return value, derivative


def dadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def dmul(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
    )


def dprod(values):
    result = dual(1)
    for value in values:
        result = dmul(result, value)
    return result


def dsum(values):
    result = dual(0)
    for value in values:
        result = dadd(result, value)
    return result


PERMUTATIONS_4 = tuple(permutations(range(4)))
MODES = tuple(range(4))
PAIRS = tuple(combinations(MODES, 2))


def permanent_dual(columns):
    return dsum(
        dprod([columns[mode][sigma[mode]] for mode in MODES])
        for sigma in PERMUTATIONS_4
    )


def g(value):
    return G73.gaussian(sp.expand(value))


def g2s(value):
    return sp.Rational(value[0]) + sp.I * sp.Rational(value[1])


def gsum(values):
    result = G73.GZERO
    for value in values:
        result = G73.gadd(result, value)
    return result


def gaddv(left, right):
    return [G73.gadd(a, b) for a, b in zip(left, right, strict=True)]


def gsubv(left, right):
    return [G73.gsub(a, b) for a, b in zip(left, right, strict=True)]


def gscale(scalar, vector):
    if not isinstance(scalar, tuple):
        scalar = G73.gaussian(sp.Integer(scalar))
    return [G73.gmul(scalar, value) for value in vector]


def gaddm(left, right):
    return [gaddv(a, b) for a, b in zip(left, right, strict=True)]


def gsubm(left, right):
    return [gsubv(a, b) for a, b in zip(left, right, strict=True)]


def gscalem(scalar, matrix):
    return [gscale(scalar, row) for row in matrix]


def gmatvec(matrix, vector):
    return [
        gsum(G73.gmul(matrix[row][column], vector[column]) for column in range(len(vector)))
        for row in range(len(matrix))
    ]


def rref_pairs(matrix):
    """Return RREF and pivot columns for a Q(i)-pair matrix."""

    if isinstance(matrix, sp.MatrixBase):
        work = [
            [G73.gaussian(sp.expand(matrix[row, column])) for column in range(matrix.cols)]
            for row in range(matrix.rows)
        ]
    else:
        work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if row_count else 0
    pivot_row = 0
    pivots = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column] != G73.GZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [G73.gdiv(value, scale) for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == G73.GZERO:
                continue
            factor = work[row][column]
            work[row] = [
                G73.gsub(value, G73.gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, tuple(pivots)


def rank_pairs(matrix):
    return len(rref_pairs(matrix)[1])


def nullspace_pairs(matrix):
    work, pivots = rref_pairs(matrix)
    column_count = len(matrix[0])
    pivot_set = set(pivots)
    vectors = []
    for free_column in range(column_count):
        if free_column in pivot_set:
            continue
        vector = [G73.GZERO] * column_count
        vector[free_column] = G73.GONE
        for row, pivot in enumerate(pivots):
            vector[pivot] = G73.gsub(G73.GZERO, work[row][free_column])
        vectors.append(vector)
    return vectors


def solve_pairs(matrix, right):
    """Solve a square nonsingular Q(i)-pair system."""

    work = [row[:] + [value] for row, value in zip(matrix, right, strict=True)]
    row_count = len(work)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            row for row in range(pivot_row, row_count) if work[row][column] != G73.GZERO
        )
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [G73.gdiv(value, scale) for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == G73.GZERO:
                continue
            factor = work[row][column]
            work[row] = [
                G73.gsub(value, G73.gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
    return [work[row][-1] for row in range(column_count)]


def transformed_ports(centre, leaf, ports):
    result = []
    for port, frame in zip(ports, (centre, leaf, leaf, leaf), strict=True):
        port_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in port))
        result.append(port_matrix * frame.inv().T)
    return result


def dual_ports(tangent, centre, leaf, ports, base_ports):
    dcentre = sp.Matrix(3, 3, list(tangent[:9]))
    dleaf = sp.zeros(3, 3)
    for index, (row, colour) in enumerate(
        (item for row in (1, 2) for item in ((row, 0), (row, 1), (row, 2)))
    ):
        dleaf[row, colour] = tangent[9 + index]
    result = []
    for port, frame, dframe, base in zip(
        ports,
        (centre, leaf, leaf, leaf),
        (dcentre, dleaf, dleaf, dleaf),
        base_ports,
        strict=True,
    ):
        port_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in port))
        inverse_transpose = frame.inv().T
        derivative = -inverse_transpose * dframe.T * inverse_transpose
        derivative_matrix = port_matrix * derivative
        result.append(
            [
                [dual(base[row, column], derivative_matrix[row, column]) for row in range(4)]
                for column in range(3)
            ]
        )
    return result


def q_layer_columns(ports_dual, xi, eta):
    local_indices = PARENT.LOCAL_INDICES
    local_index = PARENT.LOCAL_INDEX
    q_column = [
        permanent_dual([ports_dual[mode][indices[mode]] for mode in MODES])
        for indices in local_indices
    ]
    residual_columns = []
    for residual in (xi, eta):
        residual_dual = [dual(value) for value in residual]
        for labelled_mode in MODES:
            companion_modes = tuple(mode for mode in MODES if mode != labelled_mode)
            for labelled_index in range(3):
                column = [dual(0) for _ in local_indices]
                for companion_indices in product(range(3), repeat=3):
                    indices = [0] * 4
                    indices[labelled_mode] = labelled_index
                    for mode, index in zip(companion_modes, companion_indices, strict=True):
                        indices[mode] = index
                    column[local_index[tuple(indices)]] = permanent_dual(
                        [residual_dual]
                        + [ports_dual[mode][indices[mode]] for mode in companion_modes]
                    )
                residual_columns.append(column)
    pair_columns = []
    for labelled_modes in PAIRS:
        companion_modes = tuple(mode for mode in MODES if mode not in labelled_modes)
        for labelled_indices in product(range(3), repeat=2):
            column = [dual(0) for _ in local_indices]
            for companion_indices in product(range(3), repeat=2):
                indices = [0] * 4
                for mode, index in zip(labelled_modes, labelled_indices, strict=True):
                    indices[mode] = index
                for mode, index in zip(companion_modes, companion_indices, strict=True):
                    indices[mode] = index
                column[local_index[tuple(indices)]] = permanent_dual(
                    [
                        [dual(value) for value in xi],
                        [dual(value) for value in eta],
                        ports_dual[companion_modes[0]][companion_indices[0]],
                        ports_dual[companion_modes[1]][companion_indices[1]],
                    ]
                )
            pair_columns.append(column)
    return [q_column], residual_columns, pair_columns


def response_maps(ports_dual, eta, gld73):
    mixed_words = tuple(word for word in product(range(3), repeat=4) if len(set(word)) != 1)
    matchings = tuple(gld73.perfect_matchings(tuple(range(10))))
    pair_offset = {pair: index for index, pair in enumerate(combinations(range(4), 2))}
    maps = []
    for root in range(4):
        varied_edge = (root, 4)
        root_matchings = tuple(matching for matching in matchings if varied_edge in matching)
        rows = []
        for word in mixed_words:
            row = [dual(0) for _ in range(79)]
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
                factors = []
                for left_root, right_vertex in complement:
                    if left_root < 4:
                        factors.append(
                            dual(eta[left_root])
                            if right_vertex == 5
                            else ports_dual[right_vertex - 6][word[right_vertex - 6]][left_root]
                        )
                row[raw_index] = dadd(row[raw_index], dprod(factors))
            rows.append(row)
        maps.append(rows)
    return maps


def matrix_from_dual(columns, part):
    return sp.Matrix([[value[part] for value in row] for row in columns])


def quotient_derivative(x0, xd, c0, cd, cp_rows, q_rows):
    cp0 = [[c0[row][column] for column in range(13)] for row in cp_rows]
    cq0 = [[c0[row][column] for column in range(13)] for row in q_rows]
    cpd = [[cd[row][column] for column in range(13)] for row in cp_rows]
    cqd = [[cd[row][column] for column in range(13)] for row in q_rows]
    coefficient0 = solve_pairs(cp0, [x0[row] for row in cp_rows])
    coefficientd = solve_pairs(
        cp0,
        gsubv(
            [xd[row] for row in cp_rows],
            gmatvec(cpd, coefficient0),
        ),
    )
    return gsubv(
        gsubv(
            [xd[row] for row in q_rows],
            gmatvec(cqd, coefficient0),
        ),
        gmatvec(cq0, coefficientd),
    )


def build_context():
    certificate = json.loads(G75.CERTIFICATE.read_text())
    shifts = sp.symbols("x0:15")
    basis = [G75.sparse_polynomial(encoded, shifts).as_expr() for encoded in certificate["basis"]]
    zero = {shift: 0 for shift in shifts}
    scale_jacobian = sp.Matrix([*basis, shifts[8]]).jacobian(shifts).subs(zero)
    assert scale_jacobian.rank() == 11
    tangent_vectors = []
    for free_coordinate in (6, 12, 13, 14):
        vector = next(value for value in scale_jacobian.nullspace() if value[free_coordinate] != 0)
        tangent_vectors.append(vector / vector[free_coordinate])

    centre, leaf = G72.candidate_frames()
    xi, eta, ports = PARENT.canonical_torus_star(1)
    base_ports = transformed_ports(centre, leaf, ports)
    base_dual_ports = [
        [[dual(base_ports[mode][row, column]) for row in range(4)] for column in range(3)]
        for mode in range(4)
    ]
    base_layers = q_layer_columns(base_dual_ports, xi, eta)
    base_columns_dual = list(chain.from_iterable(base_layers))
    base_columns = [[value[0] for value in column] for column in base_columns_dual]
    base_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in base_columns))
    assert base_matrix.shape == (81, 79) and base_matrix.rank() == 44

    delta = sp.Matrix(
        [
            sp.Integer(root == first == second == third)
            for root, first, second, third in PARENT.LOCAL_INDICES
        ]
    )
    particular, raw_kernel, pivots, free_columns = G74.affine_fibre(
        G73, base_columns, delta
    )
    assert len(pivots) == 44 and len(free_columns) == 35
    pivot_basis = base_matrix[:, list(pivots)]
    pivot_rows = rref_pairs(
        [[G73.gaussian(sp.expand(pivot_basis[row, column])) for row in range(81)] for column in range(44)]
    )[1]
    assert len(pivot_rows) == 44

    layer_derivatives = []
    response_derivatives = []
    for tangent in tangent_vectors:
        ports_d = dual_ports(tangent, centre, leaf, ports, base_ports)
        layer_derivatives.append(list(chain.from_iterable(q_layer_columns(ports_d, xi, eta))))
        response_derivatives.append(response_maps(ports_d, eta, G73))

    base_responses_d = response_maps(base_dual_ports, eta, G73)
    base_responses = [matrix_from_dual(rows, 0) for rows in base_responses_d]
    base_response_reference = G74.q0_response_context(
        G73,
        eta,
        [
            [[base_ports[mode][row, column] for row in range(4)] for column in range(3)]
            for mode in range(4)
        ],
    )
    assert all(
        all(
            sp.expand(base_responses[root][row, column] - base_response_reference[root][row, column]) == 0
            for row in range(78)
            for column in range(79)
        )
        for root in range(4)
    )

    mixed_rows = tuple(
        PARENT.LOCAL_INDEX[word]
        for word in product(range(3), repeat=4)
        if len(set(word)) != 1
    )
    constant_indices = (0, *range(13, 25))
    constant0 = [
        [G73.gaussian(sp.expand(base_columns[column][row])) for column in constant_indices]
        for row in mixed_rows
    ]
    _constant_rref, constant_pivots = rref_pairs(
        [[constant0[row][column] for row in range(78)] for column in range(13)]
    )
    assert len(constant_pivots) == 13
    quotient_rows = tuple(row for row in range(78) if row not in set(constant_pivots))

    coefficient_data = G74.quotient_forms()
    assert G74.coefficient_fingerprint(coefficient_data["coefficient_rows"]) == (
        "17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e"
    )
    base_coefficients = [
        [
            [g(coefficient_data["coefficient_rows"][row][root][column]) for column in range(35)]
            for row in range(65)
        ]
        for root in range(3)
    ]
    base_constants = [
        [g(coefficient_data["coefficient_rows"][row][root][35]) for row in range(65)]
        for root in range(3)
    ]

    base_response_g = [
        [[g(base_responses[root][row, column]) for column in range(79)] for row in range(78)]
        for root in range(4)
    ]
    response_derivative_g = [
        [
            [[g(response_derivatives[tangent][root][row][column][1]) for column in range(79)] for row in range(78)]
            for root in range(4)
        ]
        for tangent in range(4)
    ]
    layer_derivative_g = [
        [
            [g(layer_derivatives[tangent][column][row][1]) for column in range(79)]
            for row in range(81)
        ]
        for tangent in range(4)
    ]
    constant_derivative_g = [
        [[layer_derivative_g[tangent][row][column] for column in constant_indices] for row in mixed_rows]
        for tangent in range(4)
    ]
    constant_g = constant0
    return {
        "tangents": tangent_vectors,
        "centre": centre,
        "leaf": leaf,
        "ports": ports,
        "xi": xi,
        "eta": eta,
        "base_columns": base_columns,
        "base_matrix": base_matrix,
        "particular": particular,
        "raw_kernel": raw_kernel,
        "pivots": pivots,
        "free_columns": free_columns,
        "pivot_rows": pivot_rows,
        "base_response_g": base_response_g,
        "response_derivative_g": response_derivative_g,
        "constant_g": constant_g,
        "layer_derivative_g": layer_derivative_g,
        "constant_derivative_g": constant_derivative_g,
        "constant_pivots": constant_pivots,
        "quotient_rows": quotient_rows,
        "base_coefficients": base_coefficients,
        "base_constants": base_constants,
    }


def check_point(context, name, a, b, sparse_vector):
    raw_kernel = context["raw_kernel"]
    particular = context["particular"]
    pivots = context["pivots"]
    free_columns = context["free_columns"]
    pivot_rows = context["pivot_rows"]
    base_columns = context["base_columns"]
    vector = sp.zeros(35, 1)
    for index, value in sparse_vector.items():
        vector[index] = value
    alpha = raw_kernel * vector
    assert alpha != sp.zeros(79, 1)

    base_coefficients = context["base_coefficients"]
    z0 = gmatvec(base_coefficients[0], [g(value) for value in vector])
    z1 = gmatvec(base_coefficients[1], [g(value) for value in vector])
    z2 = gmatvec(base_coefficients[2], [g(value) for value in vector])
    assert all(value == G73.GZERO for value in gsubv(z1, gscale(a, z0)))
    assert all(value == G73.GZERO for value in gsubv(z2, gscale(b, z0)))
    assert rank_pairs([[z0[row], z1[row], z2[row]] for row in range(65)]) == 1

    alpha_g = [g(alpha[row]) for row in range(79)]
    pivot_matrix_g = [
        [g(base_columns[column][row]) for column in pivots]
        for row in pivot_rows
    ]
    boundary_derivatives = [[None] * 4 for _root in range(4)]
    for tangent in range(4):
        derivative_matrix = context["layer_derivative_g"][tangent]
        pivot_derivative = [
            [derivative_matrix[row][column] for column in pivots]
            for row in pivot_rows
        ]
        free_derivative = [
            [derivative_matrix[row][column] for column in free_columns]
            for row in pivot_rows
        ]
        rhs = gscale(
            -1,
            gaddv(
                gmatvec(pivot_derivative, [alpha_g[column] for column in pivots]),
                gmatvec(free_derivative, [g(value) for value in vector]),
            ),
        )
        d_alpha = [G73.GZERO] * 79
        solved = solve_pairs(pivot_matrix_g, rhs)
        for index, column in enumerate(pivots):
            d_alpha[column] = solved[index]

        for root in range(4):
            h0 = context["base_response_g"][root]
            x0 = gmatvec(h0, alpha_g)
            hd = context["response_derivative_g"][tangent][root]
            xd = gaddv(gmatvec(hd, alpha_g), gmatvec(h0, d_alpha))
            boundary_derivatives[root][tangent] = quotient_derivative(
                x0,
                xd,
                context["constant_g"],
                context["constant_derivative_g"][tangent],
                context["constant_pivots"],
                context["quotient_rows"],
            )

    m1 = gsubm(gscalem(a, base_coefficients[0]), base_coefficients[1])
    m2 = gsubm(gscalem(b, base_coefficients[0]), base_coefficients[2])
    m = m1 + m2
    r1 = gsubv(gscale(a, context["base_constants"][0]), context["base_constants"][1])
    r2 = gsubv(gscale(b, context["base_constants"][0]), context["base_constants"][2])
    r = r1 + r2
    assert all(value == G73.GZERO for value in gmatvec(m, [g(value) for value in vector]))

    survivor_columns = []
    for tangent in range(4):
        d1 = gaddv(
            gscale(a, boundary_derivatives[0][tangent]),
            gscale(-1, boundary_derivatives[1][tangent]),
        )
        d2 = gaddv(
            gscale(b, boundary_derivatives[0][tangent]),
            gscale(-1, boundary_derivatives[2][tangent]),
        )
        survivor_columns.append(d1 + d2)
    slope_a = z0 + [G73.GZERO] * 65
    slope_b = [G73.GZERO] * 65 + z0
    s = [
        m[row]
        + [survivor_columns[tangent][row] for tangent in range(4)]
        + [slope_a[row], slope_b[row]]
        for row in range(130)
    ]
    augmented = [row_s + [row_r] for row_s, row_r in zip(s, r, strict=True)]
    rank_m = rank_pairs(m)
    rank_s = rank_pairs(s)
    rank_augmented = rank_pairs(augmented)
    result = {
        "name": name,
        "chart_ratios": [a, b],
        "raw_support_size": sum(value != 0 for value in vector),
        "rank_M": rank_m,
        "rank_S_130x41": rank_s,
        "rank_augmented_130x42": rank_augmented,
        "rho_nonzero_first_jet_consistent": rank_s == rank_augmented,
        "all_order_exclusion": False,
    }
    return result


def main():
    context = build_context()
    results = [check_point(context, *point) for point in BOUNDARY_POINTS]
    expected = {
        "v_minus": (34, 36, 37),
        "v_plus": (34, 36, 37),
        "v_third": (34, 36, 37),
    }
    computed = {
        result["name"]: (
            result["rank_M"],
            result["rank_S_130x41"],
            result["rank_augmented_130x42"],
        )
        for result in results
    }
    assert computed == expected
    assert all(not result["rho_nonzero_first_jet_consistent"] for result in results)
    print(
        json.dumps(
            {
                "status": "exact_sign_boundary_first_strict_jet_obstruction",
                "global_conjecture": "UNRESOLVED",
                "scope": "three GLD77 sign-plane points over the GLD75 scale-fixed survivor germ",
                "moving_raw_fibre_retained": True,
                "moving_response_quotient_retained": True,
                "slope_variables_retained": True,
                "all_order_exclusion": False,
                "points": results,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
