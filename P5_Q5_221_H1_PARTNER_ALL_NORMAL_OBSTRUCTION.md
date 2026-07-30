# `h_1,h_2`-partner all-normal obstruction in normalized `q5_221`

## Status

This is an exact monotone tensor theorem over `C`.

Suppose one of the two `h_2` modes is all-normal and the other contains
`h_1`.  Suppose also that a third mode contains `h_1` and at least one
of the two non-`h_2` modes contains `h_0`.  Then a normalized
`q5_221` restriction is impossible.

This excludes monotone covers `#6` and `#11`, including all their
higher-incidence strata.  Five monotone cover orbits remained at this
checkpoint; the later fixed-kernel and final-boundary theorems close
them and complete normalized `q5_221`.  The full `P_5 -> Delta_3`
problem and the global conjecture remain open.

## Setup and the two orientations

Let `F` be the all-normal mode, `P` the other `h_2` mode, `X` a third
`h_1` mode, and `Y` the remaining mode.  Thus

```text
h_0,h_1,h_2 in U_F,
h_1,h_2 in U_P,
h_1 in U_X,
h_0 in U_X or U_Y.                                   (1)
```

The distinguished-normal theorem says these are exactly the two
`h_2` modes and their pullbacks have complementary target support.  If
`h_0` were also in `U_P`, both `h_2` modes would be all-normal, already
excluded by the two-all-normal theorem.  Hence assume

```text
h_0 notin U_P.                                       (2)
```

There are two orientations:

```text
I:  L_F^*epsilon_0 in C*h_2,
    L_P^*epsilon_1 in C*h_2;

II: L_F^*epsilon_1 in C*h_2,
    L_P^*epsilon_0 in C*h_2.                         (3)
```

## Orientation I: the block-apolar dichotomy

Contract `T_0` at `F`.  The nonzero `Q_02` residual runs through
`P,X,Y` and is pure in target colour zero.  No local residual rank is
one: rank one on

```text
J_02^perp=span(h_0,h_2)
```

would require a third `h_2` incidence at `X,Y`, or the excluded
containment `h_0 in U_P`.  The nonzero decomposable-`P_3`
classification therefore applies and forces rank profile `222`.

The planes at `P,X` both contain `h_1`, so their normals in coordinates
`(u_0,e_2,e_3)` satisfy `n_1=n_2`.  As in the cover-`#13` theorem,
there are only two sign strata:

```text
support two:
  n_P=n_X=u_1, with factor directions h_1,h_1;

full support:
  n_P=(a,b,b), n_X=(a,-b,-b), with factors e_2,e_3
  in one order.                                      (4)
```

In either stratum the factor direction at `X` has nonzero `h_1`
evaluation.  Thus the `h_1` pullback at `X` has nonzero target-zero
coordinate, and contracting there gives a nonzero pure `Q_01`
residual through `F,P,Y`.

At `F`, the `Q_01` plane is `span(h_1,h_2)` and has support-one normal
`u_0`.  Modes `F,P` have residual rank at least two.  The nonzero
`P_3` theorem can therefore be escaped only by rank one at `Y`:

```text
span(h_0,u_1) subset U_Y.                            (5)
```

The target-two row at `F`, restricted to `H_2`, is `h_1`.  In the
support-two stratum of (4), the target-two rows at `P,X` lie in
`span(u_0,h_0)`, while (5) places the target-two row at `Y` in
`span(u_1,h_0)`.  The required `T_2[2222]` coefficient is zero:
the `h_0` component has block degree `3+1`, and the `u_1` component
contains

```text
Perm_2(h_1,u_1)=0.                                   (6)
```

In the full-support stratum, after nonzero target-coordinate
rescaling,

```text
P_2=P_0+a' h_1,
X_0=X_2+b' h_1,   a'b'!=0.                           (7)
```

Fixing the rows at `F,Y`, the four target-coordinate choices at `P,X`
form the same rectangle as in the cover-`#13` proof.  Three corners
are forbidden mixed coefficients and the fourth is the required pure
coefficient.  Their alternating difference is

```text
T_2(h_1,h_1,h_1,Y_2)=0.                              (8)
```

Hence the forbidden fourth corner equals the required nonzero corner,
a contradiction.  Orientation I is impossible.

## Orientation II: the directed-cycle factor collision

Let `alpha_Fc` pull back to `h_c`.  In orientation II the three
pullbacks have zero diagonal and

```text
alpha_F2=epsilon_1.
```

After rescaling, their target-coordinate matrix has the form

```text
[ 0  a  b ]
[ c  0  d ]
[ 0  1  0 ],                                        (9)
```

whose determinant is `bc`.  Thus `b,c` are nonzero.  Contracting at
`F` forces the directed residual cycle

```text
Q_20 -> e_2^3,
Q_01 -> e_0^3,
Q_12 -> e_1^3                                       (10)
```

through the same modes `P,X,Y`.  This is the opposite cycle from the
one used in orientation I.

At `P`, the `Q_12` map has rank one because
`J_12^perp=span(h_1,h_2)` is contained in `U_P`.  The `Q_20` map has
rank one or two.  We treat those two intrinsic rank strata.

### Rank two at `P`

