# Independent verification of the off-wall endpoint compatibility obstruction

## Verdict and frozen scope

**VERIFIED** for the exact construction claim in
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_CANDIDATE.md`.

A fresh verifier rebuilt the off-wall `gamma=0` endpoint planes, both marking
axes, finite `D01`, finite `D23` at slope zero, their complete mixed kernels,
the shared-extension intersection, all four binary diagonals, the transverse
mode-two minor, and the two-contraction stacked minor.  It imports neither the
construction derivation nor the earlier endpoint derivation.

The verdict is limited to the displayed finite-`D01` plus
finite-`D23,r=0` pair.  It does not verify the on-wall endpoint, other `D23`
slopes, non-diagonal source changes, arbitrary-order gluing, or the global
Krenn--Gu conjecture.

## Independent reconstruction

Use

```text
e=(1,0,0,0), w=(0,1,1,1), u=(0,1,-1,0),
v1=(0,1,1,0), v2=(0,0,0,1),

alpha=(e,e,-u,2v2-v1), beta=(w,w,e,v1).
```

The verifier implements permanents by subset dynamic programming and builds
one-marked maps by complementary-column cofactors, independently of the
construction program’s permutation formulas.

For `h=(T,0,0,0)`, direct multiplication by all fourteen mixed rows gives

```text
k0=(-1,-1,0,-2T;2T,T,1,0),
f =( 0, 0,1,  -1; 1,1,0,1),

ker M01=<k0>, rank M01=7,
ker M23=<k0,f>, rank M23=6.
```

The fixed witnesses replay exactly:

```text
det M01[3,4,5,7,9,12,13 | 0,1,2,3,4,5,7]=-16s^6,
det M23[3,4,5,7,9,13    | 0,1,2,3,4,5]  =-4.
```

The `h1` axis has

```text
k1=(-1,-1,0,-2T;T,2T,1,0)
```

and the same vector `f`, ranks, and witnesses.  Both axes are rebuilt
directly.

Because the genuine `D01` kernel is exactly one-dimensional and its generator
is one of the two complete `D23` generators, the intersection under shared
extension coordinates is exactly

```text
ker M01 intersect ker M23=<ki>.
```

No second `D23` coefficient survives this intersection.

## Genuineness and the axis intersection

For the common vector `z=Cki`, direct evaluation gives on both axes

```text
A01=-4Cs, B01=4C(Ts+1),
A23= 4C,  B23=4CT.
```

Therefore common genuineness is exactly

```text
C*s*T*(T*s+1) != 0.
```

The boundary attacks are fail-closed:

- `C=0` is the zero extension and cannot satisfy either normalization.
- `s=0` has `A01=0` on the entire direct mixed kernel; its rank jump creates
  no hidden neighbour.
- `Ts+1=0` has `B01=0` on the complete rank-seven line.
- `T=0` has `B23=0` on the complete shared line.

At `T=0` the `h0` and `h1` markings coincide.  Rebuilding that origin once,
without choosing an axis label, gives the same `D01` line and `D23` plane;
their intersection is still the line and `B23` still vanishes.  Thus the axis
intersection is covered rather than discarded.

## Two independent obstructions

On the complete shared line, the directly reconstructed `D01` mode-two map
has

```text
det N01,mode2[0127]=-32 C^3 s^2(Ts+1).
```

Every factor is nonzero on the common genuine open, so this map has rank four.
Projective rescaling by `lambda` multiplies the determinant by `lambda^3`.

Independently, extend all four endpoint rows by the common vector `Cki` and
use the full five-coordinate contraction rows

```text
q01=(1,s,0,0,0), q23=(0,0,1,0,0).
```

Stacking the two full one-marked maps in the active axis mode, rows
`(0,6,7,8,14)` and all five columns give

```text
det=64 C^4(Ts+1).
```

This is nonzero on the same genuine open and verifies the rank-five
two-slice compatibility obstruction.  Either certificate excludes the common
ternary lift for this frozen pair.

## Evidence boundary and replay

- Characteristic zero only; no finite fields or parameter grids.
- No broad minor scan: only the two frozen minors are evaluated.
- No failed branch or timeout occurred in the independent replay.
- The global conjecture remains unresolved.

The full verifier run report, including role, UTC date, commit, SHA-256
inputs/outputs, method, command, and limitations, is emitted by

```text
uv run --with sympy python \
  claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py
```
