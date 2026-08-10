# Layout migration Stage 29 report

Status: **PURE MOVE, MIGRATION-AWARE LINK/COMMAND REWRITE, FROZEN EXECUTABLE
REPAIR, NAVIGATION, AND LOCAL VALIDATION COMPLETE; PUBLICATION, HOSTED CI,
MERGE, AND MERGED-MAIN VALIDATION PENDING.**

The global Krenn-Gu conjecture remains **UNRESOLVED**.  Stage 29 changes
filesystem ownership, executable paths, navigation, and four document-hash
integrity fields only.  It does not change a theorem, quantifier, finite bound,
divisor or support condition, lifecycle, evidence role, formalization status,
case-cover claim, owner-gated conflict, or global status.

## Transaction checkpoints

| role | commit | tree |
|---|---|---|
| merged Stage 28 base | `1544a930ddfc7012f2814873ff950fe271ecb965` | `66782a81071f1babed9487439de2e9876f028b5a` |
| merged-base dry run and repair freeze | `b1c75d56763cba5b74aacd697926ca70d8db98d3` | `23772e4d0cff7bd75aa7170af8633b7f95482530` |
| exact approved batch | `3e4cec1bbf5c0867276b25ff275ee7dc393e4511` | `69106aac657df31988853b272c2755680fa4b3db` |
| pure 176-file move | `169ba6dcc4d11330845e83693bc506160dc205b2` | `dd96a76d3681401dbb6e874a6e0d4968e434907b` |
| migration-aware link/command rewrite | `2976efb02090952de0ecf0d44e1428993f90f6ea` | `722c2afea1a912a19607edb5a5fb1b6a108fb915` |
| executable repair, navigation, and local validation | `e73711982fe7bef166fb2683bf3a8c5679f3192f` | `c4fbf98990ed24cc970023d1efe8e1efa9c38969` |

Batch: [`p5-frontier-stage29`](../../catalog/batches/p5-frontier-stage29.json).
Dry run: [`p5-frontier-stage29-dry-run.md`](p5-frontier-stage29-dry-run.md).

## Exact mapping identity

| field | value |
|---|---|
| members | 176: 64 Markdown, 110 Python, two C++ |
| destinations | `claims/p5/frontier` 143; `claims/p5/boundaries` 17; `claims/p5/coordinate-cegar` 16 |
| canonical mapping SHA-256 | `6577eb9544a8bcc5c20f0c6a204a7248b1db68ec15331d12281e791baccd5d7e` |
| source-identity SHA-256 | `3b2d83d8bfc520e8d04b6beac9598845d02e04d5af076bde4ebba1c1c935a2e5` |
| run-local mapping artifact SHA-256 | `6752e0ca80ae1132e5f25a83cc94207bda3ceaf5150a946037dc0237ffe5b14e` |
| run-local mapping artifact size | 36,097 bytes |
| run-local mapping verifier SHA-256 | `3f30dd230533106f1afaafa831038cd75e5ca00c49561f5400583338e105f831` |

The pure-move checkpoint contains exactly 176 `R100` renames.  Each new-path
blob is identical to its frozen old-path blob.  The only other pure-move
change is the executor-owned `catalog/moved-paths.json` transition: the same
176 rows change from `review_required` to `moved`, gain
`executed_batch: p5-frontier-stage29`, and update aggregate counts.

After the move, the tracked root has 989 files and nine directories, or 998
entries.  Grandfathered root debt is 982.  The manifest's historical
projection is 997 because retained `AGENTS.md` is outside its original
classifier universe.  The live Git root value is 998; after publication, the
GitHub root listing should expose the same 998 entries.

## Mathematical and evidence boundary

The moved set contains the complete 60-file normalized `q4_211` artifact
forest and complete 49-file normalized `q5_221` artifact forest.  Complete
means ownership/evidence-carrier closure inside those normalized branches;
neither is an exhaustive P5 case cover.  The `q5_221` triangle working note
remains superseded.  No candidate, partial, working, or superseded artifact is
promoted by proximity.

The exact characteristic-zero
`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION` theorem, its primary, and its
audit remain separately owned at repository root.  It is a structural
antecedent, not by itself an exclusion of `P_5 -> Delta_3` or a proof of the
global conjecture.

The exact batch excludes the high-coordinate conflict triple, all 66
Component21 files, all 18 Component23 files, and every closure-crossing
package, including `P5_Q5_311_RARE_SLICE_REDUCTION`.  Component20, H22, H31,
Branch B, weighted-`p+q`, internal-`E=0`, marked-basis, legacy, and withdrawn
conflict surfaces remain outside the move and unadjudicated.

The four owner-gated conflicts remain unchanged:

1. the H31 chart-boundary marked-fibre theorem says 14 certificate strata,
   while its primary asserts and reports 16;
