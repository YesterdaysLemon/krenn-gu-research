#!/usr/bin/env python3
"""Independent exact verifier for the exceptional weighted-H22 candidate."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
CLAIM = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py"
REPORT = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_INDEPENDENT_AUDIT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Subset-DP permanent, independent of every audited implementation."""

    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                key = mask | (1 << column)
                next_states[key] = next_states.get(key, 0) + coefficient * entry
        states = next_states
    return sp.expand(states[(1 << len(rows)) - 1])


def add(*vectors):
    return tuple(sp.expand(sum(entries)) for entries in zip(*vectors))


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def shift(alpha, beta, marking):
    return tuple(add(beta[mode], scale(marking[mode], alpha[mode])) for mode in range(4))


def wedge(left, right):
    return tuple(
        sp.factor(left[i] * right[j] - left[j] * right[i])
        for i, j in itertools.combinations(range(4), 2)
    )


def direct_bases(a: sp.Expr, chart: str, lam: sp.Expr):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    k0 = scale(2 * a + 1, cap_c)
    alpha = (k0, e, e, em)
    beta0 = add(e, scale(lam, ell)) if chart == "B_full" else ell
    beta = (
        beta0,
        add(scale(a + 1, ell), cap_c),
        add(scale(a, ell), cap_c),
        e,
    )
    return alpha, beta


def lower_bases(x: sp.Expr, y: sp.Expr, gamma: sp.Expr | None = None):
    e = (sp.Integer(1), 0, 0, 0)
    ell = (0, 1, -1, 0)
    em = (0, 1, 1, 0)
    cap_c = (0, 0, 0, 1)
    w = add(scale(x, ell), scale(y, em))
    alpha = (e, em, e, add(cap_c, scale(-1, w)))
    final = ell if gamma is None else add(ell, scale(gamma, e))
    beta = (ell, e, add(cap_c, w), final)
    return alpha, beta


def contract(row, extension, direction: str, slope: sp.Expr):
    if direction == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "infinity":
        return (row[0], row[2], row[3], extension)
    raise ValueError(direction)


