# Nonresonant rank-two relation triangles reduce to cyclic cuts

## Status

This is an exact characteristic-zero reduction for the unresolved
triangle stratum of the pure `P_4` compression problem.  It is
symbolic: the proof uses a three-equation holonomy calculation and a
rank-two symmetric-matrix lemma, with no elimination or component
search.

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Let `U_1,U_2,U_3` be local two-planes in a nonzero pure restriction of
`P_4`.  Choose bases

```text
U_i=span(y_i,x_i),
```

where `y_i` is the kernel row of the pure factor and `x_i` is an
active row.  Suppose all three triangle pair images have rank three
and their unique multiplication relations have coefficient-matrix
rank two.

Then the relation on edge `ij` has the form

```text
a_ij y_i y_j+b_ij y_i x_j+c_ij x_i y_j=0,          (1)
```

with `b_ij c_ij != 0`.  Define

```text
Omega =
 c_12 b_13 c_23+b_12 c_13 b_23.                   (2)
```

The vanishing or nonvanishing of `Omega` is independent of all
allowed changes of the chosen active complements and row scalings.

On the nonresonant stratum

```text
Omega != 0,                                        (3)
```

the following conclusions hold.

1. The active complements can be shifted by the kernel rows so that

   ```text
   a_12=a_13=a_23=0.                               (4)
   ```

2. All six mixed triple products vanish:

   ```text
   x_1 y_2 y_3 = y_1 x_2 y_3 = y_1 y_2 x_3 = 0,
   y_1 x_2 x_3 = x_1 y_2 x_3 = x_1 x_2 y_3 = 0.   (5)
   ```

3. Put

   ```text
   Q_ij=b_ij y_i x_j=-c_ij x_i y_j.                (6)
   ```

   Each `Q_ij` is nonzero, and the opposite local plane is its full
   degree-one annihilator:

   ```text
   U_1=Ann_R1(Q_23),
   U_2=Ann_R1(Q_13),
   U_3=Ann_R1(Q_12).                                (7)
   ```

4. Every bridge `Q_ij` is a cut form of one of two types:

   - `1+3`: it is supported on the three edges inside a
     three-coordinate block;
   - `2+2`: across a partition `{p,q}|{r,s}`, it has the form

     ```text
     (alpha_p X_p+alpha_q X_q)
     (beta_r X_r+beta_s X_s).                       (8)
     ```

Thus the nonresonant all-rank-two-relation triangle is not a free
system of plane coefficients.  It is a cyclic compatibility problem
for three discrete `1+3`/`2+2` cuts and their rank-one weights.

The full-support case in which all three bridges have type `1+3` has
since been excluded in
[`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md).
The factorization sheets force all three singleton labels to agree,
which suspends a pure `P_3` restriction and drops every triangle pair
rank to at most two.  A companion hyperbolic-block theorem excludes
every full-support cycle containing a `2+2` bridge:
[`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md).
A final coordinate-support theorem excludes the one-edge and
two-edge bridge boundaries:
[`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md).
Thus the complete nonresonant triangle is empty.  This does **not**
classify the resonant divisor `Omega=0`, prove that the nine known
pure-`P_4` components are exhaustive, or settle the global
Krenn--Gu conjecture.

The resonant divisor has since been reduced to an affine-holonomy
dichotomy in
[`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md):
nonzero additive holonomy gives a tangent-Segre first jet and a cyclic
kernel-cut system, while zero additive holonomy gives a compressed
binary-cubic map.  Those two incidences remain unresolved.

## Why the active-active coefficient is zero

The kernel of

```text
U_i tensor U_j -> R_2
```

is one-dimensional because its image has rank three.  Write its
coefficient matrix in the bases `(y_i,x_i),(y_j,x_j)`.  If the
coefficient of `x_i x_j` were `d`, multiply the relation by the two
opposite active rows.  Purity kills the other three terms, while
`x_0x_1x_2x_3` has nonzero top coefficient.  Hence `d=0`, giving
(1).  The relation matrix

```text
( a_ij  b_ij )
( c_ij     0 )
```

has rank two exactly when `b_ij c_ij != 0`.

## The triangle holonomy

Replace each active row by

```text
x_i' = x_i+s_i y_i.
```

In the new bases the edge coefficients become

```text
a_ij' = a_ij-c_ij s_i-b_ij s_j,                   (9)
```

while `b_ij,c_ij` do not change.  Therefore (4) is the linear system

```text
( c_12  b_12     0 )(s_1)   (a_12)
( c_13     0  b_13 )(s_2) = (a_13).               (10)
(    0  c_23  b_23 )(s_3)   (a_23)
```

Its determinant is `-Omega`, proving the first conclusion.

There is a projective connection hidden in (1).  Transport active
scale from mode `1` to `2`, from `2` to `3`, and back from `3` to `1`.
Its multiplicative holonomy is

```text
h =
 -(c_12 c_23 b_13)/(b_12 b_23 c_13).              (11)
```

Equation (2) says

```text
Omega=0  iff  h=1.                                 (12)
```

So the omitted divisor is exactly the trivial-holonomy, or resonant,
triangle.  The nonresonant condition is intrinsic: rescaling a row or
an edge relation multiplies both summands of `Omega` by the same
nonzero scalar.

## Six triple products disappear

After the shifts (4), multiply the three relations by the remaining
kernel row.  In the order

```text
x_1y_2y_3,  y_1x_2y_3,  y_1y_2x_3,
```

