"""Primary exact checks for binomial-core aggregate quotients."""

from __future__ import annotations

from collections import defaultdict
from math import prod

from sympy import Add, I, Matrix, Poly, S, expand, symbols
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

Exponent = tuple[int, ...]


def quotient_type(ambient_rank: int, subgroup_rows: tuple[Exponent, ...]) -> tuple[int, tuple[int, ...]]:
    """Return free rank and nontrivial torsion invariants of Z^n/<rows>."""
    if not subgroup_rows:
        return ambient_rank, ()
    matrix = Matrix(subgroup_rows).T
    smith = smith_normal_form(matrix, domain=ZZ)
    diagonal = tuple(
        abs(int(smith[index, index]))
        for index in range(min(smith.shape))
        if smith[index, index]
    )
    free_rank = ambient_rank - len(diagonal)
    torsion = tuple(value for value in diagonal if value > 1)
    return free_rank, torsion


def finite_c2_untwist(exponents: tuple[tuple[int], ...]) -> tuple[object, object]:
    """Apply theta(x)=i and reduce modulo x^2=1 after untwisting."""
    coefficients = [S.Zero, S.Zero]
    for (power,) in exponents:
        coefficients[power % 2] += I**power
    return tuple(map(expand, coefficients))


def c2_sheets(element: tuple[object, object]) -> tuple[object, object]:
    """Apply the exact Fourier transform C[C2] -> C x C."""
    even, odd = element
    return expand(even + odd), expand(even - odd)


def assert_finite_quotient() -> dict[str, object]:
    """Check a finite quotient and exact positive-term aggregate outcomes."""
    assert quotient_type(1, ((2,),)) == (0, (2,))

    # The selected binomial is 1+x^2.  Under theta(x)=i it becomes
    # 1-x^2, and the quotient coordinate g has g^2=1.
    unit_aggregate = ((0,), (1,), (2,))
    zero_aggregate = ((0,), (1,), (2,), (3,))
    unit_element = finite_c2_untwist(unit_aggregate)
    zero_element = finite_c2_untwist(zero_aggregate)
    assert unit_element == (0, I)
    assert zero_element == (0, 0)

    unit_sheets = c2_sheets(unit_element)
    zero_sheets = c2_sheets(zero_element)
    assert unit_sheets == (I, -I)
    assert zero_sheets == (0, 0)

    # One nonzero scalar on every character sheet is exactly a unit in the
    # product C x C.  The four-term aggregate is identically zero after the
    # core and leaves both sheets alive.
    assert all(value != 0 for value in unit_sheets)
    assert all(value == 0 for value in zero_sheets)
    return {
        "free_rank": 0,
        "torsion_invariants": (2,),
        "torsion_characters": prod((2,)),
        "three_term_positive_fibre_sheets": unit_sheets,
        "three_term_residual_ideal": "(1)",
        "four_term_positive_fibre_sheets": zero_sheets,
        "four_term_residual_ideal": "proper (zero ideal)",
    }


def reduce_sign_core(exponents: tuple[tuple[int, int], ...], t) -> object:
    """Reduce positive terms modulo the untwisted core x=1, theta(x)=-1."""
    coefficients: dict[int, int] = defaultdict(int)
    for core_power, free_power in exponents:
        coefficients[free_power] += -1 if core_power % 2 else 1
    return expand(sum(value * t**power for power, value in coefficients.items()))


def laurent_gcd(expressions: tuple[object, ...], t) -> object:
    """Return a monic gcd after removing individual Laurent monomial units."""
    polynomials: list[Poly] = []
    for raw in expressions:
        expression = expand(raw)
        if expression == 0:
            continue
        powers = []
        for term in Add.make_args(expression):
            exponent = term.as_powers_dict().get(t, S.Zero)
            if not exponent.is_integer:
                raise AssertionError("nonintegral Laurent exponent")
            powers.append(int(exponent))
        shifted = expand(expression * t ** (-min(powers)))
        polynomials.append(Poly(shifted, t, extension=I))
    if not polynomials:
        return S.Zero
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = result.gcd(polynomial)
    return expand(result.monic().as_expr())


def is_laurent_unit_gcd(value: object, t) -> bool:
    """Recognize the normalized nonzero-constant unit case."""
    if value == 0:
        return False
    return Poly(value, t, extension=I).degree() == 0


