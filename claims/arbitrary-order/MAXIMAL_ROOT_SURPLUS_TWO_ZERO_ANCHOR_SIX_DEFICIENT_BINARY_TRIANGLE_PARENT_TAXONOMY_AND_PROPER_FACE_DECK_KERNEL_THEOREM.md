# Maximum-root surplus-two zero-anchor six-deficient binary-triangle parent taxonomy and proper-face deck kernel

## Status

**Exact characteristic-zero same-source parent localization (`GLS70`).**
Continue from the `GLS69` six-deficient residual.  This theorem does two
things at the first genuinely binary part of that residual.

First, it classifies all `3,405` post-span profiles having a binary
three-open target.  The `3,360` profiles with one binary triangle form
exactly two structural families and eight type-profile keys.  In one family
the triangle is the first common parent of two nonzero pure pair faces; in
the other it is a minimal binary leaf and any of three four-open equations
is its first strict target-bearing parent.  The remaining `45` profiles are
the single `S_c^2 T_c^4` key already isolated in `GLS69`; one binary pair
face propagates to four binary triangles.

Second, on that sharp `S_c^2 T_c^4` key, the binary pair equation forces an
exact separated normalization at its two endpoints.  Every triangle and
binary four-open quotient above the pair is then just the expected face of
the same equation.  This quotient tower is **not** restriction-separating.
The complete proper-face restriction map of the complementary four-port
deck has a sixteen-dimensional ambient kernel, and that kernel meets the
physical four-port hafnian family nontrivially.  Thus a genuine physical
edge parameter may be invisible to every proper restriction of that deck.

This is a proved impediment to a boundary-only top-down argument, not an
impediment to the top-down programme itself.  A different common-source
parent does see enough: the pure-`c` four-open equation on the four `T_c`
labels forces one outside probe map to carry the missing `z_(0,c)`
coefficient.  Pulling that same coefficient down to its binary triangle
kills both non-pair deck terms.  The remaining pair tensor times one common
one-port deck cannot supply two independent target colours.  This excludes
all `45` labelled copies of the `S_c^2 T_c^4` key.

The exact six-deficient residual therefore falls from `99,180 / 86` to
`99,135 / 85` profiles/keys.  The `3,360` single-binary-triangle profiles in
eight keys remain open, as do every profile without a binary triangle, both
five-deficient residuals, the three-/four-deficient residuals,
unique-nonrigid branch, attachment and response package, nonzero anchor,
arbitrary root order, and global conjecture.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Parent-theorem checkpoint

The parent proposition attacked is:

> No complete zero-anchor root-order-three all-six-rigid hypothetical
> witness realizes any of the `3,405` six-deficient profiles with a binary
> three-open target.

This attempt treats the whole binary-triangle stratum rather than selecting
another support word.  It gives the exact first-parent topology of all nine
type-profile keys, then tests the most coupled key against both the complete
proper-face restriction tower of its actual complementary deck and the
different pure four-open source equation.  The first test finds a physical
nonseparation direction; the second supplies the transverse old-probe
coefficient that closes the key through one triangle.  Consequently another
quotient of the same boundary faces would have been insufficient, while the
top-down change of parent is load-bearing.

The displayed physical four-port deck family is a sharp control, not a
counterexample.  It is not extended here to a six-label GHZ witness, and the
proved exclusion shows that no such extension can realize this key.

## Dependencies, field, and notation

- [`GLS63`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)
  owns the common physical open-set hierarchy and deficient types.
- [`GLS67`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_CLASS_AND_P3_ORBIT_LOCALIZATION_THEOREM.md)
  owns the exact two-open pair classes.
- [`GLS69`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_THEOREM.md)
  owns the post-span six-deficient census, the support formula, and the
  `S_c^2 T_c^4` binary-pair localization.

Work over the characteristic-zero fraction field `F` of the common probe
and generic-kernel polynomial domain.  No target coefficient, edge, or deck
is silently specialized to zero.  As in `GLS69`, for each colour put

