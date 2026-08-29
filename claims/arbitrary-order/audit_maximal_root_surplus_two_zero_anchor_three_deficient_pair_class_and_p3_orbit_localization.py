"""Independent standard-library audit for the reviewed GLS67 finite leaves."""

from collections import Counter
from itertools import combinations, permutations, product

COLOURS = (0, 1, 2)
STATUSES = (-1, 0, 1, 2)


def options():
    result = []
    for colour in COLOURS:
        result.append((1 << colour, 2, -1, "D"))
    for pair in combinations(COLOURS, 2):
        mask = sum(1 << colour for colour in pair)
        readout = next(colour for colour in COLOURS if not mask & (1 << colour))
        result.append((mask, 1, readout, "L"))
    for pair in combinations(COLOURS, 2):
        result.append((sum(1 << colour for colour in pair), 2, -1, "B"))
    return tuple(result)


TYPES = options()


def support_members(maps, colour):
    return tuple(
        index for index, map_type in enumerate(maps) if map_type[0] & (1 << colour)
    )


def survives(maps, assignment, pure_count):
    counts = tuple(assignment.count(colour) for colour in COLOURS)
    members = tuple(support_members(maps, colour) for colour in COLOURS)
    for colour, member_tuple in enumerate(members):
        if len(member_tuple) == 3 and counts[colour] < 3:
            return 0
        if len(member_tuple) == 2:
            if counts[colour] == 0:
                return 0
            if counts[colour] == 1:
                missing = next(index for index in range(3) if index not in member_tuple)
                if not (maps[missing][3] == "L" and maps[missing][2] == colour):
                    return 0

    unzeroed = tuple(colour for colour in COLOURS if counts[colour] == 0)
    if any(len(members[colour]) > 1 for colour in unzeroed):
        return 1
    for singleton in {
        members[colour] for colour in unzeroed if len(members[colour]) == 1
    }:
        colours = tuple(colour for colour in unzeroed if members[colour] == singleton)
        open_indices = tuple(index for index in range(3) if index not in singleton)
        rank = len(colours)
        if any(maps[index][1] < rank for index in open_indices):
            return 1
        if pure_count and rank > 1:
            return 1
        if not pure_count and rank > 2:
            return 1
        if rank == 1 and all(maps[index][1] == 2 for index in open_indices):
            return 1

    if pure_count:
        raise AssertionError("pair-class survivors must have no pure-axis port")
    for map_type in maps:
        if map_type[3] != "L":
            continue
        if sum(colour != map_type[2] for colour in unzeroed) > 1:
            return 2
    return 3


stage_counts = [0, 0, 0, 0, 0]
final_count_patterns = Counter()
residual_profiles = []
for maps in product(TYPES, repeat=3):
    for pure_count in range(4):
        for assignment in product(STATUSES, repeat=3 - pure_count):
            stage_counts[0] += 1
            stage = survives(maps, assignment, pure_count)
            for index in range(1, stage + 1):
                stage_counts[index] += 1
            if stage == 3:
                final_count_patterns[
                    tuple(assignment.count(colour) for colour in COLOURS)
                ] += 1
                if maps[0][0] & maps[1][0] & maps[2][0] == 0:
                    stage_counts[4] += 1
                    residual_profiles.append(
                        (
                            maps,
                            tuple(assignment.count(colour) for colour in COLOURS),
                        )
                    )

assert stage_counts == [61_965, 2_367, 516, 453, 432]
assert sum(final_count_patterns.values()) == 453


def canonical(maps, counts):
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved_maps = []
        for mask, rank, readout, kind in maps:
            moved_mask = sum(
                1 << colour_permutation[colour]
                for colour in COLOURS
                if mask & (1 << colour)
            )
            moved_readout = -1 if readout < 0 else colour_permutation[readout]
            moved_maps.append((moved_mask, rank, moved_readout, kind))
        inverse = tuple(colour_permutation.index(colour) for colour in COLOURS)
        moved_counts = tuple(counts[index] for index in inverse)
        candidates.append((tuple(sorted(moved_maps)), moved_counts))
    return min(candidates)


residual_orbits = Counter(canonical(maps, counts) for maps, counts in residual_profiles)
assert len(residual_orbits) == 8


def p3_tensor(bases, prime):
    tensor = {}
    for output in product(range(2), repeat=3):
        value = 0
        for source in permutations(range(3)):
            term = 1
            for mode in range(3):
                term *= bases[mode][output[mode]][source[mode]]
            value += term
        tensor[output] = value % prime
    return tensor


def hyperdet(tensor, prime):
    a = tensor
    value = (
        a[0, 0, 0] ** 2 * a[1, 1, 1] ** 2
        + a[0, 0, 1] ** 2 * a[1, 1, 0] ** 2
        + a[0, 1, 0] ** 2 * a[1, 0, 1] ** 2
        + a[1, 0, 0] ** 2 * a[0, 1, 1] ** 2
        - 2
        * (
            a[0, 0, 0] * a[0, 0, 1] * a[1, 1, 0] * a[1, 1, 1]
            + a[0, 0, 0] * a[0, 1, 0] * a[1, 0, 1] * a[1, 1, 1]
            + a[0, 0, 0] * a[1, 0, 0] * a[0, 1, 1] * a[1, 1, 1]
            + a[0, 0, 1] * a[0, 1, 0] * a[1, 0, 1] * a[1, 1, 0]
            + a[0, 0, 1] * a[1, 0, 0] * a[0, 1, 1] * a[1, 1, 0]
            + a[0, 1, 0] * a[1, 0, 0] * a[0, 1, 1] * a[1, 0, 1]
        )
        + 4
        * (
            a[0, 0, 0] * a[0, 1, 1] * a[1, 0, 1] * a[1, 1, 0]
            + a[1, 1, 1] * a[1, 0, 0] * a[0, 1, 0] * a[0, 0, 1]
        )
    )
    return value % prime


prime = 101
binary_basis = ((-1, 1, 0), (-1, 0, 1))
binary = p3_tensor((binary_basis,) * 3, prime)
assert hyperdet(binary, prime) == -48 % prime

pure_bases = (
    ((-1, 1, 0), (-1, 0, 1)),
    ((1, 1, 0), (1, 0, 1)),
    ((1, 1, 0), (-1, 0, 1)),
)
pure = p3_tensor(pure_bases, prime)
assert sum(value != 0 for value in pure.values()) == 2

zero_basis = ((1, 0, 0), (0, 1, 0))
zero = p3_tensor((zero_basis,) * 3, prime)
assert not any(zero.values())

print(f"independent_stage_counts: {stage_counts}")
print(f"independent_final_profiles: {sum(final_count_patterns.values())}")
print(f"independent_residual_orbits: {len(residual_orbits)}")
print(f"F101_binary_hyperdeterminant: {hyperdet(binary, prime)}")
print("F101_pure_support_size: 2")
print("F101_zero_support_size: 0")
print(
    "PASS (GLS67 independent finite/displayed audit only; "
    "eight residual orbits and global conjecture remain unresolved)"
)
