# Stabilization and integrity audit report

Date: 2026-08-05.  Branch: `stabilization-integrity-pass`, forked from
`main` (`f24782f`, post PR #27).  Authoritative status of the global
conjecture is unchanged: **UNRESOLVED**.

This pass did not attempt new mathematics.  Its purpose was to make the
repository trustworthy and navigable for an outside mathematician
(Professor Krenn or a referee) who must assess the strongest results
without reconstructing the full agent history.

## What was done

### 1. Merge audit (priority 1)

All nine files that conflicted in merge `72780ac` were re-derived from
the git objects and verified to resolve to the canonical-line parent
(the continuation line).  Per-file provenance is recorded in
[`MERGE_AUDIT_REPORT.md`](MERGE_AUDIT_REPORT.md).  The one genuine
collision — two independent proofs of the eighth component's weighted
`H22` closure — was resolved by keeping the canonical proof as primary
and restoring the former-`main` proof as an explicit alternate rather
than discarding it.

### 2. Alternate proof recovered (priority 2)

The former-`main` `t`-free `14 x 8 -> 10 x 4` elimination proof was
recovered as three `*_ALTERNATE` files with paths rewired and no logic
changed:

- [`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_ALTERNATE.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_ALTERNATE.md)
- `verify_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py`
- `audit_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py`

**Replayed on this machine** (Singular 4.3.2 via WSL, sympy 1.14.0):
the verifier returned `verified: true` with every unit-ideal
certificate (1327 s) and the independent finite-field audit passed at
moduli 11 and 13 (167 s).  The overlap/independence ledger between the
two proofs is in [`MERGE_AUDIT_REPORT.md`](MERGE_AUDIT_REPORT.md).

### 3. Human-facing frontier (priority 3)

[`CURRENT_FRONTIER.md`](CURRENT_FRONTIER.md) was written for a human
mathematician: what is proved exactly; what remains conditional, local,
generic, fibrewise, or boundary-limited; the shortest route to the
conjecture (frontier reduction, O-Cover, O-H31, O-H22); the three most
decisive bottlenecks; and a candid replay audit.

### 4. Machine-readable ledger (priority 4)

[`THEOREM_LEDGER.json`](THEOREM_LEDGER.json) — 85 entries with name,
status, assumptions/excluded divisors, dependencies, primary verifier,
independent audit, expected runtime, external binaries, and
drift-detection SHA-256 prefixes.  Status vocabulary is documented in
the file header.  Global status field: `UNRESOLVED`.

### 5. CI and hygiene checks (priority 5)

- [`check_hygiene.py`](check_hygiene.py): compiles all 1,687 tracked
  Python files, rejects tracked solver artifacts, resolves all local
  markdown links, validates the ledger and all 1,348 script references
  in docs (10 historical dangling references allowlisted with
  provenance), runs five fast verifiers, and prints dependency/solver
  versions.  Runs from a clean checkout with pinned dependencies only.
- [`.github/workflows/hygiene.yml`](.github/workflows/hygiene.yml):
  runs the same checks on push/PR.

### 6. Machine-specific commands removed (priority 6)

The `PYTHONPATH=tmp/python_deps` prefix was removed from 55 command
lines and 19 prose lines across 41 documents; the vendored dependency
cache no longer exists on a clean checkout and the pinned
`requirements.txt` supplies the same dependencies.  The affected Q2
verifiers were re-run and pass.  One residual `sys.path` injection was
guarded to activate only if the directory exists.  The remaining
`wsl.exe` mentions are documented optional `--singular-command`
fallbacks, not required paths.  Reproducible environments are pinned in
[`requirements.lock.txt`](requirements.lock.txt) (sympy 1.14.0,
numpy 2.5.1, python-sat 1.9.dev7, mpmath 1.3.0) and
[`Containerfile`](Containerfile) (Ubuntu 24.04 + Singular + pinned
pip deps).

### 7. Stale branches (priority 7)

After PR #27, the remote tree is exactly `main` plus three active
symbolic branches.  The former `codex/local-to-global-bottleneck` line
is fully merged into `main` and its remote branch was deleted in the
previous session.  **No divergent line remains.**  The three symbolic
branches (`symbolic/m1-extraction-pass`,
`symbolic/sparse-resultant-cores`,
`symbolic/grassmannian-pluecker`) are active attack plans, not stale;
they should be kept and worked, not archived.

## What was verified (replayed this pass)

| Item | Result |
|---|---|
| Alternate weighted-`H22` verifier | `verified: true`, all unit-ideal certs, 1327 s |
| Alternate weighted-`H22` audit | `audited: true`, moduli 11/13, 167 s |
| Ninth-component `H31` extraction | all four frames, ledger byte-for-byte (except timings), 462 s |
| `check_hygiene.py` full suite | all checks passed |
| Five fast verifiers | all exit 0 |
| `test_fourteen_vertex_cycle_cover_lattice.py` | 14 tests OK |

## What could not be replayed

- **Canonical weighted-`H22` verifier/audit** (the primary proof on the
  canonical line): requires its import chain plus hours of Singular;
  not replayed this pass.  Its status as the primary is unchanged.
- **The 717 `verify_*.py` scripts generally**: each theorem doc names
  its own verifier and audit, but a full sweep is manual and was not
  run.
- **All SAT/DRAT certificate replays**: require kissat/glucose/drat-trim
  binaries and the full CNF regeneration chain; not run.
- **Tenth-component extraction**: timeout reproduced deliberately as the
  M5 diagnostic (840 s budget, structurally diagnosed as 14 independent
  multilinear equations).

## What requires human mathematical review

These are not defects in the code; they are places where agent work
cannot substitute for mathematical judgment:

1. **The exhaustiveness claim and its quantifier scope** (bottleneck B3
   in [`CURRENT_FRONTIER.md`](CURRENT_FRONTIER.md)).  The claim that 25
   component closures cover the all-pair-rank exceptional locus needs a
   human to check the quantifiers and the symmetry-group coverage.  The
   obligation ledger's warning — a component census is a lower bound,
   not a cover — stands until that audit is done.
2. **The 14 candidate documents lacking verification docs** (components
   19/20 and embedded-`P_3` boundaries).  Candidates are discovery-run
   reports, not theorems, until independently verified.
3. **Whether the 25-component census and the 13-component ledger compose
   cleanly.**  The ledger predates the census growth; its master-theorem
   schema and obligation structure remain valid, but its per-component
   status tables are superseded where they conflict with the README
   checkpoint.

## Corrections made in response to the PR #28 review (2026-08-06)

Commits `5539615`, `25fb9e3`, `22d843c`, `c298e62`.  No theorem claim
was added or weakened; every change is wording, provenance, or tooling.

### 1. Replay contradiction resolved

`CURRENT_FRONTIER.md` no longer says both proofs were replayed.  The
eighth-component weighted-`H22` paragraph now reads: "Both proofs are
retained.  The alternate proof and audit were replayed during this
stabilization pass; the canonical proof retains its prior status but was
not replayed during this pass."  A repo-wide search found no equivalent
claim elsewhere (`MERGE_AUDIT_REPORT.md`, this report, and the PR
description were already correct).

### 2. Generic nonvanishing language corrected

The alternate package (theorem doc, verifier docstring, and the restored
`RESEARCH_NOTES.md` alternate section) no longer says coefficients
"vanish nowhere on the component" or that factors are "nowhere-vanishing
units".  Every such statement now reads: nonzero in `K(r)`, and therefore
invertible on the declared generic dense open; the zero locus is
contained in the explicitly excluded parameter/slope divisors.  This is a
wording/proof-scope correction; the generic theorem itself is unchanged.
The canonical proof was not touched.

### 3. Ledger contract strengthened

- The ledger is now **explicitly a curated partial index**:
  `coverage_scope` describes what it covers (the load-bearing backbone:
  frontier reduction, master schema, finite certificates, arbitrary-order
  structural theorems, and every on-disk H31/H22 generic component doc),
  and `completeness` is `partial_curated`.  It is not a claim to map all
  ~736 certificate docs.
- `check_hygiene.py` now **recomputes and compares every non-null
  `document_sha256_16`** (85/85 pass).  The hash is over the committed
  git blob (`git show :path`), not working-tree bytes, so it is
  identical on every platform regardless of checkout line endings — the
  first CI failure on this branch was exactly the CRLF/LF artifact this
  removes.
- Every `verified`/`verified_generic`/`verified_finite` entry must carry
  `verifier_provenance` and `audit_provenance` from a controlled
  vocabulary; a null `primary_verifier` or `independent_audit` must be
  explained (`in_document_proof_only`, `historical_certificate_chain`,
  `not_yet_mapped`, or `none_exists`).  "No independent audit exists" is
  therefore distinguished from "audit not yet entered", and the checker
  rejects entries that conflate the two.
- The `component_census` summary is validated against the entries
  (mapped counts and audit counts), and `global_status` is pinned to
  `UNRESOLVED`.
- The frontier's H31 claim is reconciled with the actual mapping: 24
  dedicated H31 docs on disk, all with a `verify_*.py` primary, 23 of 24
  with an independent `audit_*.py`; the equal-support sixfold exception
  is stated explicitly in both the frontier and the ledger.

### 4. Container scope narrowed

The `Containerfile` header now states it provides a **pinned
Python/Singular symbolic baseline only**.  It does not provide msolve,
Kissat, Glucose, drat-trim, or compiler tooling; the "any documented
command runs with zero setup" claim was removed.  It also notes that
Ubuntu 24.04's system `python3` (3.12) is not necessarily the Python
3.13 used by CI and the lockfile-generation machine.

### 5. Portability regression check added

`check_hygiene.py` has a new step that rejects newly introduced
`PYTHONPATH=tmp/python_deps`, `tmp/codex_verify_env`, hardcoded
`/home/` checkout paths, and machine-specific `sys.path` injections.
The pre-existing offenders were fixed in the same pass: 39 vendored-env
replay commands across 22 docs now use the pinned runtime, and four
`find_root()` fallbacks dropped their dead `/home/user` candidate.  The
audit reports that record the removal are allowlisted.

### 6. CI result

The workflow did execute automatically on this PR.  The first run after
the review fixes (run 31059889926) **failed** on the CRLF/LF hash
artifact described above; after switching the ledger hashes to git
blobs, run 31060102504 succeeded, and the current-tip run 31060230290
is the latest **completed with status success**.  All seven local
checks and the CI job agree.

### Ledger completeness statement

The ledger is **curated and partial by design**, not complete: it maps
the backbone claims to their on-disk documents and prover scripts with
enforced hashes and provenance, and says so in its own header.  Adding
entries for the remaining certificate docs is future work and is not
required for the ledger's stated scope.

## Policy reaffirmed

- The global conjecture remains **UNRESOLVED**; this pass did not weaken
  that statement.
- No modular evidence, numerical experiment, timeout, or failed solver
  run was promoted into a proof.
- No new theorem claim was created.  The only claim changes are the
  restoration of the alternate proof (an already-proven statement) and
  documentation of what already exists.
- Independent proofs were preserved where two branches reached the same
  result differently.
