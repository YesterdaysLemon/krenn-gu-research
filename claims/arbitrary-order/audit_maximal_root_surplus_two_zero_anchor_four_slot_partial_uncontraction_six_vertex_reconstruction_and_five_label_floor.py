"""Independent no-import audit for GLS54.

The audit uses bit masks, sparse monomials, and exact F_101 physical controls.
It imports no project code or algebra package.
"""

PRIME = 101
NAMES = ("a0", "a1", "t0", "t1", "t2", "t3")


def poly_add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_multiply(left, right):
    result = {}
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            word = tuple(sorted(left_word + right_word))
            result[word] = result.get(word, 0) + left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def symbolic_edge(left, right):
    pair = {left, right}
    if pair == {"a0", "a1"}:
        return {}
    if "a0" in pair:
        target = next(vertex for vertex in pair if vertex != "a0")
        return {(f"x{target[1:]}",): 1}
    if "a1" in pair:
        target = next(vertex for vertex in pair if vertex != "a1")
        return {(f"y{target[1:]}",): 1}
    indices = sorted((int(left[1:]), int(right[1:])))
    return {(f"e{indices[0]}{indices[1]}",): 1}


def symbolic_hafnian(mask, memo):
    if mask == 0:
        return {(): 1}
    if mask in memo:
        return memo[mask]
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    result = {}
    candidates = rest
    while candidates:
        second_bit = candidates & -candidates
        candidates ^= second_bit
        second = second_bit.bit_length() - 1
        edge = symbolic_edge(NAMES[first], NAMES[second])
        tail = symbolic_hafnian(rest ^ second_bit, memo)
        result = poly_add(result, poly_multiply(edge, tail))
    memo[mask] = result
    return result


def expected_words():
    result = {}
    for left in range(4):
        for right in range(left + 1, 4):
            complement = sorted({0, 1, 2, 3} - {left, right})
            edge = f"e{complement[0]}{complement[1]}"
            for x_index, y_index in ((left, right), (right, left)):
                word = tuple(sorted((f"x{x_index}", f"y{y_index}", edge)))
                result[word] = 1
    return result


def matrix_vector(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3)) % PRIME
        for row in range(3)
    )


def test_hostile_inactive_residual_boundary() -> None:
    z = (1, 1, 1)
    transverse = (1, 0, 0)
    left_map = ((1, -1, 0), (0, 1, -1), (1, 0, -1))
    right_map = ((2, -2, 0), (0, 3, -3), (5, 0, -5))
    assert matrix_vector(left_map, z) == (0, 0, 0)
    assert matrix_vector(right_map, z) == (0, 0, 0)
    assert matrix_vector(left_map, transverse) != (0, 0, 0)
    assert matrix_vector(right_map, transverse) != (0, 0, 0)

    # At z, both two-bijection terms vanish for every active endpoint.
    active_left = (17, 29, 43)
    active_right = (31, 47, 59)
    shore_left = matrix_vector(left_map, z)
    shore_right = matrix_vector(right_map, z)
    companion = tuple(
        (
            shore_left[row] * active_right[column]
            + active_left[row] * shore_right[column]
        )
        % PRIME
        for row in range(3)
        for column in range(3)
    )
    assert companion == (0,) * 9


def test_reversed_activity_census() -> None:
    for root_order in range(9, 2, -1):
        residual = ("q1", "q0")
        promoted = tuple(f"u{index}" for index in range(2 * root_order - 3, -1, -1))
        bhat = residual + promoted
        for activity_size in range(4, -1, -1):
            for active_residual_count in range(2, -1, -1):
                active_promoted_count = activity_size - active_residual_count
                if active_promoted_count < 0 or active_promoted_count > len(promoted):
                    continue
                active = set(residual[:active_residual_count]) | set(
                    promoted[:active_promoted_count]
                )
                needed = 4 - activity_size
                available = [label for label in promoted if label not in active]
                assert len(available) >= needed
                open_set = active | set(available[-needed:] if needed else ())
                contracted = set(bhat) - open_set
                assert len(open_set) == 4
                assert not ((open_set - active) & set(residual))

                for first_index in range(len(bhat) - 1, -1, -1):
                    for second_index in range(first_index - 1, -1, -1):
                        pair = {bhat[first_index], bhat[second_index]}
                        if pair <= open_set:
                            assert (set(bhat) - pair) == contracted | (open_set - pair)
                            assert len(open_set - pair) == 2
                        else:
                            assert pair & contracted
                            assert (pair & contracted) <= set(bhat) - active


def test_bitmask_matching_identity() -> None:
    actual = symbolic_hafnian((1 << 6) - 1, {})
    expected = expected_words()
    assert actual == expected
    assert len(actual) == 12


def test_target_weight_census() -> None:
    residual_values = ((2, 3, 5), (7, 11, 13))
    for active_mask in range(4):
        for color in range(3):
            beta = 1
            for index in range(2):
                if not (active_mask & (1 << index)):
                    beta = beta * residual_values[index][color] % PRIME
            assert beta != 0
            assert beta * pow(beta, PRIME - 2, PRIME) % PRIME == 1


def main() -> None:
    test_hostile_inactive_residual_boundary()
    test_reversed_activity_census()
    test_bitmask_matching_identity()
    test_target_weight_census()
    print("GLS54 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
