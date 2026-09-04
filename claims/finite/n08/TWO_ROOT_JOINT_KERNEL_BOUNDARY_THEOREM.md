# Eight-vertex invertible-root joint-kernel boundary

**Proved exact analytic exclusion and necessary boundary over C, independently reviewed on 2026-09-04.** Global Krenn--Gu remains UNRESOLVED. No computational certificate or Lean formalization is claimed.

## Parent, exact child, and residual

The parent is to supply SOME common-coordinate root pair in an n=8 complex ternary GHZ witness with maximum torus-root cardinality two, or directly exclude its exceptional incidence types. The downstream consumer is the proved N8R2C theorem in [the complete common-coordinate owner](TWO_ROOT_COMMON_COORDINATE_COMPLETION_THEOREM.md).

This note attacks the following exact child. Let roots 1,2 have invertible physical block Q=W_12. For each of the six outside vertices u let

    P_u(z)=W_1u(-,z), R_u(z)=W_2u(-,z),
    L_u=ker P_u intersect ker R_u.

Assume L_u contains a nonzero vector k_u having EXACTLY ONE zero coordinate c(u), with its other two coordinates nonzero. The claim is that these assumptions, full GHZ source, and maximum torus-root cardinality two are inconsistent.

No kernel dimension is enlarged by assumption. A line Ck_u is used as a line until a physical common-column port has actually been derived. The proof then uses one binary anchor per group, rather than asserting two independent binary modes everywhere.

This excludes the entire all-one-zero-kernel branch at an invertible root pair, including mixed common-column/noncoordinate-plane ports. It leaves a sharp necessary residual: every invertible candidate root pair must have some outside joint kernel equal to zero or containing no vector with exactly one zero coordinate (under maximum-root saturation, the nonzero remaining possibility is a coordinate axis). It does not handle these remaining ports, root blocks of lower rank, or arbitrary n.

The proof uses direct matching identities and the [complete common-coordinate theorem](TWO_ROOT_COMMON_COORDINATE_COMPLETION_THEOREM.md). The [parent attempt](../../../docs/strategy/astra-root-supply-parent-2026-09-04.md) records the upstream supply, synthesis, controls, and downstream gap. External literature is not a premise.

## 1. Exact source and paired kernel labels

Let B be the outside six-set. Write h=H_B for its actual physical matching tensor and C_uv=H_(B-{u,v}) for its actual four-cofactors. The full root matrix identity is

    h(z) Q+sum_(u<v) C_uv(z)
       [P_u(z_u)R_v(z_v)^T+P_v(z_v)R_u(z_u)^T]
       =diag(prod_u z_u[0],prod_u z_u[1],prod_u z_u[2]).  (1)

All root slots remain open, and all outside variables are independent. This is the original perfect-matching partition through the root partners.

Set all outside slots to k_u. Every incidence term vanishes. If any colour is absent among the c(u), its target pure product is nonzero, while present colours are killed. At least one label is present, so the resulting nonzero diagonal matrix has rank at most two. It cannot equal a scalar multiple of invertible Q. Hence every colour occurs.

If some colour c occurs only once, activate its unique port on e_c and keep the other five at their k vectors. At most one port can meet a root, so again the incidence sum vanishes. The target is a nonzero multiple of E_cc because every other k has nonzero coordinate c. This is also impossible. Therefore the six vertices are partitioned into three pairs B_c={u,v} by their unique zero coordinate.

## 2. The full two-port channel factors through the assigned coordinates

Fix B_c={u,v}, allow z_u=z and z_v=w to vary arbitrarily in C^3, and keep the other four vertices at their k vectors. Their root incidences vanish, leaving

    h_c(z,w)Q+f_c K_uv(z,w)=d_c z[c]w[c] E_cc,        (2)

where

    K_uv(z,w)=P_u(z)R_v(w)^T+P_v(w)R_u(z)^T,
    f_c=H_(B-B_c)(k), d_c=prod_(x outside B_c)k_x[c]!=0.

The scalar f_c is nonzero: otherwise evaluation at z[c]=w[c]=1 would make a scalar multiple of Q equal a nonzero rank-one matrix. Thus

    K_uv(z,w)=gamma(z,w)Q+delta_c z[c]w[c] E_cc,
    delta_c=d_c/f_c!=0, gamma=-h_c/f_c.               (3)

