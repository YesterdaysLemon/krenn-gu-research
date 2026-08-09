# Component 23 finite lambda-one all-marking weighted-H22 obstruction

## Status

**VERIFIED EMPTY.**  Over \(K=\mathbb Q(r,t)\), the complete finite
\(\lambda=1\) weighted-H22 incidence on the common-center-kernel star
component is empty for every affine marking \((h_0,h_1,h_2,h_3)\).

This closes the intrinsic \(\lambda=1\) wall left by
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md`.
It does not close that supplement's other explicit residual intersections,
the full generic finite fibre, or the global Krenn--Gu conjecture.

## Exact row module

Use the same marked component rows, the finite projections \(D_{01}\) and
\(D_{23}\), and their 28 shared mixed coefficient rows.  Set \(\lambda=1\)
before forming the standard basis.  Over

\[
 K[h_0,h_1,h_2,h_3]
\]

the resulting row module is exactly

\[
 M=\langle e_1,e_2,e_3,e_4,e_6,e_7,e_8\rangle.
\]

The verifier checks both inclusions, not only rank or standard-basis size.
It also reduces the four diagonal rows and obtains

\[
 A_{01}\in M,\qquad A_{23}\in M,\qquad B_{01}\in M,
 \qquad B_{23}\notin M.
\]

Every shared mixed-kernel vector therefore has \(B_{01}=0\).  A genuine
weighted-H22 lift inherits the all-beta \(P_4\) support and requires both
\(B_{01}\) and \(B_{23}\) to be nonzero.  This contradiction closes the
entire \(\lambda=1\) all-marking slice.

## Updated finite boundary

Together with the dense-open supplement, whose \(\lambda=-1\) slice is also
closed, the remaining generic finite component-23 locus is contained in

\[
\begin{array}{ll}
\lambda=0, & h_2h_3H=0;\\
\lambda\notin\{0,1,-1\}, & F=0\ \text{and}\ h_2h_3H=0,
\end{array}
\]

with \(F,H\) defined in that supplement.  These remaining loci are
**UNKNOWN**.  No timeout, rational specialization, or finite-field
calculation is used in this proof.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py
uv run --with sympy python audit_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py
```
