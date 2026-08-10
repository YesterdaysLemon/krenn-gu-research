# The universal mixed kernel and a dense rank-drop chart

## Status

This is an exact characteristic-zero support theorem on the elliptic
normalization of the diagonal-quadric component.  It refines the generic
marked-fibre obstruction by locating the possible extra mixed-kernel
directions for the two middle distinguished source coordinates.

On an explicit dense pivot chart, every such rank drop is forced either
onto

```text
x=1
```

with exactly the marking already treated by the complete `H=0` theorem,
or onto one of the already-treated pure-direction curves

```text
x=1+r,  x=1-r.
```

This theorem by itself is not a classification of the full survivor
divisor.  Its pivot-complement strata and both end coordinates have
since been closed by companion exact theorems.  Thus no regular
elliptic-chart marking remains.  The compactification boundary,
possible further pure components, and the `H22` frontier remain open.

## Elliptic normalization

Use the normalized diagonal-quadric variables

```text
D=x+r^2-1,
f=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2],
Y^2=f.                                                   (1)
```

The inverse map is

```text
H=(1-x)/r,  C=rx/D,  E=Y/(rx).                          (2)
```

Clear the harmless row denominators and use

```text
alpha0=(Y+r^2x,-rx-r^2x,-rx+r^2x,-Y+r^2x),
alpha1=(1,0,0,-1),
alpha2=(0,1,-1,0),
alpha3=(r,-1,-1,r),

beta0=(1,-1,1,1),
beta1=(D,rx+D,rx-D,D),
beta2=(x(1-x)+Y,rx,rx,x(1-x)-Y),
beta3=(0,1,1,0).                                       (3)
```

Every marking is `beta_i(t)=beta_i+t_i alpha_i`.

## A marking-independent kernel line

For a distinguished old source coordinate `q`, let `M_q(t)` be the
`14 x 8` matrix of mixed binary-extension coefficients.  Its columns
are ordered

```text
(a0,a1,a2,a3,b0,b1,b2,b3).
```

At `t=0`, the following vectors lie in the mixed kernels:

```text
q=1:
(-rx(r+1),0, 1,-1, -1,(r+1)(r+x-1),rx,1),

q=2:
( rx(r-1),0,-1,-1,  1,(r-1)(x-1-r),rx,1).             (4)
```

Under a marking, replace each last component by

```text
b_i -> b_i+t_i a_i.                                    (5)
```

The resulting vector `k_q(t)` satisfies

```text
M_q(t) k_q(t)=0
```

modulo (1).  Its two binary diagonal values are

```text
d_alpha,q k_q(t)=0,
d_beta,q  k_q(t)=-4rx(x-1-r)(x-1+r).                  (6)
```

Thus, wherever the mixed rank is seven, the kernel is this line and no
genuine binary extension can have both diagonal coefficients nonzero.
A binary survivor can occur only after the mixed rank drops to at most
six.

## Quotient pivot

The `a2` component in (4) is a unit.  Delete that column from `M_q(t)`
and call the resulting `14 x 7` matrix `N_q(t)`.  Select rows

```text
1,2,3,8,9,11
```

and columns

```text
0,2,3,4,5,6
```

of `N_q`.  Put

```text
Q=-r^4+r^2x^2-3r^2x+2r^2-x^2+2x-1=-f/x=-Y^2/x.
```

For both `q=1,2`, the selected `6 x 6` determinant is

```text
-64 r^2 t0 x^2 (t3-1)(r^2x-t2) D Q^2.                (7)
```

Work on the open set

```text
r x Y D (r^2-1)(x-1-r)(x-1+r)
  t0(t3-1)(r^2x-t2) != 0.                             (8)
```

Here (7) has rank six.  Rank at most six is therefore equivalent to
the vanishing of every bordered `7 x 7` minor.

The border by row zero first gives `t3=0`.  With `t3=0`, the borders
by rows ten and seven give the following two branches:

```text
q=1, branch I:   t2= rx,       t0=-1/(xD),
q=1, branch II:  t2=x(1-x),    t0=-1/[r(r-1)x],

q=2, branch I:   t2=-rx,       t0=-1/(xD),
q=2, branch II:  t2=x(1-x),    t0=-1/[r(r+1)x].       (9)
```

## Compatibility of the remaining borders

All factors suppressed below are units on (8).  Eliminating `t1`
between the borders by rows six and thirteen gives

```text
q=1, branch I:
  (x-1)(x-1-r)^2=0,

q=2, branch I:
  (x-1)(x-1+r)^2=0.                                  (10)
```

The pure-direction factors are excluded on (8) and were already
closed separately.  Hence branch I forces `x=1`.  The row-thirteen
border then reduces to a unit times

```text
Y-t1,
```

so

```text
x=1, t0=-1/r^2, t1=Y, t2=+r, t3=0   for q=1,
x=1, t0=-1/r^2, t1=Y, t2=-r, t3=0   for q=2.         (11)
```

These are exactly the two uniform survivor markings on the `H=0`
ruling, expressed in the denominator-cleared basis (3).  The complete
`H=0` marked-fibre theorem proves that every genuine binary direction
there is ternarily obstructed.

On branch II, the row-six/row-thirteen compatibility forces

```text
x-1-r=0  for q=1,
x-1+r=0  for q=2.                                    (12)
```

The row-five/row-six compatibility simultaneously forces

```text
(x-1)(x+1+r)=0  for q=1,
(x-1)(x+1-r)=0  for q=2.                             (13)
```

Together, (12)--(13) imply `r=-1` for `q=1` or `r=1` for
`q=2`, apart from `r=0`.  All are excluded by (8), and the `r=+/-1`
fibres have already been closed by the factorized-fibre theorem.
Thus branch II is empty on the pivot chart.

Consequently, for `q=1,2`, every possible binary survivor on (8) is
forced onto the already-closed `H=0` marked fibre.  No new survivor
curve occurs there.

## Companion closure of the pivot complement

The complement of (8) contains the pivot exceptions

```text
t0=0,  t3=1,  r^2x=t2,  Y=0,
x=0,  D=0,  r=0,
```

together with singular base fibres and pure-direction loci.  This
theorem does not claim to close them by the displayed pivot alone.
They are now treated as follows:

- the complete regular middle-coordinate complement, including all
  three marking divisors and the regular `Y=0` slice, is closed in
  [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md`](../elliptic-middle-coordinate-pivot-complement/P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md);
- the complete regular end-coordinate locus is closed in
  [`P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md`](../elliptic-end-t2-divisor/P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md)
  and
  [`P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md`](../elliptic-end-t3-divisor/P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md).

Only the birational/compactification boundary and possible further
pure-compression components remain for `H31`.

## Verification

Run:

```text
python claims/p5/h31/elliptic-middle-coordinate-rank-drop/verify_p5_h31_elliptic_middle_coordinate_rank_drop.py
python claims/p5/h31/elliptic-middle-coordinate-rank-drop/audit_p5_h31_elliptic_middle_coordinate_rank_drop.py
```

The primary verifier constructs permanents by direct permutation
expansion.  It checks the universal kernels, both diagonal evaluations,
the pivot and short border determinants, both branch substitutions,
the four linear compatibility determinants, and the reduction to
`t1=Y`.

The independent audit rebuilds the coefficient systems using a
subset-dynamic-programming permanent and checks the same identities
without importing the primary verifier.
