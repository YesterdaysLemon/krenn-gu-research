# Balanced `m=3` common-three-space transverse-rank-six aligned-rank-two exclusion

## Status

**Exact characteristic-zero exclusion of the aligned-rank-two alternative in
the transverse joint-rank-six common-three-space branch.**  Retain the
normalized, target-consistent physical `m=3` hypotheses and notation of S2AD:

```text
dim U=3,                     rank H=6,
B_23=B!=0,                  B_13=C!=0,        B_12=0,
rank D_(B,C)=6.                                      (1)
```

Assume that the relation three-plane is not contained in a target-coordinate
hyperplane.  S2AD then forces an involved root-row map to have rank two, with
coordinate kernel, aligned diagonal contraction, and both relation-plane
block contractions on the same target line.  No such data satisfy the full
empty-permanent target equation.

Consequently, at joint rank six the only surviving common-three-space
transverse mechanism has its relation plane contained in one of the six
coordinate hyperplanes.  That coordinate-relation branch, joint rank at most
five, the other physical branches, higher orders, a witness, and a
counterexample remain open.  Global Krenn--Gu remains **UNRESOLVED**.

The proof is exact.  No generic point is promoted across an exceptional
factor: the few choices of covectors use only the infinitude of a
characteristic-zero field, while all rank drops are treated as separate
cases in Lemma 1 below.

## 1. The rank-two row makes the joint image a graph

After exchanging the first two roots if necessary and permuting target
coordinates, let the rank-two row be

```text
pi:A_2^* -> W^*,          ker pi=span(e_0^*),
(e_0^* tensor id)(B)=kappa e_0,       kappa!=0,       (2)
```

where `W=X direct-sum Y direct-sum Z`.  Write

```text
r_a=rho(e_a^*),       p_b=pi(e_b^*),       q_c=theta(e_c^*).
                                                            (3)
```

Thus `p_0=0`.  We first show

```text
rank rho=3.                                             (4)
```

If `rho` also had rank two, S2AD's symmetric conclusion would give
`r_0=0`.  Every vector `(a,b)` of `K_12` would then have `a_0=b_0=0`.
But the root-2 coordinate-zero slice of the empty permanent is zero, whereas
the same slice of the target contains

```text
e_0 tensor e_0  T_0,          T_i=X_i tensor Y_i tensor Z_i. (5)
```

Target consistency says that its negative is the corresponding slice of an
element of `U=D_(B,C)(K_12)`.  By (2), that slice is

```text
kappa a tensor e_0.                                    (6)
```

It requires `a` to be a nonzero multiple of `e_0`, a contradiction.
This proves (4).

Since `dim pr_2 L=rank rho=3`, the first relation-plane inclusion of S2AD
gives

```text
B=b tensor e_0,                b_0=kappa.              (7)
```

Moreover `pr_1:K_12->A_1` is an isomorphism: a vector `(0,b')` in
`K_12` is annihilated by all of `pr_2 L=A_2^*` and hence is zero.  Therefore
there is a rank-two map

```text
T:A_1->A_2,
K_12={(a,Ta):a in A_1},       (Ta)_0=0,               (8)
L={(-T^*v,v):v in A_2^*}.                              (9)
```

The density of `L^circ` says in particular that no coordinate of `T^*v`
vanishes identically.  Equivalently,

```text
T e_0, T e_1, T e_2 are all nonzero.                  (10)
```

Every joint cross column belongs to `A_3 direct-sum graph(T)`, so (3)
satisfies the exact row relation

```text
p_b=sum_a T_(b,a) r_a.                                (11)
```

## 2. The torus atlas makes the aligned block diagonal

We claim that (7) sharpens to

```text
B=kappa e_0 tensor e_0.                               (12)
```

Suppose instead that `b` is not a coordinate vector.  There is then a fully
supported covector annihilating `b`.  For every fully supported third-root
covector `gamma`, the no-beta-zero-torus condition forces `C(gamma)` to be a
nonzero coordinate vector: otherwise a fully supported first-root covector
would annihilate it as well.  Irreducibility fixes that coordinate line, and
nonvanishing on the whole torus makes the scalar third-root form a coordinate
form.  Thus

```text
C=e_j tensor e_r                                      (13)
```

up to a nonzero scalar.

The second S2AD relation-plane inclusion is

```text
C^T(im T^*) subset span(e_0),                         (14)
```

or equivalently

```text
(T tensor id)C in A_2 tensor span(e_0).               (15)
```

By (10), `T e_j!=0`; applying (15) to (13) forces `r=0`.  But then
`A_1 tensor B` and `C tensor A_2` meet in the nonzero tensor
`e_j tensor b tensor e_0`, contradicting `rank D_(B,C)=6`.  Hence `b` is a
coordinate vector.  Its nonzero zeroth entry in (7) proves (12).

## 3. Target consistency is one exact polynomial identity

