# Maximum-root surplus-two zero-anchor six-deficient multi-`T_0` Family-A complete all-active linear nonseparation

## Status

**PROVED exact characteristic-zero universal linear boundary (`GLS80`).**

Restore every source-row coordinate at all three outside ports in the two
remaining Family-A charts.  Among all `6,558` zero-target colour words, no
scalar linear combination of the complete eight-vertex matching equations
can cancel every monomial not containing

```text
I_2500=[e_(2,0)e_(5,0)]W_25
```

while retaining a monomial that contains it.  This closes the cross-slice
linear loophole left by `GLS79`: the result uses every port-`5` colour row,
not only `c_5=0`.

The theorem is a universal polynomial-identity no-go.  It does not exclude
new relations after specializing source or physical coordinates, nonlinear
coefficient-ideal syzygies, activity-localized cells, a different leakage
coordinate, or either complete key.  Family A `r=2,3` remain **OPEN**, the
six-deficient residual remains `97,215 / 79`, and global Krenn--Gu remains
**UNRESOLVED**.

## 0. Complete row-plane charts

Use the `GLS71` crossed normalization and the `GLS78` parent charts

```text
r=2:  S_0 R_2 R_1 R_0 T_0 T_0,       type RTT,
r=3:  S_0 R_2 R_1 T_0 T_0 T_0,       type TTT.       (1)
```

Put the `R_0` port of `RTT` at `3`.  At every `T_0` port retain the complete
row plane

```text
J_u=span(e_(u,0)^*, e_(u,1)^*+kappa_u e_(u,2)^*),
kappa_u!=0.                                             (2)
```

Unlike `GLS78`--`GLS79`, impose no silent source row at port `5`: every
`P_a,Q_a` coordinate on (2), including `a=0`, is an independent literal
variable.  Keep all physical edge coordinates independent as well.  This is
an ambient universal polynomial chart; it does not assert that every listed
coordinate is nonzero at a source point.

For each word `w in {0,1,2}^8`, let `F_w` be its left-side complete matching
polynomial.  Remove exactly the three diagonal GHZ target words

```text
0^8,       1^8,       2^8.                            (3)
```

The remaining set `R_0` has `6,558` literal zero-target equations.  Put

```text
z=I_2500.                                             (4)
```

As in `GLS79`, split the monomial coefficient space into `M_0`, spanned by
monomials not containing `z`, and `M_z`, spanned by monomials containing it.
Let

```text
N:F^(R_0) -> M_0,       L:F^(R_0) -> M_z.             (5)
```

The exact linear-separation question is

```text
Does some a satisfy Na=0 but La!=0?                  (6)
```

Coefficients of `a` lie in the slope field: `QQ(kappa_4,kappa_5)` for
`RTT` and `QQ(kappa_3,kappa_4,kappa_5)` for `TTT`.

## 1. The complete cross-port repair identity

The active port-`4` difference already shows why restoring port `5` does not
produce a simple separator.  In the `TTT` chart, write

```text
d_24=I_2402-kappa_4 I_2401,
d_14=I_1422-kappa_4 I_1421,
d_04=I_0422-kappa_4 I_0421,
d_34=I_3402-kappa_4 I_3401,
d_45=I_4520-kappa_4 I_4510.                           (7)
```

Direct expansion of the two literal rows gives

```text
F_02220020-kappa_4 F_02220010
 =(P_300 Q_520+P_500 Q_320)
    (I_0122 d_24+I_0220 d_14+I_1220 d_04)
  +I_1220(P_500 d_34+P_300 d_45)
  +P_500(I_1320 d_24+I_2300 d_14)
  +P_300(I_2500 d_14+I_1520 d_24).                   (8)
```

Thus the desired `P_300 I_2500 d_14` term is accompanied not only by the
old `W_15,W_45` channels but also by the newly restored
`P_500,Q_320` channels.  The retained verifier checks (8) term by term.
Applying the analogous second active-port difference removes `I_2500`
rather than isolating it.

Equation (8) is illustrative.  The theorem below uses all zero-target rows,
not only this block.

