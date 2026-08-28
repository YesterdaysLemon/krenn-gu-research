"""Independent standard-library audit for GLS65 finite/displayed algebra."""

from itertools import permutations, product
from random import Random

SOURCE_ROWS = tuple(range(4))  # P,Q,A,B
P, Q, A, B = SOURCE_ROWS


def permanent(rows, modulus=None):
    total = 0
    for assignment in permutations(range(len(rows))):
        term = 1
        for i, j in enumerate(assignment):
            term *= rows[i][j]
        total += term
    return total if modulus is None else total % modulus


def tensor_permanent(local_columns):
    dimensions = tuple(len(local_columns[i][P]) for i in range(4))
    result = {}
    for output in product(*(range(dimension) for dimension in dimensions)):
        total = 0
        for assignment in permutations(SOURCE_ROWS):
            term = 1
            for i, source_row in enumerate(assignment):
                term *= local_columns[i][source_row][output[i]]
            total += term
        result[output] = total
    return result


def matrix_rank_mod(rows, modulus):
    matrix = [
        [entry % modulus for entry in row]
        for row in rows
        if any(entry % modulus for entry in row)
    ]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [(entry * inverse) % modulus for entry in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][column]:
                continue
            factor = matrix[i][column]
            matrix[i] = [
                (matrix[i][j] - factor * matrix[rank][j]) % modulus
                for j in range(columns)
            ]
        rank += 1
    return rank


def squarefree_multiply(left, right, modulus):
    result = [0] * 16
    for mask_left, coefficient_left in enumerate(left):
        if not coefficient_left:
            continue
        for mask_right, coefficient_right in enumerate(right):
            if not coefficient_right or mask_left & mask_right:
                continue
            mask = mask_left | mask_right
            result[mask] = (
                result[mask] + coefficient_left * coefficient_right
            ) % modulus
    return result


def linear_form(vector, modulus):
    result = [0] * 16
    for i, coefficient in enumerate(vector):
        result[1 << i] = coefficient % modulus
    return result


def multiply_three(first, second, third, modulus):
    return squarefree_multiply(
        squarefree_multiply(first, second, modulus), third, modulus
    )


def canonical_projective_vectors(dimension, modulus):
    representatives = []
    for vector in product(range(modulus), repeat=dimension):
        if not any(vector):
            continue
        first = next(i for i, value in enumerate(vector) if value)
        if vector[first] != 1:
            continue
        representatives.append(vector)
    return representatives


# Independent twenty-four-term source count.
assignments = set()
for i in range(4):
    for j in range(i + 1, 4):
        complement = tuple(k for k in range(4) if k not in (i, j))
        for p_at_i in (True, False):
            for a_at_first in (True, False):
                assignment = [None] * 4
                assignment[i], assignment[j] = (P, Q) if p_at_i else (Q, P)
                assignment[complement[0]], assignment[complement[1]] = (
                    (A, B) if a_at_first else (B, A)
                )
                assignments.add(tuple(assignment))
assert assignments == set(permutations(SOURCE_ROWS))


# Fixed mixed fibre and exact q-flat, using a separate integer implementation.
binary_columns = []
for a_coefficient in (-2, 1, 1, 1):
    binary_columns.append(
        {
            P: (1, 0),
            Q: (0, 1),
            A: (a_coefficient, 0),
            B: (1, 0),
        }
    )
binary_tensor = tensor_permanent(binary_columns)
assert binary_tensor[(1, 0, 0, 0)] == 6
assert sum(value != 0 for value in binary_tensor.values()) == 1

rng = Random(6502233)
flat_samples = 24
for _ in range(flat_samples):
    flat_columns = [binary_columns[0]]
    for _port in range(3):
        arbitrary_q = tuple(rng.randrange(-7, 8) for _ in range(3))
        flat_columns.append(
            {
                P: (1, 0, 0),
                Q: arbitrary_q,
                A: (1, 0, 0),
                B: (1, 0, 0),
            }
        )
    flat_tensor = tensor_permanent(flat_columns)
    assert flat_tensor[(1, 0, 0, 0)] == 6
    assert sum(value != 0 for value in flat_tensor.values()) == 1


