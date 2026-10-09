"""Independent exact replay for the Lemma 5 audit (two-ancilla contraction).

Audit document: docs/audits/LEMMA5_CONTRACTION_AUDIT_2026-10-09.md.

This file re-implements, from the repository's matching-tensor convention
(``src/krenn_gu/search_witness.py``: the block on ``e=(i,j)``, ``i<j``, is
``W[e, a, b]`` with ``a`` the colour at ``i``; the amplitude of a colouring is
the sum over perfect matchings of the products of block entries), every
object Lemma 5 talks about.  It shares no code with the scratch replays of
the compressed-Hessian or ancilla notes.

Differences from the notes' route:

* matching sums are computed natively on a vertex set in which every vertex
  has its own colour count (3 for ordinary vertices, 1 for an ancilla), with
  a block accessor that transposes stored blocks on demand, so ancilla rows
  are exercised in both storage orientations;
* the contraction identity is checked in its *split* form: the matchings of
  ``V`` containing ``{u,v}`` contribute ``(l^T W_uv m) T_B``, the others
  contribute the ancilla matching sum, for arbitrary ``(l, m)``;
* a second, permutation-formula hafnian cross-checks the matching sum;
* the full-weight criterion is checked on all 512 support patterns of a
  3 x 3 block and on every structured rank-one support.

Everything is exact (Python integers and ``fractions.Fraction``).  This is a
replay of identities with stated hand proofs, not a proof by itself.
"""

from __future__ import annotations

import itertools
import math
import random
import unittest
from fractions import Fraction

D = 3


class Config:
    """Vertex labels with colour counts and blocks stored for label order."""

    def __init__(self, ncol: dict[int, int]) -> None:
        self.ncol = dict(ncol)
        self.ancillas: tuple[int, ...] = ()
        self.blocks: dict[tuple[int, int], list[list]] = {}

    def set_block(self, i: int, j: int, mat) -> None:
        """Set the block with rows indexed by the colour at ``i``."""
        assert i != j
        if i < j:
            self.blocks[(i, j)] = [list(row) for row in mat]
        else:
            self.blocks[(j, i)] = [list(col) for col in zip(*mat)]

    def entry(self, i: int, j: int, a: int, b: int):
        """Weight of the edge {i, j} with colour a at i and b at j."""
        if i < j:
            blk = self.blocks.get((i, j))
            return 0 if blk is None else blk[a][b]
        blk = self.blocks.get((j, i))
        return 0 if blk is None else blk[b][a]

    def block(self, i: int, j: int):
        return [[self.entry(i, j, a, b) for b in range(self.ncol[j])]
                for a in range(self.ncol[i])]

    def words(self, verts):
        return itertools.product(*[range(self.ncol[v]) for v in verts])


def matching_sum(cfg: Config, verts: tuple[int, ...], word: dict[int, int]):
    """Sum over perfect matchings of ``verts`` (primary implementation)."""
    if not verts:
        return 1
    first, rest = verts[0], verts[1:]
    total = 0
    for k, other in enumerate(rest):
        w = cfg.entry(first, other, word[first], word[other])
        if w:
            total += w * matching_sum(cfg, rest[:k] + rest[k + 1:], word)
    return total


def matching_sum_perm(cfg: Config, verts: tuple[int, ...], word):
    """Hafnian by the permutation formula (independent cross-check)."""
    n = len(verts)
    k = n // 2
    total = 0
    for perm in itertools.permutations(verts):
        prod = 1
        for t in range(k):
            a, b = perm[2 * t], perm[2 * t + 1]
            prod *= cfg.entry(a, b, word[a], word[b])
            if not prod:
                break
        total += prod
    return Fraction(total, (2 ** k) * math.factorial(k))


def random_config(n: int, rng: random.Random, lo=-3, hi=3, density=0.8):
    cfg = Config({v: D for v in range(n)})
    for i, j in itertools.combinations(range(n), 2):
        cfg.set_block(i, j, [[rng.randint(lo, hi) if rng.random() < density
                              else 0 for _ in range(D)] for _ in range(D)])
    return cfg


