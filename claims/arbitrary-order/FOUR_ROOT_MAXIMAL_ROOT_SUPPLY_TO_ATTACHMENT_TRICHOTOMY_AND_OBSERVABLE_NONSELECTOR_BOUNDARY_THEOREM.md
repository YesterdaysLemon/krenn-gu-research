# Four-root maximal-root supply-to-attachment trichotomy and observable-nonselector boundary

## Status

**Proved exact characteristic-zero source-integration reduction and sharp
physical boundary.** Start with an actual hypothetical complex witness whose
maximum-cardinality torus root has order four and surplus two. The GLS4
same-pair theorem supplies one residual pair \(Q\) with a nonzero physical
edge, a nonzero complementary companion, individual survival modulo all
higher-order columns, and a nonzero raw residual permanent. This note places
that same \(Q\) in two exact, independent finite branch splits.

1. Either the order-two \(Q\)-column is observable modulo every other
   order-two column and every higher column, or a minimal order-two quotient
   circuit containing \(Q\) exists over the outside function field.
2. For the six pair targets and the four-port target of GLD5--GLD13, either a
   response polynomial is identically zero, one target generically absorbs
   its desired and all three pure columns, or one common fully supported
   residual contraction legally attaches all seven nonzero responses.

On the last branch the common contraction can also retain

~~~text
h=H_Q(z_Q)!=0,                 p_(A,Q)(z_Q)!=0.        (1)
~~~

Thus the whole common-attachment branch E is an exact source-to-interface
branch: on both O and C, GLS4 already supplies the node's required individual
order-two survival modulo every higher column, while E supplies all seven
legal nonzero GLD response selectors on the same graph and the same \(Q\).
The O subbranch additionally has the stronger separation from every other
order-two column. The GLD2 augmented-weight/alignment/anchor gates are
inapplicable to this chosen GLD5/GLD7 entry; GLD3 activity and every downstream
permanent or integrability obligation remain separate.

The R and A leaves are not excluded here. A quotient circuit is only rational
deck nonuniqueness, not a second physical graph; it obstructs the stronger O
selector but is harmless for the declared individual-supply plus GLD5/GLD7
entry on E. Generic absorption can have exceptional escape fibres. An
existing maximum-root
physical graph has the stronger property that its entire order-two sensor is
injective while all seven same-\(Q\) target selectors fail with nonzero
responses. One complete mixed coefficient excludes that graph from the
witness locus. Hence neither collective pair observability nor maximal
nuisance rank closes target attachment without the full mixed target
equations.

This is a four-root source reduction, not coverage of root orders three or
at least five, and not closure of the supply-and-target-attachment node. It
supplies no permanent restriction and closes no extraction or gluing step.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Physical source and the GLS4 pair

Work over \(\mathbb C\). Let

~~~text
Omega=R disjoint-union B,       |R|=4,       |B|=6,    (2)
~~~

and assume that the graph tensor is the ternary GHZ target. Let
\((R,x_R)\) be a maximum-cardinality fully supported torus-root
configuration. For \(u\in B\), write

~~~text
L_u(z)=(W_(i,u)(x_i,z))_(i in R).                     (3)
~~~

The maximum-root theorem gives

~~~text
rank L_u>=1,             sum_(u in B)(3-rank L_u)<=6. (4)
~~~

For \(P\in\binom B2\), write

~~~text
Pi_P=per(L_u:u in B-P).                               (5)
~~~

The complete contracted mixed target equation is

~~~text
sum_(P in binom(B,2)) H_P tensor Pi_P
  =sum_(c=0)^2 mu_c tensor_(u in B)e_(u,c)^*,
mu_c!=0.                                               (6)
~~~

GLS4 and its common-contraction corollary supply a pair
\(Q=\{q_0,q_1\}\), a root pair \(A\), and a fully supported residual
contraction \(z_Q\) such that

~~~text
H_Q!=0,       Pi_Q!=0,       [G_(B-Q)]!=0 mod Gamma^(>=4),
H_Q(z_Q)!=0,                   p_(A,Q)(z_Q)!=0.        (7)
~~~

Put \(U=B-Q\), so \(|U|=4\). All subsequent branches retain this same
physical graph and this same named pair \(Q\).

## 2. Pair-block observability or an order-two circuit

Let \(K(X)\) be the outside function field used by GLS2, and put

~~~text
V=(F/im Gamma_2^(>=4)) tensor K(X),
c_P=[G_(B-P)] in V,                P in binom(B,2).    (8)
~~~

The class \(c_Q\) is nonzero by (7).

### Theorem 1 (exact pair-block split)

