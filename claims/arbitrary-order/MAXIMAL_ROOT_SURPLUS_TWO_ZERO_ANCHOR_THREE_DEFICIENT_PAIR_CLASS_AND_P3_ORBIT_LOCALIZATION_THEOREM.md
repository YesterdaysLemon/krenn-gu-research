# Maximum-root surplus-two zero-anchor three-deficient pair-class, dual P3, and eight-orbit localization

## Status

**Candidate exact characteristic-zero parent localization (`GLS67`).**
Continue from the `GLS63` mixed-kernel hierarchy after `GLS66` excludes the
complete exactly-two-deficient branch.  For any two deficient labels left
open, contract every other deficient kernel and every injective nonaxis
cross product, then quotient every pure-axis slot.  The source becomes one
actual pair companion times one common physical deck.  This yields an exact
pair-class constraint on the deficient kernel supports.

For exactly three deficient labels, the pair-class constraints synthesize
with the `GLS63` incidence and singleton theorems to force

```text
no injective pure-axis labels;
exactly three injective nonaxis labels;
one of ten kernel-support/rank/zero-count profiles.    (1)
```

Contracting all three nonaxis cross products identifies the remaining
three-deficient source exactly as one restriction of `P_3`.  Its target is
the diagonal on precisely the colours not killed by a cross-product zero.
The accepted zero and decomposable `P_3` theorems classify its zero and
pure boundaries; the binary target remains an honest `P_3 -> Delta_2`
restriction.  Exact zero, pure, and binary-GHZ controls show that this
three-mode tensor type alone cannot close the branch; the fixed `P,Q`
shore row constraints of the ten profiles remain additional data.

The opposite contraction, at all three deficient kernels with the three
nonaxis labels open, is another exact restriction of the same `P_3`.
When the deficient supports have a common colour, its target is nonzero and
pure.  The injective nonaxis orientation theorem excludes all eight
orientation words.  Thus two of the ten initial orbits are empty, leaving

```text
432 labelled profiles in eight residual orbits.
```

When the common support is empty, the same restriction is zero; the zero
`P_3` theorem forces all three complementary one-port decks to vanish.

This is a serious parent attempt and an exhaustive three-deficient
localization, not an exclusion of the three-deficient branch.  The ten
initial profiles have been reduced to eight residual orbits.  Those eight,
the four-plus-deficient branches, unique-nonrigid branch, attachment,
response, selector, synchronization/activity, nonzero anchor, arbitrary
root order, and the global conjecture remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Parent-theorem checkpoint

The proposition attacked is:

> No complete zero-anchor root-order-three all-six-rigid hypothetical
> witness has three or more deficient auxiliary joint maps.

The present attempt starts with the whole mixed-kernel hierarchy, not one
support fibre.  It proves a reusable pair-class extraction for arbitrary
deficient count, exhausts every rank/support/pure/nonaxis profile when the
count is three, and then identifies the full three-mode source.  The exact
`P_3` controls show why source rank alone stops.  A successor is load-bearing
if it either completes the profile-aware `P_3` classification with the fixed
`P,Q` shore row constraints, couples one of the eight full-cross contractions
to equations with one or more nonaxis labels left open, or supplies an
honest lower-order receiver with all downstream gates.

## Dependencies and notation

- [`GLS63`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)
  owns the mixed deficient-kernel/cross-product hierarchy, the kernel
  supports `A_n`, the disjoint nonaxis zero sets `E_a`, the common-support
  three-zero floor, and the singleton deficient/nonaxis theorem.
- [`GLS66`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_TWO_TWO_SCALAR_AXIS_AND_COMMON_HYPERPLANE_EXCLUSION_THEOREM.md)
  excludes the preceding exactly-two-deficient branch but is not a logical
  premise of the extraction below.
- [The decomposable `P_3` classification](../p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)
  owns every nonzero pure restriction through rank-at-least-two maps.
- [The zero `P_3` theorem](../p3/restrictions/P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md)
  owns every zero restriction through three source subspaces of dimension
  at least two.

Use the `GLS63` partition

```text
Bhat=N disjoint-union P disjoint-union U,             (2)
```

where `N` is deficient, `P` is injective pure-axis, and `U` is injective
nonaxis.

Let `F` be the fraction field of the ambient polynomial domain obtained by
adjoining the two independent probe-variable sets and independent generic
coordinates on every deficient kernel.  All rowspaces, ranks, and quotient
maps below are extended to `F` unless a complex point is stated explicitly.

