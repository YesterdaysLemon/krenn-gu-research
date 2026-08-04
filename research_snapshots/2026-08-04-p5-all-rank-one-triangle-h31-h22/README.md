# Agent 6 findings: ninth-component (all-rank-one triangle) generic H31 and weighted H22

## Bottom line

Both generic local frames of the ninth pure-`P_4` component (the
all-rank-one relation triangle, free field `C(p,q)`, single word
`T_1111=-2`) are **closed, exact, characteristic zero, green
end-to-end**:

1. **H31**: `P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`
   + `verify_...py` + `audit_...py`.
2. **Weighted H22**: `P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`
   + `verify_...py` + `audit_...py`.

With these, the first **nine** certified component orbits are
generically closed for both `H31` and weighted `H22`.  (During this
work the repo census grew to **thirteen** orbits — PR #21 and the
exhaustiveness-sweep snapshot; the tenth through thirteenth have no
`H31`/`H22` theorems yet, and both docs/ledgers state this
explicitly.)

No genuine marked survivor family exists over the function field in
either frame, so there is no "major finding" branch: the component
behaves like the other eight, but through a structurally new
mechanism (below).

## What made this component easy (the predicted single-word leverage)

The tensor support is the single word `1111`.  Multilinearity then
makes the **entire marked tensor marking-invariant** (still the
single word `-2` for every `t`), so for **every** distinguished
coordinate `q` and every marking, restoring the deleted coordinate is
a mixed-kernel direction `z_rec` with `A=0, B=-2`.  This is the
reconstruction-kernel mechanism of the atlas' "why r=+-1 collapse"
note, but *ubiquitous in all four H31 frames at once* — every mixed
matrix has rank at most 7 identically in `t`.  Consequences:

- the exact marking projections are tiny (every Singular elimination
  in both theorems runs in **under 5 seconds**; no timeouts, nothing
  recorded as null);
- the `H31` survivor loci are **whole coordinate lines** in marking
  space (a new phenomenon; earlier components had isolated rational
  markings), which forced one methodological novelty: the Fitting
  certificates keep the line parameter `s` as a **polynomial ring
  variable**, so each unit ideal closes the entire line — all special
  `s` values included — over the generic `(p,q)`.

## H31 result (exact statements proved)

Marking loci over `C(p,q)` (bidirectional ideal equalities):

| frame | locus |
|---|---|
| `q=0` | `(t1,t2,t3)` — whole `t0`-line |
| `q=1` | `(1)` — empty |
| `q=2` | `(t1,t3,t0*t2)` — `t0`-line ∪ `t2`-line |
| `q=3` | point `t0=-(q+1)/(pq+p+1)`, `t3=-(pq+p+1)/(pq+1)`, `t1=t2=0` |

Sheet kernels are exactly `span(z_rec, z_gen)` (rank-6 pivots
line-parameter-free, e.g. `2(pq+1)^2(pq+p+1)` for `q=0`).  Killing
modes: mode 1 for `q=0` and `q=3`, mode 3 for both `q=2` branches
(matches the modular census).  All certificate minors reduce to exact
`A B`-multiples on `z = k z_gen + l z_rec`; the `q=3` point carries a
uniform one-minor identity in the mixed-star style:

```text
det P_1[0,1,4,7] = -(q+1)/((pq+1)(pq+p+1)) * A^2 B.
```

Four unit-ideal Fitting certificates (rows: `q=0`: (0,2,3,7),(0,3,6,7)
mode 1; `q=2` t0: (0,2,3,7),(0,2,6,7) mode 3; `q=2` t2:
(0,2,4,7),(0,2,6,7) mode 3; `q=3`: single (0,1,4,7) mode 1).

## Weighted H22 result

Both pencils `D_01^r`, `D_23^r` over `C(p,q,r)`:

