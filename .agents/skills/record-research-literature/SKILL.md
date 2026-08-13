---
name: record-research-literature
description: Verify and record external literature relevant to the Krenn-Gu project. Use for related-work or novelty searches, checking whether a result is known, determining what a paper proves, verifying an attribution or theorem hypothesis, or adding a durable source record. Do not use for internal repository references, unrelated mathematics, citation formatting alone, or incidental mentions requiring no literature work.
---

# Record Research Literature

Keep scientific status in the owning claim package; the source registry records
provenance, not whether a repository claim is proved.

Read the canonical protocol in `docs/literature/provenance.md` for a new source
record, literature search, novelty assessment, imported result, or use that
materially supports a claim. For a direct existing-record lookup or mechanical
validation, skip the protocol and run only the smallest targeted registry
command needed.

## Route the request

1. For an exploratory search, record candidates as unverified leads with null
   `identity_verification` and the search trail. Treat snippets as leads only.
2. For a background citation, verify bibliographic identity from an
   authoritative page before upgrading the record.
3. For novelty or related-work assessment, record what was searched or
   inspected and its limits.
4. For an imported theorem, require its exact locator, assumptions, scope, and
   correspondence to the repository use. If the necessary text is unavailable,
   leave an unresolved obligation rather than reconstructing it from memory.
5. For a direct lookup of an existing record, do only the lookup needed by the
   task. Do not load the full workflow.

## Work fail closed

- Never invent a title, author, year, identifier, theorem locator, or scope.
- Never infer `relevant_passage_inspected` from metadata, an abstract, a
  snippet, or a remembered reading, and never imply that an entire paper was
  read because one passage was inspected.
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
