# Hostile review: equal-leaf survivor rank-at-most-six syndrome boundary

Date: 2026-08-27

## Verdict

Accept `GLD86` as an **exact characteristic-zero, set-theoretic boundary
containment** on the displayed scale-fixed equal-leaf chart. The theorem does
not claim that the rank-at-most-six branch is empty. It confines that branch
to the union of four named leaf-frame divisors and leaves all four available
after the `GLD83` `Omega` localization.

The global Krenn--Gu conjecture remains **UNRESOLVED**. No pulled-back
Fitting ideal is computed, no Gaussian rank-seven component is closed, and no
claim is transferred to another gauge, unequal-leaf component, source
presentation, support profile, root order, or triangle.

## Exact algebra audited

The primary verifier pins the `GLD75` sparse bidirectional certificate by its
canonical SHA-256
`05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57`, checks
its `37 x 10`/`10 x 37` shapes and `27`/`63` sparse term counts, and
reconstructs the ten basis generators after `x_8=0`. It then reconstructs the
fixed `GLD71` 37-row syndrome map

```text
M(G) in Mat_(37 x 9)(Q(i)[p,q,r,a,b,c])
```

and evaluates the named rows and columns

```text
R_7=(0,1,17,19,31,32,33),
S_7=(2,3,4,5,6,7,8).
```

The exact determinant is

```text
432 (p-q)^2 (p-s)^2 (q-s)^2
    (p q+p s+q s-p-q-s)^2,
    s=1+i+r.
```

The primary check also confirms that the determinant has no `a`, `b`, or `c`
terms. The independent no-import audit rederives the selected rows from
their compact syndrome formulas and expands the determinant with a separate
sparse polynomial engine over rational Gaussian pairs. It obtains the same
187-term expanded polynomial as the factored expression; this is not a
numerical sample or a SymPy replay under a second filename.

## The incidence and rank bridge

The review checked the only logical bridge needed beyond the determinant. The
`GLD71` rows form a basis of the annihilator of the rank-44 fixed star. The
`GLD75` certificate uses another basis of the same annihilator, so its
bidirectional polynomial identities imply, on the displayed chart,

```text
B=0 iff M(G)C=0.
```

The center is read row-major. The Gaussian center has final entry `1`, and
the scale equation is `x_8=0`; therefore `C_8=1` exactly, not merely on a
generic open. At an incidence-zero point, differentiating both directions of
the certificate with respect to the eight center shifts removes the terms
containing derivatives of the certificate matrices. Since `C` is affine in
those shifts and `g=A(z)c+q(z)`, this gives

```text
rank A(z)=rank M(G)[:,0:8]
```

on `B`. This equality is pointwise on `B`; it is not being asserted as an
ambient polynomial matrix identity away from the incidence locus.

With `C_8=1`, the zero syndrome replaces column 8 by a linear combination of
columns 0 through 7. In the selected determinant, replacements by columns 2
through 7 repeat an existing column. If the factored minor is nonzero, one of
the two remaining 7-by-7 minors using columns 0 or 1 is nonzero. Thus the
first eight syndrome columns, and hence `A`, have rank at least seven.

## Scope and boundary controls

The four factors are named

```text
H_1=p-q,
H_2=p-s,
H_3=q-s,
H_4=p q+p s+q s-p-q-s.
```

The exact conclusion is

```text
B intersect V(I_7(A))
  subseteq B intersect V(H_1 H_2 H_3 H_4).
```

After retaining the `GLD83` frame/gauge open, the same statement reads

```text
Z_low subseteq
  (B intersect V(H_1 H_2 H_3 H_4)) intersect D(Omega).
```

The review specifically rejects the following stronger readings:

- the displayed factorization does not prove any `H_j` divisor empty;
- `Omega` saturation does not invert any `H_j` here, so none of the four
  divisors is excluded after `Omega` saturation;
- the theorem does not claim that each divisor intersection is nonempty or
  that these four divisors are the complete irreducible decomposition;
- the syndrome minor does not compute `I_Pl` or prove a Fitting residual
  unit; and
- the Gaussian rank-seven point is not promoted to a component theorem.

These controls preserve the distinction between a rank boundary containment,
a divisor exclusion, and a pulled-back Fitting calculation.

## Verification and independence

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py
```

The primary verifier uses the established sparse parser and exact SymPy
arithmetic to reconstruct `M(G)`, check the factorization, verify the
scale-fixed Gaussian `C_8=1` point, and replay the rank-seven syndrome
control. The no-import audit uses only the standard library, `Fraction`, its
own Gaussian arithmetic, its own sparse multivariate-polynomial determinant,
and an independent exact constant-matrix column-replacement fixture. The
full bidirectional certificate identities remain an upstream `GLD75` proof
carrier; this package pins and scopes that dependency rather than claiming a
second replay is a new GLD86 conclusion.

Both scripts finish with the global status `UNRESOLVED` and explicitly report
that the `Omega`-saturated divisors and the pulled-back Fitting problem remain
open.

## Proof-tree delta and remaining obligation

`GLD84` named `V(I_7(A))` as the retained rank-at-most-six branch. `GLD86`
adds the exact edge

```text
GLD84 -> GLD86 -> GL
```

where the first edge is the syndrome-minor containment and the second edge
is the remaining divisor/Fitting/source/component work. The next load-bearing
task is to analyze `V(H_j) intersect D(Omega)` one divisor at a time, including
the `GLD83` Fitting pullback and the full raw response incidence on any
`C_F` rank drop. Any result on one divisor is a scoped successor and does not
close the other three.
