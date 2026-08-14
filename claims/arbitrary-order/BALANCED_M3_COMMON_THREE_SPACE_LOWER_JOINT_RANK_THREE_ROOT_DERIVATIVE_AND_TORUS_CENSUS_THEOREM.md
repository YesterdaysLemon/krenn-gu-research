# Balanced `m=3` common-three-space lower-joint-rank three-root derivative and torus census

## Status

**Exact characteristic-zero derivative, incidence, and root-torus
localization for every joint-rank-three or joint-rank-four point with all
three root--root blocks nonzero in the normalized, target-consistent physical
`m=3` common-three-space full-sensor stratum.**  Let `U` be the total
singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=r in {3,4}.   (1)
```

Then the shared derivative has rank `9`, `8`, or `7`, with exact kernel
dimensions zero, one, or two.  Rank four cannot have derivative rank nine.
The rank-eight kernel has one two-supported shared-factor syzygy and one
residual block outside the corresponding Segre tangent plane.  Root-torus
blocking forces an explicit coordinate/monomial atlas on that normal form.
The rank-seven kernel is Hilbert--Burch; its `(2,2,2)` projection profile is
impossible at **every** joint rank, and its other three profiles obey the
rank-independent coordinate-boundary atlas first derived in S2AG.

This is a complete lower-rank three-root derivative census and a strict
localization, not an exclusion of all its cells.  Exact algebraic derivative
fixtures realize ranks nine, eight, and seven while blocking the derivative
root torus; they are not claimed to satisfy the physical empty target,
full-sensor, or graph equations.  Lower-rank three-root target coupling,
other S2T components and S2Q pole strata, higher orders, the all-rank-drop
branch, a witness, and a counterexample remain open.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. Shared derivative and preimage incidence

Let the three root spaces be `A_1,A_2,A_3`, each three-dimensional, and
write the nonzero root blocks as

```text
B_23 in A_2 tensor A_3,
B_13 in A_1 tensor A_3,
B_12 in A_1 tensor A_2.                              (2)
```

Their shared derivative is

```text
D(a,b,c)
 =a tensor B_23+B_13 tensor b+B_12 tensor c,
D:A_1 direct-sum A_2 direct-sum A_3
  ->A_1 tensor A_2 tensor A_3.                       (3)
```

The physical singleton formula gives

```text
D(K)=U.                                              (4)
```

Put

```text
N=ker D,                     E=D^(-1)(U).            (5)
```

Rank--nullity on `D|K` and then on `D:E->U` gives

```text
dim(K intersect N)=r-3,
dim E=dim N+3.                                       (6)
```

These two identities will fix every possible lower-rank incidence once the
derivative kernel is classified.

## 2. The zero/one/two-syzygy trichotomy

### Lemma 1 (complete three-block derivative kernel census)

If all three blocks in (2) are nonzero, then exactly one of the following
holds.

1. **Injective chart:**

   ```text
   N=0,                           rank D=9.           (7)
   ```

2. **Shared-factor chart:** after permuting roots and rescaling,

   ```text
   B_23=y tensor w,
   B_13=-x tensor w,
   B_12=C,                                             (8)

   N=span((x,y,0)),                 rank D=8,          (9)

   C notin A_1 tensor y+x tensor A_2.                (10)
   ```

3. **Hilbert--Burch chart:** there are vectors

   ```text
   x,b in A_1,       y,c in A_2,       z,w in A_3    (11)
   ```

   such that

   ```text
   N=span{(x,y,z),(b,c,w)},                          (12)

   B_23=y tensor w-c tensor z,
   B_13=b tensor z-x tensor w,
   B_12=x tensor c-b tensor y,                       (13)

   rank D=7.                                         (14)
   ```

### Proof

The S2X three-summand syzygy lemma gives `dim N<=2`.

Suppose first `dim N=1`, and let `(x,y,z)` span it.  No syzygy can have only
one nonzero component because all three blocks are nonzero.  If all three
components were nonzero, the exact `2 x 3` minor argument in S2X would
produce the second Hilbert--Burch syzygy, contradicting `dim N=1`.  Thus
exactly two components are nonzero.  After a root permutation, `z=0`.
The pairwise shared-factor intersection lemma gives (8)--(9).

The first two derivative summands have image

```text
S=(A_1 tensor y+x tensor A_2) tensor w,              (15)
dim S=5.                                             (16)
```

The third has image `C tensor A_3`, of dimension three.  A nonzero
intersection between them must have third-root factor `w`, and therefore
exists exactly when `C` belongs to the two-factor tangent plane in (10).
Thus the sum has rank eight exactly under (10); equality in the other
direction creates a second syzygy and belongs to the next chart.

Now suppose `dim N=2`.  Over an infinite field, a two-plane cannot be the
union of its three component-zero lines.  Nor can it be contained in one
component-zero hyperplane, since the kernel of any two nonzero derivative
summands has dimension at most one by the pairwise intersection lemma.
Hence `N` contains a syzygy with all three components nonzero.  The S2X
minor calculation gives (11)--(13), and its two displayed syzygies span all
of `N`.  This proves the trichotomy.  QED.

## 3. Exact lower-rank incidence table

Combining Lemma 1 with (6) gives the complete table

```text
r=3, rank D=9:  dim N=0, dim E=3, K=E;
r=3, rank D=8:  dim N=1, dim E=4,
                 K is a hyperplane in E, K intersect N=0;