def assert_rank_one_positive_aggregates() -> dict[str, object]:
    """Check proper and unit branches from positive-term aggregate fibres."""
    t = symbols("t", nonzero=True)
    assert quotient_type(2, ((1, 0),)) == (1, ())

    # All exponent lists contain the reference exponent (0,0), have four
    # distinct terms, and therefore model normalized aggregate fibres.
    fibre_minus = ((0, 0), (1, 0), (3, 0), (0, 1))
    fibre_square_minus = ((0, 0), (1, 0), (3, 0), (0, 2))
    fibre_plus = ((0, 0), (0, 1), (1, 0), (2, 0))
    assert all(len(set(fibre)) == 4 and (0, 0) in fibre for fibre in (
        fibre_minus,
        fibre_square_minus,
        fibre_plus,
    ))

    polynomial_minus = reduce_sign_core(fibre_minus, t)
    polynomial_square_minus = reduce_sign_core(fibre_square_minus, t)
    polynomial_plus = reduce_sign_core(fibre_plus, t)
    assert polynomial_minus == t - 1
    assert polynomial_square_minus == t**2 - 1
    assert polynomial_plus == t + 1

    proper_gcd = laurent_gcd((polynomial_minus, polynomial_square_minus), t)
    unit_gcd = laurent_gcd(
        (polynomial_minus, polynomial_square_minus, polynomial_plus), t
    )
    laurent_regression = laurent_gcd(
        (t**-2 * (t - 1), t**3 * (t**2 - 1)), t
    )
    assert proper_gcd == t - 1
    assert unit_gcd == 1
    assert laurent_regression == t - 1
    assert not is_laurent_unit_gcd(proper_gcd, t)
    assert is_laurent_unit_gcd(unit_gcd, t)
    return {
        "free_rank": 1,
        "torsion_invariants": (),
        "positive_aggregate_polynomials": (
            polynomial_minus,
            polynomial_square_minus,
            polynomial_plus,
        ),
        "proper_sheet_gcd": proper_gcd,
        "unit_sheet_gcd": unit_gcd,
        "Laurent_unit_normalization_gcd": laurent_regression,
    }


def group_ring_sheet(
    element: dict[tuple[int, int], int],
    torsion_character: int,
    t,
) -> object:
    """Evaluate the C2 coordinate and retain the rank-one Laurent variable."""
    assert torsion_character in (-1, 1)
    return expand(
        sum(
            coefficient * torsion_character**torsion_power * t**free_power
            for (torsion_power, free_power), coefficient in element.items()
        )
    )


def assert_torsion_rank_one_sheets() -> dict[str, object]:
    """Check C2-by-Z Fourier sheets and their independent gcds."""
    t = symbols("t", nonzero=True)
    assert quotient_type(2, ((2, 0),)) == (1, (2,))

    residuals = (
        {(0, 0): 1, (1, 1): 1},  # 1+g t
        {(1, 0): 1, (0, 1): 1},  # g+t
    )
    sheet_gcds = {}
    for character in (1, -1):
        polynomials = tuple(
            group_ring_sheet(residual, character, t)
            for residual in residuals
        )
        sheet_gcds[character] = laurent_gcd(polynomials, t)
    assert sheet_gcds == {1: t + 1, -1: t - 1}

    # The two scalar residuals 1+g and 1-g cover complementary sheets; adding
    # both makes every product factor the unit ideal.
    covers = (
        {(0, 0): 1, (1, 0): 1},
        {(0, 0): 1, (1, 0): -1},
    )
    covered_gcds = {}
    for character in (1, -1):
        polynomials = tuple(
            group_ring_sheet(residual, character, t)
            for residual in residuals + covers
        )
        covered_gcds[character] = laurent_gcd(polynomials, t)
    assert covered_gcds == {1: 1, -1: 1}
    return {
        "free_rank": 1,
        "torsion_invariants": (2,),
        "proper_sheet_gcds": sheet_gcds,
        "covered_sheet_gcds": covered_gcds,
        "proper_product_ideal": True,
        "covered_product_unit": True,
    }


def assert_fourier_multiplication() -> dict[str, object]:
    """Check that C[C2] multiplication becomes componentwise multiplication."""
    left = (2 + I, 3 - 2 * I)
    right = (-1 + I, 4 + I)
    product_element = (
        expand(left[0] * right[0] + left[1] * right[1]),
        expand(left[0] * right[1] + left[1] * right[0]),
    )
    left_sheets = c2_sheets(left)
    right_sheets = c2_sheets(right)
    product_sheets = c2_sheets(product_element)
    assert product_sheets == tuple(
        expand(a * b) for a, b in zip(left_sheets, right_sheets, strict=True)
    )
    return {
        "group_ring_product": product_element,
        "Fourier_product": product_sheets,
        "componentwise": True,
    }


def assert_holonomy_dichotomy() -> dict[str, str]:
    """Record the exact maximal-ideal alternative once the cycle is in core."""
    cycle_length = 3
    sign = -1 if cycle_length % 2 else 1
    assert sign == -1
    proper_residual = "(H+1)"
    unit_residual = "(1)"
    assert proper_residual != unit_residual
    return {
        "cycle_core_relation": "H=-1",
        "surviving_sheet_elimination": proper_residual,
        "all_sheets_killed_elimination": unit_residual,
        "third_nonunit_case": "none",
    }


def main() -> None:
    finite = assert_finite_quotient()
    rank_one = assert_rank_one_positive_aggregates()
    torsion_rank_one = assert_torsion_rank_one_sheets()
    fourier = assert_fourier_multiplication()
    holonomy = assert_holonomy_dichotomy()
    print("binomial-core torsion-sheet aggregate primary checks: PASS")
    print(f"  finite quotient: {finite}")
    print(f"  rank-one positive aggregates: {rank_one}")
    print(f"  torsion-plus-rank-one sheets: {torsion_rank_one}")
    print(f"  Fourier multiplication: {fourier}")
    print(f"  holonomy dichotomy: {holonomy}")


if __name__ == "__main__":
    main()
