#!/usr/bin/env python3
"""Independent exact audit of component 21's normalized projective boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import time
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


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_VERTICAL_U0_PROJECTIVE_BOUNDARY_COMPLETE_OBSTRUCTION.md"
PRIMARY = (
    ROOT
    / "verify_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Permanent by subset dynamic programming, independent of the primary."""
    size = len(rows)
    assert all(len(row) == size for row in rows)
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row_index, row in enumerate(rows):
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, sp.Integer(0))
                    + coefficient * row[column]
                )
        states = next_states
        assert all(mask.bit_count() == row_index + 1 for mask in states)
    return sp.expand(states[(1 << size) - 1])


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def bases(
    alpha_parameter: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr | None,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    if ell is None:
        return (
            (add(cap_a, scale(-alpha_parameter, cap_c)), cap_a, cap_c, cap_d),
            (cap_b, cap_c, add(cap_b, scale(kappa, cap_a)), cap_c),
        )
    return (
        (
            add(cap_a, scale(-alpha_parameter, cap_c)),
            add(scale(ell, cap_a), cap_c),
            cap_c,
            cap_d,
        ),
        (
            cap_b,
            cap_a,
            add(cap_b, scale(kappa, cap_a)),
            add(cap_a, scale(ell, cap_c)),
        ),
    )


def mark(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def h31_coefficients(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[mode][index] for index in retained) + (extension[mode],)
        for mode in range(4)
    )
    beta_rows = tuple(
        tuple(beta[mode][index] for index in retained) + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        word: permanent_dp(
            tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    matrix_rows: list[tuple[sp.Expr, ...]] = []
    for word in itertools.product((0, 1), repeat=3):
        selected: list[tuple[sp.Expr, ...] | None] = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if word[bit] else alpha[other])
                bit += 1
        coefficient_row: list[sp.Expr] = []
        for coordinate in range(4):
            basis = tuple(sp.Integer(index == coordinate) for index in range(4))
            square_rows = tuple(
                basis if other == mode else selected[other] for other in range(4)
            )
            assert all(row is not None for row in square_rows)
            coefficient_row.append(permanent_dp(square_rows))  # type: ignore[arg-type]
        matrix_rows.append(tuple(coefficient_row))
    return sp.Matrix(matrix_rows)


def h31_obstruction_map(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[row][index] for index in retained) + (extension[row],)
        for row in range(4)
    )
    beta_rows = tuple(
        tuple(beta[row][index] for index in retained) + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(3, alpha_rows, beta_rows)


def project(
    row: tuple[sp.Expr, ...],
    extension: sp.Symbol,
    direction: str,
    chart: str,
    slope: sp.Symbol,
) -> tuple[sp.Expr, ...]:
    if (direction, chart) == ("D01", "finite"):
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if (direction, chart) == ("D23", "finite"):
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if (direction, chart) == ("D01", "infinity"):
        return (row[0], row[2], row[3], extension)
    if (direction, chart) == ("D23", "infinity"):
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def contraction(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    direction: str,
    chart: str,
    slope: sp.Symbol,
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    dict[tuple[int, ...], sp.Expr],
]:
    alpha_rows = tuple(
        project(alpha[i], extension[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extension[4 + i], direction, chart, slope)
        for i in range(4)
    )
    coefficients: dict[tuple[int, ...], sp.Expr] = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index]
            for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent_dp(
                    tuple(selected[other][:3] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )
    return alpha_rows, beta_rows, coefficients


def contraction_obstruction_map(
    alpha_rows: tuple[tuple[sp.Expr, ...], ...],
    beta_rows: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    output: list[tuple[sp.Expr, ...]] = []
    others = (0, 1, 2)
    for word in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_rows[index] if word[position] else alpha_rows[index]
            for position, index in enumerate(others)
        )
        output.append(
            tuple(
                permanent_dp(
                    tuple(
                        tuple(row[column] for column in range(4) if column != omitted)
                        for row in selected
                    )
                )
                for omitted in range(4)
            )
        )
    return sp.Matrix(output)


FINITE_PRIMES = (
    "h3,h2,h1,kappa,alpha+ell",
    "h3,h2,h1,ell+1,kappa",
    "h3,h2,h1,ell-1,kappa",
    (
        "kappa*ell-h2,(2*alpha*ell+ell^2+1)*h1+alpha+ell,"
        "2*alpha*h1*h2+ell*h1*h2+alpha*kappa+kappa*h1+h2,h3,h0"
    ),
    "h3,h0,ell+1,kappa+h2",
    "h3,h0,ell-1,kappa-h2",
    "(ell-1)*h1+1,h3,h0,alpha+1",
    "(ell+1)*h1+1,h3,h0,alpha-1",
    "(alpha-1)*h1+1,h3,h0,ell+1",
    "(alpha+1)*h1+1,h3,h0,ell-1",
)

INFINITY_PRIMES = (
    "h3,h1+1,h0,alpha+h1",
    "h3,h1-1,h0,alpha+h1",
    "h3,h0,kappa,alpha+h1",
)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def comparison_lines(
    source_ring: str,
    retained_names: tuple[str, ...],
    expected_primes: tuple[str, ...],
    label: str,
) -> list[str]:
    count = len(expected_primes)
    lines = [
        "ring S=0,(" + ",".join(retained_names) + "),dp;",
        f"ideal J=imap({source_ring},J);",
        'LIB "primdec.lib";',
        "list L=minAssGTZ(J);",
    ]
    for expected_index, generators in enumerate(expected_primes, start=1):
        lines.extend(
            (
                f"ideal E{expected_index}={generators};",
                f"E{expected_index}=std(E{expected_index});",
            )
        )
        comparisons = []
        for actual_index in range(1, count + 1):
            lines.extend(
                (
                    f"ideal A{expected_index}_{actual_index}=std(L[{actual_index}]);",
                    (
                        f"ideal X{expected_index}_{actual_index}=simplify("
                        f"reduce(A{expected_index}_{actual_index},E{expected_index}),2);"
                    ),
                    (
                        f"ideal Y{expected_index}_{actual_index}=simplify("
                        f"reduce(E{expected_index},A{expected_index}_{actual_index}),2);"
                    ),
                )
            )
            comparisons.append(
                f"((size(X{expected_index}_{actual_index})==0)"
                f"&&(size(Y{expected_index}_{actual_index})==0))"
            )
        lines.append(f"int H{expected_index}=" + "+".join(comparisons) + ";")
    hits = "+\":\"+".join(
        f"string(H{index})" for index in range(1, count + 1)
    )
    lines.append(
        f'"CODEX_DECOMP:{label}:"+string(size(J))+":"+string(size(L))+":"+'
        + hits
        + ";"
    )
    lines.append("quit;")
    return lines


def run_case(
    label: str,
    equations: tuple[sp.Expr, ...],
    obstruction: tuple[sp.Expr, ...],
    eliminated: tuple[sp.Symbol, ...],
    retained: tuple[sp.Symbol, ...],
    expected_primes: tuple[str, ...],
) -> tuple[int, int]:
    variables = eliminated + retained
    lines = [
        "ring R=0,("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(singular(expression) for expression in equations) + ";",
        "I=slimgb(I);",
        "ideal O=" + ",".join(singular(expression) for expression in obstruction) + ";",
        "ideal G=std(I+O);",
        f'"CODEX_UNIT:{label}:"+string((size(G)==1)&&(G[1]==1));',
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    lines.extend(
        comparison_lines(
            "R", tuple(map(str, retained)), expected_primes, label
        )
    )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    unit_markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith(f"CODEX_UNIT:{label}:")
    ]
    decomposition_markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith(f"CODEX_DECOMP:{label}:")
    ]
    assert unit_markers == [f"CODEX_UNIT:{label}:1"], completed.stdout
    assert len(decomposition_markers) == 1, completed.stdout
    fields = decomposition_markers[0].split(":")
    assert fields[:2] == ["CODEX_DECOMP", label]
    assert all(field == "1" for field in fields[4:]), (
        decomposition_markers[0],
        completed.stdout,
    )
    assert int(fields[3]) == len(expected_primes)
    return int(fields[2]), int(fields[3])


def h31_case(distinguished: int, ell_infinity: bool) -> tuple[
    tuple[sp.Expr, ...],
    tuple[sp.Expr, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[str, ...],
]:
    alpha_parameter, kappa, ell = sp.symbols("alpha kappa ell")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse = sp.Symbol("v")
    alpha, canonical_beta = bases(
        alpha_parameter, kappa, None if ell_infinity else ell
    )
    beta = mark(alpha, canonical_beta, shifts)
    coefficients = h31_coefficients(distinguished, alpha, beta, extension)
    vector = sp.Matrix(extension)
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], value) for value in extension]
            for word in MIXED
        ]
    )
    diagonal_alpha = sp.Matrix(
        [[sp.diff(coefficients[WORDS[0]], value) for value in extension]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(coefficients[WORDS[-1]], value) for value in extension]]
    )
    equations = tuple(mixed * vector) + (
        sp.expand((diagonal_alpha * vector)[0] - 1),
        sp.expand(inverse * (diagonal_beta * vector)[0] - 1),
    )
    obstruction = tuple(h31_obstruction_map(
        distinguished, alpha, beta, extension
    ))
    retained = (
        (alpha_parameter, kappa) + shifts
        if ell_infinity
        else (alpha_parameter, kappa, ell) + shifts
    )
    return (
        equations,
        obstruction,
        extension + (inverse,),
        retained,
        INFINITY_PRIMES if ell_infinity else FINITE_PRIMES,
    )


