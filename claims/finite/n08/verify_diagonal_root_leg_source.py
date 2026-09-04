"""Exact replay of the universal mixed-normal matching identity.

This checks displayed identities on three integer fixtures, including both
determinant-zero boundaries. The quantified analytic proof and independent
mathematical audit remain load-bearing; this is not a global certificate.
"""
from functools import lru_cache
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


def apply(a, x):
    return [dot(row, x) for row in a]


def determinant(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def adjugate(a):
    result = [[0] * 3 for _ in range(3)]
    for i, j in product(range(3), repeat=2):
        rows = [r for r in range(3) if r != j]
        cols = [c for c in range(3) if c != i]
        result[i][j] = (-1) ** (i + j) * (
            a[rows[0]][cols[0]] * a[rows[1]][cols[1]]
            - a[rows[0]][cols[1]] * a[rows[1]][cols[0]])
    return result


def scalar_hafnian(values, vertices):
    @lru_cache(None)
    def visit(mask):
        if mask == 0:
            return 1
        bit = mask & -mask
        first = bit.bit_length() - 1
        rest = mask ^ bit
        total = 0
        scan = rest
        while scan:
            other_bit = scan & -scan
            other = other_bit.bit_length() - 1
            total += values[first, other] * visit(rest ^ other_bit)
            scan ^= other_bit
        return total

    return visit(sum(1 << v for v in vertices))


I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
SWAP01 = [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
SWAP02 = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
SWAP12 = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
Q = [[2, 1, 0], [0, 3, 1], [1, 0, 2]]
ALPHA = [2, 3, 5]
BETA = [7, 11, 13]
OUTSIDE = tuple(range(2, 8))


def unit(i, weight):
    return [[weight if row == col == i else 0 for col in range(3)]
            for row in range(3)]


def contracted_edges(blocks, vectors):
    return {(u, v): dot(vectors[u], apply(block, vectors[v]))
            for (u, v), block in blocks.items()}


def open_root_tensor(blocks, outside_vectors):
    tensor = [[0] * 3 for _ in range(3)]
    for a, b in product(range(3), repeat=2):
        vectors = [I[a], I[b], *outside_vectors]
        tensor[a][b] = scalar_hafnian(contracted_edges(blocks, vectors), range(8))
    return tensor


def fixture(name, left, right, expected_zero):
    blocks = {(0, 1): Q}
    for i in range(3):
        blocks[0, 2 + i] = left[i]
        blocks[1, 2 + i] = unit(i, ALPHA[i])
        blocks[0, 5 + i] = unit(i, BETA[i])
        blocks[1, 5 + i] = right[i]
    # Arbitrary dense outside blocks: the replay assumes no AA/BB unit form.
    for u, v in combinations(OUTSIDE, 2):
        blocks[u, v] = [[((5 * u + 7 * v + 3 * a + b) % 9) - 4
                         for b in range(3)] for a in range(3)]
    inactive = [[0, 2, 3], [5, 0, 7], [11, 13, 0],
                [0, 17, 19], [23, 0, 29], [31, 37, 0]]
    p = transpose([apply(left[i], inactive[i]) for i in range(3)])
    r = transpose([apply(right[i], inactive[3 + i]) for i in range(3)])
    d, e = determinant(p), determinant(r)
    require((d == 0, e == 0) == expected_zero, name + ': determinant scope')
    a, b = adjugate(p), adjugate(r)
    n = multiply(multiply(a, Q), transpose(b))
    values0 = contracted_edges(blocks, [I[0], I[0], *inactive])
    for i, j in product(range(3), repeat=2):
        p1 = [row[:] for row in p]
        r1 = [row[:] for row in r]
        lp, rm = apply(left[i], I[i]), apply(right[j], I[j])
        for k in range(3):
            p1[k][i] += lp[k]
            r1[k][j] += rm[k]
        di, ej = determinant(p1) - d, determinant(r1) - e
        c0 = scalar_hafnian(values0, [v for v in OUTSIDE if v not in (2 + i, 5 + j)])
        h_mixed = 0
        f_mixed = [[0] * 3 for _ in range(3)]
        for ti, sj in product((0, 1), repeat=2):
            vectors = [v[:] for v in inactive]
            vectors[i][i] += ti
            vectors[3 + j][j] += sj
            sign = 1 if ti == sj else -1
            values = contracted_edges(blocks, [I[0], I[0], *vectors])
            h_mixed += sign * scalar_hafnian(values, OUTSIDE)
            tensor = open_root_tensor(blocks, vectors)
            for x, y in product(range(3), repeat=2):
                f_mixed[x][y] += sign * tensor[x][y]
        lhs = h_mixed * n[i][j] + c0 * (
            di * ej + ALPHA[i] * BETA[j] * a[i][j] * b[j][i])
        rhs = dot(a[i], apply(f_mixed, b[j]))
        require(lhs == rhs, f'{name}: mixed identity ({i},{j}): {lhs} != {rhs}')
    return {'fixture': name, 'inactive_determinants': [d, e], 'identities': 9}


def main():
    require(determinant(Q) != 0, 'invertible root block')
    ones = {edge: 1 for edge in combinations(range(8), 2)}
    require(scalar_hafnian(ones, range(8)) == 105, 'eight-vertex matching count')
    results = [
        fixture('both determinants nonzero', [I, I, I], [I, I, I], (False, False)),
        fixture('one coincident plane shore', [I, SWAP01, SWAP02],
                [I, I, I], (True, False)),
        fixture('two coincident plane shores', [I, SWAP01, SWAP02],
                [SWAP01, I, SWAP12], (True, True)),
    ]
    print(json.dumps({
        'status': 'PASS',
        'scope': '27 exact mixed-normal identity replays; analytic proof remains load-bearing',
        'matching_count': 105,
        'fixtures': results,
    }, indent=2))


if __name__ == '__main__':
    main()
