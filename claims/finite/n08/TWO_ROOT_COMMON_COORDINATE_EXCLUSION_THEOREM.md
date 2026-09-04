# Eight-vertex two-root common-coordinate exclusion

## Status and evidence

**Proved exact finite exclusion over C**, independently reviewed on
2026-09-04. The result covers every root block of rank at least two within
the stated common-coordinate class, including all channel-rank and
zero-leg boundaries. It is not an exhaustive eight-vertex theorem or
global resolution. Global Krenn--Gu remains **UNRESOLVED**.

The [independent adversarial review](../../../docs/audits/TWO_ROOT_COMMON_COORDINATE_EXCLUSION_REVIEW_2026-09-04.md)
reconstructs the source, component classification, and cofactor argument.
The [primary replay](verify_two_root_common_coordinate_exclusion.py) checks
displayed identities and finite graph facts; it is corroboration, not the
proof. No Lean formalization or original-witness certificate is supplied.

## Exact scope and parent

Work over C. Suppose a physical ternary block graph W on eight vertices has full matching tensor T_W=Delta_(8,3), and its maximum fully-supported pairwise-zero torus-root cardinality is exactly two. Name a root pair 1,2 and put Q=W_12. Assume rank Q>=2. At each of the six other vertices assume BOTH physical root-incident blocks use one common outside coordinate:

    W_1u(-,z_u)=a_u z_u[c(u)],
    W_2u(-,z_u)=b_u z_u[c(u)],                      (1)

where a_u,b_u are constant vectors representing root covectors. Either may individually vanish. The common-coordinate hypothesis concerns physical blocks, not only evaluation at selected root vectors.

**Claim:** these hypotheses are inconsistent.

This closes one full-source child of the parent r>=n/2-1. It does not supply the common-coordinate hypothesis, exclude rank Q<=1, handle arbitrary n, or resolve the global conjecture. Non-coordinate root incidences remain a load-bearing open boundary. Global status stays **UNRESOLVED**.

Owning interfaces are the
[maximum-root theorem](../../arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md),
[full companion expansion](../../arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md),
[common cofactor decomposition](../../arbitrary-order/RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md),
[cofactor stresses](../../arbitrary-order/HIGHER_RESIDUAL_PERMANENTAL_TOMOGRAPHY_NESTED_COFACTOR_STRESS_AND_CUMULANT_INTERFACE.md),
and [physical Wick completion](../../arbitrary-order/BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md).
Each used matching identity is also proved directly below. The
[scaffold obstruction](../../arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md)
is a sharp control against replacing these full-source equations with
pure amplitudes or structural conditions alone.

## 1. Full source and the forced three pairs

Let B be the outside six-set, h=H_B its actual matching tensor, and C_uv=H_(B-{u,v}) its actual four-vertex cofactors. Set

    K_uv=a_u b_v^T+a_v b_u^T.

Partitioning a full matching by the two root partners gives the exact matrix-valued polynomial identity

    h(z)Q+sum_(u<v) z_u[c(u)]z_v[c(v)] C_uv(z) K_uv
       =diag(prod_w z_w[0],prod_w z_w[1],prod_w z_w[2]).  (2)

All nine matrix entries and all independent outside variables are retained.

For any colour c, set ALL six outside vectors to e_c. If fewer than two assigned labels equal c, the two roots cannot use two distinct outside partners: every such term in (2) vanishes. The source would read h_c Q=E_cc, impossible since Q has rank at least two. Hence each colour occurs at least twice. With six ports, the assigned colour classes B_0,B_1,B_2 are exactly pairs. This argument permits provisional labels at both-zero ports; their impossibility follows next.

Restrict every u in B_c to its inactive plane L_u=ker e_c^*. Let S be the polynomial ring over C in these twelve independent binary coordinates. Let A_uv denote the actual outside edge restricted to these planes. All restricted h,C remain the principal hafnians of the same A. From (2), h=0 in S.

