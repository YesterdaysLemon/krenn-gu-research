# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective monomial-residual endpoint localization

## Status

**Exact characteristic-zero localization inside the last `(3,3,3)` row
profile of the joint-rank-four, derivative-rank-eight three-root chart.**
Retain the normalized, target-consistent physical `m=3` common-three-space
full-sensor hypotheses with singleton span dimension three, joint rank four,
all three root blocks nonzero, shared-derivative rank eight, and

```text
rank rho=rank pi=rank theta=3.                       (1)
```

In the shared-factor derivative normal form

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),                                 (2)
```

suppose the residual block is one coordinate monomial,

```text
C=lambda e_d tensor e_e,             lambda!=0.     (3)
```

Then necessarily

```text
w_d=w_e=0.                                             (4)
```

Consequently, if `d!=e`, then `w` is proportional to the unique third
coordinate vector.  If `d=e`, then `w` lies in the complementary coordinate
plane.  The tangent-plane condition in (2) also gives

```text
x is not proportional to e_d,
y is not proportional to e_e.                        (5)
```

The proof uses the **complete** empty-target identity.  Because the third
row is injective, the four-dimensional joint preimage is a graph over the
third root space.  Contracting its three singleton generators by any
`gamma in w^perp` leaves the exact root slice

```text
per(r_i,p_j,q_gamma)-delta_(i=j) gamma_i T_i
  =C_(i,j) S_gamma.                                  (6)
```

If `w_d!=0`, the two colours complementary to `d` give an exact binary
diagonal permanent frame.  The unused row `p_d` annihilates the whole frame.
A new four-space common-zero shift lemma shows that an exact binary frame
cannot have such a nonzero common row.  Hence `w_d=0`.  Root exchange gives
`w_e=0`.

This theorem does not exclude the sharp endpoints in (4).  It does not
handle a nonmonomial residual block, joint rank three, derivative rank seven,
other components or pole strata, higher orders, or all-rank drop.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The graph identity and the exact third-root slice

The derivative syzygy in (2) belongs to `K=image H`.  Since the third row is
injective,

```text
dim ker(pr_3|K)=dim K-rank theta=1,
```

and therefore

```text
ker(pr_3|K)=ker D=span((x,y,0)).                     (7)
```

Choose the unique graph lifts modulo this line,

```text
k_c=(a_c,b_c,e_c) in K,                 c=0,1,2.    (8)
```

Their derivative images `U_c=D(k_c)` form a basis of `U=D(K)`.  Thus the
complete coefficientwise target equation has unique source tensors `S_c`
such that

```text
G_N-J=sum_(c=0)^2 U_c S_c.                          (9)
```

For `gamma in A_3^*`, write

```text
q_gamma=sum_k gamma_k q_k,
S_gamma=sum_k gamma_k S_k.                          (10)
```

If `gamma(w)=0`, contracting (2) in the third root gives

```text
(id tensor id tensor gamma)U_c=gamma_c C.           (11)
```

The same contraction of the physical six-term empty permanent has root
coefficient `per(r_i,p_j,q_gamma)`, while the target diagonal contributes
`delta_(i=j) gamma_i T_i`.  Contracting every root coefficient of (9)
therefore proves (6).  No selected-source specialization or generic-point
replacement has been made.

## 2. An exact binary frame has no nonzero common row in a four-space

We isolate the permanent-incidence statement used below.

### Lemma 1 (four-space binary-frame common-zero obstruction)

Let `E` be a four-dimensional subspace of
`W^*=X^* direct-sum Y^* direct-sum Z^*`.  Suppose two-planes

```text
R=span(r_0,r_1),
P=span(p_0,p_1),
Q=span(q_0,q_1)                                     (12)
```

carry an exact binary diagonal table

```text
per(r_a,p_b,q_c)=
  kappa_a T_a,                         a=b=c,
  0,                                  otherwise,    (13)

