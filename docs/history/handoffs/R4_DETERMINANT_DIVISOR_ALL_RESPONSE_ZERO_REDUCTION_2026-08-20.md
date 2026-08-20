# Four-root determinant-divisor all-pair-response-zero reduction

Date: 2026-08-20
Discovery base: `origin/main` at `df394d387d246d4331359a9ce0f16d7700f724bb`
Status: **research provenance for a candidate theorem package; not itself a theorem**
Strategic node: **OPEN**
Global Krenn--Gu status: **UNRESOLVED**

## 1. Purpose and non-integration notice

This note records a support-free attack on the determinant divisor left open
by the full-rank GLS9 localization.  It treats the literal vanishing of all
six same-`Q` pair-response tensors at root order four and stratifies the
remaining cases by

```text
rank H_Q = 0, 1, 2.
```

The main new candidate result is that every rank-two point satisfying the
declared source, maximum-root, response, and complete-target hypotheses is
forced into one coordinate-free `2 x 2` double-contained core.  All
rank-two quotient-escape branches are excluded.  Rank one has an exhaustive
three-branch normal-form cover but is not excluded.

This document records the discovery derivation and the exact branch ledger.
The owning statement is now the candidate
[determinant-divisor rank reduction](../../../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md),
whose proof, verifier, independent audit, and later hostile review determine
the live status.  This handoff does not independently prove that theorem and
must not be cited in place of it.  Nothing here is a witness or counterexample.
The strategic node and global status do not change merely because this
provenance note exists.

The tracked source packages used for conventions and hypotheses are:

- [GLS4 same-pair source theorem](../../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md);
- [GLS7 four-root source cover](../../../claims/arbitrary-order/FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md);
- [GLS8 promoted target reduction](../../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md);
- [GLS9 full-rank localization](../../../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md); and
- [maximum-root saturation](../../../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md).

The repository operating contract remains authoritative.  In particular,
the distinctions between a proved theorem, candidate reduction, experiment,
and global resolution in [`AGENTS.md`](../../../AGENTS.md) are retained.

## 2. Quantified hypotheses and labelled convention

The actual-witness application begins over `C`.  The linear-algebraic
arguments below work over any characteristic-zero field `K` once all the
displayed hypotheses are supplied.  Maximum-root statements use that `K` is
infinite and, for the actual source, algebraically closed.

Let

```text
Omega = R disjoint-union B,      |R|=4,      |B|=6,
Q={q_0,q_1} subset B,            U=B-Q={u_0,u_1,u_2,u_3}.       (1)
```

Every local covector space has dimension three.  Write

```text
X=V_(q_0)^*,        Y=V_(q_1)^*,        P_u=V_u^*.             (2)
```

The set `R`, with fully supported vectors `x_r`, is a
maximum-cardinality torus root.  Thus no five-vertex torus root exists
anywhere in `Omega`, not merely no extension of the fixed vectors `x_R`.

The pair `Q` is the **same pair supplied by GLS4**.  In particular,

```text
H=H_Q=W_(q_0,q_1) != 0,             Pi_Q != 0.                  (3)
```

GLS4 also supplies individual higher-column quotient survival and a fully
supported raw incidence `p_(A,Q)!=0`.  Those stronger facts remain part of
the source package but are not used in the arbitrary-point implications
below.  They must not be inferred for any sharpness control unless checked
separately.

For each `u in U`, and each distinct `u,v in U`, put

```text
A_u=W_(q_0,u) in X tensor P_u,
C_u=W_(q_1,u) in Y tensor P_u,
B_uv=W_(u,v) in P_u tensor P_v.                              (4)
```

All tensor slots are labelled and all products use the canonical shuffle.
The six pair-response hypotheses are the tensor identities

```text
Z_uv
 =H boxtimes B_uv+A_u boxtimes C_v+A_v boxtimes C_u
 =0                         for every {u,v} subset U.          (5)
```

These are identities in `X tensor Y tensor P_u tensor P_v`, not scalar
vanishing at one residual contraction.

The complete contracted six-slot target identity is

```text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(c=0)^2 mu_c product_(v in B)e_(v,c)^*,
mu_0 mu_1 mu_2 != 0.                                         (6)
```

Equation (6) contains all `3^6` outside coefficients.  No Hamming shell or
isolated projected coordinate replaces it.

For a tensor `T in E tensor F`, define its left and right supports
intrinsically by

```text
L(T)=image(F^vee -> E),       R(T)=image(E^vee -> F).          (7)
```

For `H`, abbreviate

```text
L=L(H) subset X,              M=R(H) subset Y.                 (8)
```

Let

```text
pi_X:X -> X/L,                pi_Y:Y -> Y/M,
bar A_u=(pi_X tensor id)A_u,
bar C_u=(pi_Y tensor id)C_u.                                  (9)
```

Whole-block support means nonvanishing of the entire tensor, while coordinate
support refers to the nonzero coefficients of one covector in the fixed GHZ
basis.  These two notions are never interchanged below.

## 3. The quotient cross lemma

The basic support reduction is independent of the rank of `H`, except for
the dimensions of its quotient spaces.

### Lemma 1 (quotient cross support)

Projecting (5) to `(X/L) tensor (Y/M)` gives

```text
bar A_u boxtimes bar C_v+bar A_v boxtimes bar C_u=0
                                      for u!=v.                (10)
```

If both quotient families are nonzero, their whole-block supports agree:

```text
T={u:bar A_u!=0}={u:bar C_u!=0}.                              (11)
```

