# A second closed marked curve on the diagonal-quadric component

## Status

This is an exact characteristic-zero marked-fibre theorem on a second
rational curve of the diagonal-quadric pure rank-two `P_4` component.

For every `e in C`, every marking of the four planes below, every
distinguished common source coordinate, and every genuine binary
`Delta_2` extension direction is excluded from an `H31` lift.  A
single relative projection over `Q[e]` classifies all fibres at once;
there is no function-field specialization assumption.

This curve contains the earlier isolated point theorem at `e=2` and
meets the closed `C=c` curve at `e=1,c=0`.  The two curve theorems do
not prove a generic statement on the five-dimensional component, close
its boundary, classify further components, settle `H22`, or solve the
prize problem.

## The `E=e` curve

In the normal form of
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md),
set

```text
A=B=F=H=1,   C=0,   E=e.                            (1)
```

The component equation `Psi=0` holds identically.  The four planes are

```text
U_0=span((e,-1,-1,-e),(1,-1, 1, 1)),
U_1=span((1, 0, 0,-1),(1, 1,-1, 1)),
U_2=span((1+e,1,1,1-e),(0,1,-1,0)),
U_3=span((1, 0, 0, 1),(0,1, 1,0)).                 (2)
```

They have rank two for every `e`.  Mark kernel rows

```text
alpha_0=(e+1,-2, 0,1-e),
alpha_1=(1,0,0,-1),
alpha_2=(0,1,-1,0),
alpha_3=(1,-1,-1,1),                                (3)
```

and pure-colour rows

```text
beta_0=(1,-1, 1,1),
beta_1=(1, 1,-1,1),
beta_2=(e+1,1,1,1-e),
beta_3=(0,1,1,0).                                   (4)
```

The only nonzero restricted coefficient is

```text
Perm(beta_0,beta_1,beta_2,beta_3)=4.                (5)
```

Thus the entire affine curve is nonzero-pure.  Every marking is

```text
beta_i(t)=beta_i+t_i alpha_i.                        (6)
```

## Global relative binary projection

Normalize one binary diagonal and invert the other.  Retain `e` and
the four marking variables during elimination.  Exact elimination over
`Q` gives:

| `q` | relative survivor marking ideal in `Q[e,t]` |
| ---: | --- |
| `0` | `(t_3-1,t_2-1,t_0-t_1+1,e(t_1-1),t_1(t_1-1))` |
| `1` | `(1)` |
| `2` | `(t_3,t_2-1,t_1-e,2t_0+1,e^2-1)` |
| `3` | `(t_3-1,t_2-1,t_0+t_1+1,e(t_1+1),t_1(t_1+1))` |

Consequently the complete survivor list is:

```text
all e, q=0: t=(0, 1,1,1);
all e, q=3: t=(0,-1,1,1);
e=0, q=0:   t=(-1,0,1,1);
e=0, q=3:   t=(-1,0,1,1);
e=1, q=2:   t=(-1/2, 1,1,0);
e=-1,q=2:   t=(-1/2,-1,1,0).                       (7)
```

Because `e` remains an ordinary retained variable, (7) has no hidden
complex exceptional fibres.

## The two uniform kernels

For `q=0`, use

```text
k_0=(0,0,-1,0,0,1,0,0),
k_1=(e+1,1,2,1,1,0,e+1,1).                         (8)
```

For `q=3`, replace the second vector by

```text
k_1=(1-e,-1,2,1,1,0,1-e,1).                        (9)
```

Both mixed matrices have rank six for every `e`.  If
`z=u k_0+v k_1`, their binary diagonals are respectively

```text
q=0:  2(u-2v), 2u;
q=3: -2(u-2v), 2u.                                 (10)
```

In both orientations, the mode-one marked minor on rows
`000,001,101,111` is

```text
-8u(u-2v)^2.                                       (11)
```

Thus every genuine extension in the two uniform kernels has an
injective marked map.

## The `e=0` jump

At either `q=0` or `q=3`, the extra marking in (7) has basis

```text
k_0=(1,0,0,1,0,1,1,0),
k_1=(0, 1,0,0,0,0,0,1)  for q=0,
k_1=(0,-1,0,0,0,0,0,1)  for q=3.                  (12)
```

The diagonals are, up to the orientation sign,

```text
2(u-v), 2(u+v).                                    (13)
```

The mode-zero marked minor on rows `000,010,100,111` is

```text
8(u-v)(u+v)^2.                                     (14)
```

Both nonzero diagonals force (14) to be nonzero.

## The `e=+/-1` jumps

At `q=2,e=1`, take

```text
k_0=(0, 1,0,-1,1,0,0,0),
k_1=(0,-1,-1,0,0,-1,0,1).                         (15)
```

At `q=2,e=-1`, take

```text
k_0=(0,-1,0,-1,1,0,0,0),
k_1=(0, 1,-1,0,0,-1,0,1).                         (16)
```

For `z=u k_0+v k_1`, the diagonals are

```text
e= 1:  4(u-v),4v;
e=-1: -4(u-v),4v.                                  (17)
```

The mode-zero marked minor on rows `000,010,011,111` is

```text
64v(u-v)^2                                         (18)
```

in both fibres.  It is nonzero for every genuine extension.

## Ternary conclusion

Every selected marked map above is injective whenever both binary
diagonals are nonzero, and its pure-hyperplane column at the
distinguished coordinate is nonzero.  The third target row of an
alleged `H31` map therefore vanishes on the neighbouring hyperplane
and on its sole remaining coordinate.  It is globally zero,
contradicting rank three.

Hence no marked plane tuple on (2), for any `e in C`, lifts to `H31`.

## Verification

Run:

```text
python verify_p5_h31_diagonal_quadric_e_curve_marked_fibre.py
python audit_p5_h31_diagonal_quadric_e_curve_marked_fibre.py
```

The primary verifier recomputes the four relative projections, the
six survivor kernel types, both diagonal forms, and every displayed
all-extension marked minor over characteristic zero.  The independent
audit rebuilds all parameter and marking fibres over `F_5,F_7` with a
separate dynamic-programming permanent, then checks every genuine
projective kernel direction.  The finite-field census is independent
QA; the relative elimination and displayed identities are the proof
over `C`.

Both checks pass.  The independent census covers `79,728` marking
fibres.  It finds exactly `32` binary-survivor markings and checks all
`228` projective kernel directions; `164` have both binary diagonals
nonzero, and every one has the predicted full-rank marked map.
