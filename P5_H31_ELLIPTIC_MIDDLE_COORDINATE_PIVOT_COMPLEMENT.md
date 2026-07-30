# The regular middle-coordinate pivot complement is empty

## Status

This is an exact characteristic-zero obstruction for the complete
regular middle-coordinate locus `q=1,2` on the elliptic normalization
of the diagonal-quadric component.

Together with the dense middle-coordinate pivot theorem and the
complete endpoint theorems, it proves that every possible survivor in
the regular elliptic chart has already been excluded.  The remaining
work on this component is its birational/compactification boundary, not
another marking divisor in the elliptic function field.

The proof uses a small cover of the quotient-matrix Fitting ideal.  It
does not enumerate constructions.  Nine selected `7 x 7` determinants
reduce the three missing marking divisors to incompatible linear
factors.  A separate two-minor pivot covers the regular two-torsion
slice `Y=0`.

## Setup

Put

```text
D=x+r^2-1,
f=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2],
Y^2=f,
Q=-f/x=-Y^2/x.                                        (1)
```

Use the rows

```text
alpha0=(Y+r^2x,-rx-r^2x,-rx+r^2x,-Y+r^2x),
alpha1=(1,0,0,-1),
alpha2=(0,1,-1,0),
alpha3=(r,-1,-1,r),

beta0=(1,-1,1,1),
beta1=(D,rx+D,rx-D,D),
beta2=(x(1-x)+Y,rx,rx,x(1-x)-Y),
beta3=(0,1,1,0),

beta_i(t)=beta_i+t_i alpha_i.                         (2)
```

For `q=1,2`, delete the unit `a2` component of the known universal
mixed-kernel line and call the resulting `14 x 7` quotient matrix
`N_q`.  Write

```text
sigma=-1 for q=1,
sigma=+1 for q=2.                                     (3)
```

We work away from

```text
r x D (r^2-1)(x-1)(x-1-r)(x-1+r)=0.                 (4)
```

The `x=1` ruling, the pure-direction curves, and the singular fibres in
(4) are already closed by their complete marked-fibre theorems.

## Four residual factors

Define

```text
F=(x-1)(r^3-r+sigma)+sigma r^2(x+1),
L=Y r^2 D+t1 Q,
G=t3 F+(r-sigma)D,

A=2 sigma r^2x+r t2+r x^2-rx
  -sigma t2+sigma x^2-sigma x.                       (5)
```

The quotient determinants on rows

```text
R0=(0,1,2,3,4,5,9),
RF=(0,1,2,3,4,6,9),
RL=(0,1,2,3,5,6,9),
RH=(0,1,2,3,5,7,9)                                   (6)
```

have, up to the explicit chart units checked by the verifier, residual
factors

```text
det R0 ~ t3 F L,
det RF ~ t3 L G,
det RL ~ A B,
det RH ~ F H,                                         (7)
```

where `B` is linear in `t1,t3` and

```text
B | L=0 ~ G,

H | t0=0 = (t3-1)(t2-r^2x),
H | t2=r^2x = r t0 x^2(r+sigma)D,

A | t2=r^2x = x(r+sigma)D,
G | t3=1 = r^2x(r+sigma).                             (8)
```

The earlier `6 x 6` pivot shows that only

```text
t0=0,       t3=1,       t2=r^2x                       (9)
```

need be considered on the regular `Y!=0` chart.  Equations (7)--(8)
turn each divisor into a short case tree.

## The auxiliary base curve is harmless

The only base factor introduced by the alternative minors is `F=0`.
It is linear in `x`.  Put

```text
a=r^3+sigma r^2-r+sigma,
b=r^3+3 sigma r^2+3r+3 sigma.                        (10)
```

Then

```text
x=(r+sigma)(r-sigma)^2/a,

Y^2 =
 r^4(r+sigma)^2(r-sigma)^4 b/a^3.                    (11)
```

The coefficient and constant term of `F` have resultant `8 sigma`,
so (11) misses no affine point of `F=0`.  On the regular `Y!=0`
chart, `r(r^2-1)abY` is nonzero.

Successive terminal determinants on rows

```text
(0,1,2,3,5,9,11),
(0,1,2,3,6,7,9),
(0,1,2,3,6,9,11),
(0,1,2,3,5,9,10),
(0,1,2,3,6,9,10)                                    (12)
```

pull back to nonzero chart units times only one of

```text
1,       t0,       t3-1,       C(t2),                (13)
```

where

```text
C =
 r^5-sigma r^4-r^3t2-r^3
 -sigma r^2t2+sigma r^2+r t2-sigma t2.               (14)
```

When `C=0`, the last determinant in (12) is a unit.  Thus the
genus-two-looking double cover in (11) is not a survivor curve; it is
only an intermediate base factor of this Fitting cover.

## Closure of the three marking divisors

On `t0=0`, first take `t3=0`.  The `RL` minor forces `A=0` or
`B(t3=0)=0`.  The `RH` minor then forces `F=0` or `t2=r^2x`.
The value `A(r^2x)` is a unit.  On `F=0`, the minors in (12) are
successively a unit, or force `C=0` and are followed by a unit.  The
remaining `t2=r^2x` branch is closed by the same final pair.

For `t3!=0`, the first two minors in (7) force `L=0`.
The third then forces `A=0` or `G=0`.  If `A=0`, (8) and the first
three minors in (12) reduce every possible rank drop to their common
deepest intersection, where the third is a unit.  If `G=0`, then
`F!=0`; (8) leaves only `t2=r^2x`, where the fourth minor in (12) is a
unit.  Hence the complete regular `t0=0` divisor is empty.

On `t3=1`, (7)--(8) force `L=A=0`.  The `RH` minor and the second
terminal minor reduce every possible rank drop to `t0=0`, already
closed.

On `t2=r^2x`, the value of `A` in (8) is a unit.  If `L=0`, the
`RL` minor forces `G=0`, and `RH` reduces to `t0=0`.  If `t3=0`,
`RL`, `RH`, and the second terminal minor again reduce to `t0=0`.
The `F=0,t3!=0` branch is incompatible with `RF` and `RL`.  Hence this
third regular divisor is empty as well.

## The regular two-torsion slice

It remains to remove the temporary assumption `Y!=0`.  On `Y=0`, the
elliptic equation is

```text
x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2]=0.                (15)
```

The `x=0` component is a birational boundary.  On the regular
nonzero-`x` component, the determinant on rows

```text
(0,3,4,5,6,11,13)
```

is a chart unit times `t3`.  At `t3=0`, the determinant on rows

```text
(2,3,4,5,6,11,13)
```

is itself a chart unit, independent of every remaining marking.
Therefore `N_q` has rank seven throughout the regular `Y=0` slice.

In every case, the full mixed kernel is only the known universal line.
That line kills the first binary diagonal and not the second on (4),
so no genuine binary extension survives.

Consequently every regular marked fibre of the diagonal-quadric
component is excluded for all four distinguished coordinates.  This
does not yet close `rxD=0`, the compactification boundary, possible
further pure-compression components, or `H22`.

## Verification

Run:

```text
python verify_p5_h31_elliptic_middle_coordinate_pivot_complement.py
python audit_p5_h31_elliptic_middle_coordinate_pivot_complement.py
```

The primary verifier expands permanents directly and checks every
identity in (1)--(15), including the terminal pullbacks on `F=0` and
the two-torsion pivots.

The independent audit rebuilds the mixed and diagonal systems with a
subset-DP permanent and repeats the exact Fitting-cover calculation
before replaying the primary verifier.
