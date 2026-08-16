# Self-review: S2BT support-one split-lift atlas

Date: 2026-08-13

## Claim reviewed

The S2BT claim says that, on the S2BR joint-rank-four/rank-eight
same-missing-colour `(2,2,2)` cell with coordinate third-row kernel
`span(e_s^*)`, the complete empty-target coefficient identity forces

```text
(0,0,e_d) in K,                 (0,e_s,0) in K,
```

and hence gives the two exhaustive four-space normal forms and polarized
root-product atlases stated in the theorem.  It does not claim that either
remaining atlas is empty.

## Adversarial checks

1. **Coefficient orientation.**  The proof uses physical source coefficients
   `[T_c]G_N`, whose values are root tensors.  The conditions `r_d=0` and
   `q_s=0` therefore kill first- and third-root contractions of every such
   coefficient.  They do not incorrectly assert that the whole coefficient
   vanishes.

2. **Preimage existence.**  Each correction `u_c` lies in `U` by the full
   target identity, and `U=D(K)` in this chart.  Choosing its derivative
   preimage in `K` is therefore justified.  No inverse of `D` outside its
   image is used.

3. **Missing-colour third component.**  The isolated `d` row of `C` is
   `kappa e_d`, while `pr_1 K` avoids `e_d`.  First contraction of `u_d`
   fixes all of `c_d`, not merely its `d` coordinate:
   `c_d=-kappa^(-1)e_d`.

4. **Syzygy subtraction.**  Third contraction of the same coefficient has
   no target term because `d!=s`.  Since `e_s^*(w)!=0`, the remaining
   two-factor tangent expression vanishes.  Its kernel is exactly the line
   `(e_s,y)`, so subtracting the already contained derivative syzygy is
   valid and leaves `(0,0,e_d)`.

5. **Second split vector.**  For the `T_s` coefficient, first contraction
   forces `c_s=0`; third contraction gives a nonzero scalar multiple of
   `e_s tensor e_s`.  Quotienting first by `e_s` shows that the preimage is,
   modulo the syzygy, a nonzero multiple of `(0,e_s,0)`.  This argument does
   not assume `w=e_s`.

6. **Exhaustiveness of the two normal forms.**  The only fork is whether
   `y` and `e_s` span one or two lines.  In the two-line case their second
   projections kill the second component of the fourth lift; the first-row
   rank then forces its first component to be complementary.  In the
   one-line case the first two known generators independently remove both
   `e_s` components, and the two row ranks force both remaining `e_t`
   coefficients nonzero.  The proportionality scalar `lambda` is retained;
   it is not silently normalized away.

7. **Permanent multiplicities.**  The primary and independent replays
   enumerate all 20 unordered triples of four basis vectors.  The nonaligned
   chart has exactly eight nonzero products.  The aligned chart has ten,
   including the repeated pairs and the factors `2` and `6`; both spans have
   exact rank eight.

8. **Direct quotient scope.**  The assertion `U intersect L=0` is made only
   on `C_bar!=0`.  There S2BQ forces coordinate `w`, and the third-row kernel
   selects `w=e_s`.  The `dd d`, `dd t`, and `ss s` coefficients then
   eliminate the three `U` generators in that order.  No direct-sum claim is
   made on the monomial-`C` branch with possibly noncoordinate `w`.

9. **Quantifier and status boundary.**  The proof is exact over
   characteristic zero and applies to every physical point satisfying the
   stated row-profile hypotheses.  It removes the nonsplit missing-colour
   lift parameter and classifies `K`; it does not exclude arbitrary
   complementary directions or `C_bar`, the aligned cell, other row
   profiles, pair coupling, other components, higher orders, or all-rank
   drop.  Global status remains `UNRESOLVED`.

## Independent evidence

The SymPy replay constructs the derivative and both affine contraction
systems, verifies rank eight and one-dimensional syzygy freedom, enumerates
both root-product tables, and checks the direct quotient.  The no-import
audit uses standard-library `Fraction`, reverse tensor indexing, independent
row reduction, and separately rebuilt permanent enumeration.  Neither
script imports the other or the theorem implementation.

## Review result

**PASS for the stated split-lift atlas and nonsplit-lift rigidity.**  No
global-resolution claim is supported or made.
