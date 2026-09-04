# Eight-vertex zero-root-block common-coordinate exclusion

## Status, scope, and dependencies

**Exact finite exclusion over C, with an independently checked finite Boolean certificate as one proof leaf.** Suppose a ternary physical block graph W on eight vertices satisfies the complete GHZ identity T_W=Delta_(8,3), has maximum fully supported pairwise-zero torus-root cardinality exactly two, and has named roots 1,2 with W_12=0. Assume that at each of the six outside vertices u BOTH physical root incidences use one common outside coordinate:

    W_1u(-,z_u)=a_u z_u[c(u)],
    W_2u(-,z_u)=b_u z_u[c(u)].                       (1)

The constant root covectors a_u,b_u may individually vanish. The hypothesis is about complete physical blocks, not their values at selected root vectors.

**Theorem.** These hypotheses are inconsistent.

This is the zero-root-block boundary of the common-coordinate eight-vertex child. It does not supply common-coordinate incidences for general graphs, prove an exhaustive eight-vertex exclusion, or resolve the global conjecture. Global Krenn--Gu remains **UNRESOLVED**. No Lean formalization is asserted.

The proof uses the accepted
[rank-at-least-two theorem](TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md),
at commit 73955ca0 (merged PR340), only after exact re-rooting of the SAME
graph. The zero-hafnian polynomial argument below is reproduced explicitly
and does not apply a nonzero-root theorem at Q=0. The final support leaf is
the [self-contained certificate package](two-root-zero-source-certificate/README.md);
its bridge, frozen hashes, and independent acceptance are specified in
Section 8.

The [analytic reduction review](../../../docs/audits/TWO_ROOT_COMMON_COORDINATE_ZERO_REVIEW_2026-09-04.md)
and [independent encoding/certificate review](../../../docs/audits/TWO_ROOT_ZERO_SOURCE_CERTIFICATE_REVIEW_2026-09-04.md)
serve different purposes. The
[package review](../../../docs/audits/TWO_ROOT_ZERO_SOURCE_PACKAGE_REVIEW_2026-09-04.md)
checks portable integration and exact bytes. The proof below uses the
re-rooting implication directly, without a high-rank support census.

## 1. Full source, labels, and inactive physical cofactors

Let B be the outside six-set, H_B its physical matching tensor, and C_uv=H_(B-{u,v}) its physical four-vertex cofactors. Put

    K_uv=a_u b_v^T+a_v b_u^T.

Partitioning a matching by its two outside root partners gives the exact matrix-valued polynomial identity

    sum_(u<v) z_u[c(u)] z_v[c(v)] C_uv(z) K_uv
       =diag(prod_w z_w[0], prod_w z_w[1], prod_w z_w[2]).       (2)

There is NO H_B Q term because Q=0. In particular, setting every port inactive gives 0=0 and supplies no conclusion about H_B.

For a colour c set all six outside vectors to e_c. Fewer than two ports labelled c would kill every source term, whereas the target is E_cc. Hence every label occurs at least twice and the six ports form three pairs B_0,B_1,B_2. Provisional labels at a both-zero port cause no problem: the same-pair identity below excludes that possibility.

At u in B_c define its inactive plane L_u=ker e_c^*. Let S be the polynomial ring in the twelve independent coordinates on these six binary planes. Restrict every actual outside block to L_u x L_v and call the resulting edge polynomial A_uv. Its hafnian H=haf(A) and four-cofactors C_uv are still principal hafnians of the SAME restricted physical graph. They are not freely chosen arrays.

Activate only the pair B_c by setting both its vectors to e_c, leaving the other four inactive. Then (2) reads

    f_c K_c=P_c E_cc,
    K_c=K_(B_c),
    P_c=prod_(w outside B_c) z_w[c]!=0.

Therefore

    K_c=delta_c E_cc,
    f_c=C_(B_c)=kappa_c P_c,
    delta_c!=0, kappa_c=delta_c^(-1)!=0.              (3)

Every port consequently has a nonzero leg. Activating instead a cross-group pair u,v leaves at least one inactive port of every colour, so the target is zero. Hence

    C_uv=0 whenever K_uv!=0.                         (4)

