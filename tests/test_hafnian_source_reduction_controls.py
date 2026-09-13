"""Exact controls against unproved source-reduction and exchange premises.

These are actual one-colour matrices, not Krenn--Gu witnesses. They isolate
what cannot be supplied by one-colour hafnian identities alone.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import unittest


def hafnian_oracle(n, weights):
    """Small exact principal-hafnian oracle independent of SAT encoders."""

    @lru_cache(None)
    def hafnian(vertices):
        if not vertices:
            return 1
        first = vertices[0]
        return sum(
            weights.get(tuple(sorted((first, second))), 0)
            * hafnian(tuple(v for v in vertices[1:] if v != second))
            for second in vertices[1:]
        )

    return hafnian, tuple(range(n))


def with_isolated_pairs(weights, n):
    result = dict(weights)
    result.update({(vertex, vertex + 1): 1 for vertex in range(6, n, 2)})
    return result


def has_perfect_matching(vertices, edges):
    if not vertices:
        return True
    first = vertices[0]
    return any(
        tuple(sorted((first, second))) in edges
        and has_perfect_matching(tuple(v for v in vertices[1:] if v != second), edges)
        for second in vertices[1:]
    )


class HafnianSourceReductionControls(unittest.TestCase):
    def test_bipartite_active_graph_need_not_have_a_matching(self):
        # B = [[1,1,1], [1,1,1], [1,-1,-1]], Z = [[0,B],[B^T,0]].
        base = {(left, right): (-1 if left == 2 and right in (4, 5) else 1)
                for left in range(3) for right in range(3, 6)}
        for n in (6, 8, 10, 12):
            weights = with_isolated_pairs(base, n)
            hafnian, whole = hafnian_oracle(n, weights)
            self.assertEqual(hafnian(whole), -2)
            scores = {edge: value * hafnian(tuple(v for v in whole if v not in edge))
                      for edge, value in weights.items()}
            active = {edge for edge, score in scores.items() if score}
            self.assertTrue(has_perfect_matching(whole, set(weights)))
            self.assertFalse(has_perfect_matching(whole, active))
            self.assertEqual({edge for edge in active if max(edge) < 6},
                             {(0, 3), (1, 3), (2, 3), (2, 4), (2, 5)})
            for vertex in whole:
                self.assertEqual(sum(Fraction(score, -2) for edge, score in scores.items()
                                     if vertex in edge), 1)

    def test_nonzero_hafnian_support_need_not_satisfy_symmetric_exchange(self):
        base = {(0, 1): 1, (0, 2): 1, (1, 2): 1}
        base.update({(left, right): 1 for left in (0, 1) for right in (3, 4, 5)})
        base.update({(2, right): -2 for right in (3, 4, 5)})
        for n in (6, 8, 10, 12):
            hafnian, whole = hafnian_oracle(n, with_isolated_pairs(base, n))
            self.assertEqual(hafnian((0, 1)), 1)
            self.assertEqual(hafnian(whole), -12)
            # A={0,1}, B=V, x=2. No eligible y makes A symmetric-difference
            # {x,y} nonzero, even before asking for the exchanged B to survive.
            for y in range(3, n):
                self.assertEqual(hafnian((0, 1, 2, y)), 0)

    def test_naive_rank_two_pair_contraction_creates_extra_matchings(self):
        # Contract vertices 0,1 of the all-ones six-vertex source.
        # The exact four-vertex coefficient remains haf(K6)=15.
        weights = {edge: 1 for edge in combinations(range(6), 2)}
        hafnian, whole = hafnian_oracle(6, weights)
        self.assertEqual(hafnian(whole), 15)
        # The tempting effective edge w_ij+(w_0i*w_1j+w_0j*w_1i)/w_01
        # equals 3, and its four-hafnian is 27, not 15.
        effective = {edge: 3 for edge in combinations(range(4), 2)}
        effective_hafnian, effective_whole = hafnian_oracle(4, effective)
        self.assertEqual(effective_hafnian(effective_whole), 27)


if __name__ == "__main__":
    unittest.main()
