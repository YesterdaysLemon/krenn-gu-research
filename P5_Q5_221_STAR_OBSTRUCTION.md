# Exact obstruction for the `q5_221` star type

## Status

This is an exact tensor theorem over `C`.

In normalized `q5_221`, there is no exact star rank-drop pattern

```text
D_0={O,V_0},  D_1={O,V_1},  D_2={O,V_2}.             (1)
```

This theorem closed the seventh of the nine exact minimal marked
incidence types.  The later two marked-path theorems close the exact
minimal list.  All extra-containment strata, normalized `q5_221`, the
full restriction `P_5 -> Delta_3`, and the arbitrary-order Krenn--Gu
conjecture remain open.

## A zero-diagonal determinant forces a directed cycle

Use

```text
u_0=e_0+e_1,  h_0=e_0-e_1,
u_1=e_2+e_3,  h_1=e_2-e_3,  h_2=e_4.
```

At the centre of the exact star,

```text
U_O=span(h_0,h_1,h_2).
```

Let `alpha_c` be the unique target covector with

```text
L_O^* alpha_c=h_c.
```

The three covectors form a basis, and their own-colour entries vanish:

```text
alpha_c(e_c)=0.
```

Put

```text
q_cd=alpha_d(e_c).
```

In the target-colour basis, the matrix with rows `alpha_0,alpha_1,alpha_2`
is

```text
M = [  0    q_10  q_20
      q_01   0    q_21
      q_02  q_12   0   ].
```

It is invertible, so

```text
det M = q_10 q_21 q_02 + q_20 q_01 q_12 != 0.        (2)
```

Consequently at least one of the two directed cycles

```text
C_+: Q_20,Q_01,Q_12,
C_-: Q_10,Q_21,Q_02                                  (3)
```

has nonzero pure image through the three leaf modes.  The two cycles
are exchanged by swapping the two majority colours, so it suffices to
exclude `C_+`.

## The `Q_01` rank-one gate

The residual

```text
Q_01=Sym(u_0,h_1,h_2),
J_01^perp=span(h_0,u_1)
```

is nonzero in `C_+`.  At `V_1`, the restricted row plane contains the
coordinate covector `h_1`; at `V_2`, it contains the distinct
coordinate covector `h_2`.  If all three residual ranks were at least
two, the nonzero decomposable-`P_3` classification would make the two
plane normals have the same coordinate support of size at least two.
The first normal has zero `h_1` coordinate and the second has zero
`h_2` coordinate, so their common support could contain only `u_0`.
That is impossible.

Exactness makes the residual ranks at `V_1,V_2` at least two.  Hence
the rank-one mode is `V_0`, and

```text
u_1 in U_(V_0),
U_(V_0)=span(h_0,u_1,r).                              (4)
```

## The other two residuals fix the three leaf charts

Every local rank of

```text
Q_12=Sym(e_0,e_1,u_1)
```

is at least two: its annihilator is `span(h_1,h_2)`, while each leaf
contains exactly one of the three normals.  Since `Q_12` is nonzero,
all three ranks are exactly two.

At `V_0`, equation (4) already supplies the independent rows
`h_0,u_1`.  Rank two on `J_12` says that `r` has no `u_0` component.
After subtracting the two displayed rows,

```text
r=a h_1+b h_2.
```

Exactness forces both coefficients to be nonzero: otherwise the row
space contains `h_1` or `h_2`.  Normalize

```text
U_(V_0)=span(h_0,u_1,h_1+k h_2),  k!=0.              (5)
```

On `J_20=span(h_0,e_2,e_3)`, the three rows in (5) are independent.
Thus `V_0` has rank three in the nonzero `Q_20` residual.  A nonzero
pure `P_3` image cannot have rank profile at least two with a
rank-three mode.  Exactness rules out a rank-one gate at `V_1`, so
`V_2` must be rank one:

```text
u_0 in U_(V_2).
```

Return to `Q_12`.  Its plane normal at `V_0` is `u_0`.  At `V_2`, the
row `u_0` is present, so common support forces the opposite normal
`h_0`.  If the `V_1` normal were `u_0`, its lift together with
`h_1 in U_(V_1)` would have rank three on `J_20`.  After the rank-one
map at `V_2`, contraction of `P_3` leaves a bilinear form of matrix
rank at least two; rank-three maps at both `V_0,V_1` cannot turn it
into a pure tensor.  Therefore the `V_1` normal is also `h_0`.

