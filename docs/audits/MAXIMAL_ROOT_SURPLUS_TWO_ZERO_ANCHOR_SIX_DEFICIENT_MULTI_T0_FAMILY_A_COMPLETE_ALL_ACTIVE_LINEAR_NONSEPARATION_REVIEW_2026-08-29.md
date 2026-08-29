# Hostile review: multi-`T_0` Family-A complete all-active linear nonseparation

Date: 2026-08-29

Reviewed package:

- `claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_MULTI_T0_FAMILY_A_COMPLETE_ALL_ACTIVE_LINEAR_NONSEPARATION_THEOREM.md`
- `claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_r2_complete_all_active_linear_nonseparation.py`
- `claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_r3_complete_all_active_linear_nonseparation.py`
- `claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_complete_all_active_linear_nonseparation.py`

## Verdict

**PASS as a scoped exact universal scalar-linear no-go.**

The package proves that no scalar linear combination of all `6,558`
zero-target rows universally separates an `I_2500` monomial from every
nonleak repair monomial in either remaining Family-A chart.  This result is
an identity in the unspecialized physical/source coordinate ring.  It does
not exclude relations appearing on a specialized source-coordinate fibre,
nonlinear coefficient-ideal consequences, activity-localized cells, either
key, or the global conjecture.

Both Family-A keys remain **OPEN**, the six-deficient residual remains
`97,215 / 79`, and Krenn--Gu remains **UNRESOLVED**.

## 1. Target-row correction

All three diagonal words

```text
00000000,       11111111,       22222222
```

have nonzero GHZ targets.  They are excluded from the theorem's row family,
leaving exactly `6,558` zero-target words.  An earlier exploratory count of
`6,559` had omitted `mu_0`; it was rejected before promotion.

The two primary verifiers retain all three target residuals with independent
symbols as an additional diagnostic and find no polynomial-kernel vector
supported on a target column.  That diagnostic is not used to strengthen the
zero-target theorem or to claim a contradiction for fixed target weights.

## 2. Matrix orientation and exact bridge

For each chart, `N` has literal coefficient words as columns and nonleak
monomials as rows.  `L` has the same columns and the monomials containing
`I_2500` as rows.  A universal scalar-linear separator exists exactly when

```text
Na=0,       La!=0.
```

Thus the exact criterion is `ker N subset ker L`, equivalently
`rank N=rank[N;L]`.  The verifiers use right kernels; there is no transpose
or row/column inversion.

The component graph joins two literal columns when they share a nonleak
monomial.  This makes `N` block diagonal and its kernel the direct sum of the
component kernels.  Checking the stacked-rank equality in every component is
therefore a proved bridge to the global statement.

## 3. Exact reproduced census

The three retained computations agree on

| chart | components by size | leak components by size | total nullity | leak nullity sum/max | `rank N=rank[N;L]` |
|---|---|---|---:|---:|---:|
| `RTT` | `728 x 1`, `1,458 x 2`, `2 x 3`, `727 x 4` | `132 x 1`, `133 x 2` | `1,764` | `0 / 0` | `4,794` |
| `TTT` | `242 x 1`, `729 x 2`, `729 x 4`, `2 x 7`, `241 x 8` | `80 x 1`, `162 x 2`, `81 x 4` | `1,098` | `55 / 1` | `5,460` |

The exact sparse counts are

| chart | nonleak/leak monomials | nonzero entries in `N` / `[N;L]` |
|---|---:|---:|
| `RTT` | `49,703 / 574` | `85,874 / 86,691` |
| `TTT` | `69,710 / 979` | `143,024 / 144,975` |

Every `RTT` leak-bearing component has zero nonleak kernel.  The `TTT`
leak-bearing components have `55` kernel dimensions in total, maximum one
per component, and every one is annihilated by the leak rows.

## 4. Independent derivations

The two primary verifiers enumerate all `105` perfect matchings explicitly
and retain independent slope symbols over `QQ(kappa_4,kappa_5)` and
`QQ(kappa_3,kappa_4,kappa_5)`.  They check the complete component nullspaces
and the representative one-port identity.  The `TTT` verifier additionally
checks the displayed two-active-port continuation.

The no-import audit imports neither primary verifier nor a third-party
algebra package.  It instead:

1. uses the proved local torus action to normalize every slope to one;
2. reconstructs each matching coefficient by a pointed hafnian recurrence;
3. computes exact component ranks with standard-library rational arithmetic;
4. checks the equivalent stacked-rank equality.

It reproduces every count above.

## 5. Slope and specialization scope

Nonzero `T_0` slopes form one local diagonal-torus orbit.  The transport acts
by invertible diagonal scaling on literal columns and monomial coordinates,
preserves the weighted diagonal GHZ form, and fixes the leak/nonleak
divisibility partition because `I_2500` uses colour zero at port `5`.
Therefore there is no omitted nonzero slope fibre.

The same argument does **not** identify arbitrary specializations of source
or physical coordinates.  Such a specialization can erase or merge
monomials and create a new fibrewise linear relation.  The theorem correctly
leaves exhaustive activity/source-coordinate localization open.

## 6. Representative repair identity

The `TTT` primary verifier checks the displayed port-`4` difference in the
theorem term by term.  The desired `P_300 I_2500 d_14` term remains attached
to the old `W_15,W_45` repairs and the restored `P_500,Q_320` channels.
Applying the second active-port difference removes `I_2500` instead of
isolating it.  This is consistent with, but not substituted for, the global
component proof.

## 7. Scope controls

The package does not prove:

- nonlinear ideal membership or a saturated coefficient consequence;
- a separator after a special source-coordinate or edge specialization;
- that any proposed specialized cell is exhaustive;
- nonexistence of a separator for every possible leakage coordinate;
- a complete-source contradiction or control;
- either Family-A key exclusion;
- closure of any other all-rigid, unique-nonrigid, anchor, attachment, or
  local-to-global branch.

The next legal successor is a nonlinear saturated consequence, an exhaustive
activity localization with a specialized relation, or an exact complete
source control.

## 8. Reproduction

From repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_r2_complete_all_active_linear_nonseparation.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_r3_complete_all_active_linear_nonseparation.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_complete_all_active_linear_nonseparation.py
```

All commands exit zero.  Passing them supports only the theorem scope above.
