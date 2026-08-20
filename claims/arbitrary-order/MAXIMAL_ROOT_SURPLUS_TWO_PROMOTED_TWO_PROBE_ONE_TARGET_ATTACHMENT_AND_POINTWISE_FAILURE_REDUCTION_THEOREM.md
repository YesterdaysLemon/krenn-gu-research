# Maximal-root surplus-two promoted two-probe target module and pointwise one-target failure reduction

## Status

**Exact characteristic-zero arbitrary-root promoted-module reduction; the
physical failure locus remains open.**  Start with an actual hypothetical
complex witness in the maximum-root surplus-two scope, with maximum torus root
order \(r\geq3\).  The same-pair theorem GLS4 supplies a residual pair \(Q\)
and a probe-root pair \(A\) on the same graph.  Re-rooting the complete tensor
identity at \(A\) and treating every other old root as an open port gives a
uniform fixed-\(Q\) module with only two nonzero companion grades.

For every \(r\), this note proves all of the following.

1. The GLS4 complementary permanent forces at least one promoted target
   coefficient to be nonzero and to survive the coefficient-slice space of
   the unique strictly higher companion column.
2. For each promoted target, survival modulo the **complete** nuisance-slice
   space is equivalent to a legal normalized constant selector.  On the
   complete GHZ equation, a legal selector with nonzero physical response is
   equivalent to survival of a one-dimensional pure target quotient.
3. The existence of at least one useful target on the same \(Q\), at one
   contraction retaining the GLS4 \(H_Q\) and raw \(p_{A,Q}\) gates, has an
   exact geometric radical--Fitting criterion.  Its negation includes every
   response-zero and exceptional rank-drop fibre without a support atlas.
4. Generically, either one target escapes or every target has zero response
   or a torsion pure quotient.  The generic disjunction is not pointwise
   exhaustive: torsion can escape on its support divisor.

The output on the good branch is one exact same-graph, same-\(Q\), nonzero
GLD5/GLD7-style target row.  Its selector is constant in the open target
coordinates, normalized, and annihilates every labelled nuisance slice; the
complete target supplies the nonzero pure anchor.  This is an isolated
one-row quotient interface.  It is **not** by itself the package required by
any named committed downstream detector: common-package synchronization,
GLD2 augmented weight/alignment, detector activity, and any additional anchor
hypotheses remain mandatory wherever the owning downstream theorem asks for
them.  The strategic node's closure criterion is not weakened to one row.

This theorem does **not** prove that the good branch occurs on every witness.
The exact all-target radical--Fitting failure profile remains to be contradicted
by complete mixed GHZ coefficients.  No permanent restriction, extraction,
or gluing theorem follows.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. GLS4 source and the promoted partition

Work first over a characteristic-zero field \(K\).  Let

~~~text
Omega=R disjoint-union B,       |R|=r>=3,       |B|=r+2.       (1)
~~~

Fix fully supported root vectors \(x_i\), \(i\in R\), satisfying

~~~text
W_ij(x_i,x_j)=0                       for i!=j.         (2)
~~~

Assume the complete GHZ tensor equation and the GLS4 conclusion.  Thus there
are

~~~text
Q={q_0,q_1} subset B,        A={a_0,a_1} subset R,     (3)
~~~

such that

~~~text
H_Q!=0,                     Pi_Q!=0,
[G^R_(B-Q)]!=0 mod every original order >=4 column,
p_(A,Q) is a nonzero polynomial.                       (4)
~~~

Put

~~~text
K_0=R-A,             U=B-Q,
Uhat=K_0 disjoint-union U,       m=|Uhat|=2r-2,
Bhat=Q disjoint-union Uhat=Omega-A,       |Bhat|=2r.   (5)
~~~

Here \(K_0\) is a set of promoted old roots, not the ground field.  We now
regard \(A\) as the two open probe roots and every vertex of \(\widehat U\)
as an open port.  This is a repartition of the same physical graph and the
same complete tensor equality.

## 2. Only the two top deck orders occur

For \(D\subseteq\widehat B\), let \(G^A_D\) be the root companion relative to
the two roots \(A\).  The surplus in the new partition is \(2r-2=m\).  The
general companion grade rule therefore gives

