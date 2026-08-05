#!/usr/bin/env python3
"""Exact candidate classification of component-20 intrinsic-wall exceptions."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md"
CERTIFICATE = ROOT / "component20_intrinsic_wall_exceptional_fibres_certificate.json"
INPUTS = tuple(ROOT / name for name in (
    "P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md",
    "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md",
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md",
    "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md",
    "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md",
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md",
    "P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md",
))

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in PERMUTATIONS3
    ))


def permanent4(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def tensor(planes):
    return {
        word: sp.factor(permanent4(tuple(planes[i][word[i]] for i in range(4))))
        for word in WORDS
    }


def squarefree_product(left, right):
    return sp.Matrix(tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS
    ))


def pair_matrix(left_plane, right_plane):
    return sp.Matrix.hstack(*(
        squarefree_product(left_plane[i], right_plane[j])
        for i in range(2) for j in range(2)
    ))


def rank_certificate(matrix):
    rank = matrix.rank()
    columns = tuple(matrix.rref()[1])
    assert len(columns) == rank
    rows = tuple(matrix[:, columns].T.rref()[1])
    witness = sp.factor(matrix.extract(rows, columns).det())
    assert witness != 0
    kernel = tuple(matrix.nullspace())
    assert len(kernel) == matrix.cols - rank
    if kernel:
        frame = sp.Matrix.hstack(*kernel)
        assert frame.rank() == len(kernel)
        assert matrix * frame == sp.zeros(matrix.rows, len(kernel))
    return {
        "rank": rank,
        "nonzero_minor": {
            "rows": list(rows),
            "columns": list(columns),
            "determinant": str(witness),
        },
        "kernel_basis": [[str(sp.factor(value)) for value in vector] for vector in kernel],
    }


def plucker(plane):
    left, right = plane
    return tuple(
        sp.expand(left[i] * right[j] - left[j] * right[i]) for i, j in PAIRS
    )


def base_planes(base):
    e = (1, 0, 0, 0)
    r0 = (0, -1, 1, 0)
    if base == "p0":
        r1 = (0, -1, 0, 1)
        beta1, beta2 = (0, 1, 0, 1), (0, 0, 1, 1)
    elif base == "pm1":
        r1 = (0, 1, 0, 1)
        beta1, beta2 = (0, 0, -1, 1), (0, -1, 0, 1)
    else:
        raise ValueError(base)
    return (
        (r0, r1),
        (e, beta1),
        (e, beta2),
        ((1, 1, 1, 0), e),
    )


def zero_base_certificate(base):
    planes = base_planes(base)
    restricted = tensor(planes)
    assert all(value == 0 for value in restricted.values())
    pairs = {}
    for i, j in PAIRS:
        pairs[f"{i}{j}"] = rank_certificate(pair_matrix(planes[i], planes[j]))
    profile = [pairs[f"{i}{j}"]["rank"] for i, j in PAIRS]
    assert profile == [3, 3, 3, 3, 3, 3]
    return {
        "planes": [[[str(value) for value in row] for row in plane] for plane in planes],
        "restricted_tensor_support": {},
        "pair_profile": profile,
        "pair_certificates": pairs,
        "regular_normalized_component20_chart": True,
        "nonzero_P4_fibre": False,
    }


def tangent_direction_certificate():
    p, q = sp.symbols("p q")
    coefficients = sp.Matrix((2 * (p - q + 1), -2 * q * (q - 1)))
    jacobian = coefficients.jacobian((p, q))
    out = {}
    for label, point, determinant, arc in (
        (
            "p0", {p: 0, q: 1}, -4,
            "p=(a-b)t/2, q=1-bt/2 realizes [T0111:T1111]=[a:b]",
        ),
        (
            "pm1", {p: -1, q: 0}, 4,
            "p=-1+(a+b)t/2, q=bt/2 realizes [T0111:T1111]=[a:b]",
        ),
    ):
        specialized = jacobian.subs(point)
        assert specialized.det() == determinant
        out[label] = {
            "coefficient_order": ["T0111", "T1111"],
            "jacobian": [[int(value) for value in row] for row in specialized.tolist()],
            "determinant": determinant,
            "realizing_first_order_arc": arc,
            "compactified_coefficient_direction_fibre": "P1",
        }
    return out


def compactified_bases(base, factor_chart, rho, shifts):
    planes = base_planes(base)
    r0, r1 = planes[0]
    if factor_chart == "finite_[1:rho]":
        alpha0, beta0 = add(scale(rho, r0), scale(-1, r1)), r0
    elif factor_chart == "infinity_[0:1]":
        alpha0, beta0 = r0, r1
    else:
        raise ValueError(factor_chart)
    alpha = (alpha0, planes[1][0], planes[2][0], planes[3][0])
    beta = (beta0, planes[1][1], planes[2][1], planes[3][1])
    assert all(sp.Matrix((alpha[i], beta[i])).rank() == 2 for i in range(4))
    marked = tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))
    return alpha, marked


def coefficient_model(alpha, beta, extensions, projection):
    alpha_rows = tuple(projection(alpha[i], extensions[i]) for i in range(4))
    beta_rows = tuple(projection(beta[i], extensions[4 + i]) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        coefficients[word] = sp.expand(sum(
            selected[i][3]
            * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
            for i in range(4)
        ))
    return {
        "coefficients": coefficients,
        "mixed": tuple(coefficients[word] for word in MIXED),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def h31_model(alpha, beta, extensions, deleted):
    kept = tuple(index for index in range(4) if index != deleted)
    return coefficient_model(
        alpha, beta, extensions,
        lambda row, extension: tuple(row[index] for index in kept) + (extension,),
    )


def weighted_model(alpha, beta, extensions, direction, chart, slope):
    def projection(row, extension):
        if direction == "D01":
            return (
                (row[0], row[2], row[3], extension)
                if chart == "infinity_[1:0]"
                else (slope * row[0] + row[1], row[2], row[3], extension)
            )
        return (
            (row[0], row[1], row[2], extension)
            if chart == "infinity_[1:0]"
            else (row[0], row[1], slope * row[2] + row[3], extension)
        )

    return coefficient_model(alpha, beta, extensions, projection)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.expand(expression)).replace("**", "^")


def projection_check(label, equations, eliminated, retained, expected):
    variables = tuple(eliminated) + tuple(retained)
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + ";",
        "E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        (
            '"CODEX_RESULT:"'
            '+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));'
        ),
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True, timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    markers = [
        line for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "projected_ideal": [str(sp.factor(value)) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def compactified_incidence_certificates():
    rho, slope = sp.symbols("rho lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse_0, inverse_1 = sp.symbols("u v")
    results = {}
    for base in ("p0", "pm1"):
        base_results = {"H31": [], "H22_individual": [], "H22_shared": []}
        for factor_chart in ("finite_[1:rho]", "infinity_[0:1]"):
            alpha, beta = compactified_bases(base, factor_chart, rho, shifts)
            factor_retained = (rho,) if factor_chart.startswith("finite") else ()
            for deleted in range(4):
                model = h31_model(alpha, beta, extensions, deleted)
                base_results["H31"].append(projection_check(
                    f"{base}_{factor_chart}_H31_d{deleted}",
                    (
                        *model["mixed"], model["A"] - 1,
                        inverse_0 * model["B"] - 1,
                    ),
                    extensions + (inverse_0,),
                    shifts + factor_retained,
                    (sp.Integer(1),),
                ))
            for weight_chart in ("finite_[lambda:1]", "infinity_[1:0]"):
                weight_retained = (slope,) if weight_chart.startswith("finite") else ()
                retained = shifts + factor_retained + weight_retained
                models = {
                    direction: weighted_model(
                        alpha, beta, extensions, direction, weight_chart, slope
                    )
                    for direction in ("D01", "D23")
                }
                for direction in ("D01", "D23"):
                    model = models[direction]
                    expected = (sp.Integer(1),)
                    if (
                        factor_chart.startswith("finite")
                        and weight_chart.startswith("finite")
                        and direction == "D01"
                    ):
                        if base == "p0":
                            survivor = sp.expand(
                                rho * shifts[1] * shifts[2] * slope
                                + (rho - 1) * shifts[1] * slope
                                + (rho - 1) * shifts[1]
                                + rho * shifts[2]
                            )
                        else:
                            survivor = sp.expand(
                                rho * shifts[1] * shifts[2] * slope
                                + (-rho - 1) * shifts[2] * slope
                                - rho * shifts[1]
                                + (-rho - 1) * shifts[2]
                            )
                        expected = (shifts[3], shifts[0], survivor)
                    base_results["H22_individual"].append(projection_check(
                        f"{base}_{factor_chart}_{weight_chart}_{direction}_binary",
                        (
                            *model["mixed"], model["A"] - 1,
                            inverse_0 * model["B"] - 1,
                        ),
                        extensions + (inverse_0,), retained, expected,
                    ))
                for direction, other_direction in (("D01", "D23"), ("D23", "D01")):
                    model, other = models[direction], models[other_direction]
                    base_results["H22_shared"].append(projection_check(
                        f"{base}_{factor_chart}_{weight_chart}_shared_{direction}_binary",
                        (
                            *model["mixed"], *other["mixed"],
                            model["A"] - 1,
                            inverse_0 * model["B"] - 1,
                            inverse_1 * other["B"] - 1,
                        ),
                        extensions + (inverse_0, inverse_1), retained,
                        (sp.Integer(1),),
                    ))
        results[base] = base_results
    return results


def half_point_certificate():
    e = (1, 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    c = (0, 0, 0, 1)
    half = sp.Rational(1, 2)
    planes = (
        (e, ell),
        (e, add(c, scale(half, ell))),
        (e, add(c, scale(-half, ell))),
        (e, em),
    )
    restricted = tensor(planes)
    assert all(value == 0 for value in restricted.values())
    pairs = {
        f"{i}{j}": rank_certificate(pair_matrix(planes[i], planes[j]))
        for i, j in PAIRS
    }
    profile = [pairs[f"{i}{j}"]["rank"] for i, j in PAIRS]
    assert profile == [3, 3, 2, 3, 3, 3]
    assert pairs["03"]["kernel_basis"] == [
        ["1", "0", "0", "0"], ["0", "0", "0", "1"]
    ]

    p = sp.Symbol("p")
    delta = 2 * p + 1
    scaled_plucker = (
        p * (p + 1), -p * (p + 1), 0, delta**2, -delta, delta
    )
    limit_plucker = tuple(
        sp.factor(sp.sympify(value).subs(p, -half)) for value in scaled_plucker
    )
    assert limit_plucker == (-half**2, half**2, 0, 0, 0, 0)
    assert plucker(planes[0]) == (1, -1, 0, 0, 0, 0)

    tau = sp.Symbol("tau", nonzero=True)
    component15_arc = (
        (e, ell),
        (e, add(scale(tau, em), c, scale(half, ell))),
        (add(e, scale(tau, ell)), add(scale(tau, em), scale(-1, c), scale(half, ell))),
        (e, em),
    )
    arc_tensor = tensor(component15_arc)
    assert {
        word: value for word, value in arc_tensor.items() if value != 0
    } == {(1, 1, 0, 0): -2 * tau}
    arc_profile = [
        pair_matrix(component15_arc[i], component15_arc[j]).rank()
        for i, j in PAIRS
    ]
    assert arc_profile == [3, 4, 2, 4, 3, 4]
    for index in range(4):
        limit = tuple(sp.factor(value.subs(tau, 0)) for value in plucker(component15_arc[index]))
        target = plucker(planes[index])
        nonzero_target = next(value for value in target if value != 0)
        nonzero_limit = next(value for value in limit if value != 0)
        ratio = sp.factor(nonzero_limit / nonzero_target)
        assert ratio != 0
        assert all(sp.factor(limit[i] - ratio * target[i]) == 0 for i in range(6))

    return {
        "normalized_U0_chart_at_p_plus_q_zero": "undefined",
        "scaled_mode0_plucker_before_limit": [str(value) for value in scaled_plucker],
        "scaled_mode0_plucker_limit": [str(value) for value in limit_plucker],
        "straight_intrinsic_fixed_source_planes": [
            [[str(value) for value in row] for row in plane] for plane in planes
        ],
        "restricted_tensor_support": {},
        "pair_profile": profile,
        "pair_certificates": pairs,
        "rank_two_pair_03_kernel": ["e tensor e", "(A-B) tensor (A+B)"],
        "nonzero_P4_fibre": False,
        "p_plus_q_atlas_placement": (
            "k=infinity zero-tensor edge of U0=<A-B,C-k*e>; distinct from the "
            "verified finite-k and k=0 nonzero-P4 half-centre charts"
        ),
        "component15_closure_arc": {
            "parameter": "tau",
            "pure_support": {"1100": "-2*tau"},
            "pair_profile_for_tau_nonzero": arc_profile,
            "limit_is_straight_intrinsic_point": True,
            "placement": "component fifteen closure by the support-one secant boundary theorem",
        },
        "new_H31_or_H22_analysis_performed": False,
    }


def main():
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert stored["claim_label"] == "VERIFIED"
    assert stored["discovery_claim_label"] == "CANDIDATE"
    bases = {
        "p=0,q=1": zero_base_certificate("p0"),
        "p=-1,q=0": zero_base_certificate("pm1"),
    }
    tangents = tangent_direction_certificate()
    incidence = compactified_incidence_certificates()
    half = half_point_certificate()
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
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "zero_tensor_base_points": bases,
        "compactified_tensor_direction_fibres": tangents,
        "compactified_P1_incidence": incidence,
        "p_minus_one_half": half,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": stored["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
