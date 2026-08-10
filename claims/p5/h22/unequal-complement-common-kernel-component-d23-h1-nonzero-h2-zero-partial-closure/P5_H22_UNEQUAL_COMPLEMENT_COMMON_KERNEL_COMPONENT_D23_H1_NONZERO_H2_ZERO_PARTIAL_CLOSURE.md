# Component twenty-two finite-D23 H=0, h2=0 partial closure

## Status

**Exact characteristic-zero partial closure theorem.**  A specialized
rational-function-field determinant replay and an independent low-level
matrix reconstruction close the three displayed divisors below.  The earlier
generic polynomial expansion timed out before its first checkpoint; that
failed implementation is not used as evidence.

The target statement works over `K=Q(A,R,D)`, puts `s=2*A+R`, and imposes

```text
H=2*A*h1+1=0,  h2=0,  rho*(rho+1)!=0.             (1)
```

The intended theorem would close exactly the following three divisors inside
(1):

```text
rho=1,     f6=0,     f8=0.                         (2)
```

No binary extension, and hence no weighted-H22 lift, exists on any divisor
in (2).

## Contextual four-factor scout

A separately completed exact scout for the fourteen-by-eight mixed matrix
found that the maximal minor on rows

```text
(0,1,2,3,5,6,7,11)                                (3)
```

is a coefficient-field unit times

```text
rho*(rho-1)*(rho+1)^2*f6*f8*W,                     (4)
```

where

```text
f6=(D-1)*rho+D+1,
f7=(A*D+A+R)*rho+A*D-A-R,
f8=(A*D+A+R*D)*rho+A*D-A+R*D,
W=f7*h0+2*A+R*(1-rho).                             (5)
```

This suggests the contextual rank-drop cover

```text
(rho-1)*f6*f8*W=0.                                 (6)
```

However, a clean integrated replay of this generic six-variable determinant
exceeded 604 seconds under shared CPU contention.  Therefore (4)--(6) are
context only in this package and are not needed for the direct proofs of
(2).

## Three closed divisors

On `rho=1`, rows `(1,2,3,5,6,7,10,11)` give the sole possible factor

```text
q1=D*h0+1.
```

After `q1=0`, rows `(2,3,5,6,10,11,12,13)` have determinant a nonzero
element of `K`.  Hence the `rho=1` divisor is empty.

On `f6=0`, substitute `rho=-(D+1)/(D-1)`.  Rows
`(0,1,2,3,6,7,9,11)` give the sole possible factor

```text
q6=D*s*h0+A-D*(A+R).
```

After `q6=0`, rows `(0,1,2,3,6,7,9,10)` give one linear factor `p6` in
`h3`.  After its exact root is substituted, rows
`(0,1,2,3,6,7,9,12)` have determinant a nonzero element of `K`.  Hence the
`f6=0` divisor is empty.

On `f8=0`, put

```text
rho=-(A*D-A+R*D)/(A*D+A+R*D).
```

Rows `(0,1,2,3,6,7,9,11)` give the sole possible factor

```text
q8=D*R*s*h0-A^2*(D+1)-D*R*s.
```

After `q8=0`, rows `(0,1,2,3,6,7,9,10)` give one linear factor `p8` in
`h3`.  After its exact root is substituted, rows
`(0,1,2,3,6,7,9,12)` have determinant a nonzero element of `K`.  Hence the
`f8=0` divisor is empty.

The primary verifier and no-import audit record every determinant, clearing
factor, and coefficient-field unit exactly.

## Residual on W=0

Every other `h2=0` case remains **UNKNOWN**.  The
contextual scout (6) points to

```text
W=0,  rho*(rho+1)*f6*f8!=0.                        (7)
```

as the remaining branch, but this reduction is not part of the replayable
claim.  A separately completed exact scout found a further fixed minor
whose quotient is a polynomial `P`, linear in `h3`, and suggested the sharper
residual `W=P=0` away from `f7=0`.  That refinement is not part of this
package's replayable theorem: an integrated exact replay exceeded 1204
seconds.  Treat `W=P=0` as contextual symbolic evidence only.

A direct terminal determinant run also exceeded 1204 seconds, a
rowwise-cleared generic determinant exceeded 600 seconds, and a cached exact
interpolation attempt exceeded 1804 seconds before producing its generic
degree/gcd certificate.  These timeouts are not evidence for survival or
emptiness.

## Boundary

This result closes only the three divisors (2) inside the `H=h2=0` slice.
It does not close (7), nor does it promote the contextual `W=P=0` scout to a
theorem.  In the broader `H=0` cover

```text
h2*(s*h2+1)*f7*f8*U*V=0,
```

the other five divisor branches remain **UNKNOWN**; closing the intersection
`h2=f8=0` here does not close the full `f8=0` branch.  Special parameter
fibres, arbitrary source order, other projective charts, and the global
Krenn--Gu conjecture remain **UNRESOLVED**.

No finite field, random sample, or numerical rank calculation is used in
the proof.  Exact rational fibres were used only to discover sparse row
sets.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-h2-zero-partial-closure/verify_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_h2_zero_partial_closure.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-h2-zero-partial-closure/audit_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_h2_zero_partial_closure.py
```

The primary uses exact `DomainMatrix` determinants over specialized rational
function fields.  The audit reconstructs the mixed matrix from the low-level
component model without importing the primary and uses an explicit Gaussian
elimination determinant instead.  Both remain in characteristic zero.
