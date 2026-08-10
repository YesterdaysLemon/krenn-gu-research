# All thirty minimal two-incidence enlargements are excluded

## Status

**Exact characteristic-zero bounded classification.**  Add `a_(1,0)` to the
fixed Hall-satisfying `m=7` support, then consider the thirty minimal pairs of
new incidences that create a third matching for `w=0000102`.  Every one of
the thirty enlarged supports is incompatible with vanishing of all mixed
`P_7` coefficients and nonvanishing of `S=C_0 C_1 C_2`.

For fifteen supports, `C_w` divides `S`.  For fourteen others, the monomial
coefficient `C_1112101` divides `S`; for the last support,
`C_1112220` divides `S`.  Thus each representative has a one-generator exact
saturation certificate

```text
<C_v> : S^infinity = <1>.                           (1)
```

The stabilizer of the fixed coloured path and the two labelled port-support
families is trivial, even allowing path reversal, a colour permutation, and
interchange of the port labels.  Hence the thirty supports are thirty
singleton orbits.

This excludes only this minimal two-incidence shell.  Larger support
deformations, arbitrary Hall-satisfying `P_7`, the arbitrary-order reduction,
and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite-field
inference is used.

## Representatives and certificates

Put

```text
w=(0,0,0,0,1,0,2).
```

Write `[r,u]` for the new root incidence `H_u[r,w_u]`, and `[a,u]` or
`[b,u]` for the corresponding port incidence.  The thirty pairs split as
follows.

The fifteen supports for which `C_w` divides `S` are

```text
[r0,0][a,2]   [r0,0][b,2]   [r0,1][a,2]   [r0,1][b,2]
[r0,3][r1,2]  [r0,5][r3,2]
[r1,0][a,3]   [r1,0][b,3]   [r1,1][a,3]   [r1,1][b,3]
[r1,5][r3,3]
[r3,0][a,5]   [r3,0][b,5]   [r3,1][a,5]   [r3,1][b,5]. (2)
```

For fourteen further supports, the unchanged coefficient

```text
C_1112101 = X_3 Y_0 Y_1 Y_2 Y_4 alpha_3 beta_6     (3)
```

divides `S`:

```text
[r0,4][r4,2]  [r0,6][r2,2]
[r1,4][r4,3]  [r1,6][r2,3]
[r2,0][a,6]   [r2,0][b,6]   [r2,1][a,6]   [r2,1][b,6]
[r2,4][r4,6]  [r2,5][r3,6]
[r4,0][a,4]   [r4,0][b,4]   [r4,1][a,4]   [r4,1][b,4]. (4)
```

The remaining root swap `[r3,4][r4,5]` changes (3), but leaves

```text
C_1112220 = X_4 Y_0 Y_1 Y_2 Z_3 alpha_3 beta_5     (5)
```

as a monomial divisor of `S`.  Equations (2)--(5) exhaust all thirty pairs.
The two earlier pressure words `0101010` and `1010220` are useful matching
filters, but the uniform divisibility certificates (2)--(5) are stronger and
do not require endpoint weights to be inverted separately.

## Why divisibility proves the result

For each support, symbolic permanent expansion gives a mixed coefficient
`C_v` and a polynomial `Q_v` such that

```text
S = C_v Q_v.                                        (6)
```

Therefore `S` belongs to the principal ideal `<C_v>`.  On `S != 0`, equation
(6) forces `C_v != 0`, contradicting the diagonal target.  Equivalently,
`1 in <C_v>:S`.  This is an exact sparse identity over `Q`, not a radical or
finite-field inference.

## Stabilizer and endpoint legality

The alternating path has only identity and reversal as uncoloured
automorphisms.  Exhausting these two maps, all six colour permutations, and
both port-label permutations leaves only the identity compatible with the
fixed port supports

```text
A_0={0,1}, A_1={5,6}, A_2={3};
B_0={0,1}, B_1={6},   B_2={5}.                       (7)
```

Thus no representatives in (2)--(5) can be identified.

Endpoint legality is checked only after the tensor exclusion.  Root additions
never change endpoint cofactors.  A new port incidence at an odd blocker 3 or
5 lies on a zero principal cofactor and is legal.  Twelve root--port pairs add
a port incidence at blocker 2, 4, or 6 and create a forbidden mixed endpoint
word, so they are independently illegal when their new weight is nonzero.
The other eighteen pairs (ten root swaps and eight odd-blocker root--port
exchanges) preserve endpoint legality, but are already excluded by (6).

Rank and Hall conditions cannot rescue an empty tensor locus.  Conversely,
the old nonzero minors show that these support additions do not intrinsically
destroy the rank/Hall open conditions.

## Boundary

```text
thirty minimal pair supports:                     ALL EXCLUDED;
stabilizer quotient:                              30 SINGLETON ORBITS;
principal exact saturation certificates:         30/30;
endpoint-legal representatives:                   18/30, still excluded;
finite-field proof:                               NONE;
larger support shells:                            UNKNOWN;
global Krenn-Gu conjecture:                       UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_thirty_two_incidence_supports_principal_saturation_exclusion.py
python claims/arbitrary-order/audit_root_m7_thirty_two_incidence_supports_principal_saturation_exclusion.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_m7_thirty_two_incidence_supports_principal_saturation_exclusion.py claims/arbitrary-order/audit_root_m7_thirty_two_incidence_supports_principal_saturation_exclusion.py
python -m py_compile claims/arbitrary-order/verify_root_m7_thirty_two_incidence_supports_principal_saturation_exclusion.py claims/arbitrary-order/audit_root_m7_thirty_two_incidence_supports_principal_saturation_exclusion.py
```

The primary constructs all thirty symbolic supports, derives their permanent
coefficients, and verifies every exact quotient.  The no-import audit uses a
separate labelled-matching polynomial implementation and independently checks
the orbit, certificate, and endpoint counts.
