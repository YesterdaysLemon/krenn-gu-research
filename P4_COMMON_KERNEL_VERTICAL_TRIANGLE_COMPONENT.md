# A nineteenth component from the common-kernel vertical triangle

## Status

**Exact characteristic-zero component theorem.**  The common-kernel
vertical fibre isolated in equation (15) of
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md)
is a five-dimensional irreducible component of the pure `P_4` compression
locus.  Its generic pair profile is

```text
(4,4,4,3,3,3),
```

and its three exceptional edges form a triangle of coefficient-rank-one
relations with exactly one kernel--kernel edge.  The kernel-endpoint
indegrees are `(2,1,1,0)`.  This distinguishes the component from all
eighteen previously certified component orbits and raises the exact lower
bound to nineteen.

Every nonzero all-pair-open point of the complete projective vertical fibre
belongs to this component closure.  Projective opposite-plane endpoints,
the divisor on which an exterior pair rank drops from four to three, and the
lower-pair boundary are included honestly as closure strata; no claim about
their marked `P_5` fibres or the global Krenn--Gu conjecture is made.

## Normal form for the whole vertical fibre

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
A=X_0+X_1,       A_bar=X_0-X_1,
B=X_2+X_3,       B_bar=X_2-X_3.                    (1)
```

The vertical reduction has

```text
U_1=span(B,A),
U_2=span(B_bar,A),
U_3=span(A_bar,rB+sB_bar),       rs!=0,            (2)
```

and the opposite plane is an arbitrary two-plane in

```text
K=span(A_bar,B,B_bar)=Ann_R1(A^2(rB+sB_bar))       (3)
```

which detects the displayed active cubic.  Scale the last active row by
`r^(-1)` and put `phi=s/r`.  Thus `phi!=0`.  A dense affine chart of
`Gr(2,K)=P^2` is

```text
U_0=span(A_bar+pB, B_bar+qB).                      (4)
```

Use the displayed row order.  Direct squarefree multiplication gives only

```text
T_0111=4p,       T_1111=4(q-phi),                 (5)
```

so the restriction is pure and is nonzero precisely when

```text
(p,q-phi)!=(0,0).                                  (6)
```

The selected triangle relations are

```text
y_1y_2=0,       x_1y_3=0,       x_2y_3=0.         (7)
```

Their support multiset is `{23,01,01}`: one genuine binary exact pair and
one disjoint exact pair repeated twice.  All three relation matrices have
rank one.  The first relation points to both kernel endpoints, while each
of the other two points to the common kernel at mode three.  Hence the
sorted kernel-endpoint indegrees are

```text
(2,1,1,0).                                         (8)
```

## Pair-rank geometry and the honest open set

In edge order `01,02,03,12,13,23`, fixed exterior maximal minors are

```text
-8pq,       8p,       -8(q-phi)(phi*q-1),          (9)
```

and the three triangle pair ranks are identically three for `phi!=0`.
Consequently the dense profile is

```text
(4,4,4,3,3,3)                                      (10)
```

on, for example,

```text
p*q*(q-phi)*(phi*q-1)!=0.                          (11)
```

The all-pair-open family is larger than (11).  Exact `3 x 3` minors show
that `U_0U_1` has rank at most two exactly when `p=q=0`, while `U_0U_2`
always has rank at least three on this chart.  The only rank-at-most-two
case for `U_0U_3` has `p=0`, `q=phi`, and `phi^2=1`, which is already a zero
restriction by (5).  Thus the nonzero all-pair-open chart is exactly

```text
phi!=0,
(p,q)!=(0,0),
(p,q-phi)!=(0,0).                                  (12)
```

Divisors omitted from (11) but retained in (12) merely add rank-three
exterior edges.  The point `p=q=0` is a lower-pair boundary, and
`p=0,q=phi` is the zero-tensor boundary.

## Five actual family directions

Restore the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1).                               (13)
```

The written parameter space `(p,q,phi,t_0,t_1,t_2)` has one stabilizer
direction.  Reduce all four planes in the Grassmann charts with pivots
`(02)`.  At

