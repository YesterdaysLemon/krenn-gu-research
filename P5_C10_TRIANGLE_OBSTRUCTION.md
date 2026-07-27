# A four-equation triangle obstruction in 113 additional `C10` orbits

## Status

This is an exact finite theorem inside the `P_5` exact-three-coordinate,
exact-three-partial `C10` boundary.  It excludes 113 support-semantic
survivor orbits not covered by the three-equation binary-fork rule.
Together the fork and triangle rules exclude 1,441 of the 11,751
independently audited `C10` orbits.

It does **not** exclude the remaining 10,310 `C10` orbits, close the
other `P_5` branches, or prove the global Krenn--Gu conjecture.

## The local identity

Let `P,X,Y,Z` be four forbidden mixed-colour coefficient polynomials.
Suppose that, after the standard spanning-tree gauge, they have the
form

```text
P = 1 + m*A,
X = A + B,
Y = A + C,
Z = B + C,
```

where `m` is a squarefree monomial; `m=1` is allowed.  Then

```text
2*P - m*X - m*Y + m*Z = 2.
```

All four mixed coefficients would have to vanish in a monochromatic
restriction, giving `0=2`.  Thus no common affine zero exists over
characteristic zero.

This argument uses neither the Laurent saturation equation nor a
nonzero assumption on a pure-colour amplitude.  It is a direct
four-equation obstruction.

## Complete finite scan

An integer-bitmask generator independently reconstructs every
normalized mixed coefficient in the packaged 11,751-orbit `C10`
catalogue.  For each possible `P`, it tests every common monomial
divisor and every coefficientwise decomposition of `X` and `Y`.  The
complete counts are

```text
  604 triangle obstructions in total,
  491 already covered by the binary fork,
  113 new triangle obstructions,
1,441 orbits in the union,
10,310 cases not decided by either rule.
```

For all 113 new hits, a second path calls the repository's original
exact polynomial generator, parses the four selected polynomials with
SymPy, checks that the two generators agree term for term, and
symbolically replays `2P-mX-mY+mZ=2`.  The ordered new-hit list has
SHA-256

```text
28feb91d7eaaacafa9bf16967af37d1f1f3a402738d42c37c27777e33b7c3bb3.
```

Run the complete fork and triangle replays with:

```text
PYTHONPATH=tmp/python_deps python \
  verify_p5_c10_binary_fork_obstruction.py
PYTHONPATH=tmp/python_deps python \
  verify_p5_c10_triangle_obstruction.py
```

## Structural meaning

The triangle is the next sparse constant certificate after the binary
fork.  The two rules already replace 1,441 large Gröbner calculations
by identities involving at most four forbidden coefficients.

The next search should enumerate general short monomial-linear
relations among sparse coefficient vectors.  The finite scan can then
learn candidate identities, while a separate exact replay certifies
every reported orbit.
