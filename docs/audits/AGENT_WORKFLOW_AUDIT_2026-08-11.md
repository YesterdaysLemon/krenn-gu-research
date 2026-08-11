# Agent workflow audit — 2026-08-11

## Scope and method

This audit is workflow evidence, not mathematical evidence. The Krenn–Gu
conjecture remains **UNRESOLVED**.

The audit began from then-current `origin/main` at
`87e8de02de1c6abd9b6a1cdc3238b679e38aaa1a`. Before edits, the visible checkout
was clean but 26 commits behind that ref; roughly 30 registered worktrees were
treated as protected, and no repository-bound research process was touched.
Implementation used a new isolated worktree and branch. When `origin/main`
advanced during forward testing and review, the isolated candidate was rebased
through current `1361a2e5c675b601a5e3db8271c7b87b2ca5c088` and focused checks
were rerun after each refresh.

The evidence corpus comprised:

- the complete current `AGENTS.md`, its eight modifying commits since
  `db8427b`, and the current contracts, runbooks, tools, tests, workflow, Git,
  PR, worktree, and process state;
- 15 repository-scoped parent agent sessions from 2026-07-23 through
  2026-08-11: 441 turns, 80 direct user prompts, and about 453.5 MiB of raw
  JSONL. All used GPT-5.6 Sol in the Codex Desktop/work-desktop harness at
  xhigh, ultra, or max effort;
- the two dedicated literature documents and literature/provenance sections in
  live claim packages. That focused corpus had 313 arXiv line-mentions with
  113 unique identifiers and 22 DOI line-mentions with 12 unique normalized
  identifiers after same-line deduplication;
- current first-parent and PR history, including the 18 frontier-changing PRs
  after the live-frontier rule was added.

No unrelated conversations or repositories were inspected. The private scoped
histories were inspected and summarized locally rather than copied into the
repository. Parent histories dominate the sample, one
144-turn session dominates the counts, all runs share a model family and
harness, and repository policy changed during the window. These are behavior
observations, not a model comparison or causal experiment.

## Evidence matrix

