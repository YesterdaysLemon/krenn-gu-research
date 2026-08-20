# Four-root determinant-divisor rank-two core and rank-one singleton-triangle exclusion

## Status

**Proved exact characteristic-zero follow-up.  The focused primary verifier,
genuinely independent no-import audit, and
[hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_REDUCTION_REVIEW_2026-08-20.md)
pass.**

Start with an actual hypothetical ternary GHZ witness over \(\mathbb C\)
whose maximum-cardinality torus root has order four and surplus two.  Fix the
same residual pair \(Q\) supplied by GLS4 and assume that all six same-\(Q\)
pair-response tensors vanish identically.  The preceding determinant-divisor
reduction leaves a rank-two exactly-two-active-port conformal core and three
rank-one branches.  This theorem proves two exact exclusions.

1. The complete contracted six-slot target excludes the whole rank-two core.
   Six labelled two-slot quotients give an exhaustive support-cover argument.
   The \((1,1),(2,1),(1,2)\) active-port dimension profiles fail directly.
   In the \((2,2)\) profile, conformal orthogonality forces two opposite
   symplectic graph planes and makes \(B_{st}\) rank two, while the final
   target quotient forces the same edge to be a coordinate rank-one tensor.
2. The common four-root incidence realization excludes the rank-one
   Branch-III singleton monomial triangle.  Splicing one active incidence
   column from each of its three pure complementary permanents creates a
   concise weighted restriction \(P_4\to\Delta_3\), contradicting the exact
   fourth-order permanent subrank obstruction.

The first exclusion does not use any common-root relation among the
companions.  The second does: a formal triangle with independently declared
companions remains an exact sharp control.  Neither result treats rank-one
Branch I, Branch II, or the Branch-III two-port identity.  The separate
seventh-response quartic, weaker response-zero patterns, nonzero-response
absorption and exceptional fibres, every named downstream selector package,
the supply-and-target-attachment strategic node, and the global conjecture
remain **OPEN**.  The global Krenn--Gu status is **UNRESOLVED**.

## 1. Source, complete target, and inherited determinant-divisor branches

Let \(K\) be a characteristic-zero field.  The actual-witness application is
over \(K=\mathbb C\).  Every local covector space is three-dimensional with
fixed target coordinate covectors

~~~text
E_v=V_v^*,
e_(v,0)^*, e_(v,1)^*, e_(v,2)^*.                       (1)
~~~

Let

~~~text
Omega=R disjoint-union B,        |R|=4,        |B|=6,
Q={q_0,q_1} subset B,            U=B-Q,        |U|=4.   (2)
~~~

The pair \(Q\) is the same physical pair supplied by GLS4.  Put

~~~text
X=E_(q_0),             Y=E_(q_1),
H=H_Q in X tensor Y,
A_u=H_(q_0,u) in X tensor E_u,
C_u=H_(q_1,u) in Y tensor E_u,
B_uv=H_(u,v) in E_u tensor E_v.                        (3)
~~~

All slots are labelled.  Tensor products below use the unique canonical
shuffle into their named slots.  The six pair-response identities are

~~~text
Z_uv
 =H boxtimes B_uv+A_u boxtimes C_v+A_v boxtimes C_u
 =0                         for every {u,v} subset U.   (4)
~~~

For each pair \(P\subset B\), let \(\Pi_P\) be its four-root complementary
permanent tensor on \(B-P\).  The complete contracted target is

~~~text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(c=0)^2 mu_c product_(v in B)e_(v,c)^*,
mu_0 mu_1 mu_2!=0.                                     (5)
~~~

This is the full \(3^6=729\)-coefficient equality.

The preceding
[determinant-divisor reduction](FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md)
proves that rank zero is absent for the GLS4 pair, GLS10 excludes rank three,
and ranks one and two have the exact forms recalled next.

### 1.1 Inherited rank-two core

Assume \(\operatorname{rank}H=2\), and put

~~~text
L=L(H) subset X,              M=R(H) subset Y.          (6)
~~~

The inherited theorem gives

~~~text
A_u in L tensor E_u,          C_u in M tensor E_u.      (7)
~~~

For \(u\in U\), define

