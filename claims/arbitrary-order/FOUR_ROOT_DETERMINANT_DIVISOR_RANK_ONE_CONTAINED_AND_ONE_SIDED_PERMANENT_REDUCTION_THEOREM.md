# Four-root determinant-divisor rank-one contained and one-sided permanent reduction

## Status

**Proved exact characteristic-zero reduction.  The focused exact primary
verifier, genuinely independent no-import audit, and hostile scope review
pass.**

Start with an actual hypothetical ternary GHZ witness whose
maximum-cardinality torus root has order four and surplus two.  Fix the same
residual pair \(Q\) supplied by GLS4, assume all six same-\(Q\) pair responses
vanish, and enter rank-one Branch I or Branch II of GLS11 after the rank-two
and singleton-triangle exclusions of GLS12.

This theorem proves the following exhaustive source-interface reduction.

1. In Branch I, two noncoordinate residual factors are impossible by an
   arbitrary-rank extension of the
   \(\operatorname{Sym}(a\otimes b\otimes q)\) quartic subrank obstruction.
   Eight exact deleted-mode \(P_5\) pullbacks give a nonzero decomposable
   target whenever one of their coordinate-cover sets has size two.  If none
   does, deletion counting forces both factor families to be coordinate and
   balanced \(2+2\).  A ninth cross pullback is pure unless the two residual
   factors use the same coordinate.  On the literal seventh-response-zero
   leaf, the two balanced partitions then align and one exact elementary
   symmetric equation remains.
2. The aligned balanced core has an exact two-row augmentation to \(P_6\).
   Its output is a weighted diagonal tensor plus one four-port face defect
   \(\Psi\).  The complete target puts \(\Psi\) in the active-line module, but
   does **not** prove \(\Psi=0\).
3. In Branch-II singleton support, the complete target supplies one nonzero
   pure/decomposable \(P_4\) companion.  The committed decomposable
   rank-drop theorem applies only conditionally when all four incidence maps
   have rank at least two.
4. In Branch-II two-port support, one of two explicit deleted-mode \(P_5\)
   pullbacks is nonzero and decomposable.  The labelled transpose is covered
   exactly.

The pure \(P_4/P_5\) outputs are reductions, not exclusions, and no
concision or local-rank hypothesis is silently added to them.  The balanced
\(P_6\) identity is not a \(P_6\to\Delta_3\) restriction unless the displayed
defect vanishes.  This theorem does not supply a GLD selector, close weaker
response-zero or absorption fibres, or close the supply-and-target strategic
node.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact inherited source and target

Let \(K\) be a field of characteristic zero.  The actual-witness application
is over \(K=\mathbb C\).  Every local covector space is three-dimensional
with fixed target coordinate covectors

~~~text
E_v=V_v^*,
e_(v,0)^*, e_(v,1)^*, e_(v,2)^*.                       (1)
~~~

Let

~~~text
Omega=R disjoint-union B,       |R|=4,       |B|=6,
Q={q_0,q_1} subset B,           U=B-Q,       |U|=4.    (2)
~~~

The four root vectors form a maximum-cardinality torus root: there is no
five-vertex torus root anywhere in \(\Omega\).  The pair \(Q\) is the same
physical pair supplied by GLS4.  Write

~~~text
H=H_Q in E_(q_0) tensor E_(q_1),
A_u=H_(q_0,u),       C_u=H_(q_1,u),
B_uv=H_(u,v)                              (u,v in U).  (3)
~~~

All tensor slots are labelled.  The six pair-response identities are

~~~text
H boxtimes B_uv+A_u boxtimes C_v+A_v boxtimes C_u=0
                                      for {u,v} subset U. (4)
~~~

For every pair \(P\subset B\), let \(\Pi_P\) be the four-root complementary
permanent tensor on \(B-P\).  The complete contracted target is

~~~text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(d=0)^2 mu_d product_(v in B)e_(v,d)^*,
mu_0 mu_1 mu_2!=0.                                    (5)
~~~

Equation (5) is the full \(3^6=729\)-coefficient tensor identity.  The
companions come from one common physical incidence family

~~~text
L_v:V_v -> K^4,
Pi_P=P_4((L_v)_(v in B-P)).                            (6)
~~~

For a covector \(f\in V^*\), put \(K(f)=\ker f\); in particular
\(K(0)=V\).  If \(S\subset V\), then \(L|S\) and \(f|S\) denote exact
restrictions.  For a map \(L:S\to K^4\) and a covector \(f\in S^*\), write

~~~text
(L,f):S -> K^5,             z |-> (Lz,f(z)).           (7)
~~~

A nonzero covector \(f\in E_v\) is *coordinate of colour \(d\)* if
\(f\in K^*e_{(v,d)}^*\).  Write \(\operatorname{col}(f)=d\) in that case;
zero and noncoordinate covectors have no declared colour.

### 1.1 Branch I: double containment

Assume

~~~text
rank H=1,                 H=x tensor y,
x!=0, y!=0,

A_u=x tensor a_u,        C_u=y tensor c_u,
B_uv=-(a_u tensor c_v+c_u tensor a_v).                 (8)
~~~

Neither family \((a_u)\) nor \((c_u)\) is identically zero.  Maximum-root
maximality already implies that each family contains a nonzero coordinate
covector.  Equations (8) are exactly rank-one Branch I of GLS11.

When the literal seventh six-vertex response is also assumed zero, GLS11
gives the additional quartic equation

~~~text
Phi(a,c)
 =sum_(S subset U, |S|=2)
   sh_(S,U-S)(tensor_(u in S)a_u tensor
              tensor_(v in U-S)c_v)
 =0.                                                       (9)
~~~

Equation (9) is not included silently in (4).

### 1.2 Branch II: exactly one shore escapes

Up to the labelled residual-shore exchange, GLS11 gives

~~~text
A_u=x tensor a_u                         for every u,
bar C_s!=0 in (E_(q_1)/(K y)) tensor E_s for some s.   (10)
~~~

The common active support has size one or two.

On singleton support \(T=\{s\}\),

