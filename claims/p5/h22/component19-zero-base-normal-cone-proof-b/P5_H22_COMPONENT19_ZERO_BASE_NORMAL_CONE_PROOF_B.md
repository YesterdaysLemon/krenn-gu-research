# Component 19 zero-base normal cone: proof B

```yaml
role: proof_b
date_utc: 2026-08-01T17:35:31Z
git_commit: ac0853455c978628c6f685e826f78275591d639a
claim_label: DERIVED
scope: component-19 zero base p=0,q=phi; first normal directions and exact linear DVR arcs inside the displayed component chart
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md: 43e714b95f8a092bee9bf3b9259916a66bf7e8ae5984b63bf259d7e41aa4f440
  P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md: 77bad167798b52ca6d623ded47d346255023a13f4122f672ffc485dff9c70f50
  P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md: 40a1932b552411e64ec5a44a488ea99d0d4ac985126dddff2ff177fd1b941708
  P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md: 128da2990f6800146375d78916279d0127eff372e3eab412d9d0f020bd6612b3
method: exact normal expansion, pair-minor reconstruction, verified open-stratum routing, and fresh phi=+/-1 finite/infinity endpoint algebra
command: uv run --with sympy python derive_p5_h22_component19_zero_base_normal_cone_proof_b.py
outputs: replay stdout gives final path and sha256 pairs
limitations: exact linear one-parameter arcs in the displayed component chart; no claim that the P1 leading tensor alone determines arbitrary higher-order, ramified, multi-parameter, or ambient-component valuative incidence
```

## Result and boundary

For every normal direction `[a:b] in P1`, the first nonzero restriction is

```text
4*(a*e_0111+b*e_1111).                            (1)
```

Every exact linear punctured arc

```text
p=a*tau,       q=phi+b*tau,       [a:b]!=[0:0]    (2)
```

is nonzero and all-pair-open over `K((tau))`.  Combining the exact verified
open-stratum theorems with the fresh endpoint calculation below shows that no
arc (2) has a weighted-`H22` lift, at finite or infinite weight.

This is a `DERIVED` exact-linear normal theorem.  It is not promoted to a
theorem about all higher-order or valuative arcs merely from the projective
direction `[a:b]`.

No new normal-cone or zero-base construction artifact was read or imported.

## Exact normal tensor

Write `r=q-phi`.  In the component source basis, squarefree multiplication is
exactly

```text
T_0111=4p,       T_1111=4r,
T_w=0 otherwise.                                  (3)
```

Substitution of (2) and division by `tau` gives (1) with no remainder.  More
generally, if a formal arc has minimal order `m` in the pair `(p,r)`, then
its first nonzero coefficient tensor is still (1), where `a,b` are the two
order-`m` leading coefficients.  This statement uses only the exact
linearity of (3).

The tensor in (1) is a nonzero pure local-source tensor for every point of
`P1`.  It must not be confused with the permanent of the frozen target-plane
rows: all restriction coefficients of those rows vanish at the zero base.
The normal object also retains plane-tangent information.

## Pair geometry

The complete component criterion says a nonzero point is all-pair-open iff

```text
phi!=0,       (p,q)!=(0,0),       (p,r)!=(0,0).
```

On the punctured generic point of (2), `q=phi+b*tau` is nonzero and
`(p,r)=tau*(a,b)` is nonzero.  Hence every `[a:b]` is a punctured
all-pair-open direction.

The frozen base planes tell a different story.  Five pair maps retain fixed
rank-three witnesses `4phi,4phi,-4,4phi,4phi`; the `03` pair has witness

```text
-4*(phi^2-1).
```

Thus the frozen base planes are all-pair-open when `phi^2!=1` and have a
rank-at-most-two `03` pair when `phi^2=1`.  This does not contradict punctured
openness: the missing rank is restored at positive `tau`-order.

## Routing all exact linear directions

The weighted analysis of (2) separates into four exact strata.

1. `a=0`, `b!=0`: this is the ordinary `p=0` chart with `q-phi!=0`.
   If `phi^2!=1`, its Laurent-field generic point lies on the verified
   obstruction open.  If `phi=+/-1`, the no-import endpoint theorem applies.

