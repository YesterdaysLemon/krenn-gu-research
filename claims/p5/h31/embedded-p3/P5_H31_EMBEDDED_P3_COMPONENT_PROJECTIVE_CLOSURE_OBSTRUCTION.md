# Projective closure of the ninth component is empty for `H31`

## Status

This is an exact characteristic-zero theorem on the full projective
closure of the embedded-`P_3` ninth pure-`P_4` component.

Every point of that component with nonzero pure `P_4` restriction has
empty marked `H31` fibre.  The points at which the pure restriction is
zero cannot occur as the required pure root contraction.  Consequently
the ninth component is now closed in full for `H31`, not merely on one
affine normalization.

The proof is intrinsic and uses no elimination.  The apparent
projective boundary is only the change of common-coordinate chart for
the projective normal triple of the embedded pure `P_3`.  Every
nonzero point is carried by source and mode symmetry into the affine
`B!=0` chart already excluded.

This theorem does not prove that the nine known pure-`P_4` components
are exhaustive, close the special boundaries of the other known
components, produce a prize graph, or resolve the global Krenn--Gu
conjecture.

## Homogeneous sign-rectangle base

The last three planes lie in the source hyperplane `X_0=0`.  Their
projective normals form one oriented three-vertex face of a sign
rectangle.  Homogeneously write them as

```text
n_1=(C, A, B),
n_2=(C,-A,-B),
n_3=(C,-A, B),                                    (1)
```

with

```text
[C:A:B] in P^2.                                   (2)
```

The other five oriented faces are obtained by permuting the three
tensor modes.  Thus (2), rather than a single rational parameter
`B`, is the intrinsic compactification base.

On the chart `C!=0`, bases

```text
(-A,C,0), (-B,0,C);
( A,C,0), ( B,0,C);
( A,C,0), (-B,0,C)                                (3)
```

give exactly two nonzero restricted `P_3` coefficients:

```text
T_100= 2 A C^2,           T_101=-2 B C^2.         (4)
```

After setting `C=1`, this is the affine sign chart used in the
component theorem.

## Support one is the zero restriction

If only one of `C,A,B` is nonzero, the three normals in (1) are the
same projective coordinate normal.  Hence the last three planes are
one common coordinate plane.  The restriction of `P_3` to their
triple product is zero.  Since the embedded component satisfies

```text
P_4(z,-,-,-)=z_0 P_3(-,-,-),                      (5)
```

the pure `P_4` restriction is zero as well.

A root contraction producing `Delta_3` must be a nonzero pure tensor.
Therefore the three support-one points of (2) are not admissible
marked fibres.

## Every nonzero projective point enters the closed affine chart

Now suppose the restriction is nonzero.  By (4) on each
common-coordinate chart, or equivalently by the pure-`P_3`
classification, at least two coordinates of `[C:A:B]` are nonzero.

Choose two such coordinates.  A source-coordinate permutation sends
one to the common-coordinate slot `C'` and the other to the sign
parameter slot `B'`.  Rescale projectively to obtain

```text
C'=1,             B'!=0.                          (6)
```

Signed source-coordinate changes and a permutation of the last three
modes restore the oriented face in (1).  They preserve the permanent
up to an overall nonzero scalar and preserve the `H31` signature.
The free mode-zero plane remains an arbitrary two-plane under the same
source symmetry.

Thus every nonzero point of the projective closure is symmetry
equivalent to a point of the complete affine family

```text
B'!=0.
```

That whole family is empty for `H31` by the union of:

- [`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md);
- [`P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md);
- [`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md).

This proves the projective closure theorem.

## Cross-specialty interpretation

The relevant compactification is the projectivized absolute normal,
not the closure of one matrix chart.  In oriented-matroid language,
the boundary records only which coordinates of the sign vector
vanish.  In toric language, the three coordinate points are zero
orbits and every positive-dimensional coordinate orbit meets a
two-coordinate affine chart.  This is why the apparent boundary
disappears after passing from row-reduced matrices to projective
normal triples.

The sign-rectangle viewpoint is also a small instance of the
second-hypersimplex/Grassmannian dictionary: Pluecker boundary charts
are best glued by support data rather than by limits of inverse pivot
coordinates.  See the tropical and matroidal treatment of the second
hypersimplex in
[Herrmann--Joswig](https://arxiv.org/abs/0804.2897).  No theorem from
that paper is required here.

## Verification

Run

```text
python verify_p5_h31_embedded_p3_component_projective_closure.py
python audit_p5_h31_embedded_p3_component_projective_closure.py
```

The primary verifier reconstructs (4), checks the three support-one
zero restrictions, and proves that every remaining support mask can
be permuted into (6).  The independent modular audit enumerates all
projective normal points over two finite fields and replays the same
chart cover without importing the primary implementation.  The
finite-field audit is corroboration only; the theorem is the
characteristic-zero symmetry argument above.
