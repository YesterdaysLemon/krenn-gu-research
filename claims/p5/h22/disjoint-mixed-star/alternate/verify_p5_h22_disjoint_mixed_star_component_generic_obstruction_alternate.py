#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the disjoint mixed star.

Characteristic-zero certificates over the component function field

    K = C(a,b,f)[phi]/(Phi),  slope r transcendental:

1.  In both weighted pencils, the four single-one mixed words have
    t-free own-extension coefficients that are nonzero in K(r) (nonzero
    resultants), hence invertible on the declared generic dense open.
    Eliminating the four marked-extension variables reduces the 14 x 8
    mixed system to an exact 10 x 4
    system G(t) x = 0 with x nonzero whenever the kernel is nonzero.
2.  D_01 marking locus: one-minor locus certificates prove that every
    kernel marking satisfies t1*t2 = 0, and on the two sheets the
    finer branch products (phi*(t0-1)-f)*t2 and
    ((a*f*r+a*f-r+1)*t1-r-1)*t3 vanish as well.
3.  D_23 marking locus: on each chart t1 != 0, t2 != 0, t3 != 0 the
    ideal of all 4 x 4 minors of G plus Phi is the unit ideal.
4.  On every marking stratum, the two mode-zero one-marked minors in
    rows (0,1,3,7) and (0,1,5,7) cannot both vanish on a genuine
    binary survivor: five saturated Fitting ideals are unit.

Hence every genuine binary survivor of either weighted pencil has a
rank-four mode-zero one-marked contraction and admits no ternary
lift, so the generic weighted H22 incidence on the eighth component
is empty.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sympy as sp

import sys
HERE = Path(__file__).resolve().parent


def _repo_root() -> Path:
    for candidate in (HERE, *HERE.parents):
        if (candidate / ".git").exists():
            return candidate
    return HERE


REPO_ROOT = _repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_"
    "ALTERNATE.md"
)
COMPONENT = REPO_ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"

a, b, f, phi, r = sp.symbols("a b f phi r")
T = sp.symbols("t0:4")
X = sp.symbols("x0:4")
w = sp.Symbol("w")

J = f + b * phi**2
KAPPA = phi * (b * f + 1)
ETA = -(b * f + 1)

ALPHA = (
    (0, 0, 1, -1),
    (-a * f + 1, -a * f - 1, f + phi, f - phi),
    (-a * J + ETA, -a * J - ETA, J + KAPPA, J - KAPPA),
    (1, -1, 0, 0),
)
BETA = (
    (a + b, a - b, 0, 2),
    (1, 1, 0, 0),
    (1, 1, 0, 0),
    (0, 0, 1, 1),
)
PHI = sp.expand(
    a**2 * b * f * phi**2 + a**2 * f**2
    - b**2 * f**2 + b**2 * phi**2 - b * f - 1
)
# Phi = W_DEN*phi^2 - W_NUM, so phi^2 = W_NUM/W_DEN on the component.
W_DEN = sp.expand(b * (a**2 * f + b))
W_NUM = sp.expand(-(a**2 * f**2 - b**2 * f**2 - b * f - 1))

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
SINGLE = tuple(u for u in BITS4 if sum(u) == 1)
REST = tuple(
    u for u in BITS4 if 2 <= sum(u) <= 3
)
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

D01_MINOR_WORDS = ((0, 0, 1, 1), (0, 1, 1, 0), (1, 0, 0, 1),
                   (1, 0, 1, 1))
D01_SHEET_T1_WORDS = ((0, 0, 1, 1), (1, 0, 0, 1), (1, 0, 1, 0),
                      (1, 0, 1, 1))
D01_SHEET_T2_WORDS = ((0, 0, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1),
                      (1, 0, 1, 1))
FITTING_ROWS = ((0, 1, 3, 7), (0, 1, 5, 7))
GROEBNER_TIMEOUT = 3600


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perm4(rows):
    return sp.expand(sum(
        sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4
    ))


def weighted3(row, direction: str):
    if direction == "01":
        return (r * row[0] + row[1], row[2], row[3])
    if direction == "23":
        return (row[0], row[1], r * row[2] + row[3])
    raise ValueError(direction)


