# Four-root determinant-divisor rank-one two-port \(P_5\) extraction

## Status

**Proved exact characteristic-zero reduction.  The focused primary verifier,
genuinely independent no-import audit, and
[hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_REVIEW_2026-08-20.md)
pass.**

Start with an actual hypothetical ternary GHZ witness whose
maximum-cardinality torus root has order four and surplus two.  Fix the same
residual pair \(Q\) supplied by GLS4, assume all six same-\(Q\) pair responses
vanish, and enter the surviving rank-one Branch-III two-port form of GLS11
and GLS12.

This theorem proves that the complete mixed target equations and the common
physical four-root incidence maps force an exact weighted restriction

\[
P_5\longrightarrow
\mu_i e_i^{\otimes5}+\mu_j e_j^{\otimes5}+\mu_k e_k^{\otimes5},
\qquad \mu_i\mu_j\mu_k\ne0.
\]

Equivalently, after one invertible diagonal target normalization, this branch
enters the ordinary \(P_5\to\Delta_3\) permanent-restriction node.

This is an extraction edge, not an exclusion.  No committed theorem excludes
the unrestricted \(P_5\to\Delta_3\) restriction.  The synthetic modes below
are not physical residual vertices and do not give a GLD selector,
alignment, synchronization, activity, nuisance-survival, or anchor package.
Branch I, Branch II, weaker response-zero patterns, nonzero-response
absorption and exceptional fibres, the strategic supply-and-target node, and
the global conjecture remain **OPEN**.  The global Krenn--Gu status is
**UNRESOLVED**.

## 1. Exact inherited branch

Let \(K\) be a field of characteristic zero.  The actual-witness application
is over \(K=\mathbb C\).  All local covector spaces \(E_v=V_v^*\) have the
fixed coordinate basis

~~~text
e_(v,0)^*, e_(v,1)^*, e_(v,2)^*.
~~~

Let

~~~text
B={q_0,q_1,s,t,m,n},        Q={q_0,q_1},
U={s,t,m,n}.                                             (1)
~~~

For \(u\in U\), write

~~~text
H=H_Q,
A_u=H_(q_0,u),
C_u=H_(q_1,u),
B_uv=H_(u,v).                                           (2)
~~~

The rank-one Branch-III two-port conclusion of
[GLS11](FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md)
gives distinct colours \(i,j,k\), nonzero
\(\tau,\gamma,\mu_i,\mu_j,\mu_k\), and nonzero local covectors
\(\alpha_s,\alpha_t\) such that

~~~text
A_s=e_(q_0,i)^* tensor alpha_s,
A_t=e_(q_0,i)^* tensor alpha_t,
C_s=tau e_(q_1,j)^* tensor alpha_s,
C_t=-tau e_(q_1,j)^* tensor alpha_t,

H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*,
A_m=A_n=C_m=C_n=0,
B_uv=0 for every {u,v} subset U.                        (3)
~~~

At least one of \(\alpha_s,\alpha_t\) is coordinate, and the complete
contracted target supplies the two exact identities

~~~text
gamma Pi_Q
 =mu_k product_(u in U)e_(u,k)^*,                      (4)

sum_(u in {s,t}) [
 sh_(q_0,u)(A_u tensor Pi_(q_0,u))
 +sh_(q_1,u)(C_u tensor Pi_(q_1,u))
]
 =mu_i product_(v in B)e_(v,i)^*
  +mu_j product_(v in B)e_(v,j)^*.                     (5)
~~~

Here \(\Pi_P\) is the four-root complementary permanent on \(B-P\), and
every shuffle in (4)--(5) is into the displayed labelled slots.  Equations
(4)--(5) are full tensor identities, not only pure or Hamming-one shells.

The physical complementary tensors share one family of incidence maps

~~~text
L_v:V_v -> K^4,                                        (6)
~~~

so that every \(\Pi_P\) is the order-four permanent of the four maps whose
labels lie in \(B-P\).  This common-incidence condition is load-bearing.

