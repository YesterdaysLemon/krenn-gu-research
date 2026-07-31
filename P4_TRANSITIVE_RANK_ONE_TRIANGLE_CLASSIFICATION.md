# Transitive rank-one triangles are a component-eleven boundary

## Status

**Exact characteristic-zero classification theorem.** Let three marked
planes of a nonzero pure `P_4` restriction have rank-three pair images whose
unique relations have the transitive rank-one orientation

```text
y_1 x_2=0,       y_1 x_3=0,       y_2 x_3=0.       (1)
```

Then the genuine support-two stratum lies in the closure of component
eleven.  Its support-one boundary is zero, while coincident-factor
boundaries have lower pair rank.  Consequently this Borel orientation
creates no eighteenth component.

Together with the cyclic-orientation theorem, this classifies both
tournaments carried by a triangle of rank-one pair relations.  It does not
classify exceptional graphs containing additional rank-one or rank-two
edges and does not prove component exhaustiveness for the whole pure-`P_4`
locus.

## Shared annihilator normal form

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).   (2)
```

A genuine two-coordinate linear zero divisor has a one-dimensional
degree-one annihilator.  At the source of two arrows in (1), this forces the
two annihilating rows to agree.  Applying the same observation at the middle
vertex forces all three products in (1) to be the same exact factor pair.
After source-coordinate scaling and legal Borel row shifts, put

```text
a=X_0+X_1,       c=X_0-X_1,
b=b_2 X_2+b_3 X_3,       d=d_2 X_2+d_3 X_3,         (3)

U_1=span(c, alpha*a+b),
U_2=span(c, a),
U_3=span(delta*c+d, a).                             (4)
```

Thus `c*a=0` is the common relation.  This normal form uses only row moves
that preserve each purity-fixed kernel line.

## A hyperbolic pairing is the whole determinant

Contract the three displayed modes against the missing mode.  Of the eight
covectors, only four can be nonzero.  The three that must vanish on `U_0`
are the rows

```text
r_000=(0,0,-2d_3,-2d_2),
r_100=(-S,S,-2b_3 delta,-2b_2 delta),
r_110=( S,S, 2alpha d_3,2alpha d_2),               (5)
```

where

```text
S=b_2 d_3+b_3 d_2.                                 (6)
```

The desired active covector is

```text
X=r_111=(0,0,2b_3,2b_2).                           (7)
```

The four maximal minors of the forbidden `3 x 4` matrix are

```text
4d_3 S^2,
4d_2 S^2,
4delta(b_2d_3-b_3d_2)S,
4delta(b_2d_3-b_3d_2)S.                            (8)
```

This is the useful translation: (8) is governed by the polarization of
squarefree multiplication on the complementary binary block.  The bilinear
form `(b,d) -> b_2d_3+b_3d_2` is hyperbolic.  Purity is therefore a null-cone
condition in a two-dimensional quadratic space, not a sixteen-coefficient
permanent calculation.

If `d` has genuine support two, the existence of a two-plane annihilating
(5) forces `S=0`.  Then `b` also has support two, and switching normalizes

```text
b=X_2+X_3,       d=X_2-X_3.                        (9)
```

On (9), (7) escapes the row span of (5) exactly when

```text
delta=0.                                           (10)
```

If `b,d` instead have support one, `S=0` forces them onto the same source
coordinate.  In that case `r_111=-r_000` after row normalization, so every
plane killing the forbidden all-kernel coefficient also kills the desired
coefficient.  The restriction is zero even though the three displayed pair
ranks can each equal three.  If either complementary factor vanishes, two
leaf planes coincide and the tuple is already on the lower-pair boundary.

## The survivor and its valuative placement

On the support-two branch (9)--(10), a dense chart of the apolar opposite
plane is

```text
U_0=span(a+p b, c+q b).                             (11)
```

Direct expansion gives only

```text
T_0111=4p,       T_1111=4q.                        (12)
```

The generic pair profile in edge order `01,02,03,12,13,23` is

```text
(4,3,4,3,3,3).                                    (13)
```

It remains to identify the containing component rather than merely exhibit
a pure family.  Apply the source sign change `X_1 -> -X_1`, which exchanges
`a` and `c`.  The target becomes

```text
U_0=span(a+q b,c+p b),
U_1=span(a,alpha*c+b),
U_2=span(a,c),
U_3=span(d,c).                                     (14)
```

For `epsilon!=0`, replace its third plane by

```text
U_2(epsilon)=span(a,alpha*c+epsilon*b).             (15)
```

This is the component-eleven normal form with projective parameter
`r=alpha/epsilon`, after the harmless block scaling
`diag(alpha,alpha,1,1)`.  Its Pluecker point tends to (14) as
`epsilon -> 0`.  Therefore the entire dense survivor (11) lies in component
eleven, and closure handles `alpha=0` and the remaining chart boundaries.

## Consequence

There are only two orientations of a tournament on three vertices.  The
cyclic one was classified by gain-graph switching; the transitive one is
classified here by a shared-annihilator hyperbolic pairing.  Thus a triangle
whose three exceptional pair relations all have coefficient rank one is no
longer an open source of an eighteenth component, subject only to the
support and additional-edge boundaries explicitly separated above.

## Exact replay

```text
uv run --with sympy python verify_p4_transitive_rank_one_triangle_classification.py
python audit_p4_transitive_rank_one_triangle_classification.py
```

The primary verifier checks (5)--(13), the support-one collapse, and the
symbolic Pluecker arc (15).  The independent audit recomputes contractions
by subset dynamic programming and replays the arc over exact rationals.  No
parameter search or graph enumeration is used.
