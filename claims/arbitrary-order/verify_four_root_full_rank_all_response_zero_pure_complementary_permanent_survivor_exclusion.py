"""Focused exact replay for the GLS9 pure-Pi survivor exclusion.

This bounded primary verifier checks the labelled fibre bookkeeping and the
polynomial/quotient identities used by the candidate theorem.  It is not the
arbitrary-point proof, an independent audit, or a global Krenn--Gu result.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
ROOTS = tuple(range(4))
PORTS = tuple(range(4))
Q0, Q1 = 0, 1
OUTSIDE = tuple(range(6))
PAIR_LABELS = tuple(combinations(OUTSIDE, 2))
PORT_WORDS = tuple(product(COLOURS, repeat=4))
RATIONAL_VALUES = (
    sp.Rational(-1),
    sp.Rational(0),
    sp.Rational(1, 2),
    sp.Rational(1),
)

Word = tuple[int, ...]


def basis(colour: int) -> sp.Matrix:
    return sp.eye(3)[:, colour]


def word_index(word: Word) -> int:
    index = 0
    for colour in word:
        index = 3 * index + colour
    return index


def pure_tensor(colour: int, slot_count: int) -> sp.Matrix:
    answer = sp.zeros(3**slot_count, 1)
    answer[word_index((colour,) * slot_count)] = 1
    return answer


def payload_symbols(prefix: str) -> dict[Word, sp.Symbol]:
    return {
        word: sp.Symbol(f"{prefix}_{''.join(map(str, word))}")
        for word in product(COLOURS, repeat=3)
    }


def insertion_tensor(
    line: sp.Matrix,
    payload: sp.Matrix,
    site: int,
) -> sp.Matrix:
    """Insert a one-slot line into a labelled four-port tensor."""

    assert line.shape == (3, 1)
    assert payload.shape == (27, 1)
    answer = sp.zeros(81, 1)
    for word in PORT_WORDS:
        complement = word[:site] + word[site + 1 :]
        answer[word_index(word)] = line[word[site]] * payload[word_index(complement)]
    return answer


def projected_h(
    i: int,
    j: int,
    k: int,
    prefix: str,
) -> tuple[sp.Matrix, dict[str, sp.Symbol]]:
    names = ("hii", "hij", "hik", "hjj", "hkj", "lam")
    values = sp.symbols(" ".join(f"{prefix}_{name}" for name in names))
    parameters = dict(zip(names, values, strict=True))
    matrix = sp.zeros(3)
    matrix[i, i] = parameters["hii"]
    matrix[i, j] = parameters["hij"]
    matrix[i, k] = parameters["hik"]
    matrix[j, j] = parameters["hjj"]
    matrix[k, j] = parameters["hkj"]
    matrix[k, k] = parameters["lam"]
    expected = parameters["hii"] * parameters["hjj"] * parameters["lam"]
    assert sp.expand(matrix.det() - expected) == 0
    return matrix, parameters


def check_determinant_pivots() -> int:
    checks = 0
    for i, j, k in permutations(COLOURS):
        projected_h(i, j, k, f"pivot_{i}{j}{k}")
        checks += 1
    assert checks == 6
    return checks


def local_families(
    normal_form: str,
    prefix: str,
) -> tuple[
    tuple[int, ...],
    dict[int, sp.Matrix],
    dict[int, sp.Matrix],
]:
    if normal_form == "singleton":
        alpha = sp.Matrix(sp.symbols(f"{prefix}_alpha0:3"))
        beta = sp.Matrix(sp.symbols(f"{prefix}_beta0:3"))
        a0, b0 = sp.symbols(f"{prefix}_a0 {prefix}_b0", nonzero=True)
        return (0,), {0: a0 * alpha}, {0: b0 * beta}
    if normal_form == "two_site":
        alpha_s = sp.Matrix(sp.symbols(f"{prefix}_alpha_s0:3"))
        alpha_t = sp.Matrix(sp.symbols(f"{prefix}_alpha_t0:3"))
        tau = sp.Symbol(f"{prefix}_tau", nonzero=True)
        return (
            (0, 1),
            {0: alpha_s, 1: alpha_t},
            {0: tau * alpha_s, 1: -tau * alpha_t},
        )
    raise AssertionError(f"unknown normal form: {normal_form}")


def check_labelled_fibre_splits() -> tuple[int, int]:
    """Replay all 15 labelled pair terms in both 81-entry diagonal fibres."""

    assert len(PAIR_LABELS) == 15
    word_checks = 0
    labelled_term_checks = 0
    for normal_form in ("singleton", "two_site"):
        for i, j, k in permutations(COLOURS):
            prefix = f"fibre_{normal_form}_{i}{j}{k}"
            h_matrix, h = projected_h(i, j, k, prefix)
            nu = sp.Symbol(f"{prefix}_nu", nonzero=True)
            mu = sp.symbols(" ".join(f"{prefix}_mu{c}" for c in COLOURS))
            support, q0_local, q1_local = local_families(normal_form, prefix)
            companion = {
                (shore, port, diagonal): payload_symbols(
                    f"{prefix}_D{shore}_{port}_{diagonal}"
                )
                for shore in (Q0, Q1)
                for port in support
                for diagonal in (i, j)
            }

            for diagonal in (i, j):
                for port_word in PORT_WORDS:
                    terms: dict[tuple[int, int], sp.Expr] = {}
                    for pair in PAIR_LABELS:
                        if pair == (Q0, Q1):
                            terms[pair] = (
                                h_matrix[diagonal, diagonal] * nu
                                if port_word == (k,) * 4
                                else sp.Integer(0)
                            )
                            continue
                        if pair[0] >= 2:
                            terms[pair] = sp.Integer(0)
                            continue

                        shore = pair[0]
                        port = pair[1] - 2
                        if port not in support:
                            terms[pair] = sp.Integer(0)
                            continue
                        complement = port_word[:port] + port_word[port + 1 :]
                        if shore == Q0 and diagonal == i:
                            terms[pair] = (
                                q0_local[port][port_word[port]]
                                * companion[(Q0, port, diagonal)][complement]
                            )
                        elif shore == Q1 and diagonal == j:
                            terms[pair] = (
                                q1_local[port][port_word[port]]
                                * companion[(Q1, port, diagonal)][complement]
                            )
                        else:
                            terms[pair] = sp.Integer(0)

                    assert tuple(terms) == PAIR_LABELS
                    insertion = sum(
                        (
                            terms[(Q0, 2 + port)]
                            if diagonal == i
                            else terms[(Q1, 2 + port)]
                        )
                        for port in support
                    )
                    direct = sum(terms.values(), sp.Integer(0))
                    q_term = (
                        h_matrix[diagonal, diagonal] * nu
                        if port_word == (k,) * 4
                        else sp.Integer(0)
                    )
                    assert sp.expand(direct - q_term - insertion) == 0

                    target = (
                        mu[diagonal] if port_word == (diagonal,) * 4 else sp.Integer(0)
                    )
                    equation = sp.expand(direct - target)
                    relation = sp.expand(h["lam"] * nu - mu[k])
                    desired = sp.expand(
                        h["lam"] * insertion
                        - h["lam"] * target
                        + (
                            mu[k] * h_matrix[diagonal, diagonal]
                            if port_word == (k,) * 4
                            else 0
                        )
                    )
                    correction = (
                        h_matrix[diagonal, diagonal] * relation
                        if port_word == (k,) * 4
                        else 0
                    )
                    assert sp.expand(desired - (h["lam"] * equation - correction)) == 0
                    word_checks += 1
                    labelled_term_checks += len(terms)

    assert word_checks == 2 * 6 * 2 * 81 == 1944
    assert labelled_term_checks == word_checks * 15 == 29160
    return word_checks, labelled_term_checks


def quotient_chart(
    line: sp.Matrix,
    pivot: int,
) -> sp.Matrix:
    """Return a rank-two quotient map with kernel equal to the given line."""

    assert line[pivot] == 1
    rows = []
    for colour in COLOURS:
        if colour == pivot:
            continue
        row = sp.zeros(1, 3)
        row[colour] = 1
        row[pivot] = -line[colour]
        rows.append(row)
    answer = sp.Matrix.vstack(*rows)
    assert answer * line == sp.zeros(2, 1)
    retained = [colour for colour in COLOURS if colour != pivot]
    assert answer[:, retained].det() == 1
    return answer


def rational_line_charts() -> tuple[tuple[int, sp.Matrix, sp.Matrix], ...]:
    charts = []
    for pivot in COLOURS:
        free = [colour for colour in COLOURS if colour != pivot]
        for left, right in product(RATIONAL_VALUES, repeat=2):
            line = sp.zeros(3, 1)
            line[pivot] = 1
            line[free[0]] = left
            line[free[1]] = right
            charts.append((pivot, line, quotient_chart(line, pivot)))
    assert len(charts) == 48
    return tuple(charts)


def coordinate_line(line: sp.Matrix, colour: int) -> bool:
    return all(line[other] == 0 for other in COLOURS if other != colour)


def killed_pure_line(q_s: sp.Matrix, q_t: sp.Matrix, colour: int) -> bool:
    return sp.kronecker_product(q_s * basis(colour), q_t * basis(colour)) == sp.zeros(
        4, 1
    )


def check_quotient_obstructions() -> tuple[int, int, int]:
    """Replay singleton rank and two-site line cover on exact line charts."""

    symbolic_chart_checks = 0
    for pivot in COLOURS:
        free = [colour for colour in COLOURS if colour != pivot]
        x, y = sp.symbols(f"chart_{pivot}_x chart_{pivot}_y")
        line = sp.zeros(3, 1)
        line[pivot] = 1
        line[free[0]] = x
        line[free[1]] = y
        quotient_chart(line, pivot)
        symbolic_chart_checks += 1

    singleton_rank_checks = 0
    for i, j, k in permutations(COLOURS):
        del j
        a, b = sp.symbols(f"singleton_{i}{k}_a singleton_{i}{k}_b", nonzero=True)
        desired = sp.zeros(3, 27)
        desired[i, word_index((i,) * 3)] = a
        desired[k, word_index((k,) * 3)] = b
        selected = desired.extract([i, k], [word_index((i,) * 3), word_index((k,) * 3)])
        assert sp.expand(selected.det() - a * b) == 0

        alpha = sp.Matrix(sp.symbols(f"singleton_{i}{k}_alpha0:3"))
        payload = sp.Matrix(sp.symbols(f"singleton_{i}{k}_x0:27"))
        insertion = alpha * payload.T
        insertion_minor = insertion.extract(
            [i, k], [word_index((i,) * 3), word_index((k,) * 3)]
        )
        assert sp.expand(insertion_minor.det()) == 0
        singleton_rank_checks += 1
    assert singleton_rank_checks == 6

    charts = rational_line_charts()
    rational_pair_checks = 0
    singleton_quotient_checks = 0
    for i, j, k in permutations(COLOURS):
        assert sp.Matrix.hstack(pure_tensor(i, 2), pure_tensor(k, 2)).rank() == 2
        assert sp.Matrix.hstack(pure_tensor(j, 2), pure_tensor(k, 2)).rank() == 2
        for _, line, quotient in charts:
            killed_i = quotient * basis(i) == sp.zeros(2, 1)
            killed_k = quotient * basis(k) == sp.zeros(2, 1)
            assert not (killed_i and killed_k)
            singleton_quotient_checks += 1

        for _, line_s, q_s in charts:
            for _, line_t, q_t in charts:
                killed = {
                    colour: killed_pure_line(q_s, q_t, colour) for colour in COLOURS
                }
                for colour in COLOURS:
                    expected = coordinate_line(line_s, colour) or coordinate_line(
                        line_t, colour
                    )
                    assert killed[colour] == expected
                cover_ik = killed[i] and killed[k]
                cover_jk = killed[j] and killed[k]
                expected_ik = {
                    colour
                    for colour in (i, k)
                    if coordinate_line(line_s, colour)
                    or coordinate_line(line_t, colour)
                } == {i, k}
                expected_jk = {
                    colour
                    for colour in (j, k)
                    if coordinate_line(line_s, colour)
                    or coordinate_line(line_t, colour)
                } == {j, k}
                assert cover_ik == expected_ik
                assert cover_jk == expected_jk
                assert not (cover_ik and cover_jk)
                rational_pair_checks += 1

    assert singleton_quotient_checks == 6 * 48 == 288
    assert rational_pair_checks == 6 * 48 * 48 == 13824
    return symbolic_chart_checks, singleton_quotient_checks, rational_pair_checks


def check_three_line_and_determinant_controls() -> tuple[int, int]:
    """Replay the two sharp proof-boundary controls coefficientwise."""

    three_line_coefficients = 0
    determinant_boundary_coefficients = 0
    for i, j, k in permutations(COLOURS):
        payload_i = 2 * pure_tensor(i, 3)
        payload_j = 5 * pure_tensor(j, 3)
        payload_k_first = -3 * pure_tensor(k, 3)
        payload_k_second = 7 * pure_tensor(k, 3)
        first = insertion_tensor(basis(i), payload_i, 0) + insertion_tensor(
            basis(k), payload_k_first, 2
        )
        second = insertion_tensor(basis(j), payload_j, 1) + insertion_tensor(
            basis(k), payload_k_second, 2
        )
        assert first == 2 * pure_tensor(i, 4) - 3 * pure_tensor(k, 4)
        assert second == 5 * pure_tensor(j, 4) + 7 * pure_tensor(k, 4)
        three_line_coefficients += 2 * 81

        h_boundary = sp.zeros(3)
        h_boundary[j, j] = 2
        h_boundary[k, k] = 3
        assert h_boundary.det() == 0
        singleton = insertion_tensor(basis(i), pure_tensor(i, 3), 0)
        assert singleton == pure_tensor(i, 4)
        determinant_boundary_coefficients += 81

    assert three_line_coefficients == 972
    assert determinant_boundary_coefficients == 486
    return three_line_coefficients, determinant_boundary_coefficients


def permanent4(columns: tuple[tuple[int, ...], ...]) -> int:
    return sum(
        columns[0][assignment[0]]
        * columns[1][assignment[1]]
        * columns[2][assignment[2]]
        * columns[3][assignment[3]]
        for assignment in permutations(ROOTS)
    )


def fixture_failed_coefficient() -> tuple[int, dict[tuple[int, int], int]]:
    """Recompute the GLS9 fixture's mixed 002222 coefficient from 15 terms."""

    f0, f1, f2, f3 = (tuple(int(row == column) for row in ROOTS) for column in ROOTS)
    zero = (0, 0, 0, 0)
    incidence = {
        Q0: (f0, f1, zero),
        Q1: (f2, f0, zero),
        2: (f1, f2, f0),
        3: (f2, f3, f1),
        4: (f3, zero, f2),
        5: (zero, zero, f3),
    }
    edges: dict[tuple[int, int], sp.Matrix] = {
        (Q0, Q1): sp.eye(3),
        (Q0, 2): basis(0) * basis(0).T,
        (Q1, 2): basis(1) * basis(0).T,
        (Q0, 3): basis(0) * basis(1).T,
        (Q1, 3): -basis(1) * basis(1).T,
    }
    word = (0, 0, 2, 2, 2, 2)
    terms = {}
    for pair in PAIR_LABELS:
        complement = tuple(position for position in OUTSIDE if position not in pair)
        complement_word = tuple(word[position] for position in complement)
        columns = tuple(
            incidence[position][colour]
            for position, colour in zip(complement, complement_word, strict=True)
        )
        pi_coefficient = permanent4(columns)
        edge = edges.get(pair, sp.zeros(3))
        edge_coefficient = int(edge[word[pair[0]], word[pair[1]]])
        terms[pair] = edge_coefficient * pi_coefficient

    assert len(terms) == 15
    assert terms[(Q0, Q1)] == 1
    assert all(value == 0 for pair, value in terms.items() if pair != (Q0, Q1))
    total = sum(terms.values())
    assert total == 1
    return total, terms


def main() -> None:
    fibre_words, fibre_terms = check_labelled_fibre_splits()
    determinant_pivots = check_determinant_pivots()
    symbolic_charts, singleton_quotients, rational_pairs = check_quotient_obstructions()
    three_line, determinant_boundary = check_three_line_and_determinant_controls()
    fixture_value, fixture_terms = fixture_failed_coefficient()

    print("four-root pure-Pi survivor exclusion focused replay: PASS")
    print(
        f"  {fibre_words} complete fibre words and {fibre_terms} labelled terms checked"
    )
    print(f"  {determinant_pivots} determinant pivot identities checked")
    print(
        f"  6 singleton rank minors and {singleton_quotients} quotient charts checked"
    )
    print(
        f"  {symbolic_charts} symbolic projective charts and "
        f"{rational_pairs} ordered rational two-line charts checked"
    )
    print(
        f"  {three_line} three-line and {determinant_boundary} "
        "determinant-boundary coefficients checked"
    )
    print(
        f"  GLS9 fixture 002222 coefficient={fixture_value}; "
        f"{sum(value != 0 for value in fixture_terms.values())} of 15 terms nonzero"
    )
    print("  bounded replay only; the written quotient argument is the general proof")


if __name__ == "__main__":
    main()
