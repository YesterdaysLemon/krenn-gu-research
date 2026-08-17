# Two-chart target incidence and cloned camouflage atlas boundary

Global status: **UNRESOLVED**

Mathematical status: **PROVED characteristic-zero affine trichotomy,
coefficient-pure detector criterion, and exact physical observed-package
atlas boundary**

This theorem is a breadth refinement of the
[`pair/four-port diagonal-interference theorem`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md)
and uses the response convention of the
[`residual-relative dual-Wick theorem`](RESIDUAL_RELATIVE_RESPONSE_POLYNOMIAL_DUAL_WICK_THEOREM.md).

It proves two complementary statements.

1. Two constant uncontracted chart equations have an exact affine
   supply-or-detect trichotomy.  Nonincidence produces a target-coupled left
   syzygy.  It displays one actual mixed coefficient exactly when its
   aggregate is coefficient-pure modulo already synchronized pure words.
2. Neither a second overlapping four-port window nor arbitrarily many cloned
   windows forces that favourable branch.  There is one characteristic-zero
   physical `q=2` atlas of the observed pair/four response packages, with
   common residual rows, trivial overlap transitions, diagonal pair tensors,
   the same three nonzero pure four-port coefficients on every chart, and zero
   mixed four-port coefficients, while every chart remains two-active and the
   selected package has a second physical realization with the opposite
   corrected channel.

The physical observed-package atlas is **not** a Krenn--Gu witness and is
**not** proved to be the output of constant nuisance-free selectors from one
full GHZ equation.
It is a sharp counterexample to a response-atlas inference, not a graph
counterexample.  Universal target attachment, a weighted permanent
restriction, and the global conjecture remain open.

Throughout, `K` is a characteristic-zero field.  All vector spaces are
finite-dimensional.

## 1. Two constant uncontracted chart equations

Let `F` be a coefficient space, let `P` be a common physical sector, and let
`N_0,N_1` be chart-specific nuisance spaces.  Fix constant linear maps

```text
A_c : P -> F,       B_c : N_c -> F,       c=0,1,              (1)
```

and fixed base tensors `g_0,g_1 in F`.  A common physical tensor `T in F`
has two chart presentations when

```text
T = g_c + A_c p + B_c n_c,       c=0,1,                       (2)
```

for one common `p in P` and chart nuisances `n_c in N_c`.

For a proposed target `J in F`, put

```text
tau = (J-g_0, J-g_1) in F direct_sum F                       (3)
```

and define

```text
M : P direct_sum N_0 direct_sum N_1 -> F direct_sum F,
M(p,n_0,n_1) = (A_0 p+B_0 n_0, A_1 p+B_1 n_1).               (4)
```

Equivalently, quotient the nuisance spaces first:

```text
bar A : P -> coker(B_0) direct_sum coker(B_1),
bar A(p) = ([A_0p],[A_1p]),                                  (5)

j_J = ([J-g_0],[J-g_1]).                                     (6)
```

These are uncontracted constant maps.  A pointwise contracted matrix, a
function-field inverse, or a Cramer ratio is not an instance of (1) unless a
separate theorem proves that it descends to the required constant coefficient
map.

### Theorem 1 (exact affine supply-or-detect trichotomy)

Exactly one of the following branches holds.

1. **Target nonincidence:** `j_J` is not in `im(bar A)`.  Equivalently,
   `tau` is not in `im(M)`.  There is no common completion of the two chart
   target equations.
2. **Unique common supply:** `j_J` lies in `im(bar A)` and
   `ker(bar A)=0`.  The common sector `p` is uniquely determined, although
   the individual nuisances need not be.
3. **Affine ambiguity:** `j_J` lies in `im(bar A)` and
   `ker(bar A)` is nonzero.  The possible common sectors form an affine
   translate `p_0+ker(bar A)`.

Equivalently, target incidence is

```text
rank [ M | tau ] = rank M,                                    (7)
```

and, **together with (7)**, unique common supply is

```text
rank M - rank diag(B_0,B_1) = dim P.                          (8)
```

#### Proof

The target equations are exactly `M(p,n_0,n_1)=tau`.  They are solvable iff
`tau in im M`, which after quotienting the two nuisance images is equivalent
to `j_J in im(bar A)`.  If they are solvable, the difference of any two
solutions has common-sector component in `ker(bar A)`.  Conversely every
element of `ker(bar A)` lifts by definition to nuisance corrections in the
two charts.  This gives the affine fibre and proves all three branches.
Equation (7) is the incidence test; the conjunction of (7) and (8) is the
unique-supply test.  Equation (8) alone says only that `bar A` is injective.
`square`

