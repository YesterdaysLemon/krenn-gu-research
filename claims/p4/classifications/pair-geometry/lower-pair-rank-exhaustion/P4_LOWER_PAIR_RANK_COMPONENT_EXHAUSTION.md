# Exhaustion of the pure `P_4` lower-pair locus

## Status

**Exact characteristic-zero component-exhaustion corollary.**  Let
`(U_0,U_1,U_2,U_3)` be a nonzero pure `P_4` compression over `C`, and put

```text
r_ij=dim(U_i U_j)       (0<=i<j<=3).                (1)
```

If `min r_ij<=2`, then in fact `min r_ij=2`, and, up to source-coordinate
and mode symmetry, the tuple belongs to one of exactly four already
certified component closures:

1. the embedded-`P_3` component;
2. the original six-dimensional lower-pair component;
3. the five-dimensional full-support tangent component fourteen;
4. the six-dimensional disjoint-secant component fifteen.

Conversely, each of those four closures has a pair image of rank at most two.
Thus their finite symmetry orbit union is exactly the nonzero lower-pair
locus of the pure `P_4` variety.

This is an exhaustion theorem for the lower-pair locus, not yet for the
entire pure `P_4` variety.  Components whose six pair images all have rank at
least three remain the component-exhaustiveness frontier.  The generic
marked `P_5` fibres of components fourteen and fifteen have since been
excluded for both `H31` and `H22`; their special boundaries remain open.

## Proof by geometric case separation

Choose a pair with `r_ij<=2`.

### Ranks zero and one

[`P4_RANK_ONE_PAIR_OBSTRUCTION.md`](../rank-one-pair-obstruction/P4_RANK_ONE_PAIR_OBSTRUCTION.md) proves
that ranks zero and one are impossible for a nonzero pure restriction.  Its
key step projectivizes the zero-product correspondence.  The squarefree
zero-product locus is a union of six projective lines; irreducibility forces
a hypothetical rank-one correspondence into one coordinate binary plane,
where the residual Frobenius slice has rank two and cannot be pure.

Hence `r_ij=2`.

### The kernel line

The multiplication kernel is a projective line in `P(U_i tensor U_j)`.
By
[`P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md`](../rank-two-pair-kernel-geometry/P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md),
its intersection with the Segre quadric has only two possible schemes:

- two points: a secant kernel;
- one doubled point: a tangent kernel.

There is no third pencil type.

### Tangent kernels

The tangent theorem normalizes the pair to

```text
U_i=U_j=span(X_0,w),       w in span(X_1,X_2,X_3),  (2)
```

with `w` supported on at least two coordinates.  The opposite-plane purity
classification in
[`P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md`](../tangent-rank-two-pair-purity/P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md)
has two cases.

- If `w` has full three-coordinate support, the nondegenerate ternary polar
  graph is precisely component fourteen, certified in
  [`P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md`](../full-support-tangent-pair/P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md).
- If `w` has two-coordinate support, the polar form has a radical.  Every
  survivor is either embedded `P_3` or a radical flag.  The explicit
  Pluecker degeneration in
  [`P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md`](../../../boundaries/pair-geometry/support-two-tangent-flag/P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md)
  places every radical flag in the original lower-pair sixfold.

This exhausts tangent kernels.

### Secant kernels

If both zero products have genuine two-coordinate support, their support
pairs are distinct.

- Disjoint `2+2` supports give the complementary-Witt flag classification
  and component fifteen in
  [`P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md`](../disjoint-secant-lower-pair/P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md).
- Supports meeting in one coordinate give the common-radical two-star
  classification in
  [`P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md`](../overlapping-secant-lower-pair/P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md).
  An explicit common smooth point identifies that chart with the original
  lower-pair sixfold.

If a secant point has support one, exact rank two forces its support to be
disjoint from the other binary zero product.  The valuative arc in
[`P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md`](../../../boundaries/pair-geometry/support-one-secant/P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md)
splits the singleton into a disjoint binary block.  Every punctured point is
in component fifteen, and leading Pluecker coordinates recover the target.
Thus the support-one case also belongs to the component-fifteen closure.

This exhausts secant kernels and proves the forward containment.

## Why several rank-two edges cannot add a component

The proof starts with an arbitrary pair satisfying `r_ij<=2` and classifies
the **entire four-plane tuple**, including both opposite planes.  It never
assumes the other five pair ranks are generic.  Therefore a tuple with two
or more rank-two pairs is already in the four-closure union after choosing
just one of them.

Each condition `r_ij<=2` is determinantal and hence closed.  Each of the four
listed component families has a fixed rank-two pair on a dense set, so its
closure stays in the corresponding determinantal locus.  Taking the finite
union over mode and source symmetries proves the reverse containment.

Simultaneous rank-two compatibility can refine the **intersection poset** of
the four closures, but it cannot produce another irreducible component of
the lower-pair locus.

## Proof dependencies and replay

The corollary introduces no search or elimination.  Its proof is the
disjoint union of the exact cases above.  The complete symbolic replay is:

```text
uv run --with sympy python claims/p4/classifications/pair-geometry/rank-one-pair-obstruction/verify_p4_rank_one_pair_obstruction.py
python claims/p4/classifications/pair-geometry/rank-one-pair-obstruction/audit_p4_rank_one_pair_obstruction.py

uv run --with sympy python claims/p4/classifications/pair-geometry/rank-two-pair-kernel-geometry/verify_p4_rank_two_pair_kernel_geometry.py

uv run --with sympy python claims/p4/classifications/pair-geometry/tangent-rank-two-pair-purity/verify_p4_tangent_rank_two_pair_purity_classification.py
python claims/p4/classifications/pair-geometry/tangent-rank-two-pair-purity/audit_p4_tangent_rank_two_pair_purity_classification.py

uv run --with sympy python claims/p4/classifications/pair-geometry/full-support-tangent-pair/verify_p4_full_support_tangent_pair_component.py
python claims/p4/classifications/pair-geometry/full-support-tangent-pair/audit_p4_full_support_tangent_pair_component.py

uv run --with sympy python claims/p4/boundaries/pair-geometry/support-two-tangent-flag/verify_p4_support_two_tangent_flag_boundary_inclusion.py
python claims/p4/boundaries/pair-geometry/support-two-tangent-flag/audit_p4_support_two_tangent_flag_boundary_inclusion.py

uv run --with sympy python claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/verify_p4_disjoint_secant_lower_pair_component.py
python claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/audit_p4_disjoint_secant_lower_pair_component.py

uv run --with sympy python claims/p4/classifications/pair-geometry/overlapping-secant-lower-pair/verify_p4_overlapping_secant_lower_pair_classification.py
python claims/p4/classifications/pair-geometry/overlapping-secant-lower-pair/audit_p4_overlapping_secant_lower_pair_classification.py

uv run --with sympy python claims/p4/boundaries/pair-geometry/support-one-secant/verify_p4_support_one_secant_boundary_inclusion.py
python claims/p4/boundaries/pair-geometry/support-one-secant/audit_p4_support_one_secant_boundary_inclusion.py
```

The primary programs use symbolic polynomial identities and exact rational
linear algebra.  The audits use separate subset-DP permanent, dual-number,
or Laurent-series implementations.  None performs a graph search or a
parameter census.
