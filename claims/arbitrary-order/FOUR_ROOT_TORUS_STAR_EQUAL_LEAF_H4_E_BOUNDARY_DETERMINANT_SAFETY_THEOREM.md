# Four-root torus-star equal-leaf H4 `e=0` determinant safety (GLD94)

Status: exact scoped characteristic-zero theorem; global Krenn--Gu remains
**UNRESOLVED**.

## Statement

Work over `Q`, and then base-change to `C`, in the normalized equal-leaf H4
chart

```text
d0 = p+q-1 != 0,
s = (p+q-pq)/d0,
G = [[1,1,1], [p,q,s], [a,1+b,1+c]].
```

Let `M(G)` be the fixed 37-by-9 GLD71 syndrome matrix, and let `B` be the
equal-leaf base equation.  The GLD75/GLD86 bridge says that on `B`, with the
scale-fixed last centre coordinate `C_8=1`,

```text
rank(A) <= 6  ==>  rank(M(G)) <= 6.
```

Define

```text
e  = 2*p*q^2 - 2*p*q - p - q^2 - 2*q + 2,
P  = p^2-p+1,
L1 = p^2+2*p*q-2*p-q,
L2 = 2*p*q-p+q^2-2*q,
Q6 = (the common GLD90 raw-pivot factor).
```

Then the determinant-safe rank-at-most-six locus on the retained boundary is

```text
B intersect V(I_7(A)) intersect D(Omega) intersect V(e) = empty.
```

Here the equality is a complete H4-chart statement after the already
published GLD87/GLD89 collision and `d0/P` cases are restored.  The proof is
set-theoretic and determinant-safe: it excludes the centre frame `D(Omega)`
because every surviving low-rank family has a singular centre.  It does not
assert that the unsaturated leaf family is empty.

## Exact `e=0` parameterisation and exceptional values

Put `t=q`,

```text
D(t) = 2*t^2-2*t-1,
N(t) = t^2+2*t-2,
p = N(t)/D(t).
```

Since `gcd(D,N)=1` in `Q[t]`, `D=0` gives no affine point of `e=0`.
The relevant restrictions are

```text
d0       = (2t-1)(t^2-t+1)/D,
p-q      = -(t-2)(t+1)(2t-1)/D,
p-s      = 9t(t-1)/((2t-1)D),
q-s      = 2(t^2-t+1)/(2t-1),
P        = 3(t^2-t+1)^2/D^2,
L1       = 9t(t-1)(t^2-t+1)/D^2,
L2       = 2(t^2-t+1)^2/D,
Q6       = 8(t^2-t+1)^6/D^4,
T        = 2pq-p-q+2 = 9t(t-1)/D.
```

Thus the collision-free subopen is obtained by removing
`t(t-1)(t-2)(t+1)(2t-1)(t^2-t+1)=0`.  The removed values are not divided
away: `t=2,-1` gives `p=q` (H1, GLD87); `t=0,1` gives `p=s` (H2, GLD87);
`t^2-t+1=0` gives `q=s` and `P=0` (H3, GLD87/GLD89); and `t=1/2` gives
`d0=0` together with `p=q` (GLD89).  The quadratic `D=0` has no affine
`e=0` point.

## Simultaneous-pivot obstruction

For the fixed pivot columns

```text
S = (0,1,3,4,6,7),
```

the two raw six-pivots on rows

```text
R0 = (0,1,2,17,19,32),
R1 = (0,1,17,19,28,32)
```

are exactly `-6*(p-q)^2*X0*Q6` and `-6*(p-q)^2*X1*Q6`, where

```text
X0 = a*(p^2-1) - (b+1)*(q^2-1),
X1 = a*p*(p-2) - b*q*(q-2) - p*(p-2).
```

If `X0` or `X1` is nonzero on the collision-free `e`-open, the two bordered
Schur residuals with targets `(25,5)` and `(31,5)` vanish.  After the exact
`p=N/D` substitution they are, up to nonzero displayed scalar denominators,

```text
F25 = 2*D^2*a - 9*t*(t-1)*b
      + (t-2)*(t+1)*(2*t-1)^2*c
      - 2*t^4+4*t^3-6*t^2+4*t-2,

F31 = 2*D*(t^4-8*t^3+6*t^2+4*t-2)*a
      + 9*t*(t-1)*(t^2+2*t-2)*b
      + (-4*t^6+27*t^4-17*t^3-18*t^2+18*t-4)*c
      - 4*t^6+12*t^5+6*t^4-8*t^3-24*t^2+24*t-4.
```

