"""Primary exact checks for the candidate GLS71 strict-parent theorem."""

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product

COLOURS = tuple(range(3))
LABELS = tuple(range(6))


@dataclass(frozen=True)
class DeficientType:
    support: frozenset[int]
    kind: str
    rank: int
    readout: int | None


def make_types() -> tuple[DeficientType, ...]:
    types = [DeficientType(frozenset((colour,)), "S", 2, None) for colour in COLOURS]
    for pair in combinations(COLOURS, 2):
        missing = next(colour for colour in COLOURS if colour not in pair)
        types.append(DeficientType(frozenset(pair), "R", 1, missing))
    for pair in combinations(COLOURS, 2):
        types.append(DeficientType(frozenset(pair), "T", 2, None))
    return tuple(types)


TYPES = make_types()


def memberships(profile: tuple[DeficientType, ...]):
    return tuple(
        frozenset(
            label
            for label, map_type in enumerate(profile)
            if colour in map_type.support
        )
        for colour in COLOURS
    )


def missing_sets(profile: tuple[DeficientType, ...]):
    members = memberships(profile)
    return tuple(frozenset(LABELS) - members[colour] for colour in COLOURS)


def gls63(profile: tuple[DeficientType, ...]) -> bool:
    return all(len(member_set) <= 4 for member_set in memberships(profile))


def gls67_pairs(profile: tuple[DeficientType, ...]) -> bool:
    missing = missing_sets(profile)
    for pair_tuple in combinations(LABELS, 2):
        pair = frozenset(pair_tuple)
        target_rank = sum(missing[colour] == pair for colour in COLOURS)
        if not target_rank:
            continue
        if target_rank > 2:
            return False
        if any(profile[label].rank < target_rank for label in pair):
            return False
        if target_rank == 1 and all(profile[label].rank == 2 for label in pair):
            return False
    return True


def triangle_span(profile: tuple[DeficientType, ...]) -> bool:
    missing = missing_sets(profile)
    for triple_tuple in combinations(LABELS, 3):
        triple = frozenset(triple_tuple)
        target = tuple(colour for colour in COLOURS if missing[colour].issubset(triple))
        if len(target) > 2:
            return False
        for label in triple:
            map_type = profile[label]
            if (
                map_type.kind == "R"
                and sum(colour != map_type.readout for colour in target) > 1
            ):
                return False
    return True


def canonical(profile: tuple[DeficientType, ...]):
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved = []
        for map_type in profile:
            support = tuple(
                sorted(colour_permutation[colour] for colour in map_type.support)
            )
            readout = (
                None
                if map_type.readout is None
                else colour_permutation[map_type.readout]
            )
            moved.append((map_type.kind, support, readout))
        candidates.append(tuple(sorted(moved)))
    return min(candidates)


def binary_triangles(profile: tuple[DeficientType, ...]):
    missing = missing_sets(profile)
    return tuple(
        triple
        for triple in map(frozenset, combinations(LABELS, 3))
        if sum(missing[colour].issubset(triple) for colour in COLOURS) == 2
    )


stages = [0, 0, 0, 0]
survivors: list[tuple[DeficientType, ...]] = []
for profile in product(TYPES, repeat=6):
    stages[0] += 1
    if not gls63(profile):
        continue
    stages[1] += 1
    if not gls67_pairs(profile):
        continue
    stages[2] += 1
    if not triangle_span(profile):
        continue
    stages[3] += 1
    survivors.append(profile)

assert tuple(stages) == (531_441, 276_750, 99_855, 99_180)
assert len({canonical(profile) for profile in survivors}) == 86


def is_sc2_tc4(profile: tuple[DeficientType, ...]) -> bool:
    for colour in COLOURS:
        singleton = sum(
            map_type.kind == "S" and map_type.support == frozenset((colour,))
            for map_type in profile
        )
        complementary_t = sum(
            map_type.kind == "T" and map_type.support == frozenset(COLOURS) - {colour}
            for map_type in profile
        )
        if singleton == 2 and complementary_t == 4:
            return True
    return False


