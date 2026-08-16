# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective nonmonomial-residual coordinate-shared-factor structural-zero exclusion

## Status

**Exact characteristic-zero exclusion of every structural-zero successor in
which at least one shared factor is coordinate.**  Retain the fully-injective
rank-four/rank-eight hypotheses and notation of S2CL--S2CM:

```text
D(a,b,c)=(a tensor y-x tensor b) tensor e_t+C tensor c,
ker D=span((x,y,0)) subset K,                         rank D=8,

R=rho(x^perp),             P=pi(y^perp),
Q=span(q_0,q_1,q_2),       Alt(Q)!=0,                              (1)
```

where `rho,pi,theta` are injective, the **actual** residual block `C` is
nonmonomial, and the complete target gives

```text
M_(r_alpha,p_beta)(q_h)
 =alpha_h beta_h T_h+C(alpha,beta)S_h.                            (2)
```

Here `M_(u,v)(q)=per(u,v,q)`.  Write `lambda_h in Q^*` for the basis
functional `lambda_h(q_l)=delta_(h=l)`, and write `S` for the map
`q_h -> S_h`.

S2CL proves that every mixed zero is structural, and S2CM proves that a
structural mixed zero exists.  This theorem proves

```text
x coordinate or y coordinate
  => no actual-nonmonomial survivor in this cell.                  (3)
```

Together with S2CN, which excludes the successor where both `x,y` are
noncoordinate, this closes the **entire actual-nonmonomial residual branch
of the fully-injective joint-rank-four/derivative-rank-eight cell**.  This is
a scoped local closure.  It does not close other lower-rank cells, other
components or poles, higher orders, or all-rank drop.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. Complete faces and the coordinate normalization

Put

```text
P^(h)_(m,n)=M_(r_m,p_n)(q_h),
F^(h)=P^(h)-E_(h,h)T_h.                                           (4)
```

The complete target identities retained from S2CL are

```text
F^(h)=C S_h,                                      h!=t,
F^(t)=C S_t+sum_l H_l S_l.                                        (5)
```

The tangent matrices `H_l` disappear from the perpendicular contraction
(2), but they are retained in the exceptional `t`-face of (5).

The target and permanent are symmetric under exchange of the first two
roots.  On the actual residual data this exchange carries `C` to `-C^T`, up
to the harmless overall sign convention for the derivative image.  It
preserves actual nonmonomiality, exclusion from the tangent plane, the full
faces (5), and the existence and type of every structural zero pair.  It is
therefore enough to assume

```text
x=e_s.                                                            (6)
```

Let `{i,j}={0,1,2} minus {s}`.  Then

```text
x^perp=span(epsilon_i,epsilon_j),       dim R=dim P=2.             (7)
```

We split according to whether `y_s` vanishes.  These two cases exhaust
every nonzero `y`; no root-torus normalization beyond (6) is used.

## 2. The wall `y_s!=0`: an exact `2 x 2` block

Projection `y^perp -> span(epsilon_i,epsilon_j)` is an isomorphism.  Let
`beta^(i),beta^(j)` be its inverse coordinate basis:

```text
beta^(a)_b=delta_(a=b),                    a,b in {i,j}.            (8)
```

Put

```text
A=r_i,              C_0=r_j,
B=p_(beta^(i)),      D_0=p_(beta^(j)),

C|_(x^perp by y^perp) = [[a,u],[v,b]]                              (9)
```

in these bases.  The restricted block is nonzero because the residual
class is outside the tangent plane.  Equation (2) becomes the complete
rectangle

```text
M_(A,B)   =lambda_i tensor T_i+a S,
M_(A,D_0) =u S,
M_(C_0,B) =v S,
M_(C_0,D_0)=lambda_j tensor T_j+b S.                              (10)
```

A nonzero structural pair must have one first covector supported on `i` or
`j`; its partner is then the complementary vector in (8).  Consequently

```text
structural zeros in (9)
  <=> u=0 or v=0.                                                   (11)
```

S2CM guarantees that at least one equality in (11) holds.

### 2.1 Exactly one cross entry vanishes

Assume `u=0`, `v!=0`; the other orientation is symmetric.  Thus `(A,D_0)`
is a zero pair and `M_(C_0,B)=vS` is a physical realization of the source
map.

If `A,D_0` are independent, S2CG makes their span a split two-source plane.
Every permanent of three rows of `Q` then has one fixed omitted-source
factor.  In particular the three physical maps in

```text
v M_(A,B)-a M_(C_0,B)=v lambda_i tensor T_i,
v M_(C_0,D_0)-b M_(C_0,B)=v lambda_j tensor T_j                  (12)
```