def bilinear(cfg: Config, u: int, v: int, l, m):
    return sum(l[x] * cfg.entry(u, v, x, y) * m[y]
               for x in range(D) for y in range(D))


def contraction(cfg: Config, u: int, v: int, l, m, B, gamma):
    """sum_{x,y} l_x m_y T_V(x, y, gamma)."""
    verts = tuple(sorted(cfg.ncol))
    total = 0
    for x in range(D):
        for y in range(D):
            if l[x] == 0 or m[y] == 0:
                continue
            word = dict(zip(B, gamma))
            word[u] = x
            word[v] = y
            total += l[x] * m[y] * matching_sum(cfg, verts, word)
    return total


ANC_U, ANC_V = 100, 101   # labels larger than every vertex of B
LOW_U, LOW_V = -2, -1     # labels smaller than every vertex of B


def ancilla_config(cfg: Config, u: int, v: int, l, m, B, kappa=0,
                   transpose_bug=False, low_labels=False):
    """B plus one-colour vertices u', v' as stated in Lemma 5.

    The block of u' to z is the 1 x 3 row l^T W_uz (colour at z free);
    likewise v'.  It is stored as the 3 x 1 block (z, u') because z < u',
    so every read goes through the transposing accessor.  ``kappa`` is the
    optional u'v' edge (Lemma 5 has kappa = 0).  ``transpose_bug`` builds
    the rows with the wrong orientation (W_zu read as if rows were at u),
    as a sensitivity control.  `low_labels` gives the ancillas labels
    below B, so the ancilla blocks are stored as 1 x 3 rows instead.
    """
    au, av = (LOW_U, LOW_V) if low_labels else (ANC_U, ANC_V)
    anc = Config({**{z: D for z in B}, au: 1, av: 1})
    anc.ancillas = (au, av)
    for i, j in itertools.combinations(B, 2):
        anc.set_block(i, j, cfg.block(i, j))
    for z in B:
        if transpose_bug:
            ru = [sum(l[x] * cfg.entry(u, z, c, x) for x in range(D))
                  for c in range(D)]
            rv = [sum(m[y] * cfg.entry(v, z, c, y) for y in range(D))
                  for c in range(D)]
        else:
            ru = [sum(l[x] * cfg.entry(u, z, x, c) for x in range(D))
                  for c in range(D)]
            rv = [sum(m[y] * cfg.entry(v, z, y, c) for y in range(D))
                  for c in range(D)]
        anc.set_block(au, z, [ru])        # 1 x 3, row at the ancilla
        anc.set_block(av, z, [rv])
    if kappa:
        anc.set_block(au, av, [[kappa]])
    return anc


def ancilla_sum(anc: Config, B, gamma):
    word = dict(zip(B, gamma))
    for a in anc.ancillas:
        word[a] = 0
    return matching_sum(anc, tuple(sorted(anc.ncol)), word)


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def kernel_pair(cfg: Config, u: int, v: int, rng: random.Random):
    """Integer l, m of full support with l^T W_uv m = 0 (generic block)."""
    for _ in range(1000):
        l = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(D)]
        h = [sum(l[x] * cfg.entry(u, v, x, y) for x in range(D))
             for y in range(D)]
        m = (cross(h, [rng.randint(-4, 4) for _ in range(D)])
             if any(h) else [rng.choice([-2, -1, 1, 2]) for _ in range(D)])
        if all(m) and bilinear(cfg, u, v, l, m) == 0:
            return l, m
    raise AssertionError("no full-support kernel pair found")


def full_support_orthogonal(h):
    """A full-support rational m with h . m = 0, or None.

    None is returned exactly when h is a nonzero multiple of a unit vector
    (then h . m = h_i m_i != 0 for every full-support m)."""
    supp = [i for i in range(D) if h[i]]
    if not supp:
        return [Fraction(1)] * D
    if len(supp) == 1:
        return None
    if len(supp) == 2:
        i, j = supp
        m = [Fraction(1)] * D
        m[i], m[j] = Fraction(h[j]), Fraction(-h[i])
        return m
    for t in (1, 2):
        m2 = Fraction(-(h[0] + t * h[1]), h[2])
        if m2:
            return [Fraction(1), Fraction(t), m2]
    raise AssertionError("unreachable: h_1 != 0")