| Behavior or friction | Representative evidence | Frequency and cost | Tasks | Existing coverage / apparent effect | Likely cause; confidence and confounders | Narrow intervention | Context / maintenance cost | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Scientific status and scope were protected and independently corrected | All 14 substantive sampled sessions kept `UNRESOLVED`; audits corrected an arbitrary-order statement narrowed to three colors, caught a certificate inconsistency, withdrew a generic obstruction after widened sampling, and stopped on a 14-versus-16 stratum conflict. The committed Stage 11.5 report records two consequential metadata/status contradictions. | Repeated; very high scientific cost if missed | Research, verification, migration | AGENTS sections 2–6 and 12 plus typed catalog tests directly cover the failures; protection was consistently visible | Strong alignment, but policy and review practice are confounded; high confidence that the invariant is needed | Keep concise always-on invariants and canonical contracts | Existing context cost is material but justified; maintenance low when semantics stay canonical in docs/catalog | **RETAIN** |
| Live-frontier maintenance became consistent | After `eca32327` added the rule, all 18 subsequent first-parent frontier-changing PRs (#84–#101) also changed `docs/current-frontier.md` | 18/18 observed; high navigation/status cost if missed | Claim/frontier changes | Current rule appears effective | Same owner and workflow confound causality; medium confidence | No change | No new cost | **RETAIN** |
| Stale checkouts and live workers required deliberate isolation | Three sampled sessions found live untracked theorem work, a worker 157 commits ahead of the visible checkout, or a shared checkout six commits stale; each protected it and used refs/worktrees/processes plus an isolated tree. This audit found the visible checkout 26 commits stale and about 30 worktrees. | Repeated material risk; no overwrite observed | All implementation and research | Current-Git language helped, but active-worker and fresh-base routing was implicit | Recurrent repository topology; high confidence despite selection toward complex tasks | Add two sentences requiring worker inspection, current `origin/main`, and isolation | Tiny context; low maintenance | **ADD** |
| Explicit wind-down was once followed by new research lanes | In one session the user had to repeat “call it” and “wrap things up” after persistent-goal continuations reopened research twice; later sessions honored stops | One severe incident, later improvement | Long autonomous research | No explicit AGENTS rule distinguished persistent-goal continuation from a task-local terminal stop | Harness continuation plus ambiguous stopping scope; medium confidence from one costly case | Add one narrow sentence; do not generalize into a lifecycle framework | Tiny context; low maintenance | **CLARIFY** |
| Literature work repeatedly reconstructed searches and attribution | The longest sampled session made 238 search calls across 871 query strings, including 42 repeated query instances, plus 305 open/click/find calls. A later attribution correction traced an external construction only after owner clarification. Existing literature has highly repeated identifiers and no structured usage-scoped inspection evidence. | Repeated and expensive; provenance was fragile, though no fabricated bibliography was found | Related work, novelty, theorem import, citation | AGENTS had no routing layer. Agents did sometimes inspect full text and reject abstract-level slogans when hypotheses mattered | Episodic workflow plus no canonical source record; high confidence, with counts dominated by one long session | One trigger-focused skill; canonical protocol and registry; offline inventory/validator | Small dormant skill; moderate one-file registry maintenance | **MOVE_TO_SKILL**, **MOVE_TO_REFERENCE**, **AUTOMATE**, and one AGENTS pointer |
| Search snippets or unavailable text could be overstated | No clear fabricated source was found. Successful runs distinguished snippets/abstracts from exact hypotheses, but existing records usually do not say what was inspected | Potentially high scientific cost; observed gap rather than observed hallucination | Search, novelty, theorem import | Prompt-local caution worked inconsistently and was not durable | Missing inspection vocabulary; medium confidence | Source-level identity verification, usage-scoped inspection levels, and risk-based imported-result obligations; fail closed | Small policy cost; low deterministic-test cost | **ADD** narrowly; **NO_ACTION** on a general source-quality system |
| Index-complete validation prevented a known false green | Stage 8 passed a local floor that omitted untracked files, then failed CI; regression tests now enforce index completeness. Commit `f69e42d` repaired a stale validation path copied across AGENTS, workflow, and runbook | One consequential failure plus replicated-command drift | Repository infrastructure | The staged-candidate invariant is demonstrably effective. `check_hygiene.py` incorrectly called itself a one-command CI mirror while CI also ran focused modules | Candidate-tree omission and duplicated prose; high confidence | Retain staging invariant; clarify checker/CI ownership; run the new focused registry tests in CI | Tiny context; one focused test module to maintain | **RETAIN**, **CLARIFY** |
| Completed layout-migration procedure occupies always-on context | AGENTS layout section is 59 lines / about 321 words; the evidence contract says Phase R2 is complete and the runbook owns procedure/history | Persistent context cost; no current operational failure | Any agent task | Exact batch/root/proof-boundary protections arose from real migration failures and remain valuable | Useful invariants mixed with episodic detail; medium confidence | Keep scientific/approval invariants; move procedure to the existing runbook when next edited | Potential context saving, but semantic-edit risk now | **SHORTEN / MOVE_TO_REFERENCE**; no broad rewrite in this pilot |
| Broad computation sometimes displaced requested symbolic strategy | Two sessions pivoted into a long quotient-algebra grind or a 4,598,126-case enumeration; one large run reached 5.2% available RAM before a task-local floor was imposed | At least two strategy mismatches and one resource incident | Mathematical research | Task prompts corrected course; no universal balance is scientifically appropriate | Task-specific model/tool choice; medium confidence | Use prompt-local strategy and resource limits | Zero persistent context | **NO_ACTION** |
| False CI-pass claims, recurrent unasked edits, or active-worker overwrites | Sampled runs reported absent/skipped checks honestly; no recurrent unasked edit or overwrite was found | No demonstrated recurrence | Publication, review | Existing guardrails and user scope appear adequate | Absence is not proof; corpus is finite | Do not add defensive ceremony without evidence | Zero | **NO_ACTION** |

## Allocation and implemented minimum

Durable facts have one primary owner:

- `AGENTS.md` owns only always-on invariants: scientific/status protections,
  active-worker isolation, task-local stops, and a one-sentence literature
  route.
- `.agents/skills/record-research-literature/SKILL.md` owns trigger routing and
  orchestration for related work, novelty checks, paper recording, citations,
  and theorem imports. Its negative route keeps incidental citations and
  unrelated symbolic work dormant.
- `docs/literature/provenance.md` owns human-readable inspection semantics,
  usage-risk requirements, schema meaning, and fail-closed policy.
- `catalog/literature/sources.json` owns portable source records. It does not
  duplicate theorem status.
- `tools/literature/source_registry.py` owns mechanical identifier inventory,
  normalization, duplicate/conflict checks, required-field validation, and
  exit codes. It performs no network requests.
- `tests/test_literature_registry.py` owns deterministic malformed, incomplete,
  duplicate, conflicting, missing-path, imported-result, and offline-lead
  regressions.
- Prompt-only instructions remain the home for one-time strategy, resource,
  exception, and stopping preferences not covered by a safety invariant.

The reviewed root policy adds `.agents` as the tenth allowed directory and
raises the exact limit from 16 to 17. Its justification is narrowly
“committed repository-scoped agent workflow configuration”; research
documents, ordinary tools, results, and history remain outside that owner.

No migration skill, network metadata framework, citation-manager integration,
PDF archive, source-quality score, bibliography renderer, database, README,
installation guide, or general agent framework was added.

## Literature pilot

The bounded registry contains ten identity-verified sources already used by
the repository. Inspection evidence is scoped to its eleven repository uses:
two at `abstract_inspected`, nine at `metadata_only`, and none at
`relevant_passage_inspected`. No record implies that an entire paper was read.
Authoritative arXiv, DOI/Crossref, DMTCS, EuDML, and Stacks pages established
bibliographic identity; no PDF was downloaded.

Three `imported_result` uses remain deliberately unresolved:

- arXiv `2407.00303`, Theorem 1.7: inspect the full statement and match every
  hypothesis; identify the original Bogdanov source or retain the secondary
  limitation;
- Dalwadi–Pause–Diwan–Kothari, Theorem 1.2: inspect exact assumptions and
  terminology, and resolve the Hetyei attribution if needed;
- Cook, arXiv `1111.4979`: identify the exact imported result and verify its
  characteristic, degree, and algebra hypotheses.

These are provenance obligations only. The audit did not investigate or alter
the mathematical claims that cite them.

## Forward tests

Two fresh read-only contexts received raw requests and repository artifacts,
without an expected diagnosis. One routed five realistic scenarios; the other
routed six natural trigger variants and six close negatives. Neither edited the
repository or accessed an external source.

| Request class | Fresh-context result | Context / deviation | Outcome |
|---|---|---|---|
| Exploratory sparse-graph related work | Skill activated; existing record was checked before new leads; snippets remained `lead_unverified` pending authoritative verification | Loaded the skill, protocol, registry, tool, and relevant existing literature/claim locations | Pass |
| Import Theorem 1.2 as a proof step | Skill activated; the agent noticed the record was only `identity_verified` and refused to state usable hypotheses without exact theorem text and correspondence | Loaded the owning claim and proof/evidence contracts; no quantifier strengthening | Pass |
| Incidental Cook citation during a coefficient derivation | Skill stayed dormant; at most a targeted existing-record lookup was proposed | No protocol or external source loaded | Pass |
| Symbolic Sylvester resultant with literature excluded | Skill stayed dormant | Only the displayed algebra and owning claim, if any, were proposed | Pass |
| Conflicting DOI and publisher authors | Skill activated and refused a verified/citation-ready identity; disagreement remained an explicit unverified limitation | The first pass exposed that `authors` could not be unknown. The validator was revised once to allow an empty authors array only for `lead_unverified`; verified records still require authors | Pass after one focused revision |
| Natural trigger phrasings | Related work, already-known theorem, record paper, add source, and determine what a paper proved activated. “Cite this claim” activated in external-paper context and stayed dormant for internal repository cross-references | Revised metadata routes on external-literature context without embedding the procedure | Pass after one precision revision |
| Four clearly unrelated close negatives | Local verifier rename with an incidental citation, no-literature symbolic proof, generic repository text search, and filename-only arXiv use all stayed dormant | No unnecessary literature context | Pass |
| Two registry-maintenance boundaries | Listing background records and punctuation-only maintenance activated only the small local lookup/validation path | The registry was the direct task object; no source search or full protocol replay was proposed | Pass; intentional limited activation |

No forward test produced a fabricated source, promoted a snippet, implied full
text from metadata, or loaded the literature workflow for unrelated symbolic
mathematics. The scenario pass also caught the two-commit `origin/main` advance;
the isolated candidate was refreshed and revalidated without touching the
advancing worker.

## Adversarial review

Fresh raw-diff review found and the implementation resolved:

- malformed HTTPS values passing a prefix-only URL check; authoritative URLs
  now require a valid host/port and reject malformed IPv6, whitespace, or
  embedded credentials;
- a usage path being accepted by filesystem existence rather than the candidate
  index; usages now require a regular-file mode from `git ls-files --stage`, so
  untracked files, directories, and symlink entries fail closed;
- loose date parsing that accepted compact or future dates; verification dates
  now require an exact, non-future `YYYY-MM-DD` string;
- an unqualified “cite a claim” trigger and a comprehensive JSON inventory in
  the small-lookup route; metadata now distinguishes external literature from
  internal cross-references, and targeted `rg` is the default lookup;
- two separate `origin/main` advances during review; both were handled by
  rebasing the isolated worktree and rerunning focused checks.

The same review found no concrete defect in root-policy exactness, canonical
ownership, scientific-status preservation, CI wiring, or bounded scope. A
final post-fix review supplied the malformed-host/port and Git-symlink edge
cases above; both were fixed and covered before validation.

## Validation

The complete staged candidate at base `1361a2e5c675b601a5e3db8271c7b87b2ca5c088`
passed:

- skill-creator `quick_validate.py` for `record-research-literature`;
- registry validation with 10 sources and offline inventory reporting 317
  arXiv line-mentions / 115 unique across all `claims` and `docs`, and 22 DOI
  line-mentions / 12 unique;
- 17 focused literature-registry tests, including malformed, incomplete,
  duplicate, conflicting, offline, unavailable-author, bad-URL, future-date,
  untracked-path, directory, and Git-symlink cases;
- `python check_hygiene.py`: index complete, 1,785 Python files compiled, 935
  Markdown files linked, 117 ledger hashes valid, root exactly 7 files plus 10
  directories, and all five fast verifiers passing;
- 191 migration-tool tests, 7 H31 reconciliation tests, and 14 cycle-cover
  lattice tests;
- the migration rewriter fixed point, `git diff --exit-code`, and
  `git diff --check --cached`.

No check was skipped or described as passing when unavailable.

## Scientific and publication boundary

No theorem, reduction, obstruction, experiment, candidate, withdrawn result,
dependency, quantifier, assumption, field, genericity condition, or global
status was changed. `docs/current-frontier.md` requires no update because this
is non-mathematical workflow infrastructure. No PR is to be opened or merged.
