# Maximum-root surplus-two zero-anchor residual-family generic escape and coordinate-shore normal form

## Status

**Exact characteristic-zero arbitrary-root source-family reduction and sharp
physical boundary.**  Continue on the zero-anchor branch of `GLS26`, but now
retain the fully supported residual pair as a Laurent family rather than one
chosen contraction.  Exactly one of the following holds for every fixed
physical source graph, pair `Q`, and probe pair `A`:

1. a nonempty principal open of residual contractions fails the coordinate-
   shore cover and therefore enters the essential promoted-pair branch of
   `GLS26`; or
2. the cover holds over the residual function field, with one fixed colour-
   to-shore assignment on a nonempty principal open.  Its generic shore ranks
   are only `(1,2)`, `(2,1)`, or `(2,2)`, and each has an exact coordinate
   normal form.

The rank-drop and assignment-change fibres outside the selected open are not
discarded: the theorem uses the open only to produce one legal source
contraction.  If no essential-pair contraction exists anywhere, the generic
normal-form branch is mandatory.

An existing maximum-root, blocker-saturated, pure-normalized, Hamming-one-zero,
locally concise physical graph realizes the `(2,1)` normal form identically
on the residual torus with `h`, `p`, and `Pi_Q` nonzero.  Its displayed mixed
coefficient is nonzero, so it is not a witness.  Thus the complete mixed GHZ
equations are load-bearing for eliminating the normal forms.

This theorem does not promote the essential raw pair to legal target survival,
exclude any generic shore normal form on the witness locus, force a response
or common selector, or close the strategic node.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Dependencies

Use

- [`GLS4`](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md) for the same-pair source gates;
- [`GLS26`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_THEOREM.md) for the pointwise essential-pair/shore-cover alternative; and
- [`GLD11`](FOUR_ROOT_SIMULTANEOUS_SWALLOWED_PURE_NONZERO_RESPONSE_PHYSICAL_CONTROL_THEOREM.md) for the sharp physical control.

No external literature claim is used.

## 1. Residual Laurent family

Let `K` be an infinite characteristic-zero field and retain one fixed GLS4
source package

```text
Q={q_0,q_1},          A={a_0,a_1},
h=H_Q(z_0,z_1),       p=p_(A,Q)(z_0,z_1),
h!=0,                 p!=0,          Pi_Q!=0,
omega=W_(a_0,a_1)=0.                                  (1)
```

Here `h` and `p` are nonzero Laurent polynomials before choosing the fully
supported residual vectors, while `Pi_Q` is the fixed nonzero complementary-
permanent tensor.  Put

```text
Lambda=K[z_(q_s,c),z_(q_s,c)^-1:s=0,1 and c=0,1,2],
F=Frac Lambda.                                           (2)
```

For `i,s in {0,1}`, define

```text
xi_i^s(z_s)=W_(a_i,q_s)(-,z_s) in V_(a_i)^* tensor Lambda,
X_i^F=span_F{xi_i^0,xi_i^1},
d_i=dim_F X_i^F.                                        (3)
```

Because `p!=0`, `d_i in {1,2}`.  Let `e_(i,c)^*` be the colour-`c`
coordinate covector on the `i`th probe shore.

Call the **generic coordinate-shore cover** the condition

```text
for every c in {0,1,2},
 e_(0,c)^* in X_0^F or e_(1,c)^* in X_1^F.             (4)
```

This is a function-field membership statement.  It does not mean that one
chosen `3 x 3` determinant vanishes across every rank-drop fibre.

## 2. Generic escape or fixed cover

### Theorem 1 (residual-family dichotomy)

Exactly one of the following holds.

#### E. Generic escape

Condition (4) fails.  There is a colour `c` and a nonzero Laurent polynomial
`Delta` such that every residual point of

```text
D(h p Delta)                                            (5)
```

has

```text
e_(0,c)^* notin span_K{xi_0^0(z_0),xi_0^1(z_1)},
e_(1,c)^* notin span_K{xi_1^0(z_0),xi_1^1(z_1)}.       (6)
```

Hence the pointwise shore cover fails throughout (5), and `GLS26` forces an
essential nonzero promoted pair slice at every such point.