def full_weight_pair(W, box=(-3, -2, -1, 1, 2, 3)):
    """Constructively find a full-support (l, m) with l^T W m = 0.

    Candidates for l: a box of full-support integer vectors, plus a
    full-support vector orthogonal to each column (needed when W is a single
    column with two or more entries).  Returns None if no candidate works;
    for a single-entry block this is forced (l^T W m is a monomial)."""
    cands = [list(l) for l in itertools.product(box, repeat=D)]
    for c in range(D):
        o = full_support_orthogonal([W[x][c] for x in range(D)])
        if o is not None:
            cands.append(o)
    for l in cands:
        if not all(l):
            continue
        h = [sum(l[x] * W[x][y] for x in range(D)) for y in range(D)]
        m = full_support_orthogonal(h)
        if m is not None:
            return l, m
    return None


class ContractionIdentity(unittest.TestCase):

    def test_hafnian_cross_check(self):
        rng = random.Random(20261009)
        for _ in range(2):
            cfg = random_config(6, rng)
            verts = tuple(range(6))
            for word in cfg.words(verts):
                wd = dict(zip(verts, word))
                self.assertEqual(matching_sum(cfg, verts, wd),
                                 matching_sum_perm(cfg, verts, wd))
        # also on an ancilla configuration (one-colour vertices)
        cfg = random_config(6, rng)
        B = (0, 1, 3, 5)
        l, m = [1, -2, 3], [2, 1, -1]
        anc = ancilla_config(cfg, 4, 2, l, m, B, kappa=7)
        verts = tuple(sorted(anc.ncol))
        for gamma in itertools.product(range(D), repeat=len(B)):
            wd = dict(zip(B, gamma))
            wd[ANC_U] = wd[ANC_V] = 0
            self.assertEqual(matching_sum(anc, verts, wd),
                             matching_sum_perm(anc, verts, wd))

    def _split_check(self, n, pairs, seeds, all_words=True):
        for seed in seeds:
            rng = random.Random(seed)
            cfg = random_config(n, rng)
            for k, (u, v) in enumerate(pairs):
                low = bool(k % 2)
                B = tuple(z for z in range(n) if z not in (u, v))
                l = [rng.randint(-3, 3) for _ in range(D)]
                m = [rng.randint(-3, 3) for _ in range(D)]
                kappa = bilinear(cfg, u, v, l, m)
                anc0 = ancilla_config(cfg, u, v, l, m, B, low_labels=low)
                anck = ancilla_config(cfg, u, v, l, m, B, kappa=kappa,
                                      low_labels=low)
                gammas = list(itertools.product(range(D), repeat=n - 2))
                if not all_words:
                    gammas = rng.sample(gammas, 120)
                both = 0
                for gamma in gammas:
                    lhs = contraction(cfg, u, v, l, m, B, gamma)
                    TB = matching_sum(cfg, B, dict(zip(B, gamma)))
                    phi = ancilla_sum(anc0, B, gamma)
                    self.assertEqual(lhs, kappa * TB + phi)
                    both += (kappa * TB != 0) and (phi != 0)
                    self.assertEqual(lhs, ancilla_sum(anck, B, gamma))
                # non-vacuity: both classes of matchings contribute
                self.assertGreater(both, len(gammas) // 4)

    def test_split_identity_n6(self):
        self._split_check(6, [(0, 1), (4, 2), (5, 3), (2, 5)], [1, 2, 3])

    def test_split_identity_n8(self):
        self._split_check(8, [(5, 2), (7, 0)], [11])

    def _kernel_check(self, n, pairs, seeds, all_words=True):
        for seed in seeds:
            rng = random.Random(seed)
            cfg = random_config(n, rng)
            for k, (u, v) in enumerate(pairs):
                B = tuple(z for z in range(n) if z not in (u, v))
                l, m = kernel_pair(cfg, u, v, rng)
                self.assertEqual(bilinear(cfg, u, v, l, m), 0)
                anc = ancilla_config(cfg, u, v, l, m, B,
                                     low_labels=bool(k % 2))
                gammas = list(itertools.product(range(D), repeat=n - 2))
                if not all_words:
                    gammas = rng.sample(gammas, 150)
                nonzero = 0
                for gamma in gammas:
                    lhs = contraction(cfg, u, v, l, m, B, gamma)
                    self.assertEqual(lhs, ancilla_sum(anc, B, gamma))
                    nonzero += lhs != 0
                # non-vacuity: the identity is tested on nonzero values
                self.assertGreater(nonzero, len(gammas) // 2)

    def test_kernel_identity_n6(self):
        self._kernel_check(6, [(3, 1), (0, 5), (4, 2)], [21, 22, 23, 24])

    def test_kernel_identity_n8(self):
        self._kernel_check(8, [(6, 3), (1, 4)], [31, 32])

    def test_orientation_control(self):
        """Building the rows from the transposed block breaks the identity."""
        rng = random.Random(41)
        cfg = random_config(6, rng)
        u, v = 4, 1
        B = tuple(z for z in range(6) if z not in (u, v))
        l, m = kernel_pair(cfg, u, v, rng)
        bad = ancilla_config(cfg, u, v, l, m, B, transpose_bug=True)
        mismatches = sum(
            contraction(cfg, u, v, l, m, B, g) != ancilla_sum(bad, B, g)
            for g in itertools.product(range(D), repeat=4))
        self.assertGreater(mismatches, 0)


class FullWeightCriterion(unittest.TestCase):

    def test_all_support_patterns(self):
        """Full-support kernel pair exists iff the block is not one entry."""
        rng = random.Random(51)
        cells = [(a, b) for a in range(D) for b in range(D)]
        for mask in range(1 << 9):
            support = [cells[k] for k in range(9) if mask >> k & 1]
            for _ in range(3):
                W = [[0] * D for _ in range(D)]
                for (a, b) in support:
                    W[a][b] = rng.choice([-3, -2, -1, 1, 2, 3])
                found = full_weight_pair(W)
                if len(support) == 1:
                    # l^T W m = w * l_a * m_b: a monomial, never zero on
                    # the torus; the box search must also fail.
                    self.assertIsNone(found)
                else:
                    self.assertIsNotNone(found, (support, W))
                    l, m = found
                    self.assertTrue(all(l) and all(m))
                    self.assertEqual(sum(l[x] * W[x][y] * m[y]
                                         for x in range(D)
                                         for y in range(D)), 0)

    def test_structured_rank_one_and_degenerate(self):
        """Rank one a b^T for every support pair, plus singular rank two."""
        rng = random.Random(52)
        supports = [s for s in itertools.product([0, 1], repeat=D) if any(s)]
        for sa in supports:
            for sb in supports:
                a = [rng.choice([-2, -1, 1, 2]) * s for s in sa]
                b = [rng.choice([-2, -1, 1, 2]) * s for s in sb]
                W = [[a[x] * b[y] for y in range(D)] for x in range(D)]
                single = sum(sa) == 1 and sum(sb) == 1
                self.assertEqual(full_weight_pair(W) is None, single)
        extra = [
            [[1, 1, 0], [0, 0, 0], [0, 0, 0]],      # two entries, one row
            [[1, 1, 1], [0, 0, 0], [0, 0, 0]],      # full row
            [[1, 0, 0], [1, 0, 0], [0, 0, 0]],      # two entries, one column
            [[1, 0, 0], [0, 1, 0], [0, 0, 0]],      # rank two diagonal
            [[0, 1, 0], [1, 0, 0], [0, 0, 0]],      # rank two antidiagonal
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],      # identity
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],      # all ones (rank one)
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],      # zero block
        ]
        for W in extra:
            found = full_weight_pair(W)
            self.assertIsNotNone(found, W)


