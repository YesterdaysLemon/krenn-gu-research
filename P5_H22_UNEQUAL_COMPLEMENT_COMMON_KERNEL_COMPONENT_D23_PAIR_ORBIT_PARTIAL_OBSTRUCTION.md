# Component 22 finite-D23 weighted-H22 pair-orbit partial obstruction

Claim label: **VERIFIED_PARTIAL**.  This note does not close the generic
weighted-H22 fibre and does not resolve the Krenn--Gu conjecture.

Work over `K = Q(A,R,D)` and put `s=2A+R`.  For the finite D23 projection
`(q0,q1,rho*q2+q3,e)`, binary extension forces the fourteen-by-eight mixed
coefficient matrix to have rank at most seven.  Three fixed one-marked rank
obstructions are used throughout:

* `det N0[0,1,3,7]`,
* `det N1[0,1,2,7]`, and
* `det N1[0,1,4,7]`.

The verifier certifies exact unit ideals for the three explicitly discovered
projection branches Q1, Q2, Q3.  It also certifies the following set-theoretic
cover on `h1=0`.  A selected mixed minor is associated over `K` to

```
(s*h2+1)*(2*h3-s)*rho*(rho-1)*f6*f7*f8*(rho+1)^2,
```

where

```
f6=(D-1)*rho+D+1,
f7=(A*D+A+R)*rho+A*D-A-R,
f8=(A*D+A+R*D)*rho+A*D-A+R*D.
```

Exact unit ideals close every displayed factor except `2*h3-s`.  On that
factor, `h2=0` is empty.  Away from the already closed factors, a second mixed
minor forces `L*G=0`; the `L=0` saturation is a unit ideal.  On `G=0`, a third
mixed minor forces `T*G2=0`; the unique generic `T=0` slope is again a unit
ideal.  The explicit polynomials `L`, `T`, `G`, and `G2` are defined in the
verifier so the cover is independently replayable without relying on this
prose.

The sole residual inside this `h1=0` analysis is

```
h1=0,  2*h3=s,  G=G2=0,
h2*(s*h2+1)*rho*(rho-1)*f6*f7*(rho+1)*L != 0.
```

Its direct ideal and a one-variable-reduced resultant ideal both exceeded a
300-second bound.  Therefore this residual is **UNKNOWN**, not nonempty or
empty.  The `h1!=0` part of the primary factor cover is also not exhausted.
No finite-field computation is used as proof.

A subsequent two-minor coefficient-field certificate closes the divisor
`R*h2=1` inside this residual.  Thus the refined unknown part also satisfies
`R*h2!=1`:
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2R1_RESIDUAL_OBSTRUCTION.md`](P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2R1_RESIDUAL_OBSTRUCTION.md).

Replay with:

```
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction.py
```

The audit independently rebuilds all relevant maps and checks Q1, Q2, Q3 and
the representative `h1=0, rho=0` factor slice at the exact rational
specialization `(A,R,D)=(2,1,3)`.  It is an audit of the symbolic verifier, not
a replacement for its generic coefficient-field certificates.
