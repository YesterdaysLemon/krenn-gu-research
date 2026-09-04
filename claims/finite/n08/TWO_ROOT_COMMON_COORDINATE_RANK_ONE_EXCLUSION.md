# Nonzero rank-one completion of the common-coordinate eight-vertex exclusion

**Proved exact analytic exclusion over C**, independently reviewed on
2026-09-04. The [adversarial review](../../../docs/audits/TWO_ROOT_COMMON_COORDINATE_RANK_ONE_REVIEW_2026-09-04.md)
covers both rank-one branches, every individual zero-leg case, and legal
reuse of the physical cofactor argument. No Lean formalization is claimed.

The global Krenn--Gu conjecture remains **UNRESOLVED**. This is a common-coordinate eight-vertex child, not a proof that all maximum-root-two witnesses have that incidence structure. The zero physical root block Q=0 is explicitly outside this note.

## 1. Statement and exact scope

Work over C. Let W be a physical ternary block graph on eight vertices with full perfect-matching tensor

    T_W=Delta_(8,3)=sum_(c=0)^2 e_c^(tensor 8).

Assume its maximum cardinality of a fully-supported pairwise-zero-coupled torus-root configuration is two. Name a maximum root pair 1,2 and let Q=W_12 be its physical 3-by-3 block. Suppose Q is nonzero of rank one. At every other vertex u, assume both physical root-incident blocks use one common outside coordinate c(u):

    W_1u(-,z_u)=a_u z_u[c(u)],
    W_2u(-,z_u)=b_u z_u[c(u)],                       (1)

where a_u,b_u are constant root covectors, represented as columns. Individual a_u or b_u may be zero. The condition is on physical blocks, not only on their contractions at selected root vectors.

**Theorem.** These hypotheses are inconsistent.

Write Q=pq^T with p,q nonzero. If both p and q are coordinate vectors up to scale, Q is a nonzero matrix monomial. It cannot vanish at a pair of fully-supported vectors, so it cannot be the physical edge of the named torus-root pair. It remains to cover:

1. neither p nor q is proportional to a coordinate vector;
2. exactly one factor is proportional to a coordinate vector.

Root transposition exchanges the two one-coordinate orientations. Scalar rescaling of a rank-one factor lets the second case be written p=e_t, with q non-coordinate. No general change of the GHZ coordinate axes is made.

## 2. Full source and physical cofactor supply

Let B be the six outside vertices. Denote by h=H_B the actual outside matching tensor and by C_uv=H_(B-{u,v}) its actual four-vertex cofactors. Put

    K_uv=a_u b_v^T+a_v b_u^T.

The original matching definition partitions each matching into the case using the root edge and the cases using two different outside root partners. It gives the exact matrix-valued polynomial identity

    h(z)Q+sum_(u<v) z_u[c(u)]z_v[c(v)] C_uv(z) K_uv
       =diag(prod_w z_w[0],prod_w z_w[1],prod_w z_w[2]).  (2)

All nine entries and all independent outside variables are retained. This is the uncontracted source partition, not a scalar evaluation or an ideal-membership relaxation.

In both remaining rank-one cases Q is not proportional to E_cc for any c. Set all six outside vectors to e_c. If at most one outside port is assigned c, the two roots cannot use two different outside partners and (2) would read h_c Q=E_cc, impossible. Thus there are exactly two ports of each assigned colour. Write their classes as the three pairs B_0,B_1,B_2.

At u in B_c use the inactive plane L_u=ker e_c^*. Work in the polynomial ring S over C in the twelve independent inactive coordinates. Let A_uv denote the physical outside edge restricted to L_u x L_v. The restrictions of h and C_uv are the principal hafnians of this one common A. Setting every outside port inactive in (2) gives hQ=0 and therefore

    H:=haf(A)=0.                                     (3)

