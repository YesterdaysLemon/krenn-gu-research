"""Independent no-project-import audit for the candidate GLS68 finite leaves."""

from collections import Counter
from itertools import permutations, product

COLOURS = (0, 1, 2)
ZERO_STATUSES = (-1, 0, 1, 2)
FULL_COLOUR_MASK = 0b111


def make_types():
    # Tuple fields are (support bit-mask, rank, kind, coordinate readout).
    # Kinds 0, 1, 2 are respectively S, R, T.
    result = []
    for colour in COLOURS:
        result.append((1 << colour, 2, 0, -1))
    for colour in COLOURS:
        result.append((FULL_COLOUR_MASK ^ (1 << colour), 1, 1, colour))
    for colour in COLOURS:
        result.append((FULL_COLOUR_MASK ^ (1 << colour), 2, 2, -1))
    return tuple(result)


TYPES = make_types()


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
    members = member_masks(maps)
    for colour, member_mask in enumerate(members):
        size = member_mask.bit_count()
        if size == 4 and counts[colour] < 3:
            return False
        if size != 3:
            continue
        if counts[colour] == 0:
            return False
        if counts[colour] == 1:
            missing = next(index for index in range(4) if not member_mask >> index & 1)
            _, _, kind, readout = maps[missing]
            if kind != 1 or readout != colour:
                return False
    return True


def pair_constraints_ok(maps, counts, pure_count):
    members = member_masks(maps)
    visible_colours = tuple(colour for colour in COLOURS if counts[colour] == 0)
    if any(members[colour].bit_count() > 2 for colour in visible_colours):
        return False

    for member_pair in range(1 << 4):
        if member_pair.bit_count() != 2:
            continue
        target_colours = tuple(
            colour for colour in visible_colours if members[colour] == member_pair
        )
        target_rank = len(target_colours)
        if not target_rank:
            continue
        open_indices = tuple(
            index for index in range(4) if not member_pair >> index & 1
        )
        if any(maps[index][1] < target_rank for index in open_indices):
            return False
        if pure_count > 0 and target_rank > 1:
            return False
        if pure_count == 0 and target_rank > 2:
            return False
        if target_rank == 1 and all(maps[index][1] == 2 for index in open_indices):
            return False
    return True


def canonical_key(maps, counts, pure_count):
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved_maps = []
        for support, rank, kind, readout in maps:
            moved_support = sum(
                1 << colour_permutation[colour]
                for colour in COLOURS
                if support & (1 << colour)
            )
            moved_readout = -1 if readout < 0 else colour_permutation[readout]
            moved_maps.append((moved_support, rank, kind, moved_readout))
        inverse = tuple(colour_permutation.index(colour) for colour in COLOURS)
        moved_counts = tuple(counts[index] for index in inverse)
        candidates.append((tuple(sorted(moved_maps)), moved_counts, pure_count))
    return min(candidates)


stage_by_pure = {}
survivors = []
for pure_count in range(3):
    nonaxis_count = 2 - pure_count
    stage = [0, 0, 0]
    for maps in product(TYPES, repeat=4):
        for statuses in product(ZERO_STATUSES, repeat=nonaxis_count):
            stage[0] += 1
            counts = tuple(statuses.count(colour) for colour in COLOURS)
            if not incidence_ok(maps, counts):
                continue
            stage[1] += 1
            if not pair_constraints_ok(maps, counts, pure_count):
                continue
            stage[2] += 1
            survivors.append((maps, counts, pure_count))
    stage_by_pure[pure_count] = tuple(stage)

assert stage_by_pure == {
    0: (104_976, 16_824, 4_530),
    1: (26_244, 3_252, 264),
    2: (6_561, 702, 0),
}
assert len(survivors) == 4_794

patterns = Counter((pure_count, counts) for _, counts, pure_count in survivors)
assert patterns == Counter(
    {
        (0, (0, 0, 0)): 54,
        (0, (0, 0, 1)): 224,
        (0, (0, 1, 0)): 224,
        (0, (1, 0, 0)): 224,
        (0, (0, 0, 2)): 364,
        (0, (0, 2, 0)): 364,
        (0, (2, 0, 0)): 364,
        (0, (0, 1, 1)): 904,
        (0, (1, 0, 1)): 904,
        (0, (1, 1, 0)): 904,
        (1, (0, 0, 1)): 88,
        (1, (0, 1, 0)): 88,
        (1, (1, 0, 0)): 88,
    }
)

all_keys = Counter(
    canonical_key(maps, counts, pure_count) for maps, counts, pure_count in survivors
)
assert len(all_keys) == 50
assert Counter(key[2] for key in all_keys) == {0: 45, 1: 5}

ternary = [
    profile for profile in survivors if profile[2] == 0 and profile[1] == (0, 0, 0)
]
assert len(ternary) == 54
ternary_keys = Counter(
    canonical_key(maps, counts, pure_count) for maps, counts, pure_count in ternary
)
assert sorted(ternary_keys.values()) == [18, 36]

nonternary = [profile for profile in survivors if profile not in ternary]
assert len(nonternary) == 4_740
nonternary_keys = Counter(
    canonical_key(maps, counts, pure_count) for maps, counts, pure_count in nonternary
)
assert len(nonternary_keys) == 48
assert Counter(profile[2] for profile in nonternary) == {0: 4_476, 1: 264}

# Independent bookkeeping of the root-variable interface.  A cross product
# has bidegree (1,1); a two-cross-contracted complementary deck is (2,2),
# and its product with a pair companion is (3,3), not root-multilinear.
cross_degree = (1, 1)
deck_degree = (cross_degree[0] * 2, cross_degree[1] * 2)
source_degree = (deck_degree[0] + 1, deck_degree[1] + 1)
assert source_degree == (3, 3)
assert source_degree != (1, 1)

# Sharp abstract ordered-pair/deck control.  Three independently chosen
# ordered terms produce the ternary four-fold diagonal, but they are not
# asserted to descend from one physical edge array.
control = Counter()
chosen_pairs = ((0, 1), (0, 2), (0, 3))
for colour, pair in enumerate(chosen_pairs):
    assert len(set(range(4)) - set(pair)) == 2
    control[(colour,) * 4] += 1
assert control == Counter({(colour,) * 4: 1 for colour in COLOURS})

print(f"independent_stage_by_pure: {stage_by_pure}")
print(f"independent_four_deficient_profiles: {len(survivors)}")
print(f"independent_four_deficient_orbits: {len(all_keys)}")
print(f"independent_ternary_four_port_profiles: {len(ternary)}")
print(f"independent_nonternary_profiles: {len(nonternary)}")
print(f"independent_probe_bidegree: {source_degree}")
print(
    "PASS (candidate GLS68 finite/interface audit only; all 4,794 profiles "
    "and the global conjecture remain unresolved)"
)