def reconstruct(alpha, canonical_beta, direction: str, slope: sp.Expr, marking):
    beta = shift(alpha, canonical_beta, marking)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[mode], extensions[mode], direction, slope)
        for mode in range(4)
    )
    beta_rows = tuple(
        contract(beta[mode], extensions[4 + mode], direction, slope)
        for mode in range(4)
    )
    coefficients = {
        word: permanent(tuple(
            beta_rows[mode] if word[mode] else alpha_rows[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    mixed = sp.Matrix([
        [sp.diff(coefficients[word], extension) for extension in extensions]
        for word in MIXED_WORDS
    ])
    return {
        "extensions": extensions,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "diagonal_a": coefficients[WORDS[0]],
        "diagonal_b": coefficients[WORDS[-1]],
    }


def marked_matrix(model, mode: int) -> sp.Matrix:
    alpha_rows = model["alpha_rows"]
    beta_rows = model["beta_rows"]
    other_modes = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_rows[other] if bits[position] else alpha_rows[other]
            for position, other in enumerate(other_modes)
        )
        rows.append(tuple(
            permanent(tuple(
                tuple(row[index] for index in range(4) if index != column)
                for row in selected
            ))
            for column in range(4)
        ))
    return sp.Matrix(rows)


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def assert_zero(values) -> None:
    assert all(sp.factor(value) == 0 for value in values), values


def rank_witness(matrix: sp.Matrix, rank: int):
    assert matrix.rank() == rank, matrix.rank()
    columns = matrix.rref()[1][:rank]
    rows = matrix.T.rref()[1][:rank]
    determinant = sp.factor(matrix.extract(rows, columns).det())
    assert determinant != 0
    return tuple(rows), tuple(columns), determinant


def pure_geometry_audit() -> dict[str, object]:
    lam, x, y, gamma = sp.symbols("lambda x y gamma")
    direct = {}
    for centre in (0, -1):
        direct[str(centre)] = {}
        for chart in ("B_full", "B_drop"):
            alpha, beta = direct_bases(sp.Integer(centre), chart, lam)
            coefficients = {
                word: sp.factor(permanent(tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                ))) for word in WORDS
            }
            expected = (-2 * lam if chart == "B_full" else -2) * (1 if centre == 0 else -1)
            assert_equal(coefficients[WORDS[-1]], expected)
            assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
            direct[str(centre)][chart] = str(expected)
    lower = {}
    for family, parameter in (("baseline", None), ("wall", gamma)):
        alpha, beta = lower_bases(x, y, parameter)
        coefficients = {
            word: sp.factor(permanent(tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            ))) for word in WORDS
        }
        assert coefficients[WORDS[-1]] == -2
        assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
        lower[family] = "-2"
    baseline_alpha, baseline_beta = lower_bases(x, y)
    wall_alpha, wall_beta = lower_bases(x, y, gamma)
    assert wedge(baseline_beta[3], baseline_alpha[3]) == (0, 0, 0, -2 * y, 1, -1)
    assert wedge(wall_beta[3], wall_alpha[3]) == (
        -gamma * (x + y), gamma * (x - y), gamma, -2 * y, 1, -1
    )
    return {
        "direct_sole_coefficients": direct,
        "lower_sole_coefficients": lower,
        "baseline_last_plane_pluecker": ["0", "0", "0", "-2*y", "1", "-1"],
        "wall_last_plane_pluecker": ["-gamma*(x+y)", "gamma*(x-y)", "gamma", "-2*y", "1", "-1"],
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact projection audit")


def singular_text(value: sp.Expr) -> str:
    return str(sp.cancel(value)).replace("**", "^")


def projection_audit(label, model, expected, parameters=(), inversions=(), finite=False):
    started = time.perf_counter()
    extensions = model["extensions"]
    mixed = model["mixed"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    h = sp.symbols("h0:4")
    winv = sp.Symbol("winv")
    equations = [
        *tuple(mixed * sp.Matrix(extensions)), diagonal_a - 1,
        winv * diagonal_b - 1,
    ]
    eliminated = extensions + (winv,)
    if finite:
        eliminated += (sp.Symbol("r"),)
    for parameter, inverse_name in inversions:
        inverse = sp.Symbol(inverse_name)
        equations.append(inverse * parameter - 1)
        eliminated += (inverse,)
    variables = eliminated + h + tuple(parameters)
    blocks = f"(dp({len(eliminated)}),dp(4)"
    if parameters:
        blocks += f",dp({len(parameters)})"
    blocks += ")"
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables)) + ")," + blocks + ";",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular_text, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular_text, expected)) + ";",
        "E=std(E);",
        "ideal L=simplify(reduce(J,E),2);",
        "ideal Right=simplify(reduce(E,J),2);",
        '"AUDIT:"+string((size(L)==0)&&(size(Right)==0))+":"+string(size(J));',
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
        timeout=30, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (label, completed)
    markers = [line for line in completed.stdout.splitlines() if line.startswith("AUDIT:")]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (label, completed.stdout)
    return {
        "label": label,
        "ideal": [singular_text(value) for value in expected],
        "bidirectional_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
        "normalization": "A=1, winv*B=1",
        "seconds": round(time.perf_counter() - started, 3),
    }


