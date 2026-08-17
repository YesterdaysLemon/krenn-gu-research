# Contraction escape and paired-response closure hostile review — 2026-08-17

## Verdict

**Accepted at the frozen hashes recorded below. No P0 or P1 defect remains.**

The hostile review required two pre-freeze corrections:

1. The mixed-shape discussion originally risked identifying every
   cross-intersecting support cell as an irreducible component. The final
   theorem correctly says every such family indexes a contained coordinate
   subspace, while components correspond exactly to inclusion-maximal
   families.
2. An earlier conceptual ledger conflated the four-dimensional scalar/pure
   complete-bipartite kernel with the full ternary kernel. The frozen theorem
   and both exact implementations correctly record dimensions `16` total,
   `12` mixed, and `4` pure.

The final GLD13 wording also explicitly justifies, using finiteness and
Zariski density of the contraction torus, the equivalence between a common
nonzero-response point and every response tensor being a nonzero polynomial
tensor.

These are theorem-sized but scoped advances. GLD13 does not exclude generic
pure absorption or force activity. GLD14 assumes legal same-graph, same-`Q`
attachment of the selected residual-absent rows. Neither theorem proves
witness integration or a permanent restriction. The global Krenn–Gu
conjecture remains **UNRESOLVED**.

## Frozen artifacts

Base HEAD before the untracked package:

```text
840d82b2b9a87a979e3c859f64a65bbf97755b1d
```

```text
GLD13 theorem  437C063D6FC125C893EF93439FD0ED3592A8D169473549C7D27EE6E261E9AA2C
GLD14 theorem  61EA870D1274F41A1A1402EEE779773C4E29A3B0489C93353190C58C4D54E591

GLD13 primary  33A3B32226040634D0E661551395A177A0824981C4B287FA0E141698A6A58B88
GLD13 audit    30DD2D827A2127FB7BF329120AA1045710731CCA7F32B38BCFA0C2A5E488C6DA
GLD14 primary  907330EEB8C5980AB273ED528E1B6956903E3E2A5F693DD3149A79FE8847FD76
GLD14 audit    5A6A2DBAA63728AE2455A2BAFE0459B2000FCAA9106601B590E39454DD529D6A

README         48C7A832C0D47D64A70BFF5DEC3048CFFEAFED2F0DEFADA4EA76C9A3846F777A
frontier       1A4B5A1B90DEED14BE75D1DAB53D146760E8F10E27CE2C400C3EE36FE7162E4E
```

## GLD13: common contraction escape or generic absorption

The function-field argument is valid over the stated infinite
characteristic-zero field. It uses the full uncontracted witness identity, so
the GLD7 quotient identity may legally be base-changed to the Laurent-function
field. It is not inferred from one fixed contraction or a fixed-`z_Q` slice.

Each nuisance module retains every nuisance column. In the escape branch, a
nonzero nuisance-rank minor, augmented-rank minor, and selected nonzero
response coordinate are multiplied across the finite seven-target family.
The Laurent coordinate ring is a domain, and Zariski density supplies one
rational torus point in the resulting principal open. Consequently all seven
quotient ranks equal one at the same contraction of the same graph and
residual pair `Q`, supplying the six `D_uv` tensors and the four-port `T`.

In the absorption branch, equality of generic augmented and nuisance ranks
means the desired class vanishes only over the function field. Applying the
GLD7 identity there and using the independence of the synchronized pure
target words correctly absorbs all three pure columns. Clearing one common
denominator gives the four stated polynomial nuisance identities.

The theorem correctly preserves the distinction between generic and
pointwise behavior. Rank-drop specializations may permit exceptional escape
even when the desired column is absorbed generically. The two alternatives
classify generic rank patterns; they do not assert pointwise geometric
exclusivity.

Response nonvanishing is a genuine hypothesis. If a target response tensor is
the zero polynomial, neither the common nonzero-response conclusion nor the
stated two-branch witness application follows; the theorem records this
separate response-zero obstruction.

The selector coefficients may depend on the fixed graph, `Q`, and chosen
common contraction. Their noncircular content is that they are constant in
the open-port variables and exact modulo every nuisance column, rather than
selected merely because a realized output looked diagonal.

## GLD14: paired affine incidence

For a fixed complete residual-present fibre `B_0+L`, with `L=ker mu_K`, a
fixed legally attached linear residual-absent pair package cuts the fibre by
the standard empty/affine/unique trichotomy. The ambiguity space is exactly
`L intersect ker P`.

