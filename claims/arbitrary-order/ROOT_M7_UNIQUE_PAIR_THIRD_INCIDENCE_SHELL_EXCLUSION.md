# The unique legal pair has no one-incidence extension

## Status

**Exact characteristic-zero bounded shell exclusion.**  Start with the fixed
Hall-satisfying seven-blocker support and the unique endpoint-legal pair that
breaks the first five principal certificates,

```text
H_6[3,0]=p,        H_5[4,0]=q.                     (1)
```

The endpoint-legal missing-incidence universe has size 104.  Removing the two
members of (1) leaves 102 possible third incidences.  Exact symbolic permanent
division proves:

1. for 101 of the 102 supports, `C_0101122` still divides
   `S=C_0 C_1 C_2` after the required endpoint normalization;
2. the unique escape is `a_5[2]=epsilon`; and
3. on that escape, `C_0101112` divides `S` instead.

Consequently every endpoint-legal one-incidence extension of (1) has

```text
I_mixed : S^infinity = <1>,                        (2)
```

so none is a diagonal `P_7` restriction.  This is the complete third shell
*above the unique pair only*.  It does not classify the other endpoint-legal
three-incidence supports, arbitrary enlarged supports, or arbitrary
Hall-satisfying `P_7`.  The local-to-global reduction and the global
Krenn--Gu conjecture remain **UNRESOLVED**.  No finite-field inference is
used.

## The 102-support shell

The fixed alternating blocker path has 90 missing root incidences and 14
legal missing port incidences at the odd blockers 1, 3, and 5.  Thus its legal
universe is

```text
|U_legal|=104.                                     (3)
```

Both incidences in (1) belong to this universe.  The shell considered here is

```text
{ {H_6[3,0],H_5[4,0],e} : e in U_legal minus (1) }, (4)
```

and therefore has exactly 102 labelled supports.  The fixed path and original
labelled port supports have trivial stabilizer, so no hidden orbit quotient is
being used.

For each support in (4), all three pure coefficients and the selected mixed
coefficient are expanded as exact polynomials over `Q`.  Polynomial division
in the ring containing every occurring weight gives 101 zero remainders for

```text
S / C_0101122.                                     (5)
```

There is exactly one nonzero remainder, at

```text
e=a_5[2].                                          (6)
```

This is the colour-two port-pressure direction already visible in the earlier
support analysis, but here it is the unique escape from (5) after the crossed
root pair (1) is present.

## Replacement certificate at the unique escape

Use the exact endpoint normalization

```text
alpha_0=alpha_6=beta_0=1,        beta_6=-1.         (7)
```

Write `X_i,Y_i,Z_i` for the original root weights and retain the original
port weights `alpha_3,alpha_5,beta_1,beta_5`.  On the support (1), (6), exact
permanent expansion gives

```text
C_0 = beta_1 X_0 X_1 X_2 (X_3 X_4+p q),
C_1 = -alpha_5 Y_0 Y_1 Y_2 Y_3 Y_4,
C_2 = alpha_3 beta_5 Z_0 Z_1 Z_2 Z_3 Z_4.          (8)
```

The added weight `epsilon` does not enter `C_2`: `a_5[2]` and the existing
colour-two `b` row both occupy blocker 5.  It also does not enter the new
mixed certificate

```text
C_0101112 = alpha_5 X_0 Y_1 Y_3 Y_4 Z_2.           (9)
```

Combining (8)--(9) yields the exact identity

```text
S = C_0101112 Q,

Q = -X_1 X_2 Y_0 Y_2 Z_0 Z_1 Z_3 Z_4
    * alpha_3 beta_1 beta_5
    * (X_3 X_4+p q).                               (10)
```

Thus nonvanishing of all three pure coefficients forces the forbidden mixed
coefficient (9) to be nonzero.  This proves (2) for the sole escape and closes
the entire shell (4).

## Boundary

```text
legal universe:                                  104 incidences;
third supports above the unique pair:            102;
C_0101122 principal certificates:                101;
unique escape from C_0101122:                    a_5[2];
replacement certificate there:                  C_0101112;
survivors in this 102-support shell:              0;
all endpoint-legal three-incidence supports:      UNKNOWN;
arbitrary Hall-satisfying P_7 restriction:        UNKNOWN;
finite-field proof:                               NONE;
global Krenn--Gu conjecture:                      UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_root_m7_unique_pair_third_incidence_shell_exclusion.py
uv run --with sympy python audit_root_m7_unique_pair_third_incidence_shell_exclusion.py
uv run --with sympy --with ruff python -m ruff check verify_root_m7_unique_pair_third_incidence_shell_exclusion.py audit_root_m7_unique_pair_third_incidence_shell_exclusion.py
python -m py_compile verify_root_m7_unique_pair_third_incidence_shell_exclusion.py audit_root_m7_unique_pair_third_incidence_shell_exclusion.py
```

The primary verifier reuses the pinned root/port data constructors and checks
all 102 polynomial divisions in `Q[weights]`.  The audit has no repository
imports: it rebuilds the support, permanent recurrence, legal universe, and
exact quotient tests independently.
