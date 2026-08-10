# Post-root-exit symbolic programme handoff — 2026-08-10

## Status and purpose

The global Krenn--Gu conjecture remains **UNRESOLVED**. This document records
the next exact symbolic obligations after the repository root exit; it proves
no new theorem, changes no claim status, and reports no new computation.

The operational base is merged `main` at
`e99457df478b0842a833204a2f064ab00355a838`.

- Stage 33 moved the final 305 root-debt artifacts through PR #69 and merged as
  `4263832e3ff338c5bd87528268cb8cb563866ec0`; both exact-head and exact
  merged-main CI passed in runs `31382542675` and `31382762054`. See the
  [Stage 33 report](architecture/root-exit-stage33-final-residual-dry-run.md).
- Phase R3 activated default-strict root enforcement through PR #70 and merged
  as `e99457df478b0842a833204a2f064ab00355a838`; both exact-head and exact
  merged-main CI passed in runs `31384450581` and `31384547265`. The root is
  now exactly seven allowed files and nine allowed directories, with debt
  `0/0`. See the
  [Phase R3 report](architecture/root-exit-phase-r3-enforcement-report.md).

No SAT, Singular, brute-force, numerical, sampling, or broad scientific replay
was run to prepare this handoff. The recommendations below come from a fresh
read-only reconstruction of the merged claim packages, their verifier/audit
surfaces, and the current proof-obligation graph.

## Authority and known documentation drift

For a scientific continuation, read authorities in this order:

1. the owning theorem/status document and its package README;
2. the primary verifier and genuinely independent audit, with their exact
   assumptions and evidence roles;
3. the repository README and dated handoffs for navigation;
4. the theorem ledger and older frontier summaries as curated indexes, not as
   substitutes for the owning claim.

The [2026-08-05 frontier snapshot](current-frontier.md) contains a known
post-snapshot inconsistency:

- it describes Component 22 as the sole generic weighted-`H22` exception and
  the generic closure as 24 of 25, while the owning Component 25 packages still
  leave its generic finite-`D23` branches open; the current honest count is 23
  of 25, with Components 22 and 25 live.

This tranche corrects the corresponding theorem-ledger census text and maps
the existing
[`P4 independent audit`](../claims/p4/classifications/audit_p4_all_pair_rank_exceptional_graph_reduction.py).
That audit independently reconstructs the constant-size matching combinatorics
and an `F_5` rank-factorization check; it is not the B3 semantic composition
audit and does not replace the characteristic-zero proof. These are
proof-graph/index corrections, not new mathematical results.

## Rank 0: decide the committed legal P7 pullback exactly

The primary programme-level target is the exact calculation specified by
[`COMMITTED_LEGAL_SENSOR_ORDERED_SECANT_FACTOR_CHOW_NORM_AND_BOUNDARY_TRAP_CRITERION.md`](../claims/p7/COMMITTED_LEGAL_SENSOR_ORDERED_SECANT_FACTOR_CHOW_NORM_AND_BOUNDARY_TRAP_CRITERION.md).
The note supplies the characteristic-zero reduction and structural checks, but
explicitly records that the committed scheme has not been built and neither
outcome has been selected.

### Exact obligation

1. Materialize the 24 determinant-cleared residual membership polynomials for
   the fixed rank-219 legal sensor.
2. Pull back the exact seven-variable two-factor ideal -- 35 cubics and 21
   pentads -- to the 32-dimensional ordered rank-three secant parameter space.
3. Localize by the stated torus-concise, root-torus, simple-incidence,
   pair-nonzero, and pinned product.
4. Establish properness/finiteness before using multiplication matrices. If
   the larger pullback is not independently proved finite, use the localized
   criterion componentwise; an expected-dimension count is not a finiteness
   proof.
5. Decide over characteristic zero whether the localized algebra `A_good` is
   zero or nonzero, with an independently reconstructed exact audit.
6. If `A_good` is nonzero, impose `eta=0` and star alignment and decide the
   quotient `A_gen^star`.

A successful package should contain the explicit coefficient/source manifest,
immutable hashes, a primary exact construction, and an independent route that
reconstructs the claimed unit certificate or finite quotient/multiplication
certificate without importing the primary's conclusion.

### Meaning of the branches

