# Projective exhaustion of the overlapping mixed orientation

## Status

**Exact characteristic-zero marked-chart classification.**  The full
projectivized overlapping mixed-orientation chart is exhausted.  Its generic
rank-two contraction locus is the previously classified union of five
linear primes.  Its rank-one Springer fibres produce exactly two additional
component orbits, the support-star and support-path directed triangles in
[`P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md`](P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md).
The remaining rank-one line is the first apolar component.  Every genuine
point on the two projective leaf boundaries has a rank-two pair image or is
an embedded pure-`P_3` suspension.

Thus this entire exceptional-graph orientation contributes components
sixteen and seventeen, but no eighteenth component.  This is an exhaustion
of one marked orientation chart, not of the full pure-`P_4` variety and not
of the global Krenn--Gu problem.

## Homogeneous leaf chart

Use active/kernel row order on modes `1,2,3` and put

```text
x_1=(0,0,1,1),       y_1=(A,H,C,D),
x_2=(P,R,0,Q),       y_2=(-1,0,1,0),
x_3=(1,0,1,0),       y_3=(0,0,-1,1),               (1)
```

where

```text
[A:H:C:D] in P^3,       [P:R:Q] in P^2.            (2)
```

The line `A=H=0,C=D` is omitted because there `y_1` is proportional to
`x_1` and does not define a plane.  The second and third displayed planes
are always nondegenerate on (2).

The fixed zero products are

```text
x_1 y_3=0,       y_2 x_3=0.                        (3)
```

Contract every kernel-containing word in modes `1,2,3` to a covector on
mode zero.  Four contractions vanish because of (3); the remaining three
are the rows of

```text
M=
[ DR+HQ,       (A+C)Q+DP,       DR+HQ,       (A+C)R+HP ]
[ (C-D)R-HQ,  -AQ+(C-D)P,       AR+HP,      -AR-HP     ]
[ H,            A-C+D,          -H,           H         ]. (4)
```

The all-active contraction is

```text
X=(R,P+Q,R,R).                                      (5)
```

For fixed leaves, an opposite plane `U_0` gives a nonzero pure restriction
exactly when

```text
U_0 subset ker M,       X restricted to U_0 !=0.    (6)
```

Equivalently,

```text
rank M<=2       and       rank([M;X])>rank M.       (7)
```

The second inequality is the escape condition omitted by a bare
determinantal-base calculation.

## The affine interior and its four exceptional lines

On `H R!=0`, set `H=R=1`.  Away from `rank M=1`, the five minimal primes of
the four maximal minors are

```text
(C+P+Q,A+D),
(D+Q,A+C+P),
(C,A+D+P+Q),
(C-D+P-Q,A),
(C-D,A+P-Q).                                      (8)
```

Their generic rank-two kernels were classified in
[`P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md`](P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md):
they give the sixth mixed component twice, the old lower-pair sixfold, and
the split-cubic components `L_2,L_1`.

The `2 x 2` minors of `M` have the exact Groebner basis ideal

```text
I_1=(Q+D, P+A+C, D(A+C), A(C-D)).                  (9)
```

The two product equations in (9) split set-theoretically into exactly four
lines:

```text
S: A=D=0,       P=-C,       Q=0,

P_A: C=D=0,     P=-A,       Q=0,

P_D: A=C=0,     P=0,        Q=-D,

F: C=D=-A,      P=0,        Q=A.                  (10)
```

The third row of `M` is nonzero throughout the affine chart, so its kernel
is a three-space on every line.  Moreover `X` is not in the row span: its
zero/second coordinates are equal, whereas those of the third row of `M`
are opposite.  Therefore the complete opposite-plane fibre is

```text
Gr(2,ker M)=P^2.                                   (11)
```

On `S`, a Borel shift of `x_2` turns the three relations into

```text
y_1x_2=0,       y_2x_3=0,       x_1y_3=0
```

with support labels `12,02,23`, the source-coordinate star.  This is
component sixteen.  The two lines `P_A,P_D` give the same directed pattern
with path labels.  They are symmetry equivalent: source swap `0<->3`, then

```text
diag(-1,1,1,-1),
```

