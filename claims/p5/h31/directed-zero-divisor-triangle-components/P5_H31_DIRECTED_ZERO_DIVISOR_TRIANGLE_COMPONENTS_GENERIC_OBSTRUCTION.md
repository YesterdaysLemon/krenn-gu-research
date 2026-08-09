# Generic `H31` exclusion for components 16 and 17

## Status

**Exact characteristic-zero generic-fibre theorem.** The complete marked
`H31` fibre over the generic point of each directed-zero-divisor triangle
component—support-star component sixteen and support-path component
seventeen—is empty.

The proof treats every marked basis, every distinguished source coordinate,
and every projective extension direction.  It is a function-field theorem on
a dense open of each component.  Special parameter and projective component
boundaries, the weighted `H22` fibres, pure-`P_4` component exhaustiveness,
and the global Krenn--Gu conjecture remain open.

## Pure bases and the marked extension problem

Use the families in
[`P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md`](../../../p4/classifications/P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md).
Write their pure-factor bases as `(alpha_i,beta_i)`, with

```text
P_4|_(U_0 x ... x U_3)=lambda beta_0 beta_1 beta_2 beta_3,
lambda!=0.                                         (1)
```

For the star family these are the displayed rows.  For the path family only
mode zero changes:

```text
alpha_0=row_0+row_1,       beta_0=row_1.            (2)
```

Every marked basis on the same planes is

```text
beta_i(t)=beta_i+t_i alpha_i.                       (3)
```

For distinguished source coordinate `q`, replace that coordinate by the
fifth-source extension vector `z in K^8`, where `K=C(u,v)`.  Let

```text
M_q(t)z=0                                          (4)
```

be the fourteen mixed binary equations, and let `A_q(z),B_q(z)` be the two
diagonal coefficients.  A genuine neighboring `Delta_2` slice requires

```text
A_q(z) B_q(z) != 0.                                (5)
```

Normalize `A_q=1`, invert `B_q`, and eliminate `z`.  This is the open Fitting
incidence of the extension bundle, not a search through graphs.

## Eleven marked sheets, exactly

Over `K`, the complete projected ideals are:

| component | `q` | projected marking ideal |
|---|---:|---|
| star | 0 | `t3, u*t1-v*t2-v, t0, (t2+1)(v*t2+u+v)` |
| star | 1 | `t2, (u-v)t1+(1-u)t3+u-v, u*t0+v, t3(t3+1)` |
| star | 2 | `t3,t2,t1` |
| star | 3 | `t2+(v-1)(t3+1), t1, (u-1)t0+v-1, (t3+1)((v-1)t3+v-2)` |
| path | 0 | `t3,t2,t1` |
| path | 1 | unit ideal |
| path | 2 | `t3,t1,t0*t2` |
| path | 3 | `(u+v)t3+u+v-1, t2,t1,(u+v-1)t0+v-1` |

The verifier proves each equality in both directions.  Factoring the two
quadratics and `t0*t2` gives exactly

```text
star: six points and one line,
path: one point and three lines.                    (6)
```

There are no hidden marking sheets.

## Binary extension pencils are killed by two minors

On ten of the eleven sheets, the extension kernel is a projective line.
Choose the marked mode indicated by the verifier and two `4 x 4` minors of
its `8 x 4` one-marked map.  Their homogeneous binary gcd is

```text
R(u,v,h) A_q B_q,                                  (7)
```

where `R` is nonzero on the generic component open.  The seven isolated
sheet ratios `R` are

```text
-2,
2(u+v)^2/v,
2,
2,
-2/(u-1),
-2u(v-2)/(u-1),
2(u+v)(u+v-1).                                     (8)
```

The three path-line ratios are

```text
2,       -2h^2(u+v),       -2(u+v).                (9)
```

For the middle expression take `h!=0`; its `h=0` intersection is already on
the third line.  Over an algebraically closed field, two homogeneous binary
forms have a common projective zero exactly where their gcd vanishes.
Equations (5), (7)--(9) therefore force at least one marked minor to be
nonzero.  The marked map has rank four, but an `H31` lift would factor it
through a three-dimensional target local space.  Contradiction.

This is a useful small resultant argument: a potentially large marked
incidence becomes a gcd of two binary minors.

## The one projective-plane extension fibre

The star sheet at `q=2` is

```text
t1=t2=t3=0,       t0=h.                            (10)
```

Its extension kernel is projectively two-dimensional.  In exact kernel
coordinates `[z0:z1:z2]`, three mode-one minors, after removing the common
nonzero factor `A_2B_2`, are

```text
-2hu z0,       -2hu z2,       2hu z1.              (11)
```

For `h!=0`, simultaneous rank drop would force the zero projective vector.
At `h=0`, a mode-two minor is exactly

```text
-(v-1) A_2 B_2^2,                                 (12)
```

which is again nonzero on the genuine binary open.  Thus the only
higher-dimensional extension fibre is closed without elimination.

## Consequence and proof boundary

Every genuine binary neighbor on both generic components violates a marked
rank-three condition.  Therefore

```text
generic H31 fibre(component 16)=empty,
generic H31 fibre(component 17)=empty.              (13)
```

The result does not yet address `H22`, where three coupled normal directions
must be compared, nor does it turn generic component closure into a theorem
on every special boundary.

## Exact replay

```text
uv run --with sympy python claims/p5/h31/directed-zero-divisor-triangle-components/verify_p5_h31_directed_zero_divisor_triangle_components_generic_obstruction.py
python claims/p5/h31/directed-zero-divisor-triangle-components/audit_p5_h31_directed_zero_divisor_triangle_components_generic_obstruction.py
```

The primary verifier reconstructs all eight open Fitting projections over
`C(u,v)`, proves their displayed ideals bidirectionally, and checks every
binary-gcd and projective-plane minor identity.  The independent audit uses
subset-DP permanents and a complete small finite-field marking/extension
census as corroboration.  No graph or parameter search is used in the
characteristic-zero proof.