Activate only the two members of B_c on their coordinate-c axes, keeping the other four inactive. The target becomes a nonzero pure-c product times E_cc. A zero or Q-proportional K_c would make that target a multiple of Q, impossible. Therefore Q,K_c are independent and constant matrix-span comparison supplies

    K_c:=K_(B_c)=gamma_c Q+delta_c E_cc, delta_c!=0,
    f_c:=C_(B_c)=kappa_c prod_(w outside B_c) z_w[c],
    kappa_c=delta_c^(-1)!=0.                          (4)

In particular every K_c is nonzero, and no port has both legs zero.

Define the exceptional cross-group graph F by

    uv in F iff K_uv belongs to C Q,                 (5)

including both zero channels and nonzero Q-dependent channels. Activating a cross pair leaves an inactive vertex of every group, so its target is zero. Whenever uv is not in F, independence from Q forces

    C_uv=0 on the inactive complement.               (6)

Thus H=0, the three nonzero pure cofactor values f_c, and the zero cross cofactors in (6) are actual coefficient identities of the same physical outside graph.

## 3. Reusable inactive-cofactor closure

This is the rank-independent part of the PR #340 proof. It is stated with its complete inputs so that applying it to rank-one Q does not invoke the rank-at-least-two source theorem.

### Lemma: sufficient physical inputs

Suppose the six outside vertices are paired as B_0,B_1,B_2, with independent inactive planes as above, and the following hold:

- H=haf(A)=0 as a polynomial;
- the within-group four-cofactors are the nonzero pure products f_c in (4);
- every cross cofactor outside F vanishes;
- every connected component of F has at most three vertices;
- each bipartite component has all represented vertices of a natural group on one bipartition side, giving nonzero signed multiplicity for every represented group;
- every nonbipartite component is a triangle of ports attached only to root 1 or only to root 2, with one port of each group;
- maximum torus-root cardinality is two in the original physical graph.

Then these inputs are inconsistent. The proof needs no assumption on the rank of Q. In a pure orientation triangle it needs only the zero incident legs, not coordinate purity of the surviving root covectors.

### Proof: stresses and the orientation exception

Set t_c=A_(B_c) f_c and t_uv=A_uv C_uv for uv in F. Exact partner expansion of H at u in B_c gives

    t_c+sum_(v:uv in F) t_uv=0.                       (7)

The monomial supports of t_0,t_1,t_2 are pairwise disjoint. For c!=d, both vertices of the third group k use fixed coordinate c in every monomial of t_c and fixed coordinate d in every monomial of t_d; the unknown within-group factor involves neither vertex.

On a bipartite component, sum (7) with signs on the two sides. Edge products cancel, and the nonzero signed group multiplicities force each represented t_c to vanish separately. Unless F is two orientation triangles covering all six vertices, every group has a vertex in a bipartite component. Hence all t_c vanish outside that one exception.

For two triangles, write B_i={U_i,V_i}, where U_i is attached only to root 1 and V_i only to root 2. Root 2 has zero physical edges to every U_i. If a physical U_i-U_j block had a torus zero, those two vertices together with any torus vector at root 2 would give three roots. Thus it is zero-free on the product torus and is a nonzero coordinate monomial, by the Laurent-unit property over C. The same argument applies to every V_i-V_j block using root 1. Their inactive restrictions are monomials or zero.

Put X_ii=A_(Ui,Vi), p_k=A_(Ui,Uj), q_k=A_(Vi,Vj), where {i,j,k}={0,1,2}. Solving the triangle vertex stresses gives

    p_k C_(Ui,Uj)=q_k C_(Vi,Vj)=(-t_i-t_j+t_k)/2.      (8)

If t_k!=0, the right side is nonzero by disjoint supports. The monomial p_k is therefore nonzero and divides each support-separated nonzero summand. Since t_k uses coordinate k at U_i,U_j, p_k must use k at both. But t_i uses coordinate i at U_j and t_j uses coordinate j at U_i, so t_i=t_j=0. A zero p_k instead makes the right side zero and directly kills all three t's.

Assume only t_k survives. For the other i,j, f_j!=0 gives X_jj=0. Equation (8) makes p_i,q_i nonzero monomials dividing t_k, so they use coordinate k at U_j,V_j. The exact four-hafnian for f_i is therefore

    A_(Uj,Vk) A_(Uk,Vj)=f_i-p_i q_i.                 (9)