~~~text
Phi_u:V_u -> L direct-sum M,
z |-> (A_u(-,z),C_u(-,z)),
W_u=im Phi_u.                                           (8)
~~~

Exactly two ports have nonzero \(W_u\).  Name them \(s,t\), and name the two
inactive ports \(m,n\):

~~~text
{u:W_u!=0}={s,t},                 U={s,t,m,n}.          (9)
~~~

Both projections \(W_u\to L,M\) are injective for \(u=s,t\), and

~~~text
d_u=dim W_u in {1,2}.                                  (10)
~~~

The conformal response equation says

~~~text
Xi_st=A_s boxtimes C_t+A_t boxtimes C_s
      =H boxtimes D_st,             B_st=-D_st,         (11)
~~~

where, for any \(\theta_H:L\otimes M\to K\) with
\(\theta_H(H)=1\),

~~~text
D_st=(theta_H tensor id_(E_s tensor E_t))(Xi_st).       (12)
~~~

All blocks meeting \(m\) or \(n\) vanish.  Equations (6)--(12), rather than
their proof, are the source interface for the first exclusion.

### 1.2 Inherited rank-one singleton triangle

On rank-one Branch III with singleton support \(\{t\}\), let

~~~text
T=U-{t},                         |T|=3.                 (13)
~~~

The inherited theorem gives three distinct colours \(i,j,k\), nonzero
\(\alpha,\beta,\gamma\), and the exact physical blocks

~~~text
H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*,
A_t=alpha e_(q_0,i)^* tensor e_(t,i)^*,
C_t=beta  e_(q_1,j)^* tensor e_(t,j)^*,                (14)
~~~

with every other \(A,C,B\) block zero.  The complete target splits into

~~~text
alpha Pi_(q_0,t)
 =mu_i e_(q_1,i)^* tensor product_(v in T)e_(v,i)^*,

beta Pi_(q_1,t)
 =mu_j e_(q_0,j)^* tensor product_(v in T)e_(v,j)^*,

gamma Pi_Q
 =mu_k e_(t,k)^* tensor product_(v in T)e_(v,k)^*.      (15)
~~~

Unlike arbitrary formal companion tensors, the physical companions in (15)
come from one common family of four-root incidence maps.  That fact is the
source interface for the second exclusion.

## 2. The rank-two active \(K_4\) and its two-slot target quotients

Put

~~~text
A_4={q_0,q_1,s,t}.                                     (16)
~~~

For \(v\in A_4\), define the incident coefficient-support spaces

~~~text
R_(q_0)=L subset E_(q_0),          R_(q_1)=M subset E_(q_1),
R_u=im(Phi_u^*) subset E_u                   (u=s,t).   (17)
~~~

### Lemma 1 (every active edge is supported on the four incident spaces)

For \(u=s,t\),

~~~text
dim R_u=d_u,
rank A_u=rank C_u=d_u.                                 (18)
~~~

Every possibly nonzero outside physical edge has both endpoints in \(A_4\)
and has its \(v\)-shore contained in \(R_v\) at each endpoint.  In
particular,

~~~text
L(B_st) subset R_s,                R(B_st) subset R_t. (19)
~~~

Every physical edge meeting \(m\) or \(n\) is zero.

#### Proof

The dual map \(\Phi_u^*:(L\oplus M)^*\to E_u\) has the same rank as
\(\Phi_u\), proving \(\dim R_u=d_u\).  The two coordinate projections of
\(W_u\) are injective, so the maps \(A_u:V_u\to L\) and \(C_u:V_u\to M\)
both have rank \(d_u\).

The support assertions for \(H,A_s,C_s,A_t,C_t\) follow from (6)--(8).
Formula (12) expresses \(B_{st}\) as a linear combination of products of
local coefficient rows of those four blocks, proving (19).

At an inactive port \(v\in\{m,n\}\), \(W_v=0\) means \(A_v=C_v=0\).
Substitution in (4), first with one inactive endpoint and then with two,
gives \(H\boxtimes B_{uv}=0\).  Since \(H\ne0\), every such \(B\)-block is
zero. \(\square\)

For each active vertex define the exact coordinate-containment set

