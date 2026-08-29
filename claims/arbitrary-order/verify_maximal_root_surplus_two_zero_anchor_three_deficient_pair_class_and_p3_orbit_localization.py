"""Primary exact checks for the candidate GLS67 parent localization."""

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
ZERO_STATUSES = (-1, *COLOURS)


@dataclass(frozen=True)
class DeficientType:
    support: frozenset[int]
    kind: str
    rank: int
    readout: int | None


R2S1 = "r2s1"
R1S2 = "r1s2"
R2S2 = "r2s2"


def deficient_types() -> tuple[DeficientType, ...]:
    options = [DeficientType(frozenset((colour,)), R2S1, 2, None) for colour in COLOURS]
    for pair in combinations(COLOURS, 2):
        support = frozenset(pair)
        readout = next(colour for colour in COLOURS if colour not in support)
        options.append(DeficientType(support, R1S2, 1, readout))
    options.extend(
        DeficientType(frozenset(pair), R2S2, 2, None)
        for pair in combinations(COLOURS, 2)
    )
    return tuple(options)


TYPES = deficient_types()


def zero_counts(assignment: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(assignment.count(colour) for colour in COLOURS)


def memberships(maps: tuple[DeficientType, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(
            index for index, map_type in enumerate(maps) if colour in map_type.support
        )
        for colour in COLOURS
    )


def gls63_incidence_holds(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...]
) -> bool:
    member_sets = memberships(maps)
    for colour, member_set in enumerate(member_sets):
        if len(member_set) == 3 and counts[colour] < 3:
            return False
        if len(member_set) != 2:
            continue
        if counts[colour] == 0:
            return False
        if counts[colour] == 1:
            missing = next(index for index in range(3) if index not in member_set)
            missing_map = maps[missing]
            if not (missing_map.kind == R1S2 and missing_map.readout == colour):
                return False
    return True


def pair_class_holds(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...], pure_count: int
) -> bool:
    member_sets = memberships(maps)
    unzeroed = tuple(colour for colour in COLOURS if counts[colour] == 0)
    if any(len(member_sets[colour]) > 1 for colour in unzeroed):
        return False

    singleton_classes = {
        member_sets[colour] for colour in unzeroed if len(member_sets[colour]) == 1
    }
    for member_set in singleton_classes:
        target_colours = tuple(
            colour for colour in unzeroed if member_sets[colour] == member_set
        )
        open_maps = tuple(maps[index] for index in range(3) if index not in member_set)
        target_rank = len(target_colours)
        if any(map_type.rank < target_rank for map_type in open_maps):
            return False
        if pure_count and target_rank > 1:
            return False
        if not pure_count and target_rank > 2:
            return False
        if target_rank == 1 and all(map_type.rank == 2 for map_type in open_maps):
            return False
    return True


def full_p3_target_span_holds(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...]
) -> bool:
    target_colours = tuple(colour for colour in COLOURS if counts[colour] == 0)
    for map_type in maps:
        if map_type.kind != R1S2:
            continue
        transverse_target_count = sum(
            colour != map_type.readout for colour in target_colours
        )
        if transverse_target_count > 1:
            return False
    return True


def canonical_profile(
    maps: tuple[DeficientType, ...], counts: tuple[int, ...]
) -> tuple[tuple[tuple[tuple[int, ...], str, int | None], ...], tuple[int, ...]]:
    candidates = []
    for colour_permutation in permutations(COLOURS):
        transformed_maps = []
        for map_type in maps:
            support = tuple(
                sorted(colour_permutation[colour] for colour in map_type.support)
            )
            readout = (
                None
                if map_type.readout is None
                else colour_permutation[map_type.readout]
            )
            transformed_maps.append((support, map_type.kind, readout))
        inverse = tuple(colour_permutation.index(colour) for colour in COLOURS)
        transformed_counts = tuple(counts[index] for index in inverse)
        candidates.append((tuple(sorted(transformed_maps)), transformed_counts))
    return min(candidates)


base_count = 0
incidence_count = 0
pair_count = 0
final_profiles = []
for maps in product(TYPES, repeat=3):
    for pure_count in range(4):
        nonaxis_count = 3 - pure_count
        for assignment in product(ZERO_STATUSES, repeat=nonaxis_count):
            base_count += 1
            counts = zero_counts(assignment)
            if not gls63_incidence_holds(maps, counts):
                continue
            incidence_count += 1
            if not pair_class_holds(maps, counts, pure_count):
                continue
            pair_count += 1
            assert pure_count == 0
            if full_p3_target_span_holds(maps, counts):
                final_profiles.append((maps, counts))

assert base_count == 61_965
assert incidence_count == 2_367
assert pair_count == 516
assert len(final_profiles) == 453

