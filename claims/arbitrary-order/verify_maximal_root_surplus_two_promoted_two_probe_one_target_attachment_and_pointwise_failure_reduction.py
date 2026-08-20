"""Focused exact replay for the promoted two-probe attachment reduction.

The owning document contains the arbitrary-root proofs.  This verifier uses
exact SymPy arithmetic at root orders three through six, together with small
exhaustive rank and polynomial controls.  These bounded checks do not prove
the theorem for arbitrary root order and do not exclude its physical failure
locus.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, permutations, product

import sympy as sp

ROOT_ORDERS = tuple(range(3, 7))


@cache
def permanent(entries: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Compute a square permanent by exact Laplace expansion."""

    if not entries:
        return sp.Integer(1)
    size = len(entries)
    assert all(len(row) == size for row in entries)
    tail = entries[1:]
    answer = sp.Integer(0)
    for column, value in enumerate(entries[0]):
        if value == 0:
            continue
        minor = tuple(row[:column] + row[column + 1 :] for row in tail)
        answer += value * permanent(minor)
    return sp.expand(answer)


def matrix_permanent(matrix: sp.MatrixBase) -> sp.Expr:
    """Convert a SymPy matrix to the immutable permanent input."""

    rows, columns = matrix.shape
    assert rows == columns
    entries = tuple(
        tuple(matrix[row, column] for column in range(columns)) for row in range(rows)
    )
    return permanent(entries)


def permutation_permanent(matrix: sp.MatrixBase) -> sp.Expr:
    """Independent exact permanent from the permutation definition."""

    rows, columns = matrix.shape
    assert rows == columns
    return sp.expand(
        sum(
            sp.prod(matrix[row, sigma[row]] for row in range(rows))
            for sigma in permutations(range(columns))
        )
    )


def check_depth_and_dimensions(root_order: int) -> dict[str, int]:
    """Replay active/formal label depths and dimensions by enumeration."""

    outside_count = 2 * root_order
    promoted_port_count = 2 * root_order - 2
    q_vertices = {0, 1}
    labels = tuple(
        label
        for size in range(2, outside_count + 1, 2)
        for label in combinations(range(outside_count), size)
    )
    active_orders = (promoted_port_count, outside_count)
    active_labels = tuple(label for label in labels if len(label) in active_orders)

    assert {(len(label) - promoted_port_count) // 2 for label in active_labels} == {
        0,
        1,
    }
    assert all(
        len(label) < promoted_port_count
        for label in labels
        if label not in active_labels
    )

    formal_dimension = sum(3 ** len(label) for label in labels)
    active_dimension = sum(3 ** len(label) for label in active_labels)
    evaluated_formal_dimension = sum(
        3 ** sum(vertex not in q_vertices for vertex in label) for label in labels
    )
    evaluated_active_dimension = sum(
        3 ** sum(vertex not in q_vertices for vertex in label)
        for label in active_labels
    )

    expected_formal = (16**root_order + 4**root_order) // 2 - 1
    expected_active = sp.binomial(2 * root_order, 2) * 3 ** (
        2 * root_order - 2
    ) + 3 ** (2 * root_order)
    expected_evaluated_formal = 2 * 4**promoted_port_count - 1
    expected_evaluated_active = (
        sp.binomial(promoted_port_count, 2) * 3 ** (promoted_port_count - 2)
        + 2 * promoted_port_count * 3 ** (promoted_port_count - 1)
        + 2 * 3**promoted_port_count
    )

    assert formal_dimension == expected_formal
    assert active_dimension == expected_active
    assert evaluated_formal_dimension == expected_evaluated_formal
    assert evaluated_active_dimension == expected_evaluated_active
    assert len(active_labels) == sp.binomial(2 * root_order, 2) + 1

    return {
        "root_order": root_order,
        "promoted_ports": promoted_port_count,
        "formal_dimension": int(formal_dimension),
        "active_dimension": int(active_dimension),
        "evaluated_formal_dimension": int(evaluated_formal_dimension),
        "evaluated_active_dimension": int(evaluated_active_dimension),
    }


def incidence_matrix(root_order: int) -> sp.Matrix:
    """Generate a deterministic dense exact root-to-port incidence matrix."""

    return sp.Matrix(
        root_order,
        root_order,
        lambda row, column: (
            1 + ((row + 2) * (column + 3) + row * row + 2 * column) % 11
        ),
    )