### Same-group labels

Activate exactly B_c={u,v} by setting its two slots to e_c, keeping the other four inactive. Equation (2) becomes

    h_c Q+f_c K_c=p_c E_cc,
    K_c=K_uv, p_c=prod_(w outside B_c) z_w[c]!=0.

K_c cannot be zero or proportional to Q, since this would make a nonzero rank-one matrix a scalar multiple of Q. Therefore Q,K_c are independent, and constant matrix-span comparison gives

    K_c=gamma_c Q+delta_c E_cc, delta_c!=0,
    f_c=C_(B_c)=kappa_c p_c, kappa_c=delta_c^(-1)!=0.  (3)

There is **no assertion** that rank-one K_c forces gamma_c=0 when Q has rank two. Rank-one updated channels with gamma_c!=0 are retained throughout. Every port has at least one nonzero leg, since both zero would make its K_c zero.

### Dependent cross channels

Define the graph F on outside ports by cross-group edges

    uv in F iff K_uv belongs to C Q.                  (4)

It includes zero channels and, for rank-two Q, nonzero scalar multiples of Q. Activate a cross pair u,v on its assigned axes, keeping the other four inactive. The target is zero because every group retains an inactive vertex. If uv is not in F, Q and K_uv are independent, and the source forces

    C_uv=0 on its inactive complement.               (5)

No cofactor is discarded merely because its dependent channel is nonzero.

## 2. The complete dependent-channel graph

A port is A-only if a!=0,b=0, B-only if a=0,b!=0, and both if a!=0,b!=0. A-only ports form one zero-channel clique, B-only ports another. Each clique has at most one vertex per natural group, hence order at most three, because two same-group ports of one pure type would give K_c=0. Between opposite pure types, or between a pure port and a both port, K_uv is nonzero rank one. It cannot belong to C Q, since rank Q>=2. Thus these cliques have no other F neighbours.

### Both-port components containing only zero channels

Along a zero channel, cancellation of two nonzero outer products forces proportional a directions and proportional b directions. On a connected zero-only component write

    a_u=alpha_u a, b_u=beta_u b, alpha_u beta_u!=0.

An edge means rho_u=-rho_v, rho=alpha/beta. The component is complete bipartite: the two sides have opposite fixed nonzero ratios. Same-group vertices cannot be on opposite sides, since then their K_c would be zero.

### Both-port components containing a nonzero dependent channel

Such a channel is possible only when rank Q=2. If K_uv=lambda Q, lambda!=0, the two a vectors are independent and span column(Q), while the two b vectors span row(Q). These plane inclusions propagate along nonzero dependent edges and along zero edges by the preceding proportionality fact. All vertices of the component lie in these two fixed planes.

Normalize just this two-dimensional factorization lemma: take K_uv as the chosen spanning matrix of the line C Q, use a_u,a_v as the left basis and b_v,b_u as the right basis. Then

    Q_line=I_2,
    a_u=e_1,a_v=e_2,b_u=e_2,b_v=e_1.

This is NOT a change of the original GHZ coordinate axes in any source equation. Put J_s=[[0,-1],[1,0]]. The initial vertices satisfy b_u=J_s a_u and b_v=-J_s a_v. A neighbour w of u has, by direct comparison with a scalar identity,

    a_w=(x,mu), b_w=(mu,-x)=-J_s a_w.

More invariantly, if b_x=J_s a_x, then K_xy in C I_2 forces b_y=-J_s a_y: the difference from this relation contributes the rank-one matrix a_x(b_y+J_s a_y)^T, which cannot be a nonzero scalar identity. The symmetric argument reverses signs. Thus signs alternate on the connected component.

Every opposite-sign pair has K in C I_2 by the two-dimensional determinant identity. No same-sign pair does: its channel is a nonzero symmetrized product multiplied by J_s^T, has trace zero, and cannot be a scalar identity; a zero symmetrized product of two nonzero vectors is impossible in characteristic zero. Hence the component is complete bipartite. Same-group vertices must be on the same side, because every opposite-side pair would have K_c in C Q, contrary to (3).

