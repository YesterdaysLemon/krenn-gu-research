# Eight-vertex diagonal-root-leg common-plane reduction

**Proved exact source reduction over C, independently reviewed on 2026-09-04.** No computational certificate or Lean formalization is claimed.

The conclusion is a necessary reduction, not exclusion of the entire architecture and not a proof of global Krenn--Gu. Global status remains **UNRESOLVED**.

## 1. Exact statement

Work over C with a physical ternary block graph on eight vertices whose full perfect-matching tensor is Delta_(8,3). Name two root vertices r,s and split the other six into A_0,A_1,A_2 and B_0,B_1,B_2. Assume

    Q=W_rs is invertible,
    W_(r,A_i)=L_i,             W_(s,A_i)=alpha_i E_ii,
    W_(r,B_j)=beta_j E_jj,     W_(s,B_j)=M_j,          (1)

where all L_i,M_j are invertible and every alpha_i,beta_j is nonzero.

The outside AA, AB, and BB physical blocks are otherwise arbitrary. The theorem below does NOT assume those blocks are matrix units and does NOT assume a maximum torus-root cardinality. Those conditions are relevant to the parent application supplying this architecture, not to this implication once (1) is given.

Define the inactive root-image planes

    U_i=L_i(ker e_i^*), V_j=M_j(ker e_j^*).

Then:

1. At least one shore's three planes coincide:

       U_0=U_1=U_2  or  V_0=V_1=V_2.                (2)

2. If the U planes coincide, the FULL one-shore identities are

       H(A_inactive,B_full)=0,
       P_0 C_AB+T C_BB=0                            (3)

   on that slice.

3. If the V planes coincide, the symmetric FULL one-shore identities are

       H(A_full,B_inactive)=0,
       C_AB R_0^T+C_AA S=0.                         (4)

If both shores coincide, both conclusions apply. Their normals may have any coordinate support. No nonzero inactive determinant, nonzero hafnian, or nonzero normal coordinate is assumed in (3) or (4).

The matrices and physical cofactor conventions are defined next. Equations (3)--(4) do not imply H=0 when BOTH shores are activated simultaneously; that full-source residual remains open.

## 2. Exact matching identity and notation

Use independent local vectors z_Ai,z_Bj. Put

    P=[L_i z_Ai], R=[M_j z_Bj],
    t_i=z_Ai[i], u_j=z_Bj[j],
    S=diag(alpha_i t_i), T=diag(beta_j u_j).

Let H be the actual six-vertex outside matching tensor. Let C be its hollow symmetric matrix of actual four-vertex principal hafnians, indexed by outside vertices:

    C_uv=H_(outside vertices minus {u,v}) for u!=v,
    C_uu=0.

Write C_AA,C_AB,C_BB for its shore blocks, so C_BA=C_AB^T. Matching the roots either to each other or to two outside vertices gives the complete source

    H Q+P C_AB R^T+P C_AA S+T C_BB R^T+T C_AB^T S
      =diag(pure_0,pure_1,pure_2),                   (5)

where pure_c is the product of the six outside colour-c coordinates.

For example P C_AA S accounts for both roots meeting the A shore: C_AA is symmetric and the matrix product sums the two distinct root assignments for each unordered pair. No extra factor two is inserted. All cofactors come from the same outside graph, and the AA/BB correction sectors remain present whenever their transverse variables are active.

This is the [common-cofactor matching partition](../../arbitrary-order/RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md) and [uncontracted companion expansion](../../arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md). Here it also follows directly from the original perfect-matching definition.

## 3. Full one-shore factorization, including determinant-zero boundaries

Keep all B vertices inactive, u=0, but leave every A vector fully open. Then T=0, and every target pure product is killed by its inactive B_c factor. Equation (5) becomes

    H Q+P(C_AB R_0^T+C_AA S)=0.                      (6)

Taking determinants shows det P divides H^3. The FULL determinant det P is nonzero because the L_i are invertible and the three full columns are independently arbitrary. It is squarefree: it is multiaffine in the local coordinates, so no nonconstant irreducible factor can occur twice. Unique factorization therefore gives det P divides H. The vertex multidegrees of H and det P agree at every A mode, hence

    H(A_full,B_inactive)=det P(A_full) g(B_inactive)  (7)

for a polynomial g independent of all A coordinates.

Symmetrically,

    H(A_inactive,B_full)=f(A_inactive) det R(B_full)  (8)

for a polynomial f independent of all B coordinates.

