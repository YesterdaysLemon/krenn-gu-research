# Source-coupled formal proof methods: bounded inspection

This inspection supports the current source-coupled research program. It
imports no new theorem and changes no mathematical status. Global Krenn--Gu
remains **UNRESOLVED**.

## Six-vertex certificate source

The primary repository
[algal/krenn-gu-6x3-certificate](https://github.com/algal/krenn-gu-6x3-certificate/tree/c04696e515e0c02be140353fb52ea60c62e827b1)
was inspected at commit c04696e515e0c02be140353fb52ea60c62e827b1. Its README
and `KrennGuCertificate/Unrestricted.lean`, lines 201-222, claim and assemble
the unrestricted complex six-vertex, three-color exclusion using the
official `WeightsN` and `EqSystemN` definitions. `OfficialBridge.lean`
proves the fifteen-matching expansion. The branch architecture uses eight
orbits of 3375 pure-matching triples, exact Laurent identities and LRAT.

Source inspection is not a local kernel check. No Lean build, current
axiom-closure check or LRAT replay was run here. The source search found no
local axiom or admission declaration; the documented trust closure includes
`Lean.ofReduceBool` and `Lean.trustCompiler` for native evaluation, alongside
the listed foundational assumptions. The historical release receipt names
an older commit. Neither that receipt nor the README is promoted to a
fresh validation of the checked-out tip.

The useful comparison is between `LaurentCertificate.lean`, lines 174-205,
and `LocalPattern.lean`. The former checks an exact localized algebraic
identity. The latter binds it to exactly fifteen matchings, three factors
per matching and 729 six-vertex source words. Exterior vertices introduce
additional matching terms; the finite binding cannot be reused unchanged.

The contraction and full-column mechanisms were also inspected in
`Contraction.lean` and `UniversalRules.lean`. The latter's
`full_column_anchored` theorem duplicates the existing arbitrary-order
[column-killer result](../../claims/arbitrary-order/THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md).
It supplies no new normal form here.

For a six-set U and even complement F, product contraction gives the
restricted six-vertex tensor multiplied by the exterior hafnian, plus
cross-response layers indexed by two, four or six open vertices of U.
Only if all cross responses vanish, the exterior hafnian is nonzero and
all three target products survive does diagonal normalization yield a
six-vertex witness. No universal supply of these premises was found.
The existing branch-specific partial-uncontraction results retain their
own activity and same-source hypotheses. This is a method boundary, not
an imported exclusion or a new resolution route.

## AlphaProof Nexus report and available companion source

The primary [paper](https://arxiv.org/html/2605.22763v2), version 2 of
8 June 2026, section 4, paragraph “Quantum Optics,” reports finite results
including N=d in {4,6,10}. Reference 38 lists an in-preparation paper,
“A Tensor-Algebraic No-Go Theorem for High-Dimensional Photonic GHZ States.”
No statement or proof from that unpublished reference was available in
the inspected passage, and no general bound is inferred from its title.

The linked
[companion source](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/AICollaborator/QuantumOptics/MonochromaticQuantumGraph.lean)
was inspected at commit 0647711a71183c1ea492ad60860776617ce1ea88.
Its relevant Krenn--Gu no-go declarations, including
`eqSystem_no_solution_even_ge4_d_eq_n_explicit` and the displayed
four-, six- and ten-vertex no-go targets, have `sorry` bodies in that
snapshot. Therefore this inspected file supplies encoded statements,
not completed checked proofs of those declarations. This does not refute
the paper's report; it limits what this particular public artifact
establishes. No such declaration is an imported premise in the current
common-star proof.

This was a bounded search and source comparison, not an exhaustive
literature or novelty review. The records in the source registry preserve
the inspected locations and these limitations.
