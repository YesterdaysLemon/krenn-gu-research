# GLD90 hostile review: H4 Q6-open low-rank exclusion

## Review disposition

**Accepted as an exact scoped theorem package, subject to the unchanged global
status `UNRESOLVED`.**  The reviewed claim is

```text
B intersect V(I_7(A)) intersect D(Omega Delta Q6) intersect H4 = empty,
Delta=(p-q)(p+q-1)P L1 L2 e.
```

It does not claim that `Q6=0`, `L1=0`, `L2=0`, or `e=0` is empty; it does
not compute the pulled-back `GLD83` Fitting ideal; and it does not cover other
charts, components, gauges, source branches, profiles, roots, or orders.

## Evidence inspected

The primary verifier
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_open_low_rank_exclusion.py`
reconstructs the fixed `37 x 9` `GLD71` syndrome matrix and checks exactly:

1. the old and alternate raw six-pivot factors, including their common `Q6`;
2. the alternate bordered-residual determinant `-6 Delta` and exact recovery
   of the accepted `GLD88` family;
3. the `X0=X1=0` solution on `D((p-q)T)`;
4. both auxiliary six-pivot factors and their bordered resultants;
5. equality of the double-pivot family with the `GLD88` family modulo the
   displayed residual curve `R`;
6. the `U=0`, `V=0`, and `V=0,p^2+2=0` exceptional coefficient cases;
7. the complete factor-pair cover leaving four corners and coprime exact
   seven-minors at every corner;
8. a nonempty algebraic sample on `R=0` with all declared parameter factors
   nonzero; and
9. the full `T=0` two-pivot obstruction and an exact rational sample on
   `T=X0=0` with alternate pivot nonzero and syndrome rank six.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_open_low_rank_exclusion.py`
imports neither the primary nor the `GLD71` builder.  It parses the immutable
`GLD75` carrier, independently reconstructs its scale-fixed center-linear
system, verifies the `R`-family and one complete rank-six solution fibre,
replays the finite corner cover, rederives the `T=0` two-pivot obstruction,
and verifies the complete two-dimensional center fibre at the rational
`T=X0=0` sample.  It explicitly does not claim an independent reconstruction
of the primary Schur resultants or corner seven-minors.

Both exact replays pass on the reviewed candidate tree.

## Adversarial findings

### Corrected exceptional-chart dependency

The first draft correctly found

```text
R|_(V=0)=3p(p-2)(p^2+2)P^2,
```

but attempted to certify the `p^2+2=0` backup `c` equation with a chart-B
coefficient.  Chart B's pivot also vanishes on that special fibre, so that
would not have justified division by the chart-B pivot.  The reviewed primary
now uses chart A: its pivot factor is coprime to `p^2+2`, and its backup
coefficient is independently coprime to `p^2+2`.  The theorem document states
this chart choice explicitly.  No claim relies on the rejected chart-B step.

### Rank and center-singularity logic

The proof does not infer a global rank statement from one sample.  In each
positive-dimensional branch, a named nonzero old, alternate, or auxiliary
six-pivot gives rank at least six, while membership in `V(I_7(A))` and the
`C_8=1` bridge give full syndrome rank at most six.  The exact `GLD88` kernel
identities then make the three-dimensional kernel precisely the three
block-supported copies of one row line.  Every compatible actual center has
proportional rows, hence `det(C)=0`.  The contradiction is with the explicit
`D(Omega)` determinant gate.

At the four zero-auxiliary-pivot corners the argument is different: coprime
seven-minors show rank at least seven for every remaining `c`, so those points
cannot enter the low-rank branch.  These two mechanisms are not conflated.

### T=0 is closed without dividing by T

The double-pivot rational solution is used only on `D(T)`.  The closed
`T=0` divisor is reparameterized separately by

```text
q=(p-2)/(2p-1).
```

The case `2p-1=0` is inconsistent with `T=0`.  On the parameterization,
`Q6=8P^4/(2p-1)^4`, and the two pivot brackets differ by `4P`.  Since the
declared open contains `D(P)`, at least one pivot is nonzero.  The old or
alternate bordered system therefore applies without inverting `T`.  This is
a genuine closure of the formerly exceptional divisor, not a localization
that silently discards it.

## Remaining obligations

| residual | reviewed disposition |
| --- | --- |
| `Q6=0` | open; common factor of the old and alternate raw six-pivots |
| `L1=0`, `L2=0`, `e=0` | open coefficient-boundary intersections |
| `P=0`, `d0=0` | separately closed by `GLD89`, not reproved here |
| pulled-back `GLD83` Fitting ideal | not computed |
| rank-seven and rank-eight chart coverage | only existing scoped GLD84/GLD85/GLD91 results apply |
| other gauges/components/source branches | open |
| global Krenn--Gu conjecture | **UNRESOLVED** |

The package is therefore a substantial H4 low-rank closure on one explicit
principal open, not a universal source-cover theorem and not a resolution of
the prize conjecture.
