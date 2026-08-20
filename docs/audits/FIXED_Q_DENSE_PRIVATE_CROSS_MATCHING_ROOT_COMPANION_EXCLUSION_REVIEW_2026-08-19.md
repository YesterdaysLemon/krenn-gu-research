# Fixed-Q dense private-cross-matching root-companion exclusion hostile review -- 2026-08-19

## Verdict

**Accepted at the frozen theorem and script hashes below.**  No P0, P1, or
P2 defect remains.  The package proves an exact characteristic-zero
exclusion of one positive-dimensional same-graph integrability subcell inside
the surviving dense `K_4/K_4`, `h!=0` residue of `GLD21`.

The excluded chart uses one common private root-to-port bijection in all
three GHZ colours, with each private edge colour diagonal and nonzero.  The
result does not exclude colour-dependent private permutations, nonprivate
cross arrays, proper-secondary-clique cells, other `F=empty` cells, or any
weighted-permanent branch.  No witness or counterexample was found.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Assumption and quantifier audit

The theorem is pointwise at one fixed fully supported residual contraction.
Its inputs are exactly:

- the `GLD21` dense `K_4/K_4` response-map-zero cell;
- `h!=0`, already proved on that cell;
- four roots and four ports with one common relabelling;
- twelve nonzero private colour-diagonal root-to-port contractions; and
- one physical graph whose root--root and root--residual blocks are shared by
  all coefficient equations.

The common private matching is an explicit additional subcell hypothesis,
not inferred from the pure `G_U(a^4)` slice.  The theorem does not vary the
residual contraction, promote a pointwise support statement to an
uncontracted edge identity, or assume a selector.  The proof is valid over
every characteristic-zero field; it uses only cancellation of displayed
nonzero scalars and the fact that `2!=0`.

## Matching-ledger review

Write the active colours as `c,d` and the dead colour as `a`.  On the common
private chart, a full root-to-port companion has one root word over every
port word.  Replacing one port by one residual endpoint permits a mismatch at
only that one root.  This support statement is immediate from the private
zeros and does not use a generic-rank inference.

For every edge `{i,j}` and active colour `s`, the review replayed the dense
package with the other active colour repeated on `i,j`.  At the root word
which flips both repeated positions to `s`, the `H_Q` companion and all eight
one-`Q` nuisance columns vanish: each permits at most one flip.  The unique
survivor is

```text
K_ij(r,r) tau_k^s tau_l^a W_(r_i,r_j)(s,s).
```

All three prefactors are nonzero, so the active root--root diagonal is zero.
This checks all six edges, both active colours, and both orientations.  No
other root--root edge can enter because the two private complementary ports
force their own roots, leaving exactly `r_i,r_j` to pair internally.

On the matching mixed word `(s,s,r,a)`, the `H_Q` term is `hP`.  Each of the
three active one-`Q` positions is `-hP` by the corresponding Hamming-one
root-tensor equation.  The dead singleton is zero and the only
residual-present pair term uses the active root--root diagonal just proved
zero.  Hence the coefficient is

```text
hP-3hP=-2hP!=0.
```

The target coefficient is zero because both the root and port words are
mixed.  This is the contradiction.  There is no division by a polynomial
which could vanish on an exceptional divisor.

## Same-graph and independence audit

The proof does not merely combine two formal column-space statements.  The
root--root coefficient killed by the opposite repeated-colour package is the
same physical edge coefficient used in the final matching package.  This is
the new integrability interface beyond `GLD21`'s abstract nine-column
absorptions.

The SymPy primary expands the actual ten-vertex perfect-matching tensor.  It
checks a canonical package with arbitrary symbolic private scalars and a
full exact orbit with a rational specialization.  The no-import audit imports
neither SymPy nor the primary.  It uses `Fraction`, a separately implemented
recursive matching sum, different dense shores and private scalars, all `81`
root words on the pure and Hamming-one shells, and all twenty-four oriented
double-flip and final mixed packages.

The two scripts therefore differ in arithmetic route, matching
implementation, and numerical chart.  They agree on the coefficient sign
and multiplicity.  Neither script proves the arbitrary-field cancellation;
that short argument remains the load-bearing written proof.

## Sharpness and remainder

The earlier `GLD21` private construction uses a private matching only in the
dead colour and is not excluded by this theorem.  The common-private
hypothesis in both active colours is essential to localize one-`Q`
companions to a single root position.  The opposite repeated-colour package
is also essential: without it an active root--root diagonal could cancel the
final `-2hP` coefficient.

An exact rational control satisfies the forced dead pure slice and all eight
Hamming-one equations on the common private chart, but its matching
`2+1+1` coefficient is `-2hP`.  This is a detected graph-side coefficient
window, not a witness.  The package neither claims that the remaining dense
integrability locus is proper nor that a colour-dependent matching can be
normalized to a common one.

Still **UNKNOWN**: colour-dependent private permutations; coordinate-free
nonprivate root-to-port arrays; the `h!=0` proper-secondary-clique cells; the
other `F=empty` and pure-absorption cells; legal operator supply; and every
weighted-permanent consequence.

## Frozen evidence

Frozen at base HEAD `403f80db0cc3cf42f205c35fe66bf126550485d2`:

```text
theorem  a1bad30fcf1312c55cf8ae137e015bad215458ded136ab4381d4e1fc533240b2
primary  b607ecf7503fc6d4e10a9306eec79cc11f8e3cbbacfb822599865f6cb976efd2
audit    c9cfbabeb90ecfcde05dbd30aa624281b40bc7a965e76a0112c6af220a8be6b3
```

The focused primary, independent audit, Python compilation, Ruff lint, Ruff
format check, predecessor `GLD21` primary/audit pair, repository validation
floor, and link-idempotence check pass at the reviewed candidate index.
