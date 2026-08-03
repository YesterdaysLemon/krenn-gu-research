"""Independent no-import audit of the strict two-endpoint 2+2+1 checkpoint."""


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def scale(coefficient, polynomial):
    return {monomial: coefficient * value for monomial, value in polynomial.items() if coefficient * value}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, 0) + left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def variable(name):
    return {(name,): 1}


def product(polynomials):
    result = {(): 1}
    for polynomial in polynomials:
        result = multiply(result, polynomial)
    return result


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


def hafnian(vertices, blocks):
    if not vertices:
        return {(): 1}
    first = vertices[0]
    total = {}
    for position in range(1, len(vertices)):
        second = vertices[position]
        edge = blocks.get(tuple(sorted((first, second))), {})
        if edge:
            rest = vertices[1:position] + vertices[position + 1 :]
            total = add(total, multiply(edge, hafnian(rest, blocks)))
    return total


def basis(color, coefficient=1):
    result = [0, 0, 0]
    result[color] = coefficient
    return tuple(result)


def build_data():
    names = ["x1", "y1", "x2", "y2", "u3", "y3", "u4", "y4", "u5", "x5"]
    x1, y1, x2, y2, u3, y3, u4, y4, u5, x5 = tuple(variable(name) for name in names)
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
    b = {
        (0, 1): multiply(y1, y2),
        (2, 3): multiply(y3, y4),
        (0, 2): add(scale(-1, multiply(x1, y3)), scale(-1, multiply(y1, u3)), multiply(y1, y3)),
        (0, 3): multiply(y1, y4),
        (1, 2): multiply(y2, y3),
        (1, 3): add(scale(-1, multiply(y2, u4)), scale(-1, multiply(x2, y4)), multiply(y2, y4)),
        (0, 4): scale(-1, multiply(y1, u5)),
        (1, 4): multiply(x2, x5),
        (2, 4): multiply(u3, u5),
        (3, 4): scale(-1, multiply(y4, x5)),
    }
    h = {}
    for i, j in choose(tuple(range(5)), 2):
        h[i, j] = add(multiply(p[i], q[j]), multiply(q[i], p[j]))
    blocks = dict(b)
    for i in range(5):
        blocks[i, 5] = p[i]
        blocks[i, 6] = q[i]
    return local, b, h, blocks


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
        ledger[frozenset((root,)), frozenset((5,))] = (values[0], 1)
        ledger[frozenset((root,)), frozenset((6,))] = (values[1], 1)

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
    for triple in choose(tuple(range(5)), 3):
        roots = frozenset(triple)
        ledger[roots, frozenset((5,))] = (basis(q0[triple]) if triple in q0 else basis(0, 0), 1)
        ledger[roots, frozenset((6,))] = (basis(q1[triple]) if triple in q1 else basis(0, 0), 1)

    for quartet in choose(tuple(range(5)), 4):
        roots = frozenset(quartet)
        value = basis(2) if quartet == (0, 1, 2, 3) else basis(0, 0)
        denominator = 7 if quartet == (0, 1, 2, 3) else 1
        ledger[roots, frozenset()] = (value, denominator)
        ledger[roots, frozenset((5, 6))] = (value, denominator)

    roots = frozenset(range(5))
    ledger[roots, frozenset((5,))] = (basis(0, 0), 1)
    ledger[roots, frozenset((6,))] = (basis(0, 0), 1)
    return ledger


def main() -> None:
    # Independent sparse-polynomial check of the unique mixed coefficients
    # used in the same-axis contradiction.
    a, c = variable("A"), variable("C")
    x1, y1, x2, y2, x3, y3 = tuple(
        variable(name) for name in ["X1", "Y1", "X2", "Y2", "X3", "Y3"]
    )
    px, py, qx, qy = tuple(
        variable(name) for name in ["PX", "PY", "QX", "QY"]
    )
    b12 = add(multiply(a, multiply(x1, x2)), multiply(c, multiply(y1, y2)))
    p3 = add(multiply(px, x3), multiply(py, y3))
    q3 = add(multiply(qx, x3), multiply(qy, y3))
    assert multiply(b12, p3)[tuple(sorted(("A", "PY", "X1", "X2", "Y3")))] == 1
    assert multiply(b12, q3)[tuple(sorted(("A", "QY", "X1", "X2", "Y3")))] == 1
    assert multiply(b12, p3)[tuple(sorted(("C", "PX", "X3", "Y1", "Y2")))] == 1
    assert multiply(b12, q3)[tuple(sorted(("C", "QX", "X3", "Y1", "Y2")))] == 1

    local, b, h, blocks = build_data()
    ledger = build_ledger()

    # Pair correction identities: same-axis pairs use two diagonal classes;
    # unlike pairs have B=lambda H+one shared-colour monomial.
    lambdas = {(0, 2): -1, (1, 3): -1, (0, 4): -1, (3, 4): -1}
    shared = {
        (0, 2): multiply(local[0][2], local[2][2]),
        (0, 3): multiply(local[0][2], local[3][2]),
        (1, 2): multiply(local[1][2], local[2][2]),
        (1, 3): multiply(local[1][2], local[3][2]),
        (0, 4): multiply(local[0][1], local[4][1]),
        (1, 4): multiply(local[1][1], local[4][1]),
        (2, 4): multiply(local[2][0], local[4][0]),
        (3, 4): multiply(local[3][0], local[4][0]),
    }
    for pair, target in shared.items():
        assert add(b[pair], scale(-lambdas.get(pair, 0), h[pair])) == target

    # All lower-root equations follow from the same blocks and one labelled
    # deletion-state ledger.  Denominators are cleared exactly; only 1234
    # uses denominator seven.
    checked = 0
    for size in range(1, 6):
        for roots_tuple in choose(tuple(range(5)), size):
            tags = (frozenset(), frozenset((5, 6))) if size % 2 == 0 else (frozenset((5,)), frozenset((6,)))
            graph = ({}, {}, {})
            denominator = ledger[frozenset(roots_tuple), tags[0]][1]
            for tag in tags:
                coefficients, tag_denominator = ledger[frozenset(roots_tuple), tag]
                assert tag_denominator == denominator
                companion = hafnian(tuple(sorted(roots_tuple + tuple(tag))), blocks)
                graph = tuple(add(graph[color], scale(coefficients[color], companion)) for color in range(3))
            target = tuple(product(local[root][color] for root in roots_tuple) for color in range(3))
            assert all(graph[color] == scale(denominator, target[color]) for color in range(3))
            checked += 1
    assert checked == 31 and len(ledger) == 62

    print("PASS: independent sparse-polynomial two-endpoint audit")
    print("PASS: common 2+2+1 blocks and all lower-root equations")
    print("PASS: exact denominator-seven quartet cancellation")
    print("SCOPE: formal cofactors are not a common principal-hafnian realization")


if __name__ == "__main__":
    main()
