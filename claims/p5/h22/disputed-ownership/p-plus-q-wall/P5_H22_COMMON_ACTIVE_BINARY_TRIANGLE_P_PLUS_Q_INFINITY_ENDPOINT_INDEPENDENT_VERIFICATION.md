# Independent verification of the original component-14 endpoint analysis

```yaml
role: verifier
date_utc: 2026-08-01T11:37:53Z
git_commit: ab1c3d7f12c47e3a817af86464ab66786b3d9a43
claim_label: REFUTED
scope: original one-neighbour component-14 infinity-endpoint analysis in P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_CANDIDATE.md; the later two-neighbour compatibility theorem is excluded
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_CANDIDATE.md: 19501c093f8a502346d80aa87a52015571a4842a3e1a473be35c0f0c9eb33f3a
method: independent squarefree subset-DP permanents, bidirectional characteristic-zero elimination, direct complete kernels at every exceptional slope, and exhaustive fixed one-marked minors
command: uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate_verifier.py
outputs:
  audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate_verifier.py: 0319d7144dc00599d4e8179bb0ab986927b7258f516503194c6f440e48ec97ad
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INDEPENDENT_VERIFICATION.md: hash reported by replay
limitations: the later compatibility obstruction is deliberately not read or used; this audit makes no arbitrary-order, component-exhaustiveness, prize-graph, or global Krenn-Gu claim
```

## Scoped verdict

The original note is **REFUTED as written**, but its central geometric boundary
survives the audit:

- **Verified:** both endpoint plane tensors and all eight projective marking
  projections.
- **Verified:** the `gamma=2` on-wall face has no weighted-`H22` lift because
  every finite or infinite `D01` direction is one-marked rank-four obstructed,
  while `D23` infinity is empty.
- **Verified:** the `gamma=0` off-wall finite-`D01` survivor, complete
  finite-`D23` factor cover, simple `D23(r=0)` shared-pair frame, and exact
  mode-axis swap.
- **Refuted:** at off-wall `D23` slope `r=1/2`, not every genuine kernel point
  has marked rank exactly three.  The genuine subfamily `Y=0,T!=0` has rank
  exactly two.

The correction does not remove or add any survivor: rank two is still below
the rank-four obstruction threshold.  In this deliberately restricted audit,
the off-wall pair therefore remains a binary survivor.  Nothing here evaluates
the later two-neighbour compatibility theorem.

## Independent reconstruction

The verifier rebuilds, without importing the target derivation or any helper,

```text
e=(1,0,0,0), w=(0,1,1,1), u=(0,1,-1,0),
v1=(0,1,1,0), v2=(0,0,0,1),

alpha=(e,e,-u,2v2-v1),
beta =(w,w,e,gamma e+v1),
```

for `gamma=0,2`.  A squarefree subset dynamic program, rather than a
permutation sum, gives the sole pure coefficient

```text
T_1111=4
```

in both cases and zero for the other fifteen words.

For every marking and all four projective directions, the script reconstructs
the fourteen mixed coefficients and both diagonals from

```text
D01^[rho:sigma](z,x)=(rho z0+sigma z1,z2,z3,x),
D23^[rho:sigma](z,x)=(z0,z1,rho z2+sigma z3,x).
```

Bidirectional Gröbner reduction verifies the following normalized projection
ideals, both after eliminating the finite slope and while retaining it:

| endpoint | direction | exact projected ideal |
| --- | --- | --- |
| `gamma=0` | finite `D01` | `<h3,h2,h0 h1>` |
| `gamma=0` | infinite `D01` | `<h3,h2,h0 h1>` |
| `gamma=0` | finite `D23` | `<h3,h2,h0 h1>` |
| `gamma=0` | infinite `D23` | `<1>` |
| `gamma=2` | finite `D01` | `<h3,h2,h0 h1>` |
| `gamma=2` | infinite `D01` | `<h3,h2,h0+h1,h1^2>` |
| `gamma=2` | finite `D23` | `<h3,h2,h0 h1>` |
| `gamma=2` | infinite `D23` | `<1>` |

Thus the two finite marking axes are complete and there is no hidden
slope-marking equation.  Swapping tensor modes zero and one together with
extension coordinates `(z0 z1)(z4 z5)` is checked coefficient by coefficient
for both endpoints and all four directions.  It exchanges the two axes
exactly, so it suffices below to audit `h=(T,0,0,0)`.

## On-wall `gamma=2`: verified obstruction

For finite `D01`, the independent rank-seven witness is

```text
64 r^6(Tr+1).
```

On its open set the complete kernel line has diagonals

```text
A=-2Xr/(Tr+1),              B=2X(2r+1).
```

The exact marked-mode-zero cover is

```text
T!=0, rows 0457:
  -16 T X^3 r^2(2r+1)/(Tr+1)^2,

T=0, rows 0567:
  -8 X^3 r(2r+1).
```

Every divisor suppressed by that frame was rebuilt directly:

- `r=0`: the complete kernel is killed by `A`;
- `r=-1/2`: the complete kernel is killed by `B`;
- `Tr+1=0`: the complete kernel is killed by `B`;
- their intersection `r=-1/2,T=2` is included in the direct rebuild.

At `D01` infinity, the projected ideal forces the origin.  The complete
rank-six frame is

```text
v0=(-1,-1, 2, 2;-2,-2,1,0),
v1=( 0, 0,-1,-1; 1, 1,0,1).
```

For `z=Xv0+Yv1`,

```text
A=-4X, B=4Y,
det N2[0127]=-32X^2Y.
```

