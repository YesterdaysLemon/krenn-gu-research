# Projective boundary of the common-active `(2,1,1)` triangle

## Status

**Exact characteristic-zero classification theorem.**  Consider a nonzero
pure `P_4` restriction whose exceptional triangle on modes `1,2,3` has
relation-rank word `(2,1,1)` and common-active orientation

```text
y_1 x_3=0,       y_2 x_3=0,
y_1 x_2-x_1 y_2=0.                                  (1)
```

Assume the shared exact pair in (1) has genuine two-coordinate support.  The
dense complementary-binary chart is classified in
[`P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md`](../../../../../P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md).
This theorem closes every omitted projective boundary of that chart:

1. a vanishing synchronized complement has pair image of dimension at most
   one;
2. a vanishing third-plane complement is zero or lies in the closure of
   component eleven;
3. a coordinate-supported synchronized complement has no nonzero pure
   survivor;
4. a full synchronized complement and coordinate-supported third-plane
   complement lies in the closure of one of the two component-twelve
   polarity sheets.

Consequently the complete common-active, genuine-support-two orientation is
exhausted by known component or lower-pair closures.  This does **not** close
the other common-kernel/projective orientations of the `(2,1,1)` triangle,
the two open star cells, special `P_5` fibres, the arbitrary-order reduction,
or the global Krenn--Gu conjecture.

## Homogeneous normal form

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and normalize the shared exact pair to

```text
a=X_0+X_1,       c=X_0-X_1,       ac=0.             (2)
```

The legal Borel synchronization from the dense theorem gives

```text
U_1=<a,m>,       U_2=<a,m_r>,       U_3=<d,c>,

m=beta*c+s,     m_r=m+rho*c,
d=gamma*a+delta*c+t,                                (3)
```

where `s,t` lie in `B=<X_2,X_3>` and are now allowed to vanish or meet the
coordinate boundary.  Let

```text
C_0=a^2 d,       C_1=a m d,       C_2=m m_r d,
X=m m_r c.                                             (4)
```

A pure opposite plane exists precisely when

```text
dim W<=2 and X notin W,       W=<C_0,C_1,C_2>.       (5)
```

Indeed `Ann_R1(W)` must contain the opposite two-plane, and `X` must remain
nonzero on it.  This is the projective escape condition; a rank condition
alone is insufficient.

For

```text
s=uX_2+vX_3,       t=pX_2+qX_3,
A=uq+vp,           Q=uq-vp,       E=(2beta+rho)A,   (6)
```

the four maximal minors of the `4 x 3` matrix in (4) are

```text
 4q A(E+2delta uv),
 4p A(E+2delta uv),
-4(gamma-delta)Q(E-2gamma uv),
 4(gamma+delta)Q(E+2gamma uv).                      (7)
```

Equation (7) is polynomial on the entire affine cone over
`P(B) x P(B)` and remains valid on every boundary considered below.

## Vanishing complements

If `s=0`, then `U_1U_2` is spanned by `a^2` because both planes equal
`<a,c>` after removing dependent rows.  Hence

```text
dim(U_1U_2)<=1,                                    (8)
```

outside the all-pair frontier.

Let `t=0`.  If `d` is proportional to `c`, the third plane is not a plane;
otherwise replace `d` by `a`.  If `s` is coordinate-supported, direct
calculation gives `X in W` (or `X=0`), so the restriction is zero.  If
`s=X_2+kX_3` with `k!=0`, then

```text
W=<a^2s, m m_r a>,       rank W=2,
Ann_R1(W)=<c,s_bar>,       s_bar=X_2-kX_3,           (9)
```

and the unique opposite plane is `<s_bar,c>` in kernel/active order.  After
swapping modes zero and three the four planes are

```text
V_0=<a,c>,
V_1=<a,beta*c+s>,
V_2=<a,(beta+rho)c+s>,
V_3=<s_bar,c>.                                      (10)
```

For a formal parameter `zeta!=0`, replace the middle planes by

```text
V_1(zeta)=<a,zeta*c+s>,
V_2(zeta)=<a,(zeta+rho)c+s>.                        (11)
```

After the diagonal source scaling
`diag(zeta,zeta,1,k)`, equation (11) is exactly the component-eleven normal
form with `p=q=0` and `r=(zeta+rho)/zeta`.  Its Pluecker points converge to
(10) as `zeta -> 0`.  Thus the complete nonzero `t=0` fibre lies in the
component-eleven closure, including `beta=0` and all special `rho`.

## A coordinate-supported synchronized complement

Normalize `s=X_2`.  If `t` is proportional to `X_2`, all columns in (4) and
`X` lie on one degree-three coordinate line, with `X in W`.  If

```text
t=X_2+kX_3,       k!=0,                             (12)
```

one maximal minor and the desired cubic are

```text
4k^3(2beta+rho),       X=-2(2beta+rho)X_0X_1X_2.   (13)
```

Therefore `rank W<=2` forces `2beta+rho=0`, which makes `X=0`.  The endpoint
`t=X_3` has the same conclusion with minor `4(2beta+rho)`.  No nonzero pure
tuple occurs on this whole projective line.

## A coordinate-supported third-plane complement

It remains to take

```text
s=X_2+kX_3,       k!=0,       t=X_2,
B_0=2beta+rho.                                      (14)
```

The nontrivial minors in (7) reduce to

```text
4k^2(B_0+2delta),
-4k^2(delta-gamma)(B_0-2gamma),
-4k^2(delta+gamma)(B_0+2gamma).                     (15)
```

Hence `rank W<=2` is equivalent to

```text
delta=-B_0/2,       gamma=+delta or gamma=-delta.   (16)
```

The selected `2 x 2` minor `-2k` keeps `rank W=2` on both branches, so the
opposite kernel plane varies regularly.  Put

```text
t_epsilon=X_2+epsilon X_3,
delta_epsilon=-B_0(k+epsilon)/(2k),
gamma_epsilon=+delta_epsilon or -delta_epsilon.     (17)
```

Over `C((epsilon))`, both `t_epsilon` and `s` have full support and
`A=k+epsilon`, `Q=epsilon-k` are units.  Equations (7) vanish identically,
so (17) is exactly one of the two dense component-twelve polarity sheets.
At `epsilon=0` it specializes to (16).  Regularity of the rank-two kernel
therefore places every boundary opposite plane in the component-twelve
closure.  The `t=X_3` endpoint is source-symmetric.

## Consequence

The dense theorem and (8)--(17) give a projectively complete ledger:

```text
s,t full                     -> components 11 or 12 (dense theorem),
s=0                          -> lower pair rank,
t=0                          -> component 11 or zero,
s coordinate, t nonzero      -> zero,
s full, t coordinate         -> component 12.       (18)
```

No parameter search, finite-field inference, or solver exit code is used.
The remaining `triangle-(2,1,1)` work is outside this common-active
orientation and remains **UNKNOWN**.

## Exact replay

```text
uv run --with sympy python claims/p4/classifications/triangle-211/common-active-211-triangle-projective-boundary/verify_p4_common_active_211_triangle_projective_boundary_classification.py
uv run --with sympy python claims/p4/classifications/triangle-211/common-active-211-triangle-projective-boundary/audit_p4_common_active_211_triangle_projective_boundary_classification.py
```

The primary verifier reconstructs (4)--(17), the escape condition, the
component-eleven valuative placement, and both component-twelve arcs.  The
independent audit reimplements squarefree multiplication and plane Pluecker
coordinates without importing the primary verifier.
