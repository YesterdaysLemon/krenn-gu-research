# Proof Bonsai

Interactive proof-topology viewer for the Krenn–Gu research programme.

The site is a projection of committed repository evidence, not a new source of
mathematical status. It reads:

- `docs/current-frontier.md` for the canonical node key and typed-edge table;
- `catalog/theorem-ledger.json` for separate verifier/audit metadata.

The `/field-notes` addendum is deliberately separate from that evidence view.
It projects immutable, public-safe activity notes from
`catalog/public-field-notes/entries/`. A field note says what an agent worked
on and what it does **not** establish; it never updates the frontier or theorem
ledger by implication.

`npm run data:sync` writes a deterministic snapshot to
`app/data/frontier.generated.json` and `app/data/field-notes.generated.json`.
Development and production builds run this sync automatically.

## Append a public field note

Prepare a JSON draft that follows
[`catalog/public-field-notes/README.md`](../../catalog/public-field-notes/README.md),
then run:

```bash
npm run notes:add -- --input /path/to/public-note-draft.json
npm run data:sync
```

The command creates one content-addressed file and refuses to overwrite an
existing entry. Corrections and withdrawals are new entries linked through
`corrects_entry`; editing or deleting old entries violates the public-log
contract.

## Display projection

The three bonsai states intentionally remain simple:

- **leaf / green**: established at the node's stated scope;
- **bud / yellow**: the node description contains an open, partial,
  conditional, or unresolved boundary;
- **scar / red**: a route or stronger argument is refuted, withdrawn, or
  superseded.

The exact repository status is always shown beside the projection. Green never
means that the global conjecture is solved, and ledger evidence never silently
strengthens a node's mathematical status.

The map opens on the selected node's one-edge neighborhood so labels and
branches remain readable. Search jumps directly to a node, selections are
shareable through `#node=...` links, and **Whole map** provides the global
overview without making it the first navigation surface. On narrow screens,
selecting a node brings its inspector into view and the inspector provides a
return path to the map.

The parser also reports topology maintenance findings instead of inventing
relationships when the Mermaid block, node key, and typed-edge table differ.

## Commands

```bash
npm install
npm run dev
npm run data:check
npm test
```

Node.js 22.13 or newer is required.
