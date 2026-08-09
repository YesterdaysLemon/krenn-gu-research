#!/usr/bin/env python3
"""Build the exact integral graph slice for the common-active binary component."""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p4/classifications")
from verify_p4_directed_zero_divisor_triangle_components import (  # noqa: E402
    coefficients,
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
ANCHOR = (0, 1, 1, 0)
PARAMETER_SAMPLE = (2, 4, 1, 1, 1)
POINT = (
    sp.Integer(-6),
    sp.Integer(1),
    sp.Integer(-2),
    sp.Rational(1, 6),
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(1),
    sp.Rational(1, 3),
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(2),
    sp.Rational(1, 2),
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(1),
    sp.Integer(0),
)
TARGET_POINT = (sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(-1))
FIXED_COORDINATES = (0, 1, 2, 3, 6)
RETAINED_INDICES = (4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)


def pivot01_planes(variables: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(
            (
                (1, 0, variables[4 * mode], variables[4 * mode + 1]),
                (0, 1, variables[4 * mode + 2], variables[4 * mode + 3]),
            )
        )
        for mode in range(4)
    )


def normalized_family(
    p: sp.Expr,
    q: sp.Expr,
    t_0: sp.Expr = sp.S.One,
    t_1: sp.Expr = sp.S.One,
    t_2: sp.Expr = sp.S.One,
) -> tuple[sp.Matrix, ...]:
    """Return the lambda=gamma=1 common-active binary chart."""

    e = sp.Matrix([[1, 0, 0, 0]])
    a = sp.Matrix([[0, 1, 0, 0]])
    b = sp.Matrix([[0, 0, 1, 0]])
    c = sp.Matrix([[0, 0, 0, 1]])
    h = a - b
    w = a + b
    v = p * a + q * b + c
    u = v + h
    denominator = p + q
    u_0 = sp.Matrix(
        (
            (-(p - q + 1) / denominator, -1, 1, 0),
            ((q**2 - q) / denominator, -p - q, 0, 1),
        )
    )
    raw = (
        u_0,
        sp.Matrix.vstack(e, u),
        sp.Matrix.vstack(e, v),
        sp.Matrix.vstack(e + w, e),
    )
    diagonal = sp.diag(t_0, t_1, t_2, 1)
    return tuple(plane * diagonal for plane in raw)


def chart_reduce(planes: tuple[sp.Matrix, ...]) -> tuple[sp.Matrix, ...]:
    return tuple(sp.simplify(plane[:, (0, 1)].inv() * plane) for plane in planes)


def chart_coordinates(planes: tuple[sp.Matrix, ...]) -> tuple[sp.Expr, ...]:
    return tuple(
        plane[row, column] for plane in planes for row in range(2) for column in (2, 3)
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    def product(left_row: sp.Matrix, right_row: sp.Matrix) -> sp.Matrix:
        return sp.Matrix(
            [left_row[i] * right_row[j] + left_row[j] * right_row[i] for i, j in PAIRS]
        )

    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def incidence_equations(
    plane_variables: tuple[sp.Symbol, ...],
    target_variables: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], dict[tuple[int, ...], sp.Expr]]:
    tensor = coefficients(pivot01_planes(plane_variables))
    equations = []
    for word in WORDS:
        if word == ANCHOR:
            continue
        monomial = sp.prod(
            target_variables[mode] for mode in range(4) if word[mode] != ANCHOR[mode]
        )
        equations.append(sp.expand(tensor[word] - tensor[ANCHOR] * monomial))
    return tuple(equations), tensor


def singular_string(expression: sp.Expr) -> str:
    return sp.sstr(expression).replace("**", "^")


def main() -> None:
    p, q, t_0, t_1, t_2 = sp.symbols("p q t_0 t_1 t_2")
    parameters = (p, q, t_0, t_1, t_2)
    sample = dict(zip(parameters, PARAMETER_SAMPLE, strict=True))

    raw_family = normalized_family(p, q)
    raw_tensor = coefficients(raw_family)
    expected = {
        (0, 1, 1, 1): 2 * (p - q + 1),
        (1, 1, 1, 1): -2 * q * (q - 1),
    }
    for word, value in raw_tensor.items():
        assert sp.factor(value - expected.get(word, 0)) == 0

    family = chart_reduce(normalized_family(*parameters))
    family_coordinates = chart_coordinates(family)
    assert tuple(sp.factor(value.subs(sample)) for value in family_coordinates) == POINT
    family_jacobian = sp.Matrix(family_coordinates).jacobian(parameters).subs(sample)
    assert family_jacobian.rank() == 5
    assert tuple(family_jacobian.T.rref()[1]) == FIXED_COORDINATES
    family_minor = sp.factor(family_jacobian.extract(FIXED_COORDINATES, range(5)).det())
    assert family_minor == sp.Rational(-1, 6)

    sample_planes = tuple(plane.subs({p: 2, q: 4}) for plane in raw_family)
    profile = tuple(
        pair_matrix(sample_planes[left], sample_planes[right]).rank()
        for left, right in PAIRS
    )
    assert profile == (4, 4, 4, 3, 3, 3)
    relations = {
        (1, 2): sp.Matrix([1, 0, 0, 0]),
        (1, 3): sp.Matrix([0, 1, 0, 0]),
        (2, 3): sp.Matrix([0, 1, 0, 0]),
    }
    for edge, relation in relations.items():
        matrix = pair_matrix(raw_family[edge[0]], raw_family[edge[1]])
        assert matrix * relation == sp.zeros(6, 1)
        assert sp.Matrix(2, 2, tuple(relation)).rank() == 1
        assert matrix.subs({p: 2, q: 4}).rank() == 3

    plane_variables = tuple(sp.symbols("g0:16"))
    target_variables = tuple(sp.symbols("z0:4"))
    all_variables = (*plane_variables, *target_variables)
    equations, tensor = incidence_equations(plane_variables, target_variables)
    point_substitution = dict(zip(all_variables, (*POINT, *TARGET_POINT), strict=True))
    assert tensor[ANCHOR].subs(point_substitution) == -2
    assert all(equation.subs(point_substitution) == 0 for equation in equations)
    incidence_jacobian = (
        sp.Matrix(equations).jacobian(all_variables).subs(point_substitution)
    )
    assert incidence_jacobian.rank() == 12

    # Fix the five chart coordinates whose restriction to the explicit
    # family has determinant -1/6.  Translate every retained coordinate to
    # the rational certificate point and clear the common denominator 6.
    local_variables = tuple(sp.symbols("x0:15"))
    full_point = (*POINT, *TARGET_POINT)
    local_substitution: dict[sp.Symbol, sp.Expr] = {}
    for index, variable in enumerate(all_variables):
        if index in FIXED_COORDINATES:
            local_substitution[variable] = full_point[index]
        else:
            retained_position = RETAINED_INDICES.index(index)
            local_substitution[variable] = (
                full_point[index] + local_variables[retained_position]
            )
    local_equations = tuple(
        sp.expand(equation.subs(local_substitution)) for equation in equations
    )
    assert all(
        equation.subs(dict.fromkeys(local_variables, 0)) == 0
        for equation in local_equations
    )
    assert (
        sp.Matrix(local_equations)
        .jacobian(local_variables)
        .subs(dict.fromkeys(local_variables, 0))
        .rank()
        == 12
    )
    cleared_data = tuple(
        sp.Poly(equation, *local_variables).clear_denoms()
        for equation in local_equations
    )
    denominators = tuple(int(denominator) for denominator, _ in cleared_data)
    contents = tuple(int(polynomial.primitive()[0]) for _, polynomial in cleared_data)
    assert denominators == (6,) * 15
    assert contents == (1,) * 15
    integer_equations = tuple(polynomial.as_expr() for _, polynomial in cleared_data)

    output = REPO_ROOT / "tmp" / "p4_common_active_binary_local_graph_slice.sing"
    output.parent.mkdir(exist_ok=True)
    source = f"""// Generated by {Path(__file__).name}
ring R=0,({",".join(map(str, local_variables))}),ds;
ideal I=
  {",\n  ".join(singular_string(equation) for equation in integer_equations)};
int t=timer;
ideal G=std(I);
print("STANDARD_BASIS_SECONDS");
timer-t;
print("STANDARD_BASIS_SIZE");
size(G);
print("LOCAL_DIMENSION");
dim(G);
"""
    output.write_text(source, encoding="utf-8", newline="\n")

    print(f"family_tangent_rank={family_jacobian.rank()}")
    print(f"family_tangent_minor={family_minor}")
    print(f"sample_point={POINT}")
    print(f"sample_pair_profile={profile}")
    print(f"incidence_jacobian_rank={incidence_jacobian.rank()}")
    print(f"fixed_coordinates={FIXED_COORDINATES}")
    print(f"retained_indices={RETAINED_INDICES}")
    print(f"slice_denominators={denominators}")
    print(f"slice_contents={contents}")
    print(f"graph_slice_source={output}")


if __name__ == "__main__":
    main()
