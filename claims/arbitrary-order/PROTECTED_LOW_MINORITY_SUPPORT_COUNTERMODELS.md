# Protected low-minority support countermodels

Date: 2026-09-22.

## Status and exact parent

**Proved, with dedicated independent agent reviews:** every fixed paired-
minority support cutoff has a finite countermodel, even with all whole port
graphs acyclic. P1 has an explicit 18-component certificate; the general
fixed-cutoff result is a probabilistic existence theorem with a written
proof. The
global Krenn--Gu conjecture and the full weighted protected-source parent
SFULL remain **UNRESOLVED**. No global counterexample is asserted.

The definitions are those of the
[paired-minority owner](PROTECTED_PAIRED_MINORITY_SOURCE_AND_REPAIR_BOUNDARY.md).
There are `k>=2` protected unit K4 components, with local vertices
`O,L_0,L_1,L_2` and

```text
M_c = {O L_c, L_a L_b},       {a,b,c}={0,1,2}.
q_c(w) = number of M_c pairs whose two word colors both differ from c.
```

A macro word is constant on each component. P1 requires (i) at least one
crossing matching at every mixed macro word, in addition to its protected
matching, and (ii) no mixed word with `min_c q_c<=1` having exactly one
supported scalar perfect matching. The excluded proposition was that no
such support exists at any `k>=2`. DAG-P1 adds acyclicity of every whole
port graph `D_c`; it is refuted by the same construction.

Every full complex weighted source supplies P1, but the converse was never
claimed. A support countermodel therefore refutes this proposed sufficient
proof route, not the weighted conjecture. The construction below makes all
mixed `q_c<=1` fibres empty, a stronger property than merely avoiding a
singleton fibre.

## 1. A family with no one-pair word

Use the exact
[common-star family](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md).
Every edge of a **simple component graph** has exactly one unequal endpoint
label `(a,b)` and exactly two crossing scalar entries:

```text
O_u O_v[a,b],       L_a(u) L_b(v)[a,b].
```

All protected entries are unit; every other crossing entry is zero. Each
displayed crossing can have any nonzero weight. The support arguments do
not use their values. Require that the component graph is triangle-free.

**Lemma.** For each color `c`, the only supported `q_c=0` word is the pure
all-`c` word, and no supported word has `q_c=1`.

Here is a complete proof, including the physical matching constraints.
In any scalar perfect matching each component has zero, two, or four
crossed vertices. Its possible local states are precisely:

| State | Crossed ports | Local colors | Local contribution to `q_c` |
| --- | --- | --- | --- |
| uniform | none | all `t` | 0 if `t=c`, otherwise 2 |
| AB | `O,L_s` | leaves all `s`, center `x` | 0 if `s=c`; 1 if `s!=c,x=c`; otherwise 2 |
| BB | two leaves, other leaf `L_t` protected to `O` | center `t`, each leaf `L_j` has color `j` | 1 |
| four-cross | all four | center arbitrary, each leaf `L_j` has color `j` | 1 |

For example, in an AB state the other two leaves are internally matched.
Their protected edge forces both to color `s`, and the crossing at `L_s`
has endpoint color `s`. The BB and four-cross rows follow from the same
literal protected colors and own-color-only crossing leaves. Odd crossing
degrees leave an odd number of internal vertices and are impossible.

Every local `q_c=0` state has all leaves color `c`. If a global `q_c=0`
matching crossed anywhere, every crossed leaf would consequently have
color `c`, requiring a forbidden equal-color crossing. Thus nothing
crosses and the word is pure all-`c`.

For `q_c=1` there is exactly one root component with positive local pair
count. All other components are uniform `c` or AB with all leaves `c`.
Exhaust the root states:

1. **AB root.** Its leaves all have some color `d!=c`, and its center has
   color `c`. Its only crossed leaf must meet the color-`c` leaf of an
   outside AB component `B`. No other outside component can cross: each
   such component would need another non-`c` root leaf. Therefore the two
   centers must also match each other. On the same component edge the leaf
   entry would require label `(d,c)` and the center entry `(c,x)`, which
   contradicts the one-label hypothesis.
2. **BB root whose protected edge has color `c`.** Its two non-`c` leaves
   cross to the color-`c` leaves of two distinct outside AB components
   `B,C`. They must be distinct because a physical leaf is used once. No
   further component can cross. The centers of `B,C` must match, so the
   component edges root--`B`, root--`C`, and `B`--`C` form a triangle.
