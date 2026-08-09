# Any support-one `(2,1,1)` triangle is lower-rank or embedded `P_3`

## Status

**Exact symbolic boundary classification over `C`.**  Consider a
rank-three exceptional triangle with relation-rank pattern `(2,1,1)`.  If
at least one coefficient-rank-one relation is a support-one zero product,
then:

1. every common-factor Borel orientation makes one triangle pair image have
   rank at most two;
2. every crossed orientation either has the same rank defect or places all
   three triangle planes in one coordinate three-space.  Any nonzero pure
   `P_4` restriction in the latter case is an embedded pure-`P_3`
   suspension.

Thus the entire support-one boundary produces no new pure-`P_4` component.
Lower pair-image-rank configurations, component exhaustiveness, and the
global Krenn--Gu conjecture remain open.

## A support-one zero product is rigid

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

For a coordinate form,

```text
Ann_R1(X_i)=C X_i.                                  (1)
```

Consequently a support-one zero product is necessarily `X_i*X_i=0`, up to
row scaling.  There is no second annihilator direction.

## Common-factor orientations lose pair rank

Suppose the two rank-one edges share a common-mode factor.  Equation (1)
forces that factor and both leaf factors to be the same coordinate `e=X_i`.

In the `YY` orientation, the rank-two relation is

```text
e*x_2=x_1*e,
```

so `x_2-x_1` belongs to `Ann_R1(e)=C e`.  The two leaf planes coincide, and
their product image lies in

```text
span(e*x_1,x_1^2),                                  (2)
```

of dimension at most two.  The `XX` orientation is identical with kernel
and active roles reversed.

In the mixed `YX` orientation, the rank-two relation reads

```text
e^2=x_1*y_2=0.                                     (3)
```

The four leaf-pair products are then contained in
`span(e*y_2,x_1*e)`, again of dimension at most two.  None of the three
common-factor orientations can have the required rank-three edge.

## The crossed factorization has one extra coordinate

In a crossed orientation the two support-one relations can be normalized to

```text
x_1*y_3=X_i^2=0,
y_2*x_3=X_j^2=0.                                   (4)
```

If `i=j`, the two rows of mode three are proportional and the plane
collapses.  Take `i=0,j=1`.  Then

```text
x_1=y_3=X_0,       y_2=x_3=X_1,                    (5)
```

and the rank-two relation becomes a factorization

```text
p*q=X_0X_1,       p=y_1, q=x_2.                    (6)
```

Write

```text
p=p_0X_0+p_1X_1+s_2X_2+s_3X_3,
q=q_0X_0+q_1X_1+t_2X_2+t_3X_3,
Delta=p_0q_1-p_1q_0.                               (7)
```

The six coefficients of (6) imply

```text
Delta*s_k=Delta*t_k=0,       k=2,3.                (8)
```

If `Delta!=0`, both factors lie in `span(X_0,X_1)` and the triangle is
pair-rank deficient.  If `Delta=0`, the nonzero target coefficient gives

```text
p_0q_1=p_1q_0=1/2.                                 (9)
```

Hence, for a nonzero scalar `lambda`, one has

```text
p=P+s,
q=lambda*(P-s),
P=p_0X_0+p_1X_1,
2*lambda*p_0*p_1=1,
s^2=0.                                             (10)
```

The last equation says `s_2s_3=0`.  Thus `s` uses at most one of the two
remaining coordinates.  If it is zero, pair rank drops.  Otherwise, after a
source permutation, all three triangle planes lie in

```text
H=span(X_0,X_1,X_2).                               (11)
```

## One support-one edge and one support-two edge

A common-factor orientation is impossible in the genuine mixed case: the
shared row would have to be both a singleton-support factor and a factor of
an exact support-two zero product.  Hence only the crossed orientation
remains.  Normalize the singleton edge to

```text
x_1=y_3=X_0.                                      (12)
```

Write the other zero product as `y_2*x_3=0`, with exact support two.
If its support contains `0`, a coordinate change inside that support gives

```text
y_2=X_0-X_1,       x_3=X_0+X_1.                   (13)
```

The synchronizing rank-two relation is then

```text
y_1*x_2=x_1*y_2=-X_0X_1,                          (14)
```

which is exactly the one-edge factorization (6), up to sign.  The preceding
rigid/reflected dichotomy again puts every rank-three survivor in a
coordinate three-space.

If the two supports are disjoint, normalize instead to

```text
y_2=X_1-X_2,       x_3=X_1+X_2,
y_1*x_2=X_0(X_1-X_2).                              (15)
```

This two-edge star cannot acquire the remaining coordinate.  Indeed, write
`p=y_1`, `q=x_2`.  Vanishing of the `03`, `13`, and `23` coefficients first
shows that if exactly one of `p_3,q_3` is nonzero, the other factor is
supported only on `X_3`, contrary to (15).  If both are nonzero, there is a
nonzero `k` such that

```text
q_i=-k p_i  (i=0,1,2),       q_3=k p_3.            (16)
```

The three internal edge coefficients `E_01,E_02,E_12` consequently satisfy

```text
E_01 E_02 + 2k p_0^2 E_12=0.                       (17)
```

The target in (15) has `(E_01,E_02,E_12)=(1,-1,0)`, contradicting
(17).  Thus `p_3=q_3=0`, and all three triangle planes already lie in
`span(X_0,X_1,X_2)`.

## Frobenius--Kunneth turns the survivor into embedded `P_3`

The squarefree algebra splits as

```text
R=R_H tensor C[X_3]/(X_3^2).                       (18)
```

Every triple product of rows from the three triangle planes lies in the
one-dimensional top degree

```text
(R_H)_3=C X_0X_1X_2.                               (19)
```

If `w` is a row of the opposite plane `U_0`, Frobenius pairing with such a
triple product uses only the `X_3` coefficient of `w`.  Therefore the whole
four-mode restricted tensor factors as

```text
(X_3-coordinate on U_0) tensor
(the restricted P_3 tensor on U_1,U_2,U_3).        (20)
```

If (20) is nonzero and pure, its ternary factor is a nonzero pure `P_3`
restriction.  This is exactly the embedded-`P_3` suspension component from
[`P4_EMBEDDED_P3_PURE_COMPONENT.md`](../components/embedded-p3/P4_EMBEDDED_P3_PURE_COMPONENT.md), not
a new component.

## Across the mathematical fence

The boundary has three equivalent descriptions:

```text
monomial factorization:   p*q is one edge or a two-edge star,
rank-two completion:      Delta separates rigid and reflected factors,
Kunneth decomposition:    a coordinate 3-space suspends a P_3 tensor.
```

The key points are that `s^2=0` in a two-variable squarefree block is the
union of its two coordinate axes, while a two-edge star has no factorization
that leaks into a fourth coordinate.  A potentially complicated
factorization scheme therefore becomes a coordinate-hyperplane statement,
where Frobenius duality finishes the graph classification.

## Verification

Run:

```text
uv run --with sympy python claims/p4/classifications/verify_p4_support_one_211_triangle_reduction.py
python claims/p4/classifications/audit_p4_support_one_211_triangle_reduction.py
```

The primary verifier checks the one-edge factorization dichotomy, the
two-edge-star obstruction, all common-factor rank bounds, the generic
rank-three representatives, and the Kunneth factorization of all sixteen
tensor coefficients.  The independent audit permutes the source coordinates
and uses exact rational representatives of both surviving crossed branches.
Neither performs a search.
