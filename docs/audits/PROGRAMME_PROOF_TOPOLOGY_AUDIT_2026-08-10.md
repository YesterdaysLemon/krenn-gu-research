# Programme proof-topology audit — PR #72 through PR #82

## Verdict

The global Krenn–Gu conjecture remains **UNRESOLVED**.

PRs #72–#82 add exact and useful arbitrary-order reductions, conditional
exclusions, observability boundaries, and route refutations. They do not form
a global proof or counterexample. The decisive missing edge is still universal
extraction, synchronization, and local-to-global gluing: no theorem forces
every hypothetical witness into a local P5/P6/P7 cell whose physical data
glue across charts and deletion depths.

This audit found documentation drift substantial enough to obscure that edge.
It therefore replaces the stale current map, preserves the displaced text as
history, and records the reviewers' disagreements instead of resolving them by
recency or metadata.

## Audited range and method

- Base before PR #72:
  `70a6d03125a8164940bed3d27980d489724308aa`
- Audited merged head after PR #82:
  `367eef49e5917a0f71594dce4c18a608850cdd6a`
- Merged-head hosted hygiene run: `31443271460`, successful
- Range size: 43 files changed, 12,303 insertions, 17 deletions

Two fresh read-only reviewers worked from a clean worktree whose `HEAD` and
`origin/main` both equalled the audited head:

1. `programme_proof_graph_reviewer` reconstructed mathematical nodes and typed
   edges from owning theorem prose. It separately checked PR-head/merge-tree
   identity, replayed the 26 focused primary/audit scripts added in the range,
   and ran repository hygiene. Those bounded scripts all passed; they remain
   supporting evidence rather than the arbitrary-order proof.
2. `programme_scope_reviewer` inspected assumptions, generic/pointwise and
   local/global jumps, missing case branches, provenance, navigation, ledger
   semantics, and documentation drift. It did not edit the worktree.

The reviewers were instructed not to infer mathematical dependencies from
imports, filenames, hashes, execution relationships, or the ledger's empty
dependency arrays.

## PR-to-result reconstruction

| PR | Merge SHA | Exact programme contribution | Boundary retained |
|---:|---|---|---|
| #72 | `84a2b6616e5d589156aac114d5fb6b8d87ac85cc` | Excludes simultaneous balanced all-bridge `Delta(D)<=3`; separately proves a boundary to automatic characteristic-two lifting | Higher degree, deeper blockers, gluing, and external Lean correspondence remain open |
| #73 | `633e1015b47421d5a857359548fe922d586ddc31` | Strengthens the all-bridge exclusion to maximum degree four | `Delta(D)>=5` and deeper blockers remain |
| #74 | `cb77e5323b83705d791df7ea51a4b83c2f9248bf` | Exposes the complete even deck with balanced sensors and proves the full-sensor/rank-drop dichotomy | Neither full-sensor Wick globalization nor witness-locus rank drop is excluded |
| #75 | `eef92672a8c8e6f4285a044686b272de11250d8e` | Gives the universal maximum-root split: `r=1` matrix units versus `r>=2` fixed surplus | Both branches remain |
| #76 | `4793e082f0bbcb8e3261ee8951ecbc7adeaf4a7c` | Gives exact cofactor/cycle normal forms and conditional rigid-colour factorization | Backbone cancellation alone is refuted, not the branch |
| #77 | `83ae890cb563b2730a8ef22da07aeafcb3bcac0d` | Reduces the matrix-unit branch to at most four ports and proves the rigid three-block/dual-bridge system | Arbitrary-order rigid exclusion and proper flags remain open |
| #78 | `a858617c544f9568757bbd49b0f327f9f519e122` | Proves primitive sharpness and excludes two naive physical completions | General cancelling completion remains open |
| #79 | `f22bd52e120d48c205a16076766c573abe7fa020` | Adds cross-parity erasure, bridge/deeper entry, rigid-head Wick, and pseudoforest structure | Word synchronization, flag propagation, erased `r>=2`, and deeper branches remain |
| #80 | `6e12795371e40a771c75cabe956ed04948a4e6be` | Connects fixed surplus to balanced sensors; proves truncation and zero/single-open nonobservability | Higher mixed roots and unfactorized outside blocks remain |
| #81 | `90bdffe87ef5bfcae07c3a71c63d5fe16f4086fe` | Gives the complete two-open equation and a conditional tight-star tensor gauge | It constructs neither the tight layer nor a witness; no universal detector follows |
| #82 | `367eef49e5917a0f71594dce4c18a608850cdd6a` | Proves bridge promotions change the exact word and isolates the word-shore matching target | Both six-vertex graphs are non-witness countermechanisms |

PRs #72–#74 are two-parent merges; #75–#82 are squash merges. For each PR,
the final merge tree equals the reviewed PR-head tree.

