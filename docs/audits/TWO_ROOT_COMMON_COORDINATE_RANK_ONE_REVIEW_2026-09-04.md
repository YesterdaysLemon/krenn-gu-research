# Fresh independent audit: nonzero rank-one root blocks

2026-09-04. Reviewer: independent Astra-high subagent
`lab_r2_consolidation_review`. Separate adversarial analytic review of the
[rank-one proof](../../claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_RANK_ONE_EXCLUSION.md).
The prior rank-at-least-two theorem is retained separately. Global
Krenn--Gu remains **UNRESOLVED**.

## Verdict and exact scope

PASS for BOTH proposed rank-one nonmonomial branches, hence for every nonzero rank-one root block that is not a matrix monomial, under the physical common-coordinate eight-vertex hypotheses and global maximum torus-root cardinality two.

The branches are: (i) Q=p q^T with neither factor proportional to a coordinate vector; and (ii) exactly one factor coordinate, reduced by root transposition and scalar absorption to p=e_t with q nonzero and noncoordinate. They exhaust rank-one nonmonomial blocks. If both factors are coordinate, Q is a nonzero matrix monomial and has no torus zero, so it cannot be the physical edge of the selected zero-coupled maximum root pair. Q=0 is not covered here; in particular H=0 is NOT asserted when Q=0. General incidence, higher order, and the global parent remain outside scope.

Read and pinned candidate inputs:

- tmp/lab-r2-rankone-root-two-noncoordinate-review.md: SHA256 34b98095be61ac92460e37e9dc88359fcbd04397e966ea1569c5c6957bd5c8fb.
- tmp/lab-r2-onecoordinate-root.md: SHA256 4225256dac2bd679f9fd9a8fbb731a1fd7082a7cb278efb192236b71c3b88e87.
- tmp/lab-r2-rankone-root-onecoordinate-review.md: SHA256 a05a6b32a4bd83b98f9f3b3b50970f191fed828949ac0657dac898c29cde6ff4.

This is an adversarial reconstruction of their mathematical claims, including an independent check of every class transition and central/zero-leg neighbour case. It is not a blind discovery, Lean verification, or merely agreement with another review's verdict. No computation or background process was needed or launched.

## 1. Source supply without a rank-at-least-two assumption

For these nonmonomial Q, Q is not proportional to any E_cc. If at most one outside port has assigned label c, setting all six outside vectors to e_c leaves no matching using two distinct outside root partners. The original open-root source becomes h_c Q=E_cc, impossible by NONPROPORTIONALITY, not by a rank-two comparison. Thus each label occurs twice.

Same-pair activation gives h_c Q+f_c K_c=p_c E_cc. If K_c were zero or proportional to Q, the nonzero pure target would again force Q proportional to E_cc. Hence Q,K_c are independent and the same constant matrix-span argument yields

  K_c=gamma_c Q+delta_c E_cc, delta_c!=0,
  f_c=delta_c^(-1) product_{w outside B_c} z_w[c]!=0.

All-inactive source gives H Q=0 and therefore H=0 because Q is NONZERO. The field of formal inactive variables is used only for polynomial identities and their ranks; no physical coefficient specialization is discarded. Cross activation gives C_uv=0 unless K_uv belongs to C Q. Define F by this latter proportionality condition on CROSS-group pairs, including zero. A port with both legs zero is excluded by K_c!=0.

## 2. General rank-one dependent-channel fact

For K_uv=[a_u,a_v] J [b_u,b_v]^T, both 3-by-2 factors having rank two would force K_uv to have rank two, since the first factor is injective and the second transpose surjective. Therefore a nonzero dependent K_uv=lambda p q^T has at least one factor of rank one. On the a side its image must be C p; on the b side it must be C q. Thus both endpoints belong to A={a in C p} or both belong to B={b in C q}, where ZERO IS INCLUDED in either line-membership condition.

This fact is valid with zero individual columns, but it does not alone classify zero channels. Zero channels between both-nonzero ports give proportional a directions and proportional b directions by rank-one cancellation. Pure-port cases must be checked separately, as done below.

## 3. Both factors noncoordinate

Because neither p nor q is a coordinate vector, [e_c] is nonzero in both quotients C^3/Cp and C^3/Cq for every c. Projecting the same-pair source to their tensor product gives a nonzero delta_c[e_c] tensor [e_c]. A central port in A intersect B would make both projected summands zero. Two A ports or two B ports in one group would likewise kill the target. Therefore A intersect B is empty and each group has at most one A member and one B member.

