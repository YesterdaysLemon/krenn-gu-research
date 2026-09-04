# Final joint-kernel boundary review

2026-09-04. Reviewer lab_r2_consolidation_review. Disposition: PASS for the exact analytic statement and its final necessary-boundary corollary.

Reviewed candidate:

  claims/finite/n08/TWO_ROOT_JOINT_KERNEL_BOUNDARY_THEOREM.md
  SHA256 09cbdee6112833893f9f6388b2acd54d7c2e36f8eb27a05f54b8b2bcb58b17be

Its mathematical body is unchanged from the fully read cofactor-worker consolidation tmp/lab-kernel-source.md, SHA256 3d90855eda60fcc6210badcd50c675a73548e3ecc50cdc4651774b168c344e8b. I checked the exact file diff: only title/status/navigation and the explicitly reviewed final corollary were added or adjusted. This review includes the entire unchanged proof and that corollary.

## Exact accepted scope

For a complex ternary n=8 hypothetical GHZ witness with global maximum torus-root cardinality two, an invertible physical root pair cannot have, at EVERY outsider, a joint-kernel vector with exactly one zero coordinate and two nonzero coordinates. Consequently every invertible physical edge in such a witness has some outsider whose joint kernel is zero or a coordinate axis.

This does not assert existence of an invertible edge, exclude either of the two necessary residual kernel types, address the all-rank-at-most-two physical-block branch, supply a common-coordinate pair for arbitrary incidences, or resolve the global conjecture. Global status remains UNRESOLVED.

## Load-bearing checks

1. **Pair labels use full source.** The all-kernel evaluation yields a diagonal target of rank at most two, forcing each label to occur. The singleton activation then yields a nonzero rank-one target with no two-root-partner term, forcing each label to occur twice. The exact-one-zero assumption supplies all nonzero target factors in both steps.

2. **Full pair factorization.** With the other four kernel vectors fixed, the residual f_c is a scalar and is nonzero by the rank comparison. The determinant identity in C[z,w] is exact. Integral-domain reasoning forces the scalar polynomial gamma to be zero or a constant times z[c]w[c], including adj(Q)_cc=0. No generic physical coefficient condition or division by gamma is used. The resulting K_uv=M_c z[c]w[c] is a full two-port tensor identity.

3. **Anchor extraction keeps zero cases.** If one port fails the common-column condition, evaluate it on ker e_c. With both nonzero response vectors, cancellation forces both mate maps through one common linear functional, and the nonzero full pair factorization forces that functional to be e_c. With exactly one nonzero response, one mate map is zero and the full factorization forces the other to use e_c. Thus a genuine two-dimensional inactive anchor is DERIVED at one member of every pair. Its mate remains on its actual one-dimensional joint-kernel line.

4. **Auxiliary active choices are pointwise.** Restricting a nonzero homogeneous linear or separately bilinear physical channel to assigned-coordinate-one affine slices cannot make it identically zero. A finite product of chosen nonzero entries has a nonempty nonvanishing set over C. The simultaneous active choice therefore preserves every identically zero physical leg and full channel without removing any physical coefficient stratum. In particular evaluated pure orientations are physical zero-leg orientations.

5. **Constant graph classification is valid.** Its same-pair M_c retains the rank-three source shape, and every nonzero cross channel is independent of Q. The complete-bipartite ratio analysis and doubled-group argument give F components of order at most three, with nonzero signed group counts and only pure orientation triangles. No claim of binary dimension at a mate is used here.

6. **Cofactors are re-extracted on the enlarged spaces.** Section 5 reuses the actual full source to prove H=0 and the nonzero pure f_c on the product of three binary anchor planes and three kernel lines. It does not interpolate them from the earlier scalar samples. Nonexceptional cross cofactors vanish by the auxiliary active pair and rank independence. All resulting objects remain actual principal hafnians of the same restricted physical graph.

7. **One anchor suffices for support separation.** For t_c versus t_d, the third group's anchor uses different independent coordinates. Its line mate contributes only nonzero scalar multiples and cannot erase this distinction. Thus the signed stress argument is valid on nine variables, despite the absence of a second binary mode in each group.

