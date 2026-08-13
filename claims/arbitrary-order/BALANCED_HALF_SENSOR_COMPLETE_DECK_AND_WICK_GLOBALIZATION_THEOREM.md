# Balanced half-sensor complete deck and Wick globalization theorem

## Status

This is an exact arbitrary-order characteristic-zero reduction.  Splitting
the `n=2m` vertices into two equal halves produces one legal companion sensor
whose columns are indexed by the **complete even principal hafnian deck** of
one half.  A nonempty graph-side open has full column rank at every order.
On that open a diagonal target has at most one rational deck lift, and the
lift comes from one physical block graph exactly when it extends globally,
has empty coefficient one, and satisfies the square-free Wick completion
equations.

Consequently every hypothetical ternary Krenn--Gu witness obeys the exact
dichotomy

```text
some balanced partition is generically full-sensor
  -> one unique rational complete deck must pass the global Wick gate;

every balanced partition is identically rank-deficient
  -> the witness lies in a proper closed algebraic boundary.       (1)
```

This removes the deletion-depth, coordinate-monomial, and `q>=4` *labeling*
gaps on the first branch.  It does not prove that its unique lift fails Wick
completion, exclude the closed rank-drop branch, construct a counterexample,
or resolve the global conjecture.  Global Krenn--Gu remains **UNRESOLVED**.
Restriction to any three colours makes this ternary reduction relevant to
every original `d>=3` witness, but does not strengthen the conclusion.

## 1. The balanced matching partition

Work over a characteristic-zero field `K`.  Let the vertex set be

```text
V = R disjoint-union N,        |R|=|N|=m,             (2)
```

and let `L_v` be the local vector space at vertex `v`.  A physical edge block
is a bilinear form

```text
W_uv in L_u^* tensor L_v^*.                           (3)
```

Fix vectors `z_u in L_u` for `u in N`, while leaving the `R` slots open.  For
`i in R` and `u in N`, put

```text
h_iu(z_u) = W_iu(-,z_u) in L_i^*.                    (4)
```

For `D subset N` with `|D| congruent m (mod 2)`, define the root companion
tensor `G_D(z_D)` as follows.  Choose a subset `U subset R` of size `|D|`, a
bijection `phi:U -> D`, and a perfect matching `P` of `R-U`; multiply the
root--nonroot covectors `h_(i,phi(i))` for `i in U` by the root--root edge
covectors for `P`, and sum over all three choices.  Thus

```text
G_D(z_D)
 = sum_(U subset R, |U|=|D|)
   sum_(bijections phi:U->D)
   sum_(P perfect matching of R-U)
     product_(i in U) h_(i,phi(i))(z_phi(i))
     product_({i,j} in P) W_ij.                       (5)
```

Every product in (5) is understood as a tensor in
`tensor_(i in R) L_i^*`.  For every even `I subset N`, define the scalar
principal deck member

```text
C_I(z_I)
 = haf( (W_uv(z_u,z_v))_(u,v in I) ),
C_empty = 1.                                         (6)
```

### Theorem 1 (balanced complete-deck identity)

For every block graph and every balanced partition (2),

```text
T_W(-_R,z_N)
 = sum_(I subset N, |I| even)
     G_(N-I)(z_(N-I)) C_I(z_I).                       (7)
```

There are exactly `2^(m-1)` summands, and their coefficients are every even
principal hafnian of the *same* nonroot graph, including `C_empty=1`, all
pair blocks, and every higher even deletion depth.

### Proof

Restrict a perfect matching of `V` to the root half `R`.  Let `U` be the
roots matched across the cut and let `D` be their partners in `N`.  The cross
edges give a bijection `U -> D`; the other roots are perfectly matched inside
`R`; and the other nonroots `I=N-D` are perfectly matched inside `N`.
Therefore `|D|=|U|` has the parity of `m`, while `I` is even.  Conversely,
one term in (5), together with one perfect matching of `I`, reconstructs one
and only one perfect matching of `V`.  Products and multiplicities are
preserved.  This bijection proves (7).  Half of all subsets of a nonempty
`m`-set are even, proving the column count.

The identity is pointwise and polynomial.  It uses no genericity, support
assumption, positivity, division, or enumeration.

Its matching partition is compatible with the root-deletion bookkeeping in
[`MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`](MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md),
and the repeated-root-matching coefficient in the chart below is the same
double-factorial mechanism used in
[`LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md`](LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md).
Those earlier results do not assert the balanced complete-deck sensor; (7) is
proved directly here.

