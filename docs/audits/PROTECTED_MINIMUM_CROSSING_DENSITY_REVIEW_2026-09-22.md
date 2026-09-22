# Independent audit: strict crossing density for a full protected source

Date: 2026-09-22

Verdict: **PASS for the full-source equality branch.** A nonfatal
paired-depth error in a precursor was corrected before the assembled owner
was audited. The audited implication is:

> For `k>=2`, a protected unit-K4 hollow array over `C` satisfying every
> full GHZ source coefficient equation cannot have exactly `6k` supported
> crossing scalar entries.  Since the macro equations already force at
> least `6k`, every such hypothetical full source has strictly more than
> `6k` crossings.

This is a crossing-density theorem inside the protected unit-K4 setting.  It
does not exclude denser full sources, prove SFULL, prove WP1, or resolve the
global Krenn--Gu conjecture.

Final assembled owner theorem reviewed:

```
claims/arbitrary-order/PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md
SHA256 9D29FABCD8031FED978B1E2FBB17EB4D55CAEE273594D3EC49DC615E40E7F6E6
```

At this hash the owner document contains the corrected global paired-depth
formula, preserves the WP1/WP2/full-source distinction, and introduces no
holonomy, adjacent-hidden, or finite-order dependency into the proof.

## 1. Inputs and independence

The audit checked the following separately owned arguments:

* the `6k` lower bound and equality gadget normal form, now in owner
  Section 2;
* the no-literal-triangle lemma, now in owner Section 3;
* the full-source hidden-literal row, now in owner Section 5; and
* the complete protected-edge-pairing exclusion in
  `claims/arbitrary-order/PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md`.

The derivations below recheck the logical interfaces rather than inferring
the composite statement from filenames or status labels.
Two separate Sol-agent reviews in the same research session accepted the
assembled mathematical chain. This is not independent human refereeing or
formal kernel checking. The owner hash above precedes only the final status
promotion and audit/review navigation links; its mathematical text is unchanged.

## 2. Equality normal form and literal graph

For each ordered incidence `(A,a|c)`, the singleton macro word with `A=a`
and every other component `c` needs a nonprotected matching.  Hollowness
forces it to cross the four-vertex cut of `A`; cut parity supplies at least
two entries.  Double counting the `6k` incidences gives at least `6k`
supported crossing entries.

At equality every incidence has exactly two entries.  They must form a
bijection between one `M_a(A)` edge and one `M_c(B)` edge, and their product
is `-1`.  Reciprocal incidences pair the entries into `3k` actual gadgets.
Thus the literal graph `F` on `(A,a)` is 2-regular, with exactly one neighbour
of each other colour at every literal and no intracomponent edge.

Any component-colour transversal enabling no edge of `F` has exactly its
protected matching and coefficient one.  Hence the mixed macro equations
imply that the only independent transversals are the three constant colour
classes.  This direction needs no ladder or weight formula.

## 3. Independent check of the no-triangle lemma

Orient the three bichromatic perfect matchings as permutations

```
p=sigma_01,  q=sigma_02,  r=sigma_12,
(A,0)--(p(A),1), etc.
```

The binary `0/1` restriction shows that `p` is a single `k`-cycle.  If it
had two orbits, colouring a nonempty proper union of orbits `0` and its
complement `1` would be a mixed independent transversal; edges involving
colour 2 would be inactive.

Suppose a literal triangle exists:

```
(A,0)--(B,1)--(C,2)--(A,0).
```

Then `B=p(A)` and `C=q(A)=r(B)`.  On the directed `p`-cycle assign colour
zero to the arc from `B` through `p^-1(C)`, assign colour two to `C`, and
assign colour one to the arc from `p(C)` through `A`.

There is no selected `01` edge because the cyclic pattern has no directed
`0 -> 1` transition.  The only selected 2-literal is at `C`; its unique
`q`-predecessor is `A`, coloured 1, and its unique `r`-predecessor is `B`,
coloured 0.  Hence there is no selected `02` or `12` edge either.  Both arcs
are nonempty and `C` has the third colour, so this is a nonconstant
independent transversal, contradiction.  The proof also covers `k=3`; for
`k=2` three pairwise distinct physical components cannot form the triangle.

The lemma uses only macro rigidity and the equality literal graph.  Endpoint
maps, weights, and split/transit marks play no role.

## 4. Independent check of the hidden full-source row

