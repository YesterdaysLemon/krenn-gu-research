# P4 rank-two-triangle classification packages

Migrated P4 rank-two-triangle classification packages — the fourth P4
classification spine, moved as Stage 8 batch
`p4-rank-two-triangle-stage8` (mapping_sha256 `e628b1263778…`).  This
spine is the **live** resonant / nonresonant rank-two-relation
triangle chain: reductions and classifications only.  The companion
obstruction / boundary theorems of the same chain live under
[`../../boundaries/rank-two-triangle/`](../../boundaries/rank-two-triangle/),
and the distinction is preserved by directory, not filename.

The chain proceeds: the nonresonant cut reduction reduces all
nonresonant rank-two-relation triangles to cyclic cuts; the three
boundary obstructions then prove the complete nonresonant triangle is
empty; the affine-holonomy reduction treats the sole remaining
(resonant) stratum; its flat binary-cubic frontier is handled by the
two classifications below together with their boundary companions.

Filenames are preserved; no file was renamed to a generic name.

| package | claim document | verifier | audit | status/provenance source | batch |
|---|---|---|---|---|---|
| `nonresonant/cut-reduction/` | `P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md` | `verify_p4_nonresonant_rank_two_triangle_cut_reduction.py` | **none** — the document states the verifier is a tiny exact replay of the displayed symbolic proof; intentional documented state | classifier review_required; Stage 8 review | stage8 |
| `resonant/affine-holonomy-reduction/` | `P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md` | `verify_p4_resonant_rank_two_triangle_affine_holonomy.py` | `audit_p4_resonant_rank_two_triangle_affine_holonomy.py` | classifier review_required; Stage 8 review | stage8 |
| `resonant/flat-full-kernel-collision/` | `P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md` | `verify_p4_resonant_flat_full_kernel_collision.py` | `audit_p4_resonant_flat_full_kernel_collision.py` | classifier review_required; Stage 8 review | stage8 |
| `resonant/flat-projective-partner/` | `P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md` | `verify_p4_resonant_flat_projective_partner.py` | `audit_p4_resonant_flat_projective_partner.py` | classifier review_required; Stage 8 review | stage8 |

**Preserve the status words exactly.**  A reduction is not a
classification; the affine-holonomy result is a reduction to two
intrinsic shapes, not an exhaustion.  The flat classifications cover
the collision ratios and the projective partner sheets respectively —
neither is an affine classification of the whole flat branch, and
neither resolves the boundary obstructions' divisors.

## Theorem chain (live)

```text
nonresonant/cut-reduction (reduction)
    |
    +-- boundary: one-three, two-two, degenerate-cut
    |   (claims/p4/boundaries/rank-two-triangle/nonresonant/)
    |       [complete nonresonant triangle empty]
    v
resonant/affine-holonomy-reduction (reduction)
    |
    +-- boundary: nonzero-additive-holonomy
    |       [frontier confined to Omega=0, delta=0]
    v
    flat branch:  flat-full-kernel-collision (classification)
                  flat-projective-partner (classification)
                  + boundary companions flat-generic-binary-cubic
                    and flat-kernel-zero-binary-cubic
```

## Live versus withdrawn lineage

A user browsing this tree can distinguish the live results from their
historical failed variants without Git archaeology:

| live claim | lineage | historical package (withdrawn; Stage 33) |
|---|---|---|
| mixed/two-rank-two (boundary spine) | **supersedes** | [`../../history/mixed-two-rank-two-triangle/`](../../history/mixed-two-rank-two-triangle/) — withdrew the unmarked `GL_2` row change; the live theorem keeps kernel rows Borel-marked |
| resonant/flat-generic-binary-cubic (boundary spine) | **corrected successor** of an overstrong scope | [`../../history/resonant-flat-triangle/`](../../history/resonant-flat-triangle/) — names this live theorem as the true full-support Borel chart |
| resonant/flat-kernel-zero-binary-cubic (boundary spine) | **valid scope preserved** | same withdrawn package names this live theorem as the valid one-kernel-zero theorem |
| all other Stage 8 packages | no predecessor | — |

The corrected live claims do **not** inherit the scope of their
withdrawn predecessors; the withdrawn documents remain explicitly
withdrawn and are not rehabilitated by this migration.

## Cross-spine dependencies (stable, not Stage 8 members)

- [`../triangle-211/rank-two-relation-triangle-corrected/`](../triangle-211/rank-two-relation-triangle-corrected/)
  — the Stage 5 recovered complete Borel classification; the
  withdrawn-overstrong doc names it as the recovery
- [`../star/`](../star/) and [`../pair-geometry/`](../pair-geometry/)
  — sibling spines
- The shared all-pair verifier now lives at
  [`../verify_p4_all_pair_rank_exceptional_graph_reduction.py`](../verify_p4_all_pair_rank_exceptional_graph_reduction.py);
  that path repair changes no evidence role.

Migration provenance: `catalog/batches/p4-rank-two-triangle-stage8.json`,
`docs/architecture/p4-rank-two-triangle-stage8-dry-run.md`, and
`docs/architecture/layout-migration-stage8-report.md`.  No theorem
claim changed; the global conjecture remains **UNRESOLVED**.
