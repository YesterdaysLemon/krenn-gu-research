# Degree-two source transport and the uniform-exterior boundary

Date: 2026-09-22.

Status: proved exact identities and an exact obstruction to a proposed local
proof mechanism, over C. Separate-agent reviews checked both implications
and the physical controls. No Lean formalization is supplied. The global
Krenn--Gu conjecture remains **UNRESOLVED**.

The parent is the full-source exclusion for every protected unit-K4 array
with at most two crossing entries per physical vertex/color state, at every
k>=2. Its downstream consumer is the degree-two branch of SFULL. This is
an explicit support-class hypothesis, not a normal form for arbitrary
witnesses. The attempted synthesis combines PSCG's sparse normalization,
PSMD's shared-resource exclusion, and PRDC's directed-cycle consumer.

This document, node PSDT, keeps every actual two- and four-crossing term.
Its transport theorem uses the stronger **color-regular** hypothesis: each
state has exactly one crossing to each foreign color. It forces a C8
four-crossing cancellation to have an opposite two-gadget repair. That
repair satisfies the entire same one-component/uniform-background slice. A
separate reciprocal control shows that even all three uniform-background
slices at one fixed component permit partial-resource orphans. When both
orphan targets lie in one exterior component, however, a coupled mixed row
forces a necessary paired resource through the third color. This does not
exclude the repaired same-component branch; separated orphan targets and the
general degree-two parent also remain open.

Throughout, crossings are hollow, join distinct protected components,
and carry their actual shared nonzero complex weights. Inside a component
the only entries are the unit protected matchings
M_0={01,23}, M_1={02,13}, M_2={03,12}. T_W denotes the literal physical
perfect-matching sum; all omitted scalar entries vanish.

## Exact singleton-cut formula

Fix a component `A`, a selected colour `a`, and a different exterior colour
`c`.  Give `A` colour `a` and every other component colour `c`.  Let `X` be
the actual crossing matrix from the four states `(u,a)`, `u in A`, to all
exterior states `(v,c)`.  Hollowness removes every exterior--exterior
crossing in this word.

Let `E_c` be the set of all protected `M_c` edges in the exterior
components.  For a protected edge `R` of `M_a(A)` and `P in E_c`, write
`X[R,P]` for the corresponding `2 x 2` submatrix.  A physical matching has
zero, two, or four cut crossings.  Exact deletion against the unique
protected matching outside gives

```text
0 = 1
    + sum_(R in M_a(A)) sum_(P in E_c) per X[R,P]
    + sum_({P,Q} subset E_c, P!=Q) per X[A,P union Q].       (1)
```

This includes the case where `P,Q` are the two protected `M_c` edges of one
exterior K4.  The last sum is over unordered two-element subsets of `E_c`,
so no four-crossing matching is double-counted.  Formula (1) has no
genericity or free-cofactor assumption.

To prove it, a two-crossing term must leave two vertices of `A` for one
protected `M_a` edge, so the crossed vertices form the complementary
`M_a` edge `R`.  In every exterior component the deleted endpoints must be
a union of whole edges of its unique protected `M_c` matching.  With two
crossings this is one edge `P`; with four crossings it is two distinct
edges `P,Q`.  Conversely every perfect matching counted by the displayed
permanents, together with the protected complements, is a physical matching
of the singleton word.

Under the degree-two state hypothesis the bipartite support of `X` has
maximum degree two, hence is a union of paths and even cycles.  This bounds
the internal combinatorics of each permanent but does **not** delete the last
line of (1).  In particular a four-crossing permanent can be the product of
two cycle/path factors even when every `2 x 2` protected-pair permanent in
the middle line vanishes.

## Color-regular degree-two dichotomy

There is a sharper exact normal form under the additional, explicitly
restricted hypothesis that every physical vertex/colour state has exactly
one crossing to each foreign colour.  For each unordered colour pair the
crossing support is then a perfect matching of the physical states.  Fix
`(A,a|c)` and let `t_ac` be the four matching edges leaving the `a` states
of `A`, with image vertex set `U`.

