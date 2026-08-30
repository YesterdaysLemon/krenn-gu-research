# Krenn–Gu prize conjecture research

## Status

The global Krenn–Gu conjecture is **UNRESOLVED**. The repository contains
proved reductions, exact finite results, conditional exclusions, route
refutations, experiments, and open obligations. None currently forms a
complete characteristic-zero proof or an exact counterexample to the original
global statement.

**Start here:** [`docs/current-frontier.md`](docs/current-frontier.md) is the
maintained map of the live proof topology, open leaves, and refuted routes.
Owning theorem documents remain authoritative for mathematical statements.

For an interactive projection of that map, run
[`tools/proof-visualizer`](tools/proof-visualizer/README.md). Its bonsai colours
are navigation aids; the exact node text and owning claims remain authoritative.

## The conjecture

Let `n >= 6` be even and `d >= 3`. Assign a complex `d x d` matrix `W_ij` to
each unordered pair of vertices. For a word `a=(a_1,...,a_n)`, define

```text
T_W(a) = sum over perfect matchings M of
         product over {i,j} in M of W_ij[a_i,a_j].
```

The conjecture says that no such weighted graph realizes the diagonal GHZ
tensor

```text
T_W = sum_(c=0)^(d-1) e_c tensor ... tensor e_c.
```

The live symbolic programme is concentrated on the ternary case and on exact
reductions that any hypothetical witness must satisfy. Scope and field
qualifications are recorded in the owning claims and in the current frontier.

## Claim-family navigation

- [Arbitrary-order reductions and boundaries](claims/arbitrary-order/README.md)
- [Finite-order claims and certificates](claims/finite/README.md)
- [P3 restrictions](claims/p3/restrictions/README.md)
- [P4 component programme](claims/p4/README.md)
- [P5 obstruction programme](claims/p5/README.md)
- [P6 claim packages](claims/p6/README.md)
- [P7 claim packages](claims/p7/README.md)

The four-chart `K5` pencil lane now has an exact finite support-Segre
generic-rank census: [theorem and replay package](claims/arbitrary-order/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_SUPPORT_SEGRE_GENERIC_RANK_CENSUS_THEOREM.md).
It gives `q >= 20`, hence affine codimension at least eight on the generic
exact-partition strata, with exactly two equality orbits.  Rank-degenerate
components, the `B_all` cut, compatibility among the 70 pencils, full target
equations, and witness exclusion remain open; this is not a codimension-nine
or codimension-ten result.

In the equal-leaf H4 low-rank lane, GLD89 gives an exact determinant-safe
exclusion of the full `P=p^2-p+1` divisor and its `d0=p+q-1=0` overlap.
[`GLD90`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_OPEN_LOW_RANK_EXCLUSION_THEOREM.md)
now closes the whole complementary `D((p-q)d0 P L1 L2 e Q6)` stratum,
including the old-six-pivot boundary and the formerly exceptional `T=0`
divisor.  [`GLD93`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_L1_L2_RANK_SEVEN_EXCLUSION_THEOREM.md)
then closes the complete `L1=0` and `L2=0` coefficient boundaries on the
upstream-open H4 chart by direct rank-seven certificates, including their
exceptional `T=0` fibres; it does not rely on a naive p/q carrier symmetry.
[`GLD94`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_E_BOUNDARY_DETERMINANT_SAFETY_THEOREM.md)
now closes the retained `e=0` boundary inside `D(Omega)` by an exact
parameterisation, simultaneous-pivot obstruction, and all-block common-kernel
argument.  Its unsaturated low-rank leaf family is nonempty but every
compatible centre is singular.  [`GLD95`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_EXCLUSION_THEOREM.md)
now closes the finite common-minor residual on the written GLD88 `F88`
rational family over `D(Delta)`, including every retained old-`P6=0` content
fibre via exact branch decomposition and unit six-minors.  This does not
claim arbitrary H4 `Q6=0` closure outside `F88`; the pulled-back Fitting
ideal, other chart/component/source branches, and the global conjecture remain
open, and the global status is still **UNRESOLVED**.
[`GLD96`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md)
then closes an R31-free generic localization on
`D(E31*H2*g0*Delta)` into the GLD95 `F88` theorem.  Its polynomial bordered-
determinant identity uses no inverse of `R31`, so `R31=0` is included wherever
the remaining gates are nonzero.  The normalized `H2=Q6=0` degree-drop branch
is now handled separately by GLD99, and GLD100 below removes the normalized
`g0` gate on the remaining `H2`-open.  Thus the combined normalized route
retains only the `E31=0` and `Delta=0` boundaries before the physical
`Omega`-open and the wider chart/component obligations.
[`GLD97`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P2_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md)
now gives a parent-level exact p=2 fibre closure: for symbolic `a` and
arbitrary offset coordinates `B,C`, four bordered and two direct seven-minors
adjoined to `Q2` give the exact ideal
`(Q2,T0,T1,T2,T3,D0,D2)=(Q2/5,B,C)`.  Thus syndrome rank at most six forces the F88
origin without inverting `R31`, `E31`, or `g0`, and GLD95 excludes the
resulting incidence on `D(Omega Delta_2)`.  This closes only the normalized
p=2 H4/Q6 fibre; arbitrary `p`, the pulled-back Fitting lane, other charts and
components, and the global conjecture remain open.

