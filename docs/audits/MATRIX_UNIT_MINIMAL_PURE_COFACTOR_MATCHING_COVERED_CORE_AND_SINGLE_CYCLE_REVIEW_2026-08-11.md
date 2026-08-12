# Hostile review: minimal pure-cofactor matching-covered core

Date: 2026-08-11

Reviewed artifact:

[`../../claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md)

Review disposition: **PASS at the stated least-residual structural scope**.

The Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact claim under review

The theorem starts with a least-cardinality even principal pure shore `R`
whose hafnian is zero although its support has a perfect matching.  It claims:

1. the nonzero first-cofactor graph is exactly the union of all support
   perfect matchings;
2. minimality forces that allowed-edge graph to be connected and
   matching-covered;
3. every allowed edge lies on an alternating cycle relative to any fixed
   perfect matching;
4. the old 2-regular branch is one even cycle with exactly two matching
   monomials, a primitive signed relation, and monomial first cofactors; and
5. the branching branch has at least three perfect matchings, cyclomatic rank
   at least two, and positive even branching excess.

It does not claim that either branch is contradictory or that branching
automatically enters the deeper-blocker component.

## 2. Adversarial proof checks

### 2.1 Does a nonzero cofactor really imply an allowed edge?

Yes.  If `C_ij=z_ij h(R-{i,j})` is nonzero, the edge is supported and the
complementary hafnian is nonzero.  A nonzero finite sum of matching monomials
requires at least one nonzero term, so the complement has a support perfect
matching.  Adding `ij` makes it a full support perfect matching.

### 2.2 Does an allowed edge really have a nonzero cofactor?

Yes, and least cardinality is load-bearing.  A perfect matching containing
`ij` leaves a support perfect matching on the proper even subset
`R-{i,j}`.  If that complementary hafnian vanished, it would be a smaller
supported cancellation.  Thus it is nonzero.

Without least-residual selection, this converse can fail.  The theorem never
applies it to an arbitrary vanishing shore before minimalization.

### 2.3 Is the active graph the full support graph?

Not necessarily.  It is the allowed-edge subgraph.  A support edge can have
no perfect-matching complement and therefore zero first cofactor for purely
combinatorial reasons.  Both checkers include a nonzero chord of this type.
The theorem retains rather than deletes such support edges and makes no claim
about physical-support removal.

### 2.4 Can inactive edges invalidate component factorization?

No.  Every full perfect matching uses only allowed edges by definition and
therefore stays inside allowed-core components.  Conversely, combine any
support perfect matching from each component.  Their union is a full support
perfect matching, so every used edge is automatically allowed.  Hence the
full matching set is exactly the Cartesian product of the component matching
sets, and the weighted hafnian factors.

An edge crossing two purported allowed-core components cannot occur in a
full perfect matching; if it did, it would be allowed and join them.

### 2.5 Why does factorization force connectedness?

The fixed perfect matching restricts to every allowed-core component, so each
component has positive even order and supports a perfect matching.  The
product of their hafnians is zero over a field, so one component hafnian is
zero.  If more than one component existed, that component would be a proper
smaller supported cancellation, contradicting minimality.

### 2.6 Does every allowed edge lie on a fixed-matching alternating cycle?

Yes.  For an edge outside the fixed matching, compare with a perfect matching
containing it.  For an edge inside the fixed matching, minimum degree two
supplies another allowed edge at one endpoint; compare with a perfect
matching containing that other edge.  The relevant symmetric-difference
component contains the original fixed-matching edge.  Perfect-matching
symmetric differences are disjoint alternating even cycles.

### 2.7 Why is the degree-two branch one cycle rather than many?

A finite 2-regular graph is a disjoint union of cycles, but connectedness has
already been proved.  The fixed perfect matching forces the unique component
to have even length.

### 2.8 Could support chords create additional matching terms in the cycle branch?

No.  Every edge of any full support perfect matching is allowed, while the
allowed graph is exactly the cycle.  Therefore the only full matchings are
the two alternating halves of that cycle.  A support chord may remain, but it
belongs to no full perfect matching.

### 2.9 Are the first cofactors in the cycle branch really monomials?

Yes.  Delete the endpoints of a cycle edge.  The remaining cycle path has one
perfect matching.  Any alternative support matching of that complement,
when joined to the deleted edge, would give a full matching containing an
edge outside the allowed cycle.  Thus no alternative exists.  For an
off-cycle support edge, the complementary support has no perfect matching at
all, by the definition of allowedness.

### 2.10 Is the signed exponent primitive?

Yes.  The two alternating matchings are edge-disjoint and their incidence
difference has entries `+1` and `-1`.  Its coordinates have greatest common
divisor one.  No saturation or root extraction is hidden in the relation.

### 2.11 Why must the branching branch have at least three matchings?

One matching would make the allowed graph a degree-one matching.  With only
two matchings, their union is a disjoint union of shared matching edges and
alternating cycles.  Minimum degree two removes shared isolated edges, and
connectedness leaves one cycle.  Therefore a noncycle core has at least three
perfect matchings.

### 2.12 Are the cyclomatic and branching-excess bounds exact?

Yes.  A connected graph of minimum degree two that is not 2-regular has a
positive even degree excess

```text
sum_v(deg(v)-2)=2(|E|-|V|)=2(beta-1)>=2.
```

Thus `beta>=2`.  The excess is realized either at a degree-at-least-four
vertex or at two or more degree-at-least-three vertices.  The theorem does
not infer a bounded graph size from this local alternative.

### 2.13 Does branching force a deeper blocker?

No.  This was the main scope hazard.  The branching edges are pure-colour
allowed edges with nonzero complementary hafnians.  Existing deeper-blocker
theorems concern additional root/killer incidence data not supplied by the
cofactor graph alone.  The reviewed theorem records the connected multi-cycle
exchange core as the next input; it does not promote it to deeper entry.

## 3. Evidence independence

The primary verifier uses tuple-recursive perfect matchings and exact rational
hafnians.  It checks:

- a least cancelling six-cycle with one nonzero inactive chord;
- equality of allowed and active-cofactor edges;
- exactly two cycle matchings and six unique first cofactors;
- primitive exponent data and alternating Euler rows;
- a connected branching `K_4` with three matchings and cyclomatic rank three;
- a disconnected nonminimal cancellation whose hafnian factors before the
  least component is selected.

The independent audit imports no repository module and no symbolic algebra
package.  It uses edge and vertex bitmasks, independently enumerates matching
masks, performs Fraction arithmetic and unsigned-incidence row reduction, and
uses different six/eight-vertex weights.  It independently recovers the
allowed core, inactive chord, unique cofactors, branching kernel dimension,
and least connected component.

The finite examples test mechanisms and sharpness.  The arbitrary-order
claims rest on the support and factorization proofs.

## 4. Remaining boundaries

The theorem leaves open:

- inconsistency of the primitive pure-cycle relation with active mixed data;
- forcing a target-lattice unit from that relation;
- converting the connected branching exchange core into a deeper blocker;
- classifying larger matching-covered branching cores;
- aggregate active-cycle fibres;
- arbitrary exclusion of the complete nonzero `r=1` matrix-unit branch; and
- the global conjecture.

No finite sharpness model is presented as a witness or counterexample.

## 5. Verdict

The theorem is accepted as an exact arbitrary-order refinement of the pure-
cofactor proof-DAG edge.  It closes the disconnected-cycle ambiguity and
replaces generic phase branching by a connected matching-covered exchange
core with quantified excess.  The next load-bearing step must couple one of
these structures to mixed response or deeper-blocker data.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
