# Balanced full-sensor Cramer pair-pole differential-flatness theorem

## Status

**Exact characteristic-zero refinement of the open balanced full-sensor
pair-pole gate.**  On one generically full balanced-sensor Cramer chart, let

```text
C_pq=v_pq/beta
```

be the unique rational component belonging to a nonroot pair `{p,q}`.  The
prime-divisor regularity test for `C_pq` is equivalent to a finite family of
determinant-cleared differential identities:

1. one first-order stress in every coordinate at every nonendpoint vertex;
2. one symmetric second-order stress in every pair of coordinates at `p`;
3. the analogous symmetric stresses at `q`.

For ternary local spaces this gives exactly

```text
3(m-2)+6+6 = 3m+6
```

polynomial identities per pair.  When they hold, the physical block is
reconstructed uniquely by

```text
(W_pq)_(a,b)=partial_(p,a) partial_(q,b) (v_pq/beta).
```

Thus the infinitely phrased valuation condition in the Cramer--Euler gate
can be replaced, without weakening or generic qualification, by finitely many
first- and second-jet identities in the Cramer numerator and denominator.
No factorization of `beta`, enumeration of its prime divisors, auxiliary
edge variables, or point sampling is required.

This theorem does **not** prove that a target-consistent full sensor fails a
jet identity, normalization, or an Euler--hafnian recurrence.  It does not
exclude the all-balanced rank-drop branch or construct a counterexample.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Cramer pair components on the affine cones

Use the hypotheses and notation of the
[`Cramer--Euler pair-pole gate`](BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md).
Work over a characteristic-zero field `K`; the Krenn--Gu application has
`K=C`.  Let the nonroot set be `N`, with `|N|=m`, and choose linear
coordinates

```text
z_u=(z_(u,0),...,z_(u,d_u-1))
```

on the affine cone of each `P(L_u)`.  In the ternary application every
`d_u=3`.

Fix one nonzero maximal-minor chart.  Its determinant is `beta`, its Cramer
numerator for the pair `e={p,q}` is `v_e`, and

```text
f_e=v_e/beta.                                         (1)
```

The bundle degrees imply that `f_e` is multihomogeneous of degree one in
`z_p` and `z_q` and degree zero in every `z_w`, `w notin e`.  This
homogeneity is part of the theorem: an arbitrary rational function without
these degrees is not a Cramer pair section.

For `w notin e` and a coordinate `a`, define the cleared transverse stress

```text
S_(w,a)(beta,v_e)
 = beta partial_(w,a) v_e
   -v_e partial_(w,a) beta.                           (2)
```

For one endpoint `r in {p,q}` and coordinates `a,b`, define the symmetric
cleared Hessian stress

```text
H^(r)_(a,b)(beta,v_e)
 = beta^2 partial_(r,a)partial_(r,b) v_e
   -beta(
       partial_(r,a)v_e partial_(r,b)beta
       +partial_(r,b)v_e partial_(r,a)beta
       +v_e partial_(r,a)partial_(r,b)beta)
   +2v_e partial_(r,a)beta partial_(r,b)beta.          (3)
```

Direct quotient differentiation gives the exact denominator powers

```text
S_(w,a)       = beta^2 partial_(w,a) f_e,
H^(r)_(a,b)   = beta^3 partial_(r,a)partial_(r,b) f_e. (4)
```

The powers `beta^2` and `beta^3` are essential.  Equations (2)--(3) are
polynomial identities even when the rational section has a pole.

## 2. Finite differential criterion for one physical pair

### Theorem 1 (pair-pole differential flatness)

For a Cramer pair component (1), the following conditions are equivalent.

1. `f_e` is the global section of `O(1_e)` defined by one constant physical
   bilinear block:

   ```text
   f_e(z_p,z_q)=z_p^T W_pq z_q                    (5)
   ```

   for a unique `W_pq in L_p^* tensor L_q^*`.

2. The prime-divisor inequalities from the pair-pole gate hold:

   ```text
   nu_P(v_e)>=nu_P(beta)                              (6)
   ```

   at every prime divisor `P` of `X=product_(u in N)P(L_u)`, in compatible
   local frames.

