# Hostile review of fixed-pair support-two low double-contraction incidence

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
support-two exceptional-low, distinct-mode scope.**  No contraction,
line-type, colour-support, matrix-unit, rank, field, quantifier, dependency,
implementation, or scope blocker survived hostile review.

The package assumes two support-two exceptional low vectors in distinct
remaining local modes.  For different projection families it excludes the
three pairs that miss the same colour and localizes the other six pairs.  For
one projection family it proves that the only possible pair consists of `N`
and one non-`N` line, hence that the family has at most two support-two low
modes.  In every surviving case the `x_4,x_5` pairing between the other two
modes is a nonzero single diagonal matrix unit, forcing at least one of those
modes to have colour-supported `A`-projection rank one.

This is an incidence restriction, not an existence theorem or a complete
exclusion.  It does not apply the double-contraction argument to a
`Phi_1`-low and a `Phi_2`-low in the same local mode, does not classify
singleton-supported exceptional lows, and does not exclude the surviving
distinct-mode cells.  Unrestricted `P_6 -> Delta_3` nonrestriction remains
unknown, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SUPPORT_TWO_LOW_DOUBLE_CONTRACTION_INCIDENCE_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py
  audit_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py
```

Load-bearing frozen predecessor:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
  audit_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
```

The support labels also use the forced-zero table from the frozen
kernel-support boundary package.  Those uses were checked against the theorem
rather than inferred from filenames or earlier reviews.

## 1. Independent double-contraction derivation

For the two ambient kernels write

```text
p_1(a,b)=(a,0,b,a+b,0,0),
p_2(c,d)=(0,c,d,c+d,0,0).
```

Directly polarizing the five displayed complementary quartics and suppressing
the remaining `x_4x_5` pairing gives

```text
pair                         m_1      m_2      d_0

p_1(a,b),p_2(c,d)             0        0       2b(c+d)
p_1(a,b),p_1(A,B)             0       2aA      2bB
p_2(c,d),p_2(C,D)            2cC       0       2(c+d)(C+D)

pair                         d_1                         d_2

p_1(a,b),p_2(c,d)            2d(a+b)                    -2ac
p_1(a,b),p_1(A,B)            2(a+b)(A+B)                   0
p_2(c,d),p_2(C,D)            2dD                            0.
```

The mixed-channel zeros and every scalar sign agree with both implementations.
Rescaling either projective line representative multiplies both sides of the
contracted target equation by the same nonzero factor, so using the normalized
representatives below loses no cases.

If lows `p,q` occupy distinct modes and have local coefficient vectors
`alpha,beta`, let the two other modes have `A=span{x_4,x_5}` projection maps
`P,Q`, and put

```text
M=P^T J Q,
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.
```

For every channel `z`, twice contracting the exact full target gives

```text
sigma_(m_1) M=sigma_(m_2) M=0,
sigma_(d_c) M=lambda_c alpha_c beta_c E_cc.
```

The same matrix `M` occurs in all five equations because the contracted
vectors have zero `A`-part.  This bridge uses the full four-mode diagonal
target and the nonvanishing of each `lambda_c`; it is not a numerical or
generic surrogate.

## 2. Cross-family cell exhaustion

The predecessor and support-two hypothesis give the exact line data

```text
Phi_1: N misses 2, A_0 misses 0, C_0 misses 1;
Phi_2: N misses 2, A_1 misses 1, C_1 misses 0.
```

Each vector is supported on the complementary two-colour set.  Exhausting the
nine ordered cross-family pairs gives three same-missing pairs:

```text
(N,N), (A_0,C_1), (C_0,A_1).
```

For each, the scalar table is nonzero in both common support colours.  Since
the corresponding `alpha_c beta_c lambda_c` are nonzero, the one matrix `M`
would have to be a nonzero multiple of two distinct matrix units.  These three
pairs are therefore impossible.

The six remaining cells have one common colour and exactly one nonzero
diagonal scalar:

```text
Phi_1 line   Phi_2 line   common colour   channel   scalar

N            A_1               0            d_0       2
N            C_1               1            d_1      -2
A_0          N                 1            d_1       2
A_0          A_1               2            d_2      -2
C_0          N                 0            d_0      -2
C_0          C_1               2            d_2      -2.
```

In every row the target equation yields

```text
M=mu E_ee,                    mu!=0,
```

where `e` is the displayed common colour.  The theorem localizes these cells;
it does not assert that they are realizable.

## 3. Same-family count and surviving cells

For either family, every pair of non-`N` lines contains colour `2` in both
local supports, while the same-family `d_2` scalar vanishes identically.  Its
target equation is therefore

```text
0=lambda_2 alpha_2 beta_2 E_22,
```

with nonzero right side.  This excludes all three non-`N` pairs with
repetition.  For `N/N`, both the `d_0` and `d_1` scalars are nonzero, again
forcing two incompatible nonzero matrix units.

The only survivors are

