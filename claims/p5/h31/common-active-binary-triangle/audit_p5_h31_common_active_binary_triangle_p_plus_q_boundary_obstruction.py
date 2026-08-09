#!/usr/bin/env python3
"""Independent exact audit of the p+q boundary marked-H31 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"
P4_BOUNDARY = REPO_ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
EMBEDDED_P3 = (
    REPO_ROOT / "claims" / "p5" / "h31" / "embedded-p3"
    / "P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md"
)
EXCEPTIONAL_LOWER_PAIR = (
    HERE / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md"
)
INFINITY_ENDPOINT = (
    HERE / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def perm4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            rows[0][permutation[0]]
            * rows[1][permutation[1]]
            * rows[2][permutation[2]]
            * rows[3][permutation[3]]
            for permutation in PERMUTATIONS_4
        )
    )


def perm3(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            rows[0][permutation[0]] * rows[1][permutation[1]] * rows[2][permutation[2]]
            for permutation in PERMUTATIONS_3
        )
    )


def vector_sum(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(entries)) for entries in zip(*vectors))


def multiple(scalar: sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def bases(
    chart: str, a: sp.Expr, lam: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    e = (sp.Integer(1), 0, 0, 0)
    cap_a = (0, sp.Integer(1), 0, 0)
    cap_b = (0, 0, sp.Integer(1), 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    ell = vector_sum(cap_a, multiple(-1, cap_b))
    em = vector_sum(cap_a, cap_b)
    k0 = vector_sum(multiple(2 * a + 1, cap_c), multiple(-a * (a + 1), ell))
    alpha = (k0, e, e, em)
    beta = (
        vector_sum(e, multiple(lam, ell)) if chart == "B_full" else ell,
        vector_sum(multiple(a + 1, ell), cap_c),
        vector_sum(multiple(a, ell), cap_c),
        e,
    )
    return alpha, beta


def shifted(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    marking: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(vector_sum(beta[i], multiple(marking[i], alpha[i])) for i in range(4))


def incidence_rows(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    retained = tuple(index for index in range(4) if index != distinguished)
    rows = []
    for word in WORDS:
        row = [sp.Integer(0)] * 8
        for mode in range(4):
            cofactor_rows = tuple(
                tuple(
                    (beta[other] if word[other] else alpha[other])[coordinate]
                    for coordinate in retained
                )
                for other in range(4)
                if other != mode
            )
            column = mode + (4 if word[mode] else 0)
            row[column] = perm3(cofactor_rows)
        rows.append(row)
    return sp.Matrix(rows[1:15]), sp.Matrix([rows[0]]), sp.Matrix([rows[15]])


def one_marked(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    result = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        result.append([])
        for coordinate in range(4):
            rows = tuple(
                tuple(int(index == coordinate) for index in range(4))
                if other == mode
                else selected[other]
                for other in range(4)
            )
            result[-1].append(perm4(rows))
    return sp.Matrix(result)


def extended_one_marked(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    extended_alpha = tuple(
        tuple(row[index] for index in retained) + (extension[mode],)
        for mode, row in enumerate(alpha)
    )
    extended_beta = tuple(
        tuple(row[index] for index in retained) + (extension[4 + mode],)
        for mode, row in enumerate(beta)
    )
    return one_marked(3, extended_alpha, extended_beta)


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact audit replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def projected_ideal(
    label: str,
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    canonical_beta: tuple[tuple[sp.Expr, ...], ...],
    expected: tuple[sp.Expr, ...],
    open_polynomial: sp.Expr | None,
) -> dict[str, object]:
    shifts = sp.symbols("h0:4")
    extension_symbols = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    open_inverse = sp.Symbol("u")
    a, lam, k = sp.symbols("a lambda k")
    beta = shifted(alpha, canonical_beta, shifts)
    mixed, diagonal_alpha, diagonal_beta = incidence_rows(distinguished, alpha, beta)
    extension = sp.Matrix(extension_symbols)
    equations = [
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
    ]
    if open_polynomial is None:
        eliminated = extension_symbols + (inverse,)
        parameters = shifts + (k,)
        blocks = "(dp(9),dp(4),dp(1))"
    else:
        equations.append(open_inverse * open_polynomial - 1)
        eliminated = extension_symbols + (inverse, open_inverse)
        parameters = shifts + (a, lam)
        blocks = "(dp(10),dp(4),dp(2))"
    variables = eliminated + parameters
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + ")," + blocks + ";",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            "int same=((size(JE)==0)&&(size(EJ)==0));",
            '"CODEX_AUDIT:"+string(same)+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
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
            (
                label,
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_AUDIT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "chart": label,
        "distinguished_coordinate": distinguished,
        "expected_ideal": [singular(entry) for entry in expected],
        "bidirectional_exact_equality": True,
        "standard_basis_size": int(size),
    }


def orientation_audit() -> dict[str, object]:
    a, lam = sp.symbols("a lambda")
    results = {}
    for chart, expected in (
        ("B_full", -2 * lam * (2 * a + 1)),
        ("B_drop", -2 * (2 * a + 1)),
    ):
        alpha, beta = bases(chart, a, lam)
        coefficients = {
            word: sp.factor(
                perm4(
                    tuple(
                        beta[mode] if word[mode] else alpha[mode] for mode in range(4)
                    )
                )
            )
            for word in WORDS
        }
        assert_equal(coefficients[(1, 1, 1, 1)], expected)
        assert all(
            value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
        )
        results[chart] = str(coefficients[(1, 1, 1, 1)])
    return results


def projection_audit() -> list[dict[str, object]]:
    a, lam = sp.symbols("a lambda")
    h0, h1, h2, h3 = sp.symbols("h0:4")
    results = []
    for chart in ("B_full", "B_drop"):
        alpha, beta = bases(chart, a, lam)
        residual = (
            (
                h0,
                h3,
                a * h1 + (a + 1) * h2,
                (a + 1) * h2**2,
                h1 * h2,
            )
            if chart == "B_full"
            else (h0, h3, h1 * h2)
        )
        open_polynomial = lam * (2 * a + 1) if chart == "B_full" else 2 * a + 1
        for distinguished in range(4):
            expected = (sp.Integer(1),) if distinguished in (0, 3) else residual
            results.append(
                projected_ideal(
                    chart,
                    distinguished,
                    alpha,
                    beta,
                    expected,
                    open_polynomial,
                )
            )
    return results


def fixed_minor_audit() -> list[dict[str, object]]:
    a, lam, t, parameter = sp.symbols("a lambda t T")
    results = []
    for chart in ("B_full", "B_drop"):
        alpha, canonical = bases(chart, a, lam)
        markings = (
            (("origin", (0, 0, 0, 0)),)
            if chart == "B_full"
            else (
                ("S1", (0, 0, t, 0)),
                ("S2", (0, t, 0, 0)),
            )
        )
        for label, marking in markings:
            beta = shifted(alpha, canonical, marking)
            for distinguished in (1, 2):
                mixed, diagonal_alpha, diagonal_beta = incidence_rows(
                    distinguished, alpha, beta
                )
                nullspace = mixed.nullspace()
                assert mixed.rank() == 6 and len(nullspace) == 2
                assert all(
                    sp.factor(entry) == 0
                    for entry in mixed * sp.Matrix.hstack(*nullspace)
                )
                assert_equal((diagonal_alpha * nullspace[0])[0], 0)
                assert_equal((diagonal_alpha * nullspace[1])[0], -2 * (2 * a + 1))
                extension = parameter * nullspace[0] + nullspace[1]
                second = sp.factor((diagonal_beta * extension)[0])
                determinant = sp.factor(
                    extended_one_marked(distinguished, extension, alpha, beta)[
                        [0, 4, 5, 7], :
                    ].det()
                )
                ratio = sp.factor(sp.cancel(determinant / second))
                expected = (
                    -4 * lam**2 * (2 * a + 1) if chart == "B_full" else -4 * (2 * a + 1)
                )
                assert_equal(ratio, expected)
                results.append(
                    {
                        "chart": chart,
                        "stratum": label,
                        "distinguished_coordinate": distinguished,
                        "mixed_rank": 6,
                        "kernel_dimension": 2,
                        "minor_rows": [0, 4, 5, 7],
                        "minor_over_beta_diagonal": str(ratio),
                    }
                )
    return results


def exceptional_audit() -> list[dict[str, object]]:
    lam, t, parameter, extra = sp.symbols("lambda t T S")
    results = []
    for chart in ("B_full", "B_drop"):
        for center in (sp.Integer(0), sp.Integer(-1)):
            alpha, canonical = bases(chart, center, lam)
            if chart == "B_full":
                sheets = (
                    (("line", (0, t, 0, 0)),)
                    if center == 0
                    else (("line", (0, 0, t, 0)),)
                )
            else:
                sheets = (("S1", (0, 0, t, 0)), ("S2", (0, t, 0, 0)))
            for sheet, marking in sheets:
                beta = shifted(alpha, canonical, marking)
                for distinguished in (1, 2):
                    mixed, diagonal_alpha, diagonal_beta = incidence_rows(
                        distinguished, alpha, beta
                    )
                    nullspace = mixed.nullspace()
                    frame = sp.Matrix.hstack(*nullspace)
                    assert all(sp.factor(entry) == 0 for entry in mixed * frame)
                    alpha_values = [
                        sp.factor((diagonal_alpha * vector)[0]) for vector in nullspace
                    ]
                    if chart == "B_drop" and (
                        (center == 0 and sheet == "S1")
                        or (center == -1 and sheet == "S2")
                    ):
                        assert mixed.rank() == 6 and len(nullspace) == 2
                        assert all(value == 0 for value in alpha_values)
                        results.append(
                            {
                                "chart": chart,
                                "center": str(center),
                                "sheet": sheet,
                                "distinguished_coordinate": distinguished,
                                "mixed_rank": 6,
                                "all_alpha_diagonal_zero": True,
                                "projection_only": True,
                            }
                        )
                        continue

                    expected_rank = 6 if chart == "B_full" else 5
                    assert mixed.rank() == expected_rank
                    assert len(nullspace) == 8 - expected_rank
                    s0 = 2 * center + 1
                    alpha_index = next(
                        index
                        for index, value in enumerate(alpha_values)
                        if sp.factor(value + 2 * s0) == 0
                    )
                    beta_values = [
                        sp.factor((diagonal_beta * vector)[0]) for vector in nullspace
                    ]
                    beta_index = next(
                        index
                        for index, value in enumerate(beta_values)
                        if value != 0 and index != alpha_index
                    )
                    extension = (
                        parameter * nullspace[beta_index] + nullspace[alpha_index]
                    )
                    if len(nullspace) == 3:
                        extra_index = next(
                            index
                            for index in range(3)
                            if index not in (alpha_index, beta_index)
                        )
                        extension += extra * nullspace[extra_index]
                    second = sp.factor((diagonal_beta * extension)[0])
                    determinant = sp.factor(
                        extended_one_marked(distinguished, extension, alpha, beta)[
                            [0, 4, 5, 7], :
                        ].det()
                    )
                    ratio = sp.factor(sp.cancel(determinant / second))
                    expected = -4 * (lam**2 if chart == "B_full" else 1) * s0
                    assert_equal(ratio, expected)
                    assert extra not in ratio.free_symbols
                    results.append(
                        {
                            "chart": chart,
                            "center": str(center),
                            "sheet": sheet,
                            "distinguished_coordinate": distinguished,
                            "mixed_rank": expected_rank,
                            "kernel_dimension": len(nullspace),
                            "minor_over_beta_diagonal": str(ratio),
                            "extra_kernel_parameter_absent_from_ratio": True,
                        }
                    )
    return results


def transverse_audit() -> dict[str, object]:
    a, lam = sp.symbols("a lambda")
    shifts = sp.symbols("h0:4")
    expected = {
        "B_full": (-(a**2) * shifts[0] - lam, a**2 * shifts[0] + lam),
        "B_drop": (-(a**2) * shifts[0] - 1, a**2 * shifts[0] + 1),
    }
    results = {}
    for chart in ("B_full", "B_drop"):
        alpha, canonical = bases(chart, a, lam)
        pure = one_marked(3, alpha, shifted(alpha, canonical, shifts))
        entries = tuple(sp.factor(pure[5, distinguished]) for distinguished in (1, 2))
        for actual, wanted in zip(entries, expected[chart]):
            assert_equal(actual, wanted)
        results[chart] = {
            "entries": [str(entry) for entry in entries],
            "mod_h0": [str(entry.subs(shifts[0], 0)) for entry in entries],
        }
    return results


def half_audit() -> dict[str, object]:
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, sp.Integer(1), -1, 0)
    em = (0, sp.Integer(1), 1, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    k = sp.Symbol("k")
    alpha = (ell, e, e, em)
    beta = (
        vector_sum(cap_c, multiple(-k, e)),
        vector_sum(multiple(sp.Rational(1, 2), ell), cap_c),
        vector_sum(multiple(-sp.Rational(1, 2), ell), cap_c),
        e,
    )
    coefficients = {
        word: sp.factor(
            perm4(tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4)))
        )
        for word in WORDS
    }
    assert_equal(coefficients[(1, 1, 1, 1)], sp.Rational(1, 2))
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    projections = [
        projected_ideal(
            "a=-1/2 replacement",
            distinguished,
            alpha,
            beta,
            (sp.Integer(1),),
            None,
        )
        for distinguished in range(4)
    ]
    return {
        "sole_pure_coefficient": "1/2",
        "k_inverted": False,
        "all_four_projected_ideals_unit": True,
        "projections": projections,
    }


def main() -> None:
    orientations = orientation_audit()
    projections = projection_audit()
    fixed_minors = fixed_minor_audit()
    exceptional = exceptional_audit()
    transverse = transverse_audit()
    half = half_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "verifier",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": (
                    "independent exact audit of the whole diagonal-DVR p+q "
                    "boundary marked-H31 obstruction and dependency boundary"
                ),
                "inputs": {
                    THEOREM.name: sha256(THEOREM),
                    P4_BOUNDARY.name: sha256(P4_BOUNDARY),
                    EMBEDDED_P3.name: sha256(EMBEDDED_P3),
                    EXCEPTIONAL_LOWER_PAIR.name: sha256(EXCEPTIONAL_LOWER_PAIR),
                    INFINITY_ENDPOINT.name: sha256(INFINITY_ENDPOINT),
                },
                "method": (
                    "independent cofactor incidence construction, exact Singular "
                    "projection, and direct generic/exceptional kernel replay"
                ),
                "command": (
                    "uv run --with sympy python "
                    "claims/p5/h31/common-active-binary-triangle/"
                    "audit_p5_h31_common_active_binary_triangle_p_plus_q_"
                    "boundary_obstruction.py"
                ),
                "outputs": {},
                "limitations": (
                    "timed-out 68-minor global ideal not used; dependency hashes "
                    "refer to separately audited special fibres; no H22, non-diagonal "
                    "or arbitrary GL4 source changes, local-to-global, or global claim"
                ),
                "pure_orientations": orientations,
                "projection_certificates": projections,
                "generic_fixed_minor_certificates": fixed_minors,
                "exceptional_kernel_certificates": exceptional,
                "pure_transverse_certificates": transverse,
                "a=-1/2_replacement": half,
                "primary_module_imported": False,
                "all_68_minor_global_ideal_replayed": False,
                "fixed_minor_strata_exhaustive_after_projection_caveat": True,
                "projection_closure_treated_as_actual_fibre": False,
                "invalid_generic_specializations_used": False,
                "lambda_open_preserved": True,
                "finite_field_computation_used": False,
                "finite_field_inference_used": False,
                "H31_displayed_chart_claim_verified": True,
                "H31_whole_diagonal_DVR_boundary_verified": True,
                "remaining_lower_pair_H31_gaps": [],
                "fresh_independent_verifier_complete": True,
                "H22_closed": False,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
