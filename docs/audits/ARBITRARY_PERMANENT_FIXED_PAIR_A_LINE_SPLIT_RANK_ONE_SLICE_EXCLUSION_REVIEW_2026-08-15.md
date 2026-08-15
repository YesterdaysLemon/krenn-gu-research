# Hostile review of the fixed-pair `A`-line-split exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
`A`-projection-profile scope.**  No algebraic, pure-tensor, zero-scalar,
rank, quantifier, implementation, or scope blocker survived hostile review.

After permuting the four remaining input modes, the package assumes

```text
rank(pi_A|L_2,L_3,L_4,L_5)=(1,1,1,0)
```

and assumes that each of the three fixed diagonal slices `T_0,T_1,T_2` is
nonzero and rank one.  It proves that at least two of the first three input
flattenings of the resulting `D^*`-valued sensor have rank at most two.
Consequently the sensor is not concise and cannot be equivalent to
`Delta_3`, even if an arbitrary output change is allowed.

The mixed-zero equations are not used.  The result therefore excludes the
whole indicated projection-profile family, but it does not prove that every
simultaneous-low tuple has that profile.  It does not classify the other
projection incidences, normalize another equality-five pair orbit to this
fixed pair, or prove unrestricted `P_6 -> Delta_3` nonrestriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_A_LINE_SPLIT_RANK_ONE_SLICE_EXCLUSION.md
  verify_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py
  audit_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py
```

## 1. Independent derivation of the line-split identity

Write `K^6=R direct-sum A`, with `R` on coordinates `0,1,2,3` and `A` on
coordinates `4,5`.  Since the first three local projections to `A` have
rank one, there are nonzero `u_s in A` and nonzero covectors `alpha_s` such
that

```text
a(y_s)=alpha_s(y_s)u_s,                 s=2,3,4.
```

The fourth local space lies in `R`.  In a coefficient of `x_4x_5 g`, the
two `A` coordinates must therefore be supplied by two distinct members of
`{2,3,4}`.  For an unordered pair `{s,t}`, summing the two assignments of
`x_4,x_5` gives

```text
J(a(y_s),a(y_t))
 =alpha_s(y_s)alpha_t(y_t)J(u_s,u_t).
```

The remaining `A`-line mode and mode `5` supply the two coordinates of the
square-free quadratic `g`.  Summing their two assignments on every edge is
exactly its polarization `G_g`.  Thus direct coefficient expansion gives

```text
T_g
 =kappa_23 alpha_2 alpha_3 G_g(r_4,r_5)
 +kappa_24 alpha_2 alpha_4 G_g(r_3,r_5)
 +kappa_34 alpha_3 alpha_4 G_g(r_2,r_5),
```

where `kappa_st=J(u_s,u_t)`.  There is no missing factorial: the two ordered
assignments in `J` and the two ordered assignments on each edge in `G_g`
are exactly the corresponding terms in the multilinear coefficient.

The primary verifier derives this identity symbolically over the integers.
The independent audit instead evaluates every ambient basis tensor for all
`4^3` projective triples of `A`-lines over `F_3`, all six edge quadratics,
and all `5*5*5*4` local basis-label choices, for a total of `192,000`
checks.  Both routes passed.

## 2. Restriction argument, including every `kappa=0` case

Fix a nonzero pure slice

```text
T=f_2 tensor f_3 tensor f_4 tensor f_5.
```

For a mode `s in {2,3,4}`, the restriction to `ker(alpha_s)` kills the two
summands of the line-split identity that contain `alpha_s`.  For instance,

```text
T|ker(alpha_2)
 =kappa_34 alpha_3 tensor alpha_4 tensor
   G_g|_(r(ker alpha_2) x r(L_5)).
