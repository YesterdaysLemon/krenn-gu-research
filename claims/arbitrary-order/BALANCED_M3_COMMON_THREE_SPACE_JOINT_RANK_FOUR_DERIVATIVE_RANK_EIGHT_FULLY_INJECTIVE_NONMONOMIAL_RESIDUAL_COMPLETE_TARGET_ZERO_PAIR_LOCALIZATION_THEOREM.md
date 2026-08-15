# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective nonmonomial-residual complete-target zero-pair localization

## Status

**Exact characteristic-zero complete-target normal form and zero-pair
localization for every actual nonmonomial residual block in the remaining
fully-injective `(3,3,3)` row profile.**  Retain the normalized physical
common-three-space full-sensor hypotheses

```text
dim U=3,                    K=image H=D^(-1)(U),     dim K=4,
D(K)=U,                     rank D=8,
rank rho=rank pi=rank theta=3.                                      (1)
```

In the S2BQ shared-factor chart, write

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
N=ker D=span((x,y,0)) subset K,
C notin A_1 tensor y+x tensor A_2.                                  (2)
```

Assume that the **actual** residual block `C` is nonmonomial.  The S2BQ
root-torus gate then makes `w` coordinate.  After rescaling the shared
factors, fix

```text
w=e_t.                                                              (3)
```

Explicitly, if the original factor is `w=omega e_t`, `omega!=0`, replace
`(x,y,w)` by `(omega x,omega y,e_t)`.  This leaves `D`, the kernel line, and
the actual block `C` unchanged.

The complete target has an exact three-slice rank-one normal form.  On the
two perpendicular row planes

```text
R=rho(x^perp),                 P=pi(y^perp),
Q=image theta=span(q_0,q_1,q_2),                                    (4)
```

it gives the corrected cube

```text
M_(r_alpha,p_beta)(q_k)
 =alpha_k beta_k T_k+C(alpha,beta)S_k,
M_(u,v)(q)=per(u,v,q),                                               (5)
```

and the physical full-sensor determinant gives `Alt(Q)!=0`.

If a nonzero pair `(alpha,beta) in x^perp by y^perp` is a mixed zero pair,
meaning that the map in (5) vanishes on all of `Q`, then it is necessarily a
**structural** zero:

```text
C(alpha,beta)=0,                 alpha_k beta_k=0 for every k.        (6)
```

Projectively, every structural zero belongs to an explicit union of at most
four points.  Every apparent positive-dimensional coordinate shore is
excluded by S2CG's radical-line bound.  A zero pair with
`C(alpha,beta)!=0` would instead be a **correcting** zero.  The complete
target, the order-three permanent-rank obstruction, S2CK's mixed-map
obstruction, and one retained uncorrected slice exclude every such pair,
including all coordinate `x` or `y` walls.

This theorem does not assert that a zero pair exists.  It leaves two honest
successors: the finite structural-zero cells in (6), and the zero-pair-free
cell.  It does not exclude every nonmonomial residual, any lower-rank target
cell, another component or pole stratum, a higher order, or all-rank drop.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The complete three-slice normal form

Third-row injectivity and `N subset K` give

```text
ker(pr_3|K)=N.                                                       (7)
```

Choose graph lifts, unique modulo `N`,

```text
k_s=(a_s,b_s,e_s) in K,                          s=0,1,2,
H_s=a_s tensor y-x tensor b_s,
U_s=D(k_s)=H_s tensor e_t+C tensor e_s.                             (8)
```

The three `U_s` form a basis of `U`.  Hence there are unique source tensors
`S_s` with

```text
G_N-J=sum_s U_s S_s.                                                 (9)
```

Put

```text
P^(k)_(i,j)=M_(r_i,p_j)(q_k),
F^(k)=P^(k)-E_(k,k) T_k.                                            (10)
```

Reading the third-root coefficient of (9) gives the **complete** identities

```text
F^(k)=C S_k,                                      k!=t,
F^(t)=C S_t+sum_s H_s S_s.                                          (11)
```

Equivalently, after the other tangent columns are removed,

```text
F^(t)-sum_(s!=t) H_s S_s=(C+H_t)S_t.                                (12)
```

The root factor in (12) is nonzero: `H_t` lies in
`A_1 tensor y+x tensor A_2`, whereas (2) says that `C` does not.  No divisor
or pivot was introduced.

Changing a graph lift by the kernel generator sends

```text
a_s -> a_s+zeta_s x,              b_s -> b_s+zeta_s y,
```

and leaves every `H_s` unchanged.  Thus (11)--(12) are graph-gauge
invariant.  They retain the tangent entries that disappear from (5).

## 2. The alternating physical three-space and the corrected cube

Let `L=N^perp`.  Since `N subset K`,

```text
K^perp subset L,                  dim L=8,
dim K^perp=5,                     dim H^T(L)=3.                       (13)
```

Every third-root covector lies in `L`, so `Q subset H^T(L)`.  Third-row
injectivity makes both spaces three-dimensional and therefore

```text
Q=H^T(L).                                                           (14)
```

The quotient maps

```text
H_bar:W -> K/N,                    D_bar:K/N -> U
```

are respectively onto and an isomorphism.  The separated determinant of
the physical singleton map `D_bar H_bar` is a nonzero scalar multiple of the
alternating tensor of any basis of `H^T(L)`.  Full-sensor rank therefore
gives the inherited load-bearing premise

```text
Alt(Q)!=0.                                                          (15)
```

For `alpha in x^perp`, the root covector `(alpha,0,0)` belongs to `L`; hence
`r_alpha in Q`.  Similarly `p_beta in Q` for `beta in y^perp`.  Injectivity
of `rho,pi` gives

```text
dim R=dim P=2.                                                       (16)
```

Contract (11) by `alpha in x^perp` and `beta in y^perp`.  Every tangent
column vanishes because

```text
H_s(alpha,beta)
 =alpha(a_s)beta(y)-alpha(x)beta(b_s)=0.                             (17)