Here and until Section 6, these are identities on the inactive complement planes.

Define F to contain exactly the CROSS-group pairs with K_uv=0. Put

    t_c=A_(B_c) f_c,
    t_uv=A_uv C_uv for uv in F.

The partner expansion of the physical six-hafnian at u in B_c is

    H=t_c+sum_(v:uv in F) t_uv.                      (5)

H remains unrestricted. The monomial supports of t_c and t_d are disjoint for c!=d: on the two vertices of the third group k, t_c has the fixed colour-c product and t_d the fixed colour-d product, and their unknown internal-edge factors omit those two vertices.

## 2. Exact zero-channel graph

A port is A-only if a!=0,b=0, B-only if a=0,b!=0, and both-leg otherwise. From

    [a_u,a_v] J [b_u,b_v]^T=delta_c E_cc,
    J=[[0,1],[1,0]], {u,v}=B_c,

at least one of the two factors has rank one with image e_c. Thus every both-leg port has at least one leg on its OWN coordinate axis. A pure port's unique nonzero leg is also on that axis, directly from (3).

A-only ports form one zero-channel clique, and B-only ports another. Each has at most one vertex per natural group, hence at most three vertices. A pure port has no F edge to a both-leg port or to the opposite pure type: that channel is a nonzero outer product.

Along a zero channel between two both-leg ports, the a directions are proportional and the b directions are proportional. A connected component has two common projective directions a,b. Three represented natural groups would require three distinct axes among those two directions, impossible. If a natural group were doubled within such a component, its nonzero same-pair channel would force both common directions to its own axis, excluding every other group. Thus each nontrivial both-leg component is a SINGLE edge between distinct groups c,d, and its two common directions are e_c,e_d in one order.

There is at most one both-leg F edge globally. Two such edges necessarily share a natural group c. If both join c,d, the two c ports either have the same orientation, producing an off-diagonal rank-one same-pair channel, or opposite orientations, producing nonzero E_cc and E_dd terms; neither is delta_c E_cc. If the edges join c,d and c,e, the same-orientation case produces a nonzero combination on the other two axes, while the opposite-orientation case produces E_cc and a nonzero off-diagonal E_de or E_ed term. All coefficients are nonzero for both-leg ports. These cases exhaust two edges on three groups.

Thus F consists of two disjoint pure cliques of sizes at most three, isolated ports, and at most one both-leg edge. In particular all F components have at most three vertices.

## 3. Exhaustive stress-pattern cover

Let a,b be the numbers of A-only and B-only ports and interchange root names so a>=b. A clique of size one is an isolated vertex. An isolated port of group c gives H=t_c. Isolated ports in two different groups force H=0 by disjoint supports. The two endpoint equations of an isolated F edge between groups c,d give t_c=t_d, hence both zero, although H=t_uv may remain nonzero.

The following cover is exhaustive.

- If a<=1, at least four ports are isolated because at most one both-leg edge is available. They occupy at least two groups, so H=0.
- If a=3, there is one A-only port in every group. Each partner has its nonzero b leg on its own axis. Two both-leg partners have different b directions and cannot form a zero channel. Thus the 3-b partners outside the B clique are isolated. For b<=1, two different groups are isolated and H=0. Only (a,b)=(3,2) and (3,3) remain.
- If a=2, put the A clique in groups c,d. Its edge gives t_c=t_d=0. If H!=0, the other port of each of those groups must be nonisolated. Their nonzero b legs lie on distinct own axes, so they cannot both be joined by a both-leg zero edge. If both partners are B-only, b=2 and both remaining ports lie in the third group and are isolated: the aligned (2,2) pattern. If exactly one partner is B-only, avoiding its isolation requires a second B-only port in the third group; the other both-leg partner must join the last third-group both-leg port. This is a perfect matching of three F edges. If neither partner is B-only, both would need the unique both-leg edge, already ruled out by their distinct b directions.

