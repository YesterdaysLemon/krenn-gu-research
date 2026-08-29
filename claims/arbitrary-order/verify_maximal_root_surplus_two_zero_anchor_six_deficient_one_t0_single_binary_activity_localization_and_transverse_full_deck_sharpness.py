"""Primary checks for the candidate GLS72 one-T0 localization."""

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
    types = [DeficientType(frozenset((c,)), "S", 2, None) for c in COLOURS]
    for pair in combinations(COLOURS, 2):
        missing = next(c for c in COLOURS if c not in pair)
        types.append(DeficientType(frozenset(pair), "R", 1, missing))
    for pair in combinations(COLOURS, 2):
        types.append(DeficientType(frozenset(pair), "T", 2, None))
    return tuple(types)


TYPES = make_types()


def memberships(profile):
    return tuple(
        frozenset(i for i, map_type in enumerate(profile) if c in map_type.support)
        for c in COLOURS
    )


def missing_sets(profile):
    return tuple(frozenset(LABELS) - member for member in memberships(profile))


def gls63(profile):
    return all(len(member) <= 4 for member in memberships(profile))


def gls67_pairs(profile):
    missing = missing_sets(profile)
    for pair_tuple in combinations(LABELS, 2):
        pair = frozenset(pair_tuple)
        target_rank = sum(item == pair for item in missing)
        if not target_rank:
            continue
        if target_rank > 2:
            return False
        if any(profile[i].rank < target_rank for i in pair):
            return False
        if target_rank == 1 and all(profile[i].rank == 2 for i in pair):
            return False
    return True


def triangle_span(profile):
    missing = missing_sets(profile)
    for triple_tuple in combinations(LABELS, 3):
        triple = frozenset(triple_tuple)
        target = tuple(c for c in COLOURS if missing[c].issubset(triple))
        if len(target) > 2:
            return False
        for i in triple:
            map_type = profile[i]
            if map_type.kind == "R" and sum(c != map_type.readout for c in target) > 1:
                return False
    return True


def canonical(profile):
    candidates = []
    for colour_permutation in permutations(COLOURS):
        moved = []
        for map_type in profile:
            support = tuple(sorted(colour_permutation[c] for c in map_type.support))
            readout = (
                None
                if map_type.readout is None
                else colour_permutation[map_type.readout]
            )
            moved.append((map_type.kind, support, readout))
        candidates.append(tuple(sorted(moved)))
    return min(candidates)


def binary_triangles(profile):
    missing = missing_sets(profile)
    return tuple(
        triple
        for triple in map(frozenset, combinations(LABELS, 3))
        if sum(missing[c].issubset(triple) for c in COLOURS) == 2
    )


stages = [0, 0, 0, 0]
survivors = []
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


def is_sc2_tc4(profile):
    for colour in COLOURS:
        if (
            sum(
                item.kind == "S" and item.support == frozenset((colour,))
                for item in profile
            )
            == 2
            and sum(
                item.kind == "T" and item.support == frozenset(COLOURS) - {colour}
                for item in profile
            )
            == 4
        ):
            return True
    return False


def family_signature(profile):
    triangles = binary_triangles(profile)
    if len(triangles) != 1:
        return None
    triangle = triangles[0]
    missing = missing_sets(profile)
    target = tuple(c for c in COLOURS if missing[c].issubset(triangle))
    sizes = sorted(len(missing[c]) for c in target)
    family = "A" if sizes == [2, 2] else "B"
    outside = frozenset(LABELS) - triangle
    return family, sum(profile[i].kind == "T" for i in outside)


gls70 = [profile for profile in survivors if not is_sc2_tc4(profile)]
assert len(gls70) == 99_135
assert len({canonical(profile) for profile in gls70}) == 85

before = Counter(
    signature for profile in gls70 if (signature := family_signature(profile))
)
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


def removed_by_gls71(signature):
    return signature and (
        (signature[0] == "B" and signature[1] <= 2) or signature == ("A", 0)
    )


gls71 = [
    profile for profile in gls70 if not removed_by_gls71(family_signature(profile))
]
assert len(gls71) == 98_355
assert len({canonical(profile) for profile in gls71}) == 81

