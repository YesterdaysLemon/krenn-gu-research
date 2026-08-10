# All endpoint-legal three-incidence enlargements are excluded

## Status

**Exact characteristic-zero bounded classification.**  For the fixed
Hall-satisfying seven-blocker support, there are 104 endpoint-legal missing
incidences.  Every unordered three-incidence enlargement is incompatible with
vanishing of all mixed `P_7` coefficients and nonvanishing of
`S=C_0 C_1 C_2`.

Exact symbolic permanent division checks all

```text
binomial(104,3)=182,104                             (1)
```

supports.  Six earlier certificate words exclude 182,095 supports.  Exactly
nine relative survivors remain, and the single additional word

```text
2002000                                             (2)
```

gives a principal saturation certificate on all nine.  Therefore every
support in this shell has

```text
I_mixed : S^infinity = <1>.                        (3)
```

This is a complete theorem only for three endpoint-legal additions to this
one pinned Hall-satisfying architecture.  It is not an exclusion of arbitrary
larger supports or arbitrary `P_7 -> Delta_3`, and it does not prove the
arbitrary-order local-to-global step.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.  No numerical or finite-field inference is used.

## Legal universe and certificate census

As in the preceding hitting theorem, all 90 missing root--blocker incidences
are endpoint-legal.  New port incidences are legal only at the odd blockers
1, 3, and 5; fourteen such entries are missing.  Hence

```text
|U_legal|=90+14=104.                               (4)
```

For every `T in binomial(U_legal,3)`, introduce three independent weights,
impose the exact endpoint normalization

```text
alpha_0=alpha_6=beta_0=1,       beta_6=-1,          (5)
```

and expand the pure product and selected mixed coefficients in the polynomial
ring over `Q` containing every occurring weight.  Testing the first exact
divisor in the fixed word order gives

```text
word        first-certificate supports
0000102                         179,884
1112101                           1,768
1112220                             326
0101010                               5
1010220                               0
0101122                             112
total                            182,095.           (6)
```

The zero in (6) means only that `1010220` is never the *first* divisor in this
ordering; it is retained because it was part of the previously frozen
certificate family.  Every successful test is exact polynomial division with
zero remainder, not evaluation at sample weights.

## The nine relative survivors

Write `(i,u,c)` for the root incidence `H_u[i,c]`, `(a,u,c)` for `a_u[c]`,
and `(b,u,c)` for `b_u[c]`.  The six words in (6) leave exactly

```text
{(0,3,1),(3,4,1),(4,0,1)}
{(0,4,1),(3,0,1),(4,3,1)}
{(0,5,0),(3,6,0),(4,2,0)}
{(0,6,0),(3,2,0),(4,5,0)}
{(1,4,1),(4,5,1),(a,1,1)}
{(1,4,1),(4,5,1),(b,1,1)}
{(2,3,1),(3,4,1),(4,2,1)}
{(2,4,1),(3,2,1),(4,3,1)}
{(3,6,0),(4,5,0),(a,5,2)}.                         (7)
```

The last line is the unique-pair extension isolated in
[`ROOT_M7_UNIQUE_PAIR_THIRD_INCIDENCE_SHELL_EXCLUSION.md`](ROOT_M7_UNIQUE_PAIR_THIRD_INCIDENCE_SHELL_EXCLUSION.md).
The first eight are distinct monochromatic crossed-root or odd-port triangles
that do not contain that pair.

## One final word excludes all nine

For each support in (7), exact expansion supplies a nonzero polynomial `Q_T`
such that

```text
C_0(T) C_1(T) C_2(T) = C_2002000(T) Q_T.           (8)
```

The factor is structural.  On the first two supports, for example,

```text
C_2002000 = X_0 X_2 X_3 X_4 Z_1 alpha_3 beta_1,

Q_T = -X_1 Y_1 Y_2 Z_0 Z_2 Z_3 Z_4 alpha_5 beta_5
      * (Y_0 Y_3 Y_4+t_0 t_1 t_2).                (9)
```

On the two colour-zero crossed-root supports, the new cubic instead occurs
inside the mixed coefficient:

```text
C_2002000
 = X_2 Z_1 alpha_3 beta_1
   * (X_0 X_3 X_4+t_0 t_1 t_2),                    (10)
```

and the remaining pure factors form `Q_T`.  The other five supports have the
same exact divisibility pattern, including the signed odd-port binomial and
the earlier unique-pair quadratic.  Both verifiers reconstruct all nine
quotients and check (8) by expansion.

On `S!=0`, (8) forces the forbidden mixed coefficient `C_2002000` to be
nonzero.  This excludes all nine relative survivors and proves (3) for every
one of the 182,104 supports.

## Boundary

```text
endpoint-legal missing incidences:                104;
unordered three-incidence supports:               182,104;
supports excluded by six prior words:             182,095;
relative survivors:                               9;
relative survivors excluded by C_2002000:         9/9;
survivors in the complete triple shell:           0;
four-or-more-incidence enlargements:               UNKNOWN;
arbitrary Hall-satisfying P_7 restriction:         UNKNOWN;
arbitrary-order local-to-global reduction:         UNKNOWN;
finite-field proof:                                NONE;
global Krenn--Gu conjecture:                       UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_all_endpoint_legal_three_incidence_supports_exclusion.py
uv run --with sympy python claims/arbitrary-order/audit_root_m7_all_endpoint_legal_three_incidence_supports_exclusion.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_m7_all_endpoint_legal_three_incidence_supports_exclusion.py claims/arbitrary-order/audit_root_m7_all_endpoint_legal_three_incidence_supports_exclusion.py
python -m py_compile claims/arbitrary-order/verify_root_m7_all_endpoint_legal_three_incidence_supports_exclusion.py claims/arbitrary-order/audit_root_m7_all_endpoint_legal_three_incidence_supports_exclusion.py
```

The primary verifier reuses the pinned support constructors and checks the
entire exact census.  The audit has no repository imports: it independently
rebuilds the sparse support, permanent recurrence, legal universe, polynomial
division, nine-support ledger, and final certificates.  On the reference
machine each full exact replay takes several minutes; a timeout is not proof
of failure or emptiness.
