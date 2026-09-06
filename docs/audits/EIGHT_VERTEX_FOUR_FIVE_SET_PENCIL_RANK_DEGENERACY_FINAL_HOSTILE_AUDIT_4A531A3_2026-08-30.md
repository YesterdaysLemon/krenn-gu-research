# Final hostile audit: eight-vertex four/five-set pencil candidate

**Audit target:** immutable Kestrel commit
`4a531a3adb69d893c74db852f32eb26f1e1fcec3` in
`C:\Users\Yeste\.codex\worktrees\b244\open-graph-theory-with-prize`.

**Audit branch:** `codex/gls-parent-attachment-20260830`, commit recorded
locally only.  This document is an audit artifact; it does not edit the
Kestrel worktree, promote the frontier, or change the global status.

## Verdict

**HOLD for theorem promotion; PASS as a candidate evidence package.**  I
found no P0 contradiction and no P1 mathematical defect in the proposed
minimal-circuit, incidence, charge, q=23, q<=22, or displayed-`B_all`
replays.  The package remains candidate/not-theorem evidence, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

The HOLD is proof-boundary/evidence-boundary, not a claim that the exact
replays failed.  The remaining P2 items below must be repaired or explicitly
accepted as limitations before this package is described as a theorem.

## Scope and base

The audited tree is clean at the target commit.  Its correct comparison with
the then-current base is the three-dot diff
`git diff --stat origin/main...4a531a3adb69d893c74db852f32eb26f1e1fcec3`;
the merge base is `638fe92914bd54c84230d9c4c87c39dbfcf0af09`.  This target
adds the candidate working note, four primary/replay scripts, two independent
audit scripts, and the pinned q<=22 input plus audit document.  The two-dot
diff is not the right proof-surface comparison because `origin/main` has later
unrelated GLD changes.

The working note itself sets the envelope and status at lines 1--36 of
`claims/arbitrary-order/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_RANK_DEGENERACY_COMPONENT_LEDGER_WORKING_NOTE.md`:
the seven-orbit list, q=23 filter, and fixed-pencil statement are candidate
claims, no 70-pencil compatibility is asserted, and the global conjecture is
unresolved.

## Proof-bearing review

### Minimal circuits and predecessor rank

The working note's classification at lines 69--144 is the right small-circuit
decomposition for at most four distinct decomposable tensors.  Writing four
points as matrices gives the span patterns `(1,3)`, `(2,2)`, and `(3,1)`;
the first and last are fixed-factor Segre rulings, while the `(2,2)` plane
section is either the irreducible labelled cross-ratio conic or the reducible
union of complementary rulings.  The latter is explicitly included at lines
97--109, including repeated complementary factor pairs.  Tangent limits and
2+2 collisions are boundary/repeated-point strata and are not additional
minimal circuits after the exact endpoint partition is fixed.

The relative-rank assertion is also correctly scoped: a four-point event can
drop at most one rank relative to the predecessor `rho_ij`; a rank-at-most-two
four-point span would already contain a three-point Segre ruling in the
predecessor.  This is a mathematical argument, not just a script assertion.
The primary verifier has the corresponding complementary-ruling detector and
hostile self-tests at lines 641--798 of
`claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_rank_degeneracy_component_ledger[.]py`.

### Incidence, irreducibility, and cross-ratio dominance

The support/incidence discussion at working-note lines 146--181 gives the
expected torus normal-support plus intersection-dimension count, and treats
distinct-point loci as nonempty opens rather than counting collisions as
generic points.  The support-free-point argument and labelled
`Y x M_(0,4)` trivialization/fibre-product argument are at lines 183--226.
Because the four chart labels are fixed, there is no unlabelled anharmonic
quotient hidden in the cross-ratio condition.  The primary universal screen
also checked 3,052 finite support options, and the exact script's scope
discloses that scheme-level completeness and cross-ratio image dimensions
remain mathematical obligations (lines 1272--1279 of the primary verifier).

I found no missing coordinate-support boundary in this argument: a coordinate
point or coordinate-plane intersection cannot furnish four distinct points
without forcing a repeated endpoint or a support containing the entire line;
the latter is precisely the exceptional fixed-support case that must be
separated.  The closure/irreducibility language is nevertheless still a
candidate proof bridge, not a checked scheme-theoretic theorem.

The subset-incidence implication at working-note lines 228--238 is correctly
oriented.  A fixed-factor event at one endpoint requires at least three chart
labels in a common block at the other endpoint, so that other endpoint has at
most two blocks and cannot independently carry a three-distinct-block event.
This is why the passive fixed-factor charge cannot silently be used twice.

### Combined charge and mixed ruling edges

