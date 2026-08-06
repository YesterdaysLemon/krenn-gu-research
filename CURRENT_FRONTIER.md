# Current frontier of the Krenn–Gu conjecture effort

Audience: a human mathematician assessing what this repository
actually proves.  Stabilization pass, 2026-08-05.  Nothing in this
document is a new claim; every statement cites the document that owns
it.  The machine-readable companion is
[`THEOREM_LEDGER.json`](catalog/theorem-ledger.json).

**The global conjecture is UNRESOLVED.**  For even `n >= 6`,
`d >= 3`, and complex `d x d` blocks `W_ij`, the matching-sum tensor

```text
T_W(a_1,...,a_n) = sum_M prod_{ij in M} W_ij[a_i,a_j]
```

has no proof or counterexample showing it cannot equal
`sum_c e_c tensor ... tensor e_c`.  Reduction to any three colours
makes `d = 3` the essential case.

---

## 1. What is proved exactly

### 1.1 Complete finite cases (computer-assisted, independently replayed)

- **`n = 6`, all `d >= 3`: no complex solution.**  Map:
  [`SIX_VERTEX_CERTIFICATE.md`](SIX_VERTEX_CERTIFICATE.md).  Method:
  exhaustive support reduction, exact Laurent/algebraic conflict
  extraction, byte-checked selector-CNF compilation, independent SAT
  decision, DRAT replay, SHA-256 hash-chain audit.
- **Eight-vertex boundaries** (all finite, all SAT/CEGAR with replayed
  DRAT proofs): no 4-regular witness; no degree-four-vertex witness
  through 17 edges; exact-18/19-edge degree-three results; the
  84-entry and 7,938-labelled-support macro-families.  Maps:
  `EIGHT_VERTEX_*_CERTIFICATE.md` family in the README index.
- **Ten-vertex**: no 105-entry witness on a 5-regular exact-25-edge
  skeleton; the `C10`/`C4+C6`/odd-factor equality families.  Maps:
  `TEN_VERTEX_*` certificates.
- **Order-14 equality factor families, partial but exact**:
  `C3+C3+C8`, `C3+C4+C7`, `C3+C5+C6`, `C4+C5+C5`, `C3+C3+C4+C4`,
  `C14` closed; `C4+C10`, `C6+C8`, `C4+C4+C6` closed orbit-by-orbit
  (365/425, 292/328, 67/93 selectors excluded) — each exclusion is a
  certified finite null result, **not** a family theorem.  Maps:
  `FOURTEEN_VERTEX_*` certificates,
  [`FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md`](FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md).

### 1.2 Arbitrary-order structural theorems

Proved over `C` for every even order (symbolic, with independent
finite-field or modular audits where stated):

- no 4-regular witness in the simultaneous three-colour balanced
  all-bridge boundary; no witness of maximum support degree at most
  five there; no pairwise-disjoint exact-degree-six Kotzig/reciprocal
  port boundary witness —
  `FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md`,
  `ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`;
- the root–blocker lower bounds: at least `r` outside blockers for
  `r >= 2` zero-coupled roots; four blockers impossible (ideal
  obstruction, 544-case `F_5` audit); the exact-three-blocker
  permanent-rank lemma; order-four permanent subrank exactly two
  (`FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md`, 24,336-pair
  `F_5` audit);
- the `P_5` contraction obstructions: support-three contractions have
  exact subrank two (6,561 kernel types, 104,976-case `F_5` audit);
  the support-four positive restriction showing that extension is
  false (`SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md`).

### 1.3 The `P_5 -> Delta_3` component programme (the core)

Every hypothetical restriction `P_5 -> Delta_3` reduces — by a verified
chain of exact reductions — to a local map of one of two normalized
families, **H31** or **H22**
([`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`](P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md)).
The attack then runs through the pure-`P_4` compression components:

- **Census**: twenty-five certified pure-`P_4` component orbits
  (fivefolds and sixfolds), each with an exact family-tangent /
  incidence certificate.  The all-pair-rank-exceptional-graph
  reduction claims these twenty-five closures are exhaustive
  ([`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md))
  — see bottleneck 3 for the honest status of that claim.
- **Generic marked `H31` fibre**: proved empty on **all 25**
  components.  Twenty-four dedicated
  `P5_H31_*_GENERIC_OBSTRUCTION.md` documents carry the function-field
  theorems on disk; each has a `verify_*.py` primary verifier.  Of
  those, 23 also have an independent `audit_*.py` modular audit.  The
  single exception is the equal-support sixfold, whose claim rests on
  its self-contained primary verifier together with the P4 component
  audit `audit_p4_equal_support_sixfold_pure_component.py` (recorded in
  [`THEOREM_LEDGER.json`](catalog/theorem-ledger.json) as an explicit
  `none_exists`, not an unmapped gap).  The twenty-fifth component's
  `H31` closure is carried by the README checkpoint narrative.
- **Generic weighted `H22` fibre**: proved empty on components
  1–21, 23, 24.  Component 22 has its `D01` pencil closed and its
  `D23` pencil under divisor-by-divisor closure (several divisors
  still open; README lines 1176–1227 track them).
- **Partial boundary closures**: equal/opposite-weight slopes,
  parameter-pivot branches, coupled slope divisors, `r = 0` endpoints,
  elliptic-end divisors — see
  [`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`](P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md).
- **Two independent proofs** of the eighth component's weighted-`H22`
  closure exist and are both retained: the canonical determinantal
  marking-chart proof and the recovered `t`-free `14 x 8 -> 10 x 4`
  elimination proof
  ([`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_ALTERNATE.md`](claims/p5/h22/disjoint-mixed-star/alternate/P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_ALTERNATE.md)).
  Both proofs are retained.  The alternate proof and audit were replayed
  during this stabilization pass; the canonical proof retains its prior
  status but was not replayed during this pass.  See
  [`MERGE_AUDIT_REPORT.md`](MERGE_AUDIT_REPORT.md).

### 1.4 Transfer-track inputs (bounded, no theorem promotion)

Root-of-unity block permanent selector, symmetric hafnian lift,
six-blocker quotient catalogue, and the `P_6`/`P_7` symbolic
reductions (`ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md` and the
`ARBITRARY_PERMANENT_*` family).  These are exact bounded inputs to
construction/gluing strategies; none changes the global status.

---

## 2. What remains conditional, local, generic, or boundary-limited

| Limitation | Where it lives |
|---|---|
| **Generic, not pointwise**: every component closure is over the component function field.  Points where a certificate denominator vanishes (parameter divisors, slope divisors) are excluded, not proved.  The pointwise upgrade requires the extraction pass (below). | [`P5_POINTWISE_SPECIALIZATION_META_THEOREM.md`](P5_POINTWISE_SPECIALIZATION_META_THEOREM.md); extraction scripts in `research_snapshots/2026-08-04-p5-delta3-obligation-ledger/scripts/` |
| **Boundary-limited**: projective/chart boundaries of the component parametrizations are mostly untouched (24 boundary programmes named in the ledger). | [`P5_DELTA3_OBLIGATION_LEDGER.md`](P5_DELTA3_OBLIGATION_LEDGER.md) II.5/III.2 |
| **Component 22's `D23` pencil** is not fully closed generically. | README lines 1176–1227; `P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_*` docs |
| **Components 19/20 and embedded-`P_3` boundaries**: 23 `*_CANDIDATE.md` documents exist; 9 have matching `*_VERIFICATION.md` docs, 14 do not.  Candidates are discovery-run reports, not theorems, until independently verified. | `P5_H22_COMPONENT19_*`, `COMPONENT20_INTRINSIC_*`, `P5_H22_EMBEDDED_P3_*` |
| **Order-14 results are finite orbit theorems**, not family theorems; 60/36/26 orbits remain SAT in `C4+C10`/`C6+C8`/`C4+C4+C6`. | `FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md` |
| **Stale ledger**: the 2026-08-04 obligation ledger was written against the 13-component census; the canonical line has since certified 25.  Its master-theorem schema and obligation structure remain valid; its per-component status tables are superseded where they conflict with the README checkpoint. | [`P5_DELTA3_OBLIGATION_LEDGER.md`](P5_DELTA3_OBLIGATION_LEDGER.md) header |

---

## 3. Shortest logical route to the conjecture

The ledger states the route as one theorem schema
([`P5_DELTA3_OBLIGATION_LEDGER.md`](P5_DELTA3_OBLIGATION_LEDGER.md) I.4):

1. **(Frontier reduction ⋆)** — any restriction forces an H31 or H22
   local family.  *Done* (verified reductions;
   `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`).
2. **(O-Cover)** — an explicit finite closed cover
   `X_nz ⊆ C_1 ∪ ... ∪ C_N` up to symmetry.  *Claimed for the
   all-pair-rank-exceptional locus with 25 components; needs the
   quantifier audit of bottleneck 3.*
3. **(O-H31)** — every marked `H31` fibre empty at **every** point of
   every `C_k` (interior, divisors, boundaries).  *Generic part done
   for all 25; divisor/boundary part open.*
4. **(O-H22)** — every weighted `H22` pencil fibre empty at every
   point, all slopes in `C^*`.  *Generic part done for 24 of 25;
   divisor/boundary part open.*

Then no H31/H22 family exists, hence no restriction, hence (with the
colour-reduction) the conjecture.  Every step is exact characteristic-zero
mathematics; no probabilistic or numerical ingredient enters the proof
schema — finite-field audits are corroboration only, and the repository
policy is that timeouts, modular evidence, and failed solver runs are
never promoted into proofs.

---

## 4. The three most decisive remaining bottlenecks

**B1 — The divisor/boundary recursion (the bulk of the tree).**
Each generic theorem hides finitely many inverted denominators.  The
meta-theorem's extraction pass converts them into explicit curves
([`P5_POINTWISE_SPECIALIZATION_META_THEOREM.md`](P5_POINTWISE_SPECIALIZATION_META_THEOREM.md));
the ninth component extracts in seconds to minutes (replayed in this
pass), the tenth times out (840 s budget, structurally diagnosed: 14
independent multilinear equations; see
`research_snapshots/2026-08-04-p5-delta3-obligation-ledger/scripts/M1_EXTRACTION_PASS_ATTACK_PLAN.md`).
Every extracted divisor is a one-dimension-down instance of the same
problem.  The ledger counted ~35 named open divisors and 24 untouched
boundary programmes at the 13-component stage; the count scales with
the census.  This is where the work volume lives.

**B2 — Component 22's `D23` pencil.**  The only certified component
whose generic weighted `H22` closure is incomplete.  A large
divisor-by-divisor programme is mid-flight (`rho=0`, `rho=-1`, `h0=0`
slices closed; parts of the `H=0` and `f2=0` covers remain).  Until
this closes, (O-H22) has a 24-of-25 hole at generic points.

**B3 — The O-Cover quantifier gap.**  The exhaustiveness statement is
the master theorem's load-bearing hypothesis.  The canonical line
claims the 25 closures are exhaustive *within the all-pair-rank
exceptional-graph reduction*
([`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md));
the ledger's warning still stands: a component census is a lower bound,
and the cover must be verified as `X_nz ⊆ union` up to the symmetry
group, including every support-degenerate and lower-rank tail.  This is
the step most in need of human mathematical review, because its
quantifiers are easy to over-claim and it alone converts per-component
work into a theorem.