~~~text
Gamma_v={c in {0,1,2}:e_(v,c)^* belongs to R_v}.       (20)
~~~

Thus \(|\Gamma_v|\le\dim R_v\).

### Lemma 2 (labelled two-slot support-cover quotient)

Choose any two-set

~~~text
D={v,w} subset A_4,             P=A_4-D={a,b}.         (21)
~~~

Let

~~~text
rho_v:E_v -> E_v/R_v,          rho_w:E_w -> E_w/R_w.  (22)
~~~

The companion \(\Pi_P\) has labelled slots \(D\cup\{m,n\}\).  Define

~~~text
bar Pi_P^D
 =(rho_v tensor rho_w tensor id_m tensor id_n)Pi_P.    (23)
~~~

Then the complete target (5) implies the exact labelled equality

~~~text
H_P boxtimes bar Pi_P^D
 =sum_(c notin Gamma_v union Gamma_w) mu_c
   sh_(P,D,{m,n})(
     e_(a,c)^* tensor e_(b,c)^*
     tensor rho_v(e_(v,c)^*) tensor rho_w(e_(w,c)^*)
     tensor e_(m,c)^* tensor e_(n,c)^*
   ).                                                   (24)
~~~

Put

~~~text
N_D=|{0,1,2}-(Gamma_v union Gamma_w)|.                 (25)
~~~

Then:

1. \(N_D\ge2\) is impossible.
2. If \(N_D=1\), with sole surviving colour \(c\), then

   ~~~text
   H_P in K^*(e_(a,c)^* tensor e_(b,c)^*).             (26)
   ~~~

3. If \(H_P\) has matrix rank two, then

   ~~~text
   N_D=0,
   Gamma_v union Gamma_w={0,1,2}.                      (27)
   ~~~

No conclusion about \(\bar\Pi_P^D\) is asserted when \(N_D=0\).

#### Proof

Apply \(\rho_v,\rho_w\) in their labelled slots of (5).  By Lemma 1, every
nonzero physical edge incident to \(D\) dies.  Every edge meeting \(m\) or
\(n\) is zero.  The unique active edge disjoint from \(D\) is \(P\), which
gives the left side of (24).  On the target side, colour \(c\) survives
exactly when neither coordinate covector lies in the corresponding incident
space, proving (24).

Flatten (24) across

~~~text
P | (D union {m,n}).                                   (28)
~~~

The left side has rank at most one.  The \(P\)-side pure tensors on the
right are linearly independent as the colour varies.  The opposite-side
tensors are also linearly independent: every displayed quotient factor is
nonzero by its indexing condition, and the two inactive labelled tags

~~~text
e_(m,c)^* tensor e_(n,c)^*                             (29)
~~~

separate the three colours even if quotient classes in (22) are
proportional.  Since every \(\mu_c\ne0\), the right flattening rank is exactly
\(N_D\).  This excludes \(N_D\ge2\).

If \(N_D=1\), both sides are nonzero simple tensors across (28).
Uniqueness of their factor lines gives (26).  A rank-two \(H_P\) cannot
satisfy (26), so only \(N_D=0\) remains in that case, proving (27).
\(\square\)

Lemma 2 consumes the complete labelled tensor equality.  It is not a
pure-shell or Hamming-one argument.

## 3. Exhaustion of the four active-port dimension profiles

The final profile uses the following complete conformal-plane
classification.

### Lemma 3 (full-plane \(\beta\)-orthogonality)

Let \(L,M\) be two-dimensional and let \(H\in L\otimes M\) have rank two.
Choose bases in which \(H=I_2\), and define

~~~text
beta((x,z),(y,w))
 =[x w^T+y z^T] in Mat_2(K)/K I_2.                    (30)
~~~

Let two-dimensional subspaces \(W_s,W_t\subset L\oplus M\) have both
coordinate projections injective and satisfy

~~~text
beta(W_s,W_t)=0.                                       (31)
~~~

Then there are invertible matrices \(\mathsf T,\mathsf S\) with

~~~text
W_s=graph(mathsf T),              W_t=graph(mathsf S), (32)
~~~

and a scalar \(q\in K^*\) such that, for

