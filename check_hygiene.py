#!/usr/bin/env python3
"""Repository hygiene and integrity checks.

Runs from a clean checkout with only the pinned dependencies
(requirements.txt) and the standard library.  Designed to be the local
mirror of the GitHub Actions job, so a contributor can reproduce CI
with one command:

    python check_hygiene.py

Authoritative local validation operates on an INDEX-COMPLETE candidate
tree.  Every file-selection check below enumerates files through
``git ls-files`` (which includes staged additions but not untracked
files), and ledger hashes use ``git show :path`` index blobs.  The
completeness precondition (check 12) therefore requires that the Git
index already contains the complete candidate commit: nonignored
untracked files and unstaged changes to tracked files are forbidden;
staged changes are allowed.  CI's clean checkout satisfies the same
invariant automatically.  The intended local workflow is:

    git add -A
    python check_hygiene.py
    python tools/migration/rewrite_links.py
    git diff --exit-code

Checks:
  1. every tracked Python file compiles;
  2. no generated solver artifact class is tracked (.sing/.ms/.out/
     .stdout/.drat/.cnf/.log and the brute-force JSON dump patterns);
  3. local Markdown links resolve (files and directories);
  4. catalog/theorem-ledger.json integrity: the Stage 11.5 evidence
     semantics contract is present, status values are declared,
     dependencies remain explicitly unpopulated, documents exist,
     every document_sha256_16 is recomputed and matched, mapped
     verifier/audit scripts are tracked, verified entries carry
     provenance that explains any null field, and component_census is
     explicitly marked as a curated navigation snapshot with valid shape;
  5. no machine-specific checkout paths, vendored-env prefixes, or
     unguarded sys.path injections;
  8. root layout against an exact justified allowlist and entry-count
     target (new debt fails now; grandfathered debt is warning-only
     until the migration reaches its end state);
  9. manifest-aware stale-path enforcement (executed old paths must not
     reappear outside provenance);
  10. executed-batch provenance (every moved entry names a batch file
      freezing its exact mapping);
  11. manifest summary consistency (counts match the move records and
      the moved-only root projection agrees with the executed set);
  12. candidate-index completeness (no nonignored untracked files and
      no unstaged tracked changes, so the tracked-file checks above
      cover the whole candidate commit);
  6. the fast verifier set runs and exits zero;
  7. dependency and solver versions are displayed.

Exit code 0 only if all checks pass.  The fast verifier set is the
only execution step; expensive certificate replays remain manual.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent
                       / "tools" / "migration"))
from replay_command import FENCE, match_replay_targets  # noqa: E402

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
    "claims/arbitrary-order/verify_four_blocker_ideal_obstruction.py",
    "claims/arbitrary-order/verify_fourth_order_permanent_subrank.py",
    "claims/arbitrary-order/verify_exact_three_blocker_permanent_rank.py",
    "claims/arbitrary-order/verify_support_three_p5_contraction_subrank.py",
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


def check_index_complete() -> None:
    """Candidate-index completeness precondition.

    The Git index must contain the complete candidate commit:
    nonignored untracked files and unstaged changes to tracked files
    are forbidden; staged changes are allowed.  All tracked-file
    checks (compile, generated artifacts, Markdown links, ledger
    hashes, portability, root layout, stale paths, provenance, and
    manifest summary) enumerate through ``git ls-files``, and the
    rewriter's fixed-point flow shares the same selection, so a file
    outside the index is outside every check.  Enforcing the
    invariant here makes the local floor a faithful mirror of CI
    (whose clean checkout always satisfies it).
    """
    untracked = [
        line
        for line in subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.splitlines()
        if line.strip()
    ]
    unstaged = subprocess.run(
        ["git", "diff", "--quiet"], cwd=ROOT
    ).returncode != 0
    problems = []
    if untracked:
        shown = "\n    ".join(untracked[:20])
        more = (f"\n    ... ({len(untracked) - 20} more)"
                if len(untracked) > 20 else "")
        problems.append(
            "nonignored untracked files are not staged "
            f"(`git add` them or ignore them):\n    {shown}{more}")
    if unstaged:
        problems.append(
            "unstaged changes to tracked files "
            "(stage them with `git add`)")
    if problems:
        failures.append(
            "candidate index incomplete:\n  " + "\n  ".join(problems))
    else:
        print("[12] candidate index: complete (no nonignored untracked "
              "files, no unstaged tracked changes)")


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


LEDGER_SCHEMA_VERSION = 3
LEDGER_CONTRACT_DOCUMENT = "docs/evidence-semantics-contract.md"
LEDGER_ROLE = "partial_claim_index_not_proof_graph"
LEDGER_DEPENDENCIES_STATE = "reserved_unpopulated"
LEDGER_STATUS_VALUES = {
    "verified", "verified_finite", "verified_generic", "partial",
    "candidate", "exploratory", "withdrawn", "partially_withdrawn",
    "superseded", "framework", "open",
}

VERIFIED_STATUSES = {"verified", "verified_finite", "verified_generic"}
# Provenance values that explain WHY a field is null (an explicit,
# auditable reason) as opposed to being silently unmapped.
PROVENANCE_VALUES = {
    "independent_modular_audit", "companion_point_check_script",
    "independent_exact_identity_audit",
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


def ledger_semantic_issues(ledger: dict) -> list[str]:
    """Validate the machine-enforceable part of the evidence contract.

    This deliberately checks representation, not mathematical truth.  In
    particular, it cannot determine whether a theorem's stated scope or
    status is correct; that remains a scientific review obligation.
    """
    issues = []
    if ledger.get("schema_version") != LEDGER_SCHEMA_VERSION:
        issues.append(
            f"schema_version must be {LEDGER_SCHEMA_VERSION}, got "
            f"{ledger.get('schema_version')!r}")
    if ledger.get("evidence_semantics_contract") != \
            LEDGER_CONTRACT_DOCUMENT:
        issues.append(
            "evidence_semantics_contract must point to "
            f"{LEDGER_CONTRACT_DOCUMENT}")
    if ledger.get("ledger_role") != LEDGER_ROLE:
        issues.append(
            f"ledger_role must remain {LEDGER_ROLE!r}; the theorem ledger "
            "is not a proof DAG")
    if ledger.get("completeness") != "partial_curated":
        issues.append(
            "completeness must remain 'partial_curated' until a dedicated "
            "coverage audit changes the ledger's role")

    conventions = ledger.get("conventions")
    if not isinstance(conventions, dict):
        return issues + ["conventions must be an object"]

    status_values = conventions.get("status_values")
    status_semantics = conventions.get("status_semantics")
    if not isinstance(status_values, list) or not status_values:
        issues.append("conventions.status_values must be a nonempty list")
        status_values = []
    elif len(status_values) != len(set(status_values)):
        issues.append("conventions.status_values contains duplicates")
    if set(status_values) != LEDGER_STATUS_VALUES:
        issues.append(
            "conventions.status_values must match the schema-v3 status "
            "vocabulary")
    if not isinstance(status_semantics, dict):
        issues.append("conventions.status_semantics must be an object")
        status_semantics = {}
    elif set(status_semantics) != LEDGER_STATUS_VALUES:
        issues.append(
            "conventions.status_semantics must define exactly the "
            "schema-v3 status vocabulary")
    for status in status_values:
        if not isinstance(status_semantics.get(status), str):
            issues.append(
                f"status {status!r} lacks a string semantic definition")
    for key in ("status_field_semantics", "axis_separation"):
        if not isinstance(conventions.get(key), str) or not \
                conventions[key].strip():
            issues.append(f"conventions.{key} must be a nonempty string")

    provenance_values = conventions.get("provenance_values")
    if not isinstance(provenance_values, list) or \
            set(provenance_values) != PROVENANCE_VALUES:
        issues.append(
            "conventions.provenance_values must match the hygiene "
            "provenance vocabulary")

    dependency_contract = conventions.get("dependencies")
    if not isinstance(dependency_contract, dict):
        issues.append("conventions.dependencies must be an object")
    else:
        if dependency_contract.get("state") != \
                LEDGER_DEPENDENCIES_STATE:
            issues.append(
                "conventions.dependencies.state must be "
                f"{LEDGER_DEPENDENCIES_STATE!r}")
        if dependency_contract.get("empty_array_means") != "not_recorded":
            issues.append(
                "conventions.dependencies.empty_array_means must be "
                "'not_recorded'")
        if not isinstance(dependency_contract.get("policy"), str) or not \
                dependency_contract["policy"].strip():
            issues.append(
                "conventions.dependencies.policy must be a nonempty string")

    audit_semantics = conventions.get("audit_provenance_semantics")
    required_audit_semantics = {
        "independent_modular_audit",
        "independent_exact_identity_audit",
        "none_exists",
        "not_yet_mapped",
        "historical_certificate_chain",
    }
    if not isinstance(audit_semantics, dict):
        issues.append(
            "conventions.audit_provenance_semantics must be an object")
    else:
        for provenance in sorted(required_audit_semantics):
            if not isinstance(audit_semantics.get(provenance), str) or not \
                    audit_semantics[provenance].strip():
                issues.append(
                    "audit provenance lacks a semantic definition: "
                    f"{provenance}")

    entries = ledger.get("entries")
    if not isinstance(entries, list):
        return issues + ["entries must be a list"]
    allowed = set(status_values)
    for index, entry in enumerate(entries):
        label = entry.get("name", f"entry {index}")
        status = entry.get("status")
        if status not in allowed:
            issues.append(
                f"undeclared status {status!r} ({label})")
        dependencies = entry.get("dependencies")
        if not isinstance(dependencies, list):
            issues.append(f"dependencies must be an array ({label})")
        elif dependencies:
            issues.append(
                "dependencies is reserved/unpopulated; typed relationships "
                f"belong in a future proof-obligation graph ({label})")
        if not isinstance(entry.get("assumptions_and_excluded_divisors"),
                          list):
            issues.append(
                "assumptions_and_excluded_divisors must be an array "
                f"({label})")
        if not isinstance(entry.get("external_binaries"), list):
            issues.append(f"external_binaries must be an array ({label})")
    return issues


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
    issues = ledger_semantic_issues(ledger)

    contract_path = ROOT / LEDGER_CONTRACT_DOCUMENT
    if not contract_path.exists():
        issues.append(
            f"evidence semantics contract missing: {LEDGER_CONTRACT_DOCUMENT}")

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
    # The component census is a curated navigation snapshot.  Do not derive
    # scientific counts from display-name prefixes or composite statuses.
    census = ledger.get("component_census", {})
    if not isinstance(census, dict) or not isinstance(
            census.get("semantics"), str):
        issues.append("component_census must declare its curated semantics")
    for key in ("certified_pure_p4_orbits", "h31_generic_docs_mapped",
                "h31_generic_docs_with_independent_audit",
                "h22_generic_docs_mapped"):
        value = census.get(key) if isinstance(census, dict) else None
        if not isinstance(value, int) or value < 0:
            issues.append(f"component_census.{key} must be a nonnegative int")
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
        print(f"[4] ledger: schema v{ledger.get('schema_version')}, "
              f"{len(ledger['entries'])} entries "
              f"({ledger.get('completeness')}); contract present; "
              f"hashes recomputed "
              f"{hash_checked} ok / {hash_bad} bad; provenance and "
              f"curated census shape consistent; {len(referenced)} referenced "
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
# KG_LAYOUT_STRICT=1 only after a dedicated end-state activation review).
# Every exception is named and justified.  Filename patterns below are
# diagnostics for prioritizing ordinary research artifacts; they are not an
# alternative allowlist and they never authorize a move.
ROOT_FILE_JUSTIFICATIONS = {
    ".gitignore": "repository configuration",
    "AGENTS.md": "repository-wide scientific and agent operating contract",
    "CITATION.cff": "repository citation metadata",
    "CONTRIBUTING.md": "repository-wide contributor entrypoint",
    "Containerfile": "repository environment configuration",
    "LICENSE": "repository license",
    "README.md": "top-level navigation and project status",
    "check_hygiene.py": "explicit repository-wide validation entrypoint",
    "pyproject.toml": "project configuration",
    "requirements.lock.txt": "locked project dependencies",
    "requirements.txt": "project dependencies",
}
ROOT_DIR_JUSTIFICATIONS = {
    ".github": "repository automation configuration",
    "catalog": "machine-readable repository catalogs",
    "claims": "claim-centered scientific packages",
    "docs": "repository documentation",
    "research_figures": "curated research figures",
    "research_snapshots": "pinned research snapshots",
    "src": "shared implementation",
    "tests": "repository tests",
    "tools": "repository tooling",
}
ALLOWED_ROOT_FILES = set(ROOT_FILE_JUSTIFICATIONS)
ALLOWED_ROOT_DIRS = set(ROOT_DIR_JUSTIFICATIONS)
ROOT_COUNT_TARGET = 30
ROOT_UNIVERSE_BASELINE_COUNT = 2363
ROOT_UNIVERSE_BASELINE_SHA256 = (
    "2f4f1af23a89fa3ca56fe2114676c6324385aa1dbd7e5b6ddf35863511edd76c"
)
FORBIDDEN_ROOT_PATTERNS = (
    re.compile(r"^P[4-7]_.*\.md$"),
    re.compile(r"^ARBITRARY_.*\.md$"),
    re.compile(r"^(verify|audit|explore|certify|package|generate|"
               r"probe|derive|check|close|retry|extract)_"
               r"[a-z0-9_]*\.py$"),
)


def root_layout_issues(files: list[str]) -> tuple[list[str], int, int, int]:
    """Return end-state root-policy issues and measured entry counts."""
    root_files = sorted(f for f in files if "/" not in f)
    root_dirs = sorted({f.split("/")[0] for f in files if "/" in f})
    research_pattern_matches = []
    for f in root_files:
        for pat in FORBIDDEN_ROOT_PATTERNS:
            if pat.match(f):
                research_pattern_matches.append(f)
                break
    entries = len(root_files) + len(root_dirs)
    problems = []
    if entries > ROOT_COUNT_TARGET:
        problems.append(
            f"{entries} root entries exceed the target of "
            f"{ROOT_COUNT_TARGET} (migration in progress)")
    unjustified_files = sorted(set(root_files) - ALLOWED_ROOT_FILES)
    unjustified_dirs = sorted(set(root_dirs) - ALLOWED_ROOT_DIRS)
    if unjustified_files:
        problems.append(
            f"{len(unjustified_files)} root files lack an end-state "
            f"allowlist justification, e.g. {unjustified_files[:3]}")
    if unjustified_dirs:
        problems.append(
            f"{len(unjustified_dirs)} root directories lack an end-state "
            f"allowlist justification: {unjustified_dirs[:3]}")
    if research_pattern_matches:
        problems.append(
            f"{len(research_pattern_matches)} root files match ordinary "
            f"research-artifact patterns, e.g. "
            f"{research_pattern_matches[:3]}")
    return problems, entries, len(root_files), len(root_dirs)


def catalog_root_universe(
        classification: dict, unclassified_data: dict
        ) -> tuple[set[str], list[str]]:
    """Return the exact root-path set represented by the two catalogs."""
    issues = []
    entries = classification.get("entries")
    if not isinstance(entries, list):
        return set(), [
            "catalog/layout-classification.json entries must be an array"]
    classified_paths = []
    for index, entry in enumerate(entries):
        old_path = entry.get("old_path") if isinstance(entry, dict) else None
        if not isinstance(old_path, str):
            issues.append(
                "catalog/layout-classification.json has a non-string "
                f"old_path at entry {index}")
        else:
            classified_paths.append(old_path)
    if classification.get("classified_count") != len(classified_paths):
        issues.append(
            "catalog/layout-classification.json classified_count does not "
            "match entries")
    if len(classified_paths) != len(set(classified_paths)):
        issues.append(
            "catalog/layout-classification.json contains duplicate old_path "
            "values")

    unclassified_paths = unclassified_data.get("files")
    if not isinstance(unclassified_paths, list) or not all(
            isinstance(path, str) for path in unclassified_paths):
        issues.append(
            "catalog/unclassified-files.json files must be an array of "
            "strings")
        unclassified_paths = []
    if unclassified_data.get("unclassified_count") != \
            len(unclassified_paths):
        issues.append(
            "catalog/unclassified-files.json count does not match files")
    if len(unclassified_paths) != len(set(unclassified_paths)):
        issues.append(
            "catalog/unclassified-files.json contains duplicate paths")

    classified = set(classified_paths)
    unclassified = set(unclassified_paths)
    overlap = sorted(classified & unclassified)
    if overlap:
        issues.append(
            "classified and unclassified root catalogs overlap: "
            f"{overlap[:10]}")
    root_universe = classified | unclassified
    malformed = sorted(
        path for path in root_universe
        if not path or path != path.strip() or "/" in path or "\\" in path
        or pathlib.PurePosixPath(path).name != path
        or path in {".", ".."})
    if malformed:
        issues.append(
            "root-universe paths must be normalized root basenames: "
            f"{malformed[:10]}")
    return root_universe, issues


def root_universe_fingerprint(root_universe: set[str]) -> tuple[int, str]:
    """Return the order-independent frozen-universe count and digest."""
    encoded = ("\n".join(sorted(root_universe)) + "\n").encode("utf-8")
    return len(root_universe), hashlib.sha256(encoded).hexdigest()


def root_debt_baseline() -> tuple[set[str], list[str]]:
    """Load unresolved grandfathered debt from the frozen root universe."""
    issues = []
    classification_path = ROOT / "catalog" / "layout-classification.json"
    unclassified_path = ROOT / "catalog" / "unclassified-files.json"
    try:
        classification = json.loads(
            classification_path.read_text(encoding="utf-8"))
    except (OSError, TypeError, json.JSONDecodeError) as exc:
        issues.append(f"cannot load classified root-debt baseline: {exc}")
        classification = {}
    try:
        unclassified_data = json.loads(
            unclassified_path.read_text(encoding="utf-8"))
    except (OSError, TypeError, json.JSONDecodeError) as exc:
        issues.append(f"cannot load unclassified root-debt baseline: {exc}")
        unclassified_data = {}
    root_universe, catalog_issues = catalog_root_universe(
        classification, unclassified_data)
    issues.extend(catalog_issues)
    count, digest = root_universe_fingerprint(root_universe)
    if count != ROOT_UNIVERSE_BASELINE_COUNT:
        issues.append(
            f"root universe has {count} paths, expected "
            f"{ROOT_UNIVERSE_BASELINE_COUNT}")
    if digest != ROOT_UNIVERSE_BASELINE_SHA256:
        issues.append(
            f"root-universe hash {digest} does not match frozen "
            f"{ROOT_UNIVERSE_BASELINE_SHA256}")

    manifest_path = ROOT / "catalog" / "moved-paths.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["moves"]:
            if entry.get("executed_batch") and \
                    entry.get("status") != "moved":
                issues.append(
                    "executed root path no longer has status='moved': "
                    f"{entry.get('old_path')}")
        retired = {
            entry["old_path"] for entry in manifest["moves"]
            if entry.get("status") == "moved"
        }
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        issues.append(f"cannot load retired root paths: {exc}")
        retired = set()

    # Debt is a monotonically shrinking subset.  Executed old paths are
    # retired immediately.  The ratchet also rejects disappearance without
    # retirement, so a direct delete cannot create a later resurrection slot.
    return root_universe - retired - ALLOWED_ROOT_FILES, issues


def root_debt_ratchet_issues(
        files: list[str], debt_baseline: set[str]) -> list[str]:
    """Reject new debt, unretired deletion, and unknown directories.

    Membership in ``debt_baseline`` only grandfathers a path pending
    ownership review.  It is not a destination, classification, or move
    approval.
    """
    root_files = {f for f in files if "/" not in f}
    root_dirs = {f.split("/")[0] for f in files if "/" in f}
    new_debt = sorted(root_files - ALLOWED_ROOT_FILES - debt_baseline)
    unretired_missing = sorted(debt_baseline - root_files)
    unknown_dirs = sorted(root_dirs - ALLOWED_ROOT_DIRS)
    issues = []
    if new_debt:
        issues.append(
            f"new unapproved root debt: {new_debt[:10]}"
            + (f" ({len(new_debt)} total)" if len(new_debt) > 10 else ""))
    if unretired_missing:
        issues.append(
            "grandfathered root debt disappeared without manifest "
            f"retirement: {unretired_missing[:10]}"
            + (f" ({len(unretired_missing)} total)"
               if len(unretired_missing) > 10 else ""))
    if unknown_dirs:
        issues.append(f"unapproved top-level directories: {unknown_dirs}")
    return issues


def check_root_layout(files: list[str]) -> None:
    problems, entries, root_file_count, root_dir_count = \
        root_layout_issues(files)
    debt_baseline, baseline_issues = root_debt_baseline()
    ratchet_issues = (root_debt_ratchet_issues(files, debt_baseline)
                      if not baseline_issues else [])
    for issue in baseline_issues + ratchet_issues:
        failures.append(f"root layout ratchet: {issue}")
    strict = os.environ.get("KG_LAYOUT_STRICT") == "1"
    if problems:
        label = "HYGIENE FAILURES" if strict else "LAYOUT WARNINGS"
        print(f"[8] root layout ({'strict' if strict else 'warning-only'}):")
        print(f"    measured {root_file_count} files + "
              f"{root_dir_count} directories")
        for p in problems:
            print(f"    {p}")
        if strict:
            failures.extend(f"root layout: {p}" for p in problems)
    else:
        print(f"[8] root layout: {entries} entries, every root file and "
              "directory explicitly justified")
    if not baseline_issues and not ratchet_issues:
        debt_count = len({f for f in files if "/" not in f}
                         - ALLOWED_ROOT_FILES)
        print(f"    root-debt ratchet: {debt_count} grandfathered paths, "
              "0 new paths")


# Manifest-aware stale-path enforcement (PR review item 6).  After a
# move, the old path must not reappear anywhere except provenance.
STALE_ALLOWLIST_FILES = {
    "catalog/moved-paths.json",
    "catalog/layout-classification.json",
    "catalog/unclassified-files.json",
    "docs/architecture/layout-migration-report.md",
    "docs/architecture/layout-inventory.md",
    # Per-batch dry-run reports record the approved old paths by
    # design; they are provenance, not stale references.
    "docs/architecture/navigation-docs-phase2-dry-run.md",
    "docs/architecture/layout-migration-phase2-report.md",
    "docs/audits/MERGE_AUDIT_REPORT.md",
    "docs/audits/STABILIZATION_AUDIT_REPORT.md",
}
STALE_ALLOWLIST_PREFIXES = (
    "tools/migration/",
    "tests/test_migration_tools.py",
    # Batch approval files record old paths in their member lists by
    # design; they are provenance, not stale references.
    "catalog/batches/",
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
    # Renamed root files (basename changed): the display label of a
    # correct link still spells the old name, so we must not flag a
    # link whose TARGET already points at the new location.
    renamed_base_to_new = {}
    for m in executed:
        old, new = m["old_path"], m["new_path"]
        if ("/" not in old
                and pathlib.PurePosixPath(old).name
                != pathlib.PurePosixPath(new).name):
            renamed_base_to_new[pathlib.PurePosixPath(old).name] = new
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
        # Mask markdown links whose target resolves to the new location
        # of a renamed root file, so their display label (which spells
        # the old basename) is not mistaken for a stale path.
        for base, new in renamed_base_to_new.items():
            masked = re.sub(
                r"\[[^\]]*\]\(" + re.escape(new) + r"(#[^)\s]*)?\)",
                "[link]()", masked)
        # Recompute pat_hit on the masked text; masking may have
        # removed the only occurrence of a checkable.
        pat_hit = pat is not None and pat.search(masked)
        if pat_hit:
            for m in pat.finditer(masked):
                stale.append((rel, m.group(0)))
                break  # one report per file per old path is enough
        if bases_here:
            # Python needs the original text here.  Masking a correct
            # destination path would hide a later ``PATH.name`` use that
            # discards the destination directory and recreates a stale root
            # command.
            bare_scan_text = text if rel.endswith(".py") else masked
            for ctx, base in find_stale_bare_refs(
                    bare_scan_text, rel,
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
#   - a fenced replay command or Markdown YAML-front-matter command
#     ANYWHERE, including inside the destination package: these replay
#     commands are documented as commands executed from the repository
#     root, so a moved script's bare basename is stale even when the Markdown
#     document sits inside that script's destination package.  This is
#     checked before the in-package sibling exemption (Stage 4/5
#     policy: the rewriter repoints these commands regardless of the
#     source's location, and hygiene must agree, otherwise rewrites
#     that are generated but never committed stay invisible);
#   - a markdown link in a ROOT document (](base) resolves to root);
#   - a python subprocess/command string outside the package;
#   - a moved Python path truncated to ``.name`` inside the package when
#     the same call explicitly sets ``cwd`` to repository root;
#   - a shell/yaml python invocation outside the package.
# Inside the destination package other bare references (prose mentions,
# hashes of the sibling file) remain valid sibling references and must
# not be flagged.
def _python_path_name_commands(
        text: str, moved_by_base: dict) -> tuple[set[str], set[str]]:
    """Find moved script paths truncated to ``PATH.name`` in Python argv.

    A correct destination assignment such as ``SCRIPT = ROOT / new_path``
    is still operationally stale when a command later passes
    ``SCRIPT.name`` from repository root: the attribute discards the package
    directory.  This bounded AST check follows only simple assigned names
    into list/tuple argv expressions supplied directly to a call.  The
    second result records the definite repository-root variant where that
    same call explicitly supplies ``cwd=ROOT`` or ``cwd=REPO_ROOT``; this
    must not be hidden by the destination-package sibling exemption.
    Arbitrary metadata and display uses of ``.name`` are intentionally
    ignored.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        # The compile phase reports syntax errors.  Stale-path checking must
        # not replace that clearer failure with a parser traceback.
        return set(), set()

    assigned_bases: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value = node.value
        else:
            continue
        if value is None:
            continue
        bases = set()
        for part in ast.walk(value):
            if not (isinstance(part, ast.Constant)
                    and isinstance(part.value, str)):
                continue
            literal_base = pathlib.PurePosixPath(
                part.value.replace("\\", "/")).name
            if literal_base in moved_by_base:
                bases.add(literal_base)
        if not bases:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                assigned_bases.setdefault(target.id, set()).update(bases)

    stale = set()
    repository_root_stale = set()
    for call in (node for node in ast.walk(tree)
                 if isinstance(node, ast.Call)):
        for argv in (arg for arg in call.args
                     if isinstance(arg, (ast.List, ast.Tuple))):
            parts = list(ast.walk(argv))
            has_python = any(
                isinstance(part, ast.Constant)
                and isinstance(part.value, str)
                and pathlib.PurePosixPath(
                    part.value.replace("\\", "/")).name.lower()
                in {"python", "python3", "python.exe", "python3.exe"}
                for part in parts
            ) or any(
                isinstance(part, ast.Attribute)
                and part.attr == "executable"
                and isinstance(part.value, ast.Name)
                and part.value.id == "sys"
                for part in parts
            )
            if not has_python:
                continue
            call_stale = set()
            for part in parts:
                if not (isinstance(part, ast.Attribute)
                        and part.attr == "name"
                        and isinstance(part.value, ast.Name)):
                    continue
                call_stale.update(assigned_bases.get(part.value.id, set()))
            stale.update(call_stale)
            has_repository_root_cwd = any(
                keyword.arg == "cwd"
                and isinstance(keyword.value, ast.Name)
                and keyword.value.id in {"ROOT", "REPO_ROOT"}
                for keyword in call.keywords
            )
            if has_repository_root_cwd:
                repository_root_stale.update(call_stale)
    return stale, repository_root_stale