gls70 = [profile for profile in survivors if not is_sc2_tc4(profile)]
assert len(gls70) == 99_135
assert len({canonical(profile) for profile in gls70}) == 85


def single_family(profile: tuple[DeficientType, ...]) -> tuple[str, int] | None:
    triangles = binary_triangles(profile)
    if len(triangles) != 1:
        return None
    triangle = triangles[0]
    missing = missing_sets(profile)
    target = tuple(colour for colour in COLOURS if missing[colour].issubset(triangle))
    sizes = sorted(len(missing[colour]) for colour in target)
    family = "A" if sizes == [2, 2] else "B"
    outside = frozenset(LABELS) - triangle
    number_t = sum(profile[label].kind == "T" for label in outside)
    return family, number_t


pre_family_counts = Counter(
    signature for profile in gls70 if (signature := single_family(profile))
)
assert pre_family_counts == Counter(
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


def excluded_by_gls71(profile: tuple[DeficientType, ...]) -> bool:
    signature = single_family(profile)
    return signature is not None and (
        (signature[0] == "B" and signature[1] <= 2) or signature == ("A", 0)
    )


gls71 = [profile for profile in gls70 if not excluded_by_gls71(profile)]
assert len(gls71) == 98_355
assert len({canonical(profile) for profile in gls71}) == 81

post_binary = Counter(
    signature for profile in gls71 if (signature := single_family(profile))
)
assert post_binary == Counter(
    {
        ("A", 1): 1_080,
        ("A", 2): 1_080,
        ("A", 3): 360,
        ("B", 3): 60,
    }
)
assert sum(post_binary.values()) == 2_580

# A decomposable binary tensor with corners 000 and 111 zero is supported on
# one of the six edges joining a weight-one vertex to a weight-two vertex.
cube = tuple(product((0, 1), repeat=3))
oriented_edges = tuple(
    (left, right)
    for left in cube
    for right in cube
    if sum(left) == 1
    and sum(right) == 2
    and sum(a != b for a, b in zip(left, right)) == 1
)
assert len(oriented_edges) == 6
assert len({tuple(sorted(edge)) for edge in oriented_edges}) == 6


def p3_coefficients(a, b):
    return {
        (0, 0, 1): a[0] + a[1],
        (0, 1, 0): a[0] + a[2],
        (1, 0, 0): a[1] + a[2],
        (1, 1, 0): b[0] + b[1],
        (1, 0, 1): b[0] + b[2],
        (0, 1, 1): b[1] + b[2],
    }


edge_r = Fraction(7)
edge_s = Fraction(11)
representative = p3_coefficients(
    (-edge_r / 2, edge_r / 2, edge_r / 2),
    (edge_s / 2, -edge_s / 2, edge_s / 2),
)
assert {word: value for word, value in representative.items() if value} == {
    (1, 0, 0): edge_r,
    (1, 0, 1): edge_s,
}

endpoint_r = p3_coefficients((-edge_r / 2, edge_r / 2, edge_r / 2), (0, 0, 0))
endpoint_s = p3_coefficients((0, 0, 0), (edge_s / 2, -edge_s / 2, edge_s / 2))
assert {word for word, value in endpoint_r.items() if value} == {(1, 0, 0)}
assert {word for word, value in endpoint_s.items() if value} == {(1, 0, 1)}

# Each single-colour alternative records the whole shores forced by the
# edge lemma and the selected opposite shore at an endpoint.  Every pairing
# for two independent colours conflicts on at least one shore/form.
alternatives = (
    (frozenset(("P", "Q")), frozenset()),
    (frozenset(("P",)), frozenset(("Q",))),
    (frozenset(("Q",)), frozenset(("P",))),
)
for first, second in product(alternatives, repeat=2):
    common_first, selected_first = first
    common_second, selected_second = second
    conflicting_shores = (
        common_first & common_second
        or common_first & selected_second
        or common_second & selected_first
    )
    assert conflicting_shores


def add_tensor(*tensors):
    result = defaultdict(Fraction)
    for tensor in tensors:
        for index, coefficient in tensor.items():
            result[index] += coefficient
    return {index: value for index, value in result.items() if value}


def scale_tensor(tensor, scalar):
    return {
        index: scalar * coefficient
        for index, coefficient in tensor.items()
        if scalar * coefficient
    }


def outer(*vectors):
    result = {}
    for indices in product(*(range(len(vector)) for vector in vectors)):
        coefficient = Fraction(1)
        for vector, index in zip(vectors, indices):
            coefficient *= vector[index]
        if coefficient:
            result[indices] = coefficient
    return result


# Exact all-kernel two-selector control from Theorem 6.2.  Local V_1,V_2
# target factors are represented by one-dimensional scalars; every K port
# uses basis x=(1,0), y=(0,1).
x = (Fraction(1), Fraction(0))
y = (Fraction(0), Fraction(1))
k = (x, x, y)
l = (y, y, x)
b45 = add_tensor(scale_tensor(outer(x, x), -1), scale_tensor(outer(y, y), -1))
b35 = add_tensor(scale_tensor(outer(x, x), -1), scale_tensor(outer(y, y), -1))
b34 = add_tensor(outer(x, y), outer(y, x))


def pair_zero(left_index, right_index, deck):
    return add_tensor(
        deck,
        outer(k[left_index], l[right_index]),
        outer(l[left_index], k[right_index]),
    )


assert pair_zero(1, 2, b45) == {}
assert pair_zero(0, 2, b35) == {}
assert pair_zero(0, 1, b34) == scale_tensor(b34, 2)


# Build the three attachment tensors in common slot order 3,4,5.
def spoke_times_deck(port, spoke, deck):
    result = {}
    other = tuple(index for index in range(3) if index != port)
    for local in range(2):
        for deck_indices, coefficient in deck.items():
            indices = [0, 0, 0]
            indices[port] = local
            indices[other[0]] = deck_indices[0]
            indices[other[1]] = deck_indices[1]
            value = spoke[local] * coefficient
            if value:
                result[tuple(indices)] = value
    return result


attachment_k = add_tensor(
    spoke_times_deck(0, k[0], b45),
    spoke_times_deck(1, k[1], b35),
    spoke_times_deck(2, k[2], b34),
)
attachment_l = add_tensor(
    spoke_times_deck(0, l[0], b45),
    spoke_times_deck(1, l[1], b35),
    spoke_times_deck(2, l[2], b34),
)
assert attachment_k == scale_tensor(outer(x, x, x), -2)
assert attachment_l == scale_tensor(outer(y, y, y), -2)


def vector_sum(*vectors):
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors))


