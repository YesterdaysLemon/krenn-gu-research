# Full tensor h-zero Z fibres and the two-vertex-cover boundary

## Status

**Exact characteristic-zero tensor-valued all-depth physical-response fibre
theorem.**  In a literal `q=2`, `h=0` response, the complete affine fibre of
the residual-present tensor `Z` tower through a fixed direct array `B` is

```text
B + ker(mu_K:A(W)_2 -> A(W)_4),    mu_K(T)=T Q_K.         (1)
```

Thus, once the full tensor four-port layer has a genuine kernel, no deeper
residual-present `Z` layer removes it.  For a perturbation supported on one
edge `e={u,v}`, membership in this kernel is equivalent to the two endpoints
meeting every nonzero residual-channel block.

Equivalently, if `e={u,v}` is a vertex cover of the block-support graph of
`K`, then

```text
B -> B+t T_uv                                            (1a)
```

leaves the complete residual-present tensor `Z` tower unchanged for every
scalar `t`.  Conversely, if (1a) is invisible for one nonzero `T_uv`, every
whole `K` block on an edge disjoint from `e` is zero.

There are exact seven-port examples with no isolated response port and every
diagonal pair tensor of rank at most one.  Hence neither all-subwindow
residual-present `Z` data nor arbitrarily deep `Z` data universally rescue
the low-rank branch.  The residual-absent tower `M=exp(B)` changes, so these are
not paired `(M,Z)` fibres, same-graph ambiguities, or full Krenn--Gu witnesses;
the full mixed GHZ equations may still exclude them.  No permanent
restriction follows, and the global conjecture remains **UNRESOLVED**.

This theorem sharpens the exceptional response boundary left by
[`GLD6`](SIX_PORT_PHYSICAL_WICK_SELECTOR_TWO_ACTIVE_ALL_SUBWINDOW_AND_DEEPER_RESPONSE_THEOREM.md)
and
[`GLD8`](GLOBAL_SQUARE_FREE_PHYSICAL_WICK_SUPPORT_UNION_CLASSIFICATION_AND_COMMON_ROW_SELECTOR_THEOREM.md).
The block-square-zero response factorization itself is proved in
[`BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM`](BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md)
and
[`RESIDUAL_RELATIVE_RESPONSE_POLYNOMIAL_DUAL_WICK_THEOREM`](RESIDUAL_RELATIVE_RESPONSE_POLYNOMIAL_DUAL_WICK_THEOREM.md);
the new content here is the exact affine-kernel classification, the
single-edge vertex-cover if-and-only-if, and their all-depth `Z`-fibre
boundary.

## 1. Labelled square-free tensor algebra

Let `K` have characteristic zero, let `W` be a fixed finite port universe,
let every `V_i` be finite-dimensional over `K`, and let

```text
A(W)=direct-sum_(S subset W) tensor_(i in S)V_i^*          (2)
```

be the labelled square-free tensor algebra.  Products on disjoint supports
are tensor products, products on overlapping supports are zero, and the
algebra is commutative under the canonical reordering of named factors.
Write

```text
Q_K=sum_(f in binom(W,2)) K_f,
B=sum_(f in binom(W,2)) B_f,                              (3)
```

where `K_f,B_f in tensor_(i in f)V_i^*`.  The complete residual-present
tensor-valued `h=0` `Z` response is

```text
Z_B=exp(B) Q_K.                                           (4)
```

The finite exponential in (4) is the direct matching generating function.

## 2. Exact all-depth classification

### Theorem 1 (complete affine `Z` fibre)

Fix `K`, put

```text
mu_K:A(W)_2 -> A(W)_4,       mu_K(T)=T Q_K,              (5)
```

and let `B,T in A(W)_2`.  Then

```text
Z_(B+T)=Z_B    if and only if    mu_K(T)=0.               (6)
```

Consequently the full residual-present tensor-valued `h=0` `Z` fibre through
`B` is exactly the affine space in (1).

### Proof

Commutativity gives

```text
Z_(B+T)-Z_B=exp(B)(exp(T)-1)Q_K.                         (7)
```

If `T Q_K=0`, then every `T^j Q_K` with `j>=1` vanishes, so (7) is zero.
Conversely, if (7) is zero, multiply by the unit `exp(-B)`.  The degree-four
homogeneous component of `(exp(T)-1)Q_K` is exactly `T Q_K`; every later term
has degree at least six.  Hence `T Q_K=0`. `square`

