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
package and not a closure of its projective interior.  The H31
`component-chart-boundary/` directory is the exact canonical marked-row
section on one nonzero preferred-chart divisor of the first component, not
the later complete marked-fibre strengthening or a component closure.  The H31
`component-fiber-infinity/` directory is the exact canonical marked-row
section on the first-plane Schubert-infinity locus where the other three
selected preferred Pluecker coordinates remain nonzero, not its later complete
marked-fibre strengthening or an entire projective-boundary closure.  The H31
`component-fibre-infinity-marked-fibre/` directory is the exact complete
marked-basis-fibre strengthening on that same divisor, with `H,N != 0`, `E`
arbitrary, `(A,D)!=(0,0)`, every kernel-row shift, all four orientations, and
every binary `Delta_2` extension direction with both diagonal coefficients
nonzero.  Its arbitrary-`E` scope includes the `E=0` intersection on this leaf,
not the separate whole internal-`E=0` divisor.  It does not close the rest of
the projective boundary or a whole component; the canonical predecessor
remains live and separately owned.  The H22
`common-center-kernel-star-component-finite-lambda-one-all-marking/`
directory is the exact characteristic-zero `lambda=1` all-affine-marking
obstruction over `Q(r,t)` at the generic point of component twenty-three.
It is one complete case-coverage leaf, not by itself the whole generic finite
fibre and not pointwise closure of special or projective component fibres.
Its audit is exact QA at `(r,t)=(2,4)`, not an independent generic proof. The
later generic case-union theorem and the remaining boundary forest stay at
root.  The H22
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
divisor leaf, the toric marked-fibre boundary leaf, the canonical H31
chart-boundary and first-plane Schubert-infinity section leaves, the complete
first-plane Schubert-infinity marked-fibre leaf, the
disjoint-mixed-star H22 boundary subpackages, the component-23 finite
`lambda=1` all-affine-marking H22 leaf,
and the six-dimensional H22 equal-weight
normal-form-point leaf, pointwise boundary/divisor closures for these and the
other components remain elsewhere (mostly still at the repository root) and
are separate future work.

Migrating a generic theorem under this spine does not change its
scope, status, or excluded divisors.  The global Krenn-Gu conjecture
remains **UNRESOLVED**.

## Layout

| directory | contents |
|---|---|
| [`h31/`](h31/) | marked-`H31` obstruction packages (31 directories; one complete component-closure forest, one flat three-triple `p+q=0` wall subforest, one three-package rank-one-gate forest, one internal-`E=0` divisor leaf, one toric marked-fibre boundary leaf, one canonical chart-boundary section leaf, one canonical first-plane Schubert-infinity section leaf, and one complete first-plane Schubert-infinity marked-fibre leaf) |
| [`h22/`](h22/) | weighted-`H22` obstruction packages (19; the disjoint-mixed-star pilot has a partial boundary subtree, six-dimensional also has one equal-weight generic-point leaf, and component twenty-three has one finite `lambda=1` all-affine-marking generic-point leaf) |

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
Stage 22 (`p5-h31-component-chart-boundary-stage22`) migrated the exact
canonical marked-row section on one nonzero preferred-chart divisor while
leaving the complete marked-fibre successor, its uniquely owned generator,
other component boundaries, and component exhaustiveness separately owned.
Stage 23 (`p5-h31-component-fiber-infinity-stage23`) migrated the exact
canonical marked-row section on the first-plane Schubert-infinity locus while
leaving arbitrary kernel-row shifts, its complete marked-fibre successor, the
rest of the projective boundary, later components, and component
exhaustiveness separately owned.  A different proposed complete chart-boundary
marked-fibre batch was deferred because its theorem and primary disagree on
the certificate-stratum count.
Stage 24 (`p5-h31-component-fibre-infinity-marked-fibre-stage24`, mapping
`103e5de3343c1271841a84cfa79903c9d9e8c6f2c318adc8325c3b8cd1a3ace1`)
migrated that exact four-file complete marked-basis-fibre successor while
retaining the canonical section as a separate live predecessor.  The package
closes only the stated first-plane divisor; the rest of the projective
boundary, later components, component exhaustiveness, and the global
conjecture remain open.  The blocked complete chart-boundary marked-fibre
family remains deferred with its fourteen-versus-sixteen certificate-stratum
conflict unadjudicated.
Stage 25 (`p5-h22-finite-lambda-one-all-marking-stage25`, mapping
`611abb78c553a124a4cf02308950ec5ace6c9f5f1e2e727ece7f043f3b1f59ba`)
migrated the exact component-23 finite `lambda=1` all-affine-marking leaf over
`Q(r,t)`. The old partial theorem, dense-open supplement, `lambda=0` sibling,
later ordinary case-union theorem, shared providers, and special/projective/
source-torus boundary forest remain at root. The leaf's chronological false
and residual-`UNKNOWN` fields remain unchanged; the later case union remains
closed at its stated generic scope. The exact-Q audit at `(2,4)` is QA rather
than a generic proof, and the global conjecture remains **UNRESOLVED**.

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
- `internal-e0-marked-fibre`, `toric-marked-fibre`,
  `component-chart-boundary`, `component-fiber-infinity`, and
  `component-fibre-infinity-marked-fibre` are H31-only scoped leaves; they
  participate in the separately established first-component synthesis but
  none is a generic or complete-component package.  The
  toric leaf closes only the 21 genuine toric base-orbit/orientation cases,
  while the chart-boundary leaf closes only the displayed canonical marked
  sections, the canonical first-plane leaf closes only its displayed marking,
  and the complete first-plane leaf adds all marked-basis shifts only on that
  same divisor.  Neither first-plane leaf closes the rest of the projective
  boundary or a whole component;
- `common-center-kernel-star` now has only the scoped H22 finite `lambda=1`
  leaf described above; its generic case-union core and boundary forest remain
  at root, so this is not a matching whole-component generic package;
- `unequal-complement-common-kernel`, `unequal-endpoint-inward-star`, and
  `split-center-mixed-star` are
  H31-only in this spine because their H22 work is partial, boundary
  recursive, or depends on candidate-only evidence;
- `first-rank-two` is H22-only here; `one-three` / `one-three-components`
  is the additional two-sided Stage 10 pair.

## Scope boundary

Except for the exact H31 embedded-P3 component-closure forest, the scoped H31
`p+q=0` wall and single-gate branch forests, the internal-`E=0` divisor leaf,
the toric marked-fibre boundary leaf, the canonical H31 chart-boundary and
first-plane Schubert-infinity section leaves, the complete first-plane
Schubert-infinity marked-fibre leaf, the scoped H22 disjoint-mixed-star
boundary subpackages, the component-23 finite `lambda=1` all-affine-marking
H22 leaf, and the H22 six-dimensional equal-weight
normal-form-point leaf, the following P5 layers are **not** part of this spine:
pointwise/divisor closures, boundary obstruction trees, exceptional-fibre
work, the `q4_211` / `q5_221` / component19 / component21 / remaining
component-23 programmes, and the frontier documents
(`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`,
`P5_DELTA3_OBLIGATION_LEDGER.md`,
`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`), which remain at the
repository root.
