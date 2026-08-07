# The all-rank-two-relation triangle is a divisor of component eleven

## Status

**Exact characteristic-zero component-containment theorem.**  The complete
rank-three triangle with three coefficient-rank-two relations, classified in
[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md),
does not give a sixteenth pure-`P_4` component.  Its entire closure lies in
the six-dimensional equal-support common-factor component eleven.

On the dense chart this is an equality with the divisor `p=0` in the
component-eleven normal form.  The three triangle parameters are not a new
moduli space: one is the residual block source scaling, and the other two
are precisely the parameters `r,q` on that divisor.

## The corrected triangle family

Put

```text
a=X_0+X_1,       a_bar=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3.                    (1)
```

Every nonzero pure rank-three triangle whose three unique relation matrices
have rank two is, up to the allowed symmetries,

```text
T_0=span(b_bar,a_bar),
T_i=span(a,b+alpha_i a_bar),       i=1,2,3,         (2)
```

with

```text
alpha_1+alpha_2+alpha_3 != 0.                       (3)
```

All six pair images have rank three on a dense open.  The three edges among
`T_1,T_2,T_3` have relation-matrix rank two, while the three edges from
`T_0` have relation-matrix rank one.  Thus the tuple carries a rank-two
triangle and, simultaneously, a rank-one star.

## Component eleven on `p=0`

The equal-support component from
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md)
has planes

```text
C_0=span(a+p b,       a_bar+q b),
C_1=span(a,           a_bar+b),
C_2=span(a,           r a_bar+b),
C_3=span(b_bar,       a_bar).                       (4)
```

Set `p=0`.  On the dense chart `alpha_1 alpha_3!=0`, apply the source block
scaling

```text
diag(1,1,alpha_1,alpha_1)                           (5)
```

to (2), and put

```text
r=alpha_2/alpha_1,       q=alpha_1/alpha_3.         (6)
```

Then the four transformed row spaces, in mode order, are exactly

```text
(T_0,T_1,T_2,T_3)=(C_3,C_1,C_2,C_0).               (7)
```

Indeed, the three moving planes become

```text
span(a,b+a_bar),
span(a,b+(alpha_2/alpha_1)a_bar),
span(a,b+(alpha_3/alpha_1)a_bar),                   (8)
```

and

```text
C_0|_(p=0)=span(a,a_bar+q b)
            =span(a,b+q^(-1)a_bar).                 (9)
```

Equations (6)--(9) give the claimed identity.

The nonzero conditions agree rather than merely being compatible.  On
`p=0`, the sole component-eleven active coefficient is proportional to

```text
1+q(r+1)
 =1+(alpha_1/alpha_3)(alpha_2/alpha_1+1)
 =(alpha_1+alpha_2+alpha_3)/alpha_3.                (10)
```

Thus (3) is exactly the component-eleven nonvanishing condition in this
chart.

The locus `alpha_1 alpha_3!=0` is dense in the irreducible parameter space
of (2).  Component eleven is closed, so the points with a vanishing
`alpha_i`, together with the projective parameter endpoints, belong to its
closure as well.  This proves the full containment theorem.

## Geometric interpretation

The corrected triangle originally appeared through affine holonomy and a
binary-cubic synchronizer.  Component eleven appeared through exact zero
divisors and an apolar `P^2` fibre.  Formula (7) shows that these are two
charts of the same geometry:

```text
flat synchronizer line
    = p=0 apolar divisor
    = rank-one-star/rank-two-triangle incidence.    (11)
```

This is a boundary-stratum identification of the kind familiar from quiver
Grassmannians: changing which subconfiguration is declared generic changes
the visible relation graph, but not the ambient irreducible component.

## Exact replay

```text
uv run --with sympy python verify_p4_all_rank_two_relation_triangle_component_inclusion.py
python audit_p4_all_rank_two_relation_triangle_component_inclusion.py
```

The primary verifier proves the symbolic Pluecker identities, permanent
identity, nonvanishing-factor identity, all-six rank profile, and relation-
rank word.  The independent audit uses rational row reduction, a subset-DP
permanent, and exact pair-kernel ranks.  Neither performs a search.
