# Four-root full-rank all-response-zero pure complementary-permanent survivor exclusion

## Status

**Proved exact characteristic-zero exclusion.  Focused replay, an independent
no-import audit, and hostile scope review all pass.**

This theorem closes the survivor left by the preceding full-rank
all-response-zero localization.  Start with an actual hypothetical ternary GHZ
witness whose maximum-cardinality torus root has order four and surplus two.
Fix the GLS4 residual pair \(Q\).  If its physical edge block \(H_Q\) is
invertible and all six same-\(Q\) pair-response tensors vanish identically,
the complete contracted GHZ target is inconsistent.

The proof uses two complete target fibres, not a support census.  GLS9 first
reduces the response-zero point to one or two active complementary ports,
distinct residual colours \(i,j\), and a pure third-colour complementary
permanent.  In the \((q_0,q_1)=(i,i)\) fibre, all desired insertions are
supported on at most two local covector lines, but their sum must contain two
independent pure tensors, in colours \(i\) and \(k\).  A quotient of the active
slots forces those two local lines to be exactly the \(i\)- and \(k\)-coordinate
lines.  The \((j,j)\) fibre forces the same two lines to be exactly the
\(j\)- and \(k\)-coordinate lines, a contradiction.  The singleton branch
already fails in the first quotient.

No companion entry, response coordinate, residual contraction, selector,
nuisance minor, or exceptional factor is inverted.  The result excludes only
the full-rank literal all-seven-zero branch.  The divisor
\(\det H_Q=0\), every weaker response-zero pattern, all nonzero-response
absorption and exceptional fibres, the named downstream detector interface,
and the supply-and-target-attachment strategic node remain **OPEN**.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. A two-site pure-tensor quotient lemma

Work over a field \(K\).  Let \(U\) be a labelled set with \(|U|\ge3\), and
let every \(E_u\) be a vector space containing two linearly independent
vectors \(e_{u,a},e_{u,b}\).  Write

~~~text
e_a^U=product_(u in U)e_(u,a),
e_b^U=product_(u in U)e_(u,b).                         (1)
~~~

All tensor products below use the canonical shuffle into their labelled
slots.

### Lemma 1 (one-site obstruction)

For \(t\in U\), a nonzero \(\alpha_t\in E_t\), and
\(X_t\in\bigotimes_{u\in U-\{t\}}E_u\), no equality

~~~text
sh_t(alpha_t tensor X_t)=A e_a^U+B e_b^U              (2)
~~~

exists with \(A,B\in K^*\).

#### Proof

Let \(\pi_t:E_t\to E_t/K\alpha_t\) be the quotient map.  Applying
\(\pi_t\otimes\operatorname{id}\) to (2) gives

~~~text
A pi_t(e_(t,a)) tensor e_a^(U-{t})
 +B pi_t(e_(t,b)) tensor e_b^(U-{t})=0.                (3)
~~~

The two tensors on the remaining nonempty labelled set are linearly
independent.  Hence both quotient vectors vanish.  The line \(K\alpha_t\)
would contain both independent vectors \(e_{t,a}\) and \(e_{t,b}\), which is
impossible.  \(\square\)

### Lemma 2 (two-site line cover)

Let \(s,t\in U\) be distinct, let
\(\alpha_s\in E_s,\alpha_t\in E_t\) be nonzero, and let

~~~text
X_s in tensor_(u in U-{s}) E_u,
X_t in tensor_(u in U-{t}) E_u.                        (4)
~~~

If

~~~text
sh_s(alpha_s tensor X_s)+sh_t(alpha_t tensor X_t)
 =A e_a^U+B e_b^U,                    A B!=0, a!=b,    (5)
~~~

then there is a bijection
\(\sigma:\{a,b\}\to\{s,t\}\) such that

~~~text
K alpha_(sigma(c))=K e_(sigma(c),c)   for c in {a,b}.  (6)
~~~

#### Proof