def probe_covector(incidence: sp.MatrixBase, probe: int, port: int) -> sp.Matrix:
    """Lift one scalar incidence entry to an exact ternary root covector."""

    return sp.Matrix(
        [
            incidence[probe, port],
            1 + ((probe + 1) * (port + 2)) % 5,
            1 + ((probe + 3) * (port + 1)) % 7,
        ]
    )


def promoted_probe_column(
    incidence: sp.MatrixBase, first_port: int, second_port: int
) -> sp.Matrix:
    """Build the two-probe permanental tensor for one complement pair."""

    return sp.kronecker_product(
        probe_covector(incidence, 0, first_port),
        probe_covector(incidence, 1, second_port),
    ) + sp.kronecker_product(
        probe_covector(incidence, 0, second_port),
        probe_covector(incidence, 1, first_port),
    )


def check_laplace_and_top_separation(root_order: int) -> dict[str, int]:
    """Check the permanent Laplace split and base-root separation exactly."""

    incidence = incidence_matrix(root_order)
    direct = permutation_permanent(incidence)
    assert direct == matrix_permanent(incidence)
    assert direct != 0

    probe_rows = (0, 1)
    remaining_rows = tuple(range(2, root_order))
    laplace = sp.Integer(0)
    nonzero_probe_pairs = []
    for pair in combinations(range(root_order), 2):
        complement = tuple(column for column in range(root_order) if column not in pair)
        probe_minor = permutation_permanent(incidence.extract(probe_rows, pair))
        complement_minor = permutation_permanent(
            incidence.extract(remaining_rows, complement)
        )
        laplace += probe_minor * complement_minor
        if probe_minor != 0:
            nonzero_probe_pairs.append(pair)
    assert sp.expand(laplace - direct) == 0
    assert nonzero_probe_pairs

    selected = nonzero_probe_pairs[0]
    promoted = promoted_probe_column(incidence, *selected)
    base_root = sp.zeros(1, 9)
    base_root[0, 0] = 1
    scalar_probe_minor = permutation_permanent(incidence.extract(probe_rows, selected))
    assert (base_root * promoted)[0] == scalar_probe_minor != 0

    e1 = sp.eye(3)[:, 1]
    top_column = sp.kronecker_product(e1, e1)
    assert (base_root * top_column)[0] == 0
    assert sp.Matrix.hstack(promoted, top_column).rank() == 2

    return {
        "root_order": root_order,
        "permanent": int(direct),
        "laplace_pairs": int(sp.binomial(root_order, 2)),
        "nonzero_probe_pairs": len(nonzero_probe_pairs),
    }


def check_target_family_and_presentations(root_order: int) -> dict[str, int]:
    """Check promoted target counts and the displayed nuisance sizes."""

    promoted_ports = 2 * root_order - 2
    e_m = (
        sp.binomial(promoted_ports, 2) * 3 ** (promoted_ports - 2)
        + 2 * promoted_ports * 3 ** (promoted_ports - 1)
        + 2 * 3**promoted_ports
    )
    family = {
        tuple(vertex for vertex in range(promoted_ports) if vertex not in pair)
        for pair in combinations(range(promoted_ports), 2)
    }
    family.add(tuple(range(promoted_ports)))
    assert len(family) == sp.binomial(promoted_ports, 2) + 1
    assert {len(target) for target in family} == {
        promoted_ports - 2,
        promoted_ports,
    }

    top_minus_two_left = 3 ** (2 + 2)
    top_left = 3**2
    top_minus_two_columns = e_m * 3 ** (promoted_ports - 2)
    top_columns = e_m * 3**promoted_ports
    assert top_minus_two_left == 81
    assert top_left == 9
    if root_order == 3:
        assert e_m == 432
        assert top_minus_two_columns == 3888
        assert top_columns == 34992

    return {
        "root_order": root_order,
        "target_count": len(family),
        "evaluated_domain": int(e_m),
        "top_minus_two_rows": top_minus_two_left,
        "top_minus_two_columns": int(top_minus_two_columns),
        "top_rows": top_left,
        "top_columns": int(top_columns),
    }


def tensor_slice(
    vector: sp.MatrixBase,
    right_coordinate: int,
    left_dimension: int,
    right_dimension: int,
) -> sp.Matrix:
    """Extract one right-coordinate slice from a left-right tensor vector."""

    return sp.Matrix(
        [
            vector[left * right_dimension + right_coordinate]
            for left in range(left_dimension)
        ]
    )


