# A closed marked curve on the second pure-compression component

## Status

This is an exact characteristic-zero marked-fibre theorem on a
one-parameter curve of the second pure rank-two `P_4` component.

For every `c in C` with `c!=-1`, every marking of the four planes
below, every distinguished common source coordinate, and every binary
`Delta_2` extension direction is excluded from an `H31` lift.  The
proof uses one function-field projection over `Q(c)` and exact
specializations at `c=0,1`; it is not an enumeration of ambient maps.

This is stronger than a point obstruction but weaker than a generic
theorem for the full five-dimensional component.  It does not close
the complement of this curve, the component boundary, any further
component, `H22`, or the prize problem.

## A rational curve in the `(3,3)` component

In the normal form of
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md),
set

```text
A=B=E=F=H=1,   C=c.                                 (1)
```

The component equation `Psi=0` holds identically.  Use planes

```text
U_0=span((1,-1,-1,-1),(1,-1, 1, 1)),
U_1=span((1, 0, 0,-1),(1,c+1,c-1,1)),
U_2=span((2, 1, 1, 0),(0,1,-1,0)),
U_3=span((1, 0, 0, 1),(0,1, 1,0)).                 (2)
```

All four planes have rank two for every `c`.  Mark kernel rows

```text
alpha_0=(1,-1, 0, 0),
alpha_1=(1, 0, 0,-1),
alpha_2=(0, 1,-1, 0),
alpha_3=(1,-1,-1, 1),                               (3)
```

and pure-colour rows

```text
beta_0=(1,-1, 1, 1),
beta_1=(1,c+1,c-1,1),
beta_2=(2, 1, 1, 0),
beta_3=(0, 1, 1, 0).                                (4)
```

The only nonzero restricted coefficient is

```text
Perm(beta_0,beta_1,beta_2,beta_3)=4(c+1).           (5)
```

Thus `c=-1` is the zero-tensor point and is outside the nonzero pure
locus.  Every marking for `c!=-1` is

```text
beta_i(t)=beta_i+t_i alpha_i.                        (6)
```

## A symmetry-orbit deformation

The curve theorem also closes a second displayed parameter line without
another elimination.  Swap source coordinates by

```text
(X_0,X_1,X_2,X_3) -> (X_1,X_0,X_3,X_2)
```

and then swap modes `1,2`.  This sends (2), with `c=h`, to the normal
form

```text
A=B=C=E=F=1, H=h.
```

The moving plane `U_1` becomes the moving plane `U_2`; `U_0,U_3`
are preserved and the fixed `U_2` becomes the fixed `U_1`.  The sole
pure coefficient is `4(h+1)`.  Since source-coordinate and mode
permutations preserve the complete marked `H31` lifting problem, every
point of this `H=h!=-1` curve and every point in the full discrete
source/mode symmetry orbit of (2) are excluded as well.

## Generic binary projection

There is no appeal to generic specialization.  First retain `c` as an
ordinary elimination variable, normalize one binary diagonal, invert
the other, and explicitly saturate by `c+1`.  Exact elimination over
`Q` gives the global nonzero-pure marking ideals:

| distinguished `q` | relative marking ideal in `Q[c,t]` |
| ---: | --- |
| `0` | `(t_3-1,t_2-1,t_1-1,(c-1)t_0+2c)` |
| `1` | `(1)` |
| `2` | `(t_3,t_2-1,t_1-1,t_0+1)` |
| `3` | `(t_3-1,t_2-1,t_1-2c+1,t_0+c,c^2-c)` |

This calculation proves that there are no hidden complex exceptional
fibres.  The `q=3` ideal records precisely the jumps at `c=0,1`.

For readable kernel formulas, now pass to `Q(c)`, so
`c(c-1)(c+1)` is invertible.  The same elimination specializes to:

| distinguished `q` | generic survivor marking ideal |
| ---: | --- |
| `0` | `(t_3-1,t_2-1,t_1-1,(c-1)t_0+2c)` |
| `1` | `(1)` |
| `2` | `(t_3,t_2-1,t_1-1,t_0+1)` |
| `3` | `(1)` |

