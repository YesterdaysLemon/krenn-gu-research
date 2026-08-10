# Candidate finite-`D23` construction on generic `B_drop`

```yaml
role: construction
date_utc: 2026-08-01T10:47:14Z
git_commit: a0764e34b14d56ec76471f646755c067e8cb9ff2
claim_label: CANDIDATE
scope: generic B_drop finite-D23 fibres over Q(a) on the p+q=0 diagonal-DVR wall
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md: e2a0e57269890e621e797875af3bbf635a5a4268650fab1749cbfceb48f587ae
  verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py: 5f3df560d0db922fc729d73253ff5d331cebb9a337175315d6e5cfec67e8d407
method: exact kernel stratification at r=0, rQ nonzero, and Q=0; targeted rank witnesses and explicit marked right kernels
command: uv run --with sympy python construct_p5_h22_common_active_binary_triangle_p_plus_q_b_drop_finite_d23_candidate.py
outputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_B_DROP_FINITE_D23_CANDIDATE.md: hash reported by replay
limitations: candidate pending independent replay; direct a-specializations, the paired D01 lift, arbitrary-order gluing, and the global conjecture are not claimed
```

## Claim boundary

This is a **compatible surviving-neighbour construction**, not a weighted-`H22`
obstruction and not a complete weighted-`H22` lift.  It classifies the generic
finite-`D23` extension kernels over `K=Q(a)` on the two projected marking axes

```text
S1: h=(0,0,t,0),              S2: h=(0,t,0,0),
```

where `a(a+1)(2a+1)` is nonzero.  It proves that every point of both axes is
actual and that every genuine `S1` extension has marked mode 2 of rank at most
three, while every genuine `S2` extension has marked mode 1 of rank at most
three.  The paired `D01` member is outside this construction claim.

Put

```text
s=2a+1,                 Q=2rs-1.
```

The extension order below is `(z0,...,z7)`.

## The rank-jump slope `r=0`

On both sheets the mixed matrix has rank six.  A common first kernel vector is

```text
v0=(-a-1,0,0,-1/a,1/a,(a+1)/a,1,0).
```

The second vectors are

```text
v1,S1=(0,-1,-1,ts/a^2,-ts/a^2,-t(a+1)^2/a^2,0,1),
v1,S2=(-a^2t/(a+1),-1,-1,t/(a+1),-t/(a+1),at/(a+1),0,1).
```

Rows `[1,2,3,4,6,9]` and columns `[0,1,2,3,4,5]` have determinant

```text
2 a^4 (a+1)^3 s,
```

so these two independent vectors are complete kernels over `K(t)`.  For
`z=Xv0+Yv1`, the diagonal forms are

```text
             A                         B
S1       -2Ys       -2s(-Xa+Yt(a+1))/a^2
S2       -2Ys        2Xs/a.
```

Every `t` is actual: on `S1`, take
`(X,Y)=((t(a+1)-1)/a,1)`; on `S2`, take `(X,Y)=(1,1)`.
Thus the projection closure did not introduce spurious marking points.

For `S1` marked mode 2 has the explicit right-kernel column

```text
(-Xa+Yts, Ya^2, 0, 0)^T,
```

and its rows `037`, columns `023` minor equals

```text
-4Y(a+1)^2s^2(-Xa+Yt(a+1))/a^2.
```

Genuineness makes this minor nonzero, so the marked rank is exactly three.
For `S2` mode 1 has right-kernel column

```text
(-X(a+1)+Yat, Ya(a+1), 0, 0)^T,
```

and the same minor equals `4XYas^2`, again giving rank exactly three for
every genuine extension.

## The stratum `r != 0`, `Q != 0`

The complete one-dimensional kernels, normalized by `z7=1`, are

```text
S1:
( t(a+1)s(2ar+1)/(aQ), -1,-1,0,0,
 -t(a+1)(2ar+1)/(aQ), t(2a^2r-2a-1)/(aQ), 1),

S2:
( at s(2r(a+1)+1)/((a+1)Q), -1,-1,0,0,
 t(2a^2r+4ar-2a+2r-1)/((a+1)Q),
 -at(2r(a+1)+1)/((a+1)Q), 1).
```

Three displayed seven-by-seven rank minors in the machine certificate have
greatest common divisor over `Q(a)[r]`

```text
r(r-1/(2s)).
```

The explicit kernel gives rank at most seven, while this gcd gives rank at
least seven away from `r=0` and `Q=0`; hence the kernels are complete.

Their diagonals are

```text
S1: A=-2s,
    B=-2ts(2ar-1)(r(a+1)-1)/(aQ),

S2: A=-2s,
    B=-2ts(ar-1)(2r(a+1)-1)/((a+1)Q).
```

Thus the genuine loci on this stratum are exactly the nonvanishing loci of
the displayed factors.  On the whole genuine locus, the following polynomial
right-kernel columns prove the required marked rank bounds:

```text
S1 mode 2:
(-D1,-aQ,-arQ,D1)^T,       D1=rt(a+1)(2ar+1),

S2 mode 1:
(-D2,-(a+1)Q,-r(a+1)Q,D2)^T,
                            D2=art(2r(a+1)+1).
```

The marked ranks are generically three and can drop to two on further special
slopes.  That drop strengthens the rank-at-most-three condition; this note
does not claim a complete lower-rank stratification.

## The exceptional slope `Q=0`

For nonzero `t`, both sheets have the complete rank-seven kernel

```text
(-s,0,0,0,0,1,1,0),
```

with `(A,B)=(0,1)`, so there is no genuine extension.  The replay records a
nonzero seven-by-seven minor separately on each sheet.

At `t=0`, the mixed rank drops to six and the complete kernel gains

```text
(0,-1,-1,0,0,0,0,1).
```

For the general combination with coefficients `(X,Y)`, `(A,B)=(-2Ys,X)`.
Hence the origin is genuine exactly when `XY!=0`.  Both marked modes 1 and 2
have the right-kernel column

```text
(-X,2Ys,Y,XY)^T
```

and are generically rank three.  This retains the exceptional stratum instead
of losing it by dividing by `Q`.

## Failure and limitation ledger

- The first generic kernel ansatz divided by `Q` and initially hid both the
  rank-six `r=0` family and the `Q=0,t=0` origin.  They were reconstructed
  directly and are part of the certificate.
- A typo in one exploratory one-line import produced no evidence and was
  discarded.
- No finite-field computation, parameter grid, broad all-minor scan, or graph
  search was used.  Three targeted seven-minors certify the generic rank.
- Everything here is over `Q(a)`.  Direct specializations of `a`, including
  collisions among displayed slope factors, require separate reconstruction.
- This construction does not establish the paired finite-`D23`/`D01` weighted
  `H22` lift and makes no arbitrary-order or global Krenn--Gu claim.

Replay with

```text
uv run --with sympy python \
  claims/p5/h22/disputed-ownership/p-plus-q-wall/construct_p5_h22_common_active_binary_triangle_p_plus_q_b_drop_finite_d23_candidate.py
```
