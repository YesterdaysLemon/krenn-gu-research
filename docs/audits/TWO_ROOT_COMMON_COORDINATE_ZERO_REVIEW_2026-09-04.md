# Fresh independent audit: zero-root-block analytic reduction

2026-09-04. Reviewer: independent Astra-high subagent
`lab_r2_consolidation_review`. Analytic reduction audit for the
[zero-block proof](../../claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md).
The separate [encoding and certificate audit](TWO_ROOT_ZERO_SOURCE_CERTIFICATE_REVIEW_2026-09-04.md)
owns the computational leaf. Global Krenn--Gu remains **UNRESOLVED**.

## Disposition

PASS for the analytic reduction of Q=0 to the pure-(3,3) full-cofactor system with every cross block of rank at most one. The non-pure-(3,3) branches are exhausted and excluded by the reasoning below, without assuming the inactive outside hafnian H is initially zero.

HOLD for any claim that this audit alone closes Q=0. The remaining pure-(3,3) rank-at-most-one full-cofactor system requires its independent exact support-encoding implication and accepted unsatisfiability certificate/checker. I did not audit that certificate, its clauses, or a solver log. A reported UNSAT without a native/accepted proof is not a completed proof leaf here.

That separately required gate subsequently received **PASS**: all 11,394
clauses were independently reconstructed, and all 6,860 binary branches and
6,861 conflict leaves were accepted by an exact checker. Together with this
analytic reduction, the separately reviewed certificate closes Q=0. This
paragraph does not convert the analytic reviewer into the certificate
reviewer; the linked audit supplies that distinct evidence.

Inputs read:

- tmp/lab-r2-zero-Q-checkpoint.md, SHA256 2308695985f0f557696ff3920da0cce9ecb0853362cba0637adc1001f92f3917.
- tmp/lab-r2-zero-Q-geometry-review.md, SHA256 daf47151d54508891f987cff6fb6bb1b39c3f7fcbdad5e8de0b60fe9d926e079.
- The merged rank-at-least-two owning theorem at commit 73955ca0, checked directly with git show, for the exact re-rooting consumer.

This audit independently reconstructs the port cover, the retained H!=0 cases, their matching identities, and the P2/re-rooting bridge. Earlier high-rank localization observations in the checkpoint are superseded by re-rooting and are not needed as proof dependencies.

## 1. Correct source supply and the unrestricted inactive H

The original open-root identity with Q=0 is the sum over the two distinct outside root partners. Setting every outside vector to e_c forces at least two ports of label c, since otherwise the root source is zero while its target is E_cc. Hence six ports form three pairs.

Same-pair activation has no hQ term and directly gives K_c=delta_c E_cc, delta_c!=0, and its nonzero pure inactive four-cofactor f_c. Cross-pair activation gives C_uv=0 when K_uv!=0. Define F to contain CROSS zero channels only. Every port has a nonzero leg.

Setting all ports inactive is 0=0, not H=0. For the actual inactive edge polynomials the stress is

  H=t_c+sum_{F incident at u} A_e C_e,
  t_c=A_{B_c} f_c.

The t_c have disjoint monomial supports, but H is not initially constrained to vanish. Every use below respects this distinction.

## 2. Port geometry and at most one both-leg edge

From K_c=[a_u,a_v]J[b_u,b_v]^T=delta_c E_cc, at least one factor has rank one and image e_c. Thus a both-leg port has at least one of its two nonzero legs on its OWN coordinate axis. A pure port has its unique nonzero leg on that axis as well, directly from its same-pair source.

Pure A-only and B-only ports form separate cliques, each at most one per group and of size at most three. They have no F edges to a both-leg port or to each other, because such a channel is a nonzero outer product.

A both-leg zero-channel component has two common projective directions a,b. Three distinct groups cannot occur because each requires its own distinct coordinate axis among those two directions. If a group is doubled, its same-side nonzero K_c has both directions e_c, excluding all other groups and hence any connecting cross edge. Therefore every nontrivial both-leg component is one edge between distinct groups c,d, with common directions e_c,e_d in one order.

There cannot be two such edges globally. They necessarily share a natural group. For two edges between the same groups c,d, the two c ports either have the same orientation, producing an off-diagonal rank-one same-pair channel, or opposite orientations, producing nonzero E_cc and E_dd terms; neither equals delta_c E_cc. For edges between c,d and c,e, the two c ports either give a nonzero row/column combination on the other two axes or give E_cc plus a nonzero off-diagonal E_de/E_ed term. Again pure E_cc is impossible. All coefficients used in these terms are nonzero because these are both-leg ports. This exhausts the possible two-edge patterns on three groups.

## 3. Exhaustive stress-pattern cover

Let a,b be the sizes of the pure A-only and B-only cliques, and swap the two root names if needed so a>=b. A clique of size one is an isolated port. Both-leg ports are isolated except for at most one edge. An isolated port of group c gives H=t_c. Two isolated groups force H=0 by disjoint supports. An isolated two-vertex F component between groups c,d gives t_c=t_d, hence t_c=t_d=0 by disjoint supports, but allows H=A_e C_e.

