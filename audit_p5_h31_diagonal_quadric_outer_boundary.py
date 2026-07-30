#!/usr/bin/env python3
"""Independent finite-field audit of the second-component outer boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import audit_p5_h31_diagonal_quadric_component_point as BASE


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = ROOT / "verify_p5_h31_diagonal_quadric_outer_boundary.py"
MODULI = (5, 7)
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shifted_beta(alpha, canonical, shifts, modulus):
    return tuple(
        tuple(
            (
                canonical[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            % modulus
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def check_pure(alpha, canonical, expected, modulus) -> None:
    coefficients = {
        word: BASE.permanent_dp(
            [
                list(canonical[mode] if word[mode] else alpha[mode])
                for mode in range(4)
            ],
            modulus,
        )
        for word in WORDS4
    }
    assert coefficients[(1, 1, 1, 1)] == expected % modulus
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word != (1, 1, 1, 1)
    )


def ac_rows(parameter: int, modulus: int):
    e = parameter % modulus
    return (
        (
            (e, -1 % modulus, -1 % modulus, -e % modulus),
            (1, 0, 0, -1 % modulus),
            (0, 1, -1 % modulus, 0),
            (0, 1, 1, 0),
        ),
        (
            (0, -1 % modulus, 1, 0),
            (0, 1, -1 % modulus, 0),
            ((1 + e) % modulus, 1, 1, (1 - e) % modulus),
            (1, 0, 0, 1),
        ),
        4,
    )


def ae_rows(parameter: int, modulus: int):
    c = parameter % modulus
    return (
        (
            (0, (-c - 1) % modulus, (c - 1) % modulus, 0),
            (1, 0, 0, -1 % modulus),
            (0, 1, -1 % modulus, 0),
            (0, 1, 1, 0),
        ),
        (
            (0, -1 % modulus, 1, 0),
            (0, (c + 1) % modulus, (c - 1) % modulus, 0),
            (1, 1, 1, 1),
            (1, 0, 0, 1),
        ),
        4,
    )


def ah_rows(parameter: int, modulus: int):
    c = parameter % modulus
    return (
        (
            (0, -1 % modulus, 1, 0),
            (1, 0, 0, -1 % modulus),
            (0, 1, -1 % modulus, 0),
            (1, 0, 0, 1),
        ),
        (
            (1, -1 % modulus, -1 % modulus, -1 % modulus),
            (0, (c + 1) % modulus, (c - 1) % modulus, 0),
            (1, 1, 1, -1 % modulus),
            (0, 1, 1, 0),
        ),
        -4 * c,
    )


def edge_rows(parameter: int, modulus: int):
    c = parameter % modulus
    return (
        (
            (0, -1 % modulus, 1, 0),
            (1, 0, 0, -1 % modulus),
            (0, 1, -1 % modulus, 0),
            (1, 0, 0, 1),
        ),
        (
            (1, 0, 0, -1 % modulus),
            (0, (c + 1) % modulus, (c - 1) % modulus, 0),
            (1, 0, 0, -1 % modulus),
            (0, 1, 1, 0),
        ),
        -4 * c,
    )


def conic_rows(u: int, v: int, modulus: int):
    u %= modulus
    v %= modulus
    H = u * (u - 2 * v) % modulus
    E = -(v * v - u * v + u * u) % modulus
    F = (v * v - u * u) % modulus
    u0 = (E, -F % modulus, -F % modulus, -E % modulus)
    u1 = (1, 0, 0, 1)
    y1 = (1, 0, 0, -1 % modulus)
    x1 = (1, 1, 1, 1)
    x2 = (
        (H + E) % modulus,
        F,
        F,
        (H - E) % modulus,
    )
    y2 = (0, 1, -1 % modulus, 0)
    k0 = (1, 0, 0, 1)
    k1 = (0, 1, 1, 0)
    alpha0 = tuple(
        (u0[index] + (F + H) * u1[index]) % modulus
        for index in range(4)
    )
    alpha3 = tuple(
        (F * k1[index] - (F + H) * k0[index]) % modulus
        for index in range(4)
    )
    return (
        (alpha0, y1, y2, alpha3),
        (u1, x1, x2, k0),
        4 * F,
        F,
    )


def expected_ac(parameter: int, modulus: int):
    result = {coordinate: set() for coordinate in range(4)}
    if parameter % modulus == 0:
        return result
    for t2 in range(modulus):
        result[1].add((0, 0, t2, 0))
        result[2].add((0, 0, t2, 0))
    for t3 in range(modulus):
        result[1].add((0, 0, 1, t3))
        result[2].add((0, 0, -1 % modulus, t3))
    return result


def expected_ae(parameter: int, modulus: int):
    c = parameter % modulus
    result = {coordinate: set() for coordinate in range(4)}
    if c * c % modulus == 1:
        for q in (0, 3):
            for t2 in range(modulus):
                result[q].add((0, 0, t2, 0))
            for t0 in range(modulus):
                result[q].add((t0, 0, c, 0))
        return result
    if c == 0 or (c * c + 1) % modulus == 0:
        return result
    marking = (
        -c * pow(c * c + 1, -1, modulus) % modulus,
        0,
        pow(c, -1, modulus),
        0,
    )
    result[0].add(marking)
    result[3].add(marking)
    return result


def expected_none(_parameter: int, _modulus: int):
    return {coordinate: set() for coordinate in range(4)}


def expected_edge(_parameter: int, modulus: int):
    result = {coordinate: set() for coordinate in range(4)}
    for q in (0, 3):
        for t1 in range(modulus):
            result[q].add((0, t1, 0, 0))
        for t3 in range(modulus):
            result[q].add((0, 0, 0, t3))
    return result


def expected_conic(label, modulus: int):
    result = {coordinate: set() for coordinate in range(4)}
    if label == "plus":
        inv3 = pow(3, -1, modulus)
        inv4 = pow(4, -1, modulus)
        common = (0, 1, 0, -4 * inv3 % modulus)
        result[1].add(common)
        result[2].add(common)
        result[1].add(
            (
                4 * inv3 % modulus,
                1,
                -3 * inv4 % modulus,
                -4 * inv3 % modulus,
            )
        )
        result[2].add(
            (
                4 * inv3 % modulus,
                1,
                3 * inv4 % modulus,
                -4 * inv3 % modulus,
            )
        )
    elif label == "infinity":
        common = (0, -1 % modulus, 0, 1)
        result[1].update((common, (-1 % modulus, -1 % modulus, 1, 1)))
        result[2].update(
            (common, (-1 % modulus, -1 % modulus, -1 % modulus, 1))
        )
    return result


def actual_survivors(alpha, canonical, modulus: int):
    survivors = {coordinate: set() for coordinate in range(4)}
    marking_points = 0
    for q in range(4):
        for shifts in itertools.product(range(modulus), repeat=4):
            marking_points += 1
            beta = shifted_beta(alpha, canonical, shifts, modulus)
            mixed, diagonal_a, diagonal_b = BASE.extension_system(
                q,
                alpha,
                beta,
                modulus,
            )
            kernel = BASE.nullspace_mod(mixed, modulus)
            if not kernel:
                continue
            if not any(
                BASE.dot(diagonal_a, vector, modulus)
                for vector in kernel
            ):
                continue
            if not any(
                BASE.dot(diagonal_b, vector, modulus)
                for vector in kernel
            ):
                continue
            survivors[q].add(shifts)
    return survivors, marking_points


def stacked_rank(
    distinguished: int,
    mode: int,
    extension,
    alpha,
    beta,
    modulus: int,
) -> int:
    common = [
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    ]
    pure = BASE.one_marked_map(mode, alpha, beta, modulus)
    neighbour = BASE.marked_extension(
        distinguished,
        extension,
        alpha,
        beta,
        mode,
        modulus,
    )
    pure_embedded = [row + [0] for row in pure]
    neighbour_embedded = []
    for row in neighbour:
        embedded = [0] * 5
        for local, global_coordinate in enumerate(common):
            embedded[global_coordinate] = row[local]
        embedded[4] = row[3]
        neighbour_embedded.append(embedded)
    return BASE.matrix_rank_mod(
        pure_embedded + neighbour_embedded,
        modulus,
    )


def audit_survivor_extensions(
    alpha,
    canonical,
    survivors,
    modulus: int,
) -> dict:
    projective_directions = 0
    genuine_extensions = 0
    injective_neighbour_tests = 0
    stacked_injective_tests = 0
    for q in range(4):
        for shifts in sorted(survivors[q]):
            beta = shifted_beta(alpha, canonical, shifts, modulus)
            mixed, diagonal_a, diagonal_b = BASE.extension_system(
                q,
                alpha,
                beta,
                modulus,
            )
            kernel = BASE.nullspace_mod(mixed, modulus)
            assert len(kernel) == 2
            pure_maps = tuple(
                BASE.one_marked_map(mode, alpha, beta, modulus)
                for mode in range(4)
            )
            for coefficients in BASE.projective_vectors(
                len(kernel),
                modulus,
            ):
                projective_directions += 1
                extension = BASE.combine(coefficients, kernel, modulus)
                if not BASE.dot(diagonal_a, extension, modulus):
                    continue
                if not BASE.dot(diagonal_b, extension, modulus):
                    continue
                genuine_extensions += 1
                excluded = False
                for mode in range(4):
                    neighbour = BASE.marked_extension(
                        q,
                        extension,
                        alpha,
                        beta,
                        mode,
                        modulus,
                    )
                    pure_transverse = any(
                        row[q] for row in pure_maps[mode]
                    )
                    if (
                        pure_transverse
                        and BASE.matrix_rank_mod(neighbour, modulus) == 4
                    ):
                        injective_neighbour_tests += 1
                        excluded = True
                        break
                if excluded:
                    continue
                assert any(
                    stacked_rank(
                        q,
                        mode,
                        extension,
                        alpha,
                        beta,
                        modulus,
                    )
                    == 5
                    for mode in range(4)
                )
                stacked_injective_tests += 1
    assert (
        injective_neighbour_tests + stacked_injective_tests
        == genuine_extensions
    )
    return {
        "projective_extension_directions": projective_directions,
        "genuine_binary_extensions": genuine_extensions,
        "injective_neighbour_marked_map_tests": (
            injective_neighbour_tests
        ),
        "stacked_injective_marked_map_tests": stacked_injective_tests,
    }


def audit_family(
    *,
    label: str,
    parameters,
    rows_function,
    expected_function,
    modulus: int,
) -> dict:
    total_marking_points = 0
    total_survivor_markings = 0
    totals = {
        "projective_extension_directions": 0,
        "genuine_binary_extensions": 0,
        "injective_neighbour_marked_map_tests": 0,
        "stacked_injective_marked_map_tests": 0,
    }
    per_parameter_survivors = {}
    for parameter in parameters:
        alpha, canonical, pure = rows_function(parameter, modulus)
        check_pure(alpha, canonical, pure, modulus)
        actual, marking_points = actual_survivors(
            alpha,
            canonical,
            modulus,
        )
        expected = expected_function(parameter, modulus)
        assert actual == expected, (label, modulus, parameter, actual, expected)
        total_marking_points += marking_points
        survivor_count = sum(len(points) for points in actual.values())
        total_survivor_markings += survivor_count
        per_parameter_survivors[str(parameter)] = {
            str(q): len(actual[q]) for q in range(4)
        }
        extension_audit = audit_survivor_extensions(
            alpha,
            canonical,
            actual,
            modulus,
        )
        for key, value in extension_audit.items():
            totals[key] += value
    return {
        "label": label,
        "parameters": len(tuple(parameters)),
        "marking_points": total_marking_points,
        "survivor_markings": total_survivor_markings,
        "survivors_by_parameter": per_parameter_survivors,
        **totals,
    }


def audit_conic(modulus: int) -> dict:
    projective_parameters = [
        ("finite_" + str(parameter), 1, parameter)
        for parameter in range(modulus)
    ] + [("infinity", 0, 1)]
    total_marking_points = 0
    total_survivor_markings = 0
    audited_parameters = 0
    totals = {
        "projective_extension_directions": 0,
        "genuine_binary_extensions": 0,
        "injective_neighbour_marked_map_tests": 0,
        "stacked_injective_marked_map_tests": 0,
    }
    survivors_by_parameter = {}
    inv2 = pow(2, -1, modulus)
    for label, u, v in projective_parameters:
        alpha, canonical, pure, F = conic_rows(u, v, modulus)
        if F == 0:
            # These are the two already-audited FB endpoint fibres,
            # paired exactly with AE by the primary symmetry certificate.
            continue
        audited_parameters += 1
        check_pure(alpha, canonical, pure, modulus)
        actual, marking_points = actual_survivors(
            alpha,
            canonical,
            modulus,
        )
        expected_label = "none"
        if u == 0:
            expected_label = "infinity"
        elif v % modulus == inv2:
            expected_label = "plus"
        expected = expected_conic(expected_label, modulus)
        assert actual == expected, (
            "conic",
            modulus,
            label,
            actual,
            expected,
        )
        total_marking_points += marking_points
        survivor_count = sum(len(points) for points in actual.values())
        total_survivor_markings += survivor_count
        survivors_by_parameter[label] = {
            str(q): len(actual[q]) for q in range(4)
        }
        extension_audit = audit_survivor_extensions(
            alpha,
            canonical,
            actual,
            modulus,
        )
        for key, value in extension_audit.items():
            totals[key] += value
    return {
        "label": "conic",
        "parameters": audited_parameters,
        "excluded_F_zero_endpoints": 2,
        "marking_points": total_marking_points,
        "survivor_markings": total_survivor_markings,
        "survivors_by_parameter": survivors_by_parameter,
        **totals,
    }


def audit_modulus(modulus: int) -> dict:
    families = [
        audit_family(
            label="AC",
            parameters=tuple(range(modulus)),
            rows_function=ac_rows,
            expected_function=expected_ac,
            modulus=modulus,
        ),
        audit_family(
            label="AE",
            parameters=tuple(range(modulus)),
            rows_function=ae_rows,
            expected_function=expected_ae,
            modulus=modulus,
        ),
        audit_family(
            label="AH",
            parameters=tuple(range(1, modulus)),
            rows_function=ah_rows,
            expected_function=expected_none,
            modulus=modulus,
        ),
        audit_family(
            label="edge",
            parameters=tuple(range(1, modulus)),
            rows_function=edge_rows,
            expected_function=expected_edge,
            modulus=modulus,
        ),
        audit_conic(modulus),
    ]
    return {
        "modulus": modulus,
        "families": families,
        "marking_points": sum(
            family["marking_points"] for family in families
        ),
        "survivor_markings": sum(
            family["survivor_markings"] for family in families
        ),
        "projective_extension_directions": sum(
            family["projective_extension_directions"]
            for family in families
        ),
        "genuine_binary_extensions": sum(
            family["genuine_binary_extensions"] for family in families
        ),
        "injective_neighbour_marked_map_tests": sum(
            family["injective_neighbour_marked_map_tests"]
            for family in families
        ),
        "stacked_injective_marked_map_tests": sum(
            family["stacked_injective_marked_map_tests"]
            for family in families
        ),
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "one-parameter boundary marking enumeration, independent "
            "dynamic-programming permanent, modular kernel directions, "
            "and neighbouring-or-stacked marked-map ranks"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "total_marking_points": sum(
            audit["marking_points"] for audit in audits
        ),
        "total_survivor_markings": sum(
            audit["survivor_markings"] for audit in audits
        ),
        "total_projective_extension_directions": sum(
            audit["projective_extension_directions"]
            for audit in audits
        ),
        "total_genuine_binary_extensions": sum(
            audit["genuine_binary_extensions"] for audit in audits
        ),
        "total_injective_neighbour_marked_map_tests": sum(
            audit["injective_neighbour_marked_map_tests"]
            for audit in audits
        ),
        "total_stacked_injective_marked_map_tests": sum(
            audit["stacked_injective_marked_map_tests"]
            for audit in audits
        ),
        "all_actual_survivors_match_relative_projection_strata": True,
        "all_genuine_extensions_ternarily_excluded": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_h31_diagonal_quadric_outer_boundary_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
