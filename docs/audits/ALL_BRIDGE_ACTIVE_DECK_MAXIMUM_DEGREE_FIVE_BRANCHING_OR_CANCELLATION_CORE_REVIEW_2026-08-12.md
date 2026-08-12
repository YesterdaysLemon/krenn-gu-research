# Review: all-bridge active-deck maximum-degree-five reduction

## Verdict

**PASS as an exact structural reduction at the stated all-bridge scope.**
Under the inherited simultaneous balanced all-bridge identities and
`Delta(D)<=5`, the package proves the exhaustive exit set

```text
active degree-three branching;
or a least proper supported pure cancellation whose active core is one cycle;
or a least proper supported pure cancellation whose active core branches.
```

The reduction neither excludes saturated degree five nor realizes any exit
as a witness.  The deeper-blocker branch, universal extraction/gluing, and
the global Krenn--Gu conjecture remain open.  Global status is
**UNRESOLVED**.

## Claim reconstruction

The reviewed argument has five load-bearing steps.

1. Active-deck score one and cross-colour exclusivity give three pairwise
   edge-disjoint spanning active graphs.  Under `Delta(D)<=5`, every active
   graph is subcubic and the complete local active/inactive table is finite.
2. A degree-three active vertex is the first exit.  If no such vertex exists,
   endpoint score propagation and bit-flip bipartiteness make every active
   component `K_2` or an even cycle, so each colour supplies a perfect
   matching `P_c` and a partial remainder `Q_c`.
3. The physical residual has maximum degree two.  If a pair `P_c union P_d`
   is disconnected, one component and its complement give two supported
   mixed-cut factors.  If all pairs are Hamiltonian, any residual saturated
   chord gives the same pair of supported factors on a proper arc and its
   complement.  The mixed-cut identity forces a pure principal hafnian
   cancellation in either case.
4. Minimizing over **all** colours and all proper even supported cancelling
   subsets—not merely the cuts selected in the preceding step—allows the
   existing abstract least-cancellation theorem to apply.  Its active core is
   connected and matching-covered, and is either one primitive even cycle or
   a branching core of cyclomatic rank at least two.
5. Three distinct off-diagonal primary killers lie outside the diagonal
   backbone, so a saturated degree-five vertex has full support degree at
   least eight.  This reconciles the new boundary with the historical theorem
   that excludes full support degree at most five.

## Adversarial checks

| attack | result |
|---|---|
| An active edge belongs to a nonzero matching, so `E_c` must have a perfect matching | Rejected.  Complement edges of that matching may be cofactor-inactive by cancellation.  The exact signed double-star has hafnian one, score one at every vertex, balanced bipartite active graph, and no active perfect matching. |
| Balanced active shores imply Hall's condition | Rejected.  Score sums prove equal shore cardinalities, but signed scores need not satisfy a nonnegative fractional-matching argument. |
| The local degree table misses an overlap | Rejected.  Exact enumeration gives 6, 60, and 390 labelled incident assignments at degrees three, four, and five.  At degree five the four shapes are `(1,1,1;2)`, `(2,1,1;1)`, `(3,1,1;0)`, and `(2,2,1;0)`. |
| The nonbranching residual remains a partial matching | Rejected sharply.  At every degree-five nonbranching vertex it has degree two, with labels `HH`, `HQ_c`, or `Q_cQ_d`. |
| Maximum residual degree two still gives principal noncancellation | Rejected by an exact six-vertex control: the full hafnian is one while a supported four-vertex principal hafnian is `1-1=0`. |
| The residual chord might already be a selected edge | Rejected.  `R` is physically disjoint from every `P_e`; active exclusivity also assigns a `Q_e` chord's only possible saturated colour to `e`. |
| Hamiltonian arc orientation is ambiguous | Rejected.  The common third bit makes both arcs odd; exactly one starts and ends with `P_d` edges.  Length one or `n-1` would identify the chord with `P_d` or `P_c`. |
| Minimal-core theorem applied with only cut-relative minimality | Corrected before acceptance.  The final proof minimizes globally over all pure colours and all proper even supported cancellations; the focused implementations exercise a cross-colour global selector. |
| The imported matrix-unit theorem is branch-specific algebra | Rejected.  Its cited core theorem is stated and proved for an arbitrary hollow symmetric scalar matrix over characteristic different from two; the matrix-unit text begins only in the application section. |
| Local type/active facts already force the mixed cut | Rejected.  The exact eight-vertex control passes normalization, bit flips, exclusivity, local degree five, and pairwise Hamiltonicity, but a displayed ordered mixed cut has product one. |
| The older maximum-degree-five theorem closes this case | Rejected.  That theorem bounds the full essential support skeleton; this theorem bounds only the saturated diagonal graph `D`. |
| A bounded replay is being called an arbitrary-order enumeration | Rejected.  Both scripts are explicitly scoped to displayed finite interfaces and controls; the written argument carries the arbitrary-order quantifiers. |
| Global or branch status is inflated | Rejected.  All three exits and the deeper-blocker branch remain open, and the global conjecture remains `UNRESOLVED`. |

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
Both reconstruct all displayed controls from exact integers.  They share no
imports.

Acceptance requires both scripts to print `PASS` and
`global conjecture status: UNRESOLVED`, Ruff and byte compilation to pass, and
the candidate-tree hygiene floor to remain green after navigation and ledger
integration.

## Publication boundary

The accepted live consequence is exactly:

```text
all-bridge Delta(D)=5 can be reduced to:
  active degree-three branching,
  primitive pure cancellation cycle,
  or connected branching pure cancellation core.
```

The smallest next proof obligations are:

1. use the simultaneous mixed cuts to control balanced subcubic active
   components that fail Hall's condition; and
2. on the nonbranching side, prove nonvanishing only for the labelled
   residual component and chord-arc subsets actually needed, since a
   universal maximum-degree-two noncancellation lemma is false.
