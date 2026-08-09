# Matching-fork cancellation transport

## Exact claim

Let an even-order, three-colour equality support consist of:

- full nonzero `3 x 3` blocks on a spanning 2-factor `F`;
- diagonal nonzero singleton blocks on three pairwise edge-disjoint
  colour-labelled perfect matchings `S0,S1,S2`.

Write `S=S0 union S1 union S2`.  Let `U` be any matching contained in `S`
and let `f=xz` be an edge of `U`.  Suppose:

1. `PM(F union (U-{f}))` is a nonempty family `A`;
2. `PM(F union U) = A union {Q}` for one additional perfect matching `Q`;
3. every matching in `A` pairs `x` with the same vertex `y`;
4. `xy` is a full edge in `F`;
5. the rich colouring constructed below is nonmonochromatic.

Then the support cannot realize the Krenn--Gu target over any field.

This is an arbitrary-order analytic criterion.  It does not assert that
every equality support contains such a fork.

## Adjacent exact-activation lemma

Let the singleton colour of `f` be `c`, and call the other two colours
`p,q`.

1. Precolour both endpoints of every edge in `U-{f}` by that edge's
   singleton colour.
2. Colour `z` by `c`.
3. On all still-uncoloured vertices, properly 2-colour the induced graph
   `(Sp union Sq)` using colours `p,q`.

The third step is always possible: the union of two edge-disjoint perfect
matchings is a disjoint union of even cycles, and every induced subgraph is
bipartite.

Call the resulting colouring `b`.  It activates exactly `U-{f}`:

- a precoloured target edge is active;
- a non-target edge with a precoloured endpoint has the wrong colour at
  that endpoint;
- a non-target `p`- or `q`-edge with two uncoloured endpoints has
  differently coloured endpoints;
- `f` is inactive because `b(x)` is `p` or `q`, while `b(z)=c`.

Now change only `x` to colour `c`, obtaining `a`.  This activates `f` and
no other singleton edge.  Hence `a` activates exactly `U`.

## Cancellation contradiction

The active perfect matchings at `b` are exactly `A`, while those at `a`
are exactly `A union {Q}`.  Both colourings are forbidden by condition 5,
so both amplitudes must vanish.

Every matching in `A` contains the same full edge `xy`.  Between `b` and
`a`, all of its factors except the entry on `xy` stay fixed.  Since the
whole `xy` block is supported, its old and new entries are nonzero.
Consequently there is one common nonzero ratio `r` such that

```text
sum_(M in A) monomial_M(a)
  = r * sum_(M in A) monomial_M(b)
  = 0.
```

The forbidden equation at `a` therefore reduces to

```text
monomial_Q(a) = 0.
```

Every factor of that monomial is a supported nonzero entry, a
contradiction.

## Order-14 adversarial certificates

`certify_fourteen_vertex_matching_fork.py` searches only the skeleton
perfect matchings and constructs the two adjacent colourings.  It does not
scan the `3^14` colour cube.  Four increasingly adversarial
`C3+C4+C7` supports all contain a two-to-three matching fork:

```text
candidate                                      skeleton PMs  sparse -> rich
no canonical three-extension candidate                 248       2 -> 3
100,000-prefix direct-free candidate                    254       2 -> 3
200,000-prefix direct-free candidate                    260       2 -> 3
500,000-prefix best candidate                           236       2 -> 3
```

The last support reduced the broader direct-Laurent search score to two
relation signatures, but the matching-fork certificate still appears
without any colour-cube scan.

Independent replay is performed by
`verify_fourteen_vertex_cancellation_transport.py`.  It independently:

- reconstructs the singleton factors and skeleton;
- enumerates all perfect matchings using a separate bitmask recursion;
- decodes both base-three colourings;
- recomputes both exact active-matching sets;
- checks the one-vertex difference, common full edge, singleton target,
  removed edge, and nonmonochromaticity;
- checks that the rich activity is the sparse activity plus one supported
  matching.

Pinned verified manifests:

```text
tmp/fourteen_vertex_matching_fork_no_three_extension_verified.json
tmp/fourteen_vertex_matching_fork_p100000_verified.json
tmp/fourteen_vertex_matching_fork_p200000_verified.json
tmp/fourteen_vertex_matching_fork_p500000_multiswitch_verified.json
```

Every manifest contains `"verified": true`.

## Full `C3+C4+C7` consequence

The matching-fork lemma now participates in a complete exhaustion of the
order-14 `C3+C4+C7` equality family.  Starting from all 44,226 possible
singleton colour factors, a catalogue of 168 two-edge one-term sets and
4,368 matching-fork triples leaves zero compatible three-colour supports.
The independent replay is documented in
[`FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md`](claims/finite/n14/FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md).

## `C3+C5+C6` consequence and boundary

For the order-14 `C3+C5+C6` family, the same lemma supplies exact
catalogues of 5,310 size-3 forks, 73,350 size-4 forks, and 160,920 size-5
forks.  Together with 270 two-edge one-term sets, these reduce the complete
family to 156 ordered supports in nine symmetry orbits.

Unlike `C3+C4+C7`, matching forks alone do not finish this factor type.
Each of the nine residual orbits is instead closed by an independently
replayed three-relation signed-lattice contradiction.  The complete finite
theorem is documented in
[`FOURTEEN_VERTEX_C3_C5_C6_FAMILY_CERTIFICATE.md`](claims/finite/n14/FOURTEEN_VERTEX_C3_C5_C6_FAMILY_CERTIFICATE.md).

The arbitrary-order boundary remains open: it is not proved that every
mixed or all-even equality support contains a one-term obstruction, a
matching fork, or a more general factor-lattice obstruction.
