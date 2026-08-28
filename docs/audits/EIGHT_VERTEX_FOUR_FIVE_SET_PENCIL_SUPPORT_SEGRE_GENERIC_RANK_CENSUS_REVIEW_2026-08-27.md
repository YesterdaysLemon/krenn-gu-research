# Hostile review: four-K5 support-Segre generic-rank census

## Verdict

**Accept at the stated finite generic-stratum scope.  Do not promote to a
global codimension, `B_all`, or Krenn--Gu theorem.**

The package is a material correction of the withdrawn partition-cardinality
route.  Its primary script computes the actual generic rank of the
support-Segre evaluation matrix, and its assertions pin the finite output.
The theorem document correctly calls the result a characteristic-zero
generic exact-partition census and records the unresolved rank-degenerate and
multi-pencil obligations.  The global conjecture remains **UNRESOLVED**.

## Quantifier and cover checks

The primary verifier enumerates all 120 nonconstant maps from three colours
to the five local vertices.  It first forms all 9,078,630 chart-sorted
quadruples and reduces them by the implemented `S_4` chart, common-vertex,
and `S_3` colour actions to 65,966 representatives.  The selector
representative hash is pinned.  Each of the 15 set partitions of the four
charts is tested at each common vertex; zero intersections and forced equal
one-dimensional supports are rejected exactly.  The q phase takes the full
cartesian product of the surviving state lists at every representative.  Its
reported 2,269,536,547 systems are therefore a canonical-representative
count, not a claim that this is the number of fully labelled selector
systems.  The theorem document says this explicitly.

The outer-root dimension is not accidentally dropped.  For every nonconstant
local selector, each of the three colours removes one coordinate at one of
the five local vertices, giving total root-factor dimension `5*2-3=7`.
The four outer roots remain chart-local, so the four-chart baseline is 28;
`Delta` measures only the synchronization loss at the common four vertices.

## Rank semantics and exactness

For a block-pair signature, the matrix rows are distinct block pairs and its
entries are `X_(B,p) Y_(C,q)` on the allowed coordinate support.  This is the
correct generic span model: blocks share their endpoint variables when the
same block participates in several rows.  The verifier does not replace this
rank by row cardinality.

The modular stage over `F_1000003` is used only in the sound direction:
full modular rank supplies a nonzero polynomial minor.  Every modularly
deficient signature is replayed by exact determinant-polynomial search.  The
base-5 encoding adds exponent digit weights, so distinct exponent vectors are
not collapsed by a mistaken product encoding.  The in-memory rank cache is
keyed by the explicit raw `(left_masks,right_masks,E)` tuple and is reused by
the q aggregation.

The exact rank histogram has 1,026,928 raw keys and is hash-pinned.  The
primary reports 24,765 modularly deficient keys and 22,810 actual rank
defects after exact replay.  These numbers are internally consistent with
the displayed histogram.  A full primary run completed under the bounded
runner with exit code zero.

## Frontier and dimension checks

The exact q histogram has minimum 20 and exactly two q=20 records.  The
independent audit reconstructs both records in a separate SymPy route and
gets:

```text
one synchronized common vertex: ranks (2,3,3,4,4,4), Delta (0,0,0,0)
two synchronized common vertices: ranks (1,3,3,3,3,4), Delta (0,3,0,0)
```

The first record has four distinct block pairs on edge `01` but rank two,
which directly audits the old route's failure.  The root dimension is
`28-Delta`; the 16 outer edges and the six common-edge ranks impose
`16+sum(rho)` generic coefficient equations.  Hence the source dimension is
`264-q` in affine `A^252`, and q=20 gives codimension eight.  This arithmetic
is correct for the generic-rank piece and does not divide away whole-zero
coefficient blocks.

## Key-count reconciliation

The durable key is the raw ordered support-labelled triple `(A,B,E)`, giving
1,026,928 keys.  The historical 677,260 value came from a packed/quotiented
presentation whose serializer is not present in this package.  The primary
therefore retains 677,260 only as a labelled historical convention and does
not assert equality of the two counts.  This is honest: the finite result is
pinned to the raw convention, and the old number is not used in a rank or q
assertion.

## Independence and limitations

The audit does not import the primary module.  It uses an independently
written SymPy evaluation/rank construction for both equality records and
independently recomputes the rank/q histogram hashes and total sums.  It does
not re-enumerate the selector orbits, raw pair instances, or the
2,269,536,547 partition systems.  It is consequently an independent exact
q=20 replay plus integrity audit, not an independent full-census
reimplementation.  The package says so and should retain that wording.

The following are still open and must remain open in the ledger/frontier:

- rank-degeneracy components and their true root codimensions `c_rank`;
- the inequality `Delta + sum(r_ij) + c_rank >= 20` outside the generic piece;
- whether `B_all` cuts either q=20 source properly;
- compatibility across the 70 four-chart pencils;
- the full target equations and witness exclusion.

In particular, this review rejects any codimension-nine or codimension-ten
claim derived from this census, and rejects any assertion of global closure.

## Replay reviewed

```powershell
uv run --with sympy --with numpy python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py --quiet
uv run --with sympy python claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py
python -m py_compile claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py
```

The full primary replay should be run through
`tools/research/run_bounded.py` on ordinary workers.  The audit's exact
SymPy dependency is intentional and must not be described as a no-import
audit.
