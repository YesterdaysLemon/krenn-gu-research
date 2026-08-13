# Self-review: two-source exceptional-root-row obstruction

## Claim audited

No S2U full-joint-rank sparse block-permanent solution has its exceptional
root row space contained in the sum of two source summands.

## Scope checks

- The theorem applies only after the exact S2U reduction.
- “Exceptional root” means the root opposite the unique surviving diagonal
  monomial root--root edge.
- The row-space containment is an additional subcase hypothesis.  A row
  space with nonzero projection to all three source summands remains open.
- Joint rank at most eight and all other global branches remain open.

## Adversarial checks

1. **Does a two-source graph couple the two mixed products so they cannot be
   split?**  The initial overgeneralization here was caught by the focused
   replay: the two pure-source planes have splitting rank three, not six.
   Those are handled only by the prior source-aligned theorem.  The other
   eight canonical normal forms have splitting rank six; a pure generator
   kills one term and another generator kills the other, or two independent
   diagonal generators force both to vanish.
2. **Are `P_b,Q_c` independent after concatenation?**  They are the six
   non-exceptional root rows of the invertible `9 x 9` matrix.  Any relation
   among them would already be a row relation of `H`.
3. **Can a mixed vector have two zero divisors in characteristic zero?**  Its
   entire zero-divisor space is one line; the two relevant `P_b` are
   independent.
4. **Can all six pure vectors fit in the six-dimensional `S` summand?**  No:
   the independent exceptional row space also has positive dimension inside
   `S`, so nine independent rows cannot all fit in `S` plus only the unused
   three-space as counted in the proof.  More directly, if all `Q` are in
   `S`, all `P` are in `S`, giving six rows in `S`; together with the three
   exceptional rows in `S`, this puts all nine rows in the six-space `S`.
5. **Does this prove the universal block-permanent rank floor?**  No.  It
   uses the much sharper off-diagonal zero grid and the two-source support
   hypothesis.

## Evidence independence

The primary uses symbolic characteristic-zero ranks and graph identities.
The audit imports neither SymPy nor the verifier: it performs a direct
binary census of the `(6+3)` mixed-product map, enumerates all 1395 binary
three-planes in the two-source six-space (exactly two have splitting rank
three and the other 1393 rank six), and separately checks the purity
patterns.  The arbitrary-field proof is the written rank-one-tensor argument.

## Remaining risk

The full-support chart has three coupled products, and no two-source
projection can be discarded.  The proof here must not be cited as excluding
that chart without a new simultaneous splitting theorem.

Global status remains **UNRESOLVED**.