3. The following finite differential identities hold:

   ```text
   S_(w,a)=0       for every w notin {p,q} and every a;
   H^(p)_(a,b)=0   for every 0<=a<=b<d_p;
   H^(q)_(a,b)=0   for every 0<=a<=b<d_q.             (7)
   ```

4. There is a constant matrix `W_pq` for which the single polynomial
   identity

   ```text
   v_e=beta (z_p^T W_pq z_q)                          (8)
   ```

   holds.

For ternary local spaces, (7) contains `3(m-2)` transverse first derivatives
and two symmetric `3 x 3` Hessians, hence `3m+6` identities.

### Proof

Conditions 1 and 4 are equivalent after multiplying by the nonzero rational
function `beta`.  Either one immediately implies (7), because a constant
bilinear form is independent of every nonendpoint variable and is linear in
each endpoint.

Condition 2 says exactly that the rational section has no divisorial pole.
The product of projective spaces `X` is smooth and hence normal, so a rational
line-bundle section with no prime-divisor pole extends globally.  Since

```text
H^0(X,O(1_e))=L_p^* tensor L_q^*,                    (9)
```

the extension is one constant bilinear block.  Thus 2 implies 1, while a
global section plainly satisfies 2.

It remains to show that 3 implies 1 without using divisor factorization.
By (4), the transverse stresses say

```text
partial_(w,a) f_e=0
```

for every nonendpoint coordinate.  In characteristic zero the simultaneous
constant field of these coordinate derivations is `K(z_p,z_q)`.  Therefore
`f_e` depends rationally only on its two endpoint groups.

The first endpoint Hessian in (7) now says that every
`partial_(p,a)f_e` is independent of all `z_p` coordinates.  Euler's identity
for the degree-one `z_p` homogeneity gives

```text
f_e=sum_a z_(p,a) A_a(z_q),                           (10)
```

with `A_a in K(z_q)`.  Applying the `q`-Hessian identities to (10) and using
the algebraic independence of the `z_(p,a)` shows that every `A_a` has zero
Hessian in `z_q`.  Euler's identity for its degree-one `z_q` homogeneity then
gives

```text
A_a(z_q)=sum_b (W_pq)_(a,b) z_(q,b)                  (11)
```

with constants `(W_pq)_(a,b) in K`.  Equations (10)--(11) are (5).  The
coefficients are unique because the coordinate monomials
`z_(p,a)z_(q,b)` are linearly independent.  This proves all equivalences.

Characteristic zero is load-bearing because the constant field of coordinate
derivations is larger in positive characteristic and a zero Hessian need not
force an affine function there.  The two degree-one Euler identities
themselves do not require division by a nonunit integer.

## 3. Explicit reconstruction and chart independence

Under the equivalent conditions of Theorem 1,

```text
(W_pq)_(a,b)
 =partial_(p,a)partial_(q,b) f_e.                    (12)
```

For direct computation from Cramer data, define

```text
R_(a,b)(beta,v_e)
 = beta^2 partial_(p,a)partial_(q,b) v_e
   -beta(
       partial_(p,a)v_e partial_(q,b)beta
       +partial_(q,b)v_e partial_(p,a)beta
       +v_e partial_(p,a)partial_(q,b)beta)
   +2v_e partial_(p,a)beta partial_(q,b)beta.         (13)
```

Then

```text
R_(a,b)=beta^3 (W_pq)_(a,b).                         (14)
```

Thus one may reconstruct `W_pq` at any point of the chart where `beta!=0`;
Theorem 1 proves that the result is independent of that point.

Suppose a second Cramer chart gives `(beta',v'_e)`.  Target consistency and
generic injectivity give

```text
v_e/beta=v'_e/beta'                                  (15)
```

in the function field.  By (4), vanishing of (2)--(3) on either chart is
exactly vanishing of the first derivatives and endpoint Hessians of the same
rational section.  Hence the criterion and the reconstructed block are
chart-independent.  One nonzero Cramer chart is enough.

## 4. Finite-jet version of the full-sensor gate

### Theorem 2 (Cramer--Euler gate with no prime enumeration)

