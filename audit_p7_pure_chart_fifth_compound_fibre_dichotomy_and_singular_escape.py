"""Independent no-import audit of the fifth-compound singular escape."""


def combinations(values, size):
    if size == 0:
        yield ()
        return
    for index in range(len(values) - size + 1):
        head = values[index]
        for tail in combinations(values[index + 1 :], size - 1):
            yield (head,) + tail


INDICES = tuple(range(7))
CORE_PAIRS = tuple(combinations(INDICES, 2))
TERMINAL_FACES = tuple(combinations(INDICES, 5))


def gcd(left, right):
    left, right = abs(left), abs(right)
    while right:
        left, right = right, left % right
    return left


def rational(numerator, denominator=1):
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    divisor = gcd(numerator, denominator)
    return (numerator // divisor, denominator // divisor)


def rational_add(left, right):
    return rational(
        left[0] * right[1] + right[0] * left[1], left[1] * right[1]
    )


def rational_negative(value):
    return (-value[0], value[1])


def rational_multiply(left, right):
    return rational(left[0] * right[0], left[1] * right[1])


RATIONAL_ZERO = rational(0)
RATIONAL_ONE = rational(1)
FIELD_ZERO = (RATIONAL_ZERO, RATIONAL_ZERO)
FIELD_ONE = (RATIONAL_ONE, RATIONAL_ZERO)
RHO = (RATIONAL_ZERO, RATIONAL_ONE)


def field_add(left, right):
    return (
        rational_add(left[0], right[0]),
        rational_add(left[1], right[1]),
    )


def field_negative(value):
    return (rational_negative(value[0]), rational_negative(value[1]))


def field_multiply(left, right):
    return (
        rational_add(
            rational_multiply(left[0], right[0]),
            rational_multiply(rational(21), rational_multiply(left[1], right[1])),
        ),
        rational_add(
            rational_multiply(left[0], right[1]),
            rational_multiply(left[1], right[0]),
        ),
    )


def field_sum(values):
    result = FIELD_ZERO
    for value in values:
        result = field_add(result, value)
    return result


def field_value(constant=0, rho_coefficient=0, denominator=1):
    return (rational(constant, denominator), rational(rho_coefficient, denominator))


def permanent(matrix):
    states = {0: FIELD_ONE}
    for row in matrix:
        next_states = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                next_mask = mask | bit
                contribution = field_multiply(coefficient, value)
                next_states[next_mask] = field_add(
                    next_states.get(next_mask, FIELD_ZERO), contribution
                )
        states = next_states
    return states.get((1 << len(matrix)) - 1, FIELD_ZERO)


def fifth_compound(incidence):
    return [
        [
            permanent(
                [
                    [incidence[row][column] for column in face]
                    for row in INDICES
                    if row not in deleted_pair
                ]
            )
            for deleted_pair in CORE_PAIRS
        ]
        for face in TERMINAL_FACES
    ]


def rank_mod(matrix, modulus, rho):
    def reduce_rational(value):
        return value[0] * pow(value[1], modulus - 2, modulus) % modulus

    work = [
        [
            (
                reduce_rational(value[0])
                + rho * reduce_rational(value[1])
            )
            % modulus
            for value in row
        ]
        for row in matrix
    ]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], modulus - 2, modulus)
        for row in range(rank + 1, len(work)):
            factor = work[row][column] * inverse % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
    return rank


def main():
    incidence = [
        [FIELD_ONE, FIELD_ZERO, FIELD_ONE, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO],
        [FIELD_ONE, FIELD_ZERO, FIELD_ONE, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO],
        [FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, field_value(1, 0, 7), FIELD_ZERO, FIELD_ZERO],
        [FIELD_ZERO, FIELD_ZERO, FIELD_ONE, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, field_value(0, -1)],
        [FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ONE, FIELD_ZERO, FIELD_ZERO, field_value(-105, -2, 21)],
        [FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ONE, FIELD_ZERO, field_value(1610, 104, 7)],
        [FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ZERO, FIELD_ONE, field_value(21, 16, 21)],
    ]
    compound = fifth_compound(incidence)
    for other in range(2, 7):
        left = CORE_PAIRS.index((0, other))
        right = CORE_PAIRS.index((1, other))
        assert all(row[left] == row[right] for row in compound)
    assert rank_mod(compound, 101, 18) == 6

    edge_values = {pair: FIELD_ZERO for pair in CORE_PAIRS}
    edge_values.update(
        {
            (3, 5): RHO,
            (4, 5): field_value(-126, -1, 21),
            (4, 6): field_value(0, 1, 21),
            (5, 6): field_value(21, 22, 21),
            (0, 3): field_value(-16905, 1092, 84463),
            (0, 4): field_value(5747, -4778, 84463),
            (0, 5): field_value(0, -2),
            (0, 6): field_value(16618, -339, 84463),
        }
    )
    edge_vector = [edge_values[pair] for pair in CORE_PAIRS]
    response = [
        field_sum(
            field_multiply(left, right)
            for left, right in zip(row, edge_vector)
        )
        for row in compound
    ]
    assert response == [FIELD_ZERO] * 21

    print("PASS: independent proportional-row singularity audit")
    print("PASS: a good reduction of the compound has rank 6")
    print("PASS: exact quadratic-field edge vector kills all 21 faces")
    print("SCOPE: one degree-five fibre escape; other degrees and words open")


if __name__ == "__main__":
    main()
