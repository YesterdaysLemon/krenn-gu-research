"""Independent Fraction audit of the GLS33 residual-Laurent control.

This audit imports neither SymPy nor any repository theorem/verifier module.
It independently rebuilds the rational GLS32 graph, expands perfect matchings
recursively, collects the four residual-colour coefficient tables, and checks
the constant-deck kernel defect using only ``fractions.Fraction``.
"""

from __future__ import annotations

from fractions import Fraction as F
from functools import cache
from itertools import product

A0, A1, Q0, Q1, K, U1, U2, U3 = range(8)
VERTICES = tuple(range(8))
PORTS = (K, U1, U2, U3)
ONE = (F(1), F(1), F(1))
E0 = (F(1), F(0), F(0))
E1 = (F(0), F(1), F(0))
E2 = (F(0), F(0), F(1))


def zero_matrix():
    return tuple(tuple(F(0) for _ in range(3)) for _ in range(3))


def unit(row, column):
    return tuple(
        tuple(F(int(i == row and j == column)) for j in range(3)) for i in range(3)
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))


def outer(left, right):
    return tuple(tuple(F(left[i]) * F(right[j]) for j in range(3)) for i in range(3))


def add(left, right):
    return tuple(tuple(left[i][j] + right[i][j] for j in range(3)) for i in range(3))


def scale(value, matrix):
    return tuple(tuple(F(value) * entry for entry in row) for row in matrix)


def put(edges, left, right, matrix):
    if left < right:
        edges[left, right] = matrix
    else:
        edges[right, left] = transpose(matrix)


def edge(edges, left, right):
    if left < right:
        return edges.get((left, right), zero_matrix())
    return transpose(edges.get((right, left), zero_matrix()))


def build_graph():
    edges = {}
    e00, e11, e22 = unit(0, 0), unit(1, 1), unit(2, 2)
    w = (F(0), F(1), F(1))
    j = outer(w, w)

    put(edges, A0, Q0, e11)
    put(edges, A0, Q1, e22)
    put(edges, A1, Q0, e22)
    put(edges, A1, Q1, e11)
    put(edges, Q0, Q1, e00)
    put(edges, A0, K, outer((1, 0, -1), E0))
    put(edges, A1, K, outer((1, 1, -2), E0))
    for root in (A0, A1):
        for port in (U1, U2, U3):
            put(edges, root, port, e00)

    weights = {K: F(1), U1: F(1), U2: F(1), U3: F(1, 12)}
    for port, value in weights.items():
        put(edges, Q0, port, scale(value, outer(E0, (0, 1, 1))))
        put(edges, Q1, port, scale(-value, outer(E0, (0, 1, 1))))

    response_scalars = {
        (K, U1): F(1),
        (K, U2): F(1),
        (K, U3): F(-3, 2),
        (U1, U2): F(1),
        (U1, U3): F(1),
        (U2, U3): F(-2),
    }
    for (left, right), value in response_scalars.items():
        correction = scale(2 * weights[left] * weights[right], j)
        put(edges, left, right, add(scale(value, e00), correction))
    return edges


EDGES = build_graph()


def recursive_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in recursive_matchings(rest):
            yield ((first, second),) + tail


FULL_MATCHINGS = tuple(recursive_matchings(VERTICES))
PORT_MATCHINGS = tuple(recursive_matchings(PORTS))


@cache
def coefficient(word):
    total = F(0)
    for matching in FULL_MATCHINGS:
        term = F(1)
        for left, right in matching:
            term *= edge(EDGES, left, right)[word[left]][word[right]]
        total += term
    return total


def dot(left, right):
    return sum(F(left[i]) * F(right[i]) for i in range(3))


def row_times(left, matrix):
    return tuple(sum(F(left[i]) * matrix[i][j] for i in range(3)) for j in range(3))


def matrix_times(matrix, right):
    return tuple(sum(matrix[i][j] * F(right[j]) for j in range(3)) for i in range(3))


def resolved_profile(left_vector, right_vector):
    failures = {}
    for q0, q1, *port_values in product(range(3), repeat=6):
        ports = tuple(port_values)
        observed = sum(
            left_vector[a0] * right_vector[a1] * coefficient((a0, a1, q0, q1, *ports))
            for a0, a1 in product(range(3), repeat=2)
        )
        expected = F(0)
        if q0 == q1 and ports == (q0, q0, q0, q0):
            expected = left_vector[q0] * right_vector[q0]
        defect = observed - expected
        if defect:
            failures[q0, q1, *ports] = defect
    return failures


def support_by_residual_pair(failures):
    support = {}
    for word in failures:
        pair = word[:2]
        support[pair] = support.get(pair, 0) + 1
    return support


