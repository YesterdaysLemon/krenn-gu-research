#!/usr/bin/env python3
"""Independent exact audit of the component-21 generic weighted-H22 candidate."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_"
    "OBSTRUCTION_VERIFICATION.md"
)
CANDIDATE_REPORT = ROOT / (
    "P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md"
)
CANDIDATE_SCRIPT = ROOT / (
    "derive_p5_h22_coincident_support_rank_one_star_component_generic_"
    "obstruction_candidate.py"
)
CANDIDATE_CERTIFICATE = ROOT / (
    "p5_h22_coincident_support_rank_one_star_component_generic_certificate.json"
)
P4_REPORT = ROOT / "claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md"
P4_SCRIPT = ROOT / "claims/p4/classifications/star/coincident-support-rank-one-star/verify_p4_coincident_support_rank_one_star_component.py"
H31_REPORT = ROOT / (
    "claims/p5/h31/coincident-support-rank-one-star/P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
H31_SCRIPT = ROOT / (
    "claims/p5/h31/coincident-support-rank-one-star/verify_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py"
)
H22_DEFINITION = ROOT / "claims/p5/h22/common-singleton/P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
ALPHA_WORD = WORDS[0]
BETA_WORD = WORDS[-1]


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


def run_json(command: tuple[str, ...], timeout: int) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    require(
        completed.returncode == 0,
        f"replay failed ({' '.join(command)}): {completed.stderr[-2000:]}",
    )
    try:
        output = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"non-JSON replay ({' '.join(command)}): {completed.stdout[-2000:]}"
        ) from exc
    require(isinstance(output, dict), f"non-object replay: {' '.join(command)}")
    return output


def vector_sum(*vectors: tuple[Any, ...]) -> tuple[Any, ...]:
    return tuple(
        sp.expand(sum(vector[index] for vector in vectors)) for index in range(4)
    )


def vector_scale(scalar: Any, vector: tuple[Any, ...]) -> tuple[Any, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def permanent_by_subsets(rows: tuple[tuple[Any, ...], ...]) -> sp.Expr:
    """Compute a permanent with subset DP rather than permutation enumeration."""

    width = len(rows)
    require(all(len(row) == width for row in rows), "permanent matrix is not square")
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
    return sp.expand(states[(1 << width) - 1])


def component_bases(
    p: sp.Symbol, q: sp.Symbol, kappa: sp.Symbol, ell: sp.Symbol
) -> tuple[tuple[tuple[Any, ...], ...], tuple[tuple[Any, ...], ...]]:
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    free_first = vector_sum(cap_a, vector_scale(p, cap_b))
    free_second = vector_sum(cap_c, vector_scale(q, cap_b))
    alpha_zero = vector_sum(vector_scale(q, free_first), vector_scale(-p, free_second))
    alpha = (
        alpha_zero,
        vector_sum(vector_scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    beta = (
        free_first,
        cap_a,
        vector_sum(cap_b, vector_scale(kappa, cap_a)),
        vector_sum(cap_a, vector_scale(ell, cap_c)),
    )
    # The mode-zero change from the component's two displayed free-plane rows
    # to (alpha0,beta0) has determinant p in the generic function field.
    require(
        sp.factor(sp.Matrix(((q, -p), (1, 0))).det() - p) == 0,
        "mode-zero basis change",
    )
    return alpha, beta


def mark_beta(
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
    markings: tuple[Any, ...],
) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        vector_sum(beta[index], vector_scale(markings[index], alpha[index]))
        for index in range(4)
    )


def four_source_coefficients(
    alpha: tuple[tuple[Any, ...], ...], beta: tuple[tuple[Any, ...], ...]
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent_by_subsets(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }


def project_row(
    row: tuple[Any, ...], extension: Any, chart: str, slope: Any | None
) -> tuple[Any, ...]:
    if chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((chart, slope))


def d23_model(
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
    extensions: tuple[Any, ...],
    chart: str,
    slope: Any | None = None,
) -> dict[str, Any]:
    alpha_rows = tuple(
        project_row(alpha[index], extensions[index], chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project_row(beta[index], extensions[4 + index], chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = sp.factor(permanent_by_subsets(selected))
    mixed_matrix = sp.Matrix(
        [
            [sp.diff(coefficients[word], variable) for variable in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed_matrix": mixed_matrix,
        "A": coefficients[ALPHA_WORD],
        "B": coefficients[BETA_WORD],
    }


def d01_hall_certificate(alpha: tuple[tuple[Any, ...], ...]) -> dict[str, Any]:
    rho, sigma = sp.symbols("rho sigma")
    extensions = sp.symbols("u0:4")
    rows = tuple(
        (
            rho * alpha[index][0] + sigma * alpha[index][1],
            alpha[index][2],
            alpha[index][3],
            extensions[index],
        )
        for index in range(4)
    )
    supports = tuple(
        tuple(column for column, entry in enumerate(row) if entry != 0)
        for row in rows[:3]
    )
    require(supports == ((0, 3), (0, 3), (0, 3)), "D01 Hall supports")
    summands = tuple(
        sp.expand(sp.prod(rows[index][permutation[index]] for index in range(4)))
        for permutation in itertools.permutations(range(4))
    )
    require(
        len(summands) == 24 and all(value == 0 for value in summands),
        "D01 Hall summands",
    )
    require(permanent_by_subsets(rows) == 0, "D01 all-alpha diagonal")
    return {
        "homogeneous_weight": "[rho:sigma]",
        "first_three_alpha_supports": [list(support) for support in supports],
        "hall_row_count": 3,
        "hall_neighborhood_size": 2,
        "all_24_permanent_summands_zero": True,
        "all_alpha_diagonal": "0",
        "projective_endpoints_included": ["[0:1]", "[1:0]"],
        "marking_independent": True,
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact elimination audit")


def singular_expression(expression: Any) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def finite_d23_certificate(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    ell: sp.Symbol,
) -> tuple[dict[str, Any], tuple[sp.Expr, sp.Expr, sp.Expr]]:
    lam = sp.Symbol("lam")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    beta = mark_beta(alpha, unmarked_beta, h)
    model = d23_model(alpha, beta, x, "finite", lam)
    equations = (
        *(model["coefficients"][word] for word in MIXED_WORDS),
        model["A"] - 1,
    )

    delta = p**2 - q**2
    epsilon = ell**2 - 1
    f1 = sp.expand(
        kappa * delta * epsilon * h[0] * h[1]
        - delta * h[0] * h[2]
        - p * epsilon * h[1] * h[2]
        + kappa * ell * delta * h[0]
        - q * kappa * epsilon * h[1]
        + (q - p * ell) * h[2]
        + kappa * (p - q * ell)
    )
    f2 = sp.expand(
        (h[2] - kappa)
        * (h[2] + kappa)
        * (p * epsilon * h[1] + p * ell + delta * h[0] - q)
    )
    f3 = sp.expand(
        (h[2] - kappa)
        * (h[2] + kappa)
        * ((ell - 1) * h[1] + 1)
        * ((ell + 1) * h[1] + 1)
    )
    expected = (lam + 1, h[3], f1, f2, f3)
    variables = x + h + (lam,)
    lines = (
        "ring R=(0,p,q,kappa,ell),("
        + ",".join(str(variable) for variable in variables)
        + "),(dp(8),dp(5));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_expression(item) for item in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(str(variable) for variable in x) + "));",
        "ideal E=" + ",".join(singular_expression(item) for item in expected) + ";",
        "E=std(E);",
        "ideal left=simplify(reduce(J,E),2);",
        "ideal right=simplify(reduce(E,J),2);",
        "poly beta_diagonal=" + singular_expression(model["B"]) + ";",
        "poly beta_remainder=reduce(beta_diagonal,I);",
        (
            '"CODEX_AUDIT:"+string((size(left)==0)&&(size(right)==0))+":"'
            '+string(beta_remainder==0)+":"+string(size(I))+":"+string(size(J));'
        ),
        "quit;",
    )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(lines),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=120,
    )
    require(
        completed.returncode == 0 and not completed.stderr.strip(),
        f"finite D23 Singular failure: {completed.stdout[-1000:]} {completed.stderr[-1000:]}",
    )
    markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_AUDIT:")
    ]
    require(len(markers) == 1, "finite D23 marker")
    _, same_ideal, beta_zero, full_size, projection_size = markers[0].split(":")
    require(same_ideal == "1", "finite D23 projected ideal differs")
    require(beta_zero == "1", "B23 is not in the complete normalized ideal")

    # Every equation is homogeneous linear in the extension vector except for
    # the explicit affine normalization A23-1.  Hence A23!=0 is exhausted by
    # rescaling the same extension vector to A23=1; no parameter saturation is
    # hidden in the normalization.
    linear_coefficients = tuple(model["coefficients"].values())
    require(
        all(sp.Poly(item, *x).total_degree() <= 1 for item in linear_coefficients),
        "contracted coefficients are not extension-linear",
    )
    require(
        all(item.subs(dict.fromkeys(x, 0)) == 0 for item in linear_coefficients),
        "contracted coefficient has an extension-independent term",
    )
    return (
        {
            "chart": "[lambda:1]",
            "projected_ideal": ["lambda+1", "h3", "F1", "F2", "F3"],
            "F1": str(sp.factor(f1)),
            "F2": str(sp.factor(f2)),
            "F3": str(sp.factor(f3)),
            "bidirectional_scheme_ideal_equality": True,
            "complete_normalized_ideal_basis_size": int(full_size),
            "projection_basis_size": int(projection_size),
            "B23_normal_form": "0",
            "B23_in_complete_normalized_ideal": True,
            "normalization_A23_equals_one_exhausts_A23_nonzero": True,
            "normalization_uses_only_extension_scaling": True,
            "finite_endpoint_0_1_excluded_by_lambda_plus_one": True,
            "only_possible_finite_A23_slope": "[-1:1]",
            "closure_not_used_for_binary_emptiness": True,
        },
        (f1, f2, f3),
    )


def infinity_d23_certificate(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
) -> dict[str, Any]:
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    beta = mark_beta(alpha, unmarked_beta, h)
    model = d23_model(alpha, beta, x, "infinity")
    mixed = model["mixed_matrix"]
    alpha_row = tuple(sp.diff(model["A"], variable) for variable in x)
    beta_row = tuple(sp.diff(model["B"], variable) for variable in x)
    module_rows = ",".join(
        "["
        + ",".join(singular_expression(mixed[row, column]) for column in range(8))
        + "]"
        for row in range(14)
    )
    alpha_vector = "[" + ",".join(singular_expression(item) for item in alpha_row) + "]"
    beta_vector = "[" + ",".join(singular_expression(item) for item in beta_row) + "]"
    lines = (
        "ring R=(0,p,q,kappa,ell),(h0,h1,h2,h3),dp;",
        "option(redSB);",
        "module M=" + module_rows + ";",
        "M=std(M);",
        "vector alpha_row=" + alpha_vector + ";",
        "vector beta_row=" + beta_vector + ";",
        "vector alpha_remainder=reduce(alpha_row,M);",
        "vector beta_remainder=reduce(beta_row,M);",
        (
            '"CODEX_AUDIT:"+string(alpha_remainder==0)+":"'
            '+string(beta_remainder!=0)+":"+string(size(M));'
        ),
        "quit;",
    )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(lines),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=120,
    )
    require(
        completed.returncode == 0 and not completed.stderr.strip(),
        f"infinity D23 Singular failure: {completed.stdout[-1000:]} {completed.stderr[-1000:]}",
    )
    markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_AUDIT:")
    ]
    require(len(markers) == 1, "infinity D23 marker")
    _, alpha_zero, beta_nonzero, module_size = markers[0].split(":")
    require(alpha_zero == "1", "A23 infinity row is not in the mixed row module")
    require(beta_nonzero == "1", "B23 infinity normal form unexpectedly zero")
    return {
        "chart": "[1:0]",
        "A23_in_polynomial_mixed_row_module": True,
        "A23_row_remainder": "0",
        "B23_row_remainder_nonzero": True,
        "module_coefficient_ring": "Q(p,q,kappa,ell)[h0,h1,h2,h3]",
        "marking_denominators_introduced": False,
        "standard_module_basis_size": int(module_size),
        "genuine_binary_incidence_empty": True,
    }


def one_diagonal_survivor(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    f_equations: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> dict[str, Any]:
    x = sp.symbols("x0:8")
    h = (1 / (p - q), 0, kappa, 0)
    beta = mark_beta(alpha, unmarked_beta, h)
    model = d23_model(alpha, beta, x, "finite", sp.Integer(-1))
    extension = sp.Matrix(
        (
            -q / kappa,
            -1 / kappa,
            0,
            0,
            -p / (kappa * (p - q)),
            0,
            1,
            0,
        )
    )
    substitution = dict(zip(x, extension, strict=True))
    mixed_values = [
        sp.factor(model["coefficients"][word].subs(substitution))
        for word in MIXED_WORDS
    ]
    require(all(value == 0 for value in mixed_values), "survivor mixed coefficient")
    alpha_value = sp.factor(model["A"].subs(substitution))
    beta_value = sp.factor(model["B"].subs(substitution))
    require(sp.factor(alpha_value - 4 * (p - q) / kappa) == 0, "survivor A23")
    require(beta_value == 0, "survivor B23")
    marking_substitution = {
        sp.Symbol("h0"): h[0],
        sp.Symbol("h1"): h[1],
        sp.Symbol("h2"): h[2],
        sp.Symbol("h3"): h[3],
    }
    require(
        all(sp.factor(item.subs(marking_substitution)) == 0 for item in f_equations),
        "survivor is not on F1=F2=F3",
    )
    return {
        "weight": "[-1:1]",
        "marking": "h0=1/(p-q), h1=0, h2=kappa, h3=0",
        "extension": [str(sp.factor(item)) for item in extension],
        "all_14_mixed_coefficients_zero": True,
        "A23": str(alpha_value),
        "B23": str(beta_value),
        "generic_denominators": ["kappa", "p-q"],
        "denominators_are_units_in_function_field": True,
        "finite_A23_row_module_claim": "REFUTED_BY_SURVIVOR",
        "status": "one-diagonal survivor, not binary",
    }


def replay_dependencies() -> dict[str, Any]:
    p4 = run_json(
        (
            "uv",
            "run",
            "--with",
            "sympy",
            "python",
            P4_SCRIPT.relative_to(ROOT).as_posix(),
        ),
        timeout=120,
    )
    h31 = run_json(
        (
            "uv",
            "run",
            "--with",
            "sympy",
            "python",
            H31_SCRIPT.relative_to(ROOT).as_posix(),
        ),
        timeout=180,
    )
    require(p4.get("status") == "verified", "P4 component replay")
    require(h31.get("status") == "pass", "H31 replay")
    require(h31.get("generic_marked_H31_fibre_empty") is True, "H31 conclusion")
    return {
        "P4": {"status": p4["status"]},
        "H31": {
            "status": h31["status"],
            "generic_marked_H31_fibre_empty": h31["generic_marked_H31_fibre_empty"],
        },
    }


def audit_candidate_artifacts(
    finite: dict[str, Any], infinity: dict[str, Any], survivor: dict[str, Any]
) -> dict[str, Any]:
    certificate = json.loads(CANDIDATE_CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate.get("claim_label") == "VERIFIED", "claim not promoted")
    require(
        certificate.get("discovery_claim_label") == "CANDIDATE"
        and certificate.get("independent_verifier_complete") is True,
        "discovery or independent-verification status changed",
    )
    require(
        certificate["normal_form"]["pure_support"] == {"1111": "4*p"},
        "candidate pure support",
    )
    claimed_finite = certificate["D23_finite"]
    require(
        claimed_finite["all_alpha_normalized_projection"]
        == ["lambda+1", "h3", "F1", "F2", "F3"],
        "candidate finite projection labels",
    )

    p, q, kappa, ell = sp.symbols("p q kappa ell")
    h = sp.symbols("h0:4")
    delta = p**2 - q**2
    epsilon = ell**2 - 1
    locals_map = {
        "p": p,
        "q": q,
        "kappa": kappa,
        "ell": ell,
        "Delta": delta,
        "E": epsilon,
        **{str(symbol): symbol for symbol in h},
    }
    for label in ("F1", "F2", "F3"):
        require(
            sp.factor(
                sp.sympify(finite[label], locals=locals_map)
                - sp.sympify(claimed_finite["definitions"][label], locals=locals_map)
            )
            == 0,
            f"candidate {label}",
        )
    require(
        claimed_finite["all_beta_remainder_in_normalized_mixed_ideal"] == "0"
        and finite["B23_in_complete_normalized_ideal"] is True,
        "candidate B23 reduction",
    )
    claimed_infinity = certificate["D23_infinity"]
    require(
        claimed_infinity["all_alpha_in_mixed_row_module"]
        == infinity["A23_in_polynomial_mixed_row_module"],
        "candidate infinity A23 module",
    )
    require(
        claimed_infinity["all_beta_normal_form_nonzero"]
        == infinity["B23_row_remainder_nonzero"],
        "candidate infinity B23 remainder",
    )
    require(
        certificate["retained_survivor"]["all_beta_diagonal"] == survivor["B23"],
        "candidate survivor B23",
    )

    report_text = CANDIDATE_REPORT.read_text(encoding="utf-8")
    scope_markers = {
        "verified_status": "**VERIFIED after a fresh independent no-import replay:**"
        in report_text,
        "generic_field": "K=Q(p,q,kappa,ell)" in report_text,
        "special_boundaries_open": "Special parameter and\n  projective component-boundary fibres remain open"
        in report_text,
        "global_excluded": "global Krenn--Gu claim" in report_text,
    }
    require(all(scope_markers.values()), "candidate report lost scope boundary")
    return {
        "certificate_json_valid": True,
        "certificate_claims_match_independent_reconstruction": True,
        "candidate_script_imported": False,
        "scope_markers": scope_markers,
    }


def main() -> None:
    inputs = (
        CANDIDATE_REPORT,
        CANDIDATE_SCRIPT,
        CANDIDATE_CERTIFICATE,
        P4_REPORT,
        P4_SCRIPT,
        H31_REPORT,
        H31_SCRIPT,
        H22_DEFINITION,
    )
    for path in inputs:
        require(path.is_file(), f"missing input: {path.name}")

    p, q, kappa, ell = sp.symbols("p q kappa ell")
    alpha, beta = component_bases(p, q, kappa, ell)
    h = sp.symbols("h0:4")
    for coefficients in (
        four_source_coefficients(alpha, beta),
        four_source_coefficients(alpha, mark_beta(alpha, beta, h)),
    ):
        require(
            all(
                value == 0 for word, value in coefficients.items() if word != BETA_WORD
            ),
            "four-source mixed coefficient",
        )
        require(sp.factor(coefficients[BETA_WORD] - 4 * p) == 0, "pure coefficient")

    dependencies = replay_dependencies()
    hall = d01_hall_certificate(alpha)
    finite, f_equations = finite_d23_certificate(alpha, beta, p, q, kappa, ell)
    infinity = infinity_d23_certificate(alpha, beta)
    survivor = one_diagonal_survivor(alpha, beta, p, q, kappa, f_equations)
    artifact_audit = audit_candidate_artifacts(finite, infinity, survivor)

    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "generic weighted H22 fibre of component twenty-one",
        "inputs": {path.name: sha256(path) for path in inputs},
        "method": (
            "fresh subset-DP permanents, homogeneous Hall certificate, exact "
            "characteristic-zero finite elimination and beta reduction, direct "
            "infinity row-module reduction, and exact one-diagonal witness"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            REPORT.name: sha256(REPORT) if REPORT.is_file() else "pending",
            SCRIPT.name: sha256(SCRIPT),
        },
        "limitations": (
            "generic function-field theorem only; no special-parameter or "
            "projective component-boundary fibres, P4 component exhaustiveness, "
            "arbitrary-order local-to-global reduction, prize graph, or global "
            "Krenn-Gu conclusion"
        ),
        "dependency_replays": dependencies,
        "pure_support": {"1111": "4*p"},
        "D01_homogeneous_Hall_certificate": hall,
        "D23_finite_certificate": finite,
        "D23_infinity_certificate": infinity,
        "retained_one_diagonal_survivor": survivor,
        "normalization_saturation_or_closure_gap": False,
        "parameter_denominator_gap_at_generic_point": False,
        "projective_weight_endpoint_gap": False,
        "candidate_artifact_audit": artifact_audit,
        "generic_weighted_H22_fibre_empty": True,
        "finite_field_computation_used_as_proof": False,
        "broad_brute_force_used": False,
        "candidate_script_imported": False,
        "special_or_projective_boundary_fibres_closed": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
