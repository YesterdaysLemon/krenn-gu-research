# Literature provenance protocol

This protocol records what external literature was found, how its identity was
checked, what was actually inspected, and how the repository uses it. It does
not assign mathematical status. Claim status, assumptions, dependencies, and
proof obligations remain owned by the relevant claim package and the evidence
semantics contract.

The canonical machine-readable source registry is
`catalog/literature/sources.json`. Its deterministic validator and identifier
inventory are `tools/literature/source_registry.py`.

## Inspection levels

- `lead_unverified`: a search or citation trail worth retaining, but its
  bibliographic identity has not been verified. Search-result snippets never
  exceed this level.
- `identity_verified`: title, authors, year when available, and persistent
  identity were checked against an authoritative publisher, repository, DOI,
  or author page.
- `metadata_or_abstract_inspected`: authoritative metadata or an abstract was
  inspected, but not the full source.
- `full_text_inspected`: the relevant full text was actually inspected. Record
  the exact theorem, proposition, section, or page locator when the use depends
  on a result.

These levels describe access and inspection, not source prestige or truth.
Never promote a record based on memory, a snippet, or a secondary paraphrase.

## Usage roles and evidence

- `background`: verify bibliographic identity.
- `novelty_assessment`: record the searches and material actually inspected,
  together with limits on completeness.
- `imported_result`: record the exact source locator, assumptions and scope,
  and how the result corresponds to its repository use. If full text or a
  locator is unavailable, keep the import obligation unresolved.

An exploratory lead may remain unverified when it has a reproducible search
trail and an explicit limitation. Conflicting metadata must remain a recorded
conflict until an authoritative identity is established. Network or metadata
failure never licenses filling fields from memory.

## Source record

The registry has `schema_version` 1 and a `sources` array. Each source owns:

- `citekey`: stable, lowercase repository key;
- `title`, `authors`, and `year`; authors may be an empty array only for an
  unverified lead, and an unknown year is null, both with explicit limitations;
- `identifiers`: one or more of `doi`, `arxiv`, `eudml`, or `stacks_tag` when
  available;
- `authoritative_url`;
- `identity_verification`: authoritative HTTPS `source_url` and non-future ISO
  `YYYY-MM-DD` date, or `null` for an unverified lead;
- `inspection_level`;
- `search_trail`: required for an unverified lead and useful for novelty work;
- `relevance` and `limitations`;
- `repository_usages`: index-visible tracked repository file, usage role, and
  conditional locator/correspondence fields.

Each `imported_result` usage additionally carries `source_locator`,
`assumptions_scope`, `correspondence_note`, and `unresolved_obligations`.
Unknown values stay null or become explicit obligations; they are not guessed.
One source may have multiple persistent identifiers, but no identifier or
citekey may identify two records.

## Bounded workflow

1. Inventory existing identifiers before adding a record.
2. Reuse an existing record when its identity matches.
3. Verify only to the level required by the intended use.
4. Record the inspection level, verification date, limitations, and usages.
5. Run `python tools/literature/source_registry.py validate`.
6. If the source changes a premise, novelty assessment, or imported proof
   dependency, update the owning scientific artifact through its normal review
   process; never let the registry silently change scientific meaning.

The pilot intentionally has no network metadata framework, citation-manager
integration, PDF archive, general source-quality score, or bibliography
renderer. Add such machinery only when repeated repository work demonstrates a
need.