The exact coefficient eliminations are

```text
A31_b*F25 - A25_b*F31
 = 54*t^2*(t-2)*(t-1)^2*(t+1)*(D*a-(t^2-1)),

A31_a*F25 - A25_a*F31
 = 6*t*(t-2)*(t-1)*(t+1)*D*
   (-9*t^2*b+9*t*b
    +(t-2)*(t+1)*(2t-1)^2*c+2*t^4-12*t^2+8*t).
```

Consequently the entire one-pivot rank-six family is forced to

```text
a = (t^2-1)/D,
b = (t-2)*((t+1)*(2t-1)^2*c + 2*t*(t^2+2*t-2))/(9*t*(t-1)),
```

with `c` free.  On this family the vector

```text
K(t) = (-2*D^3, 27*t*(t-1), (t-2)*(t+1)*(2t-1)^4)^T
```

is killed by each of the three 37-by-3 leaf blocks of `M(G)`.  A direct
block minor is

```text
det M_e[(1,17),(0,1)]
 = (t-2)*(t+1)*(2t-1)^2*(t^2-t+1)/D^2,
```

so on the collision-free open the syndrome rank is exactly six.  The complete
kernel is the direct sum of the three block-supported `K(t)` lines.  Every
compatible centre therefore has proportional rows and determinant zero.
The third coordinate of `K` is nonzero there, so `C_8=1` is attainable and the
unsaturated low-rank family is genuinely nonempty.

If `X0=X1=0`, the exact solution is

```text
a = (t+1)*(2t^2-5t+5)/9,
b = -(t-2)*(t^2+2t-2)*(2t^2+t+2)/(3*D^2).
```

On the auxiliary row charts

```text
RA = (0,1,2,17,19,25),
RB = (0,1,17,19,25,28),
```

the specialized raw pivots are

```text
pivot_A = -8*(t-2)^3*(t-1)*(t+1)^5*(2t-1)^4
          *(t^2-4t+1)*(t^2-t+1)^7*(2t^2-5t+5)/D^10,

pivot_B =  8*t*(t-2)^5*(t+1)^3*(2t-1)^4
          *(t^2-t+1)^7*(t^2+2t-2)*(2t^2+t+2)/D^10.
```

Their numerator gcd is, up to a nonzero rational unit,
`(t-2)^3*(t+1)^3*(2t-1)^4*(t^2-t+1)^7`; hence at least one auxiliary chart
is active on the collision-free open.  Its two exact bordered residuals have
resultant respectively

```text
-6*L1*T*L2*R,              and
-6*p*q*(p-2)*(q-2)*(p+q)*L1*L2*R,
```

where `R` is the GLD90 residual curve.  Since the active chart makes the
remaining prefactor a unit, rank at most six would force `R=0`.  But

```text
R|_{e=0} = -6*t*(t-2)*(t-1)*(t+1)*(t^2-t+1)^2/D^2,
```

which is nonzero on the collision-free open.  This excludes the simultaneous
raw-pivot branch without dividing through an auxiliary pivot boundary.

## Exact sample and status boundary

At `t=3`, `c=0`, the forced family is

```text
(p,q,a,b,c) = (13/11, 3, 8/11, 13/9, 0),
det(G) = 24/11,
rank(M) = rank(M[:,0:8]) = 6,
K = (-2662,162,2500).
```

This is an exact characteristic-zero unsaturated leaf sample.  Its compatible
scale-fixed centre is singular because every centre row is proportional to
`K`; it is consequently outside `D(Omega)`.  More generally the forced leaf
family has

```text
det(G) = 2*(t-2)*(t+1)*((2t-1)c+t)/D,
```

so the leaf frame open is not empty even though the centre frame is excluded.

The primary verifier reconstructs all 37 syndrome rows and checks every
displayed identity exactly.  The independent audit contracts a separately
transcribed nine-row subset containing every row used in the pivots,
resultants, and sample; it does not claim an independent reconstruction of
the complete 37-row kernel identity.  The upstream dependencies are GLD71,
GLD75/GLD86, GLD87, GLD89, and GLD90.  The GLD83 intrinsic Fitting pullback,
its rank-drop boundaries, other H4 boundaries/charts, other survivor
components and ranks, source branches, and the global conjecture remain open.

## Reproduction

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_e_boundary_determinant_safety.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_e_boundary_determinant_safety.py
```
