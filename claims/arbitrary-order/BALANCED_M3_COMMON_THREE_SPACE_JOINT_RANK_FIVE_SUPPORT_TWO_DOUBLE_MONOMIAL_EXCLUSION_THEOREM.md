# Balanced `m=3` common-three-space joint-rank-five support-two double-monomial exclusion

## Status

**Exact characteristic-zero exclusion of one complete rank-five boundary
profile.**  Retain the normalized, target-consistent physical `m=3`
common-three-space hypotheses, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

On the transverse two-root branch of S2AG, suppose the uninvolved root row
has rank two and its kernel has support exactly two.  If both involved root
rows also have rank two and both nonzero root--root blocks are coordinate
monomials, then the three physical singleton columns are necessarily
dependent over the function field.  Hence this profile cannot be a full
sensor.

The proof isolates a reusable linear-algebra obstruction.  A two-plane on
which the three mixed polarized products of a separated triple vanish cannot
also carry a nonzero rank-one square of the third vector while remaining
disjoint from the triple and preserving its alternating separated tensor.
The latter tensor is exactly the generic singleton determinant.

This theorem does **not** exclude the support-one kernel, a support-two point
with a `(3,3)` or `(3,2)` involved-row profile, the `(2,2)` profile with one
coordinate-monomial root block and one unrestricted nonmonomial root block,
any three-root Hilbert--Burch boundary, joint rank at most four, another
S2T/S2Q component, a higher order, or the all-rank-drop branch.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The support-two `(2,2)` row profile

Use the transverse notation of S2AG.  After permuting roots,

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (2)
```

There are a three-plane

```text
P=pr_(1,2) K subset A_1 direct-sum A_2              (3)
```

and a two-plane `N_3=K intersect A_3` such that

```text
K=P direct-sum N_3,          U=D_(B,C)(P).           (4)
```

Write the transposed root-row maps as

```text
rho:A_1^*->W^*,        pi:A_2^*->W^*,
theta:A_3^*->W^*,      W=X direct-sum Y direct-sum Z. (5)
```

The surviving S2AG branch has

```text
rank theta=2,                ker theta=span(eta),
|support eta|=2.                                      (6)
```

Assume in this theorem that

```text
rank rho=rank pi=2.                                  (7)
```

The target-kernel argument applies separately to both involved rows.  If
`e_d^*` spans `ker pi`, contraction in that zero row kills the empty
permanent.  Target consistency can absorb the surviving diagonal target
coefficient only on the fixed line `(e_d^* tensor id)(B)`.  Thus

```text
ker pi=span(e_d^*),       (e_d^* tensor id)(B)=kappa e_d,
ker rho=span(e_c^*),      (e_c^* tensor id)(C)=kappa' e_c, (8)
```

with `kappa kappa'!=0`.  In particular, each kernel is one target-coordinate
line.  This argument uses neither an injective third row nor joint rank six.

Contract the two root blocks by `eta`:

```text
b_eta=(id tensor eta)(B),
c_eta=(id tensor eta)(C).                            (9)
```

S2AG proves that the two nonzero lines in (9) are the two coordinate lines
in `support eta`, in opposite root spaces.  Relabel those colours as `0,1`
and exchange roots 1 and 2 if necessary so that

```text
support eta={0,1},       b_eta in span(e_0),
c_eta in span(e_1).                                  (10)
```

## 2. Two monomial blocks force one canonical shore

Assume now that both `B` and `C` are coordinate monomials.  The first
identity in (8), nonvanishing of `b_eta`, and (10) force both endpoints of
the monomial `B` to have colour `0`.  The symmetric argument forces both
endpoints of `C` to have colour `1`.  Rescaling harmless nonzero constants,

```text
B=e_0 tensor e_0,          C=e_1 tensor e_1,
d=0,                       c=1.                     (11)
```

Consequently every `(a,b) in P` has

```text
a_1=0,                     b_0=0.                   (12)
```

Since `q_eta=0`, contraction of the physical empty column by `eta` is zero.
Contracted target consistency gives

```text
eta(J) in eta(U),

eta(U)={a tensor e_0+e_1 tensor b:(a,b) in P}.       (13)
```

The independent pure nonroot monomials `T_0,T_1` in `eta(J)` show that
`e_0 tensor e_0` and `e_1 tensor e_1` belong to (13).  Their ambient
preimages differ respectively from `(e_0,0)` and `(0,e_1)` by multiples of

```text
(e_1,-e_0).                                         (14)
```

Equation (12) kills those multiples.  Therefore

```text
(e_0,0),(0,e_1) in P.                               (15)
```

Both projections of `P` have dimension two by (7).  Subtracting the two
vectors in (15) from a third basis vector gives the exact normal form

```text
P=span{(e_0,0),(0,e_1),(e_2,tau e_2)},     tau!=0.  (16)
```

