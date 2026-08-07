# The pure-direction boundary curve and a closed factored slice

## Status

This is an exact characteristic-zero marked-fibre theorem on the
pure-factor-direction boundary of the diagonal-quadric component.

For every `e in C` with `e^2!=1`, every marking of the four planes
below, every distinguished common source coordinate, and every genuine
binary `Delta_2` extension direction is excluded from an `H31` lift.
The proof is one relative projection over `Q[e]`, saturated only by the
nonzero-pure coefficient.

Combined with the two earlier curve theorems and one source-coordinate
symmetry, this closes the entire nonzero factored slice

```text
A=B=F=H=1.
```

The same conclusion holds on every source/mode symmetry translate of
that slice.

It is not a generic theorem on the five-dimensional component, a
boundary compactification, a classification of further components, an
`H22` result, or a solution of the prize problem.

## The pure-direction curve

In the normal form of
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md),
set

```text
A=B=F=H=1,   C=-1,   E=e.                           (1)
```

The component equation vanishes identically.  Use

```text
U_0=span((e,-1,-1,-e),(1,-1, 1,1)),
U_1=span((1, 0, 0,-1),(1, 0,-2,1)),
U_2=span((1+e,1,1,1-e),(0,1,-1,0)),
U_3=span((1, 0, 0, 1),(0,1, 1,0)).                 (2)
```

All four planes have rank two for every `e`.  On this curve the
`2 x 2` pure coefficient matrix has only its upper-right entry
nonzero.  Therefore mark

```text
alpha_0=(1,-1, 1,1),        beta_0=(e,-1,-1,-e),
alpha_1=(1, 0, 0,-1),       beta_1=(1, 0,-2, 1),
alpha_2=(0, 1,-1,0),        beta_2=(1+e,1,1,1-e),
alpha_3=(1, 0, 0,1),        beta_3=(0,1,1,0).       (3)
```

The only nonzero restricted coefficient is

```text
Perm(beta_0,beta_1,beta_2,beta_3)=4(e^2-1).         (4)
```

Thus `e=+/-1` are zero-tensor points and every marking on the nonzero
locus is `beta_i(t)=beta_i+t_i alpha_i`.

## Global relative projection

Normalize one binary diagonal, invert the other, and saturate by
`e^2-1`.  Retaining `e,t_0,...,t_3`, exact elimination gives

| distinguished `q` | relative marking ideal |
| ---: | --- |
| `0` | `(1)` |
| `1` | `(1)` |
| `2` | `(t_3,t_2+1,t_0-1,2e t_1+e^2+1)` |
| `3` | `(1)` |

At `e=0` the last equation is a unit, so no marking survives.  For

```text
e(e^2-1)!=0,
```

there is exactly one survivor:

```text
q=2,  t=(1,-(e^2+1)/(2e),-1,0).                    (5)
```

Because `e` was retained throughout the saturated elimination, there
are no hidden exceptional complex fibres.

## The survivor kernel

The mixed matrix at (5) has rank six.  A kernel basis is

```text
k_0=1/(e^2-1) *
    (-2,-2e,0,-2,e^2-1,4,e^2-1,0),

k_1=1/(e^2-1) *
    (e^2+3,4e,1-e^2,4,-2(e^2-1),-2(e^2+3),0,e^2-1).
                                                               (6)
```

For `z=u k_0+v k_1`, the two binary diagonals are

```text
d_0=-4e(u-2v)/(e^2-1),
d_1= 2u(e^2-1).                                     (7)
```

The mode-one marked minor on rows `000,100,110,111` is

```text
-64e u(u-2v)^2.                                    (8)
```

On the nonzero-pure survivor locus, `d_0 d_1!=0` forces (8) to be
nonzero.  The pure-hyperplane column at the distinguished coordinate
is also nonzero.  The usual transverse-kernel argument makes the third
target row vanish globally, contradicting rank three.

Hence no point of (2) with `e^2!=1` lifts to `H31`.

## The complete factored slice

On the larger slice `A=B=F=H=1`, equation `Psi=0` factors as

```text
C(C+1)(1-E^2)=0.                                   (9)
```

Its nonzero points are covered as follows:

- `E=1`: the closed `C=c` curve;
- `E=-1`: the image of `E=1` under the source swap `X_0<->X_3`;
- `C=0`: the closed `E=e` curve;
- `C=-1`: the pure-direction curve proved here.

At `C=-1,E=+/-1` the restricted tensor is zero, so no nonzero point is
missed.  Therefore every marked fibre on the nonzero locus of (9), and
on its full discrete source/mode symmetry orbit, is excluded from
`H31`.

## Verification

Run:

```text
python verify_p5_h31_diagonal_quadric_pure_direction_curve.py
python audit_p5_h31_diagonal_quadric_pure_direction_curve.py
```

The primary verifier recomputes the saturated relative projections,
the unique survivor kernel, both diagonals, the selected all-extension
minor, the factorization (9), and the source symmetry.  The independent
audit enumerates every nonzero-pure parameter and marking over
`F_5,F_7`, then checks every projective kernel direction with a
separate dynamic-programming permanent.  The finite-field calculation
is QA; the relative elimination and exact identities prove the result
over `C`.

Both checks pass.  The independent census covers `55,520` marking
fibres.  It finds exactly `6` binary-survivor markings and checks all
`44` projective kernel directions; `32` have both binary diagonals
nonzero, and every one has the predicted full-rank marked map.
