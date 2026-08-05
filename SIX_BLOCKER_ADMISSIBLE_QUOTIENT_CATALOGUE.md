# Six-blocker admissible-quotient catalogue

## Status

**Verified combinatorial skeleton; algebraic realizability open.**  This note
starts the quotient-closed local-to-global programme suggested by the
admissible-template method in the compactness chapter of OpenAI's
[Ten Advances in Mathematics and Theoretical Computer Science](https://cdn.openai.com/pdf/ten-proofs-oai.pdf).

It classifies the first blocker-surplus layer and all two-copy incidence
quotients at the level of colour-membership profiles.  It does not test the
simultaneous covector spaces `A_u`, edge-block compatibility, full support of
the root vectors, or realization inside one Krenn--Gu witness.

## One local configuration

Fix five fully supported pairwise-zero roots `R`.  For every outside vertex
`u`, let

```text
S(u)={c in {0,1,2}:u belongs to B_c(R)}.
```

Only vertices with `S(u)` nonempty belong to the blocker union.  The
multi-star theorem gives `|B_c(R)|>=5` for every colour.  If the total union
has size five, all five profiles are `{0,1,2}` and the tight extraction gives
`P_5 -> Delta_3`.

The next layer is a union of six blockers.

## Six-profile theorem

Up to a permutation of the three colours and the six blockers, exactly six
profile multisets satisfy

```text
S(u) nonempty,   |union B_c|=6,   |B_c|>=5 for c=0,1,2.
```

Writing `012` for `{0,1,2}`, the six types are:

| name | profiles | colour degrees |
|---|---|---:|
| `all_full` | `012^6` | `(6,6,6)` |
| `one_missing_one` | `01,012^5` | `(6,6,5)` |
| `one_missing_two` | `0,012^5` | `(6,5,5)` |
| `two_missing_singletons` | `01,02,012^4` | `(6,5,5)` |
| `missing_one_plus_missing_two` | `0,12,012^4` | `(5,5,5)` |
| `three_missing_singletons` | `01,02,12,012^3` | `(5,5,5)` |

Indeed, each colour can be absent from at most one of the six blockers.
Therefore the missing-colour sets of the defective blockers are pairwise
disjoint nonempty subsets of `{0,1,2}`.  No blocker may miss all three
colours.  The six rows above are precisely the partitions, up to `S_3`, of a
subset of the three colours into blocks of size one or two.

## Two-copy admissible quotients

Take two distinguished local configurations.  An admissible identification
in the present skeleton has the following rules:

1. the five roots remain distinct inside each local copy;
2. the six blockers remain distinct inside each local copy;
3. identifications may occur only across the two copies and within the same
   role;
4. the colour profile of a blocker relative to each local root set is
   retained;
5. one global permutation of the three colours and interchange of the two
   local configurations are quotient symmetries.

Root identifications are classified by the intersection size `0,...,5`.
Blocker identifications are partial matchings between the two local six-sets.
Relative colour orientations are retained; they cannot be normalized
independently in the two copies.

The exact catalogue contains:

```text
six local profile orbits:                       6
labelled partial matchings per oriented pair:  13,327
blocker-incidence quotient orbits:              1,791
root-overlap choices per blocker quotient:      6
decorated two-copy quotient orbits:            10,746
fully disjoint decorated orbits:                   31
orbits with a root or blocker overlap:         10,715
catalogue SHA-256:
c346ca7ce741623d50351a945fddda15bba2d0fff154b4666d78168d6f3ccc58
```

The 31 fully disjoint types are not redundant: distinct relative global
colour orientations can survive even when the vertex sets do not overlap.

## How this can help the global search

The catalogue replaces the vague phrase "persistent blocker surplus" by a
finite first layer.  Conditional on excluding `P_5 -> Delta_3`, every fully
supported pairwise-zero five-root tuple begins in one of these six local
types or has at least seven blockers.

The next useful lift is algebraic, not another combinatorial enlargement.
For an identified blocker `u` shared by root sets `R` and `R'`, attach

```text
A_u(R)=span{B_iu(x_i,-):i in R},
A_u(R')=span{B_ju(x'_j,-):j in R'}.
```

Both subspaces arise from the same incident edge blocks at `u`.  Their
coordinate-covector memberships are the two profile labels in the catalogue.
The first target should be the high-overlap strata:

- root intersection at least four;
- at least five shared blockers;
- local types `all_full`, `one_missing_one`, or
  `three_missing_singletons`.

These are small enough to ask whether the shared `W_iu` blocks force a sixth
common full blocker, a forbidden rank drop, a coordinate-boundary root, or an
order-five permanent restriction.

The compactness proof suggests using two complementary template families:

- a **concentration template** made from two five-root configurations sharing
  four roots and many blockers, intended to control repeated extension sets;
- a **cover template** joining two configurations that survive the first
  test, intended to force every zero-coupling relation to meet an exceptional
  root or blocker.

That is a research programme, not a proved implication.  In particular,
4-connectivity or minimum degree cannot be invoked until the algebraic
template hypotheses have been derived from a hypothetical minimal witness.

## Exact replay

From the repository root:

```text
python verify_six_blocker_admissible_quotient_catalogue.py
python audit_six_blocker_admissible_quotient_catalogue.py
```

The primary verifier enumerates all labelled partial matchings, then quotients
by repeated profiles, simultaneous colour permutation, and copy exchange.
The independent audit derives the local types from missing-colour owners and
enumerates feasible profile contingency matrices instead.  Both return the
same pinned digest and `1,791` blocker quotient orbits.