def find_stale_bare_refs(text: str, rel: str,
                         moved_by_base: dict) -> list:
    rel_dir = str(pathlib.PurePosixPath(rel).parent)
    if rel_dir == ".":
        rel_dir = ""
    hits = []
    # Fenced and Markdown YAML-front-matter replay commands (run from the
    # repository root), scanned once per file.  The grammar is shared with
    # the rewriter via
    # replay_command.match_replay, so plain, uv-wrapped, and
    # continuation-line forms can never drift between the two
    # machines.
    fenced_stale = set()
    if rel.endswith(".md") and moved_by_base:
        lines = text.splitlines()
        in_fence = False
        in_front_matter = bool(lines and lines[0].strip() == "---")
        i = 0
        while i < len(lines):
            line = lines[i]
            if in_front_matter and i > 0 and line.strip() == "---":
                in_front_matter = False
                i += 1
                continue
            if FENCE.match(line):
                in_fence = not in_fence
                i += 1
                continue
            if in_fence or in_front_matter:
                rm = match_replay_targets(lines, i)
                if rm:
                    bases_c, end, _form = rm
                    fenced_stale.update(
                        base for base in bases_c if base in moved_by_base)
                    i = end + 1
                    continue
            i += 1
    path_name_commands, root_cwd_path_name_commands = (
        _python_path_name_commands(text, moved_by_base)
        if rel.endswith(".py") else (set(), set())
    )
    for base, new in moved_by_base.items():
        pkg_dir = str(pathlib.PurePosixPath(new).parent)
        in_package = rel_dir == pkg_dir or rel_dir.startswith(
            pkg_dir + "/")
        esc = re.escape(base)
        if rel.endswith(".md"):
            # Fenced/front-matter replay commands run from the repository
            # root, so they are stale even inside the destination package.
            # Checked BEFORE the in-package sibling exemption.
            if base in fenced_stale:
                hits.append(("fenced replay command", base))
                continue
            if in_package:
                continue
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
        elif rel.endswith(".py"):
            # An explicit repository-root cwd makes PATH.name stale even
            # when the caller lives inside the moved script's package.
            if base in root_cwd_path_name_commands:
                hits.append(("python Path.name command", base))
                continue
            if in_package:
                continue
            if base in path_name_commands:
                hits.append(("python Path.name command", base))
                continue
            if re.search(
                    r"(subprocess|sys\.executable|python)[^\n]{0,100}?"
                    r"[\"']" + esc + r"[\"']", text):
                hits.append(("python command string", base))
        elif rel.endswith((".yml", ".yaml", ".sh")):
            if in_package:
                continue
            if re.search(
                    r"python3?\s+[\"']?" + esc + r"[\"']?(\s|$)",
                    text, re.M):
                hits.append(("command reference", base))
    return hits