The determinant is nonzero on the genuine locus.  Since `D23` infinity has
unit projected ideal, every on-wall projective pair encounters one of these
finite or infinite `D01` obstructions.  The on-wall empty-fibre conclusion is
therefore **VERIFIED** within the stated local scope.

## Off-wall `gamma=0`: verified `D01` survivor

At `D01` infinity, the complete frame

```text
v0=(-1,-1,0,-2T;2T,T,1,0),
v1=( 0, 0,-1,-1; 1,1,0,1)
```

gives

```text
A=-4X, B=4(TX+Y),
det N2[0127]=-32X^2(TX+Y).
```

Thus infinity is obstructed.

At finite slope `s`, the witness and complete kernel are

```text
-16s^6,
k=(-1,-1,0,-2T;2T,T,1,0).
```

For `z=Ck`,

```text
A=-4Cs, B=4C(Ts+1).
```

The direct `s=0` kernel is killed by `A`, and the direct `Ts+1=0`
kernel is killed by `B`.  On the genuine open, every marked-mode-zero
`4 x 4` minor vanishes, while

```text
det N0[rows 067, columns 012]=-16C^3(Ts+1)
```

is nonzero.  Hence the map has rank exactly three throughout the genuine
finite-`D01` family, as claimed.

## Off-wall finite `D23`: complete factor cover

On the ordinary chart the independent rank-six witness is

```text
-4(2r-1)^2(2r+1)(4r+1).
```

For a complete two-vector kernel frame `z=Xv0+Yv1`, the verifier obtains

```text
A=4X,
B=4(r+1)[TX(2r+1)+Y(r+1)]/(4r+1),

det N0[0167]
=32XYr(r+1)(2r-1)[TX(2r+1)+Y(r+1)]
  /[(2r+1)(4r+1)].
```

Therefore an ordinary genuine point is rank-four unless `Y=0`, `r=0`, or
`r=1/2`.  The direct exceptional rebuilds give:

| stratum | exact result |
| --- | --- |
| ordinary `Y=0` | all `4 x 4` minors zero; rank three when genuine |
| `r=0` | complete displayed frame; every genuine point rank three |
| `r=1/2` | every `4 x 4` minor zero; generic rank three, but `Y=0,T!=0` rank two |
| `r=-1/4,T!=0` | rank-four minor `-9XY^2/T` on the genuine locus |
| `r=-1/4,T=0` | all `4 x 4` minors zero and rank three on the genuine locus |
| `r=-1/2` | complete kernel killed by `B` |
| `r=-1` | complete kernel killed by `B` |

For ordinary `Y=0`, a rank-three witness is

```text
16 T X^2(r+1)(2r-1)/(4r+1).
```

At `r=-1/4,T=0`, a rank-three witness is `-3X^2`.  These, together
with the generic factor and the direct nongenuine fibres, prove that the full
rank-at-most-three survivor set is exactly

```text
r=0;
r=1/2;
ordinary Y=0 with T!=0 and B!=0;
r=-1/4,T=0,
```

plus the exact mode-swapped copy on the `h1` axis.

## Exact refutation at `r=1/2`

At `h=(T,0,0,0), r=1/2`, the complete kernel frame is

```text
g0=(-1,-1,0,0;T,0,1,0),
g1=( 0, 0,1/2,0;0,0,0,1).
```

For `z=Xg0+Yg1`,

```text
A=4X,                  B=4TX+3Y.
```

All `4 x 4` marked-mode-zero minors vanish.  When `Y!=0`, the minor

```text
det N0[rows 017, columns 123]=-3Y^2
```

proves rank three.  But on `Y=0,T!=0`, the vector `g0` is genuine:

```text
A=4,                   B=4T!=0,
rank N0=2.
```

This is an exact characteristic-zero counterexample to the sentence “every
genuine kernel point has marked rank 3.”  It is not a counterexample to the
survivor classification, because rank two remains non-obstructing.

## Shared pair retained by this scoped audit

The off-wall finite-`D01` kernel vector `k` is exactly the first vector in the
complete `D23(r=0)` frame

```text
f0=(-1,-1,0,-2T;2T,T,1,0),
f1=( 0, 0,1,-1;1,1,0,1).
```

For `D23`, `z=Uf0+Vf1` has

```text
A23=4U, B23=4(TU+V),
```

and marked rank exactly three whenever it is genuine.  This independently
verifies the displayed simple binary shared-pair type and its mode-swapped
partner.  It is not promoted to a ternary or compatible `H22` lift here.

There is a stronger exact slope-forcing statement before any later
compatibility theorem is used.  Apply the finite-`D23(r)` mixed matrix to the
complete finite-`D01` kernel vector.  On the `h0` axis use

```text
k0=(-1,-1,0,-2T;2T,T,1,0),
```

and on the `h1` axis use its exact mode swap

```text
k1=(-1,-1,0,-2T;T,2T,1,0).
```

On both axes, all fourteen `D23(r)` mixed coefficients vanish except the last
one, which is

```text
-12Tr.
```

The two `D23` diagonals on the same vector are

```text
A23=4,                 B23=4T(2r+1).
```

Common genuineness therefore forces `T!=0`; the mixed equation then forces
`r=0`.  Thus every off-wall shared-extension candidate reduces to the displayed
`D23(r=0)` type (and its mode swap).  This slope reduction is independently
verified here and does not use the excluded later compatibility obstruction.

## Replay boundary

The verifier imports neither the target derivation nor its helpers.  It uses
no finite fields, parameter grids, numerical ranks, or later compatibility
artifact.  Run:

```text
uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate_verifier.py
```

The script fails closed on any changed projection ideal, kernel, diagonal,
rank witness, exceptional-fibre result, or factor-cover determinant.
