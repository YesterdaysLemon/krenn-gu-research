# A six-dimensional component of the pure `P_4` compression locus

## Status

This is an exact characteristic-zero component theorem.  The locus of
four rank-two maps whose restriction of the order-four permanent is a
nonzero pure tensor has a generically smooth, rational,
six-dimensional irreducible component.

This component lies on the lower pair-image-rank boundary omitted by
the directed radical-star classification.  Its dimension separates it
from the six previously certified five-dimensional component orbits.
Consequently there are at least seven symmetry-inequivalent
pure-compression components at this checkpoint.  A disjoint-support
mixed star has since raised the certified lower bound to eight in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).

This is not a classification of every component.  The generic marked
`H31` fibre has since been excluded in
[`P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md);
its special parameter/projective boundary remains.  Nothing here
settles `H22` or the global prize problem.

## The family

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Put

```text
h=a+c-d
```

and take the four row planes

```text
U_0=span(
 (1,0,0,-1),
 (0,0,1, 1)),

U_1=span(
 (1,b,0,1-bh),
 (0,e,1,1-eh)),

U_2=span(
 (1,0,  -1, 0),
 (0,1,-a-c,-d)),

U_3=span(
 (1,0,0, 1),
 (0,0,1,-1)).                                    (1)
```

These bases are in the Grassmann charts with pivots

```text
(02),(02),(01),(02).
```

Let `T_ijkl` be the coefficient obtained by choosing row `i,j,k,l`
from the four planes and evaluating the permanent.  Direct
multilinear expansion gives

```text
T_1010=2(1-b(a+c)),
T_1110=2(1-e(a+c)),                               (2)
```

and every other coefficient is zero.  Therefore (1) restricts `P_4`
to a pure tensor whenever the two values in (2) do not vanish
simultaneously.

The cancellation has a simple apolar interpretation.  The two
coefficients with first-mode row zero are

```text
b(a+c-d)+(1-bh)-1,
e(a+c-d)+(1-eh)-1,
```

so the choice of the two last entries in `U_1` kills that entire
binary slice identically.  The surviving slice has fixed rows in
modes zero, two, and three and an unrestricted linear factor in mode
one.  This is a lower pair-rank construction, not a search over plane
tuples.

## Exact component certificate

Restore the diagonal source torus

```text
diag(t_0,t_1,t_2,1)
```

and reduce the resulting planes back into the four charts above.  At

```text
(a,c,d,b,e,t_0,t_1,t_2)=(1,2,4,1,2,1,1,1),        (3)
```

the Jacobian of the family map has rank six.  With chart-coordinate
rows numbered from zero, the submatrix

```text
rows    (1,3,4,5,6,10),
columns (a,d,b,e,t_0,t_2)
```

has determinant `1`.

For an independent local upper bound, adjoin the projective Segre
point of the pure coefficient tensor.  Use `T_1010` as the affine
anchor and target ratios `z_0,...,z_3`.  The fifteen incidence
equations are

```text
T_w-T_1010 product_{i:w_i!=(1010)_i} z_i=0,
                                                    w!=(1010).       (4)
```

At (3),

```text
T_1010=-4,              z=(0,5/2,0,0).
```

The `15 x 20` Jacobian of (4) has rank fourteen.  Its rows `0,...,13`
and columns

```text
(0,1,2,3,4,5,6,8,9,12,14,16,18,19)
```

form a minor of determinant `-215040`.

Thus the incidence locus has tangent dimension six at (3).  The
six-dimensional family passes through that point, so the local
dimension is exactly six and the point is smooth.  The closure of the
irreducible rational family is therefore an irreducible component.
Because a nonzero pure tensor determines its Segre point uniquely,
the same conclusion holds after projecting away the four target
ratios.

## Generic geometry

At (3), and hence on a dense open subset of the component, the six
pair-image ranks in lexicographic edge order are

```text
(r_01,r_02,r_03,r_12,r_13,r_23)
  =(4,3,2,4,4,3).                                  (5)
```

The rank-three edges `02` and `23` have rank-one multiplication
relations pointing to the same pure-kernel endpoint.  The rank-two
edge `03` has two independent rank-one relations.  The resulting
directed signature is

```text
(# rank-one exceptional edges,
 # rank-two-relation exceptional edges,
 sorted pure-kernel endpoint indegrees)
 =(2,0,(2,0,0,0)).                                 (6)
```

The diagonal-quadric jump signature is `(0,2)`.  These invariants put
the component precisely on a lower pair-rank boundary of the
star/triangle analysis.

All six earlier component orbits are five-dimensional.  Dimension is
preserved by mode permutations, source-coordinate permutations,
diagonal source rescaling, and changes of basis inside the local
planes.  Hence this component is inequivalent to all six of them.

## The determinantal prime was a subfamily

The mixed-orientation determinantal calculation in
[`P4_MIXED_ORIENTATION_PURE_COMPONENT.md`](P4_MIXED_ORIENTATION_PURE_COMPONENT.md)
also produced the linear prime

```text
d+q=0,              a+c+p=0.                       (7)
```

On `a!=0`, row reduction of the family on (7) gives exactly (1) with

```text
b=1/a,              e=0.                           (8)
```

Indeed

```text
1-b(a+c-d)=(d-c)/a,       1-e(a+c-d)=1.
```

Thus (7) is not evidence for another isolated five-dimensional
component: it is a proper subfamily of the six-dimensional component
above.  The earlier sample `(a,c,d)=(1,2,3)` lies additionally on
`d=a+c`; using it alone creates an accidental transverse curve.  The
certificate (3), with `d!=a+c`, removes that sample degeneracy.

## Verification

Run

```text
python verify_p4_six_dimensional_pure_component.py
python audit_p4_six_dimensional_pure_component.py
```

The primary verifier derives (2), the rank-six family tangent, the
rank-fourteen incidence certificate, the pair profile, the directed
relation signature, and the exact embedding (8).  The independent
audit uses modular dual numbers, a dynamic-programming permanent, and
separate row reduction over two finite fields to replay the component
certificate and the lower-rank geometry.

## Honest frontier

At this theorem checkpoint the certified lower bound was seven
pure-component orbits: six five-dimensional components and this
six-dimensional component.  It is now eight after the disjoint
mixed-star theorem.  No exhaustiveness claim follows.  The generic
fibres of all eight known components are now excluded from `H31`.
Incomplete component boundaries and the possibility of further pure
components remain to be treated.
