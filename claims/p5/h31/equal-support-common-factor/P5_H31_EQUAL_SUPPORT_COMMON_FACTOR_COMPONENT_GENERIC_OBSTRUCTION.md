# The eleventh component has no generic marked `H31` lift

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
marked-basis fibre over the generic point of the equal-support common-factor
component is empty for `H31`.

Together with the earlier component theorems, all eleven currently certified
pure-`P_4` component orbits are now generically closed for `H31`.  This does
not by itself close the eleventh component's weighted `H22` fibre; that fibre
is subsequently closed by the direct exact-zero-divisor identity in
[`P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h22/equal-support-common-factor/P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
Special parameter/projective boundaries, component exhaustiveness, and the
global Krenn--Gu conjecture remain open.

## The component and its intrinsic marked rows

Use the binary block notation

```text
a=X_0+X_1,        a_bar=X_0-X_1,
b=X_2+X_3,        b_bar=X_2-X_3                    (1)
```

and work over the component function field

```text
K=C(p,q,r).
```

The four planes from
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](../../../../P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md)
are

```text
U_0=span(u=a+p b,          v=a_bar+q b),
U_1=span(a,                a_bar+b),
U_2=span(a,                r a_bar+b),
U_3=span(b_bar,            a_bar).                  (2)
```

Put `R=r+1`.  The pure factor on mode zero has values proportional to

```text
u -> pR,              v -> 1+qR.
```

Therefore an intrinsic kernel/active pair is

```text
alpha_0=(1+qR)u-pR v,       beta_0=u.               (3)
```

For the other modes take

```text
alpha_1=a,       beta_1=a_bar+b,
alpha_2=a,       beta_2=r a_bar+b,
alpha_3=b_bar,   beta_3=a_bar.                      (4)
```

Every compatible marked basis is, up to row scaling,

```text
alpha_i,
beta_i(h)=beta_i+h_i alpha_i,

h=(h_0,h_1,h_2,h_3).                               (5)
```

The only nonzero pure coefficient in every marking is

```text
T_1111=-4p(r+1).                                    (6)
```

Thus the complete affine marking chart is the polynomial ring

```text
S=K[h_0,h_1,h_2,h_3].                              (7)
```

## The binary extension module

Delete source coordinate `d` and replace it by the fifth source coordinate.
The eight new row entries form an extension column

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3)^T.
```

Let

```text
M_d(h) z
```

be the fourteen mixed binary coefficients, and let `A_d(z),B_d(z)` be the
all-`alpha` and all-`beta(h)` binary diagonals.  Hence

```text
M_d in Mat_(14 x 8)(S),       A_d,B_d in S^(1 x 8). (8)
```

A genuine binary neighbour would require

```text
M_d z=0,             A_d(z)B_d(z)!=0.               (9)
```

Exact polynomial row-module reduction gives, for all four deleted
coordinates,

```text
A_d in Row_S(M_d),       B_d notin Row_S(M_d).       (10)
```

The reduced module sizes are

```text
d=0,1: 4 generators,
d=2,3: 8 generators.                                (11)
```

Unlike a generic determinant calculation, (10) is simultaneous in every
marking parameter, including every divisor on which the mixed rank changes.

## Why the membership is structurally visible

For the shared-support deletions,

```text
A_0=A_1=0                                           (12)
```

identically.  This is the squarefree shadow of the common exact zero divisor
`a a_bar=0`.

For `d=2`, a reduced module basis begins with

```text
g_-=(0,0,-1,-1,-1,h_3,h_0+1,0),
e_0,
e_1,
p e_2,
p e_3,
p e_4,                                               (13)
```

followed by two generators supported in coordinates `5,6,7`.  For `d=3`,
the same statement holds with

```text
g_+=(0,0,1,-1,-1,h_3,h_0+1,0).                     (14)
```

The all-kernel rows are

```text
A_2=(-2,-2Q,-2Q, 2p,0,0,0,0),
A_3=( 2, 2Q, 2Q, 2p,0,0,0,0),

Q=1+q(r+1).                                         (15)
```

Since `p` is a unit in `K`, equations (13)--(15) make the membership in
(10) immediate: the mixed module contains every standard basis row needed
to synthesize `A_2,A_3`.

Now any solution of the mixed equations satisfies

```text
A_d(z)=0,                                           (16)
```

contradicting (9).  The generic marked `H31` fibre is therefore empty before
any ternary-rank test.

## The asymmetric cokernel class

The all-active diagonal has nonzero module normal form in all four cases.
At the canonical marking and the rational component point `(p,q,r)=(1,2,2)`,
the mixed ranks are

```text
(4,4,7,7),                                          (17)
```

while adjoining `A_d` preserves those ranks and adjoining `B_d` raises them
to

```text
(5,5,8,8).                                          (18)
```

Thus the obstruction is not collapse of the entire extension map.  The
cokernel remembers the original all-active pure direction but kills its
opposite all-kernel Segre vertex.

This is the same module-level language used for the tenth component, with a
new exact-zero-divisor simplification.  Presentation modules and their
Fitting supports are organized abstractly in the
[Stacks Project, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6).
Here the direct row-module inclusion is stronger than a generic Fitting
minor: it holds over the whole marking chart.

## Proof boundary and next front

The theorem closes only the generic `H31` fibre of the eleventh component.
The suggested exact-zero-divisor continuation succeeds in
[`P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h22/equal-support-common-factor/P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md):
one weighted binary projection has identically zero all-kernel diagonal by a
two-channel permanent cancellation.  That later result is not part of the
present proof.

Special component parameters such as `p=0`, `r=0`, and the projective
boundary can change the marked module and remain open.  The existence of
further pure-`P_4` components and the global graph problem also remain open.

## Verification

Run:

```text
uv run --with sympy python claims/p5/h31/equal-support-common-factor/verify_p5_h31_equal_support_common_factor_component_generic_obstruction.py
uv run --with sympy python claims/p5/h31/equal-support-common-factor/audit_p5_h31_equal_support_common_factor_component_generic_obstruction.py
```

The primary verifier reconstructs (2)--(8), proves (12) and (15), and
computes the four polynomial row-module normal forms over
`C(p,q,r)[h_0,h_1,h_2,h_3]`.  The audit imports neither the marked-row nor
the extension-matrix constructor.  It reconstructs squarefree permanents by
subset dynamic programming and independently checks the complete all-marking
module at `(1,2,2)` and `(2,1,3)`.  These specializations are corroboration;
the primary function-field module calculation is the generic proof.
