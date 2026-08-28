# Hostile review: GLD91 rank-eight two-leaf slice Fitting exclusion

## Verdict

**Accept as an exact characteristic-zero finite-slice exclusion, with the
full-chart and global boundaries preserved.** The primary reconstructs the
named GLD84 rank-eight Schur chart from the committed moving builder, uses the
correct Gaussian-offset centre base, and derives an exact Q(i) residual
elimination on the slice
\[
x_9=1,\quad x_{10}=x_{11}=x_{12}=0,\quad x_{13}=t,\quad x_{14}=u.
\]
The resulting finite fibre classification leaves exactly one point in the
Schur/frame open. The upstream GLD85 full-intrinsic certificate proves the
Fitting map has rank 45 at that point. Thus the slice intersection with
V(I_Pl) is empty.

This must not be promoted to a unit-ideal statement for the full six-leaf
rank-eight chart, an exclusion on the other rank-eight charts, or a global
Krenn--Gu result.

## Reviewed artifacts

- [GLD91 theorem](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_TWO_LEAF_SLICE_FITTING_EXCLUSION_THEOREM.md);
- [GLD91 primary](../../claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_exclusion.py);
- [GLD91 independent audit](../../claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_exclusion.py);
- [GLD91 certificate](../../claims/arbitrary-order/four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_certificate.json);
- [GLD85 upstream full-intrinsic theorem](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_FULL_INTRINSIC_FITTING_NONZERO_THEOREM.md).

## 1. Exact claim under review

The theorem works over Q(i) and then scalar-extends to C. It fixes the
named rank-eight row chart
\[
R_8=(0,1,2,3,4,5,6,7)
\]
and the two-leaf slice displayed above. The two residual equations have
degrees 3 and 4 with 9 and 13 terms. The exact Schur determinant has degree 3
and 9 terms. The corrected centre-frame determinant numerator has degree 10
and 54 terms.

The residual Groebner basis has length 3, degrees (9,9,10), term counts
(12,12,10), and a degree-10 elimination polynomial. The direct resultant
has degree 11 because the t=-2/3 fibre has two distinct u values. Its
five-degree factor Q5 is squarefree, and the affine relation on that
component is pinned in the certificate.

The exact fibre table has six linear fibres plus five geometric Q5 points.
The Q5 substitution reduces both residuals and mu_R to zero. The linear
fibres are either Schur-boundary, centre-frame-boundary, or the pinned point.
Exactly one fibre survives the Schur/frame open.

## 2. Corrected centre-base issue

An earlier exploratory frame-boundary script used
\[
[[-2,-1,3],[0,-3,0],[0,-1,1]]
\]
and omitted the fixed Gaussian offsets. That exploratory output is not used.
The committed builder's base is
\[
[[-2-2i,-1+2i,3],[0,-3+3i,0],[0,-1+2i,1]].
\]

The GLD91 primary constructs the base from builder.chart.centre, asserts
equality with this exact Gaussian matrix, and compares the resulting
mu_R, centre numerator, leaf determinant, Groebner data, and fibres with
the byte-pinned artifact. The theorem and certificate explicitly disclose
the correction. No claim is inferred from the withdrawn exploratory
boundary output.

## 3. Boundary and quantifier controls

The Q5 roots are not silently discarded by dividing by mu_R: the audit
checks the exact composition/remainder identity
\[
\mu_R(t,U(t))\equiv 0\pmod{Q5}.
\]
They are therefore recorded as points outside the Schur localization.

For the linear fibres, a zero centre determinant numerator is treated as a
centre-frame boundary only when mu_R is nonzero. At mu_R=0 fibres the
centre solve is not evaluated. The two distinct points above t=-2/3 are
kept separate: u=-2/3 is centre-frame boundary, while u=0 is the GLD85
open point.

The leaf determinant is evaluated exactly at every linear fibre. The open
fibre count is one, not inferred from the projection polynomial alone.

## 4. Fitting input and upstream dependency

At (t,u)=(-2/3,0), GLD85 supplies the exact full intrinsic quotient map
shape 45 x 6240, rank-13 constant block, selected columns, and a
denominator-checked nonzero 45-by-45 minor. Its residues are

~~~text
1000000007: 9639769 + 249939722 i,
10000019:   1610829 +   5232695 i.
~~~

The GLD91 primary does not rederive the 6240-column transport; it pins the
GLD85 certificate hash, selected columns, denominator counts, and residues.
The upstream GLD85 primary and audit own the construction and modular
determinant proof. This dependency is stated rather than presented as a
second derivation.

## 5. Independent audit

The GLD91 audit imports no repository module, SymPy, primary verifier, or
moving builder. It parses only the committed sparse artifact and performs
its own Fraction-based Gaussian-rational polynomial arithmetic. It checks:

- the GLD75/GLD85 source hashes;
- factorization of the residual eliminant, resultant, and frame eliminant;
- squarefreeness of Q5;
- the affine u=U(t) relation;
- zero remainders for rho_8, rho_9, mu_R, and the centre numerator
  modulo Q5;
- exact evaluation of both residuals and all boundary polynomials at each
  linear fibre; and
- GLD85 point metadata and nonzero minor residues.

It does not claim to independently derive the primary's Groebner basis. That
derivation/audit division is explicit and honest.

## 6. Rejected strengthenings

1. **Full six-leaf unit ideal.** Not proved. GLD91 handles one two-variable
   slice only.
2. **Full-chart residual emptiness.** Not proved. The slice has an open
   residual point, albeit outside V(I_Pl); other six-leaf points remain.
3. **Other rank-eight charts.** Untouched: 44 additional row charts remain.
4. **Rank-seven/lower branches.** Untouched, including the rank-at-most-six
   determinantal branch.
5. **Frame-boundary deletion as a global argument.** Rejected. Schur and
   frame boundaries are explicitly retained and classified.
6. **Finite-field sampling as proof.** Not used for the residual
   classification; all slice equations and fibre data are exact over Q(i).
7. **Global resolution.** The Krenn--Gu conjecture remains **UNRESOLVED**.

## 7. Reproducibility

~~~powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_exclusion.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_exclusion.py
~~~

The certificate's canonical LF SHA-256 is
6b3fb7fbd0b62e88b9027f8d94fcf31d86331e67a3d439dc4ef9bb0d03bbf82f.

The smallest honest successor is to extend the exact ideal/Fitting
calculation off this slice across the remaining four leaf variables, while
preserving the Schur and frame boundary case split.