It therefore suffices to exclude H=0, (3,2), aligned (2,2), an F perfect matching, and pure (3,3). No full outside tensor H_B has been declared zero.

## 4. The H=0 case: conditional polynomial closure

This section proves the required inactive polynomial contradiction directly.

For an isolated vertex or F edge, the stresses (5) with H=0 force its represented t_c values to zero. Unless F consists of two pure triangles covering all six ports, every group has a vertex in such a component and all t_c vanish.

For the two-triangle exception write B_i={A_i,B_i}, with A_i A-only and B_i B-only. Every FULL physical AA edge is a nonzero matrix unit: a torus zero of that edge, together with old root 2 whose two incident legs vanish identically, would give three torus roots. A torus-zero-free bilinear Laurent polynomial over C is a unit, hence one nonzero coordinate monomial. The same argument applies to BB edges using root 1. Their inactive restrictions may be monomials OR zero.

Put p_k=A_(Ai,Aj), q_k=A_(Bi,Bj) when {i,j,k}={0,1,2}. Triangle incidence gives

    p_k C_(Ai,Aj)=q_k C_(Bi,Bj)=(-t_i-t_j+t_k)/2.     (6)

If t_k!=0, p_k is a nonzero monomial. Disjoint supports imply that it divides each nonzero summand on the right. Since t_k uses colour k at Ai,Aj, p_k uses k at both endpoints. But t_i uses colour i at Aj and t_j uses colour j at Ai; hence t_i=t_j=0. If p_k=0, disjoint supports in (6) instead kill all three terms.

Assume only t_k survives. For the other indices i,j, the nonzero f_j gives A_(Aj,Bj)=0. Equation (6) makes p_i,q_i nonzero monomials dividing t_k, so they use coordinate k at Aj and Bj respectively. The four-hafnian identity for f_i becomes

    A_(Aj,Bk) A_(Ak,Bj)=f_i-p_i q_i.                 (7)

Across (Aj,Bk)|(Ak,Bj), the left side has rank at most one. The right side is the difference of two nonzero decomposable tensors with independent factors on BOTH shores: f_i uses colour i at Aj,Bj, whereas p_i q_i uses colour k there. Its rank is two, contradiction. Hence all t_c vanish in every H=0 case.

Since f_c!=0, all three within-group edges A_(B_c) vanish. Remaining vertex equations kill every t_uv: leaf elimination on an edge and the nonsingular incidence matrix of a three-cycle suffice. Thus A_uv C_uv=0 on all cross edges, including those outside F by (4).

Write the tripartite 2-by-2 cross blocks as X,Y,Z between groups01,02,12. The exact physical identities are

    per X=kappa_2 prod_(u in B0 union B1) z_u[2],
    per Y=kappa_1 prod_(u in B0 union B2) z_u[1],
    per Z=kappa_0 prod_(u in B1 union B2) z_u[0],

    H=sum_(i,j,k) X_ij Y_(bar i,k) Z_(bar j,bar k)=0,
    C_X=J Y J Z^T J,
    C_Y=J X J Z J,
    C_Z=J X^T J Y J,                                (8)

where bar i=1-i. Rank calculations below are in the fraction field of S, not at a generic physical specialization.

If a cross block has rank one, det X=0 and per X!=0 give X00 X11=X01 X10=(per X)/2!=0. UFD and endpoint multidegrees force all four entries to be nonzero scalar multiples of their omitted-colour coordinate products. Two adjacent rank-one cross blocks then give every cofactor entry nonzero: its two terms have distinct monomials in the independent coordinates at the shared pair.

If all cross cofactors vanish, the nonzero permanents and (8) force all three blocks rank one, contradicting that observation. Otherwise take a nonzero cofactor in X. Its edge is zero by entrywise orthogonality, so det X=plus-or-minus per X!=0. A rank-one Y would have all entries nonzero, forcing C_Y=0 and then Z=0 by invertible X. Thus Y,Z also are invertible. All three cofactor blocks are invertible and their support has at least six edges. F has at most six edges, with equality only for two disjoint triangles. Therefore cofactor support is exactly those two triangles; its corresponding actual edges vanish. Nonzero permanents leave the complementary six-cycle. UFD makes each surviving edge a nonzero omitted-colour coordinate monomial. The cycle's two perfect matchings use different coordinates at each vertex and give distinct nonzero monomials, which cannot cancel. This contradicts H=0.

