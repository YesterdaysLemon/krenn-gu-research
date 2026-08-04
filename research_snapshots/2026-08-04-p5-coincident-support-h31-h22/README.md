# findings.md — tenth (coincident-support) component: generic H31 and weighted H22

Agent7 deliverable summary.  All files in this directory; nothing committed.
Repo state referenced: branch `claude/codebase-symbolic-proof-7rxbdw` at
`4f5f6f1` (includes the eleventh component's standalone package).

## Headline results

1. **Generic marked `H31` fibre of the tenth component is EMPTY — at binary
   level.**  Two of the four distinguished-coordinate frames (`q=0,1`) die by
   a polynomial *identity* (the `0000` diagonal row vanishes identically over
   `Z[b,e,k,m,c,t]`), valid at **every** chart point, not just generically.
   The other two (`q=2,3`) have `t`-free diagonal rows, a universal
   reconstruction kernel, and exact **unit** marking projections over
   `C(b,e,m,c)` (k=1 torus gauge).  No marking sheet survives anywhere — no
   ternary Fitting stage is needed, unlike components 6-8.
   Doc: `P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`;
   verifier green; independent modular audit green.

2. **Generic weighted `H22` incidence is EMPTY — also at binary level.**
   The `D_01` pencil's `0000` word vanishes *identically in the slope as
   well* (`Z[b,e,k,m,c,r,t,z]`): the `a != 0` support case of `H22` dies with
   no divisor exclusions at all.  The `D_23` pencil has the universal kernel
   `z* = r*col3 + k^2*col2` (`A z*=0`, `B z* = -2kP(r-k)^2`, from the
   doubled-column identity `D3 + k^2 D2 = 4k^2 P e_1111`), and unit
   projections over `C(b,e,m,c,r)` **and** at the special slopes
   `r=1, r=-1, r=0`; `r=infinity` is the `H31` `q=3` frame.  This is a
   cleaner slope scoreboard than any previously closed component (no
   equal-weight exception, no coupled-slope survivor).
   Doc: `P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`;
   verifier green; independent modular audit green.

3. **Both interior codimension-one survivor divisors are closed at ternary
   level.**  A char-0 per-point census (instant Groebner point checks over
   `Q`, 6400-point integer box, 19 s) shows the binary-survivor locus in
   parameter space is exactly `{c=0} + {b+e=0}` in codimension one.
   Relative projections over each divisor's function field leave tiny sheets
   (`b+e=0`: two rational markings `t=(1,0,0,-1/(2b^2))`, `(0,1,0,-1/(2b^2))`;
   `c=0`: `t_2=t_3=0` with one linear + one quadratic equation in
   `(t_0,t_1)` — a conjugate pair), **identical for `q=2`, `q=3` and the
   `D_23` pencil, and slope-free for the pencil.**  On every sheet the ideal
   (mixed rows, mode-2 one-marked minors `(0,1,2,7)`, `(0,1,3,7)`, `A=1`,
   `w*B-1`) is **unit**: every genuine survivor has a rank-four one-marked
   contraction, so no ternary `H31`/`H22` lift.  Nine unit certificates
   (six H31 + three H22), each < 0.2 s after the `A=1` normalization fix
   (the product-Rabinowitsch `w*A*B-1` form stalled past 550 s; normalizing
   `A=1` and inverting only `B` is instantaneous).  Audit corroboration:
   at `p=13` the divisor samples show exactly the two predicted survivor
   markings each — `(1,0,0,2)`/`(0,1,0,2)` on `b+e=0` at `(4,-4,3,7)`
   (H31 `q=2,3` and `D_23` slope 3 alike) and `(1,0,0,0)`/`(4,4,0,0)` on
   `c=0` at `(2,5,3,0)` — every genuine direction with mode-2 one-marked
   rank four.  The `c=0` sheet quadratic's discriminant is an irreducible
   non-square sextic, so its two markings are genuinely conjugate over the
   divisor function field (the mod-13 splitting is a reduction artifact).

## Structural mechanisms found (new to the program)

* **Identity-dead frames.**  `alpha_0 = alpha_1 = ybar` (the shared kernel
  line of the coincident-support family) plus the *apolar tails*
  `perm2((1,k),(-Q,Qk)) = 0` of the concentrated mode-2/3 kernel rows kill
  the whole `0000` diagonal row of the `q=0,1` frames and of the entire
  `D_01` pencil.  The apolarity is equivalent to the support concentration
  `T_1110=0`.  This is a stronger exclusion type than any in the atlas
  (binary-dead for every marking at every chart point) and should transport
  to any component whose two modes share a kernel line.
* **Single-`1`-word/diagonal coincidence.**  The `y_i` coefficient of the
  single-`1` word equals the `x_i` entry of the `0000` row (both are the
  `3x3` permanent of the other three alpha rows).  Hence the `t`-free
  y-elimination denominators are exactly the diagonal entries
  `A* = 2bce-(b+e)(m-1)` and `Q = be(m+1)`.
* **Pencil reconstruction kernel from doubled columns.**  The doubled-column
  permanent tensors of the concentrated basis satisfy
  `D3_w = -k^2 D2_w` off the all-beta word; this produces the universal
  `D_23` kernel `z*(r)` interpolating the `q=2` (`r=0`) and `q=3`
  (`r=infinity`) reconstruction directions, with `B(z*)` vanishing exactly
  at the equal-weight slope `r=k`.

## Runtimes (Singular 4.3.2, exact char 0)

| computation | time |
|---|---|
| H31 marking projection `q=2` / `q=3` over `C(b,e,m,c)` | 2.1 s / 1.7 s |
| H22 `D_23` projection over `C(b,e,m,c,r)` | 3.5 s |
| H22 `D_23` at slopes `r=1` / `r=-1` / `r=0` | 0.1 / 0.04 / 1.8 s |
| relative sheet projections (each, both divisors, H31+H22) | 0.1-0.2 s |
| per-sheet Fitting units (9 total, `A=1` normalized) | < 0.2 s each |
| 6400-point char-0 grid scan (batched point checks) | 19 s total |
| full verifier H31 / H22 end-to-end (sympy identities + Singular, incl. divisor closures) | 59 s / 6 m 13 s |
| modular audits end-to-end (28561+83521 markings per frame + divisor censuses) | 33 s (H31) / 20 s (H22); earlier multi-minute figures were contention with parallel Singular jobs |
| cross-validation on the seventh component (`crossvalidate_machinery.py`) | reproduces the repo's `EXPECTED_PROJECTIONS` exactly; hard `q=1` unit took 462 s |

## Timeout-nulls and superseded attempts (fail-closed record)

* Over-Z survivor-locus elimination (params as ring variables), direct
  16-equation form, `q=2,3`: **550 s timeout-nulls**.
* Reduced 11-equation form (t-free y-elimination), `q=2,3`: **550 s
  timeout-nulls**; modular `F_101` direct form: **540 s null**; a modular
  reduced run was aborted by an outer timeout before completing.
* Global unit certificate (`(M z, A z-1, w B z-1) = (1)` over
  `Q[b,e,m,c,t,z,w]`): `q=2` slimgb **550 s null**; remaining attempts died
  in a container restart and were **not rerun because the question is now
  settled negatively** — the ideal is provably *not* unit: the divisor
  points on `{c=0}` and `{b+e=0}` are explicit solutions.  The correct
  global statement is the divisor stratification of headline result 3.
* These nulls were replaced by the (exact) per-point census + relative
  divisor eliminations, which is how the true divisor landscape was found.

## Excluded-divisor lists (atlas-ready)

`H31` frame (component-10 row for the atlas Part I table):

* chart/normalization: `k=0` (pure coefficient `-2kP`, torus gauge),
  `P=bec+b+e=0` (concentration validity; raw support degenerates to the
  single word `1100` there);
* `q=0,1` and marked-basis normalization: **no divisors** (identities);
* `q=2,3`: implicit unit-elimination denominators; y-elimination
  denominators `A*`, `Q`; rank-7 witness `4bc^2e^3(m+1)^2P`; det7 drop-locus
  factors `4ecP(Qt_3-1)G`;
* survivor divisors: `{c=0}`, `{b+e=0}` **closed** (ternary, mode-2 minors);
  codim-2 strata `{ec+1=0,m=0}`, `{bc+1=0,m=0}` confirmed real and OPEN;
  deeper integer-box fine structure (families through `m=2`/`c=2` slices,
  see `grid_scan.log` + `explore_divisor_hypotheses.py`) unfitted and OPEN;
  divisor intersections OPEN.

Weighted `H22` frame: same parameter divisors; slopes `r in {0,1,-1,inf}`
**closed**; parameter-coupled slope divisors not extracted (as for
components 1-6); `D_23` divisor sheets slope-free and closed; `D_01`
divisor-free.

## Discrepancies / cautions

* **Characteristic-11 phantom.**  The `p=11` census showed one genuine
  survivor marking at `(b,e,m,c)=(2,3,7,5)`, `t=(1,0,0,2)`; the exact
  point check over `Q` at the same point is **unit**.  Single-prime modular
  censuses can exhibit phantom survivors — corroboration should use two
  primes (the repo's practice) or a char-0 point check.
* On `{b+e=0}` the **mode-3** one-marked map has rank three on the genuine
  direction — one-minor certificates must avoid mode 3 there (modes 0,1,2
  all work).  Analogue of the atlas II.5 mode-0 breakdown.
* The repo helper `p5_high_coordinate_tree_chart_cegar.py` is Windows/WSL-
  specific (`wsl.exe`) and needs `pysat`; all scripts here are
  self-contained and invoke native `Singular` directly.
* My docs rename the working note's family parameter `r` to `c` (slope
  clash); the raw certificate point `(b,e,k,m,c)=(2,3,5,7,11)` is unchanged.
* One audit-side bug was caught on the final rerun (a rank routine
  hardcoded to eight columns fed the `8x4` one-marked map, and a sign slip
  in the `c=0` sheet predicate); both fixed, audits green.  The verifier
  and doc were never affected — they use the raw Singular sheet strings.

## File inventory (this directory)

Deliverables:
* `P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md` — H31 theorem
  (frames, identities, projections, divisor closures, atlas record).
* `verify_p5_h31_coincident_support_component_generic_obstruction.py` —
  primary verifier (all identities k-symbolic; 2 unit projections; 4 sheet
  projections; 6 Fitting units; fail-closed 550 s budgets; JSON ledger to
  `tmp/`).
* `audit_p5_h31_coincident_support_component_generic_obstruction.py` —
  independent audit (DP permanent, `F_13`/`F_17` full marking censuses at
  generic samples + two divisor samples with sheet/rank-4 replay).
* `P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`,
  `verify_p5_h22_coincident_support_component_generic_obstruction.py`,
  `audit_p5_h22_coincident_support_component_generic_obstruction.py` — the
  weighted `H22` package (identity-dead `D_01`; `D_23` projections generic +
  three slopes; divisor closures; audits incl. slopes `3,1,-1,0,5` and a
  divisor census).
* `findings.md` — this file.

Exploration/replay scripts (kept for provenance): `explore_tenth_h31.py`,
`explore_tenth_h31_modular.py`, `explore_tenth_h22.py`,
`explore_kernel_structure.py`, `explore_rank7_witness.py`,
`explore_det7*.py`, `explore_h22_details.py`, `run_h31_projections.py`,
`run_h31_divisor_hunt.py`, `explore_y_elim*.py`, `explore_point_checks.py`,
`explore_grid_scan.py`, `explore_global_unit.py`,
`explore_divisor_hypotheses.py`, `explore_divisor_closures.py`,
`explore_divisor_fitting*.py`, `crossvalidate_machinery.py` (reproduces the
seventh component's published projections exactly — machinery validation),
plus logs (`grid_scan.log`, `divisor_hypotheses.log`,
`branch_ambient_replay.log` — the repo's own family certificate replays
green on this machine — and the final green runs
`h31_verify_final.log`, `h22_verify_final.log`, `h31_audit_final.log`,
`h22_audit_final.log`; ledgers in `tmp/*.json`).

## Next moves

1. **Ninth and eleventh components**: no generic `H31`/`H22` theorems yet
   (atlas Part III item 4).  The eleventh (equal-support sixfold,
   `P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md`, now merged) should be
   checked for the same support-concentration + identity-dead-frame
   playbook; its `U_3 = Pi` coordinate-plane invariant suggests strong
   universal kernels too.  The ninth has the exploratory modular census as a
   starting point.
2. **Codim-2 survivor strata** of the tenth: `{ec+1=0, m=0}`,
   `{bc+1=0, m=0}` (confirmed; sheets visible in the point checks), the
   `m=2`/`c=2` families from the grid, and divisor intersections
   (`c=0` with `b+e=0` etc.).  Each is a small relative elimination away.
3. **`P=0` divisor**: raw support is already one word (`T_1100=-2kQ`), so a
   different (simpler) concentration applies — likely another identity-dead
   configuration; quick win.
4. **`k=0` and the projective boundary**; the singular walls (branches A/B
   of the working note) sit inside the component closure — their marked
   fibres are untouched.
5. **Atlas integration**: add component-10 rows to Part I (both frames
   now have *fuller* divisor records than components 3-8: two interior
   divisors closed, four slopes closed, two frames identity-dead).
6. **Transport the identity mechanism**: scan the other certified
   components for coincident kernel rows/apolar tails; wherever present,
   the same one-line binary exclusions should replace heavy eliminations.
