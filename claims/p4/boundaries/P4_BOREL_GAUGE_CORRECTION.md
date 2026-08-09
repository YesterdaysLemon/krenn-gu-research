# Borel-gauge correction for the resonant triangle

## Status

This note records a research-integrity correction made immediately
after the first flat-triangle checkpoint.

For a nonzero pure restriction, the factor on each local plane
`U_i` has an intrinsic kernel line `C y_i`.  A basis change may scale
`y_i`, scale the active complement, and shift

```text
x_i -> x_i+s_i y_i,
```

but it may not replace `y_i` by a vector with an active component.
The legal row group is therefore Borel.  Full row `GL_2` changes the
kernel line and does not preserve the purity flag

```text
dim span(Y,K,J)<=2,              X notin span(Y,K,J).
```

## Effect on the preceding checkpoint

The normal form

```text
y=(1,0,1,1),       x=(0,1,1,lambda)
```

is valid when the kernel row has one zero coordinate and the other
columns are otherwise distinct.  Its compound-matrix obstruction is
still exact, now recorded as
[`P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md`](rank-two-triangle/resonant/flat-kernel-zero-binary-cubic/P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md).

It is not the generic full-kernel-support normal form.  Consequently:

| Earlier claim | Corrected status |
|---|---|
| complete projective-column classification of the flat triangle | withdrawn as overstrong; replaced by the corrected support classification |
| dependent global rank-two-star obstruction | withdrawn as overstrong; subsequently reproved in marked charts |
| balanced-chart proof of the mixed `(2,2,1)` triangle | withdrawn; subsequently reproved in all Borel charts |
| balanced `2+2` displayed family and local coefficient identities | exact only in their stated marked charts |
| one-kernel-zero compound identity | exact boundary theorem |

The withdrawn records are conspicuously named:

- [`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md`](../../../P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md);
- [`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md`](../../../P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md);
- [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md`](../../../P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md).

## Repaired generic chart

If the kernel row has full support, diagonal source scaling and Borel
row gauge give

```text
y=(1,1,1,1),       x=(0,1,p,q),
pq(p-1)(q-1)(p-q)!=0.
```

The exact synchronizer and binary-cubic compound obstruction on the
dense finite-partner chart are proved in
[`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](rank-two-triangle/resonant/flat-generic-binary-cubic/P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md).

Thus the correction does not merely retract scope: it replaces the
invalid generic normalization with a valid two-modulus Borel theorem.
The projective partner sheets over that center are now classified as three
additive-parallelogram pure curves, all lying on the lower-pair-rank seam,
plus an empty double-infinity sheet:
[`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](../classifications/rank-two-triangle/resonant/flat-projective-partner/P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md).
The full-support affine-ratio collisions are now classified too: the
`2+1+1` and `3+1` active cubes vanish, while all four pure `2+2` seams have
a rank-two partner pair:
[`P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md`](../classifications/rank-two-triangle/resonant/flat-full-kernel-collision/P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md).
The smaller-kernel-support strata are now classified too.  They contain one
genuine support-two annihilator-line family rather than another
obstruction:
[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](../classifications/triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md).
The dependent star and mixed `(2,2,1)` arguments have now also been replaced
by Borel-legal proofs:
[`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](../classifications/star/rank-two-relation-star-obstruction/P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md)
and
[`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](rank-two-triangle/mixed/two-rank-two/P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md).
The honest unresolved boundary is instead the one-rank-two-edge mixed
triangle, other mixed-star patterns, and lower pair-image ranks.  The crossed
genuine support-two orientation of that triangle is now classified in
[`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](../classifications/triangle-211/crossed-211-triangle-support/P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md):
only the one-coordinate-overlap orbit survives at full source support, and it
is the first apolar component.  Common-factor/radical orientations,
support-one products, and lower pair ranks remain.

The first common-factor branch has now proved nonempty and component-sized:
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](../classifications/P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md)
certifies a six-dimensional eleventh component.  Its other orientations and
boundaries remain unclassified.