Exactly one of the following holds.

#### O. Observable \(Q\)-block

~~~text
c_Q notin span_(K(X)){c_P:P!=Q}.                       (9)
~~~

Equivalently, a \(K(X)\)-linear functional on the quotient is one on \(c_Q\)
and zero on every other order-two class. Together with its annihilation of
the higher columns, this is the GLS2 rational selector for the physical pair
block \(H_Q\).

#### C. Quotient circuit through \(Q\)

There is an inclusion-minimal set

~~~text
C subset binom(B,2),          Q in C,                 (10)
~~~

and nonzero coefficients \(a_P\in K(X)\), normalized by \(a_Q=1\), such
that

~~~text
c_Q+sum_(P in C-{Q}) a_P c_P=0.                       (11)
~~~

Lifting to the sensor and applying the GLS4 base-root functional, extended
\(K(X)\)-linearly, gives

~~~text
G_(B-Q)+sum_(P in C-{Q})a_P G_(B-P)
     in im Gamma_2^(>=4),

Pi_Q+sum_(P in C-{Q})a_P Pi_P=0                       (12)
~~~

in the corresponding \(K(X)\)-extension of the complementary-tensor space.

In particular, at least one other \(\Pi_P\) in the circuit is nonzero.

### Proof

Finite-dimensional separation over \(K(X)\) gives the functional in O
exactly when (9) holds. If (9) fails, choose an inclusion-minimal spanning
dependence containing \(Q\), normalize its \(Q\)-coefficient, and delete any
zero coefficient. This gives C. Conversely, (11) forbids the separating
functional, so the alternatives are disjoint and exhaustive.

Equation (11) is an equality in the quotient, hence lifts to the first line
of (12). The base-root functional kills every higher companion and sends
\(G_{B-P}\) to the generic evaluation of \(\Pi_P\), proving the second line.
Since \(\Pi_Q\ne0\), not all other terms vanish. \(\square\)

The coefficients in (11)--(12) are rational functions. On a chosen affine
chart, clearing them requires one displayed common nonzero denominator and
saturation by that denominator; no specialization at a pole is covered.

Modulo the higher columns, (6) has only the linear form

~~~text
bar J=sum_P H_P c_P.                                  (13)
~~~

A circuit makes this rational deck representation nonunique: adding a
scalar multiple of its coefficient vector preserves (13), and one multiple
removes the \(Q\)-coordinate. The shifted coordinates need not obey the
nonlinear principal-hafnian recurrence of any graph. Thus C is not a
physical same-state fibre and is not contradicted by (13) alone.

## 3. Complete seven-target attachment split

Let

~~~text
T_Q=(G_m)^6=Spec Lambda,
Lambda=C[z_(q,c)^(+/-1):q in Q,c=0,1,2],
F_Q=Frac(Lambda),
F_7=binom(U,2) union {U}.                              (14)
~~~

For each \(S\in\mathcal F_7\), retain the complete fixed-\(Q\) GLD5 module.
In fixed bases write

~~~text
B_S(z)    for all nuisance coefficient slices,
g_S(z)    for the desired companion column,
D_S=[d_(S,0)|d_(S,1)|d_(S,2)]    for the pure columns,
P_S(H;z)  for the physical response,
r_S=rank_(F_Q) B_S.                                   (15)
~~~

No nuisance label is removed. Pair targets have \(729\) coefficient rows
and the four-port target has \(81\).

### Theorem 2 (same-pair common attachment or exhaustive failure branch)

Exactly one of the following algebraic alternatives holds.

#### R. Response-identically-zero branch

For at least one \(S\in\mathcal F_7\),

~~~text
P_S(H;z)=0                       in W_S tensor Lambda. (16)
~~~

#### E. Common seven-target escape

Every response polynomial is nonzero and, for every \(S\in\mathcal F_7\),

~~~text
rank_(F_Q)[B_S|g_S]=r_S+1.                            (17)
~~~

There is a nonempty Zariski-open \(\Omega\subset T_Q\) such that every
\(z\in\Omega(\mathbb C)\) satisfies, simultaneously,

~~~text
H_Q(z)!=0,             p_(A,Q)(z)!=0,
[g_S(z)]!=0,           P_S(H;z)!=0,
q_S(z)=1                         for every S in F_7.   (18)
~~~

Thus the same graph, \(Q\), and residual contraction supply all six physical
pair responses and the physical four-port response through seven legal
constant GLD5 selectors.

#### A. Function-field desired-plus-pure absorption

Every response polynomial is nonzero and, for at least one
\(S\in\mathcal F_7\),

~~~text
rank_(F_Q)[B_S|g_S]=r_S.                              (19)
~~~

