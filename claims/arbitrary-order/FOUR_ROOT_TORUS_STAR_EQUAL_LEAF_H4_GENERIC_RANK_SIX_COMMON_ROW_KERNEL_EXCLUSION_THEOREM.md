# Four-root torus-star equal-leaf H4 rank-six principal-open common-row-kernel exclusion

## Status

**Exact scoped characteristic-zero principal-open exclusion (`GLD88`).**
Work over `Q` and then extend scalars to `C`.  On the fourth divisor of
`GLD86`, two exact bordered Schur residuals classify every syndrome-rank-at-
most-six point on a named six-pivot and linear-coefficient open.  They force
an explicit rational three-parameter family whose complete center kernel has
three proportional rows.  Every compatible center is therefore singular, so
that principal-open part of the `H4` low-rank branch is disjoint from the
`GLD83` frame open `D(Omega)`.

This is **not** a classification of the whole `H4` divisor.  The named pivot,
linear-coefficient, and parameter-denominator boundaries remain open, as do
possible lower-rank subloci there.  The theorem does not compute the pulled-
back `GLD83` Fitting ideal.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. The `H4` parameter chart and forced family

Use the `GLD86` equal-leaf frame notation

```text
G = [1  1    1  ]
    [p  q    s  ]
    [a  1+b  1+c].
```

Put

```text
d0 = p+q-1,
e  = 2*p*q^2-2*p*q-p-q^2-2*q+2,
s  = (p+q-p*q)/d0.                                      (1)
```

Then

```text
p*q+p*s+q*s-p-q-s = 0,                                  (2)
```

so the family lies on the fourth `GLD86` divisor `H4`.  Define

```text
Nb = -2*a*p^2*q^3+3*a*p^2*q^2-3*a*p^2*q+a*p^2
     +2*a*p*q^3+2*a*p+a*q^3-3*a*q^2+3*a*q-2*a
     +p^3*q^2-p^3+p^2*q^3-3*p^2*q^2+p^2
     -2*p*q^3+3*p*q^2-2*p+q^2-3*q+2,

Nc = 2*a*p*q^3-3*a*p*q^2+3*a*p*q-a*p
     -a*q^3+3*a*q^2-3*a*q+2*a
     +p^2*q^2-2*p^2*q-3*p*q^2+p*q+p-q^2+3*q-2,

b = -Nb / ((p^2-p+1)*e),
c = -Nc / (d0*e).                                       (3)
```

Finally put

```text
dk = (p-q)*d0^3,
u  = (q^2-q+1)*(2*p*q-p+q^2-2*q) / dk,
v  = -(p^2-p+1)*(p^2+2*p*q-2*p-q) / dk,
k  = (u,v,1).                                            (4)
```

These formulas initially describe the candidate forced family.  The exact
classification in Section 2 shows that they are not an ansatz: every low-rank
point on the declared principal open must have these values of `b,c`.

All statements below are on the principal open where the displayed
denominators, `det G`, the linear determinant `Delta_lin`, and the six-minor
`P6` in Section 2 are nonzero.  Every excluded factor remains an explicit
successor obligation.

The leaf determinant factors exactly as

```text
det G = -(p-q)*(-3*a+p+1)
          *(p^2+2*p*q-2*p-q)*(2*p*q-p+q^2-2*q)
        / ((p+q-1)*(p^2-p+1)*e).                        (5)
```

Thus `det G` is not identically zero on the family.

## 2. Two linear Schur residuals classify the named open

Before imposing (3), retain `b,c` as free leaf shifts in `G` and form the
fixed `37 x 9` `GLD71` syndrome matrix `M(G)`.  Select

```text
R6=(0,1,2,17,19,32),
S6=(0,1,3,4,6,7),
P6=det M(G)_(R6,S6).                                   (6)
```

Use the two bordered positions

```text
(row,column)=(25,5), (31,5).                          (7)
```

On `D(P6)`, their determinants divided by `P6` are Schur residuals.  After
clearing their displayed denominators, both numerators are linear in `b,c`.
Their `2 x 2` coefficient determinant factors exactly as

```text
Delta_lin = -6 (p-q)(p+q-1)(p^2-p+1)
               (p^2+2pq-2p-q)(2pq-p+q^2-2q)
               (2pq^2-2pq-p-q^2-2q+2).               (8)
```

