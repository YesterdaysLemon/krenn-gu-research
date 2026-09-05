# Uniform common-plane synthesis: a nonzero BB cofactor gauge is necessary

**Proved analytic lemma over C, independently reviewed on 2026-09-04.** This is a proof leaf of the [complete parent theorem](../TWO_ROOT_DIAGONAL_LEG_SOURCE_EXCLUSION_THEOREM.md), not a global exclusion.

## Exact parent and retained inputs

Use the [parent statement](../TWO_ROOT_DIAGONAL_LEG_SOURCE_EXCLUSION_THEOREM.md). The physical eight-vertex source has invertible Q,L_i,M_j, nonzero spokes alpha_i E_ii,beta_j E_jj, and six nonzero physical AA/BB matrix units. AB blocks are arbitrary. By the [accepted N8R2S reduction](../TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_THEOREM.md), after exchanging shores the three inactive P-image planes coincide in U with nonzero normal n, and

    H(A_inactive,B_FULL)=0,
    P_0 C_AB+T C_BB=0,
    T=diag(beta_j z_Bj[j]).                          (1)

All cofactors are the actual physical four-hafnians. The normal n is allowed support three, two, or one. This note does not assume its entries are nonzero.

The uniform conclusion proved below is conditional but useful: a full source in this common-plane architecture cannot have C_BB identically zero on (1). The coordinate-normal and two-coordinate-normal proofs then force those same gauges to zero. Each case therefore closes through this one uniform contradiction. The missing root-colour equations are recovered through a new auxiliary torus projection, not by pretending n has nonzero coordinates.

## 1. Vanishing C_BB would force vanishing C_AB

Assume temporarily C_BB=0 throughout A_inactive,B_FULL. Then P_0 C_AB=0. Choose one basis of U and write x_i in C^2 for the independent coordinates of L_i z_Ai on the inactive A_i plane. Let v_i be the signed complementary two-by-two minors of [x_0,x_1,x_2]. Their gcd is one and their vertex multidegrees imply

    C_AB=v(x) d(B)^T,

where d is independent of all A variables. Put p_i for the inactive AA edge on the complementary A pair, q_j for the FULL nonzero BB edge on the complementary B pair, and X_ij for the physical AB edge restricted only at A_i. Exact matching gives

    p^T X=0, per X=0, peradj(X)=v d^T-p q^T.        (2)

Each p_i has bilinear rank at most one; every q_j is a nonzero polynomial.

The independently audited cofactor lemma proves d=0 from precisely these inputs, without any support condition on n or any inactive R determinant condition. A short proof is included to identify the required common two-plane.

Row Euler equations and p^T X=0 give sum_i v_i(Xd)_i=0. The local Plucker syzygy makes (Xd)_i=x_i^T y(B). Individual row Euler equations then equate v_i(x_i^T y), rank two in the other A pair when nonzero, to p_i(Xq)_i, rank at most one there. Hence y=0 and Xd=0.

If d!=0, all row coefficient vectors of X lie in one common two-plane ker d over the B fraction field. Each two-column permanent cofactor is therefore a symmetric two-by-two Gram form on three binary A frames. Combining q_k times cofactor column j with minus q_j times column k cancels p and gives three nonzero alternating pair forms if q_kd_j-q_jd_k!=0. Their rank forces invertible two-by-two frames and middle form; the first two pair equations make two frames proportional, so the last Gram is symmetric rather than nonzero skew. Thus d=rho q.

Normalize columns Z_ij=q_j X_ij. Its rows sum to zero. Every entry of cofactor row i is s_i=(q_0q_1q_2)(rho v_i-p_i), nonzero because rank v_i=2 and rank p_i<=1. Two rows a,b of Z then satisfy

    ab^T+ba^T=s_i(ones-3I).

The fixed right matrix has rank two. Fixing one nonzero row, injectivity of b -> ab^T+ba^T makes the other two rows proportional; their mutual symmetrized product has rank at most one, contradiction. Therefore d=0, and

    C_BB=0 implies C_AB=0                           (3)

throughout the same full one-shore slice.

## 2. Recover all three target colours at one rank-one P specialization

Assume both cofactor blocks in (3) vanish identically. The old support-three proof used the actual plane normal n as its root contraction; that loses colours when n has zeros. Instead choose one generic vector x in U and set

    a_i=L_i^(-1)x in ker e_i,
    P_0(a_0,a_1,a_2)=[x,x,x].                        (4)

Choose x to avoid finitely many proper linear subspaces of U so that:

- both available inactive coordinates of every a_i are nonzero;
- every nonzero inactive AA matrix-unit restriction and every nonzero first-normal AA restriction remains nonzero at these a values;
- every nonzero inactive AB edge polynomial retains a nonzero B-linear specialization;
- x is not proportional to a coordinate vector.

All these choices are possible. Each inactive coordinate is a nonzero linear functional on U, each nonzero matrix-unit restriction is a product of such functionals, and a nonzero AB restriction has a nonzero coefficient linear functional. A two-dimensional U is not a finite union of lines. No physical coefficient array is discarded.

Since x is noncoordinate, its annihilator contains a fully-supported vector m. Fix one such m, so

    m^T x=0, m_0 m_1 m_2!=0.                         (5)

The SAME values a_i and the SAME torus vector m are used for all three subsequent normal derivatives. It is not necessary that m annihilate all of U; it annihilates the specialized columns in (4).

## 3. Exact projected first-normal source at this specialization

Put r_j(B_j)=M_j B_j, tau_j=beta_j m_j B_j[j], w=Q^T m. Let q_j be the full BB edge on the other two B ports. For complementary {j,b,c} define

    K_j(B_b,B_c)=q_j w+tau_b r_c+tau_c r_b.

