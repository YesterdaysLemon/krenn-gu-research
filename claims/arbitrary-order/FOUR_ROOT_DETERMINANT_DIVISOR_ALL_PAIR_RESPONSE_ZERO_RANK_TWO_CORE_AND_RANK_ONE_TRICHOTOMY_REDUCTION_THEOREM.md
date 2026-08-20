# Four-root determinant-divisor all-pair-response-zero rank-two core and rank-one trichotomy reduction

## Status

**Proved exact characteristic-zero reduction.  The focused primary verifier,
genuinely independent no-import audit, and
[hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_REDUCTION_REVIEW_2026-08-20.md)
pass.**

Start with an actual hypothetical ternary GHZ witness whose
maximum-cardinality torus root has order four and surplus two.  Fix the same
residual pair \(Q\) supplied by GLS4, and assume that all six same-\(Q\)
pair-response tensors vanish identically.  GLS10 excludes the full-rank
stratum.  On the determinant divisor, the GLS4 activity of \(Q\) excludes
rank zero, so only ranks one and two remain.

This theorem proves the following support-free pointwise reduction.

1. At rank two, every \(Q\)-to-port block is contained on its residual shore
   in the corresponding support of \(H_Q\).  All simultaneous and one-sided
   quotient escapes are excluded by maximum-root maximality and complete
   mixed target coefficients.  The surviving locus is one coordinate-free
   \(2\) by \(2\) conformal core with exactly two active combined ports.
   Each active port has a fixed coordinate blocker in its combined row span,
   and both block every regular torus zero.  The core also obeys an exact
   four-port quotient target, but is not excluded here.
2. At rank one, the six response equations have an exhaustive quotient
   trichotomy: double containment, exactly one escaping shore, or two
   escaping shores.  The latter two branches have support of size at most two
   and admit the explicit labelled normal forms below.  The complete target
   sharpens the two-sided branch to a pure monomial-triangle or two-site
   insertion identity, but no common-root integrability contradiction is
   proved.
3. Six pair-response zeros do not imply the seventh, four-port response zero
   on the determinant divisor.  A denominator-free hafnian identity records
   the additional exact condition.

The theorem does not exclude the rank-two conformal core, the rank-one
double-contained or one-sided cores, or the remaining rank-one
common-permanent configurations.  It also says nothing about a GLS7 branch
where only some response is identically zero, or about nonzero-response
absorption and exceptional selector fibres.  It supplies no legal named
downstream detector package.  The supply-and-target-attachment strategic
node remains **OPEN**, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Quantified source and labelled tensor convention

Let \(K\) be a characteristic-zero field.  The actual-witness application is
over \(K=\mathbb C\).  Statements using torus points require the displayed
points over \(K\); in the actual application this causes no rational-point
qualification.

Let every local covector space be three-dimensional with fixed target basis

~~~text
E_v=V_v^*,
e_(v,0)^*, e_(v,1)^*, e_(v,2)^*.                       (1)
~~~

Let

~~~text
Omega=R disjoint-union B,       |R|=4,       |B|=6,
Q={q_0,q_1} subset B,           U=B-Q={u_0,u_1,u_2,u_3}. (2)
~~~

The vectors \(x_r\in(K^*)^3\), \(r\in R\), form a
maximum-cardinality torus-root configuration.  Thus

~~~text
W_(r,s)(x_r,x_s)=0                    for r!=s in R,     (3)
~~~

and no five vertices anywhere in \(\Omega\) admit fully supported vectors
which annihilate every internal edge.

The pair \(Q\) is the same physical pair supplied by GLS4.  Put

~~~text
X=E_(q_0),              Y=E_(q_1),              P_u=E_u,
H=H_Q=W_(q_0,q_1) in X tensor Y.                       (4)
~~~

GLS4 activity and individual higher-column survival give, on this same pair,

~~~text
H!=0,        Pi_Q!=0,
[G_(B-Q)]!=0 modulo every order-four-and-higher column. (5)
~~~

The source package also supplies a nonzero raw two-root incidence polynomial,
and GLS6/GLS7 allow a fully supported residual contraction retaining the
nonzero \(H_Q\) and raw-incidence gates.  None of those contraction,
higher-column, or selector data is used in the implications below; it remains
available at the resulting survivor.

For \(u\in U\) and distinct \(u,v\in U\), write

~~~text
A_u=W_(q_0,u) in X tensor P_u,
C_u=W_(q_1,u) in Y tensor P_u,
B_uv=W_(u,v) in P_u tensor P_v.                        (6)
~~~

Every tensor slot is labelled.  The symbol \(\boxtimes\) means ordinary
tensor product followed by the unique canonical shuffle into the named
slots.  In the slot order \((q_0,q_1,u,v)\),

~~~text
(A_u boxtimes C_v)[a,b,s,t]=A_u[a,s] C_v[b,t].         (7)
~~~

Assume all six full pair-response identities

~~~text
Z_uv
 =H boxtimes B_uv+A_u boxtimes C_v+A_v boxtimes C_u
 =0                         for every {u,v} subset U.   (8)
~~~

These are tensor identities in \(X\otimes Y\otimes P_u\otimes P_v\),
not vanishings after one residual evaluation.

For every pair \(P\subset B\), let \(\Pi_P\) be the four-root complementary
permanent tensor on \(B-P\).  The complete contracted target identity is

~~~text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(c=0)^2 mu_c product_(v in B)e_(v,c)^*,
mu_0 mu_1 mu_2!=0.                                     (9)
~~~

Equation (9) includes all \(3^6\) outside coefficients.

For a tensor \(T\in E\otimes F\), define its intrinsic supports by

~~~text
L(T)=image(F^vee -> E),          R(T)=image(E^vee -> F). (10)
~~~

Put

~~~text
L=L(H) subset X,                M=R(H) subset Y,
pi_X:X -> X/L,                  pi_Y:Y -> Y/M,
bar A_u=(pi_X tensor id)A_u,
bar C_u=(pi_Y tensor id)C_u.                           (11)
~~~

Whole-block support below means nonvanishing of a tensor such as \(A_u\).
It is distinct from the coordinate support of a covector.

## 2. Torus and quotient-cross lemmas

### Lemma 1 (torus zeros)

Over an infinite field, a nonzero covector has no zero on \((K^*)^3\) if and
only if it is a nonzero coordinate covector.  A nonzero bilinear form in
\((K^3)^*\otimes(K^3)^*\) has no zero on
\((K^*)^3\times(K^*)^3\) if and only if it is a nonzero coordinate
monomial.

#### Proof

If a covector has at least two nonzero coordinates, choose all but one torus
coordinates away from the one forbidden hyperplane and solve for the last
coordinate.  This gives a fully supported kernel vector.  A coordinate
covector is visibly nonzero on the torus.

For a bilinear form with at least two nonzero rows, choose a torus vector on
the second shore so that the resulting first-shore covector has at least two
nonzero coordinates, and apply the first assertion.  If there is exactly one
nonzero row, either that row is coordinate or the first assertion gives a
torus kernel vector on the second shore.  This proves the claim. \(\square\)

### Lemma 2 (quotient cross and support collapse)

Projecting (8) in both residual slots gives

~~~text
bar A_u boxtimes bar C_v+bar A_v boxtimes bar C_u=0
                                      for u!=v.         (12)
~~~

If both quotient families are nonzero, then

