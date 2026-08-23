# Maximum-root surplus-two zero-anchor rank-four full-swallow off-diagonal root-deck complete exclusion

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise fibre exclusion.**  Fix
one `GLS8`-eligible promoted chart, one residual contraction, and the
zero-anchor incidence map of `GLS36`.  If the raw nuisance has rank four and
fully swallows the root companion and all three pure probe tensors, then the
root companion must lie in the diagonal three-plane:

```text
omega=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=4
  => q in Delta=span{r_0,r_1,r_2}.                  (1)
```

Equivalently, the `q notin Delta`, zero-excess rank-four line in the `GLS40`
full-swallow stratification is empty.  The proof uses the complete
whole-domain labelled incidence family.  It covers arbitrary port-domain
dimensions, every residual-shore and incidence-rank drop, and every divisor
fibre.  It does not divide by a response, a shore coordinate, or a chosen
minor.

The theorem does not exclude the surviving rank-four `q in Delta` branch,
any rank at least five, or a raw-escape branch.  It does not supply a legal
selector, physical response, synchronization, selected activity, nuisance
survival, an attachment anchor, a downstream receiver, or arbitrary-root
source coverage.  The maximum-root surplus-two strategic node and the global
Krenn--Gu conjecture remain **UNRESOLVED**.

This is `GLS43`.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted chart and legal attachment boundary;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the exact equality `B_Q^anc=im sigma_Q` and its whole-domain labelled
  components;
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the unconditional rank floor `rank B_Q^anc>=4` on full swallow; and
- [`GLS40`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_THEOREM.md)
  for the canonical split by `q in Delta` and the identification of (1)'s
  excluded line as the rank-four zero-excess fibre.

`GLS41` and `GLS42` remain downstream boundaries rather than proof
dependencies: they explain why eliminating one incidence fibre does not by
itself produce pure-core survival or a useful physical attachment.

No external literature claim is used.  The new content is the complete
rank-one-shore quotient obstruction, the rank-two-shore normalization and
alignment argument, and the terminal three-coordinate compatibility lemma.

## 1. Incidence setting

Let `K` have characteristic zero.  Identify

```text
E_A^*=K^3 tensor K^3,
r_i=e_i tensor e_i,
Delta=span{r_0,r_1,r_2}.                             (2)
```

Retain the fixed residual shores and every promoted-port incidence map

```text
a_s=xi_0^s in K^3,              b_s=xi_1^s in K^3,
X_u:V_u -> K^3,                 Y_u:V_u -> K^3,

q=a_0 tensor b_1+a_1 tensor b_0.                    (3)
```

The complete `GLS36` incidence map has components

```text
sigma_(s,u)(v)
 =a_s tensor Y_u(v)+X_u(v) tensor b_s,              (4)

sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x)         (5)
```

for every residual label `s`, promoted label `u`, distinct promoted labels
`u,v`, and every vector in the indicated whole domain.  On `omega=0`,

```text
B=B_Q^anc=im sigma_Q.                                (6)
```

Assume for contradiction that the hypotheses on the left of (1) hold and
that `q notin Delta`.  Since `Delta+Kq` has dimension four and is contained
in the four-dimensional space `B`,

```text
B=S:=Delta+Kq.                                       (7)
```

Put

```text
A=span{a_0,a_1},       C=span{b_0,b_1},
d_0=dim A,             d_1=dim C.                   (8)
```

The nonzero tensor `q` rules out `d_0=0` and `d_1=0`, so each residual shore
has rank one or two.

## 2. Rank-one residual shores cannot generate full swallow

### Lemma 1 (quotient-line lemma)

Let `a,b` be nonzero vectors in `K^3`, let

```text
pi:K^3 -> K^3/Ka,
Dbar=span{pi(e_i) tensor e_i:i=0,1,2}.               (9)
```

Then

```text
L(a,b)={pi(x):pi(x) tensor b in Dbar}                (10)
```

has dimension at most one.

#### Proof

Choose `j` with `b_j!=0`.  Compare the coefficient of the second-factor
basis vector `e_j` in a presentation of `pi(x) tensor b` in (9).  It gives

```text
b_j pi(x) in K pi(e_j).
```

Thus every element of (10) lies on the fixed line `K pi(e_j)`. `square`

### Lemma 2 (rank-one-shore exclusion)

Under (7), neither `d_0` nor `d_1` can equal one.

#### Proof

Suppose `d_0=1`, so `A=Ka` for some nonzero `a`.  The root companion `q`
has every left factor in `A`.  Choose `s` with `b_s!=0`, which exists because
`q!=0`.

Fix any promoted label `u` and any `v in V_u`, and write

