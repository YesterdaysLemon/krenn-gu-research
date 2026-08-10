# The end-coordinate universal kernels and a full-rank quotient chart

## Status

This is an exact characteristic-zero dense-chart obstruction for the
end distinguished source coordinates `q=0,3` on the elliptic
normalization of the diagonal-quadric component.

For each end coordinate, the mixed binary-extension matrix has an
explicit marking-independent kernel line.  After quotienting that line,
one `6 x 6` pivot and one bordered `7 x 7` minor prove that the quotient
has full column rank on the chart below.  Hence no binary survivor occurs
there.

The marking divisors `t2=x` and `t3=1`, the `H=0` section, singular/base
factors, and the compactification boundary are not claimed here.

## Elliptic rows

Put

```text
D=x+r^2-1,
f=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2],
Y^2=f.                                                   (1)
```

Use the denominator-cleared marked rows

```text
alpha0=(Y+r^2x,-rx-r^2x,-rx+r^2x,-Y+r^2x),
alpha1=(1,0,0,-1),
alpha2=(0,1,-1,0),
alpha3=(r,-1,-1,r),

beta0=(1,-1,1,1),
beta1=(D,rx+D,rx-D,D),
beta2=(x(1-x)+Y,rx,rx,x(1-x)-Y),
beta3=(0,1,1,0),                                       (2)
```

with `beta_i(t)=beta_i+t_i alpha_i`.

## The two small kernel lines

Order the extension columns as

```text
(a0,a1,a2,a3,b0,b1,b2,b3).
```

At zero marking, the end-coordinate mixed kernels contain

```text
q=0:
(Y+r^2x,1,0,r, 1,D,Y+x-x^2,0),

q=3:
(Y-r^2x,1,0,-r, -1,-D,Y-x+x^2,0).                    (3)
```

For arbitrary marking, replace `b_i` by `b_i+t_i a_i`.  The resulting
vectors `k_q(t)` satisfy

```text
M_q(t)k_q(t)=0,
d_alpha,q k_q(t)=0,

d_beta,0 k_0(t)=-4rx(x-1-r)(x-1+r),
d_beta,3 k_3(t)= 4rx(x-1-r)(x-1+r).                  (4)
```

Thus a genuine binary direction again requires an additional mixed
kernel vector.

## Quotient rank

The `a1` component in (3) is one.  Delete that column and write

```text
N_q=M_q[:,(a0,a2,a3,b0,b1,b2,b3)].
```

Select rows

```text
0,1,2,3,4,9
```

and quotient columns

```text
0,1,2,3,4,6.
```

The resulting `6 x 6` pivots are

```text
q=0:
 64 r^8 x^5 (r^2x-Y)(r-1)(r+1)(x-t2)(t3-1)(x-1),

q=3:
 64 r^8 x^5 (r^2x+Y)(r-1)(r+1)(x-t2)(t3-1)(x-1).    (5)
```

Border the pivot by row `11` and the remaining quotient column `b2`.
The two `7 x 7` determinants are

```text
q=0:
 128 r^7 x^4 (r^2x-Y)(r-1)(r+1)
     (x-t2)(t3-1)(x-1)D,

q=3:
 128 r^7 x^4 (r^2x+Y)(r-1)(r+1)
     (x-t2)(t3-1)(x-1)D.                             (6)
```

On (1),

```text
(r^2x-Y)(r^2x+Y)=x(r-1)(r+1)(x-1)D.                 (7)
```

Therefore both factors `r^2x+/-Y` are units on

```text
r x D (r^2-1)(x-1)(x-t2)(t3-1) != 0.                (8)
```

Equations (5)--(6) show that `N_q` has rank seven on (8).  Since (3)
already gives a kernel of `M_q`, the full mixed matrix has rank exactly
seven and its kernel is precisely the universal line.  The first
diagonal vanishes on that line by (4), so no genuine binary extension
exists.

Together with the middle-coordinate rank-drop theorem, this closes one
explicit dense quotient chart for all four distinguished coordinates.
It does not close the chart complements.

## Verification

Run:

```text
python verify_p5_h31_elliptic_end_coordinate_full_rank_chart.py
python audit_p5_h31_elliptic_end_coordinate_full_rank_chart.py
```

The primary verifier uses direct permanent expansion.  The independent
audit rebuilds all coefficients with a subset-DP permanent and replays
the primary only after its own exact checks.