def nuisance_slices(
    theta: sp.MatrixBase, left_dimension: int, right_dimension: int
) -> sp.Matrix:
    """Present all coefficient slices of an operator remainder."""

    slices = [
        tensor_slice(theta[:, source], right, left_dimension, right_dimension)
        for source in range(theta.cols)
        for right in range(right_dimension)
    ]
    return sp.Matrix.hstack(*slices)


def check_selector_and_pure_quotient() -> dict[str, int]:
    """Replay legal selection and the rank-zero/one/two target profiles."""

    left_dimension = 3
    right_dimension = 3
    e0, e1, e2 = (sp.eye(left_dimension)[:, index] for index in range(3))
    right_basis = tuple(sp.eye(right_dimension)[:, index] for index in range(3))
    desired = e2

    formal_projection = sp.eye(right_dimension).row_join(sp.zeros(3, 3))
    desired_operator = sp.kronecker_product(desired, sp.eye(right_dimension))
    theta = sp.Matrix.hstack(
        sp.zeros(left_dimension * right_dimension, right_dimension),
        sp.kronecker_product(e0, right_basis[0] + right_basis[1]),
        sp.kronecker_product(e1, right_basis[1] + right_basis[2]),
        sp.kronecker_product(e0 + e1, right_basis[2]),
    )
    gamma = desired_operator * formal_projection + theta
    nuisance = nuisance_slices(theta, left_dimension, right_dimension)
    assert nuisance.rank() == 2
    assert nuisance.row_join(desired).rank() == 3

    selector = sp.Matrix([[0, 0, 1]])
    legal_operator = sp.kronecker_product(selector, sp.eye(right_dimension))
    assert legal_operator * gamma == formal_projection
    assert selector * nuisance == sp.zeros(1, nuisance.cols)
    assert (selector * desired)[0] == 1

    swallowed_desired = e0 + e1
    swallowed_gamma = (
        sp.kronecker_product(swallowed_desired, sp.eye(right_dimension))
        * formal_projection
        + theta
    )
    assert nuisance.row_join(swallowed_desired).rank() == nuisance.rank()
    equations = sp.Matrix.vstack(nuisance.T, swallowed_desired.T)
    right_hand_side = sp.zeros(equations.rows, 1)
    right_hand_side[-1] = 1
    assert equations.rank() < equations.row_join(right_hand_side).rank()
    assert swallowed_gamma.rank() >= 1

    quotient = selector
    pure = sp.Matrix.hstack(
        desired + e0,
        2 * desired + e1,
        -desired + e0 + e1,
    )
    alpha = sp.diag(2, 3, 5)
    pure_quotient = quotient * pure
    response = pure_quotient * alpha
    assert pure_quotient == sp.Matrix([[1, 2, -1]])
    assert pure_quotient.rank() == 1
    left_target = pure_quotient * alpha
    right_target = (quotient * desired)[0] * response
    assert left_target == right_target
    assert response != sp.zeros(1, 3)

    zero_response_pure = sp.Matrix.hstack(e0, e0 + e1, e1)
    assert quotient * zero_response_pure == sp.zeros(1, 3)
    assert (quotient * desired)[0] != 0
    assert (quotient * desired)[0] * sp.zeros(1, 3) == sp.zeros(1, 3)

    rank_two_quotient = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    rank_two_pure = sp.Matrix.hstack(e0, e1, sp.zeros(3, 1))
    rank_two_target = rank_two_quotient * rank_two_pure
    assert rank_two_target.rank() == 2
    arbitrary_decomposable = sp.Matrix([1, 1]) * sp.Matrix([[1, 2, 3]])
    assert arbitrary_decomposable.rank() == 1
    assert rank_two_target != arbitrary_decomposable

    return {
        "nuisance_rank": nuisance.rank(),
        "good_augmented_rank": nuisance.row_join(desired).rank(),
        "pure_rank": pure_quotient.rank(),
        "excluded_rank": rank_two_target.rank(),
    }


def minors(matrix: sp.MatrixBase, size: int) -> list[sp.Expr]:
    """Return all exact minors, using zero for an impossible size."""

    if size == 0:
        return [sp.Integer(1)]
    if size > min(matrix.rows, matrix.cols):
        return [sp.Integer(0)]
    return [
        sp.expand(matrix.extract(rows, columns).det())
        for rows in combinations(range(matrix.rows), size)
        for columns in combinations(range(matrix.cols), size)
    ]


