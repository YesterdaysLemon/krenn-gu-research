# No `H31` lift from the nonzero chart boundary of the known component

## Status

This is an exact characteristic-zero obstruction.

The chart closure theorem
[`P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md`](../../../p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md)
finds one nonzero all-rank-two boundary divisor inside the preferred
Grassmann chart of the known component.  For the displayed marked row
normal form, no point of that divisor, in any of its four
distinguished-source orientations, can lift to an `H31`
pure/`Delta_2` pencil with rank-three ternary local maps.

Together with
[`P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md`](../rank-two-component-orbit/P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md),
this excludes the canonical marked sections over the component chart
and its displayed internal divisor.  It does not exclude every marked
basis over those planes: kernel-row shifts are additional `H31` data,
as shown by
[`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](../marked-basis-open-branch/P5_H31_MARKED_BASIS_OPEN_BRANCH.md).
The full marked-basis fibre, the Schubert boundary, and additional
components were not classified by this canonical-section theorem.  The
complete marked fibre over this divisor has since been excluded in
[`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](../component-chart-boundary-marked-fibre/P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md).
The Schubert boundary has since been closed separately.  Additional
components remain outside its scope.

## Boundary normal form

Use parameters

```text
A H N !=0,   R arbitrary.
```

After a binary target-basis change, the four pairs of source rows are

```text
alpha_0=(1,0,A,H(A-N)),
 beta_0=(0,1,0,-HNR),

alpha_1=(0,0,1,H),
 beta_1=(R,1,-RN,-RHN),

alpha_2=(0,1,0,HNR),
 beta_2=(-1/N,0,1,0),

alpha_3=(1,0,N,0),
 beta_3=(0,0,-1/H,1).                               (1)
```

Their `P_4` restriction has the single nonzero binary coefficient

```text
AAAA=2AH.                                            (2)
```

For a distinguished source coordinate `q`, delete column `q`, append
the neighbouring fifth-coordinate entries

```text
(x_0,...,x_3;y_0,...,y_3),
```

and let `N_q` be the `14 x 8` mixed-coefficient matrix.  As before, a
binary `Delta_2` extension is a kernel vector on which both diagonal
coefficient functionals are nonzero.

## The stratum `R!=0`, `A!=N`

The ranks of `(N_0,N_1,N_2,N_3)` are

```text
(7,7,6,6).                                           (3)
```

For `q=0,1`, the unique kernel directions have diagonal pairs

```text
q=0: (-2AHN,0),
q=1: ( 2AH, 0),                                      (4)
```

so neither can give `Delta_2`.

For `q=2`, a kernel basis has diagonal pairs

```text
(2HN,2R),   (-2H^2(A-N),2HR).
```

Writing the extension as `(t,u)`, put

```text
F=N t-H(A-N)u,   G=t+H u.                            (5)
```

The diagonals are nonzero exactly when `F G!=0`.  The mode-two
one-marked map on the neighbouring hyperplane has determinant

```text
8 H N R G F^2,                                      (6)
```

and is therefore injective.

For `q=3`, a kernel basis has diagonal pairs

```text
(0,2/(HN)),   (2AH,2R).
```

The `Delta_2` conditions are

```text
u!=0,   K=t+HNR u!=0.                                (7)
```

A mode-two marked determinant is

```text
8 A u^2 K.                                           (8)
```

Thus this map is injective as well.

## The collision `R!=0`, `A=N`

Here `N_0,N_1` both have rank six.  Their extra kernel directions make
binary `Delta_2` extensions possible, but also expose immediate marked
determinants.

For `q=0`, the diagonal conditions force `t u!=0`, and a mode-zero
marked determinant is

```text
8 H^2 N^3 R^2 t u^2.                                (9)
```

For `q=1`, the conditions force

```text
u!=0,   t+HNRu!=0,
```

and a mode-zero marked determinant is

```text
-8 H^2 N R^3 u^2(t+HNRu).                           (10)
```

The formulas (6) and (8) continue to handle `q=2,3`.

## The divisor `R=0`

For `A!=N`, the ranks are

```text
(6,2,5,6);
```

at `A=N` the first two become `(5,1)`.  In both cases the `q=1`
beta-diagonal functional vanishes on the entire kernel, so `q=1`
cannot produce `Delta_2`.

For the other orientations, retain only the kernel coordinates that
affect a diagonal.  Their `Delta_2` conditions and mode-two marked
determinants are:

```text
q=0: t u!=0,
     det=8 A H N^3 t^2 u;

q=2: t!=0, F=N u-H(A-N)v!=0,
     det=8 H t^2 F;

q=3: t u!=0,
     det=8 A t u^2.                                  (11)
```

Any additional kernel direction on the collision `A=N` is killed by
both diagonals and does not change this conclusion.

## Ternary contradiction

In every binary survivor above, the displayed marked determinant makes
the relevant one-third-row map on the neighbouring hyperplane
injective.  Hence the third target row at that mode is supported only
on the distinguished pure coordinate `q`.

The corresponding one-marked map on the pure hyperplane does not kill
that coordinate:

- for (6), (8), and (11), use mode two;
- for (9) and (10), use mode zero.

In each case one displayed coordinate entry is a nonzero monomial in
`A,H,N,R`.  The third row must therefore vanish globally, contradicting
rank three of the full local map.  This proves the theorem.

## Verification

Run:

```text
python claims/p5/h31/component-chart-boundary/verify_p5_h31_component_chart_boundary.py
python claims/p5/h31/component-chart-boundary/audit_p5_h31_component_chart_boundary.py
```

The primary verifier reconstructs all four mixed matrices, their
kernel strata, diagonal functionals, rank minors, and marked
determinants symbolically.  The independent audit checks every boundary
parameter tuple over `F_5` and `F_7` and every projective mixed-kernel
extension with two nonzero diagonals, using a separate
dynamic-programming permanent and modular row reduction.  No ambient
local maps or Grassmannians are enumerated.
