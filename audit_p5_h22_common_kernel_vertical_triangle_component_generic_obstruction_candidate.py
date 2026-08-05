#!/usr/bin/env python3
"""No-import exact audit of the component-19 generic weighted-H22 candidate."""

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
    "P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_"
    "OBSTRUCTION_VERIFICATION.md"
)
CANDIDATE_REPORT = ROOT / (
    "P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md"
)
CANDIDATE_SCRIPT = ROOT / (
    "derive_p5_h22_common_kernel_vertical_triangle_component_generic_"
    "obstruction_candidate.py"
)
CANDIDATE_CERTIFICATE = ROOT / (
    "p5_h22_common_kernel_vertical_triangle_component_generic_certificate.json"
)
P4_REPORT = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
P4_SCRIPT = ROOT / "verify_p4_common_kernel_vertical_triangle_component.py"
H31_REPORT = ROOT / (
    "P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
H31_SCRIPT = ROOT / (
    "verify_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py"
)
H22_DEFINITION = ROOT / "P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"

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
    """Permanent by a row-by-row subset DP, independent of permutation code."""

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
    p: sp.Symbol, q: sp.Symbol, phi: sp.Symbol
) -> tuple[tuple[tuple[Any, ...], ...], tuple[tuple[Any, ...], ...]]:
    cap_a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    free_first = vector_sum(a_bar, vector_scale(p, cap_b))
    free_second = vector_sum(b_bar, vector_scale(q, cap_b))
    residual = q - phi
    alpha_zero = vector_sum(
        vector_scale(residual, free_first), vector_scale(-p, free_second)
    )
    alpha = (alpha_zero, cap_b, b_bar, a_bar)
    beta = (
        free_first,
        cap_a,
        cap_a,
        vector_sum(cap_b, vector_scale(phi, b_bar)),
    )
    # The mode-zero change from (free_first, free_second) to
    # (alpha_zero, beta_zero) has determinant p, a unit in Q(p,q,phi).
    require(
        sp.factor(sp.Matrix(((q - phi, -p), (1, 0))).det() - p) == 0,
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
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta[index] if word[index] else alpha[index] for index in range(4)
        )
        coefficients[word] = sp.factor(permanent_by_subsets(selected))
    return coefficients


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


def homogeneous_project_row(
    row: tuple[Any, ...],
    extension: Any,
    direction: str,
    rho: Any,
    sigma: Any,
) -> tuple[Any, ...]:
    if direction == "D01":
        return (rho * row[0] + sigma * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], rho * row[2] + sigma * row[3], extension)
    raise ValueError(direction)


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


def homogeneous_model(
    alpha: tuple[tuple[Any, ...], ...],
    beta: tuple[tuple[Any, ...], ...],
    extensions: tuple[Any, ...],
    direction: str,
    rho: Any,
    sigma: Any,
) -> dict[str, Any]:
    alpha_rows = tuple(
        homogeneous_project_row(alpha[index], extensions[index], direction, rho, sigma)
        for index in range(4)
    )
    beta_rows = tuple(
        homogeneous_project_row(
            beta[index], extensions[4 + index], direction, rho, sigma
        )
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = sp.factor(permanent_by_subsets(selected))
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "A": coefficients[ALPHA_WORD],
        "B": coefficients[BETA_WORD],
    }


def one_marked_matrix(model: dict[str, Any], mode: int) -> sp.Matrix:
    other_modes = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][source_mode]
            if bits[position]
            else model["alpha_rows"][source_mode]
            for position, source_mode in enumerate(other_modes)
        )
        rows.append(
            tuple(
                permanent_by_subsets(
                    tuple(
                        tuple(
                            entry
                            for column, entry in enumerate(row)
                            if column != omitted
                        )
                        for row in selected
                    )
                )
                for omitted in range(4)
            )
        )
    return sp.Matrix(rows)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact projection audit")


