# The nine relative triples have no one-incidence extension

## Status

**Exact characteristic-zero bounded shell exclusion.**  The complete
three-incidence census leaves nine supports after its first six certificate
words; `C_2002000` then excludes all nine.  Add one further endpoint-legal
incidence to any of those nine relative triples.  After deduplication there
are 908 distinct four-incidence supports.

Exact symbolic permanent division proves:

1. `C_2002000` still divides `S=C_0 C_1 C_2` on 898 supports;
2. exactly ten supports escape that certificate;
3. `C_0220212` divides `S` on eight escapes; and
4. `C_0210220` divides `S` on the other two.

Thus every support in this relative fourth shell has

```text
I_mixed : S^infinity = <1>.                        (1)
```

This is not the complete set of `binomial(104,4)=4,598,126`
endpoint-legal quadruples: it covers only quadruples containing at least one
of the nine relative triples from the preceding six-word census.  The other
quadruples, arbitrary larger supports, arbitrary `P_7 -> Delta_3`, the
local-to-global reduction, and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.  No numerical or finite-field inference is used.

## Exact shell

Let `U_legal` be the 104-incidence endpoint-legal universe and let
`T_1,...,T_9` be the nine relative triples listed in
[`ROOT_M7_ALL_ENDPOINT_LEGAL_THREE_INCIDENCE_SUPPORTS_EXCLUSION.md`](ROOT_M7_ALL_ENDPOINT_LEGAL_THREE_INCIDENCE_SUPPORTS_EXCLUSION.md).
The raw extension ledger has

```text
9*(104-3)=909                                      (2)
```

triple--edge pairs.  One quadruple contains two of the relative triples, so
deduplication leaves

```text
|{T_j union {e}:e in U_legal minus T_j}|=908.      (3)
```

After imposing the exact endpoint normalization, exact division in the full
rational polynomial ring gives

```text
S(T) = C_2002000(T) Q_T                           (4)
```

for 898 of these supports.

## The ten escapes and replacement certificates

Nine of the ten escapes add the same odd-blocker port incidence

```text
a_1[0].                                            (5)
```

There is one such extension above each relative triple.  The tenth extends
the last relative triple

```text
{H_6[3,0],H_5[4,0],a_5[2]}                         (6)
```

by the other odd-port incidence

```text
b_3[2].                                            (7)
```

The exact replacement ledger is

```text
certificate       supports
C_0220212                 8
C_0210220                 2.                       (8)
```

For every line of (8), the verifier constructs a polynomial `R_T` and checks

```text
S(T)=C_v(T) R_T                                   (9)
```

by full expansion over `Q`.  Hence pure nonvanishing forces one forbidden
mixed coefficient to be nonzero.  The two-word ledger (8), rather than a
single-word overstatement, is essential: the independent audit catches the
two odd-port variants on which `C_0220212` alone is not a divisor.

## Boundary

```text
relative triples:                                9;
raw legal one-edge extensions:                   909;
distinct four-incidence supports:                908;
C_2002000 certificates retained:                 898;
relative escapes:                                10;
C_0220212 / C_0210220 replacement counts:        8 / 2;
survivors in this relative fourth shell:          0;
all endpoint-legal four-incidence supports:       UNKNOWN;
arbitrary Hall-satisfying P_7 restriction:        UNKNOWN;
arbitrary-order local-to-global reduction:        UNKNOWN;
finite-field proof:                               NONE;
global Krenn--Gu conjecture:                      UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_relative_triple_fourth_incidence_shell_exclusion.py
uv run --with sympy python claims/arbitrary-order/audit_root_m7_relative_triple_fourth_incidence_shell_exclusion.py
uv run --with sympy --with ruff python -m ruff check verify_root_m7_relative_triple_fourth_incidence_shell_exclusion.py audit_root_m7_relative_triple_fourth_incidence_shell_exclusion.py
python -m py_compile verify_root_m7_relative_triple_fourth_incidence_shell_exclusion.py audit_root_m7_relative_triple_fourth_incidence_shell_exclusion.py
```

The primary verifier reuses the pinned exact support constructors.  The audit
has no repository imports and independently rebuilds the support, permanent
recurrence, legal universe, deduplicated fourth shell, and polynomial
divisibility tests.