The theorem is linear in the larger arbitrary-deck space.  Therefore
nonincidence and unique supply do not require a matching-secant theorem.
The ambiguous branch is different: a nonzero vector in `ker(bar A)` need not
integrate to a second physical graph deck.

## 2. Exact target coupling and coefficient-pure detection

Let

```text
L = ker(M^*) subset F^* direct_sum F^*.                       (9)
```

Thus `ell=(ell_0,ell_1) in L` exactly when

```text
ell_0 A_0 + ell_1 A_1 = 0,
ell_0 B_0 = 0,
ell_1 B_1 = 0.                                                (10)
```

Write

```text
Sigma(ell) = ell_0+ell_1 in F^*.                              (11)
```

### Theorem 2 (left-syzygy target identity)

For every common physical presentation (2) and every `ell in L`,

```text
delta_ell
 := ell_0(J-g_0)+ell_1(J-g_1)
  = Sigma(ell)(J-T).                                          (12)
```

In particular, target nonincidence is witnessed by some `ell in L` with
`delta_ell!=0`.

#### Proof

Apply `ell_0,ell_1` to (2) and add.  All common-sector and nuisance terms
vanish by (10), so

```text
ell_0(T-g_0)+ell_1(T-g_1)=0.
```

Subtracting this equality from the definition of `delta_ell` gives (12).
The final assertion is finite-dimensional separation of `tau` from `im M`.
`square`

Now fix a word basis of `F`.  Let `W_pure` be the **complete set of pure basis
words**, and assume that the physical tensor and target have already been
synchronized there:

```text
T_w = J_w       for every w in W_pure.                        (13)
```

Every basis word outside `W_pure` is mixed, hence has `J_w=0`.

### Definition 3 (coefficient-pure separator)

For a mixed word `chi`, an element `ell in L` is a
`(W_pure,chi)`-pure separator if

```text
Sigma(ell) = alpha ev_chi + z,
alpha != 0,
z in span{ev_w : w in W_pure}.                               (14)
```

More generally it is `S`-mixed-sparse modulo `W_pure` if

```text
Sigma(ell) in span{ev_w : w in W_pure union S}.
```

### Corollary 4 (displayed mixed coefficient)

If a pure separator satisfies `delta_ell!=0`, then

```text
T_chi = -delta_ell/alpha != 0.                                (15)
```

For an `S`-mixed-sparse separator, (12) is an explicit linear certificate
supported on at most `|S|` mixed target coefficients.  Existence for a fixed
`S` is exactly the constant linear system below.  The last equation is a
normalization: every separator with nonzero `ell(tau)` can be rescaled to
satisfy it.

```text
M^* ell = 0,
(Sigma ell)_w = 0       for every basis word w notin W_pure union S,
ell(tau) = 1.                                                 (16)
```

#### Proof

Insert (14) into (12).  The pure contribution vanishes by (13), and the mixed
target coefficient `J_chi` is zero.  Hence
`delta_ell=-alpha T_chi`.  The sparse statement and (16) are the same
calculation with more than one mixed coordinate.  `square`

This is the precise conversion from abstract chart disagreement to an actual
mixed GHZ coefficient.  A general nonzero cokernel class supplies only a
linear mixed aggregate.

## 3. Bare nonincidence has no uniform sparse certificate

The coefficient-purity hypothesis is load-bearing even before matching
integrability is imposed.

### Proposition 5 (arbitrarily dense affine target defect)

For every integer `s>=2`, let

```text
F = span{d,x_1,...,x_s},       J=d,       P=K,
phi_0=d^*,                     phi_1=d^*-sum_i x_i^*,          (17)

B_c : ker(phi_c) -> F          be inclusion,
A_0(1)=A_1(1)=d,
g_0=0,                         g_1=d.                          (18)
```

Then:

1. chart zero is individually target-compatible only with `p=1`, while
   chart one is individually target-compatible only with `p=0`; hence the
   two target charts are jointly incompatible;
2. `L` is one-dimensional, generated by `(phi_0,-phi_1)`;
3. its aggregate is

   ```text
   Sigma(phi_0,-phi_1)=sum_i x_i^*,                           (19)
   ```

   so every nonincidence certificate uses all `s` mixed coordinates;
