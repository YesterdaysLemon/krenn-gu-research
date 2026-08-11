# Hostile review of active matrix-unit word-shore synchronization

## Verdict and provenance

**PASS, as an exact active-fibre refinement.**  In a matrix-unit realization
of `Delta_(n,3)`, every mixed coordinate with nonzero aggregate offdiagonal
contribution already has a nonzero pure hafnian on each of its three exact
word shores.  Their union is a word-preserving diagonal matching.

The result is aggregate and fibrewise.  It does not pair each offdiagonal
matching with a diagonal matching of the same weight, prove shore matchings
for a coordinate whose offdiagonal terms sum to zero, or exclude the
remaining scalar cancellation.  A support-minimal `r=1` witness with any
offdiagonal unit has at least one active synchronized fibre, but the theorem
does not turn that fibre into a contradiction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  MATRIX_UNIT_PARITY_FIBRE_DIAGONAL_FACTORIZATION_AND_ACTIVE_WORD_SHORE_SYNCHRONIZATION_THEOREM.md
  verify_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py
  audit_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py
```

The review reconstructed the matching partition and tested the claimed scope
against both six-vertex tables before consulting either implementation.

## 1. The diagonal/offdiagonal partition is exhaustive

For a fixed coordinate word `chi`, every compatible physical perfect
matching either uses only endpoint-equal matrix units or uses at least one
endpoint-unequal unit.  These cases are disjoint and give

```text
[T_W]_chi=D_chi+Q_chi.
```

Here `Q_chi` may contain a mixture of pure and offdiagonal edges; it is
classified by the presence of at least one offdiagonal edge.  No matching is
lost by treating it as an all-cross sector.

An offdiagonal edge cannot induce a constant word, because its two endpoint
labels differ.  Thus every constant coordinate has `Q_chi=0` structurally.

## 2. The shore factorization has multiplicity one

A completely diagonal compatible edge lies wholly inside one colour shore
`V_c`.  Restriction therefore sends a diagonal matching to three disjoint
pure-colour shore matchings.  Conversely their union is a unique global
diagonal matching inducing `chi`.

The bijection is weight preserving and Cartesian, so summing its weights
gives

```text
D_chi=product_c haf(Z^c[V_c]).
```

There is no multinomial coefficient: the vertex shores are labelled and
disjoint, and a global matching has exactly one restriction to each shore.
The empty shore contributes the empty hafnian one; an odd shore contributes
zero.

## 3. Target equality gives the nonzero equivalence

For a mixed word, the corresponding coordinate of `Delta_(n,3)` is zero.
Hence

```text
Q_chi=-D_chi.
```

Over `C`, a finite product is nonzero exactly when every factor is nonzero.
Therefore

```text
Q_chi != 0
  iff D_chi != 0
  iff haf(Z^c[V_c]) != 0 for all c.
