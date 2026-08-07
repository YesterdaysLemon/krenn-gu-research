# The projective flat sheet closes through an additive parallelogram seam

## Status

This is an exact characteristic-zero classification of every projective
partner sheet over the genuine Borel-generic flat center

```text
y=(1,1,1,1),                 x=(0,1,p,q),
pq(p-1)(q-1)(p-q)!=0.                                      (1)
```

Together with
[`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md),
it proves that no pure all-rank-three-relation triangle occurs over this
center, even when one or both synchronized partners lie at infinity in
their pencil.

The one-infinity incidence is not empty as a pure `P_4` problem.  It is
exactly three rational curves.  On every one, however, the pair consisting
of the infinite partner and the remaining finite partner has product-image
rank two rather than three.  These curves are therefore the seam to the
lower-pair-rank Segre/Kronecker boundary, not counterexamples to the
rank-three triangle theorem.

The full-support affine-ratio collisions have since been classified in
[`P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md`](P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md).
The smaller-support strata have since been classified and contain one
explicit support-two survivor:
[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md).
This is not a
classification of every pure `P_4` component and not a proof or
counterexample for the global Krenn--Gu conjecture.

## Compactifying the synchronizer pencil

The true synchronizer of (1) is spanned by `A=(y;x)` and

```text
y^#=(0,p+q-1,p(1-p+q),q(1+p-q)),
x^#=pq(-1,1,1,1).                                      (2)
```

Thus a partner is a point `[s:t]` of the projective pencil

```text
A(s,t)=sA+tA^#.                                         (3)
```

The finite--finite chart `[1:t],[1:u]` is empty by the companion generic
theorem.  Up to interchanging the two partners, the omitted sheets are

```text
([0:1],[1:u])                 and                 ([0:1],[0:1]).   (4)
```

This is the appropriate compactification because the kernel line is fixed:
full row `PGL_2` would move the purity flag, while (3) compactifies only the
actual synchronizer pencil.

## One partner at infinity

Take the three planes

```text
A,                    A^#,                    A+uA^#.     (5)
```

Let

```text
C=[Y K J X]
```

be the four squarefree cubic coefficients, indexed in the omitted-source
basis.  Put

```text
H=p^2-2pq-2p+q^2-2q+1,
G=pqHu^2-6pqu-p-q-1.                                  (6)
```

Three compression minors factor as

```text
c_0= 8p^2q^2(p-1) A_0 G,
c_1= 8p^2q^2(q-1) A_1 G,
c_2=-8p^2q^2(p-q) A_2 G,                              (7)
```

where

```text
A_0=(p-q+1)(q(p-q+1)u+1),
A_1=(p-q-1)(p(p-q-1)u-1),
A_2=(p+q-1)((p+q-1)u+1).                              (8)
```

Every `3 x 3` minor of the full `C` is divisible by `G`.  Moreover, three
`2 x 2` minors of `[Y K J]` are

```text
-4pq(p-1)A_0,        -4pq(q-1)A_1,        4pq(p-q)A_2. (9)
```

If compression held with `G!=0`, equations (7) would give
`A_0=A_1=A_2=0`.  Splitting the three products in (8) gives eight tiny
factor ideals.  Four are the unit ideal, one gives the excluded collision
`p=q=1`, and the remaining three all imply `G=0`.  Hence compression forces

```text
G=0.                                                   (10)
```

All full `3 x 3` minors now vanish.  Since purity requires `X` to escape
`span(Y,K,J)`, that compressed span must be a line.  Equation (9) again
gives `A_0=A_1=A_2=0`.  The three genuine solutions are

```text
q=p+1,          u=-1/(2p),
p=q+1,          u=-1/(2q),
p+q=1,          u=-1/(2pq).                           (11)
```

On each curve, exact minors give

```text
rank[Y K J]=1,             rank C=2.                  (12)
```

Thus (11) really is pure rather than an artifact of necessary equations.

## The hidden additive-combinatorial shape

Write the four marked affine ratios as

```text
r=(r_0,r_1,r_2,r_3)=(0,1,p,q).                       (13)
```

The three equations in (11) are precisely

```text
r_0+r_3=r_1+r_2,
r_0+r_2=r_1+r_3,
r_0+r_1=r_2+r_3.                                     (14)
```

Therefore the projective pure locus occurs exactly when the four ratios
contain an additive parallelogram: two disjoint pairs have the same sum.
Equivalently, the four-point affine configuration fails the weak Sidon
condition.  This statement is invariant under the legal common affine
change `r_i -> alpha*r_i+beta`; it would not be visible after quotienting by
the larger projective group.

The additive language is not merely a name for (11).  It predicts the
three components before elimination: they are indexed by the three perfect
matchings of four marked points.

## Why the three pure curves do not belong to the triangle

Let `M_#(u)` be the `6 x 4` product matrix of the pair

```text
(A^#,A+uA^#):

[y^#y(u), y^#x(u), x^#y(u), x^#x(u)].                (15)
```

After each substitution (11), every `3 x 3` minor of `M_#(u)` vanishes.
The following `2 x 2` minors remain nonzero under (1):

```text
-2p^2(p-1)(p+1),
-2q^2(q-1)(q+1),
-2q^2(q-1)^2(2q-1),                                  (16)
```

respectively.  Hence

```text
rank M_#(u)=2                                           (17)
```

on all three pure curves.  The starting triangle stratum requires every
pair image to have rank three with one rank-two relation.  Equation (17)
removes every one-infinity pure point from that stratum.

Geometrically, the binary-cubic compression can meet the projective pencil
boundary only by falling onto the secant/tangent bounded-rank seam of the
pair kernel.  The additive parallelogram and the Kronecker rank drop are two
descriptions of the same divisor.

## Both partners at infinity

For `(A,A^#,A^#)`, the three nonzero compression minors are

```text
 8p^3q^4(p-1)(p-q+1)^2 H,
 8p^4q^3(q-1)(p-q-1)^2 H,
-8p^3q^3(p-q)(p+q-1)^2 H.                            (18)
```

The first two already show that compression forces `H=0`: otherwise they
would require `p-q=-1` and `p-q=1` simultaneously.  Every full `3 x 3`
minor is divisible by `H`, so purity would again require the first three
columns to span a line.  But two of their `2 x 2` minors are

```text
4p^2q^3(p-1)(p-q+1)^2,
4p^3q^2(q-1)(p-q-1)^2,                               (19)
```

which impose the same impossible pair of equations.  The double-infinity
sheet is empty even before using exact pair-image rank three.

## Literature translation

The surrounding tools come from three neighboring subjects.

- Projective closure of a matrix-pencil family is the correct way to retain
  singular sheets; see De Teran and Dopico,
  [Bundles of matrix pencils under strict equivalence](https://arxiv.org/abs/2204.10237).
- The coefficient flag `Y,K,J,X` is an osculating binary-cubic/Veronese
  object; see Bernardi--Catalisano--Gimigliano--Ida,
  [Osculating varieties of Veronese varieties and their higher secant varieties](https://arxiv.org/abs/0807.2455).
- Failure of distinct pair sums is the defining Sidon-type additive
  collision; for a standard vector-set formulation, see Lee,
  [On Sidon sets in a random set of vectors](https://arxiv.org/abs/1405.4227).

The specific implication

```text
projective pure binary-cubic sheet
    => repeated disjoint pair sum
    => pair-product rank two
```

was not found in that literature.  It is the repository-specific bridge
between the three languages.

## Verification

Run:

```text
python verify_p4_resonant_flat_projective_partner.py
python audit_p4_resonant_flat_projective_partner.py
```

The primary verifier reconstructs the pencil, factors the compression and
compound minors, checks all eight factor ideals, proves the exact ranks on
the three rational curves, and closes the double-infinity sheet.  The audit
uses a separate subset-dynamic-program squarefree product and independently
checks the additive curves, their pair-rank drops, and the double-infinity
divisibility.  Neither script searches for solutions.