have that factor.  Evaluating at `q_i,q_j` makes `T_i,T_j` share it,
contrary to their full transversality.

If `A,D_0` are dependent, their common row is pure by the square-zero branch
of S2CG.  Both `M_(A,B)` and `M_(C_0,D_0)` have that pure factor.  When
`ab!=0`, the source terms cancel in

```text
b M_(A,B)-a M_(C_0,D_0)
 =b lambda_i tensor T_i-a lambda_j tensor T_j,                    (13)
```

and evaluation at `q_i,q_j` again makes the transverse targets share a
factor.  The case `a=b=0` is immediate from the two maps separately.

Suppose next that `a=0,b!=0`.  Set

```text
B'=D_0-(b/v)B.                                                     (14)
```

Then

```text
M_(A,B')=-(b/v)lambda_i tensor T_i,
M_(C_0,B')=lambda_j tensor T_j.                                   (15)
```

The planes `span(A,C_0)` and `span(D_0,B')` are still two-dimensional.
Applied to the zero corner `(A,D_0)`, S2CK's zero-corner rectangle lemma
forbids the two fully transverse rank-one maps in (15).  If `a!=0,b=0`, use

```text
A'=A-(a/v)C_0
```

and the maps `M_(A',D_0)=-(a/v)lambda_j tensor T_j` and
`M_(A',B)=lambda_i tensor T_i`.  This exhausts the one-cross-entry wall.

### 2.2 Both cross entries vanish

Assume `u=v=0`.  If `ab!=0`, use the zero pair `(A,D_0)`.  In its independent
branch every physical mixed map has the fixed omitted-source factor; in its
dependent branch the two diagonal maps have the common pure factor.  In
either branch (13) forces `T_i,T_j` to share that factor, a contradiction.

It remains to treat a rank-one diagonal block.  By symmetry take

```text
a!=0,                         b=0.                                 (16)
```

The two cross pairs `(A,D_0)` and `(C_0,B)` are zero, while

```text
M_(C_0,D_0)=lambda_j tensor T_j!=0.                               (17)
```

S2CI's two-cross incidence dichotomy gives exactly one of

```text
(i)  Q is split across three pure source lines aligned with T_j;

(ii) R=P=H is a split two-source plane,
     H=ker lambda_j, aligned with the two used factors of T_j.     (18)
```

In (i), every `q_h` is a sum of the three aligned pure rows.  In (ii),
`q_s,q_i in H`.  Quotient all three physical source factors by the factor
lines of `T_j`.  In either fork the **complete** slices `P^(s),P^(i)` die.
The first map in (10) gives

```text
bar S_s=0,
bar S_i=-a^(-1)bar T_i.                                           (19)
```

If `t!=s`, the retained `s`-face in (5) becomes

```text
-E_(s,s)bar T_s=C bar S_s=0,                                     (20)
```

which is impossible.  If `t=s`, use the retained `i`-face:

```text
-E_(i,i)bar T_i=C bar S_i=-a^(-1)C bar T_i.                       (21)
```

Since `bar T_i!=0`, (21) gives the identity of actual root matrices

```text
C=a E_(i,i),                                                       (22)
```

contrary to actual nonmonomiality.  The other rank-one diagonal block gives
`C=b E_(j,j)`.  Thus every `y_s!=0` wall is empty.

## 3. The wall `y_s=0`: the map-`S` zero pair

Now `e_s in y^perp`.  The functional

```text
L=C(-,e_s)|_(x^perp)                                               (23)
```

is nonzero.  Otherwise every row of the two-plane `R` would pair to zero
with the nonzero row `p_s`, contradicting S2CG's radical-line bound.

Choose `alpha_0,alpha_1 in x^perp` with

```text
L(alpha_0)=0,                     L(alpha_1)=1,                    (24)
```

and let `eta` span `y^perp/Ke_s`.  Put

```text
U=r_(alpha_0),       V=p_s,
A=r_(alpha_1),       B=p_eta,

a=C(alpha_0,eta),    b=C(alpha_1,eta).                             (25)
```

Then the exact table is

```text
M_(U,V)=0,                           S=M_(A,V),

M_(U,B)=sum_h alpha_(0,h)eta_h lambda_h tensor T_h+aS,
M_(A,B)=sum_h alpha_(1,h)eta_h lambda_h tensor T_h+bS.             (26)
```

We split according to the support of `y` in the complementary coordinate
plane.

## 4. Noncoordinate `y` on the `y_s=0` wall

Assume `support y={i,j}`.  Then `eta_i eta_j!=0`, and only the `i,j` target
terms occur in (26).

