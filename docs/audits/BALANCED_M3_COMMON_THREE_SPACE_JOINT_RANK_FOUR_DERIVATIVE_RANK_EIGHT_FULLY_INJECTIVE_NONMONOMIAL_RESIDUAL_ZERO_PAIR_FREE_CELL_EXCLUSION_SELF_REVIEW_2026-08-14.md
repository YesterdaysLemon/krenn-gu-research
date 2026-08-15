# Self-review: nonmonomial zero-pair-free-cell exclusion

Date: 2026-08-14

## Verdict

Accept the stated exact characteristic-zero exclusion of the zero-pair-free
successor in the fully-injective joint-rank-four/derivative-rank-eight actual
nonmonomial residual cell, subject to the repository validation below.

Together with S2CL, the result proves that every surviving point in this local
cell has between one and four structural mixed zero pairs.  It does not
exclude the structural-zero cells themselves.  Global Krenn--Gu remains
**UNRESOLVED**.

## Load-bearing chain checked

1. S2CL supplies the exact corrected cube
   `M(r_alpha,p_beta)(q_k)=alpha_k beta_k T_k+C(alpha,beta)S_k`, proves that
   correcting zero pairs are impossible, and identifies structural zeros
   exactly with correction-free coordinatewise-disjoint covector supports.
2. S2BQ exhausts the actual-nonmonomial rank-eight tangent quotient by three
   alternatives: `x` coordinate, `y` coordinate, or both noncoordinate with
   `C(alpha,beta)=lambda alpha_d beta_e` on `x^perp by y^perp`.
3. In the both-noncoordinate branch, a nonzero row on
   `x^perp intersect {alpha_d=0}` cannot be coordinate, because its disjoint
   partner line would be a structural zero.  It therefore has both
   complementary coordinates nonzero.  The noncoordinate `y` premise makes
   the corresponding two coordinate evaluations nonzero linear forms on
   `y^perp`; an infinite-field avoidance chooses a partner nonzero on both.
4. That partner has zero correction and the resulting mixed map contains
   exactly the two fully transverse target endpoints on the complementary
   colours.  S2CK's mixed-map transverse-secant obstruction excludes it.
5. After root exchange, the remaining branch has `x=e_s`.  Absence of a
   structural zero forces `y_s!=0`, so projection from `y^perp` to the two
   complementary coordinates is an isomorphism and the restricted residual
   block is a nonzero `2 x 2` matrix `D` over the base field.
6. Both cross entries of `D` are nonzero: either zero entry gives a coordinate
   row and the uniquely lifted disjoint-support partner, hence a structural
   zero.  The lift's `s` coordinate is harmless because the coordinate row has
   zero `s` coordinate.
7. If `D` has rank two, choose the first covector outside the four proper
   lines given by its two coordinate entries and the two entries of its row
   product with `D`; the full kernel vector of that row product supplies the
   second covector.  If `D` has rank one, a base-field factorization
   `D=uv^T` has full `u,v`, and a full left-kernel vector plus any full partner
   gives the same construction.
8. In both matrix ranks the correction vanishes, both complementary target
   coefficients are nonzero, and the third coefficient is zero.  S2CK again
   excludes the transverse secant.  Root exchange covers coordinate `y`.

## Adversarial checks and scope controls

- Three independent research lanes reconstructed the S2BQ split, both support
  arguments, both matrix-rank constructions, the lifted coordinate-wall
  partner, and the S2CK application.  All returned mathematical PASS verdicts.
- The rank-two field argument explicitly avoids four proper lines.  It uses
  only that a characteristic-zero field is infinite; no algebraic closure is
  assumed.
- The rank-one factorization is over the base field: a nonzero row (or column)
  of a rank-one matrix supplies the factorization directly.
- The proof evaluates the actual block only through its exact restriction to
  `x^perp by y^perp`; no tangent-quotient equality is promoted to an equality
  of actual blocks.
- No numerical solve, modular inference, degeneration, saturation,
  localization, or generic-to-pointwise promotion enters the proof.
- The focused scripts replay the finite support and matrix interfaces.  The
  written proof owns the S2BQ atlas and S2CK mixed-map obstruction.

## Evidence matrix

| Evidence axis | Result |
|---|---|
| Mathematical status | proved exact exclusion |
| Scope | zero-pair-free successor in the fully-injective rank-four/rank-eight actual nonmonomial residual cell |
| Case coverage | exhaustive S2BQ root-torus split and both `2 x 2` matrix ranks |
| Primary replay | deterministic symbolic exact arithmetic |
| Independent audit | no-import standard-library exact rational arithmetic |
| Formalization | not formalized in Lean |
| Global status | **UNRESOLVED** |

## Validation

The focused primary and independent replays, Ruff, candidate-tree hygiene,
the migration and lattice unit suites, and the zero-change link rewrite must
all pass on the staged candidate tree before checkpointing.  A timeout,
missing script, or sampled matrix search is not accepted as evidence.

## Remaining obligation

Inside this local rank cell, the only surviving successor is

```text
actual nonmonomial residual with between one and four
explicit structural mixed zero pairs: OPEN.
```

This local reduction does not discharge joint-rank-three/rank-eight or
derivative-rank-seven cells, pair regularity elsewhere, other components or
poles, higher balanced orders, all-rank drop, or the global
extraction/unavoidability bridge.
