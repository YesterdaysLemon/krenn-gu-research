#!/usr/bin/env python3
"""No-import exact audit of the component-20 generic weighted-H22 candidate."""

from __future__ import annotations

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
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md"
)
CANDIDATE_REPORT = ROOT / (
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md"
)
CANDIDATE_SCRIPT = ROOT / (
    "derive_p5_h22_common_active_binary_triangle_component_generic_"
    "obstruction_candidate.py"
)
CANDIDATE_CERTIFICATE = ROOT / (
    "p5_h22_common_active_binary_triangle_component_generic_certificate.json"
)
P4_REPORT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
P4_SCRIPT = ROOT / "verify_p4_common_active_binary_triangle_component.py"
H31_REPORT = ROOT / (
    "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
H31_SCRIPT = ROOT / (
    "verify_p5_h31_common_active_binary_triangle_component_generic_obstruction.py"
)
P_PLUS_Q_WALL = ROOT / (
    "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"
)

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
    p: sp.Symbol, q: sp.Symbol
) -> tuple[tuple[tuple[Any, ...], ...], tuple[tuple[Any, ...], ...]]:
    s = p - q + 1
    e = (1, 0, 0, 0)
    alpha = (
        (0, -p * (p + 1), q * (q - 1), s),
        e,
        e,
        (1, 1, 1, 0),
    )
    beta = (
        (-s, -(p + q), p + q, 0),
        (0, p + 1, q - 1, 1),
        (0, p, q, 1),
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
        coefficients[word] = sp.factor(permanent_by_subsets(selected))
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
    return str(sp.cancel(expression)).replace("**", "^")


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


def projection_check(
    label: str,
    equations: tuple[Any, ...],
    eliminated: tuple[sp.Symbol, ...],
    retained: tuple[sp.Symbol, ...],
    expected: tuple[Any, ...] | None,
) -> dict[str, Any]:
    variables = eliminated + retained
    lines = [
        "ring R=(0,p,q),("
        + ",".join(str(variable) for variable in variables)
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_expression(item) for item in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(str(item) for item in eliminated) + "));",
    ]
    if expected is None:
        lines.append('"CODEX_AUDIT:"+string(reduce(1,J)==0)+":"+string(size(J));')
    else:
        lines.extend(
            (
                "ideal E="
                + ",".join(singular_expression(item) for item in expected)
                + ";",
                "E=std(E);",
                "ideal left=simplify(reduce(J,E),2);",
                "ideal right=simplify(reduce(E,J),2);",
                '"CODEX_AUDIT:"+string((size(left)==0)&&(size(right)==0))+":"+string(size(J));',
            )
        )
    lines.append("quit;")
    stdout = run_singular("\n".join(lines), label)
    markers = [line for line in stdout.splitlines() if line.startswith("CODEX_AUDIT:")]
    require(len(markers) == 1, f"{label}: missing output marker")
    fields = markers[0].split(":")
    require(fields[1] == "1", f"{label}: projected ideal mismatch")
    return {
        "label": label,
        "projected_ideal": ["1"]
        if expected is None
        else [str(sp.factor(item)) for item in expected],
        "bidirectional_ideal_equality": expected is not None,
        "standard_basis_size": int(fields[2]),
    }


def projection_certificates(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
    p: sp.Symbol,
    q: sp.Symbol,
) -> tuple[list[dict[str, Any]], sp.Expr]:
    lam = sp.Symbol("lam")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    inverse_first, inverse_second = sp.symbols("inverse_first inverse_second")
    beta = mark_beta(alpha, unmarked_beta, h)
    finite_d01 = contraction_model(alpha, beta, x, "D01", "finite", lam)
    finite_d23 = contraction_model(alpha, beta, x, "D23", "finite", lam)

    relation = sp.expand(
        lam * h[1] * h[2] * q * (q - 1)
        + lam * h[1] * p * q * (p + 1)
        + lam * h[2] * p * (p + 1) * (q - 1)
        + h[1] * p * q * (p + q)
        + h[2] * (p + q) * (p + 1) * (q - 1)
        + lam * p * q * (p + 1) * (q - 1)
    )
    certificates = [
        projection_check(
            "finite_D01_individual_binary_projection",
            (
                *finite_d01["mixed"],
                finite_d01["A"] - 1,
                inverse_first * finite_d01["B"] - 1,
            ),
            x + (inverse_first,),
            h + (lam,),
            (h[3], h[0], relation),
        )
    ]

    restricted_h = (sp.Integer(0), h[1], h[2], sp.Integer(0))
    restricted_beta = mark_beta(alpha, unmarked_beta, restricted_h)
    restricted_d01 = contraction_model(alpha, restricted_beta, x, "D01", "finite", lam)
    restricted_d23 = contraction_model(alpha, restricted_beta, x, "D23", "finite", lam)
    certificates.append(
        projection_check(
            "finite_shared_D01_orientation_after_necessary_projection",
            (
                *restricted_d01["mixed"],
                *restricted_d23["mixed"],
                restricted_d01["A"] - 1,
                inverse_first * restricted_d01["B"] - 1,
                inverse_second * restricted_d23["B"] - 1,
                relation,
            ),
            x + (inverse_first, inverse_second),
            (h[1], h[2], lam),
            None,
        )
    )
    certificates.append(
        projection_check(
            "finite_shared_D23_orientation",
            (
                *finite_d01["mixed"],
                *finite_d23["mixed"],
                finite_d23["A"] - 1,
                inverse_first * finite_d23["B"] - 1,
                inverse_second * finite_d01["B"] - 1,
            ),
            x + (inverse_first, inverse_second),
            h + (lam,),
            None,
        )
    )

    infinity_d01 = contraction_model(alpha, beta, x, "D01", "infinity")
    infinity_d23 = contraction_model(alpha, beta, x, "D23", "infinity")
    certificates.append(
        projection_check(
            "infinity_shared_D01_orientation",
            (
                *infinity_d01["mixed"],
                *infinity_d23["mixed"],
                infinity_d01["A"] - 1,
                inverse_first * infinity_d01["B"] - 1,
                inverse_second * infinity_d23["B"] - 1,
            ),
            x + (inverse_first, inverse_second),
            h,
            None,
        )
    )
    certificates.append(
        projection_check(
            "infinity_shared_D23_orientation",
            (
                *infinity_d01["mixed"],
                *infinity_d23["mixed"],
                infinity_d23["A"] - 1,
                inverse_first * infinity_d23["B"] - 1,
                inverse_second * infinity_d01["B"] - 1,
            ),
            x + (inverse_first, inverse_second),
            h,
            None,
        )
    )

    models = (finite_d01, finite_d23, infinity_d01, infinity_d23)
    require(
        all(
            sp.Poly(coefficient, *x).total_degree() <= 1
            and coefficient.subs(dict.fromkeys(x, 0)) == 0
            for model in models
            for coefficient in model["coefficients"].values()
        ),
        "contracted coefficients are not homogeneous linear in the extension",
    )
    return certificates, relation


def replay_dependencies() -> dict[str, Any]:
    p4 = run_json(
        ("uv", "run", "--with", "sympy", "python", P4_SCRIPT.name), timeout=180
    )
    h31 = run_json(
        ("uv", "run", "--with", "sympy", "python", H31_SCRIPT.name), timeout=180
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
    certificates: list[dict[str, Any]], relation: sp.Expr
) -> dict[str, Any]:
    certificate = json.loads(CANDIDATE_CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate.get("claim_label") == "VERIFIED", "claim not promoted")
    require(
        certificate.get("discovery_claim_label") == "CANDIDATE"
        and certificate.get("independent_verifier_complete") is True,
        "discovery or independent-verification status changed",
    )
    expected_pure = {"1111": "2*(p+q)*(p-q+1)"}
    require(
        certificate["normal_form"]["pure_support"] == expected_pure,
        "candidate pure support",
    )
    cover = certificate["projective_weight_cover"]
    require(
        cover["D01_finite_binary_marking_projection"] == ["h3", "h0", "F"],
        "candidate D01 projection labels",
    )
    p, q = sp.symbols("p q")
    h1, h2, lam = sp.symbols("h1 h2 lam")
    parsed_f = sp.sympify(
        cover["F"].replace("lambda", "lam"),
        locals={"p": p, "q": q, "h1": h1, "h2": h2, "lam": lam},
    )
    require(sp.factor(parsed_f - relation) == 0, "candidate marking relation F")
    by_label = {item["label"]: item for item in certificates}
    require(
        by_label["finite_D01_individual_binary_projection"][
            "bidirectional_ideal_equality"
        ]
        is True,
        "independent D01 ideal equality",
    )
    for label in (
        "finite_shared_D01_orientation_after_necessary_projection",
        "finite_shared_D23_orientation",
        "infinity_shared_D01_orientation",
        "infinity_shared_D23_orientation",
    ):
        require(by_label[label]["projected_ideal"] == ["1"], f"{label} not unit")
    for key in (
        "finite_shared_D01_binary_after_restriction",
        "finite_shared_D23_binary",
        "infinity_shared_D01_binary",
        "infinity_shared_D23_binary",
    ):
        require(cover[key] == ["1"], f"candidate {key}")
    timeout_entries = [
        item for item in certificate["failed_attempts"] if item["status"] == "TIMEOUT"
    ]
    require(len(timeout_entries) == 1, "timeout ledger changed")
    require(timeout_entries[0]["result_used_as_evidence"] is False, "timeout promoted")

    candidate_text = CANDIDATE_REPORT.read_text(encoding="utf-8")
    wall_text = P_PLUS_Q_WALL.read_text(encoding="utf-8")
    scope_markers = {
        "verified_status": "**VERIFIED after a fresh independent no-import replay:**"
        in candidate_text,
        "generic_field": "K=Q(p,q)" in candidate_text,
        "wall_separate": "does not overlap the separately verified `p+q=0`"
        in candidate_text,
        "timeout_non_evidence": "It is not evidence" in candidate_text,
        "special_fibres_open": "No special parameter or projective component-boundary fibre"
        in candidate_text,
        "wall_is_scoped_theorem": "diagonal-source-torus" in wall_text,
    }
    require(all(scope_markers.values()), "scope or failure boundary missing")
    return {
        "certificate_json_valid": True,
        "candidate_claims_match_independent_reconstruction": True,
        "candidate_script_imported": False,
        "timeout_replayed_or_used": False,
        "p_plus_q_wall_used_in_generic_proof": False,
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
        P_PLUS_Q_WALL,
    )
    for path in inputs:
        require(path.is_file(), f"missing input: {path.name}")

    p, q = sp.symbols("p q")
    alpha, beta = component_bases(p, q)
    h = sp.symbols("h0:4")
    expected_pure = 2 * (p + q) * (p - q + 1)
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
            sp.factor(coefficients[BETA_WORD] - expected_pure) == 0,
            "four-source pure coefficient",
        )

    dependencies = replay_dependencies()
    certificates, relation = projection_certificates(alpha, beta, p, q)
    artifact_audit = audit_candidate_artifacts(certificates, relation)

    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "generic weighted H22 fibre of component twenty over Q(p,q)",
        "inputs": {path.name: sha256(path) for path in inputs},
        "method": (
            "fresh subset-DP permanents and five bounded characteristic-zero "
            "Singular projections for one shared marking, homogeneous weight, "
            "and extension vector"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            REPORT.name: sha256(REPORT) if REPORT.is_file() else "pending",
            SCRIPT.name: sha256(SCRIPT),
        },
        "limitations": (
            "generic function field only; separately verified p+q=0 diagonal-DVR "
            "wall not used; no other special/projective fibres, P4 component "
            "exhaustiveness, arbitrary-order local-to-global reduction, prize "
            "graph, or global Krenn-Gu conclusion"
        ),
        "dependency_replays": dependencies,
        "pure_support": {"1111": str(sp.factor(expected_pure))},
        "orientation_cover": {
            "common_requirements": "M01*z=M23*z=0 and B01*B23!=0",
            "binary_requirement": "A01!=0 or A23!=0",
            "finite_orientations": ["normalize A01=1", "normalize A23=1"],
            "infinity_orientations": ["normalize A01=1", "normalize A23=1"],
            "complete": True,
        },
        "projection_certificates": certificates,
        "finite_D01_marking_relation": str(sp.factor(relation)),
        "staged_D01_projection_used_as_necessary_not_sufficient": True,
        "staged_restricted_unit_closes_entire_projection_closure": True,
        "shared_weight_and_extension_preserved": True,
        "normalization_saturation_gap": False,
        "orientation_gap": False,
        "projective_endpoint_gap": False,
        "generic_denominator_gap": False,
        "broad_D23_timeout_used_as_evidence": False,
        "candidate_artifact_audit": artifact_audit,
        "generic_weighted_H22_fibre_empty": True,
        "finite_field_computation_used_as_proof": False,
        "broad_brute_force_used": False,
        "candidate_script_imported": False,
        "p_plus_q_wall_recomputed_or_used": False,
        "special_or_projective_fibres_closed": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
