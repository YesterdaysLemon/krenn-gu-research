"""Primary exact checks for the reviewed GLS68 four-deficient boundary."""

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, permutations, product

COLOURS = tuple(range(3))
ZERO_STATUSES = (-1, *COLOURS)


@dataclass(frozen=True)
class DeficientType:
    support: frozenset[int]
    kind: str
    rank: int
    readout: int | None


S = "S"
R = "R"
T = "T"


def deficient_types() -> tuple[DeficientType, ...]:
    result = [DeficientType(frozenset((c,)), S, 2, None) for c in COLOURS]
    for pair in combinations(COLOURS, 2):
        support = frozenset(pair)
        readout = next(c for c in COLOURS if c not in support)
        result.append(DeficientType(support, R, 1, readout))
    result.extend(
        DeficientType(frozenset(pair), T, 2, None) for pair in combinations(COLOURS, 2)
    )
    return tuple(result)


TYPES = deficient_types()


def memberships(maps: tuple[DeficientType, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(i for i, map_type in enumerate(maps) if c in map_type.support)
        for c in COLOURS
    )


def zero_counts(assignment: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(assignment.count(c) for c in COLOURS)


def gls63_holds(maps: tuple[DeficientType, ...], counts: tuple[int, ...]) -> bool:
    members = memberships(maps)
    for colour, member_set in enumerate(members):
        if len(member_set) == 4 and counts[colour] < 3:
            return False
        if len(member_set) != 3:
            continue
        if counts[colour] == 0:
            return False
        if counts[colour] == 1:
            missing = next(i for i in range(4) if i not in member_set)
            missing_map = maps[missing]
            if not (missing_map.kind == R and missing_map.readout == colour):
                return False
    return True


def pair_class_holds(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...], pure_count: int
) -> bool:
    members = memberships(maps)
    unzeroed = tuple(c for c in COLOURS if counts[c] == 0)

    # If a two-label contraction set is contained in an unzeroed support,
    # GLS67 forces the whole support to equal that pair.
    if any(len(members[c]) > 2 for c in unzeroed):
        return False

    for contracted_pair in combinations(range(4), 2):
        contracted = frozenset(contracted_pair)
        colours = tuple(c for c in unzeroed if members[c] == contracted)
        target_rank = len(colours)
        if not target_rank:
            continue
        open_indices = tuple(i for i in range(4) if i not in contracted)
        if any(maps[i].rank < target_rank for i in open_indices):
            return False
        if pure_count and target_rank > 1:
            return False
        if not pure_count and target_rank > 2:
            return False
        if target_rank == 1 and all(maps[i].rank == 2 for i in open_indices):
            return False
    return True


def canonical_profile(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...], pure_count: int
) -> tuple:
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved_maps = []
        for map_type in maps:
            support = tuple(sorted(colour_permutation[c] for c in map_type.support))
            readout = (
                None
                if map_type.readout is None
                else colour_permutation[map_type.readout]
            )
            moved_maps.append((support, map_type.kind, readout))
        inverse = tuple(colour_permutation.index(c) for c in COLOURS)
        moved_counts = tuple(counts[index] for index in inverse)
        candidates.append((tuple(sorted(moved_maps)), moved_counts, pure_count))
    return min(candidates)


stage_by_pure = {}
pair_profiles = []
for pure_count in range(3):
    nonaxis_count = 2 - pure_count
    stage = [0, 0, 0]
    for maps in product(TYPES, repeat=4):
        for assignment in product(ZERO_STATUSES, repeat=nonaxis_count):
            stage[0] += 1
            counts = zero_counts(assignment)
            if not gls63_holds(maps, counts):
                continue
            stage[1] += 1
            if not pair_class_holds(maps, counts, pure_count):
                continue
            stage[2] += 1
            pair_profiles.append((maps, counts, pure_count))
    stage_by_pure[pure_count] = tuple(stage)

assert stage_by_pure == {
    0: (104_976, 16_824, 4_530),
    1: (26_244, 3_252, 264),
    2: (6_561, 702, 0),
}
assert len(pair_profiles) == 4_794

pattern_counts = Counter(
    (pure_count, counts) for _, counts, pure_count in pair_profiles
)
assert pattern_counts[0, (0, 0, 0)] == 54
for pattern in permutations((0, 0, 1)):
    assert pattern_counts[0, pattern] == 224
    assert pattern_counts[1, pattern] == 88
for pattern in permutations((0, 0, 2)):
    assert pattern_counts[0, pattern] == 364
