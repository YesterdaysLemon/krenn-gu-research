# Maximal-root surplus-two same-pair quotient survival and complementary-permanent dominance

## Status

**Exact characteristic-zero source-to-supply theorem and structural route
boundary.**  On the maximum-root surplus-two locus, the complete contracted
mixed GHZ identity forces one outside pair \(Q\) to satisfy all of the
following on the same physical graph:

1. the physical pair block \(H_Q\) is nonzero;
2. its complementary order-two companion is nonzero and survives modulo
   every order-four-and-higher companion column; and
3. some two-root/two-\(Q\) permanental incidence \(p_{A,Q}\) is nonzero, at a
   fully supported residual contraction.

The point is the **same-pair** conclusion.  Nonvanishing of the complete
complementary permanent and nonvanishing of a two-root residual permanent do
not have to be obtained from unrelated pairs.

This is individual order-two quotient survival.  It is strictly weaker than
collective pair-observability, fixed-\(Q\) observability of the full GLS2
coordinate family, or a legal GLD5/GLD7 target selector.  In particular, the
theorem does not supply the augmented GLD2 weight, alignment, synchronized
response rows, nuisance survival, or a target-pure anchor.

A second theorem proves that the vector of scalar complementary permanents is
dominant on its ambient incidence space.  Thus it satisfies no universal
Grassmann--Pluecker-style polynomial identity.  Any continuation from the
same-pair supply proved here to legal target attachment must use tensor-valued
root polarizations, higher companions, physical hafnian recurrence, or
complete target coupling; scalar base-root readings alone cannot do it.

For an actual hypothetical witness, the source application is over
\(\mathbb C\), matching the owning maximum-root theorem.  The algebra below
works over any characteristic-zero field once its displayed incidence and
target hypotheses are assumed.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Source notation and the contracted complete target

Work over a characteristic-zero field \(K\).  Let

```text
Omega=R disjoint-union B,       |R|=r>=3,       |B|=r+2.       (1)
```

Every local space is three-dimensional.  Fix fully supported root vectors
\(x_i\), \(i\in R\), such that

```text
W_ij(x_i,x_j)=0                         for i!=j.       (2)
```

For each outside mode \(u\), put

```text
L_u:V_u -> K^r,
z |-> (W_(i,u)(x_i,z))_(i in R).                         (3)
```

Assume the maximum-root surplus-two incidence consequences

```text
rank L_u>=1,
sum_(u in B) (3-rank L_u)<=6.                           (4)
```

For \(Q\in\binom B2\), let \(H_Q\) be the physical outside edge tensor and
write \(\Pi_Q\) for its complementary permanent tensor:

```text
Pi_Q=per(L_u:u in B-Q)
    in tensor_(u in B-Q) V_u^*.                         (5)
```

Thus \(\Pi_Q\) is the base-root contraction of the order-two companion
\(G_{B-Q}\).  The exact surplus-two fixed layer of the hypothetical-witness
identity is

```text
sum_(Q in binom(B,2)) H_Q tensor Pi_Q
 =sum_(c=0)^2 mu_c tensor_(u in B)e_(u,c)^*,            (6)
mu_c=lambda_c product_(i in R)e_(i,c)^*(x_i) !=0.
```

The normalized GHZ target has \(\lambda_c=1\).  Allowing arbitrary nonzero
\(\lambda_c\) records the invariant weighted-diagonal scope.  Equation (6)
is a tensor identity on all \(r+2\) outside modes; it includes every mixed
outside word, not only the pure and Hamming-one shells.

Call \(Q\) **active** when

```text
H_Q tensor Pi_Q !=0.                                   (7)
```

For \(Q=\{q_0,q_1\}\), a root pair \(A=\{i,j\}\), and residual vectors
\(z_0,z_1\), define

```text
p_(A,Q)(z_0,z_1)
 =L_(q0)(z_0)_i L_(q1)(z_1)_j
  +L_(q0)(z_0)_j L_(q1)(z_1)_i.                       (8)
```

This is the two-root/two-residual permanent used in GLS3 and in the GLD2
four-root augmented-weight ledger.

## 2. Every active complementary reading survives the higher grades

Put \(X=\prod_{u\in B}\mathbb P(V_u)\), let \(K(X)\) be its function field,
and work at the generic point of \(X\).  After trivializing the common
outside multidegree, write

