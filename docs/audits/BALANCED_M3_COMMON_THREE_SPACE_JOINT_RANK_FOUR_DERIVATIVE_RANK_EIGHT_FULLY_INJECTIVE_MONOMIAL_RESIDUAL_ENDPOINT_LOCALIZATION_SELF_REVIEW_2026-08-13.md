# Self-review: fully-injective monomial-residual endpoint localization

Date: 2026-08-13

## Claim reviewed

The reviewed claim is deliberately local.  In the last `(3,3,3)` row
profile of the physical `m=3` common-three-space joint-rank-four,
derivative-rank-eight chart, assume the residual block is

```text
C=lambda e_d tensor e_e.
```

The theorem proves the necessary endpoint equations `w_d=w_e=0`.  It
excludes the monomial cell away from that endpoint; it does not exclude the
endpoint, a nonmonomial residual block, another derivative cell, another
pole stratum, a higher order, or all-rank drop.

## Load-bearing checks

- Injectivity of the third root row and `dim K=4` make
  `ker(pr_3|K)` one-dimensional.  The shared derivative syzygy already lies
  in this kernel, so equality is justified and the three graph lifts give a
  basis of `U` after applying `D`.
- The source tensors `S_c` come from the complete coefficientwise empty
  target identity.  They are not selected target coefficients or a sampled
  source specialization.
- For `gamma(w)=0`, contraction of every graph generator kills both tangent
  terms and leaves exactly `gamma_c C`.  This proves the whole slice identity
  (6) in the theorem.
- If `w_d!=0`, the coordinate restriction from `w^perp` to the two colours
  complementary to `d` is an isomorphism.  This is an exact determinant
  statement, not a generic choice.
- A monomial `C=e_d tensor e_e` has every row complementary to `d` equal to
  zero.  Hence the selected slice is a complete binary diagonal table, and
  the injective row `p_d` is a common zero for every entry of that table.
- The four-space common-zero lemma uses S2BF only in its proved scope.  Any
  intersection between two binary row planes puts those two planes in a
  three-space which the third plane must meet.  Permanent symmetry supplies
  the required ordering of the S2BF outer and middle planes.
- Every shifted middle plane remains two-dimensional because the common-zero
  vector lies outside the original middle plane.  Multilinearity preserves
  all eight binary entries.
- The two dimension intersections with `P+span(v)` force `v` into both outer
  planes; this contradicts their already established transversality.
- Root exchange sends `e_d tensor e_e` to `e_e tensor e_d` and leaves `w` in
  the shared third root, so the second endpoint equation is exactly `w_e=0`.
- The final statements for `d=e` and `d!=e` are elementary consequences of
  the dimension of the simultaneous coordinate kernel.  They are not
  existence assertions.

## Falsification attempts

1. **Let the binary coordinate restriction lose rank.**  Its determinant is
   a nonzero scalar multiple of `w_d^2`; this is precisely the retained
   endpoint `w_d=0`, not an overlooked chart.
2. **Absorb the unused row into the binary middle plane.**  The binary table
   itself makes any common-zero vector already in that plane equal to zero.
3. **Choose a shift that collapses the middle basis.**  Independence modulo
   the original plane rules this out for every pair of shift scalars.
4. **Allow the binary row planes to intersect.**  The independently audited
   S2BF obstruction excludes every such incidence in a four-space.
5. **Use a nonzero monomial correction on a complementary row.**  There is no
   such coefficient: every row other than row `d` of `C` is identically zero.
6. **Infer `w=0` when `d=e`.**  Only one coordinate vanishes in that case;
   the theorem correctly retains the complementary two-plane.
7. **Promote numerical endpoint searches.**  Exploratory numerical behavior
   was not used in the theorem, verifier, audit, frontier, or status decision.

No falsification attempt invalidated the stated localization.

## Computational evidence and independence

The primary SymPy replay reconstructs the dense derivative contraction in
the primary tensor ordering, checks denominator-free bases of every
`w_d!=0` chart, enumerates all nine ordered monomial supports and both root
orientations, and replays the common-zero shift algebra and endpoint
dimensions.

The independent audit imports no repository or third-party module.  It uses
standard-library `Fraction`, reverses tensor flattening order, implements its
own Gaussian elimination, checks a separate dense rational derivative
fixture, enumerates the same nine supports from a different coordinate
construction, and reconstructs the shift and quotient calculations.

The programs replay displayed algebra.  The arbitrary-subspace dimension
argument and the inherited S2BF theorem are the proof.

## Status decision

The off-endpoint monomial exclusion and endpoint localization are suitable
for `verified` status after the focused commands and repository validation
pass.  The sharp monomial endpoints, nonmonomial `(3,3,3)` cells, the wider
proof frontier, and the global Krenn--Gu conjecture remain **UNRESOLVED**.
