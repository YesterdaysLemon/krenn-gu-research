# Hostile review of the active-support-five equality exclusion

## Verdict and scope

**PASS, for the stated pair-level, active-support-five, characteristic-not-two
scope.**  No mathematical, quantifier, case-exhaustiveness, field, or
implementation blocker survived hostile review.

For three-planes `U,V subset (Z_5)_1` whose union uses every coordinate, the
package proves

```text
dim(UV)=5
  => U=V=Kx_i direct-sum W,  dim W=2,  dim(W^2)=3.
```

Conversely, every plane of this form has square dimension five, and it has
active support five exactly when `W` uses all four coordinates other than
`i`.  The multiplication-dual rank-one locus is contained in one fixed
two-plane of factors, so none of these equality pairs is Delta-admissible at
the pair level.

This is not a full six-mode nonrestriction theorem.  It does not classify
active-support-four pairs, does not itself treat support at least six, and
does not prove that a putative full restriction has an equality-five omitted
pair.  Unrestricted `P_6 -> Delta_3` remains unknown, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_ACTIVE_SUPPORT_FIVE_EQUALITY_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_active_support_five_equality_exclusion.py
  audit_arbitrary_permanent_active_support_five_equality_exclusion.py
```

No theorem or verifier edit was required.

## 1. Annihilator and diagonal-rank dictionary

Let `E=K^5` and let

```text
S(U,V)={Q in Sym^2(E^*): Q(U,V)=0}.
```

The dual of the square-free quadratic space is the space of symmetric
zero-diagonal forms on `E`.  Therefore the ordinary annihilator of `UV` is
exactly `S(U,V) intersect ker(diag)`.  Since `(Z_5)_2` has dimension ten,
the equality hypothesis is equivalent to

```text
dim ker(diag|S(U,V))=5.
```

This identification uses `2!=0` when passing between edge coefficients and
symmetric matrices.  The theorem's exclusion of characteristic two is thus
necessary and explicit.

Because two three-planes in a five-space meet in dimension at least one,
the intersection dimension `r` is exactly one of `1,2,3`.  The written case
split is exhaustive.

## 2. Why intersection dimension one is impossible

For `r=1`, write

```text
E=R direct-sum A direct-sum C,
U=R direct-sum A,
V=R direct-sum C,
dim A=dim C=2.
```

Symmetry and `Q(U,V)=0` make `R` radical and kill the `A x C` block.  Hence

```text
S(U,V)=Sym^2(A^*) direct-sum Sym^2(C^*),  dim S=6.
```

Equality five would force the diagonal map on this six-space to have rank
one.  But the coordinate vectors span `E`, so their projections to `A` span
`A`.  Two nonproportional projected vectors have linearly independent
symmetric squares.  Projecting the transpose image of `diag` to
`Sym^2(A)` therefore already gives rank at least two.  This contradiction
does not use algebraic closure, infinitude, or a generic point.

## 3. Why intersection dimension two violates active support

For `r=2`, the sum `H=U+V` is a hyperplane `ker(c)`.  Covectors `alpha,beta`
may be chosen so that

```text
U intersect V=ker(c) intersect ker(alpha) intersect ker(beta),
alpha|V=0,  beta|U=0.
```

A direct block calculation gives the internal direct sum

```text
S(U,V)=(c symmetric-tensor E^*)
       direct-sum K alpha^2 direct-sum K beta^2,
