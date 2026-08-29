"""Independent sparse audit for the GLS73 two-row nonextension."""

from itertools import combinations


PRIME = 101
LABELS = tuple(range(6))


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(remainder):
            yield ((first, partner),) + tail


# Audit the matching supports independently of the primary symbolic engine.
fixed_support = {
    (0, 1, 0, 0): 1,
    (1, 3, 1, 1): 1,
    (1, 3, 0, 2): 1,
    (1, 4, 0, 1): -1,
    (2, 4, 2, 2): 1,
}


def edge_value(entries, i, j, colour_i, colour_j):
    if i < j:
        key = (i, j, colour_i, colour_j)
    else:
        key = (j, i, colour_j, colour_i)
    return entries.get(key, 0) % PRIME


def deck(entries, vertices, word):
    colour = dict(zip(vertices, word))
    total = 0
    contributing = []
    for matching in matchings(vertices):
        value = 1
        for i, j in matching:
            value = value * edge_value(entries, i, j, colour[i], colour[j]) % PRIME
        if value:
            contributing.append(matching)
            total = (total + value) % PRIME
    return total, tuple(contributing)


for xi in (1, 7, 37, 100):
    entries = dict(fixed_support)
    # Fill every incident-edge entry independently.  Only W25(0,0)=xi may
    # survive in either selected row.
    for i in range(5):
        for left_colour in range(3):
            for right_colour in range(3):
                entries[(i, 5, left_colour, right_colour)] = (
                    17 * i + 11 * left_colour + 7 * right_colour + 3
                ) % PRIME
    entries[(2, 5, 0, 0)] = xi

    h0125, support0125 = deck(entries, (0, 1, 2, 5), (0, 0, 0, 0))
    h1245, support1245 = deck(entries, (1, 2, 4, 5), (0, 0, 1, 0))
    h0124, support0124 = deck(entries, (0, 1, 2, 4), (2, 0, 0, 1))

    assert h0125 == xi
    assert h1245 == -xi % PRIME
    assert h0124 == 0
    assert support0125 == (((0, 1), (2, 5)),)
    assert support1245 == (((1, 4), (2, 5)),)
    assert support0124 == ()

# Independently enumerate all fifteen possible source pairs for the two probe
# rows.  Each support map records every local colour that could accompany the
# selected probe coefficient.  In particular q5 may be arbitrary, whereas
# whole-covector silence removes every P0 endpoint at port 5.
p0_support = {3: {0}, 4: {0}}
q0_support = {3: {0}, 4: {0}}
q2_support = {0: {2}, 3: {0}, 4: {0}, 5: {0, 1, 2}}


def compatible_source_pairs(left_support, right_support, local_word):
    pairs = set()
    for i, j in combinations(LABELS, 2):
        forward = (
            local_word[i] in left_support.get(i, set())
            and local_word[j] in right_support.get(j, set())
        )
        reverse = (
            local_word[i] in right_support.get(i, set())
            and local_word[j] in left_support.get(j, set())
        )
        if forward or reverse:
            pairs.add((i, j))
    return pairs


diagonal_word = (0, 0, 0, 0, 0, 0)
diagonal_pairs = compatible_source_pairs(p0_support, q0_support, diagonal_word)
assert diagonal_pairs == {(3, 4)}

# For omega=(2,0,0,0,1,0), derive the complete probe-compatible set and
# evaluate both complementary decks to separate the direct and repair rows.
mixed_word = (2, 0, 0, 0, 1, 0)
mixed_pairs = compatible_source_pairs(p0_support, q2_support, mixed_word)
assert mixed_pairs == {(0, 3), (3, 5)}

mixed_decks = {}
for i, j in mixed_pairs:
    complement = tuple(label for label in LABELS if label not in (i, j))
    complement_word = tuple(mixed_word[label] for label in complement)
    mixed_decks[(i, j)] = deck(entries, complement, complement_word)

mixed_direct = {pair for pair, (_, support) in mixed_decks.items() if support}
mixed_repair = {pair for pair, (_, support) in mixed_decks.items() if not support}
assert mixed_direct == {(0, 3)}
assert mixed_repair == {(3, 5)}

for a, b, c, d, mu0 in ((1, 0, 0, 1, 1), (2, 3, 5, 7, 11), (9, 4, 8, 6, 13)):
    c34 = (a * d + b * c) % PRIME
    assert a and c34 and mu0
    xi_from_diagonal = mu0 * pow(c34, -1, PRIME) % PRIME
    assert xi_from_diagonal
    assert (-a * xi_from_diagonal) % PRIME != 0

print("independent matching supports: H0125=xi, H1245=-xi, H0124 repair=0")
print("independent source supports: diagonal={34}, mixed direct={03}, repair={35}")
print("two-row contradiction=PASS over F_101")
print("GLS73 scope audit: fixed off-port core only; Family A r=1 remains OPEN")
print("unchanged inherited residual=98355 profiles / 81 keys (from GLS72)")
