# Four-regular balanced-bridge obstruction

## Status

This is an arbitrary-order impossibility theorem for the 4-regular branch
of the simultaneous three-colour balanced all-bridge normal form.  It
strictly closes the degree-four boundary left open in
`THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md`.

It does not prove the full Krenn--Gu conjecture: a hypothetical minimal
counterexample is 4-connected, hence has minimum degree at least four,
but vertices of degree at least five and the deeper-blocker branches
remain.

## Theorem

There is no Krenn--Gu witness on an even number `n >= 6` of vertices
satisfying all of the following conditions:

1. all three colours lie simultaneously in the balanced all-bridge
   boundary;
2. the support skeleton is 4-regular; and
3. the four incident support edges at every vertex are the three forced
   primary killer edges and the common diagonal-anchor edge supplied by
   that boundary.

Equivalently, the 4-regular normal form consisting of a diagonal-anchor
perfect matching and a cubic reciprocal-singleton subgraph cannot realize
the three-colour GHZ perfect-matching tensor.

## Local ports at an anchor pair

Write the normal type at a vertex as

```text
f = (f(0),f(1),f(2)),  f(c) != c.
```

Its anchor partner has the complementary type

```text
bar(f)(c) = the third colour outside {c,f(c)}.
```

The primary killer for target colour `c` at the first endpoint is the
singleton matrix entry

```text
(local colour, target colour) = (f(c),c).
```

Reciprocity makes the same edge a primary singleton at its other endpoint.
Across the two endpoints of one complementary anchor pair, the six
primary edges therefore have exactly the six directed labels

```text
0->1, 0->2, 1->0, 1->2, 2->0, 2->1,
```

where `a->c` means local colour `a` and target colour `c`.  Every
singleton edge joins opposite labels

```text
a->c  with  c->a,
```

so its endpoint colours are different.

Suppose both vertices of an anchor pair are assigned the same colour `d`
and their anchor edge is not used.  They must then use the two outgoing
ports

```text
d->a and d->b,  {a,b}={0,1,2} minus {d}.
```

This is possible only when those ports lie at different physical
endpoints.  Call their pairing the colour-`d` transition of the anchor
pair.  Direct substitution into the eight normal types gives:

- the two cyclic types have all three transitions;
- each of the other six types has exactly one transition.

Whenever it exists, a colour transition is unique.

## Contracted alternating-cycle model

Let `A` be the diagonal-anchor perfect matching and contract its
`m=n/2` edges.  Keep the six directed singleton ports at every contracted
pair.  Reciprocal singleton edges perfectly pair opposite ports, while
each usable pair-constant colour supplies one internal transition.

The union of singleton edges and all usable transitions has maximum
degree two.  Its cyclic components alternate between singleton edges and
transitions.  Along every such cycle, consecutive transition colours are
different because a singleton joins opposite directed labels with
different local colours.

For a pair-colouring

```text
g : {anchor pairs} -> {0,1,2},
```

a cycle is compatible when its transition at every visited pair has
colour `g`.  If a component revisits one pair with different transition
colours, it is compatible with no pair-colouring.

The key equivalence is:

> A perfect matching other than `A` supports the vertex colouring that is
> constant with value `g(q)` on each anchor pair `q` if and only if the
> contracted port graph contains at least one compatible alternating
> cycle.

Indeed, the symmetric difference of any two perfect matchings is a
disjoint union of alternating cycles.  Conversely, toggling any compatible
cycle against `A` gives another perfect matching with exactly the stated
local colours.

## Single-defect cycle lemma

Fix a background colour `d`.  There are `2m` nonconstant pair-colourings
obtained by choosing one pair `q` and changing only it to one of the two
colours `e != d`.

Any alternating cycle compatible with such a colouring has a proper
cyclic word of transition colours in which exactly one symbol is not
`d`.  Such a word has length two.  For if its length were at least three,
removing the unique non-`d` position would leave two consecutive
`d` positions, contradicting properness.

A compatible length-two cycle for the perturbation `(q,e)` uses:

```text
the e-transition at q,
the d-transition at some other pair r.
```

Each `d`-transition belongs to at most one cyclic component of the
maximum-degree-two port graph.  Hence at most `m` of the `2m`
single-pair perturbations can activate a length-two cycle.  At least `m`
nonconstant perturbations are cycle-free.

This counting is independent of `n`, the normal-type multiplicities, and
the singleton-edge pairing.

## Amplitude contradiction

Choose one of the cycle-free nonconstant pair-colourings `g`.  The anchor
matching `A` supports it, and its contribution is

```text
product over anchor pairs {i,j} of W_ij[g(q),g(q)].
```

Every factor is nonzero because the common anchor edge has all three
diagonal entries nonzero.

The cycle lemma says that no other perfect matching supports this
colouring.  Its amplitude is therefore the displayed single nonzero
monomial.  But the target GHZ tensor assigns amplitude zero to every
nonconstant colouring.  This contradiction proves the theorem.

Notice that no cancellation assumption, genericity condition, or
positivity argument is used.  The obstruction is purely a support theorem:
one explicitly forbidden amplitude has exactly one contributing perfect
matching.

## Audit

Run:

```text
python claims/arbitrary-order/verify_four_regular_balanced_bridge_obstruction.py
python claims/arbitrary-order/audit_four_regular_balanced_bridge_obstruction.py
```

The verifier independently reconstructs:

1. all eight normal types and their complementary anchor partners;
2. all six directed ports at every anchor pair;
3. the transition-count distribution `six types with one, two with three`;
4. the proper-cycle single-defect lemma;
5. all 4,096 contracted order-six configurations obtained from the eight
   oriented types at three anchor pairs and all reciprocal derangements of
   the three unordered colour-port classes.

The finite order-six census is a regression audit of the arbitrary-order
proof, not the source of its generality.  The general step is the
length-two and transition-count argument above.

The second program does not import the first.  It reconstructs the normal
types by a different binary parametrization, builds the actual six-vertex
endpoint multigraph in each contracted configuration, and recursively
enumerates compatible perfect matchings instead of detecting alternating
cycles.  All 73,728 single-pair perturbation checks find the anchor
matching unique.

The outputs

```text
tmp/four_regular_balanced_bridge_obstruction_verified.json
tmp/four_regular_balanced_bridge_obstruction_audited.json
```

must both contain `"verified": true` and
`"global_conjecture_resolved": false`.

## New boundary

The simultaneous balanced all-bridge branch now has no 4-regular witness.
Consequently, any witness that remains in this branch must contain a
vertex of support degree at least five.  In the minimal-counterexample
regime, this is a strict strengthening from minimum degree four to:

```text
minimum degree at least four, with at least one vertex of degree at least five.
```

Every support of maximum degree at most five has now been excluded too.
Its diagonal-support graph would be a union of even paths and cycles with
a spanning complementary-type anchor matching.  Pair-constant two-colour
amplitudes factor into principal hafnians, and the degree-two component
structure forces both factors nonzero for a suitable nonconstant list
colouring.  See
`FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`.  The remaining target
either contains a support vertex of degree at least six or lies in the
deeper double-star blocker branch.
