# Independent review: common-star at-most-two-port obstruction

## Conclusion and exact scope

The at-most-two-port theorem in
[`PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md)
is correct under its stated hypotheses over `C`.  For a common-star protected
scaffold on a simple component graph, with one unequal ordered-color gadget per
component pair and two nonzero factor weights per gadget, the singleton and
double-component targets force every ordered port to contain at least two
gadgets.  If all ports contain at most two, those same equations force the
state graph to split into coherent `K_(2,2,2)` resources.  One additional
mixed component-constant word then has nonzero source, contradicting the full
component targets.

More generally, whenever the state graph is already known to decompose into
complete tripartite resources, the singleton and double-component targets
first force balanced color-part sizes of at least two; one global component
word then excludes it.  The degree-two theorem supplies this resource
decomposition in its stated subfamily; no such decomposition is claimed for
arbitrary larger ports.  The lower bound two is essential to ensure the cycle
word leaves at least one component unchanged.

Thus a common-star array satisfying all component targets must have some
ordered port of size at least three.  The result does not classify ports of
higher degree, arbitrary hollow protected-scaffold fillings, Q4, or the global
Krenn--Gu conjecture.  The global conjecture remains **UNRESOLVED**.  No Lean
formalization was reviewed, and no external mathematical result is used.

The accepted owner and independent checker were reviewed at the following
SHA-256 values over LF-normalized text bytes:

```text
owner:
64dda6c7e0f1915f6e104821fd8ca0c40a8f03d6cc5c29a4f47ff3ae3d876bda

independent checker:
b20be2477f2372358f1d6140bec4f9ad6cb4251e684926b93d021f646b505c0c
```

The companion checker is
[`audit_protected_scaffold_common_star_two_port.py`](../../claims/arbitrary-order/audit_protected_scaffold_common_star_two_port.py).
It imports neither the owner verifier nor project scientific code.  Its finite
checks corroborate the proof; the analytic argument below supplies the
arbitrary-order result.

## Shared-neighbor identity

For two changed components `u,v` over background color `c`, retain all
compatible edges from `u` and `v` to exterior components.  Write their center
and leaf weights as `(A_j,B_j)` and `(C_j,D_j)`, and set

```text
s=sum_j A_j B_j,       t=sum_j C_j D_j,
h=sum_j A_j B_j C_j D_j,
x=sum_j A_j D_j,       y=sum_j B_j C_j.
```

The common active component set in the exact double-hafnian formula has size
zero, two, or four.  The two equal center/leaf star matchings on four vertices
give `st-h`: the common-neighbor diagonal is excluded because a matching
cannot reuse that exterior component.  The two unequal center/leaf matchings
give `xy-h` for the same reason.  Including the empty term, both one-edge star
terms, and a possible central compatible edge of product `q` gives

```text
F_(u:d,v:e | c) = (1+s)(1+t) + q + xy - 2h.          (1)
```

This derivation keeps the cyclic center/leaf interference.  It is not a
forest specialization.

The singleton equation at `u` says
`1+s=-q_uv(d,c)`, because `s` omits `v`; similarly
`1+t=-q_vu(e,c)`.  The two deleted entries cannot both be supported: the
first requires the sole label on `uv` to be `(d,c)`, while the second requires
it to be `(c,e)`, and `d!=c`.  Hence their product vanishes and every mixed
double row gives

```text
q_uv(d,e) = 2h-xy.                                  (2)
```

This also covers `d=e`, when the hollow central term is zero.  The apparent
small-order issue is harmless.  Before any double row is used, the singleton
targets require all six ordered ports at every component to be nonempty.  A
simple graph with one label per component pair therefore has degree at least
six and `k>=7`, so every double-component word in (1) is mixed.  For
`2<=k<=6`, a singleton equation already fails.

The independent checker derives (1) from formal perfect-matching expansions
with three symbolic exterior neighbors.  The two sides contain the same 20
monomials.  Deleting the `-2h` correction leaves a nonzero three-monomial
residual, which is a direct mutation control for the most likely invalid
simplification.

## Support consequences and the unique-port contradiction

Let the state graph have vertices `(u,a)` and one weighted edge of product
`q` for every compatible ordered-color gadget.  It is tripartite by state
color and has no edges between two states of one physical component.

Apply (2) with equal changed colors to two distinct same-color states.  If
their neighbor sets in another color part intersect in exactly one state,
then `xy=h` is the product of the two nonzero incident gadget products and
the central term is zero.  Equation (2) would say `0=h`, a contradiction.
The same conclusion holds with the two color parts exchanged.

Apply (2) with distinct changed colors to a supported state edge.  With no
common state of the third color, `h=x=y=0`, which would force its nonzero
product to vanish.  Thus every edge lies in a coherent state triangle.  If
the common third-color neighbor is unique, (2) reduces exactly to

```text
q_XY = q_XZ q_YZ.                                   (3)
```

Now suppose a state `X` of color `a` has a unique color-`b` neighbor `Y`.
The no-single-intersection result makes `X` the unique color-`a` neighbor of
`Y`; otherwise `X` and another color-`a` state would share exactly `Y`.
The singleton port equation gives `q_XY=-1`.

For the third color `c`, every edge `XZ` must use `Y` as its coherent
color-`b` neighbor.  The reverse argument from an edge `YZ` uses `X`, so
`N_c(X)=N_c(Y)`.  These triangles have unique third state, and (3) gives
`q_XZ=-q_YZ` term by term.  Both color-`c` port sums are `-1`, but the
termwise negation makes one sum the negative of the other.  This is impossible
over `C`.  Therefore no ordered port is empty or unique, even if other ports
have unbounded size.

Nonzero gadget factors are load-bearing here.  They make every `q` nonzero
and rule out the zero value produced by the shared-neighbor contradictions.

## Degree-two resource normal form

Assume every port has size at most two.  The preceding argument makes every
port have size exactly two.  Between two state-color parts, the graph is
2-regular.  Two same-side rows that intersect cannot intersect once, so their
two-element neighbor sets coincide.  Each bipartite component is therefore a
`K_(2,2)` block.

At a color-`a` state `X`, let the color-`b` neighbors be `Y1,Y2` and the
color-`c` neighbors be `Z1,Z2`.  Edge triangle coverage makes the induced
support between these pairs meet each row and column.  Because the full
`b-c` graph is a union of `K_(2,2)` blocks, this local support is either a
perfect matching or all four edges.  Three edges force the fourth inside the
same block.

In the four-edge case, let `X_b` be the other color-`a` state in the
`a-b` block through `X`.  The edge `X_b Y1` needs a common color-`c` state,
which must be `Z1` or `Z2`.  The color-`c` neighborhoods of `X_b` and `X`
therefore intersect.  They cannot intersect once and both have size two, so
they coincide.  Hence `X_b` is also the other color-`a` state in the `a-c`
block.  All three pair graphs close on these six states, giving a complete
`K_(2,2,2)` component with no outgoing state edge.

In the perfect-matching case, every edge at `X` has exactly one common third
state.  A neighbor cannot have the four-edge pattern, because that would give
the shared edge two common third states.  The perfect-matching pattern thus
propagates through the connected component.  On any resulting unique
triangle, applying (3) cyclically gives

```text
q_XY=q_XZ q_YZ,  q_XZ=q_XY q_YZ,  q_YZ=q_XY q_XZ.
```

All three values are nonzero, so each has square one.  In particular, the two
products in every port at `X` belong to `{1,-1}`.  Their sum cannot equal the
required singleton sum `-1`.  The perfect-matching case is impossible, and
the state graph is a disjoint union of coherent `K_(2,2,2)` resources.

As an independent finite support check, the companion enumerates every triple
of pair-block graphs on four states of each color.  There are 18 possible
unions of `K_(2,2)` blocks per pair and 5,832 triples.  Of the 1,836 triples
where every edge has a coherent third-color neighbor, 108 are entirely
`K_(2,2,2)` type and 1,728 are entirely unique-triangle type.  No mixed local
type occurs.  This is a control on the graph dichotomy, not an exhaustive
all-order proof.

## Global mixed word

In a `K_(2,2,2)` resource, all six states come from distinct physical
components.  If two different-color states came from the same component,
the complete tripartite resource would contain an edge between them, which
the state graph construction forbids.

For each color `c`, pair the two physical components whose color-`c` states
lie in each resource.  Every component has exactly one color-`c` state, so
these resource pairs form a perfect matching `P_c` on the component set.
The multigraph `P_0 union P_1` is a union of even alternating cycles; a shared
edge is a doubled two-cycle.  Two-color each cycle, and assign each component
its resulting color zero or one.

Each resource then has exactly one selected color-zero state and one selected
color-one state.  The complete tripartite block supplies their unique gadget,
and no selected state lies in another resource.  The compatible component
graph is a matching of one edge per resource.  Formula (1) at the global
component level therefore factors as

```text
F(x) = product_r (1+q_r).                            (4)
```

Each factor is nonzero.  At either endpoint of the selected edge, its relevant
ordered port contains it and one other edge of nonzero product `q'_r`.
The singleton equation gives `q_r+q'_r=-1`, hence
`1+q_r=-q'_r!=0`.  The word is mixed because every `P_0` edge has opposite
endpoint colors.  Equation (4) is consequently nonzero and contradicts its
component target zero.

This final step genuinely uses a global component word.  It neither assumes
uniform `q=-1/2` nor positivity, girth, U4, or a forest outside the constructed
compatible matching.

## General complete-resource consumer

The global contradiction has a stronger form that does not require resource
parts of size two.  Suppose the state graph is a disjoint union of complete
tripartite resources.  In one resource, let two color-part sizes be `r,s`.
Summing the singleton normalization over the `r` rows gives total edge weight
`-r`; summing the same matrix over its `s` columns gives `-s`.  Hence `r=s`
over `C`.  Repeating this for the three color pairs shows that each resource
has shape `K_(m_r,m_r,m_r)`.  The no-unique-port result gives `m_r>=2` under
the singleton and double targets.

Build a directed multigraph whose vertices are resources.  Physical component
`u` gives an edge from the resource containing `(u,0)` to the one containing
`(u,1)`.  Each resource has outdegree and indegree `m_r`.  It has no loop:
otherwise two different-color states of `u` would lie in one complete
resource and would be joined by a forbidden state edge.  Following outgoing
edges in this finite graph yields a simple directed cycle.

Begin with the globally constant color-zero word and recolor to one precisely
the physical components represented by the cycle edges.  At each cycle
resource, the active states are all its color-zero states except the state `X`
on its outgoing cycle edge, together with the color-one state `Y` on its
incoming edge.  Their compatible graph is a star, whose exact factor is

```text
1 + sum_(Z != X) q_ZY = -q_XY != 0.
```

The equality is the singleton port normalization at `Y`; nonzero gadget
factors give the final inequality.  Every off-cycle resource contributes one,
and resource components are disjoint, so the full source is the product of
these nonzero factors.  The word is mixed.  If there are `R` resources, then
`k=sum_r m_r>=2R`, while a simple resource cycle changes between one and `R`
components.  Thus it changes fewer than all `k` components.

This proves the owner's general complete-resource consumer.  It uses the
double equations only through the no-unique-port lemma, not to derive the
complete-resource hypothesis.  The degree-two argument above is the proved
upstream decomposition currently available.

## Independent replay and sharp controls

Run the portable checker from the repository root with:

```text
python -X utf8 claims/arbitrary-order/audit_protected_scaffold_common_star_two_port.py
```

An optional `--output PATH` writes LF-terminated JSON and emits only a compact
status line.  The replay reported:

```text
status: PASS
shared identity: 20 exact monomials
local pair-block triples: 5832 checked, 0 mixed types
k=14 control: 168 S1, 1092 same-color S2, 1092 distinct-color S2 equalities
k=14 derived resources: 7
k=14 literal 56-vertex source on derived binary word: 1/128
degree-three complete-resource control: 39 components, 13 resources
degree-three literal 156-vertex source on cycle word: 1/1594323
```

The `k=14` construction is rebuilt independently over `Q(sqrt(3))`.  The
checker verifies S1 and both S2 matrix identities directly rather than calling
the primary physical-row verifier.  It then derives the seven state-graph
`K_(2,2,2)` resources and the `P_0/P_1` binary coloring from the support.  A
separate recursion on all 56 literal physical vertices evaluates that mixed
word to `1/128`, against target zero.  This proves that dropping the global
row invalidates the conclusion even when every singleton and double equation
holds.  The owner verifier supplies broader exact physical controls; the two
routes have different derivations and representations.

The checker also independently constructs 13 complete `K_(3,3,3)` resources
on 39 components, with one label per component pair and every gadget product
`-1/3`.  Its resource digraph contains a 13-cycle.  Recoloring the 13
corresponding components makes each resource factor `1/3`, and direct recursion
on the 156 physical vertices gives `3^(-13)=1/1594323`.  This corroborates the
arbitrary-size consumer beyond the degree-two case.  It is only a control of
that consumer: the construction is not asserted to satisfy S2, Q4, or all
component targets.

Other mutation boundaries are explicit.  Omitting `-2h` fails the symbolic
identity.  Allowing a zero gadget factor invalidates the nonvanishing steps.
Allowing several differently labeled gadgets on one component pair invalidates
the deleted-star product and the state graph model.  None of these mutated
settings is covered by the reviewed theorem.
