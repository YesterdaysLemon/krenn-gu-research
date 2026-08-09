# All-odd full-factor one-term theorem

## Exact claim

Let `n >= 8` be even.  Consider a three-colour equality support with:

- `n` full `3 x 3` blocks forming a spanning 2-factor `F`;
- `3n/2` diagonal singleton blocks forming three pairwise edge-disjoint
  perfect matchings `S0,S1,S2`, one per colour.

If every cycle of `F` has odd length, then the support cannot realize the
Krenn--Gu target over the complex numbers.

Unlike the order-8 and order-10 catalogues, this is an arbitrary-order
analytic theorem.  It does not cover a 2-factor containing both odd and
even cycles, an all-even 2-factor, supports below the equality boundary, or
the global conjecture.

## Lemma 1: the singleton graph has a mixed-colour perfect matching

Let `S=S0 union S1 union S2`.  It is a simple cubic graph.

If `S` is disconnected, choose `S0` on one connected component and `S1`
on another.  Their union across components is a perfect matching using at
least two singleton colours.

Suppose `S` is connected.  It is bridgeless.  Indeed, deleting a bridge of
a cubic graph leaves two odd-order components, so that bridge belongs to
every perfect matching.  This is impossible because `S0,S1,S2` are
pairwise edge-disjoint perfect matchings.

Král, Sereni, and Stiebitz proved that every `n`-vertex bridgeless cubic
graph has at least `n/2` perfect matchings:

<https://doi.org/10.1137/080723843>

For `n >= 8`, this gives at least four.  Only three perfect matchings can
use a single singleton colour, namely `S0,S1,S2` themselves.  A fourth
perfect matching therefore uses at least two colours.

## Lemma 2: any singleton matching can be activated exactly

Let `T` be any matching contained in `S`.

1. For every edge of `T` labelled `c`, colour both endpoints `c`.
2. Let `U` be the uncoloured vertices.
3. The induced graph `(S1 union S2)[U]` is bipartite, because `S1 union S2`
   is a disjoint union of even cycles.  Properly 2-colour it with vertex
   colours `1` and `2`.

Now exactly the singleton edges in `T` are active.

- An edge of `S0-T` has no precoloured endpoint of colour `0`, and every
  vertex of `U` has colour `1` or `2`.
- An edge of `S1-T` or `S2-T` with a precoloured endpoint already has the
  wrong colour at that endpoint.
- If both endpoints lie in `U`, their proper 2-colouring prevents them from
  both having the edge's label.

## The one-term construction

Choose a perfect matching `M` of the whole support skeleton that minimizes
the number of singleton edges, and put

```text
T = M intersect S.
```

There are two cases.

### Case 1: `|T| < n/2`

Every odd cycle of `F` meets `T`; otherwise that cycle would have to be
perfectly matched using only its own edges.  Delete the endpoints of `T`
from `F`.  What remains is a disjoint union of paths.  Since `M` matches
each path, every path has even order and consequently has a unique perfect
matching.

Any perfect matching of `F union T` uses a subset of `T`.  A proper subset
would contradict the minimal choice of `M`.  Using all of `T` leaves the
unique path matchings just described.  Thus `M` is the unique perfect
matching of `F union T`.

Lemma 2 supplies a nonmonochromatic colouring that activates exactly `T`.
It is nonmonochromatic because `T` is nonempty, while `|T|<n/2` leaves an
uncoloured vertex whose final colour can be chosen different from the
fixed colour if necessary.  The corresponding forbidden amplitude has
exactly one active matching.

### Case 2: `|T| = n/2`

Then no skeleton perfect matching uses a full edge.  By Lemma 1 choose a
mixed-colour perfect matching `P` in the singleton graph.  Colour every
endpoint by the label of its edge in `P`.  This colouring is
nonmonochromatic and activates exactly `P`.

Any other perfect matching of `F union P` that uses a full edge would use
fewer than `n/2` singleton edges, contradicting minimality.  A perfect
matching using only the edges of `P` must equal `P`.  Hence this forbidden
amplitude is again one-term.

## Contradiction

In either case the sole active monomial is a product of supported entries.
Every supported entry is nonzero, so the product is nonzero.  A forbidden
Krenn--Gu amplitude must equal zero.  This contradiction proves the claim.

## Consequences

The theorem subsumes the finite `C3+C5` order-8 family and the `C3+C7` and
`C5+C5` order-10 families.  It also immediately excludes, for example, the
order-12 full-factor types `C3+C9`, `C5+C7`, and `C3+C3+C3+C3`.

The mixed `C3+C3+C4` order-10 type is not covered by this analytic theorem;
its one-term obstruction remains certified by the exhaustive order-10
audit.

## Finite semantic replay

`verify_odd_full_factor_one_term_mechanism.py` independently applies the
minimum-singleton and exact-activation construction to every
colour-labelled support over a fixed order-8 `C3+C5` factor:

```text
eligible singleton perfect matchings       30
colour-unlabelled factorizations           390
colour-labelled supports                 2,340
verified one-term certificates           2,340
```

All 2,340 supports have minimum singleton count one.  This finite replay is
a check of the construction, not a replacement for the published
arbitrary-order cubic matching bound.

Run:

```text
python verify_odd_full_factor_one_term_mechanism.py
```

Pinned audit:

```text
tmp/odd_full_factor_one_term_mechanism_n8_verified.json
SHA-256
  462fde1f62688298cb81ccd5df392c8168d1e0b69d859908873eb2a3542fd299
```
