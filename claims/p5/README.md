# P5 obstruction claims

This spine holds the migrated component-level `H31` and `H22`
obstruction packages.  Almost every package is generic: it proves that
the marked `H31` (respectively weighted `H22`) fibre is empty **at the
generic point of one P4 component's function field** (or on a dense
open subset of it).  The `h31/embedded-p3/` package is the sole complete
component-closure forest here; it contains the generic, affine-boundary,
and projective case-union evidence together.  Three H31 single-gate
directories form one complete rank-one-gate obstruction forest, not a
complete component closure.  The H31 `common-active-binary-triangle/`
directory contains the complete diagonal `p+q=0` wall subforest, not the
broader common-active component family.  The H31
`internal-e0-marked-fibre/` directory is one exact divisor-scoped leaf, not a
generic or complete-component package.  The H31 `toric-marked-fibre/`
directory is the exact complete marked-fibre obstruction over the 21 genuine
toric base cases of the first component, not a generic or whole-component
package and not a closure of its projective interior.  The H22
`disjoint-mixed-star/` pilot also contains a partial, explicitly scoped
boundary subtree. The H22 `six-dimensional/` package additionally contains
the equal-weight `r=1` binary leaf at the generic component function-field
normal-form point; it is not pointwise closure of the full geometric `r=1`
divisor.

**The generic packages are generic/function-field theorems.**  They do
not close the same components' special divisors, projective boundaries,
exceptional fibres, or slope divisors, and they do not imply the
pointwise statements.  Outside the exact embedded-P3 H31 closure forest, the
scoped H31 `p+q=0` wall and single-gate branch forests, the internal-`E=0`
divisor leaf, the toric marked-fibre boundary leaf, and the disjoint-mixed-star
H22 boundary subpackages, and the six-dimensional H22 equal-weight
normal-form-point leaf, pointwise boundary/divisor closures for these and the
other components remain elsewhere (mostly still at the repository root) and
are separate future work.

Migrating a generic theorem under this spine does not change its
scope, status, or excluded divisors.  The global Krenn-Gu conjecture
remains **UNRESOLVED**.

## Layout

| directory | contents |
|---|---|
| [`h31/`](h31/) | marked-`H31` obstruction packages (28 directories; one complete component-closure forest, one flat three-triple `p+q=0` wall subforest, one three-package rank-one-gate forest, one internal-`E=0` divisor leaf, and one toric marked-fibre boundary leaf) |
| [`h22/`](h22/) | weighted-`H22` obstruction packages (18; the disjoint-mixed-star pilot has a partial boundary subtree and six-dimensional also has one equal-weight generic-point leaf) |

The H22 disjoint-mixed-star package was migrated first, in the layout
migration pilot; it lives at
[`h22/disjoint-mixed-star/`](h22/disjoint-mixed-star/) together with
its boundary subpackages and is the structural template for this
spine.  Stage 9 (`p5-generic-obstructions-stage9`) migrated the 28
generic packages listed in the side READMEs.  Stage 10
(`p5-deferred-generics-stage10`) recovered and migrated nine further
generic packages (25 files), while leaving all boundary and divisor
descendants at the repository root.  Stage 13
(`p5-h22-split-center-stage13`) migrated the split-center H22 generic
triple.  Stage 16 (`p5-h31-embedded-p3-stage16`) migrated the complete
five-triple H31 embedded-P3 closure forest.  Stage 17
(`p5-h31-single-gate-stage17`) migrated the three-triple H31 rank-one-gate
obstruction forest while leaving every all-rank-two branch open.  Stage 18
(`p5-h31-common-active-p-plus-q-stage18`) migrated the complete three-triple
diagonal `p+q=0` H31 wall subforest while leaving the broader common-active
family separately owned.  Stage 19 (`p5-h31-internal-e0-stage19`) migrated
the exact internal-`E=0` marked-fibre divisor triple while leaving the other
first-component and later-component obligations separately owned.  Stage 20
(`p5-h31-toric-marked-fibre-stage20`) migrated the exact first-component
toric marked-fibre triple while leaving the projective base interior, second
or further components, and component exhaustiveness separately owned.
Stage 21 (`p5-h22-six-dimensional-equal-weight-stage21`) added the exact
equal-weight `r=1` binary leaf at the generic six-dimensional component
function-field normal-form point while leaving the full geometric divisor,
other slopes, parameter/projective boundaries, and component exhaustiveness
separately owned.

## Pairing by underlying P4 family

Where both sides of a component have migrated generic theorems they
are paired in matching subdirectory names (for example
`h31/common-singleton/` and `h22/common-singleton/`).  Recorded
asymmetries (never manufactured symmetry):

- `coincident-support-rank-one-star` and `common-kernel-vertical-triangle`
  are H31-only (no live generic H22 theorem exists for them);
- `disjoint-mixed-star` H22 is the pilot package and includes a partial
  boundary subtree; only the H31 side moved in Stage 9;
- `diagonal-quadric` H22 moved in Stage 9; its H31 side is the
  elliptic-generic theorem, inseparable from its boundary forest and
  deliberately not migrated;
- `equal-support-sixfold` has migrated H31 and H22 generic theorems,
  but each has a primary verifier only: no P5 independent audit exists;
- `six-dimensional` has migrated H31 and H22 generic theorems, and its H22
  package also carries the separately scoped equal-weight generic-point leaf;
  that leaf is not pointwise closure of the full `r=1` divisor;
- `embedded-p3` now has a complete projective H31 closure package,
  while its separate weighted-H22 programme remains at root with open
  projective coverage;
- `common-active-binary-triangle` now contains only the complete H31
  diagonal `p+q=0` wall subforest; its remaining H31 siblings and all H22
  common-active wall work remain separately owned at root;
- `internal-e0-marked-fibre` and `toric-marked-fibre` are H31-only scoped
  leaves; they participate in the separately established first-component
  synthesis but neither is a generic or complete-component package.  The
  toric leaf closes only the 21 genuine toric base-orbit/orientation cases;
- `common-center-kernel-star`, `unequal-complement-common-kernel`,
  `unequal-endpoint-inward-star`, and `split-center-mixed-star` are
  H31-only in this spine because their H22 work is partial, boundary
  recursive, or depends on candidate-only evidence;
- `first-rank-two` is H22-only here; `one-three` / `one-three-components`
  is the additional two-sided Stage 10 pair.

## Scope boundary

Except for the exact H31 embedded-P3 component-closure forest, the scoped H31
`p+q=0` wall and single-gate branch forests, the internal-`E=0` divisor leaf,
the toric marked-fibre boundary leaf, and the scoped H22 disjoint-mixed-star
boundary subpackages, and the H22 six-dimensional equal-weight
normal-form-point leaf, the following P5 layers are **not** part of this spine:
pointwise/divisor closures, boundary obstruction trees, exceptional-fibre
work, the `q4_211` / `q5_221` / component19 / component21 / component23
programmes, and the frontier documents
(`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`,
`P5_DELTA3_OBLIGATION_LEDGER.md`,
`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`), which remain at the
repository root.