def vector_scale(vector, scalar):
    return tuple(scalar * entry for entry in vector)


# Theorem 6.3's alpha != 0 projection formulas are polynomial identities.
# Replay them at independent rational coefficients; independence of the
# tensor words then forces those coefficients to vanish in the proof.
s_coefficient = Fraction(13)
q_coefficient = Fraction(17)
b_spokes = (
    vector_sum(vector_scale(x, s_coefficient), vector_scale(y, -q_coefficient)),
    vector_sum(vector_scale(x, s_coefficient), vector_scale(y, -q_coefficient)),
    vector_sum(vector_scale(y, s_coefficient), vector_scale(x, q_coefficient)),
)
assert (
    add_tensor(
        scale_tensor(b45, s_coefficient),
        outer(b_spokes[1], l[2]),
        outer(l[1], b_spokes[2]),
    )
    == {}
)
assert (
    add_tensor(
        scale_tensor(b35, s_coefficient),
        outer(b_spokes[0], l[2]),
        outer(l[0], b_spokes[2]),
    )
    == {}
)
b_attachment = add_tensor(
    spoke_times_deck(0, b_spokes[0], b45),
    spoke_times_deck(1, b_spokes[1], b35),
    spoke_times_deck(2, b_spokes[2], b34),
)
expected_b_attachment = add_tensor(
    scale_tensor(outer(x, x, x), -2 * s_coefficient),
    scale_tensor(outer(y, x, x), 2 * q_coefficient),
    scale_tensor(outer(x, y, x), 2 * q_coefficient),
    scale_tensor(outer(y, y, y), 2 * q_coefficient),
)
assert b_attachment == expected_b_attachment

