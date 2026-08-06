#!/usr/bin/env python3
"""Repository hygiene and integrity checks.

Runs from a clean checkout with only the pinned dependencies
(requirements.txt) and the standard library.  Designed to be the local
mirror of the GitHub Actions job, so a contributor can reproduce CI
with one command:

    python check_hygiene.py

Checks:
  1. every tracked Python file compiles;
  2. no generated solver artifact class is tracked (.sing/.ms/.out/
     .stdout/.drat/.cnf/.log and the brute-force JSON dump patterns);
  3. local Markdown links resolve (files and directories);
  4. catalog/theorem-ledger.json integrity: documents exist, every
     document_sha256_16 is recomputed and matched, mapped verifier/
     audit scripts are tracked, verified entries carry provenance that
     explains any null field, and the component_census summary matches
     the entry counts;
  5. no machine-specific checkout paths, vendored-env prefixes, or
     unguarded sys.path injections;
  6. the fast verifier set runs and exits zero;
  7. dependency and solver versions are displayed.

Exit code 0 only if all checks pass.  The fast verifier set is the
only execution step; expensive certificate replays remain manual.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent

GENERATED_SUFFIXES = {
    ".sing", ".ms", ".out", ".stdout", ".drat", ".cnf", ".log",
}
GENERATED_NAME_PATTERNS = [
    re.compile(r"^.*_cegar_state\.json$"),
    re.compile(r"^sat_catalogue.*\.json$"),
    re.compile(r"^.*_core_charts\.json$"),
    re.compile(r"^fresh_singular_replay\.json$"),
    re.compile(r"^q5_311_zero_forest_seeds.*\.json$"),
    re.compile(r"^rare_support_cover\.json$"),
    re.compile(r"^zero_forest_records\.json$"),
    re.compile(r"^rare_zero_probe\.json$"),
    re.compile(r"^focused_ledger\.json$"),
    re.compile(r"^audit_c10\.json$"),
    re.compile(r"^audit_c4c6\.json$"),
    re.compile(r"^degree_one_macaulay_certificates\.json$"),
]
# Hand-authored evidence kept inside snapshots (see MERGE_AUDIT_REPORT):
GENERATED_WHITELIST = {
    "research_snapshots/2026-07-27-p5-coordinate-cegar/"
    "three_partial_c10_audit/manifest.json",
    "research_snapshots/2026-07-27-p5-tree-chart-cover/manifest.json",
}
# Historical exploration/audit scripts referenced by working notes but
# never committed (verified against git log --all on 2026-08-05).  Each
# entry records the dangling reference; the check stays strict for
# everything else.
KNOWN_DANGLING_SCRIPTS = {
    "audit_p5_coordinate_support_ledger.py",
    "audit_p5_fixed_shape_symmetry.py",
    "audit_p5_global_preload_symmetry.py",
    "explore_p5_h22_diagonal_quadric_factor_ratio_rankdrop.py",
    "explore_p5_h22_diagonal_quadric_generic_samples.py",
    "explore_p5_h22_diagonal_quadric_kernel_cofactor_fitting.py",
    "explore_p5_h22_diagonal_quadric_random_modular.py",
    "explore_p5_h22_diagonal_quadric_specialized_exact.py",
    "explore_p5_h31_single_word_quadrilateral.py",
    "explore_p5_h31_split_pair.py",
}

FAST_VERIFIERS = [
    "verify_q2_n6_k4_d4_construction.py",
    "verify_four_blocker_ideal_obstruction.py",
    "verify_fourth_order_permanent_subrank.py",
    "verify_exact_three_blocker_permanent_rank.py",
    "verify_support_three_p5_contraction_subrank.py",
]

SCRIPT_REF = re.compile(
    r"((?:verify|audit|certify|explore|package|derive|check|close|retry)"
    r"_[a-z0-9_]+\.py)"
)
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")

failures: list[str] = []


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line.strip()]


def check_compiles(files: list[str]) -> None:
    bad = []
    count = 0
    for rel in files:
        if not rel.endswith(".py"):
            continue
        count += 1
        path = ROOT / rel
        try:
            py_compile.compile(str(path), doraise=True)
        except (py_compile.PyCompileError, UnicodeDecodeError) as exc:
            bad.append(f"{rel}: {exc}")
    if bad:
        failures.append("compile failures:\n  " + "\n  ".join(bad))
    else:
        print(f"[1] compile: {count} python files OK")


def check_no_generated(files: list[str]) -> None:
    hits = []
    for rel in files:
        path = pathlib.PurePosixPath(rel)
        if rel in GENERATED_WHITELIST:
            continue
        if path.suffix in GENERATED_SUFFIXES:
            hits.append(rel)
        elif any(p.match(path.name) for p in GENERATED_NAME_PATTERNS):
            hits.append(rel)
    if hits:
        failures.append(
            "generated artifacts tracked:\n  " + "\n  ".join(hits[:20])
            + (f"\n  ... ({len(hits) - 20} more)" if len(hits) > 20 else "")
        )
    else:
        print("[2] artifacts: no generated solver outputs tracked")


def check_markdown_links(files: list[str]) -> None:
    broken = []
    md_files = [f for f in files if f.endswith(".md")]
    for rel in md_files:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        base = (ROOT / rel).parent
        for match in MD_LINK.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].strip()
            # file/dir links only: skip bare math tokens with neither a
            # slash nor an extension dot, and skip comma-bearing
            # fragments like the math notation A[S](...,x_u,...)
            if not target or "," in target:
                continue
            if "/" not in target and "." not in target:
                continue
            if target.startswith("tmp/"):
                continue
            resolved = (base / target).resolve()
            if not resolved.exists():
                broken.append(f"{rel} -> {match.group(1)}")
    if broken:
        failures.append(
            "broken markdown links:\n  " + "\n  ".join(broken[:30])
            + (f"\n  ... ({len(broken) - 30} more)"
               if len(broken) > 30 else "")
        )
    else:
        print(f"[3] links: {len(md_files)} markdown files, all local links "
              "resolve")


VERIFIED_STATUSES = {"verified", "verified_finite", "verified_generic"}
# Provenance values that explain WHY a field is null (an explicit,
# auditable reason) as opposed to being silently unmapped.
PROVENANCE_VALUES = {
    "independent_modular_audit", "companion_point_check_script",
    "script_is_the_verifier", "in_document_proof_only",
    "historical_certificate_chain",
    "per_divisor_verify_scripts_named_in_atlas",
    "per_divisor_docs_P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_*",
    "not_yet_mapped", "none_exists",
}
NULL_EXPLAIN_VALUES = {
    "in_document_proof_only", "historical_certificate_chain",
    "per_divisor_verify_scripts_named_in_atlas",
    "per_divisor_docs_P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_*",
    "not_yet_mapped", "none_exists",
}


def _blob_sha16(rel: str) -> str:
    """SHA-256 of the tracked git blob, not the working-tree bytes.

    Hashing the blob makes the hash identical on every platform: git
    normalizes line endings at commit time (LF in the index), while the
    working tree may be CRLF on Windows.  The ledger pins the committed
    content, which is what a clean checkout reproduces.
    """
    proc = subprocess.run(
        ["git", "show", f":{rel}"], cwd=ROOT, capture_output=True,
    )
    if proc.returncode != 0:
        raise ValueError(f"not a tracked blob: {rel}")
    return hashlib.sha256(proc.stdout).hexdigest()[:16]


def check_ledger(files: list[str]) -> None:
    ledger_path = ROOT / "catalog" / "theorem-ledger.json"
    if not ledger_path.exists():
        failures.append("catalog/theorem-ledger.json missing")
        return
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    by_base = {}
    tracked_set = set(files)
    for rel in files:
        by_base.setdefault(pathlib.PurePosixPath(rel).name, []).append(rel)
    hash_checked = 0
    hash_bad = 0
    issues = []

    for entry in ledger["entries"]:
        name = entry.get("name", "<unnamed>")
        doc = entry["document"].split(" (")[0]
        doc_path = ROOT / doc
        if not doc_path.exists():
            issues.append(f"ledger doc missing: {doc} ({name})")
        else:
            recorded = entry.get("document_sha256_16")
            if recorded is not None:
                actual = _blob_sha16(doc)
                if actual != recorded:
                    hash_bad += 1
                    issues.append(
                        f"hash mismatch: {doc} recorded={recorded} "
                        f"actual={actual} ({name})")
                else:
                    hash_checked += 1
        # mapped script references must exist in the tracked tree
        for key in ("primary_verifier", "independent_audit"):
            ref = entry.get(key)
            if ref and (ref not in tracked_set and ref not in by_base):
                issues.append(
                    f"ledger {key} not tracked: {ref} ({name})")
        # provenance contract for verified statuses
        if entry.get("status") in VERIFIED_STATUSES:
            for field, refkey in (("verifier_provenance", "primary_verifier"),
                                  ("audit_provenance", "independent_audit")):
                prov = entry.get(field)
                ref = entry.get(refkey)
                if prov is None or prov not in PROVENANCE_VALUES:
                    issues.append(
                        f"{field} missing/unknown for verified entry: "
                        f"{prov!r} ({name})")
                elif ref is None and prov not in NULL_EXPLAIN_VALUES:
                    issues.append(
                        f"{field}={prov!r} but {refkey} is null; need an "
                        f"explicit null reason ({name})")
                elif ref is not None and prov == "none_exists":
                    issues.append(
                        f"{refkey} mapped but {field}='none_exists' "
                        f"({name})")
    # validate the summary blocks against the entries themselves
    h31 = [e for e in ledger["entries"]
           if e.get("name", "").startswith("Generic marked H31")]
    h22 = [e for e in ledger["entries"]
           if e.get("name", "").startswith("Generic weighted H22")]
    census = ledger.get("component_census", {})
    checks = {
        "h31_generic_docs_mapped": len(h31),
        "h31_generic_docs_with_independent_audit":
            sum(1 for e in h31 if e.get("independent_audit")),
        "h22_generic_docs_mapped": len(h22),
    }
    for key, expected in checks.items():
        recorded = census.get(key)
        if recorded != expected:
            issues.append(
                f"component_census.{key}={recorded} but entries give "
                f"{expected}")
    if ledger.get("global_status") != "UNRESOLVED":
        issues.append(
            f"global_status must stay UNRESOLVED, got "
            f"{ledger.get('global_status')!r}")

    # every proof-side script named in a markdown doc must exist
    # somewhere in the tracked tree (root or snapshot script dirs)
    md_text = ""
    for rel in files:
        if rel.endswith(".md"):
            md_text += (ROOT / rel).read_text(
                encoding="utf-8", errors="replace")
    referenced = set(SCRIPT_REF.findall(md_text))
    dangling = []
    for name in sorted(referenced):
        if name in by_base:
            continue
        if name in KNOWN_DANGLING_SCRIPTS:
            continue
        dangling.append(name)
    for d in dangling:
        issues.append(f"referenced script: {d}")

    if issues:
        failures.append(
            "ledger/reference integrity:\n  " + "\n  ".join(issues[:30])
            + (f"\n  ... ({len(issues) - 30} more)"
               if len(issues) > 30 else ""))
    else:
        print(f"[4] ledger: {len(ledger['entries'])} entries "
              f"({ledger.get('completeness')}); hashes recomputed "
              f"{hash_checked} ok / {hash_bad} bad; provenance and "
              f"census summary consistent; {len(referenced)} referenced "
              f"scripts exist ({len(KNOWN_DANGLING_SCRIPTS)} historical "
              "dangling refs allowlisted)")


def check_fast_verifiers() -> None:
    results = []
    for name in FAST_VERIFIERS:
        proc = subprocess.run(
            [sys.executable, name], cwd=ROOT, capture_output=True,
            timeout=600,
        )
        results.append((name, proc.returncode))
    bad = [f"{n} rc={rc}" for n, rc in results if rc != 0]
    if bad:
        failures.append("fast verifier failures:\n  " + "\n  ".join(bad))
    else:
        print(f"[6] verifiers: {len(FAST_VERIFIERS)} fast verifiers pass")


# Files that legitimately NAME the forbidden patterns in order to record
# their removal (the audit reports) or to enforce them (this checker).
PORTABILITY_ALLOWLIST = {
    "check_hygiene.py",
    "MERGE_AUDIT_REPORT.md",
    "STABILIZATION_AUDIT_REPORT.md",
}
FORBIDDEN_PORTABILITY = (
    "PYTHONPATH=tmp/python_deps",
    "tmp/codex_verify_env",
    "/home/user/open-graph-theory-with-prize",
)
HOME_LITERAL = re.compile(r'["\'](/home/[^"\']*)["\']')
SYSPATH_LITERAL = re.compile(
    r"sys\.path\.(?:insert|append)\s*\([^)]*[\"']([^\"']+)[\"']")
MACHINE_SPECIFIC = re.compile(r"(/home/|C:[\\/]|tmp/python_deps|"
                              r"tmp/codex_verify_env)")


def check_portability(files: list[str]) -> None:
    offenders = []
    for rel in files:
        base = pathlib.PurePosixPath(rel).name
        if base in PORTABILITY_ALLOWLIST:
            continue
        if not rel.endswith((".py", ".md", ".sh", ".yml", ".yaml")):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        for pat in FORBIDDEN_PORTABILITY:
            if pat in text:
                offenders.append(f"{rel}: contains {pat!r}")
        if rel.endswith(".py"):
            for m in HOME_LITERAL.finditer(text):
                offenders.append(
                    f"{rel}: hardcoded home path {m.group(1)!r}")
            for m in SYSPATH_LITERAL.finditer(text):
                if MACHINE_SPECIFIC.search(m.group(1)):
                    offenders.append(
                        f"{rel}: machine-specific sys.path injection "
                        f"{m.group(1)!r}")
    if offenders:
        failures.append(
            "portability regressions:\n  " + "\n  ".join(offenders[:30])
            + (f"\n  ... ({len(offenders) - 30} more)"
               if len(offenders) > 30 else ""))
    else:
        print("[5] portability: no machine-specific checkout paths, "
              "vendored-env prefixes, or unguarded sys.path injections")


def show_versions() -> None:
    print("[7] versions:")
    try:
        import numpy
        import sympy
        print(f"    python {sys.version.split()[0]}")
        print(f"    sympy {sympy.__version__}")
        print(f"    numpy {numpy.__version__}")
    except ImportError as exc:
        failures.append(f"import failure: {exc}")
    try:
        from importlib.metadata import version
        print(f"    python-sat {version('python-sat')}")
    except Exception:
        print("    python-sat: not installed")
    for tool in ("Singular", "msolve", "kissat", "glucose", "drat-trim"):
        found = shutil.which(tool)
        print(f"    {tool}: {found or 'not on PATH (manual replays only)'}")


# Root-layout enforcement (warning-only during the migration; set
# KG_LAYOUT_STRICT=1 to fail, e.g. once bulk migration is complete).
ALLOWED_ROOT_FILES = {
    "README.md", "LICENSE", "CONTRIBUTING.md", "CITATION.cff",
    "pyproject.toml", "requirements.txt", "requirements.lock.txt",
    "Containerfile", ".gitignore",
}
ALLOWED_ROOT_DIRS = {
    ".github", "claims", "docs", "src", "tools", "tests", "catalog",
    "research_snapshots", "research_figures",
}
ROOT_COUNT_TARGET = 30
FORBIDDEN_ROOT_PATTERNS = (
    re.compile(r"^P[4-7]_.*\.md$"),
    re.compile(r"^ARBITRARY_.*\.md$"),
    re.compile(r"^(verify|audit|explore|certify|package|generate|"
               r"probe|derive|check|close|retry|extract)_"
               r"[a-z0-9_]*\.py$"),
)


def check_root_layout(files: list[str]) -> None:
    root_files = sorted(f for f in files if "/" not in f)
    root_dirs = sorted({f.split("/")[0] for f in files if "/" in f})
    violations = []
    for f in root_files:
        if f in ALLOWED_ROOT_FILES:
            continue
        for pat in FORBIDDEN_ROOT_PATTERNS:
            if pat.match(f):
                violations.append(f)
                break
    entries = len(root_files) + len(root_dirs)
    strict = os.environ.get("KG_LAYOUT_STRICT") == "1"
    problems = []
    if entries > ROOT_COUNT_TARGET:
        problems.append(
            f"{entries} root entries exceed the target of "
            f"{ROOT_COUNT_TARGET} (migration in progress)")
    if violations:
        problems.append(
            f"{len(violations)} root files match forbidden patterns, "
            f"e.g. {violations[:3]}")
    if problems:
        label = "HYGIENE FAILURES" if strict else "LAYOUT WARNINGS"
        print(f"[8] root layout ({'strict' if strict else 'warning-only'}):")
        for p in problems:
            print(f"    {p}")
        if strict:
            failures.extend(f"root layout: {p}" for p in problems)
    else:
        print(f"[8] root layout: {entries} entries, no forbidden "
              "patterns")


# Manifest-aware stale-path enforcement (PR review item 6).  After a
# move, the old path must not reappear anywhere except provenance.
STALE_ALLOWLIST_FILES = {
    "catalog/moved-paths.json",
    "catalog/layout-classification.json",
    "catalog/unclassified-files.json",
    "docs/architecture/layout-migration-report.md",
    "docs/architecture/layout-inventory.md",
    "MERGE_AUDIT_REPORT.md",
    "STABILIZATION_AUDIT_REPORT.md",
}
STALE_ALLOWLIST_PREFIXES = (
    "tools/migration/",
    "tests/test_migration_tools.py",
)
STALE_SCAN_EXTENSIONS = (".md", ".py", ".yml", ".yaml", ".sh", ".json")


def _json_strings_outside_legacy(node, out: list) -> None:
    """Collect JSON string values, skipping legacy_paths fields."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "legacy_paths":
                continue
            _json_strings_outside_legacy(v, out)
    elif isinstance(node, list):
        for item in node:
            _json_strings_outside_legacy(item, out)
    elif isinstance(node, str):
        out.append(node)


