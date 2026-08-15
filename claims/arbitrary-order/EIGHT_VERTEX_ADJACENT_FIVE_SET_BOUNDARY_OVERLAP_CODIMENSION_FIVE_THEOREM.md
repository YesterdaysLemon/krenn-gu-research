# Eight-vertex adjacent five-set boundary-overlap codimension-five theorem

## Status

**Exact ternary characteristic-zero necessary condition at eight vertices.**
Let an eight-vertex matching tensor be a concise weighted three-colour
diagonal.  Take two five-vertex sets whose intersection has size four.  The
three-colour boundary roots supplied separately on the two five-sets cannot
be treated as independent, but their shared `K_4` blocks still force a
uniform gain over either five-set alone.

If all fourteen blocks in the union of the two induced `K_5` graphs are
nonzero, their point in `(P^8)^14` lies in a fixed closed incidence envelope,
a finite union of proper images of codimension at least five.  The
corresponding affine envelope,
with whole-zero blocks added as separate codimension-nine branches, also has
codimension at least five.  Pullback to the full `28`-block graph space
preserves that bound.

The proof stratifies the two boundary-root products by their **exact**
projective synchronization set on the common four vertices.  A generic
stratum gives codimension at least six.  The only stratum whose incidence
source can attain the weaker bound five has all four common roots
synchronized and has the same three colour-zero assignments on both
five-sets.  There are `60` such labelled selector-pair strata; selector
nonuniqueness means they are not asserted to be distinct root-support
components.

This theorem does **not** exclude that synchronized residual, prove exact
codimension, use the all-balanced maximal minors, make different adjacent
pairs independent, exclude an eight-vertex witness, or resolve the
Krenn--Gu conjecture.  The global conjecture remains **UNRESOLVED**.

## 1. Two overlapping five-root systems

Work over `C`; equivalently, extend any characteristic-zero base field to an
algebraic closure.  Let

```text
A={0,1,2,3},       S=A disjoint-union {u},
T=A disjoint-union {v},       u!=v,                   (1)
```

inside an eight-vertex set `Omega`.  Every local space `L_i` has dimension
three with target coordinate covectors

```text
e_(i,0)^*, e_(i,1)^*, e_(i,2)^*.                     (2)
```

Suppose the physical matching tensor satisfies

```text
T_W=sum_(c=0)^2 lambda_c tensor_(i in Omega)e_(i,c)^*,
lambda_0 lambda_1 lambda_2 != 0.                      (3)
```

For a five-set `R` write

```text
X_R=product_(i in R) P(L_i),
Z_R=V(W_ij(x_i,x_j):i<j in R).                        (4)
```

The five-root three-colour boundary-incidence theorem proves that `Z_R` is
nonempty and that every point of `Z_R` has at least one zero root coordinate
in each target colour.  Thus one may choose

```text
x in Z_S,       y in Z_T,                             (5)
```

and nonconstant maps

```text
f:{0,1,2}->S,       g:{0,1,2}->T                      (6)
```

such that

```text
e_(f(c),c)^*(x_(f(c)))=0,
e_(g(c),c)^*(y_(g(c)))=0       for c=0,1,2.           (7)
```

A constant selector would kill all three homogeneous coordinates of one
root and is therefore empty.  For fixed `f` and `g`, the two coordinate
products `Y_f^S` and `Y_g^T` defined by (7) both have dimension seven.

Let

```text
E_(S,T)=binom(S,2) union binom(T,2).                   (8)
```

There are fourteen distinct edges: six in the common `K_4`, four incident
to `u`, and four incident to `v`.  On the all-blocks-nonzero locus their
coefficient space is

```text
P_(S,T)=product_({i,j} in E_(S,T))
          P((L_i tensor L_j)^*)
        isomorphic to (P^8)^14,
dim P_(S,T)=112.                                      (9)
```

## 2. Exact synchronization strata

For `i in A` put

```text
F_i=f^(-1)(i),       G_i=g^(-1)(i).                  (10)
```

The `i`-th root factors in `Y_f^S` and `Y_g^T` have dimensions

```text
2-|F_i|       and       2-|G_i|.                     (11)
```

Say that the two roots synchronize at `i` when