Equivalently, for any `B,B' in A(W)_2`, equality of their full tensor
degree-four responses, `B Q_K=B' Q_K`, is equivalent to equality of their
complete residual-present `Z` towers.  Restriction of the algebra identity
to every principal port subwindow preserves the equality.  Thus full tensor
`z_4` is information-complete for the entire same-`Q`, `h=0`,
residual-present `Z` tower.  This does not say that a merely diagonal or pure
`z_4` target equals a reference response.

General kernel vectors can cancel the three complementary pairings inside a
four-vertex component; they need not be supported on an edge that covers the
block-support graph.

### Theorem 2 (single-edge two-vertex-cover fibre)

Fix an edge `e={u,v}` and a nonzero tensor

```text
T_e in V_u^* tensor V_v^*.                               (8)
```

The following are equivalent.

1. Every residual-channel edge disjoint from `e` vanishes:

   ```text
   K_f=0 for all f disjoint from e.                       (9)
   ```

2. `Q_K T_e=0` in `A(W)`.
3. For every direct polynomial `B` and every `t in K`,

   ```text
   Z_(B+t T_e)=Z_B.                                      (10)
   ```

4. There exist one `B` and one nonzero `t in K` for which (10) holds.

Condition (9) says exactly that `e` is a two-vertex cover of the
block-support graph `{f:K_f!=0}`.

### Proof

Multiplication by `T_e` kills every block whose edge meets `e`.  Hence

```text
Q_K T_e=sum_(f disjoint from e) K_f tensor T_e.          (11)
```

The summands on the right lie in distinct labelled support components as
`f` varies.  For fixed `f`, the tensor product `K_f tensor T_e` is nonzero
exactly when `K_f` is nonzero because `T_e` is nonzero and the coefficients
form a field.  This proves the equivalence of 1 and 2.

Since `T_e^2=0`,

```text
exp(t T_e)=1+t T_e.                                     (12)
```

Theorem 1 proves that 2 implies 3 and hence 4.  Conversely, suppose 4 holds.
Multiply (10) by the unit `exp(-B)` and use (12).  The result is
`t T_e Q_K=0`; since `t!=0`, condition 2 follows. `square`

The equalities (6) and (10) are identities in the complete square-free
algebra.  They therefore cover every port subwindow and every
residual-present `Z` depth on the named union, not only pair and four-port
layers.  A nonzero `T` does not preserve `M`:

```text
M_(B+T)-M_B=exp(B)(exp(T)-1)!=0,                         (13)
```

because, after multiplication by the unit `exp(-B)`, the degree-two
component is `T`.  The hypothesis `h=0` is essential: an `h exp(B)` term
detects the variation when `h!=0`.

The ordinary scalar square-free polynomial proof is the specialization in
which every displayed tensor is one chosen coefficient word.

## 3. Exact nonisolated low-rank controls

### Corollary 2.1 (complete bipartite control)

Take seven ports with one pure coefficient word.  Put

```text
a_i=1,b_i=0 for i=1,...,5,
a_6=a_7=0,b_6=b_7=1.                                    (14)
```

Then the physical channel `K_ij=a_i b_j+b_i a_j` has support graph
`K_(5,2)`.  It has no isolated vertex, every nonzero diagonal pair tensor has
rank one, and no port coefficient vector is nonisotropic.  The edge
`e={6,7}` is a vertex cover of the block-support graph, so changing the
nonzero coefficient tensor `B_67(0,0)` leaves the full residual-present `Z`
tower unchanged.

### Corollary 2.2 (one-full-port star control)

At one centre `p`, take two coefficient vectors

```text
v_(p,0)=(0,1),       v_(p,1)=(1,0),                     (15)
```

and at each of six leaves retain only `v_(i,0)=(1,0)`.  Every other
coefficient vector is zero.  The diagonal pair-support graph is a nonisolated
star, every pair matrix has rank at most one, and the centre is the unique
rank-two port frame.  For any leaf `i`, the edge `e={p,i}` is a vertex cover;
varying `B_pi(0,0)` is invisible at every residual-present `Z` depth.