## 2. Complete target forces the coordinate pairing

### Lemma 1 (the two local factors use the two residual colours)

After possibly exchanging \(s,t\) and replacing \(\tau\) by \(-\tau\),
there are \(a,b\in K^*\) such that

~~~text
alpha_s=a e_(s,i)^*,          alpha_t=b e_(t,j)^*.      (7)
~~~

#### Proof

Choose a coordinate factor among \(\alpha_s,\alpha_t\), and exchange
\(s,t\) if necessary so that

~~~text
alpha_s=a e_(s,d)^*,          a!=0.                    (8)
~~~

There are three cases.

If \(d=i\), quotient (5) in the \(q_0\)-slot by
\(K e_{(q_0,i)}^*\) and in the \(s\)-slot by
\(K e_{(s,i)}^*\).  Both \(A\)-terms and the \(C_s\)-term die.  The pure
colour-\(i\) target dies, while the nonzero pure colour-\(j\) target
survives.  The only remaining physical term is the \(C_t\)-term.  Its
\(t\)-shore is \(K\alpha_t\), so equality with the surviving pure target
forces

~~~text
K alpha_t=K e_(t,j)^*.                                 (9)
~~~

If \(d=j\), the symmetric quotient of the \(q_1\)- and \(s\)-slots by their
colour-\(j\) lines leaves only the \(A_t\)-term and the pure colour-\(i\)
target.  Hence \(K\alpha_t=K e_{(t,i)}^*\).  Exchanging \(s,t\) and replacing
\(\tau\) by \(-\tau\) returns the form (7).

If \(d=k\), quotient only the \(s\)-slot by
\(K e_{(s,k)}^*\).  The \(s\)-edge terms die.  The remaining two physical
terms both have the same \(t\)-factor \(\alpha_t\), so their flattening
across

~~~text
t | B-{t}
~~~

has rank at most one.  The two surviving pure colour-\(i\) and
colour-\(j\) target summands have rank two because \(i\ne j\) and their
complementary pure tensors are independent.  This is impossible.

Thus only the first two cases occur, proving (7).  No factor was divided
out. \(\square\)

## 3. The common two-tail table

For a colour \(c\in\{i,j,k\}\), put

~~~text
S_c=L_s[:,c],              T_c=L_t[:,c],
X=L_(q_1)[:,i],            Y=L_(q_0)[:,j].              (10)
~~~

For \(u,v\in K^4\), define the labelled two-tail tensor

~~~text
Kcal(u,v)=P_4(u,v,L_m,L_n) in E_m tensor E_n.           (11)
~~~

Thus \(\mathcal K(u,v)=\mathcal K(v,u)\).  Let

~~~text
I_c=e_(m,c)^* tensor e_(n,c)^*.                         (12)
~~~

### Lemma 2 (three diagonal and nine zero identities)

Equations (4)--(5) imply

~~~text
a Kcal(X,T_i)=mu_i I_i,
-tau b Kcal(Y,S_j)=mu_j I_j,
gamma Kcal(S_k,T_k)=mu_k I_k,                           (13)
~~~

and

~~~text
Kcal(T_i,Y)=0,       Kcal(T_k,X)=0,       Kcal(T_k,Y)=0,
Kcal(S_j,X)=0,       Kcal(S_k,Y)=0,       Kcal(S_k,X)=0,
Kcal(S_j,T_i)=0,     Kcal(S_j,T_k)=0,     Kcal(S_k,T_i)=0.   (14)
~~~

#### Proof

In (5), the pure colour-\(i\) word can only use the \(A_s\)-term because
\(\alpha_t\) has colour \(j\).  Its remaining \(q_1,t\) coefficient is
\(\mathcal K(X,T_i)\).  The pure colour-\(j\) word can only use the
\(C_t\)-term, whose remaining \(q_0,s\) coefficient is
\(\mathcal K(Y,S_j)\).  Equation (4) on the \(s,t\) colour-\(k\) slice gives
the third equality in (13).

