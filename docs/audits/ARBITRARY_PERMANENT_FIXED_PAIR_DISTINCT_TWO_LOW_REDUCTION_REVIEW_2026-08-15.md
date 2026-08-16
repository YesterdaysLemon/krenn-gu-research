# Hostile review of fixed-pair distinct-two-low reduction

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero
reduction.**  No same-mode synthesis, line/support classification,
low-count cover, complementary-index, pure-coefficient, line-split,
`E_22`-subcase, rank-boundary, fixture, field, quantifier, dependency,
implementation, or scope blocker survived hostile review.

Every exact fixed-pair `P_6 -> Delta_3` extension has exactly two low
remaining modes.  One is low only for `Phi_1`, the other is low only for
`Phi_2`, and the other two modes have rank three under both projection
families.  If `s,t` are those two high modes, their `A`-pairing matrix is
either

```text
M_(st)=0
```

or

```text
M_(st)=mu E_22,                mu!=0.
```

In the zero branch the two high `A`-ranks are `(1,1)`.  In the `E_22`
branch they are `(1,2)` or `(2,1)`; the rank-one shore is supported only at
colour `2`, and at least one low mode has rank two on its colour-`0,1`
columns.

These are necessary incidence conditions, not existence results.  The two
displayed rational fixtures satisfy the proved incidence and companion
conditions but each has

```text
T_(m_1)(0,0,0,0)=-2!=0.
```

Neither is an exact `Delta_3` restriction or a counterexample.  The final
zero and `E_22` branches remain open, unrestricted permanent nonrestriction
remains unknown, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
  audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
```

Load-bearing frozen dependencies include the two-sided projection-drop,
kernel-support, exceptional-kernel, all same-mode exclusion packages,
both `q_-` and `q_+` siblings, and the abstract rank-one-shore result in the
support-two incidence package.  Each was checked by current-byte replay.

## 1. Same-mode synthesis and the lower low-count bound

The kernel-support and two-sided projection-drop theorems give, for each
family,

```text
min_t rank(Phi_k|L_t)=2,                 k=1,2.
```

Thus each family has at least one low mode.  The exceptional-kernel theorem
places every low kernel on one of

```text
Phi_1: N,A_0,C_0,              Phi_2: N,A_1,C_1.
```

The noncommon/noncommon and common/noncommon same-mode theorems leave only
the proportional `N/N` same-mode branch.  For `N`, the kernel-support
theorem makes singleton versus support two exhaustive.  The companion
propagation and its support-two extension produce exactly the projective
fork `q_-` or `q_+`; the separately reviewed sibling theorems exclude every
support and placement case in both forks.  Therefore no mode is low for
both families.

If any local plane contained `N`, that line would lie in both ambient
projection kernels.  The rank floor would make the mode rank two in both
families, contradicting the same-mode synthesis.  Hence every surviving
low is one of

```text
Phi_1: A_0,C_0,                 Phi_2: A_1,C_1.
```

The exact allowed supports are the nonempty subsets of

```text
A_0,C_1: {1,2};                 C_0,A_1: {0,2}.
```

No size-zero, size-three, common-line, or same-mode occurrence remains.
Since each family still has a low and the family lows occupy distinct
modes, the total low-mode count is at least two and can only be `2,3,4`.

## 2. Independent pair classification

For lows `p,q` in distinct modes, with local coefficient vectors
`alpha,beta`, the other two modes have one common pairing matrix `M` and
satisfy

```text
sigma_(m_1)M=sigma_(m_2)M=0,
sigma_(d_c)M=lambda_c alpha_c beta_c E_cc.
```

Direct polarization of the fixed quartics gives the complete noncommon
line table:

```text
pair       nonzero contractions

A_0/A_0   m_2=2, d_1=2
A_0/C_0   m_2=2
C_0/C_0   m_2=2, d_0=2

A_1/A_1   m_1=2, d_0=2
A_1/C_1   m_1=2
C_1/C_1   m_1=2, d_1=2

