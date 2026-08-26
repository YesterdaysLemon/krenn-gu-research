# Hostile review: Gaussian survivor full coefficient-fibre first-response nonextension

Date: 2026-08-24

## Verdict

**Accept as an exact full-raw-fibre first-response exclusion for the fixed
`GLD73` ten-vertex effective model.**  The transformed complete torus-star map
has rank `44`, and its fibre over the literal four-port diagonal is an affine
`35`-space over `C`.  At the contracted vertex `q_0`, every point of that
fibre has a complete legal-response span whose diagonal intersection has
dimension at most two.  A ten-mode GHZ identity requires dimension three.
Hence no complex raw preimage of the exact `GLD72` tensor extends through this
fixed interface.

This does not prove that the `GLD72` point is nonintegrable through every
source presentation, exclude the whole fixed-star GHZ-survivor locus, certify
maximum root order or fifth-root absence, produce a graph witness, or resolve
Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

**Successor update (2026-08-26).**  `GLD75` exactly rules out symmetry
compression near the Gaussian point: its survivor germ is smooth of
dimension five, whereas the fixed-interface orbit is the one-dimensional
scaling line.  This leaves four transverse parameters for the still-open
parametric response incidence and does not change the accepted scope below.

Reviewed artifacts:

- [`FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_COEFFICIENT_FIBRE_FIRST_RESPONSE_NONEXTENSION_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_COEFFICIENT_FIBRE_FIRST_RESPONSE_NONEXTENSION_THEOREM.md);
- [`verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py`](../../claims/arbitrary-order/verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py);
- [`audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py`](../../claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py);
- [`generate_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension_certificates.py`](../../claims/arbitrary-order/generate_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension_certificates.py);
- [`four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension_certificates.json`](../../claims/arbitrary-order/four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension_certificates.json);
- the [`GLD73` contracted-edge theorem](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_CONTRACTED_EDGE_CONTROL_AND_FIRST_TRANSVERSE_NONEXTENSION_THEOREM.md).

## 1. Claim and dependency boundary

The claim is made only after the `GLD72` Gaussian point is pulled back to the
literal target `Delta_4` and the canonical torus-star port maps are transformed
covariantly.  Let `b'` be the resulting complete `79`-column raw map.  The
load-bearing assertions are

```text
rank b'=44,
F=(b')^(-1)(Delta_4)=alpha_0+span(k_0,...,k_34),
dim(im D_q0(alpha) intersect Diag)<=2 for every alpha in F. (1)
```

Only the last assertion is new.  The `GLD73` pinned point and its six rank
triples are retained as an independently replayable special case; they are
not used to infer constancy over the fibre.

## 2. Completeness of the affine fibre

The primary and audit reconstruct all `1+24+54=79` raw columns and all `81`
target coordinates.  Exact Gaussian elimination finds `44` pivots, sets each
of the other `35` raw coordinates free in turn, and verifies one particular
solution plus the complete kernel basis.  No finite-field sample, generic
minor, numerical tolerance, or selected subfibre enters the claim.

The port-frame transformation changes the raw presentation's pivot pattern.
The verifier therefore recomputes pivots in the transformed coordinates; it
does not reuse the original `GLD70` pivot list.  This rejects a subtle but
real basis-coordinate shortcut found during review.

## 3. The q0 response columns are complete and correctly labelled

The response domain at `q_0` has dimension

```text
five contracted-neighbour scalars + four port three-vectors = 5+12=17. (2)
```

The `q_0--q_1` cofactor is exactly the raw `Q` column.  The twelve
`q_0--port` cofactors are exactly the **eta** residual layer: pairing `q_0`
to a port leaves `q_1`, whose root incidences are `eta`.  Reversing this label
would change the fixed quotient and is independently checked.

The remaining four columns are the `q_0--r_j` matching cofactors.  Once that
varied edge is deleted, every nonzero complementary matching pairs the three
remaining roots with three of `q_1,u_0,...,u_3`; the last two nonroots form
exactly one residual-port or port-pair edge.  Consequently each root cofactor
is linear in the raw coefficients.  Matchings containing a surviving
root-root edge vanish at grade zero and are omitted only for that exact reason.

The fixed thirteen columns have full and mixed rank `13`.  Quotienting the
mixed parts of the root columns by them gives a `65 x 4` affine matrix.  Both
implementations verify

```text
Z_0+Z_1+Z_2-Z_3=0,                                     (3)
```

the sign coming from `xi=(1,1,1,-1)`.

The response space is deliberately an over-approximation of any physical
lift with additional base-edge correlations: every independently possible
incident evaluation is allowed.  Extra constraints can only shrink its
diagonal intersection and therefore cannot invalidate the exclusion.

## 4. Rank inequality audit

Put `Z=[Z_0 Z_1 Z_2]`.  By construction,

```text
rank(pi_mix D_q0)=13+rank Z.                            (4)
```

No assertion that `rank D_q0=17` throughout the fibre is made.  Only the
domain bound `rank D_q0<=17` is used:

```text
dim(im D_q0 intersect Diag)
 =rank D_q0-rank(pi_mix D_q0)
 <=4-rank Z.                                            (5)
```

Thus a three-dimensional GHZ response would require `rank Z<=1`.  This
inequality remains valid on every rank-drop locus and avoids the open-chart
gap in the provisional `GLD73` handoff.

## 5. Exhaustiveness of the projective cover

For a matrix with three columns, rank at most one has exactly three cases:

```text
Z_0!=0:             Z_1=aZ_0, Z_2=bZ_0;
Z_0=0, Z_1!=0:      Z_0=0, Z_2=bZ_1;
Z_0=Z_1=0:          no normalization parameter is needed. (6)
```

These cases include the zero matrix and every possible leading nonzero
column.  They do not assume a chosen nonzero row, divide by a polynomial in
the affine fibre parameters, or lose a projective direction.

For the first two charts, exact `liftstd` returns a unit over `Q(i)`.  This
unit identity persists after scalar extension to `C`, so the certificate
excludes complex fibre parameters rather than only `Q(i)`-rational points.
The generator checks
the full lift matrices inside Singular before serializing sparse multipliers.
The portable verifiers reconstruct the original `130` equations, including
the four identically zero positions preserved by the lift, and check

```text
sum multiplier_j * equation_j = 1                       (7)
```

as a polynomial identity over `Q(i)`.  The two certificates contain `42` and
`35` multiplier terms.  The final coordinate direction is an affine linear
system whose coefficient and augmented ranks are `35` and `36`.

Together, (6)--(7) prove `rank Z>=2` at every affine fibre point.  This is a
complete exact cover, not evidence from the exploratory `F_5` projective
enumeration or from a handful of signed directions; neither exploratory
calculation is part of the accepted proof.

## 6. Certificate provenance and independence

The affine quotient coefficient array has SHA-256

```text
17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e,
```

and the canonical LF-serialized `2744`-byte certificate has SHA-256

```text
7bb2dc47270a2c2e9b87c722aace298e63a6691a7979d86564425aac760a748f.
```

The primary route imports the owning live definitions and checks the sparse
identities with SymPy over `Q(i)`.  The audit imports neither the primary nor
any repository or third-party module.  It separately implements Gaussian
arithmetic and elimination, the four-port permanent columns, transformed
ports, matching cofactors, quotient construction, and sparse polynomial
multiplication.  It reverses the certificate variable order before replay.
This is independent checking of the proof object, not two wrappers around
one CAS answer.

## 7. Hostile attacks and rejected strengthenings

### 7.1 The pinned GLD73 rank was extrapolated across a fibre

Rejected.  Every cofactor column is recomputed as an affine function of all
`35` kernel parameters, and rank-one incidence is eliminated on the complete
affine space.

### 7.2 Only the generic rank-17 response chart was checked

Rejected.  Equation (5) uses an upper bound on full rank.  A drop in full
rank makes the diagonal response no larger; no saturation by a full-rank
minor is used.

### 7.3 A projective chart misses the all-zero or later-leading cases

Rejected.  The three cases in (6) are exhaustive in column order, and the
last case is checked without normalization.

### 7.4 A Singular unit report is being treated as the proof

Rejected.  The durable object contains explicit sparse multipliers.  Both
portable routes multiply them by independently reconstructed generators and
obtain the constant polynomial one.  Singular is needed only to regenerate
the object.

### 7.5 q0 failure proves the GLD72 tensor is globally nonintegrable

Rejected as an unsupported strengthening.  The result covers every raw
coefficient preimage only inside the fixed canonical torus-star effective
presentation.  Other points of the survivor locus, other port/root
presentations, non-star maximal profiles, and the graph/source bridge remain
outside the theorem.

### 7.6 The result is a Krenn--Gu counterexample

Rejected.  No maximum-root certification, fifth-root exclusion, or global
graph satisfying the original GHZ equations is supplied.  The theorem is an
obstruction to completing a hostile fixed-space control, not a witness.

## 8. Accepted frontier delta

Relative to `GLD73`:

1. the entire `35`-dimensional raw preimage of the exact `GLD72` tensor is
   excluded by one complete first-response test at `q_0`;
2. exceptional response-rank strata are included, rather than left as open
   determinantal charts;
3. further work on another raw preimage of the same tensor has no value;
4. the next parent task is globalization across the survivor locus or a proof
   that every relevant source presentation is forced through this interface;
5. maximum-root, fifth-root, non-star, source-coverage, and global obligations
   remain open.

This is a substantial universal-bridge advance, but not global closure.
