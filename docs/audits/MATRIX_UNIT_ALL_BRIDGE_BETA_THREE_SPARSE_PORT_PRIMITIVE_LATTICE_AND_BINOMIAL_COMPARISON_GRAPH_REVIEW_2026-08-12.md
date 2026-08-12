# Hostile review of the beta-three sparse-port primitive-lattice and comparison-graph theorem

## Verdict and immutable pins

This hostile review accepts
[`MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_SPARSE_PORT_PRIMITIVE_LATTICE_AND_BINOMIAL_COMPARISON_GRAPH_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_SPARSE_PORT_PRIMITIVE_LATTICE_AND_BINOMIAL_COMPARISON_GRAPH_THEOREM.md)
at exact reviewed core commit

```text
c3274338e03948414da601bbe365cf2ac3e75fde
```

with these exact Git-byte SHA-256 and Git-blob pins:

```text
theorem:
SHA-256 718b739207f9c579b529716d22fc32a862eebef842c28d3b21a0fd86ff8e3053
blob    a2c9ff7f6cf8f1277023bcdaef30ec58bf8a7161

primary verifier:
SHA-256 98fe22d4debf121f166fab8ed26c9918e898a282d02689d18a439a9b509a6f87
blob    6bcbd9c4d71ac25a719d84d385fd4ed48b9e8dc6

independent audit:
SHA-256 5539a006d2aad199c1e19d57ee5cb216eb3e6081ffaa07d3ff951ab7c77fa499
blob    aa62ce54ca20cf9e0b86ef5a56e95135058bbb08
```

The review found no P0, P1, P2, or P3 defect. The result is an exact
conditional characteristic-zero reduction. It does not force any of its
completion, rank, containment, or comparison-carrier hypotheses. The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Primitive sparse-port lattice

At the A5 sparse quartic site, the four A6 matchings use four distinct
designated port edges. After taking the matching indexed by port zero as
reference, projection to the other three port coordinates sends the three
A6 differences to the standard basis of `Z^3`. This supplies an explicit
integral section and retraction

```text
Z^E -> L_A6 -> Z^E.
```

Therefore `L_A6` is a primitive direct summand of the full physical edge
lattice. The identity port minor is load-bearing: rank three alone would not
establish saturation.

The same-rank conclusion was checked hostilely. If

```text
L_A6 subset L_F subset Z^E
```

and both lattices have rank three, then `L_F/L_A6` is finite. For every
`x in L_F`, some positive multiple lies in `L_A6`; saturation in the common
ambient lattice then gives `x in L_A6`. Hence `L_F=L_A6`. The theorem does
not infer the rank-three hypothesis for the complete fibre.

## 2. Complete-fibre parity consequence

Under the additional A7 integral containment `L_A6 subset L_bin`, equality
`L_F=L_A6` places every normalized complete-fibre exponent in the fixed sign
character domain. The complete target equation consequently reduces to a
sum of `+1` and `-1` values. A nonzero sum is an invertible
characteristic-zero scalar; a surviving zero sum has equal plus and minus
counts and therefore even fibre cardinality.

This excludes odd exact-rank-three contained fibres. It neither forces
exact rank three nor proves containment. In the six-term case, the four A6
signs are already balanced, so the two complement signs must be opposite.
Their difference is an absorbed binomial direction, not a forced new target
direction or proof that a six-term fibre exists.

## 3. Physical port landing

For a physical binomial comparison difference already known to lie in
`L_A6`, the proof correctly retains possible physical edges at the sparse
site outside the four designated ports.

- If only one matching uses an outside port, or they use distinct outside
  ports, their difference has a forbidden outside coordinate.
- If both use the same outside port or the same designated port, projection
  is zero; injectivity on `L_A6` forces the whole difference to be zero.
- The only nonzero case uses two distinct designated ports. Matching the
  three projected coordinates then identifies the difference with exactly
  one A6 port-pair direction, up to orientation.

This classifies a comparison only after lattice landing is assumed. It does
not produce an additional binomial fibre or force its difference into
`L_A6`.

## 4. Comparison graph and across-core caveat

Each landed comparison gives an edge of a simple graph on the four A6
ports. For one fixed balanced sign restriction, its normalized binomial
reduces to

```text
1+epsilon_p epsilon_q.
```

A same-sign edge gives the unit scalar `2`; an opposite-sign edge is already
absorbed by the chosen binomial core. Thus a restriction survives exactly
when every comparison edge crosses its balanced `2+2` cut.

The three balanced Q/Q sign patterns are alternative restrictions arising
from different possible cores. They are not three simultaneously selectable
torsion sheets of one fixed core. Accordingly, the graph census is a uniform
closure test across those alternatives: no graph with at most two edges
closes all three; the inclusion-minimal three-edge closures are exactly a
triangle plus an isolated vertex and `K_(1,3)`. The path `P_4` retains its
balanced bipartition and is the sharp nonclosure.

For the unique aligned Q/C^2 restriction, exactly the two within-doubleton
pair directions give unit scalars. Cross-doubleton comparisons are
redundant. The theorem does not force any such carrier.

## 5. Sharp controls

The exact Laurent controls support both sides of the interface. At

```text
(X,Y,Z)=(1,-1,-1)
```

the aligned core and `p=1+X+Y+Z` vanish while the two Q/C^2 port sums are
`+2` and `-2`. Adding a within-doubleton comparison gives a unit; a
cross-doubleton comparison remains absorbed and leaves the ideal proper.

The boundary core `(1+XY)` does not contain `L_A6`, yet the same point is a
common torus zero with both port sums nonzero. Hence failure of A7
containment alone forces neither a second target direction nor a unit.
These are algebraic controls, not complete physical witnesses.

## 6. Evidence and independence

The primary verifier uses explicit physical matching incidences, coordinate
retractions, rational row reduction, direct graph objects, and exact
Laurent-polynomial evaluation. It checks both route kernels, same-rank
collapse, fibre-sign parity, outside-port cases, all 64 simple comparison
graphs, the Q/C^2 cut, and the proper/unit controls.

The independent audit imports neither repository code nor the primary. It
uses recursive bitmask perfect-matching enumeration, maximal-minor gcd and
determinant tests, separate finite-index controls, bitmask graph enumeration,
and an independently implemented exact `Fraction` Laurent evaluator. The
representations and derivations are materially independent rather than only
renamed copies.

Exact replay at the pinned bytes passed for both scripts. Ruff 0.16.2 check
and format check also passed. These computations are bounded QA for the
four-port mechanisms; the arbitrary-order claims are carried by the written
coordinate-retraction, saturation, quotient, and graph-colouring proofs.

## 7. Scope and severity audit

```text
P0: none
P1: none
P2: none
P3: none
```

The theorem assumes the simultaneous balanced all-bridge branch, the A5
beta-three sparse core, and the A6 common fixed completion. It does not force
complete-fibre rank three, A7 integral containment, any extra comparison
fibre, lattice landing for a comparison, or a triangle/star carrier. It does
not close the uncontained rank-at-least-three ideal and makes no witness or
global-resolution claim.

The `S2O` and `S2P` common-shore sensor lanes use different data and proof
obligations. No conclusion is imported from them, and this theorem makes no
claim about their residuals. The global status remains **UNRESOLVED**.