~~~text
A_s=x tensor a_s,              A_v=0              (v!=s),
C_s arbitrary with bar C_s!=0,
C_v=y tensor c_v                                   (v!=s),
B_sv=-a_s tensor c_v,
B_vw=0                                   (v,w!=s).    (11)
~~~

Here \(a_s\) and \(y\) are nonzero coordinate covectors.

On two-port support \(T=\{s,t\}\), naming the inactive ports \(m,n\), there
are

~~~text
d in E_(q_1)-(K y),     a_s,a_t!=0,
c_u in E_u                                        (u in U) (12)
~~~

such that

~~~text
A_s=x tensor a_s,                    A_t=x tensor a_t,
A_m=A_n=0,

C_s=d tensor a_s+y tensor c_s,
C_t=-d tensor a_t+y tensor c_t,
C_m=y tensor c_m,                    C_n=y tensor c_n,

B_uv=-(a_u tensor c_v+c_u tensor a_v),
a_m=a_n=0.                                             (13)
~~~

At least one of \(a_s,a_t\) is coordinate, and \(y\) is coordinate or both
\(a_s,a_t\) are coordinate.  The transposed branch is obtained by the exact
labelled exchange

~~~text
(q_0,x,A,a) <-> (q_1,y,C,c).                           (14)
~~~

## 2. Arbitrary-rank quartic subrank and the two-noncoordinate exclusion

The committed support-three contraction theorem proves the following lemma
when its quadratic factor is nondegenerate.  The radical check below removes
that hypothesis.

### Lemma 1 (arbitrary-rank \(\operatorname{Sym}(a b q)\) has subrank at most two)

Let \(X\) be finite-dimensional and \(V=X\oplus K^2\).  Let
\(a,b\in V^*\) be the two coordinate covectors on the last summand and vanish
on \(X\).  Let \(q\) be any symmetric bilinear form on \(X\), of arbitrary
rank, extended by zero off \(X\).  Define the
labelled symmetric four-tensor by

~~~text
T(z_0,z_1,z_2,z_3)
 =sum_(i!=j) a(z_i)b(z_j)q(z_k,z_l),
{k,l}={0,1,2,3}-{i,j}.                                 (15)
~~~

Then over every characteristic-zero field, no four local linear maps pull
\(T\) back to a three-term diagonal four-tensor with all three diagonal
coefficients nonzero.  Equivalently, the ordinary subrank of \(T\) is at
most two.

#### Proof

First work over \(\mathbb C\).  Suppose maps
\(\phi_i:\mathbb C^3\to V\) pull \(T\) back to a weighted
\(\Delta_3\).  Its one-mode concision makes every \(\phi_i\) injective.  Put

~~~text
alpha_i=a composed with phi_i,
beta_i=b composed with phi_i,
K_i=ker(alpha_i) intersect ker(beta_i).                (16)
~~~

Every \(K_i\) is nonzero.  For nonzero \(z\in K_i\), contraction in mode
\(i\) gives on the source side

~~~text
Sym(a tensor b tensor q(phi_i(z),-)).                  (17)
~~~

If \(q(\phi_i(z),-)=0\), (17) is zero.  The corresponding target contraction
is

~~~text
sum_(d=0)^2 nu_d z[d] e_d tensor e_d tensor e_d,
nu_0 nu_1 nu_2!=0,                                    (18)
~~~

which is nonzero for every \(z\ne0\).  Hence
\(q(\phi_i(z),-)\ne0\).  It is independent from \(a,b\), because it is a
nonzero covector on \(X\) while \(a,b\) vanish there.  After discarding the
common radical, (17) is therefore the order-three permanent tensor \(P_3\).

If \(z\) had all three coordinates nonzero, (18) would be equivalent to
\(\Delta_3\), producing \(P_3\to\Delta_3\).  Both essential tensors are
three-dimensional and concise, so the local maps would be invertible and
preserve tensor rank, contrary to

~~~text
rank(P_3)=4,                     rank(Delta_3)=3.       (19)
~~~

Thus every vector of every \(K_i\) has a zero coordinate.  Over the infinite
field \(\mathbb C\), a linear space cannot be the union of three proper
subspaces, so each \(K_i\) lies in one coordinate hyperplane.  Consequently
each \(K_i\) is either a line with coordinate support one or two, or a
coordinate plane.

For complementary pairs \(\{i,j\},\{k,l\}\), restricting modes \(k,l\) to
\(K_k,K_l\) leaves the exact factorization

~~~text
sum_d nu_d z_i[d]z_j[d]z_k[d]z_l[d]
 =F_ij(z_i,z_j) Q_kl(z_k,z_l),                         (20)

F_ij=alpha_i tensor beta_j+beta_i tensor alpha_j,
Q_kl=(phi_k tensor phi_l)^*q.
~~~

Therefore the coordinatewise-product diagonal matrices from
\(K_k\times K_l\) span at most one dimension and, whenever nonzero, have the
same rank and row/column spaces as \(F_{ij}\).  The exact kernel-type
exhaustion is now independent of the rank of \(q\):

1. with four lines, intersecting singleton supports force rank one against
   a rank-two \(F\); equal two-support lines force the complementary lines
   onto the third singleton and give the same contradiction; pairwise
   disjoint nonempty supports do not fit in three coordinates;
2. with one coordinate plane, the other three lines are forced onto its
   missing coordinate, after which a complementary \(F\) has incompatible
   row and column spaces;
3. with two planes, equal missing coordinates give a two-dimensional
   product space, while distinct missing coordinates give rank one against
   a rank-two complementary \(F\);
4. with three planes, their missing coordinates are distinct, and pairing
   the other two against the remaining singleton line again gives
   incompatible row and column spaces; and
5. with four planes, two miss the same coordinate and give a
   two-dimensional product space.

These are exactly the five kernel cases in the
[support-three \(P_5\) contraction subrank proof](SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md);
the only previous use of nondegeneracy was the contraction step, replaced by
the first paragraph above.  Every case contradicts (20).

For an arbitrary characteristic-zero field \(K\), take the subfield
finitely generated over \(\mathbb Q\) by the alleged maps, form, and target
weights, and embed it into \(\mathbb C\).  Polynomial equalities, ranks, and
all declared nonzeros are preserved.  The resulting complex restriction is
impossible, proving the lemma. \(\square\)

