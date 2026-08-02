# The three independent port-pressure additions still share the first factor

## Status

**Exact characteristic-zero no-go.**  Starting from the original
Hall-satisfying `m=7` support, add the three port incidences

```text
a_(1,0)=gamma,   b_(5,1)=delta,   a_(5,2)=epsilon.  (1)
```

They are the separate one-edge matching directions suggested by the mixed
words `0000102`, `0101010`, and `1010220`.  Nevertheless, the resulting
support cannot have all mixed `P_7` coefficients zero with
`S=C_0 C_1 C_2 != 0`.

The latter two additions do not occur in `0000102`, whose colour at blocker
5 is zero.  Hence its coefficient still shares the entire colour-zero port
binomial with `C_0`, and

```text
<C_0000102> : S^infinity = <1>.                    (2)
```

This support is genuinely different from the preceding thirty-pair shell:
none of those supports is contained in it.  Larger support enlargements and
the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite field is
used.

## Symbolic identity

Put

```text
P_0 = alpha_0 beta_1 + beta_0 gamma,
P_1 = alpha_5 beta_6 + alpha_6 delta.               (3)
```

Symbolic permanent expansion gives

```text
C_0 = P_0 X_0 X_1 X_2 X_3 X_4,
C_1 = P_1 Y_0 Y_1 Y_2 Y_3 Y_4,
C_2 = alpha_3 beta_5 Z_0 Z_1 Z_2 Z_3 Z_4.          (4)
```

The weight `epsilon` does not enter `C_2`: both `a_(5,2)` and the only
colour-two `b` incidence occupy blocker 5, so they cannot be used together.

For `w=0000102`, the last two additions in (1) are invisible, and

```text
C_w = P_0 X_0 X_1 X_3 Y_4 Z_2.                    (5)
```

Therefore

```text
S = C_w Q,
Q = X_2 X_4
    * P_1 Y_0 Y_1 Y_2 Y_3
    * alpha_3 beta_5 Z_0 Z_1 Z_3 Z_4.              (6)
```

Equation (6) is the exact principal saturation certificate (2).  Cancelling
the shared binomial `P_0` cancels `C_0` as well.

## Relation to the thirty-pair shell

After adding `a_(1,0)`, the earlier thirty supports each add two incidences
whose colours agree with `w` at their blocker.  Their purpose is to create a
third perfect matching of `0000102`.  At blocker 5 that required colour zero.

The two further incidences here are instead `[b,5,1]` and `[a,5,2]`.  Neither
is an edge of the `0000102` matching graph, and no earlier pair consists of
them.  Indeed this support leaves that graph with exactly the same two
matchings as the `a_(1,0)`-only support.  Thus it contains zero of the thirty
pair-shell supports and forms a transverse three-port shell.

## Endpoint and open conditions

All three new incidences occur at odd blockers 1 or 5, whose principal path
cofactors vanish.  They preserve exact endpoint cofactors under

```text
alpha_0=alpha_6=beta_0=1,   beta_6=-1.              (7)
```

Rank and Hall conditions cannot rescue the empty tensor locus.  They are not
the cause of the obstruction: for example, take all root variables and the
remaining old pure port weights equal to one, set `gamma=1`, `delta=2`, and
`epsilon=3`, together with (7).  Then all three pure coefficients, both port
ranks, every root span, and every local rank are nonzero, and all Hall
conditions hold.  The mixed coefficient (5) remains nonzero.

## Boundary

```text
three-port pressure support:                     EXCLUDED;
principal pure/mixed saturation identity:       PROVED;
contained thirty-pair supports:                 0/30;
endpoint cofactor legality:                     PRESERVED;
rank/Hall open conditions:                      ATTAINABLE, no escape;
larger support enlargements:                    UNKNOWN;
global Krenn-Gu conjecture:                     UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_root_m7_three_port_pressure_enlargement_shared_factor_obstruction.py
python audit_root_m7_three_port_pressure_enlargement_shared_factor_obstruction.py
uv run --with sympy --with ruff python -m ruff check verify_root_m7_three_port_pressure_enlargement_shared_factor_obstruction.py audit_root_m7_three_port_pressure_enlargement_shared_factor_obstruction.py
python -m py_compile verify_root_m7_three_port_pressure_enlargement_shared_factor_obstruction.py audit_root_m7_three_port_pressure_enlargement_shared_factor_obstruction.py
```

The primary derives (4)--(6) from symbolic permanents, verifies a legal
full-rank specialization, and compares all thirty prior supports.  The
no-import audit independently enumerates labelled perfect matchings and
checks the same factor and shell-separation statements.
