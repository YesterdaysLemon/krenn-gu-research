"""Equivalence tests for the --fast paths of the general-block support model.

The --fast-plane scan must return exactly check_plane's violation list and
exactly plane_instances' instance dictionary (same keys, clauses and order);
the --fast-holonomy skip must leave the new holonomy instances and the
order of variable allocation unchanged.  These are engineering tests of the
search tool; they say nothing about any mathematical status.
"""

from __future__ import annotations

import importlib.util
import pathlib
import random
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "claims" / "finite" / "n08" / "explore_general_block_recursive_support_model.py"
SPEC = importlib.util.spec_from_file_location("gsm_support_model", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
GSM_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GSM_MODULE
SPEC.loader.exec_module(GSM_MODULE)


def random_model(enc, seed, p_g=0.5, p_m=0.04, p_other=0.5):
    """A random full assignment (not a model of the CNF; the scans only read
    literal values).  m variables are mostly false so zero cubes occur."""
    rng = random.Random(seed)
    gids = set(enc.g.values())
    mids = set(enc.m.values())
    model = []
    for var in range(1, enc.pool.top + 1):
        p = p_g if var in gids else p_m if var in mids else p_other
        # the TRUE variable is fixed by a unit clause in every real model
        model.append(var if var == enc.true or rng.random() < p else -var)
    return model


def decode(enc, model):
    pos = {lit for lit in model if lit > 0}
    gsup = {k for k, v in enc.g.items() if v in pos}
    msup = {k for k, v in enc.m.items() if v in pos}
    val = (lambda lit: (lit in pos) if lit > 0 else (-lit not in pos))
    return gsup, msup, val


class FastPlaneScanTests(unittest.TestCase):
    def test_matches_reference_on_random_assignments(self) -> None:
        enc = GSM_MODULE.GSM(6, symmetry=False, killers=True)
        fired = 0
        for seed in range(12):
            # vary the density so that both the prefilter and the minors matter
            model = random_model(enc, seed, p_g=0.35 + 0.05 * (seed % 4), p_m=0.02 * (seed % 3))
            gsup, msup, val = decode(enc, model)
            for mode in ("value", "deg3"):
                ref_bad = GSM_MODULE.check_plane(6, gsup, msup, False, mode)
                ref_inst = enc.plane_instances(val, False, mode)
                inst, bad = enc.plane_scan_fast(model, val, False, mode)
                self.assertEqual(bad, ref_bad)
                self.assertEqual(list(inst.items()), list(ref_inst.items()))
                fired += len(bad)
        self.assertGreater(fired, 0, "random assignments never exercised a PR violation")


class FastHolonomyScanTests(unittest.TestCase):
    def test_check_matches_reference_on_random_supports(self) -> None:
        enc = GSM_MODULE.GSM(6, symmetry=False)
        nonempty = 0
        for seed in range(6):
            model = random_model(enc, seed, p_g=0.3 + 0.1 * (seed % 3), p_m=0.2 + 0.1 * (seed % 2))
            gsup, msup, _ = decode(enc, model)
            for top_only in (False, True):
                for rules in (("H2", "H3"), ("H2",), ("H3",)):
                    s_ref, s_fast = {}, {}
                    ref = GSM_MODULE.check_holonomy(6, gsup, msup, top_only, rules, stats=s_ref)
                    fast = GSM_MODULE.check_holonomy_fast(6, gsup, msup, top_only, rules, stats=s_fast)
                    self.assertEqual(fast, ref)
                    self.assertEqual(s_fast, s_ref)
                    nonempty += bool(ref)
        self.assertGreater(nonempty, 0)

    def test_premises_match_reference_scan(self) -> None:
        enc = GSM_MODULE.GSM(6, symmetry=False)
        total = 0
        for seed in range(4):
            model = random_model(enc, seed, p_g=0.6, p_m=0.3, p_other=0.3 + 0.1 * seed)
            _, _, val = decode(enc, model)
            for top_only in (False, True):
                sets = [enc.V] if top_only else enc.sets
                ref = list(enc._holonomy_premises(val, sets, ("H2", "H3")))
                fast = list(enc.holonomy_premises_fast(model, top_only, ("H2", "H3")))
                self.assertEqual(len(fast), len(ref))
                for f, r in zip(fast, ref):
                    self.assertEqual(f[:7], r[:7])           # A, idx, w, mA, p, a, b
                    self.assertEqual(f[11], r[11])           # hubs q
                    if r[11]:
                        self.assertEqual(f[7:11], r[7:11])   # Ba, wa, Bb, wb
                total += len(ref)
        self.assertGreater(total, 0)


class FastHolonomySkipTests(unittest.TestCase):
    def test_skip_preserves_new_instances_and_allocation(self) -> None:
        ref = GSM_MODULE.GSM(6, symmetry=False)
        fast = GSM_MODULE.GSM(6, symmetry=False)
        models = [random_model(ref, seed, p_g=0.6, p_m=0.3, p_other=0.4) for seed in range(3)]
        added_ref, added_fast = {}, {}
        for model in models:
            _, _, val = decode(ref, model)
            full = ref.holonomy_instances(val)
            new_ref = {k: v for k, v in full.items() if k not in added_ref}
            new_fast = fast.holonomy_instances(val, skip=added_fast,
                                               premises=fast.holonomy_premises_fast(model))
            self.assertEqual(list(new_fast.items()), list(new_ref.items()))
            self.assertEqual(fast.pool.obj2id, ref.pool.obj2id)
            added_ref.update(new_ref)
            added_fast.update(new_fast)
        self.assertGreater(len(added_ref), 0)


def exact_support(n, seed, dens, vals):
    """Exact zero pattern (gsup, msup) of a random sparse integer configuration
    on n vertices: every T_A(w), |A| >= 4 even, by Laplace recursion."""
    import functools
    import itertools
    rng = random.Random(seed)
    W = {}
    for i, j in itertools.combinations(range(n), 2):
        for a in range(3):
            for b in range(3):
                W[(i, j, a, b)] = rng.choice(vals) if rng.random() < dens else 0

    def w(i, j, a, b):
        return W[(i, j, a, b)] if i < j else W[(j, i, b, a)]

    @functools.lru_cache(None)
    def T(A, word):
        if not A:
            return 1
        return sum(w(A[0], A[k], word[0], word[k]) * T(A[1:k] + A[k + 1:], word[1:k] + word[k + 1:])
                   for k in range(1, len(A)))
    gsup = {k for k, x in W.items() if x}
    msup = {(A, wd) for k in range(4, n + 1, 2) for A in itertools.combinations(range(n), k)
            for wd in itertools.product(range(3), repeat=k) if T(A, wd)}
    return gsup, msup


class CompressedHessianTests(unittest.TestCase):
    """CH (--compressed-hessian) carries 'not m' premises, so it holds for the
    exact zero pattern of every configuration at every level; and every lazy
    clause must be falsified by the assignment that produced it."""

    def test_exact_patterns_satisfy_ch_at_every_level(self) -> None:
        frames = GSM_MODULE.ch_frames(6, all_levels=True)
        certified = 0
        for seed in range(12):
            gsup, msup = exact_support(6, seed, (0.25, 0.4, 0.55)[seed % 3],
                                       (-1, 1) if seed % 2 else (-2, -1, 1, 2))
            st = {}
            self.assertEqual(GSM_MODULE.check_ch(6, gsup, msup, frames, stats=st,
                                                 factorizations=FACS), [])
            certified += sum(st["CH_certified_premises"].values())
        self.assertGreater(certified, 0, "no premise instance had a certified side")

    def test_clauses_are_falsified_by_their_assignment(self) -> None:
        for enc, N in ((GSM_MODULE.GSM(6, symmetry=False), 6),
                       (GSM_MODULE.PairDecoratedGSM(4), 6)):
            kinds = set()
            for seed in range(6):
                model = random_model(enc, seed, p_g=0.2 + 0.1 * (seed % 3), p_m=0.15)
                gsup, msup, val = decode(enc, model)
                for facs in (("F3",), ("F1",), ("F2",)):
                    bad = GSM_MODULE.check_ch(N, gsup, msup, enc.ch_frames(all_levels=True),
                                              factorizations=facs)
                    inst = enc.ch_instances(bad, val)      # asserts falsification
                    self.assertEqual(len(inst) > 0, len(bad) > 0)
                    kinds |= {(b[0], b[7]) for b in bad}
            self.assertGreaterEqual(len(kinds), 6, f"few CH kinds exercised: {sorted(kinds)}")


FACS = ("F3", "F1", "F2")


if __name__ == "__main__":
    unittest.main()