```

There are exactly two possibilities.

- If `f_2|ker(alpha_2)=0`, then `ker(alpha_2)` is contained in
  `ker(f_2)`.  Both are hyperplanes because both covectors are nonzero, so
  `f_2` is proportional to `alpha_2`.
- If `f_2|ker(alpha_2)` is nonzero, the restriction of the displayed pure
  tensor is nonzero.  Hence its right side is nonzero.  Flattening that
  equality in modes `3` and `4`, or applying uniqueness of factors of a
  nonzero pure tensor, forces `f_3` proportional to `alpha_3` and `f_4`
  proportional to `alpha_4`.

This reasoning is safe when `kappa_34=0`: in that case the right side is
zero, so the second case is impossible and the first case must hold.  The
same observation handles a zero restricted bilinear form.  The proof never
divides by any `kappa`, never assumes the three `A`-lines are generic, and
never assumes any pair has nonzero `J`-pairing.  Cyclically, if the factor
at any one of modes `2,3,4` is exceptional, the other two are forced onto
their respective `alpha`-lines.  Thus each fixed slice has at most one
exceptional mode.

## 3. Exception count and flattening ranks

Let `n_t` be the number of the three slices in which the mode-`t` factor is
not proportional to `alpha_t`.  Since every slice contributes at most one
exception,

```text
n_2+n_3+n_4 <= 3.
```

If two of these counts were at least two, their sum alone would be at least
four.  Hence at least two counts are at most one.  At either corresponding
mode, at least two of the three slice factors lie on the common line
`K alpha_t`; all three factors therefore span a space of dimension at most
two.

For completeness, the asserted flattening-rank equality does not rely on
possible independence of the other input factors.  In the mode-`t`
flattening write

```text
S=sum_c f_(t,c) tensor v_c,
v_c=d_c^* tensor (tensor_(s!=t) f_(s,c)).
```

Every `v_c` is nonzero, and the `v_c` are linearly independent because
their output factors are the independent covectors `d_c^*`.  The
flattening rank is consequently exactly

```text
dim span{f_(t,0),f_(t,1),f_(t,2)}.
```

Input flattening rank is invariant under all invertible local changes and
under an invertible output change.  Since every input flattening of
`Delta_3` has rank three, the claimed nonconciseness exclusion follows.

## 4. Discovery ledger and exact fixtures

The theorem labels the `74,620` search count correctly and repeatedly as a
**sampled** discovery ledger.  It explicitly denies exhaustiveness, case
coverage, probability content, and characteristic-zero proof status.  No
frozen search generator or full transcript for that count is part of this
package, so this review did not independently regenerate `74,620`; that
number remains non-load-bearing provenance, not verifier output.

The nine retained tuples are a different matter.  Both implementations pin
their canonical compact JSON by

```text
b24836d1b7f47f7de00f045d15015b3568cf6a63958402c3d3c4d2b2765e19ad.
```

Independent exact rational replay of the signed lifts confirms, for all
nine fixtures:

```text
four local-plane ranks:                    (3,3,3,3);
two mixed tensors:                         zero;
fixed-output rank:                         3;
all three fixed-slice multilinear ranks:   (1,1,1,1);
A-projection-rank multiset:                {1,1,1,0};
input-flattening-rank multiset:             {3,2,1,1};
mixed-radical-dimension multiset:           {3,3,5,5}.
```

The audit also checks the corresponding `F_3` mixed-zero, output-rank, and
slice-rank statements.  The discovery ledger reports these as all nine
rank-one-slice hits within that particular sample, but the sample itself is
not a case cover.  Their exact replay does not exhaust the full finite-field
locus or any characteristic-zero incidence space.  In particular, none is
a `Delta_3` restriction because each has two deficient input flattenings.

## 5. Independence and focused replay

The primary checker uses SymPy and direct square-free multiplication.  The
independent audit imports neither the primary module nor SymPy; it evaluates
quartics through explicit permanent sums, uses custom modular and rational
row reduction, stores the fixtures in an independent encoding, and checks
the expected tuple-by-tuple rank ledgers.  This is meaningful
implementation independence for the identities and fixtures, while the
written restriction argument is the proof.

Focused replay passed:

```text
new primary exact verifier:                    PASS;
new independent no-import audit:               PASS;
concise-sharpness predecessor primary:          PASS;
concise-sharpness predecessor independent audit:PASS;
py_compile on the new scripts:                  PASS;
Ruff on the new scripts:                        PASS;
git diff --check on the reviewed package:       PASS.
```

The concise-sharpness predecessor remains consistent with the new theorem:
its local `A`-projection profile is not `{1,1,1,0}`, and its fixed slices
have multilinear ranks greater than one, so it satisfies neither load-
bearing hypothesis of the exclusion.

## 6. Accepted boundary

```text
fixed equality-five pair:                              YES;
one A-zero mode and three A-line modes:                 ASSUMED;
three nonzero fixed rank-one slices:                    ASSUMED;
at least two input flattening ranks at most two:        PROVED;
kappa nonvanishing or generic A-lines:                  NOT ASSUMED;
mixed-zero equations:                                  NOT USED;
nine signed rational fixtures:                         EXACTLY REPLAYED;
74,620-point discovery ledger:                          SAMPLED, NOT REPLAYED;
other A-projection profiles:                            OPEN HERE;
general simultaneous-low residual:                     OPEN;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
1C976119D3AC5FEB861F4DA33803E6BB585AD7A63BEB1A47CAA06CA9FD30C395

new primary verifier:
EBE2D6492807418C0457D1CFE72310601ED59B10B78175AE3F51096853EED0BD

new independent audit:
DCE218D232D9BAD5BFEB33D0CEBB727E51E5EF5AF4AB33DE243C33E79C35A069

concise-sharpness predecessor theorem:
78673A99369ADB2427C6C3F9867D90FDB752C00FDFBDC4A89F094F43564F405F

concise-sharpness predecessor primary verifier:
DF8D414938E44245EB8082BBEAA652D57E70DDA4EEB7DD663E5468643B15B369

concise-sharpness predecessor independent audit:
45BF0AE22EBDEF2E44F41BC13233FAA1E9F0D96C1A40142FFC6D22CB8535D779
```