def strip_laurent_units(polynomial: sp.Poly, variable: sp.Symbol) -> sp.Poly:
    """Remove powers of the Laurent unit ``variable`` from a Q[t] generator."""

    if polynomial.is_zero:
        return polynomial
    answer = polynomial
    unit = sp.Poly(variable, variable, domain=sp.QQ)
    while answer.eval(0) == 0:
        quotient, remainder = sp.div(answer, unit)
        assert remainder.is_zero
        answer = quotient
    return answer


def laurent_radical_generator(
    polynomials: list[sp.Expr], variable: sp.Symbol
) -> sp.Poly:
    """Generator of a univariate Laurent ideal radical over Q."""

    nonzero = [
        sp.Poly(sp.expand(value), variable, domain=sp.QQ)
        for value in polynomials
        if sp.expand(value) != 0
    ]
    if not nonzero:
        return sp.Poly(0, variable, domain=sp.QQ)
    generator = nonzero[0]
    for polynomial in nonzero[1:]:
        generator = sp.gcd(generator, polynomial)
    generator = strip_laurent_units(generator, variable)
    if generator.is_ground:
        return sp.Poly(1, variable, domain=sp.QQ)
    return generator.sqf_part().monic()


def belongs_to_principal_ideal(
    value: sp.Expr, generator: sp.Poly, variable: sp.Symbol
) -> bool:
    """Test membership in one exact univariate principal ideal."""

    polynomial = sp.Poly(sp.expand(value), variable, domain=sp.QQ)
    if generator.is_zero:
        return polynomial.is_zero
    return sp.rem(polynomial, generator).is_zero


def fitting_containment_holds(
    nuisance: sp.MatrixBase,
    pure: sp.MatrixBase,
    gate: sp.Expr,
    variable: sp.Symbol,
) -> bool:
    """Check all radical--Fitting containments in the Laurent PID control."""

    augmented = nuisance.row_join(pure)
    for size in range(1, nuisance.rows + 1):
        radical = laurent_radical_generator(minors(nuisance, size), variable)
        if not all(
            belongs_to_principal_ideal(gate * minor, radical, variable)
            for minor in minors(augmented, size)
        ):
            return False
    return True


def pointwise_useful_exists(
    nuisance: sp.MatrixBase,
    pure: sp.MatrixBase,
    gate: sp.Expr,
    variable: sp.Symbol,
) -> bool:
    """Decide useful fibres independently from exact roots of nuisance minors."""

    augmented = nuisance.row_join(pure)
    for size in range(1, nuisance.rows + 1):
        nuisance_radical = laurent_radical_generator(minors(nuisance, size), variable)
        augmented_minors = minors(augmented, size)
        if nuisance_radical == sp.Poly(1, variable, domain=sp.QQ):
            continue
        if nuisance_radical.is_zero:
            if any(sp.expand(gate * minor) != 0 for minor in augmented_minors):
                return True
            continue
        roots = sp.roots(nuisance_radical.as_expr(), variable)
        assert sum(roots.values()) == nuisance_radical.degree()
        for root in roots:
            if root == 0 or sp.simplify(gate.subs(variable, root)) == 0:
                continue
            if any(
                sp.simplify(minor.subs(variable, root)) != 0
                for minor in augmented_minors
            ):
                return True
    return False


def check_univariate_fitting_controls() -> dict[str, int]:
    """Compare exact radical containments with independent root inspection."""

    t = sp.symbols("t")
    controls = (
        (sp.Matrix([[(t - 1) ** 2]]), sp.Matrix([t - 1]), sp.Integer(1), True),
        (sp.Matrix([[t - 1]]), sp.Matrix([1]), sp.Integer(1), False),
        (sp.Matrix([[t - 1]]), sp.Matrix([1]), t - 1, True),
        (
            sp.diag(1, t - 1),
            sp.Matrix([0, 1]),
            sp.Integer(1),
            False,
        ),
        (sp.diag(1, t - 1), sp.Matrix([0, 1]), t - 1, True),
        (
            sp.Matrix([1, t - 1]),
            sp.Matrix([1, 0]),
            sp.Integer(1),
            False,
        ),
        (
            sp.Matrix([[t * (t - 1)]]),
            sp.Matrix([1]),
            t - 1,
            True,
        ),
    )
    for nuisance, pure, gate, expected_empty in controls:
        containment = fitting_containment_holds(nuisance, pure, gate, t)
        useful = pointwise_useful_exists(nuisance, pure, gate, t)
        assert containment == expected_empty
        assert useful != expected_empty
    return {"univariate_controls": len(controls)}


