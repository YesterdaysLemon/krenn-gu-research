# Self-review: one-deficient involved row with injective third row

Date: 2026-08-13

Claim reviewed:
[one-deficient-involved-row third-row-rank-three complete exclusion](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_RANK_THREE_COMPLETE_EXCLUSION_THEOREM.md).

## Verdict

The new mixed `(2,3,3)` exclusion and its `(3,2,3)` root-exchanged mate are
supported.  Together with the already closed `(2,2,3)` cells, this excludes
every third-row-rank-three profile having a deficient involved row.  The
fully injective `(3,3,3)` profile and all stated lower-row branches remain
open.

## Checks

### One missing row is sufficient

The proof does not import a nonexistent kernel for the injective second row.
Only `r_d=0`, the isolated first contraction of `C`, and `pr_1 K subset
e_d^perp` determine the correction coefficients.  Third-row injectivity
makes the graph lifts over all three third coordinates a basis modulo the
single derivative syzygy.

### The `P_3` rank step transfers exactly

After the first contraction, the two complementary source targets have
their unchanged diagonal root coefficients and the only possible correction
is on `T_d`.  The nonzero-polynomial evaluation and tensor-rank contradiction
are therefore identical to S2BX.  No property of `p_d` is used.

### The binary restriction stays two-dimensional

In the genuinely new case `pi` is injective, so `p_s,p_t` are independent.
Thus restricting the complete table to `R x span(p_s,p_t) x
span(q_s,q_t)` does not collapse a row plane.  The extra row `p_d` is
irrelevant rather than silently set to zero.

### The shifted-plane contradiction is physical-scope safe

The shifts `q_c -> q_c+lambda_c q_d` are changes of basis inside the actual
three-dimensional third-row image.  They are used only in the abstract
binary permanent table; no shifted derivative or new graph is asserted.
Because `q_d` is a common zero on the restricted involved planes, all table
entries are unchanged.

### Root exchange is exact

The shared-factor derivative and polarized permanent are symmetric under
exchanging the first two roots.  The argument uses one deficient involved
row and an injective third row, so it transfers from `(2,3,3)` to `(3,2,3)`
without changing a missing-colour quantifier.

## Verification independence

The primary replay uses SymPy matrices in the order `(q_d,q_s,q_t,h)`.
The no-import audit reverses the abstract row order, uses its own `Fraction`
row reduction, reconstructs all `2 x 3 x 3` table entries, and checks every
rational one- and two-supported shift mask.  The already audited S2BX `P_3`
rank certificate and S2BF binary-frame certificate are explicit
dependencies rather than duplicated scripts masquerading as independence.

## Status boundary

```text
mixed (2,3,3)/(3,2,3):                             IMPOSSIBLE;
any deficient involved row with third rank three:  CLOSED;
fully injective (3,3,3):                            OPEN;
third-row-rank-two mixed/injective profiles:        OPEN;
other cells, components, poles, higher orders:      OPEN;
global Krenn--Gu conjecture:                        UNRESOLVED.
```
