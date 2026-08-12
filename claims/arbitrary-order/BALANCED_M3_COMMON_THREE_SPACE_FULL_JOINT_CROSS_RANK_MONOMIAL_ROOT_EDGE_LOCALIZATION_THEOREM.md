# Balanced `m=3` common-three-space full-joint-cross-rank monomial-root-edge localization

## Status

**Exact characteristic-zero localization on the full joint cross-rank part of
the S2Q common-three-space stratum.**  Let `U` be the total singleton span of
a normalized, target-consistent physical `m=3` common shore, assume

```text
dim U=3,                                                (1)
```

and collect all nine root--nonroot colour columns into the joint map

```text
H: A_x direct-sum A_y direct-sum A_r
   -> A_1 direct-sum A_2 direct-sum A_3.                (2)
```

If `H` has rank nine, then exactly one of the three root--root blocks is
nonzero, and that block has exactly one nonzero **diagonal**
target-coordinate entry.  After permuting roots it has the form

```text
B_23=lambda e_(2,s) tensor e_(3,s),   lambda!=0,
B_12=B_13=0,                                           (3)
```

and

```text
U=A_1 tensor e_(2,s) tensor e_(3,s).                   (4)
```

Consequently the physical empty companion must satisfy the sharp sparse
identity

```text
G_N congruent J modulo
 A_1 tensor e_(2,s) tensor e_(3,s).                    (5)
```

An off-diagonal monomial `e_(2,p) tensor e_(3,q)` with `p!=q` would make the
unique rational pair deck global by an explicit `2 x 2` permanent formula.
It would therefore reconstruct a forbidden six-vertex Krenn--Gu graph.
Equivalently, outside the one-diagonal-monomial-root-edge normal forms (and
their root permutations), the joint cross map has rank at most eight.

This is a localization, not an exclusion.  It does not prove that an
arbitrary invertible joint cross map can or cannot satisfy (5), although the
monomial joint-cross subcase is excluded exactly below.  Joint rank at most
eight remains open.  It does not treat the rank-one or pair-plane S2Q strata,
`m>=4`, the all-balanced rank-drop branch, a witness, or a counterexample.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The shared derivative map

Use the physical singleton notation of S2N.  Put

```text
D_B(h_1,h_2,h_3)
 =h_1 tensor B_23
  +insert_2(B_13,h_2)
  +B_12 tensor h_3.                                   (6)
```

For `u in {x,y,r}`, the three colour columns of the cross blocks define

```text
H_u:A_u -> A_1 direct-sum A_2 direct-sum A_3,
H_u(e_c)=(h_(1,u)^(c),h_(2,u)^(c),h_(3,u)^(c)).       (7)
```

The map in (2) is `(H_x,H_y,H_r)`.  Formula (6) of S2N says exactly that
the nine singleton slices are the columns of `D_B H`; hence

```text
U=image(D_B H).                                       (8)
```

If `rank H=9`, then `H` is an isomorphism and therefore

```text
U=image D_B.                                          (9)
```

The full-joint-rank hypothesis is stronger than physical full-sensor rank.
It is isolated here because (9) makes the common-three-space condition
completely rigid.

## 2. Two nonzero root blocks already give dimension at least five

For a nonzero root--root block, its contribution to (6) is a
three-dimensional subspace.  For example,

```text
S_1=A_1 tensor B_23,
S_2=insert_2(B_13,A_2),
S_3=B_12 tensor A_3.                                  (10)
```

### Lemma 1 (pairwise shared-factor intersection)

For distinct `i,j`, if both corresponding blocks in (10) are nonzero, then

```text
dim(S_i intersect S_j)<=1.                            (11)
```

### Proof

It is enough to treat `S_1,S_2`.  A nonzero tensor in their intersection has
two presentations

```text
T=a_1 tensor B_23=insert_2(B_13,a_2).                 (12)
```

The left presentation has rank one across
`A_1 | (A_2 tensor A_3)`.  In the right presentation this flattening rank is
the `A_1|A_3` matrix rank of `B_13`, so (12) forces

```text
B_13=a_1 tensor a_3.                                  (13)
```

Applying the symmetric argument across `A_2 | (A_1 tensor A_3)` forces

```text
B_23=a_2 tensor a_3                                   (14)
```

up to reciprocal nonzero scalars.  Thus every nonzero intersection tensor
lies on the one line `K(a_1 tensor a_2 tensor a_3)`.  If either forced
factorization fails, the intersection is zero.  This proves (11).  QED.

