# Route C — Grassmannian and Plücker elimination (symbolic route)

Branch: `symbolic/grassmannian-pluecker`, forked from the merged
canonical continuation (`main` @ f24782f, PR #27).

## Why this branch exists

The entire `P_5 -> Delta_3` support machinery is a chartwise description
of one intrinsic object: five two-planes `ker(A_i)` in `Gr(2,5)`, one
per local map `A_i : C^5 -> C^3`.  Every support pattern, pair-cover
condition, Hall quota, and singleton-row forcing is a Schubert-type
incidence condition on these five points.  Route C replaces the
per-chart zero-pattern bookkeeping with elimination on Plücker
coordinates, where:

- the rank condition is built in (a point of `Gr(2,5)` *is* a
  two-plane);
- changes of target basis disappear identically;
- coordinate-plane incidences become standard Schubert conditions;
- an empty intersection closes **all** support charts at once, and a
  nonempty one stratifies the survivors by matroid — a strictly more
  invariant classifier than raw zero patterns.

This route is named in `P5_ALTERNATIVE_STRATEGY_MAP.md` as proposed but
not executed.  It is the most structural remaining attack on the
support side and requires only exact linear/elimination algebra.

## What exists to translate

- `P5_KERNEL_HALL_HIERARCHY.md` — the Hall-hierarchy conditions on
  kernel spans (candidate Schubert conditions);
- `P5_COORDINATE_PLANE_PAIR_COVER.md` — the pair-cover forcing
  (span of every row pair contains a target coordinate covector);
- `P5_SOURCE_ROW_TRICOLOUR_COVER.md` — the three-colour cover;
- `FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md` — the forced singleton-row
  incidence (the `K_5` rainbow-triangle argument);
- `P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md` — the
  deletion-stable chart cover the Plücker formulation would subsume.

## Attack plan (symbolic only)

1. **Plücker parametrization.**  For each of the five kernels,
   introduce the ten Plücker coordinates `p_{ij}^{(k)}` subject to the
   five Plücker quadrics.  Work over `Q`; all conditions polynomial.
2. **Schubert translation.**  Rewrite, one by one, the verified
   incidence conditions (pair cover, Hall quotas, singleton forcing,
   exact-three-coordinate tree-chart hypotheses) as polynomial
   conditions in the Plücker coordinates.  Each translation is checked
   against the chartwise version on a random sample of charts before
   being accepted (exact rational evaluation, not numerics).
3. **Elimination.**  Intersect the translated conditions with the
   Plücker ideal using Singular (`std`/`slimgb`) or `msolve`.  The
   decision goal is ideal membership of `1`; the fallback goal is a
   primary decomposition whose components are matroid strata.
4. **Subsumption audit.**  If the intersection is empty, verify the
   proof subsumes the exact-three-coordinate tree-chart theorem
   (200 backbones, 812 charts) by checking every chart hypothesis
   appears among the translated conditions.

Explicitly out of scope: any support enumeration, SAT, or finite-field
sieves.  If the Plücker elimination needs a chart decomposition, that
is a plan failure to record, not an excuse to enumerate.

## Deliverables

- the Plücker translation table (condition <-> Schubert polynomial),
  each row independently sample-checked;
- the elimination result (unit-ideal certificate or strata
  decomposition) with its Singular/msolve transcript ledger;
- if empty: a theorem doc stating the coordinate-free closure, with
  the subsumption audit attached;
- no global-status claim; the conjecture stays **UNRESOLVED**.
