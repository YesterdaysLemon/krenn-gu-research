"""Independent no-import audit of the three scalar 2+2+1 hafnian charts."""


P = ("1", "2", "3", "4", "5", "a", "b")
Q = frozenset(("a", "b"))


def gcd(left, right):
    left, right = abs(left), abs(right)
    while right:
        left, right = right, left % right
    return left


def rat(numerator, denominator=1):
    assert denominator
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    divisor = gcd(numerator, denominator)
    return (numerator // divisor, denominator // divisor)


def radd(left, right):
    return rat(left[0] * right[1] + right[0] * left[1], left[1] * right[1])


def rneg(value):
    return (-value[0], value[1])


def rmul(left, right):
    return rat(left[0] * right[0], left[1] * right[1])


def kval(rational=0, radical=0):
    left = rational if isinstance(rational, tuple) else rat(rational)
    right = radical if isinstance(radical, tuple) else rat(radical)
    return (left, right)


ZERO = kval()
ONE = kval(1)


def kadd(left, right):
    return (radd(left[0], right[0]), radd(left[1], right[1]))


def kneg(value):
    return (rneg(value[0]), rneg(value[1]))


def kmul(left, right):
    # (a+b*rho)(c+d*rho)=(ac+21bd)+(ad+bc)rho.
    rational = radd(rmul(left[0], right[0]), rmul(rat(21), rmul(left[1], right[1])))
    radical = radd(rmul(left[0], right[1]), rmul(left[1], right[0]))
    return (rational, radical)


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


def add_edge(graph, left, right, weight):
    key = frozenset((left, right))
    assert left != right and key not in graph
    graph[key] = weight


def evaluator(graph):
    cache = {(): ONE}

    def hafnian(vertices):
        vertices = tuple(sorted(vertices))
        if vertices in cache:
            return cache[vertices]
        if len(vertices) % 2:
            return ZERO
        first = vertices[0]
        total = ZERO
        for position in range(1, len(vertices)):
            second = vertices[position]
            edge = graph.get(frozenset((first, second)), ZERO)
            if edge != ZERO:
                rest = vertices[1:position] + vertices[position + 1 :]
                total = kadd(total, kmul(edge, hafnian(rest)))
        cache[vertices] = total
        return total

    return hafnian


def ledger():
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in choose(P, size)
        if not (size == 2 and frozenset(deletion) == Q)
    ]
    result = {color: {deletion: ZERO for deletion in prescribed} for color in range(3)}

    def assign(deletion, color, value=ONE):
        result[color][frozenset(deletion)] = value

    for deletion, color in {
        "1a": 1,
        "1b": 2,
        "2a": 2,
        "2b": 1,
        "3a": 0,
        "3b": 2,
        "4a": 2,
        "4b": 0,
        "5a": 0,
        "5b": 1,
    }.items():
        assign(deletion, color)

    assign("12", 1, kval(-1))
    assign("12", 2)
    assign("12ab", 1)
    assign("34", 0, kval(-1))
    assign("34", 2)
    assign("34ab", 0)
    for pair, color, with_q in (
        ("13", 2, True),
        ("14", 2, False),
        ("23", 2, False),
        ("24", 2, True),
        ("15", 1, True),
        ("25", 1, False),
        ("35", 0, False),
        ("45", 0, True),
    ):
        assign(pair, color)
        if with_q:
            assign(pair + "ab", color)
    for deletion, color in {
        "123a": 2,
        "124b": 2,
        "134a": 2,
        "234b": 2,
        "125a": 1,
        "345b": 0,
    }.items():
        assign(deletion, color)
    assign("1234", 2, kval(rat(1, 7)))
    assign("1234ab", 2, kval(rat(1, 7)))
    return result


def coordinate_graph(color):
    graph = {}
    core = tuple(f"z_{terminal}" for terminal in P)
    for terminal, core_vertex in zip(P, core, strict=True):
        add_edge(graph, terminal, core_vertex, ONE)
    edges = {
        0: {"3a": 1, "4b": 1, "5a": 1, "35": 1, "45": 1, "34": -1},
        1: {"1a": 1, "2b": 1, "5b": 1, "15": 1, "25": 1, "12": -1},
    }
    for pair, weight in edges[color].items():
        add_edge(graph, f"z_{pair[0]}", f"z_{pair[1]}", kval(weight))
    return graph, core


def color_two_graph():
    graph = {}
    core = ("z_*", "z_1", "z_2", "z_3", "z_4", "z_5", "z_6")
    rho = kval(0, 1)
    inverse_rho = kval(0, rat(1, 21))
    kappa = kval(1, rat(22, 21))
    add_edge(graph, "5", "z_*", kval(rat(1, 7)))
    add_edge(graph, "z_1", "z_2", ONE)
    add_edge(graph, "z_3", "z_4", inverse_rho)
    add_edge(graph, "z_5", "z_6", rho)
    rows = {
        "z_1": ("1", "3"),
        "z_2": ("2", "4"),
        "z_3": ("a", "1", "3"),
        "z_4": ("b", "2", "4"),
        "z_5": ("1", "3"),
        "z_6": ("2", "4"),
    }
    for core_vertex, terminals in rows.items():
        for terminal in terminals:
            add_edge(graph, core_vertex, terminal, ONE)
    direct = {
        "12": kneg(kappa),
        "14": kneg(kappa),
        "23": kneg(kappa),
        "34": kneg(kappa),
        "13": kval(7),
        "24": kval(7),
        "1a": kval(7),
        "3a": kval(7),
        "2b": kval(7),
        "4b": kval(7),
        "1b": kneg(rho),
        "2a": kneg(rho),
        "3b": kneg(rho),
        "4a": kneg(rho),
        "ab": kadd(ONE, kneg(rho)),
    }
    for pair, weight in direct.items():
        add_edge(graph, pair[0], pair[1], weight)
    return graph, core


def cofactor(deletion, core, hafnian):
    terminals = tuple(terminal for terminal in P if terminal not in deletion)
    return hafnian(core + terminals)


def main() -> None:
    expected = ledger()
    assert all(len(chart) == 62 for chart in expected.values())
    checked = 0
    for color in (0, 1):
        graph, core = coordinate_graph(color)
        hafnian = evaluator(graph)
        for deletion, value in expected[color].items():
            assert cofactor(deletion, core, hafnian) == value
            checked += 1
        assert cofactor(Q, core, hafnian) == ZERO
        assert cofactor(frozenset(), core, hafnian) == ONE

    graph, core = color_two_graph()
    hafnian = evaluator(graph)
    for deletion, value in expected[2].items():
        assert cofactor(deletion, core, hafnian) == value
        checked += 1
    assert cofactor(Q, core, hafnian) == kval(rat(103, 147))
    assert cofactor(frozenset(), core, hafnian) == kval(rat(103, 147), 36)
    assert checked == 186

    print("PASS: independent exact Q(sqrt(21)) scalar-hafnian audit")
    print("PASS: all 186 prescribed ledger coordinates")
    print("SCOPE: common terminal block and mixed words remain UNRESOLVED")


if __name__ == "__main__":
    main()
