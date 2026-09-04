# Independent whole rank-at-least-two common-coordinate audit

2026-09-04. Reviewer: independent Astra-high subagent
`lab_r2_consolidation_review`; integration owner: coordinator. Separate
adversarial analytic audit of the
[owning theorem](../../claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md).
Earlier narrower exploratory rank cases are not prerequisites for this
proof. Global Krenn--Gu remains **UNRESOLVED**.

## Verdict and scope

PASS for the proposed complete rank-at-least-two extension within the physical common-coordinate eight-vertex class. Exact assumptions: an actual complex ternary GHZ matching tensor on eight vertices, global maximum torus-root cardinality two, a named root pair with physical Q of rank at least two, and both physical root legs at each outside vertex supported on its assigned single common outside coordinate. Individual legs may be zero.

No null-vector support condition is needed in this new proof. All rank-two root blocks, including coordinate kernels and shared zero coordinates, are covered. Rank-at-most-one Q, non-common-coordinate incidence, unrestricted eight-vertex witnesses, and the global parent remain outside scope. This PASS concerns the precise proposal reconstructed below, pending review of any final integrated theorem text.

The final integrated theorem was subsequently read in full and received
**PASS**, with SHA256
`2cdc82a71c04db736504006cd760ceb8a4b10a672197b4bafaaf0247a982e3f7`.
The rank-at-least-two statement, dependent-channel normalization, component
bound, pure-triangle repair, and four-cycle argument faithfully implement
this review. No mathematical HOLD or scope drift was found. The earlier
proposal-stage qualifications below preserve review chronology.

## 1. Universal label counts and source supply

The simpler count proof is valid at every rank Q>=2. If at most one port is assigned colour c, set ALL six outside vectors equal to e_c. Only ports assigned c can have nonzero root legs; thus no matching can attach both roots to distinct outside ports. The exact open-root source is h(e_c,...,e_c)Q=E_cc, impossible by ranks zero-or-at-least-two versus one. Every colour therefore has at least two ports, giving exactly three pairs.

Same-pair activation still gives h_c Q+C_c K_c=p_c E_cc with nonzero pure p_c. A zero or Q-proportional K_c is impossible by the same rank comparison. Constant matrix-span extraction yields

  K_c=gamma_c Q+delta_c E_cc, delta_c!=0,
  f_c=C_c=(1/delta_c)p_c!=0.

These are constant coefficients, not functions of the inactive variables. The full source on all inactive planes gives H=0. Cross activation forces C_uv=0 whenever K_uv is outside C Q. Define F on CROSS-group pairs by K_uv in C Q, including zero. Same-pair channels are outside C Q and nonzero, so each port has at least one nonzero leg.

There is deliberately NO assertion that rank-one K_c implies gamma_c=0. That assertion is false on some newly admitted rank-two fibres and is unnecessary below.

## 2. Pure orientations and both-port components

Pure A-only and B-only ports form their separate F cliques, with at most one port of each group. Other pairings involving a pure port have nonzero rank-one channel and cannot be proportional to rank-at-least-two Q. Thus no pure clique connects to a both-nonzero port or to the opposite pure type. Pure components have at most three vertices.

For a both-port component containing only zero channels, cancellation of two nonzero outer products gives common projective a,b directions. Writing a_u=alpha_u a,b_u=beta_u b, an edge means alpha_u/beta_u= -alpha_v/beta_v. Hence the component is complete bipartite. A group cannot occupy both sides, since its K_c is not in C Q and in particular is nonzero.

### Nonzero dependent components: complete bipartiteness

Such a component requires rank Q=2. A nonzero K_ij=lambda Q has rank two, so its two a vectors span col(Q) and its two b vectors span row(Q). Memberships propagate along every F edge: directly by rank factorization on a nonzero dependent edge, and by both projective proportionalities on a zero edge.

Choose auxiliary bases in these two planes so Q is represented by I_2. For an edge K_ij=lambda I_2, lambda!=0, take v in ker(b_i^T). Then lambda v=a_i b_j^T v, so ker(b_i^T)=C a_i. Therefore b_i^T a_i=0; likewise b_j^T a_j=0. This isotropy propagates along zero edges and holds directly at every nonzero dependent edge. Consequently, for fixed alternating invertible J=[[0,-1],[1,0]], each port has

  b_i=rho_i J a_i, rho_i!=0.

