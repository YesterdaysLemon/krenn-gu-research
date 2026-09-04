# Final low-rank completion integration review

2026-09-04. Reviewer: independent Astra-high subagent
`lab_r2_consolidation_review`. Final mathematical integration disposition:
**PASS** for the [completion theorem](../../claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_COMPLETION_THEOREM.md).

Reviewed the three owning documents in the astra-r2-lowrank-20260904 integration worktree:

| Owning document | SHA256 |
| --- | --- |
| claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_COMPLETION_THEOREM.md | da18dd803823f1767fefc9207db6c3b8f4624a9914ad2f785e503688b80beea9 |
| claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_RANK_ONE_EXCLUSION.md | 155e848fb31b6be9045e12b2fe3f5f1cad1e0fed35730ce734759ec16bfb94c1 |
| claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md | 0bb809cf69bdd23dff6ca60f722ea86e8bc26491ba6c6e65c8030e6d5efef02e |

This is a final exact-text mathematical integration review following the independent rank-one and zero-block analytic audits. I read the full updated owning texts, the accepted certificate/package reviews' scope and acceptance statements, and the generator's physical vertex/word/anchor mapping. I did NOT rerun or independently recertify the decision-tree checker. Its accepted proof traversal is supplied by the separately named encoding/certificate and package reviewers and the coordinator's completed replay.

## Completion cover and noncircular dependencies

The completion statement contains no root-rank or kernel assumption beyond the explicit physical common-coordinate n=8/max-r=2 hypotheses. Its rank split is exhaustive: rank>=2 uses the already merged theorem at 73955ca0; nonzero rank one is split into matrix monomials, neither factor coordinate, and exactly one factor coordinate up to root transposition; Q=0 is separately treated.

A nonzero matrix monomial cannot vanish on the product torus and is therefore incompatible with the chosen maximum torus-root pair. This is an exact exclusion, not an assumed missing rank-one branch. The two nonmonomial rank-one branches retain every zero-leg and central-port case. The zero-root re-rooting argument invokes only the prior rank>=2 result on the same graph, never the completion theorem itself or an unaccepted rank-one theorem. Thus the cover is noncircular.

The final scope is completion of THIS common-coordinate eight-vertex maximum-two-root child only. Supply of these incidences for arbitrary witnesses, maximum r=1, larger orders, the global parent, and global resolution remain separate and explicitly unresolved.

## Rank-one integrated proof

The rank-one owning document now states and proves the reusable polynomial cofactor lemma with its source-independent physical inputs. It does not invoke the rank>=2 source theorem at rank one. H=0 follows from nonzero Q, while label counts and same-pair matrix independence use Q not proportional to E_cc, rather than an invalid rank comparison.

Line membership L/R includes zero and is explicitly distinguished from first-root-only/second-root-only orientations. The projections, isolated central both-leg port, central zero-b hub, pure zero-a clique, quotient-opposite components, and remaining D components match the independently audited cover. The special K_t=p(gamma_t q+delta_t p)^T is retained with its potentially nonzero gamma_t and noncoordinate row; no coordinate-unit replacement is made.

The inherited orientation-triangle proof uses only zero root legs and pure outside cofactors. The rank/UFD/cofactor/six-cycle endpoint is rederived without a hidden root-rank assumption. Both coordinate-factor orientations are covered by exchanging the root labels, which preserves the physical common-coordinate property and GHZ target.

## Zero-block integrated proof

The initial Q=0 source explicitly has no H_B Q term, and the inactive stress is H=t_c+sum t_e. The proof never initially sets H to zero. Its complete orientation count a>=b includes the source restrictions on partners' own-axis legs; all small-clique cases and the one possible both-leg edge are accounted for.

The H=0 branch is reproduced as a conditional polynomial argument, not as an illicit application of a nonzero-root theorem. The retained (3,2), aligned (2,2), and F-perfect-matching branches retain H!=0 and are closed by the independently checked cofactor algebra. The factor-two identities and matching-support argument remain unchanged and require no hidden full-hafnian vanishing.

