# A three-equation binary-fork obstruction in 1,328 `C10` orbits

## Status

This is an exact finite theorem inside the `P_5` exact-three-coordinate,
exact-three-partial `C10` boundary.  It excludes 1,328 of the 11,751
independently audited support-semantic survivor orbits.

It does **not** exclude the remaining 10,423 `C10` orbits, close the
other `P_5` branches, or prove the global Krenn--Gu conjecture.

## The local identity

Let `P,Q,R` be three forbidden mixed-colour coefficient polynomials.
Suppose that, after the standard spanning-tree gauge, they have the
form

```text
P = 1 + m*A,
Q = 1 + m*B,
R = A + B,
```

where `m` is a squarefree monomial; `m=1` is allowed.  Then

```text
P + Q - m*R = 2.
```

All three mixed coefficients would have to vanish in a monochromatic
restriction, giving `0=2`.  Thus no common affine zero exists over
characteristic zero.

This argument uses neither the Laurent saturation equation nor a
nonzero assumption on a pure-colour amplitude.  It is a direct
three-equation obstruction.

## Complete finite scan

An integer-bitmask generator independently reconstructs every
normalized mixed coefficient in the packaged 11,751-orbit `C10`
catalogue.  For each constant-containing coefficient it tests every
common monomial divisor of its nonconstant terms, so the search is
exhaustive for the displayed pattern.  It finds exactly

```text
1,328 binary-fork affine obstructions,
10,423 cases not decided by this rule.
```

For all 1,328 hits, a second path calls the repository's original exact
polynomial generator, parses the three selected polynomials with SymPy,
checks that the two generators agree term for term, and symbolically
replays `P+Q-mR=2`.  The ordered hit list has SHA-256

```text
05436f68e3c7377ca4ee05245cc93923e849b9ef86c92d64e2de180c2f6363b8.
```

Run the complete replay with:

```text
PYTHONPATH=tmp/python_deps python \
  verify_p5_c10_binary_fork_obstruction.py
```

## Structural meaning

The large Gröbner systems are not uniformly unrelated.  At least 1,328
support orbits contain the same abstract cancellation fork, even though
the actual monomials `A`, `B`, and `m` vary.  This is the first
human-scale obstruction template with substantial coverage of the
exact-three `C10` catalogue.

The next search should look for slightly larger constant certificates,
for example four-polynomial triangles or short monomial-linear
relations.  Those identities can be found over sparse exponent vectors
before invoking Gröbner bases and can be replayed against the original
generator exactly as above.