If `U` is not a union of two protected `M_c` edges, no four-crossing term is
available.  The singleton row contains the protected constant and whichever
of the two source `M_a` edges are mapped onto one protected `M_c` edge.

If `U=P union Q` for two protected `M_c` edges, put the source `M_a`
matching, the target edges `P,Q`, and the four `t_ac` edges on the same eight
states.  This is a 2-regular graph, hence exactly one of:

* two `C4` resources.  If their two crossing products are `x,y`, the exact
  singleton coefficient is

  ```text
  1+x+y+xy=(1+x)(1+y);                              (2)
  ```

  therefore a zero target forces `x=-1` or `y=-1`; or
* one `C8`.  No source `M_a` edge maps to a target `M_c` edge, so there is no
  two-crossing term.  If `z` is the product of all four crossing weights,

  ```text
  1+z=0, hence z=-1.                                (3)
  ```

This is the precise color-regular extension of the degree-one resource
picture.  The `C8` alternative is the genuinely new four-crossing branch.
The general degree-two parent also permits a `(2,0)` distribution of a
state's two crossings between foreign colours, so this dichotomy is not a
normal form for the declared parent.

## Exact C8-to-split transport, including spanning C8s

Fix distinct colours `a,b,c`.  Suppose the singleton `(A,a|c)` is cancelled
by a C8 four-crossing term.  Its four target vertices are the disjoint union
of two exterior protected `M_c` edges `P_0,P_1`; these may lie in the same
physical component or in two different components.  Pulling this target
pairing back through the colour-regular matching `t_ac` gives one of the
three perfect matchings on the ports of `A`; call it `N`.

The C8 condition says `N!=M_a`, since equality would give two C4 resources.
Also `N!=M_c`: if an `M_c(A)` edge mapped to an exterior `M_c` edge, putting
colour `a` on that source edge and colour `c` everywhere else would force its
two unique crossings and protected complements, giving a nonzero empty-q1
coefficient.  Therefore

```text
N=M_b.                                                   (4)
```

Thus each `M_b(A)` edge `R` maps bijectively to one of `P_0,P_1`.  Let `x_R`
be the nonzero product of its two `a--c` lane weights, and let `R'` be the
complementary `M_b(A)` edge.  Consider the actual physical word

```text
A_R=a,       A_R'=b,       every vertex outside A=c.      (5)
```

The two `a` states cannot use a protected edge, since `R` is an `M_b` edge,
and their only compatible exterior crossings are their unique `a--c` lanes.
They are therefore forced to consume the target resource `P=t_ac(R)` and
contribute `x_R`.  The `b` states on `R'` have exactly two possibilities:
use their protected `M_b` edge, or use both unique `b--c` lanes.  The latter
is a physical matching exactly when `t_bc(R')` is an `M_c` edge `Q` distinct
from `P`; if so, write `y_R'` for its two-lane product.  There are no further
sectors: same-colour exterior crossings vanish, and all unconsumed `M_c`
edges are forced.  Hence the exact full-array coefficient is

```text
T_W(5) = x_R                         if no such Q exists,
       = x_R (1+y_R')                otherwise.           (6)
```

The target of (5) is zero and `x_R!=0`.  Full-source consistency therefore
forces `Q` to exist, forces it to be distinct from `P`, and forces
`y_R'=-1`.  Applying this to both choices of `R` proves:

> **C8-to-split transport.** If `(A,a|c)` is a C8 singleton resource, then
> the opposite foreground layer `(A,b|c)` maps both `M_b(A)` edges onto
> exterior `M_c` resources, and both two-lane products equal `-1`.

In particular the opposite layer is exactly a `C4+C4` split and cannot also
be a C8.  The proof retains arbitrary nonzero complex weights and applies
unchanged when `P_0,P_1` lie in different components.  It is an implication
inside a putative full source, not a support normalization derived from
macro equations alone.

### Exact local completion and its boundary

The forced split repairs not only the two transport words but every word on
`A` against the same uniform exterior background.  Write the two `M_b(A)`
edges as `E_0,E_1`.  Put

```text
P_i=t_ac(E_i),     product(P_i)=x_i,     x_0 x_1=-1,
Q_i=t_bc(E_i),     product(Q_i)=y_i=-1.
```

