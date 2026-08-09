# P5 H31 single-gate — Stage 17 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08.  No move has yet been executed.**

> **Scientific status will not change.**  The global Krenn–Gu conjecture
> remains **UNRESOLVED**.  This review resolves filesystem ownership only.  It
> does not turn the reduction into an exclusion theorem, extend the two exact
> obstructions beyond the rank-one-gate branch, reinterpret modular audits as
> characteristic-zero proofs, or close all of `H31`.

## Review authority and baseline

- Exact merged baseline:
  `7873c2026423af32dea6055fdee557ceebfcbe20`.
- Branch: `codex/stage17-h31-single-gate-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific status/scope decision, genuinely ambiguous
  proof-boundary decision, or owner-preference architecture choice is needed.
- Batch ID to freeze: `p5-h31-single-gate-stage17`.
- Approval-time manifest SHA-256:
  `79a7b498cffcc338ede0ae0ba2528582a9a5eb1ceafa7920c2bda072005335bc`.
- Canonical mapping SHA-256:
  `7525f91818132db42c0104a366f873441118befe50c0ffcf9d676fe1c765c6a0`.

The approval-time manifest SHA is informational and hashes raw Windows
checkout bytes, so it is platform-specific.  The canonical mapping hash is
the portable, authoritative binding of the approved old-to-new pairs.

All nine manifest records are currently `review_required` with medium
classifier confidence.  That confidence is proposal evidence only.  Approval
comes from the independent ownership, proof-topology, evidence-semantics, and
mechanical reviews and applies only to the mapping below.

## Exact nine-file mapping

| role | source | destination |
|---|---|---|
| reduction | `P5_H31_SINGLE_GATE_P3_REDUCTION.md` | `claims/p5/h31/single-gate-p3/P5_H31_SINGLE_GATE_P3_REDUCTION.md` |
| primary | `verify_p5_h31_single_gate_p3_reduction.py` | `claims/p5/h31/single-gate-p3/verify_p5_h31_single_gate_p3_reduction.py` |
| audit | `audit_p5_h31_single_gate_p3_reduction.py` | `claims/p5/h31/single-gate-p3/audit_p5_h31_single_gate_p3_reduction.py` |
| theorem | `P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md` | `claims/p5/h31/single-gate-rank-two-m-exclusion/P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md` |
| primary | `verify_p5_h31_single_gate_rank_two_m_exclusion.py` | `claims/p5/h31/single-gate-rank-two-m-exclusion/verify_p5_h31_single_gate_rank_two_m_exclusion.py` |
| audit | `audit_p5_h31_single_gate_rank_two_m_exclusion.py` | `claims/p5/h31/single-gate-rank-two-m-exclusion/audit_p5_h31_single_gate_rank_two_m_exclusion.py` |
| theorem | `P5_H31_SECONDARY_GATE_EXCLUSION.md` | `claims/p5/h31/secondary-gate-exclusion/P5_H31_SECONDARY_GATE_EXCLUSION.md` |
| primary | `verify_p5_h31_secondary_gate_exclusion.py` | `claims/p5/h31/secondary-gate-exclusion/verify_p5_h31_secondary_gate_exclusion.py` |
| audit | `audit_p5_h31_secondary_gate_exclusion.py` | `claims/p5/h31/secondary-gate-exclusion/audit_p5_h31_secondary_gate_exclusion.py` |

Every source is tracked grandfathered root debt, every destination is absent,
and the durable classifier and generated manifest contain exactly these
source-to-destination pairs.  There are no destination collisions, duplicate
sources or destinations, double moves, overlap cycles, or package-name
collisions.

All nine working-tree source blobs equal the exact baseline Git blobs:

| source | Git blob |
|---|---|
| `P5_H31_SECONDARY_GATE_EXCLUSION.md` | `1d8374fc1221ceb10a2651b5d42abaaddb6dc196` |
| `audit_p5_h31_secondary_gate_exclusion.py` | `735a14d87d745912b22fa3100eb9756085d3c4d7` |
| `verify_p5_h31_secondary_gate_exclusion.py` | `1b5f28b01e22e36d983db1eda2758345893b92de` |
| `P5_H31_SINGLE_GATE_P3_REDUCTION.md` | `3d15070db66e87c750bde4067cd7b40d6ce86fa9` |
| `audit_p5_h31_single_gate_p3_reduction.py` | `879162a3128d53d40356049c5ec57334a1b272a6` |
| `verify_p5_h31_single_gate_p3_reduction.py` | `8b97dd9ea84fc6d6fb2a969b19bdffe7caecfe4b` |
| `P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md` | `8de629a1e2e853d888b3e235288fe7f4e130cc9b` |
| `audit_p5_h31_single_gate_rank_two_m_exclusion.py` | `cd5fbcd408212397490113d54561db4edd67d1b1` |
| `verify_p5_h31_single_gate_rank_two_m_exclusion.py` | `7ad0fa9ed2b79c28ffdacbcb82c823fabdea4faf` |

## Proof-obligation ownership

The nine files form one asymmetric three-node forest:

```text
upstream decomposable-P3 restriction classification (stays separately owned)
  -> rank-one row pair on the pure hyperplane
       + other three row pairs rank two on M
           -> exact single-gate P3 reduction
           -> exact rank-two-M exclusion
       + at least one further rank drop on M
           -> unique secondary gate
           -> exact secondary-gate exclusion
       => every H31 pure/Delta2 pencil with a rank-one pure-hyperplane
          row pair is excluded

