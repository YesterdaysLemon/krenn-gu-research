# Final monotone-boundary obstruction for normalized `q5_221`

## Status

This is an exact tensor theorem over `C`.

Together with the nine exact minimal obstruction theorems, the three
exact seven-incidence cover obstructions, and the preceding monotone
cover theorems, it proves:

```text
There is no normalized q5_221 restriction of P_5 to Delta_3.          (1)
```

This is a complete exclusion of the normalized `q5_221` branch.  The
separate partial `q4_211` branch was subsequently excluded, but
one-partial `H31/H22` high-coordinate families remain.  Thus this
theorem does **not** prove `P_5 -> Delta_3` impossible or resolve the
arbitrary-order Krenn--Gu conjecture.

## Only two genuine eighth-incidence boundaries

The distinguished-normal theorem gives

```text
|D_2|=2.
```

Eleven of the fourteen seven-incidence covers are already excluded
monotonically:

```text
#0,#1,#2,#3,#4,#5,#6,#7,#9,#10,#11.                 (2)
```

The exact strata of `#8,#12,#13` are excluded by their separate
theorems.  To lift those three exact results, add majority-normal
incidences while keeping `|D_2|=2`, and inspect the seven-incidence
subcovers.

Up to mode permutations and swapping the majority colours, every
strict superpattern contains a cover in (2), except for exactly two
eight-incidence patterns:

```text
S: D_0=0111, D_1=1011, D_2=1100,
R: D_0=0011, D_1=1111, D_2=1100.                    (3)
```

Every ninth-incidence extension of either pattern in (3) contains a
cover in (2).  Thus it remains only to exclude `S,R`.

Use

```text
u_0=e_0+e_1, h_0=e_0-e_1,
u_1=e_2+e_3, h_1=e_2-e_3, h_2=e_4.
```

Recall the sign-slice consequence of the decomposable-`P_3`
classification:

> No nonzero decomposable rank-`222` restriction of
> `P_3(a,b,c)` has all three kernel normals satisfying `n_b=n_c`.

For support two, that equality permits only one of the two sign
variants.  For full support, it permits only two vertices of the
four-point sign rectangle, while a valid triple uses three.

## The repeated-pair boundary `R`

Label the modes so

```text
h_0,h_1 in U_A intersect U_B,
h_1,h_2 in U_C intersect U_D.                        (4)
```

The `h_2` pullbacks at `C,D` have complementary singleton target
support.  Relabel `C,D` so that

```text
L_C^*epsilon_0 in C*h_2.
```

Contracting the colour-zero identity at `C` gives

```text
(L_A tensor L_B tensor L_D)Q_02
  in C^* e_0^3.                                      (5)
```

All three local ranks in (5) are exactly two: `h_0` supplies the rank
drop at `A,B`, while `h_2` supplies it at `D`.  Moreover all three row
planes contain `h_1`, so all three `Q_02` kernel normals satisfy
equality of their last two coordinates.  This contradicts the
sign-slice statement above.  Hence `R` is impossible.

## The four-cycle boundary `S`

Label the modes so

```text
h_0,h_1 in U_A intersect U_B,
h_0,h_2 in U_C,
h_1,h_2 in U_D.                                      (6)
```

Again the `h_2` pullbacks at `C,D` have complementary singleton
support.

If the pullback at `C` is supported on target colour zero, contracting
the colour-zero identity at `C` gives a nonzero `Q_02` residual through
`A,B,D`.  Its ranks are `222`, and all three row planes contain
`h_1`, so the same sign-slice contradiction applies.

It remains that

```text
L_D^*epsilon_0 in C*h_2,
L_C^*epsilon_1 in C*h_2.                             (7)
```

Let `alpha_D1` pull back to `h_1` at `D`.  Its target-one coordinate
vanishes by the own-colour identity.  Independence from the
`h_2` pullback in (7) forces

```text
alpha_D1(e_2)!=0.
```

Similarly, if `alpha_C0` pulls back to `h_0` at `C`, then

```text
alpha_C0(e_2)!=0.                                    (8)
```

Double-contract the colour-two identity at `C,D` by
`alpha_C0,alpha_D1`.  Equations (8) make its target side a nonzero
multiple of `e_2 tensor e_2`.  Its source side is, up to a nonzero
scalar,

```text
(L_A tensor L_B)Sym(h_0,h_1).                        (9)
```

Both `L_A,L_B` are injective on `span(h_0,h_1)`, because their row
spaces contain the independent covectors `h_0,h_1`.  The bilinear form
`Sym(h_0,h_1)` has matrix rank two on that source plane, so its image
under two injective maps still has matrix rank two.  It cannot equal
the nonzero decomposable tensor required by (9).  This contradiction
excludes `S`.

## Completion of the normalized branch

Every normalized incidence pattern has at least six incidences.

- At exactly six incidences, one of the nine marked minimal
  obstruction theorems applies.
- At seven incidences, one of the fourteen cover theorems applies:
  eleven monotonically and `#8,#12,#13` on their exact strata.
- At eight or more incidences, the cover-poset reduction gives either
  one of the eleven monotone covers or one of `S,R`; both exceptional
  patterns are excluded above.

This proves (1).

## Verification

Run:

```text
python claims/p5/boundaries/verify_p5_q5_221_final_monotone_boundary.py
python claims/p5/boundaries/audit_p5_q5_221_final_monotone_boundary.py
```

The primary verifier enumerates only the `3 x 4` incidence poset,
reconstructs the two exceptional orbits, checks the sign-slice counts,
and expands the decisive double contraction.  The independent audit
rebuilds the poset from the fourteen cover representatives, audits the
projective sign slice over `F_3,F_5`, and differentiates the squarefree
quartic.  The written obstruction is over `C`; no script enumerates
ambient row spaces or local maps.