Solving this exact two-equation linear system on `D(Delta_lin)` gives
precisely the two formulas (3).  There is no function-field or hidden
genericity step: (8) names the full coefficient determinant being inverted.

At an incidence point on the scale-fixed base, `C_8=1`.  Thus
`M(G)C=0` expresses syndrome column eight as a combination of the first
eight.  The `GLD86` differentiated certificate identifies the rank of those
first eight columns with the `GLD84` center coefficient matrix.  Consequently
a point of `B intersect V(I_7(A))` has full syndrome rank at most six.  On
`D(P6)`, its two bordered determinants vanish; on `D(Delta_lin)` this forces
(3).  Therefore the displayed rational family exhausts the low-rank branch
on this named principal open.

## 3. Exact rank and kernel on the forced family

Let `M(G)` be the fixed `37 x 9` `GLD71` syndrome matrix used by `GLD86`,
with its columns grouped into the three root blocks

```text
M(G) = [M_0 | M_1 | M_2],       M_r in Mat_(37 x 3).    (9)
```

Direct exact substitution gives the `111` rational identities

```text
M_0 k^T = 0,       M_1 k^T = 0,       M_2 k^T = 0.     (10)
```

Consequently the three row-supported vectors

```text
(k,0,0),       (0,k,0),       (0,0,k)                 (11)
```

are independent elements of `ker M(G)`, and `rank M(G)<=6`.

After (1)--(3), the numerator of the `P6` from (6) is a nonzero `176`-term polynomial in
`Q[p,q,a]`, canonically hashed by the primary verifier as

```text
656128e97aa9b6e08ba57532aad1e8762eb201217cba15be58865e187214d5b5.
```

Hence on `D(P6)`, `rank M(G)>=6`.  Combining this with (7) gives

```text
rank M(G)=6,
ker M(G)=span{(k,0,0),(0,k,0),(0,0,k)}.                (12)
```

## 4. Center singularity and exclusion from `D(Omega)`

Read an actual center frame `C` row-major.  The equal-leaf incidence equation
is

```text
M(G) vec(C)=0.                                         (13)
```

By (10), every compatible center has the form

```text
C = [lambda_0*k]
    [lambda_1*k]
    [lambda_2*k].                                      (14)
```

All three rows are proportional, so

```text
rank C<=1,        det C=0.                             (15)
```

In the scale-fixed chart `C_8=1` and `k_2=1`, so (12) merely fixes
`lambda_2=1`; it does not change (13).  Since the `GLD83` open factor contains

```text
det(C)*det(G)^3,
```

the complete displayed rank-six family is disjoint from `D(Omega)`.

The independently reconstructed `GLD75` ten-generator basis gives the same
conclusion in center-shift coordinates: its coefficient matrix has rank six
on a separately pinned six-minor open, and the two-parameter scale-fixed
version of (12) is the complete affine solution there.

## 5. Nonempty exact control and scope fences

At

```text
(p,q,a)=(0,3,0),
(s,b,c)=(3/2,2/13,-1/13),
k=(-7/8,-1/8,1),
```

exact arithmetic gives

```text
det G=27/26,
P6=291600/13,
rank M(G)=6,
rank M_r=2 for r=0,1,2.                                (16)
```

At this point `Delta_lin` is also nonzero, so the declared principal open is
nonempty.  This control also explains why
finite-field and rational searches repeatedly found legal leaf frames of
syndrome rank six without finding an invertible center.

What remains open includes:

- every point of `H4` on the parameter, `Delta_lin`, or `P6` boundaries;
- possible lower-rank subloci where the kernel is larger than (11);
- the `GLD83` Fitting pullback on the surviving `H4` strata;
- other survivor components/gauges, source branches, triangles, other roots
  and orders, and the global conjecture.

## Replay

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py
```

The primary reconstructs the fixed `GLD71` syndrome map, proves the two exact
linear Schur residuals and (8), solves them as (3), and checks all `111`
kernel identities symbolically.  The independent audit imports no repository
Python module: it parses the immutable `GLD75` sparse ten-generator carrier,
works in center-shift coordinates, and checks that the forced family has the
complete proportional-row affine center solution on its own rank-six pivot
open.  It does not claim a second derivation of the two-residual classifier;
that independence limitation is retained explicitly.