```text
[x_i]=[y_i] in P(L_i).                               (12)
```

The synchronized locus is empty if `F_i union G_i` contains all three
colours.  Otherwise it is the coordinate projective space obtained by
vanishing on `F_i union G_i`, of dimension `2-|F_i union G_i|`.  Its
codimension inside the product of the two factors in (11) is therefore

```text
delta_i
 =(2-|F_i|)+(2-|G_i|)-(2-|F_i union G_i|)
 =2-|F_i intersection G_i|.                          (13)
```

Stratify `Y_f^S x Y_g^T` by the **exact** set

```text
R={i in A:[x_i]=[y_i]},       r=|R|.                 (14)
```

Empty strata are discarded.  On a nonempty stratum define

```text
delta_R=sum_(i in R) delta_i,
a_R=sum_(i in R)|F_i intersection G_i|.               (15)
```

Then

```text
delta_R=2r-a_R,                                      (16)
```

and the root stratum has dimension at most `14-delta_R`.

The integer `a_R` is exactly the number of colours `c` for which `f(c)` and
`g(c)` are the same vertex of `R`.  Hence

```text
a_R<=3.                                               (17)
```

When `r=1`, the sharper bound `a_R<=2` holds because both selectors are
nonconstant.

The use of the exact set in (14) is load-bearing.  A closed condition saying
only that synchronization holds on a chosen subset may contain points with
additional synchronized vertices, where the coefficient-fibre rank jumps.

## 3. Rank of the fourteen block constraints

Fix a point of one exact synchronization stratum.  Each of the eight outer
edges `iu` and `iv`, `i in A`, receives one nonzero evaluation equation, so
its `P^8` block factor is cut to a `P^7`.

For a common edge `ij in binom(A,2)`, the two equations are evaluation on

```text
x_i tensor x_j       and       y_i tensor y_j.        (18)
```

Two nonzero decomposable tensors are proportional exactly when both of their
factor lines are proportional.  Consequently the two equations in the
`ij` block have rank one exactly when `i,j in R`, and rank two otherwise.
The total rank of the equations across the fourteen independent block
factors is

```text
8 + binom(r,2) + 2(6-binom(r,2))
 =20-binom(r,2).                                      (19)
```

Equivalently, the projective coefficient fibre has dimension

```text
8*7 + binom(r,2)*7 + (6-binom(r,2))*6
 =92+binom(r,2).                                      (20)
```

Combining (16) and (20), the incidence stratum has dimension at most

```text
14-delta_R + 92+binom(r,2)
 =106+binom(r,2)-delta_R.                             (21)
```

Its projected coefficient image therefore has codimension at least

```text
kappa(r,a_R)
 =112-(106+binom(r,2)-delta_R)
 =6-binom(r,2)+2r-a_R.                                (22)
```

The possible lower bounds are:

| `r` | bound on `a_R` | `kappa(r,a_R)` |
|---:|---:|---:|
| 0 | 0 | at least 6 |
| 1 | 2 | at least 6 |
| 2 | 3 | at least 6 |
| 3 | 3 | at least 6 |
| 4 | 3 | at least 5 |

Thus every exact synchronization stratum has projected codimension at least
five.

The value five in the last row requires `r=4` and `a_R=3`.  Then every
colour is assigned by both selectors to the same common vertex.  In
particular,

```text
f=g:{0,1,2}->A,       f nonconstant,                  (23)
```

and neither selector uses `u` or `v`.  Conversely, each of the

```text
4^3-4=60                                               (24)
```

nonconstant maps in (23), together with synchronization on all of `A`,
gives a nonempty source stratum of dimension

```text
9 root dimensions + 98 coefficient-fibre dimensions =107.  (25)
```

This shows that the elementary incidence-source count genuinely stops at
five.  It does not prove that the projected image has exact codimension five.

## 4. The closed projective envelope

For each nonconstant selector pair `(f,g)`, let `I_(f,g)` be the incidence
inside

```text
Y_f^S x Y_g^T x P_(S,T)                              (26)
```

cut out by all ten `S`-edge evaluations at `x` and all ten `T`-edge
evaluations at `y`.  It is closed.  The finite exact-synchronization
stratification above proves

