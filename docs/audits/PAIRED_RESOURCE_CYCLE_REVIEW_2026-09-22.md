# Independent audit of the paired-resource directed-cycle theorem

Date: 2026-09-22.

Verdict: **PASS for the stated construction family**, over arbitrary
nonzero complex weights. Global Krenn--Gu remains **UNRESOLVED**.

The assembled owning proof reviewed is
`claims/arbitrary-order/PAIRED_RESOURCE_DIRECTED_CYCLE_EXCLUSION.md`, SHA-256

```text
A6D5C3A86466AB4BB32B32B65F49340FE5053769704CB6276554432963382E13
```

Two separate agents reviewed the abstract generalization; a further
promotion pass checked the complete assembled owner at this exact hash.
These are separate-agent derivations in the same research session, not
independent human refereeing or formal kernel checking.

## 1. Precise scope

There are three protected perfect matchings of one finite physical set V,
with nonzero protected weights. Their colored resources are partitioned
into pairs of different colors. Every crossing belongs to the resulting
2-by-2 state block, has nonzero weight, and is not a physical selfloop.
Each crossing block contains a perfect matching. No other scalar edges
are present. Physical overlap of resources is permitted.

The proof needs no K4 geometry, component partition, unit normalization,
product -1, positivity, or independently adjustable cofactors. It does
need the complete colored-resource partition. State crossing degree at
most two is a consequence of the construction, not a sufficient hypothesis
for reducing an arbitrary array to it.

## 2. Independently checked balance argument

Fix a base color a. An arc u->v means that the mate of u in M_a crosses
to a foreign-colored state at v. Every u has an outgoing arc. A simple
directed cycle, including a loop, changes a pure word at its vertices.

The load-bearing converse is that each selected foreign state belongs to
one protected foreign resource and hence one block. The a-resource paired
with it is the only resource from which its selecting arc can originate.
Consequently a block with r cycle endpoints in its a-resource has exactly
2-r selected base states and r selected foreign states. The successors
are distinct because the cycle is simple. A block without a selects
nothing.

At r=0 the selected edge is the protected a-edge; at r=1 it is the actual
crossing defining the outgoing arc; at r=2 it is the protected foreign
edge. Each active block therefore contributes exactly one edge. All
physical vertices are selected once and all states belong to one block,
so this yields exactly one physical perfect matching. A product of its
nonzero complex weights cannot cancel.

The argument survives physical overlap. In the r=1 case the remaining
base endpoint is outside the cycle and its crossing target is inside,
so they are physically distinct. The auxiliary digraph can have a loop
even though scalar physical selfloops are forbidden. The owner expressly
allows and handles this case.

## 3. Mixedness and consumers

A proper cycle retains color a outside and foreign colors inside. For
a spanning cycle, the number of ab, ac and bc resource blocks is |V|/4
each: every color supplies |V|/2 resources. The resulting word has |V|/2
vertices of each foreign color. This uses physical one-state-per-vertex
selection and remains valid for overlapping protected matchings.

The complete two-crossing pairings of PSCG meet all these hypotheses.
Its macro-driven sparse normal form and PSMD's equality normal form also
meet them. PRDC therefore gives an elementary alternate consumer for both
full-source exclusions. The prior cubic correspondence and imported proof
are preserved, not withdrawn. Neither proof provides a minority-depth
bound; no WP1/WP2 exclusion or degree-two normalization is promoted.

## 4. Finite replays and independence

`verify_general_paired_resource_cycle.py` directly enumerates ordered
triples of four-vertex perfect matchings, allowed resource pairings and
all nonloop block supports containing a crossing perfect matching. It
constructs a cycle word and tests it against the three physical perfect
matchings. Its exact result is 4,872 configurations, including 5,034
constructed loop words and 108 coincident-resource pairing observations.

`audit_paired_resource_cycle_k3.py` uses a separately specified nonbipartite
three-K4 pairing and constructs cycles by a functional successor walk.
It independently counts physical matchings by vertex-deletion recursion.
Five dense/mixed block suites give 15 base-color cases, including three
suites where every block is simultaneously dense. It imports neither the
primary script nor a project scientific implementation.

These checks are exact finite corroboration. The unbounded theorem is the
written state-balance and mixedness proof. No external solver or imported
matching theorem is required.

The scratch generalization and second abstract review were frozen at
SHA-256 `7D39362DF9AC5A8BC7298B019B7F56057F75E80673D17CECB26742EE3EBAC146`
and `F4A6A3C3F8EE71AE21C281EDC16C28178518D0F9839D6F2E0E43FB059776C508`,
respectively. The assembled owner above is the authoritative promoted
statement and contains the complete proof, so scratch paths are not
load-bearing dependencies.