For a colour `a`, put

```text
M_a={n in N:a in A_n}.                                (3)
```

Thus `e_(n,a)^*` belongs to `row J_n` exactly when `n notin M_a`.

## 1. Universal two-open pair-class extraction

Fix distinct `i,j in N`.  In the `GLS63` hierarchy take

```text
R=N-{i,j},             C=U,
S={i,j} union P.                                      (4)
```

Contract `R` at independent generic kernel vectors and `U` at their cross
products.  Quotient every pure-axis slot by its active full-row line.  Every
source pair meeting a pure-axis slot dies, so the only possible source pair
is `{i,j}`.

Define

```text
T_(ij)={a:R subseteq M_a and E_a=empty}.              (5)
```

### Lemma 1 (pair-class equation)

Every colour in `T_(ij)` satisfies

```text
M_a=R.                                                (6)
```

Moreover, if

```text
C_R={a:M_a=R and E_a=empty},                          (7)
```

then the exact surviving equation is

```text
g_(ij) tensor D_(ij)
 =sum_(a in C_R) gamma_a
    e_(i,a)^* tensor e_(j,a)^* tensor q_(P,a),
gamma_a!=0.                                           (8)
```

Here `D_(ij)` is one quotient of the actual complementary physical deck and
`q_(P,a)` is the product of the pure-slot quotient coordinate classes.  No
deck is selected independently.

### Proof

The generic kernel product in colour `a` is nonzero exactly when every
member of `R` contains `a` in its support.  The cross-product evaluation is
nonzero exactly when `E_a` is empty.  Every pure-slot coordinate class is
nonzero.  Hence (5) is precisely the target support before inspecting the
two open deficient slots.

The source at slot `i` lies in `row J_i`.  If `a in A_i`, apply the quotient
by `row J_i` and then isolate coordinate `a` at the still-unquotiented slot
`j`.  The source vanishes while the nonzero target coefficient does not.
Thus `a notin A_i`; symmetrically `a notin A_j`.  Since it was visible on
all of `R`, (6) follows.  Equation (8) is the remaining hierarchy member.
`square`

### Corollary 1.1 (rank and pure-companion constraints)

Let `k=|C_R|`.

1. Both `row J_i` and `row J_j` contain the `k` coordinate lines in
   `C_R`, so their ranks are at least `k`.
2. If `P` is nonempty, then `k<=1`.
3. If `P` is empty, then `k<=2`.
4. If `k=1`, the two open deficient maps cannot both have rank two.

### Proof

The first statement follows from (6).  If a pure slot exists, the quotient
classes of any two different coordinates are independent: a dependence
would put a vector supported on two coordinates on the active full-support
line.  Here the required nonzero value in all three coordinates is exactly
the inherited `GLS61` active pure-axis theorem, not an extra genericity
assumption.  Thus the target flattening between `{i,j}` and `P` has rank at
least two when `k>=2`, while the left side of (8) has rank one.  If `P` is empty,
the matrix rank of `g_(ij)` is at most two, giving `k<=2`.  Finally `k=1`
would make `g_(ij)` a nonzero pure coordinate companion; the exact `GLS63`
rank-two pure-companion theorem excludes that when both maps have rank two.
`square`

This corollary is uniform in `|N|`.  It is stronger than a support count:
it retains the physical deck and the local ranks at the two open modes.

## 2. Exact finite types for three deficient maps

Now set `|N|=3`.  There are nine possible rigid deficient types.  For a
colour permutation `{c,d,e}={0,1,2}`, write

```text
S_c: rank two, A={c};
R_c: rank one, row J=K e_c^*, A={d,e};
T_c: rank two, A={d,e}.                               (9)
```

Each nonaxis label has either no identically zero cross coordinate or one
of the three zero coordinates, because the `E_a` are disjoint.

The finite starting set therefore has

```text
9^3 sum_(p=0)^3 4^(3-p)=61,965                       (10)
```

ordered typed profiles, where `p=|P|` and `3-p=|U|`.

### Lemma 2 (three-deficient typed census)

The `GLS63` common-support and singleton rules leave `2,367` labelled
profiles.  Applying Lemma 1 and Corollary 1.1 leaves `516`, all with

```text
P=empty,                 |U|=3.                      (11)
```

The local target-span condition from the full `P_3` source below leaves
exactly `453` labelled profiles in the ten colour/map-permutation orbits of
Table 1.

