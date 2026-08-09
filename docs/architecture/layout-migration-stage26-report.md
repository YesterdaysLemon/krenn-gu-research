# Layout migration Stage 26 report

Status: **SUBSTANTIVE STAGE 26 COMPLETE AND VALIDATED ON BRANCH; AWAITING
REPORT-INCLUSIVE VALIDATION, FRESH FINAL REFEREES, FINAL PULL-REQUEST CI,
AND HEAD-GUARDED MERGE.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. Stage 26 changes
filesystem ownership, replay paths, navigation, and mechanically derived hash
metadata. It does not promote a generic-component `lambda=0` slice to
pointwise special fibres, projective marking charts, the whole component,
component exhaustiveness, arbitrary-order gluing, or the global conjecture.

## Exact reviewed transaction

- Merged-main baseline:
  `cd97b313b021e26ad6391fbb7a1cf08db958f8e6`.
- Branch:
  `codex/stage26-h22-finite-lambda-zero-all-marking-migration`.
- Dry-run approval commit:
  `0cbcc0f9a74ef300a2a1c62d971d0d8fcfc490c9`.
- Frozen-batch commit:
  `263cabec98c19615fb4edac5fadc33d369197f52`.
- Pure-move commit:
  `d0889abcba18370d36b701af889d12b1a954d194`.
- Repair/substantive head:
  `3e501cbe36a6133d02afe85ff68eaf1bf097a9a7`.
- Substantive tree:
  `7191c8c2c7d1a5c55cc0a114a4f97557c73a0c3c`.
- Batch ID:
  `p5-h22-finite-lambda-zero-all-marking-stage26`.
- Canonical mapping SHA-256:
  `06622ad9c8ab149021fd4d3a5c412327db4a28cd2f210d339418d118a7e85131`.