~~~text
T={u:bar A_u!=0}={u:bar C_u!=0},       1<=|T|<=2.       (13)
~~~

If \(T=\{s,t\}\), there are nonzero

~~~text
bar a in X/L,       bar c in Y/M,
alpha_s in P_s,     alpha_t in P_t,      tau in K^*    (14)
~~~

such that, after nonzero rescaling,

~~~text
bar A_s=bar a tensor alpha_s,
bar A_t=bar a tensor alpha_t,
bar C_s=tau bar c tensor alpha_s,
bar C_t=-tau bar c tensor alpha_t.                    (15)
~~~

Moreover, in this two-sided escape case the whole \(A,C\) supports are
contained in \(T\).  If \(|T|=2\), (15) lifts to

~~~text
A_s=a tensor alpha_s,          A_t=a tensor alpha_t,
C_s=tau c tensor alpha_s,      C_t=-tau c tensor alpha_t, (16)
~~~

where \(\pi_X(a)\ne0\) and \(\pi_Y(c)\ne0\).  For either
\(|T|=1\) or \(2\),

~~~text
B_uv=0                         for every {u,v} subset U. (17)
~~~

#### Proof

Suppose \(u\) belongs to the support of \(\bar A\) but not that of
\(\bar C\), and choose \(v\) with \(\bar C_v\ne0\).  Then \(u\ne v\).
In (12) the first simple product is nonzero and the second is zero, a
contradiction.  This proves one support inclusion; the other is symmetric.

For two distinct active ports, flatten (12) with row slots
\((X/L,u)\) and column slots \((Y/M,v)\).  The first term is the rank-one
outer product

~~~text
vec(bar A_u) vec(bar C_v)^T,                           (18)
~~~

whereas the second, up to labelled row and column permutations, has rank

~~~text
rank(bar A_v) rank(bar C_u).                           (19)
~~~

Equality forces both ranks in (19) to be one.  The opposite flattening gives
rank one for the other two blocks.  Uniqueness of the factor lines of a
nonzero four-factor simple tensor gives common residual lines and a common
local line at each active port:

~~~text
bar A_u=s_u bar a tensor alpha_u,
bar C_u=t_u bar c tensor alpha_u,
s_u t_v+s_v t_u=0.                                    (20)
~~~

All \(s_u,t_u\) are nonzero on this declared active chart.  If three ports
were active, the ratios \(r_u=s_u/t_u\) would satisfy
\(r_u=-r_v=-r_w\) and \(r_v=-r_w\), hence \(2r_v=0\).
Characteristic zero excludes this.  This proves (13)--(15).

Projecting (8) only in the \(q_0\)-slot gives

~~~text
bar A_u boxtimes C_v+bar A_v boxtimes C_u=0.           (21)
~~~

If \(u\in T\) and \(v\notin T\), (21) forces \(C_v=0\).
The symmetric one-slot projection forces \(A_v=0\).  In the two-port case,
substitution of (15) into the one-slot equations and uniqueness of simple
factor lines gives the full lifts (16).  Their two cross terms cancel on the
active pair.  Every other pair contains at most one active whole block.
Since \(H\ne0\), (8) then gives (17).  The same last argument works on the
singleton support. \(\square\)

The ratios in this proof occur only on the explicitly active nonzero charts.
Equations (12) and (20) before normalization are polynomial.

## 3. Rank zero and the rank-two double-contained core

### Proposition 3 (rank zero is absent for the GLS4 pair)

The selected pair \(Q\) cannot satisfy \(\operatorname{rank}H=0\).

#### Proof

GLS4 selects \(Q\) with \(H_Q\otimes\Pi_Q\ne0\).  In particular \(H_Q\ne0\),
whereas rank zero means \(H_Q=0\). \(\square\)

The nonzero \(\Pi_Q\) or its higher-column quotient survival alone would not
prove this; activity of the same selected physical pair is load-bearing.

### Theorem 4 (rank-two quotient escapes are impossible)

Assume (1)--(11), (8), and the complete target (9).  If

~~~text
rank H=2,                                                (22)
~~~

then for every \(u\in U\),

~~~text
A_u in L tensor P_u,             C_u in M tensor P_u.   (23)
~~~

Equivalently, every \(\bar A_u,\bar C_u\) in (11) is zero.  Neither whole
block family is identically zero.

This is a pointwise implication on the actual witness locus.  It does not
assert that the surviving double-contained locus is empty.

#### Proof

We exclude the two-sided and one-sided quotient escapes.

#### Case 1: both quotient families escape

Lemma 2 supplies a common support \(T\) of size one or two, full whole-block
support contained in \(T\), and \(B_{uv}=0\) for every pair.

If \(T=\{t\}\), the only internal edge on \(\{q_0\}\cup U\) is \(A_t\).
If it had a torus zero, adjoining arbitrary torus vectors at the other three
ports would give a five-root.  Lemma 1 makes \(A_t\) a coordinate monomial.
The same argument makes \(C_t\) a coordinate monomial.  Thus

~~~text
A_t=lambda e_(q_0,i)^* tensor e_(t,a)^*,
C_t=nu     e_(q_1,j)^* tensor e_(t,b)^*,              (24)
~~~

with \(\lambda,\nu\ne0\).

If \(T=\{s,t\}\), (16) and the same five-root argument make the common
residual covectors coordinate:

~~~text
Ka=K e_(q_0,i)^*,             Kc=K e_(q_1,j)^*.       (25)
~~~

If both local factors \(\alpha_s,\alpha_t\) were noncoordinate, torus kernel
vectors at \(s,t\), together with arbitrary torus vectors at \(q_0\) and the
two inactive ports, would give a five-root.  Hence at least one local factor
is coordinate.  This last fact is not needed in the target contradiction.

In either support size, the residual coordinate lines in (24) or (25) lie
outside \(L\) and \(M\), respectively, because their quotient images are
nonzero.  Let

~~~text
rho_i:X -> X/K e_(q_0,i)^*,
rho_j:Y -> Y/K e_(q_1,j)^*.                            (26)
~~~

Applying these quotients to the two residual slots of the complete identity
(9) kills every \(A,C\) term; all \(B\) terms are zero.  Write
\(\bar e\) for the appropriate quotient class.  Hence

~~~text
H' tensor Pi_Q
 =sum_(c notin {i,j}) mu_c
   bar e_(q_0,c)^* tensor bar e_(q_1,c)^*
   tensor product_(u in U)e_(u,c)^*,
H'=(rho_i tensor rho_j)H.                              (27)
~~~

