# Eight-vertex four-five-set support-Segre generic-rank census

## Status and scope

**Verified finite characteristic-zero census at the generic point of each
feasible exact-partition stratum.**  This package repairs the rank input to
the four-chart pencil route, but it is not a global codimension theorem and
does not resolve the Krenn--Gu conjecture.  The global conjecture remains
**UNRESOLVED**.

The result below covers four induced `K5` charts on one common labelled
`K4`.  It exhausts the 120 nonconstant ternary coordinate selectors, modulo
the implemented chart/common-vertex/colour symmetries, and the 15 set
partitions of the four charts at each common vertex.  For every feasible
exact-partition stratum it computes the **generic** rank of the shared-edge
decomposable evaluations.  It proves, by an exact finite computation, that

```text
        q(Pi,F) = Delta(Pi,F) + sum_{i<j in K4} rho_ij(Pi,F) >= 20.       (1)
```

There are exactly two equality records in the canonical census.  On the
generic exact-partition sources, (1) gives affine incidence codimension at
least eight, with equality in those two records.  Rank-degeneracy loci inside
an exact-partition stratum, the `B_all` cut, compatibility across the 70
four-chart pencils, the remaining target equations, and witness exclusion
are not covered.

The primary verifier is the theorem's finite certificate.  The independent
audit directly replays both equality records over `Q` and independently
checks the pinned histogram totals and hashes; it deliberately does not
repeat the billion-scale partition enumeration.  This asymmetry is recorded
explicitly below.

## 1. Four charts and selectors

Let the common vertices be `A={0,1,2,3}`.  Chart `t` has these four vertices
and one local outer vertex `o_t`.  A selector is a map

```text
        f_t : {0,1,2} -> {0,1,2,3,4},                              (2)
```

where `4` denotes the local outer vertex.  The map is required to be
nonconstant.  There are 120 such maps.  The coordinate support at a local
vertex `v` is

```text
        U_{t,v} = span{ e_c : f_t(c) != v }.                        (3)
```

Nonconstancy is exactly what keeps every one of the five local coordinate
factors nonempty.  Each of the three colours is excluded at exactly one
local vertex, so every selector has total local root-factor dimension

```text
        sum_{v in K5_t} (dim U_{t,v} - 1) = 5*2 - 3 = 7.              (4)
```

This remains true when a colour is selected at the outer vertex.  The census
does not omit that outer factor: its dimension is the amount that keeps the
per-chart total (4) equal to seven.  Only the four common roots are
synchronized between charts; all four outer roots remain chart-local.

The four-chart selector tuple is considered modulo the safe action generated
by permutation of the four charts, permutation of the common vertices, and
permutation of the three colours.  The primary verifier first enumerates
the 9,078,630 chart-sorted selector multisets and retains 65,966 orbit
representatives.  Its sorted representative byte-string has SHA-256

```text
e27c85bda3fc01904ad977c003eee1d235a12677186b84a9790d20a234c1e35f
```

The orbit reduction is only a computation reduction.  The partition systems
at a representative are still all enumerated, and the q-minimum is invariant
under the three stated actions.

## 2. Exact partitions and synchronization cost

At common vertex `i`, let `Pi_i` be a set partition of the four chart labels.
For a block `B` define its allowed coordinate mask by

```text
        U_{i,B} = intersection_{t in B} U_{t,i}.                     (5)
```

The exact-partition stratum consists of one projective line in
`P(U_{i,B})` for each block, with distinct lines for distinct blocks.  It is
empty if a block intersection is zero or if two blocks are forced to be the
same one-dimensional coordinate line.  Otherwise those exclusions are a
proper closed subset and the displayed product has the generic dimension

```text
Delta_i = sum_t (dim U_{t,i}-1)
          - sum_{B in Pi_i} (dim U_{i,B}-1).                        (6)
```

Put `Delta=sum_i Delta_i`.  The four common-root part of a generic stratum
has lost exactly `Delta` dimensions relative to four independent common
roots.  Combining (4) over four charts, the complete root stratum,
including the four independent outer roots, therefore has dimension

