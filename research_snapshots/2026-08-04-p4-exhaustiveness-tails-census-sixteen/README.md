# Exhaustiveness tails: two walls closed, three more components, census sixteen

Follow-up sweep to
[`../2026-08-04-p4-exhaustiveness-sweep-census-thirteen/`](../2026-08-04-p4-exhaustiveness-sweep-census-thirteen/README.md),
which left four honest tails.  Two of them are now **closed**, and the
largest one — the case-`Y` survivor walls of the coincident-support
`(b2)`-chart — turns out to contain **three further pure-compression
components**.  The certified census lower bound moves from thirteen to
**sixteen**.

Exact computations over `Q` (sympy rationals + Singular), fail-closed:
every Singular call raises on timeout or mismatch, and no claim is made
that a script does not assert.

## Tail 1 (CLOSED): the `Zc` wall is a wall of the SEVENTH component

`w01_Zc_wall_is_seventh_wall.py` identifies the `Zc` branch — the
rank-two-pair-edge branch left open with incidence tangent seven — as
the seventh component's `b = e` wall, by exact span identification.
`w02_Zc_localdim_six_slice.py` then certifies, by a char-0 six-slice
`ds` standard basis, that the local dimension of the pure locus at the
`Zc` sample is at most six; with the seventh passing through it the
local dimension is exactly six.

**No fourteenth component arises here.**  Corollary: the previous
snapshot's `s13` five-slice could never have returned local dimension
zero, so its recorded timeout is moot rather than merely unresolved.

## Tail 2 (CLOSED): the `e = 1` case-alpha leaf lies in the ELEVENTH

`w03_e1_case_alpha_resolution.py` resolves the coincident-`Pi`-position
leaf: every nonzero pure point of the `e = 1` case-alpha branch lies in
the eleventh component orbit (the `C10` walls at `c0 = c1 = 1` together
with their boundary charts).  The four survivor strata that the earlier
`s12` stratification had flagged — `{x || e0}`, `{v || e0}`,
`{s = 0, x in P01}`, `{s = 0, v in P01}` — are **chart artifacts of an
empty stratum**; all remaining branches carry only the zero
restriction.

## Tail 3: the case-`Y` survivor walls contain THREE new components

Setting (from the previous snapshot's `s09`): the coincident-support
`(b2)`-chart in case `Y` (`K3 = u3`), with

```text
ybar=(1,-1,0,0),  u3=(1,1,0,0),
U1=span(ybar,p),  p=(0,1,p2,p3),
U2=span(ybar,q),  q=(0,1,q2,q3),
U3=span(u3,w),    w=(0,wv1,wv2,wv3),
U0 in Gr(2, ker Y1),  Y1=(P,P,p3+q3,p2+q2),  P=p2 q3+p3 q2.
```

Of the residual purity system's nonzero-restriction primes, seven pass
the calibrated semicontinuity sieve against **no** census image of any
of the thirteen certified orbits.  Under the chart symmetries they form
three classes, and `w05_new_components_14_15_16.py` certifies each:

| class | primes | normal form | dim | profile | certificate |
|---|---|---|---|---|---|
| A | {11,12,26,28} | `q_Pi \|\| p_Pi`, `aY=al*p3`, `bY=be*p2`, `al+be+lam=0` | 5 | `(4,4,4,3,3,3)` | tangent 5, incidence **15** — a smooth point |
| B | {15,16} | `wv1=0` (`w in Pi`), `aY,bY` by rational solve | 5 | `(4,4,3,4,3,3)` | tangent 5, incidence **15** — a smooth point |
| C | {13} | `p_Pi \|\| q_Pi \|\| w_Pi`, conic-bundle | 5 | `(4,4,4,3,3,3)` | tangent 5, incidence 14 — singular; char-0 five-slice |

Classes A and B are the first new components since the seventh to be
certified by the **classical smooth-point argument** (incidence rank
fifteen at the sample, so the incidence locus is smooth of dimension
five there and the rational irreducible fivefold through it is the
unique component).  Class C is singular and uses the slice
standard-basis pattern of the eleventh.

Separation is verified inside the same script: the calibrated sieve
(self-alignment and two known containments as calibrations) passes no
alignment of any of the three samples against any of the thirteen
certified orbits, and the three classes are mutually sieve-separated,
with classes A and C additionally distinguished by an explicit orbit
image computation.

### A correction to the class-C tangent (`w06`)

The first draft of `w05` measured the class-C family tangent with the
same helper it used for classes A and B, differentiating in all six
parameters freely — but the class-C parametrization is pure **only on
its conic** `Q = 0` (every purity minor equals a parameter monomial
times `Q`).  The unconstrained Jacobian therefore has rank **six**,
counting a direction that leaves the pure locus, and the script's
`assert rkC == 5` failed.

`w06_classC_constrained_tangent.py` diagnoses this standalone and
computes the correct quantity — the Jacobian restricted to the tangent
hyperplane of `{Q = 0}` — obtaining rank **five**, consistent with the
five-slice bound.  `w05` in this snapshot carries the fix (the tangent
helper now takes an optional constraint) and runs green end-to-end.
Without the fix the rank-six reading would have contradicted the
script's own local-dimension bound, so this is a correctness fix, not a
cosmetic one.

## The updated census

Sixteen certified component orbits: eleven fivefolds, three sixfolds
(seventh, tenth, eleventh), and the two rank-sum-19 fivefolds of the
previous snapshot, plus the three above.

```text
14th = closure(F_A): dim 5, profile (4,4,4,3,3,3), K1=p, K3=u3, q_Pi||p_Pi
15th = closure(F_B): dim 5, profile (4,4,3,4,3,3), w in Pi
16th = closure(F_C): dim 5, profile (4,4,4,3,3,3), p||q||w in Pi, conic bundle
```

## What remains open

1. the `p`-in-`Pi` walls of the `(b2)`-chart (codimension `>= 2`);
2. the `P = 0` chart degeneration of case `Y`, needing the alternate
   kernel chart;
3. the Task-C boundary leaves never swept: support-degenerate star
   centres, lower-rank `Delta`, mixed rank-one/rank-two strata, and the
   identification of the triangle chord walls inside the census;
4. standalone theorem documents, independent audits, and `H31`/`H22`
   obstructions for the twelfth through sixteenth components;
5. the global exhaustiveness theorem — **sixteen is a certified lower
   bound, not a census**.

The discovery pipeline that produced the seven pass-none primes
(`w04`) was lost when the session that generated it was interrupted;
`w05` re-derives what it needs by checking that each normal form
satisfies the recorded prime generators identically, and performs its
own sieve separation, so the certificates here are self-contained.

## Script index

- `w01_Zc_wall_is_seventh_wall.py` — `Zc` = the seventh's `b = e` wall.
- `w02_Zc_localdim_six_slice.py` — char-0 six-slice: local dimension
  exactly six at the `Zc` sample.
- `w03_e1_case_alpha_resolution.py` — the `e = 1` case-alpha leaf lies
  in the eleventh; `s12`'s survivors were chart artifacts.
- `w05_new_components_14_15_16.py` — normal forms, purity, invariants,
  sieve separation, tangents, incidence ranks, slices: the fourteenth,
  fifteenth, and sixteenth components (class-C tangent corrected).
- `w06_classC_constrained_tangent.py` — standalone diagnosis of the
  class-C constrained-tangent correction.
