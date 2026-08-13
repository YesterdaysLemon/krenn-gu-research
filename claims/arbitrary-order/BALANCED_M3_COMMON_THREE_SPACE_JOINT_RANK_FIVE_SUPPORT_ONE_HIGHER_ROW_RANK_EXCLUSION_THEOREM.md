# Balanced `m=3` common-three-space joint-rank-five support-one higher-row-rank exclusion

## Status

**Exact characteristic-zero exclusion of every transverse joint-rank-five
support-one profile with at least one involved row of rank three.**  Let `U`
be the total singleton span of a normalized, target-consistent physical
`m=3` common shore whose complete four-column sensor has full function-field
rank.  Assume

```text
dim U=3,                         rank H=5.             (1)
```

Retain the transverse two-root branch of S2AG.  Thus the two nonzero
root--root blocks have disjoint derivative summands, the uninvolved third
root row has rank two, and its kernel has target-coordinate support exactly
one.  Then the involved-row profiles

```text
(3,3),                         (3,2),                 (2,3)             (2)
```

are impossible.

The proof does not assume that either root--root block is monomial,
separable, tangent, generic, or invertible.  In the `(3,3)` profile the
support-one contraction is injective on the relation graph, so every
singleton correction lies on the missing target line.  In a mixed profile,
the zero row of the rank-two shore pins the same conclusion and forces its
missing colour to be the support-one colour.  Permanent symmetry then
reduces the equal-kernel graph chart to a two-dimensional square pencil; an
exact two-plane strengthening of the square-pencil obstruction excludes it.
The unequal-kernel mixed chart falls to the already proved binary
five-product obstruction.

This theorem does **not** exclude the support-one `(2,2)` involved-row
profile, any of the three Hilbert--Burch coordinate atlases, joint rank at
most four, another S2T/S2Q component type, a rank-one or pair-plane pole
stratum, a higher order, the all-rank-drop branch, or the global conjecture.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The support-one target and the full coefficient equation

Use the transverse notation of S2AG.  After permuting roots,

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (3)
```

There are a three-plane `P` and a two-plane `N_3` such that

```text
K=P direct-sum N_3,
P subset A_1 direct-sum A_2,
U=D_(B,C)(P).                                        (4)
```

Write the transposed root rows as

```text
rho:A_1^*->W^*,        pi:A_2^*->W^*,
theta:A_3^*->W^*,      W=X direct-sum Y direct-sum Z. (5)
```

Relabel the support-one colour and rescale its kernel generator so that

```text
ker theta=span(e_2^*),              q_2=0.           (6)
```

Put

```text
b=(id tensor e_2^*)(B) in A_2,
c=(id tensor e_2^*)(C) in A_1.                       (7)
```

Contracting the full target equation by `e_2^*` in the third root kills the
all-cross permanent.  The colour-two target therefore gives

```text
e_2 tensor e_2 in
Phi(P),

