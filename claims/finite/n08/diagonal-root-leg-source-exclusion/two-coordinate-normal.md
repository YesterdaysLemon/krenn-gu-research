# Support-two common-plane source exclusion

**Proved analytic lemma over C, independently reviewed on 2026-09-04.** This is a proof leaf of the [complete parent theorem](../TWO_ROOT_DIAGONAL_LEG_SOURCE_EXCLUSION_THEOREM.md), not a global exclusion.

## 1. Exact scope and retained star

Use the full physical architecture in the [parent theorem](../TWO_ROOT_DIAGONAL_LEG_SOURCE_EXCLUSION_THEOREM.md) and the [published N8R2S theorem](../TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_THEOREM.md). Q,L_i,M_j are invertible; opposite root spokes are nonzero alpha_i Eii and beta_j Ejj; every physical AA and BB edge is a nonzero matrix unit. AB blocks are arbitrary. The opposite R image planes are unrestricted.

Suppose the three A-inactive images coincide in U with normal

  n=(n0,n1,0), n0*n1!=0.

Colour permutation covers any two-coordinate support. Let z_Ai be inactive and every B vector fully open. N8R2S supplies

  H=0, P0 C_AB+T C_BB=0.                            (1)

Choose the basis m=(n1,-n0,0), e2 of U, and represent the columns of P0 as independently arbitrary two-vectors x_i. Every local map from its binary A plane onto U is invertible. Write

  tau0=beta0*n0*z_B0[0], tau1=beta1*n1*z_B1[1],
  rho2=beta2*z_B2[2].

These are nonzero FULL B linear polynomials. Let X_ij be the physical AB edge with A_i inactive; p_i the inactive AA edge on the complementary A pair; q_j the FULL BB edge on the complementary B pair. Each p_i has bilinear rank at most one, possibly zero, and every q_j is nonzero. Write mu(a,b)_i=a_j*b_k+a_k*b_j on complementary row indices, so C_AB[:,j] is the corresponding unsigned two-column permanent vector plus p*q_j.

The hollow-kernel equation C_BB*(tau0,tau1,0)^T=0 and deleted-slot multidegrees give one polynomial lambda(A), independent of every B variable, with

  C_BB,01=0,
  C_BB,02=lambda*tau1,
  C_BB,12=-lambda*tau0.                             (2)

This star is RETAINED. Exact matching gives

  p^T X[:,0]=-lambda*tau0,
  p^T X[:,1]= lambda*tau1,
  p^T X[:,2]=0,
  H=per X+p^T X q=0.                               (3)

In the chosen U basis, the corrected source columns are

  P0 C[:,0]=-lambda*rho2*tau1*e_g,
  P0 C[:,1]= lambda*rho2*tau0*e_g,
  P0 C[:,2]=-lambda*beta0*beta1*z_B0[0]z_B1[1]*e_f,  (4)

where e_f,e_g are the two fixed basis vectors of U. In physical root coordinates e_f=m and e_g=e2.

We prove lambda=0. The [uniform zero-gauge exclusion](uniform-zero-gauge.md) then contradicts the full source for ANY normal support. That endpoint derives global C_AB=0 and the inactive p-support bound before choosing one common P-column vector and a torus annihilator; it does not discard the missing colour2 target.

All algebraic column combinations below take place over K=C(all FULL B coordinates). Rows remain linear in their own independent binary A variables, p_i retains complementary bilinear rank at most one, and every final conclusion is a polynomial identity. No invertibility assumption on an inactive R determinant is made.

## 2. Two audited algebraic lemmas and their exact use

### Kernel-column lemma

Let P=[x0,x1,x2] be the generic two-row sensor and k its signed 2-by-2 minor vector. Let a,b be two row-linear three-columns and p_i complementary bilinear forms of rank at most one. If

  p^T a=p^T b=0,
  mu(a,b)+q p=k d,

where q,d are field scalars independent of A variables, then d=0. This is valid for ANY q, including q=0.

