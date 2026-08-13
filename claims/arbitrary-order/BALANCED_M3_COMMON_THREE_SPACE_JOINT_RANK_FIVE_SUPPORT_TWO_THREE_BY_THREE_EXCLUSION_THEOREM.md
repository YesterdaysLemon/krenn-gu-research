# Balanced m=3 common-three-space joint-rank-five support-two (3,3) exclusion

## Status

**Exact characteristic-zero exclusion of the transverse joint-rank-five
support-two (3,3) involved-row profile.**  Let U be the total singleton span
of a normalized, target-consistent physical m=3 common shore whose complete
four-column sensor has full function-field rank.  Assume

~~~text
dim U=3,                         rank H=5.             (1)
~~~

Retain the transverse two-root branch of S2AG.  Thus the two nonzero
root--root blocks have disjoint derivative summands, the third-root row has
rank two, and the kernel of that row has target-coordinate support exactly
two.  If both involved root rows have rank three, then the physical full-sensor
conditions are inconsistent.

The proof does not assume that either root--root block is monomial, rank one,
separable, tangent, generic, or invertible.  The support contraction first
puts the relation three-plane on an invertible graph.  The two contracted
diagonal targets force that graph to preserve the supported coordinate plane.
The contracted full target equation then places every singleton correction in
the binary diagonal plane spanned by T_0 and T_1.  Permanent symmetry forces
the remaining graph column onto colour two.  The complete uncontracted target
table consequently gives a rank-one T_2 square and three mixed polarized maps
whose images lie in the binary diagonal plane.  A diagonal-plane strengthening
of the S2AI common-zero atlas makes the alternating singleton determinant
vanish, contradicting full sensor rank.

This theorem does **not** exclude a support-one third-row kernel, any of the
three Hilbert--Burch coordinate atlases, joint rank at most four, another
S2T/S2Q component type, a rank-one or pair-plane pole stratum, a higher order,
the all-rank-drop branch, or the global conjecture.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The support-two relation plane is an invertible graph

Use the transverse notation of S2AG.  After permuting roots,

~~~text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (2)
~~~

There are a three-plane P and a two-plane N_3 such that

~~~text
K=P direct-sum N_3,
P subset A_1 direct-sum A_2,
U=D_(B,C)(P).                                        (3)
~~~

Write the transposed root-row maps as

~~~text
rho:A_1^*->W^*,        pi:A_2^*->W^*,
theta:A_3^*->W^*,      W=X direct-sum Y direct-sum Z. (4)
~~~

In the present profile,

~~~text
rank rho=rank pi=3,             rank theta=2,
ker theta=span(eta),            |support eta|=2.     (5)
~~~

Projection of P to either involved root is therefore an isomorphism.  Write

~~~text
P={(a,L a):a in A_1},                    L in GL(A_1,A_2).
                                                               (6)
~~~

Let

~~~text
r_a=rho(e_a^*),       p_b=pi(e_b^*),       q_c=theta(e_c^*).
                                                               (7)
~~~

Duality with the graph gives the exact row relation

~~~text
p_b=sum_i L_(b,i) r_i.                               (8)
~~~

Relabel the two supported colours and, if necessary, exchange the involved
roots.  S2AG gives nonzero scalars beta and chi such that

~~~text
eta=eta_0 e_0^*+eta_1 e_1^*,        eta_0 eta_1!=0,

b_eta=(id tensor eta)(B)=beta e_0,
c_eta=(id tensor eta)(C)=chi e_1.                   (9)
~~~

Contracting U by eta gives

~~~text
eta(U)={beta a tensor e_0+chi e_1 tensor L a:a in A_1}. (10)
~~~

The colour-one diagonal in (10) has a preimage proportional to e_1.
Consequently, for a nonzero scalar nu,

~~~text
L e_1=-(beta/chi)e_0+(nu/chi)e_1.                   (11)
~~~

For the colour-zero diagonal, write a=e_0+t e_1 plus any component outside
span(e_0,e_1).  Projection in the first factor removes that outside
component.  Cancellation of the e_1 first-factor row and (11) then force

~~~text
L e_0=alpha e_1,                  alpha!=0.           (12)
~~~

Indeed the required preimage is

~~~text
a=e_0-(alpha chi/nu)e_1.                            (13)
~~~

The nonvanishing of alpha and nu follows from invertibility of L and the two
nonzero diagonal targets.  No entry of the third graph column has yet been
restricted.

## 2. The kernel contraction fixes the correction plane

Use the graph basis

~~~text
u_i=D_(B,C)(e_i,L e_i)=e_i tensor B+C tensor L e_i,
i=0,1,2.                                             (14)
~~~

Write the full physical target equation coefficientwise as

~~~text
G_N-J=S_0 u_0+S_1 u_1+S_2 u_2,                      (15)
~~~

where the S_i are tensors in the three nonroot target factors.  Put

~~~text
T_i=X_i tensor Y_i tensor Z_i,
D_01=span(T_0,T_1).                                  (16)
~~~