The restrictions \(\rho_i|_L\) and \(\rho_j|_M\) are injective: a
two-dimensional support cannot meet an outside coordinate line nontrivially.
Therefore \(\operatorname{rank}H'=2\).

If \(i=j\), the right side of (27) has flattening rank two across
\(Q\mid U\), while the left side has flattening rank one.  If \(i\ne j\),
only the third colour remains, so equality of nonzero simple tensors would
make \(H'\) rank one.  Both alternatives contradict
\(\operatorname{rank}H'=2\).  Thus a two-sided escape is impossible.

#### Case 2: exactly one quotient family escapes

After exchanging the two residual shores if necessary, assume

~~~text
bar A_u=0 for every u,           bar C_v!=0 for some v. (28)
~~~

The whole \(A\) family is nonzero.  Otherwise (8) gives every \(B_{uv}=0\),
and \(\{q_0\}\cup U\) with arbitrary torus vectors is a five-root.

Projecting (8) only modulo \(M\) gives

~~~text
A_u boxtimes bar C_v+A_v boxtimes bar C_u=0.           (29)
~~~

The proof of Lemma 2, with \(A_u\) in place of \(\bar A_u\), gives

~~~text
T={u:A_u!=0}={u:bar C_u!=0},       1<=|T|<=2.          (30)
~~~

Suppose first that \(T=\{t\}\).  For an inactive \(v\), \(A_v=0\) and
\(C_v\in M\otimes P_v\), so

~~~text
H boxtimes B_tv+A_t boxtimes C_v=0.                    (31)
~~~

Flatten with row slots \((q_0,t)\) and column slots \((q_1,v)\).
The first term has rank \(2\operatorname{rank}B_{tv}\); the second is a
rank-one outer product if it is nonzero.  Equality is possible only when
both vanish.  Thus \(B_{tv}=C_v=0\).  Repeating this and then considering
inactive pairs gives every \(B_{uv}=0\) and whole \(C\)-support contained in
\(\{t\}\).

By Lemma 1 a rank-two bilinear form has a torus zero.  At such a zero, the
five vertices

~~~text
Q union (U-{t})                                         (32)
~~~

have no other possibly nonzero internal edge.  They form a five-root,
contradicting maximality.

It remains that \(T=\{s,t\}\).  The realignment in (29) gives

~~~text
A_s=a tensor alpha_s,           A_t=a tensor alpha_t,
a in L-{0}.                                             (33)
~~~

The same inactive-port rank argument gives \(C_v=0\) and every incident
\(B_{uv}=0\) for \(v\notin T\).  On the active pair, apply the quotient
\(X\to X/Ka\) in the \(q_0\)-slot.  It kills both cross terms, while its
image of \(H\) is nonzero of rank one.  Hence \(B_{st}=0\).  The remaining
cross equality lifts the quotient factors to

~~~text
C_s=tau c tensor alpha_s,
C_t=-tau c tensor alpha_t,
c notin M,                  tau in K^*.                (34)
~~~

A torus kernel of \(a\), with arbitrary port vectors, would make
\(\{q_0\}\cup U\) a five-root.  Thus \(a\) is coordinate.  The symmetric
argument on \(\{q_1\}\cup U\) makes \(c\) coordinate.  Write, after absorbing
nonzero scalars,

~~~text
a=e_(q_0,i)^*,                  c=e_(q_1,j)^*.         (35)
~~~

Each local factor \(\alpha_s,\alpha_t\) is coordinate.  If, for example,
\(\alpha_s\) were noncoordinate, choose a torus zero of \(H\), a torus
kernel vector of \(\alpha_s\), and arbitrary torus vectors at the two
inactive ports.  The resulting vectors on \(Q\), \(s\), and the two inactive
ports give a five-root.  The same argument applies to \(\alpha_t\).

Apply the quotients (26) to (9).  Here \(Ke_i^*\subset L\), so
\(\rho_i|_L\) has rank one, whereas \(Ke_j^*\not\subset M\), so
\(\rho_j|_M\) is injective.  Consequently

~~~text
rank H'=1,                      H'!=0.                  (36)
~~~

As in (27), the case \(i=j\) has a rank-two target flattening and is
impossible.  Thus \(i\ne j\); let \(k\) be the third colour.  Equality of
the remaining nonzero simple tensors yields a scalar \(\lambda\ne0\) and
the denominator-free identities

~~~text
H'=lambda bar e_(q_0,k)^* tensor bar e_(q_1,k)^*,
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*.            (37)
~~~

In the pure colour-\(i\) coefficient of (9), neither the \(Q\)-term, any
\(C\)-term, nor any \(B\)-term contributes.  At least one of the two
coordinate local factors is therefore the \(i\)-coordinate covector.
The pure colour-\(j\) coefficient similarly forces the other local factor
to be the \(j\)-coordinate covector.

Now evaluate all four \(U\)-slots of (9) at the word \(kkkk\), leaving the
two \(Q\)-slots open.  Every \(A,C\) term is killed by its local
\(i\)- or \(j\)-factor and every \(B\) term is zero.  Using (37) gives

~~~text
H tensor Pi_Q
 =mu_k e_(q_0,k)^* tensor e_(q_1,k)^*
       tensor product_(u in U)e_(u,k)^*.               (38)
~~~

Since \(\Pi_Q\ne0\), (38) forces \(H\) to have rank one, contrary to (22).
The opposite one-sided escape is excluded by exchanging the residual slots.

Only the case \(\bar A_u=\bar C_u=0\) for every \(u\) remains, which is (23).
If every \(A_u\) vanished, then (8) would give every \(B_{uv}=0\) and
\(\{q_0\}\cup U\) would be a five-root.  Thus the \(A\) family is nonzero;
the \(C\) statement is symmetric. \(\square\)

## 4. Exact structure retained by the rank-two survivor

### Corollary 5 (the conformal \(2\) by \(2\) core)

Under Theorem 4, define the correctly labelled cross tensor

~~~text
Xi_uv=A_u boxtimes C_v+A_v boxtimes C_u
 in (L tensor M) tensor P_u tensor P_v.                 (39)
~~~

Then

~~~text
class(Xi_uv)=0
 in ((L tensor M)/K H) tensor P_u tensor P_v.           (40)
~~~

Conversely, (40) says that there is a unique
\(D_{uv}\in P_u\otimes P_v\) with

~~~text
Xi_uv=H boxtimes D_uv,                 B_uv=-D_uv.      (41)
~~~

If

~~~text
theta_H:L tensor M -> K,               theta_H(H)=1,    (42)
~~~

then

~~~text
D_uv=(theta_H tensor id_(P_u tensor P_v))(Xi_uv).      (43)
~~~

Formula (43) is independent of the choice of \(\theta_H\), because (40)
has already placed \(\Xi_{uv}\) in the subspace
\(KH\otimes P_u\otimes P_v\).

#### Proof

Theorem 4 puts every cross term in the labelled space in (39).  Equation (8)
is exactly

~~~text
H boxtimes B_uv+Xi_uv=0,
~~~

which proves (40)--(41).  Tensoring the one-dimensional inclusion
\(KH\subset L\otimes M\) with \(P_u\otimes P_v\) makes the coefficient
\(D_{uv}\) unique.  Applying (42) gives (43). \(\square\)

The port factors in (40) are load-bearing.  The untyped expression
\([\Xi_{uv}]=0\) merely in \((L\otimes M)/KH\) would not state the tensor
equation.

### Lemma 6 (mixed-vector conformal kernel)

Let \(L,M\) be two-dimensional, let \(H\in L\otimes M\) have rank two, and
put

~~~text
beta((a,c),(a',c'))
 =[a tensor c'+a' tensor c] in (L tensor M)/K H.       (44)
~~~

If \(w=(a,c)\) has \(a\ne0\) and \(c\ne0\), define

~~~text
K_w={w' in L direct-sum M: beta(w,w')=0}.              (45)
~~~

Then \(K_w\) contains no two nonzero vectors which are mutually
\(\beta\)-orthogonal.

#### Proof

Choose bases of \(L,M\) in which \(H=I_2\).  The stabilizer of \(I_2\) acts
as

~~~text
(a,c) -> (S a,S^(-T)c),              S in GL_2(K),     (46)
~~~

so take \(a=(1,0)^T\) and write \(c=(c_1,c_2)^T\).
For \(w'=((x,y)^T,(p,q)^T)\), the condition
\(\beta(w,w')=0\) is exactly

~~~text
q+x c_2=0,
y c_1=0,
p+x c_1-y c_2=0.                                      (47)
~~~

If \(c_1\ne0\), (47) gives

~~~text
K_w=K((1,0)^T,(-c_1,-c_2)^T).                         (48)
~~~

Its nonzero generator is mixed and is not orthogonal to itself, because
twice a nonzero rank-one matrix cannot be a scalar multiple of \(I_2\).
Thus no two nonzero members are mutually orthogonal.

If \(c_1=0\), then \(c_2\ne0\), and

~~~text
K_w={
 ((x,y)^T,c_2(y,-x)^T):x,y in K
}.                                                     (49)
~~~

For two such vectors with parameters \((x,y)\) and \((X,Y)\), mutual
orthogonality forces

~~~text
xX=0,                 yY=0,                 xY+Xy=0.   (50)
~~~

Because \(2\ne0\), if one parameter pair is nonzero these equations make the
other pair zero.  This proves the lemma. \(\square\)

### Corollary 7 (exactly two combined port supports)

For each \(u\in U\), define

~~~text
Phi_u:P_u^vee -> L direct-sum M,
z |-> (A_u(-,z),C_u(-,z)),
W_u=im Phi_u.                                           (51)
~~~

On the rank-two core:

1. no \(W_u\) contains a nonzero vector in \(L\oplus0\) or \(0\oplus M\);
2. both projections \(W_u\to L\) and \(W_u\to M\) are injective, so
   \(\dim W_u\le2\); and
3. exactly two ports have \(W_u\ne0\).

#### Proof

Corollary 5 says

~~~text
beta(W_u,W_v)=0                         for u!=v.       (52)
~~~

Suppose \(W_u\) contained \((a,0)\) with \(a\ne0\).  For \(v\ne u\),
(52) says \(a\otimes c_v\in KH\) for every
\((a_v,c_v)\in W_v\).  A rank-one tensor cannot be a nonzero scalar multiple
of the rank-two tensor \(H\), so \(c_v=0\).  Hence \(C_v=0\) for every
\(v\ne u\).  Theorem 4 says the whole \(C\) family is nonzero, so
\(C_u\ne0\).

For \(v\ne u\), response equation (8) is now

~~~text
H boxtimes B_uv+A_v boxtimes C_u=0.                   (53)
~~~

Flatten with row slots \((q_0,v)\) and column slots \((q_1,u)\).
If the second term is nonzero it has rank one, whereas the first has rank
\(2\operatorname{rank}B_{uv}\).  Therefore both terms vanish:
\(A_v=B_{uv}=0\).  Responses between two ports outside \(u\) then give their
\(B\)-blocks zero as well.  A torus zero of rank-two \(H\), together with
arbitrary torus vectors at the three ports outside \(u\), gives a five-root
on \(Q\) plus those ports.  This contradiction excludes a pure-\(L\)
vector.  The pure-\(M\) case is symmetric.  The injectivity and dimension
claim follow.

Choose a port \(u\) with \(W_u\ne0\) and any nonzero \(w\in W_u\).  It is
mixed by the first part.  Every \(W_v\), \(v\ne u\), lies in \(K_w\).  If
two distinct other ports \(v,t\) had nonzero images, choose nonzero
\(w_v\in W_v,w_t\in W_t\).  Equation (52) makes them mutually
\(\beta\)-orthogonal, contradicting Lemma 6.  Thus at most two combined
port supports are nonzero.

At least one support is nonzero because both whole block families are
nonzero.  If exactly one, say \(W_t\), were nonzero, every cross term in
(8) would vanish and hence every \(B_{uv}=0\).  A torus zero of \(H\) would
then make \(Q\cup(U-\{t\})\) a five-root.  Exactly two supports remain.
\(\square\)

This is a derived finite support bound, not a support-mask enumeration.  It
does not by itself classify the two surviving combined images or exclude
their common-root companion data.

### Corollary 7.1 (fixed coordinate blocker at each active port)

Let \(T=\{s,t\}\) be the two active combined ports from Corollary 7.  For
each \(u\in T\),

~~~text
ker Phi_u intersect (K^*)^3=empty,                     (53a)
~~~

and therefore there is a fixed colour \(d_u\) such that

~~~text
e_(u,d_u)^* in im(Phi_u^*)
 =span of all residual coefficient rows of A_u and C_u. (53b)
~~~

For the actual complex witness, (53a)--(53b) hold unconditionally.  Over a
general characteristic-zero field, the same conclusion holds whenever the
rank-two form \(H\) has a fully supported torus zero over that field.

#### Proof

Corollary 7 gives \(\dim W_u\le2\), so the kernel of the map
\(\Phi_u:P_u^\vee\to L\oplus M\) is nonzero.  Every \(A,C\) block at the two
inactive ports is zero.  Their mutual \(B\)-edge and every \(B\)-edge joining
one of them to an active port are also zero by (8) and \(H\ne0\).

If a fully supported \(z_u\in\ker\Phi_u\) existed, choose a fully supported
torus zero \((z_0,z_1)\) of the rank-two form \(H\) and arbitrary torus
vectors at the two inactive ports.  On the five vertices consisting of
\(Q\), \(u\), and those inactive ports, the \(H\)-edge is killed by
\((z_0,z_1)\), the two \(Q\)-to-\(u\) edges are killed by \(z_u\), and every
remaining edge is already zero.  This is a forbidden five-root.

Thus \(\ker\Phi_u\) misses the torus.  Over an infinite field, a linear
subspace missing the torus is contained in a coordinate hyperplane.
Annihilator duality identifies
\((\ker\Phi_u)^\perp=\operatorname{im}\Phi_u^*\), proving (53b).
\(\square\)

### Corollary 8 (the quotient four-port target \(Q4\))

For \(\{u,v\}\subset U\), the companion \(\Pi_{uv}\) has labelled slots
\(Q\cup(U-\{u,v\})\).  Define

~~~text
widehat Pi_uv
 =((pi_X tensor pi_Y) tensor id_(U-{u,v}))Pi_uv
 in (X/L) tensor (Y/M) tensor
       tensor_(w in U-{u,v})P_w.                       (54)
~~~

Apply \(\pi_X,\pi_Y\) to the two \(Q\)-slots of (9).  The \(P=Q\) term and
every cross-edge term vanish by (23); only \(P\subset U\) remains.  Thus

~~~text
sum_({u,v} subset U)
 sh_({u,v},Q union (U-{u,v}))(B_uv tensor widehat Pi_uv)
 =sum_(c=0)^2 mu_c
   pi_X(e_(q_0,c)^*) tensor pi_Y(e_(q_1,c)^*)
   tensor product_(w in U)e_(w,c)^*.                   (55)
~~~

Both quotient spaces in (55) are one-dimensional.  Keeping them labelled
and untrivialized avoids a choice of generator or scale.  Some displayed
target classes may be zero.

The selected nonzero \(\Pi_Q\) disappears from (55).  Consequently \(Q4\)
alone cannot couple GLS4 companion survival back to this core; the
unprojected target or common-root companion integrability remains necessary.

### Corollary 9 (moving two-blocker condition)

Let \((z_0,z_1)\) be a fully supported regular torus zero of \(H\):

~~~text
H(z_0,z_1)=0,
z_0|_L!=0,                       z_1|_M!=0.             (56)
~~~

For the actual complex rank-two block, such points form a nonempty open
subset of the torus-zero hypersurface.  Over a general \(K\), the following
conclusion is asserted for every \(K\)-rational point satisfying (56).

Put

~~~text
a_u=A_u(z_0,-) in P_u,         c_u=C_u(z_1,-) in P_u,
K_u=ker a_u intersect ker c_u subset P_u^vee.          (57)
~~~

Call \(u\) open when \(K_u\cap(K^*)^3\ne\varnothing\).  At most two ports
are open.  Equivalently, at least two ports satisfy

~~~text
e_(u,d)^* in span{a_u,c_u}       for some d in {0,1,2}. (58)
~~~

#### Proof

Suppose three ports \(u,v,w\) were open and choose fully supported vectors
\(z_u,z_v,z_w\) in their respective \(K\)-spaces.  Define

~~~text
p_u=A_u(-,z_u) in L,            q_u=C_u(-,z_u) in M.   (59)
~~~

The equations defining \(K_u\) say \(z_0(p_u)=z_1(q_u)=0\).  Since the
restrictions in (56) are nonzero and \(L,M\) are two-dimensional, the three
\(p\)-vectors lie in one common line of \(L\), and the three \(q\)-vectors
lie in one common line of \(M\).

Evaluate a pair response in its two port slots:

~~~text
b_uv H+p_u tensor q_v+p_v tensor q_u=0.                (60)
~~~

The cross sum has rank at most one.  A nonzero \(b_{uv}H\) has rank two, so
\(b_{uv}=0\), and the cross sum also vanishes.  This holds for all three
pairs.  Together with (56)--(57), all edges on
\(Q\cup\{u,v,w\}\) vanish at fully supported vectors, giving a forbidden
five-root.

Finally, over an infinite field a linear subspace of \(K^3\) misses the
torus exactly when it is contained in one of the three coordinate
hyperplanes.  By annihilator duality, this is equivalent to (58).
\(\square\)

The two blocking ports and their colours may move with the regular zero.
No uniform pair or colour is selected by this corollary.

### Corollary 9.1 (both active ports block every regular zero)

Let \(T=\{s,t\}\) be the two active combined ports from Corollary 7.  At every
regular torus zero (56), the two inactive ports are open and both active
ports are non-open.  Equivalently, for each \(u\in T\) there is a colour,
possibly depending on \(u\) and on the regular zero, such that

~~~text
e_(u,d)^*
 in span{A_u(z_0,-),C_u(z_1,-)}.                       (60a)
~~~

#### Proof

At an inactive port \(v\notin T\), both \(A_v,C_v\) vanish, so the space
\(K_v\) in (57) is all of \(P_v^\vee\) and meets the torus.  The two
inactive ports already account for the maximum of two open ports allowed by
Corollary 9.  Hence neither active port is open.  The final equivalence is
the annihilator statement in Corollary 9. \(\square\)

Corollary 7.1 gives a fixed coordinate covector in the full combined
coefficient-row span at each active port.  Corollary 9.1 is a different,
pointwise statement for the two covectors produced by each regular zero.

## 5. Exhaustive rank-one response trichotomy

Assume now

~~~text
rank H=1,                    H=x tensor y,              (61)
x in X-{0},                  y in Y-{0}.
~~~

The factorization has the gauge

~~~text
x -> gamma x,               y -> gamma^(-1)y,
gamma in K^*.                                             (62)
~~~

### Theorem 10 (rank-one double-contained, one-sided, and two-sided cover)

Under (1)--(11), (8), (9), and (61), exactly one of the following quotient
patterns holds, up to exchanging the two residual shores.

#### I. Double-contained rank-one Wick core

Every block is contained on its residual shore:

~~~text
A_u=x tensor a_u,                C_u=y tensor c_u,      (63)
a_u,c_u in P_u.
~~~

The six responses vanish if and only if

~~~text
B_uv=-(a_u tensor c_v+c_u tensor a_v)                  (64)
~~~

in the labelled \(P_u\otimes P_v\) slots.  Neither family
\((a_u)\) nor \((c_u)\) is identically zero.  Maximum-root maximality
forces at least one \(a_u\) and at least one \(c_v\) to be a nonzero
coordinate covector.

#### II. Exactly one shore escapes

After exchanging shores if needed,

~~~text
A_u=x tensor a_u                         for every u,
bar C_v!=0                               for some v,    (65)
~~~

where now \(\bar C_v\) is the image in \((Y/Ky)\otimes P_v\).
The common support

~~~text
T={u:a_u!=0}={u:bar C_u!=0}              (66)
~~~

has size one or two.

If \(T=\{s\}\), then

~~~text
A_s=x tensor a_s,               A_v=0             (v!=s),
C_s arbitrary with bar C_s!=0,
C_v=y tensor c_v                                  (v!=s),
B_sv=-a_s tensor c_v,
B_vw=0                                  (v,w!=s).      (67)
~~~

All products in (67) are inserted into their named local slots.  The
escaping component of \(C_s\) is absent from every pair response because no
response pairs \(s\) with itself.  Maximum-root maximality implies

~~~text
a_s is coordinate,                    y is coordinate,
x is coordinate
  or at least one inactive c_v is coordinate.          (68)
~~~

If \(T=\{s,t\}\), there are

~~~text
d in Y-Ky,        a_s,a_t in P_s,P_t nonzero,
c_u in P_u                                      (u in U) (69)
~~~

such that

~~~text
A_s=x tensor a_s,                    A_t=x tensor a_t,
A_v=0                                           (v notin T),

C_s=d tensor a_s+y tensor c_s,
C_t=-d tensor a_t+y tensor c_t,
C_v=y tensor c_v                              (v notin T),

B_uv=-(a_u tensor c_v+c_u tensor a_v),          (70)
~~~

where \(a_v=0\) for \(v\notin T\).  Maximum-root maximality implies

~~~text
at least one of a_s,a_t is coordinate,
y is coordinate or both a_s,a_t are coordinate.        (71)
~~~

The forms with the \(q_0\)-shore escaping are obtained by the exact labelled
exchange

~~~text
(q_0,x,A,a) <-> (q_1,y,C,c).                           (72)
~~~

#### III. Both shores escape

The whole \(A,C\) supports agree:

~~~text
T={u:A_u!=0}={u:C_u!=0},          1<=|T|<=2,
B_uv=0                              for every pair.     (73)
~~~

If \(T=\{t\}\), there are three distinct colours \(i,j,k\) and nonzero
scalars such that

~~~text
H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*,
A_t=alpha e_(q_0,i)^* tensor e_(t,i)^*,
C_t=beta  e_(q_1,j)^* tensor e_(t,j)^*.                (74)
~~~

The complete target splits into the three exact labelled pure pieces

~~~text
H tensor Pi_Q
 =mu_k product_(v in B)e_(v,k)^*,

A_t tensor Pi_(q_0,t)
 =mu_i product_(v in B)e_(v,i)^*,

C_t tensor Pi_(q_1,t)
 =mu_j product_(v in B)e_(v,j)^*.                      (75)
~~~

If \(T=\{s,t\}\), there are distinct residual colours \(i,j\), the third
colour \(k\), nonzero local covectors \(\alpha_s,\alpha_t\), and
\(\tau,\gamma\in K^*\) such that

~~~text
A_s=e_(q_0,i)^* tensor alpha_s,
A_t=e_(q_0,i)^* tensor alpha_t,
C_s=tau e_(q_1,j)^* tensor alpha_s,
C_t=-tau e_(q_1,j)^* tensor alpha_t,

H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*.                (76)
~~~

At least one of \(\alpha_s,\alpha_t\) is coordinate, and

~~~text
i in supp(alpha_s) union supp(alpha_t),
j in supp(alpha_s) union supp(alpha_t).                 (77)
~~~

The pure-\(k\) term is exact:

~~~text
gamma Pi_Q=mu_k product_(u in U)e_(u,k)^*.             (78)
~~~

After subtracting it, the complete remaining identity is

~~~text
sum_(u in {s,t}) [
 sh_({q_0,u},B-{q_0,u})(A_u tensor Pi_(q_0,u))
 +sh_({q_1,u},B-{q_1,u})(C_u tensor Pi_(q_1,u))
]
 =mu_i product_(v in B)e_(v,i)^*
  +mu_j product_(v in B)e_(v,j)^*.                     (79)
~~~

The three branches exhaust the rank-one six-response locus.  The complete
target is already included in the two-sided refinements (74)--(79).
No complete-target exclusion of Branch I or II is asserted.

#### Proof

The three patterns are the exhaustive possibilities for the two quotient
families relative to \(Kx\) and \(Ky\).

#### Proof of Branch I

If both quotient families vanish, (63) is forced.  Substitution into (8)
gives

~~~text
x tensor y tensor
 [B_uv+a_u tensor c_v+c_u tensor a_v]=0.
~~~

Because \(x,y\ne0\), this is equivalent to (64).

If every \(a_u\) vanished, then every \(A_u,B_{uv}\) would vanish and
\(\{q_0\}\cup U\) would be a five-root.  Thus the \(a\)-family is nonzero;
the \(c\)-statement is symmetric.  If every nonzero \(a_u\) were
noncoordinate, choose a fully supported kernel vector for each of them and
an arbitrary torus vector where \(a_u=0\).  Formula (64) then kills every
\(B_{uv}\), while all \(A_u\) vanish on those vectors.  Together with an
arbitrary torus vector at \(q_0\), this gives a five-root.  Hence some
\(a_u\) is coordinate.  The \(c\)-argument is symmetric.

#### Proof of Branch II

Assume (65).  The \(a\)-family is nonzero: otherwise (8) gives all
\(B_{uv}=0\), and \(\{q_0\}\cup U\) is a five-root.  Projecting (8) modulo
\(Ky\) gives

~~~text
a_u boxtimes bar C_v+a_v boxtimes bar C_u=0.           (80)
~~~

The support and sign proof of Lemma 2 applies with the first residual space
one-dimensional.  It proves (66) and \(1\le|T|\le2\).

On a singleton support, every inactive \(C_v\) has the form \(y\otimes c_v\).
Substitution in (8) gives exactly (67).  No equation contains the escaping
part of \(C_s\).

If \(a_s\) were noncoordinate, a torus kernel vector at \(s\) would kill
\(A_s\) and every star block \(B_{sv}\), giving a five-root on
\(\{q_0\}\cup U\).  If \(y\) were noncoordinate, choose a torus kernel at
\(q_1\).  On the five vertices \(Q\) plus the three inactive ports, it kills
\(H\) and every \(C_v\); every other internal edge is already zero.  Thus
\(a_s,y\) are coordinate.

If \(x\) and all three inactive \(c_v\) had torus zeros, choose their torus
kernel vectors.  They make the same set \(Q\) plus the three inactive ports
a five-root.  A covector has no torus zero exactly when it is coordinate,
which proves the last disjunction in (68).

On a two-port support, factor-line uniqueness in (80) gives

~~~text
bar C_s=bar d tensor a_s,
bar C_t=-bar d tensor a_t,                             (81)
~~~

after a nonzero normalization.  Choose a lift \(d\notin Ky\).  The
differences from (81) lie in \(Ky\otimes P_u\), giving (69)--(70).
Direct substitution shows that the two \(d\)-terms cancel and that (64)
with \(a_v=0\) off \(T\) supplies every \(B_{uv}\).

If both \(a_s,a_t\) were noncoordinate, torus kernel vectors for them would
kill every \(A\)- and \(B\)-edge on \(\{q_0\}\cup U\), giving a five-root.
This proves the first assertion in (71).  If \(y\) and, say, \(a_s\) were
both noncoordinate, use torus kernels for them on the five vertices
\(Q\), \(s\), and the two inactive ports.  In (70), every edge on that set
vanishes.  The same argument with \(t\) proves the second assertion in (71).

#### Proof of Branch III

Lemma 2 gives (73).  On a singleton support, maximum-root maximality and
Lemma 1 make both \(A_t,C_t\) coordinate monomials:

~~~text
A_t=alpha e_(q_0,i)^* tensor e_(t,a)^*,
C_t=beta  e_(q_1,j)^* tensor e_(t,b)^*.                (82)
~~~

Their residual lines lie outside \(Kx,Ky\), respectively.  Quotient (9) by
those two coordinate lines.  The image of \(H=x\otimes y\) is nonzero of
rank one.  If \(i=j\), the target across \(Q\mid U\) has rank two, a
contradiction.  Therefore \(i\ne j\), and with \(k\) the third colour,
equality of nonzero simple tensors gives

~~~text
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*             (83)
~~~

for a derived \(\lambda\ne0\).

The pure colour-\(i\) coefficient of (9) can come only from the \(A_t\)
term, so \(a=i\).  The pure colour-\(j\) coefficient can come only from the
\(C_t\) term, so \(b=j\).  On the all-\(k\) port slice both cross terms
vanish, and (9) forces \(H\) to be the \(k,k\) coordinate monomial.  The
three remaining summands have disjoint coordinate support at the \(t\)-slot.
Separating those three coordinates proves (74)--(75).

On a two-port support, Lemma 2 and maximum-root maximality give the first
four lines of (76): the common residual factors are coordinate and at least
one local factor is coordinate.  Quotienting by the two residual coordinate
lines gives the same target-rank contradiction when \(i=j\), so \(i\ne j\)
and (83) holds.  The pure colour-\(i\) and colour-\(j\) coefficients give
(77).

It remains to identify \(H\).  If one local factor is noncoordinate and
\(H\) had a torus zero, that zero, a torus kernel vector for the
noncoordinate local factor, and arbitrary torus vectors at the two inactive
ports would give a five-root.  Therefore \(H\) is torus-zero-free and Lemma
1 makes it a coordinate monomial.  Its two coordinate quotients and (83)
then force both residual colours of \(H\) to be \(k\).

If both local factors are coordinate, condition (77) says that their two
colours are exactly \(i,j\).  The all-\(k\) port slice of (9) kills every
cross term and again forces \(H\) onto the \(k,k\) coordinate line.  This
proves the last line of (76) and (78).  Subtracting the exact pure-\(k\)
summand from (9) gives (79).  The quotient patterns are disjoint and
exhaustive, completing the proof. \(\square\)

The monomial triangle (74)--(75) and the two-site identity (79) are necessary
same-root companion configurations.  This theorem does not assert that the
displayed complementary tensors can be realized by one common four-root
incidence system satisfying every GLS4 gate.

## 6. The seventh response and a denominator-free hafnian identity

Let \(T_4\) be the physical six-vertex hafnian tensor on \(Q\cup U\).  Fill
all six slots with arbitrary vectors and abbreviate

~~~text
h=H(z_0,z_1),
a_u=A_u(z_0,z_u),
c_u=C_u(z_1,z_u),
b_uv=B_uv(z_u,z_v),
t=T_4(z_0,z_1,(z_u)_(u in U)).                         (84)
~~~

The six pair-response equations become

~~~text
h b_uv+a_u c_v+a_v c_u=0                 for u!=v.     (85)
~~~

### Proposition 11 (denominator-free seventh-response identity)

For every such evaluation,

~~~text
h t
 =-2 sum_(S subset U, |S|=2)
       product_(u in S)a_u product_(v in U-S)c_v.      (86)
~~~

No value of \(h\) is inverted.

#### Proof

The fifteen perfect matchings of \(Q\cup U\) split according to whether
they contain the \(Q\)-edge:

~~~text
t
 =h sum_({{r,s},{v,w}} partition U) b_rs b_vw
  +sum_(u!=v) a_u c_v b_(U-{u,v}),                    (87)
~~~

where \(b_{U-\{u,v\}}\) denotes the edge on the remaining two labelled
ports.  Multiply by \(h\).  In the first sum replace both factors \(hb\)
using (85); in the second replace its one factor \(hb\).  For a fixed
two-set \(S\), the monomial

~~~text
product_(u in S)a_u product_(v in U-S)c_v
~~~

occurs twice with positive sign from the three \(Q\)-edge matchings and four
times with negative sign from the ordered cross matchings.  Its coefficient
is \(2-4=-2\).  These six monomials exhaust the expansion, proving (86).
\(\square\)

In the double-contained rank-one core, define the labelled quartic tensor

~~~text
Phi(a,c)
 =sum_(S subset U, |S|=2)
   sh_(S,U-S)(
     tensor_(u in S)a_u tensor tensor_(v in U-S)c_v
   )
 in tensor_(u in U)P_u.                                (88)
~~~

Direct substitution of (64) into the fifteen matching terms gives the full
tensor identity

~~~text
T_4=-2 sh_(Q,U)(x tensor y tensor Phi(a,c)).            (89)
~~~

Thus, in characteristic zero,

~~~text
T_4=0                     iff                  Phi(a,c)=0 (90)
~~~

on Branch I.  This is an additional quartic equation, not a consequence of
the six pair-response equations.

For the other rank-drop branches, (86) is still a necessary identity.
If the literal four-port response vanishes, its right side must vanish at
every contraction.  Conversely, when \(h=0\), (86) does not determine \(t\).
Therefore this document treats **all six pair-response zeros**.  The literal
all-seven-zero leaf requires \(T_4=0\) separately.

The independence is exact.  In Branch I take

~~~text
a_u=e_(u,0)^*,                 c_u=e_(u,1)^*
                                      for every u in U. (91)
~~~

For any fixed two-set \(S\), the port word which is colour \(0\) on \(S\)
and colour \(1\) on its complement has coefficient one in exactly the
\(S\)-summand of \(\Phi\).  Equation (89) gives coefficient \(-2x\otimes y\),
which is nonzero.  Hence all six pair responses vanish by (64), while the
four-port response does not.

## 7. Exact nonzero, denominator, and characteristic ledger

The reduction has the following pointwise chart structure.

1. **Same GLS4 pair.**  The source gives \(H_Q\ne0\) and \(\Pi_Q\ne0\).
   Tensor nonvanishing of \(\Pi_Q\) is the union of its \(81\) coordinate
   opens

   ~~~text
   D(Pi_Q[gamma]),                 gamma in {0,1,2}^4.  (92)
   ~~~

   No canonical scalar is substituted for this union.  The individual
   higher-column survival and raw-incidence conclusions are retained but not
   divided by.

2. **Rank two.**  The rank-two divisor is covered by

   ~~~text
   det H=0,          D(Delta_(I,J))
   ~~~

   for the nine \(2\) by \(2\) minors \(\Delta_{I,J}\).  Supports \(L,M\),
   quotient maps, the conformal class, and the combined images \(W_u\) are
   intrinsic and glue on chart overlaps.  Choosing bases with \(H=I_2\) in
   Lemma 6 is a change of basis on one rank-two chart, not saturation by an
   undeclared factor.

3. **Rank one.**  The rank-one stratum is covered by the nine nonzero-entry
   charts \(D(H[i,j])\), together with the vanishing of all \(2\) by \(2\)
   minors.  The only ambiguity is the displayed gauge (62).

4. **Active quotient supports.**  Whole-block zero strata remain exact zero
   equations.  Factor-line normalization uses one selected nonzero
   coefficient only on the declared active chart.  The unnormalized cross
   equations (12), (20), (29), and (80) are polynomial.

5. **Maximum-root steps.**  Every coordinate conclusion is obtained from
   Lemma 1 by constructing the stated five-root.  These steps use that the
   field is infinite.  The actual source is over \(\mathbb C\).  No
   projective point is silently promoted to a torus point.

6. **Characteristic.**  Characteristic zero is used for infinitude and for
   \(2\ne0\) in the support bound, Lemma 6, and (89)--(90).  No
   characteristic-two branch is suppressed.

7. **Complete target.**  The only declared target saturation is

   ~~~text
   mu_0 mu_1 mu_2!=0.                                  (93)
   ~~~

   Scalars such as \(\lambda\) in (37) and (83), and \(\gamma\) in (78), are
   nonzero derived or declared block coefficients.  The permanent identities
   are kept in multiplied form.

8. **Unused fixed-\(Q\) gates.**  No proof step divides by or saturates
   against

   ~~~text
   h=H_Q(z_Q),                  p_(A,Q)(z_Q),
   a response coordinate,      a nuisance or augmented minor,
   an alignment factor,        a legal-selector coefficient,
   a target-module denominator.                               (94)
   ~~~

9. **Seventh response.**  Proposition 11 multiplies by \(h\) and never
   divides by it.  Equation (89) is a direct rank-one tensor identity.
   The additional equation \(T_4=0\) is not folded silently into the six
   hypotheses.

10. **No atlas.**  The support sizes in Lemma 2 and Corollary 7 are derived
    from tensor orthogonality in characteristic zero.  No enumeration of the
    \(2^4\) whole-block masks or coordinate support masks is part of the
    proof.

## 8. Exact controls and limitations

The controls in this section separate the response/maximality mechanisms
from the complete target and common-root companion obligation.  They are not
hypothetical witnesses or counterexamples.

### 8.1 Rank-two conformal-core maximum-root control

Retain every root--outside block from the exact ten-vertex fixture in
[GLS9 Section 9.5](FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md#95-maximum-root-off-target-fixture-on-the-surviving-pure-locus).
On the outside graph set

~~~text
H=e_0^* tensor e_0^*+e_1^* tensor e_1^*,

A_(u_0)=e_(q_0,0)^* tensor e_(u_0,0)^*,
C_(u_0)=e_(q_1,1)^* tensor e_(u_0,0)^*,
A_(u_1)=e_(q_0,1)^* tensor e_(u_1,1)^*,
C_(u_1)=e_(q_1,0)^* tensor e_(u_1,1)^*,

B_(u_0,u_1)=-e_(u_0,0)^* tensor e_(u_1,1)^*,          (95)
~~~

with every other outside block zero.  The two cross terms on
\(\{u_0,u_1\}\) sum to

~~~text
H tensor e_(u_0,0)^* tensor e_(u_1,1)^*,
~~~

and \(H\boxtimes B_{u_0u_1}\) cancels them.  Every other pair response
vanishes termwise.  Here

~~~text
L=M=span{e_0^*,e_1^*},          rank H=2,
W_(u_0),W_(u_1)!=0,             W_(u_2)=W_(u_3)=0.     (96)
~~~

Thus Corollary 7 is sharp.

The unchanged root incidence gives maximum root order four, outside corank
five, and

~~~text
Pi_Q=product_(u in U)e_(u,2)^*,
p_(A,Q)((1,1,1),(1,1,1))=1,
H((1,1,1),(1,1,1))=2.                 (97)
~~~

At outside word \((0,0,2,2,2,2)\), only \(H\otimes\Pi_Q\) contributes and
its coefficient is one instead of target zero.  Hence this is an exact
maximum-root rank-two response control and an exact complete mixed failure.
It does not verify GLS4 higher-column quotient survival.

### 8.2 Rank-one double-contained maximum-root control

Keep the same root incidence and put

~~~text
H=e_(q_0,0)^* tensor e_(q_1,0)^*,

A_(u_0)=e_(q_0,0)^* tensor e_(u_0,0)^*,
C_(u_0)=e_(q_1,0)^* tensor e_(u_0,1)^*,
A_(u_1)=e_(q_0,0)^* tensor e_(u_1,1)^*,
C_(u_1)=e_(q_1,0)^* tensor e_(u_1,0)^*,

B_(u_0,u_1)
 =-[e_(u_0,0)^* tensor e_(u_1,0)^*
    +e_(u_0,1)^* tensor e_(u_1,1)^*],                 (98)
~~~

with every other outside block zero.  Formula (64) gives all six response
zeros.  The same coordinate-monomial clique cover proves maximum root order
four, and the same mixed target coefficient is one instead of zero.  This is
a rank-one core control, not a target-incidence point.

### 8.3 Formal monomial-triangle target control

At the level of independently declared companion tensors, choose distinct
colours \(i,j,k\), one port \(t\), and nonzero
\(\alpha,\beta,\gamma\).  Set

~~~text
H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*,
A_t=alpha e_(q_0,i)^* tensor e_(t,i)^*,
C_t=beta  e_(q_1,j)^* tensor e_(t,j)^*,
B_uv=0,                                                   (99)
~~~

and choose companions satisfying

~~~text
gamma Pi_Q=mu_k product_(u in U)e_(u,k)^*,
alpha Pi_(q_0,t)=mu_i product_(v in B-{q_0,t})e_(v,i)^*,
beta Pi_(q_1,t)=mu_j product_(v in B-{q_1,t})e_(v,j)^*. (100)
~~~

Then the complete target is exactly the sum of its three pure tensors and
every pair response is zero.  This proves that labelled response and target
tensor algebra alone do not contradict (74)--(75).  The companions in (100)
have not been realized as permanents of one common GLS4 incidence system.

### 8.4 The seventh response is independent

The coordinate choice (91), together with (63)--(64), is an exact algebraic
point with all six pair responses zero and \(T_4\ne0\).  It need not satisfy
the complete target or maximum-root source.  Its purpose is only to show that
the quartic condition (90) is load-bearing for a literal all-seven-zero
claim.

## 9. Proof-DAG consequence, evidence status, and open boundary

Composing GLS10 with this theorem gives the proved determinant-divisor edge

~~~text
actual four-root maximum-root surplus-two witness
 + GLS4 pair Q
 + all six same-Q pair responses identically zero

 -> rank H_Q cannot be 0 or 3
 -> rank H_Q=2 double-contained conformal core
       with exactly two combined port supports,
       fixed and regular-zero blocker consequences, and Q4
    or
    rank H_Q=1 exhaustive branches I, II, III
 -> literal all-seven zero additionally requires T_4=0. (101)
~~~

The reviewed exact ledger is

~~~text
rank zero excluded for the GLS4 pair:                     PROVED;
rank-two simultaneous two-sided escape excluded:          PROVED;
rank-two one-sided singleton escape excluded:             PROVED;
rank-two one-sided two-port escape excluded:              PROVED;
rank-two double containment:                              DERIVED EXACTLY;
rank-two exactly-two combined support theorem:            PROVED;
rank-two fixed/moving blockers, conformal, and Q4:          PROVED;

rank-one response trichotomy:                             PROVED;
rank-one two-sided target refinements:                    PROVED;
denominator-free seventh-response identity:               PROVED;

focused primary verifier:                                 PASS;
independent no-import audit:                              PASS;
hostile theorem and scope review:                         PASS;
formalization:                                            NONE;

rank-two double-contained core empty on witness locus:    EXCLUDED BY FOLLOW-UP;
rank-one core/one-sided target exclusion:                 OPEN;
rank-one monomial-triangle common-root integrability:     EXCLUDED BY FOLLOW-UP;
literal all-seven rank-drop leaf after T_4=0:             OPEN;
weaker response-zero patterns and absorption fibres:      OPEN;
legal same-Q named downstream target package:             OPEN;
supply-and-target-attachment strategic node:              OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED. (102)
~~~

The
[reviewed follow-up exclusion](FOUR_ROOT_DETERMINANT_DIVISOR_RANK_TWO_CORE_AND_RANK_ONE_SINGLETON_TRIANGLE_EXCLUSION_THEOREM.md)
combines the complete target with this reduction to exclude the whole
rank-two core and the rank-one singleton triangle.  The smallest remaining
obligation in this six-response divisor is therefore the common-root and
complete-target analysis of rank-one Branch I, Branch II and its transpose,
and the two-port Branch III identity, retaining the separate seventh-response
quartic wherever literal all-seven response zero is required.

No finite replay can prove the arbitrary-point implications above.  The
focused primary replays the labelled response identities, rank and quotient
formulas, normal forms, exact controls, and hafnian identity.  The independent
standard-library audit uses different quotient, incidence, and permutation
representations.  Both pass.  Hostile review of the case cover, maximum-root
constructions, saturations, and open boundary also passes.  These bounded
replays verify displayed identities; the written arguments prove the
arbitrary-point implications.

Dependencies:

- [GLS4 same-pair source theorem](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [GLS7 four-root source cover](FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md)
- [GLS8 promoted one-target reduction](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
- [GLS9 full-rank localization](FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md)
- [GLS10 full-rank survivor exclusion](FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_PURE_COMPLEMENTARY_PERMANENT_SURVIVOR_EXCLUSION_THEOREM.md)
- [maximum-root saturation and coordinate absorption](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md)

Evidence and provenance:

- [focused exact verifier](verify_four_root_determinant_divisor_all_pair_response_zero_rank_reduction.py);
- [independent standard-library no-import audit](audit_four_root_determinant_divisor_all_pair_response_zero_rank_reduction.py);
- [hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_REDUCTION_REVIEW_2026-08-20.md); and
- [discovery derivation and branch ledger](../../docs/history/handoffs/R4_DETERMINANT_DIVISOR_ALL_RESPONSE_ZERO_REDUCTION_2026-08-20.md).

No external literature premise is used.