For every such \(S\), the complete witness equation forces

~~~text
rank_(F_Q)[B_S|g_S|D_S]=r_S.                          (20)
~~~

Equivalently, after choosing one nonzero common Laurent denominator
\(\delta_S\), there are nuisance coefficient vectors satisfying

~~~text
B_S b_(S,g)=delta_S g_S,
B_S b_(S,c)=delta_S d_(S,c),           c=0,1,2.       (21)
~~~

The identities hold pointwise on \(D(\delta_S)\). Exceptional fibres on
\(V(\delta_S)\), including nuisance-rank drops, may still escape.

### Proof

Alternative R is disjoint from the other two. If R fails, every response
tensor has a nonzero Laurent coordinate. Adjoining one column changes rank
by zero or one, so either (17) holds for all seven targets or (19) holds for
at least one. These rank patterns give the disjoint and exhaustive E/A
split.

Assume E. For each \(S\), choose a nonzero \(r_S\)-minor of \(B_S\), with
the \(0\times0\) minor understood to be one when \(r_S=0\), a
nonzero \((r_S+1)\)-minor of \([B_S|g_S]\), and one nonzero coordinate of
\(P_S(H;z)\). Multiply these finitely many Laurent polynomials by

~~~text
H_Q(z) p_(A,Q)(z).                                    (22)
~~~

Every factor is nonzero, and \(\Lambda\) is an integral domain. The product
therefore defines a nonempty principal open. On it, every nuisance rank and
augmented rank is the generic rank, all responses are nonzero, and (1)
holds. GLD7 applied to the complete fixed-\(Q\) witness identity gives
\(q_S=1\), while GLD5 supplies the normalized legal constant selector. This
proves (18).

Assume A and work over \(F_Q\). In the quotient by
\(\operatorname{im}B_S\), condition (19) gives \([g_S]=0\). The complete
GLD7 quotient identity is

~~~text
sum_(c=0)^2 alpha_c[d_(S,c)] tensor w_(S,c)
  =[g_S] tensor P_S(H)=0.                              (23)
~~~

The \(\alpha_c\) are Laurent units and the \(w_{S,c}\) are independent, so
every pure class vanishes. This is (20). Solve the four column equations
over \(F_Q\) and clear all denominators with one nonzero \(\delta_S\), giving
(21). No statement is made at its zero locus. \(\square\)

### Corollary 2.1 (exact four-root source case cover)

Every source point in (2)--(7) lies in one of the six combined leaves

~~~text
{O,C} x {R,E,A}.                                      (24)
~~~

Both leaves \(O\times E\) and \(C\times E\) reach the declared individual
pair-supply and same-\(Q\) seven-target attachment interface. The O leaf also
has full order-two separation for \(Q\). The remaining four leaves reduce to
two genuinely different obligations:

1. exclude every response-identically-zero branch R; and
2. exclude A on its generic open and every exceptional divisor, or exhibit
   an exceptional common escape and return it to E.

If a different downstream entry expressly requires collective order-two or
full fixed-\(Q\) observability, C becomes an additional obligation for that
stronger interface. It is not an obligation for the GLD5/GLD7 entry used here.

This is source-level branch coverage for root order four. It does not claim
that the four R/A leaves are empty.

## 4. Collective pair observability does not force target attachment

Consider the maximum-root, triple-blocker physical graph in the
four-root simultaneous swallowed-pure theorem, at the all-one contraction.
Every root--root block is zero. Order its fifteen order-two companion
columns by the outside pairs.

### Theorem 3 (exact observable nonselector control)

At the all-one contraction, the \(81\times15\) order-two companion matrix of
that graph has rank fifteen. One \(15\times15\) minor, on the root words

~~~text
0000,0001,0010,0020,0021,0022,0100,0101,0110,0200,
1000,1001,1010,1101,2010,                              (25)
~~~

has determinant \(-1\). This is one specialization of a polynomial
order-two minor, so that minor is not the zero polynomial and the generic,
hence \(K(X)\)-, order-two rank is fifteen. Every higher companion column is
zero. Hence the entire order-two family is observable over the outside
function field, including the pair
\(Q=\{q_0,q_1\}\). For this \(Q\),

~~~text
H_Q=e_0^* tensor e_0^*!=0,
Pi_Q[1111]=1,
(p_(A,Q)(1,1))_A=(2,1,1,1,1,1).                      (26)
~~~

Nevertheless, all seven physical responses are nonzero and all seven GLD5
desired classes vanish. The graph is not a witness: its complete mixed
coefficient at the word

~~~text
1200100020                                             (27)
~~~

