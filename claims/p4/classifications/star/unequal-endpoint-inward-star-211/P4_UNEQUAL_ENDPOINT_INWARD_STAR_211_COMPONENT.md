# A twenty-fifth pure `P_4` component from two unequal inward endpoints

## Status

**Exact characteristic-zero component theorem.**  In the star cell with
relation ranks `(2,1,1)`, orient both rank-one spokes inward and take their
center endpoints to be distinct disjoint binary zero divisors.  One
irreducible hypersurface of the resulting normal form is a smooth
five-dimensional component orbit, component twenty-five.

The complete reverse support and projective leaf-boundary classification is
proved subsequently in
[`P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md`](../../triangle-211/unequal-endpoint-inward-star-211-complete/P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md).
This component's `P_5` fibres, special fibres, and the
arbitrary-order local-to-global step remain open.  The Krenn--Gu conjecture
remains **UNRESOLVED**.

The equal-endpoint inward stratum is excluded separately in
[`P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md`](../equal-endpoint-inward-star-211-obstruction/P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md).

## Normal form and purity equation

Work in the squarefree algebra and put

```text
A=X_0+X_1,  C=X_0-X_1,  B=X_2+X_3,  D=X_2-X_3.
```

The four planes are

```text
U_0=<A,B>,
U_1=<A+kD,B+sC>,
U_2=<C,A+eB-kD>,
U_3=<D,A-sjC+jB>.                                  (1)
```

The exceptional relations are

```text
A*x_1-B*y_1=0,   A*y_2=0,   B*y_3=0.               (2)
```

Thus the two rank-one relations use the distinct center endpoints `A,B` and
the two leaf kernel rows `C,D`: this is the unequal-endpoint two-inward word.
The only nonzero coefficient candidates are

```text
T_0011=4(ej+k^2),
T_0111=T_1011=4(e+j),
T_1111=4(1+ejs^2).                                 (3)
```

They form a rank-one `2 x 2` matrix exactly on

```text
F=(ej+k^2)(1+ejs^2)-(e+j)^2=0.                    (4)
```

All four mode flattenings then have rank one, so the multiplication tensor
is pure.  The hypersurface is irreducible in characteristic zero.  Indeed,
as a quadratic in `k`, a factorization would make

```text
((e+j)^2-ej(1+ejs^2))/(1+ejs^2)
```

a square in `C(e,j,s)`.  Its valuation along the irreducible divisor
`1+ejs^2=0` is `-1`, because the numerator restricts there to `(e+j)^2` and
is not divisible by that divisor.

## All-pair point and component certificate

At

```text
(e,j,k,s)=(-5,2,3,-1),                              (5)
```

the pair profile in the order `01,02,03,12,13,23` is

```text
(3,3,3,4,4,4),                                     (6)
```

and the exceptional relation matrices have ranks `(2,1,1)`.  Three dense
leaf-pair minors are

```text
edge 12:  8k(es-1)(es+1),
edge 13:  8s(js-1)(js+1),
edge 23: -8j(es-1)(js-1).                          (7)
```

Use Grassmann pivots `(02),(01),(01),(02)` and restore the diagonal source
torus.  Restricting the family Jacobian to the tangent hyperplane `dF=0`
gives rank five; rows `(0,3,4,5,8)` and tangent columns `(0,1,2,3,5)` have
determinant

```text
-7/27.                                             (8)
```

In the universal Segre-incidence chart, the same point has target ratios
`(3,-2,1,0)`.  The fifteen incidence equations have Jacobian rank fifteen;
columns `g_0,...,g_12,g_14,z_3` have determinant

```text
81920/3.                                           (9)
```

The incidence is therefore smooth of dimension five at (5), while the
irreducible hypersurface/source-torus family supplies all five local
directions.  Its closure is an irreducible component.  Its pair graph and
relation word separate it from components one through twenty-two; the two
distinct inward center endpoints separate it from the common-center outward
component twenty-three and the mixed-orientation component twenty-four.

## Replay and boundary

```text
uv run --with sympy python claims/p4/classifications/star/unequal-endpoint-inward-star-211/verify_p4_unequal_endpoint_inward_star_211_component.py
uv run --with sympy python claims/p4/classifications/star/unequal-endpoint-inward-star-211/audit_p4_unequal_endpoint_inward_star_211_component.py
```

The primary verifier reconstructs (1)--(9) over exact characteristic-zero
arithmetic.  The no-import audit uses the independent rational point
`(e,j,k,s)=(-2,5,3,-1)`, then applies a source permutation and unequal source
scales before checking purity, pair ranks, and relation ranks.  Neither
script uses finite-field output as proof.
