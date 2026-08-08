#!/usr/bin/env python3
"""Verify generic-weight emptiness of the finite-D01 A branch."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import time

import sympy as sp

from verify_p5_h22_unequal_endpoint_inward_star_component_partial import coordinates
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-endpoint-inward-star")

from verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction import (
    pure_basis,
)

WORDS = tuple(itertools.product((0, 1), repeat=4))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def main():
    started = time.perf_counter()
    e, j, k, s, slope, w = sp.symbols("e j k s lambda w")
    z0, z1, _, z3, _, z5, z6, z7 = sp.symbols("z0:8")
    pivot = e * j + k**2
    cross = e + j
    leading = 1 + e * j * s**2
    hypersurface = sp.expand(pivot * leading - cross**2)
    extensions = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)
    alpha, beta = pure_basis(e, j, k, s)
    tensor = coordinates(alpha, beta, extensions, "D01", "finite", slope)

    empty = tensor[WORDS[0]]
    c1 = tensor[(0, 1, 0, 0)]
    c2 = tensor[(0, 0, 1, 0)]
    c3 = tensor[(0, 0, 0, 1)]
    branch_a = 1 + 2 * (slope - 1) * (e**2 - k**2) * pivot * z3
    linear_residual = (
        2 * k * cross**2 * (e - j) * (slope - 1) * ((slope + 1) * w + z6) + j * leading
    )
    linear_ideal = (
        tensor[(1, 0, 1, 0)],
        tensor[(1, 0, 1, 1)],
        tensor[(1, 1, 1, 0)],
        empty - 1,
        branch_a,
        linear_residual,
    )
    segre_23 = tensor[(0, 0, 1, 1)] * empty - c2 * c3
    segre_123 = tensor[(0, 1, 1, 1)] * empty**2 - c1 * c2 * c3
    program = "\n".join(
        (
            "ring r=(0,e,j,s,lambda),(k,z0,z1,z3,z5,z6,z7,w),dp;",
            "ideal Q=" + sg(hypersurface) + ";",
            "qring R=std(Q);",
            "option(redSB);",
            "ideal L=" + ",".join(map(sg, linear_ideal)) + "; L=std(L);",
            "poly r23=reduce(" + sg(segre_23) + ",L);",
            "poly r123=reduce(" + sg(segre_123) + ",L);",
            "ideal J=L,r23,r123; J=std(J);",
            '"RESULT:"+string(reduce(1,J)==0)+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:1"], completed.stdout

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_exceptional_weight_residual",
                "field": "C(e,j,s,lambda)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D01",
                "input_branch": "ordinary A=0",
                "last_segre_equations": ["{2,3}", "{1,2,3}"],
                "reduced_standard_basis": ["1"],
                "A_branch_generic_weight_empty": True,
                "exceptional_weight_divisor_extracted": False,
                "A_branch_all_weights_closed": False,
                "B_branch_closed": False,
                "finite_D01_residual_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
