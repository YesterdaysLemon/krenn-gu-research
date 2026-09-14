"""Exhaustive local combinatorics behind a four-cofactor coverage argument."""

from itertools import combinations, product
import unittest

EDGES = tuple(combinations(range(4), 2))
EDGE_BIT = {edge: 1 << position for position, edge in enumerate(EDGES)}
MATCHINGS = tuple(sum(EDGE_BIT[edge] for edge in matching) for matching in (
    ((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)),
))
ALL_EDGES = (1 << len(EDGES)) - 1


def matching_count(graph):
    return sum((graph & matching) == matching for matching in MATCHINGS)


def has_mixed_matching(first, second):
    # Represent the partition by its two actual edges, independently of the
    # geometric matching bitmasks used in matching_count.
    for edge in EDGES:
        other = tuple(vertex for vertex in range(4) if vertex not in edge)
        if first & EDGE_BIT[edge] and second & EDGE_BIT[other]:
            return True
    return False


class FourVertexCofactorCoverageTests(unittest.TestCase):
    def test_no_rainbow_and_two_matchable_graphs_force_a_unique_matching(self):
        checked = 0
        for first, second in product(range(64), repeat=2):
            counts = matching_count(first), matching_count(second)
            if all(counts) and not has_mixed_matching(first, second):
                self.assertEqual(min(counts), 1)
                self.assertLessEqual(sum(counts), 3)
                checked += 1
        self.assertGreater(checked, 0)

    def test_all_disjoint_partial_matching_triples_give_coverage(self):
        partials = (0, *EDGE_BIT.values(), *MATCHINGS)
        self.assertEqual(len(partials), 10)
        checked = 0
        for pc, pd, pe in product(partials, repeat=3):
            if pc & pd or pc & pe or pd & pe:
                continue
            gd = ALL_EDGES & ~(pc | pe)
            ge = ALL_EDGES & ~(pc | pd)
            self.assertTrue(has_mixed_matching(gd, ge)
                            or (matching_count(gd) and matching_count(ge)))
            checked += 1
        self.assertGreater(checked, 0)

    def test_four_vertices_are_an_essential_boundary(self):
        # The three one-factor classes of K4 are a genuine GHZ_4 source.
        for c in range(3):
            others = [d for d in range(3) if d != c]
            self.assertEqual(ALL_EDGES & ~(MATCHINGS[others[0]] | MATCHINGS[others[1]]),
                             MATCHINGS[c])
            self.assertEqual(matching_count(MATCHINGS[c]), 1)
            self.assertFalse(has_mixed_matching(MATCHINGS[others[0]], MATCHINGS[others[1]]))

    def test_matchability_equals_triangle_free_degree_two_complement(self):
        for graph in range(64):
            missing = ALL_EDGES ^ graph
            degrees = [sum(bool(missing & EDGE_BIT[edge]) for edge in EDGES if v in edge)
                       for v in range(4)]
            triangle = any(all(missing & EDGE_BIT[edge] for edge in combinations(vertices, 2))
                           for vertices in combinations(range(4), 3))
            self.assertEqual(bool(matching_count(graph)), max(degrees) <= 2 and not triangle)


if __name__ == "__main__":
    unittest.main()
