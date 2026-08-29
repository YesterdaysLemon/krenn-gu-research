# Maximum-root surplus-two zero-anchor six-deficient multi-`T_0` Family-A proper-face repair and source-integrability boundary

## Status

This is theorem package **GLS78**.  It is the serious parent-theorem attempt
for the two remaining single-binary Family-A keys

```text
r=2:  S_0 R_2 R_1 R_0 T_0^2,       1,080 / 1 key,
r=3:  S_0 R_2 R_1 T_0^3,              360 / 1 key.
```

The result is a proved **boundary**, not a key exclusion.  It reconstructs
the exact proper-face restriction maps, identifies their common invisible
subspace and a nonzero physical hafnian direction in it, and enumerates the
repair channels that survive every partial `T_0` kernel contraction.  Exact
characteristic-zero controls satisfy all three kernel selector equations,
both nonzero pure attachments, and, on the one-silent `r=2` chart, the extra
outer-product relation suggested by `GLS77`.

Consequently the `GLS77` kernel/rank mechanism does not transfer to either
remaining key.  A successor must retain an off-kernel coordinate at an
active `T_0` port and synchronize the resulting complete-source repair
channels.  Both keys remain **OPEN**, the live six-deficient residual stays

```text
97,215 / 79,
```

and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 0. Dependencies and normalization

Work over the characteristic-zero fraction field of `GLS61`--`GLS77`.
Use the `GLS70` Family-A taxonomy and the `GLS71` crossed normalization

```text
p_0=P_1 e_(0,1),       q_0=Q_2 e_(0,2),
p_1=P_2 e_(1,2),       q_1=0,
p_2=0,                 q_2=Q_1 e_(2,1).             (1)
```

Thus the central triangle has the two pure pair faces and the unique binary
target described by

```text
D_0={3,4,5},       D_1={0,2},       D_2={0,1}.       (2)
```

Put `O={3,4,5}`.  At an `R_0` outside port,

```text
J_u=F e_(u,0)^*,       K_u=F e_(u,1) direct-sum F e_(u,2). (3)
```

At a `T_0` outside port, normalize

```text
h_u=e_(u,1)^*+kappa_u e_(u,2)^*,
J_u=F e_(u,0)^* direct-sum F h_u,
K_u=F(kappa_u e_(u,1)-e_(u,2)),       kappa_u!=0.    (4)
```

Every probe-source row at `u` lies in `J_u=Ann(K_u)`.  The target factors

```text
x_u=e_(u,1)^*|_(K_u),       y_u=e_(u,2)^*|_(K_u)    (5)
```

are independent at an `R_0` port and nonzero proportional forms at a `T_0`
port.  This synchronization is the essential difference from `GLS77`.

## 1. Exact two-key parent chart

### Proposition 1.1

The remaining Family-A single-binary charts are exactly

```text
r=2:  S_0 R_2 R_1 R_0 T_0 T_0,       1,080 profiles,
r=3:  S_0 R_2 R_1 T_0 T_0 T_0,         360 profiles. (6)
```

Up to the outside permutation action, put the `R_0` port of the first chart
at `3`.  Then

```text
r=2:  dim K=(2,1,1),       dim J=(1,2,2),
r=3:  dim K=(1,1,1),       dim J=(2,2,2).            (7)
```

### Proof

This is the `GLS70` exhaustive Family-A word

```text
S_0 R_2 R_1 R_0^(3-r) T_0^r
```

at `r=2,3`.  The sizes are `360 binom(3,r)`, giving (6), and (3)--(4)
give (7). `square`

## 2. The exact proper-face blind spot

Write `E_u=V_u^*` and let

```text
r_u:E_u -> K_u^*                                      (8)
```

be restriction.  On `E_3 tensor E_4 tensor E_5`, let `R_u` apply `r_u` in
slot `u` and the identity in the other two slots.

### Theorem 2.1 (intersection of all single-slot kernels)

```text
intersection_(u=3)^5 ker R_u = J_3 tensor J_4 tensor J_5. (9)
```

Its dimension is `4` for `r=2` and `8` for `r=3`.  By contrast, the kernel
of the simultaneous tensor-product quotient

```text
r_3 tensor r_4 tensor r_5                              (10)
```

has dimension `25` for `r=2` and `26` for `r=3`.

