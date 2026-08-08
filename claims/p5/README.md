# P5 generic obstruction claims

This spine holds the migrated **component-level generic** `H31` and
`H22` obstruction packages.  Every package here proves that the
marked `H31` (respectively weighted `H22`) fibre is empty **at the
generic point of one P4 component's function field** (or on a dense
open subset of it).

**These are generic/function-field theorems.**  They do not close the
same components' special divisors, projective boundaries, exceptional
fibres, or slope divisors, and they do not imply the pointwise
statements.  The pointwise boundary/divisor closures for these and the
other components remain elsewhere (mostly still at the repository
root) and are separate future work.

Migrating a generic theorem under this spine does not change its
scope, status, or excluded divisors.  The global Krenn-Gu conjecture
remains **UNRESOLVED**.

## Layout

| directory | contents |
|---|---|
| [`h31/`](h31/) | generic marked-`H31` obstruction packages (15) |
| [`h22/`](h22/) | generic weighted-`H22` obstruction packages (13) |

The H22 disjoint-mixed-star package was migrated first, in the layout
migration pilot; it lives at
[`h22/disjoint-mixed-star/`](h22/disjoint-mixed-star/) together with
its boundary subpackages and is the structural template for this
spine.  Stage 9 (`p5-generic-obstructions-stage9`) migrated the 28
generic packages listed in the side READMEs.

## Pairing by underlying P4 family

Where both sides of a component have migrated generic theorems they
are paired in matching subdirectory names (for example
`h31/common-singleton/` and `h22/common-singleton/`).  Recorded
asymmetries (never manufactured symmetry):

- `coincident-support-rank-one-star` and `common-kernel-vertical-triangle`
  are H31-only (no live generic H22 theorem exists for them);
- `disjoint-mixed-star` H22 is the pilot package; only the H31 side
  moved in Stage 9;
- `diagonal-quadric` H22 moved in Stage 9; its H31 side is the
  elliptic-generic theorem, inseparable from its boundary forest and
  deliberately not migrated.

## Scope boundary

The following P5 layers are **not** part of this spine and were not
moved by Stage 9: pointwise/divisor closures, boundary obstruction
trees, exceptional-fibre work, the `q4_211` / `q5_221` / component19 /
component21 / component23 programmes, and the frontier documents
(`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`,
`P5_DELTA3_OBLIGATION_LEDGER.md`,
`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`), which remain at the
repository root.
