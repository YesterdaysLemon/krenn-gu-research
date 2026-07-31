# The common-kernel `YX` triangle acquires a second relation

## Status

**Exact symbolic obstruction over `C`.**  Consider a rank-three exceptional
triangle with relation-rank pattern `(2,1,1)` and common-kernel Borel
orientation

```text
y_1y_3=0,
x_2y_3=0,
y_1x_2-x_1y_2=0.                                  (1)
```

If the common zero-divisor pair has genuine two-coordinate support, then the
pair image on edge `12` has rank at most two, contradicting the assumed
rank-three edge.  Thus the mixed kernel/active leaf orientation is empty,
including its complementary support-one boundary.

This is a theorem for the indicated orientation and support-two exact-pair
stratum.  The common-kernel `XX` orientation, support-one common zero
divisors, lower pair-image ranks, component exhaustiveness, and the global
Krenn--Gu conjecture remain outside it.

## Synchronization becomes a factorization of a square

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Normalize the common exact pair to

```text
a=X_0+X_1,             c=X_0-X_1,             ac=0. (2)
```

The two rank-one relations in (1) then force

```text
y_1=x_2=a,             y_3=c.                       (3)
```

Put `b=x_1` and `d=y_2`.  The rank-two relation is precisely

```text
b d=a^2=2X_0X_1.                                    (4)
```

Write

```text
b=b_0X_0+b_1X_1+s_2X_2+s_3X_3,
d=d_0X_0+d_1X_1+t_2X_2+t_3X_3                     (5)
```

and set

```text
Delta=b_0d_1-b_1d_0.                                (6)
```

The six coefficients of (4) give

```text
b_0d_1+b_1d_0=2,
b_0t_j+d_0s_j=0,
b_1t_j+d_1s_j=0              (j=2,3),
s_2t_3+s_3t_2=0.                                  (7)
```

## A two-branch symmetric completion

Taking the two-by-two minors of the middle equations in (7) gives

```text
Delta*s_j=Delta*t_j=0             (j=2,3).          (8)
```

If `Delta!=0`, all four complementary coefficients vanish.  Then both
planes on edge `12` lie in `span(X_0,X_1)`, so their entire product image is
the line `C X_0X_1`.  Its rank is one, not three.

Suppose `Delta=0`.  The first equation in (7) then implies

```text
b_0d_1=b_1d_0=1.                                    (9)
```

In particular all four binary coefficients are nonzero and there is a
nonzero scalar `lambda` with

```text
d_0=lambda*b_0,       d_1=lambda*b_1,
t_j=-lambda*s_j.                                    (10)
```

Put `B=b_0X_0+b_1X_1` and `s=s_2X_2+s_3X_3`.  Equations (4) and (10) become

```text
b=B+s,       d=lambda*(B-s),
lambda*b_0*b_1=1,       s^2=0.                     (11)
```

The last equation says `s_2s_3=0`: the complementary direction has support
on at most one coordinate.  More importantly, all four products on edge
`12` lie in

```text
span(a^2,a*s).                                      (12)
```

Indeed `aB=((b_0+b_1)/2)a^2`, and besides the relation (4) there is the
second exact relation

```text
lambda^(-1) a d+a b-(b_0+b_1)a^2=0.                (13)
```

Hence the pair image has rank at most two.  This contradicts the unique-
relation, rank-three hypothesis in both branches.

## Across the mathematical fence

Equation (4) is not best viewed as a generic system of six quadrics.  Its
off-diagonal coefficients form a symmetric rank-two matrix completion with
only the edge `01` prescribed.  The determinant `Delta` separates a rigid
binary completion from a reflection factorization `B+s`, `B-s`.  In the
squarefree algebra the reflected direction must satisfy `s^2=0`, so it lands
on a coordinate ray and creates the extra relation (13).

Equivalently, this is the degree-one factorization scheme of `a^2` in an
Artinian complete intersection.  The neighboring homological language of
exact homogeneous zero divisors is developed by Kustin--Striuli--Vraciu
([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)); the specific reflection
dichotomy (8)--(13) and its graph-theoretic consequence are new to this
problem.

## Verification

Run:

```text
uv run --with sympy python verify_p4_common_kernel_yx_211_factorisation_obstruction.py
python audit_p4_common_kernel_yx_211_factorisation_obstruction.py
```

The primary verifier checks every coefficient identity, the determinant
dichotomy, and the second relation symbolically.  The independent audit uses
a different source order and exact rational representatives of the rigid
and two reflected coordinate branches.  Both are fixed-size replays, not
searches.
