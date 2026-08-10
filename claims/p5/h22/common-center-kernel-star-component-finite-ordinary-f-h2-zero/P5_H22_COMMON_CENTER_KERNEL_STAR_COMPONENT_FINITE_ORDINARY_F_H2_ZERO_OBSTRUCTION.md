# Component 23 ordinary finite F-zero, h2-zero weighted-H22 obstruction

## Status

**VERIFIED EMPTY.**  Over \(K=\mathbb Q(r,t)\), the component-23 finite
weighted-H22 incidence is empty on

\[
 \lambda\notin\{0,1,-1\},\qquad F=0,\qquad h_2=0
\]

for all remaining affine markings.  Here \(F\) is the exact selected-minor
factor from
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md`.

The branches \(F=0,h_3=0\) and \(F=0,H=0\) with \(h_2\ne0\) remain
**UNKNOWN**.  Thus this result does not close the full generic finite fibre
or the global Krenn--Gu conjecture.

## Exact solution of F = 0

After setting \(h_2=0\), the coefficient of \(h_1\) in \(F\) factors as

\[
 -r(\lambda-1)(r-t)(rt-1).
\]

This is a unit over the ordinary-weight localization of the generic
coefficient field.  The verifier solves \(F=0\) exactly for \(h_1\), with no
rational specialization.

## Uniform ordinary-weight localization

To avoid treating \(\lambda\) as merely transcendental, introduce \(u\) and
the exact inverse equation

\[
 u\lambda(\lambda-1)(\lambda+1)-1=0.
\]

Substitute the solved \(h_1\) and \(h_2=0\) into all 28 shared mixed rows.
Denominators are cleared by one common multiplier per row; they are units in
this localization.  Add the inverse relation times each of the eight basis
vectors.  Exact standard-basis reduction over

\[
 K[h_0,h_3,\lambda,u]
\]

then gives the full free module

\[
 M=\langle e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8\rangle.
\]

Both inclusions are checked.  Hence no nonzero shared mixed-kernel extension
exists anywhere on this branch for any \(\lambda\notin\{0,1,-1\}\).

## Updated boundary

The sole remaining component-23 ordinary finite locus is contained in

\[
 \lambda\notin\{0,1,-1\},\qquad F=0,\qquad h_2\ne0,
 \qquad (h_3=0\ \text{or}\ H=0).
\]

This residual is **UNKNOWN**.  No finite-field calculation is used as proof.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement/verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-ordinary-f-h2-zero/verify_p5_h22_common_center_kernel_star_component_finite_ordinary_F_h2_zero_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-ordinary-f-h2-zero/audit_p5_h22_common_center_kernel_star_component_finite_ordinary_F_h2_zero_obstruction.py
```
