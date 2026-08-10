# P5 obstruction claims

This spine holds the migrated P5 obstruction packages.  The `h31/` and
`h22/` subtrees contain the component-level packages, while `frontier/`,
`boundaries/`, and `coordinate-cegar/` contain the Stage 29 and Stage 32
ownership forests. The earlier paired packages under `h31/` and `h22/` are
generic: they prove that
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
`common-center-kernel-star-component-finite-lambda-zero-all-marking/` and
`common-center-kernel-star-component-finite-lambda-one-all-marking/`
directories are the separate exact characteristic-zero `lambda=0` and
`lambda=1` all-affine-marking obstructions over `Q(r,t)` at the generic point
of component twenty-three. Each is one scoped case-coverage leaf, not by
itself the whole generic finite fibre and not pointwise closure of special or
projective component fibres. The `lambda=0` primary depends load-bearingly on
the prior dense-open factor cover `h2*h3*H0=0` and closes only its `h2=0`,
`h3=0`, and `H0=0` branches. Its no-repository-import audit is exact-`Q`
branch-module QA at `(r,t)=(2,4)`, using `h3=3/8`; it proves neither the
factor cover nor the generic theorem. The later ordinary-residual theorem
consumes the complete `lambda=0,1,-1` slices to close the generic finite case
union, while the leaves' chronological false and residual-`UNKNOWN` fields
remain leaf-local. The generic core and remaining boundary forest are
separately packaged in the H22 subtree with their original statuses. The H22
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
`lambda=0` and `lambda=1` all-affine-marking H22 leaves,
and the six-dimensional H22 equal-weight
normal-form-point leaf, pointwise boundary/divisor closures for these and the
other components remain separate obligations; their package location does not
promote them to complete closures.

Migrating a generic theorem under this spine does not change its
scope, status, or excluded divisors.  The global Krenn-Gu conjecture
remains **UNRESOLVED**.

## Layout

| directory | contents |
|---|---|
| [`h31/`](h31/) | marked-`H31` obstruction forest (52 direct directories; generic, divisor-scoped, boundary, carrier-only, and neutral disputed-ownership packages retain distinct claims and evidence roles) |
| [`h22/`](h22/) | weighted-`H22` obstruction forest (108 direct package directories; 111 total including nested packages; generic, scoped, partial, candidate, historical, and one neutral disputed-ownership package retain distinct statuses) |
| [`frontier/`](frontier/) | frontier/reduction forest: 228 artifacts after Stages 29 and 32 (`83 md + 143 py + 2 cpp`), preserving partial, candidate, superseded, and asymmetric evidence |
| [`boundaries/`](boundaries/) | selected boundary packages: 32 artifacts after Stages 29 and 32 (`11 md + 21 py`) |
| [`coordinate-cegar/`](coordinate-cegar/) | coordinate and bounded-CEGAR packages: 25 artifacts after Stages 29 and 32 (`9 md + 16 py`) |

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
marked-fibre batch was deferred at that time because its theorem and primary
disagreed on the certificate-stratum count; the later bounded reconciliation
distinguished component and record counts and resolved that stop condition.
Stage 24 (`p5-h31-component-fibre-infinity-marked-fibre-stage24`, mapping
`103e5de3343c1271841a84cfa79903c9d9e8c6f2c318adc8325c3b8cd1a3ace1`)
migrated that exact four-file complete marked-basis-fibre successor while
retaining the canonical section as a separate live predecessor.  The package
closes only the stated first-plane divisor; the rest of the projective
boundary, later components, component exhaustiveness, and the global
conjecture remain open.  The complete chart-boundary marked-fibre family was
later reconciled and migrated as its own exact four-file package without
changing this first-plane result.
Stage 25 (`p5-h22-finite-lambda-one-all-marking-stage25`, mapping
`611abb78c553a124a4cf02308950ec5ace6c9f5f1e2e727ece7f043f3b1f59ba`)
migrated the exact component-23 finite `lambda=1` all-affine-marking leaf over
`Q(r,t)`. At that stage the old partial theorem, dense-open supplement,
`lambda=0` sibling, later ordinary case-union theorem, shared providers, and
special/projective/source-torus boundary forest remained at root; Stage 31
later colocated that forest without changing status. The leaf's chronological false
and residual-`UNKNOWN` fields remain unchanged; the later case union remains
closed at its stated generic scope. The exact-Q audit at `(2,4)` is QA rather
than a generic proof, and the global conjecture remains **UNRESOLVED**.
Stage 26 (`p5-h22-finite-lambda-zero-all-marking-stage26`, mapping
`06622ad9c8ab149021fd4d3a5c412327db4a28cd2f210d339418d118a7e85131`)
migrated the separate exact component-23 finite `lambda=0`
all-affine-marking leaf over `Q(r,t)`. It depends on the separately packaged
dense-open `h2*h3*H0=0` factor cover and closes only those three residual branches. Its
no-repository-import exact-`Q` audit at `(2,4)` uses `h3=3/8` as
branch-module QA; it does not prove the factor cover or generic theorem. The
later ordinary-residual theorem consumes `lambda=0,1,-1` and closes the
generic finite union at its stated scope, so the new leaf's chronological
false and residual-`UNKNOWN` fields require no promotion. The generic core,
special/projective fibres, whole-component and component-exhaustiveness
questions, the then-separate H31 certificate-stratum conflict, and the global
conjecture remain outside this migration. The global conjecture remains
**UNRESOLVED**.