def sample_coefficients(failures, ports):
    return {word[:2]: value for word, value in failures.items() if word[2:] == ports}


def contract_residual_ones(failures):
    answer = {}
    for ports in product(range(3), repeat=4):
        total = sum(value for word, value in failures.items() if word[2:] == ports)
        if total:
            answer[ports] = total
    return answer


def audit_residual_profiles():
    profiles = {
        "00": resolved_profile(ONE, ONE),
        "10": resolved_profile(E0, ONE),
        "01": resolved_profile(ONE, E0),
        "11": resolved_profile(E0, E0),
    }
    counts = {name: len(table) for name, table in profiles.items()}
    assert counts == {"00": 200, "10": 76, "01": 76, "11": 0}

    supports = {
        name: support_by_residual_pair(table) for name, table in profiles.items()
    }
    assert supports["10"] == {(0, 1): 38, (2, 0): 38}
    assert supports["01"] == {(0, 2): 38, (1, 0): 38}
    assert supports["11"] == {}

    sample_ports = (0, 0, 0, 1)
    sample10 = sample_coefficients(profiles["10"], sample_ports)
    sample01 = sample_coefficients(profiles["01"], sample_ports)
    assert sample10 == {(0, 1): F(1, 4), (2, 0): F(-1, 4)}
    assert sample01 == {(0, 2): F(1, 4), (1, 0): F(-1, 4)}

    contracted = {
        name: contract_residual_ones(table) for name, table in profiles.items()
    }
    contracted_counts = {name: len(table) for name, table in contracted.items()}
    assert contracted_counts == {"00": 41, "10": 0, "01": 0, "11": 0}
    return counts, supports, (sample10, sample01), contracted_counts


def audit_constant_kernel_anchor():
    a = {port: row_times(ONE, edge(EDGES, A0, port)) for port in PORTS}
    b = {port: row_times(ONE, edge(EDGES, A1, port)) for port in PORTS}
    kernels = {port: E1 for port in PORTS}
    assert a[K] == b[K] == (F(0), F(0), F(0))
    assert all(a[port] == b[port] == E0 for port in (U1, U2, U3))
    assert all(dot(a[port], kernels[port]) == 0 for port in PORTS)
    assert all(dot(b[port], kernels[port]) == 0 for port in PORTS)

    killed_pair_suppliers = 0
    for left_position in range(len(PORTS)):
        for right_position in range(left_position + 1, len(PORTS)):
            left = PORTS[left_position]
            right = PORTS[right_position]
            value = dot(a[left], kernels[left]) * dot(b[right], kernels[right]) + dot(
                b[left], kernels[left]
            ) * dot(a[right], kernels[right])
            assert value == 0
            killed_pair_suppliers += 1

    killed_one_q_suppliers = 0
    for port in PORTS:
        for residual in (Q0, Q1):
            xi0 = matrix_times(edge(EDGES, A0, residual), ONE)
            xi1 = matrix_times(edge(EDGES, A1, residual), ONE)
            local_value = dot(xi0, ONE) * dot(b[port], kernels[port]) + dot(
                xi1, ONE
            ) * dot(a[port], kernels[port])
            assert local_value == 0
            killed_one_q_suppliers += 1

    h_uhat = F(0)
    port_colours = {port: 1 for port in PORTS}
    for matching in PORT_MATCHINGS:
        term = F(1)
        for left, right in matching:
            term *= edge(EDGES, left, right)[port_colours[left]][port_colours[right]]
        h_uhat += term

    xi00 = matrix_times(edge(EDGES, A0, Q0), ONE)
    xi01 = matrix_times(edge(EDGES, A0, Q1), ONE)
    xi10 = matrix_times(edge(EDGES, A1, Q0), ONE)
    xi11 = matrix_times(edge(EDGES, A1, Q1), ONE)
    p = dot(xi00, ONE) * dot(xi11, ONE) + dot(xi01, ONE) * dot(xi10, ONE)
    diagonal_target = F(1)
    assert h_uhat == 1
    assert p == 2
    assert p * h_uhat == 2
    assert diagonal_target == 1
    assert p * h_uhat - diagonal_target == 1
    return (
        killed_pair_suppliers,
        killed_one_q_suppliers,
        (p * h_uhat, diagonal_target),
        p * h_uhat - diagonal_target,
    )


def main():
    profiles = audit_residual_profiles()
    kernels = audit_constant_kernel_anchor()
    print("GLS33 independent residual-Laurent/root-deck audit: PASS")
    print("  coefficient counts/supports/samples/all-ones:", profiles)
    print("  constant kernel pair/one-Q/values/defect:", kernels)
    print("  scope: exact control audit only; theorem/node/global closure OPEN")


if __name__ == "__main__":
    main()