### Proposition 2 (both residual factors cannot be noncoordinate)

In Branch I, at least one of \(x,y\) is coordinate.

#### Proof

Assume both are noncoordinate.  The torus-zero lemma supplies fully
supported vectors

~~~text
z_0 in K(x),                  z_1 in K(y).             (21)
~~~

Define six sign-twisted augmented incidence maps

~~~text
Ltilde_(q_0)=(L_(q_0), x, 0),
Ltilde_(q_1)=(L_(q_1), 0,-y),
Ltilde_u    =(L_u,    -c_u,a_u)             (u in U).  (22)
~~~

The two-bottom-row permanents are

~~~text
beta_Q=-H,       beta_(q_0,u)=A_u,
beta_(q_1,u)=C_u,       beta_uv=B_uv.                  (23)
~~~

Laplace expansion in the two bottom rows and (5) therefore give the exact
identity

~~~text
P_6((Ltilde_v)_(v in B))
 =sum_(P subset B, |P|=2) beta_P tensor Pi_P
 =T_GHZ-2 H tensor Pi_Q.                               (24)
~~~

Contract the \(q_0,q_1\) modes at \(z_0,z_1\).  Their two augmented bottom
components vanish, and the correction term in (24) vanishes.  Put

~~~text
p_0=L_(q_0)z_0,              p_1=L_(q_1)z_1,
q(r,s)=P_4(p_0,p_1,r,s).                               (25)
~~~

The contracted universal source is
\(+\operatorname{Sym}(e_4^*e_5^*q)\).  Pulling it through the four port maps
\(z\mapsto(L_uz,-c_u(z),a_u(z))\) gives
\(-\operatorname{Sym}(c\,a\,q)\).  The overall sign is immaterial to
subrank, and \(q\) may have arbitrary rank.
The contracted right side is

~~~text
sum_(d=0)^2 mu_d z_0[d]z_1[d]
       product_(u in U)e_(u,d)^*,                      (26)
~~~

a three-term diagonal quartic with all coefficients nonzero because
\(z_0,z_1\) are torus points.  This contradicts Lemma 1. \(\square\)

## 3. Eight deleted-mode \(P_5\) pullbacks and the Branch-I cover

For \(t\in U\), let \(U_t=U-\{t\}\).  Define the following exact pullbacks of
the order-five permanent:

~~~text
Psi_t^a
 =P_5(
   (L_(q_0),x),
   (L_(q_1)|K(y),0),
   ((L_v|K(a_v),-c_v|K(a_v)))_(v in U_t)
  ),                                                        (27)

Psi_t^c
 =P_5(
   (L_(q_0)|K(x),0),
   (L_(q_1),y),
   ((L_v|K(c_v),-a_v|K(c_v)))_(v in U_t)
  ).                                                        (28)
~~~

These are tensors on the five labelled, possibly restricted, local spaces
shown in (27)--(28).  No rank or concision is part of their definition.

Define the coordinate-cover sets

~~~text
C_t^a={col(y)} union {col(a_v):v in U_t},
C_t^c={col(x)} union {col(c_v):v in U_t},               (29)
~~~

omitting undefined colours.

### Lemma 3 (coverage and pure deletion identities)

For every \(t\in U\),

~~~text
|C_t^a|>=2,                    |C_t^c|>=2.             (30)
~~~

If \(C_t^a\) has exactly two colours and \(d\) is the missing colour, then

~~~text
a_t!=0,        a_t=lambda_t e_(t,d)^*,
a_t tensor Psi_t^a
 =mu_d e_(t,d)^* tensor e_(q_0,d)^*
   tensor (e_(q_1,d)^*|K(y))
   tensor product_(v in U_t)(e_(v,d)^*|K(a_v)),        (31)
~~~

with \(\lambda_t\ne0\).  In particular \(\Psi_t^a\) is a nonzero
decomposable \(P_5\) pullback.  If \(|C_t^a|=3\) and \(a_t\ne0\), then

~~~text
Psi_t^a=0.                                             (32)
~~~

The symmetric statements hold for \(C_t^c,\Psi_t^c,c_t\).

#### Proof

Restrict (5) at \(q_1\) to \(K(y)\) and at every \(v\in U_t\) to
\(K(a_v)\).  Every \(H\)- and \(C\)-term vanishes.  Every \(A_v\)-term with
\(v\ne t\) vanishes.  In \(B_{tv}\), only
\(-a_t\otimes c_v\) survives, and every \(B_{uv}\) with
\(u,v\ne t\) vanishes.  Laplace expansion of (27) therefore gives

~~~text
a_t tensor Psi_t^a
 =sum_(d notin C_t^a) mu_d e_(t,d)^* tensor
   e_(q_0,d)^* tensor (e_(q_1,d)^*|K(y)) tensor
   product_(v in U_t)(e_(v,d)^*|K(a_v)).               (33)
~~~

Every displayed complementary factor is nonzero: a coordinate covector
restricts to zero on \(K(f)\) exactly when \(f\) is a nonzero multiple of
that same coordinate covector.  Complementary tensors belonging to distinct
surviving colours are independent because their unrestricted \(q_0\)-slot
factors are the distinct coordinate covectors \(e_{(q_0,d)}^*\).  (For the
transposed identity, the unrestricted \(q_1\)-slot gives the same
separation.)  The left side of (33) has \(t\)-flattening rank at most one,
so at most one target colour survives.  This proves (30).

If one colour \(d\) survives, equality of the two nonzero decomposable sides
gives (31).  If no colour survives and \(a_t\ne0\), (33) gives (32).  The
proof for (28) is the labelled exchange
\((q_0,x,a)\leftrightarrow(q_1,y,c)\). \(\square\)

The split is deliberately stated by coverage, not by prior vanishing of
\(\Psi_t^a\) or \(\Psi_t^c\).  If the factoring covector were zero, a zero
left side would not determine the cofactor tensor.

### Lemma 4 (the no-pure-deletion core is balanced)

Suppose none of the eight cover sets in (29) has size two.  Name the two
complementary colour pairs separately only for display:

~~~text
y=eta e_(q_1,j)^*,
{a_u:u in U}
 ={two nonzero multiples of colour r,
   two nonzero multiples of colour s},
{j,r,s}={0,1,2},                                       (34)

x=xi e_(q_0,i)^*,
{c_u:u in U}
 ={two nonzero multiples of colour r',
   two nonzero multiples of colour s'},
{i,r',s'}={0,1,2}.                                     (35)
~~~

All eight tensors in (27)--(28) then vanish.

#### Proof

By Lemma 3 every cover now has all three colours.  If \(y\) were
noncoordinate, the four \(a_u\)'s would have to cover all three coordinate
colours even after deletion of any one coordinate member.  Each colour
would occur at least twice, requiring at least six coordinate members among
four slots.  This is impossible.

Thus \(y\) has one coordinate colour \(j\).  Each of the other two colours
must occur at least twice among the \(a_u\)'s, since deleting its unique
occurrence would destroy the three-colour cover.  Four slots force exactly
two occurrences of each other colour, with no zero, noncoordinate, or
colour-\(j\) member.  This proves (34).  The same argument proves (35).
Every \(a_t,c_t\) is now nonzero and every cover has size three, so (32) and
its transpose kill all eight pullbacks. \(\square\)

There is one further cross pullback.  On the core (34)--(35), define

~~~text
Psi^x
 =P_5(
   (L_(q_1)|K(y),0),
   ((L_u|K(c_u),a_u|K(c_u)))_(u in U)
  ).                                                        (36)
~~~

### Lemma 5 (different residual colours give a ninth pure \(P_5\))

If the coordinate colours \(i,j\) of \(x,y\) in (34)--(35) are distinct,
then \(\Psi^x\) is a nonzero decomposable \(P_5\) pullback.

#### Proof

Restrict (5) at \(q_1\) to \(K(y)\) and at every port \(u\) to \(K(c_u)\).
The \(H,C,B\) terms vanish, and the \(A\)-terms assemble by bottom-row
Laplace expansion into

~~~text
x tensor Psi^x.                                        (37)
~~~

In (35), the \(c\)-family uses twice each of the two colours different from
\(i=\operatorname{col}(x)\).  Since \(j\ne i\), the coordinate factors
\(y,c_u\) kill exactly those two colours and leave colour \(i\).  Thus (37)
equals the nonzero restriction of the pure colour-\(i\) target.  Equality of
simple tensors proves the claim. \(\square\)

Combining Lemmas 3--5 gives the exhaustive Branch-I source cover:

~~~text
one of the eight deleted-mode cover sets has size two
  -> an explicit nonzero decomposable P_5 pullback;
otherwise
  -> both families are balanced coordinate 2+2;
     different colours of x,y
       -> the cross pullback (36) is nonzero decomposable;
     the only no-pure-P_5 core
       -> x,y use the same coordinate.                 (38)
~~~

The tensors in (31) and (37) are pure \(P_5\) images, not concise
\(P_5\to\Delta_3\) restrictions.  No committed theorem excludes them merely
from the data displayed here.  They define a new open pure-compression
interface; they do not enter the existing weighted \(P_5\to\Delta_3\) node
owned by GLS13.

## 4. Seventh-response alignment and the balanced \(P_6\) face defect

On the last core in (38), relabel the common residual coordinate as zero and
the ports so that

~~~text
x=xi e_(q_0,0)^*,            y=eta e_(q_1,0)^*,
xi eta!=0,

a_u=alpha_u e_(u,lambda_u^a)^*,
c_u=gamma_u e_(u,lambda_u^c)^*,
alpha_u gamma_u!=0,

|{u:lambda_u^a=1}|=|{u:lambda_u^c=1}|=2,
lambda_u^a,lambda_u^c in {1,2}.                        (39)
~~~

### Lemma 6 (the seventh response aligns the two partitions)

If the literal seventh response vanishes, then

~~~text
lambda_u^a=lambda_u^c=:lambda_u             for every u. (40)
~~~

After relabelling ports, take

~~~text
(lambda_(u_1),lambda_(u_2),lambda_(u_3),lambda_(u_4))
 =(1,1,2,2).                                           (41)
~~~

Then the seventh response vanishes if and only if

~~~text
e_2(rho_(u_1),rho_(u_2),rho_(u_3),rho_(u_4))=0,
rho_u=alpha_u/gamma_u.                                 (42)
~~~

#### Proof

For a two-set \(S\subset U\), the \(S\)-summand of \(\Phi(a,c)\) has the
coordinate word which uses \(\lambda_u^a\) on \(S\) and
\(\lambda_u^c\) off \(S\), with nonzero coefficient.  Put

~~~text
A={u:lambda_u^a=1},              C={u:lambda_u^c=1}.   (43)
~~~

Both are two-sets.  If \(A\ne C\), one of the six words occurs exactly
once.  Indeed, if \(A\cap C=\varnothing\), the all-colour-one word belongs
only to \(S=A\).  If \(|A\cap C|=1\), the six words have multiplicities
\(2,2,1,1\) after naming the common, \(A\)-only, \(C\)-only, and remaining
ports.  Hence \(\Phi(a,c)\ne0\), contrary to (9).  Therefore \(A=C\) with
the same colour labels, proving (40).

Under (40), all six summands have the same port word.  Its coefficient is

~~~text
product_(u in U)gamma_u
  sum_(S subset U, |S|=2) product_(u in S)(alpha_u/gamma_u)
 =product_u gamma_u e_2((rho_u)_u).                    (44)
~~~

All \(\gamma_u\ne0\), so (9) is equivalent to (42). \(\square\)

Now assume the aligned core (40)--(41), whether obtained from the literal
seventh-zero leaf or declared directly.  Put

~~~text
h=xi eta,                    p=mu_0/h,
Psi=Pi_Q-p product_(u in U)e_(u,0)^*.                  (45)
~~~

Define the active-line module

~~~text
J=sum_(u in U)
  [K e_(u,lambda_u)^* tensor
   tensor_(v in U-{u}) E_v]
  subset tensor_(u in U)E_u.                           (46)
~~~

### Theorem 7 (exact augmented-\(P_6\) normal form)

The augmented maps (22) satisfy

~~~text
P_6((Ltilde_v)_(v in B))
 =-mu_0 product_(v in B)e_(v,0)^*
   +mu_1 product_(v in B)e_(v,1)^*
   +mu_2 product_(v in B)e_(v,2)^*
   -2h e_(q_0,0)^* tensor e_(q_1,0)^* tensor Psi.     (47)
~~~

Moreover,

~~~text
Pi_Q[0,0,0,0]=p,                  Psi in J.            (48)
~~~

Every \(\widetilde L_v:V_v\to K^6\) is injective.  Every original incidence
map has rank at least two.  More precisely:

~~~text
rank L_(q_0)=2 -> e_(q_0,0)^* notin row(L_(q_0)),
rank L_(q_1)=2 -> e_(q_1,0)^* notin row(L_(q_1)),
rank L_u=2     -> e_(u,lambda_u)^* notin row(L_u).      (49)
~~~

The displayed tensor in (47) is a weighted diagonal tensor in the displayed
coordinates if and only if \(\Psi=0\).  No conclusion here forces that
vanishing or excludes the \(\Psi\ne0\) locus.

#### Proof

Equation (24) is valid throughout Branch I.  Substitute

~~~text
H=h e_(q_0,0)^* tensor e_(q_1,0)^*,
Pi_Q=p e_0^(tensor 4)+Psi                           (50)
~~~

into \(T_{GHZ}-2H\otimes\Pi_Q\).  Since \(hp=\mu_0\), this is exactly
(47).

For (48), take the \((q_0,q_1)=(0,0)\) coefficient of (5).  The
\(H\otimes\Pi_Q\) term is \(h\Pi_Q\).  Every non-\(Q\) term lies in \(J\):
an \(A_u\)- or \(C_u\)-term carries its active port factor
\(e_{(u,\lambda_u)}^*\), and a \(B_{uv}\)-term carries active factors at
\(u,v\).  The target slice is \(\mu_0e_0^{\otimes4}\).  Quotienting this
identity modulo \(J\) gives \(h\Psi\in J\).  Separately, at the all-zero
port word every non-\(Q\) term vanishes, so
\(h\Pi_Q[0,0,0,0]=\mu_0\).  The declared \(h\ne0\) proves both parts of
(48).

Every one-mode flattening of (47) has rank three.  At either residual mode,
the three slices are separated by the complementary residual coordinates
zero, one, and two; the zero slice remains nonzero because its all-zero
coefficient is \(-\mu_0\).  At a port, the pure colour-one and colour-two
slices have complementary residual words (11) and (22), while every
defect slice has residual word (00); the pure colour-zero all-zero
coefficient again remains \(-\mu_0\).  Thus all three slices are independent.

A pullback flattening rank is at most the rank of its local map, so all six
\(\widetilde L_v\) have rank three and are injective.  At each residual mode
only one new bottom covector, its colour-zero line, is added to \(L_v\).  At
port \(u\), both new bottom covectors are proportional to
\(e_{(u,\lambda_u)}^*\).  Rank three therefore gives
\(\operatorname{rank}L_v\ge2\), and gives the corresponding implication in
(49) whenever that rank equals two.  Finally \(\Psi[0,0,0,0]=0\); hence a
nonzero \(\Psi\) contributes a genuinely off-diagonal coefficient to (47),
proving the last assertion. \(\square\)

Theorem 7 localizes the aligned all-seven-zero survivor to the single
fixed-pair face defect

~~~text
Psi in J,                  Psi[0,0,0,0]=0.             (51)
~~~

Killing (51) is a new common-incidence/mixed-coefficient obligation.  The
pure anchors, local ranks, and equation (42) do not by themselves kill it.

## 5. Branch-II singleton: one pure \(P_4\) companion

Enter (11).  Write

~~~text
a_s=lambda e_(s,i)^*,          y=eta e_(q_1,j)^*,
lambda eta!=0.                                           (52)
~~~

Let

~~~text
pi_y:E_(q_1)->E_(q_1)/K y,
pi_a:E_s->E_s/K a_s,
D_s=(pi_y tensor pi_a)C_s.                              (53)
~~~

### Theorem 8 (singleton quotient supplies a pure \(P_4\))

The colours \(i,j\) are distinct.  If \(k\) is the third colour, then there
are nonzero \(\alpha,\beta\in K\) with \(\alpha\beta=\mu_k\) such that

~~~text
D_s=alpha (bar e_(q_1,k)^* tensor bar e_(s,k)^*),
Pi_(q_1,s)
 =beta product_(v in B-{q_1,s})e_(v,k)^*.              (54)
~~~

Thus the four common incidence maps on \(B-\{q_1,s\}\) pull \(P_4\) back to
a nonzero decomposable tensor.

Maximum-root maximality rules out rank zero for every incidence map and
makes every rank-one row line coordinate.  Exactly one of the following
remains:

~~~text
some one of those four incidence maps has rank 1 and
its row space is a coordinate-covector line;            (55a)

all four have rank >=2, in which case at least two
have rank exactly 2.                                   (55b)
~~~

The implication in (55b) uses the committed complex decomposable
restriction rank-drop theorem and exact characteristic-zero descent.

#### Proof

Apply \(\pi_y\) at \(q_1\) and \(\pi_a\) at \(s\) to (5).  In (11), every
term except \(C_s\otimes\Pi_{q_1s}\) vanishes.  Hence

~~~text
D_s tensor Pi_(q_1,s)
 =sum_(d notin {i,j}) mu_d
   (bar e_(q_1,d)^* tensor bar e_(s,d)^*) tensor
   product_(v in B-{q_1,s})e_(v,d)^*.                  (56)
~~~

If \(i=j\), the right side contains two nonzero summands and has flattening
rank two across

~~~text
{q_1,s} | B-{q_1,s},                                  (57)
~~~

whereas the left side has rank at most one.  Thus \(i\ne j\).  Exactly the
third colour \(k\) survives.  Equality of nonzero simple tensors across
(57) gives (54).

If \(L_v\) had rank zero, the four roots together with \(v\) and any torus
vector at \(v\) would form a five-root.  If \(L_v\) had rank one with
noncoordinate row covector \(f\), choose a torus vector in \(\ker f\);
again the four roots together with \(v\) would form a five-root.  Thus every
rank-one row line is coordinate, proving (55a) as the exact low-rank leaf.

Otherwise all four ranks are at least two.  The
[decomposable \(P_4\) rank-drop theorem](../p4/classifications/pair-geometry/decomposable-restriction-rank-drop/P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md)
then says over \(\mathbb C\) that at least two ranks equal two.  Over an
arbitrary characteristic-zero field, embed the finitely generated
coefficient field into \(\mathbb C\); matrix ranks and (54) are preserved.
This proves (55b). \(\square\)

The theorem does not claim that (55a) is impossible or that (55b) is an
exclusion.  The pure \(P_4\) rank-two
families in the repository show that the latter conclusion is sharp.

## 6. Branch-II two-port: a pure \(P_5\) deletion

Enter (12)--(13).  Define two exact \(P_5\) pullbacks.  For the deletion of
\(t\), restrict the other active port \(s\):

~~~text
Theta_t
 =P_5(
   (L_(q_0)|K(x),0),
   (L_(q_1)|K(y),-d|K(y)),
   (L_s|K(a_s),-c_s|K(a_s)),
   (L_m,-c_m),
   (L_n,-c_n)
  ).                                                        (58)
~~~

For the deletion of \(s\),

~~~text
Theta_s
 =P_5(
   (L_(q_0)|K(x),0),
   (L_(q_1)|K(y), d|K(y)),
   (L_t|K(a_t),-c_t|K(a_t)),
   (L_m,-c_m),
   (L_n,-c_n)
  ).                                                        (59)
~~~

The opposite signs in the \(q_1\) bottom row are the signs of the two
escaping terms in (13).

### Theorem 9 (one two-port deletion is nonzero and decomposable)

At least one of \(\Theta_s,\Theta_t\) is a nonzero decomposable pullback of
\(P_5\).

#### Proof

Restrict (5) at \(q_0,q_1,s\) to \(K(x),K(y),K(a_s)\), respectively.  The
only surviving source terms are the \(-d\otimes a_t\) part of \(C_t\), the
\(-c_s\otimes a_t\) part of \(B_{st}\), and the
\(-a_t\otimes c_v\) parts of \(B_{tv}\), \(v=m,n\).  Factoring the \(t\)-slot
and expanding the bottom row in (58) gives

~~~text
a_t tensor Theta_t
 =sum_(r notin D_t) mu_r e_(t,r)^* tensor
   (e_(q_0,r)^*|K(x)) tensor (e_(q_1,r)^*|K(y)) tensor
   (e_(s,r)^*|K(a_s)) tensor e_(m,r)^* tensor e_(n,r)^*,

D_t={col(x),col(y),col(a_s)},                          (60)
~~~

again omitting undefined colours.  The same flattening-rank argument as in
Lemma 3 proves \(|D_t|\ge2\).  If it has size two, the missing colour forces
\(a_t\) onto that coordinate and makes \(\Theta_t\) nonzero decomposable.  If
it has size three, \(a_t\ne0\) gives \(\Theta_t=0\).

Swapping \(s,t\) and using (59) gives the analogous alternatives for

~~~text
D_s={col(x),col(y),col(a_t)}.                          (61)
~~~

Suppose both tensors were zero.  Then both covers have all three colours.
Each cover contains exactly three covectors, so \(x,y\) are coordinate of
distinct colours and both \(a_s,a_t\) are coordinate of the same third
colour.  Let \(i=\operatorname{col}(x)\).  At the all-colour-\(i\) word in
(5):

- \(H\) and the \(y\otimes c_u\) parts of every \(C\)-edge vanish at the
  \(q_1\)-slot because \(\operatorname{col}(y)\ne i\); the escaping
  \(d\otimes a_s\) and \(-d\otimes a_t\) parts vanish at their active
  port because \(\operatorname{col}(a_s)=\operatorname{col}(a_t)\ne i\);
- every \(A\)-edge vanishes at its active port because
  \(\operatorname{col}(a_s)=\operatorname{col}(a_t)\ne i\); and
- every \(B\)-edge either contains one of those active \(a\)-factors or has
  both \(a\)-factors zero.

Thus the source coefficient is zero, while the target coefficient is
\(\mu_i\ne0\), a contradiction.  Hence one cover has size two and the
corresponding tensor is nonzero decomposable. \(\square\)

Applying (14) gives the complete transposed Branch-II conclusion with every
slot, sign, factor family, and kernel restriction exchanged.  No unlabelled
symmetry is being used.

## 7. Exact controls

### 7.1 Formal companion control

The balanced equations are not contradictory at the level of independently
declared companion tensors.  This control is not a common-incidence graph
point.

Take \(U=\{u_1,u_2,u_3,u_4\}\), put

~~~text
x=e_(q_0,0)^*,                  y=e_(q_1,0)^*,
(lambda_(u_1),lambda_(u_2),lambda_(u_3),lambda_(u_4))
 =(1,1,2,2),

c_u=e_(u,lambda_u)^*,
a_u=rho_u e_(u,lambda_u)^*,
(rho_(u_1),rho_(u_2),rho_(u_3),rho_(u_4))
 =(1,1,2,-5/4).                                         (62)
~~~

Define the physical edge blocks by (8), and declare

~~~text
Pi_Q=mu_0 product_(u in U)e_(u,0)^*,

Pi_(u_1,u_2)
 =-(mu_1/2) product_(v in B-{u_1,u_2})e_(v,1)^*,

Pi_(u_3,u_4)
 =-(4mu_2/3) product_(v in B-{u_3,u_4})e_(v,2)^*,

Pi_P=0 for every other pair P.                         (63)
~~~

Then

~~~text
B_(u_1,u_2)=-2 e_(u_1,1)^* tensor e_(u_2,1)^*,
B_(u_3,u_4)=-(3/4)e_(u_3,2)^* tensor e_(u_4,2)^*.     (64)
~~~

The three nonzero products \(H\otimes\Pi_Q\),
\(B_{u_1u_2}\otimes\Pi_{u_1u_2}\), and
\(B_{u_3u_4}\otimes\Pi_{u_3u_4}\) are exactly the three pure target
summands in (5); hence all (729) coefficients hold.  Formula (8) gives all
six response zeros.  Finally

~~~text
e_2(1,1,2,-5/4)=0,                                    (65)
~~~

so the literal seventh response also vanishes by Lemma 6.

The tensors (63) have not been realized as permanents of one common family
(6).  The control proves only that the complete formal companion identity,
the six responses, and the seventh quartic do not by themselves exclude the
aligned core.  The remaining load-bearing invariant is common-incidence
compatibility of the face defect (51).

### 7.2 Common-incidence anchor-only control

Conversely, common incidence, rank-three local maps, the three pure target
anchors, and the seventh quartic still do not imply the complete mixed
target.  This exact control isolates that boundary.

In the label order \(q_0,q_1,u_0,u_1,u_2,u_3\), take the following six
\(4\) by \(3\) incidence matrices, displayed by rows:

~~~text
L_(q_0)=[
 [ 1,-1,-1], [ 1, 0, 1], [-1, 0,-1], [-1,-1, 1]],

L_(q_1)=[
 [-1,-1,-1], [-1, 0, 1], [-1, 1, 1], [ 0, 1,-1]],

L_(u_0)=[
 [ 0, 1,-1/2], [-1,-1, 0], [ 1,-1, 1/2], [ 1, 1,-1/2]],

L_(u_1)=[
 [-1, 1, 0], [0,0,0], [-1,0,0], [1,1,1]],

L_(u_2)=[
 [0,0,0], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]],

