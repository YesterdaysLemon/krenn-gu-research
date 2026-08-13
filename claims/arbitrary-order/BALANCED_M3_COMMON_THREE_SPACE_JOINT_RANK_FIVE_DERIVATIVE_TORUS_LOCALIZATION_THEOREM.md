# Balanced `m=3` common-three-space joint-rank-five derivative and torus localization

## Status

**Exact characteristic-zero localization of every joint-cross-rank-five point
on the normalized, target-consistent physical `m=3` common-three-space
stratum.**  Let `U` be the total singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

The following alternatives are exhaustive.

1. Exactly two root--root blocks are nonzero.  Their derivative summands are
   disjoint, so the shared derivative has rank six.  The uninvolved root-row
   map has rank exactly two.  Its one-dimensional kernel has target-coordinate
   support at most two.
2. All three root--root blocks are nonzero.  The shared derivative has rank
   seven, its two-dimensional Hilbert--Burch kernel is contained in `K`, and
   the three kernel-projection dimensions are, up to root permutation,

   ```text
   (1,2,2),                  (1,1,2),                  (1,1,1).   (2)
   ```

   The full `(2,2,2)` profile is impossible.  Each profile in (2) lies on the
   explicit target-coordinate boundaries in Section 4.

In particular, the rank-five shared-factor derivative is impossible without
any assumption on `rank H`, and a transverse two-root rank-five point with an
injective uninvolved row is impossible.  This is a localization, not a
complete joint-rank-five exclusion.  By itself it leaves the rank-two-row
and Hilbert--Burch coordinate boundaries, joint ranks at most four, the other
S2T/S2Q component types, higher orders, the all-rank-drop branch, a witness,
and a counterexample open.  Global Krenn--Gu remains **UNRESOLVED**.

The successor chain S2AH--S2AM now excludes every transverse two-root
rank-five row/support profile.  S2AN--S2AP exclude the complete
repeated-coordinate part of the `(1,1,1)` Hilbert--Burch atlas, and S2AQ
excludes the all-coordinate-distinct triangle.  The chart with exactly two
distinct coordinate factors and a genuinely noncoordinate third factor, and
the other Hilbert--Burch profiles, remain open; these successors do not
change the scope or proof of the localization below.

## 1. The shared-factor derivative is rank-free impossible

We first remove an unnecessary rank assumption from S2AC.  Suppose at least
two root--root blocks are nonzero and the shared derivative has rank five.
The pairwise intersection lemma of S2U and the three-summand syzygy bound of
S2X give, after permuting roots,

```text
B_23=y tensor z,              B_13=x tensor z,
B_12=0,

D_B(a,b,c)=(a tensor y+x tensor b) tensor z.          (3)
```

Thus `U=U_0 tensor z` for a three-plane `U_0`.  If `z` were not a target
coordinate, its annihilator would contain a fully supported covector and
would give a forbidden fully supported product annihilator of `U`.  Hence,
for one colour `s`,

```text
z=e_(3,s),                    G_N in J+U_0 tensor e_(3,s). (4)
```

Let `t,u` be the other colours and write the involved transposed rows as

```text
r_a=rho(e_a^*),              p_b=pi(e_b^*),
q_c=theta(e_c^*).                                    (5)
```

The two root-3 slices unaffected by (4) are

```text
per(r_a,p_b,q_v)=delta_(a,v) delta_(b,v) T_v,
v=t,u,                                               (6)

T_v=X_v tensor Y_v tensor Z_v.                       (7)
```

Equation (6) forces `rank rho,rank pi>=2`.  If both ranks are two, their
kernels are the missing coordinate line `span(e_s^*)`.  Then every element
of `K` has first and second components with zero `s` coordinate.  The
`(s,s,s)` target coefficient cannot be supplied by `U_0`, a contradiction.

If both ranks are three, evaluate the source components and form the two
`3 x 3` row matrices `R,P`.  The two slices in (6) say

```text
R M(q_t) P^T=mu_t E_(t,t),
R M(q_u) P^T=mu_u E_(u,u),                            (8)
```

where generically `mu_t mu_u!=0` and `M(q)` is the symmetric zero-diagonal
matrix of the three source components of `q`.  The two independent target
row and column lines force `R,P` generically invertible.  But a nonzero
zero-diagonal `3 x 3` matrix has rank at least two and cannot become the
rank-one right side of (8).

In the remaining mixed profile, say `rank rho=2,rank pi=3`, one has `r_s=0`
and the three `p_b` form a basis of a three-plane `V`.  The zero rows of the
two unaffected slices promote coefficientwise to

```text
r_u*q_t=0,                 r_t*q_u=0,                 (9)
r_t*q_t!=0,                r_u*q_u!=0.               (10)
```

The derivatives of the two nonzero products on `V` are rank-one maps with
independent coefficient covectors and images `T_t,T_u`.  The rank-free
crossed-pair diagonal lemma of S2AC excludes every pure/pure, pure/mixed, and
mixed/mixed zero-product form.  The opposite mixed profile is symmetric.