Let

~~~text
pi_s:E_s -> E_s/K alpha_s,
pi_t:E_t -> E_t/K alpha_t.                             (7)
~~~

Apply

~~~text
pi_s tensor pi_t tensor id_(U-{s,t})                  (8)
~~~

to (5).  Each insertion term dies: the first contains \(\alpha_s\) in
the \(s\)-slot and the second contains \(\alpha_t\) in the \(t\)-slot.
Thus

~~~text
A pi_s(e_(s,a)) tensor pi_t(e_(t,a)) tensor e_a^(U-{s,t})
 +B pi_s(e_(s,b)) tensor pi_t(e_(t,b)) tensor e_b^(U-{s,t})
 =0.                                                   (9)
~~~

The remaining set \(U-\{s,t\}\) is nonempty, so its two pure tensors in
distinct colours are linearly independent.  Consequently, for each
\(c\in\{a,b\}\),

~~~text
pi_s(e_(s,c)) tensor pi_t(e_(t,c))=0.                  (10)
~~~

A simple tensor of two vectors is zero only if one factor is zero.  Hence,
for each colour \(c\), its coordinate line occurs among
\(K\alpha_s,K\alpha_t\).  One line cannot contain both independent coordinate
vectors.  The two colours therefore occupy the two different active lines,
which is exactly (6).  \(\square\)

The lemma is a quotient-module identity.  It uses no coordinates of
\(X_s,X_t\), no nonzero coefficient of either insertion tensor, and no
division.

Equivalently, for \(T\subset U\) define the labelled insertion module

~~~text
M_T=sum_(u in T)
    sh_u(K alpha_u tensor tensor_(v in U-{u})E_v).      (11)
~~~

Quotienting every active slot by its line kills \(M_T\).  Lemmas 1--2 are
the exact one- and two-line consequences needed below.

## 2. Source package and the localized normal forms

Adopt the labelled conventions of GLS9.  Thus

~~~text
Omega=R disjoint-union B,       |R|=4, |B|=6,
Q={q_0,q_1},                    U=B-Q, |U|=4,           (12)
~~~

and contraction of the four root slots gives the complete equality

~~~text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(c=0)^2 mu_c e_c^B,
mu_0 mu_1 mu_2!=0.                                    (13)
~~~

For the application of Lemmas 1--2, put
\(E_u=V_u^*\) and \(e_{u,c}=e_{u,c}^*\) for every \(u\in U\).  Thus every
abstract quotient and every coordinate line is taken in its correctly
labelled physical port space.

GLS4 supplies \(\Pi_Q\ne0\).  Assume

~~~text
det H_Q!=0,
H_(Q union {u,v})=0       for all {u,v} in binom(U,2). (14)
~~~

The second line means equality of the full four-slot pair-response tensors,
not vanishing after one residual evaluation.

GLS9 proves the following consequences of (12)--(14):

1. every \(H_{\{u,v\}}=0\) for \(u,v\in U\);
2. the two \(Q\)-to-\(U\) block families have a common nonempty active set
   \(T\subset U\) with \(|T|=1\) or \(2\);
3. there are distinct residual colours \(i,j\) and a third colour \(k\);
4. for a scalar \(\lambda\in K^*\),

   ~~~text
   H'=(rho_i tensor rho_j)H_Q
      =lambda e_(q0,k) tensor e_(q1,k),
   lambda Pi_Q=mu_k e_k^U;                             (15)
   ~~~

5. on a singleton \(T=\{t\}\), the \(q_0\)-shore has the form

   ~~~text
   H_(q0,t)=a_0 e_(q0,i) tensor alpha_t,
   H_(q1,t)=b_0 e_(q1,j) tensor beta_t,
   a_0 b_0!=0, alpha_t!=0, beta_t!=0;                  (16)
   ~~~

