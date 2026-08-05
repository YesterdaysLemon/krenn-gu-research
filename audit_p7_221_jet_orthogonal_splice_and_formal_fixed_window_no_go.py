"""Independent no-import audit of the P7 2+2+1 jet-orthogonal splice."""


ROOTS = tuple(range(5))
COLUMNS = tuple(range(5))
UNMARKED = tuple(range(1, 5))
RANK_TWO_PAIRS = {(0, 1), (2, 3)}
AXIS_LABELS = (0, 0, 1, 1, 2)


def choose(items, size):
    if size == 0:
        yield ()
        return
    if len(items) < size:
        return
    first, rest = items[0], items[1:]
    for tail in choose(rest, size - 1):
        yield (first,) + tail
    yield from choose(rest, size)


def permanent(matrix):
    if not matrix:
        return 1
    return sum(
        matrix[0][column]
        * permanent([row[:column] + row[column + 1 :] for row in matrix[1:]])
        for column in range(len(matrix))
    )


def submatrix(matrix, rows, columns):
    return [[matrix[row][column] for column in columns] for row in rows]


def complement(universe, chosen):
    return tuple(item for item in universe if item not in chosen)


def laplace_term(matrix, root_pair, retained):
    return permanent(submatrix(matrix, root_pair, retained)) * permanent(
        submatrix(
            matrix,
            complement(ROOTS, root_pair),
            complement(COLUMNS, retained),
        )
    )