The two applications of (6) also give

```text
Q_0 != P_1,                 Q_1 != P_0.                 (7)
```

If `Q_i=P_i`, full-source consistency forces the endpoint bijections on that
resource to be opposite.  Indeed, if they had the same alignment, colour one
endpoint of `E_i` by `b` and the other three vertices of `A` by `a`.  The
mixed `a--c` and `b--c` lanes on `E_i`, together with both `a--c` lanes on
`E_(1-i)`, give a unique all-four-crossing matching.  With opposite
alignment the two mixed lanes collide at one target endpoint, as required.

Under (7) and this overlap rule, the complete boundary tensor is

```text
T_W(word on A, c outside) = 1  if word on A is cccc,
                            0  for the other 80 words.   (8)
```

Here is a direct proof without treating (8) as a finite experiment.  A
`c`-coloured vertex of `A` has no compatible exterior crossing, so the set
of `c` vertices must be a union of `M_c(A)` edges.  If it is one such edge,
the other `M_c` edge meets `E_0,E_1` once each.  Equal remaining colours map
to two different `P` or `Q` resources; different remaining colours map to
`P_i,Q_(1-i)`, which are distinct by (7).  Hence no matching exists.  The
all-`c` word has its unique protected matching.

It remains to use only colours `a,b`.  A mixed-colour `E_i` cannot consume
an exterior resource: `P_i,Q_i` are distinct, or their opposite endpoint
maps collide.  If neither `E_i` is mixed, the possibilities are exhaustive:

* all `a`: protected weight `1` plus the C8 product `x_0x_1=-1`;
* all `b`: the factor `(1+y_0)(1+y_1)=0`; or
* `E_i` all `a` and `E_(1-i)` all `b`: the forced `a` lanes contribute
  `x_i(1+y_(1-i))=0`.

If one or both `E_i` are mixed, the preceding resource obstruction leaves no
boundary completion.  In particular the `b` endpoint of a mixed `E_i`
cannot use its protected `M_b` edge because its partner is the `a` endpoint.
This proves (8).

Thus every equation whose nonuniform part is confined to one component and
whose exterior is uniformly `c` is already satisfied by the repaired C8.
Any exclusion must couple at least two nonuniform components, or use a
different exterior background. The reciprocal control below strengthens
this boundary across both components and all backgrounds. This is an exact obstruction to extending
the local-isolation argument, not a full-source construction.

There is a smallest actual color-regular extension of this boundary tensor.
Take two components `A,B`, `(a,b,c)=(0,1,2)`, and port matchings represented
by xor with `1,2,3`.  On `A:0 -> B:2` use

```text
pi=(0,2,3,1),       weights=(1,1,1,-1).
```

On `A:1 -> B:2` use the endpoint-swapped map

```text
sigma=(3,1,0,2),    weights=(1,1,-1,-1).
```

Complete the unused halves of the `02` and `12` state-layer matchings, and
both halves of the `01` layer, by identity port maps of weight one.  This
gives 24 crossing scalar entries and exactly one crossing to each foreign
colour at every state.  It realizes (8) exactly but is not a full source:
the word `0000|0011` has coefficient `1`.

## Exact reciprocal all-background control

Reciprocity and all three one-component/uniform-background slices still do
not force every colour pair to split.  There is an exact two-component,
color-regular array realizing a repaired C8 in each background direction.
Identify the ports with `F_2^2` and use the common permutation

```text
P=(0,2,3,1),
```

whose action on protected matchings is the cycle
`M_0 -> M_1 -> M_2 -> M_0`.  For each target/background colour `e`, put a
C8 from source colour `e+1` through `P`, with port weights `(1,1,1,-1)`.
Put the forced split from source colour `e-1` through `P o m_(e-1)`, where
`m_d` swaps the endpoints of each `M_d` edge, and give each split pair
product `-1`.  These six directed descriptions agree on the three physical
undirected colour-pair matchings.  The resulting array has 24 crossing
entries, degree two at every state, and exactly one neighbour in each
foreign colour.

Exact physical-perfect-matching enumeration gives

