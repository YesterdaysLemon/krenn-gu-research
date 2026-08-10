#!/usr/bin/env python3
"""Generate exact marked-fibre incidences on the 21 toric H31 cases."""

from __future__ import annotations

import argparse
import itertools
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path

import sys

import sympy as sp


for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p4/classifications/pair-geometry/pure-rank-two")

from krenn_gu.singular_runtime import (
    singular_command_with_timeout,
)
from verify_p4_pure_rank_two_toric_slice_segre import (  # noqa: E402
    add,
    affine_rank,
    classify_slice,
    cross,
    dot,
    plane_from_pluecker,
    segre_equations,
    slice_map,
    subtract,
)
from krenn_gu.p5_marked_basis import mixed_matrix


CONFIGURATIONS = (
    {
        "02": ((1, 0, 0), 1),
        "03": ((1, 1, 0), 1),
        "12": ((0, 0, 0), 1),
        "13": ((0, 1, 0), 1),
    },
    {
        "01": ((0, 0, -1), 1),
        "03": ((1, 1, 0), 1),
        "12": ((0, 0, 0), 1),
        "23": ((1, 1, 1), -1),
    },
    {
        "02": ((0, -1, 0), -1),
        "03": ((0, 0, 0), 1),
        "23": ((0, 0, 1), 1),
    },
)
DELETION_COORDINATES = (
    {"12", "13", "23"},
    {"02", "03", "23"},
    {"01", "03", "13"},
    {"01", "02", "12"},
)


@dataclass(frozen=True)
class ToricCase:
    case_id: int
    dimension: int
    incident_normals: tuple[tuple[int, int, int], ...]
    pure_direction: tuple[sp.Expr, sp.Expr]
    multiplicity: int
    all_rank: tuple[int, ...]
    kernel: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]
    pure_lift: tuple[sp.Expr, ...]
    base_alpha: tuple[tuple[sp.Expr, ...], ...]
    base_beta: tuple[tuple[sp.Expr, ...], ...]


