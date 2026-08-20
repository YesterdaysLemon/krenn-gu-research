"""Standalone recursive-permanent audit of the GLD61 O2/O7 closure."""
from __future__ import annotations

from itertools import combinations
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOTS = tuple(range(4))
EDGES = tuple(combinations(ROOTS, 2))
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}
U, V, W, Z = sp.symbols("u v w z")


def rows(value):
    return tuple(tuple(item.split(":")) for item in value.split(","))


K0 = rows("1000:0100,0100:0010,1100:0000,0010:0010,1000:1000,0101:0000,1001:0000,0110:0000,0011:0000,0100:1000,1000:0010,1010:0000,0100:0100,0002:0002")
K2 = rows("1000:0100,0010:0010,1000:1000,0100:0010,0100:1000,1000:0010,0100:0100,0002:0002,0200:0200,1100:0000,0101:0000,1010:0000,0011:0000,1001:0000")
K4 = rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,1001:1001,0101:0101,1100:1100,1020:1020,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,1101:1101")
CASES = {
    "u_minus_a": (rows("0100:0100,1000:1000,0100:0010,1000:0010,0100:1000,1000:0100,0010:0010,2000:2000,0002:0002,0110:0000,1010:0000,0101:0000,1001:0000,0011:0000"), 3*V*W*(V-1)*(W-1)**3*(W+1)),
    "u_minus_b": (rows("1000:1000,0100:0100,0010:0010,0200:0200,0020:0020,2000:2000,0002:0002,1010:1010,1100:1100,0110:0110,1020:1020,1200:1200,0102:0102,0012:0012,0120:0120,1110:1110"), 2*W*(V-1)*(W-1)*(3*W-2)*(V*W+V-W+1)),
    "sum_zero_a": (rows("1101:0010,1011:0100,0110:0000,1001:0000,1000:0010,0000:0110,1000:0100,1010:0000,1100:0000,1010:0110,1002:0012"), 2*U**3*(U*W-1)),
    "sum_zero_b": (K2, 2*U**3*W**2*(U-1)*(W-2)*(U*W+1)),
    "sum_zero_c": (K4, (U-1)*(U*W+1)*(U*W-W-1)*(2*U*W-U-W+1)),
    "v_minus_two_a": (K2, 16*U*W**2*(U-1)**2*(W-2)*(U*W+1)),
    "v_minus_two_b": (K0, 2*U*W*(U*W-1)*(U*W+1)*(U**3*W+2*U**2*W**2-10*U**2*W+3*U**2+U*W**2+16*U*W-12*U-6*W**2-5*W+6)),
    "v_minus_two_c": (K4, (U-1)*(W-1)*(U*W+1)*(U*W-2*W-1)*(2*U*W-U-W+1)),
    "uw_minus_a": (rows("0000:0101,0000:0011,0100:0100,1000:1000,0001:0001,0100:0010,1000:0010,0100:1000,1000:0100,0010:0010,0200:0200,0110:0000,1010:0000,0101:0000,0101:0101,1001:0011,1002:0102"), 4*U**3*V**2*(U-1)*(U+1)*(2*U+1)),
    "uw_minus_b": (rows("0101:0000,1001:0000,0110:0000,1010:0000,1100:0000,1000:0010,1000:0100,0100:0100,0100:0010,0100:1000,0001:0001,1000:1000,1011:1000,1002:1002"), 2*U*V**2*(U**2-2*U-1)*(U**2+U-1)),
    "sum_minus_one_a": (rows("1101:0010,1011:0100,0110:0000,0100:1000,1001:0000,1000:0010,1000:0100,0000:1010,0100:0010,0110:1010,0100:1110,1010:0110,1100:0110,1002:0012"), U**2*W**2*(U-1)*(U+1)**2*(2*U+1)*(W+1)),
    "sum_minus_one_b": (rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,1001:1001,0101:0101,1100:1100,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,1101:1101"), W*(U-1)*(U+W)*(U*W+1)*(2*U*W-U-W+1)),
    "sum_minus_one_c": (K2, 2*U*W**2*(U-1)**2*(U+1)**2*(W-2)*(U*W+1)),
    "mixed_a": (K2, 2*U*V**2*(U-1)**2*(2*U+V)*(V+1)**2*(2*U+3*V+1)),
    "mixed_b": (rows("0100:0100,0001:0001,1000:1000,0010:0010,0200:0200,0002:0002,0020:0020,0110:0110,0101:0101,0011:0011,1020:1020,0201:0201,1002:1002,2100:2100,0021:0021,0210:0210,0111:0111"), V*(U-1)*(V+1)*(U**2+2*U*V+2*U-1)*(U**2+3*U*V+2*U+V**2-1)),
    "mixed_c": (K0, 2*U*V**2*(U-1)*(V+1)*(U*V+2*U+V)*(U**2+2*U*V-2*U-4*V-1)*(U**2+2*U*V+U-V-1)),
    "sum_point": (rows("0001:0001,1000:1000,0101:0000,1001:0000,0110:0000,0100:1000,1010:0000,0011:0011,1002:1002"), sp.Integer(6)),
}


def word(value):
    return tuple(map(int, value))


def p_index(which, root, colour):
    return 12*which + 3*root + colour


def w_index(left, right, lc, rc):
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return 24 + 9*EDGE_INDEX[(left, right)] + 3*lc + rc


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


def cross(colour, root, port, case):
    if root == port:
        return sp.Integer(1)
    return amplitudes(case).get((colour, root, port), sp.Integer(0))


def permanent(root_set, port_set, root_word, port_word, case):
    if not root_set:
        return sp.Integer(1)
    first, total = root_set[0], 0
    for i, port in enumerate(port_set):
        if root_word[first] != port_word[port]:
            continue
        entry = cross(port_word[port], first, port, case)
        if entry:
            total += entry*permanent(
                root_set[1:], port_set[:i] + port_set[i+1:], root_word, port_word, case
            )
    return sp.expand(total)


def add(row, index, value):
    value = sp.expand(row.get(index, 0) + value)
    if value:
        row[index] = value
    else:
        row.pop(index, None)


def equation(port_word, root_word, case):
    x, y = (1, 1, 0), (1, -1, 0)
    row = {}
    rhs = -permanent(ROOTS, ROOTS, root_word, port_word, case)
    for omitted_port in ROOTS:
        ports = tuple(port for port in ROOTS if port != omitted_port)
        for missing_root in ROOTS:
            roots = tuple(root for root in ROOTS if root != missing_root)
            minor = permanent(roots, ports, root_word, port_word, case)
            colour = port_word[omitted_port]
            add(row, p_index(0, missing_root, root_word[missing_root]), y[colour]*minor)
            add(row, p_index(1, missing_root, root_word[missing_root]), x[colour]*minor)
    for left_port, right_port in EDGES:
        lc, rc = port_word[left_port], port_word[right_port]
        corrected = x[lc]*y[rc] + y[lc]*x[rc]
        ports = tuple(port for port in ROOTS if port not in (left_port, right_port))
        for left_root, right_root in EDGES:
            roots = tuple(root for root in ROOTS if root not in (left_root, right_root))
            minor = permanent(roots, ports, root_word, port_word, case)
            add(row, w_index(left_root, right_root, root_word[left_root], root_word[right_root]), corrected*minor)
    if len(set(port_word)) == 1 and root_word == port_word:
        add(row, 78+port_word[0], -1)
    return row, sp.expand(rhs)


def unit_cover(names, variables, localizer):
    basis = sp.groebner(
        (*(CASES[name][1] for name in names), Z*localizer-1),
        Z, *variables, order="lex",
    )
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
    for case, (keys, expected) in reversed(tuple(CASES.items())):
        matrix, rhs = [], []
        for port_word, root_word in reversed(keys):
            row, value = equation(word(port_word), word(root_word), case)
            matrix.append([sp.factor(row.get(i, 0)) for i in reversed(range(81))])
            rhs.append(sp.factor(value))
        nullspace = DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix()
        assert nullspace.rows == 1, case
        vector = [sp.factor(nullspace[0, i]) for i in range(nullspace.cols)]
        detector = sp.factor(sum(a*b for a, b in zip(vector, rhs, strict=True)))
        weights = [sp.factor(value/detector) for value in vector]
        denominator = sp.factor(sp.lcm([sp.denom(sp.cancel(value)) for value in weights]))
        assert denominator == sp.factor(expected), (case, denominator)
    check_cover()
    assert {(right, left) for left, right in {(0, 1), (0, 2), (1, 0)}} == {(0, 1), (1, 0), (2, 0)}
    print("PASS: standalone recursive-permanent audit derives the GLD61 O2/O7 closure")


if __name__ == "__main__":
    main()
