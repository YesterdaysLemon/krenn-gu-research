"""Shared repository path discovery for the Krenn-Gu migration.

Introduced by the root-evacuation migration (Phase 3).  Use this only
where genuinely shared path discovery is needed; self-contained
verifiers that resolve everything relative to ``__file__`` should keep
doing so.  This module itself has no third-party dependencies.

The migration deliberately does NOT refactor every script into a
package; the objective is path portability, not software redesign.
"""

from pathlib import Path

# src/krenn_gu/paths.py -> parents[2] is the repository root.
REPO_ROOT = Path(__file__).resolve().parents[2]
CLAIMS_ROOT = REPO_ROOT / "claims"
DOCS_ROOT = REPO_ROOT / "docs"
CATALOG_ROOT = REPO_ROOT / "catalog"
TOOLS_ROOT = REPO_ROOT / "tools"
SNAPSHOTS_ROOT = REPO_ROOT / "research_snapshots"
THEOREM_LEDGER = CATALOG_ROOT / "theorem-ledger.json"


def claim_package(family: str) -> Path:
    """Directory of a claim package, e.g.
    claim_package('p5/h22/disjoint-mixed-star')."""
    return CLAIMS_ROOT / family
