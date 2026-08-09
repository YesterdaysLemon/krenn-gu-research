# Adjacent-port determinant transport lemma

## Statement

Use the equality architecture from the minimal singleton-circuit rectangle
theorem.  Thus the full edges form a vertex-disjoint union `F` of even
cycles, and `S0,S1,S2` are pairwise edge-disjoint diagonal singleton
perfect matchings.

Fix a singleton colour `c`.  Let `T` be a nonempty proper subset of `Sc`
which is positive-minimal feasible, touches every full cycle, and survives
the rectangle theorem.  On every full cycle `C`, the endpoints of `T` are
therefore an adjacent pair `x_C,y_C`.  Write

```text
h_C = x_C y_C
```

for the full edge joining those two ports, and let `R_C` be the unique
perfect matching of `C-{x_C,y_C}`.

Call the other singleton colours `p,q`.  Properly 2-colour every component
of `Sp union Sq` with `p,q`, and call the resulting vertex colouring `b`.
Put

```text
a_C = b(x_C),    d_C = b(y_C).
```

For the supported `3 x 3` block on the oriented full edge
`h_C=x_Cy_C`, define the nonzero Schur complement

```text
Delta_C(b,c)
  = W_hC[c,c]
    - W_hC[c,d_C] W_hC[a_C,c] / W_hC[a_C,d_C].
```

If the support realizes the Krenn--Gu target, then

```text
product_C Delta_C(b,c)
  = - product_(e in T) W_e[c,c].                         (1)
```

The right side does not depend on the chosen proper `p,q` colouring.
Consequently any two such colourings `b,b'` also satisfy

```text
product_C Delta_C(b,c)
  = product_C Delta_C(b',c).                             (2)
```

After clearing the supported nonzero denominators, (1) becomes

```text
product_C (
    W_hC[c,c] W_hC[a_C,d_C]
    - W_hC[c,d_C] W_hC[a_C,c]
  )
+ product_(e in T) W_e[c,c]
  product_C W_hC[a_C,d_C]
= 0.                                                     (3)
```

Thus the rigid adjacent-port exception is not algebraically silent.  It
forces a signed binomial relation after adjoining the nonzero local
determinants as variables.

## Local four-corner calculation

Fix one full cycle `C`, abbreviate its two adjacent ports by `x,y`, and
vary only whether each port keeps its base colour or is changed to `c`.
Write `H_ij` for the entry on the port edge `xy`, where bit `1` means
colour `c`, and write `A_ij` for the other alternating full-cycle
monomial.  The alternating monomial using `xy` is `R_C H_ij`.

The other alternating monomial separates across the two ports, so

```text
A_11 A_00 = A_10 A_01.
```

Every proper corner of the exact-activation cube is full-only.  Leaving
all other full cycles at their target colours makes their binomials
nonzero, so the three proper local corners obey

```text
A_00 + R_C H_00 = 0,
A_10 + R_C H_10 = 0,
A_01 + R_C H_01 = 0.
```

Since all supported entries are nonzero,

```text
A_11
  = A_10 A_01 / A_00
  = -R_C H_10 H_01 / H_00.
```

The target cycle binomial is therefore

```text
A_11 + R_C H_11
  = R_C (H_11 - H_10 H_01/H_00)
  = R_C Delta_C(b,c).                                   (4)
```

It is nonzero: otherwise the full-only product at the target corner would
vanish, leaving the one additional supported matching monomial uncancelled.
Hence every `Delta_C(b,c)` in (1) is nonzero.

## Global cancellation

At the target corner, the active perfect matchings are exactly:

- all independent alternating choices on the full cycles; and
- the unique completion using every edge of `T`.

By (4), the full-only product is

```text
product_C R_C Delta_C(b,c).
```

The additional matching has monomial

```text
product_(e in T) W_e[c,c] product_C R_C.
```

The target corner is nonmonochromatic because `T` is a proper subset of
`Sc`, so its amplitude is zero.  Cancelling the supported nonzero
`product_C R_C` gives (1).

## Why this helps

Each exceptional component cycle now contributes an exact signed Laurent
relation in the enlarged alphabet

```text
{ supported singleton entries, nonzero port determinants }.
```

An integer dependency among such relations with odd coefficient sum is
an immediate contradiction, just as in the existing signed-binomial
lattice method.  Multiple proper `p,q` colourings provide additional
same-sign transport identities (2).

This is a strict refinement of the rectangle theorem's boundary.  It does
not yet prove that the determinant relations forced by three arbitrary
singleton factors always contain an odd signed dependency.

## Independent audit

Run:

```text
python claims/arbitrary-order/verify_adjacent_port_determinant_transport_lemma.py
```

The verifier checks the local rational identity symbolically, checks its
cleared-denominator form, and exhaustively composes one through six
independent full-cycle components over deterministic nonzero rational test
data.  It must write
`tmp/adjacent_port_determinant_transport_lemma_verified.json` with
`"verified": true`.
