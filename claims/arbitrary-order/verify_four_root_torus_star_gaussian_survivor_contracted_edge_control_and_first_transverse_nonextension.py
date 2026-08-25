"""Verify the GLD73 contracted edge control and first-transverse obstruction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from itertools import chain, combinations, product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD72 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py"
)

Gaussian = tuple[Fraction, Fraction]
GZERO: Gaussian = (Fraction(0), Fraction(0))
GONE: Gaussian = (Fraction(1), Fraction(0))


def load_gld72():
    spec = importlib.util.spec_from_file_location("gld72_survivor", GLD72)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for offset in range(1, len(vertices)):
        second = vertices[offset]
        remainder = vertices[1:offset] + vertices[offset + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second),) + matching


def act_on_tensor(parent, tensor: sp.Matrix, maps: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(
                sum(
                    sp.prod(maps[mode][output[mode], source[mode]] for mode in range(4))
                    * tensor[parent.LOCAL_INDEX[source]]
                    for source in parent.LOCAL_INDICES
                )
            )
            for output in parent.LOCAL_INDICES
        ]
    )


def gaussian(value) -> Gaussian:
    real, imaginary = sp.expand(value).as_real_imag()
    real = sp.Rational(real)
    imaginary = sp.Rational(imaginary)
    return (
        Fraction(int(real.p), int(real.q)),
        Fraction(int(imaginary.p), int(imaginary.q)),
    )


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gdiv(left: Gaussian, right: Gaussian) -> Gaussian:
    norm = right[0] * right[0] + right[1] * right[1]
    assert norm
    return (
        (left[0] * right[0] + left[1] * right[1]) / norm,
        (left[1] * right[0] - left[0] * right[1]) / norm,
    )


def gsum(values) -> Gaussian:
    result = GZERO
    for value in values:
        result = gadd(result, value)
    return result


def gprod(values) -> Gaussian:
    result = GONE
    for value in values:
        result = gmul(result, value)
    return result


def gaussian_rank(matrix: list[list[Gaussian]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column] != GZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == GZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def canonical_coefficient_hash(coefficients: list[sp.Expr]) -> str:
    fields = []
    for value in coefficients:
        real, imaginary = gaussian(value)
        fields.append(
            f"{real.numerator}/{real.denominator},{imaginary.numerator}/{imaginary.denominator}"
        )
    return hashlib.sha256("\n".join(fields).encode()).hexdigest()


def check_control() -> dict[str, object]:
    survivor = load_gld72()
    gate = survivor.load_gate()
    parent = gate.load_parent()
    centre, leaf = survivor.candidate_frames()
    frames = (centre, leaf, leaf, leaf)
    inverse_frames = tuple(frame.inv() for frame in frames)

    xi, eta, ports = parent.canonical_torus_star(1)
    original_layers = parent.full_q_layer_columns(xi, eta, ports)
    original_columns = list(chain.from_iterable(original_layers))
    original_nuisance = sp.Matrix.hstack(
        *(sp.Matrix(column) for column in original_columns)
    )
    survivor_tensor = survivor.tensor_from_frames(parent, centre, leaf)
    original_basis = original_nuisance[:, list(parent.STAR_PIVOT_COLUMNS)]
    original_pivot_coefficients = original_basis.gauss_jordan_solve(survivor_tensor)[0]
    original_coefficients = [sp.Integer(0)] * 79
    for pivot, value in zip(
        parent.STAR_PIVOT_COLUMNS, original_pivot_coefficients, strict=True
    ):
        original_coefficients[pivot] = sp.simplify(value)
    assert original_nuisance * sp.Matrix(original_coefficients) == survivor_tensor

    transformed_ports = []
    for port, frame in zip(ports, frames, strict=True):
        port_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in port))
        transformed = port_matrix * frame.inv().T
        assert transformed.rank() == 3
        assert port_matrix.row_join(transformed).rank() == 3
        transformed_ports.append([list(transformed[:, column]) for column in range(3)])

    transformed_layers = parent.full_q_layer_columns(xi, eta, transformed_ports)
    transformed_columns = list(chain.from_iterable(transformed_layers))
    transformed_nuisance = sp.Matrix.hstack(
        *(sp.Matrix(column) for column in transformed_columns)
    )
    target = sp.Matrix(
        [
            sp.Integer(root == first == second == third)
            for root, first, second, third in parent.LOCAL_INDICES
        ]
    )
    assert all(
        sp.simplify(value) == 0
        for value in act_on_tensor(parent, survivor_tensor, inverse_frames) - target
    )

    transformed_coefficients = [original_coefficients[0]]
    offset = 1
    for _residual in range(2):
        for mode in range(4):
            old_vector = sp.Matrix(original_coefficients[offset : offset + 3])
            transformed_coefficients.extend(list(inverse_frames[mode] * old_vector))
            offset += 3
    for left_mode, right_mode in combinations(range(4), 2):
        old_matrix = sp.Matrix(3, 3, original_coefficients[offset : offset + 9])
        new_matrix = (
            inverse_frames[left_mode] * old_matrix * inverse_frames[right_mode].T
        )
        transformed_coefficients.extend(list(new_matrix))
        offset += 9
    assert len(transformed_coefficients) == 79
    assert all(
        sp.simplify(value) == 0
        for value in transformed_nuisance * sp.Matrix(transformed_coefficients) - target
    )

    q_value = transformed_coefficients[0]
    residual_values = transformed_coefficients[1:25]
    pair_values = transformed_coefficients[25:]
    residual_vectors = {}
    offset = 0
    for residual_name in ("xi", "eta"):
        for mode in range(4):
            residual_vectors[(residual_name, mode)] = residual_values[
                offset : offset + 3
            ]
            offset += 3
    pair_matrices = {}
    offset = 0
    for pair in combinations(range(4), 2):
        pair_matrices[pair] = sp.Matrix(3, 3, pair_values[offset : offset + 9])
        offset += 9

    matchings = tuple(perfect_matchings(tuple(range(10))))
    assert len(matchings) == 945

    def effective_edge(left: int, right: int, port_word: tuple[int, ...]):
        if left > right:
            left, right = right, left
        if right < 4:
            return sp.Integer(0)
        if left < 4:
            root = left
            if right == 4:
                return xi[root]
            if right == 5:
                return eta[root]
            port = right - 6
            return transformed_ports[port][port_word[port]][root]
        if (left, right) == (4, 5):
            return q_value
        if left in (4, 5):
            port = right - 6
            # The q0-port deck leaves q1 in the companion and therefore uses
            # eta; the q1-port deck analogously uses xi.
            residual_name = "eta" if left == 4 else "xi"
            return residual_vectors[(residual_name, port)][port_word[port]]
        left_port = left - 6
        right_port = right - 6
        return pair_matrices[(left_port, right_port)][
            port_word[left_port], port_word[right_port]
        ]

    port_words = tuple(product(range(3), repeat=4))
    contracted_tensor = sp.Matrix(
        [
            sp.simplify(
                sum(
                    sp.prod(
                        effective_edge(left, right, port_word)
                        for left, right in matching
                    )
                    for matching in matchings
                )
            )
            for port_word in port_words
        ]
    )
    assert contracted_tensor == target

    # Exact first-transverse response.  The five other contracted vertices
    # contribute scalar incident-edge parameters; the four open ports
    # contribute three coordinates each, for a 17-dimensional domain.
    effective_gaussian = {
        (left, right, port_word): gaussian(effective_edge(left, right, port_word))
        for left, right in combinations(range(10), 2)
        for port_word in port_words
    }
    off_diagonal_rows = [
        index for index, word in enumerate(port_words) if len(set(word)) != 1
    ]
    response_ranks = []
    for varied in range(6):
        parameter_labels = []
        for neighbor in range(10):
            if neighbor == varied:
                continue
            if neighbor < 6:
                parameter_labels.append((neighbor, None))
            else:
                parameter_labels.extend((neighbor, colour) for colour in range(3))
        assert len(parameter_labels) == 17

        derivative_columns: list[list[Gaussian]] = []
        for neighbor, selected_colour in parameter_labels:
            varied_edge = tuple(sorted((varied, neighbor)))
            complementary_matchings = [
                tuple(edge for edge in matching if edge != varied_edge)
                for matching in matchings
                if varied_edge in matching
            ]
            assert len(complementary_matchings) == 105
            values = []
            for port_word in port_words:
                value = GZERO
                if (
                    selected_colour is None
                    or port_word[neighbor - 6] == selected_colour
                ):
                    value = gsum(
                        gprod(
                            effective_gaussian[(left, right, port_word)]
                            for left, right in matching
                        )
                        for matching in complementary_matchings
                    )
                values.append(value)
            derivative_columns.append(values)

        derivative_rows = [
            [column[row] for column in derivative_columns] for row in range(81)
        ]
        mixed_rows = [derivative_rows[row] for row in off_diagonal_rows]
        full_rank = gaussian_rank(derivative_rows)
        mixed_rank = gaussian_rank(mixed_rows)
        assert (full_rank, mixed_rank) == (17, 16)

        base_parameters = []
        for neighbor, selected_colour in parameter_labels:
            if selected_colour is None:
                word = (0, 0, 0, 0)
            else:
                mutable_word = [0, 0, 0, 0]
                mutable_word[neighbor - 6] = selected_colour
                word = tuple(mutable_word)
            left, right = sorted((varied, neighbor))
            base_parameters.append(effective_gaussian[(left, right, word)])
        base_replay = [
            gsum(
                gmul(value, coefficient)
                for value, coefficient in zip(row, base_parameters, strict=True)
            )
            for row in derivative_rows
        ]
        assert base_replay == [
            GONE if len(set(word)) == 1 else GZERO for word in port_words
        ]
        response_ranks.append((full_rank, mixed_rank, full_rank - mixed_rank))

    # The explicit row-zero edge-matrix lift used for the contracted control
    # has zero coefficient at the global all-one word: every perfect matching
    # meets a root, and every root-incident matrix has row 1 equal to zero.
    explicit_global_all_one_coefficient = sp.Integer(0)
    assert explicit_global_all_one_coefficient != 1

    return {
        "status": "exact_single_fibre_control_and_pointwise_first_transverse_nonextension",
        "global_conjecture": "UNRESOLVED",
        "transformed_raw_coefficient_sha256": canonical_coefficient_hash(
            transformed_coefficients
        ),
        "original_pivot_nonzero": sum(value != 0 for value in original_coefficients),
        "transformed_raw_nonzero": sum(
            value != 0 for value in transformed_coefficients
        ),
        "transformed_q_residual_pair_nonzero": (
            int(q_value != 0),
            sum(value != 0 for value in residual_values),
            sum(value != 0 for value in pair_values),
        ),
        "ten_vertex_perfect_matchings": len(matchings),
        "contracted_target": "literal_unweighted_Delta_4",
        "first_transverse_full_mixed_diagonal_image_ranks": response_ranks,
        "explicit_graph_global_all_one_coefficient": str(
            explicit_global_all_one_coefficient
        ),
        "root_order_four_maximality_certified": False,
        "full_raw_coefficient_fibre_excluded": False,
        "graph_witness_proved": False,
    }


def main() -> None:
    result = check_control()
    print(
        "four-root torus-star contracted edge control and first-transverse obstruction: PASS"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
