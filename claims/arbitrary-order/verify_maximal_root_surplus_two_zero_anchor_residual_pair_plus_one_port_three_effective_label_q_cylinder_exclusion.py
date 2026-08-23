#!/usr/bin/env python3
"""Focused exact verifier for GLS49's three-label q-cylinder exclusion."""

from itertools import combinations

import sympy as sp


def root_basis(index):
    vector = sp.zeros(9, 1)
    vector[3 * index + index] = 1
    return vector


def kron(left, right):
    return sp.kronecker_product(left, right)


def quotient_dimension(q):
    port_basis = [sp.eye(3)[:, i] for i in range(3)]
    cylinder = sp.Matrix.hstack(*(kron(q, e) for e in port_basis))
    desired = sp.Matrix.hstack(*(kron(root_basis(i), port_basis[i])
                                 for i in range(3)))
    assert cylinder.rank() == 3
    return sp.Matrix.hstack(cylinder, desired).rank() - 3


def support_replay():
    residual = ("q0", "q1")
    ports = ("u0", "u1", "u2", "u3")
    labels = residual + ports
    supports = [set(s) for s in combinations(labels, 3)
                if set(residual).issubset(s)]
    assert supports == [set(residual + (u,)) for u in ports]
    for support in supports:
        pairs = {frozenset(pair) for pair in combinations(support, 2)}
        u = next(iter(support - set(residual)))
        assert pairs == {
            frozenset(residual),
            frozenset(("q0", u)),
            frozenset(("q1", u)),
        }
    return len(supports)


def cylinder_replay():
    r = [root_basis(i) for i in range(3)]
    port_basis = [sp.eye(3)[:, i] for i in range(3)]
    desired = sp.Matrix.hstack(*(kron(r[i], port_basis[i]) for i in range(3)))
    assert desired.rank() == 3
    generic_two_generator = sp.Matrix(27, 2, sp.symbols("g0:54"))
    assert generic_two_generator.rank() == 2 < desired.rank()
    assert [quotient_dimension(q) for q in r] == [2, 2, 2]

    off_diagonal = []
    for row in range(3):
        for col in range(3):
            if row != col:
                q = sp.zeros(9, 1)
                q[3 * row + col] = 1
                off_diagonal.append(q)
    hostile = off_diagonal + [r[0] + r[1], r[0] + off_diagonal[0],
                              sum(r, sp.zeros(9, 1))]
    assert all(quotient_dimension(q) == 3 for q in hostile)
    return len(hostile)


def shore_rank_replay():
    # If a 3x2 residual shore B contained e0,e1,e2, some 2x3 coefficient
    # matrix T would satisfy B*T=I3.  Its determinant is identically zero.
    b = sp.Matrix(3, 2, sp.symbols("b0:6"))
    t = sp.Matrix(2, 3, sp.symbols("t0:6"))
    assert sp.expand((b * t).det()) == 0
    assert sp.eye(3).det() == 1

    # Replay the rank-one factor dichotomy in normalized coordinates.
    a = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    c = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    assert a.rank() == c.rank() == 2
    assert (a * c.T).rank() == 2


def main():
    support_count = support_replay()
    hostile_count = cylinder_replay()
    shore_rank_replay()
    print("GLS49 focused exact verifier: PASS")
    print(f"D(p) three-label supports: {support_count}, all Q plus one port")
    print("zero-q residual-pair-plus-one-port support: rank 2 < 3")
    print("q-cylinder quotient dimensions: pure=2, non-pure=3")
    print(f"hostile non-pure rational representatives: {hostile_count}")
    print("rank-two residual shore cannot contain three coordinate axes")


if __name__ == "__main__":
    main()
