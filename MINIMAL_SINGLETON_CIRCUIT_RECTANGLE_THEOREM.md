# Minimal singleton-circuit rectangle theorem

## Theorem

Let a three-colour equality support have:

- full nonzero blocks on a vertex-disjoint union `F` of even cycles;
- three pairwise edge-disjoint diagonal singleton perfect matchings
  `S0,S1,S2`.

Fix one singleton colour `c`, and let `T` be a nonempty proper subset of
`Sc`.  Assume:

1. `T` is feasible: deleting the endpoints of `T` from `F` leaves a
   perfect matching;
2. no nonempty proper subset of `T` is feasible;
3. `T` touches every cycle of `F`.

If the support realizes the Krenn--Gu target, then on every full cycle
`C` the endpoints `V(T) intersect V(C)` are exactly two adjacent
vertices.

Equivalently, contract every cycle of `F` to one vertex and retain the
edges of `T`.  The result must be a connected 2-regular multigraph:
a single cycle through all components of `F` (with a pair of parallel
edges when `F` has two components).

Thus every proper one-colour minimal feasible set which is not such an
adjacent-port component cycle is an arbitrary-order contradiction.

## Exact activation cube

Call the other two colours `p,q`.  Properly 2-colour `Sp union Sq` with
`p,q`; this is possible because the union of two edge-disjoint perfect
matchings is a disjoint union of even cycles.  Call the resulting vertex
colouring `b`.

For each subset `X subset V(T)`, recolour precisely the vertices in `X`
to `c`, obtaining `b_X`.  Its active singleton set is exactly

```text
T_X = {e in T : both endpoints of e lie in X}.
```

Indeed, every unmodified `Sp`- or `Sq`-edge remains bichromatic, changing
one or both endpoints to `c` cannot activate it, and an `Sc`-edge can be
active only when it is one of the disjoint edges of `T` with both
endpoints changed.

If `X` is a proper subset of `V(T)`, then `T_X` is a proper subset of
`T`.  By minimality it is either empty or infeasible.  Hence the active
perfect matchings at every proper corner are exactly the full-only
matchings of `F`.

At the target corner `X=V(T)`, the active graph is `F union T`.
Every perfect matching using singleton edges uses a feasible subset of
`T`.  Minimality rules out every nonempty proper subset, while touching
every cycle makes the completion using all of `T` unique.  Thus this
corner contains the full-only matchings plus exactly one extra matching.

All corners are nonmonochromatic.  At the target this uses the assumption
`T proper subset Sc`; at the base it follows from the proper `p,q`
2-colouring.

## Local Möbius rectangle

For a full cycle `C`, write its two alternating monomials at a corner
`X` as `A_C(X),B_C(X)`, and let `rho_C(X)` be the Laurent exponent
difference `A_C(X)/B_C(X)`.  It depends only on

```text
D = V(T) intersect V(C)
```

and on `X intersect D`.

At the target corner, the full-only product cannot vanish: the target
amplitude is that product plus one supported nonzero monomial and must
be zero.  In particular every target cycle binomial is nonzero.

Now fix `C`, leave all other cycles at their target colours, and vary
`X intersect D`.  At every proper local corner the global colouring is
a proper corner of the activation cube, so its full-only amplitude is
zero.  All other cycle binomials retain their nonzero target values.
Therefore

```text
A_C(X) + B_C(X) = 0
```

at every proper subset `X proper subset D`, or equivalently the monomial
ratio with exponent `rho_C(X)` is `-1`.

Every full edge of `C` depends on at most its two endpoint bits.
Consequently the full mixed difference

```text
sum_(X subset D) (-1)^(|D|-|X|) rho_C(X)
```

is zero whenever:

- `|D| >= 3`; or
- `|D| = 2` and the two vertices of `D` are nonadjacent on `C`.

Solving this identity for the target exponent expresses it as an integer
combination of the proper-corner exponents whose coefficients sum to
one.  Since every proper-corner ratio is `-1`, the target ratio is also
`-1`.  Hence the target cycle binomial vanishes, contradicting the
nonzero target product.

The feasible-set expansion gives the remaining classification.  A
nonempty feasible deleted set on an even cycle has even cardinality.
Since `T` touches every cycle, the only way to avoid the Möbius
contradiction is therefore:

```text
|V(T) intersect V(C)| = 2
```

with the two vertices adjacent on every `C`.

## Contracted exceptional structure

The two adjacent ports on one cycle cannot be joined to each other by an
edge of `T`, because that edge already belongs to `F` and the singleton
factors are edge-disjoint from `F`.  Thus every edge of `T` joins two
different full-cycle components.  After contraction, every component has
degree two.

If the contracted 2-regular multigraph were disconnected, the edges in
one connected component would be a nonempty proper subset of `T`.
They delete both adjacent ports on every cycle in that component and no
vertices elsewhere, so they would be feasible.  This contradicts the
minimality of `T`.  The contraction is therefore connected, hence a
single component cycle.

## Independent audit

Run:

```text
python verify_minimal_singleton_circuit_rectangle_theorem.py
```

The verifier independently:

- brute-forces every deleted-vertex set on `C4,C6,...,C14`;
- checks the exact path-completion count;
- checks the edge-local Möbius criterion for every feasible set;
- confirms that the only feasible sets escaping the rectangle have two
  adjacent deleted vertices;
- exhausts all loopless pairings of two ports on each of up to six
  contracted components and verifies that positive minimality is
  equivalent to connectedness.

It must write
`tmp/minimal_singleton_circuit_rectangle_theorem_verified.json` with
`"verified": true`.

## Boundary

This theorem does not prove that every equality support contains a
proper one-colour positive-minimal feasible set touching all full cycles.
Nor does it eliminate the adjacent-port component-cycle exception.  It
reduces every such surviving set to that rigid exceptional form; the
remaining global task is to force incompatible component cycles among the
three singleton colours, or to close supports in which no such set
exists.