L_(u_3)=[
 [0,-1,-1], [ 1,0,-1], [-1,0,0], [ 1,-1,-1]].       (C1)
~~~

All six matrices have rank three.  Use the aligned factors (62), now with
\(U=(u_0,u_1,u_2,u_3)\).  Direct exact \(4!\)-term permanent expansion gives

~~~text
Pi_Q[0,0,0,0]=2,
Pi_(u_0,u_1)[1,1,1,1]=2,
Pi_(u_2,u_3)[2,2,2,2]=-1,
Pi_Q[2,2,0,0]=1.                                      (C2)
~~~

Together with

~~~text
B_(u_0,u_1)=-2 e_(u_0,1)^* tensor e_(u_1,1)^*,
B_(u_2,u_3)=-(3/4)e_(u_2,2)^* tensor e_(u_3,2)^*,     (C3)
~~~

the three pure contracted coefficients are

~~~text
(mu_0,mu_1,mu_2)=(2,-4,3/4),                          (C4)
~~~

all nonzero.  Equation (65) still gives the literal seventh response zero.
However, at the mixed outside word

~~~text
(q_0,q_1,u_0,u_1,u_2,u_3)=(0,0,2,2,0,0),
~~~

the only surviving edge-companion term is \(H\otimes\Pi_Q\), with
coefficient \(\Pi_Q[2,2,0,0]=1\), while the weighted GHZ target coefficient
is zero.  Thus (C1) is not a complete-target point, a hypothetical witness,
or a counterexample.  It proves exactly that the full mixed coefficients,
not common incidence plus pure anchors and local concision alone, must kill
the face defect.