r_coefficient = Fraction(19)
tau_coefficient = Fraction(23)
d_spokes = (
    vector_sum(vector_scale(y, r_coefficient), vector_scale(x, -tau_coefficient)),
    vector_sum(vector_scale(y, r_coefficient), vector_scale(x, -tau_coefficient)),
    vector_sum(vector_scale(x, r_coefficient), vector_scale(y, tau_coefficient)),
)
assert (
    add_tensor(
        scale_tensor(b45, r_coefficient),
        outer(k[1], d_spokes[2]),
        outer(d_spokes[1], k[2]),
    )
    == {}
)
assert (
    add_tensor(
        scale_tensor(b35, r_coefficient),
        outer(k[0], d_spokes[2]),
        outer(d_spokes[0], k[2]),
    )
    == {}
)
d_attachment = add_tensor(
    spoke_times_deck(0, d_spokes[0], b45),
    spoke_times_deck(1, d_spokes[1], b35),
    spoke_times_deck(2, d_spokes[2], b34),
)
expected_d_attachment = add_tensor(
    scale_tensor(outer(y, y, y), -2 * r_coefficient),
    scale_tensor(outer(x, x, x), 2 * tau_coefficient),
    scale_tensor(outer(x, y, y), 2 * tau_coefficient),
    scale_tensor(outer(y, x, y), 2 * tau_coefficient),
)
assert d_attachment == expected_d_attachment

# In the alpha=0 proportional branch, the isolated B34 term would equal a
# sum of the two target cubes.  This 2x2 flattening minor is nonzero.
rank_two_target = add_tensor(outer(x, x, x), outer(y, y, y))
assert (
    rank_two_target[(0, 0, 0)] * rank_two_target[(1, 1, 1)]
    - rank_two_target.get((0, 0, 1), 0) * rank_two_target.get((1, 1, 0), 0)
) != 0

selector_decks = {
    "a3": frozenset(("E45", "F45")),
    "a4": frozenset(("E35", "F35")),
    "b3": frozenset(("E45", "G45")),
    "b4": frozenset(("E35", "G35")),
}
assert selector_decks["a3"] | selector_decks["b4"] == frozenset(
    ("E45", "E35", "F45", "G35")
)
assert selector_decks["b3"] | selector_decks["a4"] == frozenset(
    ("E45", "E35", "G45", "F35")
)

# The YYZ part of sum_u Y_u E_(O-u) is symmetric in the two Y factors.
# Canonicalizing those two labels gives every monomial twice with exchanged
# order, so its alternating projection is zero.
yyz_terms = Counter()
for u in range(3):
    v, w = tuple(index for index in range(3) if index != u)
    yyz_terms[(tuple(sorted((u, v))), w)] += 1
    yyz_terms[(tuple(sorted((u, w))), v)] += 1
assert set(yyz_terms.values()) == {2}

print(f"stage={tuple(stages)}")
print(f"pre_GLS71_single_binary={dict(sorted(pre_family_counts.items()))}")
print("Family_B_r_le_2_removed=420 profiles / 3 keys")
print("Family_A_r_0_removed=360 profiles / 1 key")
print("post_GLS71_residual=98355 profiles / 81 keys")
print(f"post_GLS71_single_binary={dict(sorted(post_binary.items()))}")
print("pure_P3_oriented_edges=6; endpoints=PASS")
print("three-selector alternation=PASS; two-selector restricted control=PASS")
print("one-silent projection identities and selector pairing=PASS")