### Proof

Choose a complement `E_u=J_u direct-sum L_u`.  A basis tensor lies in
`ker R_u` exactly when its `u`-factor lies in `J_u`.  Membership in all
three kernels therefore means that all three factors lie in their `J`
spaces, proving (9).  The product dimensions in (7) give `4,8`.

The quotient (10) has image dimension

```text
product_u dim K_u = 2 for r=2,       1 for r=3,
```

inside a `27`-dimensional domain, giving `25,26`.  Its kernel is the sum of
the three subspaces having at least one `J_u` factor; it is not (9).
`square`

### Proposition 2.2 (nonzero physical intersection)

The common invisible subspace in (9) meets the physical hafnian family
nontrivially.  Choose nonzero `j_u in J_u`, a nonzero `a_2 in E_2`, and set

```text
W_23=a_2 tensor j_3,       W_45=j_4 tensor j_5,
W_24=W_25=W_34=W_35=0.                                  (11)
```

Then the actual physical four-deck is

```text
H_2345=a_2 tensor j_3 tensor j_4 tensor j_5!=0.          (12)
```

Every `R_u` kills (12).  This exhibits one physical direction; it does not
assert that the entire `E_2 tensor J_3 tensor J_4 tensor J_5` subspace is
physically realizable.

### Proof

The four-vertex hafnian is

```text
H_2345=W_23 W_45+W_24 W_35+W_25 W_34.
```

Substitution of (11) gives (12), and `j_u|_(K_u)=0` kills it in each named
outside slot.  Formally, `(id_(E_2) tensor R_u)(H_2345)=0`; equivalently,
the outside factor of (12) lies in `J_3 tensor J_4 tensor J_5`. `square`

## 3. Kernel selectors, attachments, and exact controls

On the outside kernels put

```text
A=W_12,
Y_i=W_1i|_(K_i),       Z_i=W_2i|_(K_i),
B_ij=W_ij|_(K_i tensor K_j).                           (13)
```

The three selector tensors and the two pure attachments are

```text
E_ij=A B_ij+Y_i Z_j+Y_j Z_i,                          (14)

sum_i Y_i B_(O-{i})=lambda e_(1,1) x_3x_4x_5,
sum_i Z_i B_(O-{i})=mu e_(2,2) y_3y_4y_5,
lambda mu!=0.                                         (15)
```

The following controls satisfy the stronger system in which **all three**
equations (14) vanish, whether or not activity exposes all three.

### Theorem 3.1 (`r=2` all-selector control)

Let `x,y` be the independent basis of `K_3^*`, and let `z_4,z_5` generate
the two `T_0` kernel duals.  Set the relevant component of
`A=e_(1,1)e_(2,2)` equal to one and take

```text
Y_3=e_(1,1)x,       Z_3=e_(2,2)y,
Y_4=e_(1,1)z_4,     Z_4=0,
Y_5=0,              Z_5=e_(2,2)z_5,

B_45=-z_4z_5,       B_35=-xz_5,       B_34=-yz_4.    (16)
```

Then

```text
E_45=E_35=E_34=0,
H_(1O)=-2 e_(1,1)xz_4z_5,
H_(2O)=-2 e_(2,2)yz_4z_5.                            (17)
```

### Theorem 3.2 (`r=3` all-selector control)

Let `z_3,z_4,z_5` generate the three kernel duals.  Again take the relevant
component of `A` to be one and put

```text
Y_i=e_(1,1)z_i                    for i=3,4,5,
Z_3=0,       Z_4=e_(2,2)z_4,      Z_5=e_(2,2)z_5,

B_45=-2z_4z_5,       B_35=-z_3z_5,       B_34=-z_3z_4. (18)
```

Then

```text
E_45=E_35=E_34=0,
H_(1O)=-4 e_(1,1)z_3z_4z_5,
H_(2O)=-2 e_(2,2)z_3z_4z_5.                          (19)
```

### Proof of Theorems 3.1--3.2

Substitute (16) or (18) in (14)--(15).  Each selector cancels term by term
and the two attachment sums have the displayed nonzero values. `square`

Each edgewise restriction map used in (13) is surjective, so the displayed
restricted values lift simultaneously, edge by edge, to a common physical
edge array.  They are not complete six-label sources or Krenn--Gu
counterexamples.

