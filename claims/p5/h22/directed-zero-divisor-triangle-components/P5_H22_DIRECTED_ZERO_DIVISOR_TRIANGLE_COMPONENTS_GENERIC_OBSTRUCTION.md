# Generic `H22` exclusion for components 16 and 17

## Status

**Exact characteristic-zero generic-fibre theorem.** The complete weighted
`H22` fibre over the generic point of each directed-zero-divisor triangle
component - support-star component sixteen and support-path component
seventeen - is empty.

This is a function-field theorem on a dense open of each component.  It
treats every marked basis, both weighted `2+2` contraction directions, every
slope (including the exceptional slopes where a generic kernel formula
breaks down), and every projective extension direction.  Special parameter
and projective component boundaries, pure-`P_4` component exhaustiveness,
and the global Krenn--Gu conjecture remain open.

## From a graph lift to two Fitting incidences

Use the pure-factor bases `(alpha_i,beta_i)` of
[`P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md`](../../../../P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md),
with the path basis change

```text
alpha_0=row_0+row_1,       beta_0=row_1.
```

Every marked basis of the same four planes is

```text
beta_i(t)=beta_i+t_i alpha_i.                       (1)
```

An `H22` split has two weighted contractions.  In homogeneous slope
coordinates on their dense charts they are

```text
D01^r(x,e)=(r*x0+x1,x2,x3,e),
D23^r(x,e)=(x0,x1,r*x2+x3,e).                       (2)
```

For either direction let `M_D(t,r)z=0` be the fourteen mixed binary
coefficients after adjoining the extension vector `z in K^8`, where
`K=C(u,v)`.  Write `A_D(z),B_D(z)` for the two binary diagonal
coefficients.  A genuine neighbour requires

```text
A_D(z) B_D(z) != 0.                                 (3)
```

Normalizing `A_D=1`, inverting `B_D`, and eliminating `z` gives the open
Fitting projection.  This translates the graph-lift question into the
intersection of two determinantal images.

## The complete binary marking intersection

It is important not to eliminate over `K(r)` and silently lose special
slope fibres.  Instead the verifier eliminates the finite slope `r` itself,
then computes the point `r=infinity` in the other homogeneous chart.

For finite slopes, write `J_D^fin` for the Zariski closure of the projected
genuine-neighbour incidence.  The compact projections needed below are

```text
star:
  J_23^fin = <t1, t3*((u-1)t0+v-1), t2*((u-1)t0+v-1)>;

path:
  J_01^fin = <t2,t1,t3*((u+v)t0+v)>;
  J_23^fin = <t1,t2*t3,t3*((u+v-1)t0+v-1),
                 t0*t2*(C*t0+v(v-1))>,
  C=uv-2u+v^2-v.                                  (4)
```

The star `J_01^fin` basis is longer and carries no conceptual information,
so the verifier constructs it directly from the incidence equations rather
than copying it into the theorem.  Exact ideal reduction gives

```text
star:  J_01^fin + J_23^fin = <1>,
path:  J_01^fin + J_23^fin = <t1,t2,t3>.           (5)
```

The infinity projections are also exact:

| component | direction | projected ideal at infinity |
|---|---|---|
| star | `D01` | `t2, (u-v)t1+(1-u)t3+u-v, u*t0+v, t3(t3+1)` |
| star | `D23` | `t2+(v-1)(t3+1), t1, (u-1)t0+v-1, (t3+1)((v-1)t3+v-2)` |
| path | `D01` | unit ideal |
| path | `D23` | `(u+v)t3+u+v-1, t2,t1,(u+v-1)t0+v-1` |

For the star, each cross-sum of one finite and one infinite projection, and
the sum of both infinite projections, is the unit ideal.  For the path,
`D01` has no genuine neighbour at infinity, and
`J_01^fin+J_23^infinity` is the unit ideal.  Thus every actual pair of
projective-slope incidences is either absent or lies in the line from (5);
no special fibre escapes the calculation.

The star component is therefore excluded already at the binary level.  For
the path component, the intersection of the incidence closures is exactly
the line