If `d=dim L`, one may choose `d` scalar coordinate restrictions whose
restriction to `L` is an isomorphism. Conversely fewer than `d` scalar linear
rows cannot be injective on a `d`-dimensional space. This optimality statement
is correctly limited to scalar linear `M_2` rows; it is not a lower bound
against nonlinear or higher-depth measurements.

The result does not manufacture or legally attach those rows. It begins after
a common same-graph, same-`Q` package has been attached.

## All-depth mixed-shape criterion

After pair diagonality, a mixed `M_4` coefficient on two disjoint edges of
different colours is the unique product of the corresponding direct-pair
coefficients. Its vanishing is therefore equivalent to the pairwise
cross-intersection condition on differently coloured active-edge families.

Any higher-depth mixed matching contains two disjoint edges of different
colours. Hence failure of all-depth purity is already detected at depth four,
while the cross-intersection condition excludes every mixed higher matching.
This proves an all-depth statement for the complete residual-absent response
tower on the named six-port union, not an arbitrary atlas or an attachment
theorem.

The six-port count is exact:

```text
15 pairs * 6 ordered off-diagonal colours = 90 M2 rows
15 four-sets * 3 complementary pairings * 6 ordered colour pairs = 270 M4 rows
total = 360 rows
```

The displayed one-row controls establish individual necessity inside this
coordinatewise certificate class. The theorem does not claim that `360` is
minimal among arbitrary linear combinations or nonlinear measurements.

The square-free monomial ideal is radical. Every cross-intersecting support
family indexes a contained coordinate subspace, and precisely the
inclusion-maximal families index the irreducible coordinate-subspace
components. The repaired wording is correct.

## One-colour decomposition and complete-bipartite control

The decomposition by the number of nonzero endpoint colours is exhaustive:

- the zero-nonzero-colour block is the scalar Wick kernel;
- a singleton coloured endpoint contributes the stated vertex-deleted
  degree-one kernel;
- a two-endpoint block contributes exactly when the endpoints form a
  two-vertex cover.

Distinct labelled tensor words prevent cancellation between these blocks,
giving the stated direct-sum decomposition and dimension formulas.

For the physical complete-bipartite `K_(3,3)` channel, the exact ledger is:

```text
full tensor Wick map: 1215 x 135
rank:                 119
kernel dimension:      16
mixed projection rank: 12
pure residual:           4
```

The four pure directions are the within-shore scalar edge differences. The
other twelve are the one-sided coloured directions, two colours for each of
six ports. The selected sixteen coordinates restrict to a determinant-one
matrix, so the stated linear package is genuinely unimodular.

The four-dimensional common-one-colour family has every mixed `M` and `Z`
coefficient zero at every depth. It is only a pure subfamily of the full
sixteen-dimensional tensor kernel, not the entire tensor fibre. It is a sharp
response-algebra control, not a witness or physical graph fibre satisfying
the full mixed GHZ equations.

## Independent checks

All four frozen focused commands pass:

```text
fixed-Q contraction escape/generic absorption primary replay: PASS
fixed-Q contraction escape/generic absorption independent audit: PASS
paired M2 incidence/one-colour kernel/all-depth M-shape primary: PASS
paired M2 incidence/one-colour kernel/all-depth M-shape independent audit: PASS
```

The GLD13 primary uses symbolic polynomial matrices, while its independent
audit uses a separate exact polynomial/rational rank route. The GLD14 primary
constructs the full exact ternary Wick map, while its audit uses sparse exact
elimination and the support-block decomposition. These are finite exact checks
supporting the written proofs; they do not replace the function-field,
tensor-support, or all-depth arguments.

`python -m ruff check` passes for all four scripts, and
`python -m ruff format --check` reports all four already formatted. The
Markdown whitespace/conflict scan and tracked README/frontier
`git diff --check` pass.

## Frontier and exact remainder

The README and `docs/current-frontier.md` accurately integrate the two
advances:

- GLD13 refines GLD7/GLD9 into a common seven-target escape branch or a named
  generic pure-absorption obstruction, while retaining exceptional rank-drop
  escape, response-zero cases, activity, and permanent extraction as open.
- GLD14 refines GLD12 only after legal paired-row attachment. It closes affine
  incidence and residual-absent all-depth target shape on one named six-port
  union, but not attachment, witness integration, or permanent extraction.

The typed edges do not turn either conditional result into a global proof. No
apparent counterexample is asserted. The global status remains
**UNRESOLVED**.

Publication verdict: **accept the frozen GLD13+GLD14 package at these hashes,
subject to the repository's ordinary staged candidate-tree validation
floor.**