6. on \(T=\{s,t\}\), after harmless nonzero rescaling of the local factors,

   ~~~text
   H_(q0,s)=e_(q0,i) tensor alpha_s,
   H_(q0,t)=e_(q0,i) tensor alpha_t,

   H_(q1,s)=tau e_(q1,j) tensor alpha_s,
   H_(q1,t)=-tau e_(q1,j) tensor alpha_t,
   tau!=0.                                             (17)
   ~~~

For (16), GLS9 proves more--both whole blocks are coordinate monomials--but
only the displayed nonzero simple forms are used below.  The two singleton
local factors \(\alpha_t,\beta_t\) are independent and are not identified.
The \(q_1\)-shore form is used only to kill that insertion at \(q_1=i\).
For (17), neither local factor is assumed coordinate.

### Lemma 3 (the two diagonal pivots are nonzero)

The coefficients \(H_Q[i,i]\) and \(H_Q[j,j]\) are nonzero.

#### Proof

Order rows and columns as \((i,j,k)\).  Equation (15) makes the matrix of
\(H_Q\) have the form

~~~text
[[H_ii,H_ij,H_ik],
 [0,   H_jj,0   ],
 [0,   H_kj,lambda]].                                  (18)
~~~

Therefore

~~~text
det H_Q=H_ii H_jj lambda.                              (19)
~~~

Both \(\det H_Q\) and \(\lambda\) are nonzero, so both diagonal pivots are
nonzero.  \(\square\)

## 3. Main exclusion theorem

### Theorem 4 (the full-rank literal all-response-zero branch is empty)

Over characteristic zero, no actual maximum-root surplus-two ternary GHZ
witness of root order four satisfies (14) for its GLS4 pair \(Q\).

Equivalently, on every such witness with \(\det H_Q\ne0\), at least one of the
six same-\(Q\) physical pair-response tensors is nonzero.  In particular, the
full-rank part of the literal all-seven response-zero branch of GLS7 is empty.

#### Proof

For the first insertion fibre, define the nonzero local covectors

~~~text
hat(alpha)_t=a_0 alpha_t                  if T={t},
hat(alpha)_s=alpha_s, hat(alpha)_t=alpha_t if T={s,t}. (20)
~~~

For an active \(u\in T\), define the \(q_1=i\) slice of the complementary
permanent tensor

~~~text
D_u^i=Pi_( {q0,u} )[q_1=i]
      in tensor_(v in U-{u}) E_v.                       (21)
~~~

Take the complete equality (13) at the two labelled residual coordinates

~~~text
(q_0,q_1)=(i,i).                                       (22)
~~~

The fifteen pair-deck summands split exhaustively.

- The \(P=Q\) term is \(H_{ii}\Pi_Q\).
- Every \(P\subset U\) term is zero because \(H_P=0\).
- Every \(P=\{q_1,u\}\) term is zero because its \(q_1\)-factor is the
  \(j\)-coordinate covector and \(i\ne j\).
- Only the \(P=\{q_0,u\}\), \(u\in T\), insertion terms remain.

The target side is \(\mu_i e_i^U\).  Use (15) and multiply the whole equality
by the declared nonzero scalar \(\lambda\).  After absorbing the nonzero
shore scalars into the local covectors or into \(D_u\), the exact labelled
identity is

~~~text
sum_(u in T) sh_u(hat(alpha)_u tensor lambda D_u^i)
 =lambda mu_i e_i^U-mu_k H_ii e_k^U.                  (23)
~~~

Both coefficients on the right are nonzero by the source target,
\(\lambda\ne0\), and Lemma 3.

If \(|T|=1\), (23) contradicts Lemma 1 with colours \(i,k\).

Suppose \(|T|=2\), say \(T=\{s,t\}\).  Lemma 2 applied to (23) makes both
local lines coordinate.  Define their well-typed colour labels by

~~~text
col(alpha_u)=c  iff  K alpha_u=K e_(u,c).              (24)
~~~

The conclusion is

