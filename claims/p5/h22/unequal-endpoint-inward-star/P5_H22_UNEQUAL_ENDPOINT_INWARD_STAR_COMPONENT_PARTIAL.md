# Partial weighted `H22` obstruction on component twenty-five

## Status

**Exact characteristic-zero partial theorem.**  Over the function field of
component twenty-five, both homogeneous weight-at-infinity charts are empty.
On the finite `D01` pair orbit, a dense extension subchart is also empty,
uniformly in the finite weight.

The residual finite `D01` extension divisor and the finite `D23` pair orbit
remain **UNKNOWN**.  Therefore this note does not prove that the generic
weighted `H22` fibre is empty.  Special parameter divisors, projective
component-boundary fibres, and the arbitrary-order local-to-global reduction
also remain open.  Pure-`P_4` component exhaustiveness is now proved
separately and does not close these fibres.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Exact component field and pure basis

Put

```text
P=ej+k^2,       Q=e+j,
F=P(1+ejs^2)-Q^2,
K=C(e,j,s)[k]/(F).                                  (1)
```

Use the intrinsic basis from the generic marked-`H31` theorem:

```text
alpha_0=Q A-P B,                 beta_0=A,
alpha_1=Q(A+kD)-P(B+sC),         beta_1=A+kD,
alpha_2=C,                       beta_2=A+eB-kD,
alpha_3=D,                       beta_3=A-sjC+jB.     (2)
```

Before quotienting by `F`, its only nonzero pure coefficients are

```text
T_0011=4PF,        T_1111=4P.                       (3)
```

Thus only `T_1111=4P` survives over `K`.

## The marking-free fixed-vertex equations

Let `C_w(z)` be the sixteen canonical binary coefficients of a weighted
extension.  If some marking

```text
beta_i(h)=beta_i+h_i alpha_i
```

makes the extension a genuine binary `Delta_2`, then after normalizing
`C_0000=1`, the fifteen coordinates other than the free opposite diagonal
lie in the fixed-vertex Segre join.  In particular,

```text
C_1100=C_1000 C_0100,
C_1001=C_1000 C_0001,
C_1101=C_1000 C_0100 C_0001.                       (4)
```

These necessary equations eliminate all four marking parameters.

## A uniform finite-`D01` dense obstruction

For finite homogeneous weight `[lambda:1]`, the `D01` contraction is

```text
(x,e) -> (lambda x_0+x_1,x_2,x_3,e).               (5)
```

In extension coordinates

```text
z=(z_0,z_1,z_2,z_3;z_4,z_5,z_6,z_7),
```

put

```text
L_01=(lambda+1)z_2+(lambda-1)z_4.                  (6)
```

Direct polynomial identities, valid before quotienting by `F`, give

```text
C_1101=0,
C_1000=Q C_1100,
k C_1001=jP C_1100,
C_1100=-2k L_01.                                   (7)
```

On the generic component field, `P,Q,j,k` are units.  If `L_01 != 0`, then
`C_1100 != 0`.  The first two equations in (4) and (7) force

```text
C_0100=1/Q,       C_0001=jP/(kQ).                  (8)
```

The last equation in (4) would then read

```text
0=C_1101=jP C_1100/(kQ),                           (9)
```

a contradiction.  Hence every finite `D01` candidate is forced onto the
explicit residual extension divisor

```text
L_01=0.                                            (10)
```

This is uniform in `lambda`, including `lambda=1` and `lambda=-1`; no
finite weight divisor was inverted.

## Both weight-at-infinity charts are empty

At `[1:0]`, the two pair orbits become

```text
D01: (x,e) -> (x_0,x_2,x_3,e),
D23: (x,e) -> (x_0,x_1,x_2,e).                    (11)
```

These are entry-by-entry the marked-`H31` deletion models for source
coordinates one and three.  Over

```text
K[h_0,h_1,h_2,h_3],
```

exact quotient-ring row-module reduction gives

```text
chart              D01 infinity    D23 infinity
deleted coordinate       1               3
module size              10              12
NF(all-alpha)             0               0
NF(all-beta)           nonzero         nonzero.     (12)
```

Thus the mixed equations force the required all-alpha diagonal to vanish in
both infinity charts.  Neither supports a genuine binary neighbour.

## Exact residual and failed route ledger

The remaining weighted problem over the generic component field is exactly:

```text
finite D01 on L_01=0,        and        finite D23. (13)
```

Full eleven-generator fixed-vertex Segre-join reductions and a direct
finite-slope marked row-module reduction exceeded bounded replay windows.
Those timeouts are not proof evidence and are not used in (7)--(12).

The basis chart uses `P != 0`; treating (1) as a quadratic extension also
uses `1+ejs^2 != 0`.  The dense argument additionally treats `Qjk != 0`.
Their special fibres and all projective component-boundary fibres remain
unclassified.  No finite-field computation is used as proof.

## Replay

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star/verify_p5_h22_unequal_endpoint_inward_star_component_partial.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star/audit_p5_h22_unequal_endpoint_inward_star_component_partial.py
```

The primary verifier reuses the certified hypersurface-function-field model,
checks (3) and all four identities in (7), proves the localized three-equation
Segre contradiction exactly, identifies both infinity contractions with the
corresponding `H31` matrices, and replays their quotient-ring modules.  The
audit imports no project code, reconstructs permanents by subset dynamic
programming, and independently repeats the polynomial identities and both
quotient-ring reductions.
