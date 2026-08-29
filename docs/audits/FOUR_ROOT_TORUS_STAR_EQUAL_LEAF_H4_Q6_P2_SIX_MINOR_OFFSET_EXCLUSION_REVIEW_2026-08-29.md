# GLD97 p=2 H4/Q6 six-minor offset exclusion review

## Verdict

**Verdict: PASS for the exact `GLD97` scope.**  The reviewed result is a
proved characteristic-zero theorem on the normalized equal-leaf H4 chart at
`p=2`, with symbolic `a`, on `Q2=Q6(2,q)=0` and `D(Omega Delta_2)`.  It is not
an arbitrary-`p` H4/Q6 closure, a GLD83 Fitting computation, or a global
Krenn--Gu resolution.  The global conjecture remains **UNRESOLVED**.

## Exact claim reviewed

Write the two free leaf coordinates as the GLD88 values plus offsets

```text
b = b88(2,q,a) + B,
c = c88(2,q,a) + C.
```

Let `T0,...,T3` be the four GLD96 bordered seven-minors and let `D0,D2` be
the two additional direct seven-minors recorded in the GLD97 owner and both
verifiers.  In `Q[B,C,q,a]`, use their exact denominator-safe representatives
modulo

```text
Q2 = 5q^4 - 4q^3 + 12q^2 - 16q + 8.
```

The reviewed certificate is

```text
(Q2,T0,T1,T2,T3,D0,D2) = (Q2/5,B,C).
```

Thus full syndrome rank at most six forces `B=C=0`.  The GLD75/GLD86 bridge
supplies that syndrome-rank hypothesis from the normalized incidence branch,
and GLD95 excludes the resulting F88 point on `D(Omega Delta_2)`.

## Exact replay evidence

The focused primary verifier reconstructs the committed GLD71 syndrome and
GLD88 family, checks all `111` F88 block-kernel identities, forms the four
bordered minors by the adjugate/Schur identity, forms `D0,D2` directly, and
checks all raw and reduced hashes.  Its final bounded replay passed in
`92.080` seconds.

The independent verifier imports no project builder or verifier.  It copies
the ten required sparse supports, accumulates the syndrome directly, computes
all six determinants by a local fraction-free Bareiss routine, and repeats the
quotient and Groebner calculations.  Its final bounded replay passed in
`67.197` seconds.

Both replays used CPython `3.13.14` and SymPy `1.14.0`.  They agree on all six
reduced-polynomial hashes and on the grevlex-basis hash

```text
da8b07d04dfb0dbc9935345320722fb21f9e711bb9166f82db9fb23b0f7f585f.
```

A separate read-only comparison matched every copied support literal to the
committed GLD71 relation table and matched the written F88 and Q6 formulae to
their canonical sources.  The primary additionally hashes those canonical
supports at runtime.  This makes the audit implementation-independent but not
mathematical-input-independent; the fixed sparse relations and written family
are shared upstream data.

## Adversarial findings and repairs

1. The first theorem draft stated raw/reduced equivalence only on
   `D(Delta_2)`.  Reduction modulo Q2 justifies it only on `V(Q2)`.  The owner
   now states the exact equality of vanishing loci on
   `V(Q2) intersect D(Delta_2)` and both verifiers check every denominator is
   a Q2-unit.  No hidden `B`, `C`, or `a` localization is used.

2. The first bridge presentation bounded only the first eight syndrome
   columns.  The owner now records the load-bearing ninth-column identity:
   `C_center,8=1` and `M C_center=0` put column eight in the span of columns
   zero through seven.  Hence the GLD86 rank bound applies to the full
   `37 x 9` syndrome.

3. The offset chart was initially described too narrowly.  On
   `D(Delta_2)`, `B=b-b88` and `C=c-c88` are an affine translation of the two
   unrestricted original coordinates.  Therefore GLD97 covers arbitrary
   `b,c` on this normalized p=2 H4/Q6 fibre, including old-`P6=0` points.  It
   does not cover another gauge, scale chart, or `Delta_2=0`.

4. GLD92 was initially grouped with GLD95 as though both supplied the full
   endpoint.  The corrected owner assigns GLD92 only the dense portion and
   retained finite residual; GLD95 supplies the exact all-factor closure used
   after `B=C=0`.

5. The GLD83 raw/Fitting gap was initially phrased as a promotion prerequisite.
   It is not required for this scoped theorem.  It remains a separate parent
   obligation for connecting the normalized low-rank lane to the broader raw
   response/Fitting survivor route.

6. The new `D0,D2` selections initially existed only in exploratory work.
   Their precise row/column provenance and direct-determinant construction are
   now committed in the owner, primary, and independent audit.  Any valid
   seven-minor vanishes under syndrome rank at most six; no completeness or
   minimality of this pair is claimed.

7. The final verifiers mechanically assert H4, the F88-origin determinant
   identity, raw-denominator linkage to the declared `Delta_2` factors, the
   six raw and reduced hashes, and the basis hash.  Exact basis recomputation
   and zero remainders certify `B,C` membership.  Giant standalone multiplier
   expressions are not required and are not used as evidence.

## Hostile controls and failed routes

The earlier selected `R28,R31` system retained fibres at `a=0,2`.  Direct
seven-minors show those selected-minor solutions have syndrome rank at least
seven.  They are controls against overinterpreting a selected pivot system, not
counterexamples to GLD97.

A generic-`p` quotient/Groebner reconnaissance reached its `1800`-second,
`12288`-MB containment boundary without output.  It is **inconclusive** and is
not evidence for or against arbitrary-`p` closure.  An optional attempt to
materialize very large standalone membership multipliers also produced no
durable artifact and is not used.  Both successful theorem replays instead
recompute the exact polynomial-ring basis.

## Retained obligations

GLD97 leaves open arbitrary `p`, the generic exceptional strata away from
this fibre, `Delta_2=0`, `Omega=0`, other gauges and equal-/unequal-leaf
components, the GLD83 pulled-back Fitting residual and rank-seven/higher-rank
lanes, remaining source/component/root/order coverage, and the global
Krenn--Gu conjecture.
