# Component 21: complete displayed normalized parameter compactification

## Status and scope

This note proves an exact characteristic-zero theorem for the complete
displayed normalized parameter compactification of component 21.  Every point
of that compactification is empty for fixed-order marked \(H_{31}\) and
homogeneous weighted \(H_{22}\).

The result combines four new direct unit ideals over the full finite
\((p,q,\kappa,\ell)\) polynomial ring with three pinned boundary packages:

* the complete \(p=q=0\) mode-zero blow-up;
* the complete \(\kappa=\infty\), mode-zero-projective blow-up; and
* the complete \(\ell=\infty\) parameter compactification.

The parameter compactification is the explicit one constructed by those
charts.  It starts from the mode-zero Grassmann plane \(\mathbf P^2\), blows
up its unique zero-tensor point, completes \(\kappa\) and \(\ell\) to
projective lines, and uses the certified Rees replacements on the boundary.
The proof below shows that these charts also exhaust every simultaneous
intersection among the three parameter boundaries.

This does **not** compactify the marking or extension variables.  Markings and
normalized extension coordinates remain affine variables in each Rees chart.
Their poles, non-diagonal source limits, arbitrary ambient transformations,
and arbitrary source/projective degenerations remain **UNKNOWN**.  The
arbitrary-order local-to-global reduction remains open.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

No finite-field computation is used as proof.

## The complete finite parameter sheet

Put

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1).
\]

For finite \(p,q,\kappa,\ell\), use the regular bases

\[
\begin{aligned}
 a&=(A+pB,\ell A+C,C,D),\\
 b&=(C+qB,A,B+\kappa A,A+\ell C).                \tag{1}
\end{aligned}
\]

The only nonzero pure coefficients are

\[
 T_{0111}=4p,\qquad T_{1111}=4q.                  \tag{2}
\]

Thus \((p,q)=(0,0)\) is the unique zero-tensor locus on the finite parameter
sheet.

### Global marked-\(H_{31}\) ideals

For distinguished vertices zero and one, the all-\(a\) binary diagonal is
identically zero, so Hall fails for every parameter value.

For distinguished vertices two and three, impose the fourteen mixed
extension equations, normalize the all-\(a\) diagonal, invert the all-\(b\)
diagonal, and adjoin all 32 entries of the mode-three one-marked obstruction
map.  Exact reduced Groebner calculation gives \([1]\) for each distinguished
vertex over

\[
 \mathbb Q[p,q,\kappa,\ell,h_0,h_1,h_2,h_3,z_0,\ldots,z_7,v].
\]

No component parameter or marking denominator is inverted.  These are global
polynomial unit certificates, not generic function-field identities.

### Global weighted-\(H_{22}\) ideals

For both homogeneous weight charts, the all-\(a\) diagonal of the \(D_{01}\)
contraction vanishes identically.  Hall forces \(D_{01}\) to be pure and
\(D_{23}\) to be binary.

Impose the fifteen unwanted \(D_{01}\) coefficients and normalize its
all-\(b\) coefficient.  Impose the fourteen mixed \(D_{23}\) equations,
invert both \(D_{23}\) diagonals, and adjoin all 32 entries of its mode-three
obstruction map.  The reduced Groebner basis is \([1]\) in the finite weight
chart and again \([1]\) at homogeneous weight infinity.  All
\(p,q,\kappa,\ell,h_i\), and the finite weight coordinate remain polynomial
variables.

These four unit ideals close every nonzero point of (2), including all finite
parameter intersections that formerly required separate divisor-generic or
sign-divisor arguments.

## The normalized parameter space

The mode-zero Grassmann closure is

\[
 [R:P:Q]\longmapsto
 R A\wedge C+Q A\wedge B+P B\wedge C.             \tag{3}
\]

Let \(c=[1:0:0]\), the unique zero in (2), and put

\[
 X=\operatorname{Bl}_c\mathbf P^2.
\]

The displayed normalized component compactification has parameter base

