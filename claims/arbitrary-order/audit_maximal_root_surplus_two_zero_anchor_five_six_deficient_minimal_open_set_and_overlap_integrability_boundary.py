"""Independent no-project-import audit for the reviewed GLS69 finite leaves."""

from collections import Counter
from itertools import permutations, product

COLOURS = (0, 1, 2)
STATUSES = (-1, 0, 1, 2)
FULL_COLOUR_MASK = 0b111


def type_options():
    # (kernel-support mask, rank, kind, coordinate readout)
    result = []
    for colour in COLOURS:
        result.append((1 << colour, 2, 0, -1))
    for colour in COLOURS:
        result.append((FULL_COLOUR_MASK ^ (1 << colour), 1, 1, colour))
    for colour in COLOURS:
        result.append((FULL_COLOUR_MASK ^ (1 << colour), 2, 2, -1))
    return tuple(result)


TYPES = type_options()


def member_masks(maps):
    return tuple(
        sum(
            1 << index
            for index, map_type in enumerate(maps)
            if map_type[0] & (1 << colour)
        )
        for colour in COLOURS
    )


def incidence_ok(maps, counts):
    number = len(maps)
    members = member_masks(maps)
    for colour, member_mask in enumerate(members):
        size = member_mask.bit_count()
        if size == number and counts[colour] < 3:
            return False
        if size != number - 1:
            continue
        if counts[colour] == 0:
            return False
        if counts[colour] == 1:
            missing = next(
                index for index in range(number) if not member_mask >> index & 1
            )
            _, _, kind, readout = maps[missing]
            if kind != 1 or readout != colour:
                return False
    return True


def pair_ok(maps, counts, pure_count):
    number = len(maps)
    members = member_masks(maps)
    visible = tuple(colour for colour in COLOURS if counts[colour] == 0)
    if any(members[colour].bit_count() > number - 2 for colour in visible):
        return False

    for contracted_mask in range(1 << number):
        if contracted_mask.bit_count() != number - 2:
            continue
        colours = tuple(
            colour for colour in visible if members[colour] == contracted_mask
        )
        rank = len(colours)
        if not rank:
            continue
        open_indices = tuple(
            index for index in range(number) if not contracted_mask >> index & 1
        )
        if any(maps[index][1] < rank for index in open_indices):
            return False
        if pure_count and rank > 1:
            return False
        if not pure_count and rank > 2:
            return False
        if rank == 1 and all(maps[index][1] == 2 for index in open_indices):
            return False
    return True


def canonical(maps, counts, pure_count):
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved = []
        for support, rank, kind, readout in maps:
            moved_support = sum(
                1 << colour_permutation[colour]
                for colour in COLOURS
                if support & (1 << colour)
            )
            moved_readout = -1 if readout < 0 else colour_permutation[readout]
            moved.append((moved_support, rank, kind, moved_readout))
        inverse = tuple(colour_permutation.index(colour) for colour in COLOURS)
        moved_counts = tuple(counts[index] for index in inverse)
        candidates.append((tuple(sorted(moved)), moved_counts, pure_count))
    return min(candidates)


def open_sets(maps, counts):
    number = len(maps)
    members = member_masks(maps)
    return tuple(
        frozenset(index for index in range(number) if not members[colour] >> index & 1)
        | (frozenset((number,)) if counts[colour] else frozenset())
        for colour in COLOURS
    )


def deficient_missing_sets(maps):
    number = len(maps)
    members = member_masks(maps)
    return tuple(
        frozenset(index for index in range(number) if not members[colour] >> index & 1)
        for colour in COLOURS
    )


def enumerate_branch(number, pure_count):
    nonaxis_count = 6 - number - pure_count
    stage = [0, 0, 0]
    profiles = []
    for maps in product(TYPES, repeat=number):
        for statuses in product(STATUSES, repeat=nonaxis_count):
            stage[0] += 1
            counts = tuple(statuses.count(colour) for colour in COLOURS)
            if not incidence_ok(maps, counts):
                continue
            stage[1] += 1
            if not pair_ok(maps, counts, pure_count):
                continue
            stage[2] += 1
            profiles.append((maps, counts, pure_count))
    return tuple(stage), profiles