A_0/C_1   d_1=-2, d_2=-2
C_0/A_1   d_0=-2, d_2=-2
A_0/A_1   d_2=-2
C_0/C_1   d_2=-2.
```

Rescaling either projective low multiplies every scalar in its row by a
common nonzero factor, so only the displayed zero pattern matters.

The four pair rules follow without a converse assumption:

1. A same-family pair has a nonzero mixed scalar, hence `M=0`; every
   diagonal equation then forces disjoint actual supports.
2. A cross-family same-missing pair has the same two-element maximal
   support and two nonzero diagonal scalars.  Any overlap would make `M`
   nonzero in one channel and zero or a different matrix unit in the other.
   Thus the supports are complementary singletons and `M=0`.
3. A cross-family different-missing pair has maximal supports intersecting
   only at colour `2`.  If both contain `2`, the sole nonzero scalar gives
   `M=mu E_22`; otherwise the actual supports are disjoint and `M=0`.

The primary and independent audit separately exhaust all support choices.
They agree on `28` compatible ordered same-family pairs, `22` compatible
cross-family pairs, and `8` cross-family `E_22` pairs.  The computation
replays a finite line/support table; the displayed characteristic-zero
matrix equations prove the classification.

Two consequences used later are exact:

```text
same-family low supports are disjoint;
every nonzero matrix induced by two lows is supported only at (2,2).
```

## 3. Four-low exclusion and complementary indices

Assume all four remaining modes are low.  For any chosen pair of modes
`{s,t}`, its complementary pair `{u,v}` consists of lows.  Applying the
pair classification to the contracted pair `u,v` constrains the matrix on
the uncontracted pair:

```text
M_(st)=0                  or                  M_(st)=mu E_22.
```

Because every two-element set has a low complementary pair, this holds for
all six unordered mode pairs.  In particular,

```text
J(A_s e_c,A_t e_c)=0,                 c=0,1,
```

for every distinct `s,t`.

In a four-linear evaluation of `x_4x_5g`, the two `A` factors must come from
two distinct modes.  Every contribution to the pure colour-zero word is
therefore one of the vanishing colour-zero pairings above, and similarly at
colour one.  The pure `d_0` and `d_1` coefficients both vanish, contradicting
`lambda_0 lambda_1!=0`.  This argument is independent of whether the family
partition is `1+3` or `2+2`.

Thus at least one mode is high under both families.

## 4. Two-colour three-line obstruction

Restrict all four local triples to their colour-`0,1` planes.  Suppose three
of the four `A`-maps have rank at most one and every `A` pairing involving
the distinguished fourth shore vanishes.

If fewer than two of the three line shores are nonzero, no quartic can have
two `A` suppliers.  If exactly two are nonzero, their fixed coefficient
covectors occur as factors in every nonzero tensor and cannot be
proportional to both independent colour covectors `e_0^*` and `e_1^*`.

When all three line shores are nonzero, write

```text
a(y)=alpha_i(y)u_i,                 kappa_ij=J(u_i,u_j).
```

Since the distinguished shore cannot be an `A` supplier, direct
polarization gives

```text
T_g=
 kappa_12 alpha_1 alpha_2 G_g(r_3,r_h)
