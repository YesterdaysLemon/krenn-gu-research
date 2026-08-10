# Candidate generic weighted-`H22` obstruction for component nineteen

```yaml
role: construction
date_utc: 2026-08-01T12:41:25Z
git_commit: 7f1e282c08eb030dcad35b36b3201a871702464d
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: generic weighted H22 fibre of component nineteen, the common-kernel vertical triangle
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md: 3b49c47626131fa10729961bc700d46b518a102799504c3796fb0a5b932c5832
  P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md: da64a3ee55d5dfa361a70cb771196f76f93d13b3d61df358442a22e1e72de1a8
method: exact characteristic-zero permanent reconstruction, projective binary and shared-compatibility elimination, complete shared-kernel frame, and one fixed one-marked minor
command: uv run --with sympy python derive_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
outputs:
  derive_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py: hash reported by replay
  p5_h22_common_kernel_vertical_triangle_component_generic_certificate.json: hash reported by replay
  P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: verified after a fresh no-import replay; generic function-field theorem only; no special-parameter or projective component-boundary fibres, pure-P4 component exhaustiveness, arbitrary-order local-to-global reduction, prize graph, or global Krenn-Gu conclusion
```

## Frozen claim

**VERIFIED after a fresh independent no-import replay:** the generic
weighted-`H22` fibre of component nineteen is empty.  Exact projective
elimination leaves one shared finite branch and no infinite branch.  A single
fixed one-marked determinant excludes every genuine point of the remaining
branch.

The calculation is over `K=Q(p,q,phi)` on the component's generic open.  It
uses neither a parameter grid nor a finite-field inference.

## Intrinsic pure basis

With `A,Abar,B,Bbar` as in the component theorem, put `r=q-phi` and use

```text
alpha0=r(Abar+pB)-p(Bbar+qB),   beta0=Abar+pB,
alpha1=B,                       beta1=A,
alpha2=Bbar,                    beta2=A,
alpha3=Abar,                    beta3=B+phi Bbar.    (1)
```

Direct permanent expansion gives only

```text
T1111=4p.                                             (2)
```

Every affine marking is `betai -> betai+hi alphai`.

## Complete projective binary projection

On the finite homogeneous chart `[lambda:1]`, reconstruct

```text
D01(z,e)=(lambda z0+z1,z2,z3,e),
D23(z,e)=(z0,z1,lambda z2+z3,e).                    (3)
```

At `[1:0]`, use the direct infinity maps.  Exact characteristic-zero
elimination, with both binary diagonals saturated, gives

```text
D01 finite:       <1>,
D01 infinity:     <1>,                              (4)

D23 finite:
  <h3, r*h0+1, h1*h2*((q+1)*lambda+q-1)>,

D23 infinity:
  <h3, r*h0+1, h1*h2>.                             (5)
```

Thus `D01` is never the required binary neighbour at any projective weight.
Any `H22` lift must instead have `D01` nonzero pure and `D23` genuinely
binary, using the same marking, homogeneous weight, and extension vector.

## Shared compatibility, not separate survivors

Impose all fifteen unwanted `D01` pure coefficients, its nonzero beta
diagonal, all fourteen `D23` mixed coefficients, and both nonzero `D23`
diagonals on one shared eight-coordinate extension.  Exact elimination gives

```text
finite:   <lambda-1, h3, h1, r*h0+1>,
infinity: <1>.                                      (6)
```

There are no projective-infinity survivors.  The complete finite branch is

```text
lambda=1,
h=(-1/r,0,t,0).                                     (7)
```

At (7), the combined unwanted-coefficient matrix has rank six.  Its complete
two-dimensional kernel has basis

```text
vC=(0,-1/p,phi/p,0; 1,0,0,0),
vD=(0,0,0,0;       0,1,0,0).                       (8)
```

For `z=C*vC+D*vD`, the three required diagonals are

```text
B01=4(pD-phi*t*C),
A23=-4phi*r*C/p,
B23=4C.                                             (9)
```

Hence common genuineness is exactly

```text
C*p*phi*r*(pD-phi*t*C) != 0.                       (10)
```

## Fixed transverse minor

On the same complete kernel, take the `D01` one-marked map in mode three.
Its rows `1257` and all four target columns have determinant

```text
-64*C*p*(pD-phi*t*C)^2.                            (11)
```

Every factor in (11) is nonzero under (10).  Thus this one-marked map has
rank four on every common genuine extension, whereas an `H22` lift must
factor it through at most three target columns.  This excludes the last
branch of (6).

## Retained failed lemmas

The discovery calculation found an exact low-rank false lead at

```text
h=(-1/r,0,0,0),       [rho:sigma]=[1-phi:phi+1].    (12)
```

Separately, a `D23` binary extension has all four one-marked ranks equal to
three, while a `D01` pure extension has ranks `(2,3,3,3)`.  They are not a
shared pair: their extension vectors differ, and the exact shared projection
(6) excludes (12) generically.  This records why testing the two directions
independently is insufficient.

A single preselected marked mode also fails to close each individual `D23`
binary marking line.  The rank-four obstruction appears only after imposing
the shared pure/binary compatibility and then using the transverse mode in
(11).  No stalled all-minor calculation is used in the certificate.

## Evidence boundary

- The construction-agent discovery was `CANDIDATE`; a fresh verifier has now
  independently reconstructed and promoted the exact claim to `VERIFIED`.
- Both homogeneous weight endpoints are included directly in (4)--(6).
- The result is generic over the component function field.  Special
  parameter divisors and projective component boundaries remain open.
- It makes no component-exhaustiveness, arbitrary-order, prize-graph, or
  global Krenn--Gu claim.

## Replay

```text
uv run --with sympy python claims/p5/h22/common-kernel-vertical-triangle-component-generic/derive_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
uv run --with sympy python claims/p5/h22/common-kernel-vertical-triangle-component-generic/audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
```

The standalone script reconstructs the component basis, checks all six exact
projection ideals bidirectionally, proves completeness of (8), verifies
(9)--(11), and reproduces the unshared low-rank false lead.  The independent
verifier repeats these steps without importing the discovery script.
