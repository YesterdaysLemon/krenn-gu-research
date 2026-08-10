#!/usr/bin/env python3
"""Verify exact partial weighted-H22 results for component twenty-three."""

from __future__ import annotations

import functools
import json
import shutil
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/common-center-kernel-star")

from verify_p5_h31_common_center_kernel_star_component_generic_obstruction import (
    rows,
    shifted,
)




def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def coefficient_row(expression, extension):
    entries = [sp.diff(expression, variable) for variable in extension]
    denominators = [
        sp.factor(sp.fraction(sp.together(entry))[1]) for entry in entries
    ]
    multiplier = functools.reduce(sp.lcm, denominators, sp.Integer(1))
    cleared = [sp.cancel(multiplier * entry) for entry in entries]
    assert all(sp.fraction(entry)[1] == 1 for entry in cleared)
    return "[" + ",".join(sg(sp.expand(entry)) for entry in cleared) + "]"


def module_certificate(label, alpha, beta, chart, coefficient_ring, variables, expected):
    extension = sp.symbols("x0:8")
    slope = sp.Symbol("lam") if chart == "finite" else None
    d01 = build_model(alpha, beta, extension, "D01", chart, slope)
    d23 = build_model(alpha, beta, extension, "D23", chart, slope)
    generators = ",".join(
        coefficient_row(expression, extension)
        for expression in (*d01["mixed"], *d23["mixed"])
    )
    diagonals = tuple(
        coefficient_row(expression, extension)
        for expression in (d01["A"], d23["A"], d01["B"], d23["B"])
    )
    lines = [
        f"ring R={coefficient_ring},({','.join(variables)}),dp;",
        "option(redSB);",
        "module M=" + generators + ";",
        "M=std(M);",
        "module E=" + ",".join(expected) + "; E=std(E);",
        "module ME=simplify(reduce(M,E),2);",
        "module EM=simplify(reduce(E,M),2);",
        "vector a=" + diagonals[0] + ";",
        "vector b=" + diagonals[1] + ";",
        "vector c=" + diagonals[2] + ";",
        "vector d=" + diagonals[3] + ";",
        (
            'print("RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"'
            '+string(reduce(a,M)==0)+":"+string(reduce(b,M)==0)+":"'
            '+string(reduce(c,M)==0)+":"+string(reduce(d,M)==0)+":"'
            '+string(size(M)));'
        ),
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), text=True,
        capture_output=True, timeout=180, check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(markers) == 1, (label, completed.stdout)
    fields = markers[0].split(":")[1:]
    return {
        "label": label,
        "module_equality": fields[0] == "1",
        "diagonal_membership_A01_A23_B01_B23": [field == "1" for field in fields[1:5]],
        "standard_basis_size": int(fields[5]),
    }


def main():
    r, t = sp.symbols("r t")
    h = sp.symbols("h0:4")
    alpha, canonical = rows(r, t)

    finite_expected = (
        "gen(1)", "gen(2)", "gen(3)", "gen(4)",
        "gen(6)", "gen(7)", "gen(8)", "(lam-1)*gen(5)",
    )
    infinity_expected = tuple(f"gen({index})" for index in range(1, 9))

    infinity_marked = shifted(canonical, alpha, h)
    generic_infinity = module_certificate(
        "generic_weight_infinity_all_markings",
        alpha,
        infinity_marked,
        "infinity",
        "(0,r,t)",
        ("h0", "h1", "h2", "h3"),
        infinity_expected,
    )
    assert generic_infinity == {
        "label": "generic_weight_infinity_all_markings",
        "module_equality": True,
        "diagonal_membership_A01_A23_B01_B23": [True, True, True, True],
        "standard_basis_size": 8,
    }

    generic_unmarked_finite = module_certificate(
        "generic_finite_canonical_marking",
        alpha,
        canonical,
        "finite",
        "(0,r,t)",
        ("lam",),
        finite_expected,
    )
    assert generic_unmarked_finite == {
        "label": "generic_finite_canonical_marking",
        "module_equality": True,
        "diagonal_membership_A01_A23_B01_B23": [True, True, True, False],
        "standard_basis_size": 8,
    }

    slice_alpha, slice_canonical = rows(r, sp.Integer(3))
    slice_marked = shifted(slice_canonical, slice_alpha, h)
    finite_slice = module_certificate(
        "finite_all_markings_t_equals_3_slice",
        slice_alpha,
        slice_marked,
        "finite",
        "(0,r)",
        ("h0", "h1", "h2", "h3", "lam"),
        finite_expected,
    )
    assert finite_slice == {
        "label": "finite_all_markings_t_equals_3_slice",
        "module_equality": True,
        "diagonal_membership_A01_A23_B01_B23": [True, True, True, False],
        "standard_basis_size": 8,
    }

    print(json.dumps({
        "status": "pass",
        "field": "characteristic zero",
        "component": 23,
        "generic_weight_infinity_closed": True,
        "generic_finite_canonical_marking_closed": True,
        "finite_all_markings_t_equals_3_slice_closed": True,
        "generic_finite_all_markings_closed": False,
        "generic_finite_all_markings_status": "UNKNOWN",
        "certificates": [generic_infinity, generic_unmarked_finite, finite_slice],
        "finite_field_proof_used": False,
        "global_conjecture_resolved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
