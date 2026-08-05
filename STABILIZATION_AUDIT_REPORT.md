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

[`THEOREM_LEDGER.json`](THEOREM_LEDGER.json) — 72 entries with name,
status, assumptions/excluded divisors, dependencies, primary verifier,
independent audit, expected runtime, external binaries, and
drift-detection SHA-256 prefixes.  Status vocabulary is documented in
the file header.  Global status field: `UNRESOLVED`.

### 5. CI and hygiene checks (priority 5)

- [`check_hygiene.py`](check_hygiene.py): compiles all 1,686 tracked
  Python files, rejects tracked solver artifacts, resolves all local
  markdown links, validates the ledger and all 1,346 script references
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
