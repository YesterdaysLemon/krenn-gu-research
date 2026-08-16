# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective canonical-binomial residual exclusion

## Status

**Exact characteristic-zero exclusion of one canonical nonmonomial residual
orbit in the fully-injective `(3,3,3)` rank-four/rank-eight cell.**  Retain
the normalized, target-consistent physical `m=3` common-three-space
full-sensor hypotheses with

```text
dim U=3,                 K=image H=D^(-1)(U),       dim K=4,
D(K)=U,                  rank rho=rank pi=rank theta=3. (1)
```

The target stabilizer used below consists of a common colour permutation on
all six vertex factors and diagonal maps `g_1,...,g_6` satisfying

```text
product_(s=1)^6 (g_s)_(i,i)=1             for i=0,1,2.
```

Its projection onto the three root diagonal tori is surjective: arbitrary
root scalings are compensated on the three nonroot factors.  Assume that,
up to this target stabilizer, the three shared factors are nonzero vectors on
one common coordinate line and the actual residual block is supported on the
two complementary diagonal entries.  Normalize the common line to colour
two and the three shared factors to `e_2`.  Then the derivative is

```text
D(a,b,c)=(a tensor e_2-e_2 tensor b) tensor e_2+C tensor c,

C=kappa_0 e_0 tensor e_0+kappa_1 e_1 tensor e_1,
kappa_0 kappa_1!=0.                                  (2)
```

Equivalently, `x=y=w=e_2`, the derivative kernel is
`span((e_2,e_2,0))`, and the actual residual block is the complementary
diagonal binomial.  Then no complete-target-compatible physical point exists.

The proof uses the full-sensor alternating tensor on the physical third-row
three-space, the complete target coefficients including the `q_2` direction,
one coordinate-free zero-pair lemma, and an exhaustive nine-flag projective
cover.  It uses no solver, localization, generic-point substitution, or
finite sample.

This theorem does **not** reduce an arbitrary nonmonomial residual to (2).
Other nonmonomial tangent-quotient classes and the diagonal monomial
coordinate endpoints remain open, as do the other lower-rank cells, pair
coupling, components, pole strata, higher orders, and all-rank drop.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The physical three-space has nonzero alternating tensor

Let the derivative domain be `A_1 direct-sum A_2 direct-sum A_3` and put

```text
N=ker D=span(n),              n=(e_2,e_2,0),
L=N^perp.                                             (3)
```

The rank-four/rank-eight incidence table gives `N subset K`.  Hence

```text
K^perp subset L,             dim L=8,
dim K^perp=5.                                        (4)
```

The transpose `H^T` has kernel `K^perp`, so

```text
V=H^T(L),                    dim V=3.                (5)
```

Every third-root covector `(0,0,gamma)` annihilates `n`.  Therefore

```text
Q=image theta=span(q_0,q_1,q_2) subset V.            (6)
```

Third-row injectivity makes `dim Q=3`, and consequently

```text
Q=V.                                                 (7)
```

For rows `v_0,v_1,v_2` in `W^*=X^* direct-sum Y^* direct-sum Z^*`, define

```text
Alt(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(0)))_X tensor
   (v_(sigma(1)))_Y tensor
   (v_(sigma(2)))_Z.                                 (8)
```

Let

```text
H_bar:W -> K/N,                    D_bar:K/N -> U
```

be the quotient of `H` and the map induced by `D|K`.  Because `image H=K`,
`H_bar` is onto.  Because `ker(D|K)=N` and `D(K)=U`, `D_bar` is an
isomorphism.  Moreover,

```text
(K/N)^*=N^perp/K^perp,             image H_bar^T=V.
```

Choose a dual basis of `K/N` whose row images under `H_bar^T` are
`v_0,v_1,v_2`.  The direct separated-determinant expansion of the three
`X,Y,Z` singleton columns of `D_bar H_bar` is (8), multiplied by the nonzero
basis determinant of `D_bar`.  Physical full-sensor rank makes that
singleton determinant nonzero.  Therefore, for every basis of `V`,

```text
Alt(v_0,v_1,v_2)!=0.                                 (9)
```

By (7), write this load-bearing premise as

```text
Alt(Q)!=0.                                          (10)
```

## 2. The complete target supplies two zero pairs and a rank-two difference