```text
family   lines       common colour   channel   scalar

Phi_1    N,A_0             1           d_1       2
Phi_1    N,C_0             0           d_0      -2
Phi_2    N,A_1             0           d_0       2
Phi_2    N,C_1             1           d_1      -2.
```

Their family's potentially nonzero mixed channel has scalar zero because the
`N` representative has `a=0` or `c=0`, so it does not introduce an omitted
contradiction.  Each surviving row again gives `M=mu E_ee`.

Among any three support-two low modes in one family, two line types are both
`N` or both non-`N`.  Both possibilities were excluded above.  Thus the
claimed bound of at most two modes is exhaustive and does not assume that the
two non-`N` line types coincide.

## 4. Rank-one `A` shore

Suppose

```text
P^T J Q=mu E_ee,                   mu!=0,
```

for maps `P,Q:K^3 -> A`.  The nonzero right side makes both maps nonzero.  If
both had rank two, `Q` would be surjective and `P^T J` injective, so the
composite would have rank two, contradicting the rank-one right side.
Therefore

```text
(rank P,rank Q) in {(1,1),(1,2),(2,1)}.
```

If, for example, `P` has rank one, its `e`-column is nonzero because the
`(e,e)` entry is nonzero.  Write every other column as a scalar multiple of
that column.  Pairing it with the `e`-column of `Q` and using the zero
off-`e` rows forces every scalar to vanish.  Hence the rank-one shore is
supported only at colour `e`.  The symmetric argument handles rank-one `Q`.
When the other shore has rank two, its off-`e` columns lie in the unique
`J`-orthogonal line to the rank-one shore's nonzero `e`-column.

This is exact two-dimensional linear algebra.  It uses neither algebraic
closure nor a generic-position assumption.

## 5. Same-mode and quantifier audit

The double-contraction bridge requires the two lows to occupy two distinct
tensor slots.  Two vectors from one local plane cannot be inserted into two
copies of that one slot, so the proof correctly stops when a `Phi_1`-low and
a `Phi_2`-low occur in the same local mode.

Independently solving the ambient kernels gives

```text
ker(Phi_1) intersect ker(Phi_2)=K N.
```

Thus proportional same-mode lows must use `N`, while nonproportional lows use
different exceptional lines.  Neither case is excluded by this package, and
the theorem, checker reports, and status ledger all retain that boundary.

Characteristic zero is sufficient.  It makes the factors `2` nonzero and
supplies the field assumptions of the frozen predecessors.  The new argument
uses no order, positivity, square roots, algebraic closure, or division by an
unasserted parameter.

## 6. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                    PASS;
exceptional-kernel predecessor primary:             PASS;
exceptional-kernel predecessor independent audit:   PASS;
py_compile on new and predecessor scripts:           PASS;
Ruff on new and predecessor scripts:                 PASS;
tracked and untracked whitespace checks:             PASS.
```

The primary verifier uses SymPy factor polarization to derive all three
symbolic contraction rows, exhausts the nine cross-family and twelve
same-family line pairs, checks the three-mode counting consequence, and
exhausts all `531441` ordered pairs of `2 x 3` maps over `F_3` for the
rank-one-shore implication.

The independent audit imports neither the primary module nor SymPy.  It
expands the fixed quartics as square-free monomial dictionaries, contracts by
a distinct rational derivative implementation, independently reconstructs
the line-pair split, and exhausts the one-cell pairing geometry over `F_3`
and `F_5`.  It found respectively `2448` and `70560` one-cell
configurations, with exactly the three rank patterns in the theorem.  Its
separate rational row reduction also confirms ambient kernel union rank three
and intersection dimension one.  These finite-field runs audit identities
and finite linear algebra; the written characteristic-zero argument is the
proof.

## 7. Accepted boundary

```text
support-two exceptional lows in distinct modes:          ASSUMED;
cross-family same-missing pairs:                          EXCLUDED;
cross-family different-missing pairs:                     SIX LOCALIZED;
same-family pair types:                                   CLASSIFIED;
support-two low modes per family:                         AT MOST TWO;
surviving other-mode A-ranks:                             (1,1),(1,2),(2,1);
rank-one A shore supported at the common colour:          PROVED;
same-mode cross-family lows:                              OPEN HERE;
existence or exclusion of surviving cells:                OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
8C6B0EB9AA3BDD885A0703AB1EE902456045A7DEA89B66E0C097654F1189631F

new primary verifier:
F7998E863E519BC1620384D94D9E3BF9F318907C7795A65BD50BD1A8195DF54B

new independent audit:
455E7196E534818602AA7385A54DF748DE5A9329F88E7E3CF10B8A2E7CB9CA32

exceptional-kernel predecessor theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

exceptional-kernel predecessor primary verifier:
256D1F4DEB3639E912E41C426E2D28E5FCB384C72DCDB00F9592064D33C904E5

exceptional-kernel predecessor independent audit:
90014EC8E37B0F48F26BD4A9528E235F2FC26D5E757948E34B1744B1B743D6F1
```
