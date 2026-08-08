# A diagonal-product ideal closes weighted `H22` on the Eisenstein component

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
weighted marked-basis fibre over the generic point of the thirteenth
pure-`P_4` component is empty for `H22`.

Together with the earlier component theorems, all thirteen currently
certified pure-`P_4` component orbits are now generically closed for both
`H31` and weighted `H22`.  Special component divisors, support-one common
zero divisors, lower pair-image ranks, component exhaustiveness, and the
global Krenn--Gu conjecture remain open.

## The weighted `01` neighbour

Use the intrinsic kernel and marked active rows from
[`P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h31/eisenstein-norm/P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md):

```text
alpha_rows=(b_bar,m,m_r,c),
beta_i(h)=beta_i+h_i*alpha_i,
beta_rows=(x_0,a,a,d).                              (1)
```

The Eisenstein quadric has the rational function-field chart `K=C(u,v)`
given there.  For the finite weighted `01` slope `rho`, send an extended row

```text
(z_0,z_1,z_2,z_3; e)
  -> (rho*z_0+z_1,z_2,z_3,e).                      (2)
```

Let `z=(x_0,...,x_3,y_0,...,y_3)` be the eight extension entries.  The
fourteen mixed binary coefficients are linear forms

```text
L_w(rho,h,z),       0<|w|<4,                       (3)
```

and the opposite diagonal coefficients are linear forms `A(rho,z)` and
`B(rho,h,z)`.  A binary neighbour would require

```text
L_w=0 for all mixed w,       A*B!=0.                (4)
```

## The mixed scheme lies in two diagonal hyperplanes

Work over the full polynomial ring

```text
S=K[rho,h_0,h_1,h_2,h_3,x_0,...,x_3,y_0,...,y_3]. (5)
```

No slope or marking polynomial is inverted.  Exact reduction gives the
scheme-theoretic identity

```text
A*B in (L_w : 0<|w|<4).                            (6)
```

The reduced basis of the mixed ideal has size `48`.  Thus

```text
V(L_w) subset V(A) union V(B),                     (7)
```

including every finite special slope and every marking divisor.  Every
mixed-zero extension loses at least one required binary diagonal.

This product identity is strictly better suited to the geometry than trying
to prove one fixed row-module inclusion.  Away from a slope-torsion divisor,
the all-kernel row does belong to the mixed row module; on that divisor the
vanishing can switch to the all-active diagonal.  Equation (6) records the
union without breaking it into artificial pivot charts.

## The projective slope at infinity

The finite chart (2) misses the homogeneous weight `(1:0)`.  There the
weighted row is

```text
(z_0,z_2,z_3,e).                                   (8)
```

Repeating the calculation over
`K[h_0,h_1,h_2,h_3,x_0,...,y_3]` again gives `A*B` in the fourteen-generator
mixed ideal; its reduced basis has size `10`.  Hence (7) holds on the entire
projective weighted line.

At `(u,v,rho)=(2,0,2)` and canonical marking, the mixed matrix has rank
seven.  Adjoining `A` leaves rank seven, while adjoining `B` raises it to
eight.  This diagnostic exhibits the generic all-kernel branch, but the
global proof is the product ideal (6), not that rank sample.

## Across the mathematical fence

The new shape is a scheme-theoretic union rather than a determinantal rank
condition:

```text
mixed extension scheme -> union of two Segre-coordinate hyperplanes.
```

In algebraic statistics this resembles a conditional-independence model
whose observable variety is reducible; in commutative algebra it is the
single certificate `AB` in the defining ideal.  The useful lesson is that
module torsion is not noise here: it marks where the obstruction changes
which diagonal it kills.  Encoding both branches by their product avoids
case-by-case saturation and preserves all special slopes symbolically.

## Proof boundary

The theorem is generic only in the two component parameters `u,v`.  It is
complete in the marking variables, extension entries, and projective
weighted slope.  Component divisors outside the function-field chart can
specialize differently and remain open.

## Verification

Run:

```text
uv run --with sympy python claims/p5/h22/eisenstein-norm/verify_p5_h22_eisenstein_norm_component_generic_obstruction.py
uv run --with sympy python claims/p5/h22/eisenstein-norm/audit_p5_h22_eisenstein_norm_component_generic_obstruction.py
```

The primary verifier constructs both projective slope charts over
`C(u,v)`, proves the two diagonal-product ideal memberships, and checks the
canonical rank asymmetry.  The independent audit imports no primary
constructor; it rebuilds every permanent by subset dynamic programming and
replays both ideal memberships at two rational norm-quadric points.  These
specializations corroborate, but do not replace, the function-field proof.