Use the specialized inactive AB rows X_lj(a_l,B_j) and define

    Phi_l(B)=sum_j X_lj(a_l,B_j) K_j,
    Xi_i(B)=sum_j W_(Ai,Bj)(e_i,B_j)[tau_b r_c+tau_c r_b].

Let d_(i,k)=W_(Ai,Ak)(e_i,a_k), k!=i, and let p_i be the inactive AA edge on the complementary A pair, evaluated at (4). Differentiate the FULL source in t_i=z_Ai[i] at the fixed A values (4), with B fully open, and contract root r with the fixed m. The exact vector identity is

    sum_(k!=i) d_(i,k) Phi_l+p_i Xi_i
      =m_i prod_(h!=i) a_h[i] prod_j B_j[i] e_i,     (6)

where l is the third A index in each summand.

Why the projection is valid: m^T P_0=0 at (4) kills P_0 times every cofactor derivative and the C_AA S term. The identically zero C_AB block kills the P derivative contribution and the T C_AB^T S contribution. The remaining T C_BB derivative is physical and includes p_i times the normal AB row; this is the Xi_i term and is retained. No derivative of m or of the chosen a-values is taken.

Every right side of (6) is nonzero, because m is torus and the two available coordinates at each a_h were chosen nonzero. Thus all three root-colour targets are available despite zeros in the actual common normal n.

## 4. The two possible inactive AA situations

The equations C_AB=C_BB=H=0 imply

    per X=0, peradj(X)=-p q^T.

They force at most one inactive AA edge p_i to be a nonzero polynomial. This is the already audited algebraic lemma, which applies before specialization. For completeness normalize Z_ij=q_j X_ij. Active cofactor rows are constant across their three entries and their corresponding Z rows sum to zero. If exactly two p entries are nonzero, those two rows have zero mutual symmetrized products and must include a zero row, contradicting the other nonzero cofactor rows. If all three survive, their pair symmetrized products are nonzero multiples of ones-3I; the same injectivity argument used above makes two rows proportional, contradicting the remaining rank-two pair. Hence only support zero or one is possible. The choice (4) preserves this zero/nonzero distinction for the physical unit restrictions.

### No surviving inactive AA edge

If p=0, each nonzero target in (6) requires a first-normal AA edge at its own index. A physical matrix unit can serve at most one endpoint at first normal order: it must use that endpoint's own coordinate and an inactive coordinate at the other end. Three edges serving three vertices therefore form a directed three-cycle. Each equation in (6) has one summand and forces one Phi_l to be a nonzero scalar multiple of prod_j B_j[i]e_i. The three rows l receive three different root directions.

All two-by-two permanents of X vanish. Its polynomial support is a row star, a column star, or contained in one two-by-two rectangle: two disjoint nonzero entries force the full rectangle by the permanent equation; its nonzero ordinary determinant then kills the third row and column through the other zero-permanent equations. With no disjoint entries, the support is a star. This is an algebraic zero-minor classification, not an enumeration.

A row star or two-by-two rectangle misses an A row, so its Phi_l is zero. In a column star j, all Phi_l equal X_lj(a_l,B_j) times the SAME root-vector/two-B tensor K_j. They cannot have three different nonzero fixed root directions e_i. Both alternatives contradict (6).

### One surviving inactive AA edge

Suppose only p_k survives, on the edge between the other two A vertices i,j. That edge is inactive at both endpoints and serves neither first-normal target i or j. Their equations in (6), with p_i=p_j=0, force respectively the other two AA edges to be normal at i and j and inactive at k. Thus neither serves a first-normal k response. The k-th equation becomes

    p_k Xi_k=nu prod_j B_j[k]e_k, nu!=0.             (7)

Since p_k is a nonzero scalar at (4), this would require

    sum_j x_j(B_j)[tau_b r_c+tau_c r_b]
      =nu' prod_j B_j[k]e_k, nu'!=0,                (8)

for arbitrary linear forms x_j and invertible r_j, with all tau_j nonzero coordinate-j functionals.

Identity (8) is impossible. Restrict B_k to ker B_k[k]. Its target and tau_k vanish, leaving

    r_k(B_k)F+x_k(B_k)G=0,
    F=tau_i x_j+tau_j x_i, G=tau_i r_j+tau_j r_i.

The rank-two restriction of r_k forces F=0; otherwise fixing F!=0 would express that map as rank at most one. G is nonzero, so x_k=gamma tau_k. Separation gives x_i=lambda tau_i,x_j=-lambda tau_j. The full expression is now

    tau_k[(gamma+lambda)tau_i r_j+(gamma-lambda)tau_j r_i].

On the plane ker tau_i, coordinate k is nonzero as a functional. After fixing the other B values with their required coordinates nonzero, this would make either a rank-two restriction of r_i or the zero map equal a nonzero rank-one map along e_k. Contradiction.

Thus the last AA situation is impossible.

## 5. Uniform conclusion

The temporary hypothesis C_BB=0 gives C_AB=0, then the common-vector/torus-projection argument obtains all three nonzero normal targets and excludes both possible AA situations. Therefore every full source in the stated common-plane architecture must retain

    C_BB not identically zero on A_inactive,B_FULL.   (9)

This conclusion is independent of the support of the actual plane normal n. The support-three case is then immediately excluded because C_BB*(beta_j n_j B_j[j])=0 with three nonzero entries forces C_BB=0. In support two or one, the explicit hollow-star/free-edge kernel gauges must be genuinely nonzero; any full-source argument killing them invokes this same uniform contradiction.