Moreover,

```text
1 <= |T| <= 2.                                                (12)
```

If `T={s,t}`, all four quotient blocks have tensor rank one.  Up to nonzero
rescaling of their factor lines, there are nonzero

```text
bar a in X/L,       bar c in Y/M,
alpha_s in P_s,     alpha_t in P_t,       tau in K^*           (13)
```

such that

```text
bar A_s=bar a tensor alpha_s,
bar A_t=bar a tensor alpha_t,
bar C_s=tau bar c tensor alpha_s,
bar C_t=-tau bar c tensor alpha_t.                            (14)
```

No rank-one conclusion for an individual quotient block is asserted when
`|T|=1`; there is then no active pair on which to apply the realignment.

#### Proof

Suppose `u` belongs to the support of `bar A` but not `bar C`, and choose a
port `v` with `bar C_v!=0`.  Then `u!=v`, and the first product in (10) is
nonzero while the second is zero, a contradiction.  This proves one support
inclusion; the symmetric argument proves equality.

For distinct active `u,v`, realign (10) with row slots `(X/L,u)` and column
slots `(Y/M,v)`.  The first term is the rank-one outer product

```text
vec(bar A_u) vec(bar C_v)^T,                                  (15)
```

while, after labelled row and column permutations, the other has rank

```text
rank(bar A_v) rank(bar C_u).                                  (16)
```

Equality makes both factors in (16) rank one.  The opposite realignment
handles `bar A_u,bar C_v`.  Uniqueness of the four factor lines of a nonzero
simple tensor identifies one common residual line on each side and one
common local factor line at each active port.  Thus, before normalization,

```text
bar A_u=s_u bar a tensor alpha_u,
bar C_u=t_u bar c tensor alpha_u,
s_u t_v+s_v t_u=0.                                           (17)
```

On every active chart `s_u,t_u` are nonzero.  Set `r_u=s_u/t_u`.
For three distinct active ports, (17) gives `r_u=-r_v`,
`r_u=-r_w`, and `r_v=-r_w`, hence `2r_v=0`.  Characteristic zero and
`r_v!=0` give a contradiction.  Therefore `|T|<=2`, and absorbing the
nonzero factors in the two-port case gives (14).  The equations before
normalization are polynomial; the displayed ratios are used only on the
declared nonzero charts.  `square`

### Lemma 2 (full-support collapse in the two-sided escape)

Under the hypotheses of Lemma 1, project (5) only in the `q_0` slot:

```text
bar A_u boxtimes C_v+bar A_v boxtimes C_u=0.                   (18)
```

If `v` is not in `T`, choosing `u in T` gives `C_v=0`.  The symmetric
one-slot projection gives `A_v=0`.  Thus the **whole** `A,C` supports are
contained in `T`.

If `|T|=2`, substituting (14) into the two one-slot projections and using
factor-line uniqueness lifts (14) to the whole blocks:

```text
A_s=a tensor alpha_s,        A_t=a tensor alpha_t,
C_s=tau c tensor alpha_s,    C_t=-tau c tensor alpha_t,       (19)
```

where `pi_X(a),pi_Y(c)` are nonzero.  The two cross products in (5) cancel,
so `H boxtimes B_st=0`.  Every other pair contains at most one active port.
Since `H!=0`,

```text
B_uv=0                       for every {u,v} subset U.         (20)
```

For `|T|=1`, every pair likewise contains at most one whole active port, so
(20) holds directly.  `square`

## 4. Rank zero is not a divisor leaf for the GLS4 pair

### Proposition 3 (rank-zero exclusion)

For the selected `Q`,

```text
rank H=0                                                        (21)
```

is impossible.

#### Proof

GLS4 chooses an active pair, meaning

```text
H_Q tensor Pi_Q !=0.                                           (22)
```

Equivalently, both `H_Q` and `Pi_Q` are nonzero.  Rank zero would mean
`H_Q=0`, contradicting (22).  `square`

The distinction is load-bearing: `Pi_Q!=0` and its associated companion
quotient survival do **not**, by themselves, imply `H_Q!=0`.  The exclusion
uses GLS4 activity for the same selected pair.

## 5. Rank-two double-containment theorem

### Theorem 4 (all rank-two quotient escapes are excluded)

Assume (1)--(6) and

```text
rank H=2.                                                       (23)
```

Then, for every `u in U`,

```text
L(A_u) subset L(H),                 R(C_u) subset R(H).         (24)
```

Equivalently,

```text
bar A_u=0,                          bar C_u=0                    (25)
```

for every port.  Neither whole block family is identically zero.

This is a coordinate-free pointwise implication.  It does not assert that
the locus in (24) is empty.

### 5.1 Excluding simultaneous two-sided escape

Assume first that both quotient families are nonzero.  Lemmas 1--2 give a
common support `T` of size one or two and `B_uv=0` for every pair.

If `T={t}`, the only internal edge on `{q_0} union U` is `A_t`.  If `A_t`
had a zero at two fully supported endpoint vectors, appending arbitrary torus
vectors at the other three ports would give a five-root.  Therefore `A_t`
is zero-free on the endpoint torus.  A nonzero bilinear form is torus-zero-free
exactly when it is a coordinate monomial, so

```text
A_t=lambda e_(q_0,i)^* tensor e_(t,a)^*,
C_t=nu     e_(q_1,j)^* tensor e_(t,b)^*.                       (26)
```

The residual lines `Ke_i^*,Ke_j^*` lie outside `L,M`, respectively, because
their quotient images are nonzero.