A pure A-only port has b=0, hence belongs to B, not A, so its nonzero a is outside C p. Its channel with any port is a b_v^T, and belongs to C Q only when b_v=0. Thus its component is exactly the pure A-only clique, of order at most three. The B-only case is the transpose. This explicitly separates every zero leg before quotient normalization.

For remaining A ports, a_u=alpha_u p with alpha_u!=0 and b_u outside C q. The nonzero quotient vector w_u=[b_u]/alpha_u is defined legitimately. Dependence between two such ports is exactly w_u=-w_v. Their connected components are complete bipartite and have at most one port from each group, hence at most three vertices. A nonzero dependent edge stays in A by the general rank-one fact and A intersect B being empty. A zero edge between both ports stays in A by proportional a directions. No edge to a separated pure port is missed. The B quotient argument is symmetric.

Remaining D ports belong to neither A nor B and have both legs nonzero. They have only zero exceptional channels, staying within D. Their common-projective-direction components are complete bipartite with each group on one side. If a component contains both ports of group c, their same-pair channel is nonzero rank one. Here gamma_c!=0 would give rank two because p,e_c and q,e_c are each independent. Thus gamma_c=0 and the common a,b directions are e_c. Another group d then has K_d supported only in row c or column c. Rank-one delta_d E_dd is impossible, so gamma_d!=0. Deleting row and column c from the source makes the same Q submatrix a nonzero E_dd multiple. A third group would demand a different diagonal-unit multiple, impossible; two d ports would give rank-one E_cc rather than their required E_dd. Hence this component also has at most three vertices.

This checks the entire two-noncoordinate cover, including pure ports that lie in A or B through a zero vector.

## 4. Exactly one coordinate factor: projection facts

Set p=e_t and q noncoordinate. Let A={a in Cp}, B={b in Cq}, C=A intersect B, and D the complement of A union B, again including zero in line membership. A-only/B-only refer instead to physical zero-leg orientations and must not be confused with the A/B membership classes.

For a good group c!=t, both quotient target factors remain nonzero. There is no central member and at most one A and one B member. One-sided projections give stronger exact statements:

- If a_u is in Cp, projecting only on the left leaves [a_partner] tensor b_u=delta_c[e_c] tensor e_c. Thus b_u is a NONZERO multiple of e_c, even if a_u=0.
- If b_u is in Cq, projecting only on the right gives a_u tensor [b_partner]=delta_c e_c tensor [e_c]. Thus a_u is a NONZERO multiple of e_c, even if b_u=0.

The special channel is K_t=p(gamma_t q+delta_t p)^T. Its row is nonzero and outside Cq because delta_t!=0 and q,p are independent; gamma_t is not assumed zero. If b_u is in Cq in this group, right projection gives a_u tensor [b_partner]=delta_t p tensor [p], a nonzero target. Thus a_u is a NONZERO multiple of p. Every special-group B member is therefore central. There can be at most one central port, since two would make K_t proportional to Q. In particular a central port with a=0 is impossible.

## 5. Exact central and zero-leg neighbour audit

Let a central port z have a_z=alpha p, alpha!=0, b_z=beta q.

If beta!=0, z is F-isolated. A noncentral A member gives a surviving nonzero term alpha p[b_v]^T modulo q. A noncentral B member gives a surviving nonzero term beta[a_v]q^T modulo p. A D member cannot give a nonzero dependent edge by the rank-one factor fact; a zero edge would force it into both A and B by projective proportionality. A separated pure port is covered by the same one-sided calculation. There is no other central member. Thus neither zero nor nonzero dependent neighbours remain.

If beta=0, K_zv=alpha p b_v^T is dependent exactly when b_v is in Cq. Thus its neighbours are precisely the B members from the two good groups, at most one each; the special partner cannot belong to B. For good B members u in group c and v in group d, write a_u=eta_c e_c, a_v=eta_d e_d with eta_c,eta_d nonzero and b_u=beta_c q,b_v=beta_d q. Then

  K_uv=(eta_c beta_d e_c+eta_d beta_c e_d) q^T.

The span of the two good coordinate axes excludes p=e_t. Consequently dependence on Q forces that column to be zero, which means beta_c=beta_d=0. The hub component is therefore an isolated vertex, edge, two-edge star, or three-vertex pure A-only triangle. No mixed triangle survives.

