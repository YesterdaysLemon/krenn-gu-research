# Corrected classification of rank-two-relation triangles

## Status

This is an exact characteristic-zero classification of the exceptional
triangle in a nonzero pure `P_4` restriction under the following hypotheses:

1. all three pair-product images have dimension three;
2. each unique pair relation has coefficient-matrix rank two.

The earlier theorem claimed that this triangle was empty.  That claim was
withdrawn because a full row `GL_2` normalization moved the purity-fixed
kernel lines.  The corrected answer is:

> The triangle is not empty.  Up to source-coordinate permutation and
> diagonal scaling, every example is
>
> ```text
> U_0=span(b_bar,a_bar),
> U_i=span(a,b+alpha_i a_bar),              i=1,2,3,       (1)
> ```
>
> where
>
> ```text
> a=X_0+X_1,          a_bar=X_0-X_1,
> b=X_2+X_3,          b_bar=X_2-X_3,                       (2)
> ```
>
> and
>
> ```text
> alpha_1+alpha_2+alpha_3 != 0.                           (3)
> ```

In the marked pure bases

```text
(y_0,x_0)=(b_bar,a_bar),
(y_i,x_i)=(a,b+alpha_i a_bar),
```

the restricted tensor is exactly

```text
-4(alpha_1+alpha_2+alpha_3) x_0 x_1 x_2 x_3.             (4)
```

Thus this note supplies a genuine symbolic family and a complete theorem,
not an obstruction.  It corrects the withdrawn flat-triangle record and
provides the honest input for the still-withdrawn star and mixed-triangle
arguments.  It does not prove pure-component exhaustiveness, construct a
Krenn--Gu graph, or settle the global conjecture.

## From holonomy to the flat problem

The earlier exact reductions remain valid:

- the complete nonresonant triangle is empty by the `1+3`, `2+2`, and
  proper-support cut theorems;
- on resonance, nonzero additive holonomy is empty by the tangent-Segre cut
  obstruction;
- zero additive holonomy gives synchronized row-pairs

  ```text
  y_i x_j=x_i y_j,                    i<j,                (5)
  ```

  and a binary-cubic flag

  ```text
  dim span(Y,K,J)<=2,                 X notin span(Y,K,J). (6)
  ```

Therefore only the flat synchronized problem needs classification here.

## Zero source columns descend to `P_3`

Suppose one source column of one row-pair is zero.  The synchronization
equations involving that coordinate say that the corresponding column of
every partner is symplectically orthogonal to every nonzero column of the
first row-pair.  Those columns span `C^2`, so the partner columns are zero as
well.

All three triangle planes then lie in one coordinate hyperplane.  A nonzero
pure `P_4` restriction suspends a pure `P_3` restriction.  In the
three-variable squarefree algebra, the perfect pairing

```text
R_2 tensor R_1 -> R_3=C
```

and flattening rank one force every pair image to have dimension at most
two.  This contradicts the rank-three hypothesis.  Hence the remaining
classification may assume that all source columns are nonzero.

## Borel support stratification

Choose one kernel row `y` and let `k=|supp(y)|`.  Diagonal source scaling,
one common affine change of the finite ratios, and source permutation give
a finite list without moving the kernel line.

### Kernel support four

All ratio multiplicities and both projective partner sheets are already
closed by

- [`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md),
- [`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md),
- [`P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md`](P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md).

Thus `k=4` is empty.

### Kernel support three

With no zero source column, normalize the missing kernel coordinate to have
active value one.  If the three finite ratios are distinct, the exact
one-kernel-zero compound theorem applies:

[`P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md).

The two collision types are

```text
y=(1,0,1,1),      x=(0,1,0,1),             finite type 2+1,
y=(1,0,1,1),      x=(0,1,0,0),             finite type 3. (7)
```

In both cases the synchronizer is a projective line `span(A,B)`, the point
`B` has local rank one, and every admissible partner is finite with the
same active row `x`.  That row has support at most two, so

```text
X=x^3=0.                                                   (8)
```

This contradicts the escape half of (6).  Hence `k=3` is empty.

### Kernel support one

The no-zero-column normal form is

```text
y=(1,0,0,0),             x=(0,1,1,1).                 (9)
```

Its synchronizer only changes `x` by a multiple of `y`.  Every finite
partner therefore spans the same plane `U=span(y,x)`; the point at infinity
has local rank one.  Since `y^2=0`,

```text
U^2=span(yx,x^2)
```

has dimension two.  This violates the pair-rank-three hypothesis.  Hence
`k=1` is empty.

Only `k=2` can survive.

## Kernel support two: distinct finite ratios

First take

```text
y=(1,1,0,0),             x=(0,1,1,1).                 (10)
```

The synchronizer is the pencil

```text
(y,x+t z),                z=(-1,1,0,0),                (11)
```

whose projective point `(0;z)` has local rank one.  Thus every admissible
triple is finite, with parameters `0,t,u`.

Its binary-cubic matrix is

```text
C=
[0 0 2  2t+2u+6;
 0 0 2 -2t-2u;
 0 2 2 -2tu-2t-2u;
 0 2 2 -2tu-2t-2u].                                  (12)
```

The first three columns have rank two, and a full cofactor is

```text
-8(2t+2u+3).                                          (13)
```

Consequently purity is equivalent to

```text
2t+2u+3 != 0.                                         (14)
```

This is already the family (1): shift each active row by half its kernel
row and put

```text
alpha_1=-1/2,
alpha_2=-(t+1/2),
alpha_3=-(u+1/2).                                     (15)
```

Then (14) is exactly (3).

## Kernel support two: coincident finite ratios

Use the block notation (2) and take the center `(a;b)`.  Its synchronizer
is

```text
S=span(A,B_0,B_1),
A=(a;b),             B_0=(b_bar;0),       B_1=(0;a_bar). (16)
```

The multiplication commutator is a degenerate alternating form on `S`:
`A` is its radical and `omega(B_0,B_1)!=0`.  Hence every mutually
synchronized triple lies on a projective line through `A`.  Write

```text
D=rB_0+sB_1,
A,                   A+tD,                  A+uD.      (17)
```

The coefficient matrix is, up to harmless signs of `r,s`,

```text
C=
[-2r^2tu  0 2   2s(t+u);
 -2r^2tu  0 2  -2s(t+u);
  2r(t+u) 2 0  -2s^2tu;
 -2r(t+u) 2 0  -2s^2tu].                              (18)
```

Its nonzero compression minors are both `16r(t+u)`, while a compressed
`2 x 2` minor is the constant `-4`.

- If `r!=0`, compression forces `u=-t`.  Every full cofactor then vanishes,
  but the compressed span still has dimension two, so `X` cannot escape.
- If `r=0`, the triple is exactly

  ```text
  (a;b),             (a;b+st a_bar),
                     (a;b+su a_bar),                  (19)
  ```

  and purity is equivalent to `s(t+u)!=0`, again condition (3).

A projective direction `D` is a valid local plane only when `rs!=0`.
But then the pair image of `A` and `D` is spanned only by

```text
a b_bar,                     b a_bar,                 (20)
```

and has dimension two.  Thus every endpoint sheet exits the rank-three
triangle before purity is considered.

This completes the support stratification and proves that (1) is exhaustive.

## Direct verification of the survivor

For `i!=j`, the pair products of the leaves in (1) are spanned by

```text
a^2,
ab,
b^2+(alpha_i+alpha_j)b a_bar+alpha_i alpha_j a_bar^2. (21)
```

Their supports make these three vectors independent.  The unique relation
is

```text
a(b+alpha_j a_bar)-(b+alpha_i a_bar)a=0,              (22)
```

whose coefficient matrix has rank two.  Hence all three leaf-pair images
have dimension exactly three.

The triple coefficients are

```text
Y=0,
K=a^2b,
J=ab^2,
X=e_1 b^2a_bar-e_2 a^2b,                              (23)
```

where

```text
e_1=alpha_1+alpha_2+alpha_3,
e_2=alpha_1alpha_2+alpha_1alpha_3+alpha_2alpha_3.      (24)
```

Here `a_bar^2=-a^2`, and `K,J,b^2a_bar` are independent.  Thus (6) is
equivalent to `e_1!=0`.

Finally,

```text
Ann_R1(span(K,J))=span(a_bar,b_bar).                  (25)
```

The covector induced by `X` on this annihilator kills `b_bar` and is
nonzero on `a_bar`.  This forces the opposite marked plane
`(y_0,x_0)=(b_bar,a_bar)`.  Direct degree-four multiplication then gives
exactly (4); all other fifteen coefficients vanish.

## What the neighboring mathematics contributed

Three translations make the classification small.

1. The flat relations are an affine local system; holonomy separates the
   tangent branch from the synchronized branch.
2. Synchronizer jumps are presymplectic polar spaces, so compatible triples
   are isotropic projective lines rather than arbitrary parameter triples.
3. The survivor is an annihilator-line construction in the squarefree
   Artinian complete intersection.  The identities
   `a a_bar=b b_bar=0` turn the entire tensor calculation into elementary
   symmetric polynomials in the `alpha_i`.

The surrounding literatures are matrix-pencil closure
([De Teran--Dopico](https://arxiv.org/abs/2204.10237)), projective
symplectic geometry
([Prazmowska--Prazmowski--Zynel](https://arxiv.org/abs/1203.2053)), and
Lefschetz/annihilator behavior of monomial complete intersections
([Phuong--Tran](https://arxiv.org/abs/2211.13548)).  The normal form (1) and
its exhaustiveness are repository-specific.

## Correct frontier

The all-rank-two-relation triangle is now classified rather than merely
obstructed.  The next symbolic questions are compatibility of (1) with:

1. a third rank-two spoke in the withdrawn star problem;
2. a rank-one third edge in the withdrawn mixed `(2,2,1)` problem;
3. the lower pair-image-rank components; and
4. the marked `P_5` extension strata relevant to Krenn--Gu.

Those are global compatibility questions.  This theorem alone does not
settle them.

## Verification

Run:

```text
python verify_p4_rank_two_relation_triangle_corrected_classification.py
python audit_p4_rank_two_relation_triangle_corrected_classification.py
```

The primary verifier reconstructs every remaining Borel synchronizer,
checks the support-three zero cubes, the two support-two charts and their
projective boundary, the support-one pair-rank collapse, and all sixteen
coefficients of (4).  The audit uses an independent subset-dynamic
squarefree product and separately replays the survivor, its pair ranks, and
the canonical boundary charts.  Neither script searches for solutions.