The complete cover is:

- If a<=1, there are at least four isolated ports, since the only possible nontrivial F component is one both-leg edge. They occupy at least two groups, so H=0.
- If a=3, one A-only port occurs in every group. Each partner has b on its own axis and nonzero. Two both-leg partners therefore have different b directions and cannot form a zero channel. Thus the 3-b partners outside the B clique are isolated. For b<=1, two distinct groups are isolated and H=0. The only retained possibilities are (3,2) and (3,3).
- If a=2, put its vertices in groups c,d. Their pure edge gives t_c=t_d=0. If H!=0, the other port of each group c,d must be nonisolated. These partners have nonzero b along their own distinct axes, so two both-leg partners cannot be connected by a zero edge. If both partners are B-only, b=2 and the two remaining ports lie in the third group and are isolated: this is the aligned (2,2) pattern. If exactly one partner is B-only, it must have a second B-only neighbour to avoid isolation, so b=2 and that neighbour lies in the third group; the other both-leg partner must join the remaining both-leg third-group port. This is a perfect matching of three F edges. If neither partner is B-only, both would have to lie on the same unique both-leg edge, which was just shown impossible. No other H!=0 case survives.

Thus H=0, (3,2), aligned (2,2), F perfect matching, and pure (3,3) exhaust all source-compatible possibilities. A mere count of graph edges would not suffice; the distinct own-axis b directions of partners of pure A ports are load-bearing in this cover.

When H=0, the already audited algebraic stress/pure-triangle/tripartite closure applies using the freshly established f_c and F-component bounds. This is reuse of its conditional polynomial argument, NOT an application of a nonzero-Q theorem by modifying Q. No statement about the full outside tensor H_B is inferred.

## 4. (3,2) and aligned (2,2) with H=t_2!=0

Relabel the retained group as 2. Let p_i=A_{A_j A_k}, q_i=A_{B_j B_k}, and X_ij=A_{A_i B_j}. In either retained pattern, t_0=t_1=0 and H=t_2. Hence X00=X11=0 by f_0,f_1!=0.

The pure A0-A1 and B0-B1 physical edges are nonzero matrix monomials by maximum r=2. Their inactive restrictions p_2,q_2 may a priori be zero, but their stresses are p_2 C_{A0 A1}=q_2 C_{B0 B1}=H, so H!=0 makes both nonzero. They divide t_2=X22 f_2, so they use colour 2 at all their endpoints. Thus p_2 q_2=eta f_2 for eta!=0.

I independently expanded the seven displayed four-vertex matching identities:

  f_2=p_2 q_2+X01 X10,
  p_2 X20=-p_1 X10,
  p_2 X21=-p_0 X01,
  p_2 q_0=-X01 X12,
  p_2 q_1=-X10 X02,
  f_0=p_0 q_0+X12 X21,
  f_1=p_1 q_1+X02 X20.

The four vanishing cofactors here delete respectively (B1,B2), (B0,B2), (A2,B0), and (A2,B1). Their root channels are nonzero in both patterns, including when A2 and B2 are both-leg ports. Multiplication and substitution give

  p_2 f_0=-2 p_0 X01 X12,
  p_2 f_1=-2 p_1 X10 X02.

Their left sides are nonzero, forcing X01 X10!=0. Therefore X01 X10=(1-eta)f_2 is a nonzero pure colour-2 product. UFD and endpoint multidegrees force X01 to carry colour 2 at B1. But p_2 f_0 has colour 0 at B1, and p_0,X12 omit B1. Independent coordinates 0 and 2 on the B1 inactive plane give a contradiction. No cancellation by an unproved nonzero factor or assumption H=0 is used.

The alternate aligned-(2,2) argument is also sound: retain its possibly nonzero group-2 internal edge, note C_Y and C_Z remove a group-2 port and hence cannot use that edge, and apply their zero product identities with nonzero pure permanents. The common factor rank-one/UFD argument contradicts a zero cofactor block without setting the retained internal edge or H to zero.

## 5. Perfect matching of three F edges

Each edge's two vertex stresses give equal t values of different groups, hence zero t values. All three internal physical edges therefore vanish. This does NOT give H=0 and the proof does not require it.

A perfect matching on three two-vertex groups, with no within-group edge, has exactly one edge of each cross-group type. Therefore each of C_X,C_Y,C_Z is supported in at most one position. Their pure physical permanents are nonzero.

If X were invertible over the inactive-variable fraction field, the product formulas for C_Y and C_Z would force Z and Y to have rank at most one, hence exactly one. A rank-one block with nonzero permanent has all four entries nonzero. Writing Z=r s^T, both coordinates of s are nonzero. Multiplication by invertible JXJ leaves a nonzero left factor, so C_Y has at least two nonzero entries, contradicting its support bound one. Thus X is not invertible; similarly Y and Z are not. Their nonzero permanents give rank one each, and pure-permanent UFD factorization makes every cross-cofactor entry nonzero by the independent shared-plane monomials. This again contradicts the support bound.

This closes the perfect-matching branch without using H=0 or edgewise orthogonality that stress did not provide.

## 6. Pure (3,3): full source identities

