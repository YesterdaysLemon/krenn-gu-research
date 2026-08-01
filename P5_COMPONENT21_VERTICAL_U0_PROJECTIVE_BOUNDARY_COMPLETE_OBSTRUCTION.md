# Component 21: complete normalized vertical-\(U_0\) projective-boundary obstruction

## Status and scope

This note proves, over characteristic zero, that the marked \(H_{31}\) and
weighted \(H_{22}\) incidences are empty on the **full projective boundary of
the normalized vertical mode-zero sheet of component 21**.  Both finite
\(\ell\) and \(\ell=\infty\) are included, as are every component and every
intersection of the saturated incidence schemes.

This is not a classification of arbitrary ambient, source, or projective
degenerations of component 21.  Such degenerations outside this normalized
component compactification remain **UNKNOWN**.  The arbitrary-order
local-to-global reduction also remains open, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

All computations below are exact computations over \(\mathbb Q\) and rational
function fields of characteristic zero.  No finite-field computation is used
as proof.

## Normalized sheet and its projective closure

Put

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1).
\]

The finite chart of the vertical mode-zero sheet is

\[
 \begin{aligned}
 U_0&=\langle A-\alpha C,B\rangle,&
 U_1&=\langle A,C\rangle,\\
 U_2&=\langle C,B+\kappa A\rangle,&
 U_3&=\langle A+\ell C,D\rangle.
 \end{aligned}
\]

An intrinsic pure basis is

\[
 (a_0,a_1,a_2,a_3)=(A-\alpha C,\ell A+C,C,D),\qquad
 (b_0,b_1,b_2,b_3)=(B,A,B+\kappa A,A+\ell C).
\]

Among its sixteen pure permanent coefficients, only
\(\operatorname{per}(b_0,b_1,b_2,b_3)=4\) is nonzero.  The point at infinity
has \(U_3=\langle C,D\rangle\), for which we use

\[
 (a_0,a_1,a_2,a_3)=(A-\alpha C,A,C,D),\qquad
 (b_0,b_1,b_2,b_3)=(B,C,B+\kappa A,C).
\]

Again only the all-\(b\) coefficient is nonzero, now equal to \(-4\).

The marking is

\[
 \widetilde b_i=b_i+h_i a_i \qquad (0\leq i\leq3).
\]

For marked \(H_{31}\), the distinguished vertices \(d=0,1\) are excluded
immediately: the all-\(a\) diagonal row is identically zero, so Hall's
condition cannot be met.  It remains to treat \(d=2,3\).

For weighted \(H_{22}\), Hall forces \(D_{01}\) to be the pure side and
\(D_{23}\) to be the binary side.  In the finite weight chart we use

\[
 D_{01}(z,e)=(\lambda z_0+z_1,z_2,z_3,e),\qquad
 D_{23}(z,e)=(z_0,z_1,\lambda z_2+z_3,e),
\]

and in the infinite chart the corresponding direct contractions
\((z_0,z_2,z_3,e)\) and \((z_0,z_1,z_2,e)\).

## Saturated global incidence and its ten finite-\(\ell\) components

For \(H_{31}\), let \(M_d\) be the \(14\times8\) mixed-coefficient matrix and
let \(d_a,d_b\) be its two diagonal rows.  We eliminate \(z\) and an inverse
variable from

\[
 M_dz=0,\qquad d_az=1,\qquad v(d_bz)=1.
\]

For \(H_{22}\), we set all non-all-\(b\) coefficients of the pure contraction
to zero, normalize its all-\(b\) coefficient to one, set the fourteen mixed
coefficients of the binary contraction to zero, and invert both of its
diagonal coefficients.  This is the same saturation written without ideal
quotients.

For both \(d=2,3\), and independently for both finite and infinite weight
charts of \(H_{22}\), exact elimination gives the same 13-generator ideal
\(J\subset\mathbb Q[\alpha,\kappa,\ell,h_0,h_1,h_2,h_3]\).  Its ten minimal
primes are exactly the following.  Put

\[
 E=2\alpha\ell+\ell^2+1.
\]

\[
\begin{array}{c|l}
1&\langle h_3,h_2,h_1,\kappa,\alpha+\ell\rangle\\
2&\langle h_3,h_2,h_1,\ell+1,\kappa\rangle\\
3&\langle h_3,h_2,h_1,\ell-1,\kappa\rangle\\
4&\langle \kappa\ell-h_2,\;Eh_1+\alpha+\ell,\;
2\alpha h_1h_2+\ell h_1h_2+\alpha\kappa+\kappa h_1+h_2,\;h_3,h_0\rangle\\
5&\langle h_3,h_0,\ell+1,\kappa+h_2\rangle\\
6&\langle h_3,h_0,\ell-1,\kappa-h_2\rangle\\
7&\langle(\ell-1)h_1+1,h_3,h_0,\alpha+1\rangle\\
8&\langle(\ell+1)h_1+1,h_3,h_0,\alpha-1\rangle\\
9&\langle(\alpha-1)h_1+1,h_3,h_0,\ell+1\rangle\\
10&\langle(\alpha+1)h_1+1,h_3,h_0,\ell-1\rangle.
\end{array}
\]

