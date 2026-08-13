# Self-review of the `m=3` common-three-space component trichotomy

## Review target

This review covers the theorem, primary replay, and independent audit for
the common-three-space annihilator-component trichotomy.

## Hostile checks

### Does projective dimension apply componentwise?

Yes.  The Segre variety has dimension six and the annihilator linear space
has codimension three.  The projective dimension theorem gives dimension at
least three for every irreducible component of their nonempty intersection,
not merely for the union.

### Why must one coordinate divisor contain an entire component?

S2R places the section in a finite union of nine closed coordinate divisors.
An irreducible variety contained in a finite union of closed subsets is
contained in one of them.  No choice is made point by point.

### Is a generic binary statement promoted correctly to the closure?

Yes.  On a component contained in exactly one coordinate divisor and with
`beta` not identically zero, the points with exactly two surviving colours
and `beta!=0` form a dense open subset.  S2S makes the missing-colour cross
contractions zero there.  Those contractions are fixed linear equations in
each projective factor, so their vanishing extends to the component closure.

### Is the rank budget off by a projective dimension?

No.  A cross-column span of rank `r_i` has annihilator vector dimension
`3-r_i` and projective dimension `2-r_i`.  The selected coordinate equation
subtracts one more dimension exactly when it is independent.  Thus the
ambient dimension is `6-sum r_i-epsilon`; comparison with `dim Z>=3` gives
`sum r_i<=3-epsilon`.

### When is the selected coordinate equation redundant?

It is redundant on `K_(j,d)=C_(j,d)^perp` exactly when
`K_(j,d) subset e_(j,d)^perp`.  Double annihilation makes this equivalent to
`e_(j,d) in C_(j,d)`.  The theorem states both alternatives explicitly.

### Does the trichotomy exclude its branches?

No.  Multi-boundary components, identically zero `beta`, and collapsed
missing-colour spans all remain open physical cases.  The target diagonal
plane demonstrates the need for the first geometric branch but is expressly
not a physical full sensor.

## Evidence independence

The primary uses SymPy subspace calculations.  The audit imports no SymPy or
repository code; it implements exact `Fraction` row reduction and rebuilds
the sharp coordinate configurations separately.  The scripts audit the
linear arithmetic.  Projective dimension, irreducibility, density, and the
case cover are proved in the theorem text.

## Status verdict

```text
component dimension at least three:                  PROVED;
multi-boundary / beta-zero / collapsed-column cover: PROVED;
rank budget three, or two when independent:          PROVED;
exclusion of any of the three component types:       OPEN;
common-three-space S2Q stratum:                      OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
