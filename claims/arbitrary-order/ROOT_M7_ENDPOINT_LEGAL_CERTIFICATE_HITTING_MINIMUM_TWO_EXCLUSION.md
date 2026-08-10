# The listed certificate family has a unique legal two-incidence transversal

## Status

**Exact characteristic-zero relative support lower bound and survivor
exclusion.**  In the endpoint-legal incidence universe for the fixed
alternating seven-blocker path, consider the five currently certified mixed
words

```text
0000102, 1112101, 1112220, 0101010, 1010220.        (1)
```

Say that a certificate persists when its nonzero coefficient divides
`S=C_0 C_1 C_2` after the exact endpoint weights are imposed.  Exhaustive
symbolic matching-factor division over the 104 legal missing incidences proves:

1. no single incidence breaks every persistent certificate;
2. exactly one unordered pair breaks all five; and
3. the stabilizer of the fixed path and original labelled port supports is
   trivial, so this is one actual orbit.

The unique pair is

```text
H_6[3,0]=p,        H_5[4,0]=q.                     (2)
```

Thus the exact lower bound relative to (1) is two.  The pair is not a full
`P_7` survivor: the new mixed word `0101122` has a principal saturation
certificate over the fully symbolic endpoint weights.  Hence the full mixed
ideal is still empty on `S != 0`.

This classifies the minimum only relative to the listed certificate family;
it is not a universal support lower bound for arbitrary `P_7` models.  Larger
supports and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite
field is used.

## Endpoint-legal universe

Root--blocker incidences do not alter endpoint cofactors, so all 90 missing
root incidences are legal.  A new port incidence is legal only at odd blocker
1, 3, or 5, whose principal path cofactor vanishes.  Four of the eighteen
odd-blocker port positions are already occupied, leaving fourteen legal port
additions.  Therefore

```text
|U_legal| = 90+14 = 104.                            (3)
```

At even blockers, the only insertions yielding pure endpoint words are the
already-present colour-zero rows at blocker 0 and colour-one rows at blocker
6.  Every other new even-blocker port incidence creates a forbidden mixed
endpoint word and is excluded from `U_legal`.

The original port supports are

```text
A_0={0}, A_1={5,6}, A_2={3};
B_0={0,1}, B_1={6}, B_2={5}.                        (4)
```

Testing identity/reversal of the path, all six colour permutations, and both
port-label permutations leaves only the identity.  The actual stabilizer is
trivial.

## Exact hitting problem

For a support addition `T subset U_legal`, form the symbolic permanent
coefficients `C_i(T)`.  After substituting the required endpoint weights

```text
alpha_0=alpha_6=beta_0=1,   beta_6=-1,              (5)
```

define

```text
P_v(T) = true  iff  C_v(T) != 0 and C_v(T) divides S(T). (6)
```

A transversal is a set `T` for which every predicate in (6), for the five
words (1), is false.  This definition incorporates both new mixed matchings
and new pure matching factors; merely adding a second mixed matching does not
automatically hit a certificate.

Exact enumeration gives

```text
legal singleton supports: 104,  transversals: 0;
legal unordered pairs:   5356,  transversals: 1.     (7)
```

The sole pair is (2).  It creates the crossed root matching

```text
r_3->6, r_4->5
```

beside the old matching `r_3->5,r_4->6` in pure colour zero.  Consequently

```text
C_0 = alpha_0 beta_1 X_0 X_1 X_2 (X_3 X_4+p q).    (8)
```

That new pure factor breaks every divisor in the listed family, explaining
the unique transversal structurally.

## Full-ideal saturation of the unique transversal

The other pure coefficients remain

```text
C_1 = alpha_5 beta_6 Y_0 Y_1 Y_2 Y_3 Y_4,
C_2 = alpha_3 beta_5 Z_0 Z_1 Z_2 Z_3 Z_4.          (9)
```

However, direct expansion gives

```text
C_0101122 = alpha_0 beta_5 X_0 Y_1 Y_3 Y_4 Z_2.    (10)
```

Combining (8)--(10),

```text
S = C_0101122 Q,
Q = X_1 X_2 Y_0 Y_2 Z_0 Z_1 Z_3 Z_4
    * alpha_3 alpha_5 beta_1 beta_6
    * (X_3 X_4+p q).                               (11)
```

Thus

```text
<C_0101122> : S^infinity = <1>.                    (12)
```

This identity holds before the endpoint specialization (5), so the unique
relative survivor is excluded by the tensor equations alone.

## Boundary

```text
endpoint-legal missing incidences:                104;
minimum hitting size for five-word family:        2;
minimal legal hitting supports/orbits:            1/1;
unique relative survivor full mixed ideal:        EMPTY;
new principal certificate:                        0101122;
universal arbitrary-support lower bound:          NOT CLAIMED;
global Krenn-Gu conjecture:                       UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py
uv run --with sympy python claims/arbitrary-order/audit_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py claims/arbitrary-order/audit_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py
python -m py_compile claims/arbitrary-order/verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py claims/arbitrary-order/audit_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py
```

Both scripts independently enumerate all 104 singletons and 5,356 pairs with
exact symbolic permanent division.  The audit does not import the primary.