## 4. The one-silent outer-product relation is still compatible

Consider the conditional `r=2` cell with silent `T_0` port `5`, active
`R_0` port `3`, and active `T_0` port `4`.  After absorbing the common
one-dimensional factors at ports `4,5`, write

```text
r=u_3,       m=u_4,       s=v_3,       p=v_4,
b=u_5,       c=v_5,       alpha=[e_(1,1)e_(2,2)]A.   (20)
```

Here `r,s,B_35,B_34 in K_3^*` and `m,p,b,c,B_45` are scalars.  The two
exposed selectors and attachments are

```text
alpha B_45+mc+bp=0,
alpha B_35+rc+bs=0,                                  (21)

rB_45+mB_35+bB_34=lambda x_3,
sB_45+pB_35+cB_34=mu y_3.                            (22)
```

Even adjoining the `GLS77`-shaped relation

```text
C=rp+sm=0                                             (23)
```

does not contradict (21)--(22).

### Proposition 4.1 (exact `C=0` control)

Set

```text
alpha=m=p=b=c=1,
r=(mu y_3-lambda x_3)/4,       s=-r,
B_45=-2,       B_35=0,
B_34=(lambda x_3+mu y_3)/2.                           (24)
```

Then (21)--(23) hold for arbitrary nonzero `lambda,mu` and independent
`x_3,y_3`.

### Proof

The two left sides in (21) are `-2+1+1` and `r+s`.  Relation (23) is
`r+s`.  The attachment sides are

```text
-2r+B_34=lambda x_3,
 2r+B_34=mu y_3,
```

by (24). `square`

For `r=3`, every quantity in (20)--(23) is scalar after removing the three
kernel generators and `x_i,y_i` are proportional.  The system is therefore
no stronger and supplies no independent outside flattening.

## 5. Why complete off-kernel rows retain repairs

Let `I_6` denote the complete six-open source identity and let `partial_u`
mean contraction of outside slot `u` by a nonzero `k_u in K_u`.  Since every
probe row at `u` lies in `J_u`, `partial_u` structurally removes every source
pair containing `u`; no other source-pair class is removed merely by that
contraction.

For `r=2`, contracting the `T_0` port `4` leaves the ten possible source-pair
classes among

```text
{0,1,2,3,5}.                                         (25)
```

Besides the three central pairs and the three pairs meeting the `R_0` port
`3`, these include the four genuine repairs

```text
g_05,       g_15,       g_25,       g_35.            (26)
```

For example,

```text
g_05=P_1 e_(0,1) tensor q_5+Q_2 e_(0,2) tensor p_5,
g_15=P_2 e_(1,2) tensor q_5,
g_25=Q_1 e_(2,1) tensor p_5,
g_35=p_3 tensor q_5+q_3 tensor p_5.                  (27)
```

Contracting port `5` as well removes (26), but leaves exactly the six pairs
among `{0,1,2,3}`: the three central pairs and three `g_i3` terms.  This is
the already-compatible `r=2` strict parent before quotienting port `3`.

For `r=3`, each single or double `T_0` contraction analogously leaves the
repairs from every uncontracted outside port.  Contracting all three outside
ports leaves only the three central pairs, hence exactly the accepted binary
triangle.  The GHZ target side is contracted at the same time: both target
colours survive, but their outside factors become proportional at each
`T_0` kernel.  Thus the final target is precisely the synchronized binary
central triangle, not a vanished target.  Therefore:

```text
retain an off-kernel T_0 direction  => repair channels survive;
kill every T_0 repair channel       => target colours synchronize and the
                                       equation collapses to a known parent.
                                                               (28)
```

This proves failure of the direct `GLS77` kernel-difference route.  It does
not prove that no different complete-source combination can close the keys.

### Proposition 5.1 (exact active-`T_0` leakage block nonseparation)

Use the complete word order of `GLS77` and let `F_n` be the full coefficient
with zero-based base-three index `n`.  Keep port `5` silent only in its
`P_0,Q_0` rows and retain every `P_1,P_2,Q_1,Q_2` row.  Put

```text
I_2500=[e_(2,0)e_(5,0)]W_25.                         (29)
```

For the `r=2` chart, the active-port-`4` kernel difference between words
`02220020` and `02220010` expands exactly as

