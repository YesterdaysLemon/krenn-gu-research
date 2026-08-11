# Matrix-unit active-word cross response and bridge-transport trichotomy

## Status

This is an exact arbitrary-order characteristic-zero refinement of the active
word-shore node in the `r=1` matrix-unit branch.  For any active mixed word
`chi`, the aggregate offdiagonal coefficient has a complete cross-matching
expansion over its exact word shores.  After division by the three nonzero
shore hafnians, the target equation is

```text
-1 = sum_(empty != E matching in X_chi)
       lambda(E) product_c
       haf(Z^c[V_c-partial_c E]) / haf(Z^c[V_c]).     (1)
```

Here `X_chi` is the graph of compatible offdiagonal physical units and
`partial_c E` is the set of their endpoints in the colour-`c` shore.

Consequently at least one cross matching `E` is **cofactor-active**: every
displayed deletion hafnian is nonzero.  Its three cross-type counts have one
common parity.  Absent the imported deeper-blocker alternative, its edges
partition into binary bridge squares and at most one ternary bridge hexagon.
The forced bridge edges form a diagonal matching on `partial E`, change the
word at every such endpoint, and preserve all three colour multiplicities.

Combining those bridges with nonzero residual pure matchings produces a
specific nonzero diagonal matching for a new word `chi_E`.  Exactly one of
the following then occurs:

1. a selected bridge step enters the existing deeper-blocker branch;
2. the diagonal aggregate at `chi_E` is nonzero, so target equality makes
   `chi_E` another active synchronized word; or
3. some pure-shore hafnian at `chi_E` is zero despite containing a nonzero
   matching term, hence has an internal pure alternating-cycle cancellation.

If the first and third exits never occur, repeated transport on the finite
set of words with the same colour multiplicities yields a directed cycle of
length at least two.  This is an exact active-word holonomy boundary, not a
contradiction: excluding the cycle or the pure-shore cancellation exits
remains open.  The `r=1` branch and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Imported active-fibre setting

Let `Omega` have even cardinality `n>=6`, and suppose the complete physical
graph has one nonzero matrix unit on every pair and satisfies

```text
T_W=Delta_(n,3).                                     (2)
```

Fix a mixed word `chi` whose aggregate offdiagonal coefficient `Q_chi` is
nonzero.  Put

```text
V_c={v:chi(v)=c},
h_c(S)=haf(Z^c[S]),
H_chi=product_c h_c(V_c).                            (3)
```

The imported parity-fibre theorem gives

```text
Q_chi=-H_chi !=0.                                   (4)
```

Thus every `|V_c|` is even and every denominator in (1) is nonzero.  Empty
shores use the empty hafnian one.

An edge `uv` belongs to `X_chi` precisely when its two endpoint labels are
`chi(u),chi(v)` and these colours differ.  Write `lambda(E)` for the product
of the nonzero physical edge weights in a matching `E subset X_chi`.

## 2. The exact cross-matching response

### Theorem 1

The aggregate offdiagonal coordinate is

```text
Q_chi = sum_(empty != E matching in X_chi)
          lambda(E) product_c h_c(V_c-partial_c E).  (5)
```

Equation (1) follows from (4).

### Proof

Take any compatible perfect matching contributing to `Q_chi` and let `E` be
its exact set of offdiagonal edges.  Every remaining edge is diagonal and
compatible with `chi`; it is therefore a pure-`c` edge inside one residual
shore `V_c-partial_c E`.

Conversely, a nonempty matching `E` in `X_chi`, together with one pure
perfect matching on each residual shore, reconstructs a unique compatible
perfect matching whose exact offdiagonal set is `E`.  The correspondence is
weight preserving and has no orientation or ordering multiplicity.  Summing
the residual pure matchings gives (5).  Division by the nonzero value
`H_chi` and substitution of (4) give (1).

This is a complete matching partition, not an asymptotic or formal-logarithm
expansion.

### Corollary 2 (cofactor-active cross core)

There exists a nonempty matching `E subset X_chi` such that

```text
h_c(V_c-partial_c E) !=0       for c=0,1,2.          (6)
```

Indeed, the sum (5) is nonzero, so at least one summand is nonzero.  Every
physical weight in `lambda(E)` is nonzero, leaving (6).

Choosing one nonzero matching monomial from each hafnian in (6) and adjoining
`E` gives a physical perfect matching `F_E` inducing `chi`.  Thus the bridge
theorems apply to an actual matching term, not merely to an aggregate.

## 3. Parity and bridge partition of the active core

For `0<=a<b<=2`, let

```text
x_ab=number of E edges between V_a and V_b.          (7)
```

### Lemma 3

The three integers `x_01,x_02,x_12` have the same parity.

### Proof

The nonzero residual hafnian in (6) forces every residual shore to have even
cardinality.  Since each original shore is even,

```text
x_01+x_02 = 0 mod 2,
x_01+x_12 = 0 mod 2,
x_02+x_12 = 0 mod 2.                                (8)
```

These equations say exactly that the three counts have one common parity.

### Corollary 4 (square/hexagon partition)

If the common parity is even, pair the edges of each nonempty cross type; at
least one type supplies a binary pair.  If it is odd, select one edge of each
type for one ternary triad, then pair every remaining type.  Because `E` is a
matching, these blocks have disjoint endpoint sets and partition `E`.

