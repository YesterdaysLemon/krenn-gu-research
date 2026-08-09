# Three-colour diagonal-matching balance theorem

## Status

This is an arbitrary-order structural theorem in the simultaneous
three-colour balanced all-bridge normal form.  It applies without a
support-degree bound.  It does not prove the Krenn--Gu conjecture.

The theorem is the next boundary after
`FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`: the latter excludes
every case whose diagonal-support graph has maximum degree at most two.
Here we describe the exact form of three chosen monochromatic perfect
matchings at the first remaining degree-three diagonal boundary.

## Setup

Use the eight normal types

```text
f(c) in {0,1,2} minus {c}
```

and encode them by bits

```text
b0 = 0 for f(0)=1,  b0 = 1 for f(0)=2,
b1 = 0 for f(1)=0,  b1 = 1 for f(1)=2,
b2 = 0 for f(2)=0,  b2 = 1 for f(2)=1.
```

For each colour `c`, the required all-`c` amplitude is one.  Choose one
nonzero perfect-matching monomial `M_c` from that amplitude.  Every edge
of `M_c` has a nonzero diagonal entry `(c,c)`.

## Theorem

Let `n=2m`.  Across the `n` vertices:

1. each bit `b0,b1,b2` is one at exactly `m` vertices;
2. every edge of `M_0` flips `b1` and `b2`;
3. every edge of `M_1` flips `b0` and `b2`;
4. every edge of `M_2` flips `b0` and `b1`;
5. any edge shared by two of the matchings flips all three bits, hence
   joins complementary normal types and carries both corresponding
   nonzero diagonal entries;
6. relative to any chosen matching `M_a`, every alternating cycle under
   an arbitrary anchor-pair colouring is monochromatic;
7. for every edge `p` of `M_a` and every colour `b != a`, the principal
   hafnian of the colour-`b` diagonal matrix after deleting the endpoints
   of `p` is zero.

Thus, if the three matchings are pairwise edge-disjoint, their union is a
properly three-edge-coloured cubic spanning graph.  A colour-`c` edge
joins types at Hamming distance two or three: it flips the two bits other
than `bc`, while its own bit is free.  The distance-three case is exactly
a complementary-type edge.

## Proof

The balanced all-bridge entry condition says that `(c,c)` can survive
between endpoint types `f,g` only if, for every target `t != c`, at least
one of `f(t),g(t)` equals `c`.

In the bit encoding this becomes

```text
colour 0: not 11 on b1, not 11 on b2,
colour 1: not 11 on b0, not 00 on b2,
colour 2: not 00 on b0, not 00 on b1.                 (1)
```

Consider `b0`.  Every `M_1` edge avoids `11`, so at most one endpoint per
matching edge has `b0=1`; hence the total number of ones is at most `m`.
Every `M_2` edge avoids `00`, so at least one endpoint per matching edge
has `b0=1`; hence the same total is at least `m`.  It is exactly `m`.
Equality forces every edge of both matchings to have one zero and one one
in `b0`.

The identical comparison

```text
b1: M_0 gives the upper bound, M_2 the lower bound,
b2: M_0 gives the upper bound, M_1 the lower bound
```

proves the other two balances and all three flip rules.  If an edge is in
two distinct matchings, the union of their two prescribed bit pairs is
`{b0,b1,b2}`, so the edge flips every bit.  The two endpoint normal types
are complementary.

No positivity or cancellation assumption is used.  The only amplitude
input is that a nonzero finite sum has at least one nonzero monomial.

## Matching-anchor separation and cross cofactors

Orient an edge of `M_a` and record the normal type at each endpoint.  The
flip theorem says it is one of 16 ordered saturated type transitions for
colour `a`.  For a fixed set of vertex colours, use states

```text
(oriented saturated anchor type, outgoing side, pair colour).
```

For a pair of colours there are 64 states and 1,536 allowed directed
transitions.  Exact reconstruction gives only monochromatic strongly
connected components:

```text
anchor colour belongs to the colour pair:
  component sizes 16,16,8,8,8,8

anchor colour is outside the colour pair:
  component sizes 16,16,16,16.
```

Using all three colours gives

```text
96 states,
2,880 directed transitions,
component sizes 16,16,16,16,8,8,8,8,
0 components containing more than one colour.
```

Thus a closed alternating walk can never change pair colour.  As in the
maximum-degree-five theorem, the anchor matching is only a combinatorial
reference and need not support the pair colouring.  Every pair-constant
amplitude therefore factors across all of its colour classes.

Let `p` be an edge of `M_a` and fix `b != a`.  Colour the two endpoints of
`p` by `a` and all remaining `n-2` vertices by `b`.  The target
coefficient is zero.  The factorization gives