def projection_audits():
    h0, h1, h2, h3 = sp.symbols("h0:4")
    lam, slope = sp.symbols("lambda r")
    results = []
    marking = (h0, h1, h2, h3)
    for centre in (0, -1):
        expected = (h3, h2, h0) if centre == 0 else (h3, h1, h0)
        for chart in ("B_full", "B_drop"):
            alpha, beta = direct_bases(sp.Integer(centre), chart, lam)
            for direction in ("finite", "infinity"):
                model = reconstruct(alpha, beta, direction, slope, marking)
                parameters = (lam,) if chart == "B_full" else ()
                inversions = ((lam, "linv"),) if chart == "B_full" else ()
                results.append(projection_audit(
                    f"a={centre}:{chart}:{direction}", model, expected,
                    parameters, inversions, direction == "finite",
                ))
    x, y, gamma = sp.symbols("x y gamma")
    lower_expected = {
        ("baseline", "finite"): (h3, h2, h1),
        ("baseline", "infinity"): (h3, h2, h1),
        ("wall", "finite"): (h3, h2, h1),
        ("wall", "infinity"): (h3, h2, h1, h0),
    }
    for family in ("baseline", "wall"):
        alpha, beta = lower_bases(x, y, None if family == "baseline" else gamma)
        for direction in ("finite", "infinity"):
            model = reconstruct(alpha, beta, direction, slope, marking)
            parameters = (x, y) if family == "baseline" else (x, y, gamma)
            inversions = () if family == "baseline" else ((gamma, "ginv"),)
            results.append(projection_audit(
                f"lower:{family}:{direction}", model,
                lower_expected[(family, direction)], parameters, inversions,
                direction == "finite",
            ))
    return results


def kernel_audit(label, model, expected_rank, mode, rows, expected_a, expected_b, expected_minor):
    mixed = model["mixed"]
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - expected_rank
    frame = sp.Matrix.hstack(*kernel)
    assert frame.rank() == len(kernel)
    assert_zero(mixed * frame)
    witness_rows, witness_columns, witness = rank_witness(mixed, expected_rank)
    coefficients = sp.symbols(f"K0:{len(kernel)}")
    extension = frame * sp.Matrix(coefficients)
    substitution = dict(zip(model["extensions"], extension))
    actual_a = sp.factor(model["diagonal_a"].subs(substitution))
    actual_b = sp.factor(model["diagonal_b"].subs(substitution))
    minor = sp.factor(
        marked_matrix(model, mode).subs(substitution).extract(rows, range(4)).det()
    )
    assert_equal(actual_a, expected_a(*coefficients))
    assert_equal(actual_b, expected_b(*coefficients))
    assert_equal(minor, expected_minor(*coefficients))
    projective_scale = sp.Symbol("c", nonzero=True)
    scaled = {
        variable: projective_scale * value
        for variable, value in zip(model["extensions"], extension)
    }
    assert_equal(model["diagonal_a"].subs(scaled), projective_scale * actual_a)
    assert_equal(model["diagonal_b"].subs(scaled), projective_scale * actual_b)
    scaled_minor = sp.factor(
        marked_matrix(model, mode).subs(scaled).extract(rows, range(4)).det()
    )
    assert_equal(scaled_minor, projective_scale**3 * minor)
    return {
        "label": label,
        "rank": expected_rank,
        "nullity": len(kernel),
        "complete_kernel": [[str(sp.factor(value)) for value in vector] for vector in kernel],
        "rank_witness_rows": list(witness_rows),
        "rank_witness_columns": list(witness_columns),
        "rank_witness": str(witness),
        "A": str(actual_a),
        "B": str(actual_b),
        "marked_mode": mode,
        "minor_rows": list(rows),
        "minor": str(minor),
        "projective_scaling_checked": True,
    }


def no_genuine_audit(label, model, diagonal: str):
    mixed = model["mixed"]
    rank = mixed.rank()
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - rank
    frame = sp.Matrix.hstack(*kernel)
    assert frame.rank() == len(kernel)
    assert_zero(mixed * frame)
    expression = model["diagonal_a"] if diagonal == "A" else model["diagonal_b"]
    assert all(
        sp.factor(expression.subs(dict(zip(model["extensions"], vector)))) == 0
        for vector in kernel
    )
    rows, columns, witness = rank_witness(mixed, rank)
    return {
        "label": label,
        "rank": rank,
        "nullity": len(kernel),
        "complete_kernel": [[str(sp.factor(value)) for value in vector] for vector in kernel],
        "rank_witness_rows": list(rows),
        "rank_witness_columns": list(columns),
        "rank_witness": str(witness),
        f"{diagonal}_on_complete_kernel": "zero",
        "genuine_neighbour_exists": False,
    }


