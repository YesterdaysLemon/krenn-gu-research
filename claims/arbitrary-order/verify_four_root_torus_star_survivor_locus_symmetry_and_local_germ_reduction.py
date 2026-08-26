#!/usr/bin/env python3
"""Verify the fixed-star survivor symmetry and local-germ reduction.

The calculation is exact over Q(i).  It proves the identity component of the
local GL(3)^4 stabilizer of the GLD70 fixed nuisance space is the four factor
scalars, computes the five-dimensional survivor tangent at the GLD72 point,
and checks a bidirectional polynomial certificate showing that the equal-leaf
incidence is smooth of dimension five there.  The result is a local parent
reduction, not a response exclusion on the whole survivor locus.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from itertools import chain, permutations
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD72 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py"
)
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"


def load_gld72():
    spec = importlib.util.spec_from_file_location("gld72_survivor", GLD72)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def local_action(
    parent, tensor: sp.Matrix, mode: int, row: int, column: int
) -> sp.Matrix:
    output = [sp.Integer(0)] * len(parent.LOCAL_INDICES)
    for word in parent.LOCAL_INDICES:
        if word[mode] != row:
            continue
        source = list(word)
        source[mode] = column
        output[parent.LOCAL_INDEX[word]] = tensor[parent.LOCAL_INDEX[tuple(source)]]
    return sp.Matrix(output)


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


def permute_tensor_modes(
    parent, tensor: sp.Matrix, permutation: tuple[int, ...]
) -> sp.Matrix:
    inverse = [0] * 4
    for source, target in enumerate(permutation):
        inverse[target] = source
    return sp.Matrix(
        [
            tensor[parent.LOCAL_INDEX[tuple(word[inverse[mode]] for mode in range(4))]]
            for word in parent.LOCAL_INDICES
        ]
    )


def gauge_incidence(parent, left_relations: sp.Matrix, survivor):
    variables = sp.symbols(
        " ".join(
            [f"c{row}{colour}" for row in range(3) for colour in range(3)]
            + [
                f"l{mode}{row}{colour}"
                for mode in range(1, 4)
                for row in range(1, 3)
                for colour in range(3)
            ]
        )
    )
    centre_symbols = sp.Matrix(3, 3, variables[:9])
    leaf_symbols = []
    offset = 9
    for _mode in range(1, 4):
        leaf = sp.ones(3, 3)
        for row in range(1, 3):
            for colour in range(3):
                leaf[row, colour] = variables[offset]
                offset += 1
        leaf_symbols.append(leaf)
    assert offset == 27
    tensor = sp.Matrix(
        [
            sp.expand(
                sum(
                    centre_symbols[word[0], colour]
                    * sp.prod(
                        leaf_symbols[mode - 1][word[mode], colour]
                        for mode in range(1, 4)
                    )
                    for colour in range(3)
                )
            )
            for word in parent.LOCAL_INDICES
        ]
    )
    equations = [sp.expand(value) for value in left_relations * tensor]
    centre, leaf = survivor.candidate_frames()
    basepoint = list(centre)
    for _mode in range(1, 4):
        basepoint.extend(
            leaf[row, colour] for row in range(1, 3) for colour in range(3)
        )
    substitution = dict(zip(variables, basepoint, strict=True))
    assert all(sp.expand(equation.subs(substitution)) == 0 for equation in equations)
    return variables, equations, basepoint, centre, leaf


def symmetric_shifted_system(variables, equations, basepoint):
    substitutions = {}
    for mode in (2, 3):
        for index in range(6):
            substitutions[variables[9 + 6 * (mode - 1) + index]] = variables[9 + index]
    symmetric = [sp.expand(equation.subs(substitutions)) for equation in equations]
    shifts = sp.symbols("x0:15")
    shifted_at = {
        variable: basepoint[index] + shifts[index]
        for index, variable in enumerate(variables[:15])
    }
    shifted = [sp.expand(equation.subs(shifted_at)) for equation in symmetric]
    zero = {shift: 0 for shift in shifts}
    assert all(sp.expand(equation.subs(zero)) == 0 for equation in shifted)
    return shifts, shifted


def parse_gaussian(raw: str) -> sp.Expr:
    value = sp.expand(sp.sympify(str(raw).replace("^", "**"), locals={"i": sp.I}))
    real, imaginary = value.as_real_imag()
    assert real.is_Rational and imaginary.is_Rational
    return value


def sparse_polynomial(encoded, symbols) -> sp.Poly:
    terms = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        exponent = [0] * len(symbols)
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:
            index = int(raw_index)
            power = int(raw_power)
            assert previous < index < len(symbols) and power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        coefficient = parse_gaussian(raw_coefficient)
        assert coefficient != 0 and key not in terms
        terms[key] = coefficient
    return sp.Poly.from_dict(terms, *symbols, domain=sp.QQ_I)


def certificate_replay(shifts, incidence) -> tuple[int, int, int, int, tuple[int, ...]]:
    raw = CERTIFICATE.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n")
    assert b"\r" not in canonical
    assert hashlib.sha256(canonical).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(canonical)
    assert data["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert data["variable_order"] == [f"x{index}" for index in range(15)]
    assert data["incidence_generator_count"] == len(incidence) == 37
    assert data["basis_generator_count"] == 10
    assert data["forward_shape"] == [37, 10]
    assert data["reverse_shape"] == [10, 37]

    zero = sp.Poly(0, *shifts, domain=sp.QQ_I)
    incidence_polys = [sp.Poly(value, *shifts, domain=sp.QQ_I) for value in incidence]
    basis = [sparse_polynomial(value, shifts) for value in data["basis"]]
    forward = [[zero for _column in range(10)] for _row in range(37)]
    reverse = [[zero for _column in range(37)] for _row in range(10)]
    forward_terms = 0
    reverse_terms = 0
    for entry in data["forward"]:
        row = int(entry["row"])
        column = int(entry["column"])
        assert forward[row][column] == zero
        forward[row][column] = sparse_polynomial(entry["terms"], shifts)
        forward_terms += len(entry["terms"])
    for entry in data["reverse"]:
        row = int(entry["row"])
        column = int(entry["column"])
        assert reverse[row][column] == zero
        reverse[row][column] = sparse_polynomial(entry["terms"], shifts)
        reverse_terms += len(entry["terms"])
    assert (forward_terms, reverse_terms) == (27, 63)

    for column in range(10):
        reconstructed = zero
        for row in range(37):
            reconstructed += incidence_polys[row] * forward[row][column]
        assert reconstructed == basis[column]
    for column in range(37):
        reconstructed = zero
        for row in range(10):
            reconstructed += basis[row] * reverse[row][column]
        assert reconstructed == incidence_polys[column]

    origin = {shift: 0 for shift in shifts}
    jacobian = (
        sp.Matrix([poly.as_expr() for poly in basis]).jacobian(shifts).subs(origin)
    )
    assert jacobian.rank() == 10
    pivot_columns = jacobian.rref()[1]
    free_columns = tuple(column for column in range(15) if column not in pivot_columns)
    assert free_columns == (6, 8, 12, 13, 14)
    return len(canonical), len(basis), forward_terms, reverse_terms, free_columns


def check() -> dict[str, object]:
    survivor = load_gld72()
    gate = survivor.load_gate()
    parent = gate.load_parent()
    xi, eta, ports = parent.canonical_torus_star(1)
    layers = parent.full_q_layer_columns(xi, eta, ports)
    columns = list(chain.from_iterable(layers))
    nuisance = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    nuisance_pivots = nuisance.rref()[1]
    nuisance_basis = nuisance[:, list(nuisance_pivots)]
    left_relations = sp.Matrix.hstack(*nuisance.T.nullspace()).T
    assert nuisance_basis.shape == (81, 44)
    assert left_relations.shape == (37, 81)

    labels = tuple(
        (mode, row, column)
        for mode in range(4)
        for row in range(3)
        for column in range(3)
    )
    stabilizer_columns = []
    for mode, row, column in labels:
        acted = sp.Matrix.hstack(
            *(
                local_action(parent, nuisance_basis[:, basis_column], mode, row, column)
                for basis_column in range(44)
            )
        )
        constrained = left_relations * acted
        stabilizer_columns.append(sp.Matrix(list(constrained)))
    stabilizer_system = sp.Matrix.hstack(*stabilizer_columns)
    stabilizer_lie_basis = stabilizer_system.nullspace()
    scalar_generators = []
    for mode in range(4):
        vector = sp.zeros(36, 1)
        for index in range(3):
            vector[9 * mode + 3 * index + index] = 1
        scalar_generators.append(vector)
    scalar_lie = sp.Matrix.hstack(*scalar_generators)
    stabilizer_lie = sp.Matrix.hstack(*stabilizer_lie_basis)
    assert stabilizer_lie.shape == (36, 4)
    assert stabilizer_lie.row_join(scalar_lie).rank() == 4

    centre, leaf = survivor.candidate_frames()
    tensor = survivor.tensor_from_frames(parent, centre, leaf)
    action_map = sp.Matrix.hstack(
        *(
            local_action(parent, tensor, mode, row, column)
            for mode, row, column in labels
        )
    )
    assert action_map.rank() == 27
    assert len(action_map.nullspace()) == 9
    survivor_preimage = (left_relations * action_map).nullspace()
    survivor_tangent = sp.Matrix.hstack(
        *(action_map * vector for vector in survivor_preimage)
    )
    assert survivor_tangent.rank() == 5
    stabilizer_orbit = action_map * stabilizer_lie
    assert stabilizer_orbit.rank() == 1

    symmetric_columns = [
        local_action(parent, tensor, 0, row, column)
        for row in range(3)
        for column in range(3)
    ]
    symmetric_columns.extend(
        sum(
            (local_action(parent, tensor, mode, row, column) for mode in (1, 2, 3)),
            sp.zeros(81, 1),
        )
        for row in range(3)
        for column in range(3)
    )
    symmetric_action = sp.Matrix.hstack(*symmetric_columns)
    symmetric_preimage = (left_relations * symmetric_action).nullspace()
    symmetric_tangent = sp.Matrix.hstack(
        *(symmetric_action * vector for vector in symmetric_preimage)
    )
    assert symmetric_tangent.rank() == 5

    root_actions = []
    for sigma in permutations(range(3)):
        root_map = sp.zeros(4, 4)
        for source, target in enumerate((*sigma, 3)):
            root_map[target, source] = 1
        assert root_map * sp.Matrix(xi) == sp.Matrix(xi)
        assert root_map * sp.Matrix(eta) == sp.Matrix(eta)
        local_maps = []
        for port in ports:
            port_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in port))
            coordinate_map = port_matrix.gauss_jordan_solve(root_map * port_matrix)[0]
            assert port_matrix * coordinate_map == root_map * port_matrix
            local_maps.append(coordinate_map.T)
        transformed_basis = sp.Matrix.hstack(
            *(
                act_on_tensor(parent, nuisance_basis[:, column], tuple(local_maps))
                for column in range(44)
            )
        )
        assert nuisance_basis.row_join(transformed_basis).rank() == 44
        root_actions.append(tuple(local_maps))
    leaf_permutations = tuple(permutations((1, 2, 3)))
    for leaf_sigma in leaf_permutations:
        mode_permutation = (0, *leaf_sigma)
        transformed_basis = sp.Matrix.hstack(
            *(
                permute_tensor_modes(
                    parent, nuisance_basis[:, column], mode_permutation
                )
                for column in range(44)
            )
        )
        assert nuisance_basis.row_join(transformed_basis).rank() == 44
        assert permute_tensor_modes(parent, tensor, mode_permutation) == tensor
    root_lines = set()
    for maps in root_actions:
        image = act_on_tensor(parent, tensor, maps)
        pivot = next(value for value in image if value != 0)
        root_lines.add(tuple(sp.simplify(value / pivot) for value in image))
    assert len(root_lines) == 6

    variables, equations, basepoint, centre, leaf = gauge_incidence(
        parent, left_relations, survivor
    )
    base_substitution = dict(zip(variables, basepoint, strict=True))
    full_jacobian = sp.Matrix(equations).jacobian(variables).subs(base_substitution)
    assert full_jacobian.rank() == 22
    assert len(full_jacobian.nullspace()) == 5
    shifts, symmetric_incidence = symmetric_shifted_system(
        variables, equations, basepoint
    )
    (
        certificate_bytes,
        basis_count,
        forward_terms,
        reverse_terms,
        free_columns,
    ) = certificate_replay(shifts, symmetric_incidence)
    assert centre.det() == 12 and leaf.det() == -1 - sp.I

    return {
        "status": "exact_local_survivor_germ_reduction_not_response_exclusion",
        "global_conjecture": "UNRESOLVED",
        "fixed_nuisance_shape_rank": [81, 79, nuisance.rank()],
        "ghz_orbit_tangent_dimension": action_map.rank(),
        "ghz_frame_stabilizer_dimension": len(action_map.nullspace()),
        "fixed_nuisance_local_stabilizer_identity_dimension": len(stabilizer_lie_basis),
        "fixed_nuisance_stabilizer_identity_generators": "four factor scalars",
        "interface_orbit_tangent_dimension_at_gld72": stabilizer_orbit.rank(),
        "survivor_tangent_dimension_at_gld72": survivor_tangent.rank(),
        "transverse_survivor_parameters_modulo_scaling": 4,
        "equal_leaf_tangent_dimension": symmetric_tangent.rank(),
        "verified_discrete_interface_symmetries": {
            "root_permutations_fixing_signed_root": len(root_actions),
            "leaf_port_permutations": len(leaf_permutations),
            "gld72_root_permutation_orbit_lines": len(root_lines),
        },
        "gauge_incidence_variables_equations_jacobian_rank": [27, 37, 22],
        "equal_leaf_incidence_variables_basis_jacobian_rank": [15, basis_count, 10],
        "local_survivor_germ_dimension": 5,
        "local_germ_is_smooth_and_equal_leaf_in_this_gauge": True,
        "local_free_shift_coordinates": [f"x{column}" for column in free_columns],
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_bytes": certificate_bytes,
        "certificate_forward_reverse_terms": [forward_terms, reverse_terms],
        "gld72_frame_determinants": [str(centre.det()), str(leaf.det())],
        "gld74_whole_raw_fibre_specialization_retained": True,
        "whole_survivor_locus_response_excluded": False,
    }


def main() -> None:
    result = check()
    print("fixed-star survivor symmetry and local-germ reduction: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
