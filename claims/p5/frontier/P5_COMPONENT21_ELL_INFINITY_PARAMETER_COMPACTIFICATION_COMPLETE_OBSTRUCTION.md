# Component 21: complete normalized \(\ell=\infty\) parameter compactification

## Status and scope

This note proves that the complete normalized component-21 parameter
compactification over the genuine mode-three divisor \(\ell=\infty\) is empty
for fixed-order marked \(H_{31}\) and homogeneous weighted \(H_{22}\).  It
combines four new direct characteristic-zero unit ideals on the finite
\((p,q,\kappa)\) chart with two pinned exact projective-boundary packages.

The compactification used here is explicit: the mode-zero plane is closed to
\(\operatorname{Gr}(2,\langle A,C,B\rangle)\cong\mathbf P^2\), its unique
zero-tensor centre is blown up, and \(\kappa\) is completed by the normalized
\(t=1/\kappa\) first-normal chart.  Every intersection of those parameter
charts at \(\ell=\infty\) is included.

This remains a fixed-source normalized component theorem.  It does not cover
source-marking infinity, extension-coordinate infinity outside the displayed
Rees charts, arbitrary ambient transformations, or arbitrary source and
projective degenerations.  The arbitrary-order local-to-global reduction is
open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

All direct calculations are exact over \(\mathbb Q\).  Finite fields are not
used as proof.

## The direct finite-parameter divisor

Put

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1).
\]

At \(\ell=\infty\), use

\[
\begin{aligned}
 a&=(A+pB,A,C,D),\\
 b&=(C+qB,C,B+\kappa A,C).                       \tag{1}
\end{aligned}
\]

The only nonzero pure coefficients are

\[
 T_{0111}=-4p,\qquad T_{1111}=-4q.                \tag{2}
\]

Thus \((p,q)=(0,0)\) is the only zero of the pure restriction in this affine
chart, independently of finite \(\kappa\).

### Marked \(H_{31}\)

For distinguished vertices zero and one, the all-\(a\) binary diagonal is
identically zero, so Hall fails.

For distinguished vertices two and three, impose the fourteen mixed
extension equations, normalize the all-\(a\) diagonal, invert the all-\(b\)
diagonal, and adjoin all 32 entries of the mode-three one-marked obstruction
map.  In each case the reduced Groebner basis over \(\mathbb Q\) is \([1]\),
with

\[
 p,q,\kappa,h_0,h_1,h_2,h_3
\]

retained as polynomial variables.  Hence every finite-parameter intersection
on the nonzero locus of (2) is obstructed; no generic denominator is inverted.

### Weighted \(H_{22}\)

In both homogeneous weight charts, the all-\(a\) diagonal of the \(D_{01}\)
contraction vanishes identically.  Hall therefore forces \(D_{01}\) to be pure
and \(D_{23}\) to be binary.

Impose the fifteen unwanted \(D_{01}\) coefficients and normalize its
all-\(b\) coefficient.  Impose the fourteen mixed \(D_{23}\) equations,
invert both of its diagonals, and adjoin all 32 entries of its mode-three
obstruction map.  The reduced Groebner basis is \([1]\) in both the finite and
infinite homogeneous weight charts, again over the full polynomial parameter
ring.  These are the other two direct unit certificates.

## Projective parameter atlas

Write the complete mode-zero Grassmann plane as

\[
 [R:P:Q]\longmapsto
 R A\wedge C+Q A\wedge B+P B\wedge C.             \tag{3}
\]

Let \(c=[1:0:0]\), the unique zero of (2), and let

\[
 X=\operatorname{Bl}_c\mathbf P^2.
\]

The normalized \(\ell=\infty\) parameter atlas is obtained from
\(X\times\mathbf P^1_\kappa\) by using the certified first-normal replacement
at \(\kappa=\infty\).  Its points split into the following exhaustive cases.

### 1. Finite \(\kappa\), affine nonzero \((p,q)\)

This is exactly the direct sheet (1)--(2), closed by the four new unit ideals.

### 2. Finite \(\kappa\), mode-zero boundary or exceptional line

On \(R=0\), and likewise on the exceptional line above \(c\), the mode-zero
plane is

\[
 U_0=\langle QA-PC,B\rangle.                      \tag{4}
\]

For \(Q\ne0\), this is the certified vertical-\(U_0\) sheet with
\(\alpha=P/Q\); \(Q=0\) is its certified \(\alpha=\infty\) endpoint.  The
complete \(p=q=0\) normal package covers every finite \(\kappa\), including
all marking intersections and the \(\ell=\infty\) chart used here.

### 3. \(\kappa=\infty\), every point of \(X\)

The pinned \(\kappa=\infty\) \(U_0\)-projective blow-up theorem covers the
whole surface \(X\): its affine nonzero sheet, its projective boundary, and
its exceptional line over \(c\).  That theorem includes \(\ell=\infty\) and
both homogeneous weight charts explicitly.  It also treats joint DVR/Puiseux
arcs in which \(t=1/\kappa\) and \(p,q\) vanish at unequal orders.

These cases exhaust the normalized parameter compactification.  Case 1 is
the complement in the finite-\(\kappa\) chart of the boundary and exceptional
divisors in case 2; case 3 is the complete missing point of
\(\mathbf P^1_\kappa\), with all its intersections already included.  The
unblown point \(c\) has zero pure restriction and is not a projective
\(P_5\) point; every nonconstant arc through it lands on its exceptional line.

## Theorem

**The complete normalized \(\ell=\infty\) component-21 parameter
compactification described above contains no fixed-order marked \(H_{31}\)
fibre and no homogeneous weighted \(H_{22}\) fibre.**

This strengthens the former divisor-generic mode-three result to all
finite-parameter intersections, the full mode-zero projective boundary and
zero-point blow-up, the full \(\kappa=\infty\) divisor, and every intersection
among them inside this normalized atlas.  The excluded source, extension, and
arbitrary ambient/projective charts remain **UNKNOWN**.

## Replay

Replay the pinned boundary packages first:

```powershell
uv run --with sympy python .\verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py .\audit_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py
uv run --with sympy python -m py_compile .\verify_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py .\audit_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py
```

The primary reconstructs all four direct unit ideals and pins both boundary
packages.  The genuinely independent audit uses a subset-DP permanent,
reconstructs the four ideals without importing either primary, and replays the
new primary as a subprocess.
