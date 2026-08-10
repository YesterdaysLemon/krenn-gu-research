# Stage 29 dry run: conflict-free P5 frontier, boundary, and coordinate forest

Status: **EXACT MERGED-BASE MAPPING AND REPAIR SURFACE FROZEN; BATCH NOT
YET COMMITTED OR EXECUTED.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. This dry run freezes
filesystem ownership and executable repair obligations only. It does not
change a theorem, quantifier, divisor or support condition, lifecycle,
evidence role, formalization status, case-cover claim, owner-gated conflict,
or global status.

## Frozen base and proposed batch

Stage 29 starts from merged Stage 28 commit
`1544a930ddfc7012f2814873ff950fe271ecb965`, tree
`66782a81071f1babed9487439de2e9876f028b5a`.

The proposed batch identifier is `p5-frontier-stage29`. It contains exactly
176 tracked root sources and preserves every basename. No selected source is
already moved, no destination exists in the base index, and there are no
duplicate sources, duplicate destinations, source/destination overlaps, or
mapping cycles.

The clean-base root contains 1,165 tracked files and nine directories: 1,174
entries, with 1,158 grandfathered debt entries. Merged-main hygiene run
`31342035667` passed at the frozen base.

## Exact mapping identity

| field | value |
|---|---|
| members | 176 |
| documents | 64 Markdown |
| executable carriers | 110 Python, 2 C++ |
| destination totals | `claims/p5/frontier` 143; `claims/p5/boundaries` 17; `claims/p5/coordinate-cegar` 16 |
| canonical mapping SHA-256 | `6577eb9544a8bcc5c20f0c6a204a7248b1db68ec15331d12281e791baccd5d7e` |
| source-identity SHA-256 | `3b2d83d8bfc520e8d04b6beac9598845d02e04d5af076bde4ebba1c1c935a2e5` |
| run-local mapping artifact SHA-256 | `6752e0ca80ae1132e5f25a83cc94207bda3ceaf5150a946037dc0237ffe5b14e` |
| run-local mapping artifact size | 36,097 bytes |
| mapping verifier SHA-256 | `3f30dd230533106f1afaafa831038cd75e5ca00c49561f5400583338e105f831` |

The source identity is the SHA-256 of compact, sorted-key JSON records with
the exact keys `old_path`, `new_path`, and `git_blob`, sorted by
`(old_path, new_path)`. The `git_blob` value is the base-index blob object ID.
The run-local mapping artifact and its fail-closed verifier independently
reconstruct and validate all 176 records against the clean frozen base.

## Fresh-base membership derivation

The original reviewed-plan derivation was
`252 + 2 + 6 - 66 - 18 = 176`. Stage 28 moved the P4 antecedents that had
kept six q4_211 files outside the old closure. On the merged Stage 28 base,
those six files enter the document/carrier closure directly, so the exact
fresh derivation is:

```text
258 members after removing the high-coordinate conflict triple
+ 2 C++ primaries
- 66 Component21 files
- 18 Component23 files
= 176
```

The closure begins with non-moved manifest members in `p5/frontier`,
`p5/boundaries`, and `p5/coordinate-cegar`. A Markdown claim enters only when
every named current-root Python carrier remains within those families; those
carriers then enter with it. The two C++ primaries are the explicitly named
carriers for the quartic and quintic restriction-equation packages.

Every selected record is already present in the classifier and migration
manifest with the exact reviewed destination and `review_required` status.
Stage 29 requires no classifier refinement and removes nothing from
`catalog/unclassified-files.json`.

The frozen catalog identities are:

| artifact | Git-content SHA-256 |
|---|---|
| `catalog/layout-classification.json` | `dd1b0803f5295594ce5a8d7e2c8b07617a7868fc94028ce741beea3badac5ddf` |
| `catalog/moved-paths.json` | `af4e69c84fea8d9a5979cdfc8196c97978d1584a7a53f0fbfab14023ed3a2959` |
| `catalog/unclassified-files.json` | `1d1cacfa4c59e95a73e26d4ba68d3d5e81f1295ee300777266809ee225174e28` |
| `catalog/theorem-ledger.json` | `0f415042b49598ea18ab083fb320e82b736f536a974fb0bb282d7607f30a6728` |

## Mathematical and evidence boundary

The selected set contains the complete 60-file normalized q4_211 artifact
forest and the complete 49-file normalized q5_221 artifact forest. Complete
means ownership and evidence-carrier closure inside those normalized branches;
neither forest is an exhaustive P5 case cover.

The q5_221 superseded working note moves with its lineage and remains
superseded. No candidate, partial, working, or superseded artifact is promoted
to verified proof evidence by proximity. The separate root
`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION` antecedent remains an exact
characteristic-zero theorem with its own verifier/audit and an explicit wall:
it does not prove P5 or the global conjecture. Its link is repaired; its
ownership is not absorbed into this batch.

No selected path is mapped by the theorem ledger. Stage 29 must not edit a
ledger path, hash, status, scope, evidence role, audit provenance, dependency,
or global field. Ledger completeness remains `partial_curated`, and the global
status remains **UNRESOLVED**.

The exact batch excludes:

- the `P5_HIGH_COORDINATE_PARTIAL_FRONTIER` document and two carriers;
- all 66 Component21 files;
- all 18 Component23 files;
- every closure-crossing alternative-strategy, component-boundary,
  high-coordinate-chart, or specialization-meta-theorem package; the
  `P5_Q5_311_RARE_SLICE_REDUCTION` package; and every other omitted evidence
  package;
