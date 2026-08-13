# Hostile review of the eight-vertex five-root boundary-incidence package

## Verdict and provenance

**PASS, as a scoped codimension-at-least-three necessary obstruction and a
separate monomial mixed-shell sharpness theorem.**

This was an automated adversarial review by the Codex collaborators Citrine,
Amber, and Saffron.  It is not an independent human peer review.  Amber
derived the incidence obstruction and repeatedly stress-tested its
quantifiers.  Saffron independently audited the projective/affine dimensions
and built the adjacent-cut control.  Citrine reconstructed the prior theorem
interfaces, checked novelty, and owns the final proofs and replays.

The accepted claims are:

1. every five-root zero in an eight-vertex weighted ternary witness has a
   zero root coordinate in each target colour;
2. every induced `K_5` system whose ten blocks are all nonzero lies in a
   fixed finite closed projective coefficient envelope of codimension at
   least three;
3. the affine envelope, including whole-zero block branches, retains
   codimension at least three; and
4. on the invertible monomial common-form suborbit, Hamming one is blind but
   four pair-local Hamming-two equations detect every point.

Neither theorem excludes its residual locus.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. The anchored slice uses mixed equations

The easiest serious overclaim is that pure normalization alone forces the
three colour products into the internal-edge ideal.  It does not.

For a fixed colour `c`, the proof uses the complete tensor identity after
putting `e_c` into all three complement slots while leaving the five root
slots arbitrary.  This is a `3^5`-coefficient slice.  Across all colours the
input comprises `729` target equations: three pure coefficients and `726`
mixed zeros.  The graph-side ideal membership is matching combinatorics, but
identification with the root product is a full anchored-slice consequence.

The theorem and frontier wording retain this scope.  No claim that pure data
alone gives codimension three is accepted.

## 2. The matching mechanism has prior ownership

For a five-set and its three-vertex complement, the endpoint equations give

```text
a=d+1>=1.                                              (1)
```

The exact `105`-matching ledger has `60` sectors with `(a,d)=(1,0)` and `45`
with `(a,d)=(2,1)`.  This is the first level of the existing
`MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY`; it is not presented as a new
matching theorem.

The new edge combines that ideal membership with the independent five-root
existence theorem and the three-colour incidence calculation.  The owning
document credits both predecessors explicitly.

## 3. Scheme containment and the 120-product cover are distinct

The three colour monomials belong to the ten-form ideal, so their common
zero scheme contains the five-root scheme.  The subsequent cover by `Y_f`
is used set-theoretically.

There are `125` maps from three colours to five roots.  Five constant maps
make all homogeneous coordinates of one `P^2` vanish and are empty.  The
remaining `120` coordinate products are nonempty irreducible sevenfolds:
`60` have load profile `(2,1)` and `60` have `(1,1,1)`.  They overlap; they
are not claimed to be `120` distinct irreducible components of a saturated
monomial scheme.

## 4. The incidence calculation proves only a lower codimension bound

At fixed projective roots, each nonzero rank-one evaluation cuts one
hyperplane in its own independent `P^8` edge-block factor.  Thus

```text
dim I_f=dim Y_f+10*dim P^7=7+70=77.                   (2)
```

Proper projection makes the coefficient image closed and gives dimension at
most `77` inside the `80`-dimensional coefficient product.  It does not prove
generic finiteness, exact codimension three, or equality with the witness
locus.  The theorem consistently says **codimension at least three** and
**necessary envelope**.

## 5. Projective and affine block spaces do not mix silently

The projective argument requires all ten blocks nonzero.  On that open, the
block-projectivization fibre has dimension ten, so the affine lift has
dimension at most `87` in dimension `90`.  The map is not extended across a
zero block.  Instead, the ten whole-zero-block coordinate subspaces are added
separately; each has codimension nine.  The resulting finite closed union has
codimension at least three.

## 6. Fifty-six five-sets do not yield additive codimension

There are `56` five-sets in eight vertices.  The selected root and the map
`f` may vary with the five-set, and the induced edge blocks overlap.  No
transversality, independence, or product decomposition has been proved.
The theorem records all `56` necessary pullbacks but never adds their
codimensions.

## 7. Balanced rank drop is not an input

Adjacent balanced four-shores motivate their five-vertex union, but none of
their maximal-minor equations occurs in the proof.  The codimension-three
condition applies to every eight-vertex witness.  It therefore refines the
S3 branch without classifying `B_all` or proving synchronization.

The exact next question is whether the all-cut minors make the overlapping
five-set boundary incidences incompatible, not whether two prescribed
same-vector ideals share a zero.

## 8. The monomial Hamming-shell theorem is separately scoped

For monomial gauges, direct latent-label parity proves:

- nonzero pure coefficients make every Hamming-one word vanish;
- for every pair and base colour, exactly one or two of the four Hamming-two
  cells are nonzero.

The rational fixture has all-cut rank drop by exact common-form covariance,
pure coefficients `(1,1,1)`, all `48` Hamming-one zeros, adjacent fixed-gauge
quadric determinants `4` and `-8`, and the Hamming-two failure
`[00022000]T=-1`.

It is latently synchronized and already excluded by the common-form
flattening theorem.  It does not refute existential multiroot synchronization
or say anything universal about nonmonomial or nonsynchronized points.

Once the three colour products vanish on one five-root zero, arbitrary
contractions of only the three complement modes add no internal-`K_5`
equation.  The Hamming-two result therefore remains route sharpness; no extra
codimension is imported into the universal theorem.

## 9. Computational independence and replay meaning

The primary uses SymPy, a first-pivot matching recursion, direct permutation
tables, and exact matrix conjugation.  The audit imports neither SymPy nor
the primary; it uses standard-library `Fraction`, a reverse-pivot recursion,
endpoint-assignment dynamic programming, and separate determinant and parity
implementations.

These scripts replay finite constants and conventions.  The arbitrary-field
ideal containment and the proper incidence-image proof are the written
mathematics.

## Acceptance boundary

```text
five-root existence:                                  IMPORTED / PROVED;
three anchored colour products in the edge ideal:     PROVED;
projective nonzero-block witness envelope:             CODIMENSION >= 3;
affine envelope with zero-block branches:              CODIMENSION >= 3;
monomial common-form H1 blindness / H2 detector:       PROVED;
same-vector adjacent-cut basepoint from H1 data:       FALSE;
independence of the 56 five-set conditions:            NOT CLAIMED;
eight-vertex witness exclusion:                        OPEN;
all-balanced witness exclusion:                        OPEN;
global conjecture:                                     UNRESOLVED.
```

## Strongest fresh-referee objection

Membership in one `D_f` asserts only that one triple-boundary root exists.
It does not say that every five-root solution lies there, that the other two
colour products vanish at every root in `D_f`, or that a general point of
`D_f` is a witness.  The theorem uses the witness identity to enter the
envelope; it never characterizes the envelope as the witness locus.
