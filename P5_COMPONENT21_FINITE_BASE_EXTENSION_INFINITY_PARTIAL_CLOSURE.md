# Component 21: finite-base extension-infinity partial closure

## Status and scope

This note isolates the genuinely projective part of the eight extension
coordinates over the finite, nonzero component-21 parameter sheet.  The
calculation is exact over `Q`.  It proves two bounded statements.

1. For marked `H31`, every extension-pole arc is empty away from two explicit
   component curves.  On either curve, every leading extension direction
   outside one displayed kernel line is still empty.
2. For homogeneous weighted `H22` at weight infinity, every extension-pole
   arc over the whole finite nonzero component sheet is empty.

The two `H31` kernel lines and finite-weight `H22` common-kernel directions
remain **UNKNOWN**, as do their intersections with marking poles, the zero
base `p=q=0`, component-parameter infinity, and arbitrary source or ambient
degenerations.  Thus this is a partial extension compactification, not a
properness theorem.  The arbitrary-order local-to-global reduction is open,
and the global Krenn--Gu conjecture remains **UNRESOLVED**.

No finite-field computation is used as proof.

## The extension coefficient maps

Use

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1)
\]

and the finite component bases

\[
\begin{aligned}
 a&=(A+pB,\ell A+C,C,D),\\
 b&=(C+qB,A,B+\kappa A,A+\ell C).
\end{aligned}                                      \tag{1}
\]

Finite markings replace `b_i` by `b_i+h_i a_i`.  Let

\[
 z=(z_{a0},\ldots,z_{a3},z_{b0},\ldots,z_{b3})
\]

be the fifth-coordinate extensions.  Every deleted-coordinate `H31`
coefficient and every `H22` contraction coefficient is linear in `z`.
For distinguished coordinate `d`, write `M_d` for the resulting `16 x 8`
`H31` coefficient matrix.  At homogeneous weight infinity, write
`M_infinity` for the `32 x 8` matrix obtained by stacking the `D01` and
`D23` coefficient maps.

Marking changes act by invertible triangular transformations on the binary
coefficient coordinates and on the extension columns.  Hence all ranks and
Fitting loci below may be computed at `h_i=0` without losing any finite
marking.

## Exact `H31` Fitting cover

The distinguished-zero and distinguished-one orientations remain
Hall-deficient for every extension direction.  For each of `d=2,3`, nine
explicit `8 x 8` minors have the same zero locus on the nonzero sheet
`(p,q)!=(0,0)`.  In the chart `p!=0`, exact Groebner elimination gives

\[
 \kappa=0,\qquad \ell^2=1,\qquad q=\ell p.       \tag{2}
\]

The `q!=0` chart gives the same locus.  Conversely, direct substitution of
(2) kills all nine minors.  Thus these minors certify injectivity away from
the two curves

\[
 E_\epsilon:\quad
 \kappa=0,\quad \ell=\epsilon,\quad q=\epsilon p,
 \quad p\ne0,\qquad \epsilon\in\{+1,-1\}.       \tag{3}
\]

On `E_epsilon`, both `M_2` and `M_3` have rank exactly seven.  In the
unmarked coordinates a generator of their one-dimensional kernels is

\[
\begin{array}{c|rrrrrrrr}
 &z_{a0}&z_{a1}&z_{a2}&z_{a3}&z_{b0}&z_{b1}&z_{b2}&z_{b3}\\ \hline
 d=2&-1/2&-\epsilon&0&-1/(2p)&\epsilon/2&0&-1/(2p)&1\\
 d=3&-1/2&-\epsilon&0&+1/(2p)&\epsilon/2&0&-1/(2p)&1.
\end{array}                                      \tag{4}
\]

A fixed `7 x 7` minor is `+/-256 p^3`, so (4) is the complete kernel, not
merely a found relation.

## Exact weight-infinity `H22` cover

Ten explicit `8 x 8` minors of `M_infinity` have unit ideal after adjoining
`up-1`; the same ten have unit ideal after adjoining `uq-1`.  Consequently

\[
 \operatorname{rank} M_\infty=8
 \quad\text{whenever}\quad (p,q)\ne(0,0),        \tag{5}
\]

with no restriction on `kappa` or `ell`.  This includes the two curves (3).

The corresponding assertion is deliberately not made for the finite weight
chart.  Its stacked extension map already has rank seven at the exact
rational point

\[
 (p,q,\kappa,\ell,\lambda)=(2,3,5,7,1).
\]

This is a characteristic-zero kernel witness, not a counterexample: its
coupled first normal has not been classified.

## Valuative consequence

Let an exact characteristic-zero DVR arc, or an arc after a finite Puiseux
extension, tend to a finite component and finite marking point.  Suppose at
least one extension coordinate has a pole.  After extracting its largest
common pole, write the nonzero leading direction as `Z`.

If the relevant coefficient map at the centre is injective, its leading
ambient tensor is exactly `M Z` and is nonzero.  The global component-21 unit
ideals from the pinned normalized-compactification package then apply to this
homogeneous leading system: they exclude every fixed-order marked `H31`
target and every weight-infinity `H22` target.  If the map is not injective,
the same argument still excludes every `Z` outside its kernel.

It follows that:

* all marked-`H31` extension-pole arcs over the finite nonzero sheet are
  empty except possibly arcs centred on (3) whose leading direction is the
  corresponding line (4); and
* all homogeneous weighted-`H22` extension-pole arcs at weight infinity over
  the finite nonzero sheet are empty.

At a kernel direction the first nonzero tensor may mix a subordinate
extension term with a component or marking derivative.  This coupled normal
is precisely the part not promoted here.

## Replay

Replay the pinned finite component package first:

```powershell
uv run --with sympy python .\verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_finite_base_extension_infinity_partial_closure.py
uv run --with sympy python .\audit_p5_component21_finite_base_extension_infinity_partial_closure.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_finite_base_extension_infinity_partial_closure.py .\audit_p5_component21_finite_base_extension_infinity_partial_closure.py
uv run --with sympy python -m py_compile .\verify_p5_component21_finite_base_extension_infinity_partial_closure.py .\audit_p5_component21_finite_base_extension_infinity_partial_closure.py
```

The primary reconstructs the coefficient maps, the two Fitting covers, both
exceptional kernel lines, and the finite-weight rank-drop witness.  The
independent audit imports no repository code, uses a separate subset-DP
permanent, reconstructs the same exact loci, pins the dependency hashes, and
replays the primary as a subprocess.