Stage 29 (`p5-frontier-stage29`, mapping
`6577eb9544a8bcc5c20f0c6a204a7248b1db68ec15331d12281e791baccd5d7e`)
moved 176 exact root artifacts into `frontier/`, `boundaries/`, and
`coordinate-cegar/`.  The complete 60-file normalized `q4_211` forest and
49-file normalized `q5_221` forest are ownership/evidence-carrier closures
inside those branches, not an exhaustive P5 case cover.  The `q5_221`
working note remains superseded.  The exact characteristic-zero
`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION` theorem and its verifier/audit
remain separately owned at root.  At the Stage 29 boundary, four owner-gated conflicts and every
excluded Component20/21/23, H22/H31, Branch B, high-coordinate, weighted
`p+q`, internal-`E=0`, marked-basis, legacy, and withdrawn surface remain
outside the Stage 29 forest.  The migration adjudicates none of their statuses
or ownership conflicts.  Arbitrary P7/local-to-global remains **UNKNOWN**, and
the global conjecture remains **UNRESOLVED**.

Stage 31 (`p5-h22-root-exit-stage31`, mapping
`899a1070f1515105f76265c2bfcb80e2316c0d3a623ea9afc53a59940779f2e1`)
moved 351 H22 artifacts: 311 into coherent claim packages and 40 into the
neutral `h22/disputed-ownership/p-plus-q-wall/` package. It also extracted
the exact four-source weighted-H22 contraction used by 39 consumers into
`src/krenn_gu/p5_weighted_h22_contraction.py`, while retaining the
Component20 scientific adapter inside its claim package. Candidate, partial,
superseded, scoped-refuted, open, and verified statuses were not normalized.
The disputed package records rather than adjudicates ownership; the global
conjecture remains **UNRESOLVED**.

The later owner-authorized H31 chart-boundary marked-fibre reconciliation
resolved only the former component-versus-certificate-record count conflict:
equation (9) has 13 irreducible projection components, while the verifier has
16 factor-certificate records (13 generic-basis and 3 exceptional-basis).
The four-file family now lives in
`h31/component-chart-boundary-marked-fibre/`; its exact selected unit ideals
close only that divisor.  The P4 attribution, broader first/second-component
provenance, and weighted-H22 `p+q=0` disagreements remain unadjudicated, and
the global conjecture remains **UNRESOLVED**.