Noncentral B members occur only in the two good groups. Their only possible neighbours outside those members are the preceding central b=0 hub. This follows from the nonzero-dependent factor fact and, for zero channels, projective preservation when both legs are nonzero. If the B member itself has b=0, K=a_u b_v^T with a_u on a good axis rather than p, so dependence requires b_v=0; these are exactly the same B members/hub. Thus zero legs introduce no extra connection to A or D.

An A member with a=0 is a pure B-only port with b outside Cq. Its channel with any other port is a_v b^T. Dependence requires a_v=0, because the nonzero row is outside Cq. Therefore all such ports form their separate pure B-only clique, with at most one per group and at most three total. They do not link to a nonzero-a A member, any central member, or any other class.

These checks cover every potential central/zero-leg bridge rather than relying solely on the both-port cancellation argument.

## 6. Noncentral A quotient components

For the remaining A members, a_u=alpha_u p with alpha_u!=0 and b_u outside Cq. The legitimate nonzero quotient vectors w_u=[b_u]/alpha_u have dependence exactly w_v=-w_u. Components are complete bipartite; a natural group cannot occupy both sides because its K_c is not proportional to Q.

There is at most one A member from either good group. Hence a component with more than three vertices must contain both special-group ports and one from each good group. The two special ports lie on the same side, so share w, and projecting their source modulo q gives

  2 alpha_u alpha_v w=delta_t[p].

Thus w is a nonzero multiple of [p]. A good-group c member has b_u a nonzero e_c multiple, so its quotient being proportional to w forces [e_c] proportional to [p], or q in span(p,e_c). Both good groups would force q into the intersection of two distinct coordinate planes, namely Cp, contrary to q being noncoordinate. Hence each component has order at most three. This includes support(q)=2 and support(q)=3 without treating either as generic.

There are no overlooked outgoing edges: a nonzero dependent edge must remain in A unless the port also belongs to B, which was excluded; a zero both-port edge preserves its a direction; the separated pure and central cases were checked above.

## 7. D components and exceptional special-channel rank

A D port has both legs nonzero, neither a in Cp nor b in Cq. It has only zero exceptional links, which stay in D by projective preservation. Components are complete bipartite with each group on one side.

If both ports of group t lay in one such component, its common a direction would be the column of its nonzero rank-one K_t, namely p, contrary to D. Thus only a good group c can be doubled. For such c, gamma_c!=0 makes K_c rank two, so a doubled pair's rank-one channel forces gamma_c=0 and common a,b directions e_c.

A member from the other good group d would make K_d supported in row c or column c, giving (K_d)_{dd}=0. Its source has (gamma_d p q^T+delta_d E_dd)_{dd}=delta_d!=0 because p_d=0. This contradiction is independent of gamma_d. At most one special-group t member can occur, since two would give K_t column e_c rather than p. Therefore these components too have order at most three.

The proof never replaces K_t by a coordinate matrix unit and retains its full gamma_t q+delta_t p row throughout.

## 8. Inherited physical contradiction and publication boundaries

Both branches supply exactly the downstream hypotheses already independently audited: H=0; nonzero pure same-pair cofactors; cross-cofactor support contained in F; every component of F of order at most three; bipartite components with nonzero signed group counts; and only pure orientation triangles.

The disjoint-monomial signed stresses kill every internal edge-cofactor product except the two pure triangles. Global maximum r=2 forces the AA/BB physical monomials there using zero orientation legs only; the pure-cofactor four-hafnian flattening kills that exception without root-axis purity. All internal restricted edges then vanish, and component incidence gives full edgewise orthogonality. The tripartite pure-permanent rank/UFD/cofactor and complementary-six-cycle contradiction requires no rank assumption on Q after this supply. Thus no unreplaced rank-at-least-two premise remains in the inherited endpoint.

For integration, preserve the separate line-membership and pure-orientation terminology; explicitly include zero in A/B before separating pure cases; keep the exceptional K_t row; use nonproportionality rather than rank>=2 for source labels and same-pair independence; and state Q!=0 for H=0. The nonzero matrix-monomial exclusion depends on choosing a genuine fully supported zero-coupled root pair. Q=0 needs a different proof and must not be imported by a continuity or genericity argument.

Final recommendation: accept these two analytic rank-one nonmonomial exclusions for a subsequent scoped integration, subject to a final exact-text review. No mathematical HOLD found. No original-witness candidate, computational proof claim, tracked edit, or owned running process.