```

The target coefficient is `alpha_k beta_k T_k`; this proves (5) for every
`k`, including `k=t`.  The cube is an exact consequence of the complete
faces, not a converse to them.

## 3. Structural zeros form an exact finite atlas

Let `(alpha,beta)` be a mixed zero pair and put

```text
c=C(alpha,beta).                                                     (18)
```

If `c=0`, the three independent nonzero target tensors in (5) give

```text
alpha_k beta_k=0,                          k=0,1,2.                  (19)
```

For `j=1,2`, let `epsilon_a^(j)` denote the `a`-th coordinate covector in
`A_j^*`, and put

```text
Z_a^(j)={zeta in A_j^*:zeta_a=0}.
```

The supports of the two nonzero covectors in (19) are disjoint subsets of a
three-element set, so at least one is a singleton.  Consequently the complete
projective structural-zero locus is

```text
Z_str=
 union_(a:x_a=0)
   { [epsilon_a^(1)] } by
   P(y^perp intersect Z_a^(2)
       intersect ker C(epsilon_a^(1),-))

 union

 union_(b:y_b=0)
   P(x^perp intersect Z_b^(1)
       intersect ker C(-,epsilon_b^(2)))
   by { [epsilon_b^(2)] }.                                           (20)
```

Every point of the displayed union satisfies `c=0` and (19), so (20) is an
equality, not merely a cover.

Fix one first-root shore in (20).  If its partner vector space had dimension
at least two, then injectivity of `pi` would put a two-plane in

```text
Rad_Q(r_(epsilon_a^(1)))
 ={p in Q:M_(r_(epsilon_a^(1)),p)|Q=0}.                              (21)