3. **BB root with protected color different from `c`, or four-cross
   root.** The root's color-`c` leaf crosses. Its opposite endpoint must be
   a non-`c` leaf with that leaf's own non-`c` color, whereas all outside
   leaves have color `c`. This is impossible.

These cases exhaust the table and prove the lemma at every finite order.
Triangle-freeness is used only in case 2; the one-label hypothesis is
load-bearing in case 1.

Every whole port graph is also acyclic. An arc of `D_c` from a crossing
entry goes from its non-`c` endpoint `v` to the protected partner of its
color-`c` endpoint. Thus center-center entries give `O -> L_c`, while
leaf-leaf entries give `L_a -> O`, `a!=c`. Every arc respects

```text
non-c leaves  <  centers  <  c-leaves.
```

This is a literal three-level ordering of all vertices, without deleting
any arc. It proves the whole-DAG premise directly.

## 2. An analytic macro-complete construction

Take six left components `L_1,...,L_6`. Let
`P={01,02,10,12,20,21}` be the six ordered unequal color pairs. For every
permutation `pi` of `P`, create a right component `R_pi` and label
`L_i--R_pi` by `pi(i)`. The component graph is `K_(6,720)`: simple,
bipartite, and triangle-free. This gives `k=726` protected components.

For left colors `x=(x_1,...,x_6)`, the right colors forbidden by column
`pi` are exactly

```text
B_pi(x) = { b : pi(i)=(a,b) and x_i=a for some i }.
```

If all left colors equal `c`, every column contains both pairs `(c,b)`
with `b!=c`. Avoiding a compatible gadget forces every right color to
equal `c`. These are the three globally constant assignments.

If `x` is nonconstant, choose two positions colored `a` and a third
position colored `b!=a`; six positions in three colors always permit this.
For the third color `d`, assign those positions the distinct labels
`(a,b),(a,d),(b,a)` and extend to a permutation of `P`. The corresponding
`B_pi(x)` contains all three colors, so that right component cannot avoid
an enabled gadget.

Therefore every mixed global macro word enables some gadget. Its two
crossings and the complementary protected leaf pair at each endpoint
give a physical perfect matching; protect every other component. This
matching differs from the all-protected macro matching. Macro coverage is
proved without enumerating `3^726` assignments.

Combining this construction with section 1 refutes both universal parent
exclusions by a fully written finite construction and proof.

## 3. A compact 18-component certificate

Only the following twelve permutation columns are needed. Columns are
displayed as rows; their six entries refer to the six left components.

```text
01 02 10 12 20 21
10 12 20 21 01 02
20 21 01 02 10 12
10 01 20 02 21 12
01 10 02 20 12 21
20 02 21 10 12 01
21 20 10 01 02 12
01 21 12 20 02 10
02 10 01 12 21 20
20 12 01 10 21 02
12 10 20 01 02 21
01 10 12 02 20 21
```

The corresponding `K_(6,12)` construction has 18 K4s, 72 physical vertices,
72 component edges, 144 crossing scalar entries, and 108 protected entries.
Each displayed row is a permutation of `P`, so constant-left forcing is
automatic. Exact enumeration of all `3^6=729` left words verifies that for
each of the 726 nonconstant ones, at least one displayed column has
`B_pi(x)={0,1,2}`. This finite case cover is sufficient because right
components have no edges between them and can be conditioned separately
on the left word. No physical-word or arbitrary-order extrapolation is
being made from the 729 cases.

The [primary](verify_protected_low_minority_support_countermodel.py) and
[independent literal replay](audit_protected_low_minority_support_countermodel.py)
check this [finite certificate](../../tests/fixtures/protected_eighteen_component_macro_cover.json)
and its physical support bridge. The universal no-one-pair proof remains
section 1. The twelve-column cover is deletion-minimal (each column has
an exclusive covered left word), but no minimum-size claim is made.

## 4. Every fixed paired-minority cutoff: parent synthesis

The extension combines a deterministic physical matching lemma with a self-contained
probabilistic existence argument; the latter is not a numerical experiment.

For an integer `r>=1`, let **P_r** mean macro coverage together with no
uniquely supported mixed word satisfying `min_c q_c<=r`. Thus `P_1=P1`.
The proposed stronger route would exclude P_r for some universal fixed r.