```text
D_a={n:a notin A_n},
C_I={a:D_a=I}.                                        (1)
```

The six deficient types are written

```text
S_c: rank two, A={c};
R_c: rank one, row J=F e_c^*, A={a,b};
T_c: rank two, A={a,b},              {a,b,c}={0,1,2}. (2)
```

## 1. Exact taxonomy of the single-binary-triangle stratum

Fix a profile with exactly one binary target triangle.  Relabel its unique
triangle as

```text
T={0,1,2},             O={3,4,5}.                    (3)
```

Permute colours so its two target colours are `1,2` and the third colour is
`0`.

### Theorem 1 (two families, eight keys)

Exactly one of the following occurs.

**Family A: two pure pair faces.**  For `r=0,1,2,3`, the type word is

```text
S_0 R_2 R_1 R_0^(3-r) T_0^r,                         (4)
```

up to permutations inside the indicated blocks, and

```text
D_0=O,             D_1={0,2},       D_2={0,1},
C_{01}={2},         C_{02}={1},      C_{12}=empty,
{a:D_a=T}=empty.                                      (5)
```

The four key sizes, in increasing `r`, are

```text
360, 1,080, 1,080, 360.                              (6)
```

**Family B: an exact-three-set binary leaf.**  For `r=0,1,2,3`, the type
word is

```text
S_0^3 R_0^(3-r) T_0^r,                               (7)
```

and

```text
D_0=O,             D_1=D_2=T,
C_{01}=C_{02}=C_{12}=empty,
{a:D_a=T}={1,2}.                                      (8)
```

The four key sizes are

```text
60, 180, 180, 60.                                    (9)
```

In particular, no surviving profile in this stratum has one proper pair
class together with one exact-three-set class.

### Proof

Apply the `GLS69` pair and rank-one triangle-span predicates to all
`9^6=531,441` labelled deficient type words.  There are `99,180` final
survivors.  Select those with exactly one triple containing exactly two
sets `D_a`; this gives `3,360` profiles and eight `S_6 x S_3` keys.

For each selected profile, decompose its two target colours according to
whether `D_a` is one of the three pairs in `T` or is exactly `T`.  The only
observed and exhaustively checked multisets are `pair+pair` and
`triple+triple`.  In the first case their two missing pairs intersect in one
label.  That label must be `S_0`; the other two labels of `T` are respectively
`R_2,R_1`, while every outside label supports both target colours and is
`R_0` or `T_0`.  This is (4)--(6).  In the second case every label of `T` is
`S_0`, and again every outside label is `R_0` or `T_0`, giving (7)--(9).
The binomial multiplicities of the three outside labels give the displayed
key sizes.  The primary set implementation and independent mask
implementation agree profile by profile on these alternatives. `square`

### Corollary 1.1 (first same-source parents)

In Family A the unique binary triangle equation is

```text
g_01 tensor d_2^01 + g_02 tensor d_1^02
 + g_12 tensor d_0^12
 =theta_1 e_1^tensor3+theta_2 e_2^tensor3,            (10)
```

with nonzero pure pair faces on `{0,1}` and `{0,2}` and zero target on
`{1,2}`.  Equation (10) is the smallest common same-source parent of the two
nonzero pair faces.

In Family B all three pair targets are zero.  Equation (10) is itself the
minimal target-bearing leaf.  Its first strict target-bearing parents are
exactly the three four-open equations on `T union {u}`, `u in O`; each still
has the same two target colours.

This is a statement about target support and same-source face incidence.
It does not assert that the displayed one-port decks are independent or
that either family is physically realizable.

## 2. The four-binary-triangle key and its pair normalization

The other binary-triangle profiles are the `45` labelled copies of the one
key

```text
S_c^2 T_c^4.                                         (11)
```

Let `s,t` be the two `S_c` labels and let
`U={1,2,3,4}` be the four `T_c` labels.  Write
`{a,b,c}={0,1,2}`.  Normalize the kernel lines as

```text
K_s=K_t=F e_c,
K_u=F v_u,              v_u=e_a+lambda_u e_b,
lambda_u in F^times.                                   (12)
```

