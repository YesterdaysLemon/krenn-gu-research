#!/usr/bin/env python3
"""Repository layout inventory and evidence-based classification.

Phase 1 of the root-evacuation migration.  Reads the tracked tree from
Git (never a truncated directory listing) and produces:

  docs/architecture/layout-inventory.md   human-readable inventory
  catalog/layout-classification.json      per-file proposed destination
  catalog/unclassified-files.json         files no rule classifies

Classification is deliberately conservative: every proposed move lists
its evidence (filename family, theorem-ledger entry, matching
verify/audit triple, import-graph role).  A file is only classified by
a rule; anything no rule covers is reported as unclassified and stays
put until a human decides.  No file is moved by this tool.
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"
DOCS = ROOT / "docs"

MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
SCRIPT_REF = re.compile(
    r"((?:verify|audit|certify|explore|package|derive|generate|probe|"
    r"run|search|sample|solve|materialize|enumerate|count|classify|"
    r"check|close|retry|extract|write|find|scout|compare|combine|"
    r"minimize|maximize|iterate|learn|augment|convert|decode|recover|"
    r"condition|retrofit|reorient|branch|snapshot|analyze)"
    r"_[a-z0-9_]+\.py)")
SUBPROCESS_PY = re.compile(
    r"""["']((?:verify|audit|certify|explore|generate|run|search|"""
    r"""package|probe|solve|sample|materialize|enumerate|check|"""
    r"""extract|write|find|count|classify)_[a-z0-9_]*\.py)["']""")

# Filename status markers.
WITHDRAWN_RE = re.compile(r"WITHDRAWN", re.I)
CANDIDATE_RE = re.compile(r"CANDIDATE", re.I)
VERIFICATION_RE = re.compile(r"VERIFICATION", re.I)

ORDER_PREFIX = {
    "SIX_VERTEX": "claims/finite/n06",
    "TWO_VERTEX": "claims/finite/n06",
    "EIGHT_VERTEX": "claims/finite/n08",
    "TEN_VERTEX": "claims/finite/n10",
    "TWELVE_VERTEX": "claims/finite/n12",
    "FOURTEEN_VERTEX": "claims/finite/n14",
}

ARBITRARY_PREFIXES = (
    "ARBITRARY", "THREE_COLOUR", "FOUR_REGULAR", "FIVE_REGULAR",
    "FIVE_MODE", "SIX_BLOCKER", "FIVE_ROOT", "FOUR_BLOCKER",
    "FOUR_RESIDUAL", "FOUR_ROOT", "EXACT_THREE_BLOCKER",
    "FOURTH_ORDER", "SUPPORT_THREE", "SUPPORT_FOUR", "FIVE_ROW",
    "UNIVERSAL", "ODD_FULL", "EVEN_CYCLE", "MINIMAL_SINGLETON",
    "SINGLE_EVEN_CYCLE", "MATCHING_FORK", "RECIPROCAL", "KILLER",
    "PINNED_FACTOR", "PARTIAL_CIRCUIT", "PARTIAL_MINIMAL",
    "HAFNIAN", "INTEGER_SIGNED", "INTEGER_CONSTANT", "FULL_COLOUR",
    "FULL_ADMISSIBLE", "COLOUR_SYMMETRIC", "ADJACENT_PORT",
    "DOUBLE_STAR", "MULTI_STAR", "STATE_LIFT", "ROOT_OF_UNITY",
    "ROOT_M7", "ROOT_TANGENT", "RESPONSE_JETS", "WICK",
    "COMPONENT19", "COMPONENT20", "TWO_RESIDUAL", "SIGNED_BINOMIAL",
    "GAUGE_PARTITION", "THREE_COLOUR_HYPERPLANE", "ALL_QUADRANGLE",
    "ALL_PAIR", "APOLAR", "BOSONIC", "GRAPH_EXTRACTION",
    "HIGHER_RESIDUAL", "RESIDUAL_HAFNIAN", "FORMAL_EULER",
)
# verify_/audit_/certify_ scripts are classified by pairing to their
# document (doc_for_script) rather than by prefix guessing.