Phi(a,b')=a tensor b+c tensor b'.                    (8)
```

The decomposable-tensor quotient used in S2AG says that either `b` is a
nonzero multiple of `e_2` or `c` is.  This fact will be used only in the
`(3,3)` graph profile.

For a basis `w_i=(a_i,b_i)` of `P`, put

```text
u_i=D_(B,C)(w_i).                                    (9)
```

The restriction of `D_(B,C)` to `P` is injective.  Hence the complete
coefficientwise target identity has unique tensors `S_i` in the three
nonroot target factors:

```text
G_N-J=sum_i S_i u_i.                                (10)
```

No selected-slice or generic-point replacement is made below; every claim
about the `S_i` comes from all root rows of (10).

## 2. Two exact two-plane lemmas

For `u,v,q in W^*`, write

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (11)
```

Two decomposable tensors are **fully transverse** when their corresponding
factor lines differ in each of `X^*,Y^*,Z^*`.

### Lemma 1 (tangent-line separation and mixed factor sharing)

Let `Q` be any subspace of `W^*`.

1. Suppose `M_(u,u)(Q)` is contained in `span(T,S)`, contains the nonzero
   decomposable tensor `T`, and `S` is decomposable and fully transverse to
   `T`.  Then

   ```text
   M_(u,u)(Q)=span(T).                               (12)
   ```

2. Suppose `M_(u,u)|_Q` and `M_(u,v)|_Q` are nonzero rank-one maps with
   decomposable images `span(T)` and `span(S)`.  Then `T` and `S` share at
   least one source factor line.

#### Proof

A pure `u` has zero square.  If `u=x+y` has two nonzero source components,
then

```text
M_(u,u)(q)=2 x tensor y tensor q_Z.                 (13)
```

Every decomposable tensor in its image shares the `X` and `Y` factor lines
of every other one.  If `u=x+y+z` has three nonzero components, its square
image is the Segre tangent space at `x tensor y tensor z`.  Every
decomposable point of that tangent space shares at least two base factor
lines, so two such points share at least one factor line.  This proves the
first assertion by linearity: a nonzero `S` coefficient would put `S`
itself in the square image.

For the second assertion choose `q_0,q_1 in Q` so that both the square and
mixed values are nonzero at one common linear combination; only finitely
many combinations are excluded.  It remains to work pointwise.

For `u=x+y`, write the active third component as `t`.  If `v_Z` lies on
`span(t)`, the mixed value has third factor `t`.  Otherwise quotient the
mixed value by `span(t)`.  Its surviving `X tensor Y` factor lies in the
Segre tangent at `x tensor y`; if it is decomposable, it shares `x` or `y`.
Thus the mixed product shares a factor with (13).

For `u=x+y+z`, a nonzero decomposable square value can, after permuting
sources, be written

```text
T=xi tensor y tensor z.                              (14)
```

Projecting its square preimage equation modulo `span(y)` and `span(z)`
shows that the preimage has `Y` component on `y` and `Z` component on `z`.
The corresponding mixed value therefore lies in

```text
X tensor y tensor Z + X tensor Y tensor z.           (15)
```

A decomposable tensor in (15) has its `Y` factor on `y` or its `Z` factor
on `z`: project to `(Y/span(y)) tensor (Z/span(z))`.  Thus it shares a
factor with `T`.  This proves the lemma.  QED.

### Lemma 2 (a two-plane cannot carry two transverse squares)

Let `Q` be a two-plane.  There are no nonzero `u,v` such that

```text
M_(u,v)|_Q=0,                                       (16)

M_(u,u)|_Q and M_(v,v)|_Q are nonzero rank-one maps (17)
```

whose decomposable image tensors are fully transverse.

#### Proof

Again a pure `u` is impossible.

Suppose first that `u=x+y`.  The square map is (13).  Choose a basis of `Q`
of the form

```text
q_0=a+b,                     q_1=d+e+t,       t!=0, (18)
```

with `a,d in X^*`, `b,e in Y^*`, and `t in Z^*`.  Write
`v=x'+y'+z'`.  The mixed equation at `q_0` is

```text
z' tensor (x tensor b+a tensor y)=0.                (19)
```

If the parenthesized tensor is nonzero, then `z'=0`; the equation at `q_1`
makes `v` proportional to `x-y`.  Its square image has the same first two
factor lines as (13), contradicting full transversality.

Otherwise `q_0` is proportional to `x-y`.  At `q_1`, equation (16) becomes

```text
z' tensor (x tensor e+d tensor y)
 +(x tensor y'+x' tensor y) tensor t=0.             (20)
```

If `z',t` are independent, both coefficients vanish.  After subtracting a
multiple of `q_0`, one has `q_1=t` and

```text
v=lambda(x-y)+z'.                                   (21)
```

Every square value of (21) shares the first two factor lines `x,y` with
(13).  If `z'` is proportional to `t`, every square value instead shares
the third factor `t`.  Both alternatives contradict full transversality.

Now suppose `u=x+y+z`.  The square kernel is

```text
K_0={(alpha x,beta y,gamma z):alpha+beta+gamma=0}.  (22)
```

Let `q_0` span the intersection of `Q` with this kernel.  After permuting
sources, the active square image is `span(xi tensor y tensor z)`.  Thus

```text
q_0=(a x,b y,c z),         a+b+c=0,
(q_1)_Y in span(y),         (q_1)_Z in span(z).     (23)
```

Write `v=x'+y'+z'`.  Equation (16) at `q_0` is

```text
a x' tensor y tensor z
 +b x tensor y' tensor z
 +c x tensor y tensor z'=0.                         (24)
```

If `abc!=0`, quotienting (24) by each base factor line shows that
`x',y',z'` lie on `x,y,z`, respectively.  Every square value of `v` on
`Q` then shares `y,z` with `T`.  If one coefficient is zero, say `a=0`,
then `b=-c!=0` and (24) forces `y'` and `z'` onto `y,z`.  Both vectors in
`Q` also have their `Y,Z` components on those lines, so every square value
of `v` again shares `y,z` with `T`.  The cases `b=0` and `c=0` similarly
leave the common factor `z` or `y`.  These alternatives exhaust the
nonzero kernel vector `q_0` and contradict full transversality in (17).
QED.

## 3. The `(3,3)` contraction is injective

Assume

```text
rank rho=rank pi=3.                                  (26)
```

Then `P` is the graph of an invertible map:

```text
P={(a,L a):a in A_1},                 L in GL(A_1,A_2). (27)
```

Exchange the involved roots if needed so that (8) has

```text
b=beta e_2,                     beta!=0.             (28)
```

We claim that `Phi|_P` is injective.  If `c=0`, this is immediate.  If
`c!=0`, a kernel vector exists exactly when

```text
L c=-beta e_2.                                      (29)
```

On the other hand, a preimage of the nonzero diagonal in (8) satisfies

```text
L a=mu e_2,
beta a+mu c=lambda e_2,             mu lambda!=0.   (30)
```

Applying `L` to the second identity in (30) and using (29) would give
`0=lambda L e_2`, impossible because `L` is invertible.  Thus

```text
ker(Phi|_P)=0.                                      (31)
```

Contract (10) by `e_2^*`.  Equation (6) kills `G_N`; (31) says that every
nonroot coefficient other than `T_2` has zero singleton correction.  Hence

```text
G_N-J in T_2 tensor U.                              (32)
```

Let

```text
r_a=rho(e_a^*),             p_b=pi(e_b^*),
p_b=sum_i L_(b,i) r_i.                               (33)
```

For a fixed third-root row and nonroot coefficient, write the first-two-root
matrix as `F=S L^T`, where

```text
S_(a,i)=M_(r_a,r_i)(q),                    S=S^T.   (34)
```

Thus `L F` is symmetric.  The `T_0` and `T_1` coefficients of (32) are
respectively `E_00` and `E_11`; consequently

```text
L e_0=lambda_0 e_0,          L e_1=lambda_1 e_1,
lambda_0 lambda_1!=0.                                (35)
```

Put

```text
beta_i=lambda_i^(-1)e_i^*,
alpha_i=L^T beta_i,
u_i=r_(alpha_i)=p_(beta_i),                 i=0,1.  (36)
```

Contracting (32) by `alpha_i tensor beta_i`, and cross-contracting by
`alpha_0 tensor beta_1`, gives on `Q=image theta`

```text
M_(u_0,u_0)(Q) subset span(T_0,T_2),  contains T_0,
M_(u_1,u_1)(Q) subset span(T_1,T_2),  contains T_1,
M_(u_0,u_1)(Q) subset span(T_2).                     (37)
```

The target tensors `T_0,T_1,T_2` are pairwise fully transverse.  Lemma 1
first removes the `T_2` square corrections and then makes the mixed map
zero.  Since (6) and `rank theta=2` make `Q=span(q_0,q_1)` a two-plane,
(37) contradicts Lemma 2.  Therefore the support-one `(3,3)` profile is
impossible.

## 4. A mixed profile has only a `T_2` correction

Assume, after exchanging the involved roots if necessary,

```text
rank rho=3,                     rank pi=2.           (38)
```

Then

```text
P={(a,L a):a in A_1},                   rank L=2.    (39)
```

The target-kernel argument gives a colour `d` and a nonzero scalar `kappa`
such that

```text
ker pi=span(e_d^*),          image L=e_d^perp,
p_d=0,                       B_(d,-)=kappa e_d.      (40)
```

Use the graph basis `u_i=D_(B,C)(e_i,L e_i)` in (10).  On the complete
root row with second coordinate `d`, the all-cross permanent and every
`C tensor L e_i` term vanish.  Equation (10) becomes

```text
-delta_(a,d)delta_(c,d)T_d=kappa delta_(c,d)S_a.    (41)
```

Thus

```text
S_a=0 for a!=d,                 S_d=-kappa^(-1)T_d. (42)
```

At the support-one root row `c=2`, the all-cross permanent vanishes by (6),
but the target contains `T_2 E_22`.  Equations (41)--(42) can absorb it only
if

```text
d=2.                                                    (43)
```

Therefore every mixed-profile singleton correction lies on `T_2`, and

```text
image L=span(e_0,e_1),              p_2=0.           (44)
```

Permanent symmetry applied to the unaffected `T_0,T_1` coefficient matrices
again gives

```text
L e_i in span(e_i),                         i=0,1.  (45)
```

Let `e_s` span `ker L`.

### 4.1 Equal kernel and missing colour

If `s=2`, rank two and (45) give nonzero scalars

```text
L e_0=lambda_0 e_0,       L e_1=lambda_1 e_1,
L e_2=0.                                             (46)
```

Hence `p_i=lambda_i r_i` for `i=0,1`.  The two repeated-row squares and
their cross product satisfy exactly (37).  Lemmas 1--2 exclude this chart.

### 4.2 Distinct kernel and missing colour

Suppose `s!=2`, and let `j` be the third colour.  Equations (44)--(45) give

```text
L e_s=0,             L e_2=a e_s+b e_j,
L e_j=tau e_j,                a tau!=0,              (47)

p_s=a r_2,            p_2=0,
p_j=b r_2+tau r_j.                                  (48)
```

Project each nonroot source space onto its two target-coordinate lines
`s,j`, so the sole correction line `T_2` vanishes.  Bars denote projected
rows and `Qbar` the projected third-row plane.  The binary target has
root-three flattening rank two, so

```text
dim Qbar>=2.                                         (49)
```

Put

```text
u=bar r_2,       v=bar p_j,       r=bar r_s.        (50)
```

The root pairs `(2,s)`, `(2,j)`, and `(s,j)`, followed by `(s,s)` and the
repeated-row contraction realizing `v` on both shores, give

```text
M_(u,u)|Qbar=M_(u,v)|Qbar=M_(r,v)|Qbar=0,           (51)

M_(r,u)|Qbar and M_(v,v)|Qbar are nonzero rank-one
maps onto T_s and T_j.                               (52)
```

The tensors `T_s,T_j` are fully transverse.  Equations (49)--(52) are
exactly the binary five-product obstruction proved as Lemma 1 of S2AF.
Thus the distinct-colour chart is impossible.  Exchanging the involved
roots gives the same conclusion for profile `(2,3)`.

Combining Sections 3--4 proves

```text
rank H=5, transverse derivative rank 6,
rank theta=2 with support-one kernel,
involved rows (3,3), (3,2), or (2,3):               IMPOSSIBLE.       (53)
```

## 5. Proof-topology consequence

The transverse joint-rank-five branch now has

```text
third-row kernel support two, every involved profile: IMPOSSIBLE (S2AI--S2AK);

third-row kernel support one,
  involved rows (3,3), (3,2), or (2,3):             IMPOSSIBLE (here);
  involved rows (2,2):                              OPEN;

three-root Hilbert--Burch coordinate atlases:        OPEN;
joint rank at most four / other physical branches:   OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (54)
```

The `(2,2)` support-one case is not a cosmetic omission.  Both involved
zero rows leave one correction direction that is absent from Sections 3--4;
it requires a separate exact normal form.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_one_higher_row_rank_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_one_higher_row_rank_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_one_higher_row_rank_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_one_higher_row_rank_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_one_higher_row_rank_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_one_higher_row_rank_exclusion.py
```

The primary verifier checks the graph contraction, its injectivity, the
complete zero-row correction table, both graph-kernel charts, tangent-line
separation, and the two-source/three-source two-plane atlas.  The independent
audit imports no repository module and no third-party package; it rebuilds
the sparse permanent tensors with standard-library `Fraction` arithmetic
and a distinct coordinate convention.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Complete joint-rank-six exclusion and binary five-product lemma](BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md)
- [Support-two `(3,3)` exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_THREE_BY_THREE_EXCLUSION_THEOREM.md)
