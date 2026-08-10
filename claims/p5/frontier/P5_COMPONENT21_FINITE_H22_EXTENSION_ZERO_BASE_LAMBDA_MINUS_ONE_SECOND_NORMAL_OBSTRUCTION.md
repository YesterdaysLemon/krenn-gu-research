# Component 21: zero-base `lambda=-1` second-normal obstruction

## Status

**Exact characteristic-zero theorem in the displayed raw finite chart.**  At

```text
p=q=0,  lambda=-1,                                 (1)
```

every projective direction in the complete component-21 extension kernel has
empty complete second-normal weighted-`H22` incidence whenever its complete
first normal is zero.  The theorem treats separately the kernel `P1` at
`kappa!=0` and the kernel `P2` at `kappa=0`, including every rank-jump
direction inside them.

The calculation retains subordinate extensions, later `p,q` terms, finite
`kappa,ell` tangents, and inward weight tangents.  At singular intersections
of exact zero families it also retains the quadratic cross terms that cannot
be removed by straightening.  All surviving zero-second-normal directions
and product conditions are listed below.

This result is only for the finite raw zero-base stratum (1).  It does not
cover `lambda=1`, weight or parameter infinity, arbitrary source or ambient
degenerations, or every iterated higher zero normal.  Higher continuations
after a zero second normal remain **UNKNOWN**.  The arbitrary-order
local-to-global reduction remains **UNKNOWN**, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.  No finite-field or numerical inference is
used.

## Notation

Let `M(p,q,kappa,ell,lambda)` be the `32 x 8` stacked finite `D01/D23`
extension coefficient matrix.  Write

```text
u=e_a3,  w=e_b3,  v=-e_a1+e_b0.                   (2)
```

At (1), the exact extension kernels are

```text
kappa!=0:  span{u,w},
kappa=0:   span{u,v,w}.                            (3)
```

For a leading direction `H`, the complete first normal is

```text
N_H=[M_0 | M_p H | M_q H | M_kappa H
         | M_ell H | M_lambda H].                 (4)
```

Its last five columns correspond in order to
`dp,dq,dkappa,dell,dlambda`.  Both `D01` diagonal rows of every matrix (4)
are identically zero.

## The kernel `P1` at `kappa!=0`

Write

```text
H=Xu+Yw.                                           (5)
```

### The open direction `Y!=0`

Here `rank(N_H)=9`.  A fixed mixed rank-nine minor is

```text
-131072 Y^3 kappa^2.                              (6)
```

The complete kernel is exactly

```text
span{e_u,e_w,e_dkappa,e_dell}.                    (7)
```

These are tangents to the exact zero family with `lambda=-1`, arbitrary
finite `kappa,ell`, and extension in `span{u,w}`.  Straightening along that
family makes the complete second normal another copy of (4).  Thus a zero
second normal stays in (7), while every nonzero second normal lacks both
`D01` diagonals and is H22-empty.

### The intersection direction `H=u`

At `[X:Y]=[1:0]`, `rank(N_u)=8`; a fixed minor is

```text
65536 kappa^2.                                    (8)
```

Besides (7), its kernel contains the inward weight tangent

```text
(1/2)e_b2+e_dlambda.                              (9)
```

This is the tangent of the ordinary-weight exact kernel line meeting `u` at
`lambda=-1`, up to extension rescaling.  If `B` is the first `w` coefficient
and `R=dlambda`, straightening both exact branches leaves the quadratic force

```text
B R M_lambda w.                                   (10)
```

The matrix `[N_u | M_lambda w]` has rank nine.  Exact minors

```text
-131072 kappa^2(ell^2-1),
-131072 ell kappa                                  (11)
```

cover every finite `ell` when `kappa!=0`.  The force (10) has zero entries in
all four diagonal rows.  Consequently every second normal is H22-empty, and
a zero second normal forces

```text
B R=0,                                             (12)
```

after which its second-order coefficient lies in `ker(N_u)`.  Condition
(12) is the exact second-order branch choice between the special-weight
kernel plane and the ordinary-weight kernel line.

## The kernel `P2` at `kappa=0`

Write

```text
H=Xu+Yv+Zw.                                        (13)
```

### `Y!=0` away from the exceptional projective line

Outside

```text
X=0,  Z=ell Y,                                    (14)
```

the complete first normal has rank nine and kernel exactly

```text
span{e_u,e_v,e_w,e_dell}.                         (15)
```

Four fixed rank-nine minors have determinants

```text
-131072 X^2 Y(-Y+Z ell),
-131072 X^2 Y Z,
-131072 Y(-Y+Z ell)(Y ell-Z)^2,
-131072 Y Z(Y ell-Z)^2.                           (16)
```

