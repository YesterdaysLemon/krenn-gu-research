"""Independent exact audit of the common-contraction/alignment theorem.

This file deliberately imports no project code and no primary verifier.  It
uses only ``fractions.Fraction`` and independently implemented row reduction.
The primal legal-space calculation solves an explicit subspace-intersection
system.  The dual calculation instead builds annihilators and their sums.
Agreement of those two routes audits the theorem's nontrivial identity.

The script is a finite replay of the displayed six-dimensional identities;
the written proof remains the proof of the arbitrary-field statements.
"""

from fractions import Fraction
from itertools import product

Q = Fraction
N = 6
PAIR_NAMES = ("12", "13", "14", "23", "24", "34")
COMPLEMENT = (5, 4, 3, 2, 1, 0)


def q(value):
    return value if isinstance(value, Q) else Q(value)


def vec(values):
    return tuple(q(value) for value in values)


def zero_vector(n=N):
    return tuple(Q(0) for _ in range(n))


def standard_basis(n=N):
    return [tuple(Q(int(i == j)) for j in range(n)) for i in range(n)]


def dot(left, right):
    assert len(left) == len(right)
    return sum((a * b for a, b in zip(left, right)), Q(0))


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def scale(scalar, vector):
    return tuple(q(scalar) * entry for entry in vector)


def linear_combination(coefficients, rows, n=N):
    result = [Q(0) for _ in range(n)]
    for coefficient, row in zip(coefficients, rows):
        for j, entry in enumerate(row):
            result[j] += coefficient * entry
    return tuple(result)


