# A full five-root sensor labels all 219 mixed cofactors on a legal open chart

## Status

**Exact characteristic-zero existence theorem and pinned-star gating no-go.**
For five roots and nine named nonroots, the complete mixed-root matching
expansion has exactly

```text
binom(9,5)+binom(9,3)+binom(9,1)=126+84+9=219          (1)
```

complementary-cofactor labels.  They are the depth-five principal
four-hafnians, the depth-three principal six-hafnians, and the depth-one
principal eight-hafnians.  This note constructs legal symmetric three-colour
edge blocks for which their complete companion-incidence map has rank 219 in
the `3^5=243` dimensional full root coefficient space.  Thus every label has
an individual linear selector on a nonempty Zariski-open chart.  There is no
remaining nuisance-label ambiguity on that chart.

The construction simultaneously has fully supported roots, all seven named
blockers active, both residual vertices nonblocking, and every root pair
zero-coupled.  It therefore proves that those incidence requirements do not
themselves obstruct a full sensor.  It does **not** prove that a hypothetical
GHZ witness lies in the open sensor chart, nor that the displayed graph
satisfies the GHZ tensor equations.

In fact, the displayed chart has a sharp target-incidence obstruction.  If
`Delta` is the three-dimensional diagonal root space spanned by
`e_c^(tensor 5)`, then

```text
im(Gamma) intersect Delta = {0}.                       (1a)
```

The combined `243 x 222` matrix has rank 222 by a second named integer
minor.  Hence a nonzero five-root GHZ coefficient cannot occur on a whole
open neighborhood of this otherwise complete sensor.  Any actual GHZ
witness must lie on the determinantal incidence locus where the companion
image meets `Delta`, or on the sensor rank-drop locus.  This explains why a
legal full sensor is not yet a witness-compatible sensor.

For the smaller three-root/seven-nonroot `P_5` cell, a proposed pinned-star
reconstruction asks for 15 depth-three labels containing a pin `p` and six
depth-one labels.  Merely finding those 21 columns independent is logically
insufficient: the other 21 mixed cofactor columns are nuisance columns in the
same 27 root channels.  The exact selector requirement forces their span to
have dimension at most six.  Moreover, the natural support-gating attempt to
kill all 20 unwanted depth-three columns can expose at most nine of the 15
star directions.  This is a symbolic Konig-cover obstruction, not a support
enumeration.  More subtle algebraic compression or cancellation of the
nuisance span remains **UNKNOWN**.

No support family, graph family, or parameter family is enumerated.  The
rank proof is one named integer minor of the symbolic matching operator.  A
nonzero modular residue is used only as an exact certificate that this
specific integer determinant is nonzero; no finite-field experiment is
promoted to a characteristic-zero conclusion.

## 1. The complete odd-depth companion operator

Let `R={0,1,2,3,4}` be five roots, let `N={0,...,8}` be nine nonroots, and
let `V_i=K^3`.  After fixing a vector at each nonroot, write

```text
h_(i,u) in V_i^*                                      (2)
```

for the root-side form of the edge `i--u`, and write

```text
L_ij in V_i^* tensor V_j^*                            (3)

```

for the root--root block.  For a five-set `D subset N`, define

```text
G_D^(5)
 =sum_(f:R -> D bijective) tensor_(i in R) h_(i,f(i)). (4)
```

For a three-set `D`, define

```text
G_D^(3)
 =sum_({i,j} subset R) L_ij tensor
   sum_(f:R minus {i,j} -> D bijective)
       tensor_(k notin {i,j}) h_(k,f(k)),              (5)
```

where every factor is placed in its named root slot.  Finally, for `u in N`,
let

```text
G_u^(1)
 =sum_(M a two-edge matching of R)
    tensor_({i,j} in M) L_ij tensor h_(k,u),           (6)
```

where `k` is the unique root missed by `M`.

Restricting a perfect matching to `R` proves, without any genericity
assumption, that the complete full-root coefficient tensor is

```text
T_R
 =sum_(|D|=5) G_D^(5) C_D
  +sum_(|D|=3) G_D^(3) C_D
  +sum_(|D|=1) G_D^(1) C_D.                           (7)
```

There are no other depths: a root partial matching has zero, one, or two
edges and therefore leaves five, three, or one roots to use nonroots.
Introduce the labeled companion map

```text
Gamma:
 K^(binom(N,5)) direct-sum K^(binom(N,3)) direct-sum K^N
 -> tensor_(i=0)^4 V_i^*,                             (8)
```

