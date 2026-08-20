"""Focused exact replay for the four-root supply/attachment trichotomy."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations

import sympy as sp

ROOTS = tuple(range(4))
U = tuple(range(4))
Q = (4, 5)
OUTSIDE = U + Q
PAIR_LABELS = tuple(combinations(OUTSIDE, 2))
ROOT_PAIR_LABELS = tuple(combinations(ROOTS, 2))

# An entry is the unique supported coordinate colour of that edge block.
ROOT_TABLE = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)
OUTSIDE_COLOURS = {
    (0, 1): 0,
    (0, 2): 2,
    (0, 3): 0,
    (0, 4): 2,
    (0, 5): 0,
    (1, 2): 1,
    (1, 3): 1,
    (1, 4): 2,
    (1, 5): 0,
    (2, 3): 0,
    (2, 4): 1,
    (2, 5): 2,
    (3, 4): 1,
    (3, 5): 0,
    (4, 5): 0,
}


def column_basis(matrix: sp.Matrix) -> sp.Matrix:
    basis = matrix.columnspace()
    return sp.Matrix.hstack(*basis) if basis else sp.zeros(matrix.rows, 0)


def observable(desired: sp.Matrix, others: sp.Matrix) -> bool:
    return others.row_join(desired).rank() > others.rank()


def check_pair_circuit_and_deck_shift() -> None:
    """Replay the O/C split, quotient lift, and nonphysical deck warning."""

    e0, e1, e2, e3 = (sp.eye(4)[:, index] for index in range(4))
    higher = e3

    # O: the desired quotient class is separated from the other pair classes.
    desired_o = e2
    others_o = sp.Matrix.hstack(e0, e1)
    assert observable(desired_o, others_o.row_join(higher))
    quotient_selector = sp.Matrix([[0, 0, 1, 0]])
    assert quotient_selector * desired_o == sp.Matrix([1])
    assert quotient_selector * others_o == sp.zeros(1, 2)
    assert quotient_selector * higher == sp.zeros(1, 1)

    # C: c_Q-c_1-c_2=0 after quotienting the higher line.
    g_q = e0 + e1 + 2 * e3
    g_1 = e0 + e3
    g_2 = e1 - 3 * e3
    quotient = sp.eye(4)[:3, :]
    c_q = quotient * g_q
    c_1 = quotient * g_1
    c_2 = quotient * g_2
    circuit = sp.Matrix([1, -1, -1])
    classes = sp.Matrix.hstack(c_q, c_1, c_2)
    assert classes * circuit == sp.zeros(3, 1)
    assert not observable(c_q, sp.Matrix.hstack(c_1, c_2))
    assert all(
        classes[:, keep].rank() == len(keep) for keep in ((0, 1), (0, 2), (1, 2))
    )

    lifted_relation = sp.Matrix.hstack(g_q, g_1, g_2) * circuit
    assert lifted_relation == 4 * e3
    base_root_functional = sp.Matrix([[1, 2, 0, 0]])
    assert base_root_functional * higher == sp.zeros(1, 1)
    pi_values = base_root_functional * sp.Matrix.hstack(g_q, g_1, g_2)
    assert pi_values * circuit == sp.zeros(1, 1)
    assert pi_values[0, 0] != 0
    assert any(pi_values[0, index] != 0 for index in (1, 2))

    # A circuit preserves the linear state but need not preserve a nonlinear
    # principal-deck relation.
    deck = sp.Matrix([1, 1, 1])
    state = classes * deck
    shift = -deck[0] * circuit
    shifted = deck + shift
    assert shifted[0] == 0
    assert classes * shifted == state

    def recurrence(values: sp.Matrix) -> sp.Expr:
        return values[0] * values[2] - values[1] ** 2

    assert recurrence(deck) == 0
    assert recurrence(shifted) == -4


def generic_rank(matrix: sp.Matrix) -> int:
    """SymPy computes rank over the rational-function field."""

    return matrix.rank()


def branch_name(targets: list[dict[str, object]]) -> str:
    """Classify one finite polynomial control as R, E, or A."""

    if any(
        all(sp.expand(entry) == 0 for entry in target["response"]) for target in targets
    ):
        return "R"
    for target in targets:
        nuisance = target["nuisance"]
        desired = target["desired"]
        if generic_rank(nuisance.row_join(desired)) == generic_rank(nuisance):
            return "A"
    return "E"


def escape_targets(t: sp.Symbol) -> list[dict[str, object]]:
    targets = []
    for index in range(7):
        nuisance = sp.Matrix(
            [
                [1, 0],
                [0, t + index + 1],
                [0, 0],
            ]
        )
        desired = sp.Matrix([0, 0, t + 2 * index + 3])
        pure = sp.Matrix.hstack(
            desired,
            desired + nuisance[:, 0],
            2 * desired + nuisance[:, 1],
        )
        targets.append(
            {
                "nuisance": nuisance,
                "desired": desired,
                "pure": pure,
                "response": [t + 3 * index + 5],
            }
        )
    return targets


def check_response_escape_absorption_controls() -> None:
    """Replay finite R/E/A controls and the common h*p principal open."""

    t = sp.symbols("t")
    h = t + 1
    raw_p = t + 2

    response_zero = escape_targets(t)
    response_zero[3] = dict(response_zero[3])
    response_zero[3]["response"] = [sp.Integer(0), sp.Integer(0)]
    assert branch_name(response_zero) == "R"

    escaping = escape_targets(t)
    assert branch_name(escaping) == "E"
    common_open = sp.expand(h * raw_p)
    for index, target in enumerate(escaping):
        nuisance = target["nuisance"]
        desired = target["desired"]
        pure = target["pure"]
        response = target["response"][0]
        nuisance_minor = nuisance.extract((0, 1), (0, 1)).det()
        augmented_minor = nuisance.row_join(desired).det()
        assert sp.expand(nuisance_minor) == t + index + 1
        assert sp.expand(augmented_minor) == sp.expand(
            (t + index + 1) * (t + 2 * index + 3)
        )
        assert generic_rank(nuisance) == 2
        assert generic_rank(nuisance.row_join(desired)) == 3
        assert generic_rank(nuisance.row_join(pure)) == 3
        common_open *= nuisance_minor * augmented_minor * response
    common_open = sp.expand(common_open)
    assert sp.Poly(common_open, t, domain=sp.QQ) != 0
    assert common_open.subs(t, 1) != 0
    assert h.subs(t, 1) * raw_p.subs(t, 1) == 6
    for target in escaping:
        nuisance_at_point = target["nuisance"].subs(t, 1)
        desired_at_point = target["desired"].subs(t, 1)
        assert nuisance_at_point.rank() == 2
        assert nuisance_at_point.row_join(desired_at_point).rank() == 3
        assert target["response"][0].subs(t, 1) != 0

    absorbing = escape_targets(t)
    delta = t - 1
    nuisance = sp.Matrix([[delta, 0], [0, 1]])
    desired = sp.Matrix([1, 0])
    pure = sp.Matrix.hstack(sp.eye(2), sp.Matrix([1, 1]))
    absorbing[2] = {
        "nuisance": nuisance,
        "desired": desired,
        "pure": pure,
        "response": [sp.Integer(1)],
    }
    assert branch_name(absorbing) == "A"
    assert generic_rank(nuisance) == 2
    assert generic_rank(nuisance.row_join(desired)) == 2
    assert generic_rank(nuisance.row_join(desired).row_join(pure)) == 2

    b_g = sp.Matrix([1, 0])
    b_0 = sp.Matrix([1, 0])
    b_1 = sp.Matrix([0, delta])
    b_2 = sp.Matrix([1, delta])
    assert nuisance * b_g == delta * desired
    assert nuisance * b_0 == delta * pure[:, 0]
    assert nuisance * b_1 == delta * pure[:, 1]
    assert nuisance * b_2 == delta * pure[:, 2]
    assert nuisance.subs(t, 2).row_join(desired).rank() == nuisance.subs(t, 2).rank()
    assert nuisance.subs(t, 1).rank() == 1
    assert nuisance.subs(t, 1).row_join(desired).rank() == 2


def edge_colour(left: int, right: int) -> int | None:
    """Supported colour for a full-graph edge, or None for the zero block."""

    if left > right:
        left, right = right, left
    if right < 4:
        return None
    if left < 4:
        return ROOT_TABLE[left][right - 4]
    return OUTSIDE_COLOURS[(left - 4, right - 4)]


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def compatible_matchings(word: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    """Enumerate full matchings compatible with one coordinate word."""

    answer = []
    for matching in perfect_matchings(tuple(range(10))):
        if all(
            edge_colour(left, right) == word[left] == word[right]
            for left, right in matching
        ):
            answer.append(matching)
    return answer


def root_matchings(vertices: tuple[int, ...]):
    """Root-root matchings; all corresponding physical blocks are zero."""

    yield from perfect_matchings(vertices)


def companion_counter(outside_set: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    """Companion root-word counter after evaluating outside vectors at one."""

    size = len(outside_set)
    answer: Counter[tuple[int, ...]] = Counter()
    for assigned_roots in permutations(ROOTS, size):
        root_word: list[int | None] = [None] * 4
        for root, outside in zip(assigned_roots, outside_set, strict=True):
            colour = ROOT_TABLE[root][outside]
            if colour is None:
                break
            root_word[root] = colour
        else:
            remaining = tuple(root for root in ROOTS if root_word[root] is None)
            for matching in root_matchings(remaining):
                trial = root_word[:]
                for left, right in matching:
                    colour = edge_colour(left, right)
                    if colour is None:
                        break
                    trial[left] = trial[right] = colour
                else:
                    assert all(colour is not None for colour in trial)
                    answer[tuple(trial)] += 1
    return answer


def word_index(word: tuple[int, ...]) -> int:
    value = 0
    for digit in word:
        value = 3 * value + digit
    return value


def response_counter(target: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    """Contract Q at all ones and retain the open target word."""

    vertices = tuple(4 + outside for outside in Q + target)
    answer: Counter[tuple[int, ...]] = Counter()
    for matching in perfect_matchings(vertices):
        colours: dict[int, int] = {}
        for left, right in matching:
            colour = edge_colour(left, right)
            assert colour is not None
            colours[left] = colours[right] = colour
        answer[tuple(colours[4 + outside] for outside in target)] += 1
    return answer


def check_physical_order_two_sensor() -> None:
    """Reconstruct the observable order-two sensor and higher-grade zero."""

    columns = []
    for omitted_pair in PAIR_LABELS:
        outside_set = tuple(
            outside for outside in OUTSIDE if outside not in omitted_pair
        )
        counter = companion_counter(outside_set)
        vector = sp.zeros(81, 1)
        for word, coefficient in counter.items():
            vector[word_index(word)] = coefficient
        columns.append(vector)
    sensor = sp.Matrix.hstack(*columns)
    assert sensor.rank() == 15

    pivot_words = (
        "0000",
        "0001",
        "0010",
        "0020",
        "0021",
        "0022",
        "0100",
        "0101",
        "0110",
        "0200",
        "1000",
        "1001",
        "1010",
        "1101",
        "2010",
    )
    pivot_rows = [word_index(tuple(map(int, word))) for word in pivot_words]
    assert sensor.extract(pivot_rows, range(15)).det() == -1

    for deck_label in combinations(OUTSIDE, 4):
        complement = tuple(outside for outside in OUTSIDE if outside not in deck_label)
        assert len(complement) == 2
        assert companion_counter(complement) == Counter()
    assert companion_counter(()) == Counter()


def check_q_data_responses_and_desired_zeros() -> None:
    """Check (26), all seven physical responses, and all seven g_S=0."""

    h_q = Counter({(OUTSIDE_COLOURS[Q], OUTSIDE_COLOURS[Q]): 1})
    assert h_q == Counter({(0, 0): 1})

    pi_q = Counter()
    for assigned_roots in permutations(ROOTS):
        outside_word = [None] * 4
        for root, outside in zip(assigned_roots, U, strict=True):
            colour = ROOT_TABLE[root][outside]
            if colour is None:
                break
            outside_word[outside] = colour
        else:
            pi_q[tuple(outside_word)] += 1
    assert pi_q[(1, 1, 1, 1)] == 1

    alpha = [int(ROOT_TABLE[root][Q[0]] is not None) for root in ROOTS]
    beta = [int(ROOT_TABLE[root][Q[1]] is not None) for root in ROOTS]
    raw_values = tuple(
        alpha[left] * beta[right] + alpha[right] * beta[left]
        for left, right in ROOT_PAIR_LABELS
    )
    assert ROOT_PAIR_LABELS == ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    assert raw_values == (2, 1, 1, 1, 1, 1)

    expected = {
        (0, 1): {(0, 0): 1, (0, 2): 1, (2, 0): 1},
        (0, 2): {(0, 1): 1, (2, 2): 2},
        (0, 3): {(0, 0): 1, (0, 1): 1, (2, 0): 1},
        (1, 2): {(0, 1): 1, (1, 1): 1, (2, 2): 1},
        (1, 3): {(0, 1): 1, (1, 1): 1, (2, 0): 1},
        (2, 3): {(0, 0): 1, (1, 0): 1, (2, 1): 1},
        U: {
            (0, 0, 0, 0): 1,
            (0, 0, 1, 0): 2,
            (0, 0, 2, 1): 1,
            (0, 1, 1, 0): 1,
            (0, 1, 1, 1): 2,
            (0, 2, 0, 0): 1,
            (0, 2, 2, 0): 1,
            (2, 0, 0, 0): 1,
            (2, 0, 2, 1): 1,
            (2, 1, 1, 0): 1,
            (2, 1, 2, 1): 2,
            (2, 2, 2, 0): 1,
        },
    }
    targets = tuple(combinations(U, 2)) + (U,)
    for target in targets:
        response = response_counter(target)
        assert response == Counter(expected[target])
        assert sum(response.values()) == (15 if target == U else 3)
        complement = tuple(outside for outside in U if outside not in target)
        assert companion_counter(complement) == Counter()


def check_mixed_coefficient() -> None:
    word = tuple(map(int, "1200100020"))
    matchings = compatible_matchings(word)
    assert matchings == [((0, 4), (1, 8), (2, 6), (3, 7), (5, 9))]
    assert len(matchings) == 1


def main() -> None:
    check_pair_circuit_and_deck_shift()
    check_response_escape_absorption_controls()
    check_physical_order_two_sensor()
    check_q_data_responses_and_desired_zeros()
    check_mixed_coefficient()
    print("four-root supply-to-attachment trichotomy verifier: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