4. for every `t_1,...,t_s` with `sum_i t_i=-1`, the tensor

   ```text
   T=d+sum_i t_i x_i                                           (20)
   ```

   has both common chart presentations with the same `p=1` and has the
   correct pure coefficient `T_d=J_d=1`.

For any preselected `x_j`, choose `k!=j`, put `t_k=-1`, and put every other
`t_i=0`.  Then the target defect is nonzero but `T_{x_j}=0`.  Thus no fixed
mixed coefficient is forced.  Letting `s` grow proves that finite-dimensional
linear algebra, symmetry-free Noetherianity, or the existence of a left
syzygy alone cannot give a uniform sparse bound.

#### Proof

Applying `phi_0` to the chart-zero target equation gives `p=1`; applying
`phi_1` to the chart-one target equation gives `0=p`.  The annihilator of
each nuisance image is the displayed one-dimensional span.  Cancellation on
the common `A` column forces the syzygy to be a multiple of
`(phi_0,-phi_1)`, whose aggregate is (19).

For (20), `T-d` lies in `ker(phi_0)`.  In chart one,
`T-g_1-A_1(1)=-d+sum_i t_i x_i`, and `phi_1` evaluates this vector to
`-1-sum_i t_i=0`.  The remaining assertions are immediate.  `square`

This is an affine proof-route countermodel, not a graph response or a graph
witness.  It isolates exactly what matching integrability or the full target
locus would still have to improve.

## 4. Arbitrarily wide cloned physical camouflage atlas

The response-level obstruction is stronger: even complete compatibility on
arbitrarily many overlapping windows does not force either activity or a
defect.

Let each port space be `K^3` with coordinate covectors `e_0,e_1,e_2`.  Fix
two residual vertices `Q={q_0,q_1}` and residual edge scalar `h=1`.  Use ports

```text
U = {0,1,2} disjoint_union C,       C={3,...,m+2},       m>=1. (21)
```

The residual incidence rows are

```text
a_0=a_1=e_0,       b_0=b_1=e_1,
a_2=a_j=e_1,       b_2=b_j=e_0       for j in C.          (22)
```

Put

```text
K_uv = a_u tensor b_v + b_u tensor a_v.                       (23)
```

Define diagonal pair-response tensors `D_uv` on the edges used by the atlas:

```text
D_01 = E_22,                    D_2j = E_22,
D_02 = E_00+E_11,               D_12 = 3E_00+2E_11,
D_0j = E_00+(2/3)E_11,          D_1j = 2E_00+2E_11,           (24)
```

for every `j in C`.  On clone--clone edges choose any diagonal `D_jk`; zero
is enough.  Finally define the physical direct blocks

```text
B_uv = D_uv-K_uv.                                                   (25)
```

For every clone `j`, let

```text
W_j={0,1,2,j}.                                                       (26)
```

These windows share the same named residual pair and the common triple
`{0,1,2}`.

### Theorem 6 (cloned two-active observed-package atlas)

For every `m>=1`, the data (21)--(26) define one physical `q=2` atlas of
pair/four observed packages with the following properties.

1. Every pair response on a chart is exactly the diagonal tensor `D_uv`.
2. Every four-port response, in the port order `(0,1,2,j)`, is

   ```text
   T_j = 3 e_0^tensor4 + (4/3)e_1^tensor4 + e_2^tensor4.       (27)
   ```

   Thus all four-port mixed coefficients vanish and all three pure
   coefficients are nonzero.
3. Colour `2` is inactive at every port of every chart in the precise sense
   of the three-active hypothesis of the pair/four-port interference theorem.
   Hence no chart supplies its nine-word determinant.
4. All overlaps agree literally in one physical gauge.  Their transition is
   the identity and every atlas holonomy is trivial.
5. A second physical graph is obtained by replacing all `b_u` by `-b_u`,
   hence `K_uv` by `-K_uv`, and replacing every direct block by `D_uv+K_uv`.
   Every selected pair and four-port response is unchanged, while the
   corrected channel changes.  Each realization separately supplies one
   literal same-graph atlas with identity overlaps.  The two corrected
   channels are not related by a common `O(J)` response-frame gauge, because
   such a gauge preserves every bilinear tensor `K_uv`.

#### Proof

The pair identity is `D_uv=B_uv+K_uv`, since `h=1`.