```text
F_eta=(tensor_(i in R)V_i^*) tensor_K K(X).
```

Let \(\Gamma_2^{(\ge4)}\) denote the restriction, over \(K(X)\), of the
GLS2 companion sensor to outside labels of order at least four.

### Lemma 1 (base-root quotient functional)

The \(K(X)\)-linear functional

```text
epsilon_x:F_eta -> K(X)
```

obtained by contracting every open root slot with \(x_R\) annihilates
\(\operatorname{im}\Gamma_2^{(\ge4)}\).  It sends the order-two column
\(G_{B-Q}\) to the generic evaluation of \(\Pi_Q\).  Consequently,

```text
Pi_Q!=0
  => [G_(B-Q)]!=0 in F_eta/im Gamma_2^(>=4).           (9)
```

### Proof

An outside label \(I\) of order \(2+2p\) has root--root grade \(p\).  If
\(|I|\ge4\), then \(p\ge1\), so every matching in its companion contains a
root--root edge.  Under the root contraction that edge contributes one of
the scalars in (2), hence every such column vanishes.  An order-two companion
has grade zero: every root is injected into \(B-Q\), and its contraction is
exactly the generic evaluation of the permanent tensor (5), which is nonzero
in \(K(X)\) precisely when \(\Pi_Q\ne0\).  The functional \(\epsilon_x\)
therefore descends to the displayed \(K(X)\)-quotient, where a class with
nonzero image cannot vanish.  No exceptional factor is divided out.  The
outside variables are generic only because GLS2 defines observability over
\(K(X)\); the fixed root vectors \(x_R\) are not varied.  \(\square\)

Equation (6) has nonzero right side, so at least one active \(Q\) exists.
Lemma 1 already proves individual pair-column survival.  The next theorem
shows that one can choose an active pair which also carries the GLS3 raw
residual incidence.

## 3. Same-pair exchange theorem

For nonzero \(b\in K^r\), put

```text
S_b={a in K^r:
     a_i b_j+a_j b_i=0 for every i<j}.                 (10)
```

### Lemma 2 (symmetric-product kernel)

In characteristic zero,

```text
dim S_b<=1.                                            (11)
```

### Proof

If \(b\) has one nonzero coordinate, every other coordinate of \(a\) is
zero.  If it has two, the same equations kill the coordinates off that
support and leave one relation on the remaining two.  If it has at least
three, write \(\rho_i=a_i/b_i\) on three nonzero coordinates.  Pairwise
relations give \(\rho_i=-\rho_j=-\rho_k\), while the \(j,k\) relation gives
\(\rho_j=-\rho_k\); characteristic zero forces all three to vanish, and the
remaining equations kill every other coordinate.  \(\square\)

### Theorem 3 (same-pair quotient survival and raw residual supply)

Under (1)--(6), there are a pair \(Q=\{q_0,q_1\}\), a root pair
\(A=\{i,j\}\), and fully supported residual vectors \(z_0,z_1\) such that

```text
H_Q!=0,
Pi_Q!=0,
[G_(B-Q)]!=0 in F_eta/im Gamma_2^(>=4),
p_(A,Q)(z_0,z_1)!=0.                                  (12)
```

### Proof

Suppose instead that \(p_{A,Q}\) is the zero polynomial for every active
pair \(Q\) and every root pair \(A\).

Fix an active \(Q=\{u,v\}\).  Its two incidence images are nonzero by (4).
For a fixed nonzero \(b\in\operatorname{im}L_v\), the assumed vanishing of
all (8) puts \(\operatorname{im}L_u\) inside \(S_b\).  Lemma 2 gives
\(\operatorname{rank}L_u=1\), and the symmetric argument gives
\(\operatorname{rank}L_v=1\).  Hence every active pair joins two rank-one
outside modes.

Let

```text
D={u in B:rank L_u=1}.                                 (13)
```

Each member of \(D\) contributes two to the corank sum (4), so \(|D|\le3\).
There is an active pair, hence \(|D|\ge2\).

If \(|D|=2\), only the pair \(D\) can be active, and (6) has one nonzero
summand \(H_D\otimes \Pi_D\).  Across the bipartition \(D\mid B-D\), that
summand has flattening rank one.  The right side of (6) has flattening rank
three: on both shores the three displayed pure coordinate tensors are
linearly independent and every \(\mu_c\) is nonzero.  This is impossible.