If `T={s,t}`, the same maximum-root argument applied to the common residual
factors in (19) makes

```text
a proportional e_(q_0,i)^*,      c proportional e_(q_1,j)^*.  (27)
```

If both local factors `alpha_s,alpha_t` were noncoordinate, choose torus
kernel vectors for both.  Together with any torus vector at `q_0` and the
inactive ports, these would give a five-root.  Hence at least one local factor
is coordinate.  No stronger local assertion is needed in this branch.

Let `rho_i:X -> X/Ke_i^*` and `rho_j:Y -> Y/Ke_j^*` be the coordinate
quotients.  Applying them in the two `Q` slots of the **complete** identity
(6) kills every `A,C` term, while every `B` term is already zero.  It gives

```text
H' tensor Pi_Q
 =sum_(c notin {i,j}) mu_c
   ebar_(q_0,c)^* tensor ebar_(q_1,c)^*
   tensor product_(u in U)e_(u,c)^*,
H'=(rho_i tensor rho_j)H.                                    (28)
```

Because `Ke_i^*` is not contained in `L` and both have dimensions one and
two, `rho_i|L` is injective.  Similarly `rho_j|M` is injective.  Therefore

```text
rank H'=rank H=2.                                             (29)
```

If `i=j`, the right side of (28) has `Q|U` flattening rank two, while the
left side has flattening rank one because it is one product
`H' tensor Pi_Q`.  If `i!=j`, only the third colour `k` remains, and equality
with one nonzero simple tensor forces `H'` itself to have tensor rank one.
Both alternatives contradict (29).  Thus simultaneous two-sided escape is
impossible.

### 5.2 Secondary cross lemma for a one-sided escape

Assume, after possibly exchanging `q_0,q_1`, that

```text
bar A_u=0 for every u,             bar C_v!=0 for some v.      (30)
```

The whole `A` family is nonzero.  Otherwise (5) gives every `B_uv=0`, and
`{q_0} union U` is an immediate five-root.

Projecting (5) only modulo `M` gives

```text
A_u boxtimes bar C_v+A_v boxtimes bar C_u=0.                   (31)
```

The proof of Lemma 1 applies with `A_u` in place of `bar A_u`.  Hence

```text
T={u:A_u!=0}={u:bar C_u!=0},             1<=|T|<=2.            (32)
```

When `|T|=2`, the active `A` blocks have rank one and share one residual
factor line in `L`, while the quotient `C` blocks have the corresponding
opposite-sign form.

### 5.3 The singleton one-sided chart gives a five-root

Let `T={t}` and let `v` be inactive.  Since `C_v` lies in `M`, (5) reads

```text
H boxtimes B_tv+A_t boxtimes C_v=0.                            (33)
```

Realign with row slots `(q_0,t)` and column slots `(q_1,v)`.  The first term
has rank

```text
2 rank(B_tv),                                                   (34)
```

while the second is the outer product

```text
vec(A_t) vec(C_v)^T                                             (35)
```

and has rank one if nonzero.  Equality is therefore impossible unless both
terms vanish.  Thus `B_tv=0` and `C_v=0`.  Repeating this for every inactive
port, and then for inactive pairs, gives all `B_uv=0` and whole `C` support
contained in `{t}`.

A rank-two bilinear form is not a coordinate monomial, so it has a torus
zero `(z_0,z_1)`.  The five vertices

```text
{q_0,q_1} union (U-{t})                                        (36)
```

then form a torus root: their only possibly nonzero internal edge is `H`,
and it vanishes at `(z_0,z_1)`.  This contradicts maximality.

### 5.4 The two-port one-sided chart contradicts the complete target

Let `T={s,t}`.  Equations (31) and the realignment proof give

```text
A_s=a tensor alpha_s,        A_t=a tensor alpha_t,             (37)
```

with `a in L` nonzero.  The inactive-port realignment from Section 5.3
forces `C_v=B_uv=0` whenever `v` is inactive.  For the active pair, quotient
`L -> L/Ka` kills both cross terms of (5) but not `H`, so `B_st=0`.
The remaining cross equality lifts the quotient factors and gives

```text
C_s=tau c tensor alpha_s,
C_t=-tau c tensor alpha_t,       c notin M.                    (38)
```

Maximum-root maximality forces `a,c` to be coordinate covectors.  Indeed, a
torus kernel of either residual factor, together with arbitrary port torus
vectors, would give `{q_0} union U` or `{q_1} union U` as a five-root.
Write

```text
a=e_(q_0,i)^*,                c=e_(q_1,j)^*                    (39)
```

after absorbing nonzero scalars.

Both `alpha_s` and `alpha_t` are coordinate.  If, say, `alpha_s` were
noncoordinate, choose a torus zero of the rank-two `H`, a torus kernel vector
of `alpha_s`, and arbitrary torus vectors at the two inactive ports.  The
five vertices `Q` plus those three ports would be a larger torus root.

Apply `rho_i tensor rho_j` to (6).  Here `Ke_i^*` is contained in `L`, so
`rho_i|L` has rank one.  In contrast, `Ke_j^*` is outside `M`, so
`rho_j|M` is injective.  Consequently

```text
rank H'=1,                       H'!=0.                         (40)
```

As in (28), equal residual colours give a `Q|U` rank-two contradiction.
Thus `i!=j`.  Let `k` be the third colour.  The projected equality gives a
nonzero scalar `lambda` with

