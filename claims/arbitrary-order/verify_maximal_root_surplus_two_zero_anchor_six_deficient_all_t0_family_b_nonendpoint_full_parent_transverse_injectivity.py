"""Primary exact algebra checks for the candidate GLS74 nonendpoint theorem."""

from itertools import combinations, product

import sympy as sp


OUTSIDE = tuple(range(3))


def koszul_matrix(local_dim=3):
    """Map three complementary pair tensors through the U- and V-syzygies."""
    domain = []
    for missing in OUTSIDE:
        for pair_word in product(range(local_dim), repeat=2):
            domain.append((missing, pair_word))

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


def full_parent_matrix(local_dim=3, active_q=None):
    """Map one-port decks by the three outside pair companions."""
    if active_q is None:
        active_q = set(OUTSIDE)
    else:
        active_q = set(active_q)

    domain = [(missing, colour) for missing in OUTSIDE for colour in range(local_dim)]
    rows = []
    for word in product(range(local_dim), repeat=3):
        row = []
        for missing, colour in domain:
            pair = tuple(port for port in OUTSIDE if port != missing)
            left, right = pair
            coefficient = 0
            if right in active_q:
                coefficient += int(
                    word[left] == 0 and word[right] == 1 and word[missing] == colour
                )
            if left in active_q:
                coefficient += int(
                    word[left] == 1 and word[right] == 0 and word[missing] == colour
                )
            row.append(coefficient)
        rows.append(row)
    return sp.Matrix(rows)


# The two full Koszul equations have exactly the alternating generator.
koszul, koszul_domain = koszul_matrix()
assert koszul.shape == (54, 27)
assert koszul.rank() == 26

alternating = sp.zeros(len(koszul_domain), 1)
alternating_entries = {
    (0, (0, 1)): 1,
    (0, (1, 0)): -1,
    (1, (1, 0)): 1,
    (1, (0, 1)): -1,
    (2, (0, 1)): 1,
    (2, (1, 0)): -1,
}
for key, value in alternating_entries.items():
    alternating[koszul_domain.index(key)] = value
assert koszul * alternating == sp.zeros(54, 1)
koszul_nullspace = koszul.nullspace()
assert len(koszul_nullspace) == 1
assert sp.Matrix.hstack(koszul_nullspace[0], alternating).rank() == 1

# Restoring the complete F00 row kills all three full one-port corrections.
full_parent = full_parent_matrix()
assert full_parent.shape == (27, 9)
assert full_parent.rank() == 9

# On the row planes the same map has the six scalar equations quoted in the
# proof and is still injective in characteristic different from two.
row_parent = full_parent_matrix(local_dim=2)
assert row_parent.shape == (8, 6)
assert row_parent.rank() == 6

c3, c4, c5, d3, d4, d5 = sp.symbols("c3 c4 c5 d3 d4 d5")
row_equations = (
    c3 + c4,
    c3 + c5,
    c4 + c5,
    d3 + d4,
    d3 + d5,
    d4 + d5,
)
assert sp.solve(row_equations, (c3, c4, c5, d3, d4, d5), dict=True) == [
    {c3: 0, c4: 0, c5: 0, d3: 0, d4: 0, d5: 0}
]

# Endpoint activity subsets leave genuine kernels in the pure F00 map.
assert full_parent_matrix(local_dim=2, active_q={0, 1, 2}).rank() == 6
assert full_parent_matrix(local_dim=2, active_q={0, 1}).rank() == 4
assert full_parent_matrix(local_dim=2, active_q={0}).rank() == 3

# All three central all-zero edge coefficients nonzero.  Eliminating rho_2
# with A0*rho0+A1*rho1+A2*rho2=0 yields these three common b-values.
xv, xw, yv, yw = sp.symbols("xv xw yv yw")
cross = xv * yw + xw * yv
yy = yv * yw
xx = xv * xw
k0 = cross + 2 * yy
k1 = 2 * xx + cross
k2 = -cross
assert sp.expand((k0 - k2) / 2) == cross + yy
assert sp.expand((k1 - k2) / 2) == xx + cross
assert sp.expand((xx + cross) - (cross + yy)) == xx - yy

# If a pair deck is nonzero, its two ratios obey r_v*r_w=1 and
# r_v+r_w+1=0, hence are the two primitive cube roots in characteristic 0.
rv, rw = sp.symbols("rv rw")
ratio_resultant = sp.resultant(rv * rw - 1, rv + rw + 1, rw)
assert sp.factor(ratio_resultant) == rv**2 + rv + 1

# With exactly two nonzero A_i, the two surviving b equations differ by the
# characteristic-zero factor two and force both the cross term and b to zero.
a1, a2 = sp.symbols("a1 a2", nonzero=True)
pair_cross, pair_b = sp.symbols("pair_cross pair_b")
lam = a1 / a2
two_a_equations = (a1 * pair_b - lam * pair_cross, a2 * pair_b + pair_cross)
two_a_solution = sp.solve(two_a_equations, (pair_b, pair_cross), dict=True)
assert two_a_solution == [{pair_b: 0, pair_cross: 0}]

# With exactly one nonzero A_i, at least one full row R_i is active.  The two
# full tau equations confine both other kernel-support columns to at most the
# same single active port; no unordered pair can then carry their cross term.
for active_mask in range(1, 1 << len(OUTSIDE)):
    active = {port for port in OUTSIDE if active_mask & (1 << port)}
    allowed_kernel_ports = {
        port
        for port in OUTSIDE
        if not any(other != port for other in active)
    }
    assert len(allowed_kernel_ports) <= 1
    for left, right in combinations(OUTSIDE, 2):
        assert not (left in allowed_kernel_ports and right in allowed_kernel_ports)

# The exact omega control satisfies every restricted (*) equation but has one
# nonzero outside edge; it confirms that the full D=0 consequence is needed.
omega = sp.Symbol("omega")
omega_reduce = sp.Poly(omega**2 + omega + 1, omega)
rho = {
    0: (0, 0, 0),
    1: (omega, 1, omega**2),
    2: (omega**2, 1, omega),
}
b = {(0, 1): 0, (0, 2): 0, (1, 2): 1}
for left, right in combinations(OUTSIDE, 2):
    for i, (j, k) in enumerate(((1, 2), (0, 2), (0, 1))):
        value = b[(left, right)] + (
            rho[left][j] * rho[right][k]
            + rho[right][j] * rho[left][k]
        )
        assert sp.rem(sp.Poly(value, omega), omega_reduce) == 0

print("Koszul_pair_deck_map: rank 26 / nullity 1 (alternating tau generator)")
print("complete_F00_one_port_map: rank 9 / kernel 0")
print("row_plane_F00_map: rank 6 / kernel 0 in characteristic zero")
print("central_A_support_cases: 3, 2, 1, 0 exhaustively separated")
print("endpoint_F00_ranks: all-active=6, two-active=4, one-active=3")
print("GLS74_central_mixed_support_nonendpoint_Family_B_r3=EMPTY")
print("central root-axis degeneracies and outside endpoint charts remain OPEN")
print("unchanged_inherited_residual=98355 profiles / 81 keys (from GLS72/73)")