class TorusNormalization(unittest.TestCase):

    def test_colour_row_rescaling_at_a_B_vertex(self):
        """Scaling colour rows at z in B (ancilla rows included) rescales
        T(gamma) by 1/mu_{gamma_z}, keeps one-colour vertices one-colour and
        adds no ancilla edge."""
        rng = random.Random(61)
        cfg = random_config(8, rng)
        u, v = 6, 2
        B = tuple(z for z in range(8) if z not in (u, v))
        l, m = kernel_pair(cfg, u, v, rng)
        anc = ancilla_config(cfg, u, v, l, m, B)
        z0 = B[2]
        mu = [Fraction(2), Fraction(-3), Fraction(5, 7)]
        scaled = Config(anc.ncol)
        scaled.ancillas = anc.ancillas
        for (i, j), blk in anc.blocks.items():
            scaled.set_block(i, j, blk)
        for w in scaled.ncol:
            if w == z0:
                continue
            blk = scaled.block(z0, w)
            scaled.set_block(z0, w, [[blk[c][k] / mu[c]
                                      for k in range(len(blk[c]))]
                                     for c in range(D)])
        self.assertEqual(scaled.ncol[ANC_U], 1)
        self.assertEqual(scaled.ncol[ANC_V], 1)
        self.assertEqual(scaled.entry(ANC_U, ANC_V, 0, 0), 0)
        for gamma in rng.sample(list(itertools.product(range(D), repeat=6)),
                                100):
            self.assertEqual(ancilla_sum(scaled, B, gamma),
                             ancilla_sum(anc, B, gamma)
                             / mu[gamma[B.index(z0)]])