The first six zeros in (14) are respectively the following six labelled
coefficients of (5), written in slot order \((q_0,q_1,s,t)\):

~~~text
[j,j,i,i], [i,i,i,k], [j,j,i,k],
[i,i,j,j], [j,j,k,j], [i,i,k,j].                       (15)
~~~

At those words exactly one physical summand survives.  Its scalar multiplier
is respectively

~~~text
tau a, a, tau a, b, -tau b, b,                         (16)
~~~

all nonzero, while the right side of (5) is zero.

The last three zeros in (14) are the \((s,t)\)-slices

~~~text
[j,i], [j,k], [k,i]                                    (17)
~~~

of (4).  Since (4) is pure in colour \(k\), those three slices vanish.
This proves every identity without cancellation and without division by an
undeclared factor. \(\square\)

## 4. A Latin bottom-row \(P_5\) splice

Write

~~~text
K^5=K^4 direct-sum K e_*                               (18)
~~~

and let \(\iota:K^4\hookrightarrow K^5\) be the top inclusion.  Extend the
two common tail maps by a zero bottom row:

~~~text
Lhat_m=(L_m,0),                Lhat_n=(L_n,0).           (19)
~~~

Define three synthetic maps from a three-dimensional colour space to
\(K^5\) by their columns:

~~~text
             colour i       colour j          colour k

D_0          a e_*          iota(S_j)         iota(S_k)
D_1          iota(T_i)      -tau b e_*        iota(T_k)
D_2          iota(X)        iota(Y)           gamma e_*. (20)
~~~

### Theorem 3 (exact weighted \(P_5\) extraction)

The maps in (19)--(20) satisfy

\[
P_5(D_0,D_1,D_2,\widehat L_m,\widehat L_n)
=
\mu_i e_i^{\otimes5}
+\mu_j e_j^{\otimes5}
+\mu_k e_k^{\otimes5}.                                 \tag{21}
\]

Consequently the Branch-III two-port locus admits an exact
\(P_5\to\Delta_3\) restriction.

#### Proof

Fix a colour word on the three synthetic modes.  If it selects no bottom-only
column in (20), then all five columns lie in the four-dimensional top
subspace, so the five-by-five permanent is zero.  If it selects at least two
bottom-only columns, two columns are supported on the same one-dimensional
bottom row and again no permanent term survives.

Exactly one bottom-only column occurs in twelve colour words.  The three
diagonal words give

~~~text
iii:  a Kcal(T_i,X)=mu_i I_i,
jjj: -tau b Kcal(S_j,Y)=mu_j I_j,
kkk:  gamma Kcal(S_k,T_k)=mu_k I_k.                    (22)
~~~

The other nine words route through exactly the nine zero pairings:

~~~text
iij -> Kcal(T_i,Y),       iki -> Kcal(T_k,X),
ikj -> Kcal(T_k,Y),       jji -> Kcal(S_j,X),
kjj -> Kcal(S_k,Y),       kji -> Kcal(S_k,X),
jik -> Kcal(S_j,T_i),     jkk -> Kcal(S_j,T_k),
kik -> Kcal(S_k,T_i).                                  (23)
~~~

Thus the bottom-count split accounts for all \(3^3=27\) synthetic colour
words.  Keeping the full \(E_m\otimes E_n\) values in (22)--(23) accounts
for every one of the \(3^5=243\) coefficients of (21).

The bottom entries are \(a,-\tau b,\gamma\).  Hence the construction
multiplies by the declared active factors and never divides by them.

The tensor on the right side of (21) has one-mode flattening rank three at
all five modes.  A pullback flattening rank is at most the rank of its local
map, so equality (21) forces each of
\(D_0,D_1,D_2,\widehat L_m,\widehat L_n\) to have rank three.  Their domains
are three-dimensional, hence all five maps are injective, as required by the
repository's \(P_5\) restriction convention.

Finally, since every \(\mu_c\ne0\), an invertible diagonal change on one
target mode sends the right side of (21) to
\(\Delta_3=\sum_c e_c^{\otimes5}\). \(\square\)

