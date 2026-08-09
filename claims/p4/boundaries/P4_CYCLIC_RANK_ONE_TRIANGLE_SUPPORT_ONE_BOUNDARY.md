# Singleton cyclic triangles are toric boundaries of components 16 and 17

## Status

**Exact characteristic-zero boundary classification.** Let three marked
planes of a nonzero pure `P_4` restriction form a triangle of rank-three pair
images with cyclic rank-one relations

```text
y_1x_2=0,       y_2x_3=0,       x_1y_3=0.          (1)
```

If at least one of the three zero products has support one, then the tuple
lies in the closure of component sixteen or seventeen.  More precisely, all
nonzero rank-three support data reduce to three source-support multisets;
one is a toric boundary of the support-star component and two are boundaries
of the support-path component.  Thus singleton zero products create no
eighteenth pure-`P_4` component.

Combined with the genuine support-two theorem, this completes the cyclic
rank-one triangle orientation.  The statement is at the pure-`P_4` plane
level and does not settle other exceptional graphs, marked `P_5` fibres, or
the global Krenn--Gu conjecture.

## Loops in the exact-zero-divisor support graph

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).   (2)
```

A genuine binary exact pair has support edge `ij` and factors

```text
(X_i+lambda X_j)(X_i-lambda X_j)=0.                (3)
```

A support-one pair is instead

```text
X_i^2=0.                                           (4)
```

It is useful to draw (4) as a loop at source vertex `i`.  The earlier
`C^*`-gain graph has therefore acquired loops on the boundary.  A loop is
the initial form of an ordinary gained edge:

```text
(X_i+epsilon lambda X_j)(X_i-epsilon lambda X_j)
   -> X_i^2.                                       (5)
```

This is a one-parameter-subgroup degeneration of the diagonal source torus,
the same elementary mechanism that underlies toric initial forms.  It turns
the support-one question into a graph-lifting question.

## The fourteen support orbits collapse to three

Ignoring orientation momentarily, there are fourteen `S_4`-orbits of
three-label multisets made from the four loops and six edges and containing
at least one loop.  Plane nondegeneracy, the three pair-rank conditions, and
apolar separation leave exactly

```text
A: {0, 01, 23},
B: {0, 12, 13},
C: {0, 1, 23}.                                     (6)
```

Every ordering of each multiset is allowed on a dense gain open.  All other
eleven orbits have a collapsed plane, a pair image of rank at most two, a
zero active cubic, or proportional kernel and active cubics.  This is a
constant orbit calculation, not a parameter search: the verifier treats the
three nonzero gains as algebraically independent and checks polynomial
identities on the fourteen support types.

For the displayed cyclic order, the kernel and active triple covectors
`C=y_1y_2y_3`, `D=x_1x_2x_3` are respectively

```text
A: C=(0,0,-lambda_2 lambda_3, lambda_2),
   D=(0,0,-lambda_2 lambda_3,-lambda_2),

B: C=(0,-lambda_2 lambda_3,-lambda_3, lambda_2),
   D=(0,-lambda_2 lambda_3, lambda_3,-lambda_2),

C: C=(0,0,-lambda_3,1),
   D=(0,0, lambda_3,1).                             (7)
```

In every case the three leaf-pair ranks are `(3,3,3)` and `C,D` are
independent for nonzero gains.  Hence the opposite plane is any point of
the open apolar fibre

```text
Gr(2,ker C) minus Gr(2,ker C cap ker D).             (8)
```

## Lift the loops to trees

Each support multiset in (6) has a direct gained-tree opening:

```text
A: {0,01,23}  <-epsilon- {02,01,23},   source path,
B: {0,12,13}  <-epsilon- {01,12,13},   source star,
C: {0,1,23}   <-epsilon- {02,13,23},   source path. (9)
```

For example, replace the loop factor `X_0` in case A by
`X_0 plus-or-minus epsilon*kappa*X_2`.  In case C make both replacements

```text
X_0 -> X_0 plus-or-minus epsilon*kappa*X_2,
X_1 -> X_1 plus-or-minus epsilon*eta*X_3.           (10)
```

For every `epsilon!=0`, the support graphs in (9) are forests.  Gain-graph
switching removes all their nonzero gains, so the first and third punctured
families are component seventeen and the second is component sixteen.
Their three marked leaf planes converge in Pluecker coordinates to the
given singleton triangle.

The opposite plane lifts as well.  If `C(epsilon)` is the moving kernel
covector and `C(0)_j!=0`, any target row `w in ker C(0)` has the exact lift

```text
w(epsilon)=w-
  C(epsilon)(w)/C(epsilon)(e_j) * e_j.              (11)
```

Then `C(epsilon)(w(epsilon))=0` and `w(epsilon)->w`.  Apply (11) to a basis
of the target plane.  Detection by `D(epsilon)` is an open condition, so it
persists on a punctured neighbourhood.  This proves containment of the
entire apolar fibre (8), not merely one chosen representative.

## Consequence for the rank-one triangle frontier

The cyclic orientation is now complete:

```text
three genuine support-two pairs -> components 16,17,8 or lower-pair,
at least one support-one pair   -> components 16 or 17 boundary. (12)
```

Together with the transitive-orientation theorem, both tournaments on a
rank-one exceptional triangle are classified.  The new conceptual point is
that singleton zero products are not separate algebraic species: they are
toric initial forms of gained forest edges.

## Exact replay

```text
uv run --with sympy python claims/p4/boundaries/verify_p4_cyclic_rank_one_triangle_support_one_boundary.py
python claims/p4/boundaries/audit_p4_cyclic_rank_one_triangle_support_one_boundary.py
```

The primary verifier performs the fourteen-orbit calculation over a rational
function field, checks (7), verifies all three Pluecker arcs in (9), and
checks the general apolar correction (11).  The independent audit uses
subset-dynamic-programming permanents and rational row reduction.  Neither
script searches for parameter values or graph instances.