```text
H'=lambda e_(q_0,k)^* tensor e_(q_1,k)^*,
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*.                    (41)
```

Now use unprojected pure coefficients.  The pure colour-`i` coefficient
cannot come from `H tensor Pi_Q`, whose four port factors in (41) are colour
`k`, and cannot come from a `C` edge, whose `q_1` factor is colour `j`.
Therefore one of the two coordinate local factors is colour `i`.  Similarly,
the pure colour-`j` coefficient forces the other local factor to be colour
`j`.

Evaluate (6) on the full port word `kkkk`.  Every `A,C` edge term vanishes
because its active local factor is colour `i` or `j`; every `B` term is zero.
Thus

```text
H tensor Pi_Q
 =mu_k e_(q_0,k)^* tensor e_(q_1,k)^*
      tensor product_(u in U)e_(u,k)^*.                        (42)
```

Since `Pi_Q` is nonzero, (42) forces `rank H=1`, contradicting (23).
The symmetric one-sided escape is excluded by exchanging the residual slots.
This proves Theorem 4.  `square`

## 6. Exact rank-two survivor

Theorem 4 leaves only the following core.  This section records consequences,
not an exclusion.

### Corollary 5 (the `2 x 2` conformal core)

On rank two, all blocks in the response cross terms lie in

```text
A_u in L tensor P_u,                C_u in M tensor P_u,
dim L=dim M=2.                                                 (43)
```

For every pair, the exact response condition is

```text
[A_u boxtimes C_v+A_v boxtimes C_u]=0
                  in (L tensor M)/K H.                         (44)
```

Conversely, (44) makes the cross tensor a unique `H`-multiple and recovers
`B_uv` uniquely through

```text
H boxtimes B_uv=-(A_u boxtimes C_v+A_v boxtimes C_u).          (45)
```

Equivalently, choose any linear functional

```text
theta_H:L tensor M -> K,              theta_H(H)=1.             (46)
```

Then, on the locus (44),

```text
B_uv=-theta_H(A_u boxtimes C_v+A_v boxtimes C_u).              (47)
```

The right side is independent of the choice of `theta_H` because (44) has
already put the cross tensor on the line `K H`.

Neither family can be zero.  If all `A_u` vanished, (45) would give all
`B_uv=0` and `{q_0} union U` would be a five-root.  The `C` statement is
symmetric.

### Corollary 6 (the quotient four-port target `Q4`)

Apply `pi_X` and `pi_Y` in the two `Q` slots of (6).  Since

```text
pi_X H=0,            pi_X A_u=0,            pi_Y C_u=0,        (48)
```

the `P=Q` and all cross-edge terms vanish.  Only physical edges inside `U`
remain.  For `{u,v} subset U`, define

```text
widehat Pi_uv
 =(pi_X tensor pi_Y tensor id)Pi_uv
 in (X/L) tensor (Y/M) tensor
       tensor_(w in U-{u,v}) P_w.                              (49)
```

Then the complete target implies

```text
sum_({u,v} subset U)
 sh_(uv,U-{u,v})(B_uv tensor widehat Pi_uv)
 =sum_(c=0)^2 mu_c
   pi_X(e_(q_0,c)^*) tensor pi_Y(e_(q_1,c)^*)
   tensor product_(w in U)e_(w,c)^*.                           (50)
```

Both quotient spaces in (50) are lines.  After choosing their generators,
(50) is one exact four-port ternary diagonal identity, possibly with some
zero target weights.  Keeping the quotient-line factors as displayed avoids
any artificial denominator or choice of scale.

The selected nonzero `Pi_Q` disappears from (50).  This is why scalar or
projected `Pi_Q` survival alone cannot close the double-contained core.  A
successful continuation must couple `Pi_Q` before this quotient, or use the
common-root integrability of the full companion family.

### Corollary 7 (moving two-blocker condition)

Let `(z_0,z_1)` be a fully supported **regular torus zero** of `H`, meaning

```text
H(z_0,z_1)=0,
z_0|L !=0,                    z_1|M !=0.                       (51)
```

Such points form a nonempty open subset of the torus-zero hypersurface for a
rank-two `H`.  For each port put

```text
a_u=A_u(z_0,-) in P_u,
c_u=C_u(z_1,-) in P_u,
K_u=ker a_u intersect ker c_u.                                (52)
```

Call `u` open when `K_u` meets the local torus.  Then at most two of the four
ports are open.  Equivalently, for every regular torus zero, at least two
ports satisfy

```text
e_(u,d)^* in span{a_u,c_u}       for some d in {0,1,2}.         (53)
```

#### Proof

Suppose three ports `u,v,w` were open and choose fully supported
`z_u,z_v,z_w` in their respective `K` spaces.  For each such port define

```text
p_u=A_u(-,z_u) in L,              q_u=C_u(-,z_u) in M.         (54)
```

The scalar vanishings in (52) say

```text
z_0(p_u)=0,                       z_1(q_u)=0.                   (55)
```

Because the restrictions in (51) are nonzero and `L,M` are two-dimensional,
all three `p` vectors lie on one common line of `L`, and all three `q`
vectors lie on one common line of `M`.

Evaluate (5) in the two port slots for a pair among `u,v,w`:

```text
b_uv H+p_u q_v^T+p_v q_u^T=0.                                 (56)
```

The cross sum in (56) has rank at most one, while a nonzero `b_uv H` has rank
two.  Thus `b_uv=0`, and (56) then also kills the cross sum.  Every internal
edge of the five vertices `Q union {u,v,w}` vanishes at the selected torus
vectors, contradicting maximum-root maximality.