Use generic kernel vectors `x_u=tau_u v_u`, and put

```text
Lambda=product_(u in U) lambda_u,
tau_U=product_(u in U) tau_u,
h=H_U(v_1,v_2,v_3,v_4).                              (13)
```

Here `H_U` is the actual four-port matching deck complementary to `{s,t}`.

### Theorem 2 (forced separated binary pair)

The pair equation is

```text
g_st H_U(x_U)
 =mu_a z_(0,a)z_(1,a) tau_U e_(s,a)^* tensor e_(t,a)^*
 +mu_b z_(0,b)z_(1,b) tau_U Lambda
      e_(s,b)^* tensor e_(t,b)^*.                    (14)
```

Consequently `h!=0`.  Up to exchanging `s,t`, exchanging the two source
orientations, and nonzero row scalings, its two rank-one summands are

```text
p_s=z_(0,a)e_(s,a)^*,       q_s=z_(1,b)e_(s,b)^*,
p_t=beta z_(0,b)e_(t,b)^*, q_t=alpha z_(1,a)e_(t,a)^*, (15)

alpha=mu_a/h,               beta=mu_b Lambda/h.
```

### Proof

Equation (14) is the `GLS69` two-open equation; contraction of the four
kernel vectors gives `H_U(x_U)=tau_U h`.  Its target has two nonzero diagonal
coordinates, so `h` cannot vanish.

The common kernel `F e_c` says that all four endpoint maps take values in
the `a,b` coordinate planes.  Write their scalar probe forms as

```text
p_s=A e_(s,a)^*+B e_(s,b)^*,
q_s=C e_(s,a)^*+D e_(s,b)^*,
p_t=E e_(t,a)^*+F e_(t,b)^*,
q_t=G e_(t,a)^*+H e_(t,b)^*.                         (15a)
```

Here `A,B,E,F` are linear forms in `z_0`, while `C,D,G,H` are linear forms
in `z_1`.  Coefficient comparison in (14) gives

```text
A tensor G+E tensor C=alpha z_(0,a) tensor z_(1,a),
A tensor H+F tensor C=0,
B tensor G+E tensor D=0,
B tensor H+F tensor D=beta z_(0,b) tensor z_(1,b).   (15b)
```

At least one of the eight forms in (15a) is zero.  Otherwise the two middle
rank-one syzygies give nonzero scalars `e,f` with

```text
F=f A,             H=-f C,
E=e B,             G=-e D.                           (15c)
```

The two diagonal left sides in (15b) are consequently

```text
e(B tensor C-A tensor D),
f(A tensor D-B tensor C).                            (15d)
```

They are proportional, whereas the two right sides are the independent
nonzero tensors `z_(0,a) tensor z_(1,a)` and
`z_(0,b) tensor z_(1,b)`.  This contradiction proves the claim.

The symmetries exchanging `s,t`, exchanging `a,b`, and exchanging the two
old probes act transitively on the eight forms, so take `A=0`.  The first
equation in (15b) gives

```text
E proportional z_(0,a),       C proportional z_(1,a),
E!=0,                          C!=0.
```

The second then gives `F=0`.  The fourth gives

```text
B proportional z_(0,b),       H proportional z_(1,b),
B!=0,                          H!=0.
```

The third equation now separates the independent forms `B,E` and forces
`G=D=0`.  Exchanging `a,b` and absorbing the four nonzero scalars gives
exactly (15). `square`

The normalization is a consequence of the pair equation.  It is not a
choice of independent companions at later faces.

## 3. What the triangle and four-open quotients do and do not say

For `u in U`, set

```text
d_u=H_U(x_(U-{u}),-_u),
row J_u=F r_u^0+F e_(u,c)^*,
r_u^0=e_(u,b)^*-lambda_u e_(u,a)^*.                  (16)
```

Let `rho_u` be the quotient by `row J_u`.  Since
`rho_u(e_(u,b)^*)=lambda_u rho_u(e_(u,a)^*)`, evaluation at `x_u`
gives the exact synchronized class

