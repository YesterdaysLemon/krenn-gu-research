# Rational scalar-span obstructions in 1,523 `C10` orbits

## Status

This is an exact finite theorem inside the `P_5` exact-three-coordinate,
exact-three-partial `C10` boundary.  A rational scalar combination of
forbidden mixed-colour coefficients equals `1` in 1,523 of the 11,751
independently audited support-semantic survivor orbits.

Of those, 1,348 were already covered by the binary-fork, triangle, or
five-cycle rules.  The scalar-span theorem adds 175 exact orbits, so the
four-rule union excludes 1,690 orbits and leaves 10,061 undecided by
these rules.

It does **not** close the remaining `C10` cases, the other `P_5`
branches, or the global Krenn--Gu conjecture.

## The certificate space

Let `F0,...,Fr` be all normalized forbidden mixed-colour coefficient
polynomials for one exact support.  A scalar certificate is a rational
identity

```text
q0*F0 + ... + qr*Fr = 1.
```

If every forbidden coefficient vanished, the left side would be zero.
Thus the identity is an immediate affine contradiction.

This is complementary to the named sparse templates, not a superset of
them.  The fork, triangle, and odd-cycle identities generally use a
variable monomial multiplier, whereas the coefficients `q_i` here are
rational constants.  The two searches overlap on 1,348 orbits, and the
scalar search also captures relations with no useful cycle
decomposition.

## Exact finite scan

The verifier independently reconstructs each mixed coefficient as a
sparse integer vector indexed by squarefree monomials.  Sparse Gaussian
elimination modulo `1,000,003` is used only to discover a candidate
linear combination.  Wang rational reconstruction then lifts every
candidate, and direct rational arithmetic checks the identity over
characteristic zero.

All 1,523 modular hits reconstruct exactly; none is a modular-only
accident.  A modular miss is not used as a proof of rational
non-membership, so 1,523 is a certified lower bound rather than a
completeness claim for the scalar-certificate space.  Certificate
supports and maximum denominators are:

```text
support size 3:  1,143       denominator 1:    2
support size 4:    135       denominator 2: 1,513
support size 5:    121       denominator 4:    8
support size 6:     57
support size 7:     44
support size 8:     10
support size 9:     11
support size 10:     2
```

For the 175 genuinely new orbits, a second path calls the repository's
original exact polynomial generator, checks every selected polynomial
term for term, and symbolically replays the rational identity.  The
complete ordered certificate list has SHA-256

```text
a2fdf4bc3478df94d5b09d68b4df195ebcc400164e47c5ed1b3db3aad12016ee.
```

Run:

```text
python \
  verify_p5_c10_scalar_span_obstruction.py
```

## Structural meaning

The useful transformed problem is linear algebra on the monomial
coefficient vectors, not graph geometry alone.  This pass proves that
at least 1,523 apparently large polynomial systems contain a
degree-zero Nullstellensatz certificate.

The remaining systems require monomial multipliers, nonlinear
certificates, or Laurent saturation.  The next exact layer is therefore
a degree-one Macaulay span: include `u_j*F_i` columns, search for the
constant vector, reconstruct rational certificates, and replay every
new hit against the original generator.