Finally, `K_u` misses the torus exactly when it is contained in a coordinate
hyperplane, equivalently when its annihilator `span{a_u,c_u}` contains a
coordinate covector.  This proves (53).  `square`

The moving condition is pointwise over the regular torus-zero family.  It
does not select two uniform ports or uniform colours over the whole family.

## 7. Exhaustive rank-one response trichotomy

Assume now

```text
rank H=1,                    H=x tensor y,             x,y!=0. (57)
```

The factorization is unique up to the gauge

```text
x -> gamma x,               y -> gamma^(-1)y.                  (58)
```

The rank-one response-zero locus has the following exhaustive cover.

### 7.1 Branch I: double-contained rank-one Wick core

If every `A,C` block is contained in the two support lines of `H`, write

```text
A_u=x tensor a_u,               C_u=y tensor c_u.              (59)
```

Substitution in (5) gives the exact and unique formula

```text
B_uv=-(a_u tensor c_v+c_u tensor a_v),                          (60)
```

with the labelled slot order understood.  Conversely, (59)--(60) make all
six pair responses zero identically.

Neither family `(a_u)` nor `(c_u)` is identically zero.  Moreover maximum-root
maximality forces at least one `a_u` and at least one `c_v` to be a coordinate
covector.  For example, if every nonzero `a_u` were noncoordinate, choose a
torus kernel vector for each of them; zero `a_u` impose no condition.  Then
all `A_u` and every `B_uv` vanish on `{q_0} union U`, giving a five-root.
The `c` argument is symmetric.

This core is not excluded by (5), maximum-root maximality, or rank alone.
The complete target (6) remains an additional same-graph condition.

### 7.2 Branch II: one-sided escape

Assume, after exchanging residual sides if necessary,

```text
A_u=x tensor a_u for every u,
bar C_v!=0 for at least one v.                                  (61)
```

Projecting (5) modulo `Ky` gives

```text
a_u boxtimes bar C_v+a_v boxtimes bar C_u=0.                    (62)
```

The support proof of Lemma 1 gives

```text
T={u:a_u!=0}={u:bar C_u!=0},             1<=|T|<=2.             (63)
```

#### Singleton one-sided form

If `T={s}`, then

```text
A_s=x tensor a_s,                 A_v=0                 (v!=s),
C_s arbitrary with bar C_s!=0,
C_v=y tensor c_v                                      (v!=s),
B_sv=-a_s tensor c_v,
B_vw=0                                      (v,w!=s).           (64)
```

The escaping part of `C_s` is invisible to the six pair equations because
no response pairs port `s` with itself.

Maximum-root maximality forces both `a_s` and `y` to be coordinate
covectors:

- if `a_s` were noncoordinate, a torus kernel vector at `s` would kill
  `A_s` and every star edge `B_sv`, giving the five-root `{q_0} union U`;
- if `y` were noncoordinate, a torus kernel vector at `q_1` would kill `H`
  and all three inactive `C_v`, giving the five-root `Q` plus the three
  inactive ports.

There is also the exact necessary disjunction

```text
x is coordinate
  or at least one inactive c_v is coordinate.                   (65)
```

Indeed, if `x` and all three inactive `c_v` were noncoordinate, use a torus
kernel of `x` to kill `H`, and torus kernels of all inactive `c_v` to kill
their `C` edges.  The inactive `B` edges are already zero.

#### Two-port one-sided form

If `T={s,t}`, factor-line uniqueness in (62) gives, after a nonzero
normalization,

```text
A_s=x tensor a_s,                  A_t=x tensor a_t,
C_s=d tensor a_s+y tensor c_s,
C_t=-d tensor a_t+y tensor c_t,
C_v=y tensor c_v                                      (v notin T),
B_uv=-(a_u tensor c_v+c_u tensor a_v),                         (66)
```

where

```text
d notin Ky,                       a_v=0 for v notin T.           (67)
```

The two `d`-terms cancel with opposite signs in the active-pair response;
the remaining terms give (60).

Maximum-root maximality implies

```text
at least one of a_s,a_t is coordinate;                          (68)
```

otherwise their two torus kernel vectors give `{q_0} union U` as a
five-root.  It also gives

```text
y is coordinate
  or both a_s and a_t are coordinate.                           (69)
```

If `y` and, say, `a_s` were both noncoordinate, choose torus kernel vectors
for them and use port `s` together with the two inactive ports.  Every edge
on those five vertices vanishes.

The right-sided one-port and two-port forms are obtained exactly by
exchanging

```text
(q_0,x,A,a) <-> (q_1,y,C,c).                                   (70)
```

No complete-target contradiction for either one-sided form is proved here.

### 7.3 Branch III: two-sided escape

Assume both quotient families are nonzero.  Lemmas 1--2 give

```text
T={u:A_u!=0}={u:C_u!=0},       1<=|T|<=2,
B_uv=0 for every pair.                                             (71)
```

Maximum-root coordinate forcing is exactly as in Section 5.1.

#### Singleton two-sided form: monomial triangle

Let `T={t}`.  Both whole blocks are coordinate monomials:

```text
A_t=alpha e_(q_0,i)^* tensor e_(t,a)^*,
C_t=beta  e_(q_1,j)^* tensor e_(t,b)^*.                         (72)
```

