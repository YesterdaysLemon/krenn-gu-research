# Maximum-root surplus-two zero-anchor all-rigid kernel contraction and cross-product reduction

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS58`, an exact characteristic-zero root-order-three
reduction of the all-six-rigid zero-anchor branch.  Fix an actual hypothetical
Krenn--Gu witness in one `GLS4`-eligible promoted `GLS8` chart with

```text
r=3,       A={a_0,a_1},
Bhat=Q disjoint-union Uhat,       |Bhat|=6,
omega=W_(a_0,a_1)=0.                                      (1)
```

For `t in Bhat`, put

```text
X_t=W_(a_0,t),       Y_t=W_(a_1,t),
J_t=(X_t,Y_t),       K_t=ker J_t.                         (2)
```

Assume all six labels are torus-rigid in the sense of `GLS55`.  Call a label
**deficient** when `rank J_t<3`.  Then the number of deficient labels gives an
exhaustive structural fork.

1. For every deficient `n`, every nonzero `k in K_n`, and every colour in
   `supp(k)`, the complete equation forces a distinct coordinate-pure
   neighbour.  On `K_n`, one neighbour per active coordinate can be chosen
   uniformly, and all chosen shores activate at one boundary-kernel point.
2. Contracting one deficient label gives an exact seven-slot identity with
   ten physical trilinear decks.  Each nonzero target colour forces at least
   one same-coordinate companion/deck product.
3. Contracting any two deficient labels gives the matching tensor of one
   honest six-vertex graph on the old probes and the other four auxiliary
   labels.  Its target weights are the coordinatewise products of the two
   kernel vectors.  Rigidity makes this target zero, monocolour, or binary,
   so the accepted three-colour six-vertex theorem does not exclude it.
4. Independently of the rank profile, contracting every auxiliary label
   against the cross product of its two evaluated probe rows gives one
   denominator-free polynomial identity.  If there is no deficient label,
   all six `J_t` are injective and the identity has an exact termwise
   coordinate-cover versus genuine-cancellation fork.  On the separate
   transverse all-rank-two profile, it forces the six kernel zero sets
   collectively to cover all three colours.

Thus, writing `d` for the number of deficient labels, `d=0` enters the
all-injective fork, `d=1` enters the one-kernel boundary and ten-deck results,
and `d>=2` also enters the two-kernel descent.  The cross-product identity is
valid on all three cases; its all-rank-two consequence is a separate
specialization inside `d=6`.

This is an exhaustive **rank-profile reduction**, not an exclusion of the
all-rigid branch.  It supplies no promoted response, complete-nuisance
survival, constant selector, synchronization, `GLD3` activity, alternative
receiver, arbitrary-root extension, strategic-node closure, or global
resolution.

## Dependencies and provenance

The proof uses exactly these committed interfaces.

- `GLS8` supplies the complete uncontracted two-probe matching identity and
  the physical companion/deck typing.
- `GLS55` supplies the torus-rigidity criterion and the exact rank-zero
  through rank-three kernel classification.
- `GLS56` supplies the covector alternative and the matching-kill template
  on a fully supported kernel point.  Theorem 1 below is the new boundary-
  kernel extension: it applies only to the nonzero coordinates of an
  arbitrary kernel vector.
- `GLS57` is status context for the stronger all-rank-one subbranch.  It is
  not a proof dependency.
- The accepted computer-assisted
  [`six-vertex theorem`](../finite/n06/SIX_VERTEX_CERTIFICATE.md) excludes
  complex six-vertex solutions with at least three nonzero target colours.
  Its hypothesis is deliberately *not* met on the rigid double-contraction
  branch.
- [`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`](THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md)
  is the historical unrestricted coordinate-killer antecedent.  It does not
  prove the fixed boundary-kernel shores, physical ten-deck identity, or
  double-kernel graph reconstruction established here.

No logical dependence is inferred from filenames.

## 1. Boundary-kernel pure neighbours

For distinct auxiliary labels `n,t`, define

```text
L_(nt):K_n -> V_t^*,       L_(nt)(k)=W_(n,t)(k,-).     (3)
```

### Theorem 1 (arbitrary boundary-kernel pure-neighbour escape)

Let `0!=k in K_n`, and let `c` be any colour with `k_c!=0`.  There is a
label `t_c!=n` such that

```text
0!=L_(n t_c)(k) in K e_(t_c,c)^*.                     (4)
```

Neighbours supplied for distinct colours in `supp(k)` are distinct.

### Proof

Suppose (4) fails for a fixed supported colour `c`.  For every
`t in Bhat-{n}`, apply the `GLS56` covector alternative to

```text
ell_t=L_(nt)(k).
```

Because `ell_t` is not a nonzero multiple of `e_(t,c)^*`, choose
`k_t in ker ell_t` with `(k_t)_c!=0`.

Evaluate the complete `GLS8` identity at `k` in slot `n` and at `k_t` in
every other auxiliary slot, leaving the two probes open.  A companion term
whose pair contains `n` vanishes because `J_n(k)=0`.  If its pair does not
contain `n`, the complementary physical deck contains `n`; every perfect
matching in that deck pairs `n` to some `t`, and its edge evaluates to
`ell_t(k_t)=0`.  The same matching argument kills the top deck, independently
of the value of `omega`.

The evaluated source is therefore zero.  The coefficient of the pure probe
word of colour `c` on the target is

```text
k_c product_(t in Bhat-{n}) (k_t)_c !=0,              (5)
```

a contradiction.  A nonzero covector cannot lie on two distinct coordinate
axes, so the neighbours for distinct supported colours are distinct.
`square`

The restriction `c in supp(k)` is load-bearing.  The theorem makes no claim
at a coordinate already zero on the chosen boundary vector.

Put

```text
S_n={c:e_(n,c)^*|_(K_n) is not zero}.                 (6)
```

### Theorem 2 (fixed boundary shores and simultaneous activation)

For each `c in S_n`, there is one fixed label `t_c!=n` satisfying

```text
0!=L_(n t_c)(K_n) subset K e_(t_c,c)^*.               (7)
```

The `t_c` are distinct.  There is one `k in K_n` with

```text
supp(k)=S_n,
L_(n t_c)(k)!=0              for every c in S_n.      (8)
```

### Proof

Fix `c in S_n`.  The nonempty open `K_n cap D(k_c)` is covered pointwise by
the finitely many sets

```text
{k:L_(nt)(k) in K^* e_(t,c)^*},       t!=n,           (9)
```

by Theorem 1.  Discard every label for which the displayed set is empty.  Each
remaining set is contained in the linear subspace

```text
P_(t,c)={k in K_n:L_(nt)(k) in K e_(t,c)^*}.          (10)
```

An irreducible linear space cannot have a nonempty open covered by finitely
many proper linear subspaces.  Hence some `P_(t_c,c)=K_n`.  The corresponding
displayed set was retained only if nonempty, so `L_(n t_c)|_(K_n)` is nonzero;
the equality `P_(t_c,c)=K_n` puts its entire image on the `c`-axis.
Distinctness follows because two coordinate axes intersect only at zero.

For each `c in S_n`, both `ker(e_c^*|_(K_n))` and
`ker(L_(n t_c)|_(K_n))` are proper subspaces.  Avoid their finite union.
The resulting vector has (8); colours outside `S_n` vanish identically on
`K_n`.  `square`

### Corollary 3 (rigid deficient rank profiles)

On the all-rigid branch:

- if `rank J_n=1`, then `K_n` is one coordinate plane.  The other two
  colours form `S_n`, and two distinct fixed pure neighbours activate at one
  support-two kernel vector;
- if `rank J_n=2`, then `K_n=Kk` for one vector with support one or two.
  Exactly those supported colours have distinct fixed pure neighbours, and
  every nonzero restricted shore is active at every nonzero kernel point;
- if `rank J_n=3`, then `K_n=0` and Theorems 1--2 are silent.

For rank two, if `supp(k)={c,d}`, the column relation

```text
k_c J_n(e_c)+k_d J_n(e_d)=0                          (11)
```

is denominator-free; the two displayed columns are nonzero and span a line,
while the third column is independent.  If `supp(k)={c}`, the `c` column is
zero and the other two are independent.

### Corollary 4 (probe-row alignment or rank raise)

For a forced shore `L_(nt)(k)=lambda e_(t,c)^*`, exactly one of the following
holds:

1. `e_(t,c)^* in row J_t`, so the shore factors through the joint probe map;
2. `e_(t,c)^* notin row J_t`, in which case

   ```text
   rank(J_t,e_(t,c)^*)=rank J_t+1,
   ker(J_t,e_(t,c)^*)=K_t cap ker e_(t,c)^*.          (12)
   ```

Equivalently in the second case there is `ell in K_t` with `ell_c!=0` and

```text
W_(n,t)(k,ell)!=0.                                    (13)
```

This is ordinary annihilator duality.  It is a local probe-row statement,
not complete-nuisance absorption or projective synchronization.

## 2. One-kernel ten-deck identity

The complete zero-anchor `GLS8` identity is

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D).   (14)
```