r=3, rank D=7:  dim N=2, dim E=5,
                 K has codimension two in E, K intersect N=0;

r=4, rank D=9:  IMPOSSIBLE;
r=4, rank D=8:  dim N=1, dim E=4, K=E, N subset K;
r=4, rank D=7:  dim N=2, dim E=5,
                 K is a hyperplane in E, dim(K intersect N)=1. (17)
```

In particular, lower joint rank does not force the Hilbert--Burch kernel
into `K`: rank four retains one selected syzygy line, while rank three is
transverse to the whole kernel plane.  Rank-five arguments that use
`N subset K` therefore do not silently transfer to (17).

## 4. The complete rank-eight root-torus atlas

For a root covector product `alpha tensor beta tensor gamma`, annihilation
of the whole derivative image in the shared-factor chart (8) is exactly

```text
beta(y) gamma(w)=0,
alpha(x) gamma(w)=0,
C(alpha,beta)=0.                                    (18)
```

Any fully supported solution of (18) would annihilate `U subset image D`,
contradicting S2R.  Thus (18) has no point on the product root torus.

Call a vector **coordinate** when it is proportional to one target basis
vector, and call a two-root tensor **monomial** when it is proportional to
one target coordinate tensor.

### Lemma 2 (rank-eight torus gate)

The shared-factor chart (8)--(10) blocks every fully supported product
annihilator if and only if both conditions below hold:

```text
w is coordinate or C is monomial;                   (19)

x is coordinate or y is coordinate, or
C=lambda e_i tensor e_j
  modulo (A_1 tensor y+x tensor A_2)
for some i,j and lambda!=0.                          (20)
```

In the last alternative of (20), `x,y` are understood to be noncoordinate.
Condition (10) guarantees the displayed quotient class is nonzero.

### Proof

First take `gamma(w)=0`.  A fully supported `gamma` with this property exists
exactly when `w` is noncoordinate.  Independently, the Laurent polynomial
`C(alpha,beta)` has a root on the product torus exactly when it has at least
two coordinate monomials: a nonmonomial Laurent polynomial over an
algebraically closed field has a torus zero, while a monomial is a unit.
This gives (19).

Now take `gamma(w)!=0`.  Equation (18) becomes

```text
alpha in x^perp,        beta in y^perp,
C(alpha,beta)=0.                                    (21)
```

If `x` or `y` is coordinate, its annihilator contains no fully supported
covector, so this branch is empty.  Assume both are noncoordinate.  Put

```text
E_x=P(x^perp),             E_y=P(y^perp).            (22)
```

Each is a projective line whose root-torus part is the complement of finitely
many coordinate-boundary points.  By (10), the restriction `bar C` to
`E_x x E_y` is a nonzero bilinear form.

If `bar C` has matrix rank two, its `(1,1)` zero curve cannot be contained
in the finite union of vertical and horizontal coordinate-boundary lines;
it meets the product torus.  If it has rank one, write `bar C=l tensor m`.
Its zero set avoids the product torus exactly when the unique zero of `l`
and the unique zero of `m` are coordinate-boundary points.  Thus `l` and
`m` are restrictions of coordinate evaluations `alpha_i,beta_j`.  Two
ambient tensors have the same restriction to `x^perp tensor y^perp` exactly
when their difference lies in

```text
A_1 tensor y+x tensor A_2.                           (23)
```

This proves (20), and reversing the argument proves sufficiency.  QED.

Thus the rank-eight cells are no longer arbitrary residual blocks.  Up to
root permutation, they lie on the union

```text
w coordinate and
  (x coordinate or y coordinate or C monomial modulo the tangent plane),

or

C monomial and
  (x coordinate or y coordinate or the same quotient condition). (24)