It remains to consider

```text
D={a,b,c},                  T=B-D,        |T|=r-1.     (14)
```

Write the three rank-one maps as

```text
L_u(z)=alpha_u ell_u(z),
alpha_u in K^r-{0},         ell_u in V_u^*-{0}.        (15)
```

Every active pair lies in \(D\).  For the three possible pairs, permanent
expansion at the remaining member of \(D\) gives

```text
Pi_(bc)=ell_a tensor K_a,
Pi_(ac)=ell_b tensor K_b,
Pi_(ab)=ell_c tensor K_c,                              (16)
```

for tensors \(K_u\in\bigotimes_{t\in T}V_t^*\), possibly initially zero.

Quotient the three \(D\)-mode dual spaces by the lines \(K\ell_u\).  Every
term on the left of (6) vanishes because (16) places one \(\ell_u\) in each
term.  The three pure tensors on \(T\) are linearly independent, so for each
target colour \(d\), at least one of the three quotient classes of
\(e_{u,d}^*\) is zero.  One line \(K\ell_u\) contains at most one of the
three independent coordinate covectors.  The three colours therefore require
three distinct mode--colour incidences, one on each low mode.  After
relabelling \(a,b,c\), relabelling the target colours, and rescaling the
rank-one factorizations in (15),

```text
ell_a=e_(a,0)^*,       ell_b=e_(b,1)^*,
ell_c=e_(c,2)^*.                                      (17)
```

Take in (6) the coefficient of the low-mode words \(000\), \(111\), and
\(222\), respectively.  In each word exactly one term in (16) can survive.
Writing \(E_d^T=\bigotimes_{t\in T}e_{t,d}^*\), one obtains

```text
H_(bc)[00] K_a=mu_0 E_0^T,
H_(ac)[11] K_b=mu_1 E_1^T,
H_(ab)[22] K_c=mu_2 E_2^T.                            (18)
```

Every scalar and tensor on the right is nonzero.  Hence all three triangle
pairs are active, while \(K_a,K_b,K_c\) are nonzero and pairwise linearly
independent.

There is one common linear cofactor map behind (16).  For a root \(i\), let
\(D_i\) be the permanent tensor assigning the other \(r-1\) roots to the
\(r-1\) high modes \(T\), and define

```text
Psi:K^r -> tensor_(t in T)V_t^*,
Psi(v)=sum_(i in R) v_i D_i.                           (19)
```

Then \(K_u=\Psi(\alpha_u)\) for \(u=a,b,c\).

Because the pairs \(\{a,b\}\) and \(\{a,c\}\) are active, the assumed raw
failure and (15) imply

```text
alpha_b in S_(alpha_a),       alpha_c in S_(alpha_a). (20)
```

Lemma 2 says this common space has dimension at most one.  Thus
\(\alpha_b\) and \(\alpha_c\) are proportional, so their images \(K_b\) and
\(K_c\) under the same linear map (19) are proportional.  This contradicts
(18).  The supposition was false.

We have therefore found an active \(Q\) for which some polynomial (8) is
nonzero.  A characteristic-zero field is infinite, and the fully supported
torus in \(V_{q_0}\times V_{q_1}\) is Zariski dense, so (8) is nonzero at
some fully supported \((z_0,z_1)\).  Activity gives \(H_Q,\Pi_Q\ne0\), and
Lemma 1 gives the quotient survival in (12).  \(\square\)

### Corollary 4 (actual maximum-root witness source)

Every actual hypothetical complex witness in the maximum-root surplus-two
scope of M1 has a same pair \(Q\) satisfying (12).

### Proof

M1 supplies (1)--(4) over \(\mathbb C\); in particular its five-outside-mode
bound rules out \(r=2\) at surplus two.  The complete hypothetical-witness
tensor equality supplies (6).  Apply Theorem 3.  \(\square\)

## 4. Why scalar complementary permanents have no Pluecker relation

Theorem 3 used the target tensor, the corank quota, and the common cofactor
map.  It cannot be replaced by a universal polynomial identity among the
scalar complementary permanent readings alone.

For \(r\ge2\), define

