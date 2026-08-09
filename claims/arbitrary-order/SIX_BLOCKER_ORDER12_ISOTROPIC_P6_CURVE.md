# The order-twelve maximal-overlap slice contains an isotropic `P_6` curve

## Status

**Exact characteristic-zero order-twelve structural theorem.**  Suppose a
hypothetical twelve-vertex Krenn--Gu witness contains two five-root,
six-blocker first-surplus configurations with four common roots and the same
blockers.  If the exchanged roots have nonzero mutual coupling, the two
exchanged root/port planes carry a diagonal cross form.  Its isotropic locus
is a projective `(1,1)` curve.  Every fully supported point on that curve is
a genuine six-root restriction

```text
P_6 -> Delta_3.
```

When the remaining diagonal cross value is nonzero, this gives a smooth
rational curve joining the two original mixed root/port restrictions.  When
it is zero, the curve splits into two rulings and the double-port corner is
itself an additional `P_6 -> Delta_3` restriction.

The theorem also proves that the exact rational local model in
[`SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md`](SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md)
cannot extend to an order-twelve global witness, regardless of how its
blocker--blocker edge blocks are chosen.  This is not a Krenn--Gu
counterexample and it does not exclude the remaining `P_6` curves.  The
arbitrary-order residual-vertex problem remains **UNKNOWN**, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

## The exchanged planes and their cross form

Use

```text
I={0,1,2,3},       R=I union {a},       R'=I union {b},
B={u_0,...,u_5}
```

on exactly twelve vertices.  Let `z_b` be the torus port for `R` and `z_a`
the torus port for `R'`.  Put

```text
beta=B_ab(x_a,x_b) != 0,       delta=B_ab(z_a,z_b),
X_a=span{x_a,z_a},             X_b=span{x_b,z_b}.       (1)
```

Nonzero `beta` makes both displayed pairs independent.  Every common-root
incident covector annihilates both vectors in the corresponding plane:

```text
B_ia(x_i,X_a)=0,       B_ib(x_i,X_b)=0       (i in I).  (2)
```

The two port conditions also give

```text
B_ab(x_a,z_b)=0,       B_ab(z_a,x_b)=0.                 (3)
```

Therefore, in the ordered bases `(x_a,z_a)` and `(x_b,z_b)`, the restriction
of the cross edge is

```text
B_ab|_(X_a x X_b) = diag(beta,delta).                   (4)
```

## One shared blocker--blocker cofactor

For `y_a in X_a`, `y_b in X_b`, and free blocker vectors `z_u`, let
`Pi(y_a,y_b)` be the pullback of `P_6` through the six local maps whose rows
are

```text
B_iu(x_i,-)  (i in I),       B_au(y_a,-),       B_bu(y_b,-).       (5)
```

Define the four-root blocker--blocker cofactor tensor

```text
C_I(z_B)
 =sum_({u,v} subset B)
    B_uv(z_u,z_v)
    per([B_iw(x_i,z_w)]_(i in I,w in B\{u,v})).         (6)
```

After fixing the four common roots and `y_a,y_b`, every surviving matching
has exactly one of two forms:

1. all six vertices `I,a,b` pair bijectively with the six blockers, giving
   `Pi(y_a,y_b)`;
2. `a` pairs with `b`, four blockers pair with `I`, and the remaining two
   blockers pair together, giving `B_ab(y_a,y_b) C_I`.

There are no other cases by (2).  Hence the full matching identity is

```text
Pi(y_a,y_b)+B_ab(y_a,y_b) C_I
 =D(y_a,y_b),                                           (7)

D(y_a,y_b)
 =sum_(c=0)^2 d_c y_a[c]y_b[c] product_(u in B)z_u[c],
d_c=product_(i in I)x_i[c].                            (8)
```

The same tensor `C_I` occurs for every point of `X_a x X_b`.

## The four corners

Write

```text
Pi_00=Pi(x_a,x_b),       Pi_01=Pi(x_a,z_b),
Pi_10=Pi(z_a,x_b),       Pi_11=Pi(z_a,z_b),            (9)
```

and use the same subscripts for `D`.  Equations (3)--(7) give

```text
Pi_00+beta C_I=D_00,       Pi_01=D_01,
Pi_10=D_10,                Pi_11+delta C_I=D_11.       (10)
```

Thus `Pi_01` and `Pi_10` are exactly the two original `P_6` restrictions.
Eliminating the shared cofactor gives the additional diagonal-corner
compatibility

```text
beta(Pi_11-D_11)=delta(Pi_00-D_00).                    (11)
```

Equation (11) does not impose another direct relation between `Pi_01` and
`Pi_10`; it explains precisely where the blocker--blocker information lives.

There is also a basis-free quotient formulation.  Let `mathcal D` be the
three-dimensional GHZ diagonal subspace of the six-blocker tensor space and
write a bar for reduction modulo `mathcal D`.  Equation (7) says

