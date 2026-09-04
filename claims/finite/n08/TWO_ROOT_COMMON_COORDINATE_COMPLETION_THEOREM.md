# Complete common-coordinate eight-vertex two-root exclusion

## Status and exact statement

**Proved finite exclusion over C**, combining analytic proofs with one
independently checked Boolean certificate. The global Krenn--Gu conjecture
remains **UNRESOLVED**. No Lean formalization is claimed.

Let W be a ternary complex block graph on eight vertices with full matching
tensor Delta_(8,3), and suppose its maximum fully-supported pairwise-zero
torus-root cardinality is exactly two. Choose a maximum pair 1,2. Assume
that for each of the other six vertices u there is a coordinate c(u) with

```text
W_1u(-,z_u)=a_u z_u[c(u)],
W_2u(-,z_u)=b_u z_u[c(u)].
```

This is a hypothesis about physical blocks; individual a_u or b_u may
vanish. Then W does not exist. **There is no additional rank or kernel
hypothesis on W_12.**

## Exhaustive proof cover

Put Q=W_12. The ranks zero, one, two, and three exhaust all 3-by-3 matrices.

1. If rank Q>=2, the
   [rank-at-least-two source theorem](TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md)
   gives the contradiction. It includes every rank-two kernel boundary and
   dependent-channel four-cycle.
2. If rank Q=1, a nonzero matrix monomial has no zero on the product torus
   and cannot be the edge of the chosen pair. Every other rank-one block
   factors as p q^T with both factors noncoordinate, or exactly one
   coordinate. The [rank-one theorem](TWO_ROOT_COMMON_COORDINATE_RANK_ONE_EXCLUSION.md)
   excludes both cases, retaining every central-port and zero-leg case.
3. If Q=0, the [zero-block theorem](TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md)
   retains the initially unobserved inactive hafnian. Its exhaustive
   orientation cover is closed by exact cofactor algebra or reduced to the
   pure-(3,3) full-cofactor system. The latter maps to the
   [independently certified necessary support instance](two-root-zero-source-certificate/README.md),
   which is UNSAT.

The zero-block re-rooting step uses only the already proved rank-at-least-two
theorem on the same physical graph; it does not use this completion as a
premise. Rank-one source arguments use a separately stated polynomial
cofactor lemma, not a nonzero-rank theorem outside its hypotheses. Thus
the dependency cover is noncircular.

## What this closes and what remains

This completes the common-coordinate child of the active higher-surplus
parent at n=8 and maximum r=2. Root-rank boundaries are no longer residual
within this child. It does not show that a general witness supplies such
physical incidences at any pair. Common-plane and other incidence types,
the maximum-r=1 branch, larger orders, and the global source-to-detector
programme remain separate.

The evidence is multi-axis: analytic source and rank arguments; an explicit
finite necessary-condition bridge; a supplied decision-tree certificate;
independent clause reconstruction and exact Boolean checking; and written
adversarial reviews. None of those statements is a claim of formal Lean
verification or global resolution.

Reviews: [rank one](../../../docs/audits/TWO_ROOT_COMMON_COORDINATE_RANK_ONE_REVIEW_2026-09-04.md),
[zero-block analytic reduction](../../../docs/audits/TWO_ROOT_COMMON_COORDINATE_ZERO_REVIEW_2026-09-04.md),
[encoding and certificate](../../../docs/audits/TWO_ROOT_ZERO_SOURCE_CERTIFICATE_REVIEW_2026-09-04.md),
and [portable package](../../../docs/audits/TWO_ROOT_ZERO_SOURCE_PACKAGE_REVIEW_2026-09-04.md).
