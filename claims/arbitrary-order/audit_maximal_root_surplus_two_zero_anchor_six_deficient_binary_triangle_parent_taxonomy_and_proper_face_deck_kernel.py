"""Independent mask/tensor audit for the candidate GLS70 theorem."""

from collections import Counter
from itertools import combinations, permutations, product

P = 101
COLOURS = range(3)
LABELS = range(6)
ALL_COLOURS = 0b111
ALL_LABELS = 0b111111

# Codes 0..2 are S_c, 3..5 are R_c, and 6..8 are T_c.  The stored colour is
# the singleton support for S and the missing/readout colour for R,T.


def group(code):
    return code // 3


def named_colour(code):
    return code % 3


def support(code):
    colour = named_colour(code)
    if group(code) == 0:
        return 1 << colour
    return ALL_COLOURS ^ (1 << colour)


def rank(code):
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


def popcount(value):
    return value.bit_count()


def gls63(word):
    missing = missing_masks(word)
    return all(popcount(mask) >= 2 for mask in missing)


def gls67_pairs(word):
    missing = missing_masks(word)
    for left, right in combinations(LABELS, 2):
        pair = (1 << left) | (1 << right)
        target_rank = sum(mask == pair for mask in missing)
        if not target_rank:
            continue
        if target_rank > 2 or rank(word[left]) < target_rank:
            return False
        if rank(word[right]) < target_rank:
            return False
        if target_rank == 1 and rank(word[left]) == rank(word[right]) == 2:
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
    candidates = []
    for permutation in permutations(COLOURS):
        moved = tuple(
            sorted(3 * group(code) + permutation[named_colour(code)] for code in word)
        )
        candidates.append(moved)
    return min(candidates)


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

single = [word for word in survivors if len(binary_triangles(word)) == 1]
four = [word for word in survivors if len(binary_triangles(word)) == 4]
assert len(single) == 3_360 and len(four) == 45
assert len({canonical(word) for word in single}) == 8
assert len({canonical(word) for word in four}) == 1


def family_signature(word):
    missing = missing_masks(word)
    triple = binary_triangles(word)[0]
    target = [colour for colour, mask in enumerate(missing) if not mask & ~triple]
    third = next(colour for colour in COLOURS if colour not in target)
    outside = ALL_LABELS ^ triple
    assert missing[third] == outside
    sizes = sorted(popcount(missing[colour]) for colour in target)
    if sizes == [2, 2]:
        family = "pair-pair"
        common = missing[target[0]] & missing[target[1]]
        assert popcount(common) == 1
        common_label = (common & -common).bit_length() - 1
        assert group(word[common_label]) == 0
        assert named_colour(word[common_label]) == third
        for colour in target:
            other = missing[colour] & ~common
            label = (other & -other).bit_length() - 1
            assert group(word[label]) == 1
            assert named_colour(word[label]) == colour
    elif sizes == [3, 3]:
        family = "triple-triple"
        assert all(missing[colour] == triple for colour in target)
        assert all(
            group(word[label]) == 0 and named_colour(word[label]) == third
            for label in LABELS
            if triple & (1 << label)
        )
    else:
        raise AssertionError(sizes)

    outside_t = sum(
        group(word[label]) == 2 for label in LABELS if outside & (1 << label)
    )
    return family, outside_t


family_counts = Counter(map(family_signature, single))
assert family_counts == Counter(
    {
        ("pair-pair", 0): 360,
        ("pair-pair", 1): 1_080,
        ("pair-pair", 2): 1_080,
        ("pair-pair", 3): 360,
        ("triple-triple", 0): 60,
        ("triple-triple", 1): 180,
        ("triple-triple", 2): 180,
        ("triple-triple", 3): 60,
    }
)


def sc2_tc4(word):
    for colour in COLOURS:
        if (
            sum(code == colour for code in word) == 2
            and sum(code == 6 + colour for code in word) == 4
        ):
            return True
    return False


assert all(sc2_tc4(word) for word in four)
remaining = [word for word in survivors if not sc2_tc4(word)]
assert len(remaining) == 99_135
assert len({canonical(word) for word in remaining}) == 85