The channel has matrix rank at most two for every z,w. Its determinant vanishes as a polynomial, and the exact rank-one update expansion gives

    0=gamma^2 [gamma det Q+delta_c z[c]w[c] adj(Q)_cc].

The polynomial ring C[z,w] is an integral domain. Hence gamma is zero, or

    gamma=-(delta_c adj(Q)_cc/det Q) z[c]w[c].

Consequently

    K_uv(z,w)=z[c]w[c] M_c,
    M_c=gamma_c Q+delta_c E_cc!=0, rank M_c<=2,        (4)

for a constant gamma_c. This is a full physical two-port tensor identity, not a scalar-contraction statement.

## 3. At least one physical common-column anchor per pair

If u is not a common-column port for c, choose z in ker e_c^* with (a,b)=(P_u(z),R_u(z))!=(0,0). Equation (4) gives, for every w,

    a R_v(w)^T+P_v(w)b^T=0.                          (5)

If both a,b are nonzero, (5) forces P_v(w)=a ell(w), R_v(w)=-b ell(w) for one linear functional ell. It is nonzero, since otherwise the full channel in (4) would vanish. Substituting into the nonzero full identity (4) shows ell is proportional to e_c^*: on ker e_c^*, a nonzero ell would force the remaining nonzero matrix factor to vanish. Thus both P_v and R_v are supported in column c.

