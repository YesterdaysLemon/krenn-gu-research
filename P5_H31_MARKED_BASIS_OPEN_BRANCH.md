# A marked-basis branch over the known pure-compression component

## Status

This is an exact characteristic-zero scope correction and obstruction.

The known five-dimensional component records four **planes**
in `Gr(2,4)^4`.  An `H31` local map contains more data: in each plane
it marks a kernel row and a complementary pure-colour row.  Adding a
multiple of the kernel row to the pure-colour row preserves the pure
`P_4` deletion, but it is not a symmetry of `Delta_2`.

Consequently, excluding one displayed row basis over every plane does
not by itself exclude the plane component.  The distinction is real:
on a dense open subfamily with `L!=0`, the canonical marking has no
binary `Delta_2` extension, while an explicit shifted marking on the
same four planes does have one.

The shifted branch still has no ternary `H31` lift: a one-marked map is
injective and the usual transverse-coordinate argument forces a third
target row to vanish.  This theorem closes that branch.  The subsequent
classification in
[`P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`](P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md)
now closes every marking over the finite family chart; projective
boundary planes remain separate.

## The same four planes with different markings

Normalize the known family to `E=I=1`, and put

```text
D=C+L,
A=1+LQ,
B=1+DQ.                                               (1)
```

Assume

```text
L Q D A B !=0.                                        (2)
```

Use the kernel rows

```text
alpha_0=(1,Q,0,-A)
alpha_1=(L,1,-L,-L)
alpha_2=(-1,0,1,0)
alpha_3=(0,0,-1,1)                                   (3)
```

and the canonical pure-colour rows

```text
U_0=(0,1,D,C)
U_1=(0,0,1,1)
U_2=(0,1,0,L)
U_3=(1,0,1,0).                                       (4)
```

Now shift only the pure-colour rows:

```text
t=(-1/Q,0,L/A,0),
beta_r=U_r+t_r alpha_r.                              (5)
```

For every mode,

```text
span(alpha_r,beta_r)=span(alpha_r,U_r),              (6)
```

so (5) is exactly the same point of `Gr(2,4)^4` as the
canonical family.  Nevertheless it is a different marked local map.

Direct permanent expansion gives only

```text
coefficient(BBBB)=2D                                 (7)
```

on the pure hyperplane.  Thus (5) remains a nonzero pure compression.

## A binary `Delta_2` extension off `L=0`

Choose source coordinate `q=2` as the distinguished pure coordinate.
Delete it, retain source coordinates `(0,1,3)`, and append the fifth
source coordinate with entries

```text
x=(1,0,0,-1),
y=(B/Q,1,0,0).                                       (8)
```

All fourteen mixed binary coefficients on the neighbouring hyperplane
vanish identically.  The two diagonal coefficients are

```text
AAAA=-2A,
BBBB= 2B/Q.                                          (9)
```

They are nonzero by (2).  Hence (8) is a genuine binary
`P_4 -> Delta_2` extension on the dense `L!=0` stratum.

For example, at `(L,Q,C)=(1,1,1)`, the canonical marking has mixed
matrix rank seven and its unique kernel has diagonal pair `(0,4)`.
The shifted marking (5) has rank six, and (8) has diagonal pair
`(-4,6)`.  This proves that binary extension behaviour is not a
function of the four planes alone.

## Ternary obstruction

At mode two, form the one-third-row map on the neighbouring
hyperplane.  Its rows indexed by binary words

```text
000,001,011,111
```

give the determinant

```text
8 A^2 B.                                              (10)
```

This is nonzero by (2), so the third target row at mode two vanishes
on the neighbouring hyperplane.  It is therefore supported only on
the distinguished source coordinate `q=2`.

On the pure hyperplane, the mode-two one-marked map does not kill that
coordinate; one of its entries is exactly

```text
A.                                                    (11)
```

Thus the third row vanishes globally, contradicting rank three of the
full local map.  The shifted binary branch (5)--(9) cannot lift to
`H31`.

## Scope consequence

The plane-component theorems remain valid as statements about the
pure-compression locus.  The earlier `H31` calculations remain valid
for their displayed marked row families.  What fails is the inference
that one marked section excludes every local map over the same plane
component.

That required classification has now been completed on the finite
family chart in
[`P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`](P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md).
It finds the full constructible survivor table, including three
previously hidden points on `C=-L/2`, and excludes every binary
extension by all-extension marked-minor covers.  The remaining
known-component work was therefore on its projective toric and Schubert
boundary planes.  The 21 genuine toric base cases have since been
closed, including their complete marked fibres, in
[`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](claims/p5/h31/toric-marked-fibre/P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md).
The nonzero preferred-chart divisor is also closed at complete
marked-fibre level in
[`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md).
The internal `E=0` and first-plane Schubert-infinity fibres have since
been closed at complete marked-fibre level.

## Verification

Run:

```text
python verify_p5_h31_marked_basis_open_branch.py
python audit_p5_h31_marked_basis_open_branch.py
```

The primary verifier checks (6)--(11) symbolically.  The independent
audit uses a separate dynamic-programming permanent and modular row
reduction over `F_5` and `F_7`; it checks every parameter tuple
satisfying (2), without importing the primary verifier or enumerating
ambient local maps or Grassmannians.