def h22_case(chart: str, ell_infinity: bool) -> tuple[
    tuple[sp.Expr, ...],
    tuple[sp.Expr, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[str, ...],
]:
    alpha_parameter, kappa, ell, slope = sp.symbols("alpha kappa ell lambda")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse_a, inverse_b = sp.symbols("u v")
    alpha, canonical_beta = bases(
        alpha_parameter, kappa, None if ell_infinity else ell
    )
    beta = mark(alpha, canonical_beta, shifts)
    _, _, d01 = contraction(
        alpha, beta, extension, "D01", chart, slope
    )
    d23_alpha, d23_beta, d23 = contraction(
        alpha, beta, extension, "D23", chart, slope
    )
    mixed = sp.Matrix(
        [[sp.diff(d23[word], value) for value in extension] for word in MIXED]
    )
    equations = (
        *(d01[word] for word in WORDS[:-1]),
        sp.expand(d01[WORDS[-1]] - 1),
        *tuple(mixed * sp.Matrix(extension)),
        sp.expand(inverse_a * d23[WORDS[0]] - 1),
        sp.expand(inverse_b * d23[WORDS[-1]] - 1),
    )
    obstruction = tuple(contraction_obstruction_map(d23_alpha, d23_beta))
    retained = (
        (alpha_parameter, kappa) + shifts
        if ell_infinity
        else (alpha_parameter, kappa, ell) + shifts
    )
    if chart == "finite":
        retained += (slope,)
    return (
        equations,
        obstruction,
        extension + (inverse_a, inverse_b),
        retained,
        INFINITY_PRIMES if ell_infinity else FINITE_PRIMES,
    )


def main() -> None:
    started = time.perf_counter()
    alpha_parameter, kappa, ell = sp.symbols("alpha kappa ell")
    finite_alpha, finite_beta = bases(alpha_parameter, kappa, ell)
    infinity_alpha, infinity_beta = bases(alpha_parameter, kappa, None)
    pure_support: dict[str, dict[str, str]] = {}
    for label, alpha, beta, expected in (
        ("finite_ell", finite_alpha, finite_beta, sp.Integer(4)),
        ("ell_infinity", infinity_alpha, infinity_beta, sp.Integer(-4)),
    ):
        coefficients = {
            word: sp.factor(
                permanent_dp(
                    tuple(beta[index] if word[index] else alpha[index] for index in range(4))
                )
            )
            for word in WORDS
        }
        assert coefficients[WORDS[-1]] == expected
        assert all(
            value == 0 for word, value in coefficients.items() if word != WORDS[-1]
        )
        pure_support[label] = {"1111": str(expected)}

    cases = {
        "H31_finite_d2": h31_case(2, False),
        "H31_finite_d3": h31_case(3, False),
        "H22_finite_weight": h22_case("finite", False),
        "H22_infinity_weight": h22_case("infinity", False),
        "H31_ell_infinity_d2": h31_case(2, True),
        "H31_ell_infinity_d3": h31_case(3, True),
        "H22_ell_infinity_finite_weight": h22_case("finite", True),
        "H22_ell_infinity_infinity_weight": h22_case("infinity", True),
    }
    results = {
        label: run_case(label, *case) for label, case in cases.items()
    }
    assert all(result == (13, 10) for result in list(results.values())[:4])
    assert all(result == (4, 3) for result in list(results.values())[4:])
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import direct mode-3-zero exclusion",
                "field": "characteristic zero",
                "pure_support_subset_dp": pure_support,
                "global_decompositions": results,
                "direct_mode3_zero_ideals_are_unit": 8,
                "theorem_sha256": sha256(THEOREM),
                "primary_sha256": sha256(PRIMARY),
                "finite_field_proof_used": False,
                "arbitrary_source_projective_boundary_closed": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