```text
(p,q,phi,t_0,t_1,t_2)=(2,3,2,1,1,1),              (14)
```

the family Jacobian has rank five.  Its rows

```text
(g_0,g_1,g_3,g_7,g_15)
```

and parameter columns `(p,q,phi,t_0,t_2)` have determinant

```text
1/72.                                               (15)
```

The image closure is therefore an irreducible fivefold.

## The excess tangent is quadratically obstructed

It remains to exclude a containing sixfold.  Use sixteen `(02)` Grassmann
chart coordinates `g_0,...,g_15`.  At (14), the normalized tensor has

```text
T_0001=2,       T_1001=1/3.                        (16)
```

Take `alpha=0001`, introduce Segre ratios `z_0,...,z_3`, and impose the
fifteen universal incidence equations

```text
F_beta=T_beta-T_alpha product_(i: beta_i!=alpha_i) z_i=0,
beta!=alpha.                                       (17)
```

The target point is

```text
(z_0,z_1,z_2,z_3)=(1/6,0,0,0).                    (18)
```

The first fourteen rows of (17), against columns

```text
g_0,g_1,g_2,g_4,g_5,g_6,g_7,g_8,g_9,g_10,
g_13,g_14,z_1,z_3,                                 (19)
```

have determinant

```text
1280/27.                                            (20)
```

Thus these fourteen equations cut out a regular six-dimensional local
scheme.  Their complementary local coordinates are

```text
g_3,g_11,g_12,g_15,z_0,z_2.                        (21)
```

The first five coordinates in (21) carry the five actual family
directions.  Fix them at (14),(18), set `z_2=h`, and solve the fourteen
regular equations through order two.  The omitted `beta=1111` equation is

```text
(1/6)h^2+O(h^3).                                   (22)
```

It is therefore a nonzero element of the regular six-dimensional local
ring cut out by the selected equations.  Adding it lowers local dimension
to at most five.  The family directions in (15) give the reverse inequality,
so the full incidence has local dimension exactly five at the sample.  The
irreducible family closure is consequently an irreducible component.  A
nonzero pure tensor has a unique projective Segre point, so projection to
the four-plane locus preserves the component statement.

## Why this is a new component orbit

Dimension separates the family from every old six-dimensional component.
Among old fivefolds, a different generic pair-rank multiset or a star rather
than a triangle separates all but the previously known triangle families.
The old triangle components with profile (10) split as follows:

- components one and thirteen have relation-rank word `(2,1,1)`;
- components sixteen and seventeen have three rank-one tournament
  relations, so each relation has only one kernel endpoint and the total
  kernel indegree is three;
- the present component has relation-rank word `(1,1,1)` but (7) has one
  kernel--kernel edge, giving total kernel indegree four and signature (8).

Pair-image ranks, relation-matrix ranks, the exceptional mode graph, and the
intrinsic pure-kernel endpoint signature are invariant under source
coordinate permutations, diagonal source scaling, mode permutations, and
row-basis changes.  Hence this fivefold is inequivalent to all eighteen old
orbits.

## Why the complete projective fibre is included

The chart (4) is dense in the irreducible projective plane `Gr(2,K)`.  The
parameter `phi` ranges over the irreducible torus `G_m`, and the source torus
is irreducible.  Therefore the closure of the chart used above contains
every projective opposite-plane direction in (3), including every point of
the nonzero all-pair-open vertical family.  The component certificate does
not silently discard the fibre directions on the other two Grassmann
charts.

## Exact replay

```text
uv run --with sympy python verify_p4_common_kernel_vertical_triangle_component.py
python audit_p4_common_kernel_vertical_triangle_component.py
```

The primary verifier checks (5)--(22) over `Q`, including the family and
incidence minors and the exact quadratic obstruction.  The independent
audit rebuilds squarefree permanents, pair ranks, first derivatives, and the
second-order implicit calculation modulo two unrelated primes.  Both are
fixed-size exact certificates; neither searches a parameter grid or runs an
elimination.
