# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` coordinate-coloop localization

## Status

**Exact characteristic-zero localization of the complete `(1,2,2)`
Hilbert--Burch coordinate atlas on the normalized, target-consistent physical
`m=3` common-three-space full-sensor stratum.**  Let `U` be the total
singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AG profile

```text
ker D_B=span{(x,y,z),(0,c,w)},
dim span(y,c)=dim span(z,w)=2.                        (2)
```

S2AG proves that `x` is a target-coordinate vector and at least one of
`c,w` is a target-coordinate vector.  Interchanging roots two and three
interchanges the latter alternatives.  Hence assume

```text
x=lambda e_s,                 c=mu e_t,
lambda mu!=0.                                        (3)
```

Adding a multiple of the second kernel generator to the first preserves
(2)--(3).  Use this unique gauge to arrange

```text
y_t=0.                                                (4)
```

Then the four-dimensional relation kernel `N=K^perp` lies in one of the
nine ordinary root-coordinate hyperplanes

```text
alpha_i=0,             beta_j=0,             gamma_k=0.
                                                               (5)
```

Moreover, put `R=rho(e_s^perp)`.  The map `rho|e_s^perp` is injective, so
`R` is a two-plane.  If the hyperplane in (5) is `alpha_s=0`, any
`beta_j=0`, or any `gamma_k=0`, the other six annihilator rows have image
exactly `R`.  The only two alternatives not of this equal-`R` type are

```text
alpha_a=0,                    alpha_b=0,              (6)
```

where `a,b` are the two colours different from `s`.

Here "not of this equal-`R` type" means that containment of the pure
`e_s^perp` copy no longer forces their six-row images to equal `R`; it does
not assert that either image is disjoint from, or unequal to, `R` at every
point.

This is a localization, not yet an exclusion of `(1,2,2)`.  It leaves the
seven equal-`R` coloop orientations and the two complementary first-root
coloops in (6), joint rank at most four, other physical component types,
higher orders, and global resolution open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Gauge-fixed derivative

The Hilbert--Burch blocks are

```text
B_23=y tensor w-mu e_t tensor z,
B_13=-lambda e_s tensor w,
B_12= lambda mu e_s tensor e_t.                      (7)
```

Thus

```text
D_B(a,b,d)
 =a tensor(y tensor w-mu e_t tensor z)
  -lambda e_s tensor b tensor w
  +lambda mu e_s tensor e_t tensor d.                (8)
```

The two vectors in (2) vanish under (8), and its rank is seven.  The first
summand has rank three because the matrix

```text
y tensor w-mu e_t tensor z                           (9)
```

has rank two: `y,e_t` are independent by (2), as are `z,w`.  The second and
third derivative summands complete the Hilbert--Burch equality case already
proved in S2AG.

The gauge (4) is exact.  Before gauging, replace

```text
(x,y,z) by (x,y-(y_t/mu)c,z-(y_t/mu)w).              (10)
```

The span of the kernel and all blocks in (7) are unchanged, while the new
second component has zero `t` coordinate.  Independence in (2) is
unchanged by adding a multiple of the other projected vector.

## 2. Transpose recovery and the nine-coordinate fork

The annihilator of the derivative kernel is

```text
L=(ker D_B)^perp
 ={(alpha,beta,gamma):
      lambda alpha_s+beta(y)+gamma(z)=0,
      mu beta_t+gamma(w)=0},             dim L=7.    (11)
```

For a product root functional, transpose of (8) is

```text
D_B^T(alpha tensor beta tensor gamma)
 =((beta(y)gamma(w)-mu beta_tgamma(z))alpha,
   -lambda alpha_sgamma(w)beta,
    lambda mu alpha_sbeta_tgamma).                   (12)
```

On `L`, equations (11) give

```text
beta(y)gamma(w)-mu beta_tgamma(z)
 =lambda mu alpha_sbeta_t,

-lambda alpha_sgamma(w)
 =lambda mu alpha_sbeta_t.                           (13)
```

Therefore the exact self-recovery identity is

```text
D_B^T(alpha tensor beta tensor gamma)
 =lambda mu alpha_sbeta_t(alpha,beta,gamma),
                              (alpha,beta,gamma) in L. (14)
```

Put

