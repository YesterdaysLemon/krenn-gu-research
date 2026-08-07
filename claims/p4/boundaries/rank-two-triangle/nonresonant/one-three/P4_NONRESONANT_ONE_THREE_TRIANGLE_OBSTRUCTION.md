# Full-support `1+3` triangles collapse to the embedded `P_3` boundary

## Status

This is an exact characteristic-zero obstruction on the unresolved
all-rank-two-relation triangle from
[`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](../../../../classifications/rank-two-triangle/nonresonant/cut-reduction/P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
It is a symbolic support-and-pairing proof; no component search or
elimination is used.

Let

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Suppose three local planes

```text
U_i=span(y_i,x_i),                 i=1,2,3,
```

occur in a nonzero pure `P_4` restriction, all three pair images
`U_iU_j` have dimension three, all three unique pair relations have
coefficient-matrix rank two, and the triangle holonomy is
nonresonant.  After the Borel shifts from the preceding theorem, write

```text
b_ij y_i x_j+c_ij x_i y_j=0,       b_ij c_ij != 0,                 (1)
```

and put

```text
Q_ij=b_ij y_i x_j=-c_ij x_i y_j.                                  (2)
```

The preceding theorem proves

```text
U_k=Ann_R1(Q_ij)                  for {i,j,k}={1,2,3}.              (3)
```

Assume now that every `Q_ij` is a full-support `1+3` cut: for a
singleton coordinate `s_k`, its three coefficients on the triangle
complementary to `s_k` are all nonzero.

Then no such rank-three triangle exists.

More precisely, compatibility forces

```text
s_1=s_2=s_3=s,                                                       (4)
```

and all three planes into the same coordinate hyperplane `H_s`.
The `P_4` restriction consequently suspends a nonzero pure `P_3`
restriction.  Perfect pairing in the three-variable squarefree algebra
then forces

```text
dim(U_iU_j)<=2,                                                       (5)
```

contradicting the assumed value three.  The forced rank-drop closure is
exactly the geometric source of the already certified embedded-`P_3`
component, whose complete marked `H31` fibre is empty.

Thus the full-support, all-`1+3`, nonresonant cyclic-cut case creates no
tenth pure-`P_4` component.

This theorem does **not** handle the resonant divisor where the
projective holonomy is trivial.  It therefore advances, but does not
finish, component exhaustiveness or the global Krenn--Gu problem.

Triangles containing a full-support `2+2` bridge are now excluded by
the companion anchor/crossed-graph theorem
[`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](../two-two/P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md).
Together, the two theorems empty the entire full-support nonresonant
triangle.

