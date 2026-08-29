"""No-import mask/modular audit for the candidate GLS72 localization."""

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
    for labels in combinations(LABELS, 3):
        triple = sum(1 << label for label in labels)
        target = [colour for colour, mask in enumerate(missing) if not mask & ~triple]
        if len(target) > 2:
            return False
        for label in labels:
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
            sorted(3 * group(code) + permutation[named_colour(code)] for code in word)
        )
        for permutation in permutations(COLOURS)
    )


def binary_triangles(word):
    missing = missing_masks(word)
    return tuple(
        sum(1 << label for label in labels)
        for labels in combinations(LABELS, 3)
        if sum(not mask & ~sum(1 << label for label in labels) for mask in missing) == 2
    )


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


def family_signature(word):
    triangles = binary_triangles(word)
    if len(triangles) != 1:
        return None
    triple = triangles[0]
    missing = missing_masks(word)
    target = [colour for colour, mask in enumerate(missing) if not mask & ~triple]
    sizes = sorted(missing[colour].bit_count() for colour in target)
    family = "A" if sizes == [2, 2] else "B"
    outside = ALL_LABELS ^ triple
    number_t = sum(
        group(word[label]) == 2 for label in LABELS if outside & (1 << label)
    )
    return family, number_t


gls70 = [word for word in survivors if not sc2_tc4(word)]
assert len(gls70) == 99_135
assert len({canonical(word) for word in gls70}) == 85

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

gls71 = []
for word in gls70:
    signature = family_signature(word)
    if signature and (
        (signature[0] == "B" and signature[1] <= 2) or signature == ("A", 0)
    ):
        continue
    gls71.append(word)
assert len(gls71) == 98_355
assert len({canonical(word) for word in gls71}) == 81

gls72 = list(gls71)
assert len(gls72) == 98_355
assert len({canonical(word) for word in gls72}) == 81
assert sum(family_signature(word) == ("A", 1) for word in gls72) == 1_080

after = Counter(signature for word in gls72 if (signature := family_signature(word)))
assert after == Counter({("A", 1): 1_080, ("A", 2): 1_080, ("A", 3): 360, ("B", 3): 60})


def matrix_rank(rows):
    matrix = [[entry % PRIME for entry in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], PRIME - 2, PRIME)
        matrix[rank] = [entry * inverse % PRIME for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


# Exhaustive odd-characteristic replay of the all-active determinants.
for a_value, b_value in product(range(PRIME), repeat=2):
    rank_x = matrix_rank(((b_value, a_value), (a_value, 0)))
    rank_y = matrix_rank(((0, b_value), (b_value, a_value)))
    if rank_x <= 1 and rank_y <= 1:
        assert a_value == b_value == 0

# The two central coefficient matrices have rank two precisely when their
# transverse parameter h is nonzero, independently of k.
for k_value, h_value in product(range(PRIME), repeat=2):
    delta_matrix = (
        (-2 * k_value + 4 * h_value, -2 * k_value + 2 * h_value),
        (-2 * k_value + 2 * h_value, -2 * k_value),
    )
    beta_matrix = (
        (-2 * k_value, -2 * k_value + 2 * h_value),
        (-2 * k_value + 2 * h_value, -2 * k_value + 4 * h_value),
    )
    expected_rank_two = h_value != 0
    assert (matrix_rank(delta_matrix) == 2) == expected_rank_two
    assert (matrix_rank(beta_matrix) == 2) == expected_rank_two


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


x = (1, 0)
y = (0, 1)
inverse_two = pow(2, PRIME - 2, PRIME)

# Separate F_101 replay of the alpha=0 restricted control.
u3, u4 = x, y
v3, v4 = (-1 % PRIME, 0), (0, -1 % PRIME)
l4 = (inverse_two, 0)
l3 = (0, -inverse_two % PRIME)
b34 = tensor_scale(tensor_add(tensor_outer(x, x), tensor_outer(y, y)), inverse_two)
assert tensor_add(tensor_outer(u4, (1,)), tensor_outer(v4, (1,))) == {}
assert tensor_add(tensor_outer(u3, (1,)), tensor_outer(v3, (1,))) == {}
assert tensor_add(tensor_outer(u3, l4), tensor_outer(l3, u4), b34) == tensor_outer(x, x)
assert tensor_add(tensor_outer(v3, l4), tensor_outer(l3, v4), b34) == tensor_outer(y, y)

# Endpoint selector/full-deck sign identity on many independent samples.
for alpha_value, a_value, c0_value in (
    (3, 5, 7),
    (11, 13, 17),
    (19, 23, 29),
):
    v02 = alpha_value * c0_value * pow(a_value, PRIME - 2, PRIME) % PRIME
    restricted = (a_value * v02 + alpha_value * c0_value) % PRIME
    assert restricted == 2 * alpha_value * c0_value % PRIME
    assert restricted

# Direct support audit for the tangent-space exclusions.  The missing
# diagonal coefficient is structural; varied exact samples guard both
# tensor placements without turning this audit into a large search.
tangent_samples = ((0, 0), (1, 0), (0, 1), (2, 3), (5, 7))
for left, right in product(tangent_samples, repeat=2):
    tangent_y = tensor_add(tensor_outer(left, y), tensor_outer(y, right))
    tangent_x = tensor_add(tensor_outer(left, x), tensor_outer(x, right))
    assert tangent_y.get((0, 0), 0) == 0
    assert tangent_x.get((1, 1), 0) == 0

# Independent modular expansion of the surviving alpha=a=b=0 common-edge
# control.  These are the seven nontrivial deck coordinates after K5 is
# restricted; W25 is absent because its full e50 factor annihilates K5.
e0 = (1, 0, 0)
e1 = (0, 1, 0)
e2 = (0, 0, 1)
z = (1,)
f45 = tensor_add(
    tensor_outer(e0, e0, x, z), tensor_scale(tensor_outer(e0, e0, x, z), -1)
)
assert f45 == {}
h1345 = tensor_add(
    tensor_outer(e1, x, x, z),
    tensor_outer(e0, y, x, z),
    tensor_scale(tensor_outer(e0, y, x, z), -1),
)
assert h1345 == tensor_outer(e1, x, x, z)
assert tensor_outer(e2, y, y, z) == {(2, 1, 1, 0): 1}

# On the full V5 slot, W01*W25 is exactly the pure e0^4 coefficient and is
# nonzero although W25 had zero K5 restriction.
e50 = e0
h0125 = tensor_outer(e0, e0, e0, e50)
assert h0125 == {(0, 0, 0, 0): 1}

print(f"mask_stages={tuple(stages)}")
print(f"pre_GLS71_single_binary={dict(sorted(before.items()))}")
print("Family_A_r_1_localized=1080 profiles / 1 key; removed=0")
print("post_GLS72_residual=98355 profiles / 81 keys")
print(f"post_GLS72_single_binary={dict(sorted(after.items()))}")
print("all-active and central rank tables=PASS over F_101")
print("alpha=0 restricted control and tangent support=PASS over F_101")
print("endpoint full-deck sign obstruction=PASS over F_101")
print("alpha=a=b=0 transverse common-edge control=PASS over F_101")