If `U,V` are independent, S2CG gives a common omitted-source factor for
every physical mixed map.  Subtract `aS,bS` from the last two maps in (26).
The coefficient matrix

```text
[[alpha_(0,i)eta_i, alpha_(0,j)eta_j],
 [alpha_(1,i)eta_i, alpha_(1,j)eta_j]]                              (27)
```

is invertible.  Hence both `lambda_i tensor T_i` and
`lambda_j tensor T_j` have the common factor, impossible.

Suppose `U,V` are dependent.  Their common row is pure; call its factor line
`Ku`.  The maps `S=M_(A,V)` and `M_(U,B)` have that factor.  If
`alpha_(0,i)alpha_(0,j)!=0`, subtracting `aS` from the latter gives a
two-target secant whose two targets both have factor `u`, again impossible.

It remains, up to exchanging `i,j`, that `alpha_0` is proportional to
`epsilon_i`.  Add a multiple of `alpha_0` to `alpha_1` so that
`alpha_1` is a nonzero multiple of `epsilon_j`; (24) remains valid.  Replace
`B` by

```text
B'=B-bV.                                                           (28)
```

After retaining the nonzero coordinate scalars, (26) reads

```text
M_(A,B')=c_j lambda_j tensor T_j,               c_j!=0,
M_(U,B')=c_i lambda_i tensor T_i+aS,             c_i!=0.           (29)
```

The second identity minus `aS` puts the relevant factor line of `T_i` on
`Ku`.  Evaluate it at `U`: both permanents with the repeated pure row and
`S(U)` vanish, so `lambda_i(U)=0`.  Next use permanent symmetry:

```text
M_(A,B')(U)=M_(U,B')(A).                                           (30)
```

The left side belongs to the `T_j` line; the right side has the `u` factor.
Since `T_i,T_j` are fully transverse and the `T_i` factor is `u`, the two
subspaces meet only in zero.  Thus `lambda_j(U)=0`.  Therefore

```text
U in ker lambda_i intersect ker lambda_j=Kq_s.                     (31)
```

Quotient the physical source containing `u` by `Ku`.  Every `S_h` dies
because `S=M_(A,V)` and `V` is proportional to `u`; the **complete** slice
`P^(s)` dies because `q_s` itself is proportional to the pure row `u`.
If `s!=t`, the retained `s`-face gives (20).  If `s=t`, the exceptional face
in (5) has right side

```text
C S_s+sum_l H_l S_l,
```

and every term still dies.  Its left side is `-E_(s,s)bar T_s`, again
impossible.  This closes noncoordinate `y` on the wall.

## 5. Coordinate `y`: the exact rank split

It remains that

```text
y=e_r,                         {s,r,k}={0,1,2}.                    (32)
```

Use rows `(epsilon_r,epsilon_k)` of `x^perp` and columns
`(epsilon_s,epsilon_k)` of `y^perp`, and write

```text
C|_(x^perp by y^perp)=[[a,b],[c,d]].                               (33)
```

The first column is nonzero, or `p_s` has the whole plane `R` in its
radical.  The first row is nonzero, or `r_r` has the whole plane `P` in its
radical.  We now exhaust the rank and the entry `a`.

### 5.1 Rank one

If `rank (33)=1`, then `a!=0`: otherwise the two radical-line conditions
give `b,c!=0`, contradicting `det (33)=0`.  In the displayed row and column
bases put

```text
alpha=(c,-a),                 beta=(b,-a).                          (34)
```

The pairs `(r_alpha,p_s)` and `(r_r,p_beta)` are structural zeros and form
bases of `R,P`.  Rank one also gives

```text
M_(r_alpha,p_beta)=a^2 lambda_k tensor T_k.                         (35)
```

S2CI gives a split three-source `Q` aligned with `T_k`, or an equal split
plane `R=P=H=ker lambda_k`.  Quotient the three factor lines of `T_k`.  For
`h=s,r`, the complete slice `P^(h)` dies.  Since

```text
M_(r_r,p_s)=aS,                                                     (36)
```

also `bar S_s=bar S_r=0`.  Choose

```text
h in {s,r},                         h!=t.                           (37)
```

The retained face and its diagonal coefficient both give

```text
-E_(h,h)bar T_h=0,                                                 (38)
```

impossible.

### 5.2 Rank two with `a!=0`

Let

```text
Delta=ad-bc!=0.                                                     (39)
```

The same two pairs from (34) are structural zeros.  Direct evaluation gives

```text
M_(r_alpha,p_beta)=a^2 lambda_k tensor T_k+a Delta S,
M_(r_r,p_s)=aS,                                                     (40)
```