## Mathematical reconstruction

The reviewers agreed on two universal lenses for every hypothetical ternary
witness.

### Balanced-sensor lens

The [balanced half-sensor theorem](../../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md)
exposes the complete even principal-hafnian deck. It leaves an exact dichotomy:

- on a generically full sensor, the unique rational lift must extend without
  poles to one physical graph and satisfy the all-order Wick equations; or
- every balanced partition is identically rank-deficient on the witness.

The rank-drop locus is proved proper in ambient block-graph space, not after
intersection with the hypothetical-witness incidence variety. PRs #80–#81
show why a fixed-surplus layer and its first two open-root contractions do not
by themselves decide this dichotomy.

### Maximum-root lens

The [maximal torus-root theorem](../../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md)
gives a pointwise exhaustive split:

- `r>=2` yields one complete fixed-surplus physical hafnian layer. Physical
  synchronization, higher surplus, and unfactorized detection remain open.
  At zero surplus this is a weighted `P_r -> Delta_3` restriction for arbitrary
  `r>=5`; no theorem reduces every `r>=8` case to the committed P7 sensor.
- `r=1` forces every physical block to be one nonzero matrix unit. The branch
  reduces to finite-port responses, rigid and nonrigid flag cells,
  bridge/deeper alternatives, and exact wordwise cancellation. The minimum
  `k=1`, `k=2`, and `k=3` port cells all remain open; `k=4` alone forces
  rigidity in the minimizing base colour.

The [word-synchronization boundary](../../claims/arbitrary-order/MATRIX_UNIT_BRIDGE_WORD_SYNCHRONIZATION_AND_WICK_SHARPNESS_BOUNDARY.md)
proves that parity, bridge normalization, Wick/cut identities, global pure
matchings, and fully active pure cofactors do not force a word-preserving
diagonal rematching. The smallest stated positive target is a theorem forcing
Tutte's condition on every actual word shore, or a different global rematching
mechanism.

### Conditional all-bridge and local programmes

Inside the conditional simultaneous balanced all-bridge branch, PRs #72–#73
exclude saturated-diagonal maximum degree at most four. They do not extract
that branch from every witness and do not cover `Delta(D)>=5` or deeper
blockers.

The P5, P6, and P7 programmes remain valuable local leaves. The committed P7
criterion is not a decision of its residual algebra, and a decision on that
fixed sensor would not globalize automatically. The P6 restriction remains
open rather than being absorbed by the P5/P7 lanes. The P5 component forest
contains generic and divisor-specific results with surviving special and
projective boundaries. Even a complete local exclusion at any of these ranks
would still require the universal extraction/gluing edge.

The maintained [current frontier](../current-frontier.md) records the resulting
25-node graph and its typed edges.

## Hostile scope and provenance findings

1. **Stale authority base.** The dated handoff declared PR #76
   (`4793e082...`) and workflow `31428495352` as its operational base while the
   same file had accumulated results through PR #82. It is now historical; the
   maintained frontier pins the audited reconstruction instead.
2. **False local-to-global impression.** The 2026-08-05 frontier still said
   completed pointwise P5 closure, plus colour reduction, would imply the
   conjecture. The later owning evidence explicitly retains arbitrary-order/P7
   extraction and gluing. The old claim is preserved historically but removed
   from current authority.
3. **Stale component shorthand.** The old frontier retained “24-of-25” and
   “Component 22 sole hole” language after later Component 25 and P4-B3
   qualifications. Current navigation no longer compresses those branches.
4. **P4 multi-axis disagreement.** The owning P4 reduction asserts that 25
   component closures exhaust the pure-P4 incidence. The handoff and ledger
   retain P4-B3 as an open human audit of nonzero-pure-factor, symmetry,
   inclusion, and lower-pair quantifiers. This is recorded as a theorem claim
   with an audit-acceptance gap, not flattened to “unproved” or “fully audited.”
5. **Ledger overstatement.** The master-schema ledger note said
   `schema + (star) => conjecture`, while the owning obligation ledger proves
   only the local `P5 -> Delta_3` implication. The ledger note is narrowed in
   this change; no dependency graph is populated.
6. **Ledger ownership drift.** The component-census checkpoint and the live
   Component 22 partial entry used the 5,835-line root README as their claim
   document. They now point to the P4 exhaustiveness owner and the scoped
   finite-`D23` partial owner respectively. The global problem-statement entry
   continues to point to the new concise README, which now owns only the
   original conjecture statement and navigation.
7. **External formalization boundary.** The characteristic-two note proves a
   local algebraic route obstruction. It does not upgrade the source-inspected
   external Lean candidate: local build replay and definition correspondence
   remain pending.