def singular_expression(expression: Any) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def exact_projection(
    label: str,
    equations: tuple[Any, ...],
    eliminated: tuple[sp.Symbol, ...],
    retained: tuple[sp.Symbol, ...],
    expected: tuple[Any, ...] | None,
) -> dict[str, Any]:
    variables = eliminated + retained
    lines = [
        "ring R=(0,p,q,phi),("
        + ",".join(str(variable) for variable in variables)
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I="
        + ",".join(singular_expression(equation) for equation in equations)
        + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(str(item) for item in eliminated) + "));",
    ]
    if expected is None:
        lines.append('"CODEX_AUDIT:"+string(reduce(1,J)==0)+":"+string(size(J));')
    else:
        lines.extend(
            (
                "ideal E="
                + ",".join(singular_expression(equation) for equation in expected)
                + ";",
                "E=std(E);",
                "ideal left=simplify(reduce(J,E),2);",
                "ideal right=simplify(reduce(E,J),2);",
                '"CODEX_AUDIT:"+string((size(left)==0)&&(size(right)==0))+":"+string(size(J));',
            )
        )
    lines.append("quit;")
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
        f"{label}: Singular failed: {completed.stdout[-1000:]} {completed.stderr[-1000:]}",
    )
    markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_AUDIT:")
    ]
    require(len(markers) == 1, f"{label}: missing Singular marker")
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


def projective_elimination(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
    p: sp.Symbol,
    q: sp.Symbol,
    phi: sp.Symbol,
) -> list[dict[str, Any]]:
    lam = sp.Symbol("lam")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    inverse_a, inverse_b = sp.symbols("inverse_a inverse_b")
    beta = mark_beta(alpha, unmarked_beta, h)
    certificates = []

    for chart in ("finite", "infinity"):
        retained = h + ((lam,) if chart == "finite" else ())
        d01 = contraction_model(alpha, beta, x, "D01", chart, lam)
        d23 = contraction_model(alpha, beta, x, "D23", chart, lam)

        d01_binary = (
            *(d01["coefficients"][word] for word in MIXED_WORDS),
            d01["A"] - 1,
            inverse_a * d01["B"] - 1,
        )
        certificates.append(
            exact_projection(
                f"D01_binary_{chart}",
                d01_binary,
                x + (inverse_a,),
                retained,
                None,
            )
        )

        d23_binary = (
            *(d23["coefficients"][word] for word in MIXED_WORDS),
            d23["A"] - 1,
            inverse_a * d23["B"] - 1,
        )
        expected_binary = (
            h[3],
            (q - phi) * h[0] + 1,
            h[1] * h[2] * ((q + 1) * lam + q - 1),
        )
        if chart == "infinity":
            expected_binary = (h[3], (q - phi) * h[0] + 1, h[1] * h[2])
        certificates.append(
            exact_projection(
                f"D23_binary_{chart}",
                d23_binary,
                x + (inverse_a,),
                retained,
                expected_binary,
            )
        )

        shared = (
            *(d01["coefficients"][word] for word in WORDS[:-1]),
            d01["B"] - 1,
            *(d23["coefficients"][word] for word in MIXED_WORDS),
            inverse_a * d23["A"] - 1,
            inverse_b * d23["B"] - 1,
        )
        expected_shared = None
        if chart == "finite":
            expected_shared = (lam - 1, h[3], h[1], (q - phi) * h[0] + 1)
        certificates.append(
            exact_projection(
                f"shared_D01_pure_D23_binary_{chart}",
                shared,
                x + (inverse_a, inverse_b),
                retained,
                expected_shared,
            )
        )
    return certificates