Since q_eta=0, contraction of (15) in the third root gives, for all root rows
(a,b),

~~~text
-eta_0 delta_(a,0)delta_(b,0) T_0
-eta_1 delta_(a,1)delta_(b,1) T_1

 =beta delta_(b,0) S_a
  +chi delta_(a,1) sum_i L_(b,i)S_i.                 (17)
~~~

Rows (0,0), (2,0), and (1,1), together with (11)--(12), give

~~~text
S_0=-(eta_0/beta)T_0,
S_2=0,

S_1=(chi alpha eta_0/(beta nu))T_0
    -(eta_1/nu)T_1.                                  (18)
~~~

All four displayed coefficients are nonzero where they occur.  In
particular,

~~~text
S_0,S_1,S_2 in D_01.                                 (19)
~~~

Thus the freedom that invalidated the isolated two-slice argument in the
preceding mixed-row theorem is not arbitrary at a physical (3,3) point: the
complete kernel contraction confines it to one fixed binary diagonal plane.

## 3. Permanent symmetry fixes the third graph column

For u,v,q in W^*, write

~~~text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (20)
~~~

For each third-root row c, form the 3 by 3 tensor matrix

~~~text
F_c(a,b)=M_(r_a,p_b)(q_c).                           (21)
~~~

If S_c(a,i)=M_(r_a,r_i)(q_c), then S_c is symmetric and (8) gives

~~~text
F_c=S_c L^T,                 L F_c=L S_c L^T symmetric. (22)
~~~

Take the coefficient of T_2 in F_2.  Equation (15), (18), and the pure
target show that this scalar coefficient matrix is exactly E_(2,2).  Hence

~~~text
L E_(2,2) is symmetric.                              (23)
~~~

Equations (11)--(12) already give L_(2,0)=L_(2,1)=0.  Symmetry in (23) gives
the other two off-diagonal entries in the third column:

~~~text
L_(0,2)=L_(1,2)=0.                                   (24)
~~~

Since L is invertible, for some ell!=0,

~~~text
L e_2=ell e_2.                                       (25)
~~~

The row relations are now

~~~text
p_0=-(beta/chi)r_1,
p_1=alpha r_0+(nu/chi)r_1,
p_2=ell r_2.                                         (26)
~~~

This use of permanent symmetry is coefficientwise.  It does not assume that
the full tensor matrix F_2 is diagonal.

## 4. The complete target table lands in two transverse diagonal planes

Evaluate (15) at all third-root rows q_c.  Because (18) lies in D_01 and
because L_(2,0)=L_(2,1)=0, the root pair (2,2) has no singleton correction:

~~~text
ell M_(r_2,r_2)(q_c)=delta_(c,2)T_2.                (27)
~~~

The vectors q_0,q_1 are nonzero proportional vectors, q_2 supplies the
second direction, and Q=image theta is a two-plane.  Therefore

~~~text
M_(r_2,r_2)|_Q has rank one with image span(T_2).    (28)
~~~

For a=0,1, the root pair (a,2) has no GHZ target.  Every surviving singleton
term is one of the S_i, so (25)--(26) give

~~~text
M_(r_0,r_2)(Q) subset D_01,
M_(r_1,r_2)(Q) subset D_01.                         (29)
~~~

Finally p_0=-(beta/chi)r_1.  The root pair (0,0) has only the possible
colour-zero target T_0, and all its corrections lie in D_01.  Hence

~~~text
M_(r_0,r_1)(Q) subset D_01.                         (30)
~~~

Every entry of B and C not fixed by (9) remains arbitrary.  Equations
(27)--(30) use the complete target equation, not a selected quotient or a
finite sample.

## 5. A binary-diagonal-plane common-zero lemma

### Lemma 1

Let K be a characteristic-zero field and W=X direct-sum Y direct-sum Z.
Choose linearly independent triples x_i in X, y_i in Y, z_i in Z and put

~~~text
T_i=x_i tensor y_i tensor z_i,       i=0,1,2,
D_01=span(T_0,T_1).                                  (31)
~~~

Let V=span(u_0,u_1,v) be a three-plane and Q a two-plane with
V intersect Q=0.  Suppose

~~~text
M_(v,v)|_Q has rank one with image span(T_2),        (32)

M_(u_0,v)(Q) subset D_01,
M_(u_1,v)(Q) subset D_01,
M_(u_0,u_1)(Q) subset D_01.                         (33)
~~~

Then the alternating separated tensor

~~~text
A_XYZ(u_0,u_1,v)
 =sum_(sigma in S_3) sign(sigma)
   (w_(sigma(1)))_X tensor
   (w_(sigma(2)))_Y tensor
   (w_(sigma(3)))_Z                                 (34)
~~~

vanishes, where (w_0,w_1,w_2)=(u_0,u_1,v).

### Proof

A pure v has zero square, so v has two or three nonzero source components.

If v=x+y has two components, (32) makes x, y, and the one-dimensional
projection of Q to Z the three factor lines of T_2.  Every M_(v,u)(q) lies in