### Table 1. Exact three-deficient residual

In the middle column, `(x,y,z)` means
`(|E_0|,|E_1|,|E_2|)`.  The last column is the number `t` of colours with
empty `E_a`, hence the rank of the full-cross target.

| orbit | deficient types | zero counts | `t` |
|---:|---|---:|---:|
| 1 | `S_0,S_0,S_0` | `(3,0,0)` | 2 |
| 2 | `S_0,S_0,S_1` | `(2,1,0)` | 1 |
| 3 | `S_0,S_0,R_0` | `(1,1,1)` | 0 |
| 4 | `S_0,S_0,T_0` | `(2,0,0)` | 2 |
| 5 | `S_0,S_0,T_0` | `(3,0,0)` | 2 |
| 6 | `S_0,R_2,R_1` | `(3,0,0)` | 2 |
| 7 | `S_0,R_2,R_0` | `(1,2,0)` | 1 |
| 8 | `S_0,R_2,S_2` | `(2,1,0)` | 1 |
| 9 | `S_0,S_1,S_2` | `(1,1,1)` | 0 |
| 10 | `R_2,R_1,R_0` | `(1,1,1)` | 0 |

### Proof

The nine types in (9), the four cross-zero statuses, and all possible
`P/U` counts are finite and exhaustive by `GLS63`.  Its common-support
three-zero floor and singleton theorem give the first reduction.  Lemma 1
and Corollary 1.1 give the second.

For the last reduction, let `D_T` be the span of the target coordinate
lines with `E_a=empty`.  At a deficient mode the full-cross source has local
image contained in

```text
row J_i+F h_i.                                        (12)
```

Therefore `D_T` can add at most one dimension modulo `row J_i`.  At a
rank-one type `R_c`, this says that at most one target colour differs from
the readout `c`.  Applying that test removes sixty-three more labelled
profiles.  Exact enumeration gives Table 1.  The primary verifier and a
separate standard-library audit replay all `61,965` cases and agree on each
intermediate count. `square`

The census is a necessary-profile localization.  It does not assert that
any row of Table 1 extends to a physical witness.

## 3. Exact full-cross `P_3` extraction

Under (11), take `R=empty`, `C=U`, and `S=N` in the mixed hierarchy.  For
`{i,j,k}=N`, define the actual remaining one-port deck row

```text
h_k=H_(Bhat-{i,j})(k_U,-_k),                          (13)
```

and define a local map on source labels `P,Q,H` by

```text
L_i(P)=p_i,             L_i(Q)=q_i,
L_i(H)=h_i.                                             (14)
```

### Lemma 3 (the full-cross source is `P_3`)

The exact hierarchy member is

```text
(L_0 tensor L_1 tensor L_2)P_3
 =sum_({i,j} subset N) g_(ij) tensor h_(N-{i,j})
 =sum_(a:E_a=empty) kappa_a
    e_(0,a)^* tensor e_(1,a)^* tensor e_(2,a)^*,
kappa_a!=0.                                           (15)
```

### Proof

For each of the three choices of pair `{i,j}`, the companion supplies the
two orders `P,Q`; the complementary port receives `H`.  These are the six
permutations defining `P_3`, once each.  A target colour survives all three
cross products exactly when `E_a` is empty, and its coefficient is a
product of nonzero polynomials in a domain. `square`

Thus the last column of Table 1 is simultaneously the target tensor rank
and every target flattening rank.

### Corollary 3.1 (the pair scalar is the same one-port deck)

For `{i,j,k}=N`, the scalar deck in the pair-class equation (8) is exactly

```text
D_(ij)=h_k(x_k),                                      (16)
```

where `x_k` is the generic vector of `K_k`.  Consequently, if
`C_({k})` is nonempty, then

```text
h_k|_(K_k)!=0,        h_k notin row J_k,
rank L_k>=2.                                          (17)
```

### Proof

The pair member takes `R={k}`, whereas the full-cross member leaves `k`
open.  Their complementary physical deck is otherwise evaluated at the
same three cross products.  Thus the former is precisely evaluation of
the latter at `x_k`, proving (16).  A nonempty class makes the right side
of (8) nonzero, so `h_k(x_k)` is nonzero.  The annihilator of `K_k` is
`row J_k`; hence `h_k` is outside that rowspace.  At least one of the
generic vectors `p_k,q_k` is nonzero and lies inside `row J_k`, which gives
the rank assertion. `square`

