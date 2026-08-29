# GLD96 hostile review: R31 gate removal

## Verdict

**Verdict: PASS for the strengthened exact `GLD96` scope.**  The factor
`R31` is not inverted or otherwise used as a gate in the bordered-minor
resultant proof.  The exact implication therefore strengthens from

```text
D(R31 E31 H2 g0 Delta)
```

to

```text
D(E31 H2 g0 Delta).
```

This covers `R31=0` points only where the remaining displayed factors are
nonzero.  It does not close `E31=0`, `g0=0`, `H2=0`, `Delta=0`, arbitrary H4
points outside the written normalized offset chart, the GLD83 pulled-back
Fitting obligation, other charts/components/source branches, or the global
Krenn--Gu conjecture.  The global conjecture remains **UNRESOLVED**.

The original 2026-08-28 review remains the provenance record for the
narrower first publication.  This review audits the later scope
strengthening and supersedes only its treatment of `R31` as a localization
factor.

## Exact strengthened claim

Let `T0,...,T3` be the four raw seven-by-seven bordered minors recorded in
the GLD96 owner.  After the GLD88 offset substitution and only
parameter-denominator clearing, write

```text
Ttilde_i = f_i(B) + C g_i(B),
f_i(B) in B K[q]/(Q6)[B],
K = Q(p,a).
```

Let `E31` be the cleared q-resultant/norm gate obtained from the two
cross-polynomials `H01,H02`, let `g0` be the cleared norm of `g_0(0)`, and
let `H2` and `Delta` have their existing GLD96 meanings.  Then

```text
V(Q6,T0,T1,T2,T3) intersect D(E31 H2 g0 Delta)
  is contained in V(B,C).
```

The GLD75/GLD86 bridge and GLD95 subsequently give the scoped incidence
exclusion on `D(Omega E31 H2 g0 Delta)`.

## Why no R31 inverse occurs

Write the common six-by-six submatrix as `P`, with `R31=det(P)`.  For each
added row and column, the exact block-determinant identity is

```text
det [ P  c ] = det(P) x - r adj(P) c.
    [ r  x ]
```

Both sides are polynomials.  The identity is valid when `det(P)=0`; it is
not a Schur-complement formula requiring division by `R31`.

The load-bearing proof uses only the following facts:

1. syndrome rank at most six makes each raw bordered seven-minor `T_i`
   vanish;
2. the exact raw c-degree and the 111 GLD88 common-kernel identities give
   `Ttilde_i=f_i+C g_i` with `B` dividing every `f_i`;
3. on `D(E31 H2)`, the two cross-resultants force `B=0`; and
4. on `D(g0)`, the first remaining equation forces `C=0`.

None of these steps invokes `R31`, divides a `T_i` by `R31`, or solves a
linear system with `P^{-1}`.

## Exact replay evidence

The strengthened primary still reconstructs the full GLD71 syndrome and
pins the raw `R31` factorization as a diagnostic.  It now also compares each
polynomial adjugate expression with the corresponding direct bordered
determinant exactly.  Its result metadata marks `required_as_gate: false`
and records the open as `D(E31*H2*g0*Delta)`.

The independent audit is materially different.  It imports no GLD96
primary or GLD88 builder, accumulates the required syndrome entries directly
from the pinned sparse supports, and computes the four seven-by-seven
bordered determinants by its local Bareiss routine.  It does not compute or
invert the six-by-six `R31` determinant.  It independently replays the Q6
reduction, the two cross-resultants, and the nonzero `E31` and `g0` norms.

The exact resultant tuple hash remains

```text
f0b2368dda1ea6a89d31ccf98242f48ed5d3540a14d412393b7870719780a05b.
```

On the 2026-08-29 reference replay, the canonical primary completed in
`55.938 s` under a `300 s / 12288 MB` bound (`gld96-r31-free-primary-20260829a`),
and the independent audit completed in `4.476 s` under a
`180 s / 12288 MB` bound (`gld96-r31-free-audit-20260829a`).

Thus the strengthening changes no determinant, resultant, norm, or
specialization witness.  It corrects the logical localization attached to
the already audited polynomial identities.

## Adversarial checks

### Raw minor versus pivot residual

The theorem consumes raw seven-minors because rank at most six makes them
zero at every point.  It does not consume a normalized Schur residual.  The
primary's adjugate route and the audit's direct Bareiss route agree on the
same raw polynomial.  Therefore an `R31=0` point does not invalidate the
input equations.

### Denominator scope

The offset substitutions and q-reduction still require `D(Delta H2)`.  The
clearing factors depend only on parameters and never on `B` or `C`.  Removing
`R31` does not remove any chart denominator, nor does it silently include a
`Delta=0` point.

### Generic versus pointwise resultants

The exact `(p,a)=(2,3)` computation proves only that the generic cleared
`E31` and `g0` polynomials are nonzero.  The theorem continues to localize
at both.  No claim is made that either is a unit at every parameter point.

### Downstream scope

After `B=C=0`, GLD95 applies only to its written F88 family on `D(Delta)`.
The strengthened GLD96 result does not enlarge that endpoint theorem and
does not prove a GLD83 raw/Fitting equivalence.  The ninth-column
GLD75/GLD86 bridge remains the exact upstream reason the full syndrome has
rank at most six.

### Double-pivot exploratory lineage

Earlier double-pivot searches remain valid historical controls, but they
are not proof inputs.  The strengthened theorem covers their `R31=0` locus
only on `D(E31 H2 g0 Delta)`; intersections with any retained factor remain
open and must not be described as closed by this review.

## Retained obligations

The live residual wall after this repair is:

```text
E31=0 or g0=0 or H2=0 or Delta=0,
arbitrary H4 outside the written offset chart,
the GLD83 Fitting pullback and higher-rank/raw-response branches,
other gauges, components, sources, profiles, roots, and orders.
```

No global status change follows.  Krenn--Gu remains **UNRESOLVED**.