Both facts hold even when either INACTIVE determinant vanishes identically. They require no division by H and make no claim that f or g is nonzero.

## 4. Inactive scalar and cofactor factorization when both determinants survive

Let P_0,R_0 be the inactive matrices, and set

    D_P=det P_0, D_R=det R_0,
    A=adj(P_0), B=adj(R_0), N=A Q B^T.

For this section alone suppose D_P and D_R are nonzero polynomials. On the fully inactive slice, S=T=0 and the target is zero, so

    H_0 Q+P_0 C_AB,0 R_0^T=0.                       (9)

Taking determinants gives D_P D_R divides H_0^3. Each inactive determinant is squarefree by multiaffinity; their variable sets are disjoint, so their product is squarefree. It follows that D_P D_R divides H_0. All six vertex multidegrees agree, so there is a scalar kappa in C, possibly zero, with

    H_0=kappa D_P D_R,
    C_AB,0=-kappa A Q B^T=-kappa N.                  (10)

The cofactor identity follows first on the nonempty determinant open and then as a polynomial identity. This is a pointwise implication for each fixed physical coefficient array satisfying the written nonzero-polynomial conditions; no physical coefficient specialization is discarded.

## 5. Universal mixed-normal adjugate identity

The following identity is polynomial and valid without assuming D_P D_R!=0. Define

    d_i=[t_i]det P, e_j=[u_j]det R,
    h_ij=[t_i u_j]H,
    psi_i=prod_(outside vertices other than A_i,B_i) z[i],

where coefficient extraction sets every other transverse variable to zero. All unmentioned local coordinates remain the independent inactive variables. Continue to write A,B,N for the inactive adjugates and their product above.

Multiply the FULL source (5) on the left by adj(P) and on the right by adj(R)^T. Extract entry (i,j)'s coefficient t_i u_j. The exact result is

    h_ij N_ij+
      (d_i e_j+alpha_i beta_j A_ij B_ji)(C_AB,0)_ij
       =delta_ij psi_i A_ii B_ii.                   (11)

The indexing is important. The physical cofactor C_AB,ij omits A_i and B_j, so it is independent of both selected normal variables. Row i of adj(P) omits column A_i, and row j of adj(R) omits B_j. Hence N_ij is also independent of the selected variables. The C_AA correction can select t_i only through its zero diagonal C_AA,ii; the C_BB correction similarly selects C_BB,jj=0. The surviving doubly transverse term is exactly alpha_i beta_j A_ij B_ji C_AB,ij. The target contributes only when i=j.

This is genuine local-vector coefficient extraction from the full source, not differentiation of graph entries treated as independent parameters.

Under the nonzero D_P D_R hypothesis, substitution of (10) gives, for ALL kappa including zero,

    N_ij [h_ij-kappa d_i e_j-kappa alpha_i beta_j A_ij B_ji]
       =delta_ij psi_i A_ii B_ii.                   (12)

## 6. The mixed-normal identities exclude the entire nondegenerate class

A determinant of three independently variable vectors in three two-dimensional subspaces of C^3 is identically zero exactly when all three planes coincide. One direction is immediate. For the other, suppose U_i differs from U_k, and let j be the remaining index. Choose v_i in U_i outside U_k. The two planes U_j,U_k have a nonzero intersection; choose nonzero v_j there. Choose v_k in U_k outside the line C v_j. Then v_j,v_k are independent in U_k and v_i lies outside that plane, proving the determinant polynomial is nonzero.

Since D_P!=0, the U planes are not all equal, and at most one of their three pair-equality conditions can hold. The same is true on the V shore. Therefore some omitted index i has BOTH complementary U planes distinct and BOTH complementary V planes distinct.

The cross-product coefficient map of two distinct two-dimensional planes spans all C^3. To see this directly, use a basis in which the planes are span(e_1,e_2) and span(e_1,e_3). The wedge coordinates of (alpha,beta,0) and (gamma,0,delta) are

    (beta delta,-alpha delta,-beta gamma),

three independent polynomials. Independent changes of parameters in the planes preserve this coefficient rank.

Thus row i of A and row i of B have coefficient spans of dimension three. Let U,V be their 3-by-4 coefficient matrices on the complementary two-vertex shores. The A-shore|B-shore coefficient flattening of N_ii is

    U^T Q V,

which has rank three: U^T is injective, Q invertible, and V surjective. In particular N_ii is nonzero. Also A_ii and B_ii are nonzero, because the cofactor rows span all C^3. The factor psi_i is a nonzero product of surviving inactive coordinate functions. Therefore the right side of (12) for this i is nonzero.

