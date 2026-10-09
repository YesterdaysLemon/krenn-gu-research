#!/usr/bin/env python3
"""Floating-point least-squares probe for bipartite cut-tensor witnesses.

EXPLORATORY ONLY: numerical evidence, never a proof.  Owner:
docs/strategy/cut-tensor-rigidity-attempt-2026-10-09.md.

Unknowns: complex 3x3 blocks W[p, q] for p in P, q in Q, |P| = |Q| = k.
Residual: per(A_a) - [a constant] over all 3^(2k) words a, where
A_a[p, q] = W[p, q][a_p, a_q].  Levenberg-Marquardt from random starts;
prints the residual 2-norm reached in each trial.  A residual of exactly 1
is what a two-colour configuration (two constant words right, the third 0,
all mixed words 0) attains.

Run (k = 4 takes several minutes per trial; use the bounded runner):
    python tools/explore/probe_bipartite_cut_tensor_least_squares.py --k 3 --trials 3
"""
from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=2)
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    k = args.k
    rng = np.random.default_rng(args.seed)
    words = np.array(list(itertools.product(range(3), repeat=2 * k)))
    n_words = len(words)
    target = np.array([1.0 if len(set(w)) == 1 else 0.0 for w in words])
    perms = list(itertools.permutations(range(k)))
    wp, wq = words[:, :k], words[:, k:]
    npar = k * k * 9

    def resid_jac(z):
        W = (z[:npar] + 1j * z[npar:]).reshape(k, k, 3, 3)
        val = np.zeros(n_words, complex)
        J = np.zeros((n_words, k, k, 3, 3), complex)
        for s in perms:
            fac = np.stack([W[p, s[p]][wp[:, p], wq[:, s[p]]] for p in range(k)])
            val += fac.prod(axis=0)
            for p in range(k):
                others = np.prod(np.delete(fac, p, axis=0), axis=0)
                np.add.at(J, (np.arange(n_words), p, s[p], wp[:, p], wq[:, s[p]]), others)
        r = val - target
        Jc = J.reshape(n_words, npar)
        Jr = np.block([[Jc.real, -Jc.imag], [Jc.imag, Jc.real]])
        return np.concatenate([r.real, r.imag]), Jr

    best = None
    for t in range(args.trials):
        z0 = rng.normal(size=2 * npar) * 0.7
        res = least_squares(lambda z: resid_jac(z)[0], z0, jac=lambda z: resid_jac(z)[1],
                            method="lm", max_nfev=4000, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        norm = float(np.sqrt(2 * res.cost))
        print(f"k={k} trial {t}: residual norm {norm:.6e}", flush=True)
        best = norm if best is None else min(best, norm)
    print(f"k={k} best residual norm over {args.trials} trials: {best:.6e}")


if __name__ == "__main__":
    main()