```

No pointwise target equation beyond S2R is used here.

## 5. The rank-seven Hilbert--Burch atlas is rank-independent

For the kernel in (12), put

```text
P_1=span(x,b),       P_2=span(y,c),       P_3=span(z,w). (25)
```

Every projection dimension is one or two.  For root covectors define

```text
A=(alpha(x),alpha(b)),
B=(beta(y),beta(c)),
C_0=(gamma(z),gamma(w)).                             (26)
```

The three block contractions are, up to signs,

```text
det(B,C_0),             det(A,C_0),             det(A,B). (27)
```

The S2AG beta-zero proof depends only on (25)--(27) and S2R, not on
`N subset K`.  It therefore transfers verbatim to both lower ranks:

1. Profile `(2,2,2)` is impossible.  Surjectivity of all three evaluation
   maps lets one choose a common pair in (26) while avoiding the nine
   coordinate hyperplanes, giving a forbidden fully supported product
   annihilator.
2. Up to root permutation, profile `(1,2,2)` has

   ```text
   N=span{(x,y,z),(0,c,w)},                          (28)
   ```

   and necessarily

   ```text
   x is coordinate, and c or w is coordinate.        (29)
   ```

3. Profile `(1,1,2)` has

   ```text
   N=span{(x,0,z),(0,y,w)},                          (30)
   ```

   and the allowed necessary coordinate pairs are

   ```text
   (x,y),                    (x,w),             (y,z). (31)
   ```

4. Profile `(1,1,1)` is a rank-one triangle, normalized as

   ```text
   N=span{(x,0,z),(0,y,z)},                          (32)
   ```

   and at least two of `x,y,z` are coordinate.       (33)

Conditions (29), (31), and (33) are necessary coordinate-boundary atlases,
not exclusions.  The later rank-five S2AN--S2BL chain uses the stronger
incidence `N subset K`; those exclusions are not imported into (17).

## 6. Exact derivative sharpness fixtures

The three derivative ranks and their torus-blocking conditions are all
algebraically populated.

### Rank nine

Take

```text
B_23=e_0 tensor e_0,
B_13=e_1 tensor e_1,
B_12=e_2 tensor e_2.                                (34)
```

The three derivative summands have disjoint coordinate supports, so `D` is
injective.  Their beta-zero equations are three coordinate monomials and
have no root-torus solution.

### Rank eight

Take

```text
x=y=w=e_0,                 C=e_1 tensor e_1.         (35)
```

Then (8) has kernel `span((e_0,e_0,0))`; `C` is outside the tangent plane
`A_1 tensor e_0+e_0 tensor A_2`, so the derivative has rank eight.  Both
parts of Lemma 2 hold on coordinate alternatives.

### Rank seven

Take the Hilbert--Burch kernel

```text
N=span{(e_0,0,e_2),(0,e_1,e_2)}.                    (36)
```

Formula (13) gives, up to signs,

```text
B_23=e_1 tensor e_2,
B_13=e_0 tensor e_2,
B_12=e_0 tensor e_1.                                (37)
```

The derivative has rank seven and profile `(1,1,1)`; every beta-zero
equation is a coordinate monomial.

These fixtures validate sharpness of the derivative and root-torus census
only.  They do not provide `K`, the physical empty permanent, a full sensor,
regular pair blocks, a graph, or a counterexample.

## 7. Proof-topology consequence

The lower-rank three-root common-three-space frontier is now

```text
joint rank 4:
  derivative rank 9:                                 IMPOSSIBLE;
  derivative rank 8:                                 shared-factor atlas
                                                       (19)--(24), OPEN;
  derivative rank 7:                                 Hilbert--Burch atlas
                                                       (29)/(31)/(33), OPEN;

joint rank 3:
  derivative rank 9:                                 injective, root-torus
                                                       beta-zero set empty, OPEN;
  derivative rank 8:                                 shared-factor atlas
                                                       (19)--(24), OPEN;
  derivative rank 7:                                 Hilbert--Burch atlas
                                                       (29)/(31)/(33), OPEN;

Hilbert--Burch profile (2,2,2), both ranks:           IMPOSSIBLE;
lower-rank transverse two-root graph branch:         EMPTY (S2BN/S2BO/S2BP);
other components / pole strata / higher orders:      OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.        (38)
```

The next exact obligation is to couple the finite cells in (38) to the full
empty-permanent target and the lower-rank incidence table (17).  A valid
successor must preserve the distinction between rank-four selected-kernel
lines, rank-three transverse kernels, and the rank-five containment used by
the old Hilbert--Burch exclusions.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_three_root_derivative_and_torus_census.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_three_root_derivative_and_torus_census.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_three_root_derivative_and_torus_census.py claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_three_root_derivative_and_torus_census.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_three_root_derivative_and_torus_census.py claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_three_root_derivative_and_torus_census.py
```

The primary verifier checks the rank-eight tangent-plane intersection,
zero/one/two-syzygy fixtures, the complete incidence table, representative
torus gates, and all Hilbert--Burch profiles with exact SymPy matrices.  The
independent no-import audit reconstructs the derivative ranks, kernels,
block contractions, torus evaluations, and incidence arithmetic with
standard-library `Fraction` elimination.  The arbitrary-vector kernel,
Laurent-unit, projective-line, and finite-hyperplane arguments are the
written proof above.

## Dependencies

- [`joint-rank-five derivative and torus localization`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [`complete full-joint-cross-rank exclusion`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md)
- [`singleton-span torus-annihilator obstruction`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [`lower-rank transverse q=1 complete pair-pole exclusion`](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_ONE_COMPLETE_PAIR_POLE_EXCLUSION_THEOREM.md)
