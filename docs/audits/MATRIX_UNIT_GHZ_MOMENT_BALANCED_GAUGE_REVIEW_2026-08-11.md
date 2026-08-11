# Hostile review of the matrix-unit GHZ moment-balanced gauge

## Verdict and provenance

**PASS, as an exact complex-analytic normal-form theorem and a sharp phase
boundary.**  The proof correctly upgrades the auxiliary positive incidence
balance of the preceding theorem to a positive diagonal GHZ gauge in which
the actual squared physical amplitudes have vertex-independent colour
loads.  The minimizer is unique only after quotienting by the edgewise
stabilizer, exactly as stated.

The eight-vertex table is accepted only as a sharpness model.  It has exact
unit phases, actual moment balance, the three pure target coefficients, two
target-correct active fibres, and the forced ternary bridge pattern.  It
also has an exposed mixed coefficient equal to one.  It is not a witness or
counterexample, and it makes no geometric no-deeper/deeper classification.

The `r=1` branch and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. The field scope is not silently strengthened

The predecessor endpoint-balance theorem is a rational linear theorem and
supports characteristic-zero formulations.  The new theorem uses

```text
a_e=|lambda_e|^2,
positive real exponentials,
coercivity and strict convexity.
```

It is therefore stated over `C`.  Exact here means that the proof and finite
sharpness calculations use exact identities, not that absolute value is an
algebraic operation over every characteristic-zero field.  No descent to an
arbitrary field is asserted.

## 2. Strict all-edge balance is the load-bearing hypothesis

Let `S` be the image of the zero-colour-sum Lie algebra under the edge-
exponent map.  The predecessor theorem supplies `p_e>0` on **every**
physical edge with

```text
p dot z=0 for every z in S.
```

For a nonzero `z in S`, this forces both a positive and a negative
coordinate.  On the unit sphere of `S`, the maximum positive coordinate has
a uniform positive lower bound by compactness.  This is exactly what makes

```text
sum_e a_e exp(2z_e)
```

coercive.  A merely nonnegative dual vector could vanish on the coordinates
that escape to positive infinity and would not support the proof.

The argument does not assume that the auxiliary `p_e` equal the physical
`a_e`.  It uses the former only to establish coercivity for the functional
defined from the latter.

## 3. The quotient handles all stabilizers

The exponential functional is constant along

```text
K={x:r_e(x)=0 for every physical edge e}.
```

Its Hessian is

```text
4 sum_e a_e exp(2r_e(x)) r_e(y)^2.
```

This is positive definite on the quotient and may be singular on the
unquotiented Lie algebra.  The theorem consequently claims uniqueness
modulo `K`, not uniqueness of all local scale factors.

This distinction is realized by the sharpness table: the zero-colour-sum
Lie algebra has dimension 21, the edge-exponent map and Hessian have rank
20, and an exact one-dimensional edgewise stabilizer remains.  The finite
audit explicitly exhibits it.

## 4. The critical equation is exactly endpoint moment balance

At the unique quotient minimizer, differentiation in every zero-colour-sum
direction gives

```text
sum_e |lambda'_e|^2 r_e(y)=0.
```

The transpose incidence vector therefore lies in the orthogonal complement
of the zero-colour-sum subspace.  That complement consists of arrays which,
for each fixed colour, are constant over vertices.  This is precisely

```text
sum_(e incident to v, ell_v(e)=c) |lambda'_e|^2=q_c.
```

The new positive quantities are the actual squared magnitudes after gauge,
not a relabelling of the predecessor's auxiliary integer multicover.

For a target realization every pure colour coefficient is nonzero, so at
least one pure matching exists in each colour and every vertex sees that
label.  Since all squared edge magnitudes are positive, each `q_c` is
strictly positive.

## 5. The gauge preserves the full target

The local scale products are one in each colour because the logarithmic
scale vector has zero colour sums.  Every constant target coordinate is
therefore fixed.  A mixed coordinate is multiplied by a nonzero word-
dependent scalar; since its target value is zero, it remains zero.  Thus the
action fixes `Delta_(n,3)` exactly, not merely its pure coordinates.

