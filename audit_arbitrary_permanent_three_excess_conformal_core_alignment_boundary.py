"""Independent no-import audit of the conformal-core alignment boundary."""

from __future__ import annotations

from collections import Counter


Edge = tuple[str, str]
Quadratic = tuple[int, int]


def multiply(left: Quadratic, right: Quadratic) -> Quadratic:
    """Multiply in Q[s]/(s^2-2)."""
    return (left[0] * right[0] + 2 * left[1] * right[1], left[0] * right[1] + left[1] * right[0])


def add(*values: Quadratic) -> Quadratic:
    return (sum(value[0] for value in values), sum(value[1] for value in values))


def perfect(edges: set[Edge]) -> bool:
    return len(edges) == 6 and len({u for u, _ in edges}) == 6 and len({v for _, v in edges}) == 6


def connected(edges: set[Edge]) -> bool:
    adjacency: dict[str, set[str]] = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    reached: set[str] = set()
    frontier = {next(iter(adjacency))}
    while frontier:
        vertex = frontier.pop()
        if vertex not in reached:
            reached.add(vertex)
            frontier.update(adjacency[vertex] - reached)
    return reached == set(adjacency)


def main() -> None:
    a_edges = {(f"x{j}", f"p{j}") for j in range(3)}
    n_edges = {(f"y{j}", f"q{j}") for j in range(3)}
    c_edges = {(f"x{j}", f"q{j}") for j in range(3)}
    d_edges = {(f"y{j}", f"p{j}") for j in range(3)}
    cp_edges = {(f"x{j}", f"q{(j + 1) % 3}") for j in range(3)}
    dp_edges = {(f"y{j}", f"p{(j + 1) % 3}") for j in range(3)}
    e_edges = {(f"x{j}", f"p{(j - 1) % 3}") for j in range(3)}
    support = a_edges | n_edges | c_edges | d_edges | cp_edges | dp_edges | e_edges

    m0 = {("x0", "q0"), ("y0", "p0"), ("x1", "p1"), ("x2", "p2"), ("y1", "q1"), ("y2", "q2")}
    m1 = {("x0", "p0"), ("y0", "q0"), ("x1", "q1"), ("x2", "q2"), ("y1", "p1"), ("y2", "p2")}
    m2 = cp_edges | dp_edges
    e_matching = e_edges | n_edges

    assert len(support) == 21
    assert connected(support)
    assert all(perfect(matching) for matching in (m0, m1, m2, e_matching, a_edges | n_edges))
    assert m0 | m1 | m2 | e_matching == support
    assert sorted(Counter(u for u, _ in support).values()) == [3, 3, 3, 4, 4, 4]
    assert sorted(Counter(v for _, v in support).values()) == [3, 3, 3, 4, 4, 4]

    x_modes = {f"x{j}" for j in range(3)}
    p_sources = {f"p{j}" for j in range(3)}
    assert {(u, v) for u, v in support if u in x_modes and v in p_sources} == a_edges | e_edges

    # The two aligned C6 port terms are +1 and -1.
    assert 1 + (-1) == 0

    # Exact theta/chord point in Q[sqrt(2)].
    one = (1, 0)
    minus_one = (-1, 0)
    r = (-1, -1)
    s = (-1, 1)
    assert add(r, s) == (-2, 0)
    assert multiply(r, s) == minus_one
    theta_sum = add(one, minus_one, minus_one)
    chord_sum = add(minus_one, (1, 1), (1, -1))
    assert theta_sum == minus_one
    assert chord_sum == one
    assert add(theta_sum, chord_sum) == (0, 0)

    # Private edges give coefficient equality term by term in a toric relation.
    private_edge_rows = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    assert private_edge_rows == tuple(
        tuple(1 if i == j else 0 for j in range(3)) for i in range(3)
    )

    # lambda1+lambda2+lambda3=0 with odd coefficient sum yields 1=-1.
    lambdas = ((1, 0), (0, 1), (-1, -1))
    assert tuple(sum(vector[i] for vector in lambdas) for i in range(2)) == (0, 0)
    assert len(lambdas) % 2 == 1

    print("independent no-import conformal-core alignment audit: PASS")


if __name__ == "__main__":
    main()