The exact proof is Section 1 of [coordinate-normal.md](coordinate-normal.md). Its essential steps are: d!=0 excludes zero rows; a rank-one local row in a rank-two two-column matrix forces complementary p factors and contradicts the rank-two alternating target; all invertible local frames make the primitive kernel vector have rank-two minors, incompatible with rank-one p; when p=0, three common symmetric Gram pairings cannot be nonzero alternating pairings. For a rank-one two-column matrix, all rows share one direction; multiply the three equations by their local scalar factors and set all x_i equal. The Plucker vector vanishes, forcing the common symmetric coefficient zero, again contradicting a rank-two target. No inverse of q is used.

### Nonzero-q forcing lemma

Suppose in addition to

  p^T a=p^T b=0, mu(a,b)+q p=0, q!=0,

there is a row-linear column d with G=p^T d and one corrected source

  P[mu(d,b)+r p]=-eta G e,                          (5)

where eta!=0, e is a fixed nonzero two-vector, and r is arbitrary. Then G=0.

This is exactly the input used in Sections 2--5 of the audited support-one proof; it does not require any full permanent covariance or a second corrected column. Briefly, the two annihilation equations give the two mixed cubic coefficients of product_i(a_i s+b_i t) equal to zero. Under G!=0, a zero row forces p supported at that row, and (5) gives the rank-two/Cramer determinant contradiction. If all rows are nonzero, the mixed cubics exclude a rank-two local row. All rows therefore factor through one nonzero local form, with both scalar coefficients nonzero and all complementary p coefficients nonzero. Setting two local forms to zero in (5) forces the remaining d row to share its local factor. After dividing the product of the three local forms, independent variations along their kernels kill every coefficient on the left of (5), forcing G=0. These arguments retain r=0 and use q!=0 only in this second lemma.

### The valid combination

Put

  D=X[:,0], Y=tau1*X[:,0]+tau0*X[:,1], Z=X[:,2],
  qtilde=tau0*q0+tau1*q1.

Then (3) gives p^T Y=p^T Z=0. Moreover P0(C[:,0]*tau0+C[:,1]*tau1)=0, so its polynomial kernel form is k*dtilde for a field scalar dtilde. Bilinearity of the TWO-COLUMN permanent gives exactly

  mu(Y,Z)+qtilde*p=k*dtilde.

The kernel-column lemma forces

  mu(Y,Z)+qtilde*p=0,
  C[:,0]*tau0+C[:,1]*tau1=0.                       (6)

No claim is made that this column operation preserves a three-column permanent or any other source equation.

If qtilde!=0, apply (5) with a=Y,b=Z,d=D,r=q1,eta=rho2,e=e_g. Indeed its corrected column is the ORIGINAL physical column C[:,1]=mu(D,Z)+p*q1, and (4) says

  P0 C[:,1]=lambda*rho2*tau0*e_g
            =-rho2*(p^T D)*e_g.

The forcing lemma gives p^T D=0, hence lambda=0. It remains to exclude lambda!=0 with qtilde=0.

## 3. The qtilde=0 identities and exhaustive two-column cover

Assume lambda!=0 and qtilde=0. Deleted B degrees and nonzero FULL q0,q1 force

  q0=tau1*h(B2), q1=-tau0*h(B2), h!=0,              (7)

where h is one nonzero linear form. Equation (6) is mu(Y,Z)=0. Meanwhile the ORIGINAL physical H identity gives

  per X=2 lambda tau0 tau1 h!=0.                    (8)

Thus the original third column Z is nonzero.

Consider the rows v_i=(Y_i,Z_i), each linear in its own independent two-vector x_i. The condition mu(Y,Z)=0 says every pair has zero symmetric J pairing. If a local row has rank two, every other row is zero. Otherwise each nonzero row has one fixed direction over K. If two such directions are independent, no third nonzero row is orthogonal to both. If two directions are proportional, they must be isotropic, so one of the two columns is zero on all nonzero rows. Consequently the exhaustive cases are:

1. Z=0;
2. Y=0;
3. precisely two nonzero independent rows and one zero row;
4. only one nonzero row, with both columns nonzero there.

