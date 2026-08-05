# Projective completion of the common-kernel `YY` `(2,1,1)` triangle

## Status

**Exact characteristic-zero classification theorem.**  Consider the
common-kernel `YY` orientation

```text
y_1y_3=0,       y_2y_3=0,
y_1x_2-x_1y_2=0                                  (1)
```

in the `triangle-(2,1,1)` cell.  The dense complementary-binary torus is
empty by
[`P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md`](P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md).
This theorem classifies its complete projective boundary:

- a vanishing or coordinate-supported synchronized complement is lower-pair
  or a coordinate embedded-`P_3` suspension;
- every nonzero third-plane complement is covered by the dense polarity
  obstruction;
- the sole full-support survivor with vanishing third-plane complement is a
  unique apolar tuple in the closure of component thirteen.

Thus the full `YY` flag orbit produces no new component.  This does not close
the unequal common-kernel `CC` orbit, either star cell, the remaining special
`P_5` fibres, the arbitrary-order reduction, or the global Krenn--Gu
conjecture.

## The common-kernel normal form

Put

```text
a=X_0+X_1,       c=X_0-X_1,       ac=0,

m=beta*c+s,       m_r=m+r*c,
d=gamma*a+delta*c+t,                               (2)
```

where `s,t in <X_2,X_3>`.  The three displayed planes are

```text
U_1=<a,m>,       U_2=<a,m_r>,       U_3=<c,d>.     (3)
```

The kernel-rich cubic span and desired active cubic are

```text
W=<C_0,C_1,C_2>,
C_0=a^2d,       C_1=amd,       C_2=m m_r c,
X=m m_r d.                                           (4)
```

A nonzero opposite plane requires `dim W<=2` and `X notin W`.

Write

```text
s=uX_2+vX_3,       t=pX_2+qX_3,
A=uq+vp,       Q=uq-vp,       E=(2beta+r)A.         (5)
```

The exact maximal minors are

```text
8quvA,       8puvA,
4Q(E-2gamma uv),       4Q(E+2gamma uv).             (6)
```

## Nonzero third-plane complements

Assume first `uv!=0` and `t!=0`.  At least one of `p,q` is nonzero, so the
first two equations in (6) force `A=0`.  The polar partner of a full-support
binary form is again full-support; hence `Q!=0`, and the last two equations
force `gamma=0`.  Then `st=0` and

```text
C_0=a^2t,       C_1=0,       C_2=m m_r c,

X=delta*C_2-beta(beta+r)C_0 in W.                  (7)
```

There is no nonzero pure escape.  This argument includes coordinate endpoints
of `t`; it requires only `t!=0`, not `pq!=0`.

Let `s` be coordinate-supported, say `s=X_2`.  If `q!=0`, the last two
minors in (6) force `2beta+r=0`.  Then

```text
U_1U_2 subset <a^2,aX_2>,                           (8)
```

so the synchronized edge has rank at most two.  If `q=0`, all rows in (3)
lie in the coordinate hyperplane `<X_0,X_1,X_2>`; every nonzero pure tuple
is therefore in the embedded-`P_3` closure.  The case `s=0` has even smaller
pair rank.

## The unique `t=0` survivor

It remains to take `s` full-support and `t=0`.  Normalize

```text
b=X_2+X_3,       b_bar=X_2-X_3.                    (9)
```

Plane independence forces `gamma!=0`, so shifting by `c` and scaling gives
`d=a`.  Direct multiplication yields

```text
C_0=0,
C_1=a^2b,
C_2=-(2beta+r)a^2b+c b^2.                          (10)
```

The two displayed monomial supports are independent, so

```text
rank W=2,
Ann_R1(W)=<a,b_bar>,
X=a b^2 notin W.                                   (11)
```

There is no rank-one-`W` vertical fibre.  The opposite plane is uniquely
`<b_bar,a>` in kernel/active order, and the four-tuple is

```text
U_0=<b_bar,a>,
U_1=<a,beta*c+b>,
U_2=<a,(beta+r)c+b>,
U_3=<c,a>.                                         (12)
```

Its only nonzero restricted coefficient is

```text
T_1111=4.                                           (13)
```

All pair ranks are at least three.  Generically the profile is
`(4,4,3,3,3,3)`; `r_01` or `r_02` may drop from four to three at
`beta=0` or `beta+r=0`, but never below three.

## Exact component-thirteen arc

Let `zeta^2+zeta+1=0` and put

```text
K=3beta^2+3beta*r+r^2,
V_0=zeta-zeta^2,
U_epsilon=epsilon^2 K/V_0,

gamma_epsilon=(V_0-U_epsilon)/V_0,
alpha_epsilon=U_epsilon+zeta*gamma_epsilon.         (14)
```

Then

```text
alpha_epsilon^2+alpha_epsilon*gamma_epsilon
 +gamma_epsilon^2
 -3(epsilon beta)^2-3(epsilon beta)(epsilon r)
 -(epsilon r)^2=0.                                  (15)
```

Thus `(alpha_epsilon,epsilon beta,epsilon r,gamma_epsilon)` lies on the
component-thirteen Eisenstein norm quadric.  Apply the source arc

```text
D_epsilon=diag(1,1,epsilon,epsilon).                (16)
```

The component-thirteen planes have exact leading wedges

```text
U_1(epsilon): epsilon*(beta*c+b) wedge a,
U_2(epsilon): epsilon*((beta+r)c+b) wedge a,

U_3(epsilon) -> <c,a>,
U_0(epsilon) -> <b_bar,a>,                          (17)
```

because `alpha_epsilon+gamma_epsilon -> zeta+1!=0`.  Hence their Grassmann
points converge to (12).  The marked component basis becomes singular, but
the plane-locus arc and the directly verified tensor (13) are regular; no
illegal kernel-preserving row move is used.

## Consequence

Combining (6)--(17) gives

```text
s full, t nonzero       -> zero by polarity,
s coordinate            -> lower pair or embedded P_3,
s full, t=0             -> component 13,
s=0                     -> lower pair.              (18)
```

The common-kernel `YY` orientation is therefore projectively complete.  The
global conjecture remains **UNRESOLVED**.

## Exact replay

```text
uv run --with sympy python verify_p4_common_kernel_yy_211_triangle_projective_classification.py
uv run --with sympy python audit_p4_common_kernel_yy_211_triangle_projective_classification.py
```

Both scripts use exact squarefree multiplication over `Q(zeta)` with
`zeta^2+zeta+1=0`.  The audit imports nothing from the primary verifier and
uses no finite field or parameter search.