Hence only `q=0,2` survive generically, each at one marking.

### Generic `q=0`

Put

```text
t=(-2c/(c-1),1,1,1).
```

The rank-six mixed matrix has basis

```text
k_0=(1/2,0,-1/(2c),1/2,
     -(c+1)/(2(c-1)),(c+1)/(2c),1,0),
k_1=(0,1,1/c,0,0,(c-1)/c,0,1).                     (7)
```

For `e=u k_0+v k_1`, put

```text
L=(c+1)u+2(c-1)v.
```

The two binary diagonals and a mode-one marked minor are

```text
d_0=-(c-1)(u-2v)/(2c),
d_1= (c+1)L/c,
M_1=-(c+1)(u-2v)^2 L/(2c^3).                       (8)
```

Thus `d_0 d_1!=0` implies `M_1!=0`.

### Generic `q=2`

Put

```text
t=(-1,1,1,0)
```

and use

```text
k_0=(0,1,0,-1,1,0,0,0),
k_1=(0,-1,-1,0,0,c-1,0,1).                         (9)
```

For `e=u k_0+v k_1`,

```text
d_0=2(u-v),
d_1=4v(c+1),
M_0=64v(c+1)(u-v)^2,                                (10)
```

where `M_0` is the marked mode-zero minor on rows `000,010,011,111`.
Again the two binary diagonals force the marked minor to be nonzero.
Formula (10) remains valid at `c=0,1`.

## The special fibres

The global relative projection proves that the only nonzero-pure
fibres omitted by the function-field kernel formulas are `c=0,1`.

### `c=0`

The survivor markings are

```text
q=0: t=(0, 1,1,1),
q=2: t=(-1,1,1,0),
q=3: t=(0,-1,1,1).                                  (11)
```

The `q=2` case is (10).  For `q=0`, a kernel basis is

```text
(0,0,-1,0,0,1,0,0),
(1,1, 2,1,1,0,2,1);
```

for `q=3`, replace the second vector by

```text
(0,-1,2,1,1,0,0,1).
```

In both cases the diagonals are, up to one sign,

```text
u-2v, 2u,
```

and the same mode-one marked minor is

```text
-2u(u-2v)^2.                                        (12)
```

### `c=1`

The survivor markings are

```text
q=2: t=(-1,1,1,0),
q=3: t=(-1,1,1,1).                                  (13)
```

The `q=2` case is again (10).  At `q=3`, use

```text
k_0=(0,0, 1,1,1,0,0,0),
k_1=(0,-1,-1,0,0,0,0,1).
```

Then

```text
d_0=2(u-v),   d_1=8v,
M_1=-16v(u-v)^2.                                    (14)
```

This closes both special fibres.

## Ternary conclusion

In every case above, both nonzero binary diagonals force the selected
one-marked map to be injective.  Its pure-hyperplane column at the
distinguished coordinate is nonzero.  Therefore the third target row
vanishes first on the neighbouring hyperplane and then on its sole
remaining coordinate.  It is globally zero, contradicting rank three.

Hence no marked plane tuple on (2) with `c!=-1` lifts to `H31`.

## Verification

Run:

```text
python verify_p5_h31_diagonal_quadric_curve_marked_fibre.py
python audit_p5_h31_diagonal_quadric_curve_marked_fibre.py
```

The primary verifier recomputes the four global relative projections,
the four function-field projections, all eight special-fibre
projections, the mixed kernels, diagonal forms, and selected
all-extension minors.  It also checks the displayed source/mode
symmetry taking the `C=c` curve to the `H=h` curve.  The independent audit
rebuilds every marking fibre over `F_5,F_7`, excluding only `c=-1`,
and checks every genuine projective binary extension with a separate
dynamic-programming permanent.  The finite-field census is independent
QA; the function-field elimination and displayed identities are the
characteristic-zero proof.

Both checks pass.  The independent census covers `67,624` marking
fibres.  It finds exactly `22` binary-survivor markings and checks all
`158` projective kernel directions; `114` have both binary diagonals
nonzero, and every one has the predicted full-rank marked map.