```text
rho_u(d_u)
 =h tau_(U-{u}) rho_u(e_(u,a)^*).                    (17)
```

Choose the unique row-space remainder relative to this representative,

```text
r_u=d_u-h tau_(U-{u})e_(u,a)^* in row J_u.           (18)
```

### Theorem 3 (the quotient is the pair face again)

Quotient the binary triangle on `{s,t,u}` at `u`.  Every companion incident
with `u` dies, and the result is exactly (14).  Before quotienting, its
actual residual equation is

```text
g_st tensor r_u
 +g_su tensor d_t^su+g_tu tensor d_s^tu
 =mu_b z_(0,b)z_(1,b) tau_(U-{u}) Lambda_(U-{u})
   e_(s,b)^* tensor e_(t,b)^* tensor r_u^0.           (19)
```

Thus quotient synchronization leaves the row-supported remainder `r_u`
unconstrained; it does not make either of the other two terms vanish.

For distinct `u,v in U`, put `Q=U-{u,v}` and

```text
D_uv=H_U(x_Q,-_u,-_v).
```

Then

```text
(rho_u tensor rho_v)(D_uv)
 =h tau_Q rho_u(e_(u,a)^*) tensor rho_v(e_(v,a)^*).  (20)
```

Write

```text
D_uv=h tau_Q e_(u,a)^* tensor e_(v,a)^*+R_uv,
R_uv in row J_u tensor V_v^* + V_u^* tensor row J_v. (21)
```

Double quotienting the four-open equation on `{s,t,u,v}` again gives only
the pair face.  Its honest unquotiented residual is

```text
g_st tensor R_uv
 +sum_(I in binom({s,t,u,v},2), I!={s,t})
      g_I tensor Hbar_I
 =mu_b z_(0,b)z_(1,b) tau_Q Lambda_Q
   e_(s,b)^* tensor e_(t,b)^*
   tensor [e_(u,b)^* tensor e_(v,b)^*
           -lambda_u lambda_v
            e_(u,a)^* tensor e_(v,a)^*].             (22)
```

### Proof

Equations (17) and (20) are evaluations of one physical multilinear tensor,
not new deck choices.  In the triangle quotient, `g_su` and `g_tu` die in
their `u` factor.  Substituting (15), (17), and (18) into the remaining term
and subtracting it from the unquotiented target gives (19).

In the double quotient, every pair except `{s,t}` meets `u` or `v` and dies
in a companion factor.  Substituting (20)--(21) into the full four-open
equation gives (22).  No factorization of `D_uv` into the one-port remainders
is assumed. `square`

Equations (19) and (22), rather than their quotients, are the first open
row-supported integrability obligations.

## 4. Exact proper-face kernel of the complementary deck

For each `u`, let

```text
A_u=Ann(v_u)=row J_u subset V_u^*.                   (23)
```

Define the complete proper-face restriction map

```text
Phi: tensor_(u in U)V_u^*
  -> direct-sum_(empty!=C subseteq U)
       tensor_(u notin C)V_u^*,                      (24)
```

whose `C` component evaluates every slot in `C` at its corresponding
`v_u`.  Including all nonempty `C` is redundant but makes the meaning
explicit: `Phi` records every proper face based at the common kernel tuple.

### Theorem 4 (ambient kernel and physical intersection)

The kernel is exactly

```text
ker Phi=tensor_(u in U) A_u,          dim_F ker Phi=2^4=16. (25)
```

Moreover this kernel has a nonzero direction inside the physical four-port
hafnian family.  Let

```text
R=r_1^0 tensor r_2^0 tensor r_3^0 tensor r_4^0.      (26)
```

Choose physical edge tensors on `U` by

```text
W_12=kappa r_1^0 tensor r_2^0,   W_34=r_3^0 tensor r_4^0,
W_13=e_(1,a)^* tensor e_(3,a)^*,
W_24=(1-chi)e_(2,a)^* tensor e_(4,a)^*,
W_14=e_(1,a)^* tensor e_(4,a)^*,
W_23=chi e_(2,a)^* tensor e_(3,a)^*,
kappa!=0,                    chi notin {0,1}.         (27)
```

