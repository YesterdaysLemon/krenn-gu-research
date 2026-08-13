# Literature provenance protocol

This protocol records what external literature was found, how its identity was
checked, what was actually inspected, and how the repository uses it. It does
not assign mathematical status. Claim status, assumptions, dependencies, and
proof obligations remain owned by the relevant claim package and the evidence
semantics contract.

The canonical machine-readable source registry is
`catalog/literature/sources.json`. Its deterministic validator and identifier
inventory are `tools/literature/source_registry.py`.

## Identity and usage-scoped inspection

Bibliographic identity is source-level. A non-null `identity_verification`
means that title, authors, year when available, and persistent identity were
checked against its recorded authoritative publisher, repository, DOI, or
author page. A null value marks an unverified lead. Search-result snippets are
leads only and never establish identity.

Inspection is recorded separately for each repository use:

- `metadata_only`: only authoritative bibliographic metadata was inspected for
  this use;
- `abstract_inspected`: the abstract was inspected for this use, but no
  relevant theorem, section, or passage was consulted;
- `relevant_passage_inspected`: the theorem, section, or passage relevant to
  this use was actually consulted. An exact `source_locator` is mandatory.

These levels describe scoped access, not source prestige, truth, or a reading
of the entire paper. Never promote inspection based on memory, a snippet, or a
secondary paraphrase, and never imply that one inspected passage means the full
source was read.

## Usage roles and evidence

- `background`: verify bibliographic identity and record only the inspection
  performed for this use.
- `novelty_assessment`: record the searches and material actually inspected,
  together with limits on completeness.
- `imported_result`: record the exact source locator, assumptions and scope,
  and how the result corresponds to its repository use. If the relevant
  passage or locator is unavailable, keep the import obligation unresolved.

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
- `search_trail`: required for an unverified lead and useful for novelty work;
- `relevance` and `limitations`;
- `repository_usages`: index-visible tracked repository file, usage role,
  usage-scoped `inspection_level`, `source_locator`, and conditional
  correspondence fields.

Each `imported_result` usage additionally carries `assumptions_scope`,
`correspondence_note`, and `unresolved_obligations`.
Unknown values stay null or become explicit obligations; they are not guessed.
Every `relevant_passage_inspected` usage must have an exact nonempty
`source_locator`. That assertion remains scoped to the located passage and does
not assert that the whole source was read.
One source may have multiple persistent identifiers, but no identifier or
citekey may identify two records.

## Bounded workflow

1. Inventory existing identifiers before adding a record.
2. Reuse an existing record when its identity matches.
3. Verify identity only when needed, and inspect only to the level required by
   each intended use.
4. Record identity verification at source level and inspection evidence on
   each repository use, together with limitations.
5. Run `python tools/literature/source_registry.py validate`.
6. If the source changes a premise, novelty assessment, or imported proof
   dependency, update the owning scientific artifact through its normal review
   process; never let the registry silently change scientific meaning.

The pilot intentionally has no network metadata framework, citation-manager
integration, PDF archive, general source-quality score, or bibliography
renderer. Add such machinery only when repeated repository work demonstrates a
need.
