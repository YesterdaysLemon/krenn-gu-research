# No `H31` lift at a rational point of the second `P_4` component

## Status

This is an exact characteristic-zero obstruction at one all-rank-two
point of the diagonal-quadric component proved in
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](../../../p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md).

For this plane tuple, every marking of the pure tensor, every choice of
the distinguished common source coordinate, and every binary
`Delta_2` extension direction is excluded from a ternary `H31` lift.
This is the first marked-fibre result on the second component.

The theorem is deliberately pointwise.  It does **not** exclude a
dense open subset, the complete second component, its boundary, any
further component, `H22`, or the global prize problem.

The later theorem
[`P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](../diagonal-quadric-e-curve-marked-fibre/P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md)
subsumes this point as `e=2`.  This file remains the smaller,
independently checked seed calculation.

## The rational plane tuple and its pure marking

Use source coordinates `0,1,2,3` and the planes

```text
U_0=span((2,-1,-1,-2),(1,-1, 1, 1)),
U_1=span((1, 0, 0,-1),(1, 1,-1, 1)),
U_2=span((3, 1, 1,-1),(0, 1,-1, 0)),
U_3=span((1, 0, 0, 1),(0, 1, 1, 0)).                (1)
```

They are the parameter point

```text
(A,B,C,E,F,H)=(1,1,0,2,1,1)
```

of the second component.  Mark the kernel rows by

```text
alpha_0=(3,-2, 0,-1),
alpha_1=(1, 0, 0,-1),
alpha_2=(0, 1,-1, 0),
alpha_3=(1,-1,-1, 1),                               (2)
```

and choose complementary pure-colour rows

```text
beta_0=(1,-1, 1, 1),
beta_1=(1, 1,-1, 1),
beta_2=(3, 1, 1,-1),
beta_3=(0, 1, 1, 0).                                (3)
```

Direct expansion gives

```text
Perm(beta_0,beta_1,beta_2,beta_3)=4,
```

and all fifteen coefficients containing at least one `alpha` row
vanish.  Thus the restricted tensor is the nonzero pure tensor
`4 BBBB`.

Every marking over these four planes is uniquely

```text
beta_i(t)=beta_i+t_i alpha_i,   t=(t_0,t_1,t_2,t_3). (4)
```

## Exact binary projection

For a distinguished common source coordinate `q`, delete `q`, append
the fifth source coordinate, and write its eight entries as

```text
e=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3).                (5)
```

The fourteen mixed `Delta_2` coefficients are linear in `e`.  Saturate
by both diagonal coefficients, equivalently normalize the first to one
and invert the second.  Exact characteristic-zero elimination of (5)
gives the following complete projection to marking space:

| distinguished `q` | binary-survivor marking ideal |
| ---: | --- |
| `0` | `(t_0,t_1-1,t_2-1,t_3-1)` |
| `1` | `(1)` |
| `2` | `(1)` |
| `3` | `(t_0,t_1+1,t_2-1,t_3-1)` |

Consequently `q=1,2` admit no genuine binary extension in any marking.
For `q=0,3`, there is exactly one survivor marking.

## The two survivor kernels

At `q=0`, put `t=(0,1,1,1)`.  The mixed matrix has rank six and kernel
basis

```text
k_0=(0,0,-1,0, 0,1,0,0),
k_1=(3,1, 2,1, 1,0,3,1).                            (6)
```

For

```text
e=u k_0+v k_1,
```

the two diagonal coefficients are

```text
d_0=2(u-2v),   d_1=2u.                              (7)
```

At `q=3`, put `t=(0,-1,1,1)`.  The kernel basis is

```text
k_0=(0,0,-1,0, 0,1,0,0),
k_1=(-1,-1,2,1, 1,0,-1,1),                          (8)
```

and

```text
d_0=-2(u-2v),  d_1=2u.                              (9)
```

Thus a genuine binary `Delta_2` extension in either survivor has

```text
u(u-2v) != 0.                                       (10)
```

## Uniform ternary obstruction

At mode one, form the one-third-row map on the neighbouring
hyperplane.  In both survivor cases, its rows indexed by

```text
000,001,101,111
```

have determinant

```text
-8 u (u-2v)^2.                                      (11)
```

It is nonzero for every binary extension by (10).  Hence the third
target row at mode one vanishes on the neighbouring hyperplane and is
supported only on the distinguished coordinate `q`.

On the pure hyperplane, the mode-one one-marked map has a nonzero entry
`2` in column `q`, for both `q=0` and `q=3`.  The third row must
therefore vanish on its remaining coordinate as well.  It is globally
zero, contradicting rank three of the full local map.

This excludes every binary extension over the two survivor markings
and completes the pointwise `H31` obstruction.

## Scope consequence

The second component is genuine, so closing the first component cannot
settle `H31`.  The calculation above shows that the familiar
transverse-kernel mechanism remains effective on the new geometry, but
only at the exact point (1).  The next task is a relative version over
the irreducible `(3,3)` parameter hypersurface, followed by its
projective boundary.

## Verification

Run:

```text
python claims/p5/h31/diagonal-quadric-component-point/verify_p5_h31_diagonal_quadric_component_point.py
python claims/p5/h31/diagonal-quadric-component-point/audit_p5_h31_diagonal_quadric_component_point.py
```

The primary verifier recomputes the four exact elimination ideals with
Singular, derives both mixed kernels, and proves the all-extension
minor (11).  The independent audit enumerates only the four-dimensional
marking fibre over `F_5,F_7`, reconstructs the exact survivor markings,
and checks every surviving projective extension direction with a
separate dynamic-programming permanent.  The finite-field enumeration
audits this fixed fibre; the displayed elimination and identities are
the characteristic-zero proof.
