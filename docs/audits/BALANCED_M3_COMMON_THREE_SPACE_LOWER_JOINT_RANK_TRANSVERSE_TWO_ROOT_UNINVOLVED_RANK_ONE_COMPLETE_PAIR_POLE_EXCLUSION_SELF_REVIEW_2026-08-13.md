# Self-review: lower-joint-rank transverse two-root q=1 complete pair-pole exclusion

Date: 2026-08-13

## Claim boundary

The theorem treats only normalized, target-consistent physical `m=3`
common-three-space full-sensor points with exactly two transverse root
blocks, total singleton span dimension three, joint rank three or four, and
uninvolved-row rank one.  It inherits S2BM's exact one-cell frame and proves
that every rational pair lift in that frame has a divisor pole.  It excludes
regular graph extensions of both cells.  It does not exclude lower-rank
three-root derivatives, another component or pole stratum, a higher order,
the all-rank-drop branch, or the global conjecture.

## Adversarial checks

1. The complementary monomial root blocks, the row pattern
   `r_t=a,r_s=v,p_u=b,p_s=v`, the one-cell equations, and the residual vector
   `(T_t,T_u,0)` are imported only from S2BM's proved `q=1` localization.
   They are not inferred from its displayed sharpness controls.
2. The source atlas begins with the exact rank-one tensor
   `per(v,v,q)=T_s`.  A one-source `v` gives zero.  For full source support,
   the elementary Segre-tangent quotient argument proves that the target
   shares at least two factor lines with `v`; this is not assumed as a
   generic tangent fact.
3. In the two-source chart, projecting the common-zero equation modulo the
   two target base lines forces every middle component onto `y_s` except
   precisely when `p=alpha x_s` and `r=-alpha z_s`.  The regular kernel is
   explicitly spanned by `-x_s+z_s` and `-p+y_s-r`; the exceptional kernel
   is `span(-x_s+z_s) direct-sum Y`.
4. The full-support transverse-target chart retains every value of
   `alpha,beta`.  For `alpha+beta!=0` the exact two-parameter kernel has
   alternating determinant on `x_s y_s z_s`.  For zero sum with nonzero
   parameter the kernel is one source summand and cannot have nonzero
   alternating determinant.  The remaining pure-target case has determinant
   on `x_s y_s L_Z` and is kept rather than discarded.
5. In the aligned-target chart, the three derivative weights are
   `beta+gamma`, `alpha+gamma`, and `alpha+beta`.  Their sum is twice the
   nonzero square coefficient, so zero-, one-, and two-zero-weight cases are
   exhaustive and a three-zero case is impossible in characteristic zero.
6. The theorem deliberately does not use `per(a,b,q)=0` after entering the
   atlas.  This strengthens rather than weakens the conclusion: every actual
   one-cell point lies among the classified two-common-zero rows, while some
   atlas charts may contain extra rows not satisfying the unused equation.
7. The missing-coordinate residue is multigraded.  The Cramer numerator for
   `C_X` replaces `g_X`, so it uses only `T_t,T_u,g_Y,g_Z` and is independent
   of `x_s`.  If a global polynomial `C_X` existed while `x_s` divided the
   determinant, the exact identity `N_X=Delta C_X` would force `N_X=0`.
   No point evaluation is promoted to divisibility.
8. When only two target-coordinate factors divide the determinant, the
   remaining possibility is checked rather than silently called impossible.
   In the conjugate two-source chart it would require one positive-bidegree
   polynomial to divide the coprime monomials `T_t,T_u`.  In the
   transverse-target and one-zero-weight charts the third root coordinate
   of the sole surviving singleton column forces its coefficient to vanish.
9. The sole one-factor determinant chart is the two-zero-weight aligned
   case.  Its exact numerator is
   `T_u(x C-y A)+T_t(y B-x D)`.  If this vanished, independence of
   `z_t,z_u` and two rank-one equalities would force
   `A=lambda x,C=lambda y,B=mu x,D=mu y`, making the supposedly nonzero
   alternating factor `AD-BC` vanish.  Thus a genuine `z_s` pole remains.
10. The graph conclusion uses the existing Cramer--Euler theorem as an iff
    gate: failure of even one pair-regularity valuation prevents a physical
    bilinear completion.  The proof does not infer that a local incidence is
    itself a graph.
11. The primary verifier uses dense SymPy tensors and symbolic Cramer
    determinants.  The no-import audit independently uses sparse tensor
    dictionaries, `Fraction` row reduction, and a separate sparse
    multivariate-polynomial determinant and valuation implementation.
    Neither replay substitutes for the arbitrary-vector quotient proof.
12. Joint rank enters only through S2BM's proved availability of the same
    one-cell frame at ranks three and four.  The source and residue proof does
    not silently identify the distinct row-space incidences of those ranks.

## Remaining obligations

- classify and exclude or globalize the lower-rank three-root derivative
  charts;
- return to the other S2T component types and S2Q pole strata;
- resolve higher orders and the all-balanced rank-drop branch;
- run the dedicated global resolution audit only if every load-bearing
  global branch is actually closed.

Global Krenn--Gu remains **UNRESOLVED**.
