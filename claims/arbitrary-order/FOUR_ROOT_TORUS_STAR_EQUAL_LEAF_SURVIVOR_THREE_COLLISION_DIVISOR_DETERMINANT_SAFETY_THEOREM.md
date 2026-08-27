# Four-root torus-star equal-leaf survivor three-collision-divisor determinant safety

## Status

**Exact scoped divisor theorem (`GLD87`).** Work over `Q` for the displayed
actual leaf frame and extend scalars to `C`. On the complete scale-fixed,
equal-leaf chart of `GLD83`--`GLD86`, every incidence point with
`rank(A_lin)<=6` (equivalently, on `B`, with first-eight syndrome-column rank
at most six) on any of the three pair-collision divisors

```text
H_1=p-q,       H_2=p-s,       H_3=q-s
```

has singular center matrix `C`. Consequently, on the determinant-safe part
where `det(G) det(C) != 0`, the rank-at-most-six branch is disjoint from
`H_1 union H_2 union H_3`. The proof is exact in characteristic zero and
uses no genericity or numerical sampling.

The `H_4` divisor

```text
H_4=pq+ps+qs-p-q-s
```

is **not** covered by this theorem and remains open. `GLD87` does not compute
the pulled-back `GLD83` Fitting ideal by itself. The global Krenn--Gu
conjecture remains **UNRESOLVED**.

This theorem is a divisor-safety result, not a claim that the raw
three-divisor intersections are empty before the center determinant gate.
Indeed, the proof exhibits a characteristic-zero H1 residual with
`rank(M)=6` whose entire center kernel consists of singular centers.

The owning upstream facts are the exact `GLD71` syndrome map, the `GLD75`
bidirectional equal-leaf certificate, the `GLD83` definition of `Omega`, and
the `GLD84` center-linear matrix. `GLD86` supplies the already-proved bridge
from rank-at-most-six in the center-linear system to the four named divisor
union.

## 1. Chart, notation, and the incidence bridge

Use the complete scale-fixed equal-leaf chart

```text
B=Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8),    K=Q(i),
```

with the ten pinned `GLD75` basis equations. The chart writes the common
leaf frame as

```text
G_shift = [1  1       1      ]
          [p  q       s      ],       s=1+i+r,
          [a  1+b     1+c    ],
```

where `b,c` in this display are shift coordinates. For the calculation
below, `a,b,c` are instead the **actual** third-row entries of the leaf
frame:

```text
G = [1  1  1]
    [p  q  s]
    [a  b  c].                                      (1)
```

Thus the actual variables are related by `b_actual=1+b_shift` and
`c_actual=1+c_shift`; this is only a translation of coordinates. Let `C` be
the actual `3 x 3` center matrix, flattened root-major. On `x_8=0`, its last
coordinate is the exact scale-fixed unit

```text
C_8=1.                                               (2)
```

For the fixed `GLD71` annihilator basis, let `M(G)` be the `37 x 9` syndrome
matrix, so the equal-leaf incidence equations are `M(G) C=0`. The exact
`GLD75` bidirectional certificate gives, on `B`,

```text
B=0  iff  M(G) C=0.                                  (3)
```

Differentiating both directions of that certificate in the eight center
shift variables (the terms containing a vanishing equation vector drop out)
gives the `GLD86` rank bridge

```text
rank A_lin(z) = rank M(G)[:,0:8]                      (4)
```

at every point of `B`, where `A_lin(z)` is the `10 x 8` center coefficient
matrix of `GLD84`. Therefore a point of `B` in `V(I_7(A_lin))` has
`rank M(G)[:,0:8] <= 6`, and hence every row submatrix of `M(G)` has rank at
most six as well.

The determinant-safe locus used below is the one on which

```text
det(G) det(C) != 0.                                   (5)
```

On the normalized chart, `GLD83`'s frame/gauge open has
`Omega=delta_gauge det(C) det(G)^3`; hence `D(Omega)` is contained in the
determinant-safe locus (with the displayed gauge convention). The proof is
written with (5) explicitly so it does not hide an open-condition assumption.

## 2. H1: exact collision calculation

Assume `H_1=0`, so `q=p`. Select the following eleven rows of the full
syndrome map and call the resulting `11 x 9` matrix `M_hat`:

