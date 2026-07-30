# The endpoint `t3=1` marking divisor is empty

## Status

This is an exact characteristic-zero obstruction for both endpoint
coordinates `q=0,3` on the complete regular marking divisor

```text
t3=1
```

of the elliptic normalization of the diagonal-quadric component.  With
the companion `t2=x` theorem, it closes the complete regular
end-coordinate quotient-rank complement.

The argument reframes the apparent high-degree exceptional cover in
two stages.  First, its discriminant is a square in the elliptic
function field, so the cover splits into two rational marking
branches.  Two quotient minors force either branch onto the same
genus-two trisection found at `t2=x,t3=1`.  On its normalization, the
four branch/sheet combinations reduce to elementary univariate gcds.
Only six values of the normalization parameter remain; exact
mixed-kernel and binary-diagonal ranks exclude all of them.

The theorem is stated away from the standard regular-chart factors

```text
r x (r^2-1) (x-1) (x+r^2-1) (x-1-r) (x-1+r)
```

and the normalization denominators displayed below.  It does not close
the remaining middle-coordinate pivot complement, the compactification
boundary, possible further pure-compression components, or `H22`.

## Elliptic quotient matrices

Put

```text
D=x+r^2-1,
f=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2],
Y^2=f.                                                   (1)
```

Use

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

Write `epsilon=+1` for `q=0`, `epsilon=-1` for `q=3`, and
`Z=epsilon Y`.

## The apparent cover splits

On `t3=1`, take the quotient determinants on rows

```text
A: (0,1,3,4,5,6,9),
E: (0,1,3,4,5,12,9).                                  (4)
```

After removing chart factors, both are linear in `t1`.  Eliminating
`t1` gives a quadratic in `t2`.  Its two roots in the elliptic
function field are

```text
t2- = -x(-Z+r^2x-r^2-x+1)/D,

t2+ = r^2x(2Z+r^2x+r^2+x-1)
      /[(r^2-1)(x-1)^2].                               (5)
```

Thus the apparent double cover is split, not a new irreducible curve.
For completeness, after removing the square chart unit
`x^2(x-1)^2`, the norm of its discriminant is, up to a nonzero
constant,

```text
x^4(r-1)^6(r+1)^6(x-1)^2
(x-1-r)^2(x-1+r)^2D^8 R^2 K^2,                        (6)
```

where

```text
R =
 r^8-r^6x-4r^6+3r^4x^2-9r^4x+6r^4
 +r^2x^3-6r^2x^2+9r^2x-4r^2
 -x^3+3x^2-3x+1,                                     (7)

K =
 r^8+2r^6x^2+9r^6x-4r^6
 +r^4x^4-9r^4x^3+24r^4x^2-22r^4x+6r^4
 -2r^2x^4+13r^2x^3-24r^2x^2+17r^2x-4r^2
 +x^4-4x^3+6x^2-4x+1.                                (8)
```

On the minus branch, (4) forces the compact rational value

```text
t1 =
 -epsilon[
   (epsilon Y)r^2-(epsilon Y)x+epsilon Y
   -2r^4+2r^2x^2-6r^2x+4r^2-2x^2+4x-2
 ]/D.                                                 (9)
```

Use the two further quotient minors

```text
J1: (0,1,3,4,5,11,9),
J2: (0,1,3,4,5,13,9).                                (10)
```

Substituting (5)--(9), taking elliptic norms, and removing only the
standard chart factors gives

```text
gcd(Norm J1,Norm J2) ~ R                              (minus),
gcd(Norm Res_t1(E,J1),Norm Res_t1(E,J2)) ~ R^2        (plus). (11)
```

The resultant form on the plus branch retains fibres where the
coefficient used to solve for `t1` vanishes.  Hence (11) has no hidden
pivot assumption: away from `R=0`, at least one quotient minor is
nonzero on either branch.

## Pullback to the genus-two normalization

Set

