# Component twenty-two finite-`D23` residual cofactor-open obstruction

## Status

**Exact characteristic-zero residual obstruction.**  On the remaining
finite-`D23` residual of component twenty-two, a fixed maximal mixed minor
closes a nonempty exact open at the binary-incidence level.  Combined with
the separate `h0=0` theorem, the displayed residual is reduced to one exact
cofactor divisor inside `h0!=0`.

The cofactor divisor itself and the unexhausted `h1!=0` locus remain
**UNKNOWN**.  This does not close the generic weighted-`H22` fibre,
arbitrary source order, or the global Krenn--Gu conjecture, which remains
**UNRESOLVED**.

## Residual chart

Work over `K=Q(A,R,D)`, put `s=2A+R`, and use the notation
`G,G2,f2,f6,f7,f8,L,T` of
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_PAIR_ORBIT_PARTIAL_OBSTRUCTION.md`](P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_PAIR_ORBIT_PARTIAL_OBSTRUCTION.md).
The residual under consideration is

```text
h1=0,       2*h3=s,       G=G2=0,                 (1)
```

away from the already closed factors

```text
h2*f2*rho*(rho-1)*(rho+1)*f6*f7*f8*L*T=0.         (2)
```

The prior `R*h2=1` theorem and the new `h0=0` theorem also close those two
divisors.  Hence the remaining part of (1) has

```text
h0*(R*h2-1)!=0.                                    (3)
```

## A fixed full-rank cofactor

Let `M` be the fourteen-by-eight finite-`D23` mixed extension matrix on
(1).  Take all eight columns and rows

```text
(0,1,2,3,4,5,7,8).                                (4)
```

Direct exact factorization gives

```text
det M[(4)] =
-8*A*D*s^4*(D-1)*(D+1)
 *rho*(rho-1)*(rho+1)*f6*f7*P,                    (5)
```

where equation (5) defines the polynomial

```text
P in K[h0,h2,rho].                                 (6)
```

The verifier checks that the quotient in (5) has denominator one and checks
the identity before using `P`.  The factors in `K` are units on the generic
component chart, and every remaining parameter factor outside `P` is
already inverted in (2).  Therefore

```text
P!=0  ==>  rank(M)=8.                              (7)
```

The common mixed kernel is then zero, so no binary extension--and hence no
weighted-`H22` lift--exists on this cofactor open.

## Nonvacuity

The cofactor open meets the exact residual.  Over
`Q(sqrt(29665))`, take

```text
(A,R,D,rho)=(2,1,3,2),
h0=(-35+sqrt(29665))/540,
h2=(-199-sqrt(29665))/1656,
h1=0,       h3=5/2.                                (8)
```

Direct substitution gives `G=G2=0`; every factor in (2)--(3) is nonzero;
and

```text
P=(-169645+5603*sqrt(29665))/276 !=0.              (9)
```

Thus (7) closes a genuine nonempty open of the residual, rather than merely
renaming an empty parameter chart.

Combining this theorem with the `h0=0` obstruction leaves precisely

```text
(1),       h0!=0,       P=0                       (10)
```

subject to the open conditions (2)--(3).  A direct localized standard-basis
calculation of (10) exceeded 300 seconds.  That timeout is not evidence for
emptiness or survival.  No finite-field computation is used.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_cofactor_open_obstruction.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_cofactor_open_obstruction.py
```

The primary reconstructs the component rows and contraction with repository
utilities.  The audit imports no repository code: it independently rebuilds
the rows, permanents, mixed matrix, factorization, and exact algebraic
nonvacuity point.