This finishes the H=0 case without applying a nonzero-Q theorem or changing W.

## 5. The retained nonzero-H stress cases

### (3,2) and aligned (2,2)

Relabel the retained group as 2, and name the ports A_i,B_i so the pure clique edges are A0-A1 and B0-B1. In both cases t0=t1=0 and H=t2!=0, so X00=X11=0, where Xij=A_(Ai,Bj). Write p_i,q_i for complementary A and B edges.

The full physical p2,q2 are matrix units by the same maximum-root argument as above. Their stresses equal H, so their inactive restrictions are nonzero and divide H=X22 f2. They therefore use colour2 at all their endpoints, giving p2 q2=eta f2 with eta!=0.

The actual four-hafnians and the four cofactors killed by nonzero root channels give

    f2=p2 q2+X01 X10,
    p2 X20=-p1 X10,
    p2 X21=-p0 X01,
    p2 q0=-X01 X12,
    p2 q1=-X10 X02,
    f0=p0 q0+X12 X21,
    f1=p1 q1+X02 X20.                               (9)

The vanishing cofactors delete (B1,B2), (B0,B2), (A2,B0), and (A2,B1). Their root channels are nonzero in both patterns, also when both A2,B2 are both-leg ports. Multiplying and substituting gives polynomial identities

    p2 f0=-2 p0 X01 X12,
    p2 f1=-2 p1 X10 X02.                            (10)

The left sides are nonzero. Hence X01 X10!=0 and the first equation of (9) makes this product a nonzero pure-colour2 tensor. UFD forces X01 to carry colour2 at B1. But p2 f0 carries colour0 there, and p0,X12 omit B1. The independent binary coordinates at B1 contradict (10). No division by an unproved nonzero quantity or assumption H=0 occurs.

### Perfect matching of three F edges

Each edge's endpoint stresses give equal t values from two different groups, hence zero values. All three internal edges therefore vanish, but H is not assumed zero. A cross-group perfect matching on three pairs has exactly one edge of each cross-group type. Thus C_X,C_Y,C_Z in (8) are each supported in at most one position, and their physical permanents remain nonzero.

If X were invertible, the product identities make Y,Z rank at most one, hence exactly one. Their nonzero permanents give all four entries nonzero. Multiplication by invertible JXJ preserves the full-support right factor of rank-one Z, so C_Y cannot be supported at one entry unless zero; zero would force Z=0. Contradiction. Thus none of X,Y,Z is invertible. All have rank one, and the pure-permanent factor argument from Section 4 makes every cross-cofactor entry nonzero, another contradiction.

Only pure (3,3) remains.

## 6. Pure (3,3): full ternary cofactor equations

There is now one A-only port Ai and one B-only port Bi per group i. Their same-pair channel is a nonzero multiple of Eii, so their surviving root vectors are nonzero multiples of e_i. Retain these constants or absorb them into the nonzero cofactor weights below; the actual graph and GHZ tensor need not be changed.

The (i,j) entry of the FULL source (2) is a nonzero constant times z_Ai[i] z_Bj[j] C_(Ai,Bj). Polynomial cancellation gives

    C_(Ai,Bj)=0 for i!=j,
    C_(Ai,Bi)=f_i=nonzero pure colour-i product       (11)

on the remaining FOUR FULL THREE-DIMENSIONAL port spaces. These are stronger than inactive restrictions. Nothing asserts the full outside hafnian H_B vanishes.

Maximum r=2 makes every FULL AA and BB physical block a nonzero matrix unit, by the torus-zero argument in Section 4. Put p_i=W_(Aj,Ak), q_j=W_(Bs,Bt) for complementary triangle edges and Xij=W_(Ai,Bj). Thus

    per_2 X[delete i,delete j]=-p_i q_j  for i!=j,
    per_2 X[delete i,delete i]=f_i-p_i q_i.           (12)

