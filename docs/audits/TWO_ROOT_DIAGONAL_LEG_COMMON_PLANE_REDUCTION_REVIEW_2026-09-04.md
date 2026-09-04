# Final exact-text review: diagonal-root-leg common-plane reduction

2026-09-04. Reviewer lab_r2_consolidation_review. Final disposition: PASS.

Reviewed owning document:

  claims/finite/n08/TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_THEOREM.md
  SHA256 536a438812475f83cc0be7be8c385581d5c1a81e7093a76a0852587a367a32ce

Reviewed primary replay, without rerunning it:

  claims/finite/n08/verify_diagonal_root_leg_source.py
  SHA256 595ede70345e05d93fefbace8ff71f03b878533f1891079665b172dfb3ba60c2

Read the final owning proof, compared its core to the independently reviewed candidate, and separately checked BOTH the added Section 9 parent application and the appended longer parent-application proof. They duplicate some exposition but make consistent mathematical claims. The duplicate is not a mathematical HOLD.

## Main theorem and exact scope

The theorem assumes only an actual complex ternary eight-vertex GHZ matching tensor and the displayed root architecture: invertible Q,L_i,M_j with nonzero diagonal-unit opposite spokes. It allows arbitrary outside AA/AB/BB blocks and does not assume maximum torus-root cardinality for the main implication.

The conclusion is a NECESSARY SOURCE REDUCTION: at least one shore's three inactive image planes coincide; every coincident shore has a zero full-opposite-shore hafnian and the explicitly retained corrected matrix cofactor equation. It does not exclude the coincident-plane source, assert H_FULL=0 under simultaneous activations, show that the architecture occurs in every witness, or prove a global resolution. All determinant-zero cases, all normal-coordinate supports, and both simultaneous coincidences are retained.

## Main analytic proof validation

The complete source retains the two-root direct edge, cross-shore root partners, both same-shore partner sectors, and the doubly transverse sector. It uses actual same-graph cofactor blocks with zero diagonals. Matching multiplicities and the transpose conventions are correct.

The full one-shore determinant factorization is valid even when an inactive determinant is identically zero. Full P and R determinants are nonzero and squarefree by invertibility of the individual star maps and multiaffinity. Taking determinants, applying UFD, and comparing vertex degrees gives H=detP*g or H=f*detR with the stated shore-only polynomials, including zero factors.

The universal adjugate mixed-normal identity has been independently reconstructed both before coefficient extraction and by direct term expansion. Row/column deletion removes the selected normal variables from the relevant cofactors and adjugate rows. The AA/BB terms vanish at their literal zero diagonal entries, while the two surviving cross terms have exactly d_i e_j and alpha_i beta_j A_ij B_ji. The target has the stated diagonal psi_i A_ii B_ii. This identity needs neither inactive determinant nonzero.

When both inactive determinants are nonzero, their disjoint variable sets and squarefreeness yield the one constant kappa, including zero. The corresponding N_ii has shore-flattening rank three for an omitted index whose complementary plane pairs are distinct on both shores. Such an index exists because each noncoincident triple has at most one coincident complementary pair. The diagonal source forces N_ii to divide a nonzero A-only times B-only product, which would give shore rank one by UFD. This contradiction covers every kappa and makes no generic coefficient exception.

The plane/determinant equivalence is correct: with two different planes, choose a vector in one outside a selected third plane, a second independent vector from the remaining plane, and then a third vector in the selected plane outside their span. Thus nonzero determinant is equivalent to the triple not being wholly coincident.

On a coincident shore with arbitrary normal n, the contracted full source gives C_BB t=-f adj(R)Q^T n. The literal remaining-B-port indexing yields three symmetric products of linear forms equal to nonzero rank-two skew targets if f!=0. Rank two forces all three coefficient frames into one common two-dimensional image plane BEFORE the binary Gram argument. The first two skew pairings then make the other frames proportional, contradicting symmetry of their final pairing. This handles zero normal coordinates and zero cofactor forms by immediate frame-rank failure. Thus f=0 uniformly, and full-R polynomial cancellation supplies the corrected matrix equation. The transposed statement is equally valid.

There is no appeal to the false unrestricted three-dimensional symmetric-middle Gram claim, no enlargement of inactive spaces, and no replacement of a full cofactor by an unrelated array.

## Parent application: independent verification

I read the owning THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md and verified that its quantum-graph consequence supplies a nonzero single-column block for EVERY vertex and remote colour. It is a universal full-source structural consequence, not a generic numerical assertion.

For a hypothetical maximum-r=2 witness, a triangle of three invertible physical blocks would make the product of the three cross-product components vanish on the torus part of the rank-three bilinear root hypersurface. That hypersurface is irreducible with dense torus part. One component must be divisible by the root form and hence a constant multiple of it. Its coefficient matrix has rank at most two, so it must be zero. Invertibility of the two leg maps makes their two-coordinate projections surjective and prevents that component from being identically zero. Thus the rank-three physical-edge graph is triangle-free.

