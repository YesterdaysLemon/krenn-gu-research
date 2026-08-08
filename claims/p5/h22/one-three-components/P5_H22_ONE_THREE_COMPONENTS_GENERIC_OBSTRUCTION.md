# Generic weighted `H22` obstruction on the three `1+3` components

## Status

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbits of the three split-cubic pure-compression
components proved in
[`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](../../../../P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md).

For all three components, the weighted `01` diagonal pencil has no
binary `Delta_2` extension.  The third component also has no binary
extension in the weighted `23` pencil.  On the first two components,
the complete generic `23` marking schemes split into two points and
three affine-line closures respectively; one fixed mode-zero minor
excludes every genuine extension from a ternary local map.

Thus the generic weighted `H22` incidence is empty on all three
split-cubic components.

This does **not** close their special parameter/slope divisors or
projective boundaries, the two earlier rank-two components, component
exhaustiveness, all of `H22`, or the global prize problem.

## Shared radical-plane normal form

Let `S,D,G` be the parameters of the `1+3` radical-plane construction
and set

```text
L_1: T=-D+G+S,
L_2: T= D+G-S,
L_3: T=-D-G-S.
```

Use the canonical marked bases constructed in
[`P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h31/one-three/P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md).
Their only nonzero pure coefficients are

```text
L_1: T_1111= 4DG,
L_2: T_1111= 4D(D+G-S),
L_3: T_1111=-4DS.                                  (1)
```

Every marked representative over the same plane tuple is

```text
beta_i(t_i)=beta_i+t_i alpha_i.                    (2)
```

Work over

```text
K=C(S,D,G,r),
```

where `r` is the residual diagonal-source slope.  The two neighboring
source bases are

```text
D_01^r(u)=(r u_0+u_1,u_2,u_3,u_4),
D_23^r(u)=(u_0,u_1,r u_2+u_3,u_4).                 (3)
```

Write the fifth-coordinate extensions as

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3).
```

For either pencil, a genuine binary neighbor requires the fourteen
mixed coefficients to vanish and the two diagonal coefficients
`A(t)z,B(t)z` to be nonzero.

## Exact binary projections

Normalize `A(t)z=1`, invert `B(t)z`, and eliminate `(z,w)`.  For all
three branches the `D_01^r` projected marking ideal is

```text
(1).                                               (4)
```

For `L_3`, the `D_23^r` projection is also `(1)`.  Thus those four
component/pencil incidences are already empty at binary level.

For `L_1`, the exact `D_23^r` marking ideal is

```text
S t_2+G(D-S)t_3+(D-S)(S+G),

(S-D+G)t_1+D(S-D)t_3+(D-S)(S-D+G),

(S+G)t_0+1,

t_3(t_3+1).                                        (5)
```

It consists of two rational points:

```text
L1-A:
t_0=-1/(S+G),
t_1=S-D,
t_2=(S-D)(S+G)/S,
t_3=0;

L1-B:
t_0=-1/(S+G),
t_1=(S-D)(S+G)/(S-D+G),
t_2=S-D,
t_3=-1.                                            (6)
```

For `L_2`, the exact `D_23^r` marking ideal is

```text
(D+G)t_0+1,
t_2 t_3,
t_1(t_3+1),
t_1 t_2.                                           (7)
```

Its point set is the union of three affine-line closures:

```text
L2-A: t_0=-1/(D+G), t_1=0, t_2=0, t_3 free;
L2-B: t_0=-1/(D+G), t_1=0, t_3=0, t_2 free;
L2-C: t_0=-1/(D+G), t_2=0, t_3=-1, t_1 free.       (8)
```

Indeed, if `t_2=0`, the second remaining product in (7) puts the point
on `L2-A` or `L2-C`; if `t_2!=0`, the other products force `L2-B`.

## A uniform one-minor ternary obstruction

For a ternary `H22` lift, the mode-zero one-marked contraction through
the other three binary planes must have rank at most three.  Let
`N_0(z)` be its `8 x 4` coefficient matrix and take the fixed minor

```text
det (N_0)_{0247}.                                   (9)
```

On each of the two sheets in (6) and each of the three closures in
(8), adjoin (9) to the fourteen mixed equations and saturate by
`(A(t)z)(B(t)z)`.  Exact computation over `K` gives the unit ideal in
all five cases:

```text
L1-A: (1),   L1-B: (1),
L2-A: (1),   L2-B: (1),   L2-C: (1).              (10)
```

Therefore the minor (9) is nonzero on every genuine binary extension.
The marked map has rank four and cannot factor through three target
coordinates.  Equations (4)--(10) prove that all three generic
split-cubic component incidences are empty.

This is a function-field elimination and Fitting argument, not a
search through component points.

## Honest frontier

Together with the six-dimensional and mixed-orientation component
theorems, this closes generic weighted `H22` incidence on five of the
seven currently certified pure-`P_4` component orbits.

The remaining generic component targets are the two earlier rank-two
components.  All five newly closed families still have special
parameter/slope divisors and projective boundaries.  The list of seven
pure components is not known to be exhaustive, and the global prize
problem remains unresolved.

## Verification

Run

```text
python \
  claims/p5/h22/one-three-components/verify_p5_h22_one_three_components_generic_obstruction.py

python claims/p5/h22/one-three-components/audit_p5_h22_one_three_components_generic_obstruction.py
```

The primary verifier reconstructs the three canonical bases, proves
all six exact marking projections, checks the decompositions (6) and
(8), and proves the five characteristic-zero saturated unit ideals
(10).

The independent audit imports no primary verifier.  At generic samples
over `F_5` and `F_7`, it exhausts all affine markings for both pencils
on all three branches.  It replays the empty binary incidences, the
two-point and three-line `D_23` patterns, and the nonzero mode-zero
`0247` minor on every genuine survivor.  Those finite-field censuses
are corroboration only; the theorem is the function-field calculation
above.
