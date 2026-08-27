# Hostile review: equal-leaf H4 rank-six principal-open exclusion

Date: 2026-08-27

## Verdict

Accept `GLD88` as an **exact characteristic-zero principal-open exclusion**
inside the `H4` part of the displayed scale-fixed equal-leaf low-rank branch.
On a named six-minor open, two bordered Schur residuals have an explicit
nonzero linear coefficient determinant and force the displayed rational
three-parameter leaf family.  Its complete center kernel consists of matrices
with proportional rows, so no point of that open lies in `D(Omega)`.

Do not read this as closure of all `H4`.  The parameter, linear-coefficient,
and six-pivot boundaries remain open, including possible lower-rank strata.
No pulled-back `GLD83` Fitting ideal is computed.  Other components, gauges,
source branches, support profiles, triangles, roots, and orders remain open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Pointwise H4 classifier

On the chart `p+q-1 != 0`, the H4 equation gives

```text
s=(p+q-pq)/(p+q-1).
```

The primary verifier reconstructs the fixed `37 x 9` `GLD71` syndrome map
with free leaf shifts `b,c` and selects

```text
R6=(0,1,2,17,19,32),
S6=(0,1,3,4,6,7),
P6=det M(G)_(R6,S6).
```

It then borders this pivot at `(row,column)=(25,5)` and `(31,5)`.  On
`D(P6)`, rank at most six makes both bordered determinants zero.  After exact
division by `P6` and denominator clearing, both residual numerators are
linear in `b,c`.  The determinant of their coefficient matrix is checked
symbolically as

```text
Delta_lin = -6 (p-q)(p+q-1)(p^2-p+1)
               (p^2+2pq-2p-q)(2pq-p+q^2-2q)
               (2pq^2-2pq-p-q^2-2q+2).
```

Solving that exact two-by-two system on `D(Delta_lin)` gives the displayed
formulas `b=b(p,q,a)` and `c=c(p,q,a)` entry-for-entry.  This is stronger and
cleaner than a computation over `Q(p,q,a)`: the full pointwise coefficient
determinant is named, so no hidden generic denominator is discarded.

The review checked the incidence bridge.  At a scale-fixed incidence point,
`C_8=1` and `M(G)C=0`, so syndrome column eight is a combination of the first
eight.  The exact differentiated `GLD75` certificate used by `GLD86` gives

```text
rank A_lin = rank M(G)[:,0:8]
```

on the incidence base.  Therefore `rank A_lin<=6` implies full syndrome rank
at most six there.  The bordered-minor classifier applies to the actual
`GLD84` low-rank branch; it is not an ambient rank claim away from incidence.

## Forced-family kernel and determinant gate

After the two residuals force `b,c`, the primary verifies all `111` entries
of

```text
M_0 k^T=M_1 k^T=M_2 k^T=0
```

for the displayed rational vector `k=(u,v,1)`.  The three block-supported
copies of `k` are independent.  On the same `P6` open, the syndrome has rank
at least six, hence exactly six, and these vectors form its complete kernel.
Every compatible center therefore has the form

```text
C=[lambda_0 k; lambda_1 k; lambda_2 k]
```

and has rank at most one.  In the scale-fixed chart `C_8=1`, `lambda_2=1`;
the determinant remains zero.  Since `Omega` contains `det(C)det(G)^3`, this
excludes the classified family from `D(Omega)` without invoking the Fitting
ideal.

The forced-family six-minor numerator is a nonzero 176-term polynomial with
canonical SHA-256

```text
656128e97aa9b6e08ba57532aad1e8762eb201217cba15be58865e187214d5b5.
```

At `(p,q,a)=(0,3,0)`, the verifier obtains

```text
(s,b,c)=(3/2,2/13,-1/13),
k=(-7/8,-1/8,1),
det(G)=27/26,
P6=291600/13,
rank M(G)=6.
```

The exact nonzero value of `Delta_lin` is also checked there.  Thus the
declared open is nonempty; this is not a vacuous localization.

## Independent evidence and its limit

The independent audit imports no repository Python module and does not import
the primary verifier or the GLD71 syndrome builder.  It pins the immutable
GLD75 sparse bidirectional carrier by SHA-256
`05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57`,
reconstructs its ten scale-fixed equations, and independently rebuilds the
`10 x 8` center coefficient matrix.  On the forced family it exhibits a
separate nonzero six-pivot at the exact control point and proves symbolically
that the two-dimensional proportional-row center family satisfies all ten
equations.  Rank six makes that affine family complete, so every compatible
actual center is singular in the independent representation as well.

This audit does **not** independently rederive the two GLD71 bordered Schur
residuals.  The package therefore has independent evidence for the
forced-family incidence and center-singularity conclusion, while the
pointwise H4 classifier is carried by one exact primary implementation.  The
absence of a second classifier derivation is recorded rather than disguised
as full independence.

## Rejected stronger readings

- `GLD88` does not exclude `V(P6)`, `V(Delta_lin)`, `p+q-1=0`, or any other
  displayed parameter-denominator boundary.
- It does not prove the H4 low-rank branch empty or classify all lower-rank
  components.
- The rational family is forced only on the declared principal open; its
  formulas must not be specialized through a zero denominator.
- Center singularity is an `Omega`-gate exclusion, not a computation of the
  pulled-back `I_Pl` Fitting ideal.
- The theorem does not transfer itself to another gauge, unequal-leaf
  component, source presentation, support profile, triangle, root, or order.
- Exact symbolic identities and a characteristic-zero control point do not
  change the global status.

## Verification commands

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py
```

Both scripts report `UNRESOLVED` and retain every exceptional locus.

## Proof-tree delta

`GLD87` confines the determinant-safe rank-at-most-six branch to `H4`.
`GLD88` adds

```text
GLD87 -> H4 named principal open empty on D(Omega)
      -> H4 pivot/coefficient/parameter boundaries remain.
```

The next load-bearing task is to analyze those explicit exceptional loci and
the `GLD83` Fitting pullback there, retaining the full raw response incidence
at every `C_F` rank drop.  No global resolution claim is justified.
