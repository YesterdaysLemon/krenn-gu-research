# GLS66--GLS69 evidence-status reconciliation

## Decision and scope

**Evidence-status reconciliation; no mathematical-scope change.**

At merged base `827377dac50c4d58650e5932d56e37a4ff4cd4e8`, the owning
documents for `GLS66`--`GLS69` still carried `Candidate` status headers even
though their committed hostile reviews say PASS at the exact stated scopes
and `docs/current-frontier.md` already records those scoped conclusions as
`PROVED`.  Under the repository's evidence semantics, `candidate` means a
proposed claim that has not passed the review required for live use.  Keeping
that lifecycle marker therefore contradicted the accepted review provenance
and made the downstream `GLS70`--`GLS80` dependency chain ambiguous.

This reconciliation changes the four owner headers to `Proved exact`, removes
stale candidate wording from their navigation and replay labels, and adds a
focused regression test.  It also promotes GLS66's already-reviewed
provisional conclusion wording from “would exclude” to “excludes.”  It does
not change the underlying proposition, proof, quantifier, field, hypothesis,
divisor, case cover, census, residual family, verifier algorithm, audit
algorithm, or frontier edge.

## Provenance checked

| Claim | Introduction commit | Accepted review evidence | Exact accepted conclusion and retained wall |
|---|---|---|---|
| `GLS66` | `19dbffd9c3e8acfe479756806b3ed9945c5eb308` | [PASS after three hostile reviews](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_TWO_TWO_SCALAR_AXIS_AND_COMMON_HYPERPLANE_EXCLUSION_REVIEW_2026-08-28.md) | The `GLS65` eta-zero `2233` residual, hence the stated exactly-two-deficient branch, is empty; three-plus-deficient and all broader gates remain open. |
| `GLS67` | `26eeb2ed94130f6a0e6f91cfe6c36b35ea9cf233` | [PASS after two hostile reviews and finite replays](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_CLASS_AND_P3_ORBIT_LOCALIZATION_REVIEW_2026-08-28.md) | The common-support orbits are empty and 432 profiles in eight three-deficient orbits remain open. |
| `GLS68` | `3add9a2be620f83751485382a06de8350aed1985` | [PASS after two hostile reviews and finite replays](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_DEFICIENT_PAIR_CLASS_AND_PROBE_DEPENDENT_FOUR_PORT_BOUNDARY_REVIEW_2026-08-28.md) | The 4,794-profile/50-key census and, conditional on accepted GLS63/GLS67, the invalidity of the displayed direct probe-dependent six-vertex reconstruction are proved; no surviving profile is excluded. |
| `GLS69` | `f1c421ea1c1947bca934510a6762fbe1a7c0e1d1` | [PASS after independent hostile review and finite replays](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_REVIEW_2026-08-28.md) | The support/face formulae and stated censuses are proved; the five-/six-deficient branches and shared-deck integrability remain open. |

The hostile reviews were introduced with the corresponding owner documents;
no later promotion commit existed.  The canonical frontier already used the
four results at precisely these scopes.  This is lifecycle-documentation debt,
not a new proof, new review verdict, or newly discovered mathematical result.

## Fresh replay

On 2026-08-29, a local reconciliation replay reran all four primaries and all
four companion audit programs under `tools/research/run_bounded.py` with
180-second wall-clock and 2 GiB memory caps.  It reproduced the reviewed
outputs at their stated finite/displayed layers:

```text
GLS66: displayed scalar/common-hyperplane algebra PASS;
       independent finite/displayed audit PASS.
GLS67: 61,965 -> 2,367 -> 516 -> 453 -> 432;
       ten localized orbits -> eight residual orbits; both replays PASS.
GLS68: 137,781 -> 20,778 -> 4,794; 50 keys; 54/4,740 split;
       probe bidegree (3,3); both replays PASS.
GLS69: N5 P=(59,049,18,270,2,640), U=(236,196,79,095,24,435);
       N6=(531,441,276,750,99,855,99,180), 86 keys;
       675 profiles in four orbits removed by the three-open span;
       both replays PASS.
```

The programs replay finite and displayed algebra only.  The written
same-source, rowspace, support, and receiver-interface arguments remain the
mathematical bridges, exactly as their hostile reviews state.

Each replay used the corresponding command recorded in the owning hostile
review through this bounded wrapper shape:

```powershell
python tools/research/run_bounded.py --run-id <unique-id> `
  --timeout-seconds 180 --memory-mb 2048 `
  --run-root <outside-checkout-log-root> --cwd <isolated-worktree> `
  -- <recorded-primary-or-audit-command>
```

The local runner metadata is not committed evidence.  The durable replay
provenance remains the tracked programs and exact commands in the four hostile
reviews.

## Frontier and ledger consequences

There is no proof-topology delta: the frontier already labels `GLS66`--`GLS69`
`PROVED` and already retains the exact residual branches above.  The
frontier's authority paragraph now records why the owner headers agree with
those nodes.

No entries are added mechanically to `catalog/theorem-ledger.json`.  That
catalogue declares itself `partial_curated` and currently has no
`GLS66`--`GLS69` entries; a future ledger expansion requires separately
reviewed assumptions, provenance, hashes, and typed relationships.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
