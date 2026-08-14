# Self-review: joint-rank-four derivative-rank-eight target-kernel atlas and distinct-missing-colour exclusion

Date: 2026-08-13

## Claim reviewed

The reviewed claim is deliberately local.  On the physical `m=3`
common-three-space cell with joint cross rank four, all three root blocks
nonzero, and shared-derivative rank eight, it proves:

1. each transposed root-row map has rank at least two;
2. every rank-two first/second row has one coordinate kernel and a matching
   nonzero diagonal row/column of the residual block `C`;
3. every rank-two third row has a one-/two-colour kernel represented by the
   shared tangent factors and nonvanishing on `w`;
4. if both first and second rows have rank two, distinct missing colours are
   impossible; and
5. the same-colour survivor has the isolated block form and third-projection
   incidence displayed in the theorem.

It does not claim to exclude the complete derivative-rank-eight cell, any
rank-seven cell, the joint-rank-three analogue, or the pair layer.

## Load-bearing checks

- S2BQ gives `K=D^(-1)(U)` and `ker D=span((x,y,0))` at joint rank four.
  The proof uses both facts.  It is not silently transferred to joint rank
  three.
- A row-kernel covector annihilates the corresponding projection of every
  element of `K`.  For the first and second roots this also kills `x` or
  `y`, because `(x,y,0) in K`.
- The six-term empty permanent is multilinear in each transposed root row.
  Hence a row-kernel covector kills the complete empty contraction, not just
  a sampled slice.
- The target comparison is coefficientwise in a source tensor basis
  containing `T_0,T_1,T_2`.  Different target monomials are never merged.
- In the distinct-colour contradiction, the third component of a preimage
  of `u_d` is independent of the chosen preimage because the derivative
  kernel has zero third component.
- The second contraction in the contradiction cannot cancel: its only
  surviving term is a nonzero scalar multiple of `e_e tensor e_d`.
- The third-root tangent membership test is tensorial.  It is the quotient
  identity `(e_s mod Kx) tensor (e_s mod Ky)=0`, not a coordinate scan.
- The bound `rank theta>=2` uses the nonvanishing of evaluation at `w` on
  every nonzero kernel vector; a two-dimensional kernel would necessarily
  contain a nonzero vector in the kernel of that evaluation.

## Falsification attempts

1. **Let the first-row kernel have two colours.**  Then two distinct
   diagonal target coefficients would have to use the same fixed second-root
   factor `(alpha tensor id)C`; this is impossible.
2. **Let a third-row kernel vector annihilate `w`.**  Its contraction kills
   all of `U`, while its nonzero diagonal target contraction remains.
3. **Use different first/second missing colours and absorb the contradiction
   in another derivative summand.**  Both tangent summands are killed by the
   deficient second row.  The forced `C` column leaves the uncancellable
   tensor `e_e tensor e_d`.
4. **Change the preimage by the derivative syzygy.**  This changes only the
   first two components and leaves the forced third component unchanged.
5. **Set a diagonal contraction scalar to zero.**  The matching target
   coefficient then has no possible correction, so the scalar is forced
   nonzero.
6. **Promote the same-colour conditions to existence.**  The theorem and
   frontier explicitly retain that cell as open; the exact fixtures in the
   replays validate derivative algebra only and are not labelled physical
   incidences.

No falsification attempt invalidated the stated local conclusion.

## Computational evidence and independence

The primary SymPy replay constructs dense `27 x 9` derivative matrices,
checks the symbolic contractions, tests the tangent quotient criterion,
and replays all six ordered distinct-colour contradictions.  The independent
audit imports no repository or third-party module.  It uses standard-library
`Fraction`, reverses tensor flattening order, implements its own elimination,
and reconstructs the same identities from dictionaries rather than SymPy
arrays.

The scripts replay displayed algebra and canonical exact models.  The
arbitrary-covector and coefficientwise arguments in the theorem are the
proof; the scripts are not presented as an exhaustive search over physical
shores.

## Status decision

The local row-kernel atlas and distinct-missing-colour exclusion are suitable
for `verified` status after the focused commands and repository validation
pass.  The broader lower-rank three-root branch and the global Krenn--Gu
conjecture remain **UNRESOLVED**.
