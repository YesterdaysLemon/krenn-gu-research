# Generic weighted `H22` obstruction on the diagonal-quadric component

## Status

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbit of the diagonal-quadric pure-`P_4` component
proved in
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md).

For each of the weighted diagonal directions `D01` and `D23`, the
generic binary `H22` extension incidence is empty.  The proof replaces
the large generic determinantal calculation by a projective
intersection: an extension eight-plane must meet the join of a Segre
fourfold and one of its points.  One exact empty projective fibre,
together with properness, excludes the generic incidence.

Consequently generic weighted `H22` incidence is empty on all seven
component orbits certified at this checkpoint.  A disjoint-support
mixed-star eighth component has since been certified in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md);
its generic weighted `H22` incidence is not covered here.

This does **not** classify all pure-`P_4` components, close special
component-parameter or slope divisors, exclude every `H22` incidence,
or resolve the global prize problem.

## The fixed extension space

Use the quadratic-function-field chart

```text
K=Q(C,l,r)[E]/(R),

R=-C^2 E^2+C^2 l^2+C E^2 l-C l-l^2+1,             (1)
```

and the basis

```text
y_1=(1,0,0,-1),             y_2=(0,1,-1,0),
k_0=(1,0,0, 1),             k_1=(0,1, 1,0),
x_1=(1,C+1,C-1,1),
u_0=(E,-1,-1,-E),           u_1=(1,-1,1,1),

(1-l^2)x_2=
 (C(l^2-E^2)+E(1-l^2), 1-l^2, 1-l^2,
  C(l^2-E^2)-E(1-l^2)),

alpha=(u_0+l u_1,y_1,y_2,l k_0-k_1),
beta =(u_0,x_1,x_2,k_0).                           (2)
```

The harmless scaling of `x_2` in (2) is valid on the dense open under
consideration.  Equation (1) is irreducible over `Q`, and the pure
restriction has only its `1111` coefficient nonzero.

For a weighted direction `d` in `{D01,D23}`, let

```text
D_d: K^8 -> V,              V=(K^2) tensor^4,       (3)
```

be the full extension map before changing the four marked bases.  Its
row indexed by `w in {0,1}^4` consists of the eight three-row
permanents obtained by placing the fifth-coordinate extension in one
mode.  This is the first multilinear/apolar extension map of the four
plane factors.
Write

```text
S_d=im D_d subset V.                                (4)
```

## Marking as a Segre join

Let `e_w` be the fixed binary coefficient basis of `V`, put

```text
B=e_1111,

X=Segre((P^1)^4) subset P(V),

A([u_i:v_i])_w=product_i (u_i if w_i=0 else v_i).  (5)
```

Changing `beta_i` to `beta_i+t_i alpha_i` does not move `S_d`; it
changes the first pure coefficient covector to

```text
A([1:-t_0],...,[1:-t_3]).
```

Therefore a nonzero binary `H22` extension would give

```text
P(S_d) intersect J(B,X) != empty,                   (6)
```

where `J(B,X)` is the projective join of `B` and `X`.  Condition (6)
is weaker than the genuine binary condition because it also includes
marking points at infinity and permits either pure coefficient to
vanish.  Proving the intersection empty is thus sufficient.

This formulation removes both the projective extension-kernel
coordinates and the affine marking escape that obstructed the earlier
specialization argument.

## An exact empty projective fibre

Specialize to

```text
(C,E,l,r)=(-2/3,-1/4,2,2).                          (7)
```

This point satisfies (1), all four planes in (2) have rank two, the
pure coefficient is

```text
T_1111=5,
```

and the dense-chart factors `C(C-l)(1-l^2)r` are nonzero.

For both directions, exact rational linear algebra gives

```text
                     D01                    D23
rank D_d              8                      8
rank [D_d | B]         9                      9.     (8)
```

For transparency, the same row set

```text
(0,1,2,3,4,5,6,10)
```

gives nonzero `8 x 8` minors

