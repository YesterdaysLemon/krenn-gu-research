# Phase R3 exact root-end-state enforcement

Status: **ACTIVE — EXACT-HEAD AND MERGED-MAIN CI PASSED**

This is a layout-policy tranche, not a scientific-result tranche.  It changes
no theorem, scope, lifecycle, proof obligation, certificate meaning, evidence
role, audit-independence claim, or theorem-ledger status.  The global Krenn–Gu
conjecture remains **UNRESOLVED**.

## Activation base

Stage 33 merged through PR #69 as
`4263832e3ff338c5bd87528268cb8cb563866ec0`.  Both the PR exact-head hygiene
run and the push workflow for that exact merge passed before this tranche was
started.  Fresh read-only semantic and mechanical audits then independently
reconstructed the merged root:

```text
files:       .gitignore, AGENTS.md, Containerfile, README.md,
             check_hygiene.py, requirements.lock.txt, requirements.txt
directories: .github, catalog, claims, docs, research_figures,
             research_snapshots, src, tests, tools
root:        7 files + 9 directories = 16 entries
debt:        0 grandfathered + 0 new
```

The frozen 2,363-path inventory and its hash remain unchanged.  The manifest
remains `2,357 moved + 0 proposed-high + 1 review-required`.  The one review row
is the old filename-classifier proposal for `check_hygiene.py`; its live root
ownership is explicitly justified, so the row is historical provenance rather
than debt or move authority.  The manifest's moved-only projection remains 15
because `AGENTS.md` was added after the frozen inventory.

## Enforcement change

The ordinary `python check_hygiene.py` command now enforces the end state
without an environment opt-in:

- the exact allowlist is frozen to the seven files and nine directories above;
- four absent legacy pre-authorizations (`CITATION.cff`, `CONTRIBUTING.md`,
  `LICENSE`, and `pyproject.toml`) are removed;
- the hard root-entry and allowlist-capacity limit is 16;
- every nonallowlisted root path is an unconditional hygiene failure; and
- research-artifact filename diagnostics inspect only nonallowlisted files, so
  the justified `check_hygiene.py` entrypoint cannot reject itself.

Future root metadata requires a fresh reviewed policy change.  It cannot be
enabled by an environment variable or by reinterpreting classifier confidence.
The historical debt-universe ratchet remains intact as an additional
provenance guard.

## Validation and release gates

The index-complete candidate must pass:

```text
python -B check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v tests.test_h31_cbmf_reconciliation
python -m unittest -v tests.test_fourteen_vertex_cycle_cover_lattice
python tools/migration/rewrite_links.py
git diff --exit-code
```

The focused migration tests pin the exact allowlist and capacity, zero live
debt, acceptance of the justified hygiene entrypoint, and unconditional
failure even when a caller sets the retired `KG_LAYOUT_STRICT=0` variable.
No SAT, Singular, brute-force, sampling, or broad scientific replay is required
or authorized for this enforcement-only tranche.

On the index-complete candidate, strict hygiene passed with 1,718 compiled
Python files, 875 resolving Markdown files, 86/86 ledger hashes, 2,357 moved
provenance rows, and root debt `0/0`.  The 190 migration tests, seven bounded
H31 reconciliation tests, fourteen lattice tests, and five Stage-33
inverse-taper guards passed.  The shared rewriter returned an exact zero-change
fixed point and `git diff --exit-code` confirmed no unstaged repair.

Fresh semantic and mechanical referees accepted exact clean candidate
`cf0746ad3cf80e68fa6204ce29aa87e8a02c3f2d` with no findings.  The semantic
review confirmed that ledger completeness remains `partial_curated`, global
status remains `UNRESOLVED`, and the only ledger changes are the three necessary
README hash refreshes.  The mechanical review independently replayed the full
bounded floor and adversarially confirmed default strictness, environment
non-bypass, allowlist-capacity failure, and the allowed entrypoint exception.

PR #70's hosted hygiene run passed at exact reviewed head
`bf7af12118debca9d2af2b90bc94e8b11168c9e7`.  The reviewed chain then merged
to `main` as `e99457df478b0842a833204a2f064ab00355a838`, and the push workflow for
that exact merge passed every job.  Phase R3 is therefore active on merged
`main`.