## 4. All-deficient-kernel `P_3` and common-support exclusion

The displayed `P_3` identities live over the common characteristic-zero
fraction field `F`, whereas the two cited classification files state their
results over `C`.  Their written proofs use only finite-dimensional linear
algebra, polynomial identities, and division by declared nonzero elements;
they therefore apply verbatim after extending `F` to its algebraic closure.
The coordinate-plane alternative, ranks, zero coordinates of normals, and
proportionality consequences used below all descend to `F`.  No complex
specialization or silent function-field-to-pointwise step is being used.

For `{u,v,w}=U`, define the complementary one-port row obtained after all
three deficient kernels are contracted by

```text
d_u=H_(Bhat-{v,w})(x_N,-_u),                         (18)
```

Each `d_u` depends on the fixed physical graph and the deficient-kernel
variables, but is independent of both probe-variable sets `z_0,z_1`.  This
separation is load-bearing in Theorem 5.

and put

```text
K_u(P)=p_u,             K_u(Q)=q_u,
K_u(H)=d_u.                                             (19)
```

### Lemma 4 (the kernel-side source is the same `P_3`)

The exact `R=N,C=empty,S=U` hierarchy member is

```text
(tensor_(u in U) K_u)P_3
 =sum_(a in A_N) theta_a tensor_(u in U)e_(u,a)^*,
theta_a!=0.                                           (20)
```

Every `K_u` has rank at least two.  If `A_N` is empty, then

```text
d_u=0 for every u in U.                              (21)
```

### Proof

The three choices of a pair in `U`, and the two `P,Q` orders in its
companion, again give the six permutations of `P,Q,H`.  A target colour
survives the three generic deficient-kernel contractions exactly when it
belongs to every `A_n`, which proves (20).  Every nonaxis `u` has
`p_u cross q_u!=0`, so `p_u,q_u` are independent and `rank K_u>=2`.

When `A_N` is empty, apply the zero-`P_3` theorem.  The three source
rowspaces are one common coordinate plane.  It cannot omit `P` or `Q`,
because that would make respectively `p_u` or `q_u` zero at an injective
nonaxis mode.  It therefore omits `H`, which is exactly (21). `square`

### Theorem 5 (common deficient support is impossible)

No exactly-three-deficient profile has `A_N!=empty`.  Consequently Table 1
orbits 1 and 6 are empty.  They account for twenty-one labelled profiles,
and the exact residual is

```text
432 labelled profiles in eight colour/map orbits.    (22)
```

### Proof

By the `GLS63` common-support floor, `A_N` contains at most one colour.  If
it contains `c`, then `E_c=U`, because `|U|=3` and `|E_c|>=3`.  Equation
(20) is therefore a nonzero pure target on three injective nonaxis ports,
each having one of the two exact `c`-orientations from `GLS61`.

Write a bar for quotient by the target `c`-line.  First suppose all three
ports have the `X`-orientation.  Then

```text
p_i=alpha_i c_i,      alpha_i!=0,
span of the coefficients of bar(q_i)=bar(V_i^*).
```

The scalar `alpha_i` is nonzero because otherwise `p_i cross q_i` would be
the zero polynomial, contrary to the nonaxis hypothesis.

Quotienting two slots `i,j` in (20), with `{i,j,k}=U`, gives

```text
bar(q_i) tensor bar(d_j)+bar(d_i) tensor bar(q_j)=0. (23)
```

The coefficient span of each displayed generic row is two-dimensional.  A
fixed nonzero `bar(d_j)` would force every value of `bar(q_i)` onto the
fixed `bar(d_i)` line, and symmetrically; hence every `bar(d_i)=0`.  Write
`d_i=delta_i c_i`.  Quotienting only slot `i` now gives

```text
alpha_j delta_k+alpha_k delta_j=0                    (24)
```

for all three choices.  Over the fraction field divide by the nonzero
`alpha_i`; the three pairwise sums force every `delta_i=0` in
characteristic zero.  The source side of (20) is then zero, a contradiction.
The all-`Y` orientation is symmetric.

It remains to treat a mixed word.  Up to exchanging probes and permuting
ports, take `i,j` to have the `X`-orientation and `k` the `Y`-orientation.
Quotienting the two `X` slots gives (23), tensored with the nonzero row
`p_k`, so `bar(d_i)=bar(d_j)=0`; write
`d_i=delta_i c_i,d_j=delta_j c_j`.  Quotienting only slot `i` gives

