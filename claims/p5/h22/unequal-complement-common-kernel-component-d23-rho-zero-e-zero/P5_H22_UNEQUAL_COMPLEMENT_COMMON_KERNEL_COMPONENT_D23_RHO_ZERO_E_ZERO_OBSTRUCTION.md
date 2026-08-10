# Component 22 finite-D23 rho-zero, E-zero weighted-H22 obstruction

## Status

**VERIFIED EMPTY.**  Work over \(K=\mathbb Q(A,R,D)\).  The component-22
finite-\(D_{23}\) weighted-H22 incidence is empty on the residual chart

\[
 \rho=0,\qquad E=0,\qquad h_1h_2\ne0
\]

left by
`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_RHO_ZERO_H1_NONZERO_SUPPLEMENT.md`.
Together with that supplement's \(h_2=0\) branch and cofactor open, this
closes \(\rho=0,h_1\ne0\).  The earlier pair-orbit theorem closes
\(\rho=0,h_1=0\), so the complete generic-component \(\rho=0\) slice is now
empty.  Other finite-\(D_{23}\) residual charts, special/projective component
fibres, and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Solving E = 0

Recall

\[
 E=(AD-A+RD)h_0
 +(A^2D+3A^2+ARD+2AR)h_1+(2A+R).
\]

Its \(h_0\)-coefficient is a unit in \(K\), so the verifier substitutes

\[
 h_0=-\frac{(A^2D+3A^2+ARD+2AR)h_1+(2A+R)}{AD-A+RD}.
\]

No rational specialization is used in the proof.

## Seven-minor rank certificate

At \(\rho=0\), the prior exact kernel is

\[
k=(D-1,2,2,0,(D-1)h_0+2,2h_1,2h_2,-(D-1))^T.
\]

The verifier rechecks \(Mk=0\) after the \(E=0\) substitution.  Hence the
14-by-8 mixed matrix \(M\) has rank at most seven.  Delete its last column
and use columns

\[
(0,1,2,3,4,5,6).
\]

For the following seven row sets,

\[
\begin{gathered}
(0,1,2,3,4,5,7),\quad (0,1,2,3,4,6,7),\\
(0,1,2,3,5,6,7),\quad (0,1,2,4,5,6,7),\\
(0,1,2,3,4,7,8),\quad (0,1,2,3,4,7,10),\\
(0,1,2,3,4,7,11),
\end{gathered}
\]

let \(d_0,\ldots,d_6\) be the corresponding 7-by-7 determinants.  Exact
standard-basis reduction over \(K\) gives

\[
\langle d_0,\ldots,d_6,\ z h_1h_2-1\rangle
=\langle1\rangle
\quad\text{in }K[h_1,h_2,h_3,z].
\]

Every matrix row is cleared only by one common row multiplier, a unit in
\(K\).  Thus at least one selected minor is nonzero everywhere on
\(h_1h_2\ne0\), and \(\operatorname{rank}M=7\).  Its kernel is exactly the
line \(Kk\).

## Diagonal obstruction

Direct substitution of \(x=\tau k\) gives

\[
 A(\tau k)=0,\qquad B(\tau k)=2(D+1)\tau.
\]

A genuine binary weighted-H22 extension requires the inherited \(A\)
diagonal to be nonzero.  The identity \(A=0\) on the unique mixed-kernel
line therefore closes the whole chart.

## Boundary and failed route

This is a generic-component statement over \(K=\mathbb Q(A,R,D)\); parameter
divisors where the displayed normal form degenerates belong to the still-open
special/projective analysis.  A direct four-variable localized row-module
membership computation exceeded 120 seconds and is not evidence.  The proof
uses only the smaller seven-minor unit ideal above.  No finite-field
calculation is used.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-rho-zero-h1-nonzero-supplement/verify_p5_h22_unequal_complement_common_kernel_component_d23_rho_zero_h1_nonzero_supplement.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-rho-zero-e-zero/verify_p5_h22_unequal_complement_common_kernel_component_d23_rho_zero_E_zero_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-rho-zero-e-zero/audit_p5_h22_unequal_complement_common_kernel_component_d23_rho_zero_E_zero_obstruction.py
```
