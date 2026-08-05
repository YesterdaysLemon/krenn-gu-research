# A twenty-fourth pure `P_4` component from the split-center mixed star

## Status

**Exact characteristic-zero component and reverse-classification theorem.**
In the star cell with relation ranks `(2,1,1)`, suppose the rank-two spoke
synchronizes two disjoint binary center directions and the two rank-one
spokes have mixed orientation: one uses the center kernel and the other uses
the opposite leaf kernel.  Every nonzero all-pair point in this normalized
split-center chart lies on one irreducible five-dimensional component orbit,
component twenty-four.  The complementary branch has a pair image of rank at
most two.

The two sign sheets are exchanged by a source-coordinate transposition.  The
classification includes the complete projective direction of the moving
leaf row.  The generic marked `H31` fibre is subsequently excluded in
[`P5_H31_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
This note does not classify overlapping or singleton center supports, the
remaining inward/equal-endpoint star strata, weighted `H22`, special fibres,
or the global local-to-global step.  Subsequent exact theorems close the
remaining star-`(2,1,1)` orientations and the generic weighted-`H22` fibre;
special/projective fibres remain open.  The Krenn--Gu conjecture remains
**UNRESOLVED**.

## Split-center normal form

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
A=X_0+X_1,   C=X_0-X_1,
B=X_2+X_3,   D=X_2-X_3.                            (1)
```

Take the center and its rank-two synchronizer to be

```text
U_0=<A,B>,             U_1=<A+kD,B+sC>.            (2)
```

This is the general rank-three split-center synchronizer.  Indeed, writing a
general relation as `A*x_1=B*y_1` forces

```text
y_1=wA+tD,             x_1=wB+vC.                  (3)
```

If `w=0`, the pair has the two relations `AC=BD=0` and rank at most two.
On the all-pair locus scale `w=1`, giving (2).

Orient the two rank-one spokes as

```text
A*x_2=0,               B*y_3=0.                    (4)
```

The degree-one annihilator classification gives `x_2=C` and `y_3=D`.
Before the harmless Borel shift of `x_3` by `y_3`, write

```text
y_2=aA+cC+eB+fD,       x_2=C,
y_3=D,                 x_3=gA+hC+jB+nD.            (5)
```

The plane `U_2` is nondegenerate whenever `(a,e,f)` is not all zero, and
`[g:h:j]` is nonzero modulo `D` for `U_3`.  One may set `n=0` after the
coefficient calculation without changing the plane or the marked pure basis.

## Exact purity split

The only potentially nonzero tensor entries are

```text
T_0000=-4(ak+f),
T_0001=-4(ak n-ej+fgk+fn),
T_0101=T_1001=4(aj+eg),
T_1101=4(ag-ch-cjs-ehs),
T_1111=-4(h+js),                                      (6)
```

The harmless Borel coefficient `nD` in `x_3` has been retained to show that
it disappears after `f=-ak`.  Nonzero purity is
therefore exactly

```text
f=-ak,
ej+ak^2 g=0,
aj+eg=0,
ag-ch-cjs-ehs=0,
h+js!=0.                                             (7)
```

Put `Delta=e^2-a^2k^2`.

- If `Delta!=0`, the middle two equations give `j=g=0`.  Then
  `h!=0` and `c=-es`.  Hence `U_3=<C,D>`, while `U_0=<A,B>`; their product
  has dimension at most two.  This branch is in the certified lower-pair
  locus.
- If `Delta=0`, write `e=epsilon ak`, `epsilon=+1` or `-1`.  The case `a=0`
  would make `y_2` proportional to `x_2=C`, so `a!=0`.  Scale `a=1`.
  Equations (7) become

  ```text
  j=-epsilon k g,
  c(h-epsilon ksg)=g-epsilon ksh,
  L=h-epsilon ksg!=0.                               (8)
  ```

Thus the complete nonzero sheet is

```text
U_0=<A,B>,
U_1=<A+kD,B+sC>,
U_2=<A+cC+epsilon kB-kD,C>,
U_3=<D,gA+hC-epsilon kgB>,

c(h-epsilon ksg)=g-epsilon ksh,
h-epsilon ksg!=0.                                  (9)
```

Equation (9) is a graph over `(k,s,[g:h])` on the displayed nonzero open, so
it is irreducible.  It includes `h=0` and hence the full projective moving-
leaf direction; no affine endpoint is omitted.  Swapping `X_2,X_3` sends

```text
(epsilon,k) -> (-epsilon,-k),                       (10)
```

and exchanges the two sign sheets.

On the chart `h=1`, put `tau=g/h` and take `epsilon=1`.  Then

```text
c=(tau-ks)/(1-ks tau),                              (11)
```

and the only nonzero tensor coefficient is

```text
T_1111=4(ks tau-1).                                 (12)
```

Three exterior rank-four minors, using degree-two rows `0123`, are

```text
edge 12: 8k(ks-1)(ks+1),
edge 13: 8s tau(tau+1)(ks-1),
edge 23: 8k(tau-1)(tau+1).                         (13)
```

At `(k,s,tau)=(2,3,2)` they are all nonzero.  The pair profile is

```text
(3,3,3,4,4,4),                                    (14)
```

and the three star relations are

```text
A(B+sC)-B(A+kD)=0,       AC=0,       BD=0,          (15)
```

with coefficient-matrix ranks `(2,1,1)`.

## Smooth component certificate

Use Grassmann pivots `(02),(01),(01),(02)` and restore the diagonal source
torus `diag(q_0,q_1,q_2,1)`.  At `(k,s,tau)=(2,3,2)` the family-coordinate
Jacobian has rank five.  On coordinate rows `(0,3,4,5,12)` and parameter
columns `(k,s,tau,q_0,q_2)`, its determinant is

```text
-1/81.                                             (16)
```

In the universal Segre-incidence chart, use tensor anchor `1000` and target
coordinate `(0,-1,-15/7,0)`.  The fifteen incidence equations have rank
fifteen.  On generic-plane/target columns

```text
g_0,...,g_11,g_14,z_0,z_3
```

their determinant is

```text
-57671680/6561.                                    (17)
```

Thus the pure incidence is smooth of local dimension five, and the
irreducible family supplies every local direction.  Its closure is an
irreducible component.

The generic exceptional graph is a star and its relation-rank word is
`(2,1,1)`.  These invariants leave only component twenty-three among the
first twenty-three component orbits.  There both rank-one spokes use the
center kernel; here one uses the center kernel and one uses a leaf kernel.
The oriented endpoint word relative to the unique rank-two spoke is
intrinsic and symmetry-invariant, so the present component is a new orbit,
component twenty-four.

## Replay

```text
uv run --with sympy python verify_p4_split_center_mixed_star_211_component.py
uv run --with sympy python audit_p4_split_center_mixed_star_211_component.py
```

Both scripts use exact characteristic-zero arithmetic.  The audit rebuilds
the family after an independent source permutation and unequal diagonal
scaling, and checks the projective `h=0` endpoint.  No finite-field result is
used as proof.
