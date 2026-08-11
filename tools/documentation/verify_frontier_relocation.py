#!/usr/bin/env python3
"""Verify the lossless archival relocation of programme documentation.

The three source documents are read from the pinned pre-housekeeping Git tree.
Their archival copies must be byte-for-byte identical after one deterministic
operation: local Markdown link destinations are resolved from the source
location, mapped through the documented relocation table, and re-expressed
from the archive location. Exact link labels that are themselves retired path
names are normalized to the live basename. Prose, headings, code fences, and
scientific status text are otherwise untouched.

Run with ``--write`` once to materialize the archive copies, then without
arguments to verify them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import posixpath
import re
import subprocess
import sys

SOURCE_COMMIT = "367eef49e5917a0f71594dce4c18a608850cdd6a"
RELOCATIONS = {
    "README.md": "docs/history/repository-readme-chronicle-through-2026-08-10.md",
    "docs/current-frontier.md": (
        "docs/history/current-frontier-stabilization-snapshot-2026-08-05.md"
    ),
    "docs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md": (
        "docs/history/handoffs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md"
    ),
}
_RETIRED_RESEARCH_NOTES = "RESEARCH" + "_NOTES.md"
_RETIRED_CURRENT_FRONTIER = "CURRENT" + "_FRONTIER.md"
LEGACY_LINK_LABELS = {
    _RETIRED_RESEARCH_NOTES: "research-notes.md",
    f"`{_RETIRED_RESEARCH_NOTES}`": "`research-notes.md`",
    _RETIRED_CURRENT_FRONTIER: "current-frontier stabilization snapshot",
    f"`{_RETIRED_CURRENT_FRONTIER}`": "`current-frontier stabilization snapshot`",
}

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_LINK = re.compile(
    r"(?P<open>!?\[)(?P<label>[^\]\n]*)(?P<middle>\]\()"
    r"(?P<target><[^>\n]+>|[^)\s]+)"
    r"(?P<title>\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?"
    r"(?P<suffix>\))"
)
REFERENCE_LINK = re.compile(
    r"^(?P<prefix>\s{0,3}\[[^\]\n]+\]:\s*)"
    r"(?P<target><[^>\n]+>|\S+)"
    r"(?P<suffix>.*)$"
)
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _git_blob(root: pathlib.Path, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _line_count(text: str) -> int:
    return len(text.splitlines())


def _split_suffix(target: str) -> tuple[str, str]:
    indices = [index for mark in ("#", "?") if (index := target.find(mark)) >= 0]
    if not indices:
        return target, ""
    cut = min(indices)
    return target[:cut], target[cut:]


def _normalize_repo_path(base: str, target: str) -> str:
    normalized = posixpath.normpath(posixpath.join(base, target))
    if normalized == ".." or normalized.startswith("../"):
        raise ValueError(f"link escapes repository: {base=} {target=}")
    return normalized.removeprefix("./")


def _rewrite_target(target: str, source: str, destination: str) -> str | None:
    angled = target.startswith("<") and target.endswith(">")
    bare_target = target[1:-1] if angled else target
    if (
        not bare_target
        or bare_target.startswith(("#", "/", "//"))
        or SCHEME.match(bare_target)
    ):
        return None

    path_part, suffix = _split_suffix(bare_target)
    if not path_part:
        return None

    source_dir = posixpath.dirname(source)
    destination_dir = posixpath.dirname(destination)
    absolute_target = _normalize_repo_path(source_dir, path_part)
    absolute_target = RELOCATIONS.get(absolute_target, absolute_target)
    rewritten = posixpath.relpath(absolute_target, destination_dir or ".") + suffix
    if angled:
        rewritten = f"<{rewritten}>"
    return rewritten if rewritten != target else None


def _transform(text: str, source: str, destination: str) -> tuple[str, int, int]:
    output: list[str] = []
    in_fence = False
    fence_char = ""
    rewrites = 0
    label_rewrites = 0

    for line in text.splitlines(keepends=True):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
            elif marker[0] == fence_char:
                in_fence = False
                fence_char = ""
            output.append(line)
            continue

        if in_fence:
            output.append(line)
            continue

        def inline_replace(match: re.Match[str]) -> str:
            nonlocal label_rewrites, rewrites
            rewritten = _rewrite_target(match.group("target"), source, destination)
            label = LEGACY_LINK_LABELS.get(match.group("label"), match.group("label"))
            if label != match.group("label"):
                label_rewrites += 1
            if rewritten is None and label == match.group("label"):
                return match.group(0)
            if rewritten is not None:
                rewrites += 1
            return (
                match.group("open")
                + label
                + match.group("middle")
                + (rewritten or match.group("target"))
                + (match.group("title") or "")
                + match.group("suffix")
            )

        line = INLINE_LINK.sub(inline_replace, line)
        reference = REFERENCE_LINK.match(line)
        if reference:
            rewritten = _rewrite_target(reference.group("target"), source, destination)
            if rewritten is not None:
                rewrites += 1
                line = reference.group("prefix") + rewritten + reference.group("suffix")
        output.append(line)

    return "".join(output), rewrites, label_rewrites


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="materialize deterministic archival copies before verifying",
    )
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parents[2]
    records = []
    errors = []

    for source, destination in RELOCATIONS.items():
        source_bytes = _git_blob(root, source)
        source_text = source_bytes.decode("utf-8")
        transformed, rewrites, label_rewrites = _transform(
            source_text, source, destination
        )
        expected = transformed.encode("utf-8")
        destination_path = root / destination

        if args.write:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            destination_path.write_bytes(expected)

        actual = destination_path.read_bytes() if destination_path.exists() else b""
        ok = actual == expected
        if not ok:
            errors.append(destination)

        records.append(
            {
                "source": source,
                "archive": destination,
                "source_sha256": _sha256(source_bytes),
                "archive_sha256": _sha256(actual) if actual else None,
                "source_lines": _line_count(source_text),
                "archive_lines": _line_count(actual.decode("utf-8")) if actual else 0,
                "links_reanchored": rewrites,
                "legacy_link_labels_normalized": label_rewrites,
                "exact_transform": ok,
            }
        )

    print(
        json.dumps(
            {
                "source_commit": SOURCE_COMMIT,
                "archives": records,
                "lossless_except_documented_link_rewriting": not errors,
            },
            indent=2,
        )
    )
    if errors:
        print("relocation mismatch: " + ", ".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