def shared_branch(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
    p: sp.Symbol,
    q: sp.Symbol,
    phi: sp.Symbol,
) -> dict[str, Any]:
    residual = q - phi
    t, cap_c, cap_d = sp.symbols("t C D")
    x = sp.symbols("x0:8")
    marking = (-1 / residual, 0, t, 0)
    beta = mark_beta(alpha, unmarked_beta, marking)
    d01 = contraction_model(alpha, beta, x, "D01", "finite", sp.Integer(1))
    d23 = contraction_model(alpha, beta, x, "D23", "finite", sp.Integer(1))

    combined = sp.Matrix(
        [
            [sp.diff(expression, variable) for variable in x]
            for expression in (
                *(d01["coefficients"][word] for word in WORDS[:-1]),
                *(d23["coefficients"][word] for word in MIXED_WORDS),
            )
        ]
    )
    vector_c = sp.Matrix((0, -1 / p, phi / p, 0, 1, 0, 0, 0))
    vector_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    frame = sp.Matrix.hstack(vector_c, vector_d)
    require(frame.rank() == 2, "shared frame rank")
    require(
        all(sp.factor(entry) == 0 for entry in combined * frame),
        "shared frame is not in the unwanted-coefficient kernel",
    )

    pivot_columns = tuple(combined.rref()[1])
    pivot_rows = tuple(combined.T.rref()[1])
    require(len(pivot_columns) == 6 and len(pivot_rows) == 6, "shared rank is not six")
    rank_witness = sp.factor(combined.extract(pivot_rows, pivot_columns).det())
    require(rank_witness != 0, "shared rank witness vanished")
    require(
        len(pivot_columns) + frame.shape[1] == combined.shape[1],
        "shared frame is not complete",
    )

    extension = cap_c * vector_c + cap_d * vector_d
    substitution = dict(zip(x, extension, strict=True))
    d01_values = {
        word: sp.factor(value.subs(substitution))
        for word, value in d01["coefficients"].items()
    }
    d23_values = {
        word: sp.factor(value.subs(substitution))
        for word, value in d23["coefficients"].items()
    }
    require(
        all(value == 0 for word, value in d01_values.items() if word != BETA_WORD),
        "D01 is not pure on the shared frame",
    )
    require(
        all(
            value == 0
            for word, value in d23_values.items()
            if word not in (ALPHA_WORD, BETA_WORD)
        ),
        "D23 is not binary on the shared frame",
    )
    expected_b01 = 4 * (p * cap_d - phi * t * cap_c)
    expected_a23 = -4 * phi * residual * cap_c / p
    expected_b23 = 4 * cap_c
    require(sp.factor(d01_values[BETA_WORD] - expected_b01) == 0, "D01 diagonal")
    require(sp.factor(d23_values[ALPHA_WORD] - expected_a23) == 0, "D23 alpha diagonal")
    require(sp.factor(d23_values[BETA_WORD] - expected_b23) == 0, "D23 beta diagonal")

    mode_three = one_marked_matrix(d01, 3).subs(substitution)
    fixed_rows = (1, 2, 5, 7)
    fixed_minor = sp.factor(mode_three.extract(fixed_rows, tuple(range(4))).det())
    expected_minor = -64 * cap_c * p * (p * cap_d - phi * t * cap_c) ** 2
    require(sp.factor(fixed_minor - expected_minor) == 0, "fixed rank-four minor")

    return {
        "marking": "h0=-1/(q-phi), h1=0, h2=t, h3=0",
        "weight": "[1:1]",
        "combined_unwanted_matrix_shape": list(combined.shape),
        "combined_unwanted_rank": len(pivot_columns),
        "rank_witness_rows": list(pivot_rows),
        "rank_witness_columns": list(pivot_columns),
        "rank_witness": str(rank_witness),
        "kernel_dimension": 2,
        "kernel_frame": [
            [str(sp.factor(entry)) for entry in vector_c],
            [str(sp.factor(entry)) for entry in vector_d],
        ],
        "D01_pure_diagonal": str(sp.factor(expected_b01)),
        "D23_binary_diagonals": [
            str(sp.factor(expected_a23)),
            str(sp.factor(expected_b23)),
        ],
        "genuine_open": "C*p*phi*(q-phi)*(p*D-phi*t*C)!=0",
        "fixed_mode_three_minor_rows": list(fixed_rows),
        "fixed_mode_three_minor": str(fixed_minor),
        "fixed_minor_nonzero_on_genuine_open": True,
    }


