# Component 21: complete normalized \(\kappa=\infty\) first-normal obstruction

## Status and scope

This note proves an exact characteristic-zero obstruction on the complete
normalized first/projective \(\kappa=\infty\) sheet of component 21, in the
displayed fixed-source Grassmann chart.  Every finite \((p,q)\ne(0,0)\), every
finite \(\ell\), the divisor \(\ell=\infty\), both relevant marked
\(H_{31}\) deletions, and both homogeneous weighted-\(H_{22}\) charts are
included.  Eight direct Groebner unit ideals prove that no such fibre lifts.

If \(p,q\) also vanish along the arc, the first nonzero joint direction is
identified exactly with the already certified vertical-\(U_0\) sheet at
\(\kappa=0\), including its \(\alpha=\infty\) endpoint.  This gives a complete
finite-\((p,q)\) DVR/Puiseux cover of the normalized \(\kappa=\infty\) first
normal direction.

The result is not a theorem about poles of \(p,q\), source-marking infinity,
arbitrary extension valuations outside the displayed Rees chart, iterated
normal cones after a zero restriction, or arbitrary ambient/source/projective
degenerations.  The arbitrary-order local-to-global reduction remains open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

All computations are exact over \(\mathbb Q\).  No finite-field calculation
is used as proof.

## Regular \(t=1/\kappa\) chart

Put

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1).
\]

For \(t=1/\kappa\), replace the singular mode-two basis
\((C,B+\kappa A)\) by the regular basis

\[
 (a_2,b_2^{\rm reg})=(C,A+tB).
\]

For finite \(\ell\), use

\[
\begin{aligned}
 (a_0,b_0)&=(A+pB,C+qB),\\
 (a_1,b_1)&=(\ell A+C,A),\\
 (a_2,b_2^{\rm reg})&=(C,A+tB),\\
 (a_3,b_3)&=(D,A+\ell C).
\end{aligned}
\]

Direct permanent expansion gives exactly

\[
 T_{0111}=4pt,\qquad T_{1111}=4qt,                 \tag{1}
\]

with the other fourteen pure coefficients zero.  At \(\ell=\infty\), use
\((a_1,b_1)=(A,C)\), \((a_3,b_3)=(D,C)\); the two coefficients in (1) become
\(-4pt,-4qt\).

The mode-two Pluecker vector is

\[
 C\wedge(A+tB)=C\wedge A+tC\wedge B.             \tag{2}
\]

Thus its unique nonzero projectivized normal direction is represented by
\(C\wedge B\), or by the replacement plane

\[
 U_2^{\rm exc}=\langle C,B\rangle.                \tag{3}
\]

After division by \(t\), (1) is exactly the pure tensor of the replacement
bases

\[
\begin{aligned}
 a&=(A+pB,\ell A+C,C,D),\\
 b&=(C+qB,A,B,A+\ell C),                          \tag{4}
\end{aligned}
\]

with the analogous \(\ell=\infty\) basis.  This is the \(\kappa=0\)
component-21 tensor, but the obstruction below is recomputed directly on the
whole replacement sheet; it is not inferred from equality of pure support.

## Marking and extension chart

The intrinsic finite-\(\kappa\) marked mode-two row is

\[
 B+\kappa A+h_2C.
\]

Multiplication by \(t\) gives

\[
 A+t(B+h_2C).
\]

Hence every finite intrinsic marking \(h_2\) has the exact normal row
\(B+h_2C\) used in (4).  If its marked extension coordinate is \(y_2\), row
scaling sends it to \(ty_2\), whose normal coordinate is again \(y_2\).
The new incidence calculations retain all eight normalized extension
coordinates and all four finite markings as polynomial variables.  Therefore
they cover the full affine Rees chart in which those normalized coordinates
are finite.

A marking or extension coordinate with an additional pole can select a
different source/projective initial form.  No claim about those omitted
source charts is made here.  In particular, the row calculation above defines
the normalized chart; equality of pure tensors alone is not being used to
assert an exhaustive statement about arbitrary extension arcs.

## Direct marked-\(H_{31}\) unit certificates

For distinguished vertices zero and one, the all-\(a\) diagonal of the
binary extension is identically zero, so Hall fails immediately.

For each of distinguished vertices two and three, form the fourteen mixed
extension equations.  Normalize the all-\(a\) diagonal to one, invert the
all-\(b\) diagonal, and adjoin all 32 entries of the mode-three one-marked
obstruction map.  A reduced Groebner basis over \(\mathbb Q\) is \([1]\) for
both distinguished vertices, with

