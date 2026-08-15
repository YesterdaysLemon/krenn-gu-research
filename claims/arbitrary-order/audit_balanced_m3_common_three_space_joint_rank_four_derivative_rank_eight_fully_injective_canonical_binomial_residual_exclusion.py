#!/usr/bin/env python3
"""Independent standard-library audit of the canonical binomial exclusion.

This replay uses only ``Fraction`` arithmetic and standard-library iteration.
It independently checks the exact finite-dimensional interfaces used by the
analytic theorem: the canonical derivative and selected annihilators, the
support-case coefficient algebra behind the zero-pair lemma, all nine
projective flag incidences, the scalar-correct GG identity, the dependent
profiles, and the input handed to the proved S2AL square-image lemma.

The arbitrary-vector support classification and the S2AL impossibility are
analytic arguments owned by the theorem.  This script replays their exact
coefficient interfaces; it does not replace those arguments or enlarge the
claim beyond the exact canonical binomial subcell.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
ROOT_DIM = 3
SOURCE_DIM = 3
ROOT_TRIPLES = tuple(product(reversed(range(ROOT_DIM)), repeat=3))
SOURCE_TRIPLES = tuple(product(reversed(range(SOURCE_DIM)), repeat=3))
PERMUTATIONS = tuple(reversed(tuple(permutations(range(3)))))

Vector = tuple[Q, ...]


def zero(size: int) -> Vector:
    return (Q(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Q(int(candidate == index)) for candidate in range(size))


def add(*vectors: Vector) -> Vector:
    assert vectors
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q, vector: Vector) -> Vector:
    scalar = Q(coefficient)
    return tuple(scalar * entry for entry in vector)


def dot(left: Vector, right: Vector) -> Q:
    return sum(
        (first * second for first, second in zip(left, right, strict=True)),
        Q(0),
    )


def concatenate(*vectors: Vector) -> Vector:
    return tuple(entry for vector in vectors for entry in vector)


def row_rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows if any(row)]
    if not matrix:
        return 0
    pivot_row = 0
    for column in reversed(range(len(matrix[0]))):
        pivot = next(
            (
                candidate
                for candidate in reversed(range(pivot_row, len(matrix)))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for candidate in reversed(range(len(matrix))):
            if candidate == pivot_row or not matrix[candidate][column]:
                continue
            multiplier = matrix[candidate][column]
            matrix[candidate] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[candidate], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def column_rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    return row_rank([list(row) for row in zip(*columns, strict=True)])


def in_span(vector: Vector, columns: tuple[Vector, ...]) -> bool:
    return column_rank((*columns, vector)) == column_rank(columns)


def same_line(first: Vector, second: Vector) -> bool:
    return any(first) and any(second) and column_rank((first, second)) == 1


def root_position(triple: tuple[int, int, int]) -> int:
    return ROOT_TRIPLES.index(triple)


def source_position(triple: tuple[int, int, int]) -> int:
    return SOURCE_TRIPLES.index(triple)


def root_tensor(triple: tuple[int, int, int]) -> Vector:
    return unit(len(ROOT_TRIPLES), root_position(triple))


def source_tensor(left: int, middle: int, right: int) -> Vector:
    return unit(len(SOURCE_TRIPLES), source_position((left, middle, right)))


def split_domain(vector: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(vector) == 9
    return vector[:3], vector[3:6], vector[6:9]


def canonical_derivative(alpha: Q, beta: Q, domain_vector: Vector) -> Vector:
    a, b, c = split_domain(domain_vector)
    values = []
    for i, j, k in ROOT_TRIPLES:
        tangent = a[i] * Q(j == 2) * Q(k == 2)
        tangent -= Q(i == 2) * b[j] * Q(k == 2)
        residual = (
            alpha * Q(i == 0 and j == 0)
            + beta * Q(i == 1 and j == 1)
        ) * c[k]
        values.append(tangent + residual)
    return tuple(values)


def domain_basis_vector(block: int, index: int) -> Vector:
    blocks = [zero(3), zero(3), zero(3)]
    blocks[block] = unit(3, index)
    return concatenate(*blocks)


def check_canonical_derivative_and_annihilators() -> None:
    alpha, beta = Q(2, 3), Q(-5, 7)
    columns = tuple(
        canonical_derivative(alpha, beta, domain_basis_vector(block, index))
        for block in reversed(range(3))
        for index in reversed(range(3))
    )
    assert column_rank(columns) == 8

    e_0, e_1, e_2 = (unit(3, index) for index in range(3))
    n = concatenate(e_2, e_2, zero(3))
    assert not any(canonical_derivative(alpha, beta, n))
    # Rank eight plus this nonzero kernel vector proves that the kernel is
    # exactly its span.
    assert any(n)

    annihilators: list[Vector] = []
    for k in reversed(range(3)):
        annihilators.append(root_tensor((0, 1, k)))
        annihilators.append(root_tensor((1, 0, k)))
        annihilators.append(
            add(
                scale(beta, root_tensor((0, 0, k))),
                scale(-alpha, root_tensor((1, 1, k))),
            )
        )
    assert row_rank([list(row) for row in annihilators]) == 9
    assert all(dot(functional, image) == 0 for functional in annihilators for image in columns)

    # An exact four-space K with N contained in K replays the dimension
    # interface L=N^perp -> H^T(L).  It is a linear-algebra control, not a
    # claimed physical solution.
    k_0 = concatenate(zero(3), zero(3), e_0)
    k_1 = concatenate(zero(3), zero(3), e_1)
    k_2 = concatenate(e_0, zero(3), e_2)
    k_basis = (n, k_0, k_1, k_2)
    assert column_rank(k_basis) == 4
    assert column_rank(
        tuple(canonical_derivative(alpha, beta, vector) for vector in k_basis)
    ) == 3

    a_0 = domain_basis_vector(0, 0)
    a_1 = domain_basis_vector(0, 1)
    a_2 = domain_basis_vector(0, 2)
    b_0 = domain_basis_vector(1, 0)
    b_1 = domain_basis_vector(1, 1)
    b_2 = domain_basis_vector(1, 2)
    c_0 = domain_basis_vector(2, 0)
    c_1 = domain_basis_vector(2, 1)
    c_2 = domain_basis_vector(2, 2)
    l_basis = (c_2, c_1, c_0, b_1, b_0, a_1, a_0, add(a_2, scale(-1, b_2)))
    assert column_rank(l_basis) == 8
    assert all(dot(functional, n) == 0 for functional in l_basis)

    def transpose_row(functional: Vector) -> Vector:
        return tuple(dot(functional, vector) for vector in k_basis)

    l_image = tuple(transpose_row(functional) for functional in l_basis)
    third_image = tuple(transpose_row(functional) for functional in (c_2, c_1, c_0))
    assert column_rank(l_image) == column_rank(third_image) == 3
    assert all(in_span(vector, third_image) for vector in l_image)

    # A separated injective image of K^* makes the determinant interface
    # visible explicitly: H^T(L)=Q and Alt(Q) is nonzero.
    x_0 = pure_source(0, 0)
    y_0 = pure_source(1, 0)
    z_0 = pure_source(2, 0)
    extra = add(pure_source(0, 1), pure_source(1, 1), pure_source(2, 1))
    physical_basis = (extra, x_0, y_0, z_0)
    assert column_rank(physical_basis) == 4

    def embed(functional_on_k: Vector) -> Vector:
        return add(
            *(scale(coefficient, vector) for coefficient, vector in zip(
                functional_on_k, physical_basis, strict=True
            ))
        )

    q_basis = tuple(embed(transpose_row(functional)) for functional in (c_0, c_1, c_2))
    assert column_rank(q_basis) == 3
    assert any(alternating_separated(*q_basis))

    # Replay the selected complete-target coefficient relation and its sign.
    targets = tuple(unit(6, index) for index in range(3))
    corrections = tuple(unit(6, 3 + index) for index in range(3))
    f_0: list[Vector] = []
    f_1: list[Vector] = []
    right_side: list[Vector] = []
    for k in reversed(range(3)):
        value_0 = scale(alpha, corrections[k])
        value_1 = scale(beta, corrections[k])
        if k == 0:
            value_0 = add(value_0, targets[0])
        if k == 1:
            value_1 = add(value_1, targets[1])
        f_0.append(value_0)
        f_1.append(value_1)
        right_side.append(
            add(
                scale(beta * Q(k == 0), targets[0]),
                scale(-alpha * Q(k == 1), targets[1]),
            )
        )
    left_side = tuple(
        add(scale(beta, first), scale(-alpha, second))
        for first, second in zip(f_0, f_1, strict=True)
    )
    assert left_side == tuple(right_side)
    assert column_rank(left_side) == 2


def pure_source(block: int, index: int) -> Vector:
    return unit(9, 3 * block + index)


def permutation_sign(permutation: tuple[int, ...]) -> Q:
    inversions = sum(
        int(permutation[left] > permutation[right])
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return Q(-1 if inversions % 2 else 1)


def polarized_permanent(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = (first, second, third)
    result = [Q(0) for _ in SOURCE_TRIPLES]
    for permutation in PERMUTATIONS:
        left = rows[permutation[0]][:3]
        middle = rows[permutation[1]][3:6]
        right = rows[permutation[2]][6:9]
        for i, j, k in SOURCE_TRIPLES:
            result[source_position((i, j, k))] += left[i] * middle[j] * right[k]
    return tuple(result)


def alternating_separated(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = (first, second, third)
    result = [Q(0) for _ in SOURCE_TRIPLES]
    for permutation in PERMUTATIONS:
        sign = permutation_sign(permutation)
        left = rows[permutation[0]][:3]
        middle = rows[permutation[1]][3:6]
        right = rows[permutation[2]][6:9]
        for i, j, k in SOURCE_TRIPLES:
            result[source_position((i, j, k))] += (
                sign * left[i] * middle[j] * right[k]
            )
    return tuple(result)


def permanent_map(first: Vector, second: Vector, q_basis: tuple[Vector, ...]) -> tuple[Vector, ...]:
    return tuple(
        polarized_permanent(first, second, q)
        for q in reversed(q_basis)
    )


def assert_single_tensor(value: Vector, triple: tuple[int, int, int], coefficient: Q) -> None:
    assert value == scale(coefficient, source_tensor(*triple))


def check_zero_pair_support_algebra() -> None:
    x = pure_source(0, 0)
    x_prime = pure_source(0, 1)
    y = pure_source(1, 1)
    y_prime = pure_source(1, 0)
    z = pure_source(2, 2)
    z_prime = pure_source(2, 0)
    u = add(x, y)
    conjugate = add(x, scale(-1, y))
    q_basis = (u, conjugate, z)
    assert column_rank(q_basis) == 3
    assert any(alternating_separated(*q_basis))
    assert not any(entry for q in reversed(q_basis) for entry in polarized_permanent(u, conjugate, q))

    square_u = permanent_map(u, u, q_basis)
    square_conjugate = permanent_map(conjugate, conjugate, q_basis)
    assert column_rank(square_u) == column_rank(square_conjugate) == 1
    assert square_u == tuple(scale(-1, column) for column in square_conjugate)

    # The radical map Q -> Hom(Q,XYZ) has rank two and the displayed
    # conjugate is its unique projective kernel direction.
    radical_columns = tuple(
        concatenate(
            *(polarized_permanent(u, candidate, q) for q in reversed(q_basis))
        )
        for candidate in reversed(q_basis)
    )
    assert column_rank(radical_columns) == 2
    assert not any(radical_columns[1])

    # Pure-support branch: q=v exposes the product of the two other source
    # components; if one vanishes, a complementary q exposes the survivor.
    general_v = add(x_prime, scale(2, y), scale(3, z))
    assert_single_tensor(
        polarized_permanent(x, general_v, general_v),
        (0, 1, 2),
        Q(12),
    )
    no_y = add(x_prime, scale(3, z))
    no_z = add(x_prime, scale(2, y))
    assert_single_tensor(polarized_permanent(x, no_y, y), (0, 1, 2), Q(3))
    assert_single_tensor(polarized_permanent(x, no_z, z), (0, 1, 2), Q(2))

    # Three-support branch.  These are the exact coefficient identities used
    # by the written support proof; its arbitrary-vector quotient argument is
    # deliberately not replaced by finite sampling here.
    u_three = add(x, y, z)
    samples = (
        (Q(5), Q(-2), Q(7), Q(3), Q(-4), Q(2)),
        (Q(2), Q(3), Q(-5), Q(-1), Q(6), Q(4)),
        (Q(-3), Q(8), Q(1), Q(5), Q(2), Q(-7)),
    )
    for a, b, c, coefficient_x, coefficient_y, coefficient_z in reversed(samples):
        v = add(scale(a, x), scale(b, y), scale(c, z))
        q = add(
            scale(coefficient_x, x),
            scale(coefficient_y, y),
            scale(coefficient_z, z),
        )
        assert_single_tensor(
            polarized_permanent(u_three, v, u_three),
            (0, 1, 2),
            2 * (a + b + c),
        )
        assert_single_tensor(
            polarized_permanent(u_three, v, v),
            (0, 1, 2),
            2 * (a * b + a * c + b * c),
        )
        assert_single_tensor(
            polarized_permanent(u_three, v, q),
            (0, 1, 2),
            coefficient_x * (b + c)
            + coefficient_y * (a + c)
            + coefficient_z * (a + b),
        )

    for a, b, c in reversed(((Q(1), Q(2), Q(-3)), (Q(2), Q(3), Q(-5)))):
        assert a + b + c == 0
        assert a and b and c
        v = add(scale(a, x), scale(b, y), scale(c, z))
        assert_single_tensor(
            polarized_permanent(u_three, v, x_prime),
            (1, 1, 2),
            -a,
        )
        assert_single_tensor(
            polarized_permanent(u_three, v, y_prime),
            (0, 0, 2),
            -b,
        )
        assert_single_tensor(
            polarized_permanent(u_three, v, z_prime),
            (0, 1, 0),
            -c,
        )


def flag(kind: str, direction: Vector, common: Vector) -> tuple[Vector, Vector]:
    if kind == "R":
        return common, direction
    if kind == "P":
        return direction, common
    assert kind == "G"
    return direction, add(direction, common)


def check_flag_incidence_and_cross_ratio() -> None:
    a_direction = unit(3, 0)
    b_direction = unit(3, 1)
    common = unit(3, 2)
    expected = {
        "RR": common,
        "PP": common,
        "RG": b_direction,
        "GR": a_direction,
        "PG": add(b_direction, common),
        "GP": add(a_direction, common),
    }
    cases = []
    for first_kind, second_kind in product(reversed(("R", "P", "G")), repeat=2):
        key = first_kind + second_kind
        r_0, p_0 = flag(first_kind, a_direction, common)
        r_1, p_1 = flag(second_kind, b_direction, common)
        d_0, d_1 = (r_0, p_0), (r_1, p_1)
        cross_01, cross_10 = (r_0, p_1), (r_1, p_0)
        assert column_rank(d_0) == column_rank(d_1) == 2
        assert column_rank((*d_0, *d_1)) == 3
        assert in_span(common, d_0) and in_span(common, d_1)
        cases.append(key)

        if key in expected:
            intersection = expected[key]
            assert column_rank(cross_01) == column_rank(cross_10) == 2
            assert column_rank((*cross_01, *cross_10)) == 3
            assert in_span(intersection, cross_01)
            assert in_span(intersection, cross_10)
            assert any(
                same_line(intersection, generator)
                for generator in (*cross_01, *cross_10)
            )
        elif key in ("RP", "PR"):
            ranks = (column_rank(cross_01), column_rank(cross_10))
            assert sorted(ranks) == [1, 2]
        else:
            assert key == "GG"
            intersection = add(a_direction, b_direction, common)
            assert column_rank(cross_01) == column_rank(cross_10) == 2
            assert column_rank((*cross_01, *cross_10)) == 3
            assert in_span(intersection, cross_01)
            assert in_span(intersection, cross_10)
    assert sorted(cases) == sorted(
        first + second for first, second in product(("R", "P", "G"), repeat=2)
    )

    # The continuous target covector modulus is not normalized away.  Every
    # invertible small rational 2 x 2 coefficient matrix, including all zero
    # entry walls, retains rank two; ad != bc is exactly chi != [1:1].
    alpha, beta = Q(2, 3), Q(-5, 7)
    target_0, target_1 = unit(2, 0), unit(2, 1)
    checked = 0
    values = tuple(Q(value) for value in reversed((-2, -1, 0, 1, 2)))
    for a, b, c, d in product(values, repeat=4):
        determinant = a * d - b * c
        if not determinant:
            continue
        lambda_0 = (a, b, Q(0))
        lambda_1 = (c, d, Q(0))
        target_map = tuple(
            add(
                scale(beta * lambda_0[index], target_0),
                scale(-alpha * lambda_1[index], target_1),
            )
            for index in reversed(range(3))
        )
        assert column_rank(target_map) == 2
        assert (a * d, b * c) != (Q(0), Q(0))
        assert a * d != b * c
        checked += 1
    assert checked > 100


def check_rp_and_scalar_correct_gg() -> None:
    x = pure_source(0, 0)
    y = pure_source(1, 1)
    z = pure_source(2, 2)

    # RP and PR: the dependent cross pair is a pure square zero, while the
    # other pair is conjugate in the two complementary sources.  Both
    # diagonal maps consequently use the same source tensor line.
    a_direction = add(x, y)
    b_direction = add(x, scale(-1, y))
    common = z
    q_basis = (a_direction, b_direction, common)
    assert any(alternating_separated(*q_basis))
    for reverse_roles in reversed((False, True)):
        if reverse_roles:
            r_0, p_0 = a_direction, common
            r_1, p_1 = common, b_direction
        else:
            r_0, p_0 = common, a_direction
            r_1, p_1 = b_direction, common
        assert not any(
            entry
            for q in reversed(q_basis)
            for entry in polarized_permanent(r_0, p_1, q)
        )
        assert not any(
            entry
            for q in reversed(q_basis)
            for entry in polarized_permanent(r_1, p_0, q)
        )
        f_0 = permanent_map(r_0, p_0, q_basis)
        f_1 = permanent_map(r_1, p_1, q_basis)
        assert column_rank(f_0) == column_rank(f_1) == 1
        assert column_rank((*f_0, *f_1)) == 1

    # A concrete GG zero-pair configuration checks both signs and the
    # projective row scalars.  The exact identity uses F0/(ab)+F1/(de), not
    # the unscaled literal sum.
    a_direction = add(x, y)
    b_direction = add(x, z)
    common = add(scale(-1, y), scale(-1, z))
    q_basis = (a_direction, b_direction, common)
    assert column_rank(q_basis) == 3
    assert any(alternating_separated(*q_basis))
    row_a, row_b, row_d, row_e = Q(2, 3), Q(-5, 4), Q(7, 6), Q(9, 5)
    r_0 = scale(row_a, a_direction)
    p_0 = scale(row_b, add(a_direction, common))
    r_1 = scale(row_d, b_direction)
    p_1 = scale(row_e, add(b_direction, common))
    assert not any(
        entry
        for q in reversed(q_basis)
        for entry in polarized_permanent(r_0, p_1, q)
    )
    assert not any(
        entry
        for q in reversed(q_basis)
        for entry in polarized_permanent(r_1, p_0, q)
    )
    f_0 = permanent_map(r_0, p_0, q_basis)
    f_1 = permanent_map(r_1, p_1, q_basis)
    normalized_sum = tuple(
        add(
            scale(1 / (row_a * row_b), first),
            scale(1 / (row_d * row_e), second),
        )
        for first, second in zip(f_0, f_1, strict=True)
    )
    square = permanent_map(
        add(a_direction, scale(-1, b_direction)),
        add(a_direction, scale(-1, b_direction)),
        q_basis,
    )
    assert normalized_sum == square


def check_dependent_profiles_and_s2al_interface() -> None:
    x = pure_source(0, 0)
    y = pure_source(1, 1)
    z = pure_source(2, 2)
    u = add(x, y)
    conjugate = add(x, scale(-1, y))
    q_basis = (u, conjugate, z)
    assert any(alternating_separated(*q_basis))

    radical_columns = tuple(
        concatenate(
            *(polarized_permanent(u, candidate, q) for q in reversed(q_basis))
        )
        for candidate in reversed(q_basis)
    )
    assert column_rank(radical_columns) == 2
    assert len(q_basis) - column_rank(radical_columns) == 1
    # Thus a line generator cannot cross-annihilate an independent two-plane:
    # this is the exact (1,2)/(2,1) interface.

    pure_square = permanent_map(x, x, (x, y, z))
    assert not any(entry for column in pure_square for entry in column)

    square_u = permanent_map(u, u, q_basis)
    square_conjugate = permanent_map(conjugate, conjugate, q_basis)
    assert column_rank(square_u) == column_rank(square_conjugate) == 1
    assert column_rank((*square_u, *square_conjugate)) == 1
    # These are respectively the proportional and independent (1,1)
    # interfaces: target rank is zero or at most one, never two.

    # S2AL interface from GG.  The theorem proves that the normalized GG sum
    # is a square map.  If the two rank-one summands have independent domain
    # covectors and image lines, that square has the rank-two image plane
    # spanned by two fully transverse decomposable targets.
    target_0 = source_tensor(0, 0, 0)
    target_1 = source_tensor(1, 1, 1)
    tensor_zero = zero(len(SOURCE_TRIPLES))
    first_map = (target_0, tensor_zero, tensor_zero)
    second_map = (tensor_zero, target_1, tensor_zero)
    square_interface = tuple(
        add(first, second)
        for first, second in zip(first_map, second_map, strict=True)
    )
    assert column_rank(first_map) == column_rank(second_map) == 1
    assert column_rank(square_interface) == 2
    assert in_span(target_0, square_interface)
    assert in_span(target_1, square_interface)
    assert all(first != second for first, second in zip((0, 0, 0), (1, 1, 1), strict=True))


def main() -> None:
    check_canonical_derivative_and_annihilators()
    check_zero_pair_support_algebra()
    check_flag_incidence_and_cross_ratio()
    check_rp_and_scalar_correct_gg()
    check_dependent_profiles_and_s2al_interface()
    print("canonical derivative/kernel and selected annihilators: PASS")
    print("reversed-order zero-pair support coefficient interfaces: PASS")
    print("all 9 projective flags and retained cross-ratio walls: PASS")
    print("scalar-correct RP/GG and dependent-profile interfaces: PASS")
    print("rank-two transverse square input to analytic S2AL lemma: PASS")
    print("scope: exact canonical binomial subcell only; analytic support lemmas retained")


if __name__ == "__main__":
    main()