whose columns are (4)--(6).  The deletion-label selector theorem says that
all 219 cofactors in (7) are individually observable exactly when `Gamma` is
injective.

## 2. A legal integer chart

Use the coordinate covectors `e_0,e_1,e_2` and put

```text
x_i=(1,1,1) for every root i.                          (9)
```

Name nonroots `b_0,...,b_6,q_0,q_1`, with the first seven intended as
blockers and the last two as residual nonblockers.  The root--nonroot forms
are the following table.

| root | `b_0` | `b_1` | `b_2` | `b_3` | `b_4` | `b_5` | `b_6` | `q_0` | `q_1` |
|---:|---|---|---|---|---|---|---|---|---|
| 0 | `e_1` | `e_1` | `e_0` | `e_1` | `e_2` | `e_1` | `e_1` | `e_1-e_0` | `e_1-e_2` |
| 1 | `e_2` | `e_0` | `e_1` | `e_0` | `e_0` | `e_2` | `e_1` | `e_2-e_0` | `e_1-e_2` |
| 2 | `e_2` | `e_0` | `e_2` | `e_1` | `e_1` | `e_2` | `e_0` | `e_1-e_0` | `e_1-e_2` |
| 3 | `e_2` | `e_1` | `e_1` | `e_2` | `e_1` | `e_0` | `e_2` | `e_0-e_1` | `e_2-e_1` |
| 4 | `e_2` | `e_2` | `e_2` | `e_0` | `e_2` | `e_1` | `e_1` | `e_0-e_2` | `e_2-e_0` |

In the same coordinate bases, use these root--root matrices:

```text
L_01=[[-1, 1,-1], [-1,-1, 1], [ 0,-1, 3]]
L_02=[[-1, 0, 1], [ 0,-1, 0], [ 1, 0, 0]]
L_03=[[ 1,-1, 1], [ 0, 1,-1], [ 1, 1,-3]]
L_04=[[ 1, 0, 0], [-1, 1, 0], [ 0, 1,-2]]
L_12=[[-1, 0,-1], [-1,-1,-1], [ 1, 1, 3]]
L_13=[[ 0, 0,-1], [-1, 1,-1], [-1,-1, 4]]
L_14=[[-1, 1, 1], [ 1, 0, 1], [ 1, 0,-4]]
L_23=[[ 1,-1,-1], [ 1, 1, 0], [ 1, 0,-2]]
L_24=[[ 0, 0, 1], [ 1, 1, 0], [-1, 0,-2]]
L_34=[[ 1,-1, 0], [ 1, 1, 0], [-1,-1, 0]].           (10)
```

Every blocker entry in the table evaluates to one on `x_i`, while both
residual entries evaluate to zero.  Realize the unordered edge `i--u` as

```text
B_(i,u)=h_(i,u) tensor ell_u,
ell_u(z_u)=1,                                         (11)
```

and use its transpose in the reverse orientation.  Then
`B_(i,q_j)(x_i,-)=0`, so `q_0,q_1` are genuine residual nonblockers, while
every `b_u` is active.  Each matrix in (10) has total entry sum zero, hence

```text
L_ij(x_i,x_j)=0.                                      (12)
```

Thus the five roots are fully supported and pairwise zero-coupled.  Equations
(10)--(12) define legal symmetric loopless graph blocks over the integers.

## 3. The named rank-219 certificate

Order the columns of `Gamma` by:

1. five-subsets of `{0,...,8}` in lexicographic order;
2. three-subsets in lexicographic order;
3. the singleton labels `0,...,8`.

Order the 243 tensor-coordinate rows by ternary words
`00000,00001,...,22222`.  Let `M` be the resulting integer matrix.  Take the
first 219 rows, namely the consecutive words from `00000` through `22002`,
and call the square minor `M_0`.  Direct evaluation of (4)--(6) gives

```text
det(M_0) mod 1,000,003 = 297,817 != 0,                 (13)
det(M_0) mod 1,000,033 = 921,291 != 0.                 (14)
```

Either line alone is an exact proof that the named integer determinant is
nonzero.  Therefore `Gamma` has column rank 219 over `Q`, hence over every
characteristic-zero field.

The entries of `Gamma` are polynomial in the entries of the legal edge
blocks.  The same minor is consequently nonzero on a nonempty Zariski-open
subset of the affine parameter space cut out by the linear conditions
`h_(i,q_j)(x_i)=0` and `L_ij(x_i,x_j)=0`.  The full sensor is therefore an
open-chart phenomenon, not an isolated numerical coincidence.

### Theorem 1 (complete P7 mixed-label sensor)