```text
F_2112-kappa_4 F_2109
=P_30 [
 Q_520 { I_0122 (I_2402-kappa_4 I_2401)
        +I_0220 (I_1422-kappa_4 I_1421)
        +I_1220 (I_0422-kappa_4 I_0421) }
 +I_1220 (I_4520-kappa_4 I_4510)
 +I_2500 (I_1422-kappa_4 I_1421)
 +I_1520 (I_2402-kappa_4 I_2401) ].                  (30)
```

Thus the desired off-kernel coefficient occurs, but only beside the legal
`Q_520`, `W_15`, and `W_45` repair channels.  For `r=3`, the same formula
has `P_300` in place of `P_30`; the independent port slopes are retained.

Fix `c_2=c_5=0`.  Over `QQ(kappa_4)`, exactly `28` `r=2` three-row
port-`4` blocks have a leakage-bearing kernel difference.  Over
`QQ(kappa_3,kappa_4)`, exactly `78` `r=3` blocks do.  In every one, any
linear row combination over the indicated slope field that cancels all
monomials not containing `I_2500` also cancels every monomial containing it.
The same exact nonseparation
holds in all `81` nine-row `(c_3,c_4)` blocks for each chart; their
nonleak-nullity sums/maxima are `173/7` and `100/5`, respectively.

### Proof

Enumerate the `105` perfect matchings of the eight vertices, retain the
independent `T_0` slopes, and expand the named rows.  Equation (30) follows
term by term.  For each finite block, form the matrix whose columns are its
literal rows and whose rows are the nonleak monomials.  Exact nullspace
calculation over the stated rational function field shows that every vector
in its right nullspace also annihilates the leak-monomial rows.  The retained
verifier reconstructs every expansion and block. `square`

The exhaustive `c_5=0` row spans also have zero leakage-rank increment at
two distinct large-prime, independent-slope specializations.  That is
supporting modular evidence only, not a characteristic-zero theorem.  The
exact block statement is generic over the indicated independent-slope
rational-function field and excludes only linear combinations within each
specified block, with coefficients in that field.  Exceptional slope
specializations, combinations across blocks, nonlinear syzygies, and other
complete-source couplings remain available.

**Successor update.** `GLS79` subsequently decomposes the entire `c_5=0`
row family into exact nonleak-incidence components and proves global linear
nonseparation in characteristic zero.  `GLS80` then restores every outside
source-row coordinate and all `6,558` zero-target colour words and proves the
same nonseparation for the complete universal scalar-linear row span.  Thus
combinations across the blocks named here, rows with `c_5!=0`, and nonzero
slope specializations are no longer open universal linear loopholes.
Source-coordinate specializations, nonlinear syzygies, activity
localization, and other complete-source couplings remain open.

## 6. Exact next obligation

A load-bearing successor must do at least one of the following:

1. retain an off-kernel coordinate at an active `T_0` port and prove that
   the repairs (26)--(27), together with their analogues at the other ports,
   cannot be restrictions of the same physical matching decks;
2. prove a new activity-localization theorem that puts every source in a
   stricter cell where a complete coefficient separates those repairs; or
3. construct an exact complete-source control satisfying every coefficient,
   which would refute the proposed exclusion route and require dedicated
   validation before any conjecture-level interpretation.

The three selector/attachment equations, the relation `C=0`, and any
separation argument that sees physical decks only through the single-slot
maps `R_u` cannot by themselves be the missing lemma: Theorems 2.1,
3.1--3.2, and Proposition 4.1 give the exact blind spot and compatible
controls for those data.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_proper_face_repair_and_source_integrability_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_proper_face_repair_and_source_integrability_boundary.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_active_t_leakage_row_span_boundary.py
```

The primary verifier checks the two key counts, both restriction-kernel
dimensions, the physical hafnian direction, both all-selector controls, the
one-silent `C=0` control, the exact surviving source-pair hierarchy, and the
unchanged residual.  The no-import audit reconstructs those checks through
separate finite-basis and exact rational calculations.  The third verifier
independently expands all `105` matchings, proves the representative leakage
identity and the finite exact block nonseparation over independent slope
fields, and labels its global modular ranks as evidence only.

Neither script proves a complete-source realization, excludes either key,
or resolves Krenn--Gu.
