# Order-14 `C4+C10` first-factor orbit-0 certificate

## Scope

This is a rigorously replayed **local closure**, not a proof of the whole
Krenn--Gu conjecture and not yet a proof for the full `C4+C10` factor
family.

Within the order-14 equality architecture whose full factor is `C4+C10`,
there is no residual support whose first singleton perfect matching belongs
to orbit 0 of the pinned 425-orbit census.  The orbit representative is

```text
{02, 13, 46, 57, 8-10, 9-12, 11-13}.
```

Its orbit has size 10 under the 160 automorphisms of the fixed `C4+C10`
full factor.

## Certificate mechanism

Every learned rule starts from a directly replayed factor-fork identity.
The identity uses one full-only base equation and one target equation for
each of the two full cycles.  It remains valid for any replacement support
with the same perfect-matching activity in those equations.

The minimum-activity compiler replaces the old full edge mask by:

1. source-present role-1/role-2 edges needed by the desired active
   matchings; and
2. a minimum hitting set of source-absent edges blocking every other active
   matching that can occur.

The structural version first removes an unwanted matching only after an
independent exact check proves that it cannot extend to two perfect
matchings which are edge-disjoint from each other and from the pinned
role-0 factor.  This is a safe relaxation of the complete support model:
connectivity and the additional factor-census restrictions are not used to
justify any learned clause.

Every minimized certificate is independently replayed from its source
factor fork.  The replay checks source hashes, the algebraic fork
semantics, every desired and potentially active perfect matching, structural
extendability, premise truth values, hitting coverage, and exact minimum
false-premise cardinality.

## Fresh reconstruction

The final global rule CNF was rebuilt directly from the original 425-orbit
base, not from an inherited incremental checkpoint:

```text
base CNF:
  variables: 656
  clauses:   98,676
  SHA-256:   082da87c07c89ce629fae8baf34e5cb0a3e93a9d3acee300ebd25337e40e3cde

verified structural certificates: 370
  activation score 3: 308
  activation score 4:  54
  activation score 5:   8

new symmetry-closed clauses: 11,696

fresh global CNF:
  variables: 656
  clauses:   110,372
  SHA-256:   045041595cfa7b9d53c4abb58bbbfc3b7dea827df327fbe0750a26308086a9fe
```

The independent per-selector audit solved all 425 selector assumptions.
Orbit 0 was UNSAT and the other 424 orbits remained SAT in this rule CNF.
Thus the result has exactly the local scope stated above.

Authoritative reconstruction artifacts:

- `tmp/fourteen_vertex_c4_10_rule_sat_orbit0_fresh_global_augmentation.json`
- `tmp/fourteen_vertex_c4_10_rule_sat_orbit0_fresh_global_augmentation_verified.json`
- `tmp/fourteen_vertex_c4_10_rule_sat_orbit0_fresh_global_orbit_audit.json`

## Independent UNSAT proof

Appending the orbit-0 selector unit gives a 110,373-clause conditioned CNF:

```text
conditioned CNF SHA-256:
  d14cb4bde15aae024ec595283e6d2142399d59bc8d4d6c8f4b6116b4f329d10b

Kissat binary DRAT proof:
  bytes:    1,627,237
  SHA-256:  c8f6243a850a9da16a9e690d0a9c4c464ad9bf22af8535a1c6be1564f23d6e57

drat-trim:
  SHA-256:  92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a
  result:   s VERIFIED
```

Authoritative proof artifacts:

- `tmp/fourteen_vertex_c4_10_rule_sat_orbit0_fresh_conditioned_chain.json`
- `tmp/fourteen_vertex_c4_10_orbit0_fresh_kissat.json`
- `tmp/fourteen_vertex_c4_10_orbit0_fresh_kissat.drat`
- `tmp/fourteen_vertex_c4_10_orbit0_fresh_drat_trim_verified.json`

## Evidence boundary

The result excludes one of 425 first-factor orbits inside one remaining
order-14 equality-architecture factor type.  It is meaningful progress
because all 425 orbits were SAT in the original exact rule compiler, but it
does not exclude a general complex witness.  The global prize conjecture
therefore remains unresolved.