```text
2 shores * 3 backgrounds * 81 local words: exact delta tensor
all 6 mixed component-constant words:       coefficient 0
full-source failures:                        195 words
failures with min_c q_c <= 1:                171 words
first q1 failure: 0001|0022, coefficient -1, unique matching
                  (01)(27)(36)(45), q=(1,3,2).
```

Thus even reciprocal consistency across all backgrounds leaves the q1 rows
strictly load-bearing.  This is a finite exact control, not a candidate full
source and not a proof that every repaired C8 extends globally.  The replay
is `verify_reciprocal_c8_boundary.py`.


## A q1 row excludes a same-component C8 repair

There is nevertheless an exact all-order implication behind the first q1
failure.  Suppose an `a--c` C8 sends all four ports of `A` to one component
`B`, and suppose its forced `b--c` split also sends both `M_b(A)` resources
to `B`.  Index the `M_b(A)` edges so the C8 maps `E_i` to the `M_c(B)` edge
`P_i`.  The transport inequalities `Q_0!=P_1`, `Q_1!=P_0` force the split
resource `Q_i` to equal `P_i`.  The local boundary equation then forces the
two endpoint bijections on each `E_i` to be opposite.

Write the C8 port map as `pi` and the split map as `sigma`.  On `F_2^2`, the
preceding endpoint statement is

```text
sigma = pi o m_b,                                      (9)
```

where `m_b` translates by the vector defining `M_b`.  Empty-q1 in both
directions and the C8 condition determine the matching action of `pi`:

```text
M_a -> M_b,       M_b -> M_c,       M_c -> M_a.        (10)
```

Choose an oriented `M_a(A)` edge `(u,v)`, so `u+v=a`, and put

```text
x=pi(u),                 y=sigma(v)=pi(v+b).
```

Equations (9)--(10) give `x+y=a`, so `(x,y)` is an `M_a(B)` edge.  Consider
the physical word

```text
u:a,       v:b,       x:c, y:c,       every other vertex:a.    (11)
```

It has `q_a=1`.  The state `u` cannot protect with `v`, cannot cross to the
only `b` state because it lies in the same physical component, and has only
one `a--c` neighbour; hence `u--x` is forced.  The remaining direct lane
`v--y` gives a nonzero physical matching, with the complementary `M_a`
edges protected.

There is no second sector.  If `v` uses its unique `b--a` lane, then `y`
must use its unique `c--a` lane.  By (9), the latter endpoint is

```text
pi^(-1)(y)=v+b,
```

one endpoint of the complementary `M_a(A)` edge.  Its `M_a` mate is then
the sole unmatched port of `A`: the `b--a` endpoint lies outside `A` by
hollowness, and every other vertex has colour `a`, so that port has no
compatible crossing.  Thus this putative repair cannot extend to a perfect
matching.  The direct term is unique and nonzero, contradicting the q1
source equation.

Consequently, if a one-component C8 `A -> B` occurs in a color-regular full
source, at least one of the two resources in its forced opposite split must
leave `B`.  This does not exclude a spanning C8 or a split whose resources
are separated among exterior components; those are the remaining global
propagation branch.

### Why escape does not automatically iterate

The escaping object is a paired C4 resource, not another C8.  If an
`M_b(A)` edge is paired to an `M_c(C)` edge with product `-1`, then in the
reverse singleton `(C,c|b)` its protected term and that two-lane term already
cancel.  The singleton row therefore supplies no new C8 on the complementary
`M_c(C)` edge.

This is realized literally in the independently checked three-component
extension of the local boundary tensor: the `a--c` C8 from `A` lands in
`B`, both forced `b--c` split resources land in a distinct component `C`,
and the reverse singleton at `C` has the exact four-term factor

```text
(1-1)(1-1)=0.
```

That array fails other source rows, so it is only a sharp control on the
proposed iteration.  Finiteness of the component graph cannot by itself
turn escape into a directed C8 cycle.  A genuine propagation proof must use
a mixed row to force the complementary resource or establish the two-exit
closure required by the existing transition-closed resource consumer.


## Exact macro-row countercontrol

Take two protected K4 components `A,B`.  For every ordered unequal colour
pair `(a,b)`, add exactly the four crossing entries

