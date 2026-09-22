# Every k=3 minimum-density equality support fails WP1

Date: 2026-09-22

## Verdict

**Exact k=3 equality-case exclusion.**  Every protected `k=3` array with the
minimum `6k=18` supported crossing scalar entries fails WP1.  Macro rigidity
forces its literal graph either to be color/component isomorphic to the
`C9` cycle-square graph audited below or to have an extra macro-avoiding
transversal and fail immediately.  After every necessary macro and empty-q1
condition is imposed on the `C9`, every remaining port allocation and
endpoint-bijection system has a mixed physical word with `min_c q_c<=1` and
exactly one supported matching.

Equivalently, any `k=3` WP1 array has strictly more than 18 supported
crossing entries.  This does not exclude minimum-density supports at other
orders, prove WP1, or change the global Krenn--Gu status.

## 1. Literal graph and macro rigidity

Index the nine component-color literals by

```text
t=3A+a,       A in {0,1,2}, a in {0,1,2}.
```

Start with `C9^2` and remove the three edges internal to each component
triple `{3A,3A+1,3A+2}`.  The remaining two-regular literal graph `F` has

```text
E(F)={(0,7),(0,8),(1,3),(1,8),(2,3),(2,4),(4,6),(5,6),(5,7)}.   (1)
```

Equivalently its cycle order is

```text
0,7,5,6,4,2,3,1,8.
```

Every edge joins different colors and different physical components.  Give
each edge one two-lane pair gadget of crossing-weight product `-1`.

A component-constant word selects one literal from every component triple.
The removed internal edges can never join two selected literals.  Therefore
it avoids all gadgets precisely when its three literals form an independent
set in `C9^2`.  The three cyclic gaps are each at least three and sum to nine,
so all equal three.  The only avoiding transversals are

```text
(0,0,0), (1,1,1), (2,2,2).                            (2)
```

Thus the support is exactly macro-rigid.

## 2. Every macro-rigid k=3 literal graph is this C9

In an arbitrary minimum-density equality support, the gadgets between each
pair of colors form a perfect matching of the physical components.  Identify
the three component sets by their common physical labels and write

```text
sigma_ab : components at color a -> components at color b.
```

Macro rigidity forces every `sigma_ab` to be one cycle, at every order.  If
`S` were a proper nonempty union of directed cycles of `sigma_ab`, color the
components in `S` by `a` and every other component by `b`.  Invariance of
`S` means that no `a--b` gadget has both endpoints selected; no third color
is selected.  This would be a mixed macro-avoiding transversal whose only
matching is protected, contrary to a zero macro target.

For `k=3`, hollowness and the preceding cycle statement make every
`sigma_ab` one of the two shifts `A -> A+1` and `A -> A-1` on `Z/3`.
A simultaneous reflection of the component labels reverses all three
shifts, so normalize `sigma_01` to `+1`.  In the order
`(sigma_01,sigma_02,sigma_12)`, four sign patterns remain:

| signs | literal components | conclusion |
|---|---|---|
| `(+,+,+)` | one `C9` | map to (1) by `A -> -A` |
| `(+,+,-)` | one `C9` | swap colors `1,2`, swap local ports `2,3`, then `A -> -A` |
| `(+,-,-)` | one `C9` | cycle colors `0->1->2->0`, cycle local ports `1->2->3->1`, then `A -> -A` |
| `(+,-,+)` | three `C3`s | not macro-rigid |

The local port permutations in the table carry `M_a` to the matching for
the renamed color, so these are isomorphisms of the full protected scaffold,
not merely abstract literal graphs.  They preserve coefficient
multiplicities and permute the three `q_c`, hence preserve `min_c q_c`.

For the triangle pattern, the component-color assignment

```text
(x_0,x_1,x_2)=(0,2,1)                                  (3)
```

selects one vertex from each physical component and one from each literal
triangle.  It is an extra independent transversal, so its protected macro
coefficient is one.  This pattern cannot satisfy the macro equations.

Therefore every macro-rigid `k=3` equality support is physically isomorphic
to the `C9` representative (1), and the port cover below is exhaustive for
all such supports.

## 3. Necessary local WP1 restrictions

The two neighbors of a color-1 literal lie in two different physical
components.  If its two gadgets reused one protected `M_1` edge, the macro
word selecting the literal and its two neighbors would enable a two-edge
transit ladder.  Its exact coefficient is `f_3=-1`, since the neighbors are
not adjacent in `F`.  Hence every color-1 literal must be **split**, using
the two complementary `M_1` edges.