```text
        dim(root stratum) = 28 - Delta.                            (7)
```

The feasibility test in the primary verifier is this exact intersection and
forced-line test; no numerical distinctness test is used.

## 3. The actual support-Segre rank

For a common edge `ij`, write `E_ij` for the distinct block pairs

```text
        E_ij = { (B_i(t), B_j(t)) : t=0,1,2,3 }.                   (8)
```

Repeated pairs are one evaluation, not four independent rows.  For each
endpoint block use independent generic coordinates `X_{B,p}` and `Y_{C,q}`
on its support.  The support-Segre matrix is

```text
 M_ij[(B,C),(p,q)] = X_{B,p} Y_{C,q}
```

when `p` and `q` are allowed by the two masks, and zero otherwise.  Define

```text
        rho_ij = rank_{Q(X,Y)} M_ij.                                (9)
```

This is the generic tensor-span rank of
`x_i^(t) tensor x_j^(t)`, not the cardinality `|E_ij|`.  The distinction is
load-bearing.  In the first equality record, four different block pairs on
edge `01` produce only rank two: after the selector normalization the rows
are the tensors

```text
        e_2 tensor (1,t+1,0),  t=0,1,2,3,                          (10)
```

and their span is two-dimensional.  Thus a partition cardinality of four
cannot be substituted for `rho_01`.

The exact rank calculation uses two stages.  A deterministic specialization
over `F_1000003` certifies a nonzero full-size minor whenever it is full
rank.  The 24,765 modularly deficient signatures are then replayed by exact
determinant-polynomial search over `Q(X,Y)`.  The determinant monomials are
encoded by **adding** base-5 digit weights for variable exponents; a
multiplicative encoding would incorrectly identify distinct monomials.  The
rank cache is keyed by the explicit ordered support-labelled tuple
`(left_masks,right_masks,E_ij)` and is reused in the q phase.

The exact raw signature count is 1,026,928.  The rank histogram, keyed by
`(c,r)=(|E_ij|,rho_ij)`, is

```text
(1,1):       49
(2,2):    2,755
(3,2):      541
(3,3):   92,401
(4,2):      209
(4,3):   22,060
(4,4):  908,913
```

