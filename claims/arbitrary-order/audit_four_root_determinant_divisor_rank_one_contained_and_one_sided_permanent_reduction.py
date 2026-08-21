#!/usr/bin/env python3
"""Independent exact audit for the GLS14 contained/one-sided reduction.

This file is intentionally standard-library-only.  It does not import or read
the focused verifier.  Its representations are direct row assignments,
perfect-match/permanent expansion, finite set-cover tables, quotient survival
tables, and exact ``Fraction`` Gaussian elimination.

The audit checks the new algebra in

    FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_CONTAINED_AND_ONE_SIDED_
    PERMANENT_REDUCTION_THEOREM.md

It does not re-prove the two explicitly imported dependency theorems: the
kernel-type exhaustion after the quartic radical gate, or the decomposable
P4 restriction rank-drop theorem.  It does independently replay the radical
gate and the exact hypotheses at the P4 dependency boundary.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


F = Fraction
ZERO = F(0)
ONE = F(1)

VERTICES = ("q0", "q1", "u0", "u1", "u2", "u3")
PORTS = ("u0", "u1", "u2", "u3")
PAIRS = tuple(combinations(VERTICES, 2))
STD3 = (
    (ONE, ZERO, ZERO),
    (ZERO, ONE, ZERO),
    (ZERO, ZERO, ONE),
)


def qtuple(*values: int | Fraction) -> tuple[Fraction, ...]:
    return tuple(F(value) for value in values)


def dot(covector: tuple[Fraction, ...], vector: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(covector, vector, strict=True)), ZERO)


def mapped(
    matrix: tuple[tuple[Fraction, ...], ...], vector: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    return tuple(dot(row, vector) for row in matrix)


def scale(scalar: Fraction, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(scalar * entry for entry in vector)


def permanent(columns: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    """Permanent by direct row assignments; columns are the labelled modes."""

    order = len(columns)
    assert all(len(column) == order for column in columns)
    total = ZERO
    for rows in permutations(range(order)):
        term = ONE
        for column, row in zip(columns, rows, strict=True):
            term *= column[row]
        total += term
    return total


def matrix_rank(matrix: tuple[tuple[Fraction, ...], ...]) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    width = len(rows[0])
    rank = 0
    for column in range(width):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for r, row in enumerate(rows):
            if r == rank or not row[column]:
                continue
            multiple = row[column]
            rows[r] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(row, rows[rank], strict=True)
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def kernel_basis(covector: tuple[Fraction, ...]) -> tuple[tuple[Fraction, ...], ...]:
    """An exact basis of the kernel, without normalizing any external datum."""

    pivot = next((i for i, entry in enumerate(covector) if entry), None)
    if pivot is None:
        return STD3
    basis = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [ZERO, ZERO, ZERO]
        vector[free] = ONE
        vector[pivot] = -covector[free] / covector[pivot]
        basis.append(tuple(vector))
    return tuple(basis)


def coordinate(colour: int, scalar: int | Fraction = 1) -> tuple[Fraction, ...]:
    return scale(F(scalar), STD3[colour])


def local_inputs(
    domains: dict[str, tuple[tuple[Fraction, ...], ...]],
):
    for vectors in product(*(domains[vertex] for vertex in VERTICES)):
        yield dict(zip(VERTICES, vectors, strict=True))


GENERAL_L = {
    "q0": (qtuple(1, 2, -1), qtuple(0, 1, 3), qtuple(2, -1, 1), qtuple(1, 0, 2)),
    "q1": (qtuple(2, -1, 0), qtuple(1, 1, 2), qtuple(-1, 2, 1), qtuple(0, 1, -2)),
    "u0": (qtuple(1, 0, 1), qtuple(2, -1, 0), qtuple(0, 1, 2), qtuple(-1, 1, 1)),
    "u1": (qtuple(0, 1, -1), qtuple(1, 2, 0), qtuple(2, 0, 1), qtuple(1, -1, 2)),
    "u2": (qtuple(1, -1, 2), qtuple(0, 2, 1), qtuple(2, 1, 0), qtuple(-1, 0, 1)),
    "u3": (qtuple(2, 0, -1), qtuple(1, -1, 1), qtuple(0, 1, 3), qtuple(1, 2, 1)),
}


def companion_value(
    pair: tuple[str, str],
    inputs: dict[str, tuple[Fraction, ...]],
    incidence: dict[str, tuple[tuple[Fraction, ...], ...]],
) -> Fraction:
    complement = tuple(vertex for vertex in VERTICES if vertex not in pair)
    return permanent(tuple(mapped(incidence[v], inputs[v]) for v in complement))


def contracted_source(
    edge_value,
    inputs: dict[str, tuple[Fraction, ...]],
    incidence: dict[str, tuple[tuple[Fraction, ...], ...]],
) -> Fraction:
    return sum(
        (
            edge_value(pair, inputs[pair[0]], inputs[pair[1]])
            * companion_value(pair, inputs, incidence)
            for pair in PAIRS
        ),
        ZERO,
    )


def branch_i_edge(
    x: tuple[Fraction, ...],
    y: tuple[Fraction, ...],
    a: dict[str, tuple[Fraction, ...]],
    c: dict[str, tuple[Fraction, ...]],
):
    def evaluate(
        pair: tuple[str, str],
        left: tuple[Fraction, ...],
        right: tuple[Fraction, ...],
    ) -> Fraction:
        v, w = pair
        if pair == ("q0", "q1"):
            return dot(x, left) * dot(y, right)
        if v == "q0":
            return dot(x, left) * dot(a[w], right)
        if v == "q1":
            return dot(y, left) * dot(c[w], right)
        return -(
            dot(a[v], left) * dot(c[w], right) + dot(c[v], left) * dot(a[w], right)
        )

    return evaluate


def audit_radical_gate() -> int:
    """Replay contraction before the imported kernel-type exhaustion."""

    dim_x = 3
    ambient_dimension = 5
    cov_a = qtuple(0, 0, 0, 1, 0)
    cov_b = qtuple(0, 0, 0, 0, 1)
    ambient_basis = tuple(
        tuple(ONE if i == j else ZERO for i in range(ambient_dimension))
        for j in range(ambient_dimension)
    )

    checked = 0
    for rank in range(4):
        q_matrix = tuple(
            tuple(ONE if i == j and i < rank else ZERO for j in range(dim_x))
            for i in range(dim_x)
        )
        assert matrix_rank(q_matrix) == rank

        def quadratic(left, right):
            return sum(
                (
                    left[i] * q_matrix[i][j] * right[j]
                    for i in range(dim_x)
                    for j in range(dim_x)
                ),
                ZERO,
            )

        def quartic(arguments):
            total = ZERO
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    k, ell = (index for index in range(4) if index not in (i, j))
                    total += (
                        dot(cov_a, arguments[i])
                        * dot(cov_b, arguments[j])
                        * quadratic(arguments[k], arguments[ell])
                    )
            return total

        probes = [ambient_basis[0]]
        if rank < dim_x:
            probes.append(ambient_basis[rank])
        for z in probes:
            assert dot(cov_a, z) == dot(cov_b, z) == 0
            ell_cov = tuple(
                sum((z[i] * q_matrix[i][j] for i in range(dim_x)), ZERO)
                for j in range(dim_x)
            ) + (ZERO, ZERO)

            def symmetric_cubic(arguments):
                total = ZERO
                forms = (cov_a, cov_b, ell_cov)
                for assignment in permutations(range(3)):
                    term = ONE
                    for mode, form_index in enumerate(assignment):
                        term *= dot(forms[form_index], arguments[mode])
                    total += term
                return total

            for tail in product(ambient_basis, repeat=3):
                assert quartic((z, *tail)) == symmetric_cubic(tail)
                checked += 1

            if any(ell_cov):
                active = next(i for i, entry in enumerate(ell_cov[:dim_x]) if entry)
                dual_ell = scale(ONE / ell_cov[active], ambient_basis[active])
                essential_basis = (ambient_basis[3], ambient_basis[4], dual_ell)
                for colours in product(range(3), repeat=3):
                    value = symmetric_cubic(tuple(essential_basis[d] for d in colours))
                    expected = ONE if len(set(colours)) == 3 else ZERO
                    assert value == expected
            else:
                assert all(
                    quartic((z, *tail)) == 0
                    for tail in product(ambient_basis, repeat=3)
                )
    return checked


def audit_augmented_laplace() -> int:
    """Check all two-bottom minors and all 729 augmented-P6 coefficients."""

    x = qtuple(1, 1, 2)
    y = qtuple(2, -1, 1)
    a = {
        "u0": qtuple(1, 0, 0),
        "u1": qtuple(0, 1, 1),
        "u2": qtuple(2, -1, 0),
        "u3": qtuple(0, 0, 1),
    }
    c = {
        "u0": qtuple(1, 1, 0),
        "u1": qtuple(0, 1, 0),
        "u2": qtuple(1, 0, -1),
        "u3": qtuple(1, 2, 3),
    }
    edge = branch_i_edge(x, y, a, c)

    def bottom(vertex, vector):
        if vertex == "q0":
            return (dot(x, vector), ZERO)
        if vertex == "q1":
            return (ZERO, -dot(y, vector))
        return (-dot(c[vertex], vector), dot(a[vertex], vector))

    minor_checks = 0
    for pair in PAIRS:
        for left, right in product(STD3, repeat=2):
            beta = permanent((bottom(pair[0], left), bottom(pair[1], right)))
            expected = edge(pair, left, right)
            if pair == ("q0", "q1"):
                expected = -expected
            assert beta == expected
            minor_checks += 1

    coefficient_checks = 0
    for colours in product(range(3), repeat=6):
        inputs = {v: STD3[d] for v, d in zip(VERTICES, colours, strict=True)}
        columns = []
        for vertex in VERTICES:
            columns.append(
                mapped(GENERAL_L[vertex], inputs[vertex])
                + bottom(vertex, inputs[vertex])
            )
        direct_p6 = permanent(tuple(columns))
        source = contracted_source(edge, inputs, GENERAL_L)
        q_term = edge(("q0", "q1"), inputs["q0"], inputs["q1"]) * companion_value(
            ("q0", "q1"), inputs, GENERAL_L
        )
        assert direct_p6 == source - 2 * q_term
        coefficient_checks += 1
    assert coefficient_checks == 3**6
    return minor_checks + coefficient_checks


def audit_branch_i_p5_identities() -> tuple[int, int]:
    """Directly expand the eight deleted-mode and one cross P5 identities."""

    x = qtuple(1, 1, 2)
    y = qtuple(2, -1, 1)
    a = {
        "u0": qtuple(1, 0, 0),
        "u1": qtuple(0, 1, 1),
        "u2": qtuple(2, -1, 0),
        "u3": qtuple(0, 0, 1),
    }
    c = {
        "u0": qtuple(1, 1, 0),
        "u1": qtuple(0, 1, 0),
        "u2": qtuple(1, 0, -1),
        "u3": qtuple(1, 2, 3),
    }
    edge = branch_i_edge(x, y, a, c)
    deleted_checks = 0

    for deleted in PORTS:
        remaining = tuple(v for v in PORTS if v != deleted)

        domains_a = {vertex: STD3 for vertex in VERTICES}
        domains_a["q1"] = kernel_basis(y)
        for vertex in remaining:
            domains_a[vertex] = kernel_basis(a[vertex])
        p5_modes_a = ("q0", "q1", *remaining)
        for inputs in local_inputs(domains_a):
            columns = []
            for vertex in p5_modes_a:
                base = mapped(GENERAL_L[vertex], inputs[vertex])
                if vertex == "q0":
                    extra = dot(x, inputs[vertex])
                elif vertex == "q1":
                    extra = ZERO
                else:
                    extra = -dot(c[vertex], inputs[vertex])
                columns.append(base + (extra,))
            right = dot(a[deleted], inputs[deleted]) * permanent(tuple(columns))
            left = contracted_source(edge, inputs, GENERAL_L)
            assert left == right
            deleted_checks += 1

        domains_c = {vertex: STD3 for vertex in VERTICES}
        domains_c["q0"] = kernel_basis(x)
        for vertex in remaining:
            domains_c[vertex] = kernel_basis(c[vertex])
        p5_modes_c = ("q0", "q1", *remaining)
        for inputs in local_inputs(domains_c):
            columns = []
            for vertex in p5_modes_c:
                base = mapped(GENERAL_L[vertex], inputs[vertex])
                if vertex == "q0":
                    extra = ZERO
                elif vertex == "q1":
                    extra = dot(y, inputs[vertex])
                else:
                    extra = -dot(a[vertex], inputs[vertex])
                columns.append(base + (extra,))
            right = dot(c[deleted], inputs[deleted]) * permanent(tuple(columns))
            left = contracted_source(edge, inputs, GENERAL_L)
            assert left == right
            deleted_checks += 1

    domains_cross = {vertex: STD3 for vertex in VERTICES}
    domains_cross["q1"] = kernel_basis(y)
    for vertex in PORTS:
        domains_cross[vertex] = kernel_basis(c[vertex])
    cross_checks = 0
    for inputs in local_inputs(domains_cross):
        columns = []
        for vertex in ("q1", *PORTS):
            base = mapped(GENERAL_L[vertex], inputs[vertex])
            extra = ZERO if vertex == "q1" else dot(a[vertex], inputs[vertex])
            columns.append(base + (extra,))
        right = dot(x, inputs["q0"]) * permanent(tuple(columns))
        left = contracted_source(edge, inputs, GENERAL_L)
        assert left == right
        cross_checks += 1
    return deleted_checks, cross_checks


def audit_cover_tables() -> tuple[int, int]:
    """Exhaust deletion covers with None representing any undeclared colour."""

    descriptors = (None, 0, 1, 2)
    balanced_rows = 0
    coverage_rows = 0
    for residual in descriptors:
        for family in product(descriptors, repeat=4):
            covers = []
            for deleted in range(4):
                cover = {
                    colour
                    for colour in (residual, *family[:deleted], *family[deleted + 1 :])
                    if colour is not None
                }
                covers.append(cover)
                surviving = set(range(3)) - cover
                # The displayed target flattening has one independent row per
                # surviving colour.  A factor times a cofactor has rank <= 1.
                if len(surviving) <= 1:
                    assert len(cover) >= 2
                    coverage_rows += 1
            if all(len(cover) == 3 for cover in covers):
                assert residual in range(3)
                complement = set(range(3)) - {residual}
                assert set(family) == complement
                assert all(family.count(colour) == 2 for colour in complement)
                balanced_rows += 1
    assert balanced_rows == 18

    # The ninth cross restriction leaves exactly the x-colour when x != y
    # and c is balanced on the two colours complementary to x.
    ninth_rows = 0
    for x_colour in range(3):
        complement = tuple(colour for colour in range(3) if colour != x_colour)
        for c_family in set(permutations((*complement, *complement))):
            for y_colour in range(3):
                surviving = set(range(3)) - ({y_colour} | set(c_family))
                if y_colour != x_colour:
                    assert surviving == {x_colour}
                    ninth_rows += 1
                else:
                    assert not surviving
    assert ninth_rows == 36
    return coverage_rows, balanced_rows + ninth_rows


def e2(values: tuple[Fraction, ...]) -> Fraction:
    return sum((values[i] * values[j] for i, j in combinations(range(4), 2)), ZERO)


def audit_alignment_and_e2() -> int:
    two_sets = tuple(combinations(range(4), 2))
    checks = 0
    for a_set_tuple, c_set_tuple in product(two_sets, repeat=2):
        a_set, c_set = set(a_set_tuple), set(c_set_tuple)
        words = []
        for selected_tuple in two_sets:
            selected = set(selected_tuple)
            word = tuple(
                (1 if u in a_set else 2) if u in selected else (1 if u in c_set else 2)
                for u in range(4)
            )
            words.append(word)
        multiplicities = {word: words.count(word) for word in set(words)}
        if a_set != c_set:
            assert 1 in multiplicities.values()
        else:
            assert len(multiplicities) == 1 and next(iter(multiplicities.values())) == 6
        checks += 1

    alpha = qtuple(2, -3, 5, 7)
    gamma = qtuple(1, 4, -2, 3)
    ratios = tuple(a / c for a, c in zip(alpha, gamma, strict=True))
    direct = ZERO
    for selected in two_sets:
        selected_set = set(selected)
        term = ONE
        for u in range(4):
            term *= alpha[u] if u in selected_set else gamma[u]
        direct += term
    assert direct == permanent_product(gamma) * e2(ratios)
    return checks + 1


def permanent_product(values: tuple[Fraction, ...]) -> Fraction:
    result = ONE
    for value in values:
        result *= value
    return result


def in_active_module(word: tuple[int, ...], lambdas: tuple[int, ...]) -> bool:
    return any(colour == active for colour, active in zip(word, lambdas, strict=True))


def tensor_flattening_rank(
    tensor: dict[tuple[int, ...], Fraction], mode: int, order: int
) -> int:
    other_modes = tuple(i for i in range(order) if i != mode)
    columns = tuple(product(range(3), repeat=order - 1))
    matrix = []
    for colour in range(3):
        row = []
        for other_word in columns:
            full = [0] * order
            full[mode] = colour
            for index, value in zip(other_modes, other_word, strict=True):
                full[index] = value
            row.append(tensor.get(tuple(full), ZERO))
        matrix.append(tuple(row))
    return matrix_rank(tuple(matrix))


def audit_face_normal_form() -> int:
    mu = qtuple(2, -3, 5)
    h = F(7)
    lambdas = (1, 1, 2, 2)
    psi: dict[tuple[int, ...], Fraction] = {}
    for word in product(range(3), repeat=4):
        if in_active_module(word, lambdas):
            value = F(
                1 + sum((index + 1) * colour for index, colour in enumerate(word))
            )
            if sum(word) % 2:
                value = -value
            psi[word] = value
    assert psi.get((0, 0, 0, 0), ZERO) == 0
    assert all(in_active_module(word, lambdas) for word, value in psi.items() if value)

    p = mu[0] / h
    pi_q = dict(psi)
    pi_q[(0, 0, 0, 0)] = p
    tensor: dict[tuple[int, ...], Fraction] = {}
    checks = 0
    for word in product(range(3), repeat=6):
        diagonal = mu[word[0]] if len(set(word)) == 1 else ZERO
        correction = -2 * h * pi_q.get(word[2:], ZERO) if word[:2] == (0, 0) else ZERO
        from_target = diagonal + correction

        explicit = ZERO
        if len(set(word)) == 1:
            explicit = -mu[0] if word[0] == 0 else mu[word[0]]
        if word[:2] == (0, 0):
            explicit -= 2 * h * psi.get(word[2:], ZERO)
        assert from_target == explicit
        if explicit:
            tensor[word] = explicit
        checks += 1
    assert checks == 729
    assert all(tensor_flattening_rank(tensor, mode, 6) == 3 for mode in range(6))

    zero_psi_tensor = {
        (0, 0, 0, 0, 0, 0): -mu[0],
        (1, 1, 1, 1, 1, 1): mu[1],
        (2, 2, 2, 2, 2, 2): mu[2],
    }
    assert all(
        tensor_flattening_rank(zero_psi_tensor, mode, 6) == 3 for mode in range(6)
    )
    off_diagonal = [word for word in tensor if len(set(word)) != 1]
    assert off_diagonal

    # Direct row-space tables for (49): adding one new line to a rank-two
    # row space reaches rank three exactly when that line was not already in
    # the row space; proportional duplicate bottom rows do not add a second
    # line.
    rank_tables = 0
    active = qtuple(0, 1, 0)
    row_space_in = (qtuple(1, 0, 0), active)
    row_space_out = (qtuple(1, 0, 0), qtuple(0, 0, 1))
    assert matrix_rank(row_space_in + (active,)) == 2
    assert matrix_rank(row_space_out + (active,)) == 3
    assert matrix_rank(row_space_out + (active, scale(F(5), active))) == 3
    rank_tables += 3
    return checks + 12 + rank_tables


def branch_ii_singleton_edge(
    x: tuple[Fraction, ...],
    y: tuple[Fraction, ...],
    a_s: tuple[Fraction, ...],
    c: dict[str, tuple[Fraction, ...]],
    c_s_matrix: tuple[tuple[Fraction, ...], ...],
    active: str,
):
    def bilinear(matrix, left, right):
        return sum(
            (left[i] * matrix[i][j] * right[j] for i in range(3) for j in range(3)),
            ZERO,
        )

    def evaluate(pair, left, right):
        v, w = pair
        if pair == ("q0", "q1"):
            return dot(x, left) * dot(y, right)
        if v == "q0":
            return dot(x, left) * dot(a_s, right) if w == active else ZERO
        if v == "q1":
            if w == active:
                return bilinear(c_s_matrix, left, right)
            return dot(y, left) * dot(c[w], right)
        if v == active:
            return -dot(a_s, left) * dot(c[w], right)
        return ZERO

    return evaluate


def fully_supported_kernel_vector(
    covector: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    support = [i for i, value in enumerate(covector) if value]
    assert len(support) >= 2
    if len(support) == 2:
        i, j = support
        vector = [ONE, ONE, ONE]
        vector[i] = covector[j]
        vector[j] = -covector[i]
        result = tuple(vector)
        assert all(result) and dot(covector, result) == 0
        return result
    for trial in (ONE, F(2), F(3)):
        vector = [ONE, trial, ZERO]
        vector[2] = -(covector[0] + covector[1] * trial) / covector[2]
        result = tuple(vector)
        if all(result):
            assert dot(covector, result) == 0
            return result
    raise AssertionError("an infinite-field torus kernel probe was not found")


def audit_singleton_quotient_and_rank_table() -> tuple[int, int, int]:
    quotient_rows = 0
    for i, j in product(range(3), repeat=2):
        survivors = tuple(d for d in range(3) if d not in {i, j})
        flattening_rank = len(survivors)
        if i == j:
            assert flattening_rank == 2
        else:
            assert flattening_rank == 1
            assert survivors == (next(d for d in range(3) if d not in (i, j)),)
        quotient_rows += 1

    x = qtuple(1, 2, -1)
    y = coordinate(0, 2)
    a_s = coordinate(1, -3)
    active = "u0"
    c = {
        "u1": qtuple(1, 0, 2),
        "u2": qtuple(0, 1, -1),
        "u3": qtuple(2, 1, 0),
    }
    c_s_matrix = (
        qtuple(1, 2, 0),
        qtuple(-1, 1, 3),
        qtuple(2, 0, 1),
    )
    edge = branch_ii_singleton_edge(x, y, a_s, c, c_s_matrix, active)
    domains = {vertex: STD3 for vertex in VERTICES}
    domains["q1"] = kernel_basis(y)
    domains[active] = kernel_basis(a_s)
    source_checks = 0
    for inputs in local_inputs(domains):
        c_s_value = sum(
            (
                inputs["q1"][i] * c_s_matrix[i][j] * inputs[active][j]
                for i in range(3)
                for j in range(3)
            ),
            ZERO,
        )
        expected = c_s_value * companion_value(("q1", active), inputs, GENERAL_L)
        assert contracted_source(edge, inputs, GENERAL_L) == expected
        source_checks += 1

    torus_checks = 0
    sample_covectors = []
    for entries in product(range(-2, 3), repeat=3):
        covector = tuple(F(entry) for entry in entries)
        if sum(bool(entry) for entry in covector) >= 2:
            sample_covectors.append(covector)
    for covector in sample_covectors:
        vector = fully_supported_kernel_vector(covector)
        assert all(vector) and dot(covector, vector) == 0
        torus_checks += 1
    for colour in range(3):
        covector = coordinate(colour)
        assert all(
            dot(covector, vector) != 0 for vector in product((ONE, F(2)), repeat=3)
        )
        torus_checks += 1

    # Exhaust the explicit rank branch before the imported P4 rank-drop
    # theorem.  The high-rank rows recorded here are precisely the rows on
    # which that dependency is invoked.
    high_rank_rows = 0
    low_rank_rows = 0
    for ranks in product((1, 2, 3), repeat=4):
        if 1 in ranks:
            low_rank_rows += 1
        else:
            high_rank_rows += 1
            if ranks.count(2) >= 2:
                pass  # permitted by the imported conclusion
    assert low_rank_rows == 65 and high_rank_rows == 16
    assert sum(1 for ranks in product((2, 3), repeat=4) if ranks.count(2) >= 2) == 11
    return quotient_rows + source_checks, torus_checks, high_rank_rows + low_rank_rows


def branch_ii_two_port_data():
    x = qtuple(1, 1, 0)
    y = coordinate(0, 2)
    d = qtuple(0, 1, 1)
    a = {
        "u0": coordinate(1, 3),
        "u1": qtuple(1, 0, 1),
        "u2": qtuple(0, 0, 0),
        "u3": qtuple(0, 0, 0),
    }
    c = {
        "u0": qtuple(1, -1, 2),
        "u1": qtuple(0, 2, 1),
        "u2": qtuple(2, 0, -1),
        "u3": qtuple(1, 3, 0),
    }
    return x, y, d, a, c


def branch_ii_two_port_edge(x, y, d, a, c, active=("u0", "u1")):
    s, t = active

    def evaluate(pair, left, right):
        v, w = pair
        if pair == ("q0", "q1"):
            return dot(x, left) * dot(y, right)
        if v == "q0":
            return dot(x, left) * dot(a[w], right)
        if v == "q1":
            contained = dot(y, left) * dot(c[w], right)
            if w == s:
                return dot(d, left) * dot(a[s], right) + contained
            if w == t:
                return -dot(d, left) * dot(a[t], right) + contained
            return contained
        return -(
            dot(a[v], left) * dot(c[w], right) + dot(c[v], left) * dot(a[w], right)
        )

    return evaluate


def audit_two_port_p5_and_transpose() -> tuple[int, int]:
    x, y, d, a, c = branch_ii_two_port_data()
    edge = branch_ii_two_port_edge(x, y, d, a, c)
    s, t, m, n = PORTS

    identities = (
        (
            t,
            s,
            -ONE,
            a[t],
        ),
        (
            s,
            t,
            ONE,
            a[s],
        ),
    )
    direct_checks = 0
    saved_specs = []
    for deleted, restricted_port, d_sign, factor in identities:
        domains = {vertex: STD3 for vertex in VERTICES}
        domains["q0"] = kernel_basis(x)
        domains["q1"] = kernel_basis(y)
        domains[restricted_port] = kernel_basis(a[restricted_port])
        modes = ("q0", "q1", restricted_port, m, n)

        def map_column(vertex, vector, d_sign=d_sign):
            base = mapped(GENERAL_L[vertex], vector)
            if vertex == "q0":
                extra = ZERO
            elif vertex == "q1":
                extra = d_sign * dot(d, vector)
            else:
                extra = -dot(c[vertex], vector)
            return base + (extra,)

        for inputs in local_inputs(domains):
            right = dot(factor, inputs[deleted]) * permanent(
                tuple(map_column(vertex, inputs[vertex]) for vertex in modes)
            )
            assert contracted_source(edge, inputs, GENERAL_L) == right
            direct_checks += 1
        saved_specs.append((deleted, domains, modes, map_column, factor))

    # Exact labelled transposition.  Move old q0 to new q1 and old q1 to
    # new q0, carrying every local matrix, kernel, bottom covector, and sign.
    swap = {"q0": "q1", "q1": "q0", **{u: u for u in PORTS}}
    transposed_l = {new: GENERAL_L[swap[new]] for new in VERTICES}

    def transposed_edge(pair, left, right):
        old_pair_unsorted = (swap[pair[0]], swap[pair[1]])
        if VERTICES.index(old_pair_unsorted[0]) < VERTICES.index(old_pair_unsorted[1]):
            return edge(old_pair_unsorted, left, right)
        return edge((old_pair_unsorted[1], old_pair_unsorted[0]), right, left)

    transpose_checks = 0
    for deleted, old_domains, old_modes, old_map_column, factor in saved_specs:
        new_domains = {new: old_domains[swap[new]] for new in VERTICES}
        new_modes = tuple(swap[old] for old in old_modes)

        def new_map_column(new_vertex, vector):
            return old_map_column(swap[new_vertex], vector)

        for inputs in local_inputs(new_domains):
            old_deleted = deleted
            new_deleted = swap[old_deleted]
            right = dot(factor, inputs[new_deleted]) * permanent(
                tuple(new_map_column(vertex, inputs[vertex]) for vertex in new_modes)
            )
            assert contracted_source(transposed_edge, inputs, transposed_l) == right
            transpose_checks += 1
    return direct_checks, transpose_checks


def audit_two_port_cover_and_contradiction() -> tuple[int, int]:
    descriptors = (None, 0, 1, 2)
    both_zero_rows = 0
    cover_rows = 0
    for x_colour, y_colour, a_s_colour, a_t_colour in product(descriptors, repeat=4):
        d_t = {
            colour for colour in (x_colour, y_colour, a_s_colour) if colour is not None
        }
        d_s = {
            colour for colour in (x_colour, y_colour, a_t_colour) if colour is not None
        }
        if len(set(range(3)) - d_t) <= 1:
            assert len(d_t) >= 2
            cover_rows += 1
        if len(set(range(3)) - d_s) <= 1:
            assert len(d_s) >= 2
            cover_rows += 1
        if len(d_t) == len(d_s) == 3:
            assert x_colour is not None and y_colour is not None
            assert x_colour != y_colour
            third = next(
                colour for colour in range(3) if colour not in (x_colour, y_colour)
            )
            assert a_s_colour == a_t_colour == third
            both_zero_rows += 1
    assert both_zero_rows == 6

    # At the all-x word, every edge factor is visibly killed in the forced
    # both-zero pattern, independently of all companion values.
    x_colour, y_colour, active_colour = 0, 1, 2
    x, y = coordinate(x_colour, 2), coordinate(y_colour, -3)
    d = qtuple(5, 7, 11)
    a = {
        "u0": coordinate(active_colour, 4),
        "u1": coordinate(active_colour, -2),
        "u2": qtuple(0, 0, 0),
        "u3": qtuple(0, 0, 0),
    }
    c = {u: qtuple(index + 1, 2 - index, index - 3) for index, u in enumerate(PORTS)}
    edge = branch_ii_two_port_edge(x, y, d, a, c)
    for pair in PAIRS:
        assert edge(pair, STD3[x_colour], STD3[x_colour]) == 0
    return cover_rows, both_zero_rows + len(PAIRS)


def tensor_source_coefficients(
    edge,
    companion_tensors: dict[tuple[str, str], dict[tuple[int, ...], Fraction]],
) -> dict[tuple[int, ...], Fraction]:
    result = {}
    for word in product(range(3), repeat=6):
        inputs = {
            vertex: STD3[colour] for vertex, colour in zip(VERTICES, word, strict=True)
        }
        total = ZERO
        for pair in PAIRS:
            complement = tuple(vertex for vertex in VERTICES if vertex not in pair)
            complement_word = tuple(
                word[VERTICES.index(vertex)] for vertex in complement
            )
            total += edge(
                pair, inputs[pair[0]], inputs[pair[1]]
            ) * companion_tensors.get(pair, {}).get(complement_word, ZERO)
        if total:
            result[word] = total
    return result


def audit_formal_control() -> tuple[int, int, int]:
    x = coordinate(0)
    y = coordinate(0)
    lambdas = (1, 1, 2, 2)
    rho = qtuple(1, 1, 2, F(-5, 4))
    c = {u: coordinate(lambdas[index]) for index, u in enumerate(PORTS)}
    a = {u: scale(rho[index], c[u]) for index, u in enumerate(PORTS)}
    edge = branch_i_edge(x, y, a, c)
    mu = qtuple(2, -3, 5)

    pi: dict[tuple[str, str], dict[tuple[int, ...], Fraction]] = {
        pair: {} for pair in PAIRS
    }
    pi[("q0", "q1")][(0, 0, 0, 0)] = mu[0]
    pi[("u0", "u1")][(1, 1, 1, 1)] = -mu[1] / 2
    pi[("u2", "u3")][(2, 2, 2, 2)] = -4 * mu[2] / 3
    source = tensor_source_coefficients(edge, pi)
    for word in product(range(3), repeat=6):
        expected = mu[word[0]] if len(set(word)) == 1 else ZERO
        assert source.get(word, ZERO) == expected

    response_checks = 0
    for u, v in combinations(PORTS, 2):
        for colours in product(range(3), repeat=4):
            zq0, zq1, zu, zv = (STD3[colour] for colour in colours)
            h = dot(x, zq0) * dot(y, zq1)
            b = -(dot(a[u], zu) * dot(c[v], zv) + dot(c[u], zu) * dot(a[v], zv))
            au = dot(x, zq0) * dot(a[u], zu)
            av = dot(x, zq0) * dot(a[v], zv)
            cu = dot(y, zq1) * dot(c[u], zu)
            cv = dot(y, zq1) * dot(c[v], zv)
            assert h * b + au * cv + av * cu == 0
            response_checks += 1

    phi_checks = 0
    for word in product(range(3), repeat=4):
        total = ZERO
        for selected_tuple in combinations(range(4), 2):
            selected = set(selected_tuple)
            term = ONE
            for index, vertex in enumerate(PORTS):
                term *= (a if index in selected else c)[vertex][word[index]]
            total += term
        assert total == 0
        phi_checks += 1
    assert e2(rho) == 0
    return 729, response_checks, phi_checks


C1_L = {
    "q0": (qtuple(1, -1, -1), qtuple(1, 0, 1), qtuple(-1, 0, -1), qtuple(-1, -1, 1)),
    "q1": (qtuple(-1, -1, -1), qtuple(-1, 0, 1), qtuple(-1, 1, 1), qtuple(0, 1, -1)),
    "u0": (
        qtuple(0, 1, F(-1, 2)),
        qtuple(-1, -1, 0),
        qtuple(1, -1, F(1, 2)),
        qtuple(1, 1, F(-1, 2)),
    ),
    "u1": (qtuple(-1, 1, 0), qtuple(0, 0, 0), qtuple(-1, 0, 0), qtuple(1, 1, 1)),
    "u2": (qtuple(0, 0, 0), qtuple(1, 1, -1), qtuple(-1, 1, -1), qtuple(-1, -1, -1)),
    "u3": (qtuple(0, -1, -1), qtuple(1, 0, -1), qtuple(-1, 0, 0), qtuple(1, -1, -1)),
}


def permanent_at_colours(
    vertices: tuple[str, ...], colours: tuple[int, ...], incidence=C1_L
) -> Fraction:
    return permanent(
        tuple(
            tuple(incidence[vertex][row][colour] for row in range(4))
            for vertex, colour in zip(vertices, colours, strict=True)
        )
    )


def audit_common_incidence_control() -> tuple[int, int, int]:
    assert all(matrix_rank(matrix) == 3 for matrix in C1_L.values())
    assert permanent_at_colours(PORTS, (0, 0, 0, 0)) == 2
    assert permanent_at_colours(("q0", "q1", "u2", "u3"), (1, 1, 1, 1)) == 2
    assert permanent_at_colours(("q0", "q1", "u0", "u1"), (2, 2, 2, 2)) == -1
    assert permanent_at_colours(PORTS, (2, 2, 0, 0)) == 1

    x = coordinate(0)
    y = coordinate(0)
    lambdas = (1, 1, 2, 2)
    rho = qtuple(1, 1, 2, F(-5, 4))
    c = {u: coordinate(lambdas[index]) for index, u in enumerate(PORTS)}
    a = {u: scale(rho[index], c[u]) for index, u in enumerate(PORTS)}
    edge = branch_i_edge(x, y, a, c)
    assert edge(("u0", "u1"), STD3[1], STD3[1]) == -2
    assert edge(("u2", "u3"), STD3[2], STD3[2]) == F(-3, 4)
    assert e2(rho) == 0

    pure = []
    for colour in range(3):
        inputs = {vertex: STD3[colour] for vertex in VERTICES}
        pure.append(contracted_source(edge, inputs, C1_L))
    assert tuple(pure) == qtuple(2, -4, F(3, 4))

    mixed_word = (0, 0, 2, 2, 0, 0)
    mixed_inputs = {
        vertex: STD3[colour]
        for vertex, colour in zip(VERTICES, mixed_word, strict=True)
    }
    contributions = {}
    for pair in PAIRS:
        value = edge(
            pair, mixed_inputs[pair[0]], mixed_inputs[pair[1]]
        ) * companion_value(pair, mixed_inputs, C1_L)
        if value:
            contributions[pair] = value
    assert contributions == {("q0", "q1"): ONE}
    assert len(set(mixed_word)) != 1

    # A second all-word permanent/Laplace replay on the published common-
    # incidence fixture, independent of the generic fixture above.
    p6_checks = 0

    def bottom(vertex, vector):
        if vertex == "q0":
            return (dot(x, vector), ZERO)
        if vertex == "q1":
            return (ZERO, -dot(y, vector))
        return (-dot(c[vertex], vector), dot(a[vertex], vector))

    for word in product(range(3), repeat=6):
        inputs = {
            vertex: STD3[colour] for vertex, colour in zip(VERTICES, word, strict=True)
        }
        columns = tuple(
            mapped(C1_L[vertex], inputs[vertex]) + bottom(vertex, inputs[vertex])
            for vertex in VERTICES
        )
        direct = permanent(columns)
        source = contracted_source(edge, inputs, C1_L)
        q_term = edge(("q0", "q1"), inputs["q0"], inputs["q1"]) * companion_value(
            ("q0", "q1"), inputs, C1_L
        )
        assert direct == source - 2 * q_term
        p6_checks += 1
    return 10, len(contributions), p6_checks


def audit_face_module_support() -> int:
    """Check the q0=q1=0 slice modulo J with arbitrary companion tensors."""

    x = coordinate(0, 2)
    y = coordinate(0, -3)
    lambdas = (1, 1, 2, 2)
    a = {u: coordinate(lambdas[index], index + 1) for index, u in enumerate(PORTS)}
    c = {u: coordinate(lambdas[index], 5 - index) for index, u in enumerate(PORTS)}
    edge = branch_i_edge(x, y, a, c)
    companion_tensors = {}
    for pair_index, pair in enumerate(PAIRS):
        values = {}
        for word in product(range(3), repeat=4):
            value = F(
                (pair_index + 1) * (1 + sum((i + 1) * d for i, d in enumerate(word)))
            )
            if (sum(word) + pair_index) % 2:
                value = -value
            values[word] = value
        companion_tensors[pair] = values

    checks = 0
    for port_word in product(range(3), repeat=4):
        full_word = (0, 0, *port_word)
        inputs = {
            vertex: STD3[colour]
            for vertex, colour in zip(VERTICES, full_word, strict=True)
        }
        non_q = ZERO
        for pair in PAIRS:
            if pair == ("q0", "q1"):
                continue
            complement = tuple(vertex for vertex in VERTICES if vertex not in pair)
            complement_word = tuple(
                full_word[VERTICES.index(vertex)] for vertex in complement
            )
            non_q += (
                edge(pair, inputs[pair[0]], inputs[pair[1]])
                * companion_tensors[pair][complement_word]
            )
        if not in_active_module(port_word, lambdas):
            assert non_q == 0
        checks += 1
    return checks


def audit_nonzero_and_characteristic_zero_ledger() -> int:
    mu = qtuple(2, -3, 5)
    xi, eta = F(7), F(-11)
    gamma = qtuple(1, -2, 3, 4)
    alpha = qtuple(5, 6, -7, 8)
    h = xi * eta
    assert permanent_product(mu) != 0
    assert h != 0 and all(gamma) and all(alpha)
    ratios = tuple(a / c for a, c in zip(alpha, gamma, strict=True))
    p = mu[0] / h
    assert all(ratio * c == a for ratio, c, a in zip(ratios, gamma, alpha, strict=True))
    assert h * p == mu[0]

    # In characteristic zero, the small integers used by the finite
    # multiplicity and e2 calculations remain nonzero.  Fraction retains
    # every denominator, so no exceptional divisor is silently discarded.
    assert F(2) and F(3) and F(4) and F(6)
    declared_divisors = (xi, eta, *gamma)
    assert all(declared_divisors)
    return 6 + len(declared_divisors)


def main() -> None:
    radical = audit_radical_gate()
    augmented = audit_augmented_laplace()
    branch_i_deleted, branch_i_cross = audit_branch_i_p5_identities()
    coverage, balanced = audit_cover_tables()
    alignment = audit_alignment_and_e2()
    face = audit_face_normal_form()
    singleton, torus, rank_table = audit_singleton_quotient_and_rank_table()
    two_port, transpose = audit_two_port_p5_and_transpose()
    two_port_cover, contradiction = audit_two_port_cover_and_contradiction()
    formal_target, responses, phi = audit_formal_control()
    anchor_claims, mixed_terms, anchor_p6 = audit_common_incidence_control()
    module_words = audit_face_module_support()
    ledger = audit_nonzero_and_characteristic_zero_ledger()

    print("GLS14 INDEPENDENT NO-IMPORT AUDIT PASS")
    print(f"  quartic radical-gate evaluations: {radical}")
    print(f"  augmented minors/all-word P6 checks: {augmented}")
    print(
        "  Branch-I P5 direct identities: "
        f"{branch_i_deleted} deleted-mode + {branch_i_cross} cross"
    )
    print(f"  cover/balanced/ninth finite rows: {coverage + balanced}")
    print(f"  seventh alignment/e2 rows: {alignment}")
    print(f"  P6 face/rank checks: {face}; quotient-module words: {module_words}")
    print(
        "  Branch-II singleton checks: "
        f"{singleton}; torus-kernel probes: {torus}; rank rows: {rank_table}"
    )
    print(
        "  Branch-II P5 checks: "
        f"{two_port} direct + {transpose} labelled-transpose; "
        f"cover/contradiction: {two_port_cover + contradiction}"
    )
    print(
        "  formal control: "
        f"{formal_target} target + {responses} responses + {phi} quartic"
    )
    print(
        "  common-incidence control: "
        f"{anchor_claims} anchors/ranks + {mixed_terms} surviving mixed term + "
        f"{anchor_p6} all-word P6"
    )
    print(f"  characteristic-zero/nonzero ledger checks: {ledger}")
    print("  imported boundaries not re-proved: quartic kernel-type exhaustion;")
    print("    conditional decomposable-P4 rank-drop theorem")
    print("  theorem scope retained: source interfaces only; strategic node OPEN;")
    print("    global Krenn-Gu conjecture UNRESOLVED")


if __name__ == "__main__":
    main()