```text
d=s^3+3s^2-s+1,
n=s^3+3s^2+3s+5,

r=v/d,
x=(s+1)^4/d,
Y=epsilon sigma (s-1)(s+1)^3n/d^2,
v^2=nd,                                                (12)
```

where `sigma=+1,-1` labels the two sheets above `R=0`.  The sextic
`nd` has discriminant `2^24 3^3 11`, so (12) is a smooth genus-two
normalization.

On the positive sheet `sigma=+1`, the two split branches have

```text
t1=epsilon (s-1)^2(s+1)(s+3)n/d^2,
t0=-d^2/[2s(s+1)^3n],                                 (13)

t2-=(s+1)^4(s^3+s^2-5s-1)/d^2,
t2+=(s+1)^4(s+2)/d.                                   (14)
```

Three complementary quotient minors have residual gcd

```text
s^2+2s-1                                                (minus),
1                                                        (plus). (15)
```

Thus the plus branch is empty.  The minus branch remains only at
`s=-1+/-sqrt(2)`.

On the negative sheet `sigma=-1`, the minus branch is

```text
t2-=-(s+1)^4(s^3+s^2+3s-1)/d^2,
t1-=-epsilon (s-1)^3(s+1)n/d^2,
t0-=-d^2/[2(s+1)^3n].                                 (16)
```

For the plus branch put

```text
P=2s^5+7s^4+6s^3+4s^2+1,
N=2s^6+5s^5+7s^4+6s^3-4s^2+s-1.                      (17)
```

Then

```text
t2+=(s+1)^4(s^2+s+1)/(s^2d),
t1+=-epsilon nN/(dP),

t0+=
 -d^2(s^5+3s^4+4s^3+4s^2-s+1)
 /[(s+1)^4nP].                                        (18)
```

There is no marking hidden at `P=0`, since

```text
gcd(P,N)=1,       Res_s(P,N)=2^19.                    (19)
```

For both negative-sheet branches, the square-free common factor of
the two minors in (10) is

```text
s(s-1)(s^2+1).                                        (20)
```

The factor `s=0` is the already closed `x=1` ruling.  The remaining
regular values are `s=1,+i,-i`.

## Exact closure of the finite exceptions

At each value left by (15) and (20), substitute both points
`v=+/-sqrt(nd)` of the genus-two cover.  Let `M` be the full
`14 x 8` mixed matrix and let `d_alpha,d_beta` be the two binary
diagonal rows.  Exact algebraic-number ranks are:

| sheet and parameter | branch | `rank M` | `rank[M;d_alpha]` | `rank[M;d_beta]` |
| --- | --- | ---: | ---: | ---: |
| `sigma=+1`, `s=-1+/-sqrt(2)` | minus | 6 | 7 | 6 |
| `sigma=-1`, `s=1` | minus or plus | 7 | 7 | 8 |
| `sigma=-1`, `s=+/-i` | minus or plus | 6 | 7 | 6 |

The table is unchanged for either sign of `v` and for both
`q=0,3`.  When `rank M=7`, its only kernel line is the universal line
and the other diagonal is nonzero on it.  When `rank M=6`,
`d_beta` vanishes on the whole mixed kernel while `d_alpha` cuts it
back to that same universal line.  In neither case is there an
additional kernel vector killed by both diagonals.

Therefore the complete regular `t3=1` divisor contains no genuine
binary extension for either endpoint.  Together with the dense
end-coordinate chart and the complete `t2=x` theorem, every regular
end-coordinate marking is excluded.

## Verification

Run:

```text
python verify_p5_h31_elliptic_end_t3_divisor.py
python audit_p5_h31_elliptic_end_t3_divisor.py
```

The primary verifier expands permanents directly.  It checks the split
roots, the discriminant norm, both generic branch gcds, all four
genus-two branch/sheet markings, the residual univariate gcds, and the
exact finite-point rank table.  The `q=3` endpoint is run in a fresh
process to control symbolic expression swell.

The independent audit rebuilds all mixed and diagonal coefficient rows
using a subset-DP permanent, repeats the exact calculation for both
endpoints, and then replays the primary verifier.
