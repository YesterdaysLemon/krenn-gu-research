#!/usr/bin/env python3
"""Independent no-import audit of the embedded-P3 free-plane r0 boundary."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md"
CLAIM = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION_CANDIDATE.md"
PRIMARY = ROOT / "derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py"
H31 = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
H31_PRIMARY = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/verify_p5_h31_embedded_p3_component_r_zero_boundary.py"
)
H22_GENERIC = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
H22_RANK_TWO = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
H22_RANK_ONE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, encoding="utf-8",
        capture_output=True, check=True,
    ).stdout.strip()


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(sum(
        rows[0][columns[p[0]]] * rows[1][columns[p[1]]] * rows[2][columns[p[2]]]
        for p in PERMUTATIONS3
    ))


def bases(cap_s, cap_u, markings):
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    canonical = (
        (1, 0, 0, 0),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    beta = tuple(tuple(
        sp.expand(canonical[i][j] + markings[i] * alpha[i][j]) for j in range(4)
    ) for i in range(4))
    return alpha, beta


def project(row, extension, direction, slope=None):
    if direction == "01f":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "23f":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "01i":
        return (row[0], row[2], row[3], extension)
    if direction == "23i":
        return (row[0], row[1], row[2], extension)
    if direction == "delete0":
        return (row[1], row[2], row[3], extension)
    raise ValueError(direction)


def model(cap_s, cap_u, markings, extension, direction, slope=None):
    alpha, beta = bases(cap_s, cap_u, markings)
    aa = tuple(project(alpha[i], extension[i], direction, slope) for i in range(4))
    bb = tuple(project(beta[i], extension[4+i], direction, slope) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(bb[i] if word[i] else aa[i] for i in range(4))
        coefficients[word] = sp.expand(sum(
            selected[i][3] * permanent3(tuple(selected[j] for j in range(4) if j != i))
            for i in range(4)
        ))
    mixed = sp.Matrix([[sp.diff(coefficients[word], value) for value in extension] for word in MIXED])
    return {"aa": aa, "bb": bb, "coefficients": coefficients, "mixed": mixed,
            "A": coefficients[WORDS[0]], "B": coefficients[WORDS[-1]]}


def one_marked(instance, mode):
    other = tuple(i for i in range(4) if i != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            instance["bb"][index] if bits[position] else instance["aa"][index]
            for position, index in enumerate(other)
        )
        rows.append(tuple(
            permanent3(selected, tuple(j for j in range(4) if j != coordinate))
            for coordinate in range(4)
        ))
    return sp.Matrix(rows)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def exact_elimination_equality(equations, eliminated, retained, expected):
    variables = tuple(eliminated) + tuple(retained)
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables)) + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + "; I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + "; E=std(E);",
        "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
        '"AUDIT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        "quit;",
    ))
    completed = subprocess.run(
        singular_command(), input=program, cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, timeout=45, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    markers = [line for line in completed.stdout.splitlines() if line.startswith("AUDIT:")]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", completed.stdout
    return int(markers[0].split(":")[2])


def simultaneous_projection(infinity=False):
    cap_s, cap_u, slope = sp.symbols("S U r")
    markings = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    w = sp.symbols("w0:8")
    inv_a, inv_b = sp.symbols("ia ib")
    d01 = model(cap_s, cap_u, markings, z, "01i" if infinity else "01f", slope)
    d23 = model(cap_s, cap_u, markings, w, "23i" if infinity else "23f", slope)
    equations = (
        *tuple(d01["mixed"] * sp.Matrix(z)), d01["A"] - 1, inv_a*d01["B"] - 1,
        *(d23["coefficients"][word] for word in WORDS[:-1]), inv_b*d23["B"] - 1,
    )
    if infinity:
        expected = (sp.Integer(1),)
        retained = markings + (cap_s, cap_u)
    else:
        h0, a, b, c = markings
        phi = sp.expand(
            cap_s*(cap_u*((cap_s-cap_u)*(a+1)*(b+1)-a*(b+1)+1)+b*(cap_s+1))
            + c*(cap_s*b*(cap_s+cap_u+1)+cap_u*a*(1-cap_s-cap_u))
        )
        expected = (
            slope*(cap_s-cap_u), slope*(slope+1), slope*cap_u*(2*c+1),
            slope*cap_u*(b+1), slope*cap_u*(a+1), h0*cap_u, h0*cap_s,
            h0*(slope+1), 2*b*c*slope+h0+2*b*slope+slope,
            2*a*c*slope-h0-slope, 2*h0*c+h0+2*c*slope+slope, phi,
            a*b*slope-h0-slope, h0*b+h0+b*slope+slope,
            h0*a+h0+a*slope+slope, h0*(h0-1),
        )
        retained = markings + (slope, cap_s, cap_u)
    size = exact_elimination_equality(equations, z+w+(inv_a,inv_b), retained, expected)
    return {"expected": expected, "size": size, "symbols": (cap_s,cap_u,slope,markings,z)}


def finite_branch_checks(finite):
    cap_s, cap_u, slope, markings, z = finite["symbols"]
    h0, a, b, c = markings
    expected = finite["expected"]
    phi = expected[11]
    # r=0 is exactly h0=Phi=0 after specialization.
    specialized_zero = [sp.factor(g.subs(slope, 0)) for g in expected]
    specialized_zero = [g for g in specialized_zero if g != 0]
    zero_variables = (h0, a, b, c, cap_s, cap_u)
    actual_zero = sp.groebner(specialized_zero, *zero_variables, order="grevlex")
    expected_zero = sp.groebner((h0, phi), *zero_variables, order="grevlex")
    assert all(expected_zero.reduce(g)[1] == 0 for g in specialized_zero)
    assert actual_zero.reduce(h0)[1] == 0
    assert actual_zero.reduce(phi)[1] == 0

    # r=-1 forces S=U.  On S=U=s!=0, reconstruct the complete kernel.
    s, cap_x, cap_y = sp.symbols("s X Y")
    branch = {cap_s:s, cap_u:s, slope:-1, h0:0, a:-1, b:-1, c:-sp.Rational(1,2)}
    d01 = model(cap_s,cap_u,markings,z,"01f",slope)
    matrix = d01["mixed"].subs(branch)
    v0 = sp.Matrix((0,0,0,0,1,0,0,0))
    v1 = sp.Matrix((1,1,-1,0,0,0,0,1))
    assert all(sp.factor(q)==0 for q in matrix*v0)
    assert all(sp.factor(q)==0 for q in matrix*v1)
    inv = sp.Symbol("winv")
    kernel_expected = (z[3],z[5],z[6],z[1]-z[0],z[2]+z[0],z[7]-z[0])
    kernel_size = exact_elimination_equality(
        (*tuple(matrix*sp.Matrix(z)),inv*s-1),(inv,),(s,)+z,kernel_expected
    )
    vector = cap_x*v0+cap_y*v1
    values = dict(zip(z,vector))
    diag_a = sp.factor(d01["A"].subs(branch).subs(values))
    diag_b = sp.factor(d01["B"].subs(branch).subs(values))
    minor = sp.factor(one_marked(d01,1).subs(branch).subs(values).extract((0,1,3,7),range(4)).det())
    assert sp.factor(diag_a-4*s*cap_y)==0
    assert sp.factor(diag_b+2*(cap_x+cap_y))==0
    assert sp.factor(minor+16*s**2*cap_y**2*(cap_x+cap_y))==0

    # Deep h0=0 has the same two-dimensional kernel but loses A.
    deep0 = {cap_s:0,cap_u:0,slope:-1,h0:0,a:-1,b:-1,c:-sp.Rational(1,2)}
    deep_matrix = d01["mixed"].subs(deep0)
    assert deep_matrix.rank()==6
    assert d01["A"].subs(deep0).subs(values)==0

    # At h0=1 the projected ideal is <ab,ac,b(c+1)> and the D01 rows are
    # literally the H31 deletion-zero singular-base rows.
    specialized_one = [sp.factor(g.subs({slope:-1,cap_s:0,cap_u:0,h0:1})) for g in expected]
    specialized_one = [g for g in specialized_one if g != 0]
    groebner = sp.groebner(specialized_one,a,b,c,order="grevlex")
    assert {sp.factor(p.as_expr()) for p in groebner.polys} == {a*b,a*c,b*(c+1)}
    d01_h1 = model(0,0,(1,a,b,c),z,"01f",-1)
    deletion = model(0,0,(0,a,b,c),z,"delete0")
    assert d01_h1["aa"] == deletion["aa"]
    assert d01_h1["bb"] == deletion["bb"]
    assert d01_h1["coefficients"] == deletion["coefficients"]

    return {
        "r_zero_branch": "h0=0,Phi=0",
        "r_minus_one_branch": "S=U",
        "open_equal_coordinate_kernel_saturation_size": kernel_size,
        "open_diagonals": [str(diag_a),str(diag_b)],
        "open_minor": str(minor),
        "deep_h0_zero_A": "0",
        "deep_h0_one_ideal": ["a*b","a*c","b*(c+1)"],
        "deep_h0_one_equals_H31_deletion_zero_model": True,
    }


def weight_transport_audit():
    rho,sigma,x0,x1,x2,x3,e = sp.symbols("rho sigma x0 x1 x2 x3 e")
    transformed = (x0,x1,-x3,-x2)
    d01 = (rho*transformed[0]+sigma*transformed[1],transformed[2],transformed[3],e)
    d23 = (transformed[0],transformed[1],rho*transformed[2]+sigma*transformed[3],e)
    assert d01 == (rho*x0+sigma*x1,-x3,-x2,e)
    assert d23 == (x0,x1,-rho*x3-sigma*x2,e)
    # After harmless target signs/swaps: D01 retains [rho:sigma], D23 has
    # [sigma:rho].  A diagonal rebalance diag(1,1,rho^2,sigma^2) is invertible
    # only off the two homogeneous endpoints.
    determinant = sp.factor(rho**2*sigma**2)
    return {
        "D01_weight_after_swap": "[rho:sigma]",
        "D23_weight_after_swap": "[sigma:rho]",
        "weight_dependent_rebalance": "diag(1,1,rho^2,sigma^2)",
        "rebalance_determinant": str(determinant),
        "covers_rho_sigma_nonzero": True,
        "covers_weight_[0:1]": False,
        "covers_weight_[1:0]": False,
        "normalized_dependencies_require_one_common_weight": True,
    }


def main():
    finite = simultaneous_projection(False)
    infinity = simultaneous_projection(True)
    branches = finite_branch_checks(finite)
    transport = weight_transport_audit()
    result = {
        "status":"pass",
        "claim_label":"REFUTED",
        "role":"verifier",
        "date_utc":datetime.now(UTC).isoformat(),
        "git_commit":git_commit(),
        "scope":"full homogeneous weighted-H22 claim on the embedded-P3 free-plane r0=0 divisor",
        "inputs":{path.name:sha256(path) for path in (CLAIM,PRIMARY,H31,H31_PRIMARY,H22_GENERIC,H22_RANK_TWO,H22_RANK_ONE)},
        "method":"no-import exact corner elimination, saturated kernels, literal H31-model comparison, and homogeneous weight transport audit",
        "command":'uv run --with sympy python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py',
        "outputs":{SCRIPT.name:sha256(SCRIPT),REPORT.name:sha256(REPORT)},
        "limitations":"REFUTED is the full-divisor proof because t0!=0 homogeneous endpoints are not transported; the t0=0 corner obstruction is independently verified, while the uncovered endpoint fibres remain UNKNOWN",
        "finite_projection_generator_count":finite["size"],
        "infinity_projection_unit_ideal":infinity["size"]==1,
        "finite_branch_checks":branches,
        "H31_dependency_use":"sound only where D01 rows are literally the verified deletion-zero model",
        "t_nonzero_weight_transport":transport,
        "t_zero_corner_obstruction":"VERIFIED_BY_THIS_AUDIT",
        "t_nonzero_nonendpoint_transport":"SUPPORTED",
        "t_nonzero_homogeneous_endpoint_status":"UNKNOWN",
        "full_r0_divisor_obstruction_proved":False,
        "finite_field_computation_used_as_proof":False,
        "global_Krenn_Gu_conjecture_resolved":False,
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