def direct_fibre_audits():
    lam, slope, t = sp.symbols("lambda r t")
    results = []
    specifications = (
        (0, "B_full", "finite", (0,t,0,0), 6, (0,2,4,7),
         lambda X,Y: -2*Y*slope,
         lambda X,Y: -2*(lam+slope)*(X*slope+Y*(slope*t+1)),
         lambda X,Y: -8*Y**2*lam*slope**2*(lam+slope)*(X*slope+Y*(slope*t+1))),
        (0, "B_full", "infinity", (0,t,0,0), 6, (0,2,4,7),
         lambda X,Y: -2*Y, lambda X,Y: -2*(X*lam+Y),
         lambda X,Y: -8*Y**2*lam*(X*lam+Y)),
        (0, "B_drop", "finite", (0,t,0,0), 6, (0,2,4,7),
         lambda X,Y: -2*Y*slope,
         lambda X,Y: -2*(X*slope+Y*(slope*t+1)),
         lambda X,Y: -8*Y**2*slope**2*(X*slope+Y*(slope*t+1))),
        (0, "B_drop", "infinity", (0,t,0,0), 5, (0,2,4,7),
         lambda X,Y,Z: -2*Z, lambda X,Y,Z: -2*X,
         lambda X,Y,Z: -8*X*Z**2),
        (-1, "B_full", "finite", (0,0,t,0), 6, (0,1,4,7),
         lambda X,Y: 2*Y*slope,
         lambda X,Y: -2*(X*lam*slope-Y*(lam+slope)),
         lambda X,Y: 8*Y**2*lam*slope**2*(X*lam*slope-Y*(lam+slope))),
        (-1, "B_full", "infinity", (0,0,t,0), 6, (0,1,4,7),
         lambda X,Y: 2*Y, lambda X,Y: -2*(X*lam-Y),
         lambda X,Y: 8*Y**2*lam*(X*lam-Y)),
        (-1, "B_drop", "finite", (0,0,t,0), 6, (0,1,4,7),
         lambda X,Y: 2*Y*slope, lambda X,Y: -2*(X*slope-Y),
         lambda X,Y: 8*Y**2*slope**2*(X*slope-Y)),
        (-1, "B_drop", "infinity", (0,0,t,0), 5, (0,1,4,7),
         lambda X,Y,Z: 2*Z, lambda X,Y,Z: -2*Y,
         lambda X,Y,Z: 8*Y*Z**2),
    )
    for centre, chart, direction, marking, rank, rows, ea, eb, em in specifications:
        alpha, beta = direct_bases(sp.Integer(centre), chart, lam)
        model = reconstruct(alpha, beta, direction, slope, marking)
        results.append(kernel_audit(
            f"a={centre}:{chart}:{direction}:generic", model, rank, 3,
            rows, ea, eb, em,
        ))
    for centre in (0, -1):
        marking = (0,t,0,0) if centre == 0 else (0,0,t,0)
        for chart in ("B_full", "B_drop"):
            alpha, beta = direct_bases(sp.Integer(centre), chart, lam)
            model = reconstruct(alpha, beta, "finite", sp.Integer(0), marking)
            results.append(no_genuine_audit(f"a={centre}:{chart}:r=0", model, "A"))
    for centre in (0, -1):
        marking = (0,t,0,0) if centre == 0 else (0,0,t,0)
        alpha, beta = direct_bases(sp.Integer(centre), "B_full", lam)
        model = reconstruct(alpha, beta, "finite", -lam, marking)
        results.append(no_genuine_audit(f"a={centre}:B_full:r=-lambda", model, "B"))
    return results


def residue_specializations(x, y):
    return (
        ("generic-x2-ne-y2", x, y),
        ("x=0", sp.Integer(0), y),
        ("x=y", y, y),
        ("x=-y", -y, y),
        ("y=0", x, sp.Integer(0)),
        ("origin", sp.Integer(0), sp.Integer(0)),
    )


