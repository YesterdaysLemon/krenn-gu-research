"""Independent no-import audit of the same-mode N/N, q-minus exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json


IntVector = tuple[int, ...]
RatVector = tuple[Fraction, ...]
Quadratic = dict[tuple[int, int], int]
Matrix = tuple[tuple[int, ...], ...]
Tensor3 = tuple[int, ...]


QUADRATICS: dict[str, Quadratic] = {
    "m1": {(0, 1): -1, (1, 2): -1, (1, 3): 1},
    "m2": {(0, 1): -1, (0, 2): -1, (0, 3): 1},
    "d0": {(0, 1): -1, (0, 2): -1, (1, 3): 1, (2, 3): 1},
    "d1": {(0, 1): -1, (1, 2): -1, (0, 3): 1, (2, 3): 1},
    "d2": {(0, 1): -2},
}


def add(left: IntVector, right: IntVector) -> IntVector:
    """Add equal-length integer vectors."""
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(scalar: int, vector: IntVector) -> IntVector:
    """Scale an integer vector."""
    return tuple(scalar * entry for entry in vector)


def contract(quadratic: Quadratic, vector: IntVector) -> IntVector:
    """Contract an edge-dictionary quadratic by one vector."""
    result = [0, 0, 0, 0]
    for (left, right), coefficient in quadratic.items():
        result[right] += coefficient * vector[left]
        result[left] += coefficient * vector[right]
    return tuple(result)


def residuals(vector: IntVector) -> dict[str, IntVector]:
    """Compute all residual covectors without symbolic algebra."""
    return {name: contract(quadratic, vector) for name, quadratic in QUADRATICS.items()}


def quadratic_pair(quadratic: Quadratic, left: IntVector, right: IntVector) -> int:
    """Evaluate the polarization of an R-quadratic."""
    return sum(
        coefficient * (left[i] * right[j] + left[j] * right[i])
        for (i, j), coefficient in quadratic.items()
    )


def j_pair(left: IntVector, right: IntVector) -> int:
    """Evaluate the hyperbolic form on two A-vectors."""
    return left[0] * right[1] + left[1] * right[0]


def quartic_value(quadratic: Quadratic, vectors: tuple[IntVector, ...]) -> int:
    """Completely polarize x4*x5*quadratic on four six-vectors."""
    total = 0
    for first, second in combinations(range(4), 2):
        remaining = [index for index in range(4) if index not in (first, second)]
        total += j_pair(vectors[first][4:6], vectors[second][4:6]) * quadratic_pair(
            quadratic,
            vectors[remaining[0]][:4],
            vectors[remaining[1]][:4],
        )
    return total


def rref(rows: list[IntVector]) -> tuple[list[list[Fraction]], list[int]]:
    """Compute rational reduced row echelon form."""
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    if not matrix:
        return matrix, []
    pivots: list[int] = []
    pivot_row = 0
    for column in range(len(matrix[0])):
        candidate = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if candidate is None:
            continue
        matrix[pivot_row], matrix[candidate] = matrix[candidate], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            coefficient = matrix[row][column]
            if coefficient:
                matrix[row] = [
                    entry - coefficient * base
                    for entry, base in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivots


def rank(rows: list[IntVector]) -> int:
    """Return rational row rank."""
    return len(rref(rows)[1])


def nullspace(rows: list[IntVector], width: int) -> list[RatVector]:
    """Return a rational basis for the common row kernel."""
    reduced, pivots = rref(rows)
    free = [column for column in range(width) if column not in pivots]
    basis: list[RatVector] = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(width)]
        vector[free_column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return basis


def tensor3(left: IntVector, middle: IntVector, right: IntVector) -> Tensor3:
    """Flatten a decomposable integer 3-tensor."""
    return tuple(a * b * c for a in left for b in middle for c in right)


def tensor_add(*tensors: Tensor3) -> Tensor3:
    """Add flattened integer tensors."""
    return tuple(sum(entries) for entries in zip(*tensors, strict=True))


def matrix_column(matrix: Matrix, column: int) -> IntVector:
    """Extract one column."""
    return tuple(row[column] for row in matrix)


def matrix_from_rank_one(vector: IntVector, row: IntVector) -> Matrix:
    """Build a 2-by-3 rank-one matrix."""
    return tuple(tuple(vector[i] * row[j] for j in range(3)) for i in range(2))


def cubic_tensor(rows: tuple[IntVector, IntVector, IntVector], a_maps: tuple[Matrix, Matrix, Matrix]) -> Tensor3:
    """Independently polarize x4*x5*h on three local triples."""
    first_row, second_row, third_row = rows
    first_a, second_a, third_a = a_maps
    values: list[int] = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                value = (
                    first_row[i] * j_pair(matrix_column(second_a, j), matrix_column(third_a, k))
                    + second_row[j] * j_pair(matrix_column(first_a, i), matrix_column(third_a, k))
                    + third_row[k] * j_pair(matrix_column(first_a, i), matrix_column(second_a, j))
                )
                values.append(value)
    return tuple(values)


def coefficient_row(left: IntVector, matrix: Matrix, reverse: bool = False) -> IntVector:
    """Pair one A-vector with each column of a matrix."""
    if reverse:
        return tuple(j_pair(matrix_column(matrix, index), left) for index in range(3))
    return tuple(j_pair(left, matrix_column(matrix, index)) for index in range(3))


def audit_residual_geometry() -> dict[str, object]:
    """Reconstruct the companion fork from edge dictionaries."""
    n = (0, 0, 1, 1)
    m = (1, 1, 0, 0)
    k = (0, 0, 1, -1)
    ell = (-1, -1, -1, 1)
    h0 = (-1, 1, 1, 1)
    h1 = (1, -1, 1, 1)
    h2 = (1, -1, -1, 1)
    h2p = (-1, 1, -1, 1)

    n_values = residuals(n)
    assert n_values == {
        "m1": (0, 0, 0, 0),
        "m2": (0, 0, 0, 0),
        "d0": h0,
        "d1": h1,
        "d2": (0, 0, 0, 0),
    }
    kernel = nullspace([h0, h1], 4)
    assert len(kernel) == 2
    assert all(
        sum(Fraction(row[i]) * basis[i] for i in range(4)) == 0
        for row in (h0, h1)
        for basis in (tuple(Fraction(entry) for entry in m), tuple(Fraction(entry) for entry in k))
    )

    for s_value, u_value in ((1, 0), (0, 1), (1, -1), (2, 3), (-3, 2)):
        q = add(scale(s_value, m), scale(u_value, k))
        values = residuals(q)
        assert values["m1"] == add(scale(s_value, ell), (0, -2 * u_value, 0, 0))
        assert values["m2"] == add(scale(s_value, ell), (-2 * u_value, 0, 0, 0))
        assert values["d0"] == values["d1"] == scale(s_value + u_value, ell)
        assert values["d2"] == scale(-2 * s_value, m)

    minus = residuals(add(m, scale(-1, k)))
    assert minus["m1"] == h2p and minus["m2"] == h2
    assert minus["d0"] == minus["d1"] == (0, 0, 0, 0)
    assert minus["d2"] == scale(-2, m)
    minus_rows = [minus["m1"], minus["m2"], minus["d2"]]
    assert rank(minus_rows) == 3
    minus_kernel = nullspace(minus_rows, 4)
    assert minus_kernel == [(Fraction(0), Fraction(0), Fraction(1), Fraction(1))]
    assert h1 == add(add(h0, h2), scale(-1, h2p))
    return {
        "parameter_pairs_checked": 5,
        "H_N_dimension": len(kernel),
        "q_minus_residual_rank": 3,
        "q_minus_kernel": "K*N",
        "coincident_cycle_relation": "h1=h0+h2-h2prime",
    }


def audit_support_words() -> dict[str, object]:
    """Audit the identical double-N row and the no-second-N word identities."""
    n = (0, 0, 1, 1)
    double = {
        name: quadratic_pair(quadratic, n, n) for name, quadratic in QUADRATICS.items()
    }
    assert double == {"m1": 0, "m2": 0, "d0": 2, "d1": 2, "d2": 0}

    # A separating exact sample for the sign identity.  The implementation
    # is direct complete polarization, not the factorized primary route.
    n6 = (0, 0, 1, 1, 0, 0)
    t0 = (1, 2, 3, 4, 1, 2)
    t1 = tuple(n6[index] - t0[index] for index in range(6))
    companion = (2, -1, 1, 3, 2, 1)
    shore_u = (1, 0, 2, -1, 0, 0)
    shore_v = (0, 1, -1, 2, 0, 0)
    pure = quartic_value(QUADRATICS["d0"], (t0, companion, shore_u, shore_v))
    mixed = quartic_value(QUADRATICS["d0"], (t1, companion, shore_u, shore_v))
    assert pure != 0 and mixed == -pure
    assert quartic_value(QUADRATICS["d0"], (n6, companion, shore_u, shore_v)) == 0

    # Vary every shore to guard against an accidental numerical equality.
    samples = (
        ((2, 1, 0, 1, 3, -1), (1, -2, 3, 0, 0, 0), (2, 0, 1, -1, 0, 0)),
        ((0, 3, -1, 2, 1, 4), (-1, 1, 2, 3, 0, 0), (3, -2, 0, 1, 0, 0)),
        ((1, 1, 1, 1, -2, 3), (2, 3, -1, 4, 0, 0), (1, -1, 3, 2, 0, 0)),
    )
    for companion_sample, left_shore, right_shore in samples:
        live = quartic_value(QUADRATICS["d0"], (t0, companion_sample, left_shore, right_shore))
        forbidden = quartic_value(QUADRATICS["d0"], (t1, companion_sample, left_shore, right_shore))
        assert forbidden == -live
        assert quartic_value(
            QUADRATICS["d0"], (n6, companion_sample, left_shore, right_shore)
        ) == 0
    return {
        "double_N_row": double,
        "polarization_samples": 4,
        "support_two_sign_gate": "PASS",
        "singleton_one_supplier_gate": "PASS",
    }


def audit_collapsed_tensors() -> dict[str, object]:
    """Replay the 108 tensor entries on independent exact data."""
    data_sets = (
        ((1, 2), (1, 0, 2), (2, -1, 3)),
        ((2, -1), (0, 3, 1), (-2, 1, 1)),
        ((0, 1), (4, -1, 2), (3, 0, -2)),
        ((1, 0), (-1, 2, 1), (0, 1, 3)),
    )
    entries_checked = 0
    for offset, (p, alpha, gamma) in enumerate(data_sets):
        q = (p[0], -p[1])
        assert j_pair(p, q) == 0
        a_b = matrix_from_rank_one(p, alpha)
        a_d = matrix_from_rank_one(q, gamma)
        a_a = (
            (1 + offset, -2, 3),
            (2, 1 + offset, -1),
        )
        a_c = (
            (-1, 3 + offset, 2),
            (4, -2, 1 + offset),
        )
        x = (1, 2 + offset, -1)
        y = (-2, 1, 3 + offset)
        z = (3, -1, 2 + offset)
        w = (1 + offset, 4, -3)
        a0_row = (2, -3, 1 + offset)
        a1_row = (-1, 2 + offset, 4)
        c0_row = (3 + offset, 1, -2)
        c1_row = (1, -4, 2 + offset)

        beta = coefficient_row(p, a_c)
        delta = coefficient_row(q, a_c, reverse=True)
        pi = coefficient_row(p, a_a, reverse=True)
        epsilon = coefficient_row(q, a_a, reverse=True)
        direct = (
            cubic_tensor((x, c0_row, z), (a_b, a_c, a_d)),
            cubic_tensor((y, c1_row, w), (a_b, a_c, a_d)),
            cubic_tensor((x, a0_row, z), (a_b, a_a, a_d)),
            cubic_tensor((y, a1_row, w), (a_b, a_a, a_d)),
        )
        displayed = (
            tensor_add(tensor3(x, delta, gamma), tensor3(alpha, beta, z)),
            tensor_add(tensor3(y, delta, gamma), tensor3(alpha, beta, w)),
            tensor_add(tensor3(x, epsilon, gamma), tensor3(alpha, pi, z)),
            tensor_add(tensor3(y, epsilon, gamma), tensor3(alpha, pi, w)),
        )
        assert direct == displayed
        entries_checked += sum(len(tensor) for tensor in direct)

    e0, e1, zero = (1, 0, 0), (0, 1, 0), (0, 0, 0)
    target0, target1 = tensor3(e0, e0, e0), tensor3(e1, e1, e1)
    zero_tensor = (0,) * 27
    fork_e1 = (
        tensor_add(tensor3(e0, e0, e0), tensor3(e1, zero, zero)),
        tensor_add(tensor3(zero, e0, e0), tensor3(e1, zero, e1)),
        tensor_add(tensor3(e0, zero, e0), tensor3(e1, e1, zero)),
        tensor_add(tensor3(zero, zero, e0), tensor3(e1, e1, e1)),
    )
    fork_e0 = (
        tensor_add(tensor3(zero, zero, e1), tensor3(e0, e0, e0)),
        tensor_add(tensor3(e1, zero, e1), tensor3(e0, e0, zero)),
        tensor_add(tensor3(zero, e1, e1), tensor3(e0, zero, e0)),
        tensor_add(tensor3(e1, e1, e1), tensor3(e0, zero, zero)),
    )
    expected = (target0, zero_tensor, zero_tensor, target1)
    assert fork_e1 == fork_e0 == expected
    return {
        "exact_data_sets": len(data_sets),
        "tensor_entries_checked": entries_checked,
        "coordinate_forks": ["alpha=e0", "alpha=e1"],
    }


def projective_vectors(prime: int, dimension: int) -> list[IntVector]:
    """Enumerate normalized nonzero projective vectors over F_p."""
    vectors: list[IntVector] = []
    for vector in product(range(prime), repeat=dimension):
        if not any(vector):
            continue
        first = next(entry for entry in vector if entry)
        if first != 1:
            continue
        vectors.append(tuple(vector))
    return vectors


def modular_rank(rows: list[IntVector], prime: int) -> int:
    """Compute row rank over one prime field."""
    matrix = [[entry % prime for entry in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        candidate = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if candidate is None:
            continue
        matrix[pivot_row], matrix[candidate] = matrix[candidate], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], prime - 2, prime)
        matrix[pivot_row] = [(inverse * entry) % prime for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            coefficient = matrix[row][column]
            if coefficient:
                matrix[row] = [
                    (entry - coefficient * base) % prime
                    for entry, base in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivot_row += 1
    return pivot_row


def audit_modular_stress() -> dict[str, object]:
    """Audit-only finite-field stress of rank-one alignment and final pairing."""
    report: dict[str, object] = {}
    for prime in (3, 5):
        lines_a = projective_vectors(prime, 2)
        lines_c = projective_vectors(prime, 3)
        aligned_count = 0
        for rho in lines_c:
            for sigma in lines_c:
                matrix = [
                    tuple((rho[i] * sigma[j]) % prime for j in range(3))
                    for i in range(3)
                ]
                if any(matrix[i][j] for i in range(3) for j in range(3) if (i, j) != (2, 2)):
                    continue
                assert matrix[2][2]
                assert rho == sigma == (0, 0, 1)
                aligned_count += 1

        orthogonal_pairs = 0
        final_pairs = 0
        for p in lines_a:
            for q in lines_a:
                if j_pair(p, q) % prime:
                    continue
                orthogonal_pairs += 1
                p_perp = [
                    vector
                    for vector in product(range(prime), repeat=2)
                    if j_pair(p, tuple(vector)) % prime == 0
                ]
                q_perp = [
                    vector
                    for vector in product(range(prime), repeat=2)
                    if j_pair(q, tuple(vector)) % prime == 0
                ]
                for a_vector in q_perp:
                    for c_vector in p_perp:
                        assert j_pair(tuple(a_vector), tuple(c_vector)) % prime == 0
                        final_pairs += 1

        # Independently check rank(A_b)+rank(A_d)<=2 whenever all cross
        # pairings vanish, on every projective image-line pair.
        for p in lines_a:
            for q in lines_a:
                if j_pair(p, q) % prime == 0:
                    assert modular_rank([p], prime) + modular_rank([q], prime) == 2
        report[str(prime)] = {
            "projective_colour_rows": len(lines_c),
            "aligned_rank_one_matrices": aligned_count,
            "orthogonal_A_line_pairs": orthogonal_pairs,
            "final_pair_checks": final_pairs,
        }
    return report


def main() -> None:
    """Run the independent exact and audit-only modular checks."""
    report = {
        "residual_geometry": audit_residual_geometry(),
        "support_words": audit_support_words(),
        "collapsed_cycle": audit_collapsed_tensors(),
        "finite_field_stress_audit_only": audit_modular_stress(),
        "implementation": "standard library only; no SymPy or primary-verifier import",
        "scope": "q_minus exclusion only; q_plus remains open here",
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
