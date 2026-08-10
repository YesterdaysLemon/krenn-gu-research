#!/usr/bin/env python3
"""Exact proof-B replay for the two transverse component-20 base points.

The replay uses the regular polynomial Pluecker map and tensor covectors.  It
does not import another research script and does not inspect construction
artifacts.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp
import z3

ROOT = HERE
SCRIPT = Path(__file__).resolve()
REPORT = HERE / "P4_COMPONENT20_TRANSVERSE_BASE_DIAGONAL_FAN_PROOF_B.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
COMMON_SINGLETON = REPO_ROOT / "claims/p4/classifications/P4_COMMON_SINGLETON_COMPONENT.md"
TRIPLE_KERNEL = REPO_ROOT / "claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


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
    ).stdout.strip()


def multiply(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return result


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    value = {0: sp.Integer(1)}
    for row in rows:
        linear = {
            1 << index: sp.sympify(entry)
            for index, entry in enumerate(row)
            if entry != 0
        }
        value = multiply(value, linear)
    return sp.factor(value.get(15, 0))


def tensor(
    planes: tuple[tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]], ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS
    }


def nonzero_support(
    values: dict[tuple[int, ...], sp.Expr],
) -> dict[str, sp.Expr]:
    return {
        "".join(str(bit) for bit in word): sp.factor(value)
        for word, value in values.items()
        if value != 0
    }


def assert_support(
    actual: dict[str, sp.Expr], expected: dict[str, sp.Expr]
) -> None:
    assert actual.keys() == expected.keys()
    for key, value in actual.items():
        assert sp.expand(value - expected[key]) == 0


def wedge(
    left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]
) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.factor(left[i] * right[j] - left[j] * right[i]) for i, j in PAIRS
    )


def symmetric_product(
    left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]
) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def product_matrix(
    left: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
    right: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def pair_profile(
    planes: tuple[tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]], ...],
) -> tuple[int, ...]:
    return tuple(
        product_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )


def normalized_planes(p: sp.Expr, q: sp.Expr):
    delta = p + q
    s = p - q + 1
    e = (sp.Integer(1), 0, 0, 0)
    return (
        (
            (-s / delta, -1, 1, 0),
            ((q**2 - q) / delta, -delta, 0, 1),
        ),
        (e, (0, p + 1, q - 1, 1)),
        (e, (0, p, q, 1)),
        ((1, 1, 1, 0), e),
    )


def polynomial_u0_plucker(p: sp.Expr, q: sp.Expr) -> tuple[sp.Expr, ...]:
    delta = p + q
    s = p - q + 1
    return (
        sp.expand(p * (p + 1)),
        sp.expand(-q * (q - 1)),
        -s,
        delta**2,
        -delta,
        delta,
    )


def transform_row(row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Apply (e,A,B,C) -> (e,B,A,-C)."""
    return (row[0], row[2], row[1], -row[3])


