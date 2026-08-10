# Component 19 `p=0` finite-boundary geometry reconnaissance

```yaml
role: verifier
date_utc: 2026-08-01T15:59:20Z
git_commit: 7a3eea50e311a163765750fa5f22f9d2b5c1b98e
claim_label: VERIFIED
scope: ordinary finite component-19 geometry on p=0, its exact zero-restriction base, pair-rank strata, and projectivized first-order normal tensor directions; weighted-H22 incidence remains UNKNOWN
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: independent squarefree-permanent reconstruction, exact symbolic pair minors and ranks, zero-ideal Groebner basis, Jacobian normal-space calculation, and explicit first-order arcs
command: uv run --with sympy python claims/p5/h22/component19-p0-finite-boundary-geometry-reconnaissance/audit_p4_component19_p0_finite_boundary_geometry.py
outputs:
  - audit_p4_component19_p0_finite_boundary_geometry.py sha256=c8bf03247889d9c28dd72adbaa084868b295aedbb5db51362066f0cb04358a5a
  - P5_H22_COMPONENT19_P0_FINITE_BOUNDARY_GEOMETRY_RECONNAISSANCE.md
limitations: no weighted-H22 incidence was constructed or excluded; no other Grassmann chart or projective opposite-plane endpoint was audited; higher-order arcs with zero first normal direction remain untreated; phi=0 is outside the component chart
```

## Status

The ordinary finite `p=0` geometry and its first normal-direction fibre are
**VERIFIED**.  Weighted `H22` on this boundary remains **UNKNOWN**.

This audit did not inspect or execute any `p=0` construction, candidate,
proof-B, or certificate artifact.  It reconstructs the geometry only from the
component theorem.

## Ordinary finite restriction

In the displayed finite family basis, the complete restriction has only

```text
T_0111=4p,
T_1111=4(q-phi).
```

Therefore setting `p=0` does **not** make the ordinary restriction identically
zero.  It leaves

```text
T_1111=4(q-phi).
```

Consequently:

- `p=0,q!=phi` is an ordinary nonzero pure restriction; no degenerating
  generic pure-basis formula is needed to see it.
- `p=0,q=phi` is the exact zero-restriction locus in the `p=0` divisor.

Over the whole finite chart, the tensor-coefficient ideal is exactly

```text
<p,q-phi>.
```

Its Jacobian with respect to `(p,q,phi)` has rank two, with a fixed unit
minor.  The zero base is therefore a smooth codimension-two locus, not an
embedded or multiplicity-only artefact.

## Exact pair ranks on `p=0`

For generic `q,phi`, the pair profile in edge order
`01,02,03,12,13,23` is

```text
(3,3,4,3,3,3).
```

The complete finite stratification needed here is:

- Edge `01` has rank three for `q!=0`, witnessed by `4q`, and rank exactly
  two at `q=0`.
- Edge `02` has rank three throughout this finite chart.
- Edge `03` has rank four off

  ```text
  (q-phi)*(phi*q-1)=0,
  ```

  witnessed by `-8(q-phi)(phi*q-1)`.
- On `q=phi`, edge `03` has rank three for `phi^2!=1`, witnessed by
  `-4(phi^2-1)`.
- On `phi*q=1`, it has rank three for `phi^2!=1`; one witness is
  `4(phi-1)(phi+1)^2/phi`.
- At `(q,phi)=(1,1)` and `(-1,-1)`, edge `03` has rank exactly two.
- Edges `12,13,23` have rank three on the component chart `phi!=0`.

Thus the nonzero ordinary `p=0` family is all-pair-open exactly when

```text
phi!=0, q!=0, q!=phi.
```

The divisor `phi*q=1`, away from `phi^2=1`, merely changes its profile to
`(3,3,3,3,3,3)` and stays all-pair-open.

At the zero-restriction base `p=0,q=phi`:

```text
phi^2!=1: profile (3,3,3,3,3,3), but the tensor is zero;
phi=+/-1: profile (3,3,2,3,3,3), and the tensor is zero.
```

The formal `phi=0,q=0` limit has profile `(2,3,3,3,3,2)`, but `phi=0` is
outside the component chart and is not promoted to an ordinary component
point.

## Projectivized first-order tensor directions

Take a general first-order arc through a zero-base point
`p=0,q=phi=r`:

```text
p(u)=a*u,
q(u)=r+(b+c)*u,
phi(u)=r+c*u.
```

The common `c` direction is tangent to the zero base.  The first nonzero
normal tensor term is

```text
4a*T_0111 + 4b*T_1111.
```

Because `<p,q-phi>` is a regular sequence of length two, its normal space has
basis `(a,b)` and its projectivization is exactly

```text
P^1_[a:b].
```

Every point of this `P^1` is realized by an explicit linear arc.  This is a
verified first-order tensor-direction fibre, not an ordinary tensor fibre at
the zero base.

## Separation of boundaries

### Finite ordinary points

The statements above concern only the displayed affine Grassmann chart and
literal finite parameter values.  Nonzero points with `p=0,q!=phi` remain
ordinary restrictions.  Points with `p=0,q=phi` have zero restriction.

### Exceptional or projective geometry

The `P^1_[a:b]` above is the exceptional fibre of the first normal
projectivization of the zero ideal.  It is not one of the ordinary finite
four-plane tuples and is not a checked endpoint on either omitted Grassmann
chart.  No projective opposite-plane completion is claimed here.

### Valuative arcs

The calculation records only arcs whose first normal pair `(a,b)` is nonzero.
It does not classify higher-order or ramified arcs with `a=b=0`, compare
different arc valuations, or prove that a first-order tensor direction carries
a compatible marked extension.  Those are separate valuative problems.

## Weighted-`H22` boundary

No weighted-`H22` conclusion follows merely from the ordinary zero tensor or
from its normal `P^1`.  A future incidence audit must choose the correct
regular marked bases along each direction, cover finite and infinite weights,
and keep ordinary and valuative extensions distinct.  Until then:

```text
weighted H22 on the p=0 boundary: UNKNOWN.
```

## Replay

```powershell
uv run --with sympy python claims/p5/h22/component19-p0-finite-boundary-geometry-reconnaissance/audit_p4_component19_p0_finite_boundary_geometry.py
```

Expected final markers:

```text
FINITE_P0_GEOMETRY_VERIFIED
WEIGHTED_H22_STATUS_UNKNOWN
```
