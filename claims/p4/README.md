# P4 pure-component claims

The P4 programme certifies the irreducible components of the
pure-`P_4` compression locus.  Each component is a symmetry-inequivalent
family of maps sending the order-four permanent tensor `P_4` to a
nonzero pure tensor; the components and their certificates feed the
`P_5 -> Delta_3` reduction described in the top-level
[`README.md`](../../README.md).

**Package migration does not mean the global conjecture is resolved.**
The Krenn-Gu conjecture remains **UNRESOLVED**.

## Migrated standalone pure-component packages

Nine high-confidence pure-`P_4` component packages have been migrated
into [`components/`](components/).  These are the migrated standalone
pure-component packages — not a statement that they exhaust the P4
component classification, which is documented separately (see below).

| package | theorem | verifier | audit | migration batch |
|---|---|---|---|---|
| [`all-rank-one-triangle/`](components/all-rank-one-triangle/) | `P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md` | `verify_p4_all_rank_one_triangle_pure_component.py` | `audit_p4_all_rank_one_triangle_pure_component.py` | `p4-components-stage4` |
| [`diagonal-quadric/`](components/diagonal-quadric/) | `P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md` | `verify_p4_diagonal_quadric_pure_component.py` | `audit_p4_diagonal_quadric_pure_component.py` | `p4-components-stage4` |
| [`disjoint-mixed-star/`](components/disjoint-mixed-star/) | `P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md` | `verify_p4_disjoint_mixed_star_pure_component.py` | `audit_p4_disjoint_mixed_star_pure_component.py` | `p4-components-stage3` |
| [`embedded-p3/`](components/embedded-p3/) | `P4_EMBEDDED_P3_PURE_COMPONENT.md` | `verify_p4_embedded_p3_pure_component.py` | `audit_p4_embedded_p3_pure_component.py` | `p4-components-stage4` |
| [`equal-support-sixfold/`](components/equal-support-sixfold/) | `P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md` | `verify_p4_equal_support_sixfold_pure_component.py` | `audit_p4_equal_support_sixfold_pure_component.py` | `p4-components-stage3` |
| [`mixed-orientation/`](components/mixed-orientation/) | `P4_MIXED_ORIENTATION_PURE_COMPONENT.md` | `verify_p4_mixed_orientation_pure_component.py` | `audit_p4_mixed_orientation_pure_component.py` | `p4-components-stage4` |
| [`single-word-quadrilateral/`](components/single-word-quadrilateral/) | `P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md` | `verify_p4_single_word_quadrilateral_pure_component.py` | `audit_p4_single_word_quadrilateral_pure_component.py` | `p4-components-stage4` |
| [`six-dimensional/`](components/six-dimensional/) | `P4_SIX_DIMENSIONAL_PURE_COMPONENT.md` | `verify_p4_six_dimensional_pure_component.py` | `audit_p4_six_dimensional_pure_component.py` | `p4-components-stage4` |
| [`split-pair/`](components/split-pair/) | `P4_SPLIT_PAIR_PURE_COMPONENT.md` | `verify_p4_split_pair_pure_component.py` | `audit_p4_split_pair_pure_component.py` | `p4-components-stage3` |

Every package holds its theorem document, primary verifier, and
independent audit under their preserved filenames; cross-package
imports use the shared `krenn_gu.bootstrap.expose_claim_package`
helper.

## Migrated classification and boundary spines

Classification spines migrated from the root live under
[`classifications/`](classifications/): triangle / 211
([`classifications/triangle-211/`](classifications/triangle-211/),
Stage 5), star / mixed-star
([`classifications/star/`](classifications/star/), Stage 6), pair
geometry — secant/tangent lower-pair strata and the pure rank-two
component cluster
([`classifications/pair-geometry/`](classifications/pair-geometry/),
Stage 7), and rank-two-triangle — the live resonant/nonresonant
rank-two-relation triangle chain (reductions and flat
classifications;
[`classifications/rank-two-triangle/`](classifications/rank-two-triangle/),
Stage 8).  Genuine boundary theorems and obstructions are kept under
[`boundaries/`](boundaries/) (Stage 7 established
[`boundaries/pair-geometry/`](boundaries/pair-geometry/); Stage 8
established
[`boundaries/rank-two-triangle/`](boundaries/rank-two-triangle/)).
Withdrawn historical attempts in the rank-two-triangle lineage stay
at the root pending a dedicated legacy stage and are labeled
withdrawn, not live.  Migration completeness is not mathematical
exhaustiveness: each spine README states its own scope and the
global conjecture remains **UNRESOLVED**.

## Structure

Each component package holds its theorem document, primary verifier,
and independent audit (filenames preserved):

```text
claims/p4/components/<component>/
  <THEOREM>.md
  verify_<component>_pure_component.py
  audit_<component>_pure_component.py
```

Where the overall component census and the global reduction remain
documented:

- component census and exhaustiveness: the checkpoint section of the
  top-level [`README.md`](../../README.md) and
  [`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](classifications/P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md);
- migration mechanics and provenance:
  [`docs/architecture/layout-migration-stage4-report.md`](../../docs/architecture/layout-migration-stage4-report.md)
  and [`catalog/moved-paths.json`](../../catalog/moved-paths.json).