Only the pure-(3,3) branch proceeds to full ternary cofactor equations. The document explicitly distinguishes these full equations from their inactive restrictions, retains nonzero root-leg scalars without modifying the graph, and proves the six FULL AA/BB blocks are nonzero matrix units. It never claims FULL H_B=0 and never adds or changes a root edge.

The general P2 row/column anchor lemma covers rank-one and zero blocks, using an unanchored first-row evaluation rather than assuming rank>=2. Re-rooting at a hypothetical rank>=2 X_ij provides the exact shared-coordinate physical incidences for all six outsiders. Its new block has a torus zero by the Laurent-unit argument, so it is a valid maximum pair in the unchanged graph. The invocation of the accepted rank>=2 theorem is legitimate and proves all nine X blocks have rank at most one.

## Full cofactor word and support map

The package generator uses vertices 0,1,2 for A0,A1,A2 and 3,4,5 for B0,B1,B2. Cofactor (i,j) deletes vertices i and j+3, assigns all 81 words to the remaining vertices in their sorted order, and enumerates their three perfect matchings. Thus its unique nonzero target condition i==j and word==(i,i,i,i) matches the owning full f_i exactly. The nine cofactor tensors contribute precisely three nonzero and 726 zero coefficient positions. This is not an inactive binary-word map.

The six same-shore edges are exactly the AA and BB blocks and allow all nine physical coordinate entries as their nonzero matrix-unit choice. Cross blocks allow empty support. Rank-one rectangular-support implications agree with the physical rank<=1 reduction.

For off-diagonal cofactor (i,j), the remaining A row pair is the complement of i and the remaining B column pair is the complement of j. The chosen AA unit fixes its two actual A endpoint coordinates, and the BB unit fixes its two actual B endpoint coordinates. Generator row/column selector clauses use those respective coordinates at the correct endpoints and constrain the two corresponding cross blocks. This faithfully expresses the proved P2 support disjunction, including zero blocks. Every physical solution extends to selector values; no converse or coefficient-realizability assertion is made.

This focused semantic map check is consistent with the separate complete encoding reconstruction. It does not substitute for that reconstruction or its certificate checker.

## Accepted certificate interface

The owning zero-block proof explicitly identifies a NECESSARY support relaxation, not an equivalent complex coefficient system. It correctly uses field nonzero-product semantics, excludes singleton support at zero target coefficients, and only requires some nonzero term at a nonzero target. Dropping actual cancellation equations enlarges the feasible set, so a sound UNSAT proof of this relaxation is sufficient.

The frozen CNF hash 4415ea3d243603910729098d104240ca2d6fd2fa1d2843098e3131b4088ac1ac and certificate hash d73b746cbf5bafdcb1ac6e2af9bcac65475e5d7d1595f82cabca25bc8556c1fd agree with the separately accepted review records. Those records report exact reconstruction of all 11,394 clauses and acceptance of all 6,860 binary branch nodes and 6,861 conflict leaves. The portable package review preserves the distinction between canonical and formatted checker hashes and records semantics-preserving integration. The parent additionally reports the completed packaged replay, including child and bounded-runner exit zero.

The prior analytic audit's HOLD was explicitly for closure WITHOUT this separate proof gate. The integrated documents now cite the accepted distinct gate, so that former pending condition does not remain a mathematical gap. This review does not relabel the analytic reviewer as the certificate producer or independent checker reviewer.

## Final disposition and boundaries

PASS: the integrated rank-one proof, zero-block analytic-plus-certificate implication, and exhaustive completion cover compose without circularity, omitted root-rank cases, inactive/full-hafnian confusion, or scope inflation. The completion is conditional on the stated common-coordinate physical incidence and does not resolve the global conjecture.

No tracked files were edited, no new mathematical scope was pursued, no checker traversal or other computation was launched, and no process is left running. This receipt is the sole new scratch artifact. The PASS is pinned to the three owning-document hashes above; later mathematical edits require their own review.
