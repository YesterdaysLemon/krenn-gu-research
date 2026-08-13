# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` `beta_t`-coloop support localization

## Status

**Exact characteristic-zero localization of the distinguished second-root
coordinate-coloop orientation in the `(1,2,2)` Hilbert--Burch profile on the
normalized, target-consistent physical `m=3` common-three-space full-sensor
stratum.**  Let `U` be the total singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AZ normal form

```text
ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2.                     (2)
```

Write `N=K^perp`.  Suppose the S2AZ coordinate-coloop fork selects

```text
N subset {beta_t=0}.                                  (3)
```

Then necessarily

```text
pi:A_2^*->W^* and theta:A_3^*->W^* are injective,
w_t=0,
w is proportional to e_a or e_b,                     (4)
```

where `a,b` are the two colours different from `t`.  Two further exact
incidence conditions hold:

```text
if s=t, then y is proportional to e_a or e_b;

span(z,w) contains e_i for at least one i!=s.         (5)
```

Consequently the complete residual of the `beta_t`-coloop orientation is a
pair of target-coordinate endpoints for `w`, subject to (5):

```text
w proportional to e_a or e_b, with
  s=t only if y is also coordinate,
  and span(z,w) containing a coordinate e_i, i!=s;    OPEN.       (6)
```

This theorem does not exclude either coordinate endpoint in (6), the other
eight coordinate-coloop orientations, joint rank at most four, other physical
component types, higher orders, or the global conjecture.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. The complete derivative-zero face

The gauge-fixed Hilbert--Burch blocks and derivative are

```text
B_23=y tensor w-mu e_t tensor z,
B_13=-lambda e_s tensor w,
B_12= lambda mu e_s tensor e_t,

D_B(A,B,C)
 =A tensor(y tensor w-mu e_t tensor z)
  -lambda e_s tensor B tensor w
  +lambda mu e_s tensor e_t tensor C.                (7)
```

For root covectors `alpha,beta,gamma`, its transpose is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_t gamma(z))alpha,
   -lambda alpha_s gamma(w) beta,
    lambda mu alpha_s beta_t gamma).                 (8)
```

Hence, without imposing the annihilator equations of S2AZ,

```text
beta_t=0,                  gamma(w)=0
       implies D_B^T(alpha tensor beta tensor gamma)=0. (9)
```

Write the transposed root rows as

```text
r(alpha)=rho(alpha),       p(beta)=pi(beta),
q(gamma)=theta(gamma),
T_i=X_i tensor Y_i tensor Z_i.                       (10)
```

Since `U=D_B(K)`, equation (9) and the complete target equation give the
exact face

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i,
 beta_t=0,                  gamma(w)=0.               (11)
```

This is a polynomial identity on the entire displayed product of linear
spaces, not a sampled or generic statement.

## 2. Root-row ranks and what the `beta_t` coloop does

Put

```text
A=lambda^(-1)r_s,
R=rho(e_s^perp).                                     (12)
```

Let `E=image H^T`.  Since `rank H=5` and

```text
V=H^T(L),                    dim V=3,                 (13)
```

the quotient `E/V` has dimension two.  The S2AZ canonical rows give, modulo
`V`,

```text
r(alpha) congruent lambda alpha_s A,
p(beta) congruent beta(y)A+mu beta_t B,
q(gamma) congruent gamma(z)A+gamma(w)B,               (14)
```

where `B=mu^(-1)p_t`.  The classes of `A,B` form a basis of `E/V`.
Independence of `y,e_t` and of `z,w` makes each of the last two quotient
maps have rank two.

Let `0!=u` span `y^perp intersect e_t^perp`.  If `p(u)=0`, second-root
contraction by `u` kills the all-cross term and every term of `D_B(K)`:
the first and third terms use `u(y)=u_t=0`, and the middle term is killed
because `u` annihilates the second projection of `K`.  The target contraction
is nonzero, a contradiction.  Thus `p(u)!=0`, and it supplies the third row
direction over the rank-two quotient image.  The identical third-root
argument with `0!=v in z^perp intersect w^perp` gives `q(v)!=0`.  Therefore

```text
dim image pi=dim image theta=3.                       (15)
```

Both maps are injective.

S2AZ proves `dim R=2` and, under (3),

```text
H^T(L intersect {beta_t=0})=R,                       (16)
```

where `L=(ker D_B)^perp`.  For every `beta in e_t^perp`, the covector

```text
(-lambda^(-1)beta(y)e_s^*, beta,0)                   (17)
```

belongs to the hyperplane in (16).  For every `gamma in w^perp`, so does

```text
(-lambda^(-1)gamma(z)e_s^*,0,gamma).                 (18)
```

Their row images give

```text
p(beta)-beta(y)A in R,          beta_t=0,
q(gamma)-gamma(z)A in R,       gamma(w)=0.           (19)
```

All first-root rows also lie in

```text
S_0=R+span(A),                    dim S_0<=3.          (20)
```

Thus every row occurring in the complete face (11) lies in the same space
`S_0` of dimension at most three.

## 3. Two auxiliary complete faces

The line

```text
span(u)=y^perp intersect e_t^perp                    (21)
```

lies in `e_t^perp`.  For `alpha_s=0`, `beta=u`, and arbitrary `gamma`, all
three components of (8) vanish.  Likewise, with

```text
span(v)=z^perp intersect w^perp,                     (22)
```

the transpose vanishes for `alpha_s=0`, `gamma=v`, and arbitrary `beta`.
The complete target equation gives

```text
per(r(alpha),p(u),q(gamma))
 =sum_i alpha_i u_i gamma_i T_i,

per(r(alpha),p(beta),q(v))
 =sum_i alpha_i beta_i v_i T_i,        alpha_s=0.    (23)
```