~~~text
{col(alpha_s),col(alpha_t)}={i,k}.                     (25)
~~~

Now repeat the same extraction at

~~~text
(q_0,q_1)=(j,j).                                       (26)
~~~

The fifteen labels now split symmetrically: \(P=Q\) gives
\(H_{jj}\Pi_Q\); all six \(P\subset U\) terms vanish; all four
\(P=\{q_0,u\}\) terms vanish because their \(q_0\)-factor has colour
\(i\ne j\); and only the two active \(P=\{q_1,u\}\) insertions remain.
Define their exact slices, including the signs from (17), by

~~~text
D_s^j= tau Pi_( {q1,s} )[q_0=j],
D_t^j=-tau Pi_( {q1,t} )[q_0=j].                      (27)
~~~

Using \(H_{jj}\ne0\), (15), and multiplying the complete fibre by
\(\lambda\) gives

~~~text
sh_s(alpha_s tensor lambda D_s^j)
 +sh_t(alpha_t tensor lambda D_t^j)
 =lambda mu_j e_j^U-mu_k H_jj e_k^U.                  (28)
~~~

Both coefficients are nonzero, so Lemma 2 and the same fixed local lines give

~~~text
{col(alpha_s),col(alpha_t)}={j,k}.                     (29)
~~~

Equations (25) and (29) cannot both hold because \(i,j,k\) are three distinct
colours.  This contradiction excludes the two-port branch as well.  The two
cases exhaust GLS9, proving the theorem.  \(\square\)

## 4. Exact saturation and divisor ledger

The proof has the following pointwise ledger.

1. **Inherited full-rank chart.**  The only physical edge-block determinant
   inverted upstream is

   ~~~text
   det H_Q!=0.                                         (30)
   ~~~

   The whole divisor \(V(\det H_Q)\) remains open.

2. **Inherited source nonzeros.**  GLS4 and the GHZ target supply

   ~~~text
   Pi_Q!=0,                 mu_0 mu_1 mu_2!=0.         (31)
   ~~~

   GLS9 derives \(\lambda\ne0\) and the denominator-free identity
   \(\lambda\Pi_Q=\mu_k e_k^U\).

3. **Derived pivots.**  Neither \(H_{ii}\) nor \(H_{jj}\) is independently
   saturated.  Their nonvanishing follows polynomially from
   \(\det H_Q=H_{ii}H_{jj}\lambda\).

4. **Active shores.**  The local factors in (16)--(17) are nonzero because
   they index active whole blocks.  The proof quotients by their lines.  It
   does not select or invert a coordinate of either line.

5. **Complete target use.**  Equations (23) and (28) are full
   \((q_0,q_1)\)-coordinate fibres of (13), including all \(3^4=81\) port
   coefficients in each fibre.  They are not pure-shell or Hamming-one
   equations.

6. **No selector divisions.**  No residual evaluation \(z_Q\), raw
   \(p_{A,Q}\), response coordinate, nuisance minor, Fitting denominator,
   alignment scalar, legal-selector coefficient, or target-module
   denominator appears.

7. **Characteristic.**  The final quotient lemma works over every field.
   Characteristic zero enters through the full upstream GLS9 localization:
   infinitude of \(K\) is used in its maximum-root coordinate forcing, and
   \(2\ne0\) is used in its exhaustive bound \(1\le|T|\le2\).

## 5. Sharpness and proof-boundary controls

The short proof has three load-bearing gates.

### 5.1 The determinant divisor is genuinely outside the argument

If \(H_{ii}=0\), the right side of (23) can lose its \(k\)-pure summand.
A one-site insertion can then equal the remaining \(i\)-pure tensor.  Thus
the singleton quotient contradiction does not extend to
\(V(\det H_Q)\) without a new argument.

### 5.2 Three active local lines evade the two-site contradiction

With three active sites and local lines

~~~text
K e_i, K e_j, K e_k,                                  (32)
~~~

