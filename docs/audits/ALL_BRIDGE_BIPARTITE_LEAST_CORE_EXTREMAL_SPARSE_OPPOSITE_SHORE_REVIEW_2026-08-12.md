# Hostile review: all-bridge extremal-sparse opposite-shore dichotomy

## Verdict

**PASS as an exact characteristic-zero reduction in the simultaneous
balanced all-bridge branch.**

The theorem does not exclude an extremal sparse least core.  It proves the
following conditional structure.  If a globally least bipartite pure core of
cyclomatic rank `beta` has a sparse site with

```text
d=N=beta+1,
```

then that site exhausts its shore's degree excess.  The opposite shore either
has one second extremal site, making the core an odd
`Theta_(beta+1)` subdivision, or has `2,...,beta-1` lower-degree branch sites,
each with a nonzero aggregate cofactor port.  The sparse site also satisfies
`deg_D>=beta+3` and `deg_G>=beta+6`.  At `beta=3` the two sparse-site kernels
are exactly `Q/Q` and `Q/C^2`; the full rank-three route-kernel census has five
forms and `N` is four or five.

The exact scalar controls show both sparse alternatives occur at pure-core
level and show that `N=beta+1` alone does not force a sparse site or a theta.
They are not simultaneous all-bridge witnesses.  No aggregate port is coupled
to mixed response, neither sparse alternative is excluded, and no universal
extraction or gluing theorem is supplied.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Claim reconstruction

The load-bearing chain is:

1. the globally least pure residual has a connected matching-covered allowed
   core of minimum degree at least two;
2. all-bridge bit flips make that core bipartite;
3. on each bipartition shore, the degree excess above two is `beta-1`;
4. its matching polytope has dimension `beta`, so its number `N` of perfect
   matchings is at least `beta+1`;
5. the cofactor-port theorem partitions those `N` matchings into nonempty
   ports with nonzero port sums;
6. sparsity at a site means `N=d`; consequently A3's bounds force the exact
   equality `d=N=beta+1`.

The new argument begins only after item 6.  The sparse site's excess
`d-2=beta-1` exhausts one shore.  The opposite shore's positive excess parts
sum to `beta-1`.  One part gives a second degree-`beta+1` site.  Two or more
parts give degrees at most `beta`, hence strictly fewer ports than matchings
and a nonzero multi-monomial port at every opposite branch site.

The one-part case additionally uses the fact that a nontrivial connected
matching-covered graph has no cut vertex.  Suppressing degree-two chains can
therefore create no petal based at either of the only two branch vertices;
all `beta+1` chains join the two sites.  They have odd length because the
sites lie on opposite bipartition shores.

At rank three, each shore has excess two.  The only shore profiles are `Q`
(one quartic site) and `C^2` (two cubic sites).  In the sparse branch this
gives `Q/Q` or `Q/C^2`; the latter has route multiplicities `(2,2,1)`.  For
the complete census, the `C^2/C^2` degree equations reduce to

```text
h+p+q=3,
```

where `h` is the same-shore route multiplicity and `p,q` are the two cross
perfect-matching multiplicities.  Connectivity and allowedness leave exactly
three further kernel types, with matching counts five, four, and four.

## Adversarial checks

