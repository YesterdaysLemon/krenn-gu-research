# Crossing run, 2026-10-09: coordinator record

The global Krenn–Gu status is **UNRESOLVED** and nothing in this run changes
it.  This is the coordinator's record of the 2026-10-09 run (eleven merged
PRs, #381–#391), written at wind-down so that the next session can start
from committed evidence.  Every claim below is owned by the note, theorem
document, verifier, audit or frontier row it names; this file owns nothing.

## 1. What was attacked

The run followed the plane-rigidity / hyperdeterminant lane into the
eight-vertex support-level question and then into the gluing gap `GL`.
The unit of work was one question at a time, each dispatched to a single
research worker with an explicit scope, exact-arithmetic requirement and
escalation rule; the coordinator integrated results as separate PRs.

## 2. Results, in order

| PR | Result | Status / evidence | Owner |
|---|---|---|---|
| #381 | Six-vertex exclusion at the support level from column killers, signed holonomy and plane rigidity (`SL6`); the permanent restricted to three planes vanishes iff the Plücker vectors are coaxial; Cayley's hyperdeterminant lies in the degree-3 ideal and is not the invariant | proved (theorem, reviewed); finite exclusion with native CaDiCaL DRAT checked by the pinned `drat-trim`; also UNSAT with no symmetry block (#386, 4.3 h, no DRAT) | `claims/arbitrary-order/PERMANENT_PLANE_RESTRICTION_HYPERDETERMINANT_THEOREM.md`, `hyperdeterminant-crossing-2026-10-09.md` |
| #382 | The 128-entry eight-vertex survivor is not fibre-realizable (four-word `H3` identity); the 156-entry one survives every encoded family | exact identity with verifier; S156 modular/sampling evidence only | `n8-support-realizability-2026-10-09.md` |
| #383 | Multi-partner grid transport (hub flattening and the adjugate identity) for every hub degree; its clause families are silent on S156 | proved for every `k`; verifier replays `k <= 6`; exact reason for the silence | `multi-partner-grid-transport-2026-10-09.md` |
| #384 | S156 and S128 excluded fibre-exactly by the diagonal-anchor lemma of `docs/research-notes.md`, which the support model had never encoded; `--anchors` added | exact 16-word identities with verifier | `s156-hub-trichotomy-2026-10-09.md` |
| #385 | The 121-entry survivor of killers + anchors + plane rigidity excluded by top-level `H3`; its run had omitted holonomy | exact four-word identity with verifier | `s121-exclusion-2026-10-09.md` |
| #386 | `SL6` is UNSAT fully symmetry-free; the 6 h full-rule `n = 8` run was inconclusive (38 rounds, 11.06 million lazy instances) | SAT-RUN records | crossing note, Section 3a |
| #387 | `--fast` numpy prefilters for the plane-rigidity and holonomy checks; same trajectory, byte-identical `n = 6` certificate; about 2x on early `n = 8` rounds, late rounds solver-bound | engineering, equivalence by exact comparison | model script, `tests/test_general_block_support_model_fast.py` |
| #388 | Induction `n -> n+2` by restriction is circular inside the model; the inherited families exclude nothing; the non-hereditary ingredient is the top-level GHZ zeros on word types 4+2, 3+3, 3+2+1, 2+2+2 with the subset's killers; pair-expansion identity | exact propositions; SAT runs | `support-model-induction-2026-10-09.md` |
| #389 | Compressed-Hessian clause family: sound, encodable, not hereditary at the support level (the rank condition is invisible to zero patterns); **Lemma 5**: contracting an order-8 witness at a pair whose block is not a single entry gives an ancilla-assisted GHZ(6,3) | exact lemma; SAT runs | `compressed-hessian-family-2026-10-09.md` |
| #390 | `C_{6,1}` (six three-colour vertices plus two non-adjacent one-colour vertices realizing GHZ(6,3)): literature checked at passage level; the single-entry residual is exactly `N8R1`'s class, already excluded; the ancilla-edge variant is nonempty (PyTheus Fig. 3, replayed exactly) | candidate node `C61`, not live; literature registered | `ancilla-c61-2026-10-09.md` |
| #391 | Independent audit of Lemma 5: PASS with corrections; the dichotomy is the `M1` split at `n = 8`, so `C_{6,1}` empty would close the `n = 8` child of `M2` | audit with a separate exact implementation | `docs/audits/LEMMA5_CONTRACTION_AUDIT_2026-10-09.md` |

## 3. What the run established, stated carefully

- **No new order is excluded.**  Six vertices was already excluded; the run
  gave it a second, support-level proof whose only computation is a
  zero-pattern search with a checked certificate.
- **Three eight-vertex support survivors are dead, each by an already-proved
  rule** that the generating run had not switched on.  None of them exposed
  a gap in the rule set.  The informative object is a model of the full rule
  set, which the 24-hour runs are computing (Section 5).
- **The support-level programme has a ceiling at S156-type patterns** (every
  two-vertex-deleted full-block subgraph with two or more perfect matchings
  certifies no minor), and **restriction-induction inside the model is
  circular**.  Both are exact statements with named obstructions.
- **The one candidate reduction is `C61`:** if ancilla-assisted GHZ(6,3)
  without an ancilla edge is impossible, the `n = 8` child of `M2` closes
  (Lemma 5, audited, plus `N8R1`).  `C_{6,1}` is open; the literature
  neither constructs nor excludes it; numerics do not converge on it and are
  not evidence.
- Nothing was escalated: no apparent exact witness of any kind appeared.

## 4. What went wrong, and the fixes recorded

- Three survivors were produced by runs with incomplete rule sets, costing a
  worker each (though each produced an exact verifier).  Rule: before
  searching for a new lemma, list the already-proved all-order mechanisms
  the model does not encode.
- Integration mechanics failed four times before the first merge of the day
  (a doubled link prefix, a commit gate that matched failure lines, the
  reserved ledger `dependencies` field, a stale Proof Bonsai data file).
  All four are recorded in the integrator's working notes; none touched
  mathematics.
- The lazy CEGAR loop is the wrong shape for `n = 8` once it is
  solver-bound; `--fast` removed the Python cost but late rounds remain
  SAT-solver time.

## 5. Live handoff at wind-down

- Three bounded 24-hour runs of the `n = 8` support model from the worktree
  of the anchor worker (`tmp/n8/n8full24`, `n8top24`, `n8htop24`; full rule
  set; holonomy and plane rigidity top-level only; holonomy top-level with
  all-level plane rigidity; each with `--proof`) were at rounds 28–30 after
  3.5 h and were left running under `tools/research/run_bounded.py`.
  Outcome handling: UNSAT means a support-level eight-vertex exclusion
  candidate (native DRAT of the final formula, review, frontier node);
  SAT means the full mechanism battery on the model; inconclusive means the
  solver side is the next lever.
- One research worker (exact attack on `C_{6,1}` / `Phi0`, branch
  `claude/c61-attack-20261009`) was still running; its result is to be
  integrated as a PR when it lands, with no further lanes opened.

## 6. Next question

Decide `C_{6,1}`, or prove `Phi0` (in any realization of GHZ(6,3) by six
three-colour and two one-colour vertices, with the ancilla edge allowed, one
constant word has zero ancilla contribution).  Success closes the `n = 8`
child of `M2`; an exact `C_{6,1}` witness would refute the route and must be
escalated.
