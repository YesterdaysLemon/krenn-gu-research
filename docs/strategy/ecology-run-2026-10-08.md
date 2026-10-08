# Ecology run record — 2026-10-08

Coordinator record for a multi-agent run requested by the repository owner
on 2026-10-08.  It is a research-process document: no theorem, no frontier
entry, no change of mathematical status.  The global Krenn–Gu conjecture
remains **UNRESOLVED**.

## Why this record exists

AGENTS.md ("Resolution-first ecology runs") requires the coordinator to
record, before dispatching workers, the parent implication attacked, its
upstream supply, one named downstream consumer, and what would prove or
refute the route; and to keep one integration owner.  This run has two
research lanes and one ownership lane, each declared below.  The integration
owner is the coordinating session; workers push branches and do not open or
merge pull requests.

## Lane T (trunk): quantitative relations at every order

**Parent proposition.**  There is a family of relations among the values of
the word coefficients of `T_W` and of its sub-configurations `T_{W[A]}`,
valid for every even `n` as a consequence of `T_W = Delta_n`, that refutes
every zero pattern surviving the single-term support conditions (Laplace
accessibility, singleton noncancellation, the GHZ zero pattern, the
column-killer theorem).

**Upstream supply.**  `docs/strategy/trunk-level-attempt-2026-10-08.md`:
the single-term support model is satisfiable at `n = 6` (minimum 27 entries
under the killer theorem) and at `n = 8`; the repository's eight-vertex
row-space refutations (`docs/strategy/source-cancellation-mechanisms-2026-09-13.md`)
are instances of two-term relations.

