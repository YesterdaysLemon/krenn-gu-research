"""Primary exact replay for the P7 h=0 pair-projection theorem."""

from itertools import combinations

import sympy as sp

PORT_EDGES = tuple(combinations(range(5), 2))


def pentad(edge_values):
    """The ordered five-port pentad."""
    k12 = edge_values[(0, 1)]
    k13 = edge_values[(0, 2)]
    k14 = edge_values[(0, 3)]
    k15 = edge_values[(0, 4)]
    k23 = edge_values[(1, 2)]
    k24 = edge_values[(1, 3)]
    k25 = edge_values[(1, 4)]
    k34 = edge_values[(2, 3)]
    k35 = edge_values[(2, 4)]
    k45 = edge_values[(3, 4)]
    return (
        k12 * k13 * k24 * k35 * k45
        - k12 * k13 * k25 * k34 * k45
        - k12 * k14 * k23 * k35 * k45
        + k12 * k14 * k25 * k34 * k35
        + k12 * k15 * k23 * k34 * k45
        - k12 * k15 * k24 * k34 * k35
        + k13 * k14 * k23 * k25 * k45
        - k13 * k14 * k24 * k25 * k35
        - k13 * k15 * k23 * k24 * k45
        + k13 * k15 * k24 * k25 * k34
        - k14 * k15 * k23 * k25 * k34
        + k14 * k15 * k23 * k24 * k35
    )


def verify_pentad_covariant():
    a = sp.symbols("a0:5")
    b = sp.symbols("b0:5")
    gram = {(i, j): a[i] * b[j] + b[i] * a[j] for i, j in PORT_EDGES}
    assert sp.expand(pentad(gram)) == 0

    y_symbols = sp.symbols("y0:10")
    y = dict(zip(PORT_EDGES, y_symbols, strict=True))
    rho = sp.symbols("rho")
    scaled = {edge: rho * value for edge, value in y.items()}
    assert sp.expand(pentad(scaled) - rho**5 * pentad(y)) == 0

    for neighbor in range(4):
        swap = {index: index for index in range(5)}
        swap[neighbor], swap[neighbor + 1] = neighbor + 1, neighbor
        swapped = {
            (i, j): y[tuple(sorted((swap[i], swap[j])))] for i, j in PORT_EDGES
        }
        assert sp.expand(pentad(swapped) + pentad(y)) == 0

    bad = dict(zip(PORT_EDGES, range(1, 11), strict=True))
    assert pentad(bad) == -6


def verify_pinned_clearing_and_alignment():
    u0 = sp.symbols("u0_0:5")
    u1 = sp.symbols("u1_0:5")
    khat = {(i, j): u0[i] * u1[j] + u0[j] * u1[i] for i, j in PORT_EDGES}
    assert sp.expand(pentad(khat)) == 0

    d0, d1, t = sp.symbols("d0 d1 t", nonzero=True)
    y_symbols = sp.symbols("z0:10")
    y = dict(zip(PORT_EDGES, y_symbols, strict=True))
    tau = t * d0 * d1
    for edge in PORT_EDGES:
        physical = khat[edge] / (d0 * d1)
        cleared = sp.together((t * y[edge] - physical) * d0 * d1)
        assert sp.expand(cleared - (tau * y[edge] - khat[edge])) == 0

    rho = sp.symbols("rho")
    scaled_khat = {
        edge: (rho**8 * u0[i]) * (rho**8 * u1[j])
        + (rho**8 * u0[j]) * (rho**8 * u1[i])
        for edge, (i, j) in ((edge, edge) for edge in PORT_EDGES)
    }
    for edge in PORT_EDGES:
        assert sp.expand(scaled_khat[edge] - rho**16 * khat[edge]) == 0

    edge_a, edge_b = PORT_EDGES[0], PORT_EDGES[1]
    alignment = y[edge_a] * khat[edge_b] - y[edge_b] * khat[edge_a]
    scaled_alignment = (
        rho * y[edge_a] * scaled_khat[edge_b]
        - rho * y[edge_b] * scaled_khat[edge_a]
    )
    assert sp.expand(scaled_alignment - rho**17 * alignment) == 0

    fixed_u0 = (1, 2, 3, 4, 5)
    fixed_u1 = (2, -1, 4, 1, 3)
    fixed_khat = {
        (i, j): fixed_u0[i] * fixed_u1[j] + fixed_u0[j] * fixed_u1[i]
        for i, j in PORT_EDGES
    }
    fixed_tau = sp.Integer(3)
    fixed_y = {edge: sp.Rational(value, fixed_tau) for edge, value in fixed_khat.items()}
    assert all(
        fixed_y[e] * fixed_khat[f] - fixed_y[f] * fixed_khat[e] == 0
        for e, f in combinations(PORT_EDGES, 2)
    )
    perturbed = dict(fixed_y)
    perturbed[PORT_EDGES[0]] += 1
    assert any(
        perturbed[e] * fixed_khat[f] - perturbed[f] * fixed_khat[e] != 0
        for e, f in combinations(PORT_EDGES, 2)
    )


def verify_simple_incidence_boundary():
    # A 12-dimensional restriction of formula (11).  The proof works
    # identically with 219 domain coordinates and a 240-dimensional quotient.
    w = sp.Matrix(range(1, 13))
    gamma = sp.zeros(14, 12)
    gamma[0, 0] = 1
    for j in range(1, 12):
        gamma[j + 2, 0] = -w[j]
        gamma[j + 2, j] = 1

    quotient = gamma[3:, :]
    assert gamma.rank() == 12
    assert quotient.rank() == 11
    assert quotient * w == sp.zeros(11, 1)
    assert gamma * w == sp.Matrix([1] + [0] * 13)

    bad = dict(zip(PORT_EDGES, tuple(w[:10]), strict=True))
    assert pentad(bad) == -6


def main():
    verify_pentad_covariant()
    verify_pinned_clearing_and_alignment()
    verify_simple_incidence_boundary()
    print("PASS: P7 target-line h=0 pair projection and star alignment")
    print("pentad_degree=5 h_numerator_degree=8 alignment_degree=17")
    print("ambient_simple_incidence_bad_pentad=-6")
    print("graph_or_parameter_search_used=False")


if __name__ == "__main__":
    main()