Here B_i={A_i,B_i} with A_i attached only to root 1 and B_i only to root 2. The same-pair source forces their surviving vectors to be nonzero multiples of e_i. Their scalar constants may be retained explicitly or absorbed into f_i; no modification of the actual GHZ tensor is needed.

The full root-source (i,j) entry is a nonzero constant times z_{Ai}[i] z_{Bj}[j] C_{Ai Bj}(z). For i!=j its target is zero, so C_{Ai Bj}=0 as a polynomial on all remaining THREE-dimensional port spaces. For i=j it gives the nonzero pure full cofactor f_i. Polynomial cancellation here is by nonzero coordinate polynomials, not by a numerical point value.

Every FULL physical AA and BB edge is a nonzero matrix monomial by the opposite root's identically zero orientation legs and global maximum r=2. Thus, for complementary AA/BB edges p_i,q_j,

  per_2 X[delete i,delete j]=-p_i q_j  (i!=j),
  per_2 X[delete i,delete i]=f_i-p_i q_i.

The six off-diagonal targets are nonzero decomposable tensors on full independent port spaces. Inactive restrictions could vanish, but these FULL target monomials cannot. This distinction is essential to subsequent support constraints.

## 7. General P2 anchor lemma, including rank-one and zero cases

For a nonzero pure identity

  f(A,B)g(C,D)+h(A,D)l(C,B)
     =alpha(A) beta(C) gamma(B) delta(D),

at least one whole row is anchored to its target covector: either f,h have the alpha factor at A, or g,l have the beta factor at C. The column version follows by swapping modes.

Independent proof: if the first row is not entirely alpha-anchored, choose a in ker alpha where one of f(a,-),h(a,-) is nonzero, exchanging the two terms if needed so f_a!=0. If h_a=0, restriction forces g=0; the original nonzero product h*l equals the target and forces l to have the beta factor, while zero g has it trivially. If h_a!=0, the crossed-product identity f_a(B)g(C,D)=-h_a(D)l(C,B) forces g=b(C)h_a(D), l=-b(C)f_a(B) by independent-variable factorization. The nonzero full target makes b nonzero and proportional to beta. Thus the opposite row is anchored.

This does not require rank f>=2: it requires only that some first-row edge lack the alpha factor. Rank>=2 is a sufficient special case. Consequently the FULL row/column support disjunction used by the support relaxation is valid even after all X blocks are rank one or zero. Zero edges satisfy factor containment and were explicitly covered.

## 8. Re-rooting exclusion of every rank-at-least-two X block

Suppose Xij has rank at least two and choose new roots A_i,B_j. For each other A_k, choose a B_l so the row-label set {i,k} differs from the column-label set {j,l}; among the two available l choices at most one is forbidden. The corresponding off-diagonal permanent is the nonzero monomial -p_m q_n. Its row anchor cannot be at A_i, because that would make the rank-at-least-two block Xij factor through one covector. Therefore both edges at A_k factor through precisely the coordinate factor of the AA edge A_i-A_k at A_k. This establishes common-coordinate physical incidences from both new roots to every other A port, including zero X_kj.

The symmetric column argument gives the same property at every other B port. At old root 1, the A_i incidence uses outside coordinate i and the B_j incidence is zero; at old root 2, the incidences are zero and coordinate j. Thus all six outsiders have the exact physical common-coordinate form required by the merged rank-at-least-two theorem at 73955ca0.

The new root block itself has a torus zero: a bilinear form of rank at least two cannot be a Laurent unit, since a bilinear Laurent unit is a rank-one matrix monomial. Its torus zero provides a fully supported zero-coupled pair, and unchanged global maximum r=2 makes that pair maximum. This is re-rooting the SAME graph, not adding or replacing any physical edge. All hypotheses of the merged theorem hold, contradiction.

Hence every Xij in the remaining pure-(3,3) system has rank at most one. A nonzero rank-one physical matrix has rectangular nonzero support, and the preceding full P2 anchor disjunctions supply additional necessary support constraints. I have not audited their particular Boolean encoding here.

## 9. Precisely remaining obligation

Only the pure-(3,3) FULL cofactor system remains: AA/BB edges are full nonzero matrix monomials; all nine cross blocks are rank one or zero; the six off-diagonal full cofactors vanish with their corresponding nonzero monomial permanent targets; the three diagonal full cofactors are nonzero pure f_i; and all general P2 row/column anchor disjunctions hold. The support-certificate workers must prove that their encoded finite family is a necessary relaxation of these exact tensor conditions, with exhaustive coordinate/support handling, and supply an accepted exact UNSAT certificate and sound independent checker.

No part of this reduction proves full H_B(z)=0. Inactive H=0, where it occurs, only licenses the conditional inactive algebraic contradiction. It does not permit adding a root edge. The re-rooting argument above is valid precisely because it alters no graph tensor.

Final recommendation: accept the analytic reduction with the explicit exhaustive port cover and general P2 anchor proof above. Keep whole-Q=0 closure on HOLD pending the separate certificate/encoding reviews. No original-witness candidate, tracked edit, computation, or owned running process was produced by this audit.