The source involution \(X_0\leftrightarrow X_1\) acts by

\[
 (\alpha,\ell,h_1,h_2)\longmapsto
 (-\alpha,-\ell,-h_1,-h_2)
\]

and fixes \(\kappa,h_0,h_3\).  It fixes primes 1 and 4 and pairs
\(2\leftrightarrow3\), \(5\leftrightarrow6\),
\(7\leftrightarrow8\), and \(9\leftrightarrow10\).  Thus the explicit
certificates below need only treat primes 1, 3, 4, 6, 7, and 10.

## Exact marked-\(H_{31}\) fibre certificates

Write an extension vector as \((x_0,x_1,x_2,x_3;y_0,y_1,y_2,y_3)\).
On each representative prime the verifier supplies an explicit basis for
\(\ker M_d\), checks it by exact multiplication, checks the generic rank of
\(M_d\), evaluates both diagonal rows, and factors a fixed \(4\times4\)
mode-3 minor.  The displayed factors show that the minor is nonzero whenever
both diagonal coefficients required by Hall are nonzero.

For prime 1, with \(h=(T,0,0,0)\), \(\kappa=0\), and
\(\alpha=-\ell\), a kernel basis for \(d=2\) is

\[
 e_0=(\ell^2-1,0,\ell,0;0,1,0,0),\qquad
 e_1=(0,0,0,1;1,0,1,0),
\]

with the sign of the fourth entry of \(e_1\) reversed for \(d=3\).  For
\(z=c_0e_0+c_1e_1\) and
\(Q_1=T c_0(\ell^2-1)-2c_1\), the two diagonal coefficients are
\(\pm2c_0(\ell^2-1)\) and \(-2Q_1\), while the rows \(0467\) mode-3 minor is
\(8c_0^2(\ell^2-1)Q_1\).

Prime 3 has \(\ell=1\), \(\kappa=0\), and \(h=(T,0,0,0)\).  The verifier
uses

\[
 e_0=(0,0,0,\pm1;1,0,1,0),\qquad
 e_1=(-1,-1,0,0;-T\alpha,0,0,1).
\]

If \(Q_3=-T\alpha c_1+Tc_1+2c_0\), then the diagonals are
\(\pm2c_1(\alpha-1)\), \(2Q_3\), and the rows \(0347\) minor is
\(-8c_1^2(\alpha-1)Q_3\).

On the dense prime 4, with

\[
 h=(0,-(\alpha+\ell)/E,\kappa\ell,0),
\]

the kernel basis is

\[
 e_0=(-\alpha\ell-1,0,\ell,0;0,1,0,0),\qquad
 e_1=(0,0,0,\pm1;1,0,1,0).
\]

For \(Q_4=\kappa(\ell^2-1)c_0-2c_1\), its diagonals are
\(\mp2Ec_0\) and \(-2Q_4\); the rows \(0467\) minor equals
\(\mp2c_0(d_az)(d_bz)\).

On prime 6, \(\ell=1\) and \(h=(0,T,\kappa,0)\).  The exact two-vector
kernel basis is printed in the primary verifier.  Here the diagonals reduce
to \(\pm2c_1(\alpha^2-1)\) and \(4c_0\).  Two minors are used:

\[
 \begin{aligned}
 \Delta_{0147}&=-32c_0c_1^2(2T+1)(\alpha-1)(\alpha+1)^2,\\
 \Delta_{0467}&=-16Tc_0c_1^2(\alpha-1)^2(\alpha+1).
 \end{aligned}
\]

They cover the possible zeros \(T=0\) and \(2T+1=0\) after the diagonal
conditions are imposed.

On prime 7, \(\alpha=-1\) and
\(h=(0,-1/(\ell-1),T,0)\).  If
\(Q_7=(T-\kappa)(\ell+1)c_0-2c_1\), the two diagonals are
\(\mp2c_0(\ell-1)^2\) and \(-2Q_7\), and the rows \(0467\) minor is
\(-8c_0^2(\ell-1)^2Q_7\).

On prime 10, \(\ell=1\) and
\(h=(0,-1/(\alpha+1),T,0)\).  If

\[
 Q_{10}=-T\alpha c_1+Tc_1+\alpha\kappa c_1+2c_0-\kappa c_1,
\]

the diagonals are \(\pm2c_1(\alpha+1)^2\) and \(2Q_{10}\), and the rows
\(0467\) minor is \(8c_1^2(\alpha+1)^2Q_{10}\).

The most important rank-drop collision, \((\alpha,\ell)=(-1,1)\), is checked
without division and including \(\kappa=0\).  There \(M_d\) has rank 5 and
the verifier gives a three-vector kernel basis.  Its diagonal coefficients
are \(\mp4c_2\) and \(4c_1\), and a fixed mode-3 minor is exactly
\(4c_2(d_az)(d_bz)\).  The direct specialized saturated ideals at the other
endpoint collisions are likewise accounted for by the global minimal-prime
decomposition; no denominator-localized argument is used to discard an
intersection.