### Corollary 3.1 (the seventh physical response is already zero)

On the branch (3), the six-vertex hafnian response on \(Q\cup U\) vanishes
term by term.

#### Proof

A perfect matching that uses \(H\) must cover \(U\) with two \(B\)-edges,
and every \(B\)-edge is zero.  A perfect matching that does not use \(H\)
must attach \(q_0,q_1\) through \(A,C\).  Those shores are supported only at
\(s,t\), leaving \(m,n\) joined by the zero edge \(B_{mn}\).  Thus all
fifteen matchings vanish.

This is not the opposite-sign cancellation in the four-vertex response
\(A_s\boxtimes C_t+A_t\boxtimes C_s\); the six-vertex assertion is
termwise. \(\square\)

## 5. Sharpness and the downstream boundary

The three pairings

~~~text
Kcal(X,Y),          Kcal(T_i,T_k),          Kcal(S_j,S_k)   (24)
~~~

are not controlled by (4)--(5).  Obvious two-synthetic-mode \(P_4\) splices
retain one of these mixed slabs.  The Latin placement (20) is designed so
that none of (24) appears in an exactly-one-bottom mixed word.

For comparison, the direct two-extra-row construction

~~~text
Ltilde_(q_0)=(L_(q_0); e_i; 0),
Ltilde_(q_1)=(L_(q_1); 0; tau e_j),
Ltilde_s=(L_s; a e_i; a e_i),
Ltilde_t=(L_t; -b e_j; b e_j),                         (25)
~~~

with zero extra rows on \(m,n\), gives

\[
P_6(\widetilde L_v)
=
\mu_i e_i^{\otimes6}
+\mu_j e_j^{\otimes6}
+\frac{\tau\mu_k}{\gamma}
 e_{q_0,i}\otimes e_{q_1,j}\otimes e_k^{\otimes U}.    \tag{26}
\]

The third term has mismatched \(q_0,q_1\) colours.  More invariantly, the
\(q_0\)- and \(q_1\)-mode flattenings of (26) both have rank two: only the
coordinate lines \(K e_i,K e_j\) occur at either mode.  A concise weighted
\(\Delta_3\) has rank three at every one-mode flattening, and invertible local
changes preserve those ranks.  Therefore (26) is not a
\(P_6\to\Delta_3\) restriction and supplies no contradiction.  It records
why the successful extraction is the five-mode Latin splice rather than the
naive augmentation.

The repository's
[current \(P_5\) obligation ledger](../p5/frontier/P5_DELTA3_OBLIGATION_LEDGER.md)
does not exclude every unrestricted \(P_5\to\Delta_3\) restriction.  The
conclusion (21) must therefore stop at that downstream permanent node.

## 6. Field, saturation, and scope ledger

1. **Field.**  Lemmas 1--2 and Theorem 3 are exact algebra over the inherited
   characteristic-zero branch.  The splice itself uses no algebraic closure
   or generic point.

2. **Declared nonzero factors.**  The only factors used as nonzero are

   ~~~text
   a, b, tau, gamma, mu_i, mu_j, mu_k.                 (27)
   ~~~

   They are inherited active or target scalars.  Equations (13), (21), and
   the construction (20) keep them multiplied through.  No exceptional
   divisor is silently discarded.

3. **Complete equations.**  The coordinate pairing, the first two diagonal
   identities in (13), and the first six zero identities in (14) use the
   complete mixed identity (5).  The third diagonal identity and the final
   three zeros use the complete physical companion identity (4).  Thus the
   twelve common-tail relations split exactly \(8+4\).  This proof uses
   coefficients beyond the pure and Hamming-one shells.

4. **Common physical incidence.**  The same \(L_m,L_n\) occur in all twelve
   relations.  Independently declared companion tensors do not provide the
   common bilinear map \(\mathcal K\) and do not imply (21).

5. **No selector claim.**  The synthetic maps \(D_0,D_1,D_2\) are algebraic
   maps used to enter a permanent-restriction node.  They are not physical
   residual vertices and are not constant GLD selectors.

