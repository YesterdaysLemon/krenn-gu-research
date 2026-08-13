# Balanced `m=3` common-three-space joint-rank-five support-two Type-I monomial complete exclusion

## Status

**Exact characteristic-zero exclusion of the complete Type-I monomial atlas
in the transverse joint-rank-five support-two `(2,2)` profile.**  Let `U` be
the total singleton span of a normalized, target-consistent physical `m=3`
common shore.  Assume

```text
dim U=3,                         rank H=5,             (1)
```

and retain the transverse two-root branch of S2AG with a rank-two third row,
kernel support exactly two, and both involved rows of rank two.  If at least
one of the two nonzero root--root blocks is a coordinate monomial (Type I of
the beta-zero atlas), then the physical full-sensor conditions are
inconsistent.

The other root--root block is arbitrary: it is not assumed monomial,
rank-one, tangent, generic, or separable.  Thus this theorem contains the
double-monomial profile of S2AH and closes the previously open
singly-monomial/nonmonomial profile as well.

This theorem does **not** exclude the Type-II-only boundary-pencil tangent
atlas with no coordinate-monomial block, a support-two `(3,3)` or `(3,2)`
involved-row profile, support one, a three-root Hilbert--Burch boundary,
joint rank at most four, another S2T/S2Q component, the all-rank-drop branch,
or a higher order.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. A monomial block leaves two exact kernel-colour charts

Use the transverse notation of S2AG and S2AH.  After permuting roots,

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (2)
```

There are a three-plane `P` and a two-plane `N_3` such that

```text
K=P direct-sum N_3,
P subset A_1 direct-sum A_2,
U=D_(B,C)(P).                                        (3)
```

Write the transposed root-row maps as

```text
rho:A_1^*->W^*,        pi:A_2^*->W^*,
theta:A_3^*->W^*,      W=X direct-sum Y direct-sum Z. (4)
```

The present profile has

```text
rank rho=rank pi=rank theta=2,
ker theta=span(eta),              |support eta|=2.   (5)
```

The target-kernel argument gives target-coordinate kernels

```text
ker pi=span(e_d^*),       (e_d^* tensor id)(B)=kappa e_d,
ker rho=span(e_c^*),      (e_c^* tensor id)(C)=kappa' e_c, (6)
```

with `kappa kappa'!=0`.  The support-two contraction gives, after relabelling
the two supported colours and possibly exchanging roots 1 and 2,

```text
support eta={0,1},
b_eta=(id tensor eta)(B) in span(e_0),
c_eta=(id tensor eta)(C) in span(e_1).               (7)
```

Assume without loss of generality that the Type-I block is `B`.  Equations
(6)--(7) force both endpoints of its monomial to have colour zero.  Rescale:

```text
B=e_0 tensor e_0,                     d=0.           (8)
```

The diagonal row in (6) rules out `c=0`: since `eta(e_0)!=0`, row zero of
`C` would contribute a nonzero `e_0` component to `c_eta`, contrary to (7).
Hence

```text
c in {1,2}.                                           (9)
```

Every `(a,b) in P` satisfies

```text
a_c=0,                          b_0=0.               (10)
```

Contracting target consistency by `eta` gives

```text
eta(U)={a tensor e_0+e_1 tensor b:(a,b) in P}.       (11)
```

The independent target terms of colours zero and one force
`e_0 tensor e_0` and `e_1 tensor e_1` into (11).  The kernel of the ambient
map `(a,b)|->a tensor e_0+e_1 tensor b` is
`span((e_1,-e_0))`; condition `b_0=0` removes that ambiguity.  Therefore

```text
(e_0,0),(0,e_1) in P.                               (12)
```

Both projections of `P` have dimension two.  Subtracting the vectors in
(12) from a third basis vector gives exactly two charts.

```text
c=1:
P=span{(e_0,0),(0,e_1),(e_2,tau e_2)},

c=2:
P=span{(e_0,0),(0,e_1),(tau e_1,e_2)},

tau!=0.                                              (13)
```

No property of the uncontracted rows of `C` was used.

## 2. The `c=2` chart contradicts two target coefficients

In the second chart of (13), choose dual row forms `v_0,v_1,v_2`.  The
involved root rows are

```text
r_0=v_0,        r_1=tau v_2,        r_2=0,
p_0=0,          p_1=v_1,            p_2=v_2.        (14)
```

The singleton plane has basis

```text
u_0=E_000,
u_1=C tensor e_1,
u_2=tau E_100+C tensor e_2.                          (15)
```

Write the full target equation coefficientwise as

```text
G_N-J=S_0 u_0+S_1 u_1+S_2 u_2,                      (16)
```

where the `S_i` are tensors in the three nonroot target factors.  At root
row `(1,0,0)`, the all-cross permanent is zero because `p_0=0`, the target
has no term, and (15) contributes `tau S_2`.  Thus `S_2=0`.

At root row `(2,2,2)`, the all-cross permanent is zero because `r_2=0`,
while the target contributes `T_2`.  By (6), row two of `C` is
`kappa' e_2`, so (15)--(16) give

