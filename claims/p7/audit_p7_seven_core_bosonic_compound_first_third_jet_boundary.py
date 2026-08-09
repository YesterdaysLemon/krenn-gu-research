"""Independent no-import audit of the seven-core first/third-jet boundary."""


CORE = tuple(range(7))


def combinations(values, size):
    if size == 0:
        yield ()
        return
    for index in range(len(values) - size + 1):
        head = values[index]
        for tail in combinations(values[index + 1 :], size - 1):
            yield (head,) + tail


EDGES = tuple(combinations(CORE, 2))
TRIPLES = tuple(combinations(CORE, 3))
JACOBIAN_COLUMNS = tuple(range(34)) + (35, 36, 37, 38, 39, 40, 42, 43)


def permutations(values):
    if not values:
        yield ()
        return
    for index, value in enumerate(values):
        rest = values[:index] + values[index + 1 :]
        for tail in permutations(rest):
            yield (value,) + tail


def product(values, modulus):
    result = 1
    for value in values:
        result = result * value % modulus
    return result


def permanent(matrix, modulus):
    return sum(
        product(
            (matrix[row][column] for row, column in enumerate(order)), modulus
        )
        for order in permutations(tuple(range(len(matrix))))
    ) % modulus


def hafnian_deleted(edge_values, deleted, modulus):
    remaining = tuple(vertex for vertex in CORE if vertex not in deleted)

    def recurse(vertices):
        if not vertices:
            return 1
        first = vertices[0]
        total = 0
        for position in range(1, len(vertices)):
            second = vertices[position]
            edge = (min(first, second), max(first, second))
            rest = vertices[1:position] + vertices[position + 1 :]
            total += edge_values[edge] * recurse(rest)
        return total % modulus

    return recurse(remaining)


def response_jacobian(modulus):
    def point_value(index):
        return (((index * index + 3 * index + 7) % 11) - 5) % modulus

    edge_values = {
        edge: point_value(index) for index, edge in enumerate(EDGES)
    }
    terminal_matrix = [
        [point_value(21 + 7 * row + column) for column in CORE]
        for row in CORE
    ]
    hafnians = {
        frozenset(deleted): hafnian_deleted(
            edge_values, frozenset(deleted), modulus
        )
        for size in (1, 3, 5)
        for deleted in combinations(CORE, size)
    }

    def subpermanent(rows, columns):
        matrix = [
            [terminal_matrix[row][column] for column in columns]
            for row in rows
        ]
        return permanent(matrix, modulus)

    jacobian = []
    for terminal in CORE:
        row = [
            sum(
                hafnians[frozenset((core, left, right))]
                * terminal_matrix[core][terminal]
                for core in CORE
                if core not in (left, right)
            )
            % modulus
            for left, right in EDGES
        ]
        row.extend(
            hafnians[frozenset((core,))] if terminal == column else 0
            for core in CORE
            for column in CORE
        )
        jacobian.append(row)

    for terminal_triple in TRIPLES:
        row = []
        for left, right in EDGES:
            derivative = sum(
                hafnians[frozenset(core_triple + (left, right))]
                * subpermanent(core_triple, terminal_triple)
                for core_triple in TRIPLES
                if left not in core_triple and right not in core_triple
            )
            row.append(derivative % modulus)
        for core in CORE:
            for terminal in CORE:
                derivative = 0
                if terminal in terminal_triple:
                    other_terminals = tuple(
                        value for value in terminal_triple if value != terminal
                    )
                    derivative = sum(
                        hafnians[frozenset(core_triple)]
                        * subpermanent(
                            tuple(value for value in core_triple if value != core),
                            other_terminals,
                        )
                        for core_triple in TRIPLES
                        if core in core_triple
                    )
                row.append(derivative % modulus)
        jacobian.append(row)
    return jacobian


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


def check_scaled_deconvolution():
    # A scalar is stored as 147*(a+b*rho), rho^2=21.  A diagonal tensor
    # coefficient is a triple of such pairs, one for each D_c.
    zero = (0, 0)
    unit = (147, 0)
    seventh = (21, 0)
    zero_vector = (zero, zero, zero)
    d0 = (unit, zero, zero)
    d1 = (zero, unit, zero)
    d2 = (zero, zero, unit)
    d2_seventh = (zero, zero, seventh)

    # Degree-three F ledger, indexed by surviving terminal sets.  These are
    # the nonzero size-four-deletion entries before Wick deconvolution.
    f_three = {
        "123": d0,
        "125": d0,
        "12a": d0,
        "135": d2,
        "15a": d2,
        "234": d1,
        "245": d2,
        "25b": d2,
        "345": d1,
        "34b": d1,
        "35a": d2,
        "45b": d2,
        "5ab": d2_seventh,
    }

    # Scaled values 147*(M_ij/7), needed because Phi_5=D_2/7.
    terminal_correction = {
        "12": (-21, -22),
        "14": (-21, -22),
        "23": (-21, -22),
        "34": (-21, -22),
        "13": unit,
        "24": unit,
        "1a": unit,
        "3a": unit,
        "2b": unit,
        "4b": unit,
        "1b": (0, -21),
        "2a": (0, -21),
        "3b": (0, -21),
        "4a": (0, -21),
        "ab": (21, -21),
    }

    def subtract_pair(left, right):
        return (left[0] - right[0], left[1] - right[1])

    terminals = ("1", "2", "3", "4", "5", "a", "b")
    phi_three = {}
    for triple in combinations(terminals, 3):
        key = "".join(triple)
        value = list(f_three.get(key, zero_vector))
        if "5" in triple:
            pair = "".join(item for item in triple if item != "5")
            correction = terminal_correction.get(pair, zero)
            value[2] = subtract_pair(value[2], correction)
        phi_three[key] = tuple(value)

    expected = {
        "123": d0,
        "125": (unit, zero, (21, 22)),
        "12a": d0,
        "145": (zero, zero, (21, 22)),
        "15b": (zero, zero, (0, 21)),
        "234": d1,
        "235": (zero, zero, (21, 22)),
        "25a": (zero, zero, (0, 21)),
        "345": (zero, unit, (21, 22)),
        "34b": d1,
        "35b": (zero, zero, (0, 21)),
        "45a": (zero, zero, (0, 21)),
        "5ab": (zero, zero, (0, 21)),
    }
    assert {
        key: value for key, value in phi_three.items() if value != zero_vector
    } == expected


def main():
    check_scaled_deconvolution()
    jacobian = response_jacobian(1009)
    minor = [[row[column] for column in JACOBIAN_COLUMNS] for row in jacobian]
    assert len(jacobian) == 42
    assert all(len(row) == 70 for row in jacobian)
    assert determinant_mod(minor, 1009) == 833
    print("PASS: independent scaled Wick ledger audit")
    print("PASS: fixed Jacobian minor is 833 mod 1009")
    print("SCOPE: no scalar degree-1/3 polynomial obstruction")


if __name__ == "__main__":
    main()