For rows `u,v,q in W^*`, put

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (11)
```

Let `T_i=X_i tensor Y_i tensor Z_i` be the three fully transverse target
tensors.  The root coefficient of (2) at `(i,j,k)` is

```text
delta_(j=2)delta_(k=2)a_i
-delta_(i=2)delta_(k=2)b_j
+(kappa_0 delta_(i=j=0)+kappa_1 delta_(i=j=1))c_k.  (12)
```

Thus every tensor in `U=D(K)` has zero `(0,1,k)` and `(1,0,k)` coefficients
and satisfies

```text
kappa_1 u_(0,0,k)-kappa_0 u_(1,1,k)=0.              (13)
```

Apply (13) to the complete coefficientwise identity `G_N-J in U`.  Since
`Q=span(q_0,q_1,q_2)`, it gives

```text
M_(r_0,p_1)|Q=0,             M_(r_1,p_0)|Q=0.       (14)
```

Put

```text
F_i=M_(r_i,p_i)|Q,
lambda_i(q_j)=delta_(i=j).                           (15)
```

The weighted diagonal relation is

```text
kappa_1 F_0-kappa_0 F_1
 =kappa_1 lambda_0 tensor T_0
  -kappa_0 lambda_1 tensor T_1.                      (16)
```

Its right side has map rank two because both covector and target pairs are
independent.  Also

```text
ker lambda_0 intersect ker lambda_1=span(q_2).       (17)
```

## 3. Zero-pair classification

### Lemma 1 (a mixed zero pair is a two-source conjugate pair)

Let `Q subset X^* direct-sum Y^* direct-sum Z^*` have dimension three and
`Alt(Q)!=0`.  If independent `u,v in Q` satisfy

```text
M_(u,v)|Q=0,                                        (18)
```

then, after permuting the three sources,

```text
u=x+y,                 v=mu(x-y),
x in X^* nonzero,      y in Y^* nonzero,      mu!=0. (19)
```

In particular, their span is a split two-source plane and the radical partner
line of `u` is unique.

#### Proof

Split by the number of nonzero source components of `u`.

If `u=x` is pure in `X^*`, evaluation at `v` gives

```text
0=M_(x,v)(v)=2x tensor v_Y tensor v_Z.               (20)
```

Suppose, after exchanging `Y,Z`, that `v_Z=0`.  For every `q in Q`,

```text
M_(x,v)(q)=x tensor v_Y tensor q_Z.                  (21)
```

If `v_Y!=0`, all of `Q` misses `Z`.  If `v_Y=0`, the independent rows `u,v`
are both pure in `X`.  Either alternative makes `Alt(Q)=0`, a contradiction.

If `u=x+y` has support two, evaluation at `u` gives

```text
0=M_(u,u)(v)=2x tensor y tensor v_Z,                 (22)
```

so `v_Z=0`.  Condition (10) supplies a `q in Q` with `q_Z!=0`; evaluating
(18) there gives

```text
x tensor v_Y+v_X tensor y=0.                         (23)
```

Both terms are nonzero, and equality of rank-one tensors gives (19).

Finally, let `u=x+y+z` have full support.  Evaluation at `u` and projection
modulo the three factor lines give

```text
v=(a x,b y,c z),               a+b+c=0.             (24)
```

Evaluation at `v` gives

```text
ab+ac+bc=0.                                           (25)
```

No one of `a,b,c` can vanish without forcing `v=0`, so `abc!=0`.  For an
arbitrary `q in Q`, project `M_(u,v)(q)=0` modulo `span(x)` in the first
source.  The surviving coefficient is

```text
(b+c)(q_X mod x)=-a(q_X mod x),
```

and hence `q_X in span(x)`.  The other two projections similarly put
`q_Y in span(y)` and `q_Z in span(z)`.  Dimension three then gives

```text
Q=span(x,y,z).                                       (26)
```

For `q=A x+B y+C z`, direct expansion of the mixed map is

```text
M_(u,v)(q)=-(aA+bB+cC)x tensor y tensor z.           (27)
```

The nonzero linear form in (27) cannot vanish on all of `Q`.  This excludes
full support and completes the proof.  QED.

### Corollary 2 (radical-line bound)

For every nonzero `u in Q`,

```text
Rad_Q(u)={v in Q:M_(u,v)|Q=0},       dim Rad_Q(u)<=1. (28)
```

If `M_(u,u)|Q` is nonzero and a radical partner exists, Lemma 1 gives its
unique conjugate line.  If the square map is zero, support two would make `Q`
miss one source.  For full support `u=x+y+z`, the equation
`M_(u,u)(q)=0` forces

```text
q=(a x,b y,c z),                    a+b+c=0,
```

so its square kernel has dimension two and cannot contain the three-space
`Q`.  Thus `u` is pure; Lemma 1 then forbids an independent radical partner.

### Corollary 3 (intersection of two zero-pair planes)

Let two independent zero pairs span distinct planes `H,H' subset Q`.  Their
split planes cannot omit the same source, because then `H+H'=Q` would miss
that source.  After permuting sources,

