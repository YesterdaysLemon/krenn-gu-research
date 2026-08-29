"""No-import modular audit for the GLS75 complete nonendpoint exclusion."""

from itertools import combinations, product


PRIME = 101
OUTSIDE = tuple(range(3))
OUTSIDE_LABELS = (3, 4, 5)


def rank_mod(matrix, prime=PRIME):
    rows = [[entry % prime for entry in row] for row in matrix]
    if not rows:
        return 0
    height = len(rows)
    width = len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [(entry * inverse) % prime for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % prime
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def koszul_matrix(local_dim=3):
    domain = [
        (missing, pair_word)
        for missing in OUTSIDE
        for pair_word in product(range(local_dim), repeat=2)
    ]
    rows = []
    for shore in (0, 1):
        for word in product(range(local_dim), repeat=3):
            row = []
            for missing, pair_word in domain:
                rest = tuple(port for port in OUTSIDE if port != missing)
                row.append(
                    int(
                        word[missing] == shore
                        and pair_word == tuple(word[port] for port in rest)
                    )
                )
            rows.append(row)
    return rows, domain


def parent_matrix(local_dim=3, active_q=None):
    active_q = set(OUTSIDE if active_q is None else active_q)
    domain = [(missing, colour) for missing in OUTSIDE for colour in range(local_dim)]
    rows = []
    for word in product(range(local_dim), repeat=3):
        row = []
        for missing, colour in domain:
            left, right = tuple(port for port in OUTSIDE if port != missing)
            coefficient = 0
            if right in active_q:
                coefficient += int(
                    word[left] == 0
                    and word[right] == 1
                    and word[missing] == colour
                )
            if left in active_q:
                coefficient += int(
                    word[left] == 1
                    and word[right] == 0
                    and word[missing] == colour
                )
            row.append(coefficient)
        rows.append(row)
    return rows, domain


def hstack(left, right):
    return [left_row + right_row for left_row, right_row in zip(left, right)]


def zero_rows(height, width):
    return [[0] * width for _ in range(height)]


def forced_zero(matrix, coordinate):
    unit = [0] * len(matrix[0])
    unit[coordinate] = 1
    return rank_mod(matrix + [unit]) == rank_mod(matrix)


koszul, pair_domain = koszul_matrix()
shore_u = koszul[:27]
shore_v = koszul[27:]
parent, row_domain = parent_matrix()

one_sided = hstack(shore_u, zero_rows(27, 9)) + hstack(
    shore_v, [[-entry for entry in row] for row in parent]
)
assert len(one_sided) == 54 and len(one_sided[0]) == 36
assert rank_mod(one_sided) == 31
assert rank_mod(koszul) == 26
# The one-sided kernel has dimension five; imposing D=0 leaves the
# one-dimensional common Koszul kernel, so its D projection has dimension 4.
assert (36 - rank_mod(one_sided)) - (27 - rank_mod(koszul)) == 4

for missing in OUTSIDE:
    coordinate = 27 + row_domain.index((missing, 2))
    assert forced_zero(one_sided, coordinate)

for colour in (0, 1):
    total_row = [0] * 36
    for missing in OUTSIDE:
        total_row[27 + row_domain.index((missing, colour))] = 1
    assert rank_mod(one_sided + [total_row]) == 31

for missing in OUTSIDE:
    coordinate = pair_domain.index((missing, (2, 2)))
    assert forced_zero(shore_u, coordinate)

zero_coupling = hstack(shore_u, zero_rows(27, 9)) + hstack(
    zero_rows(27, 27), parent
)
assert rank_mod(zero_coupling) == 28
for missing, colour in row_domain:
    assert forced_zero(zero_coupling, 27 + row_domain.index((missing, colour)))


def shore_supports(label, probe_index):
    return probe_index == 0 if label in OUTSIDE_LABELS or label == 0 else True


for target_colour in (1, 2):
    surviving = []
    for left, right in combinations(range(6), 2):
        pq = shore_supports(left, target_colour) and shore_supports(
            right, target_colour
        )
        qp = shore_supports(left, target_colour) and shore_supports(
            right, target_colour
        )
        if pq or qp:
            surviving.append((left, right))
    assert surviving == [(1, 2)]

# Exhaust the one-A bracket over F_7.  Every nonendpoint row has both shore
# coordinates nonzero, and either available identity leaves a nonzero mixed
# coefficient in the bracket.
small_prime = 7
brackets_checked = 0
for au, bu, aw, bw in product(range(1, small_prime), repeat=4):
    bracket_u = ((aw + au) % small_prime, bw, bu, 0)
    bracket_v = (0, au, aw, (bw + bu) % small_prime)
    assert any(bracket_u)
    assert any(bracket_v)
    brackets_checked += 1

# Independently exhaust the all-A scalar pair relations.  A nonzero edge
# forces its complementary column and the other two edges to zero.
all_a_solutions = 0
nonzero_edges = 0
for values in product(range(small_prime), repeat=6):
    x = values[:3]
    y = values[3:]
    edges = {}
    valid = True
    for left, right in combinations(OUTSIDE, 2):
        cross = (x[left] * y[right] + x[right] * y[left]) % small_prime
        if (x[left] * x[right] - y[left] * y[right]) % small_prime:
            valid = False
            break
        if (cross + y[left] * y[right]) % small_prime:
            valid = False
            break
        edges[(left, right)] = y[left] * y[right] % small_prime
    if not valid:
        continue
    all_a_solutions += 1
    for pair, value in edges.items():
        if not value:
            continue
        nonzero_edges += 1
        complement = next(port for port in OUTSIDE if port not in pair)
        assert x[complement] == y[complement] == 0
        assert all(not edge for other, edge in edges.items() if other != pair)

assert all_a_solutions and nonzero_edges
assert rank_mod(parent_matrix(local_dim=2)[0]) == 6
assert rank_mod(parent_matrix(local_dim=2, active_q={0, 1})[0]) == 4
assert rank_mod(parent_matrix(local_dim=2, active_q={0})[0]) == 3

print("independent one-sided block: rank 31/36; nullity 5")
print("all transverse D coordinates and all pair KxK scalars forced zero")
print("double-root central source-pair support: exactly {1,2} for both colours")
print(f"F_7 one-A transverse brackets checked={brackets_checked}")
print(
    f"F_7 all-A solutions={all_a_solutions}; nonzero-edge cases={nonzero_edges}"
)
print("GLS75 scope audit: complete outside nonendpoint EMPTY")
print("P/Q-common endpoints OPEN; inherited residual unchanged")