8. **The two-triangle branch invokes an established consumer legally.** Full paired factorization plus physical zero-leg orientations forces BOTH members of every group to have common-coordinate physical blocks. The already proved N8R2C applies on this same graph. The proof does not transplant a two-binary-shore flattening into a setting where its independence might fail, and does not invoke the current theorem circularly.

9. **One-anchor UFD and gradients are explicit.** A rank-one cross block with nonzero pure permanent has all entries nonzero. UFD and endpoint multidegrees force the pure endpoint factors. At line endpoints their coefficients are nonzero because the chosen kernel line has both other coordinates nonzero. In an adjacent cofactor product, its two terms differ at the shared group's binary anchor and therefore cannot cancel. The corresponding rank/invertibility arguments are scalar matrix arguments over the fraction field of the fixed polynomial ring and remain valid.

10. **Six-cycle endpoint retains a real monomial distinction.** The support count uses the same six physical vertices. In the equality case the two complementary six-cycle matchings differ at all three binary anchors, even though the line-mode factors are proportional. Both coefficients are nonzero, so their distinct anchor monomials cannot cancel. No missing local variable is silently reintroduced.

## Final necessary-boundary corollary

Every invertible physical edge admits a product-torus zero: its evaluated covector can be chosen noncoordinate at a torus point, and the resulting noncoordinate hyperplane contains a torus vector. The global maximum two then makes this a usable maximum root pair.

An outsider's PHYSICAL joint kernel cannot contain a torus vector, or it would extend that pair to three roots. Since a linear subspace over C cannot be covered by finitely many proper subspaces, a torus-avoiding joint kernel lies in a coordinate hyperplane. A nonzero such subspace is either that whole coordinate hyperplane (dimension two), a coordinate axis, or a line of support two. The hyperplane and support-two line have vectors with exactly one zero coordinate. If all outsiders had these two types, the proved exclusion would apply. Therefore some outsider has zero joint kernel or a coordinate axis. This argument adds no root-rank supply assumption and explicitly leaves graphs without invertible edges outside its conclusion.

## Independence and evidence limits

I independently derived the source pair-factorization and anchor extraction and adversarially checked the cofactor worker's rewritten one-anchor closure, specifically every place where the previous proof used binary dimensions. This is a mathematical reconstruction across distinct proof steps, not a blind independent discovery or a claim that finite checks prove the theorem. The final proof is analytic; no computational certificate or Lean result is asserted.

No mathematical HOLD, generic-to-pointwise gap, kernel-dimension inflation, circular consumer invocation, or scope drift was found. No tracked files were edited, no computation/background process was launched, and no process remains owned by this reviewer. This receipt is the sole final-review artifact. Further mathematical changes require review against a new hash.

## Final status/navigation addendum

2026-09-04. PASS remains in force for the final owning-document hash:

  dd42552e58ae7ac3aa9efcf4144bf5d8f8ea8c333e36853d8915b4b3efb47479

Read the final diff against the already reviewed mathematical body and rechecked the necessary-boundary corollary. The intervening changes promote the reviewed candidate status to proved analytic exclusion/necessary boundary, replace conditional acceptance wording, add reviewed navigation, and explicitly state that the older replay corroborates shared identities rather than proving the new supply implication. No mathematical hypothesis, conclusion, proof step, quantifier, or kernel-space dimension changed from the preceding PASS.

Also reviewed the new N8R2K node, its frontier table entry, dependency arrows, relationship-table rows, and the dated parent strategy's synthesis delta. They correctly state n=8/max-r=2, restrict the edge conclusion to invertible physical edges, require a zero or coordinate-axis joint kernel somewhere outside each such edge, and leave both residual kernel types, absence of invertible edges/lower root ranks, general incidences, and the global parent open. The N8R2C dependency is only the orientation exception after its complete incidence premise has been derived. No arrow or prose claims that maximum-root geometry itself supplies the new source implication.

The strategy's exact off-source construction is explicitly not a witness and not a dependency of N8R2K. Its displayed labels, root diagonal scaling, pure/mixed coefficient claims, and structural scope were checked against the existing pair-exchange worker's written exact bounded-replay receipt; I did not rerun that computation. The strategy correctly uses it to expose the remaining zero-joint-kernel obstacle, not to refute the full-source parent.

Final disposition: PASS for the status-only owner update and proof-topology integration. No tracked files edited, no new research lane opened, no computation launched, and no process left running.