```text
H subset X^* direct-sum Y^*,
H' subset X^* direct-sum Z^*.
```

Comparing source components shows

```text
H intersect H' is a pure X^* line.                   (29)
```

## 4. The two diagonal planes meet only on `q_2`

Put

```text
D_0=span(r_0,p_0),             D_1=span(r_1,p_1).   (30)
```

All four rows lie in `Q`, because their defining root covectors annihilate
`n=(e_2,e_2,0)`.  Let `ell in D_0 intersect D_1`.  Expressing `ell` in the
opposite diagonal plane and using permanent symmetry with (14) gives

```text
F_0(ell)=F_1(ell)=0.                                 (31)
```

Equation (16), independence of `T_0,T_1`, and (17) therefore imply

```text
D_0 intersect D_1 subset span(q_2).                  (32)
```

## 5. Exhaustive exclusion when both diagonal planes have dimension two

Assume `dim D_0=dim D_1=2`.  Their intersection is nonzero by dimension, and
(32) confines it to one line; hence

```text
D_0 intersect D_1=span(c)=span(q_2).                 (33)
```

The two cross zeros also give

```text
F_0(D_1)=0,                    F_1(D_0)=0.           (34)
```

Each `F_i` has rank at most one.  Since their weighted difference (16) has
rank two, both have rank one, their kernels are exactly the opposite planes,
and their image lines are independent:

```text
ker F_0=D_1,                   ker F_1=D_0,
im F_0+im F_1=span(T_0,T_1).                         (35)
```

Choose `A in D_0\span(c)` and `B in D_1\span(c)`, and let `A^*,B^*` be the
basis dual to their classes in `Q/span(c)`.  Then

```text
lambda_0=a A^*+b B^*,          lambda_1=c_0 A^*+d B^*,
ad-bc_0!=0.                                           (36)
```

Thus the target cross-ratio is left unfixed:

```text
chi=[ad:bc_0]!=[1:1]                                  (37)
```

No allowed value is normalized away or specialized in the argument.

### The complete flag cover

Relative to the common line `span(c)`, the ordered row lines in either
diagonal plane have exactly three projective types:

```text
R=(c,A),              P=(A,c),              G=(A,A+c), (38)
```

and similarly with `B` in `D_1`.  Indeed, `R` and `P` are the two cases in
which one row is common.  If neither row is common, rescale representatives
against the fixed `c` so that their difference is `c`, giving `G`.  Hence the
nine pairs `RR,RP,RG,PR,PP,PG,GR,GP,GG` are exhaustive.

The symbols `R,P,G` record projective row lines.  Actual rows may carry
arbitrary nonzero scalars; those scalars change neither zero-pair planes nor
radicals or intersections.  They are restored explicitly in the `GG`
calculation below.

For the six charts

```text
RR, PP, RG, GR, PG, GP,
```

the two cross-zero planes are distinct and their intersections are,
respectively,

```text
span(c), span(c), span(B), span(A), span(B+c), span(A+c). (39)
```

Corollary 3 makes each line in (39) pure.  In every case its displayed
generator is one of the two actual rows in an independent cross-zero pair,
so Lemma 1 makes that same row two-supported.  This contradiction excludes
all six charts.

In `RP`, and symmetrically in `PR`, the cross zeros are

```text
M_(c,c)|Q=0,                    M_(A,B)|Q=0.          (40)
```

The square-zero support split in Corollary 2 makes `c` pure.  Lemma 1 makes
`A,B` a conjugate pair in two sources.  Nonvanishing of `Alt(A,B,c)` puts
`c` in the third source.  Both diagonal maps then have image in the single
line spanned by the corresponding three-factor pure tensor, contradicting
the rank-two right side of (16).

