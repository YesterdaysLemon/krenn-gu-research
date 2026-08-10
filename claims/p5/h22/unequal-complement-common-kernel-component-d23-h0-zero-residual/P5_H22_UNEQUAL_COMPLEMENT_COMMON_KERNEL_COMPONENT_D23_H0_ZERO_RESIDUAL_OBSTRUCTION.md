# Component twenty-two finite-`D23` residual obstruction on `h0=0`

## Status

**Exact characteristic-zero residual-divisor obstruction.**  The complete
`h0=0` part of the displayed finite-`D23` residual on component twenty-two
is empty.  More precisely, work over `K=Q(A,R,D)`, put `s=2A+R`, and impose

```text
h0=0,       h1=0,       2*h3=s,       G=G2=0.       (1)
```

Away from the factor divisors already closed in the preceding pair-orbit
theorem, and away from the separately closed divisor `R*h2=1`, the genuine
binary incidence ideal is the unit ideal.  Thus no one-marked ternary test
is needed on this chart.  Together with the earlier `R*h2=1` theorem, this
closes every `h0=0` point of the residual (1).

The complementary `h0!=0` residual and the unexhausted `h1!=0` finite-`D23`
locus remain **UNKNOWN**.  This does not close the generic weighted-`H22`
fibre, arbitrary source order, or the global Krenn--Gu conjecture, which
remains **UNRESOLVED**.

## Exact chart and saturation

Use the notation and polynomials `G,G2,f2,f6,f7,f8,L,T` of
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_PAIR_ORBIT_PARTIAL_OBSTRUCTION.md`](P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_PAIR_ORBIT_PARTIAL_OBSTRUCTION.md).
After (1), they are polynomials in `K[h2,rho]`; in particular

```text
f2=s*h2+1,                    L=R*rho+s,
f6=(D-1)*rho+D+1,
f7=(A*D+A+R)*rho+A*D-A-R,
f8=(A*D+A+R*D)*rho+A*D-A+R*D.                       (2)
```

The exact open multiplier is

```text
U=h2*f2*rho*(rho-1)*(rho+1)*f6*f7*f8*L*T*(R*h2-1). (3)
```

Every factor in (3), except the last, is a branch already proved empty by
the partial pair-orbit theorem before its `G=G2=0` residual was declared.
The last factor removes the divisor proved empty in
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2R1_RESIDUAL_OBSTRUCTION.md`](P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2R1_RESIDUAL_OBSTRUCTION.md).
Consequently (3) is exactly the still-open part of (1), not a new genericity
assumption.

## Unit binary-incidence ideal

Let `M` be the fourteen-by-eight finite-`D23` mixed extension matrix after
(1), and let `a,b` be its all-alpha and all-beta diagonal rows.  With

```text
x=(x0,x1,x2,x3;y0,y1,y2,y3)^T,
```

a genuine binary neighbour lies on the projective open

```text
M*x=0,             (a*x)*(b*x)!=0.                 (4)
```

Normalize `a*x=1`, introduce `w` for `(b*x)^-1`, and introduce `z` for
`U^-1`.  Exact standard-basis reduction over the coefficient field gives

```text
< M*x, a*x-1, w*(b*x)-1, G, G2, z*U-1 >
   = <1>

in K[x0,...,x7,h2,rho,w,z].                        (5)
```

Equation (5) proves that the refined `h0=0` residual contains no genuine
binary extension.  Combining it with the previously closed factor divisors
and `R*h2=1` closes the full `h0=0` intersection of (1).

This is not a vacuous parameter calculation.  Before adjoining the mixed
incidence equations, exact reduction gives

```text
<G,G2,z*U-1> != <1>,       dim <G,G2,z*U-1> = 0
```

in `K[h2,rho,z]`.  Thus the refined parameter residual has geometric points
over an algebraic closure of `K`; equation (5) specifically excludes their
genuine binary extensions.

No finite-field computation or rational specialization is used in the
proof.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_zero_residual_obstruction.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_h0_zero_residual_obstruction.py
```

The primary reconstructs the component rows and finite-`D23` incidence with
the repository contraction builder.  The audit imports no repository code:
it independently rebuilds the rows, permanents, mixed equations, diagonals,
residual polynomials, and the coefficient-field unit ideal before replaying
the primary.
