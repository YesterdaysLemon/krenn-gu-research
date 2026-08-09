# Three-colour balanced-bridge intersection theorem

## Status

This is an arbitrary-order structural theorem for the simultaneous
all-bridge boundary of the double-star argument.  It is not a proof of the
Krenn--Gu conjecture.  Its purpose is to replace three overlapping families
of bilinear restrictions by one exact, very sparse block classification.

## Setup

Let the colours be `0,1,2`.  For every vertex `i` and colour `c`, choose a
coordinate normal

```text
f_i(c) in {0,1,2} minus {c},
H_i^c = {x : x[f_i(c)] = 0}.
```

This is precisely the normal form left by the balanced all-bridge boundary:
for each fixed `c`, half of the vertices have one of the two complementary
coordinate normals and half have the other.

Suppose that every oriented edge block `W_ij` obeys, for every colour `c`,

```text
x^T W_ij y = lambda_ij^c x[c] y[c]
for all x in H_i^c and y in H_j^c.
```

No compatibility between the three scalars is assumed.

## Theorem

Each endpoint has one of only eight normal types

```text
(f(0),f(1),f(2)) =
100, 101, 120, 121, 200, 201, 220, or 221.
```

For endpoints of types `f_i,f_j`, an entry `W_ij[r,s]` can be nonzero only
when

```text
for every c:
  (r,s) = (c,c), or r = f_i(c), or s = f_j(c).        (1)
```

Consequently:

1. every edge block has at most four potentially nonzero entries;
2. a block can have rank three only when the endpoint types are
   complementary, meaning

   ```text
   f_i(c) != f_j(c) for c=0,1,2;
   ```

3. on every such full-rank type pair, all three diagonal entries are
   allowed and there is at most one additional off-diagonal entry;
4. the two cyclic types `120` and `201` cannot support an edge to another
   vertex of the same type: the simultaneous restrictions force the whole
   block to be zero;
5. for every noncomplementary type pair, the allowed zero pattern has
   structural rank at most two.
6. a permitted primary singleton is automatically reciprocal: if the
   entry

   ```text
   (f_i(c),c)
   ```

   is allowed on `ij`, then

   ```text
   f_j(f_i(c)) = c.
   ```

   Thus the same singleton block, after transposition, is a killer for
   the paired colour at `j`.

Across all 64 ordered endpoint-type pairs, the exact distributions are

```text
allowed entries:  0 on 2 pairs, 2 on 12, 3 on 44, 4 on 6;
structural rank:  0 on 2 pairs, 1 on 12, 2 on 42, 3 on 8.
```

The eight ordered full-rank pairs are

```text
100 <-> 221,
101 <-> 220,
120 <-> 201,
121 <-> 200.
```

The cyclic pair `120 <-> 201` permits only the three diagonal entries.
Each of the other three unordered complementary pairs permits the three
diagonal entries and one oriented off-diagonal entry.

## Proof

Fix `c`.  Both basis vectors `e_r in H_i^c` and `e_s in H_j^c` exactly
when

```text
r != f_i(c),  s != f_j(c).
```

The bridge restriction says that the coefficient of
`x[r]y[s]` on this product of planes vanishes unless `(r,s)=(c,c)`.
This proves condition (1) after intersecting the restrictions for all
three colours.

There are two independent choices for each `f(c)`, hence eight endpoint
types.  Applying (1) to the 64 ordered pairs gives the displayed counts.
For structural rank, enumerate the six possible transversal permutations
of a `3 x 3` zero pattern.  A transversal survives exactly for the eight
ordered complementary pairs.  In those cases direct substitution in (1)
gives all three diagonal positions and at most one off-diagonal position.
Every other pair has no size-three transversal and therefore has
structural rank at most two.  Substitution for `120,120` and `201,201`
leaves no position at all.

