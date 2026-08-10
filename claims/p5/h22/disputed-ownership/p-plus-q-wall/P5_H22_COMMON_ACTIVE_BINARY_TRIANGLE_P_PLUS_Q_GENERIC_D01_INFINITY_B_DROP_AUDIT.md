# Independent audit of generic `B_drop` at `D01` infinity

## Restricted verdict

**VERIFIED**, only for the generic `B_drop` `S1/S2` `D01`-infinity claim in
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_OBSTRUCTION.md`.

This audit does not import the discovery verifier or the partial-checkpoint
helper.  It independently reconstructs the four planes, markings,
`D01`-infinity contraction, permanent coefficients, fourteen mixed rows,
complete kernels, rank witness, binary diagonals, fixed marked minor, and
projective scaling.  It also rebuilds the common `t=0` fibre from both
sheets and checks that the matrices and kernel frames agree there.

The coefficient field is `C(a,t)` on

```text
a(a+1)(2a+1) != 0.                                  (1)
```

No verdict is issued here for `B_full`, finite `D23`, `a=0,-1`, the
half-centre replacement, non-diagonal source changes, arbitrary-order
gluing, or the global Krenn--Gu conjecture.

## Independent reconstruction

Put

```text
e=X0, L=A-B, M=A+B, s0=2a+1,
k0=s0 C-a(a+1)L.
```

The audit starts from

```text
alpha=(k0,e,e,M),
beta =(L,(a+1)L+C,aL+C,e).                          (2)
```

For each marking it constructs `beta_i(h)=beta_i+h_i alpha_i` and verifies
that all four Pluecker tuples are unchanged.  Its separate subset-DP
permanent gives the sole pure coefficient

```text
T1111=-2s0.                                         (3)
```

It then applies

```text
D01^infinity(z,x)=(z0,z2,z3,x)                      (4)
```

and differentiates all sixteen permanent coefficients in the eight
extension entries, retaining the fourteen mixed rows.

## Kernel and rank attack

For both

```text
S1: h=(0,0,t,0),       S2: h=(0,t,0,0),             (5)
```

the claimed two kernel vectors are annihilated by all fourteen independently
constructed rows.  They are linearly independent.  Mixed rows
`[1,2,3,4,6,9]` and extension columns `[0,1,2,3,4,5]` have determinant

```text
2a^4(a+1)^3s0.                                      (6)
```

Thus the rank is at least six, while the two independent kernel vectors make
it at most six.  The symbolic nullspace has dimension two and the claimed
frame spans it.  The kernels are therefore complete, not sampled.

At `t=0`, the two independently reconstructed mixed matrices agree, and the
two kernel frames become the same frame.  Their intersection is not omitted
or double-counted.

## Diagonals, fixed minor, and scaling

Writing a general kernel vector as `Xv0+Yv1`, the audit recovers

```text
S1:
  A=-2Ys0,
  B=2s0(-Xa+Yt(a+1))/a^2;

S2:
  A=-2Ys0,
  B=-2Xs0/a.                                        (7)
```

For marked mode three, rows `0147` give respectively

```text
S1: det= 8Y^2s0^2(-Xa+Yt(a+1)),
S2: det=-8XY^2a s0^2,                               (8)
```

and on both sheets

```text
det/(AB)=-2Ya^2.                                    (9)
```

Genuineness forces `Y!=0`; all remaining factors in (9) are units on (1).
Hence every genuine extension has marked rank four.  Replacing the kernel
vector by `c` times itself scales both diagonals by `c`, the minor by `c^3`,
and (9) by `c`; the nonvanishing conclusion is projectively invariant.

## Run report

```yaml
role: verifier
date_utc: 2026-08-01T10:45:57Z
git_commit: a0764e34b14d56ec76471f646755c067e8cb9ff2
claim_label: VERIFIED
scope: only generic B_drop S1/S2 D01-infinity obstruction
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_OBSTRUCTION.md: 3d279feb91958279b0d9f5e499f4599e64b9d4d40314c85a02521af4cee04430
  verify_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_obstruction.py: f942fb92608dcf8f594ffba2ab91008ea09e7d05e6782764501cca6dfc965a31
method: independent subset-DP permanent and full symbolic matrix reconstruction
command: uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py
outputs: this report and the additive audit script; sha256 values emitted at replay
limitations: generic B_drop D01-infinity only; no B_full, finite-D23, exceptional, non-diagonal, arbitrary-order, or global claim
```

Replay with

```text
uv run --with sympy python \
  claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py
```

No finite-field computation, parameter grid, random sample, or broad minor
scan contributes to this verdict.