the first diagonal fibre may use the \(i,k\) lines and the second may use the
\(j,k\) lines.  Thus the support bound \(|T|\le2\), not merely finiteness of
the support, is load-bearing.  GLS9 obtains that bound from the complete
pair-response identities in characteristic zero.

### 5.3 The existing maximum-root fixture fails exactly where required

In the GLS9 rational boundary fixture,

~~~text
i=0, j=1, k=2,
{col(alpha_s),col(alpha_t)}={0,1}.                     (33)
~~~

The first diagonal-fibre line-cover requirement (25) would instead need the
local lines
\(\{K e_0,K e_2\}\).  Correspondingly, the displayed coefficient

~~~text
(q_0,q_1,U)=(0,0,2,2,2,2)                             (34)
~~~

equals one rather than zero.  The fixture is not a witness or counterexample;
it is an exact off-target control for the new quotient obstruction.

## 6. Proof-DAG consequence and open boundary

Composing GLS9 with Theorem 4 gives

~~~text
actual four-root maximum-root surplus-two witness
  + GLS4 pair Q
  + det H_Q!=0
  + all six same-Q pair responses identically zero
 -> contradiction.                                    (35)
~~~

The exact status is

~~~text
full-rank literal all-seven response-zero branch:       EXCLUDED;
det H_Q=0 literal response-zero divisor:                OPEN;
one-zero and other weaker GLS7 R patterns:              OPEN;
nonzero-response absorption and exceptional fibres:     OPEN;
legal same-Q named downstream target package:           OPEN;
supply-and-target-attachment strategic node:            OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED. (36)
~~~

This is a source-witness exclusion inside the strategic node, not a target
attachment theorem.  It does not supply common selector packages,
synchronization, augmented alignment, activity, nuisance survival, anchors,
permanent restriction, extraction, or gluing.

The smallest remaining obligation on the literal all-response-zero side is
the determinant divisor \(\det H_Q=0\).  The broader node also still requires
coverage of every response pattern in which only some targets vanish and of
every nonzero-response swallowed or exceptional fibre.

## 7. Verification and dependencies

The arbitrary-point proof is Lemmas 1--3 and the two complete target-fibre
extractions above.  The focused verifier
[`verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py`](verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py)
independently generates all fifteen labelled deck classes in both diagonal
fibres, replays all 81 port words per fibre, checks the pivot determinant,
the singleton and two-line quotient obstructions, sharp three-line and
determinant-boundary controls, and the GLS9 fixture coefficient.

The genuinely independent standard-library audit
[`audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py`](audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py)
does not import the primary verifier or repository modules.  It uses dual
annihilator incidence rather than the written quotient-coordinate route,
checks the symbolic pivot and exact rational specializations, and compares
the full fifteen-pair deck with all 945 ten-vertex perfect matchings for every
outside word.  Both exact replays pass.  They check the displayed identities
and bounded sharpness controls; they do not replace the written arbitrary-point
proof.

The
[hostile theorem and scope review](../../docs/audits/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_PURE_SURVIVOR_EXCLUSION_REVIEW_2026-08-20.md)
accepts the proof, checker independence, saturation ledger, and declared open
boundary at frozen hashes.

The exploratory
[729-coefficient exact probe](../../docs/history/handoffs/R4_PURE_PI_SURVIVOR_EXACT_PROBE_2026-08-20.md)
materializes the relaxed contracted module and discovers the same singleton
minor and two-line contradiction.  It is theorem-discovery provenance, not a
physical integrability proof or the proof of arbitrary-point coverage.

Exact commands:

~~~text
python claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py
python -I claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py
python tools/explore/r4_pure_pi_survivor_exact_probe.py
~~~

Dependencies:

- [GLS4 same-pair quotient survival and complementary-permanent dominance](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [GLS7 four-root all-seven source cover](FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md)
- [GLS9 full-rank all-response-zero localization](FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md)

No external literature premise is used.