- Actual reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Publication vehicle:
  [draft pull request #58](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/58).

The approved ownership analysis is recorded in
[`p5-h22-common-center-kernel-star-component-finite-lambda-zero-all-marking-stage26-dry-run.md`](p5-h22-common-center-kernel-star-component-finite-lambda-zero-all-marking-stage26-dry-run.md),
and the executable batch is frozen in
[`catalog/batches/p5-h22-finite-lambda-zero-all-marking-stage26.json`](../../catalog/batches/p5-h22-finite-lambda-zero-all-marking-stage26.json).
Classifier confidence supplied proposal evidence, not review authority.

## Moved proof-obligation boundary

Exactly three files moved flat into
`claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/`:

1. `P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ZERO_ALL_MARKING_OBSTRUCTION.md`;
2. `verify_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py`; and
3. `audit_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py`.

The selected leaf is characteristic-zero work over the generic component
field `K=Q(r,t)`. It covers component 23, the finite homogeneous-weight chart
at `lambda=0`, every affine marking `h0,h1,h2,h3`, and the shared `D01/D23`
mixed-extension system. Its load-bearing predecessor is the dense-open
supplement, which supplies the factor cover

```text
h2*h3*H0=0,

H0 = (4*r^2 - 2*r*t - 2*r + 2*t^2 + 2*t - 4)*h3
     - r^2 - r*t + r - t + 2.
```

The selected primary does not prove that cover. It closes exactly the three
residual branches `h2=0`, `h3=0`, and `H0=0` by full-module certificates.
The prior cover plus those three leaves closes only the complete
`lambda=0` all-affine-marking slice at the generic component point.

The audit imports no repository module and reconstructs the three branch
modules over exact `Q` at `(r,t)=(2,4)`, where the `H0=0` branch uses
`h3=3/8`. It shares Singular machinery, does not audit the factor cover, and
is neither an independent generic `Q(r,t)` proof nor a complete independent
audit of the theorem.

The selected theorem's residual `UNKNOWN` prose and the primary's
`generic_finite_all_markings_closed: false` field are chronological and
leaf-local. The later ordinary-residual theorem consumes the complete
`lambda=0,1,-1` slices plus ordinary branches and closes the generic finite
case union at its stated scope. Both records remain truthful; Stage 26 edits
neither mathematical status.

Special parameter divisors, projective marking or weight charts, the whole
common-center-kernel-star component, component exhaustiveness, wider
source-torus or ambient degenerations, `P5 -> Delta3`, arbitrary-order
local-to-global gluing, and global resolution remain outside this package.
Stage 26 also does not consume or adjudicate the owner-gated H31
chart-boundary marked-fibre conflict: its theorem says fourteen certificate
strata while its primary constructs, asserts, and reports sixteen.

## Baseline, pure move, and repair

The first baseline wrapper attempted to use PowerShell/.NET
`ProcessStartInfo.ArgumentList`, failed before `Process.Start`, and launched
zero scientific processes. The infrastructure-only record is preserved at
`C:\Users\Yeste\.codex\run-artifacts\stage26-baseline-cd97b313b021e26ad6391fbb7a1cf08db958f8e6-20260809T160643Z`.

A separately authorized corrected collection then ran the selected primary,
selected audit, and staying dense-open primary exactly once each, strictly
serially, with no retry. All three returned rc=0, empty stderr, and one JSON
object. Their elapsed times and captured stdout SHA-256 values were:

| executable | elapsed s | captured stdout SHA-256 |
|---|---:|---|
| selected `Q(r,t)` primary | 15.1499832 | `82a2f4f35afa63ca69b0000e002ed5d0d9916b558fd231055e5647d37c972004` |
| selected exact-`Q` audit | 6.7623319 | `0ef8123b3dc8c1305793d509e471f6167fc6af11f494af609965412043cf4c23` |
| staying dense-open primary | 10.5731619 | `aa0c198261388168d8306ba383aa8c055e5bba9df324aa8832c0c4119277c95f` |

The corrected artifacts are preserved at
`C:\Users\Yeste\.codex\run-artifacts\stage26-baseline-cd97b313b021e26ad6391fbb7a1cf08db958f8e6-20260809T160643Z-corrected`.
Offline checks matched exact schemas and source/provider identities, verified
`H|lambda=0=H0`, preserved all scope/status fields, and found no generated
repository JSON.

Against its direct parent, `d0889abc` contains exactly three `R100` moves
plus the corresponding manifest transaction. Scientific bytes are identical
across the move. The manifest changes only the selected records from
`review_required` to `moved`:

| measure | before | after |
|---|---:|---:|
| total records | 2,015 | 2,015 |
| moved | 408 | 411 |
| proposed high-confidence | 242 | 242 |
| review-required | 1,365 | 1,362 |
| unclassified | 348 | 348 |
| measured root files | 1,956 | 1,953 |
| root directories | 9 | 9 |
| grandfathered root debt | 1,949 | 1,946 |
| new root debt | 0 | 0 |
| retired/provenance paths | 408 | 411 |
| tracked files under `claims/` | 412 | 415 |
| H22 package directories | 19 | 20 |
| H31 package directories | 31 | 31 |

Commit `3e501cbe` repairs exactly eight files: the moved theorem, primary, and
audit; root `README.md`; the P5 and H22 navigation READMEs; the theorem
ledger; and `docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md`. No equation, branch,
module assertion, timeout, JSON field, or scientific status changed.

The moved primary now installs shared bootstrap before its repository
imports and exposes the migrated H31 provider package. The audit remains
free of repository imports and gains only a portable launcher selecting
native `Singular -q`, then `wsl.exe --exec /usr/bin/Singular -q`, or failing
clearly. The deterministic rewriter changed two links and four fenced
commands across three Markdown files; the theorem's inline-code predecessor
reference received one separately reviewed ordinary Markdown link. The
second rewriter pass was a `0/0/0` fixed point with no ambiguity.

The ledger remains at 86 entries and gains no selected-theorem entry.
Exactly three existing root-README-backed hashes changed to
`a0cf89174c320e7b`; their statuses remain `open`, `verified_generic`, and
`partial`. Key final normalized-LF SHA-256 pins are:

| file | normalized-LF SHA-256 |
|---|---|
| moved theorem | `0d4f2d89f9d11359dc594a065617263688e7119a99d516dffcaa9933d91f85d3` |
| moved primary | `ccc9e14059649b9e6918e020373eba205799d6ad5ec2e4eb3bad2212d0456ba7` |
| moved audit | `c818b712e74699fece78aceb0d7dab75a9c2133956db30dbbcd33a36abf7c5bb` |
| historical handoff | `ddbcca43fdeeb06b3deb74cfdc7ee74ec24ebd880c856706c5d925a47875998f` |
| root README | `a0cf89174c320e7b77a14f94c6322755bd9db8613ebacb8b17c8138049fd5b03` |
| theorem ledger | `a79f86dc6c4bc6d7c0530087a6197f1d3ce63e27d4042d19d800a62d2891d79b` |

## Exact post-move replay

The complete affected scientific closure was three unique executables and
five invocations. Every row ran exactly once, strictly serially, through
`uv run --quiet --python 3.13 --with sympy python`, with no retry,
`python-sat`, priority change, or process intervention. The total scientific
elapsed time was 50.4137666 seconds.

| row | executable/context | elapsed s | stdout SHA-256 |
|---:|---|---:|---|
| 1 | staying dense-open primary, root | 11.1073439 | `ce3694d16d3c4a2a4585487599a1fee6bc8ffb1387a5c62aabe3598e2c95c9d9` |
| 2 | moved primary, root | 13.1050292 | `d15ad537f183824fb4196dd33ba35db970ecb2565de10dbdd417163116bb360f` |
| 3 | moved primary, foreign CWD | 12.0803270 | `d15ad537f183824fb4196dd33ba35db970ecb2565de10dbdd417163116bb360f` |
| 4 | moved audit, root | 7.0724304 | `acfb23f7feab97dbd8fd535079e67c0e10601b61cc3bc8beb180da7a42ce6a20` |
| 5 | moved audit, foreign CWD | 7.0486361 | `acfb23f7feab97dbd8fd535079e67c0e10601b61cc3bc8beb180da7a42ce6a20` |

All five rows returned rc=0, empty stderr, and exactly one JSON object. Each
root/foreign pair was byte- and object-identical. The matrix represents
exactly fifteen serial Singular subprocesses. Separate import-only foreign-
CWD probes passed once each: primary in 2.0236260 seconds and audit in
6.0540972 seconds, both rc=0 with empty stderr. Offline checks independently
confirmed `H|lambda=0=H0` and `H0(2,4,3/8)=0`. The scripts generated no
repository JSON, foreign directories stayed empty, and tracked/index state
remained clean.

Every first stdout, stderr, return code, timing, argument vector, and offline
assertion is preserved outside the repository at
`C:\Users\Yeste\.codex\run-artifacts\stage26-acceptance-3e501cb-20260809T170257245Z`.

## Validation and publication boundary

At exact substantive head `3e501cbe` and tree `7191c8c2`, the complete
pre-report local floor passed:

- `check_hygiene.py`: all 1,698 Python files compile, all 826 Markdown files
  have resolving local links, all 86 ledger hashes match, root is 1,953 files
  plus 9 directories, root debt is `1,946 grandfathered / 0 new`, all 411
  provenance records pass, and manifest counts are
  `411 moved / 242 proposed / 1,362 review_required`;
- all 152 migration-tool tests in 10.540 seconds;
- all 14 fourteen-vertex cycle-cover lattice tests in 0.003 seconds; and
- deterministic rewriter output `links=0 / replay=0 / files=0`, with clean
  tracked and index state.

The substantive
[`hygiene` workflow_dispatch run 31325904337](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31325904337)
succeeded at the exact substantive head; job `93276122040` concluded
success. This was a `workflow_dispatch` event, not final pull-request CI.

Adding this report changes the candidate tree and raises the Markdown count.
Therefore the report-inclusive index-complete floor, fresh final
semantic/status and mechanical/provenance referees, final exact-head
pull-request CI, and the normal head-guarded merge remain mandatory. Their
verdicts belong in the pull-request trail and must not be preclaimed here.

## Stop boundary

Stage 26 stops at the finite `lambda=0` all-affine-marking slice over
`Q(r,t)` at the generic component-23 point, with the earlier dense-open
factor cover remaining load-bearing. It does not begin Stage 27, adjudicate
any owner-gated scientific conflict, or change any global mathematical
status.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