The three `Q_12` normals are consequently

```text
u_0, h_0, h_0.                                       (6)
```

A direct expansion of this support-two `P_3` chart shows that its
three decomposable factor directions are

```text
u_1 at V_0,  u_0 at V_1,  u_0 at V_2.                (7)
```

Because `Q_12` has pure target colour one,

```text
L_(V_0)(u_1) in C^* e_1,
L_(V_1)(u_0) in C^* e_1,
L_(V_2)(u_0) in C^* e_1.                             (8)
```

The rank-one `Q_20` contraction leaves the factor `h_0` at `V_0`.
Its pure target colour is two, hence

```text
L_(V_0)(h_0) in C^* e_2.                             (9)
```

Finally, the rank-one `Q_01` image at `V_0` has target colour zero.
Equations (5), (8), and (9) therefore fix the only source components
needed below:

```text
L_(V_0)^* epsilon_0 | H_2 = c_0 h_1,
L_(V_2)^* epsilon_1 | H_2 = c_2 u_0,                 (10)
```

where `H_2=span(e_0,e_1,e_2,e_3)` and the displayed scalars are
nonzero.  At `V_1`, let `s` be the direction of
`L_(V_1)^* epsilon_0` in `span(h_1,u_1)`.  The `Q_12` factor direction
and the `Q_20` pure-colour condition give

```text
L_(V_1)^* epsilon_1 | H_2 = c_1 u_0+t s,             (10a)
```

with `c_1!=0`.  The possible shear term is important: target colours
do not permit us simply to change it away.

## A forced forbidden coefficient

The coefficient of `h_1` in the central row
`L_O^* epsilon_0` is the `(0,1)` entry of `M^{-1}`.  From the matrix
above,

```text
[h_1] L_O^* epsilon_0
  = q_20 q_12 / det M != 0                           (11)
```

in cycle `C_+`.  On `H_2`, its other relevant component is a multiple
of `h_0`.

Now use the colour-two embedded tensor

```text
T_2=Sym(e_0,e_1,e_2,e_3).
```

Consider its target coefficient with leaf/centre colouring

```text
(V_0,V_1,V_2,O)=(0,1,1,0).
```

The shear contribution from `t s` is identically zero.  Indeed, write
`s=d h_1+e u_1`.  Against the `V_0` row `h_1`, the `V_2` row `u_0`,
and a central row in `span(h_0,h_1)`, its two possible blockwise
pairings contain either

```text
per(u_0,h_0 on e_0,e_1)=0
```

or too many rows supported on `span(e_2,e_3)`.  This is an exact
four-row permanent identity, not a target-coordinate change.

The remaining `c_1 u_0` term has two colour-one rows that vanish on
`e_2,e_3` and restrict to nonzero multiples of `u_0` on
`span(e_0,e_1)`.  The `V_0` colour-zero row is a nonzero multiple of
`h_1` on `span(e_2,e_3)`.  In the central colour-zero row, the `h_0`
component vanishes on that same plane, while the `h_1` coefficient in
(11) is nonzero.  Hence the four-mode permanent factors into

```text
per(u_0,u_0 on e_0,e_1)
per(h_1,h_1 on e_2,e_3)
  = 2*(-2) = -4,
```

times four nonzero scalars.  This forbidden mixed coefficient is
therefore nonzero, contradicting the requirement that `T_2` map to a
pure fourth power in target colour two.

Thus `C_+` is impossible.  Swapping majority colours gives the same
contradiction for `C_-`.  Equation (2) requires one of them, so the
exact star pattern (1) is impossible.

## Verification

Run:

```text
python verify_p5_q5_221_star_obstruction.py
python audit_p5_q5_221_star_obstruction.py
```

The primary verifier reconstructs the zero-diagonal determinant, the
`Q_12` support-two factor directions, the rank-one `Q_20` bilinear
factor, and the forced mixed `T_2` coefficient symbolically over `C`.
The independent audit expands the determinant and the decisive
four-mode permanent with a separate exact polynomial representation.
Neither replay searches row spaces or support masks.