```text
alpha_j d_k+delta_j p_k=0.                           (25)
```

Modulo the `c`-line, the coefficient span of `p_k` is two-dimensional.
Since `d_k` is independent of the probe variables, (25) forces
`delta_j=0` and then `d_k=0`.  The symmetric slot-`j` equation forces
`delta_i=0`.  Again the complete source vanishes.  This covers all mixed
orientation words and contradicts the nonzero pure target.

The finite census identifies precisely Table 1 orbits 1 and 6 as having a
common support.  Their orbit multiplicities are `3` and `18`; removing them
from `453` gives (22). `square`

The fibre-level mixed-orientation controls in `GLS63` do not contradict
Theorem 5.  Those controls choose rows such as `d_i=-p_i` after fixing the
probe values.  Here each actual complementary deck depends on the graph and
the deficient-kernel variables but not on `z_0,z_1`, and (20) is a
function-field identity in both probe sets.  That separation is exactly
what forces the decks to vanish above.

## 5. Exact full-cross `P_3` orbit fork

### Theorem 6 (`GLS67`)

Every hypothetical exactly-three-deficient witness lies in one of the eight
residual profiles `2,3,4,5,7,8,9,10` of Table 1 and its full-cross source
obeys the following exhaustive fork.

1. **Binary target (`t=2`).**  Retraction to the two target coordinate
   lines gives three rank-two maps whose `P_3` restriction is locally
   equivalent to `Delta_2`.
2. **Pure target (`t=1`).**  If every `L_i` has rank at least two, all three
   have rank exactly two and their source-plane normals belong to one of the
   exact decomposable-`P_3` sign charts.  Otherwise some `L_i` has rank one,
   and every such mode is a rank-one deficient map whose coordinate readout
   is the surviving target colour.  Consequently orbit 2 is necessarily in
   the sign-chart alternative.  In orbits 7 and 8 the sign-chart alternative
   is impossible and their displayed `R_2` mode has rank-one `L_i`; its
   `p_i,q_i,h_i` all lie on the target `2`-line.
3. **Zero target (`t=0`).**  If every `L_i` has rank at least two, their
   source rowspaces are one common coordinate plane.  Equivalently, exactly
   one of the three uniform source-coordinate alternatives holds:

   ```text
   X_0=X_1=X_2=0,  or  Y_0=Y_1=Y_2=0,
   or  h_0=h_1=h_2=0.                                (26)
   ```

   Otherwise some `L_i` has rank one.

### Proof

For `t=2`, the target local slice plane lies in every `im L_i`; choose a
linear retraction onto it.  The retracted maps have rank two because the
target is concise, and preserve (15).  For `t=1`, apply the accepted
decomposable `P_3` classification whenever all ranks are at least two.  For
`t=0`, apply the accepted zero `P_3` theorem under the same hypothesis.

If the nonzero pure target has colour `a` and `rank L_i=1`, target
conciseness at mode `i` makes `im L_i=F e_(i,a)^*`.  In particular the
generic rows `p_i` and `q_i` both lie on that fixed coordinate line.  Their
coefficients in the independent probe variables show that every row of
`X_i` and `Y_i` lies on the same line.  Thus `J_i` has rank one and readout
`a`: the all-six-rigid hypothesis has already excluded rank zero.  This
proves the sharpened pure alternative and its orbit statements.

It remains to justify the stronger conclusion for orbits 7 and 8.  Their
surviving target colour is `2`.  In orbit 7 its support class `M_2` is the
displayed `R_0` mode; in orbit 8 it is the displayed `S_2` mode.  Corollary
3.1 makes the corresponding `L_i` rank at least two.  Every rank-two
deficient `J_i` also rules out rank-one `L_i` in a nonzero pure target,
because a rank-one image would be the fixed target line and would put all
rows of `X_i,Y_i` on that line.  Thus the only possible low-rank mode in
either orbit is `R_2`.

