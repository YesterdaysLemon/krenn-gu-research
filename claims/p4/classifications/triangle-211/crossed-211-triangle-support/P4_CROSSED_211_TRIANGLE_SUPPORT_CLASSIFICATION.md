# Crossed `(2,1,1)` triangles are controlled by an octahedron

## Status

**Exact dense support-two classification.**  Work over `C` in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Let `U_i=span(y_i,x_i)` be marked planes, with `y_i` the kernel row of
a nonzero pure `P_4` restriction.  Suppose the exceptional pairs on modes
`1,2,3` form a rank-three triangle whose unique relation ranks are
`(2,1,1)`.  Consider the crossed Borel orientation

```text
x_1 y_3=0,
y_2 x_3=0,
y_1 x_2=lambda x_1 y_2,       lambda!=0.             (1)
```

Assume the two zero products in (1) have genuine two-coordinate support.
Let `S,T` be their support pairs.  Then exactly the following alternatives
occur.

1. `S=T`: nonzero purity forces all three triangle planes into one
   coordinate hyperplane.
2. `S cap T=empty`: one marked plane collapses or one of the two
   rank-three pairs acquires a second zero product.  Hence this case is
   impossible under the hypotheses.
3. `|S cap T|=1`: either all three triangle planes again lie in one
   coordinate hyperplane, or the triangle is, up to source permutation,
   diagonal source scaling, and Borel-legal row scaling, exactly

   ```text
   U_1=span((1,1,1,1), (0,0,1,1)),
   U_2=span((1,0,1,0), (1,-1,1,1)),
   U_3=span((0,0,1,-1), (1,0,-1,0)).                (2)
   ```

Thus the full-source-support part of the crossed orientation is precisely
the fixed triangle of the first apolar component.  There is no disjoint
competitor.  This proves a complete theorem for the indicated Borel
orientation and genuine support-two stratum; common-factor orientations,
support-one zero products, and lower pair-image ranks remain outside it.
It is not component exhaustiveness and does not settle the global
Krenn--Gu conjecture.

The equal-support common-factor orientation has since supplied a new
six-dimensional component rather than an obstruction:
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](../../../../../P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md).
That result is consistent with this theorem because its two rank-one edges
share a common-mode factor, whereas (1) uses two independent common-mode
rows.

## Why an octahedron appears

A genuine linear zero product is, after diagonal source scaling,

```text
(X_i+X_j)(X_i-X_j)=0.                              (3)
```

Its invariant label is the two-subset `{i,j}`.  The six labels are the
vertices of

```text
J(4,2)=L(K_4),
```

the octahedral graph.  Two labels are adjacent when they overlap once and
opposite when they are disjoint.  Equality, opposition, and adjacency in
this octahedron are exactly the three branches above.  A picture is in
[`research_figures/P4_CROSSED_211_TRIANGLE_SUPPORT_OCTAHEDRON.svg`](../../../../../research_figures/P4_CROSSED_211_TRIANGLE_SUPPORT_OCTAHEDRON.svg).

The signed forms `X_i plus-or-minus X_j` are also the roots of type `D_4`.
The relation pattern therefore has a small Coxeter-arrangement shadow:
source permutations reduce the support problem to the three orbits of an
ordered pair of octahedron vertices.

![The six two-coordinate support labels as an octahedron; an adjacent pair
leads to the first apolar component and an opposite pair forces rank
drop.](../../../../../research_figures/P4_CROSSED_211_TRIANGLE_SUPPORT_OCTAHEDRON.png)

## The Borel reduction is legal

Before shifting, the rank-two relation on edge `12` has the form

```text
A y_1y_2+B y_1x_2+C x_1y_2=0,       BC!=0.          (4)
```

The active-active coefficient is zero because the opposite active product
detects it.  The shift

```text
x_2 -> x_2+(A/B)y_2
```

preserves `y_2x_3=0`, does not touch `x_1y_3=0`, and removes `A`.
Row rescaling then gives (1).  No kernel row is moved, so the entire
reduction stays inside the purity-preserving Borel group.