Their matching deck is

```text
H_U=e_(1,a)^* tensor e_(2,a)^* tensor e_(3,a)^*
       tensor e_(4,a)^*+kappa R.                     (28)
```

All values of `kappa` have exactly the same complete proper-face tower,
while the full four-open tensor changes when `kappa` changes.

### Proof

Choose a covector `l_u` with `l_u(v_u)=1`.  Then

```text
V_u^*=F l_u direct-sum A_u.                          (29)
```

The tensor-product decomposition indexed by subsets of `U` is direct.  Any
component having an `l_u` factor is detected by evaluation at `v_u` after
projecting the other factors to their chosen summands.  The only component
killed by every one-slot evaluation is the component with an `A_u` factor
at every slot.  This proves (25); all larger-`C` components in (24) add no
further restriction.

Each `r_u^0` annihilates `v_u`, so `R` lies in (25).  The three perfect
matchings of four labels give

```text
W_12 W_34+W_13 W_24+W_14 W_23,
```

The last two matching products have coefficients `1-chi` and `chi`, so
their sum is the first term of (28); the first matching product is
`kappa R`.  Thus the result is exactly (28), with every displayed edge
nonzero.  Every proper face evaluates at least one factor
`r_u^0` of `R` on `v_u` and kills it.  The coefficient of `R` in the full
tensor remains `kappa`. `square`

The construction is a common physical **deck** control.  It is not a
six-label graph satisfying the GHZ identity: varying one of its edges can
change other complementary decks and may be detected by the unquotiented
terms in (19), (22), the pure four-open equation, or the full six-open
equation.

## 5. Top-down exclusion of the four-binary-triangle key

For the pure four-open set `U`, contract `s,t` at nonzero vectors on their
common kernel lines.  If

```text
eta=W_st(x_s,x_t),
a_u=W_su(x_s,-),               b_u=W_tu(x_t,-),
D_uv^st=eta W_uv+a_u tensor b_v+b_u tensor a_v,       (30)
```

then the exact common-source equation is

```text
sum_({u,v} subset U) g_uv tensor D_(U-{u,v})^st
 =kappa_c z_(0,c)z_(1,c) tensor_(u in U)e_(u,c)^*,
kappa_c!=0.                                            (31)
```

This is an honest four-port source equation coupling the two `S_c` kernel
contractions to all four `T_c` probe maps.  The tensors `D_uv^st` are fixed
physical decks, independent of the old-probe variables.  Equation (31) is
not called a separated `P_4` restriction: when `eta!=0`, its first term in
(30) need not have the required two-row factorization.

Write

```text
p_u(z_0)=sum_(d=0)^2 z_(0,d) p_(u|d),
q_u(z_1)=sum_(d=0)^2 z_(1,d) q_(u|d).                (32)
```

### Theorem 5 (`S_c^2 T_c^4` is impossible)

No hypothetical witness realizes the profile (11).

### Proof

If every `p_(u|c)` vanished, every companion `g_uv` in (31) would have zero
`z_(0,c)` coefficient: the other shore `q` depends only on `z_1`, and the
decks are old-probe independent.  The right side of (31) has the nonzero
coefficient

```text
kappa_c z_(1,c) tensor_(u in U)e_(u,c)^*.
```

Therefore choose `u in U` with

```text
p_(u|c)!=0.                                           (33)
```

Return to the actual binary triangle on `{s,t,u}`.  In the notation of
(19), take its `z_(0,c)` coefficient.  The pair companion `g_st` contributes
nothing by the separated normalization (15).  In `g_su` and `g_tu`, only
the terms `q_s tensor p_u` and `q_t tensor p_u` contribute.  Factoring the
nonzero common local vector (33) gives

```text
q_s(z_1) tensor d_t^su+d_s^tu tensor q_t(z_1)=0.      (34)
```

