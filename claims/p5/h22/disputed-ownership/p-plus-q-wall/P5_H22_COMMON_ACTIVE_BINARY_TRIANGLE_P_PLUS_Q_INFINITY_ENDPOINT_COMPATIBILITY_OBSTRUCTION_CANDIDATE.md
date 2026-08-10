# Verified compatibility obstruction on the off-wall component-14 endpoint

Discovery run report (before independent verification):

```yaml
role: construction
date_utc: 2026-08-01T11:15:30Z
git_commit: 7392ae7e7352a66fc5c42cb017d002043dfd794f
claim_label: CANDIDATE
scope: off-wall gamma=0 finite-D01 plus finite-D23,r=0 surviving pair on both marking axes
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_CANDIDATE.md: 7d81633da73dfac074d77408ebc118c452a8a7a067d3b2c95fa2f4fe8d14e456
method: independent complete kernels, shared-extension intersection, one fixed transverse minor, and one fixed stacked minor
command: uv run --with sympy python derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction.py
outputs:
  derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction.py: hash reported by replay
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: construction-side candidate pending independent replay; no on-wall, non-diagonal, arbitrary-order, or global claim
```

## Result

**VERIFIED exact obstruction.**  The two individually surviving axis-mode
maps do not form a common ternary weighted-`H22` lift.  Shared extension
variables force a single projective line.  On that line a previously
unchecked transverse `D01` marked map has rank four, and the full two-slice
axis-mode stack has rank five.

The independent verifier rebuilds both marking axes, complete mixed kernels,
the shared-extension intersection, all diagonal conditions, the `T=0` axis
intersection, and the two fixed rank witnesses without importing either
discovery derivation.  Its report is
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md`.

No finite field, grid, elimination, or broad minor scan is used.

## Common setup

On `gamma=0`, use

```text
e=(1,0,0,0),       w=(0,1,1,1),       u=(0,1,-1,0),
v1=(0,1,1,0),      v2=(0,0,0,1),

alpha=(e,e,-u,2v2-v1),
beta =(w,w,e,v1).
```

For the `h0` axis, mark `beta0` by `T alpha0`.  The `h1` axis is obtained by
marking `beta1` instead.  Let the finite `D01` slope be `s`, and use the
surviving finite `D23` slope `r=0`.  Their contraction rows in the full
five-coordinate reconstruction are

```text
q01=(1,s,0,0,0),          q23=(0,0,1,0,0).
```

## Complete shared extension

On the `h0` axis put

```text
k0=(-1,-1,0,-2T; 2T,T,1,0),
f =( 0, 0,1,  -1; 1,1,0,1).
```

Direct reconstruction gives

```text
ker M01=<k0>,              rank M01=7,
ker M23=<k0,f>,            rank M23=6.
```

The fixed rank witnesses are

```text
det M01[3,4,5,7,9,12,13 | 0,1,2,3,4,5,7]=-16s^6,
det M23[3,4,5,7,9,13    | 0,1,2,3,4,5]  =-4.
```

Thus a shared extension is necessarily

```text
z=C k0.
```

Its four binary diagonals are

```text
A01=-4Cs,          B01=4C(Ts+1),
A23= 4C,           B23=4CT.
```

The complete common genuine condition is therefore

```text
C s T (Ts+1) != 0.                                (1)
```

On the `h1` axis the same statements hold with

```text
k1=(-1,-1,0,-2T; T,2T,1,0).
```

The vector `f`, both rank witnesses, all four diagonal formulas, and (1)
remain unchanged.  These facts are rebuilt directly rather than inferred
only from the mode swap.

## Missed transverse rank-four obstruction

The original binary candidate checked the one-marked map in the active axis
mode; both `D01` and `D23` have rank exactly three there.  A ternary lift,
however, requires every one-marked contraction to factor through at most
three target columns.

On either axis, the `D01` mode-two map has the fixed rows `0127` determinant

```text
det N01,mode2[0127]
  =-32 C^3 s^2 (Ts+1).                            (2)
```

Every factor in (2) is nonzero under (1).  Hence this marked map has rank
four on every genuine shared pair.  This alone obstructs the ternary lift.

Projective rescaling `z -> lambda z` multiplies (2) by `lambda^3`; its
nonvanishing is independent of the chosen kernel normalization.

## Independent stacked compatibility obstruction

Extend the four marked `alpha,beta` rows by the same vector `Cki`.  For the
axis mode, independently reconstruct the two full `8 x 5` one-marked maps
obtained from contraction rows `q01` and `q23`, then stack them.

For both axes, stacked rows

```text
(0,6,7,8,14)
```

and all five source columns have determinant

```text
64 C^4 (Ts+1).                                    (3)
```

Thus the two individually rank-three projected neighbours combine to a
rank-five full two-slice map on (1), incompatible with a common ternary local
factorization.  Equation (3) is independent of the transverse obstruction
(2) and directly attacks the shared two-neighbour condition.

## Boundaries and retained failure

- At `T=0`, the shared line loses the `D23` beta diagonal; it is not a hidden
  common lift.
- At `s=0` or `Ts+1=0`, the `D01` line loses a required diagonal.
- The earlier mode-axis rank-three calculation was correct but insufficient;
  it is retained as a genuine binary survivor rather than reclassified as an
  error.
- The construction was promoted only after the fresh no-import verifier
  reproduced the complete frozen claim.
- The on-wall face, other component boundaries, non-diagonal source changes,
  arbitrary-order reduction, and the global Krenn--Gu conjecture are outside
  scope.

Replay:

```text
uv run --with sympy python \
  derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction.py

uv run --with sympy python \
  audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py
```
