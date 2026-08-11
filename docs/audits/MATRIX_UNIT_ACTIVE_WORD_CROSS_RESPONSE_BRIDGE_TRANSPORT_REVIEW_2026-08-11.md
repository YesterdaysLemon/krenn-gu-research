# Hostile review of the active-word cross response and bridge transport

## Verdict and provenance

**PASS, as an exact trichotomy and finite-holonomy boundary.**  Every active
mixed matrix-unit word has a normalized cross-matching response with nonzero
shore-hafnian denominators.  At least one offdiagonal cross matching has
nonzero pure deletion cofactors on all three shores.  Applying the imported
square/hexagon bridge alternative to that physical term yields one of:

- the existing deeper component;
- transport to another active word with the same colour multiplicities; or
- a weighted pure-shore cancellation despite nonempty matching support.

If the first and third exits never occur, finite iteration gives a nontrivial
cycle of active words.  This does not exclude that cycle or the exit strata,
and it supplies no odd signed-product contradiction.  The `r=1` branch and
global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  MATRIX_UNIT_ACTIVE_WORD_FIBRE_CROSS_MATCHING_RESPONSE_AND_BRIDGE_TRANSPORT_TRICHOTOMY.md
  verify_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py
  audit_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py
```

The review reconstructed the matching bijection and bridge partition before
comparing the primary and no-import implementations.

## 1. The response indexes the exact offdiagonal edge set

Fix an active word `chi`.  Any compatible perfect matching has a unique set
`E` of endpoint-unequal edges.  Every edge outside `E` is endpoint-equal and
compatible with `chi`, hence is pure of colour `c` inside one residual shore
`V_c-partial_c E`.

Conversely, a matching `E` in the compatible cross graph and three residual
pure matchings reconstruct one global matching.  Because `E` is the exact
offdiagonal set, the correspondence neither counts the same matching under a
proper subset of `E` nor omits matchings containing both pure and offdiagonal
edges.  This verifies

```text
Q_chi=sum_(empty != E)
  lambda(E) product_c haf(Z^c[V_c-partial_c E]).
```

There is no exponential/logarithmic formal-series interpretation and no
orientation factorial.

## 2. Normalization is legal only on an active fibre

The preceding parity-fibre theorem gives

```text
Q_chi=-product_c haf(Z^c[V_c]) != 0.
```

Thus each denominator in the normalized response is nonzero.  The proof does
not divide by a shore hafnian for an aggregate-zero fibre.  Empty shores use
hafnian one, while an odd shore would have hafnian zero and therefore cannot
occur in an active fibre.

The normalized equation is a sum equal to `-1`; its summands are not asserted
to be units, independent variables, or binomial ratios.

## 3. A cofactor-active core really exists

All physical matrix-unit weights are nonzero.  Since the unnormalized sum is
nonzero, at least one summand is nonzero, forcing every residual pure hafnian
in that summand to be nonzero.

Choosing one matching monomial from each residual hafnian and adjoining `E`
gives an actual nonzero physical perfect matching inducing `chi`.  This is
important: the later bridge step is applied to a matching term, not to a
formal aggregate or to a support pattern lacking a completion.

The theorem does not claim that every cross matching is cofactor-active.

## 4. The cross-count parity is complete

Write `x_ab` for the number of `E` edges between shores `a,b`.  Original and
residual shore sizes are even, so

```text
x_01+x_02 = x_01+x_12 = x_02+x_12 = 0 mod 2.
```

These equations force all three counts to have the same parity.  If even,
each type pairs into binary blocks.  If odd, removing one edge of every type
leaves three even counts, giving one ternary block plus binary pairs.

Because `E` is a matching, all selected endpoints are distinct; the block
partition cannot reuse a primary killer or create overlapping bridge edges.

## 5. The imported bridge alternative is scoped honestly

For each binary pair or ternary triad, the upstream theorem gives either its
deeper component or the specified nonzero pure bridge units.  The new theorem
does not decide the deeper alternative or claim a uniform blocker pair across
its component.

When every selected block takes the bridge alternative, their endpoint sets
are disjoint.  Their forced pure edges therefore form a perfect matching on
`partial E`.  The square swaps the two endpoint colours in pairs; the hexagon
changes every endpoint and preserves two occurrences of every colour.  Thus
the new word differs from `chi` while retaining exactly the same three colour
multiplicities.

No relation between the scalar weights of the original cross edges and the
forced bridge edges is imported.  Only nonzero support and labels are used.

## 6. The transport/pure-cancellation split is exhaustive

Nonzero residual pure matchings combined with the forced bridges give one
nonzero diagonal matching for the transported word `chi_E`.  The diagonal
aggregate factors as the product of its three new shore hafnians.

- If that product is nonzero, `chi_E` is still mixed and target equality makes
  its offdiagonal aggregate the nonzero negative product.  This is transport.
- If the product is zero, at least one new shore hafnian vanishes.  The
  constructed diagonal matching restricts to a nonzero term in that shore,
  so at least one other nonzero pure matching term cancels it.  This is a
  genuine weighted cancellation, not a Tutte failure.

The theorem does not infer that all three shore sums vanish or select a
unique alternating cycle inside the cancelling shore.

## 7. Finite iteration proves a cycle, not a contradiction

Transport preserves a fixed colour-multiplicity vector and changes a
nonempty endpoint set.  Only finitely many coordinate words have those
multiplicities.  Repeated transport without an exit must therefore revisit a
word, and no arrow is a self-loop; a directed cycle of length at least two
follows.

Each transition arose from a **sum** of response terms and a choice of one
nonzero term.  Multiplying transitions around the cycle does not telescope to
`1=(-1)^m`.  An odd signed-gain contradiction would require additional
binomiality or ratio synchronization not proved here.

## 8. Computational independence

The primary checker:

- compares the cross-set response with complete matching coefficients on all
  six-vertex words and a bounded eight-vertex collection;
- reconstructs the active `111` ternary core;
- exhausts 53 parity-valid cross-count triples through count five with an
  endpoint-level square/hexagon normalization; and
- checks separate nonzero-transport and two-term pure-cancellation charts.

The independent audit imports no primary code.  It uses least-set-bit perfect
matchings, a residual-vertex partial-cross recursion, different exact tables,
an independently reconstructed one-factor active core, population-only bridge
accounting through count six, a different cancelling shore, and a three-word
finite-cycle ledger.

These checks audit indexing, multiplicities, signs, parity, and the two exit
modes.  The arbitrary-order result is the written exact-set partition,
nonzero-summand argument, imported bridge alternative, and finite iteration.

## 9. Accepted proof-topology update

```text
active normalized cross-matching response:             PROVED;
cofactor-active cross core:                            PROVED;
square/hexagon partition of that core:                 PROVED;
deeper or active transport or pure-shore cancellation: PROVED;
no-exit iteration yields active-word cycle:             PROVED;
pure-shore cancellation excluded:                       UNKNOWN;
active-word holonomy cycle excluded:                    UNKNOWN;
deeper component excluded:                              UNKNOWN;
r=1 matrix-unit branch excluded:                        UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The new result replaces one opaque scalar cancellation by three precise live
exits.  It does not close any of them or change the global status.

## Strongest fresh-referee objection

The tempting overstatement is to treat a cofactor-active response summand as
the whole coordinate and then multiply its ratio around the transport cycle.
Other response summands can contribute, and the bridge scalars are not tied
to the cross scalars.  The theorem is accepted because it uses one nonzero
summand only to construct a physical matching and transport word, and it
records the resulting cycle as a boundary rather than as a sign
contradiction.
