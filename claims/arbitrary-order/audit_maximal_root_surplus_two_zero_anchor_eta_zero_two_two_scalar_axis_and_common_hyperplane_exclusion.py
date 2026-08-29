"""Independent standard-library audit for GLS66 finite algebra."""

from itertools import combinations, product

SOURCE_DIM = 4
PAIRS = tuple(combinations(range(SOURCE_DIM), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
FULL = frozenset(range(SOURCE_DIM))


def inv(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def edge_value(edges: dict[tuple[int, int], int], i: int, j: int) -> int:
    return edges[tuple(sorted((i, j)))]


def squarefree_product(
    u: tuple[int, ...], v: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    return tuple((u[i] * v[j] + u[j] * v[i]) % prime for i, j in PAIRS)


def pairing(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> int:
    total = 0
    for pair, coefficient in zip(PAIRS, left, strict=True):
        complement = tuple(sorted(FULL - set(pair)))
        total += coefficient * right[PAIR_INDEX[complement]]
    return total % prime


def matrix_rank(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    work = [[entry % prime for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][column], prime)
        work[rank] = [(entry * scale) % prime for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def hyperplane_basis(
    normal: tuple[int, ...], prime: int
) -> tuple[tuple[int, ...], ...]:
    vectors: list[tuple[int, ...]] = []
    for candidate in product(range(prime), repeat=SOURCE_DIM):
        if candidate == (0,) * SOURCE_DIM:
            continue
        if sum(x * y for x, y in zip(normal, candidate, strict=True)) % prime:
            continue
        proposed = vectors + [candidate]
        if matrix_rank([list(vector) for vector in proposed], prime) > len(vectors):
            vectors.append(candidate)
        if len(vectors) == SOURCE_DIM - 1:
            return tuple(vectors)
    raise AssertionError("failed to construct hyperplane basis")


def scalar_hierarchy_census() -> int:
    prime = 3
    ports = range(4)  # s,t,r,v
    accepted = 0
    nonzero_pairs = tuple(
        pair for pair in product(range(prime), repeat=2) if pair != (0, 0)
    )
    for (ar, br), (av, bv) in product(nonzero_pairs, repeat=2):
        a_values = (0, 0, ar, av)
        b_values = (0, 0, br, bv)
        for edge_tuple in product(range(prime), repeat=6):
            edges = dict(zip(PAIRS, edge_tuple, strict=True))
            deltas = []
            for i, j in PAIRS:
                deltas.append(
                    (a_values[i] * b_values[j] + b_values[i] * a_values[j]) % prime
                )
            if any(deltas):
                continue

            cofactors = []
            for omitted in ports:
                rest = tuple(port for port in ports if port != omitted)
                for values in (a_values, b_values):
                    total = 0
                    for i in rest:
                        j, k = (port for port in rest if port != i)
                        total += values[i] * edge_value(edges, j, k)
                    cofactors.append(total % prime)
            if any(cofactors):
                continue

            h_value = (
                edge_value(edges, 0, 1) * edge_value(edges, 2, 3)
                + edge_value(edges, 0, 2) * edge_value(edges, 1, 3)
                + edge_value(edges, 0, 3) * edge_value(edges, 1, 2)
            ) % prime
            if h_value == 0:
                continue

            accepted += 1
            assert edge_value(edges, 0, 1) == 0
            a_axis = ar != 0 and av != 0 and br == 0 and bv == 0
            b_axis = br != 0 and bv != 0 and ar == 0 and av == 0
            assert a_axis != b_axis
            first_r, first_v = (ar, av) if a_axis else (br, bv)
            lam = first_v * inv(first_r, prime) % prime
            assert edge_value(edges, 1, 3) == -lam * edge_value(edges, 1, 2) % prime
            assert edge_value(edges, 0, 3) == -lam * edge_value(edges, 0, 2) % prime
            cross = (
                edge_value(edges, 0, 2),
                edge_value(edges, 0, 3),
                edge_value(edges, 1, 2),
                edge_value(edges, 1, 3),
            )
            assert all(cross)
            assert (
                h_value
                == -2 * lam * edge_value(edges, 0, 2) * edge_value(edges, 1, 2) % prime
            )
    assert accepted > 0
    return accepted


def independent_hyperplane_census() -> tuple[int, int]:
    prime = 3
    p_row = (1, 0, 0, 0)
    q_row = (0, 1, 0, 0)
    projective_normals = []
    for p_coordinate, q_coordinate, b_coordinate in product(range(prime), repeat=3):
        raw = (p_coordinate, q_coordinate, 0, b_coordinate)
        if raw == (0, 0, 0, 0):
            continue
        first = next(entry for entry in raw if entry)
        normalized = tuple(entry * inv(first, prime) % prime for entry in raw)
        if normalized not in projective_normals:
            projective_normals.append(normalized)

    def silent_rows(orientation: str):
        if orientation == "X":
            off = q_row
            for a_coordinate, b_coordinate in product(range(prime), repeat=2):
                yield (1, 0, a_coordinate, b_coordinate), off
        else:
            off = p_row
            for a_coordinate, b_coordinate in product(range(prime), repeat=2):
                yield (0, 1, a_coordinate, b_coordinate), off

    trials = 0
    compatible = 0
    for normal_r, normal_v in product(projective_normals, repeat=2):
        if normal_r == normal_v:
            continue
        basis_r = hyperplane_basis(normal_r, prime)
        basis_v = hyperplane_basis(normal_v, prime)
        pair_image = tuple(
            squarefree_product(left, right, prime)
            for left in basis_r
            for right in basis_v
        )
        for orientation_s, orientation_t in product(("X", "Y"), repeat=2):
            for (u_s, off_s), (u_t, off_t) in product(
                silent_rows(orientation_s), silent_rows(orientation_t)
            ):
                trials += 1
                off_products = (
                    squarefree_product(off_s, off_t, prime),
                    squarefree_product(off_s, u_t, prime),
                    squarefree_product(u_s, off_t, prime),
                )
                if all(
                    pairing(off_product, hh, prime) == 0
                    for off_product in off_products
                    for hh in pair_image
                ):
                    compatible += 1
    assert compatible == 0
    return trials, compatible


def common_hyperplane_census() -> tuple[int, int]:
    prime = 5
    p_row = (1, 0, 0, 0)
    q_row = (0, 1, 0, 0)
    a_row = (0, 0, 1, 0)
    trials = 0
    purity_compatible = 0

    def silent_rows(orientation: str):
        if orientation == "X":
            off = q_row
            for a_coordinate, b_coordinate in product(range(prime), repeat=2):
                yield (1, 0, a_coordinate, b_coordinate), off
        else:
            off = p_row
            for a_coordinate, b_coordinate in product(range(prime), repeat=2):
                yield (0, 1, a_coordinate, b_coordinate), off

    for tau in range(prime):
        r0 = (1, 0, 0, -tau % prime)
        hyperplane_basis = (q_row, a_row, r0)
        pair_image = tuple(
            squarefree_product(left, right, prime)
            for left in hyperplane_basis
            for right in hyperplane_basis
        )
        for orientation_s, orientation_t in product(("X", "Y"), repeat=2):
            for (u_s, off_s), (u_t, off_t) in product(
                silent_rows(orientation_s), silent_rows(orientation_t)
            ):
                trials += 1
                off_products = (
                    squarefree_product(off_s, off_t, prime),
                    squarefree_product(off_s, u_t, prime),
                    squarefree_product(u_s, off_t, prime),
                )
                if any(
                    pairing(off_product, hh, prime)
                    for off_product in off_products
                    for hh in pair_image
                ):
                    continue
                purity_compatible += 1
                target_product = squarefree_product(u_s, u_t, prime)
                target_matrix = [
                    [
                        pairing(
                            target_product,
                            squarefree_product(left, right, prime),
                            prime,
                        )
                        for right in hyperplane_basis
                    ]
                    for left in hyperplane_basis
                ]
                assert matrix_rank(target_matrix, prime) != 1
    return trials, purity_compatible


scalar_solutions = scalar_hierarchy_census()
independent_trials, independent_compatible = independent_hyperplane_census()
orientation_trials, compatible_off_shells = common_hyperplane_census()

print(f"F3_scalar_hierarchy_solutions_with_H_nonzero: {scalar_solutions}")
print(f"F3_independent_hyperplane_orientation_trials: {independent_trials}")
print(f"F3_independent_hyperplane_off_shells: {independent_compatible}")
print(f"F5_common_hyperplane_orientation_trials: {orientation_trials}")
print(f"F5_off_shell_compatible_trials: {compatible_off_shells}")
print("F5_nonzero_rank_one_target_slices: 0")
print(
    "PASS (GLS66 independent finite/displayed audit only; higher-deficient "
    "branches and global Krenn-Gu conjecture remain unresolved)"
)