```text
bar(Pi):X_a tensor X_b -> Tensor(B)/mathcal D,
bar(Pi)=-[C_I] tensor (B_ab|_(X_a x X_b)).             (12)
```

In particular `rank(bar(Pi))<=1`, and every decomposable isotropic vector
for the cross form maps into `mathcal D`.  This quotient-rank-one statement
is the intrinsic content of the four corner equations.

## The isotropic rational curve

For an affine parameter `t`, set

```text
y_a(t)=x_a+t z_a,
y_b(t)=delta t x_b-beta z_b.                           (13)
```

By (4),

```text
B_ab(y_a(t),y_b(t))=beta delta t-delta beta t=0.       (14)
```

The four roots in `I` are zero-coupled to both vectors by (2).  Outside a
finite set of values of `t`, every coordinate of both vectors is nonzero.
For those `t`, the six vectors

```text
(x_i)_(i in I), y_a(t), y_b(t)
```

are fully supported and pairwise zero-coupled.  Equation (7) becomes

```text
Pi_t=D_t,                                               (15)

Pi_t
 =-beta Pi_01+t(delta Pi_00-beta Pi_11)+delta t^2 Pi_10.             (16)
```

The three diagonal coefficients in `D_t` are nonzero away from another
finite set, so conciseness forces every one of the six local maps in (5) to
have rank three.  Thus every such `t` gives a genuine `P_6 -> Delta_3`
restriction.

If `delta != 0`, the zero locus of (4) in `P(X_a) x P(X_b)` is a smooth
`(1,1)` curve.  Formula (13) parametrizes it; `t=0` is the `Pi_01` endpoint
up to scale, while `t=infinity` is the `Pi_10` endpoint up to scale.  If
`delta=0`, the isotropic locus is the union of two rulings.  The ruling with
`y_b=z_b` contains `Pi_01` and `Pi_11`, and (10) immediately yields

```text
Pi_11=D_11.                                             (17)
```

The target coefficient curve has the three frame vectors

```text
v_01=x_a hadamard z_b,
v_10=z_a hadamard x_b,
v_m=delta(x_a hadamard x_b)-beta(z_a hadamard z_b).    (18)
```

Indeed its coefficient polynomial, before multiplication by the fixed torus
vector `d`, is

```text
-beta v_01+t v_m+delta t^2 v_10.                       (19)
```

For `delta!=0`, the conic spans the full GHZ diagonal plane exactly off the
frame divisor

```text
Theta=det(v_01,v_10,v_m)=0.                            (20)
```

For `delta=0`, the same determinant measures the span of the two isotropic
rulings together.  Thus `Theta!=0` and `Theta=0` are the exact first split
for any frame-orbit or projected-Veronese attack on this synchronized family.

## The earlier local model cannot globalize at order twelve

In the rational local model of the port-freedom theorem,

```text
x=(1,1,1),       z_a=(1,2,3),       z_b=(1,3,2),
W_ab=alpha_a alpha_b^T,
alpha_a(z_a)=alpha_b(z_b)=0.
```

Therefore `beta=1` and `delta=0`.  Its double-port permanent `Pi_11` has
exact coefficient

```text
[z_0^0 z_1^0 z_2^0 z_3^0 z_4^0 z_5^1] Pi_11=18.       (21)
```

This is an off-diagonal blocker word, so the corresponding coefficient of
`D_11` is zero.  Equations (17) and (21) contradict each other.  Because the
cofactor is multiplied by `delta=0` at this corner, no choice of any
blocker--blocker edge can repair the failure.  The model remains a valid
local independence certificate, but it is now exactly excluded as an
order-twelve global realization.

## Exact residual

The maximal-overlap order-twelve problem is reduced to a synchronized family,
not solved:

```text
delta=0: an additional double-port P_6 restriction is forced;
delta!=0: a smooth rational curve of P_6 restrictions is forced;
classification or exclusion of such synchronized P_6 curves: UNKNOWN;
ambient orders with residual vertices: governed by the separate GHZ
  hypercube theorem, but not reduced to the same curve;
global Krenn--Gu conjecture: UNRESOLVED.
```

The next useful finite target is therefore not a single unrestricted `P_6`
point.  It is a rational curve of `P_6` pullbacks sharing four fixed rows and
coming from two bilinear row pencils.

## Replay

```text
uv run --with sympy python verify_six_blocker_order12_isotropic_p6_curve.py
uv run --with sympy python audit_six_blocker_order12_isotropic_p6_curve.py
```

The primary verifier checks the exact matching partition, the four-corner
elimination, the isotropic parametrization, and the off-diagonal coefficient
`18` in the local model.  The no-import audit uses an independent weighted
hafnian decomposition, alternate symbolic scalars, and a separate subset
permanent.  No finite-field inference is used.
