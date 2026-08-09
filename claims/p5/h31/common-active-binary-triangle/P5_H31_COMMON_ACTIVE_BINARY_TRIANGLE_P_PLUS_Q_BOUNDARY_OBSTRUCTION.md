# Marked `H31` obstruction on the `p+q=0` boundary of component twenty

## Status

**VERIFIED on the whole diagonal-DVR wall.**  This note gives exact
characteristic-zero marked-`H31` obstruction certificates
for the two finite generic-centre `p+q=0` boundary charts `B_full` and
`B_drop`, their `a=0,-1` fibres, and the replacement family at `a=-1/2`.
The prerequisite `P_4` actual-arc exhaustion is now independently verified.
It also places the finite generic and half-centre `y<0` strata and the
infinity strata with `y<-r` in the complete embedded-`P_3` closure, whose
whole projective marked-`H31` fibre is independently closed.

The two lower-pair special families that generic component-fourteen/fifteen
emptiness cannot reach are now closed by direct certificates:

- `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md`
  treats the `a=0,-1`, `y<0` support-one component-fifteen fibres;
- `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md`
  treats both `y=-r` faces at the special component-fourteen infinity
  endpoint equivalent to `(p,q)=(-1,0)`.

Together with the embedded-`P_3` projective closure for every `y<-r` stratum,
these direct certificates exhaust the lower-pair cases in the verified `P_4`
arc classification.  Thus the whole diagonal-source-torus DVR boundary on
`p+q=0` is `VERIFIED` for marked `H31`.

The result is a boundary theorem for the diagonal-source-torus charts
classified in `P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md`.  It
does not identify `B_drop` with an older named component, prove weighted
`H22`, classify non-diagonal or arbitrary `GL_4` source changes, or resolve
the global Krenn--Gu conjecture.

## Pure orientations

Put

```text
e=X0, L=A-B, M=A+B, s0=2a+1, c=a(a+1), k0=s0 C-cL.
```

For `B_full`, use

```text
alpha=(k0,e,e,M),
beta =(e+lambda L,(a+1)L+C,aL+C,e).                 (1)
```

The sole nonzero squarefree permanent coefficient is

```text
T_1111=-2 lambda s0.                                (2)
```

Thus the exact chart open is `lambda*s0 != 0`.  In particular, `lambda=0`
is not a missing marked fibre: it has already left the nonzero pure-`P_4`
locus.

For `B_drop`, use

```text
alpha=(k0,e,e,M),
beta =(L,(a+1)L+C,aL+C,e),                          (3)
```

with sole coefficient

```text
T_1111=-2s0.                                        (4)
```

This orientation is valid on `s0 != 0`.  Both orientations reproduce the
boundary planes because

```text
k0=s0(C+mu L), mu=-a(a+1)/(2a+1).                  (5)
```

Equation (5) also explains why substituting `a=-1/2` into (1) or (3) is
invalid.

## Complete normalized marked-neighbour incidence

For every marking, set

```text
beta_i(h)=beta_i+h_i alpha_i.
```

For deletion `d`, let `M_d(h)` be the `14 x 8` mixed matrix in extension
coordinates

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3),
```

and let `A_d,B_d` be the two binary diagonal rows.  The exact normalized
incidence ideal is

```text
I_d=<M_d(h)z, A_d z-1, w B_d z-1, u O-1>,           (6)
O_full=lambda(2a+1), O_drop=2a+1.
```

Normalizing `A_d z=1` and adjoining the inverse of `B_d z` covers every
projective extension direction for which both binary diagonals are nonzero.
The `u` equation records precisely the chart open.

The exact elimination uses the block order

```text
ring R=0,(x0,x1,x2,x3,y0,y1,y2,y3,w,u,
          h0,h1,h2,h3,a,lambda),(dp(10),dp(4),dp(2));
I=slimgb(I);
J=std(eliminate(I,x0*x1*x2*x3*y0*y1*y2*y3*w*u));    (7)
```

with `lambda` unused for `B_drop`.

## Exact displayed projections

For both charts,

```text
J0=J3=<1>.                                          (8)
```

Only deletions `1,2` can therefore support a genuine binary neighbour.

For `B_full`, both residual projections are

```text
J1=J2=<h0,h3,
       a h1+(a+1)h2,
       (a+1)h2^2,
       h1 h2>.                                      (9)