For five fully supported pairwise-zero roots, seven active blockers, and two
residual nonblockers, there exists a legal symmetric graph-side chart on
which all 126 depth-five, all 84 depth-three, and all nine depth-one
complementary cofactors have simultaneous individual linear selectors in the
full root tensor.

In particular, the depth-one labels are not an unaccounted nuisance when the
depth-five and depth-three decks are selected.  The chart exposes the entire
odd deletion filtration at once.

## 4. Consequence for nonlinear P7 tomography

On nine nonroots, the depth-five labels are all principal four-hafnians and
the depth-three labels are all principal six-hafnians.  The established
pinned-star system uses those two named decks to recover every nonroot edge
rationally on its own nonempty coefficient-matrix open set.  Theorem 1
removes the prior **linear sensor capacity** objection on a nonempty legal
root chart and also separates every depth-one nuisance column.

Their product intersection is nonempty in the ambient legal parameter space,
as proved below, but the GHZ equations have not been shown to meet it.  A
hypothetical witness could lie on either rank-drop locus.  Moreover, the
chart (9)--(12) is not asserted to have root tensor equal to the GHZ target.
Therefore this is an exact existence/observability theorem, not a `P_7`
obstruction.

There is nevertheless an exact graph-side local-to-global inverse theorem.
The sensor minor depends only on root--root and root--nonroot companion
blocks.  The pinned-hafnian star determinants in
`PINNED_HAFNIAN_STAR_SYSTEM_AND_RATIONAL_EDGE_TOMOGRAPHY_THEOREM.md` depend
only on the nonroot graph and are nonzero at the all-one graph.  These are
independent parameter families.  Their two nonempty principal opens
therefore have nonempty product intersection.

### Corollary 2 (relative rational local-to-global inverse)

Fix, or retain as known base parameters, the root--root and root--nonroot
companion blocks in the sensor open set.  On the resulting nonempty legal
product-open chart, the full five-root tensor recovers all 219 named
`h_4,h_6,h_8` cofactors linearly through a rational left inverse of `Gamma`.
The pinned `h_4,h_6` star systems then recover all 36 nonroot edge weights
uniquely and rationally.  Thus the relative graph-side map

```text
(known companion blocks, full five-root tensor)
             -> named shallow decks -> nonroot graph            (15)
```

has a rational left inverse on a nonempty open set.

This corollary is conditional on the companion blocks being in the sensor
open set, being available to form the left inverse, and the nonroot graph
being in the pinned-star open set.  It does not reconstruct unknown companion
blocks from the tensor alone, and it is not a claim about the GHZ fibre.
Indeed, the explicit sensor point below is separated from every nonzero
diagonal target by (1a).

## 5. The diagonal target-incidence locus

Let

```text
E:K^3 -> tensor_i V_i^*,
(lambda_0,lambda_1,lambda_2)
 |-> sum_c lambda_c e_c^(tensor 5).                   (16)
```

At a full-rank sensor, a formal nonzero diagonal GHZ completion exists if
and only if

```text
rank[Gamma | E] <= 221,                               (17)
```

equivalently every `222 x 222` minor of `[Gamma|E]` vanishes.  For a fixed
nonzero diagonal target `J_lambda`, completion is equivalent to

```text
rank[Gamma | J_lambda]=219,                           (18)
```

or the vanishing of all corresponding `220 x 220` minors.  Because `Gamma`
is injective, the cofactor vector is then unique.  Principal-hafnian
realizability, pinned-star equations, and nested recurrences become exact
determinant-cleared polynomial conditions on that unique vector.

For the explicit integer chart, append the three columns supported on the
pure words `00000,11111,22222`.  Select the first 221 tensor rows, from
`00000` through `22011`, together with the last row `22222`.  The resulting
named `222 x 222` integer minor `M_Delta` satisfies

```text
det(M_Delta) mod 1,000,003 = 30,011 != 0,
det(M_Delta) mod 1,000,033 = 812,790 != 0.             (19)
```

Thus `[Gamma|E]` has rank 222 and (1a) follows.  As before, either residue is
an exact proof that one specified integer determinant is nonzero.  The same
minor stays nonzero on a Zariski-open neighborhood, proving that the
target-incidence obstruction is nonvacuous.

The coordinate-free quotient, dual left-kernel, Schubert-codimension, and
generic cofactor-line forms of this condition are proved in
`FIVE_ROOT_DIAGONAL_TARGET_INCIDENCE_SCHUBERT_DUALITY_AND_COFACTOR_LINE_THEOREM.md`.
On the generic one-line stratum, the determinant-cleared physical hafnian
test is given in
`P7_TARGET_INCIDENCE_DETERMINANT_CLEARED_HAFNIAN_INTEGRABILITY_THEOREM.md`.

