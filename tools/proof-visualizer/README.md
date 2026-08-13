# Proof Bonsai

Interactive proof-topology viewer for the Krenn–Gu research programme.

The site is a projection of committed repository evidence, not a new source of
mathematical status. It reads:

- `docs/current-frontier.md` for the canonical node key and typed-edge table;
- `catalog/theorem-ledger.json` for separate verifier/audit metadata.

`npm run data:sync` writes a deterministic snapshot to
`app/data/frontier.generated.json`. Development and production builds run this
sync automatically.

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