**Downstream consumer.**  The `P25` boundary row of
`docs/current-frontier.md` ("an all-order route must add a weighted
source-isolation consequence"), and every finite order beyond eight, which
currently close one support at a time.

**Prove / refute.**  Proved: an all-order theorem with a verifier.  Refuted:
an exact pattern at some order that survives every relation of the family;
or a proof that the family is inherently finite.  Workers: an Opus agent on
the all-order statement and an Opus agent on the exact refutation of the
six-vertex survivor patterns (to identify the relation type).

## Lane A (scoped branch sprint): the top-matching lemma of AP'

**Parent proposition.**  No AP' model has all three top-active graphs
`E_c = {e : V - e in S_c}` perfect matchings (WB4, Section 7); first
sub-lemma: in such a model no colour has `G_c = E_c`.

**Upstream supply.**  WB4 (Theorem 3 and Section 8.3's started widow-chain
argument); solver evidence that the sub-lemma's negation is refuted in 0.3 s
at `n = 10`.

**Downstream consumer.**  The all-order AP' conjecture (WB2), hence "every
witness has a bichromatic entry" — a scoped branch consumer, declared as
such per the 2026-09-01 brief.

**Prove / refute.**  A written proof at every even `n >= 6`, an exact
obstruction naming the missing hypothesis, or a model (none is expected
below `n = 12`).  Worker: one Opus agent.

## Lane C (structural, exploratory): Parent C

Whether every column-killer block is a monochromatic matrix unit.  Known
today: not decidable at the support level at `n = 6`.  Worker: one Sonnet
agent, think-only, expected output a mechanism map or an honest stall.

## Ownership lane (not research)

- Same-day adversarial reviews of WB4 (Opus) and of the three-edge-cut
  Proposition E of pull request #359 (Sonnet), writing `docs/audits/`
  records and setting ledger `review` fields.
- Read-only hygiene scan (Haiku): stale guidance, product-name references,
  ledger entries without review, missing verifier paths.
- Node-side checks of the Proof Bonsai tooling (Haiku), report only.

These are explicitly not research objectives under AGENTS.md section 7; they
are maintenance that the owner asked for.

## Rules in force for every worker

Own worktree and branch; no edits to other worktrees; bounded computation
through `tools/research/run_bounded.py`; no process left running; evidence
labels on every statement; `check_hygiene.py` before commit; no pull
requests, no merges, no edits to `docs/current-frontier.md` (the integrator
makes frontier changes after accepting a result).

## Outcome

### Lane T (trunk)

- **Six-vertex survivor patterns refuted exactly** (`claims/finite/n06/SIX_VERTEX_SUPPORT_SURVIVOR_PATTERNS_EXACT_REFUTATION.md`,
  PR #367): no monomial kills; the 27- and 41-entry patterns die by an odd
  cycle of forced `-1` ratios on a `K_{2,3}` ("sign holonomy"), the 63-entry
  pattern by transported holonomy.  Two lemmas proved at every even order.
- **Two-term relation closure theorems A–D** (`claims/arbitrary-order/TWO_TERM_RELATION_CLOSURE_THEOREMS.md`,
  PR #370, review pending): the binomial-linear closure is sound at every
  order, complete on supports whose fibres have at most two live matchings,
  inert on supports whose mixed fibres all have at least three; with the
  killer theorem a **51-entry six-vertex support survives the whole closure**
  and one 27-word slice needs three-term relations with degree-two monomial
  multipliers.  Named next statement: the degree-bounded closure conjecture
  `TM_D`.
- **Holonomy-strengthened support model** (branch
  `claude/holonomy-support-model-20261008`): adding the sign-holonomy and
  rank-one-grid rules as valid clauses leaves six vertices **SAT** (51-entry
  survivor whose permanent-type words have Groebner basis `[1]`, so the next
  relation is multilinear, not two-term).

**Lane T outcome.**  No all-order theorem; an exact obstruction twice over:
two-term relations, even closed under lattice and linear combination and
even with the killer theorem, do not exclude six vertices.  The trunk
mechanism must produce multilinear (three-term, degree-bounded) consequences
at every order.  Proof-distance delta: a proposed mechanism eliminated by an
exact countermodel, with one sharper statement (`TM_D`).

### Lane A (AP' sub-lemma)

`claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_TOP_MATCHING_EXTRA_EDGE_LEMMA.md`
(PR #369, merged): the sub-lemma is not proved.  Proved at every order: the
reduction to a two-colour condition, Hamiltonicity of widow-first chains, the
equivalence of the uniform case with the imported CGI theorem, and a
**locality obstruction** (uniform models on girth-ten cubic graphs at
`n = 160, 162` and every even `n >= 12640` satisfy every axiom behind the fast
`n <= 10` refutations).  Next lemma: the arc lemma, which would close
`n = 2 (mod 4)`.  Frontier: one refuted-route row.

### Lane C (Parent C)

`docs/strategy/parent-c-attempt-2026-10-08.md` (PR #366, merged): not proved,
not refuted; local lemmas (a mixed killer forces degree at least four; a
degree-four classification with two residual local models; reciprocity with
row anchors), a well-posedness correction (the `C`-span form), and the
reason torus degeneration cannot settle it.

### Ownership lane

- Reviews written and ledger `review` fields set: WB4 (gap found, see
  below), Proposition E (PASS), ST20 (PASS), the three eight-vertex
  documents (PASS).
- README status refreshed; five strategy notes marked historical; the RZP10
  document's dangling output path fixed (PR #364).
- Node-side checks all pass; `npm ci` reports 27 dependency advisories in
  `tools/proof-visualizer`, left for the owner.

### The review that mattered

The WB4 review found the lex-leader symmetry block of the primary AP' search
script unsound (helper variables keyed by reused `id()` values).  Every
`n >= 10` result of that script was withdrawn in a correction (PR #371): the
`n = 10` exclusion of AP' now rests on the audit encoding's checked
certificate alone, AP'+(F') at `n = 10` has no valid certificate outside
RZP10, and the "minimum 27 entries" claim of the trunk record is withdrawn
(23-entry models exist).  Both encoders are fixed; corrected certified reruns
were launched.  This is the run's most important outcome for process: an
adversarial same-day review caught a certificate that two solvers and a
proof checker had all accepted, because the formula they checked was not
the formula claimed.

### Global status

Unchanged: **UNRESOLVED**.  No countermodel was found anywhere; every
finished exact search was UNSAT or SAT exactly as the honest labels say.