## 6. The P5 pinned-star selector condition

Now take three roots and seven nonroots `{p} disjoint union A`, `|A|=6`.
The full mixed companion map has

```text
binom(7,3)+binom(7,1)=35+7=42                         (20)
```

columns in only 27 root channels.  A pinned-star reconstruction asks for

```text
S_3={D:|D|=3 and p in D},       |S_3|=15,
S_1={{a}:a in A},               |S_1|=6.              (21)
```

The nuisance set is

```text
N_3={D subset A:|D|=3},         |N_3|=20,
N_1={{p}},                       |N_1|=1.              (22)
```

By the individual-label criterion, all 21 selected coordinates are
observable if and only if

```text
rank Gamma_(S union N)=rank Gamma_N+21.               (23)
```

Since the target has dimension 27, (23) requires

```text
rank Gamma_N <= 6.                                    (24)
```

Thus rank 21 of the selected submatrix alone proves nothing about legal
observability in the presence of the other 21 physical columns.

### Theorem 3 (support gating cannot expose the pinned star)

Suppose the unwanted depth-three columns in `N_3` are killed termwise by
zero root--endpoint blocks: equivalently, the bipartite support graph between
the three roots and `A` has no matching of size three.  Then

```text
dim span{G_(pab)^(3):a,b in A distinct} <= 9.          (25)
```

Hence the 15 pinned depth-three labels cannot be individually selected by
such a gating construction, even before the six depth-one labels are added.

### Proof

By Konig's theorem, the root--`A` support graph has a vertex cover of size at
most two.  Let the cover contain `c_R` roots and `c_A` endpoints.

- If `(c_R,c_A)=(2,0)`, all `A` edges use two roots.  Any nonzero matching
  on `{p,a,b}` therefore assigns `p` to the third root.  All star columns
  lie in one fixed root covector tensored with the other two three-dimensional
  root spaces, of dimension at most `3*3=9`.
- If `(c_R,c_A)=(1,1)`, a nonzero star matching must use the one covered
  endpoint.  Only the five pairs containing it can contribute, so the span
  has dimension at most five.
- If `(c_R,c_A)=(0,2)`, only the single pair of covered endpoints can
  contribute, so the span has dimension at most one.
- Covers of size zero or one only decrease these bounds.

This proves (25).  The statement concerns structural zero gating.  It does
not exclude rank-six nuisance compression by cancellations among nonzero
matching terms.

## 7. Scope wall

```text
five-root mixed expansion at depths 5,3,1:             EXACT;
legal pairwise-zero/nonblocker chart:                  CONSTRUCTED;
complete 219-column companion map on that chart:       INJECTIVE;
all P7 mixed deletion labels individually selectable: YES ON THE CHART;
nonempty legal full-sensor Zariski-open set:            PROVED;
sensor plus pinned-star inverse product-open:           NONEMPTY;
all 36 nonroot edges relative to companion data:        RATIONAL UNIQUE;
explicit sensor image meets diagonal target nontrivially: FALSE;
rank[Gamma|diagonal target space] at explicit chart:    222;
nonvacuous target-incidence determinantal locus:        PROVED;
finite-field sampling used as proof:                   NO;
GHZ equations force the sensor open set:               UNKNOWN;
GHZ fibre meets sensor plus pinned-star open set:       UNKNOWN;
displayed chart is a GHZ witness:                       NOT CLAIMED;
P5 selected 21-column rank alone is sufficient:        FALSE;
P5 termwise nuisance support gating works:              IMPOSSIBLE;
P5 algebraic nuisance compression to rank <=6:          UNKNOWN;
P6 selected pinned-system observability:                UNKNOWN;
unrestricted P5/P6/P7 nonrestriction:                  UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py
python claims/p7/audit_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py
python -m py_compile verify_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py audit_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py
uv run --with ruff ruff check verify_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py audit_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py
```

The primary verifier constructs (4)--(6) by a root-matching recursion,
checks all legality contractions, and evaluates the named determinants (13)
and (19).
The independent no-import audit reconstructs every entry by Ryser permanent
formulas and near-perfect root matchings, then evaluates the same named
integer minors modulo the different prime in (14) and (19).  Both are fixed exact
audits of one symbolic linear operator.  Neither searches graph supports,
coefficients, or parameter families.