class OrderFourWitness(unittest.TestCase):
    """The only exact witness family at hand: complete matrix units, n = 4."""

    def _witness(self, lam):
        cfg = Config({v: D for v in range(4)})
        E = lambda a, b, w: [[w if (x, y) == (a, b) else 0
                              for y in range(D)] for x in range(D)]
        cfg.set_block(0, 1, E(0, 0, lam[0]))
        cfg.set_block(2, 3, E(0, 0, 1))
        cfg.set_block(0, 2, E(1, 1, lam[1]))
        cfg.set_block(1, 3, E(1, 1, 1))
        cfg.set_block(3, 0, E(2, 2, lam[2]))
        cfg.set_block(2, 1, E(2, 2, 1))
        return cfg

    def test_full_statement_on_weighted_ghz4(self):
        lam = [Fraction(3), Fraction(-2), Fraction(5, 3)]
        cfg = self._witness(lam)
        verts = tuple(range(4))
        for word in cfg.words(verts):
            t = matching_sum(cfg, verts, dict(zip(verts, word)))
            pure = len(set(word)) == 1
            self.assertEqual(t, lam[word[0]] if pure else 0)
        for u, v in itertools.permutations(range(4), 2):
            B = tuple(z for z in range(4) if z not in (u, v))
            W = cfg.block(u, v)
            # every pair is the residual: no full-support kernel pair
            self.assertIsNone(full_weight_pair(W))
            (a, b), = [(x, y) for x in range(D) for y in range(D) if W[x][y]]
            # kernel pairs exist only with l_a m_b = 0; take l_a = 0
            l = [0 if x == a else x + 2 for x in range(D)]
            m = [y - 4 for y in range(D)]
            self.assertEqual(bilinear(cfg, u, v, l, m), 0)
            anc = ancilla_config(cfg, u, v, l, m, B)
            for gamma in itertools.product(range(D), repeat=2):
                expect = (lam[gamma[0]] * l[gamma[0]] * m[gamma[0]]
                          if gamma[0] == gamma[1] else 0)
                self.assertEqual(contraction(cfg, u, v, l, m, B, gamma),
                                 expect)
                self.assertEqual(ancilla_sum(anc, B, gamma), expect)


if __name__ == "__main__":
    unittest.main()
