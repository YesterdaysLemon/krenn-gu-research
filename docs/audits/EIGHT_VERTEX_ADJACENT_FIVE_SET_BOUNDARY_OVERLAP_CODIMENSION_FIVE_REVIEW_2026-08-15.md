# Hostile review of the adjacent five-set boundary-overlap theorem

## Verdict and provenance

**PASS, as an exact codimension-at-least-five necessary incidence envelope
for one labelled adjacent pair of five-sets at eight vertices.**

This was an automated adversarial review, not an independent human peer
review.  The root agent derived the overlap stratification.  A separate
attack scout reconstructed the dimension formula and searched the current
tree for a predecessor.  A hostile-referee agent then re-derived every
stratum, wrote an independent exhaustive enumeration, checked projective and
affine closure, and required three wording/type corrections before accepting
the theorem.

The reviewed theorem SHA-256 is

```text
93d3bd6a09fa87ebc8384fa8831c9cd0c3b5ae1ea61ca5f6cb2f340f34052adf
```

The accepted claim is a strict overlap gain from the predecessor's
single-five-set codimension-at-least-three envelope to an
adjacent-pair codimension-at-least-five envelope.  It does not exclude the
envelope.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported witness input is unchanged

The successor does not re-prove or strengthen the matching-slice theorem.
For each of the two five-sets it imports exactly:

1. nonemptiness of the ten-edge five-root zero scheme; and
2. the full three-colour anchored-slice conclusion that every selected root
   has at least one zero coordinate in each target colour.

The second input uses the complete mixed slices, not pure normalization.
Choosing one zero vertex for each colour gives one of `120` nonconstant
selectors on each five-set.  Selector nonuniqueness is harmless because the
theorem takes a finite union over all choices.

## 2. Exact synchronization, not an at-least condition

Let the five-sets share `A` with `|A|=4`.  The proof stratifies by the exact
set

```text
R={i in A:[x_i]=[y_i]}.
```

This is load-bearing.  A closed condition saying only that synchronization
holds on a chosen subset also contains points with additional synchronized
vertices.  On those points more pairs of common-edge evaluations become
dependent, so using the smaller subset's fibre rank would be wrong.

The exact strata are locally closed and finite in number.  Bounding each one
bounds the dimension of the complete closed incidence before proper
projection.

## 3. The synchronization cost is correct

For a common vertex `i`, let `F_i` and `G_i` be the target coordinates killed
by the two selectors.  The two coordinate root factors have dimensions
`2-|F_i|` and `2-|G_i|`.  Their projective diagonal is empty when
`F_i union G_i` is all three colours; otherwise it has dimension
`2-|F_i union G_i|`.  Hence synchronization costs

```text
delta_i=2-|F_i intersection G_i|.
```

For `r=|R|`, put

```text
a_R=sum_(i in R)|F_i intersection G_i|.
```

Then `delta_R=2r-a_R`.  Each colour contributes to `a_R` at most once, so
`a_R<=3`; for `r=1`, nonconstancy improves this to `a_R<=2`.

The primary checked these dimensions by exact SymPy ranks of coordinate
subspaces.  The no-import audit encoded the same data as three-bit masks.

## 4. Common-edge constraint ranks are correct

The eight outer blocks each receive one nonzero evaluation equation.  A
common `K_4` block receives evaluations at `x_i tensor x_j` and
`y_i tensor y_j`.  Two nonzero decomposable tensors are proportional exactly
when both factor lines are proportional.  Thus a common edge contributes one
constraint precisely when both endpoints lie in `R`, and two otherwise.

The total rank is therefore

```text
20-binom(r,2),
```

and the coefficient fibre in `(P^8)^14` has dimension

```text
92+binom(r,2).
```

Different edge-block factors are independent, so these ranks add.  No
genericity of the block coefficients is being assumed.

## 5. Five, not a fictional additive six

Combining root and coefficient dimensions gives the projected lower bound