Both controls are exact physical `q=2` responses.  Neither is asserted to
satisfy maximum-root incidence, local concision, or the full mixed GHZ
target.

### Corollary 1.1 (genuine multi-edge cancellation)

On six scalar ports split as `{1,2,3} sqcup {4,5,6}`, let `K` be the complete
bipartite physical channel with every cross-shore coefficient one and every
within-shore coefficient zero.  Then

```text
T=x_1x_3-x_1x_2.                                        (16)
```

is a nonzero element of `ker(mu_K)`.  No single support edge of `T` is a
two-vertex cover.  Indeed `Q_K=(x_1+x_2+x_3)(x_4+x_5+x_6)` and
`T(x_1+x_2+x_3)=0`; the two complementary terms cancel in each relevant
four-set.  Theorem 1 therefore makes (16) invisible throughout the complete
residual-present `Z` tower.  This separates the full affine-kernel theorem
from the single-edge support classification.

## 4. Interface with seven-port tensor supply

The
[`five-helper tensor selector`](SEVEN_PORT_FIVE_NONISOTROPIC_HELPER_TENSOR_WICK_SELECTOR_THEOREM.md)
gives a positive seven-port branch when every port supplies a bi-supported
coefficient, or when one diagonal pair has rank two and the pair-support
graph has no isolated port.  Corollaries 2.1 and 2.2 lie in the complementary
observable branch:

```text
every diagonal pair has rank at most one,
the pair-support graph has no isolated port.              (17)
```

They prove that deeper residual-present `Z` response alone cannot universally
eliminate that branch.  The residual-absent `M` rows do distinguish the
graphs.
A witness theorem must use the full mixed target equations, attached paired
`M,Z` data, another legally attached channel, or a structural argument
excluding the two-vertex-cover fibres.

For a scalar physical channel `K_ij=a_i b_j+b_i a_j`, Theorem 1 upgrades the
[`GLD8`](GLOBAL_SQUARE_FREE_PHYSICAL_WICK_SUPPORT_UNION_CLASSIFICATION_AND_COMMON_ROW_SELECTOR_THEOREM.md)
injectivity criterion to an exhaustive all-depth scalar `Z` criterion: the
complete direct scalar pair array is identifiable from the `h=0` `Z` tower
exactly when the GLD8 degree-two-to-four map is injective.  Every GLD8 kernel
vector on a complementary support/discriminant branch remains invisible at
all deeper `Z` layers.  A wordwise scalar kernel need not be a full tensor
kernel after polarization, so no automatic tensor-witness conclusion follows.

## 5. Frontier and UNKNOWN remainder

```text
complete affine Z fibre B+ker(mu_K):                      PROVED;
single-edge fibre iff two-vertex-cover support:           PROVED;
genuine multi-edge cancellation fibre:                   PROVED;
K_(5,2) nonisolated diagonal-rank-one fibre:              PROVED;
one-full-port nonisolated star fibre:                     PROVED;
deeper residual-present Z improves on full tensor z4:     FALSE;
these fibres meet the full hypothetical-witness locus:   UNKNOWN;
closed support description of general tensor ker(mu_K):   UNKNOWN;
legal target attachment outside the response package:    UNKNOWN;
coefficient-pure detector or permanent implication:      UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The breadth is every subwindow of one named port union.  The depth is the
entire residual-present tensor-valued `q=2`, `h=0` `Z` tower.  The direct
array fails to be unique from those rows exactly along the affine kernel in
(1); Theorem 2 classifies its one-edge-supported lines.  The residual-absent
`M` tower changes, so this is neither a paired-response nor a same-graph
ambiguity.  There is no transition gauge.  The target implication is a sharp `Z`-level
nonidentifiability boundary, not a GHZ witness.  The permanent implication is
none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_two_vertex_cover_all_depth_h_zero_response_fibre.py
python -I claims/arbitrary-order/audit_two_vertex_cover_all_depth_h_zero_response_fibre.py
```

The primary verifier constructs exact scalar specializations of the
square-free algebra, replays both directions of the affine-kernel and
single-edge equivalences, and checks the multi-edge cancellation and both
seven-port controls at every finite depth.  The independent
no-import audit uses a separate bit-mask representation and
`fractions.Fraction`.  These scripts audit finite specializations; the
labelled-support and nonzero-tensor-product proof above is load-bearing.
