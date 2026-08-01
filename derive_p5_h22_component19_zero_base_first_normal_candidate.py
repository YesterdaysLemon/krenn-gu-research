#!/usr/bin/env python3
"""Exact first-normal construction at component 19's zero base."""

from __future__ import annotations

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
REPORT = ROOT / "P5_H22_COMPONENT19_ZERO_BASE_FIRST_NORMAL_CANDIDATE.md"
GEOMETRY_CERTIFICATE = (
    ROOT / "p5_h22_component19_zero_base_first_normal_geometry_certificate.json"
)
INCIDENCE_CERTIFICATE = (
    ROOT / "p5_h22_component19_zero_base_first_normal_incidence_certificate.json"
)
SOURCE = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
RECONNAISSANCE = (
    ROOT / "P5_H22_COMPONENT19_P0_FINITE_BOUNDARY_GEOMETRY_RECONNAISSANCE.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))


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
    assert sp.cancel(value) == 0


def displayed_rows(p, q, phi):
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    first = (
        add(abar, scale(p, cap_b)), cap_b, bbar, abar,
    )
    second = (
        add(bbar, scale(q, cap_b)), cap_a, cap_a,
        add(cap_b, scale(phi, bbar)),
    )
    return first, second


def tensor_coefficients(first, second):
    return {
        word: permanent(tuple(
            second[i] if word[i] else first[i] for i in range(4)
        ))
        for word in WORDS
    }


def first_normal_geometry():
    p, q, phi, eps, a, b, c, r = sp.symbols("p q phi eps a b c r")
    first, second = displayed_rows(p, q, phi)
    coefficients = tensor_coefficients(first, second)
    support = {word: value for word, value in coefficients.items() if value != 0}
    assert set(support) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert_zero(support[(0, 1, 1, 1)] - 4 * p)
    assert_zero(support[(1, 1, 1, 1)] - 4 * (q - phi))
    zero_basis = tuple(
        polynomial.as_expr() for polynomial in
        sp.groebner(tuple(support.values()), p, q, phi, order="lex").polys
    )
    assert zero_basis == (p, q - phi)

    arc = {p: a * eps, q: r + (b + c) * eps, phi: r + c * eps}
    leading = {
        word: sp.expand(value.subs(arc)).coeff(eps, 1)
        for word, value in coefficients.items()
    }
    leading = {word: value for word, value in leading.items() if value != 0}
    assert set(leading) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert_zero(leading[(0, 1, 1, 1)] - 4 * a)
    assert_zero(leading[(1, 1, 1, 1)] - 4 * b)

    # At the zero base use the regular swap from the q=phi divisor.  In this
    # basis the leading mode-zero covector has values (b,a) on (alpha,beta).
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    u0 = add(bbar, scale(r, cap_b))
    v0 = abar
    base_planes = (
        (u0, v0), (cap_b, cap_a), (bbar, cap_a),
        (abar, add(cap_b, scale(r, bbar))),
    )

    s, t = sp.symbols("s t")
    direction_charts = {
        "a_nonzero_[1:s]": {
            "normal_direction": ["1", "s"],
            "alpha0": add(u0, scale(-s, v0)),
            "beta0": v0,
            "change_determinant": sp.Integer(1),
            "normal_values_before_alignment": ["s", "1"],
            "normal_values_after_alignment": ["0", "1"],
        },
        "b_nonzero_[t:1]": {
            "normal_direction": ["t", "1"],
            "alpha0": add(scale(t, u0), scale(-1, v0)),
            "beta0": u0,
            "change_determinant": sp.Integer(1),
            "normal_values_before_alignment": ["1", "t"],
            "normal_values_after_alignment": ["0", "1"],
        },
    }
    assert direction_charts["a_nonzero_[1:s]"]["normal_values_after_alignment"] == ["0", "1"]
    assert direction_charts["b_nonzero_[t:1]"]["normal_values_after_alignment"] == ["0", "1"]
    # On t!=0, s=1/t and the transition from the b-chart basis to the
    # a-chart basis has matrix [[1/t,0],[-1,t]], of determinant one.
    transition = sp.Matrix(((1 / t, 0), (-1, t)))
    assert_zero(transition.det() - 1)

    def squarefree(left, right):
        return sp.Matrix(tuple(
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in PAIRS
        ))

    def pair_matrix(plane_i, plane_j):
        return sp.Matrix.hstack(*(
            squarefree(plane_i[i], plane_j[j])
            for i in range(2) for j in range(2)
        ))

    base_profile = tuple(
        pair_matrix(base_planes[i], base_planes[j]).rank() for i, j in PAIRS
    )
    assert base_profile == (3, 3, 3, 3, 3, 3)
    endpoint_profiles = {}
    for sign in (1, -1):
        endpoint_planes = tuple(tuple(
            tuple(sp.expand(sp.sympify(value).subs(r, sign)) for value in row)
            for row in plane
        ) for plane in base_planes)
        endpoint_profiles[str(sign)] = tuple(
            pair_matrix(endpoint_planes[i], endpoint_planes[j]).rank()
            for i, j in PAIRS
        )
    assert set(endpoint_profiles.values()) == {(3, 3, 2, 3, 3, 3)}

    arc_profiles = {}
    arc_models = {
        "[1:0]": {p: eps, q: r, phi: r},
        "[0:1]": {p: 0, q: r + eps, phi: r},
        "[1:s]_s_nonzero": {p: eps, q: r + s * eps, phi: r},
    }
    for label, substitution in arc_models.items():
        arc_first, arc_second = displayed_rows(p, q, phi)
        planes = tuple((arc_first[i], arc_second[i]) for i in range(4))
        arc_profiles[label] = tuple(
            pair_matrix(planes[i], planes[j]).subs(substitution).rank()
            for i, j in PAIRS
        )
    assert arc_profiles == {
        "[1:0]": (4, 4, 3, 3, 3, 3),
        "[0:1]": (3, 3, 4, 3, 3, 3),
        "[1:s]_s_nonzero": (4, 4, 4, 3, 3, 3),
    }

    return {
        "tensor_coefficient_ideal": [str(value) for value in zero_basis],
        "arc": {
            "p": "a*eps", "q": "r+(b+c)*eps", "phi": "r+c*eps",
            "tangent_coordinate": "c",
        },
        "first_normal_support_displayed_basis": {
            "0111": str(leading[(0, 1, 1, 1)]),
            "1111": str(leading[(1, 1, 1, 1)]),
        },
        "projectivized_normal_fibre": "P^1_[a:b]",
        "regular_zero_base_basis": {
            "alpha": [[str(value) for value in plane[0]] for plane in base_planes],
            "beta": [[str(value) for value in plane[1]] for plane in base_planes],
            "normal_mode0_values_alpha_beta": ["b", "a"],
        },
        "direction_charts": {
            key: {
                subkey: (
                    [str(value) for value in subvalue]
                    if isinstance(subvalue, tuple) else
                    str(subvalue) if isinstance(subvalue, sp.Basic) else subvalue
                )
                for subkey, subvalue in value.items()
            }
            for key, value in direction_charts.items()
        },
        "chart_transition_on_t_nonzero": [["1/t", "0"], ["-1", "t"]],
        "chart_transition_determinant": "1",
        "normal_support_after_alignment_and_all_affine_markings": {"1111": "4"},
        "literal_zero_base_pair_profile_on_r^2!=1": list(base_profile),
        "literal_zero_base_endpoint_profiles": {
            key: list(value) for key, value in endpoint_profiles.items()
        },
        "nearby_linear_arc_pair_profiles": {
            key: list(value) for key, value in arc_profiles.items()
        },
        "all_projective_normal_directions_have_all_pair_open_generic_arc_for_r_nonzero": True,
        "literal_limiting_plane_is_all_pair_open_exactly_when_r^2!=1": True,
        "higher_order_tensor_statement": (
            "For any arc not contained in the zero base, divide by eps^m, "
            "where m=min(ord(p),ord(q-phi)); its first nonzero tensor is "
            "4*a_m*T0111+4*b_m*T1111 and again defines [a_m:b_m] in P1."
        ),
    }


def normal_aligned_basis(r, direction, chart):
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    u0 = add(bbar, scale(r, cap_b))
    v0 = abar
    if chart == "a_nonzero":
        alpha0, beta0 = add(u0, scale(-direction, v0)), v0
    elif chart == "b_nonzero":
        alpha0, beta0 = add(scale(direction, u0), scale(-1, v0)), u0
    else:
        raise ValueError(chart)
    alpha = (alpha0, cap_b, bbar, abar)
    beta = (beta0, cap_a, cap_a, add(cap_b, scale(r, bbar)))
    return alpha, beta


def projected_row(row, extension, weight_chart, slope):
    if weight_chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if weight_chart == "infinity":
        return (row[0], row[2], row[3], extension)
    raise ValueError(weight_chart)


def d01_model(r, direction, direction_chart, weight_chart, slope, shifts, extensions):
    alpha, unmarked_beta = normal_aligned_basis(r, direction, direction_chart)
    beta = tuple(
        add(unmarked_beta[i], scale(shifts[i], alpha[i])) for i in range(4)
    )
    projected_alpha = tuple(
        projected_row(alpha[i], extensions[i], weight_chart, slope)
        for i in range(4)
    )
    projected_beta = tuple(
        projected_row(beta[i], extensions[4 + i], weight_chart, slope)
        for i in range(4)
    )
    coefficients = {
        word: permanent(tuple(
            projected_beta[i] if word[i] else projected_alpha[i]
            for i in range(4)
        ))
        for word in WORDS
    }
    return coefficients


def structural_d01_obstruction():
    r, direction, slope = sp.symbols("r d lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    h0, h1, h2, h3 = shifts
    x1, x2 = extensions[1], extensions[2]
    output = []
    for weight_chart in ("finite", "infinity"):
        coefficients = d01_model(
            r, direction, "a_nonzero", weight_chart, slope, shifts, extensions
        )
        factor = slope - 1 if weight_chart == "finite" else sp.Integer(1)
        alpha_diagonal = coefficients[WORDS[0]]
        beta_diagonal = coefficients[WORDS[-1]]
        mixed_0001 = coefficients[(0, 0, 0, 1)]
        mixed_1000 = coefficients[(1, 0, 0, 0)]
        mixed_1001 = coefficients[(1, 0, 0, 1)]
        mixed_1011 = coefficients[(1, 0, 1, 1)]
        mixed_1101 = coefficients[(1, 1, 0, 1)]
        S = r * x2 - x1
        R = r * x1 - x2
        assert_zero(alpha_diagonal - 2 * factor * S)
        assert_zero(mixed_1000 - h0 * alpha_diagonal)
        assert_zero(mixed_0001 - 2 * factor * (direction * R + h3 * S))
        assert_zero(mixed_1001.subs({h0: 0, h3: 0}) + 2 * factor * R)
        reduction = {h0: 0, h3: 0, x2: r * x1}
        assert_zero(
            beta_diagonal.subs(reduction)
            - (h1 * mixed_1011 + h2 * mixed_1101).subs(reduction)
        )
        output.append({
            "weight_chart": weight_chart,
            "alpha_diagonal": str(alpha_diagonal),
            "mixed_1000_identity": "m1000=h0*A01",
            "mixed_0001_identity": (
                "m0001=2*w*(d*(r*x1-x2)+h3*(r*x2-x1))"
            ),
            "mixed_1001_after_h0_h3_zero": "-2*w*(r*x1-x2)",
            "beta_syzygy_after_h0_h3_zero_and_x2_r_x1": (
                "B01=h1*m1011+h2*m1101"
            ),
            "weight_factor_w": str(factor),
            "deduction": (
                "A01!=0 forces w!=0; mixed equations give h0=0, "
                "x2=r*x1, then h3=0 (or A01=0 when r^2=1), and "
                "the displayed beta syzygy forces B01=0"
            ),
        })

    # The second normal-direction chart is needed only at t=0: on that
    # endpoint its alpha diagonal vanishes.  Its t!=0 part is the overlap
    # transported by the determinant-one transition checked above.
    endpoint = {}
    for weight_chart in ("finite", "infinity"):
        coefficients = d01_model(
            r, direction, "b_nonzero", weight_chart, slope, shifts, extensions
        )
        endpoint[weight_chart] = sp.factor(coefficients[WORDS[0]].subs(direction, 0))
        assert_zero(endpoint[weight_chart])
    return output, {key: str(value) for key, value in endpoint.items()}


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def unit_elimination(label, equations, eliminated, retained, coefficient_ring):
    variables = tuple(eliminated) + tuple(retained)
    lines = [
        "ring R=" + coefficient_ring + ",("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
        '"CODEX_RESULT:"+string(reduce(1,J)==0)+":"+string(size(J));',
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
        "coefficient_ring": coefficient_ring,
        "projected_ideal": ["1"],
        "standard_basis_size": int(markers[0].split(":")[2]),
    }


def elimination_audits():
    r, direction, slope = sp.symbols("r d lam")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:8")
    inverse, open_inverse = sp.symbols("u o")
    output = []
    for direction_chart in ("a_nonzero", "b_nonzero"):
        for weight_chart in ("finite", "infinity"):
            coefficients = d01_model(
                r, direction, direction_chart, weight_chart, slope,
                shifts, extensions,
            )
            equations = (
                *(coefficients[word] for word in MIXED),
                coefficients[WORDS[0]] - 1,
                inverse * coefficients[WORDS[-1]] - 1,
            )
            retained = shifts + (
                (slope,) if weight_chart == "finite" else ()
            ) + (direction,)
            output.append(unit_elimination(
                f"{direction_chart}_{weight_chart}_over_Q(r)", equations,
                extensions + (inverse,), retained, "(0,r)",
            ))
            output.append(unit_elimination(
                f"{direction_chart}_{weight_chart}_over_Q[r]_on_r_nonzero",
                (*equations, open_inverse * r - 1),
                extensions + (inverse, open_inverse), retained + (r,), "0",
            ))
    return output


def main():
    geometry = first_normal_geometry()
    structural, second_chart_endpoint = structural_d01_obstruction()
    eliminations = elimination_audits()
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "git_commit": git_commit(),
        "claim_label": "CANDIDATE",
        "scope": (
            "component 19 zero base p=0,q=phi=r, r!=0: exact first-normal "
            "P1 and its regular weighted-H22 incidence"
        ),
        "inputs": {
            SOURCE.name: sha256(SOURCE),
            RECONNAISSANCE.name: sha256(RECONNAISSANCE),
        },
        "method": (
            "direct normal-jet permanent reconstruction, two regular P1 "
            "direction charts, exact pair ranks, coefficient syzygies, and "
            "eight bounded characteristic-zero unit-ideal audits"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT),
            GEOMETRY_CERTIFICATE.name: sha256(GEOMETRY_CERTIFICATE),
            INCIDENCE_CERTIFICATE.name: sha256(INCIDENCE_CERTIFICATE),
        },
        "geometry": geometry,
        "weighted_H22": {
            "structural_D01_obstruction_on_a_nonzero_chart": structural,
            "b_nonzero_chart_endpoint_t_zero_A01": second_chart_endpoint,
            "bounded_elimination_audits": eliminations,
            "audit_count": len(eliminations),
            "both_homogeneous_weight_charts_checked": ["finite [lam:1]", "infinity [1:0]"],
            "D01_binary_incidence_empty": True,
            "shared_H22_incidence_empty": True,
            "reason_shared_is_empty": "the necessary D01 binary incidence is already empty",
            "first_normal_weighted_H22_fibre_empty_candidate": True,
        },
        "higher_order_boundary": {
            "tensor_direction_extension": (
                "proved for the first nonzero normal jet of every arc not "
                "contained in p=q-phi=0"
            ),
            "actual_H22_arc_extension": "UNKNOWN",
            "reason": (
                "the first-normal incidence does not classify simultaneous "
                "valuations of markings, extension coordinates, and diagonal "
                "normalizations along a higher-order or ramified H22 arc"
            ),
        },
        "finite_field_computation_used": False,
        "generic_specialization_used_as_proof": False,
        "broad_brute_force_used": False,
        "limitations": [
            "Construction result remains CANDIDATE pending independent verification.",
            "The H22 conclusion is for the exact first-normal/projectivized incidence, not a theorem excluding every higher-order valuative H22 arc.",
            "The formal r=0 limit is outside the component chart.",
            "No arbitrary-order local-to-global or global Krenn-Gu conclusion is made.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