## 8. Field, nonzero, saturation, and interface ledger

1. **Same actual source.**  Every branch starts with the same GLS4 pair and
   the full complete target.  The inherited source retains
   \(H_Q\ne0\), \(\Pi_Q\ne0\), higher-column survival, raw incidence, and
   maximum-root data.  Only the explicitly displayed consequences are used
   here.

2. **Target saturation.**  The target saturation is exactly

   ~~~text
   mu_0 mu_1 mu_2!=0.                                  (66)
   ~~~

   Active branch factors declared nonzero in (8), (12), (39), and (52) are
   never treated as nonzero outside their declared strata.

3. **Kernel restrictions.**  Equations (27)--(28), (36), and (58)--(59)
   are restrictions to exact linear kernels.  No basis, kernel coordinate,
   or minor is inverted.  The pure identities are kept in multiplied form
   before any optional normalization of a declared nonzero scalar.

4. **Coordinate cover.**  A noncoordinate or zero covector contributes no
   colour to a cover.  The cover alternatives are exhaustive because they
   are derived from the flattening rank of the full restricted target, not
   from a support sample.  The no-pure case is taken only after every cover
   has size three.

5. **Quartic field scope.**  Torus kernels in Proposition 2 use that a
   noncoordinate covector over an infinite field has a fully supported zero.
   Lemma 1 is exact over \(\mathbb C\) and descends to every
   characteristic-zero field through a finitely generated coefficient
   field.  Degenerate and zero quadratic forms are included; no determinant
   of \(q\) is saturated.

