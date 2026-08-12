# Review: all-degree localized pure cancellation and bipartite least-core reduction

## Verdict

**PASS as an exact characteristic-zero reduction in the simultaneous balanced
all-bridge branch.**
The proposed theorem removes the artificial upper-degree restriction from the
active-deck localization proved in the degree-five owner.  Every all-bridge
system has a supported pure hafnian cancellation of at least one of the
following three forms:

```text
inactive-selected-edge complement;
one side of a selected-matching-component/complement cut;
one side of a Hamiltonian-chord-arc/complement cut.
```

The forms are exhaustive, not globally exclusive.  When every active graph
has a perfect matching, the component/Hamiltonian alternative is exhaustive
for each fixed selected matching triple; different triples may expose
different forms.

The theorem also separates two statements that the degree-five owner had
presented together.  Every globally least pure core is bipartite at **every**
all-bridge saturated degree.  Only the subcubic bound and the degree-five site
labels require `Delta(D)=5`.  Consequently the one-open-port theta from the
generic pure-core theorem is impossible after all-bridge specialization, and
cyclomatic rank two is always one closed all-odd theta.

Finally, the perfect-matching polytope of a connected bipartite
matching-covered least core has affine dimension equal to its cyclomatic rank
`beta`.  Thus a rank-`beta` core has at least `beta+1` perfect matchings.  A
branch vertex of degree at most `beta` therefore carries a genuine nonzero
multi-monomial cofactor port; a sparse fan can survive only at the extremal
equality `d=N=beta+1`.

These are reductions, not exclusions.  No localized cancellation form, closed
theta, aggregate port, or extremal sparse fan is proved impossible.  The
separate deeper-blocker branch and universal extraction/gluing remain open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Claim reconstruction

The reviewed proof has seven load-bearing steps.

1. The inherited all-bridge identities give `haf(Z^c[V])=1`, the ordered
   mixed-cut products, active-deck score one, pairwise active exclusivity, the
   saturated bit flips, and the unconditional lower bound `Delta(D)>=5`.
2. If some active graph `E_c` has no graph-theoretic perfect matching, any
   nonzero full colour-`c` matching contains an inactive support edge `f`.
   Its full complementary cofactor is zero while the remaining matching
   supports `V-f`.  Minimal Hall deficiency further gives a boundary score
   `-1` and `b=q+2>=2` vertex-disjoint inactive repairs with all three global
   pair-deletion cofactors zero.  No degree bound is used here.
3. Otherwise choose any perfect matching `P_c subset E_c` in every colour.
   Active exclusivity makes the three selected matchings physically disjoint.
   At a vertex of `D`-degree at least five, they occupy only three incident
   edges, so `R_P=D-(P_0 union P_1 union P_2)` is nonempty.  This uses the
   inherited lower bound, not an upper bound on `D`.
4. If some `P_c union P_d` is disconnected, each component and its complement
   have the displayed supported matchings and the ordered mixed cut kills one
   factor.  If every selected pair is Hamiltonian, any `r in R_P`, any colour
   supporting `r`, and either other colour produce two odd Hamiltonian arcs.
   The uniquely `P_d`-ended arc is proper and supplies the two supported
   mixed-cut factors.  The proof never uses `deg(R_P)<=2`.
5. Every edge of `support(Z^e)` flips both fixed non-`e` normal bits.  Either
   bit therefore gives a global bipartition of the support and of every least
   core `A_S`.  The generic one-open-port theta contains odd cycles and is
   consequently unavailable in the all-bridge specialization; every local
   two-exit carrier is closed all-odd.
6. If the least core has shores `L,R`, matching-coveredness supplies a perfect
   matching, so `|L|=|R|`.  For cyclomatic rank `beta`,

   ```text
   sum_(v in L)(deg(v)-2)=sum_(v in R)(deg(v)-2)=beta-1.
   ```

   Thus `beta=1` is one even cycle.  At `beta=2`, exactly one cubic site lies
   on each shore.  Matching-coveredness rules out bridges, and suppression of
   degree-two paths gives three odd routes between the two cubic sites: one
   closed all-odd theta with exactly three perfect matchings.
7. For a connected bipartite matching-covered graph, the nonnegative system
   `Bx=1` is the convex hull of perfect-matching incidence vectors: Hall's
   condition holds on the positive support, and iterative subtraction of a
   supported perfect matching gives a finite decomposition.  The unsigned
   incidence matrix has rank `|V|-1`; matching-coveredness supplies a strictly
   positive feasible average, so no coordinate inequality shrinks the affine
   hull.  The polytope dimension is therefore

   ```text
   |E|-|V|+1=beta.
   ```

   Hence `N>=beta+1`.  Shore excess also gives `deg(v)<=beta+1`.  Combining
   this with the exact cofactor-port partition proves a forced aggregate port
   whenever `deg(v)<=beta`; sparse ports can occur only when
   `deg(v)=N=beta+1`.

## Adversarial checks