equals one.

### Proof

With zero root--root blocks, the companion grade rule kills every order at
least four. Exact root-to-outside injection expansion at the all-one point
gives the displayed minor and determinant. Since the minor is a polynomial
in the residual contraction coordinates, its one nonzero specialization
makes the order-two quotient map injective over the function field. The
values in (26) follow by direct evaluation of the named pair edge, its
complementary four-root permanent, and the six two-root/two-residual
permanents. The owning swallowed-pure theorem proves the seven nonzero
responses, the seven vanishing desired classes, and the unique matching of
coefficient (27). \(\square\)

This control is not on the complete target locus, so it does not refute the
desired bridge. It proves that even the O branch, nonzero \(h\), nonzero
raw \(p\), maximum-root incidence, local concision, pure normalization,
Hamming-one vanishing, and nonzero responses do not imply E. A successful
exclusion of A/R must use additional complete mixed coefficients or a
physical companion-exchange identity that entails them.

## 5. Proof-DAG consequence

The four-root source edge is now

~~~text
actual maximum-root surplus-two witness
  -> same Q with h!=0 and raw p!=0
  -> {observable pair block O | quotient circuit C}
  -> {response zero R | common seven attachment E | generic absorption A}.
                                                               (28)
~~~

What is proved and what remains are:

~~~text
same-pair h/p common contraction:                         PROVED;
pair-observable or named quotient circuit:                PROVED EXHAUSTIVE;
response-zero / common escape / generic absorption:       PROVED EXHAUSTIVE;
E reaches individual pair plus legal seven-target interface: PROVED;
O x E additionally reaches stronger pair observability:   PROVED;
collective pair observability alone forces attachment:    FALSE OFF TARGET;
R excluded on witnesses:                                  OPEN;
A plus exceptional divisors excluded on witnesses:        OPEN;
root orders r=3 and r>=5 source-integrated:                OPEN;
supply-and-target-attachment strategic node:               OPEN;
global Krenn--Gu conjecture:                               UNRESOLVED.       (29)
~~~

No finite support atlas is used. The open node leaves are the response
polynomial identity (16) and the four-column function-field identities (21),
with every denominator shown. These are the smallest current support-free
inputs for a physical mixed-coefficient syzygy. The quotient-circuit identity
(11) is an additional input only for a different downstream entry that
requires stronger pair-block observability; it does not obstruct the declared
GLD5/GLD7 entry on E.

## 6. Verification and dependencies

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_four_root_maximal_root_supply_to_attachment_trichotomy_and_observable_nonselector_boundary.py
python -I claims/arbitrary-order/audit_four_root_maximal_root_supply_to_attachment_trichotomy_and_observable_nonselector_boundary.py
python -m py_compile claims/arbitrary-order/verify_four_root_maximal_root_supply_to_attachment_trichotomy_and_observable_nonselector_boundary.py claims/arbitrary-order/audit_four_root_maximal_root_supply_to_attachment_trichotomy_and_observable_nonselector_boundary.py
uv run --with ruff ruff check claims/arbitrary-order/verify_four_root_maximal_root_supply_to_attachment_trichotomy_and_observable_nonselector_boundary.py claims/arbitrary-order/audit_four_root_maximal_root_supply_to_attachment_trichotomy_and_observable_nonselector_boundary.py
```

The focused primary verifier replays the circuit linear algebra, the finite
E/R/A controls, the exact minor in (25), and (26)--(27) with exact SymPy
arithmetic. The independent no-import audit uses only the Python standard
library, separately constructed rational row reduction, direct matching
recurrences, and an independent finite branch census. The arbitrary witness
implication is the written combination of GLS4, GLD5, GLD7, and GLD13;
bounded computation does not prove it.

Dependencies:

- [same-pair quotient survival and complementary-permanent dominance](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [common residual contraction and augmented-alignment gate](MAXIMAL_ROOT_SURPLUS_TWO_COMMON_RESIDUAL_CONTRACTION_AND_AUGMENTED_ALIGNMENT_GATE_THEOREM.md)
- [complete-deck sensor](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md)
- [constant target-module selector quotient](FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md)
- [target quotient rank-one trichotomy](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md)
- [contraction escape or generic pure absorption](FIXED_Q_CONTRACTION_ESCAPE_OR_FUNCTION_FIELD_PURE_ABSORPTION_DICHOTOMY_THEOREM.md)
- [simultaneous swallowed-pure physical control](FOUR_ROOT_SIMULTANEOUS_SWALLOWED_PURE_NONZERO_RESPONSE_PHYSICAL_CONTROL_THEOREM.md)