def modular_rank(matrix):
    rows = [[entry % P for entry in row] for row in matrix]
    if not rows:
        return 0
    pivot_row = 0
    width = len(rows[0])
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], P - 2, P)
        rows[pivot_row] = [(entry * inverse) % P for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % P
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


# Separate finite-field check of the P_c triangle coefficient.  The two
# endpoint Q-forms use different Q coordinates, so the six deck coordinates
# give six independent columns.
triangle_rows = []
for q_colour, s_coordinate, t_coordinate in product(COLOURS, repeat=3):
    row = [0] * 6
    if q_colour == 1 and s_coordinate == 1:
        row[t_coordinate] = 1
    if q_colour == 0 and t_coordinate == 0:
        row[3 + s_coordinate] = 1
    triangle_rows.append(row)
assert modular_rank(triangle_rows) == 6


def flat_index(indices):
    return sum(index * 3 ** (3 - slot) for slot, index in enumerate(indices))


def tensor_product(vectors):
    result = {}
    for indices in product(COLOURS, repeat=4):
        coefficient = 1
        for slot, index in enumerate(indices):
            coefficient = coefficient * vectors[slot][index] % P
        if coefficient:
            result[tuple(indices)] = coefficient
    return result


def edge(left, right, scale=1):
    return {
        (i, j): scale * left[i] * right[j] % P
        for i, j in product(COLOURS, repeat=2)
        if scale * left[i] * right[j] % P
    }


def matching(pair_a, edge_a, pair_b, edge_b):
    result = {}
    for indices in product(COLOURS, repeat=4):
        coefficient = (
            edge_a.get((indices[pair_a[0]], indices[pair_a[1]]), 0)
            * edge_b.get((indices[pair_b[0]], indices[pair_b[1]]), 0)
            % P
        )
        if coefficient:
            result[indices] = coefficient
    return result


def add_tensors(*tensors):
    result = {}
    for tensor in tensors:
        for index, coefficient in tensor.items():
            result[index] = (result.get(index, 0) + coefficient) % P
            if not result[index]:
                del result[index]
    return result


lambdas = (2, 3, 5, 7)
vectors_v = tuple((1, value, 0) for value in lambdas)
vectors_r = tuple(((-value) % P, 1, 0) for value in lambdas)
ea = (1, 0, 0)
for v, r in zip(vectors_v, vectors_r):
    assert sum(left * right for left, right in zip(v, r)) % P == 0

kappa = 11
chi = 13
hafnian = add_tensors(
    matching(
        (0, 1),
        edge(vectors_r[0], vectors_r[1], kappa),
        (2, 3),
        edge(vectors_r[2], vectors_r[3]),
    ),
    matching((0, 2), edge(ea, ea), (1, 3), edge(ea, ea, 1 - chi)),
    matching((0, 3), edge(ea, ea), (1, 2), edge(ea, ea, chi)),
)
expected = add_tensors(
    tensor_product((ea, ea, ea, ea)),
    {
        index: kappa * coefficient % P
        for index, coefficient in tensor_product(vectors_r).items()
    },
)
assert hafnian == expected

# A different modular row reduction checks the common kernel of all one-slot
# contractions.  Since those maps are part of the complete proper-face map,
# the common nullity must be 16.
contractions = []
for slot in range(4):
    others = tuple(index for index in range(4) if index != slot)
    for other_indices in product(COLOURS, repeat=3):
        row = [0] * 81
        for contracted_coordinate in COLOURS:
            indices = [0, 0, 0, 0]
            indices[slot] = contracted_coordinate
            for other_slot, coordinate in zip(others, other_indices):
                indices[other_slot] = coordinate
            row[flat_index(indices)] = vectors_v[slot][contracted_coordinate]
        contractions.append(row)
assert modular_rank(contractions) == 65
assert 81 - modular_rank(contractions) == 16

free = tensor_product(vectors_r)
for row in contractions:
    assert (
        sum(row[flat_index(index)] * coefficient for index, coefficient in free.items())
        % P
        == 0
    )

print(f"mask_stages={tuple(stages)}")
print(f"family_counts={dict(sorted(family_counts.items()))}")
print("S_c^2T_c^4 exclusion census: 45/1 -> residual 99135/85")
print("triangle cancellation rank=6 over F_101")
print("proper-face nullity=16 over F_101; physical hafnian control=PASS")
