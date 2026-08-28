# GLD89 hostile review: `P=0` and `d0=0` H4 boundary safety

## Review disposition

**Accepted as a scoped exact theorem package, with the global conjecture still
`UNRESOLVED`.** The package proves only

```text
B intersect V(I_7(A)) intersect D(Omega) intersect H4 intersect V(P) = empty,
B intersect V(I_7(A)) intersect D(Omega) intersect H4 intersect V(d0) = empty,
```

on the complete scale-fixed equal-leaf chart. It does not claim that all of
`H4` is excluded, that the pulled-back `GLD83` Fitting ideal is a unit, or
that other gauges, components, source branches, roots, orders, or profiles
are covered.

## Exact evidence inspected

The primary verifier
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_p_divisor_and_d0_overlap_determinant_safety.py`
reconstructs the fixed `37 x 9` `GLD71` syndrome matrix over characteristic
zero and checks:

1. the two `P=0` six-minors on rows `(0,1,2,17,19,32)` and
   `(0,1,2,17,19,31)`, columns `(0,1,3,4,6,7)`;
2. both `GLD88` bordered residual numerators, reduced modulo `P`;
3. the two alternate bordered seven-minors at the `mP=0,m3!=0` boundary,
   including their coefficient cross-consistency factor and the remaining
   `c` equation;
4. all `3*37=111` block-column kernel identities on both forced slices;
5. the `q!=0`, `q=0`, `q=1`, and `q=-1` seven-minor branches when both
   six-minors vanish; and
6. the independent `d0=0` chart rows `(0,1,17,19)` without dividing by `d0`.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_p_divisor_and_d0_overlap_determinant_safety.py`
imports neither SymPy nor a repository verifier. It repeats the reduced
factor algebra in a sparse `Fraction` quotient, evaluates the relevant
linear resultants, reconstructs the `d0` two-by-two system, and checks the
exceptional-factor contradiction relations. It intentionally reports that
it does not rebuild all 37 source rows; that distinction is preserved rather
than calling the audit a second full syndrome replay.

Both scripts pass on the reviewed tree. The primary output reports
`Q_characteristic_zero_then_C`, `111` kernel identities, all eleven listed
exceptional seven-minor factors, and `global_conjecture_resolved: false`.

## Mathematical checks

### P branch, `d0!=0`

The identity

```text
Q=(q-p)d0+P
```

removes the `Q=0` subcase on `P=0,d0!=0` after the already accepted `GLD87`
H1 exclusion. The exact resultants of `P` with `d0`, `pq-1`, `e`, `L2`,
`p+1`, and `2pq-p-q-1` supply the nonvanishing factors used in the two
rank-six branches.

On the named six-pivot open, the two bordered residuals force
`c=-a`, `a=B0/(3L2)`. The complete syndrome kernel then contains the three
block-supported copies of `(-1,0,1)`; the nonzero pivot makes these the whole
kernel, so every compatible center has proportional rows.

At the pivot boundary, `F1=0` and `F3!=0` force `q^2!=1`. The alternate
bordered minors have exact cross factor

```text
-3 a^2(q-1)(q+1)^2 Q^2(p+1)(3a-p-1)d0^6 mod P,
```

and then force
`a=(p+1)/3`, `b=q^2/(1-q^2)`, `c=-(p+1)/3`. The alternate six-minor is
`6(q+1)Q^4`, and the same complete common kernel makes the center singular.

When both six-minors vanish, the verifier reconstructs every exceptional
factor used in the case split. For `q^2!=1,q!=0` the `K=2pq-p-q-1`
seven-minor is nonzero on the determinant-safe open; `q=0` has two minors.
The `q=1` and `q=-1` tables are separately checked, including the
`c=-1` subcases. No genericity assertion is substituted for these cases.

### `d0=0` overlap

The proof changes chart. `H4+d0=0` gives `q=1-p` and `P=0`, with `s` free.
Rows `(0,1,17,19)` give the exact equations

```text
x0+x1+x2=0,
-y0-y1+s^3*y2=0,
f*(x2+(s-1)y2)=0,
f*((s-1)x2-s*y2)=0,
f=s^2-s+1.
```

For `f!=0`, the two-by-two determinant is `-f`, forcing
`x=(u,-u,0)` and `y=(v,-v,0)`, hence a singular center. For `f=0`, the two
roots are `s=p` and `s=q`, exactly the GLD87 H2/H3 cases. This use of GLD87
is explicit and does not claim an H4 theorem beyond the named overlap.

## Residual obligations

The following remain open and must not be inferred closed from GLD89:

| residual | disposition |
| --- | --- |
| `L1=0` | only the prior GLD88 principal-open argument; `L1 intersect V(P6)` retained |
| `L2=0` | only the prior GLD88 principal-open argument; `L2 intersect V(P6)` retained |
| `e=0` | only the prior GLD88 principal-open argument; `e intersect V(P6)` retained |
| pure `P6` with no named `Delta` factor | retained for complementary GLD90 work |
| pulled-back `GLD83` Fitting ideal | not computed here |
| other charts/components/source branches | open |
| global Krenn--Gu conjecture | `UNRESOLVED` |

The result is therefore a real reduction of the H4 boundary, not a global
resolution or a full `H4` emptiness claim.
