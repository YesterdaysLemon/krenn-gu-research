# Component 21: triple and quadruple marking-pole weighted normals

## Status and scope

This note classifies the nonzero `P4` restrictions of weighted normals at
the four triple and one quadruple simultaneous marking-pole corners on the
displayed normalized component-21 sheet.  The calculation is exact over
`Q`.  It keeps `kappa`, `ell`, and every remaining finite marking as
polynomial variables; it makes no genericity assumption and inverts no
component or marking parameter.

For each of the five corners, the homogeneous boundary tensor has zero
`P4` restriction.  The statement proved here is that every weighted normal
whose first ambient term has nonzero `P4` restriction is obstructed for
fixed-order marked `H31` and homogeneous weighted `H22`.  The proof applies
the full incidence and obstruction equations directly to exact residual
pairs.  Sparse pure support identifies the controlling monomials and checks
the residual tensor, but is not used as a transfer theorem.

Intersections with a component-parameter boundary, extension-coordinate
infinity, arbitrary source, ambient, and projective degenerations, and every
ambient `P5` leading term whose `P4` restriction is zero remain **UNKNOWN**.
The arbitrary-order local-to-global reduction is open, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

No finite-field computation is used as proof.

## Homogeneous marking charts

Write

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1),
\]

and use the normalized component bases

\[
\begin{aligned}
 a&=(A+pB,\ell A+C,C,D),\\
 b&=(C+qB,A,B+\kappa A,A+\ell C).
\end{aligned}                                      \tag{1}
\]

At a marking pole `h_i=infinity`, put `s_i=1/h_i` and replace the marked
row by the regular homogeneous row

\[
 b_i^\infty(s_i)=a_i+s_i b_i.                     \tag{2}
\]

Rows outside the pole set retain their finite marking shifts.

### The corner `{1,2,3}`

Put `S=s_1s_2s_3`.  Direct permanent expansion gives precisely

\[
 T_{0111}=4Sp,\qquad T_{1111}=4S(h_0p+q).          \tag{3}
\]

Thus the monomials controlling every nonzero `P4` leading term are

\[
 X=Sp,\qquad Y=Sq.                                 \tag{4}
\]

### Corners containing `0`

Let `J` be either a two-element subset of `{1,2,3}` or all of
`{1,2,3}`, and put

\[
 S=\prod_{i\in J}s_i.
\]

At the pole set `{0} union J`, the only nonzero coefficients are

\[
 T_{0111}=4Sp,\qquad T_{1111}=4S(p+s_0q).          \tag{5}
\]

The controlling monomials are

\[
 X=Sp,\qquad Y=s_0Sq.                              \tag{6}
\]

Equations (3) and (5) vanish when all inverse marking coordinates in the
chosen pole set vanish.  That zero restriction is recorded, not promoted
to an obstruction.

## Exact weighted-normal representatives

Consider a characteristic-zero DVR arc, or an arc after a finite Puiseux
extension, approaching one of the five corners.  Assume its first ambient
term has nonzero `P4` restriction.  Let `m` be the smaller valuation of the
two monomials in (4) or (6), and let `P,Q` be their coefficients of order
`m`, with zero used when one monomial has larger valuation.  Then
`(P,Q)!=(0,0)`.

Specialize `p=q=0` in (1).  At `{1,2,3}`, an exact residual-pair
representative is

\[
 (a_0^{\rm wt},b_0^{\rm wt})=(PB,(h_0P+Q)B),
 \qquad
 (a_i^{\rm wt},b_i^{\rm wt})=(0,b_i)\quad(1\le i\le3). \tag{7}
\]

Its pure support is

\[
 T_{0111}^{\rm wt}=4P,\qquad
 T_{1111}^{\rm wt}=4(h_0P+Q).                     \tag{8}
\]

At `{0} union J`, use

\[
 (a_0^{\rm wt},b_0^{\rm wt})=(PB,(P+Q)B),
 \qquad
 (a_i^{\rm wt},b_i^{\rm wt})=(0,b_i)\quad(i\in J). \tag{9}
\]

Every mode outside the pole set retains its finite component basis and
finite marking shift.  The pure support of (9) is

\[
 T_{0111}^{\rm wt}=4P,\qquad
 T_{1111}^{\rm wt}=4(P+Q).                        \tag{10}
\]

These formulas include every valuation comparison and cancellation
direction.  If the second coefficient in (8) or (10) cancels, `P` is
nonzero and the first survives.  If `P=0`, then `Q` is nonzero and the
second survives.  No affine chart on `[P:Q]` is selected.

## Direct incidence obstruction

For each residual pair (7) or (9), introduce all eight extension
coordinates and retain `P,Q,kappa,ell` together with every marking outside
the pole set.

For marked `H31`, the all-alpha diagonal is identically zero for every one
of the four distinguished source-coordinate deletions, before imposing any
mixed equations and for arbitrary extension coordinates.  This is a direct
Hall deficiency.  Hence none of the four fixed-order marked `H31`
orientations can have both required diagonals nonzero.  No Groebner
certificate is claimed for an orientation already excluded by this
identity.

For homogeneous weighted `H22`, the reverse orientation is Hall-deficient
because the `D01` all-alpha diagonal vanishes identically.  In the surviving
`D01`-pure/`D23`-binary orientation, impose all unwanted coefficients,
normalize the required `D01` coefficient, invert both `D23` diagonals, and
impose the full mode-three obstruction map.  The finite and infinite weight
charts both have reduced Groebner basis `[1]` for each of the five corners.
This gives ten exact global unit ideals.  No factor is discarded and no
finite component or marking value is removed.

## Exact conclusion

**At every triple or quadruple simultaneous marking-pole corner of the
displayed normalized component-21 sheet, every weighted normal with
nonzero `P4` restriction contains no fixed-order marked `H31` point and no
homogeneous weighted `H22` point.**

The five boundary tensors themselves have zero `P4` restriction.  An
earlier ambient `P5` leading term invisible on `P4`, or a simultaneous
component-parameter or extension-coordinate degeneration, lies outside
this theorem.

## Replay

Replay the pairwise package used as the pinned dependency:

```powershell
uv run --with sympy python .\verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python .\audit_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python .\audit_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py .\audit_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python -m py_compile .\verify_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py .\audit_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py
```

The primary reconstructs all five homogeneous charts, all five exact
residual pairs, the twenty Hall-deficient `H31` orientations, and all ten
`H22` unit ideals.  The independent audit imports no repository code, uses
a separate subset-DP permanent, reconstructs the same identities and unit
ideals, pins the pairwise dependency hashes, and replays the primary as a
subprocess.