```text
N=K^perp subset L,       dim N=4,
V=H^T(L),                dim V=3.                    (15)
```

If an element of `N` has all nine target-coordinate evaluations nonzero,
then (14) makes its product functional a fully supported annihilator of
`U=D_B(K)`, contrary to S2R.  Hence `N` is covered by the nine hyperplanes
in (5).  Each restricted coordinate form is nonzero on `L`: the two kernel
vectors in (2) have no pure-coordinate annihilator because all their stated
projections are nonzero.  Over the infinite characteristic-zero field, a
vector space cannot be the union of finitely many proper subspaces.  Thus
`N` is contained in one fixed hyperplane in (5).

If `F subset L` is that hyperplane, then

```text
dim H^T(F)=dim F-dim N=6-4=2.                         (16)
```

This is the exact coordinate-coloop fork.

## 3. Canonical seven rows and the fixed two-plane

Write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),

A=lambda^(-1)r_s,     B=mu^(-1)p_t.                 (17)
```

For `i!=s`, `j!=t`, and every `k`, define

```text
g_j=p_j-y_jA,
h_k=q_k-z_kA-w_kB.                                  (18)
```

The seven rows

```text
(r_i)_(i!=s),        (g_j)_(j!=t),        h_0,h_1,h_2 (19)
```

lie in `V`, are the images of a basis of `L`, and span `V`.  Modulo `V`,

```text
r(alpha) congruent lambda alpha_sA,
p(beta) congruent beta(y)A+mu beta_tB,
q(gamma) congruent gamma(z)A+gamma(w)B.              (20)
```

Let

```text
R=rho(e_s^perp)=span(r_a,r_b).                       (21)
```

This is a two-plane.  Indeed, if `0!=alpha in e_s^perp` and
`r(alpha)=0`, then `alpha` annihilates the first projection of every vector
of `K=image H`.  Contracting (8) by `alpha` in its first factor therefore
kills `D_B(K)=U`; the other two summands are already killed by
`alpha_s=0`.  The same contraction kills the all-cross term because
`r(alpha)=0`, but the target contraction

```text
sum_i alpha_iT_i                                    (22)
```

is nonzero.  This contradicts the complete target equation.  Hence

```text
dim R=2.                                              (23)
```

The pure elements `(alpha,0,0)` with `alpha_s=0` belong to `L`.  Therefore
the six-dimensional hyperplanes

```text
alpha_s=0,                 beta_j=0,                 gamma_k=0 (24)
```

all contain this copy of `e_s^perp`, and their row images contain `R`.
Equations (16) and (23) force every one of those seven images to equal `R`.

For `alpha_a=0` or `alpha_b=0`, the pure-coordinate argument guarantees only
one line of `R` in the six-row image; it does not determine whether another
row supplies the missing line at a special point.  These are the two residual
first-root coloop orientations in (6).  The alternatives in (24) and (6)
exhaust all nine coordinate hyperplanes.

## 4. Proof-topology consequence

S2AG and this theorem refine the remaining rank-five three-block frontier to

```text
Hilbert--Burch (1,1,1):                              IMPOSSIBLE;
Hilbert--Burch (1,1,2):                              IMPOSSIBLE;

Hilbert--Burch (1,2,2):
  after root symmetry and kernel gauge,
  x=lambda e_s, c=mu e_t, y_t=0;
  one of nine coordinate coloops:
    alpha_s / any beta_j / any gamma_k: six rows -> R;
    alpha_a or alpha_b: complementary first-root coloop;
                                                      OPEN.      (25)
```

No claim is made about lower joint rank, another physical component type,
higher order, or the global conjecture.

## Focused replay

```bash
python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_coordinate_coloop_localization.py
python claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_coordinate_coloop_localization.py
```

The primary replay checks the gauge, blocks, derivative, rank, kernel,
annihilator, transpose recovery, nine proper coordinate restrictions,
canonical seven-row parameterization, and the two-dimensional fixed-plane
argument exactly.  The independent audit reconstructs those identities with
standard-library rational arithmetic and its own Gaussian elimination.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Singleton-span torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [`(1,1,2)` outer-coordinate-chart exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_OUTER_COORDINATE_CHART_EXCLUSION_THEOREM.md)
