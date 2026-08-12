# Hostile review of the Cramer pair projective-minimal jet gate

## Verdict and exact scope

This review accepts
[`BALANCED_FULL_SENSOR_CRAMER_PAIR_PROJECTIVE_MINIMAL_JET_GATE_THEOREM.md`](../../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_PROJECTIVE_MINIMAL_JET_GATE_THEOREM.md)
as an exact compression of the already proved full-sensor pair differential-
flatness gate.

For one fixed projective pivot in each variable group, the accepted new fact
is

```text
all cone first/Hessian stresses vanish
iff
only the nonpivot first/Hessian stresses vanish.     (1)
```

The reverse implication uses the Euler syzygies of a degree-zero outside
function and a degree-one endpoint function.  In uniform local dimension
`d`, the pair layer therefore has `(d-1)(m+d-2)` identities; in ternary
dimension it has `2m+2`, rather than `3m+6`.

The result does not prove that one of the retained identities fails on a
balanced target incidence.  It does not strengthen target consistency,
normalization, or the higher Euler--hafnian gate, and it does not touch the
all-balanced rank-drop branch.  Global Krenn--Gu status remains
**UNRESOLVED**.

The coordinate controls establish irredundancy only for the fixed-chart
coordinate list in the ambient multihomogeneous rational-section lemma.  They
are not balanced complete-deck sensors with the GHZ target and do not prove
minimality among arbitrary encodings of the actual target-incidence image.

A fresh read-only hostile pass from the disjoint Lumen lane pinned exact S2L
head `4a237b25ef694208e15df654bdf6d472131210c6` and theorem SHA-256
`9f5f864c3f8402093708cc644edcd2c51e5e901d455ad7dd80cb4c90b5206266`.
It found no P0--P2 or blocking P3 defect.  It independently replayed all eight
structured `k=4,m=3` controls, their deck-complement multidegrees, pure-GHZ
selected-row pattern, Cramer solutions, and intended retained-jet failures.
It also accepted the explicit boundary: no matching-sum sensor realization,
unselected/full-row consistency, or empty normalization is supplied.

## 1. Imported obligations

Two verified predecessors remain load-bearing.

- The pair-pole differential-flatness theorem proves, in characteristic
  zero, that all outside first stresses and both full endpoint Hessians vanish
  exactly when the pair component is one global physical bilinear block.
- The pair-jet replacement-minor theorem identifies every such cleared jet
  with one selected-column replacement determinant and, only after full
  target consistency and function-field column rank `k`, with a full-row
  target-column-span condition.

The new theorem does not re-prove these statements.  Its new proof is the
equivalence between their full jet family and a smaller coordinate subfamily.

## 2. Outside Euler relation

For an outside group `w`, the pair component `f=v/beta` has degree zero.
Euler's identity gives

```text
sum_a z_a partial_a f=0.
```

Since `S_a=beta^2 partial_a f`, this is the exact polynomial relation

```text
sum_a z_a S_a=0.                                    (2)
```

If all nonpivot `S_a`, `a>0`, vanish, (2) gives `z_0 S_0=0`.  The working
cone ring is a polynomial ring over the relevant coefficient/function field,
so it is a domain and `z_0` is nonzero.  Hence `S_0=0` as an identity.  This
is not an inference from pointwise vanishing on one affine chart and does not
leave an unchecked component on `z_0=0`.

The direct numerator calculation

```text
sum_a z_a(beta partial_a v-v partial_a beta)
 =beta(deg(v)-deg(beta))v=0
```

confirms that no denominator or localization hypothesis is missing.

## 3. Endpoint differentiated Euler relation

At an endpoint, `f` has degree one.  Differentiating Euler's identity in
coordinate `b` gives

```text
sum_a z_a partial_a partial_b f=0.                   (3)
```

Multiplication by `beta^3` gives

```text
sum_a z_a H_(a,b)=0.                                (4)
```

Suppose only the symmetric nonpivot block `H_(a,b)`, `a,b>0`, is known to
vanish.  For `b>0`, (4) leaves `z_0 H_(0,b)=0`, so every mixed radial entry
vanishes.  Hessian symmetry then supplies `H_(a,0)=0`; using (4) with `b=0`
leaves `z_0 H_(0,0)=0`.  Thus the entire Hessian vanishes.

The order is load-bearing.  One may not infer `H_(0,0)=0` before obtaining
the mixed entries, and one must use symmetry of commuting coordinate
derivations.  The theorem follows this order explicitly.

## 4. Characteristic statement

The new radial compression itself is characteristic-free.  Euler degrees
are zero and one, the differentiated endpoint coefficient is `1-1=0`, and
the proof cancels the nonzero coordinate `z_0` in a domain rather than
dividing by an integer.

Characteristic zero remains necessary for the imported conclusion that the
full differential-flatness family forces a constant physical block.  In
positive characteristic, coordinate derivations have a larger constant
field and zero Hessian need not imply affine linearity.  The theorem keeps
these two layers separate.

## 5. Counts and reconstruction scope

At an outside group of dimension `d_w`, exactly `d_w-1` nonpivot first
stresses remain.  At an endpoint of dimension `d_r`, a symmetric Hessian on
`d_r-1` coordinates has

```text
(d_r-1)d_r/2=binomial(d_r,2)
```

