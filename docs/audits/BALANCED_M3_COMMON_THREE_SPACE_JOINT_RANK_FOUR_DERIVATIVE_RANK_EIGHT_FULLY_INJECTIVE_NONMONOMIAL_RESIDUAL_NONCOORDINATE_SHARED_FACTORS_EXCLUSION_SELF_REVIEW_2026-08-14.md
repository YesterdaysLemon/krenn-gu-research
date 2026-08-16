# Self-review: nonmonomial noncoordinate-shared-factors exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion of the structural-zero
successor with both shared factors noncoordinate, subject to the repository
validation below.

Together with S2CL--S2CM, this reduces every surviving actual-nonmonomial
point in the fully-injective joint-rank-four/derivative-rank-eight cell to a
coordinate `x` or coordinate `y` structural cell.  It does not exclude those
coordinate cells.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2BQ gives `Cbar=lambda ev_d tensor ev_e` on `x^perp by y^perp` when both
   shared factors are noncoordinate.  The kernel line of `ev_d|x^perp`
   cannot be two-supported: a partner nonzero on those two coordinates would
   create S2CK's forbidden transverse secant.  Hence it is one coordinate
   row `e_a`, with `a!=d` and `support x=complement{a}`.
2. This coordinate row has an exact one-sided table
   `M(r_a,p_b)=b_a lambda_a T_a`.  Since `y` is noncoordinate, evaluation at
   `a` is nonzero on `y^perp`; its kernel supplies a structural zero partner
   and a complementary row supplies a nonzero target map.
3. If the zero pair is independent, S2CG makes it a conjugate pair in a
   split two-source plane.  If the complementary row has no omitted-source
   component, its plane equals `ker lambda_a`; otherwise evaluations at the
   conjugate sum and the complementary row align all three pure source lines
   and split `Q`.  These alternatives are exhaustive.
4. In either independent alternative, choose a colour complementary to `a`
   and different from the coordinate colour `t`.  Quotienting the three
   `T_a` factor lines kills the complete physical slice.  The corrected cube
   gives `Sbar=-c Tbar` with `c!=0`, and the retained face forces the actual
   residual block to be a diagonal monomial.
5. If the zero pair is dependent, its common row is pure.  The nonzero
   one-sided map fixes at least one source projection of `Q` to a `T_a`
   factor line; if both complementary components are nonzero, evaluation at
   their row aligns both before quotienting.  Thus every `Q^3` permanent lies
   in at least one one-factor slab through `T_a`.
6. Modulo that slab, both complementary coordinate bilinear forms are
   nonzero scalar multiples of `Cbar`.  Their proportionality forces
   `support x=support y=complement{a}`; this holds whether or not `t=a`.
7. Only after that support conclusion, `p_a` is introduced as a genuine
   complement in `P`.  The full complementary row in `R` and `p_a` form a
   second structural zero, while the original pure row and `p_a` give the
   visible `lambda_a T_a` corner.  Target products and correction terms
   vanish separately at the new zero.
8. S2CI's exhaustive two-cross-pair dichotomy now gives a split
   three-source `Q` or coincident split planes `R=P=ker lambda_a`.  The same
   retained complementary face and source quotient force the actual `C`
   monomial, excluding the dependent case.

## Adversarial checks and scope controls

- An initial attempted closure treated a one-sided physical-source extension
  as if both source projections were fixed.  An independent auditor supplied
  an exact local countermodel to that coverage step.  The claim was retracted.
  The final proof instead uses the one-factor slab to manufacture the second
  structural corner and invokes the already proved S2CI dichotomy; it covers
  the one-sided and two-sided extensions uniformly.
- A draft also silently used `a!=t`.  The final theorem works with the two
  colours complementary to `a` and chooses one different from `t`; it covers
  `a=t` without a new premise.
- The proof distinguishes the actual residual block `C` from its restriction
  `Cbar`.  Only the retained complete face promotes the quotient relation to
  the forbidden actual-monomial identity.
- No numerical solve, modular inference, degeneration, saturation,
  localization, algebraic-closure step, or generic-to-pointwise promotion is
  used.
- The focused scripts replay finite algebraic and incidence interfaces.  The
  written theorem owns the S2BQ atlas and the S2CG/S2CI/S2CK geometric inputs.

## Evidence matrix

| Evidence axis | Result |
|---|---|
| Mathematical status | proved exact exclusion |
| Scope | both-noncoordinate structural-zero successor in the fully-injective rank-four/rank-eight actual-nonmonomial cell |
| Case coverage | independent/dependent zero pair; equal-plane/split-space; one-/two-factor slab; every `a,t` relation |
| Primary replay | deterministic SymPy exact arithmetic |
| Independent audit | no-import standard-library exact rational arithmetic |
| Formalization | not formalized in Lean |
| Global status | **UNRESOLVED** |

## Validation

The focused primary and independent replays, Ruff, candidate-tree hygiene,
the migration and lattice unit suites, and the zero-change link rewrite must
all pass on the staged candidate tree before checkpointing.

## Remaining obligation

Inside this local rank cell, the residual is now

```text
actual nonmonomial structural-zero point with x coordinate or y coordinate:
OPEN.
```

This local reduction does not discharge joint-rank-three/rank-eight or
derivative-rank-seven cells, pair regularity elsewhere, other components or
poles, higher balanced orders, all-rank drop, or the global extraction bridge.