```text
x=X_u(v),                  y=Y_u(v).
```

Equation (4) belongs to `S`.  Quotient its left factor by `A`.  The term
`a_s tensor y` and the `Kq` part disappear, leaving

```text
pi(x) tensor b_s
 in span{pi(e_i) tensor e_i:i=0,1,2}.               (11)
```

Lemma 1 puts every `pi(X_u(V_u))` in one fixed quotient line.  Hence

```text
L_0=A+sum_u im X_u
```

has dimension at most two.  Every tensor in every component (4)--(5) has
all left factors in `L_0`, so

```text
B subset L_0 tensor K^3.                             (12)
```

But `Delta subset B` forces all three `e_i` into `L_0`, contradicting
`dim L_0<=2`.  Transposing every tensor gives the same contradiction when
`d_1=1`. `square`

It remains only to treat

```text
(d_0,d_1)=(2,2).                                    (13)
```

## 3. Rank-two residual shores align after diagonal covariance

In (13), the factorization in (3) has rank two.  Let nonzero vectors
`alpha,beta in K^3` span its left and right kernels:

```text
alpha^T q=0,          q beta=0,
A=ker alpha^T,        C=ker beta^T.                  (14)
```

Put

```text
L_0=A+sum_u im X_u,       L_1=C+sum_u im Y_u.        (15)
```

As in (12), `B subset L_0 tensor K^3` and
`B subset K^3 tensor L_1`.  Since `Delta subset B`,

```text
L_0=L_1=K^3.                                         (16)
```

### Lemma 3 (both residual normals have full coordinate support)

Every coordinate of `alpha` and every coordinate of `beta` is nonzero.

#### Proof

By (16), choose a port slice `x=X_u(v)` outside `A`, with paired slice
`y=Y_u(v)`.  For each `s`, put

```text
m_s=a_s y^T+x b_s^T in S.                           (17)
```

Multiplication by `alpha^T` kills both the first term of (17) and `q`.
Because `alpha^T x!=0` and the remaining diagonal part has support only on
`supp alpha`, both `b_0,b_1` are supported on `supp alpha`.  Their
independence gives `|supp alpha|>=2`.

If `|supp alpha|=2`, then `C` is exactly that coordinate two-plane and
`beta` is the complementary coordinate axis.  By (16), choose a paired
slice with `y notin C`.  Right multiplication of (17) by `beta` now forces
both independent `a_s` into the one coordinate axis `supp beta`, a
contradiction.  Hence `alpha` has full support.  The transposed argument
shows the same for `beta`. `square`

Put `D_alpha=diag(alpha_0,alpha_1,alpha_2)` and define `D_beta` similarly.
The covariance `M -> D_alpha M D_beta` is invertible, preserves `Delta`
setwise, and transforms every vector and every whole-domain incidence
component in (3)--(7) together.  Lemma 3 therefore permits the normalization

```text
alpha=beta=1=(1,1,1)^T,
A=C=H={z:1^T z=0}.                                  (18)
```

### Lemma 4 (residual and port shore alignment)

After (18), there is one scalar `c!=0` such that

```text
b_s=c a_s                    for s=0,1,
Y_u=c X_u                    for every promoted u.  (19)
```

#### Proof

Both row and column sums of `q` vanish.  Every matrix in
`S=Delta+Kq` therefore has the same row-sum and column-sum vectors.  Apply
this to (17).  Since `a_s,b_s in H`, for every port slice `(x,y)` one gets

```text
(1^T y)a_s=(1^T x)b_s                 for s=0,1.     (20)
```

Equation (16) supplies a slice with `x notin H`.  Dividing only by the
nonzero scalar `1^T x` in this contradiction branch, (20) gives
`b_s=c a_s` for one common `c`; independence makes `c!=0`.  Equation (20)
then gives `1^T y=c 1^T x` for every slice.

Now `q=c(a_0a_1^T+a_1a_0^T)`, so every element of `S` is symmetric.
Symmetry of (17) gives

```text
a_s(y-cx)^T=(y-cx)a_s^T                 for s=0,1.   (21)
```

For nonzero `a_s`, (21) says that `y-cx` is proportional to `a_s`.  The two
`a_s` are independent, so `y=cx`.  This holds on every input vector and
proves the map identity in (19). `square`

## 4. The terminal three-coordinate compatibility lemma

For vectors `u,v`, write

```text
sym(u,v)=uv^T+vu^T.
```

After Lemma 4, every one-residual incidence slice is
`c sym(a_s,x)`.  Since `a_0,a_1` span `H`, every port slice `x` obeys

```text
sym(a,x) in Delta+Kq        for every a in H.        (22)
```