five_p_stage, five_p = enumerate_branch(5, 1)
five_u_stage, five_u = enumerate_branch(5, 0)
six_pair_stage, six_pair = enumerate_branch(6, 0)

assert five_p_stage == (59_049, 18_270, 2_640)
assert five_u_stage == (236_196, 79_095, 24_435)
assert six_pair_stage == (531_441, 276_750, 99_855)


def triangle_span_ok(profile):
    maps, counts, pure_count = profile
    assert not any(counts) and pure_count == 0
    missing_masks = tuple(
        ((1 << 6) - 1) ^ member_mask for member_mask in member_masks(maps)
    )
    for triple_mask in range(1 << 6):
        if triple_mask.bit_count() != 3:
            continue
        target_colours = tuple(
            colour for colour in COLOURS if missing_masks[colour] & ~triple_mask == 0
        )
        if len(target_colours) > 2:
            return False
        for index, (_, _, kind, readout) in enumerate(maps):
            if not triple_mask >> index & 1 or kind != 1:
                continue
            if sum(colour != readout for colour in target_colours) > 1:
                return False
    return True


six = tuple(filter(triangle_span_ok, six_pair))
six_stage = (*six_pair_stage, len(six))
assert six_stage == (531_441, 276_750, 99_855, 99_180)
six_removed = tuple(profile for profile in six_pair if not triangle_span_ok(profile))
assert len(six_removed) == 675


def removed_family_rank_one_count(profile):
    maps, counts, pure_count = profile
    assert not any(counts) and pure_count == 0
    for colour in COLOURS:
        singleton_mask = 1 << colour
        complementary_mask = FULL_COLOUR_MASK ^ singleton_mask
        singleton_count = sum(
            support == singleton_mask and kind == 0 for support, _, kind, _ in maps
        )
        complementary = tuple(
            map_type
            for map_type in maps
            if map_type[0] == complementary_mask and map_type[2] in (1, 2)
        )
        if singleton_count == 2 and len(complementary) == 4:
            return sum(map_type[2] == 1 for map_type in complementary)
    return None


assert Counter(map(removed_family_rank_one_count, six_removed)) == Counter(
    {4: 45, 3: 180, 2: 270, 1: 180}
)

five_p_keys = Counter(canonical(*profile) for profile in five_p)
five_u_keys = Counter(canonical(*profile) for profile in five_u)
six_keys = Counter(canonical(*profile) for profile in six)
assert (len(five_p_keys), len(five_u_keys), len(six_keys)) == (12, 89, 86)
assert len({canonical(*profile) for profile in six_removed}) == 4

five_p_patterns = Counter(
    tuple(sorted(map(len, open_sets(maps, counts)))) for maps, counts, _ in five_p
)
assert five_p_patterns == Counter(
    {
        (2, 2, 2): 540,
        (2, 2, 3): 720,
        (2, 3, 3): 810,
        (2, 3, 4): 120,
        (3, 3, 3): 360,
        (3, 3, 4): 90,
    }
)

five_u_statuses = Counter(counts for _, counts, _ in five_u)
assert five_u_statuses == Counter(
    {
        (0, 0, 0): 2_880,
        (1, 0, 0): 7_185,
        (0, 1, 0): 7_185,
        (0, 0, 1): 7_185,
    }
)
five_u_deficient_patterns = Counter(
    tuple(sorted(map(len, deficient_missing_sets(maps)))) for maps, _, _ in five_u
)
assert five_u_deficient_patterns == Counter(
    {
        (1, 2, 2): 810,
        (1, 2, 3): 1_440,
        (1, 3, 3): 720,
        (1, 3, 4): 240,
        (1, 4, 4): 15,
        (2, 2, 2): 3_420,
        (2, 2, 3): 7_320,
        (2, 2, 4): 720,
        (2, 3, 3): 6_150,
        (2, 3, 4): 1_680,
        (2, 3, 5): 60,
        (2, 4, 4): 60,
        (3, 3, 3): 1_440,
        (3, 3, 4): 360,
    }
)


