# Hostile review of balanced Cramer pair-pole differential flatness

## Verdict and provenance

This review accepts
[`BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md`](../../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md)
as an exact characteristic-zero refinement of the balanced full-sensor gate.
It accepts the replacement

```text
prime-divisor regularity of every Cramer pair component

by

finite nonendpoint first stresses plus endpoint Hessian stresses.
```

The accepted result is a finite symbolic reformulation of one open gate.  It
is not a proof that any target incidence fails that gate.  It does not close
the full-sensor branch, the all-balanced rank-drop branch, or the Krenn--Gu
conjecture.

The primary verifier and independent no-import audit were written for this
checkpoint.  They are separate implementations, not independent authors.
The written differential-algebra argument, rather than either bounded replay,
is the arbitrary-order proof.

A fresh read-only hostile pass from the disjoint Lumen lane found no P0 or P1
defect.  Its P2 scope and characteristic objections and P3 evidence-hardening
requests were incorporated before publication: the examples below are now
stated only as ambient degree-lemma controls, and both scripts enumerate every
claimed pass-layer identity and check the displayed multidegrees.

## 1. Imported obligation and exact scope

The predecessor
[`balanced Cramer--Euler pair-pole gate`](../../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)
has already proved the following statement on a generically full balanced
sensor.

1. A nonzero maximal minor `beta` and its Cramer vector `v` give the unique
   rational target lift `C=v/beta` when every target residual vanishes.
2. Empty normalization and the Euler--hafnian recurrences are separate
   conditions.
3. After the recurrences hold, regularity of the whole deck is equivalent to
   regularity of its pair components.
4. For each pair `e`, regularity is expressed as

   ```text
   nu_P(v_e)>=nu_P(beta)
   ```

   at every prime divisor in a compatible line-bundle frame.

The new theorem imports all four points.  It does not re-prove target
consistency or Euler--Wick equivalence and must not be cited without that
predecessor when claiming the complete globalization gate.

The new proof begins only with one Cramer pair rational section

```text
f_e=v_e/beta
```

whose affine-cone multidegrees are one at the endpoints and zero everywhere
else.  This degree statement comes from the summand `O(1_e)` of the complete
deck bundle.  It would be false for an unrelated rational scalar function.

## 2. Denominator clearing

For a coordinate derivative `partial`, the displayed first stress is

```text
S=beta partial(v)-v partial(beta).
```

The quotient rule gives exactly

```text
S=beta^2 partial(v/beta).
```

There is no missing factor or sign.

For two coordinate derivatives `partial_a,partial_b`, differentiating the
quotient twice gives

```text
beta^3 partial_a partial_b(v/beta)
 = beta^2 partial_a partial_b(v)
   -beta(
       partial_a(v) partial_b(beta)
       +partial_b(v) partial_a(beta)
       +v partial_a partial_b(beta))
   +2v partial_a(beta) partial_b(beta).
```

This is exactly the theorem's Hessian stress.  The coefficient two and the
three terms inside the middle parenthesis are all necessary.  The formula
also covers `a=b`; in that case the first two middle products coincide, as
they should.

The primary derives these identities with generic symbolic functions.  The
no-import audit instead evaluates complete value/gradient/Hessian jets at an
exact rational point, constructs inversion in the jet algebra from scratch,
and compares the results with independently represented sparse polynomials.
The no-import calculation is exact but specialized and pointwise; it
corroborates the powers `2` and `3`.  The displayed quotient-rule derivation
and the generic primary identity carry the universal claim.

## 3. Why the finite jets imply a constant bilinear block

This is the load-bearing theorem step.

Let the endpoints be `p,q`.  Vanishing of every nonendpoint stress gives

```text
partial_(w,a) f_e=0
```

for every coordinate in every `w notin {p,q}`.  Over characteristic zero,
the common constant field of all those coordinate derivations is precisely
`K(z_p,z_q)`.  Hence `f_e` has no rational dependence on an outside group.

