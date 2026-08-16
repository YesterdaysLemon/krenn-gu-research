# Hostile review of the arbitrary permanent co-two corank-two strengthening

## Verdict and provenance

**PASS, as a scoped strengthening of a necessary permanent boundary.**  For
every characteristic-zero weighted restriction `P_r -> Delta_3` and every
omitted pair `{a,b}`, the reviewed proof gives

```text
dim B_ab >= 5,
dim A_S <= binomial(r,2)-2.
```

For `P_6`, all fifteen four-mode product sensors therefore have rank at most
`13`.  This does not exclude the simultaneous corank-two locus after the
mixed target equations are imposed.  Unrestricted `P_6 -> Delta_3`,
arbitrary-order permanent nonrestriction, and the global Krenn--Gu
conjecture remain **UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md
  verify_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py
  audit_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py
```

The proof was reconstructed independently by two research subagents before
the written package was compared against their derivations.  A third hostile
review replayed the final files and attacked cancellation, low-order, and
scope edge cases.

## 1. Exact dependency on the predecessor theorem

The strengthening imports four proved facts from
`ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_RANK_DROP_THEOREM.md`:

1. the degree-two/degree-`r-2` square-free complement pairing is perfect;
2. its restriction to `B_ab x A_S` has rank three;
3. the three diagonal pair products are independent modulo the left radical,
   while all six mixed products lie in that radical; and
4. a nonzero degree-one form has annihilator dimension at most one, with a
   nonzero annihilator only at coordinate support at most two.

The predecessor's conclusion `dim B_ab>=4` is also used.  Both predecessor
replays pass unchanged.  The new theorem neither weakens their hypotheses nor
transfers their permanent semantics to the balanced hafnian sensor.

## 2. The equality-four radical argument is pointwise

Assume `dim B_ab=4`.  Rank three makes the left radical a single nonzero line
`Kq`.  For fixed colour `c` at mode `a`, the two off-diagonal products against
the other two colours at mode `b` both lie in `Kq`, so they are dependent.
Their second factors are independent.  A nonzero linear combination of those
factors therefore annihilates `u_(a,c)`, forcing support at most two.

The two products cannot both vanish: that would place two independent forms
inside a degree-one annihilator of dimension at most one.  Thus every one of
the three forms at mode `a` occurs as a factor of a nonzero scalar multiple of
the same `q`.  The symmetric argument gives the same statement at mode `b`.

This reasoning permits zero individual mixed products.  It requires only that
each off-diagonal row and column is not identically zero.  No genericity,
division by an unproved coefficient, or rational sampling is used.

## 3. Cancellation-sensitive factor classification

If `0!=q=uv` and both linear factors have support at most two, direct support
case analysis gives

```text
V(q)=supp(u) union supp(v),
|V(q)|<=4.
```

The possible nonzero support graphs are a single edge, a two-edge path, a
triangle, and `K_(2,2)`.  The only coefficient that can cancel the entire
structural support occurs when the two factor supports are the same
two-element set; conditional on `q!=0`, its remaining edge still uses both
vertices.  When four vertices occur, the supports are disjoint, every cross
edge is nonzero, and the connected `K_(2,2)` has a unique bipartition.  Edge
ratios fix one projective factor line on each shore.

The contradiction is then exhaustive:

- at most two vertices, three independent local forms cannot fit;
- at three vertices, all nine pair products lie in a three-dimensional
  square-free quadratic space, contradicting `dim B_ab=4`; and
- at four vertices, only two possible factor lines cannot contain the three
  independent forms at one mode.

Therefore equality four is impossible.  Together with the predecessor lower
bound, integral dimension gives `dim B_ab>=5`.

## 4. The dimension conclusion has exactly one new ingredient

With `N=binomial(r,2)`, the perfect-pairing inequality remains

```text
dim A_S + dim B_ab <= N+3.
```

It is not strengthened.  Substituting only the new lower bound on `dim B_ab`
gives `dim A_S<=N-2`.  In particular `N=15` at `r=6`, hence rank at most
`13`.

At `r=3`, the conditional pair lower bound exceeds the ambient degree-two
dimension; as already happens with the predecessor's weaker bound, this says
that the hypothesized restriction does not exist.  It is not a hidden change
of ambient dimension.

## 5. Computational evidence and independence

The primary verifier uses SymPy and rational arithmetic to check:

- every support-set pair on four canonical vertices;
- the four possible support graphs and the unique `K_(2,2)` shores;
- symbolic weighted `K_(2,2)` edge ratios;
- 40 rational projective support-two forms and 458 resulting quadratic
  classes; and
- that observed four-vertex quadratics have factor-span at most two, while
  factor-span three occurs only on three vertices.

The independent audit imports neither the primary module nor SymPy.  It uses
a custom exact field implementation of `Q(omega)`, a separate graph
two-colouring walk, and custom Gaussian elimination.  Through six coordinate
variables it checks up to 96 projective factor forms and 2,715 quadratic
classes.  Its six-unit Eisenstein grid includes cancellation-sensitive
triangle cases; every observed factor-span-three quadratic is supported on
three vertices, and its factor squares span the quadratic itself.

These are bounded falsification audits, not the universal proof.  The written
radical, annihilator, and support arguments prove the characteristic-zero
statement.

## 6. Mistakes retained as scientific information

Three tempting strengthenings failed during development:

1. **Every support-two quadratic has at most two factor lines.** False.  A
   three-vertex triangle can have three factor lines.  The correct
   contradiction is that all nine pair products then live in a
   three-dimensional quadratic space.
2. **Every mixed product is nonzero.** Not proved and not needed.  The
   annihilator lemma shows only that no off-diagonal row or column can vanish
   entirely.
3. **The dimension-sum inequality improves by one.** False as an inference.
   The predecessor's non-target P6 model still saturates
   `dim A_S+dim B_ab=N+3`; only the restriction-locus lower bound on `B_ab`
   improves.
4. **One small factor is enough for the four-vertex classification.** This
   was broader than the supplied proof.  The accepted lemma, exactly as used,
   assumes both factors have support at most two; the theorem now says so.

The theorem and both audits use the corrected statements.

## 7. Novelty, ownership, and proof-topology boundary

The fresh `origin/main` base contains the predecessor bounds
`dim B_ab>=4`, `dim A_S<=N-1`, and P6 sensor rank at most `14`.  A focused
search found no existing `dim B_ab>=5` or P6 rank-at-most-`13` theorem.

The reviewed files are new and isolated from the active arbitrary-order S2
owner.  Shared navigation, `docs/current-frontier.md`, and
`catalog/theorem-ledger.json` were intentionally not edited while that owner
remains live.  The local theorem is therefore review-ready but not yet
integrated into the canonical frontier map.

Accepted scoped update:

```text
every restriction pair space B_ab has dimension >=5:  PROVED;
every complementary co-two sensor has corank >=2:     PROVED;
every P6 four-mode product sensor rank <=13:           PROVED necessary;
simultaneous corank-two locus excludes P6:             OPEN;
balanced hafnian sensor consequence:                  NOT INFERRED;
unrestricted permanent restriction:                   UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

## Replay result

The two new replays, both predecessor replays, `py_compile`, Ruff, repository
hygiene, migration-tool tests, fourteen-vertex lattice tests, link-rewrite
idempotence, and Git whitespace checks pass on the index-complete candidate
tree.  The final reviewed theorem SHA-256 is
`486CC700D12F99FC72997DB918D816EFCF5368AE6B45ADF722A4AA38ABF0D0B8`.