def low_rank_false_lead(
    alpha: tuple[tuple[Any, ...], ...],
    unmarked_beta: tuple[tuple[Any, ...], ...],
    p: sp.Symbol,
    q: sp.Symbol,
    phi: sp.Symbol,
) -> dict[str, Any]:
    residual = q - phi
    marking = (-1 / residual, 0, 0, 0)
    beta = mark_beta(alpha, unmarked_beta, marking)
    rho, sigma = 1 - phi, phi + 1
    d23_extension = (0, 1, 0, 0, 0, 0, 0, 1)
    d01_extension = (phi * residual, 0, 0, phi, 0, 1, 1, 0)
    d23 = homogeneous_model(alpha, beta, d23_extension, "D23", rho, sigma)
    d01 = homogeneous_model(alpha, beta, d01_extension, "D01", rho, sigma)
    d23_support = {
        word: value for word, value in d23["coefficients"].items() if value != 0
    }
    d01_support = {
        word: value for word, value in d01["coefficients"].items() if value != 0
    }
    require(
        d23_support == {ALPHA_WORD: 4 * phi * residual, BETA_WORD: 4 * p},
        "false-lead D23 support",
    )
    require(d01_support == {BETA_WORD: 8 * p}, "false-lead D01 support")
    d23_ranks = [one_marked_matrix(d23, mode).rank() for mode in range(4)]
    d01_ranks = [one_marked_matrix(d01, mode).rank() for mode in range(4)]
    require(d23_ranks == [3, 3, 3, 3], "false-lead D23 ranks")
    require(d01_ranks == [2, 3, 3, 3], "false-lead D01 ranks")

    proportionality_witness = (
        sp.Matrix.hstack(sp.Matrix(d23_extension), sp.Matrix(d01_extension))
        .extract((1, 5), (0, 1))
        .det()
    )
    require(proportionality_witness == 1, "false-lead extensions may be proportional")
    finite_slope = sp.factor(rho / sigma)
    branch_residual = sp.factor(finite_slope - 1)
    require(branch_residual == -2 * phi / (phi + 1), "false-lead slope residual")

    return {
        "marking": "h0=-1/(q-phi), h1=h2=h3=0",
        "weight": "[1-phi:phi+1]",
        "D23_one_marked_ranks": d23_ranks,
        "D01_one_marked_ranks": d01_ranks,
        "D23_extension": list(d23_extension),
        "D01_extension": [str(sp.factor(entry)) for entry in d01_extension],
        "nonproportional_extension_minor_rows": [1, 5],
        "nonproportional_extension_minor": str(proportionality_witness),
        "finite_chart_lambda_minus_one": str(branch_residual),
        "generic_incompatibility": (
            "shared finite compatibility requires lambda=1, while this weight "
            "has lambda-1=-2*phi/(phi+1); phi=0 is outside the generic field, "
            "and phi=-1 is the separately unit projective-infinity chart"
        ),
    }


def replay_dependencies() -> dict[str, Any]:
    p4 = run_json(
        ("uv", "run", "--with", "sympy", "python", P4_SCRIPT.name), timeout=120
    )
    h31 = run_json(
        ("uv", "run", "--with", "sympy", "python", H31_SCRIPT.name), timeout=180
    )
    require(p4.get("status") == "verified", "P4 component replay")
    require(
        p4.get("component") == "common-kernel vertical rank-one triangle",
        "P4 component identity",
    )
    require(p4.get("component_dimension") == 5, "P4 component dimension")
    require(p4.get("generic_pair_profile") == [4, 4, 4, 3, 3, 3], "P4 pair profile")
    require(h31.get("status") == "pass", "H31 replay")
    require(h31.get("generic_marked_H31_fibre_empty") is True, "H31 conclusion")
    require(h31.get("weighted_H22_closed") is False, "H31 theorem overclaimed H22")
    return {
        "P4": {
            "status": p4["status"],
            "component_dimension": p4["component_dimension"],
            "generic_pair_profile": p4["generic_pair_profile"],
        },
        "H31": {
            "status": h31["status"],
            "generic_marked_H31_fibre_empty": h31["generic_marked_H31_fibre_empty"],
            "weighted_H22_closed": h31["weighted_H22_closed"],
        },
    }