Write the nonzero off-diagonal coordinate vector of the symmetric `q` as

```text
f=(q_01,q_02,q_12)=(r,s,t)!=0.                       (23)
```

### Lemma 5 (three-coordinate line classification)

For a fixed nonzero `f`, the solution space of (22) is either zero or one
of the following three lines:

```text
f proportional to (1,-1,-1):   x in K(1,1,0),
f proportional to (1,-1, 1):   x in K(1,0,1),
f proportional to (1, 1,-1):   x in K(0,1,1).       (24)
```

#### Proof

Use the basis `e_0-e_1,e_0-e_2` of `H`.  For `x=(X,Y,Z)`, condition (22)
is exactly the existence of `lambda,mu in K` such that

```text
(Y-X,Z,-Z)=lambda(r,s,t),
(Y,Z-X,-Y)=mu(r,s,t).                                (25)
```

If `lambda=mu=0`, then `x=0`.  If `lambda=0` and `mu!=0`, equations (25)
give the first line in (24).  If `mu=0` and `lambda!=0`, they give the
second.  If both are nonzero, they first give

```text
r=s=-t,
```

and then `2(lambda-mu)r=0`.  Characteristic zero and `f!=0` give
`lambda=mu`, hence the third line.  These cases are exhaustive and direct
substitution proves their converses. `square`

### Theorem 6 (rank-four off-diagonal full swallow is empty)

Implication (1) holds pointwise.

#### Proof

If either residual shore has rank one, Lemma 2 contradicts full swallow.
In the remaining rank-two/rank-two case, Lemmas 3--5 put every port image
`X_u(V_u)` in one common line `L_f` (or make all of them zero), and (19)
puts every `Y_u(V_u)` in `cL_f`.  Therefore all components (4)--(5) satisfy

```text
B subset sym(H,L_f)+K sym(L_f,L_f).                  (26)
```

The first summand has dimension at most two and the second at most one, so
`rank B<=3`.  This contradicts (7), completing every residual-shore case.
`square`

## 5. Hostile boundary: unrestricted compatible-kernel containment is false

The proof does not claim that each compatible port--port tensor lies in the
span of the residual-star tensors.  That tempting statement is false over
`Q`.  Take identical residual pairs

```text
a_0=a_1=(1,0,-1),       b_0=b_1=(-1,0,-1),
q=[[-2,0,-2],[0,0,0],[2,0,2]],                      (27)
```

and the port pair

```text
x=(0,0,1),              y=(0,0,1).                  (28)
```

Both residual--port tensors and `sym(x,y)=2E_22` lie in
`Delta+Kq`, but `2E_22` is outside the two-dimensional residual-star span.
Assigning (28) to two distinct promoted labels makes this a legal
distinct-label port--port component, not a forbidden self-label pairing.

Exact elimination writes every compatible port shore as

```text
x=(-A-B+C,0,A),             y=(B,0,C).
```

Thus every compatible left and right shore in this fibre avoids colour `1`,
so the complete labelled span is contained in

```text
span{E_00,E_22,q},                                  (29)
```

of dimension three.  It cannot contain `r_1` and therefore cannot satisfy
full swallow.  Equations (27)--(29) are a no-go for the discarded shortcut,
not a witness, graph, or counterexample to Theorem 6 or to Krenn--Gu.

## 6. Frontier and unresolved remainder

```text
rank-four q-outside-Delta full-swallow fibre:          EMPTY;
rank-four q-in-Delta full-swallow fibre:               OPEN;
rank-five through rank-nine full-swallow fibres:       OPEN;
raw escape supplies an original legal target:          OPEN;
pure-core survival / response / synchronization:       OPEN;
selected activity / nuisance survival / anchors:       OPEN;
named downstream receiver and arbitrary-r cover:       OPEN;
strategic-node closure:                                OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

The smallest remaining rank-four full-swallow obligation is now the
`q in Delta` branch.  In `GLS40` it carries one excess row rather than zero;
on `D(p)`, `GLS41` still requires pointwise survival from the complete
pure-core intersection and all physical attachment gates.  Higher-rank,
silent `p=0`, raw-escape, and source-cover obligations remain separate.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_off_diagonal_root_deck_complete_exclusion.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_off_diagonal_root_deck_complete_exclusion.py
```

The primary uses exact SymPy matrices to replay the terminal compatibility
ideal, all exceptional lines, diagonal covariance, and the divisor boundary
(27)--(29).  The audit imports no project module or third-party package; it
uses independent rational elimination, direct polynomial determinants, and
a separate support-quotient representation.  The arbitrary-domain theorem
is the written proof above, not a finite search.
