# Self-review: S2BU aligned split-lift exclusion

Date: 2026-08-13

## Claim reviewed

S2BU excludes the complete aligned normal form in S2BT's
same-missing-colour, coordinate-third-kernel `(2,2,2)` atlas.  The claim is
uniform in the nonzero aligned parameters, the complementary residual block
including zero, and every shared third factor nonzero on the missing
third-row coordinate.

## Adversarial checks

1. **Use of the S2BT atlas.**  The proof starts only after S2BT has forced
   `(0,0,e_d)` and `(0,e_s,0)` into `K` and derived the aligned fourth lift.
   It does not infer this normal form from a coordinate specialization.

2. **Arbitrary shared third factor.**  The direct-root-box argument does not
   assume `w=e_s`.  The `dd d` and `dd t` coefficients kill the first and
   third `U` generators, and the nonzero `s` coordinate of `w` kills the
   second.  Thus `U intersect L=0` also on the monomial-`C`, noncoordinate-`w`
   branch.

3. **Target representatives.**  The `d` target is represented by
   `-kappa^(-1) C_bar tensor e_d`.  The `s` target is represented by the two
   `ss d` and `ss t` terms obtained from `e_s e_s w`.  Neither representative
   has `stt`, `tst`, or `ttd` support except that the `d` representative can
   contribute `ttd` through `c_tt`.  The `ttt` representative is unchanged.

4. **Combinatorial coefficients.**  The four source equations are read
   directly from the root rows, not inferred from unordered-root-product
   multiplicities.  The factors `alpha`, `beta`, and `lambda` are retained,
   and all divisions use their stated nonvanishing.

5. **Cube nonvanishing.**  The `ttt` equation gives
   `alpha beta P(g_3,g_3,g_3)=T_t`.  In characteristic zero this makes all
   three source components of `g_3` nonzero and fixes their factor lines to
   those of `T_t`.

6. **Tangent-kernel dimension.**  For fully supported `v=x+y+z`, the map
   `h -> P(h,v,v)` has kernel exactly the scaling-difference plane
   `{a x+b y+c z:a+b+c=0}`.  Quotienting successively by `x,y,z` rules out
   hidden off-line kernel components.

7. **Separation from the other target.**  The image of that map is the
   Segre tangent at `T_t`.  Quotienting all three factors by the `t` lines
   kills the tangent but not `T_d`, whose three factor lines are different.
   Therefore the `ttd` equation cannot hold with a nonzero `T_d` scalar; it
   forces both `c_tt=0` and `g_1` into the tangent kernel.

8. **Final rank contradiction.**  The `stt` equation puts `g_0` in the
   two-plane kernel.  Substitution into `tst` puts `g_2` there, and `ttd`
   puts `g_1` there.  Adding `g_3` gives span dimension at most three.  This
   contradicts injectivity of `H^*`, which follows from the assumed
   surjectivity of `H:W->K` and `dim K=4`.

9. **Scope.**  No pair identity, generic argument, numerical search, or
   finite-field inference is used.  The theorem excludes only the aligned
   support-one split chart.  The nonaligned chart, other row profiles,
   lower-rank cells, pair coupling, other components, higher orders, and
   all-rank drop remain open.  Global status remains `UNRESOLVED`.

## Independent evidence

The SymPy replay reconstructs the derivative quotient for noncoordinate
`w`, symbolically checks the four row formulas, and computes the tangent map,
its kernel, and target separation.  The no-import audit uses reverse tensor
indexing, standard-library `Fraction` row reduction, independently chosen
exact fixtures, and separately rebuilt permanent arithmetic.  Neither
implementation imports the other.

## Review result

**PASS for the complete aligned-chart exclusion.**  No broader resolution
claim is supported or made.
