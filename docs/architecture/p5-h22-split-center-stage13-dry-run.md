# Stage 13 dry-run — split-center weighted-H22 generic package

Status: **pre-migration repair and exact dry-run; no file move, frozen batch,
or migration approval**

Baseline: `main` at
`2b92c8f42e9d907ee8550d1c370387473437abe7` (the merge commit for PR #41).

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Decision

Exactly three root files form a coherent component-24 generic weighted-`H22`
claim package:

```text
P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py
audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
```

The classifier's common destination,
`claims/p5/h22/split-center-mixed-star/`, is ownership-correct.  The theorem,
primary verifier, and distinct no-import audit have the same mathematical
owner and no same-theorem boundary child is stranded by selecting this
triple.

Stage 12 established that the primary's use of `build_model` and `project`
is a neutral shared-implementation edge, not a mathematical premise from the
component-20 candidate theorem.  The other imported H31 utilities are also
implementation edges.  They do not transfer an H31 theorem conclusion into
this H22 proof.

This dry-run resolves two pre-migration defects:

1. it moves both root imports below the repository bootstrap, making the
   primary portable from its proposed nested destination and clearing the
   existing Ruff `E402` failure; and
2. it corrects a stale theorem-ledger scope summary that incorrectly excluded
   special weights even though the theorem covers the full projective weight
   line.

Neither repair changes the theorem, its proof, or its status.  The exact
three-path mapping still requires explicit human approval before a batch may
be frozen or executed.

## 2. Scientific and evidence boundary

The owning document proves an exact characteristic-zero theorem over
`K=C(k,s,t)`, the function field of the generic point of component 24.  It
covers both pair orbits and the full homogeneous weight line:

| pair orbit | finite `[lambda:1]` | infinity `[1:0]` |
|---|---:|---:|
| `D01` | one projected branch | one projected branch |
| `D23` | two projected branches | two projected branches |

The primary directly reconstructs four projections and proves that the fixed
minor `N0[0137]` makes each of the six branch ideals unit.  This is an exact
SymPy/Singular proof replay, not a detached certificate and not a finite-field
experiment.

The separate audit imports no repository implementation.  It independently
reconstructs the component rows, projections, contraction, one-marked map,
and subset-DP permanent algorithm.  It checks selected exact-rational branch
witnesses and both rational roots of one specialized quadratic branch.  It is
independent at that implementation/model-reconstruction layer, but it does
not replay or replace the generic function-field unit-ideal proof.

The following remain open and are not members of this package:

- special component-parameter divisor fibres;
- projective component-boundary fibres;
- exhaustion of all possible P4 components;
- the arbitrary-order local-to-global reduction; and
- the global conjecture.

Weight infinity and special finite values of `lambda` are not open boundaries
of this theorem.  No formal or Lean counterpart is mapped or present.  The
ledger's `dependencies: []` means relationships are not recorded, not that no
mathematical or executable dependencies exist.

The ledger token `independent_modular_audit` is retained unchanged.  Under
schema v3 it is explicitly a legacy broad carrier-mapping label, not a literal
claim that this audit uses modular arithmetic or is independent at every
layer.  The audit itself controls the method and scope description.

## 3. Pre-migration repairs

### 3.1 Portable primary imports

At the baseline, the primary imported two root modules before calling
`bootstrap`:

- `build_model` and `project` from
  `derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate`;
- `one_marked_map` from `verify_p5_h31_marked_basis_open_branch`.

That happened to work from repository root but would fail when the script's
directory became `sys.path[0]` under the proposed package.  The H31 sibling
import was already delayed but lacked a scoped Ruff exemption.

The preparatory repair now:

1. performs the standard marker scan and calls `bootstrap(__file__)` first;
2. exposes `claims/p5/h31/split-center-mixed-star`;
3. imports both root shared implementations and the moved H31 sibling only
   after bootstrap; and
4. scopes `# noqa: E402` to those intentional delayed imports.

The root helper files remain in place.  This stage neither extracts shared
infrastructure nor changes any of their other consumers.

### 3.2 Ledger scope correction

The ledger formerly said `slope r transcendental; special slopes excluded`.
No `r` occurs in this theorem or primary, and the exact replay covers the
entire finite chart plus weight infinity.  The entry now records:

```text
over the component function field C(k,s,t) (generic point)
all homogeneous weights covered in the finite [lambda:1] and infinite [1:0] charts
special component-parameter divisor fibres and projective component-boundary fibres excluded, not proved
```

The focused regression
`test_split_center_h22_scope_covers_full_weight_line` pins the corrected
scope and rejects the stale `slope r` / `special slopes excluded` wording.
The mathematical status remains `verified_generic`.

## 4. Typed dependency topology

The three relevant dependency classes are deliberately separate.

### Mathematical and ownership edges

- The already-migrated P4 split-center component theorem supplies the
  component/normal-form anchor.
- The H31 split-center theorem is a sibling result on the same P4 component,
  not an H22 proof premise.
- The theorem document, H22 primary, and H22 audit are owned by this exact H22
  generic package.

### Executable implementation edges

- `build_model` and `project`: root neutral four-source weighted-H22
  construction, as audited in Stage 12;
- `one_marked_map`: the 81-import-statement / 79-consumer root marked-basis
  helper;
- `rows` and `shifted`: the moved H31 split-center primary, exposed through
  the shared bootstrap helper; and
- WSL `/usr/bin/Singular`: exact elimination backend used by the primary.

The audit has no repository import edge.  No downstream Python script imports,
dynamically loads, or subprocesses the selected H22 primary or audit.

### Evidence and formalization edges

- The primary is the direct exact verifier carrier.
- The audit is exact-rational corroboration with a no-import model
  reconstruction; it is not the generic proof.
- There is no mapped formalization carrier.

## 5. Exact proposed mapping

| source | destination |
|---|---|
| `P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h22/split-center-mixed-star/P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py` | `claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py` |
| `verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py` | `claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py` |

The destination directory is absent.  The manifest contains exactly these
three `proposed_high_confidence` mappings, with no destination collision,
double move, or overlap cycle.

Canonical mapping SHA-256:

```text
fd1d3e4163068b2e0e16f6e6161a52f822a4d02acd74bdd5e80e5bc6ba341154
```

Dry-run manifest SHA-256:

```text
3d254459159bd136f4d2e9cc4c6d1fcbd75384c5548fa1059df4b1e7edbf40d3
```

These values identify the reviewed proposal; they are not approval.  A future
batch must use the exact approved commit as `base_sha`, record the
approval-time manifest hash, and recompute the same canonical mapping hash.

## 6. Staying references and repair surface

After a pure move, the mechanical repair must update:

- the four replay/lint/compile lines inside the theorem document to
  root-relative forward-slash destination paths;
- the live theorem link in root `README.md`;
- one theorem link and two replay commands in
  `docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md`;
- the theorem-ledger document, primary, and audit paths, normalized document
  hash, `claim_package`, `proof_variant`, `subpackage`, and legacy paths; and
- `claims/p5/h22/README.md`: add the package row, disclose both root shared
  dependencies, remove split-center from “Not migrated here,” and avoid the
  current blanket suggestion that every H22 package leaves weight slopes
  open.

The migration rewriter must run twice, and the second pass must be a fixed
point.  The theorem's current `.\`-style PowerShell paths and combined Ruff
command require explicit inspection rather than an assumption that automatic
rewriting catches all four lines.

Stage 10--12 architecture documents may retain old root names as historical
provenance.  The frozen classifier remains a historical source snapshot; it
is not regenerated to manufacture approval.

No source hash consumer, dynamic loader, subprocess call, certificate, or
tracked result file targets the selected primary or audit.  Semantic replays
must nevertheless leave the tracked tree clean.

## 7. Projected transitions

| measure | before | after exact three-file move |
|---|---:|---:|
| manifest `moved` | 350 | 353 |
| manifest `proposed_high_confidence` | 252 | 249 |
| manifest `review_required` | 1,413 | 1,413 |
| manifest moved-only root projection | 2,022 | 2,019 |
| measured root files | 2,014 | 2,011 |
| measured root directories | 9 | 9 |
| measured root entries | 2,023 | 2,020 |
| grandfathered root debt | 2,007 | 2,004 |
| enforceable retired old paths | 350 | 353 |

The classifier-era projections for all high-confidence mappings (`1,770`) and
all classified mappings (`357`) are unchanged because these files were
already members of those sets.  The one-entry difference between measured
root and the manifest moved-only projection remains the documented
post-inventory `AGENTS.md` addition.

## 8. Replay evidence

Environment:

```text
Windows Python 3.13.14
SymPy 1.14.0
uv 0.11.8
Ruff 0.15.21
native Windows Singular absent
WSL /usr/bin/Singular 4.3.2 available
```

Baseline and post-repair semantic replays both passed.  The final preparatory
replay recorded:

| role | command | result | elapsed reported by script |
|---|---|---|---:|
| primary | `uv run --with sympy python verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py` | pass; four projections, six branch unit ideals, generic H22 empty; special fibres/global false | 115.218 s |
| audit | `uv run --with sympy python audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py` | pass; seven exact-rational witnesses including both specialized quadratic roots; generic proof not replaced | 0.496 s |

The preparatory repair also passes:

```powershell
python -m ruff check claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
python -m py_compile claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
```

The baseline Ruff command had one pre-existing `E402` on the delayed H31
import; the scoped import repair removes it.  Replays created no tracked
output changes.

After an approved move and mechanical repair, the same four commands must be
rerun at the destination paths.  The primary replay is mandatory because the
script uses an external exact backend and the path/bootstrap surface changes.

## 9. Approval and execution plan

No batch artifact is created by this dry-run.  If the repository owner
approves exactly the mapping in section 5, the next stage will:

1. create and commit
   `catalog/batches/p5-h22-split-center-stage13.json` with the exact approval,
   approval date, base SHA, manifest hash, mapping hash, member count three,
   and the three mappings;
2. run the transaction-aware executor in a pure-move commit;
3. verify source absence, destination presence, byte-identical blobs, `R100`
   move identity, manifest provenance, and exact root arithmetic;
4. perform only the path/navigation/ledger repairs listed above;
5. run the semantic replays, Ruff, compilation, rewriter fixed point, and
   full candidate-tree validation floor;
6. obtain fresh independent review appropriate to the evidence and
   executable path changes; and
7. require exact-head PR CI, a fresh merge base, no unresolved review thread,
   and merged-main CI.

Approval of these three mappings would not approve moving or extracting the
candidate-housed H22 helper, the marked-basis helper, the H31 sibling, any
special/projective boundary, or any other root file.

## 10. Hard stop

Stage 13 stops before a batch file, `git mv`, manifest status transition,
theorem replay-path rewrite, navigation update, or root-debt reduction.

The broad root-exit goal is not exact human approval for this mapping.  Until
that approval is recorded, the repository remains at 2,007 grandfathered
root-debt files and this proposal is non-executable.