def minimum_size(profile):
    maps, counts, _ = profile
    return min(map(len, open_sets(maps, counts)))


five_p_min = Counter(map(minimum_size, five_p))
five_u_min = Counter(map(minimum_size, five_u))
six_pair_min = Counter(map(minimum_size, six_pair))
six_min = Counter(map(minimum_size, six))
assert five_p_min == Counter({2: 2_190, 3: 450})
assert five_u_min == Counter({2: 17_475, 3: 6_960})
assert six_pair_min == Counter({2: 65_385, 3: 34_380, 4: 90})
assert six_min == Counter({2: 64_710, 3: 34_380, 4: 90})

five_u_with_five_open = [
    profile
    for profile in five_u
    if max(map(len, open_sets(profile[0], profile[1]))) == 5
]
assert len(five_u_with_five_open) == 270
five_u_higher_with_five_open = [
    profile for profile in five_u_with_five_open if minimum_size(profile) >= 3
]
assert len(five_u_higher_with_five_open) == 150
assert len({canonical(*profile) for profile in five_u_higher_with_five_open}) == 2

assert (
    len({canonical(*profile) for profile in five_p if minimum_size(profile) == 3}) == 3
)
assert (
    len({canonical(*profile) for profile in five_u if minimum_size(profile) == 3}) == 30
)
six_minimum_key_counts = Counter()
for minimum in (2, 3, 4):
    six_minimum_key_counts[minimum] = len(
        {canonical(*profile) for profile in six if minimum_size(profile) == minimum}
    )
assert six_minimum_key_counts == Counter({2: 48, 3: 37, 4: 1})

six_patterns = Counter(
    tuple(sorted(map(len, open_sets(maps, counts)))) for maps, counts, _ in six
)
assert six_patterns == Counter(
    {
        (2, 2, 2): 2_430,
        (2, 2, 3): 15_840,
        (2, 2, 4): 4_365,
        (2, 3, 3): 23_760,
        (2, 3, 4): 15_120,
        (2, 3, 5): 1_440,
        (2, 4, 4): 1_575,
        (2, 4, 5): 180,
        (3, 3, 3): 14_880,
        (3, 3, 4): 14_400,
        (3, 3, 5): 1_800,
        (3, 3, 6): 60,
        (3, 4, 4): 2_880,
        (3, 4, 5): 360,
        (4, 4, 4): 90,
    }
)
six_pair_patterns = Counter(
    tuple(sorted(map(len, open_sets(maps, counts)))) for maps, counts, _ in six_pair
)
assert six_pair_patterns - six_patterns == Counter({(2, 2, 4): 675})


def triple_sizes(profile):
    maps, counts, _ = profile
    sets = open_sets(maps, counts)
    assert not any(counts)
    return tuple(
        sum(open_set.issubset(triple) for open_set in sets)
        for triple in (
            frozenset(index for index in range(6) if mask >> index & 1)
            for mask in range(1 << 6)
            if mask.bit_count() == 3
        )
    )


six_maximum = Counter(max(triple_sizes(profile)) for profile in six)
assert six_maximum == Counter({0: 90, 1: 95_685, 2: 3_405})
six_binary_multiplicity = Counter(
    sum(value == 2 for value in triple_sizes(profile))
    for profile in six
    if max(triple_sizes(profile)) == 2
)
assert six_binary_multiplicity == Counter({1: 3_360, 4: 45})
six_four_binary = tuple(
    profile
    for profile in six
    if sum(value == 2 for value in triple_sizes(profile)) == 4
)


