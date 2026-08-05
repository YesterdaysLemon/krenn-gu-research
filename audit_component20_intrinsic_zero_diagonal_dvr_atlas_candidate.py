#!/usr/bin/env python3
"""Independent no-import verifier for the component-20 zero-base diagonal atlas."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sympy as sp
import z3

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_VERIFICATION.md"
CANDIDATE = ROOT / "COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_CANDIDATE.md"
COMPONENT20 = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
COMPONENT18 = ROOT / "P4_COMMON_SINGLETON_COMPONENT.md"
COMPONENT15_BOUNDARY = ROOT / "P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md"
COMPONENT16_BOUNDARY = ROOT / "P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md"
FROZEN_COMMIT = "f997c8366b461f3952faef0d35b512318341909d"

WORDS = tuple(itertools.product((0, 1), repeat=4))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))
MODE_PAIRS = tuple(itertools.combinations(range(4), 2))
PAIR_LABELS = tuple(f"{i}{j}" for i, j in MODE_PAIRS)
PROFILE_ORDER = "01,02,03,12,13,23"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=15,
    ).stdout.strip()


def frozen_component_sources_unchanged() -> bool:
    component_sources = (
        COMPONENT20,
        COMPONENT18,
        COMPONENT15_BOUNDARY,
        COMPONENT16_BOUNDARY,
    )
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", FROZEN_COMMIT, "HEAD"),
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=15,
    )
    if ancestor.returncode != 0:
        return False
    unchanged = subprocess.run(
        (
            "git",
            "diff",
            "--quiet",
            FROZEN_COMMIT,
            "--",
            *(path.name for path in component_sources),
        ),
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=15,
    )
    return unchanged.returncode == 0


def add(*rows: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(4))


def scale(value: Any, row: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def permanent(rows: tuple[tuple[Any, ...], ...]) -> sp.Expr:
    size = len(rows)
    require(all(len(row) == size for row in rows), "permanent input is not square")
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                target = mask | bit
                next_states[target] = sp.expand(
                    next_states.get(target, sp.Integer(0)) + coefficient * entry
                )
        states = next_states
    return sp.factor(states[(1 << size) - 1])


def tensor(
    alpha: tuple[tuple[Any, ...], ...], beta: tuple[tuple[Any, ...], ...]
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS
    }


def support(values: dict[tuple[int, ...], Any]) -> dict[str, sp.Expr]:
    return {
        "".join(str(bit) for bit in word): sp.factor(value)
        for word, value in values.items()
        if sp.factor(value) != 0
    }


def wedge(left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(left[i] * right[j] - left[j] * right[i]) for i, j in SOURCE_PAIRS
    )


def symmetric_product(left: tuple[Any, ...], right: tuple[Any, ...]) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in SOURCE_PAIRS]
    )


def pair_matrix(
    left: tuple[tuple[Any, ...], tuple[Any, ...]],
    right: tuple[tuple[Any, ...], tuple[Any, ...]],
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def base_plucker_audit() -> dict[str, Any]:
    p, q = sp.symbols("p q")
    delta = p + q
    s_intrinsic = p - q + 1
    a = p * (p + 1)
    g = q * (q - 1)
    polynomial_plucker = (a, -g, -s_intrinsic, delta**2, -delta, delta)
    p01, p02, p03, p12, p13, p23 = polynomial_plucker
    require(
        sp.expand(p01 * p23 - p02 * p13 + p03 * p12) == 0,
        "polynomial mode-zero Pluecker relation",
    )
    source_tensor = {
        "0111": sp.factor(2 * s_intrinsic),
        "1111": sp.factor(-2 * g),
    }
    bases = {}
    for label, point in (("p0_q1", (0, 1)), ("pm1_q0", (-1, 0))):
        substitution = {p: point[0], q: point[1]}
        specialized = tuple(
            sp.factor(value.subs(substitution)) for value in polynomial_plucker
        )
        require(
            any(value != 0 for value in specialized),
            f"{label}: Grassmann point vanished",
        )
        require(
            all(value.subs(substitution) == 0 for value in source_tensor.values()),
            f"{label}: restriction is not zero",
        )
        bases[label] = {
            "point": list(point),
            "polynomial_U0_plucker": [str(value) for value in specialized],
            "restricted_tensor_support": {},
            "Grassmann_map_regular": True,
        }
    return {
        "polynomial_U0_plucker": [str(value) for value in polynomial_plucker],
        "plucker_relation_identically_zero": True,
        "generic_pure_support": {
            key: str(value) for key, value in source_tensor.items()
        },
        "bases": bases,
    }


def zmin(*values: z3.ArithRef) -> z3.ArithRef:
    result = values[0]
    for value in values[1:]:
        result = z3.If(result <= value, result, value)
    return result


def fan_query(
    name: str,
    constraints: tuple[z3.BoolRef, ...],
    energy: z3.ArithRef,
    h: z3.ArithRef,
    x0: z3.ArithRef,
    x1: z3.ArithRef,
    x2: z3.ArithRef,
) -> dict[str, Any]:
    expected = z3.And(x1 == 0, x2 == 0, x0 <= -h)
    solver = z3.Solver()
    solver.add(*constraints)
    solver.add(z3.Or(energy < 0, z3.Xor(energy == 0, expected)))
    result = solver.check()
    require(result == z3.unsat, f"{name}: min-plus counterexample")
    return {
        "branch": name,
        "E_nonnegative_and_zero_cone_exact": True,
        "counterexample_query": "unsat",
        "zero_cone": "x1=x2=0, x0<=-h",
    }


def valuation_fan_audit() -> dict[str, Any]:
    r, s, w, x0, x1, x2 = z3.Reals("r s w x0 x1 x2")
    z = zmin(x0, x1, x2)
    a0 = zmin(r + x1, s + x2, w)
    m0 = zmin(
        r + x0 + x1,
        s + x0 + x2,
        w + x0,
        x1 + x2,
        x1,
        x2,
    )
    m1 = zmin(x0 + x1, s + x0 + x2, x0)
    m2 = zmin(r + x0 + x1, x0 + x2, x0)
    m3 = zmin(x0 + x1, x0 + x2)
    energy = 3 * x0 + x1 + x2 + z + a0 - m0 - m1 - m2 - m3
    finite = []
    finite_cases = (
        ("r_lt_s", (r > 0, s > 0, r < s, w == r), r),
        ("s_lt_r", (r > 0, s > 0, s < r, w == s), s),
        ("equal_no_cancellation", (r > 0, r == s, w == r), r),
        ("equal_higher_cancellation", (r > 0, r == s, w > r), r),
    )
    for name, constraints, h in finite_cases:
        finite.append(fan_query(name, constraints, energy, h, x0, x1, x2))

    h = z3.Real("h")
    exact_axes = []
    # v=0: the terms containing v are absent rather than assigned a large sample value.
    a0_v0 = zmin(h + x1, h)
    m0_v0 = zmin(h + x0 + x1, h + x0, x1 + x2, x1, x2)
    m1_v0 = zmin(x0 + x1, x0)
    m2_v0 = zmin(h + x0 + x1, x0 + x2, x0)
    energy_v0 = 3 * x0 + x1 + x2 + z + a0_v0 - m0_v0 - m1_v0 - m2_v0 - m3
    exact_axes.append(fan_query("v_equals_0", (h > 0,), energy_v0, h, x0, x1, x2))

    a0_u0 = zmin(h + x2, h)
    m0_u0 = zmin(h + x0 + x2, h + x0, x1 + x2, x1, x2)
    m1_u0 = zmin(x0 + x1, h + x0 + x2, x0)
    m2_u0 = zmin(x0 + x2, x0)
    energy_u0 = 3 * x0 + x1 + x2 + z + a0_u0 - m0_u0 - m1_u0 - m2_u0 - m3
    exact_axes.append(fan_query("u_equals_0", (h > 0,), energy_u0, h, x0, x1, x2))

    a0_equal = zmin(h + x1, h + x2)
    m0_equal = zmin(h + x0 + x1, h + x0 + x2, x1 + x2, x1, x2)
    m1_equal = zmin(x0 + x1, h + x0 + x2, x0)
    m2_equal = zmin(h + x0 + x1, x0 + x2, x0)
    energy_equal = 3 * x0 + x1 + x2 + z + a0_equal - m0_equal - m1_equal - m2_equal - m3
    exact_axes.append(
        fan_query("u_equals_v_nonzero", (h > 0,), energy_equal, h, x0, x1, x2)
    )

    numeric = {r: 1, s: 1, w: 1, x0: 1, x1: 0, x2: 0}
    correct_sample = sp.Integer(1)
    bad_sample = sp.Integer(-1)

    # Mirror the exact min evaluation independently in integers.
    def integer_min(*items: int) -> int:
        return min(items)

    numeric_m0 = integer_min(2, 2, 2, 0, 0, 0)
    numeric_m1 = integer_min(1, 2, 1)
    numeric_m2 = integer_min(2, 1, 1)
    numeric_m3 = integer_min(1, 1)
    reconstructed_correct = (
        3
        + integer_min(1, 0, 0)
        + integer_min(1, 1, 1)
        - numeric_m0
        - numeric_m1
        - numeric_m2
        - numeric_m3
    )
    reconstructed_bad = 1 + 1 - numeric_m0 - numeric_m1 - numeric_m2 - numeric_m3
    require(reconstructed_correct == correct_sample, "correct exponent regression")
    require(reconstructed_bad == bad_sample, "bad shortcut regression")
    return {
        "derivation": {
            "plane_wedge_valuations": {
                "m0": "min(r+x0+x1,s+x0+x2,w+x0,x1+x2,x1,x2)",
                "m1": "min(x0+x1,s+x0+x2,x0)",
                "m2": "min(r+x0+x1,x0+x2,x0)",
                "m3": "min(x0+x1,x0+x2)",
            },
            "kernel_row_valuations": ["a0", "x0", "x0", "z"],
            "source_determinant_valuation": "x0+x1+x2",
            "E": "3*x0+x1+x2+z+a0-m0-m1-m2-m3",
            "centre_two_exchanges_m1_m2_only": True,
        },
        "finite_ultrametric_branches": finite,
        "exact_one_sided_and_diagonal_axes": exact_axes,
        "constant_u_equals_v_equals_0_restriction": "identically zero",
        "fan_exhaustive": True,
        "E_nonnegative": True,
        "E_zero_iff": "x1=x2=0, x0<=-h",
        "strata": ["interior x0<-h", "wall x0=-h"],
        "wrong_selected_row_shortcut": {
            "sample": {str(key): value for key, value in numeric.items()},
            "correct_E": reconstructed_correct,
            "E_bad": reconstructed_bad,
            "shortcut_refuted": True,
        },
    }


c0, c1, c2, pi, theta = sp.symbols("c0 c1 c2 pi theta", nonzero=True)
e = (sp.Integer(1), 0, 0, 0)

BRANCHES = (
    "r_lt_s",
    "s_lt_r",
    "equal_no_cancellation",
    "equal_higher_cancellation",
)

EXPECTED_CENTRE0_PROFILES = {
    ("r_lt_s", "interior"): (2, 3, 3, 3, 3, 3),
    ("r_lt_s", "wall"): (3, 4, 4, 3, 3, 3),
    ("s_lt_r", "interior"): (3, 2, 3, 3, 3, 3),
    ("s_lt_r", "wall"): (4, 3, 4, 3, 3, 3),
    ("equal_no_cancellation", "interior"): (3, 3, 3, 3, 3, 3),
    ("equal_no_cancellation", "wall"): (4, 4, 4, 3, 3, 3),
    ("equal_higher_cancellation", "interior"): (3, 3, 2, 3, 3, 3),
    ("equal_higher_cancellation", "wall"): (4, 4, 3, 3, 3, 3),
}


def branch_kernel(branch: str) -> tuple[sp.Expr, ...]:
    if branch == "r_lt_s":
        return (0, -pi * c1, 0, pi)
    if branch == "s_lt_r":
        return (0, 0, theta * c2, -theta)
    if branch == "equal_no_cancellation":
        return (0, -pi * c1, theta * c2, pi - theta)
    if branch == "equal_higher_cancellation":
        return (0, -pi * c1, pi * c2, 0)
    raise ValueError(branch)


def wall_plucker(branch: str) -> tuple[sp.Expr, ...]:
    low = (-c1 * c2, c1, -c2)
    if branch == "r_lt_s":
        return (-pi * c0 * c1, 0, pi * c0, *low)
    if branch == "s_lt_r":
        return (0, theta * c0 * c2, -theta * c0, *low)
    if branch == "equal_no_cancellation":
        return (
            -pi * c0 * c1,
            theta * c0 * c2,
            (pi - theta) * c0,
            *low,
        )
    if branch == "equal_higher_cancellation":
        return (-pi * c0 * c1, pi * c0 * c2, 0, *low)
    raise ValueError(branch)


def plane_from_p23(plucker: tuple[Any, ...]) -> tuple[tuple[sp.Expr, ...], ...]:
    _p01, p02, p03, p12, p13, p23 = plucker
    require(p23 != 0, "p23 pivot vanished")
    first = (
        sp.factor(p03 / p23),
        sp.factor(p13 / p23),
        sp.Integer(1),
        sp.Integer(0),
    )
    second = (
        sp.factor(-p02 / p23),
        sp.factor(-p12 / p23),
        sp.Integer(0),
        sp.Integer(1),
    )
    reconstructed = wedge(first, second)
    require(
        all(sp.factor(reconstructed[i] * p23 - plucker[i]) == 0 for i in range(6)),
        "p23 chart reconstruction",
    )
    return first, second


def source_centre_symmetry(row: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    return (row[0], -row[1], -row[2], row[3])


def plucker_centre_symmetry(plucker: tuple[Any, ...]) -> tuple[sp.Expr, ...]:
    signs = (-1, -1, 1, 1, -1, -1)
    return tuple(sp.expand(signs[i] * plucker[i]) for i in range(6))


def oriented_chart(
    centre: str, branch: str, stratum: str
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]], ...],
    tuple[sp.Expr, ...],
]:
    kernel0 = branch_kernel(branch)
    active1 = (0, c1, 0, 1)
    active2 = (0, 0, c2, 1)
    active3 = (0, c1, c2, 0)
    if stratum == "interior":
        plane0 = (e, kernel0)
        beta0 = e
        raw_plucker = wedge(*plane0)
    elif stratum == "wall":
        raw_plucker = wall_plucker(branch)
        plane0 = plane_from_p23(raw_plucker)
        # K0 is the intrinsic kernel line in the reconstructed plane.
        require(
            sp.Matrix((*plane0, kernel0)).rank() == 2,
            f"{branch}: K0 not in wall U0",
        )
        beta0 = plane0[1] if branch == "equal_higher_cancellation" else plane0[0]
        require(
            sp.Matrix((kernel0, beta0)).rank() == 2,
            f"{branch}: wall complement collapsed",
        )
    else:
        raise ValueError(stratum)

    alpha = (kernel0, e, e, e)
    beta = (beta0, active1, active2, active3)
    planes = (
        (alpha[0], beta[0]),
        (alpha[1], beta[1]),
        (alpha[2], beta[2]),
        (alpha[3], beta[3]),
    )
    if centre == "p0_q1":
        return alpha, beta, planes, raw_plucker
    if centre != "pm1_q0":
        raise ValueError(centre)
    transformed_planes = tuple(
        tuple(source_centre_symmetry(row) for row in plane) for plane in planes
    )
    transformed_planes = (
        transformed_planes[0],
        transformed_planes[2],
        transformed_planes[1],
        transformed_planes[3],
    )
    transformed_alpha = tuple(plane[0] for plane in transformed_planes)
    transformed_beta = tuple(plane[1] for plane in transformed_planes)
    return (
        transformed_alpha,
        transformed_beta,
        transformed_planes,
        plucker_centre_symmetry(raw_plucker),
    )


def guaranteed_nonzero(expression: sp.Expr, branch: str) -> bool:
    numerator, denominator = sp.together(expression).as_numer_denom()
    if numerator == 0 or denominator == 0:
        return False
    allowed = [c0, c1, c2, pi, theta]
    if branch == "r_lt_s":
        allowed = [c0, c1, c2, pi]
    elif branch == "s_lt_r":
        allowed = [c0, c1, c2, theta]
    elif branch == "equal_higher_cancellation":
        allowed = [c0, c1, c2, pi]
    elif branch == "equal_no_cancellation":
        allowed = [c0, c1, c2, pi, theta, pi - theta]

    def allowed_factor(factor: sp.Expr) -> bool:
        if factor.is_number:
            return factor != 0
        return any(
            sp.factor(factor / candidate).is_number
            and sp.factor(factor / candidate) != 0
            for candidate in allowed
        )

    for polynomial in (numerator, denominator):
        coefficient, factors = sp.factor_list(polynomial)
        if coefficient == 0 or any(not allowed_factor(factor) for factor, _ in factors):
            return False
    return True


def rank_certificate(matrix: sp.Matrix, target: int, branch: str) -> dict[str, Any]:
    if target < min(matrix.rows, matrix.cols):
        for rows in itertools.combinations(range(matrix.rows), target + 1):
            for columns in itertools.combinations(range(matrix.cols), target + 1):
                require(
                    sp.factor(matrix.extract(rows, columns).det()) == 0,
                    "rank upper-bound minor survived",
                )
    witness = None
    for rows in itertools.combinations(range(matrix.rows), target):
        for columns in itertools.combinations(range(matrix.cols), target):
            determinant = sp.factor(matrix.extract(rows, columns).det())
            if guaranteed_nonzero(determinant, branch):
                witness = {
                    "rows": list(rows),
                    "columns": list(columns),
                    "determinant": str(determinant),
                }
                break
        if witness is not None:
            break
    require(witness is not None, f"no residue-stable rank-{target} witness")
    return {"rank": target, "witness": witness, "upper_bound_exact": True}


def expected_profile(centre: str, branch: str, stratum: str) -> tuple[int, ...]:
    profile = EXPECTED_CENTRE0_PROFILES[(branch, stratum)]
    if centre == "p0_q1":
        return profile
    return (profile[1], profile[0], profile[2], profile[3], profile[5], profile[4])


def permanent3(rows: tuple[tuple[Any, ...], ...]) -> sp.Expr:
    return permanent(tuple(tuple(row[i] for i in (1, 2, 3)) for row in rows))


def h31_hall_audit(alpha: tuple[tuple[Any, ...], ...]) -> dict[str, Any]:
    extensions = sp.symbols("z0:4")
    deletion_results = {}
    for distinguished in range(4):
        projected = []
        for mode, row in enumerate(alpha):
            extended = (*row, extensions[mode])
            projected.append(
                tuple(
                    entry
                    for coordinate, entry in enumerate(extended)
                    if coordinate != distinguished
                )
            )
        value = sp.factor(permanent(tuple(projected)))
        require(value == 0, f"H31 deletion {distinguished} Hall diagonal")
        deletion_results[str(distinguished)] = "0"
    return {
        "all_markings": True,
        "reason_markings_do_not_change_alpha_rows": True,
        "all_alpha_diagonals_by_deletion": deletion_results,
        "three_e_rows_use_at_most_two_columns": True,
    }


def weighted_project_row(
    row: tuple[Any, ...], extension: Any, direction: str, chart: str, lam: sp.Symbol
) -> tuple[sp.Expr, ...]:
    if direction == "D01" and chart == "finite":
        return (sp.expand(lam * row[0] + row[1]), row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], sp.expand(lam * row[2] + row[3]), extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def h22_hall_audit(alpha: tuple[tuple[Any, ...], ...]) -> dict[str, Any]:
    extensions = sp.symbols("w0:4")
    lam = sp.Symbol("lambda")
    results = {}
    for chart in ("finite", "infinity"):
        for direction in ("D01", "D23"):
            rows = tuple(
                weighted_project_row(alpha[i], extensions[i], direction, chart, lam)
                for i in range(4)
            )
            value = sp.factor(permanent(rows))
            require(value == 0, f"{chart} {direction} H22 Hall diagonal")
            results[f"{chart}_{direction}"] = "0"
    return {
        "all_markings": True,
        "finite_weight_polynomial_in_lambda_including_zero": True,
        "direct_weight_infinity_endpoint": True,
        "all_alpha_diagonals": results,
        "neither_weighted_direction_can_be_binary": True,
    }


def placement_audit(
    branch: str,
    stratum: str,
    planes: tuple[tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]], ...],
    profile: tuple[int, ...],
    kernel0: tuple[sp.Expr, ...],
) -> dict[str, Any]:
    active = (planes[1][1], planes[2][1], planes[3][1])
    if stratum == "interior":
        require(
            all(sp.Matrix((*plane, e)).rank() == 2 for plane in planes),
            "interior common singleton",
        )
        require(
            all(
                permanent3((kernel0, active[i], active[j])) == 0
                for i, j in itertools.combinations(range(3), 2)
            ),
            "component-18 orthogonality",
        )
        active_cubic = sp.factor(permanent3(active))
        require(guaranteed_nonzero(active_cubic, branch), "component-18 active cubic")
        placement = {
            "component20_closure": True,
            "component18_common_singleton_closure": True,
            "component18_hypotheses": {
                "all_planes_contain_e": True,
                "three_B_K0_orthogonalities": True,
                "active_cubic": str(active_cubic),
            },
        }
        lower_edges = [
            edge for edge, rank in zip(PAIR_LABELS, profile, strict=True) if rank == 2
        ]
        require(len(lower_edges) <= 1, "multiple interior rank-two pairs")
        lower_pair = tuple(map(int, lower_edges[0])) if lower_edges else None
        if lower_pair is not None:
            i, j = lower_pair
            require(
                profile[PAIR_LABELS.index(f"{i}{j}")] == 2, "support-one rank-two pair"
            )
            require(
                symmetric_product(planes[i][1], planes[j][0]) == sp.zeros(6, 1),
                "support-one e*e kernel point",
            )
            require(
                symmetric_product(planes[i][0], planes[j][1]) == sp.zeros(6, 1),
                "disjoint binary kernel point",
            )
            placement["component15_support_one_secant_closure"] = True
            placement["component15_exact_rank_two_pair"] = f"{i}{j}"
        else:
            placement["component15_support_one_secant_closure"] = False
        placement["component16_triple_kernel_closure"] = False
        return placement

    require(all(rank >= 3 for rank in profile), "wall has a lower pair")
    for edge in ("12", "13", "23"):
        i, j = map(int, edge)
        matrix = pair_matrix(planes[i], planes[j])
        require(matrix.rank() == 3, f"wall triangle pair {edge}")
        nullspace = matrix.nullspace()
        require(
            nullspace == [sp.Matrix((1, 0, 0, 0))],
            f"wall triangle kernel {edge}",
        )
    raw0 = wedge(*planes[0])
    require(any(raw0[index] != 0 for index in (3, 4, 5)), "wall U0 contains e")
    return {
        "component20_closure": True,
        "component18_common_singleton_closure": False,
        "component15_support_one_secant_closure": False,
        "component16_triple_kernel_closure": True,
        "component16_hypotheses": {
            "all_pair_ranks_at_least_three": True,
            "triangle_pairs_12_13_23_rank_three": True,
            "unique_relations": ["e*e", "e*e", "e*e"],
            "U0_contains_e": False,
        },
    }


def chart_atlas_audit() -> dict[str, Any]:
    charts = {}
    centre0_cache = {}
    for centre in ("p0_q1", "pm1_q0"):
        for branch in BRANCHES:
            for stratum in ("interior", "wall"):
                label = f"{centre}_{branch}_{stratum}"
                alpha, beta, planes, raw_plucker = oriented_chart(
                    centre, branch, stratum
                )
                pure = support(tensor(alpha, beta))
                require(set(pure) == {"1111"}, f"{label}: non-pure support")
                require(
                    guaranteed_nonzero(pure["1111"], branch),
                    f"{label}: zero pure scalar",
                )
                target_profile = expected_profile(centre, branch, stratum)
                pair_certificates = {}
                actual_profile = []
                for edge, (i, j), target in zip(
                    PAIR_LABELS, MODE_PAIRS, target_profile, strict=True
                ):
                    certificate = rank_certificate(
                        pair_matrix(planes[i], planes[j]), target, branch
                    )
                    pair_certificates[edge] = certificate
                    actual_profile.append(certificate["rank"])
                require(
                    tuple(actual_profile) == target_profile, f"{label}: pair profile"
                )

                if (
                    centre == "p0_q1"
                    and branch == "equal_no_cancellation"
                    and stratum == "interior"
                ):
                    physical_pair = pair_matrix((e, alpha[0]), (e, beta[3]))
                    robust = sp.factor(
                        physical_pair.extract((0, 2, 3), (1, 2, 3)).det()
                    )
                    require(
                        robust == -(c1**2) * c2 * (pi - theta) ** 2,
                        "pi+theta-stable 03 witness",
                    )

                if branch == "equal_no_cancellation":
                    substituted_profile = tuple(
                        pair_matrix(planes[i], planes[j]).subs(theta, -pi).rank()
                        for i, j in MODE_PAIRS
                    )
                    require(
                        substituted_profile == target_profile,
                        f"{label}: pi+theta=0 rank drop",
                    )
                    require(
                        sp.factor(pure["1111"].subs(theta, -pi)) != 0,
                        f"{label}: pi+theta=0 pure scalar",
                    )

                c0_retained = False
                if stratum == "wall":
                    high_index = next(i for i in range(3) if raw_plucker[i] != 0)
                    ratio = sp.factor(raw_plucker[high_index] / raw_plucker[5])
                    require(
                        sp.factor(sp.diff(ratio, c0)) != 0, f"{label}: wall c0 lost"
                    )
                    c0_retained = True
                    require(
                        sp.expand(
                            raw_plucker[0] * raw_plucker[5]
                            - raw_plucker[1] * raw_plucker[4]
                            + raw_plucker[2] * raw_plucker[3]
                        )
                        == 0,
                        f"{label}: leading Pluecker relation",
                    )

                placement = placement_audit(
                    branch, stratum, planes, target_profile, alpha[0]
                )
                h31 = h31_hall_audit(alpha)
                h22 = h22_hall_audit(alpha)
                chart = {
                    "centre": centre,
                    "branch": branch,
                    "stratum": stratum,
                    "raw_U0_plucker": [str(value) for value in raw_plucker],
                    "leading_planes": [
                        [[str(entry) for entry in row] for row in plane]
                        for plane in planes
                    ],
                    "intrinsic_kernel_rows": [
                        [str(entry) for entry in row] for row in alpha
                    ],
                    "pure_support": {key: str(value) for key, value in pure.items()},
                    "pair_profile_order": PROFILE_ORDER,
                    "pair_profile": list(target_profile),
                    "pair_certificates": pair_certificates,
                    "pi_plus_theta_zero_checked": branch == "equal_no_cancellation",
                    "wall_c0_retained": c0_retained,
                    "placement": placement,
                    "H31_Hall": h31,
                    "weighted_H22_Hall": h22,
                }
                charts[label] = chart
                if centre == "p0_q1":
                    centre0_cache[(branch, stratum)] = chart
                else:
                    source = centre0_cache[(branch, stratum)]
                    symbol_table = {
                        "c0": c0,
                        "c1": c1,
                        "c2": c2,
                        "pi": pi,
                        "theta": theta,
                    }
                    source_raw = tuple(
                        sp.sympify(value, locals=symbol_table)
                        for value in source["raw_U0_plucker"]
                    )
                    expected_raw = plucker_centre_symmetry(source_raw)
                    require(
                        all(
                            sp.factor(raw_plucker[i] - expected_raw[i]) == 0
                            for i in range(6)
                        ),
                        f"{label}: raw centre symmetry",
                    )
                    source_profile = tuple(source["pair_profile"])
                    require(
                        target_profile
                        == (
                            source_profile[1],
                            source_profile[0],
                            source_profile[2],
                            source_profile[3],
                            source_profile[5],
                            source_profile[4],
                        ),
                        f"{label}: profile centre symmetry",
                    )
    require(len(charts) == 16, "atlas chart count")
    return {
        "chart_count": len(charts),
        "charts": charts,
        "all_charts_nonzero_pure": True,
        "all_charts_in_component20_closure": True,
        "exact_centre_symmetry": True,
        "axes_routing": {
            "v=0": "r_lt_s",
            "u=0": "s_lt_r",
            "u=v_nonzero": "equal_higher_cancellation",
            "u=v=0": "zero restriction, no nonzero chart",
        },
    }


def source_and_candidate_audit(
    atlas: dict[str, Any], fan: dict[str, Any]
) -> dict[str, Any]:
    component20_text = " ".join(COMPONENT20.read_text(encoding="utf-8").split())
    component18_text = " ".join(COMPONENT18.read_text(encoding="utf-8").split())
    component15_text = " ".join(
        COMPONENT15_BOUNDARY.read_text(encoding="utf-8").split()
    )
    component16_text = " ".join(
        COMPONENT16_BOUNDARY.read_text(encoding="utf-8").split()
    )
    require(
        "T_0111=2(p-q+1), T_1111=-2q(q-1)" in component20_text,
        "component-20 tensor source",
    )
    require("U0=span(e,ell)" in component18_text, "component-18 family source")
    require(
        "pairwise `B_ell`-orthogonal" in component18_text, "component-18 hypothesis"
    )
    require("exact rank-two pair" in component15_text, "component-15 rank hypothesis")
    require(
        "support-one zero product" in component15_text,
        "component-15 support hypothesis",
    )
    require(
        "all six pair images have rank at least three" in component16_text,
        "component-16 all-pair hypothesis",
    )
    require("y_1 y_2=0" in component16_text, "component-16 kernel triangle")
    require(
        "otherwise it belongs to component sixteen" in component16_text,
        "component-16 conclusion",
    )

    # The candidate is read only after the independent atlas is complete.
    candidate_text = " ".join(CANDIDATE.read_text(encoding="utf-8").split())
    for marker in (
        "claim_label: CANDIDATE",
        "E >= 0",
        "E=0` iff `x1=x2=0` and `x0<=-h",
        "Complete 16-chart machine atlas",
        "pi+theta=0",
        "diagonal arcs only",
        "global conjecture unresolved",
    ):
        require(marker in candidate_text, f"candidate marker: {marker}")
    require(atlas["chart_count"] == 16, "independent atlas count")
    require(fan["E_nonnegative"], "independent fan conclusion")
    return {
        "candidate_read_after_independent_reconstruction": True,
        "candidate_script_imported_or_executed": False,
        "candidate_json_read_or_trusted": False,
        "proof_B_script_or_report_read_or_used": False,
        "candidate_claim_matches_independent_atlas": True,
        "frozen_component_hypotheses_checked": True,
    }


def main() -> None:
    require(
        frozen_component_sources_unchanged(),
        "frozen component sources changed or the frozen commit is not an ancestor",
    )
    base = base_plucker_audit()
    fan = valuation_fan_audit()
    atlas = chart_atlas_audit()
    dependency_audit = source_and_candidate_audit(atlas, fan)
    inputs = (
        CANDIDATE,
        COMPONENT20,
        COMPONENT18,
        COMPONENT15_BOUNDARY,
        COMPONENT16_BOUNDARY,
    )
    payload = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "complete diagonal source-torus DVR/Puiseux atlas over component-20 "
            "intrinsic zero bases (p,q)=(0,1),(-1,0), including pointwise Hall "
            "H31/H22 obstructions on the sixteen nonzero leading charts"
        ),
        "inputs": {path.name: sha256(path) for path in inputs},
        "method": (
            "fresh polynomial Pluecker reconstruction, exact real-linear min-plus "
            "exhaustion, symbolic leading planes/permanents/minor witnesses, exact "
            "centre symmetry, component-hypothesis checks, and direct Hall support"
        ),
        "command": ("uv run --with sympy --with z3-solver python " + SCRIPT.name),
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT) if REPORT.exists() else "pending",
        },
        "base_geometry": base,
        "valuation_fan": fan,
        "atlas": atlas,
        "dependency_audit": dependency_audit,
        "all_16_H31_pointwise_Hall_obstructions": True,
        "all_16_both_weighted_H22_Hall_obstructions": True,
        "finite_weight_including_zero_and_projective_infinity_checked": True,
        "all_markings_checked_structurally": True,
        "wall_c0_retained_in_all_8_wall_charts": True,
        "pi_plus_theta_zero_rank_stable": True,
        "finite_field_inference_used": False,
        "parameter_grid_used": False,
        "broad_brute_force_used": False,
        "global_Krenn_Gu_resolved": False,
        "limitations": (
            "diagonal source-torus DVR/Puiseux arcs only; placement is closure "
            "placement under frozen component theorems; no non-diagonal or arbitrary "
            "GL4 arcs, component exhaustiveness, arbitrary-order reduction, prize "
            "graph, or global Krenn-Gu conclusion"
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