gls72 = list(gls71)
assert len(gls72) == 98_355
assert len({canonical(profile) for profile in gls72}) == 81
assert sum(family_signature(profile) == ("A", 1) for profile in gls72) == 1_080

after = Counter(
    signature for profile in gls72 if (signature := family_signature(profile))
)
assert after == Counter({("A", 1): 1_080, ("A", 2): 1_080, ("A", 3): 360, ("B", 3): 60})


# Tiny exact polynomial ring for the displayed determinant identities.
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]
NVAR = 4


def poly_var(index: int) -> Polynomial:
    exponent = [0] * NVAR
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def poly_add(*polynomials: Polynomial) -> Polynomial:
    result = defaultdict(Fraction)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] += coefficient
    return {monomial: value for monomial, value in result.items() if value}


def poly_scale(polynomial: Polynomial, scalar) -> Polynomial:
    scalar = Fraction(scalar)
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] += left_coefficient * right_coefficient
    return {monomial: value for monomial, value in result.items() if value}


def det2(matrix) -> Polynomial:
    return poly_add(
        poly_mul(matrix[0][0], matrix[1][1]),
        poly_scale(poly_mul(matrix[0][1], matrix[1][0]), -1),
    )


a, b, k, h = (poly_var(i) for i in range(NVAR))
zero: Polynomial = {}

all_active_x = ((b, a), (a, zero))
all_active_y = ((zero, b), (b, a))
assert det2(all_active_x) == poly_scale(poly_mul(a, a), -1)
assert det2(all_active_y) == poly_scale(poly_mul(b, b), -1)

minus_two_k = poly_scale(k, -2)
two_h = poly_scale(h, 2)
four_h = poly_scale(h, 4)
central_delta = (
    (poly_add(minus_two_k, four_h), poly_add(minus_two_k, two_h)),
    (poly_add(minus_two_k, two_h), minus_two_k),
)
central_beta = (
    (minus_two_k, poly_add(minus_two_k, two_h)),
    (poly_add(minus_two_k, two_h), poly_add(minus_two_k, four_h)),
)
expected_central_det = poly_scale(poly_mul(h, h), -4)
assert det2(central_delta) == expected_central_det
assert det2(central_beta) == expected_central_det


def add_tensor(*tensors):
    result = defaultdict(Fraction)
    for tensor in tensors:
        for index, coefficient in tensor.items():
            result[index] += coefficient
    return {index: value for index, value in result.items() if value}


def scale_tensor(tensor, scalar):
    scalar = Fraction(scalar)
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


def vector_scale(vector, scalar):
    scalar = Fraction(scalar)
    return tuple(scalar * entry for entry in vector)


def vector_add(*vectors):
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors))


x = (Fraction(1), Fraction(0))
y = (Fraction(0), Fraction(1))

# Replay the derivation of (23) and (25), not only their determinants, at
# independent exact rational parameters.  In the p,q bases take
# q3q4-p3p4=Y-X and choose lambda,mu so that (20) holds.
alpha_scalar = Fraction(2)
a_scalar = Fraction(3)
b_scalar = Fraction(5)
lambda_scalar = -Fraction(2, 1) / (b_scalar * alpha_scalar)
mu_scalar = -Fraction(2, 1) / (a_scalar * alpha_scalar)
p3 = p4 = x
q3 = q4 = y
u3_generic = u4_generic = vector_scale(x, 1 / b_scalar)
v3_generic = v4_generic = vector_scale(y, 1 / a_scalar)
l3_generic = l4_generic = vector_scale(vector_add(x, y), -1 / alpha_scalar)
d_u = add_tensor(outer(u3_generic, l4_generic), outer(l3_generic, u4_generic))
b_generic = scale_tensor(
    add_tensor(scale_tensor(outer(x, x), lambda_scalar), scale_tensor(d_u, -1)),
    1 / a_scalar,
)
assert vector_add(
    vector_scale(l3_generic, alpha_scalar),
    vector_scale(u3_generic, b_scalar),
    vector_scale(v3_generic, a_scalar),
) == (0, 0)
assert add_tensor(
    outer(u3_generic, l4_generic),
    outer(l3_generic, u4_generic),
    scale_tensor(b_generic, a_scalar),
) == scale_tensor(outer(x, x), lambda_scalar)
assert add_tensor(
    outer(v3_generic, l4_generic),
    outer(l3_generic, v4_generic),
    scale_tensor(b_generic, b_scalar),
) == scale_tensor(outer(y, y), mu_scalar)