But (12) asserts that N_ii divides a nonzero separated-shore product

    F(A_variables) G(B_variables)=psi_i A_ii B_ii.

In the combined polynomial UFD, every irreducible factor of this product depends on only one shore. (A prime in one shore's polynomial ring remains prime after adjoining the other shore's variables.) Hence N_ii itself must be a product N_A(A)N_B(B), up to a nonzero scalar. Such a polynomial has shore flattening rank one, contradicting rank three.

Therefore D_P D_R!=0 is impossible. By the plane/determinant equivalence above, at least one shore's three inactive image planes coincide. This proves (2), with every kappa value covered uniformly.

## 7. Uniform vanishing on a coincident shore

Assume U_0=U_1=U_2 and choose a nonzero normal n. No support condition is imposed on n. Equation (8) supplies

    H(A_inactive,B_full)=f(A)det R(B_full).

On this slice S=0 and the target is zero. Contract (5) on the left by n. Since n^T P_0=0, then multiplying by R^(-T) and transposing gives the polynomial identity

    C_BB t=-f(A) adj(R) w,
    t_j=beta_j n_j z_Bj[j], w=Q^T n!=0.              (13)

The calculation first uses the nonempty FULL R determinant open; the displayed equality is polynomial and holds identically. It does not require a nonzero INACTIVE determinant of R.

For distinct j,k, let l be their complement. The actual cofactor C_BB,jk leaves the three A vertices and only B_l. Hence it is one linear form G_l(B_l), with coefficients depending on A. Component l of (13) is

    t_j(B_j)G_k(B_k)+G_j(B_j)t_k(B_k)
       =plus-or-minus f(A)det(w,M_j B_j,M_k B_k).    (14)

Suppose f is not zero and fix an A assignment with f(A)!=0. Use x_j=M_j B_j as independent coordinates, which is legal because each M_j is invertible. The three right sides of (14) are nonzero scalar multiples of one common 3-by-3 skew-symmetric matrix J_w of rank two.

Let T_j be the 3-by-2 matrix of coefficient vectors of the two linear forms t_j,G_j in the x_j coordinates. Their pair forms are

    T_j J_+ T_k^T=lambda_jk J_w,
    J_+=[[0,1],[1,0]], lambda_jk!=0.                 (15)

Every T_j has rank two because every right side has rank two. Moreover column(T_j)=column(J_w), since each pair's column space is contained in column(T_j) and both have dimension two. Thus these frames lie in ONE common two-dimensional plane. Choose a basis matrix U for that plane. Since J_w is skew, its row plane is the same, and it factors as

    J_w=U J_2 U^T

for a nonzero invertible 2-by-2 skew matrix J_2. Write T_j=U F_j with all F_j invertible. Applying a left inverse of U and its transpose to (15) gives

    F_j J_+ F_k^T=lambda_jk J_2                     (16)

for all three pairs.

The first two equations make F_1 and F_2 proportional. Their mutual Gram matrix is consequently symmetric, being a scalar multiple of F_1 J_+ F_1^T. But (16) says it is a nonzero skew matrix. This is impossible over C. Therefore f=0.

This argument includes normals with zero coordinates: if n_j=0, then t_j=0 and T_j has rank at most one, already contradicting (15). It also includes identically zero cofactor linear forms, which likewise cannot provide rank two. No normal-coordinate or cofactor denominator has been introduced.

We have proved H(A_inactive,B_full)=0. The full source on this slice now reads

    (P_0 C_AB+T C_BB)R^T=0.

The FULL determinant of R is a nonzero polynomial, so multiplying by its adjugate and using the integral domain gives P_0 C_AB+T C_BB=0. This proves (3).

Transposing the two shores gives (4). In particular both conclusions hold when both triples of inactive planes coincide.

The forced common two-plane in (15) is essential. No false claim is made about arbitrary 2-by-3 frames with a symmetric 3-by-3 middle form. Here the middle form is 2-by-2, and the common image plane is forced by the rank-two skew target.

## 8. Interpretation, evidence, and retained boundary

This theorem uses only the full source and architecture (1). It requires neither rank-one AA/BB blocks nor a maximum-root condition after that architecture is assumed. In the current parent programme, adjacent degree-four invertible centres supply (1) by the source and root arguments in Section 9; this theorem does not prove that every witness has such centres.

