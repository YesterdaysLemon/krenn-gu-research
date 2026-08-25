"""Verify the GLD74 full-coefficient-fibre first-response obstruction.

The proof is exact over Q(i).  It reconstructs the GLD72 transformed
79-column map, parametrizes its full 35-dimensional fibre over Delta_4,
forms the complete q0 legal-response span, and replays two sparse
Nullstellensatz certificates plus the remaining coordinate direction.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from itertools import chain, combinations, product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD73 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py"
)
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension_certificates.json"
)
CERTIFICATE_SHA256 = "7bb2dc47270a2c2e9b87c722aace298e63a6691a7979d86564425aac760a748f"

PARAMETERS = tuple(f"t{index}" for index in range(35))
VARIABLES = (*PARAMETERS, "a", "b")
SYMBOLS = sp.symbols(" ".join(VARIABLES))
T_SYMBOLS = SYMBOLS[:35]
A_SYMBOL = SYMBOLS[35]
B_SYMBOL = SYMBOLS[36]


def load_gld73():
    spec = importlib.util.spec_from_file_location("gld73_control", GLD73)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transformed_map():
    """Return the exact GLD72 map in literal-Delta coordinates."""

    gld73 = load_gld73()
    survivor = gld73.load_gld72()
    gate = survivor.load_gate()
    parent = gate.load_parent()
    centre, leaf = survivor.candidate_frames()
    frames = (centre, leaf, leaf, leaf)
    xi, eta, ports = parent.canonical_torus_star(1)

    transformed_ports = []
    for port, frame in zip(ports, frames, strict=True):
        port_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in port))
        transformed = port_matrix * frame.inv().T
        assert transformed.rank() == 3
        transformed_ports.append([list(transformed[:, column]) for column in range(3)])

    layers = parent.full_q_layer_columns(xi, eta, transformed_ports)
    columns = list(chain.from_iterable(layers))
    matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    target = sp.Matrix(
        [
            sp.Integer(root == first == second == third)
            for root, first, second, third in parent.LOCAL_INDICES
        ]
    )
    assert matrix.shape == (81, 79)
    return gld73, xi, eta, transformed_ports, columns, target


def affine_fibre(gld73, columns, target: sp.Matrix):
    """Parametrize the full fibre by one exact Q(i) row reduction."""

    gaussian_columns = [
        [gld73.gaussian(value) for value in column] for column in columns
    ]
    gaussian_target = [gld73.gaussian(value) for value in target]
    work = [
        [gaussian_columns[column][row] for column in range(79)] + [gaussian_target[row]]
        for row in range(81)
    ]
    pivot_row = 0
    pivots = []
    for column in range(79):
        pivot = next(
            (row for row in range(pivot_row, 81) if work[row][column] != gld73.GZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gld73.gdiv(value, scale) for value in work[pivot_row]]
        for row in range(81):
            if row == pivot_row or work[row][column] == gld73.GZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gld73.gsub(value, gld73.gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
    assert len(pivots) == 44
    assert all(work[row][-1] == gld73.GZERO for row in range(pivot_row, 81))

    pivot_set = set(pivots)
    free = tuple(column for column in range(79) if column not in pivot_set)
    assert len(free) == 35
    particular_gaussian = [gld73.GZERO] * 79
    kernel_gaussian = [[gld73.GZERO] * 35 for _ in range(79)]
    for row, pivot in enumerate(pivots):
        particular_gaussian[pivot] = work[row][-1]
        for parameter, free_column in enumerate(free):
            kernel_gaussian[pivot][parameter] = gld73.gsub(
                gld73.GZERO, work[row][free_column]
            )
    for parameter, free_column in enumerate(free):
        kernel_gaussian[free_column][parameter] = gld73.GONE

    assert all(
        gld73.gsum(
            gld73.gmul(gaussian_columns[column][row], particular_gaussian[column])
            for column in range(79)
        )
        == gaussian_target[row]
        for row in range(81)
    )
    for parameter in range(35):
        assert all(
            gld73.gsum(
                gld73.gmul(
                    gaussian_columns[column][row],
                    kernel_gaussian[column][parameter],
                )
                for column in range(79)
            )
            == gld73.GZERO
            for row in range(81)
        )

    def sympy_gaussian(value):
        real, imaginary = value
        return sp.Rational(real.numerator, real.denominator) + sp.I * sp.Rational(
            imaginary.numerator, imaginary.denominator
        )

    particular = sp.Matrix([sympy_gaussian(value) for value in particular_gaussian])
    kernel = sp.Matrix(
        [[sympy_gaussian(value) for value in row] for row in kernel_gaussian]
    )
    return particular, kernel, tuple(pivots), free


def q0_response_context(gld73, eta, transformed_ports):
    mixed_words = tuple(
        word for word in product(range(3), repeat=4) if len(set(word)) != 1
    )
    matchings = tuple(gld73.perfect_matchings(tuple(range(10))))
    eta_gaussian = [gld73.gaussian(value) for value in eta]
    port_gaussian = [
        [[gld73.gaussian(value) for value in column] for column in port]
        for port in transformed_ports
    ]
    pair_offset = {pair: index for index, pair in enumerate(combinations(range(4), 2))}

    def sympy_gaussian(value):
        real, imaginary = value
        return sp.Rational(real.numerator, real.denominator) + sp.I * sp.Rational(
            imaginary.numerator, imaginary.denominator
        )

    response_maps = []
    for root in range(4):
        varied_edge = (root, 4)
        root_matchings = tuple(
            matching for matching in matchings if varied_edge in matching
        )
        assert len(root_matchings) == 105
        rows = []
        for word in mixed_words:
            row = [gld73.GZERO] * 79
            for matching in root_matchings:
                complement = tuple(edge for edge in matching if edge != varied_edge)
                if any(right < 4 for _left, right in complement):
                    # A surviving root--root edge has base value zero.
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
                fixed_weight = gld73.gprod(
                    eta_gaussian[left_root]
                    if right_vertex == 5
                    else port_gaussian[right_vertex - 6][word[right_vertex - 6]][
                        left_root
                    ]
                    for left_root, right_vertex in complement
                    if left_root < 4
                )
                row[raw_index] = gld73.gadd(row[raw_index], fixed_weight)
            rows.append([sympy_gaussian(value) for value in row])
        response_maps.append(sp.Matrix(rows))
    assert all(response.shape == (78, 79) for response in response_maps)
    return response_maps


def quotient_forms():
    """Construct the 65-by-3 affine quotient matrix Z(t)."""

    (
        gld73,
        xi,
        eta,
        transformed_ports,
        columns,
        target,
    ) = transformed_map()
    # The port-frame change mixes raw labels inside the 79-column
    # presentation, so recompute this presentation's pivot set rather than
    # reusing the original-coordinate GLD70 indices.
    particular, kernel, pivots, free = affine_fibre(gld73, columns, target)

    mixed_rows = [
        row
        for row, word in enumerate(product(range(3), repeat=4))
        if len(set(word)) != 1
    ]
    # At q0, the q0--q1 cofactor is Q and the twelve q0--port cofactors
    # are the eta residual layer.  These thirteen columns are independent.
    constant_columns = [columns[0], *columns[13:25]]
    constant = sp.Matrix(
        [[column[row] for column in constant_columns] for row in mixed_rows]
    )
    assert constant.shape == (78, 13)
    assert constant.rank() == 13
    pivot_rows = tuple(constant.T.rref()[1])
    assert len(pivot_rows) == 13
    pivot_row_set = set(pivot_rows)
    quotient_rows = tuple(row for row in range(78) if row not in pivot_row_set)
    assert len(quotient_rows) == 65
    pivot_inverse = constant[list(pivot_rows), :].inv()

    correction = constant[list(quotient_rows), :] * pivot_inverse
    assert tuple(xi) == (1, 1, 1, -1)
    response_maps = q0_response_context(gld73, eta, transformed_ports)
    affine_coefficients = particular.row_join(kernel)
    projected_affine = []
    for response_map in response_maps:
        response = response_map * affine_coefficients
        projected_affine.append(
            response[list(quotient_rows), :]
            - correction * response[list(pivot_rows), :]
        )
    relation = (
        projected_affine[0]
        + projected_affine[1]
        + projected_affine[2]
        - projected_affine[3]
    )
    assert all(sp.expand(value) == 0 for value in relation)

    forms = []
    coefficient_rows = []
    for row in range(65):
        form_row = []
        coefficient_row = []
        for column in range(3):
            coefficients = list(projected_affine[column][row, 1:])
            constant_value = projected_affine[column][row, 0]
            coefficient_row.append([*coefficients, constant_value])
            form_row.append(
                sp.expand(
                    constant_value
                    + sum(
                        (
                            coefficient * variable
                            for coefficient, variable in zip(
                                coefficients, T_SYMBOLS, strict=True
                            )
                        ),
                        sp.Integer(0),
                    )
                )
            )
        forms.append(form_row)
        coefficient_rows.append(coefficient_row)

    return {
        "forms": forms,
        "coefficient_rows": coefficient_rows,
        "map_rank": len(pivots),
        "pivots": pivots,
        "free": free,
        "constant_rank": constant.rank(),
        "constant_full_rank": sp.Matrix.hstack(
            *(sp.Matrix(column) for column in constant_columns)
        ).rank(),
        "quotient_rows": quotient_rows,
    }


def polynomial_systems(forms):
    chart = []
    d0_chart = []
    for z0, z1, z2 in forms:
        chart.extend((sp.expand(A_SYMBOL * z0 - z1), sp.expand(B_SYMBOL * z0 - z2)))
        d0_chart.extend((z0, sp.expand(B_SYMBOL * z1 - z2)))
    assert len(chart) == len(d0_chart) == 130
    return {"z0_nonzero": chart, "z0_zero_z1_nonzero": d0_chart}


def parse_gaussian(raw: str) -> sp.Expr:
    value = sp.expand(sp.sympify(raw.replace("^", "**"), locals={"i": sp.I}))
    real, imaginary = value.as_real_imag()
    assert real.is_Rational and imaginary.is_Rational
    return value


def multiplier_poly(encoded) -> sp.Poly:
    terms = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        coefficient = parse_gaussian(str(raw_coefficient))
        exponent = [0] * len(VARIABLES)
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:
            index = int(raw_index)
            power = int(raw_power)
            assert previous < index < len(VARIABLES) and power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        assert coefficient != 0 and key not in terms
        terms[key] = coefficient
    return sp.Poly.from_dict(terms, *SYMBOLS, domain=sp.QQ_I)


def certificate_replay(systems) -> tuple[int, dict[str, int]]:
    raw = CERTIFICATE.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n")
    assert b"\r" not in canonical
    assert hashlib.sha256(canonical).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(canonical)
    assert data["format"] == "sparse-nullstellensatz-Qi-v1"
    assert tuple(data["variable_order"]) == VARIABLES
    assert data["generator_order"] == "quotient_row_then_equation"
    assert set(data["charts"]) == set(systems)

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ_I)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ_I)
    term_counts = {}
    for chart_name, expressions in systems.items():
        generators = [
            sp.Poly(expression, *SYMBOLS, domain=sp.QQ_I) for expression in expressions
        ]
        multipliers = data["charts"][chart_name]
        assert len(generators) == len(multipliers) == 130
        total = zero
        term_counts[chart_name] = 0
        for generator, encoded in zip(generators, multipliers, strict=True):
            term_counts[chart_name] += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, chart_name
    return len(canonical), term_counts


def coefficient_fingerprint(coefficient_rows) -> str:
    fields = []
    for row in coefficient_rows:
        for column in row:
            for value in column:
                real, imaginary = sp.expand(value).as_real_imag()
                real = sp.Rational(real)
                imaginary = sp.Rational(imaginary)
                fields.append(f"{real.p}/{real.q},{imaginary.p}/{imaginary.q}")
    return hashlib.sha256("\n".join(fields).encode()).hexdigest()


def check() -> dict[str, object]:
    data = quotient_forms()
    systems = polynomial_systems(data["forms"])
    certificate_bytes, term_counts = certificate_replay(systems)

    point_rows = [
        data["coefficient_rows"][row][column] for row in range(65) for column in (0, 1)
    ]
    gld73 = load_gld73()
    gaussian_rows = [
        [gld73.gaussian(sp.expand(value)) for value in row] for row in point_rows
    ]
    coefficient_rank = gld73.gaussian_rank([row[:35] for row in gaussian_rows])
    augmented_rank = gld73.gaussian_rank(gaussian_rows)
    assert (coefficient_rank, augmented_rank) == (35, 36)

    return {
        "status": "exact_full_coefficient_fibre_first_response_nonextension",
        "global_conjecture": "UNRESOLVED",
        "transformed_permanent_map_shape": [81, 79],
        "transformed_permanent_map_rank": data["map_rank"],
        "affine_fibre_dimension": len(data["free"]),
        "q0_constant_full_mixed_ranks": [
            data["constant_full_rank"],
            data["constant_rank"],
        ],
        "q0_quotient_matrix_shape": [65, 3],
        "rank_at_most_one_projective_cover": [
            "z0_nonzero",
            "z0_zero_z1_nonzero",
            "z0_equals_z1_equals_zero",
        ],
        "nullstellensatz_multiplier_terms": term_counts,
        "coordinate_direction_coefficient_augmented_ranks": [
            coefficient_rank,
            augmented_rank,
        ],
        "quotient_affine_coefficient_sha256": coefficient_fingerprint(
            data["coefficient_rows"]
        ),
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_bytes": certificate_bytes,
        "full_raw_coefficient_fibre_excluded_at_q0_first_response": True,
        "whole_ghz_survivor_locus_excluded": False,
        "root_order_four_maximality_certified": False,
        "fifth_root_excluded": False,
        "graph_witness_proved": False,
    }


def main() -> None:
    result = check()
    print("GLD74 full coefficient-fibre first-response obstruction: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