```text
R_hat=(0,1,2,17,19,25,28,31,32,33,34).
```

At a point of `B` in the rank-at-most-six branch, (3) and `C_8=1` give the
exact column relation

```text
M(G)[:,8] = -sum_(j=0)^7 C_j M(G)[:,j].
```

Thus the selected row matrix has `rank(M_hat)<=6` whenever the first-eight
syndrome columns (equivalently `A_lin`) have rank at most six. This is the
point at which the scale-fixed unit is used; the H1 calculation below does
not silently replace a first-eight rank bound by a full nine-column rank
bound.

Apply the same unimodular change in each center block,

```text
T_0 = [ 1  0  0 ]       T=diag(T_0,T_0,T_0),       det(T_0)=1,
      [-1  1  0 ]
      [ 0  0  1 ],
```

and put `X=M_hat T` after substituting `q=p`. The three difference columns
are `(0,3,6)` and the six base columns are `(1,2,4,5,7,8)`. On the base rows
`(0,1,3,4,9)`, the difference columns vanish, and the base block is exactly

```text
B_0 = [ 0                 0                 p^3                 s^3                 0                    0                   ]
       [ 1                 1                 0                   0                   0                    0                   ]
       [ p^2-p             s^2-s             -2p^2+2p-1          -2s^2+2s-1          0                    0                   ]
       [ p^3-2p^2+2p       s^3-2s^2+2s       p^2-p               s^2-s               0                    0                   ]
       [ 0                 0                 12p^2-12p+4         12s^2-12s+4         -12p^2+12p           -12s^2+12s          ].  (6)
```

There are exactly `37` nonzero `4 x 4` minors of `B_0`. Each is divisible
by `p-s`. Exact division and a lexicographic Groebner calculation over
`Q[p,s]` give

```text
< (4-minor)/(p-s) >
  = < p-2s^3+3s^2-2s,
      s(s-1)(s^2-s+1) >.                              (7)
```

This is a calculation in the polynomial ring, not a sampled factor check.
If `p != s` and `rank(B_0)<4`, (7) leaves only

```text
p=1-s,       s^2-s+1=0.                                (8)
```

Indeed, the alternatives `s=0,p=0` and `s=1,p=1` contradict `p != s`.

The six difference rows are `(2,5,6,7,8,10)`. After factoring the common
`a-b`, their `6 x 3` difference block is

```text
Delta(p) = [ 0                         0                         -(p^2-1)                 ]
           [ 0                         2p-1                      1-2p                    ]
           [ p(p-2)                    0                         -p(p-2)                 ]
           [ 0                         6(p^2+2p-2)               0                       ]
           [ 6(2p^2-2p-1)              0                         0                       ]
           [ 0                         12(2p-1)                  12p(p-2)                ]. (9)
```

Three of its `3 x 3` minors are

```text
p(p-2)(p-1)(p+1)(2p-1),
6(p-1)(p+1)(2p-1)(2p^2-2p-1),
36p(p-2)(p^2+2p-2)(2p^2-2p-1),                         (10)
```

whose gcd in `Q[p]` is `1`. Thus `rank(Delta)=3` at every characteristic-zero
value of `p`. Since `det(G)=(p-s)(b-a)` under `q=p`, (5) gives
`p != s` and `a != b`. If `B_0` had rank at least four, a block-triangular
`7 x 7` minor using four base columns and three difference columns would be
nonzero by (6) and (9). Therefore a rank-at-most-six point must satisfy (8).

### 2.1 The only H1 residual is center-singular

Reduce coefficients modulo `s^2-s+1` after substituting `p=1-s`. On rows
`(0,1,9,2,5,6,8)` and columns `(1,2,4,7,0,3,6)`, the exact transformed
`7 x 7` determinant is

```text
det X_(rows,columns) = -648(a-b)^3 (c s+c-s)                         (11)
```

in that quotient. A rank-at-most-six point makes (11) zero. The factors
`a-b` and `s+1` are nonzero on (5) and `s^2-s+1=0`, respectively, so

```text
c = s/(s+1) = (s+1)/3.                                (12)
```

On rows `(0,1,2,5,6,7)` and columns `(0,1,3,4,6,7)`, the corresponding exact
`6 x 6` determinant is

```text
36(a-b)^3(2s-1),                                      (13)
```