```

The row `r_(epsilon_a^(1))` is nonzero by injectivity of `rho`.  S2CG's
coordinate-free consequence of (15) says every such radical has dimension
at most one.  Thus each first-root shore in (20) contributes at most one
projective point.  The root-exchanged argument handles every second-root
shore.  Since a nonzero three-coordinate vector has at most two zero
coordinates,

```text
# Z_str <=(3-|support x|)+(3-|support y|)<=4.                         (22)
```

In particular, if both `x` and `y` are fully supported, `Z_str` is empty.
No multiplicity or scheme-length assertion is made in (22); it counts the
underlying projective zero pairs relevant to the incidence argument.

## 4. A correcting zero forces a diagonal tangent-quotient pivot

Assume for contradiction that `c!=0`.  Equation (5) gives

```text
S_k=-mu_k T_k,                    mu_k=alpha_k beta_k/c.              (23)
```

Substitution in (9) writes the physical empty permanent as

```text
G_N=sum_k A_k T_k,
A_k=E_(k,k,k)-mu_k U_k.                                             (24)
```

Suppose all three root tensors `A_k` were nonzero.  Their three trilinear
root polynomials have a common nonvanishing evaluation over the infinite
characteristic-zero field.  Evaluating (24) there produces

```text
lambda_0 T_0+lambda_1 T_1+lambda_2 T_2,
lambda_0 lambda_1 lambda_2!=0.                                      (25)
```

Every one-mode flattening of (25) has rank three.  Therefore all three local
maps from the order-three permanent tensor `P_3` are invertible.  They would
preserve tensor rank, contradicting

```text
tensor-rank(P_3)=4,             tensor-rank((25))=3.                 (26)
```

This is the exact S2R rank obstruction used in S2CB.  Hence `A_s=0` for some
colour `s`.  Necessarily `mu_s!=0`.  If `s!=t`, comparison of the independent
third-root factors `e_s,e_t` in

```text
E_(s,s) tensor e_s
 =mu_s(H_s tensor e_t+C tensor e_s)                                 (27)
```

gives

```text
H_s=0,                         C=mu_s^(-1)E_(s,s).                   (28)
```

This makes the actual `C` monomial, contrary to the standing branch.
Therefore `s=t`, and for `nu=mu_t^(-1)` one has

```text
C+H_t=nu E_(t,t),
C(a,b)=nu a_t b_t                  on x^perp by y^perp,
alpha_t beta_t!=0.                                                   (29)
```

Scale `alpha,beta` so that `alpha_t=beta_t=1`.  Combining (23) and (29),
the whole corrected cube becomes

```text
M_(r_a,p_b)(q_k)=B_k(a,b)T_k,
B_k(a,b)=a_k b_k-alpha_k beta_k a_t b_t,
B_t=0.                                                               (30)
```

## 5. The correcting cube has exactly one target colour

Fix two colours `i,j`.  Quotient each of the three physical source factors
by the corresponding factor line of the third target tensor, and put bars on
the images of `r_a,p_b,Q` and `M`.  The remaining images of `T_i,T_j` are
nonzero and fully transverse.  If for some `(a,b)` both `B_i(a,b)` and
`B_j(a,b)` were nonzero, the projected mixed map

```text
M_(bar(r_a),bar(p_b))(bar(Q))
```

would lie in the span of those two transverse decomposable tensors and
contain both.  This contradicts S2CK's two-transverse mixed-map lemma.
Therefore

```text
B_i(a,b)B_j(a,b)=0                 for every (a,b).                  (31)
```

The coordinate ring of the affine space `x^perp by y^perp` is a domain.
Thus (31) says that at most one of the three bilinear forms `B_k` is nonzero.
They cannot all vanish: otherwise every nonzero row in `R` would have the
two-plane `P` in its radical, contradicting (15) and S2CG.  Hence exactly one
form, say `B_l`, is nonzero.  Moreover,

```text
rank B_l=2.                                                           (32)
```

Indeed, a rank-one form has a nonzero left-kernel row, whose mixed map again
vanishes on the whole two-plane `P`.

Let `lambda_l in Q^*` be defined by `lambda_l(q_j)=delta_(l,j)` and put

```text
H=ker lambda_l.                                                       (33)
```

Transporting `B_l` through the injective row maps, (30) reads

```text
M_(r,p)(q)=B_l(r,p)lambda_l(q)T_l,
r in R,                       p in P,                 q in Q.        (34)
```

For `r,r' in R` and `p in P`, permanent symmetry gives