**Fixed-cutoff countermodel theorem.** For every fixed integer `r>=1`
there is a finite simple one-label common-star protected support satisfying
P_r, with every whole `D_c` acyclic. Its component graph can have arbitrarily
large prescribed girth. The support depends on r; no single finite support
is claimed to satisfy every P_r simultaneously.

### 4.1 A non-macro term exposes a short component cycle

Fix one supported scalar perfect matching and a background `c`. Write
`q=sum_i q_i` for its paired-minority count, with `q_i` local to component i.
Call a component active when some physical vertex crosses.

At most q active components have `q_i>0`. By the local table in section 1,
every active `q_i=0` component crosses precisely its center and `L_c`, and
all its leaves have color c. Its crossed `L_c` must meet a non-c leaf at a
positive-q component. Different zero-q components use different such
physical leaves. Each positive-q component has at most two non-c leaves,
and hence at most `2q_i` such crossed leaves. Therefore

```text
number of active components <= q + 2q = 3q.                 (G1)
```

Project the crossing matching to a multigraph on its active components.
Every degree is two or four, and every component edge has multiplicity at
most two. If its underlying simple projection is a forest, the odd-
multiplicity edges form an even-degree subgraph of a forest and are empty.
Thus every used component edge is doubled. Each doubled edge uses its
gadget's center-center entry, so two doubled edges cannot meet at a
component. The projection is a matching. Each doubled gadget forces its
two endpoint components to be constant, and every inactive component is
internally constant. The physical word is consequently a macro word.

Contrapositively, any non-macro term has a simple component cycle on at
most `3q` vertices. Thus a component graph of girth greater than `3r` has
only macro words among its supported `q_c<=r` words. If it is macro-complete,
each mixed such word has its protected matching and an additional crossing
matching. This proves P_r. The whole-port layering from section 1 still
holds independently of girth.

### 4.2 High girth is compatible with complete macro coverage

We prove that for every fixed integer `g>=2`, a finite simple bipartite
component graph exists whose girth exceeds g and whose only gadget-avoiding
colorings are the three constants. For smaller requested g, use g=2.

Let X and Y each have N vertices. For each of the six ordered unequal
color labels `(a,b)`, independently choose eight uniform perfect matchings
from X to Y, all carrying label `(a,b)`. Keep the 48 layer identities even
when their edges coincide. This is initially a bipartite multigraph.

Every constant coloring avoids every layer. We first prove that with
probability tending to one these are the only avoiding colorings.
For a fixed nonconstant coloring, choose a most frequent color c over
both sides. Let s and t be the numbers of non-c vertices in X and Y, so
`s+t<=4N/3`, and put `x=s/N, y=t/N`. If exactly one of s,t is zero,
avoidance is impossible.

Otherwise, in a layer labeled `(a,c)`, all left vertices colored `a!=c`
must map into the t right non-c vertices. For m such left vertices the
exact probability is `binom(t,m)/binom(N,m)<=y^m` (zero if m>t).
Use all eight layers for each a. Independently, the layers `(c,b)`, b!=c,
must map every right b vertex back into the left non-c set. These four
families of layers are distinct. Ignoring the other two families yields

```text
Pr(this coloring avoids every edge) <= y^(8s) x^(8t).        (G2)
```

For fixed s,t and c, there are at most
`binom(N,s)2^s binom(N,t)2^t` colorings. Write H for binary entropy using
natural logarithms, and set

```text
C(x,y)=x log(1/y)+y log(1/x).
```

For positive x,y with x+y<=4/3,

```text
x log(1/x)+y log(1/y) <= C(x,y),
C(x,y) >= (x+y) log(2/(x+y)) >= (x+y) log(3/2),
H(x)+H(y)+(x+y)log 2 <= A C(x,y),
A=1+(1+log 2)/log(3/2).                                  (G3)
```

The first inequality has difference `(x-y)log(x/y)>=0`. For the second,
weighted Jensen gives `C/(x+y)>=log((x+y)/(2xy))`, and
`4xy<=(x+y)^2`. The third follows from `H(u)<=u log(e/u)` and the first
two. These inequalities include endpoints x=1 or y=1 by continuity.

Let `delta=8-A>2`. For example, the strict last inequality is equivalent
to `(3/2)^5>2e`, which follows from `243/32>6` and `e<3`. Combining the
entropy bound `binom(N,s)<=exp(N H(s/N))` with (G2)--(G3) bounds the expected
number of nonconstant avoiding colorings by

