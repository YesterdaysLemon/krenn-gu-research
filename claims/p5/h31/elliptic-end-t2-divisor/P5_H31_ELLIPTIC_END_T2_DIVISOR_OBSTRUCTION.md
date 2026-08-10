# The endpoint `t2=x` marking divisor is empty

## Status

This is an exact characteristic-zero obstruction for both end
coordinates `q=0,3` on the complete regular marking divisor

```text
t2=x
```

of the elliptic normalization of the diagonal-quadric component.  It
extends the dense end-coordinate chart and the previously closed
intersection `t2=x,t3=1`.

The argument is determinantal and geometric.  One small quotient minor
forces every possible rank drop either onto `t3=1` or onto the smooth
genus-two trisection already found at the deepest intersection.  On its
normalization, four further minors reduce the whole remaining marking
problem to two univariate polynomials.  Their only regular common-root
exception is a quadratic pair, where a final minor is nonzero.

The theorem is stated away from the standard regular-chart factors

```text
r x (r^2-1) (x-1) (x+r^2-1) (x-1-r) (x-1+r)
```

and the normalization denominators displayed below.  It does not close
the other marking divisor `t3=1`, the elliptic compactification
boundary, or possible further pure-compression components.

## Elliptic quotient matrices

Put

```text
D=x+r^2-1,
f=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2],
Y^2=f.                                                   (1)
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

beta_i(t)=beta_i+t_i alpha_i.                            (2)
```

For `q=0,3`, delete the unit `a1` component of the universal mixed
kernel:

```text
N_q=M_q[:,(a0,a2,a3,b0,b1,b2,b3)].                     (3)
```

Write `epsilon=+1` for `q=0` and `epsilon=-1` for `q=3`.

## A minor that forces the genus-two curve

On `t2=x`, the quotient determinant on rows

```text
(0,1,3,4,5,10,9)
```

is

```text
128 r^5 x^6(r^2-1)(x-1)(t3-1)L_epsilon,                (4)
```

where

```text
L_epsilon=B+epsilon Y C,

B=r^8x-5r^6x+3r^4x^3-10r^4x^2+7r^4x
  -3r^2x^3+6r^2x^2-3r^2x,

C=-r^6+2r^4x+3r^4-r^2x^2+4r^2x-3r^2
  +x^2-2x+1.                                           (5)
```

Its quadratic-field norm is

```text
B^2-C^2f
 =x(r^2-1)^2(x-1)D^2 R,                                (6)
```

with

```text
R =
 r^8-r^6x-4r^6+3r^4x^2-9r^4x+6r^4
 +r^2x^3-6r^2x^2+9r^2x-4r^2
 -x^3+3x^2-3x+1.                                      (7)
```

Moreover, on

```text
Y=epsilon r^2x(x-r^2-1)/D,
```

one has

```text
L_epsilon=2r^2xR/D.                                    (8)
```

Thus, away from `t3=1` and the standard factors, rank drop forces the
same conjugate pair of residual trisections as in the deepest
intersection theorem.

## Pullback to the genus-two normalization

Set

```text
d=s^3+3s^2-s+1,
n=s^3+3s^2+3s+5,

r=v/d,
x=(s+1)^4/d,
Y=epsilon(s-1)(s+1)^3n/d^2,
v^2=nd.                                                (9)
```

The sextic `nd` is smooth, so this is the genus-two normalization.
On (9), a quotient minor forces

```text
t1=epsilon (s-1)^2(s+1)(s+3)n/d^2.                    (10)
```

The determinant on rows

```text
(0,1,3,4,6,7,9)
```

then equals a chart unit times

```text
Phi =
 2s(s+1)^4n t0-((s-1)t3-2s)d^2.                       (11)
```

Hence any remaining rank drop has

```text
t0=((s-1)t3-2s)d^2/[2s(s+1)^4n].                      (12)
```

## Two incompatible residual minors

After (10)--(12), the determinants on rows

```text
(0,1,3,4,6,9,11),
(0,1,3,4,6,9,12)
```

are, respectively,

```text
 epsilon 4096 v(s+1)^27 n^7 L1/d^17,
 epsilon 4096 v(s+1)^27 n^7 t3 L2/d^17,               (13)
```

where

```text
L1=s^4+3s^3-s^2+s+2(1-s)t3,
L2=s^3+s^2+3s-1+2(1-s)t3.                             (14)
```

Their residual resultant is

```text
Res_t3(L1,t3 L2)
 =-2s(s-1)^2(s+1)(s^2+2s-1)d.                         (15)
```

The factors `s=-1` and `d=0` are outside the chart.  The case `s=0`
is `x=1`, already closed by the `H=0` ruling theorem.  At `s=1`, the
apparent resultant factor comes only from degree drop:

```text
L1=4,  t3 L2=4t3,
```

so there is no common root.

It remains only

```text
s^2+2s-1=0.
```

Equations (14) then force `t3=-s`.  On this quadratic pair, the
numerator of the quotient minor on rows

```text
(0,1,3,4,6,8,9)
```

reduces modulo `v^2=nd` and `s^2+2s-1` to

```text
-2^34 v(12s+29).                                      (16)
```

Since

```text
gcd(s^2+2s-1,12s+29)=1
```

and `v` is a chart unit, (16) is nonzero.  Therefore at least one
quotient determinant is nonzero at every point of the regular
`t2=x` divisor.  The full mixed kernel is only the universal line,
which kills the first binary diagonal.  No genuine binary extension,
and hence no `H31` lift, occurs there for either `q=0` or `q=3`.

## Verification

Run:

```text
python claims/p5/h31/elliptic-end-t2-divisor/verify_p5_h31_elliptic_end_t2_divisor.py
python claims/p5/h31/elliptic-end-t2-divisor/audit_p5_h31_elliptic_end_t2_divisor.py
```

The primary verifier expands permanents directly.  It checks
(4)--(16) in the elliptic and genus-two function fields, with the `q=3`
calculation isolated in a fresh process to avoid symbolic
expression-swell artifacts.

The independent audit rebuilds both mixed systems with a subset-DP
permanent and repeats the same exact determinant identities before
replaying the primary verifier.