def check_stale_paths(files: list[str]) -> None:
    manifest_path = ROOT / "catalog" / "moved-paths.json"
    if not manifest_path.exists():
        print("[9] stale paths: no manifest, nothing to enforce")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    moves = manifest.get("moves", [])
    old_paths = {m["old_path"] for m in moves}
    new_paths = {m["new_path"] for m in moves}
    # Enforcement applies only to EXECUTED moves (status "moved").
    # Planned-but-unexecuted moves still sit at their old location, so
    # referencing them there is correct until a batch actually runs.
    executed = [m for m in moves if m["status"] == "moved"]
    current_basenames = {pathlib.PurePosixPath(f).name for f in files}
    # Full old paths enforceable when unambiguous: sub-path moves, or
    # root files renamed away entirely.
    checkables = sorted(
        old for old in {m["old_path"] for m in executed}
        if "/" in old
        or pathlib.PurePosixPath(old).name not in current_basenames)
    # Executed root->package moves keeping the filename: enforced
    # context-aware via bare-basename reference scanning.
    moved_by_base = {}
    for m in executed:
        old, new = m["old_path"], m["new_path"]
        if ("/" not in old
                and pathlib.PurePosixPath(old).name
                == pathlib.PurePosixPath(new).name):
            moved_by_base[pathlib.PurePosixPath(old).name] = new
    pat = (re.compile("|".join(re.escape(o) for o in checkables))
           if checkables else None)
    # Precompute the (bounded) set of new paths that can embed an old
    # path, so per-file masking never scans the whole move table.
    maskable_for_checkables = sorted(
        np for np in new_paths
        if any(c in np for c in checkables)) if checkables else []
    stale = []
    for rel in files:
        if not rel.endswith(STALE_SCAN_EXTENSIONS):
            continue
        if rel in STALE_ALLOWLIST_FILES:
            continue
        if rel.startswith(STALE_ALLOWLIST_PREFIXES):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8",
                                      errors="replace")
        if pat is None and not moved_by_base:
            continue
        pat_hit = pat is not None and pat.search(text)
        # Cheap prefilter for the bare-basename scan: only bases that
        # actually occur in this file need context analysis.
        bases_here = {b for b in moved_by_base if b in text}
        if not pat_hit and not bases_here:
            continue
        if rel.endswith(".json"):
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                stale.append((rel, "unparseable JSON containing an "
                                   "old path"))
                continue
            strings = []
            _json_strings_outside_legacy(data, strings)
            hits = sorted({s for s in strings if s in checkables})
            for h in hits:
                stale.append((rel, h))
            continue
        # Mask current (correct) paths so an old string inside a new
        # path cannot false-positive, then re-scan.  Only the small
        # relevant subsets are masked, never the whole move table.
        masked = text
        for np in maskable_for_checkables:
            if np in masked:
                masked = masked.replace(np, "")
        for base in bases_here:
            np = moved_by_base[base]
            if np in masked:
                masked = masked.replace(np, "")
        if pat_hit:
            for m in pat.finditer(masked):
                stale.append((rel, m.group(0)))
                break  # one report per file per old path is enough
        if bases_here:
            for ctx, base in find_stale_bare_refs(
                    masked, rel,
                    {b: moved_by_base[b] for b in bases_here}):
                stale.append((rel, f"{base} ({ctx})"))
    enforced = len(checkables) + len(moved_by_base)
    if stale:
        failures.append(
            "stale legacy paths found (manifest-aware):\n  "
            + "\n  ".join(f"{r}: {p}" for r, p in stale[:30])
            + (f"\n  ... ({len(stale) - 30} more)"
               if len(stale) > 30 else ""))
    else:
        print(f"[9] stale paths: {enforced} enforceable old paths "
              f"({len(checkables)} full-path, {len(moved_by_base)} "
              "root-to-package), none present outside provenance")


