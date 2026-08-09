# The unique one-edge port escape shares the pure coefficient factor

## Status

**Exact characteristic-zero no-go for the first enlarged support.**  Start
with the fixed `m=7` Hall-satisfying two-port support and add only

```text
a_(1,0)=gamma.                                      (1)
```

This is the unique single incidence that gives the old mixed obstruction
`0000102` a second perfect matching.  Nevertheless, it does not permit
cancellation while preserving the pure coefficient.  The new matching also
appears in the pure word `0^7`, so both coefficients acquire the same port
binomial.  An exact monomial identity gives

```text
<C_0000102> : (C_0 C_1 C_2)^infinity = <1>.         (2)
```

Thus all mixed coefficients cannot vanish with all three pure coefficients
nonzero.  This precedes endpoint-cofactor, Hall, and rank conditions.  Those
conditions are compatible with the pure open set and do not provide an
escape.  The arbitrary-support `P_7` problem and global Krenn--Gu conjecture
remain **UNRESOLVED**.  No finite field is used.

## Shared binomial

Use the symbolic zero pattern of the preceding fixed-support obstruction and
write

```text
P = alpha_0 beta_1 + beta_0 gamma.                 (3)
```

The two port rows on colour-zero columns 0 and 1 form a symbolic `2 x 2`
permanent with value `P`.  The pure coefficients are

```text
C_0 = P X_0 X_1 X_2 X_3 X_4,
C_1 = alpha_5 beta_6 Y_0 Y_1 Y_2 Y_3 Y_4,
C_2 = alpha_3 beta_5 Z_0 Z_1 Z_2 Z_3 Z_4.          (4)
```

For `w=0000102`, the root matching uses
`X_0,X_1,X_3,Y_4,Z_2`, while the same two port matchings survive.  Hence

```text
C_w = P X_0 X_1 X_3 Y_4 Z_2.                      (5)
```

In particular, setting `P=0` cancels both `C_w` and `C_0`.

## One-generator saturation certificate

Let `S=C_0 C_1 C_2`.  Every factor of `C_w` occurs in `S`, including the
binomial `P`.  Direct division gives the polynomial monomial

```text
Q = S/C_w
  = X_2 X_4
    * alpha_5 beta_6 Y_0 Y_1 Y_2 Y_3
    * alpha_3 beta_5 Z_0 Z_1 Z_3 Z_4.              (6)
```

Therefore

```text
S = C_w Q.                                         (7)
```

Equation (7) puts `S` in the principal mixed ideal `<C_w>`, so `1` lies in
`<C_w>:S`, proving (2).  Equivalently, `S != 0` forces `C_w != 0` over every
field.  The conclusion allows arbitrary specialization of all symbolic
weights; no torus assumption beyond the requested pure nonvanishing is used.

## Endpoint and rank checks after the `P_7` obstruction

Blocker 1 has zero principal path cofactor, so (1) does not change either
endpoint cofactor.  Exact compatibility remains

```text
alpha_0=alpha_6=beta_0=1,   beta_6=-1.              (8)
```

Nonvanishing of (4) forces `P`, all `X_r,Y_r,Z_r`, and the six displayed
pure port factors to be nonzero.  It then supplies:

- rank three for both port families via minors
  `alpha_0 alpha_5 alpha_3` and `beta_1 beta_6 beta_5` under (8);
- rank three for each root-row family via `X_r Y_r Z_r`;
- a coordinate-triangular nonzero local minor at every blocker; and
- the three colourwise Hall conditions.

Thus loss of concision is not responsible for (2).

## Next minimal support deformation

For `w=0000102`, the enlarged support has exactly two perfect matchings: the
two port matchings on columns 0 and 1 times one fixed root matching.  Exhaustive
bipartite matching enumeration proves that **no single further incidence**
creates a third matching.  At least two new incidences are required merely to
break the shared factor in (3)--(5).

The minimal two-incidence possibilities have a clean structural
classification.  Write the root matching as

```text
mu: r_0->2, r_1->3, r_2->6, r_3->5, r_4->4.        (9)
```

Exactly 30 unordered pairs create an additional matching:

1. **Ten root swaps.**  Choose two root rows `r,s` and add both crossed
   incidences `r->mu(s)` and `s->mu(r)`.  This creates a root alternating
   4-cycle.
2. **Twenty root--port exchanges.**  Choose a root row `r`, a port column
   in `{0,1}`, and a port row in `{a,b}`.  Add the root incidence to that
   port column and the chosen port-row incidence to `mu(r)`.

These 10+20 pairs are all the two-edge possibilities for this word.  They
are necessary combinatorial escape candidates only; none is claimed to
solve the other mixed equations.

Two other unique-matching words show additional pressure.  `0101010` has
the unique one-edge escape `b_(5,1)`, while `1010220` has the distinct escape
`a_(5,2)`; no single new root incidence helps either word.  These facts do
not strengthen the proven lower bound beyond two additions, but they give
concrete filters for the next enlarged-support search.

## Boundary

```text
original support plus a_(1,0):                    EXCLUDED;
principal mixed ideal saturated by pure product: UNIT IDEAL;
endpoint binary cofactors:                        COMPATIBLE, no escape;
Hall/root-span/local-rank conditions:              COMPATIBLE, no escape;
further incidences required:                      AT LEAST TWO;
30 minimal pairs for the witness word:            CLASSIFIED;
arbitrary enlarged-support P_7 restriction:       UNKNOWN;
global Krenn-Gu conjecture:                        UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py
python claims/arbitrary-order/audit_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py
uv run --with sympy --with ruff python -m ruff check verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py audit_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py
python -m py_compile verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py audit_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py
```

The primary derives the coefficients from symbolic permanents, verifies (7),
checks endpoint/rank/Hall data, and enumerates every one- and two-incidence
deformation.  The no-import audit independently enumerates labelled matchings
and checks the same factor identity and 10+20 classification.