together with mode swap `1<->2`, sends `P_A` to `P_D`.  Their common orbit is
component seventeen.

On `F`, the relation-rank word is `(2,1,1)`, and the two rank-one support
labels are adjacent.  The crossed-triangle support theorem
[`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md)
identifies its full-support part and its apolar `P^2` with the first
component.  The common point of the four lines is contained in their
closures and creates no further component.

Thus the vertical fibres over the singular determinantal base are fully
accounted for.  This is precisely the step that the earlier five-prime
classification could not see.

## Boundary `H=0, R!=0`

Set `R=1` and put

```text
L=A-C+D.
```

The four maximal minors of `M` are

```text
-D L^2,
 C L(A+C-D),
 0,
-A L(A+C+D).                                      (12)
```

Hence the rank-two locus is the union of

```text
L=0                                                (13)
```

and the residual plane

```text
D=0,       A+C=0.                                 (14)
```

On (13), if `AC!=0`, then exactly

```text
X=(row_1(M)+row_2(M))/C,                           (15)
```

so every allowed `U_0` annihilates `X` and the full tensor is zero.  If
`A=0,C!=0`, then `X=row_1(M)/C`, with the same conclusion.  The point
`A=C=0` makes `y_1=0` and is not a plane.  The only genuine part of (13) is

```text
C=0,       A!=0,       D=-A.                       (16)
```

There `rank M=1`, `X` escapes, and the fixed pair `U_1U_3` has rank two.

On (14), plane nondegeneracy forces `A!=0`; the augmented contraction matrix
has a `3 x 3` minor `-4A^2`, so the tensor genuinely escapes.  Again
`dim(U_1U_3)=2`.  The lower-pair exhaustion theorem therefore puts every
nonzero point of this boundary in one of its four known closures.

## Boundary `R=0, H!=0`

The maximal minors now factor simultaneously as

```text
(P-Q)(P+Q) H^2 (D,-C,-H,-A).                       (17)
```

Since `H!=0`, the rank condition is exactly `P=Q` or `P=-Q`.

- On `P=-Q`, equation (5) gives `X=0`, so the full tensor is zero.
- On `P=Q!=0`, the tensor can escape, but `dim(U_2U_3)=2` identically.

Thus the genuine ruling is again already covered by the lower-pair
exhaustion theorem.

## The corner `H=R=0`

All three leaf planes now lie in the source-coordinate hyperplane

```text
z_1=0.                                             (18)
```

Every row of `M` and the covector `X` is a multiple of `z_1^*`.  If `M` is
nonzero, either `X=0` or `X` lies in its row span, so the tensor vanishes on
every allowed `U_0`.  A nonzero pure restriction is possible only when

```text
M=0,       P+Q!=0.                                 (19)
```

Then the restriction to the three leaf modes has only its all-active
coefficient.  The fourth plane supplies the missing coordinate exactly as
in
[`P4_EMBEDDED_P3_PURE_COMPONENT.md`](P4_EMBEDDED_P3_PURE_COMPONENT.md).
Hence every genuine corner point is an embedded pure-`P_3` suspension.

## Consequence

Combining (8)--(19) gives a complete finite list for this projective marked
orientation:

```text
rank-two affine base  -> components 6, 7, L_1, L_2,
rank-one affine fibre -> components 16, 17, or component 1,
H/R boundary          -> lower-pair closures or zero,
H=R=0 corner          -> embedded P_3 closure or zero.          (20)
```

There is no unclassified normalization divisor and no extra vertical
component in this chart.

## Exact replay

```text
uv run --with sympy python verify_p4_overlapping_mixed_orientation_projective_exhaustion.py
python audit_p4_overlapping_mixed_orientation_projective_exhaustion.py
```

The primary verifier reconstructs (4)--(5) from permanents, proves the
rank-one Groebner basis and four-line split, checks the exact path symmetry,
and verifies every boundary factor and pair-rank claim.  The independent
audit uses a separately implemented subset-DP permanent, rational-free row
reduction over `F_101,F_103`, and direct Pluecker comparison.  Both are
fixed-size symbolic proof replays; neither searches graphs or parameter
grids.