Choose dual row forms `v_0,v_1,v_2` on this basis.  The involved root rows
and the third-root rows are

```text
r_0=v_0,       r_1=0,       r_2=v_2,
p_0=0,         p_1=v_1,     p_2=tau v_2,

Q=image theta=span(q_0,q_2),        dim Q=2,         (17)
```

where the names `q_0,q_2` only select a basis of the two-plane.  Equations
`dim V=3`, `rank H=5`, and S2AG's row-space splitting say

```text
V=span(v_0,v_1,v_2),       dim V=3,
V intersect Q=0.                                          (18)
```

## 3. The full target equation gives a mixed-product table

For `u,v,q in W^*`, let

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*  (19)
```

be the sign-free polarized product.  From (11) and (16),

```text
U=span{
  E_000,
  E_111,
  E_200+tau E_121
}.                                                   (20)
```

Now impose `G_N-J in U` coefficientwise in all 27 root rows, not merely on
a selected quotient.  The four root-row pairs

```text
(0,1),          (0,2),          (2,1),          (2,2) (21)
```

do not meet the support (20).  The first three also miss the GHZ diagonal,
while the last one carries exactly the colour-`2` diagonal.  Using (17),
the complete consequence is

```text
M_(v_0,v_1)|_Q=0,
M_(v_0,v_2)|_Q=0,
M_(v_1,v_2)|_Q=0,

M_(v_2,v_2)|_Q has rank one with image span(T_2).    (22)
```

The scalar `tau` only rescales the last map.  No Cramer chart, selected-row
replacement, or point evaluation is used in (22).

The three singleton columns are the images under the injective map
`D_(B,C)|_P` of the three separately linear `P`-valued columns.  Their
generic determinant is the alternating separated tensor

```text
A(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(1)))_X tensor
   (v_(sigma(2)))_Y tensor
   (v_(sigma(3)))_Z.                                 (23)
```

Thus full-sensor rank requires

```text
A(v_0,v_1,v_2)!=0.                                  (24)
```

## 4. A separated two-plane mixed-product obstruction

### Lemma 1

Let `K` be a characteristic-zero field and let `W=X direct-sum Y direct-sum
Z`.  Suppose `v_0,v_1,v_2` span a three-plane `V`, `Q` is a two-plane,

```text
V intersect Q=0,                                    (25)
```

the three mixed maps in the first three lines of (22) vanish, and
`M_(v_2,v_2)|_Q` has nonzero rank one with decomposable image.  Then

```text
A(v_0,v_1,v_2)=0.                                   (26)
```

### Proof

Write `v_2=x+y+z` by source components and split according to the number of
nonzero components.

#### One source

If at most one of `x,y,z` is nonzero, then `M_(v_2,v_2)=0`, contrary to the
rank-one hypothesis.

#### Two sources

After permuting sources and rescaling, write

```text
v_2=x+y,              x!=0, y!=0.                   (27)
```

The square map is

```text
M_(v_2,v_2)(q)=2 x tensor y tensor q_Z.             (28)
```

Since its restriction to `Q` has rank one, choose a basis

```text
q_0=a+b,                  q_1=d+e+t,       t!=0,     (29)
```

with `a,d in X`, `b,e in Y`, and `t in Z`.  For any common mixed zero
divisor `u`, the equation at `q_0` is

```text
u_Z tensor (x tensor b+a tensor y)=0.                (30)
```

If the parenthesized tensor is nonzero, then `u_Z=0`; the equation at `q_1`
then gives

```text
u_X tensor y+x tensor u_Y=0,
```

so all common zero divisors lie on the one line `span(x-y)`.  In particular
`v_0,v_1` are dependent and (26) follows.

Otherwise `q_0` is proportional to

```text
w=x-y.                                               (31)
```

Put `R=x tensor e+d tensor y`.  If `R!=0`, the common zero-divisor space of
`v_2` on `Q` is exactly

```text
span{w,-d-e+t}.                                      (32)
```

If `v_0,v_1` are independent, they span (32), so `w` belongs to both `V`
and `Q`, contradicting (25).  If they are dependent, (26) is immediate.

It remains that `R=0`.  Then, after changing `q_1` by a multiple of `q_0`,

```text
q_1=t,
```

and every common zero divisor has the form

```text
v_i=alpha_i w+z_i,             z_i in Z.            (33)
```

The last mixed equation `M_(v_0,v_1)|_Q=0`, first at `w` and then at `t`,
gives

```text
alpha_0 z_1+alpha_1 z_0=0,
alpha_0 alpha_1=0.                                  (34)
```

Direct expansion of (23) gives

```text
A(v_0,v_1,v_2)
 =2 x tensor y tensor (alpha_1 z_0-alpha_0 z_1).     (35)
