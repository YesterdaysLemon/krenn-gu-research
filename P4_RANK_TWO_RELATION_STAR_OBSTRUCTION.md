# Rank-two-relation stars are impossible after the Borel repair

## Status

This is an exact characteristic-zero obstruction on the
all-pair-rank-at-least-three pure `P_4` locus.

Suppose three exceptional pair edges form a star, every star edge has
product-image dimension three, and every unique star-edge relation has
coefficient-matrix rank two.  Then no such nonzero pure plane tuple exists.

An earlier proof of this statement was withdrawn because it invoked an
overstrong empty-triangle classification obtained by moving a purity-fixed
kernel line.  The present proof retains the Borel markings, uses the
corrected triangle classification, and separately closes the full-support
`2+2` Borel chart that the old normalization missed.

This repairs the star theorem; it does not classify mixed rank-one/rank-two
graphs, lower pair-image ranks, all pure `P_4` components, or the global
Krenn--Gu problem.

## Tree gauge

Let mode zero be the center and modes `1,2,3` the leaves.  In pure factor
bases `(y_i,x_i)`, each rank-two relation can be scaled to

```text
A_i y_0y_i+y_0x_i-x_0y_i=0.                         (1)
```

The star is a tree.  Independent Borel shifts

```text
x_i -> x_i+A_i y_i
```

therefore kill all three constants without a holonomy condition:

```text
y_0x_i=x_0y_i,                    i=1,2,3.           (2)
```

All leaves lie in the synchronizer of the marked center.

## Zero columns and kernel support one

If the center has a zero source column, (2) propagates that zero column to
every leaf.  All four planes lie in one source-coordinate hyperplane, so
their degree-four squarefree product is zero.  The restriction cannot be
nonzero pure.

If the center kernel has support one and there is no zero source column,
its synchronizer only changes the active row by the kernel row.  Every
finite leaf spans the center plane, whose square has dimension two.  This
contradicts the required center-leaf rank three; the projective point has
local rank one.

## Four distinct projective columns

For a center with four distinct nonzero projective columns, the
synchronizer is the classical adjugate pencil.  Pair-image rank drops among
two pencil points occur on three unordered pairs.  In a cross-ratio
coordinate `lambda`, the endpoints of those pairs are the roots of

```text
z^2-2z+1/lambda,
z^2-(2/lambda)z+1/lambda,
z^2-1/lambda.                                         (3)
```

Their pairwise resultants are

```text
4(lambda-1)^2/lambda^3,
-4(lambda-1)/lambda^2,
4(lambda-1)/lambda^3.                                (4)
```

Thus, for `lambda(lambda-1)!=0`, the rank-drop graph is a matching of
three disjoint edges.  The projective pencil point has no finite rank-drop
partner.

Among three leaves, some pair consequently still has image rank three.
The center and those two leaves form a triangle of three rank-three pairs
with rank-two relations.  The corrected theorem

[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md)

forces the kernel of every triangle mode onto one common two-coordinate
line.  This contradicts the present center, whose kernel support is three
or four.  Hence every four-distinct center is impossible.

Using full `PGL_2` to derive (3)--(4) is harmless here: pair-image rank and
the matching of pencil points are unmarked invariants.  The purity kernel is
not read after that coordinate calculation; it is retained in the Borel
triangle theorem that supplies the contradiction.

## The `2+1+1` and `3+1` collision pencils

For kernel support three or four, the remaining unbalanced collision
centers have synchronizer pencils whose projective point has local rank
one.  Every admissible leaf is finite and shares the center's active row
`x`.  In the `2+1+1` and `3+1` normal forms, `x` has support at most two.
Therefore the required all-active coefficient is

```text
x_0x_1x_2x_3=x^4=0.                                  (5)
```

These strata are empty.

## Kernel support two, distinct finite ratios

Use complementary binary blocks

```text
a=X_0+X_1,        a_bar=X_0-X_1,
b=X_2+X_3,        b_bar=X_2-X_3.                     (6)
```

The distinct-ratio synchronizer pencil has every admissible row-pair in
the form

