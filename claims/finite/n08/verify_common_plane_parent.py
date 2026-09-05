"""Primary exact replays for the common-plane parent proof.

These integer fixtures check the cofactor column identity and the repaired
mixed-normal extraction. They are not GHZ witnesses or a proof certificate.
The analytic case cover and independent mathematical audit remain essential.
"""
from itertools import combinations, product
import json

from verify_diagonal_root_leg_source import (
    I, Q, OUTSIDE, apply, contracted_edges, determinant, dot,
    open_root_tensor, require, scalar_hafnian, transpose,
)


def unit(row, col, weight=1):
    return [[weight if (a, b) == (row, col) else 0 for b in range(3)]
            for a in range(3)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def outer(a, b, weight=1):
    return [[weight * x * y for y in b] for x in a]


def pair_products(a, b):
    return [a[j] * b[k] + a[k] * b[j]
            for j, k in ((1, 2), (0, 2), (0, 1))]


def column_identity():
    p, q, tau0, tau1 = [5, 7, 11], [13, 17, 19], 2, 3
    count = 0
    for x in ([[1, 2, 3], [5, 7, 11], [13, 17, 19]],
              [[0, 2, -3], [5, 0, 7], [-11, 13, 0]],
              [[2, 4, 6], [0, 0, 0], [3, 6, 9]]):
        a, b, c = transpose(x)
        c0 = [v + pi * q[0] for v, pi in zip(pair_products(b, c), p)]
        c1 = [v + pi * q[1] for v, pi in zip(pair_products(a, c), p)]
        y = [tau1 * ai + tau0 * bi for ai, bi in zip(a, b)]
        lhs = [tau0 * u + tau1 * v for u, v in zip(c0, c1)]
        rhs = [v + pi * (tau0 * q[0] + tau1 * q[1])
               for v, pi in zip(pair_products(y, c), p)]
        require(lhs == rhs, 'cofactor column combination')
        count += 1
    return count


def repaired_normal_identity():
    # U=ker(1,1,0). All three P columns are specialized to v, while m
    # is a DIFFERENT torus covector in v-perp, held fixed in every derivative.
    n, v, m = [1, 1, 0], [1, -1, 2], [1, 3, 1]
    f, g, outside_u = [1, -1, 0], [0, 0, 1], [1, 1, 0]
    left, inactive_a = [], []
    for i in range(3):
        columns = [None] * 3
        columns[i] = outside_u
        others = [j for j in range(3) if j != i]
        columns[others[0]], columns[others[1]] = f, g
        left.append(transpose(columns))
        ai = [0] * 3
        ai[others[0]], ai[others[1]] = 1, 2
        inactive_a.append(ai)
        require(determinant(left[i]) != 0, 'invertible A spoke')
        require(apply(left[i], ai) == v, 'same inactive P column')
    require(dot(n, v) == dot(m, v) == 0, 'two annihilators at chosen vector')
    require(all(m) and n[2] == 0, 'new projection sees missing colour')
    right = [I, [[1, 2, 0], [0, 1, 3], [0, 0, 1]], I]
    alpha, beta = [2, 3, 5], [7, 11, 13]
    blocks = {(0, 1): Q}
    for i in range(3):
        blocks[0, 2 + i] = left[i]
        blocks[1, 2 + i] = unit(i, i, alpha[i])
        blocks[0, 5 + i] = unit(i, i, beta[i])
        blocks[1, 5 + i] = right[i]
    for u, w, colour in ((2, 3, 2), (2, 4, 1), (3, 4, 0)):
        blocks[u, w] = unit(colour, colour)
    # q0=tau1*h, q1=-tau0*h, q2=eta*tau0*tau1; h(B2)=B2[2].
    blocks[6, 7] = unit(1, 2, beta[1])
    blocks[5, 7] = unit(0, 2, -beta[0])
    blocks[5, 6] = unit(0, 1, 2 * beta[0] * beta[1])
    for i in range(3):
        ell = [j + 2 for j in range(3)]
        ell[i] = 0
        normal0, normal1 = [2 + i, 3, 5], [7, 11 + i, 13]
        blocks[2 + i, 5] = add(outer(ell, I[0], beta[0]), outer(I[i], normal0))
        blocks[2 + i, 6] = add(outer(ell, I[1], -beta[1]), outer(I[i], normal1))
        blocks[2 + i, 7] = [[1 + i + a + 2 * b for b in range(3)]
                            for a in range(3)]
    require(set(blocks) == set(combinations(range(8), 2)), 'all physical pairs')
    inactive_b = [[0, 2, 3], [5, 0, 7], [11, 13, 0]]
    inactive = inactive_a + inactive_b
    h_mixed = 0
    f_mixed = [[0] * 3 for _ in range(3)]
    for t2, s2 in product((0, 1), repeat=2):
        values = [x[:] for x in inactive]
        values[2][2] += t2
        values[5][2] += s2
        sign = 1 if t2 == s2 else -1
        edges = contracted_edges(blocks, [I[0], I[0], *values])
        h_mixed += sign * scalar_hafnian(edges, OUTSIDE)
        tensor = open_root_tensor(blocks, values)
        for a, b in product(range(3), repeat=2):
            f_mixed[a][b] += sign * tensor[a][b]
    require(h_mixed == 0, 'H t2*s2 coefficient vanishes')
    # C_AB is zero with A inactive, B0/B1 inactive, even when B2 is normal.
    for s2 in (0, 1):
        values = [x[:] for x in inactive]
        values[5][2] += s2
        edges = contracted_edges(blocks, [I[0], I[0], *values])
        for i, j in product(range(3), repeat=2):
            c = scalar_hafnian(edges, [u for u in OUTSIDE if u not in (2 + i, 5 + j)])
            require(c == 0, 'inactive C and its s2 coefficient vanish')
    a0, a1 = inactive_a[:2]
    p2 = dot(a0, apply(blocks[2, 3], a1))
    b0, b1 = inactive_b[:2]
    g20 = dot(blocks[4, 5][2], b0)
    g21 = dot(blocks[4, 6][2], b1)
    require(p2 and g20 and g21, 'AB normal rows remain nonzero')
    r0, r1 = apply(right[0], b0), apply(right[1], b1)
    rhs = [beta[2] * m[2] * p2 * (g21 * x + g20 * y) for x, y in zip(r0, r1)]
    lhs = [dot(m, column) for column in zip(*f_mixed)]
    require(lhs == rhs, 'repaired projected mixed-normal identity')
    require(lhs[0] or lhs[1], 'fixture is not a pure-colour-2 target or a witness')
    return {'projected_actual_tensor': lhs, 'nonzero_AB_normal_rows': [g20, g21]}


def main():
    count = column_identity()
    normal = repaired_normal_identity()
    print(json.dumps({
        'status': 'PASS',
        'cofactor_column_fixtures': count,
        'normal_repair_fixture': normal,
        'scope': 'exact identity corroboration only; analytic proof remains load-bearing',
    }, indent=2))


if __name__ == '__main__':
    main()
