# Component 19 zero-base valuative reduction: independent verification

```yaml
role: verifier
date_utc: 2026-08-01T19:30:00Z
git_commit: a3d47ed7d9debeaa9ae55c225c71e39ddd6d0116
claim_label: VERIFIED
scope: all characteristic-zero DVR arcs through p=0,q=phi with nonzero residue phi, whose generic point remains in the displayed component-19 chart and has (p,q-phi) not both zero
inputs:
  P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md: ebb4bc46e06b99d4d21e0dff96a35fb071d48dfeceeb926cb4b2643fdeeddbc3
  P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md: 77bad167798b52ca6d623ded47d346255023a13f4122f672ffc485dff9c70f50
method: no-import polynomial-parameter elimination localized on exact opens, complete symbolic kernels, fixed target-local minors, and a generic-point partition over the DVR fraction field
command: uv run --with sympy python claims/p5/h22/component19-zero-base-valuative-reduction/audit_p5_h22_component19_zero_base_valuative_reduction.py
outputs: replay stdout gives final path and sha256 pairs
limitations: displayed component chart and DVR arcs only; no ambient-component, multi-parameter, component-exhaustiveness, or global Krenn-Gu claim
```

## Verdict

**VERIFIED.**  Every such DVR arc has empty weighted-`H22` fibre at its
generic point.  This conclusion does not follow merely from the empty affine
projectivized normal fibre.  It follows from a parameter-aware cover over the
fraction field, including the denominator divisor that the earlier generic
function-field computation missed.

The audit is independent of construction artifacts: it rebuilds the component
rows, contractions, incidence equations, kernels, and minors directly.  It
does not import or execute a construction or candidate module.

## Exact generic-point reduction

Put `r=q-phi`.  For a DVR arc through the zero base with residue `phi_bar!=0`,
both `phi` and `q` are units, while `p,r` lie in the maximal ideal.  On the
fraction field `F`, a nonzero restriction has `(p,r)!=(0,0)`.  Exactly one of
the following occurs.

| Fraction-field case | Complete obstruction |
|---|---|
| `p=0,r!=0` | verified ordinary `p=0` theorem, since `q*phi*r!=0` |
| `r=0,p!=0` | verified `q=phi` theorem on `p*phi!=0` |
| `p*r!=0, phi^2!=1` | new parameter-aware open calculation below |
| `p*r!=0, phi^2=1` | `phi=+1` or `-1`; new parameter-aware endpoint calculation below |

All markings, extension coordinates, and finite weights are allowed to be
arbitrary elements of `F`; weight infinity is checked separately.  Thus poles,
ramification, unequal orders of `p` and `r`, and higher-order cancellations do
not evade this field-valued partition.

## Parameter-aware open and the hidden sheet

The verifier retains `p,q,phi` as polynomial variables and localizes exactly at

```text
S=p*(q-phi)*phi*(phi-1)*(phi+1).
```

It checks all four choices of pure direction and pure diagonal.  At finite
weight, the only nonunit projections are

```text
D01 pure-beta, D23 binary:
  <lambda-1,h3,h1,(q-phi)h0+1>

D01 pure-alpha, D23 binary:
  <lambda+1,h3,h2,h1,q*phi-1,
    (q-phi)h0+1,(phi^2-1)h0-phi>.
```

Both orientations with `D01` binary are unit.  All four orientations at weight
infinity are unit.  These are bidirectional ideal equalities in the localized
polynomial ring, so no unrecorded coefficient-field denominator remains.

The second projection is the hidden sheet lost over `Q(p,q,phi)`.  On it,

```text
q*phi=1,  lambda=-1,  h=(-1/(q-phi),0,0,0).
```

Its complete shared extension kernel is spanned by

```text
(0,1/phi,1,0; 0,0,0,0),
(0,0,0,0;     1,0,0,0),
(p/phi,0,0,0; 0,0,0,1).
```

For coefficients `X,Y,Z`, put

```text
G=p*Z-(phi^2-1)*Y.
```