# Context-aware stale-REFERENCE detection for root->package moves that
# keep their filename (review item: root-to-package coverage).  A bare
# basename is actionable only where it resolves to the OLD location:
#   - a markdown link in a ROOT document (](base) resolves to root);
#   - a fenced replay command anywhere outside the destination package
#     (documented commands run from the repository root);
#   - a python subprocess/command string outside the package;
#   - a shell/yaml python invocation outside the package.
# Inside the destination package the same basename is a valid sibling
# reference and must not be flagged.
def find_stale_bare_refs(text: str, rel: str,
                         moved_by_base: dict) -> list:
    rel_dir = str(pathlib.PurePosixPath(rel).parent)
    if rel_dir == ".":
        rel_dir = ""
    hits = []
    for base, new in moved_by_base.items():
        pkg_dir = str(pathlib.PurePosixPath(new).parent)
        in_package = rel_dir == pkg_dir or rel_dir.startswith(
            pkg_dir + "/")
        if in_package:
            continue
        esc = re.escape(base)
        if rel.endswith(".md"):
            # inline links in root documents resolve to the old path
            if rel_dir == "" and re.search(
                    r"\]\(" + esc + r"(#[^)\s]*)?\)", text):
                hits.append(("markdown link", base))
                continue
            if rel_dir == "" and re.search(
                    r"^\s*\[[^\]]+\]:\s*" + esc + r"\s*$", text,
                    re.M):
                hits.append(("reference-style link", base))
                continue
            # fenced replay commands (run from the repository root)
            in_fence = False
            for line in text.splitlines():
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence and re.match(
                        r"\s*(python3?|wsl[^\n]*python3?)\s+" + esc
                        + r"(\s|$)", line):
                    hits.append(("fenced replay command", base))
                    break
        elif rel.endswith(".py"):
            if re.search(
                    r"(subprocess|sys\.executable|python)[^\n]{0,100}?"
                    r"[\"']" + esc + r"[\"']", text):
                hits.append(("python command string", base))
        elif rel.endswith((".yml", ".yaml", ".sh")):
            if re.search(
                    r"python3?\s+[\"']?" + esc + r"[\"']?(\s|$)",
                    text, re.M):
                hits.append(("command reference", base))
    return hits


def main() -> int:
    files = tracked_files()
    check_compiles(files)
    check_no_generated(files)
    check_markdown_links(files)
    check_ledger(files)
    check_portability(files)
    check_root_layout(files)
    check_stale_paths(files)
    check_fast_verifiers()
    show_versions()
    if failures:
        print("\nHYGIENE FAILURES:")
        for failure in failures:
            print("  -", failure)
        return 1
    print("\nhygiene: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