Every window `W_j` has the same labelled data as the four-port camouflage
control after identifying `j` with port `3`.  Direct calculation gives

```text
C(D)-C(K)
 = 3 e_0^tensor4 + (4/3)e_1^tensor4 + e_2^tensor4,             (28)
```

and the pair/four-port interference identity identifies the left side with
the physical four-port response.  For completeness, the exact primary
verifier and independent audit enumerate the six-vertex perfect matchings.

The only colour-`2` pair tensors in `W_j` are `D_01` and `D_2j`.  If a port
uses one of these as its colour-`2` active edge, the complementary edge is the
other and has no colour different from `2`.  Therefore the required
`delta_2!=2` complementary product is zero at every port.  This proves item
3.  Items 4 and 5 follow from the common rows and from the even occurrence of
`K` in `C(K)`.  The sign realization is a second graph, not a second hidden
channel inside one fixed graph.  A common `O(J)` gauge leaves
`F_u^T J F_v=K_uv` invariant, whereas the sign change is nontrivial in
characteristic zero.  `square`

The construction works for arbitrary `m`.  It therefore refutes the hoped-for
response-level dichotomy

```text
second overlapping window
  => some chart becomes three-active or an overlap defect appears.          (29)
```

Only the selected sunflower charts `{0,1,2,j}` are controlled.  A four-set
containing multiple clones has new response equations, and no higher response
on the full union is asserted.  Thus the example does not refute a theorem
using the complete family of all subwindows or a deeper union response.

The sign ambiguity is only an ambiguity of the observed `D`-pair/`T`-four
package.  A complete GLQ2 paired-depth chart retains the residual-absent deck
`M`, whose pair layer is the direct block `B`; it therefore distinguishes the
two sign realizations.  The construction also does **not** refute a theorem
whose hypothesis says that every chart is the output of already-proved
nuisance-free constant selectors from one full GHZ equation.  It supplies
physical response data of the required diagonal shape, not that upstream
target attachment.

## 5. Breadth, depth, transitions, and global interface

| item | exact content |
|---|---|
| breadth | two arbitrary constant uncontracted charts in Theorems 1--2; an arbitrary star of overlapping `K_4` charts in Theorem 6 |
| depth | one common chart sector in the affine theorem; residual-present pair and four-port response depths in the physical observed-package atlas |
| common hidden data | the affine theorem names `p`; each physical realization uses one common residual pair, one scalar `h`, common incidence rows, and one direct deck |
| transition group | no transition is needed for the affine rank statement; each physical sign realization has literal identity transitions |
| agreement output | unique common `p` only when `ker(bar A)=0`; cloned `D`/`T` agreement does not identify `K`, although the complete `M,Z` chart would distinguish the displayed signs |
| disagreement output | a target-defect aggregate, mixed after synchronizing the complete pure basis; one displayed coefficient only under Definition 3 |
| permanent output | none |

Consequently the live Universal Supply obligation is narrower but not closed.
A positive successor must use at least one datum absent from the cloned atlas:

1. prove constant nuisance-free target attachment from the full hypothetical
   witness equation;
2. use a coefficient-pure cross-window syzygy supplied by that target
   attachment;
3. use a genuinely deeper response layer on the union; or
4. prove a witness-locus structural condition excluding the two-active
   corrected-channel fibre.

The abstract dense family shows that a bounded coefficient certificate cannot
be inferred from cross-chart linear algebra alone.  A bounded-obstruction
theorem must prove its sparse support using the target/matching structure.

## 6. Evidence and limitations

The focused primary verifier
[`verify_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py`](verify_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py)
checks exact rational rank identities, the dense affine family, every pair and
four-port response in finite cloned atlases, activity failure, and the global
sign ambiguity.

The independent no-import audit
[`audit_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py`](audit_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py)
uses a separate standard-library row reduction and a direct perfect-matching
recurrence on the physical six-vertex charts.  The programs replay the bounded
displayed controls; the written arguments prove the arbitrary characteristic-
zero statements.

What remains **UNKNOWN**:

- whether every hypothetical witness supplies even one constant target-
  attached same-`Q` pair/four window;
- whether two such genuinely attached windows force a coefficient-pure
  syzygy on the witness locus;
- whether six-port target depth closes every normalized two-active physical
  atlas;
- whether a common corrected factorization can be made weighted diagonal;
- whether any permanent restriction follows; and
- the global Krenn--Gu conjecture.