For any two ports, K_ij belongs to C I_2 iff rho_i=-rho_j. This includes parallel a directions: then K_ij is zero exactly for opposite rho, and otherwise is nonzero rank one. For independent a directions, change the two-dimensional a basis to see K_ij represented, up to a common nonzero factor and conjugation, by diag(-rho_j,rho_i); it is scalar exactly for opposite rho. Equivalently this follows directly by expanding a_i(Ja_j)^T and a_j(Ja_i)^T.

Thus a connected component has exactly the two opposite nonzero rho values on its two sides and is complete bipartite. Same-group vertices cannot lie on opposite sides because that would put K_c in C Q. No physical GHZ coordinate change is made: this normalization only proves channel-proportionality facts inside the two image planes. No Hermitian conjugation or positivity assumption is used.

## 3. Every both component has at most four vertices

Suppose a both component contains at least five of the six ports. It contains both ports of two groups c,d and at least one port of the third group k.

If it has a nonzero dependent edge, all its a vectors lie in U=col Q and b vectors in V=row Q. Since it contains both c ports, K_c and Q have column space in U and row space in V, and their difference delta_c E_cc puts e_c in both U,V. The d pair similarly puts e_d in both. Therefore U=V=span(e_c,e_d), Q is supported on that principal coordinate plane, and Q_kk=0. The represented k port has both a[k]=b[k]=0. Consequently its same-pair K_k has (k,k) entry zero, regardless of the other k port. But K_k=gamma_k Q+delta_k E_kk has (k,k) entry delta_k!=0. Contradiction.

If all channels in the component are zero, its same-side full-group channels K_c,K_d are nonzero scalar multiples of the same rank-one outer product P. Eliminate P from their source equations. The resulting Q coefficient cannot be zero, because the remaining nonzero multiples of the distinct E_cc,E_dd cannot cancel. Thus Q is a rank-two diagonal matrix supported on coordinates c,d; rank-three Q is already impossible in this branch. Furthermore P, being a nonzero scalar multiple of gamma_c Q+delta_c E_cc, is a nonzero rank-one matrix supported on that coordinate plane. Its common a,b directions lie in the plane. The represented k port again has a[k]=b[k]=0 and yields the same zero-versus-delta_k contradiction.

This entrywise (k,k) argument avoids any need to reintroduce rank-one iff gamma=0 or nonzero principal-adjugate assumptions. It also covers a six-port component by choosing any two complete groups and a third-group port.

The remaining four-vertex both-component possibilities are exactly K_1,3 and K_2,2. A natural group lies entirely on one bipartition side. Smaller both components are forests; pure orientation cliques of order three remain the only triangles.

## 4. Internal-edge stresses and the pure-triangle exception

The previously audited disjoint monomial supports of t_c=A_{B_c} f_c depend only on the independent inactive planes and the pure f_c. A signed sum of vertex stresses on any bipartite F component has nonzero signed multiplicity for every represented group, because the group lies on one side. Thus every represented t_c vanishes. As before, the only exception is two disjoint pure orientation triangles covering all six ports.

The pure-two-triangle repair does NOT need a_{A_i} or b_{B_i} proportional to e_i. It only needs A_i to have its root-2 physical leg zero and B_i to have its root-1 physical leg zero, plus the already proved pure f_i. Global maximum r=2 then forces every physical AA and BB edge to have no torus zero, hence be a nonzero matrix monomial. Their inactive restrictions are monomials or zero. The old stress-divisibility argument shows at most one t_k can remain; the exact four-hafnian identity has a rank-at-most-one crossed product and a rank-two difference of pure tensors, by independent coordinates i versus k at A_j and B_j. This contradiction is entirely about outside planes and pure f_i. Root-leg axis purity appears nowhere in it.

Thus every t_c vanishes, and nonzero f_c implies all three internal restricted physical edges vanish. Forest incidence elimination and triangle determinant two kill every edge product A_e C_e except potentially on a K_2,2 component. One must NOT assert entrywise orthogonality on that even cycle before the separate argument below.

## 5. Reusable pure-cofactor product fact

After internal edges vanish, use the tripartite X,Y,Z blocks with their nonzero pure permanents. The exact identities are

  C_X=J Y J Z^T J,
  C_Y=J X J Z J,
  C_Z=J X^T J Y J,

where J now denotes the exchange matrix, not the alternating matrix used only in the component lemma.