localized_orbit_counts = Counter(
    canonical_profile(maps, counts) for maps, counts in final_profiles
)
expected_orbit_counts = {
    ((((0,), R2S1, None), ((0,), R2S1, None), ((0,), R2S1, None)), (3, 0, 0)): 3,
    ((((0,), R2S1, None), ((0,), R2S1, None), ((1,), R2S1, None)), (2, 1, 0)): 54,
    ((((0,), R2S1, None), ((0,), R2S1, None), ((1, 2), R1S2, 0)), (1, 1, 1)): 54,
    ((((0,), R2S1, None), ((0,), R2S1, None), ((1, 2), R2S2, None)), (2, 0, 0)): 27,
    ((((0,), R2S1, None), ((0,), R2S1, None), ((1, 2), R2S2, None)), (3, 0, 0)): 9,
    ((((0,), R2S1, None), ((0, 1), R1S2, 2), ((0, 2), R1S2, 1)), (3, 0, 0)): 18,
    ((((0,), R2S1, None), ((0, 1), R1S2, 2), ((1, 2), R1S2, 0)), (1, 2, 0)): 108,
    ((((0,), R2S1, None), ((0, 1), R1S2, 2), ((2,), R2S1, None)), (2, 1, 0)): 108,
    ((((0,), R2S1, None), ((1,), R2S1, None), ((2,), R2S1, None)), (1, 1, 1)): 36,
    ((((0, 1), R1S2, 2), ((0, 2), R1S2, 1), ((1, 2), R1S2, 0)), (1, 1, 1)): 36,
}
assert localized_orbit_counts == expected_orbit_counts

residual_profiles = [
    (maps, counts)
    for maps, counts in final_profiles
    if not set.intersection(*(set(map_type.support) for map_type in maps))
]
assert len(residual_profiles) == 432
residual_orbit_counts = Counter(
    canonical_profile(maps, counts) for maps, counts in residual_profiles
)
common_support_orbits = {
    profile: multiplicity
    for profile, multiplicity in localized_orbit_counts.items()
    if profile not in residual_orbit_counts
}
assert sorted(common_support_orbits.values()) == [3, 18]
assert len(residual_orbit_counts) == 8


# The three pair companions and complementary one-port rows are exactly P_3.
source_terms: Counter[tuple[str, ...]] = Counter()
for i, j in combinations(range(3), 2):
    k = next(index for index in range(3) if index not in (i, j))
    first = [""] * 3
    first[i], first[j], first[k] = "P", "Q", "H"
    second = [""] * 3
    second[i], second[j], second[k] = "Q", "P", "H"
    source_terms[tuple(first)] += 1
    source_terms[tuple(second)] += 1
permanent_terms = Counter(permutation for permutation in permutations(("P", "Q", "H")))
assert source_terms == permanent_terms


def p3_restriction(
    bases: tuple[tuple[tuple[int, ...], ...], ...],
) -> dict[tuple[int, int, int], sp.Expr]:
    tensor = {}
    for output in product(range(2), repeat=3):
        value = 0
        for source_permutation in permutations(range(3)):
            term = 1
            for mode in range(3):
                term *= bases[mode][output[mode]][source_permutation[mode]]
            value += term
        tensor[output] = sp.expand(value)
    return tensor


def hyperdeterminant(tensor: dict[tuple[int, int, int], sp.Expr]) -> sp.Expr:
    a = tensor
    return sp.expand(
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


# Sharp binary-GHZ P_3 control: common full-support quotient beta=(1,1,1).
binary_basis = ((-1, 1, 0), (-1, 0, 1))
binary_tensor = p3_restriction((binary_basis, binary_basis, binary_basis))
assert hyperdeterminant(binary_tensor) == -48

# Sharp pure P_3 sign chart.
pure_bases = (
    ((-1, 1, 0), (-1, 0, 1)),
    ((1, 1, 0), (1, 0, 1)),
    ((1, 1, 0), (-1, 0, 1)),
)
pure_tensor = p3_restriction(pure_bases)
assert {index: value for index, value in pure_tensor.items() if value} == {
    (1, 0, 0): 2,
    (1, 0, 1): -2,
}

# Sharp zero P_3 coordinate-plane control.
zero_basis = ((1, 0, 0), (0, 1, 0))
zero_tensor = p3_restriction((zero_basis, zero_basis, zero_basis))
assert all(value == 0 for value in zero_tensor.values())

print(f"typed_three_deficient_profiles: {base_count}")
print(f"after_GLS63_incidence: {incidence_count}")
print(f"after_pair_class_extraction: {pair_count}")
print(f"after_full_P3_target_span: {len(final_profiles)}")
print(f"localized_three_deficient_orbits: {len(localized_orbit_counts)}")
print(f"after_common_support_P3_exclusion: {len(residual_profiles)}")
print(f"residual_three_deficient_orbits: {len(residual_orbit_counts)}")
print(f"P3_source_assignments: {sum(source_terms.values())}")
print(f"binary_P3_hyperdeterminant: {hyperdeterminant(binary_tensor)}")
print("pure_P3_nonzero_coefficients: 2")
print("zero_P3_nonzero_coefficients: 0")
print(
    "PASS: candidate GLS67 pair-class/P3 localization checks "
    "(audit only; eight residual orbits and global conjecture remain unresolved)"
)