entries.  Therefore one pair requires

```text
sum_(w notin e)(d_w-1)
 +binomial(d_p,2)+binomial(d_q,2).                   (5)
```

For uniform `d`, this is `(d-1)(m+d-2)`.  At `d=3`, it is
`2(m-2)+3+3=2m+2`; the predecessor count was
`3(m-2)+6+6=3m+6`, so the saving is `m+4` per pair.

The nine mixed endpoint derivatives reconstructing a ternary physical block
are outputs after flatness, not vanishing conditions.  They are correctly
excluded from both the old and new gate counts.

## 6. Target-column and chart scope

The retained stress coordinates inherit the predecessor's exact forms

```text
det(A[e <- q])=0
```

and, under full target consistency and full column rank,

```text
Q in span Gamma_hat(e).
```

Even before target consistency, the selected-row replacement determinants
inherit the Euler relations exactly:

```text
sum_a z_(w,a) det(A[e <- q_(w,a)])=0,

sum_a z_(r,a) det(A[e <- q_((r,a),(r,b))])=0.
```

These follow from the unconditional selected-system transport theorem, not
from the full-row span interpretation.  They make the radial redundancy
visible directly in the raw target/sensor derivatives.

The new theorem does not claim a span equivalence from the tautological
selected equation `Av=beta j`.  Full target residuals must still vanish.
Likewise, the projective pivot chart and the Cramer row-minor chart are
different choices and are not conflated.

Changing the Cramer chart rescales first and second cleared stresses by
`g^2` and `g^3`.  Changing the projective pivot merely chooses another
coordinate subfamily.  Either change preserves vanishing because every
reduced family is equivalent to the intrinsic full gradient/Hessian family.

## 7. Coordinatewise sharpness and forbidden inference

For each outside nonpivot coordinate, the theorem uses

```text
f=(r_a/r_0)x_0y_0.
```

Exactly that retained outside derivative is nonzero; all other retained
outside directions and both endpoint Hessians vanish.  For each symmetric
endpoint pair `(a,b)`, it uses

```text
f=(x_a^2/x_0)y_0       or       f=(x_a x_b/x_0)y_0.
```

Exactly the selected retained endpoint Hessian entry is nonzero; all other
retained entries, the other endpoint Hessian, and every outside derivative
vanish.  Swapping endpoints completes the ternary list.

These functions have the required degrees and can be put into an abstract
diagonal `2 x 2` Cramer system.  That does not construct the prescribed
balanced sensor matrix, GHZ target rows, or target consistency.  The examples
therefore forbid dropping a retained coordinate using multidegrees alone;
they say nothing about which coordinates might be forced by the special
balanced target-incidence image.

The theorem also gives a stronger `m=3` embedding for every control.  Each
embedding is a full `4 x 4` selected Cramer minor whose four columns have the
exact complement degrees of the even deck labels.  Its selected target vector
is zero except for one pure monomial `x_a y_a r_a`, as required by a selected
GHZ row pattern.  Exact Cramer multiplication gives the same outside or
endpoint pole coordinate, and its named retained replacement minor is
nonzero.

This hardening rules out an easier objection to the diagonal controls: the
failure persists after imposing the complete deck-column count, all column
multidegrees, and the selected GHZ zero/pure pattern.  It still does not
realize the columns by the balanced matching-sum formula, retain every target
row, prove full target consistency, or impose empty normalization in the
controls.  It therefore remains a selected-system boundary rather than a
balanced target incidence.

## 8. Replay coverage and independence

The primary verifier uses SymPy and checks:

- nonzero exact outside and endpoint jets satisfying every Euler syzygy;
- the full recovery from all ten retained to all eighteen cone stresses on a
  four-group ternary physical family;
- all two outside and six endpoint retained replacement minors, together
  with all seven replacement-minor Euler syzygies, on an abstract nonconstant
  Cramer system;
- every retained chart-rescaling identity;
- both outside coordinates and all six endpoint Hessian coordinates as
  independent ambient controls;
- a structured four-column, deck-degree and selected-GHZ compatible Cramer
  embedding for every one of those eight controls; and
- the uniform-d formula and ternary counts.

The independent audit imports neither SymPy nor repository code.  It builds
a separate sparse polynomial ring over `Fraction`, formal derivatives, and
different homogeneous data.  It independently checks the radial syzygies,
physical family, diagonal replacement entries, covariance, all eight sharp
controls, all eight structured selected systems, and counts.

The implementations are independent exact specialized replays, not
independent authors of the arbitrary-dimension proof.  The written Euler and
domain argument proves the universal statement.

## Strongest fresh-referee objection

The strongest plausible objection is that checking derivatives only on the
affine chart `z_0!=0` could miss a pole or nonlinear residue supported on the
hyperplane `z_0=0`.  That objection would be valid for finite point testing.
It does not apply here: the retained stresses vanish as rational or
polynomial identities, and the global Euler syzygies give
`z_0 times omitted_stress=0` in a domain.  Cancellation proves the omitted
stress itself is the zero identity before any geometric specialization.

The remaining obstruction is therefore not an exceptional chart boundary.
It is the same target-specific `S2` problem in a smaller exact coordinate
system: force one of the `2m+2` retained pair minors, normalization, or a
higher recurrence to fail.  No such universal failure is proved here.
