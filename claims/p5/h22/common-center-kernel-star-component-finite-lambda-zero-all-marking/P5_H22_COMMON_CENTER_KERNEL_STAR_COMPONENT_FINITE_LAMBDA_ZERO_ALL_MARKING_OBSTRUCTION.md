# Component 23 finite lambda-zero all-marking weighted-H22 obstruction

## Status

**VERIFIED EMPTY, using the prior exact cofactor cover.**  Over
\(K=\mathbb Q(r,t)\), the complete finite \(\lambda=0\) weighted-H22
incidence on component 23 is empty for every affine marking.

This result combines the \(\lambda=0\) specialization of the selected minor
in
[`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md`](../common-center-kernel-star-component-finite-all-marking-dense-open-supplement/P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md)
with three exact row-module computations below.  It does not close the
ordinary finite residual away from \(\lambda=0,\pm1\), the complete generic
finite fibre, or the global Krenn--Gu conjecture.

## Prior factor cover

The cross-contraction 8-by-8 minor from the dense-open supplement specializes
at \(\lambda=0\) to a coefficient-field unit times

\[
 h_2h_3H_0,
\]

where

\[
 H_0=(4r^2-2rt-2r+2t^2+2t-4)h_3-r^2-rt+r-t+2.
\]

Thus the mixed matrix has full rank away from \(h_2h_3H_0=0\), and any bad
lift must lie on one of the three factor branches.

## Exact branch modules

On each of

\[
 h_2=0,\qquad h_3=0,\qquad H_0=0,
\]

the 28 shared mixed rows generate the complete free module

\[
 K[\text{remaining markings}]^8.
\]

For the last branch the verifier solves the linear equation exactly as

\[
 h_3=\frac{r^2+rt-r+t-2}{4r^2-2rt-2r+2t^2+2t-4}.
\]

The denominator is a unit in the generic coefficient field \(K\).  For all
three branches, both module inclusions are checked and all four diagonal rows
reduce to zero.  Hence no nonzero shared mixed-kernel extension exists on
any branch.  Combined with the prior cover, this closes all of \(\lambda=0\).

## Updated finite boundary

The separate exact supplements now close \(\lambda=-1,0,1\).  The remaining
generic finite component-23 locus is contained in

\[
 \lambda\notin\{0,1,-1\},\qquad F=0,\qquad h_2h_3H=0,
\]

where \(F,H\) are defined in the dense-open supplement.  This residual is
**UNKNOWN**.  No branch timed out, and no rational specialization or
finite-field calculation is used in the generic proof.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement/verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/verify_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/audit_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
```
