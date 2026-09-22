# Resource-simple transition closure and the mixed-cycle obstruction

Date: 2026-09-22

Status: proved all-order sufficient construction-family exclusion, strictly
extending paired resource blocks to resource-simple triple blocks.  An exact
four-vertex control shows that endpoint supply and degree two do not imply
the load-bearing local closure.  No reduction of arbitrary degree-two
sources to this family is claimed. This is node RSTC, a conditional consumer
for the degree-two SFULL parent. The global conjecture is **UNRESOLVED**.
The proof has a separate-agent audit and no external theorem or Lean
formalization.

## 1. Resource-simple block setting

Let nonempty `V` carry three colored protected perfect matchings `M_0,M_1,M_2`, with
arbitrary nonzero protected weights.  Partition their colored resources
into finite blocks.  Assume:

1. every block contains at most one resource of each color, hence has size
   at most three;
2. every crossing joins endpoint states of two distinct resources in one
   block, and no crossing is a physical self-loop;
3. every state endpoint has at least one supported crossing neighbor in its
   block; and
4. all supported scalar weights are nonzero.

There are no scalar entries other than the protected matching edges and
the stated within-block crossings. A scalar entry is specified by its
physical endpoints and their colors, with the usual transpose convention.
A physical word selects one colored state per vertex; its coefficient is
the sum of actual products over physical perfect matchings.

Resources may overlap physically.  The blocks partition colored
states, not necessarily physical vertices.

Fix a color `a` and an `a`-resource `e={u,bar(u)}` in a block.  Removing the
selected state `(u,a)` from the constant-`a` word can be repaired locally by
a crossing from `(bar(u),a)` to a foreign state `(v,b)`.  Call this the
transition `u -> (v,b)`.

## 2. Transition closure

A resource-simple block is **transition closed** when the following holds
for every one of its resources and every choice of two transitions from
its opposite endpoints:

```text
u      -> (v,b)  via (bar(u),a)--(v,b),
bar(u) -> (w,c)  via (u,a)--(w,c),
```

if `v!=w`, then the two target states `(v,b),(w,c)` are joined by a supported
scalar edge.

For resource-simple blocks this is the exact local condition needed when
both endpoints of a protected resource lie on the directed change cycle.
The selected block then contains only the two target states, so adjacency is
both necessary and sufficient for a local perfect matching.  When zero or
one endpoint changes, the protected edge or the defining crossing already
gives the unique local matching.

## 3. Theorem

**Theorem.** If every block is transition closed under the assumptions of
Section 1, the support has a mixed physical word with exactly one supported
perfect matching.  It therefore cannot realize a full source with vanishing
mixed coefficients.

### Labeled transition digraphs

For each base color `a`, form a labeled directed multigraph `D_a` on `V`.
For every crossing

```text
(bar(u),a)--(v,b)
```

put an arc `u->v` labeled `b`.  Endpoint supply gives every vertex positive
outdegree.  Choose a simple directed cycle and one available label on every
cycle arc.  Change the target vertex of each arc from color `a` to that
label.

Here is the exact block-balance step.  Every selected foreign state `(v,b)`
has a unique incoming predecessor `x` on the simple cycle.  Its defining
crossing uses the state `(bar(x),a)`, so the within-block support assumption
puts `(v,b)` in the block containing the `a`-resource of `x`.  Conversely,
every cycle endpoint of an `a`-resource creates one such foreign arrival in
that resource's block.  Successor injectivity on the simple cycle makes the
arrivals distinct.  Thus a block with `r` cycle endpoints has exactly `r`
foreign arrivals, and a block with no `a`-resource has none.

Because a block has at most one `a`-resource, it therefore selects exactly
two states:

* its protected `a` pair if the cycle contains neither endpoint;
* the remaining `a` state and the outgoing foreign target if it contains
  one endpoint; or
* the two outgoing foreign targets if it contains both endpoints.

The first pair has its protected edge, the second its defining crossing,
and the third its transition-closure edge.  In each case there is exactly
one scalar edge between the selected states.  Blocks omitting color `a`
select no state.  Thus every labeled cycle word has exactly one supported
global matching.

It remains only to ensure that some cycle word is mixed.  If a cycle is
proper, outside vertices retain color `a` while its vertices change away
from `a`.  If a spanning cycle uses both foreign labels, its word is also
mixed.