Every off-diagonal target in (12) is a nonzero coordinate monomial on four full independent local spaces. Its inactive restriction could be zero; we do not restrict it here.

## 7. P2 anchors and exact re-rooting

**Pure P2 anchor lemma.** If

    f(A,B)g(C,D)+h(A,D)l(C,B)
      =alpha(A) beta(C) gamma(B) delta(D)!=0,

then either both f,h have their A factor in span(alpha), or both g,l have their C factor in span(beta). The analogous column disjunction also holds. Zero edges satisfy factor containment.

Proof: if the first row is not wholly alpha-anchored, exchange terms if needed and choose a in ker alpha with f_a!=0. If h_a=0, restriction forces g=0; the original nonzero product h*l then forces l to have the beta factor. If h_a!=0, the crossed-product equality f_a(B)g(C,D)=-h_a(D)l(C,B) forces g=b(C)h_a(D), l=-b(C)f_a(B), up to reciprocal scalars. Substitution in the nonzero target makes b proportional to beta. The column statement follows by interchanging tensor roles. This proof applies to rank-one and zero edges, not only to a rank-at-least-two special case.

Suppose some physical Xij has rank at least two. Use Ai,Bj as new roots of the SAME graph. For each other Ak choose Bl with l!=j so {i,k}!={j,l}; of two available choices at most one is forbidden. The associated off-diagonal rectangle in (12) has nonzero pure target -p_m q_n. Its row anchor cannot be at Ai, since Xij has rank at least two. The opposite row therefore makes Xkj factor through exactly the coordinate at Ak of AA edge Ai-Ak. These two physical incidences from the new roots share one outside coordinate, including when Xkj=0.

The symmetric column argument supplies common-coordinate incidences at every other Bl, using the BB edge Bj-Bl. At old root1, the Ai incidence is Eii up to scale and the Bj incidence is zero; at old root2 they are zero and Ejj. Hence all six outsiders have the precise common-coordinate form of the accepted rank-at-least-two theorem.

The new root block Xij has a torus zero: a zero-free bilinear Laurent polynomial is a rank-one coordinate monomial, whereas rank Xij>=2. Its fully supported zero pair is maximum because the unchanged global maximum is two. All hypotheses of the accepted theorem at commit 73955ca0 hold, contradiction. Consequently

    rank Xij<=1 for all nine cross blocks.           (13)

No edge has been added or altered. No unaccepted rank-one-root theorem is needed.

## 8. Exact finite support leaf and mathematical bridge

It remains to exclude (11)--(13), with all six AA/BB blocks nonzero matrix
units. The accepted [certificate package](two-root-zero-source-certificate/README.md)
provides reproducible generation and independent checking.

Associate one Boolean variable with each of the nine coordinate entries on each of fifteen outside edges: true means that physical complex coefficient is nonzero. There are 135 such variables. Every actual hypothetical solution would satisfy the following finite necessary conditions.

1. Each of the six AA/BB blocks has exactly one true entry; all nine coordinate choices are permitted. Cross blocks may be zero.
2. For each of the nine full cofactor tensors in (11), enumerate all 3^4=81 words and the three four-vertex perfect matchings. A matching product is nonzero exactly when both of its entry-support variables are true, since C is a field. Introduce a term variable equivalent to that conjunction. At a zero-target word, exactly one nonzero matching product cannot sum to zero, so the three term variables may have counts 0,2,3 but not 1. At each of the three nonzero pure-target words, at least one term is nonzero. There are 729 coefficient positions: three nonzero targets and 726 zero targets.
3. Rank at most one makes the nonzero support of each cross block rectangular: two true entries (a,b),(c,d) force (a,d),(c,b). A zero block has empty support. This is necessary only; no coefficient sufficiency is claimed.
4. Each of the six off-diagonal rectangles in (12) satisfies the FULL row and column anchor disjunctions proved in Section 7. The selected AA unit fixes the required endpoint coordinate at either row, and the selected BB unit fixes it at either column. Existential selectors choose a valid row/column anchor; a selector imposes absence of all entries outside its prescribed physical coordinate row or column on both incident blocks. Zero blocks satisfy these containments. Every physical anchor disjunction extends to such selector values.