```

Over `C(a,lambda)`, this is a doubled scheme supported at the origin.  Its
two exceptional specializations are genuine marking lines:

```text
a=0:   h=(0,t,0,0),
a=-1:  h=(0,0,t,0).                                (10)
```

For `B_drop`,

```text
J1=J2=<h0,h3,h1 h2>,                               (11)
```

the union of the two marking lines

```text
S1: h=(0,0,t,0),
S2: h=(0,t,0,0).                                   (12)
```

These are eliminated projection closures.  A point of a displayed closure
must still have an actual extension satisfying both normalized diagonals.
This distinction is essential at `a=0,-1` below.

## Generic residual kernels and the fixed mode-three minor

For the generic `B_full` marking `h=0`, deletion `1` has complete mixed
kernel

```text
v0=(-a-1,0,0,1/a; lambda/a,(a+1)/a,1,0),
v1=(0,-1,-1,0;1,0,0,1).                            (13)
```

Every genuine extension is `z=T v0+v1`, and

```text
A1 z=-2s0,
B1 z=-(2s0/a)(T lambda+a).                          (14)
```

For deletion `2`, replace the displayed `x3=1/a` by `-1/a`; the second
diagonal changes sign.  Let `N3(z)` be the neighbouring mode-three map with
rows ordered `000,001,...,111`.  For both deletions,

```text
det N3(z)[0457]/(B_d z)=-4 lambda^2 s0.             (15)
```

The right side is a unit on the `B_full` open.  The identity remains exact
on both exceptional marking lines (10), after rebuilding their kernels
without the invalid `1/a` or `1/(a+1)` formulas.

For `B_drop`, the two generic lines admit complete rank-six mixed kernels.
With a compatible kernel parameter `T`, on `S1` and deletion `1`,

```text
A1 z=-2s0,
B1 z=(2s0/a^2)(-Ta+(a+1)t),                         (16)
```

while on `S2`,

```text
A1 z=-2s0,
B1 z=-2Ts0/a.                                       (17)
```

Deletion `2` reverses the signs of the second diagonals.  On both sheets and
both deletions,

```text
det N3(z)[0457]/(B_d z)=-4s0.                       (18)
```

## Exceptional `B_drop` fibres

At `a=0`, away from the common marking `t=0`, the `S1` branch has `A_d=0` on
its complete mixed kernel, so it contains no genuine neighbour despite
appearing in the projection closure.  The `S2` fibre survives: `M_d` has rank
five and a complete three-dimensional kernel.  The common origin is covered
by this surviving rank-five calculation; it is not discarded with the
vanishing branch.

At `a=-1`, the roles reverse away from the common origin.  The `S2` kernel
has identically zero `A_d`, while `S1` survives with mixed rank five and
kernel dimension three, including their common marking.

After normalizing the coefficient on which `A_d=-2s0`, the determinant ratio
on every surviving rank-five fibre is still (18), independent of the extra
kernel parameter.  Generic formulas containing `1/a` or `1/(a+1)` cannot be
specialized to obtain these fibres.

The exact projections (9) and (11), together with the direct `a=0,-1` kernel
rebuilds, exhaust every actual normalized incidence stratum.  The fixed
`[0457]/B_d` identities (15) and (18) are checked on each of those strata.
They therefore give a complete rank certificate, rather than a sample of
extension directions.                                                     (19)

## Fixed pure transverse entries

Row `101` of the pure mode-three map has deleted-column entries

```text
                 d=1                 d=2
B_full     -a^2 h0-lambda       a^2 h0+lambda
B_drop     -a^2 h0-1            a^2 h0+1.           (20)
```

Every projected ideal (9) or (11) contains `h0`, so these reduce to

```text
B_full: (-lambda,lambda), B_drop: (-1,1),            (21)
```

and never vanish on the relevant opens.

Mode-three injectivity forces a hypothetical third target row to be
supported only in the deleted source coordinate.  The fixed transverse
entry then kills that final coefficient.  Consequently

```text
generic marked H31(B_full)=empty,
generic marked H31(B_drop)=empty,                   (22)
```

including the exact `a=0,-1` fibres described above.

## The `a=-1/2` replacement family

At `a=-1/2`, use the nondegenerate basis

```text
alpha=(L,e,e,M),
beta =(C-k e,(1/2)L+C,-(1/2)L+C,e).                 (23)
```

Its sole pure coefficient is

```text
T_1111=1/2.                                         (24)
```

Here `k=0` is the `B_drop` specialization and `k!=0` is the direct
`x0=d` valuative chart.  Exact elimination over `Q[k]`, without inverting
`k`, gives

```text
J_d=<1> for d=0,1,2,3.                              (25)
```

The entire replacement family has no genuine binary neighbour and hence no
marked `H31` lift.

## Retained cautions and scope wall

- Direct substitution `p+q=0` in the older generic component theorem is
  invalid because its intrinsic basis degenerates.
- `B_drop` has two generic marking lines, not a finite residual set.
- The ideals (9) and (11) are projection closures; the disappearing
  exceptional branches are not genuine fibres away from their common origin,
  which is covered by the surviving rank-five branch.
- Generic kernel formulas with `1/a` or `1/(a+1)` are invalid at `a=0,-1`.
- Substitution `a=-1/2` in (1) or (3) is invalid; (23) is required.
- `lambda!=0` is part of the `B_full` pure open, not an optional genericity
  assumption.
- **Failure ledger:** an attempted replay of a redundant global ideal formed
  from all 68 nonzero maximal minors exceeded 150 CPU seconds and was
  terminated.  It contributes no evidence and is not needed for the bounded
  exhaustive fixed-minor proof in (19).
- All computations are exact over characteristic zero.  No finite-field
  computation or inference is used.
- Weighted `H22`, non-diagonal or arbitrary `GL_4` source changes,
  older-component placement, arbitrary-order local-to-global reduction, and
  the global conjecture remain open.
- The verified `P_4` arc classification does not by itself close `H31` on
  special fibres of the lower-pair components.  The two direct obstruction
  notes named in the status section supply those missing certificates; their
  own primary and fresh independent audits are required dependencies of this
  whole-wall statement.

## Exact replay

```text
uv run --with sympy python \
  claims/p5/h31/common-active-binary-triangle/verify_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py

uv run --with sympy python \
  claims/p5/h31/common-active-binary-triangle/audit_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
```

The primary verifier independently constructs the permanent incidence over
characteristic zero, proves all displayed projection ideals bidirectionally,
rebuilds every generic and exceptional kernel stratum, checks the uniform
fixed maximal minor, and verifies the fixed transverse entries.  The audit
does not import the primary and reconstructs the bases, projections, residual
certificates, and replacement-family unit projections through a separate
exact code path.  The intentionally unreplayed 68-minor global ideal is
reported only in the failure ledger, not as a theorem certificate.  The
special component-fifteen and component-fourteen dependencies each have a
separate exact no-import or separately constructed audit; all dependency
hashes are recorded by the aggregate replays.
