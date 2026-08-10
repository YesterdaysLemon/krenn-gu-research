# Component 19 zero base: first-normal `P1` and weighted `H22` - CANDIDATE

```yaml
role: construction
date_utc: 2026-08-01T17:32:50Z
git_commit: ac0853455c978628c6f685e826f78275591d639a
claim_label: CANDIDATE
scope: component 19 at Z0={p=0,q=phi=r}, r!=0; exact first-normal P1 and regular first-normal weighted-H22 incidence
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMPONENT19_P0_FINITE_BOUNDARY_GEOMETRY_RECONNAISSANCE.md: a22b55ec24747983b60a5d479e93c012d8018871123d3ec1c80bf5d03a65c335
method: direct normal-jet permanents, two regular normal-direction charts, exact pair ranks, structural D01 syzygies, and bounded characteristic-zero elimination
command: uv run --with sympy python claims/p5/h22/component19-zero-base-first-normal/derive_p5_h22_component19_zero_base_first_normal_candidate.py
outputs:
  - P5_H22_COMPONENT19_ZERO_BASE_FIRST_NORMAL_CANDIDATE.md
  - p5_h22_component19_zero_base_first_normal_geometry_certificate.json
  - p5_h22_component19_zero_base_first_normal_incidence_certificate.json
  - derive_p5_h22_component19_zero_base_first_normal_candidate.py
limitations: construction result pending independent verification; actual higher-order valuative H22 arcs remain UNKNOWN
```

## Frozen result

**CANDIDATE:** the exact projectivized first-normal tensor fibre over the zero
base is `P1_[a:b]`.  Every direction has an all-pair-open transverse linear
arc for `r!=0`.  After aligning the first-normal pure tensor on two regular
direction charts, the `A01`-binary orientation is structurally impossible.
A complete four-open shared-incidence cover is empty on both homogeneous
weight charts.  Hence the regular first-normal weighted-`H22` incidence is
empty.

This does not promote the global conjecture or exclude every higher-order
valuative `H22` arc.

## Exact normal tensor

In the displayed component basis, direct permanent expansion has exactly

```text
T0111=4p,
T1111=4(q-phi).
```

Thus the zero ideal is the verified regular sequence

```text
I(Z0)=<p,q-phi>.
```

For a general transverse arc

```text
p=a*eps+...,
q=r+(b+c)*eps+...,
phi=r+c*eps+...,
```

the tangent coordinate `c` cancels, and the first normal tensor is

```text
4a*T0111+4b*T1111.
```

The nonzero first normal pair `(a,b)` therefore gives exactly
`P1_[a:b]`; every projective direction is realized by a linear arc.

## Two regular direction charts

At `p=0,q=phi=r`, put

```text
u=Bbar+rB,
v=Abar.
```

Use the regular zero-base mode-zero order `(alpha0,beta0)=(u,v)`.  In this
order the first-normal mode-zero covector has values `(b,a)`.

On `a!=0`, write `[a:b]=[1:s]` and take

```text
alpha0'=u-sv,
beta0'=v.
```

On `b!=0`, write `[a:b]=[t:1]` and take

```text
alpha0'=tu-v,
beta0'=u.
```

Both changes have determinant one and make the normal tensor

```text
T1111=4
```

with every other coefficient zero, even after all four affine markings.
On the overlap `s=1/t`, the transition from the second basis to the first is

```text
[[1/t,0],[-1,t]],
```

again of determinant one.  Hence the two charts cover the whole normal
`P1` without a singular basis choice.

## Pair-open classification

Changing a mode basis does not change its local two-plane.  The literal
limiting zero-base plane tuple has pair profile

```text
(3,3,3,3,3,3)       when r^2!=1,
(3,3,2,3,3,3)       when r=+1 or r=-1.
```

Therefore every first-normal direction lies over an all-pair-open limiting
plane when `r^2!=1`, while no direction changes the literal rank-two edge
`03` at `r=+/-1`.

