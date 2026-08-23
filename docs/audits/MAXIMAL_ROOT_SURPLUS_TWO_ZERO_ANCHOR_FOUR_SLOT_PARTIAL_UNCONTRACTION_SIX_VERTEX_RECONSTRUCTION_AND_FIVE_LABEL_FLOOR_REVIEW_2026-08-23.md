# Hostile review: zero-anchor four-slot partial uncontraction and five-label floor

## Verdict

**ACCEPT after a mandatory quantifier correction, three independent hostile
derivations, focused exact verification, genuinely independent no-import
audit, and authenticated six-vertex dependency replay.**

`GLS54` proves that every actual characteristic-zero zero-anchor hypothetical
witness has at least five effective auxiliary labels at every fully supported
residual point.  It does not assume full swallow.  If at most four labels are
effective, pad them to four with inactive promoted ports, retain every active
residual vertex as an open physical vertex, and partially contract the full
graph identity.  The result is a reconstructed legal six-vertex graph with a
fully supported weighted GHZ target, excluded by the accepted six-vertex
theorem.

The original attack idea was rejected when phrased as reopening variables
from one abstract fixed-residual equation.  `GLS36` explicitly warns that one
such equation does not imply the residual family.  The accepted theorem
instead starts from an actual complete uncontracted witness, then fixes the
residual point, defines activity, and partially contracts the full identity.

This is an activity floor, not a response, selector, synchronization,
nuisance-survival, source-coverage, or attachment theorem.  Five-plus-label
zero-anchor points, every nonzero-anchor branch, the strategic node, and the
global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts and interfaces