```text
B_l(r,p)lambda_l(r')=B_l(r',p)lambda_l(r).                            (35)
```

If `lambda_l|R` were nonzero, take a nonzero row in its kernel and a row on
which it is nonzero.  Equation (35) would put the first row in the left
kernel of `B_l`, contradicting (32).  Thus `R subset H`.  Root exchange gives
`P subset H`, and dimensions yield

```text
R=P=H.                                                               (36)
```

On this common plane `B_l` is symmetric and nondegenerate.  Choose
`h in H` with `B_l(h,h)!=0`, and choose a nonzero `h'` on its orthogonal
line.  Then `h,h'` are independent and

```text
M_(h,h')|Q=0.                                                        (37)
```

S2CG's zero-pair lemma makes `H` a split two-source plane.  Evaluation of
`M_(h,h)(q_l)=B_l(h,h)T_l` aligns its two pure source lines and the omitted
component of `q_l` with the three factor lines of `T_l`.

## 6. One retained full slice excludes the correcting zero

Since `B_t=0`, the surviving colour `l` is not `t`.  Let `k` be the third
colour, distinct from both `l` and `t`.  Then

```text
k!=t,                            q_k in H.                            (38)
```

Quotient the three physical source factors by the three factor lines of
`T_l`.  Every term of `M_(r_i,p_j)(q_k)` contains one of the two pure lines
of the split plane `H`, so

```text
bar(P^(k))=0,                    bar(T_k)!=0.                         (39)
```

Because `k!=t`, the complete retained face in (11), not merely the corrected
cube, is

```text
P^(k)-E_(k,k)T_k=C S_k
                   =-mu_k C T_k.                                   (40)
```

Applying the quotient and using (39) gives

```text
-E_(k,k) bar(T_k)=-mu_k C bar(T_k),
E_(k,k)=mu_k C.                                                       (41)
```

If `mu_k=0`, (41) is already impossible.  If `mu_k!=0`, it makes the actual
residual block `C` a diagonal coordinate monomial.  Both alternatives
contradict the remaining nonmonomial branch.  Therefore

```text
C(alpha,beta)!=0 mixed zero pairs:              IMPOSSIBLE.         (42)
```

Together, (20), (22), and (42) prove the stated zero-pair localization.

## 7. Evidence and proof ownership

The primary symbolic replay checks the graph coefficients, gauge invariance,
the corrected cube, the structural support cover, the correcting rank-fork
interfaces, the one-target bilinear reduction, and the final complete-slice
coefficient comparison.  The independent standard-library audit reconstructs
the same interfaces using separate exact rational arithmetic and reversed
traversal.  These scripts replay algebraic interfaces; they do not replace
the analytic S2R tensor-rank theorem, S2CG zero-pair/radical classification,
S2CK mixed-map lemma, or the written source-quotient argument.

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_complete_target_zero_pair_localization.py
python -B -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_complete_target_zero_pair_localization.py
```

## Dependencies

- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Rank-four/rank-eight target-row atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Canonical-binomial residual exclusion and general zero-pair geometry](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)
- [Diagonal two-visible-cell exclusion and mixed-map lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_TWO_VISIBLE_CELL_EXCLUSION_THEOREM.md)
- [Order-three permanent-rank obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)

## Scope boundary

```text
fully-injective rank-four/rank-eight actual nonmonomial residual:
  complete three-slice normal form:                         PROVED;
  correcting mixed zero pairs:                             IMPOSSIBLE;
  structural mixed zero pairs:                             AT MOST FOUR;
  zero-pair-free cell:                                     OPEN;
  structural-zero cells after localization:                OPEN;

monomial residual branch:                                  CLOSED (S2CC--S2CK);
other lower-rank cells / components / poles:                OPEN;
higher balanced orders / all-balanced rank drop:            OPEN;
global Krenn--Gu conjecture:                                UNRESOLVED.       (43)
```