6. **Balanced divisions.**  The ratios \(\rho_u=\alpha_u/\gamma_u\) and
   \(p=\mu_0/(\xi\eta)\) use exactly the declared nonzeros in (39).  The
   preceding identities (44) and \(h\Psi\in J\) are polynomial multiplied
   forms.  No exceptional divisor is removed.

7. **Seventh response.**  Equation (9) is an additional hypothesis for the
   literal all-seven-zero leaf.  Branch-I coverage, Branch-II conclusions,
   and the augmented identity do not silently infer it from the six pair
   responses.

8. **\(P_4\) local ranks.**  The pure companion (54) alone gives no lower
   bound on its four incidence-map ranks.  The committed rank-drop theorem
   is invoked only on the explicit all-ranks-at-least-two branch (55b).

9. **Pure \(P_5\) interface.**  The outputs (31), (37), (58), and (59) are
   nonzero decomposable images of \(P_5\) on the exact displayed restricted
   local spaces.  They are not asserted concise, injective, or equivalent to
   \(\Delta_3\).  This is a new open pure-compression interface, not the
   weighted \(P_5\to\Delta_3\) node reached by GLS13.  No downstream
   exclusion is imported.

10. **Balanced \(P_6\) interface.**  The maps in Theorem 7 are injective,
    but (47) is the desired weighted diagonal restriction in the displayed
    coordinates only at \(\Psi=0\).  No GL-equivalence or nonrestriction
    conclusion is made at \(\Psi\ne0\).

