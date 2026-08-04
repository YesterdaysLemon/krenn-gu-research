from pathlib import Path

base = Path(__file__).resolve().parent.parent

atlas = base / "P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md"
text = atlas.read_text()

old = ("| `af(r+1)-(r-1)=0` | `D_01` | four markings | ternary "
       "(attempted) | mode-3 reduced Fitting (II.5; status in ledger) |")
new = ("| `af(r+1)-(r-1)=0` | `D_01` | four markings | OPEN "
       "(ternary attempted) | mode-3 chart-free Fitting: on-divisor "
       "denominator units certified, main Groebner timeout-null at "
       "the 550 s budget; modular evidence complete (II.5) |")
assert old in text, "scoreboard row"
text = text.replace(old, new)

old = """Char-0 certificate design
(`verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py`,
case `coupled`): one chart-free Fitting run over all markings,
`ideal(G(t)x rows at r_c, Phi, det D3[0,2,4,7], det D3[0,4,5,7],
w*A(x)B(x)-1)` in `(phi,t0..t3,x0..x3,w)`, with every denominator
cleared by powers of the unit `af-1`.  Outcome recorded in
`special_slope_reduced_fitting_results.json` and `findings.md`."""
new = """Char-0 certificate attempt
(`verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py`,
case `coupled`): one chart-free Fitting run with the slope kept as a
ring VARIABLE and the divisor polynomial `af(r+1)-(r-1)` adjoined to
the ideal — `ideal(divisor, Phi, G(t)x rows, det D3[0,2,4,7],
det D3[0,4,5,7], w*A(x)B(x)-1)` in `(phi,r,t0..t3,x0..x3,w)`, all
permanents computed inside Singular (program
`scripts/coupled_program.sing`, log
`scripts/coupled_singular_run.log`).  The four on-divisor denominator
unit certificates PASSED, certifying the reduced system is valid on
the whole divisor; the main Groebner hit the 550 s budget —
**timeout-null**, recorded in
`special_slope_reduced_fitting_results.json`.  The divisor therefore
remains OPEN at characteristic zero, with the complete modular
picture above and two natural next moves: (i) rerun with the `H31`
verifier's block ordering `(dp(extension),dp(marking))` + `slimgb`
(the pattern that succeeded where plain `dp` stalled), (ii) split
into the four sheet strata first (each fixes at least two `t`'s)."""
assert old in text, "II.5 tail"
text = text.replace(old, new)

old = """af(r+1)-(r-1)=0 (D_01)   see the case-study section (status recorded
                          there honestly)."""
new = """af(r+1)-(r-1)=0 (D_01)   OPEN: mode-3 certificate designed, modular
                          evidence complete, on-divisor denominator
                          units certified; main Groebner timeout-null
                          (II.5)."""
assert old in text, "header block"
text = text.replace(old, new)
atlas.write_text(text)
print("atlas finalized")

f = base / "findings.md"
text = f.read_text()
old = """  - char-0 certificate attempted: chart-free mode-3 Fitting on the
    reduced system with r symbolic and the divisor polynomial in the
    ideal
    (verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py,
    'coupled' case; program scripts/coupled_program.sing, log
    scripts/coupled_singular_run.log).  The four on-divisor
    denominator unit certificates PASSED (y-elimination valid on the
    divisor); final status of the main Groebner is recorded in
    special_slope_reduced_fitting_results.json."""
new = """  - char-0 certificate attempted: chart-free mode-3 Fitting on the
    reduced system with r symbolic and the divisor polynomial in the
    ideal
    (verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py,
    'coupled' case; program scripts/coupled_program.sing, log
    scripts/coupled_singular_run.log).  The four on-divisor
    denominator unit certificates PASSED (y-elimination valid on the
    divisor); the main Groebner hit the 550 s budget — TIMEOUT-NULL,
    recorded in special_slope_reduced_fitting_results.json.  The
    divisor stays OPEN at char 0.  Next moves: block ordering
    (dp(extension),dp(marking)) + slimgb as in the H31 verifier, or
    per-sheet strata (each fixes at least two t's)."""
assert old in text, "findings coupled"
text = text.replace(old, new)

old = """Together with the generic theorem: on the eighth component the
weighted-H22 slope divisors r in {0, 1, -1, infinity} of both pencils
are all closed over the generic component point.  The remaining open
slope locus is the coupled divisor af(r+1)-(r-1)=0 (status below),
plus all slope x parameter intersections and the projective boundary."""
new = """Together with the generic theorem: on the eighth component the
weighted-H22 slope divisors r in {0, 1, -1, infinity} of both pencils
are all closed over the generic component point.  The remaining open
slope locus is the coupled divisor af(r+1)-(r-1)=0 (attempted;
timeout-null; status below), plus all slope x parameter
intersections and the projective boundary."""
assert old in text, "findings summary"
text = text.replace(old, new)
f.write_text(text)
print("findings finalized")
