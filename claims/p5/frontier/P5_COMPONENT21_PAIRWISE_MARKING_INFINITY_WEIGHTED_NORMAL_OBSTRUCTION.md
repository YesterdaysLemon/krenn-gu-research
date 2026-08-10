# Component 21: all pairwise marking-pole weighted normals

## Status and scope

This note classifies the nonzero `P4` restrictions of weighted normals at
all six pairwise simultaneous marking-pole corners on the displayed
normalized component-21 sheet.  The calculation is exact over `Q`.  It
keeps `kappa`, `ell`, and every remaining finite marking as polynomial
variables; it makes no genericity assumption and inverts no component or
marking parameter.

For each corner, the homogeneous boundary tensor has zero `P4`
restriction.  The statement proved here is that every weighted normal whose
first ambient term has nonzero `P4` restriction is obstructed for
fixed-order marked `H31` and homogeneous weighted `H22`.  The proof applies
the full incidence and obstruction equations directly to exact residual
pairs.  Sparse pure support identifies the controlling monomials and checks
the residual tensor, but is not used as a transfer theorem.

Triple and quadruple marking poles remain **UNKNOWN**.  Intersections with a
component-parameter boundary, extension-coordinate infinity, arbitrary
source, ambient, and projective degenerations, and every ambient `P5`
leading term whose `P4` restriction is zero also remain **UNKNOWN**.  The
arbitrary-order local-to-global reduction is open, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

No finite-field computation is used as proof.

## Homogeneous pair charts

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

All rows outside the chosen pole pair retain their finite marking shifts.
Direct permanent expansion gives two symmetry classes.

### A pair containing `h0`

For `{0,j}`, where `j` is one of `1,2,3`, the only nonzero coefficients are

\[
 T_{0111}=4s_jp,\qquad
 T_{1111}=4s_j(p+s_0q).                            \tag{3}
\]

Thus the two monomials controlling every nonzero `P4` leading term are

\[
 X=s_jp,\qquad Y=s_0s_jq.                         \tag{4}
\]

### A pair not containing `h0`

For `{i,j}` contained in `{1,2,3}`, the only nonzero coefficients are

\[
 T_{0111}=4s_is_jp,\qquad
 T_{1111}=4s_is_j(h_0p+q).                        \tag{5}
\]

The controlling monomials are now

\[
 X=s_is_jp,\qquad Y=s_is_jq.                      \tag{6}
\]

Equations (3) and (5) vanish when both inverse marking coordinates vanish.
That zero restriction is recorded, not promoted to an obstruction.

## Exact weighted-normal representatives

Consider a characteristic-zero DVR arc, or an arc after a finite Puiseux
extension, approaching one of the pairwise corners.  Assume its first
ambient term has nonzero `P4` restriction.  Let `m` be the smaller valuation
of the two monomials in (4) or (6), and let `P,Q` be their coefficients of
order `m`, with zero used when one monomial has larger valuation.  Then
`(P,Q)!=(0,0)`.

Specialize `p=q=0` in (1).  All modes outside the pole pair retain their
finite component bases and finite marking shifts.

For a pair `{0,j}`, an exact residual-pair representative is

\[
 (a_0^{\rm wt},b_0^{\rm wt})=(PB,(P+Q)B),\qquad
 (a_j^{\rm wt},b_j^{\rm wt})=(0,b_j).             \tag{7}
\]

Its pure support is

\[
 T_{0111}^{\rm wt}=4P,\qquad
 T_{1111}^{\rm wt}=4(P+Q).                        \tag{8}
\]

For a pair `{i,j}` contained in `{1,2,3}`, use

\[
\begin{aligned}
 (a_0^{\rm wt},b_0^{\rm wt})&=(PB,(h_0P+Q)B),\\
 (a_i^{\rm wt},b_i^{\rm wt})&=(0,b_i),\\
 (a_j^{\rm wt},b_j^{\rm wt})&=(0,b_j).
\end{aligned}                                      \tag{9}
\]

Its pure support is

\[
 T_{0111}^{\rm wt}=4P,\qquad
 T_{1111}^{\rm wt}=4(h_0P+Q).                     \tag{10}
\]

These formulas include all valuation comparisons and all cancellation
directions.  If the second coefficient in (8) or (10) cancels, `P` is
nonzero and the first survives.  If `P=0`, then `Q` is nonzero and the
second survives.  No affine chart on `[P:Q]` is selected.

## Direct incidence obstruction

For each of the six residual pairs (7) or (9), introduce all eight extension
coordinates and retain `P,Q,kappa,ell` together with every marking not in
the pole pair.

For marked `H31`, the distinguished-zero and distinguished-one orientations
are Hall-deficient.  For each of distinguished vertices two and three,
impose the fourteen mixed equations, normalize the all-alpha diagonal,
invert the all-beta diagonal, and impose the full 32-entry mode-three
obstruction map.  Both reduced Groebner bases are `[1]` over `Q`.

For homogeneous weighted `H22`, the reverse orientation is Hall-deficient
because the `D01` all-alpha diagonal vanishes identically.  In the surviving
`D01`-pure/`D23`-binary orientation, impose all unwanted coefficients,
normalize the required `D01` coefficient, invert both `D23` diagonals, and
impose the full mode-three obstruction map.  The finite and infinite weight
charts both have reduced Groebner basis `[1]`.

This gives four exact global unit ideals for each of six pole pairs, for a
total of twenty-four.  No factor is discarded and no finite component or
marking value is removed.

## Exact conclusion

**At every pairwise simultaneous marking-pole corner of the displayed
normalized component-21 sheet, every weighted normal with nonzero `P4`
restriction contains no fixed-order marked `H31` point and no homogeneous
weighted `H22` point.**

The pairwise boundary itself has zero `P4` restriction.  An earlier ambient
`P5` leading term invisible on `P4`, or a further simultaneous pole, lies
outside this theorem.

## Replay

Replay the pinned normalized component-21 package first:

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy --with ruff python -m ruff check claims/p5/frontier/verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py claims/p5/frontier/audit_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python -m py_compile claims/p5/frontier/verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py claims/p5/frontier/audit_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py
```

The primary reconstructs all six homogeneous charts, the six exact residual
pairs, and all twenty-four unit ideals.  The independent audit imports no
repository code, uses a separate subset-DP permanent, reconstructs the same
twenty-four ideals, pins the normalized component-21 dependency hashes, and
replays the primary as a subprocess.
