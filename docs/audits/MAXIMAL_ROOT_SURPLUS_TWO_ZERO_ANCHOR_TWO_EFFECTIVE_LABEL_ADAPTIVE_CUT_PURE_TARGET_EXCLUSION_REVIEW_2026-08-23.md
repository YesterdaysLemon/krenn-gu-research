# Hostile review: zero-anchor two-effective-label adaptive-cut pure-target exclusion

## Verdict

**ACCEPT after correction of the proposed flattening, owning-interface
reconstruction, exhaustive support-case audit, focused exact replay, and an
independent no-import implementation.**  `GLS48` proves that every exact
zero-anchor fixed-residual target point has at least three effective `GLS39`
auxiliary labels.

The review rejected the first proposed `E_A^*|Z_Uhat^*` rank-one statement.
A residual--port or port--port coefficient is a tensor on its open port
variables and may have rank greater than one across that cut; the exact
`GLS40` two-port block has incidence rank five.  The corrected theorem uses
the coefficient/deck cut which moves the unique active pair's open ports to
the probe-root shore.  Across that cut the one remaining labelled summand is
genuinely simple.  All theorem artifacts use only this corrected statement.

The theorem excludes neither the three-effective-label rank-five cell nor
any legal attachment/source branch.  The strategic node and the global
Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS48 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_EFFECTIVE_LABEL_ADAPTIVE_CUT_PURE_TARGET_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py)
- owning interfaces `GLS8`, `GLS21`, `GLS23`, `GLS36`, `GLS39`, and `GLS40`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

Two bounded hostile attacks were kept read-only.  One reconstructed the
auxiliary-pair/raw-label correspondence and found the initial cut error.  The
other sought stronger rank-five cut and principal-deck obstructions and
returned exact controls showing why neither strengthening is sound without
the complete target equations.

## Owning-interface and type audit

At a fixed residual contraction, `GLS39` adjoins two one-dimensional
residual labels to the promoted ports.  Its unordered auxiliary pairs match
the raw labels exactly:

```text
{q_0,q_1}:  coefficient q, deck H_Uhat;
{q_s,u}:    coefficient tensor sigma_(s,u), deck h_(q_s,u);
{u,v}:      coefficient tensor sigma_(u,v), deck h_(u,v).
```

This is the `GLS36` construction of `rho_Q`, not a new formal relabelling.
Zero physical decks are retained as zero components.  A pair coefficient is
zero whenever either endpoint label has both incidence maps zero, so at most
one raw label can survive when the effective support has size at most two.
There is no cancellation assumption and no selected vector or rank minor.

The zero-anchor premise is necessary: it removes the separate top `omega`
coefficient.  The fully supported residual premise is also explicit: it
makes all three residual-torus target scalars nonzero.  An actual witness
satisfies the contracted target equation at every residual choice, so the
pointwise application loses no witness branch.

## Correct adaptive flattening

Let `D` be the unique possibly nonzero auxiliary pair and
`D_0=D intersect Uhat`.  The raw term is

```text
g_D(z_Q) tensor h_D,
```

where the first tensor contains `E_A^*` and the zero, one, or two open port
duals indexed by `D_0`; the second contains all complementary promoted-port
duals.  It is therefore simple across

```text
(A union D_0) | (Uhat-D_0).                           (1)
```

The review explicitly checked the four exhaustive cells:

```text
|Act|<=1:        no pair term;
Act={q_0,q_1}:   q tensor H;
Act={q_s,u}:     one residual--port coefficient/deck term;
Act={u,v}:       one port--port coefficient/deck term.
```

A zero pair map, zero deck, or cancelling polarization only lowers the source
rank.  No other active port remains on the deck shore because `D` contains
the entire effective support.

For root order `r>=3`, `|Uhat|=2r-2>=4` and `|D_0|<=2`, so the right shore in
(1) contains at least two promoted ports.  The target is

```text
sum_c alpha_c
 (r_c tensor e_c^(tensor D_0)) tensor e_c^(tensor (Uhat-D_0)).
```

Its left factors are independent because the `r_c` are independent; its
right constant-colour words are independent on every nonempty ternary tensor
product.  The source and target flattening ranks are therefore at most one
and exactly three.

## Hostile scope boundary

The review actively attacked two tempting strengthenings: that three
effective labels force a rank-five spanning label cut, and that rank five
plus principal-deck compatibility forces an ambient low-rank flattening.
Neither strengthening is stated or used here.  The read-only attacks returned
candidate controls, but those controls are not retained in this package and
have not passed its independent-evidence gates, so this review makes no
mathematical claim about them.  The only accepted conclusion is the
pointwise exclusion of support size at most two.

## Independent computational audit

The SymPy primary enumerates all `22` effective subsets of size at most two
in the minimal six-label auxiliary family (`2` residual plus `4` promoted).
It obtains exactly `7` zero/one-label, `1` residual-pair, `8` residual--port,
and `6` port-pair cells.  On every adaptive cut the sparse GHZ matrix has
exact rank three, and the sole source term has the displayed outer-product
factorization and vanishing `2 by 2` minors.

The no-import audit shares no primary code or algebra package.  It encodes
labels as bit masks, derives the same support census independently, builds
the GHZ matrices over `F_101`, computes their ranks with a custom Gaussian
eliminator, and represents outer-product minors as formal monomials whose two
terms cancel.  The finite-field calculation corroborates the combinatorics;
the characteristic-zero theorem is the written support/factorization proof.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

Focused checks, candidate-tree QA, exact-head hosted CI, safe merge, and fresh
postmerge verification remain publication gates until performed.

## Unresolved boundary

`GLS48` proves only the three-effective-label floor.  Exact three-label
rank-five incidence families exist, and their physical target compatibility
is open.  Rank-five target-coupled classification, ranks six through nine,
silent source-to-swallow coverage, raw escape, nonzero anchor, every selector/
response/activity/synchronization/nuisance/anchor/receiver gate, arbitrary-
root source coverage, strategic-node closure, and global resolution remain
open.
