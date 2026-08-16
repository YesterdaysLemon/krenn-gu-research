# Self-review: fully-injective diagonal-monomial two-supported endpoint exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion as a live local theorem,
subject to the repository validation recorded below.  The theorem excludes
only

```text
C=lambda e_d tensor e_d,
w_d=0 with both complementary coordinates of w nonzero.
```

It does not exclude either coordinate endpoint for `w`, the off-diagonal
monomial endpoints, a nonmonomial residual, or any wider branch.  Global
Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2CC supplies the complete coefficientwise identity on `w^perp`, not a
   selected-source sample.  For diagonal `C` and two-supported complementary
   `w`, it gives the exact same-third-row table and the two full tensor common
   zeros `per(R,p_d,Q)=0`, `per(r_d,P,Q)=0`.
2. S2BG applies only to force `R intersect Q=P intersect Q=0`.  Its scope is
   not silently strengthened to an arbitrary four-space exclusion.
3. The placements `p_d,r_d in Q` follow from four-space dimension and shifts
   which preserve the complete table.  The argument separately proves that
   each common row is outside the row plane it shifts.
4. The first--middle intersection lemma has two exact gates.  Cayley's
   hyperdeterminant separates a two-target secant from every repeated-row
   Segre tangent.  S2AL mixed-factor sharing eliminates the one-target but
   noncoordinate alternatives.  The two cross-coordinate incidences are
   retained rather than accidentally discarded.
5. Since `E=R direct-sum Q`, the middle plane is a graph with invertible
   quotient columns.  Intersections with `R+span(u)` and `R+span(v)`, followed
   by common-row shifts, force at least one coordinate graph column and the
   stated attachment condition for each common row.
6. The four quotient matrices and seven Borel graph-component orbits are
   exhaustive.  Zero components, proportional components, independent pairs
   meeting the invariant `q_1` line, and independent affine pairs are kept
   distinct.  Nonzero shears are normalized; `g,h` remain arbitrary.
7. The resulting census has 29 charts: 13 table-only ideals and 16 ideals
   with both 32-equation common-zero tails.  The certificate replay checks the
   original ordered generators, not only a standard basis.

## Certificate audit

The pinned certificate file has SHA-256

```text
e9414389e653a76770d8f105a086fcae6887d2dbe012f41e5d74f78686c72f52.
```

It contains 29 rational polynomial identities with 2,972 sparse multiplier
terms.  Each identity is checked as

```text
sum_nu h_nu f_nu = 1
```

in the ordinary polynomial ring.  The generation route uses `slimgb` and
`lift`, and checks the lifted identity before serialization.  Replay does not
trust the generator.

The primary verifier uses SymPy.  The independent audit imports neither the
primary verifier nor SymPy; it reverses all 27 variables and reconstructs the
permanent expansion and certificate multiplication with standard-library
`Fraction` sparse maps.

## Adversarial checks and rejected shortcuts

- An early exploratory function-field lift simplified to a displayed unit
  only after localization at graph coefficients.  Substitution into the
  original polynomial ideal returned a nonconstant monomial rather than one.
  That formulation was rejected.  None of its output is present in the
  durable certificate.
- The final parameter certificates are polynomial in `tau,g,h`; no inverse,
  saturation variable, or finite parameter sample occurs.  The
  `prop_q1` certificate even holds at `tau=0`, though that point is already a
  neighbouring zero-component orbit.
- The common-zero tails use only selected binary source coefficients.  This
  is sound because the physical tensors vanish completely, so those
  coefficients are necessary equations.  No converse is claimed.
- A table-only identity is allowed to omit redundant common-zero equations:
  inconsistency of a subset already excludes the physical chart.
- The tangent hyperdeterminant is checked as a polynomial identity, including
  degenerate factor evaluations; the proof does not rely on an unrecorded
  source-form nonvanishing assumption.
- Singular is a regeneration dependency, not a replay dependency.  Both
  checked replay routes use only the pinned JSON.

## Validation

Focused validation completed:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff 0.16.2:                                  PASS
candidate-tree hygiene:                       PASS
  1,989 Python / 1,133 Markdown / 216 ledger entries
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

## Remaining obligations

The diagonal branch now has two discrete coordinate endpoints for each
diagonal colour.  Those endpoints have not been shown empty.  The
off-diagonal monomial endpoint and every nonmonomial S2BQ tangent-quotient
chart are also untouched by this theorem.  The global resolution gate is not
triggered by this local advance.
