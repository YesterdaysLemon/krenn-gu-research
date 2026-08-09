# The radical-crossed `(2,1,1)` triangle has lower pair rank

## Status

**Exact characteristic-zero obstruction.**  Let a nonzero pure `P_4`
restriction have a rank-three exceptional triangle on modes `1,2,3`, with
rank-two edge `12` and rank-one edges `13,23`.  In pure kernel/active bases
suppose the Borel flags are

```text
y_1 y_3=0,       y_2 x_3=0,
y_1 x_2-x_1 y_2=0.                                  (1)
```

Then the product image `U_1U_2` has dimension at most two, contradicting the
assumed rank-three edge.  Thus this entire orientation is empty on the
all-pair frontier.  Together with
[`P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md`](../classifications/P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md),
the statement includes support-one boundaries as lower-pair or embedded
`P_3` strata.

This fills the previously unnamed sixth Borel-flag orbit of the
`triangle-(2,1,1)` cell.  It does not classify the remaining unequal
common-kernel `CC` orientation, close the two star cells, settle special
`P_5` fibres, or resolve the global Krenn--Gu conjecture.

## Two exact pairs and one synchronizer

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Put

```text
a=y_1,       a_bar=y_3,
b=y_2,       b_bar=x_3.                              (2)
```

The rank-one relations in (1) say

```text
a a_bar=0,       b b_bar=0,                         (3)
```

while the rank-two relation is the synchronization equation

```text
a x_2=x_1 b.                                        (4)
```

Every genuine degree-one zero product in `R` is an opposite pair on a
two-coordinate support.  The two labels in (3) are equal, adjacent, or
disjoint.

## Distinct supports are a forest intersection

If the two support labels are distinct, their union is either a three-vertex
path or two disjoint edges.  Source permutations and diagonal scaling remove
all gains on this forest.  Direct coefficient comparison in (4) gives the
complete solution

```text
x_1=lambda*a+mu*b_bar,
x_2=lambda*b+nu*a_bar.                              (5)
```

The solution space has dimension three: the `6 x 8` coefficient matrix of
(4) has rank five, and the three displayed directions are independent.
Consequently

```text
a x_2=x_1 b=lambda*a b,

x_1x_2=lambda^2*a b+mu*nu*a_bar*b_bar,              (6)
```

so every one of the four products on edge `12` belongs to

```text
span(a b,a_bar b_bar).                              (7)
```

Hence `dim(U_1U_2)<=2`.

Canonical representatives are

```text
adjacent: a=X_0+X_1,       b=X_0+X_2,
disjoint: a=X_0+X_1,       b=X_2+X_3.               (8)
```

The verifier checks rank five and (5)--(7) over `Q` for both.

## Equal supports

Normalize

```text
a=X_0+X_1,       a_bar=X_0-X_1,
b=X_0+gX_1,      b_bar=X_0-gX_1,       g!=0.        (9)
```

If `g=1`, then `b` is proportional to `a` and `b_bar` to `a_bar`; the two
rows of `U_3=<a_bar,b_bar>` are proportional, so there is no plane.

Assume `g!=1`.  Comparing the `02` and `12` coefficients of (4) gives

```text
(x_2)_2=(x_1)_2,
(x_2)_2=g(x_1)_2,                                   (10)
```

and therefore both entries vanish.  The identical `03,13` equations kill
the coordinate-three entries.  Thus `x_1,x_2` lie in
`span(X_0,X_1)`.  Every product of `U_1` and `U_2` is then a multiple of
`X_0X_1`, so

```text
dim(U_1U_2)<=1.                                     (11)
```

The endpoint `g=-1`, where `b` is proportional to `a_bar`, is included in
(10)--(11).  No projective gain or vertical kernel fibre remains.

## Consequence

The six unordered flag pairs for the two rank-one edges are

```text
AA, AB, AC, BB, BC, CC,
```

where `A=(leaf kernel, common kernel)`,
`B=(leaf kernel, common active)`, and
`C=(leaf active, common kernel)`.  The repository already named the other
five.  Equations (2)--(11) close the missing `AB` orbit without an
elimination or parameter search.

The global conjecture remains **UNRESOLVED**.

## Exact replay

```text
uv run --with sympy python claims/p4/boundaries/verify_p4_radical_crossed_211_triangle_obstruction.py
uv run --with sympy python claims/p4/boundaries/audit_p4_radical_crossed_211_triangle_obstruction.py
```

The independent audit rebuilds the squarefree product maps and never imports
the primary verifier.  All calculations are over characteristic zero;
finite fields are not used.