```text
-T_2=kappa' S_2=0,                                  (17)
```

a contradiction.  Hence only the `c=1` chart could survive.

## 3. The `c=1` chart gives one fully transverse correction line

Retain the nonzero diagonal scalar from (6):

```text
(e_1^* tensor id)(C)=kappa' e_1,       kappa'!=0.   (18)
```

In the first chart of (13), the row forms and singleton plane are

```text
r_0=v_0,       r_1=0,       r_2=v_2,
p_0=0,         p_1=v_1,     p_2=tau v_2,

u_0=E_000,
u_1=C tensor e_1,
u_2=E_200+tau C tensor e_2.                          (19)
```

Let

```text
Q=image theta,
V=span(v_0,v_1,v_2).
```

The S2AG row-space splitting and `rank H=5` give

```text
dim V=3,              dim Q=2,              V intersect Q=0. (20)
```

For `u,v,q in W^*`, write

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (21)
```

Use (16) with the basis (19).  The zero root rows `(0,0,0)`, `(2,0,0)`,
and `(1,1,1)` give respectively

```text
S_0=-T_0,       S_2=0,       S_1=-(kappa')^(-1) T_1. (22)
```

Comparing every third-root colour in the root-row pairs `(0,2)`, `(2,2)`,
`(0,1)`, and `(2,1)` now gives the complete table

```text
M_(v_0,v_2)|_Q=0,
M_(v_2,v_2)|_Q has rank one with image span(T_2),

M_(v_0,v_1)(Q) subset span(T_1),
M_(v_2,v_1)(Q) subset span(T_1).                    (23)
```

More explicitly, for the three root rows `q_j=theta(e_j^*)`,

```text
tau M_(v_2,v_2)(q_j)=delta_(j,2) T_2,
M_(v_0,v_1)(q_j)=-(kappa')^(-1) C_(0,j) T_1,
M_(v_2,v_1)(q_j)=-(kappa')^(-1) C_(2,j) T_1.       (24)
```

Thus every uncontracted entry of the arbitrary block `C` is retained.  The
only information used about its first and third rows is that their target
corrections lie on the colour-one line.

Physical full singleton rank is exactly

```text
Alt_XYZ(v_0,v_1,v_2)!=0.                            (25)
```

The next lemma contradicts (20), (23), and (25).

## 4. A fully transverse correction-line lemma

### Lemma 1

Let `W=X direct-sum Y direct-sum Z`.  Let `V=span(u_0,u_1,v)` be a
three-plane and let `Q` be a two-plane with `V intersect Q=0`.  Suppose

```text
M_(v,v)|_Q has rank one with decomposable image span(T), (26)
```

and let `S` be another nonzero decomposable tensor whose factor line differs
from the corresponding factor line of `T` in **all three** sources.  If

```text
M_(u_0,v)|_Q=0,
M_(u_1,v)(Q) subset span(S),
M_(u_0,u_1)(Q) subset span(S),                       (27)
```

then

```text
Alt_XYZ(u_0,u_1,v)=0.                               (28)
```

### Proof

First, the middle inclusion in (27) is actually equality to zero.

If `v` has only one nonzero source component, its square map is zero,
contrary to (26).  If `v=x+y` has two source components, then

```text
M_(v,u)(q) in
  x tensor Y tensor Z + X tensor y tensor Z          (29)
```

for every `u,q`.  The rank-one square image has first two factor lines
`span(x),span(y)`.  The line `span(S)` meets (29) only at zero because both
of its corresponding factor lines are different.  Hence
`M_(u_1,v)|_Q=0`.

Now let `v=x+y+z` have three source components.  A decomposable tensor in
the tangent image of the square map shares at least two factor lines with
`x tensor y tensor z`: quotient by each base factor line to see this.
After permuting sources, write

```text
T=x tensor y tensor t.                              (30)
```

The square identity

```text
M_(v,v)(q)=2(
  x tensor y tensor q_Z
 +x tensor q_Y tensor z
 +q_X tensor y tensor z)                            (31)
```

and quotienting successively by `span(x)` and `span(y)` show that every
`q in Q` has `q_X in span(x)` and `q_Y in span(y)`.  Consequently (29)
again holds for `M_(v,u)(q)`, and full factor transversality again forces
`M_(u_1,v)|_Q=0`.

Thus `u_0,u_1` are two common mixed zero divisors of `v` on `Q`.  We replay
the exact common-zero atlas from S2AH, retaining the weaker last condition
in (27).

If `v=x+y`, let `q_0` span the square kernel and choose `q_1` with nonzero
square.  The atlas has three cases.

1. In the nonconjugate case the common-zero space is `span(x-y)`, so
   `u_0,u_1` are dependent.
2. In the conjugate case with nonzero tangent term, the common-zero space is
   a two-plane containing `q_0=x-y`.  If `u_0,u_1` were independent, then
   `V intersect Q` would contain `q_0`; otherwise they are dependent.
3. In the fully conjugate case, after changing `q_1` by a multiple of
   `q_0`, write

```text
q_0=w=x-y,                 q_1=t,
u_i=alpha_i w+z_i,         z_i in Z.                 (32)
```

Direct expansion gives

```text
M_(u_0,u_1)(w)
 =-2 x tensor y tensor (alpha_0 z_1+alpha_1 z_0),

M_(u_0,u_1)(t)
 =-2 alpha_0 alpha_1 x tensor y tensor t,

Alt_XYZ(u_0,u_1,v)
 =2 x tensor y tensor (alpha_1 z_0-alpha_0 z_1).     (33)
```

The first two tensors in (33) lie in `span(S)` by (27).  The first already
has the two base factor lines of `T`; the second lies on `span(T)` itself.
Full factor transversality makes both zero.  The two resulting equations
make the last tensor in (33) zero.

Finally let `v=x+y+z`.  A square-kernel vector has the scaling form

```text
q_0=(a x,b y,c z),                 a+b+c=0.          (34)
```

If `abc!=0`, every common zero divisor is

```text
u=(lambda x,mu y,nu z),
a lambda+b mu+c nu=0.                              (35)
```

The scalar triples for `u_0,u_1,v` lie in one two-plane, so their
alternating separated tensor is zero.  If one coefficient in (34) is zero,
say `a=0`, then `b=-c!=0` and every common zero divisor first has the form

```text
u=(u_X,lambda y,lambda z).                          (36)
```

Writing a nonkernel vector as
`q_1=(A x,B y,C z+t)` with `A+B+C=0`, its remaining zero equation is

```text
-A(u_X-lambda x) tensor z
 +(u_X+lambda x) tensor t=0.                        (37)
```

If `z,t` are independent, the solution space has dimension at most one.
If they are proportional, it again has dimension at most one except for
the exact exceptional equality in which every solution is pure in `X`.
Thus `u_0,u_1` are dependent or both pure in one source, and (28) follows.
The other zero-coefficient cases are symmetric.  QED.

## 5. Exclusion of the complete Type-I atlas

Apply Lemma 1 to (20), (23), and the two physical target tensors

```text
T=T_2=X_2 tensor Y_2 tensor Z_2,
S=T_1=X_1 tensor Y_1 tensor Z_1.                    (38)
```

Their factor lines differ in all three sources.  Lemma 1 gives
`Alt_XYZ(v_0,v_1,v_2)=0`, contradicting (25).  Together with (17), this
proves

```text
support-two rank-five (2,2), beta-zero Type I
(at least one coordinate-monomial root block):       IMPOSSIBLE.       (39)
```

No finite-field search, generic-point promotion, point evaluation, or
tangent-family assumption on `C` is used.

### Sharpness of full factor transversality

The three-factor transversality in Lemma 1 is load-bearing.  Let

```text
v=x+y,                  w=x-y,
Q=span(w,t),
u_0=w+z_0,              u_1=z_1,                    (40)
```

where `x in X`, `y in Y`, and `z_0,z_1,t in Z` are independent.  Then

```text
dim span(u_0,u_1,v,Q)=5,
M_(u_0,v)|_Q=M_(u_1,v)|_Q=0,
M_(u_0,u_1)(Q)=span(x tensor y tensor z_1),
M_(v,v)(Q)=span(x tensor y tensor t),

Alt_XYZ(u_0,u_1,v)!=0.                              (41)
```

The two correction lines in (41) share their `X` and `Y` factors.  This is
an exact tensor sharpness fixture, not a physical Krenn--Gu witness.

## 6. Proof-topology consequence

The transverse rank-five branch is now

```text
third-row kernel support two, involved rows (2,2),
  beta-zero Type I, both blocks monomial:             IMPOSSIBLE (S2AH);
  beta-zero Type I, other block arbitrary:            IMPOSSIBLE (this theorem);
  Type-II-only boundary pencil, no monomial block:    OPEN;

third-row kernel support two, involved (3,3)/(3,2):   OPEN;
third-row kernel support one:                         OPEN;
three-root Hilbert-Burch coordinate atlases:          OPEN;
joint rank at most four / other physical branches:    OPEN;
global Krenn-Gu conjecture:                           UNRESOLVED.       (42)
```

The next exact obligation inside this row profile is the Type-II-only
boundary-pencil tangent atlas.  The Type-I theorem does not infer that its
nonmonomial block is tangent and does not apply to a Type-II point unless
that point independently has a coordinate-monomial block.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_type_i_monomial_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_type_i_monomial_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_type_i_monomial_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_type_i_monomial_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_type_i_monomial_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_type_i_monomial_complete_exclusion.py
```

The primary verifier checks both kernel-colour planes, the incompatible
`c=2` coefficients, the complete arbitrary-`C` target table, the
fully-transverse correction-line atlas, and the exact sharpness fixture.
The independent no-import audit rebuilds the root and separated tensors with
standard-library `Fraction` arithmetic and uses a separate sparse
representation.  The scripts replay displayed identities; the arbitrary-
vector and case-exhaustion arguments are the proof above.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md)