# Independent random audit of every all-rank-two orientation word over F_101.
prime = 101
orientation_trials = 0
for word in product((P, Q), repeat=4):
    for _ in range(300):
        rows = [[rng.randrange(prime) for _ in range(4)] for _ in range(4)]
        # Required active c-row coefficient: P for off Q, Q for off P.
        if any(rows[i][P if word[i] == Q else Q] == 0 for i in range(4)):
            continue
        pure = True
        for off_bits in product((0, 1), repeat=4):
            if not any(off_bits):
                continue
            selected = []
            for i, is_off in enumerate(off_bits):
                unit = [0, 0, 0, 0]
                unit[word[i]] = 1
                selected.append(unit if is_off else rows[i])
            if permanent(selected, prime):
                pure = False
                break
        if pure:
            assert permanent(rows, prime) == 0
        orientation_trials += 1


# Exhaustive F_3 census of all mixed triples of planes through e_P/e_Q.
finite_prime = 3
quotient_points = canonical_projective_vectors(3, finite_prime)
assert len(quotient_points) == 13


def plane_row(off_coordinate, quotient_point):
    row = []
    cursor = 0
    for coordinate in range(4):
        if coordinate == off_coordinate:
            row.append(0)
        else:
            row.append(quotient_point[cursor])
            cursor += 1
    return row


mixed_words = [word for word in product((P, Q), repeat=3) if len(set(word)) == 2]
mixed_triples = 0
dangerous_mixed_triples = 0
for word in mixed_words:
    off_forms = [
        linear_form(tuple(1 if j == word[i] else 0 for j in range(4)), finite_prime)
        for i in range(3)
    ]
    for point_tuple in product(quotient_points, repeat=3):
        u_forms = [
            linear_form(plane_row(word[i], point_tuple[i]), finite_prime)
            for i in range(3)
        ]
        all_c = multiply_three(*u_forms, finite_prime)
        off_products = []
        for bits in product((0, 1), repeat=3):
            if not any(bits):
                continue
            factors = [off_forms[i] if bits[i] else u_forms[i] for i in range(3)]
            off_products.append(multiply_three(*factors, finite_prime))
        off_rank = matrix_rank_mod(off_products, finite_prime)
        total_rank = matrix_rank_mod(off_products + [all_c], finite_prime)
        if total_rank <= 2 and total_rank > off_rank:
            dangerous_mixed_triples += 1
        mixed_triples += 1

assert dangerous_mixed_triples == 0


# Independent finite checks of the anchor permanent identities.
anchor_trials = 5000
for _ in range(anchor_trials):
    x = [rng.randrange(prime) for _ in range(3)]
    alpha = [rng.randrange(prime) for _ in range(3)]
    beta = [rng.randrange(prime) for _ in range(3)]
    h_p = []
    h_a = []
    h_b = []
    for i in range(3):
        j, k = tuple(index for index in range(3) if index != i)
        h_p.append((alpha[j] * beta[k] + beta[j] * alpha[k]) % prime)
        h_a.append((x[j] * beta[k] + beta[j] * x[k]) % prime)
        h_b.append((x[j] * alpha[k] + alpha[j] * x[k]) % prime)
    k_p4 = permanent([[x[i], alpha[i], beta[i]] for i in range(3)], prime)
    assert k_p4 == sum(x[i] * h_p[i] for i in range(3)) % prime
    assert k_p4 == sum(alpha[i] * h_a[i] for i in range(3)) % prime
    assert k_p4 == sum(beta[i] * h_b[i] for i in range(3)) % prime

print("factorized source assignments: 24")
print("fixed-fibre nonzero binary coefficients: 1")
print(f"exact q-flat samples: {flat_samples}")
print(f"all-rank-two orientation trials: {orientation_trials}")
print(f"mixed triple plane tuples over F_3: {mixed_triples}")
print("dangerous mixed triple tuples: 0")
print(f"anchor identity trials over F_101: {anchor_trials}")
print(
    "PASS (GLS65 finite/displayed audit only; 2233 residual and global "
    "Krenn-Gu conjecture remain unresolved)"
)