~~~text
x tensor Y tensor Z + X tensor y tensor Z.           (35)
~~~

The plane D_01 has zero intersection with (35), because its two generators
use factor lines different from those of T_2 in both X and Y.  The first two
inclusions in (33) therefore strengthen to

~~~text
M_(u_0,v)|_Q=M_(u_1,v)|_Q=0.                        (36)
~~~

If v=x+y+z has three components, a decomposable tensor in the Segre tangent
image of the square shares at least two base factor lines.  Permute sources
so that T_2=x tensor y tensor t.  Quotienting the square identity by x and
then by y shows that every q in Q has q_X in span(x) and q_Y in span(y).
Thus (35) again contains every M_(v,u)(q), and the same transverse-plane
intersection proves (36).

It remains to inspect the exact common-zero atlas proved in S2AI.

For v=x+y, the nonconjugate chart has a one-dimensional common-zero space.
The conjugate chart with a nonzero tangent term either makes u_0,u_1
dependent or puts the square-kernel vector in V intersect Q.  In the fully
conjugate chart, choose

~~~text
w=x-y,          Q=span(w,t),
u_i=a_i w+z_i,  z_i in Z.                            (37)
~~~

Direct expansion gives

~~~text
M_(u_0,u_1)(w)
 =-2 x tensor y tensor (a_0 z_1+a_1 z_0),

M_(u_0,u_1)(t)
 =-2 a_0 a_1 x tensor y tensor t,

A_XYZ(u_0,u_1,v)
 =2 x tensor y tensor (a_1 z_0-a_0 z_1).             (38)
~~~

The first two tensors lie in D_01 by (33), but
D_01 intersects x tensor y tensor Z only at zero.  They vanish.  Since
characteristic is zero, their two scalar-vector equations make the last
tensor in (38) vanish.

For v=x+y+z, let a square-kernel vector be

~~~text
q_0=(a x,b y,c z),                 a+b+c=0.           (39)
~~~

When abc!=0, every common zero divisor has the scaling form

~~~text
u=(lambda x,mu y,nu z),       a lambda+b mu+c nu=0.  (40)
~~~

The scalar triples for u_0,u_1,v lie in one two-plane, so (34) vanishes.
If one coefficient in (39) is zero, the remaining common-zero equations have
dimension at most one, except for the exact exceptional chart in which every
solution is pure in one source.  The former makes u_0,u_1 dependent and the
latter also makes (34) zero.  These are the exhaustive two- and three-source
charts of the S2AI atlas.  Therefore (34) vanishes in every case.  QED.

## 6. Exclusion of the (3,3) profile

Put

~~~text
V=span(r_0,r_1,r_2),             Q=image theta.       (41)
~~~

Since rho has rank three, V is a three-plane.  The S2AG row-space splitting
and rank H=5 give

~~~text
dim Q=2,                         V intersect Q=0.      (42)
~~~

Equations (27)--(30) satisfy Lemma 1 with

~~~text
(u_0,u_1,v)=(r_0,r_1,r_2).                           (43)
~~~

Hence

~~~text
A_XYZ(r_0,r_1,r_2)=0.                                (44)
~~~

On the other hand, D_(B,C)|_P is injective.  In the graph basis (14), the
generic determinant of the three separately linear physical singleton
columns is exactly A_XYZ(r_0,r_1,r_2), multiplied by the nonzero determinant
of that basis change.  Full sensor rank therefore requires

~~~text
A_XYZ(r_0,r_1,r_2)!=0.                               (45)
~~~

This contradiction proves

~~~text
rank H=5, transverse two-root derivative rank 6,
rank theta=2 with support-two kernel,
involved row profile (3,3):                         IMPOSSIBLE. (46)
~~~

## 7. Proof-topology consequence

The transverse rank-five support-two branch is now

~~~text
involved rows (2,2):                                  IMPOSSIBLE (S2AI);
involved rows (3,2)/(2,3):                            IMPOSSIBLE (S2AJ);
involved rows (3,3):                                  IMPOSSIBLE (here);

third-row kernel support one:                         OPEN;
three-root Hilbert--Burch coordinate atlases:         OPEN;
joint rank at most four / other physical branches:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (47)
~~~

This closes the support-two involved-row census only.  It does not promote
the common-three-space stratum, S2, or the global conjecture to a proof.

## Focused replay

Run from repository root:

~~~text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_three_by_three_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_three_by_three_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_three_by_three_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_three_by_three_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_three_by_three_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_three_by_three_exclusion.py
~~~

The primary verifier checks the symbolic graph contractions, correction
tensors, coefficientwise permanent-symmetry step, complete target-plane table,
transverse-plane intersections, and every displayed common-zero atlas
identity.  The independent audit imports no repository module and no
third-party package; it rebuilds the graph and sparse tensor identities with
standard-library Fraction arithmetic and a separate index convention.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Support-two (2,2) complete exclusion and common-zero atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [Support-two mixed-row-rank exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_MIXED_ROW_RANK_EXCLUSION_THEOREM.md)
