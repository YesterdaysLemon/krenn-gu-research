# Self-review: S2BV nonaligned source atlas and pair-pole exclusion

Date: 2026-08-13

## Claim reviewed

S2BV classifies every complete empty-target solution in S2BT's nonaligned
same-missing-colour, coordinate-third-kernel `(2,2,2)` chart.  It proves that
the surviving solutions are one exact same-source two-plane family and that
their unique rational pair lift always has a prime-divisor pole.  The claim
is a graph-extension exclusion, not an assertion that the local empty cell is
empty.

## Adversarial checks

1. **Root-box directness.**  As in S2BU, `U intersect L=0` uses the isolated
   `dd d`, then `dd t`, then nonzero `ss s` coefficients.  It does not assume
   `C_bar!=0` or coordinate `w`.  The eight source equations therefore come
   from unique representatives rather than an arbitrary quotient splitting.

2. **Basis change and independence.**  The rows
   `u=g_0`, `r=g_1`, `q=y_s g_0-g_2`, and `v=g_3` differ from the injected
   dual `K` basis by an invertible triangular change.  Their independence is
   justified by surjectivity of `H`, not assumed separately without origin.

3. **Complete target data.**  The four `d`-slice coefficients retain all four
   entries of `C_bar`; the `ss d` coefficient also retains the `w_d T_s`
   term.  The `ss t` coefficient retains `w_t T_s`; the `stt,tst` zeros and
   nonzero `ttt` target are retained.  No root coefficient used by the source
   classification is silently discarded.

4. **Support split.**  Nonzero `P(v,u,v)` rules out one-source `v`.  The proof
   separately treats exactly-two-source and three-source `v`, exhausting the
   source-support possibilities.

5. **Two-source branch.**  The deformed zero
   `P(u+A v,u,v)=0` puts the first two components of `u` on the two lines of
   `v` and gives the exact scalar relation.  The square equation for `q` and
   the remaining mixed zero force the sum/difference pair.  If `A` or the two
   scaling coefficients survive, the equations put `r` on the same three
   source lines and violate four-row independence.  The final zero removes
   the residual opposite scaling in `r`, leaving the independent same-source
   vector.

6. **Three-source tangent branch.**  A decomposable vector in a Segre tangent
   shares at least two base factor lines.  The proof separates an off-base
   component from the all-scaling case.  In the off-base case, the two exact
   scalar equations plus the mixed zero give `3 beta^2=0`, so characteristic
   zero is used explicitly.  In the scaling case, any off-line component of
   `r` forces the other two components of `u` to vanish; otherwise all four
   rows lie in a three-space.  Both routes reduce to the same pure-source
   normal form.

7. **Target-line separation.**  Whenever the proof declares a `T_d` or
   `T_s` coefficient zero, the corresponding permanent contains at least two
   factor lines of `T_t`, or has a fixed `T_t` factor in a source where the
   other targets use distinct lines.  Quotienting those factor lines
   separates it from `T_d,T_s`; this is not a numerical orthogonality claim.

8. **Residual root parameters.**  Reading the vanished target coefficients
   forces all of `C_bar=0` and `w_d=w_t=0`.  The deformed shear scalar is the
   `e_s` component of the nonaligned fourth lift, so its vanishing forces
   `a=e_t` up to the already allowed nonzero scaling.  The other tangent
   factor retains the honest parameter `b`.

9. **Sharp control versus graph.**  Direct permanent expansion shows that
   every root coefficient except `ttt` vanishes and that `ttt=T_t`.  The four
   dual rows are independent for every allowed `r`; the singleton determinant
   is nonzero.  Thus the family is a real local target incidence.  It is not
   mislabeled as an exact graph or counterexample.

10. **Cramer uniqueness.**  The three singleton columns are written in an
    explicit `U` basis and have determinant `-2 mu x_t y_t r`.  Hence the
    displayed three pair components are the unique rational Cramer solution;
    no alternative regular pair deck can evade them.

11. **Divisor argument.**  At the generic point of `x_t=0`, the factors
    `r` and all other-source variables are units, while the numerator of
    `C_x` contains no `x_t`.  Regularity therefore forces its numerator to
    vanish identically; similarly for `y_t`.  The two residue identities
    first force `c=0`, then equate nonzero `x_s y_s` and `x_d y_d` monomials,
    an exact polynomial impossibility.  Thus at least one valuation is
    `-1`.

12. **Use of the pair gate.**  Pair regularity is necessary for every graph
    extension independently of whether the remaining Euler identities are
    checked.  Showing one unavoidable pair pole is sufficient for exclusion;
    no sufficiency direction is being misused.

13. **Scope.**  Combining S2BU and S2BV closes only the coordinate-third-
    kernel same-colour `(2,2,2)` graph cell.  Noncoordinate third-kernel
    support, other row profiles, lower-rank cells, other components, higher
    orders, and all-rank drop remain open.  Global status remains
    `UNRESOLVED`.

## Independent evidence

The SymPy replay checks both source-support normal forms, the exact root and
source control, all eight root coefficients, singleton determinant, Cramer
solution, and divisor residues.  The no-import audit uses reverse tensor
indexing, standard-library `Fraction` elimination, and an independently
implemented sparse-polynomial ring to reconstruct the residue contradiction.
Neither implementation imports the other.

## Review result

**PASS for the exhaustive nonaligned source atlas and pair-pole graph-cell
exclusion.**  No broader resolution claim is supported or made.