No entire cross-cofactor block can be zero. Indeed, in such a zero matrix product neither factor block is zero, since its permanent is nonzero. If either factor were invertible, the other would be zero. Thus both have rank one over the inactive-variable fraction field. Their determinants zero and nonzero pure permanents force every entry to be a nonzero constant times its omitted-colour endpoint monomial. Every entry of their cofactor product is then a sum of two nonzero terms with distinct monomials on the shared group's two independent binary planes. It cannot vanish. This proves the reusable fact without edgewise orthogonality or any property of the third physical block.

This is stronger than merely excluding all three cofactor blocks simultaneously zero, and is valid pointwise in the physical coefficients.

## 6. Complete K_2,2 cover and exclusion

A K_2,2 component uses four ports. Since there are only three groups, some group appears twice; both its ports lie on the same side. The exhaustive alternatives are therefore (a) two full groups on opposite sides, or (b) one full group on one side and one port from each other group on the other side. No group can be split across sides, and no fourth distinct group exists.

(a) Two full groups. The remaining two ports belong to the third group and cannot have an F edge between themselves. F has no edges from them to the four-port component by definition of component. Therefore the two cross-cofactor types involving the third group vanish identically. Either one contradicts the reusable fact above. No assumption about physical cycle edge products is needed.

(b) Full group c against singles a in B_d and b in B_e. Let X be the c-d block, Y the c-e block, and Z the d-e block. Each of C_X,C_Y has support in one column, the column of the represented single port. The only possible F edge outside the cycle is d'e', so C_Z has at most the one entry d'e'. These orientations agree with the displayed gradient identities.

If C_Z=0, the reusable fact gives a contradiction. Otherwise its d'e' entry is nonzero and d'e' must be a separate two-vertex F component. Its vertex stresses, with t_d=t_e=0, give A_d'e' C_d'e'=0. The integral domain then gives A_d'e'=0. Hence Z has a zero entry while per Z!=0, making det Z=plus-or-minus per Z nonzero.

Now rank C_X=rank Y<=1 by C_X=JYJZ^T J and the one-column support. Likewise rank C_Y=rank X<=1. Nonzero permanents make rank X=rank Y=1. Pure-permanent factorization forces each X edge to use colour e and each Y edge colour d. EVERY one of the four entries of C_Z=JX^T JYJ is then a sum of two nonzero distinct shared-c-group monomials. Thus all four entries are nonzero, contradicting its at-most-one-entry support.

All K_2,2 components are excluded. This reasoning only used edgewise orthogonality on the separate d'e' edge, never on the cycle itself, so it is not circular.

## 7. Return to the existing cofactor endpoint

With K_2,2 excluded, F consists of forests on at most four vertices and pure orientation triangles. Every edge product now vanishes by the already justified incidence systems. If F has a four-vertex star, it has at most four edges total: three in the star and at most one on the remaining two vertices. Otherwise every component has at most three vertices and the maximum is six edges, with equality only two disjoint triangles. Thus F has at most six edges, and six forces precisely those triangles.

The old nonzero-cofactor argument uses only entrywise orthogonality, pure nonzero permanents, and this edge-count equality characterization. A nonzero cofactor makes its own physical edge zero, forces its block invertible, then all three blocks invertible, hence all three cofactor blocks invertible and at least six support edges. The equality case is therefore two triangles and the complementary physical six-cycle, whose two pure matching monomials differ at every vertex and cannot cancel. This remains valid with four-vertex stars admitted, because the support cannot reach six edges when such a star exists. The all-zero branch is also excluded by the reusable fact.

## Integration requirements and evidence limits

The final theorem must explicitly replace the <=3 component claim by <=4 followed by K_2,2 exclusion; remove rank-one iff gamma=0 as a general assertion; remove root-axis purity from the pure-triangle setup; retain F as CROSS channels in C Q; and delay full edgewise orthogonality until K_2,2 is addressed. These are mathematical changes required for faithful integration, not editorial preferences.

The adjugate/common-null-support restrictions are no longer assumptions of this reviewed proof. Earlier narrow-case derivations may be retained only as remarks or history, not as hidden dependencies.

I independently checked the isotropy-to-rho classification, >=5 contradiction, both K_2,2 support patterns and exact gradient orientations, and removal of root purity from the pure-triangle proof. No computation or background process was needed or launched. This is an analytic adversarial reconstruction, not Lean verification and not a claim that finite checks alone prove the theorem. No original-witness candidate was found. Final edited theorem text still requires a focused integration read before promotion of that artifact.
