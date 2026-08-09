# Fourteen-vertex support with no one-term amplitude

## Exact claim

There is an explicit `n=14`, `d=3` equality support with:

- fourteen full blocks forming `C3+C4+C7`;
- three colour-labelled diagonal singleton perfect matchings;
- a 5-regular, 35-edge skeleton;

for which no nonmonochromatic colouring has exactly one active perfect
matching.

This is **not** a Krenn--Gu counterexample.  It is a support-level
obstruction showing that the arbitrary-order all-odd one-term theorem
cannot be extended unchanged to mixed odd/even full factors.

## The support

The full cycles are

```text
0-1-2-0
3-4-5-6-3
7-8-9-10-11-12-13-7.
```

The singleton colour classes are

```text
S0 = {0-12, 1-11, 2-10, 3-8, 4-7, 5-13, 6-9}
S1 = {0-10, 1-12, 2-9, 3-11, 4-6, 5-7, 8-13}
S2 = {0-9, 1-10, 2-8, 3-5, 4-13, 6-12, 7-11}.
```

## Why the singleton-set poset decides one-term amplitudes

For a skeleton perfect matching `M`, let

```text
T = M intersect (S0 union S1 union S2).
```

If a colouring activates `M`, it activates every singleton edge of `T`;
all full edges are always active.  Therefore every perfect matching of
`F union T` is active under the same colouring.

Two conditions are necessary for `M` to be the only active matching:

1. no skeleton perfect matching has a singleton set properly contained in
   `T`;
2. `T` touches every full-factor cycle, because an untouched even cycle can
   be flipped between its two alternating perfect matchings.

They are also sufficient at the support level.  The exact-activation lemma
can activate precisely any matching `T`; if `T` is inclusion-minimal and
touches every full cycle, deleting its endpoints leaves even paths with
unique full-edge matchings.

## Independent exhaustive audit

The support has 267 skeleton perfect matchings and 242 distinct feasible
singleton sets.  Exactly nine singleton sets are inclusion-minimal.  Every
one:

- consists of one edge;
- touches the `C3` and `C7`;
- misses the `C4`.

Thus none can produce a one-term amplitude.  The independent verifier goes
further and constructs a second active matching for every one of the 267
possible target matchings:

```text
249  use a proper feasible singleton subset
 18  flip the untouched C4
267  total matching alternatives checked
```

Run:

```text
python verify_fourteen_vertex_no_one_term_support.py
```

Pinned audit:

```text
tmp/fourteen_vertex_no_one_term_support_verified.json
SHA-256
  1f455dbb3edca012f44025f8a2dd944386047d1c0a8481274a9a1236797ad4b4
```

The output contains `"verified": true`.

## What remains

The support is in fact impossible for a stronger, very small reason.

Equation 118 is a forbidden binomial amplitude on skeleton matchings 77 and
83.  Its two nonzero monomials force a four-entry Laurent ratio to equal
`-1`.  Equation 112 is a forbidden trinomial on matchings 30, 32, and 40.
The ratio between the terms for matchings 30 and 40 is exactly the same
Laurent vector, up to orientation.  Those two target terms must therefore
cancel, leaving the matching-32 monomial nonzero.

`verify_fourteen_vertex_binomial_trinomial.py` independently reconstructs
the support, both colourings from their base-three equation indices, all
five activities, and both Laurent exponent differences.

Run:

```text
python certify_fourteen_vertex_binomial_trinomial.py
python verify_fourteen_vertex_binomial_trinomial.py
```

Pinned final audit:

```text
tmp/fourteen_vertex_binomial_trinomial_verified.json
SHA-256
  9b884bf89b1ecd626c68f9885e7944d8f3204687d9b6b56c99d68efaaea63326
```

This certificate closes the explicit support only.  The complete
`C3+C4+C7` family is now closed separately by the one-term/matching-fork
exhaustion in `FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md`.

There is now also a simpler certificate for this support that does not scan
the colour cube.  `certify_fourteen_vertex_matching_fork.py` finds a
singleton matching `U` for which removing one edge leaves exactly two
perfect matchings sharing a full edge at one endpoint, while restoring the
edge adds exactly one perfect matching.  The adjacent exact-activation
lemma turns that fork into a cancellation-transport contradiction.
Independent replay is pinned at
`tmp/fourteen_vertex_matching_fork_no_three_extension_verified.json`; see
`MATCHING_FORK_TRANSPORT_LEMMA.md`.