The modes `X,Y` do not contain `h_2`, so their `Q_20` ranks are at
least two.  The nonzero decomposable-`P_3` theorem makes all three
ranks two.  Hence

```text
u_0 in U_X intersect U_Y.                            (11)
```

In `J_20=(h_0,e_2,e_3)` coordinates, the kernel normals at `P,X`
have equal last two coordinates because both row spaces contain
`h_1`.  One of `X,Y` also contains `h_0`.  The `P_3` sign
classification then has only the support-two chart

```text
normals:  n_P=n_X=u_1,  n_Y=h_1,
factors:  h_1 at P,X,   h_0 at Y.                    (12)
```

Indeed a normal belonging to the `h_0` mode has zero first coordinate;
the common-support theorem forces support `{e_2,e_3}`, and the two
equal-coordinate normals can only be the repeated `u_1` variant.

The normal `n_P=u_1`, together with rank two and
`h_0 notin U_P`, writes the third row of `U_P`, modulo `h_1,h_2`, as

```text
a u_0+b h_0,  ab!=0.
```

Consequently `P` has rank three on `J_01`.  A nonzero decomposable
`Q_01` image must therefore have a rank-one mode.  That mode cannot be
`X`: equations (11) and `h_1 in U_X` already occupy the independent
directions `u_0,h_1`, while rank one on `J_01` would add both
`h_0,u_1`.  Hence `Y` has rank one on `J_01`.  Combining this with
(11) gives

```text
U_Y=span(u_0,h_0,u_1).                               (13)
```

Contract `Q_01` at `Y` by its surviving `u_0` row.  The remaining
bilinear tensor is

```text
Sym(h_1,h_2) -> e_0 tensor e_0.                      (14)
```

At `P`, the two displayed directions have independent images because
the `J_01` map has rank three.  Thus the two-summand Segre lemma makes
their images dependent at `X`.  In particular the local factor line
of `Q_01` at `X` is the line of `L_X(h_1)`.  But (12) says that the
local factor line of `Q_20` at `X` is the same line.  Equation (10)
would have to send that one line simultaneously to target colours zero
and two, a contradiction.

### Rank one at `P`

Now

```text
U_P=span(u_0,h_1,h_2).                               (15)
```

The local factors of `Q_20,Q_12` at `P` are respectively `h_1,u_0`.
Contracting them gives two nonzero bilinear identities through `X,Y`:

```text
Sym(h_0,h_1) -> e_2 tensor e_2,
Sym(u_0,u_1) -> e_1 tensor e_1.                      (16)
```

Each identity forces its source pair to become dependent at `X` or
at `Y`.  The two dependencies must occur at opposite modes.  Otherwise
one mode would collapse both pairs

```text
{h_0,h_1}, {u_0,u_1},
```

and have rank at most two on `H_2`, whereas neither `X` nor `Y`
contains `h_2` and both have rank three there.

The `Q_01` map at `P` has rank three.  Hence one of `X,Y` has rank one
on `J_01` and contains `span(h_0,u_1)`.

If that mode is `X`, then

```text
U_X=span(h_0,u_1,h_1).
```

The second identity in (16) reduces to the nonzero product
`L_X(u_1) tensor L_Y(u_0)`, so the `Q_12` factor at `Y` is
`L_Y(u_0)`.  Contracting `Q_01` at `X` by its surviving `h_1` row
leaves

```text
Sym(u_0,h_2) -> e_0 tensor e_0.
```

The two directions are independent at `P`, so they become dependent
at `Y`.  The `Q_01` factor at `Y` is again the line of `L_Y(u_0)`,
contradicting the distinct target colours in (10).

It remains that `Y` is the rank-one `Q_01` mode.  Write

```text
U_Y=span(h_0,u_1,w),  p=w(u_0), q=w(h_1), r=w(h_2).
```

If the first dependency in (16) occurs at `Y`, then `q=0` and the
second pair is independent there, so `p!=0`.  Contracting `Q_01` at
`Y` gives

```text
Sym(h_1,p h_2+r u_0).
```

Those two directions are independent at `P`, so they become dependent
at `X`.  Its `Q_01` factor is therefore the line of `L_X(h_1)`, which
is already the `Q_20` factor at `X` from the first identity in (16).

If instead the second dependency in (16) occurs at `Y`, then `p=0`
and `q!=0`.  The contracted `Q_01` tensor is

```text
Sym(u_0,q h_2+r h_1).
```

The same argument makes its factor at `X` the line of `L_X(u_0)`,
which is already the `Q_12` factor there.  Either way two different
target colours in (10) share one local factor line, a contradiction.

Orientation II is impossible, completing the monotone proof.

## Verification

Run:

```text
python verify_p5_q5_221_h1_partner_all_normal.py
python audit_p5_q5_221_h1_partner_all_normal.py
```

The primary verifier reconstructs both orientation-I `Q_02` sign
strata and `T_2` identities, the orientation-II zero-diagonal cycle,
the support-two `Q_20` chart, and every bilinear factorization used in
the two rank branches.  The independent audit uses squarefree apolar
differentiation and a separate factor-line calculation.  Neither
verifier enumerates local maps or ambient row spaces.