- Marking loci are **slope-independent**: `D_01`: the `t0`-line;
  `D_23`: `t0`-line ∪ the line `t0=-(q+1)/(pq+p+1), t3` free (the
  `H31` `q=3` marking's `t0`).  Loci interpolate the four `H31`
  frames at `r ∈ {0,∞}` exactly as the atlas frame identifications
  predict.
- Unlike `H31` there is **no reconstruction direction**: each sheet
  has a unique kernel line with both diagonals generically nonzero —
  honest binary `Delta_2` survivor families, killed only at ternary
  level.
- Single mode-1 minors kill both `t0`-sheets, with explicit
  identities on the displayed kernel representatives:
  `det P_1[0,2,3,7] = -4pr(pq+1)(pr-1)^2 B` (`D_01`) and
  `(r-1) det P_1[0,2,3,7] = 4(r+1)^3(pq+1)^2(pq+pr+1) B` (`D_23`).
  The `t3`-sheet needs mode 3 and the pair (0,2,3,7),(0,2,6,7)
  (mode-1 and mode-3 full Fitting ideals are unit there; modes 0/2
  are not — the killing mode is genuinely sheet-dependent).
- Three unit-ideal certificates, `s` polynomial throughout.

## Runtimes (this container; Singular 4.3.2, sympy)

| script | wall time | Singular budget used |
|---|---|---|
| verify H31 | 1m35s–4m20s (machine-dependent; 8 Singular runs) | every run < 5 s of the 550 s cap |
| verify H22 | ~27 s (5 Singular runs) | every run < 5 s |
| audit H31 (F_11, F_13 exhaustive, 798 directions) | ~26 s | — |
| audit H22 (F_11 r=3, F_13 r=4, both pencils) | ~12 s | — |

Fail-closed plumbing: every Singular call is wrapped in a hard
timeout; a timed-out/failed run is recorded as `null` in the ledger
and the verifier raises.  Nothing was ever null in the final runs.

## Excluded divisor lists (honest frontier)

- **H31**: `p, q, q+1, p-1, pq+1, pq-p+1, pq+p+1` (explicit in the
  pivots/identities), plus implicit Groebner denominators; the `q=3`
  sheet exists only where `(pq+1)(pq+p+1) != 0`, and its genuine
  direction degenerates on `p=1`.
- **H22**: slopes `r=0, 1, -1`; coupled `pr±1, pq+pr+1, pqr+r+1`;
  parameters `p, q, q+1, pq+1, pq-p+1, pq+p+1`; marking-coupled
  `r+s`, `s(pq+1)+q+r`, `G=r^2(pq(s+1)+p+s+1)-pqs-r-s`,
  `W=pqrs+pqr+pqs+pr+rs+r+s` (no `s`-free rank pivot exists on the
  `t3`-sheet — the `(r,s)`-coupling there is necessary).  At `r=1`
  the `D_23` `B`-diagonal dies on both sheets (equal-weight
  collapse); at `r=-1` its `A`-diagonal dies.

## A concrete modular specialization jump (documented, not a bug)

At the single sample `F_11, (p,q,r)=(2,3,4)`, the `D_01` census has 9
extra genuine survivor markings on the line `t0=-2, t3` free — absent
at `F_13` with the same `(p,q,r)` and at every other tested `F_11`
slope (r=3,7,8,9), so an implicit elimination denominator has
**integer content divisible by 11** there (the natural char-0
divisor guess `r+pq^2` was tested and refuted at `F_13, r=8`).
Importantly, every direction on the jump line still has a rank-four
mode-1 marked map — even the artifact is obstruction-consistent.
Recorded in the H22 doc's honest frontier and in the audit's sample
choice comment.  This is a concrete instance of the atlas' "implicit
denominators are not vacuous" warning.

## Deliverables (all in agent6_out/; run from repo root; tmp/ ledgers)

- `P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`
- `verify_p5_h31_all_rank_one_triangle_component_generic_obstruction.py`
- `audit_p5_h31_all_rank_one_triangle_component_generic_obstruction.py`
- `P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`
- `verify_p5_h22_all_rank_one_triangle_component_generic_obstruction.py`
- `audit_p5_h22_all_rank_one_triangle_component_generic_obstruction.py`
- `findings.md` (this file)

Integration notes for the main session:

1. The verifiers define a **local** `singular_command(timeout)`
   (posix: `timeout --signal=KILL <t> Singular -q`; nt: the repo's
   wsl.exe wrapper).  The repo's shared helper
   `p5_high_coordinate_tree_chart_cegar.singular_command_with_timeout`
   returns the `wsl.exe` command on **every** OS, which cannot run on
   this Linux container; the local helper mirrors it on Windows and
   fixes Linux.  Consider upstreaming that fix.
2. The H31 verifier imports `family` from
   `verify_p4_all_rank_one_triangle_pure_component` (guarded by
   existence) and pins sha256 of the component doc+verifier, in the
   established dependency pattern; both verifiers hash their theorem
   docs.
3. Ledgers land in `tmp/` (gitignored), keys follow the
   nine-closed/thirteen-certified split.

## Next moves

1. Atlas rows for component 9: the explicit divisor lists above slot
   directly into `P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md` Part I
   (both frames), with the `F_11` jump as a Part-II-style case study
   candidate.
2. Slope boundaries `r=1, -1, 0` of both pencils via the Part-II
   equal/opposite-weight pattern; the ubiquitous reconstruction
   kernel should make the `r=±1` universal-kernel identities exact
   one-liners here too.
3. Parameter divisors `pq+1=0, pq+p+1=0, p=1, q=-1, p=0, q=0` and the
   projective boundary of the free chart.
4. Transport the same single-word leverage to the **tenth through
   thirteenth** components: the tenth/eleventh are also free
   families (identically pure), so the marked-tensor invariance
   argument and the ubiquitous reconstruction kernel apply verbatim
   whenever their support is a single word — check their normal
   forms first; if support is single-word, expect line-shaped loci
   and the same polynomial-line-parameter certificate pattern.