```text
(A_i,a)--(B_i,b),       i=0,1,2,3,                        (M1)
```

with weights `(1,1,1,-1)` in physical-port order.  Add no other crossings.
Every physical vertex/colour state has exactly two supported crossings: its
same-port neighbour in each of the other two colours.  The array is hollow.

For the component word `A=a,B=b` with `a!=b`, the protected term has weight
one and all four entries in (M1) give one four-crossing matching of weight
`-1`.  There is no two-crossing term.  Indeed the identity port map sends an
`M_a` edge of `A` to the same physical pair in `B`, which is an `M_a` edge,
not an `M_b` edge.  It therefore cannot leave a protected `M_b` complement.
Thus every mixed component-constant coefficient is

```text
1 + (-1) = 0.                                          (M2)
```

The three pure coefficients are one.  For `k=2` these are every singleton
and every two-exception component-constant row.  Hence those rows, even with
the degree-two state bound, do not force any two-entry pair gadget or any
nonzero `2 x 2` protected-pair permanent.

The control fails the full source for an equally local reason.  The word

```text
A = 0000,       B = 0011                              (M3)
```

has the unique matching

```text
A_0--A_1 protected in colour 0,
A_2--B_2 and A_3--B_3 crossing with labels [0,1],
B_0--B_1 protected in colour 0.
```

Its coefficient is `-1`.  No other crossing label is compatible with (M3).
Thus the four-crossing mechanism itself exposes a mixed partial-lane word in
this control; what is missing in the general parent is a proof that the
other degree-two support paths cannot repair every such partial word.

## A macro-invisible entry still matters to the full source

The four-crossing control above is color-regular. A separate degree-two
control shows a different obstruction to macro-only support normalization.
On two K4s A={0,1,2,3}, B={4,5,6,7}, add for every a!=b

```text
W_04[a,b]=1,       W_(a+1,b+5)[a,b]=-1,
```

and add W_25[0,1]=2. There are 13 crossing entries and maximum state crossing
degree two. Each mixed macro has protected term 1 and its displayed pair
term -1. The extra entry could only occur on 0000|1111: pairing it with
0-4 leaves an incompatible protected complement, pairing it with 1-6 does
likewise, and only three compatible crossings exist, precluding a four-cut
term. Cut parity rules out all other possibilities. Thus all nine macro
targets hold and the extra entry occurs in no macro matching.

It is nevertheless source-live. The word 0101|1100 has exactly the matching
0-4, 1-3, 2-5, 6-7, with product 2. Thus deleting this entry changes a
physical source coefficient. This refutes macro equations plus degree two
implying minimum density; it is not a full source or a refutation of SFULL.

## A partial-resource branch survives the complete local tensor

The color-regular degree-two parent still contains a singleton branch in
which one source protected pair maps to one background protected resource
with lane product `-1`, while the other two source endpoints land at targets
that do not form a resource.  The proposed local implication was:

> the full mixed-foreground tensor on that one component against a uniform
> exterior forces the orphan targets to form the complementary resource.

This implication is false.  The actual three-component array below satisfies
all 81 equations in that tensor and has the partial-pair/orphan branch for
both foreground colors.  It fails other source rows, so it does not refute a
global full-source implication.  It proves that any such global implication
must use another nonuniform component or another exterior background.

### Literal array

Use components `A,B,C`, each with ports `0,1,2,3`, and protected matchings

```text
M_0={01,23},   M_1={02,13},   M_2={03,12}.
```

Fix exterior color `c=2`.  From the color-0 states of `A`, use

```text
port in A       0    1    2    3
target          B0   B3   B1   C0
weight          1   -1    1    1.                    (O1)
```

Thus the `M_0(A)` edge `01` maps to the `M_2(B)` resource `B0B3` with
product `-1`, while the complementary endpoints `2,3` map to `B1,C0`, in
different components.

From the color-1 states of `A`, use

```text
port in A       0    1    2    3
target          B1   B0   B2   C0
weight          1    1   -1    1.                    (O2)
```

Here the `M_1(A)` edge `02` maps to the `M_2(B)` resource `B1B2` with
product `-1`, while `1,3` map to `B0,C0`.

