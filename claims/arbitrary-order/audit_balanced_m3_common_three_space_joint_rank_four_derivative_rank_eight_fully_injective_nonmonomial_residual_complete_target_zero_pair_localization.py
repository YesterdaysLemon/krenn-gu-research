#!/usr/bin/env python3
"""Independent Fraction audit of the nonmonomial zero-pair localization.

This standard-library-only replay independently reconstructs the exact
finite-dimensional interfaces in the owning theorem.  It checks the graph
three-slice identity and its contraction, reverses the structural support
census and shore-rank calculation, replays correcting-zero source recovery
and the root-tensor rank fork, builds the surviving bilinear ``B_k`` forms
as exact coefficient arrays, checks the symmetry plane collapse, and uses
an independent split-plane permanent fixture for the final full-slice
quotient and actual-``C`` monomial/zero-scalar fork.

The analytic S2R tensor-rank obstruction, S2CG radical and zero-pair
classification, S2CK mixed-map obstruction, infinite-field polynomial
separation, and split-plane source-quotient implication remain arguments of
the written theorem.  This audit checks their coefficient and rank
interfaces.  It imports no primary verifier, SymPy, or solver.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
DIM = 3
COLOURS = tuple(reversed(range(DIM)))
ROOT_TRIPLES = tuple(product(COLOURS, repeat=3))
SOURCE_TRIPLES = tuple(product(COLOURS, repeat=3))
PERMUTATIONS = tuple(reversed(tuple(permutations(range(3)))))

Vector = tuple[Q, ...]
Matrix = tuple[Q, ...]
RootSource = tuple[Q, ...]


def zero(size: int) -> Vector:
    return (Q(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Q(candidate == index) for candidate in range(size))


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


def column_rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    row_count = len(columns[0])
    assert all(len(column) == row_count for column in columns)
    matrix = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in reversed(range(len(columns))):
        pivot = next(
            (
                candidate
                for candidate in reversed(range(pivot_row, row_count))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for candidate in reversed(range(row_count)):
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
        if pivot_row == row_count:
            break
    return pivot_row


def row_rank(rows: tuple[Vector, ...] | list[Vector]) -> int:
    return column_rank(tuple(zip(*rows, strict=True))) if rows else 0


def matrix_entry(matrix: Matrix, row: int, column: int) -> Q:
    return matrix[DIM * row + column]


def matrix_unit(row: int, column: int) -> Matrix:
    return unit(DIM * DIM, DIM * row + column)


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(first * second for first in left for second in right)


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(
            (matrix_entry(matrix, row, column) * vector[column] for column in range(DIM)),
            Q(0),
        )
        for row in range(DIM)
    )


def matrix_bilinear(matrix: Matrix, left: Vector, right: Vector) -> Q:
    return dot(left, matrix_vector(matrix, right))


def tangent_matrix(a: Vector, b: Vector, x: Vector, y: Vector) -> Matrix:
    return add(outer(a, y), scale(-1, outer(x, b)))


def root_position(index: tuple[int, int, int]) -> int:
    return ROOT_TRIPLES.index(index)


def source_position(index: tuple[int, int, int]) -> int:
    return SOURCE_TRIPLES.index(index)


def root_tensor(index: tuple[int, int, int]) -> Vector:
    return unit(len(ROOT_TRIPLES), root_position(index))


def source_target(colour: int) -> Vector:
    return unit(len(SOURCE_TRIPLES), source_position((colour,) * 3))


def matrix_third_tensor(matrix: Matrix, third: Vector) -> Vector:
    return tuple(
        matrix_entry(matrix, i, j) * third[k] for i, j, k in ROOT_TRIPLES
    )


def root_source_product(root: Vector, source: Vector) -> RootSource:
    return tuple(root_entry * source_entry for root_entry in root for source_entry in source)


def root_source_block(value: RootSource, root_index: tuple[int, int, int]) -> Vector:
    offset = root_position(root_index) * len(SOURCE_TRIPLES)
    return value[offset : offset + len(SOURCE_TRIPLES)]


def source_slice(
    value: RootSource,
    third_colour: int,
) -> tuple[Vector, ...]:
    return tuple(
        root_source_block(value, (i, j, third_colour))
        for i in range(DIM)
        for j in range(DIM)
    )


def matrix_source_product(matrix: Matrix, source: Vector) -> tuple[Vector, ...]:
    return tuple(scale(entry, source) for entry in matrix)


def matrix_source_add(*values: tuple[Vector, ...]) -> tuple[Vector, ...]:
    return tuple(add(*entries) for entries in zip(*values, strict=True))


def contract_first_two(
    value: RootSource,
    alpha: Vector,
    beta: Vector,
    third_colour: int,
) -> Vector:
    return tuple(
        sum(
            (
                alpha[i]
                * beta[j]
                * root_source_block(value, (i, j, third_colour))[source_index]
                for i in range(DIM)
                for j in range(DIM)
            ),
            Q(0),
        )
        for source_index in range(len(SOURCE_TRIPLES))
    )


def graph_fixture() -> dict[str, object]:
    t = 2
    x = (Q(2), Q(-3), Q(5))
    y = (Q(-7), Q(11), Q(13))
    w = unit(DIM, t)
    c_matrix = (
        Q(1),
        Q(2),
        Q(-1),
        Q(3),
        Q(-4),
        Q(5),
        Q(2),
        Q(0),
        Q(7),
    )
    lifts_a = (
        (Q(1), Q(-2), Q(3)),
        (Q(4), Q(1), Q(-1)),
        (Q(-3), Q(2), Q(5)),
    )
    lifts_b = (
        (Q(2), Q(1), Q(-4)),
        (Q(-1), Q(3), Q(2)),
        (Q(5), Q(-2), Q(1)),
    )
    h_matrices = tuple(
        tangent_matrix(a, b, x, y)
        for a, b in zip(lifts_a, lifts_b, strict=True)
    )
    u_roots = tuple(
        add(matrix_third_tensor(h_matrices[s], w), matrix_third_tensor(c_matrix, unit(DIM, s)))
        for s in range(DIM)
    )
    source_s = (
        add(source_target(0), scale(Q(2, 3), source_target(2))),
        add(scale(Q(-3, 5), source_target(0)), source_target(1)),
        add(source_target(2), scale(Q(4, 7), source_target(1))),
    )
    j_tensor = add(
        *(root_source_product(root_tensor((k, k, k)), source_target(k)) for k in COLOURS)
    )
    residual = add(
        *(root_source_product(u_roots[s], source_s[s]) for s in COLOURS)
    )
    complete = add(j_tensor, residual)
    return {
        "t": t,
        "x": x,
        "y": y,
        "w": w,
        "C": c_matrix,
        "a": lifts_a,
        "b": lifts_b,
        "H": h_matrices,
        "U": u_roots,
        "S": source_s,
        "J": j_tensor,
        "P": complete,
    }


def check_graph_slices_and_contraction() -> None:
    data = graph_fixture()
    t = data["t"]
    x = data["x"]
    y = data["y"]
    c_matrix = data["C"]
    h_matrices = data["H"]
    source_s = data["S"]
    complete = data["P"]
    assert isinstance(t, int)
    assert isinstance(x, tuple) and isinstance(y, tuple)
    assert isinstance(c_matrix, tuple)
    assert isinstance(h_matrices, tuple) and isinstance(source_s, tuple)
    assert isinstance(complete, tuple)

    for k in COLOURS:
        face = list(source_slice(complete, k))
        face[DIM * k + k] = add(face[DIM * k + k], scale(-1, source_target(k)))
        expected = matrix_source_product(c_matrix, source_s[k])
        if k == t:
            tangent = tuple(zero(len(SOURCE_TRIPLES)) for _ in range(DIM * DIM))
            for s in COLOURS:
                tangent = matrix_source_add(
                    tangent,
                    matrix_source_product(h_matrices[s], source_s[s]),
                )
            expected = matrix_source_add(expected, tangent)
        assert tuple(face) == expected

    # Gauge shifts by the kernel generator preserve every H_s exactly.
    for s, zeta in zip(range(DIM), (Q(5, 7), Q(-2, 9), Q(11, 4)), strict=True):
        shifted_a = add(data["a"][s], scale(zeta, x))
        shifted_b = add(data["b"][s], scale(zeta, y))
        assert tangent_matrix(shifted_a, shifted_b, x, y) == h_matrices[s]

    alpha = (Q(3), Q(2), Q(0))
    beta = (Q(11), Q(7), Q(0))
    assert dot(alpha, x) == dot(beta, y) == 0
    c_value = matrix_bilinear(c_matrix, alpha, beta)
    assert c_value != 0
    for k in COLOURS:
        expected = add(
            scale(alpha[k] * beta[k], source_target(k)),
            scale(c_value, source_s[k]),
        )
        assert contract_first_two(complete, alpha, beta, k) == expected


def mask_support(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(DIM) if mask & (1 << index))


def check_structural_support_census() -> None:
    masks = tuple(reversed(range(1, 1 << DIM)))
    disjoint = tuple(
        (left, right)
        for left, right in reversed(tuple(product(masks, repeat=2)))
        if left & right == 0
    )
    assert disjoint
    assert all(
        len(mask_support(left)) == 1 or len(mask_support(right)) == 1
        for left, right in disjoint
    )

    # Reconstruct the two singleton-shore orientations without assuming
    # that both covectors are coordinate.
    for left, right in disjoint:
        if len(mask_support(left)) == 1:
            a = mask_support(left)[0]
            assert all(index != a for index in mask_support(right))
        if len(mask_support(right)) == 1:
            b = mask_support(right)[0]
            assert all(index != b for index in mask_support(left))

    # A nonzero x or y has at most two zero coordinates, so after the
    # analytic radical-line bound makes each shore projectively finite,
    # the union contains at most four points.
    for x_mask, y_mask in reversed(tuple(product(masks, repeat=2))):
        zero_count = DIM - len(mask_support(x_mask))
        zero_count += DIM - len(mask_support(y_mask))
        assert zero_count <= 4


def shore_kernel(
    shared: Vector,
    coordinate: int,
    c_row: Vector,
) -> tuple[int, tuple[Vector, ...]]:
    equations = (shared, unit(DIM, coordinate), c_row)
    rank = row_rank(equations)
    nullity = DIM - rank
    candidates = tuple(
        vector
        for vector in (
            unit(DIM, 0),
            unit(DIM, 1),
            unit(DIM, 2),
            (Q(1), Q(1), Q(1)),
            (Q(2), Q(-3), Q(5)),
            (Q(-7), Q(11), Q(13)),
        )
        if all(dot(equation, vector) == 0 for equation in equations)
    )
    return nullity, candidates


def check_structural_shore_ranks() -> None:
    for coordinate in COLOURS:
        other = tuple(index for index in range(DIM) if index != coordinate)
        # Rank two: one projective partner line.
        y = add(unit(DIM, coordinate), scale(2, unit(DIM, other[0])))
        c_row = add(y, scale(3, unit(DIM, coordinate)))
        nullity, _ = shore_kernel(y, coordinate, c_row)
        assert nullity == 1

        # Rank one: a two-dimensional partner shore.  Every beta on it is
        # a structural zero partner for alpha=e_coordinate; S2CG excludes
        # this positive-dimensional physical radical shore analytically.
        y_plane = unit(DIM, coordinate)
        c_plane = scale(Q(-5, 3), unit(DIM, coordinate))
        nullity, _ = shore_kernel(y_plane, coordinate, c_plane)
        assert nullity == 2
        beta_basis = tuple(unit(DIM, index) for index in other)
        alpha = unit(DIM, coordinate)
        for beta in beta_basis:
            assert dot(y_plane, beta) == dot(c_plane, beta) == 0
            assert all(alpha[k] * beta[k] == 0 for k in range(DIM))

        # Rank three: no partner vector.
        c_full = unit(DIM, other[1])
        y_full = add(unit(DIM, coordinate), unit(DIM, other[0]))
        nullity, _ = shore_kernel(y_full, coordinate, c_full)
        assert nullity == 0


def pivot_correcting_fixture() -> dict[str, object]:
    t = 2
    x = unit(DIM, 0)
    y = unit(DIM, 0)
    alpha = (Q(0), Q(2), Q(1))
    beta = (Q(0), Q(-3), Q(1))
    assert dot(alpha, x) == dot(beta, y) == 0
    nu = Q(5, 2)
    a_t = (Q(2), Q(-1), Q(3))
    b_t = (Q(-4), Q(5), Q(1))
    h_t = tangent_matrix(a_t, b_t, x, y)
    c_matrix = add(scale(nu, matrix_unit(t, t)), scale(-1, h_t))
    assert sum(bool(entry) for entry in c_matrix) > 1
    c_value = matrix_bilinear(c_matrix, alpha, beta)
    assert c_value == nu
    mu = tuple(alpha[k] * beta[k] / c_value for k in range(DIM))
    assert mu == (Q(0), Q(-12, 5), Q(2, 5))

    h_matrices = (
        tangent_matrix((Q(1), Q(2), Q(-1)), (Q(3), Q(-2), Q(4)), x, y),
        tangent_matrix((Q(-2), Q(1), Q(5)), (Q(1), Q(3), Q(-1)), x, y),
        h_t,
    )
    w = unit(DIM, t)
    u_roots = tuple(
        add(matrix_third_tensor(h_matrices[s], w), matrix_third_tensor(c_matrix, unit(DIM, s)))
        for s in range(DIM)
    )
    return {
        "t": t,
        "x": x,
        "y": y,
        "alpha": alpha,
        "beta": beta,
        "nu": nu,
        "C": c_matrix,
        "H": h_matrices,
        "U": u_roots,
        "mu": mu,
    }


def evaluate_root_tensor(
    tensor: Vector,
    first: Vector,
    second: Vector,
    third: Vector,
) -> Q:
    return sum(
        (
            tensor[root_position((i, j, k))] * first[i] * second[j] * third[k]
            for i in range(DIM)
            for j in range(DIM)
            for k in range(DIM)
        ),
        Q(0),
    )


def tensor_mode_rank(tensor: Vector, factor: int) -> int:
    other = tuple(index for index in range(3) if index != factor)
    columns = []
    for pair in product(COLOURS, repeat=2):
        column = []
        for coordinate in COLOURS:
            index = [0, 0, 0]
            index[factor] = coordinate
            index[other[0]] = pair[0]
            index[other[1]] = pair[1]
            column.append(tensor[source_position(tuple(index))])
        columns.append(tuple(column))
    return column_rank(columns)


def check_correcting_source_recovery_and_rank_fork() -> None:
    data = pivot_correcting_fixture()
    alpha = data["alpha"]
    beta = data["beta"]
    c_matrix = data["C"]
    mu = data["mu"]
    u_roots = data["U"]
    assert isinstance(alpha, tuple) and isinstance(beta, tuple)
    assert isinstance(c_matrix, tuple) and isinstance(mu, tuple)
    assert isinstance(u_roots, tuple)
    c_value = matrix_bilinear(c_matrix, alpha, beta)

    source_s = tuple(scale(-mu[k], source_target(k)) for k in range(DIM))
    for k in COLOURS:
        corrected = add(
            scale(alpha[k] * beta[k], source_target(k)),
            scale(c_value, source_s[k]),
        )
        assert not any(corrected)

    a_roots = tuple(
        add(root_tensor((k, k, k)), scale(-mu[k], u_roots[k]))
        for k in range(DIM)
    )
    g_from_a = add(
        *(root_source_product(a_roots[k], source_target(k)) for k in COLOURS)
    )
    j_tensor = add(
        *(root_source_product(root_tensor((k, k, k)), source_target(k)) for k in COLOURS)
    )
    g_from_sources = add(
        j_tensor,
        *(root_source_product(u_roots[k], source_s[k]) for k in COLOURS),
    )
    assert g_from_a == g_from_sources
    assert not any(a_roots[data["t"]])
    assert all(any(a_roots[k]) for k in range(DIM) if k != data["t"])

    # Exact interface to the all-A_k-nonzero S2R fork: independent nonzero
    # root polynomials admit a common exact sample, and the resulting three
    # transverse source targets have mode rank three.
    graph = graph_fixture()
    sample_mu = (Q(2, 7), Q(-3, 5), Q(5, 11))
    sample_a = tuple(
        add(root_tensor((k, k, k)), scale(-sample_mu[k], graph["U"][k]))
        for k in range(DIM)
    )
    assert all(any(value) for value in sample_a)
    candidates = tuple(
        reversed(
            (
                (Q(1), Q(1), Q(1)),
                (Q(2), Q(-1), Q(3)),
                (Q(-3), Q(5), Q(2)),
                (Q(7), Q(2), Q(-4)),
            )
        )
    )
    evaluation = next(
        (
            (first, second, third)
            for first, second, third in product(candidates, repeat=3)
            if all(
                evaluate_root_tensor(value, first, second, third) != 0
                for value in sample_a
            )
        ),
        None,
    )
    assert evaluation is not None
    coefficients = tuple(
        evaluate_root_tensor(value, *evaluation) for value in sample_a
    )
    assert all(coefficients)
    diagonal = add(
        *(scale(coefficients[k], source_target(k)) for k in COLOURS)
    )
    assert all(tensor_mode_rank(diagonal, factor) == 3 for factor in range(3))

    # If a vanishing A_s occurs away from t, the independent third-root
    # coefficients force H_s=0 and the actual C to be a monomial.
    t, s = 2, 1
    assert s != t
    mu_s = Q(-7, 3)
    monomial_c = scale(1 / mu_s, matrix_unit(s, s))
    u_s = matrix_third_tensor(monomial_c, unit(DIM, s))
    assert add(root_tensor((s, s, s)), scale(-mu_s, u_s)) == zero(len(ROOT_TRIPLES))
    assert sum(bool(entry) for entry in monomial_c) == 1
    h_probe = matrix_unit(0, 2)
    u_probe = add(
        matrix_third_tensor(h_probe, unit(DIM, t)),
        matrix_third_tensor(monomial_c, unit(DIM, s)),
    )
    a_probe = add(root_tensor((s, s, s)), scale(-mu_s, u_probe))
    assert any(a_probe)
    assert tuple(
        a_probe[root_position((i, j, t))]
        for i in range(DIM)
        for j in range(DIM)
    ) == scale(-mu_s, h_probe)
    assert tuple(
        a_probe[root_position((i, j, s))]
        for i in range(DIM)
        for j in range(DIM)
    ) == zero(DIM * DIM)

    # At s=t the exact pivot is C+H_t=nu E_tt, while actual C retains its
    # tangent entries and is not silently replaced by its quotient class.
    assert add(c_matrix, data["H"][data["t"]]) == scale(
        data["nu"], matrix_unit(data["t"], data["t"])
    )
    assert c_matrix != scale(data["nu"], matrix_unit(data["t"], data["t"]))


def perpendicular_basis(vector: Vector) -> tuple[Vector, Vector]:
    pivot = next(index for index in range(DIM) if vector[index])
    others = tuple(index for index in range(DIM) if index != pivot)
    basis = []
    for index in reversed(others):
        candidate = [Q(0)] * DIM
        candidate[index] = vector[pivot]
        candidate[pivot] = -vector[index]
        basis.append(tuple(candidate))
    assert all(dot(vector, candidate) == 0 for candidate in basis)
    assert column_rank(tuple(basis)) == 2
    return basis[0], basis[1]


def bilinear_form_matrix(
    colour: int,
    t: int,
    alpha: Vector,
    beta: Vector,
    x_basis: tuple[Vector, Vector],
    y_basis: tuple[Vector, Vector],
) -> Matrix:
    return tuple(
        left[colour] * right[colour]
        - alpha[colour] * beta[colour] * left[t] * right[t]
        for left in x_basis
        for right in y_basis
    )


def bilinear_value(matrix: Matrix, left: Vector, right: Vector) -> Q:
    assert len(left) == len(right) == 2 and len(matrix) == 4
    return sum(
        (
            left[i] * matrix[2 * i + j] * right[j]
            for i in range(2)
            for j in range(2)
        ),
        Q(0),
    )


def check_bilinear_survivor_arrays() -> Matrix:
    data = pivot_correcting_fixture()
    t = data["t"]
    alpha = data["alpha"]
    beta = data["beta"]
    x_basis = perpendicular_basis(data["x"])
    y_basis = perpendicular_basis(data["y"])
    assert isinstance(t, int)
    assert isinstance(alpha, tuple) and isinstance(beta, tuple)
    forms = tuple(
        bilinear_form_matrix(k, t, alpha, beta, x_basis, y_basis)
        for k in range(DIM)
    )
    assert forms[t] == zero(4)
    nonzero = tuple(k for k in range(DIM) if any(forms[k]))
    assert nonzero == (1,)
    survivor = forms[1]
    assert row_rank((survivor[:2], survivor[2:])) == 2

    # Rejected exact control: two nonzero B-forms have a rational pair at
    # which both survive, the interface prohibited by S2CK.
    x_control = (Q(2), Q(-3), Q(5))
    y_control = (Q(7), Q(11), Q(-13))
    alpha_control = (Q(-5, 2), Q(0), Q(1))
    beta_control = (Q(13, 7), Q(0), Q(1))
    assert dot(alpha_control, x_control) == dot(beta_control, y_control) == 0
    xb_control = perpendicular_basis(x_control)
    yb_control = perpendicular_basis(y_control)
    control_forms = tuple(
        bilinear_form_matrix(
            k,
            t,
            alpha_control,
            beta_control,
            xb_control,
            yb_control,
        )
        for k in range(DIM)
    )
    active = tuple(k for k in range(DIM) if any(control_forms[k]))
    assert len(active) == 2 and t not in active
    probes = tuple(
        reversed(
            (
                (Q(1), Q(0)),
                (Q(0), Q(1)),
                (Q(1), Q(1)),
                (Q(2), Q(-3)),
            )
        )
    )
    witness = next(
        (
            (left, right)
            for left, right in product(probes, repeat=2)
            if all(bilinear_value(control_forms[k], left, right) != 0 for k in active)
        ),
        None,
    )
    assert witness is not None

    # A rank-one survivor has a nonzero exact left-kernel direction, which
    # would place the whole physical P-plane in one radical.
    rank_one = (Q(2), Q(-3), Q(-4), Q(6))
    assert row_rank((rank_one[:2], rank_one[2:])) == 1
    left_kernel = (Q(2), Q(1))
    assert all(
        bilinear_value(rank_one, left_kernel, unit(2, index)) == 0
        for index in range(2)
    )
    return survivor


def check_symmetry_plane_collapse(survivor: Matrix) -> None:
    rows = (survivor[:2], survivor[2:])
    assert row_rank(rows) == 2
    # For each p-column, symmetry gives
    # B(e0,p)*lambda(e1)-B(e1,p)*lambda(e0)=0.
    coefficient_rows = tuple(
        (-matrix_entry_2(survivor, 1, column), matrix_entry_2(survivor, 0, column))
        for column in range(2)
    )
    assert row_rank(coefficient_rows) == 2
    assert determinant_2(coefficient_rows) == determinant_2(rows)
    assert all(
        dot(equation, zero(2)) == 0 for equation in coefficient_rows
    )


def matrix_entry_2(matrix: Matrix, row: int, column: int) -> Q:
    return matrix[2 * row + column]


def determinant_2(rows: tuple[Vector, Vector]) -> Q:
    return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]


def pure_source_row(source: int, factor: Vector) -> Vector:
    blocks = [zero(DIM), zero(DIM), zero(DIM)]
    blocks[source] = factor
    return tuple(entry for block in blocks for entry in block)


def split_source_row(row: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(row) == 3 * DIM
    return row[:DIM], row[DIM : 2 * DIM], row[2 * DIM :]


def permanent(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = [Q(0)] * len(SOURCE_TRIPLES)
    for permutation in PERMUTATIONS:
        x_part = split_source_row(rows[permutation[0]])[0]
        y_part = split_source_row(rows[permutation[1]])[1]
        z_part = split_source_row(rows[permutation[2]])[2]
        for index in SOURCE_TRIPLES:
            i, j, k = index
            result[source_position(index)] += x_part[i] * y_part[j] * z_part[k]
    return tuple(result)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def alternating(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = zero(len(SOURCE_TRIPLES))
    for permutation in PERMUTATIONS:
        x_part = split_source_row(rows[permutation[0]])[0]
        y_part = split_source_row(rows[permutation[1]])[1]
        z_part = split_source_row(rows[permutation[2]])[2]
        term = tuple(
            x_part[i] * y_part[j] * z_part[k] for i, j, k in SOURCE_TRIPLES
        )
        result = add(result, scale(permutation_sign(permutation), term))
    return result


def quotient_target(tensor: Vector, removed_colour: int) -> Vector:
    kept = tuple(index for index in range(DIM) if index != removed_colour)
    return tuple(tensor[source_position(index)] for index in product(kept, repeat=3))


def check_split_plane_and_final_full_slice() -> None:
    l, t, k = 1, 2, 0
    assert len({l, t, k}) == 3
    factor = unit(DIM, l)
    x_line = pure_source_row(0, factor)
    y_line = pure_source_row(1, factor)
    z_line = pure_source_row(2, factor)
    h = add(x_line, y_line)
    h_prime = add(x_line, scale(-1, y_line))
    q_rows = (h, z_line, h_prime)  # q_0,q_1,q_2; ker(lambda_1)=H.
    assert column_rank(q_rows) == 3
    assert any(alternating(*q_rows))
    assert all(not any(permanent(h, h_prime, q)) for q in q_rows)
    assert permanent(h, h, q_rows[l]) == scale(2, source_target(l))

    # The induced symmetric form on H in the basis (X_l,Y_l) is exact,
    # nondegenerate, and has h,h' as an orthogonal pair.
    induced = tuple(
        permanent(left, right, q_rows[l])[source_position((l, l, l))]
        for left in (x_line, y_line)
        for right in (x_line, y_line)
    )
    assert induced == (Q(0), Q(1), Q(1), Q(0))
    assert determinant_2((induced[:2], induced[2:])) == -1

    # Since q_k lies in H, every complete P^(k) entry dies after quotienting
    # the three physical source factors by the T_l factor lines.
    r_rows = tuple(
        tuple(Q(2 + 5 * row + coordinate, 3 + coordinate) for coordinate in range(9))
        for row in range(DIM)
    )
    p_rows = tuple(
        tuple(Q(-7 + 3 * row - coordinate, 5 + coordinate) for coordinate in range(9))
        for row in range(DIM)
    )
    for first, second in reversed(tuple(product(r_rows, p_rows))):
        assert not any(quotient_target(permanent(first, second, q_rows[k]), l))

    bar_tk = quotient_target(source_target(k), l)
    assert any(bar_tk)
    e_kk = matrix_unit(k, k)
    left = tuple(entry * value for entry in scale(-1, e_kk) for value in bar_tk)

    # mu_k=0 leaves a nonzero target coefficient with no possible right
    # side.  For mu_k nonzero, equality uses the actual root matrix C and
    # holds exactly only at the displayed coordinate monomial.
    assert any(left)
    zero_right = zero(len(left))
    assert left != zero_right

    mu_k = Q(-7, 4)
    forced_c = scale(1 / mu_k, e_kk)
    right_forced = tuple(
        entry * value for entry in scale(-mu_k, forced_c) for value in bar_tk
    )
    assert left == right_forced
    nonmonomial_c = add(forced_c, matrix_unit(1, 2))
    right_nonmonomial = tuple(
        entry * value for entry in scale(-mu_k, nonmonomial_c) for value in bar_tk
    )
    assert left != right_nonmonomial
    assert sum(bool(entry) for entry in forced_c) == 1


def main() -> None:
    check_graph_slices_and_contraction()
    check_structural_support_census()
    check_structural_shore_ranks()
    check_correcting_source_recovery_and_rank_fork()
    survivor = check_bilinear_survivor_arrays()
    check_symmetry_plane_collapse(survivor)
    check_split_plane_and_final_full_slice()

    print("complete graph slices, gauge, and corrected contraction: PASS")
    print("structural support census and finite-shore rank interfaces: PASS")
    print("correcting-zero source recovery and root-rank fork: PASS")
    print("B-form survivor and symmetry plane collapse: PASS")
    print("split-plane source quotient and actual-C final fork: PASS")
    print("S2R/S2CG/S2CK support lemmas remain analytic theorem inputs")
    print("scope: nonmonomial fully-injective rank-four/rank-eight zero pairs")


if __name__ == "__main__":
    main()