+kappa_13 alpha_1 alpha_3 G_g(r_2,r_h)
+kappa_23 alpha_2 alpha_3 G_g(r_1,r_h).
```

For one nonzero pure rank-one slice, restrict mode `i` to
`ker alpha_i`.  If its target factor vanishes there, that factor is
proportional to `alpha_i`.  Otherwise only the term with the other two
line shores survives; equality with a nonzero pure tensor forces both of
their target factors to align with their fixed `alpha` rows.  Thus each
slice has at most one failure of alignment among the three modes.

The two live diagonal slices can together have failures in at most two
modes.  A third mode aligns both `e_0^*` and `e_1^*` with one fixed
`alpha_i`, impossible because those covectors are independent on the
two-colour plane.  This is an exact factor-line proof over the stated field,
not an inference from the finite audit.

## 5. Complete three-low cover

With exactly three low modes, two modes `a,b` belong to one family, the
third `c` to the other, and `h` is high in both.  The complementary-pair
indices are

```text
low pair a,b  -> M_(ch)=0,
low pair a,c  -> M_(bh) in {0,mu E_22},
low pair b,c  -> M_(ah) in {0,mu E_22}.
```

The same-family supports of `a,b` are disjoint, so at most one contains
colour `2`.  An `E_22` matrix requires both lows in its inducing cross-family
pair to contain colour `2`; consequently at most one of `M_(ah),M_(bh)` is
nonzero.  The exhaustive finite support replay found `14` compatible
`2+1` diagrams for each majority family and never more than one live edge.

The high map `A_h` is nonzero.  If it vanished, either mixed-factor
projection on `L_h` would use only two residual `R` covectors and have rank
at most two, contradicting that `h` is high.

### All three high-to-low matrices zero

If `M_(ah)=M_(bh)=M_(ch)=0` and `rank A_h=2`, nondegeneracy of `J` forces
all three low `A`-maps to vanish; then no quartic has two `A` suppliers.
Therefore `A_h` has rank one.  Each low image lies in its one-dimensional
orthogonal complement, so on the colour-`0,1` restriction the three low
maps have rank at most one and all pairings with `h` vanish.  The line-split
lemma contradicts the two live `d_0,d_1` tensors.

### Exactly one `E_22` matrix

Relabel so

```text
M_(bh)=mu E_22,          M_(ah)=M_(ch)=0.
```

The exact rank-one-shore lemma gives

```text
(rank A_b,rank A_h) in {(1,1),(1,2),(2,1)},
```

and any rank-one shore is supported only at colour `2`.

If `rank A_h=2`, the zero matrices force `A_a=A_c=0`, while `A_b` has rank
one and vanishes at colours `0,1`.  The pure `d_0,d_1` words again lack two
suppliers.  Hence `A_h` has rank one and is supported only at colour `2`.

Let `im A_h=Kq` and `Kp=q^perp`.  The two zero matrices put every column of
`A_a,A_c` in `Kp`; the off-`(2,2)` entries of `M_(bh)` put the colour-`0,1`
columns of `A_b` there too.  On the two-colour restriction, the high map is
zero and the other three maps are line shores.  The same line-split lemma
contradicts both live diagonal targets.

This closes every three-low diagram.  Since the only possible low counts
were `2,3,4`, exactly two remain.  Each family must contribute one, the lows
are distinct, and the other two modes have rank three under both families.

## 6. Final zero and `E_22` branches

Let `a,b` be the two lows and `s,t` the highs.

### Zero branch

If the low supports are disjoint, pair classification gives `M_(st)=0`.
Both high `A`-maps are nonzero: an `A`-rank-zero local plane has projection
rank at most two.  For nonzero subspaces of a nondegenerate two-space,

```text
J(im A_s,im A_t)=0
```

implies their dimensions sum to at most two.  Hence both high ranks are
one, with mutually orthogonal image lines.

### `E_22` branch

If the two different-missing low supports both contain colour `2`, then

```text
M_(st)=mu E_22,                  mu!=0.
```

The abstract rank-one-shore lemma gives preliminary high-rank profiles

```text
(1,1),(1,2),(2,1),
```

with each rank-one map supported only at colour `2`.

The `(1,1)` profile is impossible.  Both high maps vanish on their
colour-`0,1` columns, so only the two low modes can supply `x_4,x_5` there.
Their common pairing matrix

```text
B=A_a^T J A_b
```

is independent of the residual quadratic.  The nonzero pure `d_0` tensor
would force `B` to be a nonzero multiple of `E_00`, while the nonzero pure
`d_1` tensor would force the same matrix to be a nonzero multiple of
`E_11`.  These matrix units are independent.

Thus the high ranks are `(1,2)` or `(2,1)`.  Let `s` be rank one.  Its map
is supported only at colour `2`, and the off-`(2,2)` entries of `M_(st)`
put the colour-`0,1` columns of the rank-two high shore in the single line
orthogonal to `im A_s`.

If both lows also had colour-`0,1` `A`-rank at most one, then on the
two-colour restriction mode `s` would be the zero distinguished shore and
the other three modes would be line shores.  The line-split lemma would
again contradict the `d_0,d_1` targets.  Therefore at least one low has
colour-`0,1` rank exactly two.

These deductions establish the stated rank boundaries but do not construct
either branch.

## 7. Exact incidence-only fixtures

Both rational fixtures were replayed by independent matrix and polarization
implementations.  Each local `6 by 3` matrix has rank three and the four
projection-rank pairs are

```text
(2,3),(3,2),(3,3),(3,3).
```

The zero fixture has singleton `A_0` at colour `1`, singleton `A_1` at
colour `0`, high companions `U_0` at colour `0` and `U_1` at colour `1`,
four `A`-ranks `(1,1,1,1)`, and `M_(45)=0`.

The `E_22` fixture has singleton `A_0,A_1` lows both at colour `2`, both
forced companions in mode `L_4`, `A`-ranks

```text
(2,2,1,2),
```

colour-`0,1` ranks

```text
(2,2,0,1),
```

and `M_(45)=E_22`.  It meets both surviving sharp rank boundaries.

For every colour in both fixtures, at least one same-colour cross-mode
`A` pairing is nonzero, so neither fixture is rejected by a trivial missing
supplier.  Nevertheless exact complete polarization gives

```text
T_(m_1)(e_0,e_0,e_0,e_0)=-2
```

in each.  The required mixed target is zero.  The fixtures are therefore
countermodels only to an incidence-only closure, not to the conjecture or
to the theorem's exact target.

## 8. Field, quantifier, and finite-audit boundary

Characteristic zero is sufficient for every new step and for all frozen
dependencies.  The pair table and rank arguments use the nonvanishing of
the displayed factors `2`; the exact proof otherwise uses finite-dimensional
linear algebra, nondegeneracy of `J`, and factor uniqueness.  It uses no
order, positivity, algebraic closure, genericity, numerical approximation,
or finite-field-to-characteristic-zero inference.

The `F_3` enumeration checks `2704` zero-pair and `816` `E_22`-pair map
configurations.  It audits the rank-boundary algebra only.  The written
characteristic-zero arguments prove the zero and `E_22` conclusions.

Every double contraction in the pair classification uses lows from distinct
modes.  Pair matrices always belong to the complementary uncontracted mode
pair.  Every supplier argument assigns `x_4,x_5` to two distinct input
slots.  No same-mode double contraction or family/complement index reversal
survived review.

## 9. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                    PASS;
two-sided projection-drop primary and audit:        PASS;
kernel-support primary and audit:                    PASS;
exceptional-kernel primary and audit:                PASS;
noncommon/noncommon same-mode primary and audit:     PASS;
common/noncommon same-mode primary and audit:        PASS;
q_- same-mode primary and audit:                     PASS;
q_+ same-mode primary and audit:                     PASS;
support-two incidence primary and audit:             PASS;
py_compile on new and dependency scripts:            PASS;
Ruff on new and dependency scripts:                  PASS;
tracked and untracked whitespace checks:              PASS.
```