## 2. Full rank occurs at every order

Identify `R={R_1,...,R_m}` and `N={N_1,...,N_m}`.  Assume
`dim L_(R_i)>=2`.  Fix one point `z_N` with every `z_(N_i)` nonzero.  Choose
linearly independent covectors

```text
a_i,b_i in L_(R_i)^*.                                (8)
```

The following evaluated shore is physical.  Choose a covector `ell_i` on
`L_(N_i)` with `ell_i(z_(N_i))=1`, and set

```text
W_(R_i,N_j) = 0                         for i!=j,
W_(R_i,N_i) = a_i tensor ell_i,
W_(R_i,R_j) = b_i tensor b_j            for i<j.      (9)
```

The blocks internal to `N` do not affect the sensor.

### Theorem 2 (explicit full-rank chart)

On (9), for every parity-legal `D`,

```text
G_D
 = (|N-D|-1)!!
   tensor_(i:N_i in D)     a_i
   tensor_(i:N_i notin D)  b_i,                       (10)
```

where `(-1)!!=1`.  These `2^(m-1)` tensors are linearly independent.  Hence
the balanced sensor has full column rank `2^(m-1)` for every `m>=1`.

### Proof

The zero off-diagonal cross blocks in (9) force `R_i` to meet `N_i` whenever
`N_i in D`.  Thus `U` is the copy of `D` in `R` and the cross bijection is
unique.  Every perfect matching of the remaining `|N-D|` roots contributes
the same tensor product of their `b_i`; there are `(|N-D|-1)!!` such
matchings.  This proves (10).  Since `a_i,b_i` are independent at every root,
all `2^m` binary tensor words in them are independent.  The parity-selected
half is therefore independent as well.  Characteristic zero keeps every
double factorial nonzero.

Full rank is the nonvanishing of some maximal minor.  The construction shows
that such a minor is not the zero polynomial in the shore blocks and `z_N`.
It follows that a nonempty Zariski-open set of shores has a generically
full-rank balanced sensor.

### A target-disjoint full sensor

Now take ternary local spaces and `m>=3`.  Choose `a_i,b_i` to be distinct
coordinate covectors.  On the first three roots use the unordered pairs

```text
{e_0^*,e_1^*},   {e_1^*,e_2^*},   {e_2^*,e_0^*};     (11)
```

on later roots use any distinct coordinate pair.  Every coordinate colour
is absent at one of the first three roots.  The coordinate words in (10)
therefore contain none of

```text
e_0^* tensor m,  e_1^* tensor m,  e_2^* tensor m.    (12)
```

Because coordinate words form a basis, the sensor image meets the diagonal
target plane spanned by (12) only at zero.  Choose the point used in (9) in
the coordinate torus and choose each `ell_i` with `ell_i(z_(N_i))=1`.  The
sensor is then still the full-rank sensor (10), while the GHZ contraction is
nonzero and cannot lie in its image.  Thus target incidence is a genuine
proper determinantal condition, not an identity of the balanced architecture.

The low-order boundary is explicit.  The full-rank construction works from
`m=1`, but the target plane is the whole root space at `m=1`, so it cannot be
disjoint there.  The cyclic target-disjoint construction above is asserted
only for `m>=3` (no claim is made for `m=2`).  At `m=3` the nonroot deck has
only empty and pair members, so Wick completion has no degree-at-least-four
equation.  At `m=4` the four-point Wick relation is the first nontrivial one,
and the `D=empty` column in (10) has coefficient `3!!=3`.

## 3. The proper closed all-balanced boundary

For a fixed balanced partition, form every maximal minor of the polynomial
sensor matrix `Gamma_R(z_N)` whose columns are (5).  The sensor is
identically rank-deficient in `z_N` exactly when every coefficient of every
maximal minor is zero.  These are polynomial equations in the physical shore
blocks.  There are finitely many balanced partitions, so

```text
B_all
 = intersection_(balanced R|N)
     {every maximal minor of Gamma_R(z_N) is identically zero}     (13)
```

is closed in the ambient block-graph parameter space.  The chart (9) avoids
at least one factor of this intersection, so `B_all` is proper there.  It is
not proved proper after intersecting with the hypothetical-witness/target-
incidence variety.

This proves the exhaustive geometric part of (1): any fixed graph is either
in `B_all`, or some balanced partition has a dense full-sensor open in
`X=product_(u in N) P(L_u)`.  Properness is not permission to discard
`B_all`; a hypothetical witness could lie entirely on it.