### Every both-port component has at most four vertices

If a component had at least five vertices, it would contain both ports of two distinct natural groups c,d.

In a component with a nonzero dependent edge, every a lies in column(Q) and every b in row(Q). Equation (3) for each full group puts e_c and e_d in both planes. Since Q has rank two, these planes must both equal span(e_c,e_d). Thus Q is supported on the corresponding principal 2-by-2 coordinate block, which is invertible. Let k be the third colour. The equation K_k=gamma_k Q+delta_k E_kk and rank K_k<=2 force gamma_k=0: otherwise its principal 2-by-2 block and independent k entry give rank three. So K_k=delta_k E_kk has rank one. A both port of group k cannot have both legs in the Q planes and participate in this K_k: rank one of [a_u,a_v]J[b_u,b_v]^T forces at least one whole factor to have rank one with image e_k, contradicting the nonzero member leg in a plane excluding e_k. Thus no vertex from the third group can occur, contradicting component order at least five.

In a zero-only component, the two full-group channels K_c,K_d are nonzero scalar multiples of the same rank-one matrix P=a b^T. Eliminating P from their two instances of (3) forces

    Q in span(E_cc,E_dd).

Indeed the coefficient of Q in that elimination cannot be zero, since delta_c E_cc and a nonzero multiple of delta_d E_dd cannot cancel. If rank Q=3 this is already impossible. If rank Q=2, Q is diagonal with nonzero c and d entries. Its same-pair channels K_c,K_d, and hence P, are diagonal rank-one matrices supported on one of these two axes. The third group's K_k is again delta_k E_kk by the rank-three block argument. A member port in the zero-only component has both a,b along the same c or d axis, so its K_k is supported in that axis's row or column and cannot equal E_kk. Again the third group cannot occur.

Therefore every both component has order at most four. Such components are isolated vertices, edges, two-edge stars, three-edge stars K_(1,3), or K_(2,2). Every represented group lies entirely on one bipartition side and consequently has nonzero signed multiplicity. The only nonbipartite components of F are the pure A-only/B-only triangles.

## 3. Physical stresses and the two pure triangles

Set

    t_c=A_(B_c) f_c,
    t_uv=A_uv C_uv for uv in F.

Exact six-hafnian partner expansion at u in B_c gives, by h=0 and (5),

    t_c+sum_(v:uv in F) t_uv=0.                       (6)

The monomial supports of t_0,t_1,t_2 are pairwise disjoint. For c!=d, both vertices of the third group k have fixed coordinate c in t_c and fixed coordinate d in t_d; the unknown within-group edge factor cannot change those coordinates.

A signed sum of (6) over any bipartite F component cancels edge products. Every represented group's signed multiplicity is nonzero. Disjoint supports force the corresponding t_c zero. Unless F is exactly two pure triangles covering all six ports, every group has a vertex in a bipartite component. Thus all t_c vanish except for that single orientation configuration, which is handled next.

### Pure two-triangle repair, without coordinate purity of root vectors

Write B_i={A_i,B_i}, with A_i attached only to root 1 and B_i only to root 2. Their surviving root vectors need NOT be coordinate vectors: rank-one K_i may have gamma_i!=0. None of the following argument assumes otherwise.

Root 2 has zero physical edges to every A_i. A torus zero of any A_i-A_j physical edge would therefore form a three-root configuration with root 2. Maximum root cardinality two makes every such edge zero-free on the product torus, hence a nonzero matrix unit by the Laurent-unit argument over C. The same holds for B_i-B_j using root 1. Their inactive restrictions are monomials or zero.

Put X_ii=A_(Ai,Bi), t_i=X_ii f_i and, for {i,j,k}={0,1,2}, p_k=A_(Ai,Aj), q_k=A_(Bi,Bj). Solving the two triangle incidence systems gives

    p_k C_(Ai,Aj)=q_k C_(Bi,Bj)=(-t_i-t_j+t_k)/2.      (7)