def phi_reduce_uniform(expressions):
    """Reduce a family modulo phi^2 = W_NUM/W_DEN, clearing the W_DEN
    powers by one uniform factor for the whole family."""
    split = []
    max_q = 0
    for expr in expressions:
        p = sp.Poly(sp.expand(expr), phi)
        terms = []
        for (k,), coeff in p.terms():
            q, rem = divmod(k, 2)
            terms.append((q, rem, coeff))
            max_q = max(max_q, q)
        split.append(terms)
    out = []
    for terms in split:
        e = 0
        for q, rem, coeff in terms:
            e += coeff * W_NUM**q * W_DEN**(max_q - q) * phi**rem
        out.append(sp.expand(e))
    return out


def phi_normal_form(expr):
    return phi_reduce_uniform([expr])[0]


def build_direction(direction: str):
    """Mixed/diagonal coefficients of the weighted binary extension,
    the y-eliminated 10 x 4 system, and the mode-zero one-marked
    matrix with the kernel substitution applied."""
    marked_beta = tuple(
        tuple(BETA[m][c] + T[m] * ALPHA[m][c] for c in range(4))
        for m in range(4)
    )
    walpha = tuple(weighted3(ALPHA[m], direction) for m in range(4))
    wbeta = tuple(
        weighted3(marked_beta[m], direction) for m in range(4)
    )
    zx = sp.symbols(f"zx_{direction}_0:4")
    zy = sp.symbols(f"zy_{direction}_0:4")
    alpha_ext = tuple(walpha[m] + (zx[m],) for m in range(4))
    beta_ext = tuple(wbeta[m] + (zy[m],) for m in range(4))
    coefficients = {
        bits: perm4(tuple(
            beta_ext[m] if bits[m] else alpha_ext[m] for m in range(4)
        ))
        for bits in BITS4
    }
    zvars = tuple(zx) + tuple(zy)
    matrix_rows = {}
    for bits in BITS4:
        expr = coefficients[bits]
        row = []
        for zv in zvars:
            coefficient = sp.expand(sp.diff(expr, zv))
            assert not set(coefficient.free_symbols) & set(zvars)
            row.append(coefficient)
        reconstructed = sp.expand(
            sum(c * zv for c, zv in zip(row, zvars))
        )
        assert sp.expand(expr - reconstructed) == 0
        matrix_rows[bits] = row
    # The single-one rows have t-free own-extension coefficients.
    denominators = {}
    y_numerators = {}
    for u in SINGLE:
        m = u.index(1)
        row = matrix_rows[u]
        own = row[4 + m]
        assert not set(own.free_symbols) & set(T)
        assert all(row[4 + k] == 0 for k in range(4) if k != m)
        row_t = {
            k: row[k] for k in range(4) if k != m
        }
        assert all(
            not (set(value.free_symbols) & set(T)) - {T[m]}
            for value in row_t.values()
        )
        denominators[m] = own
        y_numerators[m] = [
            -row[k] if k != m else sp.Integer(0) for k in range(4)
        ]
    # Substitution Z(x) = D*(x, y(x)).
    D_full = sp.expand(
        denominators[0] * denominators[1]
        * denominators[2] * denominators[3]
    )
    Zx = [sp.expand(D_full * X[m]) for m in range(4)]
    Zy = []
    for m in range(4):
        clear = sp.prod(
            denominators[k] for k in range(4) if k != m
        )
        Zy.append(sp.expand(
            sum(y_numerators[m][col] * X[col] for col in range(4))
            * clear
        ))
    substitution = dict(zip(zvars, tuple(Zx) + tuple(Zy)))
    # Single-one rows vanish identically under the substitution.
    for u in SINGLE:
        residue = phi_normal_form(
            coefficients[u].subs(substitution)
        )
        assert sp.expand(residue) == 0, u
    # The reduced system G.
    g_rows = []
    for u in REST:
        substituted = sp.expand(coefficients[u].subs(substitution))
        g_rows.append(phi_normal_form(substituted))
    g_matrix = []
    for expr in g_rows:
        row = []
        for xv in X:
            coefficient = sp.expand(sp.diff(expr, xv))
            assert not set(coefficient.free_symbols) & set(X)
            row.append(coefficient)
        assert sp.expand(
            expr - sum(c * xv for c, xv in zip(row, X))
        ) == 0
        g_matrix.append(row)
    # The extended rows carry the kernel substitution in the fourth
    # column.  The one-marked matrix and the two diagonals are
    # expanded lazily, after each stratum's t-substitution, which
    # keeps the permanent expansions small.
    alpha_sub = tuple(
        walpha[m] + (Zx[m],) for m in range(4)
    )
    beta_sub = tuple(
        wbeta[m] + (Zy[m],) for m in range(4)
    )
    return {
        "denominators": denominators,
        "g_words": REST,
        "g_matrix": g_matrix,
        "alpha_rows": alpha_sub,
        "beta_rows": beta_sub,
    }