TOOL_EXPLORE_PREFIXES = (
    "explore_", "probe_", "scout_", "search_", "find_", "enumerate_",
    "count_", "classify_", "compare_", "analyze_", "derive_",
    "extract_", "check_", "close_", "retry_", "minimize_", "maximize_",
    "iterate_", "learn_",
)
TOOL_GENERATE_PREFIXES = (
    "generate_", "write_", "materialize_", "augment_", "combine_",
    "convert_", "decode_", "recover_", "condition_", "retrofit_",
    "reorient_", "snapshot_", "solve_", "run_", "branch_", "sample_",
)


def tracked_files(ref: str | None = None) -> list[str]:
    cmd = (["git", "ls-tree", "-r", "--name-only", ref] if ref
           else ["git", "ls-files"])
    out = subprocess.run(
        cmd, cwd=ROOT, capture_output=True, text=True, check=True)
    return [l for l in out.stdout.splitlines() if l.strip()]


def read_at(ref: str | None, rel: str) -> str:
    """Read a tracked file's content at *ref*, or from the working
    tree when ref is None.  Git stores LF bytes, so content read this
    way is identical on every platform."""
    if ref is None:
        return (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    proc = subprocess.run(
        ["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise FileNotFoundError(f"{ref}:{rel}")
    return proc.stdout


def resolve_ref(ref: str) -> str:
    out = subprocess.run(
        ["git", "rev-parse", ref], cwd=ROOT, capture_output=True,
        text=True, check=True)
    return out.stdout.strip()


def load_ledger(files: list[str], ref: str | None = None) -> dict:
    for cand in ("catalog/theorem-ledger.json", "THEOREM_LEDGER.json"):
        if cand in files:
            return json.loads(read_at(ref, cand))
    return {}


def slugify(name: str) -> str:
    return name.lower().replace("_", "-")


def build_family_maps(root_files: list[str]) -> tuple[dict, dict]:
    """Seed P5_H31/P5_H22 families from the generic theorem docs.

    A family is defined by every ``P5_H{31,22}_<FAMILY>_GENERIC_
    OBSTRUCTION.md`` document.  Any other file whose stem starts with
    the same ``P5_H*_`` + family prefix joins that family (boundary
    docs, working notes, verifiers, audits).  Files with no family
    prefix match fall back to suffix-stripped slugs at lower
    confidence.
    """
    maps = {}
    for frame in ("H31", "H22"):
        fam = {}
        pat = re.compile(
            rf"^P5_{frame}_(.+?)_(?:COMPONENT_)?GENERIC_OBSTRUCTION\.md$")
        for f in root_files:
            m = pat.match(f)
            if m:
                fam[m.group(1)] = slugify(m.group(1))
        maps[frame] = fam
    return maps["H31"], maps["H22"]


def p5_family_slug(frame: str, stem: str, families: dict) -> tuple:
    """Return (slug, is_generic, matched_prefix) or (None, False, None)."""
    pfx = f"P5_{frame}_"
    if not stem.upper().startswith(pfx):
        return None, False, None
    body = stem[len(pfx):].upper()
    generic = body.endswith(("GENERIC_OBSTRUCTION",))
    best = None
    for fam_prefix in families:
        fp = fam_prefix.upper()
        if body == fp or body.startswith(fp + "_"):
            if best is None or len(fam_prefix) > len(best):
                best = fam_prefix
    if best is not None:
        return families[best], generic, best
    # Fallback: suffix-stripped slug, lower confidence.
    core = body
    for suffix in ("_COMPONENT_GENERIC_OBSTRUCTION",
                   "_GENERIC_OBSTRUCTION", "_OBSTRUCTION",
                   "_VERIFICATION", "_CANDIDATE", "_THEOREM",
                   "_REDUCTION", "_PARTIAL", "_FRONTIER"):
        if core.endswith(suffix):
            core = core[:-len(suffix)]
            break
    core = re.sub(r"_(COMPONENT|OBSTRUCTION|VERIFICATION|CANDIDATE)$",
                  "", core)
    if not core:
        return None, False, None
    return slugify(core), generic, None


def normalize_link_target(base_dir: str, target: str) -> str | None:
    """Resolve *target* against *base_dir* textually (posix).  Returns
    the normalized repo-relative path, or None if it escapes the repo
    or is malformed."""
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


def collect_markdown_links(files: list[str],
                           ref: str | None = None) -> dict:
    """Local markdown links resolved against the source file's dir.
    Resolution is textual, against the tracked-file set, so it works
    for any git ref."""
    fileset = set(files)
    resolved, broken = [], []
    for rel in files:
        if not rel.endswith(".md"):
            continue
        text = read_at(ref, rel)
        base_dir = str(pathlib.PurePosixPath(rel).parent)
        if base_dir == ".":
            base_dir = ""
        for m in MD_LINK.finditer(text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:",
                                  "#")):
                continue
            target = target.split("#", 1)[0].strip()
            if not target or "," in target:
                continue
            if "/" not in target and "." not in target:
                continue
            if target.startswith("tmp/"):
                continue
            norm = normalize_link_target(base_dir, target)
            if norm is not None and norm in fileset:
                resolved.append((rel, norm))
            else:
                broken.append((rel, m.group(1)))
    return {"resolved_count": len(resolved), "broken": broken}


def collect_script_refs(files: list[str],
                        ref: str | None = None) -> dict:
    refs = collections.Counter()
    for rel in files:
        if not rel.endswith(".md"):
            continue
        text = read_at(ref, rel)
        refs.update(SCRIPT_REF.findall(text))
    return refs


def collect_imports(root_mods: set[str], files: list[str],
                    ref: str | None = None) -> dict:
    """Static import graph among root-level python modules."""
    importers = collections.Counter()
    edges = collections.defaultdict(list)
    subprocess_refs = collections.Counter()
    for rel in files:
        if not rel.endswith(".py") or "/" in rel:
            continue
        try:
            tree = ast.parse(read_at(ref, rel))
        except SyntaxError:
            continue
        stem = pathlib.PurePosixPath(rel).stem
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            else:
                continue
            for n in names:
                if n in root_mods and n != stem:
                    importers[n] += 1
                    edges[n].append(rel)
        text = read_at(ref, rel)
        subprocess_refs.update(SUBPROCESS_PY.findall(text))
    return {"importers": importers, "edges": edges,
            "subprocess_refs": subprocess_refs}


def classify(rel: str, ctx: dict) -> dict | None:
    """Return a classification record, or None if no rule applies."""
    p = pathlib.PurePosixPath(rel)
    if "/" in rel:
        return None  # only root files are evacuation candidates here
    name, stem, ext = p.name, p.stem, p.suffix.lower()
    evidence, confidence = [], "high"

    # Status-marker documents.
    if ext == ".md" and WITHDRAWN_RE.search(name):
        return {"old_path": rel,
                "proposed_path": f"claims/legacy/{name}",
                "category": "withdrawn_document",
                "claim_family": "legacy", "confidence": "high",
                "evidence": ["filename WITHDRAWN marker"]}

    ledger_status = ctx["ledger_doc_status"].get(rel)
    # Withdrawn claims go to legacy.  Superseded documents stay with
    # their family package as provenance (claim-package principle), so
    # only withdrawn statuses route here.
    if ledger_status in ("withdrawn", "partially_withdrawn") \
            and ext == ".md":
        return {"old_path": rel,
                "proposed_path": f"claims/legacy/{name}",
                "category": "legacy_document",
                "claim_family": "legacy", "confidence": "high",
                "evidence": [f"theorem ledger status={ledger_status}"]}

    # Navigation/meta documents with fixed destinations.
    fixed_docs = {
        "RESEARCH_NOTES.md": ("docs/research-notes.md", "navigation"),
        "CURRENT_FRONTIER.md": ("docs/current-frontier.md", "navigation"),
        "MERGE_AUDIT_REPORT.md": (
            "docs/audits/MERGE_AUDIT_REPORT.md", "audit_report"),
        "STABILIZATION_AUDIT_REPORT.md": (
            "docs/audits/STABILIZATION_AUDIT_REPORT.md", "audit_report"),
        "LITERATURE_REVIEW_2026-07-30.md": (
            "docs/LITERATURE_REVIEW_2026-07-30.md", "navigation"),
        "SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md": (
            "docs/SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md",
            "navigation"),
        "ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md": (
            "docs/ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md", "navigation"),
        "NEXT_INSTANCE_HANDOFF_2026-07-31.md": (
            "docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md", "navigation"),
        "SPARSE_RESULTANT_CORES_ATTACK_PLAN.md": (
            "docs/architecture/SPARSE_RESULTANT_CORES_ATTACK_PLAN.md",
            "navigation"),
        "GRASSMANNIAN_PLUECKER_ATTACK_PLAN.md": (
            "docs/architecture/GRASSMANNIAN_PLUECKER_ATTACK_PLAN.md",
            "navigation"),
    }
    # The ledger itself moved during the infrastructure phase; it must
    # appear in every move manifest so no tracked source disappears.
    if name == "THEOREM_LEDGER.json":
        return {"old_path": rel,
                "proposed_path": "catalog/theorem-ledger.json",
                "category": "catalog", "claim_family": None,
                "confidence": "high",
                "evidence": ["ledger relocated to catalog/ in the "
                             "infrastructure phase"]}
    if name in fixed_docs:
        dst, cat = fixed_docs[name]
        return {"old_path": rel, "proposed_path": dst, "category": cat,
                "claim_family": None, "confidence": "high",
                "evidence": ["fixed navigation/meta mapping"]}
    if name == "README.md":
        return None  # stays at root by design

    # Claim documents and their named scripts by family prefix.
    if ext in (".md", ".py", ".cpp", ".json"):
        # Finite-order certificates.
        for pfx, dst in ORDER_PREFIX.items():
            if stem.startswith(pfx):
                family = slugify(pfx)
                cat = "claim_document" if ext == ".md" else (
                    "claim_script" if ext == ".py" else "claim_data")
                ev = [f"filename prefix {pfx}_"]
                if ledger_status:
                    ev.append(f"theorem ledger status={ledger_status}")
                if stem in ctx["triples"]:
                    ev.append("part of verify/audit triple")
                    confidence = "high"
                elif ext == ".md":
                    confidence = "medium"
                return {"old_path": rel,
                        "proposed_path": f"{dst}/{name}",
                        "category": cat, "claim_family": f"finite/{family}",
                        "confidence": confidence, "evidence": ev}
        # P5 H31 / H22 packages (family-seeded prefix matching).
        if stem.startswith(("P5_H31_", "verify_p5_h31_",
                            "audit_p5_h31_", "explore_p5_h31_")):
            core = re.sub(r"^(verify|audit|explore)_", "", stem)
            slug, generic, matched = p5_family_slug(
                "H31", core, ctx["h31_families"])
            if slug:
                ev = ["filename prefix P5_H31_ family",
                      f"family slug {slug}"
                      + (f" (matches family '{matched}')"
                         if matched else " (suffix-stripped fallback)")]
                if generic:
                    ev.append("family generic theorem doc")
                if stem in ctx["triples"]:
                    ev.append("part of verify/audit triple")
                if ledger_status:
                    ev.append(f"theorem ledger status={ledger_status}")
                cat = "claim_document" if ext == ".md" else "claim_script"
                high = matched is not None and (
                    len(ev) >= 3 or generic)
                return {"old_path": rel,
                        "proposed_path":
                            f"claims/p5/h31/{slug}/{name}",
                        "category": cat,
                        "claim_family": f"p5/h31/{slug}",
                        "confidence": "high" if high else "medium",
                        "evidence": ev}
        if stem.startswith(("P5_H22_", "verify_p5_h22_",
                            "audit_p5_h22_", "explore_p5_h22_")):
            core = re.sub(r"^(verify|audit|explore)_", "", stem)
            slug, generic, matched = p5_family_slug(
                "H22", core, ctx["h22_families"])
            if slug:
                ev = ["filename prefix P5_H22_ family",
                      f"family slug {slug}"
                      + (f" (matches family '{matched}')"
                         if matched else " (suffix-stripped fallback)")]
                if generic:
                    ev.append("family generic theorem doc")
                if stem in ctx["triples"]:
                    ev.append("part of verify/audit triple")
                if ledger_status:
                    ev.append(f"theorem ledger status={ledger_status}")
                cat = ("claim_document" if ext == ".md"
                       else "claim_script")
                high = matched is not None and (
                    len(ev) >= 3 or generic)
                return {"old_path": rel,
                        "proposed_path":
                            f"claims/p5/h22/{slug}/{name}",
                        "category": cat,
                        "claim_family": f"p5/h22/{slug}",
                        "confidence": "high" if high else "medium",
                        "evidence": ev}
        # Other P5 material.
        if stem.startswith(("P5_", "verify_p5_", "audit_p5_")):
            sub = "frontier"
            low = stem.lower()
            if any(k in low for k in ("boundary", "atlas", "divisor")):
                sub = "boundaries"
            elif any(k in low for k in ("exact_three", "coordinate",
                                        "tree_chart", "cegar")):
                sub = "coordinate-cegar"
            elif any(k in low for k in ("c10", "q4_", "q5_")):
                sub = "frontier"
            cat = ("claim_document" if ext == ".md"
                   else "claim_script" if ext in (".py", ".cpp")
                   else "claim_data")
            ev = ["filename prefix P5_"]
            if ledger_status:
                ev.append(f"theorem ledger status={ledger_status}")
            if stem in ctx["triples"]:
                ev.append("part of verify/audit triple")
            return {"old_path": rel,
                    "proposed_path": f"claims/p5/{sub}/{name}",
                    "category": cat, "claim_family": f"p5/{sub}",
                    "confidence": "medium" if len(ev) >= 2 else "low",
                    "evidence": ev}
        # P4 components.
        if stem.startswith(("P4_", "verify_p4_", "audit_p4_")):
            low = stem.lower()
            if "pure_component" in low:
                # Pure-component claim packages get a per-component
                # directory: theorem doc + verifier + audit live
                # together in claims/p4/components/<component>/.
                slug = low
                for prefix in ("verify_", "audit_"):
                    if slug.startswith(prefix):
                        slug = slug[len(prefix):]
                for suffix in ("_pure_component",):
                    if slug.endswith(suffix):
                        slug = slug[:-len(suffix)]
                # match the H22 pilot dash convention and drop the
                # redundant p4_ prefix (already under claims/p4/).
                if slug.startswith("p4_"):
                    slug = slug[len("p4_"):]
                slug = slug.replace("_", "-")
                sub = "components"
                dest = f"claims/p4/components/{slug}/{name}"
                family = f"p4/components/{slug}"
                conf = "high"
            elif any(k in low for k in ("classification", "exhaustion",
                                        "reduction", "census",
                                        "component")):
                sub = "classifications"
                dest = f"claims/p4/{sub}/{name}"
                family = f"p4/{sub}"
                conf = None
            else:
                sub = "boundaries"
                dest = f"claims/p4/{sub}/{name}"
                family = f"p4/{sub}"
                conf = None
            cat = ("claim_document" if ext == ".md"
                   else "claim_script" if ext in (".py", ".cpp")
                   else "claim_data")
            ev = ["filename prefix P4_"]
            if ledger_status:
                ev.append(f"theorem ledger status={ledger_status}")
            if stem in ctx["triples"]:
                ev.append("part of verify/audit triple")
            if conf is None:
                conf = "medium" if len(ev) >= 2 else "low"
            return {"old_path": rel,
                    "proposed_path": dest,
                    "category": cat, "claim_family": family,
                    "confidence": conf,
                    "evidence": ev}
        # P6 / P7.
        if stem.startswith(("P6_", "verify_p6_", "audit_p6_")):
            cat = "claim_document" if ext == ".md" else "claim_script"
            ev = ["filename prefix P6_"]
            if ledger_status:
                ev.append(f"theorem ledger status={ledger_status}")
            return {"old_path": rel,
                    "proposed_path": f"claims/p6/{name}",
                    "category": cat, "claim_family": "p6",
                    "confidence": "medium", "evidence": ev}
        if stem.startswith(("P7_", "verify_p7_", "audit_p7_")):
            cat = "claim_document" if ext == ".md" else "claim_script"
            ev = ["filename prefix P7_"]
            if ledger_status:
                ev.append(f"theorem ledger status={ledger_status}")
            return {"old_path": rel,
                    "proposed_path": f"claims/p7/{name}",
                    "category": cat, "claim_family": "p7",
                    "confidence": "medium", "evidence": ev}
        # Arbitrary-order analytic results.
        if any(stem.startswith(p) for p in ARBITRARY_PREFIXES):
            cat = ("claim_document" if ext == ".md"
                   else "claim_script" if ext in (".py", ".cpp")
                   else "claim_data")
            ev = ["filename prefix in arbitrary-order family"]
            if ledger_status:
                ev.append(f"theorem ledger status={ledger_status}")
            if stem in ctx["triples"]:
                ev.append("part of verify/audit triple")
            return {"old_path": rel,
                    "proposed_path": f"claims/arbitrary-order/{name}",
                    "category": cat, "claim_family": "arbitrary-order",
                    "confidence": "medium" if len(ev) >= 2 else "low",
                    "evidence": ev}

    # Scripts by tool prefix.
    if ext == ".py":
        if any(stem.startswith(p) for p in TOOL_EXPLORE_PREFIXES):
            ev = ["tool prefix (exploration/derivation)"]
            if ledger_status:
                ev.append(f"theorem ledger status={ledger_status}")
            return {"old_path": rel,
                    "proposed_path": f"tools/explore/{name}",
                    "category": "tool_script", "claim_family": None,
                    "confidence": "medium", "evidence": ev}
        if any(stem.startswith(p) for p in TOOL_GENERATE_PREFIXES):
            return {"old_path": rel,
                    "proposed_path": f"tools/generate/{name}",
                    "category": "tool_script", "claim_family": None,
                    "confidence": "medium",
                    "evidence": ["tool prefix (generation/replay)"]}
        if stem.startswith("package_"):
            return {"old_path": rel,
                    "proposed_path": f"tools/package/{name}",
                    "category": "tool_script", "claim_family": None,
                    "confidence": "medium",
                    "evidence": ["tool prefix package_"]}
        # Shared library modules: imported by many root scripts.
        if ctx["importers"].get(stem, 0) >= 3:
            return {"old_path": rel,
                    "proposed_path": f"src/krenn_gu/{name}",
                    "category": "shared_library", "claim_family": None,
                    "confidence": "medium",
                    "evidence": [
                        f"imported by {ctx['importers'][stem]} root "
                        "scripts"]}

    # Figures.
    if ext in (".png", ".svg"):
        return {"old_path": rel,
                "proposed_path": f"docs/figures/{name}",
                "category": "figure", "claim_family": None,
                "confidence": "medium",
                "evidence": ["figure referenced from claim documents"]}

    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--ref", default=None,
        help="git ref to inspect (tag/branch/commit); defaults to the "
             "working tree. The pre-migration inventory must be built "
             "from --ref pre-layout-migration-v1.")
    args = ap.parse_args()
    ref = resolve_ref(args.ref) if args.ref else None
    files = tracked_files(ref)
    root_files = [f for f in files if "/" not in f]
    root_dirs = sorted({f.split("/")[0] for f in files if "/" in f})
    root_mods = {pathlib.PurePosixPath(f).stem
                 for f in root_files if f.endswith(".py")}

    ledger = load_ledger(files, ref)
    ledger_doc_status = {}
    ledger_refs = []
    for e in ledger.get("entries", []):
        doc = e.get("document", "").split(" (")[0]
        ledger_doc_status[doc] = e.get("status")
        for key in ("document", "primary_verifier", "independent_audit"):
            v = e.get(key)
            if v:
                ledger_refs.append(v)

    # verify/audit triples inferred from naming.
    names = set(root_files)
    triples = {}
    for f in root_files:
        if f.endswith(".md") and not f.startswith(("verify_", "audit_")):
            stem = f[:-3]
            v, a = f"verify_{stem.lower()}.py", f"audit_{stem.lower()}.py"
            have = [x for x in (v, a) if x in names]
            if have:
                triples[stem] = have

    links = collect_markdown_links(files, ref)
    script_refs = collect_script_refs(files, ref)
    graph = collect_imports(root_mods, files, ref)

    h31_families, h22_families = build_family_maps(root_files)
    ctx = {"ledger_doc_status": ledger_doc_status, "triples": triples,
           "importers": graph["importers"],
           "h31_families": h31_families,
           "h22_families": h22_families}

    classified, unclassified = [], []
    for rel in sorted(root_files):
        rec = classify(rel, ctx)
        if rec is None:
            unclassified.append(rel)
        else:
            classified.append(rec)

    # Second pass: orphan verify_/audit_/certify_ scripts follow their
    # document when the pairing is exact (same stem, case-insensitive).
    doc_dest = {}
    for c in classified:
        if c["category"] in ("claim_document", "withdrawn_document",
                             "legacy_document"):
            doc_dest[pathlib.PurePosixPath(
                c["old_path"]).stem.lower()] = c
    paired, still_unclassified = [], []
    for rel in unclassified:
        p = pathlib.PurePosixPath(rel)
        if p.suffix == ".py" and p.stem.split("_", 1)[0] in (
                "verify", "audit", "certify"):
            base = p.stem
            for role in ("verify_", "audit_", "certify_"):
                if base.startswith(role):
                    base = base[len(role):]
                    break
            doc = doc_dest.get(base.lower())
            if doc is not None:
                dst_dir = str(pathlib.PurePosixPath(
                    doc["proposed_path"]).parent)
                paired.append({
                    "old_path": rel,
                    "proposed_path": f"{dst_dir}/{p.name}",
                    "category": "claim_script",
                    "claim_family": doc["claim_family"],
                    "confidence": "high",
                    "evidence": [
                        "exact name pairing with classified document",
                        f"paired doc {doc['old_path']}"],
                })
                continue
        still_unclassified.append(rel)
    classified.extend(paired)
    unclassified = still_unclassified

    ext_counts = collections.Counter(
        pathlib.PurePosixPath(f).suffix.lower() for f in root_files)
    fam_counts = collections.Counter(
        c["claim_family"] for c in classified if c["claim_family"])
    cat_counts = collections.Counter(c["category"] for c in classified)
    conf_counts = collections.Counter(c["confidence"] for c in classified)

    CATALOG.mkdir(exist_ok=True)
    (DOCS / "architecture").mkdir(parents=True, exist_ok=True)

    classification = {
        "generated_by": "tools/migration/inventory_layout.py",
        "inspected_ref": args.ref,
        "starting_commit": ref if ref else subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT,
            capture_output=True, text=True).stdout.strip(),
        "total_tracked_entries": len(files),
        "root_level_files": len(root_files),
        "root_level_directories": root_dirs,
        "github_root_entries": len(root_files) + len(root_dirs),
        "root_files_by_extension": dict(ext_counts),
        "classification_counts_by_family": dict(fam_counts),
        "classification_counts_by_category": dict(cat_counts),
        "confidence_counts": dict(conf_counts),
        "classified_count": len(classified),
        "unclassified_count": len(unclassified),
        "estimated_root_entries_after_full_migration":
            len([f for f in root_files if f in
                 {u for u in unclassified}])
            + len(root_dirs)
            + 1  # README.md stays
            + len({"pyproject.toml", "CONTRIBUTING.md", "CITATION.cff",
                   "LICENSE"}),  # planned additions, at most
        "verify_audit_triples": {k: v for k, v in sorted(triples.items())},
        "ledger_references": sorted(set(ledger_refs)),
        "markdown_local_links_resolved": links["resolved_count"],
        "markdown_broken_links": [
            {"source": s, "target": t} for s, t in links["broken"]],
        "script_references_in_markdown": dict(script_refs),
        "subprocess_script_references": dict(graph["subprocess_refs"]),
        "shared_library_candidates": {
            k: v for k, v in sorted(graph["importers"].items(),
                                    key=lambda kv: -kv[1]) if v >= 3},
        "entries": classified,
    }
    (CATALOG / "layout-classification.json").write_text(
        json.dumps(classification, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (CATALOG / "unclassified-files.json").write_text(
        json.dumps({"unclassified_count": len(unclassified),
                    "note": "no rule classified these files; each needs "
                            "an explicit human decision",
                    "files": unclassified},
                   indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")

    md = []
    md.append("# Layout inventory (pre-migration)\n")
    md.append(f"Starting commit: `{classification['starting_commit']}` "
              "(tag `pre-layout-migration-v1`).\n")
    md.append("## Headline counts\n")
    md.append(f"- total tracked entries: **{len(files)}**")
    md.append(f"- root-level files: **{len(root_files)}** "
              f"(+ {len(root_dirs)} directories = "
              f"{classification['github_root_entries']} entries, "
              "GitHub truncates at 1,000)")
    md.append(f"- classified by rules: **{len(classified)}** "
              f"({dict(conf_counts)})")
    md.append(f"- unclassified (need human decision): "
              f"**{len(unclassified)}**\n")
    md.append("## Root files by extension\n")
    for ext, n in ext_counts.most_common():
        md.append(f"- `{ext or '(none)'}`: {n}")
    md.append("\n## Top-level directories\n")
    for d in root_dirs:
        md.append(f"- `{d}/`")
    md.append("\n## Classification by destination family (top 30)\n")
    for fam, n in fam_counts.most_common(30):
        md.append(f"- `{fam}`: {n}")
    md.append("\n## Classification by category\n")
    for cat, n in cat_counts.most_common():
        md.append(f"- `{cat}`: {n}")
    md.append("\n## Shared-library candidates (imported by >=3 root "
              "scripts)\n")
    for mod, n in sorted(graph["importers"].items(),
                         key=lambda kv: -kv[1]):
        if n >= 3:
            md.append(f"- `{mod}.py`: {n} importers")
    md.append("\n## Markdown link health\n")
    md.append(f"- resolved local links: {links['resolved_count']}")
    md.append(f"- broken local links: {len(links['broken'])}")
    for item in links["broken"][:20]:
        md.append(f"  - `{item['source']}` -> `{item['target']}`")
    md.append(f"\n## verify/audit triples inferred from naming: "
              f"{len(triples)}\n")
    md.append(f"## Unclassified root files: {len(unclassified)}\n")
    md.append("See `catalog/unclassified-files.json` for the complete "
              "list.\n")
    (DOCS / "architecture" / "layout-inventory.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8")

    print(f"tracked={len(files)} root_files={len(root_files)} "
          f"classified={len(classified)} unclassified={len(unclassified)}")
    print(f"broken markdown links: {len(links['broken'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
