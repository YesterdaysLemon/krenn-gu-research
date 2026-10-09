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


if __name__ == "__main__":
    unittest.main()