The
[`diagonal-complete sharpness theorem`](BALANCED_ALL_RANK_DROP_DIAGONAL_COMPLETE_SHARPNESS_THEOREM.md)
shows that this warning is substantive.  For every `m>=4`, `B_all` contains a
complete graph with invertible edge blocks, local concision, and all three
normalized pure target coefficients.  Its mixed even-colour coefficients are
nonzero, so it is not a witness.  Thus those strong ambient and pure
conditions cannot replace the missing mixed GHZ equations on the rank-drop
branch.

The subsequent
[`common-quadratic orbit theorem`](BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md)
excludes the full vertex-gauge orbit of that diagonal mechanism from the
witness locus by a `6` versus `3` two-flattening rank mismatch.  It does not
show that an arbitrary member of `B_all` has common-quadratic form, so the
nonsynchronized witness intersection remains open.

The further
[`common-quadric mixed-permanent obstruction`](BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md)
uses the all-cross `C_empty=1` sector directly.  On one balanced shore whose
root-root diagonal quadratics share a nondegenerate `Q`, every nonconstant
mixed-word cross permanent must be divisible by `Q`; a column-separable
common-conformal shore is therefore impossible even with arbitrary internal
nonroot blocks.  A nonzero scalar permanent fails a mixed word, while zero
permanent fails the constant-colour pure residue.  The later
[`root-quadric basepoint bridge`](BALANCED_ROOT_QUADRIC_BASEPOINT_PERMANENT_RESTRICTION_AND_GAUGE_SHARPNESS_THEOREM.md)
routes every nonseparable common-`Q` shore to `P_m -> Delta_3`; this excludes
`m=3,4` and leaves `m>=5` open at the permanent restriction frontier.

## 4. Projective complete-deck lift

Continue over `K=C`.  Use the convention that `P(L_u)` parametrizes lines in
`L_u`, so `H^0(P(L_u),O(1))=L_u^*`.  Put

```text
X = product_(u in N) P(L_u),
O(1_I) = tensor_(u in I) pr_u^* O_P(L_u)(1),

E = direct-sum_(I subset N, |I| even) O(1_I),
F = (tensor_(i in R) L_i^*) tensor O(1_N).            (14)
```

In the ternary case,

```text
rank(E)=2^(m-1),             rank(F)=3^m,
dim H^0(X,E)=(4^m+(-2)^m)/2, dim H^0(X,F)=9^m.        (15)
```

In particular, `H^0(X,O(1_I))=tensor_(u in I)L_u^*` records exactly one
multilinear tensor on the present vertex set `I`.

The companion `G_(N-I)` is a section of
`(tensor_R L_i^*) tensor O(1_(N-I))`.  Multiplication therefore defines the
bundle map

```text
Gamma_tilde_W : E -> F.                              (16)
```

The ternary GHZ target contracts on `N` to the global section

```text
J(z_N)
 = sum_(c=0)^2
     (tensor_(i in R) e_(i,c)^*)
     product_(u in N) z_u[c]                         (17)
```

of `F`.

### Theorem 3 (exact lift and Wick gate)

Fix the root--root and root--nonroot shore blocks which define (16).  They
extend to a ternary block graph satisfying the original full tensor equality
`T_W=GHZ` if and only if there is a global section

```text
C=(C_I)_I in H^0(X,E)                                (18)
```

such that

```text
Gamma_tilde_W(C)=J,                                  (19)
C_empty=1,                                           (20)
log(M_C) has only vertex-degree two.                  (21)
```

Choose the coordinate basis `e_(u,c)` at every nonroot.  Here `M_C` is the
following element of the vertex-exclusive square-zero algebra on `N`:

```text
M_C
 = 1 + sum_(nonempty even I subset N)
       sum_(alpha:I->{0,1,2})
         C_I( (e_(u,alpha(u)))_(u in I) )
         product_(u in I) x_(u,alpha(u)).             (22)
```

Thus every coloured monomial has a scalar coefficient, and every odd
coefficient is zero.  Condition (21) means that every logarithmic component
of vertex-degree other than two vanishes.

### Proof

An extending block graph supplies (18) by its complete internal principal
hafnian deck.  The balanced identity (7) gives (19), the empty hafnian gives
(20), and the block-square-zero Wick theorem gives (21).