Suppose color `a` supplies neither possibility.  Fix a spanning cycle with
successor permutation `P_a`.  Every other outgoing arc `u->v` must have
`v=P_a(u)`: otherwise that arc followed by the appropriate segment of the
spanning cycle gives a proper directed cycle.  All labels on these successor
arcs must be one common foreign color `b`, since changing one label on the
spanning cycle would otherwise give a mixed word.  Call this the
**exceptional transition** `a=>b`.

Exceptional transitions are symmetric.  If `a=>b`, then for every `u` the
crossing

```text
(bar_a(u),a)--(P_a(u),b)
```

also gives in `D_b` the reverse-color transition

```text
bar_b(P_a(u)) -> bar_a(u)
```

labeled `a`.  Both mate maps and `P_a` are permutations, so every vertex of
`D_b` has an outgoing arc labeled `a`.  If `b` is exceptional, its one common
target label must therefore be `a`; that is, `b=>a`.

All three colors cannot be exceptional: a fixed-point-free symmetric map on
three elements would have to pair all three elements.  Hence at least one
color has a proper cycle or a spanning cycle with two labels.  Its cycle
word is mixed and has the unique matching already proved.

## 4. Sharp failure without transition closure

Endpoint supply, resource simplicity, and state crossing degree one do not
imply transition closure.

On physical vertices `0,1,2,3`, take

```text
M_0 = {01,23},
M_1 = M_2 = {02,13}.
```

Use two triple-resource blocks

```text
B_1 = { 01 of color 0, 02 of color 1, 13 of color 2 },
B_2 = { 23 of color 0, 13 of color 1, 02 of color 2 }.
```

Support the six crossings

```text
B_1: (1,0)--(2,1),  (0,0)--(3,2),  (0,1)--(1,2),
B_2: (3,0)--(1,1),  (2,0)--(0,2),  (3,1)--(2,2).
```

Every colored state has crossing degree exactly one, every block contains
one resource of each color, and no crossing is a physical self-loop.

For base color zero the transition digraph is the single Hamiltonian cycle

```text
0 -> 2 -> 1 -> 3 -> 0.
```

Its labels give the mixed word

```text
(2,1,1,2).
```

In `B_1` the selected targets are `(2,1),(3,2)`, and in `B_2` they are
`(1,1),(0,2)`.  Neither pair is adjacent.  The word has no supported
matching.  Thus the pair-block balance argument cannot be extended to
triple blocks using endpoint supply or degree alone.  The missing two-exit
closure is genuinely load-bearing.

This control is a mechanism counterexample, not a full-source or macro
solution.  Existing macro controls with four-crossing cancellation and a
macro-invisible source-live orphan separately show that macro equations do
not already supply a complete resource-block normal form.  Whether all
nonmacro source rows force transition closure or an alternative unique word
remains open.

## 5. Replay

`audit_resource_triple_closure_obstruction.py` reconstructs the literal control,
checks the resource partition and degree ledger, derives the labeled
Hamiltonian cycle, and enumerates all physical perfect matchings of its word.


## 6. Consumers, evidence and remaining supply

Every paired block of [PRDC](PAIRED_RESOURCE_DIRECTED_CYCLE_EXCLUSION.md)
satisfies transition closure: distinct foreign targets belong to its one
foreign resource and have its protected edge. Endpoint supply follows from
the crossing perfect matching. Thus the present proof extends that family
and supplies a second, odd-color symmetry proof of mixedness.

Triple blocks with state graph K3,3 also satisfy closure. Give each of the
three resources endpoints 0,1, use diagonal a-b and a-c crossing bijections
and the anti-diagonal b-c bijection. Every state has crossing degree two;
opposite-endpoint exits have their targets joined. Hence triple blocks are
a genuine extension in the degree-two class. The theorem itself needs no
crossing-degree upper bound.

The exact obstruction in Section 4 concerns failure of this universal
cycle-balance mechanism; it does not prove that its array lacks some other
unique mixed word. Nor does it refute the full-source exclusion for all
resource-simple blocks. The missing supplier is a full-source reduction
to suitable blocks and two-exit closure, or a weaker existential cycle
selection condition. Sections 7--8 show that endpoint supply alone cannot
provide even that existential cycle condition. Repeated-color resource cycles remain outside the
resource-simple block hypothesis.

The proof is Sections 1--3. The portable negative replay checks the
displayed obstruction; it is not an all-order proof. The
[independent audit](../../docs/audits/RESOURCE_SIMPLE_TRANSITION_REVIEW_2026-09-22.md)
rederives the arrival converse, all-arc exceptional argument and reverse
transition symmetry. No independent human refereeing is claimed.

