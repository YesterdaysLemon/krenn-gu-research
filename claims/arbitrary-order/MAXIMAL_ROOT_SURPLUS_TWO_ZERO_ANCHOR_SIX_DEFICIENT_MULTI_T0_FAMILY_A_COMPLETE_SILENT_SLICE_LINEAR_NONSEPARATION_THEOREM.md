# Maximum-root surplus-two zero-anchor six-deficient multi-`T_0` Family-A complete silent-slice linear nonseparation

## Status

**PROVED exact characteristic-zero source-integrability boundary (`GLS79`).**

This theorem upgrades the two modular global row ranks recorded in `GLS78`
to an exact statement.  On the complete `c_5=0` coefficient family in both
remaining Family-A charts, no linear combination of literal matching
coefficients can cancel every monomial not containing the off-kernel physical coefficient

```text
I_2500=[e_(2,0)e_(5,0)]W_25
```

while retaining a monomial that contains it.  The family contains the one
nonzero-target all-zero word; its matching polynomial is retained as an
extra ambient column.  Therefore the theorem applies a fortiori to the
`2,186` actual zero-target rows.  The proof is an exhaustive
`105`-matching expansion followed by an exact decomposition into row-incidence
components of size at most two in the `r=2` chart and at most four in the
`r=3` chart.

This is a no-go theorem for the entire linear silent-slice route, not an
exclusion of either key.  Rows with `c_5!=0`, nonlinear coefficient-ideal
syzygies, activity localization, and arbitrary complete-source couplings are
not covered.  The Family-A `r=2,3` keys remain **OPEN**, the six-deficient
residual remains `97,215 / 79`, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 0. Parent chart and exact coefficient space

Use the `GLS71` crossed normalization and the two `GLS78` charts

```text
r=2:  S_0 R_2 R_1 R_0 T_0 T_0,       type RTT,
r=3:  S_0 R_2 R_1 T_0 T_0 T_0,       type TTT.       (1)
```

Relabel the outside ports as `3,4,5`, put the `R_0` port of the first chart
at `3`, and retain independent nonzero `T_0` slopes.  Impose only the named
silent source rows

```text
P_50=Q_50=0,                                           (2)
```

not silence of the other source colours at port `5`.  Keep every physical
edge entry and every other legal source-row coordinate independent.

Let `F_w` be the complete eight-vertex matching coefficient for the colour
word `w`.  Restrict to the complete family

```text
R={w in {0,1,2}^8 : c_5=0},       |R|=3^7=2,187.     (3)
```

Exactly one row in (3), the all-zero word, has the nonzero GHZ target
`mu_0`; the other `2,186` rows are zero-target rows.  Here `F_w` denotes the
left-side matching polynomial before subtracting any target scalar.  Retain
all `2,187` columns for a stronger ambient row-span calculation.  Any linear
separator formed from the zero-target equations would also be a separator
in this larger column space.  There are `105` perfect matchings of eight
vertices.

Write

```text
z=I_2500=[e_(2,0)e_(5,0)]W_25.                       (4)
```

Split the monomial coordinate space into the span `M_0` of monomials not
containing `z` and the span `M_z` of monomials containing it.  Let

```text
N:F^R -> M_0,       L:F^R -> M_z                     (5)
```

be the two coefficient matrices, with one column for each literal row.
Here the coefficient field is `QQ(kappa_4)` for `RTT` and
`QQ(kappa_3,kappa_4)` for `TTT`; `kappa_5` is inert on (2)--(3).

An ambient linear leakage separator is exactly a vector `a` satisfying

```text
Na=0,       La!=0.                                   (6)
```

Thus absence of a separator is the exact inclusion

```text
ker N subset ker L,                                  (7)
```

equivalently `rank N=rank [N;L]`.

## 1. Nonzero slopes form one local torus orbit

### Lemma 1.1

The existence or nonexistence of a separator in (6) is unchanged by
specializing every retained `T_0` slope to an arbitrary nonzero value.

### Proof

At a `T_0` port `u`, the source row plane is

```text
span(e_(u,0)^*, e_(u,1)^*+kappa_u e_(u,2)^*).
```

Apply the invertible local diagonal change that fixes colours `0,1` and
sends `e_(u,2)^*` to `kappa_u^(-1)e_(u,2)^*`.  It sends the displayed row
plane to the slope-one plane.  Applying the same change to every incident
physical edge is an invertible diagonal renaming and rescaling of literal
edge coordinates.  It preserves the weighted diagonal GHZ form, changing
only its nonzero colour-`2` weight.

The condition `c_5=0` is preserved, and (4) uses colour `0` at port `5`, so
the partition into monomials containing or not containing `z` is preserved.
Consequently the row columns and the two monomial spaces in (5) change only
by invertible diagonal maps.  In the inverse transport from slope one back
to `kappa`, if `d_(u,c)=1` except
`d_(u,2)=kappa_u`, then physical entries scale by

```text
I_(uv)^(ab) -> d_(u,a)d_(v,b) I_(uv)^(ab),
```