Their residual lines lie outside `Kx,Ky`, respectively.  Apply the two
coordinate quotients in (6).  Their restrictions to `Kx,Ky` are injective,
so the projected `H` is nonzero of rank one.  Equal residual colours again
give a `Q|U` flattening-rank-two contradiction.  Therefore `i!=j`; let `k`
be the third colour.  The projected target gives

```text
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*.                    (73)
```

The pure colour-`i` coefficient of (6) can come only from the `A_t` term, so
`a=i`.  The pure colour-`j` coefficient can come only from `C_t`, so `b=j`.
On the all-`k` port slice, both cross terms vanish and (6) forces

```text
H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*.                         (74)
```

The three remaining physical edge terms have disjoint support in the `t`
slot: colours `k,i,j`, respectively.  Therefore they cannot cancel each
other, and the complete target splits exactly into three pure pieces:

```text
H tensor Pi_Q
   =mu_k product_(v in B)e_(v,k)^*,
A_t tensor Pi_(q_0,t)
   =mu_i product_(v in B)e_(v,i)^*,
C_t tensor Pi_(q_1,t)
   =mu_j product_(v in B)e_(v,j)^*.                             (75)
```

Thus the smallest two-sided rank-one leaf is one coordinate-monomial
triangle on `{q_0,q_1,t}` with three correspondingly pure complementary
permanent tensors.  Equation (75) is a necessary same-root companion
configuration, not a proof that such companions can be realized on a GLS4
source point.

#### Two-port two-sided form

Let `T={s,t}`.  There are distinct residual colours `i,j`, a third colour
`k`, nonzero local covectors `alpha_s,alpha_t`, and `tau!=0` such that

```text
A_s=e_(q_0,i)^* tensor alpha_s,
A_t=e_(q_0,i)^* tensor alpha_t,
C_s=tau e_(q_1,j)^* tensor alpha_s,
C_t=-tau e_(q_1,j)^* tensor alpha_t.                            (76)
```

At least one local factor is coordinate.  The target projection gives

```text
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*,                    (77)
```

and the pure colour-`i` and colour-`j` coefficients imply

```text
i belongs to supp(alpha_s) union supp(alpha_t),
j belongs to supp(alpha_s) union supp(alpha_t).                 (78)
```

In fact

```text
H=gamma e_(q_0,k)^* tensor e_(q_1,k)^*.                         (79)
```

To prove this, first suppose one local factor is noncoordinate.  If `H` had
a torus zero, that zero, a torus kernel vector of the noncoordinate local
factor, and the two inactive ports would form a five-root.  Hence `H` is
torus-zero-free, so rank one makes it a coordinate monomial.  The projected
identity then forces both of its colours to be `k`.

Otherwise both local factors are coordinate.  Conditions (78) force their
two colours to be exactly `i,j`.  Evaluating the complete target on the
all-`k` port word kills every cross term and forces (79).

After removing the already exact pure-`k` term, the remaining necessary
identity is

```text
sum_(u in {s,t})
 sh(A_u tensor Pi_(q_0,u)+C_u tensor Pi_(q_1,u))
 =mu_i product_(v in B)e_(v,i)^*
  +mu_j product_(v in B)e_(v,j)^*.                             (80)
```

No contradiction to the common-root permanent realization of (80) is proved
here.

### 7.4 Rank-one cover ledger

The rank-one response locus is exhausted by:

```text
I.   both block families contained in Kx and Ky:       (59)--(60);
II.  exactly one family escapes:                       (64) or (66),
     and its residual-slot transpose;
III. both families escape:                             (75) or (76)--(80).
                                                                    (81)
```

This is a quotient-support cover, not an enumeration of the `2^4` whole-block
support masks.  Support size one or two is derived from the cross equation.

## 8. Six pair zeros do not automatically give the seventh response

GLS9 used rank three to prove every `B_uv=0`; the four-port response then
vanished because every perfect matching on `Q union U` used a `U-U` edge.
That implication fails on the determinant divisor.

Let `T_4` denote the physical six-vertex hafnian tensor on `Q union U`.
Evaluate the two `Q` slots and all four port slots at arbitrary vectors, and
write

```text
h=H(z_0,z_1),
a_u=A_u(z_0,z_u),
c_u=C_u(z_1,z_u),
b_uv=B_uv(z_u,z_v),
t=T_4(z_0,z_1,(z_u)_(u in U)).                                (82)
```

The six pair-response equations give

```text
h b_uv+a_u c_v+a_v c_u=0.                                     (83)
```

Direct expansion of the fifteen six-vertex matchings, followed by (83),
gives the denominator-free identity

```text
h t
 =-2 sum_(S subset U, |S|=2)
       product_(u in S)a_u product_(v in U-S)c_v.              (84)
```

#### Proof of (84)

The matching expansion is

```text
t
 =h sum_({{a,b},{c,d}} partition U) b_ab b_cd
  +sum_(u!=v) a_u c_v b_(U-{u,v}).                             (85)
```

Multiply by `h`.  In the first sum replace both factors `h b` using (83); in
the second replace its single `h b`.  Expanding and collecting the six
labelled `a_a a_b c_c c_d` monomials gives coefficient `-2` for each and no
other monomial.  This proves (84) without dividing by `h`.  `square`

In the rank-one double-contained core, (84) tensorizes to

```text
T_4
 =-2 x tensor y tensor
   sum_(S subset U, |S|=2)
     product_(u in S)a_u product_(v in U-S)c_v.                (86)
```