Next, every second derivative in the `p` variables vanishes.  Therefore each
first `p` derivative is independent of `z_p`.  A rational function with zero
Hessian is affine-linear over the remaining constant field; the known
degree-one `p` homogeneity and Euler's identity remove its affine constant.
Thus

```text
f_e=sum_a z_(p,a) A_a(z_q).
```

The `q`-Hessian identities imply that every `A_a` has zero `q` Hessian.  The
degree-one `q` homogeneity again removes the affine constants, leaving

```text
A_a=sum_b W_(a,b) z_(q,b)
```

with `W_(a,b) in K`.  This is one constant bilinear form.

Three hostile alternatives were checked.

- A rational outside ratio cannot survive: some outside first derivative is
  nonzero in characteristic zero.
- A rational endpoint ratio cannot survive: its endpoint Hessian is nonzero
  unless the ratio cancels to a linear form.
- An affine endpoint constant cannot survive the prescribed degree-one
  homogeneity.

Positive characteristic is correctly excluded.  For example, `x^p` has zero
derivative in characteristic `p`, so the constant field enlarges and zero
Hessian no longer forces affine linearity.  The degree-one Euler identities
themselves require no division by a nonunit integer.

## 4. Cone and projective meanings agree

The Cramer pair is not treated as a scalar function on projective space.  It
is represented on the product of affine cones as a multihomogeneous rational
function of degree

```text
(...,1 at p,...,1 at q,...,0 elsewhere,...).
```

Such functions are the equivariant rational representatives of rational
sections of `O(1_e)`.  A constant endpoint-bilinear representative therefore
descends to a global section of precisely that bundle.

Conversely, the product of projective spaces is smooth and normal.  A rational
line-bundle section is global exactly when it has nonnegative valuation in a
regular local frame at every prime divisor.  Its global-section space is

```text
H^0(X,O(1_e))=L_p^* tensor L_q^*.
```

Therefore the predecessor's valuation condition, global regularity, one
constant bilinear block, and the new differential identities are genuinely
equivalent.  Codimension-at-least-two extension is not being silently added;
it is already the normality argument in the predecessor theorem.

## 5. Coordinate and Cramer-chart invariance

Vanishing of all first derivatives in one entire vector-space group is
invariant under a linear change of basis in that group.  Likewise, vanishing
of the full symmetric Hessian is invariant under endpoint basis changes.
The theorem does not select a privileged physical coordinate direction.

On an overlapping Cramer chart, target consistency gives

```text
v/beta=v'/beta'.
```

The differential conditions are properties of this common rational section.
Equivalently, if a common rational factor `g` changes the representatives to

```text
(beta',v')=(g beta,g v),
```

then the first stresses multiply by `g^2` and the Hessian stresses multiply
by `g^3`.  Hence their vanishing is unchanged wherever either Cramer chart is
defined, and therefore as a function-field identity.

The primary checks these covariance exponents with a nonconstant common
factor.  The independent audit checks every first and every second coordinate
of a separate sparse-polynomial example.

## 6. Finite count and reconstruction

At ternary local dimension, every outside vertex contributes three first
stresses.  There are `m-2` outside vertices.  A symmetric `3 x 3` Hessian has
six entries, and there are two endpoint Hessians.  Thus the count per pair is

```text
3(m-2)+6+6=3m+6.
```

No mixed endpoint Hessian is a vanishing condition.  Instead it reconstructs
the block:

```text
partial_(p,a)partial_(q,b) f_e=W_(a,b).
```

The determinant-cleared version has numerator `beta^3 W_(a,b)`.  Both
implementations reconstruct all nine entries of a nonsymmetric integer
`3 x 3` test block.  Nonsymmetry is appropriate because `W_pq` is bilinear
between two different local spaces; physical graph symmetry relates
`W_qp` to its transpose and does not require the displayed `p`-by-`q` matrix
itself to be symmetric.

For all nonroot pairs, the finite regularity layer contains

```text
binomial(m,2)(3m+6)
```

identities.  This is a symbolic family size, not permission to replace a
polynomial identity with finitely many unproved evaluations.