Genuineness forces `X*G!=0` on the standing open.  Rows `(0,1,3,7)` and
columns `(0,1,2,4)` of the `D23`, mode-three full-target one-marked map have
determinant

```text
64*X^2*p^2*G/phi^3.
```

It is nonzero everywhere genuine, giving the required rank-four obstruction.
The hidden sheet therefore contains no weighted-`H22` lift.

On the first projection the complete two-dimensional extension frame and the
fixed rank-six witness remain valid after localizing at `S`.  Its diagonals are

```text
B01=4*(p*D-phi*t*C),
A23=-4*phi*(q-phi)*C/p,
B23=4*C,
```

and the established fixed one-marked determinant

```text
-64*C*p*(p*D-phi*t*C)^2
```

is nonzero on its genuine locus.

## Endpoint calculation

For each `e=+1,-1`, substitute `phi=e`, `q=e+r`, retain `p,r` as polynomial
variables, and localize only at `p*r`.  At finite weight the sole nonunit
projection is

```text
<lambda-1,h3,h1,r*h0+1>
```

for `D01` pure-beta and `D23` binary.  The other three orientations are unit,
and all four infinity orientations are unit.

The surviving branch has a complete three-dimensional kernel.  With kernel
coordinates `X,Y,Z`, define

```text
F=e*X*r+Z*p,
G=p*r*Y-t*F,
H=X*r+Z*p*r+e*Z*p.
```

Its three required diagonals are `4G/r,-4F/p,4H/r`; hence genuineness is
`F*G*H!=0`.  The fixed `D23`, mode-three full-target minor is

```text
64*F^2*H/r^2,
```

which excludes the complete branch.  This is polynomial-parameter evidence,
not an extension of a result proved only over a generic coefficient field.

## Why the naive normal-fibre properness argument is insufficient

Blowing up `(p,r)` regularizes the intrinsic pure row.  On the `p`-chart
`p=s,r=s*x`, use `alpha_p=x*u-v,beta_p=u`; on the `r`-chart
`r=t,p=t*y`, use `alpha_r=u-y*v,beta_r=v`.  On `xy=1`,

```text
alpha_r=y*alpha_p,
beta_r=x*beta_p-alpha_p.
```

For markings `m=beta+h*alpha` and fifth coordinates `(C,E)`, the transitions
are

```text
h_p=(-1+y*h_r)/x,
C_r=y*C_p,
E_r=x*E_p-C_p,
D_r=x*D_p,  where D=E+h*C.
```

Thus markings and extensions are twisted projective-bundle data, not a fixed
affine product.  Homogeneous weight is already a `P1`, but genuineness is an
open condition and the extension kernels are not a uniform vector subbundle.
A closed projective kernel incidence can be formed, yet its boundary must be
computed after saturation by marking independence and all required diagonals.
Empty affine normal charts alone do not establish that saturated boundary is
empty.

For example, on the ordinary shared branch take

```text
p=r=tau, C=D=1, t=0.
```

Then `h0=-1/tau` and the projective extension vector is

```text
[0,-1/tau,phi/tau,0;1,1,0,0]
  -> [0,-1,phi,0;0,0,0,0].
```

Along this profile `B01=4*tau` and the fixed obstruction is `-64*tau^3`, so
both vanish at the compactification boundary even though the obstruction is
nonzero at every generic point.  This explains why a normal-fibre argument
needs closure data.  The fraction-field cover above avoids that missing step.

## Evidence boundary and replay

The verified conclusion is component-local.  It covers arbitrary-order and
ramified DVR arcs inside the displayed component chart, but not arcs entering
from another component, non-diagonal ambient source deformations, or
multi-parameter families.

```powershell
uv run --with sympy python claims/p5/h22/component19-zero-base-valuative-reduction/audit_p5_h22_component19_zero_base_valuative_reduction.py
uv run --with ruff ruff check claims/p5/h22/component19-zero-base-valuative-reduction/audit_p5_h22_component19_zero_base_valuative_reduction.py
python -m py_compile claims/p5/h22/component19-zero-base-valuative-reduction/audit_p5_h22_component19_zero_base_valuative_reduction.py
git diff --check
```