~~~text
|I|=m+2p,             p in {0,1}.                     (6)
~~~

Equivalently, the complete open-\(A\) tensor identity is

~~~text
T_W(-_A,-_Bhat)
 =sum_(C in binom(Bhat,2)) G^A_C tensor H_(Bhat-C)
  +G^A_empty tensor H_Bhat.                            (7)
~~~

The first family has deck order \(2r-2\) and root--root grade zero.  Thus
\(G^A_C\) is the two-by-two root-to-\(C\) permanental tensor.  The last term
has deck order \(2r\), and

~~~text
G^A_empty=W_(a_0,a_1).                                (8)
~~~

All formal lower even deck summands map to zero.  Retaining them as zero
columns changes no image, quotient, selector, or rank statement below.

The formal full-domain dimension and active-domain dimension are respectively

~~~text
dim E_full=(16^r+4^r)/2-1,
dim E_active=binom(2r,2)3^(2r-2)+3^(2r).              (8a)
~~~

### Lemma 1 (GLS4 forces a promoted coefficient)

There is a pair \(C\in\binom U2\) such that

~~~text
epsilon_A(G^A_C)!=0,                                  (9)
~~~

where \(\epsilon_A\) contracts the two probe-root slots with
\(x_{a_0},x_{a_1}\).  Write
\(V_C^*=\bigotimes_{u\in C}V_u^*\), put

~~~text
S_C=Uhat-C,                                             (13)
L^*_(S_C)=(tensor_(a in A)V_a^*) tensor V_C^*,
g_(S_C)=G^A_C,
N^top_(S_C)=G^A_empty tensor V_C^* subset L^*_(S_C),
~~~

where this is the target coefficient space used below.  Then

~~~text
[g_(S_C)]!=0 in L^*_(S_C)/N^top_(S_C).                (10)
~~~

#### Proof

The original complementary permanent \(\Pi_Q\) assigns every root of \(R\)
to one port of \(U\).  Expand this permanent according to the two members of
\(U\) assigned to the roots in \(A\).  It has the exact Laplace form

~~~text
Pi_Q=sum_(C in binom(U,2))
  epsilon_A(G^A_C) tensor Per_(K_0,U-C),              (11)
~~~

where \(\operatorname{Per}_{K_0,U-C}\) is the complementary root-to-port
permanent for the remaining \(r-2\) old roots.  Tensor symmetrization in the
disjoint port factors is understood.  If every first factor in (11) were
zero, then \(\Pi_Q\) would be zero, contrary to (4).  This proves (9).

Equation (2) gives

~~~text
epsilon_A(G^A_empty)=W_(a_0,a_1)(x_(a_0),x_(a_1))=0. (12)
~~~

The top deck tensor supplies coefficient slices in the two open \(C\)-slots,
so its padded coefficient-slice space is exactly the declared
\(N^{\mathrm{top}}_{S_C}=G^A_\varnothing\otimes V_C^*\).  Applying
\(\epsilon_A\otimes\mathrm{id}_{V_C^*}\) kills that entire space and sends
\(G^A_C\) to the nonzero tensor in (9).  This proves (10).  No denominator is
used.
\(\square\)

For the pair \(C\) and target \(S_C\) in Lemma 1, \(|S_C|=m-2=2r-4\), and the
coefficient of the physical residual-present
deck member \(H_{Q\cup S_C}=H_{\widehat B-C}\) in (7) is exactly
\(g_{S_C}=G^A_C\).  Lemma 1 does not say that this deck member or its residual
contraction is nonzero, and it does not give survival modulo the other
order-\(2r-2\) nuisance slices.  Those are the remaining response and
full-nuisance gates.

The GLS4 raw polynomial has a second promoted interpretation:

~~~text
p_(A,Q)(z_Q)=epsilon_A(G^A_Q(z_Q)).                   (14)
~~~

It is the base-root reading of the coefficient of the residual-absent
all-port deck member \(H_{\widehat U}\).  It is not a residual-present target
selector by itself.

## 3. The full promoted fixed-\(Q\) module

Fix fully supported residual vectors at \(Q\).  Put

~~~text
Ehat=direct-sum_(I subset Bhat, |I| in {2r-2,2r})
       tensor_(v in I)V_v^*,