By (15), after harmless nonzero scalings,

```text
q_s=z_(1,b)e_(s,b)^*,        q_t=z_(1,a)e_(t,a)^*.   (35)
```

The scalar forms `z_(1,a)` and `z_(1,b)` are independent.  Their separate
coefficients in (34) force

```text
d_t^su=0,                     d_s^tu=0.               (36)
```

The full triangle equation consequently reduces to

```text
g_st tensor d_u
 =theta_a z_(0,a)z_(1,a)e_(s,a)^* tensor e_(t,a)^*
                         tensor e_(u,a)^*
 +theta_b z_(0,b)z_(1,b)e_(s,b)^* tensor e_(t,b)^*
                         tensor e_(u,b)^*,            (37)
```

with `theta_a theta_b!=0`.  Comparing the first probe monomial with (15)
makes the same one-port deck `d_u` a nonzero multiple of `e_(u,a)^*`.
Comparing the second makes it a nonzero multiple of the independent
covector `e_(u,b)^*`.  This is impossible. `square`

Every deck in the proof is an actual restriction of the one physical edge
array.  The argument divides by no edge, by no `eta`, and by no possibly
zero complementary deck other than the already-proved nonzero pair scalar
`h`.  It uses the pure four-open parent only to select one nonzero fixed
probe coefficient and then descends to that port's synchronized triangle.

### Corollary 5.1 (updated six-deficient residual)

Deleting the `45` labelled profiles in the one key (11) gives

```text
99,180 / 86  ->  99,135 / 85.                        (38)
```

The `(2,2,4)` missing-size row falls from `4,365 / 4` to `4,320 / 3`.
The minimum-size-two row falls from `64,710 / 48` to `64,665 / 47`.
All remaining profiles with a binary triangle are exactly the `3,360`
single-triangle profiles in the eight keys of Theorem 1.

## 6. Exact frontier and next parents

```text
single-binary-triangle taxonomy:                      3,360 / 8 PROVED;
Family A pair+pair first-parent structure:            PROVED;
Family B exact-triple first-parent structure:         PROVED;

S_c^2 T_c^4 binary pair normalization:                PROVED;
four triangle quotient faces:                         SYNCHRONIZED;
six binary four-open double quotients:                SYNCHRONIZED;
complete proper-face map for H_U:                     NOT SEPARATING;
ambient proper-face kernel dimension:                 16;
physical hafnian direction in that kernel:            EXHIBITED;
pure-U parent plus one triangle:                       S_c^2 T_c^4 EXCLUDED;

six-deficient post-GLS70 residual:                    99,135 / 85 OPEN;
single-binary Family A and B source integrability:     OPEN;
all pure/zero-triangle six-deficient profiles:         OPEN;
five-deficient, three-/four-deficient residuals:       OPEN;
unique-nonrigid and every downstream gate:             OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.        (39)
```

For the `3,360` single-triangle profiles, Family A next requires coupling
the two pure pair faces inside (10), while Family B next requires coupling
its exact-three-set leaf to all three four-open parents.  The two families
must not be collapsed into the now-excluded `S_c^2 T_c^4` mechanism.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py
```

The primary verifier independently rebuilds the nine deficient types,
replays the `GLS69` pair and triangle-span predicates, checks all profile and
key counts, and verifies the two-family classification.  It also checks the
displayed pair/quotient scalar identities, the rank-six coefficient system
in (34), the updated residual count, and the physical hafnian family
exactly.

The independent audit uses integer support masks, a different canonical
signature, a separate tensor-dictionary hafnian expansion, and modular
linear algebra.  It reproduces the finite taxonomy and checks that the
proper-face kernel has dimension sixteen on exact sample fibres.

The programs audit the finite and displayed algebraic leaves.  The
rank-two decomposition argument, the characteristic-zero direct-sum proof,
the old-probe coefficient extraction from (31), and the same-source
derivation of the residual equations remain written mathematics.  The
programs do not prove a full physical realization; the written argument
excludes only the one key stated in Theorem 5.
