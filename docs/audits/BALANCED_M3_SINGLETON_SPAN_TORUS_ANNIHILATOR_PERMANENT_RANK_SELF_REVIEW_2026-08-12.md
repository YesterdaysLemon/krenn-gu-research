# Self-review of the `m=3` singleton-span torus-annihilator obstruction

## Verdict

**PASS at its exact scope; not an independent mathematical review and not a
global-resolution audit.**  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Mathematical audit

The review checked these load-bearing steps.

1. Empty normalization turns target consistency into
   `J-G_N` lying in the fixed total singleton span `U`.  Passing to `A/U`
   is legitimate even when the three pair coefficients have poles, because
   the quotient kills their columns identically and a generically zero
   polynomial section is zero everywhere.
2. Contracting the physical empty companion by a decomposable root
   functional gives the six-bijection local image
   `(L_x tensor L_y tensor L_r)P_3`.  This is a term-by-term identity, not a
   Gaussian or matchgate analogy.
3. If the product functional is nonzero on all nine target coordinates, the
   contracted GHZ tensor is a three-term diagonal with all coefficients
   nonzero.  Every one-mode flattening has rank three.
4. A local image flattening has rank at most the corresponding `L_u` rank.
   Hence all three `3 x 3` maps are invertible.  Their tensor product preserves
   tensor rank.
5. The accepted exact `P_3` theorem gives tensor rank four; the concise
   diagonal has tensor rank three.  This is the contradiction.  No assertion
   about rank-two or zero boundary restrictions is imported.
6. `Seg(P^2 x P^2 x P^2)` has dimension six and `P(U^perp)` has codimension
   `dim U`.  The projective dimension lower bound is therefore `6-dim U`
   when `dim U<=6`.  The obstruction puts the entire intersection, not merely
   sampled points, in the nine coordinate boundary divisors.

The target diagonal plane sharpness example correctly blocks every fully
supported product annihilator.  It is also correctly excluded from the
common-three-space full-sensor stratum because target consistency would put
the empty column in that same three-space.

## 2. Evidence and independence

The SymPy primary reconstructs `P_3`, all three flattenings, the slice-minor
lower-bound certificate, the four-term polarization, a generic physical
six-bijection contraction, the diagonal rank, and the target-plane boundary.

The standard-library audit imports neither SymPy, the primary, nor repository
code.  It builds sparse tensors directly from permutations, performs exact
`Fraction` row reduction, independently applies fixed invertible local maps,
enumerates the six cross matchings, and replays the polarization and boundary
checks.

```text
primary replay:              PASS;
independent python -I audit: PASS;
Python compilation:          PASS;
Ruff 0.16.2:                 PASS.
```

The scripts replay the fixed tensor identities.  The quotient argument and
projective dimension statement are the written proof.

## 3. Scope firewall

```text
all singleton spans admit a torus product annihilator:       FALSE;
all boundary product annihilators are excluded:              NOT PROVED;
rank-two P3 restrictions are impossible:                     NOT CLAIMED;
the common-three-space pole stratum is empty:                 NOT PROVED;
the rank-one and pair-plane pole strata are empty:            NOT PROVED;
the argument applies unchanged to m>=4:                      FALSE;
the all-balanced rank-drop branch is excluded:                NOT PROVED;
the global Krenn--Gu conjecture is resolved:                  FALSE.
```

The exact next obligation is the coordinate-boundary product-annihilator
classification, using the already proved zero and decomposable `P_3`
restriction theorems without assuming that every boundary contraction is
zero or pure.
