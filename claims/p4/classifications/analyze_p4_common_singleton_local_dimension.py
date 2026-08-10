#!/usr/bin/env python3
"""Build the exact integral local model for the common-singleton P4 family.

The emitted graph-slice ideal has integer coefficients.  The theorem verifier
computes one exact local standard basis modulo a prime and uses that result as
an integral height certificate; Krull's height theorem, not a finite-field
point census, supplies the characteristic-zero conclusion.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])
expose_claim_package(REPO_ROOT, "claims/p4/classifications")


import sympy as sp

from verify_p4_directed_zero_divisor_triangle_components import coefficients

ROOT = HERE
CERTIFICATE_PRIME = 32003
WORDS = tuple(itertools.product((0, 1), repeat=4))
ANCHOR = (0, 1, 1, 1)
POINT = (
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(-3),
    sp.Integer(-2),
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(-1),
    sp.Integer(-1),
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(-1),
    sp.Integer(2),
    sp.Integer(0),
    sp.Integer(0),
    sp.Integer(3),
    sp.Integer(-1),
)


def pivot01_planes(variables: tuple[sp.Symbol, ...]):
    planes = []
    for mode in range(4):
        a, b, c, d = variables[4 * mode : 4 * mode + 4]
        planes.append(sp.Matrix(((1, 0, a, b), (0, 1, c, d))))
    return tuple(planes)


def incidence_equations(
    plane_variables: tuple[sp.Symbol, ...],
    target_variables: tuple[sp.Symbol, ...],
):
    tensor = coefficients(pivot01_planes(plane_variables))
    equations = []
    for word in WORDS:
        if word == ANCHOR:
            continue
        target_monomial = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != ANCHOR[mode]
        )
        equations.append(
            sp.expand(tensor[word] - tensor[ANCHOR] * target_monomial)
        )
    return tuple(equations), tensor


def singular_string(expression: sp.Expr) -> str:
    return sp.sstr(expression).replace("**", "^")


def lowest_degree_part(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> sp.Expr:
    polynomial = sp.Poly(expression, *variables)
    minimum = min(sum(monomial) for monomial, _coefficient in polynomial.terms())
    return sp.Add(
        *(
            coefficient * sp.prod(variable**power for variable, power in zip(variables, monomial, strict=True))
            for monomial, coefficient in polynomial.terms()
            if sum(monomial) == minimum
        )
    )


def common_singleton_family(
    ell_2: sp.Expr,
    ell_3: sp.Expr,
    v1_2: sp.Expr,
    v1_3: sp.Expr,
    v2_2: sp.Expr,
):
    """Return the rational five-parameter common-singleton chart."""

    denominator = ell_2 + v1_2
    v2_3 = -(
        ell_2 * v1_3
        + ell_3 * v1_2
        + ell_3 * v2_2
        + v1_3 * v2_2
    ) / denominator
    polar = sp.Matrix(
        (
            (0, ell_3, ell_2),
            (ell_3, 0, 1),
            (ell_2, 1, 0),
        )
    )
    ell = sp.Matrix((1, ell_2, ell_3))
    v1 = sp.Matrix((1, v1_2, v1_3))
    v2 = sp.Matrix((1, v2_2, v2_3))
    v3_raw = (polar * v1).cross(polar * v2)
    v3 = sp.simplify(v3_raw / v3_raw[0])
    vectors = (ell, v1, v2, v3)
    planes = tuple(
        sp.Matrix(((1, 0, 0, 0), (0, *tuple(vector))))
        for vector in vectors
    )
    return planes, v2_3, v3


def squarefree_pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    pairs = tuple(itertools.combinations(range(4), 2))

    def product(left_row: int, right_row: int) -> sp.Matrix:
        return sp.Matrix(
            [
                left[left_row, i] * right[right_row, j]
                + left[left_row, j] * right[right_row, i]
                for i, j in pairs
            ]
        )

    return sp.Matrix.hstack(
        *(product(i, j) for i in range(2) for j in range(2))
    )


def main() -> None:
    ell_2, ell_3, v1_2, v1_3, v2_2 = sp.symbols(
        "ell_2 ell_3 v1_2 v1_3 v2_2"
    )
    parameters = (ell_2, ell_3, v1_2, v1_3, v2_2)
    parameter_sample = dict(zip(parameters, (-3, -2, -1, -1, -1), strict=True))
    family_planes, v2_3, v3 = common_singleton_family(*parameters)
    family_tensor = coefficients(family_planes)
    assert all(
        sp.factor(value) == 0
        for word, value in family_tensor.items()
        if word != ANCHOR
    )
    assert sp.factor(family_tensor[ANCHOR]).subs(parameter_sample) == 4
    family_coordinates = tuple(
        entry
        for plane in family_planes
        for entry in (plane[0, 2], plane[0, 3], plane[1, 2], plane[1, 3])
    )
    assert tuple(
        sp.factor(entry.subs(parameter_sample)) for entry in family_coordinates
    ) == POINT
    family_jacobian = sp.Matrix(family_coordinates).jacobian(parameters).subs(
        parameter_sample
    )
    assert family_jacobian.rank() == 5
    family_pivot_rows = tuple(family_jacobian.T.rref()[1])
    family_minor = sp.factor(
        family_jacobian.extract(family_pivot_rows, range(5)).det()
    )
    assert family_minor != 0

    z = tuple(sp.symbols("z0:16"))
    r = tuple(sp.symbols("r0:4"))
    x = tuple(sp.symbols("x0:20"))
    equations, tensor = incidence_equations(z, r)
    point_substitution = dict(zip(z, POINT, strict=True)) | dict(
        zip(r, (0, 0, 0, 0), strict=True)
    )

    # A small-height point on the same rational chart: (L,M,a,b,c)=
    # (-3,-2,-1,-1,-1), d=2, and v3=(1,3,-1).
    assert tensor[ANCHOR].subs(point_substitution) == 4
    assert all(equation.subs(point_substitution) == 0 for equation in equations)
    point_planes = tuple(plane.subs(parameter_sample) for plane in family_planes)
    pair_matrices = tuple(
        squarefree_pair_matrix(point_planes[left], point_planes[right])
        for left, right in itertools.combinations(range(4), 2)
    )
    assert tuple(matrix.rank() for matrix in pair_matrices) == (3,) * 6
    assert all(
        sp.Matrix(2, 2, tuple(matrix.nullspace()[0])).rank() == 1
        for matrix in pair_matrices
    )

    all_variables = (*z, *r)
    jacobian = sp.Matrix(equations).jacobian(all_variables).subs(point_substitution)
    assert jacobian.rank() == 10

    shift = {
        variable: value + local
        for variable, value, local in zip(
            all_variables, (*POINT, 0, 0, 0, 0), x, strict=True
        )
    }
    local_equations = tuple(sp.expand(equation.subs(shift)) for equation in equations)
    assert all(equation.subs(dict.fromkeys(x, 0)) == 0 for equation in local_equations)
    tangent_generators = tuple(
        lowest_degree_part(equation, x) for equation in local_equations
    )

    output = ROOT / "tmp" / "p4_common_singleton_local_dimension.sing"
    output.parent.mkdir(exist_ok=True)
    variable_names = ",".join(map(str, x))
    ideal = ",\n  ".join(singular_string(equation) for equation in local_equations)
    source = f'''// Generated by {Path(__file__).name}
ring R=0,({variable_names}),ds;
ideal I=
  {ideal};
int t=timer;
ideal G=std(I);
print("STANDARD_BASIS_SECONDS");
timer-t;
print("STANDARD_BASIS_SIZE");
size(G);
print("LOCAL_DIMENSION");
dim(G);
'''
    output.write_text(source, encoding="utf-8", newline="\n")
    tangent_output = ROOT / "tmp" / "p4_common_singleton_tangent_generators.sing"
    tangent_ideal = ",\n  ".join(
        singular_string(equation) for equation in tangent_generators
    )
    tangent_source = f'''// Generated by {Path(__file__).name}
ring R=0,({variable_names}),dp;
ideal H=
  {tangent_ideal};
int t=timer;
ideal G=std(H);
print("TANGENT_GENERATOR_BASIS_SECONDS");
timer-t;
print("TANGENT_GENERATOR_BASIS_SIZE");
size(G);
print("TANGENT_GENERATOR_IDEAL_DIMENSION");
dim(G);
'''
    tangent_output.write_text(tangent_source, encoding="utf-8", newline="\n")

    # Eliminate the ten independent linear initial equations.  Five of the
    # remaining tangent coordinates are free, and all nonlinear initial
    # forms live in the other five.  Their projective zero set identifies
    # the finitely many candidate transverse arcs that a higher-order local
    # calculation must either lift or obstruct.
    linear_parts = tuple(
        equation
        for equation in tangent_generators
        if sp.Poly(equation, *x).total_degree() == 1
    )
    linear_matrix, _zero = sp.linear_eq_to_matrix(linear_parts, x)
    row_reduced, pivot_columns = linear_matrix.rref()
    free_columns = tuple(index for index in range(20) if index not in pivot_columns)
    linear_solution = {
        x[pivot]: -sum(row_reduced[row, column] * x[column] for column in free_columns)
        for row, pivot in enumerate(pivot_columns)
    }
    reduced_nonlinear = tuple(
        sp.factor(equation.subs(linear_solution))
        for equation in tangent_generators
        if sp.factor(equation.subs(linear_solution)) != 0
    )
    active_columns = tuple(
        column
        for column in free_columns
        if any(equation.has(x[column]) for equation in reduced_nonlinear)
    )
    inactive_columns = tuple(column for column in free_columns if column not in active_columns)
    assert active_columns == (12, 13, 17, 18, 19)
    assert inactive_columns == (7, 10, 11, 14, 15)
    q = tuple(sp.symbols("q0:5"))
    active_substitution = {
        x[column]: variable for column, variable in zip(active_columns, q, strict=True)
    }
    transverse_generators = tuple(
        sp.factor(equation.subs(active_substitution)) for equation in reduced_nonlinear
    )
    transverse_ideal = ",\n  ".join(
        singular_string(equation) for equation in transverse_generators
    )
    transverse_output = ROOT / "tmp" / "p4_common_singleton_transverse_tangent.sing"
    transverse_source = f'''// Generated by {Path(__file__).name}
LIB "primdec.lib";
ring S=0,(q0,q1,q2,q3,q4),dp;
ideal H=
  {transverse_ideal};
ideal G=std(H);
print("TRANSVERSE_TANGENT_DIMENSION");
dim(G);
print("TRANSVERSE_TANGENT_BASIS_SIZE");
size(G);
list P=minAssGTZ(H);
print("TRANSVERSE_MINIMAL_PRIME_COUNT");
size(P);
print("TRANSVERSE_MINIMAL_PRIMES");
P;
'''
    transverse_output.write_text(transverse_source, encoding="utf-8", newline="\n")

    # Precondition the full local ideal before asking Singular for a standard
    # basis: make the ten independent linear jets monic in their pivot
    # variables, eliminate all linear jets from the other five generators,
    # and order the pivot variables first.  This is an invertible constant
    # row operation and a variable permutation, so it preserves the germ.
    full_linear_matrix = sp.Matrix(local_equations).jacobian(x).subs(dict.fromkeys(x, 0))
    independent_rows = tuple(full_linear_matrix.T.rref()[1])
    pivot_minor = full_linear_matrix.extract(independent_rows, pivot_columns)
    pivot_determinant = sp.factor(pivot_minor.det())
    assert pivot_determinant == -36864
    assert int(pivot_determinant) % CERTIFICATE_PRIME != 0
    inverse_minor = pivot_minor.inv()
    normalized_generators = tuple(
        sp.expand(
            sum(
                inverse_minor[row, column] * local_equations[independent_rows[column]]
                for column in range(10)
            )
        )
        for row in range(10)
    )
    remaining_rows = tuple(index for index in range(15) if index not in independent_rows)
    residual_generators = tuple(
        sp.expand(
            local_equations[index]
            - sum(
                full_linear_matrix[index, pivot] * normalized_generators[column]
                for column, pivot in enumerate(pivot_columns)
            )
        )
        for index in remaining_rows
    )
    preconditioned = (*normalized_generators, *residual_generators)
    preconditioned_linear_matrix, _zero = sp.linear_eq_to_matrix(
        tuple(lowest_degree_part(equation, x) for equation in preconditioned[:10]),
        x,
    )
    assert preconditioned_linear_matrix[:, pivot_columns] == sp.eye(10)
    assert all(
        lowest_degree_part(equation, x) == 0
        if equation == 0
        else sp.Poly(equation, *x).terms()[0][0] != ()
        for equation in residual_generators
    )
    assert all(
        not any(
            term_degree == 1
            for term_degree in (sum(monomial) for monomial, _coefficient in sp.Poly(equation, *x).terms())
        )
        for equation in residual_generators
    )
    ordered_columns = (*pivot_columns, *free_columns)
    y = tuple(sp.symbols("y0:20"))
    ordered_substitution = {
        x[column]: variable
        for column, variable in zip(ordered_columns, y, strict=True)
    }
    optimized_generators = tuple(
        sp.expand(equation.subs(ordered_substitution)) for equation in preconditioned
    )
    optimized_ideal = ",\n  ".join(
        singular_string(equation) for equation in optimized_generators
    )
    optimized_output = ROOT / "tmp" / "p4_common_singleton_local_optimized.sing"
    optimized_source = f'''// Generated by {Path(__file__).name}
ring R=0,({','.join(map(str, y))}),ds;
ideal I=
  {optimized_ideal};
int t=timer;
ideal G=std(I);
print("OPTIMIZED_STANDARD_BASIS_SECONDS");
timer-t;
print("OPTIMIZED_STANDARD_BASIS_SIZE");
size(G);
print("OPTIMIZED_LOCAL_DIMENSION");
dim(G);
'''
    optimized_output.write_text(optimized_source, encoding="utf-8", newline="\n")

    # A five-hyperplane slice transverse to the explicit family tangent.
    # If this quotient is zero-dimensional, Krull's principal ideal theorem
    # gives dim(local incidence)<=5; the five-parameter family gives equality.
    slice_variables = (y[10], y[11], y[12], y[15], y[16])
    retained_variables = tuple(variable for variable in y if variable not in slice_variables)
    sliced_generators = tuple(
        sp.expand(equation.subs(dict.fromkeys(slice_variables, 0)))
        for equation in optimized_generators
    )
    sliced_ideal = ",\n  ".join(
        singular_string(equation) for equation in sliced_generators if equation != 0
    )
    sliced_output = ROOT / "tmp" / "p4_common_singleton_local_slice.sing"
    sliced_source = f'''// Generated by {Path(__file__).name}
ring R=0,({','.join(map(str, retained_variables))}),ds;
ideal I=
  {sliced_ideal};
int t=timer;
ideal G=std(I);
print("SLICED_STANDARD_BASIS_SECONDS");
timer-t;
print("SLICED_STANDARD_BASIS_SIZE");
size(G);
print("SLICED_LOCAL_DIMENSION");
dim(G);
'''
    sliced_output.write_text(sliced_source, encoding="utf-8", newline="\n")

    active_slice_variables = (y[13], y[14], y[17], y[18], y[19])
    slice_matrix = sp.Matrix(
        (
            (1, 2, -1, 3, 1),
            (2, -1, 1, 1, 3),
            (-1, 1, 3, 2, 1),
            (3, 1, 2, -1, 2),
            (1, 3, 2, 2, -1),
        )
    )
    graph_slice_substitution = {
        variable: sum(
            slice_matrix[row, column] * active_slice_variables[column]
            for column in range(5)
        )
        for row, variable in enumerate(slice_variables)
    }
    graph_sliced_rational_generators = tuple(
        sp.expand(equation.subs(graph_slice_substitution))
        for equation in optimized_generators
    )
    cleared_data = tuple(
        sp.Poly(equation, *retained_variables).clear_denoms()
        for equation in graph_sliced_rational_generators
    )
    cleared_denominators = tuple(int(denominator) for denominator, _ in cleared_data)
    assert cleared_denominators == (
        96,
        192,
        2,
        4,
        48,
        4,
        6,
        48,
        64,
        4,
        1,
        1,
        1,
        1,
        1,
    )
    assert all(value % CERTIFICATE_PRIME != 0 for value in cleared_denominators)
    cleared_contents = tuple(int(polynomial.primitive()[0]) for _, polynomial in cleared_data)
    assert cleared_contents == (1,) * 15
    graph_sliced_generators = tuple(
        polynomial.as_expr() for _, polynomial in cleared_data
    )

    # The five graph equations restrict independently to the explicit family
    # tangent.  This transversality is not needed for the height upper bound,
    # but it independently checks that the chosen slice has the intended
    # codimension at the certificate point.
    full_family_jacobian = family_jacobian.col_join(sp.zeros(4, 5))
    ordered_family_jacobian = full_family_jacobian.extract(
        ordered_columns, range(5)
    )
    y_positions = {variable: index for index, variable in enumerate(y)}
    slice_rows = []
    for row, inactive_variable in enumerate(slice_variables):
        coefficients_row = [sp.Integer(0)] * 20
        coefficients_row[y_positions[inactive_variable]] = 1
        for column, active_variable in enumerate(active_slice_variables):
            coefficients_row[y_positions[active_variable]] -= slice_matrix[row, column]
        slice_rows.append(coefficients_row)
    slice_restriction_determinant = sp.factor(
        (sp.Matrix(slice_rows) * ordered_family_jacobian).det()
    )
    assert slice_restriction_determinant == sp.Rational(1, 4)
    graph_sliced_ideal = ",\n  ".join(
        singular_string(equation)
        for equation in graph_sliced_generators
        if equation != 0
    )
    graph_sliced_output = ROOT / "tmp" / "p4_common_singleton_local_graph_slice.sing"
    graph_sliced_source = f'''// Generated by {Path(__file__).name}
ring R=0,({','.join(map(str, retained_variables))}),ds;
ideal I=
  {graph_sliced_ideal};
int t=timer;
ideal G=std(I);
print("GRAPH_SLICED_STANDARD_BASIS_SECONDS");
timer-t;
print("GRAPH_SLICED_STANDARD_BASIS_SIZE");
size(G);
print("GRAPH_SLICED_LOCAL_DIMENSION");
dim(G);
'''
    graph_sliced_output.write_text(
        graph_sliced_source, encoding="utf-8", newline="\n"
    )

    print(f"incidence_equations={len(equations)}")
    print(f"family_v2_3={sp.factor(v2_3)}")
    print(f"family_v3={tuple(map(sp.factor, v3))}")
    print(f"family_tangent_rank={family_jacobian.rank()}")
    print(f"family_tangent_minor={family_minor}")
    print(f"jacobian_rank={jacobian.rank()}")
    print(f"tangent_dimension={20 - jacobian.rank()}")
    print(
        "tangent_generator_degrees="
        + str(tuple(sp.Poly(equation, *x).total_degree() for equation in tangent_generators))
    )
    print(f"singular_source={output}")
    print(f"tangent_singular_source={tangent_output}")
    print(f"linear_pivot_columns={pivot_columns}")
    print(f"free_tangent_columns={free_columns}")
    print(f"active_transverse_columns={active_columns}")
    print(f"transverse_singular_source={transverse_output}")
    print(f"independent_generator_rows={independent_rows}")
    print(f"pivot_determinant={pivot_determinant}")
    print(f"optimized_singular_source={optimized_output}")
    print(f"slice_variables={slice_variables}")
    print(f"sliced_singular_source={sliced_output}")
    print(f"graph_slice_matrix={tuple(map(tuple, slice_matrix.tolist()))}")
    print(f"graph_slice_cleared_denominators={cleared_denominators}")
    print(f"graph_slice_cleared_contents={cleared_contents}")
    print(f"graph_slice_family_restriction_determinant={slice_restriction_determinant}")
    print(f"graph_sliced_singular_source={graph_sliced_output}")


if __name__ == "__main__":
    main()