for pattern in permutations((0, 1, 1)):
    assert pattern_counts[0, pattern] == 904
# Ten patterns occur for p=0 and three additional p=1 patterns occur under
# the same zero-count triples.  The pure-count coordinate is part of the key.
assert len(pattern_counts) == 13

localized_orbits = Counter(
    canonical_profile(maps, counts, pure_count)
    for maps, counts, pure_count in pair_profiles
)
assert len(localized_orbits) == 50

ternary_profiles = [
    profile for profile in pair_profiles if profile[2] == 0 and profile[1] == (0, 0, 0)
]
assert len(ternary_profiles) == 54
ternary_orbits = Counter(
    canonical_profile(maps, counts, pure_count)
    for maps, counts, pure_count in ternary_profiles
)
assert sorted(ternary_orbits.values()) == [18, 36]


def type_word(maps: tuple[DeficientType, ...]) -> tuple[tuple[str, int], ...]:
    word = []
    for map_type in maps:
        if map_type.kind == S:
            colour = next(iter(map_type.support))
        elif map_type.kind == R:
            assert map_type.readout is not None
            colour = map_type.readout
        else:
            # T_c has support equal to the two colours complementary to c.
            colour = next(c for c in COLOURS if c not in map_type.support)
        word.append((map_type.kind, colour))
    return tuple(sorted(word))


assert {type_word(maps) for maps, _, _ in ternary_profiles} == {
    ((R, 0), (R, 0), (S, 0), (S, 0)),
    ((R, 0), (S, 0), (S, 0), (T, 0)),
    ((R, 1), (R, 1), (S, 1), (S, 1)),
    ((R, 1), (S, 1), (S, 1), (T, 1)),
    ((R, 2), (R, 2), (S, 2), (S, 2)),
    ((R, 2), (S, 2), (S, 2), (T, 2)),
}

nonternary_profiles = [
    profile for profile in pair_profiles if profile not in ternary_profiles
]
assert len(nonternary_profiles) == 4_740
assert Counter(profile[2] for profile in nonternary_profiles) == {0: 4_476, 1: 264}
nonternary_orbits = Counter(
    canonical_profile(maps, counts, pure_count)
    for maps, counts, pure_count in nonternary_profiles
)
assert len(nonternary_orbits) == 48

# Cross-contracting the two nonaxis labels produces probe-dependent two-port
# decks.  Each cross product has probe bidegree (1,1), so each complementary
# deck has bidegree (2,2); multiplying by the pair companion gives (3,3).
# An honest six-vertex matching tensor is multilinear in the two root modes,
# hence has probe bidegree (1,1).  This degree check records the receiver-
# interface obstruction; it is not an exclusion of the ternary stratum.
cross_bidegree = (1, 1)
deck_bidegree = tuple(2 * degree for degree in cross_bidegree)
companion_bidegree = (1, 1)
four_port_source_bidegree = tuple(
    left + right for left, right in zip(companion_bidegree, deck_bidegree)
)
honest_six_vertex_root_bidegree = (1, 1)
assert deck_bidegree == (2, 2)
assert four_port_source_bidegree == (3, 3)
assert four_port_source_bidegree != honest_six_vertex_root_bidegree

# The abstract ordered pair/deck equation itself admits a ternary diagonal:
# use one ordered pair term for each colour.  These independently selected
# terms are only a sharp equation-level control, not a same-graph witness.
control_tensor = Counter()
for colour, open_pair in enumerate(((0, 1), (0, 2), (0, 3))):
    complement = tuple(index for index in range(4) if index not in open_pair)
    assert len(complement) == 2
    control_tensor[(colour,) * 4] += 1
assert control_tensor == Counter({(colour,) * 4: 1 for colour in COLOURS})

print(f"normalized_start_total: {sum(stage[0] for stage in stage_by_pure.values())}")
print(f"after_GLS63_incidence: {sum(stage[1] for stage in stage_by_pure.values())}")
print(f"after_GLS67_pair_classes: {len(pair_profiles)}")
print(f"localized_four_deficient_orbits: {len(localized_orbits)}")
print(f"ternary_probe_dependent_four_port_profiles: {len(ternary_profiles)}")
print(f"nonternary_four_deficient_profiles: {len(nonternary_profiles)}")
print(f"nonternary_four_deficient_orbits: {len(nonternary_orbits)}")
print(f"probe_bidegree: {four_port_source_bidegree}")
print(
    "PASS: GLS68 normalized finite localization "
    "and receiver-interface boundary "
    "(audit only; all 4,794 profiles and global conjecture remain unresolved)"
)
