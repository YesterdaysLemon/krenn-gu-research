#!/usr/bin/env python3
"""Exact diagonal-DVR atlas candidate over component-20 zero restrictions."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp
import z3

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_CANDIDATE.md"
CERTIFICATE = ROOT / "component20_intrinsic_zero_diagonal_dvr_atlas_certificate.json"
INPUTS = tuple(ROOT / name for name in (
    "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md",
    "COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md",
    "P4_COMMON_SINGLETON_COMPONENT.md",
    "claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md",
    "P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md",
    "claims/p4/boundaries/pair-geometry/support-one-secant/P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md",
    "P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md",
    "P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md",
))

PAIRS = tuple(itertools.combinations(range(4), 2))
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True,
    ).stdout.strip()


def zmin(*entries):
    result = entries[-1]
    for entry in reversed(entries[:-1]):
        result = z3.If(entry <= result, entry, result)
    return result


class ProofRecorder:
    def __init__(self):
        z3.set_option(proof=True)
        self.digest = hashlib.sha256()
        self.queries = []

    def unsat(self, label, assumptions):
        solver = z3.Solver()
        solver.add(*assumptions)
        result = solver.check()
        assert result == z3.unsat, (label, result, solver.model() if result == z3.sat else "")
        proof = solver.proof().sexpr().encode("utf-8")
        self.digest.update(label.encode("utf-8") + b"\0" + proof + b"\0")
        self.queries.append(label)


def regular_expression(center="p0"):
    r, s, w, x0, x1, x2 = z3.Reals("r s w x0 x1 x2")
    m0 = zmin(
        r + x0 + x1, s + x0 + x2, w + x0,
        x1 + x2, x1, x2,
    )
    if center == "p0":
        m1 = zmin(x0 + x1, s + x0 + x2, x0)
        m2 = zmin(r + x0 + x1, x0 + x2, x0)
    else:
        m1 = zmin(r + x0 + x1, x0 + x2, x0)
        m2 = zmin(x0 + x1, s + x0 + x2, x0)
    m3 = zmin(x0 + x1, x0 + x2)
    a0 = zmin(r + x1, s + x2, w)
    z = zmin(x0, x1, x2)
    expression = 3 * x0 + x1 + x2 + z + a0 - m0 - m1 - m2 - m3
    return (r, s, w, x0, x1, x2), expression, (m0, m1, m2, m3, a0, z)


def axis_expression(axis):
    h, x0, x1, x2 = z3.Reals(f"h_{axis} x0_{axis} x1_{axis} x2_{axis}")
    if axis == "v_zero":
        m0 = zmin(h + x0 + x1, h + x0, x1 + x2, x1, x2)
        m1 = zmin(x0 + x1, x0)
        m2 = zmin(h + x0 + x1, x0 + x2, x0)
        a0 = zmin(h + x1, h)
    elif axis == "u_zero":
        m0 = zmin(h + x0 + x2, h + x0, x1 + x2, x1, x2)
        m1 = zmin(x0 + x1, h + x0 + x2, x0)
        m2 = zmin(x0 + x2, x0)
        a0 = zmin(h + x2, h)
    elif axis == "u_equals_v":
        m0 = zmin(h + x0 + x1, h + x0 + x2, x1 + x2, x1, x2)
        m1 = zmin(x0 + x1, h + x0 + x2, x0)
        m2 = zmin(h + x0 + x1, x0 + x2, x0)
        a0 = zmin(h + x1, h + x2)
    else:
        raise ValueError(axis)
    m3 = zmin(x0 + x1, x0 + x2)
    z = zmin(x0, x1, x2)
    expression = 3 * x0 + x1 + x2 + z + a0 - m0 - m1 - m2 - m3
    return (h, x0, x1, x2), expression


def min_plus_certificate():
    recorder = ProofRecorder()
    variables0, expression0, minima0 = regular_expression("p0")
    variables1, expression1, _ = regular_expression("pm1")
    r, s, w, x0, x1, x2 = variables0
    substitutions = tuple(zip(variables1, variables0))
    expression1_same_symbols = z3.simplify(z3.substitute(expression1, *substitutions))
    assert z3.is_true(z3.simplify(expression0 == expression1_same_symbols))
    h = zmin(r, s)
    target = z3.And(x1 == 0, x2 == 0, x0 <= -h)
    branches = {
        "r_lt_s": (r > 0, s > 0, r < s, w == r),
        "s_lt_r": (r > 0, s > 0, s < r, w == s),
        "equal_no_cancellation": (r > 0, s > 0, r == s, w == r),
        "equal_higher_cancellation": (r > 0, s > 0, r == s, w > r),
    }
    for name, assumptions in branches.items():
        recorder.unsat(name + "_nonnegative", (*assumptions, expression0 < 0))
        recorder.unsat(
            name + "_zero_necessity",
            (*assumptions, expression0 == 0, z3.Not(target)),
        )
        recorder.unsat(
            name + "_zero_sufficiency",
            (*assumptions, target, expression0 != 0),
        )

    for axis in ("v_zero", "u_zero", "u_equals_v"):
        axis_variables, axis_value = axis_expression(axis)
        axis_h, axis_x0, axis_x1, axis_x2 = axis_variables
        axis_target = z3.And(
            axis_x1 == 0, axis_x2 == 0, axis_x0 <= -axis_h
        )
        assumptions = (axis_h > 0,)
        recorder.unsat(axis + "_nonnegative", (*assumptions, axis_value < 0))
        recorder.unsat(
            axis + "_zero_necessity",
            (*assumptions, axis_value == 0, z3.Not(axis_target)),
        )
        recorder.unsat(
            axis + "_zero_sufficiency",
            (*assumptions, axis_target, axis_value != 0),
        )

    bad_shortcut = x0 + x1 + x2 + h - sum(minima0[:4])
    counterexample = tuple(
        (variable, z3.RealVal(value)) for variable, value in
        ((r, 1), (s, 1), (w, 1), (x0, 1), (x1, 0), (x2, 0))
    )
    assert z3.simplify(z3.substitute(bad_shortcut, *counterexample)) == -1
    assert z3.simplify(z3.substitute(expression0, *counterexample)) == 1
    return {
        "p0_formula": (
            "E=3*x0+x1+x2+z+a0-m0-m1-m2-m3; "
            "z=min(x0,x1,x2); a0=min(r+x1,s+x2,w); "
            "m0=min(r+x0+x1,s+x0+x2,w+x0,x1+x2,x1,x2); "
            "m1=min(x0+x1,s+x0+x2,x0); "
            "m2=min(r+x0+x1,x0+x2,x0); "
            "m3=min(x0+x1,x0+x2)"
        ),
        "pm1_formula": "the same expression, with m1 and m2 exchanged",
        "ultrametric_branches": list(branches),
        "exact_axes": ["v=0", "u=0", "u=v"],
        "constant_arc_u_equals_v_equals_zero": "identically zero restriction",
        "nonnegative": True,
        "zero_locus": "x1=x2=0 and x0<=-h, h=min(r,s)",
        "strata": ["interior x0<-h", "wall x0=-h"],
        "unsat_query_count": len(recorder.queries),
        "proof_digest_sha256": recorder.digest.hexdigest(),
        "failed_shortcut_counterexample": {
            "values": "r=s=w=x0=1, x1=x2=0",
            "shortcut_value": -1,
            "correct_value": 1,
        },
    }


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def permanent4(rows):
    return sp.factor(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def squarefree_product(left, right):
    return sp.Matrix(tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
    ))


def pair_matrix(left_plane, right_plane):
    return sp.Matrix.hstack(*(
        squarefree_product(left_plane[i], right_plane[j])
        for i in range(2) for j in range(2)
    ))


def plucker(plane):
    left, right = plane
    return tuple(
        sp.factor(left[i] * right[j] - left[j] * right[i]) for i, j in PAIRS
    )


def plane_from_plucker(values):
    _p01, p02, p03, p12, p13, p23 = values
    assert p23 != 0
    plane = (
        (sp.factor(p03 / p23), sp.factor(p13 / p23), 1, 0),
        (sp.factor(-p02 / p23), sp.factor(-p12 / p23), 0, 1),
    )
    check = plucker(plane)
    assert all(sp.factor(check[i] - values[i] / p23) == 0 for i in range(6))
    return plane


def rank_witness(matrix, rank, rows, columns):
    determinant = sp.factor(matrix.extract(rows, columns).det())
    assert determinant != 0
    higher_size = rank + 1
    zero_higher = 0
    if higher_size <= min(matrix.rows, matrix.cols):
        for row_set in itertools.combinations(range(matrix.rows), higher_size):
            for column_set in itertools.combinations(range(matrix.cols), higher_size):
                assert sp.factor(matrix.extract(row_set, column_set).det()) == 0
                zero_higher += 1
    return {
        "rank": rank,
        "nonzero_minor": {
            "rows": list(rows),
            "columns": list(columns),
            "determinant": str(determinant),
        },
        "higher_minors_checked_zero": zero_higher,
    }


def expected_profile(branch, stratum):
    if stratum == "interior":
        return {
            "r_lt_s": [2, 3, 3, 3, 3, 3],
            "s_lt_r": [3, 2, 3, 3, 3, 3],
            "equal_no_cancellation": [3, 3, 3, 3, 3, 3],
            "equal_higher_cancellation": [3, 3, 2, 3, 3, 3],
        }[branch]
    return {
        "r_lt_s": [3, 4, 4, 3, 3, 3],
        "s_lt_r": [4, 3, 4, 3, 3, 3],
        "equal_no_cancellation": [4, 4, 4, 3, 3, 3],
        "equal_higher_cancellation": [4, 4, 3, 3, 3, 3],
    }[branch]


def witness_selection(branch, stratum, edge, rank):
    common = ((0, 1, 3), (1, 2, 3))
    if edge in ((1, 2), (1, 3), (2, 3)):
        return common
    if stratum == "interior":
        table = {
            ("r_lt_s", (0, 1)): ((0, 2), (1, 2)),
            ("r_lt_s", (0, 2)): common,
            ("r_lt_s", (0, 3)): common,
            ("s_lt_r", (0, 1)): common,
            ("s_lt_r", (0, 2)): ((1, 2), (1, 2)),
            ("s_lt_r", (0, 3)): common,
            ("equal_no_cancellation", (0, 1)): common,
            ("equal_no_cancellation", (0, 2)): common,
            ("equal_no_cancellation", (0, 3)): ((0, 2, 3), (1, 2, 3)),
            ("equal_higher_cancellation", (0, 1)): common,
            ("equal_higher_cancellation", (0, 2)): common,
            ("equal_higher_cancellation", (0, 3)): ((0, 1), (1, 2)),
        }
        return table[(branch, edge)]
    table = {
        ("r_lt_s", (0, 1)): ((0, 1, 2), (0, 1, 2)),
        ("r_lt_s", (0, 2)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("r_lt_s", (0, 3)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("s_lt_r", (0, 1)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("s_lt_r", (0, 2)): ((0, 1, 2), (0, 1, 2)),
        ("s_lt_r", (0, 3)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("equal_no_cancellation", (0, 1)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("equal_no_cancellation", (0, 2)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("equal_no_cancellation", (0, 3)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("equal_higher_cancellation", (0, 1)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("equal_higher_cancellation", (0, 2)): ((0, 1, 2, 3), (0, 1, 2, 3)),
        ("equal_higher_cancellation", (0, 3)): ((0, 1, 2), (0, 2, 3)),
    }
    return table[(branch, edge)]


def transform_source(row):
    return (row[0], -row[1], -row[2], row[3])


def chart_data(branch, stratum, center, symbols):
    pi, theta, c0, c1, c2 = symbols
    e = (1, 0, 0, 0)
    cases = {
        "r_lt_s": (-pi * c1, 0, pi),
        "s_lt_r": (0, theta * c2, -theta),
        "equal_no_cancellation": (-pi * c1, theta * c2, pi - theta),
        "equal_higher_cancellation": (-pi * c1, pi * c2, 0),
    }
    a, b, c = cases[branch]
    raw_u0 = (
        c0 * a, c0 * b, c0 * c, -c1 * c2, c1, -c2
    ) if stratum == "wall" else (c0 * a, c0 * b, c0 * c, 0, 0, 0)
    if stratum == "interior":
        u0 = (e, (0, a, b, c))
        alpha0, beta0 = u0[1], e
    else:
        # Keep c0: it cannot be removed without also changing the last three
        # Plucker coordinates.  The distinguished kernel K0 is nevertheless
        # independent of c0 and lies in this exact plane.
        u0 = plane_from_plucker(raw_u0)
        alpha0 = (0, a, b, c)
        beta0 = u0[1] if branch == "equal_higher_cancellation" else u0[0]
    u1 = (e, (0, c1, 0, 1))
    u2 = (e, (0, 0, c2, 1))
    u3 = (e, (0, c1, c2, 0))
    planes = [u0, u1, u2, u3]
    alpha = [alpha0, e, e, e]
    beta = [beta0, u1[1], u2[1], u3[1]]
    if center == "pm1":
        planes = [[transform_source(row) for row in plane] for plane in planes]
        alpha = [transform_source(row) for row in alpha]
        beta = [transform_source(row) for row in beta]
        planes[1], planes[2] = planes[2], planes[1]
        alpha[1], alpha[2] = alpha[2], alpha[1]
        beta[1], beta[2] = beta[2], beta[1]
        raw_u0 = (
            -raw_u0[0], -raw_u0[1], raw_u0[2],
            raw_u0[3], -raw_u0[4], -raw_u0[5],
        )

    support = {}
    for word in WORDS:
        value = permanent4(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        if value != 0:
            support["".join(map(str, word))] = str(value)
    assert list(support) == ["1111"]
    profile0 = expected_profile(branch, stratum)
    profile = profile0 if center == "p0" else [
        profile0[1], profile0[0], profile0[2], profile0[3], profile0[5], profile0[4]
    ]
    pair_certificates = {}
    for position, (i, j) in enumerate(PAIRS):
        matrix = pair_matrix(planes[i], planes[j])
        rank = profile[position]
        if center == "p0":
            rows, columns = witness_selection(branch, stratum, (i, j), rank)
            pair_certificates[f"{i}{j}"] = rank_witness(
                matrix, rank, rows, columns
            )
        else:
            assert matrix.rank() == rank
            pair_certificates[f"{i}{j}"] = {"rank": rank, "via_exact_symmetry": True}

    u0_contains_e = stratum == "interior"
    placement = ["component 20 closure"]
    if u0_contains_e:
        placement.append("component 18 common-singleton closure")
        if 2 in profile:
            placement.append("component 15 support-one secant closure")
    else:
        placement.append("component 16 directed-triangle closure")
    return {
        "id": f"{center}_{branch}_{stratum}",
        "center": "(p,q)=(0,1)" if center == "p0" else "(p,q)=(-1,0)",
        "valuation_branch": branch,
        "torus_stratum": "x0<-h" if stratum == "interior" else "x0=-h",
        "raw_U0_plucker_01_02_03_12_13_23": [str(value) for value in raw_u0],
        "leading_planes": [
            [[str(sp.factor(value)) for value in row] for row in plane]
            for plane in planes
        ],
        "pure_kernel_rows": [
            [str(sp.factor(value)) for value in row] for row in alpha
        ],
        "pure_tensor_support": support,
        "pair_profile": profile,
        "pair_certificates": pair_certificates,
        "U0_contains_e": u0_contains_e,
        "placement": placement,
    }


def atlas_certificate():
    symbols = sp.symbols("pi theta c0 c1 c2", nonzero=True)
    charts = []
    for center in ("p0", "pm1"):
        for branch in (
            "r_lt_s", "s_lt_r", "equal_no_cancellation",
            "equal_higher_cancellation",
        ):
            for stratum in ("interior", "wall"):
                charts.append(chart_data(branch, stratum, center, symbols))
    assert len(charts) == 16
    return {
        "local_parameters": {
            "p0": "u=p, v=q-1",
            "pm1": "u=p+1, v=q",
            "valuations": "r=v(u)>0, s=v(v)>0, w=v(u-v), h=min(r,s)",
        },
        "residue_branches": {
            "r_lt_s": "w=r, sigma=pi; includes v=0 as s=infinity",
            "s_lt_r": "w=s, sigma=-theta; includes u=0 as r=infinity",
            "equal_no_cancellation": "r=s=w=h, pi,theta,pi-theta all nonzero",
            "equal_higher_cancellation": (
                "r=s=h, pi=theta nonzero, w>h with arbitrary nonzero sigma; "
                "includes exact u=v as w=infinity"
            ),
            "u=v=0": "constant zero-restriction arc; never a nonzero P4 limit",
        },
        "torus": "diag(c0*t^x0,c1*t^x1,c2*t^x2,1), c0*c1*c2!=0",
        "chart_count": len(charts),
        "charts": charts,
        "centre_isomorphism": {
            "source": "diag(1,-1,-1,1)",
            "modes": "swap modes 1 and 2",
            "effect": "p0 atlas maps exactly to pm1 atlas",
        },
    }


def hall_certificate():
    lam, mu = sp.symbols("lambda mu")
    source = sp.symbols("s0:4", nonzero=True)
    extension = sp.symbols("z0:4")
    ell = sp.symbols("L0:4")
    e = (1, 0, 0, 0)
    alpha = (ell, e, e, e)
    h31 = []
    for deleted in range(4):
        kept = tuple(index for index in range(4) if index != deleted)
        rows = tuple(
            tuple(source[index] * alpha[mode][index] for index in kept)
            + (extension[mode],)
            for mode in range(4)
        )
        value = permanent4(rows)
        assert value == 0
        h31.append({
            "deleted_coordinate": deleted,
            "three_common_kernel_support_size": 1 if deleted == 0 else 2,
            "all_alpha_diagonal": "0",
        })

    def d01(row, ext):
        return (
            lam * source[0] * row[0] + mu * source[1] * row[1],
            source[2] * row[2], source[3] * row[3], ext,
        )

    def d23(row, ext):
        return (
            source[0] * row[0], source[1] * row[1],
            lam * source[2] * row[2] + mu * source[3] * row[3], ext,
        )

    weighted = {}
    for name, projection in (("D01", d01), ("D23", d23)):
        rows = tuple(projection(alpha[i], extension[i]) for i in range(4))
        assert permanent4(rows) == 0
        supports = [
            [index for index, value in enumerate(row) if value != 0]
            for row in rows[1:]
        ]
        assert all(len(support) <= 2 for support in supports)
        weighted[name] = {
            "common_kernel_row_supports": supports,
            "all_alpha_diagonal": "0",
            "all_homogeneous_weights_and_endpoints": True,
        }
    return {
        "pointwise_scope": "every chart, residue, marking, and extension",
        "H31": h31,
        "weighted_H22": weighted,
        "conclusion": (
            "no H31 binary neighbour; neither H22 direction can be binary, "
            "independently of component-placement labels"
        ),
    }


def main():
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert stored["claim_label"] == "VERIFIED"
    assert stored["discovery_claim_label"] == "CANDIDATE"
    assert stored["independent_verifier_complete"] is True
    min_plus = min_plus_certificate()
    atlas = atlas_certificate()
    hall = hall_certificate()
    expected_ids = stored["expected_chart_ids"]
    assert [chart["id"] for chart in atlas["charts"]] == expected_ids
    expected_profiles = stored["expected_pair_profiles"]
    assert {
        chart["id"]: chart["pair_profile"] for chart in atlas["charts"]
    } == expected_profiles
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "CANDIDATE",
        "scope": stored["scope"],
        "inputs": {path.name: sha256(path) for path in INPUTS},
        "method": stored["method"],
        "command": (
            "uv run --with sympy --with z3-solver python " + SCRIPT.name
        ),
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "min_plus_certificate": min_plus,
        "atlas": atlas,
        "pointwise_H31_H22": hall,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": stored["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