---

## 5. Candid audit (stabilization pass, 2026-08-05)

The complete pass record — what was done, replayed, could not be
replayed, and needs human review — is
[`STABILIZATION_AUDIT_REPORT.md`](STABILIZATION_AUDIT_REPORT.md).  The
per-file merge resolution record is
[`MERGE_AUDIT_REPORT.md`](MERGE_AUDIT_REPORT.md).

**Replayed and passed on this machine** (Singular 4.3.2 under WSL;
sympy 1.14):

- alternate weighted-`H22` verifier: `verified: true`, all unit-ideal
  certificates, 1327 s;
- alternate weighted-`H22` audit: `audited: true`, moduli 11/13,
  167 s;
- ninth-component `H31` extraction: all four frames extracted, ledger
  reproduced byte-for-byte except per-run timings, 462 s.

**Not replayed in this pass** (documented, not hidden):

- the canonical weighted-`H22` verifier/audit (import chain + hours of
  Singular); its status as the primary proof is unchanged by this pass;
- the 717 `verify_*.py` scripts generally — each theorem doc names its
  own verifier and audit, but a full sweep is manual;
- all SAT/DRAT certificate replays (require kissat/glucose/drat-trim
  binaries and the full CNF regeneration chain);
- the tenth-component extraction (timeout reproduced deliberately as
  the M5 diagnostic).

**Requires human mathematical review** (agents cannot adjudicate):

- the exhaustiveness claim and its quantifier scope (B3);
- the 14 candidate documents lacking verification docs;
- whether the 25-component census and the 13-component ledger's
  obligation structure compose cleanly (the ledger predates the census
  growth).

Nothing in this pass weakened the UNRESOLVED status, promoted modular
evidence to proof, or created a new theorem claim.
