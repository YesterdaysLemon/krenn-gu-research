# Component 21: complete \(U_0\)-projective blow-up over \(\kappa=\infty\)

## Status and scope

This note closes the full projective mode-zero Grassmann surface attached to
the normalized \(\kappa=\infty\) first-normal sheet of component 21, after
blowing up its unique zero-tensor point.  It is an exact transport theorem
from two pinned characteristic-zero packages:

* the complete finite-\((p,q)\) normalized \(\kappa=\infty\) obstruction; and
* the complete \(p=q=0\) projectivized normal obstruction, equivalently the
  complete vertical-\(U_0\) projective line at finite \(\kappa\), including
  \(\kappa=0\).

Every nonzero point of this projective surface or of the exceptional line is
empty for fixed-order marked \(H_{31}\) and homogeneous weighted \(H_{22}\),
including finite \(\ell\), \(\ell=\infty\), and both homogeneous weight
charts.

This is a theorem inside the displayed normalized component compactification.
It does not classify source-marking or extension-coordinate infinity,
additional ambient transformations, or arbitrary source/projective
degenerations.  The arbitrary-order local-to-global reduction remains open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.  No finite-field result
is used as proof.

## Homogeneous \(U_0\) Grassmann chart

Put

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad B=(0,0,1,1).
\]

The affine plane

\[
 U_0(p,q)=\langle A+pB,C+qB\rangle
\]

has Pluecker vector

\[
 A\wedge C+qA\wedge B+pB\wedge C.
\]

Its closure in \(\operatorname{Gr}(2,\langle A,C,B\rangle)\cong\mathbf P^2\)
is therefore the exact homogeneous map

\[
 [R:P:Q]\longmapsto
 R A\wedge C+Q A\wedge B+P B\wedge C.             \tag{1}
\]

There are no omitted mode-zero Grassmann points in (1).

On \(R\ne0\), put \(p=P/R\), \(q=Q/R\).  Away from \((p,q)=(0,0)\), this is
the directly certified finite-\((p,q)\) \(\kappa=\infty\) sheet.

On the projective line \(R=0\), equation (1) becomes

\[
 QA\wedge B+PB\wedge C=(QA-PC)\wedge B.           \tag{2}
\]

Thus every point at infinity is the vertical plane

\[
 U_0^\infty[P:Q]=\langle QA-PC,B\rangle.           \tag{3}
\]

Together with the \(\kappa=\infty\) mode-two replacement
\(U_2=\langle C,B\rangle\), this is exactly the certified vertical-\(U_0\)
sheet at \(\kappa=0\).  For \(Q\ne0\), its coordinate is
\(\alpha=P/Q\); the endpoint \(Q=0\) is the separately certified
\(\alpha=\infty\) chart.

## The unique base point and its blow-up

On the affine chart, the normalized \(\kappa=\infty\) pure tensor has exactly

\[
 T_{0111}=4p,\qquad T_{1111}=4q
\]

for finite \(\ell\), with both signs reversed at \(\ell=\infty\).  Hence its
only zero is

\[
 c=[R:P:Q]=[1:0:0].
\]

The two coefficients are regular parameters at \(c\), so one ordinary blow-up
has exceptional line \([P:Q]\).  The exact Pluecker calculation for its first
normal direction again gives

\[
 U_0^{\rm exc}[P:Q]=\langle QA-PC,B\rangle,        \tag{4}
\]

with \(U_2=\langle C,B\rangle\).  Thus the exceptional line (4) and the
projective boundary line (3) are two copies of the same already certified
vertical-\(U_0\), \(\kappa=0\) obstruction sheet.  They are disjoint in the
blow-up because the boundary line \(R=0\) does not contain \(c\).

The point \(c\) itself has zero pure restriction and is not a projective
\(P_5\) point.  Every nonconstant DVR/Puiseux arc through it has a first
nonzero pair \([P:Q]\) on (4).  No iterated mode-zero blow-up is needed for
the restriction tensor in this normalized chart.

## Exact cover

The blow-up is covered by three disjoint types of points:

1. \(R\ne0\) and \((P,Q)\ne(0,0)\): the direct normalized
   \(\kappa=\infty\) sheet, obstructed by eight exact unit ideals.
2. \(R=0\): the complete vertical-\(U_0\) line at \(\kappa=0\), obstructed by
   the pinned vertical and \(\alpha=\infty\) certificates.
3. The exceptional line above \(c\): the same complete vertical-\(U_0\) line,
   again obstructed by the pinned \(p=q=0\) normal package.

These three types exhaust the blow-up of \(\mathbf P^2\) at \(c\).  The two
dependency packages retain every finite marking and normalized extension
coordinate polynomially and include the full \(\ell\)- and homogeneous-weight
charts.  Therefore:

**The complete normalized \(U_0\)-projective blow-up over the component-21
\(\kappa=\infty\) first-normal sheet contains no fixed-order marked
\(H_{31}\) fibre and no homogeneous weighted \(H_{22}\) fibre.**

The theorem removes the earlier `p`/`q`-pole boundary from this specific
Grassmann compactification.  It does not remove the stated source, extension,
or arbitrary ambient/projective boundaries.

## Replay

Replay the two pinned packages first:

```powershell
uv run --with sympy python .\verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_kappa_infinity_first_normal_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py .\audit_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
uv run --with sympy python -m py_compile .\verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py .\audit_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
```

The primary verifies the homogeneous Pluecker surface, both vertical lines,
the unique tensor base point, and all dependency hashes.  The independent
audit uses a separate subset-DP permanent and replays the primary without
importing it.
