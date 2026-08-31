# GLD101 residual-factor parent attempt

## Status and purpose

This is a **parent-theorem attempt**, not a theorem and not a global proof.
It records the synthesis required before any third residual-factor sibling is
proposed beneath GLD101.  At this checkpoint the global Krenn--Gu conjecture
remains **UNRESOLVED**.

The attempt concerns only the normalized GLD88/F88 equal-leaf H4 chart in
characteristic zero, with

```text
a=0,
Q6(p,q)=0,
H2(p) Delta(p,q) != 0.
```

It does not address the endpoint after the offsets vanish, the full E31 wall,
arbitrary `a`, another H4 chart, another component or source branch, physical
incidence, the pulled-back Fitting ideal, other roots or orders, or global
gluing.

## 1. Exact parent proposition

Let `k` be an algebraically closed field of characteristic zero.  On the
normalized GLD88 H4 chart, specialize `a=0`.  Let

```text
Q6, T0, T1, T2, T3, D0, Y0, Y1, X3 in k[p,q,B,C]
```

denote the tracked Q6 equation and denominator-cleared numerators of eight
actual seven-minors.  On `D(Delta)` each numerator vanishes exactly when its
raw rational minor vanishes.  The corrected parent proposition under attack
is

```text
Q6=T0=T1=T2=T3=D0=Y0=Y1=X3=0
and H2*Delta != 0
    => B=C=0.                                      (P8)
```

The quantifiers in (P8) range over all `p,q,B,C` in this one normalized chart.
Every leaf identity is an exact polynomial identity over `QQ` after clearing
only denominators proved nonzero on `D(H2*Delta)`.  Tensoring those identities
with any algebraically closed characteristic-zero `k` preserves the unit and
contradiction certificates, so the coefficient-field computations used below
base-change to the stated field without a pointwise sampling inference.
The intended upstream use is one-way: complete syndrome rank at most six
forces all eight actual seven-minors to vanish, so (P8) would force the two
chart offsets to vanish.  No converse from the selected minors to complete
syndrome rank is needed or claimed.

The first version of this attempt stated the six-selector implication

```text
Q6=T0=T1=T2=T3=Y1=X3=0 => B=C=0.                 (P6)
```

The adversarial parent audit found that the R110 multiplier identity uses
`D0` and `Y0` with nonzero multipliers.  It therefore proves the R110 leaf of
(P8), or directly of a rank-at-most-six parent, but does not prove (P6).
This is a load-bearing implication repair: (P6) remains unproved because the
separate compact-kernel probe was inconclusive.  Enlarging to (P8) is enough
because the six GLD101 norm-cover selectors are a subset of these eight, and
the upstream rank hypothesis forces all eight.

The intended downstream consumer is the existing GLD95 endpoint theorem,
but only after the separate physical incidence bridge supplies its hypotheses.
Thus even a proof of (P8) would be a scoped algebraic offset closure, not a
physical empty-set theorem.

## 2. Exhaustive open cover and GLD101 support supply

The nonzero-offset locus has the exhaustive cover

```text
D(B) union (V(B) intersect D(C)).                  (1)
```

On `D(B)`, put `C=B*t` and divide the common factor `B` from each selected
minor.  On `V(B) intersect D(C)`, divide the common factor `C`.  These are the
only two offset charts used below.

GLD101 proves the following necessary support statement on
`D(H2*Delta)`: if the six selected minors vanish at a nonzero-offset point,
then

```text
(p-1)*p*(p^2+1)*P*H2*R4*R8*R110 = 0.             (2)
```

Here

```text
P   = p^2-p+1,
R4  = 5*p^4-16*p^3+30*p^2-16*p+5,
R8  = 64*p^8-256*p^7+580*p^6-844*p^5
      +946*p^4-784*p^3+388*p^2-94*p+13,
```

and `R110` is the pinned degree-110 primitive factor in the GLD101
certificate.  The `P` support lies on `Delta=0`, and the `H2` support lies
outside the declared `D(H2)` open.  Since the six GLD101 selectors are a
subset of the eight hypotheses in (P8), a proof of (P8) reduces exactly
to:

1. the `p=0` and `p=1` fibres;
2. the `p^2+1` fibre;
3. the `R4` fibre;
4. the `R8` fibre; and
5. the `R110` fibre,

on the two offset charts in (1).  This is an exhaustive consequence of the
proved GLD101 norm cover; it is not an inference from numerical factor
sampling.