11. **No selector saturation.**  Nothing here divides by or saturates
    against a response coordinate, observable minor, nuisance determinant,
    selector coefficient, alignment form, activity factor, or target-module
    denominator.  The synthetic bottom rows are permanent reductions, not
    physical residual vertices or GLD selectors.

12. **Pointwise cover.**  The Branch-I and Branch-II alternatives are
    pointwise on the inherited all-six-response rank-one locus.  There is no
    generic, sampled, modular, numerical, or finite-support-atlas inference.

## 9. Proof-DAG consequence and exact open boundary

This package is GLS14, a sibling of GLS13 rather than its descendant.  The exact
determinant-divisor topology is

~~~text
GLS11 rank-one trichotomy
  -> Branch III singleton: excluded by GLS12;
  -> Branch III two-port: weighted P_5 -> Delta_3 by GLS13;
  -> Branch I:
       pure/decomposable P_5 deletion or cross pullback,
       or same-coordinate balanced core, which splits as
          Phi!=0: the seventh response is nonzero, but no legal
                  selector/attachment follows,
          Phi=0: the partitions align, e_2=0, and Psi lies in J;
  -> Branch II and transpose:
       singleton pure/decomposable P_4 companion,
       or two-port pure/decomposable P_5 deletion.       (67)
~~~

The exact evidence ledger is

~~~text
arbitrary-rank Sym(a b q) subrank <=2:          PROVED;
Branch-I eight coverage identities:             PROVED;
Branch-I balanced no-pure cover:                 PROVED;
seventh-response alignment/e_2 condition:        PROVED;
balanced augmented-P_6 face normal form:         PROVED;
Branch-II singleton pure P_4 companion:          PROVED;
Branch-II two-port pure P_5 deletion:            PROVED;
transpose coverage:                              PROVED;

focused primary verifier:                        PASS;
independent no-import audit:                      PASS;
hostile theorem/scope review:                     PASS;
formalization:                                    NONE;

pure P_4/P_5 downstream exclusions:              OUTSIDE / OPEN;
balanced Phi!=0 nonzero-response selector:       OPEN;
balanced common-incidence face defect Psi:        OPEN;
weaker response-zero and absorption fibres:       OPEN;
legal same-Q selector/attachment package:         OPEN;
supply-and-target strategic node:                 OPEN;
global Krenn--Gu conjecture:                       UNRESOLVED. (68)
~~~

On the same-coordinate Branch-I leaf with \(\Phi\ne0\), the nonzero value
makes the physical seventh response nonzero by the exact GLS11 identity.
Response nonvanishing alone supplies no legal nuisance-annihilating selector.  That
leaf therefore returns to the response-visible selector/attachment
obligation rather than disappearing from the cover.  On the aligned
\(\Phi=0\) leaf, the smallest remaining obligation is to prove \(\Psi=0\)
from the complete common-incidence equations, or to prove an exact
downstream theorem that accepts the nonzero face-defect normal form.  On the
other leaves, the theorem stops at the stated pure \(P_4/P_5\) permanent
interfaces.  Closing those downstream restriction/nonrestriction nodes is
outside this package.

The strategic node remains open also because this theorem assumes all six
same-\(Q\) pair responses vanish.  It does not cover weaker response-zero
patterns, nonzero-response absorption, exceptional selector fibres, or the
remaining legal same-\(Q\) target-attachment gates.

## 10. Verification evidence

The
[focused exact primary verifier](verify_four_root_determinant_divisor_rank_one_contained_and_one_sided_permanent_reduction.py)
replays:

1. replay the two-bottom-row minors and all (729) coefficients of (24);
2. reconstruct the restricted Laplace identities (33), (37), (56), and
   (60), including every sign and labelled complement;
3. exhaust the finite three-colour deletion-cover count and the six
   two-subset words in Lemma 6;
4. replay the aligned formula (47), membership (48), and all six one-mode
   flattening ranks;
5. check the Branch-II all-\(x\) contradiction and the formal control
   (62)--(65); and
6. replay the arbitrary-rank radical gate before importing the committed
   kernel-type quartic proof.

The
[independent no-import audit](audit_four_root_determinant_divisor_rank_one_contained_and_one_sided_permanent_reduction.py)
does not read or import that verifier.  It uses standard-library exact
arithmetic and a different representation: direct perfect-matching and
row-assignment expansion for the augmented permanents, finite set partitions
for the coverage proof, exact kernel bases, and direct multilinear contraction
for the arbitrary-rank quartic gate.  Both exact scripts pass.  The audit does
not independently re-prove the two explicitly imported downstream dependency
theorems.

The
[hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_CONTAINED_AND_ONE_SIDED_PERMANENT_REDUCTION_REVIEW_2026-08-20.md)
passes.  It audits especially:

- that coverage, rather than unexplained cofactor vanishing, is the initial
  Branch-I split;
- every restricted domain and the signs \(-d,+d\) in (58)--(59);
- the arbitrary-rank radical step in Lemma 1;
- the distinction between the formal companion control and common physical
  incidence;
- the conditional rank floor in (55); and
- the absence of any \(P_4/P_5/P_6\) downstream overclaim.

Dependencies:

- [GLS11 determinant-divisor rank-one trichotomy](FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md);
- [GLS12 rank-two and singleton-triangle exclusion](FOUR_ROOT_DETERMINANT_DIVISOR_RANK_TWO_CORE_AND_RANK_ONE_SINGLETON_TRIANGLE_EXCLUSION_THEOREM.md);
- [GLS13 rank-one two-port \(P_5\to\Delta_3\) extraction](FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_THEOREM.md);
- [arbitrary-order quartic kernel-type proof](SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md);
- [decomposable \(P_4\) rank-drop theorem](../p4/classifications/pair-geometry/decomposable-restriction-rank-drop/P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md);
- [order-five remaining-obligation ledger](../p5/frontier/P5_DELTA3_OBLIGATION_LEDGER.md); and
- [order-six permanent package](../p6/README.md).

No external literature premise is used.
