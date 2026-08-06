"""Claim-package metadata resolver (Phase 2, item 1B).

The ledger schema for a claim document is::

    claim_package = claims/p5/h22/disjoint-mixed-star   (package root)
    proof_variant = alternate | canonical | null
    subpackage    = alternate | boundaries | null

This module derives all three STRUCTURALLY.  It never guesses from
arbitrary path depth:

  1. if the path is the source or destination of a manifest move that
     carries a ``claim_family``, the family defines the package root;
  2. otherwise the path is parsed against the well-defined package
     structure: ``claims/<family...>[/(alternate|boundaries)]/<file>``,
     where the deepest directory that is not a known subpackage name is
     the last family component.

``proof_variant`` is assigned only to markdown documents:

  - ``alternate`` for ``.md`` files inside the ``alternate/``
    subpackage (an independent proof of the same claim);
  - ``canonical`` for ``.md`` files directly at the package root that
    are not working notes;
  - ``null`` otherwise (verifiers, audits, boundary documents, working
    notes, exploration scripts).

This preserves the independence of alternate proofs: an alternate
theorem keeps its own package root and is distinguished only by
``proof_variant``/``subpackage``, never by a different
``claim_package``.
"""

from __future__ import annotations

import pathlib

SUBPACKAGES = ("alternate", "boundaries")

# Suffix marking a working note rather than a theorem document.
_WORKING_NOTE_SUFFIX = "_WORKING_NOTE"


def resolve_claim_package_metadata(path, manifest_moves=None):
    """Return ``{"claim_package", "proof_variant", "subpackage"}`` for a
    claims/ path, or None for anything outside claims/.

    ``manifest_moves`` is the manifest's ``moves`` list (used for the
    authoritative ``claim_family`` when available).
    """
    p = pathlib.PurePosixPath(str(path).replace("\\", "/"))
    parts = p.parts
    if not parts or parts[0] != "claims" or len(parts) < 2:
        return None

    # 1. manifest claim_family (authoritative when present).
    family = None
    if manifest_moves:
        for m in manifest_moves:
            if m.get("new_path") == str(p) or m.get("old_path") == str(p):
                fam = m.get("claim_family")
                if fam:
                    family = fam
                    break

    # 2. structural parse: family = every directory component except
    #    known subpackage names.
    if family is None:
        dirs = parts[1:-1]
        fam_dirs = [d for d in dirs if d not in SUBPACKAGES]
        if not fam_dirs:
            return None
        family = "/".join(fam_dirs)

    claim_package = "claims/" + family

    # Subpackage: directory between the family root and the file.
    fam_parts = family.split("/")
    rest = parts[1:-1][len(fam_parts):]
    subpackage = rest[0] if rest and rest[0] in SUBPACKAGES else None

    # Proof variant: markdown theorem documents only.
    proof_variant = None
    name = parts[-1]
    if name.endswith(".md"):
        stem = pathlib.PurePosixPath(name).stem
        if subpackage == "alternate":
            proof_variant = "alternate"
        elif subpackage is None and not stem.endswith(
                _WORKING_NOTE_SUFFIX):
            proof_variant = "canonical"

    return {
        "claim_package": claim_package,
        "proof_variant": proof_variant,
        "subpackage": subpackage,
    }