## 3. Sibling mechanisms being synthesized

This attempt combines more than the conclusions of nearby factor checks.
The following factor and chart mechanisms are relevant.

### 3.0 The p=0,1 base fibres at a=0

GLD102 is stated upstream as a rank-at-most-six theorem, but its two offset
chart calculations use only the displayed six-selector subsystem, which is a
subset of (P8).  This is enough for the present parent: on `p=1` the
six-selector B-open locus is empty, while on `p=0` its only two B-open
survivors have `a=1`, hence are absent after this parent's `a=0`
specialization.  The C-open six-coefficient ideals are unit for both fibres.
Thus this use does not import GLD102's full-rank conclusion backwards from
selected minors; it records the exact a=0 selected-minor sub-implication that
the parent needs.

### 3.1 Uniform C-open coefficient obstruction

After setting `B=0` and cancelling `C`, every selected minor is linear in the
remaining open coordinate.  The tracked GLD71/GLD88 construction gives six
exact coefficients in `QQ(p)[q]/(Q6)`.  Their saturated ideal

```text
<Q6, h_T0, h_T1, h_T2, h_T3, h_Y1, h_X3,
 z*H2*Delta-1>
```

has exact unit basis.  This is an arbitrary-`p` mechanism on the C-open
boundary; it eliminates that whole chart at once and does not need a
factor-by-factor sibling theorem.

The independent audit rebuilt the six coefficients from the pinned GLD71 and
GLD88 parents before reading the downstream source, checked every rational
denominator against `H2*Delta`, and replayed the unit computation exactly.
The first two audit attempts failed closed on support-manifest and archived
PID-identity checks and remain non-evidence.  The repaired third audit is the
accepted scoped evidence.

### 3.2 Compact B-open unit identities

For `p^2+1` and `R4`, direct rational-minor reconstruction followed by
`C=B*t` and common-`B` division produces exact raw numerator systems.  Small
selector subfamilies already generate the unit ideal with `Q6`:

```text
p^2+1: <Q6,H_T3,H_Y1,H_X3> = (1),
R4:    <Q6,H_T3,H_Y1,H_X3> = (1).                 (3)
```

The direct equations and their Delta-supported denominators are separately
bridged to the tracked quotient-algebra determinants.  On `p^2+1`, the
published `p=i` identity also covers `p=-i` by coefficient conjugation: the
unreduced equations have rational coefficients, conjugation fixes `Q6` and
the ideal operations, and sends the exact `p=i` identity to the exact
`p=-i` identity.  This conjugation step is load-bearing and must be explicit
in any theorem package.

For `R4`, independent determinant regeneration matches the three raw
numerators exactly after factor reduction.  Two separately constructed
exact multiplication-back routes verify the disclosed unit identity.  These
computations establish only (3) in the stated coefficient fields.

### 3.3 Five-row cofactor-kernel obstruction

The R8 work exposes a smaller parent-style mechanism than a Gröbner basis.
Five B-open selector equations are linear in the six monomial coordinates

```text
(t,1,B*t,B,B^2*t,B^2).                             (4)
```

Let `M` be their `5 x 6` coefficient matrix and `K` its signed cofactor
kernel.  The exact identities are

```text
M*K=0,
gcd(Q6,K6)=1,
gcd(Q6,K2)=gcd(Q6,K3*K2-K1*K4)=L,                 (5)
```

with the same nonzero linear polynomial `L` in the last two gcds.  The first
gcd gives rank five at every Q6 point.  A physical monomial vector (4) has
second coordinate one and satisfies

```text
x3*x2-x1*x4=0.                                    (6)
```

Rank five makes it a scalar multiple of `K`.  Equations (5)--(6) force
`L=0`, hence `K2=0`, contradicting the second coordinate one.  This is a
compact exact obstruction.  The independent audit regenerated the five
tracked-parent equations without importing the candidate implementation,
proved exact rowwise unit equivalence in `QQ[p,q]/(R8,Q6)`, replayed all
cofactor and gcd identities, and checked the monomial-vector inference.
Two preliminary comparison attempts that used the wrong `Q6` normalization
or an overly strong single-unit-pivot condition remain quarantined
non-evidence.

This kernel argument explains why the R8 full six-selector unit screen can
be replaced by a small human-auditable certificate.  It also identifies the
structural parent mechanism to seek on R110: a low-row coefficient matrix,
an exact cofactor kernel, and a monomial-semigroup relation, rather than a
sequence of opaque factor-specific Gröbner searches.

