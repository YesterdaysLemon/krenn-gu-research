# Three protected matchings and the paired-resource cycle obstruction

Date: 2026-09-22.

Status: proved over C by the elementary argument below, with two separate
agent reviews. No external matching theorem or Lean formalization is used.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

This result, node PRDC, excludes a construction family on arbitrary physical
vertex sets. It extends the complete-pair family of
[PSCG](PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md) to blocks with two,
three or four crossings, arbitrary nonzero protected weights, and physically
overlapping protected matchings. The full-source equations are not known to
force this family. The support-class parent at crossing degree at most two
remains open.

## 1. Exact hypotheses and conclusion

Let V be a finite physical vertex set with |V|>1. For each a in {0,1,2},
specify a perfect matching M_a of V. Every edge of M_a is a **colored
resource**, consisting of its two endpoint states (u,a),(v,a). Give each
resource a nonzero complex protected weight. The three matchings may overlap
as uncolored edge sets.

Partition all colored resources into unordered pairs of different colors.
A pair consisting of an a-resource e and a b-resource f defines a block
on their four colored states. Its scalar support consists of the protected
edge on each resource and a bipartite crossing support between e and f.
Require that this crossing support contain a perfect matching. Thus a block
has two, three or four supported crossings, all with nonzero complex weights.
Allow resources to overlap physically, but forbid scalar physical selfloops.
There are no scalar entries outside the stated protected edges and blocks.
As usual, a scalar edge is specified by its physical endpoints and their
colors; reversing its orientation transposes these labels, rather than
creating a second entry.

A physical word w:V->{0,1,2} selects the state (v,w(v)) at every v. Its
coefficient T(w) is the sum of products of actual scalar weights over perfect
matchings of the induced selected-state graph. This definition includes all
matching terms and all cancellations in that word.

**Theorem.** Every array with the above support has a mixed physical word
with exactly one supported perfect matching. Its coefficient is nonzero.
In particular, no such array has all mixed coefficients zero.

No normalization of pure coefficients is needed. A global order, a K4
partition, disjoint physical shores, gadget product -1, positivity, or
genericity is not assumed. The resource partition does imply |V| divisible
by four: writing n_ab for the number of blocks of color type {a,b},

```text
n_01+n_02 = n_01+n_12 = n_02+n_12 = |V|/2,
so n_01=n_02=n_12=|V|/4.                         (1)
```

## 2. A cycle changing one pure word

Fix a base color a. For u in V, let m_a(u) be its mate in M_a. The resource
e_u={u,m_a(u)} is paired with a unique resource f_u of some foreign color
b!=a. Define a directed graph D_a on V by drawing an arc u->v, labeled b,
whenever the actual scalar crossing

```text
(m_a(u),a) -- (v,b),     v in f_u,                (2)
```

is supported. Every vertex has positive outdegree, since every endpoint
of every resource has a crossing neighbor in its block. A finite directed
graph with this property contains a simple directed cycle C. Auxiliary
selfloops are allowed and count as one-vertex cycles: prohibition of
physical scalar selfloops does not prohibit u->u in (2).

Start with the constant word a. For each arc u->v in C, change the color
at v to the foreign label of that arc. Distinct cycle vertices have
distinct successors, so this specifies exactly one selected state at every
physical vertex. Every cycle vertex changes away from a.

## 3. Why every active block selects exactly one edge

The blocks partition colored states, even when their physical vertex sets
overlap. Every selected foreign state (v,b) was chosen by an incoming cycle
arc from some u. The resource of M_b containing v belongs to one block,
so the unique a-resource in that same block must be e_u. Consequently a
foreign state in a given a-block is selected **only** by an outgoing cycle
arc from one of its two a-resource endpoints. This converse excludes
uncontrolled arrivals from other resources. A block omitting a selects
no state at all: it contains neither a retained base state nor any foreign
state reachable from an a-resource.

Consider a block pairing e={u,m_a(u)} with f. Set r=|C intersect e|.
Exactly 2-r states of e survive and exactly r states of f are selected.
The latter count uses injectivity of the successor map on C.