Across (U_j,V_k)|(U_k,V_j), the left side has rank at most one. The right side is a difference of two nonzero product tensors with independent factors on both shores: f_i uses coordinate i at U_j,V_j, while p_iq_i uses k. Its rank is two, contradiction.

All t_c vanish, including the two-triangle case. Since each f_c is nonzero in the integral polynomial ring, all within-group physical restricted edges vanish. The remaining componentwise equations in (7) kill every t_uv: leaf elimination handles edges/stars, and the triangle incidence determinant is plus-or-minus two. Thus

    A_(B_c)=0 for every group,
    A_uv C_uv=0 for every cross-group pair.           (10)

For pairs outside F the second identity also follows directly from C_uv=0.

### Proof: the common physical tripartite endpoint

Let X,Y,Z be the 2-by-2 physical edge matrices between groups 01,02,12. Their permanents are the nonzero pure products f_2,f_1,f_0. With J=[[0,1],[1,0]] and bar i=1-i, direct matching expansion gives

    H=sum_(i,j,k) X_ij Y_(bar i,k) Z_(bar j,bar k)=0,
    C_X=JYJZ^T J, C_Y=JXJZJ, C_Z=JX^T JYJ.          (11)

If every cross cofactor is zero, these product equations and the nonzero permanents make X,Y,Z rank one over Frac(S). For rank-one X,

    X00 X11=X01 X10=(per X)/2!=0.

Unique factorization and endpoint bidegrees force every X edge to be a nonzero constant times its coordinate-2 endpoint product. Likewise Y uses coordinate 1 and Z coordinate 0. Each resulting cross cofactor contains two nonzero distinct monomials on the intermediate group's independent planes, impossible.

If some cross cofactor is nonzero, its physical edge is zero by (10). Say it is an X entry. Then det X=plus-or-minus per X!=0, so X is invertible. A rank-one Y would have all entries nonzero by its pure permanent; entrywise Y*C_Y=0 would force C_Y=0, and invertible X in (11) would force Z=0. Thus Y is invertible, and similarly Z is invertible. All three cofactor matrices are invertible, hence their support has at least six edges.

That support lies in F, whose components have order at most three. It can have at most six edges, with equality only for two disjoint triangles. Entrywise orthogonality kills their six actual edges. The complementary physical support is a six-cycle, with each cross block's two surviving entries nonzero by its permanent. Endpoint factorization makes them pure omitted-colour products. The six-cycle has two perfect matchings; at every vertex its two incident edges use different available coordinates. Their two nonzero monomials are distinct and cannot cancel, contradicting H=0. This proves the lemma.

## 4. Rank-one dependent-edge facts and notation

To avoid confusing line membership with zero-leg orientation, use the following distinct terms:

- **first-root-only:** a!=0,b=0;
- **second-root-only:** a=0,b!=0;
- **both-leg:** a!=0,b!=0;
- line class L={u:a_u in Cp}, including a_u=0;
- line class R={u:b_u in Cq}, including b_u=0;
- central class Z=L intersect R;
- remaining class D, the complement of L union R.

For a nonzero dependent channel K_uv=lambda pq^T, lambda!=0, either both endpoints belong to L or both belong to R. Indeed write K_uv=[a_u,a_v]J[b_u,b_v]^T. If both two-column factors had rank two, the product would have rank two. A rank-one left factor must have image Cp, or a rank-one right factor must have image Cq. This argument includes zero individual columns.

A zero channel between both-leg ports forces their a directions proportional and their b directions proportional. A connected component consisting only of such zero channels has fixed projective a,b directions and opposite nonzero scalar ratios. It is complete bipartite. Same-group ports cannot lie on opposite sides, because that would make their K_c zero.

## 5. Neither root factor is a coordinate vector

Assume neither p nor q is proportional to any e_c. Then (4) has rank one exactly when gamma_c=0: with gamma_c!=0, the independent left vectors p,e_c and independent right vectors q,e_c give rank two.