The right side is generically nonzero.  Therefore the present theorem is an
**all-six-pair-response-zero** reduction.  If one wants the literal
all-seven-zero leaf, `T_4=0` must be imposed separately.  Equation (84) then
adds the exact quartic necessary condition

```text
sum_(|S|=2) a_S c_(U-S)=0                                     (87)
```

at every contraction.  When `h=0`, (84) does not conversely determine `t`.

## 9. Nonzero charts, denominators, and saturation ledger

The case cover has the following exact chart structure.

1. **Source pair.**  `H_Q!=0` comes from GLS4 activity.  `Pi_Q!=0` is a
   union of the `81` coefficient opens

   ```text
   D(Pi_Q[gamma]),             gamma in {0,1,2}^4.              (88)
   ```

   There is no invented canonical scalar for tensor nonvanishing.

2. **Rank two.**  The rank-two stratum is covered by the nine possible
   nonzero `2 x 2` minors of the `3 x 3` matrix of `H`, together with
   `det H=0`.  On each `D(Delta_(IJ))`, bases for `L,M` may be chosen and the
   preceding calculations become ordinary `2 x 2` matrix algebra.  The
   conclusions use only `L(H),M(H)` and hence glue across overlaps.

3. **Rank one.**  The rank-one stratum is covered by the nine nonzero-entry
   charts `D(H[i,j])`, with all `2 x 2` minors zero.  Factoring
   `H=x tensor y` on one chart introduces only the gauge (58); every normal
   form is invariant under that rescaling.

4. **Active support charts.**  Whole-block zero strata remain exact zero
   equations.  Where factor lines are normalized, one selected nonzero
   coefficient of each declared active quotient block is inverted.  The
   unnormalized equations (17), (31), and (62) are polynomial and
   denominator-free.

5. **Coordinate forcing.**  Statements that a covector is coordinate are
   discrete conclusions from the absence of torus zeros.  The scalar
   multiplying the selected coordinate covector is nonzero on that chart;
   no unmentioned support entry is inverted.

6. **Target weights.**  The only target saturation is the declared
   `mu_0 mu_1 mu_2!=0`.  Scalars such as `lambda` in (41), (73), and (77) are
   derived from equality of nonzero simple tensors.  The equations are kept
   denominator-free.

7. **Unused GLS gates.**  No step divides by or saturates against

   ```text
   h=H_Q(z_Q),
   p_(A,Q)(z_Q),
   a response coordinate,
   a nuisance, augmented, or selector minor,
   an alignment or anchor factor,
   a target-module denominator.                                (89)
   ```

8. **No support-mask enumeration.**  The sets `T` arise from support equality
   in Lemma 1 or its one-sided version.  The characteristic-zero sign
   relation proves `|T|<=2`; no search through labelled masks is part of the
   proof.

## 10. Sharp controls and exact limitations

The controls below separate the response/maximality mechanisms from the
complete mixed target.  They are not witness points.

### 10.1 Rank-two double-contained maximum-root control

