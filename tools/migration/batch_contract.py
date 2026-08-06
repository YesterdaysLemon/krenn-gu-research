"""Frozen batch approval contract (Phase 2, item 1A).

A batch approval artifact must freeze the EXACT migration it approves:
not just member source paths, but the full old_path -> new_path
mappings, the member count, and a canonical mapping hash.  A later
manifest edit cannot drift under an approved batch without tripping
validation.

Batch file schema (catalog/batches/<batch_id>.json)::

    {
      "batch_id": "...",
      "approved_by": "...",
      "approved_at": "YYYY-MM-DD",
      "base_sha": "<full or abbreviated git SHA>",
      "manifest_sha256": "<sha256 of catalog/moved-paths.json at
                           approval time>",
      "mapping_sha256": "<canonical_mapping_hash of `moves`>",
      "member_count": N,
      "moves": [ {"old_path": "...", "new_path": "..."}, ... ],
      "rationale": "...",            (optional, recommended)
      "notes": "..."                 (optional)
    }

``canonical_mapping_hash`` is deterministic: the SHA-256 of the JSON
serialization of the sorted move mappings with sorted keys and no
whitespace.  It depends only on the mappings, never on manifest churn
(status flips, counts), so it is the durable integrity check and is
MANDATORY: ``validate_batch`` refuses a batch without a
``mapping_sha256`` that matches its own ``moves``.

``manifest_sha256`` is INFORMATIONAL approval-time provenance, not an
execution gate.  It records the exact manifest state the approver saw,
but the full manifest naturally changes as execution statuses flip
(entries move proposed -> moved), so it cannot be validated at
execution time without spurious refusals.  The canonical mapping hash
is the durable old->new approval binding; the mapping-vs-manifest
equality check covers destination drift.
"""

from __future__ import annotations

import hashlib
import json
import pathlib