def lower_generic_audits():
    x, y, gamma, slope, t = sp.symbols("x y gamma r t")
    results = []
    for residue, residue_x, residue_y in residue_specializations(x, y):
        baseline_alpha, baseline_beta = lower_bases(residue_x, residue_y)
        wall_alpha, wall_beta = lower_bases(residue_x, residue_y, gamma)
        model = reconstruct(baseline_alpha, baseline_beta, "finite", slope, (t,0,0,0))
        results.append(kernel_audit(
            f"lower:baseline:{residue}:finite", model, 6, 1, (0,1,3,7),
            lambda X,Y: -2*X*slope,
            lambda X,Y: -2*X*(slope*t+1),
            lambda X,Y: 8*X**3*slope**2*(slope*t+1),
        ))
        model = reconstruct(baseline_alpha, baseline_beta, "infinity", slope, (t,0,0,0))
        results.append(kernel_audit(
            f"lower:baseline:{residue}:infinity", model, 5, 1, (0,1,3,7),
            lambda X,Y,Z: -2*X,
            lambda X,Y,Z: -2*(X*t+Z),
            lambda X,Y,Z: 8*X**2*(X*t+Z),
        ))
        model = reconstruct(wall_alpha, wall_beta, "finite", slope, (t,0,0,0))
        results.append(kernel_audit(
            f"lower:wall:{residue}:finite", model, 6, 1, (0,1,3,7),
            lambda X,Y: -2*Y*slope/(gamma*(slope*t+1)),
            lambda X,Y: -2*Y*(gamma*slope+1)/gamma,
            lambda X,Y: 8*Y**3*slope**2*(gamma*slope+1)/(gamma**3*(slope*t+1)**2),
        ))
        model = reconstruct(wall_alpha, wall_beta, "infinity", slope, (0,0,0,0))
        results.append(kernel_audit(
            f"lower:wall:{residue}:infinity", model, 5, 1, (0,1,3,7),
            lambda X,Y,Z: -2*X, lambda X,Y,Z: -2*Z,
            lambda X,Y,Z: 8*X**2*Z,
        ))
    return results


def lower_singular_audits():
    x, y, gamma, slope, t = sp.symbols("x y gamma r t")
    results = []
    for residue, residue_x, residue_y in residue_specializations(x, y):
        baseline_alpha, baseline_beta = lower_bases(residue_x, residue_y)
        wall_alpha, wall_beta = lower_bases(residue_x, residue_y, gamma)
        for family, alpha, beta in (
            ("baseline", baseline_alpha, baseline_beta),
            ("wall", wall_alpha, wall_beta),
        ):
            model = reconstruct(alpha, beta, "finite", sp.Integer(0), (t,0,0,0))
            results.append(no_genuine_audit(
                f"lower:{family}:{residue}:r=0", model, "A"
            ))
            model = reconstruct(alpha, beta, "finite", slope, (-1/slope,0,0,0))
            results.append(no_genuine_audit(
                f"lower:{family}:{residue}:r*t+1=0", model, "B"
            ))
        model = reconstruct(
            wall_alpha, wall_beta, "finite", -1/gamma, (t,0,0,0)
        )
        results.append(no_genuine_audit(
            f"lower:wall:{residue}:gamma*r+1=0", model, "B"
        ))
    return results