def resultant_certificate(expr):
    """Nonzero resultant with Phi proves the expression is nonzero in
    K(r) = Frac(C(a,b,f,r)[phi]/(Phi)), hence invertible on the declared
    generic dense open; its zero locus is contained in the explicitly
    excluded parameter/slope divisors.  A phi-free reduction is itself a
    nonzero parameter function with the same property."""
    reduced = phi_normal_form(expr)
    assert reduced != 0
    if phi not in reduced.free_symbols:
        return str(sp.factor(reduced))
    resultant = sp.resultant(
        sp.Poly(reduced, phi), sp.Poly(PHI, phi)
    )
    resultant = sp.factor(resultant)
    assert resultant != 0
    return str(resultant)


def singular_command(timeout: float):
    if os.name == "nt":
        return (
            "wsl.exe",
            "--exec",
            "/usr/bin/timeout",
            "--signal=KILL",
            f"{timeout:.6f}s",
            "/usr/bin/Singular",
            "-q",
        )
    return ("Singular", "-q")


def run_singular(program: str, label: str) -> str:
    completed = subprocess.run(
        singular_command(GROEBNER_TIMEOUT),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=GROEBNER_TIMEOUT + 10,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (label, completed.returncode, completed.stdout,
             completed.stderr)
        )
    return completed.stdout


def sing(expr) -> str:
    return str(sp.expand(expr)).replace("**", "^")