- `(J_Gamma : D_tc^infinity)=<1>`: the mandatory intersection is trapped in
  the classified secant/root boundary.
- `A_good=0`: the mandatory intersection misses the good union and lies on a
  torus-concise/collision, root-torus, simple-incidence, pair-zero, or pinned
  boundary. This is not yet a P7 obstruction until those boundary mechanisms
  are exhausted.
- `A_good!=0`: an honest good-open survivor exists.
- `A_gen^star=0`: the legal `h=0` weighted pair ideal is unit on that good
  union.
- `A_gen^star!=0`: a legal pair-sector survivor exists. It is not a Krenn--Gu
  witness; 105 other four-deck entries and the upper-deck equations remain.

The required geometric inputs are the exact rank-219 sensor and pivot block,
the 24-dimensional cokernel incidence in the
[`five-root target-incidence theorem`](../claims/p7/five-root-diagonal-target-incidence/FIVE_ROOT_DIAGONAL_TARGET_INCIDENCE_SCHUBERT_DUALITY_AND_COFACTOR_LINE_THEOREM.md),
and the determinant-cleared partner/pair/integrability filters in
[`P7_TARGET_INCIDENCE_DETERMINANT_CLEARED_HAFNIAN_INTEGRABILITY_THEOREM.md`](../claims/p7/P7_TARGET_INCIDENCE_DETERMINANT_CLEARED_HAFNIAN_INTEGRABILITY_THEOREM.md).
The existing
[`primary verifier`](../claims/p7/verify_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py)
and
[`independent audit`](../claims/p7/audit_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py)
check the present structural theorem; they do not decide the as-yet-unbuilt
`A_good` calculation.

## Bounded P5 closure lane

This is the smaller, already-factored continuation if the next tranche should
close a narrow existing leaf rather than start the P7 quotient construction.

### Component 22: smallest isolated complement

On the generic finite-`D23` chart

```text
H=2*A*h1+1=0,    rho*(rho+1)!=0,
```

the exact rank-drop cover is

```text
h2*f2*f7*f8*U*V=0.
```

The full `h2=0` factor, the `f2=f7=0` intersection, and the slope-zero
subintersection `f2=f8=2*h3+s=0` are already closed in their stated scopes.
The smallest explicitly isolated unknown complement is therefore

```text
H=f2=f8=0,    rho*(rho+1)!=0,    2*h3+s!=0.
```

Its owning boundary is stated in
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_F2_F8_H3_SLOPE_INTERSECTION_OBSTRUCTION.md`](../claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-h3-slope-intersection/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_F2_F8_H3_SLOPE_INTERSECTION_OBSTRUCTION.md).
No theorem/primary/audit package yet closes the complement. After it, the
remaining `f2=0` residual is still a separate obligation. The broader cover is
owned by
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_TWO_MINOR_FACTOR_COVER_PARTIAL_OBSTRUCTION.md`](../claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-two-minor-factor-cover-partial/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_TWO_MINOR_FACTOR_COVER_PARTIAL_OBSTRUCTION.md).

### Component 25: parallel generic hole

Component 25 is not closed generically. Its
[`finite-D23 three-branch cover`](../claims/p5/h22/unequal-endpoint-inward-star-component-finite-d23-factor-cover/P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D23_FACTOR_COVER.md)
places every generic candidate in three branches but excludes none of them.
The
[`lambda=1 theorem`](../claims/p5/h22/unequal-endpoint-inward-star-component-finite-d23-lambda-one/P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D23_LAMBDA_ONE_OBSTRUCTION.md)
closes only that slice. Other finite-`D23` branches, a finite-`D01` residual,
special parameter fibres, and projective boundaries remain `UNKNOWN`.

Do not revive the withdrawn Branch-B coefficient-splitting argument: its
passing scripts certify narrower descent identities and do not establish the
full-field claim.

### B3: audit the P4 cover's quantifiers