```text
dim I_(f,g)<=107.                                     (27)
```

Projection to `P_(S,T)` is projective, hence proper, so

```text
D_(f,g)=pr_(P_(S,T))(I_(f,g))                         (28)
```

is closed and has dimension at most `107`.  Therefore

```text
C_(S,T)=union_(f,g nonconstant) D_(f,g)               (29)
```

is a fixed closed subset of `P_(S,T)`, expressed as a finite union of the
proper images (28), and has codimension at least five.

For a tensor (3), choose the two roots in (5), selectors in (6), and let `B`
be the fourteen-block coefficient point.  Every block in the two induced
`K_5` systems vanishes on its selected root pair, so

```text
(x,y,B) in I_(f,g),       B in D_(f,g) subset C_(S,T). (30)
```

This proves the projective necessary condition.

## 5. Affine blocks and the full graph space

Let

```text
A_(S,T)=product_({i,j} in E_(S,T))(L_i tensor L_j)^*
        isomorphic to (C^9)^14,
dim A_(S,T)=126.                                      (31)
```

On the open where all fourteen blocks are nonzero, independent block
projectivization has `(C^*)^14` fibres.  The closure of the inverse image of
`C_(S,T)` therefore has dimension at most

```text
107+14=121.                                           (32)
```

If one whole block is zero, the corresponding coordinate subspace has
codimension nine.  Adding the fourteen such branches gives a fixed closed
affine envelope of codimension at least

```text
min(126-121,9)=5.                                     (33)
```

The projection from the full affine `28`-block graph space to the fourteen
blocks in (31) is surjective and linear.  Pullback preserves codimension, so
the same bound holds in the full graph space for each adjacent pair `(S,T)`.

There are

```text
56*15/2=420                                           (34)
```

unordered pairs of five-sets in eight vertices with four-vertex
intersection.  Every hypothetical witness lies in all `420` pullbacks, but
no independence, transversality, or additive codimension among them is
claimed.

## 6. Proof-topology consequence

The exact status is

```text
one five-set projective envelope:                    CODIMENSION >= 3;
one adjacent five-set pair, all 14 blocks nonzero:  CODIMENSION >= 5;
affine pair envelope with whole-zero blocks:         CODIMENSION >= 5;
only incidence-source bound-five stratum:            FULL K4 SYNC;
all-balanced maximal minors used:                    NO;
independence among the 420 pair pullbacks:           NOT CLAIMED;
eight-vertex witness exclusion:                      OPEN;
all-balanced witness exclusion:                      OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.          (35)
```

The next exact overlap question is the synchronized residual (23): either
intersect it with the balanced maximal-minor and remaining mixed equations,
or compare a third overlapping five-set and prove that its required root
cannot remain compatible.  A second direction is to use the transverse
five-root blocker flags to strengthen (13) on the reduced finite scheme.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py
python -I claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py
python -m py_compile claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py
uv run --with sympy python claims/arbitrary-order/verify_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
python -I claims/arbitrary-order/audit_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
```

The primary enumerates all `120^2=14,400` selector pairs and every feasible
exact synchronization stratum, verifies coordinate-subspace dimensions with
exact SymPy ranks, and checks the projective and affine incidence arithmetic.
The independent no-import audit uses a per-vertex dynamic programme rather
than synchronization masks or symbolic matrices.  Both find `213,648`
feasible exact strata, minimum codimension five, and exactly `60` source
strata attaining that bound.

The arbitrary-field decomposable-tensor lemma, projective incidence
argument, and proper-image dimension bound are the written proof.  The
bounded scripts audit the finite selector stratification and conventions;
they are not an enumeration of the witness locus.

## Dependencies and lineage

- [`EIGHT_VERTEX_FIVE_ROOT_THREE_COLOUR_BOUNDARY_INCIDENCE_CODIMENSION_THREE_THEOREM.md`](EIGHT_VERTEX_FIVE_ROOT_THREE_COLOUR_BOUNDARY_INCIDENCE_CODIMENSION_THREE_THEOREM.md)
- [`MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md`](MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md)
- [`FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md`](FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md)
- [`FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md`](FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md)