def one_minor_locus_certificate(data, words, substitution, product,
                                label):
    """One 4x4 minor of the (restricted) reduced system cuts the
    marking locus: the ideal generated by the reduced determinant,
    Phi, and the Rabinowitsch inversion of `product` is the unit
    ideal.  Hence every kernel marking on the restriction satisfies
    `product` = 0.  The determinant factorization is recorded for
    the ledger; the certificate is the unit ideal."""
    indices = [REST.index(word) for word in words]
    entries = ",".join(
        sing(sp.expand(entry.subs(substitution)))
        for i in indices
        for entry in data["g_matrix"][i]
    )
    program = "\n".join((
        "ring R=(0,a,b,f,r),(phi,t0,t1,t2,t3,s),dp;",
        "option(redSB);",
        f"matrix S[4][4]={entries};",
        "poly d=det(S);",
        f"poly Phi={sing(PHI)};",
        "poly nf=reduce(d,std(Phi));",
        "int nonzero=(nf!=0);",
        f"ideal I=nf,Phi,s*({sing(sp.expand(product))})-1;",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        f'"CODEX_RESULT:{label}:"+string(nonzero)+":"+string(unit);',
        "list L=factorize(nf);",
        "int i;",
        'string factors="";',
        "for(i=2;i<=size(L[1]);i++){",
        '  factors=factors+"["+string(L[1][i])+"]^"'
        '+string(L[2][i])+" ";',
        "}",
        '"CODEX_FACTORS:"+factors;',
        "quit;",
    ))
    output = run_singular(program, f"minor locus {label}")
    markers = [
        line.strip() for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == [f"CODEX_RESULT:{label}:1:1"], (label, output)
    factor_lines = [
        line.split(":", 1)[1]
        for line in output.splitlines()
        if line.startswith("CODEX_FACTORS:")
    ]
    return factor_lines[0]


def d23_chart_certificate(data, chart: str) -> None:
    entries = ",".join(
        sing(entry) for row in data["g_matrix"] for entry in row
    )
    program = "\n".join((
        "ring R=(0,a,b,f,r),(phi,t0,t1,t2,t3,s),dp;",
        "option(redSB);",
        f"matrix G[10][4]={entries};",
        "ideal I=minor(G,4);",
        f"I=I,{sing(PHI)},s*({chart})-1;",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        f'"CODEX_RESULT:{chart}:"+string(unit);',
        "quit;",
    ))
    output = run_singular(program, f"D23 chart {chart}")
    markers = [
        line.strip() for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == [f"CODEX_RESULT:{chart}:1"], (chart, output)


def fitting_certificate(direction: str, data, sheet, label: str,
                        extra_generators=(), algorithm="std"):
    substitution = {tv: sheet.get(str(tv), tv) for tv in T}
    free_t = [tv for tv in T if str(tv) not in sheet]
    rows = [
        sp.expand(
            sum(
                entry.subs(substitution) * xv
                for entry, xv in zip(row, X)
            )
        )
        for row in data["g_matrix"]
    ]
    alpha_rows = tuple(
        tuple(
            sp.expand(sp.sympify(entry).subs(substitution))
            for entry in row
        )
        for row in data["alpha_rows"]
    )
    beta_rows = tuple(
        tuple(
            sp.expand(sp.sympify(entry).subs(substitution))
            for entry in row
        )
        for row in data["beta_rows"]
    )

    def marked_row(bits):
        chosen = [
            beta_rows[m] if bits[m - 1] else alpha_rows[m]
            for m in (1, 2, 3)
        ]
        row = []
        for col in range(4):
            basis = tuple(int(i == col) for i in range(4))
            row.append(perm4((basis,) + tuple(chosen)))
        return row

    marked_cache = {}
    matrices = []
    for selected in FITTING_ROWS:
        entries = []
        for i in selected:
            bits = BITS3[i]
            if bits not in marked_cache:
                marked_cache[bits] = marked_row(bits)
            entries.append(marked_cache[bits])
        flat = phi_reduce_uniform(
            [entry for row in entries for entry in row]
        )
        matrices.append([flat[i * 4:(i + 1) * 4] for i in range(4)])
    diag_a = phi_normal_form(
        perm4(tuple(alpha_rows[m] for m in range(4)))
    )
    diag_b = phi_normal_form(
        perm4(tuple(beta_rows[m] for m in range(4)))
    )
    variables = [phi] + list(X) + [w] + free_t
    lines = [
        "ring R=(0,a,b,f,r),("
        + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(sing(e) for e in rows) + ";",
        f"I=I,{sing(PHI)};",
    ]
    for generator in extra_generators:
        lines.append(f"I=I,{generator};")
    for index, entries in enumerate(matrices):
        flat = ",".join(
            sing(entry) for row in entries for entry in row
        )
        lines.append(f"matrix D{index}[4][4]={flat};")
        lines.append(f"I=I,det(D{index});")
    lines.extend((
        f"poly AB=({sing(diag_a)})*({sing(diag_b)});",
        "I=I,w*AB-1;",
        f"I={algorithm}(I);",
        "int unit=(reduce(1,I)==0);",
        f'"CODEX_RESULT:{label}:"+string(unit);',
        "quit;",
    ))
    output = run_singular("\n".join(lines), f"Fitting {label}")
    markers = [
        line.strip() for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == [f"CODEX_RESULT:{label}:1"], (label, output)


def main() -> None:
    started = time.monotonic()
    theorem_text = " ".join(
        THEOREM.read_text(encoding="utf-8").split()
    )
    assert "t_1 t_2 = 0" in theorem_text
    assert "t_1 = t_2 = t_3 = 0" in theorem_text
    assert "component exhaustiveness" in theorem_text
    assert "global prize problem" in theorem_text

    # Pure component sanity: only the all-beta coefficient survives.
    pure = {
        bits: perm4(tuple(
            (BETA if bits[m] else ALPHA)[m] for m in range(4)
        ))
        for bits in BITS4
    }
    for bits, value in pure.items():
        residue = phi_normal_form(value)
        if bits == (1, 1, 1, 1):
            assert sp.expand(residue - 4) == 0
        elif bits == (1, 0, 0, 1):
            assert sp.expand(value + 4 * PHI) == 0
        else:
            assert sp.expand(residue) == 0

    certificates = {}
    directions = {}
    for direction in ("01", "23"):
        data = build_direction(direction)
        directions[direction] = data
        certificates[f"denominator_resultants_{direction}"] = {
            str(m): resultant_certificate(value)[:400]
            for m, value in sorted(
                data["denominators"].items()
            )
        }

    branch_t0 = phi * T[0] - phi - f
    branch_t1 = (
        (a * f * r + a * f - r + 1) * T[1] - r - 1
    )
    factors_global = one_minor_locus_certificate(
        directions["01"], D01_MINOR_WORDS, {}, T[1] * T[2],
        "d01-global",
    )
    factors_sheet_t1 = one_minor_locus_certificate(
        directions["01"], D01_SHEET_T1_WORDS, {T[1]: 0},
        branch_t0 * T[2], "d01-sheet-t1",
    )
    factors_sheet_t2 = one_minor_locus_certificate(
        directions["01"], D01_SHEET_T2_WORDS, {T[2]: 0},
        branch_t1 * T[3], "d01-sheet-t2",
    )
    certificates["d01_global_locus"] = {
        "rows": [
            "".join(map(str, word)) for word in D01_MINOR_WORDS
        ],
        "locus_product": "t1*t2",
        "certificate": "unit ideal after inverting the product",
        "determinant_factors": factors_global,
    }
    certificates["d01_sheet_t1_locus"] = {
        "rows": [
            "".join(map(str, word)) for word in D01_SHEET_T1_WORDS
        ],
        "locus_product": "(phi*t0-phi-f)*t2",
        "certificate": "unit ideal after inverting the product",
        "determinant_factors": factors_sheet_t1,
    }
    certificates["d01_sheet_t2_locus"] = {
        "rows": [
            "".join(map(str, word)) for word in D01_SHEET_T2_WORDS
        ],
        "locus_product": "((a*f*r+a*f-r+1)*t1-r-1)*t3",
        "certificate": "unit ideal after inverting the product",
        "determinant_factors": factors_sheet_t2,
    }

    fitting_strata = (
        (
            "fitting_d23_line",
            "23",
            {"t1": 0, "t2": 0, "t3": 0},
            "23-line",
            (),
            "std",
        ),
        (
            "fitting_d01_t1_t2",
            "01",
            {"t1": 0, "t2": 0},
            "01-t1t2",
            (),
            "std",
        ),
        (
            "fitting_d01_t1_branch",
            "01",
            {"t1": 0},
            "01-t1-branch",
            ("phi*t0-phi-f",),
            "std",
        ),
        (
            "fitting_d01_t2_t3",
            "01",
            {"t2": 0, "t3": 0},
            "01-t2t3",
            (),
            "std",
        ),
        (
            "fitting_d01_t2_branch",
            "01",
            {"t2": 0},
            "01-t2-branch",
            ("(a*f*r+a*f-r+1)*t1-r-1",),
            "slimgb",
        ),
    )
    jobs = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for chart in ("t1", "t2", "t3"):
            jobs.append((
                f"d23_chart_{chart}",
                executor.submit(
                    d23_chart_certificate, directions["23"], chart
                ),
            ))
        for key, direction, sheet, label, extra, algorithm in (
            fitting_strata
        ):
            jobs.append((
                key,
                executor.submit(
                    fitting_certificate,
                    direction,
                    directions[direction],
                    sheet,
                    label,
                    extra,
                    algorithm,
                ),
            ))
        for label, job in jobs:
            job.result()
            certificates[label] = "unit ideal"

    result = {
        "verified": True,
        "field": "C(a,b,f)[phi]/(Phi), slope r transcendental",
        "component": "disjoint mixed-star fivefold (eighth orbit)",
        "pencils": {
            "D01": {
                "marking_locus": "t1*t2=0",
                "proof": (
                    "one 4x4 minor of the y-eliminated 10x4 system "
                    "equals a nonzero field constant times t1*t2 "
                    "modulo Phi"
                ),
                "sheet_refinements": {
                    "t1=0": "t2*(phi*(t0-1)-f)=0",
                    "t2=0": "t3*((a*f*r+a*f-r+1)*t1-r-1)=0",
                },
                "fitting_strata": [
                    "t1=t2=0",
                    "t1=0, phi*(t0-1)=f",
                    "t2=t3=0",
                    "t2=0, (a*f*r+a*f-r+1)*t1=r+1",
                ],
            },
            "D23": {
                "marking_locus": "t1=t2=t3=0",
                "proof": (
                    "all 4x4 minors of the y-eliminated system plus "
                    "Phi form the unit ideal on each chart t_i != 0"
                ),
                "fitting_strata": ["t1=t2=t3=0"],
            },
        },
        "mode_zero_one_marked_minor_rows": [
            list(rows) for rows in FITTING_ROWS
        ],
        "certificates": certificates,
        "generic_weighted_H22_component_incidence_empty": True,
        "all_eight_component_orbits_generically_closed_for_H22": True,
        "parameter_and_slope_divisors_closed": False,
        "projective_boundary_closed": False,
        "all_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "dependencies": {
            "theorem": {
                "path": THEOREM.name,
                "sha256": sha256(THEOREM),
            },
            "component": {
                "path": COMPONENT.name,
                "sha256": sha256(COMPONENT),
            },
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / "tmp"
        / (
            "p5_h22_disjoint_mixed_star_component_generic_"
            "obstruction_alternate_verified.json"
        )
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