Here and below

```text
E_(A,c)=e_(a_0,c)^* tensor e_(a_1,c)^*,
```

and `G_D^A` is the physical companion tensor on the slots `A union D`.

Fix a deficient `n`, a nonzero `k in K_n`, and put `R=Bhat-{n}`.  For every
pair `D subset R`, define the physical trilinear deck

```text
E_D^(n,k)=H_(Bhat-D)(k,-_(R-D)).                      (15)
```

### Theorem 5 (seven-slot ten-deck contraction)

The following exact tensor identity holds:

```text
sum_(D in binom(R,2)) G_D^A tensor E_D^(n,k)
 =sum_(c=0)^2 k_c E_(A,c)
                  tensor tensor_(t in R)e_(t,c)^*.    (16)
```

There are exactly ten terms.  Each deck has the three-term physical expansion

```text
E_D^(n,k)
 =sum_(t in R-D) L_(nt)(k) tensor W_((R-D)-{t}),      (17)
```

with canonical slot order.

### Proof

Contract (14) at `k` in slot `n`.  Every pair term containing `n` has zero
companion because `J_n(k)=0`.  The other ten pairs are exactly
`binom(R,2)`, and their physical complements give (15).  Contracting the
target gives the right side of (16).  Equation (17) is the partition of the
three perfect matchings on the four deck vertices according to the neighbour
paired with `n`.  No division, response, or nonzero deck assumption occurs.
`square`