#### C. Generic fixed cover

Condition (4) holds.  There is a map

```text
sigma:{0,1,2}->{0,1}                                   (7)
```

and a nonzero Laurent polynomial `Delta_sigma` such that on
`D(h p Delta_sigma)` the shore ranks equal `(d_0,d_1)` and

```text
e_(sigma(c),c)^* in
 span_K{xi_(sigma(c))^0(z_0),xi_(sigma(c))^1(z_1)}
 for c=0,1,2.                                          (8)
```

The same assignment works at every point of that principal open.

#### Proof

Choose, for each shore, a nonzero `d_i`-minor of its `3 x 2` incidence
matrix over `F`.  After clearing denominators, their product is a nonzero
Laurent polynomial and fixes both ranks on a principal open.

If (4) fails, choose a colour absent from both generic spans.  Then adjoining
that coordinate column raises both generic ranks.  Choose one nonzero
`(d_i+1)`-minor on each shore and include their cleared numerators in
`Delta`.  On (5), both rank rises persist, giving (6).

If (4) holds, choose one valid shore for each of the three colours.  Over `F`,
each chosen coordinate column is a rational combination of a fixed generic
basis of that shore.  Clear the basis minors and all coefficient denominators.
On the resulting principal open, the same combinations prove (8).

All polynomials multiplied into `Delta` are nonzero in the Laurent domain.
An infinite field has a torus point outside the zero set of their product,
so both declared opens are nonempty.  No exceptional minor is divided out in
a universal identity; an open point is chosen because the source theorem
requires one contraction.  `square`

### Corollary 1.1 (universal pointwise failure implication)

If every point of `D(hp)` lies in the GLS26 coordinate-shore-cover branch,
then branch C holds.  Therefore any proposed universal attachment failure
must include one of the generic normal forms below; isolated rank-drop cover
points cannot by themselves obstruct choosing an essential-pair contraction.

## 3. Exact generic normal forms

### Theorem 2 (coordinate-shore normal forms)

Assume branch C.  After possibly exchanging the two probe roots and
permuting the three colours, exactly one of the following holds over `F`.

#### C12. One-by-two cross-axis form

```text
(d_0,d_1)=(1,2),
X_0^F=F e_(0,0)^*,
X_1^F=F e_(1,1)^*+F e_(1,2)^*.                       (9)
```

The all-port tensor has the form

```text
0!=q=e_(0,0)^* tensor v,
v in F e_(1,1)^*+F e_(1,2)^*.                        (10)
```

It has matrix rank one and every diagonal entry is zero.

The transpose profile `(2,1)` is obtained by exchanging the shores.

#### C22. Plane-and-covered-plane form

```text
(d_0,d_1)=(2,2),
X_1^F=F e_(1,1)^*+F e_(1,2)^*,
X_0^F=F e_(0,0)^*+F v_0,
0!=v_0 in F e_(0,1)^*+F e_(0,2)^*.                   (11)
```

The tensor `q` has matrix rank two, left shore span `X_0^F`, and right shore
span `X_1^F`.  In particular its colour-zero column is zero.  If both shores
are coordinate planes, their missing colours are distinct.

No fourth generic rank profile occurs.

#### Proof

By GLS26's low-rank shore boundary, a cover forces `d_0+d_1>=3`, leaving
`(1,2)`, `(2,1)`, and `(2,2)`.

For `(1,2)`, the rank-one shore can contain at most one coordinate line and
the rank-two shore at most two.  Covering all three uses these capacities
without overlap.  A colour permutation gives (9).  The two residual
covectors on shore zero are proportional to `e_(0,0)^*`; substituting in

```text
q=xi_0^0 tensor xi_1^1+xi_0^1 tensor xi_1^0           (12)
```

gives (10).  Nonzero `p` makes its right factor nonzero.  The supports in
(9) are disjoint in colour, proving diagonal vanishing.