At a vertex with exactly four invertible neighbours there are exactly three other neighbours. The three different colour-killer blocks are nonzero and cannot be invertible or share one physical edge, so they exhaust those three neighbours. For the unique colour-c block b_c(x)z[c], if b_c is not proportional to x[c], choose x in ker b_c with x[c]!=0, avoiding the finitely many inverse-image coordinate-c lines of the four invertible maps. Such x exists in the two-dimensional kernel plane. Each remaining neighbour's row kernel then admits a vector with nonzero coordinate c. Fixing the killed neighbour to e_c makes every graph matching vanish while the full GHZ contraction has its single nonzero c product. This contradiction proves each complementary block is a nonzero scalar E_cc. It explicitly permits boundary vectors and does not misuse a torus-only condition.

For adjacent degree-four vertices r,s, their other three rank-three neighbour sets are disjoint by triangle-freeness. They partition the six outsiders. Each root's opposite three edges are the just-proved distinct diagonal units. Labelling by these unit colours gives precisely Q,L_i,M_j and alpha_i,beta_j in the main statement. This application assumes adjacency and degree four; it does not claim that such vertices necessarily exist. No AA/BB support condition is required for the main reduction.

## Replay and evidence distinctions

The primary script statically matches its described purpose. It reconstructs actual root-open tensors through nine root basis evaluations and exact subset-recursive hafnians, extracts mixed normal coefficients by four corners, and compares the universal adjugate identity on three explicit integer fixtures. Dense arbitrary outside blocks, nonsymmetric Q, nonunit spoke weights, and determinant-zero fixtures exercise the index conventions. Its 27 checks and 105-matching count are finite corroboration, not a quantified exclusion certificate or an independent proof of the analytic implication.

The final prose preserves that distinction and explicitly leaves the corrected coincident-plane source equations, other invertible components, lower-rank graphs, and global Krenn--Gu open. The unfinished finer cofactor arguments are not promoted into this theorem.

## Final receipt

PASS for the exact owning hash above, including both presentations of the parent application. No mathematical hypothesis drift, incomplete case promotion, incorrect source cancellation, circular use of the result, generic-to-pointwise jump, or frame-dimension gap was found.

No tracked files were edited, no checker or other computation was rerun for this final review, and no process remains owned. This is the sole final-review artifact. Later mathematical edits require a new exact-text review; purely editorial status/navigation changes may be checked by a pinned diff addendum.

## Final status and proof-topology addendum

2026-09-04. PASS is confirmed for final owning-document SHA256:

  b095cff74313172004efa7fea4cf15ed99b44a8bd3a59f8d1bc5e731e2f47731

Compared the final text with the reviewed mathematical body. The changes remove the redundant worker appendix while retaining the independently reviewed Section 9 parent proof, promote candidate wording to the reviewed proved source-reduction status, and point Section 8 to that exact application. No hypothesis, quantifier, source identity, determinant case, or conclusion changed.

Reviewed N8R2S in the frontier node, both graph arrows, owning-claim table, and relationship table. They consistently state a source REDUCTION to at least one coincident shore with a zero opposite-full-shore hafnian and corrected matrix cofactor equation. The adjacency/degree-four application is conditional at n=8/max-r=2; neither such vertices nor an exhaustive architecture cover are asserted. The whole coincident cofactor system, arbitrary invertible components, lower-rank source graphs, and global conjecture remain open. The main theorem's independence from maximum-root and outside-support assumptions after the root architecture is specified is correctly recorded.

The parent strategy's accepted outcome accurately describes the all-kappa nondegenerate contradiction, forced two-dimensional Gram representation, uniform normal-support coverage, and retained simultaneous-source obligation. Its control paragraph correctly distinguishes scalar hafnian factorizations from full corrected matrix one-shore source and does not claim the control satisfies the latter. One editorial reference to the removed 'owning appendix' was reported to the integration owner for replacement by 'Section 9 of the owning theorem'; it changes no mathematical scope or dependency.

Final mathematical and proof-topology disposition: PASS. The unfinished normal-support cofactor sublemma is not included or awaited. No tracked files edited, no new research scope opened, no computation rerun, and no owned process left running.

## Final editorial hash receipt

2026-09-04. Final PASS for owning-document SHA256:

  dbe6c6ccddad18a103faf31b28bd87e72feed63f599a87bcb0130d090393bb99

Verified the exact byte-level difference: deleting only the added replay clarification reproduces the previously reviewed b095cff74313172004efa7fea4cf15ed99b44a8bd3a59f8d1bc5e731e2f47731 hash. Thus no mathematical proof or scope changed. The clarification correctly states that the replay fixtures are not GHZ witnesses and that their actual root-open tensor supplies the right side of the general matching identity, matching the earlier static code review.

Also verified the parent strategy now refers to Section 9 of the owning theorem rather than the removed appendix. No stale application reference remains at that location.

Final disposition: PASS, ready for the coordinator's staging and ordinary final checks. No new candidate research or audit was started. No tracked files edited and no process remains running.