kappa_0 kappa_1!=0,                                  (14)
```

where `T_0,T_1` are decomposable and fully transverse.  Then there is no
nonzero `v in E` satisfying

```text
per(R,v,Q)=0.                                       (15)
```

#### Proof

The S2BF intersecting-middle-plane binary obstruction first implies

```text
R intersect P=R intersect Q=P intersect Q=0.        (16)
```

Indeed, if any two of the planes met, they would lie in a three-space, and
the third two-plane would meet that three-space in the four-space `E`.
S2BF would then contradict (13).

Equation (13) also shows that a vector of `P` satisfying (15) is zero, so a
nonzero `v` in (15) lies outside `P`.  Put

```text
B=P+span(v),                         dim B=3.        (17)
```

Dimension gives a nonzero vector in `R intersect B`.  Write it

```text
ell=a p_0+b p_1+c v.                                (18)
```

Here `c!=0` by (16).  If `(a,b)!=(0,0)`, choose scalars
`lambda_0,lambda_1` with

```text
a lambda_0+b lambda_1=c.                            (19)
```

The shifted plane

```text
P_lambda=span(p_0+lambda_0 v,p_1+lambda_1 v)        (20)
```

carries exactly the same table (13), by (15), but contains `ell` and hence
meets `R`.  This contradicts (16) applied to the shifted frame.  Therefore
`a=b=0`, so `v in R`.

Repeating the same dimension argument with `Q intersect B` shows
`v in Q`: a nonzero `P` coefficient would again put the intersection vector
in a shifted plane (20), now contradicting `P_lambda intersect Q=0`.
Thus `v in R intersect Q`, contrary to (16).  QED.

The lemma is a direct incidence consequence of the already independently
audited S2BF obstruction; it does not assert that arbitrary pairwise
transverse binary frames exist.

## 3. A monomial row forces the first endpoint equation

Assume (3), and let `{a,b}` be the two colours complementary to `d`.  Put

```text
R_d=span(r_a,r_b),
P_d=span(p_a,p_b),
Q_w={q_gamma:gamma(w)=0}.                            (21)
```

Injectivity in (1) makes all three spaces in (21) two-dimensional.  If
`w_d!=0`, restriction to the two complementary coordinates is an
isomorphism

```text
w^perp -> K^2,                  gamma |->(gamma_a,gamma_b). (22)
```

Indeed, its kernel would consist of a multiple of `e_d^*`, which belongs to
`w^perp` exactly when `w_d=0`.  Choose the basis
`q'_a,q'_b` of `Q_w` dual to the two coordinates in (22).

For `i in {a,b}`, the monomial row (3) has `C_(i,j)=0` for every `j`.
Equation (6) therefore becomes

```text
per(r_i,p_j,q'_k)=delta_(i=j=k) T_i,
i,j,k in {a,b}.                                     (23)
```

This is an exact binary diagonal frame on `(R_d,P_d,Q_w)`.  The same equation
with `j=d` gives

```text
per(R_d,p_d,Q_w)=0.                                 (24)
```

The vector `p_d` is nonzero because `pi` is injective.  Lemma 1 contradicts
(24).  Hence

```text
w_d=0.                                               (25)
```

## 4. Root exchange gives the second endpoint equation

Exchange roots one and two.  The monomial (3) becomes
`lambda e_e tensor e_d`.  If `w_e!=0`, use the two colours complementary to
`e`, the exact binary frame obtained from the zero columns of `C`, and the
nonzero common row `r_e`.  The same proof gives

```text
w_e=0.                                               (26)
```

Equations (25)--(26) prove (4).  If `d!=e`, a nonzero three-vector with both
coordinates zero lies on the unique third coordinate line.  If `d=e`, it
lies in the complementary coordinate plane.

Finally, a rank-one tensor `e_d tensor e_e` belongs to
`A_1 tensor y+x tensor A_2` exactly when `e_d` lies on `x` or `e_e` lies on
`y`.  The rank-eight hypothesis in (2) excludes that tangent-plane
membership, proving (5).

## 5. Proof-topology consequence

Inside the only remaining rank-four/rank-eight row profile,

```text
fully injective (3,3,3):
  C=lambda e_d tensor e_e:
    w_d!=0 or w_e!=0:                              IMPOSSIBLE;
    w_d=w_e=0:                                     OPEN;
  C nonmonomial:                                   OPEN.

joint-rank-three / derivative-rank-seven cells:    OPEN;
other components and pole strata:                  OPEN;
higher balanced orders / all-rank-drop:             OPEN;
global Krenn--Gu conjecture:                        UNRESOLVED.       (27)
```

For `d!=e`, the monomial survivor is the discrete coordinate pattern

```text
C=lambda e_d tensor e_e,             w proportional e_t,
{d,e,t}={0,1,2}.                                     (28)
```

For `d=e`, the survivor has `w_d=0`.  These endpoints are necessary
conditions, not constructed physical incidences.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_monomial_residual_endpoint_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_monomial_residual_endpoint_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_monomial_residual_endpoint_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_monomial_residual_endpoint_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_monomial_residual_endpoint_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_monomial_residual_endpoint_localization.py
```

The primary replay checks the graph derivative contraction, every ordered
monomial support, both complementary-coordinate isomorphisms, the exact
binary table and common-zero shift trap with SymPy.  The independent
no-import audit reverses tensor indexing, uses standard-library `Fraction`
elimination, and reconstructs all nine ordered monomials and both root
orientations.  The arbitrary-subspace dimension argument and inherited S2BF
binary-frame obstruction are the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Fully-injective third-row-rank-two exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_INVOLVED_ROWS_THIRD_ROW_RANK_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [Intersecting-middle-plane binary obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md#2-a-binary-diagonal-frame-cannot-have-an-arbitrary-middle-intersection)

## Scope boundary

```text
monomial residual away from w_d=w_e=0:              IMPOSSIBLE;
monomial residual at w_d=w_e=0:                     OPEN;
nonmonomial fully injective (3,3,3):                OPEN;
other lower-rank cells / components / poles:        OPEN;
higher balanced orders / all-balanced rank-drop:    OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.      (29)
```
