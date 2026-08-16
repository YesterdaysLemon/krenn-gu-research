# Self-review: fully-injective off-diagonal-monomial coordinate-endpoint exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion as a live local theorem,
subject to the repository validation recorded below.  The theorem excludes
only

```text
C=lambda e_d tensor e_e,       d!=e,
w proportional to the unique third coordinate.
```

It does not exclude either diagonal coordinate endpoint, a nonmonomial
residual, or any wider branch.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2CC supplies the complete coefficientwise identity on `w^perp`.  At the
   off-diagonal endpoint it gives two transverse target corners, exactly one
   unrestricted parallel edge, the common-row faces `per(R,v,Q)=0` and
   `per(u,P,Q)=0`, and the separate cross-zero `per(u,v,Q)=0`.
2. The sparse-edge separation statement is not inferred from S2BG or from a
   solver timeout.  Its incidence cover has 218 initial charts: 162 for
   `dim(R intersect Q)=1` and 56 for `R=Q`.
3. Exact table-only identities exclude 210 initial charts.  The eight
   lift-hard charts are replaced by a proved split on whether the physical
   row lies in `S=R+Q`, producing 98 logical physical refinements.
4. The reduced flag unions are exhaustive by the displayed Pluecker-minor
   pivot argument.  The `f21_p10_zero` replacement is exact: its complement
   inside `f21` has a nonzero coefficient and is already `f20`.  No failed or
   timed-out leaf is used as evidence.
5. Lemma 1 gives `R intersect Q=0`; root exchange gives `P intersect Q=0`.
   Injectivity, not the sparse table alone, supplies `v notin P` and
   `u notin R`.
6. To place `v` in `Q`, the shifted middle plane must still carry the
   root-exchanged common-row face.  This is where `per(u,v,Q)=0` is essential.
   The theorem states that cross-zero explicitly rather than silently treating
   it as a consequence of the two separate common-row faces.
7. Once `E=R direct-sum Q`, the quotient matrix has three
   diagonal-torus/right-Borel orbits and the nonzero line `span(v)` has three
   torus support orbits.  The resulting nine terminal charts are exhaustive.
8. All 317 logical charts are excluded by exact ordinary-ring identities.
   A separate characteristic-not-two tangent-tensor argument also excludes
   the nine terminal charts and never uses the unrestricted `(r_0,p_1)` edge.

## Coverage audit

An adversarial read-only audit reconstructed the Schubert cover independently.
For independent rows `a,b in k^3`, it used the pivot condition

```text
a_i (a_i b_j-a_j b_i) !=0
```

and checked every residual minor wall against the explicit boundary charts.
It found no missing stratum.  As implementation sanity checks, the primary
verifier enumerates the complete flag varieties over `F_3` and `F_5`, while
the no-import audit uses an independent `F_7` implementation.  The respective
counts `52`, `186`, and `456` are completely covered.  These finite checks do
not replace the characteristic-zero minor proof.

## Certificate and deduplication audit

The pinned certificate file has SHA-256

```text
e940282a15261df2e5cc6d46c698b9bdb5e37299d5b5bb791dfeef4d711e3af1.
```

It records 317 logical coverage keys but only 287 literal polynomial systems.
An independent exact audit found 18 duplicate groups accounting for 30 alias
keys.  All duplicates are physical 80-generator systems; all 210 table-only
systems are unique.  The generator now hashes the complete rendered Singular
program after replacing only the display key.  Thus the solver strategy is
already frozen before canonicalization, identical systems share one cache and
one certificate, and every logical key retains explicit stage and parent
lineage.

The 287 rational identities contain 151,484 sparse multiplier terms and are
checked as

```text
sum_nu h_nu f_nu = 1.
```

There are 48 ordered generators for table-only systems and 80 after the
physical `per(R,v,Q)=0` tail.  The primary verifier reconstructs the rows and
permanents with SymPy.  The independent audit imports neither the primary
verifier nor the generator; it reverses all 36 variables, parses the row
expressions through a restricted standard-library AST, and multiplies sparse
polynomials with `Fraction` coefficients.

## Adversarial checks and rejected shortcuts

- The initial unrestricted batch was stopped and supplies no mathematical
  evidence.  The durable generator uses one process per leaf, defaults to a
  120-second wall cap and 8-GiB address-space cap, caches only parsed outputs,
  and cannot write a final JSON after a filtered or incomplete run.
- Nineteen early broad refinements hit their resource cap.  None is cited as
  an exclusion.  Exact projective boundary decompositions replaced them, and
  every replacement produced a checked ordinary-ring lift.
- One surviving broad `f21` lift had 150,106 multiplier terms.  Its overlap
  with `f20` was proved algebraically, leaving only the `p10=0` wall.  The wall
  has a 204-term identity.  This reduced the canonical artifact from 301,386
  to 151,484 terms without removing a geometric point.
- No inverse, saturation variable, hidden nonzero solver parameter, modular
  lift, random parameter sample, or generic-point substitution occurs in a
  certificate.
- The finite-field flag enumerations are labeled sanity checks.  The
  characteristic-zero coverage is the projective/minor argument in the owning
  theorem.
- The terminal tangent lemma divides only by two and is therefore valid over
  the stated characteristic-zero field.  The exact endpoint certificates
  remain a redundant independent route.

## Validation

Focused validation completed:

```text
primary SymPy replay:                         PASS
  317 logical charts / 287 systems
  151,484 rational multiplier terms
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
  1,992 Python / 1,135 Markdown / 217 ledger entries
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

## Remaining obligations

The monomial part of the fully-injective `(3,3,3)` profile is now reduced to
the diagonal coordinate endpoints left by S2CD.  Those endpoints have not
been shown empty.  Every nonmonomial S2BQ tangent-quotient chart also remains
open, as do the other target cells, components, pole strata, pair gates, and
higher orders.  The global resolution gate is not triggered by this local
advance.