def facet_data() -> tuple[
    tuple[tuple[int, int, int], ...],
    dict[tuple[int, int, int], frozenset[tuple[int, int, int]]],
]:
    points = tuple(sorted({
        add(first[0], second[0], third[0])
        for first in CONFIGURATIONS[0].values()
        for second in CONFIGURATIONS[1].values()
        for third in CONFIGURATIONS[2].values()
    }))
    facets: dict[
        tuple[int, int, int],
        frozenset[tuple[int, int, int]],
    ] = {}
    for first, second, third in itertools.combinations(points, 3):
        normal = cross(
            subtract(second, first),
            subtract(third, first),
        )
        if normal == (0, 0, 0):
            continue
        relative = [
            dot(normal, subtract(point, first))
            for point in points
        ]
        if not (
            all(value >= 0 for value in relative)
            or all(value <= 0 for value in relative)
        ):
            continue
        if all(value >= 0 for value in relative):
            normal = tuple(-entry for entry in normal)
        divisor = math.gcd(*(abs(entry) for entry in normal if entry))
        normal = tuple(entry // divisor for entry in normal)
        offset = dot(normal, first)
        facets[normal] = frozenset(
            point for point in points if dot(normal, point) == offset
        )
    return points, facets


def pure_factors(
    tensor: sp.Matrix,
) -> tuple[tuple[sp.Expr, sp.Expr], ...]:
    values = tuple(map(sp.factor, tensor))
    index = next(i for i, value in enumerate(values) if value != 0)
    bits = ((index >> 2) & 1, (index >> 1) & 1, index & 1)
    base = values[index]
    factors = []
    for mode, bit in enumerate(bits):
        flipped = index ^ (1 << (2 - mode))
        ratio = sp.factor(values[flipped] / base)
        factor = [sp.Integer(0), sp.Integer(0)]
        factor[bit] = sp.Integer(1)
        factor[1 - bit] = ratio
        factors.append(tuple(factor))
    for target in range(8):
        target_bits = (
            (target >> 2) & 1,
            (target >> 1) & 1,
            target & 1,
        )
        expected = base * sp.prod(
            factors[mode][target_bits[mode]]
            for mode in range(3)
        )
        assert sp.factor(values[target] - expected) == 0
    return tuple(factors)


def toric_cases(
    include_internal_e0: bool = False,
) -> tuple[ToricCase, ...]:
    points, facets = facet_data()
    faces: dict[int, set[frozenset[tuple[int, int, int]]]] = {
        2: set(facets.values()),
        1: set(),
    }
    for first, second in itertools.combinations(facets.values(), 2):
        intersection = first & second
        if intersection and affine_rank(intersection) == 1:
            faces[1].add(frozenset(intersection))

    raw_cases = []
    for dimension in (2, 1):
        for face in faces[dimension]:
            incident = tuple(sorted(
                normal
                for normal, facet in facets.items()
                if face <= facet
            ))
            weight = tuple(
                sum(normal[index] for normal in incident)
                for index in range(3)
            )
            supports = []
            planes = []
            for configuration in CONFIGURATIONS:
                pairings = {
                    label: dot(weight, exponent)
                    for label, (exponent, _coefficient)
                    in configuration.items()
                }
                maximum = max(pairings.values())
                values = {
                    label: configuration[label][1]
                    for label, pairing in pairings.items()
                    if pairing == maximum
                }
                supports.append(tuple(values))
                planes.append(plane_from_pluecker(values))
            matrix = slice_map(tuple(planes))
            slice_type, _rank, _equation = classify_slice(matrix)
            all_rank = tuple(
                distinguished
                for distinguished in range(4)
                if all(
                    set(support)
                    & DELETION_COORDINATES[distinguished]
                    for support in supports
                )
            )
            if (
                slice_type not in ("secant", "tangent")
                or not all_rank
                or (
                    not include_internal_e0
                    and
                    dimension == 2
                    and incident == ((-1, 0, 0),)
                )
            ):
                continue

            image_basis = sp.Matrix.hstack(*matrix.columnspace())
            variables, equations = segre_equations(image_basis)
            common = equations[0]
            for equation in equations[1:]:
                common = sp.gcd(common, equation)
            for factor, multiplicity in sp.factor_list(
                sp.factor(common)
            )[1]:
                polynomial = sp.Poly(factor, *variables)
                direction = (
                    polynomial.coeff_monomial(variables[1]),
                    -polynomial.coeff_monomial(variables[0]),
                )
                pure_tensor = image_basis * sp.Matrix(direction)
                solution, parameters = matrix.gauss_jordan_solve(
                    pure_tensor
                )
                pure_lift = solution.subs({
                    parameter: 0 for parameter in parameters
                })
                factors = pure_factors(pure_tensor)
                base_alpha = []
                base_beta = []
                for plane, pure_factor in zip(
                    planes,
                    factors,
                    strict=True,
                ):
                    alpha = (
                        -pure_factor[1] * plane[0, :]
                        + pure_factor[0] * plane[1, :]
                    )
                    beta = (
                        plane[0, :] / pure_factor[0]
                        if pure_factor[0] != 0
                        else plane[1, :] / pure_factor[1]
                    )
                    base_alpha.append(tuple(map(sp.factor, alpha)))
                    base_beta.append(tuple(map(sp.factor, beta)))
                kernel = tuple(
                    tuple(map(sp.factor, vector))
                    for vector in matrix.nullspace()
                )
                assert len(kernel) == 2
                raw_cases.append({
                    "dimension": dimension,
                    "incident": incident,
                    "direction": tuple(map(sp.factor, direction)),
                    "multiplicity": multiplicity,
                    "all_rank": all_rank,
                    "kernel": kernel,
                    "pure_lift": tuple(map(sp.factor, pure_lift)),
                    "base_alpha": tuple(base_alpha),
                    "base_beta": tuple(base_beta),
                })

    raw_cases.sort(key=lambda case: (
        -case["dimension"],
        case["incident"],
        case["direction"],
    ))
    cases = tuple(
        ToricCase(
            case_id=index,
            dimension=case["dimension"],
            incident_normals=case["incident"],
            pure_direction=case["direction"],
            multiplicity=case["multiplicity"],
            all_rank=case["all_rank"],
            kernel=case["kernel"],
            pure_lift=case["pure_lift"],
            base_alpha=case["base_alpha"],
            base_beta=case["base_beta"],
        )
        for index, case in enumerate(raw_cases)
    )
    if include_internal_e0:
        assert len(cases) == 19
        assert sum(len(case.all_rank) for case in cases) == 45
    else:
        assert len(cases) == 17
        assert sum(len(case.all_rank) for case in cases) == 39
    return cases


def marked_rows(
    case: ToricCase,
    chart: str,
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    tuple[sp.Symbol, ...],
]:
    t = sp.symbols("t0:4")
    s = sp.Symbol("s")
    k0 = sp.Matrix(case.kernel[0])
    k1 = sp.Matrix(case.kernel[1])
    pure_lift = sp.Matrix(case.pure_lift)
    if chart == "finite":
        r = sp.Symbol("r")
        alpha_zero = k0 + r * k1
        beta_zero = pure_lift + s * k1 + t[0] * alpha_zero
        plane_parameters = (r, s)
    elif chart == "infinity":
        alpha_zero = k1
        beta_zero = pure_lift + s * k0 + t[0] * alpha_zero
        plane_parameters = (s,)
    else:
        raise ValueError(f"unknown first-plane chart: {chart}")
    alpha = (tuple(alpha_zero),) + case.base_alpha
    beta = (tuple(beta_zero),) + tuple(
        tuple(
            case.base_beta[mode][coordinate]
            + t[mode + 1] * case.base_alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(3)
    )
    return alpha, beta, plane_parameters


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def singular_program(
    case: ToricCase,
    distinguished: int,
    chart: str,
    absolute: bool,
) -> str:
    if distinguished not in case.all_rank:
        raise ValueError(
            f"q={distinguished} is not all-rank for case {case.case_id}"
        )
    alpha, beta, plane_parameters = marked_rows(case, chart)
    t = sp.symbols("t0:4")
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    extension = sp.Matrix(x + y)
    inverse_b = sp.Symbol("ub")
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    equations = list(mixed * extension)
    equations.extend((
        (diagonal_a * extension)[0] - 1,
        inverse_b * (diagonal_b * extension)[0] - 1,
    ))
    eliminated = x + y + (inverse_b,)
    if absolute:
        retained = t + plane_parameters
        variables = eliminated + retained
        ring = (
            "ring R=0,("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));"
        )
    else:
        variables = eliminated + t
        ring = (
            "ring R=(0,"
            + ",".join(map(str, plane_parameters))
            + "),("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(t)}));"
        )
    return "\n".join((
        ring,
        "option(redSB);",
        "ideal incidence=" + ",".join(map(singular, equations)) + ";",
        "ideal basis=slimgb(incidence);",
        "ideal marking=eliminate(basis,"
        + "*".join(map(str, eliminated))
        + ");",
        "marking=slimgb(marking);",
        f'"CASE={case.case_id}_Q={distinguished}_CHART={chart}_'
        + ("ABSOLUTE" if absolute else "GENERIC")
        + '";',
        '"BASIS_SIZE"; size(basis);',
        '"MARKING_SIZE"; size(marking);',
        "marking;",
        "quit;",
        "",
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_id", type=int, nargs="?")
    parser.add_argument("--q", type=int, choices=range(4))
    parser.add_argument(
        "--chart",
        choices=("finite", "infinity"),
        default="finite",
    )
    parser.add_argument("--absolute", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--timeout", type=float, default=120)
    arguments = parser.parse_args()
    cases = toric_cases()
    if arguments.list:
        for case in cases:
            print(
                case.case_id,
                f"dim={case.dimension}",
                f"normals={case.incident_normals}",
                f"direction={case.pure_direction}",
                f"multiplicity={case.multiplicity}",
                f"q={case.all_rank}",
            )
        return
    if arguments.case_id is None or arguments.q is None:
        parser.error("case_id and --q are required unless --list is used")
    case = cases[arguments.case_id]
    program = singular_program(
        case,
        arguments.q,
        arguments.chart,
        arguments.absolute,
    )
    if not arguments.run:
        print(program, end="")
        return
    completed = subprocess.run(
        singular_command_with_timeout(arguments.timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=arguments.timeout + 5,
        check=False,
    )
    print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
