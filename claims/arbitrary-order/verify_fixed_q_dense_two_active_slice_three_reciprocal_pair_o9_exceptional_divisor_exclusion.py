"""Primary 945-match derivation for the GLD62 O9 closure."""
from __future__ import annotations

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion as base

U, V, W, Z = base.U, base.V, base.W, sp.symbols("z")
T = 2*V**2*W - 4*V*W + V + 2*W + 1
G = V**2*W - 2*V*W + W + 1
S = T + V*W*(V-1)
H = 2*V*W**2 - V*W + W - 1
HL = V**2*W - 3*V*W + V + 2*W + 1


def rows(value):
    return tuple(tuple(item.split(":")) for item in value.split(","))


K5 = rows("1101:0010,0111:1000,1000:0100,0100:1000,0100:0010,0010:0100,0010:1000,1000:0010,0110:0000,1010:0000,1100:0000,1100:0110,0102:0012")
K11 = rows("1011:0100,0111:1000,1100:0000,1010:0000,0010:0100,1000:0010,0100:1000,0000:0110,0010:1000,0110:0000,0100:0010,1000:0100,1010:0110,0012:1002")
K4 = rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,2000:2000,0110:0110,0101:0101,0011:0011,1020:1020,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,0111:0111")

CASES = {
    "product_plus_a": (K5, 2*U*V**2*(U*V+V-1)),
    "product_plus_b": (K11, 2*U*V*(U+1)*(U*V-V+1)),
    "product_minus_a": (rows("1101:0010,0111:1000,1000:0100,0100:1000,0100:0010,0010:0100,0010:1000,1000:0010,0110:0000,1010:0000,1100:0110,1010:1100,0102:0012"), U*V**2*(2*U*V+V-1)),
    "product_minus_b": (rows("1011:0100,0111:1000,1100:0000,1010:0000,0010:0100,1000:0010,0100:1000,0010:1000,0100:0010,1000:0100,1110:0100,0012:1002"), U*V*(2*U-1)*(U*V-V+1)),
    "product_minus_c": (rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0020:0020,2000:2000,0110:0110,0101:0101,0011:0011,1020:1020,0201:0201,1002:1002,2100:2100,0021:0021,0102:0102,0210:0210,0111:0111"), (U+1)*(V-1)*(U*V-V-1)*(U**2*V+U*V**2-1)),
    "uv_plus_a": (rows("1000:1000,0100:0100,0010:0010,0200:0200,0020:0020,2000:2000,0002:0002,1010:1010,1100:1100,0110:0110,1020:1020,1200:1200,0012:0012,0120:0120,1110:1110"), 2*V*W*(V+1)*(3*V**2*W-2*V**2+V-W+1)),
    "uv_plus_b": (K5, V**2*W**2*(V+1)**2*(V*W-W+1)*(V*W+W-1)),
    "vw_plus": (K5, 2*U**2*W**2*(W+1)**2*(U*W+U-1)),
    "uw_affine_a": (rows("1000:1000,0100:0100,0010:0010,0200:0200,0020:0020,2000:2000,0002:0002,1010:1010,1100:1100,0110:0110,1020:1020,1002:1002,1200:1200,0102:0102,0012:0012,0120:0120,1110:1110"), 2*W*(3*V*W-2*V-W+1)*(3*V**2*W**4-2*V**2*W**3+2*V*W**4-3*V*W**3-2*V*W**2+5*V*W-2*V-W**4-W**3+2*W**2+W-1)),
    "uw_affine_b": (K4, (V-1)*(3*W-2)*(V*W+W+1)*H*(2*V*W**2-V+W**2+2*W-2)),
    "uw_affine_c": (K5, V**2*W**2*(2*W-1)**2*(V*W-W+1)*H),
    "long_a": (K4, 2*(V-1)*(V*W+W+1)*G*HL*(2*V**3*W**2-V**3*W-5*V**2*W**2+3*V**2*W+3*V*W**2-2*V*W+V+2*W+1)),
    "long_b": (K5, 2*V**2*W**2*(V*W-W+1)*G*T**2),
    "long_c": (K11, 2*V*W**2*G*HL*T**2*(3*V**2*W-6*V*W+V+3*W+1)),
}


def parameters(case):
    if case.startswith("product_plus"):
        return U, V, 1/(U*V)
    if case.startswith("product_minus"):
        return U, V, -1/(U*V)
    if case.startswith("uv_plus"):
        return -(V+1)/V, V, W
    if case == "vw_plus":
        return U, -(W+1)/W, W
    if case.startswith("uw_affine"):
        return (2*W-1)/(W-1), V, W
    return -T/(V*W*(V-1)), V, W


def amplitudes(case):
    u, v, w = parameters(case)
    return {
        (0, 0, 1): u, (1, 1, 0): sp.cancel(u/(u-1)),
        (0, 1, 2): v, (1, 2, 1): sp.cancel(v/(v-1)),
        (0, 2, 0): w, (1, 0, 2): sp.cancel(w/(w-1)),
    }


def unit_cover(names, variables, localizer):
    basis = sp.groebner(
        (*(CASES[name][1] for name in names), Z*localizer-1),
        Z, *variables, order="lex",
    )
    assert basis.contains(sp.Integer(1)), names


def check_cover():
    assert sp.cancel((-(V+1)/V)*V*W+1 + (V*W+W-1)) == 0
    assert sp.cancel(U*(-(W+1)/W)*W+1 + (U*W+U-1)) == 0
    assert sp.cancel(((2*W-1)/(W-1))*V*W+1 - H/(W-1)) == 0
    long_u = -T/(V*W*(V-1))
    assert sp.cancel(long_u*V*W+1 + 2*G/(V-1)) == 0
    assert sp.cancel(long_u-1 + S/(V*W*(V-1))) == 0
    unit_cover(("product_plus_a", "product_plus_b"), (U, V), U*V*(U-1)*(V-1)*(U*V-1))
    unit_cover(("product_minus_a", "product_minus_b", "product_minus_c"), (U, V), U*V*(U-1)*(V-1)*(U*V+1))
    unit_cover(("uv_plus_a", "uv_plus_b"), (V, W), V*W*(V-1)*(V+1)*(2*V+1)*(W-1)*(V*W+W-1))
    unit_cover(("vw_plus",), (U, W), U*W*(U-1)*(W-1)*(W+1)*(2*W+1)*(U*W+U-1))
    unit_cover(("uw_affine_a", "uw_affine_b", "uw_affine_c"), (V, W), V*W*(V-1)*(W-1)*(2*W-1)*H)

    substitution = {W: -1/(V-1)}
    a = sp.factor((V*W+W+1).subs(substitution))
    h = sp.factor(HL.subs(substitution))
    i = sp.factor((2*V**3*W**2-V**3*W-5*V**2*W**2+3*V**2*W+3*V*W**2-2*V*W+V+2*W+1).subs(substitution))
    j = sp.factor((3*V**2*W-6*V*W+V+3*W+1).subs(substitution))
    expected = (-2/(V-1), 3, (V**3-V-3)/(V-1), -2*(V-2))
    assert all(sp.cancel(left-right) == 0 for left, right in zip((a, h, i, j), expected, strict=True))
    assert sp.gcd(V**3-V-3, V-2) == 1


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
    print("PASS: 945-match expansion derives the 14-core pointwise O9 closure")


if __name__ == "__main__":
    main()