def canonical_mapping_hash(moves) -> str:
    """SHA-256 over the canonical serialization of the mappings.

    Accepts either a list of ``{"old_path", "new_path"}`` dicts or a
    manifest ``moves`` list (extra keys are ignored).  Ordering is
    canonical: sorted by (old_path, new_path), then serialized with
    sorted keys and no whitespace, so the hash is deterministic and
    independent of insertion order.
    """
    canonical = sorted(
        ({"old_path": m["old_path"], "new_path": m["new_path"]}
         for m in moves),
        key=lambda d: (d["old_path"], d["new_path"]))
    blob = json.dumps(canonical, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def manifest_sha256(root: pathlib.Path) -> str:
    return hashlib.sha256(
        (root / "catalog" / "moved-paths.json").read_bytes()
    ).hexdigest()


def make_batch(batch_id, approved_by, approved_at, base_sha, members,
               root: pathlib.Path, rationale=None, notes=None) -> dict:
    """Build a frozen batch artifact from a manifest.

    ``members`` is a list of old_paths that must exist in the manifest
    as not-yet-moved entries.  The exact old/new pairs are frozen from
    the manifest at approval time.
    """
    manifest = json.loads(
        (root / "catalog" / "moved-paths.json").read_text(
            encoding="utf-8"))
    by_src = {m["old_path"]: m for m in manifest["moves"]}
    moves = []
    for src in members:
        m = by_src.get(src)
        if m is None:
            raise ValueError(f"{src} is not in the manifest")
        if m["status"] == "moved":
            raise ValueError(f"{src} is already moved")
        moves.append({"old_path": m["old_path"],
                      "new_path": m["new_path"]})
    batch = {
        "batch_id": batch_id,
        "approved_by": approved_by,
        "approved_at": approved_at,
        "base_sha": base_sha,
        "manifest_sha256": manifest_sha256(root),
        "mapping_sha256": canonical_mapping_hash(moves),
        "member_count": len(moves),
        "moves": sorted(moves, key=lambda m: m["old_path"]),
    }
    if rationale:
        batch["rationale"] = rationale
    if notes:
        batch["notes"] = notes
    return batch


def validate_batch(batch: dict, root: pathlib.Path,
                   manifest_moves) -> list:
    """Validate a frozen batch against the current repo state.

    Returns a list of problems; empty means the batch is safe to
    execute.  Refusal must happen before the first git mv.
    """
    problems = []
    for field in ("batch_id", "approved_by", "approved_at", "base_sha",
                  "member_count", "moves", "mapping_sha256"):
        if not batch.get(field) and batch.get(field) != 0:
            problems.append(f"batch missing required field: {field}")
    if problems:
        return problems
    if not isinstance(batch["moves"], list):
        return ["batch moves must be a list"]
    if not batch.get("approved_at"):
        problems.append("batch missing approved_at")

    # base_sha must resolve in this repository.
    import subprocess
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", str(batch["base_sha"]) + "^{commit}"],
        cwd=root, capture_output=True, text=True)
    if proc.returncode != 0:
        problems.append(
            f"batch base_sha does not resolve: {batch['base_sha']}")

    # member_count must equal the mapping list.
    if batch["member_count"] != len(batch["moves"]):
        problems.append(
            f"member_count {batch['member_count']} != "
            f"len(moves) {len(batch['moves'])}")

    # No duplicate sources or destinations within the batch.
    srcs = [m["old_path"] for m in batch["moves"]]
    dsts = [m["new_path"] for m in batch["moves"]]
    if len(srcs) != len(set(srcs)):
        problems.append("batch has duplicate sources")
    if len(dsts) != len(set(dsts)):
        problems.append("batch has duplicate destinations")

    # mapping_sha256 is mandatory (checked above) and must match the
    # frozen mapping (catches any drift in the batch file itself after
    # approval).
    actual = canonical_mapping_hash(batch["moves"])
    if actual != batch["mapping_sha256"]:
        problems.append(
            "batch mapping_sha256 does not match its own moves "
            "(batch altered after approval)")

    # Every batch mapping must equal the CURRENT manifest mapping
    # (catches destination drift in the manifest after approval).
    by_src = {m["old_path"]: m for m in manifest_moves}
    for bm in batch["moves"]:
        mm = by_src.get(bm["old_path"])
        if mm is None:
            problems.append(
                f"batch source missing from manifest: {bm['old_path']}")
        elif mm["new_path"] != bm["new_path"]:
            problems.append(
                f"manifest drift for {bm['old_path']}: batch says "
                f"{bm['new_path']}, manifest says {mm['new_path']}")
    return problems



def validate_executed_provenance(manifest_moves, root: pathlib.Path):
    """Provenance invariant (item 1C): every moved entry names a batch
    that exists and freezes its exact mapping.  Returns problems."""
    problems = []
    batches = {}
    moved = [m for m in manifest_moves if m.get("status") == "moved"]
    for m in moved:
        bid = m.get("executed_batch")
        if not bid:
            problems.append(
                f"moved entry lacks executed_batch: {m['old_path']}")
            continue
        if bid not in batches:
            bpath = root / "catalog" / "batches" / f"{bid}.json"
            if not bpath.exists():
                problems.append(
                    f"executed_batch file missing for {m['old_path']}: "
                    f"{bpath}")
                batches[bid] = None
                continue
            batches[bid] = json.loads(
                bpath.read_text(encoding="utf-8"))
        b = batches[bid]
        if b is None:
            continue
        bmap = {mv["old_path"]: mv["new_path"]
                for mv in b.get("moves", [])}
        if m["old_path"] not in bmap:
            problems.append(
                f"batch {bid} does not contain {m['old_path']}")
        elif bmap[m["old_path"]] != m["new_path"]:
            problems.append(
                f"batch {bid} mapping differs for {m['old_path']}: "
                f"batch {bmap[m['old_path']]} vs manifest "
                f"{m['new_path']}")
    return problems