def canonical_matrices():
    return (
        (
            (-1, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (-1, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
            (1, 1, 0, 1, 0),
        ),
        (
            (0, 1, 0, 0, 0),
            (-1, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (-1, 0, 0, 0, 1),
            (1, 0, 1, 0, 1),
        ),
        (
            (-1, 1, 0, 0, 0),
            (-1, 0, 1, 0, 0),
            (-1, 0, 0, 1, 0),
            (1, 0, 0, 0, 1),
            (1, 1, 0, 1, 0),
        ),
    )


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def scale(coefficient, polynomial):
    return {
        monomial: coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def variable(name):
    return {(name,): 1}


def product(polynomials):
    result = {(): 1}
    for polynomial in polynomials:
        result = multiply(result, polynomial)
    return result


def hafnian(vertices, blocks):
    if not vertices:
        return {(): 1}
    first = vertices[0]
    result = {}
    for position in range(1, len(vertices)):
        second = vertices[position]
        edge = blocks.get(tuple(sorted((first, second))), {})
        if edge:
            rest = vertices[1:position] + vertices[position + 1 :]
            result = add(result, multiply(edge, hafnian(rest, blocks)))
    return result


def basis(colour, coefficient=1):
    result = [0, 0, 0]
    result[colour] = coefficient
    return tuple(result)


def build_tangent_data():
    names = ("x1", "y1", "x2", "y2", "u3", "y3", "u4", "y4", "u5", "x5")
    x1, y1, x2, y2, u3, y3, u4, y4, u5, x5 = tuple(
        variable(name) for name in names
    )
    zero = {}
    local = (
        (zero, x1, y1),
        (zero, x2, y2),
        (u3, zero, y3),
        (u4, zero, y4),
        (u5, x5, zero),
    )
    p = (x1, y2, u3, y4, u5)
    q = (y1, x2, y3, u4, x5)
    root_blocks = {
        (0, 1): multiply(y1, y2),
        (2, 3): multiply(y3, y4),
        (0, 2): add(
            scale(-1, multiply(x1, y3)),
            scale(-1, multiply(y1, u3)),
            multiply(y1, y3),
        ),
        (0, 3): multiply(y1, y4),
        (1, 2): multiply(y2, y3),
        (1, 3): add(
            scale(-1, multiply(y2, u4)),
            scale(-1, multiply(x2, y4)),
            multiply(y2, y4),
        ),
        (0, 4): scale(-1, multiply(y1, u5)),
        (1, 4): multiply(x2, x5),
        (2, 4): multiply(u3, u5),
        (3, 4): scale(-1, multiply(y4, x5)),
    }
    residual_blocks = {
        (i, j): add(multiply(p[i], q[j]), multiply(q[i], p[j]))
        for i, j in choose(ROOTS, 2)
    }
    blocks = dict(root_blocks)
    for root in ROOTS:
        blocks[root, 5] = p[root]
        blocks[root, 6] = q[root]
    return local, root_blocks, residual_blocks, blocks


def build_ledger():
    ledger = {}
    singletons = {
        0: (basis(1), basis(2)),
        1: (basis(2), basis(1)),
        2: (basis(0), basis(2)),
        3: (basis(2), basis(0)),
        4: (basis(0), basis(1)),
    }
    for root, values in singletons.items():
        roots = frozenset((root,))
        ledger[roots, frozenset((5,))] = (values[0], 1)
        ledger[roots, frozenset((6,))] = (values[1], 1)

    pair_values = {
        (0, 1): ((0, -1, 1), basis(1)),
        (2, 3): ((-1, 0, 1), basis(0)),
        (0, 2): (basis(2), basis(2)),
        (0, 3): (basis(2), basis(0, 0)),
        (1, 2): (basis(2), basis(0, 0)),
        (1, 3): (basis(2), basis(2)),
        (0, 4): (basis(1), basis(1)),
        (1, 4): (basis(1), basis(0, 0)),
        (2, 4): (basis(0), basis(0, 0)),
        (3, 4): (basis(0), basis(0)),
    }
    for pair, values in pair_values.items():
        roots = frozenset(pair)
        ledger[roots, frozenset()] = (values[0], 1)
        ledger[roots, frozenset((5, 6))] = (values[1], 1)

    q0 = {(0, 1, 2): 2, (0, 2, 3): 2, (0, 1, 4): 1}
    q1 = {(0, 1, 3): 2, (1, 2, 3): 2, (2, 3, 4): 0}
    for triple in choose(ROOTS, 3):
        roots = frozenset(triple)
        ledger[roots, frozenset((5,))] = (
            basis(q0[triple]) if triple in q0 else basis(0, 0),
            1,
        )
        ledger[roots, frozenset((6,))] = (
            basis(q1[triple]) if triple in q1 else basis(0, 0),
            1,
        )

    for quartet in choose(ROOTS, 4):
        roots = frozenset(quartet)
        value = basis(2) if quartet == (0, 1, 2, 3) else basis(0, 0)
        denominator = 7 if quartet == (0, 1, 2, 3) else 1
        ledger[roots, frozenset()] = (value, denominator)
        ledger[roots, frozenset((5, 6))] = (value, denominator)

    roots = frozenset(ROOTS)
    ledger[roots, frozenset((5,))] = (basis(0, 0), 1)
    ledger[roots, frozenset((6,))] = (basis(0, 0), 1)
    return ledger


def independent(left, right):
    monomials = tuple(sorted(set(left) | set(right)))
    return any(
        left.get(first, 0) * right.get(second, 0)
        - left.get(second, 0) * right.get(first, 0)
        != 0
        for first, second in choose(monomials, 2)
    )


def audit_splice_projectors():
    frozen = (1, 1, 1)
    identity = tuple(tuple(int(row == column) for column in range(3)) for row in range(3))
    for axis in AXIS_LABELS:
        alpha = tuple(int(coordinate == axis) for coordinate in range(3))
        projection = tuple(
            tuple(identity[row][column] - frozen[row] * alpha[column] for column in range(3))
            for row in range(3)
        )
        assert tuple(sum(projection[row][column] * frozen[column] for column in range(3)) for row in range(3)) == (0, 0, 0)
        assert tuple(sum(alpha[row] * projection[row][column] for row in range(3)) for column in range(3)) == (0, 0, 0)
        for tangent_coordinate in range(3):
            if tangent_coordinate == axis:
                continue
            tangent = tuple(int(coordinate == tangent_coordinate) for coordinate in range(3))
            assert sum(alpha[index] * tangent[index] for index in range(3)) == 0
            assert tuple(
                sum(projection[row][column] * tangent[column] for column in range(3))
                for row in range(3)
            ) == tangent


def audit_lower_jets_and_companions():
    local, root_blocks, residual_blocks, blocks = build_tangent_data()
    ledger = build_ledger()
    for root, axis in enumerate(AXIS_LABELS):
        assert local[root][axis] == {}

    expected_minors = {
        (0, 1): (("y1", "y2"), ("x1", "x2"), 1),
        (0, 2): (("y1", "y3"), ("x1", "y3"), 1),
        (0, 3): (("y1", "y4"), ("u4", "x1"), 1),
        (0, 4): (("x1", "x5"), ("u5", "y1"), 1),
        (1, 2): (("y2", "y3"), ("u3", "x2"), 1),
        (1, 3): (("y2", "y4"), ("x2", "y4"), 1),
        (1, 4): (("x5", "y2"), ("x2", "x5"), -1),
        (2, 3): (("y3", "y4"), ("u3", "u4"), 1),
        (2, 4): (("u5", "y3"), ("u3", "u5"), -1),
        (3, 4): (("x5", "y4"), ("u4", "u5"), -1),
    }
    for pair, (left_names, right_names, expected) in expected_minors.items():
        left_monomial = tuple(sorted(left_names))
        right_monomial = tuple(sorted(right_names))
        determinant = (
            root_blocks[pair].get(left_monomial, 0)
            * residual_blocks[pair].get(right_monomial, 0)
            - root_blocks[pair].get(right_monomial, 0)
            * residual_blocks[pair].get(left_monomial, 0)
        )
        assert determinant == expected
        assert independent(root_blocks[pair], residual_blocks[pair])

    checked = 0
    for size in range(1, 6):
        for roots_tuple in choose(ROOTS, size):
            tags = (
                (frozenset(), frozenset((5, 6)))
                if size % 2 == 0
                else (frozenset((5,)), frozenset((6,)))
            )
            graph = ({}, {}, {})
            denominator = ledger[frozenset(roots_tuple), tags[0]][1]
            for tag in tags:
                coefficients, tag_denominator = ledger[frozenset(roots_tuple), tag]
                assert tag_denominator == denominator
                companion = hafnian(tuple(sorted(roots_tuple + tuple(tag))), blocks)
                graph = tuple(
                    add(graph[colour], scale(coefficients[colour], companion))
                    for colour in range(3)
                )
            target = tuple(
                product(local[root][colour] for root in roots_tuple)
                for colour in range(3)
            )
            assert all(
                graph[colour] == scale(denominator, target[colour])
                for colour in range(3)
            )
            checked += 1
    assert checked == 31 and len(ledger) == 62
    return root_blocks, residual_blocks


def audit_fixed_windows(root_blocks, residual_blocks):
    checked = 0
    for matrix in canonical_matrices():
        matrix_lists = [list(row) for row in matrix]
        assert permanent(matrix_lists) == -1
        for retained in choose(UNMARKED, 2):
            terms = {
                root_pair: laplace_term(matrix_lists, root_pair, retained)
                for root_pair in choose(ROOTS, 2)
            }
            assert sum(terms.values()) == -1
            assert terms[(0, 1)] == terms[(2, 3)] == 0
            active = [pair for pair, value in terms.items() if value]
            assert active and all(pair not in RANK_TWO_PAIRS for pair in active)
            assert all(independent(root_blocks[pair], residual_blocks[pair]) for pair in active)
            checked += 1
    assert checked == 18


def main():
    audit_splice_projectors()
    root_blocks, residual_blocks = audit_lower_jets_and_companions()
    audit_fixed_windows(root_blocks, residual_blocks)
    print("PASS: independent exact jet-orthogonal projector audit")
    print("PASS: independent sparse-polynomial audit of all 31 lower jets")
    print("PASS: independent integer audit of all 18 fixed windows")
    print("PASS: independent companion-minor audit at every root pair")
    print("SCOPE: common tensor hafnian ledger and marked-star fan remain UNRESOLVED")


if __name__ == "__main__":
    main()
