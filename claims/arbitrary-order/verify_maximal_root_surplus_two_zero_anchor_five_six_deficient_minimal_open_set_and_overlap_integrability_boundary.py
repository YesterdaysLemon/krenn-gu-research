"""Primary finite checks for the reviewed GLS69 higher-deficient boundary."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
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


def make_types() -> tuple[DeficientType, ...]:
    result = [DeficientType(frozenset((c,)), S, 2, None) for c in COLOURS]
    for pair in combinations(COLOURS, 2):
        support = frozenset(pair)
        readout = next(c for c in COLOURS if c not in support)
        result.append(DeficientType(support, R, 1, readout))
    result.extend(
        DeficientType(frozenset(pair), T, 2, None) for pair in combinations(COLOURS, 2)
    )
    return tuple(result)


TYPES = make_types()


def memberships(
    maps: tuple[DeficientType, ...],
) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(i for i, map_type in enumerate(maps) if c in map_type.support)
        for c in COLOURS
    )


def zero_counts(statuses: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(statuses.count(c) for c in COLOURS)


def gls63_holds(maps: tuple[DeficientType, ...], counts: tuple[int, ...]) -> bool:
    size = len(maps)
    members = memberships(maps)
    for colour, member_set in enumerate(members):
        if len(member_set) == size and counts[colour] < 3:
            return False
        if len(member_set) != size - 1:
            continue
        if counts[colour] == 0:
            return False
        if counts[colour] == 1:
            missing = next(index for index in range(size) if index not in member_set)
            missing_map = maps[missing]
            if not (missing_map.kind == R and missing_map.readout == colour):
                return False
    return True


def gls67_pair_holds(
    maps: tuple[DeficientType, ...],
    counts: tuple[int, ...],
    pure_count: int,
) -> bool:
    size = len(maps)
    members = memberships(maps)
    unzeroed = tuple(c for c in COLOURS if counts[c] == 0)

    if any(len(members[c]) > size - 2 for c in unzeroed):
        return False

    for contracted in combinations(range(size), size - 2):
        contracted_set = frozenset(contracted)
        target_colours = tuple(c for c in unzeroed if members[c] == contracted_set)
        target_rank = len(target_colours)
        if not target_rank:
            continue
        open_indices = tuple(
            index for index in range(size) if index not in contracted_set
        )
        if any(maps[index].rank < target_rank for index in open_indices):
            return False
        if pure_count and target_rank > 1:
            return False
        if not pure_count and target_rank > 2:
            return False
        if target_rank == 1 and all(maps[index].rank == 2 for index in open_indices):
            return False
    return True


def canonical_profile(
    maps: tuple[DeficientType, ...],
    counts: tuple[int, ...],
    pure_count: int,
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


def missing_sets(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...]
) -> tuple[frozenset[int], ...]:
    size = len(maps)
    members = memberships(maps)
    # A possible single nonaxis label is represented by the extra index size.
    return tuple(
        frozenset(index for index in range(size) if index not in members[colour])
        | (frozenset((size,)) if counts[colour] else frozenset())
        for colour in COLOURS
    )


def deficient_missing_sets(
    maps: tuple[DeficientType, ...],
) -> tuple[frozenset[int], ...]:
    size = len(maps)
    members = memberships(maps)
    return tuple(
        frozenset(index for index in range(size) if index not in members[colour])
        for colour in COLOURS
    )


def enumerate_profiles(size: int, pure_count: int):
    nonaxis_count = 6 - size - pure_count
    assert nonaxis_count >= 0
    stage = [0, 0, 0]
    survivors = []
    for maps in product(TYPES, repeat=size):
        for statuses in product(ZERO_STATUSES, repeat=nonaxis_count):
            stage[0] += 1
            counts = zero_counts(statuses)
            if not gls63_holds(maps, counts):
                continue
            stage[1] += 1
            if not gls67_pair_holds(maps, counts, pure_count):
                continue
            stage[2] += 1
            survivors.append((maps, counts, pure_count))
    return tuple(stage), survivors


# Exactly five deficient labels: one remaining label is pure-axis or nonaxis.
n5_pure_stage, n5_pure = enumerate_profiles(5, 1)
n5_nonaxis_stage, n5_nonaxis = enumerate_profiles(5, 0)
assert n5_pure_stage == (59_049, 18_270, 2_640)
assert n5_nonaxis_stage == (236_196, 79_095, 24_435)

n5_pure_keys = Counter(
    canonical_profile(maps, counts, pure_count) for maps, counts, pure_count in n5_pure
)
n5_nonaxis_keys = Counter(
    canonical_profile(maps, counts, pure_count)
    for maps, counts, pure_count in n5_nonaxis
)
assert len(n5_pure_keys) == 12
assert len(n5_nonaxis_keys) == 89

n5_pure_missing_patterns = Counter(
    tuple(sorted(len(item) for item in missing_sets(maps, counts)))
    for maps, counts, _ in n5_pure
)
assert n5_pure_missing_patterns == Counter(
    {
        (2, 2, 2): 540,
        (3, 3, 3): 360,
        (2, 3, 3): 810,
        (2, 2, 3): 720,
        (3, 3, 4): 90,
        (2, 3, 4): 120,
    }
)

n5_nonaxis_status = Counter(counts for _, counts, _ in n5_nonaxis)
assert n5_nonaxis_status == Counter(
    {
        (0, 0, 0): 2_880,
        (1, 0, 0): 7_185,
        (0, 1, 0): 7_185,
        (0, 0, 1): 7_185,
    }
)

n5_nonaxis_deficient_missing_patterns = Counter(
    tuple(sorted(len(item) for item in deficient_missing_sets(maps)))
    for maps, _, _ in n5_nonaxis
)
assert n5_nonaxis_deficient_missing_patterns == Counter(
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


def minimum_open_size(profile) -> int:
    maps, counts, _ = profile
    return min(len(item) for item in missing_sets(maps, counts))


n5_pure_minimum = Counter(minimum_open_size(profile) for profile in n5_pure)
n5_nonaxis_minimum = Counter(minimum_open_size(profile) for profile in n5_nonaxis)
assert n5_pure_minimum[2] == 2_190
assert sum(count for size, count in n5_pure_minimum.items() if size >= 3) == 450
assert n5_nonaxis_minimum[2] == 17_475
assert sum(count for size, count in n5_nonaxis_minimum.items() if size >= 3) == 6_960
assert max(n5_pure_minimum) <= 4
assert max(n5_nonaxis_minimum) <= 4

n5_nonaxis_with_five_open = [
    profile
    for profile in n5_nonaxis
    if max(len(item) for item in missing_sets(profile[0], profile[1])) == 5
]
assert len(n5_nonaxis_with_five_open) == 270
n5_nonaxis_higher_with_five_open = [
    profile for profile in n5_nonaxis_with_five_open if minimum_open_size(profile) >= 3
]
assert len(n5_nonaxis_higher_with_five_open) == 150
assert (
    len({canonical_profile(*profile) for profile in n5_nonaxis_higher_with_five_open})
    == 2
)

n5_pure_higher_keys = {
    canonical_profile(*profile)
    for profile in n5_pure
    if minimum_open_size(profile) >= 3
}
n5_nonaxis_higher_keys = {
    canonical_profile(*profile)
    for profile in n5_nonaxis
    if minimum_open_size(profile) >= 3
}
assert len(n5_pure_higher_keys) == 3
assert len(n5_nonaxis_higher_keys) == 30


# Exactly six deficient labels: no injective label remains.  First retain the
# GLS63/GLS67 pair-level census, then impose the exact open-triple source-span
# predicate.  At a rank-one R_c mode, an open-triple source has local image in
# row(J_i) plus one companion row, so at most one target colour can differ
# from c.
def triangle_span_holds(profile) -> bool:
    maps, counts, _ = profile
    assert not any(counts)
    sets = missing_sets(maps, counts)
    for triple_tuple in combinations(range(6), 3):
        triple = frozenset(triple_tuple)
        target_colours = tuple(
            colour for colour in COLOURS if sets[colour].issubset(triple)
        )
        if len(target_colours) > 2:
            return False
        for index in triple:
            map_type = maps[index]
            if (
                map_type.kind == R
                and sum(colour != map_type.readout for colour in target_colours) > 1
            ):
                return False
    return True


n6_pair_stage, n6_pair_profiles = enumerate_profiles(6, 0)
assert n6_pair_stage == (531_441, 276_750, 99_855)
n6_profiles = tuple(filter(triangle_span_holds, n6_pair_profiles))
n6_stage = (*n6_pair_stage, len(n6_profiles))
assert n6_stage == (531_441, 276_750, 99_855, 99_180)
n6_triangle_span_removed = tuple(
    profile for profile in n6_pair_profiles if not triangle_span_holds(profile)
)
assert len(n6_triangle_span_removed) == 675


def removed_family_rank_one_count(profile) -> int | None:
    maps, counts, pure_count = profile
    assert not any(counts) and pure_count == 0
    for colour in COLOURS:
        singleton = [
            map_type
            for map_type in maps
            if map_type.kind == S and map_type.support == frozenset((colour,))
        ]
        complementary = [
            map_type
            for map_type in maps
            if map_type.support == frozenset(COLOURS) - {colour}
            and map_type.kind in (R, T)
        ]
        if len(singleton) == 2 and len(complementary) == 4:
            return sum(map_type.kind == R for map_type in complementary)
    return None


assert Counter(map(removed_family_rank_one_count, n6_triangle_span_removed)) == Counter(
    {4: 45, 3: 180, 2: 270, 1: 180}
)
n6_keys = Counter(
    canonical_profile(maps, counts, pure_count)
    for maps, counts, pure_count in n6_profiles
)
assert len(n6_keys) == 86
assert len({canonical_profile(*profile) for profile in n6_triangle_span_removed}) == 4

n6_missing_patterns = Counter(
    tuple(sorted(len(item) for item in missing_sets(maps, counts)))
    for maps, counts, _ in n6_profiles
)
assert n6_missing_patterns == Counter(
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
n6_pair_missing_patterns = Counter(
    tuple(sorted(len(item) for item in missing_sets(maps, counts)))
    for maps, counts, _ in n6_pair_profiles
)
assert n6_pair_missing_patterns - n6_missing_patterns == Counter({(2, 2, 4): 675})

n6_pair_minimum = Counter(minimum_open_size(profile) for profile in n6_pair_profiles)
assert n6_pair_minimum == Counter({2: 65_385, 3: 34_380, 4: 90})
n6_minimum = Counter(minimum_open_size(profile) for profile in n6_profiles)
assert n6_minimum == Counter({2: 64_710, 3: 34_380, 4: 90})
n6_minimum_key_counts = Counter()
for key in n6_keys:
    maps_key, counts, pure_count = key
    # Reconstruct only the invariant minimum size directly from the key.
    support_sets = tuple(map_key[0] for map_key in maps_key)
    minimum = min(
        sum(colour not in support for support in support_sets) + counts[colour]
        for colour in COLOURS
    )
    n6_minimum_key_counts[minimum] += 1
assert n6_minimum_key_counts == Counter({2: 48, 3: 37, 4: 1})


def triple_target_sizes(profile) -> tuple[int, ...]:
    maps, counts, _ = profile
    sets = missing_sets(maps, counts)
    assert not any(counts)
    return tuple(
        sum(sets[colour].issubset(triple) for colour in COLOURS)
        for triple in map(frozenset, combinations(range(6), 3))
    )


n6_max_triple = Counter(max(triple_target_sizes(profile)) for profile in n6_profiles)
assert n6_max_triple == Counter({0: 90, 1: 95_685, 2: 3_405})
n6_binary_triangle_multiplicity = Counter(
    sum(size == 2 for size in triple_target_sizes(profile))
    for profile in n6_profiles
    if max(triple_target_sizes(profile)) == 2
)
assert n6_binary_triangle_multiplicity == Counter({1: 3_360, 4: 45})
n6_four_binary_profiles = tuple(
    profile
    for profile in n6_profiles
    if sum(size == 2 for size in triple_target_sizes(profile)) == 4
)


def is_binary_pair_class_profile(profile) -> bool:
    maps, counts, pure_count = profile
    assert not any(counts) and pure_count == 0
    for colour in COLOURS:
        singleton = sum(
            map_type.kind == S and map_type.support == frozenset((colour,))
            for map_type in maps
        )
        complementary = sum(
            map_type.kind == T and map_type.support == frozenset(COLOURS) - {colour}
            for map_type in maps
        )
        if singleton == 2 and complementary == 4:
            return True
    return False


assert len(n6_four_binary_profiles) == 45
assert all(map(is_binary_pair_class_profile, n6_four_binary_profiles))
assert len({canonical_profile(*profile) for profile in n6_four_binary_profiles}) == 1

n6_max_key_counts = Counter()
for key in n6_keys:
    maps_key, counts, _ = key
    support_sets = tuple(map_key[0] for map_key in maps_key)
    sets = tuple(
        frozenset(
            index for index, support in enumerate(support_sets) if colour not in support
        )
        for colour in COLOURS
    )
    max_target = max(
        sum(sets[colour].issubset(triple) for colour in COLOURS)
        for triple in map(frozenset, combinations(range(6), 3))
    )
    n6_max_key_counts[max_target] += 1
assert n6_max_key_counts == Counter({0: 1, 1: 76, 2: 9})
assert (
    len(
        {
            canonical_profile(*profile)
            for profile in n6_profiles
            if sum(size == 2 for size in triple_target_sizes(profile)) == 1
        }
    )
    == 8
)

# Exact local binary P3 control over Q(omega), omega^2+omega+1=0.
Quadratic = tuple[Fraction, Fraction]


def qadd(left: Quadratic, right: Quadratic) -> Quadratic:
    return left[0] + right[0], left[1] + right[1]


def qmul(left: Quadratic, right: Quadratic) -> Quadratic:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
OMEGA = (Fraction(0), Fraction(1))
OMEGA_SQUARED = qmul(OMEGA, OMEGA)
assert OMEGA_SQUARED == (Fraction(-1), Fraction(-1))

sixth = Fraction(1, 6)
p_row = (ONE, ONE)
q_row = (ONE, OMEGA)
h_row = (
    (sixth, Fraction(0)),
    (sixth * OMEGA_SQUARED[0], sixth * OMEGA_SQUARED[1]),
)

binary_p3 = {}
for output in product(range(2), repeat=3):
    value = ZERO
    for source_order in permutations(range(3)):
        rows = (p_row, q_row, h_row)
        term = ONE
        for mode in range(3):
            term = qmul(term, rows[source_order[mode]][output[mode]])
        value = qadd(value, term)
    binary_p3[output] = value
assert binary_p3 == {
    output: ONE if output in ((0, 0, 0), (1, 1, 1)) else ZERO
    for output in product(range(2), repeat=3)
}

print(f"N5_pure_stage: {n5_pure_stage}")
print(f"N5_nonaxis_stage: {n5_nonaxis_stage}")
print(f"N5_orbits: pure={len(n5_pure_keys)}, nonaxis={len(n5_nonaxis_keys)}")
print(f"N5_minimum_open_sizes: pure={n5_pure_minimum}, nonaxis={n5_nonaxis_minimum}")
print(
    "N5_nonaxis_five_open: "
    f"all={len(n5_nonaxis_with_five_open)}, "
    f"minimum_at_least_three={len(n5_nonaxis_higher_with_five_open)}"
)
print(f"N6_stage: {n6_stage}")
print(f"N6_orbits: {len(n6_keys)}")
print(f"N6_triangle_span_removed: profiles={len(n6_triangle_span_removed)}, orbits=4")
print(f"N6_minimum_open_sizes: {n6_minimum}")
print(f"N6_max_triple_targets: {n6_max_triple}")
print("Q(omega)_binary_P3_control: exact")
print(
    "PASS: GLS69 finite/minimal-open checks only "
    "(same-source integrability and global conjecture remain unresolved)"
)