```text
det D_D01 = 3107727,
det D_D23 = 6284849697/256.                         (9)
```

Let `L_d` be an exact `8 x 16` left annihilator of `D_d`.  Cover the
Segre factor by its sixteen standard charts.  A chart word
`epsilon in {0,1}^4` uses

```text
(u_i,v_i)=(1,x_i) if epsilon_i=0,
(u_i,v_i)=(x_i,1) if epsilon_i=1.                  (10)
```

On the finite join chart, solve the eight equations

```text
L_d (A(x)+qB)=0.                                   (11)
```

Exact characteristic-zero Gröbner bases give the unit ideal on the
first fifteen charts, in both directions.  On the last chart
`epsilon=1111`, the reduced ideal is

```text
(x_0,x_1,x_2,x_3,q+1).                             (12)
```

The point (12) is not a projective intersection: there `A=B` and
`A+qB=0`.

It remains essential to check the limit directions over this base
point.  In the `1111` chart the projective coordinate ideal is

```text
(q+1,x_0,x_1,x_2,x_3,
  x_i x_j,x_i x_j x_k,x_0x_1x_2x_3)
=(q+1,x_0,x_1,x_2,x_3).                            (13)
```

Hence one ordinary blow-up resolves the rational join
parametrization.  Its exceptional divisor maps to

```text
T=span(B,e_0111,e_1011,e_1101,e_1110).             (14)
```

Exact ranks are

```text
rank T=5,
rank [D_D01 | T]=13,
rank [D_D23 | T]=13.                               (15)
```

The `13 x 13` minors on rows

```text
(0,1,2,3,4,5,6,7,10,11,13,14,15)
```

are respectively

```text
-3107727,       -6284849697/256.                   (16)
```

Thus `S_d intersect T=0`.  Equations (11)--(16) cover the resolved
join, including every marking-at-infinity and tangent limit, and prove

```text
P(S_D01) intersect J(B,X)=empty,
P(S_D23) intersect J(B,X)=empty                    (17)
```

at (7).

## Why one fibre proves the generic theorem

The hypersurface (1) is irreducible.  On the open set where either
minor (9) remains nonzero, `S_d` is a rank-eight vector subbundle of
the trivial bundle with fibre `V`.  The incidence

```text
Z_d=P(S_d) intersect (base x J(B,X))                (18)
```

is closed in a projective bundle over that open base.  Its projection
to the base is proper and therefore has closed image.

By (17), this image misses the point (7).  It is consequently a proper
closed subset and cannot contain the generic point of the irreducible
base.  This proves that (18), and hence the genuine binary `H22`
incidence, is empty over `K` for each weighted direction.

No Gröbner basis over the generic quadratic function field is needed:
proper projective geometry transports the exact empty fibre to a
nonempty generic open.

## Honest frontier

The seven component orbits known at this checkpoint are generically
excluded from weighted `H22`.  The new eighth orbit is not.  This is
not an exhaustive `H22` theorem.  The remaining tasks are:

1. transport the eighth component through weighted `H22`;
2. prove whether the eight pure-component orbits are exhaustive;
3. close the special parameter, source-slope, and component-boundary
   strata on the known families;
4. combine that classification with the remaining global lift from
   local `P_5` contractions.

The previous exploratory calculations, including their completed
special fibres and explicitly null timeout outcomes, remain recorded
in
[`P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md`](P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md).

## Verification

Run:

```text
python \
  verify_p5_h22_diagonal_quadric_component_generic_obstruction.py

python \
  audit_p5_h22_diagonal_quadric_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(5), the exact extension maps,
all sixteen rational chart ideals in both directions, and the rank
certificates (8)--(16).  Singular computes the chart Gröbner bases
over `Q`.

The independent audit imports nothing from the primary verifier.  It
rebuilds the matrices with a separate dynamic-programming permanent,
uses SymPy's independent exact Gröbner implementation on all
thirty-two charts, and rechecks the exceptional-space ranks and
displayed minors over `Q`.