~~~text
J=[[0,1],[-1,0]],
~~~

one has

~~~text
mathsf T=qJ,                       mathsf S=-qJ.        (33)
~~~

For all \(x,y\in K^2\),

~~~text
x(mathsf S y)^T+y(mathsf T x)^T
 =-q det(x,y) I_2.                                     (34)
~~~

#### Proof

The injective projections from a two-plane to two-dimensional \(L,M\) are
isomorphisms, giving the graphs in (32) with both matrices invertible.
Write

~~~text
mathsf T=[[p,q],[r,t]],            mathsf S=[[a,b],[c,d]]. (35)
~~~

Condition (31) says, for every \(x,y\in K^2\),

~~~text
x(mathsf S y)^T+y(mathsf T x)^T in K I_2.              (36)
~~~

Equate the two off-diagonal entries to zero and the difference of the two
diagonal entries to zero, coefficient by coefficient in
\(x_1,x_2,y_1,y_2\).  The complete solution is

~~~text
p=t=a=d=0,             r=-q,             b=-q, c=q.    (37)
~~~

Thus (33) holds.  Invertibility of \(\mathsf T\) gives \(q\ne0\); this
nonzero is derived, not assumed.  Direct substitution gives (34).
\(\square\)

### Theorem 4 (the complete target excludes the rank-two core)

Over characteristic zero, no data satisfying (1)--(12) and the complete
target (5) exist.  In particular, the rank-two double-contained survivor of
the preceding determinant-divisor reduction is empty on the actual complex
witness locus.

Once (6)--(12) are supplied, this conclusion remains valid with arbitrary
labelled tensors in place of the companions \(\Pi_P\).  It uses no
common-root permanent relation, no nonzero \(\Pi_Q\), and none of the fixed
or moving blocker corollaries of the preceding theorem.

#### Proof

The four possibilities for \((d_s,d_t)\) in (10) are exhaustive.

#### Profile \((1,1)\)

Apply Lemma 2(3) to the rank-two edge \(H\).  Its opposite quotient pair is
\(\{s,t\}\), so

~~~text
Gamma_s union Gamma_t={0,1,2}.                         (38)
~~~

But \(|\Gamma_s|\le d_s=1\) and \(|\Gamma_t|\le d_t=1\), making (38)
impossible.

#### Profile \((2,1)\)

Suppose \(d_s=2,d_t=1\); the \((1,2)\) profile is obtained by exchanging
\(s,t\).  Equation (38) and the dimension bounds force a unique colour
\(k\) and the other two colours \(i,j\) such that

~~~text
Gamma_t={k},                       Gamma_s={i,j}.       (39)
~~~

By Lemma 1, \(A_s\) has matrix rank two.  Its opposite quotient pair in the
active \(K_4\) is \(\{q_1,t\}\).  Lemma 2(3) gives

~~~text
Gamma_(q_1) union Gamma_t={0,1,2}.                     (40)
~~~

Since \(\dim M=2\), (39)--(40) force

~~~text
Gamma_(q_1)={i,j}.                                     (41)
~~~

The rank-two edge \(C_s\), with opposite pair \(\{q_0,t\}\), similarly
gives

~~~text
Gamma_(q_0)={i,j}.                                     (42)
~~~

Now apply Lemma 2 with quotient pair \(D=\{q_1,s\}\).  Its complementary
physical edge is \(A_t\), and exactly colour \(k\) survives.  Lemma 2(2)
forces

~~~text
A_t in K^*(e_(q_0,k)^* tensor e_(t,k)^*).              (43)
~~~

But the \(q_0\)-shore of \(A_t\) lies in
\(L=R_{q_0}\), while \(k\notin\Gamma_{q_0}\).  This contradicts (43).
The same proof with \(s,t\) exchanged excludes \((1,2)\).

#### Profile \((2,2)\)

For every \(v\in A_4\), put

~~~text
Delta_v={0,1,2}-Gamma_v.                               (44)
~~~

Every \(\Delta_v\) is nonempty because \(R_v\) is two-dimensional and cannot
contain all three independent coordinate covectors.

The five edges

~~~text
H, A_s, C_s, A_t, C_t                                  (45)
~~~