The transverse-arc statement is stronger but distinct.  Over the punctured
arc, every `[a:b]` is all-pair-open for every `r!=0`.  Exact profiles for
representative linear arcs are

```text
[1:0]:            (4,4,3,3,3,3),
[0:1]:            (3,3,4,3,3,3),
[1:s], s!=0:      (4,4,4,3,3,3).
```

These profiles remain valid for `r=+/-1` over the punctured arc.  Thus the
endpoint base plane is a pair-rank boundary, but every normal direction
there is still approached by all-pair-open component points.  The formal
`r=0` limit remains outside the component chart.

## Structural `D01` obstruction

It suffices to work on the `a!=0` direction chart; write its coordinate as
`d=s`.  Let `x0,...,x3` and `x4,...,x7` be the alpha and beta extension
coordinates, and `h0,...,h3` the markings.  Put

```text
S=r*x2-x1,
R=r*x1-x2.
```

For finite homogeneous weight `[lambda:1]`, put `w=lambda-1`; for the
infinity chart `[1:0]`, put `w=1`.  Direct expansion gives

```text
A01=2*w*S,
m1000=h0*A01,
m0001=2*w*(d*R+h3*S).
```

If `A01!=0`, then `w!=0` and the mixed equations first force `h0=0`.  The
coefficient `m1001` then forces `R=0`, so `x2=r*x1`; `m0001` next forces
`h3=0`.  At `r^2=1`, this already gives `S=0`, contradicting `A01!=0`.
Otherwise the two remaining mixed coefficients satisfy the exact reduced
syzygy

```text
B01=h1*m1011+h2*m1101
```

after `h0=h3=0` and `x2=r*x1`.  Their vanishing forces `B01=0`, contradicting
the required nonzero beta diagonal.

On the second direction chart, the endpoint `t=0` has `A01=0` identically
in both weight charts.  Its `t!=0` part is the determinant-one overlap with
the first chart.  Therefore the `A01`-binary orientation is empty on all of

```text
P1_[a:b] x P1_weight
```

for `r!=0`.  This structural argument alone does not exclude the reverse
orientation in which `D23` is binary and `D01` retains only its common beta
diagonal.  That orientation is included explicitly in the complete shared
audit below.

## Bounded elimination audit

Every genuine shared weighted-`H22` point lies in at least one of the four
diagonal opens

```text
(A01,B01,A23),
(A01,B01,B23),
(A23,B23,A01),
(A23,B23,B01).
```

The replay independently eliminates the sixteen systems obtained from

```text
2 normal-direction charts x 2 homogeneous-weight charts
x 4 diagonal opens.
```

In each case it sets all `D01` and `D23` mixed coefficients to zero,
normalizes the first selected diagonal, saturates the other two selected
diagonals, and saturates `r!=0`.  All markings, the normal-direction
coordinate, `r`, and the finite weight coordinate are retained over
characteristic zero.  Every projected ideal is `<1>`.  Thus both shared
orientations, their overlap, both normal endpoints, every finite weight, and
weight infinity are covered.  No finite-field computation or broad search
is used.

## Higher-order boundary

Because the tensor coefficients are exactly linear in the regular generators
`p` and `q-phi`, the tensor-direction statement extends to the first nonzero
normal jet of any arc not contained in `Z0`.  If

```text
m=min(ord_eps(p),ord_eps(q-phi)),
```

then division by `eps^m` gives

```text
4*a_m*T0111+4*b_m*T1111,
```

and hence the same projective direction `[a_m:b_m]`.

The weighted-`H22` conclusion here remains **first-normal only**.  It does
not classify simultaneous valuations of markings, extension coordinates,
and diagonal normalizations in a higher-order or ramified `H22` arc.  Until
a valuative/properness argument closes those possibilities, actual
higher-order `H22` arcs at `Z0` remain **UNKNOWN**.
