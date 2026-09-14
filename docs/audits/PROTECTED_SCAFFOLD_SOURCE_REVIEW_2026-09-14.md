# Protected scaffold source review, 2026-09-14

## Status and scope

This is an independent review of Sections 5--7 of
`tmp/scaffold-binary-algebra.md` at SHA-256
`2d13cbea51201dcd02df02eb107f27cdc11aef6c249b0755b9414dc39253b3d2`.
The reviewed claims are valid for the protected K4 matrix-unit scaffold over
the complex numbers, and more generally over an integral domain, with the
same-colour crossing blocks zero. They do not prove an arbitrary-order
scaffold exclusion, a reduction from general sources, or the Krenn--Gu
conjecture. The global conjecture remains **UNRESOLVED**.

## Algebraic review

The minority formula

```text
T_W(a) = per(H_R),  H_vw = W_{v,p_c(w)}[d_v,c]
```

is exact when the majority colour `c` is fixed and `R` contains at most one
endpoint of every `M_c` edge. Each minority breaks one protected edge, its
partner must match a minority, and all untouched `M_c` edges are forced.
Thus supported matchings are precisely the bijections in the permanent.

For a fixed `c`, vanishing of every nonempty admissible-minority coefficient
is equivalent to the absence of an admissible directed cycle in `D_c`. A
permanent term gives a directed cycle cover. Conversely, a shortest
admissible directed cycle has no nonsuccessor chord: such a chord would give
a shorter cycle on an admissible subset. The colour `d_v` affects only the
outgoing row from `v`, so the cycle edges can be made nonzero independently.
The induced permanent then consists of one nonzero cycle monomial. The
integral-domain assumption is needed when concluding that this product is
nonzero; it is satisfied by the intended complex coefficient field.

The exterior-resource expansion is also exact. Every used exterior `M_c`
edge supplies one unordered boundary pair, its kernel `K^e` sums the two
endpoint assignments, and an injection from boundary pairs to exterior edges
prevents resource reuse. Expanding the boundary hafnian over commuting
square-zero resource labels and then applying the stated linear functional
counts every full matching once. In Equation (11), the six two-subsets for
each `e<f` are exactly the three boundary pairings with the two assignments
of the labeled resources; no numerical factor is missing.

Two presentation qualifications should be retained. Equation (9) is stated
for a two-component boundary, while Equation (11) uses the same valid
argument for a one-component boundary; the resource statement should be
given for an arbitrary union of whole components. Also, Formula (7) is a
literal special case of the displayed two-component expansion only when that
boundary contains all minority vertices. Its arbitrary-component version is
established by the direct exposed-partner argument.

## Exact countercontrol audit

The initial standalone checker reviewed had SHA-256
`f4fa3b75d23985b8a3d3aa8170eb61d4306d415e4e8964f7125b5c85a041f80d`.
Its [portable successor](../../claims/arbitrary-order/verify_protected_scaffold_resource_control.py)
retains the physical array and exact matching recursion, and additionally
checks the distinct-word count. The original scratch version is historical
provenance, not a required durable proof dependency.

An independent exact recursion reproduced all generated localization cases,
the three pure amplitudes, and

```text
T_W(111100000000) = 0,
T_(W restricted to A union C)(11110000) = 1,
T_W(222200000000) = 1.
```

This validates the stated countercontrol against deriving literal
two-component localization from the homogeneous admissible-minority
subsystem. The array is not a full GHZ source, and the control says nothing
against a localization argument that uses additional full-target equations.

The checker executes 46,875 cases indexed by a chosen majority colour and an
admissible pattern. These comprise 46,851 distinct colour words: 46,827 occur
once and 24 occur for two majority colours. Accordingly, `46,875 evaluations`
or `46,851 distinct words` is exact; `46,875 distinct words` is not.

## Independent stress checks

Two standalone exact-integer stress checks were run without importing the
author's scientific implementation:

- 120 seeded random protected-scaffold instances agreed between direct
  physical hafnian recursion and the minority permanent.
- 100 seeded random boundary tensors agreed between direct full hafnians and
  the square-free exterior-resource expansion.

These checks are finite falsification tests for indexing, multiplicity, and
sign errors. They are not proofs of the universal formulas. The proofs are
the matching bijections and shortest-cycle argument reviewed above.

## Correction adoption

The source owner adopted the review qualifications in
`claims/arbitrary-order/PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md`
at SHA-256
`77427f387953ce767040bfe7ad910d1e2e68c766d55aae0f65b213af6fb419e7`.
That durable statement now quantifies fixed `c` and nonempty `R`, permits a
boundary that is any union of whole components, limits the resource
special-case wording to a boundary containing `R`, and records both the
46,875 indexed evaluations and 46,851 distinct words. The historical scratch
draft reviewed above was intentionally left unchanged.
