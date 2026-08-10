"""Primary symbolic checks for cross-root coordinate chart compatibility."""

from itertools import product

import sympy as sp

e = sp.eye(3)
v = sp.Matrix([1, 1, 1])

# Columns are bases for the three planes in the note.
planes = (
    sp.Matrix.hstack(v, sp.Matrix([1, 0, 0])),  # x1=x2
    sp.Matrix.hstack(v, sp.Matrix([0, 0, 1])),  # x0=x1
    sp.Matrix.hstack(v, sp.Matrix([0, 1, 0])),  # x0=x2
)
normals = (
    sp.Matrix([[0, 1, -1]]),
    sp.Matrix([[1, -1, 0]]),
    sp.Matrix([[1, 0, -1]]),
)
for label, (plane, normal) in enumerate(zip(planes, normals, strict=True)):
    assert plane.rank() == 2
    assert normal * plane == sp.zeros(1, 2)
    assert e[0, :] * plane == e[label, :] * plane
    assert all(coordinate != 0 for coordinate in v)

# The common physical residual edge is e0 tensor e0.
residual_edge = sp.zeros(3)
residual_edge[0, 0] = 1
for left_label, right_label in product(range(3), repeat=2):
    left_plane = planes[left_label]
    right_plane = planes[right_label]
    restricted = left_plane.T * residual_edge * right_plane
    left_coordinate = e[left_label, :] * left_plane
    right_coordinate = e[right_label, :] * right_plane
    expected = left_coordinate.T * right_coordinate
    assert restricted == expected
    assert (v.T * residual_edge * v)[0] == 1

# Every pair of distinct planes intersects in exactly the common torus line Kv.
for left, right in ((0, 1), (0, 2), (1, 2)):
    stacked_normals = normals[left].col_join(normals[right])
    assert stacked_normals.rank() == 2
    assert stacked_normals.nullspace() == [v]
    # All coordinate transition gains at v equal one, so every cycle is flat.
    for first_label, second_label in product(range(3), repeat=2):
        assert v[first_label] / v[second_label] == 1

# A coordinate-separating overlap really forbids a label change.
assert sp.Matrix.vstack(e[0, :] * planes[0], e[1, :] * planes[0]).rank() == 2

# One fixed six-root gate system generates all nine kernel-plane charts.
omega = sp.Matrix([[1, -1, 0]])
x_off = v
x_on = sp.Matrix([2, 1, 1])
assert (omega * x_off)[0] == 0
assert (omega * x_on)[0] == 1
# The blocker-side left endpoint e2 has the same value in every gate state.
blocker_endpoint = sp.Matrix([[0, 0, 1]])
assert (blocker_endpoint * x_off)[0] == 1
assert (blocker_endpoint * x_on)[0] == 1
for active in range(3):
    incidence_rows = []
    for root in range(3):
        scalar = (omega * (x_on if root == active else x_off))[0]
        incidence_rows.append(scalar * normals[root])
    incidence = sp.Matrix.vstack(*incidence_rows)
    assert incidence.rowspace() == normals[active].rowspace()
    assert incidence * planes[active] == sp.zeros(3, 2)
    assert incidence.rank() == 1

# Nine torus line-pair tensors form a basis of the 3x3 edge space.
x_rows = sp.Matrix([[1, t, t**2] for t in (1, 2, 3)])
y_rows = sp.Matrix([[1, t, t**2] for t in (4, 5, 6)])
assert x_rows.det() != 0
assert y_rows.det() != 0
evaluation_rows = []
for i, j in product(range(3), repeat=2):
    x = x_rows[i, :].T
    y = y_rows[j, :].T
    evaluation_rows.append(sp.Matrix(list(x * y.T)).reshape(1, 9))
evaluation_matrix = sp.Matrix.vstack(*evaluation_rows)
assert evaluation_matrix.rank() == 9

# Arbitrary symbolic chart values interpolate through one common edge.
h_symbols = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"h{i}{j}"))
interpolated_edge = x_rows.inv() * h_symbols * y_rows.inv().T
assert sp.simplify(x_rows * interpolated_edge * y_rows.T - h_symbols) == sp.zeros(3)

# On each torus line every coordinate label is a valid trivialization.
for i, j, left_label, right_label in product(range(3), repeat=4):
    denominator = x_rows[i, left_label] * y_rows[j, right_label]
    assert denominator != 0
    chart_scalar = h_symbols[i, j] / denominator
    assert sp.expand(chart_scalar * denominator - h_symbols[i, j]) == 0

print("cross-chart overlap and holonomy law: PASS")
print("nine overlapping coordinate-labelled plane charts: PASS")
print("common gated root-kernel realization: PASS")
print("nine-chart evaluation universality: PASS")
print("GLOBAL KRENN-GU STATUS: UNRESOLVED")
