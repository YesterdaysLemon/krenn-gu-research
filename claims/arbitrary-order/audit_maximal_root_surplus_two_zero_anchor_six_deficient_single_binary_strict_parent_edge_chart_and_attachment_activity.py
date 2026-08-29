"""No-import mask/tensor audit for the candidate GLS71 theorem."""

from collections import Counter, defaultdict
from itertools import combinations, permutations, product

PRIME = 101
COLOURS = range(3)
LABELS = range(6)
ALL_COLOURS = 0b111
ALL_LABELS = 0b111111


def group(code):
    return code // 3


def named_colour(code):
    return code % 3


def support(code):
    colour = named_colour(code)
    if group(code) == 0:
        return 1 << colour
    return ALL_COLOURS ^ (1 << colour)


def local_rank(code):
    return 1 if group(code) == 1 else 2


def missing_masks(word):
    result = []
    for colour in COLOURS:
        mask = 0
        for label, code in enumerate(word):
            if not support(code) & (1 << colour):
                mask |= 1 << label
        result.append(mask)
    return tuple(result)


def gls63(word):
    return all(mask.bit_count() >= 2 for mask in missing_masks(word))


def gls67_pairs(word):
    missing = missing_masks(word)
    for left, right in combinations(LABELS, 2):
        pair = (1 << left) | (1 << right)
        target_rank = sum(mask == pair for mask in missing)
        if not target_rank:
            continue
        if target_rank > 2:
            return False
        if local_rank(word[left]) < target_rank:
            return False
        if local_rank(word[right]) < target_rank:
            return False
        if target_rank == 1 and local_rank(word[left]) == local_rank(word[right]) == 2:
            return False
    return True


def triangle_span(word):
    missing = missing_masks(word)
    for triple_tuple in combinations(LABELS, 3):
        triple = sum(1 << label for label in triple_tuple)
        target = [colour for colour, mask in enumerate(missing) if not mask & ~triple]
        if len(target) > 2:
            return False
        for label in triple_tuple:
            code = word[label]
            if (
                group(code) == 1
                and sum(colour != named_colour(code) for colour in target) > 1
            ):
                return False
    return True


def canonical(word):
    return min(
        tuple(
            sorted(
                3 * group(code) + colour_permutation[named_colour(code)]
                for code in word
            )
        )
        for colour_permutation in permutations(COLOURS)
    )


def binary_triangles(word):
    missing = missing_masks(word)
    result = []
    for triple_tuple in combinations(LABELS, 3):
        triple = sum(1 << label for label in triple_tuple)
        if sum(not mask & ~triple for mask in missing) == 2:
            result.append(triple)
    return tuple(result)


stages = [0, 0, 0, 0]
survivors = []
for word in product(range(9), repeat=6):
    stages[0] += 1
    if not gls63(word):
        continue
    stages[1] += 1
    if not gls67_pairs(word):
        continue
    stages[2] += 1
    if not triangle_span(word):
        continue
    stages[3] += 1
    survivors.append(word)

assert tuple(stages) == (531_441, 276_750, 99_855, 99_180)
assert len({canonical(word) for word in survivors}) == 86


def sc2_tc4(word):
    for colour in COLOURS:
        if (
            sum(code == colour for code in word) == 2
            and sum(code == 6 + colour for code in word) == 4
        ):
            return True
    return False


gls70 = [word for word in survivors if not sc2_tc4(word)]
assert len(gls70) == 99_135
assert len({canonical(word) for word in gls70}) == 85


def family_signature(word):
    triangles = binary_triangles(word)
    if len(triangles) != 1:
        return None
    missing = missing_masks(word)
    triple = triangles[0]
    target = [colour for colour, mask in enumerate(missing) if not mask & ~triple]
    sizes = sorted(missing[colour].bit_count() for colour in target)
    family = "A" if sizes == [2, 2] else "B"
    outside = ALL_LABELS ^ triple
    number_t = sum(
        group(word[label]) == 2 for label in LABELS if outside & (1 << label)
    )
    return family, number_t


before = Counter(signature for word in gls70 if (signature := family_signature(word)))
assert before == Counter(
    {
        ("A", 0): 360,
        ("A", 1): 1_080,
        ("A", 2): 1_080,
        ("A", 3): 360,
        ("B", 0): 60,
        ("B", 1): 180,
        ("B", 2): 180,
        ("B", 3): 60,
    }
)