For the reciprocal statement, put `a=f_i(c)`.  Apply (1) to the candidate
entry `(a,c)` using colour `a`.  Since `a != c` and `f_i(a) != a`, neither
the diagonal exception nor the left-normal exception is possible.
Therefore the right-normal exception is forced:

```text
f_j(a)=c.
```

The accompanying verifier reconstructs (1), checks transpose consistency,
tests every transversal independently, and records all 64 patterns:

```text
python verify_three_colour_balanced_bridge_intersection.py
python audit_three_colour_balanced_bridge_intersection.py
```

The second program does not import the first.  It rebuilds the types from
three binary choices, restricts all nine matrix units directly to the six
coordinate planes, and compares the complete 64-record table.  Both outputs
must contain

```text
"verified": true
"full_rank_exactly_complementary": true
"allowed_primary_singletons_are_reciprocal": true
"global_conjecture_resolved": false
```

## Consequence and remaining boundary

If all three colours simultaneously remain in the balanced bridge branch,
the hypothetical witness is no longer an arbitrary collection of
`3 x 3` edge blocks.  Every block lies in one of 64 explicit coordinate
patterns, has at most four entries, and every possible rank-three edge
joins complementary vertex types.  In particular, the rank-three-edge
subgraph is a union of four bipartite type-pair graphs, while each cyclic
type is an independent set in the full support skeleton.

This is a strict reduction of the outstanding all-bridge case, but it does
not yet exclude the sparse patterns.  The next analytic step is to combine
this eight-type classification with the diagonal-anchor edges, reciprocal
singleton killers, and the forbidden mixed-colour perfect-matching
amplitudes.

Here “primary singleton” uses the full preceding reduction.  The generic
killer theorem first supplies a chosen nonzero block
`A_i^c transpose(e_c)`.  The balanced all-bridge theorem then makes the
chosen vector `A_i^c` proportional to the coordinate vector
`e_(f_i(c))`, so that this particular block is the singleton
`(f_i(c),c)`.  Condition (1) proves reciprocity once that singleton has
been obtained; condition (1) by itself would only say that the matrix unit
is permitted.

There is already a sharp degree-four corollary.  At a vertex of support
degree four, its three coordinate primary killers use three distinct
neighbours.  None can be a diagonal anchor, so all three colour anchors
must use the sole fourth neighbour.  That block has all three diagonal
entries nonzero.  The classification forces the fourth neighbour to have
the complementary normal type, and the block itself is diagonal.

If the whole support skeleton is 4-regular, these fourth-neighbour edges
form a perfect matching joining complementary types.  Every remaining
edge is one of the three reciprocal off-diagonal singleton killers at
both endpoints.  Hence the support decomposes into a diagonal anchor
perfect matching and a cubic reciprocal-singleton subgraph.

That normal form has now been excluded at every even order.  Contract the
anchor matching and colour each contracted pair constantly.  At least one
nonconstant single-pair perturbation contains no compatible alternating
cycle, so the anchor matching is the unique matching contributing to that
forbidden colouring.  Its product of nonzero diagonal entries cannot
cancel.  The complete argument and its finite regression audit are in
`FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md`.  The remaining simultaneous
all-bridge boundary therefore has a vertex of support degree at least five.

Every support of maximum degree at most five is now excluded as well.  Its
diagonal-support graph would be a union of even paths and cycles with a
spanning complementary-type anchor matching.  Relative to that anchor,
every pair-constant two-colour amplitude factors into principal hafnians.
The degree-two component structure and a two-colour list assignment force
both factors nonzero for some nonconstant colouring, a contradiction.
See `FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`.  A remaining
simultaneous all-bridge witness must contain a support vertex of degree at
least six.  Three chosen monochromatic matchings then obey the bit-flip
laws in `THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md`; the
order-eight exact-degree-six pairwise-disjoint branch is excluded in
`EIGHT_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`; the
overlapping-matching, degree-seven, larger-order, and deeper-blocker
branches remain unresolved.