Three proportional nonzero rows are included in cases 1 or2. Rank zero is included in case1. This is a direct two-dimensional Gram classification, not a support census.

Case1 contradicts (8).

## 4. Two independent rows and one zero row

Let row i of (Y,Z) be zero, and rows j,k independent. From p^T Y=p^T Z=0, p_j=p_k=0. Nonzero p^T D=-lambda*tau0 makes p_i,D_i nonzero. In the original corrected column C[:,1], put

  F=D_j Z_k+D_k Z_j+p_i q1.

Equation (4) becomes

  x_i F+D_i[x_j Z_k+x_k Z_j+rho2 p_i e_g]=0.        (9)

Every bracketed coefficient and F is independent of x_i. A nonzero F would make the first term a rank-two linear map in x_i, while the second has rank at most one. Thus F=0, then the bracket is zero.

Let Delta=det[x_j,x_k], a nondegenerate irreducible bilinear polynomial. Cramer's identity gives

  Delta Z_k=-rho2 p_i (adj[x_j,x_k]e_g)_1.

The right side is nonzero. Delta divides neither rank-at-most-one p_i nor the displayed nonzero linear form; hence it cannot divide their product in the polynomial UFD. Contradiction. This case does not divide by qtilde.

## 5. Only one active row

Let i be the sole nonzero row of (Y,Z), with j,k the others. The annihilation p^T Z=0 gives p_i=0. Physical B separation in Y_j=Y_k=0 gives

  X_j0=tau0*l_j(Aj), X_j1=-tau1*l_j(Aj), X_j2=0,

and the same formulas for row k. The nonzero original permanent (8) forces l_j,l_k,Z_i nonzero. Expanding that permanent and using (7)--(8) gives

  l_j l_k Z_i=h(p_j l_j+p_k l_k),
  lambda=-(p_j l_j+p_k l_k).

Independent B2 variables and polynomial divisibility give

  Z_i=h z_i(Ai),
  p_j=l_k r_j(Ai), p_k=l_j r_k(Ai),
  z_i=r_j+r_k!=0.                                  (10)

For example reduction modulo l_k forces l_k to divide p_j; reduction modulo l_j gives the other factor. No nonzero p component is assumed in advance.

The entries of C[:,1] are now

  C_i1=0,
  C_j1=tau0 h l_k r_k,
  C_k1=tau0 h l_j r_j.

The corrected source (4), divided by the nonzero tau0*l_j*l_k, becomes

  h[r_k x_j/l_j+r_j x_k/l_k]
      =-rho2 z_i e_g.                              (11)

Fix Ai at a value with z_i!=0 and fix the B field parameters. Hold l_j=1 and vary x_j along its nonzero kernel direction. Since x_j is an independently arbitrary two-vector, (11) forces r_k=0. The corresponding variation at x_k forces r_j=0, contradicting z_i!=0. Thus case4 is impossible.

## 6. The Y=0 case: physical normal rows retained

The only remaining case is Y=0. Physical separation in B0,B1 gives

  X_i0=tau0*l_i(Ai), X_i1=-tau1*l_i(Ai)             (12)

on the A-INACTIVE/FULL-B slice. These are NOT assertions about the AB blocks with A normals opened. The normal rows W_(Ai,Bj)(e_i,-) may be arbitrary and will be retained.

Here lambda=-p^T l. In particular p!=0. Also P0 p!=0: otherwise its primitive generic two-row kernel would make p a constant multiple of the rank-two Plucker minors, incompatible with every p_i having bilinear rank at most one.

The original third cofactor column is

  C[:,2]=-2 tau0 tau1 (l_j l_k)_i+p q2.

Its corrected source (4) has all B0,B1 dependence in tau0*tau1. Since the polynomial vector P0p is nonzero and independent of all B variables, separation forces

  q2=eta*tau0*tau1, eta!=0.                        (13)

This is a FULL physical BB identity. Together with (7), every BB edge contains the own normal at B0 or B1.

### The decisive full t2*s2 target