Suppose instead that all three maps had rank at least two.  At the
pair-class mode in orbit 7, `J_i` has rank one and `h_i` lies outside its
row line.  Its rank-two source plane therefore has a normal whose `H`
coordinate is zero.  The same conclusion holds at the pair-class mode in
orbit 8: `h_i` lies outside `row J_i`, so any rank-two relation among
`p_i,q_i,h_i` has zero `H` coefficient.  In an exact decomposable-`P_3`
sign chart, a source coordinate vanishes in one normal if and only if it
vanishes in all three normals.  Moreover no sign-chart normal has support
one.  Hence every local relation would use both `P` and `Q` but not `H`,
forcing `p_i` and `q_i` to be proportional at every mode.  Independence of
the two probe-variable sets then puts the complete row spaces of `X_i` and
`Y_i` on one fixed line, contradicting the rank-two deficient modes in
both orbits.  Therefore `L_(R_2)` has rank one and target conciseness puts
all three of its columns on the target line.

In the zero case, a common coordinate plane in the source coordinates
`P,Q,H` omits exactly one of those coordinates.  Omitting `P` makes every
`p_i` the zero polynomial and hence every `X_i=0`; omitting `Q` similarly
makes every `Y_i=0`; omitting `H` is exactly the last alternative in (26).
`square`

## 6. Sharp source controls and the impediment

All three endpoints of Theorem 6 are algebraically nonempty.

**Binary GHZ.**  Let `beta=(1,1,1)` and restrict every source mode to the
plane `beta^perp`, with basis

```text
u=(-1,1,0),              v=(-1,0,1).                 (27)
```

The resulting binary `P_3` tensor has Cayley hyperdeterminant `-48`, hence
is in the open binary GHZ orbit.

**Pure.**  The source-plane normals

```text
(1,1,1),        (1,-1,-1),        (1,-1,1)           (28)
```

give exactly two nonzero adjacent binary coefficients, hence one nonzero
decomposable tensor.

**Zero.**  Restrict all three modes to the common coordinate plane
`span{P,Q}`.  The restriction is zero because no term can use source label
`H`.

The physical content of the remaining obstruction can also be displayed
exactly.  If `U={u,v,w}` and

```text
w_(uv)=W_(uv)(k_u,k_v),
```

then hafnian expansion of the common one-port deck gives, for every
deficient mode `i`,

```text
h_i=W_(iu)(-,k_u)w_(vw)
   +W_(iv)(-,k_v)w_(uw)
   +W_(iw)(-,k_w)w_(uv).                             (29)
```

This formula is same-source bookkeeping, but not by itself a fibrewise
no-go.  At one fixed fibre, if one displayed internal `U` cofactor is
nonzero, the distinct physical edges incident to each `i` can prescribe
the corresponding `h_i` rows independently.  Those edges reappear in the
higher-open hierarchy, so their polynomial compatibility there is the
remaining integrability datum.

These are exact source restrictions, not physical GHZ graph witnesses, and
they do not satisfy the eight residual profiles' fixed shore-row constraints by
declaration.  They prove only that target rank and the abstract `P_3`
endpoint type do not furnish a contradiction.  The load-bearing successor
must either use the fixed `P,Q` row constraints inside the `P_3`
classification or couple the resulting plane/normal data to the same
physical decks in hierarchy members where one or more of the three nonaxis
labels remain open.  A fibrewise choice of a different `P_3` basis is
insufficient.

## 7. Exact frontier

```text
universal two-open pair-class extraction:             PROVED;
exactly-three-deficient pure-axis count:               P=empty, |U|=3;
three-deficient typed support profiles:                TEN / LOCALIZED;
common-support profiles 1 and 6:                       EXCLUDED;
three-deficient residual:                              432 / EIGHT ORBITS;
kernel-side source on the residual:                    ZERO P_3 / d_U=0;
full-cross source:                                     P_3 / PROVED;
binary, pure, zero P_3 endpoints:                      ALL NONEMPTY;
exactly-three-deficient branch:                        OPEN;
four-plus-deficient branches:                          OPEN;
unique-nonrigid / alternate receiver:                  OPEN;
response/selector/synchronization/activity package:    OPEN;
nonzero-anchor and arbitrary-root strategic node:      OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED. (30)
```

## 8. Verification boundary

The primary verifier enumerates the nine deficient types, every pure/nonaxis
count and labelled cross-zero assignment, all pair-class constraints, the
ten localized and eight residual canonical orbits, and the six `P_3` source
assignments.  It also checks the binary hyperdeterminant and the pure/zero
controls.  The independent standard-library audit uses integer support
masks and a separate finite implementation and independently recovers the
`432/8` residual.  These programs audit the finite and displayed algebraic
leaves and controls; they do not independently prove the symbolic
orientation quotient.  The same-source extraction, orientation quotients,
and `P_3` bridges above remain the written proof.

From repository root run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
```