The positive companion independently reconstructs actual three-K4
all-triple and hybrid pair/triple arrays. It checks endpoint degrees,
resource partition, and every two-exit closure condition before counting
physical perfect matchings of the constructed words. It includes a word
using the r=2 closure case in three blocks, and a two-vertex overlap
control. A triangular-prism mutation fails six closure conditions. These
are explicit exact controls, not a finite cover over arbitrary orders.

```text
python claims/arbitrary-order/verify_transition_closed_resource_blocks.py
python claims/arbitrary-order/audit_resource_triple_closure_obstruction.py
```

The coupled source-side attempt and its exact boundary obstruction are
recorded in [PSDT](DEGREE_TWO_SOURCE_TRANSPORT_AND_LOCAL_BOUNDARY.md).
See also the [parent review brief](../../docs/strategy/degree-two-source-parent-review-2026-09-22.md).


## 7. Exact cyclewise criterion

Use the resource-simple block setting and transition digraphs of
`RESOURCE_SIMPLE_TRANSITION_CLOSED_EXCLUSION`.  Fix a base color `a`, a
simple directed cycle `C` in `D_a`, and one crossing label on each arc.
Color each cycle target by its arc label and every other physical vertex by
`a`.

The block-balance argument gives exactly two selected states in every active
block.  If `C` meets a protected `M_a` resource in zero or one endpoint,
those two states have respectively the protected edge or the defining
crossing.  If it meets both endpoints, the two states are the two foreign
exit targets.  Therefore:

> **Cyclewise criterion.** The cycle word has exactly one supported perfect
> matching if and only if every double-hit resource on `C` has adjacent exit
> target states.

The word is mixed whenever `C` is proper, or when a spanning `C` uses two
foreign labels.  Thus a single mixed cycle satisfying the criterion excludes
a full source.  Pointwise transition closure is a convenient all-cycles
supplier, not a necessary hypothesis for exclusion.

Equivalently, any support escaping this entire directed-cycle mechanism must
obey the **bad-exit hitting condition**:

```text
every mixed labeled simple D_a cycle contains a double-hit M_a resource
whose two exit targets are nonadjacent.
```

In particular it has no `M_a`-independent directed cycle.  This is the exact
closure-free existential obligation.


## 8. Exact `k=3` obstruction to existential cycle selection

The fixture `resource_triple_bad_exit_control.json` uses three ordinary protected
K4 components.  It partitions the eighteen colored protected resources into
six resource-simple triple blocks.  Within each block the crossing support
is a three-edge matching with one edge between each pair of resource colors.
Consequently:

* every one of the 36 physical vertex/color states has crossing degree one;
* all crossings join different physical K4 components, so the support is
  hollow as well as free of physical self-loops;
* each `D_a` is functional; and
* in a degree-one triple block, opposite exits of one resource land at the
  two foreign endpoints not used by the third crossing.  They are therefore
  nonadjacent.  A cycle is good exactly when it is `M_a`-independent.

The three functional cycle ledgers are

```text
a=0: (5,11,2,10)
a=1: (8,6,9,4,2)
a=2: (9,3,5,10,4).
```

Every cycle contains both endpoints of a protected `M_a` resource.  The
checker constructs each associated word and separately counts zero
compatible physical perfect matchings.  Thus endpoint supply, resource
simplicity, hollowness, and even crossing degree one do not supply one good
directed cycle.

This does not refute support exclusion.  Full term enumeration gives 364
supported terms on 342 words, including 317 uniquely supported mixed words;
the first displayed witness is `000000001111`.  The fixture therefore fails
UPM and macro supply very strongly.  Its exact role is to rule out a proof
that selects only one constant-background transition cycle.

The fixture has only triple blocks, so the binary macro word
`000000001111` is also the promised all-triple witness from the factorization below.



## 9. Why the control does not satisfy macro supply

At crossing degree exactly one, each pair block has an alternating C4
and each triple block an alternating C6. A component-constant physical
word selects either both states or neither state of each resource. A
proper subset of a block's resources has just its protected matching;
a fully selected block has its protected and crossing matchings. Hence

```text
T_W(phi)=P(phi) product_(fully selected blocks B) (1+sigma_B),
```

where P(phi) is the nonzero protected product and sigma_B is the ratio
of the crossing product to the protected product in B. In the all-triple
fixture, any mixed binary macro leaves one color absent, so no block is
fully selected. Its protected matching is unique. Thus the fixture only
refutes selection of one good constant-background cycle from endpoint
supply; it does not refute any full-source exclusion.