Use original normal coordinates t_i=z_Ai[i], s_j=z_Bj[j], all unmentioned normal coordinates zero. At all A/B inactive, equations (7), (12), (13) imply

  C_AB,0=0,
  [s2]C_AB=0.                                     (14)

Every entry retains a factor tau0 or tau1, also after differentiating s2. The mixed hafnian coefficient h22=[t2*s2]H is zero as well. On B0,B1 inactive all three BB edges vanish; the outside hafnian is therefore just the AB permanent. Its columns0,1 vanish at every inactive A row. Opening only A2 can make entries in both columns nonzero only in that SAME row, whereas a permanent must assign the columns to distinct rows. Thus H is zero on this entire t2,s2 slice and

  h22=0.                                           (15)

Choose ONE noncoordinate v in U such that all available coordinates of a_i=L_i^(-1)v are nonzero. Such v exists by avoiding finitely many proper lines. Set all three inactive P columns to v. Choose ONE fully supported root covector m with m^T v=0 and keep it fixed during coefficient extraction. Existence follows because v is noncoordinate. In particular m2!=0, and a0[2]a1[2]!=0.

Project the FULL source by m and extract t2*s2. Terms carrying P0 are killed by m^T P0=0. Differentiated P terms multiply C_AB,0 or [s2]C_AB, which vanish by (14). The H term vanishes by (15), and T C_AB^T S has base C_AB,0=0. Exactly one term remains:

  beta2*m2*row_2([t2]C_BB)*R0^T.

Let

  g20(b0)=W_(A2,B0)(e2,b0),
  g21(b1)=W_(A2,B1)(e2,b1),

where b0,b1 remain on their actual inactive binary planes. These normal AB rows are NOT set to zero. Direct four-hafnian expansion gives

  row_2([t2]C_BB)
    =p2(a0,a1) (g21(b1),g20(b0),0).                 (16)

AA-normal derivative terms multiply the inactive X_i0 or X_i1 and vanish; only the p2 times actual AB-normal derivative remains. Thus the nonzero colour2 mixed target gives

  p2(a0,a1)[g21(b1) M0 b0+g20(b0) M1 b1]
     =gamma b0[2]b1[2] e2, gamma!=0.               (17)

If the evaluated p2 is zero, this is already impossible. Otherwise take b0=e1, a nonzero vector in ker e0 intersect ker e2. The right side vanishes. Since M0 e1!=0 and M1 restricted to ker e1 has rank two, the resulting identity forces g20(e1)=0 and g21 to vanish on the ENTIRE inactive B1 plane. This is only that restriction, not a claim about its full physical normal row.

Equation (17) now has just the g20(b0) M1 b1 term. Choose b0 with b0[2]!=0. If g20(b0)=0, its nonzero target is impossible. Otherwise the rank-two map M1|ker e1 would equal a nonzero rank-one map proportional to b1[2]e2. Contradiction.

This closes Y=0 through the MISSING normal colour2 with all AB-normal contributions retained. The earlier tempting full single-neighbour argument would have been invalid because (12) holds only on A inactive; it is not used here.

## 7. Conclusion and parent handoff

Every lambda!=0 case has been excluded: qtilde!=0 by the audited nonzero-q forcing lemma; qtilde=0 by the complete symmetric-zero two-column classification and Sections4--6. Therefore lambda=0, so C_BB=0 on the FULL A-inactive/B-open slice.

The uniform zero-gauge implication, proved in [uniform-zero-gauge.md](uniform-zero-gauge.md), excludes this for every normal support. It first proves global C_AB=0 and the p-support bound, then uses one common P-column specialization and one fixed torus annihilator for ALL THREE nonzero normal targets. Thus its application does not lose colour2 merely because the original n2=0.

This proves the support-two child under the explicit physical AA/BB matrix-unit hypotheses, with EVERY opposite R-plane configuration retained. It is an ingredient for the complete common-plane parent, not a separate profile PR and not a global Krenn--Gu proof. No inactive R determinant, nonzero inactive AA edge, nonzero qtilde, or nonzero lambda was assumed without its complementary case being handled. No full H=0 or full AB coordinate containment was inferred from a restricted slice.