Let `M` be any nonroot monomial.  Target consistency supplies a unique
`a_M in A_1` such that the `M` coefficient of `G_N-J` is

```text
D_(B,C)(a_M,T a_M)
 =a_M tensor B+C tensor T a_M.                        (16)
```

Uniqueness follows from the injectivity of `D_(B,C)` on `K_12`.  Contract
(16) in the zeroth second-root coordinate.  Because `p_0=0`, `(Ta_M)_0=0`,
and (12) holds, that contraction is `kappa a_M tensor e_0`.  It vanishes for
every `M!=T_0`, while for `M=T_0` it equals
`-e_0 tensor e_0`.  Put

```text
t=T e_0!=0.                                           (17)
```

Coefficient comparison gives the full, uncontracted identity

```text
G_N
 =J-kappa^(-1) T_0 D_(B,C)(e_0,t)
 =T_1 E_111+T_2 E_222-kappa^(-1)T_0 C tensor t.       (18)
```

Here `C tensor t` is inserted in root order `A_1 tensor A_2 tensor A_3`.
Unlike a selected slice, (18) accounts for every one of the 27 nonroot
monomials.

## 4. Permanent symmetry gives the last block normal form

Fix a third-root index `c` and a nonroot monomial `M`.  Let `F_(c,M)` be the
`3 x 3` matrix, in first- and second-root indices, of the corresponding
coefficient of

```text
per(r_a,p_b,q_c).                                     (19)
```

By (11),

```text
F_(c,M)=S_(c,M) T^T,                                  (20)
```

where `S_(c,M)` is symmetric because the permanent is symmetric in the two
rows `r_a,r_d`.  Consequently

```text
T F_(c,M)=T S_(c,M) T^T is symmetric.                 (21)
```

For `M=T_i`, `c=i`, and `i=1,2`, equation (18) gives
`F_(i,T_i)=E_(i,i)`.  Hence `(T e_i)e_i^T` is symmetric.  Combining this
with (10),

```text
T e_1=tau_1 e_1,       T e_2=tau_2 e_2,
tau_1 tau_2!=0,                                       (22)
T e_0=t_1 e_1+t_2 e_2,       (t_1,t_2)!=(0,0).        (23)
```

Let `k` span `ker T`, normalized by `k_0=1`; explicitly,

```text
k=e_0-(t_1/tau_1)e_1-(t_2/tau_2)e_2.                 (24)
```

Write `C_c` for the `c`-th third-root column of `C`.  Equation (15) says

```text
T C_1=T C_2=0.                                       (25)
```

For the `T_0` coefficient, (18) gives

```text
F_(c,T_0)=-kappa^(-1) C_c t^T.                       (26)
```

At `c=0`, (21) makes `(T C_0)t^T` symmetric, so `T C_0=lambda t` for one
scalar `lambda`.  Equations (24)--(25) now yield

```text
C=lambda e_0 tensor e_0+k tensor w                   (27)
```

for one `w in A_3`.

## 5. A repeated-row tangent forces `lambda=0`

Choose a second-root covector `beta` with

```text
beta_1 beta_2 beta(t)!=0,
```

and put `alpha=T^* beta`.  Then (11) gives

```text
r_alpha=p_beta.                                      (28)
```

Choose a fully supported third-root covector `gamma`.  Contracting (18) by
`alpha tensor beta tensor gamma` gives a diagonal nonroot tensor with
coefficients

```text
T_1: tau_1 beta_1^2 gamma_1,
T_2: tau_2 beta_2^2 gamma_2,
T_0: -kappa^(-1) lambda gamma_0 beta(t)^2.            (29)
```

If `lambda!=0`, all three are nonzero.  The resulting diagonal tensor has
flattening rank three in every nonroot mode.

On the physical side, (28) makes the same contraction

```text
per(u,u,q)
 =2(u_X tensor u_Y tensor q_Z
    +u_X tensor q_Y tensor u_Z
    +q_X tensor u_Y tensor u_Z),                     (30)
```

where `u=r_alpha` and `q=q_gamma`.  In each mode (30) uses at most the two
factor lines supplied by `u` and `q`, so every flattening rank is at most
two.  This contradicts (29).  Therefore

```text
lambda=0,                 C=k tensor w.               (31)
```

The rank-six hypothesis in particular keeps `w` nonzero and prevents it
from being proportional to `e_0`; those facts are not needed for the final
lemma.

## 6. Symmetric binary-diagonal obstruction

For `u,v in W`, let `D_(u*v):W->X tensor Y tensor Z` be the polarization

```text
D_(u*v)(q)=per(u,v,q).                                (32)
```

### Lemma 1 (a square pencil cannot carry two disjoint diagonals)

Let `Q subset W` be a three-plane.  There do not exist nonzero `u,v` such
that

```text
D_(u*v)|_Q=0,                                        (33)
D_(u*u)|_Q and D_(v*v)|_Q are nonzero rank-one maps  (34)
```