all-rank-two pure-P4 H31, all H31, P5 -> Delta3, and global stay open
```

The reduction is exact characteristic-zero mathematics but is explicitly not
an exclusion theorem.  The rank-two-M theorem closes its stated branch.  The
secondary-gate theorem closes the complementary further-rank-drop branch and,
only together with the rank-two-M theorem, reports
`all_single_gate_H31_excluded: true`.

Evidence axes remain separate:

- each primary verifier replays exact characteristic-zero identities for its
  own document;
- each audit independently reimplements its corresponding symbolic primary's
  calculations using finite-field permanents and row reduction over F5 and F7
  rather than import that primary verifier;
- the rank-two-M and secondary audits reuse arithmetic helpers from the P3
  reduction audit, so the three audits are not mutually no-import independent;
- each audit explicitly reports that it is not a characteristic-zero proof;
  and
- no one of the six executables claims all `H31`, `P5 -> Delta3`, or the
  global conjecture is resolved.

No curated theorem-ledger entry names or hashes any of these three documents.
Migration therefore requires no ledger entry, status, or document-hash edit.

## Explicit exclusions

The exact `P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION` theorem, primary, and
audit remain separately owned upstream.  They are not absorbed merely because
the single-gate reduction consumes the theorem.

Also excluded:

- the all-rank-two P4/H31 component and boundary forests;
- the P4 pure-rank-two toric-boundary package, which is a staying downstream
  consumer of the secondary-gate theorem;
- the high-coordinate frontier, Delta3 obligation ledger, component-boundary
  atlas, and root README, which are staying synthesis or navigation consumers;
- every H22 programme; and
- historical notes and migration provenance.

These exclusions preserve the exact case boundary: closing all branches with
a rank-one pure-hyperplane pair is not a proof that all pure-P4 compressions,
all `H31`, or the global conjecture are excluded.

## Recorded nonblocking provenance conflict

The staying P4 pure-rank-two component theorem still describes the second
diagonal-quadric generic and boundary fibres as open, while later frontier and
navigation documents describe later closures.  That pre-existing conflict is
unrelated to the single-gate forest and does not alter this mapping, but it
must be resolved by a separate scientific provenance audit rather than
silently rewritten during migration.

## Mechanical repair surface

All six moved Python executables currently derive `ROOT` from their source
directory.  After the pure move they must use the shared repository bootstrap:

- `HERE` for each co-located theorem document;
- `REPO_ROOT` for the upstream root P3 theorem and durable ignored `tmp/`
  replay outputs;
- full `REPO_ROOT` package paths for cross-package theorem or audit
  dependencies; and
- `expose_claim_package` before the two moved audits import helpers from the
  new `single-gate-p3/` directory.

The cross-package dependencies are bounded:

1. the P3-reduction primary consumes the staying root P3 classification;
2. the rank-two-M primary consumes the moved P3 reduction document;
3. the rank-two-M audit consumes and imports the moved P3 audit;
4. the secondary primary consumes the moved rank-two-M theorem; and
5. the secondary audit imports the moved P3 audit.

Two staying executables require operational path repair:

1. `verify_p5_high_coordinate_partial_frontier.py` consumes the rank-two-M and
   secondary theorem documents; and
2. `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/verify_p4_pure_rank_two_component_toric_boundary.py`
   consumes the secondary theorem document.

A read-only virtual post-move simulation predicts 12 Markdown-link rewrites
and six fenced replay-command rewrites across six Markdown files, with zero
ambiguities and zero theorem-ledger updates.  Navigation must add a distinct
three-triple single-gate branch forest to `claims/p5/h31/README.md`, update the
parent P5 count from 22 to 25 H31 directories, and identify it as a scoped
branch closure rather than a generic package or complete component closure.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| moved manifest entries | 368 | 377 |
| proposed-high-confidence entries | 246 | 246 |
| review-required entries | 1,401 | 1,392 |
| moved-only manifest root projection | 2,004 | 1,995 |
| high-confidence manifest root projection | 1,758 | 1,749 |
| all-classified manifest root projection | 357 | 357 |
| grandfathered root debt | 1,989 | 1,980 |
| root files | 1,996 | 1,987 |
| root directories | 9 | 9 |
| root entries | 2,005 | 1,996 |
| enforceable retired paths | 368 | 377 |

The move creates no top-level directory and changes no root baseline or
end-state allowlist.

## Replay and acceptance plan

Replay all three primaries and all three audits from repository root using
their destination paths, then repeat all six by absolute path from a foreign
working directory.  Parse one JSON object per run and require the root and
foreign objects to be exactly equal.  All six must report `verified: true`.

Required semantic boundaries:

- P3 reduction: viable locus classified, but `H31_excluded`,
  `P5_to_Delta3_resolved`, and global resolution remain false;
- rank-two-M: its single-gate lift is impossible, but
  `all_single_gate_H31_excluded`, all `H31`, `P5 -> Delta3`, and global remain
  false;
- secondary gate: its lift is impossible and
  `all_single_gate_H31_excluded` is true, while all-rank-two pure-P4 H31, all
  `H31`, `P5 -> Delta3`, and global remain false; and
- all audits retain
  `finite_field_audit_is_characteristic_zero_proof: false`.

Replay both staying executable consumers once from repository root and once
from a foreign working directory, and require equal parsed JSON for each
pair.  The P4 toric-boundary result must remain scoped to its P4 boundary
theorem, and the high-coordinate frontier must retain
`P5_to_Delta3_resolved: false` and `global_conjecture_resolved: false`.

Final acceptance requires exact frozen-batch validation, nine byte-identical
`R100` moves, correct manifest/root arithmetic, no stale operational paths,
six moved-script root/foreign replay pairs with equal JSON, two consumer
root/foreign replay pairs with equal JSON, isolated foreign-CWD import probes
for all eight affected executables, the
index-complete validation floor, exact-head CI, and fresh Tier-2 semantic plus
mechanical review before a normal merge.
