# Independent verification: component 19, `q=0`, `phi=+/-1`

```yaml
role: verifier
date_utc: 2026-08-01T15:42:49Z
git_commit: 7dc8acbc6186f84c6c9d78cab4f7be5c46e727cf
claim_label: VERIFIED
scope: component 19 q=0 weighted-H22 endpoint obstruction at phi=+1 and phi=-1 over Q(p), p!=0, including finite and projective-infinity weighted directions
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: separate exact reconstruction for epsilon=+1,-1; bidirectional function-field elimination; complete 28x8 shared-kernel calculation; exact diagonal forms; fixed one-marked rank minor; direct-D01 constructible-slope audit
command: uv run --with sympy python audit_p5_h22_component19_q0_phi_endpoints_obstruction_candidate.py
outputs:
  - audit_p5_h22_component19_q0_phi_endpoints_obstruction_candidate.py sha256=8043c26ef7fb214033f8982c215fa21eb8fe0d9412ae10a46bb00e06382cb4a7
  - P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_OBSTRUCTION_VERIFICATION.md
limitations: p=0 is excluded; no claim is made for other q=0 divisors, other component parameters, component exhaustiveness, arbitrary-order reduction, or the global Krenn-Gu conjecture
```

## Verdict

The frozen endpoint claims are **VERIFIED** separately for

```text
epsilon=+1, phi=epsilon, p!=0,
epsilon=-1, phi=epsilon, p!=0.
```

The audit did not read, import, or execute the endpoint candidate, discovery
script, certificate, or endpoint proof-B artifacts.  It is standalone and
reconstructs the marked rows from the component source.

## Exact endpoint projections

All projected ideals were checked in both containment directions over
`Q(p)`.  For either sign `epsilon`, the direct marking-closure ideals are

```text
D01 finite:    <p*h3+1, h1, h0-epsilon>,
D01 infinity:  <p*h3+1, h1, h0-epsilon>,

D23 finite:
<h3, h0-epsilon, h1*h2*(lambda-1), h1^2*h2>,

D23 infinity:
<h3, h0-epsilon, h1*h2>.
```

Imposing both mixed systems while retaining a genuine `D23` binary neighbour
gives exactly

```text
shared finite:
<lambda-1, h3, h1, h0-epsilon>,

shared infinity:
(1).
```

Thus the unique shared finite marking branch is

```text
lambda=1, h=(epsilon,0,t,0),
```

and there is no shared projective-infinity incidence.

## Complete endpoint kernel

Order extension coordinates as
`(x0,x1,x2,x3;y0,y1,y2,y3)` after selecting the marked rows.  On the shared
finite branch, the stacked `28 x 8` mixed matrix has the complete kernel

```text
z=C*vC+D*vD+E*vE,

vC=(0,-1/p,epsilon/p,0; 1,0,0,0),
vD=(0,0,0,0; 0,1,0,0),
vE=(epsilon*p,0,-epsilon,0; 0,0,0,1).
```

Rows `(1,2,10,12,15)` and columns `(0,1,2,3,6)` have determinant

```text
1024*p^3
```

for both signs.  Hence the matrix has rank five and the displayed three-frame
is complete, including `t=0`.

Put `Q=C-pE`.  The four diagonal forms are exactly

```text
A01 = 0,
B01 = 4*(pD-epsilon*tQ),
A23 = 4Q/p,
B23 = 4C.
```

The three non-identically-zero required factors are simultaneously nonzero
exactly when

```text
C*Q*(pD-epsilon*tQ) != 0.
```

The identity `A01=0` is the required pure `D01` polarity, while the other
three factors define the common genuine open.  It does not by itself obstruct
the surviving orientation; the one-marked rank certificate below does.  A
genuine shared `D23` binary neighbour alone has `C*Q!=0`.

## Fixed rank-four obstruction

For the standard finite-`D23`, mode-three one-marked `8 x 4` map, the fixed
row-`0237` determinant is

```text
-64*epsilon*C*Q^2.
```

It is nonzero on every genuine shared `D23` neighbour.  Thus that map has rank
four and cannot factor through three target coordinates.  This independently
corroborates the endpoint obstruction without relying only on `A01=0`.

## Direct `D01` false leads and projective slope boundary

The direct `D01` marking closure is the distinct branch

```text
h=(epsilon,0,t,-1/p),
```

so it cannot meet the shared finite branch, which has `h3=0`.  Its finite
mixed matrix has the fixed rank-six witness

```text
64*p^4*(lambda-1)^2*(lambda+1)^4
```

on `lambda^2!=1`.  Both diagonal functionals are nonzero there, so genuine
direct binary extensions exist, but they are unshared false leads.

The elimination ideal above is the Zariski closure of this constructible
image.  At the omitted finite slopes themselves:

```text
lambda=+1: rank 4, fixed minor 256*epsilon*p^3, A01 identically zero;
lambda=-1: rank 3, fixed minor -64*p^3, B01 identically zero.
```

Neither slope is a genuine binary incidence.  At projective infinity the
mixed rank is six, witnessed by `64*p^4`, and both diagonal functionals are
nonzero; genuine direct `D01` extensions exist there, but the exact shared
infinity ideal is `(1)`.  This keeps incidence, its projection closure, and
rank-drop boundary points distinct.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/component19-q0-phi-endpoints/audit_p5_h22_component19_q0_phi_endpoints_obstruction_candidate.py
```

Expected final marker:

```text
ENDPOINT_AUDIT_VERIFIED
```

The replay uses bounded, file-backed Singular eliminations, removes temporary
solver inputs, and performs exact characteristic-zero calculations rather
than finite-field sampling or broad search.
