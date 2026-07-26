# Six-vertex, three-colour exclusion

## Claim

There is no complex solution of the Krenn-Gu equation system on six
vertices with three or more colours.

Equivalently, no weighted bichromatically edge-coloured multigraph on six
vertices produces a GHZ state of dimension at least three.  The reduction
from `d >= 3` to `d = 3` is immediate: restrict every edge matrix and every
vertex colouring to any three of the feasible monochromatic colours.

This is a computer-assisted theorem about the six-vertex case.  It does not
settle the prize conjecture for arbitrary even numbers of vertices.

## 1. Local rank-one lemma

For a vertex `v`, contract its local factor against a generic vector `x`.
For every other vertex `u`, write

```text
l_u(x) = transpose(W_vu) x.
```

Choose `y_u` in the kernel of `l_u(x)`.  Every perfect-matching term then
vanishes, while the GHZ target gives

```text
sum_c x_c product_u y_(u,c) = 0.
```

Passing each factor to the two-dimensional quotient by `l_u(x)` gives a
three-term relation between decomposable tensors.  The three-term Segre
lemma implies that every summand must vanish separately.  A finite union of
proper linear subspaces cannot cover a Zariski-open set, so for every
`(v,c)` there is a distinct neighbour `u_c` for which

```text
image(transpose(W_vu_c)) is contained in span(e_c)
```

and the block is nonzero.  Call this forced condition the directed killer
arc `v --c--> u_c`.  The three neighbours at a vertex are distinct.

Thus every hypothetical six-vertex witness supplies 18 killer tasks and a
selected simple union with minimum degree at least three.

## 2. Support and minimum-cover reduction

`candidate_support_problem` represents the zero/nonzero support of all 135
matrix entries and derives every eligible killer arc.  It imposes only
necessary conditions:

1. every monochromatic amplitude has a nonzero matching monomial;
2. a forbidden amplitude cannot have exactly one nonzero matching monomial;
3. every one of the 18 killer tasks has an eligible arc.

Make a compatibility graph on the 18 tasks.  Two tasks are adjacent exactly
when their opposite arcs can share one undirected edge.  If `nu` is its
maximum matching size, the minimum number of union edges is exactly

```text
18 - nu.
```

The possible minimum is at least nine.  Exact support classification leaves
only:

```text
9 edges:  triangular prism or K3,3
10 edges: complement C4 + K2
11/12 edges: the global residual
```

All other union skeletons are support-UNSAT.

## 3. Nine-edge cases

The `K3,3` half-edge patterns reduce to 48 support orbits.  Every orbit CNF
is UNSAT; MiniSat and CaDiCaL agree, and DRAT traces are stored as
`tmp/k33_orbit_*.drat`.

For the triangular prism there are 718 half-edge-label orbits.  A
row/column-orientation audit splits them by whether their mutual singleton
weights can be normalized using vertex-colour gauge scalings:

```text
652 orbits: gauge incidence has full row rank; normalized correctly
 66 orbits: gauge deficient; singleton weights retained as Laurent variables
```

Every orbit is exhausted by signed Laurent support certificates:

```text
tmp/prism_orientation_fixed_general_certified.json
tmp/prism_gauge_deficient_unnormalized_certified.json
```

Glucose independently replays the polynomial cubes and final support UNSAT
in:

```text
tmp/prism_orientation_fixed_general_verified_glucose.json
tmp/prism_gauge_deficient_unnormalized_verified_glucose.json
```

## 4. Ten-edge case

The only support-feasible skeleton has complement `C4 + K2` and 7,932
half-edge-pattern orbits.  The same exact gauge audit gives:

```text
7,605 orbits: full gauge rank
  327 orbits: gauge deficient
```

The full-rank orbits are covered by the signed normalized manifest
`tmp/m10_all_orbits_verification_signed.json`; the 327 deficient orbits were
rerun with every mutual singleton retained:

```text
tmp/m10_gauge_deficient_unnormalized_certified.json
tmp/m10_gauge_deficient_unnormalized_verified_glucose.json
```

The deficient rerun contains 1,748 signed Laurent certificates and no
algebraic survivor.  Its orbit indices are exactly the complement of the
7,605 full-rank indices.

## 5. Eleven/twelve-edge global residual

The first 5,000 support CEGAR rows expose 18 whole killer-pattern orbits
under `S6 x S3`.  They were all rerun without normalizing any mutual
singleton.  The original fail-closed run used 146 Laurent cubes and four
exact rational torus saturations.

A stronger rerun recognizes rational linear combinations of reduced
amplitudes that isolate one Laurent monomial.  It exhausts the same 18
pattern orbits using:

```text
145 primitive Laurent-unit cubes
  1 rational linear-monomial cube
  0 Singular fallbacks
```

The one linear cube subsumes all four old fallback supports.  Glucose
independently reconstructs every cube and proves every pattern support CNF
UNSAT:

```text
tmp/global_pattern_orbits_unnormalized_linear_certified.json
tmp/global_pattern_orbits_unnormalized_linear_verified_glucose.json
```

The old detailed manifest and its four Singular logs remain preserved as a
cross-check.  Greedy deletion reduces each old saturation to two
non-saturation equations: a rational sum or difference is a single
nonzero monomial, so the torus contradiction is elementary after the
binomial substitution.

Full symmetry gives 40,680 distinct whole-pattern blocking clauses.

## 6. Final support UNSAT

Add those blockers to the exact CNF saying that no killer cover of size at
most ten exists.  To remove search symmetry, require the 135-bit entry
support to be lexicographically no larger than each of its five adjacent
vertex swaps and two adjacent colour swaps.  This is sound: the globally
least support in every `S6 x S3` orbit satisfies all seven comparisons.

The resulting DIMACS has:

```text
variables                 66,152
base clauses             292,788
whole-pattern clauses     40,680
symmetry clauses            5,628
total clauses            339,096
SHA-256 154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7
```

The exact file is
`tmp/global_candidate_pattern18_unnormalized_certified_symbreak.cnf`.
CaDiCaL 1.9.5, Glucose 4.2, and MapleChrono independently return UNSAT.
An external CaDiCaL 1.9.5 run produced the 86,426,936-byte proof

```text
tmp/global_candidate_pattern18_final_cadical195.drat
SHA-256 9273c872b3aa071e67b3ff176d84c50d104e212bcab38980be38de69f9ffb1d1
```

Independent `drat-trim` backward checking used 10,809,065 resolution steps
and returned `s VERIFIED`.  Its log is
`tmp/global_candidate_pattern18_final_drat_trim_verified.log`.

The fail-closed top-level audit

```text
python verify_six_vertex_final.py
```

checks the CNF and proof hashes, all four solver results, the external solver
and proof-checker logs, the 18 fallback-free pattern replays, both gauge
partitions, and all 48 `K3,3` DRAT proofs.  Its output is
`tmp/six_vertex_final_audit.json`, with `"verified": true`.

Combining the 9-edge, 10-edge, and global 11/12-edge cases excludes every
support of a hypothetical six-vertex complex witness.  Since every exact
solution induces one of these supports, the claim follows.

## Audit history

Two earlier checkpoints are deliberately superseded:

1. an exact-fallback driver stopped after its first torus chart instead of
   resuming boundary-support enumeration;
2. the old prism normalization placed a mutual singleton at
   `(forward colour, reverse colour)` instead of the structurally active
   `(reverse colour, forward colour)`.

The four-Singular global-pattern manifest is still valid, but the
fallback-free linear-monomial manifest now supersedes it in the top-level
audit because it proves the same pattern set with a strictly simpler exact
certificate family.

Independent replay exposed both issues.  The manifests named in this file
are the repaired, fail-closed artifacts: fallback enumeration continues
until support UNSAT, fixed singleton entries are checked against the killer
mask, and gauge-deficient patterns are never normalized.