In Theorem 3 of the Cramer--Euler pair-pole gate, replace condition (17c) by
the finite identities (7) for every nonroot pair.  The resulting four-part
gate

```text
target residuals;
empty normalization;
pair differential flatness;
Euler--hafnian recurrences                              (16)
```

is again necessary and sufficient for same-graph globalization.

### Proof

Theorem 1 proves that pair differential flatness is equivalent to condition
(17c), including physical endpoint bilinearity.  Every other condition and
every implication in the Cramer--Euler globalization theorem is unchanged.

For ternary local spaces the pair-regularity portion of (16) has

```text
binomial(m,2)(3m+6)                                  (17)
```

displayed differential identities.  They are polynomial identities in the
shore parameters and cone coordinates after inserting
`v_e=adj(A)j`.  “Finite” here means a finite symbolic identity family; it
does not mean that evaluation at finitely many unproved sample points is a
certificate.

## 5. Ambient sharpness: both jet layers are needed from degrees alone

At the level of the multihomogeneous rational-section lemma used in Theorem
1, neither the transverse first-order layer nor the endpoint Hessian layer
follows from the other layer plus the prescribed degrees.  The examples below
are not shown to lie in the balanced Cramer image, so they do not prove that
either layer is independently sharp inside actual target incidences.

### Endpoint linearity does not remove transverse poles

Let `x,y` be the endpoint groups and let `r` be one outside group.  On their
affine cones take

```text
beta=r_1,
v=r_0 x_0 y_0,
f=(r_0/r_1)x_0y_0.                                  (18)
```

The rational section has the correct degrees: `(1,1)` at the endpoints and
degree zero at `r`.  Both endpoint Hessians vanish identically, but

```text
S_(r,0)=r_1 x_0 y_0 !=0,                             (19)
```

and `f` has a pole along `r_1=0`.

### Transverse constancy does not remove endpoint poles

With no outside dependence, take

```text
beta=x_1,
v=x_0^2 y_0,
f=(x_0^2/x_1)y_0.                                   (20)
```

Every transverse stress is vacuous or zero, and the section again has the
correct endpoint bidegree.  However

```text
H^(x)_(0,0)=2x_1^2 y_0 !=0,                         (21)
```

so the endpoint pole remains.

Multiplying both `beta` and `v` in either example by any common nonzero
multihomogeneous polynomial preserves the rational section and all pass/fail
outcomes.  This pads the common twist only; it does not construct a Cramer
matrix, target vector, or target-consistent incidence.  The examples are
therefore abstract rational-section controls, not balanced target incidences
and not Krenn--Gu counterexamples.

## 6. Proof-topology consequence and exact frontier

The open `S2` full-sensor branch now has the exact finite symbolic form

```text
one target-consistent full sensor
  -> unique Cramer numerators beta,v;
  -> empty normalization;
  -> first-order nonendpoint pair stresses;
  -> second-order endpoint pair stresses;
  -> one Euler--hafnian recurrence per higher even subset;
  -> same-graph extension iff every identity passes.                (22)
```

The advance is elimination-facing: it replaces all prime-divisor searches
and the existential matrices in (8) by explicit polynomial identities in
the Cramer data.  A future obstruction may now exhibit one named nonzero
stress without factoring a maximal minor.

No such universal nonzero stress is proved here.  The target residuals,
normalization, pair jets, and higher recurrences remain logically separate.
The all-balanced rank-drop branch is unchanged.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_pole_differential_flatness.py
python claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_pole_differential_flatness.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_pole_differential_flatness.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_pole_differential_flatness.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_pole_differential_flatness.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_pole_differential_flatness.py
```

The primary verifier uses SymPy to derive the cleared quotient formulas,
checks a nontrivial multihomogeneous physical family, reconstructs all nine
ternary edge-block entries, verifies chart rescaling, and retains both sharp
pole controls.  The independent no-import audit implements a separate sparse
multivariate polynomial ring over `Q` and rebuilds the same identities using
only the Python standard library.  These scripts verify displayed algebra
and conventions; the arbitrary-order implication is the differential-
algebra proof in Theorem 1.
