# P4 rank-two-triangle boundary packages

Migrated P4 rank-two-triangle boundary packages — the genuine
obstruction / boundary theorems of the live resonant / nonresonant
rank-two-relation triangle chain, moved as Stage 8 batch
`p4-rank-two-triangle-stage8` (mapping_sha256 `e628b1263778…`).  The
companion reductions and classifications live under
[`../../classifications/rank-two-triangle/`](../../classifications/rank-two-triangle/).

An obstruction on one divisor is not exhaustion: each package below
closes its stated cut type, branch, or chart, and the combined
theorems confine (not resolve) the frontier step by step.

Filenames are preserved; no file was renamed to a generic name.

## Nonresonant branch

| package | claim document | verifier | audit | role | batch |
|---|---|---|---|---|---|
| `nonresonant/degenerate-cut/` | `P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md` | `verify_p4_nonresonant_degenerate_cut_triangle_obstruction.py` | `audit_p4_nonresonant_degenerate_cut_triangle_obstruction.py` | closes every proper bridge-support boundary | stage8 |
| `nonresonant/one-three/` | `P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md` | `verify_p4_nonresonant_one_three_triangle_obstruction.py` | `audit_p4_nonresonant_one_three_triangle_obstruction.py` | full-support `1+3` collapse | stage8 |
| `nonresonant/two-two/` | `P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md` | `verify_p4_nonresonant_two_two_triangle_obstruction.py` | `audit_p4_nonresonant_two_two_triangle_obstruction.py` | full-support `2+2` bridge exclusion | stage8 |

Together these three prove: the complete nonresonant
all-rank-two-relation triangle is empty.

## Resonant branch

| package | claim document | verifier | audit | role | batch |
|---|---|---|---|---|---|
| `resonant/nonzero-additive-holonomy/` | `P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md` | `verify_p4_resonant_nonzero_additive_holonomy_obstruction.py` | `audit_p4_resonant_nonzero_additive_holonomy_obstruction.py` | excludes the `delta != 0` branch; confines the frontier to `Omega=0, delta=0`; does **not** resolve zero holonomy | stage8 |
| `resonant/flat-generic-binary-cubic/` | `P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md` | `verify_p4_resonant_flat_generic_binary_cubic.py` | `audit_p4_resonant_flat_generic_binary_cubic.py` | the true Borel-generic chart obstruction; does **not** automatically include special kernel-zero cases | stage8 |
| `resonant/flat-kernel-zero-binary-cubic/` | `P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md` | `verify_p4_resonant_flat_kernel_zero_binary_cubic.py` | `audit_p4_resonant_flat_kernel_zero_binary_cubic.py` | the valid one-kernel-zero boundary theorem | stage8 |

## Mixed bridge

| package | claim document | verifier | audit | role | batch |
|---|---|---|---|---|---|
| `mixed/two-rank-two/` | `P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md` | `verify_p4_mixed_two_rank_two_triangle_obstruction.py` | `audit_p4_mixed_two_rank_two_triangle_obstruction.py` | corrected exact theorem for the `(2,2,1)` triangle stratum; keeps kernel rows Borel-marked | stage8 |

## Historical withdrawn predecessors

The following related artifacts remain historical/legacy and are **not**
members of the live Stage 8 spine; Stage 33 preserves them in dedicated
history packages without rehabilitation:

- [`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md`](../../history/resonant-flat-triangle/P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md)
  (+ verify/audit) — **WITHDRAWN**: full-row `GL_2` used where purity permits
  only Borel gauge. It names the live `flat-kernel-zero-binary-cubic` and
  `flat-generic-binary-cubic` packages as its valid descendants. It has not
  been rehabilitated.
- [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md`](../../history/mixed-two-rank-two-triangle/P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md)
  (+ verify/audit) — **WITHDRAWN pending Borel audit**; the live
  `mixed/two-rank-two` package supersedes it. It has not been rehabilitated.

Withdrawn evidence is never substituted for live verification: each
live package was replayed independently during Stage 8.

Migration provenance: `catalog/batches/p4-rank-two-triangle-stage8.json`
and `docs/architecture/layout-migration-stage8-report.md`.  No
theorem claim changed; the global conjecture remains **UNRESOLVED**.