```

Equations (34) make (35) zero.

#### Three sources

Now `x,y,z` are all nonzero.  The square kernel is the scaling plane

```text
K_0={(a x,b y,c z):a+b+c=0}.                        (36)
```

A nonzero decomposable tensor in the tangent image of the square map shares
at least two factor lines with `x tensor y tensor z`: quotienting by each
base factor line proves this directly.  Permute sources so that the rank-one
image is `x tensor y tensor t`.  Choose

```text
q_0=(a x,b y,c z),                  a+b+c=0,
q_1=(A x,B y,C z+t),                A+B+C=0.         (37)
```

If `abc!=0`, the equation `M_(u,v_2)(q_0)=0` forces

```text
u=(lambda x,mu y,nu z),
a lambda+b mu+c nu=0.                               (38)
```

Both `v_0,v_1` satisfy (38), and `v_2` does as well because `a+b+c=0`.
The three scalar rows therefore lie in one two-plane, so their determinant,
hence (23), is zero.

If one coefficient in (37) is zero, say `a=0`, then `b=-c!=0` and the same
equation gives

```text
u=(u_X,lambda y,lambda z).                          (39)
```

The equation at `q_1` reduces to

```text
-A(u_X-lambda x) tensor z
 +(u_X+lambda x) tensor t=0.                        (40)
```

When `z,t` are independent, (40) has solution space of dimension at most
one.  When `t=tau z`, it again has dimension at most one unless `tau=A`;
in that exceptional case `lambda=0` and every solution lies in the one pure
source `X`.  Thus `v_0,v_1` are either dependent or both pure in `X`, and
(23) vanishes.  The cases `b=0` and `c=0` are symmetric.  This proves the
lemma.  QED.

## 5. Exclusion of the double-monomial profile

Apply Lemma 1 to (18), (22), and (24).  Equations (18) give the required
direct sum, (22) gives all four mixed/square hypotheses, and physical
full-sensor rank gives the nonzero alternating tensor (24).  Lemma 1 instead
gives its vanishing.  This contradiction proves

```text
rank H=5, transverse two-root, rank theta=2,
|support ker(theta)|=2,
rank rho=rank pi=2,
B and C both coordinate monomials:                  IMPOSSIBLE. (41)
```

The argument uses the complete target rows only to obtain the table (22).
It does not assume that the rational pair deck is regular or that a retained
pair jet vanishes.

## 6. Exact sharpness fixture without full singleton rank

The singleton determinant is load-bearing.  Let source coordinates be
`X_i,Y_i,Z_i` and take

```text
v_0=Z_1,                 v_1=Z_0,
v_2=X_2+Y_2,
q_0=X_2-Y_2,             q_2=(1/2)Z_2.              (42)
```

The five row forms in (42) are independent.  They satisfy every identity in
(22), with

```text
M_(v_2,v_2)(q_2)=T_2.                               (43)
```

Together with (11) and (16), the physical empty permanent is exactly
`T_2 E_222`, so `G_N-J` lies in (20).  However the three singleton columns
are

```text
G_X=X_2 u_2,
G_Y=Y_2 u_2,
G_Z=Z_1 u_0+Z_0 u_1,                                (44)
```

for a basis `u_0,u_1,u_2` of `U`.  The first two occupy the same line and
the full sensor has rank at most three.  This exact characteristic-zero
fixture explains why the quotient/permanent equations alone did not close
the profile.  It is a rank-drop shore, not a witness or counterexample.

## 7. Proof-topology consequence

The S2AG transverse rank-five boundary now refines to

```text
third-row kernel support two, involved rows (2,2),
  both root blocks coordinate monomials:             IMPOSSIBLE;

third-row kernel support one:                        OPEN;
support two with involved profile (3,3) or (3,2):    OPEN;
support two, involved profile (2,2),
  one coordinate monomial / unrestricted nonmonomial: OPEN;
three-root Hilbert-Burch coordinate atlases:          OPEN;
joint rank at most four / other physical branches:    OPEN;
global Krenn-Gu conjecture:                           UNRESOLVED.       (45)
```

The next exact transverse obligation is the singly monomial/nonmonomial
`(2,2)` profile, with no tangent-family restriction proved for the
nonmonomial block, or one of the higher involved-row profiles.  No
finite-field probe, timeout, sample, or generic-point promotion is used in
the theorem.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_double_monomial_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_double_monomial_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_double_monomial_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_double_monomial_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_double_monomial_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_double_monomial_exclusion.py
```

The primary verifier checks the forced canonical derivative plane, the four
mixed/square target rows, the alternating singleton determinant, every
source-support case in Lemma 1, and the exact rank-drop fixture.  The
independent no-import audit rebuilds the polarized and alternating tensors
with `Fraction` arithmetic, uses a separate row-reduction implementation,
and checks different representatives of every zero-divisor case.  The
arbitrary-vector and tangent-space arguments are the proof above; the scripts
replay their displayed identities and conventions.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md)
