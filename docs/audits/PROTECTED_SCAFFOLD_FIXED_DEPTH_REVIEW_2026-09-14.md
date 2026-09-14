# Protected-scaffold fixed-depth review, 2026-09-14

## Status and exact scope

This is an independent adversarial review of
`claims/arbitrary-order/PROTECTED_SCAFFOLD_FIXED_MINORITY_DEPTH_NO_GO.md`
and its finite control. The constructive theorem is sound over the complex
numbers. For every fixed minority radius `r`, it constructs a finite protected
scaffold satisfying every source equation within that radius while failing a
mixed source equation outside it.

This is a proper-subsystem obstruction. It does not construct a full GHZ
source, exclude arbitrary protected scaffolds, give one array that works for
all radii, or resolve the Krenn--Gu conjecture. The graph and its order depend
on `r`. The global conjecture remains **UNRESOLVED**.

```text
owner snapshot SHA-256: 7149c88f804a3878723e27723a6a2aa2581b10a94a57d93466b84a064690b186
owner canonical-LF SHA-256: 77491d6251f66f8f9513e0c654094a2dc922e4365c0d34e1192c8e1583763427
verifier SHA-256: 8f868f461e949cc6f6c26c4ca5db96e4d813730ec9194a815c56eb4f3811accf
```

The snapshot hash records the reviewed Windows file. The canonical-LF hash
identifies its Git contents and is portable across checkout line endings;
normalizing CRLF changes no mathematical text. The verifier already uses LF.

## Literal gadget and indexing review

The six labels are `01,02,10,12,20,21`. I independently reconstructed the
displayed row and column allocations. For each left color `c`, the two labels
`cd` use exactly the two edges of `M_c`; for each right color `d`, the two
labels `cd` use exactly the two edges of `M_d`. Each gadget's two rows and two
columns are distinct, so it is a partial permutation between its allocated
pairs, and its two crossing weights have product `-1`.

This verifies the physical indexing in both orientations. Transposition gives
the reverse matrix entry with reversed endpoint colors. Distinct component
edges cannot collide as physical edges, and the distinct shifts ensure that
the labeled component graph is simple.

## Forest and monochromatic-component argument

For a word with at most `r` non-`c` vertices, every supported crossing edge
uses at least one such vertex because all crossing entries have distinct
endpoint colors. A physical perfect matching therefore uses at most `r`
crossing edges and at most `r` component-graph edges. In a component graph of
girth greater than `r`, its used simple subgraph is a forest.

For any used forest edge, delete it and take the cut given by either resulting
tree component. The cut side is a union of four-vertex blocks, so a perfect
matching crosses it an even number of times. The deleted gadget is the only
used component edge across that cut and has at most two physical entries.
Because it is used, its multiplicity is exactly two. This cut argument applies
to every used gadget; it does not assume a leaf order or discard edges incident
to an already removed block.

A doubled gadget consumes its full allocated edge at each endpoint block. Two
used gadgets at one block must use disjoint local edges. Edges from distinct
perfect-matching classes on `K4` intersect, so both allocations then have the
same scaffold color and consume all four vertices with that color. With one
used gadget, its two remaining vertices form the complementary edge in the
same matching class and have that color. With no used gadget, the internal
physical perfect matching is one of `M_0,M_1,M_2`; both of its edges are
nonzero only when all four vertices carry its class color. Thus every block in
a supported term is monochromatic. Non-component-constant words in the fixed
minority ball vanish term by term.

## Component-constant amplitude and availability

For a component-constant word, a gadget is scalar-supported exactly when its
ordered label equals its endpoint block colors. At any block the at most two
available gadgets use the two disjoint edges of that block's matching class.
Consequently the scalar graph decomposes into untouched protected edges and
vertex-disjoint four-cycles, one per available gadget. The two perfect
matchings of each four-cycle contribute `1` and `-1`. Hence the full amplitude
is exactly

```text
product over available gadgets of (1-1).
```

The empty product is one; no unlisted cofactor or exterior resource remains.