def audit_candidate_artifacts(
    projections: list[dict[str, Any]], branch: dict[str, Any]
) -> dict[str, Any]:
    p, q, phi = sp.symbols("p q phi")
    h = sp.symbols("h0:4")
    lam = sp.Symbol("lam")
    parser_locals = {
        "p": p,
        "q": q,
        "phi": phi,
        "lam": lam,
        **{str(symbol): symbol for symbol in h},
    }

    def parse_generators(strings: list[str]) -> list[sp.Expr]:
        return [
            sp.sympify(item.replace("lambda", "lam"), locals=parser_locals)
            for item in strings
        ]

    def same_ideal(
        independent: list[str], claimed: list[str], variables: tuple[sp.Symbol, ...]
    ) -> bool:
        left = parse_generators(independent)
        right = parse_generators(claimed)
        domain = sp.QQ.frac_field(p, q, phi)
        left_basis = sp.groebner(left, *variables, domain=domain)
        right_basis = sp.groebner(right, *variables, domain=domain)
        return all(
            sp.factor(right_basis.reduce(expression)[1]) == 0 for expression in left
        ) and all(
            sp.factor(left_basis.reduce(expression)[1]) == 0 for expression in right
        )

    certificate = json.loads(CANDIDATE_CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate.get("claim_label") == "VERIFIED", "claim not promoted")
    require(
        certificate.get("discovery_claim_label") == "CANDIDATE"
        and certificate.get("independent_verifier_complete") is True,
        "discovery or independent-verification status changed",
    )
    require(
        certificate["normal_form"]["pure_support"] == {"1111": "4*p"},
        "certificate pure support",
    )
    projected = {item["label"]: item["projected_ideal"] for item in projections}
    claimed_cover = certificate["projective_weight_cover"]
    finite_variables = h + (lam,)
    infinity_variables = h
    require(
        same_ideal(
            projected["D01_binary_finite"],
            claimed_cover["D01_binary_finite_projection"],
            finite_variables,
        ),
        "candidate D01 finite",
    )
    require(
        same_ideal(
            projected["D01_binary_infinity"],
            claimed_cover["D01_binary_infinity_projection"],
            infinity_variables,
        ),
        "candidate D01 infinity",
    )
    require(
        same_ideal(
            projected["D23_binary_finite"],
            claimed_cover["D23_binary_finite_projection"],
            finite_variables,
        ),
        "candidate D23 finite",
    )
    require(
        same_ideal(
            projected["D23_binary_infinity"],
            claimed_cover["D23_binary_infinity_projection"],
            infinity_variables,
        ),
        "candidate D23 infinity",
    )
    shared = certificate["shared_compatibility"]
    require(
        same_ideal(
            projected["shared_D01_pure_D23_binary_finite"],
            shared["finite_projection"],
            finite_variables,
        ),
        "candidate shared finite projection",
    )
    require(
        same_ideal(
            projected["shared_D01_pure_D23_binary_infinity"],
            shared["infinity_projection"],
            infinity_variables,
        ),
        "candidate shared infinity projection",
    )
    frame_locals = {
        **parser_locals,
        "C": sp.Symbol("C"),
        "D": sp.Symbol("D"),
        "t": sp.Symbol("t"),
    }
    require(
        all(
            sp.factor(
                sp.sympify(left, locals=frame_locals)
                - sp.sympify(right, locals=frame_locals)
            )
            == 0
            for left_row, right_row in zip(
                branch["kernel_frame"], shared["shared_extension_frame"], strict=True
            )
            for left, right in zip(left_row, right_row, strict=True)
        ),
        "candidate frame",
    )
    require(
        sp.factor(
            sp.sympify(branch["fixed_mode_three_minor"], locals=frame_locals)
            - sp.sympify(shared["fixed_minor"]["determinant"], locals=frame_locals)
        )
        == 0,
        "candidate fixed minor",
    )

    report_text = CANDIDATE_REPORT.read_text(encoding="utf-8")
    scope_markers = {
        "verified_status": "**VERIFIED after a fresh independent no-import replay:**"
        in report_text,
        "generic_only": "generic over the component function field" in report_text,
        "special_boundaries_open": "Special\n  parameter divisors and projective component boundaries remain open"
        in report_text,
        "global_excluded": "global Krenn--Gu claim" in report_text,
    }
    require(all(scope_markers.values()), "candidate report lost a scope boundary")
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
    p, q, phi = sp.symbols("p q phi")
    alpha, beta = component_bases(p, q, phi)
    h = sp.symbols("h0:4")
    unmarked_coefficients = four_source_coefficients(alpha, beta)
    marked_coefficients = four_source_coefficients(alpha, mark_beta(alpha, beta, h))
    for coefficients in (unmarked_coefficients, marked_coefficients):
        require(
            all(
                value == 0 for word, value in coefficients.items() if word != BETA_WORD
            ),
            "four-source restriction has a mixed coefficient",
        )
        require(
            sp.factor(coefficients[BETA_WORD] - 4 * p) == 0,
            "four-source pure coefficient",
        )

    dependencies = replay_dependencies()
    projections = projective_elimination(alpha, beta, p, q, phi)
    branch = shared_branch(alpha, beta, p, q, phi)
    false_lead = low_rank_false_lead(alpha, beta, p, q, phi)
    artifact_audit = audit_candidate_artifacts(projections, branch)

    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": "generic weighted H22 fibre of component nineteen",
        "inputs": {path.name: sha256(path) for path in inputs},
        "method": (
            "fresh subset-DP permanents, direct finite/infinity homogeneous "
            "contractions, exact characteristic-zero Singular projection ideals, "
            "complete symbolic shared kernel, and fixed transverse rank witness"
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
        "component_normal_form_reconstructed": True,
        "pure_support": {"1111": "4*p"},
        "dependency_replays": dependencies,
        "projective_projection_certificates": projections,
        "projective_weight_endpoints_checked": ["[0:1]", "[1:0]"],
        "D01_binary_projection_is_unit_on_P1": True,
        "complete_shared_branch": branch,
        "unshared_low_rank_false_lead": false_lead,
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