gls71 = [
    word
    for word in gls70
    if not (
        (signature := family_signature(word))
        and ((signature[0] == "B" and signature[1] <= 2) or signature == ("A", 0))
    )
]
assert len(gls71) == 98_355
assert len({canonical(word) for word in gls71}) == 81

after = Counter(signature for word in gls71 if (signature := family_signature(word)))
assert after == Counter(
    {
        ("A", 1): 1_080,
        ("A", 2): 1_080,
        ("A", 3): 360,
        ("B", 3): 60,
    }
)


def tensor_add(*tensors):
    result = defaultdict(int)
    for tensor in tensors:
        for index, coefficient in tensor.items():
            result[index] = (result[index] + coefficient) % PRIME
    return {index: value for index, value in result.items() if value}


def tensor_scale(tensor, scalar):
    return {
        index: scalar * coefficient % PRIME
        for index, coefficient in tensor.items()
        if scalar * coefficient % PRIME
    }


def tensor_outer(*vectors):
    result = {}
    for indices in product(*(range(len(vector)) for vector in vectors)):
        coefficient = 1
        for vector, index in zip(vectors, indices):
            coefficient = coefficient * vector[index] % PRIME
        if coefficient:
            result[indices] = coefficient
    return result


# Independent six-permutation P3 expansion.  Local columns are p=(1,0),
# q=(0,1), h_i=a_i p+b_i q.
p_column = (1, 0)
q_column = (0, 1)
edge_r = 7
edge_s = 11
inverse_two = pow(2, PRIME - 2, PRIME)
a = (
    -edge_r * inverse_two % PRIME,
    edge_r * inverse_two % PRIME,
    edge_r * inverse_two % PRIME,
)
b = (
    edge_s * inverse_two % PRIME,
    -edge_s * inverse_two % PRIME,
    edge_s * inverse_two % PRIME,
)
h_columns = tuple((a[i], b[i]) for i in range(3))

p3 = {}
for source_permutation in permutations((0, 1, 2)):
    columns = []
    for mode, source in enumerate(source_permutation):
        columns.append((p_column, q_column, h_columns[mode])[source])
    p3 = tensor_add(p3, tensor_outer(*columns))
assert p3 == {(1, 0, 0): edge_r, (1, 0, 1): edge_s}

cube = tuple(product((0, 1), repeat=3))
edges = {
    tuple(sorted((left, right)))
    for left in cube
    for right in cube
    if {sum(left), sum(right)} == {1, 2}
    and sum(a_bit != b_bit for a_bit, b_bit in zip(left, right)) == 1
}
assert len(edges) == 6

# Endpoint replay: deleting either edge coefficient leaves one nonzero cube
# vertex and no unlisted term.
assert tensor_scale(p3, 1) == p3
p3_r = {index: value for index, value in p3.items() if index == (1, 0, 0)}
p3_s = {index: value for index, value in p3.items() if index == (1, 0, 1)}
assert len(p3_r) == len(p3_s) == 1

# Separate finite-field two-selector physical control.
x = (1, 0)
y = (0, 1)
k = (x, x, y)
l = (y, y, x)
b45 = tensor_add(
    tensor_scale(tensor_outer(x, x), -1), tensor_scale(tensor_outer(y, y), -1)
)
b35 = tensor_add(
    tensor_scale(tensor_outer(x, x), -1), tensor_scale(tensor_outer(y, y), -1)
)
b34 = tensor_add(tensor_outer(x, y), tensor_outer(y, x))


def zero_deck(left, right, deck):
    return tensor_add(
        deck,
        tensor_outer(k[left], l[right]),
        tensor_outer(l[left], k[right]),
    )


assert zero_deck(1, 2, b45) == {}
assert zero_deck(0, 2, b35) == {}
assert zero_deck(0, 1, b34) == tensor_scale(b34, 2)


def spoke_deck(port, spoke, deck):
    result = {}
    other = tuple(index for index in range(3) if index != port)
    for local_coordinate in range(2):
        for deck_indices, coefficient in deck.items():
            indices = [0, 0, 0]
            indices[port] = local_coordinate
            indices[other[0]] = deck_indices[0]
            indices[other[1]] = deck_indices[1]
            value = spoke[local_coordinate] * coefficient % PRIME
            if value:
                result[tuple(indices)] = value
    return result


