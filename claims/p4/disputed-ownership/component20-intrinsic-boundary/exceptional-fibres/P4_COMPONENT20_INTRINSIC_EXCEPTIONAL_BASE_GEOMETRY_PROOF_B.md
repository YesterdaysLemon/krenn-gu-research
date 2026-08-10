# Proof-B analysis of component-twenty intrinsic exceptional base geometry

```yaml
role: proof_b
date_utc: 2026-08-01T13:58:27Z
git_commit: 00c3574f854e1f86cb8ec2304645204479c3f75e
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: component-20 intrinsic-wall exceptional base geometry at p=0,-1,-1/2, including exact s=0 diagonal-DVR arcs only
inputs:
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
method: fresh subset-algebra permanent reconstruction, polynomial Pluecker extension, transverse base-ideal Jacobian, and exact four-region min-plus proof
command: uv run --with sympy python claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py
outputs:
  derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py: hash reported by replay
  P4_COMPONENT20_INTRINSIC_EXCEPTIONAL_BASE_GEOMETRY_PROOF_B.md: hash reported by replay
limitations: no arbitrary or non-diagonal source arcs; no complete source-torus atlas at p=0 or p=-1; no component-intersection classification, H31, H22, component exhaustiveness, arbitrary-order reduction, prize graph, or global Krenn-Gu conclusion
```

## Result

**VERIFIED after an independent no-import reconstruction.**  The three
excluded values on the intrinsic wall `q=p+1` have two different geometric
meanings.

- At `p=0,-1`, the four-plane map is regular, but its restricted `P4` tensor
  is zero.  These are two ordinary transverse base points of the projective
  pure-factor map.  Its resolution has an exceptional `P1` at each point.
- At `p=-1/2`, the displayed row basis for `U0` has a pole, but the
  Grassmann-valued plane map extends regularly.  Its straight fixed-source
  limit is again a zero-restriction point, with pair profile
  `(3,3,2,3,3,3)`.  It is a formal `k=infinity` edge, not one of the actual
  nonzero-`P4` wall strata.
- Every exact `s=0` **diagonal-DVR arc whose limiting `P4` restriction is
  nonzero** satisfies the same valuation cone and has the same leading planes
  as the already recorded half-centre `p+q=0` atlas.  Thus no new diagonal
  blow-up chart is needed at `p=-1/2`.  This says nothing about arbitrary or
  non-diagonal source arcs.

No `H31` or `H22` conclusion is drawn from these structural statements.

## The two ordinary base points

Put

```text
delta=p+q,                 s=p-q+1.
```

On `delta!=0`, the normalized family has only

```text
T0111=2s,                  T1111=-2q(q-1).            (1)
```

The base ideal of the projective pure-factor map is therefore

```text
I=(s,q(q-1)).                                       (2)
```

On the intrinsic wall `s=0`, its two points with `delta!=0` are

```text
(p,q)=(0,1),             (p,q)=(-1,0).              (3)
```

The Jacobian of `(s,q(q-1))` with respect to `(p,q)` is

```text
[ 1   -1   ]
[ 0  2q-1 ],
```

whose determinants at (3) are respectively `1` and `-1`.  Thus both base
points are reduced transverse complete intersections.  Blowing up (2)
introduces an ordinary projective line of first-order pure directions at
each point.

This base locus is not a singularity of the four-plane map.  A polynomial
homogeneous representative for its mode-zero plane is

```text
P0=(p(p+1),-q(q-1),-s,delta^2,-delta,delta)          (4)
```

in Pluecker order `(01,02,03,12,13,23)`.  The replay checks

```text
P01 P23-P02 P13+P03 P12=0
```

identically and verifies that (4) is nonzero at both points in (3).  Direct
permanent expansion of all sixteen coefficients at each four-plane point is
zero.

For first-order arcs

```text
(p,q)=(P t,1+Q t),             (p,q)=(-1+P t,Q t),
```

the leading coefficient pairs from (1) are

```text
(2(P-Q),-2Q),                  (2(P-Q),2Q).           (5)
```

They sweep the full exceptional `P1`.  Exact intrinsic arcs have `P=Q` and
select the single direction `[0:1]` at both points.  The exceptional-centre
analysis in the `p+q=0` atlas does not cover these two base points: here
`delta` is a unit.  A complete source-torus or non-diagonal valuative atlas
over (3) remains to be constructed.

## The half-centre Grassmann limit

Near the intersection of `s=0` and `delta=0`, use

```text
p=(delta+s-1)/2,        q=(delta-s+1)/2,
a=p(p+1),               g=q(q-1).
```

Since `a=-1/4` at the origin, the following pivot-`01` basis is regular:

```text
U0=< (1,0,-delta^2/a,delta/a),
      (0,1,-g/a,-s/a) >.                             (6)
```

With the unchanged regular bases of `U1,U2,U3`, all sixteen permanent
coefficients reduce to the single identity

```text
T0111=-2 delta.                                     (7)
```