Only positive real diagonal scalings are used.  They do not rotate or align
any phase.  The theorem does not claim a normal form for the full local
general-linear action.

## 6. The exact phase table defeats the tempting positivity argument

Write an Eisenstein number as `a+b omega`, with
`omega^2+omega+1=0`.  Its squared modulus is

```text
a^2-ab+b^2.
```

The primary and independent checkers agree on the following exact data:

```text
physical pairs present:                     28 of 28;
every physical squared magnitude:           1;
actual colour load at every vertex:         (3,2,2);
zero-sum Lie dimension / exponent rank:      21 / 20;
pure coefficients:                          (1,1,1);
chi_0 diagonal/offdiagonal values:           (1,-1);
chi_1 diagonal/offdiagonal values:           (1,-1);
an exposed mixed coefficient:               1;
perfect matchings enumerated:               105.
```

The pure zero coordinate is

```text
(-omega)+(-omega^2)=1,
```

while each selected mixed active fibre cancels as `1+(-1)=0`.  Thus even
unit magnitudes and exact moment balance leave full phase cancellation
intact.

The cross core

```text
04=(0,1), 15=(1,2), 23=(2,0)
```

and bridges

```text
24=(0,0), 05=(1,1), 13=(2,2)
```

reproduce the support, word-change, and scalar algebra of the existing
active transport theorem.  Since the table violates another mixed target
coordinate, it is not an instance of the full trichotomy and cannot certify
either absence or presence of the geometric deeper component.

## 7. Proper nonrigidity is not resolved by magnitude balance

The independently recomputed sets are

```text
S_0={0,2,3,4,5,6},
S_1={0,1,3,4,5,6,7},
S_2={1,2,3,6,7}.
```

All are nonempty and proper despite complete support, unit magnitudes,
moment balance, and exact pure targets.  This refutes only the shortcut that
those conditions alone force global nonrigidity.  It does not refute or
prove propagation under the complete mixed target system because the table
is a nonwitness.

## 8. Computational independence

The primary checker represents `Q(omega)` in its rational basis, enumerates
all labelled perfect matchings, computes rational Gaussian ranks of the
incidence matrix and Gram Hessian, and exactly reverses a nontrivial rational
GHZ scaling.

The no-import audit uses decimal endpoint codes, integer coefficient pairs,
a compatible-word bitmask recursion, an alternate vertex anchor, modular
rank, and a separately hard-coded exact stabilizer.  Modular rank 20 gives a
lower bound over `Q`, while the nonzero exact kernel vector gives the
matching upper bound.  The two implementations therefore do not share the
primary matching or elimination routines.

Neither finite program proves the arbitrary-order analytic theorem.  That
proof is the coercive strict-convexity argument in the claim document.

## 9. Accepted proof-topology update

```text
support-minimal matrix-unit GHZ realization
  -> strict positive endpoint incidence balance       PROVED
  -> coercive positive GHZ-torus moment functional    PROVED over C
  -> actual squared amplitudes balanced after gauge   PROVED over C
  -> phases or matching sums synchronized             FALSE
  -> pure targets plus balance close active transport FALSE
  -> full mixed equations close r=1                   OPEN

proper nonrigidity propagation:                       OPEN;
pure-shore cancellation and active holonomy:          OPEN;
deeper-blocker branch:                                OPEN;
r=1 matrix-unit branch:                               OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Strongest fresh-referee objection

The dangerous inference is that a moment-balanced representative converts
the complex coefficient equations into a positive matching model.  It does
not.  Moment balance controls only sums of squared **edge** magnitudes at
labelled endpoints.  Tensor coordinates are sums of products of complex
edge amplitudes, and their phases remain unconstrained by the positive
gauge.  The exact unit-phase table is decisive: it sits at the moment
minimum and still realizes the full local active-transport cancellation
mechanism.  Any next proof must couple phases with the complete mixed
equations or with the remaining geometric exits; the convex argument cannot
be iterated as if it supplied termwise positivity.