6. **Unused gates.**  Nothing here saturates or divides by a response
   coordinate, observable minor, nuisance determinant, selector
   coefficient, alignment form, activity factor, or pure-anchor factor.

7. **Pointwise scope.**  Every physical point satisfying the exact inherited
   Branch-III two-port hypotheses yields (21).  There is no support-mask,
   generic-chart, sampled, modular, or numerical inference.

8. **Downstream stop.**  This theorem does not prove a \(P_5\) nonrestriction,
   permanent nonrestriction, extraction/gluing completion, or the global
   conjecture.

## 7. Proof-DAG consequence and open obligation

Together with GLS11 and GLS12, the literal six-pair-response-zero rank-one
cover becomes

~~~text
rank-one Branch I double-contained:          OPEN;
rank-one Branch II and transpose:            OPEN;
rank-one Branch III singleton:               EXCLUDED by GLS12;
rank-one Branch III two-port:                P_5 extraction here.
                                                               (28)
~~~

The exact status of this package is

~~~text
coordinate pairing:                          PROVED;
three diagonal common-tail identities:       PROVED;
nine mixed common-tail zeros:                PROVED;
Latin bottom-row P_5 splice:                 PROVED;
automatic seventh response zero:             PROVED;

focused primary verifier:                    PASS;
independent no-import audit:                 PASS;
hostile theorem and scope review:            PASS;
formalization:                               NONE;

unrestricted P_5 -> Delta_3 exclusion:       OPEN;
rank-one Branch I and II:                    OPEN;
weaker response-zero patterns:               OPEN;
nonzero-response absorption/exceptional:     OPEN;
named same-Q attachment package:             OPEN;
supply-and-target strategic node:            OPEN;
global Krenn--Gu conjecture:                  UNRESOLVED.       (29)
~~~

The smallest remaining obligation on this particular branch is downstream:
exclude the structured restriction (20)--(21), or prove the needed
permanent-node theorem.  That downstream task is outside the present
supply-and-target-node programme.  Inside the current strategic node, the
remaining source obligations are Branch I, Branch II, weaker response-zero
patterns, and the simultaneous nonzero-response absorption/exceptional
locus.

## 8. Verification obligations

A focused primary verifier must:

1. replay the three coordinate-pairing quotient cases;
2. derive all twelve \(\mathcal K\)-relations from the exact labelled
   coefficients of (4)--(5);
3. enumerate the \(27\) synthetic colour triples and all \(243\) output
   coefficients by direct permanent expansion;
4. enumerate all fifteen physical six-vertex matchings for Corollary 3.1;
5. check the signs and mixed term in the sharpness construction (25)--(26).

The independent audit must not read or import that verifier.  It should
reconstruct the \(5!\) permanent terms and the bottom-count routing through a
genuinely different sparse-permutation or row-assignment representation.

A hostile review must audit especially:

- the shore orientation \(X=L_{q_1}[:,i]\), \(Y=L_{q_0}[:,j]\);
- the bottom sign \(-\tau b\);
- the use of the same labelled tail maps in every companion;
- exhaustion of every zero-, one-, and multiple-bottom word;
- the exact downstream-only scope.

Dependencies:

- [GLS11 determinant-divisor rank reduction](FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md);
- [GLS12 rank-two and singleton-triangle exclusion](FOUR_ROOT_DETERMINANT_DIVISOR_RANK_TWO_CORE_AND_RANK_ONE_SINGLETON_TRIANGLE_EXCLUSION_THEOREM.md);
- [GLS4 same-pair source theorem](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md);
- [order-five permanent package](../p5/README.md); and
- [order-five remaining-obligation ledger](../p5/frontier/P5_DELTA3_OBLIGATION_LEDGER.md).

Evidence:

- [focused exact verifier](verify_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py); and
- [independent no-import audit](audit_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py); and
- [hostile theorem and scope review](../../docs/audits/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_REVIEW_2026-08-20.md).
