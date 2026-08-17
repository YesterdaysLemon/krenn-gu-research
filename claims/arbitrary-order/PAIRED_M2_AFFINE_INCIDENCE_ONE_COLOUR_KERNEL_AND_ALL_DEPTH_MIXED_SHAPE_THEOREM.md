# Paired M2 affine incidence, one-colour kernels, and all-depth mixed-shape closure

## Status

**Exact characteristic-zero paired-response boundary and bounded mixed-shape
theorem.**  Fix one physical `q=2`, `h=0` residual channel `K` on one finite
port union.  The full residual-present `Z` tower fixes the affine direct-pair
fibre

```text
B_0+L,                 L=ker(mu_K:A_2->A_4),              (1)
```

by `GLD12`.  Any fixed legally attached package of residual-absent pair rows
`M_2(B)=B` cuts (1) by an exact affine incidence/injectivity/kernel
trichotomy.  If `d=dim L`, exactly `d` scalar linear `M_2` rows are always
sufficient to identify the kernel component, and fewer than `d` cannot be
uniformly injective.

After pair diagonality, every mixed residual-absent coefficient at every
depth vanishes exactly when the differently coloured active edge families
are pairwise cross-intersecting.  This is already decided by the two-colour
four-port rows.  On six ternary ports, the complete coordinatewise purity
certificate has `90` off-diagonal pair rows and `270` two-colour four-port
rows; each row is individually necessary.

For a residual channel supported in one pure coefficient colour, the entire
ternary kernel in (1) has an exact support decomposition.  The physical
complete-bipartite `K_(3,3)` control has full tensor kernel dimension `16`,
mixed projection rank `12`, and pure residual dimension `4`.  Twelve mixed
and four pure `M_2` coordinates give an explicit unimodular reconstruction.
The four-dimensional common-one-colour subfamily has every mixed `M` and `Z`
coefficient zero at every depth.

All `M` rows in these conclusions are assumed legally attached on the same
graph, `Q`, and normalization.  The theorem does not manufacture attachment,
promote different direct arrays to one graph, prove witness integration, or
imply a permanent restriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The upstream full-`Z` fibre is
[`GLD12`](TWO_VERTEX_COVER_ALL_DEPTH_H_ZERO_RESPONSE_FIBRE_THEOREM.md).

## 1. Paired M2 affine incidence

Work over a characteristic-zero field `K`.  Let `W` be a finite port set and
let `A(W)` be the labelled square-free tensor algebra.  Fix

```text
Q_K in A(W)_2,
mu_K:A(W)_2 -> A(W)_4,       mu_K(T)=T Q_K,
L=ker mu_K.                                               (2)
```

Let `P:A(W)_2->K^r` be a fixed linear package of scalar coefficient rows of
the residual-absent pair layer `M_2(B)=B`.  It may depend on the fixed
channel `K` and the named port union, but it is chosen before the target
values are inspected and is fixed across the fibre.

### Theorem 1 (affine paired-row trichotomy)

Fix one full-`Z` fibre `B_0+L` and a prescribed attached value `tau in K^r`.
Then

```text
{B in B_0+L:P(B)=tau}                                    (3)
```

is:

1. empty exactly when `tau-P(B_0) notin im(P|_L)`;
2. otherwise an affine space

   ```text
   B_0+T_0+ker(P|_L),                                    (4)
   ```

   where `T_0 in L` is any lift of `tau-P(B_0)`;
3. a single point exactly when `P|_L` is injective.

Thus the paired ambiguity is exactly `L intersect ker P`.

### Proof

Write `B=B_0+T` with `T in L`.  Equation `P(B)=tau` is the linear equation

```text
P|_L(T)=tau-P(B_0).                                      (5)
```

The standard image/fibre trichotomy for (5) is precisely (3)--(4). `square`

### Corollary 1.1 (optimal scalar M2 row count)

Put `d=dim L`.  The restrictions of all scalar pair-coordinate functionals
span `L^*`, so some `d` of them form a basis.  Their common kernel on `L` is
zero.  Conversely any package of fewer than `d` scalar linear rows has rank
less than `d` on `L` and cannot be injective.  Hence exactly `d` fixed scalar
linear `M_2` rows are always sufficient and are uniformly optimal in this
class.

Let `D subset A(W)_2` be the pair-diagonal subspace and put

```text
d_0=dim(L intersect D).                                  (6)
```

The mixed-coordinate projection has rank `d-d_0` on `L`.  Therefore
`d-d_0` mixed coordinate rows can reduce the ambiguity exactly to
`L intersect D`, and `d_0` further pure coordinate rows can eliminate that
residue.  This count concerns scalar linear `M_2` rows, not nonlinear higher
response equations.

## 2. All-depth mixed-shape closure for M