For each `c in supp(k)`, evaluate all five `R` slots of (16) at colour `c`.
The result is the nonzero probe tensor `k_c E_(A,c)`.  Hence at least one
pair `D` has simultaneously

```text
G_D^A(-_A,tensor_(u in D)e_(u,c))!=0,
E_D^(n,k)(tensor_(t in R-D)e_(t,c))!=0.               (18)
```

This is a same-coordinate companion/deck product.  It need not be a promoted
target, a full pure companion, a response, or a nuisance-surviving row.

## 3. Two-kernel legal six-vertex descent

Choose distinct deficient labels `n,m`, nonzero vectors

```text
k in K_n,       ell in K_m,       P=Bhat-{n,m}.       (19)
```

For `u in P`, put

```text
h=W_(n,m)(k,ell),
a_u=W_(n,u)(k,-),       b_u=W_(m,u)(ell,-),           (20)
```

and for distinct `u,v in P` define

```text
D_uv=h W_uv+a_u tensor b_v+b_u tensor a_v.           (21)
```

### Theorem 6 (two-deficient six-vertex reconstruction)

Let `B'` be the graph on the six open vertices `A union P` with edge blocks

```text
B'_(a_0,a_1)=0,
B'_(a_0,u)=X_u,       B'_(a_1,u)=Y_u,
B'_(u,v)=D_uv.                                          (22)
```

Then contraction of the original physical matching tensor is exactly the
matching tensor of this honest six-vertex graph:

```text
T_W(k at n,ell at m,-_(A union P))=T_(B').            (23)
```

On the hypothetical witness its target is

```text
sum_(c=0)^2 k_c ell_c
       tensor_(v in A union P)e_(v,c)^*.              (24)
```

Equations (21)--(24) are polynomial and remain valid at `h=0`.

### Proof

Partition original perfect matchings after inserting `k,ell`.

- A matching using `n--m` contributes `h`.  Since the old probe edge is zero,
  the remaining six-vertex matching has exactly one `P--P` edge `u--v`; this
  gives the branch `hW_uv` of (21).
- Otherwise `n` and `m` meet two distinct vertices `u,v in P`.  The two
  orientations contribute `a_u tensor b_v` and `b_u tensor a_v`.  The two
  probes match the other two vertices of `P`.