which is nonzero in characteristic zero under `s^2-s+1=0` and `a != b`.
Finally, with (8) and (12), every one of the three `11 x 3` root blocks of
`X` annihilates

```text
w=(3b+s-2, -3(a-b), 3(a-b))^T.                        (14)
```

The three block-supported copies of `w` are independent. Equation (13)
therefore proves `rank(X)=6`, and (14) is the complete three-dimensional
kernel of `X`. Since `T` is blockwise invertible, the kernel of `M_hat` is
obtained by applying `T_0` to each block. Consequently every kernel vector,
when reshaped as a `3 x 3` center matrix, has three proportional rows and

```text
det(C)=0.                                              (15)
```

This proves the H1 statement: no point satisfying `H_1=0`, `det(G)!=0`, and
`rank M(G)[:,0:8] <= 6` can have an invertible center. Notice that only the
selected row submatrix was used; no unproved claim that the eleven rows span
all thirty-seven syndrome rows is needed.

## 3. H2 and H3 by exact leaf-column equivariance

For a permutation `P` of the three leaf columns, let
`P_blk=diag(P,P,P)` act on the root-major center columns. Direct symbolic
coefficient comparison in the fixed `GLD71` basis gives the exact identity

```text
M(GP) = M(G) P_blk.                                    (16)
```

The primary verifier checks (16) for the two transpositions `(2 3)` and
`(1 3)`; these suffice to move `H_1` to the other two pair-collision
divisors. If `M(G)C=0`, then the corresponding frame `GP` has solution
`P_blk^{-1}C`. Its determinant differs from `det(C)` by the unit
`det(P)^{-1}=+-1`, and `det(GP)=det(G)det(P)`. Rank is unchanged.

The transposition `(2 3)` maps `p=q` to `p=s`, namely `H_2=0`; the
transposition `(1 3)` maps `p=q` to `q=s`, namely `H_3=0`. The original
point has `C_8=1`, so its full nine-column syndrome matrix has rank at most
six by the column relation above. The transported matrix has the same full
rank, even though the permuted center need not have its *new* final entry
equal to one. Since the H1 calculation only used the full selected-row rank
bound after the column relation, (15) transfers verbatim to both H2 and H3.

## 4. Scoped consequence for the low-rank and Omega branches

Let `I_7(A_lin)` be the seven-minor ideal of the `GLD84` center coefficient
matrix. Combining (3)--(4) with the H1--H3 result gives the exact
determinant-safe exclusion

```text
B intersect V(I_7(A_lin)) intersect D(det(G)det(C))
       intersect V(H_1 H_2 H_3) = empty.                (17)
```

`GLD86` already proves, without any determinant gate beyond its stated chart
scope, the four-divisor containment

```text
B intersect V(I_7(A_lin))
       subseteq B intersect V(H_1 H_2 H_3 H_4).          (18)
```

Because `D(Omega)` lies in `D(det(G)det(C))` on this normalized frame/gauge,
(17)--(18) sharpen the retained branch to

```text
B intersect V(I_7(A_lin)) intersect D(Omega)
       subseteq B intersect V(H_4) intersect D(Omega).   (19)
```

Equation (19) is the useful downstream handoff: the three linear collision
divisors are excluded on the actual retained determinant-safe open, while
the nonlinear H4 divisor remains the sole named low-rank candidate in this
chart. This is not an assertion that the H4 intersection is empty, nor a
calculation of the `GLD83` pulled-back Fitting ideal.

The theorem makes no claim about H4, other survivor components or gauges,
unequal leaves, other support profiles, triangles, other roots, off-chart
source branches, or the global conjecture. Those obligations remain open.

## 5. Verification and audit

From repository root:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_three_collision_divisor_determinant_safety.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_three_collision_divisor_determinant_safety.py
```

The primary verifier replays the upstream GLD86 check, reconstructs the
actual `GLD71` syndrome map, verifies the transformed matrices, all `37`
base-minor divisions and their exact Groebner basis, the difference-minor
gcd, the two exceptional determinants, the complete exceptional kernel, and
both leaf-column covariance identities. The no-import audit uses a separate
standard-library sparse polynomial implementation over `Q`; it rederives the
same base/difference matrices and independently expands the exceptional
determinants and kernel identities. Neither script computes a pulled-back
Fitting ideal or changes the global status.
