# Hyperplane-incidence reduction for normalized `q5_221`

## Status

This is an exact structural reduction over `C` for the normalized
`q5_221` branch of a possible restriction

```text
P_5 -> Delta_3.
```

It converts the first rank-drop consequences into nine finite marked
incidence types, lying over six uncoloured multigraph types.  It does
not yet exclude `q5_221`, `P_5 -> Delta_3`, or the
arbitrary-order Krenn--Gu prize conjecture.

## Three embedded copies of `P_4`

Normalize the five coordinate rows of the distinguished mode so target
colours zero, one, and two have source multiplicities `2,2,1`.
Apply one simultaneous diagonal rescaling of the five source
coordinates in every mode.  This multiplies `P_5` by the product of
the five diagonal entries, so it preserves the restriction problem up
to one nonzero overall scalar.  It puts the three target-coordinate
covectors in the form

```text
u_0=(1,1,0,0,0),
u_1=(0,0,1,1,0),
u_2=(0,0,0,0,1).                                    (1)
```

Regard `P_5` as the polarization of the squarefree monomial
`x_0 x_1 x_2 x_3 x_4`.  Contracting the distinguished mode gives

```text
T_0=u_0 contract P_5
   = Sym(e_0+e_1,e_2,e_3,e_4),

T_1=u_1 contract P_5
   = Sym(e_0,e_1,e_2+e_3,e_4),

T_2=u_2 contract P_5
   = Sym(e_0,e_1,e_2,e_3).                            (2)
```

Here `Sym(v_0,v_1,v_2,v_3)` is the embedded order-four permanent tensor
on the displayed ordered basis.  Its source hyperplanes are

```text
H_0=span(e_0+e_1,e_2,e_3,e_4),
H_1=span(e_0,e_1,e_2+e_3,e_4),
H_2=span(e_0,e_1,e_2,e_3),                           (3)
```

with independent normals

```text
h_0=(1,-1,0,0,0),
h_1=(0,0,1,-1,0),
h_2=(0,0,0,0,1).                                    (4)
```

The target identities require the same four remaining local maps to
send `T_c` to a nonzero pure fourth power in target colour `c`.

## Rank drop is normal containment

Let

```text
L_i:C^5 -> C^3,   i=0,1,2,3,
```

be the four remaining local maps and let `U_i` be the
three-dimensional row space of `L_i`.

Restriction to `H_c` has rank

```text
rank(L_i restricted to H_c)
  = 3 - dim(U_i intersect span(h_c)).                 (5)
```

Consequently it has rank two exactly when

```text
h_c in U_i.                                           (6)
```

Every original local map has rank three, and a hyperplane restriction
has rank at least two.  Apply the decomposable-`P_4` rank-drop theorem
to each tensor in (2).  If

```text
D_c={i:h_c in U_i},
```

then

```text
|D_0|>=2,   |D_1|>=2,   |D_2|>=2.                    (7)
```

Thus the branch becomes an incidence problem between three independent
normal points and four row-space planes in `P^4`.  There are at least
six incidences, so some mode contains at least two of the three normals.
If a mode contains all three, its row space is exactly
`span(h_0,h_1,h_2)`.

## Nine marked minimal incidence types

Choose any two incidences from each `D_c`.  Extra containments only add
constraints, so every branch contains one minimal `3 x 4` incidence
matrix with each row sum two.

Equivalently, regard each target colour `c` as an edge `D_c` on the four
mode vertices.  The two multiplicity-two colours `0,1` may be swapped,
but the multiplicity-one colour `2` is distinguished and cannot be
permuted with them.  After forgetting that mark, a three-edge
multigraph on four vertices has exactly six types:

1. three parallel edges;
2. a double edge plus an adjacent edge;
3. a double edge plus a disjoint edge;
4. a triangle;
5. a three-edge star;
6. a three-edge path.

Marking the singleton-colour edge splits double-plus-adjacent,
double-plus-disjoint, and the three-edge path into two cases each.  The
normalized branch therefore has nine types:

```text
underlying graph       D_0   D_1   D_2

triple parallel        0011  0011  0011
double+adjacent A      0011  0011  0101
double+adjacent B      0011  0101  0011
double+disjoint A      0011  0011  1100
double+disjoint B      0011  1100  0011
triangle               0011  0101  0110
star                   0011  0101  1001
path, marked end       0011  0101  1010
path, marked middle    0101  1010  0011.             (8)
```

Here `A` means that the marked singleton edge is the lone edge, while
`B` means that it is one of the doubled edges.  Matrix (8) is a
minimal selected sub-incidence, not an exact-containment
stratification: unselected containments may still occur and must not be
silently discarded.

## Cross-contraction pencil

Put

```text
x_+=e_0+e_1,  x_-=e_0-e_1,
y_+=e_2+e_3,  y_-=e_2-e_3,  z=e_4.
```

Thus `u_0=x_+`, `u_1=y_+`, `u_2=z` and
`h_0=x_-`, `h_1=y_-`, `h_2=z`, identifying vectors and covectors in
the displayed coordinate basis.

Suppose one mode `i` contains two normals `h_c,h_d`.  Since `L_i` has
rank three, there are unique independent target covectors
`alpha_(i,c),alpha_(i,d)` satisfying

```text
L_i^* alpha_(i,c)=h_c,
L_i^* alpha_(i,d)=h_d.
```

Contracting the colour-`c` pure `P_4` identity by
`alpha_(i,c)` gives zero on the source side.  Hence

```text
alpha_(i,c)(e_c)=0.                                  (9)
```

Cross-contracting instead gives

```text
(tensor_(j!=i) L_j) Q_cd
  = lambda_c alpha_(i,d)(e_c) e_c^3,

Q_cd=(u_c,h_d) contract P_5.                         (10)
```

The two cross scalars
`alpha_(i,d)(e_c)` and `alpha_(i,c)(e_d)` cannot both vanish:
together with (9), that would make the two independent covectors
proportional to the dual direction of the third target colour.
Therefore at least one of `Q_cd,Q_dc` is sent to a nonzero pure cube.

Up to irrelevant nonzero signs, the six residual tensors and the
annihilators of their three-dimensional source spaces are

```text
Q_01 = Sym(x_+,y_-,z),       J_01^perp=span(h_0,u_1)
Q_10 = Sym(x_-,y_+,z),       J_10^perp=span(u_0,h_1)
Q_02 = Sym(x_+,e_2,e_3),     J_02^perp=span(h_0,h_2)
Q_20 = Sym(x_-,e_2,e_3),     J_20^perp=span(u_0,h_2)
Q_12 = Sym(e_0,e_1,y_+),     J_12^perp=span(h_1,h_2)
Q_21 = Sym(e_0,e_1,y_-),     J_21^perp=span(u_1,h_2). (11)
```

For another mode `k`,

```text
rank(L_k restricted to J_cd)
  = 3-dim(U_k intersect J_cd^perp).                  (12)
```

Equation (12) is an essential boundary gate.  If the intersection has
dimension two, the residual map has rank one and the rank-at-least-two
`P_3` classification cannot be applied.

The next analytic target is therefore finite and explicit: for each of
the nine marked types, classify the pair of residual tensors in (11),
including the rank-one boundary in (12).  The residual source factors
differ by the sign involutions

```text
e_0+e_1  <->  e_1-e_0,
e_2+e_3  <->  e_3-e_2,
```

so the zero/nonzero plane classifications from the `q5_311` proof can
be reused on a two-chart pencil rather than on raw support masks.

## Verification

Run:

```text
python verify_p5_q5_221_hyperplane_incidence.py
python audit_p5_q5_221_hyperplane_incidence.py
```

The primary verifier expands all three contractions in (2), checks the
hyperplane normals, rank formula, and six cross-contractions in (11),
and enumerates the nine marked minimal incidence orbits.  The
independent audit enumerates an unordered pair of majority-colour edges
and one distinguished singleton-colour edge.  It obtains the same nine
marked orbits, lying over six uncoloured multigraphs, without importing
the primary code.
