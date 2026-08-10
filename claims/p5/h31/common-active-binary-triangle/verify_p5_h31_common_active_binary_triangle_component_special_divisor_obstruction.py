#!/usr/bin/env python3
"""Verify generic special-divisor H31 exclusion on pure-P4 component twenty."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_SPECIAL_DIVISOR_OBSTRUCTION.md"
)
COMPONENT = REPO_ROOT / 'claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md'
GENERIC_THEOREM = (
    ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
p, q, t, r = sp.symbols("p q t r")
SHIFTS = sp.symbols("h0:4")


@dataclass(frozen=True)
class MarkingStratum:
    label: str
    distinguished: int
    marking: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
    minor_rows: tuple[int, int, int, int] = (0, 1, 4, 7)


@dataclass(frozen=True)
class DivisorCase:
    label: str
    substitution: tuple[tuple[sp.Symbol, sp.Expr], ...]
    projections: tuple[tuple[sp.Expr, ...], ...]
    strata: tuple[MarkingStratum, ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def pure_bases() -> tuple[
    tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]
]:
    one, zero = sp.Integer(1), sp.Integer(0)
    e = (one, zero, zero, zero)
    return (
        ((zero, -p * (p + 1), q * (q - 1), p - q + 1), e, e, (one, one, one, zero)),
        (
            (-p + q - 1, -p - q, p + q, zero),
            (zero, p + 1, q - 1, one),
            (zero, p, q, one),
            e,
        ),
    )


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    marking: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.factor(beta[mode][coordinate] + marking[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def specialize(
    rows: tuple[tuple[sp.Expr, ...], ...],
    substitution: dict[sp.Symbol, sp.Expr],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(sp.factor(entry.subs(substitution)) for entry in row) for row in rows
    )


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact special-fibre replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(program: str, timeout: int = 300) -> str:
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular failure",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return completed.stdout


def ideal_equality_program(
    ring: str,
    equations: tuple[sp.Expr, ...],
    eliminated: tuple[sp.Symbol, ...],
    expected: tuple[sp.Expr, ...],
) -> str:
    return "\n".join(
        (
            ring,
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
            "J=std(J);",
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal JE=reduce(J,E);",
            "ideal EJ=reduce(E,J);",
            "JE=simplify(JE,2);",
            "EJ=simplify(EJ,2);",
            "int same=((size(JE)==0)&&(size(EJ)==0));",
            '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
            "quit;",
        )
    )


def parse_ideal_equality(output: str) -> int:
    markers = [
        line.strip() for line in output.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, output
    _, same, size = markers[0].split(":")
    assert same == "1", output
    return int(size)


def deletion_three_base_support_certificate() -> dict[str, object]:
    alpha, canonical_beta = pure_bases()
    beta = shifted_basis(alpha, canonical_beta, SHIFTS)
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(3, alpha, beta)
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,) + SHIFTS
    expected_factor = sp.factor(
        p * (p + 1) * q * (q - 1) * (q - p) * (q - p - 2) * (2 * p * q - p + q)
    )
    variables = eliminated + (p, q)
    program = ideal_equality_program(
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(13),dp(2));",
        equations,
        eliminated,
        (expected_factor,),
    )
    size = parse_ideal_equality(run_singular(program))
    return {
        "distinguished_coordinate": 3,
        "base_support_factor": str(expected_factor).replace("**", "^"),
        "bidirectional_ideal_equality": True,
        "standard_basis_size": size,
    }


def global_marking_projection_certificates() -> list[dict[str, object]]:
    alpha, canonical_beta = pure_bases()
    beta = shifted_basis(alpha, canonical_beta, SHIFTS)
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    expected = {
        0: (sp.Integer(1),),
        1: (
            SHIFTS[0],
            SHIFTS[3],
            SHIFTS[1] * SHIFTS[2],
            (2 * q - 1) * (q * SHIFTS[1] + (q - 1) * SHIFTS[2] + q * (q - 1)),
        ),
        2: (
            SHIFTS[0],
            SHIFTS[3],
            SHIFTS[1] * SHIFTS[2],
            (2 * p + 1) * (p * SHIFTS[1] + (p + 1) * SHIFTS[2] + p * (p + 1)),
        ),
    }
    certificates = []
    for distinguished in range(3):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
        extension = sp.Matrix(extensions)
        equations = (
            *tuple(mixed * extension),
            (diagonal_alpha * extension)[0] - 1,
            inverse * (diagonal_beta * extension)[0] - 1,
        )
        eliminated = extensions + (inverse,)
        variables = eliminated + SHIFTS + (p, q)
        program = ideal_equality_program(
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(6));",
            equations,
            eliminated,
            expected[distinguished],
        )
        size = parse_ideal_equality(run_singular(program))
        certificates.append(
            {
                "distinguished_coordinate": distinguished,
                "projected_ideal": [
                    str(sp.factor(entry)).replace("**", "^")
                    for entry in expected[distinguished]
                ],
                "bidirectional_ideal_equality": True,
                "standard_basis_size": size,
            }
        )
    return certificates


def projection_certificate(
    case: DivisorCase,
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    canonical_beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, object]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    beta = shifted_basis(alpha, canonical_beta, SHIFTS)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    expected = case.projections[distinguished]
    variables = eliminated + SHIFTS
    program = ideal_equality_program(
        "ring R=(0,t),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        equations,
        eliminated,
        expected,
    )
    size = parse_ideal_equality(run_singular(program))
    return {
        "distinguished_coordinate": distinguished,
        "projected_ideal": [singular(entry) for entry in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": size,
    }


def nonvanishing_minor_certificate(
    case: DivisorCase,
    stratum: MarkingStratum,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    canonical_beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, object]:
    beta = shifted_basis(alpha, canonical_beta, stratum.marking)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
        stratum.distinguished, alpha, beta
    )
    assert mixed.rank() == 6
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    extension = sp.Matrix(extensions)
    neighbouring = marked_extension(stratum.distinguished, extension, alpha, beta, 3)
    determinant = sp.factor(neighbouring[list(stratum.minor_rows), :].det())
    assert determinant != 0
    pure = one_marked_map(3, alpha, beta)
    transverse = next(
        (
            (row, sp.factor(pure[row, stratum.distinguished]))
            for row in range(8)
            if sp.factor(pure[row, stratum.distinguished]) != 0
            and r not in sp.factor(pure[row, stratum.distinguished]).free_symbols
        ),
        None,
    )
    assert transverse is not None

    raw_equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
        determinant,
    )
    # All discarded denominators lie in the coefficient field C(t).  Clearing
    # them also avoids Singular parsing ``z^3/2`` as ``z^(3/2)``.
    equations = tuple(
        sp.together(equation).as_numer_denom()[0] for equation in raw_equations
    )
    variables = (
        extensions + (inverse,) + ((r,) if r in determinant.free_symbols else ())
    )
    program = "\n".join(
        (
            "ring R=(0,t),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=std(I);",
            "poly remainder=reduce(1,I);",
            '"CODEX_RESULT:"+string(remainder==0)+":"+string(size(I));',
            "quit;",
        )
    )
    output = run_singular(program)
    markers = [
        line.strip() for line in output.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, output
    _, unit, size = markers[0].split(":")
    assert unit == "1", output
    return {
        "label": stratum.label,
        "distinguished_coordinate": stratum.distinguished,
        "marking": [str(entry) for entry in stratum.marking],
        "marking_line_uniform": r in stratum.marking,
        "mixed_rank": 6,
        "marked_mode": 3,
        "minor_rows": list(stratum.minor_rows),
        "binary_open_plus_minor_zero_is_empty": True,
        "standard_basis_size": int(size),
        "pure_transverse_entry": {
            "row": transverse[0],
            "column": stratum.distinguished,
            "value": str(transverse[1]),
        },
        "global_third_row_forced_zero": True,
    }


def generic_projection(
    p_value: sp.Expr, q_value: sp.Expr
) -> tuple[tuple[sp.Expr, ...], ...]:
    return (
        (sp.Integer(1),),
        (
            SHIFTS[3],
            q_value * SHIFTS[1] + (q_value - 1) * SHIFTS[2] + q_value * (q_value - 1),
            SHIFTS[0],
            SHIFTS[2] ** 2 + q_value * SHIFTS[2],
        ),
        (
            SHIFTS[3],
            p_value * SHIFTS[1] + (p_value + 1) * SHIFTS[2] + p_value * (p_value + 1),
            SHIFTS[0],
            SHIFTS[2] ** 2 + p_value * SHIFTS[2],
        ),
        (sp.Integer(1),),
    )


def generic_strata(p_value: sp.Expr, q_value: sp.Expr) -> tuple[MarkingStratum, ...]:
    return (
        MarkingStratum("C1", 1, (0, 1 - q_value, 0, 0)),
        MarkingStratum("C2", 1, (0, 0, -q_value, 0)),
        MarkingStratum("C3", 2, (0, -p_value - 1, 0, 0)),
        MarkingStratum("C4", 2, (0, 0, -p_value, 0)),
    )


def divisor_cases() -> tuple[DivisorCase, ...]:
    h0, h1, h2, h3 = SHIFTS
    cases: list[DivisorCase] = []

    for label, p_value, q_value, special_marking, rows in (
        ("q=p", t, t, (0, 0, t, 0), (0, 1, 4, 7)),
        ("q=p+2", t, t + 2, (0, t + 1, 0, 0), (0, 2, 4, 7)),
        (
            "2pq-p+q=0",
            t,
            t / (2 * t + 1),
            (0, 0, 0, 0),
            (0, 1, 4, 7),
        ),
    ):
        projections = list(generic_projection(p_value, q_value))
        if label == "q=p":
            projections[3] = (h3, h2 - t, h1, h0)
        elif label == "q=p+2":
            projections[3] = (h3, h2, h1 - t - 1, h0)
        else:
            projections[3] = (h3, h1 - h2, h0, h2**2)
        cases.append(
            DivisorCase(
                label,
                ((p, p_value), (q, q_value)),
                tuple(projections),
                generic_strata(p_value, q_value)
                + (MarkingStratum("D3", 3, special_marking, rows),),
            )
        )

    p_zero_projection = list(generic_projection(0, t))
    p_zero_projection[2] = (h3, h2, h0)
    p_zero_projection[3] = (h3, h2, h1 - t + 1, h0)
    cases.append(
        DivisorCase(
            "p=0",
            ((p, sp.Integer(0)), (q, t)),
            tuple(p_zero_projection),
            (
                MarkingStratum("C1", 1, (0, 1 - t, 0, 0), (0, 2, 4, 7)),
                MarkingStratum("C2", 1, (0, 0, -t, 0), (0, 2, 4, 7)),
                MarkingStratum("D2-line", 2, (0, r, 0, 0), (0, 2, 4, 7)),
                MarkingStratum("D3", 3, (0, t - 1, 0, 0), (0, 2, 4, 7)),
            ),
        )
    )

    p_minus_one_projection = list(generic_projection(-1, t))
    p_minus_one_projection[2] = (h3, h1, h0)
    p_minus_one_projection[3] = (h3, h2 - t, h1, h0)
    cases.append(
        DivisorCase(
            "p=-1",
            ((p, sp.Integer(-1)), (q, t)),
            tuple(p_minus_one_projection),
            (
                MarkingStratum("C1", 1, (0, 1 - t, 0, 0)),
                MarkingStratum("C2", 1, (0, 0, -t, 0)),
                MarkingStratum("D2-line", 2, (0, 0, r, 0)),
                MarkingStratum("D3", 3, (0, 0, t, 0)),
            ),
        )
    )

    q_zero_projection = list(generic_projection(t, 0))
    q_zero_projection[1] = (h3, h2, h0)
    q_zero_projection[3] = (h3, h2, h1 - t - 1, h0)
    cases.append(
        DivisorCase(
            "q=0",
            ((p, t), (q, sp.Integer(0))),
            tuple(q_zero_projection),
            (
                MarkingStratum("D1-line", 1, (0, r, 0, 0), (0, 2, 4, 7)),
                MarkingStratum("C3", 2, (0, -t - 1, 0, 0), (0, 2, 4, 7)),
                MarkingStratum("C4", 2, (0, 0, -t, 0), (0, 2, 4, 7)),
                MarkingStratum("D3", 3, (0, t + 1, 0, 0), (0, 2, 4, 7)),
            ),
        )
    )

    q_one_projection = list(generic_projection(t, 1))
    q_one_projection[1] = (h3, h1, h0)
    q_one_projection[3] = (h3, h2 - t, h1, h0)
    cases.append(
        DivisorCase(
            "q=1",
            ((p, t), (q, sp.Integer(1))),
            tuple(q_one_projection),
            (
                MarkingStratum("D1-line", 1, (0, 0, r, 0)),
                MarkingStratum("C3", 2, (0, -t - 1, 0, 0)),
                MarkingStratum("C4", 2, (0, 0, -t, 0)),
                MarkingStratum("D3", 3, (0, 0, t, 0)),
            ),
        )
    )

    q_half_projection = list(generic_projection(t, sp.Rational(1, 2)))
    q_half_projection[1] = (h3, h0, h1 * h2)
    cases.append(
        DivisorCase(
            "q=1/2",
            ((p, t), (q, sp.Rational(1, 2))),
            tuple(q_half_projection),
            (
                MarkingStratum("D1-h2-axis", 1, (0, r, 0, 0)),
                MarkingStratum("D1-h1-axis", 1, (0, 0, r, 0)),
                MarkingStratum("C3", 2, (0, -t - 1, 0, 0)),
                MarkingStratum("C4", 2, (0, 0, -t, 0)),
            ),
        )
    )

    p_minus_half_projection = list(generic_projection(sp.Rational(-1, 2), t))
    p_minus_half_projection[2] = (h3, h0, h1 * h2)
    cases.append(
        DivisorCase(
            "p=-1/2",
            ((p, sp.Rational(-1, 2)), (q, t)),
            tuple(p_minus_half_projection),
            (
                MarkingStratum("C1", 1, (0, 1 - t, 0, 0)),
                MarkingStratum("C2", 1, (0, 0, -t, 0)),
                MarkingStratum("D2-h2-axis", 2, (0, r, 0, 0)),
                MarkingStratum("D2-h1-axis", 2, (0, 0, r, 0)),
            ),
        )
    )
    return tuple(cases)


def verify_case(case: DivisorCase) -> dict[str, object]:
    substitution = dict(case.substitution)
    universal_alpha, universal_beta = pure_bases()
    alpha = specialize(universal_alpha, substitution)
    canonical_beta = specialize(universal_beta, substitution)
    assert all(
        sp.Matrix((alpha[mode], canonical_beta[mode])).rank() == 2 for mode in range(4)
    )
    tensor = {
        word: sp.factor(
            permanent(
                tuple(
                    canonical_beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    expected_pure = sp.factor(2 * (p + q) * (p - q + 1)).subs(substitution)
    assert sp.factor(tensor[(1, 1, 1, 1)] - expected_pure) == 0
    assert expected_pure != 0
    assert all(value == 0 for word, value in tensor.items() if word != (1, 1, 1, 1))
    projections = [
        projection_certificate(case, distinguished, alpha, canonical_beta)
        for distinguished in range(4)
    ]
    residuals = [
        nonvanishing_minor_certificate(case, stratum, alpha, canonical_beta)
        for stratum in case.strata
    ]
    return {
        "label": case.label,
        "field": "C(t)",
        "substitution": {str(key): str(value) for key, value in case.substitution},
        "pure_support_1111": str(sp.factor(expected_pure)),
        "projection_certificates": projections,
        "marking_strata": residuals,
        "generic_point_of_divisor_H31_fibre_empty": True,
    }


def main() -> None:
    base_support = deletion_three_base_support_certificate()
    global_projections = global_marking_projection_certificates()
    cases = [verify_case(case) for case in divisor_cases()]
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "generic_theorem": GENERIC_THEOREM.name,
                "generic_theorem_sha256": sha256(GENERIC_THEOREM),
                "global_marking_projections_d0_d2": global_projections,
                "deletion_three_base_support": base_support,
                "special_divisors": cases,
                "special_divisor_generic_points_closed": True,
                "divisor_intersections_closed": False,
                "source_torus_or_projective_boundaries_closed": False,
                "weighted_H22_closed": False,
                "global_Krenn_Gu_conjecture_resolved": False,
                "finite_field_inference_used": False,
                "broad_search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