Stage 32 (`p5-residual-root-exit-stage32`, mapping
`be94dcaadb97d29eb6e6b5efe712485ac55aa3286e802dfa457746cd8dd4cf56`)
moved 220 residual P5 artifacts: 85 to `frontier/`, 83 to `h31/`, 15 to
`boundaries/`, nine to `coordinate-cegar/`, one to `h22/`, 31 operator
entry points to `tools/`, and one pre-existing shared module to
`src/krenn_gu`.  Seven first/second-component provenance files use the
neutral `h31/disputed-ownership/first-second-component-provenance/` package;
its README records the disagreement without adjudicating it.  Widely consumed
marked-basis, high-coordinate, support-system, q5_311, pair-catalogue,
split-saturation, and Singular-runtime code was separated into narrow shared
cores with frozen no-solver parity tests.  Claim-specific entry points and
audits remain with their owners, all statuses and asymmetries are preserved,
and the global conjecture remains **UNRESOLVED**.

## Pairing by underlying P4 family

Where both sides of a component have migrated generic theorems they
are paired in matching subdirectory names (for example
`h31/common-singleton/` and `h22/common-singleton/`).  Recorded
asymmetries (never manufactured symmetry):

- `coincident-support-rank-one-star` and `common-kernel-vertical-triangle`
  are H31-only (no live generic H22 theorem exists for them);
- `disjoint-mixed-star` H22 is the pilot package and includes a partial
  boundary subtree; only the H31 side moved in Stage 9;
- `diagonal-quadric` H22 moved in Stage 9; its H31 elliptic-generic theorem
  and boundary forest now live in their distinct H31 packages, without
  merging their scopes or evidence roles;
- `equal-support-sixfold` has migrated H31 and H22 generic theorems,
  but each has a primary verifier only: no P5 independent audit exists;
- `six-dimensional` has migrated H31 and H22 generic theorems, and its H22
  package also carries the separately scoped equal-weight generic-point leaf;
  that leaf is not pointwise closure of the full `r=1` divisor;
- `embedded-p3` has a complete projective H31 closure package, while its
  separately packaged weighted-H22 programme retains its open projective
  coverage and other narrower statuses;
- `common-active-binary-triangle` contains the complete H31 diagonal
  `p+q=0` wall subforest and a separate H22 forest; the H22 weighted-wall
  ownership disagreement remains explicit in the neutral disputed package;
- `internal-e0-marked-fibre`, `toric-marked-fibre`,
  `component-chart-boundary`, `component-chart-boundary-marked-fibre`,
  `component-fiber-infinity`, and `component-fibre-infinity-marked-fibre`
  are H31-only scoped leaves; they
  participate in the separately established first-component synthesis but
  none is a generic or complete-component package.  The
  toric leaf closes only the 21 genuine toric base-orbit/orientation cases,
  while the canonical chart-boundary leaf closes only the displayed marked
  sections and its complete successor adds all kernel-row shifts only on that
  same divisor.  The canonical first-plane leaf likewise closes only its
  displayed marking, and its complete successor adds all marked-basis shifts
  only on that same divisor.  None of these divisor leaves closes the rest of
  the projective boundary or a whole component;
- `common-center-kernel-star` includes the separately scoped H22 finite
  `lambda=0` and `lambda=1` leaves plus its generic case-union and boundary
  forest; these distinct records do not become a matching whole-component
  generic package through colocation;
- `unequal-complement-common-kernel`, `unequal-endpoint-inward-star`, and
  `split-center-mixed-star` now have their H22 partial, recursive, or
  candidate-dependent evidence under `h22/`; those statuses remain
  asymmetric with the H31 side;
- `first-rank-two` is H22-only here; `one-three` / `one-three-components`
  is the additional two-sided Stage 10 pair.

## Scope boundary

This spine now contains the residual P5 ownership forest as well as the
earlier generic and bounded packages.  That filesystem closure is not a
mathematical case cover: each document's quantifiers, divisor restrictions,
candidate/partial/lifecycle state, proof dependencies, and audit limitations
remain authoritative.  P4 antecedents, arbitrary-order and finite-instance
programmes, local-to-global gluing, and every explicitly open remainder remain
separate proof obligations.  No package location supplies a missing bridge or
promotes a computational record.  The global conjecture remains
**UNRESOLVED**.