and hence

```text
M_(r_alpha,p_beta)-Delta M_(r_r,p_s)
 =a^2 lambda_k tensor T_k.                                        (41)
```

The right side of (41) is nonzero, so at least one of the two diagonal maps
in its left side is nonzero and S2CI's two-cross incidence proof applies.
In either its split-`Q` or equal-split-plane fork, all diagonal maps lie in
the same aligned decomposable slab; equation (41) then identifies that slab's
three factor lines with those of `T_k`.  The quotient and retained colour
(37) therefore give the same contradiction (38).

### 5.3 Rank two with `a=0`: independent zero row

Now `b,c!=0`, and the exact table is

```text
u=r_r,               v=p_s,               A=r_k,      B=p_k,

M_(u,v)=0,
M_(u,B)=bS,
M_(A,v)=cS,
M_(A,B)=lambda_k tensor T_k+dS.                                  (42)
```

First suppose `u,v` are independent.  Write their S2CG normal form as

```text
u=x_0+y_0,              v=mu(x_0-y_0),
H=span(x_0,y_0),
```

with omitted source `Z`.  Symmetry with the zero pair gives

```text
S(u)=S(v)=0.                                                       (43)
```

Thus `M_(u,B)=bS` vanishes on `H`.  Evaluating it at the two pure generators
`x_0,y_0` forces `B_Z=0`.  The symmetric argument using `M_(A,v)=cS`
forces `A_Z=0`.  The projection `Q -> Z` is nonzero with kernel `H`, so

```text
A,B in H,                    R=P=H.                                (44)
```

The map `S` is nonzero; otherwise `u` would have the two-plane `P` in its
radical.  Equation (42) now puts `H` in `ker lambda_k`, and dimensions give

```text
H=ker lambda_k.                                                     (45)
```

All maps made from two rows of `H` have the same decomposable image line
`x_0 tensor y_0 tensor z_0`; (42) aligns it with `T_k`.  The full `T_k`
triple quotient therefore legitimately kills `P^(s),P^(r)`, while (43)
gives `S_s=S_r=0`.  The retained colour (37) again yields (38).

### 5.4 Rank two with `a=0`: dependent pure row

Finally suppose the zero pair in (42) is dependent.  Rescale it as

```text
u in X pure,                       v=rho u,       rho!=0.           (46)
```

The adjacent maps in (42) give

```text
M_(u,A-(c/(rho b))B)|Q=0.                                          (47)
```

S2CG's radical-line uniqueness for the pure row `u` makes the row in (47)
proportional to `u`.  Hence

```text
R=P=H=span(u,A).                                                    (48)
```

Set

```text
B'=B-(d/c)v.                                                       (49)
```

Then

```text
M_(A,B')=lambda_k tensor T_k,
B'=lambda A+mu u,                         lambda!=0.                (50)
```

Write `A=A_X+A_Y+A_Z` in the three physical sources.

If `A_Y=0`, then `A_Z!=0` and `H subset X direct-sum Z`.  The map in (50)
vanishes on `H`, so `H=ker lambda_k`, and its `Z` factor is the line
`KA_Z`.  Thus `q_s,q_r in H` and

```text
S_s=S_r=0.                                                         (51)
```

Choose `h` as in (37), but use only the diagonal retained coefficient

```text
P_(h,h,h)-T_h=C_(h,h)S_h.                                         (52)
```

One of `r_h,p_h` is the pure row `u`: it is `p_s=v` when `h=s`, and `r_r=u`
when `h=r`.  In every nonzero term of `P_(h,h,h)`, that row occupies source
`X`, so `q_h` must occupy the non-`X` factor of `H`, namely `KA_Z`.
Quotienting `Z/KA_Z` kills `P_(h,h,h)`.  It also kills the right side by
(51), whereas `T_h` survives by transversality with `T_k`.  This contradicts
(52).  If `A_Z=0`, use the symmetric quotient `Y/KA_Y`.

It remains that `A_Y,A_Z` are both nonzero.  From (50), exact polarization
at `u` and `A` gives

```text
M_(A,B')(u)=2 lambda u tensor A_Y tensor A_Z,

M_(A,B')(A)
 =(6 lambda A_X+2 mu u) tensor A_Y tensor A_Z.                     (53)
```

The first line is nonzero and aligns the corresponding factor of `T_k`
with `Ku`.  Since the entire map has the one decomposable image line, the
second line forces

```text
A_X in Ku.                                                         (54)
```

For arbitrary `q in Q`, project (50) in source `X` modulo `Ku`.  Using (54),
the only surviving term is