Conversely, the Wick completion criterion says that (20)--(21) reconstruct
unique internal edge blocks `W_uv`, `u,v in N`, whose complete partial
matching family is exactly `C`.  Adjoin them to the fixed shore.  Equation
(7) turns (19) into equality with the GHZ tensor after arbitrary contraction
of every nonroot slot and with every root slot left open.  Multilinearity then
gives the original full tensor equality.  Thus no local-to-global or
same-graph step is omitted.

This theorem invokes
[`BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md`](BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md)
only for its proved necessary-and-sufficient logarithmic criterion.  A
finite list of low-order Wick equations is not substituted for (21).

## 5. The unique rational lift on a full sensor

Assume one balanced partition has generic fiber rank `2^(m-1)`.  Over the
function field of `X`, the map (16) is injective.  Hence (19), if consistent,
has at most one rational solution `C`.  Target consistency itself is the
determinantal identity

```text
rank[Gamma_R(z_N) | J(z_N)] = rank Gamma_R(z_N)       (23)
```

on the dense full-rank open.  On each maximal-minor chart, Cramer's rule gives
a local rational solution.  Uniqueness over the function field makes these
local formulas agree on overlaps, so they glue to one rational section of
`E`.

The unique rational solution is a global section of `E` exactly when every
component has nonnegative valuation at every prime divisor in the appropriate
line-bundle trivialization.  Since `X` is smooth and the solution is regular
where the sensor has constant full rank, only divisorial components of the
rank-drop boundary can support a pole; codimension-at-least-two holes do not
obstruct extension of a line-bundle section on this normal variety.

After extension, the remaining tests are the affine normalization (20) and
the full Wick criterion (21).  For `m>=3`, passing all of them constructs an
exact counterexample to the conjecture; for `m=1,2` it constructs only a
low-order equality outside the conjecture's range.  Failing any one is an
exact obstruction on that branch.

The line-bundle condition includes deletion locality and endpoint
multilinearity.  In a product-compatible affine-cone trivialization, in which
`O(1_I)` has no `u`-twist for `u notin I`, suppose

```text
C_I = v_I / beta.                                    (24)
```

then every transverse derivative in a vertex `u notin I` must obey the
denominator-cleared stress

```text
beta D_(u,xi) v_I - v_I D_(u,xi) beta = 0.            (25)
```

For a pair `I={p,q}`, physicality of that pair component is equivalently the
existence of one constant bilinear block `W_pq` such that

```text
v_pq = beta (z_p^T W_pq z_q).                         (26)
```

Equations (25)--(26) are cheap necessary globalization tests.  They are not
by themselves a replacement for pole removal and the all-order Wick gate.

The
[`Cramer--Euler pair-pole gate`](BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)
sharpens this boundary exactly.  The complete Wick criterion is equivalent
to one symmetric Euler--hafnian recurrence for each even `Q` with `|Q|>=4`.
After those recurrences hold, every higher component is the hafnian polynomial
in the pair components, so divisorial regularity needs to be checked only on
the `binomial(m,2)` pairs.  The target residuals, empty normalization, pair
poles, and Euler recurrences remain separate gates; none is proved to fail on
every target incidence.

## 6. Exact frontier

The balanced sensor changes the arbitrary-order obligation graph as follows.

```text
matching partition exposes every even deck label:       PROVED;
balanced full-column-rank graph-side open at every m:    PROVED;
one target-disjoint full sensor exists:                   PROVED for m>=3;
all-balanced identically-rank-drop locus:                PROPER CLOSED;
same-graph projective lift plus Wick criterion:           NECESSARY AND SUFFICIENT;
unique rational lift on a generic full sensor:            PROVED;
normalization/pair-pole/Euler failure for every incidence: UNKNOWN;
all-balanced rank-drop witness exclusion:                 UNKNOWN;
exact counterexample passing the gate:                    NOT FOUND;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

In particular, a successful pointwise `P_7` incidence computation is not a
counterexample: its reconstructed coefficients must be restrictions of the
one global section (18) and pass (20)--(21).  Conversely, the theorem does
not infer failure merely because a local chart, finite field, bounded order,
or generic ambient sensor fails.

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_balanced_half_sensor_complete_deck_and_wick_globalization.py
python claims/arbitrary-order/audit_balanced_half_sensor_complete_deck_and_wick_globalization.py
```

The primary check compares the matching partition with direct exact hafnian
evaluation on fixed small integer instances, checks the parity count and the
explicit full-rank words through `m=7`, and checks the target-disjoint chart.
The independent no-import audit uses a separately written matching recursion
and different fixed weights.  These bounded calculations test the displayed
identities and conventions; the arbitrary-order matching bijection and Wick
criterion above are the proof.
