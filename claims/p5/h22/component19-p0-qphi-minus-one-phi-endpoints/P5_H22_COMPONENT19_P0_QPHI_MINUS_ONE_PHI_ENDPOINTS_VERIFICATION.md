# Independent verification of the `q*phi=-1`, `phi^2=1` intersections

```yaml
role: verifier
date_utc: 2026-08-01T16:54:04Z
git_commit: 565e1a39cf34228c8bf3fe598eab9485720c175d
claim_label: VERIFIED
scope: complete finite ordinary component-19 p=0 intersections q*phi=-1 and phi^2=1, namely (q,phi)=(1,-1),(-1,1)
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: fresh regular-basis reconstruction, three-diagonal-saturated incidence elimination, complete shared kernel, exhaustive local maximal minors, fixed exact rank witnesses, and full 8x5 two-slice compatibility
command: uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-phi-endpoints/audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py
outputs:
  audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py: 89dbecbcf37a5a9afdf5ca50ec26e67ae2b2cf5fdfefc2ef23fdd575dd257327
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md: hash emitted by replay
limitations: finite ordinary lambda chart at the two stated parameter points; no weight-infinity/projective boundary, other parameter fibre, other component, arbitrary-order reduction, or global claim
```

## Verdict

The two previously excluded finite ordinary intersections are **VERIFIED
closed**.  They have a genuine survivor jump that must not be reduced to the
older `X=0` and `Z=0` axes: every point of a full non-axis `Y=0` sheet passes
all eight individual one-marked rank tests.  Nevertheless, a uniform full
two-slice stacked determinant obstructs that entire sheet.

There is no remaining `UNKNOWN` locus in this frozen finite ordinary scope.
The global Krenn--Gu conjecture remains unresolved.

## Complete genuine shared incidence

Put `phi=+1` or `-1` and `q=-phi`.  In each endpoint fibre, exact elimination
of all eight extension coordinates after normalizing `A23=1` and inverting
both `B01` and `B23` gives, in both ideal-containment directions,

```text
<lambda-1, h3, h1, h0>.
```

Thus the complete genuine finite marking branch is

```text
lambda=1,              h=(0,0,t,0).
```

No additional endpoint marking component occurs.

Order extensions as `(x0,x1,x2,x3;y0,y1,y2,y3)`.  The complete shared kernel
is

```text
z = X vX + Y vY + Z vZ,

vX=(0, phi/2,-1/2,0;1,0,0,0),
vY=(0, 0,    0,  0;0,1,0,0),
vZ=(0,-1/2,-phi/2,0;0,0,0,1).                    (1)
```

The stacked `28 x 8` mixed matrix has rank five.  Rows
`(2,9,10,12,15)` and columns `(0,1,2,3,6)` give the fixed determinant

```text
4096*phi,
```

so (1) is complete at both endpoints.

Define

```text
F=phi*X+Z,
G=-2*phi*Y-tF,
H=X-phi*Z.
```

Direct reconstruction gives

```text
(A01,B01,A23,B23)=(0,4G,2phi*F,4H),
```

and the genuine open is exactly `F*G*H!=0`.

## The full individual-rank survivor jump

Among all eight one-marked projected maps, the fixed `D23`, mode-two minor on
rows `0127` is

```text
-32*Y*F*H.                                         (2)
```

Therefore individual rank at most three forces `Y=0` on the genuine open.
Conversely, direct evaluation of every `4 x 4` maximal minor of all eight maps
shows that they all vanish identically when `Y=0`.  Fixed lower-rank witnesses
then give the exact profiles, throughout the same open,

```text
D01 modes 0,1,2,3: (3,1,1,3),
D23 modes 0,1,2,3: (3,3,3,3).
```

On `Y=0`, one has `G=-tF`, so the complete individual-rank survivor locus is

```text
Y=0,              t*F*H != 0.                     (3)
```

Projectively, `[X:Z]` ranges over the whole line with only the two points
`F=0` and `H=0` removed, while `t!=0`.  In particular, (3) includes the dense
non-axis locus `X*Z!=0`; the older two axes are only two special subfamilies.

## Full target-local compatibility obstruction

Let `N01_i,N23_i` be the full `8 x 5` one-marked maps for contraction rows

```text
q01=(1,1,0,0,0),       q23=(0,0,1,1,0).
```

A common three-column local reconstruction at mode `i` is a solution of

```text
N01_i=U01_i R_i,       N23_i=U23_i R_i,
```

with one shared `R_i` in `Mat(3,5)`.  This is equivalent to

```text
rank stack(N01_i,N23_i) <= 3.                      (4)
```

The verifier reconstructs the full maps by complementary cofactors and checks
their exact projection identities with the eight maps above.  At mode one,
stacked rows `(7,8,9,15)` and source columns `(0,1,2,3)` have determinant

```text
-16*F^3*H.                                         (5)
```

Equation (5) is nonzero everywhere on (3).  Hence no point of the enlarged
individual-rank sheet admits the required common local factorization, and no
finite ordinary weighted-`H22` lift survives at either endpoint.

## Evidence boundary and replay

- All identities are over characteristic zero.  No finite field or parameter
  grid is used.
- The complete local maximal-minor enumeration is bounded to the eight exact
  `8 x 4` maps; it is not a broad parameter search.
- No new q-endpoint exploration, candidate, construction, or proof-B artifact
  is read or imported.
- Weight infinity and other projective boundaries are outside this theorem.

Replay with

```powershell
uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-phi-endpoints/audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py
```