Fhat=(tensor_(a in A)V_a^*) tensor
     (tensor_(u in Uhat)V_u^*).                       (15)
~~~

The active raw dimensions are

~~~text
dim Ehat=binom(2r,2)3^(2r-2)+3^(2r),
dim Fhat=3^(2r).                                      (16)
~~~

After evaluating the \(Q\)-slots, the domain factors through a quotient of
dimension

~~~text
e_m=binom(m,2)3^(m-2)+2m 3^(m-1)+2*3^m.             (17)
~~~

Indeed, the complement pair \(C\) in (7) meets \(Q\) in zero, one, or two
vertices, giving respectively \(\binom m2\), \(2m\), or one labels; the
order-\(2r\) label contributes the second \(3^m\) summand.

If the structurally zero lower labels are retained, the formal evaluated
domain has dimension

~~~text
2*4^m-1.                                              (17a)
~~~

Let

~~~text
F_m={Uhat-C:C in binom(Uhat,2)} union {Uhat}.          (18)
~~~

For \(S\in\mathcal F_m\), define

~~~text
W_S=tensor_(u in S)V_u^*,
L_S^*=(tensor_(a in A)V_a^*) tensor
      (tensor_(u in Uhat-S)V_u^*),
Fhat=L_S^* tensor W_S.                                (19)
~~~

For \(S=\widehat U-C\), the desired physical block is

~~~text
P_S(H;z_Q)=H_(Q union S)(z_Q,-_S),
g_S=G^A_C.                                            (20)
~~~

For \(S=\widehat U\), it is

~~~text
P_Uhat(H;z_Q)=H_Bhat(z_Q,-_Uhat),
g_Uhat=G^A_empty.                                     (21)
~~~

Let

~~~text
mathsf P_S:Ehat -> W_S,                               (21a)
Gammahat_Q:Ehat -> Fhat                               (22)
~~~

where \(\mathsf P_S\) is the formal desired-label projection: it is zero on
every labelled direct summand except \(I=Q\cup S\), and on that summand it
evaluates the two \(Q\)-slots at \(z_Q\).  The physical response in
(20)--(21) is

~~~text
P_S(H;z_Q)=mathsf P_S(H).                             (22a)
~~~

Let \(\widehat\Gamma_Q\) be the complete fixed-\(Q\) companion map with every
active labelled deck summand retained.  Its desired-label decomposition is

~~~text
Gammahat_Q=g_S tensor mathsf P_S+Theta_S.             (23)
~~~

Define the complete nuisance coefficient-slice space

~~~text
N_S=span{
 (id_(L_S^*) tensor eta)(Theta_S(x)):
 x in Ehat, eta in W_S^*}
 subset L_S^*.                                       (24)
~~~

No same-grade label, higher-grade label, residual-absent label, or unwanted
coefficient slice is removed.

For \(S=\widehat U-C\), \(\dim L_S^*=81\) and an evaluated presentation may
use \(e_m3^{m-2}\) nuisance columns.  For \(S=\widehat U\),
\(\dim L_S^*=9\) and it may use \(e_m3^m\) columns.  These are finite exact
presentations, not proposed elimination sizes.

### Theorem 2 (legal constant selector criterion)

For every \(S\in\mathcal F_m\), the following are equivalent.

1. There is a constant \(\lambda_S\in L_S=(L_S^*)^*\) such that

   ~~~text
   (lambda_S tensor id_(W_S))Gammahat_Q=mathsf P_S.   (25)
   ~~~

2. There is a \(\lambda_S\in N_S^\perp\) with

   ~~~text
   lambda_S(g_S)=1.                                  (26)
   ~~~

3. The desired coefficient survives the complete nuisance space:

   ~~~text
   [g_S]!=0 in L_S^*/N_S.                            (27)
   ~~~

#### Proof

Subtract \(\mathsf P_S\) from (25) and use the labelled direct-summand decomposition
in (23).  On the desired label the difference is
\((\lambda_S(g_S)-1)\mathsf P_S\); on every other label it is
\((\lambda_S\otimes\mathrm{id})\Theta_S\).  Hence (25) is equivalent to
(26).  Finite-dimensional separation proves the equivalence with (27), and
normalization is legal in characteristic zero.  \(\square\)