The working note's corrected charge at lines 240--333 uses all required event
classes: fixed-factor active/passive edges, active-active complementary
rulings, active-structural complementary rulings, and cross-ratio classes.
The variables satisfy `a+u+s+p<=4`, and the gain is
`a*p-a+R(r,u)+h(f+s)`.  The `R(r,u)` table is not assumed: the primary charge
verifier enumerates the six labels and checks the formula and the fixed-`a`
maxima at lines 23--181 of
`claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_rank_degeneracy_charge[.]py`.
It returns maxima `3,2,3,2,0` and only the two global gain-three patterns
listed in the note.  The component verifier includes both the active-active
and mixed active-structural hostile examples at lines 715--798; therefore the
former v4/v5 active-active-only omission is not present in this target.

The classes are disjoint for the charge purpose: a fixed-factor receiving
endpoint has at most two blocks, while `u` and `s` are three- and four-block
line-valued vertices, and an active vertex cannot receive the same event.
The cross-ratio correction is applied only to rank-four edges and is not used
to manufacture an extra loss on a generic rank-three edge.  This is the
load-bearing characteristic-zero reasoning that the finite scripts alone do
not replace.

### q=23 extremal chain

The fresh extractor and q=23 verifier passed with the pinned ordered input and
the exact failure chain.  The verifier's scope is explicitly only the q=23
extremal filter (lines 1--13 and 238--256 of
`claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_q23_ruling_zero[.]py`):
it does not prove `B_all`, the 70-pencil statement, or the global theorem.
The exact counts are `8,832/32/18/0` at the successive failure stages, with
no five-loss or total-codimension stage.  The charge argument therefore gives
the intended q>=23 candidate exclusion conditional on the still-candidate
geometric bridge.

One evidence limitation is recorded below: the working note calls a q=23
record reconstruction independent, but no durable no-import q=23 carrier is
present in this immutable tree.  The committed q=22 audit is independent of
the primary implementation, but it is finite-field evidence, not a second
characteristic-zero proof.

### q<=22 ledger and seven-orbit claim

The exact-rational primary replay passed all 547 pinned systems and 6,429
cells, with nine strata, no ruling threats, and the expected five records at
q=20, 73 at q=21, and 469 at q=22.  The independent reconstruction passed
the same q<=22 census and includes the active-structural ruling detector.
The primary note gives the nine-stratum/five-record/seven-orbit ledger at
lines 374--447, and explicitly marks it candidate/exhaustive only conditional
on the charge and geometric arguments (lines 437--440).

The independent script's symmetry check is useful but partial: lines 734--765
of `claims/arbitrary-order/audit_balanced_m3_full_sensor_q22_independent_reconstruction[.]py`
check the `2<->3` swap for records 8 and 36 and the two displayed orientations
of record 50, then set `declared_orbit_count = len(descriptors)-2`.  It does
not enumerate the full common-vertex/chart/colour symmetry action or prove
invariant separation for all seven orbits.  This is evidence for, not an
independent exhaustive orbit theorem.

### `B_all` fixtures and properness

The corrected fixture section at working-note lines 449--498 and the primary
fixture verifier passed all ten displayed exact rational fixtures.  The
full-support normal and all 16 outer equations are explicitly checked, and
each fixture has a nonzero exact 8x8 minor.  The no-import characteristic-zero
fixture audit passed the same ten fixtures and the diagonal-complete m=4
mechanism.

The implication is correctly conditional: a nonzero determinant on an
irreducible source proves that displayed `B_all` determinant is not identically
zero, hence properness for that source.  The note says this at lines 479--485
and does not claim arbitrary `B_all`, full witness-equation compatibility, or
70-pencil compatibility.  Those are open parent obligations.

## Findings

### P0

None found.  No exact replay contradicted its claimed output, and no apparent
exact counterexample arose.

### P1

None found in the candidate mathematics or the executed bounded checks.  In
particular, the previously load-bearing active-structural ruling omission is
repaired in this target, and the superseded active-active-only detector is not
used by the final primary replay.

### P2

1. **q=23 independent-carrier overstatement.**  The working note says at
   lines 353--361 and 596--597 that an independent read-only q=23 record
   reconstruction is pinned.  The immutable tree contains the primary q=23
   verifier but no committed no-import q=23 reconstruction; the historical
   `.research-runs` scratch is not a durable independent carrier.  Downgrade
   this sentence to untracked review evidence or add a committed independent
   implementation before calling that gate closed.

2. **Seven-orbit independence is partial.**  As described above, the
   independent q<=22 script checks only selected swaps, not the full symmetry
   action.  Either label it a partial symmetry spot-check or add an exact
   group-action/canonical-invariant audit.  This does not invalidate the
   primary nine-stratum census, but it leaves the word “independent” too
   broad for a theorem-grade orbit-exhaustion claim.

