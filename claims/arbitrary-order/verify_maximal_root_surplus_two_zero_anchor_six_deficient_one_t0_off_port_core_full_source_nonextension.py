"""Primary exact checks for the GLS73 off-port-core nonextension theorem."""

from collections import defaultdict
from itertools import combinations

import sympy as sp


LABELS = tuple(range(6))
ZERO = sp.Integer(0)
ONE = sp.Integer(1)

A, B, C, D, MU0, XI = sp.symbols("A B C D MU0 XI")
Q32, Q42, Q50, Q51, Q52 = sp.symbols("Q32 Q42 Q50 Q51 Q52")


def add_term(table, key, value):
    table[key] = sp.expand(table.get(key, ZERO) + value)
    if table[key] == 0:
        del table[key]


# Sparse probe coefficient vectors.  A key is (probe_colour, local_colour).
p = [defaultdict(lambda: ZERO) for _ in LABELS]
q = [defaultdict(lambda: ZERO) for _ in LABELS]

# Crossed triangle normalization.
p[0][(1, 1)] = ONE
q[0][(2, 2)] = ONE
p[1][(2, 2)] = ONE
q[2][(1, 1)] = ONE

# The two R0 rows and the silent P0/Q0 coefficient at port 5.
p[3][(0, 0)] = A
q[3][(0, 0)] = B
p[4][(0, 0)] = C
q[4][(0, 0)] = D
q[3][(2, 0)] = Q32
q[4][(2, 0)] = Q42
q[5][(2, 0)] = Q50
q[5][(2, 1)] = Q51
q[5][(2, 2)] = Q52

# Only entries needed by the selected matching rows are materialized.  The
# five incident edges are arbitrary; irrelevant entries receive independent
# names so accidental cancellation cannot be hidden.
incident = {}
incident_symbols = []
for i in range(5):
    for left_colour in range(3):
        for right_colour in range(3):
            symbol = sp.Symbol(f"W{i}5_{left_colour}{right_colour}")
            incident[(i, 5, left_colour, right_colour)] = symbol
            incident_symbols.append(symbol)
incident[(2, 5, 0, 0)] = XI

# Fixed off-port core, keyed by ordered endpoint colours.
edge = defaultdict(lambda: ZERO)
edge[(0, 1, 0, 0)] = ONE
edge[(1, 3, 1, 1)] = ONE
edge[(1, 3, 0, 2)] = ONE
edge[(1, 4, 0, 1)] = -ONE
edge[(2, 4, 2, 2)] = ONE
edge.update(incident)


def edge_entry(i, j, colour_i, colour_j):
    if i < j:
        return edge[(i, j, colour_i, colour_j)]
    return edge[(j, i, colour_j, colour_i)]


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for remainder in matchings(rest):
            yield ((first, second),) + remainder


def deck_coefficient(vertices, local_colours):
    result = ZERO
    colour = dict(zip(vertices, local_colours))
    for matching in matchings(vertices):
        term = ONE
        for i, j in matching:
            term *= edge_entry(i, j, colour[i], colour[j])
        result += term
    return sp.expand(result)


def source_coefficient(probe_pair, local_word):
    left_probe, right_probe = probe_pair
    result = ZERO
    for i, j in combinations(LABELS, 2):
        companion = (
            p[i][(left_probe, local_word[i])] * q[j][(right_probe, local_word[j])]
            + q[i][(right_probe, local_word[i])] * p[j][(left_probe, local_word[j])]
        )
        complement = tuple(label for label in LABELS if label not in (i, j))
        deck_word = tuple(local_word[label] for label in complement)
        result += companion * deck_coefficient(complement, deck_word)
    return sp.expand(result)


all_zero_word = (0, 0, 0, 0, 0, 0)
mixed_word = (2, 0, 0, 0, 1, 0)

diagonal_source = source_coefficient((0, 0), all_zero_word)
mixed_source = source_coefficient((0, 2), mixed_word)

assert sp.expand(diagonal_source - (A * D + B * C) * XI) == 0
assert mixed_source == -A * XI
assert deck_coefficient((0, 1, 2, 5), (0, 0, 0, 0)) == XI
assert deck_coefficient((1, 2, 4, 5), (0, 0, 1, 0)) == -XI
assert deck_coefficient((0, 1, 2, 4), (2, 0, 0, 1)) == 0

# The two source equations are inconsistent on A*(AD+BC)*MU0 != 0.
diagonal_residual = sp.expand(diagonal_source - MU0)
mixed_residual = mixed_source
resultant = sp.resultant(diagonal_residual, mixed_residual, XI)
assert sp.factor(resultant) == -A * MU0

print("P0Q0_all_zero=(AD+BC)*xi=mu0")
print("P0Q2_mixed=-A*xi=0")
print("resultant=-A*mu0")
print("arbitrary incident-edge and unused-probe symbols cancel from both rows")
print("GLS73_off_port_core_full_source_completion=EMPTY")
print("unchanged_inherited_residual=98355 profiles / 81 keys (from GLS72)")