all have rank two by Lemma 1.  Applying Lemma 2(3) to their opposite
quotient pairs gives

~~~text
Delta_s intersect Delta_t=empty,
Delta_(q_1) intersect Delta_t=empty,
Delta_(q_0) intersect Delta_t=empty,
Delta_(q_1) intersect Delta_s=empty,
Delta_(q_0) intersect Delta_s=empty.                   (46)
~~~

The nonempty sets \(\Delta_s,\Delta_t\) are disjoint.  The nonempty
\(\Delta_{q_0}\) is disjoint from both, so their union cannot contain all
three colours.  Hence \(\Delta_s,\Delta_t\) are distinct singleton sets.
After naming their elements \(i,j\) and the third colour \(k\), all relations
in (46) force

~~~text
Delta_s={i},                 Delta_t={j},
Delta_(q_0)=Delta_(q_1)={k}.                            (47)
~~~

It remains to compute the rank of \(B_{st}\).  Choose bases of \(L,M\) in
which \(H=I_2\).  Since \(d_s=d_t=2\), there are surjective maps

~~~text
X_s:V_s -> K^2,                 X_t:V_t -> K^2         (48)
~~~

and matrices \(\mathsf T,\mathsf S\in GL_2(K)\) such that

~~~text
Phi_s(z)=(X_s z,mathsf T X_s z),
Phi_t(z)=(X_t z,mathsf S X_t z).                       (49)
~~~

The conformal relation (11) is exactly
\(\beta(W_s,W_t)=0\), so Lemma 3 supplies \(q\ne0\) and

~~~text
mathsf T=qJ,                      mathsf S=-qJ.         (50)
~~~

For \(z_s\in V_s,z_t\in V_t\), equation (34) and
\(\Xi_{st}=H\boxtimes D_{st}\) give

~~~text
D_st(z_s,z_t)=-q det(X_s z_s,X_t z_t),
B_st(z_s,z_t)=q det(X_s z_s,X_t z_t).                  (51)
~~~

Therefore the matrix of the labelled local edge is

~~~text
[B_st]=q X_s^T J X_t.                                  (52)
~~~

The map \(X_t\) is surjective, \(J\) is invertible, and \(X_s^T\) is
injective.  Hence

~~~text
rank B_st=2.                                           (53)
~~~

Finally take the quotient pair \(D=\{q_0,q_1\}\) in Lemma 2.  By (47),
exactly colour \(k\) survives, so Lemma 2(2) forces

~~~text
B_st in K^*(e_(s,k)^* tensor e_(t,k)^*),               (54)
~~~

which has rank one.  This contradicts (53).  All four profiles are
excluded. \(\square\)

The two inactive tags \(m,n\) in Lemma 2 are load-bearing: they make the
surviving opposite-side pure tensors independent without choosing bases in
the quotient spaces.  The proof is a six-quotient support cover, not a
coordinate support-mask census.

## 4. Common-incidence column splicing excludes the singleton triangle

For each outside vertex \(v\in B\), the four fixed root vectors define the
common incidence map

~~~text
L_v:V_v -> K^4,
z |-> (W_(r,v)(x_r,z))_(r in R).                       (55)
~~~

If \(P\subset B\) is a pair, its complementary permanent is the pullback of
the order-four permanent form along the four maps on \(B-P\):

~~~text
Pi_P=P_4((L_v)_(v in B-P)).                            (56)
~~~

Concretely, after ordering four labelled modes \(v_0,v_1,v_2,v_3\),

~~~text
[c_0,c_1,c_2,c_3]P_4(L_(v_0),L_(v_1),L_(v_2),L_(v_3))
 =per[
   L_(v_0)[:,c_0], L_(v_1)[:,c_1],
   L_(v_2)[:,c_2], L_(v_3)[:,c_3]
 ].                                                     (57)
~~~

The same maps \(L_v\) occur in every companion.  This common-incidence
constraint was not used in Theorem 4.

### Theorem 5 (the rank-one singleton monomial triangle is impossible)

Over every characteristic-zero field, no common incidence family (55)
satisfies the three pure companion identities (15).  Consequently the
rank-one Branch-III singleton survivor of the determinant-divisor reduction
is empty on the actual complex witness locus.