For `(2,2)`, at least one shore must contain two coordinate lines.  Exchange
the shores and permute colours so that it is the coordinate plane in (11).
The other shore must contain the missing colour-zero line; subtracting its
colour-zero component from a second basis vector gives the displayed `v_0`.
Both pairs `xi_i^0,xi_i^1` are bases.  In those bases (12) has coefficient
matrix `[[0,1],[1,0]]`, which is invertible.  Hence `q` has rank two and its
left and right spans are exactly the two shore spaces.  The zero column and
the final coordinate-plane assertion follow.  `square`

These are projective shore-space normal forms.  They do not normalize the
nonzero entries of `q`, the physical edge blocks, or the residual vectors.

## 4. Maximum-root sharpness control

### Theorem 3 (the generic cover is physically realizable off the witness locus)

The exact GLD11 four-root graph, with

```text
Q={q_0,q_1},       A={r_0,r_2},                       (13)
```

has, for every fully supported residual pair,

```text
X_0=span{e_0^*,e_2^*},        X_1=K e_1^*,
q=z_(q_0,0)z_(q_1,1) e_0^* tensor e_1^*,
p=z_(q_0,0)z_(q_1,1),
h=z_(q_0,0)z_(q_1,0).                                 (14)
```

Thus it realizes the transpose of C12 identically on the residual torus.
Moreover `Pi_Q!=0`: its all-colour-one coefficient contains the injection

```text
r_0-u_0,       r_1-u_3,       r_2-u_1,       r_3-u_2. (15)
```

The same graph has maximum root set `R`, rank-three blockers at all six
outside modes, pure coefficients one, zero Hamming-one shell, local
concision, all seven fixed-`Q` responses nonzero, and all seven active pure
target classes swallowed.  It is not a witness: the mixed word

```text
1200100020                                             (16)
```

has coefficient one.

#### Proof

Read the `q_0,q_1` columns of the GLD11 root-incidence table at rows `r_0`
and `r_2`.  They are respectively `(e_0^*,e_2^*)` and `(0,e_1^*)`, giving
(14) by (12).  The residual-pair edge has colour zero, giving `h`; all torus
coordinates displayed in (14) are units.  Matching (15) proves the stated
nonzero coefficient of `Pi_Q`.  Every remaining property and the unique
mixed matching for (16) are the exact proved GLD11 statements.  `square`

The control proves that maximum-root incidence, `h,p,Pi_Q` supply, pure
normalization, Hamming-one equations, local concision, response nonvanishing,
and the generic shore cover do not exclude branch C.  The complete mixed
equations beyond that boundary must be used.

## 5. Frontier

```text
residual-family generic escape / fixed-cover dichotomy: PROVED;
one principal open keeps h,p and generic ranks:         PROVED;
generic shore profiles C12/C21/C22:                     PROVED;
rank-drop and assignment-change fibres as source escape: INCLUDED;
maximum-root C21 sharp physical control:                PROVED;

essential raw pair survives complete target nuisance:   PARTIAL (GLS28);
C12/C21/C22 excluded on the complete witness locus:     NOT PROVED;
nonzero response, synchronization, and activity:        NOT PROVED;
arbitrary-r downstream promoted detector:               OPEN;
complete maximum-root supply/attachment node:           OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.       (17)
```

`GLS28` proves that an essential supplier outside its complete foreign-
supplier envelope gives a legal row, while a projected diagonal direction
outside that envelope gives the legal nonzero-response row.  Universal useful-
row failure is thereby confined to a deletion-stable diagonal cover.  It does
not force either positive locus or exclude the redundant cover.  On C, use the
complete mixed equations on the three normal forms, starting with the one-by-
two cross-axis form; the GLD11 control shows why pure and Hamming-one
coefficients alone cannot do this.

## Verification boundary

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_family_generic_escape_and_coordinate_shore_normal_form.py
```

The primary verifier checks rational-function rank stability, fixed cover and
escape fixtures, all three normal forms, and the GLD11 shore/source data.  The
independent no-import audit uses `Fraction`, separate elimination, a different
function-field specialization argument, and an independent matching replay
of the sharp control.  Finite scripts audit the mechanisms; the Laurent-open
and arbitrary-root statements are the written proof.

See the
[`2026-08-20 hostile review`](../../docs/audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_FAMILY_GENERIC_ESCAPE_AND_COORDINATE_SHORE_NORMAL_FORM_REVIEW_2026-08-20.md).