If t_k!=0, the right side is nonzero by disjoint supports, so p_k is a nonzero monomial. It divides each nonzero support-separated summand. Since t_k uses coordinate k at A_i,A_j, p_k uses k at both. But t_i has coordinate i at A_j and t_j has coordinate j at A_i, so both must vanish. Thus at most one t_k can survive. A zero p_k instead makes the support-separated right side zero and kills all three directly.

Assume only t_k survives and let i,j be the other colours. Since f_j!=0, X_jj=0. Equation (7) makes p_i,q_i nonzero monomials dividing t_k, so they use coordinate k at A_j,B_j respectively. The physical four-hafnian for f_i reads

    A_(Aj,Bk) A_(Ak,Bj)=f_i-p_i q_i,                  (8)

because the X_jj X_kk term is zero. Across the flattening (A_j,B_k)|(A_k,B_j), the left side has rank at most one. The two nonzero product tensors on the right have independent factors on both shores: f_i uses coordinate i at A_j,B_j while p_i q_i uses k there. Their difference has rank two, contradiction.

Consequently all t_c vanish in every case, and the nonzero f_c give

    A_(B_c)=0 for all three groups.                  (9)

On every F component other than K_(2,2), its remaining vertex incidence equations kill all t_uv: use leaf elimination on a star and the nonsingular three-edge incidence matrix on a triangle. A K_(2,2) can retain a circulation, so it is addressed separately rather than silently imposing entrywise orthogonality.

## 4. Physical tripartite cofactor formulas

By (9), the outside graph on the inactive planes is tripartite 2+2+2. Let X,Y,Z be its 2-by-2 edge matrices between groups 01,02,12. Let J=[[0,1],[1,0]] and bar i=1-i. The three nonzero same-pair cofactors and exact cross-cofactor matrices are

    per X=kappa_2 prod_(v in B_0 union B_1) z_v[2],
    per Y=kappa_1 prod_(v in B_0 union B_2) z_v[1],
    per Z=kappa_0 prod_(v in B_1 union B_2) z_v[0],     (10)

    H=sum_(i,j,k) X_ij Y_(bar i,k) Z_(bar j,bar k)=0,
    C_X=J Y J Z^T J,
    C_Y=J X J Z J,
    C_Z=J X^T J Y J.                                 (11)

These are direct unsigned matching identities. Rank calculations use the fraction field of S, not a generic specialization of the physical coefficients.

### Endpoint factor lemma

If X has rank one, its nonzero permanent gives

    X00 X11=X01 X10=(per X)/2!=0.

Unique factorization and each entry's endpoint bidegree force every X entry to be a nonzero constant times its coordinate-2 endpoint product. Likewise rank-one Y entries are pure coordinate 1 and rank-one Z entries pure coordinate 0.

If X,Y are rank one, EVERY entry of C_Z is nonzero: it is a sum of two nonzero terms with different monomials at the two shared group-0 vertices, namely their coordinate-2/coordinate-1 products in opposite assignments. These independent monomials cannot cancel. The same statement holds under relabelling.

In particular, no entire cofactor block can vanish. For example C_Z=0 would force X,Y both rank one by (11) and their nonzero permanents, and the preceding paragraph contradicts C_Z=0.

## 5. Every K_(2,2) exceptional component is impossible

There can be only one such component, using four of the six vertices. Same-group ports lie entirely on one of its sides. There are two possible group-count patterns.

### Pattern 2+2

The component uses both ports of two groups, on opposite sides. The remaining two ports belong to the third group and cannot form a cross-group F edge. Hence at least one whole cross-cofactor block vanishes by (5), contradicting the endpoint factor lemma above.

### Pattern 2+1+1

