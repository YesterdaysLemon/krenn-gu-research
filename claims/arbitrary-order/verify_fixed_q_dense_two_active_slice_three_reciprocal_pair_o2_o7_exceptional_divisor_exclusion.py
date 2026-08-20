"""Primary 945-match derivation for the GLD61 O2/O7 closure."""
from __future__ import annotations

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion as base

U, V, W = base.U, base.V, base.W
Z = sp.symbols("z")


def rows(value):
    return tuple(tuple(item.split(":")) for item in value.split(","))


K_SEED0 = rows("1000:0100,0100:0010,1100:0000,0010:0010,1000:1000,0101:0000,1001:0000,0110:0000,0011:0000,0100:1000,1000:0010,1010:0000,0100:0100,0002:0002")
K_SEED2 = rows("1000:0100,0010:0010,1000:1000,0100:0010,0100:1000,1000:0010,0100:0100,0002:0002,0200:0200,1100:0000,0101:0000,1010:0000,0011:0000,1001:0000")
K_SEED4 = rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,1001:1001,0101:0101,1100:1100,1020:1020,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,1101:1101")

CASES = {
    "u_minus_a": (rows("0100:0100,1000:1000,0100:0010,1000:0010,0100:1000,1000:0100,0010:0010,2000:2000,0002:0002,0110:0000,1010:0000,0101:0000,1001:0000,0011:0000"), 3*V*W*(V-1)*(W-1)**3*(W+1)),
    "u_minus_b": (rows("1000:1000,0100:0100,0010:0010,0200:0200,0020:0020,2000:2000,0002:0002,1010:1010,1100:1100,0110:0110,1020:1020,1200:1200,0102:0102,0012:0012,0120:0120,1110:1110"), 2*W*(V-1)*(W-1)*(3*W-2)*(V*W+V-W+1)),
    "sum_zero_a": (rows("1101:0010,1011:0100,0110:0000,1001:0000,1000:0010,0000:0110,1000:0100,1010:0000,1100:0000,1010:0110,1002:0012"), 2*U**3*(U*W-1)),
    "sum_zero_b": (K_SEED2, 2*U**3*W**2*(U-1)*(W-2)*(U*W+1)),
    "sum_zero_c": (K_SEED4, (U-1)*(U*W+1)*(U*W-W-1)*(2*U*W-U-W+1)),
    "v_minus_two_a": (K_SEED2, 16*U*W**2*(U-1)**2*(W-2)*(U*W+1)),
    "v_minus_two_b": (K_SEED0, 2*U*W*(U*W-1)*(U*W+1)*(U**3*W+2*U**2*W**2-10*U**2*W+3*U**2+U*W**2+16*U*W-12*U-6*W**2-5*W+6)),
    "v_minus_two_c": (K_SEED4, (U-1)*(W-1)*(U*W+1)*(U*W-2*W-1)*(2*U*W-U-W+1)),
    "uw_minus_a": (rows("0000:0101,0000:0011,0100:0100,1000:1000,0001:0001,0100:0010,1000:0010,0100:1000,1000:0100,0010:0010,0200:0200,0110:0000,1010:0000,0101:0000,0101:0101,1001:0011,1002:0102"), 4*U**3*V**2*(U-1)*(U+1)*(2*U+1)),
    "uw_minus_b": (rows("0101:0000,1001:0000,0110:0000,1010:0000,1100:0000,1000:0010,1000:0100,0100:0100,0100:0010,0100:1000,0001:0001,1000:1000,1011:1000,1002:1002"), 2*U*V**2*(U**2-2*U-1)*(U**2+U-1)),
    "sum_minus_one_a": (rows("1101:0010,1011:0100,0110:0000,0100:1000,1001:0000,1000:0010,1000:0100,0000:1010,0100:0010,0110:1010,0100:1110,1010:0110,1100:0110,1002:0012"), U**2*W**2*(U-1)*(U+1)**2*(2*U+1)*(W+1)),
    "sum_minus_one_b": (rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,1001:1001,0101:0101,1100:1100,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,1101:1101"), W*(U-1)*(U+W)*(U*W+1)*(2*U*W-U-W+1)),
    "sum_minus_one_c": (K_SEED2, 2*U*W**2*(U-1)**2*(U+1)**2*(W-2)*(U*W+1)),
    "mixed_a": (K_SEED2, 2*U*V**2*(U-1)**2*(2*U+V)*(V+1)**2*(2*U+3*V+1)),
    "mixed_b": (rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,0110:0110,0101:0101,0011:0011,1020:1020,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,0111:0111"), V*(U-1)*(V+1)*(U**2+2*U*V+2*U-1)*(U**2+3*U*V+2*U+V**2-1)),
    "mixed_c": (K_SEED0, 2*U*V**2*(U-1)*(V+1)*(U*V+2*U+V)*(U**2+2*U*V-2*U-4*V-1)*(U**2+2*U*V+U-V-1)),
    "sum_point": (rows("0001:0001,1000:1000,0101:0000,1001:0000,0110:0000,0100:1000,1010:0000,0011:0011,1002:1002"), sp.Integer(6)),
}


def parameters(case):
    if case.startswith("u_minus"):
        return sp.Integer(-1), V, W
    if case.startswith("sum_zero"):
        return U, -U, W
    if case.startswith("v_minus_two"):
        return U, sp.Integer(-2), W
    if case.startswith("uw_minus"):
        return U, V, -1/U
    if case.startswith("sum_minus_one"):
        return U, -U-1, W
    if case.startswith("mixed"):
        return U, V, -(V+1)/(U+V)
    return sp.Rational(-1, 2), sp.Rational(-1, 2), sp.Integer(2)


def amplitudes(case):
    u, v, w = parameters(case)
    return {
        (0, 0, 1): u, (1, 1, 0): sp.cancel(u/(u-1)),
        (0, 0, 2): v, (1, 2, 0): sp.cancel(v/(v-1)),
        (0, 1, 0): w, (1, 0, 1): sp.cancel(w/(w-1)),
    }


def unit_cover(names, variables, localizer):
    denominators = [CASES[name][1] for name in names]
    basis = sp.groebner((*denominators, Z*localizer-1), Z, *variables, order="lex")
    assert basis.contains(sp.Integer(1)), names


def check_cover():
    unit_cover(("u_minus_a", "u_minus_b"), (V, W), V*W*(V-1)*(W-1))
    unit_cover(("sum_zero_a", "sum_zero_b", "sum_zero_c"), (U, W), U*W*(U-1)*(U+1)*(W-1))
    unit_cover(("v_minus_two_a", "v_minus_two_b", "v_minus_two_c"), (U, W), U*W*(U-1)*(W-1)*(U*W+1))
    unit_cover(("uw_minus_a", "uw_minus_b"), (U, V), U*V*(U-1)*(U+1)*(V-1))
    unit_cover(("mixed_a", "mixed_b", "mixed_c"), (U, V), U*V*(U-1)*(V-1)*(V+1)*(U+V)*(U+2*V+1))
    names = ("sum_minus_one_a", "sum_minus_one_b", "sum_minus_one_c")
    basis = sp.groebner(
        (*(CASES[name][1] for name in names), Z*U*W*(U-1)*(U+1)*(U+2)*(W-1)-1),
        Z, U, W, order="lex",
    )
    assert tuple(poly.as_expr() for poly in basis.polys) == (9*Z-8, 2*U+1, W-2)


def main():
    base.amplitudes = amplitudes
    for case, (keys, expected) in CASES.items():
        matrix, rhs = [], []
        for port_word, root_word in keys:
            row, value = base.equation(base.word(port_word), base.word(root_word), case)
            matrix.append([sp.factor(row.get(i, 0)) for i in range(81)])
            rhs.append(sp.factor(value))
        nullspace = DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix()
        assert nullspace.rows == 1, case
        vector = [sp.factor(nullspace[0, i]) for i in range(nullspace.cols)]
        detector = sp.factor(sum(a*b for a, b in zip(vector, rhs, strict=True)))
        assert detector != 0, case
        weights = [sp.factor(value/detector) for value in vector]
        denominator = sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in weights]))
        assert denominator == sp.factor(expected), (case, denominator)
    check_cover()
    o2 = {(0, 1), (0, 2), (1, 0)}
    o7 = {(0, 1), (1, 0), (2, 0)}
    assert {(right, left) for left, right in o2} == o7
    print("PASS: 945-match expansion derives the 17-core O2 closure and O2/O7 reversal")


if __name__ == "__main__":
    main()
