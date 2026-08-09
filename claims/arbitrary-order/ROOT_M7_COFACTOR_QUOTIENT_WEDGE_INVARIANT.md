# Root `m=7` cofactor quotient-wedge invariant

## Status

This note extracts the first genuinely coloured elimination invariant from
the four-root hidden-pair equation.  Each active deletion sector forces a
rank-one condition on two complementary blocker cofactors after quotienting
by the binary diagonal plane.  Equivalently, every `2 x 2` coloured
coefficient minor vanishes.

The invariant is quadratic, complete for eliminating the hidden scalar
forms in one sector, and minimal: there is no nonzero universal linear
equation on the cofactor pair.  Since at least two of the five sectors are
active, five explicit degree-eight products vanish without having to name
the active sectors.

This does not yet contradict the `P_7` coefficient table.  The missing
input is an independent lower-jet or incidence theorem forcing a selected
minor to be nonzero in enough sectors.

## Quotient equation

Use the notation of the four-root hidden-pair theorem.  For each root
`k`, put

```text
C_k=C_(R-{r_k}),
E_k=C_((R-{r_k}) union Q),
D_01=span{D_0,D_1},
bar W=(blocker tensor space)/D_01.                    (1)
```

Under the projectively constant root--blocker tangent hypothesis, the
four-root derivative gives

```text
h_k tensor bar(C_k)+q_k tensor bar(E_k)=0.            (2)
```

Call sector `k` **active** when `(h_k,q_k)!=(0,0)`.  Equation (2) implies

```text
bar(C_k) wedge bar(E_k)=0.                            (3)
```

Indeed, if `h_k,q_k` are independent, both quotient cofactors vanish.  If
they span one dimension, (2) makes the cofactors proportional.  The cases
with exactly one scalar form nonzero are included.

## Coloured coefficient minors

Every word coordinate other than `0^7` and `1^7` descends to `bar W`.
For any two such words `w,w'`, define

```text
Delta_k(w,w')
 =[w]C_k [w']E_k-[w']C_k [w]E_k.                    (4)
```

Then every active sector satisfies

```text
Delta_k(w,w')=0.                                     (5)
```

Useful legal choices include the mixed word `w=0000102` and the third
diagonal word `w'=2222222`: although `2^7` is diagonal in the full ternary
space, it is a valid quotient coordinate because only `D_0,D_1` are
removed in (1).

Equation (4) retains the colour grading and relative cofactor information.
A single scalar contraction of the blocker tensor space necessarily
annihilates this wedge invariant because `exterior^2 K=0`; it also discards
other information.  Several coordinated contractions can recover the
minor.

## Complete hidden-form elimination in one sector

Choose any basis of `bar W` and write the two quotient cofactors as rows of
a `2 x N` matrix

```text
M_k=[bar(C_k); bar(E_k)].                             (6)
```

There exists a nonzero scalar-form pair `(h,q)` satisfying

```text
h tensor bar(C_k)+q tensor bar(E_k)=0                (7)
```

if and only if `rank M_k<=1`.  Therefore the full elimination ideal in the
visible cofactor coordinates is exactly the determinantal ideal generated
by all minors (4).

This completeness statement eliminates unrestricted hidden scalar forms
from the abstract tensor equation (7).  It does not eliminate the actual
common root-edge parametrization of `h_k,q_k`; hafnian realizability can
impose additional visible equations across sectors.

This is minimal in degree.  The rank-at-most-one variety contains every
matrix unit, and the matrix units span the full `2 x N` ambient space.
Hence a linear form vanishing on the variety is zero.  Quadratic two-word
minors are the first possible universal equations.

## Removing the unknown active-sector labels

The all-root frame theorem proves that at least two `h_k` sectors are
endpoint-active, hence at least two hidden pairs in (2) are active.  Fix
`w,w'` and abbreviate `Delta_k=Delta_k(w,w')`.  At least two of the five
numbers `Delta_k` vanish.  Consequently, for every four-subset
`K subset {0,1,2,3,4}`,

```text
product_(k in K) Delta_k=0.                           (8)
```

These are five explicit degree-eight coloured equations.  The arity four
is sharp from the active-count statement alone: a formal model with
exactly two active sectors may have all three inactive minors nonzero, so
the product on those three sectors need not vanish.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_root_m7_cofactor_quotient_wedge_invariant.py
python claims/arbitrary-order/audit_root_m7_cofactor_quotient_wedge_invariant.py
```

The scripts check the determinantal parametrization, the affine-chart
converse, linear minimality through matrix units, and the five active-label
free products.  They are fixed-size symbolic linear algebra, not a support
or word search.

## Boundary

```text
one active sector:                         ALL QUOTIENT 2x2 MINORS ZERO;
abstract hidden-form elimination ideal:   RANK-ONE DETERMINANTAL IDEAL;
common-edge/hafnian elimination ideal:    MAY BE STRICTER;
nonzero linear visible invariant:         NONE;
active sectors among five:                AT LEAST TWO;
active-label-free consequence:            FIVE DEGREE-EIGHT PRODUCTS;
forced nonzero P_7 minor:                 UNKNOWN;
global Krenn--Gu conjecture:               UNRESOLVED.
```