Thus every physical solution would extend to a satisfying assignment of this CNF. Dropping actual complex cancellation equations only enlarges its feasible set, so UNSAT of this necessary relaxation is sufficient for exclusion. There is no numerical, modular, genericity, or support-converse step.

The frozen CNF has 2394 variables and 11394 clauses:

| Clause category | Count |
| --- | ---: |
| Six matrix-unit choices | 222 |
| Matching-term equivalences | 6561 |
| Coefficient necessities | 2181 |
| Cross-block rectangles | 1458 |
| P2 row/column anchors | 972 |

The 2394 variables comprise 135 physical-entry supports, 2187 matching terms, and 72 anchor selectors. The independently reconstructed clause multiset, including multiplicities and duplicate literals, equals the frozen CNF exactly. Its SHA256 is

    4415ea3d243603910729098d104240ca2d6fd2fa1d2843098e3131b4088ac1ac.

The accepted proof is a `dpll-binary-up-v1` binary decision tree. Every internal node has both opposite decision branches; every leaf must yield contradiction by exact unit propagation from the original clauses under its decisions. Acceptance therefore proves UNSAT by exhaustive Boolean case splitting. This uses no trusted native SAT-solver verdict or unconnected UNSAT log.

The certificate contains 6860 binary branch nodes and 6861 conflict leaves, 13721 nodes total. Its SHA256 is

    d73b746cbf5bafdcb1ac6e2af9bcac65475e5d7d1595f82cabca25bc8556c1fd.

The independent standard-library checker uses functional residual clauses represented by positive/negative integer bit masks and repeated batch-unit elimination. It imports neither the producer's mutable watched-literal solver nor its backtracking/search code. It checks metadata against the raw frozen CNF and checks both children of every branch. Duplicate literals and tautologies are simplified only by exact Boolean identities. Nine positive and negative checker controls cover valid proofs, invalid conflict leaves, satisfiable branches, duplicate/tautological clauses, out-of-range decisions, and malformed nodes.

The accepted independent checker SHA256 is

    3fad19ae0bba42e40d9e77c30377da3263943dbdb14f8857f021b6ee0c10d6af.

Its full traversal accepted all nodes with child and bounded-runner exit
code zero in 88.619 seconds. The supplied portable
[checker](two-root-zero-source-certificate/check_certificate.py) preserves
every load-bearing function's AST and adds reviewed command-line/path
handling and optimization guards. Its SHA256 is
`ab565a6ee2a207687b56611b90871412115b9f052e31f0c016f99b25b85fc825`.
The independent reviews record exact encoding reconstruction, byte hashes,
and process-exit verification. Earlier empty native proof output and a
timed-out checker attempt were not accepted as proof. This theorem uses
only the accepted exact certificate.

The CNF is therefore unsatisfiable. By the necessary-support implication above, the remaining full physical pure-(3,3) cofactor system is impossible.

## 9. Conclusion and evidence boundaries

The exhaustive stress cover reduces Q=0 to branches closed by exact inactive polynomial algebra or to the pure-(3,3) FULL ternary cofactor system. The latter is reduced by a proved P2 anchor lemma and exact re-rooting to a frozen necessary support instance, independently shown UNSAT by an exact exhaustive decision-tree checker. These implications establish the stated common-coordinate Q=0 exclusion over C.

The proof never assumes the initially unobserved inactive H vanishes. Where H=0 is obtained, it is used only within that branch; no claim that full H_B is zero and no root-edge modification is made. The finite support instance covers all nine coordinate choices on every same-orientation matrix unit, all rank-one/zero cross supports, all full cofactor words, and all anchor choices, with no symmetry-fixed physical case omitted.

This closes only the named eight-vertex, maximum-two-root, common-coordinate zero-block child. Arbitrary root incidences, other orders, the global parent, and the Krenn--Gu conjecture remain separate. Global status is **UNRESOLVED**.