The two-exception macro argument says that a transit literal outside a
literal triangle has both neighbours in one physical component.  Since
triangles are now impossible, every transit literal is hidden.  Normalize
it as `(A,a)` with neighbours `(B,b),(B,c)`.

The empty-q1 row first forces the common-star alignment.  Without it, the
two unshared neighbour ports map to different endpoints of the reused
`M_a(A)` edge and give the already established unique q1 matching.

Under alignment, name the shared `B` port `u`; the two gadget maps send `u`
to one root endpoint `s` and their unshared ports to the other root endpoint
`p`.  Use the word

```
A: aaaa,
B: b at u and c at the other three ports,
every exterior component: aaaa.
```

There is exactly one matching: the shared `a-b` lane `s--u`, the unshared
`a-c` lane from `p`, the complementary protected `M_a(A)` edge, the
complementary protected `M_c(B)` edge, and exterior protected matchings.
The other lane of each displayed gadget has the wrong target colour.  The
literal `(A,a)` has no third gadget.  At `(B,b)` the unused gadget has
foreign colour `c`, and at `(B,c)` the unused gadget has foreign colour `b`;
neither colour occurs outside `B`.  Reciprocity also rules out an exterior
`a` gadget reaching those states, because their unique `a`-neighbour is
already `(A,a)`.  Hollowness removes exterior `a-a` crossings.  The sole
coefficient is therefore a nonzero product of supported entries, contrary
to the mixed full-source target zero.

This checks uniqueness in the whole array, not only on `A union B`, and it
does not require the two neighbour literals to be split.

### Paired-depth correction

For normalized `(a,b,c)=(0,1,2)`, an early precursor displayed `(2,3,2)`. That is
the `k=2` or local `A union B` vector.  Every one of the `k-2` exterior
components is uniformly colour 0 and contributes two complete minority
pairs to both `q_1` and `q_2`.  The global vector is

```
(q_a,q_b,q_c) = (2, 2k-1, 2k-2),
```

up to interchanging `b,c`.  Its minimum is still exactly two.  This does
not change the full-source contradiction or the stated reason WP1 cannot
use this row.
The assembled owner already uses the corrected global vector.

## 5. Composite conclusion

The no-triangle lemma and hidden-row contradiction eliminate every transit
literal.  Therefore both gadgets at every `(A,a)` use the complementary
edges of `M_a(A)`.  Each of the `6k` protected coloured edges occurs in
exactly one gadget, so the equality array is exactly a complete
protected-edge pairing with nonzero crossing weights.

The published cubic matching theorem applies with all hypotheses intact:
different gadgets use disjoint state resources, gadgets join different
colours and physical components, and every crossing entry is nonzero.  It
supplies a mixed physical word with one supported matching and hence a
nonzero coefficient.  This contradicts the full source.  Combined with the
lower bound, equality is impossible and the crossing count is strictly
greater than `6k`.

For WP1, only the no-triangle step transfers.  The hidden separator has
minimum paired depth two, and the cubic theorem does not bound the depth of
its additional matching.  The minimum-density WP1 equality parent therefore
remains open.

## 6. Exact replay receipts

All commands exited zero:

```
python -X utf8 claims/arbitrary-order/verify_protected_minimum_crossing_normal_form.py
python -X utf8 claims/arbitrary-order/verify_protected_literal_triangle_witness.py
python -X utf8 claims/arbitrary-order/verify_protected_pair_gadget_cubic_bridge.py
python -X utf8 claims/arbitrary-order/audit_protected_hidden_crossing_words.py
```

The triangle replay checked 11,618 literal triangles across all deranged
permutation pairs through `k=6`.  This corroborates the all-order proof; it
does not replace it. The separately reviewed symbolic hidden calculation
recovered the separator coefficient `-x/z`; the tracked full-array replay
checks the global word. The cubic replay recovered the physical
word/perfect-matching correspondence on its frozen controls.  No process
remains running.

The final full-array hidden replay also passed all 768 constructed arrays:
384 misaligned q1 cases and 384 aligned q2 cases, over `k=2,3,4,7`, every
colour order, every local resource choice, both local orientation bits, and
exact rational nonzero weights.  Its reviewed hash is

```
claims/arbitrary-order/audit_protected_hidden_crossing_words.py
SHA256 F375D55E9A236782CADBA6D453E3D79A74DB0E8CDB06A8F49A18FAC93CFFF192
```

The replay varies exterior choices nontrivially but is not used as an
exhaustive exterior-allocation proof; Section 4 supplies the full-array
uniqueness argument independently of those choices.
