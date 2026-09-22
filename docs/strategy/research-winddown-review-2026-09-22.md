# Krenn--Gu research checkpoint for model review

The global complex-weighted Krenn--Gu conjecture is **UNRESOLVED**. No
candidate global proof or counterexample is being submitted. This run
followed the full-source programme beyond the common-star family and
stopped at the owner's usage threshold. The following is a compact review
handoff; the linked owners contain the proofs, exact hypotheses and audits.

Work takes place mainly on k>=2 protected unit-K4 components with hollow
intercomponent crossings. This is an explicit construction family, not a
proved normal form for arbitrary conjecture witnesses.

**Closed branches and reusable implications.** State crossing degree at
most one is excluded for full sources. Every full protected source needs
strictly more than 6k supported crossing scalar entries. An elementary
directed-cycle proof excludes complete paired-resource blocks on any three
protected matchings, allowing nonunit weights and physical overlap; this
removes the imported matching classification from the density proof.
These results are on main in PRs #354--#356.

**Main remaining reduction (PR #357).** In the stronger color-regular,
all-split class, each state has one crossing to each foreign color and each
protected resource maps onto a whole foreign resource. Full-source rows
force all binary physical transitions Hamiltonian, one resource cycle
C_(6k), and every normalized crossing-pair product -1. A global diagonal
gauge removes all continuous weights. The coefficient of any physical word
is nonzero exactly when its resulting ladder paths have even singleton
counts, correct transport between consecutive singleton pairs, and no
free full run of length 2 modulo 3. The missing theorem is a mixed physical
transversal satisfying this criterion. Physical K4 incidence is essential.

**Final accepted additions.** Exact, independently checked finite covers
prove the weaker WP1 equations already force more than 6k crossings at
k=2 and k=3 (8 and 12 vertices). WP1 includes all macro targets and mixed
zeros with min_c q_c<=1. The k=2 certificate covers 262,144 supports; the
k=3 topology/gauge reduction and analytic gates leave 32,768. Each has a
low-q mixed word with exactly one matching for arbitrary nonzero weights.
This does not settle WP1 for k>=4 or denser supports.

For color-regular partial-resource sources, two orphan targets in the same
component must form the third-color protected edge. Its complementary edge
must send both exits to a different whole resource with product -1: the
complete mixed coefficient is h or h(1+g), with h nonzero. Separated orphan
targets remain open. A fixed-component, all-background control passes all
243 local specifications while retaining orphan targets; an explicit
outside mixed word still has coefficient one.

**Where the all-split proof is stuck.** An exact k=5 control has one hollow
C30 resource cycle, all binary transitions Hamiltonian, and every forward
one-switch boundary for one base color saturated. It refutes forward-only
minimum-cycle and predecessor-cycle arguments. It fails reverse switches
and explicit mixed words, so it is not a source. The sharper proposed
lemma is: K4 matching involutions cannot admit hollow Hamilton transitions
P,Q for which both oriented one-resource switch systems retain both root
endpoints in a cycle for every root pair. A proof would close the all-split
branch. The proposition remains open. An unrestricted cyclic-order argument
that omits the physical K4 hypotheses is false; the abstract control does
not isolate the necessity of the Klein relation alone.
General color-regular source supply, separated orphan consistency, the
non-color-regular degree-two branch, and arbitrary-witness extraction are
additional open obligations.

Please review the full matching-sector arguments, finite-to-mathematical
bridges, gauge closure and physical incidence before attempting that lemma.
Separate agents supplied adversarial and exact computational audits; no
Lean proof or independent human refereeing is claimed. More samples or a
stronger-looking local statement would not close the missing global edge.

- [Minimum-density proof](../../claims/arbitrary-order/PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md)
- [Elementary paired-resource proof](../../claims/arbitrary-order/PAIRED_RESOURCE_DIRECTED_CYCLE_EXCLUSION.md)
- [All-split reduction](../../claims/arbitrary-order/COLOR_REGULAR_ALL_SPLIT_SOURCE_REDUCTION.md)
- [Finite WP1 proofs and certificates](../../claims/arbitrary-order/minimum-density-wp1/README.md)
- [Coupled source transport](../../claims/arbitrary-order/DEGREE_TWO_SOURCE_TRANSPORT_AND_LOCAL_BOUNDARY.md)
- [One-switch obstruction and precise open lemma](../../claims/arbitrary-order/all-split-one-switch/README.md)
- [Current frontier and typed proof dependencies](../current-frontier.md)
