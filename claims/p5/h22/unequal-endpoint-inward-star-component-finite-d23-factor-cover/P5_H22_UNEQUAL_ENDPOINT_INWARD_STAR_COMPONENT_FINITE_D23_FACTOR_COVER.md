# A three-branch factor cover for component twenty-five's finite `D23` orbit

## Status

**Exact characteristic-zero supplemental reduction.**  Every finite-`D23`
binary candidate over the generic point of component twenty-five lies in one
of three explicit linear branches.

The branches are not excluded here.  Thus finite `D23`, the residual
finite-`D01` branches, and the full generic weighted `H22` fibre remain
**UNKNOWN**.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Canonical coefficients

Put

```text
P=ej+k^2,       Q=e+j,
F=P(1+ejs^2)-Q^2.
```

For finite weight `[lambda:1]`, contract the source `23` block by

```text
(x,e) -> (x_0,x_1,lambda x_2+x_3,e).               (1)
```

Let `C_w` be the resulting canonical binary coordinates in the intrinsic
pure basis.  The following identities hold before quotienting by `F`:

```text
C_0100=Q C_1100,
C_1100=2(lambda-1)z_2,
C_1000=2(lambda-1)(Ps z_4+Qz_2).                  (2)
```

Define

```text
G=(lambda-1)(z_0-Qz_4)-P(lambda+1)z_3,
J=js(kz_3-z_5)-z_2.                                (3)
```

Two further exact identities are

```text
C_0000-Q C_1000=2Ps G,                             (4)

C_0101-Q C_1101
 =2[js k(lambda-1)(z_0-Qz_4)
    -P(lambda+1)(jsz_5+z_2)]
 =2[P(lambda+1)J+jksG].                            (5)
```

## Fixed-vertex factor cover

A genuine binary neighbour has `C_0000 != 0` and satisfies the
fixed-vertex Segre equations.  The equation for subset `{0,1}`, together
with (2), factors as

```text
C_1100(C_0000-Q C_1000)=0.                         (6)
```

Hence either

```text
A23: (lambda-1)z_2=0,                              (7)
```

or `G=0`.  On the latter branch, the `{1,3}` and `{0,1,3}` Segre equations
combine with (5) to force

```text
(lambda+1)J=0.                                     (8)
```

Thus every candidate lies in the three-branch cover

```text
A23:             (lambda-1)z_2=0,
G23_endpoint:    G=0, lambda=-1,
G23_ordinary:    G=0, J=0.                         (9)
```

No extension coordinate was divided out, and the cover is uniform over the
complete finite weight line.

## Boundary and replay

The three branches in (9) remain to be analyzed.  The generic inference
from (4) uses `Ps != 0`; `P=0`, `s=0`, the quadratic leading divisor
`1+ejs^2=0`, and projective component-boundary fibres remain outside the
claim.  No finite-field computation is used as proof.

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d23-factor-cover/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d23_factor_cover.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d23-factor-cover/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d23_factor_cover.py
```

The primary verifier constructs all canonical coefficients from the
certified component model and checks (2)--(8).  The audit imports no project
code, reconstructs the permanent tensor by subset dynamic programming, and
repeats every identity independently.
