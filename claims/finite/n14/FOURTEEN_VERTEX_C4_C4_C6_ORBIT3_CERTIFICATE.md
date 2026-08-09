# Order-14 `C4+C4+C6` first-factor orbit-3 certificate

## Scope

This is a finite computer-assisted theorem for one first-factor orbit in
the order-14 `C4+C4+C6` equality architecture.  It is not a proof of the
full family or of the Krenn--Gu conjecture.

No support exists whose pinned first singleton perfect matching belongs
to census orbit 3.

## Connectivity prerequisite

The Krenn--Gu conjecture is known for skeletons of vertex connectivity at
most two.  The global formula therefore includes the necessary condition
that deleting any set of at most two vertices leaves the skeleton
connected.

For all 93 pinned first-factor orbits, an independent implementation
reconstructs every fixed-component quotient after each of the 106
possible deleted-vertex sets.  It matches all 2,576 new quotient-cut
clauses and the exact DIMACS sequence.  The resulting formula remains
SAT before the orbit-3 rules and selector are imposed.

## Minimum-activity reconstruction

A targeted structural search produced 272 independently audited
minimum-activity certificates for orbit 3.  Independent symmetry
transport reconstructs exactly 5,856 new clauses.

The resulting 324-variable, 960,540-clause global CNF has SHA-256

```text
dc1f8054ee1dfd3dec3b17c43ce7862f165aab52f00c944adf6aba4f1a1ad839
```

It remains SAT until the orbit-3 selector is imposed.

## Conditioned UNSAT proof

Appending DIMACS selector 235 gives a 960,541-clause conditioned CNF
with SHA-256

```text
d1bf8e88de55ac9bc693b69f657f1537def9cd88fd682b46589586213e3a32e8
```

Kissat generated a 56,073,606-byte DRAT proof with SHA-256

```text
50c9bac8a98b556d0472f9bd4e0ee4f94e29a366e96c263eeee7b2d4ec70cb7c
```

The independent `drat-trim` checker returned `s VERIFIED`.

## Independent algebraic cross-check

One support encountered during the orbit search also has a much smaller
obstruction.  Four graph-derived dual-Horn clauses force one cycle
binomial cancellation.  Under that cancellation, a five-term target
amplitude reduces in the exact integer relation lattice to signed class
coefficients

```text
0, 0, 1
```

and hence has one uncancelled Laurent monomial class.  The independent
verifier reconstructs all 864 reported factor relations from their graph
equations, the four core clauses, the target activity, the one-relation
lattice basis, and the final SAT contradiction:

```text
python claims/finite/n14/verify_fourteen_vertex_unforced_factor_choice_core.py
```

This compact witness concerns one fixed support; the global orbit theorem
comes from the reconstructed CNF and DRAT proof above.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit3.py
```

The final audit is
`tmp/fourteen_vertex_c4_c4_c6_orbit3_final_verified.json` and contains
`"verified": true`.

## Boundary

This excludes one pinned first-factor orbit in the remaining
`C4+C4+C6` family.  Other open selectors and the global conjecture remain
unresolved.