def interpolation_polynomials(
    points: tuple[int, ...], variable: sp.Symbol
) -> tuple[sp.Expr, ...]:
    """All zero/one functions on a finite reduced rational point set."""

    return tuple(
        sp.expand(sp.interpolate(tuple(zip(points, values)), variable))
        for values in product((0, 1), repeat=len(points))
    )


def check_exhaustive_finite_point_controls() -> dict[str, int]:
    """Exhaust finite reduced scalar tables and all small 0/1 rank states."""

    t = sp.symbols("t")
    points = (-2, -1, 1, 2)
    functions = interpolation_polynomials(points, t)
    vanishing = sp.Poly(sp.prod(t - point for point in points), t, domain=sp.QQ)
    scalar_cases = 0
    for nuisance in functions:
        nuisance_poly = sp.Poly(nuisance, t, domain=sp.QQ)
        zero_set_generator = sp.gcd(vanishing, nuisance_poly).monic()
        for pure in functions:
            for gate in functions:
                no_useful = not any(
                    gate.subs(t, point) != 0
                    and nuisance.subs(t, point) == 0
                    and pure.subs(t, point) != 0
                    for point in points
                )
                product_polynomial = sp.Poly(sp.expand(gate * pure), t, domain=sp.QQ)
                containment = sp.rem(product_polynomial, zero_set_generator).is_zero
                assert containment == no_useful
                scalar_cases += 1

    rank_cases = 0
    binary_matrices = tuple(
        sp.Matrix(2, 2, entries) for entries in product((0, 1), repeat=4)
    )
    for nuisance in binary_matrices:
        for pure in binary_matrices:
            for gate in (0, 1):
                direct = bool(gate) and nuisance.row_join(pure).rank() > nuisance.rank()
                fitting = False
                if gate:
                    augmented = nuisance.row_join(pure)
                    fitting = any(
                        all(minor == 0 for minor in minors(nuisance, size))
                        and any(minor != 0 for minor in minors(augmented, size))
                        for size in (1, 2)
                    )
                assert fitting == direct
                rank_cases += 1

    return {"finite_scalar_cases": scalar_cases, "point_rank_cases": rank_cases}


def check_generic_and_exceptional_modules() -> dict[str, int]:
    """Replay all four displayed generic/exceptional quotient modules."""

    t = sp.symbols("t")
    response = sp.ones(1, 3)

    nuisance = sp.Matrix([1, t - 1])
    desired = sp.Matrix([1, 0])
    pure = sp.Matrix.hstack(desired, desired, desired)
    assert nuisance.rank() == 1
    assert nuisance.row_join(desired).rank() == 2
    assert nuisance.subs(t, 1).row_join(desired).rank() == 1
    quotient_row = sp.Matrix([[-(t - 1), 1]])
    assert quotient_row * nuisance == sp.zeros(1, 1)
    assert quotient_row * pure == (quotient_row * desired)[0] * response

    nuisance = sp.Matrix([[t - 1]])
    desired = sp.Matrix([1])
    pure = sp.ones(1, 3)
    assert nuisance.rank() == nuisance.row_join(desired).rank() == 1
    assert nuisance.subs(t, 1).rank() == 0
    assert nuisance.subs(t, 1).row_join(desired).rank() == 1
    assert nuisance * sp.Matrix([1]) == (t - 1) * desired
    for column in range(3):
        assert nuisance * sp.Matrix([1]) == (t - 1) * pure[:, column]

    nuisance = sp.Matrix([[1]])
    desired = sp.Matrix([1])
    pure = sp.ones(1, 3)
    assert nuisance.row_join(desired).row_join(pure).rank() == nuisance.rank()

    e0, e1 = (sp.eye(2)[:, index] for index in range(2))
    nuisance = e0
    pure = sp.Matrix.hstack(e0, e0, e0)
    desired = e1
    zero_response = sp.zeros(1, 3)
    quotient = e1.T
    assert quotient * nuisance == sp.zeros(1, 1)
    assert quotient * pure == sp.zeros(1, 3)
    assert (quotient * desired)[0] * zero_response == sp.zeros(1, 3)
    assert nuisance.row_join(desired).rank() == 2

    return {"module_controls": 4}


@cache
def perfect_matchings(vertices: tuple[str, ...]):
    """Enumerate perfect matchings of one ordered vertex tuple."""

    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def matching_weight(
    matching: tuple[tuple[str, str], ...],
    edges: dict[tuple[str, str], sp.Expr],
) -> sp.Expr:
    return sp.expand(sp.prod(edges.get(edge_key(*edge), 0) for edge in matching))


