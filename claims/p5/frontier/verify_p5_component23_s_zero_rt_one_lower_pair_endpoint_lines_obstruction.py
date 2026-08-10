#!/usr/bin/env python3
"""Close component 23's finite-k s=0, rt=1 lower-pair endpoint lines."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _repo_parent in Path(__file__).resolve().parents:
    if (_repo_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_repo_parent / "src"))
        break
else:
    raise RuntimeError("could not locate repository src directory")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model
REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star")

from verify_p5_h22_common_center_kernel_star_component_partial import (
    coefficient_row,
    singular_command,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    permanent,
)



WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
k, lam, w = sp.symbols("k lam w")


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def endpoint_rows(sign):
    sign = sp.Integer(sign)
    cap_a = (sp.Integer(1), 1, 0, 0)
    cap_c = (sp.Integer(1), -1, 0, 0)
    cap_b = (0, 0, sp.Integer(1), 1)
    cap_d = (0, 0, sp.Integer(1), -1)
    alpha = (
        cap_a,
        add(cap_a, cap_d, k),
        add(cap_b, cap_d, sign),
        add(cap_b, cap_d, sign),
    )
    beta = (cap_b, cap_b, cap_c, cap_c)
    return alpha, beta


def symmetric_product(left, right):
    return sp.Matrix(
        [
            left[first] * right[second] + left[second] * right[first]
            for first, second in PAIRS
        ]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def same_plane(left, right):
    return left.row_join(right).rank() == 2


def permanent5(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(5))
            for permutation in itertools.permutations(range(5))
        )
    )


def geometry_certificate(sign):
    alpha, beta = endpoint_rows(sign)
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    generic_profile = tuple(
        pair_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )
    zero_planes = tuple(
        tuple(tuple(sp.sympify(value).subs(k, 0) for value in row) for row in plane)
        for plane in planes
    )
    zero_profile = tuple(
        pair_matrix(zero_planes[left], zero_planes[right]).rank()
        for left, right in PAIRS
    )
    assert generic_profile == (3, 3, 3, 4, 4, 2)
    assert zero_profile == (3, 3, 3, 3, 3, 2)

    edge = pair_matrix(planes[2], planes[3])
    kernel = edge.nullspace()
    assert len(kernel) == 2
    assert kernel[0] == sp.Matrix((1, 0, 0, 0))
    assert kernel[1] in (
        sp.Matrix((0, -1, 1, 0)),
        sp.Matrix((0, 1, -1, 0)),
    )
    u, v = sp.symbols("u v")
    kernel_matrix = sp.Matrix(2, 2, tuple(u * kernel[0] + v * kernel[1]))
    assert sp.factor(kernel_matrix.det()) in (v**2, -(v**2))
    assert symmetric_product(alpha[2], alpha[3]) == sp.zeros(6, 1)

    cap_a = sp.Matrix((1, 1, 0, 0))
    cap_c = sp.Matrix((1, -1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 1))
    cap_d = sp.Matrix((0, 0, 1, -1))
    e = (cap_b + sign * cap_d) / 2
    zed = (cap_b - sign * cap_d) / 2
    tangent = sp.Matrix.vstack(e.T, cap_c.T)
    opposite_zero = sp.Matrix.vstack(cap_a.T, (e + zed).T)
    opposite_one = sp.Matrix.vstack(
        (cap_a + 2 * sign * k * e).T,
        (e + zed).T,
    )
    assert same_plane(sp.Matrix(planes[2]), tangent)
    assert same_plane(sp.Matrix(planes[3]), tangent)
    assert same_plane(sp.Matrix(planes[0]), opposite_zero)
    assert same_plane(sp.Matrix(planes[1]), opposite_one)

    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )
    projective_markings = tuple(
        coefficients[tuple(0 if index == mode else 1 for index in range(4))]
        for mode in range(4)
    )
    assert projective_markings == (0, 0, 0, 0)
    assert all(sp.Matrix(plane).rank() == 2 for plane in planes)
    return {
        "sign": sign,
        "generic_k_profile": generic_profile,
        "k_zero_profile": zero_profile,
        "rank_two_edge": "23",
        "kernel_type": "support-one tangent Segre point",
        "tangent_plane": "span(e,H)",
        "opposite_planes": (
            "span(S,e+Z)",
            "span(S+2*sign*k*e,e+Z)",
        ),
        "lower_pair_placement": "support-two tangent polar-flag boundary of the known sixfold",
        "pure_coefficient": "T1111=-4",
        "omitted_projective_marking_coefficients": tuple(map(str, projective_markings)),
    }


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(label, program, expected, timeout=300):
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
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [expected], (label, completed.stdout, expected)
    return label


def shifted_beta(alpha, beta, marking):
    return tuple(add(beta[index], alpha[index], marking[index]) for index in range(4))


def h31_projection(sign, deletion):
    alpha, beta = endpoint_rows(sign)
    marked = shifted_beta(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    extension = sp.Matrix(x)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        w * (diagonal_b * extension)[0] - 1,
    )
    surviving_deletion = 3 if sign == 1 else 2
    expected = (
        (h[0], h[1], h[2] * h[3])
        if deletion == surviving_deletion
        else (sp.Integer(1),)
    )
    eliminated = x + (w,)
    variables = eliminated + h + (k,)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(5));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    run_singular(
        f"r_{sign}_deletion_{deletion}_projection",
        program,
        f"RESULT:1:{len(expected)}",
    )
    return {
        "sign": sign,
        "deletion": deletion,
        "projected_ideal": tuple(map(str, expected)),
    }


def h31_punctured_marking_branch(sign, zero_coordinate):
    deletion = 3 if sign == 1 else 2
    p = sp.Symbol("p")
    marking = (0, 0, 0, p) if zero_coordinate == "h2" else (0, 0, p, 0)
    active_mode = 2 if zero_coordinate == "h2" else 3
    alpha, beta = endpoint_rows(sign)
    marked = shifted_beta(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 4
    kernel = mixed.nullspace()
    assert len(kernel) == 4
    coefficients = sp.symbols("c0:4")
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix(coefficients)
    c0, c1, c2, c3 = coefficients
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    assert sp.expand(actual_a - 4 * (c0 * p - c3) / p) == 0
    assert sp.expand(actual_b + 2 * (c1 + c2)) == 0

    row_sets = (
        (0, 1, 2, 7),
        (0, 1, 3, 7),
        (0, 1, 4, 7),
        (0, 1, 5, 7),
    )
    residuals = (
        c0 + 2 * c2,
        2 * c2 * p + c3,
        c0 + 2 * c1,
        2 * c1 * p + c3,
    )
    common = 16 * (c1 + c2) * (c0 * p - c3)
    expected = tuple(common * residual for residual in residuals)
    marked_map = marked_extension(deletion, extension, alpha, marked, active_mode)
    actual = tuple(
        sp.factor(marked_map.extract(rows, range(4)).det(method="domain-ge"))
        for rows in row_sets
    )
    assert all(sp.expand(left - right) == 0 for left, right in zip(actual, expected))
    groebner = sp.groebner(residuals, c0, c1, c2, c3, order="grevlex")
    assert groebner.reduce(c0 * p - c3)[1] == 0
    return {
        "sign": sign,
        "deletion": deletion,
        "branch": f"{zero_coordinate}=0, other=p!=0",
        "mixed_rank": 4,
        "mixed_nullity": 4,
        "A": str(actual_a),
        "B": str(actual_b),
        "active_mode": active_mode,
        "minor_rows": row_sets,
        "minors": tuple(map(str, actual)),
    }


def h31_intersection_k_nonzero(sign):
    deletion = 3 if sign == 1 else 2
    alpha, beta = endpoint_rows(sign)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, beta)
    assert mixed.rank() == 4
    kernel = mixed.nullspace()
    assert len(kernel) == 4
    coefficients = sp.symbols("c0:4")
    extension = sp.Matrix.hstack(*kernel) * sp.Matrix(coefficients)
    c0, c1, c2, c3 = coefficients
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    assert sp.expand(actual_a - 4 * (c0 + c1)) == 0
    assert sp.expand(actual_b + 2 * (c2 + c3)) == 0

    rows = ((0, 1, 3, 7), (0, 2, 3, 7), (0, 3, 5, 7), (0, 3, 6, 7))
    residuals = (c0 - 2 * c2, c1 - 2 * c2, c0 + 2 * c3, c1 + 2 * c3)
    common = (c0 + c1) * (c2 + c3)
    expected = (
        -16 * k**2 * common * residuals[0],
        -16 * k**2 * common * residuals[1],
        16 * sign * k * common * residuals[2],
        16 * sign * k * common * residuals[3],
    )
    marked_map = marked_extension(deletion, extension, alpha, beta, 0)
    actual = tuple(
        sp.factor(marked_map.extract(row_set, range(4)).det(method="domain-ge"))
        for row_set in rows
    )
    assert all(sp.expand(left - right) == 0 for left, right in zip(actual, expected))
    groebner = sp.groebner(residuals, c0, c1, c2, c3, order="grevlex")
    assert groebner.reduce(c2 + c3)[1] == 0
    return {
        "sign": sign,
        "deletion": deletion,
        "branch": "h2=h3=0, k!=0",
        "A": str(actual_a),
        "B": str(actual_b),
        "minor_rows": rows,
        "minors": tuple(map(str, actual)),
    }


def one_gamma_map(alpha, beta, source_row, mode):
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[bit_index] else alpha[other])
                bit_index += 1
        coefficient_row_values = []
        for coordinate in range(5):
            basis = tuple(sp.Integer(index == coordinate) for index in range(5))
            coefficient_row_values.append(
                permanent5(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                    + (source_row,)
                )
            )
        rows.append(coefficient_row_values)
    return sp.Matrix(rows)


def h31_intersection_k_zero(sign):
    c0, c1, c2, c3 = sp.symbols("c0:4")
    # Rows of the alpha/beta coefficient map for a possible support-three
    # source row (u0,u1,u_common,u4).  These five rows generate the map.
    annihilator_rows = sp.Matrix(
        (
            (2 * (c0 + c1), 2 * (c0 + c1), 0, 0),
            (-2 * (c0 + c2 + c3), 2 * (c0 + c2 + c3), 0, 0),
            (-2 * (c1 + c2 + c3), 2 * (c1 + c2 + c3), 0, 0),
            (0, 0, -2 * (c2 + c3), -4),
        )
    )
    u0, u1, u_common, u4 = sp.symbols("u0 u1 u_common u4")
    source = sp.Matrix((u0, u1, u_common, u4))
    equations = annihilator_rows * source
    assert sp.expand(equations[0] - 2 * (c0 + c1) * (u0 + u1)) == 0
    # On diagonal_a*diagonal_b*u0*u1*u_common != 0, the next two rows force
    # c0=c1=-(c2+c3).  Normalize c2+c3=1 by scaling the fifth source row.
    assert sp.expand(equations[1].subs(u1, -u0) + 4 * u0 * (c0 + c2 + c3)) == 0
    assert sp.expand(equations[2].subs(u1, -u0) + 4 * u0 * (c1 + c2 + c3)) == 0

    tau, a, b = sp.symbols("tau a b")
    alpha4, beta4 = endpoint_rows(sign)
    alpha4 = tuple(
        tuple(sp.sympify(value).subs(k, 0) for value in row) for row in alpha4
    )
    beta4 = tuple(tuple(map(sp.sympify, row)) for row in beta4)
    extension = (0, 0, -1, -1, tau, 1 - tau, 0, 0)
    alpha5 = tuple(tuple(row) + (extension[index],) for index, row in enumerate(alpha4))
    beta5 = tuple(
        tuple(row) + (extension[4 + index],) for index, row in enumerate(beta4)
    )
    deletion = 3 if sign == 1 else 2
    common = tuple(index for index in range(4) if index != deletion)
    support_three_row = [sp.Integer(0)] * 5
    support_three_row[common[0]] = a
    support_three_row[common[1]] = -a
    support_three_row[common[2]] = b
    support_three_row[4] = -b / 2
    support_three_row = tuple(support_three_row)
    active_mode = 2 if sign == 1 else 3
    one_gamma = one_gamma_map(alpha5, beta5, support_three_row, active_mode)
    expected = sp.zeros(8, 5)
    expected[0, 3 if sign == 1 else 2] = -4 * b
    expected[2, 0] = expected[2, 1] = -2 * b
    expected[4, 0] = expected[4, 1] = -2 * b
    expected[7, 2] = expected[7, 3] = -2 * a
    expected[7, 4] = -4 * a
    assert one_gamma == expected
    selected_minor = sp.factor(one_gamma.extract((0, 2, 7), (0, 2, 3)).det())
    assert selected_minor == -16 * sign * a * b**2
    active_plane = sp.Matrix.vstack(
        sp.Matrix(alpha5[active_mode]).T,
        sp.Matrix(beta5[active_mode]).T,
    )
    assert one_gamma * active_plane.T == sp.zeros(8, 2)
    assert active_plane.rank() == 2
    # The selected minor gives rank three for a*b!=0, so the kernel is exactly
    # this two-plane and cannot contain a third independent local row.
    return {
        "sign": sign,
        "deletion": deletion,
        "branch": "h2=h3=k=0",
        "special_extension_condition": "c0=c1=-(c2+c3), c2+c3!=0",
        "support_three_row": "(a,-a,b,-b/2), a*b!=0",
        "one_gamma_mode": active_mode,
        "one_gamma_rank_minor": str(selected_minor),
        "one_gamma_kernel": "the existing marked two-plane",
    }


def h22_certificate(sign, chart):
    alpha, beta = endpoint_rows(sign)
    marked = shifted_beta(alpha, beta, h)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, marked, x, "D01", chart, slope)
    d23 = build_model(alpha, marked, x, "D23", chart, slope)
    generators = ",".join(
        coefficient_row(expression, x) for expression in (*d01["mixed"], *d23["mixed"])
    )
    diagonals = tuple(
        coefficient_row(expression, x)
        for expression in (d01["A"], d23["A"], d01["B"], d23["B"])
    )
    if chart == "finite":
        variables = x + (w,) + h + (k, lam)
        equations = (
            *d01["mixed"],
            *d23["mixed"],
            d23["A"] - 1,
            w * d01["B"] * d23["B"] - 1,
        )
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(6));",
                "option(redSB);",
                "module M=" + generators + "; M=std(M);",
                "vector d0=" + diagonals[0] + ";",
                "int alpha01=reduce(d0,M)==0;",
                "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
                "int unit=(size(I)==1)&&(I[1]==1);",
                '"RESULT:"+string(alpha01)+":"+string(unit);',
                "quit;",
            )
        )
        run_singular(f"r_{sign}_finite_h22", program, "RESULT:1:1", timeout=600)
        result = {
            "sign": sign,
            "chart": chart,
            "A01_in_shared_mixed_module": True,
            "normalized_genuine_ideal": "(1) after A23=1 and B01*B23!=0",
        }
    else:
        variables = h + (k,)
        program = "\n".join(
            (
                "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
                "option(redSB);",
                "module M=" + generators + "; M=std(M);",
                *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
                *(f"int m{index}=reduce(d{index},M)==0;" for index in range(4)),
                '"RESULT:"+string(m0)+":"+string(m1)+":"+string(m2)+":"+string(m3);',
                "quit;",
            )
        )
        run_singular(f"r_{sign}_projective_h22", program, "RESULT:1:1:1:1", timeout=600)
        result = {
            "sign": sign,
            "chart": chart,
            "diagonal_order": ("A01", "A23", "B01", "B23"),
            "diagonal_membership": (True, True, True, True),
        }
    return result


def main():
    geometry = tuple(geometry_certificate(sign) for sign in (1, -1))
    projections = tuple(
        h31_projection(sign, deletion) for sign in (1, -1) for deletion in range(4)
    )
    punctured = tuple(
        h31_punctured_marking_branch(sign, zero_coordinate)
        for sign in (1, -1)
        for zero_coordinate in ("h2", "h3")
    )
    intersections_nonzero = tuple(h31_intersection_k_nonzero(sign) for sign in (1, -1))
    intersections_zero = tuple(h31_intersection_k_zero(sign) for sign in (1, -1))
    h22 = tuple(
        h22_certificate(sign, chart)
        for sign in (1, -1)
        for chart in ("finite", "infinity")
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "scope": "component 23 normalized s=0, rt=1, r=+/-1 lower-pair endpoint lines, k arbitrary",
                "field": "Q",
                "geometry": geometry,
                "h31_projections": projections,
                "h31_punctured_marking_branches": punctured,
                "h31_k_nonzero_intersections": intersections_nonzero,
                "h31_k_zero_intersections": intersections_zero,
                "h22": h22,
                "limitations": (
                    "fixed normalized contraction order only; arbitrary ambient/source bases, "
                    "other projective component charts, arbitrary order, local-to-global, and "
                    "the global conjecture are not claimed"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