#### Proof

First take \(K=\mathbb C\).

Order the three tail vertices as \(T=\{v_1,v_2,v_3\}\).  The complements of
the three physical triangle edges are exactly

~~~text
B-{q_0,t}={q_1} union T,
B-{q_1,t}={q_0} union T,
B-Q={t} union T.                                       (58)
~~~

The colours \(i,j,k\) in (14)--(15) are distinct and therefore exhaust
\(\{0,1,2\}\).  Define one synthetic incidence map

~~~text
mathsf D:K^3 -> K^4                                    (59)
~~~

by splicing the three active source columns:

~~~text
mathsf D[:,i]=alpha L_(q_1)[:,i],
mathsf D[:,j]=beta  L_(q_0)[:,j],
mathsf D[:,k]=gamma L_t[:,k].                          (60)
~~~

No scalar is divided out.

Let \(c\in\{0,1,2\}\) and let
\(\omega=(\omega_1,\omega_2,\omega_3)\) be a tail word.  If

~~~text
(eta_c,v_c)
 =(alpha,q_1) for c=i,
 =(beta,q_0)  for c=j,
 =(gamma,t)   for c=k,                                 (61)
~~~

then permanent multilinearity in the first source column gives

~~~text
[c,omega]P_4(mathsf D,L_(v_1),L_(v_2),L_(v_3))
 =eta_c [c,omega]P_4(L_(v_c),L_(v_1),L_(v_2),L_(v_3)).
                                                               (62)
~~~

Equations (15), together with the exact complement ledger (58), make the
right side

~~~text
mu_c       if omega=(c,c,c),
0          otherwise.                                  (63)
~~~

Thus all \(3^4=81\) coefficients assemble into

~~~text
P_4(mathsf D,L_(v_1),L_(v_2),L_(v_3))
 =sum_(c=0)^2 mu_c e_c tensor e_c tensor e_c tensor e_c.
                                                               (64)
~~~

In the tensor formulation, (64) says that the four linear maps

~~~text
mathsf D^T, L_(v_1)^T,L_(v_2)^T,L_(v_3)^T:
K^4 -> K^3                                             (65)
~~~

send the order-four permanent tensor to a weighted
\(\Delta_3\).  Every \(\mu_c\ne0\).  To invoke the normalized obstruction
without a silent division, explicitly postcompose the first map in (65) by

~~~text
S=diag(mu_0^(-1),mu_1^(-1),mu_2^(-1)).                 (66)
~~~

Then

~~~text
(S tensor id tensor id tensor id)
  sum_(c=0)^2 mu_c e_c tensor 4
 =Delta_3.                                             (67)
~~~

This is forbidden by the
[fourth-order permanent subrank obstruction](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md),
which allows arbitrary four local linear maps and proves
\(\operatorname{subrank}(P_4)=2\) over \(\mathbb C\).  No symmetry or
pre-existing rank hypothesis on the maps in (65) is missing: equality (64)
itself has one-mode flattening rank three.

This contradiction excludes (15) over \(\mathbb C\).

#### Exact characteristic-zero descent

Suppose instead that the finite data (55), (60), and (15) existed over an
arbitrary characteristic-zero field \(K\).  Let \(K_0\subset K\) be the
subfield generated over \(\mathbb Q\) by their finitely many matrix and
scalar entries.  The field \(K_0\) is finitely generated over \(\mathbb Q\)
and admits an injective embedding into \(\mathbb C\).  Applying that embedding
preserves every polynomial equality in (15), every coefficient identity
(62)--(64), and the declared nonzeros

~~~text
alpha beta gamma mu_0 mu_1 mu_2!=0.                    (68)
~~~

It would therefore produce the forbidden complex restriction (64).
Consequently the singleton triangle is impossible over every
characteristic-zero field as stated. \(\square\)

The column-splicing step is the same exact mechanism used in the committed
[three pure cofactor compatibility obstruction](SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md).
Here the three shared tails are precisely the three vertices of \(T\).

## 5. Controls, limitations, and saturation ledger

### 5.1 The common-incidence gate is load-bearing

