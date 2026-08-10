#!/usr/bin/env python3
"""Verify the generic marked H31 obstruction on the tenth (coincident-support)
pure-compression component.

Self-contained (sympy + Singular on PATH).  All statements are exact: the
symbolic identities are over Z[b,e,k,m,c,t0..t3], and the two Groebner
projections are over the function field C(b,e,m,c) at the k=1 torus gauge.
Fail-closed: any Singular timeout or mismatch raises.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def find_root() -> Path:
    for candidate in (HERE, *HERE.parents):
        if (candidate / "claims/p4/boundaries/inout-path-stratum/P4_INOUT_PATH_STRATUM_WORKING_NOTE.md").exists():
            return candidate
    return HERE


ROOT = find_root()
THEOREM = HERE / "P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = REPO_ROOT / "claims/p4/boundaries/inout-path-stratum/P4_INOUT_PATH_STRATUM_WORKING_NOTE.md"
COMPONENT_PRIMARY = REPO_ROOT / "claims/p4/boundaries/inout-path-stratum/branch_ambient_certificates.py"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, k, m, c = sp.symbols("b e k m c")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")

SINGULAR_TIMEOUT = 550
WITNESS_ROWS = (0, 1, 3, 4, 5, 7, 8)  # words 0001,0010,0100,0101,0110,1000,1001
WITNESS_COLS = (0, 1, 2, 3, 4, 5, 6)  # x0..x3, y0..y2


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def raw_planes(kk):
    return (
        ((1, -1, 0, 0), (0, 1, b, -b * kk)),
        ((1, -1, 0, 0), (0, 1, e, -e * kk)),
        ((1, 1, 0, 0), (0, 0, 1, kk)),
        ((1, m, 0, 0), (0, c, 1, -kk)),
    )


def concentrated_basis(kk):
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, kk),
             (P, P * m - Q * c, -Q, Q * kk))
    beta = ((0, 1, b, -b * kk), (0, 1, e, -e * kk), (1, 1, 0, 0), (0, c, 1, -kk))
    return alpha, beta


def marked_beta(alpha, beta):
    return tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                 for i in range(4))


def h31_word_coefficients(q, alpha, betat):
    """word -> [coefficient of the extension variable of row i, i=0..3]."""
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    out = {}
    for wd in WORDS:
        out[wd] = [perm3(tuple((bett[j] if wd[j] else alph[j])
                               for j in range(4) if j != i))
                   for i in range(4)]
    return out


def zvar(wd, i):
    return Z[i + (4 if wd[i] else 0)]


def word_form(coeffs, wd):
    return sp.expand(sum(coeffs[wd][i] * zvar(wd, i) for i in range(4)))


def check_component_normal_form():
    planes = raw_planes(k)
    raw = {wd: perm4(tuple(planes[i][wd[i]] for i in range(4))) for wd in WORDS}
    assert sp.expand(raw[(1, 1, 0, 0)] + 2 * k * Q) == 0
    assert sp.expand(raw[(1, 1, 0, 1)] + 2 * k * P) == 0
    assert all(sp.expand(v) == 0 for wd, v in raw.items()
               if wd not in ((1, 1, 0, 0), (1, 1, 0, 1)))

    alpha, beta = concentrated_basis(k)
    for i in range(4):
        stack = sp.Matrix([list(planes[i][0]), list(planes[i][1]),
                           list(alpha[i]), list(beta[i])])
        assert stack.rank() == 2, i
    tensor = {wd: perm4(tuple(beta[i] if wd[i] else alpha[i] for i in range(4)))
              for wd in WORDS}
    assert sp.expand(tensor[(1, 1, 1, 1)] + 2 * k * P) == 0
    assert all(sp.expand(v) == 0 for wd, v in tensor.items() if wd != (1, 1, 1, 1))

    # marking invariance and marked-basis forcing
    betat = marked_beta(alpha, beta)
    shifted = {wd: perm4(tuple(betat[i] if wd[i] else alpha[i] for i in range(4)))
               for wd in WORDS}
    assert all(sp.expand(shifted[wd] - tensor[wd]) == 0 for wd in WORDS)

    kappa = sp.symbols("ka0:4")
    nu = sp.symbols("nu0:4")
    sigma = sp.symbols("si0:4")
    tau = sp.symbols("ta0:4")
    kernel_rows = tuple(tuple(sigma[i] * alpha[i][j] + kappa[i] * beta[i][j]
                              for j in range(4)) for i in range(4))
    colour_rows = tuple(tuple(tau[i] * alpha[i][j] + nu[i] * beta[i][j]
                              for j in range(4)) for i in range(4))
    for i in range(4):
        near = tuple(0 if j == i else 1 for j in range(4))
        value = perm4(tuple(colour_rows[j] if near[j] else kernel_rows[j]
                            for j in range(4)))
        expected = -2 * k * P * kappa[i] * sp.prod(nu[j] for j in range(4) if j != i)
        assert sp.expand(value - expected) == 0, i
    top = perm4(colour_rows)
    assert sp.expand(top + 2 * k * P * sp.prod(nu)) == 0
    return str(-2 * k * P)


def check_gauge():
    lam = sp.symbols("lam0:4")
    rows = sp.symbols("r0:4c0:4")
    generic = tuple(tuple(sp.Symbol(f"g{i}_{j}") for j in range(4)) for i in range(4))
    scaled = tuple(tuple(generic[i][j] * lam[j] for j in range(4)) for i in range(4))
    assert sp.expand(perm4(scaled) - sp.prod(lam) * perm4(generic)) == 0

    planes_k = raw_planes(k)
    planes_1 = raw_planes(sp.Integer(1))
    torus = (1, 1, 1, 1 / k)
    for i in range(4):
        moved = tuple(tuple(planes_k[i][row][j] * torus[j] for j in range(4))
                      for row in range(2))
        stack = sp.Matrix([list(moved[0]), list(moved[1]),
                           list(planes_1[i][0]), list(planes_1[i][1])])
        stack = stack.applyfunc(sp.cancel)
        assert stack.rank() == 2, i


def check_dead_frames():
    alpha, beta = concentrated_basis(k)
    betat = marked_beta(alpha, beta)
    for q in (0, 1):
        coeffs = h31_word_coefficients(q, alpha, betat)
        assert all(sp.expand(x) == 0 for x in coeffs[(0, 0, 0, 0)]), q
    # mechanism 1: apolar mode-2/3 alpha tails
    assert sp.expand(alpha[2][2] * alpha[3][3] + alpha[2][3] * alpha[3][2]) == 0
    # mechanism 2: coincident kernel rows alpha_0 = alpha_1 = ybar
    assert alpha[0] == alpha[1] == (1, -1, 0, 0)


def check_live_frames():
    alpha, beta = concentrated_basis(k)
    betat = marked_beta(alpha, beta)
    astar = 2 * b * c * e - (b + e) * (m - 1)
    expected_a = {
        2: tuple(sp.expand(v) for v in (-k * astar, -k * astar, -2 * k * Q, -2 * k)),
        3: tuple(sp.expand(v) for v in (-astar, -astar, 2 * Q, -2)),
    }
    witness = {}
    for q in (2, 3):
        coeffs = h31_word_coefficients(q, alpha, betat)
        arow = tuple(sp.expand(x) for x in coeffs[(0, 0, 0, 0)])
        assert arow == expected_a[q], (q, arow)
        assert all(sp.diff(x, ti) == 0 for x in arow for ti in T)

        # reconstruction kernel: restore column q
        sub = {Z[i]: alpha[i][q] for i in range(4)}
        sub.update({Z[4 + i]: betat[i][q] for i in range(4)})
        for wd in WORDS:
            value = sp.expand(word_form(coeffs, wd).subs(sub))
            if wd == (1, 1, 1, 1):
                assert sp.expand(value + 2 * k * P) == 0, q
            else:
                assert value == 0, (q, wd)

        # rank-7 witness at t=0 and k=1
        zero = {ti: 0 for ti in T}
        one = {k: 1}
        matrix = sp.Matrix([[sp.diff(word_form(coeffs, wd).subs(zero).subs(one), zz)
                             for zz in Z] for wd in MIXED])
        minor = sp.factor(matrix[list(WITNESS_ROWS), list(WITNESS_COLS)].det())
        sign = 1 if q == 2 else -1
        expected = sign * 4 * b * c**2 * e**3 * (m + 1)**2 * P
        assert sp.expand(minor - expected) == 0, (q, minor)
        witness[q] = str(minor)
    return witness


def singular_str(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run_singular(program: str, timeout: float):
    start = time.time()
    completed = subprocess.run(
        ["Singular", "-q"],
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 10,
    )
    elapsed = time.time() - start
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            ("Singular failure", completed.returncode, completed.stdout[-2000:],
             completed.stderr[:2000])
        )
    return completed.stdout, elapsed


def run_projection(q: int):
    alpha, beta = concentrated_basis(sp.Integer(1))
    betat = marked_beta(alpha, beta)
    coeffs = h31_word_coefficients(q, alpha, betat)
    equations = [word_form(coeffs, wd) for wd in MIXED]
    equations.append(word_form(coeffs, (0, 0, 0, 0)) - 1)
    equations.append(W * word_form(coeffs, (1, 1, 1, 1)) - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        "ring R=(0,b,e,m,c),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal incidence=" + ",".join(singular_str(x) for x in equations) + ";",
        "ideal basis=std(incidence);",
        "ideal marking=eliminate(basis," + "*".join(map(str, eliminated)) + ");",
        "marking=std(marking);",
        '"MARKING";',
        "marking;",
        "quit;",
    ))
    stdout, elapsed = run_singular(program, SINGULAR_TIMEOUT)
    generators = tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )
    return generators, elapsed


# --------------------------------------------------------------------------
# Interior parameter divisors {c=0} and {b+e=0}: sheet projections and
# per-sheet ternary Fitting closures (mode-2 one-marked minors, A=1
# normalization).
# --------------------------------------------------------------------------

WORDS3 = tuple(itertools.product((0, 1), repeat=3))
DIVISOR_SHEETS = {
    "c=0": (
        "t3",
        "t2",
        "(e^2*m+e^2)*t0+(b^2*m+b^2)*t1+(-b^2+b*e*m-b*e-e^2)",
        "(b^2*m^2-b^2)*t1^2+(2*b^2+b*e*m^2-2*b*e*m+b*e-2*e^2*m)*t1"
        "+(-b^2+b*e*m-b*e+e^2*m)",
    ),
    "b+e=0": (
        "(2*b^2)*t3+1",
        "t2",
        "t0+t1-1",
        "t1^2-t1",
    ),
}
DIVISOR_PARAMS = {"c=0": "b,e,m", "b+e=0": "b,m,c"}
DIVISOR_SUBS = {"c=0": {c: 0}, "b+e=0": {e: -b}}
MINOR_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7))
MARKED_MODE = 2


def divisor_frame(q, divisor, tvals):
    """Frame word forms and extended rows on the divisor with marking tvals
    (entries may be symbols); row denominators cleared."""
    sub = DIVISOR_SUBS[divisor]
    alpha, beta = concentrated_basis(sp.Integer(1))
    alpha = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row)
                  for row in alpha)
    beta = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row)
                 for row in beta)
    betat = []
    for i in range(4):
        row = tuple(sp.together(beta[i][j] + tvals[i] * alpha[i][j])
                    for j in range(4))
        lcm = sp.lcm([sp.fraction(sp.cancel(x))[1] for x in row])
        betat.append(tuple(sp.expand(sp.cancel(x * lcm)) for x in row))
    betat = tuple(betat)
    common = tuple(j for j in range(4) if j != q)
    alpha_p = tuple(tuple(alpha[i][j] for j in common) + (Z[i],) for i in range(4))
    beta_p = tuple(tuple(betat[i][j] for j in common) + (Z[4 + i],)
                   for i in range(4))
    forms = {wd: sp.expand(perm4(tuple(beta_p[i] if wd[i] else alpha_p[i]
                                       for i in range(4)))) for wd in WORDS}
    return forms, alpha_p, beta_p


def one_marked_map(mode, alpha_p, beta_p):
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta_p[other] if bits[bit_index] else alpha_p[other])
                bit_index += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(idx == coordinate) for idx in range(4))
            row.append(perm4(tuple(basis if other == mode else selected[other]
                                   for other in range(4))))
        rows.append(row)
    return sp.Matrix(rows)


def divisor_sheet_projection(q, divisor):
    forms, _, _ = divisor_frame(q, divisor, T)
    equations = [forms[wd] for wd in MIXED]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        f"ring R=(0,{DIVISOR_PARAMS[divisor]}),("
        + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_str(x) for x in equations) + ";",
        "ideal J=std(I);",
        "ideal L=eliminate(J," + "*".join(map(str, eliminated)) + ");",
        "L=std(L);",
        '"SHEETS";',
        "L;",
        "quit;",
    ))
    stdout, elapsed = run_singular(program, SINGULAR_TIMEOUT)
    generators = tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("L[")
    )
    return generators, elapsed


def divisor_fitting_certificate(q, divisor, tvals, extra_vars=(), extra_eqs=()):
    forms, alpha_p, beta_p = divisor_frame(q, divisor, tvals)
    marked = one_marked_map(MARKED_MODE, alpha_p, beta_p)
    minors = [sp.expand(marked[list(rows_), :].det()) for rows_ in MINOR_ROWS]
    equations = [forms[wd] for wd in MIXED] + minors + list(extra_eqs)
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z + (W,))) + [str(v) for v in extra_vars]
    order = f"(dp(9),dp({len(extra_vars)}))" if extra_vars else "dp"
    program = "\n".join((
        f"ring R=(0,{DIVISOR_PARAMS[divisor]}),("
        + ",".join(variables) + f"),{order};",
        "ideal I=" + ",".join(singular_str(x) for x in equations) + ";",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        '"UNIT:"+string(unit);',
        "quit;",
    ))
    stdout, elapsed = run_singular(program, SINGULAR_TIMEOUT)
    lines = [ln.strip() for ln in stdout.splitlines() if ln.startswith("UNIT:")]
    assert lines == ["UNIT:1"], (q, divisor, lines, stdout[-800:])
    return elapsed


def run_divisor_closures():
    results = {}
    s0, s1 = sp.symbols("s0 s1")
    lin = (e**2 * m + e**2) * s0 + (b**2 * m + b**2) * s1 \
        + (-b**2 + b * e * m - b * e - e**2)
    quad = (b**2 * m**2 - b**2) * s1**2 \
        + (2 * b**2 + b * e * m**2 - 2 * b * e * m + b * e - 2 * e**2 * m) * s1 \
        + (-b**2 + b * e * m - b * e + e**2 * m)
    for q in (2, 3):
        for divisor in ("c=0", "b+e=0"):
            generators, elapsed = divisor_sheet_projection(q, divisor)
            assert generators == DIVISOR_SHEETS[divisor], (q, divisor, generators)
            certificates = {}
            if divisor == "b+e=0":
                t3v = sp.Rational(-1, 2) / b**2
                for t1v, name in ((0, "t=(1,0,0,-1/(2b^2))"),
                                  (1, "t=(0,1,0,-1/(2b^2))")):
                    dt = divisor_fitting_certificate(
                        q, divisor, (1 - t1v, t1v, 0, t3v))
                    certificates[name] = {"unit": True, "seconds": round(dt, 2)}
            else:
                dt = divisor_fitting_certificate(
                    q, divisor, (s0, s1, 0, 0), extra_vars=(s0, s1),
                    extra_eqs=(lin, quad))
                certificates["t2=t3=0, (t0,t1) on lin+quad"] = {
                    "unit": True, "seconds": round(dt, 2)}
            results[f"q={q} {divisor}"] = {
                "sheet_ideal": list(generators),
                "sheet_projection_seconds": round(elapsed, 2),
                "mode2_minors": [list(rows_) for rows_ in MINOR_ROWS],
                "fitting_certificates": certificates,
            }
    return results


def main() -> None:
    pure = check_component_normal_form()
    check_gauge()
    check_dead_frames()
    witness = check_live_frames()

    projections = {}
    timings = {}
    for q in (2, 3):
        generators, elapsed = run_projection(q)
        assert generators == ("1",), (q, generators)
        projections[q] = generators
        timings[q] = round(elapsed, 2)

    divisor_closures = run_divisor_closures()

    astar = "2*b*c*e-(b+e)*(m-1)"
    output = {
        "verified": True,
        "component": "tenth (coincident-support double-arrow) P4 component",
        "field": "C(b,e,m,c) at the k=1 torus gauge",
        "parameter_renaming": "working-note parameter r renamed to c",
        "method": (
            "support concentration to one word, two identity-dead frames, "
            "reconstruction kernels, and two exact unit marking projections"
        ),
        "pure_coefficient": pure,
        "concentration": {
            "P": "b*e*c+b+e",
            "Q": "b*e*(m+1)",
            "alpha_3": "P*(1,m,0,0)-Q*(0,c,1,-k)",
            "valid_iff": "P != 0",
        },
        "gauge": {
            "torus_element": "diag(1,1,1,1/k)",
            "action": "Z(b,e,k,m,c) -> Z(b,e,1,m,c)",
            "eigenvector_identity": "perm4(rows*diag(lam)) = lam0*lam1*lam2*lam3*perm4(rows)",
        },
        "dead_frames": {
            "q": [0, 1],
            "statement": (
                "the 0000-diagonal row vanishes identically over "
                "Z[b,e,k,m,c,t0..t3]: no genuine binary Delta_2 neighbour for "
                "any marking at any chart point"
            ),
            "mechanisms": [
                "coincident kernel rows alpha_0=alpha_1=ybar supported in columns {0,1}",
                "apolar mode-2/3 alpha tails: perm2((1,k),(-Q,Q*k))=0",
            ],
        },
        "live_frames": {
            "q": [2, 3],
            "A_row_t_free": True,
            "A_row": {
                "2": f"-k*({astar}, {astar}, 2*b*e*(m+1), 2) on (x0,x1,x2,x3)",
                "3": f"-({astar}, {astar}, -2*b*e*(m+1), 2) on (x0,x1,x2,x3)",
            },
            "reconstruction_kernel": (
                "z_rec = restore column q: M z_rec = 0, A z_rec = 0, "
                "B z_rec = -2*k*(b*e*c+b+e), identically in t"
            ),
            "rank7_witness_rows_words": ["0001", "0010", "0100", "0101", "0110",
                                          "1000", "1001"],
            "rank7_witness_cols": ["x0", "x1", "x2", "x3", "y0", "y1", "y2"],
            "rank7_witness_at_t0": witness,
        },
        "marking_projections": {str(q): list(v) for q, v in projections.items()},
        "projection_runtimes_seconds": timings,
        "interior_divisor_closures": {
            "statement": (
                "on the two codimension-one survivor divisors {c=0} and "
                "{b+e=0}, the binary marking sheets are exactly the displayed "
                "ideals, and on every sheet each genuine survivor has a "
                "rank-four mode-2 one-marked map (minors 0127/0137): no "
                "ternary H31 lift exists over the generic point of either "
                "divisor"
            ),
            "mode3_caveat": (
                "on {b+e=0} the mode-3 one-marked map drops to rank three on "
                "the genuine direction; modes 0,1,2 stay rank four"
            ),
            "results": divisor_closures,
        },
        "binary_level_exclusion": True,
        "fitting_stage_needed": False,
        "generic_marked_fibre_excluded": True,
        "complete_boundary_marked_fibre_excluded": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    out_path = HERE / "tmp" / "p5_h31_coincident_support_component_generic_verified.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
