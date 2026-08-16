# Self-review: residual second-root-coloop exclusion

Date: 2026-08-13

## Claim reviewed

Both residual second-root coordinate-coloop orientations

```text
N subset {beta_j=0},                 j!=t,
```

are impossible on the normalized physical `m=3` common-three-space,
joint-rank-five Hilbert--Burch `(1,2,2)` stratum.

This closes two coloop orientations.  It does not close the other five
`(1,2,2)` coloops or the global conjecture.

## Load-bearing checks

### 1. The terminal face is complete

S2BI leaves `y=w=e_u`, `z_s=0`, and `z_t!=0`.  A projective direction
avoiding three points gives exact rows `beta_*` and `gamma_*` with both
`u,t` coordinates nonzero.  On the full product face, not a finite sample,
the only nonzero binary cells are

```text
(r_u,p_*,q_*) -> T_u,
(r_t,p_*,q_*) -> T_t.
```

The target tensors are fully transverse.

### 2. The two selected-colour orientations are not conflated

If `j=s`, `beta_*` is the selected-divisor row with nonzero evaluation pair;
choosing the opposite `gamma_*` gives `p_*+q_* in R`.  If `j=u`, the
selected-divisor row is instead `e_s^*` with zero evaluation pair, giving
`p_s in R`.  These are different quotient branches and produce the `9+6`
cover.

### 3. The third-plane intersection is exact

Since `z,w` form a basis of `e_s^perp`, their common annihilator is exactly
`e_s^*`; hence `q_s in R`.  Injectivity makes this row nonzero.  If `Q=R`,
permanent symmetry forces the first row of an invertible change matrix to
vanish.  Otherwise `R intersect Q=span(q_s)` in a three-space.

### 4. The 15 families are exhaustive

The nonzero line `q_s` has three supports in the ordered target basis of
`R`.  In the `j=s` branch, the vector `p_*+q_* in R` has two affine patches
plus the zero vector, giving `3*3=9`.  In the `j=u` branch, the nonzero line
`p_s in R` has two affine patches, giving `3*2=6`.  The polynomial parameter
`tau` is neither sampled nor inverted.

### 5. The certificate subsystem is necessary

Full transversality chooses the two target factor lines as selected source
coordinates.  The full binary table therefore forces 64 selected cubic
coefficients: one at `(000;000)`, one at `(111;100)`, and zero at the other
62 positions.  Unit ideal for this subsystem excludes a realization of the
full tensor equations.

### 6. Independent replay is genuinely separate

The primary verifier uses SymPy and the certificate variable order.  The
audit imports no repository module or third-party package, reverses all 26
variables, reconstructs all 15 row systems independently, expands every
permanent by a separate loop, and uses standard-library `Fraction` sparse
arithmetic.

### 7. Exploratory local-order output is not evidence

During exploration, a local monomial ordering made any polynomial with
nonzero constant term appear as a unit.  That route was explicitly rejected
and contributes nothing to the theorem.  The durable certificate consists
only of globally checked rational polynomial identities replayed directly
as `sum h_i f_i=1`.

## Exact evidence

- Certificate cases: `15`.
- Sparse multiplier terms: `32,871`.
- Certificate SHA-256:
  `bc63359ece10e7d12237ab5821f64227de8391b5a9422091d9b5c0591484a7a0`.
- Primary SymPy replay: passed.
- Independent no-import rational replay: passed.
- Deterministic Singular 4.3.2 regeneration: byte-for-byte passed.

## Scope boundary

The three third-root and two complementary first-root `(1,2,2)` coloops,
joint rank at most four, other physical components and pole strata, higher
orders, and the global conjecture remain open.  The global status remains
**UNRESOLVED**.
