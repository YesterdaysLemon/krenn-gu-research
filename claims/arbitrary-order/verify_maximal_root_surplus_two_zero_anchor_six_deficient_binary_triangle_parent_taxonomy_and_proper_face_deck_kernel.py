"""Primary exact checks for the candidate GLS70 binary-triangle parent theorem."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product

COLOURS = tuple(range(3))
LABELS = tuple(range(6))
S = "S"
R = "R"
T = "T"


@dataclass(frozen=True)
class DeficientType:
    support: frozenset[int]
    kind: str
    rank: int
    readout: int | None


def make_types() -> tuple[DeficientType, ...]:
    result = [DeficientType(frozenset((c,)), S, 2, None) for c in COLOURS]
    for pair in combinations(COLOURS, 2):
        support = frozenset(pair)
        missing = next(c for c in COLOURS if c not in support)
        result.append(DeficientType(support, R, 1, missing))
    for pair in combinations(COLOURS, 2):
        result.append(DeficientType(frozenset(pair), T, 2, None))
    return tuple(result)


TYPES = make_types()


def memberships(maps: tuple[DeficientType, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(i for i, map_type in enumerate(maps) if c in map_type.support)
        for c in COLOURS
    )


def missing_sets(maps: tuple[DeficientType, ...]) -> tuple[frozenset[int], ...]:
    members = memberships(maps)
    return tuple(frozenset(LABELS) - members[c] for c in COLOURS)


def gls63_holds(maps: tuple[DeficientType, ...]) -> bool:
    members = memberships(maps)
    # With all six labels deficient and no U-label, GLS63 says that no colour
    # is visible on five or six kernel supports.
    return all(len(member_set) <= 4 for member_set in members)


def gls67_pair_holds(maps: tuple[DeficientType, ...]) -> bool:
    sets = missing_sets(maps)
    for open_pair_tuple in combinations(LABELS, 2):
        open_pair = frozenset(open_pair_tuple)
        target = tuple(c for c in COLOURS if sets[c] == open_pair)
        target_rank = len(target)
        if not target_rank:
            continue
        if target_rank > 2:
            return False
        if any(maps[index].rank < target_rank for index in open_pair):
            return False
        if target_rank == 1 and all(maps[index].rank == 2 for index in open_pair):
            return False
    return True


def triangle_span_holds(maps: tuple[DeficientType, ...]) -> bool:
    sets = missing_sets(maps)
    for triple_tuple in combinations(LABELS, 3):
        triple = frozenset(triple_tuple)
        target = tuple(c for c in COLOURS if sets[c].issubset(triple))
        if len(target) > 2:
            return False
        for index in triple:
            map_type = maps[index]
            if map_type.kind == R and sum(c != map_type.readout for c in target) > 1:
                return False
    return True


def canonical_key(maps: tuple[DeficientType, ...]) -> tuple:
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved = []
        for map_type in maps:
            moved_support = tuple(
                sorted(colour_permutation[c] for c in map_type.support)
            )
            moved_readout = (
                None
                if map_type.readout is None
                else colour_permutation[map_type.readout]
            )
            moved.append((map_type.kind, moved_support, moved_readout))
        candidates.append(tuple(sorted(moved)))
    return min(candidates)


def binary_triples(maps: tuple[DeficientType, ...]) -> tuple[frozenset[int], ...]:
    sets = missing_sets(maps)
    return tuple(
        triple
        for triple in map(frozenset, combinations(LABELS, 3))
        if sum(sets[c].issubset(triple) for c in COLOURS) == 2
    )


stage = [0, 0, 0, 0]
survivors: list[tuple[DeficientType, ...]] = []
for profile in product(TYPES, repeat=6):
    stage[0] += 1
    if not gls63_holds(profile):
        continue
    stage[1] += 1
    if not gls67_pair_holds(profile):
        continue
    stage[2] += 1
    if not triangle_span_holds(profile):
        continue
    stage[3] += 1
    survivors.append(profile)

assert tuple(stage) == (531_441, 276_750, 99_855, 99_180)
assert len({canonical_key(profile) for profile in survivors}) == 86

binary_multiplicity = Counter(
    len(binary_triples(profile)) for profile in survivors if binary_triples(profile)
)
assert binary_multiplicity == Counter({1: 3_360, 4: 45})

single_binary = [profile for profile in survivors if len(binary_triples(profile)) == 1]
four_binary = [profile for profile in survivors if len(binary_triples(profile)) == 4]
assert len({canonical_key(profile) for profile in single_binary}) == 8
assert len({canonical_key(profile) for profile in four_binary}) == 1


def classify_single(profile: tuple[DeficientType, ...]) -> tuple[str, int]:
    sets = missing_sets(profile)
    triangle = binary_triples(profile)[0]
    target = tuple(c for c in COLOURS if sets[c].issubset(triangle))
    assert len(target) == 2
    third_colour = next(c for c in COLOURS if c not in target)
    outside = frozenset(LABELS) - triangle
    assert sets[third_colour] == outside

    target_sizes = tuple(len(sets[c]) for c in target)
    if target_sizes == (2, 2):
        family = "A"
        common = sets[target[0]] & sets[target[1]]
        assert len(common) == 1
        common_label = next(iter(common))
        assert profile[common_label].kind == S
        assert profile[common_label].support == frozenset((third_colour,))
        for colour in target:
            other_label = next(iter(sets[colour] - common))
            assert profile[other_label].kind == R
            assert profile[other_label].readout == colour
    elif target_sizes == (3, 3):
        family = "B"
        assert all(sets[c] == triangle for c in target)
        assert all(
            profile[index].kind == S
            and profile[index].support == frozenset((third_colour,))
            for index in triangle
        )
    else:
        raise AssertionError((target_sizes, profile))

    for index in outside:
        assert profile[index].support == frozenset(target)
        assert profile[index].kind in (R, T)
    number_t = sum(profile[index].kind == T for index in outside)
    return family, number_t


family_counts = Counter(map(classify_single, single_binary))
assert family_counts == Counter(
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

family_key_counts = Counter()
for key in {canonical_key(profile) for profile in single_binary}:
    representative = next(
        profile for profile in single_binary if canonical_key(profile) == key
    )
    family_key_counts[classify_single(representative)[0]] += 1
assert family_key_counts == Counter({"A": 4, "B": 4})


def is_sc2_tc4(profile: tuple[DeficientType, ...]) -> bool:
    for colour in COLOURS:
        singleton = sum(
            map_type.kind == S and map_type.support == frozenset((colour,))
            for map_type in profile
        )
        complementary_t = sum(
            map_type.kind == T and map_type.support == frozenset(COLOURS) - {colour}
            for map_type in profile
        )
        if singleton == 2 and complementary_t == 4:
            return True
    return False


assert all(map(is_sc2_tc4, four_binary))

# Removing the analytically excluded S_c^2 T_c^4 key leaves the exact GLS70
# finite residual claimed in the prose.
gls70_survivors = [profile for profile in survivors if not is_sc2_tc4(profile)]
assert len(gls70_survivors) == 99_135
assert len({canonical_key(profile) for profile in gls70_survivors}) == 85
assert sum(bool(binary_triples(profile)) for profile in gls70_survivors) == 3_360


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    height = len(rows)
    width = len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [entry / scale for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


# Exact coefficient check for the load-bearing triangle step.  In normalized
# coordinates q_s=Q_b e_b and q_t=Q_a e_a.  The P_c coefficient is
# q_s tensor E_t + F_s tensor q_t.  Its coefficient matrix has trivial
# kernel in the six unknown coordinates of E_t,F_s.
triangle_matrix: list[list[Fraction]] = []
for q_colour in COLOURS:
    for s_coordinate in COLOURS:
        for t_coordinate in COLOURS:
            row = [Fraction(0) for _ in range(6)]
            # E_t coordinates occupy columns 0..2; q_s=Q_b e_(s,b).
            if q_colour == 1 and s_coordinate == 1:
                row[t_coordinate] += 1
            # F_s coordinates occupy columns 3..5; q_t=Q_a e_(t,a).
            if q_colour == 0 and t_coordinate == 0:
                row[3 + s_coordinate] += 1
            triangle_matrix.append(row)
assert matrix_rank(triangle_matrix) == 6

# With those two decks zero, g_st tensor d cannot equal a binary diagonal:
# the colour-a coefficient forces d=e_a up to a nonzero scalar, while the
# colour-b coefficient forces d=e_b up to a nonzero scalar.
ea = (Fraction(1), Fraction(0), Fraction(0))
eb = (Fraction(0), Fraction(1), Fraction(0))
assert ea != eb and matrix_rank([list(ea), list(eb)]) == 2


def tensor_index(indices: tuple[int, int, int, int]) -> int:
    value = 0
    for index in indices:
        value = 3 * value + index
    return value


def outer4(vectors: tuple[tuple[Fraction, ...], ...]) -> list[Fraction]:
    result = [Fraction(0) for _ in range(81)]
    for indices in product(COLOURS, repeat=4):
        coefficient = Fraction(1)
        for slot, index in enumerate(indices):
            coefficient *= vectors[slot][index]
        result[tensor_index(indices)] = coefficient
    return result


def matching_term(
    first_pair: tuple[int, int],
    first_edge: list[list[Fraction]],
    second_pair: tuple[int, int],
    second_edge: list[list[Fraction]],
) -> list[Fraction]:
    result = [Fraction(0) for _ in range(81)]
    for indices in product(COLOURS, repeat=4):
        coefficient = (
            first_edge[indices[first_pair[0]]][indices[first_pair[1]]]
            * second_edge[indices[second_pair[0]]][indices[second_pair[1]]]
        )
        result[tensor_index(indices)] = coefficient
    return result


def edge(left: tuple[Fraction, ...], right: tuple[Fraction, ...], scale=1):
    return [[Fraction(scale) * left[i] * right[j] for j in COLOURS] for i in COLOURS]


lambdas = tuple(map(Fraction, (2, 3, 5, 7)))
vectors_v = tuple((Fraction(1), lam, Fraction(0)) for lam in lambdas)
vectors_r = tuple((-lam, Fraction(1), Fraction(0)) for lam in lambdas)
for v, r in zip(vectors_v, vectors_r):
    assert sum(left * right for left, right in zip(v, r)) == 0

kappa = Fraction(11)
chi = Fraction(13)
w12 = edge(vectors_r[0], vectors_r[1], kappa)
w34 = edge(vectors_r[2], vectors_r[3])
w13 = edge(ea, ea)
w24 = edge(ea, ea, 1 - chi)
w14 = edge(ea, ea)
w23 = edge(ea, ea, chi)

physical_hafnian = [
    left + middle + right
    for left, middle, right in zip(
        matching_term((0, 1), w12, (2, 3), w34),
        matching_term((0, 2), w13, (1, 3), w24),
        matching_term((0, 3), w14, (1, 2), w23),
    )
]
expected_hafnian = [
    left + kappa * right
    for left, right in zip(outer4((ea, ea, ea, ea)), outer4(vectors_r))
]
assert physical_hafnian == expected_hafnian

# Stack the four one-slot contraction maps.  Their common kernel is already
# the kernel of the complete proper-face tower.  Exact rational elimination
# gives ambient rank 65 and kernel dimension 16.
contraction_matrix: list[list[Fraction]] = []
for contracted_slot in range(4):
    remaining_slots = tuple(slot for slot in range(4) if slot != contracted_slot)
    for remaining_indices in product(COLOURS, repeat=3):
        row = [Fraction(0) for _ in range(81)]
        for contracted_index in COLOURS:
            full = [0, 0, 0, 0]
            full[contracted_slot] = contracted_index
            for slot, index in zip(remaining_slots, remaining_indices):
                full[slot] = index
            row[tensor_index(tuple(full))] = vectors_v[contracted_slot][
                contracted_index
            ]
        contraction_matrix.append(row)
assert matrix_rank(contraction_matrix) == 65
assert 81 - matrix_rank(contraction_matrix) == 16

# The physical free direction is killed by every proper face.
free_direction = outer4(vectors_r)
for row in contraction_matrix:
    assert sum(left * right for left, right in zip(row, free_direction)) == 0

print(f"stage={tuple(stage)}")
print(f"single_binary_families={dict(sorted(family_counts.items()))}")
print("four_binary=S_c^2 T_c^4: profiles=45, keys=1")
print("post_GLS70_residual=99135 profiles / 85 keys")
print("triangle_P_c_cancellation_rank=6")
print("proper_face_kernel_dimension=16; physical_hafnian_direction=PASS")