r_scalar = Fraction(7)
d_scalar = Fraction(11)
delta3 = delta4 = vector_scale(
    vector_add(
        vector_scale(l3_generic, r_scalar),
        vector_scale(u3_generic, d_scalar),
    ),
    -1 / a_scalar,
)
delta_attachment = add_tensor(
    outer(delta3, l4_generic),
    outer(l3_generic, delta4),
    scale_tensor(b_generic, d_scalar),
)
k_scalar = r_scalar / alpha_scalar
h_scalar = d_scalar / b_scalar
m_delta = add_tensor(
    scale_tensor(outer(p3, p4), -2 * k_scalar + 4 * h_scalar),
    scale_tensor(outer(p3, q4), -2 * k_scalar + 2 * h_scalar),
    scale_tensor(outer(q3, p4), -2 * k_scalar + 2 * h_scalar),
    scale_tensor(outer(q3, q4), -2 * k_scalar),
    scale_tensor(outer(x, x), d_scalar * alpha_scalar * lambda_scalar),
)
assert scale_tensor(delta_attachment, a_scalar * alpha_scalar) == m_delta

s_scalar = Fraction(13)
c_scalar = Fraction(17)
beta3 = beta4 = vector_scale(
    vector_add(
        vector_scale(l3_generic, s_scalar),
        vector_scale(v3_generic, c_scalar),
    ),
    -1 / b_scalar,
)
beta_attachment = add_tensor(
    outer(beta3, l4_generic),
    outer(l3_generic, beta4),
    scale_tensor(b_generic, c_scalar),
)
k_scalar = s_scalar / alpha_scalar
h_scalar = c_scalar / a_scalar
m_beta = add_tensor(
    scale_tensor(outer(p3, p4), -2 * k_scalar),
    scale_tensor(outer(p3, q4), -2 * k_scalar + 2 * h_scalar),
    scale_tensor(outer(q3, p4), -2 * k_scalar + 2 * h_scalar),
    scale_tensor(outer(q3, q4), -2 * k_scalar + 4 * h_scalar),
    scale_tensor(outer(y, y), c_scalar * alpha_scalar * mu_scalar),
)
assert scale_tensor(beta_attachment, b_scalar * alpha_scalar) == m_beta

# Exact alpha=0 silent-T control for the restricted E/attachment subsystem.
# The theorem must use the central/full-parent equations beyond this control.
u3, u4, u5 = x, y, Fraction(1)
v3, v4, v5 = (-x[0], -x[1]), (-y[0], -y[1]), Fraction(1)
l4 = scale_tensor(outer(x), Fraction(1, 2))
l3 = scale_tensor(outer(y), Fraction(-1, 2))
b34 = scale_tensor(add_tensor(outer(x, x), outer(y, y)), Fraction(1, 2))


def vector_from_tensor(tensor):
    return tuple(tensor.get((i,), Fraction(0)) for i in range(2))


l4_vector = vector_from_tensor(l4)
l3_vector = vector_from_tensor(l3)
assert add_tensor(outer(u4, (v5,)), outer(v4, (u5,))) == {}
assert add_tensor(outer(u3, (v5,)), outer(v3, (u5,))) == {}
attachment_u = add_tensor(
    outer(u3, l4_vector), outer(l3_vector, u4), scale_tensor(b34, u5)
)
attachment_v = add_tensor(
    outer(v3, l4_vector), outer(l3_vector, v4), scale_tensor(b34, v5)
)
assert attachment_u == outer(x, x)
assert attachment_v == outer(y, y)