\[
 X\times\mathbf P^1_\kappa\times\mathbf P^1_\ell, \tag{4}
\]

with the boundary points interpreted by their certified first-normal Rees
replacements.  Formula (4) describes the parameter strata, not a claim that
marking or extension coordinates have also been made proper.

## Exhaustion of simultaneous parameter limits

Every point of (4) lies in exactly one of the following four routing cases.

### A. Finite \(\ell\), finite \(\kappa\), affine nonzero mode zero

Here \(R\ne0\) and \((P,Q)\ne(0,0)\).  Put \(p=P/R\), \(q=Q/R\).  The four
new global unit ideals apply directly.

### B. Finite \(\ell\), finite \(\kappa\), mode-zero boundary or exceptional line

On \(R=0\), and on the exceptional line over \(c\), the exact mode-zero
replacement is

\[
 U_0=\langle QA-PC,B\rangle.                      \tag{5}
\]

For \(Q\ne0\), this is the pinned vertical-\(U_0\) sheet with
\(\alpha=P/Q\); \(Q=0\) is its separately certified
\(\alpha=\infty\) endpoint.  The \(p=q=0\) normal package includes all finite
\(\kappa\), every finite \(\ell\), and every finite marking intersection.

### C. Finite \(\ell\), \(\kappa=\infty\), every mode-zero point

The pinned \(\kappa=\infty\) theorem covers all of \(X\): the affine nonzero
sheet, the line \(R=0\), and the exceptional line above \(c\).  Its direct
normal chart uses \(t=1/\kappa\) and

\[
 U_2=\langle C,A+tB\rangle
 \rightsquigarrow \langle C,B\rangle.
\]

It explicitly includes joint DVR/Puiseux arcs where \(t,p,q\) vanish at
different orders.  When \(p,q\) also vanish, their first pair \([P:Q]\)
again gives (5), now on the \(\kappa=0\) vertical replacement sheet.  Hence no
relative valuation among these three parameters creates another point of
this normalized atlas.

### D. \(\ell=\infty\), every \(\kappa\) and every mode-zero point

The pinned \(\ell=\infty\) compactification theorem covers the whole
\(X\times\mathbf P^1_\kappa\) boundary.  It contains its own four direct
finite-parameter unit ideals, the finite-\(\kappa\) vertical boundary and
exceptional line, the complete \(\kappa=\infty\) surface, and all
intersections among them.  Thus simultaneous \(\ell=\infty\),
\(\kappa=\infty\), and mode-zero projective limits are already included.

Cases A--D exhaust (4): first choose the finite or infinite \(\ell\)-chart;
on finite \(\ell\), choose finite or infinite \(\kappa\); on the remaining
finite pair, choose the affine nonzero or boundary/exceptional mode-zero
chart.  The unblown centre \(c\) has zero pure restriction and is not a
projective \(P_5\) point.  Every nonconstant arc through it has a first
direction on its exceptional line, including unequal-valuation Puiseux arcs.

## Theorem

**The complete displayed normalized component-21 parameter compactification
contains no fixed-order marked \(H_{31}\) fibre and no homogeneous weighted
\(H_{22}\) fibre.**

This closes all finite and projective component-parameter fibres in the
explicit Grassmann/Rees atlas (4).  It is not promoted to the omitted marking,
extension, source, or ambient compactifications, and it does not prove the
arbitrary-order local-to-global reduction.

## Replay

First replay the three pinned boundary packages:

```powershell
uv run --with sympy python .\verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py
uv run --with sympy python .\verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py
uv run --with sympy python .\verify_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_ell_infinity_parameter_compactification_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py .\audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy python -m py_compile .\verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py .\audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
```

The primary constructs the four global unit ideals and pins every boundary
dependency.  The no-import audit independently rebuilds the permanent by
subset dynamic programming, reconstructs all four unit ideals, verifies the
same dependency hashes, and replays the primary as a subprocess.