```text
3 sum_(S=2)^floor(4N/3) (S-1) exp[-delta S log(2N/S)].        (G4)
```

For S<=sqrt(N), the summands are bounded by
`3(S-1) N^(-delta S/2)`, a geometric tail tending to zero. For larger S,
the entire remainder is at most a constant times
`N^2 exp[-delta sqrt(N) log(3/2)]`, which also tends to zero. Hence the
probability of any nonconstant avoiding coloring tends to zero.

### 4.3 A positive fraction of layer outcomes have any fixed girth

Here is the needed short-cycle argument for this exact layer model.
It imports no random-graph theorem. Count each multigraph cycle with its
layer identities retained, modulo cyclic rotation and reversal; include
a length-two cycle for each unordered pair of parallel edges from distinct
layers. Different descriptions of the same cycle are not distinct cycles.

For a fixed cycle length `2l<=g`, there are finitely many patterns of
layer identities. Adjacent cycle edges must have different layers, since
each layer is a perfect matching. A compatible pattern with e_j distinct
specified pairs in layer j has probability exactly `1/(N)_(e_j)`, where
the denominator is a falling factorial. Counting injective choices of
the l left and l right vertices shows that the mean number of cycles of
each fixed pattern has a finite limit. More explicitly, proper layer
colorings of a cycle of length 2l number `47^(2l)+47` (the trace of
`(J_48-I_48)^(2l)`), and its unrooted
vertex embeddings number `(N)_l^2/(2l)`. Thus the mean number of cycles of
length 2l converges to

```text
lambda_l = (47^(2l)+47)/(2l).
```

For l=1 this is `binom(48,2)=1128`, including parallel layers that have
the same endpoint-color label. Hence
`Lambda=sum_(l=1)^floor(g/2) lambda_l` is explicit and finite.

Let Z be the total number of cycles of lengths at most g and let Lambda
be the sum of their finitely many limiting means. For every fixed integer
h, the factorial moment `E[(Z)_h]` counts ordered h-tuples of distinct
cycles. Vertex-disjoint cycles give the product of their limiting means:
the exact matching probabilities factor asymptotically, even when the
cycles share layer identities. An overlapping collection containing two
distinct cycles in one connected component has more distinct specified
edges than vertices. Its total contribution is `O(N^(v-e))=o(1)`.
Incompatible layer incidences contribute zero. Therefore

```text
E[(Z)_h] -> Lambda^h       for every fixed h.                (G5)
```

For any fixed J, inclusion-exclusion (the Bonferroni bounds) gives

```text
sum_(h=0)^(2J+1) (-1)^h E[(Z)_h]/h!
  <= Pr(Z=0) <= sum_(h=0)^(2J) (-1)^h E[(Z)_h]/h!.
```

First take N to infinity using (G5), then J to infinity. The two
exponential-series truncations converge to the same positive number:

```text
Pr(no cycle of length at most g) -> exp(-Lambda)>0.          (G6)
```

Because g>=2, this event removes every parallel edge pair and makes the
component graph simple with one label per edge. Its probability stays
positive, whereas the failure probability in section 4.2 tends to zero.
Thus for some finite N both high girth and complete macro coverage hold.
Every component has degree 48 on this simple outcome.

Taking g=3r and applying section 4.1 proves the fixed-cutoff theorem.
The existence proof does not provide a small graph or a least-N bound for
general r. It does not assert a useful relation between r and graph size.
The finite 18-component certificate remains a separate explicit witness
for r=1.

## 5. The weighted boundary is essential

Setting every crossing weight to one gives a concrete support realization.
Its mixed macro coefficients are positive integers, not the required zero.
In fact **no choice of nonzero complex weights on this support can satisfy
the macro target**, by the already proved
[triangle obstruction](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md).

For a gadget edge `uv` labeled `(a,b)`, let `c` be the third color. Let
`F_u,F_v,F_uv` be the full macro coefficients with exceptions respectively
`u:a`, `v:b`, or both, against background `c`. When `uv` has no common
neighbor, the actual shared source identity is

```text
A_uv B_uv = F_uv - F_u F_v.
```

All three target coefficients are zero, forcing a nonzero gadget product
to vanish. This accepted identity applies directly to our bipartite graph.
It does not follow merely by counting whether these words have multiple
terms. The common-star full-source exclusion also remains valid.

