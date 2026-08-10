#!/usr/bin/env python3
"""Exact generic weighted-H22 obstruction for component twenty-four."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model, project

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/split-center-mixed-star")

from krenn_gu.p5_marked_basis import one_marked_map  # noqa: E402
from verify_p5_h31_split_center_mixed_star_component_generic_obstruction import (  # noqa: E402
    rows,
    shifted,
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def permanent4(square):
    return sp.expand(
        sum(
            sp.prod(square[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS
        )
    )


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def sg(expression):
    return str(sp.expand(sp.fraction(sp.cancel(expression))[0])).replace("**", "^")


def clear_row(entries):
    multiplier = sp.prod(sp.fraction(sp.together(entry))[1] for entry in entries)
    return tuple(
        sp.expand(sp.fraction(sp.cancel(multiplier * entry))[0]) for entry in entries
    )


def run(program, timeout=500):
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
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    return [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]


def model(direction, chart, marking, slope, k, s, t, z):
    alpha, canonical = rows(k, s, t)
    beta = shifted(canonical, alpha, marking)
    contraction = build_model(alpha, beta, z, direction, chart, slope)
    projected_alpha = tuple(
        project(alpha[index], z[index], direction, chart, slope) for index in range(4)
    )
    projected_beta = tuple(
        project(beta[index], z[4 + index], direction, chart, slope)
        for index in range(4)
    )
    return contraction, projected_alpha, projected_beta


def row_module(direction, chart, alpha, beta, z, slope):
    contraction = build_model(alpha, beta, z, direction, chart, slope)
    mixed = sp.Matrix(
        [[sp.diff(value, variable) for variable in z] for value in contraction["mixed"]]
    )
    diagonal_alpha = tuple(sp.diff(contraction["A"], variable) for variable in z)
    diagonal_beta = tuple(sp.diff(contraction["B"], variable) for variable in z)
    generators = ",".join(
        "["
        + ",".join(map(sg, clear_row(tuple(mixed[row, col] for col in range(8)))))
        + "]"
        for row in range(14)
    )
    a_text = "[" + ",".join(map(sg, clear_row(diagonal_alpha))) + "]"
    b_text = "[" + ",".join(map(sg, clear_row(diagonal_beta))) + "]"
    ring_variables = "h0,h1,h2,h3" + (",lambda" if chart == "finite" else "")
    program = "\n".join(
        (
            f"ring R=(0,k,s,t),({ring_variables}),dp;",
            "option(redSB);",
            f"module M={generators}; M=std(M);",
            f"vector a={a_text}; vector b={b_text};",
            "vector ar=reduce(a,M); vector br=reduce(b,M);",
            '"RESULT:"+string(ar==0)+":"+string(br==0)+":"+string(size(M));',
            "quit;",
        )
    )
    marker = run(program, 180)[0].split(":")
    return {
        "direction": direction,
        "chart": chart,
        "all_alpha_in_mixed_module": marker[1] == "1",
        "all_beta_in_mixed_module": marker[2] == "1",
        "module_basis_size": int(marker[3]),
    }


def finite_d23_primes(k, s, t, h, slope):
    quadratic = sp.expand(
        (k**3 * s**3 * t + k**2 * s**2 - k * s * t - 1) * slope**2
        + (-4 * k**3 * s**3 * t - 2 * k**2 * s**2 * t**2 - 2) * slope
        + 3 * k**3 * s**3 * t
        + 2 * k**2 * s**2 * t**2
        + 3 * k**2 * s**2
        + k * s * t
        - 1
    )
    h3_relation = sp.expand(
        2 * s * (k**2 * s**2 - 1) * h[3]
        + (k**4 * s**4 * t**2 - k**2 * s**2 * t**2 - k**2 * s**2 + 1) * slope
        - 3 * k**4 * s**4 * t**2
        - 2 * k**3 * s**3 * t**3
        + 4 * k**3 * s**3 * t
        + k**2 * s**2 * t**2
        + k**2 * s**2
        - 2 * k * s * t
        + 1
    )
    h2_relation = sp.expand(
        k * (t**2 - 1) * (k * s * t + 1) * h[2]
        + (k * s * t - 1) * h[3]
        + k * t * (1 - k * s * t)
    )
    h1_relation = sp.expand(
        (1 - k**2 * s**2) * h[3] * slope
        + 2 * k**3 * s * (t**2 - 1) * h[1]
        + (k**2 * s**2 + 2 * k * s * t + 1) * h[3]
        + k * (k**2 * s**2 * t - t) * slope
        + k * (-(k**2) * s**2 * t - 2 * k * s - t)
    )
    quadratic_prime = (quadratic, h3_relation, h2_relation, h1_relation, h[0])
    linear_prime = (h[3] - k * t, h[2], k * h[1] + 1, h[0])
    return quadratic_prime, linear_prime


def projection(direction, chart, expected_size, primes, k, s, t, h, z, slope):
    inverse = sp.Symbol("u")
    alpha, canonical = rows(k, s, t)
    marked = shifted(canonical, alpha, h)
    contraction = build_model(alpha, marked, z, direction, chart, slope)
    equations = (
        *contraction["mixed"],
        contraction["A"] - 1,
        inverse * contraction["B"] - 1,
    )
    eliminated = z + (inverse,)
    retained = h + ((slope,) if chart == "finite" else ())
    variables = eliminated + retained
    lines = [
        'LIB "primdec.lib";',
        "ring R=(0,k,s,t),("
        + ",".join(map(str, variables))
        + f"),(dp(9),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(sg(value) for value in equations) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "list L=minAssGTZ(J);",
    ]
    for expected_index, prime in enumerate(primes, start=1):
        lines.extend(
            (
                f"ideal P{expected_index}="
                + ",".join(sg(value) for value in prime)
                + ";",
                f"P{expected_index}=std(P{expected_index});",
            )
        )
        comparisons = []
        for actual_index in range(1, len(primes) + 1):
            lines.extend(
                (
                    f"ideal Q{expected_index}_{actual_index}=std(L[{actual_index}]);",
                    f"ideal X{expected_index}_{actual_index}=simplify(reduce(Q{expected_index}_{actual_index},P{expected_index}),2);",
                    f"ideal Y{expected_index}_{actual_index}=simplify(reduce(P{expected_index},Q{expected_index}_{actual_index}),2);",
                )
            )
            comparisons.append(
                f"((size(X{expected_index}_{actual_index})==0)&&(size(Y{expected_index}_{actual_index})==0))"
            )
        lines.append(f"int H{expected_index}=" + "+".join(comparisons) + ";")
    hit_text = '+":"+'.join(f"string(H{index})" for index in range(1, len(primes) + 1))
    lines.extend(
        (
            '"RESULT:"+string(size(J))+":"+string(size(L))+":"+' + hit_text + ";",
            "quit;",
        )
    )
    marker = run("\n".join(lines), 600)[0].split(":")
    assert int(marker[1]) == expected_size
    assert int(marker[2]) == len(primes)
    assert all(value == "1" for value in marker[3:])
    return {
        "direction": direction,
        "chart": chart,
        "projection_basis_size": expected_size,
        "minimal_prime_count": len(primes),
        "minimal_primes": [
            [str(sp.factor(value)) for value in prime] for prime in primes
        ],
    }


def unit_branch(label, direction, chart, marking, branch, free, k, s, t, z, slope):
    inverse = sp.Symbol("u")
    contraction, alpha, beta = model(direction, chart, marking, slope, k, s, t, z)
    submatrix = one_marked_map(0, alpha, beta).extract((0, 1, 3, 7), range(4))
    variables = z + (inverse,) + free
    denominators = {
        sp.factor(sp.fraction(sp.together(value))[1]) for value in submatrix
    }
    matrix_multiplier = sp.prod(denominators)
    scaled_submatrix = tuple(
        sp.cancel(matrix_multiplier * value) for value in submatrix
    )
    assert all(sp.fraction(value)[1] == 1 for value in scaled_submatrix)
    entries = ",".join(sg(value) for value in scaled_submatrix)
    equations = (
        *contraction["mixed"],
        contraction["A"] - 1,
        inverse * contraction["B"] - 1,
        *branch,
    )
    program = "\n".join(
        (
            "ring R=(0,k,s,t),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            f"matrix N[4][4]={entries};",
            "poly f=det(N);",
            "ideal I=" + ",".join(sg(value) for value in equations) + ",f;",
            "I=slimgb(I);",
            '"RESULT:"+string(reduce(1,I)==0)+":"+string(size(I));',
            "quit;",
        )
    )
    markers = run(program, 600)
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", markers
    return {
        "branch": label,
        "direction": direction,
        "chart": chart,
        "minor": "N0[0137]",
        "unit_ideal": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def main():
    started = time.perf_counter()
    k, s, t, slope, free_h = sp.symbols("k s t lambda H")
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    alpha, beta = rows(k, s, t)
    pure = {
        word: sp.factor(
            permanent4(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[WORDS[-1]] - 4 * (k * s * t - 1)) == 0
    assert all(value == 0 for word, value in pure.items() if word != WORDS[-1])

    marked = shifted(beta, alpha, h)
    modules = [
        row_module(
            direction, chart, alpha, marked, z, slope if chart == "finite" else None
        )
        for direction in ("D01", "D23")
        for chart in ("finite", "infinity")
    ]
    assert all(
        not result["all_alpha_in_mixed_module"]
        and not result["all_beta_in_mixed_module"]
        for result in modules
    )

    quadratic_prime, linear_prime = finite_d23_primes(k, s, t, h, slope)
    q3b_h2 = -(k**2 * s**2 * t**2 - 1) / (2 * t * (k**2 * s**2 - 1))
    projections = [
        projection(
            "D01", "finite", 3, ((h[3] - k * t, h[2], h[0]),), k, s, t, h, z, slope
        ),
        projection(
            "D01",
            "infinity",
            4,
            ((h[3] - k * t, h[2], k * (t - 1) * h[1] + 2 * k * s * t - t - 1, h[0]),),
            k,
            s,
            t,
            h,
            z,
            None,
        ),
        projection(
            "D23", "finite", 7, (quadratic_prime, linear_prime), k, s, t, h, z, slope
        ),
        projection(
            "D23",
            "infinity",
            4,
            (
                (
                    h[3] - k * t,
                    2 * t * (k**2 * s**2 - 1) * h[2] + k**2 * s**2 * t**2 - 1,
                    h[1] - s * t,
                    h[0],
                ),
                linear_prime,
            ),
            k,
            s,
            t,
            h,
            z,
            None,
        ),
    ]

    units = [
        unit_branch(
            "D01_finite",
            "D01",
            "finite",
            (0, free_h, 0, k * t),
            (),
            (free_h, slope),
            k,
            s,
            t,
            z,
            slope,
        ),
        unit_branch(
            "D01_infinity_q1",
            "D01",
            "infinity",
            (0, (t + 1 - 2 * k * s * t) / (k * (t - 1)), 0, k * t),
            (),
            (),
            k,
            s,
            t,
            z,
            None,
        ),
        unit_branch(
            "D23_finite_linear",
            "D23",
            "finite",
            (0, -1 / k, 0, k * t),
            (),
            (slope,),
            k,
            s,
            t,
            z,
            slope,
        ),
        unit_branch(
            "D23_finite_quadratic",
            "D23",
            "finite",
            h,
            quadratic_prime,
            h + (slope,),
            k,
            s,
            t,
            z,
            slope,
        ),
        unit_branch(
            "D23_infinity_q3a",
            "D23",
            "infinity",
            (0, -1 / k, 0, k * t),
            (),
            (),
            k,
            s,
            t,
            z,
            None,
        ),
        unit_branch(
            "D23_infinity_q3b",
            "D23",
            "infinity",
            (0, s * t, q3b_h2, k * t),
            (),
            (),
            k,
            s,
            t,
            z,
            None,
        ),
    ]
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(k,s,t)",
                "component": 24,
                "pure_support": {"1111": "4*(k*s*t - 1)"},
                "row_modules": modules,
                "projections": projections,
                "branch_unit_ideals": units,
                "D01_pair_orbit_empty": True,
                "D23_pair_orbit_empty": True,
                "generic_weighted_H22_fibre_empty": True,
                "finite_field_proof_used": False,
                "special_component_fibres_closed": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