The
[`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](../claims/p4/classifications/P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md)
claims that 25 component closures exhaust the all-pair-rank exceptional locus.
The remaining B3 gate is a bounded human semantic/composition audit of the
cover statement, including its nonzero-pure-factor, symmetry, and inclusion
quantifiers. Do not restart the component search, and do not treat replay of
the primary/audit scripts alone as that composition audit.

Even after B3 and both generic weighted-`H22` holes close, the local
`P5 -> Delta_3` programme still needs pointwise treatment of every excluded
parameter divisor and projective/chart boundary. The obligation schema in
[`P5_DELTA3_OBLIGATION_LEDGER.md`](../claims/p5/frontier/P5_DELTA3_OBLIGATION_LEDGER.md)
remains useful, but its historical per-component counts are not current.

## P7 backups

If the rank-0 quotient construction is blocked for a concrete algebraic reason,
use one of these independent symbolic routes rather than broad search.

1. **Force two transverse root-pair fans on one legal P7 window.** The exact
   sharing classification constructs graph-side rank-`4+4`, stacked-rank-six
   controls. The missing theorem must force such a pair from the actual
   GHZ/companion equations with common nonzero shores and nuisance separation,
   or prove every available pair lies on a classified boundary. See
   [`P7_FIVE_ROOT_TWO_FAN_SHARING_AND_SHARED_ROOT_VERONESE_TRANSVERSALITY.md`](../claims/p7/P7_FIVE_ROOT_TWO_FAN_SHARING_AND_SHARED_ROOT_VERONESE_TRANSVERSALITY.md).
2. **Decide the seven-variable Hessian/projective-stationarity incidence.**
   Exhaust the generic full-edge chart and every higher-corank/exceptional wall
   over characteristic zero using the full `Psi wedge Lambda=0` system and its
   scalar filters. See
   [`P7_PHYSICAL_EXTENSION_BOOLEAN_SQUARE_PROJECTIVE_STATIONARITY_MASTER_SYSTEM.md`](../claims/p7/P7_PHYSICAL_EXTENSION_BOOLEAN_SQUARE_PROJECTIVE_STATIONARITY_MASTER_SYSTEM.md).

An exact survivor in either route triggers dedicated validation; it is not an
automatic counterexample or global-status change.

## P6/arbitrary-order boundary

P6 is the first root-parity-compatible deletion-deck case, but the clean
`2 x 3` fan's Segre pullback always meets the coordinate torus and the physical
six-face map is split-surjective. Canonical and `tau=0` exclusions are not
fibre-invariant. A viable P6 continuation must synchronize mixed-colour,
four-deck, or even-Wick data on one legal graph; repeating scalar-face or
single-fibre exclusions cannot close it.

The arbitrary-order two-port factorization remains a valid bridge, but the
coordinate-monomial alternative and all-full-span gluing remain open. The
five-port pentad is exact, while the present null-polar implementation makes it
vanish termwise. Neither route currently closes local-to-global gluing.

## Closed traps and non-evidence

Do not reopen or overclaim the following:

- H31 is generically closed on all 25 P4 components, but generic closure is not
  pointwise divisor/boundary closure.
- Component 22's `h2=0`, `f2=f7`, and slope-zero `f2=f8` subintersection do
  not close the whole `f2`, `f7`, or `f8` factors.
- The high-coordinate CEGAR and named `q5_311`, `q5_221`, and `q4_211`
  forests are closed only in their recorded scopes.
- Odd-root P5/P7 polarization cannot expose even deletion decks.
- GHZ/Segre quadrics, fan nonvanishing, scalar faces, the factor/pentad layer,
  or eight chosen covariants alone do not supply the missing P7 obstruction.
- Fan rank or Veronese transversality alone does not prove physical
  compatibility.
- Expected dimension, finite-field evidence, numerical continuation,
  sampling, timeouts, and modular agreement do not prove characteristic-zero
  emptiness, finiteness, or exhaustiveness.
- A finite-order exclusion, including any remaining order-14 selector work,
  is not an arbitrary-order or global result.

## Completion and stop contract

For a new exact leaf, preserve the repository's standard package shape:

1. a characteristic-zero theorem/reduction note with assumptions and scope;
2. a primary exact verifier or certificate constructor;
3. an independent no-import audit where practical;
4. immutable inputs/hashes and a bounded focused test;
5. explicit `UNKNOWN` boundaries and unchanged global status.

Stop and request a dedicated adversarial review if the work appears to produce
a complete proof route or an exact counterexample. Also stop rather than infer
through an unproved finiteness, case-cover, specialization, audit-independence,
or withdrawn-premise step. A complete local `P5 -> Delta_3` exclusion would
still leave the arbitrary-order/P7 gluing obligation open.