At `delta=s=0`, equation (6) gives

```text
U0=<e,A-B>,
U1=<e,(A-B)/2+C>,
U2=<e,-(A-B)/2+C>,
U3=<e,A+B>.                                         (8)
```

The replay verifies directly that (8) has zero restricted tensor and pair
profile

```text
(3,3,2,3,3,3).                                     (9)
```

For the straight fixed-source arc `delta=Delta t^d`, `s=0`, one has
`x0=x1=x2=0`.  The exact valuation below gives `E=d>0`, so (8) is a
zero-tensor limit rather than an actual nonzero-`P4` boundary stratum.  In
the finite-`k` wall coordinates it is naturally viewed as the missing
formal `k=infinity` edge.  It must not be merged into the verified actual
wall atlas.

## Exact diagonal-DVR specialization at `s=0`

Now take

```text
delta=Delta t^d,       s=0,       d>0,
D=diag(c0 t^x0,c1 t^x1,c2 t^x2,1).
```

In the regular basis (6), let

```text
n=min(x1,x2),       w=|x1-x2|,
m=min(n,0),         z=min(x0,n),
a0=min(x0,d,2d+x2).
```

The row-normalization-invariant valuation of the sole pure coefficient is

```text
E=d+n+w-2m+z-a0.                                   (10)
```

There is a compact exhaustive proof of its zero set.  In the four regions
cut out by the signs of `n` and `x0-n`, equation (10) is respectively

| region | exact expression |
| --- | --- |
| `n>=0, x0<=n` | `(d+n+w)+(x0-a0)` |
| `n>=0, x0>=n` | `(2n+w)+(d-a0)` |
| `n<0, x0<=n` | `(d-n+w)+(x0-a0)` |
| `n<0, x0>=n` | `w+(d-a0)` |

In the two `x0<=n` regions, `a0<=x0`, so the expressions are strictly
positive.  In the other two, `a0<=d`.  Equality in the `n>=0` region forces
`n=w=0` and `a0=d`, hence `x1=x2=0` and `x0>=d`.  Equality in the `n<0`
region forces `w=0` and `a0=d`, hence `x1=x2=n`, `n>=-d`, and `x0>=d`.
Conversely these conditions make (10) zero.  Therefore

```text
E=0 iff x1=x2=y,       -d<=y<=0,       x0>=d.       (11)
```

This proof is exact min-plus algebra; it uses neither a grid nor a finite
field.

## Match to the existing half-centre atlas

Put

```text
L=c1 A-c2 B,             M=c1 A+c2 B,
k=c0/(4 Delta),
eps_x=[x0=d],             eps_y=[y=-d].
```

For `y<0`, direct leading-term extraction from the polynomial Pluecker vector
(4) gives

```text
U0=<L,C-eps_x k e-(eps_y Delta/2)M>,
U1=U2=<e,L>,
U3=<e,M>.                                           (12)
```

Equivalently, the four mode-zero vectors are

```text
(eps_x k c1,-eps_x k c2,0,
 -eps_y Delta c1 c2,c1,-c2).                        (13)
```

The replay reconstructs all four flags in (13), checks the Pluecker relation,
and finds the sole pure coefficient `T1110=-2c1c2`.  These are exactly the
embedded-`P3` half-centre flags already recorded in the diagonal wall atlas.

For `y=0`, equation (11) leaves two charts:

```text
x0=d:  U0=<L,C-k e>,
x0>d:  U0=<L,C>,

U1=<e,L/2+C>,
U2=<e,-L/2+C>,
U3=<e,M>.                                           (14)
```

Their sole pure coefficient in the displayed bases is `T1110=c1c2/2`.
These are the finite-`k` half-centre `B_drop`-type charts already recorded in
the same atlas.  Equations (11)--(14) justify only the exact `s=0` diagonal
specialization: they do not enlarge the published atlas to non-diagonal
source changes.

## Evidence boundary

- The two ordinary base points require a projective pure-direction blow-up,
  even though no new Grassmann chart is needed there.
- Their complete source-torus boundary, intersections with other named
  components, and all non-diagonal arcs remain `UNKNOWN`.
- At the half centre, the straight fixed-source `k=infinity` edge is retained
  as a zero-tensor limit and is not counted as an actual nonzero-`P4` wall
  stratum.
- Exact `s=0` diagonal arcs with `E=0` require no new chart beyond the existing
  finite-`k`/embedded-`P3` atlas.  Arbitrary source `GL4` arcs remain
  `UNKNOWN`.
- This report proves no marked `H31` or weighted `H22` obstruction and makes
  no global Krenn--Gu claim.

## Replay

```text
uv run --with sympy python \
  claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py

uv run --with sympy --with z3-solver python \
  claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/audit_component20_intrinsic_wall_exceptional_fibres_candidate.py
```

The replay is exact over characteristic zero and imports no other research
script.  The independent audit reconstructs the base geometry and exact
diagonal half-centre cone before comparing this proof-B artifact.