Consequently every saturated marked-\(H_{31}\) point on the finite
\(\ell\)-chart has a nonzero mode-3 coefficient and is obstructed.

## Exact weighted-\(H_{22}\) fibre certificates

For each representative finite-\(\ell\) prime, the mixed equations of
\(D_{01}\) and \(D_{23}\) have rank 7 and the verifier displays their common
one-dimensional kernel.  It then evaluates

\[
 B_{01},\qquad A_{23},\qquad B_{23},\qquad
 \Delta_{0467}^{(3)}
\]

in both weight charts.  The fixed minor is always a nonzero scalar multiple
of the three required nonzero diagonal factors.  Representative kernel
vectors are

\[
\begin{array}{c|l}
1&(\ell^2-1,0,\ell,0;0,1,0,0)\\
4&(-\alpha\ell-1,0,\ell,0;0,1,0,0)\\
6&(-(\alpha+1)(\alpha T+T+1),-(\alpha+1)(2T+1),T(\alpha-1),0;
0,-2T(\alpha T+T+1),\kappa(\alpha+1)(2T+1),(\alpha+1)(2T+1))\\
7&(\ell-1,0,\ell,0;0,1,T-\ell\kappa,0)\\
10&(0,-\alpha-1,-1,0;0,0,\alpha T+\kappa,\alpha+1).
\end{array}
\]

For example, on the dense prime 4 in the finite weight chart,

\[
 \begin{aligned}
 B_{01}&=2C((\ell+1)\lambda+1-\ell),\\
 A_{23}&=2C(\lambda-1)E,\\
 B_{23}&=-2C\kappa(\ell^2-1)(\lambda+1),\\
 \Delta_{0467}^{(3)}&=-8C^3\kappa(\ell^2-1)(\lambda+1)^3E.
 \end{aligned}
\]

The other displayed vectors are checked in the same way, and the infinite
weight chart removes the corresponding powers of \(\lambda\pm1\).  Thus all
ten finite-\(\ell\) components, including their intersections, are obstructed
for weighted \(H_{22}\).

## The \(\ell=\infty\) divisor

For both distinguished vertices of \(H_{31}\), and for both weight charts of
\(H_{22}\), elimination at \(\ell=\infty\) gives

\[
 J_\infty=\langle h_3,h_0,\alpha+h_1,
                    \kappa(h_1^2-1)\rangle.
\]

Its three minimal primes are

\[
 \begin{aligned}
 &\langle h_3,h_1+1,h_0,\alpha+h_1\rangle,\\
 &\langle h_3,h_1-1,h_0,\alpha+h_1\rangle,\\
 &\langle h_3,h_0,\kappa,\alpha+h_1\rangle,
 \end{aligned}
\]

with \(h_2\) free.  On \(\kappa=0\), the marked-\(H_{31}\) kernel frame is

\[
 e_0=(\alpha,0,-1,0;0,1,0,0),\qquad
 e_1=(0,0,0,\pm1;1,0,1,0).
\]

For \(h=(0,-\alpha,T,0)\), the diagonals are \(\pm2c_0\) and
\(-2(Tc_0+2c_1)\), while the rows \(0147\) minor is
\(8c_0^2(Tc_0+2c_1)\).  The \(\alpha=1\) endpoint has the same formula with
\(T\) replaced by \(T+\kappa\); \(\alpha=-1\) follows by source symmetry.

For weighted \(H_{22}\), the \(\kappa=0\) kernel is the line spanned by
\((\alpha,0,-1,0;0,1,0,0)\).  In the finite weight chart the three diagonals
are \(2C(\lambda-1)\), \(-2C(\lambda-1)\), and
\(-2CT(\lambda+1)\), while the rows \(0147\) minor is
\(8C^3T(\lambda+1)^3\).  At \(\alpha=1\) the kernel is spanned by
\((-1,0,1,0;0,-1,\kappa,0)\), and the same calculation gives the factor
\(-8C^3(T-\kappa)(\lambda+1)^3\).  The infinite weight chart and the
\(\alpha=-1\) endpoint are checked separately by the verifier.

Therefore the entire \(\ell=\infty\) divisor is obstructed as well.

## Theorem

**The normalized vertical mode-zero projective compactification of component
21 contains no marked \(H_{31}\) fibre and no weighted \(H_{22}\) fibre.**

Equivalently, within this fixed component normalization, every saturated Hall
incidence point has a certified nonzero mode-3 coefficient.  This closes this
specific component-21 projective boundary, but it does not enlarge the claim
to arbitrary source or ambient degenerations.

## Replay

Run from the repository root:

```powershell
python .\verify_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py
python .\audit_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py
python -m ruff check .\verify_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py .\audit_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py
python -m py_compile .\verify_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py .\audit_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py
```

Both Python programs fail closed if Singular is unavailable.  The primary
verifier reconstructs all eight characteristic-zero eliminations and all
explicit kernel/minor certificates.  The independent audit uses a separate
subset-dynamic-programming permanent, independently reconstructs all eight
saturated elimination ideals and their minimal primes, and directly proves
that adjoining the full mode-3-zero condition gives the unit ideal in every
chart.  It does not import the primary verifier.