The primary verifier derives the double-contraction table from factorized
quartics with SymPy, exhausts all line/support pairs and every compatible
`2+1` diagram, checks the rank boundaries over `F_3`, and directly replays
both rational fixtures.

The independent audit imports neither the primary module nor SymPy.  It
rebuilds the quartics in the square-free algebra, uses a separate exact
`Fraction` row reducer and permutation polarizer, independently exhausts
the finite pair/support table, and verifies the fixtures.  Both executables
print `UNRESOLVED`, preserving the scientific boundary.

## 10. Accepted boundary

```text
same-mode cross-family lows:                            EXCLUDED;
common low line N:                                     EXCLUDED;
distinct-mode noncommon low pairs:                     CLASSIFIED;
four-low diagrams:                                     EXCLUDED;
three-low diagrams:                                    EXCLUDED;
low modes in every exact fixed-pair extension:         EXACTLY TWO;
family distribution:                                   ONE PER FAMILY;
other two modes:                                       HIGH IN BOTH;
zero high-pairing branch:                              OPEN;
E_22 high-pairing branch:                              OPEN;
incidence-only fixtures:                               NOT SOLUTIONS;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E

new primary verifier:
20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A

new independent audit:
F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56

two-sided projection-drop theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

kernel-support theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

exceptional-kernel theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

same-mode noncommon theorem:
BC8851D171C140163259385135B81F9A52567B57D36912C682CD181061966B68

same-mode common/noncommon theorem:
05F1655F238025804309A8A0071BA0B53FE4BB5A250DE76DD5ABF15438FAF990

q_- same-mode theorem:
3F4141CDE71069FB249025A0122C657F8F803DA922FDC47268181B5BE99D76D4

q_+ same-mode theorem:
2DFD23DFDE70593BF8363B633C15901D106CDF7F9C7C40C41B6CCA00CF1FBB50

support-two incidence theorem:
8C6B0EB9AA3BDD885A0703AB1EE902456045A7DEA89B66E0C097654F1189631F
```