Assume the pair layer is diagonal:

```text
B=sum_(e in binom(W,2)) sum_(c=0)^2
    b_e^c e_(u,c)^* tensor e_(v,c)^*,       e={u,v}.       (7)
```

For each colour put

```text
E_c={e:b_e^c!=0}.                                        (8)
```

### Theorem 2 (M2/M4 criterion for all-depth purity)

The complete residual-absent tower `M=exp(B)` has no mixed coefficient at
any depth if and only if

```text
every e in E_c meets every f in E_d,       c!=d.          (9)
```

Equivalently, the active edge families of distinct colours are pairwise
cross-intersecting.  If (9) fails for disjoint `e in E_c`, `f in E_d`, then
the single four-port coefficient on `e union f` with colour `c` on `e` and
colour `d` on `f` is

```text
b_e^c b_f^d!=0.                                         (10)
```

Thus one coefficient-pure `M_4` row detects every failure.

### Proof

For disjoint `e,f` and `c!=d`, the named `2+2`-colour coefficient of
`B^2/2` receives the two ordered products `B_eB_f` and `B_fB_e`; the factor
`1/2` leaves exactly (10).  The other two perfect matchings of the four
vertices would use an off-diagonal pair coefficient and vanish.  Therefore
vanishing of every mixed `M_4` row is exactly (9).

Conversely, a mixed monomial in any matching term of `exp(B)` contains two
disjoint matching edges of different colours.  This contradicts (9), so no
mixed coefficient occurs at any depth. `square`

### Corollary 2.1 (radical support locus and exact six-port certificate)

The complete mixed-`M` target locus inside the diagonal pair space is the
square-free monomial variety

```text
I_M=<b_e^c b_f^d:e intersect f=empty, c!=d>.             (11)
```

The ideal is radical.  Every pairwise cross-intersecting coloured
edge-support family indexes a contained coordinate subspace, and the
irreducible coordinate-subspace components are indexed exactly by the
inclusion-maximal such families.

On six ternary ports, pair diagonality requires the `15*6=90` ordered
off-diagonal `M_2` coefficient rows.  There are

```text
15 four-sets * 3 complementary pairings
  * 6 ordered distinct-colour choices =270               (12)
```

two-colour `M_4` rows.  These `360` rows are an exhaustive coordinatewise
all-depth purity certificate; once pair diagonality is known, only the `270`
four-port rows remain.  Every row is individually necessary: retaining only
its corresponding one off-diagonal pair coefficient, or its two disjoint
pure pair coefficients, makes that row the unique mixed response coefficient.

Condition (9) permits several active colours.  For example
`E_0={12,13}` and `E_1={14,15}` are cross-intersecting, and the three edges
`12,13,14` may carry three different colours while `B^2=0`.  Mere colour
activity is therefore not a substitute for disjoint complementary-edge
activity.

## 3. One-pure-colour tensor kernels

Suppose `K` is supported in the pure colour zero.  Thus

```text
Q_K=sum_(e in E(G)) k_e x_e^(0,0),       k_e!=0,          (13)
```

for one weighted support graph `G` on `W`.  Let `A_j(X)` denote the scalar
square-free degree-`j` space on a vertex set `X`.

For a direct pair coefficient, let `N` be the subset of its two endpoints
whose coefficient colour is nonzero.  Multiplication by (13) preserves `N`
and its colour labels, so distinct blocks cannot cancel.

### Theorem 3 (exhaustive one-colour kernel decomposition)

The full ternary kernel of `mu_K` is the direct sum of the following blocks.

1. For `N=empty`,

   ```text
   ker(A_2(W) --*Q_G--> A_4(W)).                         (14)
   ```

2. For `N={p}` and either nonzero colour `c=1,2`,

   ```text
   e_(p,c)^* tensor
   ker(A_1(W-{p}) --*Q_(G-p)--> A_3(W-{p})).             (15)
   ```

3. For `N={p,q}` and colours `c,d in {1,2}`, the coordinate line on
   `e_(p,c)^* tensor e_(q,d)^*` occurs exactly when `{p,q}` is a
   two-vertex cover of `E(G)`.

### Proof

The block split follows from preservation of `N` and its labels.  In the
empty block, (14) is the scalar definition.  In a singleton block, every
channel edge incident to `p` overlaps the direct edge and vanishes, leaving
exactly multiplication by `Q_(G-p)` on the other endpoint; this is (15).
For two nonzero-colour endpoints, the direct coefficient is one coordinate.
Its product with `Q_K` is zero exactly when there is no disjoint nonzero
channel edge, which is precisely the two-vertex-cover condition. `square`

Put

