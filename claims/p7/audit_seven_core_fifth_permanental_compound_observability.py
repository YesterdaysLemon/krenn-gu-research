"""Independent no-import audit of fifth-compound observability."""


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


def permanent_mod(matrix, modulus):
    states = {0: 1}
    for row in matrix:
        next_states = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                next_mask = mask | bit
                next_states[next_mask] = (
                    next_states.get(next_mask, 0) + coefficient * value
                ) % modulus
        states = next_states
    return states.get((1 << len(matrix)) - 1, 0)


def compound_mod(incidence, modulus):
    compound = []
    for face in TERMINAL_FACES:
        row = []
        for deleted_pair in CORE_PAIRS:
            surviving_rows = [
                index for index in INDICES if index not in deleted_pair
            ]
            submatrix = [
                [incidence[index][column] for column in face]
                for index in surviving_rows
            ]
            row.append(permanent_mod(submatrix, modulus))
        compound.append(row)
    return compound


def determinant_mod(matrix, modulus):
    work = [[value % modulus for value in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column] != 0
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % modulus
        inverse = pow(pivot_value, modulus - 2, modulus)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * inverse % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[column])
                ]
    return determinant % modulus


def fixed_incidence(modulus, rho):
    inverse_7 = pow(7, modulus - 2, modulus)
    inverse_21 = pow(21, modulus - 2, modulus)
    incidence = [[0 for _ in INDICES] for _ in INDICES]
    incidence[0][4] = inverse_7
    incidence[1][0] = incidence[1][2] = 1
    incidence[2][1] = incidence[2][3] = 1
    incidence[3][2] = 1
    incidence[3][6] = -rho % modulus
    incidence[4][3] = 1
    incidence[4][6] = (-5 - 2 * rho * inverse_21) % modulus
    incidence[5][4] = 1
    incidence[5][6] = (230 + 104 * rho * inverse_7) % modulus
    incidence[6][5] = 1
    incidence[6][6] = (1 + 16 * rho * inverse_21) % modulus
    return incidence


def check_complement_identity():
    rows_seen = []
    for face in TERMINAL_FACES:
        row = []
        for deleted_pair in CORE_PAIRS:
            surviving = tuple(
                index for index in INDICES if index not in deleted_pair
            )
            # The permanent of an identity submatrix is one exactly when its
            # row and column index sets agree.
            row.append(int(face == surviving))
        assert sum(row) == 1
        rows_seen.append(tuple(row))
    assert len(set(rows_seen)) == 21


def main():
    check_complement_identity()
    modulus = 101
    rho = 18
    assert rho * rho % modulus == 21
    compound = compound_mod(fixed_incidence(modulus, rho), modulus)
    assert len(compound) == 21
    assert all(len(row) == 21 for row in compound)
    assert determinant_mod(compound, modulus) == 91
    print("PASS: independent complement-index identity audit")
    print("PASS: fixed C5 determinant is 91 mod 101 at rho=18")
    print("SCOPE: full-rank certificate only; no four-face circuit duplication")


if __name__ == "__main__":
    main()