No step after the normal form (3) uses `rank H`.  Therefore

```text
at least two root blocks and rank D_B=5:  IMPOSSIBLE  (11)
```

at every joint rank under the common-three-space target hypotheses.

## 2. The rank-five derivative census

Return to (1).  Since `D_B(K)=U`, rank--nullity on the restriction gives

```text
dim(K intersect ker D_B)=rank K-rank U=2.             (12)
```

The quotient `A/K` has dimension four, so

```text
rank D_B<=rank(D_B restricted to K)+dim(A/K)=3+4=7.  (13)
```

S2AB excludes exactly one nonzero root block at every joint rank.  With
exactly two nonzero blocks, their two three-dimensional derivative summands
have intersection zero or one.  Their derivative rank is therefore six or
five.  Equation (11) removes rank five, leaving the transverse rank-six
case.

If all three blocks are nonzero, the S2X syzygy lemma gives
`dim ker D_B<=2`, hence `rank D_B>=7`.  Equality holds in (13), and (12)
becomes

```text
rank D_B=7,                 ker D_B subset K,
K=D_B^(-1)(U).                                      (14)
```

These alternatives exhaust the rank-five derivative topology.

## 3. The transverse case has a rank-two uninvolved row

Assume exactly `B_23=B` and `B_13=C` are nonzero and their derivative
summands are disjoint.  Then

```text
D_(B,C)(a,b,c)=a tensor B+C tensor b,
ker D_(B,C)=A_3.                                     (15)
```

Let

```text
N_3=K intersect A_3,                 dim N_3=2,
P=pr_(1,2) K subset A_1 direct-sum A_2, dim P=3.     (16)
```

The restriction of (15) to `A_1 direct-sum A_2` is injective, so

```text
U=D_(B,C)(P).                                        (17)
```

Put `L=P^perp`, and let `V=image rho+image pi`.  Then

```text
dim L=3,                       dim V=3.               (18)
```

The relation-plane and beta-zero arguments of S2AD use only (17)--(18), not
the containment `A_3 subset K` specific to joint rank six.  They therefore
give the same exhaustive alternatives: either `L` lies in a target-coordinate
hyperplane, or an involved row has rank two with coordinate kernel and the
aligned diagonal block contraction.

Let `Q=image theta`.  Because `pr_3 K` contains the two-plane `N_3`,

```text
rank theta=dim pr_3 K in {2,3}.                       (19)
```

If `rank theta=3`, the rows `q_c` fill a three-plane.  The proofs of S2AE
and S2AF now apply without change.  In the non-coordinate alternative their
graph identity, permanent symmetry, repeated-row tangent reduction, and
square-pencil lemma use only that `Q` is a three-plane.  In the coordinate
alternative the `(3,2)` binary five-product argument and the `(2,2)`
square-pencil factor-sharing argument likewise use only the dimension of
`Q` (or the proved two-dimensional rank of its local projection).  Neither
proof uses `V intersect Q=0`.  Both alternatives are impossible.  Hence

```text
rank theta=2,                  dim(V direct-sum Q)=5. (20)
```

Let `eta` span `ker theta`.  Then `(0,0,eta) in K^perp`, and (16) implies

```text
N_3=eta^perp,                  K=P direct-sum N_3.    (21)
```

Contract the two root blocks by `eta` in their third-root factor:

```text
b_eta=(id tensor eta)(B) in A_2,
c_eta=(id tensor eta)(C) in A_1.                     (22)
```

Since `q_eta=0`, the empty permanent vanishes after the same contraction.
For every colour `i` in the coordinate support of `eta`, target consistency
therefore requires

```text
e_(1,i) tensor e_(2,i) in eta(U)
 subset A_1 tensor b_eta+c_eta tensor A_2.            (23)
```

A nonzero decomposable tensor in
`A_1 tensor b_eta+c_eta tensor A_2` has first factor on `c_eta` or second
factor on `b_eta`: project to
`(A_1/span(c_eta)) tensor (A_2/span(b_eta))`.  Consequently the fixed pair
of lines `span(c_eta),span(b_eta)` can cover at most two distinct coordinate
diagonals in (23).  Thus

```text
|support eta|<=2.                                    (24)
```

If equality holds, both contractions in (22) are nonzero and, in one order,
their lines are exactly the two target-coordinate lines in `support eta`.
Equations (20)--(24) are the new transverse rank-five boundary.

## 4. The three-block Hilbert--Burch torus atlas

Assume all three root blocks are nonzero.  By (14), choose a basis of the
two-dimensional derivative kernel.  The equality case of the S2X
Hilbert--Burch argument gives vectors

```text
x,b in A_1,                 y,c in A_2,
z,w in A_3                                            (25)
```

such that

```text
ker D_B=span{(x,y,z),(b,c,w)},                        (26)

B_23=y tensor w-c tensor z,
B_13=b tensor z-x tensor w,
B_12=x tensor c-b tensor y.                          (27)
```

Each projection

