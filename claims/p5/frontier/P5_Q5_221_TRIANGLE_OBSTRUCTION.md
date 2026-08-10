# Triangle and singleton-cover obstruction in normalized `q5_221`

## Status

This is an exact tensor theorem over `C`.

In normalized `q5_221`, suppose

```text
U_A contains exactly h_0,h_1,
U_B contains exactly h_0,h_2,
U_C contains exactly h_1,h_2,                        (1)
```

among the three distinguished normals.  If `U_D` contains at most one
of `h_0,h_1,h_2`, the required restriction is impossible in either of
the two repeated-`h_2` chiralities.  Thus the theorem excludes the exact
minimal triangle and both marked singleton extensions: the added normal
may have the distinguished colour or either majority colour.  These are
two of the fourteen seven-incidence cover orbits in
[`P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md`](P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md).
This theorem does not address the other twelve exact cover orbits or
any monotone cover boundary.  Later work excludes several of those
orbits by different arguments, but normalized `q5_221`, the full
restriction `P_5 -> Delta_3`, and the arbitrary-order Krenn--Gu
conjecture remain open.

## Normalized source directions and chiral split

Use

```text
u_0=e_0+e_1,   h_0=e_0-e_1,
u_1=e_2+e_3,   h_1=e_2-e_3,   h_2=e_4.
```

The six cross residuals and their source spaces are those in
[`P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md`](P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md).
For example,

```text
J_02=span(u_0,e_2,e_3),
J_12=span(e_0,e_1,u_1),
J_01=span(u_0,h_1,h_2),
J_10=span(h_0,u_1,h_2).                              (2)
```

The first three modes are as in (1).  Mode `D` contains zero or one
distinguished normal.  The proof below first treats the cases in which
`D` contains no normal or only `h_2`; the majority-singleton extension
is handled afterward.

Repeated contraction by `h_2` at `B,C` leaves two cases:

```text
I:   Q_02 at B and Q_12 at C are nonzero;
II:  Q_12 at B and Q_02 at C are nonzero.             (1)
```

## Chirality I: common-support transport

Write

```text
U_A=span(h_0,h_1,a u_0+b u_1+c h_2).                 (3)
```

In the ordered bases of `J_02` and `J_12` in (2), the two mode-`A`
plane normals are, up to nonzero coordinate scalings,

```text
n_A,02=(b,-a,-a),
n_A,12=(b, b,-a).                                    (4)
```

The two chirality-I residuals in (1) are nonzero decomposable
restrictions of `P_3`.  Every local residual map has rank at least two.
At `D`, optional containment of `h_2` gives a one-dimensional
intersection with each of `J_02^perp=span(h_0,h_2)` and
`J_12^perp=span(h_1,h_2)`; absence of `h_0,h_1` prevents rank one.
The nonzero decomposable-`P_3` classification therefore applies.  A
normal of support one is forbidden, so (4) gives

```text
a != 0,  b != 0.                                     (5)
```

## Carrying the common support into modes `B` and `C`

Modulo their two forced normals, write

```text
U_C=span(h_1,h_2,p u_0+q h_0+r u_1),
U_B=span(h_0,h_2,s u_0+t h_1+v u_1).                 (6)
```

For the nonzero `Q_02` residual, the mode-`C` plane normal is

```text
n_C,02=(r,-p,-p).
```

The `P_3` classification says that its coordinate support agrees with
the support of `n_A,02`.  By (5), the latter support is all three
coordinates.  Hence

```text
p != 0,  r != 0.                                     (7)
```

Similarly, for the nonzero `Q_12` residual the mode-`B` plane normal is

```text
n_B,12=(v,v,-s),
```

so

```text
s != 0,  v != 0.                                     (8)
```

These two conclusions are the missing compatibility condition in the
earlier working note.  In particular, the apparent spaces

```text
span(h_0,h_2,u_1),  span(h_1,h_2,u_0)
```

cannot occur in chirality I: their residual normals have support two,
whereas (4) has support three.

## Cross-scalar contradiction

At mode `A`, the zero diagonal contractions for `h_0,h_1` imply that
at least one of

```text
Q_01, Q_10
```

is sent to a nonzero pure cube.  This is the cross-scalar lemma: if both
cross scalars vanished, the two independent target covectors pulling
back to `h_0,h_1` would both lie on the third target-coordinate line.

Suppose first that `Q_01` is nonzero.  On

```text
J_01=span(u_0,h_1,h_2)
```

the three remaining maps have ranks

```text
rank_B=2,  rank_C=3,  rank_D>=2.                      (9)
```

Indeed, (8) makes the mode-`B` projection contain `h_2` and a vector
with nonzero `u_0` coefficient, while (7) makes the mode-`C` projection
contain the independent triple `h_1,h_2,u_0`.  The mode-`D` rank is at
least two because

```text
J_01^perp=span(h_0,u_1)
```

and exactness gives `h_0 notin U_D`.  But every nonzero decomposable
rank-at-least-two restriction of `P_3` has rank profile `222`.
The rank-three mode in (9) is a contradiction.  Therefore `Q_01=0`.

The argument for `Q_10` is symmetric but uses the other nonzero
coefficients in (7)--(8).  On

```text
J_10=span(h_0,u_1,h_2)
```

the ranks are

