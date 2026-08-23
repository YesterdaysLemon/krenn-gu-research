"""Independent no-import audit for GLS53.

This audit uses a bit-mask hafnian, sparse monomial dictionaries, and direct
finite-field coefficient evaluation.  It imports no project code or algebra
package and shares no implementation with the primary verifier.
"""

NAMES = ("a0", "a1", "u0", "u1", "u2", "u3")
PORT_INDEX = {f"u{index}": index for index in range(4)}
MODULUS = 101


def add_poly(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply_poly(left, right):
    result = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            result[monomial] = result.get(monomial, 0) + (
                coefficient_left * coefficient_right
            )
    return {key: value for key, value in result.items() if value}


def symbolic_edge(left, right):
    pair = {left, right}
    if pair == {"a0", "a1"}:
        return {}
    if "a0" in pair:
        port = next(vertex for vertex in pair if vertex != "a0")
        return {(f"x{PORT_INDEX[port]}",): 1}
    if "a1" in pair:
        port = next(vertex for vertex in pair if vertex != "a1")
        return {(f"y{PORT_INDEX[port]}",): 1}
    indices = sorted((PORT_INDEX[left], PORT_INDEX[right]))
    return {(f"d{indices[0]}{indices[1]}",): 1}


def symbolic_hafnian(mask, memo):
    if mask == 0:
        return {(): 1}
    if mask in memo:
        return memo[mask]
    first = (mask & -mask).bit_length() - 1
    rest = mask ^ (1 << first)
    result = {}
    candidates = rest
    while candidates:
        second_bit = candidates & -candidates
        second = second_bit.bit_length() - 1
        candidates ^= second_bit
        edge = symbolic_edge(NAMES[first], NAMES[second])
        tail = symbolic_hafnian(rest ^ second_bit, memo)
        result = add_poly(result, multiply_poly(edge, tail))
    memo[mask] = result
    return result


def expected_raw_polynomial():
    result = {}
    for left in range(4):
        for right in range(left + 1, 4):
            complement = sorted(set(range(4)) - {left, right})
            deck = f"d{complement[0]}{complement[1]}"
            for x_index, y_index in ((left, right), (right, left)):
                monomial = tuple(sorted((f"x{x_index}", f"y{y_index}", deck)))
                result[monomial] = result.get(monomial, 0) + 1
    return result


def next_value(state):
    return (37 * state + 17) % MODULUS


def make_matrices(seed):
    values = {}
    state = seed
    for family in ("x", "y"):
        for port in range(4):
            matrix = []
            for _ in range(3):
                row = []
                for _ in range(3):
                    state = next_value(state)
                    row.append(state)
                matrix.append(tuple(row))
            values[(family, port)] = tuple(matrix)
    for left in range(4):
        for right in range(left + 1, 4):
            matrix = []
            for _ in range(3):
                row = []
                for _ in range(3):
                    state = next_value(state)
                    row.append(state)
                matrix.append(tuple(row))
            values[("d", left, right)] = tuple(matrix)
    return values


def numeric_edge(left, right, colors, matrices):
    pair = {left, right}
    if pair == {0, 1}:
        return 0
    if 0 in pair:
        port_vertex = right if left == 0 else left
        port = port_vertex - 2
        return matrices[("x", port)][colors[0]][colors[port_vertex]]
    if 1 in pair:
        port_vertex = right if left == 1 else left
        port = port_vertex - 2
        return matrices[("y", port)][colors[1]][colors[port_vertex]]
    port_left, port_right = sorted((left - 2, right - 2))
    color_left = colors[port_left + 2]
    color_right = colors[port_right + 2]
    return matrices[("d", port_left, port_right)][color_left][color_right]


def numeric_hafnian(mask, colors, matrices):
    if mask == 0:
        return 1
    first = (mask & -mask).bit_length() - 1
    rest = mask ^ (1 << first)
    result = 0
    candidates = rest
    while candidates:
        second_bit = candidates & -candidates
        second = second_bit.bit_length() - 1
        candidates ^= second_bit
        result += numeric_edge(first, second, colors, matrices) * numeric_hafnian(
            rest ^ second_bit, colors, matrices
        )
    return result % MODULUS


def raw_value(colors, matrices):
    result = 0
    for left in range(4):
        for right in range(left + 1, 4):
            complement = sorted(set(range(4)) - {left, right})
            x_left = matrices[("x", left)][colors[0]][colors[left + 2]]
            y_right = matrices[("y", right)][colors[1]][colors[right + 2]]
            x_right = matrices[("x", right)][colors[0]][colors[right + 2]]
            y_left = matrices[("y", left)][colors[1]][colors[left + 2]]
            deck = matrices[("d", complement[0], complement[1])][
                colors[complement[0] + 2]
            ][colors[complement[1] + 2]]
            result += (x_left * y_right + x_right * y_left) * deck
    return result % MODULUS


def test_sparse_bitmask_identity() -> None:
    actual = symbolic_hafnian((1 << 6) - 1, {})
    expected = expected_raw_polynomial()
    assert actual == expected
    assert len(actual) == 12


def test_direct_finite_field_identity() -> None:
    for seed in (1, 7, 23, 61):
        matrices = make_matrices(seed)
        state = seed
        for _ in range(80):
            colors = []
            for _ in range(6):
                state = next_value(state)
                colors.append(state % 3)
            colors = tuple(colors)
            assert numeric_hafnian((1 << 6) - 1, colors, matrices) == raw_value(
                colors, matrices
            )


def test_independent_label_census() -> None:
    for root_order in range(3, 10):
        labels = ["q0", "q1"] + [f"u{index}" for index in range(2 * root_order - 2)]
        active = {"u0", "u1", "u2", "u3"}
        live = []
        for left_index, left in enumerate(labels):
            for right in labels[left_index + 1 :]:
                if left in active and right in active:
                    live.append(frozenset((left, right)))
        assert len(live) == 6
        assert all(pair <= active for pair in live)
        assert len(labels) - 2 - len(active) == 2 * root_order - 6


def main() -> None:
    test_sparse_bitmask_identity()
    test_direct_finite_field_identity()
    test_independent_label_census()
    print("GLS53 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
