# Layout migration report — Stage 14 (dependency portability and stale-path enforcement)

Status: **the bounded Stage 14 correctness repair is complete locally and
ready for two fresh Tier-2 merge-gate reviews.**  The stage repairs four
hidden moved-script command paths across three root H22 audits, restores
foreign-working-directory execution for one migrated P4 analyzer, and teaches
hygiene to reject the `Path(...).name` command pattern that hid those failures.

> **Scientific status did not change.**  No theorem text, coefficient domain,
> elimination, witness, evidence role, lifecycle field, or ledger status was
> changed.  All repaired H22 audits still report their generic obstruction,
> leave special/projective boundary fibres open, and report the global
> Krenn–Gu conjecture unresolved.

## Provenance anchors

- Exact merged baseline: `1129a2e35b3a9bfebe7599f190e7210d623b7c02`.
- Branch: `codex/stage14-common-active-portability`.
- Runtime repair commit: `f6d94228549f5223013abdd9526073670d408c6f`.
- Enforcement and regression commit:
  `97d401c99028304c8addf54da94ad6bc5834c6c2`.
- The Stage 13 mandatory program audit first identified the common-active
  stale path and analyzer bootstrap-order defect in
  [`layout-migration-stage13-report.md`](layout-migration-stage13-report.md).

This is a correctness/enforcement stage, not a migration batch.  It creates no
batch, changes no manifest status, and moves no file.

## Reproduced failures

### Retired-path command indirection

The affected audits use a shared `run_json()` shape whose subprocess working
directory is repository root.  Four dependency constants name executed moves,
but the command passed only `SCRIPT.name`, discarding the correct destination
directory:

| audit | dependency discarded by `.name` |
|---|---|
| common-active binary triangle | moved P4 common-active verifier |
| coincident-support rank-one star | moved P4 verifier and moved H31 verifier |
| common-kernel vertical triangle | moved H31 verifier |

All four root basenames are absent, all four manifest destinations exist, and
each bare command failed before the dependent mathematics could run.  The
common-active constant was additionally still assigned to its retired root
location, so its audit failed even earlier at the required-input check.

The common-kernel P4 dependency remains a root file and `review_required`; it
is not an enforceable retired path and was not reclassified or moved.

### Analyzer import before bootstrap

The migrated common-active P4 analyzer imported the root coefficient provider
before running shared bootstrap.  Its owning P4 verifier happened to mask the
defect by bootstrapping first, but direct execution from a foreign working
directory failed with `ModuleNotFoundError`.

## Runtime repair

The three H22 audits now pass repository-relative POSIX paths obtained from
`SCRIPT.relative_to(ROOT).as_posix()`.  The common-active P4 constant now names
its actual moved package.  Root-owned dependencies continue to resolve to the
same basename through the same expression.

The P4 analyzer now performs shared bootstrap before importing the root
coefficient provider.  No new package exposure is needed: `bootstrap()`
already exposes repository root and `src`, while the owning P4 verifier keeps
its existing exposure of the hyphenated analyzer package.

These are path/import-order changes only.  Candidate certificates, reports,
historical hashes, and mathematical bodies were not rewritten.

## Enforcement repair

The previous stale-reference grammar detected literal Python command strings
only when a quoted retired basename occurred near `subprocess`, `python`, or
`sys.executable`.  It could not connect:

```python
SCRIPT = ROOT / "claims/.../moved_verifier.py"
run_json(("python", SCRIPT.name), timeout=180)
```

The new bounded AST check:

1. parses only Python files already selected by the existing retired-basename
   prefilter;
2. records simple assigned variables whose static path literals end in an
   executed-move basename;
3. inspects list/tuple argv expressions supplied directly to calls;
4. requires a Python launcher (`python`, `python3`, or `sys.executable`) and
   the assigned variable's `.name`; and
5. preserves the existing destination-package and provenance exemptions.

Original Python text is used for this check, because masking a correct current
destination would otherwise hide the destructive `.name` operation.  Syntax
errors remain the compile phase's responsibility.

Six focused regressions cover a retired bare assignment, a correct full
destination still truncated by `.name`, `sys.executable`, a correct
repository-relative command, metadata-only `.name`, and the existing
in-package exemption.  The real repository has zero remaining violations.

## Semantic replay

The common-active analyzer was executed by absolute path from a foreign
working directory.  It preserved tangent rank `5`, minor `-1/6`, incidence
rank `12`, fifteen primitive denominator-six equations, and generated-source
SHA-256
`346598947e89b7d088b016bbe559942e56d8791fe3879b388d6bb38b922f594d`.

Its owning P4 primary and independent audit passed with the same standard
basis data `(18, 0, 9)`; the primary kept
`global_conjecture_resolved: false`.

All three repaired H22 audits were then replayed at exact committed head
`97d401c99028304c8addf54da94ad6bc5834c6c2`:

| audit | wall time | semantic result |
|---|---:|---|
| common-active binary triangle | 28.589 s | pass; generic H22 empty; special/projective fibres false; global false |
| coincident-support rank-one star | 19.085 s | pass; generic H22 empty; special/projective boundary fibres false; global false |
| common-kernel vertical triangle | 52.872 s | pass; generic H22 empty; special/projective boundary fibres false; global false |

Each output embedded the exact `97d401c` Git commit.  Replays changed no
tracked output.

## Validation floor

The index-complete substantive tree passes:

- Ruff for the four runtime files;
- Ruff for the modified hygiene/tests with only their unchanged baseline
  `F841`/`E741` findings excluded;
- `py_compile` for all six changed Python files;
- all 24 focused stale-reference tests;
- `check_hygiene.py` on the real repository in 20.020 seconds;
- all 149 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests; and
- migration-rewriter fixed point with a clean working tree.

On the final report candidate, hygiene must additionally confirm 1,698 Python
files, 801 Markdown files with resolving local links, 86/86 ledger hashes,
353 retired paths with exact batch provenance, zero new root debt, and
unchanged manifest arithmetic `353 / 249 / 1,413`.

## Debt and stop condition

Root debt remains 2,004 files.  This zero-reduction stage closes a named
program-audit blocker affecting the common-active candidate family and makes
the stale-path ratchet materially stronger; it does not use allowed-directory
dumping or baseline/allowlist changes.

Stage 14 stops before any claim migration, shared-helper extraction,
scientific wording repair, or batch-approval policy change.  The repository
owner's standing mapping delegation requires a separate narrow durable policy
clarification before the next batch is frozen.  After that clarification, the
next independently identified migration candidate is the complete 15-file H31
embedded-P3 closure, subject to its own exact topology audit and review.
