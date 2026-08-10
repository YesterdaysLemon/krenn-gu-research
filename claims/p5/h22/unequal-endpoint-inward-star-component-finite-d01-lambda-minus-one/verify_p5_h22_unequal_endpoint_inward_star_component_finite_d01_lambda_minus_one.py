#!/usr/bin/env python3
"""Exact finite-D01 lambda=-1 analysis for component twenty-five."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import time

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/unequal-endpoint-inward-star")
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-endpoint-inward-star")

from verify_p5_h22_unequal_endpoint_inward_star_component_partial import coordinates
from verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction import (
    marked,
    pure_basis,
)



WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def module_check(alpha, beta, extensions, hypersurface):
    tensor = coordinates(alpha, beta, extensions, "D01", "finite", sp.Integer(-1))
    rows = {
        word: tuple(sp.diff(tensor[word], extension) for extension in extensions)
        for word in WORDS
    }
    generators = ",".join("[" + ",".join(map(sg, rows[word])) + "]" for word in MIXED)
    alpha_text = "[" + ",".join(map(sg, rows[WORDS[0]])) + "]"
    beta_text = "[" + ",".join(map(sg, rows[WORDS[-1]])) + "]"
    program = "\n".join(
        (
            "ring r=(0,e,j,s),(k,h0,h1,h2,h3),dp;",
            "ideal Q=" + sg(hypersurface) + ";",
            "qring R=std(Q);",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "vector a=" + alpha_text + "; vector b=" + beta_text + ";",
            "vector ar=reduce(a,M); vector br=reduce(b,M);",
            '"RESULT:"+string(ar==0)+":"+string(br==0)+":"+string(size(M));',
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
    assert len(markers) == 1, completed.stdout
    _, alpha_zero, beta_zero, size = markers[0].split(":")
    return {
        "all_alpha_in_mixed_module": alpha_zero == "1",
        "all_beta_in_mixed_module": beta_zero == "1",
        "module_basis_size": int(size),
    }


def main():
    started = time.perf_counter()
    e, j, k, s = sp.symbols("e j k s")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    pivot = e * j + k**2
    hypersurface = sp.expand(pivot * (1 + e * j * s**2) - (e + j) ** 2)
    alpha, beta = pure_basis(e, j, k, s)
    active = marked(alpha, beta, shifts)
    module = module_check(alpha, active, extensions, hypersurface)
    assert module == {
        "all_alpha_in_mixed_module": False,
        "all_beta_in_mixed_module": True,
        "module_basis_size": 12,
    }
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D01",
                "weight": "lambda=-1",
                "row_module": module,
                "all_markings_covered": True,
                "lambda_minus_one_binary_incidence_empty": True,
                "finite_D01_residual_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "special_component_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