### 3.4 R110 eight-minor q-substitution certificate

The accepted R110 B-open certificate is an exact identity in the ideal

```text
<Q6, R110, T0, T1, T2, T3, D0, Y0, Y1, X3, z*B-1>.
```

Its replay uses nonzero multipliers of `D0` and `Y0`, so this is deliberately
an eight-actual-minor certificate for (P8), not a six-selector certificate
for (P6).  A no-import audit first regenerated the nine coefficient tables
from tracked GLD71/GLD88 data, checked the degree-548 norm and the
multiplicity-one R110 factor, all coefficient-field/Delta/linear-relation
gates, and only then reconstructed and replayed the B identity.  The generic
C-open certificate already removes the other offset chart for arbitrary `p`;
the separately accepted R110 C-open replay is corroborative rather than
load-bearing for (P8).

An exploratory attempt to replace this with the R8-style five-row
six-selector cofactor kernel passed the R110 root gates but became
inconclusive during the first degree-110 cofactor calculation.  It supplies
neither a proof nor a counterexample to (P6).

## 4. Hostile controls and known no-go boundaries

The synthesis has been tested against the following failure modes.

1. **No selector converse.**  The parent uses only
   `rank <= 6 => selected minors vanish`.  Nothing below infers complete rank
   from the selected equations.
2. **No ambient-polynomial comparison.**  Raw direct minors can retain high
   powers of `q`, while the tracked primary lives in
   `QQ(p)[q]/(Q6)`.  Comparisons are made in the quotient algebra with every
   cleared denominator proved to lie on the declared Delta gate.
3. **No silent field-point loss.**  `p^2+1`, `R4`, `R8`, and `R110` are
   treated through exact coefficient fields or all conjugate roots.  The
   `p=-i` conjugate of the Gaussian identity is not omitted.
4. **No Delta/H2 promotion.**  A factor supported on `Delta=0` or `H2=0`
   is outside (P8), not closed by an open-chart calculation.
5. **No endpoint promotion.**  All B-open and C-open arguments stop at
   `B=C=0`; the endpoint is a separate GLD95/physical-incidence obligation.
6. **No arbitrary-a promotion.**  Except for the already proved GLD102
   `p=0,1` fibres, the present factor work is specialized to `a=0`.
7. **No timeout evidence.**  Interrupted subset probes and unsuccessful
   audit versions are retained as failed or inconclusive runs and are not
   inputs to (P8).
8. **No modular promotion.**  Modular screens may guide selector choice but
   do not discharge any item in the exact factor cover.

The Gaussian E31 control reconstruction is a regression guard for the
tracked Q6/selector provenance and for the known wall geometry.  It is not a
proof that the four residual factors exhaust the full E31 wall.

## 5. Current result of the parent attempt

At this checkpoint:

```text
C-open, arbitrary p on D(H2*Delta): independently accepted;
p=0,1 a=0 selected-minor subcase:     supplied by GLD102;
p^2+1 B-open:                         independently accepted;
R4 B-open:                            independently accepted;
R8 B-open cofactor-kernel:            independently accepted;
R110 P8 B-open q-substitution:         independently accepted;
R110 C-open q-substitution:            independently accepted, corroborative;
R110 six-selector compact probe:       inconclusive non-evidence.
```

The factor cover now supplies the claimed implication (P8), but (P8) is
**not yet promoted to a theorem**.  The load-bearing next work is to package
the accepted leaf identities and independent receipts into a clean-clone,
path-portable certificate/audit seam, then complete adversarial consolidation.
The original six-selector proposition (P6) remains open: the compact R110
probe was inconclusive and the accepted R110 identity proves only the larger
eight-minor system.

## 6. Proof-topology delta

The live frontier is unchanged by this attempt.  No new theorem edge is
recorded until the accepted P8 composition is independently consolidated and
made clean-clone reproducible.  The proposed future delta, conditional on
that packaging and consolidation, would be

```text
GLD101
  -> complete a=0 nonzero-offset closure on D(H2*Delta)
  -> B=C=0 endpoint / physical-incidence and wider E31 obligations remain.
```

That conditional edge would close only the normalized `a=0` nonzero-offset
part of the GLD101 factor cover.  It would not change the `UNRESOLVED` global
status.