def rref(rows, ncols=N):
    matrix = [[q(entry) for entry in row] for row in rows]
    assert all(len(row) == ncols for row in matrix)
    pivot_columns = []
    pivot_row = 0
    for column in range(ncols):
        selected = next(
            (i for i in range(pivot_row, len(matrix)) if matrix[i][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot for entry in matrix[pivot_row]]
        for i in range(len(matrix)):
            if i == pivot_row or not matrix[i][column]:
                continue
            factor = matrix[i][column]
            matrix[i] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(matrix[i], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, tuple(pivot_columns)


def row_basis(rows, n=N):
    reduced, _ = rref(rows, n)
    return [tuple(row) for row in reduced if any(row)]


def rank(rows, ncols=N):
    return len(row_basis(rows, ncols))


def nullspace(rows, ncols=N):
    reduced, pivots = rref(rows, ncols)
    pivot_rows = [row for row in reduced if any(row)]
    free_columns = [column for column in range(ncols) if column not in pivots]
    basis = []
    for free in free_columns:
        candidate = [Q(0) for _ in range(ncols)]
        candidate[free] = Q(1)
        for i, pivot in enumerate(pivots):
            candidate[pivot] = -pivot_rows[i][free]
        basis.append(tuple(candidate))
    return basis


def in_span(vector, rows, n=N):
    basis = row_basis(rows, n)
    return rank(basis + [tuple(vector)], n) == len(basis)


def same_subspace(left, right, n=N):
    left_basis = row_basis(left, n)
    right_basis = row_basis(right, n)
    return len(left_basis) == len(right_basis) and all(
        in_span(row, right_basis, n) for row in left_basis
    )


def transpose(rows, ncols=N):
    return [tuple(row[j] for row in rows) for j in range(ncols)]


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def solve_linear(matrix, target, nvars):
    """Return one solution of matrix*x=target, or None."""

    assert len(matrix) == len(target)
    augmented = [list(row) + [q(rhs)] for row, rhs in zip(matrix, target)]
    reduced, pivots = rref(augmented, nvars + 1)
    if any(all(not row[j] for j in range(nvars)) and row[-1] for row in reduced):
        return None
    if nvars in pivots:
        return None
    solution = [Q(0) for _ in range(nvars)]
    for row in reduced:
        pivot = next((j for j in range(nvars) if row[j]), None)
        if pivot is not None:
            solution[pivot] = row[-1]
    assert mat_vec(matrix, tuple(solution)) == tuple(target)
    return tuple(solution)


def intersection_primal(left, right, n=N):
    """Compute row(left) intersect row(right) from equality witnesses.

    If B and C are row bases, solve B^T*a-C^T*c=0 and map every kernel
    vector (a,c) back to a^T B.  This is independent of the annihilator
    identity audited below.
    """

    left_basis = row_basis(left, n)
    right_basis = row_basis(right, n)
    if not left_basis or not right_basis:
        return []
    coefficient_system = []
    for coordinate in range(n):
        coefficient_system.append(
            tuple(row[coordinate] for row in left_basis)
            + tuple(-row[coordinate] for row in right_basis)
        )
    witnesses = nullspace(
        coefficient_system,
        len(left_basis) + len(right_basis),
    )
    vectors = [
        linear_combination(witness[: len(left_basis)], left_basis, n)
        for witness in witnesses
    ]
    return row_basis(vectors, n)


def annihilator(rows, n=N):
    return row_basis(nullspace(rows, n), n)


def j_action(p):
    return tuple(p[index] for index in COMPLEMENT)


def complement_matrix():
    basis = standard_basis()
    return [j_action(row) for row in basis]


def quadratic(p):
    return dot(p, j_action(p))


def augmented_column_rank(u_rows, column):
    u_transpose = transpose(u_rows, N)
    augmented = [row + (entry,) for row, entry in zip(u_transpose, column)]
    return rank(augmented, len(u_rows) + 1)


def ambient_case(u_rows, p, counters):
    assert any(p)
    u_rank = rank(u_rows, N)
    kernel = nullspace(u_rows, N)
    jp = j_action(p)

    # Direct aligned-vector route: p and a kernel basis generate every l.
    generators = [p] + kernel
    witness = next((candidate for candidate in generators if dot(candidate, jp)), None)
    direct_success = witness is not None
    if witness == p:
        kappa = Q(1)
    else:
        kappa = Q(0)
    if witness is not None:
        aligned_difference = add(witness, scale(-kappa, p))
        assert mat_vec(u_rows, aligned_difference) == tuple(Q(0) for _ in u_rows)
        assert dot(witness, jp)

    isotropic = quadratic(p) == 0
    dual_membership = in_span(jp, u_rows, N)
    theorem_failure = isotropic and dual_membership
    assert direct_success == (not theorem_failure)

    rank_equality = augmented_column_rank(u_rows, jp) == u_rank
    assert rank_equality == dual_membership

    if theorem_failure:
        # U^*:K^t -> K^6 is the transpose matrix.
        phi = solve_linear(transpose(u_rows, N), jp, len(u_rows))
        assert phi is not None
        assert quadratic(p) == 0
        # The displayed dual certificate kills a spanning family of all
        # aligned vectors and therefore the whole aligned space.
        for kappa_value in (Q(-3), Q(0), Q(2)):
            for kernel_vector in [zero_vector()] + kernel:
                aligned = add(scale(kappa_value, p), kernel_vector)
                assert dot(aligned, jp) == 0
                assert mat_vec(u_rows, add(aligned, scale(-kappa_value, p))) == tuple(
                    Q(0) for _ in u_rows
                )
        counters["ambient_failures"] += 1
    else:
        counters["ambient_successes"] += 1
        if isotropic:
            counters["rank_drop_repairs"] += 1


def legal_case(u_rows, p, m_rows, counters):
    kernel = nullspace(u_rows, N)
    a_p = row_basis([p] + kernel, N)
    m_space = row_basis(m_rows, N)
    jp = j_action(p)

    # Primal route: explicitly solve l in M and l in A_p.
    legal_aligned = intersection_primal(m_space, a_p, N)
    direct_success = any(dot(candidate, jp) for candidate in legal_aligned)
    direct_failure = not direct_success

    # Dual route: build M^perp + (p^perp intersect im U^*) without using
    # the already-computed legal intersection.
    m_perp = annihilator(m_space, N)
    p_perp = annihilator([p], N)
    image_u_star = row_basis(u_rows, N)
    p_perp_in_image = intersection_primal(p_perp, image_u_star, N)
    theorem_rhs = row_basis(m_perp + p_perp_in_image, N)
    theorem_failure = in_span(jp, theorem_rhs, N)
    assert direct_failure == theorem_failure

    # Stronger subspace replay of equations (29)--(30), not just membership
    # of the single covector Jp.
    direct_annihilator = annihilator(legal_aligned, N)
    assert same_subspace(direct_annihilator, theorem_rhs, N)

    a_p_perp_direct = annihilator(a_p, N)
    assert same_subspace(a_p_perp_direct, p_perp_in_image, N)

    dm = len(m_space)
    da = len(a_p)
    di = len(legal_aligned)
    if dm and di == dm:
        counters["contained_intersections"] += 1
    if dm and da and di == 0:
        counters["nontrivial_zero_intersections"] += 1
    if dm and da and 0 < di < dm and di < da:
        counters["proper_crossings"] += 1
    if dm and da and di == max(0, dm + da - N):
        counters["transverse_intersections"] += 1
    counters["legal_cases"] += 1


def canonical_map(target_rank):
    basis = standard_basis()
    rows = basis[:target_rank]
    if target_rank:
        rows += [
            linear_combination([Q(i + 1) for i in range(target_rank)], rows),
            rows[0],
        ]
    else:
        rows += [zero_vector(), zero_vector()]
    assert rank(rows, N) == target_rank
    return rows


def skew_map(target_rank):
    invertible_rows = [
        vec((1, 2, 0, 0, 0, 0)),
        vec((0, 1, 3, 0, 0, 0)),
        vec((0, 0, 1, -2, 0, 0)),
        vec((0, 0, 0, 1, 5, 0)),
        vec((0, 0, 0, 0, 1, -3)),
        vec((0, 0, 0, 0, 0, 1)),
    ]
    rows = invertible_rows[:target_rank]
    if target_rank:
        rows += [
            linear_combination(
                [Q((-1) ** i * (i + 2)) for i in range(target_rank)], rows
            ),
            scale(Q(-4), rows[-1]),
        ]
    else:
        rows += [zero_vector(), zero_vector(), zero_vector()]
    assert rank(rows, N) == target_rank
    return rows


def distinct_spaces(spaces):
    result = []
    keys = set()
    for rows in spaces:
        basis = row_basis(rows, N)
        key = tuple(basis)
        if key not in keys:
            keys.add(key)
            result.append(basis)
    return result


def legal_spaces(u_rows, p):
    basis = standard_basis()
    kernel = nullspace(u_rows, N)
    a_p = row_basis([p] + kernel, N)
    image = row_basis(u_rows, N)
    spaces = [
        [],
        basis,
        [p],
        kernel,
        a_p,
        image,
        annihilator(a_p, N),
        basis[:1],
        basis[1:2],
        basis[:2],
        basis[2:5],
        [vec((1, 1, 0, 1, 0, 0)), vec((0, 1, 1, 0, 1, 0))],
        [
            vec((1, 2, -1, 0, 0, 1)),
            vec((0, 1, 3, -1, 0, 0)),
            vec((2, 0, 1, 1, 1, 0)),
        ],
    ]
    if a_p:
        spaces.append(a_p[:1])
    if len(a_p) >= 2:
        spaces.append(a_p[:2])
    return distinct_spaces(spaces)


def raw_pair_permanents(first, second):
    pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    return tuple(first[i] * second[j] + first[j] * second[i] for i, j in pairs)


# Sparse polynomials in x0,x1,x2,y0,y1,y2.
def monomial(variable_a, variable_b, coefficient=1):
    exponent = [0] * N
    exponent[variable_a] += 1
    exponent[variable_b] += 1
    return {tuple(exponent): q(coefficient)}


def poly_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            answer[exponent] = answer.get(exponent, Q(0)) + coefficient
            if not answer[exponent]:
                del answer[exponent]
    return answer


def poly_scale(scalar, polynomial):
    return {
        exponent: q(scalar) * coefficient
        for exponent, coefficient in polynomial.items()
        if q(scalar) * coefficient
    }


def poly_multiply(left, right):
    answer = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            answer[exponent] = answer.get(exponent, Q(0)) + (
                left_coefficient * right_coefficient
            )
            if not answer[exponent]:
                del answer[exponent]
    return answer


def linear_form(coefficients, offset):
    polynomial = {}
    for i, coefficient in enumerate(coefficients):
        if coefficient:
            exponent = [0] * N
            exponent[offset + i] = 1
            polynomial[tuple(exponent)] = q(coefficient)
    return polynomial


def poly_evaluate(polynomial, point):
    value = Q(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for coordinate, power in zip(point, exponent):
            term *= coordinate**power
        value += term
    return value


def coordinate_degrees(polynomial):
    return tuple(max(exponent[i] for exponent in polynomial) for i in range(N))


def audit_torus_density_example():
    # H is a nonzero physical bilinear block.
    h = poly_add(
        monomial(0, 3, 1),
        monomial(1, 4, -1),
        monomial(2, 5, 2),
    )

    # p=(a.x)(b.y)+(d.x)(c.y), exactly the raw two-root form (6).
    a_x = linear_form((1, 1, 0), 0)
    b_y = linear_form((0, 1, 1), 3)
    d_x = linear_form((1, 0, 1), 0)
    c_y = linear_form((1, -1, 1), 3)
    p_polynomial = poly_add(
        poly_multiply(a_x, b_y),
        poly_multiply(d_x, c_y),
    )
    product_polynomial = poly_multiply(h, p_polynomial)
    assert h and p_polynomial and product_polynomial

    # A nonzero polynomial of coordinate degrees d_i cannot vanish on a
    # Cartesian grid having d_i+1 distinct field elements in coordinate i.
    # We replay that interpolation witness using only nonzero rational points.
    degrees = coordinate_degrees(product_polynomial)
    grids = [tuple(Q(i + 1) for i in range(degree + 1)) for degree in degrees]
    witness = next(
        (
            point
            for point in product(*grids)
            if poly_evaluate(product_polynomial, point) != 0
        ),
        None,
    )
    assert witness is not None
    assert all(witness)
    assert poly_evaluate(h, witness) != 0
    assert poly_evaluate(p_polynomial, witness) != 0
    assert poly_evaluate(product_polynomial, witness) == (
        poly_evaluate(h, witness) * poly_evaluate(p_polynomial, witness)
    )
    return witness, degrees, len(product_polynomial)


def audit_complementary_form():
    j_matrix = complement_matrix()
    identity = standard_basis()
    assert [j_action(row) for row in j_matrix] == identity
    assert j_matrix == transpose(j_matrix, N)
    for p_entries in product((-2, -1, 0, 1, 2), repeat=N):
        p = vec(p_entries)
        expected = 2 * (p[0] * p[5] + p[1] * p[4] + p[2] * p[3])
        assert quadratic(p) == expected
        weight = vec((2, -1, 3, 0, 4, -2))
        omega_by_complements = sum(
            (weight[index] * p[COMPLEMENT[index]] for index in range(N)), Q(0)
        )
        assert dot(weight, j_action(p)) == omega_by_complements


def audit_raw_isotropic_pattern():
    roots = standard_basis(4)
    p = raw_pair_permanents(roots[0], roots[1])
    assert p == standard_basis()[0]
    assert quadratic(p) == 0

    injective = standard_basis()
    counters = {"ambient_successes": 0, "ambient_failures": 0, "rank_drop_repairs": 0}
    ambient_case(injective, p, counters)
    assert counters["ambient_failures"] == 1

    rank_five = standard_basis()[:5]
    repair = standard_basis()[5]
    assert mat_vec(rank_five, repair) == tuple(Q(0) for _ in rank_five)
    assert dot(repair, j_action(p)) == 1
    ambient_case(rank_five, p, counters)
    assert counters["rank_drop_repairs"] == 1


def main():
    audit_complementary_form()
    audit_raw_isotropic_pattern()
    torus_witness, torus_degrees, torus_terms = audit_torus_density_example()

    maps = []
    for target_rank in range(N + 1):
        maps.append((f"canonical-rank-{target_rank}", canonical_map(target_rank)))
        maps.append((f"skew-rank-{target_rank}", skew_map(target_rank)))
    maps.append(("empty-codomain-rank-0", []))

    counters = {
        "ambient_successes": 0,
        "ambient_failures": 0,
        "rank_drop_repairs": 0,
        "legal_cases": 0,
        "contained_intersections": 0,
        "nontrivial_zero_intersections": 0,
        "proper_crossings": 0,
        "transverse_intersections": 0,
    }

    # Exhaust the 3^6-1 nonzero {-1,0,1} patterns for two representatives of
    # every possible rank.  This includes coordinate and cancellation-based
    # isotropic vectors as well as non-isotropic vectors.
    ambient_patterns = [
        vec(entries) for entries in product((-1, 0, 1), repeat=N) if any(entries)
    ]
    rank_outcomes = {
        target_rank: {"success": 0, "failure": 0} for target_rank in range(N + 1)
    }
    for name, u_rows in maps:
        expected_rank = int(name.rsplit("-", 1)[1])
        assert rank(u_rows, N) == expected_rank
        for p in ambient_patterns:
            ambient_case(u_rows, p, counters)
            outcome = (
                "failure"
                if quadratic(p) == 0 and in_span(j_action(p), u_rows, N)
                else "success"
            )
            rank_outcomes[expected_rank][outcome] += 1

    assert rank_outcomes[0]["failure"] == 0
    assert all(rank_outcomes[target_rank]["success"] for target_rank in range(N + 1))
    assert all(rank_outcomes[target_rank]["failure"] for target_rank in range(1, N + 1))

    hostile_p = [
        vec((1, 0, 0, 0, 0, 0)),
        vec((1, 1, 0, 0, 0, 0)),
        vec((1, 1, 0, 0, -1, 1)),
        vec((1, 0, 0, 0, 0, 1)),
        vec((1, 1, 1, 1, 1, 1)),
        vec((2, -1, 3, 1, -2, 1)),
    ]
    assert quadratic(hostile_p[0]) == 0
    assert quadratic(hostile_p[2]) == 0
    assert quadratic(hostile_p[3]) != 0

    for _, u_rows in maps:
        for p in hostile_p:
            for m_rows in legal_spaces(u_rows, p):
                legal_case(u_rows, p, m_rows, counters)

    assert counters["ambient_successes"] > 0
    assert counters["ambient_failures"] > 0
    assert counters["rank_drop_repairs"] > 0
    assert counters["contained_intersections"] > 0
    assert counters["nontrivial_zero_intersections"] > 0
    assert counters["proper_crossings"] > 0
    assert counters["transverse_intersections"] > 0

    print("NO-IMPORT ALIGNMENT AUDIT PASS")
    print(f"pair order: {PAIR_NAMES}")
    print(
        f"maps checked: {len(maps)} "
        "(at least two representatives at each rank 0..6, including T=0)"
    )
    print(f"ambient p-patterns per map: {len(ambient_patterns)}")
    print(
        "ambient cases: "
        f"{counters['ambient_successes'] + counters['ambient_failures']} "
        f"(success {counters['ambient_successes']}, "
        f"failure {counters['ambient_failures']}, "
        f"isotropic rank-drop repairs {counters['rank_drop_repairs']})"
    )
    print(
        "legal-subspace cases: "
        f"{counters['legal_cases']} "
        f"(contained {counters['contained_intersections']}, "
        f"nontrivial-zero {counters['nontrivial_zero_intersections']}, "
        f"proper-crossing {counters['proper_crossings']}, "
        f"transverse {counters['transverse_intersections']})"
    )
    print(
        "torus interpolation witness: "
        f"{tuple(str(entry) for entry in torus_witness)}, "
        f"degrees {torus_degrees}, product terms {torus_terms}"
    )
    print(
        "scope: finite exact replay only; physical selector/response gates remain open"
    )


if __name__ == "__main__":
    main()
