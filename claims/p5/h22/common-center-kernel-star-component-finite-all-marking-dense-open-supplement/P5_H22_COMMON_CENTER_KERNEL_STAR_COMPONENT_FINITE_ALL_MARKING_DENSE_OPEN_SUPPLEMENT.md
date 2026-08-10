# Component 23 finite all-marking weighted-H22 dense-open supplement

## Status

**VERIFIED PARTIAL SUPPLEMENT.**  Over \(K=\mathbb Q(r,t)\), the generic
finite all-marking weighted-H22 fibre for the common-center-kernel star
component is empty on an explicit dense open.  In addition, the entire
\(\lambda=-1\) all-marking slice is empty.  Explicit residual intersections
remain **UNKNOWN**, so the generic finite fibre and the global Krenn--Gu
conjecture remain unresolved.

This supplement uses the component rows and the 28-row shared mixed module
defined in `P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_PARTIAL.md`.  Number
the fourteen mixed words for \(D_{01}\) by 0 through 13 in lexicographic
order, followed by the fourteen \(D_{23}\) words numbered 14 through 27.
Every rational row is cleared by a single common row multiplier.

## First dense-open minor

The 8-by-8 minor on rows

\[
 (0,1,3,7,8,9,11,12)
\]

and all extension columns is associated over \(K\) to

\[
 \lambda(\lambda-1)^2(\lambda+1)^3F,
\]

where

\[
\begin{aligned}
F={}&(-2r^4t^2+2r^3t+2r^2t^2-2rt)h_0h_2\lambda\\
&+(-r^4t^2+r^3t^3+r^3t-rt^3-rt+t^2)h_0h_3\lambda\\
&+(r^4t^2+r^3t^3-r^3t-2r^2t^2-rt^3+rt+t^2)h_0h_3\\
&+(r^4t^2-r^3t-r^2t^2+rt)h_0\lambda\\
&+(-r^3t+r^2t^2+r^2-rt)h_1\lambda\\
&+(2r^4-2r^3t-2r^2+2rt)h_2\lambda\\
&+(-r^4t^2+r^3t+r^2t^2-rt)h_0\\
&+(r^3t-r^2t^2-r^2+rt)h_1\\
&+(-2r^3t+2r^2t^2+2rt-2t^2)h_3\\
&+(-r^3t+r^2t^2+r^2-rt)\lambda\\
&+(r^3t-r^2t^2-r^2+rt).
\end{aligned}
\]

Where this determinant is nonzero, the mixed matrix has rank eight.  Its
kernel is zero, so neither required beta diagonal can be nonzero.

## Cross-contraction minor

The 8-by-8 minor on rows

\[
 (0,1,2,3,7,8,9,14)
\]

is associated over \(K\) to

\[
 h_2h_3H(\lambda-1)^3(\lambda+1)^4,
\]

where

\[
\begin{aligned}
H={}&(2r^2-2rt-2r+4t^2+2t-4)h_3\lambda\\
&+(4r^2-2rt-2r+2t^2+2t-4)h_3\\
&+(r^2-rt+r-t)\lambda-r^2-rt+r-t+2.
\end{aligned}
\]

This removes \(\lambda=0\) as a whole exceptional divisor from the first
minor; only its intersection with \(h_2h_3H=0\) remains.

## Complete lambda = -1 slice

After setting \(\lambda=-1\), exact standard-basis reduction over

\[
 K[h_0,h_1,h_2,h_3]
\]

gives the full free row module

\[
 M=\langle e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8\rangle.
\]

Both inclusions are checked.  Hence the entire all-marking
\(\lambda=-1\) slice is empty, not merely a dense open in that slice.

## Exact remaining boundary

Combining the two determinant covers and the complete \(\lambda=-1\) result
leaves only

\[
\begin{array}{ll}
\lambda=1, & \text{all markings};\\
\lambda=0, & h_2h_3H=0;\\
\lambda\notin\{0,1,-1\}, & F=0\ \text{and}\ h_2h_3H=0.
\end{array}
\]

These loci are **UNKNOWN** here.  The earlier canonical-marking theorem and
the full \(t=3\) theorem still close their intersections with this residual.

A broad cross-contraction basis search exceeded 120 seconds and yielded no
certificate.  It is not theorem evidence.  No finite-field computation or
rational specialization is used in the generic proof.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement/verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement/audit_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
```