Project each same-pair source to (C^3/Cp) tensor (C^3/Cq). The target delta_c[e_c] tensor [e_c] is nonzero. Therefore no port is central, and each group has at most one member of L and at most one member of R.

A first-root-only port belongs to R but not L, so its nonzero a is not proportional to p. Its channel with any other port is a b_v^T; it cannot be a nonzero multiple of Q. Its exceptional neighbours are exactly other first-root-only ports, through zero channels. They form a separate clique with at most one vertex per group. The second-root-only clique is symmetric. Both cliques have order at most three, and their triangles are exactly the orientation triangles allowed in the lemma.

On the both-leg L ports write a_u=alpha_u p, alpha_u!=0. Since none is central, b_u is not in Cq. Put

    w_u=[b_u/alpha_u] in C^3/Cq, w_u!=0.

The dependent-channel equation is precisely w_u=-w_v. Each component is complete bipartite, has at most one port of each group, and therefore order at most three. A zero-channel neighbour also remains in L by proportionality; a nonzero dependent neighbour remains in L by the rank-one dependent-edge fact, because this endpoint is not in R. Thus no exceptional edges leave these components. The symmetric quotient construction handles both-leg R ports.

Every D port has both legs nonzero, and a nonzero dependent edge is impossible. Its components have only zero channels and the projective-ratio structure above. If a component contains both ports of a group c, its same-pair channel is nonzero rank one; hence K_c=delta_c E_cc and its common a,b directions are e_c. A member of another group d makes K_d supported only in row c or column c. Rank-one K_d=delta_d E_dd is impossible, so gamma_d!=0. Removing row and column c in (4) makes the same Q submatrix a nonzero multiple of E_dd. The third group would force it to be a nonzero E_ee multiple, impossible. Nor can both ports of d occur, since their rank-one channel would be proportional to E_cc. Thus every D component has order at most three. A component without a full group trivially has that bound.

All exceptional components satisfy the reusable lemma's graph hypotheses: their bipartite signed group counts are nonzero, and their only triangles are pure zero-leg orientation cliques. The physical contradiction follows. This excludes the entire two-non-coordinate-factor case.

## 6. Exactly one coordinate factor

By root transposition and scalar normalization assume p=e_t and q is non-coordinate. The special same-pair channel is

    K_t=p(gamma_t q+delta_t p)^T,

always rank one, with row direction not proportional to q. It need not be a coordinate matrix unit. For each good group c!=t, rank K_c=1 exactly when gamma_c=0, giving K_c=delta_c E_cc.

### Source restrictions on line classes

For a good group, the double quotient modulo p and q again excludes central ports and gives at most one L port and at most one R port. One-sided quotients are stronger:

- if u in B_c is in L, then b_u is a nonzero multiple of e_c; the left quotient is [a_partner] tensor b_u=delta_c[e_c] tensor e_c, including a_u=0;
- if u in B_c is in R, then a_u is a nonzero multiple of e_c, by the right quotient, including b_u=0.

Every R port in the special group t is central. Projecting its same-pair equation on the right modulo q gives

    a_u tensor [b_partner]=delta_t p tensor [p],

which is nonzero because q is non-coordinate. Thus a_u is a nonzero multiple of p. All central ports therefore belong to B_t and have nonzero a. There is at most one central port, since two would make K_t proportional to Q. Its partner's b is not in Cq.

### Central components, including every zero-leg case

Let z be central, a_z=alpha p, alpha!=0, and b_z=beta q. If beta!=0, z is F-isolated. A potential dependent neighbour in L but not R leaves an uncancelled term modulo q; a neighbour in R but not L leaves an uncancelled term modulo p. A zero channel would require another central both-leg port. None exists.

If beta=0, z is first-root-only. Its exceptional neighbours are exactly the R ports: K_zv=alpha p b_v^T. There can be at most one such port from each good group and none from its same-group partner. The two good R ports have a directions on their different coordinate axes e_c,e_d. Their mutual channel cannot have image p, and it can be zero only when both b legs are zero. Thus the component is an isolated vertex, edge, two-edge star, or ordinary first-root-only triangle. It has at most three vertices; a triangle has one member of every group.