| Attack | Result |
|---|---|
| `N=beta+1` might already force `Theta_(beta+1)` | **Rejected.** Weighted `K_(3,3)-e` has `beta=3,N=4`, is a least matching-covered residual, and has no quartic site. |
| A sparse site might still force a global multi-theta | **Rejected.** The eight-vertex `Q/C^2` control has one sparse quartic site opposite two cubic aggregate sites. |
| Shore exhaustion might use a hidden maximum-degree hypothesis | **Rejected.** It is the degree-excess identity plus `d=beta+1`; no bound on `D` is used. |
| The opposite lower-degree sites might have only a combinatorial multi-port, not a nonzero aggregate | **Rejected under the stated hypotheses.** Global leastness and the imported cofactor-port theorem make every port sum nonzero.  The theorem does not claim this for arbitrary matching-covered graphs. |
| Connectedness alone might justify the route conclusion | **Rejected as too weak.** Matching-coveredness is load-bearing in the cut-vertex parity proof. |
| Suppression might create a route returning to the same branch site | **Rejected.** Such a petal makes that site a cut vertex once there is a second branch site. |
| The two-site routes might have mixed parity | **Rejected.** Their endpoints lie on opposite fixed bipartition shores, so every route is odd. |
| A `C^2/C^2` kernel with `h=2` might be missing | **Rejected by allowedness.** Its cross routes are forced into endpoint state `00`, so their endpoint edges occur in no perfect matching. |
| A `C^2/C^2` kernel with `h=3` might be missing | **Rejected by connectivity.** It separates the two shores. |
| The density landing might double-count physical edges | **Rejected.** The `beta+1` colour-`e` support edges avoid the two other pairwise-disjoint positive-degree active graphs.  A2 then contributes three distinct offdiagonal killers in `G`. |
| The finite census might be carrying the arbitrary-order proof | **Rejected.** The written shore partition, cut-vertex lemma, suppression, and integer kernel equations carry the quantifiers; both scripts label their enumeration as bounded QA. |
| The scalar controls might be promoted to all-bridge systems | **Rejected explicitly.** They contain one weighted pure least residual only and do not supply the other colours, active decks, mixed cuts, or target equations. |

## Computational evidence and independence

The primary verifier

```text
python -B claims/arbitrary-order/verify_all_bridge_bipartite_least_core_extremal_sparse_opposite_shore.py
```

checks the integer shore-partition and density ledgers, all ten rank-three
`(h,p,q)` rows, exhaustive connected bipartite matching-covered graphs through
equal shores `4+4`, the `N=4` and `N=5` rank-three kernel counts, and exact
rational `Theta_4`, `K_(3,3)-e`, `Q/C^2`, and `C^2/C^2` controls.  It verifies
all proper supported balanced minors in the weighted least-residual controls.

The independent audit

```text
python -B claims/arbitrary-order/audit_all_bridge_bipartite_least_core_extremal_sparse_opposite_shore.py
```

uses only the Python standard library, imports neither repository code nor the
primary verifier, and independently rebuilds perfect matchings, connectivity,
ports, shore profiles, and exact proper-minor values.  It exhausts connected
bipartite matching-covered supports through `4+4` and independently confirms
the sparse `Q/Q` versus `Q/C^2` census and both decisive rational
countercontrols.

The implementations differ in derivation and coverage topology.  Agreement
between them is exact bounded evidence for the displayed mechanisms, not an
exhaustive arbitrary-order proof.

## Publication boundary

```text
globally least all-bridge pure core:                         IMPORTED;
extremal sparse site d=N=beta+1:                            ASSUMED;
same-shore degree-two exhaustion:                           PROVED;
one opposite extremal site / several aggregate sites:       PROVED EXHAUSTIVE;
one-site alternative is odd Theta_(beta+1):                 PROVED;
deg_D>=beta+3 and deg_G>=beta+6 at sparse site:              PROVED;
beta=3 sparse Q/Q or Q/C^2 kernels:                          PROVED EXHAUSTIVE;
complete beta=3 five-kernel census and N in {4,5}:           PROVED;
N=beta+1 forces sparse site or theta:                        REFUTED;
either sparse-shore alternative impossible:                 OPEN;
opposite aggregate ports coupled or independent:            OPEN;
every least core has an extremal sparse site:                OPEN;
localized active-deck shore equals globally least core:      OPEN;
scalar controls are simultaneous all-bridge witnesses:       FALSE / NOT CLAIMED;
deeper blocker and universal extraction/gluing:              OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.
```

The next proof obligation is not more pure graph enumeration.  It is to
couple every forced opposite-shore aggregate port to mixed target response,
exclude the two-extremal odd multi-theta using genuinely all-bridge data, or
prove that a localized active-deck cancellation transfers its labels to the
globally least core.