Relabel so the full group is B_0 on one side, with one vertex from B_1 and one from B_2 on the other. The F supports in the 01 and 02 cofactor blocks are each contained in one column. The only possible extra F edge joins the two remaining anchor ports in B_1,B_2. Thus C_Z has support at most one entry.

If C_Z=0, the preceding endpoint factor lemma is already contradictory. Otherwise that sole nonzero cofactor belongs to the isolated anchor edge. Its edge product was killed by its two vertex stresses after t_c=0. Therefore the corresponding physical Z entry is zero. Since per Z!=0, det Z=plus-or-minus per Z!=0, so Z is invertible.

The one-column supports make rank C_X<=1 and rank C_Y<=1. From (11) and invertible Z, rank Y<=1 and rank X<=1. Their nonzero permanents force both ranks exactly one. The endpoint factor lemma then makes ALL four entries of C_Z nonzero, contradicting its support of at most one entry.

This excludes the K_(2,2) circulation directly from the full physical cofactors; no unjustified edgewise stress elimination is used.

## 6. Closure when F has no K_(2,2)

Every F component is now a star of order at most four or a pure clique of order at most three. The vertex incidence equations give

    A_uv C_uv=0 on every F edge.

The same product is zero outside F by (5). Also |F|<=6, with equality only for two disjoint triangles: a four-vertex star plus the remaining two-vertex component has at most four edges, and the alternatives on six vertices attain six only through two triangles.

If all cross cofactors vanish, (11) and the nonzero permanents force X,Y,Z rank one; the endpoint factor lemma contradicts their zero cofactor blocks.

Otherwise take a nonzero cross cofactor, say in X. Its corresponding edge is zero by entrywise orthogonality, and per X!=0 makes X invertible. If Y were rank one, all its entries would be nonzero by the endpoint factor lemma, so entrywise Y*C_Y=0 would force C_Y=0. Invertible X would then force Z=0 through (11), impossible. Thus Y is invertible; symmetrically Z is invertible.

All three cofactor matrices are now invertible and each has at least two nonzero entries. Their support is contained in F and has at least six edges. The preceding edge bound forces exactly two disjoint triangles, each using one vertex of each group. Entrywise orthogonality kills the six actual edges of these triangles. Each cross block has its two complementary entries nonzero because its permanent is nonzero. The surviving graph is the complementary six-cycle in K_(2,2,2).

Each pure permanent is now the product of two surviving edge forms. Unique factorization and endpoint bidegrees force each such edge to be a nonzero constant multiple of its omitted-colour coordinate product. The six-cycle has two perfect matchings. At each vertex its two incident edges go to different groups and use different available coordinates. Hence the two matching monomials are distinct and both nonzero; they cannot cancel. This contradicts H=0.

Every case is impossible, proving the theorem for all rank Q>=2.

## Status and limits

The proof is pointwise in the physical complex coefficients. It retains all same-pair rank patterns, nonzero Q-dependent cross channels, zero individual incident legs, coordinate-boundary kernels, zero inactive matrix-unit restrictions, and K_(2,2) stress circulations. No solver or search is a proof leaf. The only uses of maximum root cardinality are the physical AA/BB matrix-unit constraints in the pure orientation case.

The proof-topology delta is exclusion of this complete common-coordinate
n=8 child, including the entire rank-two root boundary and all same-pair
rank patterns. Rank Q<=1, common-coordinate supply, general root
incidences, higher n, and the global parent remain separate. This result
does not justify a third sibling refinement without the parent-theorem
attempt required by the operating contract.

## Replay

```text
python claims/finite/n08/verify_two_root_common_coordinate_exclusion.py
```

The exact replay checks the 105-term source partition, twelve cross-cofactor
identities, the same-group cofactors, triangle stress, flattening ranks,
dependent-channel finite algebra, and the complete labelled four-cycle
support split. It also checks the two-triangle equality cases. The written
proof establishes the quantified source and graph implications; passing
these finite checks does not enlarge the theorem's scope.
