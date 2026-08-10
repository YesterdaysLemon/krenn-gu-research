#!/usr/bin/env python3
"""Exact partial weighted-H22 obstruction for component twenty-five."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-endpoint-inward-star")

from verify_p5_h31_marked_basis_open_branch import mixed_matrix, permanent
from verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction import (
    marked,
    pure_basis,
    quotient_row_module,
)



WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def contract(row, extension, direction, chart, slope=None):
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def coordinates(alpha, beta, extensions, direction, chart, slope=None):
    alpha_rows = tuple(
        contract(alpha[index], extensions[index], direction, chart, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        contract(beta[index], extensions[4 + index], direction, chart, slope)
        for index in range(4)
    )
    return {
        word: permanent(
            tuple(
                beta_rows[index] if word[index] else alpha_rows[index]
                for index in range(4)
            )
        )
        for word in WORDS
    }


def coefficient_rows(tensor, extensions):
    mixed = sp.Matrix(
        [
            [sp.diff(tensor[word], extension) for extension in extensions]
            for word in MIXED
        ]
    )
    diagonal_alpha = sp.Matrix(
        [[sp.diff(tensor[WORDS[0]], extension) for extension in extensions]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(tensor[WORDS[-1]], extension) for extension in extensions]]
    )
    return mixed, diagonal_alpha, diagonal_beta


def finite_d01_dense_obstruction(alpha, beta, extensions, slope, e, j, k):
    tensor = coordinates(alpha, beta, extensions, "D01", "finite", slope)
    pivot = e * j + k**2
    cross = e + j
    linear_factor = sp.expand((slope + 1) * extensions[2] + (slope - 1) * extensions[4])
    identities = {
        "C1101": tensor[(1, 1, 0, 1)],
        "C1000_minus_Q_C1100": sp.expand(
            tensor[(1, 0, 0, 0)] - cross * tensor[(1, 1, 0, 0)]
        ),
        "k_C1001_minus_jP_C1100": sp.expand(
            k * tensor[(1, 0, 0, 1)] - j * pivot * tensor[(1, 1, 0, 0)]
        ),
        "C1100_plus_2kL": sp.expand(tensor[(1, 1, 0, 0)] + 2 * k * linear_factor),
    }
    assert all(sp.factor(value) == 0 for value in identities.values())

    # On C_empty=1, the three fixed-vertex Segre equations for subsets
    # {0,1}, {0,3}, and {0,1,3} have no solution when C1100 is nonzero.
    t, c1, c3, inverse = sp.symbols("t c1 c3 inverse")
    equations = (
        sp.expand(t - cross * t * c1),
        sp.expand(j * pivot * t - k * cross * t * c3),
        sp.expand(cross * t * c1 * c3),
        sp.expand(inverse * t - 1),
    )
    domain = sp.QQ.frac_field(e, j, k)
    basis = sp.groebner(equations, inverse, t, c1, c3, domain=domain)
    assert list(basis) == [1]
    return {
        "direction": "D01",
        "weight_chart": "finite",
        "linear_extension_factor": str(linear_factor),
        "uniform_in_weight": True,
        "excluded_subchart": "L01 != 0",
        "residual_subchart": "L01 = 0",
        "fixed_vertex_join_unit_ideal_on_excluded_subchart": True,
    }


def infinity_obstruction(
    direction, distinguished, alpha, active, extensions, hypersurface
):
    tensor = coordinates(alpha, active, extensions, direction, "infinity")
    weighted_rows = coefficient_rows(tensor, extensions)
    deleted_rows = mixed_matrix(distinguished, alpha, active)
    assert all(
        sp.factor(value) == 0
        for weighted, deleted in zip(weighted_rows, deleted_rows, strict=True)
        for value in weighted - deleted
    )
    module = quotient_row_module(distinguished, alpha, active, hypersurface)
    assert module["all_alpha_in_mixed_module"]
    return {
        "direction": direction,
        "weight_chart": "infinity",
        "identified_H31_deleted_coordinate": distinguished,
        "all_alpha_in_mixed_module": True,
        "all_beta_in_mixed_module": False,
        "module_basis_size": module["module_basis_size"],
        "binary_incidence_empty": True,
    }


def main():
    started = time.perf_counter()
    e, j, k, s, slope = sp.symbols("e j k s lambda")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    pivot = e * j + k**2
    hypersurface = sp.expand(pivot * (1 + e * j * s**2) - (e + j) ** 2)
    alpha, beta = pure_basis(e, j, k, s)

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(0, 0, 1, 1)] - 4 * pivot * hypersurface) == 0
    assert sp.factor(pure[WORDS[-1]] - 4 * pivot) == 0
    assert all(
        value == 0
        for word, value in pure.items()
        if word not in ((0, 0, 1, 1), WORDS[-1])
    )

    finite = finite_d01_dense_obstruction(alpha, beta, extensions, slope, e, j, k)
    active = marked(alpha, beta, shifts)
    infinity = (
        infinity_obstruction("D01", 1, alpha, active, extensions, hypersurface),
        infinity_obstruction("D23", 3, alpha, active, extensions, hypersurface),
    )
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_residual",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pure_support_mod_F": {"1111": str(4 * pivot)},
                "finite_D01_dense_obstruction": finite,
                "weight_infinity_obstructions": infinity,
                "finite_D01_residual_closed": False,
                "finite_D23_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "special_component_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