whose image tensors are decomposable and have distinct factor lines in each
of `X,Y,Z`.

### Proof

Write `u=(x,y,z)`, `v=(x',y',z')` and form the three pair tensors

```text
A=y tensor z'+y' tensor z,
B=x tensor z'+x' tensor z,
C=x tensor y'+x' tensor y.                           (35)
```

Then

```text
D_(u*v)(q)=q_X tensor A+B tensor q_Y+C tensor q_Z.   (36)
```

We separate the exact number of nonzero tensors in (35).

**Three.**  The three-nonzero-summand syzygy lemma gives
`dim ker D_(u*v)<=2`, contradicting (33).

**Zero.**  The zero-product classification says that `u,v` are either pure
in one common source or, after permuting sources, proportional to
`x+y,x-y`.  In the pure case both square derivatives vanish.  In the mixed
case the two square derivatives are proportional and have the same two
fixed factor lines.  Neither satisfies (34).

**One.**  Suppose only `C` is nonzero.  Then `Q subset X direct-sum Y`.
If `z=z'=0`, both square derivatives vanish on this kernel.  Otherwise the
two zero equations force, up to a scalar,

```text
v=(-x,-y,z).                                         (37)
```

The two square derivatives on `X direct-sum Y` are nonzero scalar multiples
of one another.  Again their image lines cannot have three distinct target
factors.  The cases with only `A` or only `B` are symmetric.

**Two.**  Suppose `A,B` are nonzero and `C=0`.  The whole source summand `Z`
lies in the kernel.  If `A,B` have no shared third factor, it is the entire
kernel; each square derivative on a three-plane `Z` has rank zero or three.
If they do share a third factor, the pairwise intersection lemma gives

```text
ker D_(u*v)=Z direct-sum ell                         (38)
```

for one line `ell`.  A boundary solution of `C=0` makes one of `u,v` pure
in `Z`, so its square derivative is zero.  Otherwise

```text
x'=a x,                  y'=-a y                    (39)
```

with `x,y` nonzero.  Every vector of `ell` has its `X,Y` components on the
lines `x,y`.  Thus `D_(u*u)` maps (38) onto

```text
span(x tensor y) tensor Z                            (40)
```

and its kernel inside (38) has dimension at most one; its restriction to
the three-plane `Q` has rank at least two.  This contradicts (34).  The
other choices of two nonzero pair tensors are symmetric.  The four cases
are exhaustive.  QED.

## 7. The aligned rank-two contradiction

Under (31), the correction in (18) vanishes whenever the first-root covector
annihilates `k`.  The plane `k^perp=im T^*` has the basis

```text
alpha^(1)=(t_1/tau_1,1,0),
alpha^(2)=(t_2/tau_2,0,1).                           (41)
```

Put

```text
u_i=r_(alpha^(i)),
beta^(1)=tau_1^(-1)e_1^*,
beta^(2)=tau_2^(-1)e_2^*.                            (42)
```

Equations (22)--(23) give `T^*beta^(i)=alpha^(i)`, so
`p_(beta^(i))=u_i`.  Contracting (18) now yields, for every `gamma`,

```text
per(u_1,u_2,q_gamma)=0,
per(u_1,u_1,q_gamma)=tau_1^(-1) gamma_1 T_1,
per(u_2,u_2,q_gamma)=tau_2^(-1) gamma_2 T_2.          (43)
```

Because `theta` is injective, the vectors `q_gamma` fill the three-plane
`Q=image theta`.  Equations (43) satisfy Lemma 1, while `T_1` and `T_2` have
distinct coordinate factor lines in all three nonroot sources.  This final
contradiction excludes the aligned rank-two branch.

## 8. Proof-topology consequence

Combining S2AD with this theorem leaves the exact rank-six frontier

```text
two transverse root blocks, rank D=6;
relation plane contained in one coordinate hyperplane:       OPEN;
non-coordinate relation plane / aligned rank-two row:        IMPOSSIBLE;

joint rank at most five / other physical branches:           OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED. (44)
```

The next rank-six obligation is the full permanent equation on the
coordinate-relation-plane branch.  This theorem neither covers that branch
nor changes any lower-rank, other-component, or higher-order status.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_transverse_rank_six_aligned_rank_two_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_transverse_rank_six_aligned_rank_two_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_transverse_rank_six_aligned_rank_two_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_transverse_rank_six_aligned_rank_two_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_transverse_rank_six_aligned_rank_two_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_transverse_rank_six_aligned_rank_two_exclusion.py
```

The primary verifier replays the graph/target identity, symmetric coefficient
pullback, repeated-row tangent rank obstruction, and all four exact
mixed-product kernel cases.  The independent no-import audit reconstructs
the tensors with `Fraction` arithmetic and a separate row-oriented
implementation.  The irreducibility, coefficientwise target-consistency,
and arbitrary-subspace dimension arguments above are the proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md)
