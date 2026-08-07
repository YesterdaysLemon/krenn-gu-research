#!/usr/bin/env python3
"""Migration-aware reference rewriting for moved claim packages.

Phase 4 machinery.  After execute_moves.py has performed pure git-mv
operations, every reference to a moved file must be re-anchored:

  1. Markdown links (inline ``[text](target)`` and reference-style
     ``[text]: target`` definitions, including image links): resolved
     against the SOURCE file's location at the time the link was
     written (its old location if the source was also moved), the
     resolved path is NORMALIZED before the manifest lookup, mapped
     through catalog/moved-paths.json, and re-expressed relative to
     the source's NEW location.  URL fragments are preserved; external
     URLs are untouched; ambiguous or nonexistent targets are reported,
     never guessed.
  2. Fenced replay commands: ``python <script>.py [args]``,
     ``uv run ... python <script>.py``, and continuation-line
     ``python \\`` + ``<script>.py`` commands inside ```text/```bash
     blocks are rewritten to the script's new root-relative path when
     the script was moved and its basename is unambiguous.  The
     grammar lives in ``replay_command.py`` and is shared with the
     stale-reference scanner, so the two machines cannot drift.  Other
     code-block content is untouched.
  3. Theorem ledger: entries whose document, primary_verifier, or
     independent_audit was moved get updated paths, a claim_package
     field, a legacy_paths list, and recomputed committed-blob hashes.

Nothing here changes theorem wording; only path expressions move.

Functions take an explicit *root* so the test suite can exercise them
against a synthetic fixture tree without touching the real repository.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

from package_metadata import resolve_claim_package_metadata
from replay_command import match_replay

MD_LINK = re.compile(r"(\]\()([^)\s]+)(\))")
REF_LINK = re.compile(r"^(\s*\[[^\]]+\]:\s*)(\S+)(\s*)$", re.M)
FENCE = re.compile(r"^```")


def normalize_rel(base_dir: str, target: str) -> str | None:
    """Resolve *target* against *base_dir* and normalize textually.

    Returns the normalized repo-relative path, or None when the target
    escapes the repository root (too many '..') or normalizes to
    nothing.  This is the ONLY path used for manifest lookups and for
    re-expression — never the raw join.
    """
    parts = [] if base_dir in ("", ".") else base_dir.split("/")
    for part in target.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(part)
    return "/".join(parts) if parts else None


def relative_to(src_dir: str, dst_path: str) -> str:
    """Express *dst_path* (repo-relative) from *src_dir*."""
    src_parts = [] if src_dir in ("", ".") else src_dir.split("/")
    dst_parts = dst_path.split("/")
    common = 0
    for a, b in zip(src_parts, dst_parts):
        if a == b:
            common += 1
        else:
            break
    ups = [".."] * (len(src_parts) - common)
    rest = dst_parts[common:]
    if not ups:
        return "/".join(rest) if rest else dst_parts[-1]
    if not rest:
        return "/".join(ups)
    return "/".join(ups + rest)


def load_move_map(root: pathlib.Path) -> dict:
    manifest = json.loads(
        (root / "catalog" / "moved-paths.json").read_text(
            encoding="utf-8"))
    return {m["old_path"]: m["new_path"]
            for m in manifest["moves"] if m["status"] == "moved"}


def _resolves_at(root, base_dir, bare):
    """True when *bare* resolves to an existing path from base_dir."""
    norm = normalize_rel(base_dir, bare)
    if norm is None:
        return False
    return (root / norm).exists()


def _remap_target(target: str, old_to_new: dict, written_from: str,
                  now_from: str, moved_source: bool,
                  counter: dict, root) -> str | None:
    """Map a link target to its new expression, or None to leave it.

    Idempotency guard: a target that ALREADY resolves from the source's
    current location is left untouched, so re-running the rewriter never
    re-anchors an already-correct relative link.
    """
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    frag = ""
    bare = target
    if "#" in target:
        bare, frag = target.split("#", 1)
        frag = "#" + frag
    bare = bare.strip()
    if not bare or "," in bare:
        return None
    if "/" not in bare and "." not in bare:
        return None
    if bare.startswith("tmp/"):
        return None
    # Idempotency: already-correct at the current location -> untouched.
    if _resolves_at(root, now_from, bare):
        return None
    new_abs = None
    # Interpretation 1: the link was written relative to the source's
    # PRE-move location (the usual case for a freshly moved source).
    norm = normalize_rel(written_from, bare)
    if norm is not None:
        if norm in old_to_new:
            new_abs = old_to_new[norm]
        elif moved_source and written_from != now_from and \
                _resolves_at(root, written_from, bare):
            # target not moved but still at the pre-move location:
            # re-anchor so it keeps resolving.
            new_abs = norm
    # Interpretation 2: the link was ALREADY re-anchored relative to
    # the source's current (post-move) location in an earlier
    # migration pass, and its target has since moved again.  Resolve
    # against the current location and remap if the resolved path is a
    # moved source.
    if new_abs is None:
        norm_now = normalize_rel(now_from, bare)
        if norm_now is not None and norm_now in old_to_new:
            new_abs = old_to_new[norm_now]
    if new_abs is None:
        return None
    counter["n"] += 1
    return relative_to(now_from, new_abs) + frag


def rewrite_markdown(old_to_new: dict, sources: list[str],
                     root: pathlib.Path) -> dict:
    """Rewrite local links in every markdown file.  Returns stats."""
    stats = {"links_rewritten": 0, "replay_rewritten": 0,
             "files_touched": 0, "ambiguous": []}
    base_to_olds = {}
    for o in old_to_new:
        base_to_olds.setdefault(
            pathlib.PurePosixPath(o).name, []).append(o)

    for rel in sources:
        if not rel.endswith(".md"):
            continue
        path = root / rel
        if not path.exists():
            continue
        old_rel = None
        for o, n in old_to_new.items():
            if n == rel:
                old_rel = o
                break
        written_from = str(pathlib.PurePosixPath(
            old_rel if old_rel else rel).parent)
        if written_from == ".":
            written_from = ""
        now_from = str(pathlib.PurePosixPath(rel).parent)
        if now_from == ".":
            now_from = ""
        moved_source = old_rel is not None

        text = path.read_text(encoding="utf-8")
        counter = {"n": 0}
        replay_changed = 0

        def inline_sub(m):
            new = _remap_target(m.group(2), old_to_new, written_from,
                                now_from, moved_source, counter, root)
            if new is None:
                return m.group(0)
            return m.group(1) + new + m.group(3)

        def refdef_sub(m):
            new = _remap_target(m.group(2), old_to_new, written_from,
                                now_from, moved_source, counter, root)
            if new is None:
                return m.group(0)
            return m.group(1) + new + m.group(3)

        new_text = MD_LINK.sub(inline_sub, text)
        new_text = REF_LINK.sub(refdef_sub, new_text)

        lines = new_text.splitlines()
        out_lines = []
        in_fence = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if FENCE.match(line):
                in_fence = not in_fence
                out_lines.append(line)
                i += 1
                continue
            if in_fence:
                rm = match_replay(lines, i)
                if rm:
                    base, end, form = rm
                    olds = base_to_olds.get(base, [])
                    if len(olds) == 1:
                        new = old_to_new[olds[0]]
                        if form == "line":
                            out_lines.append(
                                line.replace(base, new, 1))
                        else:
                            out_lines.append(lines[i])
                            out_lines.append(
                                lines[i + 1].replace(base, new, 1))
                        replay_changed += 1
                        i = end + 1
                        continue
                    if len(olds) > 1:
                        stats["ambiguous"].append(
                            f"{rel}: replay command basename {base} "
                            f"matches {len(olds)} moves)")
                        i = end + 1
                        continue
            out_lines.append(line)
            i += 1
        final = "\n".join(out_lines)
        if text.endswith("\n"):
            final += "\n"

        if counter["n"] or replay_changed:
            path.write_text(final, encoding="utf-8")
            stats["files_touched"] += 1
            stats["links_rewritten"] += counter["n"]
            stats["replay_rewritten"] += replay_changed
    return stats


def blob_sha16(root: pathlib.Path, rel: str) -> str:
    """SHA-256 of the committed git blob for *rel* under *root*.

    Hashes the index blob (git show :rel) so the value is identical on
    every platform regardless of working-tree line endings.  Inject a
    different callable via update_ledger(hash_func=...) in tests.
    """
    proc = subprocess.run(
        ["git", "show", f":{rel}"], cwd=root, capture_output=True)
    if proc.returncode != 0:
        raise ValueError(f"not a tracked blob: {rel}")
    return hashlib.sha256(proc.stdout).hexdigest()[:16]


def update_ledger(old_to_new: dict, root: pathlib.Path,
                  rehash: bool = True, hash_func=None,
                  manifest_moves=None) -> dict:
    ledger_path = root / "catalog" / "theorem-ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    moved_entries = 0
    for e in ledger["entries"]:
        touched = False
        for key in ("document", "primary_verifier", "independent_audit"):
            v = e.get(key)
            if not v:
                continue
            base_doc = v.split(" (")[0]
            suffix = v[len(base_doc):]
            if base_doc in old_to_new:
                e[key] = old_to_new[base_doc] + suffix
                touched = True
        if touched:
            doc = e["document"].split(" (")[0]
            meta = resolve_claim_package_metadata(
                doc, manifest_moves)
            if meta is not None:
                e["claim_package"] = meta["claim_package"]
                e["proof_variant"] = meta["proof_variant"]
                e["subpackage"] = meta["subpackage"]
            legacy = e.setdefault("legacy_paths", [])
            for o, n in old_to_new.items():
                if n in (doc, e.get("primary_verifier"),
                         e.get("independent_audit")) and o not in legacy:
                    legacy.append(o)
            if rehash and (root / doc).exists():
                hf = hash_func or blob_sha16
                try:
                    e["document_sha256_16"] = hf(root, doc)
                except (ValueError, subprocess.SubprocessError):
                    pass
            moved_entries += 1
    ledger_path.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    return {"ledger_entries_updated": moved_entries}


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[2]
    old_to_new = load_move_map(root)
    try:
        manifest = json.loads((root / "catalog" / "moved-paths.json")
                              .read_text(encoding="utf-8"))
        moves = manifest.get("moves", [])
    except (OSError, json.JSONDecodeError):
        moves = None
    if not old_to_new:
        print("no moved entries in manifest")
        return 1
    out = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True,
        check=True)
    sources = [l for l in out.stdout.splitlines() if l.strip()]
    stats = rewrite_markdown(old_to_new, sources, root)
    led = update_ledger(old_to_new, root, manifest_moves=moves)
    print(json.dumps({**stats, **led}, indent=2))
    if stats["ambiguous"]:
        print("\nAMBIGUOUS (not rewritten):")
        for a in stats["ambiguous"]:
            print("  ", a)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
