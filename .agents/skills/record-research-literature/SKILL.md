---
name: record-research-literature
description: Record and verify external research literature used in the Krenn-Gu repository. Use when asked to look up related work, decide whether a theorem is already known, record a paper, add a source to the bibliography or literature registry, determine what a paper actually proves, cite a claim using external literature, assess novelty, or import an external theorem. Do not use for internal cross-references, unrelated symbolic or computational mathematics, or merely because an already-registered citation is mentioned incidentally.
---

# Record Research Literature

Follow the canonical policy in `docs/literature/provenance.md`. Keep scientific
status in the owning claim package; the source registry records provenance, not
whether a repository claim is proved.

## Route the request

1. For an exploratory search, record candidates as `lead_unverified` with the
   search trail. Treat snippets as leads only.
2. For a background citation, verify bibliographic identity from an
   authoritative page before upgrading the record.
3. For novelty or related-work assessment, record what was searched or
   inspected and its limits.
4. For an imported theorem, require its exact locator, assumptions, scope, and
   correspondence to the repository use. If the necessary text is unavailable,
   leave an unresolved obligation rather than reconstructing it from memory.
5. For an incidental citation already in `catalog/literature/sources.json`, do
   only the lookup needed by the task. Do not load the full workflow.

## Work fail closed

- Never invent a title, author, year, identifier, theorem locator, or scope.
- Never infer full-text inspection from metadata, an abstract, a snippet, or a
  remembered reading.
- Preserve conflicts and unavailable metadata as explicit limitations.
- Do not download or archive PDFs unless the user separately authorizes it.
- Stop and escalate any apparent mathematical or provenance conflict without
  changing the claim or frontier.

## Use repository tooling

Run the smallest relevant command:

```bash
rg -n "<citekey-or-identifier>" catalog/literature/sources.json
python tools/literature/source_registry.py inventory
python tools/literature/source_registry.py validate --json
```

Use `inventory --json` only when a caller needs the complete machine-readable
location set; its output is intentionally comprehensive.

Edit the canonical registry only when the task calls for a durable source
record. Validate it after editing. Do not duplicate the schema or inspection
vocabulary here; those are owned by `docs/literature/provenance.md` and enforced
by the validator.
