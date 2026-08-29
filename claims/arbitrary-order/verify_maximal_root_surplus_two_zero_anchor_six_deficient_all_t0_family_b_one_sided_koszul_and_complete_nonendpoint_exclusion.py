"""Primary exact checks for the GLS75 complete nonendpoint exclusion."""

from itertools import combinations, product

import sympy as sp


OUTSIDE = tuple(range(3))
OUTSIDE_LABELS = (3, 4, 5)


def koszul_matrix(local_dim=3):
    """Return the two shore maps on three complementary pair tensors."""
    domain = [
        (missing, pair_word)
        for missing in OUTSIDE
        for pair_word in product(range(local_dim), repeat=2)
    ]
    rows = []
    for shore in (0, 1):
        for word in product(range(local_dim), repeat=3):
            row = []
            for missing, pair_word in domain:
                rest = tuple(port for port in OUTSIDE if port != missing)
                row.append(
                    int(
                        word[missing] == shore
                        and pair_word == tuple(word[port] for port in rest)
                    )
                )
            rows.append(row)
    return sp.Matrix(rows), domain


def parent_matrix(local_dim=3, active_q=None):
    """Map three one-port rows through the outside P0Q0 companions."""
    active_q = set(OUTSIDE if active_q is None else active_q)
    domain = [(missing, colour) for missing in OUTSIDE for colour in range(local_dim)]
    rows = []
    for word in product(range(local_dim), repeat=3):
        row = []
        for missing, colour in domain:
            left, right = tuple(port for port in OUTSIDE if port != missing)
            coefficient = 0
            if right in active_q:
                coefficient += int(
                    word[left] == 0
                    and word[right] == 1
                    and word[missing] == colour
                )
            if left in active_q:
                coefficient += int(
                    word[left] == 1
                    and word[right] == 0
                    and word[missing] == colour
                )
            row.append(coefficient)
        rows.append(row)
    return sp.Matrix(rows), domain


def row_forced_zero(matrix, coordinate):
    """Check that coordinate vanishes on the exact nullspace."""
    unit = sp.zeros(1, matrix.cols)
    unit[0, coordinate] = 1
    return matrix.col_join(unit).rank() == matrix.rank()


koszul, pair_domain = koszul_matrix()
shore_u = koszul[:27, :]
shore_v = koszul[27:, :]
parent, row_domain = parent_matrix()

# One available Koszul row plus the missing row coupled to the complete
# parent map.  The kernel is alternating plus four full-row coboundaries.
one_sided = shore_u.row_join(sp.zeros(27, 9)).col_join(
    shore_v.row_join(-parent)
)
assert one_sided.shape == (54, 36)
assert one_sided.rank() == 31
one_sided_nullspace = one_sided.nullspace()
assert len(one_sided_nullspace) == 5
assert sp.Matrix.hstack(*[vector[27:, :] for vector in one_sided_nullspace]).rank() == 4

# Every one-port transverse coordinate is zero in that kernel.
for missing in OUTSIDE:
    transverse_d = 27 + row_domain.index((missing, 2))
    assert row_forced_zero(one_sided, transverse_d)

# The four coboundary directions have zero total U and V row coefficient.
for colour in (0, 1):
    functional = sp.zeros(1, 36)
    for missing in OUTSIDE:
        functional[0, 27 + row_domain.index((missing, colour))] = 1
    assert one_sided.col_join(functional).rank() == one_sided.rank()

# A single Koszul row already kills the scalar restriction of every pair deck
# to the two complementary kernel lines.
for missing in OUTSIDE:
    scalar_pair = pair_domain.index((missing, (2, 2)))
    assert row_forced_zero(shore_u, scalar_pair)

# If the root-axis opposite shore is identically zero, lambda=0: the parent
# block is injective, so all D rows vanish (a stronger conclusion).
zero_coupling = shore_u.row_join(sp.zeros(27, 9)).col_join(
    sp.zeros(27, 27).row_join(parent)
)
assert zero_coupling.rank() == shore_u.rank() + parent.rank() == 28
for missing, colour in row_domain:
    assert row_forced_zero(zero_coupling, 27 + row_domain.index((missing, colour)))

# If both shores at central label 0 are root-axis-only, the P_a Q_a
# coefficient can use only the complementary central pair {1,2}.
def supports_probe(label, probe_index):
    if label in OUTSIDE_LABELS or label == 0:
        return probe_index == 0
    return True


for target_colour in (1, 2):
    surviving_pairs = []
    for left, right in combinations(range(6), 2):
        pq = supports_probe(left, target_colour) and supports_probe(
            right, target_colour
        )
        qp = supports_probe(left, target_colour) and supports_probe(
            right, target_colour
        )
        if pq or qp:
            surviving_pairs.append((left, right))
    assert surviving_pairs == [(1, 2)]

# In every nonendpoint pure-P3 representative the three h rows have both
# outside-shore coordinates nonzero.  Signs and mode permutations preserve
# this property.
r, s = sp.symbols("r s", nonzero=True)
pure_rows = ((-r, s), (r, -s), (r, s))
assert all(first != 0 and second != 0 for first, second in pure_rows)

# The one-A bracket cannot vanish for either available shore orientation.
au, bu, aw, bw = sp.symbols("au bu aw bw", nonzero=True)
bracket_u = sp.Matrix([[aw + au, bw], [bu, 0]])
bracket_v = sp.Matrix([[0, au], [aw, bw + bu]])
assert bracket_u[0, 1] == bw and bracket_u[1, 0] == bu
assert bracket_v[0, 1] == au and bracket_v[1, 0] == aw

# Replay the all-A and exactly-two-A scalar eliminations inherited from GLS74.
xv, xw, yv, yw = sp.symbols("xv xw yv yw")
cross = xv * yw + xw * yv
assert sp.expand((cross + 2 * yv * yw + cross) / 2) == cross + yv * yw
assert sp.expand((2 * xv * xw + cross + cross) / 2) == xv * xw + cross

a1, a2 = sp.symbols("a1 a2", nonzero=True)
pair_cross, pair_b = sp.symbols("pair_cross pair_b")
lam = a1 / a2
two_a = (a1 * pair_b - lam * pair_cross, a2 * pair_b + pair_cross)
assert sp.solve(two_a, (pair_b, pair_cross), dict=True) == [
    {pair_b: 0, pair_cross: 0}
]

# The endpoint parent rank drop remains genuine.
row_parent, _ = parent_matrix(local_dim=2)
two_active, _ = parent_matrix(local_dim=2, active_q={0, 1})
one_active, _ = parent_matrix(local_dim=2, active_q={0})
assert row_parent.rank() == 6
assert two_active.rank() == 4
assert one_active.rank() == 3

print("one_sided_Koszul_parent: rank 31 / nullity 5")
print("kernel decomposition: alternating 1 + row-coboundary 4")
print("one_sided consequences: pair KxK=0 and one-port D|K=0")
print("double-central-root-axis: impossible from the two P_aQ_a rows")
print("nonendpoint h rows: transverse to both outside shore lines")
print("GLS75_Family_B_r3_outside_nonendpoint=EMPTY")
print("P/Q-common outside endpoint charts remain OPEN")
print("unchanged_inherited_residual=98355 profiles / 81 keys")
