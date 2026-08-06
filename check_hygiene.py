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
  4. every document, verifier, and audit named in THEOREM_LEDGER.json
     exists, and every verify_*/audit_* script referenced by name in a
     Markdown document exists somewhere in the tracked tree;
  5. the fast verifier set runs and exits zero;
  6. dependency and solver versions are displayed.

Exit code 0 only if all checks pass.  The fast verifier set is the
only execution step; expensive certificate replays remain manual.
"""

from __future__ import annotations

import hashlib
import json
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


def _sha16(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def check_ledger(files: list[str]) -> None:
    ledger_path = ROOT / "THEOREM_LEDGER.json"
    if not ledger_path.exists():
        failures.append("THEOREM_LEDGER.json missing")
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
                actual = _sha16(doc_path)
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
        print(f"[5] verifiers: {len(FAST_VERIFIERS)} fast verifiers pass")


def show_versions() -> None:
    print("[6] versions:")
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


def main() -> int:
    files = tracked_files()
    check_compiles(files)
    check_no_generated(files)
    check_markdown_links(files)
    check_ledger(files)
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
