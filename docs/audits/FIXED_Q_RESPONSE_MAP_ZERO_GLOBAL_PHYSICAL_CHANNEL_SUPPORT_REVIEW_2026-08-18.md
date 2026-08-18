# Fixed-Q response-map-zero global physical-channel support hostile review -- 2026-08-18

## Verdict

**Accepted at the frozen theorem and script hashes below.**  No P0, P1, or
P2 defect remains.  The package proves an exact characteristic-zero global
common-shore support classification on the `GLD19` response-map-zero locus,
an exhaustive finite raw-support atlas, and a conditional full-witness
reduction to complementary `GLD15` pure absorption.  It does not exclude the
support atlas, force a legal complete-nuisance operator row, integrate a
response window into a witness, or imply a permanent restriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Global common-shore classification

For each port `u` and colour `c`, the corrected channel is represented by a
two-dimensional shore vector `v_u^c`, with

```text
K_uv(c,d)=q(v_u^c,v_v^d)
```

for the nondegenerate hyperbolic form `q`.  Pair diagonality makes shore
vectors of different colours orthogonal across distinct ports.  The hostile
review checked all common-edge and distinct-edge cases in the resulting
line argument.  Three corrected-active colours would force either three
pairwise orthogonal nonisotropic lines in a two-space, a nonisotropic line
orthogonal to itself, or a rank-three diagonal pair block.  All are
impossible.

With one corrected-active colour, its nonempty edge-support graph is any
labelled four-vertex graph except `P_4`.  The path is excluded by successive
orthogonal-line constraints, while nine rational unlabeled fixtures realize
all other nonempty graph types.  The empty graph belongs only to the separate
zero-channel case.  With two active colours, each support graph is a clique
on at least two participating vertices.  The proof explicitly handles an
additional edge coinciding with the other colour's chosen edge through the
two same-edge off-diagonal zeros.  Orthogonal rational shore lines realize
every ordered pair of clique supports.

These are arbitrary-field written arguments; the finite programs audit their
rational fixtures and ledgers but do not replace the proofs.

## Exact support atlas and full-capable family

The classification gives exactly

```text
1+3*51+3*11^2=517
```

labelled corrected-channel support triples.  Combining this atlas with the
three exhaustive `GLD19` complementary support alternatives gives exactly
`467715` labelled raw `(B,K)` support patterns.  The primary uses a
matchingwise dynamic count; the independent audit uses direct recursive
product enumeration.  Both reproduce every entry of the displayed
active-colour/full-family table.  These are response-window support counts,
not a witness enumeration or a fibre count.

For arbitrary residual scalar `h`, the projective change

```text
(alpha,beta) -> (alpha+h beta,beta)
```

is invertible.  Over the infinite characteristic-zero field, finite
projective avoidance therefore proves that an edge admits a three-full row
exactly when its raw `B/K` support union contains all three colours.  The
review checked that this row need not be legal: the theorem replays
`GLD19`'s common-shore opposite-annihilation proof using response-window data
only.  The resulting full-capable family is intersecting and hence is empty,
one edge, two adjacent edges, a three-edge star, or a triangle.  The maximal
star/triangle table consistently records sorted support-size profiles.

## Conditional full-witness reduction

Only after returning to the complete fixed-`Q` witness quotient does an
opposite raw-zero pair become a `GLD15` pure-absorption target.  With
`M_f=Z_f=0`, independence of the three pure port words and nonvanishing of
the fully supported contraction coefficients force all three pure target
classes to vanish, so `q_f=0`.  A maximal star or triangle therefore forces
three simultaneous complementary pure-rank-zero targets.

This conclusion does not make the desired companion classes zero, determine
the operator rank, or exclude the target.  In particular, the allowed
`q_f=0,r_f=0,k_f=2` branch is preserved.

## Controls and independent checks

Exact physical controls attain maximal stars, maximal triangles, the
normalized three-colour `K=0` cell, a dense two-colour channel, the dense
two-colour triangle profile, and the two-colour star profile.  They have
literal all-seven response-map zero for arbitrary `h` where claimed, but are
response windows rather than witnesses or counterexamples.  Formal `P_4`
and three-colour-star blocks satisfy the edgewise diagonal/rank and response
support equations but fail the common-shore classification, showing that
physical shore compatibility is load-bearing.

The primary exact replay uses SymPy rational shores, complete four-port word
enumeration, a dynamic support count, tensor controls, and pure-absorption
linear algebra.  The no-import audit imports neither SymPy nor the primary;
it uses standard-library `Fraction`, a separately implemented bilinear form,
recursive raw-support enumeration, sparse response tensors, and independent
rational rank elimination.  Both focused scripts pass, as do Ruff check,
Ruff format-check, and the predecessor `GLD15`, `GLD18`, and `GLD19`
primary/audit pairs.

Frozen at base HEAD `01d0b107884524677726673c221b3a45740c6b24`:

```text
theorem  b1a8f81623aacea0f1a1a9ca2b6015c4c7b9bc0787a23063690dc481da35bf4e
primary  2758c4de6abe4f4e8cef72d758970e7d64de5e9ce5fa7d7064416068ca9a9792
audit    f46c7f6171faeb413596b989696504ebb31d7a10fff353e1b7f06d9bece6cc0d
```

## Exact remainder

Still **UNKNOWN**: excluding the `254995`-pattern no-full-capable cell;
excluding one to three simultaneous pure-absorption targets; forcing a
nonzero legal complete-nuisance operator package; using genuinely
uncontracted same-graph mixed coefficients to integrate or exclude the
response window; cross-window activity; and every weighted-permanent
consequence.
