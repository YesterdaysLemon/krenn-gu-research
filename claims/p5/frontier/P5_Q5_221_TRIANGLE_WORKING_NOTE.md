# Triangle working note for normalized `q5_221`

## Status

**SUPERSEDED AS A PROOF FRONTIER.**

This note records the exact boundary reached while studying the remaining
triangle incidence pattern

```text
D_0={A,B},  D_1={A,C},  D_2={B,C}.                   (1)
```

Both chiralities are now excluded exactly in
[`P5_Q5_221_TRIANGLE_OBSTRUCTION.md`](P5_Q5_221_TRIANGLE_OBSTRUCTION.md).
This note retains the split that exposed the two cases.  The other
minimal incidence types and all extra-containment strata are closed in
the later obstruction theorems.

## Repeated-`h_2` contraction and the two chiralities

Let `alpha_(B,2)` and `alpha_(C,2)` be the target covectors whose
pullbacks are `h_2`.  Their colour-two coordinates vanish.  Contracting
the colour-zero and colour-one identities at both `B,C` gives

```text
alpha_(B,2)(e_0) alpha_(C,2)(e_0)=0,
alpha_(B,2)(e_1) alpha_(C,2)(e_1)=0.                 (2)
```

Both covectors are nonzero.  Consequently their supports in target
coordinates zero and one are complementary singleton supports.  There
are two chiral cases:

```text
I:   Q_02 at B and Q_12 at C are nonzero;
II:  Q_12 at B and Q_02 at C are nonzero.            (3)
```

The second case is not obtained from the first while preserving which
triangle vertex contains `h_0,h_2` and which contains `h_1,h_2`.  An
earlier sketch incorrectly treated (3) as a single case.

## Closed chirality I

Write

```text
U_A=span(h_0,h_1,a u_0+b u_1+c h_2).
```

The nonzero `Q_02` residual through `A,C,D` and the nonzero `Q_12`
residual through `A,B,D` pass the rank-at-least-two gate.  In the bases

```text
J_02=span(x_+,e_2,e_3),
J_12=span(e_0,e_1,y_+),
```

the two mode-`A` plane normals are proportional, up to the harmless
normalization of `x_+` and `y_+`, to

```text
(b,-a,-a),  (b,b,-a).                                (4)
```

The nonzero decomposable-`P_3` classification forbids a support-one
normal.  Applying it to both residuals forces

```text
a!=0,  b!=0.                                         (5)
```

Their common-support rule actually forces two nonzero coefficients in
each adjacent row space, not only the two coefficients retained in the
earlier draft:

- nonzero `u_0` and `u_1` coefficients in the third generator of
  `U_C=span(h_1,h_2,r_C)`;
- nonzero `u_0` and `u_1` coefficients in the third generator of
  `U_B=span(h_0,h_2,r_B)`.

At the pair `h_0,h_1` in mode `A`, these facts give

```text
rank(L_C restricted to J_01)=3,
rank(L_B restricted to J_10)=3.                      (6)
```

The apparent rank-one exceptions from the earlier draft,

```text
U_B=span(h_0,h_2,u_1),
U_C=span(h_1,h_2,u_0),
```

are therefore unavailable: they have support-two normals in the
already nonzero `Q_12` and `Q_02` residuals, while the mode-`A` normals
in (4) have support three.

Consequently every map in both `Q_01` and `Q_10` has residual rank at
least two.  Equation (6) gives a rank-three mode in either direction,
so the nonzero decomposable-`P_3` classification makes both residuals
zero.  This contradicts the cross-scalar lemma, which requires at least
one to be nonzero.  The exact proof and two replays are in the theorem
linked above.

## Open boundary

Chirality II in (3) has rank-one vertices in the opposite locations, so
the chirality-I argument cannot simply be relabelled.  The completed
theorem uses the target colours of those rank-one images: the exceptional
mode at `B` lands in colour one although `Q_01` requires colour zero,
and the exceptional mode at `C` lands in colour zero although `Q_10`
requires colour one.  Outside those exceptions, a rank-three map or a
support-one normal rejects each cross residual.

The star and both marked paths are now excluded separately.  All
extra-containment strata, normalized `q5_221`, the full
`P_5 -> Delta_3` restriction, and the arbitrary-order Krenn--Gu
conjecture remain open.