8. **Review provenance is not durable for the earlier PRs.** PR descriptions
   report fresh mathematical and hostile-scope reviews, but PRs #72–#82 have
   no GitHub review objects or comments and no committed reviewer reports.
   This does not invalidate the written proofs; it means those prior review
   attestations cannot be independently reconstructed from durable records.
9. **No accidental global status promotion found.** Every owning document in
   PRs #72–#82 retains global `UNRESOLVED`. The failures were missing edges and
   stale navigation, not a hidden global `PROVED` claim.
10. **The committed P7 lane is not arbitrary permanent closure.** Zero surplus
    exposes weighted `P_r -> Delta_3` for every `r>=5`; the arbitrary `r>=8`
    branch remains live and is now a separate frontier node.

## Disagreements and remaining doubts

The reviewers did not resolve the following by fiat:

- whether the P4 owner's component-exhaustiveness proof passes the independent
  P4-B3 semantic/composition audit;
- whether the all-balanced rank-drop locus is empty on the witness incidence
  variety;
- whether the full-sensor rational deck extends pole-free and Wick-complete;
- whether higher mixed roots detect every unfactorized fixed-surplus witness;
- whether the live P6 restriction and every arbitrary zero-surplus
  `P_r -> Delta_3` restriction beyond the locally studied ranks are
  impossible;
- whether higher mixed identities force word-shore Tutte inequalities;
- whether the all-bridge `Delta(D)=5` or deeper-blocker branches are empty;
- whether the remaining P5 divisors and committed P7 algebra close locally;
  and, even if they do, whether a universal extraction/gluing theorem exists.

These are explicit obligations, not implicit assumptions.

## Documentation relocation inventory

The original documents are read from the pinned audited Git tree. The
repository verifier
[`tools/documentation/verify_frontier_relocation.py`](../../tools/documentation/verify_frontier_relocation.py)
reconstructs each archive byte-for-byte after only documented link rewriting:
local Markdown link targets are resolved from the old location, mapped through
the three-path relocation table, and re-expressed from the archive location.
Three exact link labels containing retired research-notes or current-frontier
path names are normalized to their live descriptions. Prose, headings, code
fences, line counts, and scientific status text are untouched.

| Source at `367eef49...` | Historical destination | Lines | Links re-anchored | Source SHA-256 | Archive SHA-256 |
|---|---|---:|---:|---|---|
| `README.md` | `docs/history/repository-readme-chronicle-through-2026-08-10.md` | 5,835 | 737 targets; 3 retired-path labels | `2256187bb842350abca125283f784f8b96876d5652f834ffba27d7ec1c3541fd` | `84bb7d330761dd94931908c725f651dbee6a34583bf86d09f4dbad03d1d63735` |
| `docs/current-frontier.md` | `docs/history/current-frontier-stabilization-snapshot-2026-08-05.md` | 246 | 18 | `1fbbe41a5aafee627aff6bc3fbe36936988d8753427b3b2649bffcb95233d782` | `1cd173e3a956ad20c0e748431dd1be01fa9d323389633b09b795d7ab231dbd19` |
| `docs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md` | `docs/history/handoffs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md` | 484 | 30 | `25e748ee5063691a940c36fcdca0b9df706e65f8e1ac6b55300ac501ba542799` | `9a3c1082ad052a75a70dc6ab1d1243ca69a94585f7c54e9f5643e27dcecbae0d` |

The root README is now a short front door. The old handoff path is a historical
redirect. Claim-family READMEs remain navigation indexes; the theorem ledger
remains `partial_curated` with `dependencies` reserved and unpopulated.

## Review of the maintenance rule

Both fresh reviewers reviewed the new `AGENTS.md` rule. It requires a PR that
changes the live mathematical frontier to update `docs/current-frontier.md`;
a PR that changes mathematical claims while leaving the frontier unchanged
must instead explain why no frontier update is needed. They agreed that this
two-case rule is scope-preserving because the frontier does not replace an
owning theorem, evidence carrier, or formalization record.

## Validation verdict

The index-complete candidate passed the bounded documentation floor:

- the deterministic relocation verifier reconstructed all three archives and
  reported `lossless_except_documented_link_rewriting: true`;
- the new root README has 98 lines;
- repository hygiene passed with 893 Markdown files, 98/98 ledger hashes, and
  root debt `0/0`;
- all 191 migration-tool regressions and all 14 cycle-cover lattice
  regressions passed;
- the documentation link rewriter made zero changes on its idempotence pass;
  and
- Ruff check and format check passed for the relocation verifier.

Both original read-only reviewers rereviewed the final staged candidate. The
proof-graph reviewer returned PASS after the P6 branch, exact-erasure edge,
and identifier namespace were corrected. The hostile-scope reviewer returned
PASS after the maintenance rule and its programme-audit description were
tightened. Hosted CI must still pass at the exact pushed head before merge.
No global status change is proposed. No scientific package is moved, merged,
or promoted by this documentation change.