```text
2 lambda (q_X mod Ku) tensor A_Y tensor A_Z=0.                     (55)
```

Therefore

```text
pr_X(Q)=Ku.                                                        (56)
```

Again use the diagonal coefficient (52), not the whole slice.  Its pure row
`r_r=u` or `p_s=rho u` forces every term to contain the `X` factor `u`, so
the quotient `X/Ku` kills `P_(h,h,h)`.  It kills `S_h` for the same reason,
while the fully transverse `T_h` survives.  Equation (52) is impossible.
This exhausts the rank-two `a=0` wall.

## 6. Proof-scope correction

Two stronger exploratory quotient statements are expressly **retracted**
and are not used above:

1. a single fixed projection line of `Q` does not by itself kill an entire
   physical slice `P^(h)`, because `r_s` or `p_r` may lie outside `Q` and
   supply that source;
2. `pr_X(Q)=Ku` likewise does not by itself kill every entry of `P^(h)`.

Full-slice vanishing is invoked only in the aligned split-space or split-plane
forks, where the particular row `q_h` has all its components on the three
quotiented target lines.  In Sections 5.3--5.4, the repaired argument uses
either that aligned conclusion or only the diagonal coefficient (52), whose
known pure row supplies the needed factor.  These are load-bearing scope
restrictions.

## 7. Conclusion and proof topology

Sections 2--5 exclude every point with `x=e_s`.  Exchanging the first two
roots excludes every point with coordinate `y`.  Thus (3) holds.

S2CL, S2CM, S2CN, and this theorem now give the exact chain

```text
actual nonmonomial residual
  -> correcting zero / zero-pair-free / structural zero;

correcting zero:                         impossible (S2CL),
zero-pair-free:                          impossible (S2CM),
structural, both factors noncoordinate:  impossible (S2CN),
structural, a coordinate shared factor:  impossible (this theorem).

Therefore the fully-injective rank-four/rank-eight
actual-nonmonomial residual branch is closed.                       (57)
```

This theorem is analytic.  Its uses of S2BQ, S2CG, S2CI, and S2CK retain
their stated hypotheses and scopes; no finite support replay is substituted
for those inputs.

## 8. Exact replay and independent audit

The focused primary replay is

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_coordinate_shared_factor_structural_zero_exclusion.py
```

It checks all six colour permutations and both root orientations, the complete
`8+3` cross-zero matrix atlas on `y_s!=0`, both retained-face quotient signs,
the independent/full-dependent/singleton-dependent `y_s=0` noncoordinate
interfaces, all three coordinate-`y` matrix-rank branches, and the repaired
rank-two zero-corner pure-row pencil.

The no-import audit is

```text
python -B -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_coordinate_shared_factor_structural_zero_exclusion.py
```

It uses standard-library `Fraction` arithmetic, reverses the root, colour,
matrix, and retained-face traversals, implements its own bilinear-map and rank
interfaces, checks 5,625 root-exchange fixtures and 580 admissible coordinate
matrices, and separately replays the two repaired pencil quotients.  Both
scripts explicitly leave the S2CG, S2CI, and S2CK source-support theorems to
the analytic proof.

## Dependencies

- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Canonical-binomial zero-pair geometry](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)
- [Same-coordinate one-visible two-cross incidence dichotomy](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_SAME_COORDINATE_ONE_VISIBLE_WALL_EXCLUSION_THEOREM.md)
- [Diagonal two-visible mixed-map and zero-corner obstructions](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_TWO_VISIBLE_CELL_EXCLUSION_THEOREM.md)
- [Nonmonomial complete-target zero-pair localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_COMPLETE_TARGET_ZERO_PAIR_LOCALIZATION_THEOREM.md)
- [Nonmonomial zero-pair-free-cell exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_ZERO_PAIR_FREE_CELL_EXCLUSION_THEOREM.md)
- [Noncoordinate shared-factor structural-zero exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_NONCOORDINATE_SHARED_FACTORS_EXCLUSION_THEOREM.md)

## Scope boundary

```text
fully-injective rank-four/rank-eight actual nonmonomial residual:
  correcting mixed zeros:                               IMPOSSIBLE (S2CL);
  zero-pair-free cell:                                  IMPOSSIBLE (S2CM);
  both shared factors noncoordinate:                    IMPOSSIBLE (S2CN);
  x coordinate or y coordinate structural cells:       IMPOSSIBLE;
  complete actual-nonmonomial residual branch:          CLOSED;

other lower-rank cells / components / poles:             OPEN;
higher balanced orders / all-balanced rank drop:         OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED.       (58)
```