```text
Phi_r:Mat_(r x (r+2)) -> K^(binom(r+2,2)),
Phi_r(A)_Q=per(A with the two columns Q deleted).       (21)
```

### Theorem 5 (complementary-permanent dominance)

If \(\operatorname{char}K\ne2\), then \(\Phi_r\) is dominant.  Equivalently,
the coordinates in (21) satisfy no nonzero universal polynomial relation.

### Proof

Label the final two columns \(a,b\), and evaluate at

```text
A_0=[I_r | 1 | 1].                                    (22)
```

Write the outputs as \(p_{ab},p_{ia},p_{ib},p_{ij}\).  At (22),

```text
p_ab=1,             p_ia=p_ib=1,             p_ij=2. (23)
```

For \(i<j\), let \(x_{ij}\) be the row-\(i\), identity-column-\(j\) entry and
put

```text
D_ij=partial_(x_ij)-partial_(a_i)-partial_(b_i).       (24)
```

Expanding a permanent at the changed entry gives

```text
dp_ab(D_ij)=dp_ka(D_ij)=dp_kb(D_ij)=0,
dp_kl(D_ij)=-2 delta_({k,l},{i,j}).                    (25)
```

Indeed, for a pair \(\{k,l\}\) containing \(i\) but not \(j\), the
\(x_{ij}\)-derivative has the two assignments of \(a,b\) and cancels the two
subtracted derivatives.  For \(\{i,j\}\), identity column \(j\) is absent,
so only the two subtracted derivatives remain.  Every other case is zero.

The \(\binom r2\) directions (24), followed by

```text
partial_(a_i), partial_(b_i)  (1<=i<=r),
partial_(x_11),                                       (26)
```

give a square Jacobian minor.  The first block is \(-2I\); the next two
blocks contain the two identity matrices for the \(p_{ib}\) and \(p_{ia}\)
outputs; and \(\partial_{x_{11}}p_{ab}=1\).  After block elimination its
determinant is

```text
plus-or-minus 2^(binom(r,2)) !=0.                     (27)
```

Thus the differential of \(\Phi_r\) is surjective at \(A_0\).  A morphism
with a surjective differential at one smooth source point is dominant.
The induced map on coordinate rings is injective, proving the final
formulation.  \(\square\)

The nonzero factor two in (25) is the bosonic exchange defect: the alternating
sign that creates Grassmann--Pluecker relations is absent for permanents.

## 5. Exact proof-DAG consequence

The maximum-root surplus-two supply hierarchy is now:

```text
some same Q has H_Q!=0, individual order-two quotient survival,
and a nonzero raw p_(A,Q):                              PROVED;

collective pair-observability:                         OPEN;
fixed-Q full-coordinate-family observability:         OPEN;
same-Q GLD5/GLD7 legal response/target attachment:     OPEN;
GLD2 augmented l, Omega, alignment, and anchor:         OPEN.     (28)
```

The scalar readings \(\Pi_Q\) have zero ambient elimination ideal by Theorem
5.  The smallest remaining node obligation is therefore to couple the
same-\(Q\) supply in (12) to the decomposable target-selector quotient, or to
send every nonzero selector defect--including maximal-nuisance-rank,
response-zero, and exceptional-rank fibres--to a complete mixed GHZ
contradiction on the same graph.

This theorem supplies no permanent restriction and closes no downstream
extraction/gluing obligation.  The global conjecture remains **UNRESOLVED**.

## 6. Verification and evidence boundary

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py claims/arbitrary-order/audit_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py claims/arbitrary-order/audit_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py
```

The focused verifier replays the finite matching-grade, triangle, and exact
Jacobian identities with symbolic arithmetic.  The independent no-import
audit uses standard-library sparse tensors, direct injection/permanent
enumeration, and separately written rational row reduction.  These programs
audit the displayed identities and conventions at bounded ranks.  The
arbitrary-\(r\) matching partition, quotient, symmetric-kernel, and Jacobian
arguments above are the proofs.

Dependencies:

- [`maximum torus-root saturation and coordinate absorption`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md)
- [`surplus-two complete-deck sensor`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md)
- [`nonzero raw pair companion and rank-drop boundary`](MAXIMAL_ROOT_SURPLUS_TWO_NONZERO_PAIR_COMPANION_AND_PHYSICAL_RANK_DROP_SHARPNESS_THEOREM.md)