This is the same decomposable constant-selector interface as GLD5.  The proof
does not use the number of open ports.  It is recorded here because the
promoted two-probe module is not literally the four-root/four-port module in
the owning GLD5 statement.

## 4. Complete-target pure quotient and nonzero attachment

Assume now that the full graph tensor is the ternary GHZ target.  For
\(c\in\{0,1,2\}\), put

~~~text
d_(S,c)=(tensor_(a in A)e_(a,c)^*) tensor
        (tensor_(u in Uhat-S)e_(u,c)^*) in L_S^*,
w_(S,c)=tensor_(u in S)e_(u,c)^* in W_S,              (28)
alpha_c=z_(q0,c)z_(q1,c).                             (29)
~~~

On the fully supported residual torus every \(\alpha_c\) is a unit, and the
three \(w_{S,c}\) are independent.  Quotienting the complete fixed-\(Q\)
identity by \(N_S\) gives

~~~text
sum_(c=0)^2 alpha_c[d_(S,c)] tensor w_(S,c)
 =[g_S] tensor P_S(H;z_Q).                            (30)
~~~

### Theorem 3 (pure rank and useful-row equivalence)

At every fully supported residual contraction,

~~~text
dim span{[d_(S,0)],[d_(S,1)],[d_(S,2)]}<=1.          (31)
~~~

Moreover, the following are equivalent.

1. \([g_S]\ne0\) and \(P_S(H;z_Q)\ne0\).
2. At least one pure class \([d_{S,c}]\) is nonzero.
3. The pure quotient in (31) has rank exactly one.

On these equivalent conditions, Theorem 2 supplies a legal normalized
constant selector and its output is the named nonzero physical response.

#### Proof

The right side of (30) is decomposable, so its left flattening has rank at
most one, proving (31).  Because all \(\alpha_c\) are nonzero and the
\(w_{S,c}\) are independent, the left side is nonzero exactly when at least
one pure class survives.  The right side is nonzero exactly when both of its
factors are nonzero.  This proves the equivalence, and Theorem 2 gives the
selector.  \(\square\)

Thus the nonzero response and target-pure anchor are not extra generic
assumptions on the complete witness locus: together they are exactly the
nonzero pure quotient profile.  If \(P_S=0\), all pure classes are swallowed
but \([g_S]\) can still survive; that row is legal algebraically but has zero
physical output and is not useful even for the isolated one-row reduction.

## 5. Exact pointwise one-target failure

Let \(K\) be a characteristic-zero field and work geometrically after base
change to \(\overline K\).  For the actual maximum-root source, take
\(K=\mathbb C\).  Let

~~~text
Lambda=K[z_(q,c)^(+/-1):q in Q,c=0,1,2],
bar Lambda=bar K tensor_K Lambda,
T_Q=Spec Lambda,              F_Q=Frac(Lambda).       (32)
~~~

Choose fixed bases and let \(B_S(z)\) present \(N_S(z)\).  Write

~~~text
D_S=[d_(S,0)|d_(S,1)|d_(S,2)],
h(z)=H_Q(z),                 p(z)=p_(A,Q)(z).         (33)
~~~

Both \(h\) and \(p\) are nonzero Laurent polynomials by GLS4 and the common
contraction theorem.  For a matrix \(M\), let \(I_j(M)\) be its \(j\)-minor
ideal, with \(I_0(M)=\Lambda\).  For every ideal \(J\subseteq\Lambda\), write

~~~text
sqrt_geom(J)=sqrt(J bar Lambda) subset bar Lambda.     (32a)
~~~

Thus every radical containment and variety below is taken only after extending
all displayed ideals to \(\overline K[z_{q,c}^{\pm1}]\).  Over \(\mathbb C\)
this is the ordinary Laurent Nullstellensatz radical.  The useful loci below
are geometric torus loci unless \(K\)-rational points are stated explicitly.

Define the useful locus for one target by

~~~text
U_S={z in T_Q:
 h(z)p(z)!=0 and rank[B_S(z)|D_S]>rank B_S(z)}.       (34)
~~~