def sparse_permanent_matrix(
    rows: tuple[str, ...],
    columns: tuple[str, ...],
    edges: dict[tuple[str, str], sp.Expr],
) -> sp.Matrix:
    return sp.Matrix(
        [[edges.get(edge_key(row, column), 0) for column in columns] for row in rows]
    )


def check_response_zero_physical_control(root_order: int) -> dict[str, int]:
    """Enumerate the arbitrary-r response-zero matching control exactly."""

    z0, z1 = sp.symbols(f"z{root_order}_0 z{root_order}_1", nonzero=True)
    tail_count = root_order - 2
    roots = ("a0", "a1") + tuple(f"k{index}" for index in range(tail_count))
    ports = ("c0", "c1") + tuple(f"v{index}" for index in range(tail_count))
    q_pair = ("q0", "q1")
    edges: dict[tuple[str, str], sp.Expr] = {}

    def add(left: str, right: str, weight: sp.Expr | int = 1) -> None:
        edges[edge_key(left, right)] = sp.sympify(weight)

    add("a0", "c0")
    add("a1", "c1")
    for index in range(tail_count):
        add(f"k{index}", f"v{index}")
    add("a0", "q0", z0)
    add("a1", "q1", z1)
    add("q0", "q1", z0 * z1)
    add("q0", "k0", z0)
    add("q1", "v0", -z1)

    incidence = sparse_permanent_matrix(roots, ports, edges)
    assert matrix_permanent(incidence) == 1
    assert permutation_permanent(incidence) == 1
    p_matrix = sparse_permanent_matrix(("a0", "a1"), q_pair, edges)
    assert matrix_permanent(p_matrix) == z0 * z1
    assert edges[edge_key("q0", "q1")] == z0 * z1

    laplace_terms = {}
    for pair in combinations(range(root_order), 2):
        complement = tuple(index for index in range(root_order) if index not in pair)
        probe_minor = matrix_permanent(incidence.extract((0, 1), pair))
        tail_minor = matrix_permanent(
            incidence.extract(tuple(range(2, root_order)), complement)
        )
        laplace_terms[pair] = probe_minor * tail_minor
    assert sum(laplace_terms.values()) == 1
    assert {pair: value for pair, value in laplace_terms.items() if value} == {
        (0, 1): sp.Integer(1)
    }

    target_vertices = (
        q_pair
        + tuple(f"k{index}" for index in range(tail_count))
        + tuple(f"v{index}" for index in range(tail_count))
    )
    nonzero_matchings = [
        (matching, matching_weight(matching, edges))
        for matching in perfect_matchings(target_vertices)
        if sp.expand(matching_weight(matching, edges)) != 0
    ]
    assert len(nonzero_matchings) == 2
    weights = {sp.expand(weight) for _, weight in nonzero_matchings}
    assert weights == {z0 * z1, -z0 * z1}
    assert sp.expand(sum(weight for _, weight in nonzero_matchings)) == 0

    return {
        "root_order": root_order,
        "target_vertices": len(target_vertices),
        "all_matchings": len(perfect_matchings(target_vertices)),
        "nonzero_matchings": len(nonzero_matchings),
    }


def main() -> None:
    dimensions = [check_depth_and_dimensions(root_order) for root_order in ROOT_ORDERS]
    laplace = [
        check_laplace_and_top_separation(root_order) for root_order in ROOT_ORDERS
    ]
    targets = [
        check_target_family_and_presentations(root_order) for root_order in ROOT_ORDERS
    ]
    selector = check_selector_and_pure_quotient()
    univariate = check_univariate_fitting_controls()
    exhaustive = check_exhaustive_finite_point_controls()
    modules = check_generic_and_exceptional_modules()
    physical = [
        check_response_zero_physical_control(root_order) for root_order in ROOT_ORDERS
    ]

    print("promoted two-probe one-target primary checks: PASS")
    print(f"  exact depth/dimension orders: {dimensions}")
    print(f"  permanent Laplace/top separation: {laplace}")
    print(f"  promoted target/B dimensions: {targets}")
    print(f"  selector and pure quotient: {selector}")
    print(f"  Laurent radical controls: {univariate}")
    print(f"  exhaustive finite controls: {exhaustive}")
    print(f"  generic/exceptional modules: {modules}")
    print(f"  response-zero physical controls: {physical}")
    print(
        "  bounded exact replay only; arbitrary-r proof and failure exclusion are written"
    )


if __name__ == "__main__":
    main()
