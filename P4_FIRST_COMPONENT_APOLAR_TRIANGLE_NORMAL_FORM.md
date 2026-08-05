# The first pure `P_4` component is an apolar triangle bundle

## Status

**Exact dense normal-form theorem.**  The repository's original
five-dimensional pure-`P_4` component has a two-parameter presentation in
which three planes form one fixed exceptional triangle and the fourth plane
moves inside a three-dimensional apolar hyperplane.  Restoring the projective
diagonal source torus gives the full five-dimensional component.

This identifies the generic one-rank-two-edge triangle already present in the
repository.  It does not yet prove that every possible Borel orientation or
special boundary of that graph belongs to this component.

## The fixed triangle

Use marked kernel/active rows `(y_i,x_i)` and put

```text
U_1=span((1,1,1,1), (0,0,1,1)),
U_2=span((1,0,1,0), (1,-1,1,1)),
U_3=span((0,0,1,-1), (1,0,-1,0)).                (1)
```

The three pair images have rank three.  Their unique relations are

```text
y_1x_2-2x_1y_2=0,           coefficient rank 2,
x_1y_3=0,                    coefficient rank 1,
y_2x_3=0,                    coefficient rank 1.                 (2)
```

Thus the exceptional graph on modes `1,2,3` is a triangle with relation-rank
multiset `{1,1,2}`.  The two rank-one edges are opposite binary zero products
on supports `{2,3}` and `{0,2}`; their one-coordinate overlap is the `1+3`
geometry hidden in the older parameterization.

## Why the rank-two edge becomes one factorization

Preserve the two zero-product rows in (2).  A Borel shift of `x_2` removes the
constant term of the rank-two relation without changing either zero product.
The remaining equation is a factorization of the fixed squarefree quadratic

```text
(1/2)y_1x_2=x_1y_2=(X_2+X_3)(X_0+X_2).            (3)
```

On the dense branch where both missing-coordinate entries are nonzero, write
`y_1=(a_0,a_1,a_2,a_3)`.  The three zero target coefficients involving
coordinate one force

```text
x_2=lambda(-a_0,a_1,-a_2,-a_3).                  (4)
```

The three nonzero coefficients of (3) are

```text
-2lambda a_0a_2,
-2lambda a_0a_3,
-2lambda a_2a_3.
```

Equality makes `a_0=a_2=a_3`.  Row scaling fixes their common value and the
remaining source-coordinate scaling fixes `a_1`.  This yields exactly the
three fixed planes in (1).  No polynomial-system search is involved.

## The apolar opposite plane

In degree three, every mixed triple product of the rows in (1) vanishes.  The
only two nonzero triples are

```text
y_1y_2y_3=(-1,-1,-1, 1),
x_1x_2x_3=( 1, 1,-1,-1),                            (5)
```

where a degree-three vector is indexed by the missing source coordinate.
Therefore the fourth plane must lie in the hyperplane annihilating the first
covector.  On its dense `(01)` chart it is

```text
U_0=span(
 (1,0,p,1+p),
 (0,1,q,1+q)).                                      (6)
```

The active covector in (5) restricts to `(-2p,-2q)`.  Consequently the full
restriction has only

```text
T_0111=-2p,       T_1111=-2q,                       (7)
```

and is the pure tensor

```text
-2(p e_0+q e_1) tensor e_1 tensor e_1 tensor e_1.  (8)
```

The opposite-plane parameter space is the open part of
`Gr(2,ker(y_1y_2y_3))=Gr(2,3)=P^2`.  Formula (6) is one affine chart of that
projective plane.

## Exact exceptional graph

In lexicographic edge order, the generic pair profile is

```text
(4,4,4,3,3,3).                                      (9)
```

For the three pairs involving `U_0`, explicit maximal minors are

```text
-2(p-q)(p+q+1),
-2q(p+1),
-2p.                                                (10)
```

Thus (9) holds on

```text
pq(p+1)(p-q)(p+q+1) != 0.                          (11)
```

At `(p,q)=(1,2)`, all three exterior pair images have rank four and the
triangle relations have coefficient ranks `(2,1,1)`.

## Equivalence with the original family

In [`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](P4_DECOMPOSABLE_RANK_TWO_FAMILY.md),
set

```text
e=i=l=1,       c=-1-q,       j=-p/q.               (12)
```

Apply the diagonal source transformation

```text
diag(-1,-1,1,1),                                   (13)
```

then perform the displayed legal row rescalings and shifts.  The four
Pluecker vectors become exactly those of (1), (6).  Conversely every point of
the dense chart `q!=0` arises from (12).  The diagonal-source orbit of the
two-parameter apolar family is therefore precisely the original
five-dimensional component, whose smooth component certificate remains
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](P4_PURE_RANK_TWO_COMPONENT_THEOREM.md).

## Foreign-language payoff and frontier

The older family looked like a five-variable permanent cancellation.  In the
new shape it is a bundle of apolar two-planes over one fixed rank-one/rank-two
exceptional triangle:

```text
fixed squarefree-quadratic factorization
        -> two degree-three covectors
        -> Gr(2,3)=P^2 apolar fibre
        -> diagonal source torus.
```

This is the Artinian-Gorenstein analogue of reconstructing a linear space from
its apolar covectors.  The remaining component-classification question is
whether the other Borel orientations and support collisions of a `{1,1,2}`
triangle reduce to this component or to already known star/lower-rank
closures.

The crossed orientation with genuine support-two zero products is now
classified completely in
[`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md):
equal labels force a coordinate hyperplane, disjoint labels force a pair-rank
drop, and one-coordinate overlap gives exactly the triangle above.  The
remaining question is confined to the other Borel orientations and
support-one/lower-pair-rank boundaries.

One of those other orientations has now produced a distinct component rather
than another chart of this one.  When both rank-one edges use the same
support label and the same active row at their common mode, an extra affine
synchronization parameter survives.  Its `P^2` apolar fibre and source torus
form the six-dimensional eleventh component in
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md).

## Verification

Run:

```text
uv run --with sympy python verify_p4_first_component_apolar_triangle_normal_form.py
uv run --with sympy python audit_p4_first_component_apolar_triangle_normal_form.py
```

The primary verifier checks (2)--(13), including the exact Pluecker
identification with the original family.  The audit permutes the source order
to `(1,0,3,2)` and reconstructs permanents by subset dynamic programming.
Both are exact symbolic replays, not searches.