and the column of a word `w` scales by the nonzero product
`product_(u in T_0)d_(u,w_u)`.  Monomial coordinates have their corresponding
nonzero diagonal scalings.  Condition (6) is invariant. `square`

The rational-function calculation below is therefore generic and, by this
equivariance, has no additional exceptional fibre at a nonzero slope.

## 2. Exact global incidence decomposition

Make a graph whose vertices are the `2,187` literal rows.  Join two rows
when their expansions share a monomial in `M_0`.  By construction, `N` is
block diagonal on the connected components of this graph.  Hence

```text
ker N = direct-sum_C ker N_C.                         (8)
```

It is enough to check `L_C ker N_C=0` separately on every component that
contains a `z`-monomial.  This remains sufficient even if one leak monomial
were shared by different components, because each summand in (8) is killed
before the component images are added.

### Theorem 2.1 (complete silent-slice linear nonseparation)

For both charts in (1), inclusion (7) holds.  The exact component census is

| chart | zero rows | all components by size | leak-bearing components by size | `nullity(N)` | leak-component nullity sum/max | `rank N=rank[N;L]` |
|---|---:|---|---|---:|---:|---:|
| `RTT` | `162` | `837 x 1`, `675 x 2` | `133 x 1`, `133 x 2` | `495` | `27 / 1` | `1,692` |
| `TTT` | `0` | `243 x 1`, `486 x 2`, `243 x 4` | `81 x 1`, `162 x 2`, `81 x 4` | `288` | `100 / 3` | `1,899` |

In particular, none of the `266` `RTT` or `324` `TTT` ambient leak-bearing
components admits a separator.  The all-zero target row is by itself in a
rank-one size-one component, with four nonleak and two leak monomials, all
unique to that row.  Removing it leaves `2,186` zero-target columns, ranks
`1,691` and `1,898`, and respectively `265` and `323` leak-bearing
components; nonseparation and the two total nullities are unchanged.

For the actual zero-target subsets, the exact monomial and entry counts are

| chart | nonleak/leak monomials | nonzero entries in `N` / `[N;L]` |
|---|---:|---:|
| `RTT` | `16,187 / 574` | `21,290 / 22,107` |
| `TTT` | `22,586 / 979` | `36,680 / 38,631` |

The corresponding exact sparse-matrix census is

| chart | nonleak/leak monomials | nonzero entries in `N` / `[N;L]` |
|---|---:|---:|
| `RTT` | `16,191 / 576` | `21,294 / 22,113` |
| `TTT` | `22,590 / 981` | `36,684 / 38,637` |

### Proof

Expand every `F_w` in (3) by the perfect-matching recurrence.  For every
nonleak monomial, join all columns in which its coefficient is nonzero.
This gives the component census in the table.  The `162` zero `RTT` rows
are retained as singleton zero blocks; they contribute `162` to
`nullity(N)` and nothing to `L`.

For each leak-bearing component, form the exact matrix `N_C` over the
indicated rational-function field, compute its right nullspace, and evaluate
every leak-monomial row of `L_C` on every nullspace basis vector.  Every
evaluation is zero.  The displayed nullity sums and maxima give a complete
dimension check.  Summing the component ranks yields `1,692` and `1,899`;
adjoining all leak rows changes neither rank.  Equation (8) proves (7).
`square`

The retained verifier expands all `105` matchings rather than sampling
them.  As regression controls, two distinct large-prime specializations
independently reproduce the same two ranks and zero leak-rank increment;
the theorem itself is the exact component calculation, not those modular
checks.

## 3. Consequence and surviving obligation

`GLS78` proved exact nonseparation only in the named three-row and nine-row
blocks and recorded the full `c_5=0` ranks as modular evidence.  Theorem 2.1
removes the cross-block linear loophole: every linear combination of the
`2,186` zero-target silent-slice rows that cancels the repair monomials also
cancels every term containing the desired off-kernel coordinate (4).  The
same statement remains true after adjoining the one nonzero-target row as
an ambient column.

Therefore a load-bearing successor must leave the linear slice in at least
one of the following ways:

1. use rows with `c_5=1,2` and prove that their additional source-row terms
   synchronize with the `c_5=0` repairs through the same physical decks;
2. prove a nonlinear coefficient-ideal consequence, with every divisor and
   nonzero hypothesis stated and every exceptional component retained; or
3. give an exhaustive activity localization that supplies a different
   complete coefficient outside the no-go space (3).

This theorem does not show that a nonlinear separator exists, that every
source enters the silent slice, or that a complete source is impossible.
It removes no profile.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_active_t_leakage_row_span_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_complete_silent_slice_linear_nonseparation.py
```

The primary verifier constructs the complete `105`-matching expansion,
checks the representative `GLS78` identity and its named blocks, builds the
global nonleak incidence components, and proves (7) by exact nullspaces.  The
no-import audit reconstructs the expansion by a separate hafnian recurrence
and checks the equivalent exact stacked-rank criterion component by
component.

Neither program checks nonlinear ideal membership, rows outside (3), a
complete-source realization, either key exclusion, or the global conjecture.