```

This step uses a nonzero **weighted** shore hafnian, not merely support.  It
is therefore safe against complex cancellation: a nonzero hafnian certainly
contains a matching monomial, while the existence of a matching does not
conversely guarantee a nonzero hafnian sum.

## 4. The Tutte conclusion has the correct direction

Each nonzero shore hafnian supplies a pure perfect matching.  Tutte's
one-factor inequalities follow from that existence, and the union of the
three shore matchings induces the exact original word.

If one shore fails Tutte, its support has no matching and its hafnian is
zero.  The target identity then forces both `D_chi` and the aggregate
`Q_chi` to vanish.  Compatible offdiagonal matchings may still exist in that
coordinate, but their nonzero terms must cancel internally.

The converse is not asserted.  A zero weighted shore hafnian may arise from
cancellation even when its support satisfies Tutte.  Thus the theorem does
not replace weighted algebra by an unweighted matching criterion.

## 5. Parity is a consequence, not a hidden hypothesis

If any shore has odd cardinality, the diagonal factor is zero.  Every active
mixed fibre therefore has all three shore sizes even, i.e. colour-count
parity `000`.

The theorem does not claim synchronization in the `110`, `101`, or `011`
matching-parity sectors.  Their aggregate offdiagonal coordinates are zero
under the target equality, exactly as the upstream cross-parity projection
requires.

## 6. Support minimality is used only once

The upstream parity-erasure theorem says that a support-minimal matrix-unit
witness with an offdiagonal unit must have nonzero parity-zero offdiagonal
tensor `Q_off`.  Otherwise all offdiagonal blocks could be deleted while
preserving the target, contradicting minimality.

Choosing a nonzero coordinate of `Q_off` and applying the fibre theorem gives
one mixed parity-zero word with

```text
0 != Q_chi=-product_c haf(Z^c[V_c]).
```

No claim is made that every matrix-unit witness is support minimal.  The
usual finite-support minimization supplies such a representative if the
branch is nonempty.  The factorization itself needs neither minimality nor
the bridge/deeper dichotomy.

## 7. The active six-vertex table checks the intended phenomenon

The first exact table has three unique pure matchings, all of weight one.
For

```text
chi=(2,1,0,0,2,1),
```

its compatible graph is an alternating six-cycle with exactly two matchings:

```text
04|15|23  of weight +1, completely diagonal;
01|24|35  of weight -1, offdiagonal.
```

Thus `D_chi=1`, `Q_chi=-1`, and all three two-vertex shores have hafnian one.
The example also has an explicitly unique different mixed coefficient, so it
is not a witness.  It audits active-fibre cancellation without purporting to
construct a counterexample.

## 8. The zero-fibre table preserves the earlier sharp boundary

In the binary-square sharpness gadget, the word `(a,a,b,b,b,b)` has exactly
two compatible offdiagonal matchings of weights `+1,-1` and no diagonal
matching.  Hence

```text
D_chi=Q_chi=0.
```

The pure-`a` graph on the two `a` positions is edgeless, so the empty Tutte
separator leaves two odd components.  This is not a counterexample to the
new theorem: the offdiagonal fibre is zero.  It proves that one cannot erase
the qualifier "active" or infer shore matching from the existence of an
individual compatible term.

The gadget still realizes only one pure tensor, not ternary GHZ.

## 9. Computational independence

The primary checker uses direct recursive perfect-matching enumeration and
principal hafnian recursion.  It checks every word in independent complete
tables at orders six and eight, then replays both six-vertex fibres.

The no-import audit uses least-set-bit matching enumeration, a separate
bitmask hafnian, different deterministic tables at orders four, six, and
eight, and reconstructs the active example from a one-factorization of
`K_6`.  It also enumerates every Tutte separator in the active two-vertex
shores and the failed zero-fibre shore.

These checks cover signs, endpoint ordering, empty/odd hafnians, and sector
membership.  The arbitrary-order result is the written matching bijection
and target-coordinate equality.

## 10. Accepted proof-topology update

```text
active offdiagonal fibre has word-shore hafnians !=0: PROVED;
active fibre has exact word-preserving rematching:    PROVED;
Tutte failure in a nonzero Q_off coordinate:          IMPOSSIBLE;
internally zero offdiagonal fibres may fail Tutte:     TRUE;
support-minimal offdiagonal witness has active fibre:  PROVED upstream+here;
individual termwise weight-preserving normalization:  NOT PROVED;
nonzero D_chi+Q_chi cancellation is impossible:       UNKNOWN;
r=1 matrix-unit witness exclusion:                    UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

The live word-shore node is therefore no longer "force Tutte on every
matching-induced word."  The exact positive rematching exists on every
coordinate that matters to `Q_off` as a tensor.  The residual task is to
exclude or exploit the nonzero aggregate identity, while zero fibres remain
irrelevant to the value of `Q_off` unless their shared physical edges affect
other active coordinates.

## Strongest fresh-referee objection

The dangerous inference is to replace `Q_chi!=0` by "there exists an
offdiagonal matching inducing `chi`."  The binary-square gadget refutes that
replacement: two nonzero compatible terms cancel to `Q_chi=0` and the shore
fails Tutte.  The theorem is accepted because every synchronization claim is
conditioned on the **aggregate coordinate** being nonzero and because it
retains internally cancelling fibres as a separate support phenomenon.
