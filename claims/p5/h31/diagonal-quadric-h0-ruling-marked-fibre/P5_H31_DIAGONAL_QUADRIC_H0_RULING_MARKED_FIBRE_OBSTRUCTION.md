# A closed interior ruling and the complete `H=0` slice

## Status

This is an exact characteristic-zero marked-fibre theorem on an
interior rational ruling of the diagonal-quadric component.

For every `e in C^*`, every marking of the four planes below, every
distinguished common source coordinate, and every genuine binary
`Delta_2` extension direction is excluded from an `H31` lift.  Exact
relative projection keeps `e` as a geometric variable and saturates
only by `e`.

The opposite ruling is a source-coordinate image of this one.  Hence
the theorem closes the complete nonzero slice

```text
A=B=F=1, H=0.
```

It remains a lower-dimensional result, not a generic theorem for the
second component, a boundary compactification, a classification of
further components, an `H22` result, or a solution of the prize
problem.

## A polynomial marking of `CE=1`

Set

```text
A=B=F=1, H=0, E=e, C=1/e,   e!=0.                  (1)
```

To avoid denominators in the plane rows, multiply `x_1` by `e`.  Use

```text
U_0=span((2e,-e-1,e-1,0),(1,-1,1,1)),
U_1=span((1,0,0,-1),(e,e+1,1-e,e)),
U_2=span((0,1,-1,0),(e,1,1,-e)),
U_3=span((e,-1,-1,e),(0,1,1,0)).                  (2)
```

The first row in each plane is the kernel row `alpha_i`; the second is
the pure-colour row `beta_i`.  All four planes have rank two for every
`e!=0`.  The only nonzero restricted coefficient is

```text
Perm(beta_0,beta_1,beta_2,beta_3)=4e.              (3)
```

Every marking is `beta_i(t)=beta_i+t_i alpha_i`.

## Global relative projection

Normalize one binary diagonal, invert the other, and saturate by `e`.
Exact elimination over `Q`, retaining `e,t_0,...,t_3`, gives

| `q` | relative survivor marking ideal |
| ---: | --- |
| `0` | `(1)` |
| `1` | `(t_3,t_2-1,t_1-e,e t_0+1)` |
| `2` | `(t_3,t_2+1,t_1-e,e t_0+1)` |
| `3` | `(t_3-1,t_2-e,t_1-e,2t_0+e,e^2-1)` |

Thus the complete survivor list is

```text
all e!=0, q=1: t=(-1/e,e, 1,0);
all e!=0, q=2: t=(-1/e,e,-1,0);
e= 1, q=3:     t=(-1/2, 1, 1,1);
e=-1, q=3:     t=( 1/2,-1,-1,1).                  (4)
```

There are no hidden exceptional complex fibres.

## The two uniform kernels

At `q=1`, take

```text
k_0=(0,-1/e,0,0,0,0,1,0),
k_1=(-e-1,2/e,1,-1,1/e,e+1,0,1).                 (5)
```

At `q=2`, replace the second vector by

```text
k_1=(e-1,2/e,-1,-1,1/e,1-e,0,1).                 (6)
```

Both mixed matrices have rank six.  For `z=u k_0+v k_1`, the
diagonals are

```text
q=1:  2e(u-2v),2eu;
q=2: -2e(u-2v),2eu.                                (7)
```

In both cases the mode-two marked minor on rows `000,100,101,111` is

```text
-8u(u-2v)^2.                                       (8)
```

It is nonzero whenever both binary diagonals are nonzero.

## The `e=+/-1` jumps

At `e=1,q=3`, use

```text
k_0=(0,0,1,1,1,0,0,0),
k_1=(0,-1,-1,0,0,0,-1,1).                         (9)
```

The diagonals are `4(u-v),4v`.  At `e=-1,q=3`, use

```text
k_0=(0,0,1,-1,1,0,0,0),
k_1=(0,1,1,0,0,0,-1,1),                           (10)
```

with diagonals `4(u+v),4v`.  The mode-zero marked minor on rows
`000,100,101,111` is respectively

```text
-64v(u-v)^2,  -64v(u+v)^2.                         (11)
```

Every genuine jump extension is therefore excluded.

The selected pure-hyperplane column is nonzero in all four kernel
types.  Injectivity on the neighbouring hyperplane and transversality
to the pure hyperplane force the third target row to vanish globally,
contradicting rank three.

## The complete `H=0` slice

On `A=B=F=1,H=0`, the component equation becomes

```text
1-C^2 E^2=-(CE-1)(CE+1).                           (12)
```

The source swap `X_0<->X_3` sends `E` to `-E` while preserving `C` and
the plane tuple up to row bases.  It exchanges `CE=1` and `CE=-1`.
Therefore the theorem closes every marked fibre on the complete
nonzero slice (12), and every source/mode symmetry translate of that
slice.

## Verification

Run:

```text
python claims/p5/h31/diagonal-quadric-h0-ruling-marked-fibre/verify_p5_h31_diagonal_quadric_h0_ruling.py
python claims/p5/h31/diagonal-quadric-h0-ruling-marked-fibre/audit_p5_h31_diagonal_quadric_h0_ruling.py
```

The primary verifier recomputes all four saturated relative
projections, the four survivor kernel types, their diagonals and
selected all-extension minors, the factorization (12), and the
source-coordinate symmetry.  The independent audit enumerates every
parameter and marking over `F_5,F_7`, then checks every projective
kernel direction with a separate dynamic-programming permanent.  The
finite-field calculation is QA; the relative elimination and exact
identities prove the result over `C`.

Both checks pass.  The independent census covers `67,624` marking
fibres.  It finds exactly `24` binary-survivor markings and checks all
`172` projective kernel directions; `124` have both binary diagonals
nonzero, and every one has the predicted full-rank marked map.
