# Review: all-bridge degree-five cut reduction and full-support degree-eight boundary

## Verdict

**PASS as an exact theorem at the stated all-bridge scope.**  The package
proves the unconditional support boundary and an exhaustive degree-five
localization

```text
Delta(G)>=8 and n>=10;
under Delta(D)=5:
  a supported pure cancellation on an inactive-selected-edge complement,
  or one side of a selected-matching-component/complement cut,
  or one side of a Hamiltonian-chord-arc/complement cut.
```

The universal zero-layer and abstract least-cancellation owners already imply
the primitive-cycle/branching-core dichotomy for every all-bridge witness.
The reviewed theorem imports that topology and does not relabel it as a new
degree-five result.  Degree five further makes the least core bipartite
subcubic: an even cycle, a closed all-odd rank-two theta, or rank at least
three with at least four cubic sites.  The reduction neither excludes
saturated degree five nor realizes any localized form as a witness.  The deeper-
blocker branch, universal extraction/gluing, and the global Krenn--Gu
conjecture remain open.  Global status is **UNRESOLVED**.

## Claim reconstruction

The reviewed argument has five load-bearing steps.

1. Active-deck score one and cross-colour exclusivity give three pairwise
   edge-disjoint spanning active graphs.  Under `Delta(D)<=5`, every active
   graph is subcubic and the complete local active/inactive table is finite.
2. If some active graph has no perfect matching, every nonzero full matching
   contains an inactive edge whose complementary principal hafnian is a
   supported zero.  A minimal Hall-deficient shore sharpens this to two
   vertex-disjoint inactive repairs whose global pair-deletion cofactors vanish
   in all three colours.
3. If all active graphs have perfect matchings, choose one `P_c` in each.
   They are physically disjoint, and a degree-five vertex leaves a residual
   edge.  A disconnected `P_c union P_d` gives component/complement factors;
   if every pair is Hamiltonian, a residual saturated chord gives arc/
   complement factors.  The mixed cut forces one supported factor to vanish.
4. Independently of the degree-five reduction, the universal zero-layer
   theorem already makes the family of proper supported pure cancellations
   nonempty.  Global minimization—not minimization only among the cuts in step
   3—allows the existing abstract least-cancellation theorem to apply.  Its
   cycle/branching dichotomy is inherited universal topology; the global
   least core need not inherit the labels of the cut in step 3.  Support
   subtraction makes the core bipartite subcubic at degree five, and exact
   handshaking yields the cycle/theta/higher-rank trichotomy.
5. Three distinct off-diagonal primary killers lie outside the diagonal
   backbone at every vertex, so `deg_G(v)>=deg_D(v)+3` unconditionally.
   Combining this with the existing `Delta(D)>=5` theorem yields
   `Delta(G)>=8` and, by simplicity and even order, `n>=10`.  Thus maximum
   full-support degree at most seven is excluded.

## Adversarial checks