```text
6-binom(r,2)+2r-a_R.
```

For `r=0,1,2,3` this is at least six.  For `r=4` it is at least five.  The
value five requires `a_R=3`, so both selectors assign every colour to the
same common vertex and all four common roots synchronize.  The selectors are
the same nonconstant map from three colours into four common vertices, giving
`4^3-4=60` labelled minimizers.

Those `60` choices are not asserted to be distinct intrinsic components.
Additional root-coordinate zeros can make one root pair admit several
selectors.

The worst source has dimension

```text
9 root parameters + 98 coefficient-fibre parameters =107
```

inside coefficient ambient dimension `112`.  Proper projection may lower
the image dimension further.  The theorem therefore says codimension **at
least** five, not exact codimension five.

## 6. Closed projective and affine envelopes

For each selector pair, the unstratified root/block incidence is closed in a
product of projective spaces.  Its exact-sync strata all have dimension at
most `107`, so the complete incidence does too.  Projection to block
coefficients is proper and its image is closed.  The finite union over
selector pairs is therefore a closed envelope.

On the all-fourteen-nonzero affine open, block projectivization adds fourteen
torus dimensions, giving dimension at most `121` in ambient dimension `126`.
If any whole block is zero, the point lies in a coordinate subspace of
codimension nine.  The union retains codimension at least five.

The projection from all `28` affine edge blocks to the selected fourteen is
surjective, so inverse image preserves codimension.  This yields dimension
at most `247` in full dimension `252`.

## 7. The tempting mistakes were retained as lessons

Four failed shortcuts materially improved the final package:

1. **Adding `3+3`.**  Two individual codimension-three envelopes do not give
   codimension six.  Full synchronization on the common `K_4` produces six
   block-rank jumps at a root-parameter cost of five.
2. **Stratifying by at least `R`.**  This mixes fibre ranks.  Exact
   synchronization sets repair the count.
3. **Calling a finite union a finite closed subset.**  The images are
   positive-dimensional; the theorem now says a closed subset expressed as
   a finite union.
4. **Putting a coefficient point in a root/block incidence.**  The typed
   statement is `(x,y,B) in I_(f,g)`, hence `B in D_(f,g)`.

None of these mistakes survives in the reviewed theorem.

## 8. Computational independence and replay meaning

The primary enumerates synchronization masks and uses SymPy coordinate-space
ranks.  The independent audit imports neither SymPy nor the primary; it
decodes selectors from base-five integers and uses a per-vertex dynamic
programme on bit masks.  Both report:

```text
selector pairs:                  14,400
feasible exact-sync strata:     213,648
codimension histogram:
  5 ->     60
  6 -> 15,444
  7 -> 14,088
  8 -> 87,576
  9 -> 96,480
minimum source strata:               60
adjacent five-set pairs:             420
```

The scripts audit the finite boundary-selector and dimension arithmetic.
The decomposable-tensor proportionality lemma, incidence argument, and
proper-image conclusion are the written proof.

## Acceptance boundary

```text
single five-set envelope:                            CODIMENSION >= 3;
adjacent five-set pair envelope:                     CODIMENSION >= 5;
affine zero-block branches:                          INCLUDED;
only source stratum attaining the five bound:        CLASSIFIED;
exact projected codimension:                         NOT CLAIMED;
independence among 420 adjacent-pair pullbacks:       NOT CLAIMED;
all-balanced maximal-minor incompatibility:           OPEN;
eight-vertex witness exclusion:                      OPEN;
all-balanced witness exclusion:                      OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Strongest fresh-referee objection

The synchronized `r=4,a_R=3` residual is not a common-quadratic or
common-conformal shore merely because four selected root lines agree across
two five-sets.  Importing an existing synchronized-orbit exclusion here would
silently strengthen the hypotheses.  The honest successors are to intersect
this residual with the balanced maximal minors and remaining mixed equations,
or to add a third overlapping five-set and prove an exact compatibility
gain.