The sharper weighted parent **WP1** asks whether an arbitrary hollow
protected array can simultaneously satisfy the pure normalization, all
mixed macro zero equations, and all mixed `min_c q_c<=1` zero equations.
A full source supplies these equations. Excluding their conjunction would
prove SFULL, but is presently open. The support construction does not
refute WP1. Neither does a weighted macro control with a nonzero one-pair
coefficient. This is the load-bearing distinction for the next parent
attempt; no acyclic-port supply is assumed for WP1.

On the simple one-label common-star family, WP1 specializes to the existing
CSQ4 parent rather than a new subproblem. The root classification in
section 1, without triangle-freeness, leaves only an ABB triangle: a BB
root protected in color `c` and two outside AB components. Such a term has
the two non-`c` root leaves and one or two non-`c` outside centers, hence
exactly three or four physical minorities. All other mixed `q_c<=1` words
are unsupported. Conversely the
[exhaustive U4 classification](PROTECTED_SCAFFOLD_COMMON_STAR_RESOURCE_ALIGNMENT_NO_GO.md)
shows that every supported word within four physical minorities is either
a singleton macro row or one of these ABB triangles. Thus macro plus all
`min_c q_c<=1` equations is exactly macro plus U4 on this family. General
WP1 must address arbitrary protected fillings; renaming CSQ4 does not
advance it.

## 6. Exact weighted macro cancellation still does not suffice

A complementary literal control rules out the attempted strengthening
that whole-port acyclicity is already incompatible with weighted macro
targets. The
[rational fixture](../../tests/fixtures/protected_twelve_vertex_weighted_macro_dag_control.json)
has three protected K4s and 72 nonzero crossing entries over Q. With its
18 protected unit entries it satisfies all 27 macro equations exactly:
the three pure coefficients are one and the 24 mixed coefficients are zero.
Its three whole port graphs are DAGs, with respectively 33, 38, and 37 arcs.

This array is not a P1 support or a full source. The word
`1210|1111|1221` has `q_1=1`, with sole complete minority pair `{1,3}`,
and exactly one matching:

```text
(0,2), (1,11), (3,8), (4,6), (5,7), (9,10).
```

The two crossing entries are `(1,11)[2,1]` of weight one and
`(3,8)[0,1]` of weight minus one; the other four factors are protected
units. The coefficient is exactly `-1`. Thus actual non-macro equations
are load-bearing even after exact macro cancellation and whole acyclicity.

The [primary checker](verify_protected_weighted_macro_dag_control.py)
recurses on word-compatible edges using exact fractions. The
[independent audit](audit_protected_weighted_macro_dag_control.py) first
generates all 10,395 unlabelled perfect matchings on twelve vertices and
then evaluates each requested word. It imports none of the primary
scientific code. Both validate every literal and independently reconstruct
the transpose-linked port arcs. Their common macro term-count histogram is
`{1:3, 2:14, 3:6, 5:1, 9:1, 10:1, 11:1}`.

The fixture is the complete exact object; its historical source indices and
source-domain hash are provenance metadata, not an external dependency.
No numerical optimizer or discarded 78-entry support is needed to replay
the claim.

## Evidence boundaries

The [independent review](../../docs/audits/PROTECTED_LOW_MINORITY_PARENT_REVIEW_2026-09-22.md)
records the separate construction, probability, physical-matching, and
weighted-control audits. The analytic 726-component proof is independent of the finite cover search.
The 18-component reduction uses the stated finite certificate and exact
checkers. Neither relies on a numerical solver or an unchecked UNSAT claim.
Independent review means separately assigned agents and implementations in
the same session, not human refereeing. No Lean formalization is supplied.
UPM's unrestricted all-word no-singleton condition and SFULL are not
established or refuted by this package.

Portable replay commands, from the repository root:

```text
python claims/arbitrary-order/verify_protected_low_minority_support_countermodel.py
python claims/arbitrary-order/audit_protected_low_minority_support_countermodel.py
python claims/arbitrary-order/verify_protected_weighted_macro_dag_control.py
python claims/arbitrary-order/audit_protected_weighted_macro_dag_control.py
python claims/arbitrary-order/audit_common_star_paired_depth_local_states.py
```

The scripts have no third-party dependencies; they use the standard library
and the shared repository bootstrap. They also run by absolute path
from a neutral working directory. The primary support replay includes
literal one-pair witnesses after removing triangle-freeness or permitting
two labels on one component pair, checking both load-bearing hypotheses.
