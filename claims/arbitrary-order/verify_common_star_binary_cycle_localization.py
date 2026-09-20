"""Exact companion replay; the owning written proof is the all-order theorem.

Uses SymPy and actual permanent polynomials. This is not an independent audit
or a full-target witness search. The five-component control passes one face
and deliberately fails a global binary target.
"""
from __future__ import annotations

from itertools import combinations, permutations, product
import json

import sympy as sp


def subsets(values):
    values = tuple(values)
    for size in range(len(values) + 1):
        yield from combinations(values, size)


def permanent(matrix, rows, columns):
    return sum((sp.prod(matrix[u][v] for u, v in zip(rows, perm))
                for perm in permutations(columns)), sp.S.Zero)


def local_source(a, b, rows, columns):
    rows, columns = tuple(rows), tuple(columns)
    return sp.expand(sum(
        permanent(a, chosen_rows, chosen_columns)
        * permanent(b, chosen_rows, chosen_columns)
        for size in range(min(len(rows), len(columns)) + 1)
        for chosen_rows in combinations(rows, size)
        for chosen_columns in combinations(columns, size)
    ))


def symbolic_deletion():
    """Generic two exterior rows and three separately weighted matching rows."""
    a = [list(sp.symbols(f'a{u}_0:3')) for u in range(2)]
    b = [list(sp.symbols(f'b{u}_0:3')) for u in range(2)]
    aa, bb = sp.symbols('aa0:3'), sp.symbols('bb0:3')
    for u in range(3):
        a.append([aa[u] if v == u else sp.S.Zero for v in range(3)])
        b.append([bb[u] if v == u else sp.S.Zero for v in range(3)])
    left = local_source(a, b, range(5), range(3))
    right = sum(sp.prod(aa[u] * bb[u] for u in chosen)
                * local_source(a, b, range(2), set(range(3)) - set(chosen))
                for chosen in subsets(range(3)))
    assert sp.expand(left - right) == 0
    # A second selected column in a supposed matching row invalidates deletion.
    a[2][1], b[2][1] = sp.Integer(1), sp.Integer(1)
    assert sp.expand(local_source(a, b, range(5), range(3)) - right) != 0
    return {'symbolic_matching_rows': 3, 'exterior_rows': 2,
            'invalid_second_column_rejected': True}


def control_matrices(s=None, cycle_leaf=None):
    if s is None:
        s = (-3 + sp.sqrt(-3)) / 6
    q = -1 - s if cycle_leaf is None else cycle_leaf
    w = s / 2
    a, b = sp.zeros(5).tolist(), sp.zeros(5).tolist()
    for u in range(3):
        a[u][(u + 1) % 3], b[u][(u + 1) % 3] = sp.Integer(1), q
    for u in (3, 4):
        for v in range(3):
            a[u][v], b[u][v] = sp.Integer(1), w
    return a, b


def binary_amplitude(a, b, word):
    return sp.simplify(local_source(a, b,
                                   [i for i, c in enumerate(word) if c == 0],
                                   [i for i, c in enumerate(word) if c == 1]))


def face_control():
    s = (-3 + sp.sqrt(-3)) / 6
    q, w = -1 - s, s / 2
    assert sp.simplify(3 * s**2 + 3 * s + 1) == 0
    assert q != 0 and w != 0
    a, b = control_matrices(s)
    for u, v in product(range(5), repeat=2):
        assert bool(a[u][v]) == bool(b[u][v])
        assert not (a[u][v] and a[v][u])
    for word in product(range(2), repeat=3):
        assert binary_amplitude(a, b, (*word, 0, 0)) == int(word == (0, 0, 0))
    for selected in subsets(range(3)):
        actual = sp.simplify(local_source(a, b, (3, 4), selected))
        expected = (-q)**len(selected) if len(selected) < 3 else 0
        assert sp.simplify(actual - expected) == 0
    assert sp.simplify(-s**3 - q**3) == 0
    failure = (0, 0, 0, 1, 0)
    assert binary_amplitude(a, b, failure) == 1
    assert binary_amplitude(a, b, (1,) * 5) == 1
    return {'components': 5, 'physical_vertices': 20, 'gadgets': 9,
            'face_words_checked': 8, 'proper_exterior_subsets_checked': 7,
            'full_exterior_value': 0, 'failed_global_word': ''.join(map(str, failure)),
            'failed_global_value': 1, 'status': 'ONE_FACE_CONTROL_NOT_FB'}


def cycle_control(k):
    a, b = sp.zeros(k).tolist(), sp.zeros(k).tolist()
    for u in range(k):
        a[u][(u + 1) % k], b[u][(u + 1) % k] = sp.Integer(1), -sp.Integer(1)
    for word in product(range(2), repeat=k):
        assert binary_amplitude(a, b, word) == int(len(set(word)) == 1)
    return 2**k


def arbitrary_length_control_identities():
    """Replay finite symbolic instances of the written all-order construction."""
    weights = sp.symbols('w0:3')
    a = [[sp.S.One] * 4 for _ in weights]
    b = [[weight] * 4 for weight in weights]
    for size in range(4):
        columns = tuple(range(size))
        coefficient = sum(
            permanent(a, rows, columns) * permanent(b, rows, columns)
            for rows in combinations(range(3), size)
        )
        elementary = sum(sp.prod(weights[u] for u in rows)
                         for rows in combinations(range(3), size))
        assert sp.expand(coefficient - sp.factorial(size)**2 * elementary) == 0
    rho = sp.Symbol('rho')
    s = 1 / (rho - 1)
    for size in range(3, 10):
        defect = sp.cancel(((1 + s)**size - s**size) * (rho - 1)**size)
        assert sp.expand(defect - (rho**size - 1)) == 0
    return {'generic_row_weights': 3, 'moment_sizes_checked': 4,
            'root_of_unity_identity_orders_checked': list(range(3, 10)),
            'all_orders_use_written_proof': True}


def main():
    result = {'deletion': symbolic_deletion(), 'face_control': face_control(),
              'directed_cycle_words_checked': sum(cycle_control(k) for k in (3, 4, 5)),
              'arbitrary_length_identities': arbitrary_length_control_identities(),
              'global_status': 'UNRESOLVED',
              'evidence': 'exact finite companion replay; all-order proof is written'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
