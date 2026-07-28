# Triangle working note for normalized `q5_221`

## Status

**INCOMPLETE AND UNVERIFIED.**

This note records the exact boundary reached while studying the remaining
triangle incidence pattern

```text
D_0={A,B},  D_1={A,C},  D_2={B,C}.                   (1)
```

It is deliberately not named or cited as an obstruction theorem.  One
chirality has a plausible closure that still needs a fresh proof audit;
the other chirality remains open.  No verifier has been run for this note.

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

## Candidate reduction in chirality I

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

Their common-support rule then forces:

- a nonzero `u_0` coefficient in the third generator of
  `U_C=span(h_1,h_2,r_C)`;
- a nonzero `u_1` coefficient in the third generator of
  `U_B=span(h_0,h_2,r_B)`.

At the pair `h_0,h_1` in mode `A`, these facts give

```text
rank(L_C restricted to J_01)=3,
rank(L_B restricted to J_10)=3.                      (6)
```

The cross-scalar lemma requires at least one of `Q_01,Q_10` to be
nonzero.  Equation (6) rejects such a residual provided all the other
maps have residual rank at least two.  There are, however, two
rank-one exceptions:

```text
Q_01: U_B=K_1=span(h_0,h_2,u_1),
Q_10: U_C=K'_0=span(h_1,h_2,u_0).                    (7)
```

An earlier sketch omitted (7).

If only one exception occurs, the residual in the opposite direction
passes every rank gate and is rejected by (6).  Thus the only remaining
boundary has both exceptional spaces in (7).

## Proposed exceptional-boundary closure

This is the part that needs a fresh independent proof audit.

With `U_B=K_1`, a nonzero `Q_01` assigns the `z` factor to mode `B`
and leaves the nondegenerate bilinear tensor on

```text
span(x_+,y_-)
```

through `C,D`.  Mode `C` is injective on this plane.  Purity should
therefore force `ker L_D` to contain a line in that plane.

With `U_C=K'_0`, the symmetric `Q_10` argument should force
`ker L_D` to contain a line in

```text
span(x_-,y_+).
```

The two displayed source planes have zero intersection, so the two
kernel lines are independent.  Since `ker L_D` has dimension two, this
would put it inside

```text
H_2=span(e_0,e_1,e_2,e_3).
```

Then `h_2` annihilates `ker L_D`, equivalently `h_2 in U_D`, contrary
to the exact triangle pattern (1).

Before promoting this to a theorem, verify explicitly:

1. the bilinear purity implication in both directions, including the
   possibility that the corresponding cross scalar vanishes;
2. that the cross-scalar alternatives force the needed direction when
   both exceptions occur;
3. every residual rank gate at `B,C,D`;
4. the field-independent kernel-line argument over `C`.

## Open boundary

Chirality II in (3) remains open.  Its direct `Q_02` and `Q_12`
contractions encounter rank-one vertices in the opposite locations, so
the chirality-I argument cannot simply be relabelled.

The star, both marked paths, all extra-containment strata, normalized
`q5_221`, the full `P_5 -> Delta_3` restriction, and the arbitrary-order
Krenn--Gu conjecture also remain open.
