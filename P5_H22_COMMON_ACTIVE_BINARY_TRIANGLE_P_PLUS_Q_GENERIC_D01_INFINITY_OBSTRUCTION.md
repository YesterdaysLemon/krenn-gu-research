# Verified generic weighted-`H22` obstruction at `D01` infinity

## Status and scope

**VERIFIED after two disjoint fresh replays.**  This note closes the only
generic weighted-`H22` direction left by
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md` on the
two verified `p+q=0` charts.  It treats `D01` at infinity directly on
`B_full` and `B_drop`, over characteristic zero and on the finite-centre open

```text
a(a+1)(2a+1) != 0,  and lambda != 0 on B_full.       (1)
```

Together with the already verified finite-`D01` obstruction and half-centre
Hall obstruction, this closes weighted `H22` on the generic points of the two
diagonal-DVR charts.  It does not
treat the direct exceptional fibres `a=0,-1`, non-diagonal source changes,
arbitrary-order gluing, or the global Krenn--Gu conjecture.

## Actual marking fibres

The exact generic `D01`-infinity projections are

```text
B_full: <h3, a h1+(a+1)h2, h0, h2^2>,
B_drop: <h3, h0, h1 h2>.                            (2)
```

Thus `B_full` has the single geometric marking `h=0`.  The nilpotent `h2`
direction in its projection scheme is not treated as an extra actual point.
The `B_drop` marking set is the union

```text
S1: h=(0,0,t,0),       S2: h=(0,t,0,0).             (3)
```

All three actual fibres are rebuilt directly below.

## Complete mixed kernels

Order the eight extension entries as `z0,...,z7` and put `s0=2a+1`.  The
same fixed rank-six witness works in every case: mixed rows

```text
[1,2,3,4,6,9],  extension columns [0,1,2,3,4,5]
```

have determinant

```text
2 a^4 (a+1)^3 s0.                                   (4)
```

Hence the mixed kernel has dimension two on (1).  Write its general vector
as `z=X v0+Y v1`.

For `B_full,h=0`, take

```text
v0=(-a-1,0,0,1/a,lambda/a,(a+1)/a,1,0),
v1=(0,-1,-1,0,1,0,0,1).                            (5)
```

For both `B_drop` sheets, take

```text
v0=(-a-1,0,0,1/a,1/a,(a+1)/a,1,0).                 (6)
```

The second vectors are

```text
S1: v1=(0,-1,-1,-t s0/a^2,-t s0/a^2,
        -t(a+1)^2/a^2,0,1),

S2: v1=(-a^2 t/(a+1),-1,-1,-t/(a+1),-t/(a+1),
        a t/(a+1),0,1).                             (7)
```

Direct multiplication by the full fourteen-row mixed matrix annihilates
every displayed vector.  Equation (4) and the two independent vectors prove
that these are complete kernels, including their intersection at `t=0`.

## Diagonals and one fixed marked minor

Let `A` and `B` be the all-alpha and all-beta binary diagonals.  On the three
complete kernels they are

```text
B_full:
  A=-2Y s0,
  B=-2 s0 (X lambda+Y a)/a;

B_drop,S1:
  A=-2Y s0,
  B=2 s0 (-X a+Yt(a+1))/a^2;

B_drop,S2:
  A=-2Y s0,
  B=-2X s0/a.                                      (8)
```

For marked mode three, the fixed four rows `0147` give

```text
                         det N3[0147]/(A B)
B_full,h=0                    -2Y a^2 lambda
B_drop,S1                     -2Y a^2
B_drop,S2                     -2Y a^2.              (9)
```

A genuine binary extension has `A B != 0`.  In particular, (8) forces
`Y!=0`.  Every other factor in (9) is a unit on (1), so the fixed marked
minor is nonzero for every genuine projective kernel vector.  Scaling the
kernel vector by `c!=0` scales `A,B` by `c`, the minor by `c^3`, and the ratio
by `c`; nonvanishing is projectively invariant.

Therefore `D01` at infinity cannot supply the required sharp marked
neighbour on any actual generic marking branch.  The finite-`D23` kernel need
not be classified: the paired weighted-`H22` candidate already fails on its
`D01` member.

## Boundaries and replay

- The result uses the exact projections (2), but interprets them by rebuilding
  every geometric fibre in (3).
- Denominators in (5)--(8) make `a=0,-1` separate direct problems.
- The half centre `a=-1/2` is already excluded by its homogeneous Hall
  obstruction and is not specialized from these formulas.
- No finite-field computation, parameter grid, or broad all-minor search is
  used.
- A fresh no-import verifier reconstructed the `B_full` chart and its paired
  finite-`D23` slope exhaustion.  A second no-import verifier independently
  reconstructed both `B_drop` sheets, including their `t=0` intersection.

Replay the primary and the two disjoint audits with

```text
uv run --with sympy python \
  verify_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_obstruction.py

uv run --with sympy python \
  audit_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_verifier.py

uv run --with sympy python \
  audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py
```