Conversely, every nonzero matching of (22) contains exactly one `P--P` edge,
and expanding that edge through the three terms in (21) reconstructs exactly
one of these original cases.  Thus the matching terms are in bijection.  The
target contraction is (24).  `square`

The exact matching census is

```text
105 original matchings
 =15 zero-anchor matchings
  +54 joint-kernel-killed companion matchings
  +36 matching slots not forced to zero by the joint kernels,

36=12 formal six-vertex matchings avoiding the zero root edge
      * 3 formal branches of D_uv.                         (25)
```

Individual edge tensors or individual `h`, `a tensor b`, and `b tensor a`
branches may still vanish; (25) is a formal matching-slot census.

### Corollary 7 (rigid zero/mono/binary target classification)

For rigid deficient `n,m`, every nonzero kernel vector has a zero coordinate.
The nonzero target-colour set in (24) is exactly

```text
supp(k) intersect supp(ell),                           (26)
```

which has size zero, one, or two, never three.  Binary output occurs exactly
when both vectors have the same two-element support.

The accepted six-vertex theorem excludes only the case of at least three
nonzero target colours.  It therefore cannot contradict any rigid pair via
(23).  The same contraction would contradict two fully supported kernel
vectors: the finitely many coefficients of a characteristic-zero witness
generate a finitely generated field over `Q`, which embeds in `C`, so the
complex six-vertex exclusion applies after scalar extension.  This is
consistent with the `GLS55` conclusion that at most one label is nonrigid at
`r=3`.

## 4. Cross-product identity and the injective fork

Fix arbitrary probe vectors `z_0,z_1`.  At auxiliary label `t`, put

```text
p_t=X_t(z_0,-),       q_t=Y_t(z_1,-),
k_t=p_t cross q_t.                                      (27)
```

The cross product uses the fixed target coordinate volume form:

```text
(k_t)_0=p_(t,1)q_(t,2)-p_(t,2)q_(t,1),
(k_t)_1=p_(t,2)q_(t,0)-p_(t,0)q_(t,2),
(k_t)_2=p_(t,0)q_(t,1)-p_(t,1)q_(t,0).               (28)
```

Thus `p_t(k_t)=q_t(k_t)=0` identically.

### Theorem 8 (global cross-product polynomial identity)

Every zero-anchor complete witness obeys

```text
F(z_0,z_1)
 =sum_(c=0)^2 z_(0,c)z_(1,c)
                 product_(t in Bhat) (k_t)_c
 =0                                                        (29)
```

as a polynomial identity, including every rank and cross-product divisor.

### Proof

Contract the two probes at `z_0,z_1` and every auxiliary label at its
polynomial vector `k_t`.  For a companion pair `{s,t}`, its two summands are

```text
p_s(k_s)q_t(k_t)+q_s(k_s)p_t(k_t)=0.                  (30)
```

The zero anchor removes the top term.  Evaluating the pure target gives
exactly (29).  No cross product or rank minor is divided out.  `square`

Let `R_t^X=row X_t`, `R_t^Y=row Y_t`, and let `pi_c` delete coordinate `c`.

### Lemma 9 (injective cross-product visibility)

If `J_t` is injective, then:

1. `k_t` is the zero polynomial exactly on the two pure-probe axes

   ```text
   (R_t^X,R_t^Y)=(0,V_t^*) or (V_t^*,0);              (31)
   ```

2. its coordinate `(k_t)_c` is the zero polynomial exactly when

   ```text
   R_t^X subset K e_c^* and pi_c(R_t^Y)=K^2,
   or
   R_t^Y subset K e_c^* and pi_c(R_t^X)=K^2.          (32)
   ```

### Proof

All cross products between `R_t^X` and `R_t^Y` vanish exactly when one space is
zero or both nonzero spaces are one common line.  Injectivity says
`R_t^X+R_t^Y=V_t^*`, excluding the common-line case and forcing the nonzero
space to be all of `V_t^*`.  This proves (31).

Coordinate `c` of a cross product is the two-dimensional determinant of the
projections `pi_c(R_t^X),pi_c(R_t^Y)`.  It vanishes for every pair exactly
when one projection is zero or both nonzero projections are one common line.
The common-line alternative puts `R_t^X+R_t^Y` in the two-space spanned by
that line and `e_c^*`, contradicting injectivity.  The other projection must
therefore be all of `K^2`, proving (32).  `square`

