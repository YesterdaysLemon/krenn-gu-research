"""Independent stdlib-only audit of the P7 Boolean-down/Hessian reduction."""

from fractions import Fraction
from itertools import combinations

N = 7
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))


def zeros(rows, cols):
    return [[Fraction(0) for _ in range(cols)] for _ in range(rows)]


def eye(size):
    result = zeros(size, size)
    for i in range(size):
        result[i][i] = Fraction(1)
    return result


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum(x * y for x, y in zip(row, col)) for col in right_t]
        for row in left
    ]


def add(left, right):
    return [
        [x + y for x, y in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def diag(values):
    result = zeros(len(values), len(values))
    for i, value in enumerate(values):
        result[i][i] = value
    return result


def determinant(matrix):
    work = [row[:] for row in matrix]
    size = len(work)
    result = Fraction(1)
    for col in range(size):
        pivot = next((row for row in range(col, size) if work[row][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        pivot_value = work[col][col]
        result *= pivot_value
        for row in range(col + 1, size):
            if not work[row][col]:
                continue
            factor = work[row][col] / pivot_value
            for k in range(col + 1, size):
                work[row][k] -= factor * work[col][k]
        # Only the strict upper triangle is needed after this column.
    return result


def matrix_equal(left, right):
    return all(x == y for lr, rr in zip(left, right) for x, y in zip(lr, rr))


def redge_matrix():
    result = zeros(N, len(EDGES))
    for col, edge in enumerate(EDGES):
        for i in edge:
            result[i][col] = Fraction(1)
    return result


def down_and_up():
    down = zeros(len(EDGES), len(TRIPLES))
    up = zeros(len(EDGES), len(TRIPLES))
    for row, edge in enumerate(EDGES):
        edge_set = set(edge)
        for col, triple in enumerate(TRIPLES):
            triple_set = set(triple)
            down[row][col] = Fraction(int(edge_set <= triple_set))
            up[row][col] = Fraction(2 * int(edge_set.isdisjoint(triple_set)))
    return down, up


def build_pencils(a, redge):
    alpha = sum(a)
    delta = [alpha - 2 * (a[i] + a[j]) for i, j in EDGES]
    pmat = zeros(len(EDGES), N)
    for row, (i, j) in enumerate(EDGES):
        pmat[row][i] = a[j]
        pmat[row][j] = a[i]
    local = add(diag(delta), matmul(pmat, redge))

    mixed = zeros(len(EDGES), len(EDGES))
    for row, g in enumerate(EDGES):
        gset = set(g)
        for col, e in enumerate(EDGES):
            eset = set(e)
            if eset.isdisjoint(gset):
                mixed[row][col] = 2 * sum(
                    a[v] for v in VERTICES if v not in eset | gset
                )
    return delta, pmat, local, mixed


def main():
    redge = redge_matrix()
    down, up = down_and_up()
    redge_gram = matmul(transpose(redge), redge)
    jmat = zeros(len(EDGES), len(EDGES))
    for row in range(len(EDGES)):
        for col in range(len(EDGES)):
            jmat[row][col] = Fraction(2 * int(row == col), 1)
            jmat[row][col] += Fraction(2, 3)
            jmat[row][col] -= redge_gram[row][col]

    assert matrix_equal(matmul(jmat, down), up)
    assert determinant(jmat) == Fraction(2**16 * 3**6)

    # Seven coefficient matrices prove the universal pencil identity without CAS.
    for k in VERTICES:
        basis = [Fraction(int(i == k)) for i in VERTICES]
        _, _, local_k, mixed_k = build_pencils(basis, redge)
        assert matrix_equal(matmul(jmat, local_k), mixed_k)

    # Exact generic specialization for determinant lemma and Hessian symmetry.
    a = [Fraction(2**i) for i in VERTICES]
    delta, pmat, local, mixed = build_pencils(a, redge)
    assert all(delta)
    delta_inverse = diag([1 / value for value in delta])
    tmat = add(eye(N), matmul(matmul(redge, delta_inverse), pmat))
    hmat = matmul(tmat, diag(a))
    assert matrix_equal(hmat, transpose(hmat))
    assert determinant(local) == determinant(diag(delta)) * determinant(tmat)
    assert determinant(mixed) == determinant(jmat) * determinant(local)

    # Test the universal reconstruction identities at the same exact point.
    fmap = scale(Fraction(-1), matmul(delta_inverse, pmat))
    assert matrix_equal(matmul(redge, fmap), add(eye(N), scale(-1, tmat)))
    assert matrix_equal(
        matmul(local, fmap), scale(-1, matmul(pmat, tmat))
    )

    # A non-special rational row vector confirms the coordinate formula itself.
    r = [[Fraction(i + 1)] for i in VERTICES]
    f = matmul(fmap, r)
    lhs = matmul(local, f)
    rhs = scale(-1, matmul(pmat, matmul(tmat, r)))
    assert matrix_equal(lhs, rhs)

    print("PASS: independent Fraction audit proves U2 = J D3")
    print("PASS: seven coefficient pencils prove M_A = J L_A universally")
    print("PASS: det(J) = 2^16 3^6 and the exact determinant lemma agrees")
    print("PASS: the 7x7 master matrix is symmetric after row-coordinate gauging")
    print("PASS: exact reconstruction identities agree without project imports")
    print("UNKNOWN: generic and exceptional full-edge physical P7 survival")


if __name__ == "__main__":
    main()
