"""Independent rational first-jet reconstruction for the scaffold no-go.

No primary constructor is imported. Generic existence and arbitrary-order
incidence are proved in the owning document, not by these finite checks.
"""

from fractions import Fraction as Q
from itertools import combinations


def rref(a):
    a = [[Q(x) for x in r] for r in a]
    piv = []
    r = 0
    for c in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        z = a[r][c]
        a[r] = [v / z for v in a[r]]
        for k in range(len(a)):
            if k != r:
                z = a[k][c]
                a[k] = [v - z * w for v, w in zip(a[k], a[r])]
        piv.append(c)
        r += 1
        if r == len(a):
            break
    return a, piv


# Coefficient order 01,02,10,12,20,21. Rows value,du,dv,ds,dt.
J = [
    [1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0],
]
assert len(rref(J)[1]) == 5
solutions = []
for chosen in range(1, 5):
    rhs = [int(i == chosen) for i in range(5)]
    mat, piv = rref([r + [b] for r, b in zip(J, rhs)])
    sol = [Q(0)] * 6
    for r, p in enumerate(piv):
        assert p < 6
        sol[p] = mat[r][-1]
    assert [sum(Q(a) * b for a, b in zip(r, sol)) for r in J] == rhs
    solutions.append(sol)
# Direct regular tournament: i sends to i+1,i+2 modulo5.
rows = []
assigned = []
for a, b in combinations(range(5), 2):
    tail, head = (a, b) if (b - a) % 5 in (1, 2) else (b, a)
    coordinate = 0 if (head - tail) % 5 == 1 else 1
    local = 1 + coordinate if tail == a else 3 + coordinate
    sol = solutions[local - 1]
    jets = [sum(Q(x) * y for x, y in zip(r, sol)) for r in J]
    row = [Q(0)] * 10
    row[2 * a] = jets[1]
    row[2 * a + 1] = jets[2]
    row[2 * b] = jets[3]
    row[2 * b + 1] = jets[4]
    assert jets[0] == 0
    rows.append(row)
    assigned.append(2 * tail + coordinate)
assert sorted(assigned) == list(range(10))
assert len(rref(rows)[1]) == 10
# B -> x^T B, x=(x0,x1,x2): at sample x=(2,3,5), distinct columns use disjoint coefficients.
rowmap = [[0, 0, 3, 0, 5, 0], [2, 0, 0, 0, 0, 5], [0, 2, 0, 3, 0, 0]]
assert len(rref(rowmap)[1]) == 3
print(
    {
        "jet_rank": 5,
        "four_exact_jet_preimages": [[str(x) for x in s] for s in solutions],
        "K5_jacobian_rank": 10,
        "row_map_sample_rank": 3,
        "all_checks": "PASS",
    }
)
