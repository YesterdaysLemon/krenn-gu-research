# Component 22 finite-D23 weighted-H22: the rho-zero, h1-nonzero supplement

## Status

**VERIFIED PARTIAL SUPPLEMENT.**  Work throughout over
\(K=\mathbb Q(A,R,D)\).  On the component-22 finite-\(D_{23}\) weighted-H22
model, the subchart

\[
 \rho=0,\qquad h_1\ne0
\]

has no bad binary extension away from one explicit residual hypersurface.
The branch \(h_2=0\) is closed exactly.  The surviving branch displayed
below is **UNKNOWN**.  This does not close the generic weighted-H22 fibre,
component 22, or the global Krenn--Gu conjecture.

## Exact kernel on rho = 0

Let \(M\) be the 14-by-8 coefficient matrix of the mixed equations.  Direct
symbolic multiplication gives

\[
 M\big|_{\rho=0}\,k=0
\]

for

\[
 k=\bigl(D-1,\ 2,\ 2,\ 0,\ (D-1)h_0+2,\ 2h_1,\ 2h_2,\ -(D-1)\bigr)^T.
\]

The two endpoint coefficients on the kernel line \(x=tk\) are

\[
 A(tk)=0,\qquad B(tk)=2(D+1)t.
\]

Consequently, wherever \(M\) has rank seven, its kernel is exactly the line
\(Kk\), and the normalization \(A=1\) is impossible.

## A small selected-cofactor cover

Take rows

\[
 (0,1,3,4,5,7,9)
\]

of \(M|_{\rho=0}\), and columns

\[
 (1,2,3,4,5,6,7),
\]

so the \(x_0\) column is deleted.  Singular verifies that this 7-by-7
determinant is associated over \(K\) to

\[
 h_2E,
\]

where

\[
 E=(AD-A+RD)h_0
   +(A^2D+3A^2+ARD+2AR)h_1
   +(2A+R).
\]

Thus \(h_2E\ne0\) forces rank seven and is impossible by the kernel
calculation.

## The h2 = 0 branch

On

\[
 \rho=0,\qquad h_2=0,\qquad h_1\ne0,
\]

the exact ideal consisting of all mixed equations, \(A-1\), the inverse
equation for \(B\ne0\), the three fixed one-marked 4-by-4 minors, and the
inverse equation for \(h_1\ne0\), is the unit ideal over \(K\).  Hence this
whole branch is closed.

Combining the cofactor cover with this unit ideal leaves only

\[
 \boxed{\rho=0,\quad E=0,\quad h_1h_2\ne0}
\]

in the present subchart.

## Honest boundary

The boxed residual is **UNKNOWN**.  Two attempted exact eliminations of it,
one saturated by \(h_1\) and one by \(h_1h_2\), each exceeded a two-minute
bound.  Those timeouts are not theorem evidence.  No rational specialization
and no finite-field computation is used in the proof above.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_rho_zero_h1_nonzero_supplement.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_rho_zero_h1_nonzero_supplement.py
```