## 2. Exact complete-family theorem

Join two literal zero-target columns whenever their polynomials share a
nonleak monomial.  The matrix `N` is block diagonal on the resulting
components, so

```text
ker N = direct-sum_C ker N_C.                         (9)
```

### Theorem 2.1 (complete all-active linear nonseparation)

For both charts in (1),

```text
ker N subset ker L,
rank N=rank[N;L].                                    (10)
```

The exact component census is

| chart | all components by size | leak-bearing components by size | total nullity | leak nullity sum/max | `rank N=rank[N;L]` |
|---|---|---|---:|---:|---:|
| `RTT` | `728 x 1`, `1,458 x 2`, `2 x 3`, `727 x 4` | `132 x 1`, `133 x 2` | `1,764` | `0 / 0` | `4,794` |
| `TTT` | `242 x 1`, `729 x 2`, `729 x 4`, `2 x 7`, `241 x 8` | `80 x 1`, `162 x 2`, `81 x 4` | `1,098` | `55 / 1` | `5,460` |

The sparse-matrix census is

| chart | nonleak/leak monomials | nonzero entries in `N` / `[N;L]` |
|---|---:|---:|
| `RTT` | `49,703 / 574` | `85,874 / 86,691` |
| `TTT` | `69,710 / 979` | `143,024 / 144,975` |

In `RTT`, every leak-bearing component already has zero nonleak nullity.  In
`TTT`, the `55` surviving component-kernel dimensions are all killed by `L`.

### Proof

Enumerate all `105` perfect matchings of eight vertices and expand each of
the `6,558` words outside (3).  Build the component graph from shared
nonleak monomials.  For every component, form `N_C` and append all its leak
rows to form `[N_C;L_C]`.  Exact rational-function nullspaces give the census
above and equal ranks in every component.  Equation (9) proves (10).
`square`

An independent no-import audit instead normalizes every slope to one,
reconstructs all coefficients by the pointed hafnian recurrence, and checks
the equivalent stacked-rank criterion using standard-library rational
arithmetic.  The two derivations give the same census.

## 3. Nonzero slopes and specialization boundary

At each `T_0` port, the local diagonal torus fixing colours `0,1` and scaling
colour `2` transports (2) to the slope-one plane.  It acts by invertible
diagonal scalings on literal word columns and monomial rows.  Because (4)
uses colour zero at port `5`, the leak/nonleak partition is preserved.
Consequently (10) holds at every allowed nonzero slope, not only generically.

This equivariance applies to slopes, not to arbitrary specializations of the
source and physical edge variables.  Such a specialization can merge or
erase monomials and create new fibrewise linear relations.  An exhaustive
activity localization exploiting one of those relations remains a legal
successor.

## 4. Exact successor obligation

The direct linear programme is now exhausted at three nested levels:

```text
proper-face/kernel selectors              GLS78 boundary,
complete c_5=0 linear span                 GLS79 boundary,
complete 6,558-row zero-target linear span GLS80 boundary.             (11)
```

A key-closing successor must therefore do at least one of the following:

1. prove nonlinear ideal membership or a saturated consequence of the
   complete coefficient equations, with every divisor and exceptional
   component retained;
2. prove an exhaustive activity/source-coordinate localization on which a
   new specialized linear relation becomes legal; or
3. construct an exact complete-source control, which would refute the
   proposed exclusion route and require dedicated validation before any
   conjecture-level interpretation.

No profile is removed by this theorem.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_r2_complete_all_active_linear_nonseparation.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_r3_complete_all_active_linear_nonseparation.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_complete_all_active_linear_nonseparation.py
```

The two primary verifiers use explicit matching enumeration and retain the
independent slope symbols.  Both check the representative one-port identity;
the `TTT` primary also checks the displayed two-active-port continuation.
The independent audit uses a separate hafnian recurrence, slope-one torus
normalization, and exact rational stacked ranks.

None of these programs tests nonlinear syzygies, specialized
source-coordinate fibres, activity exhaustiveness, either key exclusion, or
the global conjecture.