```text
0 = W_p[a,a] haf(L^b[V minus endpoints(p)]).
```

The first factor is nonzero by the choice of `M_a`, so

```text
haf(L^b[V minus endpoints(p)]) = 0.                  (2)
```

Equation (2) holds on every edge of each of the two other monochromatic
matchings.  Equivalently, the gradient of the full colour-`b` hafnian
vanishes on those two perfect-matching edge sets, while the full hafnian
itself equals one.

## Pairwise-disjoint cubic boundary

Suppose now that the diagonal-support graph `D` has maximum degree three
and the selected matchings `M_0,M_1,M_2` are pairwise edge-disjoint.
Their three incident edges at every vertex exhaust `D`, so `D` is cubic.

Fix a colour `a` and expand `haf(L^a)=1` at a vertex `v`.  The three
possible diagonal edges are the incident edges of `M_0,M_1,M_2`.
Equation (2) makes the cofactors on the two edges belonging to the other
matchings zero.  Therefore the sole remaining term gives

```text
1 = W_p[a,a] haf(L^a[V minus endpoints(p)])           (3)
```

for the `M_a` edge `p` at `v`.  In particular its own cofactor is
nonzero.  If the same edge had a nonzero diagonal entry `(b,b)` for
`b != a`, colour its anchor pair by `b` and every other `M_a` pair by
`a`.  Full-colour anchor factorization would make that forbidden
amplitude the nonzero product

```text
W_p[b,b] haf(L^a[V minus endpoints(p)]),
```

contradicting the target zero.  Hence every edge of `M_a` carries exactly
one nonzero diagonal colour, namely `a`.  Consequently

```text
support(L^a) = M_a.                                   (4)
```

Finally consider `M_a union M_b`.  It is a disjoint union of alternating
even cycles.  If it had a proper cycle component `C`, colour the `M_a`
anchor pairs of `C` by `b` and all other anchor pairs by `a`.  By (4), the
two factors are the unique products of the `M_b` edges on `C` and the
`M_a` edges outside `C`; both are nonzero.  This again contradicts the
target zero.

Thus every pairwise union

```text
M_0 union M_1,
M_0 union M_2,
M_1 union M_2
```

is one spanning Hamiltonian cycle.  The pairwise-disjoint exact-cubic
diagonal boundary is therefore confined to a cubic perfect
one-factorization, often called a Kotzig graph together with its
distinguished edge colouring.

There is a further block-level collapse.  Fix an edge of `M_a`.  The
cross-cofactor argument has already shown that its two other diagonal
entries vanish.  Intersecting its saturated endpoint transition with the
64 balanced bridge patterns leaves only

```text
the forced nonzero diagonal unit (a,a),
and at most one off-diagonal unit (r,s).               (5)
```

Every permitted off-diagonal unit in (5) is itself reciprocal:

```text
f_i(s)=r,
f_j(r)=s.                                              (6)
```

Indeed, apply the bridge entry criterion first with target `s`.  Because
`r != s` and `f_j(s) != s`, the left-normal exception is forced, giving
`f_i(s)=r`.  Applying it with target `r` then forces the right-normal
exception `f_j(r)=s`.  Equivalently, (5) is an own-colour diagonal
together with at most one port-shaped transition.

The exact local census, for each fixed matching colour, is

```text
2 of the 16 saturated ordered type transitions: diagonal only,
14 of the 16: diagonal plus one possible reciprocal off-diagonal.
```

If the entire support skeleton is exactly 6-regular, the three distinct
coordinate-primary singleton killers at each vertex occupy the three
edges outside `D`.  Incidence counting makes every such edge reciprocal
at both endpoints.  This exact cover pairs *target tasks*: pairing target
`c` at `u` with target `r=f_u(c)` at `v` gives the physical singleton
half-colours `(r,c)`, not `(c,r)`.  The physical unit must also survive
the complete balanced-bridge table; reciprocity alone is not sufficient.
See `RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`.

With this corrected convention, the complete support splits into

```text
D: a cubic perfect one-factorization, at most two units per block;
K: a cubic reciprocal-singleton port graph, one unit per block.
```

Thus this exact-degree-six residual system has at most `9n/2` nonzero
matrix units over its `3n` physical support edges.  The statement is a
sparsity normal form, not yet an arbitrary-order contradiction.

## Positive optional and physical-port potential

The two-unit normal form has a useful monotone grading.  For a vertex of
bit type `(b0,b1,b2)`, define the integer potential of a local colour by

```text
q(0) = 1 - 2 b2,
q(1) = 2 (b2 - b0),
q(2) = 2 (b0 + b1 - 1).                              (7)
```

Equivalently, on the eight normal types:

```text
type   q(0) q(1) q(2)
100      1    0   -2
101     -1    2   -2
120      1    0    0
121     -1    2    0
200      1   -2    0
201     -1    0    0
220      1   -2    2
221     -1    0    2
```

Every saturated colour-`a` diagonal edge `ij` has

```text
q_i(a) + q_j(a) = 0.                                 (8)
```

This follows directly from the flip rules: `q(0)` changes sign when `b2`
flips, `q(1)` changes sign when both `b0,b2` flip, and `q(2)` changes sign
when both `b0,b1` flip.

By contrast, every optional off-diagonal `(r,s)` in (5) has

```text
q_i(r) + q_j(s) > 0.                                 (9)
```

The complete 42-transition value histogram is

```text
potential 1:  6 transitions
potential 2:  4 transitions
potential 3: 22 transitions
potential 4: 10 transitions.
```

The corrected physical primary ports satisfy an additional strict table.
Pair target `c` at `u` with target `r=f_u(c)` at `v`, require
`f_v(r)=c`, and retain the physical unit `(r,c)` only when it survives all
three bridge restrictions.  Across the eight normal types there are 96
reciprocal target-task transitions, 72 admissible physical units, and

```text
q_u(r)+q_v(c) > 0.
```

Their exact value histogram is

```text
potential 1: 24 transitions
potential 2: 16 transitions
potential 3: 24 transitions
potential 4:  8 transitions.                          (10)
```

This closes the branch at every even order.  By Bogdanov's matching
theorem, reported as Theorem 1.7 in
[Chandran--Gajjala--Illickan](https://arxiv.org/abs/2407.00303), the
three differently coloured perfect matchings in `D` force a
nonmonochromatic perfect matching `F` in `D` when `n>4`.  Its forced
own-colour units induce a nonmonochromatic colouring `chi` of total
potential zero.

Every supported unit in the exact-degree-six normal form has
nonnegative potential: forced `D` units have value zero, while optional
`D` and corrected physical `K` units have positive value.  Any monomial
inducing the same `chi` must therefore use only forced `D` units.  The
proper three-edge-colouring makes that matching unique, since colour `c`
at a vertex selects its sole incident `M_c` edge.  Its product is nonzero
but the target coefficient is zero, a contradiction.

The complete proof and two independent local-table audits are in
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.

The former lowest-layer `D/K` path-cycle argument is withdrawn.  It
mistook target-task labels for inherited half-colours and incorrectly
assumed that `c -> f_i(c)` uses every physical colour once.  The corrected
strict port positivity makes that argument unnecessary.

## Independent audits

Run:

```text
python claims/arbitrary-order/verify_three_colour_diagonal_matching_balance.py
python claims/arbitrary-order/audit_three_colour_diagonal_matching_balance.py
python claims/arbitrary-order/verify_arbitrary_order_degree_six_kotzig_port_obstruction.py
python claims/arbitrary-order/audit_arbitrary_order_degree_six_kotzig_port_obstruction.py
```

The primary verifier reconstructs all eight normal types, all 64 ordered
type pairs, and the exact diagonal conditions (1).  For each colour it
checks the 16 saturated ordered transitions: eight distance-two and eight
complementary transitions.  It also constructs all nine 64-state
two-colour and all three 96-state full-colour matching-anchor automata
and checks their exact component sizes.  It records the Laplace/cofactor
reduction from the pairwise-disjoint cubic branch to a perfect
one-factorization, and checks the exact `2+14` effective block census and
reciprocity of every remaining optional off-diagonal unit.  It also
reconstructs (7), checks zero potential on all 48 saturated diagonal
transitions, and checks the positive `1,2,3,4` histogram on all 42
optional transitions.  The two added programs independently reconstruct
the corrected 72-unit physical-port table and its strict histogram (10).

The second program does not import the first.  It tests each diagonal
matrix unit directly on all coordinate-plane restrictions, rebuilds the
bit tables in a separate order, checks every shared-colour intersection,
and recomputes the automata by transitive closure.

Both output records retain

```text
"global_conjecture_resolved": false
```

## New boundary

A remaining simultaneous balanced all-bridge witness has a vertex of
diagonal-support degree at least three and therefore a support vertex of
degree at least six.  At the exact cubic diagonal boundary, the three
chosen monochromatic matchings either overlap on complementary-type edges
or form the rigid bit-flipping cubic graph above.  In either case the
cross-cofactor equations (2) hold.  In the pairwise-disjoint case the
cubic graph is further forced into the Hamiltonian
perfect-one-factorization boundary above.  The corrected physical-port
potential excludes its exact-degree-six realization at every even order;
see `ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.

The next targets are the overlapping-matching branch, support degree at
least seven, and the separate deeper-blocker alternative.
