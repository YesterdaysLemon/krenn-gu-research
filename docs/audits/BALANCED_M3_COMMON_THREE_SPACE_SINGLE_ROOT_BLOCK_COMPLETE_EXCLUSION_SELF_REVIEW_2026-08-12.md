# Self-review: balanced `m=3` single-root-block complete exclusion

Date: 2026-08-12

## Claimed advance

The theorem excludes exactly one nonzero root--root block on the entire
common-three-space stratum, without a joint-rank assumption.  Together with
the already committed rank-nine/eight/seven results, every survivor has at
least two root blocks and joint rank at most six.  No multi-root rank-six
case or other physical component is claimed.  Global Krenn--Gu remains
**UNRESOLVED**.

## Load-bearing checks

1. With one root block, singleton dimension three makes the opposite root
   block row rank three.  Full-sensor rank makes each source projection
   nonzero; otherwise one singleton sensor column vanishes.
2. The torus and off-diagonal globalization arguments used to obtain one
   diagonal coordinate root edge do not require joint rank nine.  Their
   scopes were checked in S2U and again in S2Z.
3. The exceptional derivative chart is excluded by two independent
   rank-one GHZ coefficient covectors, not by a total-rank count.  The
   regular chart is the only place where off-diagonal derivative zeros are
   promoted to zero quadratic triples.
4. The proof that `p_s=q_s=0` uses nonzero diagonal products.  A common zero
   divisor of the other two marked rows makes them either pure in the same
   source or proportional mixed rows; the crossed zero then kills a required
   diagonal.
5. Nonzero zero-product pairs are exhaustively pure or conjugate mixed.
   Pure pairs are allowed to be one-dimensional; the proof does not import
   the rank-four complementarity used by S2Z.
6. In the all-three-source `P/M` case, a one-dimensional pure pair would
   already make the two target tensors share their pure-source factor.  The
   remaining two-dimensional case is exactly the two-kernel-line argument.
7. Same-source-pair `M/M` products are proportional for arbitrary nonzero
   rescalings.  Different-pair `M/M` has two genuinely different branches:
   independent shared-source lines give an injective derivative pair, while
   proportional lines give a seven-dimensional Segre tangent image.
8. The tangent rank-one lemma is projective and arbitrary-dimensional in
   the three factors.  Three quotient projections force a decomposable
   tangent tensor to share at least two base factor lines.  Two different
   GHZ colours cannot both do so because their corresponding factor lines
   are distinct in every mode.
9. Characteristic different from two is load-bearing for conjugate mixed
   lines, sum/difference separation, and distinct kernel lines.  The theorem
   is stated only in characteristic zero.

## Computational evidence boundary

The primary verifier instantiates seven exact controls covering the six
geometric families (including a pure-line boundary), reconstructs their pair
products and derivatives, and checks ranks `9`, `8`, and tangent-image `7`
on the three different `M/M` boundaries.  The no-import audit rebuilds these
maps with `Fraction` arithmetic and separately checks the Boolean content of
the tangent-ruling lemma.  The written pure-or-mixed classification and
arbitrary-vector arguments are the proof.

## Remaining boundary

Every surviving common-three-space point now has at least two nonzero root
blocks and joint rank at most six.  At rank six the shared derivative can
have rank five with only a three-dimensional intersection between its
four-dimensional kernel and `image H`, or rank six with its whole
three-dimensional kernel contained in `image H`.  Those are distinct next
mechanisms.  The theorem does not infer anything about the other S2T
component types or the other S2Q pole strata.