The one-edge and two-edge cut boundaries are now excluded in
[`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](../degenerate-cut/P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md),
so the complete nonresonant triangle is empty.

## A factorization lemma for a triangle cut

It is enough to take the singleton coordinate to be zero.  Write

```text
q=q_12 X_1X_2+q_13 X_1X_3+q_23 X_2X_3,
q_12 q_13 q_23 != 0.                                                 (6)
```

Suppose `q=uv` in `R`, with

```text
u=sum_i u_iX_i,                 v=sum_i v_iX_i.
```

The absent edges from coordinate zero say

```text
e_j:=u_0v_j+v_0u_j=0,             j=1,2,3.                           (7)
```

There are exactly two possibilities relevant here.

### Internal factorization

If `u_0=0`, then `v_0=0`.  Indeed, otherwise (7) kills all three
coordinates of `u` and hence kills `q`.  The converse is symmetric.
Thus both factors lie in

```text
H_0={z_0=0}.                                                         (8)
```

### Reflection factorization

If `u_0v_0!=0`, equations (7) give

```text
v_j=-(v_0/u_0)u_j,                 j=1,2,3.                          (9)
```

For distinct `j,k` one has the exact identity

```text
u_0(u_jv_k+u_kv_j)+2v_0u_ju_k
  =u_je_k+u_ke_j.                                                     (10)
```

On (7), therefore,

```text
u_0 q_jk=-2v_0u_ju_k.                                                (11)
```

All three values `q_jk` in (6) are nonzero, so every coordinate of
both `u` and `v` is nonzero.  In other words, the non-internal
factorization is a fully supported sign reflection across the
singleton coordinate.

The conclusion needed below is especially short:

```text
if either factor of a full 1+3 cut lies in any coordinate
hyperplane, then the factorization is internal and both factors
lie in the cut's three-coordinate block.                            (12)
```

This is a multiaffine analogue of separating the two sign sheets of a
rank-two quadratic factorization.

## The annihilator remembers the singleton

Multiplication by (6), from `R_1` to `R_3`, has catalecticant

```text
C(q)=
( 0     q_23 q_13 q_12 )
( q_23  0    0    0    )
( q_13  0    0    0    )
( q_12  0    0    0    ).                                           (13)
```

It has rank two, and

```text
Ann_R1(q)={
 z_0=0,
 q_23z_1+q_13z_2+q_12z_3=0
}.                                                                   (14)
```

Thus the opposite plane in (3) lies in the coordinate hyperplane
selected by the cut:

```text
U_k subset H_(s_k).                                                   (15)
```

## Cyclic compatibility of the three labels

Consider edge `ij`, whose bridge `Q_ij` has singleton label `s_k`.
Both factorizations in (2) use rows lying in coordinate hyperplanes,
by (15).  The reflection alternative in the factorization lemma is
fully supported and is therefore impossible.  Both factorizations are
internal.  Hence

```text
y_i,x_i,y_j,x_j in H_(s_k),
```

or equivalently

```text
U_i,U_j subset H_(s_k).                                               (16)
```

Apply (15)--(16) cyclically.  Every local plane satisfies

```text
U_i subset H_(s_1) intersection H_(s_2) intersection H_(s_3).       (17)
```

If the three labels contain three distinct coordinates, the
intersection in (17) has dimension one and cannot contain a plane.
If they contain exactly two distinct coordinates, the intersection is
the coordinate two-plane on the complementary coordinates.  Every
`U_i` must equal that plane, whose squarefree degree-two product is the
single line spanned by the product of those two coordinates.  This
would give

```text
dim(U_iU_j)=1,
```

again impossible.

Therefore all three labels coincide, proving (4).

## Why the common label is a rank-drop boundary

With `s_1=s_2=s_3=s`, all three planes lie in `H_s`.  Every surviving
`P_4` monomial must take coordinate `s` from the remaining mode zero,
so the restriction factors as

```text
P_4|_(U_0,U_1,U_2,U_3)
 =(X_s|U_0) tensor P_3|_(U_1,U_2,U_3).                              (18)
```

The left side is nonzero and pure.  Hence `X_s|U_0` is nonzero and the
three-variable restriction on the right is nonzero and pure.

In the three-variable squarefree algebra, multiplication gives a
perfect pairing

```text
R_2 tensor R_1 -> R_3=C.                                             (19)
```

For `r_ij=dim(U_iU_j)` and `dim U_k=2`, the restricted pairing has rank
at least

```text
r_ij+2-3=r_ij-1.                                                      (20)
```

Purity makes that flattening rank one.  Therefore `r_ij<=2`, proving
(5) and the contradiction.

If one deliberately drops the rank-three hypothesis at this last
step, (18) lands in the complete pure-`P_3` sign-rectangle
classification:
[`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](../../../../../../P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md).
Allowing the fourth plane to supply coordinate `s` is precisely the
six-dimensional suspension component in
[`P4_EMBEDDED_P3_PURE_COMPONENT.md`](../../../../components/embedded-p3/P4_EMBEDDED_P3_PURE_COMPONENT.md).
That component is not merely generically excluded from `H31`; its
entire marked projective fibre is closed by
[`P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md`](../../../../../../P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md).

## The neighboring mathematical languages

The three singleton labels behave like discrete cut data.  The fact
that compatibility is controlled by whether these labels agree is in
the spirit of cut ideals and split systems; see
Sturmfels--Sullivant,
[Toric geometry of cuts and splits](https://arxiv.org/abs/math/0606683).
No cut-ideal theorem is invoked here: the present compatibility is the
much smaller `K_4` squarefree calculation above.

The earlier scalar `Omega` is a genuine multiplicative holonomy.
The resonant/nonresonant distinction is analogous to the role of
rank-one local systems and their resonance loci in arrangement theory;
see Cohen--Orlik,
[Arrangements and local systems](https://arxiv.org/abs/math/9907117).
Again, the cited theory supplies the organizing language, while
(7)--(20) are the complete proof needed here.

The useful lesson is that the apparent polynomial boundary has become
a three-label compatibility problem followed by one perfect-pairing
inequality.

## Verification

Run:

```text
python claims/p4/boundaries/rank-two-triangle/nonresonant/one-three/verify_p4_nonresonant_one_three_triangle_obstruction.py
python claims/p4/boundaries/rank-two-triangle/nonresonant/one-three/audit_p4_nonresonant_one_three_triangle_obstruction.py
```

The primary verifier checks the catalecticant, the reflection identity
(10), the coordinate-intersection alternatives, the coordinate-plane
pair rank, and the three-variable perfect pairing.  The independent
audit uses the opposite singleton convention, replays the reflection
normal form, and checks the complete 64-label support table.  These are
tiny exact replays of the displayed proof, not searches for components.