Each nonzero `S_i` has dimension three.  Lemma 1 therefore gives

```text
dim(S_i+S_j)>=3+3-1=5                                 (15)
```

whenever two root blocks are nonzero.  Equations (1), (9), and (10) rule
this out.  Since `image D_B` has dimension three rather than zero, exactly
one root block is nonzero.

After permuting roots, suppose it is `B_23`.  Then

```text
image D_B=A_1 tensor B_23.                            (16)
```

## 3. Torus blocking forces a coordinate monomial

The S2R torus-annihilator theorem says that no fully supported product
functional annihilates `U`.  Under (16), a product functional

```text
a_1 tensor a_2 tensor a_3
```

annihilates `U` exactly when

```text
(a_2 tensor a_3)(B_23)=0.                             (17)
```

### Lemma 2 (a nonmonomial bilinear form has a torus zero)

Let

```text
F(s,t)=sum_(j,k) b_(j,k) s_j t_k                     (18)
```

be a nonzero bilinear form over `C`.  If at least two coefficients in (18)
are nonzero, then `F` vanishes at a point with every `s_j,t_k` nonzero.

### Proof

Choose integer weights on the six variables such that the finitely many
exponent vectors of the nonzero monomials `s_j t_k` have distinct weights.
Substitute every variable by a nonzero constant times an integral power of
one parameter `z`.  The result is a Laurent polynomial with at least two
distinct nonzero terms.  After removing its lowest power of `z`, it is a
nonconstant ordinary polynomial with nonzero constant term.  Over `C` it
has a root, and that root is nonzero.  The corresponding six substituted
coordinates are therefore all nonzero and annihilate (18).  QED.

If `B_23` had at least two nonzero coordinate entries, Lemma 2 would supply
fully supported `a_2,a_3` satisfying (17).  Choosing any fully supported
`a_1` would contradict S2R.  Hence `B_23` has one nonzero entry, proving
(3)--(4).

All arguments are polynomial and descend from a putative solution over a
characteristic-zero field to a finitely generated extension of `Q`, which
embeds in `C`.  Thus the localization is valid in characteristic zero.

## 4. Off-diagonal monomials globalize the pair deck

Before identifying the two endpoint colours, write the monomial supplied by
Section 3 as

```text
B_23=lambda e_(2,p) tensor e_(3,q).                   (19)
```

For a nonroot `u`, let `A_u:A_u -> A_1` be the root-`1` cross block, and let
`b_u,c_u` be the scalar linear forms obtained by taking respectively the
root-`2` colour-`p` row and root-`3` colour-`q` row of their cross blocks.
The singleton columns are

```text
G_u=lambda A_u(u) tensor e_(2,p) tensor e_(3,q).      (20)
```

Grouping the six cross matchings according to the nonroot matched to root
`1` gives the coefficient of `G_N` on the exceptional root line:

```text
G_N|_(A_1 tensor e_p tensor e_q)
 =A_x(x)[b_y(y)c_r(r)+b_r(r)c_y(y)]
  +A_y(y)[b_x(x)c_r(r)+b_r(r)c_x(x)]
  +A_r(r)[b_x(x)c_y(y)+b_y(y)c_x(x)].                (21)
```

Suppose `p!=q`.  The GHZ target has no root coefficient on
`A_1 tensor e_(2,p) tensor e_(3,q)`.  Since (5) already fixes every other
root coefficient, the target equation is satisfied by the three **global**
bilinear pair blocks

```text
C_yr=-lambda^(-1)[b_y c_r+b_r c_y],
C_xr=-lambda^(-1)[b_x c_r+b_r c_x],
C_xy=-lambda^(-1)[b_x c_y+b_y c_x].                 (22)
```

These are ordinary physical edge blocks, not rational chart functions.
Together with the same root and cross blocks they reconstruct a six-vertex
ternary graph satisfying the GHZ equality and normalization.  The accepted
exact six-vertex theorem excludes this.  Hence `p=q`; writing their common
value as `s` proves (3)--(5).

## 5. The surviving block-permanent obligation

S2R proves, without regularizing the rational pair deck, that

```text
G_N congruent J modulo U.                             (23)
```

Substitution of (4) gives (5).  In coordinates, every root coefficient of
the six-cross-matching tensor is therefore fixed to the GHZ coefficient
except the three root words

