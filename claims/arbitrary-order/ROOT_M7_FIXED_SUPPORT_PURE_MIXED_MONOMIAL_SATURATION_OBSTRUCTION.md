# A pure--mixed monomial identity excludes the fixed `m=7` support

## Status

**Exact characteristic-zero support-stratum no-go.**  Keep the alternating
seven-blocker path and the zero pattern of the Hall-satisfying two-port
construction, but replace every displayed nonzero root entry and every port
weight by an arbitrary scalar.  Then the three pure coefficients of
`P_7(H;a;b)` cannot all be nonzero while every mixed coefficient vanishes.

The obstruction is the single mixed word

```text
w = 0000102.
```

Its coefficient and the three pure coefficients are monomials satisfying

```text
C_0 C_1 C_2 = C_w Q                              (1)
```

for an explicit monomial `Q`.  Consequently `C_0 C_1 C_2 != 0` forces
`C_w != 0` over every field.  Equivalently, the mixed-coefficient ideal
already becomes the unit ideal after saturation by the product of the three
pure coefficients.

This is stronger than a torus-only statement: the allowed symbolic entries
may specialize to zero, provided the three pure coefficients remain nonzero.
The proof does not use the rank, Hall, endpoint-cofactor, or concision
conditions, so imposing those additional conditions cannot evade it.

Thus the fixed support pattern is rigorously excluded.  A support deformation
is necessary.  The arbitrary Hall-satisfying `P_7` problem, the arbitrary-
order local-to-global reduction, and the global Krenn--Gu conjecture remain
**UNRESOLVED**.  No finite-field inference is used.

## Fixed support with symbolic weights

Retain the port supports

```text
A_0={0},       B_0={0,1},
A_1={5,6},     B_1={6},
A_2={3},       B_2={5}.                            (2)
```

Write the eight port weights as

```text
a_(0,0)=alpha_0,  a_(3,2)=alpha_3,
a_(5,1)=alpha_5,  a_(6,1)=alpha_6,
b_(0,0)=beta_0,   b_(1,0)=beta_1,
b_(5,2)=beta_5,   b_(6,1)=beta_6.                  (3)
```

Only six of these occur in the coefficients below.  Keep exactly five root
entries in each colour.  Index them by their root row:

```text
X_0=H_2[0,0], X_1=H_3[1,0], X_2=H_4[2,0],
X_3=H_5[3,0], X_4=H_6[4,0];

Y_0=H_0[0,1], Y_1=H_1[1,1], Y_2=H_2[2,1],
Y_3=H_3[3,1], Y_4=H_4[4,1];

Z_0=H_1[0,2], Z_1=H_0[1,2], Z_2=H_6[2,2],
Z_3=H_4[3,2], Z_4=H_2[4,2].                        (4)
```

Every other root entry remains zero.  This is precisely the zero pattern of
the previous integer construction; only its nonzero values have become
variables.

## Four unique matchings

Expand the last two permanent rows first.

For `0^7`, column 1 can only be used by the `b` row, so column 0 is used by
the `a` row.  The five root rows then have their unique coordinate columns.
Thus

```text
C_0 = alpha_0 beta_1 X_0 X_1 X_2 X_3 X_4.          (5)
```

The same support argument in colours one and two gives

```text
C_1 = alpha_5 beta_6 Y_0 Y_1 Y_2 Y_3 Y_4,
C_2 = alpha_3 beta_5 Z_0 Z_1 Z_2 Z_3 Z_4.          (6)
```

Now take `w=0000102`.  Column 1 again forces `b`, and column 0 then forces
`a`.  The five remaining columns support exactly

```text
root 0 -> column 2,   root 1 -> column 3,
root 2 -> column 6,   root 3 -> column 5,
root 4 -> column 4.
```

Therefore

```text
C_w = alpha_0 beta_1 X_0 X_1 X_3 Y_4 Z_2.          (7)
```

There are no second permanent terms in (5)--(7), so neither signs nor
parameter choices can create internal cancellation.

## Sparse identity and saturation certificate

Define

```text
Q = X_2 X_4
    * alpha_5 beta_6 Y_0 Y_1 Y_2 Y_3
    * alpha_3 beta_5 Z_0 Z_1 Z_3 Z_4.              (8)
```

Direct multiplication of (5)--(8) proves (1).  If all three pure
coefficients are nonzero, their product is nonzero.  Equation (1) then makes
`C_w Q` nonzero, hence in particular `C_w` is nonzero.  This contradicts the
required vanishing of every mixed coefficient.

There is also a one-line ideal certificate.  In the polynomial ring over
`Q` on the symbolic entries, put

```text
I = <C_w>,          S = C_0 C_1 C_2.
```

Since `S=C_w Q`, one has `S in I`; hence

```text
1 in I:S,     and therefore     I:S^infinity = <1>. (9)
```

So the open locus `S != 0` has empty intersection with `V(C_w)`.  Adding the
other mixed equations or any rank-open conditions cannot restore a point.

## Minimal support consequence

For the word `0000102`, the present bipartite support graph has a unique
perfect matching.  Reweighting existing entries cannot cancel it.  At least
one new incidence is therefore necessary before a full diagonal restriction
can exist on a deformation of this model.

Among port incidences, adding `a_(1,0)` creates the only one-edge alternating
cycle: it exchanges the assignments `(a->0,b->1)` and `(a->1,b->0)`.
If port supports are held fixed, no single new root incidence creates a
second perfect matching for this word; a root-only deformation requires at
least two new incidences.  These are necessary combinatorial conditions, not
a claim that the resulting enlarged support solves all mixed equations.

## Boundary

```text
fixed blocker path:                              RETAINED;
fixed port and root zero pattern:                EXCLUDED for full P_7;
three pure coefficients nonzero:                 INCOMPATIBLE with C_w=0;
exact saturation certificate:                    PROVED;
rank/Hall/local-concision escape:                 IMPOSSIBLE on this support;
one new port incidence sufficient globally:      NOT CLAIMED;
two new root incidences sufficient globally:     NOT CLAIMED;
arbitrary Hall-satisfying P_7 restriction:        UNKNOWN;
global Krenn-Gu conjecture:                       UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_fixed_support_pure_mixed_monomial_saturation_obstruction.py
python claims/arbitrary-order/audit_root_m7_fixed_support_pure_mixed_monomial_saturation_obstruction.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_m7_fixed_support_pure_mixed_monomial_saturation_obstruction.py claims/arbitrary-order/audit_root_m7_fixed_support_pure_mixed_monomial_saturation_obstruction.py
python -m py_compile claims/arbitrary-order/verify_root_m7_fixed_support_pure_mixed_monomial_saturation_obstruction.py claims/arbitrary-order/audit_root_m7_fixed_support_pure_mixed_monomial_saturation_obstruction.py
```

The primary verifier constructs the full symbolic `7 x 7` permanent matrices,
derives all four coefficients, checks the monomial identity and saturation
certificate, and enumerates one-edge support deformations.  The no-import
audit independently enumerates labelled perfect matchings and checks the
exponent-vector identity.  All calculations are exact over `Q`.