def transform_row_diagonal(row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Apply diag(1,1,1,-1) in coordinates (e,A,B,C)."""
    return (row[0], row[1], row[2], -row[3])


def projectively_equal(
    left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]
) -> bool:
    assert len(left) == len(right)
    return all(
        sp.factor(left[i] * right[j] - left[j] * right[i]) == 0
        for i, j in itertools.combinations(range(len(left)), 2)
    )


def raw_family_and_symmetry() -> dict[str, object]:
    p, q = sp.symbols("p q")
    delta = p + q
    s = p - q + 1
    a = p * (p + 1)
    g = q * (q - 1)
    planes = normalized_planes(p, q)

    assert_support(
        nonzero_support(tensor(planes)),
        {"0111": 2 * s, "1111": -2 * g},
    )
    assert nonzero_support(tensor(normalized_planes(0, 1))) == {}
    p0 = polynomial_u0_plucker(p, q)
    for rational_entry, polynomial_entry in zip(
        wedge(*planes[0]), p0, strict=True
    ):
        assert sp.factor(delta * rational_entry - polynomial_entry) == 0
    p01, p02, p03, p12, p13, p23 = p0
    assert sp.expand(p01 * p23 - p02 * p13 + p03 * p12) == 0

    factor_kernel = tuple(
        sp.factor(
            (-2 * g) * planes[0][0][index]
            - (2 * s) * planes[0][1][index]
        )
        for index in range(4)
    )
    expected_kernel = (0, 2 * a, -2 * g, -2 * s)
    for actual_entry, expected_entry in zip(
        factor_kernel, expected_kernel, strict=True
    ):
        assert sp.factor(actual_entry - expected_entry) == 0

    target_planes = normalized_planes(-q, -p)
    for source_plane, target_plane in zip(planes, target_planes, strict=True):
        transformed = wedge(*(transform_row(row) for row in source_plane))
        assert projectively_equal(transformed, wedge(*target_plane))

    transformed_p0 = wedge(*(transform_row(row) for row in planes[0]))
    assert projectively_equal(transformed_p0, polynomial_u0_plucker(-q, -p))

    alternate_target = normalized_planes(-p - 1, 1 - q)
    source_to_target_mode = (0, 2, 1, 3)
    for source_mode, target_mode in enumerate(source_to_target_mode):
        transformed = wedge(
            *(transform_row_diagonal(row) for row in planes[source_mode])
        )
        assert projectively_equal(
            transformed, wedge(*alternate_target[target_mode])
        )

    return {
        "U0_polynomial_plucker": [str(value) for value in p0],
        "pure_support": {"0111": "2*(p-q+1)", "1111": "-2*q*(q-1)"},
        "mode_zero_factor_kernel": ["0", "-p*(p+1)", "q*(q-1)", "p-q+1"],
        "centre_exchange": {
            "coordinate_swap_model": {
                "parameters": "(p,q)->(-q,-p)",
                "source": "(e,A,B,C)->(e,B,A,-C)",
                "mode_permutation": "none",
                "diagonal_weights": "x1<->x2",
            },
            "diagonal_plus_mode_swap_model": {
                "parameters": "(p,q)->(-p-1,1-q)",
                "source": "diag(1,1,1,-1)",
                "mode_permutation": "1<->2",
                "diagonal_weights": "unchanged",
            },
        },
    }


def zmin(*values):
    result = values[0]
    for value in values[1:]:
        result = z3.If(result <= value, result, value)
    return result


def zmax(left, right):
    return z3.If(left >= right, left, right)


def assert_unsat(name: str, *constraints) -> str:
    solver = z3.Solver()
    solver.add(*constraints)
    result = solver.check()
    assert result == z3.unsat, (name, result, solver.model() if result == z3.sat else None)
    return "unsat"


def fan_certificate() -> dict[str, object]:
    cap_p, cap_q, cap_s, x0, x1, x2 = z3.Reals("P Q S x0 x1 x2")
    rank = zmin(cap_p, cap_q)
    actual_finite = z3.Or(
        z3.And(cap_p < cap_q, cap_s == cap_p),
        z3.And(cap_q < cap_p, cap_s == cap_q),
        z3.And(cap_p == cap_q, cap_s >= cap_p),
    )
    assumptions = (cap_p > 0, cap_q > 0, actual_finite)

    maximum = zmax(x1, x2)
    z = zmin(x0, x1, x2)
    k = zmin(cap_p + x1, cap_q + x2, cap_s)
    ell = zmin(x1 + x2, x1, x2)
    u = zmin(x0 + k, ell)
    b1 = zmin(x1, cap_q + x2, z3.RealVal(0))
    b2 = zmin(cap_p + x1, x2, z3.RealVal(0))
    excess = maximum + z + k - u - b1 - b2
    target = z3.And(x1 == 0, x2 == 0, x0 <= -rank)

    finite_checks = {
        "E_nonnegative": assert_unsat("finite E<0", *assumptions, excess < 0),
        "necessity": assert_unsat(
            "finite necessity", *assumptions, excess == 0, z3.Not(target)
        ),
        "sufficiency": assert_unsat(
            "finite sufficiency", *assumptions, target, excess != 0
        ),
    }

    intrinsic_rank, ix0, ix1, ix2 = z3.Reals("R ix0 ix1 ix2")
    imax = zmax(ix1, ix2)
    iz = zmin(ix0, ix1, ix2)
    ik = zmin(intrinsic_rank + ix1, intrinsic_rank + ix2)
    iell = zmin(ix1 + ix2, ix1, ix2)
    iu = zmin(ix0 + ik, iell)
    ib1 = zmin(ix1, intrinsic_rank + ix2, z3.RealVal(0))
    ib2 = zmin(intrinsic_rank + ix1, ix2, z3.RealVal(0))
    iexcess = imax + iz + ik - iu - ib1 - ib2
    itarget = z3.And(ix1 == 0, ix2 == 0, ix0 <= -intrinsic_rank)
    intrinsic_assumption = intrinsic_rank > 0
    intrinsic_checks = {
        "E_nonnegative": assert_unsat(
            "intrinsic E<0", intrinsic_assumption, iexcess < 0
        ),
        "necessity": assert_unsat(
            "intrinsic necessity",
            intrinsic_assumption,
            iexcess == 0,
            z3.Not(itarget),
        ),
        "sufficiency": assert_unsat(
            "intrinsic sufficiency",
            intrinsic_assumption,
            itarget,
            iexcess != 0,
        ),
    }

    def one_sided_infinite_checks(
        name: str, finite_order, ax0, ax1, ax2, ak, ab1, ab2
    ) -> dict[str, str]:
        amax = zmax(ax1, ax2)
        az = zmin(ax0, ax1, ax2)
        aell = zmin(ax1 + ax2, ax1, ax2)
        au = zmin(ax0 + ak, aell)
        aexcess = amax + az + ak - au - ab1 - ab2
        atarget = z3.And(ax1 == 0, ax2 == 0, ax0 <= -finite_order)
        return {
            "E_nonnegative": assert_unsat(
                f"{name} E<0", finite_order > 0, aexcess < 0
            ),
            "necessity": assert_unsat(
                f"{name} necessity",
                finite_order > 0,
                aexcess == 0,
                z3.Not(atarget),
            ),
            "sufficiency": assert_unsat(
                f"{name} sufficiency",
                finite_order > 0,
                atarget,
                aexcess != 0,
            ),
        }

    axis_q, qx0, qx1, qx2 = z3.Reals("Qaxis qx0 qx1 qx2")
    p_infinity_checks = one_sided_infinite_checks(
        "P=infinity",
        axis_q,
        qx0,
        qx1,
        qx2,
        zmin(axis_q + qx2, axis_q),
        zmin(qx1, axis_q + qx2, z3.RealVal(0)),
        zmin(qx2, z3.RealVal(0)),
    )
    axis_p, px0, px1, px2 = z3.Reals("Paxis px0 px1 px2")
    q_infinity_checks = one_sided_infinite_checks(
        "Q=infinity",
        axis_p,
        px0,
        px1,
        px2,
        zmin(axis_p + px1, axis_p),
        zmin(px1, z3.RealVal(0)),
        zmin(axis_p + px1, px2, z3.RealVal(0)),
    )

    def numeric_excess(
        p_value: int,
        q_value: int,
        s_value: int,
        x0_value: int,
        x1_value: int,
        x2_value: int,
    ) -> int:
        maximum_value = max(x1_value, x2_value)
        z_value = min(x0_value, x1_value, x2_value)
        k_value = min(p_value + x1_value, q_value + x2_value, s_value)
        ell_value = min(x1_value + x2_value, x1_value, x2_value)
        u_value = min(x0_value + k_value, ell_value)
        b1_value = min(x1_value, q_value + x2_value, 0)
        b2_value = min(p_value + x1_value, x2_value, 0)
        return maximum_value + z_value + k_value - u_value - b1_value - b2_value

    assert numeric_excess(1, 1, 1, 1, 0, 0) == 1

    return {
        "parameters": (
            "P,Q in (0,infinity]; R=min(P,Q); S=v(u-v)>=R"
        ),
        "actual_order_cases": [
            "P<Q => S=P",
            "Q<P => S=Q",
            "P=Q => S>=P, including S=infinity",
            "P=infinity => Q=S<infinity",
            "Q=infinity => P=S<infinity",
            "P=Q=infinity => identically zero raw tensor",
        ],
        "E": (
            "max(x1,x2)+min(x0,x1,x2)+k-min(x0+k,ell)-b1-b2"
        ),
        "k": "min(P+x1,Q+x2,S)",
        "ell": "min(x1+x2,x1,x2)",
        "b1": "min(x1,Q+x2,0)",
        "b2": "min(P+x1,x2,0)",
        "zero_cone": (
            "x1=x2=0 and x0<=-R when R<infinity; empty when R=infinity"
        ),
        "finite_order_solver_checks": finite_checks,
        "exact_intrinsic_S_infinity_checks": intrinsic_checks,
        "one_sided_infinite_order_checks": {
            "P=infinity,u=0,Q=S<infinity": p_infinity_checks,
            "Q=infinity,v=0,P=S<infinity": q_infinity_checks,
        },
        "both_orders_infinite": (
            "u=v=0 gives the identically zero restricted tensor for every "
            "finite diagonal weight triple"
        ),
        "shortcut_counterexample": {
            "P_Q_S": [1, 1, 1],
            "x0_x1_x2": [1, 0, 0],
            "correct_E": 1,
            "limiting_restriction": "zero",
        },
    }


def case_planes(pi0: sp.Expr, theta0: sp.Expr):
    c0, c1, c2 = sp.symbols("c0 c1 c2", nonzero=True)
    e = (sp.Integer(1), 0, 0, 0)
    v1 = (0, c1, 0, 1)
    v2 = (0, 0, c2, 1)
    v3 = (0, c1, c2, 0)
    kernel = (
        0,
        sp.expand(pi0 * c1),
        sp.expand(-theta0 * c2),
        sp.expand(-(pi0 - theta0)),
    )
    deep = ((e, kernel), (e, v1), (e, v2), (e, v3))
    row_a = (sp.expand(-c0 * theta0), c1, 0, -1)
    row_b = (sp.expand(-c0 * pi0), 0, c2, -1)
    boundary = ((row_a, row_b), (e, v1), (e, v2), (e, v3))
    return deep, boundary, kernel, (c0, c1, c2)


def fixed_rank_certificate(
    matrix: sp.Matrix,
    rank: int,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    allowed_nonzero_factors: tuple[sp.Expr, ...],
) -> dict[str, object]:
    determinant = sp.factor(matrix.extract(rows, columns).det())
    assert determinant != 0
    coefficient, factors = sp.factor_list(determinant)
    assert coefficient != 0
    for factor, _multiplicity in factors:
        assert any(
            sp.factor(factor - allowed) == 0
            or sp.factor(factor + allowed) == 0
            for allowed in allowed_nonzero_factors
        ), (determinant, factor, allowed_nonzero_factors)

    if rank < 4:
        for larger_rows in itertools.combinations(range(matrix.rows), rank + 1):
            for larger_columns in itertools.combinations(
                range(matrix.cols), rank + 1
            ):
                assert (
                    sp.factor(
                        matrix.extract(larger_rows, larger_columns).det()
                    )
                    == 0
                )

    return {
        "rank": rank,
        "witness_rows": list(rows),
        "witness_columns": list(columns),
        "witness_determinant": str(determinant),
        "all_larger_minors_zero": rank < 4,
    }


def leading_plane_classification() -> dict[str, object]:
    pi, theta = sp.symbols("pi theta", nonzero=True)
    deep, boundary, kernel, (c0, c1, c2) = case_planes(pi, theta)
    assert_support(nonzero_support(tensor(deep)), {"0111": 2 * c1 * c2})
    assert_support(
        nonzero_support(tensor(boundary)),
        {
            "0111": -2 * c0 * theta * c1 * c2,
            "1111": -2 * c0 * pi * c1 * c2,
        },
    )
    expected_boundary_plucker = (
        c0 * pi * c1,
        -c0 * theta * c2,
        -c0 * (pi - theta),
        c1 * c2,
        -c1,
        c2,
    )
    assert tuple(sp.factor(value) for value in wedge(*boundary[0])) == (
        tuple(sp.factor(value) for value in expected_boundary_plucker)
    )
    boundary_kernel = tuple(
        sp.factor(
            (-c0 * pi) * boundary[0][0][index]
            - (-c0 * theta) * boundary[0][1][index]
        )
        for index in range(4)
    )
    assert boundary_kernel == tuple(sp.factor(-c0 * value) for value in kernel)

    e = deep[0][0]
    assert sp.Matrix((boundary[0][0], boundary[0][1], e)).extract(
        range(3), (0, 1, 2)
    ).det() == c1 * c2

    for left, right in ((1, 2), (1, 3), (2, 3)):
        matrix = product_matrix(boundary[left], boundary[right])
        assert matrix.rank() == 3
        nullspace = matrix.nullspace()
        assert len(nullspace) == 1
        assert tuple(nullspace[0]) == (1, 0, 0, 0)

    common_three = ((0, 1, 3), (1, 2, 3))
    full_four = ((0, 1, 2, 3), (0, 1, 2, 3))
    witness_catalog = {
        "P<Q": {
            "residues": (pi, sp.Integer(0)),
            "allowed": (pi,),
            "deep": (
                (2, (0, 2), (1, 2)),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
            "boundary": (
                (3, (0, 1, 2), (0, 2, 3)),
                (4, *full_four),
                (4, *full_four),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
        },
        "Q<P": {
            "residues": (sp.Integer(0), theta),
            "allowed": (theta,),
            "deep": (
                (3, *common_three),
                (2, (1, 2), (1, 2)),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
            "boundary": (
                (4, *full_four),
                (3, (0, 1, 2), (0, 1, 2)),
                (4, *full_four),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
        },
        "P=Q,S=R": {
            "residues": (pi, theta),
            "allowed": (pi, theta, pi - theta),
            "deep": (
                (3, *common_three),
                (3, *common_three),
                (3, (0, 2, 4), (1, 2, 3)),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
            "boundary": (
                (4, *full_four),
                (4, *full_four),
                (4, *full_four),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
        },
        "P=Q,S>R": {
            "residues": (pi, pi),
            "allowed": (pi,),
            "deep": (
                (3, *common_three),
                (3, *common_three),
                (2, (0, 1), (1, 2)),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
            "boundary": (
                (4, *full_four),
                (4, *full_four),
                (3, (0, 1, 2), (0, 1, 2)),
                (3, *common_three),
                (3, *common_three),
                (3, *common_three),
            ),
        },
    }
    profiles: dict[str, object] = {}
    rank_certificates: dict[str, object] = {}
    for name, case in witness_catalog.items():
        deep_case, boundary_case, _, case_scalars = case_planes(*case["residues"])
        allowed = (*case_scalars, *case["allowed"])
        face_certificates: dict[str, object] = {}
        face_profiles: dict[str, list[int]] = {}
        for face_name, planes in (
            ("deep", deep_case),
            ("boundary", boundary_case),
        ):
            certificates: dict[str, object] = {}
            ranks: list[int] = []
            for pair, witness in zip(
                PAIRS, case[face_name], strict=True
            ):
                rank, rows, columns = witness
                ranks.append(rank)
                certificates[f"{pair[0]}{pair[1]}"] = fixed_rank_certificate(
                    product_matrix(planes[pair[0]], planes[pair[1]]),
                    rank,
                    rows,
                    columns,
                    allowed,
                )
            face_certificates[face_name] = certificates
            face_profiles[face_name] = ranks
        assert min(face_profiles["boundary"]) >= 3
        profiles[name] = {
            "deep_x0<-R": face_profiles["deep"],
            "boundary_x0=-R": face_profiles["boundary"],
        }
        rank_certificates[name] = face_certificates

    return {
        "plus_centre_active_rows": {
            "v1": "c1*A+C",
            "v2": "c2*B+C",
            "v3": "c1*A+c2*B",
        },
        "leading_kernel": "pi0*c1*A-theta0*c2*B-(pi0-theta0)*C",
        "residue_cases": {
            "P<Q": "(pi0,theta0)=(pi,0)",
            "Q<P": "(pi0,theta0)=(0,theta)",
            "P=Q,S=R": "pi0=pi, theta0=theta, pi!=theta",
            "P=Q,S>R": "pi0=theta0=pi",
            "P=infinity": "same leading cell as Q<P",
            "Q=infinity": "same leading cell as P<Q",
            "P=Q=infinity": "identically zero restriction",
        },
        "deep_face": {
            "U0": "<e,kernel>",
            "pure_support": {"0111": "2*c1*c2"},
            "route": "component 18 common-singleton closure",
        },
        "boundary_face": {
            "U0": [
                "<-c0*theta0*e+c1*A-C, -c0*pi0*e+c2*B-C>",
            ],
            "pure_support": {
                "0111": "-2*c0*theta0*c1*c2",
                "1111": "-2*c0*pi0*c1*c2",
            },
            "contains_common_singleton_e": False,
            "route": "component 16 by the fully kernel-kernel triangle theorem",
        },
        "pair_profiles_plus_centre": profiles,
        "fixed_minor_rank_certificates": rank_certificates,
        "minus_centre_rules": {
            "coordinate_swap_model": "apply P<->Q and x1<->x2",
            "diagonal_plus_mode_swap_model": (
                "preserve P,Q and x1,x2; exchange modes 1 and 2"
            ),
        },
    }


def source_text_audit() -> None:
    component = " ".join(COMPONENT.read_text(encoding="utf-8").split())
    common = " ".join(COMMON_SINGLETON.read_text(encoding="utf-8").split())
    triple = " ".join(TRIPLE_KERNEL.read_text(encoding="utf-8").split())
    assert "T_0111=2(p-q+1), T_1111=-2q(q-1)" in component
    assert "U0=span(e,ell), Ui=span(e,vi), i=1,2,3" in common
    assert "if `U_0` contains the common singleton" in triple
    assert "otherwise it belongs to component sixteen" in triple


def main() -> None:
    source_text_audit()
    payload = {
        "status": "pass",
        "role": "proof_b",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "DERIVED",
        "scope": (
            "complete diagonal source-torus valuative classification over "
            "the transverse component-20 base points (0,1) and (-1,0)"
        ),
        "inputs": {
            path.name: sha256(path)
            for path in (COMPONENT, COMMON_SINGLETON, TRIPLE_KERNEL)
        },
        "method": (
            "fresh polynomial Pluecker and subset-algebra tensor reconstruction; "
            "factor-covector kernel normalization; exact min-plus inequalities "
            "with rational-linear unsatisfiability checks; direct limit planes; "
            "fixed symbolic minor rank certificates"
        ),
        "command": (
            "uv run --with sympy --with z3-solver python "
            f"{SCRIPT.name}"
        ),
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "raw_family_and_symmetry": raw_family_and_symmetry(),
        "fan_certificate": fan_certificate(),
        "leading_plane_classification": leading_plane_classification(),
        "finite_field_computation_used": False,
        "broad_grid_used": False,
        "H31_or_H22_claim_made": False,
        "global_Krenn_Gu_resolved": False,
        "limitations": (
            "diagonal source tori only; no non-diagonal or arbitrary GL4 arcs, "
            "no component-intersection equality, marked H31, weighted H22, "
            "component exhaustiveness, arbitrary-order reduction, prize graph, "
            "or global Krenn-Gu conclusion"
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