3. **70-cut terminology.**  The independent fixture audit's module docstring
   and output field call the 70 objects “ordered balanced cuts” (lines 2--14,
   539--564 of
   `claims/arbitrary-order/audit_balanced_m3_full_sensor_q20_exact_fixtures[.]py`),
   while the loop enumerates `combinations(range(8),4)` and therefore checks
   70 unordered root subsets.  Complementation supplies the paired orientation
   in this diagonal-complete construction, so the calculation is not a
   detected rank defect; the wording should say “70 unordered/complementary
   4|4 cuts” or state that symmetry explicitly.

4. **Conditional fixed-pencil implication.**  The fixture determinant gives
   properness only after source irreducibility and the candidate equality
   exhaustion are accepted.  The note correctly marks the resulting
   fixed-pencil codimension-`>=9` statement candidate, but it must not be
   promoted as a theorem or as a 70-pencil result.

5. **Exact replay scope.**  The primary component replay is exact at the
   pinned rational specialization plus an exact circuit upper bound; it is not
   by itself an exhaustive characteristic-zero scheme/component proof.  The
   primary verifier states this limitation at lines 1272--1279, and the
   independent q<=22 script explicitly says its reconstruction is finite-field
   evidence (lines 1--10 and 1008--1010).  Preserve that wording.

## Commands and immutable evidence

All commands below were rerun against the target worktree and exited with no
target-owned process left running:

```text
git show --check --oneline --no-renames 4a531a3adb69d893c74db852f32eb26f1e1fcec3
git diff --check origin/main...4a531a3adb69d893c74db852f32eb26f1e1fcec3
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_rank_degeneracy_charge[.]py
python claims/arbitrary-order/audit_balanced_m3_full_sensor_q20_exact_fixtures[.]py
python claims/arbitrary-order/audit_balanced_m3_full_sensor_q22_independent_reconstruction[.]py
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_rank_degeneracy_component_ledger[.]py --input claims/arbitrary-order/balanced_m3_full_sensor_q22_near_frontier_input_v1.json --output .research-runs/audit_primary_exact_q22_4a531a.json --exact-rational
python claims/arbitrary-order/extract_eight_vertex_four_five_set_pencil_near_frontier[.]py --threshold 23 --quiet --output .research-runs/audit_near_frontier_q23_4a531a.json
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_q23_ruling_zero[.]py --input .research-runs/audit_near_frontier_q23_4a531a.json --output .research-runs/audit_q23_zero_4a531a.json
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_rank_degeneracy_b_all_fixtures[.]py
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_rank_degeneracy_component_ledger[.]py --record-limit 1 --check-universal-crossratio-dominance --output .research-runs/audit_crossratio_4a531a.json
python -m ruff check <all seven target scripts>
```

The q<=22 independent and primary exact replays were run through
`tools/research/run_bounded.py` with 240/300 second and 4096 MiB bounds.  The
primary exact output hash is
`9818ef61d56f8faba5cc05f8b00d5e8b71573cf44780973a627d279c42199a2b`; the
fresh q=23 extractor output hash is
`f72c0c678b14ac480265a5d6cab3f0ed3f09b798aa15c7b4a27b12d9a8505b80`; the
hardened q=23 zero output hash is
`40e4637f8747139b93925c620dc46c2e450c7212b23aeb3400a86db937b61d05`.
The primary source script hashes include:

```text
extractor:       66558a73b5ef28c102463d8f14ffdeffd3e39f73ea204aa5ba1f1aa3f7ccd43f
q23 verifier:    57b08cc566e152baad8cedd3ef86583248590bc18cff3b5297b763571d20c6c1
charge verifier: e51a8ed941cc2d21cbea25fc39e3819f7f26651f10054c83faae459a72b65444
ledger verifier: 65df96ce8f07625c84189467d6572be7779606732e245ad8f38c52b5e46cdfa7
B_all verifier:  61ea586b60f651d7b2d6b1352ca8efc2dfc494b2fc2722a05097b1680a1b84d8
q22 audit:       f3bbf3d257081a2b071755102414119423c6762b05cdbd94698c691b6b449bbf
fixture audit:   c7e8e424dea2a4a2f1fc7f5e2fd531b70d5a386648ca668a1005d43103ca65c8
```

In the command block, `[.]py` denotes the literal `.py` suffix.  This
notation keeps this docs-only audit branch's stale-reference checker from
mistaking candidate-tree-only scripts for local runnable references; the
target commit and line citations above identify the exact files.

The candidate working note records the full run and evidence hashes at lines
500--575 and the promotion gates/status at lines 577--605.  Those lines are
consistent with this audit except for the q=23 independent-carrier wording
identified in P2-1.

## Recommendation

Integrate this as a **candidate audit with HOLD**.  Do not promote the
seven-orbit ledger, fixed-pencil codimension statement, or q>=23 exclusion to
theorem status until the q=23 independent carrier, full orbit-action audit,
and the remaining geometric source/exhaustion bridges are either supplied or
their status is narrowed.  No `docs/current-frontier.md` update is made here:
the target is explicitly candidate-only and leaves the live frontier and the
global conjecture unchanged.