```text
(a,s,s),              a=0,1,2.                       (24)
```

The remaining exact question on this branch is:

```text
Can an invertible 9 x 9 block matrix H have its
three-by-three block permanent supported on GHZ plus (24)?             (25)
```

The singleton full-sensor condition supplies an additional open condition:
the three vectors `H_(1,x)x`, `H_(1,y)y`, `H_(1,r)r` must be generically
independent in `A_1`.  Neither (25) nor this open condition is decided here.

There is, however, one exact exclusion inside (25).

### Theorem 3 (an invertible monomial joint cross map is impossible)

If `H` has exactly one nonzero entry in every row and every column, then its
block-permanent map has rank at least six.  It therefore cannot satisfy (5),
whose support has at most the three exceptional rows (24) and the two
unexceptional GHZ diagonal rows.

### Proof

Partition the rows of `H` by the three roots and its columns by the three
nonroots.  Let

```text
N_(i,u)=number of nonzero entries from root block i
        to nonroot block u.                          (26)
```

Every row and column sum of the nonnegative integer `3 x 3` matrix `N` is
three.  The block-permanent map of a monomial matrix is a partial monomial
matrix: a root-colour transversal survives precisely when its three unique
nonzero entries land in three distinct nonroot blocks.  Consequently

```text
rank(block-permanent H)=per(N).                      (27)
```

For completeness, `per(N)>=6` follows by three elementary cases.  If a row
has type `(3,0,0)`, expansion along it gives three times the permanent of a
`2 x 2` matrix with row and column sums three, hence at least `3*5=15`.  If a
row has type `(1,1,1)`, write the next row as `(a,b,c)`; the last is
`(2-a,2-b,2-c)`, with `a+b+c=3`, and direct expansion gives

```text
per(N)=12-2(ab+ac+bc)>=6.                            (28)
```

In the remaining case every row has type `(2,1,0)`.  Column sums force every
column to have the same type, so the positions of the twos and ones are two
disjoint permutation matrices.  After row and column permutations,
`N=2I+P` for a three-cycle permutation matrix `P`, and `per(N)=9`.  This
proves the lower bound and the theorem.  QED.

The bound six is sharp.  A Latin monomial permutation `H` with count matrix
`N` equal to the all-one matrix has block-permanent rank six.  Its six rows
are the six Latin mixed-colour matchings.  Three diagonal target rows plus a
three-word root line cannot absorb them: when the line is diagonal, one
diagonal row overlaps it and the allowed support has dimension at most five.

The localization can be recorded as the exact dichotomy

```text
rank H<=8;                                              OPEN;
or rank H=9 and one diagonal monomial edge gives (5);  OPEN;

two or three nonzero root--root blocks at rank H=9:    IMPOSSIBLE;
one nonmonomial root--root block at rank H=9:           IMPOSSIBLE;
one off-diagonal monomial block at rank H=9:            IMPOSSIBLE;
invertible monomial joint cross map in the last case:   IMPOSSIBLE;
general nonmonomial joint cross map in the last case:   OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.       (29)
```

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_full_joint_cross_rank_monomial_root_edge_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_full_joint_cross_rank_monomial_root_edge_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_full_joint_cross_rank_monomial_root_edge_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_full_joint_cross_rank_monomial_root_edge_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_full_joint_cross_rank_monomial_root_edge_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_full_joint_cross_rank_monomial_root_edge_localization.py
```

The primary replay builds the shared derivative matrix, checks every pair of
coordinate-monomial root blocks, verifies the sharp intersection dimensions,
constructs exact torus zeros for every two-monomial bilinear support, checks
the six-term grouping (21), checks the GHZ-modulo-line support, and exhausts
the `3 x 3` integer count matrices in (26).  The
independent no-import audit uses `Fraction` row reduction, a separately
written sparse tensor assembly, a different direct two-term torus
construction, its own permutation expansion of (21), and direct monomial
`9 x 9` controls for (27).  Lemmas 1--2 supply the arbitrary-tensor and
arbitrary-support proofs.

## Dependencies

- [`BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md`](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_ANNIHILATOR_COMPONENT_TRICHOTOMY_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_ANNIHILATOR_COMPONENT_TRICHOTOMY_THEOREM.md)
- [`SIX_VERTEX_CERTIFICATE.md`](../finite/n06/SIX_VERTEX_CERTIFICATE.md)