| attack | result |
|---|---|
| An active edge belongs to a nonzero matching, so `E_c` must have a perfect matching | Rejected.  Complement edges of that matching may be cofactor-inactive by cancellation.  The exact signed double-star has hafnian one, score one at every vertex, balanced bipartite active graph, and no active perfect matching. |
| Balanced active shores imply Hall's condition | Rejected.  Score sums prove equal shore cardinalities, but signed scores need not satisfy a nonnegative fractional-matching argument. |
| Active branching remains a separate exit | Rejected. A branching active graph may contain a perfect matching, as the exact `K_(3,3)` score-`1/3` control shows. If it does not, the inactive selected-edge complement is already a supported cancellation. |
| The Hall-deficient argument finds only one arbitrary inactive edge | Rejected. A minimal deficient shore has boundary score `-1`; every complementary matching to a boundary edge contains `b=q+2>=2` vertex-disjoint inactive repairs, each with all three global cofactors zero. |
| The local degree table misses an overlap | Rejected.  Exact enumeration gives 6, 60, and 390 labelled incident assignments at degrees three, four, and five.  At degree five the four shapes are `(1,1,1;2)`, `(2,1,1;1)`, `(3,1,1;0)`, and `(2,2,1;0)`. |
| The nonbranching residual remains a partial matching | Rejected sharply.  At every degree-five nonbranching vertex it has degree two, with labels `HH`, `HQ_c`, or `Q_cQ_d`. |
| Maximum residual degree two still gives principal noncancellation | Rejected by an exact six-vertex control: the full hafnian is one while a supported four-vertex principal hafnian is `1-1=0`. |
| The residual chord might already be a selected edge | Rejected.  The chosen residual `R_P=D-(P_0 union P_1 union P_2)` is physically disjoint from every selected matching.  The chord may be an unselected active edge, which does not affect the support-colour or arc argument. |
| Hamiltonian arc orientation is ambiguous | Rejected.  The common third bit makes both arcs odd; exactly one starts and ends with `P_d` edges.  Length one or `n-1` would identify the chord with `P_d` or `P_c`. |
| Minimal-core theorem applied with only cut-relative minimality | Corrected before acceptance.  The final proof minimizes globally over all pure colours and all proper even supported cancellations; the focused implementations exercise a cross-colour global selector. |
| The imported matrix-unit theorem is branch-specific algebra | Rejected.  Its cited core theorem is stated and proved for an arbitrary hollow symmetric scalar matrix over characteristic different from two; the matrix-unit text begins only in the application section. |
| The least-core dichotomy is a new consequence of degree five | Rejected during the final novelty audit.  The universal zero-layer theorem already supplies a proper supported pure cancellation in every all-bridge witness.  New here are the three active-deck localizations and the degree-five bipartite-subcubic rank refinement. |
| Local type/active facts already force the mixed cut | Rejected.  The exact eight-vertex control passes normalization, bit flips, exclusivity, local degree five, and pairwise Hamiltonicity, but a displayed ordered mixed cut has product one. |
| The older maximum-degree-five theorem closes this case | Rejected.  That theorem bounds the full essential support skeleton; the local reduction bounds saturated `D`.  Conversely, the new unconditional inequality plus `Delta(D)>=5` now strengthens the live full-support exclusion through degree seven. |
| A bounded replay is being called an arbitrary-order enumeration | Rejected.  Both scripts are explicitly scoped to displayed finite interfaces and controls; the written argument carries the arbitrary-order quantifiers. |
| The globally least core inherits the component/chord labels | Rejected.  A smaller cancellation elsewhere may be globally selected.  Localized cuts and the global core remain separate interfaces. |
| Global or branch status is inflated | Rejected.  All three localized forms, all three refined least-core strata, `Delta(D)>=6`, and the deeper-blocker branch remain open as exclusions; the global conjecture remains `UNRESOLVED`. |

## Evidence replay

Run from repository root:

```powershell
python -B claims/arbitrary-order/verify_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
python -B claims/arbitrary-order/audit_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
python -m ruff check claims/arbitrary-order/verify_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py claims/arbitrary-order/audit_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
python -m py_compile claims/arbitrary-order/verify_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py claims/arbitrary-order/audit_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
```

The primary uses cached perfect-matching enumeration and direct graph
algorithms.  The no-import audit uses a separate bitmask hafnian recurrence,
independently labelled graph routines, and a relabelled/reversed chord audit.
Both reconstruct all displayed controls with exact rational arithmetic.  They share no
imports.

Acceptance requires both scripts to print `PASS` and
`global conjecture status: UNRESOLVED`, Ruff and byte compilation to pass, and
the candidate-tree hygiene floor to remain green after navigation and ledger
integration.

## Publication boundary

The accepted live consequences are exactly:

```text
all-bridge maximum full-support degree <=7: EXCLUDED;
all-bridge even orders n=6,8: EXCLUDED;
all-bridge Delta(D)=5 can be reduced to:
  inactive-selected-edge complement cancellation,
  selected-matching-component/complement cancellation,
  or Hamiltonian-chord-arc/complement cancellation (PROVED EXHAUSTIVE).

globally least pure-cancellation core under Delta(D)=5:
  even cycle, closed all-odd rank-two theta, or rank>=3 bipartite
  subcubic core with at least four cubic sites (PROVED REFINEMENT).
```

The smallest next proof obligations are:

1. use the simultaneous identities to exclude the Hall-deficient form through
   its two inactive common-cofactor-zero repairs;
2. prove simultaneous control for both factors of the selected-matching-
   component/complement and Hamiltonian-chord-arc/complement cuts; or
3. exclude one of the global cycle, theta, or higher-rank least-core strata.