A central port with a=0 is impossible by the preceding nonzero quotient. These arguments cover central both-leg and central zero-b cases without division by a zero scalar.

### Noncentral R ports

There is no noncentral R port in B_t, and at most one in each good group. Apart from the central zero-b hub, their exceptional edges cannot leave R: nonzero dependence uses the same-class fact, while zero dependence preserves their a direction or joins first-root-only ports. Between the two good R ports an exceptional edge is possible only when both b legs vanish, as above. Hence these components have order at most two unless joined by the already treated hub.

### Noncentral L ports

First take a_u=0. These ports are second-root-only and have b_u outside Cq. They form a separate zero-channel clique, with at most one port per group. They cannot join a nonzero-a L port, because its channel would require this b_u to lie in Cq, and cannot join the central or remaining classes. Thus the clique has order at most three, with any triangle a pure orientation triangle.

For all other L ports write a_u=alpha_u p, alpha_u!=0, and b_u outside Cq. The nonzero quotient vectors w_u=[b_u]/alpha_u satisfy the exact exceptional relation w_u=-w_v. Components are complete bipartite; same-group vertices lie on one side, because K_c is not proportional to Q.

Every good group has at most one L port. A component larger than three would thus contain both t ports and one port of each good group. The two t ports have the same quotient w on their side. Projecting their same-pair source modulo q gives

    2 alpha_u alpha_v w=delta_t[p].                  (12)

Therefore w is proportional to [p]. A good c member has b proportional to e_c, so [e_c] is proportional to [p] modulo q. Equivalently q belongs to span(p,e_c). Both good groups cannot satisfy that relation: the intersection of the two coordinate planes is Cp, which would make q coordinate. Hence every such component has order at most three. This includes both support-two and support-three q; support two can permit one good neighbour but never both.

### Remaining D components

D ports have both legs nonzero and belong to neither distinguished line class. Their exceptional edges are all zero channels, so their components have the projective-ratio bipartition with each group on one side.

A component containing both t ports would have common a direction p, because K_t has column line Cp, contradicting D. If it contains both ports of a good group c, rank one of their same-pair channel forces K_c=delta_c E_cc and common directions e_c. A port of the other good group d makes K_d supported only in row c or column c. Its source cannot vanish off that row and column: after deletion, the d,d entry remains delta_d, because Q=pq^T has only row t and d differs from c,t. Therefore no other good group can occur. At most one t port can occur, since two would give K_t proportional to E_cc, contradicting its column line Cp. Thus every D component has order at most three.

### Return to the physical lemma

Every exceptional component has order at most three. Each bipartite component has nonzero signed group counts; all triangles are first-root-only or second-root-only cliques with one port per group. The exact physical source supplies H=0, the three pure f_c, and the zero cofactors outside F. The reusable lemma therefore gives the contradiction, including its orientation repair, which uses only zero legs and not purity of the nonzero root vectors.

This excludes the entire one-coordinate-factor case. Root transposition excludes the opposite orientation.

## 7. Completion and provenance

The two cases exhaust all nonzero rank-one root blocks except matrix monomials. Such a monomial cannot vanish on the product torus and is incompatible with the named torus-root pair before any source analysis. Thus every nonzero rank-one Q is excluded under the stated common-coordinate n=8/max-r=2 hypotheses.

The reusable inactive-cofactor lemma is the analytic content of the
[rank-at-least-two proof](TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md),
stated and proved here without importing its source-rank hypothesis.
The source identities retain the owning
[maximum-root](../../arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md),
[complete companion](../../arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md),
and [common cofactor](../../arbitrary-order/RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md)
interfaces. No solver result is used in this rank-one argument.

The zero root block is treated in the separate
[zero-block proof](TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md).
Supply of common-coordinate physical incidences, higher orders, and the
unrestricted parent are not established by this note.