[`GLD99`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md)
now closes the normalized `H2=Q6=0` degree-drop branch in the GLD88/F88
offset chart on `D(Delta)`.  Both `Q(i)` branches are recomputed with
symbolic `a`; all six selected minor payloads have total `BC` degree `3`,
with genuine `C^2` terms in `D0,D2`, and the exact `158 x 144` system has
rank `140` with both target augmentations still rank `140`.  The branch-
specific payload and certificate hashes are pinned, no `R31/E31/g0`
localization is used, and GLD95 remains the separate endpoint.  This does not
cover arbitrary H4/Q6 points outside F88, `Delta=0`, the pulled-back Fitting
lane, other charts/components/source branches, or global resolution; the
global status remains **UNRESOLVED**.

[`GLD100`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_G0_GATE_REMOVAL_THEOREM.md)
is the parent-level synthesis of GLD96, GLD99, and the GLD95 `F88` endpoint,
not a third sibling refinement.  On the normalized `D(E31*H2*Delta)` open,
GLD96 first forces `B=0`; the source-recomputed pair-resultant cover has the
eight necessary factors
`p(p-1)(p^2+1)(p^2-2p+2)P H2 A4 C4`, and exact quotient-field fibre closures
force `C=0` on every admissible branch.  This removes `g0` on that open.
Combining it with GLD99's exact `H2=0` handoff gives the normalized
`D(E31*Delta)` route.  The `C_8=1` incidence bridge and GLD95 then retain the
physical exclusion on `D(Omega)`.  This remains a scoped characteristic-zero
result: `E31=0`, `Delta=0`, `Omega=0`, arbitrary H4 Q6 points outside the
normalized F88-offset chart, the GLD83 Fitting pullback, other
charts/components/source branches, other roots/orders, and global resolution
remain open; the global status is still **UNRESOLVED**.

[`GLD101`](claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md)
is a separate exact scoped characteristic-zero `a=0` continuation on the
normalized GLD88/F88 equal-leaf H4 chart.  On `V(a,Q6)` over
`D(H2*Delta)`, every rank-at-most-six point with
nonzero offsets `(B,C)` has its `p` coordinate in the radical support of the
exact degree-548 six-selector norm,
`(p-1)*p*(p^2+1)*P*H2*R4*R8*R110`.  This is a one-way necessary support cover
only: it does not force `B=C=0`, close any factor, provide a selector or norm
converse, or yield physical emptiness.  It is not arbitrary in `a` and does
not close the full `E31=0` wall; `H2=0`, `Delta=0`, other charts and source
branches, and all wider physical/global obligations remain open.  The
[`GLD101 hostile review`](docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION_REVIEW_2026-08-30.md)
passes this exact scoped claim, and the global status remains **UNRESOLVED**.

The newest zero-anchor, root-order-three, all-six-rigid source-integrability
line is `GLS61`--`GLS80`.  `GLS66` closes the exactly-two-deficient branch;
`GLS67`--`GLS69` localize the surviving three-, four-, five-, and
six-deficient families; and `GLS70`--`GLS77` remove several exact
six-deficient keys.  The required `GLS78` parent attempt leaves Family-A
`r=2,3` open, while `GLS79`--`GLS80` prove that the complete stated
scalar-linear separator route cannot remove them.  Nonlinear or specialized
same-source integrability, the other deficient families, attachment and
arbitrary-root transport, and global gluing remain open.  The
[`GLS66`--`GLS69` evidence-status reconciliation](docs/audits/GLS66_GLS69_EVIDENCE_STATUS_RECONCILIATION_2026-08-29.md)
records the owner/review/frontier alignment without changing those scopes.

The [`catalog/theorem-ledger.json`](catalog/theorem-ledger.json) is a partial
claim/evidence index. Its empty `dependencies` arrays mean “not recorded,” not
“no dependencies”; it is not the proof DAG.

## Evidence and proof contracts

- [Agent and contributor operating contract](AGENTS.md)
- [Evidence semantics](docs/evidence-semantics-contract.md)
- [Proof-obligation architecture](docs/proof-obligation-architecture.md)
- [Formalization interface](docs/formalization-interface.md)
- [Layout-migration runbook](docs/architecture/layout-migration-runbook.md)

These contracts require exact scope, separate evidence axes, honest
generic-versus-pointwise boundaries, and a proved bridge from any computation
to the mathematical obligation it is claimed to discharge.

## Basic verification

From repository root:

```text
python check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v tests.test_fourteen_vertex_cycle_cover_lattice
```

Run a claim's focused verifier and independent audit from the commands in its
own theorem document. A passing bounded script supports only the scope stated
there; it does not automatically prove an arbitrary-order or global claim.

## Contributing

1. Work in the owning claim package and state the exact obligation, field,
   quantifiers, assumptions, and excluded boundaries.
2. Keep written proof, primary verifier, independent audit, and formalization
   status distinct.
3. Preserve failed and refuted routes when they constrain future work.
4. If a PR changes the live mathematical frontier, update
   [`docs/current-frontier.md`](docs/current-frontier.md). If mathematical
   claims change without altering the live frontier, explicitly state why no
   frontier update is needed.
5. Stage the complete candidate tree before the final hygiene and link checks.

## History and programme audits

- [Repository README chronicle through 2026-08-10](docs/history/repository-readme-chronicle-through-2026-08-10.md)
- [Frontier stabilization snapshot from 2026-08-05](docs/history/current-frontier-stabilization-snapshot-2026-08-05.md)
- [Dated 2026-08-10 symbolic handoff](docs/history/handoffs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md)
- [PR #72–#82 proof-topology audit](docs/audits/PROGRAMME_PROOF_TOPOLOGY_AUDIT_2026-08-10.md)

Historical documents preserve chronology and prior wording. They are not
current authority when they conflict with the maintained frontier or an owning
theorem document.