By Theorem 3, \(U_S\) is exactly the locus on which the GLS4 gates coexist
with a legal nonzero same-\(Q\) target row.

### Theorem 4 (radical--Fitting criterion)

For a fixed target \(S\), the following are equivalent.

1. \(U_S\) is empty.
2. For every \(1\le j\le\dim L_S^*\),

   ~~~text
   (h p) I_j([B_S|D_S])
      subset sqrt_geom(I_j(B_S)).                    (35)
   ~~~

Consequently, this fixed \((Q,A)\) has no useful promoted target anywhere on
the residual torus exactly when (35) holds for every
\(S\in\mathcal F_m\).

#### Proof

At a fibre of rank \(j-1\), adjoining \(D_S\) raises rank exactly when every
\(j\)-minor of \(B_S\) vanishes and some \(j\)-minor of \([B_S|D_S]\) does
not.  Taking the union over \(j\) gives the rank-rise locus in (34).  Its
intersection with \(D(hp)\) is empty exactly when

~~~text
V(I_j(B_S)) subset V(hp) union V(I_j([B_S|D_S]))
~~~

for every \(j\).  The Laurent Nullstellensatz translates these containments
to (35).  \(\square\)

The criterion covers generic ranks, every nuisance-rank drop, response-zero
fibres, and exceptional selector escape in one statement.  It divides by no
minor or response coordinate.

For comparison, in the ambient module let \(\mathcal R_S\) be the ideal of
coordinates of \(P_S(H;z)\).  The legal nonzero-response locus can also be
written

~~~text
D(hp) intersect D(R_S) intersect
 {rank[B_S|g_S]>rank B_S}.                            (36)
~~~

It is empty exactly when, for every \(j\),

~~~text
(h p) R_S I_j([B_S|g_S])
 subset sqrt_geom(I_j(B_S)).                          (37)
~~~

Here \(D(\mathcal R_S)\) means that at least one response coordinate is
nonzero.  One must not replace the response ideal by the product of all its
coordinates.  On the complete target locus, (35) and (37) are equivalent by
(30).

Call \((Q,A)\) **GLS4-eligible** when \(H_Q\ne0\), \(\Pi_Q\ne0\), the original
order-two companion survives modulo every higher column, and
\(p_{A,Q}\) is a nonzero polynomial.  GLS4 says that this finite set is
nonempty.  It may contain more than one pair.  A source
point fails the promoted one-row interface **if and only if** (35) holds for
every eligible \((Q,A)\) and every target in its promoted family.  Failure for
one arbitrarily chosen pair or probe pair is not a source-level failure
theorem.

### Corollary 4.1 (exact four-root isolated one-row criterion)

In the standard \(r=4\), four-root/four-port module of GLS7, let
\(\mathcal F_7=\binom U2\cup\{U\}\), and retain its matrices
\(B_S,g_S,D_S\).  For a fixed GLS4-eligible \(Q\), let

~~~text
P_Q=(p_(A,Q):A in binom(R,2)) subset Lambda          (37a)
~~~

be the raw-incidence coordinate ideal.  There is no fully supported
contraction retaining \(h\ne0\), at least one raw incidence, and one useful
GLD5/GLD7 target row exactly when, for every \(S\in\mathcal F_7\) and every
relevant \(j\),

~~~text
(h) P_Q I_j([B_S|D_S])
 subset sqrt_geom(I_j(B_S)).                          (37b)
~~~

Equivalently, the useful locus is the union

~~~text
union_(S,j) V(I_j(B_S)) intersect
 D((h)P_Q I_j([B_S|D_S])).                            (37c)
~~~

The proof is Theorem 4 with \(D(\mathcal P_Q)\), meaning that at least one
raw coordinate is nonzero.  It is essential that \(\mathcal P_Q\) is an ideal,
not the product of all raw coordinates.

Let \(\operatorname{Elig}(W)\) be the nonempty set of residual pairs \(Q\)
having the complete GLS4 package: \(H_Q\ne0\), \(\Pi_Q\ne0\), original
individual survival modulo higher columns, and \(\mathcal P_Q\ne0\).  Exact
four-root pointwise failure of the one-row interface is (37b) for every
\(Q\in\operatorname{Elig}(W)\), every target, and every minor order.  One
arbitrarily selected \(Q\), one generic absorption identity, or one
exceptional denominator is not exhaustive.