2. P4 internal-`E=0` versus chart `D=0,a!=0` attribution remains unresolved;
3. first/second-component provenance and closure disagree across marked-basis,
   toric, high-coordinate, outer-boundary, README, and synthesis artifacts;
4. weighted-H22 `p+q=0` status disagrees between the dedicated root forest and
   migrated aggregate provenance.

Conflict 1 remains a repository stop condition.  Conflicts 2-4 remain
ownership/provenance ambiguities, not adjudicated mathematical
contradictions.  Arbitrary P7/local-to-global remains **UNKNOWN**, and the
global conjecture remains **UNRESOLVED**.

No selected path is mapped by `catalog/theorem-ledger.json`.  The pure-move and
rewrite commits did not touch the ledger, but post-rewrite hygiene correctly
found four stale document hashes: zero-based entries 0, 65, and 71 now pin
root `README.md` as `d4c1c0fe5c6fe19d`, and entry 17 pins
`claims/arbitrary-order/SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md` as
`b5806984afb34ec9`.  The candidate refreshes only those four
`document_sha256_16` fields.  All statuses, scopes, evidence roles,
provenance, dependencies, completeness `partial_curated`, and global status
`UNRESOLVED` remain unchanged.

## Rewrite and frozen repair surface

The rewrite checkpoint changes exactly 76 Markdown files: 129 local-link
targets and 172 replay-command script paths.  The 301 old/new line pairs are
otherwise text-identical.  It changes no theorem/status prose and produced no
automatic ledger update; the later four hash-only integrity refreshes are
recorded above.  Staying root claim documents touched by the rewrite are only
path consumers.

The frozen executable repair inventory records exactly 40 crossing import
edges across 26 importer files:

| partition | importer files | edges |
|---|---:|---:|
| staying inbound | 8 | 10 |
| selected outbound | 15 | 21 |
| selected internal cross-destination only | 3 | 9 |

The implemented import repair uses 25 new guarded bootstraps, one retained
bootstrap, and 18 `expose_claim_package` calls across 16 importers.  The
selected Python/C++ surface has 147 explicit repository references across 85
files: 133 same-final-directory references and 14 nonlocal references.  The
nonlocal set consists of seven direct root paths, five basename semantic keys,
and two paths already rooted through `REPO_ROOT`.  Nine research-snapshot root
references, four dynamic source/hash dependencies in the staying
high-coordinate verifier, and four subprocess call sites are separately
recorded.  The exact bounded edit union is 33 Python files: 26 importers union
15 path-repair files, with eight overlaps and seven path-only files.

Run-local repair artifacts are pinned as follows:

| artifact | raw SHA-256 |
|---|---|
| `repair-inventory-1544a93.json` | `4ead2baf8b900e8eea0a44d0ce041fe6c5a4fd9f73c9150053bf0abb43fb51b1` |
| repair verifier | `1b0afc007f25052e230867ff4add5f1024d118f6dfb5ebdc704ab0654a9dbd58` |
| `repair-verification-output.json` | `d6ee1ade68fc35dedc66525a7c44302103e1158c0285450a1c931706193e7233` |

These hashes freeze the authorized repair surface.  The implemented candidate
matches that surface; the focused probes and authoritative validation results
are recorded below.

## Repair and local validation

Executable repair is complete and confined to the frozen bootstrap,
package-exposure, direct-path, semantic-key, research-snapshot, dynamic-source,
and subprocess surface.  The frozen union contains 33 Python files: 32 have
path/bootstrap changes, while
`claims/p5/frontier/verify_p5_pair_signature_catalogue_coverage.py` already
satisfied its retained-bootstrap and `REPO_ROOT` contract and remains
byte-identical.  No mathematical algorithm, assertion, theorem document, or
excluded conflict claim changes.  No ledger field changes except the four
enumerated document-hash refreshes.

Focused compile, foreign-working-directory import, provider-resolution,
semantic-key, research-snapshot, dynamic-source, and subprocess argument/cwd
probes pass on the exact frozen surface.  The index-complete candidate then
passes the authoritative local floor:

- `python check_hygiene.py`: PASS; 1,699 Python files compile, all 847 Markdown
  links resolve, and all 86 ledger hashes match;
- `python -m unittest -v tests.test_migration_tools`: PASS, 152 tests;
- `python -m unittest -v test_fourteen_vertex_cycle_cover_lattice.py`: PASS,
  14 tests;
- `python tools/migration/rewrite_links.py`: exact `0/0/0` fixed point with no
  ambiguity or ledger update, followed by clean `git diff --exit-code` and
  `git diff --cached --check`;
- independent repair-surface, catalog/ledger, and proof-boundary review: PASS.

The exact repair checkpoint is pinned above.  Publication, exact-head hosted
CI, guarded merge, and merged-main CI remain **PENDING**.

No local success, publication event, or CI run changes the mathematical
status.  Broad SAT, Singular, numerical, sampling, and theorem reruns remain
outside this path-only migration unless a focused repair probe exposes a real
discrepancy.