```text
s(G)=dim ker(A_2(W) --*Q_G--> A_4(W)),
h_p=dim ker(A_1(W-{p}) --*Q_(G-p)--> A_3(W-{p}),
c_2(G)=number of two-vertex covers of E(G).               (16)
```

The direct sum gives

```text
dim L=s(G)+2 sum_p h_p+4c_2(G),
dim(L intersect D)=s(G)+2c_2(G),
rank(mixed projection on L)=2 sum_p h_p+2c_2(G).         (17)
```

## 4. Complete-bipartite K_(3,3) sharpness

Take six ports split as `A={1,2,3}`, `C={4,5,6}` and the physical channel

```text
Q_K=(x_1+x_2+x_3)(x_4+x_5+x_6)                          (18)
```

in pure colour zero.  This is the complete-bipartite channel, not the
two-disjoint-clique `3+3` shore word of `GLD6`.

### Corollary 3.1 (exact tensor rank and optimal coordinates)

For (18),

```text
s(G)=4,       h_p=1 for all six p,       c_2(G)=0,
dim L=16,     dim(L intersect D)=4.                       (19)
```

Hence the full `1215 x 135` tensor Wick map has rank `119`.  The four pure
kernel directions are

```text
x_1x_3-x_1x_2,       x_2x_3-x_1x_2,
x_4x_6-x_4x_5,       x_5x_6-x_4x_5.                     (20)
```

For every port `p` and colour `c=1,2`, one additional mixed kernel line is
the difference of the two edges from `p` to its same-shore mates, with colour
`c` at `p` and colour zero at the mate.  These twelve lines and (20) form a
basis.  Choosing the positive coordinate from each displayed difference
gives a `16 x 16` restriction matrix with determinant one.  Thus twelve mixed
and four pure `M_2` rows explicitly and optimally identify the full tensor
kernel.

For the scalar block, multiplication by the left shore sum on
`A_2(A)->A_3(A)` has rank one and kernel two, and the right shore is the same.
The cross-shore block is a tensor product of two injective
`A_1(3)->A_2(3)` maps.  This proves `s(G)=4`.  Removing any port leaves a
`K_(2,3)` channel; (15) has its one-dimensional same-shore difference kernel,
so every `h_p=1`.  No two vertices cover all nine cross edges, proving
`c_2(G)=0` and (19).

The pure four-dimensional family `B=tT`, with `T` in the span (20), satisfies

```text
Z_(tT)=Q_K at every residual-present depth,
M_(tT)=exp(tT) changes but has only pure colour-zero words. (21)
```

Thus every mixed coefficient of both towers vanishes throughout this family.
Mixed target shape cannot remove the pure residual; fixed pure target values
or legally attached pure `M_2` rows are load-bearing.

## 5. Frontier and UNKNOWN remainder

```text
fixed attached M2 rows cut a full-Z fibre affinely:       PROVED;
d scalar linear M2 rows are sufficient and optimal:      PROVED;
M2 diagonality + M4 mixed zeros imply all-depth M purity: PROVED;
six-port coordinate purity certificate has 360 rows:     PROVED;
one-pure-colour tensor kernel decomposition:              PROVED;
complete-bipartite K_(3,3) tensor kernel 16/12/4 split:   PROVED;
legal same-Q attachment of the selected M rows:           UNKNOWN;
these response fibres meet the full witness locus:        UNKNOWN;
coefficient-pure target attachment beyond assumed rows:  UNKNOWN;
weighted permanent implication:                          UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The breadth is one named finite port union, with the explicit sharp control
on all fifteen `K_4` subwindows of one six-set.  The depth is the complete
residual-present `Z` tower, the residual-absent pair/four layers, and, through
Theorem 2, every deeper residual-absent mixed layer.  The reconstructed data
are the direct pair tensor once enough fixed legally attached `M_2` rows are
given.  The ambiguity object is `L intersect ker P`, refined under target
shape by the radical ideal (11).  There is no transition gauge.  The target
implication is an exact paired-response incidence or one displayed mixed
`M_4` coefficient.  The permanent implication is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_paired_m2_affine_incidence_one_colour_kernel_and_all_depth_mixed_shape.py
python -I claims/arbitrary-order/audit_paired_m2_affine_incidence_one_colour_kernel_and_all_depth_mixed_shape.py
```

The primary verifier constructs the exact `1215 x 135` ternary
complete-bipartite map, checks rank `119`, the `16`-vector kernel basis, mixed
rank `12`, pure residual `4`, and the unimodular coordinate restriction.  It
also replays the affine trichotomy and the `360`-row mixed-shape ledger.  The
independent no-import audit uses separate sparse rational elimination,
support-block decomposition, and direct square-free products.  These bounded
programs audit the finite controls; the affine, cross-intersection, and block
decomposition proofs are load-bearing.