## 6. Generic split and intrinsic divisor ledger

For each target put

~~~text
r_S=rank_(F_Q)B_S.                                    (38)
~~~

### Corollary 4.2 (generic escape or universal generic absorption)

Exactly one of the following holds for a fixed eligible \((Q,A)\).

#### G. One-target generic escape

For some \(S\in\mathcal F_m\), the response polynomial is nonzero and

~~~text
rank_(F_Q)[B_S|g_S]=r_S+1.                            (39)
~~~

Then \(U_S\ne\varnothing\).  More explicitly, choose a nonzero response
coordinate, a nonzero \(r_S\)-minor of \(B_S\) (one if \(r_S=0\)), and a
nonzero \((r_S+1)\)-minor of \([B_S|g_S]\).  Their product with \(hp\) is a
nonzero Laurent polynomial.  Characteristic-zero fields are infinite, so the
principal open has a \(K\)-point; any such point gives the legal nonzero row
of Theorem 3.

#### F. Simultaneous generic failure

For every \(S\in\mathcal F_m\), either

~~~text
Z_S: P_S(H;z) is the zero polynomial tensor,           (40)
~~~

or the response is nonzero and

~~~text
A_S: rank_(F_Q)[B_S|g_S]=r_S.                         (41)
~~~

On \(Z_S\), all three pure classes vanish over \(F_Q\).  On \(A_S\), the
desired class and all three pure classes vanish over \(F_Q\).

#### Proof

For each target, the response is zero or nonzero, and adjoining one desired
column changes generic rank by zero or one.  If one target has both nonzero
response and rank rise, it is G; otherwise every target lies in (40) or (41),
which is F.  The alternatives are disjoint and exhaustive.

Over \(F_Q\), equation (30) has independent pure output words and unit
\(\alpha_c\).  Its right side is zero in Z because the response is zero, and
in A because \([g_S]=0\).  Hence all pure classes vanish.  In A the desired
class vanishes by definition.  \(\square\)

Branch F is only a necessary generic shadow of pointwise failure.  An A
target can acquire a useful selector where the nuisance rank drops.  Therefore
F cannot replace the exact containments (35).

Let

~~~text
M_S=coker(B_S:Lambda^(n_S)->Lambda^(dim L_S^*)).      (42)
~~~

In Z, let \(T_S\subset M_S\) be generated by the three pure classes.  In A,
include the desired class as well.  Corollary 4.2 gives

~~~text
T_S tensor_Lambda F_Q=0.                              (43)
~~~

Thus

~~~text
mathfrak a_S=Ann_Lambda(T_S)
   =intersection_v (im B_S :_Lambda v)               (44a)
~~~

is a nonzero ideal, where \(v\) ranges over the displayed generators of
\(T_S\).  This is the simultaneous module saturation, not a chosen least
common multiple of denominators.
Every nonzero \(\delta_S\in\mathfrak a_S\) gives simultaneous
denominator-cleared identities

~~~text
B_S b_(S,v)=delta_S v                                (44)
~~~

for the relevant pure columns and, in A, the desired column.  They prove
fibrewise absorption on \(D(\delta_S)\), including rank drops.  On
\(V(\delta_S)\), division is illegal and (44) proves no membership.  The
intrinsic possible-escape support is \(\operatorname{Supp}T_S=V(\mathfrak
a_S)\), which can be strictly smaller than the zero set of one chosen
denominator.  Exact failure on that support is still governed by (35).

## 7. Small-root interfaces and the four-root scope correction

For \(r=3\), \(m=4\).  The promoted family consists of the six pair targets
and the four-port target used by GLD3.  Here

~~~text
dim E_full=2079,       dim Ehat=15*3^4+3^6=1944,
dim E_full,eval=511,   e_4=432,
B_S:81 x 3888 for |S|=2,
B_Uhat:9 x 34992.                                      (45)
~~~

The unused old root is exactly the fourth promoted port.  The naive
three-port construction from \(U=B-Q\) has no all-port response because
\(|Q\cup U|=5\) is odd; it cannot supply the GLD3 four-port tensor.

