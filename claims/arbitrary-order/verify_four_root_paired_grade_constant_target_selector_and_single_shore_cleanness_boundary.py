"""Focused exact verifier for the four-root paired-grade selector theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations, permutations

import sympy as sp

ROOTS = ("r0", "r1", "r2", "r3")
Q = ("q0", "q1")
U = ("u0", "u1", "u2", "u3")
VERTICES = ROOTS + Q + U


def pair_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def generic_edge(left: str, right: str) -> sp.Symbol:
    left, right = pair_key(left, right)
    prefix = "l" if left in ROOTS and right in ROOTS else "w"
    return sp.Symbol(f"{prefix}_{left}_{right}")


@cache
def hafnian(vertices: tuple[str, ...]) -> sp.Expr:
    if not vertices:
        return sp.Integer(1)
    first = vertices[0]
    answer: sp.Expr = sp.Integer(0)
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        answer += generic_edge(first, partner) * hafnian(rest)
    return sp.expand(answer)


def permanent(left: tuple[str, ...], right: tuple[str, ...]) -> sp.Expr:
    if not left:
        return sp.Integer(1)
    answer: sp.Expr = sp.Integer(0)
    for assigned in permutations(right):
        term: sp.Expr = sp.Integer(1)
        for root, outside in zip(left, assigned, strict=True):
            term *= generic_edge(root, outside)
        answer += term
    return sp.expand(answer)


ROOT_PAIRS = tuple(combinations(ROOTS, 2))


def complement(pair: tuple[str, str], universe: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(item for item in universe if item not in pair)


def u_term(root_pair: tuple[str, str]) -> sp.Expr:
    active = complement(root_pair, ROOTS)
    answer: sp.Expr = sp.Integer(0)
    for ports in combinations(U, 2):
        assigned = complement(ports, U)
        answer += generic_edge(*ports) * permanent(active, assigned)
    return sp.expand(answer)


def k_term(left: str, right: str) -> sp.Expr:
    return sp.expand(
        generic_edge(Q[0], left) * generic_edge(Q[1], right)
        + generic_edge(Q[0], right) * generic_edge(Q[1], left)
    )


def pi_term(root_pair: tuple[str, str]) -> sp.Expr:
    active = complement(root_pair, ROOTS)
    answer: sp.Expr = sp.Integer(0)
    for ports in combinations(U, 2):
        assigned = complement(ports, U)
        answer += k_term(*ports) * permanent(active, assigned)
    return sp.expand(answer)


def p_term(root_pair: tuple[str, str]) -> sp.Expr:
    return permanent(root_pair, Q)


def c_one() -> sp.Expr:
    answer: sp.Expr = sp.Integer(0)
    for root_pair in ROOT_PAIRS:
        active = complement(root_pair, ROOTS)
        for residual in Q:
            other_q = Q[1] if residual == Q[0] else Q[0]
            for port in U:
                outside = (residual, port)
                remaining = (other_q,) + tuple(item for item in U if item != port)
                answer += (
                    generic_edge(*root_pair)
                    * permanent(active, outside)
                    * hafnian(tuple(sorted(remaining)))
                )
    return sp.expand(answer)


def c_zero() -> sp.Expr:
    answer: sp.Expr = sp.Integer(0)
    for residual in Q:
        other_q = Q[1] if residual == Q[0] else Q[0]
        for port in U:
            assigned = (residual,) + tuple(item for item in U if item != port)
            answer += permanent(ROOTS, assigned) * generic_edge(other_q, port)
    return sp.expand(answer)


def root_grade(expression: sp.Expr, degree: int) -> sp.Expr:
    root_edges = tuple(generic_edge(*pair) for pair in ROOT_PAIRS)
    polynomial = sp.Poly(expression, *root_edges)
    answer: sp.Expr = sp.Integer(0)
    for powers, coefficient in polynomial.terms():
        if sum(powers) != degree:
            continue
        monomial: sp.Expr = coefficient
        for variable, power in zip(root_edges, powers, strict=True):
            monomial *= variable**power
        answer += monomial
    return sp.expand(answer)


def check_generic_decomposition() -> None:
    full = hafnian(tuple(sorted(VERTICES)))
    y_zero = root_grade(full, 0)
    y_one = root_grade(full, 1)
    y_two = root_grade(full, 2)
    assert len(sp.Add.make_args(y_zero)) == 360
    assert len(sp.Add.make_args(y_one)) == 540
    assert len(sp.Add.make_args(y_two)) == 45

    h = generic_edge(*Q)
    v = permanent(ROOTS, U)
    h_u = hafnian(tuple(sorted(U)))
    omega = sum(
        generic_edge(*root_pair) * p_term(complement(root_pair, ROOTS))
        for root_pair in ROOT_PAIRS
    )
    direct = sum(generic_edge(*pair) * u_term(pair) for pair in ROOT_PAIRS)
    corrected = sum(generic_edge(*pair) * pi_term(pair) for pair in ROOT_PAIRS)
    p_direct = sum(p_term(pair) * u_term(pair) for pair in ROOT_PAIRS)

    rhs_one = sp.expand(omega * h_u + h * direct + corrected + c_one())
    rhs_zero = sp.expand(h * v + p_direct + c_zero())
    assert sp.expand(y_one - rhs_one) == 0
    assert sp.expand(y_zero - rhs_zero) == 0


def check_assignment_fan() -> None:
    vectors = (
        sp.Matrix([1, 0, 0]),
        sp.Matrix([0, 1, 0]),
        sp.Matrix([0, 0, 1]),
        sp.Matrix([1, 1, 1]),
    )
    columns = []
    for left, right in combinations(range(4), 2):
        symmetric = vectors[left] * vectors[right].T + vectors[right] * vectors[left].T
        columns.append(
            sp.Matrix(
                [
                    symmetric[0, 0],
                    symmetric[1, 1],
                    symmetric[2, 2],
                    symmetric[0, 1],
                    symmetric[0, 2],
                    symmetric[1, 2],
                ]
            )
        )
    matrix = sp.Matrix.hstack(*columns)
    assert abs(matrix.det()) == 8


def alignment_u_tensor(root_pair: tuple[int, int]) -> dict[tuple[int, ...], int]:
    root_port_colour = {
        (2, 2): 0,
        (3, 3): 0,
        (0, 2): 1,
        (1, 3): 1,
    }
    direct_blocks = {(0, 1): (0, 0)}
    active_roots = tuple(root for root in range(4) if root not in root_pair)
    answer: dict[tuple[int, ...], int] = {}
    for direct_ports, direct_colours in direct_blocks.items():
        assigned_ports = tuple(port for port in range(4) if port not in direct_ports)
        for image in permutations(assigned_ports):
            word = [-1] * 4
            word[direct_ports[0]], word[direct_ports[1]] = direct_colours
            for root, port in zip(active_roots, image, strict=True):
                colour = root_port_colour.get((root, port))
                if colour is None:
                    break
                word[port] = colour
            else:
                key = tuple(word)
                answer[key] = answer.get(key, 0) + 1
    return answer


def check_alignment_and_purity_controls() -> None:
    kappa = sp.Symbol("kappa")
    root_pairs = tuple(combinations(range(4), 2))
    root_edges = {pair: int(pair == (0, 1)) for pair in root_pairs}
    root_q = {(2, 0): 1, (3, 1): 1}
    p_values = {
        pair: root_q.get((pair[0], 0), 0) * root_q.get((pair[1], 1), 0)
        + root_q.get((pair[1], 0), 0) * root_q.get((pair[0], 1), 0)
        for pair in root_pairs
    }
    omega = sum(
        root_edges[pair]
        * p_values[tuple(root for root in range(4) if root not in pair)]
        for pair in root_pairs
    )
    assert {pair for pair, value in root_edges.items() if value} == {(0, 1)}
    assert {pair for pair, value in p_values.items() if value} == {(2, 3)}
    assert omega == 1

    u_01 = alignment_u_tensor((0, 1))
    u_23 = alignment_u_tensor((2, 3))
    assert u_01 == {(0, 0, 0, 0): 1}
    assert u_23 == {(0, 0, 1, 1): 1}
    difference = dict(u_01)
    for word, coefficient in u_23.items():
        difference[word] = difference.get(word, 0) - kappa * coefficient
    assert any(sp.expand(coefficient) != 0 for coefficient in difference.values())

    zu0, zv0, zu1, zv1 = sp.symbols("zu0 zv0 zu1 zv1", nonzero=True)
    target_e0 = zu0 * zv0
    target_e1 = zu1 * zv1
    rational_contraction = sp.cancel((zv1 / zv0) * target_e0 + 0 * target_e1)
    assert rational_contraction == zu0 * zv1


def permanent_pair(
    left: tuple[sp.Expr, sp.Expr], right: tuple[sp.Expr, sp.Expr]
) -> sp.Expr:
    return sp.expand(left[0] * right[1] + left[1] * right[0])


def check_single_shore_control() -> None:
    q = (sp.Integer(1), sp.Integer(1))
    port = (sp.Integer(1), sp.Integer(-1))
    zero = (sp.Integer(0), sp.Integer(0))
    assert permanent_pair(q, q) == 2
    assert permanent_pair(q, port) == 0
    assert permanent_pair(port, port) == -2
    assert permanent_pair(port, zero) == 0


def scalar_matchings(vertices: tuple[str, ...]) -> list[tuple[tuple[str, str], ...]]:
    if not vertices:
        return [()]
    first = vertices[0]
    answer: list[tuple[tuple[str, str], ...]] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in scalar_matchings(rest):
            answer.append(((first, partner),) + tail)
    return answer


CONTROL = {
    pair_key("r0", "r1"): sp.Integer(1),
    pair_key("r0", "q0"): sp.Integer(1),
    pair_key("r1", "q1"): sp.Integer(1),
    pair_key("r2", "q0"): sp.Integer(1),
    pair_key("r3", "q1"): sp.Integer(1),
    pair_key("r0", "u0"): sp.Rational(1, 2),
    pair_key("r1", "u1"): sp.Integer(1),
    pair_key("r2", "u2"): sp.Integer(1),
    pair_key("r3", "u3"): sp.Integer(1),
    pair_key("q0", "q1"): sp.Integer(1),
    pair_key("q0", "u1"): sp.Integer(1),
    pair_key("q1", "u0"): sp.Integer(-3),
    pair_key("u0", "u1"): sp.Integer(1),
    pair_key("u2", "u3"): sp.Integer(2),
}


def control_edge(left: str, right: str) -> sp.Expr:
    return CONTROL.get(pair_key(left, right), sp.Integer(0))


def control_permanent(left: tuple[str, ...], right: tuple[str, ...]) -> sp.Expr:
    answer: sp.Expr = sp.Integer(0)
    for assigned in permutations(right):
        term: sp.Expr = sp.Integer(1)
        for root, outside in zip(left, assigned, strict=True):
            term *= control_edge(root, outside)
        answer += term
    return sp.expand(answer)


def control_hafnian(vertices: tuple[str, ...]) -> sp.Expr:
    answer: sp.Expr = sp.Integer(0)
    for matching in scalar_matchings(vertices):
        term: sp.Expr = sp.Integer(1)
        for left, right in matching:
            term *= control_edge(left, right)
        answer += term
    return sp.expand(answer)


def check_nested_cancellation() -> None:
    active_pair = ("r0", "r1")
    active_roots = complement(active_pair, ROOTS)
    h = control_edge(*Q)
    h_u = control_hafnian(U)
    p_complement = control_permanent(active_roots, Q)
    omega = control_edge(*active_pair) * p_complement

    u_value: sp.Expr = sp.Integer(0)
    pi_value: sp.Expr = sp.Integer(0)
    for ports in combinations(U, 2):
        assigned = complement(ports, U)
        cofactor = control_permanent(active_roots, assigned)
        u_value += control_edge(*ports) * cofactor
        k_value = control_edge(Q[0], ports[0]) * control_edge(
            Q[1], ports[1]
        ) + control_edge(Q[0], ports[1]) * control_edge(Q[1], ports[0])
        pi_value += k_value * cofactor

    grade_sums = {0: sp.Integer(0), 1: sp.Integer(0), 2: sp.Integer(0)}
    grade_counts = {0: 0, 1: 0, 2: 0}
    for matching in scalar_matchings(VERTICES):
        term: sp.Expr = sp.Integer(1)
        grade = 0
        for left, right in matching:
            value = control_edge(left, right)
            term *= value
            if left in ROOTS and right in ROOTS:
                grade += 1
        if term:
            grade_sums[grade] += term
            grade_counts[grade] += 1

    assert omega == 1
    assert h_u == 2
    assert u_value == 1
    assert pi_value == -3
    assert h * u_value + pi_value == -2
    assert grade_sums == {0: 0, 1: 0, 2: 0}
    assert grade_counts == {0: 5, 1: 3, 2: 0}


def upgraded_blocks() -> dict[tuple[str, str], dict[tuple[int, int], sp.Rational]]:
    blocks: dict[tuple[str, str], dict[tuple[int, int], sp.Rational]] = {}

    def add(
        left: str,
        right: str,
        left_colour: int,
        right_colour: int,
        coefficient: sp.Rational,
    ) -> None:
        ordered = pair_key(left, right)
        colours = (
            (left_colour, right_colour)
            if ordered == (left, right)
            else (right_colour, left_colour)
        )
        block = blocks.setdefault(ordered, {})
        block[colours] = block.get(colours, sp.Rational(0)) + coefficient

    for left_colour, left_sign in ((0, 1), (1, -1)):
        for right_colour, right_sign in ((0, 1), (1, -1)):
            add(
                "r0",
                "r1",
                left_colour,
                right_colour,
                sp.Rational(left_sign * right_sign),
            )

    selected = (
        ("r0", "q0", 0, 0, sp.Rational(1)),
        ("r1", "q1", 0, 0, sp.Rational(1)),
        ("r2", "q0", 1, 0, sp.Rational(1)),
        ("r3", "q1", 1, 0, sp.Rational(1)),
        ("r0", "u0", 0, 0, sp.Rational(1, 2)),
        ("r1", "u1", 0, 0, sp.Rational(1)),
        ("r2", "u2", 1, 1, sp.Rational(1)),
        ("r3", "u3", 1, 1, sp.Rational(1)),
    )
    for item in selected:
        add(*item)

    for outside in ("q0", "q1", "u0", "u1"):
        add("r2", outside, 0, 1, sp.Rational(1))
        add("r3", outside, 0, 2, sp.Rational(1))
    for outside in ("u2", "u3"):
        add("r0", outside, 1, 0, sp.Rational(1))
        add("r1", outside, 1, 2, sp.Rational(1))

    outside_vertices = Q + U
    outside_selected = {
        pair_key("q0", "q1"): (0, sp.Rational(1)),
        pair_key("q0", "u1"): (0, sp.Rational(1)),
        pair_key("q1", "u0"): (0, sp.Rational(-3)),
        pair_key("u0", "u1"): (0, sp.Rational(1)),
        pair_key("u2", "u3"): (1, sp.Rational(2)),
    }
    for left, right in combinations(outside_vertices, 2):
        colour, coefficient = outside_selected.get(
            pair_key(left, right), (2, sp.Rational(1))
        )
        add(left, right, colour, colour, coefficient)
    return blocks


def upgraded_coefficient(
    word: tuple[int, ...],
    blocks: dict[tuple[str, str], dict[tuple[int, int], sp.Rational]],
) -> sp.Rational:
    answer = sp.Rational(0)
    for matching in scalar_matchings(VERTICES):
        term = sp.Rational(1)
        for left, right in matching:
            ordered = pair_key(left, right)
            left_index = VERTICES.index(ordered[0])
            right_index = VERTICES.index(ordered[1])
            term *= blocks.get(ordered, {}).get(
                (word[left_index], word[right_index]), sp.Rational(0)
            )
        answer += term
    return answer


def check_maximal_triple_upgrade() -> None:
    blocks = upgraded_blocks()
    for outside in Q + U:
        rows = []
        for root in ROOTS:
            ordered = pair_key(root, outside)
            row = [sp.Rational(0)] * 3
            for (left_colour, right_colour), coefficient in blocks.get(
                ordered, {}
            ).items():
                root_colour, outside_colour = (
                    (left_colour, right_colour)
                    if ordered == (root, outside)
                    else (right_colour, left_colour)
                )
                # x_root=(1,1,1), so every root coordinate evaluates to one.
                assert root_colour in (0, 1, 2)
                row[outside_colour] += coefficient
            rows.append(row)
        assert sp.Matrix(rows).rank() == 3

    selected_word = tuple(map(int, "0011000011"))
    assert upgraded_coefficient(selected_word, blocks) == 0
    for colour in range(3):
        assert upgraded_coefficient((colour,) * 10, blocks) == 0
    assert upgraded_coefficient(tuple(map(int, "0000001211")), blocks) == 4


def main() -> None:
    check_generic_decomposition()
    check_assignment_fan()
    check_alignment_and_purity_controls()
    check_single_shore_control()
    check_nested_cancellation()
    check_maximal_triple_upgrade()
    print("four-root paired-grade constant-selector verifier: PASS")


if __name__ == "__main__":
    main()