There is also an alternative sparse supplier for mixed pairs and triples.
If t counts triple blocks and s_ab counts pair blocks of colors a,b,
resource counting gives s_01=s_02=s_12=s and 2s+t=2k. Binary macro
no-uniqueness requires the s arcs from the a-resource's component to the
b-resource's component to cross every nontrivial directed cut. The
component digraph is therefore strongly connected, so s>=k. It follows
that s=k and t=0; all blocks are pairs and PRDC applies. This is an
alternative derivation inside the degree-one branch already subsumed by
[PSCG](PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md) and
[PSMD](PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md), not a new
degree-two exclusion.

The literal fixture is durable exact control data. Replays:

```text
python claims/arbitrary-order/verify_resource_triple_bad_exit.py
python claims/arbitrary-order/audit_resource_triple_bad_exit.py
```

Both reconstruct all state and block incidence, all functional cycles,
and every compatible term. The independent implementation imports neither
the primary checker nor project scientific code. The missing parent
supplier must use macro/mixed-row consistency, or an exchange across
cycles, rather than endpoint supply alone.


## 10. The degree-two prism supplier boundary

### Local setting

Take one resource-simple triple block with protected resources `A,B,C` on
pairwise disjoint physical endpoints and nonzero protected rung products
`p_A,p_B,p_C`.  In the protected-hollow K4 application this disjointness is
automatic: endpoint supply between every resource pair forces the three
resources to lie in distinct physical components.  Suppose every state has
one crossing to each of the two foreign resources.  Thus each resource pair
has a two-edge crossing bijection.  Write its product as
`x_AB,x_AC,x_BC` and

```text
sigma_AB = x_AB/(p_A p_B),
sigma_AC = x_AC/(p_A p_C),
sigma_BC = x_BC/(p_B p_C).
```

For a component-constant word selecting exactly resources `A,B`, the local
coefficient is

```text
p_A p_B + x_AB = p_A p_B (1+sigma_AB),                 (T1)
```

and cyclically for the other two faces.

The three endpoint bijections have two parity types.  With two fixed as
diagonal, the third is:

* anti-diagonal: the six crossing edges form one `C6`; adding protected
  rungs gives `K3,3`, and the block is transition closed;
* diagonal: the crossings form two triangles; adding protected rungs gives
  the triangular prism, and every resource has failed two-exit choices.

### Exact full-block polynomial

When all three resources are selected, every matching in either orientation
is one of:

```text
all three protected rungs,
the AB crossing bijection plus the C rung,
the AC crossing bijection plus the B rung,
the BC crossing bijection plus the A rung,
or a crossing-only perfect matching.
```

The prism has no crossing-only perfect matching, so its normalized local
coefficient is exactly

```text
L_prism = 1 + sigma_AB + sigma_AC + sigma_BC.           (T2)
```

The transition-closed `K3,3` orientation has two crossing-only matchings. If
their products normalized by `p_A p_B p_C` are `tau_0,tau_1`, then

```text
L_K33 = 1 + sigma_AB + sigma_AC + sigma_BC + tau_0+tau_1,
tau_0 tau_1 = sigma_AB sigma_AC sigma_BC.               (T3)
```

Consequently, if all three binary faces of a prism are local zero suppliers,
then `sigma_AB=sigma_AC=sigma_BC=-1`, while

```text
L_prism = -2 != 0.                                      (T4)
```

Thus a nonclosed prism cannot cancel all three of its binary faces and its
fully selected triple word locally.  Any putative full source using such a
block must outsource at least the fully selected row to another active zero
block.  Conversely, the extra `tau` sectors explain why this local argument
does not replace the transition-closure theorem on the `K3,3` orientation.

### Global boundary

For component-constant words, scalar support still decomposes by resource
blocks.  Each block contributes the polynomial for its selected resource
subset, so a global coefficient is the product of those local factors.  A
row can therefore vanish in a block other than the prism under inspection.
Equations (T1)--(T4) prove a local incompatibility, not local isolation.

The exact next supplier is combinatorial: show that the binary face-cover
constraints force some fully selected prism to be the only possible zero
supplier, or combine the outsourced dependency chain into a transition-
closed block/good mixed cycle.  The known macro controls show that this
cannot be assumed without proof.


The local formulas have a separate-agent sector audit, with primary and
independent replays:

```text
python claims/arbitrary-order/verify_degree_two_triple_polynomial.py
python claims/arbitrary-order/audit_degree_two_triple_polynomial.py
```

This is a local weighted incompatibility. Source-driven global isolation
of such a block remains open; the sufficient theorem in Section 3 retains
its explicit transition-closure hypothesis.
