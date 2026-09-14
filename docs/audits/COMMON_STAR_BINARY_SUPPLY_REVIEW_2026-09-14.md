# Independent review of the common-star binary-supply countercontrol

## Verdict and exact scope

I accept the construction in
[`PROTECTED_SCAFFOLD_COMMON_STAR_BINARY_SUPPLY_NO_GO.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_COMMON_STAR_BINARY_SUPPLY_NO_GO.md)
as an exact countercontrol to BS, establishing:

> In a finite one-label common-star array, S1, both S2 families, and every
> full physical source equation through four minorities do not force any
> binary option graph to be a union of complete bicliques.

This is a negative parent-route result.  The constructed array fails a
displayed mixed full component target, so it is not a CSQ4 witness or a
counterexample to Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

I reconstructed the exact field, matrices, tensor signs, clone factors, cover,
binary components and full-source failure without importing the primary
scientific implementation.  I also checked the proof of the four-minority
classification rather than treating the finite triangle count as an
enumeration of all physical words.  I found no mathematical gap.

## Matrix and tensor audit

Work over `Q(sqrt(3))`.  Starting from the displayed 3-by-3 matrix `A`, I
embedded it in `I_5` on coordinates `012` and `234`, then multiplied the two
embeddings to obtain `M`.  Direct exact elimination gives `D=M^(-T)` and the
same 21-entry support for `M` and `D`.  The row degrees of `M` are
`(5,5,5,3,3)` and the column degrees are `(3,3,5,5,5)`.

The overlap at coordinate 2 supplies at most one product path for every entry
of both `LR` and `L^(-T)R^(-T)`.  Therefore the entrywise relative inverse
factorizes as the ordinary product of the two embedded 3-state relative
inverses.  Independent exact multiplication confirms that

```
W = M Hadamard M^(-T),   W 1 = 1,   W W^T = I.
```

I reconstructed the two strict color triples, including the swap of colors 0
and 1 in the second tensor factor.  With the single minus sign in
`N_cd=-P_cd^(-T)`, all six orientations satisfy, entry by entry,

```
Q_dc Q_ce = -Q_de,
(P_dc N_ce) Hadamard (N_dc P_ce) = -Q_de.
```

The sign is load-bearing: replacing `N` by the positive inverse transpose
changes the five-state `Q` row sums from `-1` to `+1` and breaks S1.

The tensor support counts are 441, 105 and 105 for pairs 01, 02 and 12.
For 01 the binary graph is one connected `25+25` component with 441 edges.
For 02 and 12 it is five connected `5+5` components with 21 edges each.  The
path `(0,0),(0,2),(3,2)` with missing corner `(3,0)` proves the five-state
support is not complete.  Tensoring and cloning preserve an explicit missing
corner inside the same connected component.  Thus none of the three binary
graphs is a union of bicliques.

Omitting the second-factor color swap is a substantive control: pair 02 then
becomes 25 isolated complete `K_(1,1)` components before cloning, so the BS
conclusion is restored for that pair.

## S1, S2 and physical assembly

The two-clone construction was recomputed from the displayed factors.  Exact
entry checks cover 600 row/column S1 sums, 14,700 ordered off-diagonal
same-color S2 entries and 15,000 ordered distinct-color S2 entries.  These
checks retain the center and leaf factors separately.  They use

```
(1+r)(1+r^(-1))/4 = 3/2
```

and the two strict tensor identities above, so the coefficient-three term in
the distinct-color formula has the correct sign and multiplicity.

The independent cover replay reconstructs `SL(2,F5)` from its determinant-one
definition and applies the six displayed translations.  It creates 120
resources, 6,000 physical K4 components, 24,000 physical vertices, 312,480
gadgets and 624,960 crossing entries.  Different old components share at most
one resource.  Copies of one old component can share resources only in the
same state color, where no gadget exists.  Hence every physical component
pair carries at most one unequal-color label.

Every component-color state belongs to one resource.  Local S1/S2 identities
therefore assemble globally except for the possible deletion of background
spokes by the second selected component.  Keeping those terms gives the
product `(1+s)(1+t)`.  S1 converts its factors to direct `Q` entries, and the
one-label condition makes their product zero because the two required labels
on the same physical pair are incompatible.  This covers equal as well as
unequal changed colors; no independent cofactor variable is substituted.

## Four-minority bridge

I checked the inherited matching classification directly.  Hollowness makes
each crossing edge consume a minority vertex, so a word with at most four
minorities has at most four crossing edges.  Parity in each K4 component makes
the crossing multigraph Eulerian.  Degree four is impossible under the
one-label common-center geometry, leaving doubled edges and cycles whose used
vertices all have degree two.

The two local types are AB (center and one leaf cross) and BB (two distinct
leaves cross).  The minority budget leaves only:

1. one doubled gadget, which is a singleton changed component and is S1;
2. an ABB triangle with three or four minorities; or
3. no crossings, which is pure unless exactly one whole component changed.

Four-cycles, two doubled gadgets and all remaining triangle patterns exceed
the budget.  At the BB vertex an ABB term can survive only when its two gadget
labels disagree there, so the triangle is incoherent.  The full cover replay
enumerates 423,360 actual component triangles and verifies that every one lies
in one resource with consistent labels at every component.  S1 plus this
coherence therefore proves every U4 equation.  This is a proof-based case
cover; neither checker enumerates all `3^6000` component words.

As a negative control, the algebra audit inserts one incoherent three-component
ABB triangle and expands its literal 12-vertex source.  Its target is zero but
its exact source is one.  This confirms that triangle coherence is a necessary
input to this U4 bridge.

## Independent full-source failure

For the word assigning clone-zero components color 0 and clone-one components
color 2, each resource splits into five residual blocks.  The literal
24,000-vertex graph decomposes into 600 weighted 20-vertex blocks and 6,000
isolated protected unit edges.  Each residual block has 6,130 supported
perfect matchings and exact source

```
F_5 = -463/2592.
```

I obtained this value by three separate exact routes:

- a word-first 20-vertex hafnian recursion;
- the permanent of the bipartite 10-by-10 matrix
  `[[M,I],[I,(-D/2)^T]]`;
- the generating sum `sum_l T_l(-1/2)^l`, where

| `l` | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| `T_l` | 1 | 5 | 10 | 10/81 | -83/9 | 169/9 |

The Boolean permanent independently returns 6,130.  The complete physical
source is therefore `(-463/2592)^600`, which is nonzero, while its target is
zero.  This failure is part of the scope boundary, not evidence against the
original conjecture.

## Reproducible evidence and identities

The analytic proof above and the finite companion checks are distinct evidence.
The primary verifier reads the tracked fixture.  The first independent audit
reconstructs the algebra, clone identities, cover counts, three residual-block
calculations and mutation controls.  The second independently materializes
every cover gadget, binary connected component, component triangle and scalar
connected component.

Run:

```bash
python claims/arbitrary-order/verify_common_star_binary_resource_supply_control.py
python claims/arbitrary-order/audit_common_star_binary_resource_supply_control.py
python claims/arbitrary-order/audit_common_star_binary_resource_cover.py
```

Pinned LF SHA-256 identities:

- binary-supply owner: `27578b436d01f98a9e19b77caae97d7a1d9de7d4ef9fa6dbf9ce9e6d5764f826`;
- component-target/consumer owner after its BS boundary update: `e32784ed8faa2898539b99852608429add86872c4299f6b79fca5c217c07f432`;
- resource-alignment owner after its historical BS boundary update: `0f58eb58caa050fb801aec71602eac7699dc41d967a592536899d7af9abfee67`;
- primary verifier: `dd1a0047a9b40f34a2ea31fa10215802fb7b31af5b810befbc8d0b1f83a1bd0b`;
- fixture: `baa050b2fb8013bc4da289f4becbbf413c3253aa69d49b6f1c06fa54781197a6`;
- independent algebra audit: `b51258df8596b712e5d15874bdd525696eaf1ab4dbbbe97c602457b7da53dec5`;
- independent full-cover audit: `177489d54beb718d55f0a54b1194598960828dd904eb0c0acf7ae0eb19d9875c`.

The last two owner edits only update the proof-topology boundary: the earlier
PSCS and RCS mathematics and their historical review identities remain
unchanged in scope.