def is_binary_pair_class_profile(profile):
    maps, counts, pure_count = profile
    assert not any(counts) and pure_count == 0
    for colour in COLOURS:
        singleton_mask = 1 << colour
        complementary_mask = FULL_COLOUR_MASK ^ singleton_mask
        singleton = sum(
            support == singleton_mask and kind == 0 for support, _, kind, _ in maps
        )
        complementary = sum(
            support == complementary_mask and kind == 2 for support, _, kind, _ in maps
        )
        if singleton == 2 and complementary == 4:
            return True
    return False


assert len(six_four_binary) == 45
assert all(map(is_binary_pair_class_profile, six_four_binary))
assert len({canonical(*profile) for profile in six_four_binary}) == 1
six_maximum_key_counts = Counter()
for maximum in (0, 1, 2):
    six_maximum_key_counts[maximum] = len(
        {
            canonical(*profile)
            for profile in six
            if max(triple_sizes(profile)) == maximum
        }
    )
assert six_maximum_key_counts == Counter({0: 1, 1: 76, 2: 9})
assert (
    len(
        {
            canonical(*profile)
            for profile in six
            if sum(value == 2 for value in triple_sizes(profile)) == 1
        }
    )
    == 8
)

# Independently check target survival against L_a subset T on every canonical
# key and every possible open-set mask.  A colour survives iff every contracted
# deficient mode sees it and no contracted nonaxis mode kills it.
for profiles in (five_p, five_u, six):
    representatives = {}
    for profile in profiles:
        representatives.setdefault(canonical(*profile), profile)
    for maps, counts, pure_count in representatives.values():
        number = len(maps)
        nonaxis_count = 6 - number - pure_count
        members = member_masks(maps)
        sets = open_sets(maps, counts)
        universe_size = number + nonaxis_count
        for open_mask in range(1 << universe_size):
            for colour in COLOURS:
                direct = all(
                    open_mask >> index & 1 or members[colour] >> index & 1
                    for index in range(number)
                ) and all(
                    open_mask >> (number + index) & 1 or counts[colour] == 0
                    for index in range(nonaxis_count)
                )
                subset = all(open_mask >> index & 1 for index in sets[colour])
                assert direct == subset

# Finite-field replay of the Q(omega) binary P3 control.  In F_7, omega=2.
prime = 7
omega = 2
inverse_six = pow(6, -1, prime)
rows = ((1, 1), (1, omega), (inverse_six, omega * omega * inverse_six % prime))
control = {}
for output in product(range(2), repeat=3):
    value = 0
    for source_order in permutations(range(3)):
        term = 1
        for mode in range(3):
            term = term * rows[source_order[mode]][output[mode]] % prime
        value = (value + term) % prime
    control[output] = value
assert control == {
    output: 1 if output in ((0, 0, 0), (1, 1, 1)) else 0
    for output in product(range(2), repeat=3)
}

print(f"independent_N5_stages: P={five_p_stage}, U={five_u_stage}")
print(f"independent_N5_keys: P={len(five_p_keys)}, U={len(five_u_keys)}")
print(f"independent_N5_minimum_sizes: P={five_p_min}, U={five_u_min}")
print(
    "independent_N5_U_five_open: "
    f"all={len(five_u_with_five_open)}, "
    f"minimum_at_least_three={len(five_u_higher_with_five_open)}"
)
print(f"independent_N6_stage: {six_stage}")
print(f"independent_N6_keys: {len(six_keys)}")
print(f"independent_N6_triangle_span_removed: profiles={len(six_removed)}, orbits=4")
print(f"independent_N6_minimum_sizes: {six_min}")
print(f"independent_N6_triple_targets: {six_maximum}")
print("F7_binary_P3_control: exact")
print(
    "PASS (GLS69 finite/displayed audit only; same-source "
    "integrability and global conjecture remain unresolved)"
)