Start from the exact ten-vertex root-incidence fixture in Section 9.5 of the
[GLS9 theorem](../../../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md#95-maximum-root-off-target-fixture-on-the-surviving-pure-locus).
Keep every root--outside block unchanged.  On the outside graph use colours
`0,1,2`, ports `u_0,u_1,u_2,u_3`, and set

```text
H=e_0^* tensor e_0^*+e_1^* tensor e_1^*,

A_(u_0)=e_0^* tensor e_0^*,
C_(u_0)=e_1^* tensor e_0^*,
A_(u_1)=e_1^* tensor e_1^*,
C_(u_1)=e_0^* tensor e_1^*,

B_(u_0,u_1)=-e_(u_0,0)^* tensor e_(u_1,1)^*,                 (90)
```

with all other outside blocks zero.  Then

```text
L=M=span{e_0^*,e_1^*},
rank H=2,                                                        (91)
```

and the two cross terms on `{u_0,u_1}` add to

```text
H tensor e_(u_0,0)^* tensor e_(u_1,1)^*,                       (92)
```

which is cancelled by `H tensor B_(u_0,u_1)`.  Every other pair response is
zero termwise.

The original coordinate-monomial clique cover still proves maximum root
order four.  Root incidence is unchanged, so the total outside corank remains
five,

```text
Pi_Q=product_(u in U)e_(u,2)^*,        p_(A,Q)=1,
H(1,1)=2.                                                       (93)
```

At the outside word `(0,0,2,2,2,2)`, only `H tensor Pi_Q` contributes, with
coefficient one instead of target zero.  Thus this is an exact
maximum-root/rank-two-core/pure-`Pi_Q` response control and an exact complete
mixed **failure**.

It does not verify GLS4 higher-column quotient survival and is not a witness.

### 10.2 Rank-one double-contained maximum-root control

Keep the same root-incidence fixture and put

```text
H=e_0^* tensor e_0^*,

A_(u_0)=e_0^* tensor e_(u_0,0)^*,
C_(u_0)=e_0^* tensor e_(u_0,1)^*,
A_(u_1)=e_0^* tensor e_(u_1,1)^*,
C_(u_1)=e_0^* tensor e_(u_1,0)^*,

B_(u_0,u_1)
 =-(e_(u_0,0)^* tensor e_(u_1,0)^*
    +e_(u_0,1)^* tensor e_(u_1,1)^*),                          (94)
```

with other outside blocks zero.  Formula (60) gives all six response zeros.
The monomial-edge independent-set bound remains four, the root incidence and
`Pi_Q` remain unchanged, and the same mixed word has coefficient one instead
of zero.  This is a sharp rank-one core control, not target incidence.

### 10.3 Formal monomial-triangle target control

At the level of independently declared companion tensors, take distinct
colours `i,j,k` and one active port `t`:

```text
H=e_k^* tensor e_k^*,
A_t=e_i^* tensor e_i^*,
C_t=e_j^* tensor e_j^*,
B_uv=0,                                                         (95)

Pi_Q=product_(u in U)e_(u,k)^*,
Pi_(q_0,t)=product_(v in B-{q_0,t})e_(v,i)^*,
Pi_(q_1,t)=product_(v in B-{q_1,t})e_(v,j)^*.                  (96)
```

Then the three terms are exactly the three GHZ pure tensors and every pair
response is zero.  This proves that the labelled tensor algebra and target
identity alone do not contradict the monomial-triangle shape.

However, (96) has **not** been realized as three permanents of one common
four-root incidence system satisfying GLS4 source survival, raw incidence,
and maximum-root conditions.  It is a formal integrability control only,
not a physical graph point.

### 10.4 The seventh response is genuinely independent

In the rank-one core, choose all `a_u,c_u` nonzero.  The coefficient of (86)
at a port word selecting two `a` factors and two complementary `c` factors is
`-2` times a nonzero product.  Hence all six pair responses vanish while the
four-port response does not.  The extra condition (87) is load-bearing for
an all-seven-zero theorem.

### 10.5 Bounded replay evidence

During the read-only derivation, exact in-memory rational/SymPy replays
checked:

- every coefficient of the rank-two controls (90) and the pre-target
  one-sided normal form;
- every coefficient of the rank-one response formula (60);
- all `3^6` coefficients of the formal monomial triangle (95)--(96);
- the ten-vertex clique/independent-set maximum-root bound in (90) and (94);
- unchanged root-incidence corank, `Pi_Q`, and raw incidence; and
- the displayed mixed target defects.

The tracked GLS9 primary verifier and independent no-import audit were also
rerun and passed unchanged.  These bounded replays are not a proof of the
arbitrary-point implications.  The proofs are the quotient, realignment,
maximum-root, and complete-target arguments above.  No new durable verifier
or independent audit is claimed by this handoff.

## 11. Exact proved, candidate, and open ledger

The status of this **handoff**, prior to theorem packaging or hostile review,
is:

```text
GLS4-selected Q has H_Q!=0; rank zero excluded:             DERIVED EXACTLY;

quotient cross-support equality and |T|<=2:                 DERIVED EXACTLY;
rank-two simultaneous two-sided escape:                     EXCLUDED;
rank-two one-sided singleton escape:                        EXCLUDED;
rank-two one-sided two-port escape:                         EXCLUDED;
rank-two double containment (24):                           DERIVED EXACTLY;
rank-two conformal core equations (44)--(47):               DERIVED EXACTLY;
rank-two quotient four-port target Q4 (50):                 DERIVED EXACTLY;
rank-two moving two-blocker condition (53):                 DERIVED EXACTLY;
rank-two double-contained core empty on witness locus:      OPEN;

rank-one double-contained normal form:                      DERIVED EXACTLY;
rank-one one-sided singleton/two-port normal forms:         DERIVED EXACTLY;
rank-one two-sided support-one/support-two normal forms:     DERIVED EXACTLY;
rank-one monomial-triangle common-root integrability:       OPEN;
rank-one one-sided/core complete-target exclusion:          OPEN;

six pair zeros imply four-port response zero on rank drop:  FALSE;
denominator-free seventh-response identity (84):            DERIVED EXACTLY;
all-seven rank-drop branch after quartic (87):              OPEN;

written candidate promoted to reviewed theorem:             NOT DONE;
independent audit of the new arbitrary-point arguments:      NOT DONE;
formalization:                                               NONE;
legal useful target row on every four-root witness:          OPEN;
supply-and-target-attachment strategic node:                 OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.       (97)
```

`DERIVED EXACTLY` in (97) describes the algebra in this candidate handoff.
It is not the repository evidence status `proved` until the result is
packaged, independently audited, reviewed, and integrated through the normal
frontier process.

No apparent exact witness or counterexample arose.  Both physical sharpness
controls fail an explicit complete mixed target coefficient.

## 12. Smallest next obligation

The smallest **rank-two** continuation is not another support census.  It is
to decide the double-contained core consisting simultaneously of:

1. the six conformal equations (44), with `B` recovered by (47);
2. the complete quotient four-port target (50);
3. the moving two-blocker condition (53) on every regular torus zero of `H`;
4. `Pi_Q!=0` and GLS4 same-pair higher-column quotient survival; and
5. the unprojected complete six-slot identity (6), retaining common-root
   companion integrability.

A positive next theorem should either derive a complete mixed coefficient
contradiction from those same-graph conditions or give an exact physical
point satisfying **every** coefficient and every GLS4 source gate.  The
double quotient (50) loses `Pi_Q`, so an argument using only `Q4` cannot be
sufficient.

The smallest support leaf at rank one is the monomial triangle (75).  Its
next exact question is whether three differently pure complementary
permanents can arise from one common four-root incidence system while the
selected `Q` retains GLS4 raw incidence and quotient survival.  The formal
control (95)--(96) does not answer that integrability question.

Neither obligation authorizes work on the separate current pure-`Pi_Q`
candidate, changes the live frontier, or closes a downstream detector.  This
handoff ends with the determinant-divisor node **OPEN** and the global
conjecture **UNRESOLVED**.