For `X!=0`, the first two cover `Z=0` and `Z!=0`.  For `X=0` away
from (14), the last two cover `Z=0` and `Z!=0`.  Thus (16) is an exact
projective cover, not a generic sample.

The directions (15) are tangents to the exact `kappa=0,lambda=-1` kernel
`P2`.  After straightening, the second normal is (4), has the same rank-nine
image, and is H22-empty because its `D01` diagonal pair is zero.  A zero
second normal remains exactly in (15).

### The exceptional line `H=v+ell w`

Normalize `Y=1` on (14).  Here `rank(N_H)=7`; the two minors

```text
-8192(ell^2-1),  -8192 ell                         (17)
```

cover all finite `ell`.  The complete kernel is

```text
span{e_u,e_v,e_w,e_dp,e_dq,e_dell}.               (18)
```

Thus first-order `p,q` motion is possible only on this projective line.  Let
the first subordinate extension be

```text
A u+B v+C w,                                      (19)
```

and put `P=dp`, `Q=dq`, `E=dell`.  After straightening the exact
`p=q=kappa=0,lambda=-1` kernel family, the quadratic forcing has exactly four
possibly nonzero rows:

```text
D01 row 2:   -4 A P,
D01 row 3:    4 P(B ell-C+E),
D01 row 10:  -4 A Q,
D01 row 11:   4 Q(B ell-C+E).                     (20)
```

Every entry of (20) is mixed, while the entire `D01` block of `N_H` is zero.
Hence a nonzero force (20) cannot be cancelled into H22 form, and when (20)
vanishes the remaining second-normal image still has no `D01` diagonal.
Every complete second normal is therefore H22-empty.

The second normal is zero precisely when its second-order coefficient lies
in (18) and

```text
A P=A Q=P(B ell-C+E)=Q(B ell-C+E)=0.              (21)
```

Equivalently, either `P=Q=0`, or `A=0` and `B ell-C+E=0`.  These are retained
as exact survivor valuation patterns; no higher-order integrability is
claimed.

### `Y=0,Z!=0`: the `kappa`-jump crossing

For `H=Xu+Zw`, `Z!=0`, the complete first normal has rank eight.  Its kernel
is

```text
span{e_u,e_v,e_w,e_dkappa,e_dell},                (22)
```

and a fixed rank-eight minor is `-32768 Z^3`.  If `B` is the first `v`
coefficient and `K=dkappa`, straightening the two exact kernel sheets leaves

```text
B K M_kappa v.                                    (23)
```

The augmented matrix `[N_H | M_kappa v]` has rank nine, certified by the
fixed minor `131072 Z^3`.  The force has zero diagonal rows.  Thus every
second normal is H22-empty, and a zero second normal forces

```text
B K=0,                                             (24)
```

followed by membership of the second coefficient in (22).

### `H=u`: the triple crossing

At `[X:Y:Z]=[1:0:0]`, `rank(N_u)=7`, certified by the constant minor
`-16384`.  Its six-dimensional kernel is (22) plus the weight tangent (9).
Let `B,C` be the first `v,w` coefficients and let
`K=dkappa`, `R=dlambda`.  Exact straightening leaves

```text
B K M_kappa v + B R M_lambda v + C R M_lambda w.  (25)
```

The three displayed force columns are independent modulo `col(N_u)`:
the augmented matrix has rank ten, with constant minor `262144`.  All three
forces have zero `D01` diagonal pair.  Hence every second normal is H22-empty,
and a zero second normal forces exactly

```text
B K=0,  B R=0,  C R=0.                            (26)
```

If `R!=0`, (26) gives `B=C=0` and selects the ordinary-weight line.  If
`R=0`, it gives either `B=0` and allows the special-weight kernel plane to
move in `kappa`, or `K=0` and stays on the `kappa=0` kernel `P2`.  This is the
complete second-order branch decomposition at the triple intersection.

## Boundary

Equations (12), (21), (24), and (26) classify all zero-second-normal
survivors at `lambda=-1`; none is silently discarded.  They do not prove
that every survivor integrates, nor do they iterate the straightening past
this order.  The `lambda=1` kernel `P2/P3` has different generators and is
not claimed by symmetry.

## Replay

```powershell
uv run --with sympy python verify_p5_component21_finite_h22_extension_zero_base_lambda_minus_one_second_normal_obstruction.py
uv run --with sympy python audit_p5_component21_finite_h22_extension_zero_base_lambda_minus_one_second_normal_obstruction.py
```

The primary verifier uses the committed component-21 contraction builder.
The audit has no repository imports and reconstructs every permanent by
direct six-term summation.