The pure covectors `(0,u,0)` and `(0,0,v)` lie in the coloop hyperplane in
(16), so

```text
p(u),q(v) in R.                                      (24)
```

We use the following immediate coefficient fork.  Let `(r_i,r_j)` be a
basis of `R`, let `d=c r_i+d' r_j` lie in `R`, and suppose a three-dimensional
row shore has independent coordinate functionals `ell_i,ell_j` with

```text
per(r_i,d,-)=ell_i T_i,
per(r_j,d,-)=ell_j T_j.                              (25)
```

If `c,d'` are both nonzero, the square map `per(d,d,-)` contains both fully
transverse targets, contrary to the S2AL tangent-line lemma.  If exactly one
coefficient is zero, its nonzero square and the other mixed map are rank-one
maps onto fully transverse targets, contrary to S2AL mixed factor sharing.
Thus (25) is impossible.

Because `theta` is injective, distinct root coordinates are independent
functionals on its three-dimensional image.  The first equation of (23) and
(24)--(25) therefore show that `u` cannot have both coordinates outside `s`
nonzero.  Since `u_t=0`, this has new content precisely when `s=t`; then
choosing `u=y_b e_a^*-y_a e_b^*` gives
`u_a u_b=-y_a y_b`, so `y` is coordinate.  This proves the first line of
(5).

Similarly `pi` is injective, so the second equation of (23) shows that `v`
cannot have both coordinates outside `s` nonzero.  Hence `v_i=0` for at
least one `i!=s`.  Since `v` is the normal to the two-plane `span(z,w)`, this
is equivalent to `e_i in span(z,w)`, proving the second line of (5).

## 4. Excluding `w_t!=0`

Assume `w_t!=0`.  Restriction to the two complementary target coordinates
is an isomorphism

```text
w^perp -> span(e_a,e_b)^*,
gamma |-> (gamma_a,gamma_b).                         (26)
```

Choose its coordinate lifts `gamma^a,gamma^b` and put

```text
q'_i=q(gamma^i),              i in {a,b}.             (27)
```

Equation (11) becomes the complete binary diagonal cube

```text
per(r_i,p_j,q'_k)=delta_(i,j,k)T_k,
i,j,k in {a,b}.                                      (28)
```

The two nonzero diagonal cells and the crossed zero cells show separately
that

```text
R_t=span(r_a,r_b),
P_t=span(p_a,p_b),
Q_t=span(q'_a,q'_b)                                  (29)
```

are two-planes.  By (19)--(20), all three lie in `S_0`.  If their span has
dimension two, all three planes agree and the equal-plane part of the S2AN
binary-diagonal obstruction applies.  If it has dimension three, S2AN
Lemma 1 applies directly.  Both alternatives contradict the full
transversality of `T_a,T_b`.  Therefore (4) holds.

## 5. Excluding complementary support two

Now assume (4) and

```text
w_a w_b!=0.                                          (30)
```

The covectors

```text
n=w_b e_a^*-w_a e_b^*,            e_t^*              (31)
```

form a basis of `w^perp`.  Put `q'=q(n)`.  Equation (11) gives

```text
per(r_a,p_a,q')= w_b T_a,
per(r_b,p_b,q')=-w_a T_b,
per(r_a,p_b,q')=per(r_b,p_a,q')=0,                  (32)

per(r_i,p_j,q_t)=0,                 i,j in {a,b}.    (33)
```

Again the first two row families in (32) are two-planes.  Injectivity of
`theta` gives `q_t!=0`.  Moreover `q_t` is not proportional to `q'`, since
(32)--(33) would otherwise make a nonzero target vanish.  Hence

```text
Q=span(q',q_t)                                       (34)
```

is a two-plane.  Equations (19)--(20) place the three two-planes

```text
span(r_a,r_b),       span(p_a,p_b),       Q           (35)
```

inside the same at-most-three-space.  In dimension two the relevant planes
agree and the equal-plane calculation in S2AO applies; in dimension three,
S2AO Lemma 1 applies directly.  The table (32)--(33) is exactly its
same-third-row binary diagonal table with fully transverse targets
`T_a,T_b`.  This contradiction proves `w_a w_b=0`.  Since `w` is nonzero
and `w_t=0`, it is proportional to exactly one of `e_a,e_b`, completing
(4).

## 6. Proof-topology consequence

S2AZ and this theorem refine one of the nine `(1,2,2)` coordinate-coloop
orientations to the two coordinate endpoints in (6):

```text
beta_t coloop:
  pi and theta:                                        INJECTIVE;
  w_t!=0:                                             IMPOSSIBLE;
  w_t=0, w_a w_b!=0:                                 IMPOSSIBLE;
  w proportional e_a or e_b, subject to (5):         OPEN.

other eight (1,2,2) coloops / joint rank <=4
  / other components / higher m:                     OPEN.       (36)
```

Neither endpoint in (36) is asserted to be realizable.

## Focused replay

```bash
python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_support_localization.py
python claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_support_localization.py
```

The primary replay checks the derivative-zero face, injectivity rank forks,
both auxiliary faces and their coordinate-incidence consequences, and both
exact binary tables.  The independent audit rebuilds the same identities
with standard-library rational arithmetic and separate elimination code.
The S2AL coefficient fork and S2AN/S2AO three-plane incidence lemmas are
invoked as already proved dependencies.

## Dependencies

- [`(1,2,2)` coordinate-coloop localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md)
- [Tangent-line and mixed factor-sharing lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
- [Three-plane binary-diagonal frame obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_LOCALIZATION_THEOREM.md#2-a-three-plane-cannot-carry-a-binary-diagonal-permanent-frame)
- [Same-third-row binary-diagonal obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md#2-a-same-third-row-binary-diagonal-frame-is-impossible)