For \(r=4\), the standard four-root/four-port module of GLS7 remains valid.
Its \(R/E/A\) trichotomy is the exact split for the stronger **all-seven**
GLD3 package.  It is not the minimal split for an isolated legal row: a response-zero
or absorbed target can coexist with another useful target.  In that standard
module the one-row generic alternatives are exactly G/F above with seven
targets, and the pointwise failure is the seven corresponding radical
containments.  The promoted construction in this theorem gives a second,
uniform two-probe/six-port interface.

There is an important downstream qualification.  At \(r=3\), the promoted
family has exactly the six-pair-plus-four-port target shapes accepted by
GLD3, but the one-row G branch does not supply all seven of them.  The stronger
common seven-row escape is still required before entering GLD3.  At
\(r=4\), the promoted family has fifteen four-port targets and one six-port
target; GLD6 additionally asks for all fifteen pair targets.  For \(r\ge5\),
no presently committed downstream GLD detector accepts only the
top-minus-two and top response layers on \(2r-2\) ports.  Theorems 2--4 are
nevertheless exact legal constant-target attachment statements at every
\(r\).  The strategic node requires entry into a named committed downstream
detector, so the one-row theorem is not enough at any root order.  The standard
GLS7 E branch separately supplies the full four-root GLD3 package;
the analogous promoted \(r=3\) common escape and every \(r\ge5\) downstream
entry remain conditional.

Thus GLS7's edge

~~~text
E -> one common six-pair-plus-four-port package -> GLD3
~~~

is retained.  For the isolated one-row quotient, the exact open branch is
simultaneous pointwise failure of every eligible target for every eligible
\((Q,A)\).  Neither one R target nor one A target is by itself a bad one-row
leaf.  This refinement does not identify the strategic node's full downstream
package with a single row.

## 8. Sharp algebraic boundaries

The following exact one-parameter modules satisfy the quotient identity (30)
with three independent pure output words.  They are not physical graphs or
witnesses.

1. **Generic escape, exceptional swallowing.**  Over \(\mathbb Q[t^{\pm1}]\),
   take \(B=(1,t-1)^{\mathsf T}\), \(g=d_c=e_1\), nonzero response, and
   \(h=p=1\).  Generic rank rises, but at \(t=1\) every desired/pure column is
   swallowed.
2. **Generic absorption, exceptional useful escape.**  Take
   \(B=[t-1]\), \(g=d_c=[1]\), and nonzero response.  Over \(\mathbb Q(t)\)
   every target column is absorbed with denominator \(t-1\), while at
   \(t=1\) the nuisance vanishes and a useful selector exists.
3. **Permanent absorption.**  Take \(B=[1]\) and \(g=d_c=[1]\).  There is no
   escape on any fibre.
4. **Legal zero-response row.**  Take \(L^*=\mathbb Q^2\),
   \(B=e_1\), \(d_c=e_1\), \(g=e_2\), and response zero.  The constant
   selector exists but is unusable because its physical output vanishes.

These controls prove that generic rank, exceptional support, desired
survival, and nonzero response are logically distinct.  They also explain why
neither silent denominator division nor a generic-only theorem closes this
node.

There is also a physical graph-side response-zero control for every
\(r\ge3\).  Choose one coordinate monomial and unit weights.  Write

~~~text
A={a_0,a_1},       C={c_0,c_1},
K_0={k_t:1<=t<=r-2},       U-C={v_t:1<=t<=r-2}.       (45a)
~~~

Install only the following relevant edges:

~~~text
a_0-c_0, a_1-c_1, k_t-v_t,
a_0-q_0, a_1-q_1, q_0-q_1,
q_0-k_1, q_1-v_1,                                      (45b)
~~~

giving the final edge \(q_1-v_1\) weight \(-1\) and every other displayed
edge weight one.  Tensorially,

