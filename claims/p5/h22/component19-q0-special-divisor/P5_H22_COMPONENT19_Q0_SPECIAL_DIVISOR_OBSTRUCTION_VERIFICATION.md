# Independent verification: component 19, `q=0`, weighted `H22`

```yaml
role: verifier
date_utc: 2026-08-01T15:34:33Z
git_commit: 6e6e02ad34c8462f2fc08087ee6fc73e3e543f28
claim_label: VERIFIED
scope: component 19 q=0 weighted-H22 obstruction over Q(p,phi) on p*phi*(phi^2-1)!=0, including finite and projective-infinity weighted directions
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  - P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md sha256=5b1c85f89cd45b9c8f8d0604566145b4b7cd765d4cb350119d1bbf73b365e685
  - P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md sha256=28aa991219f090e82bd9a5cfc682cb12cf980eb12b437aa8bfdebddd1b10b3a8
method: independent reconstruction of q=0 marked bases; exact squarefree permanents; bidirectional Singular ideal comparison over Q(p,phi); complete shared-kernel frame; fixed one-marked rank minor; explicit false-lead and boundary attacks
command: uv run --with sympy python audit_p5_h22_component19_q0_special_divisor_obstruction_candidate.py
outputs:
  - audit_p5_h22_component19_q0_special_divisor_obstruction_candidate.py sha256=a62f0ca7cecce673561c3ab431b890c6ed7ac64521797a3d1326bcfd7b4c39ef
  - P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_VERIFICATION.md
limitations: phi=+1 and phi=-1 are excluded because the shared mixed rank drops from 6 to 5; p=0 is the zero-tensor boundary and phi=0 is outside the component chart; no claim is made for those boundaries, other component divisors, component exhaustiveness, arbitrary-order reduction, or the global Krenn-Gu conjecture
```

## Verdict

The frozen `q=0` claim is **VERIFIED** on

```text
p*phi*(phi^2-1) != 0.
```

The audit was written without reading, importing, or executing the candidate,
proof-B, certificate, or generic component-19 `H22` artifacts.  It reconstructs
the bases directly from the component theorem and uses only the standard
weighted-`H22` definitions in the two cited background reports.

## Reconstructed component data

With the independent orientation used by the audit, the only pure coefficient
is

```text
T_1111 = 4p,
```

and the exterior pair profile in edge order `01,02,03,12,13,23` is exactly

```text
(3,4,4,3,3,3).
```

Fixed nonzero rank witnesses returned by the replay are

```text
-4p^2 phi,  8p^3,  -8p^2 phi,  -4,  4phi,  4phi.
```

## Exact binary and shared projections

Every displayed equality below was checked in both ideal-containment
directions after eliminating all eight extension coordinates and the relevant
normalization/inverse variable over `Q(p,phi)`.

The finite and infinite `D01` binary incidence ideals are both

```text
(1).
```

Thus “empty” here means an empty incidence, not a zero projection ideal.  This
alone is already a complete weighted-`H22` obstruction in the stated open.

The direct `D23` projections are

```text
finite:
<h3, phi*h0-1, h1*h2*(lambda-1), h1^2*h2>,

infinity:
<h3, phi*h0-1, h1*h2>.
```

The audit separately reduces `h1^2*h2` modulo the other three finite
generators and obtains a nonzero remainder.  That generator is therefore
scheme-theoretically essential; omitting it changes the projected ideal.

For the system imposing both mixed kernels while retaining a genuine `D23`
binary neighbour, the projections are

```text
finite:
<lambda-1, h3, h1, phi*h0-1>,

infinity:
(1).
```

Normalizing the `D23` all-alpha diagonal and inverting its all-beta diagonal
is important here.  The larger shared-mixed rank-drop locus at `lambda=-1`
is not a binary neighbour: its `D23` all-alpha diagonal vanishes on every
kernel vector.

## Complete finite shared frame and rank attack

Put

```text
lambda=1,  h=(1/phi,0,t,0),
z=C*vC+D*vD,
```

where extension coordinates are ordered
`(x0,x1,x2,x3,y0,y1,y2,y3)` and

```text
vC=(0,-1/p,phi/p,0,1,0,-phi*t/p,0),
vD=(0,0,0,0,0,1,0,0).
```

Both vectors lie in the stacked mixed kernel.  Rows
`(1,2,4,10,12,15)` and columns `(0,1,2,3,6,7)` have determinant

```text
4096*p^4*phi^2*(phi-1)*(phi+1),
```

so the stacked matrix has rank six and this two-frame is the complete kernel
throughout the stated open, including `t=0`.

On this frame the four diagonals `(A01,B01,A23,B23)` are

```text
(0, 4*(pD-phi*tC), 4*C*phi^2/p, 4*C).
```

The identically zero `A01` is the concrete reason the direct `D01` incidence
is empty.  As an independent supplementary Fitting check, form the standard
`D01` mode-three one-marked `8 x 4` map.  Its row-`1257` minor is exactly

```text
-64*C*p*(pD-phi*tC)^2.
```

Hence it has rank four whenever `C*(pD-phi*tC)` is nonzero.  This rank
certificate is supplementary; the global obstruction on the whole frozen
open comes from the exact `D01` unit ideals and does not silently discard the
minor's vanishing sublocus.

## False lead and boundary attacks

At

```text
lambda=0, h=(1/phi,0,1,0),
z=(0,1,0,0,1,0,1,0),
```

all `D23` mixed coefficients vanish and its two diagonals are

```text
-2phi,  -2(phi-1),
```

so this is a genuine direct `D23` extension on the open.  Several `D01`
mixed coefficients are nonzero, and the exact shared projection forces
`lambda=1`; it is therefore an unshared false lead, not an `H22` lift.

Finally, specialization to either `phi=1` or `phi=-1` lowers the shared mixed
rank from six to five.  The complete two-frame and its completeness minor no
longer apply.  Those endpoints are correctly excluded rather than promoted
to the verified theorem.

## Replay

```powershell
uv run --with sympy python audit_p5_h22_component19_q0_special_divisor_obstruction_candidate.py
```

Expected terminal marker:

```text
AUDIT_VERIFIED
```

The replay uses file-backed Singular jobs with bounded runtime and removes its
temporary solver inputs.  The result is a characteristic-zero function-field
calculation, not a finite-field audit and not a broad search.
