#!/usr/bin/env python3
"""Independent exact audit of component 20's intrinsic-wall H22 candidate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_"
    "OBSTRUCTION_VERIFICATION.md"
)
CANDIDATE_REPORT = ROOT / (
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md"
)
CANDIDATE_SCRIPT = ROOT / (
    "derive_p5_h22_common_active_binary_triangle_intrinsic_boundary_"
    "obstruction_candidate.py"
)
CANDIDATE_CERTIFICATE = ROOT / (
    "p5_h22_common_active_binary_triangle_intrinsic_boundary_certificate.json"
)
H31_REPORT = REPO_ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md"
H31_SCRIPT = REPO_ROOT / "verify_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py"
GENERIC_H22 = REPO_ROOT / "claims/p5/h22/common-active-binary-triangle-component-generic/P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md"
P_PLUS_Q_WALL = REPO_ROOT / "claims/p5/h22/disputed-ownership/p-plus-q-wall/P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"

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
        cwd=REPO_ROOT,
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
        sp.factor(sum(vector[index] for vector in vectors)) for index in range(4)
    )


def vector_scale(scalar: Any, vector: tuple[Any, ...]) -> tuple[Any, ...]:
    return tuple(sp.factor(scalar * entry) for entry in vector)


def permanent_by_subsets(rows: tuple[tuple[Any, ...], ...]) -> sp.Expr:
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
                next_states[target] = sp.factor(
                    next_states.get(target, sp.Integer(0)) + coefficient * entry
                )
        states = next_states
    return sp.factor(states[(1 << width) - 1])


def replacement_bases(
    p: sp.Symbol,
) -> tuple[tuple[tuple[Any, ...], ...], tuple[tuple[Any, ...], ...]]:
    zero, one = sp.Integer(0), sp.Integer(1)
    e = (one, zero, zero, zero)
    alpha = (
        (zero, -one, one, zero),
        e,
        e,
        (one, one, one, zero),
    )
    beta = (
        (p * (p + 1) / (2 * p + 1), -2 * p - 1, zero, one),
        (zero, p + 1, p, one),
        (zero, p, p + 1, one),
        e,
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
        word: permanent_by_subsets(
            tuple(beta[index] if word[index] else alpha[index] for index in range(4))
        )
        for word in WORDS
    }


def project_row(
    row: tuple[Any, ...],
    extension: Any,
    direction: str,
    chart: str,
    slope: Any | None,
) -> tuple[Any, ...]:
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart, slope))


def contraction_model(
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
    extensions: tuple[Any, ...],
    direction: str,
    chart: str,
    slope: Any | None = None,
) -> dict[str, Any]:
    alpha_rows = tuple(
        project_row(alpha[index], extensions[index], direction, chart, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        project_row(beta[index], extensions[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = permanent_by_subsets(selected)
    return {
        "coefficients": coefficients,
        "mixed": tuple(coefficients[word] for word in MIXED_WORDS),
        "A": coefficients[ALPHA_WORD],
        "B": coefficients[BETA_WORD],
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact projection audit")


def singular_expression(expression: Any) -> str:
    numerator, denominator = sp.together(expression).as_numer_denom()
    numerator_text = str(sp.expand(numerator)).replace("**", "^")
    denominator_text = str(sp.factor(denominator)).replace("**", "^")
    if denominator == 1:
        return numerator_text
    return f"({numerator_text})/({denominator_text})"


def run_singular(program: str, label: str) -> str:
    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    process = subprocess.Popen(
        singular_command(),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creation_flags,
    )
    try:
        stdout, stderr = process.communicate(program, timeout=120)
    except subprocess.TimeoutExpired as exc:
        if os.name == "nt":
            subprocess.run(
                ("taskkill", "/PID", str(process.pid), "/T", "/F"),
                capture_output=True,
                check=False,
                timeout=15,
            )
        else:
            process.kill()
        process.communicate()
        raise AssertionError(f"{label}: bounded Singular replay timed out") from exc
    require(
        process.returncode == 0 and not stderr.strip(),
        f"{label}: Singular failed: {stdout[-1000:]} {stderr[-1000:]}",
    )
    return stdout


def unit_projection(
    label: str,
    equations: tuple[Any, ...],
    eliminated: tuple[sp.Symbol, ...],
    retained: tuple[sp.Symbol, ...],
) -> dict[str, Any]:
    variables = eliminated + retained
    lines = (
        "ring R=(0,p),("
        + ",".join(str(variable) for variable in variables)
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_expression(item) for item in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(str(item) for item in eliminated) + "));",
        "ideal E=1;",
        "E=std(E);",
        "ideal left=simplify(reduce(J,E),2);",
        "ideal right=simplify(reduce(E,J),2);",
        '"CODEX_AUDIT:"+string((size(left)==0)&&(size(right)==0))+":"+string(size(J));',
        "quit;",
    )
    stdout = run_singular("\n".join(lines), label)
    markers = [line for line in stdout.splitlines() if line.startswith("CODEX_AUDIT:")]
    require(len(markers) == 1, f"{label}: missing output marker")
    fields = markers[0].split(":")
    require(fields[1] == "1", f"{label}: projection is not the unit ideal")
    return {
        "label": label,
        "projected_ideal": ["1"],
        "bidirectional_unit_ideal_equality": True,
        "standard_basis_size": int(fields[2]),
    }


def projection_certificates(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
) -> dict[str, list[dict[str, Any]]]:
    lam = sp.Symbol("lam")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    inverse_first, inverse_second = sp.symbols("inverse_first inverse_second")
    beta = mark_beta(alpha, unmarked_beta, h)
    individual = []
    shared = []
    all_models = []
    for chart in ("finite", "infinity"):
        retained = h + ((lam,) if chart == "finite" else ())
        models = {
            direction: contraction_model(alpha, beta, x, direction, chart, lam)
            for direction in ("D01", "D23")
        }
        all_models.extend(models.values())
        for direction in ("D01", "D23"):
            model = models[direction]
            individual.append(
                unit_projection(
                    f"{chart}_{direction}_individual_binary",
                    (
                        *model["mixed"],
                        model["A"] - 1,
                        inverse_first * model["B"] - 1,
                    ),
                    x + (inverse_first,),
                    retained,
                )
            )
        for direction, other_direction in (("D01", "D23"), ("D23", "D01")):
            model = models[direction]
            other = models[other_direction]
            shared.append(
                unit_projection(
                    f"{chart}_{direction}_shared_orientation",
                    (
                        *model["mixed"],
                        *other["mixed"],
                        model["A"] - 1,
                        inverse_first * model["B"] - 1,
                        inverse_second * other["B"] - 1,
                    ),
                    x + (inverse_first, inverse_second),
                    retained,
                )
            )

    require(
        all(
            sp.Poly(coefficient, *x).total_degree() <= 1
            and coefficient.subs(dict.fromkeys(x, 0)) == 0
            for model in all_models
            for coefficient in model["coefficients"].values()
        ),
        "contracted coefficient is not homogeneous linear in the extension",
    )
    return {"individual_binary": individual, "shared_H22": shared}


def replay_h31_dependency() -> dict[str, Any]:
    h31 = run_json(
        ("uv", "run", "--with", "sympy", "python", H31_SCRIPT.relative_to(REPO_ROOT).as_posix()), timeout=180
    )
    require(h31.get("status") == "pass", "intrinsic-wall H31 replay")
    return {"status": h31["status"]}


def audit_candidate_artifacts(
    projections: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    certificate = json.loads(CANDIDATE_CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate.get("claim_label") == "VERIFIED", "verified label changed")
    require(
        certificate.get("discovery_claim_label") == "CANDIDATE",
        "discovery label changed",
    )
    require(
        certificate.get("independent_verifier_complete") is True,
        "independent verification marker missing",
    )
    normal = certificate["replacement_normal_form"]
    require(normal["base_divisor"] == "q=p+1", "candidate base divisor")
    require(normal["pure_support"] == {"1111": "-2*p*(p+1)"}, "candidate pure support")
    require(
        normal["excluded_component_parameters"]
        == ["p=0", "p=-1", "p=-1/2", "p=infinity"],
        "candidate exclusions",
    )
    require(
        all(
            item["projected_ideal"] == ["1"]
            for item in projections["individual_binary"]
        ),
        "independent individual projection",
    )
    require(
        all(item["projected_ideal"] == ["1"] for item in projections["shared_H22"]),
        "independent shared projection",
    )
    cover = certificate["projective_weight_cover"]
    require(
        all(
            value == ["1"] for value in cover["individual_binary_projections"].values()
        ),
        "candidate individual projection",
    )
    require(
        all(value == ["1"] for value in cover["shared_H22_projections"].values()),
        "candidate shared projection",
    )

    candidate_text = CANDIDATE_REPORT.read_text(encoding="utf-8")
    h31_text = H31_REPORT.read_text(encoding="utf-8")
    generic_text = GENERIC_H22.read_text(encoding="utf-8")
    wall_text = P_PLUS_Q_WALL.read_text(encoding="utf-8")
    scope_markers = {
        "verified_status": "**VERIFIED after a fresh independent no-import replay:**"
        in candidate_text,
        "replacement_not_specialization": "generic component basis collapses"
        in candidate_text,
        "exceptional_parameters_open": "p=0,-1,-1/2" in candidate_text,
        "parameter_infinity_open": "component-parameter infinity" in candidate_text,
        "p_plus_q_wall_separate": "verified `p+q=0` wall is a separate theorem"
        in candidate_text,
        "h31_divisor_generic": "divisor-generic" in h31_text,
        "generic_q_p_field_separate": "Q(p,q)" in generic_text,
        "wall_diagonal_scope": "diagonal-source-torus" in wall_text,
    }
    require(all(scope_markers.values()), "scope boundary missing")
    return {
        "certificate_json_valid": True,
        "candidate_claims_match_independent_reconstruction": True,
        "candidate_script_imported": False,
        "generic_H22_theorem_used": False,
        "p_plus_q_wall_used": False,
        "scope_markers": scope_markers,
    }


def main() -> None:
    inputs = (
        CANDIDATE_REPORT,
        CANDIDATE_SCRIPT,
        CANDIDATE_CERTIFICATE,
        H31_REPORT,
        H31_SCRIPT,
        GENERIC_H22,
        P_PLUS_Q_WALL,
    )
    for path in inputs:
        require(path.is_file(), f"missing input: {path.name}")

    p = sp.Symbol("p")
    alpha, beta = replacement_bases(p)
    require(
        all(sp.Matrix((alpha[index], beta[index])).rank() == 2 for index in range(4)),
        "replacement basis rank",
    )
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
        require(
            sp.factor(coefficients[BETA_WORD] + 2 * p * (p + 1)) == 0,
            "four-source pure coefficient",
        )

    denominators = {
        str(sp.factor(sp.together(entry).as_numer_denom()[1]))
        for plane in (alpha, beta)
        for row in plane
        for entry in row
    }
    require(denominators == {"1", "2*p + 1"}, "replacement basis denominator set")

    h31 = replay_h31_dependency()
    projections = projection_certificates(alpha, beta)
    artifact_audit = audit_candidate_artifacts(projections)

    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "generic weighted H22 fibre on q=p+1 over Q(p)",
        "inputs": {path.name: sha256(path) for path in inputs},
        "method": (
            "fresh replacement-basis subset-DP permanents and eight bounded "
            "characteristic-zero finite/infinity individual/shared projections"
        ),
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {
            REPORT.name: sha256(REPORT) if REPORT.is_file() else "pending",
            SCRIPT.name: sha256(SCRIPT),
        },
        "limitations": (
            "generic point of q=p+1 only; p=0,-1,-1/2, component-parameter "
            "infinity, mixed source-torus/projective limits, and unrelated special "
            "fibres remain open; generic Q(p,q) theorem and p+q wall not used; no "
            "P4 exhaustiveness, arbitrary-order reduction, prize graph, or global claim"
        ),
        "H31_dependency_replay": h31,
        "replacement_intrinsic_basis_used": True,
        "collapsed_generic_basis_specialized": False,
        "pure_support": {"1111": "-2*p*(p+1)"},
        "pure_coefficient_nonzero_open": "p*(p+1)!=0",
        "replacement_basis_denominators": sorted(denominators),
        "projection_certificates": projections,
        "all_four_individual_binary_projections_unit": True,
        "all_four_complete_shared_orientation_projections_unit": True,
        "orientation_cover_complete": True,
        "normalization_saturation_gap": False,
        "projective_weight_endpoint_gap": False,
        "parameter_denominator_gap_on_Q_p": False,
        "exceptional_parameters_closed": False,
        "parameter_infinity_closed": False,
        "p_plus_q_intersection": "p=-1/2, excluded because 2*p+1=0",
        "candidate_artifact_audit": artifact_audit,
        "generic_intrinsic_wall_weighted_H22_fibre_empty": True,
        "finite_field_computation_used_as_proof": False,
        "broad_brute_force_used": False,
        "candidate_script_imported": False,
        "generic_Q_p_q_theorem_used": False,
        "p_plus_q_wall_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