Its SHA-256 (of the verifier's sorted `repr` form) is

```text
b4610a69106b5fa342f7d5e386ba28761523b3976fea29657d7a348d7351d00f.
```

The modular stage flagged 24,765 signatures; 22,810 are genuinely deficient
after exact replay.  A modular full-rank result is used only as a
nonzero-minor certificate, while every modularly deficient case receives the
exact replay.

## 4. Finite q result and equality records

For every canonical selector representative, the verifier forms the exact
15-state feasible partition list at each common vertex and evaluates all
cartesian products of the four lists.  It uses the exact ranks (9), not
partition cardinalities, and aggregates the integer q values.  The number of
pair instances used to form the raw signature set is 74,083,334.  The full
canonical-representative partition enumeration contains 2,269,536,547
systems.  The q histogram is

```text
20:          2
21:         39
22:        506
23:      8,882
24:    150,155
25:    804,555
26:  5,147,814
27: 18,813,205
28: 65,063,565
29:162,773,111
30:322,044,201
31:496,230,100
32:535,661,624
33:394,624,590
34:194,788,958
35: 55,870,011
36: 13,169,086
37:  3,943,026
38:    443,117
```

Its SHA-256 (again of the verifier's sorted `repr` form) is

```text
1af40871b003b0bbbdcb23aa46de728ff950b9edae489f65a2b504a8808bcb6a.
```

The minimum is 20, and the two q=20 records, up to the selector and vertex
symmetries above, are:

```text
selector shape:  all four charts f=(0,0,1)

record A partitions by common vertex:
    0000 | 0123 | 0123 | 0123
    ranks on (01,02,03,12,13,23) = (2,3,3,4,4,4)
    Delta by vertex = (0,0,0,0)

record B partitions by common vertex:
    0000 | 0000 | 0123 | 0123
    ranks on (01,02,03,12,13,23) = (1,3,3,3,3,4)
    Delta by vertex = (0,3,0,0)
```

Here `0000` means one fully synchronized block and `0123` means four
singleton blocks.  The selector `f=(0,0,1)` is the fibre-size `(2,1)`
nonconstant orbit; all its coordinate factors are nonempty.  The two lines
above are equality **orbits**, not two claims that every labelled copy is a
different intrinsic component.

## 5. Incidence dimension consequence at generic rank

Each of the 16 outer edges belongs to one chart and supplies one independent
linear coefficient equation.  A common edge `ij` supplies `rho_ij` generic
linear equations.  Thus the generic coefficient-constraint rank is

```text
        16 + sum_{i<j} rho_ij.                                    (11)
```

The affine coefficient space has dimension `28*9=252`.  Using (7), a generic
exact-partition incidence source has dimension

```text
 (28-Delta) + (252 - 16 - sum rho_ij)
       = 264 - q.                                                  (12)
```

Consequently its affine codimension is

```text
        252 - (264-q) = q-12 >= 8.                                (13)
```

The two equality records have codimension eight.  This is a dimension
statement for the generic-rank piece of each exact-partition source.  It is
not a claim that every point of the source has this rank or that the union
of all rank-degenerate subvarieties has codimension eight.

## 6. Key-count conventions and audit boundary

The durable verifier uses one explicit raw key convention: an ordered pair of
endpoint support-mask tuples together with the sorted ordered block-pair
tuple `(A,B,E)`.  Under that convention the count is **1,026,928**.

The historical probe reported **677,260** after an old packed/quotiented key
presentation.  That serializer is not part of the durable package, so the
smaller number is retained only as a labelled historical convention and is
not used in any assertion or rank calculation.  The discrepancy is therefore
not silently reconciled as an arithmetic identity: the two numbers count
different key presentations.  The raw convention, selector hash, rank
histogram hash, q histogram hash, and all totals used by the theorem are
pinned by the primary verifier.  Duplicate presentations cannot change a
local matrix or a q value because each q phase looks up the same raw key.

The independent audit constructs the two equality fixtures from scratch with
SymPy, replays their six common-edge ranks and deltas over `Q`, verifies the
codimension-eight arithmetic, and independently recomputes the histogram
hashes and sums.  It does **not** re-enumerate the 65,966 selector orbits,
74,083,334 pair instances, or 2,269,536,547 partition systems.  That is an
audit limitation, not an independence claim beyond the stated checks.

## 7. What remains open

The finite result does not classify a rank-degeneracy component.  If a
rank-degenerate locus has actual rank `r_ij` and root-stratum codimension
`c_rank`, the missing global envelope inequality is of the form

```text
        Delta + sum r_ij + c_rank >= 20.                            (14)
```

The census supplies only the `c_rank=0` generic-rank values.  In particular,
it does not prove that the all-balanced rank-drop locus `B_all` cuts either
equality source properly, nor that four-chart conditions glue across the 70
possible pencils.  It also does not impose the full GHZ target equations,
exclude a witness, or establish any codimension-nine or codimension-ten
statement.  Those are separate load-bearing obligations.  The prior
cardinality-based codimension-nine/ten lift remains withdrawn by the exact
rank boundary.

## Replay

From repository root, the exact primary replay is:

```powershell
uv run --with sympy --with numpy python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py --quiet
```

For bounded execution of the full enumeration:

```powershell
python tools/research/run_bounded.py `
  --run-id kg-four-k5-census-primary-20260827 `
  --timeout-seconds 900 --memory-mb 4096 -- `
  python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py --quiet
```

The independent equality/integrity audit is:

```powershell
uv run --with sympy python claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py
```

The primary run prints `four-K5 support-Segre generic-rank census: PASS` and
asserts every count, histogram, equality record, and hash above.  The audit
prints `four-K5 support-Segre census independent audit: PASS` and reports its
limited scope in JSON.