It remains to exclude `GG`.  Retain the actual nonzero row scalars:

```text
r_0=a_0 A,          p_0=b_0(A+c),
r_1=a_1 B,          p_1=b_1(B+c),
a_0 b_0 a_1 b_1!=0.                               (41)
```

The cross zeros imply

```text
M_(A,c)=M_(B,c)=-M_(A,B).                           (42)
```

Consequently

```text
M_(A-B,A-B)|Q
 =F_0/(a_0 b_0)+F_1/(a_1 b_1).                     (43)
```

The two summands in (43) retain the independent kernels and image lines from
(35).  Thus the square map has rank two and image exactly
`span(T_0,T_1)`.  The S2AL tangent-line separation lemma says that a square
map whose image lies in the span of two fully transverse decomposable tensors
and contains one of them has image only that one line.  This contradicts
(43), closing `GG` and hence all nine `(2,2)` flags.

## 6. The dependent diagonal-plane profiles

Because `rho,pi` are injective, each `D_i` has dimension one or two.

If `(dim D_0,dim D_1)=(1,2)`, write `D_0=span(u)`.  Both nonzero rows in
`D_0` are multiples of `u`, and (14) puts the whole two-plane `D_1` inside
`Rad_Q(u)`, contradicting (28).  Root exchange excludes `(2,1)`.

If both dimensions are one, write `D_0=span(u),D_1=span(v)`.  If `u,v` are
proportional, a cross zero makes both diagonal maps zero.  If they are
independent, Lemma 1 gives `u=x+y,v=mu(x-y)`, and

```text
M_(u,u)(q)=2x tensor y tensor q_Z,
M_(v,v)(q)=-2mu^2 x tensor y tensor q_Z.             (44)
```

The two diagonal maps are proportional.  In either fork, the left side of
(16) has rank at most one, contradicting its rank-two right side.

All four profiles `(2,2),(1,2),(2,1),(1,1)` are impossible.  Therefore the
canonical binomial residual (2) is empty.

## 7. Proof-topology consequence

Up to the target stabilizer specified above, this theorem excludes exactly

```text
x,y,w in k^times e_t,
C=kappa_d e_d tensor e_d+kappa_e e_e tensor e_e,
{d,e,t}={0,1,2},                    kappa_d kappa_e!=0. (45)
```

Here `x=y=w=e_t` is only the chosen normalized representative; (45) is the
invariant orbit statement.  The continuous coefficient ratio is arbitrary.
This is a genuine nonmonomial target-coupled exclusion, but it is not an
atlas theorem.  S2BQ forces `w` coordinate for a nonmonomial residual; it
does not force the three shared-factor lines to agree, does not force two
complementary diagonal terms, and supplies no target-preserving degeneration
to (45).  Full-sensor rank and `Alt(Q)` can also drop on a projective
boundary.

```text
canonical complementary-diagonal binomial residual: IMPOSSIBLE;
all other nonmonomial rank-eight residuals:          OPEN;
diagonal monomial coordinate endpoints:              OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.      (46)
```

## 8. Focused replay

From repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_canonical_binomial_residual_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_canonical_binomial_residual_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_canonical_binomial_residual_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_canonical_binomial_residual_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_canonical_binomial_residual_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_canonical_binomial_residual_exclusion.py
```

The primary replay checks the canonical derivative, complete target
annihilator relations, every support branch of Lemma 1, the radical bound,
the full nine-flag incidence table, the scalar-correct `GG` identity, and the
dependent profiles with SymPy.  The independent no-import audit reverses
traversal and permutation order, uses standard-library `Fraction` arithmetic,
and separately reconstructs the coefficient, zero-pair, flag, rank, and
tangent-line interfaces.

## Dependencies

- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Support-one tangent-line separation](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)

## Scope boundary

```text
characteristic-zero canonical-binomial exclusion:    PROVED;
full-sensor alternating three-space interface:       PROVED;
zero-pair support classification:                    PROVED;
nine-flag projective coverage:                       PROVED;
continuous target cross-ratio:                       RETAINED;
general nonmonomial atlas/degeneration bridge:       OPEN;
diagonal monomial coordinate endpoints:              OPEN;
other lower-rank cells, components, poles, higher m: OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.      (47)
```