Both rows extend to honest global state-layer bijections.  In physical
vertex indices `A=0..3`, `B=4..7`, `C=8..11`, take

```text
t_02=(4,7,5,8,  9,10,11,0,  1,2,3,6),
t_12=(5,4,6,8,  9,10,11,0,  1,2,3,7),
t_01=(4,5,6,7,  8,9,10,11,  0,1,2,3).
```

Give the first four `t_02` weights `(1,-1,1,1)`, the first four `t_12`
weights `(1,1,-1,1)`, and every completion weight one.  Every crossing joins
different components.  Each physical vertex/color state has exactly one
neighbor of each foreign color, hence crossing degree exactly two.

### Exact 81-row proof

Give `B,C` color 2 and let the word on `A` be arbitrary.  A physical matching
can cross the cut of `A` zero, two, or four times.

* With zero crossings, the four selected states of `A` have a protected
  perfect matching only for the three uniform words `0000`, `1111`, `2222`.
  This follows directly from the one-factorization of `K4`: two disjoint
  protected edges belong to the same `M_d`.
* With two crossings, the exterior targets must form an `M_2` resource and
  the two vertices left in `A` must form a protected edge.  Inspection of
  (O1)--(O2) gives exactly two possible target-resource pairs:

  ```text
  (A0,0),(A1,0) -> B0,B3;
  (A0,1),(A2,1) -> B1,B2.
  ```

  Their complementary source pairs can protect only in the uniform words
  `0000` and `1111`, respectively.
* With four crossings, choose at each port either its row-(O1) or row-(O2)
  target.  No choice gives four distinct endpoints that are a union of two
  exterior `M_2` resources.  Indeed port 3 always targets `C0`, whose
  `M_2(C)` mate `C3` appears nowhere in (O1)--(O2).  Hence no four-crossing
  sector exists.

Therefore the only supported local rows and term weights are

```text
0000 : (1,-1),
1111 : (1,-1),
2222 : (1).
```

They are exactly the required delta tensor.  Every mixed local word has no
supported matching at all.  The two orphan weights are immaterial to these
81 equations as long as they remain nonzero.

### Evidence boundary and consequence

`verify_partial_resource_boundary.py` reconstructs the full
three-component array, verifies the color-regular degree ledger, and
enumerates physical perfect matchings for all 81 rows.  It also displays the
global failure `0000|1111|2222`, whose coefficient is `3`; the control is not
a macro source or full source.

Thus the color-regular cover cannot be reduced locally to “complete split or
C8.”  The still-load-bearing statement must couple this orphan half to a
second nonuniform component/background, or prove from another source row
that the orphan endpoints acquire a resource partner.  Singleton and the
entire same-component/uniform-background tensor do not supply that step.

## Reciprocity and all backgrounds still permit partial resources

The preceding obstruction survives both reciprocity and every uniform
background at one fixed component. There is a four-component hollow
color-regular array in which all six ordered foreground/background incidences
at component `A` have exactly one product-`-1` source resource and two orphan
targets, while all

```text
3 backgrounds * 3^4 local words = 243
```

one-component equations at `A` hold.

Use physical vertices `A=0..3`, `B=4..7`, `C=8..11`, `D=12..15`. For each
increasing color pair, take the displayed global state-layer bijection

```text
t_01=(7,5,8,4,  0,2,3,12,  1,13,14,15,  6,9,10,11),
t_02=(4,7,5,8,  2,12,0,3,  1,13,14,15,  6,9,10,11),
t_12=(5,4,6,8,  0,12,3,1,  2,13,14,15,  7,9,10,11).     (O3)
```

The tuple index is the lower-color source vertex and its value is the
higher-color target. Each map is a permutation and every entry changes
component, so the reverse shore is the actual inverse of the same physical
layer. Give every crossing weight one except

```text
(1,5)[0,1], (5,2)[0,1],
(1,7)[0,2], (7,3)[0,2],
(2,6)[1,2], (6,3)[1,2],                              (O4)
```

which have weight `-1`. Every state has one crossing to each foreign color.