dim S=7.
```

The first summand has diagonal image exactly the coordinate subspace on
`supp(c)`: its diagonal is `(2c_j ell_j)_j`, and the values of `ell` are
arbitrary.  Equality five makes the full diagonal rank two, hence
`|supp(c)|<=2`.

Support one would make `H` a coordinate hyperplane omitted by both planes,
contradicting active support.  At support two, the first summand already
fills the entire allowed diagonal image.  Thus the square diagonals of
`alpha` and `beta` vanish on each of the other three coordinate axes.
Over a field this forces both covectors themselves to vanish there.  Those
three independent axes then lie in the two-space
`ker(c,alpha,beta)=U intersect V`, which is impossible.  This closes every
`r=2` configuration, not merely the representative replayed by the primary
checker.

Consequently an active equality-five pair has `r=3`, so `U=V`.

## 4. The unique symmetric relation forces a coordinate axis

The symmetric multiplication map on the common plane has six-dimensional
domain and five-dimensional image.  Its kernel is therefore one line
`KQ subset Sym^2(U)`.  For the five nonzero coordinate restrictions
`ell_j=x_j|U`, the vanishing of every square-free edge coefficient is

```text
Q(ell_i,ell_j)=0,  i!=j.
```

The `ell_j` span `U^*`.

- Rank three is impossible: three coordinate restrictions forming a basis
  would be an orthogonal basis for a nondegenerate form, and every fourth
  restriction, being orthogonal to that basis, would be zero.
- Rank two is impossible: choose two restrictions whose images form a basis
  modulo the radical.  They are orthogonal and anisotropic, while each of
  the other three restrictions lies in the radical.  In the resulting
  basis, the two independent tensors `diag(1,0,0)` and `diag(0,1,0)` both
  satisfy every off-diagonal edge equation.  The multiplication kernel
  would have dimension at least two, contradicting uniqueness.

Thus `Q` has rank one, say `Q=w^2`.  Its vanishing square-free square says
`w_iw_j=0` for every `i!=j`; since `2!=0`, `w` is a coordinate vector.
After permutation and basis adjustment,

```text
U=Kx_0 direct-sum W,
W subset span{x_1,x_2,x_3,x_4}.
```

The edge supports give a genuine direct sum

```text
U^2=x_0W direct-sum W^2.
```

Multiplication by `x_0` is injective on `W`, so the first summand has
dimension two.  This proves both `dim(W^2)=3` and the converse.  Once
`U=V`, active support is exactly the requirement that `W` use the four
remaining coordinates.

## 5. Rank-one-factor obstruction

In a basis beginning with the coordinate-axis vector, the ordered
multiplication kernel is

```text
Alt^2(U) direct-sum K(x_0 tensor x_0).
```

Its annihilator is therefore exactly

```text
L={A in Sym_3(K): A_00=0}.
```

A nonzero rank-one member of a symmetric matrix space has proportional
left and right factors, so it is `c lambda lambda^T`.  The zero `(0,0)`
entry gives `c lambda(x_0)^2=0`, hence `lambda(x_0)=0`.  All left and right
factors in the entire rank-one locus lie in the same two-plane annihilating
`x_0`.  No three of them can span either copy of `U^*`, so the invariant
rank-one criterion excludes pair-level Delta admissibility.

This argument handles every classified pair and does not infer
nonadmissibility from the single displayed example.

## 6. Computational replay and independence

The primary verifier uses exact SymPy linear algebra.  It replays the
`r=1,2` annihilator dimensions and diagonal ranks, the rank-three and
rank-two relation obstructions, the rational active-support-five example,
the split product ranks, and the multiplication-dual factor obstruction.

The independent audit imports neither the primary verifier nor SymPy.  It
constructs all 1,210 RREF representatives of `Gr(3,5)(F_3)`, checks all
1,464,100 ordered pairs with a custom modular row reducer, reconstructs the
dual rank-one locus, and verifies the coordinate-axis normal form directly.
It found

```text
full-union-support ordered pairs: 1,456,110;
equality-five ordered pairs:             340;
off-diagonal equality-five pairs:          0;
projective rank-one points per pair:        4.
```

Every one of the 340 equality planes contains exactly one coordinate axis,
has a complementary `W` with `dim(W^2)=3`, and fails the independent-factor
criterion.  The equality-plane census hash reproduced as

```text
971fbb787f554b9d12d844dc5551aafdeb49a3d1bfaba1ba36a2ee4c98e25901.
```

This is meaningfully independent finite-field audit evidence.  It is not
used to promote a finite census into the characteristic-not-two theorem;
Sections 2--5 of the theorem supply that proof.

Focused replay passed:

```text
primary exact verifier:       PASS;
independent no-import audit:  PASS;
py_compile:                   PASS;
Ruff:                         PASS.
```

## 7. Accepted boundary

```text
active-support-five equality-five pairs:                 CLASSIFIED;
such a pair with U!=V:                                   NONE;
normal form Kx_i direct-sum W with dim(W^2)=3:           PROVED;
pair-level Delta-admissible active-support-five pair:    NONE;
active-support-four classification:                      NOT CHANGED;
support at least six:                                    NOT ADDRESSED HERE;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Final reviewed hashes

```text
theorem:
DE7FA0633E0D79796A5F76528F7B79BC99655F3F0F549133DF4651B71F6E83D2

primary verifier:
998EADDE4D7F268524B2DA6C612BECCAC29D3EBDB8D24E8B1E9216EE4977376B

independent audit:
757572A83973A8D9D26DC3B75CD97C7344EFE89DFEA1F77BB9A82D0784F0400B
```