```text
t1=t2=t3=0,       t0=h.                             (6)
```

It remains to show that every genuine extension above (6) makes a marked
one-mode map have rank four.

## The path line: generic slopes

For `D01`, away from its exceptional factors, the mixed kernel is generated
by one vector `zeta`, and a mode-one marked minor `Delta_01` satisfies

```text
A=-2*zeta*(r+1)/(r-1),
B= 2*zeta*(h+r),
Delta_01/(A^2 B)=r*(u+v)*(r-1)^2/(r+1)^2.           (7)
```

For `D23`, the analogous identity is

```text
A=-2*zeta*(r-1)*(u+v)/(r+1),
B=-2*zeta*(h*(u+v)+r+v),
Delta_23/(A^2 B)=-(r-1)*(r+u+v)/(r+1).              (8)
```

Whenever the right side is nonzero, (3) makes the displayed minor nonzero.
The one-marked map then has rank four, whereas an `H22` lift would factor it
through a three-dimensional target local space.

## Every exceptional slope

The apparent poles and zeros in (7)--(8) are coordinate degenerations, not
unresolved fibres.

For `D01`:

- at `r=1`, `B` vanishes on the whole mixed kernel;
- at `r=-1`, `A` vanishes on the whole mixed kernel;
- on `h=-r` with `r!=0`, `B` vanishes on the whole mixed kernel;
- at `r=0`, the mixed kernel jumps to dimension two.  In homogeneous kernel
  coordinates `(x,y)`,

```text
A=2(x-y),       B=2(hx-hy-y),
gcd(Delta_1,Delta_2)=2 A B,                         (9)
```

  for mode-one row sets `0237` and `0267`.  Hence no genuine projective
  extension makes both marked minors vanish.

For `D23`:

- at `r=1`, `A` vanishes on the whole mixed kernel;
- at `r=-1`, `B` vanishes on the whole mixed kernel;
- on `h(u+v)+r+v=0` with `r!=0`, `B` vanishes on the whole mixed kernel;
- at its remaining zero-slope intersection
  `r=0, h=-v/(u+v)`, the kernel is two-dimensional and the mode-one row
  sets `0237` and `0247` obey

```text
A=2(u+v)(x-y),       B=-2y,
gcd(Delta_1,Delta_2)=-2 A B;                        (10)
```

- the zero `r=-(u+v)` of the generic minor is closed by a different minor.
  For `h!=0`, mode one and rows `0247` give

```text
Delta/(A^2 B)=-h*(u+v+1)^2/(u+v-1),                (11)
```

  while at `h=0`, mode two and rows `0137` give

```text
Delta/(A^2 B)=-(u+v)*(u+v-1)/(u+v+1).              (12)
```

All parameter factors in (7)--(12) are nonzero elements of the component
function field on the stated generic open.  The list partitions the full
projective slope line, so no slope has been discarded by division.

## Consequence and proof boundary

The star component has no pair of genuine weighted binary neighbours.  On
the path component, every possible common marking lies on (6), and every
genuine extension there has a rank-four marked map.  Therefore

```text
generic H22 fibre(component 16)=empty,
generic H22 fibre(component 17)=empty.              (13)
```

Together with the separate `H31` theorem, both fifth-coordinate partition
types are generically excluded over these two components.  This does not
yet close special parameter/projective boundaries or prove that the
seventeen known pure-`P_4` components exhaust the full pure locus.

## Exact replay

```text
uv run --with sympy python claims/p5/h22/directed-zero-divisor-triangle-components/verify_p5_h22_directed_zero_divisor_triangle_components_generic_obstruction.py
python claims/p5/h22/directed-zero-divisor-triangle-components/audit_p5_h22_directed_zero_divisor_triangle_components_generic_obstruction.py
```

The primary verifier eliminates the finite slopes, checks every finite and
infinite projection intersection, and proves the displayed projection ideals
bidirectionally.  It then checks all kernel, gcd, and exceptional-minor
identities symbolically.  The independent
audit uses a small finite field only as corroboration.  No graph search or
parameter search is used in the characteristic-zero proof.