Fix background `c`, put `d=c+1`, `e=c+2` modulo three, and apply the unique
linear port relabeling sending `M_d,M_e,M_c` to `M_0,M_1,M_2`. The actual
forward or inverse layer leaving `A` becomes

```text
d -> c : (B0,B3,B1,C0),
e -> c : (B1,B0,B2,C0).                              (O5)
```

In each row exactly one source protected edge maps to one background resource
with lane product `-1`; the complementary endpoints land in `B` and `C` and
therefore do not form a resource. This proves all six incidence claims from
the same reciprocal array.

For a word arbitrary on `A` and uniformly `c` outside, zero cut crossings
support only the three uniform local words. With two cut crossings, (O5) has
exactly the displayed resource pair for uniform foreground `d` and the
displayed pair for uniform foreground `e`; mixed choices do not form another
`M_c` resource. Four cut crossings cannot complete because canonical port 3
always targets `C0`, while its `M_2(C)` mate `C3` is absent. Hence the only
term weights are

```text
cccc : (1),       dddd : (1,-1),       eeee : (1,-1),
```

and every mixed local word has no term. This proves all 243 equations. The
outside word `0000|1200|0000|0000` has one matching of coefficient `1`, so
the array is not a full source. This word is nonmacro, so it does not establish
macro failure; no macro-source claim is made. The array is an exact
obstruction to closing the partial-resource branch with reciprocal
one-component data alone.

## Coupled transport for same-component orphan targets

There is nevertheless an all-order implication once the two orphan targets
meet in one component. Let `a,b,c` be distinct colors. Suppose one `M_a(A)`
edge supplies a product-`-1` `a--c` resource cancellation and the
complementary `M_a(A)` edge `R={r,s}` has orphan targets
`y=t_ac(r), z=t_ac(s)` in one component `B`.

The layer bijection makes `y,z` distinct. The orphan hypothesis excludes an
`M_c(B)` edge. If they formed an `M_a(B)` edge, color `y,z` by `c` and every
other physical vertex by `a`. The `c` states cannot protect, have no
compatible `c--b` lane, and are forced through their `c--a` lanes to `r,s`.
All remaining vertices use their unique protected `M_a` edges. This gives one
nonzero matching and a forbidden `q_a=1` coefficient. Therefore `y,z` form
an `M_b(B)` edge.

Let `L={l_0,l_1}` be the complementary `M_b(B)` edge and use the word

```text
A uniformly a;   y,z:c;   l_0,l_1:b;   every other vertex:a.  (O6)
```

The `c` states cannot protect: their `M_c` mates lie on `L` and have color
`b`. Their only word-`b` vertices lie in their own component, where crossings
are hollow. Thus their `c--a` lanes to `r,s` are forced; write their nonzero
product as `h`.

The two `b` states on `L` either use their protected `M_b` edge or both use
their unique `b--a` lanes. A one-exit sector cannot complete. In the two-exit
sector every remaining vertex has color `a`, so the two targets must be one
protected `M_a` resource `Q`. The `b--a` layer is a bijection, hence the
targets are distinct. The choice `Q=R` collides with the forced orphan lanes;
all malformed or partially overlapping target pairs strand a vertex.
Conversely, any `M_a` resource `Q!=R` gives exactly one additional matching.
If the two exit weights have product `g`, the exact coefficient is

```text
h                    if no such Q exists,
h(1+g)               if Q exists.                         (O7)
```

Word (O6) is mixed, so its target is zero. Since `h!=0`, full-source
consistency forces `Q` to exist and `g=-1`. Untouched all-`a` components use
their protected matching, so the proof applies at every `k>=2` with arbitrary
nonzero complex crossing weights. This is a coupled source implication, not
a block normal form. If `y,z` lie in different components, there is no
complementary edge `L`; that separated-target branch remains open.

## Parent checkpoint and proof-topology delta

The all-order transport theorem is a new necessary source implication;
the full local tensor calculation is a no-go for extending that implication
to a contradiction using only the same slice. Its actual k=2 and k=3
extensions keep all scalar entries in one color-regular array. They have
explicit failures elsewhere. No arbitrary cofactor, numerical fit,
protected support degeneration, or cancellation chosen separately for
different words is substituted.

