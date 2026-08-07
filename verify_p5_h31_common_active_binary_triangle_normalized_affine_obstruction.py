#!/usr/bin/env python3
"""Verify the full finite normalized component-20 marked-H31 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import time
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_NORMALIZED_AFFINE_OBSTRUCTION.md"
COMPONENT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
GENERIC_THEOREM = (
    ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

p, q = sp.symbols("p q")
SHIFTS = sp.symbols("h0:4")
EXTENSIONS = sp.symbols("x0:4") + sp.symbols("y0:4")
w, u = sp.symbols("w u")


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
    s = p - q + 1
    e = (one, zero, zero, zero)
    alpha = (
        (zero, -p * (p + 1), q * (q - 1), s),
        e,
        e,
        (one, one, one, zero),
    )
    beta = (
        (-s, -p - q, p + q, zero),
        (zero, p + 1, q - 1, one),
        (zero, p, q, one),
        e,
    )
    return alpha, beta


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + SHIFTS[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def extension_coefficients(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[tuple[int, ...], sp.Expr]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_extended = tuple(
        tuple(alpha[mode][index] for index in retained) + (EXTENSIONS[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][index] for index in retained) + (EXTENSIONS[4 + mode],)
        for mode in range(4)
    )
    return {
        word: permanent(
            tuple(
                beta_extended[mode] if word[mode] else alpha_extended[mode]
                for mode in range(4)
            )
        )
        for word in WORDS4
    }


def mixed_matrix(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    coefficients = extension_coefficients(distinguished, alpha, beta)
    rows = {
        word: [sp.diff(coefficients[word], variable) for variable in EXTENSIONS]
        for word in WORDS4
    }
    mixed = sp.Matrix(
        [rows[word] for word in WORDS4 if word not in ((0, 0, 0, 0), (1, 1, 1, 1))]
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
    for bits in WORDS3:
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
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_extended = tuple(
        tuple(alpha[mode][index] for index in retained) + (EXTENSIONS[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][index] for index in retained) + (EXTENSIONS[4 + mode],)
        for mode in range(4)
    )
    return one_marked_map(3, alpha_extended, beta_extended)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact normalized-sheet replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def expected_projection_generators(distinguished: int) -> tuple[sp.Expr, ...]:
    h0, h1, h2, h3 = SHIFTS
    if distinguished == 0:
        return (sp.Integer(1),)
    if distinguished == 1:
        return (
            h3,
            h0,
            h1 * h2,
            (2 * q - 1) * (q * h1 + (q - 1) * h2 + q * (q - 1)),
            h2 * (h2 + q) * (q - 1) * (2 * q - 1),
        )
    if distinguished == 2:
        return (
            h3,
            h0,
            h1 * h2,
            (2 * p + 1) * (p * h1 + (p + 1) * h2 + p * (p + 1)),
            h2 * (h2 + p) * (p + 1) * (2 * p + 1),
        )
    raise ValueError("deletion three is specified by its primary decomposition")


def expected_primary_components(
    distinguished: int,
) -> tuple[tuple[sp.Expr, ...], ...]:
    h0, h1, h2, h3 = SHIFTS
    if distinguished == 1:
        return (
            (h0, h3, h2, h1 + q - 1),
            (h0, h3, h2, q),
            (h0, h3, h2, 2 * q - 1),
            (h0, h3, h1, 2 * q - 1),
            (h0, h3, h1, h2 + q),
            (h0, h3, h1, q - 1),
        )
    if distinguished == 2:
        return (
            (h0, h3, h2, h1 + p + 1),
            (h0, h3, h2, p),
            (h0, h3, h2, 2 * p + 1),
            (h0, h3, h1, 2 * p + 1),
            (h0, h3, h1, h2 + p),
            (h0, h3, h1, p + 1),
        )
    if distinguished == 3:
        return (
            (q, h2, h1 - p - 1, h0, h3),
            (q - 1, h2 - p, h1, h0, h3),
            (p - q, h2 - q, h1, h0, h3),
            (p - q + 2, h2, h1 - q + 1, h0, h3),
            (2 * p * q - p + q, h2**2, h1 - h2, h0, h3),
            (p, h2, h1 - q + 1, h0, h3),
            (p + 1, h2 - q, h1, h0, h3),
        )
    raise ValueError(distinguished)


def expected_radical_components(
    distinguished: int,
) -> tuple[tuple[sp.Expr, ...], ...]:
    primary = list(expected_primary_components(distinguished))
    if distinguished == 3:
        h0, h1, h2, h3 = SHIFTS
        primary[4] = (2 * p * q - p + q, h2, h1, h0, h3)
    return tuple(primary)


def ideal_definition(name: str, generators: tuple[sp.Expr, ...]) -> str:
    return "ideal " + name + "=" + ",".join(map(singular, generators)) + ";"


def component_program_lines(
    distinguished: int,
) -> tuple[list[str], int, bool]:
    primary = expected_primary_components(distinguished)
    radical = expected_radical_components(distinguished)
    lines = []
    for index, generators in enumerate(primary, start=1):
        lines.append(ideal_definition(f"Q{index}", generators))
    for index, generators in enumerate(radical, start=1):
        lines.append(ideal_definition(f"R{index}", generators))
    expected_names = ",".join(f"Q{index}" for index in range(1, len(primary) + 1))
    radical_names = ",".join(f"R{index}" for index in range(1, len(radical) + 1))
    lines.extend(
        (
            f"list ExpectedQ={expected_names};",
            f"list ExpectedR={radical_names};",
            "ideal E=Q1;",
            "ideal ER=R1;",
        )
    )
    for index in range(2, len(primary) + 1):
        lines.extend(
            (
                f"E=intersect(E,Q{index});",
                f"ER=intersect(ER,R{index});",
            )
        )
    lines.extend(
        (
            "E=std(E);",
            "ER=std(ER);",
            "list MA=minAssGTZ(J);",
            "ideal MR=MA[1];",
            "for(int i=2;i<=size(MA);i++){MR=intersect(MR,MA[i]);}",
            "MR=std(MR);",
            "list PD=primdecGTZ(J);",
            "ideal MP=PD[1][1];",
            "for(int j=2;j<=size(PD);j++){MP=intersect(MP,PD[j][1]);}",
            "MP=std(MP);",
            "int component_pairs_match=1;",
            "for(int qi=1;qi<=size(ExpectedQ);qi++)",
            "{",
            "  int pair_found=0;",
            "  for(int pj=1;pj<=size(PD);pj++)",
            "  {",
            "    if(sameIdeal(ExpectedQ[qi],PD[pj][1])",
            "       &&sameIdeal(ExpectedR[qi],PD[pj][2]))",
            "    { pair_found=1; }",
            "  }",
            "  component_pairs_match=component_pairs_match&&pair_found;",
            "}",
            "int expected_equal=sameIdeal(J,E);",
            "int primary_match=sameIdeal(MP,E);",
            "int radical_match=sameIdeal(MR,ER);",
            "int j_radical=sameIdeal(J,ER);",
        )
    )
    return lines, len(primary), distinguished != 3


def exact_certificate(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    pure_map: sp.Matrix,
) -> dict[str, object]:
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
    neighbouring = marked_extension(distinguished, alpha, beta)
    extension = sp.Matrix(EXTENSIONS)
    normalized_open = (p + q) * (p - q + 1)
    equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        w * (diagonal_beta * extension)[0] - 1,
        u * normalized_open - 1,
    )
    variables = EXTENSIONS + (w, u) + SHIFTS + (p, q)
    rows = [neighbouring[row, column] for row in range(8) for column in range(4)]
    transverse = tuple(pure_map[:, distinguished])
    fixed_transverse = (
        (pure_map[7, 0],)
        if distinguished == 0
        else (pure_map[1, distinguished], pure_map[2, distinguished])
    )
    program = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(10),dp(4),dp(2));",
        'LIB "primdec.lib";',
        "option(redSB);",
        "proc sameIdeal(ideal A,ideal B)",
        "{",
        "  ideal SA=std(A); ideal SB=std(B);",
        "  ideal AB=reduce(SA,SB); ideal BA=reduce(SB,SA);",
        "  AB=simplify(AB,2); BA=simplify(BA,2);",
        "  return((size(AB)==0)&&(size(BA)==0));",
        "}",
        ideal_definition("I", equations),
        "I=slimgb(I);",
        "ideal J=std(eliminate(I,x0*x1*x2*x3*y0*y1*y2*y3*w*u));",
    ]
    expected_primary_count = 0
    expected_radical = True
    if distinguished == 0:
        program.extend(
            (
                "ideal E=1;",
                "int expected_equal=sameIdeal(J,E);",
                "int primary_match=1;",
                "int component_pairs_match=1;",
                "int radical_match=1;",
                "int j_radical=1;",
                "int minass_count=0;",
                "int primary_count=0;",
            )
        )
    else:
        component_lines, expected_primary_count, expected_radical = (
            component_program_lines(distinguished)
        )
        program.extend(component_lines)
        program.extend(
            (
                "int minass_count=size(MA);",
                "int primary_count=size(PD);",
            )
        )
        if distinguished in (1, 2):
            program.append(
                ideal_definition(
                    "Displayed", expected_projection_generators(distinguished)
                )
            )
            program.append("expected_equal=expected_equal&&sameIdeal(J,Displayed);")
    program.extend(
        (
            "matrix N[8][4]=" + ",".join(map(singular, rows)) + ";",
            "ideal Mn=minor(N,4);",
            "ideal RankDrop=slimgb(I+Mn);",
            "poly rankRemainder=reduce(1,RankDrop);",
            ideal_definition("TP", transverse),
            "ideal Transverse=slimgb(I+TP);",
            "poly transverseRemainder=reduce(1,Transverse);",
            ideal_definition("FixedTP", (u * normalized_open - 1, *fixed_transverse)),
            "FixedTP=slimgb(FixedTP);",
            "poly fixedRemainder=reduce(1,FixedTP);",
        )
    )
    if distinguished == 3:
        base_factor = sp.factor(
            p * (p + 1) * q * (q - 1) * (p - q) * (p - q + 2) * (2 * p * q - p + q)
        )
        program.extend(
            (
                "ideal Base=std(eliminate(J,h0*h1*h2*h3));",
                ideal_definition("BaseExpected", (base_factor,)),
                "int base_equal=sameIdeal(Base,BaseExpected);",
                "int base_size=size(Base);",
            )
        )
    else:
        program.extend(("int base_equal=1;", "int base_size=0;"))
    program.extend(
        (
            '"CODEX_RESULT:d='
            + str(distinguished)
            + ':j_size="+string(size(J))'
            + '+":minass="+string(minass_count)'
            + '+":primary="+string(primary_count)'
            + '+":expected_equal="+string(expected_equal)'
            + '+":primary_match="+string(primary_match)'
            + '+":component_pairs_match="+string(component_pairs_match)'
            + '+":radical_match="+string(radical_match)'
            + '+":j_radical="+string(j_radical)'
            + '+":minors="+string(size(Mn))'
            + '+":rank_unit="+string(rankRemainder==0)'
            + '+":transverse_unit="+string(transverseRemainder==0)'
            + '+":fixed_transverse_unit="+string(fixedRemainder==0)'
            + '+":base_equal="+string(base_equal)'
            + '+":base_size="+string(base_size);',
            "quit;",
        )
    )
    started = time.perf_counter()
    completed = subprocess.run(
        singular_command(),
        input="\n".join(program),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=600,
        check=False,
    )
    elapsed = time.perf_counter() - started
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    values = dict(field.split("=", 1) for field in markers[0].split(":")[1:])
    assert int(values["d"]) == distinguished
    assert values["expected_equal"] == "1"
    assert values["primary_match"] == "1"
    assert values["component_pairs_match"] == "1"
    assert values["radical_match"] == "1"
    assert values["j_radical"] == str(int(expected_radical))
    assert values["rank_unit"] == "1"
    assert values["transverse_unit"] == "1"
    assert values["fixed_transverse_unit"] == "1"
    assert values["base_equal"] == "1"
    assert int(values["primary"]) == expected_primary_count
    assert int(values["minass"]) == expected_primary_count
    # Standard-basis size is order-dependent.  These values are for the
    # documented (dp(10),dp(4),dp(2)) elimination order.
    expected_projection_size = (1, 5, 5, 14)[distinguished]
    expected_minor_count = (6, 68, 68, 68)[distinguished]
    assert int(values["j_size"]) == expected_projection_size, (
        distinguished,
        values,
        completed.stdout,
    )
    assert int(values["minors"]) == expected_minor_count, (
        distinguished,
        values,
        completed.stdout,
    )
    return {
        "distinguished_coordinate": distinguished,
        "projected_standard_basis_size": int(values["j_size"]),
        "minimal_components": int(values["minass"]),
        "primary_components": int(values["primary"]),
        "displayed_projection_or_decomposition_equal": True,
        "primary_decomposition_replay_equal": True,
        "primary_components_matched_individually": True,
        "minimal_radical_replay_equal": True,
        "projected_ideal_is_radical": expected_radical,
        "nonzero_generated_maximal_minors": int(values["minors"]),
        "simultaneous_rank_drop_empty": True,
        "all_pure_transverse_entries_vanish_empty": True,
        "fixed_pure_transverse_entries_vanish_empty": True,
        "base_factor_equal": bool(int(values["base_equal"])),
        "base_standard_basis_size": int(values["base_size"]),
        "singular_seconds": round(elapsed, 3),
    }


def main() -> None:
    alpha, canonical_beta = pure_bases()
    beta = shifted_basis(alpha, canonical_beta)
    tensor = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS4
    }
    normalized_open = (p + q) * (p - q + 1)
    assert sp.factor(tensor[(1, 1, 1, 1)] - 2 * normalized_open) == 0
    assert all(
        sp.factor(value) == 0 for word, value in tensor.items() if word != (1, 1, 1, 1)
    )

    pure_map = one_marked_map(3, alpha, beta)
    expected_fixed = {
        0: (2 * normalized_open,),
        1: (p * q, (p + 1) * (q - 1)),
        2: (-p * q, -(p + 1) * (q - 1)),
        3: (-p * q * (p - q + 2), -(p + 1) * (p - q) * (q - 1)),
    }
    for distinguished, expected in expected_fixed.items():
        actual = (
            (pure_map[7, 0],)
            if distinguished == 0
            else (pure_map[1, distinguished], pure_map[2, distinguished])
        )
        assert all(
            sp.factor(left - right) == 0 for left, right in zip(actual, expected)
        )

    certificates = [
        exact_certificate(distinguished, alpha, beta, pure_map)
        for distinguished in range(4)
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "field": "characteristic zero",
                "normalized_open": "(p+q)*(p-q+1) != 0",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "generic_theorem": GENERIC_THEOREM.name,
                "generic_theorem_sha256": sha256(GENERIC_THEOREM),
                "pure_support": {"1111": "2*(p+q)*(p-q+1)"},
                "certificates": certificates,
                "all_special_divisor_intersections_inside_open_closed": True,
                "finite_field_inference_used": False,
                "broad_search_used": False,
                "intrinsic_boundary_p_minus_q_plus_one_closed": False,
                "normalization_boundary_p_plus_q_closed": False,
                "parameter_infinity_closed": False,
                "source_torus_or_projective_boundaries_closed": False,
                "singleton_sheet_closed": False,
                "weighted_H22_closed": False,
                "component_exhaustiveness_closed": False,
                "arbitrary_order_reduction_closed": False,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