If a!=0,b=0, then R_v=0. The remaining nonzero channel is P_v(w)R_u(z')^T; (4) forces P_v supported on w[c]. The case a=0,b!=0 is symmetric. These arguments retain zero individual maps. Therefore at least one member of every B_c is a physical common-column port.

Choose one such member U_c as the anchor. Let V_c be its mate. For the rest of the proof use the actual inactive spaces

    S_(Uc)=ker e_c^* (dimension two),
    S_(Vc)=C k_(Vc)  (dimension one).                 (6)

Both physical root maps vanish on each space. The line mate has nonzero restrictions of each of the two coordinates different from c. The anchor has those two coordinate functionals linearly independent.

## 4. An exact constant channel graph without a generic-coefficient assumption

For each fixed physical W, choose auxiliary ACTIVE vectors z_u^* with z_u^*[c(u)]=1 so that:

- a_u=P_u(z_u^*) is zero iff the physical map P_u is zero;
- b_u=R_u(z_u^*) is zero iff the physical map R_u is zero;
- K_uv(z_u^*,z_v^*) is zero iff the physical two-port channel K_uv is identically zero.

Such a simultaneous choice exists over C. There are finitely many nonzero map/channel polynomials to avoid. A nonzero homogeneous linear map, or separately homogeneous bilinear channel, cannot vanish identically on the affine slices z_u[c(u)]=1, because each such slice spans its full vector space. Choosing a nonzero entry of each nonzero map/channel gives finitely many nonzero polynomials; their nonvanishing opens have nonempty intersection. This choice is auxiliary and pointwise in W. It excludes no physical coefficient stratum.

By (4), the evaluated same-pair channels are still exactly M_c=gamma_c Q+delta_c E_cc. Define F on cross-group pairs by zero evaluated channel. It is precisely the graph of IDENTICALLY ZERO physical two-port channels.

Since Q has rank three and every channel has rank at most two, any nonzero cross channel is independent of Q. For same-pair channels, rank one is equivalent to gamma_c=0 and M_c=delta_c E_cc. Every port has at least one nonzero physical map, because M_c!=0.

### Every F component has at most three vertices

For the evaluated vectors a_u,b_u, ports with b=0 form one clique and ports with a=0 another. These are physical first-root-only and second-root-only orientations by the auxiliary choice. Each clique has at most one vertex per natural pair, and there are no F links to both-leg ports or to the opposite pure orientation.

A both-leg zero channel forces proportional a directions and proportional b directions. Components have fixed projective directions and opposite nonzero scalar ratios, hence are complete bipartite. Same-pair vertices cannot occupy opposite sides because M_c!=0.

If a component contains both vertices of B_c, their same-side M_c is rank one, so its common a,b directions are e_c. A vertex of another group d then makes M_d supported in row c or column c. It cannot be rank one (that would be E_dd), so gamma_d!=0. Deleting row and column c gives the corresponding Q submatrix as a nonzero multiple of E_dd. A member of the third group e would require the same submatrix to be a nonzero E_ee multiple, impossible. Nor can both d vertices occur, since then M_d would be rank-one E_cc. Thus the component has at most three vertices. A component without a doubled pair trivially has that bound.

Every bipartite component has nonzero signed multiplicity for each represented group; its only possible triangles are the physical pure-orientation cliques, with one vertex per group.

## 5. Physical cofactor labels on the actual 2D/1D spaces

Let A_uv be the actual physical outside edge restricted to S_u x S_v from (6). Work in the polynomial ring in the three anchors' six independent coordinates and the three independent scalar line variables. This ring is an integral domain. The mate coordinate functionals are k_(Vc)[d] times its scalar variable, with k_(Vc)[d]!=0 for d!=c.

All root incidences vanish on these inactive spaces. Every colour is killed by its own pair, so (1) gives

    H:=haf(A)=0.                                     (7)

Activate one same-group pair on its coordinate axes and let all other slots vary on their spaces S. The channel is M_c by (4), and Q,M_c are independent. Therefore the actual four-cofactor is

    f_c:=C_(B_c)=delta_c^(-1) prod_(w outside B_c) z_w[c]!=0.  (8)

For a cross pair, activate its two slots at the auxiliary z^* vectors and leave all others on S. The target is zero. If uv is not in F, its nonzero channel is independent of Q, so

    C_uv=0 on the inactive complement whenever uv is not in F.  (9)

These are labelled physical cofactor identities on exactly the chosen spaces. No missing binary coordinate has been invented at a line mate.

## 6. Stress with one binary anchor per group

Set t_c=A_(B_c) f_c and t_uv=A_uv C_uv for uv in F. Exact hafnian partner expansion at u in B_c gives

    t_c+sum_(v:uv in F) t_uv=0.                       (10)

For c!=d, the anchor in the third group e carries coordinate c in every monomial of t_c and coordinate d in every monomial of t_d. These are independent variables at that anchor, and the unknown within-group edge factors omit it. Thus t_0,t_1,t_2 still have pairwise disjoint monomial support. The line mate contributes nonzero scalar-coordinate factors and cannot erase this distinction.

Signed summation over each bipartite F component therefore kills t_c for all its represented groups. Unless F is two pure-orientation triangles, every group has a vertex in a bipartite component. Thus all t_c vanish outside that exception.

### The pure two-triangle exception has full common-column supply

The auxiliary evaluation preserved physical zero maps. In the two-triangle case, each B_c contains one physical first-root-only port u and one physical second-root-only port v. Its full paired channel (4) is

    P_u(z) R_v(w)^T=z[c]w[c] M_c.

This nonzero outer-product tensor forces P_u supported on z[c] and R_v supported on w[c]. (For example w[c]=0 forces R_v(w)=0, since P_u is not zero.) Therefore BOTH ports of every pair are physical common-column ports. The accepted N8R2C theorem applies to the same graph, named invertible root block, and unchanged maximum root cardinality two. It excludes this exceptional configuration.

This invocation is a legal use of the named downstream consumer; it does not infer binary independence at a line mate. The current proof derives its entire incidence premise on this branch.

Outside that excluded exception, all t_c=0. The nonzero f_c in the integral ring force

    A_(B_c)=0.

The remaining component incidence equations in (10) kill every t_uv by leaf elimination on edges/stars and the nonsingular triangle incidence matrix. Together with (9), this gives

    A_uv C_uv=0 for every cross-group pair.           (11)

## 7. Physical cofactor contradiction with line mates retained

Let X,Y,Z be the 2-by-2 cross-edge matrices between groups 01,02,12. They are matrices of actual restricted edge polynomials, on endpoint spaces of dimension two or one as specified in (6). The within-group cofactors and direct matching formulas give

    per X=f_2, per Y=f_1, per Z=f_0, all nonzero,
    H=sum_(i,j,k) X_ij Y_(1-i,k) Z_(1-j,1-k)=0,
    C_X=JYJZ^T J, C_Y=JXJZJ, C_Z=JX^T JYJ,
    J=[[0,1],[1,0]].                                 (12)

The scalar matrix-rank arguments are unchanged by endpoint dimensions, but the factor argument needs its precise one-anchor justification.

### One-anchor factor lemma

If X has rank one over the fraction field, then

    X00 X11=X01 X10=(per X)/2!=0.

Every entry is nonzero. Unique factorization and endpoint multidegrees force each entry to be a nonzero constant multiple of its pure coordinate-2 endpoint product. At a line endpoint, this coordinate is a fixed nonzero multiple of the line variable; at an anchor it is the genuine indicated binary coordinate. The same conclusion holds for Y with coordinate 1 and Z with coordinate 0.

If X,Y are rank one, an entry of C_Z contains two nonzero terms using the opposite coordinate-2/coordinate-1 assignments at their shared group-0 pair. At its anchor these are two distinct independent coordinates. At its line mate both coordinate values are nonzero multiples of the line variable. Thus the two terms have different anchor monomials with nonzero coefficients and cannot cancel. Every entry of C_Z is nonzero. Only ONE binary anchor in the shared group was required. The other orientations are identical.

### Both cofactor-rank alternatives fail

If all cross cofactors vanish, their product identities in (12) and nonzero permanents force X,Y,Z rank one. The one-anchor factor lemma contradicts the zero cofactor blocks.

If some cross cofactor is nonzero, (11) kills its physical edge. Say it lies in X. Then det X=plus-or-minus per X!=0. If Y were rank one, all its entries would be nonzero; entrywise Y*C_Y=0 would force C_Y=0, and invertible X would force Z=0 in (12), impossible. Hence Y is invertible, and similarly Z is invertible.

All three cofactor matrices are invertible and their support has at least six edges. It lies in F, whose connected components have at most three vertices. The only possibility is exactly two disjoint triangles, with one vertex from every group in each triangle. Their six actual edges vanish by (11). The two surviving entries of each cross block are nonzero by its permanent, and the surviving graph is the complementary six-cycle.

Each pure permanent is now the product of its two surviving edges. Unique factorization and endpoint multidegrees again give the omitted-colour factors. The six-cycle has exactly two perfect matchings. At every anchor its two incident edges go to the two different other groups and use different available coordinates. Hence the two matching monomials differ at all THREE binary anchors. Line-mate factors remain nonzero scalar multiples of their line variables. The two nonzero matching monomials cannot cancel, contradicting H=0.

This excludes both alternatives and completes the conditional proof.

## Scientific status and precise next boundary

The proof is pointwise in W and uses only finite auxiliary open choices, exact source coefficients, and physical polynomial identities. It does not promote a generic physical graph result to a witness statement. No scalar kernel line was treated as a binary plane. The binary spaces were supplied by the full two-port factor identity, one anchor per colour pair.

The conclusion is conditional on an invertible root block and a joint-kernel vector with exactly one zero coordinate at EACH outside vertex. The off-source no-kernel/common-plane controls do not satisfy the full labelled source identities used here. Conversely they show why this result alone cannot close the parent: a witness might still force a zero-dimensional joint kernel or a coordinate-axis joint kernel at some port of every invertible root pair. Those cases require further full-source work, not an assumed extension of this proof.

## Necessary boundary for every invertible physical edge

In a hypothetical witness satisfying the stated n=8 and maximum-r=2
hypotheses, every invertible physical edge has an outsider whose joint
kernel is either zero or a coordinate axis.

Indeed, an invertible bilinear block has a product-torus zero: choose a
torus vector at one endpoint with a noncoordinate row at the other, then
choose a torus vector in that row's kernel. Thus it is a usable root pair.
A joint kernel cannot contain a torus vector, since that would extend the
pair to a root triple. A linear subspace contained in the union of the
three coordinate hyperplanes is contained in one of them. Consequently a
nonzero joint kernel is a coordinate hyperplane, a coordinate axis, or a
line with exactly two nonzero coordinates. The first and third types
contain a vector with exactly one zero coordinate. If every outsider had
one of those two types, the exclusion above would apply. The asserted zero
or coordinate-axis outsider is therefore necessary.

This boundary does not assert that an invertible edge exists. Graphs with
all physical blocks of rank at most two remain outside this theorem. It
also supplies no exclusion of the zero-kernel or coordinate-axis cases.
The global conjecture and general eight-vertex maximum-r=2 branch remain
unresolved.

Independent review: [exact-text mathematical audit](../../../docs/audits/TWO_ROOT_JOINT_KERNEL_BOUNDARY_REVIEW_2026-09-04.md). The proof is analytic; the earlier common-coordinate replay checks shared displayed cofactor identities and is not a proof of the new supply implication.
