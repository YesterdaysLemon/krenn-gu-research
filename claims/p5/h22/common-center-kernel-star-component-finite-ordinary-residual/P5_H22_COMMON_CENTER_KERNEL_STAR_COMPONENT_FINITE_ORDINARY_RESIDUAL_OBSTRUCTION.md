# Component 23 remaining ordinary finite weighted-H22 obstruction

## Status

**VERIFIED EMPTY, using the prior exact factor cover.**  Over
\(K=\mathbb Q(r,t)\), the component-23 finite weighted-H22 incidence is
empty on the entire remaining ordinary locus

\[
 \lambda\notin\{0,1,-1\},\qquad F=0,\qquad h_2\ne0,
 \qquad (h_3=0\ \text{or}\ H=0).
\]

Together with the earlier dense-open and \(h_2=0\) results and the complete
\(\lambda=0,1,-1\) slices, this closes the generic finite all-marking fibre
of component 23.  The prior infinity theorem therefore also closes generic
weighted H22 on this component.  Special or projective component fibres,
the arbitrary-order local-to-global reduction, and the global Krenn--Gu
conjecture remain **UNRESOLVED**.

The polynomials \(F,H\) are exactly those in
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md`.

## The h3 = 0 branch

The coefficient of \(h_1\) in \(F\) is

\[
 -r(\lambda-1)(r-t)(rt-1).
\]

It is a unit on the ordinary-weight locus over \(K\).  Set \(h_3=0\) and
solve \(F=0\) exactly for \(h_1\).  After this substitution, adjoin the
inverse equation

\[
 u h_2\lambda(\lambda-1)(\lambda+1)-1=0.
\]

The 28 shared mixed rows, together with this inverse relation times each
basis vector, generate the full free module

\[
 K[h_0,h_2,\lambda,u]^8.
\]

Both module inclusions are checked.  Hence the shared mixed kernel is zero
everywhere on \(F=h_3=0\) with \(h_2\ne0\) and ordinary weight.

## The H = 0 branch

Write

\[
 H=2Lh_3+(r+1)C,
\]

where

\[
\begin{aligned}
L={}&\lambda r^2-\lambda rt-\lambda r+2\lambda t^2+\lambda t-2\lambda
     +2r^2-rt-r+t^2+t-2,\\
C={}&\lambda r-\lambda t-r-t+2.
\end{aligned}
\]

The resultant in \(\lambda\) is

\[
\operatorname{Res}_\lambda(L,C)=
-3r^3+3r^2t+4r^2-3rt^2-4rt+2r-t^3+4t^2+2t-4,
\]

a nonzero element of \(K\).  Thus \(L\) and \(C\) are coprime in
\(K[\lambda]\), and \(L\) cannot vanish at a point of \(H=0\).

For the 8-by-8 mixed minor on rows

\[
 (0,1,2,3,7,8,9,11),
\]

exact standard-basis reduction modulo \(\langle F,H\rangle\), with
\(h_1,h_3\) as polynomial variables, gives

\[
 -\frac{1024rt(r+1)(rt-1)^5}{(r-t)^2}
 \frac{h_2\lambda(\lambda-1)^2(\lambda+1)^4C}{L}.
\]

All omitted prefactors are units on the stated ordinary generic-component
locus.  Therefore the mixed matrix has rank eight wherever \(C\ne0\).  If
instead \(C=0\), the equations \(H=0\) and \(L\ne0\) force \(h_3=0\), which
is the already-closed branch above.  This exhausts the \(H=0\) residual.

## Boundary and failed routes

This theorem is over the generic component field \(K=\mathbb Q(r,t)\).  It
does not cover special or projective component fibres.  A direct localized
four-variable standard-basis calculation on the full \(H=0\) branch and a
raw generic SymPy determinant factorization exceeded their caps; neither is
used as evidence.  The proof instead uses the displayed two-variable normal
form and the exact \(h_3=0\) module.  No finite-field computation is used.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-all-marking-dense-open-supplement/verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-ordinary-f-h2-zero/verify_p5_h22_common_center_kernel_star_component_finite_ordinary_F_h2_zero_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-ordinary-residual/verify_p5_h22_common_center_kernel_star_component_finite_ordinary_residual_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-finite-ordinary-residual/audit_p5_h22_common_center_kernel_star_component_finite_ordinary_residual_obstruction.py
```
