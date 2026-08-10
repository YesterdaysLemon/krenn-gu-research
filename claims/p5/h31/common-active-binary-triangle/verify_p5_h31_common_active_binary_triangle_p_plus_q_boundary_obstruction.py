#!/usr/bin/env python3
"""Verify the whole diagonal-DVR H31 obstruction on component 20's p+q wall."""

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
GENERIC_THEOREM = HERE / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
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
PERMUTATIONS = tuple(itertools.permutations(range(4)))


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


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def add(*vectors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(entries)) for entries in zip(*vectors))


def scale(scalar: sp.Expr, vector: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(scalar * entry) for entry in vector)


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(add(beta[mode], scale(shifts[mode], alpha[mode])) for mode in range(4))


def tensor(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }


def extension_matrices(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    extension = sp.symbols("x0:4") + sp.symbols("y0:4")
    retained = tuple(index for index in range(4) if index != distinguished)
    extended_alpha = tuple(
        tuple(row[index] for index in retained) + (extension[mode],)
        for mode, row in enumerate(alpha)
    )
    extended_beta = tuple(
        tuple(row[index] for index in retained) + (extension[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent(
            tuple(
                extended_beta[mode] if word[mode] else extended_alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    rows = {
        word: [sp.diff(coefficients[word], variable) for variable in extension]
        for word in WORDS
    }
    mixed = sp.Matrix(
        [rows[word] for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    )
    return (
        mixed,
        sp.Matrix([rows[(0, 0, 0, 0)]]),
        sp.Matrix([rows[(1, 1, 1, 1)]]),
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected: list[tuple[sp.Expr, ...] | None] = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        rows.append(
            [
                permanent(
                    tuple(
                        tuple(int(index == coordinate) for index in range(4))
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                )
                for coordinate in range(4)
            ]
        )
    return sp.Matrix(rows)


def marked_extension(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    mode: int,
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    extended_alpha = tuple(
        tuple(row[index] for index in retained) + (extension[j],)
        for j, row in enumerate(alpha)
    )
    extended_beta = tuple(
        tuple(row[index] for index in retained) + (extension[4 + j],)
        for j, row in enumerate(beta)
    )
    return one_marked_map(mode, extended_alpha, extended_beta)


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def assert_zero(matrix: sp.Matrix) -> None:
    assert all(sp.factor(entry) == 0 for entry in matrix)


def complete_kernel_certificate(
    matrix: sp.Matrix, frame: sp.Matrix, expected_rank: int
) -> dict[str, object]:
    assert matrix.rank() == expected_rank
    assert frame.cols == matrix.cols - expected_rank
    assert frame.rank() == frame.cols
    assert_zero(matrix * frame)
    pivot_columns = matrix.rref()[1]
    pivot_rows = matrix.T.rref()[1]
    witness = sp.factor(
        matrix.extract(pivot_rows[:expected_rank], pivot_columns[:expected_rank]).det()
    )
    assert witness != 0
    return {
        "mixed_rank": expected_rank,
        "kernel_dimension": frame.cols,
        "complete_kernel_frame": True,
        "rank_witness_rows": list(pivot_rows[:expected_rank]),
        "rank_witness_columns": list(pivot_columns[:expected_rank]),
        "rank_witness_determinant": str(witness),
    }


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact projection replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(program: str, label: str, timeout: int = 240) -> str:
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (label, completed.returncode, completed.stdout, completed.stderr)
        )
    return completed.stdout


def projection_certificate(
    chart: str,
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
    beta = shifted_basis(alpha, canonical_beta, shifts)
    mixed, diagonal_alpha, diagonal_beta = extension_matrices(
        distinguished, alpha, beta
    )
    extension = sp.Matrix(extension_symbols)
    equations = [
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
    ]
    if open_polynomial is not None:
        equations.append(open_inverse * open_polynomial - 1)
        eliminated = extension_symbols + (inverse, open_inverse)
        parameters = shifts + (a, lam)
        blocks = "(dp(10),dp(4),dp(2))"
    else:
        eliminated = extension_symbols + (inverse,)
        parameters = shifts + (k,)
        blocks = "(dp(9),dp(4),dp(1))"
    variables = eliminated + parameters

    lines = [
        "ring R=0,(" + ",".join(map(str, variables)) + ")," + blocks + ";",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + ";",
        "E=std(E);",
        "ideal JE=reduce(J,E);",
        "ideal EJ=reduce(E,J);",
        "JE=simplify(JE,2);",
        "EJ=simplify(EJ,2);",
        "int same=((size(JE)==0)&&(size(EJ)==0));",
        '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
        "quit;",
    ]
    output = run_singular("\n".join(lines), f"{chart}-d{distinguished}")
    markers = [
        line.strip() for line in output.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, output
    _, same, basis_size = markers[0].split(":")
    assert same == "1", output
    return {
        "chart": chart,
        "distinguished_coordinate": distinguished,
        "projected_ideal": [singular(entry) for entry in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(basis_size),
        "projection_is_closure": True,
    }


def chart_bases(
    chart: str, a: sp.Expr, lam: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    zero, one = sp.Integer(0), sp.Integer(1)
    e = (one, zero, zero, zero)
    cap_a = (zero, one, zero, zero)
    cap_b = (zero, zero, one, zero)
    cap_c = (zero, zero, zero, one)
    ell = add(cap_a, scale(-one, cap_b))
    em = add(cap_a, cap_b)
    s0 = 2 * a + 1
    c = a * (a + 1)
    k0 = add(scale(s0, cap_c), scale(-c, ell))
    alpha = (k0, e, e, em)
    beta0 = add(e, scale(lam, ell)) if chart == "B_full" else ell
    beta = (
        beta0,
        add(scale(a + 1, ell), cap_c),
        add(scale(a, ell), cap_c),
        e,
    )
    return alpha, beta


def pure_orientation_certificate() -> dict[str, object]:
    a, lam = sp.symbols("a lambda")
    results = {}
    for chart, expected in (
        ("B_full", -2 * lam * (2 * a + 1)),
        ("B_drop", -2 * (2 * a + 1)),
    ):
        alpha, beta = chart_bases(chart, a, lam)
        coefficients = tensor(alpha, beta)
        assert_equal(coefficients[(1, 1, 1, 1)], expected)
        assert all(
            value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
        )
        results[chart] = {
            "sole_pure_coefficient": str(coefficients[(1, 1, 1, 1)]),
            "all_other_pure_coefficients_zero": True,
            "open": "lambda*(2*a+1)!=0" if chart == "B_full" else "2*a+1!=0",
        }
    return results


def projection_certificates() -> list[dict[str, object]]:
    a, lam = sp.symbols("a lambda")
    h0, h1, h2, h3 = sp.symbols("h0:4")
    results = []
    for chart in ("B_full", "B_drop"):
        alpha, beta = chart_bases(chart, a, lam)
        open_polynomial = lam * (2 * a + 1) if chart == "B_full" else 2 * a + 1
        if chart == "B_full":
            residual = (
                h0,
                h3,
                a * h1 + (a + 1) * h2,
                (a + 1) * h2**2,
                h1 * h2,
            )
        else:
            residual = (h0, h3, h1 * h2)
        for distinguished in range(4):
            expected = (sp.Integer(1),) if distinguished in (0, 3) else residual
            results.append(
                projection_certificate(
                    chart,
                    distinguished,
                    alpha,
                    beta,
                    expected,
                    open_polynomial,
                )
            )
    return results


def full_residual_certificates() -> list[dict[str, object]]:
    a, lam, parameter, line_parameter = sp.symbols("a lambda T t")
    s0 = 2 * a + 1
    alpha, canonical_beta = chart_bases("B_full", a, lam)
    results = []
    for distinguished, sign in ((1, 1), (2, -1)):
        mixed, diagonal_alpha, diagonal_beta = extension_matrices(
            distinguished, alpha, canonical_beta
        )
        v0 = sp.Matrix((-a - 1, 0, 0, sign / a, lam / a, (a + 1) / a, 1, 0))
        v1 = sp.Matrix((0, -1, -1, 0, 1, 0, 0, 1))
        frame = sp.Matrix.hstack(v0, v1)
        kernel = complete_kernel_certificate(mixed, frame, 6)
        extension = parameter * v0 + v1
        first = sp.factor((diagonal_alpha * extension)[0])
        second = sp.factor((diagonal_beta * extension)[0])
        assert_equal(first, -2 * s0)
        expected_second = sign * -2 * s0 * (parameter * lam + a) / a
        assert_equal(second, expected_second)
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, canonical_beta, mode=3)[
                [0, 4, 5, 7], :
            ].det()
        )
        ratio = sp.factor(sp.cancel(determinant / second))
        assert_equal(ratio, -4 * lam**2 * s0)
        results.append(
            {
                "fibre": "generic doubled-origin support",
                "distinguished_coordinate": distinguished,
                **kernel,
                "all_alpha_diagonal": str(first),
                "all_beta_diagonal": str(second),
                "minor_rows": [0, 4, 5, 7],
                "minor_over_beta_diagonal": str(ratio),
            }
        )

    for center, marking in (
        (sp.Integer(0), (0, line_parameter, 0, 0)),
        (sp.Integer(-1), (0, 0, line_parameter, 0)),
    ):
        specialized_alpha, specialized_canonical = chart_bases("B_full", center, lam)
        specialized_beta = shifted_basis(
            specialized_alpha, specialized_canonical, marking
        )
        center_s0 = 2 * center + 1
        for distinguished in (1, 2):
            mixed, diagonal_alpha, diagonal_beta = extension_matrices(
                distinguished, specialized_alpha, specialized_beta
            )
            nullspace = mixed.nullspace()
            frame = sp.Matrix.hstack(*nullspace)
            kernel = complete_kernel_certificate(mixed, frame, 6)
            assert_equal((diagonal_alpha * nullspace[0])[0], 0)
            assert_equal((diagonal_alpha * nullspace[1])[0], -2 * center_s0)
            extension = parameter * nullspace[0] + nullspace[1]
            second = sp.factor((diagonal_beta * extension)[0])
            determinant = sp.factor(
                marked_extension(
                    distinguished,
                    extension,
                    specialized_alpha,
                    specialized_beta,
                    mode=3,
                )[[0, 4, 5, 7], :].det()
            )
            ratio = sp.factor(sp.cancel(determinant / second))
            assert_equal(ratio, -4 * lam**2 * center_s0)
            results.append(
                {
                    "fibre": f"exceptional marking line a={center}",
                    "distinguished_coordinate": distinguished,
                    **kernel,
                    "minor_rows": [0, 4, 5, 7],
                    "minor_over_beta_diagonal": str(ratio),
                    "generic_denominator_specialization_used": False,
                }
            )
    return results


def drop_residual_certificates() -> list[dict[str, object]]:
    a, lam, line_parameter, parameter = sp.symbols("a lambda t T")
    s0 = 2 * a + 1
    alpha, canonical_beta = chart_bases("B_drop", a, lam)
    sheets = (
        ("S1", (0, 0, line_parameter, 0)),
        ("S2", (0, line_parameter, 0, 0)),
    )
    results = []
    for distinguished in (1, 2):
        sign = 1 if distinguished == 1 else -1
        for sheet, marking in sheets:
            beta = shifted_basis(alpha, canonical_beta, marking)
            mixed, diagonal_alpha, diagonal_beta = extension_matrices(
                distinguished, alpha, beta
            )
            nullspace = mixed.nullspace()
            frame = sp.Matrix.hstack(*nullspace)
            kernel = complete_kernel_certificate(mixed, frame, 6)
            assert_equal((diagonal_alpha * nullspace[0])[0], 0)
            assert_equal((diagonal_alpha * nullspace[1])[0], -2 * s0)
            extension = parameter * nullspace[0] + nullspace[1]
            first = sp.factor((diagonal_alpha * extension)[0])
            second = sp.factor((diagonal_beta * extension)[0])
            assert_equal(first, -2 * s0)
            if sheet == "S1":
                expected_second = (
                    sign * 2 * s0 * (-parameter * a + (a + 1) * line_parameter) / a**2
                )
            else:
                expected_second = sign * -2 * parameter * s0 / a
            assert_equal(second, expected_second)
            determinant = sp.factor(
                marked_extension(distinguished, extension, alpha, beta, mode=3)[
                    [0, 4, 5, 7], :
                ].det()
            )
            ratio = sp.factor(sp.cancel(determinant / second))
            assert_equal(ratio, -4 * s0)
            results.append(
                {
                    "fibre": f"generic {sheet}",
                    "distinguished_coordinate": distinguished,
                    **kernel,
                    "all_alpha_diagonal": str(first),
                    "all_beta_diagonal": str(second),
                    "minor_rows": [0, 4, 5, 7],
                    "minor_over_beta_diagonal": str(ratio),
                }
            )

    for center, disappearing, surviving in (
        (sp.Integer(0), "S1", "S2"),
        (sp.Integer(-1), "S2", "S1"),
    ):
        specialized_alpha, specialized_canonical = chart_bases("B_drop", center, lam)
        center_s0 = 2 * center + 1
        for distinguished in (1, 2):
            for sheet, marking in sheets:
                beta = shifted_basis(specialized_alpha, specialized_canonical, marking)
                mixed, diagonal_alpha, diagonal_beta = extension_matrices(
                    distinguished, specialized_alpha, beta
                )
                nullspace = mixed.nullspace()
                frame = sp.Matrix.hstack(*nullspace)
                if sheet == disappearing:
                    kernel = complete_kernel_certificate(mixed, frame, 6)
                    alpha_values = [
                        sp.factor((diagonal_alpha * vector)[0]) for vector in nullspace
                    ]
                    assert all(value == 0 for value in alpha_values)
                    results.append(
                        {
                            "fibre": f"a={center} {sheet} projection-only sheet",
                            "distinguished_coordinate": distinguished,
                            **kernel,
                            "all_alpha_diagonal_zero_on_complete_kernel": True,
                            "genuine_binary_neighbour_exists": False,
                            "projection_closure_caveat_applied": True,
                        }
                    )
                    continue

                assert sheet == surviving
                kernel = complete_kernel_certificate(mixed, frame, 5)
                alpha_values = [
                    sp.factor((diagonal_alpha * vector)[0]) for vector in nullspace
                ]
                alpha_index = next(
                    index
                    for index, value in enumerate(alpha_values)
                    if sp.factor(value + 2 * center_s0) == 0
                )
                beta_values = [
                    sp.factor((diagonal_beta * vector)[0]) for vector in nullspace
                ]
                beta_index = next(
                    index
                    for index, value in enumerate(beta_values)
                    if value != 0 and index != alpha_index
                )
                extra_index = next(
                    index
                    for index in range(3)
                    if index not in (alpha_index, beta_index)
                )
                extra_parameter = sp.Symbol("S")
                extension = (
                    parameter * nullspace[beta_index]
                    + extra_parameter * nullspace[extra_index]
                    + nullspace[alpha_index]
                )
                first = sp.factor((diagonal_alpha * extension)[0])
                second = sp.factor((diagonal_beta * extension)[0])
                assert_equal(first, -2 * center_s0)
                determinant = sp.factor(
                    marked_extension(
                        distinguished,
                        extension,
                        specialized_alpha,
                        beta,
                        mode=3,
                    )[[0, 4, 5, 7], :].det()
                )
                ratio = sp.factor(sp.cancel(determinant / second))
                assert_equal(ratio, -4 * center_s0)
                assert extra_parameter not in ratio.free_symbols
                results.append(
                    {
                        "fibre": f"a={center} surviving {sheet}",
                        "distinguished_coordinate": distinguished,
                        **kernel,
                        "all_alpha_diagonal": str(first),
                        "minor_rows": [0, 4, 5, 7],
                        "minor_over_beta_diagonal": str(ratio),
                        "ratio_independent_of_extra_kernel_parameter": True,
                        "genuine_binary_open_nonempty": second != 0,
                        "generic_denominator_specialization_used": False,
                    }
                )
    return results


def transverse_certificate() -> dict[str, object]:
    a, lam = sp.symbols("a lambda")
    shifts = sp.symbols("h0:4")
    expected = {
        "B_full": {1: -(a**2) * shifts[0] - lam, 2: a**2 * shifts[0] + lam},
        "B_drop": {1: -(a**2) * shifts[0] - 1, 2: a**2 * shifts[0] + 1},
    }
    results = {}
    for chart in ("B_full", "B_drop"):
        alpha, canonical_beta = chart_bases(chart, a, lam)
        beta = shifted_basis(alpha, canonical_beta, shifts)
        pure = one_marked_map(3, alpha, beta)
        chart_results = {}
        for distinguished in (1, 2):
            entry = sp.factor(pure[5, distinguished])
            assert_equal(entry, expected[chart][distinguished])
            chart_results[str(distinguished)] = {
                "row": "101",
                "entry": str(entry),
                "mod_projected_h0": str(entry.subs(shifts[0], 0)),
                "nonzero_on_chart_open": True,
            }
        results[chart] = chart_results
    return results


def half_replacement_certificate() -> dict[str, object]:
    zero, one = sp.Integer(0), sp.Integer(1)
    e = (one, zero, zero, zero)
    cap_a = (zero, one, zero, zero)
    cap_b = (zero, zero, one, zero)
    cap_c = (zero, zero, zero, one)
    ell = add(cap_a, scale(-one, cap_b))
    em = add(cap_a, cap_b)
    k = sp.Symbol("k")
    alpha = (ell, e, e, em)
    beta = (
        add(cap_c, scale(-k, e)),
        add(scale(sp.Rational(1, 2), ell), cap_c),
        add(scale(-sp.Rational(1, 2), ell), cap_c),
        e,
    )
    coefficients = tensor(alpha, beta)
    assert_equal(coefficients[(1, 1, 1, 1)], sp.Rational(1, 2))
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    projections = [
        projection_certificate(
            "a=-1/2 replacement",
            distinguished,
            alpha,
            beta,
            (sp.Integer(1),),
            open_polynomial=None,
        )
        for distinguished in range(4)
    ]
    return {
        "sole_pure_coefficient": "1/2",
        "k_inverted": False,
        "k=0_included": True,
        "all_four_projected_ideals_unit": True,
        "projection_certificates": projections,
    }


def main() -> None:
    orientations = pure_orientation_certificate()
    projections = projection_certificates()
    full_residuals = full_residual_certificates()
    drop_residuals = drop_residual_certificates()
    transverse = transverse_certificate()
    half = half_replacement_certificate()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "proof_a",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": (
                    "whole diagonal-source-torus DVR p+q=0 marked-H31 wall, "
                    "including its component-14/15 special lower-pair fibres"
                ),
                "inputs": {
                    P4_BOUNDARY.name: sha256(P4_BOUNDARY),
                    GENERIC_THEOREM.name: sha256(GENERIC_THEOREM),
                    EMBEDDED_P3.name: sha256(EMBEDDED_P3),
                    EXCEPTIONAL_LOWER_PAIR.name: sha256(EXCEPTIONAL_LOWER_PAIR),
                    INFINITY_ENDPOINT.name: sha256(INFINITY_ENDPOINT),
                },
                "method": (
                    "exact characteristic-zero permanent expansion, normalized "
                    "incidence elimination, exhaustive fixed-minor strata, and "
                    "complete mixed-kernel reconstruction"
                ),
                "command": (
                    "uv run --with sympy python "
                    "claims/p5/h31/common-active-binary-triangle/"
                    "verify_p5_h31_common_active_binary_triangle_p_plus_q_"
                    "boundary_obstruction.py"
                ),
                "outputs": {THEOREM.name: sha256(THEOREM)},
                "limitations": (
                    "projection closures distinguished from actual fibres; no H22, "
                    "non-diagonal or arbitrary GL4 source changes, older-component "
                    "placement, local-to-global reduction, or global conjecture claim"
                ),
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "pure_orientations": orientations,
                "projection_certificates": projections,
                "B_full_residual_certificates": full_residuals,
                "B_drop_residual_certificates": drop_residuals,
                "pure_transverse_certificates": transverse,
                "a=-1/2_replacement": half,
                "B_full_generic_doubled_origin": True,
                "B_full_exceptional_marking_lines": {
                    "a=0": "h1-line",
                    "a=-1": "h2-line",
                },
                "B_drop_generic_two_marking_lines": True,
                "B_drop_exceptional_projection_sheets_checked_against_actual_kernels": True,
                "all_68_minor_global_ideal_replayed": False,
                "all_68_minor_global_ideal_replay_failure": (
                    "discarded timeout above 150 CPU seconds; contributes no evidence"
                ),
                "complete_uniform_fixed_minor_rank_certificates": True,
                "projection_closure_treated_as_actual_fibre": False,
                "invalid_generic_specializations_used": False,
                "lambda_open_preserved": True,
                "finite_field_computation_used": False,
                "finite_field_inference_used": False,
                "independent_replay_complete_for_displayed_charts": True,
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
