# Balanced `m=3` full-sensor q<=22 independent audit

## Status and boundary

**Audit evidence only; no theorem or global-status promotion.**  This
package preserves a fresh reconstruction of the pinned q<=22 near-frontier
screen and a separate exact fixture/B_all audit.  It does not prove the
analytic parent bridge, classify arbitrary `B_all`, close the target
equations, or resolve the Krenn--Gu conjecture, which remains
**UNRESOLVED**.

The finite screen is the four-chart support/partition ledger used by the
S3 equality route.  Its q=20 fixture replay is an exact characteristic-zero
check.  The q<=22 reconstruction uses a hand-written finite-field reducer
over `F_1000033`; it is exact for that finite-field screen, but is not a
characteristic-zero proof of a generic-rank statement.

## Durable inputs and implementations

The pinned input is
[`balanced_m3_full_sensor_q22_near_frontier_input_v1.json`](../../claims/arbitrary-order/balanced_m3_full_sensor_q22_near_frontier_input_v1.json).
It has 666,521 bytes and SHA-256
`d5b821a47f8164f56e1254e9400ff1875bab650ce5e64be3a0e191129bed541a`.
The canonical SHA-256 of its `records` value, using sorted JSON keys and
compact separators, is
`650e8ed6e2165a3066fc9ba1cda30709b9f6e24fe599a6860afb2b1deb471550`.
The input contains 547 canonical records with q histogram `2/39/506` for
q=`20/21/22`; no derived Kestrel output or failure ledger is an input.

The two durable, independently written scripts are:

- [`audit_balanced_m3_full_sensor_q22_independent_reconstruction.py`](../../claims/arbitrary-order/audit_balanced_m3_full_sensor_q22_independent_reconstruction.py), SHA-256 `d6c4437f3acf4cc45d32f31bd403d3be4c12224d0513dbc1178310b8a2cd0347`;
- [`audit_balanced_m3_full_sensor_q20_exact_fixtures.py`](../../claims/arbitrary-order/audit_balanced_m3_full_sensor_q20_exact_fixtures.py), SHA-256 `801846ae6e70e26812f0fad334dd9820c712d185e54e97881917a9c206f4ad4e`.

The first imports only the standard library and NumPy, and no repository or
Kestrel module.  The second imports only the standard library and SymPy, and
reconstructs the q=20 fixtures, exact sensor matrices, complementary-ruling
fixtures, and diagonal-complete B_all mechanism from definitions.  The
external pinned input was copied byte-for-byte into the repository; the
external checkout was not edited.

## Fresh q<=22 reconstruction

The screen re-derived every support option and its codimension, generated
three exact finite-field samples per option, formed all six edge matrices,
checked the base ranks, and explained every rank drop by the implemented
fixed-side, three-point, two-three, or complementary-ruling mechanisms.
It also includes active-structural as well as active-active ruling logic.

The bounded finite-field replay output was:

```text
records                         547
q histogram                     20:2, 21:39, 22:506
explained rank-drop cells       6429
complementary-ruling cells      0
records with ruling drops       0
minimum-cost histogram          20:5, 21:73, 22:469
```

The five minimum-cost records are indices `8, 36, 50, 142, 431`.  The two
q=20 records are indices `50` and `142`:

```text
index  Delta vector       edge ranks (01,02,03,12,13,23)  cells  option shape
50     (0,3,0,0)           (1,3,3,3,3,4)                   28     (1,1,36,36)
142    (0,0,0,0)           (2,3,3,4,4,4)                   14     (1,1,36,36)
```

The other three minima are q=21 records:

```text
index  Delta vector       edge ranks (01,02,03,12,13,23)  cells  option shape
8      (0,3,6,0)           (1,1,3,1,3,3)                   21     (1,1,1,36)
36     (0,3,0,6)           (1,3,1,3,1,3)                   21     (1,1,36,1)
431    (3,3,3,0)           (1,1,3,1,3,3)                   21     (1,1,1,36)
```

The no-import audit extracts and asserts these nine equality strata directly:

```text
record  (Delta,c_rank)  edge-rank vector              description
8       (9,2)           (1,1,2,1,2,2)
36      (9,2)           (1,2,1,2,1,2)
50      (3,0)           (1,3,3,3,3,4)
50      (3,2)           (1,3,2,3,2,4)                  one-line, vertex 3
50      (3,2)           (1,2,3,2,3,4)                  one-line, vertex 2
50      (3,4)           (1,2,2,2,2,4)                  both planes
50      (3,5)           (1,2,2,2,2,3)                  plane plus cross-ratio {2,3}
142     (0,0)           (2,3,3,4,4,4)
431     (9,2)           (1,1,2,1,2,2)
```

The script verifies two selected identifications by the explicit vertex swap
`2 <-> 3`: records `8` and `36`, and the two single-line orientations in
record `50`.  Applying only those displayed identifications leaves seven
candidate classes among the nine strata.  The audit does **not** enumerate the
full chart/common-vertex/colour symmetry action or independently prove that
the remaining five rows are distinct orbits.  These are finite ledger strata,
not a claim that every rank-degenerate component is classified.

### Corrected option census

The non-generic line-option total is 19,662:

```text
selected triple options       15,913 = q20:112 + q21:1,794 + q22:14,007
selected four-block options     3,749 = q20:28  + q21:434   + q22:3,287
```

The non-generic option counts by normal mask `1..7` are
`(2779, 2813, 2773, 2999, 2771, 2756, 2771)`.  By q they are:

```text
q=20  (20,20,20,20,20,20,20)
q=21  (315,315,315,338,315,315,315)
q=22  (2444,2478,2438,2641,2436,2421,2436)
```

