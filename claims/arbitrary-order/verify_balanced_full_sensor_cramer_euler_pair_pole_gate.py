"""Primary exact checks for the balanced Cramer--Euler pair-pole gate."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

Vertices = tuple[int, ...]
Edge = tuple[int, int]
Weights = dict[Edge, sp.Expr]
SquareFree = dict[int, sp.Expr]


def edge(left: int, right: int) -> Edge:
    """Return an ordered representation of an unordered edge."""
    return (left, right) if left < right else (right, left)


def hafnian(vertices: Vertices, weights: Weights) -> sp.Expr:
    """Expand a labelled hafnian by the partner of the first vertex."""
    if not vertices:
        return sp.Integer(1)
    first = vertices[0]
    total = sp.Integer(0)
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        total += weights[edge(first, partner)] * hafnian(remainder, weights)
    return sp.expand(total)


def sf_add(left: SquareFree, right: SquareFree) -> SquareFree:
    """Add two elements of the vertex-square-free algebra."""
    result = left.copy()
    for mask, value in right.items():
        result[mask] = sp.expand(result.get(mask, 0) + value)
        if result[mask] == 0:
            del result[mask]
    return result


def sf_scale(value: SquareFree, scalar: sp.Expr) -> SquareFree:
    """Scale a square-free element."""
    return {
        mask: sp.expand(scalar * coefficient)
        for mask, coefficient in value.items()
        if coefficient != 0
    }


def sf_multiply(left: SquareFree, right: SquareFree) -> SquareFree:
    """Multiply and kill every product that repeats a vertex."""
    result: SquareFree = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(
                result.get(mask, 0) + left_value * right_value
            )
    return {mask: value for mask, value in result.items() if value != 0}


def sf_euler(value: SquareFree) -> SquareFree:
    """Apply the vertex-degree Euler derivation."""
    return {
        mask: sp.expand(mask.bit_count() * coefficient)
        for mask, coefficient in value.items()
        if mask
    }


def assert_cramer_residuals_and_overlap() -> dict[str, sp.Expr]:
    """Check selected rows, an unused target residual, and chart overlap."""
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    x, y = sp.symbols("x y")
    gamma = sp.Matrix(((a, b), (c, d), (e, f)))
    solution = sp.Matrix((x, y))
    target = gamma * solution

    first_rows = gamma[:2, :]
    first_target = target[:2, :]
    beta = sp.expand(first_rows.det())
    numerator = first_rows.adjugate() * first_target
    assert (numerator - beta * solution).applyfunc(sp.expand) == sp.zeros(2, 1)
    assert (gamma * numerator - beta * target).applyfunc(sp.expand) == sp.zeros(
        3, 1
    )

    other_rows = gamma[[0, 2], :]
    other_target = target[[0, 2], :]
    other_beta = sp.expand(other_rows.det())
    other_numerator = other_rows.adjugate() * other_target
    overlap = other_beta * numerator - beta * other_numerator
    assert overlap.applyfunc(sp.expand) == sp.zeros(2, 1)

    j0, j1, j2 = sp.symbols("j0 j1 j2")
    arbitrary_target = sp.Matrix((j0, j1, j2))
    selected_target = arbitrary_target[:2, :]
    candidate = first_rows.adjugate() * selected_target
    unused_residual = sp.expand((gamma * candidate - beta * arbitrary_target)[2])
    augmented = gamma.row_join(arbitrary_target)
    assert sp.expand(unused_residual + augmented.det()) == 0
    return {"beta": beta, "other_beta": other_beta}


def generic_weights(vertex_count: int, prefix: str) -> Weights:
    """Create one independent symbol for every labelled edge."""
    return {
        pair: sp.Symbol(f"{prefix}{pair[0]}{pair[1]}")
        for pair in combinations(range(vertex_count), 2)
    }


def assert_symmetric_hafnian_recurrence() -> dict[int, int]:
    """Verify the matching multiplicity through six generic labels."""
    weights = generic_weights(6, "w")
    counts: dict[int, int] = {}
    for size in (2, 4, 6):
        checked = 0
        for subset in combinations(range(6), size):
            moment = hafnian(subset, weights)
            right = sp.Integer(0)
            for pair in combinations(subset, 2):
                remainder = tuple(vertex for vertex in subset if vertex not in pair)
                right += weights[edge(*pair)] * hafnian(remainder, weights)
            assert sp.expand((size // 2) * moment - right) == 0
            checked += 1
        counts[size] = checked
    assert counts == {2: 15, 4: 15, 6: 1}
    return counts


def assert_square_free_euler_identity() -> int:
    """Check D exp(Q)=2 Q exp(Q) in the six-vertex quotient."""
    weights = generic_weights(6, "q")
    quadratic: SquareFree = {
        (1 << left) | (1 << right): value
        for (left, right), value in weights.items()
    }
    exponential: SquareFree = {0: sp.Integer(1)}
    power: SquareFree = {0: sp.Integer(1)}
    for degree in range(1, 4):
        power = sf_multiply(power, quadratic)
        exponential = sf_add(
            exponential,
            sf_scale(power, sp.Rational(1, sp.factorial(degree))),
        )

    left = sf_euler(exponential)
    right = sf_scale(sf_multiply(quadratic, exponential), sp.Integer(2))
    assert set(left) == set(right)
    assert all(sp.expand(left[mask] - right[mask]) == 0 for mask in left)

    for mask, coefficient in exponential.items():
        vertices = tuple(index for index in range(6) if mask & (1 << index))
        if len(vertices) % 2 == 0:
            assert sp.expand(coefficient - hafnian(vertices, weights)) == 0
    return len(exponential)


def assert_denominator_clearing() -> sp.Expr:
    """Check that the cleared Euler equation has exactly one beta on the left."""
    beta = sp.Symbol("beta", nonzero=True)
    vertices = (0, 1, 2, 3)
    numerators = generic_weights(4, "v")
    top = sp.Symbol("v0123")
    rational_equation = 2 * top / beta
    cleared_right = sp.Integer(0)
    for pair in combinations(vertices, 2):
        remainder = tuple(vertex for vertex in vertices if vertex not in pair)
        product = numerators[edge(*pair)] * numerators[edge(*remainder)]
        rational_equation -= product / beta**2
        cleared_right += product
    cleared = sp.expand(2 * beta * top - cleared_right)
    assert sp.cancel(rational_equation - cleared / beta**2) == 0
    assert sp.degree(cleared, beta) == 1
    return cleared


def assert_pair_regularity_propagates() -> dict[int, int]:
    """Check v_Q=beta*haf(W_Q) obeys every cleared recurrence."""
    beta = sp.Symbol("beta", nonzero=True)
    weights = generic_weights(6, "p")
    numerators: dict[Vertices, sp.Expr] = {(): beta}
    for size in (2, 4, 6):
        for subset in combinations(range(6), size):
            numerators[subset] = sp.expand(beta * hafnian(subset, weights))

    counts: dict[int, int] = {}
    for size in (4, 6):
        checked = 0
        for subset in combinations(range(6), size):
            right = sp.Integer(0)
            for pair in combinations(subset, 2):
                remainder = tuple(vertex for vertex in subset if vertex not in pair)
                right += numerators[tuple(pair)] * numerators[remainder]
            left = (size // 2) * beta * numerators[subset]
            assert sp.expand(left - right) == 0
            assert sp.rem(numerators[subset], beta, beta) == 0
            checked += 1
        counts[size] = checked
    return counts


def assert_pole_counterexample() -> dict[str, sp.Expr]:
    """Retain the exact normalized Wick deck with a pair pole."""
    t = sp.Symbol("t")
    beta = t
    v12 = sp.Integer(1)
    v34 = t**2
    v1234 = t
    assert sp.expand(2 * beta * v1234 - v12 * v34 - v34 * v12) == 0

    c12 = sp.cancel(v12 / beta)
    c34 = sp.cancel(v34 / beta)
    c1234 = sp.cancel(v1234 / beta)
    assert c12 == 1 / t
    assert c34 == t
    assert c1234 == 1
    assert sp.limit(c12, t, 0, dir="+") == sp.oo
    assert sp.expand(c1234 - c12 * c34) == 0
    return {"C12": c12, "C34": c34, "C1234": c1234}


def main() -> None:
    cramer = assert_cramer_residuals_and_overlap()
    recurrence = assert_symmetric_hafnian_recurrence()
    square_free_terms = assert_square_free_euler_identity()
    cleared = assert_denominator_clearing()
    propagation = assert_pair_regularity_propagates()
    pole = assert_pole_counterexample()
    print("balanced Cramer--Euler pair-pole primary checks: PASS")
    print(f"  Cramer minors: {cramer}")
    print(f"  generic recurrence subsets: {recurrence}")
    print(f"  square-free exponential terms: {square_free_terms}")
    print(f"  cleared four-label identity: {cleared}")
    print(f"  pair-regular propagation: {propagation}")
    print(f"  retained pole chart: {pole}")


if __name__ == "__main__":
    main()