k_attachment = tensor_add(
    spoke_deck(0, k[0], b45),
    spoke_deck(1, k[1], b35),
    spoke_deck(2, k[2], b34),
)
l_attachment = tensor_add(
    spoke_deck(0, l[0], b45),
    spoke_deck(1, l[1], b35),
    spoke_deck(2, l[2], b34),
)
assert k_attachment == tensor_scale(tensor_outer(x, x, x), -2)
assert l_attachment == tensor_scale(tensor_outer(y, y, y), -2)


def vector_linear(x_coefficient, y_coefficient):
    return (x_coefficient % PRIME, y_coefficient % PRIME)


def projected_b_attachment(s_coefficient, q_coefficient):
    spokes = (
        vector_linear(s_coefficient, -q_coefficient),
        vector_linear(s_coefficient, -q_coefficient),
        vector_linear(q_coefficient, s_coefficient),
    )
    return tensor_add(
        spoke_deck(0, spokes[0], b45),
        spoke_deck(1, spokes[1], b35),
        spoke_deck(2, spokes[2], b34),
    )


def projected_d_attachment(r_coefficient, tau_coefficient):
    spokes = (
        vector_linear(-tau_coefficient, r_coefficient),
        vector_linear(-tau_coefficient, r_coefficient),
        vector_linear(r_coefficient, tau_coefficient),
    )
    return tensor_add(
        spoke_deck(0, spokes[0], b45),
        spoke_deck(1, spokes[1], b35),
        spoke_deck(2, spokes[2], b34),
    )


def matrix_rank_mod(rows):
    matrix = [list(row) for row in rows if any(entry % PRIME for entry in row)]
    rank = 0
    number_columns = len(matrix[0]) if matrix else 0
    for column in range(number_columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column] % PRIME),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % PRIME, PRIME - 2, PRIME)
        matrix[rank] = [entry * inverse % PRIME for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            factor = matrix[row][column] % PRIME
            if factor:
                matrix[row] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


# A separate finite-field rank replay of (58)--(59): each zero projected
# attachment kills both of its two scalar parameters.
all_words = tuple(product((0, 1), repeat=3))
b_s = projected_b_attachment(1, 0)
b_q = projected_b_attachment(0, 1)
d_r = projected_d_attachment(1, 0)
d_tau = projected_d_attachment(0, 1)
assert (
    matrix_rank_mod([(b_s.get(word, 0), b_q.get(word, 0)) for word in all_words]) == 2
)
assert (
    matrix_rank_mod([(d_r.get(word, 0), d_tau.get(word, 0)) for word in all_words]) == 2
)

# The alpha=0 proportional case would make a rank-one separated term equal
# the sum of the two target cubes.  This flattening has rank two.
target_sum = tensor_add(tensor_outer(x, x, x), tensor_outer(y, y, y))
target_flattening = [
    (target_sum.get((left, right, 0), 0), target_sum.get((left, right, 1), 0))
    for left, right in product((0, 1), repeat=2)
]
assert matrix_rank_mod(target_flattening) == 2

# Independent activity-mask check.  A nonzero pure P0Q0 pair needs at least
# two active ports; three active ports supply three E equations, so the only
# unexcluded support size is exactly two.
activity_sizes = Counter()
for states in product(range(4), repeat=3):
    # 0=silent, 1=P, 2=Q, 3=both.
    p_active = {i for i, state in enumerate(states) if state & 1}
    q_active = {i for i, state in enumerate(states) if state & 2}
    union = p_active | q_active
    has_pair = any(i != j for i in p_active for j in q_active)
    if has_pair:
        activity_sizes[len(union)] += 1
assert activity_sizes == Counter({2: 21, 3: 25})

print(f"mask_stages={tuple(stages)}")
print(f"pre_GLS71_single_binary={dict(sorted(before.items()))}")
print("Family_B_r_le_2_removed=420 profiles / 3 keys")
print("Family_A_r_0_removed=360 profiles / 1 key")
print("post_GLS71_residual=98355 profiles / 81 keys")
print(f"post_GLS71_single_binary={dict(sorted(after.items()))}")
print("P3_edge_chart_and_endpoints=PASS over F_101")
print("activity_support_fork=PASS; two-selector restricted control=PASS")
print("one-silent projection ranks=PASS over F_101")
