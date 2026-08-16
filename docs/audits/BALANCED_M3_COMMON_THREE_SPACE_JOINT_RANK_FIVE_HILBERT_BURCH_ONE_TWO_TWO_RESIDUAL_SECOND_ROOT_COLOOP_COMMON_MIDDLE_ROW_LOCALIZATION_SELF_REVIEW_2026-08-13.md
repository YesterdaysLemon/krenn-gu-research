# Self-review: residual second-root-coloop common-middle-row localization

Date: 2026-08-13

## Claim reviewed

On the normalized physical `m=3` common-three-space, joint-rank-five
Hilbert--Burch `(1,2,2)` stratum, every surviving residual `beta_j` coloop
endpoint is localized from

```text
s in {j,k},       y proportional to e_u,
w in {e_s,e_u}
```

to

```text
w=e_u,            z_s=0,            z_t!=0.
```

This is not an endpoint exclusion and not a global resolution.

## Load-bearing checks

### 1. The escaping plane is not silently put inside the common space

S2BF supplies only a nonzero line of `p(P_delta)` in the at-most-three-space;
it does not put the full middle plane there.  The new lemma assumes exactly
`P intersect S!=0`.  Its row-space cover treats all three possibilities for
the intersection line relative to `(p_0,p_1)`: the active row, the zero row,
or a genuinely non-coordinate combination.  Only the separate `P subset S`
case invokes the older all-in-space obstruction.

### 2. The first/third-plane incidence cover is exhaustive

If the two planes agree, permanent symmetry forces their indexed bases to
align; this is the tenth plane case.  If they differ, their intersection
line has one of three supports in each ordered plane.  Nonzero row rescaling
normalizes the coefficients, giving exactly nine cases.  No claim that the
intersection is a target-indexed row is made.

### 3. The line parameter is not sampled

The nonzero vector spanning `P intersect S` is covered by the three affine
patches

```text
(1,tau,sigma),       (0,1,tau),       (0,0,1).
```

The first two certificate families are polynomial in the displayed
parameters.  They use no inverse, saturation, finite sample, or generic-point
promotion.

### 4. The 64 equations are necessary

Full transversality lets the factor lines of the two target tensors be the
first two lines of source-coordinate bases.  Tensor equality at all eight
binary row cells therefore forces the eight selected source coefficients at
each cell.  Only `(000;000)` and `(111;101)` are one after target scaling;
the other 62 coefficients are zero.  A unit ideal for this subsystem is a
valid obstruction to the full tensor equations.

### 5. Independent certificate replay is genuinely separate

The primary verifier uses SymPy and the certificate variable order.  The
audit imports no repository module or third-party package, reverses all 26
variables, independently builds the 90 row systems and polarized permanents,
and uses standard-library `Fraction` sparse arithmetic.  Both reconstruct
the 64 generators rather than trusting stored generator lists.

### 6. The projective direction exists over every characteristic-zero field

When `L_Q=kappa z_s-hw_s` is nonzero, the excluded directions are its sole
projective zero and the two coordinate directions.  A characteristic-zero
field is infinite, so another direction exists.  At that direction the
second-root row has both active coordinates and the third-root plane has
exact coordinate lifts.

### 7. The terminal conclusion uses both endpoint alternatives

The common-middle-row contradiction forces `z_s=w_s=0`.  The endpoint
`w=e_s` has `w_s!=0`, so only `w=e_u` survives.  Independence of `z,w` then
forces `z_t!=0`; no normalization of `z_u` is claimed.

## Exact evidence

- Certificate cases: `90`.
- Sparse multiplier terms: `31,591`.
- Certificate SHA-256:
  `a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1`.
- Primary SymPy replay: passed.
- Independent no-import rational replay: passed.
- Deterministic Singular 4.3.2 regeneration: byte-for-byte passed.

## Scope boundary

The terminal `w=e_u,z_s=0,z_t!=0` chart remains open, as do the other five
`(1,2,2)` coloop orientations, lower joint rank, other physical components
and pole strata, higher orders, and the global conjecture.  The correct
global status is **UNRESOLVED**.