\[
 p,q,\ell,h_0,h_1,h_2,h_3
\]

retained as polynomial variables.  Repeating the calculation directly in the
\(\ell=\infty\) basis again gives \([1]\) for both vertices.  These four unit
ideals include all parameter intersections; no generic denominator is
inverted.

## Direct weighted-\(H_{22}\) unit certificates

For both homogeneous weight charts, the all-\(a\) diagonal of the \(D_{01}\)
contraction is identically zero.  Thus Hall forces \(D_{01}\) to be pure and
\(D_{23}\) to be binary.

Impose the fifteen unwanted \(D_{01}\) coefficients, normalize its all-\(b\)
coefficient, impose the fourteen mixed \(D_{23}\) equations, and invert both
\(D_{23}\) diagonals.  After adjoining all 32 entries of the mode-three
obstruction map, the reduced Groebner basis is \([1]\) in both the finite and
infinite weight charts.  The same two direct calculations at
\(\ell=\infty\) are also unit ideals.  All \(p,q,h_i\), finite \(\ell\), and
the finite weight parameter remain polynomial variables.

Together with the marked calculation, this gives eight direct unit ideals on
the normalized \(\kappa=\infty\) sheet.

## DVR and Puiseux valuation cover in \((t,p,q)\)

Let \(t,p,q\) lie in a characteristic-zero DVR or a finite Puiseux extension,
with \(v(t)>0\) and with \(p,q\) regular.

If \(\min(v(p),v(q))=0\), the leading restriction in (1) is a nonzero point of
the replacement sheet (4), and the eight direct unit ideals apply.

Now suppose \(r=\min(v(p),v(q))>0\).  Write the leading pair after division by
the common order as \((P,Q)\ne(0,0)\).  The mode-zero Pluecker expansion is

\[
 (A+pB)\wedge(C+qB)
 =A\wedge C+qA\wedge B+pB\wedge C,
\]

so the simultaneous normal replacement is

\[
 U_0^{\rm exc}=\langle QA-PC,B\rangle,\qquad
 U_2^{\rm exc}=\langle C,B\rangle.                \tag{5}
\]

For \(Q\ne0\), (5) is exactly the certified vertical-\(U_0\) sheet with
\(\alpha=P/Q\) and \(\kappa=0\).  For \(Q=0\), it is its separately certified
\(\alpha=\infty\) endpoint.  Unequal valuations of \(p,q\) give
\(\alpha=0\) or \(\alpha=\infty\), so no additional first-normal point is
missing.  The pure replacement basis in (5) has only \(T_{1111}=4\) for
finite \(\ell\), and only \(T_{1111}=-4\) at \(\ell=\infty\).

If \(p=q=0\) identically, (1) is identically zero and supplies no projective
\(P_5\) restriction.  Poles of \(p\) or \(q\) leave the regular mode-zero
Grassmann chart and remain outside this theorem.

Therefore every nonzero finite-\((p,q)\) first-normal tensor direction at
\(\kappa=\infty\) lands either on the directly obstructed sheet (4) or on the
already obstructed double-normal sheet (5).

## Theorem

**The complete normalized finite-\((p,q)\) first/projective
\(\kappa=\infty\) atlas of component 21 contains no fixed-order marked
\(H_{31}\) fibre and no homogeneous weighted \(H_{22}\) fibre.**

This includes the full \(\ell\)-compactification, both homogeneous weight
charts, all finite marking intersections on the normalized replacement sheet,
and all equal- or unequal-valuation \((p,q)\) directions described above.  It
does not enlarge the claim to the omitted source, extension, ambient, or
Grassmann charts.

## Replay

First replay the pinned double-normal dependency:

```powershell
uv run --with sympy python .\verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_kappa_infinity_first_normal_complete_obstruction.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py .\audit_p5_component21_kappa_infinity_first_normal_complete_obstruction.py
uv run --with sympy python -m py_compile .\verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py .\audit_p5_component21_kappa_infinity_first_normal_complete_obstruction.py
```

The primary reconstructs all eight endpoint unit ideals.  The no-import audit
uses a separate subset-dynamic-programming permanent, reconstructs the same
eight ideals independently, and replays the primary as a subprocess.  Both
programs fail closed if the theorem or the pinned double-normal package has
changed.