### Corollary 10 (all-injective coordinate-cover/cancellation fork)

Assume all six `J_t` are injective and put

```text
P_c=product_(t in Bhat)(k_t)_c.                       (33)
```

Exactly one of the following holds.

1. `P_0=P_1=P_2=0`.  For every colour `c`, at least one label has the
   coordinate-axis/complementary-surjective shore pattern (32).
2. At least two `P_c` are nonzero, and (29) is a genuine polynomial
   cancellation among their summands.

Indeed, the polynomial ring is a domain; a product is zero exactly when one
factor is zero, and one lone nonzero summand cannot equal zero.  This is an
exact fork, but neither leaf is excluded.

### Corollary 11 (transverse all-rank-two kernel cover)

Suppose all six `J_t` have rank two and both `X_t,Y_t` are nonzero.  Choose a
generator `v_t` of `K_t`.  Then

```text
k_t=Delta_t(z_0,z_1) v_t                              (34)
```

for a nonzero polynomial `Delta_t`.  Consequently

```text
product_(t in Bhat) (v_t)_c=0       for c=0,1,2.      (35)
```

Thus the coordinate-zero sets of the six projective kernel lines cover all
three colours.

To prove this, `p_t,q_t` lie in `v_t^perp`, so their cross product has the
form (34).  Rank two plus both probe blocks nonzero makes their row spaces
contain an independent pair, hence `Delta_t` is not the zero polynomial.
Substitute (34) into (29), cancel the nonzero product of the `Delta_t` in the
polynomial domain, and compare the three distinct monomials
`z_(0,c)z_(1,c)`.  If one probe block is zero, that label remains a separate
pure-probe boundary and no cancellation is licensed.

## 5. Sharp controls and no-go boundaries

### 5.1 Binary sharpness already at `h=0`

Let two deficient labels have the rigid rank-two kernel

```text
k=ell=(1,1,0),                                        (36)
```

and take `h=0`.  On retained ports `0,1,2,3`, choose

```text
a_0=e_(0,1)^*,       a_2=e_(2,0)^*,
b_1=e_(1,1)^*,       b_3=e_(3,0)^*,                   (37)
```

with all other `a,b` zero.  Formula (21) gives

```text
D_01=E_11,       D_23=E_00,
D_03=e_(0,1)^* tensor e_(3,0)^*,
D_12=e_(1,1)^* tensor e_(2,0)^*,                     (38)
```

and the other port blocks zero.  Take the only probe--port blocks to be

```text
a_0--0:E_00,       a_1--1:E_00,
a_1--2:E_11,       a_0--3:E_11.                      (39)
```

All four retained ports are rank-one rigid.  For an explicit full
eight-vertex lift, at each deficient label take

```text
X_n=X_m=[[1,-1,0],[0,0,1],[0,0,0]],
Y_n=Y_m=0,                                           (40a)
```

so the joint row space is `span{e_0^*-e_1^*,e_2^*}` with kernel
`K(1,1,0)`.  Set

```text
W_(n,0)=E_(0,1),    W_(n,2)=E_(0,0),
W_(m,1)=E_(0,1),    W_(m,3)=E_(0,0),                (40b)
```

and set `W_(n,m)` and all raw retained-port edges to zero.  Keep the
probe--port blocks (39).  Contracting `n,m` at `(1,1,0)` reconstructs
(37)--(38) coefficientwise.  Thus all six auxiliary labels in this full lift
are rigid: the deficient labels have rank two and the retained labels have
rank one.

The effective six-vertex graph has exactly two nonzero words: the all-zero
and all-one words, both with coefficient one.  The two mixed blocks in (38)
have no compatible probe completion.  This is an exact all-six-rigid,
`h=0` contraction control for the binary endpoint.  It is not a complete
eight-vertex witness.

### 5.2 Termwise injective cross-product control

Let

```text
P=[[0,0,1],[1,0,0],[0,1,0]].                         (41)
```

On labels `(q_0,q_1,u_0,u_1,u_2,u_3)`, take `X_t=P`, adding respectively
`E_00,E_11,0,E_22,0,0`, and take the rank-one `Y_t` cells

```text
E_22,E_01,E_00,E_02,E_11,E_01.                       (42)
```

Every `X_t` is invertible, so all six `J_t` are injective and both probe maps
are nonzero.  Nevertheless