2. `b=0`, `a!=0`: this is the verified divisor `q=phi`, `p*phi!=0`, whose
   complete finite and infinity shared incidences are empty.

3. `a*b!=0`, `phi^2!=1`: the verified generic component calculation applies.
   Its complete finite branch has a fixed rank-four one-marked obstruction,
   and its weight-at-infinity incidence is empty.

4. `a*b!=0`, `phi=e=+/-1`: the generic rank witness loses `phi^2-1`, so this
   stratum is rebuilt directly below.

All nonzero `[a:b]` occur in exactly one of these cases.

## Fresh `phi=+/-1`, `a*b!=0` calculation

Put `r=q-e`; on (2), both `p` and `r` are nonzero Laurent elements.  A regular
intrinsic pure basis is

```text
alpha0=r*Abar-p*(Bbar+e*B),       beta0=Abar+p*B,
```

with the three unchanged component planes.  It has only `T_1111=4p`.

### `D23`-binary finite branch

Direct mixed equations force

```text
lambda=1,       h=(-1/r,0,t,0).
```

The combined unwanted-coefficient matrix has rank five; a fixed five-minor
is `-1024*e*p^3*r`.  Its complete kernel is generated by

```text
vX=(0,-1/p,e/p,0; 1,0,0,0),
vY=(0,0,0,0;      0,1,0,0),
vZ=(e*p,-(r+e)/r,1/r,0; 0,0,0,1).
```

For `X*vX+Y*vY+Z*vZ`, put

```text
F=e*X*r+Z*p,
G=p*r*Y-t*F,
H=X*r+Z*p*r+e*Z*p.
```

The required diagonals are nonzero exactly on `F*G*H!=0`, up to the standing
units.  Rows `(0,2,3,7)`, columns `(0,1,2,4)` of the `D23`, mode-three
one-marked map have determinant

```text
64*F^2*H/r^2.                                     (4)
```

It is nonzero throughout the genuine branch, so every point is obstructed.

### Reverse finite orientation

Normalize its `D01` all-alpha diagonal.  The complete mixed equations have a
single branch.  For `e=1`, `lambda=r/(r+2)`; for `e=-1`,
`lambda=(r-2)/r`.  Uniformly,

```text
h=(-1/r,0,0,e*r/p),
C=(-e*p*(r+2e)/r,(r+e)/r,1/r,0),
D=(2e*p*(r+e)/r^2,0,0,-(r+2e)/r).
```

Its `D01` all-beta diagonal is identically zero.  It is therefore a complete
mixed solution but not a genuine binary neighbour.

### Weight infinity

If `D23` is binary, `D01` purity and one further mixed equation force its
required all-alpha diagonal to zero.  In the reverse orientation, `e=-1`
contradicts the normalized `D01` diagonal immediately; for `e=1`, the
remaining equation is a nonzero multiple of `r+2`, a unit on the normal arc.
Thus the infinity incidence is empty.

This closes the last exact-linear direction stratum.

## What extends to higher order, and what does not

Equation (3) extends verbatim: every nonconstant one-parameter formal arc has
a minimal-order normal pair and therefore a first tensor direction `[a:b]`.
The punctured all-pair-open argument also extends whenever the arc remains in
this component chart and is not identically on the zero base.

The weighted-`H22` conclusion is different.  Its equations use the full
target-plane rows, markings, extension coordinates, and projective weights.
Those variables may carry poles or higher-order cancellations.  The leading
coefficient tensor (1) does not remember this data.  The present replay checks
exact linear arcs and exact algebraic strata, but it does not construct the
Rees incidence or prove flat/proper specialization for arbitrary formal
arcs.  Therefore:

- first-tensor and punctured pair-openness statements extend to minimal-order
  formal arcs;
- weighted-`H22` emptiness is proved here only for exact linear arcs (2);
- arbitrary higher-order, ramified, multi-parameter, non-diagonal-source, or
  ambient-component valuative lifts remain `UNKNOWN` in this report.
