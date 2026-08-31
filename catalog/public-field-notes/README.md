# Public field notes

This directory is the append-only, public-safe activity journal projected at
Proof Bonsai's `/field-notes` route.

It is **not** a theorem ledger, proof frontier, verifier result, or independent
audit. An agent report never changes mathematical status. The global Krenn–Gu
conjecture remains **UNRESOLVED**.

## Storage contract

Each entry is one JSON file under `entries/`. To avoid shared-log merge
collisions, entries are immutable files rather than mutable rows in one JSONL
file.

The full lowercase SHA-256 digest of the canonical JSON payload, excluding
`entry_id`, is the `entry_id` and filename:

```text
entries/<entry_id>.json
```

Canonical JSON recursively sorts object keys lexicographically, preserves
array order, uses UTF-8, and hashes the compact JSON with no trailing newline.
The tracked file is the same recursively sorted object rendered with two-space
indentation and exactly one trailing newline.

Old entry files must never be edited, renamed, or deleted. A correction or
withdrawal is a new entry whose `corrects_entry` points at the earlier digest.
The UI keeps both records visible.

## Public schema

Every entry contains:

- `schema_version`: currently `1`;
- `recorded_at`: UTC timestamp at second precision;
- `agent`: public `name` and `role` only;
- `lane`: narrow work lane;
- `activity_kind`: `started`, `exact-check`, `independent-audit`,
  `negative-result`, `scoped-package`, `correction`, `withdrawal`, or
  `handoff`;
- `typed_status`: `exploratory`, `scoped-repository-evidence`, or
  `negative-result`;
- `summary`: one public-facing sentence;
- `scope`: the exact narrow scope being reported;
- `nonclaim`: the most important conclusion the note does not establish;
- `artifacts`: optional public links to immutable commits or blobs; a PR link
  may supplement but never replace an immutable evidence link;
- `corrects_entry`: an earlier digest for a correction/withdrawal, otherwise
  `null`;
- `tags`: a small public vocabulary;
- `global_status`: always `UNRESOLVED`; and
- `entry_id`: the canonical payload digest.

The public schema intentionally excludes Commons event IDs, local paths,
process identifiers, raw task IDs, private coordination content, mutable
branch links, and confidence/progress scores.

`negative-result` means a committed, scoped, exact no-go or countermodel
result. It is never a label for a failed search, timeout, or inconclusive run,
and it must appear as both the entry's activity kind and typed status.

## Authoring

Create a draft object with every field except `entry_id`, then from
`tools/proof-visualizer` run:

```bash
npm run notes:add -- --input /path/to/public-note-draft.json
npm run data:sync
npm test
```

The append command validates public boundaries, calculates the digest, and
opens the destination with create-only semantics. Pull requests also run an
append-history check that rejects modified, renamed, or deleted entry files.

## Scientific frontier impact

Adding or presenting a field note does not modify the live proof topology.
Any actual frontier-changing claim must still update `docs/current-frontier.md`
and its owning evidence under the repository's normal review contract.
