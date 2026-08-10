# Component 22 finite-`D23` residual obstruction on `R*h2=1`

## Status

**Exact characteristic-zero residual-divisor obstruction.**  In the notation
of
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_PAIR_ORBIT_PARTIAL_OBSTRUCTION.md`](../unequal-complement-common-kernel-component-d23-pair-orbit-partial/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_PAIR_ORBIT_PARTIAL_OBSTRUCTION.md),
the remaining `h1=0`, `2*h3=2*A+R`, `G=G2=0` residual has no point on

```text
R*h2=1
```

away from the already closed factors

```text
(s*h2+1)*rho*(rho-1)*f6*f7*(rho+1)*L*T=0,
s=2*A+R.
```

The obstruction already occurs in the `14 x 8` mixed extension matrix: two
fixed maximal minors generate the unit ideal together with `G`, `G2`, and
the displayed saturation.  No binary or one-marked lift remains to test.

This is a strict refinement of the earlier partial cover, not a closure of
the complete finite-`D23` orbit.  The complementary `R*h2!=1` residual and
the unexhausted `h1!=0` locus remain **UNKNOWN**.  The generic weighted-`H22`
fibre and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Exact certificate

Work over `K=Q(A,R,D)` and set

```text
h1=0,       h2=1/R,       h3=(2*A+R)/2.
```

Let `M` be the finite-`D23` mixed matrix.  Use the two row sets

```text
J0=(0,1,2,5,6,8,9,10),
J1=(0,1,3,4,7,10,11,12).                          (1)
```

If a binary extension existed, both `det M[J0]` and `det M[J1]` would
vanish.  Direct exact standard-basis reduction in

```text
K[h0,rho,z]
```

gives

```text
<det M[J0], det M[J1], G, G2,
 z*(s*h2+1)*rho*(rho-1)*f6*f7*(rho+1)*L*T-1> = <1>. (2)
```

The factor `T=0` is included in the saturation because it was independently
closed in the preceding partial theorem.  Every other saturation factor is
likewise one of that theorem's exact unit branches.  Equation (2) therefore
closes the complete `R*h2=1` slice of its residual.

## Replay

```text
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h2r1-residual/verify_p5_h22_unequal_complement_common_kernel_component_d23_h2r1_residual_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h2r1-residual/audit_p5_h22_unequal_complement_common_kernel_component_d23_h2r1_residual_obstruction.py
```

The primary replay proves (2) over the coefficient field.  The independent
audit rebuilds the mixed matrix without importing the primary or partial
verifier and checks the unique saturated residual point at
`(A,R,D)=(2,1,3)` by exact rational arithmetic.  That specialization is an
audit only; the coefficient-field unit ideal is the proof.  No finite field
is used.