~~~text
H_Q=e_(q0,0)^* tensor e_(q1,0)^*,
Pi_Q=product_(u in U)e_(u,0)^*,                       (45b')
~~~

with coefficient one on the displayed monomials.  After residual contraction,

~~~text
h(z)=p_(A,Q)(z)=z_(q0,0)z_(q1,0),                    (45b'')
~~~

a nonzero Laurent monomial.  The unique nonzero Laplace pair is \(C\), and
\(\epsilon_A(G^A_C)\) has coefficient one on its coordinate monomial.  But
\(H_{\widehat B-C}\) has exactly two nonzero matchings,

~~~text
(q_0q_1) product_t(k_tv_t),
(q_0k_1)(q_1v_1) product_(t>=2)(k_tv_t),              (45c)
~~~

whose residual contractions have weights
\(+z_{q_0,0}z_{q_1,0}\) and
\(-z_{q_0,0}z_{q_1,0}\).  Hence that entire promoted physical response is the
zero polynomial tensor.  This control is not a hypothetical witness: every installed edge
uses one coordinate monomial, so its all-one and all-two pure GHZ
coefficients are zero rather than one.  It is also not asserted to satisfy
the maximum-root quota package.  It proves that the displayed
\(H_Q,\Pi_Q,p_{A,Q}\) supply data alone do not clear even the response gate for the
Laplace-selected target.

## 9. Proof-DAG consequence and remaining obligation

The support-free source reduction is now

~~~text
actual maximum-root surplus-two witness, any r>=3
 -> GLS4 same Q,A with original individual pair supply and nonzero h,p
 -> promoted two-probe top-depth module on the same graph and Q
 -> {some legal nonzero target row
     | every eligible target satisfies the exact pointwise failure profile}.
                                                               (46)
~~~

What is proved and what remains are:

~~~text
uniform promoted source module for every r>=3:                PROVED;
some desired promoted coefficient survives the top column:   PROVED;
full-nuisance constant-selector criterion:                    PROVED;
nonzero selector/response iff pure rank one on target:        PROVED;
exact pointwise all-rank failure criterion:                   PROVED;
generic G/F split and denominator ledger:                     PROVED;
promoted target shapes match the GLD3 family at r=3:          PROVED;
simultaneous promoted seven-row GLD3 entry at r=3:            OPEN;
existing downstream entry for promoted top layers at r>=4:   OPEN;
every actual witness reaches G:                               OPEN;
complete mixed equations exclude all containments (35):      OPEN;
supply-and-target-attachment strategic node:                  OPEN;
global Krenn--Gu conjecture:                                  UNRESOLVED.      (47)
~~~

The smallest remaining physical obligation for this isolated reduction is to
prove, for every actual source point, that at least one containment (35) fails
for at least one GLS4-eligible \((Q,A)\), or to derive a complete mixed GHZ
contradiction from the simultaneous validity of all those containments.  The
strategic node additionally requires a proved edge from whatever rows survive
to every common-package, synchronization, alignment, activity, and anchor
hypothesis of a named committed downstream detector.  This is a target-coupled
operator-descent problem.  Scalar complementary permanents, unrestricted deck
recovery, generic ranks, and finite support atlases are known to be
insufficient.

## 10. Verification and dependencies

The focused verifier for this theorem checks the two-grade companion census,
the Laplace expansion and top-column separation at small exact orders, every
dimension formula, the selector/pure-rank linear algebra, the finite
rank-locus controls behind (35), and all four sharp modules.  Its independent
no-import audit uses a separate matching enumeration, Fraction row reduction,
and exhaustive exact characteristic-zero reduced-point/rank tables; it does not
read or import the primary verifier.  Bounded replays verify the displayed
identities, not the arbitrary-root written proof.

Run from repository root after the two verification files are added:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
```

Dependencies:

- [GLS4 same-pair source theorem](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [GLS2 companion-grade expansion](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md)
- [GLD5 constant-selector criterion](FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md)
- [GLD7 pure-rank attachment](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md)
- [GLS5 pointwise failure module](MAXIMAL_ROOT_SURPLUS_TWO_POINTWISE_SELECTOR_FAILURE_AND_DECOMPOSABLE_RETRACTION_BOUNDARY_THEOREM.md)
- [GLS6 common \(h,p\) contraction](MAXIMAL_ROOT_SURPLUS_TWO_COMMON_RESIDUAL_CONTRACTION_AND_AUGMENTED_ALIGNMENT_GATE_THEOREM.md)
- [GLS7 four-root all-seven cover](FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md)