```text
P_1=span(x,b),       P_2=span(y,c),       P_3=span(z,w) (28)
```

has dimension one or two.  It cannot have dimension zero because all three
blocks in (27) are nonzero.

For root covectors `alpha,beta,gamma`, define the evaluation pairs

```text
A=(alpha(x),alpha(b)),
B=(beta(y),beta(c)),
C=(gamma(z),gamma(w)).                               (29)
```

The three root-block contractions are, up to harmless signs,

```text
det(B,C),                    det(A,C),
det(A,B).                                             (30)
```

When all three determinants vanish, the product functional
`alpha tensor beta tensor gamma` annihilates `image D_B`, hence annihilates
`U`.  S2R forbids such a product when all nine coordinate evaluations are
nonzero.

If the profile in (28) is `(2,2,2)`, all three restriction maps to the pair
space are surjective.  Choose one common pair in (29) and independently add
the one-dimensional annihilator of each `P_i`.  This five-dimensional
parameter space projects onto every `A_i^*`; none of the nine coordinate
evaluations vanishes identically.  Over an infinite field a point avoids
their finite union of hyperplanes, producing a fully supported product with
(30) zero.  This contradicts S2R.  Therefore `(2,2,2)` is impossible.

For the remaining profiles, row operations in (26) give the following
normal forms and necessary coordinate-boundary conditions.  Here
"coordinate" means proportional to one of the three target basis vectors in
the indicated root space.

### Profile `(1,2,2)`

After permuting roots,

```text
ker D_B=span{(x,y,z),(0,c,w)},
dim span(y,c)=dim span(z,w)=2.                        (31)
```

The beta-zero locus has two components.  The first has `alpha(x)=0` and
arbitrary proportional pairs `B,C`; the second has arbitrary `alpha` and
`beta(c)=gamma(w)=0`.  Avoidance of a fully supported point on each component
forces

```text
x is coordinate,
and at least one of c,w is coordinate.                (32)
```

### Profile `(1,1,2)`

After permuting roots,

```text
ker D_B=span{(x,0,z),(0,y,w)},
dim span(z,w)=2.                                     (33)
```

The three beta-zero components respectively impose

```text
x coordinate or y coordinate,
x coordinate or z coordinate,
y coordinate or w coordinate.                       (34)
```

Equivalently, the allowed coordinate pairs are

```text
(x,y),                 (x,w),                 (y,z), (35)
```

with additional coordinates permitted.

### Profile `(1,1,1)`

The three blocks are a rank-one triangle.  Normalize

```text
ker D_B=span{(x,0,z),(0,y,z)}.                        (36)
```

The beta-zero ideal has the three components on which two of
`alpha(x),beta(y),gamma(z)` vanish.  S2R forces

```text
x coordinate or y coordinate,
x coordinate or z coordinate,
y coordinate or z coordinate.                       (37)
```

Thus at least two of `x,y,z` are target-coordinate vectors.

The conditions (32), (34), and (37) are necessary, not exclusions.  They are
the complete beta-zero coordinate-boundary atlas for the three-block
rank-seven equality case.

## 5. Proof-topology consequence

Together with S2AB--S2AF, the common-three-space joint-rank frontier is now

```text
joint rank >=6:                                      IMPOSSIBLE;

joint rank 5, two blocks, derivative rank 5:         IMPOSSIBLE;
joint rank 5, two blocks, derivative rank 6,
  uninvolved row rank 3:                             IMPOSSIBLE;
joint rank 5, two blocks, derivative rank 6,
  uninvolved row rank 2 and support <=2:             OPEN;

joint rank 5, three blocks, Hilbert--Burch (2,2,2):  IMPOSSIBLE;
joint rank 5, three blocks, profiles in (2),
  on the coordinate atlas (32)/(34)/(37):            OPEN;

joint rank at most 4 / other physical branches:      OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (38)
```

The next exact rank-five obligations are the transverse rank-two uninvolved
row in (20)--(24) and the three Hilbert--Burch coordinate atlases.  No finite
scan, numerical search, or generic-point promotion is used.

The later support-profile chain S2AH--S2AM has now closed the first of those
two obligations.  S2AN--S2AP close the repeated-coordinate `(1,1,1)` chart,
and S2AQ closes its all-coordinate-distinct triangle.  The chart with exactly
two distinct coordinate factors and a genuinely noncoordinate third factor,
and the other two coordinate atlases, remain open.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_derivative_torus_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_derivative_torus_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_derivative_torus_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_derivative_torus_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_derivative_torus_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_derivative_torus_localization.py
```

The primary replay checks the rank-free shared-factor normal form, the
rank-five derivative census, both transverse row-rank models, all four
Hilbert--Burch projection profiles, their exact kernels and beta-zero ideals,
and the coordinate-boundary Boolean table.  The independent no-import audit
reconstructs the derivative and contraction matrices with `Fraction`
elimination and a separate row-oriented atlas.  The arbitrary-vector,
irreducibility, and finite-hyperplane-avoidance arguments above are the proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
