#!/usr/bin/env python3
"""Exact finite-cover valuative obstruction near component 19's zero base."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp

ROOT = HERE
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_ZERO_BASE_VALUATIVE_FINITE_COVER_CANDIDATE.md"
CERTIFICATE = (
    ROOT / "p5_h22_component19_zero_base_valuative_finite_cover_certificate.json"
)
INPUTS = tuple(REPO_ROOT / name for name in (
    "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md",
    "P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md",
    "P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md",
    "P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md",
))

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
ALPHA_WORD = WORDS[0]
BETA_WORD = WORDS[-1]
OPEN_TRIPLES = (
    ("A01", "B01", "A23"),
    ("A01", "B01", "B23"),
    ("A23", "B23", "A01"),
    ("A23", "B23", "B01"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=15,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.expand(sum(row[i] for row in rows)) for i in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not (mask >> column) & 1:
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = {mask: sp.expand(value) for mask, value in following.items()}
    return sp.factor(states[(1 << len(rows)) - 1])


def assert_zero(value):
    reduced = sp.cancel(value)
    assert reduced == 0, sp.factor(reduced)


def p_chart_rows(base, normal, phi, shifts):
    """Exact blow-up chart p=base, q-phi=base*normal."""
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    # If v=Abar+pB and u=Bbar+qB, then u-normal*v cancels
    # every base term and is a regular exact pure row on the blow-up.
    alpha = (
        add(bbar, scale(phi, cap_b), scale(-normal, abar)),
        cap_b, bbar, abar,
    )
    unmarked_beta = (
        add(abar, scale(base, cap_b)), cap_a, cap_a,
        add(cap_b, scale(phi, bbar)),
    )
    beta = tuple(
        add(unmarked_beta[i], scale(shifts[i], alpha[i])) for i in range(4)
    )
    return alpha, beta


def project(row, extension, contraction, weight_chart, slope):
    if weight_chart == "finite":
        if contraction == "D01":
            return (slope * row[0] + row[1], row[2], row[3], extension)
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if contraction == "D01":
        return (row[0], row[2], row[3], extension)
    return (row[0], row[1], row[2], extension)


def contraction_model(
    base, normal, phi, shifts, extensions, contraction, weight_chart, slope,
):
    alpha, beta = p_chart_rows(base, normal, phi, shifts)
    alpha_rows = tuple(
        project(alpha[i], extensions[i], contraction, weight_chart, slope)
        for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], contraction, weight_chart, slope)
        for i in range(4)
    )
    coefficients = {
        word: permanent(tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        ))
        for word in WORDS
    }
    mixed_matrix = sp.Matrix([
        [sp.diff(coefficients[word], value) for value in extensions]
        for word in MIXED
    ])
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed_matrix": mixed_matrix,
        "A": coefficients[ALPHA_WORD],
        "B": coefficients[BETA_WORD],
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def projected_ideal(
    label, equations, eliminated, retained, expected,
):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=0,(" + ",".join(map(str, variables)) + ")"
        + f",(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        "ideal E=" + ",".join(map(singular, expected)) + "; E=std(E);",
        "ideal JE=simplify(reduce(J,E),2);",
        "ideal EJ=simplify(reduce(E,J),2);",
        '"CODEX_RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
        "quit;",
    ]
    completed = subprocess.run(
        singular_command(), input="\n".join(lines), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
        timeout=120, check=False,
    )
    markers = [
        line for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", (
        label, completed.stdout
    )
    return {
        "label": label,
        "projected_ideal": [str(sp.factor(value)) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def shared_projection_atlas():
    base, normal, phi, slope = sp.symbols("z n phi lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverses = sp.symbols("u0:2")
    open_inverse = sp.Symbol("o")
    output = []
    expected_finite = {
        OPEN_TRIPLES[0]: (sp.Integer(1),),
        OPEN_TRIPLES[1]: (sp.Integer(1),),
        OPEN_TRIPLES[2]: (
            slope + 1, shifts[3], shifts[2], shifts[1],
            shifts[0] * normal - 1,
            normal * phi * base + phi**2 - 1,
            shifts[0] * phi**2 + phi * base - shifts[0],
        ),
        OPEN_TRIPLES[3]: (
            slope - 1, shifts[3], shifts[1], shifts[0] * normal - 1,
        ),
    }
    for weight_chart in ("finite", "infinity"):
        d01 = contraction_model(
            base, normal, phi, shifts, extensions,
            "D01", weight_chart, slope,
        )
        d23 = contraction_model(
            base, normal, phi, shifts, extensions,
            "D23", weight_chart, slope,
        )
        diagonals = {
            "A01": d01["A"], "B01": d01["B"],
            "A23": d23["A"], "B23": d23["B"],
        }
        for open_triple in OPEN_TRIPLES:
            equations = (
                *(d01["coefficients"][word] for word in MIXED),
                *(d23["coefficients"][word] for word in MIXED),
                diagonals[open_triple[0]] - 1,
                inverses[0] * diagonals[open_triple[1]] - 1,
                inverses[1] * diagonals[open_triple[2]] - 1,
                open_inverse * base * normal * phi - 1,
            )
            retained = shifts + (
                (slope,) if weight_chart == "finite" else ()
            ) + (normal, phi, base)
            expected = (
                expected_finite[open_triple]
                if weight_chart == "finite" else (sp.Integer(1),)
            )
            output.append(projected_ideal(
                f"p_chart_{weight_chart}_{'_'.join(open_triple)}",
                equations,
                extensions + inverses + (open_inverse,),
                retained, expected,
            ))
    return output


def endpoint_projection_atlas():
    base, normal, slope = sp.symbols("z n lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverses = sp.symbols("u0:2")
    open_inverse = sp.Symbol("o")
    output = []
    for epsilon in (1, -1):
        for weight_chart in ("finite", "infinity"):
            d01 = contraction_model(
                base, normal, sp.Integer(epsilon), shifts, extensions,
                "D01", weight_chart, slope,
            )
            d23 = contraction_model(
                base, normal, sp.Integer(epsilon), shifts, extensions,
                "D23", weight_chart, slope,
            )
            diagonals = {
                "A01": d01["A"], "B01": d01["B"],
                "A23": d23["A"], "B23": d23["B"],
            }
            for open_triple in OPEN_TRIPLES:
                equations = (
                    *(d01["coefficients"][word] for word in MIXED),
                    *(d23["coefficients"][word] for word in MIXED),
                    diagonals[open_triple[0]] - 1,
                    inverses[0] * diagonals[open_triple[1]] - 1,
                    inverses[1] * diagonals[open_triple[2]] - 1,
                    open_inverse * base * normal - 1,
                )
                retained = shifts + (
                    (slope,) if weight_chart == "finite" else ()
                ) + (normal, base)
                expected = (
                    (slope - 1, shifts[3], shifts[1], shifts[0] * normal - 1)
                    if weight_chart == "finite"
                    and open_triple == OPEN_TRIPLES[3]
                    else (sp.Integer(1),)
                )
                output.append(projected_ideal(
                    f"phi={epsilon}_{weight_chart}_{'_'.join(open_triple)}",
                    equations,
                    extensions + inverses + (open_inverse,),
                    retained, expected,
                ))
    return output


def full_one_marked_map(alpha, beta, extension, contraction, slope, mode):
    full_planes = tuple(
        (tuple(alpha[i]) + (extension[i],), tuple(beta[i]) + (extension[4 + i],))
        for i in range(4)
    )

    def restrict(row):
        if contraction == "D01":
            return (slope * row[0] + row[1], row[2], row[3], row[4])
        return (row[0], row[1], slope * row[2] + row[3], row[4])

    other_modes = tuple(i for i in range(4) if i != mode)
    basis = tuple(
        tuple(sp.Integer(i == j) for j in range(5)) for i in range(5)
    )
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        fixed = tuple(
            restrict(full_planes[source][bits[position]])
            for position, source in enumerate(other_modes)
        )
        rows.append([
            permanent(fixed + (restrict(basis_row),)) for basis_row in basis
        ])
    return sp.Matrix(rows)


def target_local_certificates():
    base, normal, phi, marking = sp.symbols("z n phi t", nonzero=True)
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    branch_substitution = {
        shifts[0]: 1 / normal, shifts[1]: 0,
        shifts[2]: marking, shifts[3]: 0,
    }
    d01 = contraction_model(
        base, normal, phi, shifts, extensions, "D01", "finite", sp.Integer(1)
    )
    d23 = contraction_model(
        base, normal, phi, shifts, extensions, "D23", "finite", sp.Integer(1)
    )
    combined = d01["mixed_matrix"].col_join(d23["mixed_matrix"]).subs(
        branch_substitution
    )
    rank_rows = (1, 2, 4, 10, 12, 15)
    rank_columns = (0, 1, 2, 3, 6, 7)
    rank_witness = sp.factor(
        combined.extract(rank_rows, rank_columns).det()
    )
    assert_zero(
        rank_witness
        - 4096 * normal * phi * base**2 * (phi - 1) * (phi + 1)
    )
    cap_c, cap_d = sp.symbols("C D")
    vector_c = sp.Matrix((0, -1 / base, phi / base, 0, 1, 0, 0, 0))
    vector_d = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    for vector in (vector_c, vector_d):
        assert all(sp.factor(value) == 0 for value in combined * vector)
    extension = cap_c * vector_c + cap_d * vector_d
    extension_substitution = dict(zip(extensions, extension, strict=True))
    generic_diagonals = tuple(sp.factor(value.subs(
        branch_substitution
    ).subs(extension_substitution)) for value in (
        d01["A"], d01["B"], d23["A"], d23["B"],
    ))
    expected_diagonals = (
        0,
        4 * (base * cap_d - phi * marking * cap_c),
        4 * cap_c * normal * phi / base,
        4 * cap_c,
    )
    for actual, expected in zip(generic_diagonals, expected_diagonals, strict=True):
        assert_zero(actual - expected)
    alpha, unmarked_beta = p_chart_rows(base, normal, phi, (0, 0, 0, 0))
    beta = tuple(
        add(unmarked_beta[i], scale(branch_substitution[shifts[i]], alpha[i]))
        for i in range(4)
    )
    generic_marked = full_one_marked_map(
        alpha, beta, extension, "D01", sp.Integer(1), 3
    )
    generic_minor = sp.factor(
        generic_marked.extract((1, 2, 5, 7), (0, 2, 3, 4)).det()
    )
    assert_zero(
        generic_minor
        + 64 * cap_c * (base * cap_d - phi * marking * cap_c)**2 / base
    )

    # Hidden finite branch: lambda=-1 and q*phi=1.
    special_base = (1 - phi**2) / (normal * phi)
    special_shifts = {shifts[0]: 1 / normal, shifts[1]: 0,
                      shifts[2]: 0, shifts[3]: 0}
    s01 = contraction_model(
        special_base, normal, phi, shifts, extensions,
        "D01", "finite", sp.Integer(-1),
    )
    s23 = contraction_model(
        special_base, normal, phi, shifts, extensions,
        "D23", "finite", sp.Integer(-1),
    )
    special_combined = s01["mixed_matrix"].col_join(
        s23["mixed_matrix"]
    ).subs(special_shifts)
    special_rank_rows = (0, 1, 3, 19, 20)
    special_rank_columns = (0, 1, 3, 5, 6)
    special_rank_witness = sp.factor(
        special_combined.extract(
            special_rank_rows, special_rank_columns
        ).det()
    )
    assert_zero(special_rank_witness + 1024 * normal * phi**3)
    vectors = (
        sp.Matrix((0, 1 / phi, 1, 0, 0, 0, 0, 0)),
        sp.Matrix((0, 0, 0, 0, 1, 0, 0, 0)),
        sp.Matrix((-1 / phi, 0, 0, 0, 0, 0, 0, 1)),
    )
    for vector in vectors:
        assert all(sp.factor(value) == 0 for value in special_combined * vector)
    c0, c1, c2 = sp.symbols("c0:3")
    special_extension = sum(
        (coefficient * vector for coefficient, vector in zip(
            (c0, c1, c2), vectors, strict=True
        )), sp.zeros(8, 1)
    )
    special_substitution = dict(zip(
        extensions, special_extension, strict=True
    ))
    special_diagonals = tuple(sp.factor(value.subs(
        special_shifts
    ).subs(special_substitution)) for value in (
        s01["A"], s01["B"], s23["A"], s23["B"],
    ))
    expected_special_diagonals = (
        -4 * c0 * (phi - 1) * (phi + 1) / phi,
        0,
        -4 * c0 * normal / phi,
        -4 * (c1 * normal * phi + c2) / normal,
    )
    for actual, expected in zip(
        special_diagonals, expected_special_diagonals, strict=True
    ):
        assert_zero(actual - expected)
    special_alpha, special_unmarked = p_chart_rows(
        special_base, normal, phi, (0, 0, 0, 0)
    )
    special_beta = tuple(
        add(special_unmarked[i], scale(special_shifts[shifts[i]], special_alpha[i]))
        for i in range(4)
    )
    special_marked = full_one_marked_map(
        special_alpha, special_beta, special_extension,
        "D23", sp.Integer(-1), 3,
    )
    special_minor = sp.factor(
        special_marked.extract((0, 1, 3, 7), (0, 1, 2, 4)).det()
    )
    assert_zero(
        special_minor
        + 64 * c0**2 * (c1 * normal * phi + c2) / phi**3
    )

    return {
        "generic_lambda_one": {
            "scope_open": "z*n*phi*(phi^2-1)!=0",
            "combined_rank": 6,
            "rank_witness": str(rank_witness),
            "kernel": [[str(sp.factor(value)) for value in vector]
                       for vector in (vector_c, vector_d)],
            "diagonals_A01_B01_A23_B23": [str(value) for value in generic_diagonals],
            "genuine_open": "C*n*phi*(z*D-phi*t*C)!=0",
            "D01_mode3_minor": str(generic_minor),
            "target_local_obstructed": True,
        },
        "hidden_qphi_one_lambda_minus_one": {
            "base_relation": "z=(1-phi^2)/(n*phi)",
            "combined_rank": 5,
            "rank_witness": str(special_rank_witness),
            "kernel": [[str(sp.factor(value)) for value in vector]
                       for vector in vectors],
            "diagonals_A01_B01_A23_B23": [str(value) for value in special_diagonals],
            "genuine_open": "c0*n*(phi^2-1)*(c1*n*phi+c2)!=0",
            "D23_mode3_minor": str(special_minor),
            "target_local_obstructed": True,
        },
    }


def endpoint_target_certificates():
    base, normal, marking = sp.symbols("z n t", nonzero=True)
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    cap_x, cap_y, cap_z = sp.symbols("X Y Z")
    output = {}
    for epsilon in (1, -1):
        branch = {shifts[0]: 1 / normal, shifts[1]: 0,
                  shifts[2]: marking, shifts[3]: 0}
        d01 = contraction_model(
            base, normal, sp.Integer(epsilon), shifts, extensions,
            "D01", "finite", sp.Integer(1),
        )
        d23 = contraction_model(
            base, normal, sp.Integer(epsilon), shifts, extensions,
            "D23", "finite", sp.Integer(1),
        )
        combined = d01["mixed_matrix"].col_join(d23["mixed_matrix"]).subs(branch)
        rank_witness = sp.factor(
            combined.extract((1, 2, 10, 12, 15), (0, 1, 2, 3, 6)).det()
        )
        assert_zero(rank_witness + 1024 * epsilon * normal * base**2)
        vectors = (
            sp.Matrix((0, -1 / base, epsilon / base, 0, 1, 0, 0, 0)),
            sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0)),
            sp.Matrix((
                -epsilon, -(normal * base + epsilon) / (normal * base),
                1 / (normal * base), 0, 0, 0, 0, 1,
            )),
        )
        for vector in vectors:
            assert all(sp.factor(value) == 0 for value in combined * vector)
        extension = cap_x * vectors[0] + cap_y * vectors[1] + cap_z * vectors[2]
        extension_substitution = dict(zip(extensions, extension, strict=True))
        diagonals = tuple(sp.factor(value.subs(branch).subs(
            extension_substitution
        )) for value in (d01["A"], d01["B"], d23["A"], d23["B"]))
        factor_f = cap_x * normal + epsilon * cap_z
        factor_g = cap_y * normal * base - epsilon * marking * factor_f
        factor_h = factor_f + cap_z * normal * base
        expected = (
            0,
            4 * factor_g / normal,
            4 * epsilon * factor_f / base,
            4 * factor_h / normal,
        )
        for actual, target in zip(diagonals, expected, strict=True):
            assert_zero(actual - target)
        alpha, unmarked = p_chart_rows(
            base, normal, sp.Integer(epsilon), (0, 0, 0, 0)
        )
        beta = tuple(
            add(unmarked[i], scale(branch[shifts[i]], alpha[i]))
            for i in range(4)
        )
        marked = full_one_marked_map(
            alpha, beta, extension, "D23", sp.Integer(1), 3
        )
        target_minor = sp.factor(
            marked.extract((0, 2, 3, 7), (0, 1, 2, 4)).det()
        )
        assert_zero(
            target_minor + 64 * factor_f**2 * factor_h
            / (normal**2 * base**2)
        )
        output[str(epsilon)] = {
            "shared_projection": "only lambda=1,h0*n=1,h1=h3=0",
            "combined_rank": 5,
            "rank_witness": str(rank_witness),
            "kernel": [[str(sp.factor(value)) for value in vector]
                       for vector in vectors],
            "diagonals_A01_B01_A23_B23": [str(value) for value in diagonals],
            "genuine_open": "F*G*H!=0",
            "D23_mode3_minor": str(target_minor),
            "target_local_obstructed": True,
        }
    return output


def main():
    shared = shared_projection_atlas()
    endpoints = endpoint_projection_atlas()
    target = target_local_certificates()
    endpoint_targets = endpoint_target_certificates()
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "git_commit": git_commit(),
        "claim_label": "CANDIDATE",
        "scope": (
            "all one-parameter formal DVR/Puiseux arcs through component-19 "
            "Z0 inside the displayed finite chart with phi a unit"
        ),
        "inputs": {path.name: sha256(path) for path in INPUTS},
        "method": (
            "exact p-chart blow-up rows, parameter-aware shared projections, "
            "hidden-divisor extraction, complete extension kernels, fixed "
            "target-local minors, and a field-valued case partition"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT),
            CERTIFICATE.name: sha256(CERTIFICATE),
        },
        "field_valued_partition": [
            "p=0, d=q-phi!=0: verified p=0 aggregate",
            "d=0, p!=0: verified q=phi divisor",
            "p*d!=0, phi^2!=1: parameter-aware atlas plus two target-local obstructions",
            "p*d!=0, phi=+/-1: direct localized atlas plus endpoint target-local obstruction",
        ],
        "generic_parameter_aware_shared_projections": shared,
        "generic_projection_count": len(shared),
        "hidden_divisor": {
            "equation": "q*phi-1=normal*phi*base+phi^2-1",
            "weight": "lambda=-1",
            "orientation": ["A23", "B23", "A01"],
            "generic_function_field_projection_misses_it": True,
        },
        "target_local_certificates": target,
        "endpoint_parameter_aware_shared_projections": endpoints,
        "endpoint_projection_count": len(endpoints),
        "endpoint_target_certificates": endpoint_targets,
        "poles_and_ramification": (
            "allowed: every marking, extension, inverse diagonal, weight, and "
            "blow-up ratio is solved over the Laurent/Puiseux fraction field"
        ),
        "weighted_H22_lift_over_generic_DVR_field_exists_candidate": False,
        "formal_DVR_and_Puiseux_arcs_inside_displayed_chart_obstructed_candidate": True,
        "Rees_properness_used": False,
        "why_specialization_is_not_used": (
            "a hypothetical formal lift gives a fraction-field point; the "
            "four diagonal opens and two homogeneous weight charts are "
            "eliminated directly over that field"
        ),
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "limitations": [
            "Construction result remains CANDIDATE pending independent verification.",
            "Only one-parameter DVR/Puiseux arcs inside the displayed finite component chart with phi a unit are covered.",
            "Multi-parameter arcs, ambient-component or omitted Grassmann-chart approaches, phi=0, arbitrary local maps, and the local-to-global reduction are outside scope.",
            "The global Krenn-Gu conjecture remains unresolved.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
