# Transfer strategy from the ten mathematics advances

## Status and purpose

The global Krenn--Gu conjecture remains **UNRESOLVED**.  This note records a
parallel method-transfer track inspired by OpenAI's 1 August 2026 release
[Ten advances in mathematics and theoretical computer science](https://openai.com/index/ten-advances-in-mathematics/),
its [full manuscripts](https://cdn.openai.com/pdf/ten-proofs-oai.pdf), and the
[discovery notes](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf).

This work is deliberately separated from the immediate `P_4/P_5` component
and marked-fibre proof track.  It develops two bounded experiments that can
run without changing any current component classification.

## Transfer assessment

### Directly actionable: permanent block selection

The arithmetic-circuit chapter constructs a root-of-unity specialization of
one permanent in which all mixed-block matchings cancel and every intended
block permanent survives.  Its proof uses commuting square-zero variables,
the same Frobenius-algebra language already used throughout this repository.

The transfer is now written and independently replayed in
[`ROOT_OF_UNITY_BLOCK_PERMANENT_SELECTOR.md`](ROOT_OF_UNITY_BLOCK_PERMANENT_SELECTOR.md).
It changes the counterexample-oriented side of the strategy:

- Route E now has a postselection-safe exact matching-sector filter, rather
  than only a Gaussian reformulation involving unobserved photon sectors.
- Route F now has a concrete candidate mechanism for cancelling cross
  matchings between selector modules.
- The safest interface is the bipartite root--blocker permanent already
  extracted by the arbitrary-order blocker theorems.

It does not change the current proof-side priority because legal realization
inside a symmetric graph matching tensor is still unproved.

### Directly actionable later: admissible quotient templates

The extremal compactness chapter does not propagate one local obstruction.
It closes finite templates under admissible identifications, uses one family
to control concentrated extension sets, and uses a second to turn the
remaining exceptional vertices into a cover.

Our first quotient-closed layer is now finite and replayable in
[`SIX_BLOCKER_ADMISSIBLE_QUOTIENT_CATALOGUE.md`](SIX_BLOCKER_ADMISSIBLE_QUOTIENT_CATALOGUE.md):
six local first-surplus profiles and `1,791` two-copy blocker-incidence
quotients, or `10,746` after the six possible root intersection sizes.

This is a framework for the eventual blocker-surplus/gluing problem.  It is
not yet evidence that any quotient is algebraically realizable.

### Confirmation rather than a new route

The quantum parallel-repetition proof isolates a four-cycle holonomy
obstruction to gluing local purification gauges.  That confirms the
repository's existing practice: use gain-graph, projective-holonomy, affine-
holonomy, and Grassmannian invariants instead of independently normalizing
every local chart.  No new operator-entropy machinery appears relevant to
the algebraic Krenn--Gu fibres.

The multicolour Ramsey construction organizes blocks by missing-colour
palettes and retains per-colour local labels.  That is useful language for
blocker profiles, but its quantitative gain requires a growing colour set.
The Krenn--Gu core has three fixed colours, so no Ramsey bound transfers.

The sphere-packing, coding, group-theoretic, lattice, and Ehrhart results do
not presently supply a theorem that acts on the `P_5` restriction, special
marked fibres, or arbitrary-order graph gluing.

## Parallel workstreams

### Workstream A: selector legality

1. Recast the verified heralded Question-2 module as a variable permanent
   block with explicit contraction modes.
2. Realize or obstruct the `d=2` four-row selector using legal graph blocks.
3. If it is legal, verify the full graph matching tensor, not only its
   bipartite permanent projection.
4. Lift to the three-colour and four-channel selector only after the seed
   passes exactly.

The stopping rule is immediate: if the required constant columns cannot be
implemented by legal contractions, record that obstruction and do not search
larger selector supports.

### Workstream B: algebraic lift of quotient templates

1. Filter the catalogue to root overlap at least four and blocker overlap at
   least five.
2. Attach shared edge-block/covector variables to the smallest profile pairs.
3. Use row-space containment, Fitting minors, and legal gauge invariants to
   decide realizability.
4. Only after a two-copy theorem exists, formulate concentration and cover
   templates for a minimal counterexample.

The stopping rule is equally strict: quotient counts are combinatorial
organization, not graph or tensor existence.

## Priority relative to the main proof track

The component and special-fibre programme remains the main proof track.
Alongside it:

1. the root-of-unity selector is the leading bounded construction test;
2. high-overlap six-blocker quotients are the leading gluing experiment;
3. simultaneous-root Grassmannian Route G remains the leading basis-free
   proof experiment if the quotient lift exposes a small incidence stratum;
4. broad support enumeration, generic-only elimination, and unconstrained
   gadget unions remain low priority.

## Replays

```text
uv run --with sympy python verify_root_of_unity_block_permanent_selector.py
python audit_root_of_unity_block_permanent_selector.py
python verify_six_blocker_admissible_quotient_catalogue.py
python audit_six_blocker_admissible_quotient_catalogue.py
```

Every output explicitly retains
`"global_krenn_gu_resolved": false`.