def symmetry_and_residue_exhaustion():
    z0, z1, z2, z3, extension, slope = sp.symbols("z0 z1 z2 z3 u r")
    row = (z0, z1, z2, z3)
    signed = (-z0, z1, z2, z3)
    assert contract(signed, extension, "finite", slope) == contract(
        row, extension, "finite", -slope
    )
    infinity_signed = contract(signed, extension, "infinity", slope)
    infinity_original = contract(row, extension, "infinity", slope)
    assert infinity_signed == (
        -infinity_original[0], infinity_original[1],
        infinity_original[2], infinity_original[3],
    )
    symbolic_entries = sp.symbols("m0:16")
    symbolic_rows = tuple(
        tuple(symbolic_entries[4 * row + column] for column in range(4))
        for row in range(4)
    )
    swapped_rows = (
        symbolic_rows[0], symbolic_rows[2], symbolic_rows[1], symbolic_rows[3]
    )
    assert permanent(swapped_rows) == permanent(symbolic_rows)
    pi, theta, delta = sp.symbols("pi theta Delta")
    x_map = (pi - theta) / 2
    y_map = (pi + theta) / 2
    assert_equal(x_map**2 - y_map**2, -pi * theta)
    assert_equal(-2 * y_map, -(pi + theta))
    assert_equal((-2 * y_map).subs(pi + theta, delta), -delta)
    assert_equal((x_map - y_map).subs(theta, 0), 0)
    assert_equal((x_map + y_map).subs(pi, 0), 0)
    return {
        "a_minus_one": {
            "lower_mode_swap_preserves_permanent": True,
            "source_sign_e_to_minus_e_reparametrizes_finite_slope": "r -> -r",
            "infinity_preserved_up_to_invertible_target_column_sign": True,
        },
        "residue_map": {"x": "(pi-theta)/2", "y": "(pi+theta)/2"},
        "x_squared_minus_y_squared": "-pi*theta",
        "p12": "-2*y=-(pi+theta)=-Delta",
        "audited_residue_strata": [
            "generic x^2!=y^2", "x=0", "x=y", "x=-y", "y=0", "origin"
        ],
        "valuation_regimes": [
            "valuation(y0)>-R gives x=y=0",
            "valuation(y0)=-R,R<d gives y=0",
            "valuation(y0)=-R,R=d gives y=Delta/2!=0",
        ],
    }


def main():
    started = time.perf_counter()
    claim_hash = sha256(CLAIM)
    primary_hash = sha256(PRIMARY)
    geometry = pure_geometry_audit()
    projections = projection_audits()
    direct = direct_fibre_audits()
    lower_generic = lower_generic_audits()
    lower_singular = lower_singular_audits()
    exhaustion = symmetry_and_residue_exhaustion()
    assert sha256(CLAIM) == claim_hash
    assert sha256(PRIMARY) == primary_hash
    source = Path(__file__).resolve()
    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "exceptional a=0,-1 B_full/B_drop and all actual lower-pair "
            "baseline/wall D01 fibres on the verified p+q=0 diagonal-DVR boundary"
        ),
        "inputs": {CLAIM.name: claim_hash, PRIMARY.name: primary_hash},
        "method": (
            "independent subset-DP permanent; direct plane and contraction "
            "reconstruction; 12 exact projections; complete kernels, diagonal-zero "
            "special slopes, fixed marked minors, symmetry and residue exhaustion"
        ),
        "command": (
            "uv run --with sympy python audit_p5_h22_common_active_binary_"
            "triangle_p_plus_q_exceptional_fibres_independent.py"
        ),
        "outputs": {REPORT.name: sha256(REPORT), source.name: sha256(source)},
        "limitations": (
            "VERIFIED only conditional on the cited P4 residue classification and "
            "only for diagonal-DVR exceptional D01 fibres; no other centres, "
            "non-diagonal source transformations, arbitrary-order gluing, or global claim"
        ),
        "verdict": "VERIFIED",
        "geometry": geometry,
        "projection_certificates": projections,
        "direct_fibre_certificates": direct,
        "lower_generic_residue_certificates": lower_generic,
        "lower_singular_slope_certificates": lower_singular,
        "symmetry_and_residue_exhaustion": exhaustion,
        "projection_count": len(projections),
        "direct_certificate_count": len(direct),
        "lower_generic_residue_certificate_count": len(lower_generic),
        "lower_singular_slope_certificate_count": len(lower_singular),
        "primary_or_helper_or_existing_audit_imported": False,
        "audited_inputs_unchanged_during_run": True,
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "failure_ledger": [
            {
                "attempt": "initial independent projection replay",
                "result": "Singular identifier collision: ring and right-reduction ideal were both named R",
                "correction": "renamed the reduction ideal Right and reran the entire audit",
                "mathematical_evidence_from_failed_run": False,
            }
        ],
        "global_Krenn_Gu_conjecture_resolved": False,
        "runtime_seconds": round(time.perf_counter() - started, 3),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