The three equations in (1) also kill every mixed triple product.  For
example, multiplying the rank-two relation by `y_3` or `x_3` makes each
side zero by one of the rank-one relations.  Hence only

```text
C=y_1y_2y_3,              D=x_1x_2x_3              (5)
```

can survive.  When `C!=0`, the opposite plane is therefore any two-plane in
`Ann(C)` on which `D` is nonzero.  On the surviving full-support adjacent
branch this is exactly the apolar `Gr(2,3)=P^2` fibre already found for the
first component.

## Equal support forces a coordinate hyperplane

Put `S=T={0,1}`.  The product `x_1y_2` must be nonzero: otherwise the two
terms in the nonsingular relation (1) are two separate decomposable kernel
tensors, and the pair image has rank at most two.  Rescale it to `X_0X_1`.
Write

```text
y_1=(a_0,a_1,a_2,a_3),       x_2=(b_0,b_1,b_2,b_3),
y_1x_2=X_0X_1.                                      (6)
```

Nonzero purity requires `D=x_1x_2x_3!=0`.  Since `x_1,x_3` are supported
on `{0,1}`, some `b_k` with `k in {2,3}` is nonzero.  Suppose `b_2!=0`.
The `02` and `12` coefficients in (6) give

```text
b_0=-a_0b_2/a_2,        b_1=-a_1b_2/a_2.            (7)
```

Here `a_2`, `a_0`, and `a_1` are nonzero because the target `01`
coefficient is nonzero.  The vanishing `03` and `13` coefficients then give

```text
b_3=a_3b_2/a_2,
```

while the `23` coefficient is `2a_3b_2` and must vanish.  Characteristic
zero gives

```text
a_3=b_3=0.                                          (8)
```

Thus all six triangle rows lie in the coordinate hyperplane `z_3=0`.
The case `b_3!=0` is symmetric.  This is a Schubert boundary, not a new
full-support branch.

## Disjoint support is the `K_(2,2)` anchor lemma

Put `S={0,1}`, `T={2,3}` and normalize

```text
a=(1,1,0,0),       a_bar=(1,-1,0,0),
b=(0,0,1,1),       b_bar=(0,0,1,-1),                (9)
```

so that

```text
x_1=a,       y_3=a_bar,       y_2=b,       x_3=b_bar.
```

The remaining equation is a factorization

```text
y_1x_2=ab.                                           (10)
```

Split `y_1=u+v` and `x_2=u'+v'` across the two binary blocks
`A=span(X_0,X_1)` and `B=span(X_2,X_3)`.  The cross-block part of (10) is

```text
u(v')^T+u'v^T=ab^T.                                  (11)
```

The right side has matrix rank one.  Factoring the left side as
`[u u'][v' v]^T` gives the exterior identity

```text
det(u,u') det(v',v)=0.                                (12)
```

If `u,u'` are dependent, their common direction must be `a`.  The internal
zero coefficient and `a^2!=0` force one of them to vanish.  The other block
then gives one of

```text
y_1=a+t b_bar,       x_2=b,                           (13a)
y_1=b,               x_2=a+t b_bar.                  (13b)
```

The first collapses `U_2`; the second adds `y_1x_3=bb_bar=0` to edge `13`,
which already has `x_1y_3=aa_bar=0`, so its image rank is at most two.
The case `v,v'` dependent gives

```text
y_1=a,               x_2=b+t a_bar,                  (13c)
y_1=b+t a_bar,       x_2=a.                          (13d)
```