The two neighbors of every color-0 or color-2 literal lie in one common
physical component.  Such a literal may be split or hidden transit.  At a
hidden transit literal, the empty-q1 alignment prohibition is necessary:
the unshared ports of the two target pairs must have the same preimage in
the reused root pair.  If not, the corresponding empty-q1 word has one
nonzero matching monomial.

The independently proved decorated two-hidden-block lemma in
[two-hidden-block proof](TWO_HIDDEN_BLOCK.md) excludes adjacent hidden
transit literals, even when the two end literals are not assumed split.
The finite residual therefore consists only of isolated hidden literals
separated by split literals.

## 4. Exact gauge quotient

The color-preserving automorphisms of a protected K4 are its four
translations on the binary port labels.  On the two `M_c` pair indices they
flip exactly the even vectors

```text
000, 011, 101, 110.                                    (4)
```

At each physical component this gauge uniquely fixes the first color-0 and
first color-1 incidence to pair index zero.  Since color 1 is split, its
other incidence then has pair index one.  The remaining choices are:

* the second color-0 pair index; and
* both color-2 pair indices.

There are therefore `2^3=8` allocation representatives per component and
`8^3=512` for the three components.  Every gadget has two endpoint
bijections, giving `2^9=512` map systems.  Thus the exact gauge-fixed cover
has

```text
512 * 512 = 262144                                      (5)
```

configurations.  Physical relabeling preserves the protected matchings,
the three `q_c`, matching multiplicities, and all coefficient equations, so
the quotient loses no possible WP1 support.

Of the 512 pair allocations, 296 contain adjacent hidden literals and are
already excluded analytically.  The isolated-hidden residual has

```text
(512-296)*512 = 110592                                  (6)
```

raw configurations.  Imposing every hidden alignment equation leaves
exactly 32,768 scalar supports.

## 5. Exact residual exclusion

`enumerate_k3.py` independently reconstructs all 18 protected and
18 crossing scalar entries for each residual support.  Coincident gadgets
share physical color states, so the checker deliberately does not use the
disjoint-C4 auxiliary graph.  It recursively enumerates literal scalar
matchings of the 12 physical vertices, groups them by their full color word,
and computes all three paired-minority counts.

For an exact weight check it assigns the two lanes of every gadget weights
`+1,-1`.  The replay verifies all three pure coefficients are one and all 24
mixed macro coefficients are zero for every checked support.  The exclusion
itself is stronger and support-only: every residual support has a mixed
`min_c q_c<=1` word with exactly one matching.  Its coefficient is one
nonzero product for every choice of nonzero gadget weights, so no weight
specialization can repair it.

One literal witness from the cover is

```text
0000|2100|0100,        (q_0,q_1,q_2)=(1,4,5),
```

with sole matching

```text
P_A0(01), P_A0(23),
X_(B,2)--(C,1)(4,9), X_(B,1)--(C,0)(5,8),
P_B0(23), P_C0(23).
```

The exact witness varies with the port configuration; the checker derives
one rather than assuming a uniform word.

## 6. Replays and scope

Run from the repository root:

```text
python -X utf8 claims/arbitrary-order/minimum-density-wp1/verify_k3_topology.py
python tools/research/run_bounded.py --run-id replay-k3-wp1 --timeout-seconds 300 --memory-mb 8192 -- python -X utf8 claims/arbitrary-order/minimum-density-wp1/enumerate_k3.py
```

The first replay enumerates the four normalized signed-shift patterns,
checks their literal component sizes and independent transversals, verifies
the three displayed component/color/port isomorphisms, and returns
`K3_LITERAL_TOPOLOGY_CLASSIFICATION_PASS`.

Receipt:

```text
gauge_fixed_raw_configurations 262144
adjacent_hidden_pair_allocations_excluded_analytically 296
raw_isolated_hidden_configurations 110592
q1_aligned_configurations 32768
independent_transversals [(0,0,0),(1,1,1),(2,2,2)]
checked_scalar_supports 32768
passing_configurations 0
C9_FAMILY_EXCLUDED
```

The analytic inputs remove configurations that already violate a macro or
empty-q1 equation.  The topology lemma proves that the finite check covers
the remaining isolated-hidden port systems of every macro-rigid `k=3`
equality support.  No analogous classification or finite cover is claimed
at higher orders.


## Certificate and independent verification

The durable compressed k3-witnesses.jsonl.gz contains one primary witness
for each of the 32,768 residual supports. The independent audit_k3_words.py
reconstructs the entire residual configuration set, every scalar support,
and the matching count of each supplied word without importing the primary
enumerator. It rejects omissions and duplicates. The exact certificate
semantics, promotion provenance and hashes are in [README](README.md),
[AUDIT](AUDIT.md) and manifest.json.