```text
(a,b+alpha_i a_bar).                                 (7)
```

Choose the center kernel row, one leaf kernel row, and the active rows of
the other two leaves.  Since `a a_bar=0`,

```text
a*a*(b+alpha_2 a_bar)*(b+alpha_3 a_bar)
 =a^2b^2
 =4X_0X_1X_2X_3 !=0.                                (8)
```

This coefficient contains kernel rows and must vanish in a pure tensor.
Equation (8) is a contradiction.

## Kernel support two, coincident finite ratios

Now the center is `(a;b)` and its synchronizer is the presymplectic plane

```text
span((a;b),(b_bar;0),(0;a_bar)).                     (9)
```

Center-leaf rank three forces the radical coefficient to be nonzero, so
each leaf may be rescaled to

```text
y_i=a+beta_i b_bar,
x_i=b+alpha_i a_bar.                                 (10)
```

The analogue of (8) is again parameter-free:

```text
a*(a+beta_1 b_bar)
 *(b+alpha_2 a_bar)*(b+alpha_3 a_bar)
 =a^2b^2
 =4X_0X_1X_2X_3.                                    (11)
```

Thus kernel support two is completely excluded.

## The full-support `2+2` Borel chart

This is the chart absent from the withdrawn proof.  Put

```text
(y_0,x_0)=(a+b,b).                                   (12)
```

Its synchronizer is spanned by

```text
(a+b;b),               (-b_bar;0),
(-a_bar;-a_bar).                                      (13)
```

A general synchronized leaf is

```text
y_i=c_i(a+b)-r_i b_bar-s_i a_bar,
x_i=c_i b-s_i a_bar.                                 (14)
```

One center-leaf `3 x 3` product minor is `4c_i^3`.  Rank three therefore
forces `c_i!=0`, and each leaf can be rescaled to `c_i=1`.

Define

```text
E=s_1s_2+s_1s_3+s_2s_3.                              (15)
```

Two forbidden marked coefficients are

```text
T_0111=-4E,
T_0011=-4(E-1).                                      (16)
```

Both words contain at least one kernel row, so purity requires both to be
zero.  They demand `E=0` and `E=1` simultaneously.  This closes the last
Borel center type.

## Conclusion

The no-zero-column center types are exhausted by:

| kernel support | disposition |
|---|---|
| `4`, four distinct columns | rank-drop matching plus corrected triangle |
| `4`, `2+1+1` or `3+1` | common active fourth power is zero |
| `4`, `2+2` | incompatible coefficients (16) |
| `3`, distinct | rank-drop matching plus corrected triangle |
| `3`, collision | common active fourth power is zero |
| `2`, distinct or equal | constant forbidden coefficient `4` |
| `1` | center-leaf pair image has rank two |

Together with zero-column descent, this proves that the rank-two-relation
star is empty.

## Literature translation

The proof uses a small piece from each neighboring language:

- Kronecker/adjugate pencil roots make the generic rank-drop graph a
  matching;
- presymplectic radical geometry gives the full-support `2+2`
  synchronizer plane;
- annihilator lines in the squarefree complete intersection give the
  constant coefficients (8) and (11);
- the corrected binary-cubic theorem turns one surviving pencil pair into
  the rigid support-two triangle.

The relevant surrounding sources remain De Teran--Dopico--Landsberg on
[bounded-normal-rank pencils](https://arxiv.org/abs/1606.02574) and
Phuong--Tran on
[Lefschetz behavior of monomial complete intersections](https://arxiv.org/abs/2211.13548).
The Borel support synthesis and the two-word contradiction (16) are direct
repository results.

## Verification

Run:

```text
python verify_p4_rank_two_relation_star_obstruction.py
python audit_p4_rank_two_relation_star_obstruction.py
```

The primary verifier checks the three pencil resultants, projective endpoint
factors, both support-two constant coefficients, the full-support
synchronizer, its rank-three pivot, and the incompatible words (16).  The
audit uses a separate subset-dynamic permanent and independently replays the
resultants and coefficient contradictions.  Neither script searches for
solutions.
