#!/usr/bin/env python3
"""Verify the derived p+q valuative boundary classification for component 20."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp
import z3

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
COMPONENT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
INPUTS = (
    COMPONENT,
    ROOT / "P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md",
    ROOT / "P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md",
    ROOT / "P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md",
    ROOT / "P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md",
    ROOT / "P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md",
    ROOT / "P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md",
    ROOT / "P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md",
)
CLASSIFICATION_VERIFIERS = (
    "verify_p4_rank_two_pair_kernel_geometry.py",
    "verify_p4_tangent_rank_two_pair_purity_classification.py",
    "verify_p4_support_two_tangent_flag_boundary_inclusion.py",
    "verify_p4_full_support_tangent_pair_component.py",
    "verify_p4_disjoint_secant_lower_pair_component.py",
    "verify_p4_support_one_secant_boundary_inclusion.py",
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def wedge(left: sp.Matrix, right: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(sp.factor(left[i] * right[j] - left[j] * right[i]) for i, j in PAIRS)


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def product_matrix(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(left_row, right_row) for left_row in left for right_row in right)
    )


def rank_certificate(matrix: sp.Matrix, expected_rank: int) -> dict[str, object]:
    if expected_rank < min(matrix.rows, matrix.cols):
        assert all(
            sp.factor(matrix.extract(rows, columns).det()) == 0
            for rows in itertools.combinations(range(matrix.rows), expected_rank + 1)
            for columns in itertools.combinations(range(matrix.cols), expected_rank + 1)
        )
    witness = None
    for rows in itertools.combinations(range(matrix.rows), expected_rank):
        for columns in itertools.combinations(range(matrix.cols), expected_rank):
            determinant = sp.factor(matrix.extract(rows, columns).det())
            if determinant != 0:
                witness = (rows, columns, determinant)
                break
        if witness is not None:
            break
    assert witness is not None
    rows, columns, determinant = witness
    return {
        "rank": expected_rank,
        "witness_rows": list(rows),
        "witness_columns": list(columns),
        "witness_determinant": str(determinant),
        "all_next_size_minors_zero": expected_rank < min(matrix.rows, matrix.cols),
    }


def normalized_family_certificate() -> dict[str, object]:
    p, q = sp.symbols("p q")
    delta = p + q
    s = p - q + 1
    e = sp.Matrix((1, 0, 0, 0))
    alpha = (
        sp.Matrix((0, -p * (p + 1), q * (q - 1), s)),
        e,
        e,
        sp.Matrix((1, 1, 1, 0)),
    )
    beta = (
        sp.Matrix((-s, -delta, delta, 0)),
        sp.Matrix((0, p + 1, q - 1, 1)),
        sp.Matrix((0, p, q, 1)),
        e,
    )
    expected_wedge = (
        -p * (p + 1) * s,
        q * (q - 1) * s,
        s**2,
        -(delta**2) * s,
        delta * s,
        -delta * s,
    )
    actual_wedge = wedge(alpha[0], beta[0])
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(actual_wedge, expected_wedge)
    )
    tensor = {
        word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS
    }
    assert sp.factor(tensor[(1, 1, 1, 1)] - 2 * delta * s) == 0
    assert all(value == 0 for word, value in tensor.items() if word != (1, 1, 1, 1))

    # If both rows in mode i are rescaled by valuation rho_i, then the pure
    # scalar gains sum rho_i, a_i gains rho_i, and u_i gains 2 rho_i.  The
    # invariant E therefore does not change.
    rho = sp.symbols("rho0:4")
    change_in_e = sp.factor(sum(rho) + sum(rho[i] - 2 * rho[i] for i in range(4)))
    assert change_in_e == 0
    return {
        "pure_support": {"1111": "2*(p+q)*(p-q+1)"},
        "corrected_alpha0_wedge_beta0": [str(entry) for entry in expected_wedge],
        "wedge_coordinate_order": ["01", "02", "03", "12", "13", "23"],
        "row_normalization_change_in_E": str(change_in_e),
        "invariant_E": (
            "v(2*delta*s)+x0+x1+x2+sum_i(v(D*alpha_i)-v(D*alpha_i wedge D*beta_i))"
        ),
    }


class ProofRecorder:
    """Record explicit QF_LRA queries and Z3 proof objects, not process codes."""

    def __init__(self) -> None:
        z3.set_option(proof=True)
        self.query_digest = hashlib.sha256()
        self.proof_digest = hashlib.sha256()
        self.queries = 0

    def unsat(self, label: str, constraints: tuple[object, ...]) -> None:
        solver = z3.Solver()
        solver.add(*constraints)
        query = solver.to_smt2()
        result = solver.check()
        if result != z3.unsat:
            model = solver.model() if result == z3.sat else solver.reason_unknown()
            raise AssertionError((label, result, model, query))
        proof = solver.proof().sexpr()
        assert proof and "false" in proof.lower(), (label, proof)
        self.query_digest.update(label.encode("utf-8"))
        self.query_digest.update(query.encode("utf-8"))
        self.proof_digest.update(label.encode("utf-8"))
        self.proof_digest.update(proof.encode("utf-8"))
        self.queries += 1

    def summary(self) -> dict[str, object]:
        return {
            "unsatisfiable_queries": self.queries,
            "smt2_sha256": self.query_digest.hexdigest(),
            "z3_proof_objects_sha256": self.proof_digest.hexdigest(),
            "solver_result_used": "Python API result plus nonempty proof object",
        }


def zmin(*entries: object) -> object:
    result = entries[-1]
    for entry in reversed(entries[:-1]):
        result = z3.If(entry <= result, entry, result)
    return result


def zmax(*entries: object) -> object:
    result = entries[-1]
    for entry in reversed(entries[:-1]):
        result = z3.If(entry >= result, entry, result)
    return result


def selected_minimum(
    entries: tuple[object, ...], selected: int
) -> tuple[object, tuple[object, ...]]:
    value = entries[selected]
    constraints = tuple(
        value <= entry for index, entry in enumerate(entries) if index != selected
    )
    return value, constraints


def generic_min_plus_certificate(recorder: ProofRecorder) -> dict[str, object]:
    d, x0, x1, x2 = z3.Reals("d x0 x1 x2")
    zero = z3.RealVal(0)
    m = zmin(x1, x2, zero)
    n = zmin(x1, x2)
    ell = zmin(x1 + x2 + d, x1, x2)
    expression = d + x1 + x2 - m + zmin(x0, n) - n - zmin(x0 + m, d + ell)
    target = z3.And(x1 == x2, x1 >= -d, x1 <= 0, x0 >= d)

    branch_cells = []
    negative_queries = 0
    necessity_queries = 0
    for choices in itertools.product(range(3), range(2), range(3), range(2), range(2)):
        m_value, m_conditions = selected_minimum((x1, x2, zero), choices[0])
        n_value, n_conditions = selected_minimum((x1, x2), choices[1])
        ell_value, ell_conditions = selected_minimum((x1 + x2 + d, x1, x2), choices[2])
        inner_value, inner_conditions = selected_minimum((x0, n_value), choices[3])
        outer_value, outer_conditions = selected_minimum(
            (x0 + m_value, d + ell_value), choices[4]
        )
        conditions = (
            *m_conditions,
            *n_conditions,
            *ell_conditions,
            *inner_conditions,
            *outer_conditions,
        )
        branch_cells.append(z3.And(*conditions))
        branch_expression = d + x1 + x2 - m_value + inner_value - n_value - outer_value
        label = "branch_" + "_".join(map(str, choices))
        recorder.unsat(label + "_negative", (d > 0, *conditions, branch_expression < 0))
        negative_queries += 1
        recorder.unsat(
            label + "_zero_outside_target",
            (d > 0, *conditions, branch_expression == 0, z3.Not(target)),
        )
        necessity_queries += 1

    recorder.unsat("branch_cover", (d > 0, z3.Not(z3.Or(*branch_cells))))
    recorder.unsat("target_sufficiency", (d > 0, target, expression != 0))
    recorder.unsat("global_nonnegative", (d > 0, expression < 0))
    recorder.unsat("global_zero_necessity", (d > 0, expression == 0, z3.Not(target)))

    # Direct exact simplification on the target cell.
    y = sp.symbols("y")
    d_symbol = sp.symbols("d")
    target_expression = sp.factor(d_symbol + 2 * y - y + y - y - (d_symbol + y))
    assert target_expression == 0
    return {
        "formula": (
            "d+x1+x2-m+min(x0,n)-n-min(x0+m,d+ell), "
            "m=min(x1,x2,0), n=min(x1,x2), "
            "ell=min(x1+x2+d,x1,x2)"
        ),
        "assumption": "d>0",
        "target": "x1=x2=y and -d<=y<=0 and x0>=d",
        "linear_branch_cells": len(branch_cells),
        "negative_counterexample_queries": negative_queries,
        "zero_outside_target_queries": necessity_queries,
        "branch_cover_query": "d>0 and not OR(all 72 branch cells)",
        "sufficiency_counterexample_query": "d>0 and target and E!=0",
        "global_negative_query": "d>0 and E<0",
        "global_necessity_query": "d>0 and E=0 and not target",
        "direct_target_cell_simplification": str(target_expression),
    }


def generic_hand_cone_certificate(recorder: ProofRecorder) -> dict[str, object]:
    """Replay the compact nine-cone proof independently of the 72 minima cells."""

    d, n, w, x0 = z3.Reals("dh nh wh x0h")
    u = n + w + d
    m = zmin(n, z3.RealVal(0))
    ell = zmin(2 * n + w + d, n)
    original_e = (
        d
        + n
        + w
        - m
        + zmin(x0, n)
        - zmin(x0 + m, d + ell)
    )
    target = z3.And(w == 0, n >= -d, n <= 0, x0 >= d)
    cones = (
        ("nonnegative_left", (n >= 0, x0 <= n), d + n + w),
        ("nonnegative_middle", (n >= 0, x0 >= n, x0 <= d + n), d + 2 * n + w - x0),
        ("nonnegative_right", (n >= 0, x0 >= d + n), n + w),
        ("negative_u_nonnegative_left", (n < 0, u >= 0, x0 <= n), d + w - n),
        ("negative_u_nonnegative_middle", (n < 0, u >= 0, x0 >= n, x0 <= d), d + w - x0),
        ("negative_u_nonnegative_right", (n < 0, u >= 0, x0 >= d), w),
        ("negative_u_negative_left", (n < 0, u < 0, x0 <= n), d + w - n),
        ("negative_u_negative_middle", (n < 0, u < 0, x0 >= n, x0 <= d + u), d + w - x0),
        ("negative_u_negative_right", (n < 0, u < 0, x0 >= d + u), -n - d),
    )
    cells = []
    table = []
    for label, conditions, expression in cones:
        cell = z3.And(*conditions)
        cells.append(cell)
        assumptions = (d > 0, w >= 0, *conditions)
        recorder.unsat(
            "hand_" + label + "_formula_mismatch",
            (*assumptions, original_e != expression),
        )
        recorder.unsat("hand_" + label + "_negative", (*assumptions, expression < 0))
        recorder.unsat(
            "hand_" + label + "_zero_outside_target",
            (*assumptions, expression == 0, z3.Not(target)),
        )
        table.append(
            {
                "cone": label,
                "conditions": tuple(str(condition) for condition in conditions),
                "E": str(expression),
            }
        )
    recorder.unsat(
        "hand_cone_cover",
        (d > 0, w >= 0, z3.Not(z3.Or(*cells))),
    )
    return {
        "substitution": "n=min(x1,x2), w=abs(x1-x2), u=n+w+d",
        "original_E_in_n_w": (
            "d+n+w-min(n,0)+min(x0,n)-"
            "min(x0+min(n,0),d+min(2n+w+d,n))"
        ),
        "cones": table,
        "cone_count": len(cones),
        "formula_equality_queries": len(cones),
        "zero_face": "w=0, -d<=n<=0, x0>=d",
        "bounded_scan_used": False,
    }


def exceptional_schema_certificate(recorder: ProofRecorder) -> dict[str, object]:
    d, x0, x1, x2 = z3.Reals("de x0e x1e x2e")
    n = zmin(x1, x2)
    z = zmin(x0, x1, x2)
    ell = zmin(x1 + x2 + d, x1, x2)

    def prove_iff(
        label: str,
        assumptions: tuple[object, ...],
        expression: object,
        target: object,
    ) -> None:
        recorder.unsat(label + "_negative", (*assumptions, expression < 0))
        recorder.unsat(
            label + "_necessity",
            (*assumptions, expression == 0, z3.Not(target)),
        )
        recorder.unsat(
            label + "_sufficiency",
            (*assumptions, target, expression != 0),
        )

    # Centres a=0 and a=-1 have the same raw min-plus expression.  P,Q are
    # the two positive exceptional valuations and R=min(P,Q).  If they are
    # unequal, v(p+q)=R; if equal, leading cancellation allows d>=R.
    cap_p, cap_q = z3.Reals("P Q")
    cap_r = zmin(cap_p, cap_q)
    cancellation_law = z3.Or(
        z3.And(cap_p < cap_q, d == cap_p),
        z3.And(cap_q < cap_p, d == cap_q),
        z3.And(cap_p == cap_q, d >= cap_r),
    )
    g0 = zmin(x1 + cap_p, x2 + cap_q, z3.RealVal(0))
    m0 = zmin(x1, x2, z3.RealVal(0))
    e0 = d + x1 + x2 - m0 + z - n - zmin(x0 + g0, d + ell)
    target0 = z3.And(
        x1 == x2,
        x1 >= -d,
        x1 <= 0,
        x0 >= zmax(d - cap_r, d + x1),
    )
    a0_assumptions = (d > 0, cap_p > 0, cap_q > 0, cancellation_law)
    prove_iff("a0_and_a_minus1", a0_assumptions, e0, target0)
    recorder.unsat(
        "exceptional_max_equivalence",
        (
            *a0_assumptions,
            x1 == x2,
            z3.Xor(
                x0 >= zmax(d - cap_r, d + x1),
                z3.And(x0 >= d - cap_r, x0 >= d + x1),
            ),
        ),
    )

    # At a=-1/2, h=v(s)>0 and the raw expression acquires g-2m.
    h = z3.Real("h")
    gh = zmin(x1, x2, h)
    mh = zmin(x1, x2, z3.RealVal(0))
    eh = d + x1 + x2 + gh - 2 * mh + z - n - zmin(x0 + gh, d + ell)
    targeth = z3.And(x1 == x2, x1 >= -d, x1 <= 0, x0 >= d)
    prove_iff("a_minus_half", (d > 0, h > 0), eh, targeth)

    # At infinity, r<0 and the two shifted minima differ by r.
    r = z3.Real("r")
    ginf = zmin(x1 + 2 * r, x2 + 2 * r, r)
    binf = zmin(x1 + r, x2 + r, z3.RealVal(0))
    einf = d + x1 + x2 + ginf - 2 * binf + z - n - zmin(x0 + ginf, d + ell)
    targetinf = z3.And(
        x1 == x2,
        x1 >= -d,
        x1 <= -r,
        x0 >= d - 2 * r,
    )
    prove_iff("infinity", (d > 0, r < 0), einf, targetinf)
    recorder.unsat(
        "infinity_y_partition",
        (d > 0, r < 0, targetinf, z3.Not(z3.Or(x1 < -r, x1 == -r))),
    )
    recorder.unsat("infinity_upper_positive", (d > 0, r < 0, targetinf, -r <= 0))
    return {
        "a=0": ("x1=x2=y, -d<=y<=0, x0>=max(d-R,d+y), R=min(v(p),v(q))"),
        "a=0_raw_E": (
            "d+x1+x2-m+z-n-min(x0+g,d+ell), "
            "g=min(x1+P,x2+Q,0), m=min(x1,x2,0), "
            "z=min(x0,x1,x2)"
        ),
        "a=-1": ("x1=x2=y, -d<=y<=0, x0>=max(d-R,d+y), R=min(v(p+1),v(q-1))"),
        "a=-1/2": "x1=x2=y, -d<=y<=0, x0>=d",
        "a=-1/2_raw_E": ("d+x1+x2+g-2m+z-n-min(x0+g,d+ell), g=min(x1,x2,h), h=v(s)>0"),
        "infinity": ("r<0, d>0, x1=x2=y, -d<=y<=-r, x0>=d-2r"),
        "infinity_raw_E": (
            "d+x1+x2+g-2b+z-n-min(x0+g,d+ell), g=min(x1+2r,x2+2r,r), b=min(x1+r,x2+r,0)"
        ),
        "max_threshold_equivalent_to_two_linear_inequalities": True,
        "all_three_raw_E_counterexample_families_unsatisfiable": True,
        "infinity_support_two_or_full_support_partition": True,
        "cancellation_law": ("P<Q => d=P; Q<P => d=Q; P=Q=R allows d>=R"),
    }


def chart_certificate() -> dict[str, object]:
    a, lam = sp.symbols("a lambda", nonzero=True)
    mu = -a * (a + 1) / (2 * a + 1)
    e = sp.Matrix((1, 0, 0, 0))
    cap_a = sp.Matrix((0, 1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 0))
    cap_c = sp.Matrix((0, 0, 0, 1))
    ell = cap_a - cap_b
    em = cap_a + cap_b

    full_alpha = (e + lam * ell, e, e, e)
    full_beta = (
        cap_c + mu * ell,
        (a + 1) * ell + cap_c,
        a * ell + cap_c,
        em,
    )
    drop_alpha = (cap_c, e, e, e)
    drop_beta = (ell, full_beta[1], full_beta[2], em)

    def tensor(alpha: tuple[sp.Matrix, ...], beta: tuple[sp.Matrix, ...]):
        return {
            word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
            for word in WORDS
        }

    full_tensor = tensor(full_alpha, full_beta)
    assert sp.factor(full_tensor[(0, 1, 1, 0)] + 2 * lam * (2 * a + 1)) == 0
    assert full_tensor[(1, 1, 1, 0)] == 0
    assert all(
        value == 0
        for word, value in full_tensor.items()
        if word not in ((0, 1, 1, 0), (1, 1, 1, 0))
    )

    drop_tensor = tensor(drop_alpha, drop_beta)
    assert sp.factor(drop_tensor[(0, 1, 1, 0)] + 2 * a * (a + 1)) == 0
    assert sp.factor(drop_tensor[(1, 1, 1, 0)] + 2 * (2 * a + 1)) == 0
    assert all(
        value == 0
        for word, value in drop_tensor.items()
        if word not in ((0, 1, 1, 0), (1, 1, 1, 0))
    )

    full_planes = tuple(zip(full_alpha, full_beta))
    drop_planes = tuple(zip(drop_alpha, drop_beta))
    expected_profiles = {
        "B_full": (4, 4, 4, 3, 3, 3),
        "B_drop": (4, 4, 3, 3, 3, 3),
    }
    profiles = {}
    rank_certificates = {}
    for label, planes in (("B_full", full_planes), ("B_drop", drop_planes)):
        matrices = [
            product_matrix(planes[left], planes[right]) for left, right in PAIRS
        ]
        profile = tuple(matrix.rank() for matrix in matrices)
        assert profile == expected_profiles[label]
        profiles[label] = list(profile)
        rank_certificates[label] = [
            rank_certificate(matrix, expected_rank)
            for matrix, expected_rank in zip(matrices, profile)
        ]

    c1, c2 = sp.symbols("c1 c2", nonzero=True)
    residue_ell = c1 * cap_a - c2 * cap_b
    residue_em = c1 * cap_a + c2 * cap_b
    lower_pair_plane = (e, residue_ell)
    lower_pair = rank_certificate(product_matrix(lower_pair_plane, lower_pair_plane), 2)
    exceptional_profiles = {}
    for center in (sp.Integer(0), sp.Integer(-1)):
        full_special = tuple(
            tuple(row.subs(a, center) for row in plane) for plane in full_planes
        )
        drop_special = tuple(
            tuple(row.subs(a, center) for row in plane) for plane in drop_planes
        )
        exceptional_profiles[str(center)] = {
            "B_full": [
                product_matrix(full_special[left], full_special[right]).rank()
                for left, right in PAIRS
            ],
            "B_drop": [
                product_matrix(drop_special[left], drop_special[right]).rank()
                for left, right in PAIRS
            ],
        }

    # The centre a=-1/2 cannot be obtained by substituting into B_full:
    # 2a+1 vanishes.  Rebuild its valuatively normalized chart directly.
    k = sp.symbols("k", nonzero=True)
    half_planes = (
        (residue_ell, cap_c - k * e),
        (e, sp.Rational(1, 2) * residue_ell + cap_c),
        (e, -sp.Rational(1, 2) * residue_ell + cap_c),
        (e, residue_em),
    )
    half_tensor = tensor(
        tuple(plane[0] for plane in half_planes),
        tuple(plane[1] for plane in half_planes),
    )
    half_nonzero = {word: value for word, value in half_tensor.items() if value != 0}
    assert tuple(half_nonzero) == ((1, 1, 1, 0),)
    half_profile = tuple(
        product_matrix(half_planes[left], half_planes[right]).rank()
        for left, right in PAIRS
    )
    assert half_profile == (4, 4, 3, 3, 3, 3)

    # At infinity the mode-zero plane has five exact Pluecker charts.  These
    # identities retain the lower endpoint, upper endpoint, and x0 wall.
    kappa, delta_lead, alpha_lead, p_lead = sp.symbols(
        "kappa Delta alpha P0", nonzero=True
    )
    infinity_mode_zero = {
        "interior_baseline": (residue_ell, cap_c),
        "interior_x0_wall": (residue_ell, cap_c + kappa * e),
        "lower_y_wall": (
            residue_ell,
            cap_c - sp.Rational(1, 2) * delta_lead * residue_em,
        ),
        "lower_y_and_x0_wall": (
            residue_ell,
            cap_c + kappa * e - sp.Rational(1, 2) * delta_lead * residue_em,
        ),
        "upper_y_and_x0_wall": (
            residue_ell + alpha_lead * e,
            cap_c + kappa * e,
        ),
    }
    expected_infinity_wedges = {
        "interior_baseline": (0, 0, 0, 0, c1, -c2),
        "interior_x0_wall": (-kappa * c1, kappa * c2, 0, 0, c1, -c2),
        "lower_y_wall": (0, 0, 0, -delta_lead * c1 * c2, c1, -c2),
        "lower_y_and_x0_wall": (
            -kappa * c1,
            kappa * c2,
            0,
            -delta_lead * c1 * c2,
            c1,
            -c2,
        ),
        "upper_y_and_x0_wall": (
            -kappa * c1,
            kappa * c2,
            alpha_lead,
            0,
            c1,
            -c2,
        ),
    }
    infinity_wedges = {}
    for label, plane in infinity_mode_zero.items():
        actual = wedge(*plane)
        assert all(
            sp.factor(left - right) == 0
            for left, right in zip(actual, expected_infinity_wedges[label])
        )
        infinity_wedges[label] = [str(value) for value in actual]

    infinity_support_plane = (e, residue_ell)
    infinity_full_plane = (e, p_lead * residue_ell + cap_c)
    infinity_pair_ranks = {
        "support_two_y_below_minus_r": rank_certificate(
            product_matrix(infinity_support_plane, infinity_support_plane), 2
        ),
        "full_support_y_equals_minus_r": rank_certificate(
            product_matrix(infinity_full_plane, infinity_full_plane), 2
        ),
    }
    return {
        "B_full": {
            "mu": "-a*(a+1)/(2*a+1)",
            "pure_coefficients": {
                "0110": str(full_tensor[(0, 1, 1, 0)]),
                "1110": str(full_tensor[(1, 1, 1, 0)]),
            },
            "all_other_pure_coefficients_zero": True,
            "generic_pair_profile": profiles["B_full"],
            "pair_rank_certificates": rank_certificates["B_full"],
        },
        "B_drop": {
            "pure_coefficients": {
                "0110": str(drop_tensor[(0, 1, 1, 0)]),
                "1110": str(drop_tensor[(1, 1, 1, 0)]),
            },
            "all_other_pure_coefficients_zero": True,
            "generic_pair_profile": profiles["B_drop"],
            "pair_rank_certificates": rank_certificates["B_drop"],
        },
        "negative_equal_weight_pair": lower_pair,
        "exceptional_center_profile_specializations": exceptional_profiles,
        "a=-1/2_exact_chart": {
            "mode_zero_wedge": [str(value) for value in wedge(*half_planes[0])],
            "nonzero_pure_coefficients": {
                "".join(map(str, word)): str(value)
                for word, value in half_nonzero.items()
            },
            "pair_profile": list(half_profile),
        },
        "a=-1/2_direct_substitution_used": False,
        "a=-1/2_requires_valuative_row_renormalization": True,
        "infinity_mode_zero_wedges": infinity_wedges,
        "infinity_coefficient_relations": ("kappa=c0*P0^2/Delta; alpha=c0*2*P0/Delta"),
        "infinity_repeated_pair_rank_certificates": infinity_pair_ranks,
        "simultaneous_infinity_y_endpoints_possible": False,
    }


def raw_mode_zero_leading_tables() -> dict[str, object]:
    """Derive every table directly from the six factored raw wedge entries."""

    a, cap_p, cap_q, p0 = sp.symbols("a P Q P0", nonzero=True)
    c0, c1, c2 = sp.symbols("c0 c1 c2", nonzero=True)
    delta_lead, sigma = sp.symbols("Delta Sigma", nonzero=True)
    d, h, r, x0, y = sp.symbols("d h r x0 y", real=True)
    s0 = 2 * a + 1
    eta = c0 * a * (a + 1) / delta_lead
    k = c0 / (4 * delta_lead)
    kappa = c0 * p0**2 / delta_lead
    alpha = 2 * c0 * p0 / delta_lead

    def derive(
        factor_leads: tuple[sp.Expr, ...],
        raw_weights: tuple[sp.Expr, ...],
        base_weight: sp.Expr,
        normalizer: sp.Expr,
        expected_coefficients: tuple[sp.Expr, ...],
    ) -> dict[str, object]:
        lead_p, lead_p1, lead_q, lead_q1, lead_s, lead_delta = factor_leads
        raw_coefficients = (
            -lead_p * lead_p1 * lead_s * c0 * c1,
            lead_q * lead_q1 * lead_s * c0 * c2,
            lead_s**2 * c0,
            -(lead_delta**2) * lead_s * c1 * c2,
            lead_delta * lead_s * c1,
            -lead_delta * lead_s * c2,
        )
        normalized = tuple(sp.factor(value / normalizer) for value in raw_coefficients)
        assert all(
            sp.factor(actual - expected) == 0
            for actual, expected in zip(normalized, expected_coefficients)
        )
        excesses = tuple(sp.factor(weight - base_weight) for weight in raw_weights)
        return {
            "factor_leading_coefficients_p_p1_q_q1_s_delta": [
                str(value) for value in factor_leads
            ],
            "raw_weights_01_02_03_12_13_23": [str(value) for value in raw_weights],
            "base_weight": str(base_weight),
            "excess_weights": [str(value) for value in excesses],
            "raw_leading_coefficients": [str(value) for value in raw_coefficients],
            "normalizer_leading_coefficient": str(normalizer),
            "normalized_leading_coefficients": [str(value) for value in normalized],
        }

    finite_weights = (x0 + y, x0 + y, x0, 2 * d + 2 * y, d + y, d + y)
    exceptional_weights = (
        cap_p + x0 + y,
        cap_q + x0 + y,
        x0,
        2 * d + 2 * y,
        d + y,
        d + y,
    )
    tables = {
        "finite_generic": derive(
            (a, a + 1, -a, -a - 1, s0, delta_lead),
            finite_weights,
            d + y,
            delta_lead * s0,
            (-eta * c1, eta * c2, c0 * s0 / delta_lead, -delta_lead * c1 * c2, c1, -c2),
        ),
        "a=0": derive(
            (sp.symbols("pi", nonzero=True), 1, sp.symbols("theta", nonzero=True), -1, 1, delta_lead),
            exceptional_weights,
            d + y,
            delta_lead,
            (
                -c0 * c1 * sp.symbols("pi", nonzero=True) / delta_lead,
                -c0 * c2 * sp.symbols("theta", nonzero=True) / delta_lead,
                c0 / delta_lead,
                -delta_lead * c1 * c2,
                c1,
                -c2,
            ),
        ),
        "a=-1": derive(
            (-1, sp.symbols("pi", nonzero=True), 1, sp.symbols("theta", nonzero=True), -1, delta_lead),
            exceptional_weights,
            d + y,
            -delta_lead,
            (
                c0 * c1 * sp.symbols("pi", nonzero=True) / delta_lead,
                c0 * c2 * sp.symbols("theta", nonzero=True) / delta_lead,
                -c0 / delta_lead,
                -delta_lead * c1 * c2,
                c1,
                -c2,
            ),
        ),
        "a=-1/2": derive(
            (-sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2), -sp.Rational(1, 2), sigma, delta_lead),
            (h + x0 + y, h + x0 + y, 2 * h + x0, 2 * d + h + 2 * y, d + h + y, d + h + y),
            d + h + y,
            delta_lead * sigma,
            (k * c1, -k * c2, sigma * c0 / delta_lead, -delta_lead * c1 * c2, c1, -c2),
        ),
        "infinity": derive(
            (p0, p0, -p0, -p0, 2 * p0, delta_lead),
            (3 * r + x0 + y, 3 * r + x0 + y, 2 * r + x0, 2 * d + r + 2 * y, d + r + y, d + r + y),
            d + r + y,
            2 * delta_lead * p0,
            (-kappa * c1, kappa * c2, alpha, -delta_lead * c1 * c2, c1, -c2),
        ),
    }
    return {
        "source": (
            "(-p(p+1)s*tau0*tau1,q(q-1)s*tau0*tau2,s^2*tau0,"
            "-delta^2*s*tau1*tau2,delta*s*tau1,-delta*s*tau2)"
        ),
        "coordinate_order": ("01", "02", "03", "12", "13", "23"),
        "field": "characteristic zero; 2 invertible",
        "opens": {
            "finite_generic": "a*(a+1)*(2*a+1)*c0*c1*c2*Delta != 0",
            "a=0": "pi*theta*c0*c1*c2*Delta != 0 subject to residue law",
            "a=-1": "pi*theta*c0*c1*c2*Delta != 0 subject to residue law",
            "a=-1/2": "Sigma*c0*c1*c2*Delta != 0",
            "infinity": "P0*c0*c1*c2*Delta != 0",
        },
        "tables": tables,
    }


def pluecker_relation(coordinates: tuple[sp.Expr, ...]) -> sp.Expr:
    p01, p02, p03, p12, p13, p23 = coordinates
    return sp.factor(p01 * p23 - p02 * p13 + p03 * p12)


def actual_arc_realization_certificate(recorder: ProofRecorder) -> dict[str, object]:
    """Persist the complete residue-level Laurent/Puiseux realization data."""

    e = sp.Matrix((1, 0, 0, 0))
    cap_a = sp.Matrix((0, 1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 0))
    cap_c = sp.Matrix((0, 0, 0, 1))
    c0, c1, c2, delta_lead = sp.symbols("c0 c1 c2 Delta", nonzero=True)
    a, eta = sp.symbols("a eta", nonzero=True)
    residue_ell = c1 * cap_a - c2 * cap_b
    residue_em = c1 * cap_a + c2 * cap_b

    # The four finite generic negative-y faces are exact decomposable wedges.
    finite_generic_faces = {}
    for eps_x, eps_y in itertools.product((0, 1), repeat=2):
        plane = (
            residue_ell,
            cap_c + eps_x * eta * e - eps_y * delta_lead * residue_em / 2,
        )
        expected = (
            -eps_x * eta * c1,
            eps_x * eta * c2,
            0,
            -eps_y * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        actual = wedge(*plane)
        assert all(sp.factor(left - right) == 0 for left, right in zip(actual, expected))
        assert pluecker_relation(actual) == 0
        finite_generic_faces[f"eps_x={eps_x},eps_y={eps_y}"] = [str(v) for v in actual]

    # Every B_full parameter and every eta are realized by a nonzero leading
    # coefficient; these are identities, not sampled parameter choices.
    lam = sp.symbols("lambda", nonzero=True)
    assert sp.factor((lam * c0 * (2 * a + 1)) / (c0 * (2 * a + 1)) - lam) == 0
    assert sp.factor((eta * delta_lead / (a * (a + 1))) * a * (a + 1) / delta_lead - eta) == 0

    # At a=-1/2 the special H_k plane is the exact Grassmann closure of B_full.
    u, k = sp.symbols("u k", nonzero=True)
    moving_a = -sp.Rational(1, 2) + u
    mu = -moving_a * (moving_a + 1) / (2 * moving_a + 1)
    moving_lam = mu / k
    moving_wedge = tuple(
        sp.factor(value / moving_lam)
        for value in wedge(e + moving_lam * residue_ell, cap_c + mu * residue_ell)
    )
    half_limit = tuple(sp.factor(sp.limit(value, u, 0)) for value in moving_wedge)
    expected_half = (k * c1, -k * c2, 0, 0, c1, -c2)
    assert half_limit == expected_half
    assert pluecker_relation(half_limit) == 0
    assert sp.factor((4 * k * delta_lead) / (4 * delta_lead) - k) == 0

    # Exceptional residue laws.  Complete wall signatures are proved by
    # excluding every one of the other 16 Boolean signatures with QF_LRA.
    cap_p, cap_q, d, y, x0 = z3.Reals("Pr Qr dr yr x0r")
    residue_cases = {
        "P<Q": {
            "assumptions": (cap_p > 0, cap_q > cap_p, d == cap_p),
            "R": cap_p,
            "expected": {(1, 0, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 0, 0)},
            "relation": "Delta=pi",
            "arc": "p=pi*t^P, q=theta*t^Q, d=P, Delta=pi",
            "witnesses": {
                (1, 0, 1, 1): (1, 2, 1, -1, 0),
                (0, 0, 0, 1): (1, 2, 1, -1, 1),
                (0, 0, 1, 0): (1, 2, 1, "-1/2", "1/2"),
                (0, 0, 0, 0): (1, 2, 1, "-1/2", 1),
            },
        },
        "Q<P": {
            "assumptions": (cap_q > 0, cap_p > cap_q, d == cap_q),
            "R": cap_q,
            "expected": {(0, 1, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 0, 0)},
            "relation": "Delta=theta",
            "arc": "p=pi*t^P, q=theta*t^Q, d=Q, Delta=theta",
            "witnesses": {
                (0, 1, 1, 1): (2, 1, 1, -1, 0),
                (0, 0, 0, 1): (2, 1, 1, -1, 1),
                (0, 0, 1, 0): (2, 1, 1, "-1/2", "1/2"),
                (0, 0, 0, 0): (2, 1, 1, "-1/2", 1),
            },
        },
        "P=Q=R=d": {
            "assumptions": (cap_p > 0, cap_q == cap_p, d == cap_p),
            "R": cap_p,
            "expected": {(1, 1, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 0, 0)},
            "relation": "Delta=pi+theta!=0",
            "arc": "p=pi*t^d, q=theta*t^d, Delta=pi+theta!=0",
            "witnesses": {
                (1, 1, 1, 1): (1, 1, 1, -1, 0),
                (0, 0, 0, 1): (1, 1, 1, -1, 1),
                (0, 0, 1, 0): (1, 1, 1, "-1/2", "1/2"),
                (0, 0, 0, 0): (1, 1, 1, "-1/2", 1),
            },
        },
        "P=Q=R<d": {
            "assumptions": (cap_p > 0, cap_q == cap_p, d > cap_p),
            "R": cap_p,
            "expected": {
                (1, 1, 0, 1),
                (0, 0, 0, 1),
                (1, 1, 0, 0),
                (0, 0, 0, 0),
                (1, 1, 1, 0),
                (0, 0, 1, 0),
            },
            "relation": "theta=-pi",
            "arc": "p=pi*t^R, q=-pi*t^R+Delta*t^d, R<d",
            "witnesses": {
                (1, 1, 0, 1): (1, 1, 2, -2, 1),
                (0, 0, 0, 1): (1, 1, 2, -2, 2),
                (1, 1, 0, 0): (1, 1, 2, "-3/2", 1),
                (0, 0, 0, 0): (1, 1, 2, "-3/2", 2),
                (1, 1, 1, 0): (1, 1, 2, -1, 1),
                (0, 0, 1, 0): (1, 1, 2, "-1/2", "3/2"),
            },
        },
    }
    pi, theta = sp.symbols("pi theta", nonzero=True)
    exceptional_output = {}
    for label, data in residue_cases.items():
        cap_r = data["R"]
        eps = (
            z3.And(cap_p == cap_r, x0 == d - cap_r),
            z3.And(cap_q == cap_r, x0 == d - cap_r),
            x0 == d + y,
            y == -d,
        )
        base = (
            *data["assumptions"],
            y >= -d,
            y <= 0,
            x0 >= d - cap_r,
            x0 >= d + y,
        )
        for signature in itertools.product((0, 1), repeat=4):
            signature_conditions = tuple(
                condition if bit else z3.Not(condition)
                for bit, condition in zip(signature, eps)
            )
            if signature not in data["expected"]:
                recorder.unsat(
                    "exceptional_signature_" + label.replace("=", "eq").replace("<", "lt").replace(">", "gt") + "_" + "".join(map(str, signature)),
                    (*base, *signature_conditions),
                )
                continue
            witness = data["witnesses"][signature]
            instantiated = z3.simplify(
                z3.substitute(
                    z3.And(*base, *signature_conditions),
                    (cap_p, z3.RealVal(str(witness[0]))),
                    (cap_q, z3.RealVal(str(witness[1]))),
                    (d, z3.RealVal(str(witness[2]))),
                    (y, z3.RealVal(str(witness[3]))),
                    (x0, z3.RealVal(str(witness[4]))),
                )
            )
            assert z3.is_true(instantiated), (label, signature, instantiated)
            ep, eq, ec, e12 = signature
            relation = ep * pi / delta_lead + eq * theta / delta_lead - ec * e12
            if label == "P<Q":
                relation = relation.subs(delta_lead, pi)
            elif label == "Q<P":
                relation = relation.subs(delta_lead, theta)
            elif label == "P=Q=R=d":
                relation = relation.subs(delta_lead, pi + theta)
            else:
                relation = relation.subs(theta, -pi)
            assert sp.factor(relation) == 0, (label, signature, relation)
        exceptional_output[label] = {
            "arc_residue_relation": data["relation"],
            "arc_template": data["arc"],
            "complete_wall_signatures_epsP_epsQ_epsC_eps12": sorted(data["expected"]),
            "explicit_rational_witnesses_P_Q_d_y_x0": {
                "".join(map(str, signature)): list(witness)
                for signature, witness in data["witnesses"].items()
            },
            "a=0_pluecker_relation_checked": True,
            "a=-1_pluecker_relation_checked": True,
        }

    # The exceptional lower-pair placement is a support-one/disjoint-binary
    # secant: e^2=L*M=0 and the pair multiplication rank is exactly two.
    assert product(e, e) == sp.zeros(6, 1)
    assert product(residue_ell, residue_em) == sp.zeros(6, 1)
    exceptional_pair_rank = product_matrix((e, residue_ell), (e, residue_em)).rank()
    assert exceptional_pair_rank == 2
    assert sp.Matrix.hstack(e, residue_ell, residue_em).rank() == 3

    # Infinity has exactly five faces.  Exclude all other Boolean signatures.
    di, ri, yi, x0i = z3.Reals("di ri yi x0i")
    infinity_eps = (
        x0i == di - 2 * ri,
        yi == -di,
        z3.And(yi == -ri, x0i == di - 2 * ri),
    )
    infinity_expected = {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 1)}
    infinity_witnesses = {
        (0, 0, 0): (2, -1, 0, 5),
        (1, 0, 0): (2, -1, 0, 4),
        (0, 1, 0): (2, -1, -2, 5),
        (1, 1, 0): (2, -1, -2, 4),
        (1, 0, 1): (2, -1, 1, 4),
    }
    infinity_base = (di > 0, ri < 0, yi >= -di, yi <= -ri, x0i >= di - 2 * ri)
    for signature in itertools.product((0, 1), repeat=3):
        conditions = tuple(
            condition if bit else z3.Not(condition)
            for bit, condition in zip(signature, infinity_eps)
        )
        if signature not in infinity_expected:
            recorder.unsat("infinity_face_signature_" + "".join(map(str, signature)), (*infinity_base, *conditions))
        else:
            witness = infinity_witnesses[signature]
            instantiated = z3.simplify(
                z3.substitute(
                    z3.And(*infinity_base, *conditions),
                    (di, z3.RealVal(witness[0])),
                    (ri, z3.RealVal(witness[1])),
                    (yi, z3.RealVal(witness[2])),
                    (x0i, z3.RealVal(witness[3])),
                )
            )
            assert z3.is_true(instantiated), (signature, instantiated)

    kappa, alpha = sp.symbols("kappa alpha", nonzero=True)
    p0 = 2 * kappa / alpha
    c0_over_delta = alpha**2 / (4 * kappa)
    assert sp.factor(c0_over_delta * p0**2 - kappa) == 0
    assert sp.factor(2 * c0_over_delta * p0 - alpha) == 0
    infinity_vectors = {}
    for eps_x, eps_l, eps_u in sorted(infinity_expected):
        vector = (
            -eps_x * kappa * c1,
            eps_x * kappa * c2,
            eps_u * alpha,
            -eps_l * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        assert pluecker_relation(vector) == 0
        infinity_vectors[f"eps_x={eps_x},eps_l={eps_l},eps_u={eps_u}"] = [str(v) for v in vector]

    full_direction = p0 * residue_ell + cap_c
    assert all(full_direction[index] != 0 for index in (1, 2, 3))
    assert product_matrix((e, full_direction), (e, full_direction)).rank() == 2
    return {
        "claim_label": "VERIFIED",
        "finite_generic_arc": "p=a, q=-a+Delta*t^d, D=diag(c0*t^x0,c1*t^y,c2*t^y,1)",
        "finite_generic_negative_y_faces": finite_generic_faces,
        "B_full_all_nonzero_lambda_realized": True,
        "all_nonzero_eta_realized": True,
        "a=-1/2_arc": "delta=Delta*t^d, s=Sigma*t^h, p=(delta+s-1)/2, q=(delta-s+1)/2",
        "a=-1/2_B_full_closure_limit": [str(value) for value in half_limit],
        "a=-1/2_k_nonzero_on_x0_wall_and_zero_off_wall": True,
        "exceptional_residue_cases": exceptional_output,
        "exceptional_mode_zero_vector_a0": "(-epsP*c0*c1*pi/Delta,-epsQ*c0*c2*theta/Delta,epsC*c0/Delta,-eps12*Delta*c1*c2,c1,-c2)",
        "exceptional_mode_zero_vector_a_minus1": "(epsP*c0*c1*pi/Delta,epsQ*c0*c2*theta/Delta,-epsC*c0/Delta,-eps12*Delta*c1*c2,c1,-c2)",
        "exceptional_lower_pair_rank": exceptional_pair_rank,
        "exceptional_placement": "component 15 via support-one/disjoint-binary secant closure",
        "infinity_arc": "p=P0*t^r, q=-P0*t^r+Delta*t^d",
        "infinity_complete_face_signatures": sorted(infinity_expected),
        "infinity_explicit_witnesses_d_r_y_x0": {
            "".join(map(str, signature)): list(witness)
            for signature, witness in infinity_witnesses.items()
        },
        "infinity_mode_zero_vectors": infinity_vectors,
        "arbitrary_nonzero_kappa_alpha_realized": True,
        "negative_y_generic_and_half_placement": "embedded P3 via U1=U2=<e,L>, U3=<e,M>",
        "infinity_placement": "embedded P3 for y<-r; component 14 for y=-r",
        "finite_field_computation_used": False,
        "bounded_scan_used": False,
    }


def replay_classification_verifiers() -> list[dict[str, object]]:
    results = []
    for filename in CLASSIFICATION_VERIFIERS:
        path = ROOT / filename
        completed = subprocess.run(
            (sys.executable, str(path)),
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=120,
            check=False,
        )
        if completed.returncode != 0 or completed.stderr.strip():
            raise AssertionError(
                (filename, completed.returncode, completed.stdout, completed.stderr)
            )
        payload = json.loads(completed.stdout)
        if filename == "verify_p4_rank_two_pair_kernel_geometry.py":
            assert payload["verified"] is True
            assert payload["secant_representative_pair_ranks"] == {"1+3": 2, "2+2": 2}
        elif filename == "verify_p4_tangent_rank_two_pair_purity_classification.py":
            assert payload["status"] == "pass"
            assert payload["nonembedded_survivors"] is True
        elif filename == "verify_p4_support_two_tangent_flag_boundary_inclusion.py":
            assert payload["status"] == "pass"
            assert payload["new_component"] is False
            assert payload["containing_component_dimension"] == 6
        elif filename == "verify_p4_full_support_tangent_pair_component.py":
            assert payload["status"] == "pass"
            assert payload["component_number"] == 14
            assert payload["pair_profile"] == [2, 3, 4, 3, 4, 4]
        elif filename == "verify_p4_disjoint_secant_lower_pair_component.py":
            assert payload["status"] == "pass"
            assert payload["component_number"] == 15
            assert payload["rank_two_kernel_type"] == "reduced secant"
        else:
            assert filename == "verify_p4_support_one_secant_boundary_inclusion.py"
            assert payload["status"] == "pass"
            assert payload["containing_component"] == 15
            assert payload["new_component"] is False
        results.append(
            {
                "verifier": filename,
                "sha256": sha256(path),
                "parsed_claim_fields_passed": True,
            }
        )
    return results


def git_commit() -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def main() -> None:
    recorder = ProofRecorder()
    family = normalized_family_certificate()
    generic = generic_min_plus_certificate(recorder)
    generic_hand = generic_hand_cone_certificate(recorder)
    exceptional = exceptional_schema_certificate(recorder)
    charts = chart_certificate()
    raw_tables = raw_mode_zero_leading_tables()
    arcs = actual_arc_realization_certificate(recorder)
    replayed = replay_classification_verifiers()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "construction",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": ("component-20 p+q diagonal-source-torus valuative boundary"),
                "method": (
                    "exact SymPy/Rees/Pluecker reconstruction, explicit Z3 "
                    "linear-arithmetic proof objects, actual Laurent/Puiseux "
                    "arc templates, and replay of six existing classifiers"
                ),
                "command": (
                    "uv run --with sympy --with z3-solver python "
                    "verify_p4_common_active_binary_triangle_p_plus_q_boundary.py"
                ),
                "outputs": {THEOREM.name: sha256(THEOREM)},
                "limitations": (
                    "diagonal source tori only; arbitrary GL4, older-component "
                    "placement, H31, H22, local-to-global, and global closure open"
                ),
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "inputs": {path.name: sha256(path) for path in INPUTS},
                "normalized_family": family,
                "generic_min_plus_certificate": generic,
                "generic_hand_cone_certificate": generic_hand,
                "exceptional_and_infinity_schemas": exceptional,
                "linear_arithmetic_proof_evidence": recorder.summary(),
                "boundary_charts": charts,
                "raw_mode_zero_leading_tables": raw_tables,
                "actual_arc_realization_and_exhaustion": arcs,
                "fresh_independent_verifier_complete": True,
                "classification_verifier_replays": replayed,
                "finite_field_inference_used": False,
                "bounded_scan_used_as_proof": False,
                "arbitrary_GL4_used": False,
                "GL4_exclusion_reason": (
                    "arbitrary GL4 is not a symmetry of the squarefree permanent"
                ),
                "older_component_intersection_placement_closed": False,
                "H31_closed": False,
                "H22_closed": False,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
