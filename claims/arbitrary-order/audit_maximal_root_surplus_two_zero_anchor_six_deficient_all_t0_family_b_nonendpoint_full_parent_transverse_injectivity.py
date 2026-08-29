"""No-import modular audit for the candidate GLS74 nonendpoint theorem."""

from itertools import combinations, product


PRIME = 101
OUTSIDE = tuple(range(3))


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
                    word[left] == 0 and word[right] == 1 and word[missing] == colour
                )
            if left in active_q:
                coefficient += int(
                    word[left] == 1 and word[right] == 0 and word[missing] == colour
                )
            row.append(coefficient)
        rows.append(row)
    return rows


koszul, domain = koszul_matrix()
assert rank_mod(koszul) == 26
alternating = [0] * len(domain)
for key, value in {
    (0, (0, 1)): 1,
    (0, (1, 0)): -1,
    (1, (1, 0)): 1,
    (1, (0, 1)): -1,
    (2, (0, 1)): 1,
    (2, (1, 0)): -1,
}.items():
    alternating[domain.index(key)] = value % PRIME
assert all(
    sum(entry * value for entry, value in zip(row, alternating)) % PRIME == 0
    for row in koszul
)

assert rank_mod(parent_matrix()) == 9
assert rank_mod(parent_matrix(local_dim=2)) == 6
assert rank_mod(parent_matrix(local_dim=2, active_q={0, 1})) == 4
assert rank_mod(parent_matrix(local_dim=2, active_q={0})) == 3

# Exhaust the all-A scalar pair system over F_7.  Whenever one b pair is
# nonzero, the complementary column vanishes and the other two b pairs do.
small_prime = 7
checked = 0
nonzero_edge_solutions = 0
for values in product(range(small_prime), repeat=6):
    x = values[:3]
    y = values[3:]
    valid = True
    edge_values = {}
    for left, right in combinations(OUTSIDE, 2):
        cross = (x[left] * y[right] + x[right] * y[left]) % small_prime
        if (x[left] * x[right] - y[left] * y[right]) % small_prime:
            valid = False
            break
        if (cross + y[left] * y[right]) % small_prime:
            valid = False
            break
        edge_values[(left, right)] = y[left] * y[right] % small_prime
    if not valid:
        continue
    checked += 1
    for pair, edge_value in edge_values.items():
        if not edge_value:
            continue
        nonzero_edge_solutions += 1
        complement = next(port for port in OUTSIDE if port not in pair)
        assert x[complement] == y[complement] == 0
        assert all(
            not value for other_pair, value in edge_values.items() if other_pair != pair
        )
assert checked
assert nonzero_edge_solutions

# The omega boundary survives every restricted pair equation over F_7.
omega = 2
assert (omega * omega + omega + 1) % small_prime == 0
rho = {
    0: (0, 0, 0),
    1: (omega, 1, omega * omega % small_prime),
    2: (omega * omega % small_prime, 1, omega),
}
edges = {(0, 1): 0, (0, 2): 0, (1, 2): 1}
for left, right in combinations(OUTSIDE, 2):
    for j, k in ((1, 2), (0, 2), (0, 1)):
        value = (
            edges[(left, right)]
            + rho[left][j] * rho[right][k]
            + rho[right][j] * rho[left][k]
        ) % small_prime
        assert value == 0

# Exhaust the exactly-one-A support logic independently.
for active_mask in range(1, 8):
    active = {port for port in OUTSIDE if active_mask & (1 << port)}
    allowed = {
        port
        for port in OUTSIDE
        if all(other == port for other in active)
    }
    assert len(allowed) <= 1
    assert all(not (left in allowed and right in allowed) for left, right in combinations(OUTSIDE, 2))

print("independent ranks: Koszul=26/27, full-parent=9/9, row-parent=6/6")
print(f"F_7 all-A scalar solutions checked={checked}; nonzero-edge cases={nonzero_edge_solutions}")
print("omega restricted control=PASS; full D=0 row is load-bearing")
print("endpoint activity ranks=4 (two active) / 3 (one active): endpoint OPEN")
print("GLS74 scope audit: central-mixed-support nonendpoint only")
print("central root-axis degeneracies / outside endpoints OPEN; inherited residual unchanged")