- every Component20, H22, H31, Branch B, weighted-`p+q`, internal-`E=0`,
  marked-basis, legacy, or withdrawn conflict surface.

No selected theorem depends on an excluded conflict forest. The known
marked-H31 14-versus-16 theorem/primary contradiction remains a repository
stop condition and is neither moved nor adjudicated. The other three
owner-gated surfaces remain unadjudicated ownership/provenance ambiguities.

## Executable repair freeze

### Import topology

The merged-base AST scan finds exactly 40 crossing import edges across 26
distinct importer files:

| partition | importer files | edge direction |
|---|---:|---|
| staying inbound | 8 | 10 staying-to-selected edges |
| selected outbound | 15 | 21 selected-to-staying edges |
| selected internal cross-destination only | 3 | 9 selected cross-destination edges |

The fresh count is 26, not the older plan count of 25. The additional
internal-only importer is `audit_p5_two_singleton_coordinate_obstruction.py`,
which imports `audit_p5_pair_signature_catalogue_coverage.py` across final
destination directories.

All edges are preserved with 25 new guarded-bootstrap files, one retained
bootstrap, and 18 `expose_claim_package` calls across 16 importers. No qualified
`krenn_gu` import rewrite, helper extraction, algorithm rewrite, or mathematical
replay is required.

### Path, subprocess, and semantic-key topology

The selected Python/C++ surface contains 147 explicit repository references
across 85 files:

- 133 are same-final-directory references;
- 14 are nonlocal: seven direct repository-root paths requiring their reviewed
  destination, five basename semantic keys retained behind a manifest-aware
  resolver, and two paths already rooted through `REPO_ROOT`;
- nine research-snapshot root references across nine files are repaired to the
  reviewed repository-relative targets;
- the staying high-coordinate verifier has four actionable dynamic source/hash
  dependencies that follow the moved P5 targets;
- four subprocess call sites contain zero moved-path literal hits; focused
  post-repair argument-vector and working-directory probes remain required;
- the folded-string scan finds zero additional moved-path literal consumers.

The exact bounded edit union is 33 Python files: 26 importers union 15
path-repair files, with eight overlaps and seven path-only files.
Same-directory references and manifest semantic keys must retain their
existing meaning; only filesystem resolution changes.

The migration-aware Markdown simulation rewrites exactly 129 local links and
172 replay commands across 76 files, with zero ambiguity. A second pass is an
exact `0/0/0` fixed point. This simulation produces no theorem-ledger update.

The line-exact repair inventory and its fail-closed verifier are run-local
freeze artifacts:

| artifact | raw SHA-256 |
|---|---|
| `repair-inventory-1544a93.json` | `4ead2baf8b900e8eea0a44d0ce041fe6c5a4fd9f73c9150053bf0abb43fb51b1` |
| run-local repair verifier | `1b0afc007f25052e230867ff4add5f1024d118f6dfb5ebdc704ab0654a9dbd58` |
| `repair-verification-output.json` | `d6ee1ade68fc35dedc66525a7c44302103e1158c0285450a1c931706193e7233` |

The recorded output is `PASS` at the frozen commit/tree, pins the authoritative
mapping artifact hash, and reproduces every count and both rewriter passes
above.

## Root and manifest projection

Executing only these 176 moves yields:

| measure | before | after |
|---|---:|---:|
| live root files | 1,165 | 989 |
| live root directories | 9 | 9 |
| live root entries | 1,174 | 998 |
| grandfathered debt | 1,158 | 982 |
| manifest moved | 1,199 | 1,375 |
| manifest proposed high-confidence | 45 | 45 |
| manifest review-required | 880 | 704 |

The historical manifest projection is 997 rather than the live 998 because
retained `AGENTS.md` lies outside the original classifier universe. Both
numbers are intentional; the live GitHub root listing is the 998-entry value.

## Execution and acceptance contract

Stage 29 may be approved and executed only after the repair inventory hashes
are pinned and independent reviewers accept this exact 176-member mapping and
repair surface. The required transaction is:

1. commit this dry run and the Stage 28/plan status corrections;
2. create and commit `catalog/batches/p5-frontier-stage29.json` with the exact
   reviewed mapping, base, manifest hash, reviewer, delegation basis, and
   mapping hash;
3. validate the batch geometry and run the executor in dry-run mode;
4. execute exactly 176 `R100` moves plus the executor-owned
   `catalog/moved-paths.json` transition in a pure move commit;
5. run the migration-aware rewriter and commit its exact first-pass result;
6. apply only the frozen import/path/semantic-key repairs and navigation/report
   additions;
7. stage the index-complete candidate tree and require the rewriter fixed
   point, zero stale executable references, and no ledger mutation;
8. run the authoritative validation floor:

```text
python check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v test_fourteen_vertex_cycle_cover_lattice.py
python tools/migration/rewrite_links.py
git diff --exit-code
```

9. obtain independent mechanical, catalog/ledger, and proof-boundary review;
10. publish the exact reviewed head, require hosted CI on that head, merge with
    a head-SHA guard, and require merged-main CI before any Stage 30 decision.

Broad SAT, Singular, numerical, sampling, or theorem reruns are outside this
path-only migration unless a focused repair probe exposes a real discrepancy.
No successful migration or CI run changes the global mathematical status.