| attack | result |
|---|---|
| The localization still needs `Delta(D)<=5` | Rejected.  The no-perfect-matching argument is explicitly degree-free.  In the all-perfect-matching case, the already proved `Delta(D)>=5` makes every selected triple leave a residual saturated edge; the component/chord proof uses no upper bound. |
| `Delta(D)>=5` means every vertex has degree five | Rejected.  Only one vertex of degree at least five is needed to prove `R_P` nonempty. |
| Selected active perfect matchings can overlap | Rejected.  Active exclusivity makes the three physical edge sets pairwise disjoint. |
| A selected pair need not be cycles | Rejected.  Two edge-disjoint spanning perfect matchings form a spanning disjoint union of alternating even cycles. |
| The residual chord may equal a selected edge | Rejected.  It is chosen in `R_P`.  Arc length one or `n-1` would identify it with a selected edge and is therefore impossible. |
| Only one convenient selected triple is covered | Rejected.  The proof works for every selected triple.  For a fixed triple, disconnected-pair versus all-pairs-Hamiltonian is exhaustive. |
| Hall balance silently assumes positive scores | Rejected.  Equal shore size follows from signed score sums in characteristic zero; Hall deficiency is retained and sharpened rather than dismissed. |
| The two Hall repairs require maximum degree five | Rejected.  The matching ledger `b=q+2` is degree-free.  Only the later claim that their endpoints cannot have active degree three uses the degree-five cap. |
| Bipartiteness needs the subcubic estimate | Rejected.  Bipartiteness comes directly from either fixed non-colour bit flip; subcubicity is a separate degree-five consequence. |
| The generic one-open-port theta remains possible | Rejected only in this specialization.  It contains odd cycles, so it cannot lie in the all-bridge pure support.  The generic pure-core theorem and its abstract sharp example remain valid outside all-bridge. |
| Rank two could contain a degree-four branch site | Rejected.  The separate shore excess is one on each side, forcing exactly one cubic site per shore and all other degrees two. |
| `Bx=1` may have fractional vertices outside the matching hull | Rejected for bipartite graphs by the explicit Hall/subtraction decomposition. |
| The polytope dimension may drop below `beta` | Rejected.  Connected bipartite incidence rank is `|V|-1`, and the average of all perfect matchings is strictly positive because the graph is matching-covered. |
| `N>=beta+1` alone forces an aggregate at every branch site | Rejected as too strong.  It forces an aggregate only when `d<=beta`; the extremal sparse case `d=N=beta+1` survives and has exact theta-fan controls. |
| A finite graph scan proves the arbitrary-order theorem | Rejected.  The written Hall, incidence-rank, and mixed-cut arguments carry the arbitrary-order quantifiers; scripts test mechanisms and sharp controls only. |
| An abstract pure-core control is an all-bridge witness | Rejected.  The controls do not supply the three simultaneous target tables or universal extraction. |
| The global conjecture is closed | Rejected.  Every newly displayed topology and port alternative remains open as an exclusion, and the deeper-blocker and extraction branches remain. |

## Evidence replay

Run from repository root:

```powershell
python -B claims/arbitrary-order/verify_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
python -B claims/arbitrary-order/audit_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
uv run --with ruff ruff check claims/arbitrary-order/verify_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py claims/arbitrary-order/audit_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
python -m py_compile claims/arbitrary-order/verify_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py claims/arbitrary-order/audit_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
```

The primary and audit must use independent graph representations and matching
enumerators.  Their bounded obligations are the selected-pair component/chord
geometry, the Hall-repair control, bipartite shore excess, affine rank of the
matching polytope on small matching-covered graphs, the extremal sparse
`Theta_d` family, and a genuine aggregate-port control.  Neither script is an
arbitrary-order graph enumeration or a complete witness checker.

Acceptance additionally requires exact theorem hashing, repository hygiene,
the migration and lattice regression floors, a fixed-point link rewrite, and
hostile review of the frozen candidate bytes.

## Publication boundary

The candidate live consequences are exactly:

```text
every simultaneous balanced all-bridge system:
  one of three active-deck-localized supported pure cancellations: REDUCED;
  minimal Hall-deficient shore has two common-cofactor-zero repairs: PROVED;
  globally least pure core is bipartite: PROVED;
  every local two-exit theta carrier is closed all-odd: PROVED;
  beta=1 core is an even cycle/binomial: PROVED;
  beta=2 core is a closed all-odd theta/trinomial: PROVED;
  N>=beta+1 for every least core: PROVED;
  d<=beta branch site has a nonzero aggregate port: PROVED;
  sparse fan only at d=N=beta+1: PROVED BOUNDARY;

impossibility of the three localized forms: OPEN;
aggregate-port exclusion: OPEN;
extremal sparse-fan exclusion: OPEN;
deeper-blocker branch: OPEN;
universal extraction/gluing: NOT PROVED;
global Krenn--Gu conjecture: UNRESOLVED.
```

The smallest next obligations are to couple a localized cut or Hall repair to
the simultaneous mixed target system, control a forced aggregate cofactor
port, or add all-bridge data that excludes the extremal sparse fan.