# Executed-batch provenance invariant (Phase 2, item 1C).  Every
# manifest entry with status "moved" must name an executed_batch, the
# named batch file must exist, and the batch must freeze the entry's
# exact old/new mapping.  Batch provenance is a durable integrity
# invariant, not a one-time record.
def check_executed_provenance(files: list[str]) -> None:
    manifest_path = ROOT / "catalog" / "moved-paths.json"
    if not manifest_path.exists():
        print("[10] provenance: no manifest, nothing to enforce")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    moved = [m for m in manifest.get("moves", [])
             if m.get("status") == "moved"]
    problems = []
    batch_cache = {}
    for m in moved:
        bid = m.get("executed_batch")
        if not bid:
            problems.append(
                f"moved entry lacks executed_batch: {m['old_path']}")
            continue
        if bid not in batch_cache:
            bpath = ROOT / "catalog" / "batches" / f"{bid}.json"
            if not bpath.exists():
                problems.append(
                    f"executed_batch file missing for {m['old_path']}: "
                    f"catalog/batches/{bid}.json")
                batch_cache[bid] = None
                continue
            try:
                batch_cache[bid] = json.loads(
                    bpath.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                problems.append(
                    f"executed_batch file unparseable: {bid}")
                batch_cache[bid] = None
                continue
        b = batch_cache[bid]
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
    if problems:
        failures.append(
            "executed-batch provenance violations:\n  "
            + "\n  ".join(problems[:30])
            + (f"\n  ... ({len(problems) - 30} more)"
               if len(problems) > 30 else ""))
    else:
        print(f"[10] provenance: {len(moved)} moved entries all "
              f"reference a batch file with matching mappings")


# Manifest summary consistency invariant (Stage 3 review item 1).  The
# manifest's counts section must be derived from its move records:
#   counts.moved                     == count(status == "moved")
#   counts.proposed_high_confidence  == count(status ==
#                                            "proposed_high_confidence")
#   counts.review_required           == count(status == "review_required")
# and the moved-only root projection must agree with the executed move
# set.  A summary that can drift from the records is a bug by
# definition.
def check_manifest_summary_consistency(files: list[str]) -> None:
    manifest_path = ROOT / "catalog" / "moved-paths.json"
    if not manifest_path.exists():
        print("[11] manifest summary: no manifest, nothing to enforce")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest.get("moves", [])
    counts = manifest.get("counts", {})
    problems = []

    actual = {
        "moved": sum(1 for r in records if r["status"] == "moved"),
        "pilot": sum(1 for r in records if r["status"] == "pilot"),
        "proposed_high_confidence": sum(
            1 for r in records
            if r["status"] == "proposed_high_confidence"),
        "review_required": sum(
            1 for r in records if r["status"] == "review_required"),
        "total_classified_moves": len(records),
    }
    for key, val in actual.items():
        if counts.get(key) != val:
            problems.append(
                f"counts.{key}={counts.get(key)} but records give {val}")

    # The moved-only root projection must agree with the executed move
    # set (root files minus moved sources, plus destination top-level
    # dirs and the fixed architecture dirs).
    moved = [r for r in records if r["status"] == "moved"]
    if moved:
        # Independently recompute the moved-only root projection from
        # the base ref recorded in the manifest, then compare.  This is
        # the same arithmetic build_manifest.recompute_manifest_summary
        # uses, so agreement here means the committed summary matches
        # the executed move set by construction.
        start = manifest.get("starting_commit")
        if start:
            out = subprocess.run(
                ["git", "ls-tree", "-r", "--name-only", start],
                cwd=ROOT, capture_output=True, text=True)
            if out.returncode == 0:
                tree = [l for l in out.stdout.splitlines() if l.strip()]
                base_files = sorted(f for f in tree if "/" not in f)
                base_dirs = sorted({f.split("/")[0] for f in tree
                                    if "/" in f})
                left = [f for f in base_files
                        if f not in {m["old_path"] for m in moved}]
                dirs = set(base_dirs)
                new_dirs = {m["new_path"].split("/")[0] for m in moved}
                fixed_dirs = {".github", "claims", "docs", "src",
                              "tools", "tests", "catalog",
                              "research_snapshots", "research_figures"}
                expected = len(left) + len(dirs | new_dirs | fixed_dirs)
                if counts.get("projected_root_if_moved_only") != expected:
                    problems.append(
                        "projected_root_if_moved_only="
                        f"{counts.get('projected_root_if_moved_only')} "
                        f"but base-ref recomputation gives {expected}")

    if problems:
        failures.append(
            "manifest summary inconsistency:\n  "
            + "\n  ".join(problems[:30])
            + (f"\n  ... ({len(problems) - 30} more)"
               if len(problems) > 30 else ""))
    else:
        print(f"[11] manifest summary: counts match records "
              f"(moved={actual['moved']}, "
              f"proposed={actual['proposed_high_confidence']}, "
              f"review={actual['review_required']}) and moved-only "
              "projection agrees with the executed set")

def main() -> int:
    check_index_complete()
    files = tracked_files()
    check_compiles(files)
    check_no_generated(files)
    check_markdown_links(files)
    check_ledger(files)
    check_portability(files)
    check_root_layout(files)
    check_stale_paths(files)
    check_executed_provenance(files)
    check_manifest_summary_consistency(files)
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
