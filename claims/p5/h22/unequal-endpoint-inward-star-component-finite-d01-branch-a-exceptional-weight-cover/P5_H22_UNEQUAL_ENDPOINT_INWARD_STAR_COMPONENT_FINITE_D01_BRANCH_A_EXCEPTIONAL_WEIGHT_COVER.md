# Exceptional-weight cover on component twenty-five's finite-`D01` `A` branch

## Status

**Exact characteristic-zero retained-weight projection.**  On the ordinary
finite-`D01` branch `A=0`, every surviving binary candidate is supported on

```text
(js-1)lambda-(js+1)=0.                              (1)
```

The second factor in the full projection is `lambda+1`; that fibre was closed
by the separate finite-`D01`, `lambda=-1` obstruction.  Thus (1) is the only
remaining exceptional-weight divisor on this branch.  This certificate does
not test (1), close the `A` branch, or address the parallel `B=0` branch.
The generic weighted `H22` fibre therefore remains **UNKNOWN**, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact retained-weight elimination

Put

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
F=PR-Q^2.
```

Work over `C(e,j,s)` and retain both `k` and `lambda`.  In the polynomial ring

```text
C(e,j,s)[z0,z1,z3,z5,z6,z7,w,k,lambda],            (2)
```

let `J_A` contain `F`, the three forced mode-zero mixed coordinates, the
normalization `C_0000-1`, the denominator-free `A=0` equation, the
denominator-free linear residual from `S_13`, and the last two Segre equations

```text
S_23 =C_0011 C_0000-C_0010 C_0001,
S_123=C_0111 C_0000^2-C_0100 C_0010 C_0001.        (3)
```

An exact block-order standard-basis calculation eliminates the seven extension
variables and gives

```text
J_A intersect C(e,j,s)[k,lambda]
 = ( F,
     (js-1)lambda^2-2lambda-(js+1) )
 = ( F,
     (lambda+1)((js-1)lambda-(js+1)) ).            (4)
```

Consequently every solution on the ordinary chart `lambda^2 != 1` satisfies
(1).  If `js != 1`, this is equivalently

```text
lambda=(js+1)/(js-1).                              (5)
```

When `js=1`, equation (1) is the nonzero constant `-2`, so this branch has no
ordinary survivor.  No division by `js-1` is used in (4).

## Boundaries and replay

The same component-chart denominators as in the preceding linear-reduction
certificate remain assumed nonzero:

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1).
```

Equation (4) is a necessary-and-exact elimination statement for the terminal
ideal; it is not an assertion that the residual divisor (1) is populated.
That divisor, the `B=0` branch, and the projective/component-boundary fibres
remain outside this theorem.  No finite-field computation is used as proof.

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-exceptional-weights/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_weights.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-exceptional-weights/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_weights.py
```

The primary verifier reconstructs the certified component model.  The audit
imports no project code, rebuilds every permanent coefficient by subset dynamic
programming, and independently repeats the retained-weight elimination.  Each
Singular call is capped at 120 seconds.
