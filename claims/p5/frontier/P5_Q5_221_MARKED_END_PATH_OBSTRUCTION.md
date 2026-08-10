# Exact obstruction for the marked-end `q5_221` path

## Status

This is an exact tensor theorem over `C`.

There is no exact normalized `q5_221` rank-drop pattern

```text
D_0={C,D},  D_1={B,D},  D_2={A,C}.                  (1)
```

This is the three-edge path whose distinguished singleton-colour edge
is an end edge.  The proof combines the nonzero decomposable-`P_3`
normal classification, one small complement-pairing lemma, and two
four-row permanent coefficients.  It does not search row spaces.

Together with the marked-middle theorem, this closes all nine exact
minimal marked incidence types.  Extra containments remain outside the
scope of this theorem, so normalized `q5_221`, `P_5 -> Delta_3`, and
the arbitrary-order Krenn--Gu conjecture remain open.

## Coordinates and cross residuals

Use

```text
u_0=e_0+e_1,  h_0=e_0-e_1,
u_1=e_2+e_3,  h_1=e_2-e_3,  h_2=e_4.
```

The exact row-space incidences in (1) are

```text
A: h_2,
B: h_1,
C: h_0,h_2,
D: h_0,h_1.                                         (2)
```

At `D`, the local cross-scalar alternative makes at least one of

```text
Q_01=Sym(u_0,h_1,h_2),
Q_10=Sym(h_0,u_1,h_2)                               (3)
```

a nonzero pure residual through `A,B,C`.  At `C`, at least one of

```text
Q_02=Sym(u_0,e_2,e_3),
Q_20=Sym(h_0,e_2,e_3)                               (4)
```

is nonzero pure through `A,B,D`.  As in the earlier `q5_221`
obstructions, “`Q_cd` is zero/nonzero” below refers to this pure image,
equivalently to its cross scalar.

## The two rank-one gates at `D`

Suppose `Q_01` is nonzero.  Its residual annihilator is

```text
J_01^perp=span(h_0,u_1).
```

If the mode-`C` restriction had rank at least two, all three residual
maps would have rank at least two.  Modes `A,C` contain the source
factor `h_2`, so both plane normals would omit the `h_2` coordinate.
Mode `B` contains the source factor `h_1`, so its normal would omit the
`h_1` coordinate.  Their common normal support could contain only
`u_0`, contrary to the nonzero decomposable-`P_3` classification.
Thus `C` is the unique possible rank-one gate:

```text
U_C=span(h_0,h_2,u_1).                               (5)
```

The surviving source factor at `C` is `h_2`, and it maps to target
colour zero.  If `alpha_(C,2)` pulls back to `h_2`, then

```text
alpha_(C,2)(e_0)!=0.
```

This is exactly the cross scalar for `Q_02`.  Therefore

```text
Q_01 nonzero  ==>  Q_02 nonzero.                    (6)
```

The symmetric support argument for a nonzero `Q_10` makes `B` its
rank-one gate:

```text
u_0 in U_B,
U_B=span(u_0,h_1,r).                                 (7)
```

## Every nonzero `Q_02` branch is impossible

Assume `Q_02` is nonzero.  Its three maps at `A,B,D` all have rank
two: exactness rules out rank one, and the nonzero `P_3` theorem rules
out rank three.

We first show

```text
L_B(u_1)=L_D(u_1)=0.                                 (8)
```

If `Q_10` is nonzero, (7) makes the `Q_02` plane normal at `B` equal
to `u_1`.  Mode `D` contains `h_1`; common support in the nonzero
`Q_02` sign chart then selects the same `u_1` normal at `D`.

It remains to obtain (8) if `Q_01` is nonzero.  By (5), the
colour-two row plane of `C` on

```text
H_2=span(e_0,e_1,e_2,e_3)
```

is

```text
V=span(h_0,u_1).
```

The corresponding plane `U` at `A` contains neither `h_0` nor `h_1`.
Let

```text
T_v(w)=(w_p v_q+w_q v_p)_(p<q)
```

be the pair map into the six off-diagonal coordinates.  Its restriction
`T_(u_1)|U` is injective because

```text
ker T_(u_1)=C h_1.
```

If `dim A(U,V)<=2`, then the two-dimensional image
`T_(u_1)(U)` would contain `T_(h_0)(U)`.  The `01` coordinate first
forces every `w in U` to satisfy `w_0=w_1`.  If
`w=(a,a,c,d)` and `T_(h_0)(w)=T_(u_1)(v)` for `v in U`, comparison of
coordinates `02,03,12,13` gives

```text
c=d=-c=-d,
```

so `c=d=0`.  This would make the plane `U` one-dimensional, a
contradiction.  Hence

```text
dim A(U,V)>=3.                                       (9)
```

The `AC|BD` flattening of the colour-two tensor is the nondegenerate
complement pairing between the two pair images.  Its target has rank
one, so (9) gives

```text
dim A(U_B|H_2,U_D|H_2)<=4.
```

The hyperplane-pair classification says that the two hyperplanes are
equal and their common normal has coordinate support at most two.
Because `D` contains both `h_0,h_1`, that normal is `u_0` or `u_1`.
The choice `u_0` is a support-one `Q_02` normal, impossible.  Thus the
normal is `u_1`, proving (8).

The `Q_02` sign chart now has normals

```text
h_1 at A,  u_1 at B,  u_1 at D,                     (10)
```

and decomposable factor directions

