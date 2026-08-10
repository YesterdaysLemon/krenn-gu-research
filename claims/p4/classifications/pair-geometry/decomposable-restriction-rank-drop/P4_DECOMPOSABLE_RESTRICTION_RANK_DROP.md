# Rank-drop theorem for decomposable restrictions of `P_4`

## Status

This is an exact tensor theorem over `C`.

Let

```text
L_i : C^4 -> W_i,   i=0,1,2,3,
```

be linear maps of rank at least two.  If

```text
(L_0 tensor L_1 tensor L_2 tensor L_3) P_4
```

is a nonzero decomposable tensor, then at least two of the four maps
have rank exactly two.  Equivalently, at most two local maps can have
rank three.

The theorem supplies a new structural reduction for the two rare
deleted-`P_4` slices in `q5_311`.  It does not yet exclude that branch,
`P_5 -> Delta_3`, or the arbitrary-order Krenn--Gu conjecture.

The rank-two conclusion is sharp.  The exact five-parameter family in
[`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](../decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md)
has all four local maps of rank two and maps `P_4` to a nonzero pure
tensor.  Thus the simultaneous compatibility of the two rare deletions,
not either deletion alone, is the remaining source of a contradiction.

## Pair images

Dually, regard the image of `L_i^*` as a subspace

```text
U_i subset C^4.
```

If `L_i` has rank three, then `U_i` is a hyperplane `a_i^perp`.
Let `E` be the six-dimensional space indexed by unordered pairs of
source coordinates.  For subspaces `U,V subset C^4`, put

```text
A(U,V)
  = span{(u[p]v[q]+u[q]v[p])_(p<q) : u in U, v in V}
    subset E.                                           (1)
```

The `ij|kl` flattening of `P_4` is the complement pairing between
`A(U_i,U_j)` and `A(U_k,U_l)`.  This pairing is nondegenerate on `E`,
so its restricted rank is at least

```text
dim A(U_i,U_j) + dim A(U_k,U_l) - 6.                   (2)
```

The hyperplane-pair classification from the fourth-order permanent
subrank theorem says:

```text
dim A(a^perp,b^perp) >= 5                 if a,b are independent,
dim A(a^perp,a^perp) = |supp(a)| + 2.                  (3)
```

Consequently a pair of hyperplanes has pair-image dimension at most
four exactly when the hyperplanes are equal and their common normal
has coordinate support at most two.

We also need one small extension.

**Hyperplane--plane bound.** If `dim(U)=3` and `dim(V)>=2`, then

```text
dim A(U,V) >= 3.                                       (4)
```

To prove (4), fix nonzero `v in V` and consider

```text
T_v(u) = (u[p]v[q]+u[q]v[p])_(p<q).
```

If `v` has at least three nonzero coordinates, the equations `T_v(u)=0`
force `u=0`, so `T_v` is injective and its image of `U` has dimension
three.  If `V` contains no such vector, every vector in the
two-dimensional space `V` has support at most two.  A generic linear
combination of a basis then shows that `V` must be one coordinate
two-plane, say `span(e_p,e_q)`.  The images `T_(e_p)(U)` and
`T_(e_q)(U)` each have dimension at least two.  They lie in the two
coordinate stars of `E`, whose intersection is only the line indexed
by `{p,q}`.  Their sum therefore has dimension at least three.  This
proves (4).

## Proof of the theorem

Suppose for a contradiction that three maps have rank three.  Relabel
them as `L_0,L_1,L_2`; the fourth map still has rank at least two.

The target tensor is nonzero and decomposable, so each of its three
`2|2` flattenings has rank one.  Apply (2) to the partition

```text
ij | k3,   {i,j,k}={0,1,2}.
```

By (4), the `k3` pair image has dimension at least three.  Rank one in
(2) therefore forces

```text
dim A(U_i,U_j) <= 4.
```

Using (3) for all three pairs among `U_0,U_1,U_2`, the three
hyperplanes are equal:

```text
U_0=U_1=U_2=a^perp,    |supp(a)|<=2.                  (5)
```

It remains to inspect the fourth-mode slice space.

If `|supp(a)|=1`, normalize `a=e_0`.  The first three modes omit source
coordinate zero, so every surviving permanent term assigns coordinate
zero to the fourth mode.  The other three factors form `P_3`.
Therefore the nonzero fourth-mode slice space is spanned by `P_3`,
whose one-mode flattening has rank three.  It contains no nonzero
decomposable tensor.

If `|supp(a)|=2`, diagonal rescaling and a coordinate permutation
normalize

```text
a=(1,1,0,0),   a^perp={x:x[0]+x[1]=0}.
```

Writing a vector in this hyperplane as `(-l,l,m,n)`, the four
fourth-mode slices are proportional to

```text
lmn, -lmn, -l^2 n, -l^2 m.                            (6)
```

Their span is

```text
l * span{mn,ln,lm}.                                    (7)
```

A symmetric decomposable cubic is a cube `q^3`.  If `q^3` lies in
(7), divisibility by `l` forces `q` to be a multiple of `l`, but (7)
contains no nonzero multiple of `l^3`.  Thus this slice space also has
no nonzero decomposable tensor.

In either case, contracting the alleged nonzero decomposable
four-tensor against a fourth-mode covector nonzero on its fourth factor
would produce a nonzero decomposable tensor in the forbidden slice
space.  This contradiction proves that at least two `L_i` have rank
two.

## Consequence for the two rare `q5_311` slices

Let `s_1,s_2` be the two rare source rows in normalized `q5_311`.
For each of the other four local maps, delete row `s_c` and record
whether its rank drops below three.  The rare-slice equations make each
deleted `P_4` restriction a nonzero pure tensor, so the theorem gives

```text
at least two rank drops for deletion s_1,
at least two rank drops for deletion s_2.              (8)
```

There are now only two incidence cases.

1. Some local map loses rank under both deletions.  In that map the
   three rows common to both deletions span one line, and that line
   together with the two rare rows gives a basis of `C^3`.
2. No map loses rank under both deletions.  Then the two rank-drop sets
   are disjoint two-element sets partitioning the four modes.

For the first claim, the four rows remaining after either deletion span
a plane.  If the three common rows spanned a plane, both rare rows
would lie in it, contradicting rank three of the original five-row
map.  Their span is therefore a line; the two rare rows must complete
it to rank three.

This first replaces an unconstrained pair of rank-one `P_4`
compressions by a small rank-drop incidence dichotomy.  The shared case
is subsequently excluded in
[`P5_Q5_311_SHARED_DROP_OBSTRUCTION.md`](../../../../p5/frontier/P5_Q5_311_SHARED_DROP_OBSTRUCTION.md),
and the disjoint `2+2` case is excluded in
[`P5_Q5_311_EXCLUSION_THEOREM.md`](../../../../p5/frontier/P5_Q5_311_EXCLUSION_THEOREM.md).
In particular, the all-rank-two family linked above shows why
simultaneous compatibility was necessary: nonzero pure compression of
one deleted slice is genuinely possible over `C`.

## Verification

Run:

```text
python claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/verify_p4_decomposable_restriction_rank_drop.py
python claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/audit_p4_decomposable_restriction_rank_drop.py
```

The primary verifier reconstructs the pair-image ranks, complement
pairing, support-one `P_3` slice, and support-two cubic obstruction
symbolically.  The independent audit enumerates all 40 hyperplanes and
130 planes in `F_3^4`.  It checks the hyperplane--plane bound and all
10,880,000 canonical ordered rank profiles `3333` and `3332`, fixing
the rank-two position by mode symmetry; none has all three `2|2`
flattening ranks equal to one.  The finite-field census audits the
formulas and case boundary; the written proof above is over `C`.