The sum of all four-vertex option products is `1,994,316`.  Cross-ratio
eligible counts are `4,080` among non-generic line options and `4,193`
including the generic option; the q-wise totals (non-generic, including
generic) are `(28,29)`, `(463,475)`, and `(3589,3689)` for q=`20,21,22`.

The input has 30 cells in which both endpoints have 2+1+1 partitions.  All
30 repeat the same chart pair at both endpoints (five occurrences for each
of the six pair labels), and there are zero complementary repeated-pair
cells.  This is a property of the pinned q<=22 support, not a general
exclusion of complementary rulings.

## Separate exact fixture and B_all audit

The SymPy audit reconstructs ten q=20 fixture/deformation types.  Every
displayed exact sensor has rank eight on its 15-column parity sensor, and the
compensation ledger is:

```text
fixture                                      (Delta,c_rank)  edge ranks                         q
A_generic                                    (0,0)           (2,3,3,4,4,4)                     20
A_one_collinear_cross_incompatible           (0,2)           (2,2,3,4,4,4)                     21
A_one_collinear_cross_compatible             (0,3)           (2,2,3,3,4,4)                     21
A_both_collinear_cross_compatible            (0,6)           (2,2,2,3,3,3)                     21
B_generic                                    (3,0)           (1,3,3,3,3,4)                     20
B_one_collinear                              (3,2)           (1,2,3,2,3,4)                     20
B_both_collinear_cross_incompatible          (3,4)           (1,2,2,2,2,4)                     20
B_both_collinear_cross_compatible            (3,5)           (1,2,2,2,2,3)                     20
C_two_one_three_synchronized_plus_line      (9,2)           (1,1,2,1,2,2)                     20
D_injective_three_synchronized_plus_line    (9,2)           (1,1,2,1,2,2)                     20
```

The active-ruling fixture has left partition `(0,0,1,2)` and right
partition `(0,1,2,2)`, with complementary repeated pairs `(0,1)` and
`(2,3)`.  Exact ranks are:

```text
generic four-chart products                 4
dense-normal active / dense-normal active  3
dense-normal active / structural plane     3
```

The structural plane has rank two and the dense vectors lie on the exact
normal `(1,1,1)`.  This validates the active-structural warning used by the
screen logic; it is not a q<=22 survivor.

For the diagonal-complete `m=4` B_all boundary, the audit symbolically
constructs eight companion columns.  Seven non-all-cross columns are
divisible by the common quadratic `Q=x^2+y^2+z^2`; an exact numeric
specialization has sensor rank seven, so the column defect is one.  It
recomputes rank seven for all 70 unordered four-root subsets, representing
the complementary balanced `4|4` cuts; complementation supplies the mate
orientation in this diagonal-complete construction.  The direct
coefficient checks give pure coefficient `105`, mixed coefficient `15`, and
ratio `1/7`; at `m=3` the threshold sensor rank is four.  This confirms the
known diagonal-complete ambient B_all mechanism and its mixed-word failure;
it does not classify arbitrary B_all points or intersect B_all with the full
witness equations.

## Reproducible commands and process ownership

From the repository root, the bounded runs were:

```powershell
python tools/research/run_bounded.py --run-id kestrel-s3-independent-q22-p2-scope-v3 --timeout-seconds 240 --memory-mb 4096 --run-root .research-runs --cwd . -- python claims/arbitrary-order/audit_balanced_m3_full_sensor_q22_independent_reconstruction.py
python tools/research/run_bounded.py --run-id kestrel-s3-independent-exact-fixture-p2-scope-v3 --timeout-seconds 60 --memory-mb 4096 --run-root .research-runs --cwd . -- python claims/arbitrary-order/audit_balanced_m3_full_sensor_q20_exact_fixtures.py
python -m py_compile claims/arbitrary-order/audit_balanced_m3_full_sensor_q22_independent_reconstruction.py claims/arbitrary-order/audit_balanced_m3_full_sensor_q20_exact_fixtures.py
python -m ruff check --output-format concise claims/arbitrary-order/audit_balanced_m3_full_sensor_q22_independent_reconstruction.py claims/arbitrary-order/audit_balanced_m3_full_sensor_q20_exact_fixtures.py
```

Both bounded runs returned exit code zero and `PASS`.  The q<=22 run took
138.882 seconds (runner PID 5964, child PID 12524); its `run.json` has
SHA-256 `aec192ea545a40bb218e9abcc5235fe355ac1b309140ca1a8087b2244461b7a4`.
The exact fixture run took 4.293 seconds (runner PID 42768, child PID 38508);
its `run.json` has SHA-256
`3b5f5696184b0f8aaa43dff942b5b437c5ce1fdc5873c1902f3625e3d7149f2c`.
All four processes exited before this audit package was finalized.  Other
workers observed on the host were not stopped or modified.

The candidate parent package remains the owner of the analytic claim:
[`EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_RANK_DEGENERACY_COMPONENT_LEDGER_WORKING_NOTE.md`](../../claims/arbitrary-order/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_RANK_DEGENERACY_COMPONENT_LEDGER_WORKING_NOTE.md).
This report adds no theorem-ledger or frontier entry because it is an
evidence-only audit and leaves the live mathematical frontier unchanged.

## Open boundaries

The following remain outside this audit:

- characteristic-zero equivalence of every finite-field rank in the q<=22
  screen;
- rank-degenerate component codimensions and the `Delta + sum(r_ij) + c_rank`
  envelope beyond the displayed fixtures;
- arbitrary `B_all`, all target residuals, and the 70-pencil compatibility
  problem;
- realization of every option by a common-shore physical graph;
- the analytic S2J/S2L/S2E/S1 bridge and the exact six-vertex exclusion; and
- all q>=23 strata and the global Krenn--Gu conjecture.

Accordingly, the package records matched finite evidence and corrected
counts, but no counterexample, theorem closure, or global resolution.