the coefficient matrix is exactly the matrix in (10).  Its determinant
is `-Omega`, so the first line of (5) follows.

Next multiply the three relations by the remaining active row.  In
the order

```text
y_1x_2x_3,  x_1y_2x_3,  x_1x_2y_3,
```

the coefficient matrix is

```text
( b_12  c_12     0 )
( b_13     0  c_13 )
(    0  b_23  c_23 ),                              (13)
```

which again has determinant `-Omega`.  This proves the second line of
(5).

Now (6) and (5) give

```text
U_k Q_ij=0
```

for the remaining index `k`.

The bridge cannot vanish.  If `Q_ij=0`, both
`y_i x_j` and `x_i y_j` vanish because `b_ij,c_ij` are nonzero.
Those are two independent kernel tensors, contradicting pair-image
rank three.

## The degree-two catalecticant

Write

```text
q=sum_(i<j) q_ij X_iX_j in R_2.
```

Use the bases `X_0,...,X_3` of `R_1` and

```text
X_1X_2X_3, X_0X_2X_3, X_0X_1X_3, X_0X_1X_2
```

of `R_3`.  Multiplication by `q` has matrix

```text
C(q)=
(   0  q_23 q_13 q_12 )
(q_23    0  q_03 q_02 )
(q_13 q_03    0  q_01 )
(q_12 q_02 q_01    0 ).                            (14)
```

It is symmetric with zero diagonal.  Since `U_k` is contained in its
kernel, (14) has rank at most two.  A nonzero symmetric
zero-diagonal matrix cannot have rank one: a symmetric rank-one matrix
is a scalar multiple of `vv^T`, and its zero diagonal would force
every coordinate of `v` to vanish.  Hence `C(Q_ij)` has rank exactly
two and its kernel has dimension exactly two.  This proves (7).

## Rank-two zero-diagonal matrices are cuts

Here is the small matrix theorem which supplies the discrete support
geometry.

Let `C` be a nonzero symmetric `4 x 4` matrix over `C`, with zero
diagonal and rank at most two.  Since its rank is exactly two, factor

```text
C=Z Z^T
```

after a congruence change in the two-dimensional auxiliary space.
Each row `z_i` of `Z` is isotropic because `C_ii=0`.  The isotropic
cone of the binary form

```text
s^2+t^2=(s+i t)(s-i t)
```

is the union of two lines.  Partition the nonzero rows according to
those two isotropic lines.  Inner products vanish inside each part,
while the cross block is an outer product.  Consequently

```text
C =
( 0       u v^T )
( v u^T     0  )                                  (15)
```

after permuting coordinates according to a nontrivial cut.  Zero rows
are harmless boundary cases.  Conversely every matrix (15) has rank
at most two.

Apply this to (14).

- For a `1+3` cut, say `{0}|{1,2,3}`, only
  `C_01,C_02,C_03` can be nonzero.  Under complementary-edge
  indexing in (14), this says

  ```text
  q in span(X_1X_2,X_1X_3,X_2X_3).
  ```

- For a `2+2` cut, say `{0,1}|{2,3}`, the cross block has rank one.
  In the `q` coordinates this is the tetrad

  ```text
  q_02 q_13-q_03 q_12=0,                           (16)
  ```

  and (16) is exactly the factorization (8).

This proves the cut classification.

## The useful neighboring literature

The holonomy calculation is the smallest instance of the
matrix-pencil/Kronecker viewpoint used in Bernardi--Gesmundo,
[Triangular tensor networks, pencils of matrices and
beyond](https://arxiv.org/abs/2602.15114).

The catalecticant step lands unexpectedly in algebraic statistics.
The `2+2` equation (16) is a tetrad: a rank-one off-diagonal block
constraint.  Sullivant--Talaska--Draisma,
[Trek separation for Gaussian graphical
models](https://arxiv.org/abs/0812.1938), organize covariance
submatrix rank by graph separation and matrix factorizations.  The
present matrix is not assumed positive and is not a covariance
matrix, but the same rank-factorization language exposes the cut.

The six coordinates `q_ij` are also the edge coordinates of the
second hypersimplex.  Sullivant,
[A Groebner basis for the secant ideal of the second
hypersimplex](https://arxiv.org/abs/0804.2897), relates its
off-diagonal minors to graph combinatorics.  Finally, the use of
degree-wise annihilators belongs to the exact-zero-divisor and
Lefschetz neighborhood of commutative algebra; see
Eddings--Vraciu,
[Rings for which general linear forms are exact zero
divisors](https://arxiv.org/abs/2407.16000).  None of these papers
states the reduction above; they supply the languages in which its
two short proofs become visible.

## Verification

The proof is the displayed symbolic argument.  A tiny exact replay
checks the two holonomy determinants, the catalecticant formula, and
representative `1+3`/`2+2` cut normal forms:

```text
uv run --with sympy \
  python verify_p4_nonresonant_rank_two_triangle_cut_reduction.py
```

It is not a search and is not a substitute for the proof.

The next symbolic compatible-label step is replayed by:

```text
python verify_p4_nonresonant_one_three_triangle_obstruction.py
python audit_p4_nonresonant_one_three_triangle_obstruction.py
python verify_p4_nonresonant_two_two_triangle_obstruction.py
python audit_p4_nonresonant_two_two_triangle_obstruction.py
python verify_p4_nonresonant_degenerate_cut_triangle_obstruction.py
python audit_p4_nonresonant_degenerate_cut_triangle_obstruction.py
```
