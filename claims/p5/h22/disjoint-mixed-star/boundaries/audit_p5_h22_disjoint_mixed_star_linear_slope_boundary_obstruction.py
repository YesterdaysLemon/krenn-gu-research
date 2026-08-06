#!/usr/bin/env python3
"""Independent modular audit of three linear-slope H22 boundaries.

The finite-field census is corroboration only, not a proof over C.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import audit_p5_h31_disjoint_mixed_star_component_generic_obstruction as A
from audit_p5_h31_marked_basis_open_branch import rank_mod
import explore_p5_h22_disjoint_mixed_star_modular as E


ROOT = Path(__file__).resolve().parent
SAMPLES = (
    (11, (1, 2, 7, 3)),
    (13, (1, 3, 5, 10)),
)
EXPECTED_COUNTS = {
    (11, "source_plus", "01"): 0,
    (11, "source_plus", "23"): 10,
    (11, "source_minus", "01"): 5,
    (11, "source_minus", "23"): 10,
    (11, "basis_ratio", "01"): 4,
    (11, "basis_ratio", "23"): 10,
    (13, "source_plus", "01"): 0,
    (13, "source_plus", "23"): 12,
    (13, "source_minus", "01"): 5,
    (13, "source_minus", "23"): 12,
    (13, "basis_ratio", "01"): 4,
    (13, "basis_ratio", "23"): 12,
}


def component_basis(parameters, modulus):
    a, b, f, phi = parameters
    p = modulus
    j = (f + b * phi * phi) % p
    kappa = phi * (b * f + 1) % p
    eta = -(b * f + 1) % p
    alpha = (
        (0, 0, 1, -1),
        (-a * f + 1, -a * f - 1, f + phi, f - phi),
        (
            -a * j + eta,
            -a * j - eta,
            j + kappa,
            j - kappa,
        ),
        (1, -1, 0, 0),
    )
    beta = (
        (a + b, a - b, 0, 2),
        (1, 1, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    alpha = tuple(
        tuple(value % p for value in row) for row in alpha
    )
    beta = tuple(tuple(value % p for value in row) for row in beta)
    relation = (
        a * a * b * f * phi * phi
        + a * a * f * f
        - b * b * f * f
        + b * b * phi * phi
        - b * f
        - 1
    ) % p
    assert relation == 0
    assert all(
        A.rref_nullspace(plane, p)[0] == 2
        for plane in (
            alpha[0:1] + beta[0:1],
            alpha[1:2] + beta[1:2],
            alpha[2:3] + beta[2:3],
            alpha[3:4] + beta[3:4],
        )
    )
    return alpha, beta


def slope_value(graph: str, parameters, modulus: int) -> int:
    a, b, f, _phi = parameters
    if graph == "source_plus":
        numerator, denominator = -(a - b), a + b
    elif graph == "source_minus":
        numerator, denominator = a - b, a + b
    elif graph == "basis_ratio":
        numerator, denominator = -(a * f + 1), a * f - 1
    else:
        raise ValueError(graph)
    assert denominator % modulus
    return numerator * pow(denominator, -1, modulus) % modulus


def audit_case(
    modulus: int,
    parameters,
    graph: str,
    direction: str,
) -> dict[str, object]:
    alpha, canonical_beta = component_basis(
        parameters, modulus
    )
    slope = slope_value(graph, parameters, modulus)
    mode = 1 if graph == "basis_ratio" and direction == "01" else 0
    minor_rows = (
        ((0, 4, 5, 7),)
        if mode == 1
        else ((0, 1, 3, 7), (0, 1, 5, 7))
    )
    genuine_markings = 0
    genuine_directions = 0
    rank_four_directions = 0
    for shifts in itertools.product(range(modulus), repeat=4):
        beta = tuple(
            tuple(
                (
                    canonical_beta[local_mode][coordinate]
                    + shifts[local_mode]
                    * alpha[local_mode][coordinate]
                )
                % modulus
                for coordinate in range(4)
            )
            for local_mode in range(4)
        )
        mixed, first, second = E.matrices(
            alpha,
            beta,
            direction,
            slope,
            modulus,
        )
        _rank, kernel = A.rref_nullspace(mixed, modulus)
        local_genuine = 0
        for projective in A.projective_directions(
            len(kernel), modulus
        ):
            extension = A.combine(projective, kernel, modulus)
            if not (
                A.dot(first, extension, modulus)
                and A.dot(second, extension, modulus)
            ):
                continue
            local_genuine += 1
            genuine_directions += 1
            _values, alpha_d, beta_d = E.coefficients(
                alpha,
                beta,
                direction,
                slope,
                extension,
                modulus,
            )
            marked = A.one_marked_map(
                mode,
                alpha_d,
                beta_d,
                modulus,
            )
            minors = tuple(
                A.determinant_mod(
                    [
                        [
                            marked[row][column]
                            for column in range(4)
                        ]
                        for row in rows
                    ],
                    modulus,
                )
                for rows in minor_rows
            )
            assert any(minors), (
                modulus,
                graph,
                direction,
                shifts,
                extension,
                minors,
            )
            assert rank_mod(marked, modulus) == 4
            rank_four_directions += 1
        if local_genuine:
            genuine_markings += 1
    expected = EXPECTED_COUNTS[(modulus, graph, direction)]
    assert genuine_directions == expected
    assert rank_four_directions == genuine_directions
    return {
        "modulus": modulus,
        "component_point": list(parameters),
        "graph": graph,
        "direction": direction,
        "slope": slope,
        "marked_mode": mode,
        "minor_rows": [list(rows) for rows in minor_rows],
        "markings": modulus**4,
        "genuine_markings": genuine_markings,
        "genuine_projective_directions": genuine_directions,
        "rank_four_projective_directions": rank_four_directions,
    }


def main() -> None:
    cases = [
        audit_case(modulus, parameters, graph, direction)
        for modulus, parameters in SAMPLES
        for graph in ("source_plus", "source_minus", "basis_ratio")
        for direction in ("01", "23")
    ]
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "cases": cases,
        "audited": True,
    }
    output = (
        ROOT
        / "tmp"
        / "p5_h22_disjoint_mixed_star_linear_slope_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
