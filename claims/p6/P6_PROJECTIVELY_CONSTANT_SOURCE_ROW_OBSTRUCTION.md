# A projectively constant source row obstructs concise diagonal `P_6`

## Status

**Exact characteristic-zero structural obstruction.**  Let six local maps
from the source of `P_6` to a three-dimensional target be represented by
source-by-target matrices `M_0,...,M_5`.  If the six covectors occurring in
one fixed source row are all proportional to one target covector, then the
pullback of `P_6` cannot be a concise GHZ diagonal tensor.

Applied to the order-twelve synchronized family, this excludes every
common-four-row core in which at least one common root has projectively
constant incident covectors across the six blockers.  It does **not** exclude
cores in which all four common roots vary in projective target space, and it
does not settle unrestricted `P_6 -> Delta_3`.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Statement

Write the row covectors of the local map at target mode `u` as

```text
r_(0,u),...,r_(5,u) in (C^3)^*.                       (1)
```

Suppose that for one source row, say row zero, there are scalars `kappa_u`
and one covector `ell` such that

```text
r_(0,u)=kappa_u ell       for u=0,...,5.               (2)
```

No nonvanishing assumption on the `kappa_u` is needed.  If `ell=0`, the
pulled-back tensor is immediately zero; hence assume below that `ell!=0`.
Then

```text
(M_0 tensor ... tensor M_5) P_6
```

is not a concise tensor in the GHZ diagonal plane.

## Equal-input polynomial

Evaluate all six target modes at the same vector `t=(t_0,t_1,t_2)`.  The
resulting homogeneous sextic is

```text
F(t)=per([r_(i,u)(t)]_(i,u=0,...,5)).                  (3)
```

Every permanent monomial uses row zero exactly once.  By (2), every monomial
therefore contains the common factor `ell(t)`, and

```text
ell(t) divides F(t).                                   (4)
```

This argument allows cancellations: divisibility holds term by term before
any terms are collected.

If the pulled-back tensor were a concise diagonal, then for nonzero scalars
`lambda_0,lambda_1,lambda_2` its equal-input polynomial would instead be

```text
F(t)=lambda_0 t_0^6+lambda_1 t_1^6+lambda_2 t_2^6.    (5)
```

The ternary diagonal sextic in (5) has no linear factor over a
characteristic-zero field.  One direct proof is as follows.  If a proposed
factor line has equation

```text
alpha t_0+beta t_1+gamma t_2=0                        (6)
```

with `gamma!=0`, substitute
`t_2=-(alpha t_0+beta t_1)/gamma`.  The coefficients of
`t_0^5 t_1` and `t_0 t_1^5` force `alpha beta=0`.  If `alpha=0`, the surviving
`lambda_0 t_0^6` term prevents the restriction from vanishing identically;
if `beta=0`, the surviving `lambda_1 t_1^6` does the same.  If `gamma=0`,
restricting to the line in the `(t_0,t_1)` variables leaves the nonzero term
`lambda_2 t_2^6`.  Thus no line divides (5).

Equations (4) and (5) contradict one another.  Hence a projectively constant
source row is impossible in a concise diagonal `P_6` restriction.

## Synchronized-family consequence

In the maximal-overlap order-twelve notation, the six maps have four fixed
common-root rows

```text
H_u[i,-]=B_(i,u)(x_i,-),       i in I, u in B,         (7)
```

followed by the two exchanged rows.  Therefore any prospective quotient-zero
surface or quotient-rank-one isotropic curve must satisfy

```text
dim span{H_u[i,-]:u in B} >= 2       for every i in I. (8)
```

This is independent of the blocker--blocker cofactor, the cross-form value
`delta`, and the target-frame divisor `Theta`.  It removes the complete
projectively constant common-root stratum before those later splits.

## Boundary

```text
one projectively constant source-row family: EXCLUDED;
all four common-root row families projectively varying: UNKNOWN;
quotient-zero surface: UNKNOWN outside the fixed-core obstruction;
quotient-rank-one synchronized curve: UNKNOWN;
unrestricted P_6 -> Delta_3: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```text
uv run --with sympy python claims/p6/verify_p6_projectively_constant_source_row_obstruction.py
python claims/p6/audit_p6_projectively_constant_source_row_obstruction.py
```

The primary verifier expands the symbolic six-by-six permanent by subset
dynamic programming, checks its exact linear factor, and checks the line
restriction coefficient argument over a characteristic-zero polynomial
ring.  The no-import audit independently enumerates all `6!=720` permanent
assignments and checks the case split for a diagonal sextic using integer
coefficient dictionaries.  No finite-field inference is used.