## 4. Bridge normalization and the transport word

Apply the imported bridge-square theorem to every binary block and the
bridge-hexagon theorem to the ternary block, if present.  At any block, the
deeper component may occur.  Suppose it does not.

For two type-`{a,b}` edges, the square replaces them by a pure-`b` edge on
their two `a` endpoints and a pure-`a` edge on their two `b` endpoints.  For
one edge of each type, the hexagon supplies the three crossed pure edges in
the imported theorem.  In both cases:

- the forced edges are nonzero and disjoint;
- every endpoint changes colour; and
- the number of endpoints of each colour is preserved.

Taking the union over all blocks gives a diagonal perfect matching

```text
B(E) on partial E.                                  (9)
```

Define `chi_E` to equal `chi` off `partial E` and to take the pure colour of
the incident edge of `B(E)` on `partial E`.  Then

```text
chi_E != chi,
|chi_E^(-1)(c)|=|V_c| for every c.                  (10)
```

Choose one nonzero pure matching `P_c` represented in each hafnian (6).
The union

```text
B(E) union P_0 union P_1 union P_2                  (11)
```

is a nonzero completely diagonal matching inducing `chi_E`.

### Theorem 5 (bridge-transport trichotomy)

For every active word `chi` and cofactor-active core `E`, at least one of the
following holds:

```text
deeper:       some selected square/hexagon enters the deeper component;
transport:    D_(chi_E) !=0 and Q_(chi_E)=-D_(chi_E) !=0;
pure cancel:  some h_d(chi_E^(-1)(d))=0 despite a nonzero matching term.
                                                               (12)
```

### Proof

If any bridge step takes the deeper alternative, the first case holds.
Otherwise (9)--(11) construct a nonzero diagonal term at `chi_E`.  The exact
diagonal factorization gives

```text
D_(chi_E)=product_c h_c(chi_E^(-1)(c)).              (13)
```

If this product is nonzero, the mixed target coordinate is zero and the
active-fibre theorem gives the transport case.  The transported word is
still mixed because (10) preserves the multiplicity vector of the original
mixed word.

If the product is zero, at least one shore hafnian vanishes.  Matching (11)
restricts to a nonzero term in every new shore.  A vanishing shore sum must
therefore contain at least one further nonzero matching term, producing an
internal pure alternating-cycle cancellation.  This is the third case.

The theorem makes no claim that the scalar weight of `B(E)` equals the weight
of `E`.

## 5. Finite active-word holonomy

### Corollary 6

Start from any active mixed word and, at every active word reached, choose
one cofactor-active core from Corollary 2.  Then either a chosen transition
hits the deeper or pure-cancellation exit in (12), or the process contains a
directed cycle of active words

```text
chi_0 -> chi_1 -> ... -> chi_(m-1) -> chi_0,
m>=2.                                                (14)
```

Every word in (14) has the same three colour multiplicities, and every arrow
changes the word on every endpoint of a cofactor-active cross core.

### Proof

Transport preserves the three multiplicities and changes a nonempty endpoint
set, by (10).  There are only finitely many words with those multiplicities.
If neither exit occurs, iteration stays inside that finite active set and
eventually repeats a word.  No transition is a self-loop, so the resulting
directed cycle has length at least two.

The cycle is a holonomy boundary, not an odd-sign contradiction.  Each arrow
comes from a sum such as (1), not from a single binomial ratio.

## 6. Exact scope and next obstruction

In a support-minimal offdiagonal matrix-unit witness, the imported erasure
theorem and active-fibre theorem supply an initial active word.  The result
here therefore gives the exact no-random-drift continuation:

```text
normalized word-shore cross response:              PROVED;
cofactor-active offdiagonal core exists:            PROVED;
cross counts have square/hexagon parity:            PROVED;
deeper or activity transport or pure cancellation:  PROVED;
no-exit transport gives finite word holonomy:        PROVED;
pure-shore internal cancellation excluded:          UNKNOWN;
active holonomy cycle excluded:                     UNKNOWN;
deeper-blocker branch excluded:                     UNKNOWN;
r=1 matrix-unit branch excluded:                    UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

The result does not assert a uniform blocker pair on a deeper component,
termwise equality of cross and bridge weights, noncancellation of a shore
hafnian merely from its support, or an odd signed cycle.  Any later holonomy
argument must use additional coefficient identities rather than multiplying
the summed equations (1) as though they were binomials.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py
python claims/arbitrary-order/audit_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py claims/arbitrary-order/audit_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py claims/arbitrary-order/audit_matrix_unit_active_word_fibre_cross_matching_response_and_bridge_transport.py
```

The primary verifier checks the complete response partition on every word in
bounded exact tables, reconstructs the active ternary core, and exhausts the
square/hexagon normalization convention for small cross-count triples.  The
independent no-import audit uses a separate bitmask response recursion,
different tables, explicit Tutte/shore cofactors, and independent transport
and finite-cycle ledgers.  These bounded checks audit formulas and examples;
the arbitrary-order theorem is the matching partition, parity argument,
imported bridge alternative, and finite iteration above.