For a mixed word in the radius, let `S` be its non-majority blocks. If no
gadget is available, a left block of color `d != c` follows its unique label
`dc`, while a right block follows its unique label `cd`. Its neighbor must
also lie in `S`, or that gadget would be available. The resulting finite
out-degree-one digraph has a directed cycle. Immediate reversal along one
component edge would require the opposite endpoint to have the majority color,
contrary to its membership in `S`. The cycle therefore gives a simple
component-graph cycle of length at most
`|S| <= floor(r/4) <= r`, contradicting girth greater than `r`. At least one
gadget is available and the mixed amplitude is zero. Pure words have no
available gadget and amplitude one.

## Base graph and explicit failure

For shifts `D=(0,1,3,8,12,18)` modulo 31, I independently enumerated the 30
ordered differences. Every nonzero residue occurs exactly once. The resulting
62-vertex, 186-edge bipartite component graph is simple, has every label once
at each vertex, has no four-cycle, and has girth exactly six.

I also checked every labeled edge against the displayed component-color
strings:

```text
L: 0100100100100100101001002000000
R: 0000120100100100100201001000000
```

There are zero available gadgets. The color histogram on components is
`{0:44, 1:15, 2:3}`, so the word is mixed and has 72 physical minority
vertices relative to color zero. Its scalar graph contains only the protected
internal edges, giving exactly one global perfect matching of weight one while
the target is zero. This is an explicit full-source failure, rather than an
inference from the fixed-depth proof.

## Arbitrary-girth finite cover

For fixed `r>=1`, the reduced-word ball `B_r` is finite. For a letter `l`, the
map `s_l` pairs each word `w` of length less than `r` not beginning with `l`
with `lw`; boundary words without such a partner are fixed. This partitions
`B_r` into transpositions and fixed points, so every `s_l` is an involution.
With rightmost action first, any nonempty reduced product of length at most
`r` sends the empty word to that same nonempty reduced word. The generated
subgroup of the finite symmetric group on `B_r` therefore has no reduced
relation of that length.

On the lifted graph, traversing a label `l` changes the group coordinate by
right multiplication with `s_l` in either direction; the reverse-neighbor
formula uses `s_l^2=1`. A simple cycle has unequal consecutive labels because
each label occurs only once at a vertex. A cycle of length at most `r` would
therefore yield a forbidden nonempty reduced relation. This proves girth
greater than `r`. The `Z/31` coordinate and distinct shifts preserve
simplicity, bipartiteness, degree six, and the one-of-each-label incidence.
The construction is finite because the permutation group is finite; no group
enumeration or residual-finiteness theorem is assumed.

Pulling the explicit base coloring back by the `Z/31` coordinate preserves
the label and endpoint colors of every edge. It therefore preserves the
absence of available gadgets and the full-failure amplitude one. Since a
finite 6-regular graph contains a cycle, girth greater than `r` also forces
its `62|G|` component vertices to exceed `r`. The pulled-back coloring has
`72|G|` physical minority vertices relative to color zero, so the displayed
failure remains outside the claimed fixed minority ball.

## Finite replay and adversarial controls

The standalone source verifier completed successfully with 248 physical
vertices and 744 nonzero literal entries. It checked the three pure amplitudes,
all 372 single-minority-component words, the explicit mixed failure, the
allocation table, the exact base girth, and reduced-word permutation controls
through radius three. Its own receipt explicitly says that this is not an
exhaustive check of all four-minority words or the arbitrary-depth theorem;
those claims are owned by the arguments above.

A separate standard-library reconstruction, with no project scientific
imports, additionally checked reduced-word balls through radius six and gave
this local receipt:

```text
PASS_INDEPENDENT_FIXED_DEPTH_STRESS_CHECKS
receipt SHA-256: 19e1f9bea17434d5e92c7155545f8f57ea31d2e68ceccfb76819267931a01044
```

The following mutations behaved as required:

- replacing shift 18 by 17 creates a four-cycle, demonstrating that the
  difference-set/girth guard is load-bearing;
- changing one color in the explicit failure introduces one available gadget
  and changes its factored amplitude from one to zero;
- giving a gadget two equal signs changes its local cancellation factor from
  zero to two; and
- the local allocation census confirms that edges from distinct matching
  classes always intersect, which is the step used to force one block color.

These finite controls test the indexing, signs, graph guard, explicit failure,
and truncated permutation construction. The universal result rests on the
written cut-parity, availability, and reduced-relation proofs.