```text
u_0 at A,  h_1 at B,  h_1 at D.                     (11)
```

All three directions in (11) map to target colour zero.

At `A`, the covector pulling back to `h_2` vanishes in target
coordinate two by the diagonal identity and in coordinate zero by
(11).  Hence

```text
L_A^* epsilon_1 in C^* h_2,
L_A^* epsilon_2|H_2 in C^*(u_1+beta h_0),            (12)
```

with both displayed leading coefficients nonzero.  At `B,D`, (8) and
(11) imply

```text
L_B^* epsilon_1|H_2,
L_D^* epsilon_1|H_2 in span(u_0,h_0).                (13)
```

Let `gamma` be the `u_1` coefficient of
`L_C^* epsilon_1|H_2`, and let `P` be the two-row permanent of the
rows in (13) on `e_0,e_1`.  The required all-colour-one coefficient of

```text
T_1=Sym(e_0,e_1,u_1,h_2)
```

is a nonzero scalar times

```text
gamma P.                                             (14)
```

Indeed, `A` supplies `h_2`, `C` supplies `u_1`, and `B,D` supply
`e_0,e_1`.  Since the pure `T_1` coefficient is nonzero, (14) is
nonzero.

Now take the forbidden target colouring

```text
(A,B,C,D)=(2,1,1,1)
```

of `T_2=Sym(e_0,e_1,e_2,e_3)`.  Modes `B,D` again supply
`e_0,e_1`.  The `h_0` term in (12) vanishes on `e_2,e_3`, and the
`h_1` component of the row at `C` cancels against `u_1`.  The
coefficient is therefore another nonzero scalar times the same
`gamma P`, contradicting purity of `T_2`.  Every nonzero `Q_02`
branch is impossible.

## The remaining branch

We may now assume `Q_02=0`.  Equation (6) gives `Q_01=0`, so the local
alternatives at `C,D` force

```text
Q_20 nonzero,  Q_10 nonzero.                         (15)
```

The zero cross scalars and own-colour diagonal entries pin two target
rows:

```text
L_C^* epsilon_1 in C^* h_2,
L_D^* epsilon_2 in C^* h_1.                         (16)
```

Moreover, the nonzero `Q_10` scalar makes

```text
L_D^* epsilon_1 in span(h_0,h_1)
```

with a nonzero `h_0` coefficient.

By (7), `B` is the rank-one `Q_10` mode.  Write

```text
U_B=span(u_0,h_1,r_B),
L_B(r_B) in C^*e_1.                                  (17)
```

### Rank-one `Q_20` at `A`

If the `Q_20` restriction at `A` has rank one, then

```text
U_A=span(u_0,h_2,r_A),
L_A(r_A) in C^*e_2.
```

Consequently

```text
L_A^* epsilon_1 in span(u_0,h_2).                    (18)
```

Consider the required all-colour-one coefficient of `T_1`.  The row
at `C` in (16) must supply `h_2`.  The row at `D` annihilates `u_1`,
as does (18), so the row at `B` must supply `u_1`.  The two remaining
rows on `e_0,e_1` are proportional to `u_0` at `A` and have nonzero
`h_0` part at `D`.  Their permanent is

```text
per(u_0,h_0)=0.
```

Thus the required pure `T_1` coefficient would be zero, a
contradiction.

### Rank-two `Q_20` at `A`

Otherwise all three `Q_20` residual maps have rank two.  Its sign chart
has normals

```text
h_1 at A,  u_1 at B,  u_1 at D,                     (19)
```

because the `D` plane contains both source rows `h_0,h_1`.  After
harmless row-basis choices,

```text
U_A=span(h_2,h_0+a u_0,u_1+b u_0),   a!=0,
U_B=span(u_0,h_1,h_0+k h_2),         k!=0,
U_D=span(h_0,h_1,u_0+d h_2).                         (20)
```

The factor directions in the nonzero `Q_20` image are

```text
h_0 at A,  h_1 at B,  h_1 at D,
```

all mapping to target colour two.  Combining this with (16)-(17), the
only rows needed below can be normalized as

```text
A_1=r h_2+s(u_1+b u_0),
B_0=u_0,
B_1=h_0+k h_2+sigma u_0,
C_1=c h_2,
D_0=C(u_0+d h_2)+A h_0,
D_1=h_0,                                             (21)
```

where `c,C` are nonzero.

The required all-colour-one coefficient of `T_1` formed from
`A_1,B_1,C_1,D_1` is

```text
-4 c s
```

up to the harmless nonzero row normalizations.  Hence `s!=0`.

The forbidden target colouring

```text
(A,B,C,D)=(1,0,1,0)
```

uses `A_1,B_0,C_1,D_0`.  Its coefficient is

```text
4 c C s,
```

again up to the same harmless conventions.  This is nonzero because
`c,C,s` are nonzero, contradicting purity of `T_1`.

Both ranks at `A` are impossible.  This excludes the remaining branch
and completes the proof of (1).

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_marked_end_path.py
python claims/p5/frontier/audit_p5_q5_221_marked_end_path.py
```

The primary verifier reconstructs the pair-image lemma, both
support-two residual charts, and every decisive permanent coefficient
symbolically over `C`.  The independent audit checks the pair-image
lower bound over `F_3,F_5` and repeats the coefficient expansions with
a separate exact polynomial implementation.  The finite-field portion
audits only the linear-algebra lemma; the written proof is over `C`.
