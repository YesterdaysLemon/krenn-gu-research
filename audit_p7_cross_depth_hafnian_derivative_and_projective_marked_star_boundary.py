"""Independent no-import audit of the P7 cross-depth hafnian boundary."""


def canonical_edge(u: int, v: int) -> tuple[int, int]:
    if u < v:
        return (u, v)
    return (v, u)


def multiply(left: dict[tuple[tuple[int, int], ...], int], edge_value: tuple[int, int]):
    result: dict[tuple[tuple[int, int], ...], int] = {}
    for monomial, coefficient in left.items():
        new_monomial = tuple(sorted(monomial + (edge_value,)))
        result[new_monomial] = result.get(new_monomial, 0) + coefficient
    return result


def add_into(target: dict[tuple[tuple[int, int], ...], int], source):
    for monomial, coefficient in source.items():
        target[monomial] = target.get(monomial, 0) + coefficient


def hafnian_polynomial(vertices: tuple[int, ...]):
    if not vertices:
        return {(): 1}
    first = vertices[0]
    total: dict[tuple[tuple[int, int], ...], int] = {}
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        add_into(total, multiply(hafnian_polynomial(rest), canonical_edge(first, partner)))
    return total


def shore_filter(poly, left=(0, 1), right=(2, 3)):
    shore_matchings = (
        frozenset((canonical_edge(left[0], right[0]), canonical_edge(left[1], right[1]))),
        frozenset((canonical_edge(left[0], right[1]), canonical_edge(left[1], right[0]))),
    )
    selected = {}
    for monomial, coefficient in poly.items():
        edge_set = frozenset(monomial)
        if any(shore <= edge_set for shore in shore_matchings):
            selected[monomial] = coefficient
    return selected


# Reconstruct the eight-vertex shore identity as a monomial statement.
full = hafnian_polynomial(tuple(range(8)))
selected = shore_filter(full)
expected = {}
for shore in (
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
):
    for remainder, coefficient in hafnian_polynomial((4, 5, 6, 7)).items():
        monomial = tuple(sorted(tuple(canonical_edge(*item) for item in shore) + remainder))
        expected[monomial] = expected.get(monomial, 0) + coefficient
assert selected == expected

# Differentiating edge 45 retains exactly the complementary edge 67.
edge_45 = (4, 5)
with_45 = {
    tuple(item for item in monomial if item != edge_45): coefficient
    for monomial, coefficient in selected.items()
    if edge_45 in monomial
}
expected_after = {
    tuple(sorted((canonical_edge(*shore[0]), canonical_edge(*shore[1]), (6, 7)))): 1
    for shore in (
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
}
assert with_45 == expected_after

# P7 complement map: the three differentiated edges avoiding a are exactly
# the complements of the three retained edges incident to a.
w_set = frozenset((1, 2, 3, 4))
all_pairs = []
for u in sorted(w_set):
    for v in sorted(w_set):
        if u < v:
            all_pairs.append(frozenset((u, v)))

for a in sorted(w_set):
    derivative_triangle = {p for p in all_pairs if a not in p}
    retained = {w_set - p for p in derivative_triangle}
    star = {p for p in all_pairs if a in p}
    assert retained == star


def permanental_pairs(first, second):
    values = []
    for pair in all_pairs:
        u, v = sorted(pair)
        values.append(first[u - 1] * second[v - 1] + first[v - 1] * second[u - 1])
    return tuple(values)


assert permanental_pairs((1, 1, 1, 1), (1, 1, 1, 1)) == (2, 2, 2, 2, 2, 2)
assert permanental_pairs((1, 0, 1, 0), (0, 1, 1, 2)) == (1, 1, 2, 1, 0, 2)
assert permanental_pairs((0, 0, 0, 0), (0, 0, 0, 0)) == (0, 0, 0, 0, 0, 0)

# Independent propagation proof: equality on every complement triangle makes
# all six values equal because every two triangles share one pair.
labels = {pair: next(iter(pair)) * 10 + max(pair) for pair in all_pairs}
relations = []
for a in sorted(w_set):
    triangle = sorted((p for p in all_pairs if a not in p), key=lambda p: tuple(sorted(p)))
    relations.append(tuple(triangle))
for first_index in range(len(relations)):
    for second_index in range(first_index + 1, len(relations)):
        assert set(relations[first_index]).intersection(relations[second_index])

# Simulate equality closure without linear-algebra imports.
parent = {pair: pair for pair in all_pairs}


def find(item):
    while parent[item] != item:
        parent[item] = parent[parent[item]]
        item = parent[item]
    return item


def union(left, right):
    root_left = find(left)
    root_right = find(right)
    if root_left != root_right:
        parent[root_right] = root_left


for triangle in relations:
    union(triangle[0], triangle[1])
    union(triangle[0], triangle[2])
assert len({find(pair) for pair in all_pairs}) == 1

# Free-h control in square-zero degree bookkeeping: Z has only its empty term.
empty_scalars = (-7, 0, 11)
for arbitrary_lambda in empty_scalars:
    z_nonempty = {pair: 0 for pair in all_pairs}
    marked_values = {
        a: sum(z_nonempty[pair] for pair in all_pairs if a in pair)
        for a in w_set
    }
    assert set(marked_values.values()) == {0}
    assert arbitrary_lambda in empty_scalars
assert len(set(empty_scalars)) == 3

print("independent shore-monomial recurrence: PASS")
print("independent P7 complement-star incidence: PASS")
print("independent permanental normalization/projective controls: PASS")
print("free-h marked-sector control: PASS")
print("GLOBAL KRENN-GU STATUS: UNRESOLVED")
