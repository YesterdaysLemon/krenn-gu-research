# P4 pure-component claims

The P4 programme certifies the irreducible components of the
pure-`P_4` compression locus.  Each component is a symmetry-inequivalent
family of maps sending the order-four permanent tensor `P_4` to a
nonzero pure tensor; the components and their certificates feed the
`P_5 -> Delta_3` reduction described in the top-level
[`README.md`](../../README.md).

**Package migration does not mean the global conjecture is resolved.**
The Krenn-Gu conjecture remains **UNRESOLVED**.

## Migrated packages

- [`disjoint-mixed-star/`](components/disjoint-mixed-star/) — theorem `P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`, verifier present, independent audit present (moved under batch `p4-components-stage3`).
- [`equal-support-sixfold/`](components/equal-support-sixfold/) — theorem `P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md`, verifier present, independent audit present (moved under batch `p4-components-stage3`).
- [`split-pair/`](components/split-pair/) — theorem `P4_SPLIT_PAIR_PURE_COMPONENT.md`, verifier present, independent audit present (moved under batch `p4-components-stage3`).

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
  [`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](../../P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md);
- migration mechanics and provenance:
  [`docs/architecture/layout-migration-stage3-report.md`](../../docs/architecture/layout-migration-stage3-report.md)
  and [`catalog/moved-paths.json`](../../catalog/moved-paths.json).