The macro controls prevent dropping the four-crossing sector or deleting
entries just because macros do not see them. A next load-bearing supplier
must couple repaired C8s across nonuniform components or use a global
resource identity. The q1 escape theorem forces at least one split resource
away from a one-component C8 target, but its reverse singleton may already
cancel and does not force another C8. The reciprocal C8 control satisfies all
one-component slices across all backgrounds. The reciprocal partial-resource
control satisfies the three fixed-`A` slices while retaining separated
orphans. The coupled theorem forces a paired third-color repair when the
orphans share a component, but does not exclude that repaired branch or give
a block normal form. Separated-target propagation remains an additional open
branch. Crossing degree two alone also permits a `(2,0)` distribution between
foreign colors; that branch is outside the color-regular transport theorem.

On the consumer side,
[PRDC](PAIRED_RESOURCE_DIRECTED_CYCLE_EXCLUSION.md) excludes complete paired
resources. The broader
[transition-closed resource theorem](RESOURCE_SIMPLE_TRANSITION_CLOSED_EXCLUSION.md)
allows triple blocks but requires explicit two-exit closure. Neither
resource partition nor that closure has been derived from general full
source equations. The two directions are recorded as a conditional
consumer and a source-transport reduction, not as an exhaustive cover.

The `k=1` protected K4 is the valid sharp full-source exception. The source
parent here quantifies `k>=2`. The reciprocal `k=2` C8 control satisfies all
one-component slices on both components in every uniform exterior background:
486 specifications, 477 distinct physical words. The reciprocal `k=4`
partial-resource control satisfies 243 fixed-`A` specifications. Both fail
the full source. Thus even reciprocal all-background local tests do not
supply the missing global edge.

## Evidence and review

The written formulas and matching-sector arguments prove the stated
unbounded implications. The companions are finite exact corroboration:

```text
python claims/arbitrary-order/verify_degree_two_four_cross_macro.py
python claims/arbitrary-order/verify_c8_split_local_boundary.py
python claims/arbitrary-order/audit_c8_to_split_transport.py
python claims/arbitrary-order/audit_c8_symbolic_boundary.py
python claims/arbitrary-order/audit_c8_global_boundary_extension.py
python claims/arbitrary-order/audit_degree_two_macro_excess.py
python claims/arbitrary-order/verify_reciprocal_c8_boundary.py
python claims/arbitrary-order/audit_reciprocal_c8_boundary.py
python claims/arbitrary-order/verify_c8_q1_escape_ports.py
python claims/arbitrary-order/audit_c8_q1_escape.py
python claims/arbitrary-order/verify_partial_resource_boundary.py
python claims/arbitrary-order/audit_partial_resource_boundary.py
python claims/arbitrary-order/verify_partial_orphan_reciprocal_boundary.py
python claims/arbitrary-order/audit_partial_orphan_reciprocal_boundary.py
python claims/arbitrary-order/verify_partial_orphan_coupled_transport.py
python claims/arbitrary-order/audit_partial_orphan_coupled_transport.py
```

The transport audit checks 6,720 collision cases plus the empty-q1 gate.
The primary k=2 boundary control enumerates all 6,561 physical words and
records 600 failures outside its 81-word slice. An independent Laurent
polynomial audit checks the tensor identity for arbitrary x_0=t,
x_1=-t^-1; a separate k=3 whole-array extension covers disjoint exterior
resources. The reciprocal orphan scripts verify 48 hollow crossing entries,
all six ordered incidences and all 243 fixed-component rows. The coupled
transport scripts enumerate every normalized exit placement at `k=2,3,4`;
the written matching-sector proof supplies the arbitrary-`k` quantifier.
These independent derivations import neither the primary implementation nor
project scientific code. All scripts use the Python standard library. The
finite controls are not a finite cover of all degree-two sources.

See the [independent review](../../docs/audits/DEGREE_TWO_SOURCE_TRANSPORT_REVIEW_2026-09-22.md)
and [model-review brief](../../docs/strategy/degree-two-source-parent-review-2026-09-22.md).
No external theorem, formal kernel check or human-referee claim is used.