The output is one universal source reduction: any witness in this architecture must reach a coincident inactive-image shore, and every such shore obeys the exact zero-hafnian/matrix equations (3) or (4). All determinant-zero branches, all normal supports, and both simultaneous coincidences are retained. The nonzero three-colour target when both shores are activated has not been shown inconsistent on that final boundary.

In particular, zero H on each one-shore slice is NOT asserted to imply H_FULL=0, and no dead-edge erasure is applied from that weaker premise. The scalar-factorization countercontrols do not satisfy the full corrected matrix equations used in Section 7; they are not counterexamples to this reduction.

The proofs are pointwise in complex physical coefficients. Auxiliary variable opens are used only to establish polynomial identities, never to discard physical parameter fibres. No solver, support-profile enumeration, numerical sampling, or Lean formalization is part of this proof.

The [recorded parent attempt](../../../docs/strategy/astra-source-residual-parent-2026-09-04.md) explains the source-supply obligation and retained boundary. No new external-literature premise is used.

## 9. Exact parent application at maximum root cardinality two

Let H3 be the graph of invertible physical blocks in a hypothetical
eight-vertex GHZ witness with maximum torus-root cardinality two. If H3
has adjacent vertices of degree four, they supply exactly architecture
(1), so the source reduction above applies. This is a conditional
application; no such adjacent vertices are asserted to exist.

First, H3 is triangle-free. Otherwise name the three invertible blocks
Q(x,y), L(x,z), M(y,z). For every product-torus point with Q(x,y)=0,
the common kernel of the two z rows has no torus point. Thus the product
of the three components of their cross product vanishes there. The
rank-three bilinear Q is irreducible and has a dense torus part, so one
cross-product component is divisible by Q. Both have bidegree (1,1),
making that component a constant multiple of Q. Its coefficient matrix
has rank at most two, whereas Q has rank three; the multiple is zero.
But this component cannot vanish identically when L and M are invertible:
their two-coordinate row projections are both surjective. This is a
contradiction.

Second, at a vertex with four invertible incident blocks, the other
three blocks are nonzero scalar E00, E11, E22, in some neighbour order.
The [three-colour killer theorem](../../arbitrary-order/THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md)
supplies a nonzero single-column block for each remote colour. These
three distinct blocks exhaust the noninvertible neighbours. Write the
unique colour-c one as b_c(x) z[c]. If b_c is not proportional to x[c],
choose a generic x in ker b_c with x[c]!=0. Each invertible neighbour
maps this two-dimensional plane to a two-dimensional row space, so its
row is generically not on the coordinate-c line. The other two
single-column neighbours have different labels and also cannot block c.

At the killed colour-c neighbour put e_c. At every other neighbour choose
a vector in its incident-row kernel with colour-c coordinate nonzero.
Every matching vanishes at the original vertex, but the anchored target
has one nonzero colour-c product. This full-source contradiction proves
b_c is a nonzero multiple of x[c]. Boundary x vectors are legitimate in
this direct anchored argument; no torus hypothesis is imposed on x here.

Now let r,s be adjacent degree-four vertices in H3. Their three other
H3 neighbours are disjoint by triangle-freeness, exhausting all six
outsiders. Each root's remaining three blocks are the diagonal units
just proved. Label A_i by the colour of its unit to s, and B_j by the
colour of its unit to r. Their other root blocks are invertible, giving
(1) with nonzero alpha_i,beta_j. No assumption about outside-block
support is required for the source reduction.

## 10. Evidence and replay

The [independent mathematical review](../../../docs/audits/TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_REVIEW_2026-09-04.md)
checks the exact source, all nine normal identities, the polynomial
factor argument, the forced two-dimensional Gram representation, and
the parent application. The proof is analytic and pointwise.

The [primary integer replay](verify_diagonal_root_leg_source.py) checks
27 displayed mixed-normal identities using three explicit physical
graphs, including both determinant-zero configurations. It reconstructs
the actual full matching tensor by scalar subset recursion and uses
arbitrary dense outside blocks. These finite checks corroborate indexing
and matching algebra; they do not prove the quantified source reduction.
The fixtures are not GHZ witnesses: the replay uses their actual root-open
tensor on the right side of the general matching identity.

```text
python claims/finite/n08/verify_diagonal_root_leg_source.py
```

The live implication is a common-plane and vanishing-one-shore reduction
for the stated root configuration, including all its determinant cases.
The surviving corrected cofactor equations, arbitrary rank-three
components, lower-rank source graphs, and the global conjecture remain
open. This is not an exclusion of the whole root configuration.