```text
rank_B=3,  rank_C=2,  rank_D>=2.                      (10)
```

Here `v != 0` supplies the third independent mode-`B` direction, and
`J_10^perp=span(u_0,h_1)` together with `h_1 notin U_D` gives the last
rank gate.  Again the nonzero `P_3` classification rejects (10), so
`Q_10=0`.

Both cross residuals are zero, contradicting the cross-scalar lemma.
This excludes chirality I.

## Chirality II: wrong-colour rank-one gates

In chirality II, the two `h_2` pullback covectors have complementary
singleton support on target colours zero and one.  More precisely,

```text
L_B^*(epsilon_1)=rho_B h_2,
L_C^*(epsilon_0)=rho_C h_2,                           (11)
```

for nonzero scalars `rho_B,rho_C`.  Thus a rank-one residual at `B`
supported only on `h_2` has target image `span(e_1)`, while the
corresponding residual at `C` has target image `span(e_0)`.

Use the same row-space parametrization (6), now without the
chirality-I nonvanishing conclusions.  Suppose `Q_01` were nonzero.
On

```text
J_01=span(u_0,h_1,h_2)
```

the mode-`B` restriction has rank one exactly when

```text
s=t=0.
```

Exactness then gives `v != 0`, so

```text
U_B=span(h_0,h_2,u_1).
```

Only the `h_2` row survives on `J_01`.  By (11) its image is target
colour one, but nonzero `Q_01` must be a pure cube in target colour
zero.  This rank-one exception is therefore impossible.  Outside it,
the mode-`B` residual rank is at least two.

At mode `C`, restriction to `J_01` has rank three when `p != 0`.
When `p=0`, its row plane is

```text
span(h_1,h_2) subset J_01^*,
```

whose normal is the support-one vector `u_0`.  Mode `D` again has rank
at least two because `h_0 notin U_D`.  Hence a nonzero `Q_01` would
either have a rank-three local map or a support-one plane normal.
Both alternatives contradict the nonzero decomposable-`P_3`
classification.  Thus

```text
Q_01=0.                                               (12)
```

The argument for `Q_10` is symmetric.  Its mode-`C` restriction has
rank one exactly when `q=r=0`; exactness then gives

```text
U_C=span(h_1,h_2,u_0).
```

Only `h_2` survives on `J_10`, and (11) puts its image in target colour
zero rather than the required target colour one.  Outside that
wrong-colour exception, mode `C` has rank at least two.  Mode `B` has
rank three when `v != 0`, while for `v=0` its residual plane
`span(h_0,h_2)` has support-one normal `u_1`.  Therefore

```text
Q_10=0.                                               (13)
```

Equations (12)--(13) again violate the cross-scalar lemma at `A`.
This excludes chirality II and completes both the exact triangle and
its distinguished-singleton extension.

## Majority-singleton extension

It remains to allow one majority normal at `D`.  The two majority
colours are symmetric, so take

```text
h_0 in U_D,  h_1,h_2 notin U_D.                     (14)
```

The direct residuals `Q_02,Q_12` still have rank at least two at `D`.
The only new cross-residual gate in the proof above is rank one for
`Q_01`; rank one for `Q_10` would require `h_1 in U_D`, contrary to
(14).

If the `Q_01` gate occurs, write

```text
U_D=span(h_0,u_1,r),
r=a u_0+b h_1+c h_2.                                (15)
```

On `J_02`, the two nonzero restricted rows are

```text
u_1=(0,1,1),  r=(2a,b,-b),
```

so their plane normal is

```text
n_D,02=(b,-a,a).                                     (16)
```

On `J_12`, the determinant of the restrictions of
`h_0,u_1,r` is a nonzero scalar times `a`.

In chirality I, the original common-support transport gives full support
for every `Q_02` plane normal.  Equation (16) therefore has
`a,b!=0`.  But then the mode-`D` restriction to `J_12` has rank three,
contradicting the simultaneous nonzero `Q_12` residual.  Hence the new
rank-one gate cannot rescue `Q_01`; the cross-scalar contradiction from
chirality I remains valid.

In chirality II, the earlier argument still gives `Q_10=0`.  A nonzero
`Q_01` can escape its rank-three/support-one contradiction only through
the new rank-one gate (15).  Both direct residuals are nonzero.  The
nonzero decomposable-`P_3` theorem forces the mode-`D` rank on `J_12`
to be two, hence `a=0`.  Exactness in (14) then gives `b!=0`: otherwise
`r` would be a multiple of `h_2`.  Equation (16) becomes the
support-one normal `u_0`, impossible for the nonzero `Q_02` residual.

This excludes the majority-singleton extension.  Swapping majority
colours handles `h_1 in U_D`.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_triangle_obstruction.py
python claims/p5/frontier/audit_p5_q5_221_triangle_obstruction.py
```

The primary verifier reconstructs the four residual spaces, the
symbolic plane normals, both chiral rank boundaries, the wrong-colour
rank-one images, the majority-singleton gate, the decisive rank minors,
and the cross-scalar gate over `C`.  The independent audit enumerates
rank-three row spaces over `F_3` and `F_5`; it checks the common-support
implications, the wrong-colour gates, and all three possible singleton
extensions at mode `D`.  The finite-field audit corroborates the
incidence formulas; the written argument above is the
characteristic-zero proof.