## 7. Ambient sharp omission controls

The transverse example

```text
beta=r_1,
v=r_0 x_0 y_0,
f=(r_0/r_1)x_0y_0
```

has endpoint bidegree `(1,1)`, degree zero in the outside `r` group, and
vanishing endpoint Hessians.  Its first stress in `r_0` is

```text
r_1 x_0y_0,
```

and it has a pole on `r_1=0`.  Thus endpoint Hessians do not imply transverse
constancy.

The endpoint example

```text
beta=x_1,
v=x_0^2 y_0,
f=(x_0^2/x_1)y_0
```

has endpoint bidegree `(1,1)` and no outside dependence.  Its `x_0,x_0`
Hessian stress is

```text
2x_1^2y_0,
```

and it has a pole on `x_1=0`.  Thus transverse stresses do not imply endpoint
linearity.

Both examples obey the theorem's multidegrees.  Multiplying numerator and
denominator by a common nonzero multihomogeneous factor pads any desired
common twist without changing the rational section or the pass/fail result.
It does not construct a Cramer matrix or target-consistent incidence.  These
examples show that no proof using only the multidegrees and one jet layer can
deduce the other layer; neither example is claimed to arise from a balanced
target incidence.

## 8. Replay independence and limitations

The primary verifier uses SymPy expressions and differentiation.  It checks:

- both universal quotient-clearing formulas;
- all ternary first and endpoint-Hessian stresses on one physical family;
- all nine reconstructed block entries;
- chart rescaling by a nonconstant factor;
- all twelve endpoint Hessians and the explicit multidegree in the transverse
  pole example;
- all three outside stresses and the explicit multidegree in the endpoint pole
  example; and
- the `3m+6` count through representative orders.

The audit imports neither repository code nor SymPy.  It implements:

- a sparse multivariate polynomial ring over `Fraction`;
- polynomial addition, multiplication, powers, derivatives, and evaluation;
- a separate exact two-jet algebra with multiplication and inversion;
- a separate physical block reconstruction;
- full first-/second-stress chart covariance; and
- every claimed pass-layer identity, multidegree, and monomial divisibility
  check for both pole examples.

The implementations share the displayed theorem identities because those
are the objects under review.  They do not share algebra code, polynomial
representation, quotient evaluation, or an imported helper.  This is useful
implementation independence, not an independent mathematical authorship
claim.

The scripts do not prove the constant-field theorem, normality, the
projective-cone correspondence, or arbitrary-order Euler homogeneity by
enumeration.  Those are written proof steps above and in the theorem.

## 9. Accepted consequence and residual boundary

The predecessor full-sensor gate may now replace every pair's infinite
prime-divisor test by explicit determinant-cleared first and second jets.
The resulting gate remains necessary and sufficient for same-graph
globalization:

```text
target residuals;
empty normalization;
finite pair differential flatness;
higher Euler--hafnian recurrences.
```

This is a meaningful theorem-producing advance because it makes pair
regularity directly accessible to symbolic elimination and named nonzero
stress certificates.  It is not itself a universal failure certificate.

The following remain open.

- Whether every target-consistent full sensor violates normalization, one
  pair stress, or one higher recurrence.
- Whether any target-consistent full sensor passes the whole gate.
- The all-balanced rank-drop branch.
- Universal extraction questions in other local restriction lanes.
- The global conjecture.

The global Krenn--Gu status therefore remains **UNRESOLVED**.

## Strongest fresh-referee objection

The strongest objection is that “zero Hessian implies linear” is false if
one forgets either characteristic zero or the prescribed multihomogeneous
degree.  A positive-characteristic `p`-th power has zero derivative, while a
degree-zero rational endpoint ratio can evade the affine conclusion one
would want.  The theorem does not forget these hypotheses: characteristic
zero is explicit, and the Cramer component's `O(1_e)` degree is imported
before any derivative argument.  The two Euler steps use that degree
load-bearingly.  Accordingly, the result must not be generalized to arbitrary
rational chart functions or positive characteristic without a new proof.