```text
(k_(q_0))_2=0,       (k_(u_0))_0=0,
(k_(u_2))_1=0,                                      (43)
```

while no whole `k_t` vanishes.  Hence all three products `P_c` vanish
termwise.

This local data has an exact physical same-graph control.  Keep the zero
anchor and add only the internal cells

```text
q_1--u_3:E_00+E_22,       u_1--u_2:E_00,
q_0--u_3:E_11,            u_0--u_1:E_11,
u_0--u_2:E_22.                                      (44)
```

Its eight-vertex matching tensor has pure coefficients `(1,1,1)` and `64`
supported words, of which `61` are mixed; there are `66` nonzero coloured
matching terms.  Thus injectivity, both-probe activity, all three required
pure coefficients, and termwise (29) can coexist off the mixed target locus.
The control has `H_Q=0`, is not `GLS4`-eligible, and is not a witness.

### 5.3 Load-bearing limitations

1. Theorem 1 supplies neighbours only for `c in supp(k)`.
2. Full **joint** kernels are essential.  Killing one chosen probe row does
   not kill companions through the other probe.
3. The zero anchor is essential for (16), (23), and (29).  At nonzero anchor,
   the contracted top deck remains.
4. A pure neighbour shore is not a physical promoted response, selector,
   nuisance-free quotient class, or synchronized receiver row.
5. A nonzero pure summand in (17) can cancel with the other two deck terms.
   No individual trilinear deck is forced to be pure or target-attached.
6. The graph in Theorem 6 is legal and physical, but its rigid target has at
   most two colours.  The accepted finite theorem has no binary conclusion.
7. Identity (29) is necessary, not sufficient.  The exact control
   (41)--(44) lies on its termwise-zero leaf while failing mixed coefficients.
8. The all-rank-one branch has the stronger `GLS57` conclusions; none of its
   `2+2+2` pairing or response supply is inferred for mixed ranks.
9. Root order is fixed at three.  The double contraction leaves six vertices
   only because `|Bhat|=6`.

## 6. Exact frontier

```text
arbitrary boundary-kernel supported-colour pure neighbour: PROVED;
fixed boundary shore and simultaneous activation:          PROVED;
rigid rank-one/rank-two support consequences:               PROVED;
one-deficient seven-slot ten-deck identity:                 PROVED;
supported-colour same-coordinate companion/deck product:    PROVED;
two-deficient honest six-vertex reconstruction:             PROVED;
rigid double-contraction target has at most two colours:     PROVED;
binary endpoint excluded by accepted n=6 theorem:           FALSE;
global cross-product polynomial identity:                   PROVED;
all-injective coordinate-cover/cancellation fork:           PROVED;
transverse all-rank-two kernel zero-set cover:               PROVED;
all-rigid higher-rank branch excluded:                       OPEN / NOT CLAIMED;
promoted response and complete-nuisance selector:            OPEN;
synchronization, activity, anchor, and named receiver:       OPEN;
unique-nonrigid low-activity branch:                         OPEN;
arbitrary-root and nonzero-anchor coverage:                  OPEN;
maximum-root strategic-node closure:                         OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.
```

The smallest successor is to couple the zero/mono/binary descents and the
injective coordinate-cover/cancellation fork across multiple kernel choices
using additional complete mixed equations.  Reapplying the three-colour
six-vertex theorem or treating (29) as sufficient cannot close the branch.

## Verification

Run from repository root:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_all_rigid_kernel_contraction_and_cross_product_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_all_rigid_kernel_contraction_and_cross_product_reduction.py
```

The primary verifier uses exact rational dense edge blocks to compare all
`3^7=2187` coefficients of the one-kernel contraction and all `3^6=729`
coefficients of the two-kernel reconstruction.  It also checks the finite
covector alternative, an explicit full eight-vertex lift of the exact `h=0`
all-rigid binary endpoint, symbolic cross-product annihilation, and the
physical injective control.

The independent no-project-import audit uses an `F_5` covector/subspace
census, bit-mask perfect matchings, a reverse `105=15+30+60` and
`105=15+54+36` matching classification, independent one- and two-kernel
monomial-level descent bijections, independent sparse replays of both
physical controls, a direct all-rank-two cross-product-factor audit, and
bilinear coefficient tables.  The written proof, not either bounded replay,
carries the characteristic-zero complete-witness result.