- [`GLS54 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_SLOT_PARTIAL_UNCONTRACTION_SIX_VERTEX_RECONSTRUCTION_AND_FIVE_LABEL_FLOOR_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_slot_partial_uncontraction_six_vertex_reconstruction_and_five_label_floor.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_slot_partial_uncontraction_six_vertex_reconstruction_and_five_label_floor.py)
- owning complete identity `GLS8`
- auxiliary-label interface `GLS39`
- fixed-equation scope warning `GLS36`
- special-case reconstruction `GLS53`
- accepted
  [`six-vertex theorem`](../../claims/finite/n06/SIX_VERTEX_CERTIFICATE.md)
- current-frontier, node-DAG, and arbitrary-order README updates.

The three hostile reviews separately reconstructed the full source, audited
the pointwise/full-domain quantifier distinction, and analyzed both
residual-containing four-label support types.  All agreed on the corrected
full-witness theorem and the stronger inactive-promoted padding extension.

## Quantifier and partial-uncontraction audit

The legal order of quantifiers is:

1. start with one actual graph satisfying the complete GHZ tensor equality;
2. choose the maximum-root promoted chart with probe pair `A` and residual
   pair `Q`;
3. fix fully supported residual vectors `z_Q`;
4. define pointwise residual activity and whole-domain promoted activity;
5. choose the four-set `P` and partially evaluate the complete identity.

It is not legal to begin with only the already evaluated `GLS36` equation
and then vary a residual vertex.  The theorem does not do that.

For an inactive promoted label `u`, both physical maps

```text
W_(a_0,u), W_(a_1,u)
```

vanish on the whole local domain.  Such a port can safely be left open as a
padding vertex: every incident root-pair companion is still zero, while its
GHZ target factor remains open.

For an inactive residual `q_s`, only the evaluated shores

```text
W_(a_0,q_s)(-,z_(q_s)), W_(a_1,q_s)(-,z_(q_s))
```

are known to vanish.  The full maps may be nonzero transversely.  Hence an
inactive residual is always kept contracted at its defining `z_(q_s)` and is
never used as padding.  An active residual is left open only because it is
retained directly from the original complete identity.

The primary and independent audits both include exact maps that kill
`z=(1,1,1)` but act nontrivially on `(1,0,0)`.  This countercontrol rejects
the tempting but invalid rule “fixed-point inactive implies whole-map zero.”

## Padding and exhaustive support audit

Write

```text
s=|Act intersect Q|,     p=|Act intersect Uhat|,
m=s+p<=4.
```

There are `2r-2-p` inactive promoted labels, while padding requires `4-m`.
The surplus is

```text
2r-6+s>=0.
```

Thus every activity set of size at most four extends to a four-set

```text
P superset Act
```

using inactive promoted labels only.  Put `C=Bhat-P`, leave `P` open,
contract residual vertices of `C` at their defining vectors, and contract
promoted vertices of `C` at all ones.

Every raw pair `D not subset P` meets `C`.  Its contracted endpoint is
inactive: a promoted endpoint contributes a zero whole map and a residual
endpoint contributes two zero evaluated shores.  Therefore its root
companion vanishes.  This is exhaustive even when both endpoints lie in
`C`, and it includes the residual pair `Q` whenever one residual is outside
`P`.  The top term vanishes because `omega=0`.

For each surviving `D subset P`, the physical complement is

```text
Bhat-D=C union (P-D).
```

After the declared `C` contraction it is a bilinear tensor on the two
vertices of `P-D`.  This is a legal effective edge block.  Zero blocks and
terms incident with padded vertices are retained as zero; no nonzero deck or
rank gate is assumed.

At `r=3`, `Bhat` has six vertices and `C` has two.  The open four-set may
contain zero, one, or two residual vertices and respectively four, three, or
two promoted vertices.  The proof and both audits cover all three types.

## Matching, target, and field audit

On `A union P`, set the probe edge to zero, retain the original physical
probe--`P` blocks, and use each contracted complement as the corresponding
`P`--`P` edge.  Of the fifteen six-vertex matchings, three use the zero probe
edge.  The other twelve group into six unordered probe-target pairs and two
orientations, exactly the six remaining raw labels.  There is no multiplicity
or transpose defect.

Contracted inactive promoted vertices contribute one to every pure target
coefficient.  A contracted residual contributes its colour coordinate,
which is nonzero on the fully supported residual torus.  Open active or
padded vertices remain pure-colour slots.  Hence all three reconstructed
target weights are nonzero.  One invertible diagonal scaling at one probe
normalizes them without creating mixed coefficients.

For an arbitrary characteristic-zero field, all used coefficients and
weight inverses generate a finitely generated extension of `Q`, which embeds
injectively in `C`.  This preserves equations and nonvanishing, so the
accepted complex six-vertex theorem applies.

## Authenticated dependency replay

The historical six-vertex certificate bundle was read from the protected
authority checkout without editing it.  The current-main verifier wrote its
audit outside every repository:

```text
python claims/finite/n06/verify_six_vertex_final.py \
  --base C:\Users\Yeste\OneDrive\Documents\open-graph-theory-with-prize \
  --output C:\w\kg-gls54-six-vertex-dependency-audit-20260823.json
```

```text
GLS54 base HEAD:              ccab541ce38a91dbb9e1deb52d9282a94767c15d
authority checkout HEAD:      a16315f145324b503c3ec0ccd017ee7562f9626d
six-vertex theorem SHA-256:   63d41774e2a8c45ded67cb949b920c34d0cabb499ba6c215423dc274686066c4
top verifier SHA-256:         e383454d167b8d0cc7c35d6c56fb69fe7d302c2ca15d5d234047016c783a889e
replay output SHA-256:        2e539db1802048560e7e18c8bc69c5e1274ffd7883863e33dbe1551070de67b7
verified:                     true
CNF SHA-256:                  154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7
DRAT proof SHA-256:           9273c872b3aa071e67b3ff176d84c50d104e212bcab38980be38de69f9ffb1d1
```

The theorem document and verifier hashes agree between current main and the
authority bundle.  No protected checkout or process was modified.

## Computational independence

The primary verifier uses SymPy, forward support traversal, symbolic matrix
annihilation, direct perfect-matching enumeration, exact rational target
weights, and explicit complement sets.

The independent audit imports no project code or algebra package.  It uses a
bit-mask hafnian with sparse monomial dictionaries, reverse root-order and
support traversal, exact `F_101` physical maps, and its own target-weight
census.  Its inactive-residual countercontrol has nonzero transverse action
despite zero chosen shores.  The two implementations therefore differ in
representation, traversal, arithmetic, and matching algorithm.

The written proof, not either finite test range, carries arbitrary root order
and characteristic zero.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_slot_partial_uncontraction_six_vertex_reconstruction_and_five_label_floor.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_slot_partial_uncontraction_six_vertex_reconstruction_and_five_label_floor.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_promoted_label_six_vertex_reconstruction_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_promoted_label_six_vertex_reconstruction_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
```

The package must still pass full candidate-tree validation, exact-head hosted
CI, safe merge, and fresh merged-main replay before publication is complete.

## Unresolved boundary

The theorem raises only the zero-anchor activity floor.  It gives no
information about how five or more active labels' physical decks combine,
whether any named response is nonzero, whether a constant normalized selector
survives the complete nuisance, whether projective quotient lines synchronize,
or whether any target-pure anchor and downstream gate hold.

Full-swallow source coverage is not needed for the floor, but it remains open
for attachment routes.  Raw escape is not attached.  Nonzero marginal and
double-transverse anchors remain open.  The strategic node and global
conjecture remain **UNRESOLVED**.