Now either `U_1` collapses or edge `23` acquires the second zero product
`x_2y_3=aa_bar=0`.  This excludes the disjoint branch without solving an
ideal.  It is the four-vertex specialization of the hyperbolic-block anchor
lemma in
[`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md).

## One-coordinate overlap has one dense orbit

Normalize the adjacent labels to `S={2,3}`, `T={0,2}`:

```text
x_1=(0,0,1,1),       y_3=(0,0,1,-1),
y_2=(1,0,1,0),       x_3=(1,0,-1,0).                (14)
```

Then, up to a nonzero scalar, (10) is

```text
y_1x_2=(X_2+X_3)(X_0+X_2).                          (15)
```

Write `y_1=(a_0,a_1,a_2,a_3)` and `x_2=(b_0,b_1,b_2,b_3)`.  The three
zero coefficients incident with the missing coordinate one are

```text
a_1b_j+a_jb_1=0,       j=0,2,3.                     (16)
```

If `a_1=0`, the three nonzero target coefficients force `b_1=0`; the
converse is symmetric.  This is again the coordinate-hyperplane boundary.

On the complementary branch, put `mu=b_1/a_1`.  Equations (16) give

```text
x_2=mu(-a_0,a_1,-a_2,-a_3).                         (17)
```

The three nonzero coefficients of the product are

```text
-2mu a_0a_2,       -2mu a_0a_3,       -2mu a_2a_3. (18)
```

They are equal and nonzero, so

```text
a_0=a_2=a_3!=0.                                    (19)
```

Row scaling fixes their common value.  Coordinate one appears in none of
the four fixed rows (14), so the unused diagonal source scaling fixes the
remaining ratio `a_1/a_0`.  After rescaling `x_2`, this is exactly (2).

For the one-parameter form before that last source scaling,

```text
y_1=(1,r,1,1),       x_2=(1,-r,1,1),       r!=0,    (20)
```

three explicit pair-image minors are

```text
-2r^2,       -2r,       r^2,                         (21)
```

so all three exceptional pair ranks really are three.  The unique relation
on edge `12` is

```text
-(1/2)y_1x_2+x_1y_2=0.                              (22)
```

At `r=1`, the covectors in (5) are

```text
C=(-1,-1,-1,1),       D=(1,1,-1,-1),                (23)
```

which recovers the apolar normal form verbatim.

## Matrix completion and exact-zero-divisor neighbors

For column vectors `u,v`, multiplication in `R_2` records the off-diagonal
entries of

```text
uv^T+vu^T.                                           (24)
```

The diagonal is forgotten because `X_i^2=0`.  Thus (6), (10), and (15) are
free-diagonal symmetric low-rank completions of weighted adjacency matrices
supported on `K_2`, `K_(2,2)`, and `K_3`.  The local
determinantal/matroid viewpoint is adjacent to Kiraly--Theran--Tomioka,
[The Algebraic Combinatorial Approach for Low-Rank Matrix Completion](https://arxiv.org/abs/1211.4116),
and the symmetric version studied by Bernstein--Blekherman--Lee,
[Typical ranks in symmetric matrix completion](https://arxiv.org/abs/1909.06593).
Those works organize generic completion patterns; neither states the
marked squarefree factorization (13)--(22).

The pairs in (3) are homogeneous zero divisors in an Artinian algebra.
Kustin--Striuli--Vraciu,
[Exact pairs of homogeneous zero divisors](https://arxiv.org/abs/1304.0411),
develop general Hilbert-function constraints for exact pairs.  Here the
degree-one annihilator bound is much sharper and the `D_4` support label is
what makes the triangle finite.  Finally, the passage from (5) to the
opposite `Gr(2,3)` is Macaulay duality in the same Artinian-Gorenstein world
as Maeno--Watanabe's
[higher-Hessian characterization of Lefschetz elements](https://arxiv.org/abs/0903.3581).

The new point is the synthesis: octahedral support incidence selects the
matrix-completion graph, its rank-one factorization fixes the triangle, and
apolarity supplies the opposite plane.

## Verification

Run:

```text
uv run --with sympy python claims/p4/classifications/triangle-211/crossed-211-triangle-support/verify_p4_crossed_211_triangle_support_classification.py
uv run --with sympy python claims/p4/classifications/triangle-211/crossed-211-triangle-support/audit_p4_crossed_211_triangle_support_classification.py
```

The primary verifier checks (9)--(23), the three generic rank minors, all
six mixed triple vanishings, and the exact apolar pure restriction.  The
audit applies an unrelated source permutation and unequal diagonal scaling,
reconstructs products and permanents by separate routines, and checks the
same relation ranks and pure tensor.  Both are constant-size symbolic proof
replays, not searches.
