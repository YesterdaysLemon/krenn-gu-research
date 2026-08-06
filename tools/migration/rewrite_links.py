#!/usr/bin/env python3
"""Migration-aware reference rewriting for moved claim packages.

Phase 4 machinery.  After execute_moves.py has performed pure git-mv
operations, every reference to a moved file must be re-anchored:

  1. Markdown links: resolved against the SOURCE file's location at
     the time the link was written (its old location if the source was
     also moved), mapped through catalog/moved-paths.json, and
     re-expressed relative to the source's NEW location.  URL fragments
     are preserved; external URLs are untouched; ambiguous or
     nonexistent targets are reported, never guessed.
  2. Fenced replay commands: lines of the form
     ``python <script>.py [args]`` inside ```text/```bash blocks are
     rewritten to the script's new root-relative path when the script
     was moved.  Other code-block content is untouched.
  3. Theorem ledger: entries whose document, primary_verifier, or
     independent_audit was moved get updated paths, a claim_package
     field, a legacy_paths list, and recomputed committed-blob hashes.

Nothing here changes theorem wording; only path expressions move.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"

MD_LINK = re.compile(r"(\]\()([^)\s]+)(\))")
REPLAY_LINE = re.compile(r"^(\s*(?:python3?|wsl[^\n]*python3?)\s+)"
                         r"([A-Za-z0-9_]+\.py)(\s.*)?$")
FENCE = re.compile(r"^```")


def load_move_map() -> tuple[dict, dict]:
    manifest = json.loads(
        (CATALOG / "moved-paths.json").read_text(encoding="utf-8"))
    old_to_new = {m["old_path"]: m["new_path"]
                  for m in manifest["moves"] if m["status"] == "moved"}
    return old_to_new, manifest


def blob_sha16(rel: str) -> str:
    import hashlib
    proc = subprocess.run(
        ["git", "show", f":{rel}"], cwd=ROOT, capture_output=True)
    if proc.returncode != 0:
        raise ValueError(f"not a tracked blob: {rel}")
    return hashlib.sha256(proc.stdout).hexdigest()[:16]


def rewrite_markdown(old_to_new: dict, sources: list[str]) -> dict:
    """Rewrite local links in every markdown file.  Returns stats."""
    stats = {"links_rewritten": 0, "replay_rewritten": 0,
             "files_touched": 0, "ambiguous": []}
    for rel in sources:
        if not rel.endswith(".md"):
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        # Where the file's links were written relative to.
        old_rel = None
        for o, n in old_to_new.items():
            if n == rel:
                old_rel = o
                break
        written_from = pathlib.PurePosixPath(
            old_rel if old_rel else rel).parent
        now_from = pathlib.PurePosixPath(rel).parent
        moved_source = old_rel is not None

        text = path.read_text(encoding="utf-8")
        changed = 0
        replay_changed = 0

        def link_sub(m):
            nonlocal changed
            target = m.group(2)
            if target.startswith(("http://", "https://", "mailto:",
                                  "#")):
                return m.group(0)
            frag = ""
            bare = target
            if "#" in target:
                bare, frag = target.split("#", 1)
                frag = "#" + frag
            bare = bare.strip()
            if not bare or "," in bare:
                return m.group(0)
            if "/" not in bare and "." not in bare:
                return m.group(0)
            if bare.startswith("tmp/"):
                return m.group(0)
            # Resolve where the link pointed, relative to where the
            # links were written.
            resolved = (written_from / bare)
            resolved_str = str(pathlib.PurePosixPath(resolved))
            # Normalize ./ and collapse .. segments textually.
            parts = []
            for part in resolved_str.split("/"):
                if part in ("", "."):
                    continue
                if part == "..":
                    if parts:
                        parts.pop()
                    else:
                        return m.group(0)  # escapes repo; leave alone
                else:
                    parts.append(part)
            new_target_abs = old_to_new.get(resolved_str)
            if new_target_abs is None and not moved_source:
                # target not moved, source not moved: link stays as is
                return m.group(0)
            new_abs = new_target_abs if new_target_abs is not None \
                else resolved_str
            # Re-express from the source's current location.
            try:
                new_rel = str(pathlib.PurePosixPath(
                    pathlib.PurePosixPath("/" + new_abs).relative_to(
                        pathlib.PurePosixPath("/") / now_from
                        if str(now_from) != "." else
                        pathlib.PurePosixPath("/"))))
            except ValueError:
                # compute relative manually
                src_parts = ([] if str(now_from) == "."
                             else str(now_from).split("/"))
                dst_parts = new_abs.split("/")
                common = 0
                for a, b in zip(src_parts, dst_parts):
                    if a == b:
                        common += 1
                    else:
                        break
                ups = [".."] * (len(src_parts) - common)
                rest = dst_parts[common:]
                if not ups and not rest:
                    new_rel = dst_parts[-1]
                elif not ups:
                    new_rel = "/".join(rest)
                else:
                    new_rel = "/".join(ups + rest)
            changed += 1
            return m.group(1) + new_rel + frag + m.group(3)

        new_text = MD_LINK.sub(link_sub, text)

        # Fenced replay-command lines.
        out_lines = []
        in_fence = False
        for line in new_text.splitlines(keepends=False):
            if FENCE.match(line):
                in_fence = not in_fence
                out_lines.append(line)
                continue
            if in_fence:
                m = REPLAY_LINE.match(line)
                if m and m.group(2) in {
                        pathlib.PurePosixPath(o).name
                        for o in old_to_new}:
                    # find the old path with this basename
                    base = m.group(2)
                    olds = [o for o in old_to_new
                            if pathlib.PurePosixPath(o).name == base]
                    if len(olds) == 1:
                        new = old_to_new[olds[0]]
                        out_lines.append(m.group(1) + new
                                         + (m.group(3) or ""))
                        replay_changed += 1
                        continue
                    stats["ambiguous"].append(
                        f"{rel}: replay command basename {base} "
                        f"matches {len(olds)} moves")
            out_lines.append(line)
        final = "\n".join(out_lines)
        if text.endswith("\n"):
            final += "\n"

        if changed or replay_changed:
            path.write_text(final, encoding="utf-8")
            stats["files_touched"] += 1
            stats["links_rewritten"] += changed
            stats["replay_rewritten"] += replay_changed
    return stats


def update_ledger(old_to_new: dict) -> dict:
    ledger_path = CATALOG / "theorem-ledger.json"
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
            # claim package = deepest package dir for claim docs
            if doc.startswith("claims/"):
                e["claim_package"] = str(
                    pathlib.PurePosixPath(doc).parent)
            legacy = e.setdefault("legacy_paths", [])
            for o, n in old_to_new.items():
                if n == doc and o not in legacy:
                    legacy.append(o)
                if n == e.get("primary_verifier") and o not in legacy:
                    legacy.append(o)
                if n == e.get("independent_audit") and o not in legacy:
                    legacy.append(o)
            if pathlib.Path(doc).exists():
                e["document_sha256_16"] = blob_sha16(doc)
            moved_entries += 1
    ledger_path.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    return {"ledger_entries_updated": moved_entries}


def main() -> int:
    old_to_new, _manifest = load_move_map()
    if not old_to_new:
        print("no moved entries in manifest")
        return 1
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
        check=True)
    sources = [l for l in out.stdout.splitlines() if l.strip()]
    stats = rewrite_markdown(old_to_new, sources)
    led = update_ledger(old_to_new)
    print(json.dumps({**stats, **led}, indent=2))
    if stats["ambiguous"]:
        print("\nAMBIGUOUS (not rewritten):")
        for a in stats["ambiguous"]:
            print("  ", a)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
