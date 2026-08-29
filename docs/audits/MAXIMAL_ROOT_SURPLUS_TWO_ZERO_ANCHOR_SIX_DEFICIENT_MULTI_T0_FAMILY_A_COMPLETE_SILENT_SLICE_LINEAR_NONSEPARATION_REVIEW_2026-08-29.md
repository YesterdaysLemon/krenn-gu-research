# Hostile review: multi-`T_0` Family-A complete silent-slice linear nonseparation

Date: 2026-08-29

Reviewed package:

- `claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_MULTI_T0_FAMILY_A_COMPLETE_SILENT_SLICE_LINEAR_NONSEPARATION_THEOREM.md`
- `claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_active_t_leakage_row_span_boundary.py`
- `claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_complete_silent_slice_linear_nonseparation.py`

## Verdict

**PASS as a scoped exact characteristic-zero linear nonseparation theorem.**

The package proves that the complete `2,187`-row `c_5=0` literal coefficient
family has no linear leakage separator for `I_2500` in either remaining
Family-A chart.  The all-zero word is the sole nonzero-target row on this
slice; its left-side matching polynomial is an isolated rank-one component.
The ambient result therefore applies a fortiori to the other `2,186`
zero-target rows.  It does not prove nonlinear ideal membership, use rows with
`c_5!=0`, localize every source to this slice, exclude either key, or resolve
Krenn--Gu.

The Family-A `r=2,3` keys remain **OPEN**, the residual remains
`97,215 / 79`, and the global conjecture remains **UNRESOLVED**.

## 1. Exact obligation audited

For each chart, the complete `c_5=0` left-side matching matrix was split into

```text
N = rows indexed by monomials not containing I_2500,
L = rows indexed by monomials containing I_2500.
```

Literal coefficient words are the columns.  A linear separator exists
exactly when some column vector `a` has

```text
Na=0,       La!=0.
```

Thus the claimed theorem is precisely

```text
ker N subset ker L,
```

or equivalently `rank N=rank[N;L]`.  This orientation was checked directly;
the computation is not confusing monomial rows with literal coefficient
columns.

The primary and independent scripts explicitly check that the all-zero
target row has six monomials (four nonleak and two leak), all unique to its
rank-one singleton component.  Removing that column lowers the two ranks to
`1,691` and `1,898`, and the leak-bearing component counts to `265` and
`323`, without changing either total nullity or the nonseparation verdict.
The resulting zero-target monomial counts are `16,187/574` and
`22,586/979`; their nonleak/full nonzero-entry counts are
`21,290/22,107` and `36,680/38,631`.

## 2. Independent reconstruction

The primary verifier expands an explicitly enumerated set of all `105`
perfect matchings of eight vertices.  The no-import audit does not import
that verifier or SymPy.  It instead reconstructs each coefficient by the
pointed hafnian recurrence, normalizes all nonzero `T_0` slopes to one using
the proved local torus action, and performs exact Gaussian elimination with
standard-library rational numbers.

A separate hostile calculation also rebuilt the rational-function matrices
and checked them in two independent ways:

1. sparse exact forward elimination with rational-function cancellation;
2. exact `DomainMatrix` ranks over `QQ(kappa_4)` and
   `QQ(kappa_3,kappa_4)`.

All three routes agree.

## 3. Exact matrix and component census

The reproduced global counts are

| chart | nonleak/leak monomials | nonzero entries in `N` / `[N;L]` | `rank N` | `rank[N;L]` | total column nullity |
|---|---:|---:|---:|---:|---:|
| `RTT` | `16,191 / 576` | `21,294 / 22,113` | `1,692` | `1,692` | `495` |
| `TTT` | `22,590 / 981` | `36,684 / 38,637` | `1,899` | `1,899` | `288` |

The graph joining literal rows that share a nonleak monomial has

```text
RTT: 1,512 components = 837 of size 1 + 675 of size 2,
TTT:   972 components = 243 of size 1 + 486 of size 2 + 243 of size 4.
```

The leak-bearing subcensus is

```text
RTT: 266 components = 133 of size 1 + 133 of size 2,
TTT: 324 components =  81 of size 1 + 162 of size 2 + 81 of size 4.
```

Every leak monomial occurs in exactly one of those components.  This is
stronger than needed: because `N` is block diagonal, proving that `L` kills
each component kernel already kills their direct sum even if leak coordinates
were shared.

Every leak-bearing component passes the exact stacked-rank test.  Their
nullity sums/maxima are `27/1` for `RTT` and `100/3` for `TTT`.  The
nonleak-only components contribute the remaining `468` and `188` nullity
dimensions, respectively.

## 4. Slope fibres

At a `T_0` port, let `d_(u,c)=1` except `d_(u,2)=kappa_u`.  Local diagonal
transport scales a physical coordinate by

```text
I_(uv)^(ab) -> d_(u,a)d_(v,b) I_(uv)^(ab)
```

and a literal word column by the nonzero product

```text
product_(u in T_0) d_(u,w_u).
```

This sends the slope-one row plane to the `kappa_u` row plane, preserves the
weighted diagonal GHZ shape, and acts by invertible diagonal maps on both
matrix axes.  Since `I_2500` has colour zero at both endpoints, its
divisibility partition is preserved.  The hostile audit checked the scaling
identity on all `2,187` rows in both charts with zero failures.

Therefore the exact slope-one audit transports to every allowed nonzero
slope.  The result is not merely a generic rational-function statement and
has no omitted nonzero exceptional slope fibre.

## 5. Repaired audit issue

During development of the global component check, an empty-list SymPy matrix
lost the intended column count on the `162` identically zero `RTT` rows.  That
first aggregation understated the total `RTT` nullity by `162`.  Those rows
contain no leak monomial, so the issue did not affect any leak-bearing
component or the nonseparation verdict.  The retained primary verifier now
constructs an explicit `0 x column_count` matrix, reproduces total nullity
`495`, and asserts the `162` zero-row count.  The standard-library audit
handles the same boundary independently.

This issue was found and repaired before promotion.  It did not affect the
previous GLS78 named-block theorem, whose tested matrices all have nonleak
rows.

## 6. Scope controls

The following stronger statements are **not** proved:

- that a nonlinear combination of coefficient equations cannot isolate the
  off-kernel coordinate;
- that rows with port-`5` colours `1,2` add no useful coupling;
- that every hypothetical source has the silent rows used here;
- that another off-kernel physical coordinate has the same no-go property;
- that either Family-A key is empty;
- that any other all-rigid, unique-nonrigid, anchor, attachment, or
  local-to-global branch is closed.

The correct next obligation is nonlinear, cross-slice, or an exhaustive
activity localization outside this linear no-go space.

## 7. Reproduction

From repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_active_t_leakage_row_span_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_complete_silent_slice_linear_nonseparation.py
```

Both commands exit zero and print the exact component census and equal
stacked ranks.  Passing them supports only the theorem scope above.