* If r=0, the selected states are the two states of e and their protected
  edge is the only scalar edge between them.
* If r=1, say u is on C, the remaining state is (m_a(u),a). The successor
  of u is joined to it by the supported crossing (2), which is the only
  scalar entry on this pair of selected states.
* If r=2, the two distinct successors exhaust the two endpoints of f.
  Its protected edge is the only scalar edge between those selected states.

These statements also cover physical overlap between e and f. In the
middle case, m_a(u) is outside C and the selected foreign endpoint is on
C, so they are physically distinct. A one-vertex cycle is therefore safe.
In the other cases a protected matching edge has distinct endpoints by
definition.

Thus every nonempty selected block is exactly one edge. Because the word
selects one state per physical vertex and the blocks partition all states,
these edges give a unique physical perfect matching. Its weight is a
product of actual nonzero supported entries, and is nonzero over C.
No cancellation equation or independently chosen weight is used.

## 4. Why the word is mixed

If C is a proper subset of V, a vertex outside C retains a and every
vertex on C has a foreign color. The word is mixed.

If C spans V, every a-resource has r=2. Every ab-block selects its entire
b-resource and every ac-block its entire c-resource. Equation (1) gives
2n_ab=|V|/2 selected b-states and 2n_ac=|V|/2 selected c-states. Both counts
are positive. Since the word selects one state at each physical vertex,
these are also its physical color counts. The word is again mixed.

This completes the all-order proof.

## 5. Consumers and the unresolved parent

The two-crossing complete pairings in PSCG satisfy every hypothesis, so
Sections 2--4 give an elementary alternative proof of their full-source
exclusion. PSCG's cubic correspondence and imported proof remain valid;
they are no longer required for that exclusion. Its state-degree-one macro
normal form still supplies a conditional reduction into this family.

The equality normal form of
[PSMD](PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md) supplies the same
family. Thus its strict crossing-density conclusion also has a proof route
without the imported classification of graphs with three perfect matchings.
Neither proof bounds the constructed word's paired-minority depth. In
particular, neither establishes the all-order WP1 or WP2 exclusion.

The larger two/three/four-crossing paired-block family has state crossing
degree at most two and is excluded. However, that degree bound alone
does not partition resources into pairs. Endpoints may send crossings into
different foreign resources; protected resources may be reused across
candidate blocks. Deriving a usable resource structure from the full
source remains a load-bearing open obligation for the degree-two SFULL
parent. No arbitrary-witness-to-scaffold or block reduction is asserted.

The parent attempt synthesizes PSCG's support normalization and PSMD's
shared-resource elimination. It yields this reusable exclusion, not an
exhaustive degree-two cover. The four-crossing singleton terms and
macro-invisible excess entries documented in the degree-two research
controls cannot be discarded when trying to supply the missing reduction.

## 6. Evidence

The proof is Sections 1--4, not finite extrapolation. Two separate agents
reviewed the general physical-overlap and spanning-cycle cases; see the
[independent audit](../../docs/audits/PAIRED_RESOURCE_CYCLE_REVIEW_2026-09-22.md).
No human-referee or formal-kernel verification is claimed.

Portable standard-library companions:

```text
python claims/arbitrary-order/verify_general_paired_resource_cycle.py
python claims/arbitrary-order/audit_paired_resource_cycle_k3.py
```

The first exhausts the 4,872 four-vertex configurations formed by ordered
triples of protected perfect matchings, different-color resource pairings,
and allowed block supports containing a perfect matching. It includes
coincident resources and 5,034 constructed one-vertex cycle words. The
second uses a separate nonbipartite three-K4 construction and physical
matching recursion, checking 15 base-color cases with simultaneous dense
blocks. Neither imports the other or a project scientific implementation.
The finite checks corroborate the overlap and dense-block boundaries.

For a short handoff, see the
[model-review brief](../../docs/strategy/paired-resource-cycle-review-2026-09-22.md).