At the level of independently declared companion tensors, the singleton
triangle is consistent.  Choose distinct \(i,j,k\), nonzero
\(\alpha,\beta,\gamma\), the physical blocks (14), and \(B_{uv}=0\).  Declare
companions by the three multiplied identities (15), with every other
physical edge term zero.  Then all six pair responses vanish and the
complete target is exactly its three pure tensors.

This is the formal monomial-triangle control from the preceding reduction.
It is not a graph point: the three declared companions are not shown to be
permanents of one common incidence family.  Theorem 5 excludes precisely
that missing common-incidence realization.

### 5.2 The quotient support cover does not infer a companion at \(N_D=0\)

When \(\Gamma_v\cup\Gamma_w\) contains all three colours, the right side of
(24) is zero.  Lemma 2 then says only

~~~text
H_P boxtimes bar Pi_P^D=0.                              (69)
~~~

For a nonzero \(H_P\), this kills the displayed quotient of the companion,
but it does not make \(H_P\) coordinate and it supplies no common-root
identity.  The profile proof uses the rank-two edge only to force support
coverage, never to divide by a companion coefficient.

### 5.3 Exact nonzero and divisor ledger

1. **Actual source.**  The application is over \(\mathbb C\), with the same
   GLS4 pair and the complete target weights

   ~~~text
   mu_0 mu_1 mu_2!=0.                                  (70)
   ~~~

   Theorem 4 does not use \(\Pi_Q\ne0\), higher-column survival, the raw
   residual incidence, or a selected contraction.

2. **Inherited rank-two chart.**  Theorem 4 begins only after the preceding
   reduction has proved rank two, double containment, and exactly two active
   combined ports.  Normalizing \(H\) to \(I_2\) in Lemma 3 is a pointwise
   change of bases.  Equivalently it may be carried out on any nonzero
   \(2\) by \(2\) minor chart.  No chosen minor enters the conclusion.

3. **Quotient spaces.**  Membership in each \(\Gamma_v\) is an exact linear
   containment.  A colour omitted from \(\Gamma_v\) has a nonzero quotient
   class by definition; no coordinate of that class is inverted.  The
   inactive pure tags in (29) establish independence without trivializing
   any quotient line or plane.

4. **Dimension profiles.**  The four profiles

   ~~~text
   (d_s,d_t)=(1,1),(2,1),(1,2),(2,2)                  (71)
   ~~~

   are exhaustive because both projections of each nonzero \(W_u\) are
   injective and \(L,M\) are two-dimensional.  This is a derived cover, not
   a support-mask census.

5. **Full-plane scalar.**  The scalar \(q\ne0\) in (33) is derived from
   invertibility of the graph map \(\mathsf T\).  No \(q\)-chart is silently
   removed.  Formula (52) obtains rank two from an injective--invertible--
   surjective composition.

6. **Rank-one active scalars.**  The factors

   ~~~text
   alpha beta gamma!=0                                  (72)
   ~~~

   are inherited from three active coordinate-monomial physical blocks.
   Synthetic columns (60) multiply by them; they are never divided out.

7. **Weighted target normalization.**  Division by \(\mu_c\) occurs only in
   the explicit invertible output map (66), under the declared saturation
   (70).  Before that final normalization, every splicing equation is kept
   in the multiplied form (15).

8. **Characteristic-zero scope.**  The rank-two proof is exact linear
   algebra in characteristic zero after its inherited interface.  The
   permanent-subrank dependency is stated over \(\mathbb C\); the finitely
   generated-field embedding argument after (68) gives the exact
   characteristic-zero descent.  No finite-field or numerical inference is
   used.

9. **Unused selector gates.**  Neither exclusion divides by or saturates
   against

   ~~~text
   h=H_Q(z_Q),                  p_(A,Q)(z_Q),
   a response coordinate,      a nuisance or augmented minor,
   an alignment factor,        a selector coefficient,
   a target-module denominator.                               (73)
   ~~~

10. **Complete target use.**  Equation (24) is a quotient of the full
    \(729\)-coefficient equality.  Equation (64) reconstructs all \(81\)
    coefficients of a four-mode restriction.  Neither proof is a sampled,
    generic, pure-shell, or Hamming-one argument.

