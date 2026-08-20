"""No-import Fraction audit of the dense private-cross-matching exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = ROOTS + (Q0, Q1) + PORTS
ACTIVE = (0, 1)
DEAD = 2


def solve_residual_covectors(
    h: Fraction,
    tau: tuple[tuple[Fraction, ...], ...],
    x: tuple[Fraction, ...],
    y: tuple[Fraction, ...],
) -> tuple[tuple[tuple[Fraction, ...], ...], tuple[tuple[Fraction, ...], ...]]:
    determinant = y[0] * x[1] - y[1] * x[0]
    assert determinant != 0
    p0_rows = []
    p1_rows = []
    for root in ROOTS:
        l0 = (-h * tau[root][0], Fraction(0), Fraction(0))
        l1 = (Fraction(0), -h * tau[root][1], Fraction(0))
        p0_rows.append(
            tuple(
                (l0[colour] * x[1] - l1[colour] * x[0]) / determinant
                for colour in range(3)
            )
        )
        p1_rows.append(
            tuple(
                (y[0] * l1[colour] - y[1] * l0[colour]) / determinant
                for colour in range(3)
            )
        )
    return tuple(p0_rows), tuple(p1_rows)


def make_data(kill_active_diagonals: bool) -> dict[str, object]:
    h = Fraction(11)
    tau = tuple(
        tuple(Fraction(3 + 5 * root + 2 * colour) for colour in range(3))
        for root in ROOTS
    )
    x = (Fraction(2), Fraction(5), Fraction(0))
    y = (Fraction(3), Fraction(-15, 2), Fraction(0))
    assert x[0] * y[1] + y[0] * x[1] == 0
    p0, p1 = solve_residual_covectors(h, tau, x, y)

    root_root: dict[tuple[int, int, int, int], Fraction] = {}
    for left, right in combinations(ROOTS, 2):
        for left_colour in range(3):
            for right_colour in range(3):
                value = Fraction(
                    101 + 23 * left + 29 * right + 7 * left_colour + 3 * right_colour
                )
                if kill_active_diagonals and left_colour == right_colour in ACTIVE:
                    value = Fraction(0)
                root_root[(left, right, left_colour, right_colour)] = value

    return {
        "h": h,
        "tau": tau,
        "x": x,
        "y": y,
        "p0": p0,
        "p1": p1,
        "root_root": root_root,
    }


def edge_value(
    data: dict[str, object],
    left: int,
    right: int,
    root_word: tuple[int, ...],
    port_word: tuple[int, ...],
) -> Fraction:
    if left > right:
        left, right = right, left

    tau = data["tau"]
    x = data["x"]
    y = data["y"]
    p0 = data["p0"]
    p1 = data["p1"]
    root_root = data["root_root"]
    assert isinstance(tau, tuple)
    assert isinstance(x, tuple)
    assert isinstance(y, tuple)
    assert isinstance(p0, tuple)
    assert isinstance(p1, tuple)
    assert isinstance(root_root, dict)

    if left in ROOTS and right in ROOTS:
        return root_root[(left, right, root_word[left], root_word[right])]
    if left in ROOTS and right in (Q0, Q1):
        values = p0 if right == Q0 else p1
        return values[left][root_word[left]]
    if left in ROOTS and right in PORTS:
        port = right - PORTS[0]
        if left != port or root_word[left] != port_word[port]:
            return Fraction(0)
        return tau[left][root_word[left]]
    if left == Q0 and right == Q1:
        h = data["h"]
        assert isinstance(h, Fraction)
        return h
    if left in (Q0, Q1) and right in PORTS:
        port = right - PORTS[0]
        shore = x if left == Q0 else y
        return shore[port_word[port]]
    if left in PORTS and right in PORTS:
        return Fraction(0)
    raise AssertionError((left, right))


def matching_sum(
    data: dict[str, object],
    root_word: tuple[int, ...],
    port_word: tuple[int, ...],
    remaining: tuple[int, ...] = VERTICES,
) -> Fraction:
    if not remaining:
        return Fraction(1)
    first = remaining[0]
    total = Fraction(0)
    for index in range(1, len(remaining)):
        second = remaining[index]
        value = edge_value(data, first, second, root_word, port_word)
        if value == 0:
            continue
        rest = remaining[1:index] + remaining[index + 1 :]
        total += value * matching_sum(data, root_word, port_word, rest)
    return total


def tau_product(data: dict[str, object], word: tuple[int, ...]) -> Fraction:
    tau = data["tau"]
    assert isinstance(tau, tuple)
    result = Fraction(1)
    for root, colour in enumerate(word):
        result *= tau[root][colour]
    return result


def corrected(data: dict[str, object], colour: int) -> Fraction:
    x = data["x"]
    y = data["y"]
    assert isinstance(x, tuple)
    assert isinstance(y, tuple)
    return 2 * x[colour] * y[colour]


def words_for(
    edge: tuple[int, int], repeated: int, orientation: int
) -> tuple[tuple[int, ...], tuple[int, int]]:
    complement = tuple(root for root in ROOTS if root not in edge)
    if orientation:
        complement = (complement[1], complement[0])
    word = [DEAD] * 4
    word[edge[0]] = repeated
    word[edge[1]] = repeated
    word[complement[0]] = 1 - repeated
    return tuple(word), complement


def audit_pure_and_hamming_shell(data: dict[str, object]) -> None:
    h = data["h"]
    assert isinstance(h, Fraction)
    all_dead = (DEAD,) * 4
    for root_word in product(range(3), repeat=4):
        value = matching_sum(data, root_word, all_dead)
        expected = h * tau_product(data, all_dead) if root_word == all_dead else 0
        assert value == expected

    for port in ROOTS:
        for colour in ACTIVE:
            port_word = [DEAD] * 4
            port_word[port] = colour
            port_word = tuple(port_word)
            for root_word in product(range(3), repeat=4):
                assert matching_sum(data, root_word, port_word) == 0


def audit_dense_orbit(
    raw: dict[str, object], diagonal_killed: dict[str, object]
) -> None:
    raw_root_root = raw["root_root"]
    h = raw["h"]
    assert isinstance(raw_root_root, dict)
    assert isinstance(h, Fraction)
    double_flip_count = 0
    obstruction_count = 0

    for edge in combinations(ROOTS, 2):
        for repeated in ACTIVE:
            other = 1 - repeated
            for orientation in (0, 1):
                matching_word, complement = words_for(edge, repeated, orientation)

                opposite_port = list(matching_word)
                opposite_port[edge[0]] = other
                opposite_port[edge[1]] = other
                opposite_port[complement[0]] = repeated
                opposite_port = tuple(opposite_port)
                double_flip_root = list(opposite_port)
                double_flip_root[edge[0]] = repeated
                double_flip_root[edge[1]] = repeated
                double_flip_root = tuple(double_flip_root)

                tau = raw["tau"]
                assert isinstance(tau, tuple)
                expected_double = (
                    corrected(raw, other)
                    * tau[complement[0]][repeated]
                    * tau[complement[1]][DEAD]
                    * raw_root_root[(edge[0], edge[1], repeated, repeated)]
                )
                assert (
                    matching_sum(raw, double_flip_root, opposite_port)
                    == expected_double
                )
                assert expected_double != 0
                double_flip_count += 1

                expected_obstruction = (
                    -2 * h * tau_product(diagonal_killed, matching_word)
                )
                actual_obstruction = matching_sum(
                    diagonal_killed, matching_word, matching_word
                )
                assert actual_obstruction == expected_obstruction
                assert actual_obstruction != 0
                obstruction_count += 1

    assert double_flip_count == 24
    assert obstruction_count == 24


def main() -> None:
    raw = make_data(kill_active_diagonals=False)
    diagonal_killed = make_data(kill_active_diagonals=True)
    audit_pure_and_hamming_shell(raw)
    audit_pure_and_hamming_shell(diagonal_killed)
    audit_dense_orbit(raw, diagonal_killed)
    print(
        "PASS: independent Fraction matching audit checks the pure/Hamming shell, "
        "24 diagonal gates, and 24 nonzero -2hP coefficients"
    )


if __name__ == "__main__":
    main()