# Endpoint sign obstruction: selectors force V02=alpha*c0/a, so the
# restricted full-deck coefficient is exactly 2*alpha*c0.
alpha_value = Fraction(5)
a_value = Fraction(7)
c0_value = Fraction(11)
v02_value = alpha_value * c0_value / a_value
assert a_value * v02_value + alpha_value * c0_value == 2 * alpha_value * c0_value
assert 2 * alpha_value * c0_value != 0

# Tangent tensors at Y have no X coefficient, and tangent tensors at X have
# no Y coefficient.  This is the coefficient obstruction in (27), (33),
# and (34).
generic_left = (Fraction(2), Fraction(3))
generic_right = (Fraction(5), Fraction(7))
tangent_y = add_tensor(outer(generic_left, y), outer(y, generic_right))
tangent_x = add_tensor(outer(generic_left, x), outer(x, generic_right))
assert tangent_y.get((0, 0), 0) == 0
assert tangent_x.get((1, 1), 0) == 0

# The exact alpha=a=b=0 common-edge control from Theorem 3.2.  An edge is a
# list of decomposable terms (coefficient, left covector, right covector).
# We independently enumerate each four-vertex perfect matching.
e0 = (Fraction(1), Fraction(0), Fraction(0))
e1 = (Fraction(0), Fraction(1), Fraction(0))
e2 = (Fraction(0), Fraction(0), Fraction(1))
z = (Fraction(1),)

restricted_edges = {
    (0, 1): ((Fraction(1), e0, e0),),
    (0, 5): ((Fraction(1), e0, z),),
    (1, 3): ((Fraction(1), e1, x), (Fraction(1), e0, y)),
    (1, 4): ((Fraction(-1), e0, x),),
    (2, 4): ((Fraction(1), e2, y),),
    (3, 5): ((Fraction(1), y, z),),
    (4, 5): ((Fraction(1), x, z),),
}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((min(first, second), max(first, second)),) + matching


def physical_deck(vertices, edges):
    vertices = tuple(vertices)
    result = {}
    for matching in perfect_matchings(vertices):
        choices = [edges.get(edge, ()) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            factors = {}
            coefficient = Fraction(1)
            for edge, (term_coefficient, left, right) in zip(matching, selected):
                coefficient *= term_coefficient
                factors[edge[0]] = left
                factors[edge[1]] = right
            result = add_tensor(
                result,
                scale_tensor(
                    outer(*(factors[vertex] for vertex in vertices)), coefficient
                ),
            )
    return result


assert physical_deck((1, 2, 4, 5), restricted_edges) == {}
assert physical_deck((1, 2, 3, 5), restricted_edges) == {}
assert physical_deck((0, 1, 4, 5), restricted_edges) == {}
assert physical_deck((0, 2, 3, 5), restricted_edges) == {}
assert physical_deck((0, 3, 4, 5), restricted_edges) == {}
assert physical_deck((1, 3, 4, 5), restricted_edges) == outer(e1, x, x, z)
assert physical_deck((2, 3, 4, 5), restricted_edges) == outer(e2, y, y, z)

# W25 is transverse and therefore absent from restricted_edges.  On the
# full slot V5, it combines with W01 into the required pure four-deck.
e50 = e0
full_0125_edges = {
    (0, 1): ((Fraction(1), e0, e0),),
    (0, 5): ((Fraction(1), e0, e1),),
    (2, 5): ((Fraction(1), e0, e50),),
}
h0125_control = physical_deck((0, 1, 2, 5), full_0125_edges)
assert h0125_control == outer(e0, e0, e0, e50)

print(f"stage={tuple(stages)}")
print(f"pre_GLS71_single_binary={dict(sorted(before.items()))}")
print("Family_A_r_1_localized=1080 profiles / 1 key; removed=0")
print("post_GLS72_residual=98355 profiles / 81 keys")
print(f"post_GLS72_single_binary={dict(sorted(after.items()))}")
print("all-active determinants=PASS")
print("silent-T0 central determinants=PASS")
print("alpha=0 restricted control and tangent tests=PASS")
print("endpoint full-deck sign obstruction=PASS")
print("alpha=a=b=0 transverse common-edge control=PASS")