### 5.4 Exact boundaries

Theorem 4 excludes only the rank-two core already reached by the previous
all-six-pair-zero reduction.  It says nothing about a branch where merely one
or several responses vanish, or about any nonzero-response absorption
profile.

Theorem 5 excludes only the rank-one two-sided singleton branch.  It does not
apply to the double-contained Branch I, the one-sided Branch II, or the
two-port Branch III identity.  In particular, no column-splicing conclusion
is asserted unless the three pure tensors have the exact common tails in
(58).

The four-port response is a separate issue on the determinant divisor.  The
preceding theorem gives the denominator-free identity and its additional
rank-one quartic.  Nothing here silently assumes that seventh response zero
outside branches where it is already derived.

## 6. Proof-DAG consequence and evidence status

Composing this theorem with GLS10 and the preceding determinant-divisor
reduction gives

~~~text
actual four-root maximum-root surplus-two witness
 + GLS4 pair Q
 + all six same-Q pair responses identically zero

 -> rank H_Q=0 excluded by GLS4 activity
 -> rank H_Q=3 excluded by GLS10
 -> rank H_Q=2 excluded by Theorem 4 here
 -> rank H_Q=1
      Branch I double-contained,                  OPEN
      Branch II one-sided,                        OPEN
      Branch III singleton triangle,              EXCLUDED HERE
      Branch III two-port,                        OPEN.          (74)
~~~

The reviewed exact status is

~~~text
rank-two conformal core:                                  EXCLUDED;
profiles (1,1),(2,1),(1,2),(2,2):                        EXHAUSTED;
rank-two B_st full-plane rank calculation:                PROVED;
rank-one singleton common-incidence triangle:             EXCLUDED;
characteristic-zero column-splicing descent:              PROVED;

focused primary verifier:                                 PASS;
independent no-import audit:                              PASS;
hostile theorem and scope review:                         PASS;
formalization:                                            NONE;

rank-one Branch I:                                        OPEN;
rank-one Branch II and its transpose:                     OPEN;
rank-one Branch III two-port identity:                    OPEN;
separate seventh-response quartic on surviving rank one:  OPEN;
weaker response-zero patterns:                            OPEN;
nonzero-response absorption and exceptional fibres:       OPEN;
legal same-Q named downstream target package:             OPEN;
supply-and-target-attachment strategic node:              OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED. (75)
~~~

The smallest remaining obligation inside the literal all-six-pair-zero leaf
is the complete-target and common-incidence analysis of rank-one Branches I,
II, and the two-port Branch III identity, retaining the separate
seventh-response condition wherever a literal all-seven-zero claim is
needed.  This theorem supplies no target selector, downstream detector
activity, permanent restriction beyond the local contradiction in Theorem 5,
extraction, or gluing result.

The focused exact verifier checks the six labelled quotient identities, every
dimension profile, the full-plane \(\beta\) classification and \(B_{st}\)
rank, all \(81\) column-splicing coefficients, and the exact control
boundaries.  The independent standard-library audit reconstructs the same
obligations through different quotient tables, coefficient solving, and
permutation expansion.  Both pass, and the hostile theorem and scope review
also passes.  These bounded replays verify displayed identities; the written
arguments prove the arbitrary-point implications.

Dependencies:

- [determinant-divisor rank-two core and rank-one trichotomy reduction](FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md)
- [GLS10 full-rank response-zero exclusion](FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_PURE_COMPLEMENTARY_PERMANENT_SURVIVOR_EXCLUSION_THEOREM.md)
- [GLS4 same-pair source theorem](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [GLS7 four-root source cover](FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md)
- [fourth-order permanent subrank obstruction](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md)
- [three pure cofactor column-splicing precedent](SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md)

Evidence:

- [focused exact verifier](verify_four_root_determinant_divisor_rank_two_core_and_rank_one_singleton_triangle_exclusion.py); and
- [independent standard-library no-import audit](audit_four_root_determinant_divisor_rank_two_core_and_rank_one_singleton_triangle_exclusion.py); and
- [hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_REDUCTION_REVIEW_2026-08-20.md).

No external literature premise is used.
